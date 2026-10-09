"""Flaw injection with exact sample time maps and labels.

Chain A (stored clips): numpy WSOLA for time, Praat PSOLA (parselmouth) for pitch. Chain B (evaluation only, RUSH / DRAG /
MONOTONE): Praat PSOLA duration + WORLD pitch. Edits are applied right to left; every edit contributes one Warp (a
monotone piecewise-linear map from samples before the edit to samples after it) and the whole clip is described by the
Chain of those warps, so labels follow analytically: a span [a, b) of the parent maps to
[chain(a, 'right'), chain(b, 'left')) in the clip. Samples outside the edit supports are bit-identical.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

import numpy as np
from scipy import signal
from scipy.ndimage import gaussian_filter1d

from . import audio
from . import config as C
from .features import Recording, frame_features, frame_slice, stress_points, stress_words

SR = C.SR


class EditError(RuntimeError):
    """An edit cannot be applied (no voiced material, no room tone, ...)."""


# ============================================================================================ time maps
class Warp:
    """Monotone piecewise-linear map from samples before an edit to samples after it. Repeated src knots = inserted
    material (a jump), repeated dst knots = removed material. side 'left' gives the left limit (use for interval ends),
    'right' the right limit (use for interval starts)."""

    def __init__(self, src, dst) -> None:
        self.src, self.dst = np.asarray(src, float), np.asarray(dst, float)
        if self.src.shape != self.dst.shape or len(self.src) < 2 or np.any(np.diff(self.src) < 0) or np.any(np.diff(self.dst) < 0):
            raise ValueError("a warp needs at least two knots and monotone non-decreasing src and dst")

    def __call__(self, t, side: str = "left"):
        t = np.asarray(t, float)
        i = np.clip(np.searchsorted(self.src, t, side=side), 1, len(self.src) - 1)
        x0, x1, y0, y1 = self.src[i - 1], self.src[i], self.dst[i - 1], self.dst[i]
        ok = x1 > x0
        w = np.where(ok, (t - x0) / np.where(ok, x1 - x0, 1.0), 0.0 if side == "left" else 1.0)
        out = y0 + np.clip(w, 0.0, 1.0) * (y1 - y0)
        out = np.where(ok & (y1 - y0 == x1 - x0), y0 + (t - x0), out)  # unedited stretches stay exact: a rounding error here moves t across a later knot
        out = np.where(t < self.src[0], self.dst[0] + (t - self.src[0]), out)  # slope 1 outside the knots
        return np.where(t > self.src[-1], self.dst[-1] + (t - self.src[-1]), out)


class Chain:
    """Warps in application order; evaluating maps parent samples to final samples."""

    def __init__(self) -> None:
        self.warps: list[Warp] = []

    def __call__(self, t, side: str = "left"):
        for w in self.warps:
            t = w(t, side)
        return t

    def cur(self, a: float, b: float) -> tuple[int, int]:
        """Current (a, b) of a parent span: start via the right limit, end via the left limit."""
        return int(round(float(self(a, "right")))), int(round(float(self(b, "left"))))


# ============================================================================================ primitives (numpy)
def _xfade(n: int) -> np.ndarray:
    """Raised-cosine fade-in of n samples."""
    return 0.5 - 0.5 * np.cos(np.pi * (np.arange(n) + 0.5) / n)


def _ramp_window(t: np.ndarray, t0: float, t1: float, ramp: float) -> np.ndarray:
    """1 inside [t0, t1] with raised-cosine ramps of `ramp` inside the span; 0 outside."""
    ramp = min(ramp, (t1 - t0) / 2)
    w = np.zeros_like(t, dtype=float)
    w[(t >= t0) & (t <= t1)] = 1.0
    if ramp > 0:
        up, dn = (t >= t0) & (t < t0 + ramp), (t > t1 - ramp) & (t <= t1)
        w[up] = 0.5 - 0.5 * np.cos(np.pi * (t[up] - t0) / ramp)
        w[dn] = 0.5 - 0.5 * np.cos(np.pi * (t1 - t[dn]) / ramp)
    return w


def wsola(x: np.ndarray, a: int, b: int, rate: float) -> np.ndarray:
    """Time-scale x[a:b] by `rate` (> 1 faster) reading real context around the span. Integer correlation, so the result
    is platform independent; each frame stays within +-tolerance of its ideal position (no drift)."""
    N = int(round(C.WSOLA_FRAME_MS / 1000 * SR))
    N += N % 2
    Hs = N // 2
    tol = int(round(C.WSOLA_TOL_MS / 1000 * SR))
    w = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(N) / N)
    n_out = int(round((b - a) / rate))
    K = int(np.ceil(n_out / Hs)) + 1
    stepf = Hs * rate
    front, back = Hs + tol + N, int(np.ceil(stepf)) + 2 * tol + 3 * N
    xp = np.concatenate([np.zeros(front), x, np.zeros(back)])
    xi = np.round(xp * 32767.0).astype(np.int64)
    yb = np.zeros((K + 1) * Hs + N)
    prev = a - Hs
    for k in range(K):
        ideal = a - Hs if k == 0 else a + int(round((k - 1) * stepf))
        if k == 0:
            p = ideal
        else:
            target = xi[front + prev + Hs:front + prev + Hs + N]
            lo = front + ideal - tol
            cand = xi[lo:lo + N + 2 * tol]
            cc = np.correlate(cand, target, mode="valid")
            if cc.max() <= 0:
                j = tol
            else:
                sq = np.concatenate([[0], np.cumsum(cand * cand)])
                energy = sq[N:N + 2 * tol + 1] - sq[:2 * tol + 1]
                j = int(np.argmax(cc / np.sqrt(np.maximum(energy, 1).astype(np.float64))))
            p = ideal - tol + j
        yb[k * Hs:k * Hs + N] += w * xp[front + p:front + p + N]
        prev = p
    return yb[Hs:Hs + n_out].copy()


def stretch_span(x: np.ndarray, a: int, b: int, rate: float) -> tuple[np.ndarray, Warp, int]:
    """Replace x[a:b] by its WSOLA time-scaled version (exit cross-fade of XFADE_S). Returns (y, warp, new length)."""
    seg = wsola(x, a, b, rate)
    n_new, f = len(seg), int(round(C.XFADE_S * SR))
    y = np.concatenate([x[:a], seg, x[b:]])
    fi = _xfade(f)
    y[a + n_new - f:a + n_new] = seg[n_new - f:] * (1 - fi) + x[b - f:b] * fi
    N = len(x)
    return y, Warp([0, a, b, N], [0, a, a + n_new, N - (b - a) + n_new]), n_new


def speech_pieces(a: int, b: int, pauses: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """[a, b) split at the pauses (>= PAUSE_MIN_S) it contains; speech pieces shorter than WSOLA_MIN_PIECE_S are dropped."""
    pieces, cur = [], a
    for p0, p1 in sorted(pauses):
        if p1 <= a or p0 >= b or p1 - p0 < C.PAUSE_MIN_S * SR:
            continue
        p0, p1 = max(p0, a), min(p1, b)
        pieces.append((cur, p0))
        cur = p1
    pieces.append((cur, b))
    return [(s0, s1) for s0, s1 in pieces if s1 - s0 >= C.WSOLA_MIN_PIECE_S * SR]


def stretch_speech(x: np.ndarray, a: int, b: int, rate: float, pauses: list[tuple[int, int]]) -> tuple[np.ndarray, list[Warp], dict]:
    """Time-scale the speech inside [a, b) by `rate`; in-span pauses stay unscaled. Pieces are processed right to left."""
    warps, old, new = [], 0, 0
    for s0, s1 in reversed(speech_pieces(a, b, pauses)):
        x, w, n_new = stretch_span(x, s0, s1, rate)
        warps.append(w)
        old, new = old + (s1 - s0), new + n_new
    return x, warps, {"speech_old": old, "speech_new": new}


def room_tone(rec: Recording):
    """tone(n): n samples of room tone tiled (equal-power cross-fades) from the recording's own silent runs. Raises
    EditError when no run is long enough."""
    from .align import pause_threshold
    silent = (rec.fr.L < pause_threshold(rec.fr.L)) & ~rec.fr.voiced
    d = np.diff(np.r_[0, silent.astype(np.int8), 0])
    guard = int(C.ROOM_TONE_GUARD_S * SR)
    chunks = []
    for k0, k1 in zip(np.flatnonzero(d == 1), np.flatnonzero(d == -1)):
        s0, s1 = int(k0 * C.HOP) + guard, int(k1 * C.HOP) - guard
        if s1 - s0 >= C.ROOM_TONE_MIN_S * SR:
            chunks.append(rec.wav[s0:s1].copy())
    if not chunks:
        raise EditError("no silent run long enough for room tone")
    chunks.sort(key=lambda c: float(np.mean(c * c)))
    q = float(np.mean(chunks[0] ** 2))
    chunks = [c for c in chunks if float(np.mean(c * c)) <= q * 10 ** (C.ROOM_TONE_DB_SPREAD / 10)]
    f = int(C.ROOM_TONE_XFADE_S * SR)
    fi = _xfade(f)

    def tone(n: int) -> np.ndarray:
        out, i = chunks[0].copy(), 1
        while len(out) < n:
            c = chunks[i % len(chunks)]
            i += 1
            out[-f:] = out[-f:] * np.sqrt(1 - fi) + c[:f] * np.sqrt(fi)
            out = np.concatenate([out, c[f:]])
        return out[:n].copy()

    return tone


def insert_pause(x: np.ndarray, i: int, n: int, tone) -> tuple[np.ndarray, Warp]:
    """Insert n samples of room tone at sample i; speech fades out / in over PAUSE_FADE_S with the tone underneath."""
    f = int(round(C.PAUSE_FADE_S * SR))
    fi = _xfade(f)
    pre, post = x[:i].copy(), x[i:].copy()
    pre[-f:] *= 1 - fi
    post[:f] *= fi
    fill = tone(n + 2 * f).copy()
    fill[:f] *= np.sqrt(fi)
    fill[-f:] *= np.sqrt(1 - fi)
    y = np.concatenate([pre, np.zeros(n), post])
    y[i - f:i + n + f] += fill
    N = len(x)
    return y, Warp([0, i, i, N], [0, i, i + n, N + n])


def remove_pause(x: np.ndarray, p0: int, p1: int, keep: int) -> tuple[np.ndarray, Warp]:
    """Shorten the pause [p0, p1) to `keep` samples by cutting its middle; equal-power cross-fade over PAUSE_FADE_S."""
    cut = (p1 - p0) - keep
    a = p0 + keep // 2
    b = a + cut
    f = int(round(C.PAUSE_FADE_S * SR))
    fi = _xfade(f)
    y = np.concatenate([x[:a], x[b:]])
    y[a - f:a] = x[a - f:a] * np.sqrt(1 - fi) + x[b - f:b] * np.sqrt(fi)
    N = len(x)
    return y, Warp([0, a, b, N], [0, a, a, N - cut])


def gain_ramp(x: np.ndarray, a: int, b: int, gain_db: float, tone) -> np.ndarray:
    """Gain falls linearly in dB to gain_db over the first third of [a, b), holds to b, returns to 0 dB over FADE_RELEASE_S.
    Room tone of power (1 - g^2) keeps the background floor from pumping."""
    rel = int(round(C.FADE_RELEASE_S * SR))
    t = np.arange(len(x))
    knots = [a, a + (b - a) * C.FADE_RAMP_FRACTION, b, b + rel]
    g = 10 ** (np.interp(t, knots, [0.0, gain_db, gain_db, 0.0], left=0.0, right=0.0) / 20)
    y = x * g
    sl = slice(a, min(b + rel, len(x)))
    if gain_db < 0:
        y[sl] += tone(sl.stop - sl.start) * np.sqrt(np.clip(1 - g[sl] ** 2, 0, None))
    return y


def _cep_envelope(logmag: np.ndarray, n_cep: int) -> np.ndarray:
    c = np.fft.irfft(logmag, axis=0)
    c[n_cep:-n_cep + 1] = 0.0
    return np.fft.rfft(c, axis=0).real


def mumble(x: np.ndarray, a: int, b: int, strength: float) -> np.ndarray:
    """Under-articulation without a vocoder: time-varying filter H = E'/E on the STFT. The per-frame cepstral envelope
    shape is smeared in time and pulled toward the span's mean shape; frame level and F0 are untouched."""
    nfft, hop = C.MUMBLE_NFFT, C.MUMBLE_HOP
    f, tt, X = signal.stft(x, SR, nperseg=nfft, noverlap=nfft - hop, boundary="zeros", padded=True)
    E = _cep_envelope(np.log(np.abs(X) + 1e-9), max(8, int(0.0015 * SR)))
    L = E.mean(axis=0, keepdims=True)
    S = E - L
    bw = strength * _ramp_window(tt, a / SR, b / SR, C.FLATTEN_RAMP_S)[None, :]
    inside = (tt >= a / SR) & (tt <= b / SR)
    speech = inside & (L[0] > np.percentile(L[0][inside], 20))
    S_mean = S[:, speech].mean(axis=1, keepdims=True)
    sigma = max(1e-6, strength * C.MUMBLE_SIGMA_MS / 1000 * SR / hop)
    S_new = (1 - bw) * ((1 - bw) * S + bw * gaussian_filter1d(S, sigma, axis=1, mode="nearest")) + bw * S_mean
    lim = C.MUMBLE_MAX_GAIN_DB / 20 * np.log(10)
    Y = X * np.exp(np.clip(S_new - S, -4 * lim, lim))
    Y *= np.sqrt((np.abs(X) ** 2).sum(axis=0) / np.maximum((np.abs(Y) ** 2).sum(axis=0), 1e-20))[None, :]  # keep each frame's level: mumbling is not a fade
    _, y = signal.istft(Y, SR, nperseg=nfft, noverlap=nfft - hop, boundary=True)
    y = np.pad(y, (0, max(0, len(x) - len(y))))[:len(x)]
    out = x.copy()
    out[a:b] = y[a:b]
    return out


# ============================================================================================ Praat PSOLA / WORLD
def psola(x: np.ndarray, pitch_fn=None, dur_points=None) -> tuple[np.ndarray, float]:
    """Whole-clip TD-PSOLA through a Praat Manipulation object; the Praat RNG is seeded first (K). pitch_fn(times, f0,
    median) -> new f0; dur_points = [(time_s, relative_duration)]. Returns (resynthesis, median F0 Hz)."""
    import parselmouth
    from parselmouth.praat import call
    parselmouth.praat.run(f"random_initializeWithSeedUnsafelyButPredictably: {C.PRAAT_SEED}")
    snd = parselmouth.Sound(np.ascontiguousarray(x, dtype=np.float64), sampling_frequency=SR)
    man = call(snd, "To Manipulation", C.PSOLA_STEP_S, *C.PSOLA_F0)
    pt = call(man, "Extract pitch tier")
    n = int(call(pt, "Get number of points"))
    if n == 0:
        raise EditError("no voiced frames for PSOLA")
    times = np.array([call(pt, "Get time from index", i + 1) for i in range(n)])
    vals = np.array([call(pt, "Get value at index", i + 1) for i in range(n)])
    med = float(np.median(vals))
    if pitch_fn is not None:
        pt2 = call("Create PitchTier", "p", 0.0, snd.duration)
        for t, v in zip(times, pitch_fn(times, vals, med)):
            call(pt2, "Add point", float(t), float(v))
        call([man, pt2], "Replace pitch tier")
    if dur_points:
        dt = call("Create DurationTier", "d", 0.0, snd.duration)
        for t, f in dur_points:
            call(dt, "Add point", float(t), float(f))
        call([man, dt], "Replace duration tier")
    return call(man, "Get resynthesis (overlap-add)").values[0].copy(), med


def _flatten_fn(a: int, b: int, strength: float, ramp: float):
    """F0 compression toward the speaker median in the semitone domain: st' = (1 - strength * w(t)) * st."""
    def fn(times, f0, med):
        w = _ramp_window(times, a / SR, b / SR, ramp)
        return med * 2 ** (12 * np.log2(f0 / med) * (1 - strength * w) / 12)
    return fn


def splice_whole(x: np.ndarray, y: np.ndarray, a: int, b: int, b2: int, equal_power: bool = False) -> np.ndarray:
    """Keep y[a:b2] (a whole-clip resynthesis) in place of x[a:b], cross-faded over SPLICE_FADE_S on the original side
    of both edges; everything outside [a - f, b + f) is x, bit-identical."""
    f = int(round(C.SPLICE_FADE_S * SR))
    fi = _xfade(f)
    up, dn = (np.sqrt(fi), np.sqrt(1 - fi)) if equal_power else (fi, 1 - fi)
    y = np.pad(y, (0, max(0, b2 + f - len(y))))
    head = x[a - f:a] * dn + y[a - f:a] * up
    tail = y[b2:b2 + f] * dn + x[b:b + f] * up
    return np.concatenate([x[:a - f], head, y[a:b2], tail, x[b + f:]])


def flatten_span(x: np.ndarray, a: int, b: int, strength: float, ramp: float = C.FLATTEN_RAMP_S) -> np.ndarray:
    """PSOLA F0 compression over [a, b) spliced back (length preserved)."""
    y, _ = psola(x, pitch_fn=_flatten_fn(a, b, strength, ramp))
    return splice_whole(x, np.pad(y, (0, max(0, len(x) - len(y))))[:len(x)], a, b, b)


def deemphasis(x: np.ndarray, a: int, b: int, strength: float) -> tuple[np.ndarray, list[Warp], dict]:
    """Remove the prominence of one word: flatten its F0 excursion (PSOLA), shorten it (WSOLA), lower it, all scaled by
    strength."""
    y = flatten_span(x, a, b, strength, C.DEEMPH_RAMP_S)
    y, w, n_new = stretch_span(y, a, b, 1 + strength * (C.DEEMPH_MAX_RATE - 1))
    t = np.arange(len(y)) / SR
    y = y * 10 ** (strength * C.DEEMPH_MAX_GAIN_DB * _ramp_window(t, a / SR, (a + n_new) / SR, C.DEEMPH_RAMP_S) / 20)
    return y, [w], {"speech_old": b - a, "speech_new": n_new}


def world_flatten(x: np.ndarray, a: int, b: int, strength: float) -> np.ndarray:
    """Chain B pitch: WORLD (harvest / cheaptrick / d4c) resynthesis with F0 compressed over [a, b), spliced back
    with equal-power cross-fades."""
    import pyworld as pw
    xd = np.ascontiguousarray(x, dtype=np.float64)
    f0, t = pw.harvest(xd, SR, f0_floor=C.PSOLA_F0[0], f0_ceil=C.PSOLA_F0[1], frame_period=5.0)
    sp, ap = pw.cheaptrick(xd, f0, t, SR, f0_floor=C.PSOLA_F0[0]), pw.d4c(xd, f0, t, SR)
    v = f0 > 0
    if not v.any():
        raise EditError("no voiced frames for WORLD")
    f0n = f0.copy()
    f0n[v] = _flatten_fn(a, b, strength, C.FLATTEN_RAMP_S)(t[v], f0[v], float(np.median(f0[v])))
    y = pw.synthesize(f0n, sp, ap, SR, 5.0)
    return splice_whole(x, np.pad(y, (0, max(0, len(x) - len(y))))[:len(x)], a, b, b, equal_power=True)


TIER_EPS_S = 0.001  # s, linear transition of the Praat duration tier
TIER_PAD = int(np.ceil(TIER_EPS_S * SR)) + 1  # samples either side of a scaled span that the PSOLA splice covers


def stretch_speech_psola(x: np.ndarray, a: int, b: int, rate: float, pauses: list[tuple[int, int]]) -> tuple[np.ndarray, Warp, dict]:
    """Chain B time: Praat PSOLA duration tier over the speech pieces of [a, b) (pauses at 1.0), whole-clip resynthesis
    spliced back. The warp follows the nominal duration tier (1 ms transitions)."""
    pieces = speech_pieces(a, b, pauses)
    if not pieces:
        raise EditError("no speech piece long enough to scale")
    eps = TIER_EPS_S
    pts: list[tuple[float, float]] = []
    src, dst = [0.0], [0.0]

    def add(s: float, inc: float) -> None:
        src.append(s)
        dst.append(dst[-1] + inc)

    for s0, s1 in pieces:
        t0, t1, f = s0 / SR, s1 / SR, 1.0 / rate
        pts += [(t0 - eps, 1.0), (t0, f), (t1, f), (t1 + eps, 1.0)]
        add(t0 - eps, t0 - eps - src[-1])
        add(t0, eps * (1 + f) / 2)
        add(t1, (t1 - t0) * f)
        add(t1 + eps, eps * (1 + f) / 2)
    N = len(x)
    add(N / SR, N / SR - src[-1])
    S, D = np.array(src) * SR, np.array(dst) * SR
    y, _ = psola(x, dur_points=sorted(pts))
    a_s, b_s = a - TIER_PAD, b + TIER_PAD  # the duration tier is back to 1.0 here, so both edges are unshifted / constant-shift
    b2 = int(round(float(np.interp(b_s, S, D))))
    D[-1] = N + (b2 - b_s)
    new = int(round(sum(float(np.interp(s1, S, D)) - float(np.interp(s0, S, D)) for s0, s1 in pieces)))
    return splice_whole(x, y, a_s, b_s, b2), Warp(S, D), {"speech_old": sum(s1 - s0 for s0, s1 in pieces), "speech_new": new}


# ============================================================================================ edits
WINDOWED = ("RUSH", "DRAG", "MONOTONE", "FADE", "MUMBLE")
MAGNITUDE = {"RUSH": ("duration_ratio", "x"), "DRAG": ("duration_ratio", "x"), "PAUSE_DROPPED": ("kept_fraction", "fraction"),
             "PAUSE_INTRUSIVE": ("inserted_s", "s"), "MONOTONE": ("f0_range_kept", "fraction"),
             "DEEMPHASIS": ("strength", "fraction"), "FADE": ("gain_db", "dB"), "MUMBLE": ("strength", "fraction")}


@dataclass
class Edit:
    """One edit in parent coordinates. [a, b) is the parent sample span acted on (insertion point: a == b; dropped pause:
    the silent run). words = (first, last) word touched (boundary edits: (i, i + 1)). param = physical magnitude of the
    level (None: null parameters, i.e. a placebo edit)."""
    type: str
    level: int | None
    a: int
    b: int
    words: tuple[int, int]
    param: float | dict | None
    pauses: tuple = ()
    selection: str | None = None

    @property
    def kind(self) -> str:
        return C.FLAW_REGISTRY[self.type]["event"]


def level_param(typ: str, level: int | None) -> float | None:
    """Physical magnitude of a level (None for placebo edits)."""
    return None if level is None else C.LEVEL_PARAM[typ][level - 1]


def apply_edit(x: np.ndarray, ed: Edit, chain: Chain, tone, chain_name: str = "A") -> tuple[np.ndarray, dict]:
    """Apply one edit to x (current coordinates found through `chain`), append its warps, return (y, info)."""
    t, p = ed.type, ed.param
    a, b = chain.cur(ed.a, ed.b)
    info: dict = {}
    if t in ("RUSH", "DRAG"):
        rate = 1.0 if p is None else (p if t == "RUSH" else 1.0 / p)
        pauses = [chain.cur(q0, q1) for q0, q1 in ed.pauses]
        if chain_name == "A":
            x, warps, info = stretch_speech(x, a, b, rate, pauses)
        else:
            x, w, info = stretch_speech_psola(x, a, b, rate, pauses)
            warps = [w]
        chain.warps += warps
    elif t == "PAUSE_DROPPED":
        dur = b - a
        keep = dur if p is None else max(int(round(p * dur)), int(round(C.PAUSE_FLOOR_S * SR)))
        info = {"keep": keep, "cut": dur - keep}
        if dur - keep > 0:
            x, w = remove_pause(x, a, b, keep)
            chain.warps.append(w)
    elif t == "PAUSE_INTRUSIVE":
        n = 0 if p is None else int(round(p * SR))
        i = int(round(float(chain(ed.a, "left"))))
        info = {"inserted": n}
        if n > 0:
            x, w = insert_pause(x, i, n, tone)
            chain.warps.append(w)
    elif t == "MONOTONE":
        strength = 0.0 if p is None else 1.0 - p
        x = flatten_span(x, a, b, strength) if chain_name == "A" else world_flatten(x, a, b, strength)
    elif t == "DEEMPHASIS":
        x, warps, info = deemphasis(x, a, b, 0.0 if p is None else p)
        chain.warps += warps
    elif t == "FADE":
        if p is not None and p != 0:
            x = gain_ramp(x, a, b, -p, tone)
    elif t == "MUMBLE":
        x = mumble(x, a, b, 0.0 if p is None else p)
    else:
        raise ValueError(f"unknown flaw type {t}")
    return x, info


def apply_edits(rec: Recording, edits: list[Edit], chain_name: str = "A") -> tuple[np.ndarray, Chain, list[dict]]:
    """Apply edits right to left (by parent start). Returns (clip on the int16 grid, chain, info per edit in input order)."""
    x = rec.wav.copy()
    chain = Chain()
    need_tone = any(e.type in ("PAUSE_INTRUSIVE", "FADE") and e.param is not None and e.param != 0 for e in edits)
    tone = room_tone(rec) if need_tone else None
    infos: dict[int, dict] = {}
    for k in sorted(range(len(edits)), key=lambda k: (-edits[k].a, k)):
        ed = edits[k]
        if ed.type in C.EXTRA_TYPES:
            if chain_name != "A":
                raise ValueError("extra recipes support chain A only")
            try:
                measurements = []
                y, local, lab = render_extra(rec, ed, measurements)
            except EditError as exc:
                infos[k] = {"skipped": str(exc)}
                continue
            f = lab["flaws"][0]
            lo, hi = min(a for a, b in f["parent_supports"]), max(b for a, b in f["parent_supports"])
            a, b = chain.cur(lo, hi)
            u, v = round(float(local(lo, "left"))), round(float(local(hi, "right")))
            x = np.r_[x[:a], y[u:v], x[b:]]
            chain.warps += local.warps
            infos[k] = {"extra": f, "suffix_start": len(chain.warps), "duration_delta_samples": len(y) - len(rec.wav), "measure": measurements[0]}
        else:
            x, infos[k] = apply_edit(x, ed, chain, tone, chain_name)
    return audio.quantize(x), chain, [infos[k] for k in range(len(edits))]


# ============================================================================================ planning
@dataclass
class Plan:
    edits: list[Edit]
    skipped: list[dict] = field(default_factory=list)


def clip_seed(clip_id: str) -> int:
    return int(hashlib.sha256(clip_id.encode()).hexdigest()[:8], 16)


def parent_pauses(rec: Recording) -> list[tuple[int, int]]:
    """Acoustic pauses (>= PAUSE_MIN_S) of a recording as sample intervals."""
    return [(int(round(s * SR)), int(round(e * SR))) for s, e in rec.sil_span if np.isfinite(s)]


def stress_set(rec: Recording, sigma: np.ndarray | None = None) -> set[int]:
    """Stress words of rec (own medians; scales from `sigma` when given, e.g. the baseline's)."""
    return set(stress_words(stress_points(rec.ws.u, rec.m, rec.sigma if sigma is None else sigma)))


# Types placed on a stressed word: shared stress first, then own stress, then any eligible content word.
STRESS_FALLBACK_TYPES = ("SOUND_REPETITION", "ONSET_PROLONGATION", "BLOCK")


def shared_stress(rec: Recording, ref: Recording | None) -> set[int]:
    """Words stressed in both rec and ref (on the scales of ref); the own stress words of rec when there is no ref."""
    if ref is None:
        return stress_set(rec)
    return stress_set(ref) & stress_set(rec, ref.sigma)


def stress_selection(word: int, shared: set[int], rec: Recording) -> str:
    if word in shared:
        return "shared stress"
    if word in stress_set(rec):
        return "own stress fallback"
    return "content fallback"


def _span_samples(rec: Recording, i0: int, i1: int) -> tuple[int, int]:
    N = len(rec.wav)
    return max(int(round(rec.regions[i0, 0] * SR)), 0), min(int(round(rec.regions[i1, 1] * SR)), N)


def _candidates(rec: Recording, ref: Recording | None, typ: str, width: int, taken: list[tuple[int, int]],
                same_sentence: bool = True) -> list[tuple[int, int]]:
    """Eligible (first, last) word positions for an edit of this type."""
    if typ in C.EXTRA_TYPES:
        return extra_candidates(rec, ref, typ, width, taken)
    n, g, tr = len(rec.tr), C.EDIT_GAP_WORDS, rec.tr
    def free(i0, i1):
        return all(i1 + g < t0 or i0 - g > t1 for t0, t1 in taken)
    out = []
    if typ in WINDOWED:
        for i0 in range(0, n - width + 1):
            i1 = i0 + width - 1
            if free(i0, i1) and (not same_sentence or tr.sentence[i0] == tr.sentence[i1]):
                out.append((i0, i1))
    elif typ == "DEEMPHASIS":
        s = shared_stress(rec, ref)
        out = [(i, i) for i in sorted(s) if free(i, i)]
    else:
        for i in range(n - 1):
            if not free(i, i + 1):
                continue
            if typ == "PAUSE_DROPPED":
                good = rec.sil[i] >= C.PAUSE_DROP_MIN_BASE_S and (ref is None or ref.sil[i] >= C.PAUSE_DROP_MIN_BASE_S)
            else:
                good = rec.sil[i] == 0 and tr.punct[i] == "" and rec.al.start[i + 1] - rec.al.end[i] >= C.INSERT_MIN_GAP_S
            if good:
                out.append((i, i + 1))
    return out


def make_edit(rec: Recording, typ: str, level: int | None, pos: tuple[int, int]) -> Edit:
    """Turn a chosen word position into an Edit with parent sample spans."""
    i0, i1 = pos
    param = level_param(typ, level)
    if typ in C.EXTRA_TYPES:
        return Edit(typ, level, round(rec.al.start[i0] * SR), round(rec.al.end[i1] * SR), pos, param)
    if typ == "PAUSE_DROPPED":
        s, e = rec.sil_span[i0]
        return Edit(typ, level, int(round(s * SR)), int(round(e * SR)), pos, param)
    if typ == "PAUSE_INTRUSIVE":
        k0 = int(np.ceil(rec.al.end[i0] / C.HOP_S - 1e-9))
        k1 = max(int(np.ceil(rec.al.start[i1] / C.HOP_S - 1e-9)), k0 + 1)
        k = k0 + int(np.argmin(rec.fr.L[k0:k1])) if k0 < len(rec.fr.L) else k0
        s = min(k * C.HOP, len(rec.wav))
        return Edit(typ, level, s, s, pos, param)
    a, b = _span_samples(rec, i0, i1)
    pauses = tuple((p0, p1) for p0, p1 in parent_pauses(rec) if p1 > a and p0 < b) if typ in ("RUSH", "DRAG") else ()
    return Edit(typ, level, a, b, pos, param, pauses)


def plan_clip(rec: Recording, specs: list[tuple[str, int | None]], seed: int, *, ref: Recording | None = None,
              cap: float | None = C.COVERAGE_CAP, null_width: bool = False, attempts: int = 200) -> Plan:
    """Place one edit per (type, level) spec: windowed types take 5-8 words (5 for placebo clips), pauses one boundary,
    DEEMPHASIS one stress word; positions are uniform over eligible positions, edits stay EDIT_GAP_WORDS apart, and the
    edited word coverage stays <= cap (None: no cap; the cap is hard). `ref` = the baseline when rec is another speaker's
    rendition. Deterministic in `seed`; returns the attempt under the cap with the fewest skipped specs; when every attempt is
    over the cap, the first one with its last windowed edits dropped (recorded as skipped) until it is under."""
    n = len(rec.tr)
    def coverage(edits):
        return sum(e.words[1] - e.words[0] + 1 for e in edits if e.kind != "boundary") / n
    best: Plan | None = None
    over: Plan | None = None
    for attempt in range(attempts):
        rng = np.random.default_rng([seed, attempt])
        taken: list[tuple[int, int]] = []
        edits: list[Edit] = []
        skipped: list[dict] = []
        for typ, level in specs:
            width = C.SPAN_WORDS[0] if (null_width or attempt >= attempts // 2) else int(rng.integers(C.SPAN_WORDS[0], C.SPAN_WORDS[1] + 1))
            cands = _candidates(rec, ref, typ, width, taken) or (_candidates(rec, ref, typ, width, taken, False) if typ in WINDOWED else [])
            if not cands:
                skipped.append({"type": typ, "level": level, "reason": "no eligible position"})
                continue
            pos = cands[int(rng.integers(len(cands)))]
            taken.append(pos)
            ed = make_edit(rec, typ, level, pos)
            if typ in STRESS_FALLBACK_TYPES:
                ed.selection = stress_selection(pos[0], shared_stress(rec, ref), rec)
            edits.append(ed)
        plan = Plan(edits, skipped)
        if cap is not None and coverage(edits) > cap:
            over = over or plan
            continue
        if not skipped:
            return plan
        if best is None or len(skipped) < len(best.skipped):
            best = plan
    if best is not None:
        return best
    assert over is not None
    edits, skipped = list(over.edits), list(over.skipped)
    while edits and coverage(edits) > cap:
        e = edits.pop(max(i for i, e in enumerate(edits) if e.kind != "boundary"))
        skipped.append({"type": e.type, "level": e.level, "reason": f"coverage cap {cap}"})
    return Plan(edits, skipped)


def plan_botched(rec: Recording, seed: int) -> Plan:
    """Bottom ladder rung: whole-passage RUSH (x1.9) and MONOTONE (k = 0), every pause >= 0.5 s dropped to 0.06 s, and
    G5_FADES level-3 fades. Exempt from the coverage cap."""
    n = len(rec.tr)
    a, b = _span_samples(rec, 0, n - 1)
    edits = [make_edit(rec, "RUSH", 3, (0, n - 1)), make_edit(rec, "MONOTONE", 3, (0, n - 1))]
    edits[0].a, edits[0].b = edits[1].a, edits[1].b = a, b
    edits += [make_edit(rec, "PAUSE_DROPPED", 3, (i, i + 1)) for i in range(n - 1) if rec.sil[i] >= C.PAUSE_DROP_MIN_BASE_S]
    rng = np.random.default_rng([seed, 5])
    taken: list[tuple[int, int]] = []
    skipped: list[dict] = []
    for _ in range(C.G5_FADES):
        cands = _candidates(rec, None, "FADE", C.SPAN_WORDS[1], taken) or _candidates(rec, None, "FADE", C.SPAN_WORDS[1], taken, False)
        if not cands:
            skipped.append({"type": "FADE", "level": 3, "reason": "no eligible position"})
            continue
        pos = cands[int(rng.integers(len(cands)))]
        taken.append(pos)
        edits.append(make_edit(rec, "FADE", 3, pos))
    return Plan(edits, skipped)


# ============================================================================================ labels
def _support(ed: Edit, info: dict, chain_name: str) -> tuple[int, int]:
    """Parent samples whose values the edit may change (cross-fades and the fade release included)."""
    f = int(round(C.SPLICE_FADE_S * SR))
    if ed.type == "PAUSE_DROPPED":
        a_cut = ed.a + info["keep"] // 2
        return a_cut - int(round(C.PAUSE_FADE_S * SR)), a_cut + info["cut"]
    if ed.type == "PAUSE_INTRUSIVE":
        f = int(round(C.PAUSE_FADE_S * SR))
        return ed.a - f, ed.a + f
    if ed.type in ("MONOTONE", "DEEMPHASIS") or (ed.type in ("RUSH", "DRAG") and chain_name == "B"):
        pad = TIER_PAD if ed.type in ("RUSH", "DRAG") else 0
        return ed.a - f - pad, ed.b + f + pad
    if ed.type == "FADE":
        return ed.a, ed.b + int(round(C.FADE_RELEASE_S * SR))
    return ed.a, ed.b


def _frames(a: int, b: int, n: int) -> slice:
    return frame_slice(a / SR, b / SR, n)


def _pitch_range(fr, a: int, b: int) -> float | None:
    sl = _frames(a, b, len(fr))
    v = fr.S[sl][fr.voiced[sl]]
    return float(np.percentile(v, 90) - np.percentile(v, 10)) if v.size >= C.MIN_VOICED_WORD else None


def realised(ed: Edit, info: dict, rec: Recording, fy, span: tuple[int, int]) -> dict:
    """Signed change actually realised by the edit, measured on the edited clip (frame features `fy`) against the parent
    where an acoustic measure exists, analytically (exact) for durations."""
    t, (s, e) = ed.type, span
    if t in ("RUSH", "DRAG"):
        old, new = info.get("speech_old", 0), info.get("speech_new", 0)
        return {"name": "ln_speech_duration_ratio", "value": float(np.log(new / old)) if old and new else None, "unit": "ln"}
    if t == "PAUSE_DROPPED":
        return {"name": "pause_change", "value": -info["cut"] / SR, "unit": "s"}
    if t == "PAUSE_INTRUSIVE":
        return {"name": "pause_change", "value": info["inserted"] / SR, "unit": "s"}
    if t == "MONOTONE":
        before, after = _pitch_range(rec.fr, ed.a, ed.b), _pitch_range(fy, s, e)
        return {"name": "pitch_range_change", "value": None if before is None or after is None else after - before, "unit": "st"}
    if t == "FADE":
        before, after = rec.fr.L[_frames(ed.a, ed.b, len(rec.fr))].mean(), fy.L[_frames(s, e, len(fy))].mean()
        return {"name": "level_change", "value": float(after - before), "unit": "dB"}
    if t == "MUMBLE":
        before, after = rec.fr.Q[_frames(ed.a, ed.b, len(rec.fr))].mean(), fy.Q[_frames(s, e, len(fy))].mean()
        return {"name": "ln_mfcc_delta_ratio", "value": float(np.log((after + 1e-6) / (before + 1e-6))), "unit": "ln"}
    i = ed.words[0]  # DEEMPHASIS: change of the word's stress points p
    sl = _frames(s, e, len(fy))
    v = fy.S[sl][fy.voiced[sl]]
    dur = max((e - s) / SR, 1e-3)
    if v.size < C.MIN_VOICED_WORD:
        return {"name": "stress_points_change", "value": None, "unit": "p"}
    u = np.array([np.log(dur / rec.tr.syll[i]), np.percentile(v, 90), np.percentile(fy.E[sl], 90)])
    p_after = float(np.mean((u - rec.m) / rec.sigma))
    p_before = float(stress_points(rec.ws.u, rec.m, rec.sigma)[i])
    return {"name": "stress_points_change", "value": p_after - p_before, "unit": "p"}


def make_labels(clip_id: str, parent_id: str, rec: Recording, y: np.ndarray, chain: Chain, plan: Plan, infos: list[dict], *,
                recipe: str, seed: int, chain_name: str = "A") -> dict:
    """labels.json content: parent hash, recipe, seed, chain, word times carried through the time map, and per flaw the
    type, dimension, level, physical magnitude, signed realised change, expected secondary dimensions, word index span,
    half-open sample spans in the clip and in the parent, and the edit support."""
    fy = frame_features(y)
    flaws = []
    supports = []
    skipped = list(plan.skipped)
    for ed, info in zip(plan.edits, infos):
        if "skipped" in info:
            skipped.append({"type": ed.type, "level": ed.level, "reason": info["skipped"]})
            continue
        if "extra" in info:
            f = info["extra"]
            suffix = Chain()
            suffix.warps = chain.warps[info["suffix_start"]:]
            for name in ("span", "support"):
                a, b = f[name]
                f[name] = [round(float(suffix(a, "left"))), round(float(suffix(b, "right")))]
            for event in f["events"]:
                if event["kind"] == "silence":
                    point = event["parent_span"][0]
                    event["clip_span"] = [round(float(chain(point, "left"))), round(float(chain(point, "right")))]
                elif event["kind"] != "copy":
                    event["clip_span"] = list(chain.cur(*event["parent_span"]))
                else:
                    for name in ("clip_span", "pause_span"):
                        event[name] = list(suffix.cur(*event[name]))
            if not f["placebo"]:
                try:
                    f["realised"] = info["measure"](y, fy, chain)
                except EditError as exc:
                    f["realised"] = {**f["realised"], "value": None, "reason": str(exc)}
            f["duration_delta_samples"] = info["duration_delta_samples"]
            f["inserted_samples"] = sum(max(0, (ev["pause_span"][1] - ev["clip_span"][0]) if ev["kind"] == "copy" else
                                               ev["output_samples"] - (ev["parent_span"][1] - ev["parent_span"][0])) for ev in f["events"])
            f["removed_samples"] = sum(max(0, (ev["parent_span"][1] - ev["parent_span"][0]) - ev["output_samples"])
                                       for ev in f["events"] if ev["kind"] != "copy")
            supports += [tuple(v) for v in f["parent_supports"]]
            flaws.append(f)
            continue
        s_par, e_par = _support(ed, info, chain_name)
        supports.append((s_par, e_par))
        if ed.type == "PAUSE_INTRUSIVE":
            span = (int(round(float(chain(ed.a, "left")))), int(round(float(chain(ed.a, "right")))))
        else:
            span = chain.cur(ed.a, ed.b)
        sup = (int(round(float(chain(s_par, "right")))), int(round(float(chain(e_par, "left")))))
        name, unit = MAGNITUDE[ed.type]
        flaws.append({
            "type": ed.type, "dimension": C.FLAW_DIM[ed.type], "level": ed.level, "placebo": ed.param is None,
            "magnitude": {"name": name, "value": ed.param, "unit": unit},
            "realised": realised(ed, info, rec, fy, span),
            # Core labels keep the schema-3 values, so stored label bytes and GOLDEN_LABELS stay the same.
            "expected_secondary": list(C.as_dict(3)["EXPECTED_SECONDARY"][ed.type]),
            "event": ed.kind, "words": list(ed.words), "span": list(span), "parent_span": [ed.a, ed.b], "support": list(sup),
        })
    words, parent_words = word_maps(rec, chain)
    return {
        "clip": clip_id, "parent": {"id": parent_id, "sha256": audio.sha256_pcm(rec.wav)}, "sha256": audio.sha256_pcm(y),
        "recipe": recipe, "seed": seed, "chain": chain_name, "sr": SR, "n_samples": len(y),
        "words": words, "parent_words": parent_words,
        "flaws": flaws, "skipped": skipped,
        "outside_support_identical": outside_support_identical(rec.wav, y, chain, supports),
        "chain_warps": chain_warps(chain),
    }


def outside_support_identical(parent: np.ndarray, y: np.ndarray, chain: Chain, supports) -> bool:
    """True when every parent sample outside the supports reaches the clip unchanged through the time map."""
    outside = np.ones(len(parent), dtype=bool)
    for s_par, e_par in supports:
        outside[max(s_par, 0):max(e_par, 0)] = False
    mapped = np.rint(chain(np.arange(len(parent)), "right")).astype(np.int64)
    ok = outside & (mapped >= 0) & (mapped < len(y))
    return bool(np.array_equal(parent[ok], y[mapped[ok]]))


def word_maps(rec: Recording, chain: Chain) -> tuple[dict, dict]:
    """Word start and end samples in the clip (through the time map) and in the parent."""
    starts, ends = np.round(rec.al.start * SR), np.round(rec.al.end * SR)
    clip = {"start": [int(round(float(chain(v, "right")))) for v in starts], "end": [int(round(float(chain(v, "left")))) for v in ends]}
    return clip, {"start": [int(v) for v in starts], "end": [int(v) for v in ends]}


def chain_warps(chain: Chain) -> list[dict]:
    return [{"src": w.src.tolist(), "dst": w.dst.tolist()} for w in chain.warps]


def inject(rec: Recording, plan: Plan, clip_id: str, parent_id: str, *, recipe: str, seed: int, chain_name: str = "A") -> tuple[np.ndarray, dict]:
    """Apply a plan to a recording and return (clip, labels)."""
    y, chain, infos = apply_edits(rec, plan.edits, chain_name)
    return y, make_labels(clip_id, parent_id, rec, y, chain, plan, infos, recipe=recipe, seed=seed, chain_name=chain_name)


def identity_plan(rec: Recording, seed: int) -> Plan:
    """Placebo / identity plan: every recipe run with null parameters over 5-word spans (no coverage cap)."""
    return plan_clip(rec, [(t, None) for t in C.CORE8_TYPES], seed, cap=None, null_width=True)


def placebo_clip(rec: Recording, parent_id: str, k: int) -> tuple[np.ndarray, dict]:
    """Placebo seed k of a recording (generated on the fly in calibration and evaluation, not stored)."""
    cid = f"{parent_id}__placebo{k}"
    seed = clip_seed(cid)
    return inject(rec, identity_plan(rec, seed), cid, parent_id, recipe="placebo", seed=seed)


EXTRA_WINDOWED = ("NATURAL_RUSH", "WORD_BY_WORD", "UNEVEN_TEMPO", "LOW_EFFORT")


def extra_candidates(rec, ref, typ, width, taken):
    from .edits_extra import FUNCTION_WORDS, continuant_span, gap_point, onset_burst
    tr, gap = rec.tr, C.EDIT_GAP_WORDS
    def free(a, b):
        return all(b + gap < c or a - gap > d for c, d in taken)

    def content(i):
        return tr.norm[i] not in FUNCTION_WORDS

    def voiced(i):
        return rec.fr.voiced[frame_slice(rec.al.start[i], rec.al.end[i], len(rec.fr))].sum() >= C.MIN_VOICED_WORD

    stressed = shared_stress(rec, ref)
    if typ in EXTRA_WINDOWED:
        out = [(i, i + width - 1) for i in range(len(tr) - width + 1)
               if free(i, i + width - 1) and tr.sentence[i] == tr.sentence[i + width - 1]
               and all(rec.al.end[w] - rec.al.start[w] >= C.XFADE_S * max(C.RUSH_RATE) for w in range(i, i + width))]
        if typ == "NATURAL_RUSH":
            out = [(a, b) for a, b in out if any(rec.sil[a:b] > 0)]
        if typ == "WORD_BY_WORD":
            def gaps(pos):
                try:
                    for i in range(pos[0], pos[1]):
                        gap_point(rec, i)
                    return True
                except EditError:
                    return False
            out = [pos for pos in out if gaps(pos)]
        if typ == "LOW_EFFORT":
            out = [(a, b) for a, b in out if any(voiced(i) for i in range(a, b + 1))]
        return out
    if typ in ("TRAILING_OFF", "RISING_ENDING", "FLAT_FINAL_FALL", "REPEATED_CONTOUR"):
        sentences = [tr.sentence_words(s) for s in range(tr.n_sentences)]
        full = [(a, b) for a, b in sentences if tr.punct[b] == "." and any(voiced(i) for i in range(a, b + 1))]
        if typ == "REPEATED_CONTOUR":
            full = [(a, b) for a, b in full if rec.al.end[b] - rec.al.start[a] >= C.EXTRA_SENTENCE_MIN_S]
            return [(a, b) for a, b in full if free(a, b) and any((c, d) != (a, b) for c, d in full)]
        if typ == "TRAILING_OFF":
            return [(max(a, b - C.TRAIL_WORDS + 1), b) for a, b in full if free(max(a, b - C.TRAIL_WORDS + 1), b)]
        return [(b, b) for a, b in full if free(b, b) and voiced(b) and
                rec.fr.voiced[frame_slice(max(rec.al.start[b], rec.al.end[b] - C.ENDING_WINDOW_S), rec.al.end[b], len(rec.fr))].sum() >= C.MIN_VOICED_WORD
                and (typ != "FLAT_FINAL_FALL" or (a < b and voiced(b - 1)))]
    if typ == "MISPLACED_EMPHASIS":
        return sorted({(min(i, j), max(i, j)) for j in stressed if content(j) and voiced(j)
                       for i in range(len(tr)) if not content(i) and voiced(i) and tr.sentence[i] == tr.sentence[j]
                       and abs(i - j) <= C.EDIT_GAP_WORDS and free(min(i, j), max(i, j))})
    out = []
    for i in range(len(tr)):
        if not free(i, i):
            continue
        good = not content(i) if typ == "WORD_REPETITION" else content(i)
        if not good:
            continue
        try:
            if typ in ("ONSET_PROLONGATION", "RHYME_PROLONGATION"):
                continuant_span(rec, i, typ == "ONSET_PROLONGATION")
            if typ == "RHYME_PROLONGATION" and i < len(tr) - 1 and rec.al.start[i + 1] - rec.al.end[i] < C.INSERT_MIN_GAP_S:
                continue
            if typ == "BLOCK":
                onset_burst(rec, i)
            if typ == "HESITATION":
                gap_point(rec, i - 1)
        except EditError:
            continue
        out.append((i, i))
    if typ in STRESS_FALLBACK_TYPES:
        shared = [pos for pos in out if pos[0] in stressed]
        own = [pos for pos in out if pos[0] in stress_set(rec)]
        return shared or own or out
    return out


def render_extra(rec, ed, measurements=None):
    from . import edits_extra as E
    a, b = ed.words
    typ, lv = ed.type, ed.level
    if typ in EXTRA_WINDOWED:
        fn = {"NATURAL_RUSH": E.natural_rushing, "WORD_BY_WORD": E.word_by_word_reading,
              "UNEVEN_TEMPO": E.uneven_tempo, "LOW_EFFORT": E.low_vocal_effort}[typ]
        return fn(rec, (a, b), lv, measurements=measurements, **({"seed": clip_seed(f"tempo:{audio.sha256_pcm(rec.wav)}:{a}:{b}")} if typ == "UNEVEN_TEMPO" else {}))
    if typ == "MISPLACED_EMPHASIS":
        candidates = [(i, j) for i in (a, b) for j in (a, b)
                      if rec.tr.norm[i] in E.FUNCTION_WORDS and rec.tr.norm[j] not in E.FUNCTION_WORDS]
        if not candidates:
            raise EditError("no stressed content/function pair")
        return E.misplaced_emphasis(rec, *candidates[0], lv, measurements=measurements)
    sentence = rec.tr.sentence[b]
    if typ == "REPEATED_CONTOUR":
        templates = [s for s in range(rec.tr.n_sentences) if s != sentence and rec.tr.punct[rec.tr.sentence_words(s)[1]] == "."
                     and rec.al.end[rec.tr.sentence_words(s)[1]] - rec.al.start[rec.tr.sentence_words(s)[0]] >= C.EXTRA_SENTENCE_MIN_S
                     and rec.fr.voiced[frame_slice(rec.al.start[rec.tr.sentence_words(s)[0]],
                                                  rec.al.end[rec.tr.sentence_words(s)[1]], len(rec.fr))].sum() >= C.MIN_VOICED_WORD]
        if not templates:
            raise EditError("no voiced template sentence")
        return E.repeated_contour(rec, templates[0], lv, target_sentences=[sentence], measurements=measurements)
    if typ in ("TRAILING_OFF", "RISING_ENDING", "FLAT_FINAL_FALL"):
        fn = {"TRAILING_OFF": E.trailing_off, "RISING_ENDING": E.rising_ending, "FLAT_FINAL_FALL": E.flattened_final_fall}[typ]
        return fn(rec, sentence, lv, measurements=measurements)
    fn = {"HESITATION": E.hesitation_before_word, "WORD_REPETITION": E.word_repetition,
          "SOUND_REPETITION": E.sound_repetition, "RHYME_PROLONGATION": E.rhyme_prolongation,
          "ONSET_PROLONGATION": E.onset_prolongation, "BLOCK": E.block_before_release}[typ]
    y, chain, lab = fn(rec, a, lv, measurements=measurements)
    f = lab["flaws"][0]
    if not f["approximation"]:
        f["approximation"] = {"method": "aligned content-word prior" if typ == "HESITATION" else "function-word prior; copied waveform"}
    if ed.selection is not None:
        f["approximation"]["stress_fallback"] = ed.selection
    if typ in STRESS_FALLBACK_TYPES:
        f["approximation"]["selection"] = "shared stress preferred, own stress then eligible content fallback; signal eligibility"
        f["approximation"]["own_stressed"] = a in stress_set(rec)
    return y, chain, lab
