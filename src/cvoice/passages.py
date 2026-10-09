"""Automatic passage selection: chunked wav2vec2 emissions -> greedy CTC words with frame times ->
difflib anchors against the official transcript text -> sentence anchors -> windows of consecutive sentences of
20-40 s (each sentence >= 80 % anchored) -> forced alignment of the window with 0.5 s context -> clip.
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

import numpy as np

from . import config as C
from .align import Alignment, Transcript, TranscriptMismatch, greedy_words, require_match
from .features import frame_level_db
from .pipeline import make_job, run_jobs


# ============================================================================================ official text
class _Page(HTMLParser):
    """Block-level text lines of an HTML page, skipping scripts, styles and navigation."""
    _SKIP = {"script", "style", "noscript", "svg", "head", "nav", "header", "footer", "form", "button", "select"}
    _BLOCK = {"p", "div", "li", "br", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "blockquote", "section", "article"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[str] = []
        self._cur: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip += 1
        if tag in self._BLOCK:
            self._flush()

    def handle_endtag(self, tag):
        if tag in self._SKIP and self._skip:
            self._skip -= 1
        if tag in self._BLOCK:
            self._flush()

    def handle_data(self, data):
        if not self._skip:
            self._cur.append(data)

    def _flush(self):
        line = " ".join("".join(self._cur).split())
        if line:
            self.lines.append(line)
        self._cur = []


def page_text(path: Path) -> str:
    """Official transcript text from an HTML page or a plain-text file (Project Gutenberg boilerplate markers are cut).
    Everything on the page is kept: sentences that are not speech simply never anchor and stay ineligible."""
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in (".html", ".htm"):
        p = _Page()
        p.feed(raw)
        p._flush()
        # a line without closing punctuation (a heading, a nav item) must not run into the next sentence
        return "\n".join(l if re.search(r"[.!?][\"'\u201d\u2019)]*$", l) else l + "." for l in p.lines)
    m = re.search(r"\*\*\* START OF[^\n]*\n", raw)
    if m:
        raw = raw[m.end():]
    m = re.search(r"\*\*\* END OF", raw)
    return raw[:m.start()] if m else raw


# ============================================================================================ anchors
@dataclass
class Anchor:
    """A sentence of the official text located in a recording by greedy-decode anchoring."""
    k: int
    w0: int
    w1: int
    coverage: float
    eligible: bool
    start: float | None
    end: float | None


def sentence_anchors(official: Transcript, decoded: list[dict]) -> list[Anchor]:
    """difflib (autojunk off) between the official words and the greedy decode; per sentence the fraction of anchored
    words, and whether its first and last words are anchored. Eligible = both endpoints and coverage >= 80 %."""
    matcher = difflib.SequenceMatcher(None, list(official.norm), [d["norm"] for d in decoded], autojunk=False)
    matched: dict[int, dict] = {}
    for blk in matcher.get_matching_blocks():
        for j in range(blk.size):
            matched[blk.a + j] = decoded[blk.b + j]
    out = []
    for k in range(official.n_sentences):
        w0, w1 = official.sentence_words(k)
        cov = sum(i in matched for i in range(w0, w1 + 1)) / (w1 - w0 + 1)
        ends = w0 in matched and w1 in matched
        out.append(Anchor(k, w0, w1, cov, ends and cov >= C.SENTENCE_COVERAGE_MIN, matched[w0]["start"] if w0 in matched else None,
                          matched[w1]["end"] if w1 in matched else None))
    return out


def text_anchors(official: Transcript, decoded: list[dict]) -> list[Anchor]:
    matcher = difflib.SequenceMatcher(None, list(official.norm), [d['norm'] for d in decoded], autojunk=False)
    matched = {blk.a + j: decoded[blk.b + j] for blk in matcher.get_matching_blocks() for j in range(blk.size)}
    coverage = len(matched) / len(official)
    left = min(matched, default=len(official))
    right = max(matched, default=-1)
    eligible = coverage >= C.SENTENCE_COVERAGE_MIN and left < 5 and right >= len(official) - 5
    return [Anchor(0, 0, len(official) - 1, coverage, eligible,
                   max(0., matched[left]['start'] - left * C.PASSAGE_CONTEXT_S) if matched else None,
                   matched[right]['end'] + (len(official) - 1 - right) * C.PASSAGE_CONTEXT_S if matched else None)]


def locate_many(wavs: list[np.ndarray], officials: list[Transcript], pool=None, aligner=None, whole_text=False) -> list[list[Anchor]]:
    """Chunked emissions of whole recordings (one pool batch), greedy decode, sentence anchors. float32 samples are what the
    aligner reads anyway, and half the size across the pipe."""
    logps = run_jobs([make_job(w.astype(np.float32), kind="emit") for w in wavs], pool, aligner)
    anchors = text_anchors if whole_text else sentence_anchors
    return [anchors(o, greedy_words(lp)) for o, lp in zip(officials, logps)]


def candidate_windows(anchor_lists: list[list[Anchor]], allowed: set[int] | None = None) -> list[dict]:
    """Windows of consecutive sentences eligible in every recording, each lasting PASSAGE_S in every recording, ranked by
    minimum sentence coverage (descending), closeness of the mean duration to 30 s, earliest start (in the first recording)."""
    n = len(anchor_lists[0])
    ok = [all(al[k].eligible for al in anchor_lists) and (allowed is None or k in allowed) for k in range(n)]
    out = []
    for i in range(n):
        if not ok[i]:
            continue
        for j in range(i, n):
            if not ok[j]:
                break
            durs = [al[j].end - al[i].start for al in anchor_lists]
            if max(durs) > C.PASSAGE_S[1]:
                break
            if min(durs) >= C.PASSAGE_S[0]:
                cov = min(a.coverage for al in anchor_lists for a in al[i:j + 1])
                out.append({"first": i, "last": j, "durations": durs, "min_coverage": cov, "start": anchor_lists[0][i].start})
    out.sort(key=lambda c: (-c["min_coverage"], abs(float(np.mean(c["durations"])) - C.PASSAGE_TARGET_S), c["start"]))
    return out


# ============================================================================================ clip
def window_of(wav: np.ndarray, official: Transcript, anchors: list[Anchor], first: int, last: int) -> tuple[Transcript, np.ndarray, float]:
    """(window transcript, crop, crop start in source seconds): sentences first..last of the official text, cropped to
    PASSAGE_CONTEXT_S around the greedy hint."""
    tr = official.slice(anchors[first].w0, anchors[last].w1)
    a = max(int((anchors[first].start - C.PASSAGE_CONTEXT_S) * C.SR) // C.CTC_STRIDE * C.CTC_STRIDE, 0)
    b = min(int((anchors[last].end + C.PASSAGE_CONTEXT_S) * C.SR), len(wav))
    return tr, wav[a:b], a / C.SR


def cut_clip(wav: np.ndarray, al: Alignment) -> tuple[np.ndarray, int]:
    """Clip [first word - CLIP_PAD_S, last word + CLIP_PAD_S] clamped to the recording; returns (clip, start sample)."""
    a = max(int(round((al.start[0] - C.CLIP_PAD_S) * C.SR)), 0)
    b = min(int(round((al.end[-1] + C.CLIP_PAD_S) * C.SR)), len(wav))
    return wav[a:b].copy(), a


@dataclass
class Passage:
    """A selected passage cut from a recording: clip audio (16 kHz mono), its transcript, and the manifest record."""
    wav: np.ndarray
    tr: Transcript
    meta: dict


def passage_from(wav: np.ndarray, tr: Transcript, anchors: list[Anchor], first: int, last: int, al: Alignment) -> Passage:
    """Cut the clip for the force-aligned window `al` (source seconds). Passage selection is a trust boundary: raises
    TranscriptMismatch when the window does not match the audio or falls outside PASSAGE_S."""
    require_match(al)
    dur = float(al.end[-1] - al.start[0])
    if not C.PASSAGE_S[0] <= dur <= C.PASSAGE_S[1]:
        raise TranscriptMismatch(f"aligned window lasts {dur:.1f} s, outside {C.PASSAGE_S}")
    clip, a = cut_clip(wav, al)
    L = frame_level_db(clip)
    meta = {"sentences": [first, last], "words": [anchors[first].w0, anchors[last].w1], "text": tr.text(), "n_words": len(tr),
            "source_start_s": round(float(al.start[0]), 3), "source_end_s": round(float(al.end[-1]), 3),
            "clip_offset_s": round(a / C.SR, 3), "clip_duration_s": round(len(clip) / C.SR, 3),
            "qa": {"mean_compat": round(al.mean_compat, 4),
                   "rms_dbfs": round(float(10 * np.log10(np.mean(clip ** 2) + 1e-20)), 2),
                   "level_range_p95_p5_db": round(float(np.percentile(L, 95) - np.percentile(L, 5)), 2),
                   "anchor_min_coverage": round(min(a.coverage for a in anchors[first:last + 1]), 3)}}
    return Passage(clip, tr, meta)  # tr is the slice itself: re-parsing its display text would lose sentence boundaries


@dataclass
class Group:
    """Recordings that must share one window (the first is the baseline the ranking looks at)."""
    name: str
    wavs: list[np.ndarray]
    official: Transcript
    anchors: list[list[Anchor]]
    allowed: set[int] | None = None


def select_passages(groups: list[Group], pool=None, aligner=None, max_tries: int = 10) -> list[list[Passage]]:
    """Best window of every group, one pool batch per round: round r force-aligns the r-th ranked candidate of every group
    still unresolved (a window that fails the final alignment moves its group to the next candidate). Raises when a group
    runs out of candidates."""
    ranked = [candidate_windows(g.anchors, g.allowed)[:max_tries] for g in groups]
    out: list[list[Passage] | None] = [None] * len(groups)
    errors: list[list[str]] = [[] for _ in groups]
    for r in range(max_tries):
        todo = [gi for gi in range(len(groups)) if out[gi] is None and r < len(ranked[gi])]
        if not todo:
            break
        jobs, where = [], []
        for gi in todo:
            c, g = ranked[gi][r], groups[gi]
            for wi, (w, al) in enumerate(zip(g.wavs, g.anchors)):
                tr, crop, off = window_of(w, g.official, al, c["first"], c["last"])
                jobs.append(make_job(crop, tr, "align"))
                where.append((gi, wi, tr, off))
        found: dict[int, list] = {gi: [] for gi in todo}
        for (gi, wi, tr, off), a in zip(where, run_jobs(jobs, pool, aligner)):
            found[gi].append((tr, Alignment(a.start + off, a.end + off, a.compat, a.mean_compat)))
        for gi in todo:
            c, g = ranked[gi][r], groups[gi]
            try:
                out[gi] = [passage_from(w, tr, al, c["first"], c["last"], a) for w, al, (tr, a) in zip(g.wavs, g.anchors, found[gi])]
            except TranscriptMismatch as e:
                errors[gi].append(f"sentences {c['first']}-{c['last']}: {e}")
    for gi, g in enumerate(groups):
        if out[gi] is None:
            raise RuntimeError((f"{g.name}: " if g.name else "") + ("no passage window survived forced alignment: " + "; ".join(errors[gi]) if errors[gi]
                                                  else "no eligible 20-40 s sentence window"))
    return out  # type: ignore[return-value]
