"""Dashboard server: the static page, the gallery files, and upload analysis jobs.

    python -m cvoice.app [--host 127.0.0.1] [--port 7860] [--gallery DIR]

The port defaults to the PORT environment variable when it is set (hosting platforms set it), else 7860.

    GET  /api/health                       uploads possible? limits; which gallery examples can be fixed; stage names;
                                           report_url (the technical report, or null when the PDF is missing)
    GET  /report                           the technical report (docs/technical.pdf), shown in the browser
    POST /api/analyze                      multipart: audio, transcript (text) or transcript_file, and baseline_id or
                                           baseline_audio (one to MAX_REFERENCES files: the user's own reference bank, the
                                           first one shown) or neither (no reference reading: the SELF mode)
    POST /api/jobs/{id}/fix                JSON {"finding": index in result.flaws} or {"all": true}, optional "pitch_method":
                                           fix the finding(s) of a finished analysis on its own recording, then re-analyse
    POST /api/gallery/{item}/fix           the same for a bundled example
    GET  /api/jobs/{id}                    {kind, state, stage (on error: the stage that failed), stages, stage_labels, error?;
                                           analysis: result?, reference?; fix: audio?, fix?}
    GET  /api/jobs/{id}/result.json        the analysis result JSON
    GET  /api/jobs/{id}/{participant|baseline|fixed}.wav   the decoded audio the analysis used, or the fixed audio (Range-capable)
    /gallery/...  /                        static files (gallery data, then the page)

Regime rule: a bundled dataset clip against its own baseline is R1; anything else is R2. An upload is never a
bundled clip, so every upload with a reference is analysed as R2, and an upload without one as SELF. A bundled baseline
with `references` (a reference bank) is passed to the pipeline as its bank, and so are two or more uploaded reference
recordings; the pipeline selects the reference mode, and a finished job states the mode it used (`reference`).

Analysis and fix jobs share one queue: one job at a time. A fix job re-analyses with the inputs of its analysis (the
decoded recordings and the transcript stay in the analysis job folder), so the scores before and after are comparable
when the reproduction check passes (fix_summary gives the fix job's JSON).
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import os
import re
import shutil
import tempfile
import threading
import time
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import __version__, audio, repair
from . import config as C
from .align import MISMATCH_PART, MISMATCH_SHORT, Transcript, TranscriptError, TranscriptMismatch, parse_transcript
from .detect import load_detector, scale, threshold
from .pipeline import DEFAULT_DETECTOR, REPORT_PDF, ROOT, analyze, dumps
from .selfref import DEFAULT_DETECTOR as SELF_DETECTOR
from .selfref import NAME as SELF_REGIME

GALLERY = ROOT / "gallery"
STATIC = Path(__file__).parent / "static"
REPORT_URL = "report"  # relative to the page, as the api/ URLs are
STAGES = ("decode", "align", "features", "compare", "detect")
FIX_STAGES = ("edit", "check")
STAGE_LABELS = {"decode": "Reading the audio", "align": "Finding each word", "features": "Measuring the delivery",
                "compare": "Comparing", "detect": "Finding the spots to work on",
                "edit": "Editing your recording", "check": "Checking the result"}
UPLOAD_REGIME = "R2"
TRANSCRIPT_MAX_CHARS = 20_000  # characters; Starlette would accept 1 MB per text field
JOB_TTL_S = 3600  # s, finished jobs and their files are swept after this
TRANSCRIPT_HINT = "The transcript must be the exact words both recordings read."
REFERENCE_FIELDS = ("reference_mode", "reference_count", "references_available")  # result.detection fields of the job status
MAX_REFERENCES = C.CONSENSUS_K  # the pipeline uses at most CONSENSUS_K readings, so more uploads would only cost time
# Rows whose flag threshold is a plain physical change (speed factor, seconds, dB); pitch range has a regularising offset.
LIMIT_ROWS = {"D1": "pace", "D2": "pauses", "D5": "volume"}
MODE_REGIMES = {"single": "R2", "consensus5": "R2_consensus"}  # detector.json regime entry of each upload reference mode
LISTEN_CONTEXT_S = 1.0  # s of audio before and after a fixed region in the page's looping player
BUSY = "Another analysis or fix is running. Try again when it has finished."
# Plain words of a fix that stopped short of its target or was skipped, by repair.Fix cause. The caps are chosen limits,
# not measured thresholds, so the words say "could".
CAUSE_WORDS = {
    repair.CAP: "A larger change could sound processed, so the edit stops part of the way.",
    repair.HEADROOM: "A louder edit would clip the recording, so the edit stops part of the way.",
    repair.SHARED_CAP: "Other fixes already change these words about as far as they can go before they could sound processed.",
    repair.FLAT_PITCH: "Your pitch here is too flat to widen enough within natural limits.",
    repair.INAUDIBLE: "The change allowed here is probably too small to hear.",
}
STILL_FLAGGED_WORDS = "The edit changed this spot, but it is still flagged."
# Below this share of the wanted change, a still-flagged edit is reported as skipped: a chosen limit, not a measured one.
MIN_HEARD_SHARE = 0.10
FLOOR_WORDS = "The pause is now shorter than the shortest pause the analysis measures, so it is no longer compared."
# What each kind of edit leaves unchanged; vocal effort is not gain: docs/PAPERS.md #69.
LIMIT_WORDS = {
    "gain": "A level change does not restore vocal effort, so these words can still sound weak.",
    "pause_insert": "An added silence has no slowing or pitch fall before it, so the break can sound abrupt.",
    "emphasis": "The size of an emphasis edit was checked only against the same speaker's own recording.",
}
SELF_CAUTION = ("Closer to your typical delivery. Without a reference reading, some flagged spots may be natural phrasing, "
                "so listen before you change how you read.")
CHECK_LABELS = {
    "reproduced": "Your unedited recording analysed again gives the same result, so before and after can be compared.",
    "alignment": "Every word of the edited recording is found where the edit moved it.",
    "pitch_trackers": "Two pitch trackers agree on how much the pitch range changed.",
}
NOT_REPRODUCED_WORDS = ("Your unedited recording analysed again did not give the same result, so the scores before and "
                        "after are not compared.")
SELF_SCORE_WORDS = "Without a reference reading, the result counts flagged spots instead of a score."
CONTOUR_SELF_WORDS = "The reference's melody needs a reference reading, and this analysis has none."


def max_request_bytes() -> int:
    """Request body cap: every file of a full upload (yours and MAX_REFERENCES references) may reach the per-file limit."""
    return C.MAX_UPLOAD_BYTES * (1 + MAX_REFERENCES)


# ============================================================================================ guards
class BodySizeLimit:
    """Pure-ASGI cap on request body bytes: Starlette spools uploaded file parts to disk with no size limit."""

    def __init__(self, app, max_bytes: int):
        self.app, self.max_bytes = app, max_bytes

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["method"] not in ("POST", "PUT", "PATCH"):
            return await self.app(scope, receive, send)
        declared = dict(scope["headers"]).get(b"content-length")
        if declared and declared.isdigit() and int(declared) > self.max_bytes:
            body = json.dumps({"detail": f"Upload larger than {self.max_bytes // 2**20} MB."}).encode()
            await send({"type": "http.response.start", "status": 413,
                        "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode()),
                                    (b"connection", b"close")]})
            return await send({"type": "http.response.body", "body": body})
        seen = 0

        async def limited_receive():  # chunked bodies and lying Content-Length headers
            nonlocal seen
            message = await receive()
            if message["type"] == "http.request":
                seen += len(message.get("body", b""))
                if seen > self.max_bytes:
                    raise StarletteHTTPException(413, f"Upload larger than {self.max_bytes // 2**20} MB.")
            return message

        await self.app(scope, limited_receive, send)


def read_transcript(text: str, file: UploadFile | None) -> str:
    """The transcript field or file (the file wins when both are sent); 422 when empty, too long or not UTF-8."""
    if file is not None and file.size:
        try:
            text = file.file.read().decode("utf-8")
        except UnicodeDecodeError as e:
            raise HTTPException(422, "The transcript file is not UTF-8 text.") from e
    if not text.strip():
        raise HTTPException(422, "The transcript is empty.")
    if len(text) > TRANSCRIPT_MAX_CHARS:
        raise HTTPException(422, f"The transcript is longer than {TRANSCRIPT_MAX_CHARS} characters.")
    return text


def bundled_baselines(gallery: Path) -> dict[str, dict]:
    """The gallery's bundled baselines by id, each {id, title, audio, text, references?}; an index without `baselines` has
    its one `baseline`."""
    index = json.loads((gallery / "index.json").read_text())
    return {b["id"]: b for b in index.get("baselines") or [index["baseline"]]}


def bundled_text_words(baseline: dict) -> str:
    """The refusal of a transcript that is not the fixed text of a bundled reference (one reading or a bank)."""
    return f"The transcript is not the text of the reference '{baseline['title']}'. Use that text, or choose another reference."


def bundled_choice(gallery: Path, baseline_id: str, tr: Transcript) -> dict:
    """The bundled baseline with its audio paths; 422 for an unknown id, or when its fixed text differs from the
    transcript (checked before any audio is read, for one reading and for a bank alike)."""
    baseline = bundled_baselines(gallery).get(baseline_id)
    if baseline is None:
        raise HTTPException(422, f"Unknown baseline '{baseline_id}'.")
    if parse_transcript(baseline["text"]).norm != tr.norm:
        raise HTTPException(422, bundled_text_words(baseline))
    baseline = {**baseline, "wav": gallery / baseline["audio"]}
    if baseline.get("references"):
        baseline["reference_wavs"] = [gallery / r["audio"] for r in baseline["references"]]
    return baseline


def smallest_flagged(regime: dict, dim: str, sign: int) -> float | None:
    """threshold x scale: the smallest flagged change of one direction, as in a result row's `tol`; None where it is not flagged."""
    h = threshold(regime, dim, sign)
    if h is None or dim not in regime["enabled"]:
        return None
    return round(float(h * scale(regime, dim, sign)), 6)


def flag_limits(regime: dict) -> dict[str, list[float | None]]:
    """[below, above] per LIMIT_ROWS row, in the shape of a result row's `tol`."""
    return {row: [smallest_flagged(regime, dim, sign) for sign in (-1, 1)] for dim, row in LIMIT_ROWS.items()}


def upload_limits(detector: Path) -> dict:
    """flag_limits per upload reference mode; empty when the detector is missing or has no such regimes."""
    if not detector.exists():
        return {}
    regimes = load_detector(detector).get("regimes", {})
    return {mode: flag_limits(regimes[name]) for mode, name in MODE_REGIMES.items() if name in regimes}


def reference_uploads(files: list[UploadFile] | None) -> list[UploadFile]:
    """The non-empty reference files; 422 above MAX_REFERENCES."""
    files = [f for f in files or [] if f.size is not None and f.size > 0]
    if len(files) > MAX_REFERENCES:
        raise HTTPException(422, f"Upload at most {MAX_REFERENCES} reference recordings of the same text.")
    return files


def too_large_words(who: str) -> str:
    return f"{who} is larger than {C.MAX_UPLOAD_BYTES // 2**20} MB."


def unsupported_words(who: str) -> str:
    return f"{who} could not be read as audio. Use wav, mp3, m4a, ogg, flac or webm."


def check_sizes(files: list[tuple[UploadFile | None, str]]) -> None:
    """413 naming the first file (file, words of its name) above the per-file limit (the body cap allows several files)."""
    for file, who in files:
        if file is not None and file.size is not None and file.size > C.MAX_UPLOAD_BYTES:
            raise HTTPException(413, too_large_words(who))


def reference_names(count: int) -> list[str]:
    """Server-chosen file names of the uploaded references; upload_label turns a name into the words of an error message."""
    return ["reference recording"] if count == 1 else [f"reference recording {k + 1}" for k in range(count)]


def decoded_reference_names(count: int) -> list[str]:
    """File names of the decoded references in the job folder; the first is the one the page plays."""
    return ["baseline.wav", *(f"reference_{k + 1}.wav" for k in range(1, count))]


def save_upload(file: UploadFile, dest: Path) -> None:
    """Write an upload under a server-chosen name and sniff its magic bytes; 415 naming the file when it is not audio."""
    with dest.open("wb") as fh:
        shutil.copyfileobj(file.file, fh)
    try:
        audio.sniff(dest)
    except audio.AudioError as e:
        raise HTTPException(415, unsupported_words(upload_label(dest.name))) from e


# ============================================================================================ plain errors
LOG = logging.getLogger("cvoice.app")
ANALYSIS_FAILED = "The analysis stopped because of an error on the server. Try again."
FIX_FAILED = "The fix stopped because of an error on the server. Try again."


class InputProblem(Exception):
    """A refusal of one input in plain words for the user; the technical cause is chained and goes to the server log."""


def upload_label(name: str) -> str:
    """The user's name of an uploaded file from its server-chosen name: "your recording" or "reference recording [k]"."""
    return "Your recording" if name == "your recording" else f"Your {name}"


def audio_words(e: audio.AudioError, who: str) -> str:
    """Plain words of a decode refusal of the file `who` ("Your recording", "Your reference recording 2")."""
    seconds = f"{C.MAX_UPLOAD_S:.0f} s"
    return {
        audio.DECODE_TIMEOUT: f"{who} took too long to read. Save it as wav or mp3 and upload it again.",
        audio.CHANNELS: f"{who} has more than two channels. Use a mono or stereo recording.",
        audio.TOO_LARGE: too_large_words(who),
        audio.TOO_LONG: f"{who} is longer than {seconds}. Use a recording of {seconds} or less.",
        audio.TOO_SHORT: f"{who} is shorter than {audio.MIN_SECONDS:.0f} s. Upload a recording of the whole text.",
    }.get(e.kind, unsupported_words(who))


def load_upload(folder: Path, name: str):
    """Decode one upload of the job folder; InputProblem in plain words when it cannot be used."""
    try:
        return audio.load_audio(folder / name, C.MAX_UPLOAD_BYTES, C.MAX_UPLOAD_S)[0]
    except audio.AudioError as e:
        raise InputProblem(audio_words(e, upload_label(name))) from e


def too_short_words(who: str, needed_s: float | None) -> str:
    needed = "" if needed_s is None else f": at least {math.ceil(needed_s)} seconds of speech is needed"
    return f"{who} is too short for this transcript{needed}."


def mismatch_sentence(e: TranscriptMismatch, who: str) -> str:
    """The first sentence of a transcript refusal of the recording `who` ("Your recording", "Your reference recording 2")."""
    if e.kind == MISMATCH_SHORT:
        return too_short_words(who, e.needed_s)
    lower = who[:1].lower() + who[1:]
    if e.kind == MISMATCH_PART:
        where = "" if e.at_s is None else f" (at about {e.at_s:.0f} s, near '{e.near}')"
        return f"Part of the transcript does not match {lower}{where}."
    return f"The words in {lower} do not match the transcript."


BRACKET_HINT = "Words in brackets or parentheses count as not read aloud."


def bracket_hint(text: str, e: TranscriptMismatch) -> str:
    """parse_transcript drops bracketed text as stage directions, so a partial mismatch of a transcript with brackets may
    come from words that were read inside them."""
    return f" {BRACKET_HINT}" if e.kind == MISMATCH_PART and re.search(r"[\[(]", text) else ""


def own_reference_label(role: str, own_count: int) -> str:
    """"Your reference recording [k]" of a refused role: the baseline is the first upload, "reference k" the k-th."""
    k = 1 if role == "baseline" else int(role.split()[-1])
    return upload_label(reference_names(own_count)[k - 1])


def mismatch_words(e: TranscriptMismatch, baseline: dict | None, own_count: int) -> str:
    """Plain words of a transcript refusal that name the input to correct. The user's own recording comes first; a
    bundled reference reads a fixed text, so its refusal asks for that text. An error without roles is the user's."""
    roles = e.roles or ("participant",)
    if "participant" in roles:
        also = ""
        if "baseline" in roles:
            who = "The reference reading" if baseline is not None else own_reference_label("baseline", own_count)
            also = f" {who} does not match the transcript either."
        return f"{mismatch_sentence(e, 'Your recording')} Check that the transcript is the exact text you read.{also}"
    if baseline is not None:
        return bundled_text_words(baseline)
    return f"{mismatch_sentence(e, own_reference_label(roles[0], own_count))} {TRANSCRIPT_HINT}"


# ============================================================================================ jobs
@dataclass(frozen=True)
class FixSource:
    """The inputs of one analysis that a fix needs to re-analyse the edited recording the same way: canonical WAV files,
    the transcript text and the regime. baseline and references are None in the SELF mode."""
    participant: Path
    result: Path
    transcript: str
    regime: str
    baseline: Path | None = None
    references: tuple[Path, ...] | None = None


class Jobs:
    """In-memory job table with one worker thread for analysis and fix jobs. Known limit: jobs are lost on restart and the
    table is wrong with more than one uvicorn worker, so main() starts one worker."""

    def __init__(self, work: Path):
        self.work, self.table = work, {}
        self.cache = work / "align-cache"  # alignments by audio and text hash: a fix re-analyses the unedited recording
        self.cache.mkdir(parents=True, exist_ok=True)
        self.pool = ThreadPoolExecutor(max_workers=1)
        self.lock = threading.Lock()

    def sweep(self) -> None:
        for jid in [k for k, j in self.table.items() if j["state"] in ("done", "error") and time.monotonic() - j["born"] > JOB_TTL_S]:
            shutil.rmtree(self.work / jid, ignore_errors=True)
            del self.table[jid]
        for cached in self.cache.glob("*.npz"):
            if time.time() - cached.stat().st_mtime > JOB_TTL_S:
                cached.unlink(missing_ok=True)

    def new(self, kind: Literal["analysis", "fix"] = "analysis") -> tuple[str, Path] | None:
        """A fresh job id and folder, or None while another job is queued or running."""
        with self.lock:
            if any(j["state"] in ("queued", "running") for j in self.table.values()):
                return None
            self.sweep()
            jid = uuid.uuid4().hex  # server-generated: no client file name is ever used
            (self.work / jid).mkdir()
            stage = STAGES[0] if kind == "analysis" else FIX_STAGES[0]
            self.table[jid] = {"kind": kind, "state": "queued", "stage": stage, "born": time.monotonic()}
            return jid, self.work / jid


def run_job(job: dict, folder: Path, text: str, baseline: dict | None, detector: Path, own_count: int = 0,
            cache_dir: Path | None = None) -> None:
    """Worker: decode, analyse as R2 (against the bank when the baseline has one or the user uploaded two or more references)
    or, without any reference, as SELF; write result.json and keep the decoded inputs for a fix (job["source"]).
    text: the transcript as sent; own_count: number of uploaded references (baseline is None then). Every failure becomes a
    plain message on the job."""
    try:
        job.update(state="running", stage="decode")
        tr = parse_transcript(text)
        participant_wav = load_upload(folder, "your recording")
        audio.write_wav(folder / "participant.wav", participant_wav)
        participant_meta = {"id": folder.name, "title": "Your recording", "audio": f"api/jobs/{folder.name}/participant.wav"}
        common = {"participant_meta": participant_meta, "progress": lambda stage: job.update(stage=stage), "refuse_mismatch": True,
                  "cache_dir": cache_dir}
        source = {"participant": folder / "participant.wav", "result": folder / "result.json", "transcript": text}
        if baseline is None and own_count == 0:
            res = analyze(participant_wav, tr, regime=SELF_REGIME, **common)
            source = FixSource(**source, regime=SELF_REGIME)
        else:
            if baseline is None:
                own = [load_upload(folder, name) for name in reference_names(own_count)]
                paths = [folder / name for name in decoded_reference_names(own_count)]
                for path, wav in zip(paths, own):
                    audio.write_wav(path, wav)
                references, reference_wav, reference_paths = (own if len(own) > 1 else None), own[0], paths
                baseline_meta = {"id": "uploaded_baseline", "title": "Your baseline recording", "audio": f"api/jobs/{folder.name}/baseline.wav"}
            else:
                reference_paths = list(baseline.get("reference_wavs") or [baseline["wav"]])
                references = [audio.read_wav(p) for p in baseline["reference_wavs"]] if baseline.get("reference_wavs") else None
                reference_wav = references[0] if references else audio.read_wav(baseline["wav"])
                baseline_meta = {"id": baseline["id"], "title": baseline["title"], "audio": f"gallery/{baseline['audio']}"}
            res = analyze(participant_wav, tr, reference_wav, regime=UPLOAD_REGIME, detector=load_detector(detector), baseline_meta=baseline_meta,
                          references=references, **common)
            source = FixSource(**source, regime=UPLOAD_REGIME, baseline=reference_paths[0],
                               references=tuple(reference_paths) if references is not None else None)
        (folder / "result.json").write_text(dumps(res) + "\n")
        detection = res.get("detection", {})
        job.update(state="done", stage="done", reference={k: detection.get(k) for k in REFERENCE_FIELDS}, source=source)
    except InputProblem as e:
        LOG.warning("analysis %s refused: %s (%s)", folder.name, e, e.__cause__)
        job.update(state="error", error=str(e))
    except TranscriptError as e:
        LOG.warning("analysis %s refused: %s", folder.name, e)
        job.update(state="error", error=str(e))
    except TranscriptMismatch as e:
        LOG.warning("analysis %s refused: %s", folder.name, e)
        job.update(state="error", error=mismatch_words(e, baseline, own_count) + bracket_hint(text, e))
    except Exception:  # report, never lose the worker thread silently
        traceback.print_exc()
        job.update(state="error", error=ANALYSIS_FAILED)
    finally:
        for raw in folder.glob("*recording*"):
            raw.unlink(missing_ok=True)


# ============================================================================================ fix your speech
class FixRequest(BaseModel):
    """finding: index in the result's `flaws` list (the stored order); all: fix every finding."""
    finding: int | None = None
    all: bool = False
    pitch_method: Literal["own", "contour"] = "own"


def fix_target(request: FixRequest, result: dict) -> int | None:
    """The finding index to fix, or None for all; 422 in plain words for anything else."""
    if request.all == (request.finding is not None):
        raise HTTPException(422, 'Send either {"finding": <number>} or {"all": true}.')
    if request.all:
        if not result.get("flaws"):
            raise HTTPException(422, "This analysis has no findings to fix.")
        return None
    if not 0 <= request.finding < len(result.get("flaws", [])):
        raise HTTPException(422, f"This analysis has no finding number {request.finding}.")
    return request.finding


def gallery_source(gallery: Path, item: dict) -> FixSource | None:
    """The fix inputs of a bundled example: its audio, stored result and the bundled baseline it was analysed against
    (a bank example names one of the bank's readings). An item with its own `text` (an example whose baseline is not
    offered for uploads, or a SELF example) uses that text and the baseline audio of its result. None when the gallery
    bundles no text for the example."""
    result_path = gallery / item["result"]
    result = json.loads(result_path.read_text())
    regime = result["regime"]
    if item.get("text"):
        if regime == SELF_REGIME:
            return FixSource(gallery / item["audio"], result_path, item["text"], regime)
        return FixSource(gallery / item["audio"], result_path, item["text"], regime, gallery / result["baseline"]["audio"])
    for baseline in bundled_baselines(gallery).values():
        references = baseline.get("references") or []
        if item.get("baseline") == baseline["id"]:
            refs = tuple(gallery / r["audio"] for r in references) or None
            return FixSource(gallery / item["audio"], result_path, baseline["text"], regime, gallery / baseline["audio"], refs)
        if any(r["id"] == item.get("baseline") for r in references):
            refs = tuple(gallery / r["audio"] for r in references)
            return FixSource(gallery / item["audio"], result_path, baseline["text"], regime, refs[0], refs)
    return None


def fixable_examples(gallery: Path) -> list[str]:
    items = json.loads((gallery / "index.json").read_text()).get("items", [])
    return [it["id"] for it in items if it.get("result") and (gallery / it["result"]).exists() and gallery_source(gallery, it) is not None]


def analyze_kwargs(source: FixSource, detector: Path, cache_dir: Path | None) -> dict:
    """The pipeline.analyze arguments of the source's own analysis, other than the participant (repair.verify)."""
    kwargs = {"transcript": source.transcript, "cache_dir": cache_dir}
    if source.regime == SELF_REGIME:
        return kwargs
    references = None if source.references is None else [audio.read_wav(p) for p in source.references]
    return {**kwargs, "baseline": references[0] if references else audio.read_wav(source.baseline), "references": references,
            "detector": load_detector(detector)}


def unsigned_zero(value: float) -> float:
    """-0.0 + 0.0 is 0.0 in IEEE 754, so the page never shows "-0"."""
    return value + 0.0


def plain_outcome(fix: repair.Fix, removed: set[str], owner: repair.Fix | None = None) -> tuple[str, str]:
    """(no_longer_flagged | still_flagged | unfixable | skipped, the reason in plain words or ""), from the fix, the
    re-analysis and, for a covered finding, the fix of the finding whose edit covers it. A still-flagged spot whose edit
    applied less than MIN_HEARD_SHARE of its change counts as skipped: the change is too small to hear."""
    if fix.status == repair.UNFIXABLE:
        return "unfixable", fix.reason[:1].upper() + fix.reason[1:]
    if fix.status == repair.SKIPPED:
        return "skipped", CAUSE_WORDS.get(fix.cause, CAUSE_WORDS[repair.INAUDIBLE])
    outcome = "no_longer_flagged" if fix.finding in removed else "still_flagged"
    share = owner.share if owner is not None else fix.share
    if outcome == "still_flagged" and share is not None and share < MIN_HEARD_SHARE:
        return "skipped", CAUSE_WORDS[repair.INAUDIBLE]
    if owner is not None:
        whose = f"The edit of {owner.finding} also changes this spot"
        partial = owner.share is not None and owner.share < 1
        return outcome, (f"{whose}; it applied {owner.share:.0%} of its change." if partial else f"{whose}.")
    if fix.share is not None and fix.share < 1:
        return outcome, f"{fix.share:.0%} of the change toward the target was applied. {CAUSE_WORDS.get(fix.cause, '')}".strip()
    return outcome, ("" if outcome == "no_longer_flagged" else STILL_FLAGGED_WORDS)


def covering_finding(fix: repair.Fix, result: dict) -> str | None:
    """The id of the finding whose edit also fixes a covered finding (repair names it in the reason)."""
    if fix.status != repair.COVERED:
        return None
    return next((f["id"] for f in result["flaws"] if f["id"] != fix.finding and f["id"] in fix.reason), None)


def fix_checks(report: dict) -> list[dict]:
    """The checks of the re-analysis, each {name, passed, label}. "reproduced" holds the unedited recording and the null
    chain (repair.verify); "pitch_trackers" is present only when an edit changed the pitch."""
    null_chain, alignment = report.get("null_chain") or {}, report.get("alignment") or {}
    passed = {"reproduced": bool(report.get("reproduced")) and bool(null_chain.get("within_tolerance", True)),
              "alignment": not alignment.get("words_off")}
    if report.get("pitch_check"):
        passed["pitch_trackers"] = all(row.get("agree", True) for row in report["pitch_check"])
    return [{"name": name, "passed": ok, "label": CHECK_LABELS[name]} for name, ok in passed.items()]


def fix_entry(fx: repair.Fix, finding: dict, owner: repair.Fix | None, removed: set[str], after: dict | None,
              context: dict) -> dict:
    """One fix in the shape of the page contract. owner: the fix whose edit covers this finding; after: the re-analysis
    (None when the report has none); context: mode, pitch_method and regime of the fix job."""
    outcome, words = plain_outcome(fx, removed, owner)
    left = None if after is None else repair.residual(finding, after)
    floor_removed = fx.operation == "pause_shorten" and outcome == "no_longer_flagged" and after is not None and left is None
    if floor_removed:
        words = FLOOR_WORDS
    share = owner.share if owner is not None else fx.share
    limit = LIMIT_WORDS.get(fx.operation) if outcome in ("no_longer_flagged", "still_flagged") else None
    if fx.operation == "emphasis" and context["regime"] == "R1":
        limit = None
    alt = (context["mode"] == "reference" and context["pitch_method"] == "own" and fx.dimension == "D3"
           and outcome in ("skipped", "still_flagged"))
    return {"finding": fx.finding, "status": fx.status, "outcome": outcome, "reason": words, "detail": fx.reason, "share": share,
            "covered_by": None if owner is None else owner.finding, "flagged_after": fx.finding not in removed,
            "residual": None if left is None else unsigned_zero(round(left, 3)),
            "residual_share": None if left is None or not finding.get("delta") else unsigned_zero(round(left / finding["delta"], 3)),
            "unit": finding.get("unit"), "floor_removed": floor_removed, "alt_pitch_available": alt, "limit": limit, "round": fx.round}


def score_change_note(reproduced: bool, mode: str) -> str | None:
    """Why the fix job gives no score change, or None."""
    if not reproduced:
        return NOT_REPRODUCED_WORDS
    if mode == "self":
        return SELF_SCORE_WORDS
    return None


def fix_summary(outcome: repair.FixOutcome, report: dict, finding: int | None, result: dict, mode: str = "reference",
                pitch_method: str = "own") -> dict:
    """What the page shows: the score change when the re-analysis reproduces the original (reference mode only), the
    flagged spots before and after, which findings went, stayed or are new, the checks of the re-analysis, each fix in
    plain words with its remaining departure, and the region of each edit in the original and the fixed audio. mode:
    "reference" or "self"."""
    removed = set(report["removed"])
    after = report.get("result")
    flaws = {f["id"]: f for f in result["flaws"]}
    by_id = {fx.finding: fx for fx in outcome.fixes}
    context = {"mode": mode, "pitch_method": pitch_method, "regime": result.get("regime")}
    fixes = [fix_entry(fx, flaws[fx.finding], by_id.get(covering_finding(fx, result)), removed, after, context) for fx in outcome.fixes]
    checks = fix_checks(report)
    reproduced = next(c["passed"] for c in checks if c["name"] == "reproduced")
    before, score = report.get("score_before"), report.get("score")
    comparable = reproduced and mode == "reference" and before is not None and score is not None
    note = score_change_note(reproduced, mode)
    counts = {name: sum(f["outcome"] == name for f in fixes) for name in ("no_longer_flagged", "still_flagged", "unfixable", "skipped")}
    counts["partial"] = sum(f["outcome"] == "no_longer_flagged" and f["share"] is not None and f["share"] < 1 for f in fixes)
    counts["floor_removed"] = sum(f["floor_removed"] for f in fixes)
    return {"target": "all" if finding is None else result["flaws"][finding]["id"], "mode": mode, "pitch_method": pitch_method,
            "caution": SELF_CAUTION if mode == "self" else None,
            "score_before": before, "score_after": score, "score_change": round(score - before, 2) if comparable else None,
            "score_change_note": note, "flags_before": len(result["flaws"]), "flags_after": None if after is None else len(after["flaws"]),
            "removed": report["removed"], "remaining": [r["id"] for r in report.get("remaining", [])],
            "new_findings": len(report.get("new_findings") or []), "checks": checks, "checks_passed": all(c["passed"] for c in checks),
            "counts": counts, "fixes": fixes, "listen": repair.listen_pairs(outcome, LISTEN_CONTEXT_S),
            "duration": round(len(outcome.audio) / C.SR, 3)}


def run_fix(job: dict, folder: Path, source: FixSource, finding: int | None, pitch_method: str, detector: Path,
            cache_dir: Path | None) -> None:
    """Worker: fix one finding (an index of result.flaws) or all of them, write fixed.wav, re-analyse it with the source's
    own settings (repair.verify) and keep the summary on the job."""
    try:
        job.update(state="running", stage="edit")
        result = json.loads(source.result.read_text())
        wav = audio.read_wav(source.participant)
        if finding is None:
            outcome = repair.fix_all(result, wav, pitch_method=pitch_method, transcript=source.transcript)
        else:
            outcome = repair.fix_finding(result, wav, finding, pitch_method=pitch_method, transcript=source.transcript)
        audio.write_wav(folder / "fixed.wav", outcome.audio)
        job.update(stage="check")
        report = repair.verify(outcome, result, analyze_kwargs(source, detector, cache_dir))
        mode = "self" if source.regime == SELF_REGIME else "reference"
        job.update(state="done", stage="done", fix=fix_summary(outcome, report, finding, result, mode, pitch_method))
    except Exception:  # report, never lose the worker thread silently
        traceback.print_exc()
        job.update(state="error", error=FIX_FAILED)


# ============================================================================================ app
def create_app(gallery: Path = GALLERY, detector: Path = DEFAULT_DETECTOR, work: Path | None = None) -> FastAPI:
    """The dashboard app. gallery: folder with index.json, results/ and audio/ (built by `python -m cvoice.gallery`)."""
    if not (gallery / "index.json").exists():
        raise FileNotFoundError(f"{gallery}/index.json not found: the gallery is built by the Kaggle run (python -m cvoice.gallery)")
    jobs = Jobs(work or Path(tempfile.mkdtemp(prefix="cvoice-jobs-")))
    fixable = set(fixable_examples(gallery))
    app = FastAPI(title="Contrastive Voice", version=__version__)
    app.add_middleware(BodySizeLimit, max_bytes=max_request_bytes())

    @app.get("/api/health")
    def health() -> dict:
        reason = None if detector.exists() else f"{detector.name} is missing: run `python -m cvoice.calibrate` first."
        return {"ok": True, "pipeline": __version__,
                "limits": {"max_bytes": C.MAX_UPLOAD_BYTES, "max_total_bytes": max_request_bytes(), "max_seconds": C.MAX_UPLOAD_S,
                           "max_references": MAX_REFERENCES, "consensus_k": C.CONSENSUS_K},
                "flag_limits": upload_limits(detector), "analysis": {"available": reason is None, "reason": reason},
                "self": {"available": SELF_DETECTOR.exists()},
                "fix": {"available": reason is None, "examples": sorted(fixable)}, "stages": STAGES, "fix_stages": FIX_STAGES,
                "stage_labels": STAGE_LABELS, "report_url": REPORT_URL if REPORT_PDF.is_file() else None}

    @app.get("/report")
    def report() -> FileResponse:
        if not REPORT_PDF.is_file():  # fixed path: no client string reaches the file system
            raise HTTPException(404, "The technical report is not included in this installation.")
        return FileResponse(REPORT_PDF, media_type="application/pdf", filename=REPORT_PDF.name, content_disposition_type="inline")

    @app.post("/api/analyze")
    def submit(audio_file: UploadFile = File(alias="audio"), transcript: str = Form(""), transcript_file: UploadFile | None = File(None),
               baseline_id: str = Form(""), baseline_audio: list[UploadFile] | None = File(None)) -> dict:
        own = reference_uploads(baseline_audio)
        if own and baseline_id:
            raise HTTPException(422, "Choose a bundled baseline or upload your own reference recordings, not both.")
        needed = detector if own or baseline_id else SELF_DETECTOR
        if not needed.exists():
            raise HTTPException(503, f"Analysis is not available: {needed.name} is missing.")
        check_sizes([(audio_file, "Your recording"), *zip(own, map(upload_label, reference_names(len(own)))),
                     (transcript_file, "The transcript file")])
        try:
            text = read_transcript(transcript, transcript_file)
            tr = parse_transcript(text)
        except TranscriptError as e:
            raise HTTPException(422, str(e)) from e
        baseline = bundled_choice(gallery, baseline_id, tr) if baseline_id else None
        made = jobs.new()
        if made is None:
            raise HTTPException(429, BUSY)
        jid, folder = made
        try:
            save_upload(audio_file, folder / "your recording")
            for file, name in zip(own, reference_names(len(own))):
                save_upload(file, folder / name)
        except HTTPException:
            shutil.rmtree(folder, ignore_errors=True)
            del jobs.table[jid]
            raise
        jobs.pool.submit(run_job, jobs.table[jid], folder, text, baseline, detector, len(own), jobs.cache)
        return {"job_id": jid}

    def job_or_404(job_id: str) -> dict:
        if job_id not in jobs.table:  # dict lookup: no client string ever reaches the file system
            raise HTTPException(404, "This analysis is no longer available. Upload again.")
        return jobs.table[job_id]

    def start_fix(source: FixSource, request: FixRequest) -> dict:
        finding = fix_target(request, json.loads(source.result.read_text()))
        if source.regime == SELF_REGIME and request.pitch_method == "contour":
            raise HTTPException(422, CONTOUR_SELF_WORDS)
        if source.regime != SELF_REGIME and not detector.exists():
            raise HTTPException(503, f"Fixing is not available: {detector.name} is missing.")
        made = jobs.new("fix")
        if made is None:
            raise HTTPException(429, BUSY)
        jid, folder = made
        jobs.pool.submit(run_fix, jobs.table[jid], folder, source, finding, request.pitch_method, detector, jobs.cache)
        return {"job_id": jid}

    @app.post("/api/jobs/{job_id}/fix")
    def fix_upload(job_id: str, request: FixRequest) -> dict:
        job = job_or_404(job_id)
        if job["kind"] != "analysis" or job["state"] != "done":
            raise HTTPException(409, "Only a finished analysis can be fixed.")
        return start_fix(job["source"], request)

    @app.post("/api/gallery/{item_id}/fix")
    def fix_example(item_id: str, request: FixRequest) -> dict:
        items = {it["id"]: it for it in json.loads((gallery / "index.json").read_text()).get("items", [])}
        if item_id not in items:  # dict lookup: no client string ever reaches the file system
            raise HTTPException(404, "Unknown example.")
        source = gallery_source(gallery, items[item_id]) if item_id in fixable else None
        if source is None:
            raise HTTPException(422, "This example cannot be fixed here: its text is not bundled.")
        return start_fix(source, request)

    @app.get("/api/jobs/{job_id}")
    def job_status(job_id: str) -> dict:
        job = job_or_404(job_id)
        fix = job["kind"] == "fix"
        stages = FIX_STAGES if fix else STAGES
        out = {"kind": job["kind"], "state": job["state"], "stage": job["stage"], "stages": stages,
               "stage_labels": {stage: STAGE_LABELS[stage] for stage in stages}}
        if job["state"] == "error":
            out["error"] = job["error"]
        if job["state"] == "done" and fix:
            out["audio"] = f"api/jobs/{job_id}/fixed.wav"
            out["fix"] = job["fix"]
        elif job["state"] == "done":
            out["result"] = f"api/jobs/{job_id}/result.json"
            out["reference"] = job["reference"]
        return out

    @app.get("/api/jobs/{job_id}/result.json")
    def job_result(job_id: str) -> FileResponse:
        job = job_or_404(job_id)
        if job["kind"] != "analysis" or job["state"] != "done":
            raise HTTPException(404, "The analysis has not finished.")
        return FileResponse(jobs.work / job_id / "result.json", media_type="application/json")

    @app.get("/api/jobs/{job_id}/{role}.wav")
    def job_audio(job_id: str, role: Literal["participant", "baseline", "fixed"]) -> FileResponse:
        job_or_404(job_id)
        path = jobs.work / job_id / f"{role}.wav"
        if not path.exists():
            raise HTTPException(404, f"No {role} audio for this job.")
        return FileResponse(path, media_type="audio/wav")

    app.mount("/gallery", StaticFiles(directory=gallery), name="gallery")
    app.mount("/", StaticFiles(directory=STATIC, html=True), name="static")  # last: it matches every path
    return app


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m cvoice.app", description=__doc__.splitlines()[0])
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "7860")))
    parser.add_argument("--gallery", type=Path, default=GALLERY)
    parser.add_argument("--detector", type=Path, default=DEFAULT_DETECTOR, help="detector.json used for uploads")
    args = parser.parse_args(argv)
    uvicorn.run(create_app(args.gallery, args.detector), host=args.host, port=args.port, workers=1)


if __name__ == "__main__":
    main()
