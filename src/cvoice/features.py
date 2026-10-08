"""Frame features (energy, two-pass Praat F0, semitones, MFCC delta), word statistics, stress points.

Frame k is centred on sample k * HOP (400-sample symmetric Hann, hop 160, FFT 512), so frame times are k * 0.01 s.
Energy E and pitch S are gain- and register-invariant by construction (recording-relative).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import scipy.fft
from scipy import ndimage, signal

from . import config as C
from .align import Alignment, Transcript, acoustic_pauses, frame_index, pause_threshold

# Frames per batch: the batch size bounds the temporary arrays of the frame-level DSP.
LEVEL_BATCH_FRAMES = 8192
MFCC_BATCH_FRAMES = 4096


# ============================================================================================ frame level
def frames(x: np.ndarray) -> np.ndarray:
    """Centred frames as a view: [n_frames, WIN]; n_frames = 1 + len(x) // HOP; zero padded at the edges."""
    n = 1 + len(x) // C.HOP
    xp = np.concatenate([np.zeros(C.WIN // 2), x, np.zeros(C.WIN // 2 + C.HOP)])
    return np.lib.stride_tricks.sliding_window_view(xp, C.WIN)[::C.HOP][:n]


def frame_level_db(x: np.ndarray) -> np.ndarray:
    """L = 10 log10(sum(w x^2) / sum(w) + 1e-12) per frame, dB re full scale."""
    w = np.hanning(C.WIN)
    fr = frames(x)
    out = np.empty(len(fr))
    for i in range(0, len(fr), LEVEL_BATCH_FRAMES):
        b = fr[i:i + LEVEL_BATCH_FRAMES]
        out[i:i + LEVEL_BATCH_FRAMES] = (b * b * w).sum(1) / w.sum()
    return 10.0 * np.log10(out + C.LEVEL_EPS)


def runs(mask: np.ndarray) -> list[tuple[int, int]]:
    d = np.diff(np.r_[0, np.asarray(mask, np.int8), 0])
    return list(zip(np.flatnonzero(d == 1).tolist(), np.flatnonzero(d == -1).tolist()))


def _praat_f0(x: np.ndarray, floor: float, ceil: float) -> np.ndarray:
    """Praat autocorrelation F0 mapped to the 10 ms frame grid (nearest, ties earlier; > 10 ms away = unvoiced)."""
    import parselmouth
    snd = parselmouth.Sound(np.ascontiguousarray(x, dtype=np.float64), sampling_frequency=C.SR)
    p = snd.to_pitch_ac(time_step=C.HOP_S, pitch_floor=float(floor), pitch_ceiling=float(ceil), **C.PRAAT_AC)
    ts, vs = np.asarray(p.xs(), float), np.nan_to_num(np.asarray(p.selected_array["frequency"], float), nan=0.0)
    tg = np.arange(1 + len(x) // C.HOP) * C.HOP_S
    if len(ts) < 2:
        return np.zeros(len(tg))
    idx = np.clip(np.searchsorted(ts, tg), 1, len(ts) - 1)
    idx = np.where(np.abs(tg - ts[idx - 1]) <= np.abs(ts[idx] - tg), idx - 1, idx)
    out = vs[idx].copy()
    out[np.abs(ts[idx] - tg) > C.HOP_S] = 0.0
    return out


def pitch_track(x: np.ndarray) -> tuple[np.ndarray, bool]:
    """Two-pass Praat F0 (Hz, 0 = unvoiced) with a 5-frame median inside voiced runs. Returns (f0, fallback_used).
    Pass 1 uses 60-700 Hz; pass 2 floor max(50, 0.75 Q25), ceiling min(800, 1.5 Q75)."""
    first = _praat_f0(x, *C.F0_PASS1)
    v = first[first > 0]
    fallback = v.size < C.F0_MIN_FIRST_PASS
    if fallback:
        lo, hi = C.F0_FALLBACK
    else:
        q25, q75 = np.percentile(v, [25, 75])
        lo, hi = max(C.F0_FLOOR_MIN, C.F0_FLOOR_Q25_FACTOR * q25), min(C.F0_CEIL_MAX, C.F0_CEIL_Q75_FACTOR * q75)
    f0 = _praat_f0(x, lo, hi)
    out = f0.copy()
    for a, b in runs(f0 > 0):
        out[a:b] = ndimage.median_filter(f0[a:b], size=C.F0_MEDIAN_FRAMES, mode="nearest")
    return out, fallback


def _mel_filterbank() -> np.ndarray:
    mel = lambda f: 2595.0 * np.log10(1.0 + f / 700.0)
    imel = lambda m: 700.0 * (10.0 ** (m / 2595.0) - 1.0)
    pts = imel(np.linspace(mel(C.MEL_FMIN), mel(C.MEL_FMAX), C.N_MEL + 2))
    f = np.fft.rfftfreq(C.NFFT, 1.0 / C.SR)
    fb = np.zeros((C.N_MEL, len(f)))
    for i in range(C.N_MEL):
        lo, c, hi = pts[i:i + 3]
        fb[i] = np.clip(np.minimum((f - lo) / (c - lo), (hi - f) / (hi - c)), 0.0, None)
    return fb


_MELFB = _mel_filterbank()


def mfcc_delta_magnitude(x: np.ndarray) -> np.ndarray:
    """Q = ||delta c1..c12||_2 per frame (c0..c12 from 40 mel filters 50-7600 Hz, orthonormal DCT-II; delta over +-2)."""
    fr, w = frames(x), np.hanning(C.WIN)
    ceps = np.empty((len(fr), C.N_CEPS))
    for i in range(0, len(fr), MFCC_BATCH_FRAMES):
        power = np.abs(np.fft.rfft(fr[i:i + MFCC_BATCH_FRAMES] * w, C.NFFT, axis=1)) ** 2
        ceps[i:i + MFCC_BATCH_FRAMES] = scipy.fft.dct(np.log(power @ _MELFB.T + C.MEL_LOG_EPS), type=2, norm="ortho", axis=1)[:, :C.N_CEPS]
    n = C.DELTA_HALF_WIDTH
    cp = np.pad(ceps, ((n, n), (0, 0)), mode="edge")
    num = sum(k * (cp[n + k:len(ceps) + n + k] - cp[n - k:len(ceps) + n - k]) for k in range(1, n + 1))
    delta = num / (2.0 * sum(k * k for k in range(1, n + 1)))
    return np.linalg.norm(delta[:, 1:], axis=1)


@dataclass
class Frames:
    """Frame series on the 10 ms grid (length n). E = L - median of L over voiced frames; S in semitones re the
    recording's median voiced F0 (NaN where unvoiced); Q = MFCC delta magnitude."""
    L: np.ndarray
    E: np.ndarray
    f0: np.ndarray
    voiced: np.ndarray
    S: np.ndarray
    Q: np.ndarray
    f0_fallback: bool

    def __len__(self) -> int:
        return len(self.L)


def frame_features(x: np.ndarray) -> Frames:
    L = frame_level_db(x)
    f0, fallback = pitch_track(x)
    voiced = f0 > 0
    ref = voiced if voiced.sum() >= C.MIN_VOICED_REF else np.ones(len(L), dtype=bool)
    S = np.full(len(L), np.nan)
    if voiced.any():
        S[voiced] = 12.0 * np.log2(f0[voiced] / np.median(f0[voiced]))
    return Frames(L, L - np.median(L[ref]), f0, voiced, S, mfcc_delta_magnitude(x), fallback)


# ============================================================================================ word statistics
def word_regions(al: Alignment) -> np.ndarray:
    """Word support [n, 2] (s) from raw CTC spans: a short gap is split at its midpoint, a longer gap is entered by
    at most REGION_MAX_EXT_S (raw spans are narrow spikes)."""
    n = len(al)
    out = np.empty((n, 2))
    for i in range(n):
        gp = al.start[i] - al.end[i - 1] if i else np.inf
        gn = al.start[i + 1] - al.end[i] if i + 1 < n else np.inf
        out[i, 0] = max(al.start[i] - (gp / 2 if gp < C.REGION_SHARE_BELOW_S else C.REGION_MAX_EXT_S), 0.0)
        out[i, 1] = al.end[i] + (gn / 2 if gn < C.REGION_SHARE_BELOW_S else C.REGION_MAX_EXT_S)
    return out


def frame_slice(a: float, b: float, n: int) -> slice:
    """Frames whose centres lie in [a, b); at least one frame (the nearest)."""
    k0 = frame_index(a)
    k1 = frame_index(b)
    if k1 <= k0:
        k0 = min(max(int(round(a / C.HOP_S)), 0), n - 1)
        k1 = k0 + 1
    return slice(min(k0, n - 1), min(k1, n))


@dataclass
class WordStats:
    """Per-word statistics (NaN = unavailable). u = (ln(duration / syllables), P90 S, P90 E)."""
    dur: np.ndarray
    med_s: np.ndarray
    p90_s: np.ndarray
    p90_e: np.ndarray
    mean_q: np.ndarray
    u: np.ndarray


def word_stats(fr: Frames, regions: np.ndarray, syll: tuple[int, ...]) -> WordStats:
    n = len(regions)
    dur = regions[:, 1] - regions[:, 0]
    med_s, p90_s, p90_e, mean_q = (np.full(n, np.nan) for _ in range(4))
    for i, (a, b) in enumerate(regions):
        sl = frame_slice(a, b, len(fr))
        s = fr.S[sl][fr.voiced[sl]]
        if s.size >= C.MIN_VOICED_WORD:
            med_s[i], p90_s[i] = np.median(s), np.percentile(s, 90)
        p90_e[i] = np.percentile(fr.E[sl], 90)
        mean_q[i] = fr.Q[sl].mean()
    u = np.column_stack([np.log(np.maximum(dur, 1e-3) / np.asarray(syll)), p90_s, p90_e])
    return WordStats(dur, med_s, p90_s, p90_e, mean_q, u)


def stress_reference(u: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(m, sigma): the recording's own medians and robust scales of u, scales floored at STRESS_SIGMA_FLOOR."""
    ok = np.isfinite(u).all(axis=1)
    if ok.sum() < 3:
        return np.full(3, np.nan), np.asarray(C.STRESS_SIGMA_FLOOR)
    m = np.median(u[ok], axis=0)
    return m, np.maximum(C.MAD_SCALE * np.median(np.abs(u[ok] - m), axis=0), C.STRESS_SIGMA_FLOOR)


def stress_points(u: np.ndarray, m: np.ndarray, sigma: np.ndarray) -> np.ndarray:
    """p = mean over the three components of (u - m) / sigma (NaN where a component is missing)."""
    return np.where(np.isfinite(u).all(axis=1), ((u - m) / sigma).mean(axis=1), np.nan)


def stress_words(p: np.ndarray) -> list[int]:
    """Indices with p >= STRESS_P_MIN that are a local maximum over +-1 word (ties: earlier word wins)."""
    out = []
    for i in range(len(p)):
        if not np.isfinite(p[i]) or p[i] < C.STRESS_P_MIN:
            continue
        if all(not np.isfinite(p[j]) or p[i] > p[j] or (p[i] == p[j] and i < j)
               for j in (i - 1, i + 1) if 0 <= j < len(p)):
            out.append(i)
    return out


# ============================================================================================ recording
def windows(tr: Transcript) -> list[tuple[int, int] | None]:
    """Five-word centred window per word (inclusive word indices), clipped at sentence boundaries; None when fewer
    than WINDOW_MIN_WORDS words remain."""
    half = C.WINDOW_WORDS // 2
    first: dict[int, int] = {}
    last: dict[int, int] = {}
    for i, s in enumerate(tr.sentence):
        first.setdefault(s, i)
        last[s] = i
    out: list[tuple[int, int] | None] = []
    for i, s in enumerate(tr.sentence):
        lo, hi = max(i - half, first[s]), min(i + half, last[s])
        out.append((lo, hi) if hi - lo + 1 >= C.WINDOW_MIN_WORDS else None)
    return out


@dataclass
class Recording:
    """One analysed recording: audio, transcript, alignment, frame features, word statistics, pauses, and the
    per-window quantities (NaN where the window is missing):
    win_T speech time without pauses (s), win_R P90-P10 of S (st), win_E mean E (dB) and win_Q mean Q over the
    frames outside acoustic pauses, win_W sum of the aligned word durations (s)."""
    wav: np.ndarray
    tr: Transcript
    al: Alignment
    fr: Frames
    regions: np.ndarray
    ws: WordStats
    sil: np.ndarray  # s, acoustic pause after word i (n - 1)
    sil_span: np.ndarray  # (n - 1, 2) s, start / end of that pause (NaN where none)
    sil_raw: np.ndarray  # s, longest silent run in the gap after word i without the PAUSE_MIN_S cut
    m: np.ndarray  # own medians of u
    sigma: np.ndarray  # own robust scales of u
    win: list
    win_T: np.ndarray
    win_R: np.ndarray
    win_E: np.ndarray
    win_Q: np.ndarray
    win_W: np.ndarray

    occ: np.ndarray | None = None
    orphan_spans: np.ndarray | None = None
    word_silence_spans: np.ndarray | None = None
    stable_spans: np.ndarray | None = None
    inserted: list[dict] = field(default_factory=list)
    alpha_word: np.ndarray | None = None
    final_df0: np.ndarray | None = None

    @property
    def duration(self) -> float:
        return len(self.wav) / C.SR


def make_recording(wav: np.ndarray, tr: Transcript, al: Alignment) -> Recording:
    fr = frame_features(wav)
    regions = word_regions(al)
    ws = word_stats(fr, regions, tr.syll)
    m, sigma = stress_reference(ws.u)
    sil, sil_span, sil_raw = acoustic_pauses(al, fr.L, fr.voiced)
    win = windows(tr)
    n = len(tr)
    T, R, E, Q = (np.full(n, np.nan) for _ in range(4))
    speech = np.ones(len(fr), dtype=bool)  # frames outside acoustic pauses: a pause is not a quiet or unclear word
    for a, b in sil_span[np.isfinite(sil_span[:, 0])]:
        speech[frame_slice(a, b, len(fr))] = False
    for i, w in enumerate(win):
        if w is None:
            continue
        lo, hi = w
        T[i] = speech_time({'start': al.start[lo:hi+1], 'end': al.end[lo:hi+1], 'sil': sil[lo:hi]})
        sl = frame_slice(regions[lo, 0], regions[hi, 1], len(fr))
        v = fr.S[sl][fr.voiced[sl]]
        if v.size >= C.D3_MIN_VOICED_FRAMES:
            R[i] = np.percentile(v, 90) - np.percentile(v, 10)
        k = speech[sl] if speech[sl].any() else np.ones(len(fr.E[sl]), dtype=bool)
        E[i], Q[i] = fr.E[sl][k].mean(), fr.Q[sl][k].mean()
    rec = Recording(wav, tr, al, fr, regions, ws, sil, sil_span, sil_raw, m, sigma, win, T, R, E, Q, window_word_time(al.start, al.end, win))
    edits = decode_edits(tr.norm, al.decoded)
    x = compact_features(rec, al.decoded, np.diff(al.char_spans, axis=1).ravel(), [c for w in tr.norm for c in w], edits)
    rec.orphan_spans, rec.word_silence_spans, rec.stable_spans = x['orphan_spans'], x['word_silence_spans'], x['stable_spans']
    rec.inserted = edits[0]
    rec.alpha_word = x['alpha']
    rec.final_df0 = final_pitch_word(rec)
    rec.occ = word_occupancy(rec)
    return rec


def orphan_voiced_spans(rec):
    """Silence-bounded voiced runs wholly inside inter-word gaps, seconds."""
    if rec.fr is None:
        return np.empty((0, 2))
    spans = []
    for start, end in runs(rec.fr.voiced):
        a, b = start * C.HOP_S, end * C.HOP_S
        i = int(np.searchsorted(rec.regions[:, 0], b, side='right'))
        if 0 < i < len(rec.regions) and a > rec.regions[i - 1, 1] and b < rec.regions[i, 0] and (end - start) * C.HOP_S >= C.ORPHAN_MIN_S:
            spans.append((a, b))
    return np.array(spans).reshape(-1, 2)


def word_occupancy(rec):
    """Aligned word duration plus isolated orphan voiced time in its preceding gap, seconds."""
    occ = rec.al.end - rec.al.start
    for a, b in orphan_voiced_spans(rec):
        i = int(np.searchsorted(rec.regions[:, 0], b))
        occ[i] += b - a
    return occ


def window_word_time(start, end, win) -> np.ndarray:
    """Sum of the aligned word durations (s) of each five-word window; no gap between words is counted."""
    duration = np.asarray(end, float) - np.asarray(start, float)
    return np.array([duration[w[0]:w[1] + 1].sum() if w is not None else np.nan for w in win])


def speech_time(x) -> float:
    """Speech time in s: the aligned span minus the pauses, at least 1 ms."""
    return max(x['end'][-1] - x['start'][0] - np.sum(x['sil']), 1e-3)


def speech_time_ratio(x, b=None):
    """docs/research/chain/pace_pauses/REPORT.md §4 #2: ln participant/reference speech time. Without b, the speech time
    of x in s."""
    v = speech_time(x)
    return v if b is None else np.log(v / speech_time(b))


def finite(a):
    a = np.asarray(a, float).ravel()
    return a[np.isfinite(a)]


def mean(a):
    a = finite(a)
    return float(a.mean()) if len(a) else np.nan


def median(a):
    a = finite(a)
    return float(np.median(a)) if len(a) else np.nan


def slope(t, v):
    t, v = np.asarray(t), np.asarray(v)
    ok = np.isfinite(t) & np.isfinite(v)
    if ok.sum() < 3 or np.ptp(t[ok]) < 1e-6:
        return np.nan
    return float(np.polyfit(t[ok] - t[ok].mean(), v[ok], 1)[0])


def decode_edits(prompt, decoded):
    """docs/research/chain/disfluency/REPORT.md §2.6 M2: minimum word edit alignment; choose match/substitution before deletion/insertion ties."""
    a, z = list(prompt), [w['norm'] for w in decoded]
    d = np.zeros((len(a) + 1, len(z) + 1), np.int32)
    d[:, 0], d[0, :] = np.arange(len(a) + 1), np.arange(len(z) + 1)
    for i in range(1, len(a) + 1):
        for j in range(1, len(z) + 1):
            d[i, j] = min(d[i - 1, j - 1] + (a[i - 1] != z[j - 1]), d[i - 1, j] + 1, d[i, j - 1] + 1)
    ins, errors, i, j = [], np.zeros(len(a)), len(a), len(z)
    while i or j:
        if i and j and d[i, j] == d[i - 1, j - 1] + (a[i - 1] != z[j - 1]):
            errors[i - 1] = a[i - 1] != z[j - 1]
            i, j = i - 1, j - 1
        elif i and d[i, j] == d[i - 1, j] + 1:
            errors[i - 1] = 1
            i -= 1
        else:
            ins.append({**decoded[j - 1], 'prompt_index': i})
            j -= 1
    return ins[::-1], errors


def recording_arrays(r):
    return dict(norm=np.asarray(r.tr.norm), disp=np.asarray(r.tr.disp), punct=np.array([bool(p) for p in r.tr.punct]),
                punctuation=np.asarray(r.tr.punct), sentence=np.asarray(r.tr.sentence), syll=np.asarray(r.tr.syll),
                start=r.al.start, end=r.al.end, compat=r.al.compat, regions=r.regions, u=r.ws.u,
                ws_dur=r.ws.dur, med_s=r.ws.med_s, p90_s=r.ws.p90_s, p90_e=r.ws.p90_e, mean_q=r.ws.mean_q,
                m=r.m, sigma=r.sigma, sil=r.sil, sil_raw=r.sil_raw, sil_span=r.sil_span,
                win_T=r.win_T, win_R=r.win_R, win_E=r.win_E, win_Q=r.win_Q,
                win=np.array([w if w is not None else (-1,-1) for w in r.win]), duration=r.duration)


def spectral_arrays(rec):
    """docs/research/chain/volume_clarity/REPORT.md §§2.1/2.4: batched spectra; F0-driven Butterworth power response implements the stated filter."""
    fr = frames(rec.wav)
    freq = np.fft.rfftfreq(C.NFFT, 1 / C.SR)
    alpha, emph, share = (np.full(len(fr), np.nan) for _ in range(3))
    centers = C.ENVELOPE_BASE_HZ * 2 ** (np.arange(C.ENVELOPE_BANDS) / C.ENVELOPE_BANDS_PER_OCTAVE)
    bands = np.empty((len(fr), len(centers)))
    stability = np.empty((len(fr), C.STABLE_BANDS))
    w = np.hanning(C.WIN)
    for a in range(0, len(fr), C.SPECTRAL_BATCH):
        z = min(a + C.SPECTRAL_BATCH, len(fr))
        p = np.abs(np.fft.rfft(fr[a:z] * w, C.NFFT, axis=1)) ** 2
        energy = p.sum(1) + C.LEVEL_EPS
        alpha[a:z] = 10 * np.log10((p[:, (freq >= C.ALPHA_HIGH_HZ[0]) & (freq <= C.ALPHA_HIGH_HZ[1])].sum(1) + 1e-12)
                                  / (p[:, (freq >= C.ALPHA_LOW_HZ[0]) & (freq < C.ALPHA_LOW_HZ[1])].sum(1) + 1e-12))
        share[a:z] = p[:, (freq >= C.MID_SHARE_HZ[0]) & (freq <= C.MID_SHARE_HZ[1])].sum(1) / energy
        cutoff = np.clip(C.EMPH_CUTOFF_F0 * rec.fr.f0[a:z], *C.EMPH_CUTOFF_HZ)
        # Bilinear-transform magnitude of a fourth-order digital Butterworth, -3 dB at cutoff.
        ratio = np.tan(np.pi * freq / C.SR)[None] / np.tan(np.pi * cutoff / C.SR)[:, None]
        gain2 = 1 / (1 + ratio ** (2 * C.EMPH_FILTER_ORDER))
        emph[a:z] = 10 * np.log10(energy / ((p * gain2).sum(1) + 1e-12))
        for j, c in enumerate(centers):
            bands[a:z, j] = np.sqrt(p[:, (freq >= c / 2 ** (1 / (2 * C.ENVELOPE_BANDS_PER_OCTAVE))) & (freq < c * 2 ** (1 / (2 * C.ENVELOPE_BANDS_PER_OCTAVE)))].sum(1))
        for j in range(C.STABLE_BANDS):
            stability[a:z, j] = np.sqrt(p[:, (freq >= j * C.STABLE_BAND_HZ) & (freq < (j + 1) * C.STABLE_BAND_HZ)].sum(1)) / np.sqrt(energy)
    emph[~rec.fr.voiced] = np.nan
    return alpha, emph, share, bands, stability


def window_stability(values, width):
    out = np.full(len(values), np.nan)
    if len(values) < width:
        return out
    blocks = np.lib.stride_tricks.sliding_window_view(values, width, axis=0)
    t = np.arange(width) - (width-1)/2
    fitted_slope = np.sum(blocks*t,axis=-1) / np.sum(t*t)
    residual = blocks - blocks.mean(axis=-1,keepdims=True) - fitted_slope[...,None]*t
    score = np.abs(fitted_slope) + np.sqrt(np.mean(residual**2,axis=-1))
    centre = (width - 1) // 2
    out[centre:centre + len(score)] = score if score.ndim==1 else score.mean(axis=1)
    return out


def insertion_form(word: dict, prompt) -> str:
    """'copy_or_prefix' when the inserted word is a prefix of a prompt word near its insertion point, else 'added_material'."""
    index = word['prompt_index']
    near = prompt[max(0, index - C.INSERTION_CONTEXT_WORDS):index + C.INSERTION_CONTEXT_WORDS]
    return 'copy_or_prefix' if any(n.startswith(word['norm']) for n in near) else 'added_material'


def compact_features(rec, decoded, char_duration, chars, edits=None):
    """One Recording to reusable arrays; derived measures share DSP, all event coordinates retain clip origin.
    edits: decode_edits(rec.tr.norm, decoded) when the caller has it already."""
    x = recording_arrays(rec)
    alpha, emph, share, bands, spectrum = spectral_arrays(rec)
    threshold = pause_threshold(rec.fr.L)
    silent = (rec.fr.L < threshold) & ~rec.fr.voiced
    x['silence_share'] = float(silent.mean())
    x['pitch_level'] = median(rec.fr.f0[rec.fr.voiced])
    x['pitch_span'] = float(np.ptp(np.percentile(finite(rec.fr.S), [10, 90]))) if rec.fr.voiced.any() else np.nan
    x['latency'] = np.r_[0., rec.sil_raw]
    x['production'] = rec.al.end - rec.al.start
    x['char_duration'], x['chars'] = np.asarray(char_duration), np.asarray(chars)
    x['prominence'] = stress_points(rec.ws.u, rec.m, rec.sigma)
    ins, errors = edits if edits is not None else decode_edits(rec.tr.norm, decoded)
    x['decode_errors'], x['insertions_per100'] = errors, 100 * len(ins) / len(rec.tr)
    x['inserted_spans'] = np.array([[w['start'], w['end']] for w in ins]).reshape(-1, 2)
    x['insertion_forms'] = [insertion_form(w, rec.tr.norm) for w in ins]
    x['orphan_spans'] = orphan_voiced_spans(rec)
    x['orphan_seconds'] = np.sum(np.diff(x['orphan_spans'], axis=1))
    # Goto's window lengths; amplitude envelope extraction/scales are not specified well enough to transfer P_fp constants.
    pitch_stability = window_stability(rec.fr.S, C.STABLE_PITCH_FRAMES)
    spectrum_stability = window_stability(spectrum, C.STABLE_SPECTRUM_FRAMES)
    stable = rec.fr.voiced & (rec.fr.f0 < median(rec.fr.f0[rec.fr.voiced])) & (pitch_stability <= C.STABLE_PITCH_ST) & (spectrum_stability <= C.STABLE_SPECTRUM)
    x['stable_spans'] = np.array([[a*C.HOP_S, z*C.HOP_S] for a,z in runs(stable) if (z-a)*C.HOP_S >= C.STABLE_S]).reshape(-1, 2)
    x['stable_seconds'] = np.sum(np.diff(x['stable_spans'], axis=1))
    word_silence, block_spans = [], []
    for s,e in zip(rec.al.start,rec.al.end):
        sl = frame_slice(s,e,len(rec.fr))
        spans = [(a+sl.start,z+sl.start) for a,z in runs(silent[sl])]
        word_silence.append(max([0.] + [(z-a)*C.HOP_S for a,z in spans]))
        block_spans.extend([(a*C.HOP_S,z*C.HOP_S) for a,z in spans])
    x['word_silence'] = np.array(word_silence)
    x['word_silence_spans'] = np.array(block_spans).reshape(-1,2)
    word_f0, av, ev, mv, env = [], [], [], [], []
    for a, z in rec.regions:
        sl = frame_slice(a, z, len(rec.fr))
        word_f0.append(mean(rec.fr.f0[sl][rec.fr.voiced[sl]]))
        av.append(mean(alpha[sl][rec.fr.voiced[sl]])); ev.append(mean(emph[sl]))
        mv.append(mean(share[sl][rec.fr.L[sl] >= threshold]))
        env.append(np.array([np.interp(np.linspace(0, 1, C.CONTOUR_POINTS), np.linspace(0, 1, len(b)), b)
                             for b in bands[sl].T]))
    x.update(alpha_relative=np.array(av)-median(av), word_f0=np.array(word_f0), alpha=np.array(av), spectral_emphasis=np.array(ev),
             mid_share=np.array(mv), band_envelopes=np.array(env))
    envelope = np.sqrt(10 ** (rec.fr.L / 10))
    if len(envelope) >= C.MODULATION_MIN_FRAMES:
        sos = signal.butter(C.MODULATION_ORDER, C.MODULATION_HZ, btype='bandpass', fs=1/C.HOP_S, output='sos')
        x['modulation_depth'] = np.sqrt(np.mean(signal.sosfilt(sos, envelope)**2)) / max(envelope.mean(),1e-12)
    else:
        x['modulation_depth'] = np.nan
    final, decl, contours, slopes, drops = [], [], [], [], []
    ending = final_pitch_word(rec, min_voiced=1)
    final_words = sentence_final(rec.tr)
    ends = np.flatnonzero(x['punct'])
    if not len(ends) or ends[-1] != len(rec.tr)-1:
        ends = np.r_[ends, len(rec.tr)-1]
    first = 0
    for last in ends:
        sl = frame_slice(rec.al.start[first], rec.al.end[last], len(rec.fr))
        voiced = rec.fr.voiced[sl]
        tt = np.arange(len(rec.fr))[sl] * C.HOP_S
        slopes.append(slope(tt[voiced], rec.fr.L[sl][voiced]))
        lw = frame_slice(*rec.regions[last], len(rec.fr))
        drops.append(mean(rec.fr.L[lw][rec.fr.voiced[lw]]) - median(rec.fr.L[sl][voiced]))
        first = last + 1
    for s in range(rec.tr.n_sentences):
        a,z = rec.tr.sentence_words(s)
        sl = frame_slice(rec.al.start[a], rec.al.end[z], len(rec.fr))
        tt = np.arange(len(rec.fr))[sl] * C.HOP_S
        v = rec.fr.S[sl]
        decl.append(slope(tt, v))
        ok = np.isfinite(v)
        contour = np.full(C.CONTOUR_POINTS, np.nan)
        if ok.sum() >= 3:
            grid = np.linspace(tt[0], tt[-1], C.CONTOUR_POINTS)
            contour = np.interp(grid, tt[ok], v[ok], left=np.nan, right=np.nan)
        contours.append(contour)
        if final_words[z]:
            final.append(ending[z])
    x.update(final_pitch=np.array(final), declination=np.array(decl), contours=np.array(contours),
             level_slopes=np.array(slopes), last_drops=np.array(drops))
    return x


def sentence_final(tr) -> np.ndarray:
    """Per word: the word ends a sentence (it carries a full stop)."""
    return np.array([punctuation == '.' for punctuation in tr.punct])


def final_span(rec, i):
    """The last FINAL_WINDOW_S of word i (s), or the whole word when it is shorter."""
    a, b = rec.regions[i]
    return float(max(a, b - C.FINAL_WINDOW_S)), float(b)


def final_pitch_word(rec, min_voiced=C.MIN_FINAL_VOICED):
    out = np.full(len(rec.tr), np.nan)
    if rec.fr is None:
        return out
    for i in np.flatnonzero(sentence_final(rec.tr)):
        a, b = rec.regions[i]
        cut = final_span(rec, i)[0]
        early = rec.fr.S[frame_slice(a, cut, len(rec.fr))] if cut > a else np.array([])
        late = rec.fr.S[frame_slice(cut, b, len(rec.fr))]
        if np.isfinite(early).sum() >= min_voiced and np.isfinite(late).sum() >= min_voiced:
            out[i] = median(late) - median(early)
    return out
