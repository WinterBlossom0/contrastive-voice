"""The whole detector: tolerance scales, thresholds per dimension and direction (one common value in R1), offline hysteresis
regions, whole-clip flags, detector.json I/O.

z = x / s_k with s_k = max(floor_k, 1.4826 wMAD, wQ68(|x|)) over the null pairs of the regime. A region opens where
sign * z >= h and extends over the contiguous signed run with sign * z >= max(h / 2, 0.5 * peak), peak being the largest
sign * z in that run (half-maximum rule: five-word windows smear an edit by two words each side, the half-maximum cut
removes most of that; the pitch range is the exception, see REGION_PEAK_FRACTION). No gap bridging; sentence boundaries and units without a value break runs. D2 and D4 are single events.
h is stored per flag key (dimension and direction, e.g. "D2+"): a lengthened and a shortened pause are different populations.
Whole-clip flags (overall tempo, overall pitch range) compare the clip median g with the regime's whole-clip threshold.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import __version__
from . import config as C
from .compare import Comparison, Dim

SCHEMA = 4


def key(dim: str, sign: int) -> str:
    """Flag key of a dimension and direction, e.g. "D1-" (faster), "D2+" (longer pause)."""
    return f"{dim}{'+' if sign > 0 else '-'}"


def parse_key(flag_key: str) -> tuple[str, int]:
    """Dimension and direction of a flag key: the inverse of key."""
    return C.dim_of(flag_key), (1 if flag_key.endswith('+') else -1)


def whole_clip_key(dim: str, sign: int) -> str:
    """Flag key of a whole-clip flag, e.g. "D1- whole clip"."""
    return key(dim, sign) + " whole clip"


KEYS = tuple(key(k, s) for k in C.DIMS for s in C.FLAG_SIGNS[k])


# ============================================================================================ scales
def wquantile(v: np.ndarray, w: np.ndarray, q: float) -> float:
    """Lower weighted quantile: the smallest value whose cumulative weight share reaches q."""
    o = np.argsort(v, kind="stable")
    cw = np.cumsum(w[o])
    return float(v[o][min(int(np.searchsorted(cw, q * cw[-1] - 1e-12)), len(v) - 1)])


def pooled(dim: str, comps: list[Comparison], sign: int | None = None, pair_weights=None) -> tuple[np.ndarray, np.ndarray]:
    """Valid x of one dimension over null pairs, each pair carrying total weight 1 (unit weights normalised)."""
    xs, ws = [], []
    for j, c in enumerate(comps):
        d = c.dims[dim]
        ok = np.isfinite(d.x)
        if sign is not None:
            ok &= d.countable & (sign * d.x > 0)
        if ok.any() and d.w[ok].sum() > 0:
            xs.append(d.x[ok])
            ws.append(d.w[ok] / d.w[ok].sum() * (pair_weights[j] if pair_weights is not None else 1.0))
    if not xs:
        return np.array([]), np.array([])
    return np.concatenate(xs), np.concatenate(ws)


def fit_scales(comps: list[Comparison], pair_weights=None) -> tuple[dict[str, float], dict[str, float | None], dict[str, int]]:
    """(scales, null medians, valid unit counts) per window dimension or countable signed event key. The null median is stored, never subtracted."""
    scales, medians, counts = {}, {}, {}
    units = [(dim, sign) for dim in C.DIMS for sign in (C.FLAG_SIGNS[dim] if C.is_event(dim) else (None,))]
    for dim, sign in units:
        k = key(dim, sign) if sign is not None else dim
        x, w = pooled(dim, comps, sign, pair_weights)
        counts[k] = int(len(x))
        if len(x) == 0:
            scales[k], medians[k] = C.FLOORS[dim], None
            continue
        m = wquantile(x, w, 0.5)
        mad = C.MAD_SCALE * wquantile(np.abs(x - m), w, 0.5)
        q68 = wquantile(np.abs(x), w, C.Q68)
        scales[k], medians[k] = max(C.FLOORS[dim], mad, q68), m
    return scales, medians, counts


def scale(regime: dict, dim: str, sign: int) -> float:
    scales = regime['scales']
    if C.is_event(dim) and key(dim, sign) in scales:
        return scales[key(dim, sign)]
    return scales[dim]


# ============================================================================================ regions
@dataclass
class Region:
    """A flagged region over units i0..i1 (inclusive word / boundary indices) of dimension dim; sign = sign of x;
    peak = unit with the largest |z|; z = signed z at the peak."""
    dim: str
    sign: int
    i0: int
    i1: int
    peak: int
    z: float
    units: tuple[int, ...]


def _peak_regions(sz: np.ndarray, a: int, b: int, h: float, min_words: int, peak_fraction: float) -> list[tuple[int, int, int]]:
    """(first, last, peak) regions inside the run a..b (all sz >= h / 2): the region around the run's peak is the contiguous
    part with sz >= max(h / 2, peak_fraction * peak); what is left on either side is treated the same way, except the WINDOW_WORDS // 2
    units next to the region: a five-word window centred there still overlaps the region, so they are its shoulder, not another
    flaw. A run whose peak stays below h opens nothing. Anchoring on the peak is the fixed point of 'recompute the peak after
    each trim'."""
    half = C.WINDOW_WORDS // 2
    out, todo = [], [(a, b, 0, 0)]  # (first, last, shoulder units at the left end, at the right end)
    while todo:
        a, b, sl, sr = todo.pop()
        if a > b:
            continue
        pk = a + int(np.argmax(sz[a:b + 1]))
        if sz[pk] < h:
            continue
        if pk < a + sl:  # the largest value left sits on a neighbour's shoulder: drop the shoulder, look at the rest
            todo.append((a + sl, b, 0, sr))
            continue
        if pk > b - sr:
            todo.append((a, b - sr, sl, 0))
            continue
        cut = max(h * C.HYSTERESIS_LOW, peak_fraction * sz[pk])
        lo = hi = pk
        while lo > a and sz[lo - 1] >= cut:
            lo -= 1
        while hi < b and sz[hi + 1] >= cut:
            hi += 1
        if hi - lo + 1 >= min_words:
            out.append((lo, hi, pk))
        todo += [(a, lo - 1, sl, half), (hi + 1, b, half, sr)]
    return sorted(out)


def decode_dim(dim: Dim, s: float, h: float, sentence: tuple[int, ...], signs: tuple[int, ...]) -> list[Region]:
    """Regions of one dimension in the directions `signs` at scale s and threshold h (candidate runs at h * HYSTERESIS_LOW,
    trimmed by the half-maximum rule)."""
    z = dim.x / s
    out: list[Region] = []
    if C.is_event(dim.key):
        for i in np.flatnonzero(np.isfinite(z) & dim.countable):
            sign = 1 if z[i] > 0 else -1
            if sign not in signs or abs(z[i]) < h:
                continue
            if dim.key == "D4" and not dim.p[i] < C.STRESS_P_MIN:
                continue  # the word is still stressed, so no emphasis is lost
            out.append(Region(dim.key, sign, int(i), int(i), int(i), float(z[i]), (int(i),)))
        return out
    n = len(z)
    for sign in signs:
        sz = np.where(np.isfinite(z), sign * z, -np.inf)
        low = sz >= h * C.HYSTERESIS_LOW
        i = 0
        while i < n:
            if not low[i]:
                i += 1
                continue
            j = i
            while j + 1 < n and low[j + 1] and sentence[j + 1] == sentence[i]:
                j += 1
            for lo, hi, pk in _peak_regions(sz, i, j, h, C.MIN_REGION_WORDS[dim.key], C.REGION_PEAK_FRACTION[dim.key]):
                out.append(Region(dim.key, sign, lo, hi, pk, float(z[pk]), tuple(range(lo, hi + 1))))
            i = j + 1
    return out


def threshold(regime: dict, dim: str, sign: int) -> float | None:
    """The threshold h of a dimension and direction; None where the regime does not flag it."""
    return regime["h"].get(key(dim, sign))


def flagged_dims(regime: dict) -> tuple[str, ...]:
    """Enabled dimensions with a threshold in at least one direction."""
    return tuple(k for k in regime["enabled"] if any(threshold(regime, k, s) is not None for s in C.FLAG_SIGNS[k]))


def decode(comp: Comparison, regime: dict, sentence: tuple[int, ...]) -> list[Region]:
    """The local regions of one comparison under a regime entry of detector.json."""
    regions: list[Region] = []
    for k in regime["enabled"]:
        for sign in C.FLAG_SIGNS[k]:
            h = threshold(regime, k, sign)
            if h is not None:
                regions += decode_dim(comp.dims[k], scale(regime, k, sign), h, sentence, (sign,))
    return sorted(regions, key=lambda r: (r.i0, r.dim, r.sign))


def clip_flags(comp: Comparison, regime: dict) -> dict[str, float]:
    """Whole-clip departures: tempo, pitch range and word-time unevenness beyond their enabled thresholds."""
    out = {}
    for k in C.CLIP_DIMS:
        if k not in regime['enabled'] or k not in comp.dims:
            continue
        if k == 'D7' and not regime.get('pattern_labels', {}).get('uneven_tempo', False):
            continue
        thr, g = regime["clip"].get(k), comp.dims[k].g
        if thr is not None and np.isfinite(g) and abs(g) > thr and (1 if g > 0 else -1) in C.FLAG_SIGNS[k]:
            out[k] = float(g)
    return out


def fit_clip(comps: list[Comparison], pair_weights=None) -> dict[str, float]:
    """Whole-clip thresholds from null pairs: CLIP_H robust units of the clip medians g (floored like the local scale)."""
    out = {}
    for k in C.CLIP_DIMS:
        g = np.array([c.dims[k].g for c in comps])
        ok = np.isfinite(g)
        w = np.ones(len(g)) if pair_weights is None else np.asarray(pair_weights)
        g, w = g[ok], w[ok]
        quantile = (lambda v, q: float(np.quantile(v, q))) if pair_weights is None else (lambda v, q: wquantile(v, w, q))
        spread = max(C.MAD_SCALE * quantile(np.abs(g - quantile(g, .5)), .5), quantile(np.abs(g), C.Q68)) if g.size else 0.0
        out[k] = round(C.CLIP_H * max(C.FLOORS[k], spread), 6)
    return out


def choose_h(dims: list[Dim], sentences: list[tuple[int, ...]], s: float, sign: int, minutes: float, budget: float,
             full_curve: bool = True, counting=None) -> tuple[float | None, list[dict]]:
    """Smallest h on the grid whose false regions per minute in direction `sign` over the null comparisons `dims` is <= the
    budget; None if no h qualifies. Returns (h, table of {h, regions, per_minute})."""
    table = []
    chosen = None
    for h in C.H_GRID:
        if counting is None:
            n = sum(len(decode_dim(d, s, h, sent, (sign,))) for d, sent in zip(dims, sentences))
            rate = n / minutes if minutes > 0 else float("inf")
        else:
            n, rate = counting(h)
        table.append({"h": h, "regions": int(n), "per_minute": round(float(rate), 4)})
        if chosen is None and rate <= budget:
            chosen = h
            if not full_curve:
                break
    return chosen, table


# ============================================================================================ detector.json
def config_hash(det: dict) -> str:
    """SHA-256 over the config constants and the fitted state (scales, thresholds, enabled dimensions, Pmax)."""
    state = {"config": C.as_dict(det["schema"]), "schema": det["schema"],
             "regimes": {r: {k: v[k] for k in ("scales", "h", "clip", "enabled", "name")} for r, v in sorted(det["regimes"].items())},
             "pmax": det["score"]["pmax"]}
    for r, v in det['regimes'].items():
        if 'pattern_labels' in v:
            state['regimes'][r]['pattern_labels'] = v['pattern_labels']
    return hashlib.sha256(json.dumps(state, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def make_detector(regimes: dict, pmax: dict, report: dict) -> dict:
    det = {"schema": SCHEMA, "pipeline_version": __version__, "regimes": regimes,
           "score": {"pmax": {k: round(float(v), 6) for k, v in pmax.items()}}, "report": report}
    det["config_sha256"] = config_hash(det)
    return det


def save_detector(det: dict, path: Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(det, indent=1, sort_keys=True) + "\n")


def load_detector(path: Path) -> dict:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found: run `python -m cvoice.calibrate` first")
    det = json.loads(path.read_text())
    if det.get("schema") != SCHEMA:
        raise ValueError(f"{path}: detector schema {det.get('schema')} != {SCHEMA}")
    for r, v in det["regimes"].items():
        if set(v["h"]) != set(KEYS) or set(v["clip"]) != set(C.CLIP_DIMS):
            raise ValueError(f"{path}: {r} needs a threshold entry per flag key and per whole-clip dimension")
    expected = {key(d, s) if C.is_event(d) else d for d in C.DIMS for s in C.FLAG_SIGNS[d]}
    if any(set(v['scales']) != expected for v in det['regimes'].values()):
        raise ValueError(f"{path}: needs a scale per event key and window dimension")
    if det["config_sha256"] != config_hash(det):
        raise ValueError(f"{path}: config hash mismatch (constants changed since calibration)")
    return det
