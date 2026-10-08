"""Synthetic speech-like signals with known word times (no model needed): buzzed 'words' separated by gaps and pauses."""
from __future__ import annotations

import numpy as np

from cvoice import audio, config as C
from cvoice.align import Alignment, parse_transcript
from cvoice.compare import Comparison, compare
from cvoice.detect import KEYS, Region, key
from cvoice.features import make_recording

WORDS = "we hold these truths to be self evident that all men are created equal and so on".split()


def synth(n_words: int = 16, word_s: float = 0.30, gap_s: float = 0.06, pauses: dict | None = None, f0: float = 120.0,
          lead: float = 0.6, seed: int = 0, glide_st: float = 4.0, level: float = 0.2):
    """(wav on the int16 grid, start[s], end[s]) with `pauses` = {boundary index: gap seconds}. Each word is a harmonic buzz
    with a pitch glide and an amplitude envelope; the floor is white noise at about -60 dBFS."""
    pauses = pauses or {}
    rng = np.random.default_rng(seed)
    starts, ends, t = [], [], lead
    for i in range(n_words):
        starts.append(t)
        ends.append(t + word_s)
        t += word_s + pauses.get(i, gap_s)
    total = t + lead
    x = rng.standard_normal(int(total * C.SR)) * 1e-3
    for s, e in zip(starts, ends):
        n = int((e - s) * C.SR)
        tt = np.arange(n) / C.SR
        f = f0 * 2 ** (glide_st * (tt / (e - s) - 0.5) / 12)
        ph = 2 * np.pi * np.cumsum(f) / C.SR
        w = sum(np.sin(k * ph) / k for k in range(1, 9))
        env = np.sin(np.pi * np.arange(n) / n) ** 0.5
        i0 = int(s * C.SR)
        x[i0:i0 + n] += level * env * w / 2.5
    return audio.quantize(x), np.array(starts) + 0.02, np.array(ends) - 0.02


def recording(n_words: int = 16, text: str | None = None, **kw):
    """A Recording of a synthetic clip whose alignment is the planted word times (compatibility 0.9)."""
    wav, st, en = synth(n_words, **kw)
    words = [WORDS[i % len(WORDS)] for i in range(n_words)]
    text = text or (" ".join(words[:8]) + ". " + " ".join(words[8:]).capitalize() + ".")
    tr = parse_transcript(text)
    assert len(tr) == n_words, (len(tr), n_words)
    compat = np.full(n_words, 0.9)
    return make_recording(wav, tr, Alignment(st, en, compat, 0.9))


def regime(name: str = "R1", h: float | dict = 2.0, scales: dict | None = None, clip: dict | None = None, enabled: list | None = None) -> dict:
    """An in-memory schema-4 regime: scales default to the design floors, `h` is one value for every flag key of an enabled
    dimension (or a {flag key: h or None} dict), `clip` defaults to the R1 design thresholds CLIP_LN."""
    enabled = list(C.REGIME_DIMS[name]) if enabled is None else enabled
    hs = {k: (h.get(k) if isinstance(h, dict) else h) if C.dim_of(k) in enabled else None for k in KEYS}
    return {"name": name, "enabled": enabled, "scales": dict(scales) if scales else {key(d, sign) if C.is_event(d) else d: C.FLOORS[d]
                                                               for d in C.DIMS for sign in C.FLAG_SIGNS[d]}, "h": hs, "clip": dict(C.CLIP_LN if clip is None else clip), "pattern_labels": {"uneven_tempo": True}}


def comparison(dims: dict, n: int = 24) -> Comparison:
    """A Comparison of n words around the given dimensions (identity time map, full coverage)."""
    return Comparison(dims, np.array([0.0, 1.0]), np.array([0.0, 1.0]), [], [], np.zeros(n), np.zeros(n), dict.fromkeys(C.DIMS, 1.0))


def local(dim: str, a: int, b: int, z: float = -3) -> Region:
    """A local region over words a..b of `dim` (sign of z) peaking at its first word."""
    return Region(dim, 1 if z > 0 else -1, a, b, a, z, tuple(range(a, b + 1)))


def label(B, typ: str = "FADE", words: tuple = (10, 15), secondary: tuple = ()) -> dict:
    """Labels of one injected flaw of type `typ` over words a..b of the recording B."""
    a, b = words
    return {"flaws": [{"type": typ, "dimension": C.FLAW_DIM[typ], "level": 2, "placebo": False,
                       "span": [round(B.al.start[a] * C.SR), round(B.al.end[b] * C.SR)], "words": [a, b],
                       "event": "span", "expected_secondary": list(secondary)}]}


def with_x(B, dim: str, values: list) -> Comparison:
    """compare(B, B) with the deltas of `dim` set to x over the given (first word, last word, x) triples."""
    comp = compare(B, B)
    for a, b, x in values:
        comp.dims[dim].x[a:b + 1] = x
    return comp
