"""Dashboard server: the static page, the gallery files, and upload analysis jobs.

    python -m cvoice.app [--host 127.0.0.1] [--port 7860] [--gallery DIR]

The port defaults to the PORT environment variable when it is set (hosting platforms set it), else 7860.

    GET  /api/health                       uploads possible? limits
    POST /api/analyze                      multipart: audio, transcript (text) or transcript_file, baseline_id or baseline_audio
                                           (one to MAX_REFERENCES files: the user's own reference bank, the first one shown)
    GET  /api/jobs/{id}                    {state, stage, stages, error?, result?, reference?}
    GET  /api/jobs/{id}/result.json        the analysis result JSON
    GET  /api/jobs/{id}/{participant|baseline}.wav   the decoded audio the analysis used (Range-capable)
    /gallery/...  /                        static files (gallery data, then the page)

Regime rule: a bundled dataset clip against its own baseline is R1; anything else is R2. An upload is never a
bundled clip, so every upload is analysed as R2. A bundled baseline with `references` (a reference bank) is passed to the
pipeline as its bank, and so are two or more uploaded reference recordings; the pipeline selects the reference mode, and a
finished job states the mode it used (`reference`).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
import threading
import time
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Literal

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import __version__, audio
from . import config as C
from .align import Transcript, TranscriptError, TranscriptMismatch, parse_transcript
from .detect import load_detector, scale, threshold
from .pipeline import DEFAULT_DETECTOR, ROOT, analyze, dumps

GALLERY = ROOT / "gallery"
STATIC = Path(__file__).parent / "static"
STAGES = ("decode", "align", "features", "compare", "detect")
UPLOAD_REGIME = "R2"
TRANSCRIPT_MAX_CHARS = 20_000  # characters; Starlette would accept 1 MB per text field
JOB_TTL_S = 3600  # s, finished jobs and their files are swept after this
TRANSCRIPT_HINT = "The transcript must be the exact words both recordings read."
REFERENCE_FIELDS = ("reference_mode", "reference_count", "references_available")  # result.detection fields of the job status
MAX_REFERENCES = C.CONSENSUS_K  # the pipeline uses at most CONSENSUS_K readings, so more uploads would only cost time
# Rows whose flag threshold is a plain physical change (speed factor, seconds, dB); pitch range has a regularising offset.
LIMIT_ROWS = {"D1": "pace", "D2": "pauses", "D5": "volume"}
MODE_REGIMES = {"single": "R2", "consensus5": "R2_consensus"}  # detector.json regime entry of each upload reference mode


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


def bundled_choice(gallery: Path, baseline_id: str, tr: Transcript) -> dict:
    """The bundled baseline with its audio paths; 422 for an unknown id, or for a bank whose text differs from the transcript
    (the bank readings are aligned to the transcript without the mismatch check that the uploads get)."""
    baseline = bundled_baselines(gallery).get(baseline_id)
    if baseline is None:
        raise HTTPException(422, f"Unknown baseline '{baseline_id}'.")
    baseline = {**baseline, "wav": gallery / baseline["audio"]}
    if baseline.get("references"):
        if parse_transcript(baseline["text"]).norm != tr.norm:
            raise HTTPException(422, f"The {baseline['title']} readings read a fixed text. {TRANSCRIPT_HINT}")
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


def check_sizes(files: list[UploadFile]) -> None:
    """413 when one file is above the per-file limit (the body cap allows several files)."""
    if any(f.size is not None and f.size > C.MAX_UPLOAD_BYTES for f in files):
        raise HTTPException(413, f"Each recording must be {C.MAX_UPLOAD_BYTES // 2**20} MB or smaller.")


def reference_names(count: int) -> list[str]:
    """Server-chosen file names of the uploaded references; the name starts each decode error message."""
    return ["reference recording"] if count == 1 else [f"reference recording {k + 1}" for k in range(count)]


def save_upload(file: UploadFile, dest: Path) -> None:
    """Write an upload under a server-chosen name and sniff its magic bytes; 415 when it is not audio."""
    with dest.open("wb") as fh:
        shutil.copyfileobj(file.file, fh)
    try:
        audio.sniff(dest)
    except audio.AudioError as e:
        raise HTTPException(415, "Unsupported audio. Use wav, mp3, m4a, ogg, flac or webm.") from e


# ============================================================================================ jobs
class Jobs:
    """In-memory job table with one worker thread. Known limit: jobs are lost on restart and the table is wrong with more
    than one uvicorn worker, so main() starts one worker."""

    def __init__(self, work: Path):
        self.work, self.table = work, {}
        work.mkdir(parents=True, exist_ok=True)
        self.pool = ThreadPoolExecutor(max_workers=1)
        self.lock = threading.Lock()

    def sweep(self) -> None:
        for jid in [k for k, j in self.table.items() if j["state"] in ("done", "error") and time.monotonic() - j["born"] > JOB_TTL_S]:
            shutil.rmtree(self.work / jid, ignore_errors=True)
            del self.table[jid]

    def new(self) -> tuple[str, Path] | None:
        """A fresh job id and folder, or None while another analysis is queued or running."""
        with self.lock:
            if any(j["state"] in ("queued", "running") for j in self.table.values()):
                return None
            self.sweep()
            jid = uuid.uuid4().hex  # server-generated: no client file name is ever used
            (self.work / jid).mkdir()
            self.table[jid] = {"state": "queued", "stage": "decode", "born": time.monotonic()}
            return jid, self.work / jid


def run_job(job: dict, folder: Path, tr, baseline: dict | None, detector: Path, own_count: int = 0) -> None:
    """Worker: decode, analyse as R2 (against the bank when the baseline has one or the user uploaded two or more references),
    write result.json. own_count: number of uploaded references (baseline is None then). Every failure becomes a plain message on the job."""
    try:
        job.update(state="running", stage="decode")
        participant_wav = audio.load_audio(folder / "your recording", C.MAX_UPLOAD_BYTES, C.MAX_UPLOAD_S)[0]
        audio.write_wav(folder / "participant.wav", participant_wav)
        references = None
        if baseline is None:
            own = [audio.load_audio(folder / name, C.MAX_UPLOAD_BYTES, C.MAX_UPLOAD_S)[0] for name in reference_names(own_count)]
            references = own if len(own) > 1 else None
            reference_wav = own[0]
            audio.write_wav(folder / "baseline.wav", reference_wav)
            baseline_meta = {"id": "uploaded_baseline", "title": "Your baseline recording", "audio": f"api/jobs/{folder.name}/baseline.wav"}
        else:
            if baseline.get("reference_wavs"):
                references = [audio.read_wav(p) for p in baseline["reference_wavs"]]
            reference_wav = references[0] if references else audio.read_wav(baseline["wav"])
            baseline_meta = {"id": baseline["id"], "title": baseline["title"], "audio": f"gallery/{baseline['audio']}"}
        res = analyze(participant_wav, tr, reference_wav, regime=UPLOAD_REGIME, detector=load_detector(detector), baseline_meta=baseline_meta, refuse_mismatch=True,
                      participant_meta={"id": folder.name, "title": "Your recording", "audio": f"api/jobs/{folder.name}/participant.wav"},
                      progress=lambda stage: job.update(stage=stage), references=references)
        (folder / "result.json").write_text(dumps(res) + "\n")
        detection = res.get("detection", {})
        job.update(state="done", stage="done", reference={k: detection.get(k) for k in REFERENCE_FIELDS})
    except (audio.AudioError, TranscriptError) as e:
        job.update(state="error", error=str(e))
    except TranscriptMismatch as e:
        job.update(state="error", error=f"{e}. {TRANSCRIPT_HINT}")
    except Exception as e:  # report, never lose the worker thread silently
        traceback.print_exc()
        job.update(state="error", error=f"Analysis failed ({type(e).__name__}: {e}).")
    finally:
        for raw in folder.glob("*recording*"):
            raw.unlink(missing_ok=True)


# ============================================================================================ app
def create_app(gallery: Path = GALLERY, detector: Path = DEFAULT_DETECTOR, work: Path | None = None) -> FastAPI:
    """The dashboard app. gallery: folder with index.json, results/ and audio/ (built by `python -m cvoice.gallery`)."""
    if not (gallery / "index.json").exists():
        raise FileNotFoundError(f"{gallery}/index.json not found: the gallery is built by the Kaggle run (python -m cvoice.gallery)")
    jobs = Jobs(work or Path(tempfile.mkdtemp(prefix="cvoice-jobs-")))
    app = FastAPI(title="Contrastive Voice", version=__version__)
    app.add_middleware(BodySizeLimit, max_bytes=max_request_bytes())

    @app.get("/api/health")
    def health() -> dict:
        reason = None if detector.exists() else f"{detector.name} is missing: run `python -m cvoice.calibrate` first."
        return {"ok": True, "pipeline": __version__,
                "limits": {"max_bytes": C.MAX_UPLOAD_BYTES, "max_total_bytes": max_request_bytes(), "max_seconds": C.MAX_UPLOAD_S,
                           "max_references": MAX_REFERENCES, "consensus_k": C.CONSENSUS_K},
                "flag_limits": upload_limits(detector), "analysis": {"available": reason is None, "reason": reason}, "stages": STAGES}

    @app.post("/api/analyze")
    def submit(audio_file: UploadFile = File(alias="audio"), transcript: str = Form(""), transcript_file: UploadFile | None = File(None),
               baseline_id: str = Form(""), baseline_audio: list[UploadFile] | None = File(None)) -> dict:
        if not detector.exists():
            raise HTTPException(503, f"Analysis is not available: {detector.name} is missing (run `python -m cvoice.calibrate`).")
        own = reference_uploads(baseline_audio)
        if bool(own) == bool(baseline_id):
            raise HTTPException(422, "Choose a bundled baseline or upload your own reference recordings (one of the two).")
        check_sizes([audio_file, *own])
        try:
            tr = parse_transcript(read_transcript(transcript, transcript_file))
        except TranscriptError as e:
            raise HTTPException(422, str(e)) from e
        baseline = bundled_choice(gallery, baseline_id, tr) if baseline_id else None
        made = jobs.new()
        if made is None:
            raise HTTPException(429, "Another analysis is running. Try again when it has finished.")
        jid, folder = made
        try:
            save_upload(audio_file, folder / "your recording")
            for file, name in zip(own, reference_names(len(own))):
                save_upload(file, folder / name)
        except HTTPException:
            shutil.rmtree(folder, ignore_errors=True)
            del jobs.table[jid]
            raise
        jobs.pool.submit(run_job, jobs.table[jid], folder, tr, baseline, detector, len(own))
        return {"job_id": jid}

    def job_or_404(job_id: str) -> dict:
        if job_id not in jobs.table:  # dict lookup: no client string ever reaches the file system
            raise HTTPException(404, "This analysis is no longer available. Upload again.")
        return jobs.table[job_id]

    @app.get("/api/jobs/{job_id}")
    def job_status(job_id: str) -> dict:
        job = job_or_404(job_id)
        out = {"state": job["state"], "stage": job["stage"], "stages": STAGES}
        if job["state"] == "error":
            out["error"] = job["error"]
        if job["state"] == "done":
            out["result"] = f"api/jobs/{job_id}/result.json"
            out["reference"] = job["reference"]
        return out

    @app.get("/api/jobs/{job_id}/result.json")
    def job_result(job_id: str) -> FileResponse:
        if job_or_404(job_id)["state"] != "done":
            raise HTTPException(404, "The analysis has not finished.")
        return FileResponse(jobs.work / job_id / "result.json", media_type="application/json")

    @app.get("/api/jobs/{job_id}/{role}.wav")
    def job_audio(job_id: str, role: Literal["participant", "baseline"]) -> FileResponse:
        job_or_404(job_id)
        path = jobs.work / job_id / f"{role}.wav"
        if not path.exists():
            raise HTTPException(404, f"No {role} audio for this analysis.")
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
