"""Audio ingest: ffmpeg decode, channel policy, resample, canonical 16 kHz mono PCM16 WAV.

Canonical audio is float64 on the int16 grid: sample = int16 / 32768. Everything downstream reads audio through
`read_wav` (or `quantize` for in-memory edits), so memory and disk give identical values.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
import soxr

from . import config as C

_MAGIC = (  # (offset, bytes, family)
    (0, b"RIFF", "wav"), (0, b"OggS", "ogg"), (0, b"fLaC", "flac"), (0, b"ID3", "mp3"),
    (0, b"\x1aE\xdf\xa3", "webm"), (4, b"ftyp", "mp4"),
)


UNREADABLE, DECODE_TIMEOUT, CHANNELS, TOO_LARGE, TOO_LONG, TOO_SHORT = (
    "unreadable", "decode_timeout", "channels", "too_large", "too_long", "too_short")
MIN_SECONDS = 1.0  # s, shortest upload that load_audio accepts


class AudioError(ValueError):
    """Raised at the upload boundary: unreadable, unsupported, or over the size / duration cap. kind: one of UNREADABLE,
    DECODE_TIMEOUT, CHANNELS, TOO_LARGE, TOO_LONG, TOO_SHORT, so that a caller can word the refusal for its user."""

    def __init__(self, message: str, kind: str = UNREADABLE):
        super().__init__(message)
        self.kind = kind


def sniff(path: Path) -> str:
    """Container family from magic bytes (never from the file name); raises AudioError when unknown."""
    with open(path, "rb") as f:
        head = f.read(16)
    for off, magic, family in _MAGIC:
        if head[off:off + len(magic)] == magic:
            return family
    if len(head) >= 2 and head[0] == 0xFF and (head[1] & 0xE0) == 0xE0:
        return "mp3"
    raise AudioError(f"{Path(path).name}: not a recognised audio container (magic bytes {head[:4].hex()})")


def decode(path: Path, timeout: float = C.DECODE_TIMEOUT_S, max_seconds: float | None = None) -> tuple[np.ndarray, int]:
    """ffmpeg decode to float64 [samples, channels] at the native sample rate (first audio stream). With max_seconds
    ffmpeg stops one second after that duration, so a long upload cannot fill the disk."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "decoded.wav"
        limit = [] if max_seconds is None else ["-t", str(max_seconds + 1.0)]
        cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-threads", "1", "-i", str(path),
               "-vn", "-map", "0:a:0", *limit, "-c:a", "pcm_f32le", "-f", "wav", str(out)]
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired as e:
            raise AudioError(f"{Path(path).name}: ffmpeg decode exceeded {timeout:.0f} s", DECODE_TIMEOUT) from e
        except subprocess.CalledProcessError as e:
            raise AudioError(f"{Path(path).name}: ffmpeg could not decode it: {e.stderr.decode(errors='replace')[:300]}") from e
        x, sr = sf.read(out, dtype="float64", always_2d=True)
    return x, int(sr)


def to_mono(x: np.ndarray) -> tuple[np.ndarray, str]:
    """Channel policy: mono as is; stereo with side energy > mid energy + STEREO_SIDE_DB uses the left channel
    (anti-phase transfers cancel in a mean), otherwise (L+R)/2. More than two channels is refused."""
    if x.shape[1] == 1:
        return x[:, 0], "mono"
    if x.shape[1] != 2:
        raise AudioError(f"{x.shape[1]} channels: only mono and stereo are supported", CHANNELS)
    mid, side = 0.5 * (x[:, 0] + x[:, 1]), 0.5 * (x[:, 0] - x[:, 1])
    side_db = 10.0 * np.log10((np.mean(side ** 2) + 1e-20) / (np.mean(mid ** 2) + 1e-20))
    return (x[:, 0], "left") if side_db > C.STEREO_SIDE_DB else (mid, "mean")


def quantize(x: np.ndarray) -> np.ndarray:
    """Round to the int16 grid used on disk: float64 samples int16 / 32768."""
    return to_int16(x).astype(np.float64) / 32768.0


def to_int16(x: np.ndarray) -> np.ndarray:
    return np.clip(np.round(x * 32768.0), -32768, 32767).astype(np.int16)


def canonical(x: np.ndarray, sr: int) -> np.ndarray:
    """Mono float -> 16 kHz (soxr HQ), DC removed, on the int16 grid."""
    if sr != C.SR:
        x = soxr.resample(np.ascontiguousarray(x, dtype=np.float64), sr, C.SR, quality="HQ")
    return quantize(x - x.mean())


def load_audio(path: Path, max_bytes: int | None = None, max_seconds: float | None = None) -> tuple[np.ndarray, dict]:
    """Upload path: size cap, magic-byte sniff, ffmpeg decode with timeout, channel policy, canonical 16 kHz mono.
    Returns (audio, info) with info = {family, sr_in, channels, channel_rule, duration_s}."""
    path = Path(path)
    size = path.stat().st_size
    if max_bytes is not None and size > max_bytes:
        raise AudioError(f"{path.name}: {size / 1e6:.1f} MB exceeds the {max_bytes / 1e6:.0f} MB cap", TOO_LARGE)
    family = sniff(path)
    x, sr = decode(path, max_seconds=max_seconds)
    mono, rule = to_mono(x)
    dur = len(mono) / sr
    if max_seconds is not None and dur > max_seconds:
        raise AudioError(f"{path.name}: longer than the {max_seconds:.0f} s cap", TOO_LONG)
    if dur < MIN_SECONDS:
        raise AudioError(f"{path.name}: {dur:.2f} s is too short to analyse", TOO_SHORT)
    return canonical(mono, sr), {"family": family, "sr_in": sr, "channels": int(x.shape[1]), "channel_rule": rule,
                                 "duration_s": round(dur, 3)}


def write_wav(path: Path, x: np.ndarray) -> None:
    """Canonical WAV: 16 kHz mono PCM16."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(path), to_int16(x), C.SR, subtype="PCM_16")


def read_wav(path: Path) -> np.ndarray:
    """Read a canonical WAV (16 kHz mono PCM16) as float64 on the int16 grid; refuses anything else."""
    with sf.SoundFile(str(path)) as f:
        if f.samplerate != C.SR or f.channels != 1 or f.subtype != "PCM_16":
            raise AudioError(f"{Path(path).name}: not a canonical WAV (16 kHz mono PCM16): "
                             f"{f.samplerate} Hz, {f.channels} ch, {f.subtype}")
        x = f.read(dtype="int16")
    return x.astype(np.float64) / 32768.0


def sha256_pcm(x: np.ndarray) -> str:
    """Hash of the canonical samples (not of the file bytes), stable across WAV writers."""
    import hashlib
    return hashlib.sha256(to_int16(x).tobytes()).hexdigest()
