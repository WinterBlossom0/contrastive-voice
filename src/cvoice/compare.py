"""Contrastive deltas (participant P against baseline B, word i <-> word i) and the time map.

Units: D1, D3, D5, D6 have one unit per word (its five-word window); D2 one per word boundary (after word i);
D4 one per baseline stress word. x is NaN where the unit cannot be scored; for D2 x is defined at every eligible boundary
(the scale fit sees all of them) and `countable` marks those that may be flagged under the sign rules.
The windowed deltas are local: each is taken relative to the clip's own median difference, and for pace (D1) and pitch range
(D3) that median is kept as the whole-clip measure g (overall tempo, overall pitch range).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import config as C
from .features import Recording, final_pitch_word, final_span, sentence_final, stress_points, stress_words, word_occupancy


@dataclass
class Dim:
    """x: delta per unit in physical units (D1/D6 ln ratio, D2 s, D3 st, D4 p-units, D5 dB); b, p: the underlying
    baseline / participant measures; countable: unit may be flagged under the sign rules (D2, D4); w: unit weight
    (share of baseline duration, or 1/N events); g: whole-clip measure. D1 (ln speech-time ratio) and D3 (ln pitch-range
    ratio): the median that was removed from x. D9: the ln word-time ratio over all words; x is not centred. D7: the
    robust spread of x, MAD_SCALE * median |x| (uneven tempo). NaN for the other dimensions."""
    key: str
    x: np.ndarray
    b: np.ndarray
    p: np.ndarray
    countable: np.ndarray
    w: np.ndarray
    g: float = float("nan")

    def reference(self, i: int) -> float:
        """The baseline measure of unit i carried to the participant's overall tempo / pitch range / level, in the units of
        p: the value the participant would show there with no local departure (p against it is exactly x)."""
        x, p = float(self.x[i]), float(self.p[i])
        if self.key in ("D1", "D6"):
            return p / float(np.exp(x))
        if self.key == 'D7':
            return max((p + C.D7_REG_S) / float(np.exp(x)) - C.D7_REG_S, 0.0)
        if self.key == "D3":
            return max((p + C.RANGE_REG_ST) / float(np.exp(x)) - C.RANGE_REG_ST, 0.0)
        if self.key in ("D5", "D8"):
            return p - x
        return float(self.b[i])


@dataclass
class Comparison:
    dims: dict[str, Dim]
    map_p: np.ndarray  # participant knot times (s), strictly increasing
    map_b: np.ndarray  # baseline times (s) at those knots
    stress_b: list[int]
    stress_p: list[int]
    pts_b: np.ndarray  # stress points p per word, baseline
    pts_p: np.ndarray  # participant (baseline scales)
    coverage: dict[str, float]  # share of the baseline's word time (D2: boundaries) with a measurement, per dimension
    sentence: tuple[int, ...] = ()
    syllables: tuple[int, ...] = ()


def _centred_with_median(v: np.ndarray) -> tuple[np.ndarray, float]:
    """(v - g, g) with g the median of the finite entries of v (all NaN if there is none)."""
    ok = np.isfinite(v)
    if not ok.any():
        return np.full(len(v), np.nan), float("nan")
    g = float(np.median(v[ok]))
    return v - g, g


def _centred(v: np.ndarray) -> np.ndarray:
    return _centred_with_median(v)[0]


def _pause_eligible(B: Recording, P: Recording) -> np.ndarray:
    """Boundaries where either recording has an acoustic pause."""
    return (B.sil >= C.PAUSE_MIN_S) | (P.sil >= C.PAUSE_MIN_S)


def _duration_share(B: Recording) -> np.ndarray:
    d = B.regions[:, 1] - B.regions[:, 0]
    return d / d.sum()


def _speech_time(X: Recording, elig: np.ndarray) -> np.ndarray:
    """win_T with the pause rule applied to both recordings alike: where either has a pause at a boundary, each loses its own
    silent gap there, also one below PAUSE_MIN_S (otherwise a 0.19 s gap against a 0.21 s gap reads as a 0.2 s pace change)."""
    c = np.where(elig & (X.sil == 0), X.sil_raw, 0.0)
    return np.array([max(t - c[w[0]:w[1]].sum(), 1e-3) if w is not None else np.nan for t, w in zip(X.win_T, X.win)])


def paired_speech_time(B: Recording, P: Recording) -> tuple[np.ndarray, np.ndarray]:
    elig = _pause_eligible(B, P)
    return _speech_time(B, elig), _speech_time(P, elig)


def d1_pace(B: Recording, P: Recording) -> Dim:
    tb, tp = paired_speech_time(B, P)
    x, g = _centred_with_median(np.log(tp / tb))
    return Dim("D1", x, tb, tp, np.ones(len(x), bool), _duration_share(B), g)


def d2_pauses(B: Recording, P: Recording) -> Dim:
    n = len(B.tr)
    sb = B.sil
    elig = _pause_eligible(B, P)
    rb, rp = B.sil_raw, P.sil_raw  # the difference is taken on the uncut gap lengths: continuous across PAUSE_MIN_S
    x = np.where(elig, rp - rb, np.nan)
    punct = np.array([B.tr.punct[i] != "" for i in range(n - 1)])
    countable = elig & (((x < 0) & (sb >= C.PAUSE_DROP_MIN_BASE_S)) | ((x > 0) & (sb < C.PAUSE_MIN_S) & ~punct))
    n_events = max(1, int((sb >= C.PAUSE_MIN_S).sum()))
    return Dim("D2", x, np.where(elig, rb, np.nan), np.where(elig, rp, np.nan), countable, np.full(n - 1, 1.0 / n_events))


def d3_pitch(B: Recording, P: Recording) -> Dim:
    """ln ratio of the window pitch ranges, relative to the clip's overall ratio: speakers differ in overall liveliness by a
    factor, so the local question is where this speaker is flatter than their own usual range while the reference is not."""
    x, g = _centred_with_median(np.log((P.win_R + C.RANGE_REG_ST) / (B.win_R + C.RANGE_REG_ST)))
    return Dim("D3", x, B.win_R, P.win_R, np.ones(len(x), bool), _duration_share(B), g)


def d4_emphasis(B: Recording, P: Recording) -> tuple[Dim, list[int], list[int], np.ndarray, np.ndarray]:
    n = len(B.tr)
    pb = stress_points(B.ws.u, B.m, B.sigma)
    pp = stress_points(P.ws.u, P.m, B.sigma)  # participant: own medians, baseline scales
    sb, sp = stress_words(pb), stress_words(pp)
    x, bv, pv = (np.full(n, np.nan) for _ in range(3))
    for i in sb:
        if np.isfinite(pp[i]):
            x[i], bv[i], pv[i] = pp[i] - pb[i], pb[i], pp[i]
    countable = np.isfinite(x)
    return Dim("D4", x, bv, pv, countable, np.full(n, 1.0 / max(1, len(sb)))), sb, sp, pb, pp


def d5_volume(B: Recording, P: Recording) -> Dim:
    d = P.win_E - B.win_E
    return Dim("D5", _centred(d), B.win_E, P.win_E, np.ones(len(d), bool), _duration_share(B))


def d6_clarity(B: Recording, P: Recording) -> Dim:
    c = np.log((P.win_Q + 1e-6) / (B.win_Q + 1e-6))
    return Dim("D6", _centred(c), B.win_Q, P.win_Q, np.ones(len(c), bool), _duration_share(B))


def d9_speech_tempo(B: Recording, P: Recording) -> Dim:
    """D9 compares the aligned word durations only, ln participant/reference per five-word window, so
    the words themselves are measured and every pause is left to D2. It is not centred, and it is not the lab measure
    speech_time_ratio (aligned span minus pauses). g is the same ratio over all words."""
    x = np.log(P.win_W / B.win_W)
    whole = float(np.log(np.sum(P.al.end - P.al.start) / np.sum(B.al.end - B.al.start)))
    return Dim('D9', x, B.win_W, P.win_W, np.isfinite(x), _duration_share(B), whole)


def d7_word_time(B: Recording, P: Recording) -> Dim:
    b = B.occ if B.occ is not None else word_occupancy(B)
    p = P.occ if P.occ is not None else word_occupancy(P)
    ok = np.isfinite(b) & np.isfinite(p) & (b >= C.D7_MIN_S - 1e-9) & (p >= C.D7_MIN_S - 1e-9)
    x = np.full(len(B.tr), np.nan)
    x[ok] = np.log((p[ok] + C.D7_REG_S) / (b[ok] + C.D7_REG_S))
    x = _centred(x)
    g = float(C.MAD_SCALE * np.median(np.abs(x[ok]))) if ok.any() else float('nan')
    return Dim('D7', x, b, p, ok, np.full(len(x), 1 / len(x)), g)


def d8_ending(B: Recording, P: Recording) -> Dim:
    b = B.final_df0 if B.final_df0 is not None else final_pitch_word(B)
    p = P.final_df0 if P.final_df0 is not None else final_pitch_word(P)
    eligible = sentence_final(B.tr)
    ok = eligible & np.isfinite(b) & np.isfinite(p)
    x = np.where(ok, p - b, np.nan)
    return Dim('D8', x, b, p, ok, np.full(len(x), 1 / max(1, eligible.sum())))


def event_span(comp: Comparison, dim: str, i: int, B: Recording, P: Recording) -> tuple[float, float]:
    """Evidence span shared by matching and display; subtype selection never depends on the recipe."""
    if dim == 'D2':
        return pause_span(B, P, i, comp)
    if dim == 'D7':
        from .patterns import word_time
        return tuple(word_time(comp, B, P, i)['p'])
    if dim == 'D8':
        return final_span(P, i)
    if C.is_event(dim):
        return float(P.al.start[i]), float(P.al.end[i])
    raise KeyError(dim)


def time_map(B: Recording, P: Recording) -> tuple[np.ndarray, np.ndarray]:
    """Piecewise-linear map from participant time to baseline time through the word starts and ends; knots that would
    break monotonicity are dropped."""
    n = len(B.tr)
    pts = sorted([(P.al.start[i], B.al.start[i]) for i in range(n)] + [(P.al.end[i], B.al.end[i]) for i in range(n)])
    mp, mb = [], []
    for tp, tb in pts:
        if (not mp) or (tp > mp[-1] + 1e-6 and tb >= mb[-1]):
            mp.append(tp)
            mb.append(tb)
    if len(mp) < 2:
        raise ValueError("fewer than two words: no time map")
    return np.array(mp), np.array(mb)


def warp(t, map_p: np.ndarray, map_b: np.ndarray) -> np.ndarray:
    """Participant time(s) -> baseline time(s); slope 1 outside the mapped range."""
    t = np.asarray(t, dtype=float)
    out = np.interp(t, map_p, map_b)
    out = np.where(t < map_p[0], map_b[0] + (t - map_p[0]), out)
    return np.where(t > map_p[-1], map_b[-1] + (t - map_p[-1]), out)


def pause_span(B: Recording, P: Recording, i: int, comp: Comparison) -> tuple[float, float]:
    """Measured participant pause, else a removed-pause point mapped from the reference's acoustic span."""
    s, e = P.sil_span[i]
    if np.isfinite(s) and np.isfinite(e) and e > s:
        return float(s), float(e)
    bs, be = B.sil_span[i]
    boundary = float(warp((bs + be) / 2, comp.map_b, comp.map_p)) if np.isfinite(bs + be) else float(P.al.end[i])
    return boundary, boundary


def compare(B: Recording, P: Recording) -> Comparison:
    """All deltas plus the time map. B and P must carry the same transcript words."""
    if B.tr.norm != P.tr.norm:
        raise ValueError("baseline and participant transcripts differ")
    d4, sb, sp, pb, pp = d4_emphasis(B, P)
    dims = {"D1": d1_pace(B, P), "D2": d2_pauses(B, P), "D3": d3_pitch(B, P), "D4": d4, "D5": d5_volume(B, P),
            "D6": d6_clarity(B, P), "D9": d9_speech_tempo(B, P), 'D7': d7_word_time(B, P), 'D8': d8_ending(B, P)}
    mp, mb = time_map(B, P)
    w = _duration_share(B)
    valid = {k: np.isfinite(d.x) for k, d in dims.items()}
    # Event absence is a valid measurement; only missing acoustic evidence reduces coverage.
    valid["D2"] = np.isfinite(B.sil_raw) & np.isfinite(P.sil_raw)
    valid["D4"] = np.isfinite(pb) & np.isfinite(pp)
    coverage = {k: float(w[ok].sum()) for k, ok in valid.items() if k != "D2"}
    boundary_w = w[:-1]
    coverage["D2"] = float(boundary_w[valid["D2"]].sum() / boundary_w.sum()) if boundary_w.sum() else 0.0
    finals = sentence_final(B.tr)
    coverage['D8'] = float(valid['D8'][finals].mean()) if finals.any() else 0.0
    return Comparison(dims, mp, mb, sb, sp, pb, pp, coverage, B.tr.sentence, B.tr.syll)
