"""Participant-only channel and speaker stress transforms; each preserves sample count."""
from __future__ import annotations

import functools
import math
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from scipy import signal

from . import audio
from . import config as C


def _gain(x: np.ndarray, seed: int, db: float) -> np.ndarray:
    return np.clip(x * 10 ** (db / 20), -1, 1)


def gain(db: float):
    return functools.partial(_gain, db=db)  # picklable: pool workers run the transforms


def lowpass(x: np.ndarray, seed: int) -> np.ndarray:
    return np.ascontiguousarray(signal.sosfiltfilt(signal.butter(4, C.LOWPASS_HZ, "low", fs=C.SR, output="sos"), x))


def noise(x: np.ndarray, seed: int) -> np.ndarray:
    nz = np.random.default_rng(seed).standard_normal(len(x))
    return x + nz * math.sqrt(float((x ** 2).mean()) / 10 ** (C.NOISE_SNR_DB / 10) / float((nz ** 2).mean()))


def mp3(x: np.ndarray, seed: int) -> np.ndarray:
    """ffmpeg MP3 round trip at MP3_KBPS, delay compensated by cross-correlation."""
    with tempfile.TemporaryDirectory() as tmp:
        a, b, c = (Path(tmp) / n for n in ("a.wav", "b.mp3", "c.wav"))
        audio.write_wav(a, x)
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(a), "-c:a", "libmp3lame", "-b:a", f"{C.MP3_KBPS}k", str(b)], check=True, timeout=120)
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(b), "-ar", str(C.SR), "-ac", "1", "-c:a", "pcm_s16le", str(c)], check=True, timeout=120)
        z = audio.read_wav(c)
    n = min(len(x), len(z), 5 * C.SR)
    lag = int(np.argmax(signal.correlate(z[:n], x[:n], mode="full", method="fft"))) - (n - 1)
    z = z[lag:] if lag > 0 else np.r_[np.zeros(-lag), z]
    return np.pad(z, (0, max(0, len(x) - len(z))))[:len(x)]


def compressor_gain(x: np.ndarray) -> np.ndarray:
    """Applied gain in dB before RMS make-up, using the stress compressor's follower. The threshold is relative to the clip's
    own peak envelope (P99): an absolute -20 dBFS threshold barely touched these quiet recordings (0.06 dB reduction)."""
    thr, ratio = C.COMPRESSION
    env = np.abs(x)
    a_att, a_rel = math.exp(-1 / (0.010 * C.SR)), math.exp(-1 / (0.100 * C.SR))
    sm = signal.lfilter([1 - a_rel], [1, -a_rel], env)  # release-style smoothing, then attack by max follower
    sm = np.maximum(sm, signal.lfilter([1 - a_att], [1, -a_att], env))
    db = 20 * np.log10(sm + 1e-9)
    thr += float(np.percentile(db, 99))
    gain = np.where(db > thr, (thr - db) * (1 - 1 / ratio), 0.0)
    return gain


def compression_reduction(x: np.ndarray) -> float:
    """Achieved RMS gain reduction in dB before make-up."""
    gain = compressor_gain(x)
    return float(10 * np.log10(max(np.mean(x ** 2), 1e-12) / max(np.mean(x ** 2 * 10 ** (gain / 10)), 1e-12)))


def compress(x: np.ndarray, seed: int) -> np.ndarray:
    """Feed-forward dynamic-range compressor (threshold / ratio from COMPRESSION, 10 ms attack, 100 ms release) with make-up
    gain restoring the RMS."""
    gain = compressor_gain(x)
    y = x * 10 ** (gain / 20)
    y *= math.sqrt((x ** 2).mean() / max((y ** 2).mean(), 1e-12))
    return np.clip(y, -1, 1)


def world_speaker(x: np.ndarray, seed: int) -> np.ndarray:
    """WORLD resynthesis with F0 scaled and the spectral envelope warped (a different-speaker proxy)."""
    import pyworld as pw
    f0r, fmr = C.SPEAKER_TRANSFORM
    xd = np.ascontiguousarray(x, dtype=np.float64)
    f0, t = pw.harvest(xd, C.SR, f0_floor=C.PSOLA_F0[0], f0_ceil=600.0, frame_period=5.0)
    sp, ap = pw.cheaptrick(xd, f0, t, C.SR), pw.d4c(xd, f0, t, C.SR)
    K = sp.shape[1]
    src = np.clip(np.arange(K) / fmr, 0, K - 1)
    i0 = np.floor(src).astype(int)
    i1 = np.minimum(i0 + 1, K - 1)
    w = src - i0
    sp = np.exp(np.log(sp)[:, i0] * (1 - w) + np.log(sp)[:, i1] * w)
    y = pw.synthesize(f0 * f0r, np.ascontiguousarray(sp), ap, C.SR, 5.0)
    return np.pad(y, (0, max(0, len(x) - len(y))))[:len(x)]


RANDOM_SEEDS = (1, 2, 3)
ROOM_RT60_S = 0.4


def room_impulse(seed, rt60=ROOM_RT60_S):
    t = np.arange(round(1.5 * rt60 * C.SR)) / C.SR
    diffuse = np.random.default_rng(seed).standard_normal(len(t)) * np.exp(-np.log(1000) * t / rt60)
    diffuse *= .35 / np.linalg.norm(diffuse)
    diffuse[0] += 1.
    return diffuse


def reverb(x, seed):
    """Synthetic room: exponential diffuse decay, nominal RT60 0.4 s, direct arrival at zero."""
    y = signal.fftconvolve(x, room_impulse(seed))[:len(x)]
    return y * math.sqrt(np.mean(x ** 2) / max(np.mean(y ** 2), 1e-12))


def babble(x, seed, speakers, snr):
    rng = np.random.default_rng(seed)
    noise = np.zeros(len(x))
    for speaker in speakers:
        if not len(speaker):
            continue
        part = np.take(speaker, (np.arange(len(x)) + rng.integers(len(speaker))) % len(speaker))
        noise += part / max(np.sqrt(np.mean(part ** 2)), 1e-12)
    return x + noise * math.sqrt(np.mean(x ** 2) / max(np.mean(noise ** 2), 1e-12) / 10 ** (snr / 10))


def phone(x, seed):
    """300–3400 Hz band-pass, 8 kHz sampling and G.711 mu-law companding on the participant."""
    y = signal.sosfiltfilt(signal.butter(4, (300, 3400), 'bandpass', fs=C.SR, output='sos'), x)
    y = np.clip(signal.resample_poly(y, 1, 2), -1, 1)
    encoded = np.sign(y) * np.log1p(255 * np.abs(y)) / np.log(256)
    encoded = np.round((encoded + 1) * 127.5) / 127.5 - 1
    decoded = np.sign(encoded) * np.expm1(np.abs(encoded) * np.log(256)) / 255
    return signal.resample_poly(decoded, 2, 1)[:len(x)]


def seeds(fn):
    return RANDOM_SEEDS if fn in (noise, reverb) or getattr(fn, 'func', None) is babble else (1,)


MATRIX = [("gain +6 dB", gain(C.GAIN_DB)), ("gain -6 dB", gain(-C.GAIN_DB)), ("low-pass 3.4 kHz", lowpass),
          ("white noise 20 dB SNR", noise), ("MP3 64 kbit/s", mp3), ("dynamic-range compression", compress),
          ("room reverb RT60 0.4 s", reverb), ("phone band + mu-law (participant only)", phone),
          ("WORLD speaker transform", world_speaker)]


def apply(fn, wav: np.ndarray, seed: int) -> np.ndarray:
    """A stress transform followed by the int16 grid (a pool worker runs this)."""
    return audio.quantize(fn(wav, seed))
