"""Synthesizes the sound effects of the launch video into this folder.

    python3 make_sfx.py [OUT_DIR]

Every sound is computed here from sine waves and seeded noise (LICENSE.txt). Each file is scaled so that its loudest
100 ms block is at LEVEL_DB (block RMS, dBFS); src/components/SoundEffects.tsx sets each effect's level against the
narration from that same measure.
"""
import os
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

RATE = 48000
LEVEL_DB = -26.0
# One keystroke per typed character: the terminal types 0.5 characters per frame at 30 fps (src/scenes/S15Open.tsx).
KEY_INTERVAL = 1 / 15
KEYSTROKES = 80
rng = np.random.default_rng(11)


def seconds(n):
    return np.arange(int(n * RATE)) / RATE


def band(signal, low, high):
    return sosfilt(butter(2, [low, high], btype="bandpass", fs=RATE, output="sos"), signal)


def loudest_block_db(audio):
    mono = audio if audio.ndim == 1 else audio.mean(axis=0)
    block = int(0.1 * RATE)
    blocks = [mono[i : i + block] for i in range(0, max(1, len(mono) - block + 1), block // 4)]
    return max(10 * np.log10((b**2).mean() + 1e-20) for b in blocks)


def place(buffer, start, sound):
    index = int(start * RATE)
    end = min(len(buffer), index + len(sound))
    buffer[index:end] += sound[: end - index]


def click_part(strength):
    t = seconds(0.05)
    noise = band(rng.standard_normal(len(t)), 2000, 9000) * np.exp(-t / 0.0015)
    tick = np.sin(2 * np.pi * 3200 * t) * np.exp(-t / 0.006)
    body = np.sin(2 * np.pi * 180 * t) * np.exp(-t / 0.01)
    return strength * (0.6 * noise + 0.5 * tick + 0.35 * body)


def mouse_click():
    out = np.zeros(int(0.16 * RATE))
    place(out, 0.0, click_part(1.0))
    place(out, 0.075, click_part(0.55))
    return out


def whoosh():
    """Noise through a band that sweeps up and back, panned from left to right; returns stereo."""
    length = 0.75
    t = seconds(length)
    noise = rng.standard_normal(len(t))
    frame = 1024
    hop = 256
    window = np.hanning(frame)
    out = np.zeros(len(t) + frame)
    freqs = np.fft.rfftfreq(frame, 1 / RATE)
    for start in range(0, len(t) - frame, hop):
        position = start / len(t)
        centre = 500 * (5 ** np.sin(np.pi * position))
        mask = np.exp(-0.5 * (np.log2(np.maximum(freqs, 1) / centre) / 0.9) ** 2)
        spectrum = np.fft.rfft(noise[start : start + frame] * window) * mask
        out[start : start + frame] += np.fft.irfft(spectrum) * window
    out = out[: len(t)] * np.sin(np.pi * t / length) ** 2
    pan = np.linspace(-0.6, 0.6, len(t))
    angle = (pan + 1) * np.pi / 4
    return np.stack([out * np.cos(angle), out * np.sin(angle)])


def pop():
    t = seconds(0.16)
    freq = 550 + 550 * np.exp(-t / 0.02)
    phase = 2 * np.pi * np.cumsum(freq) / RATE
    tone = np.sin(phase) + 0.2 * np.sin(2 * phase)
    return tone * (1 - np.exp(-t / 0.002)) * np.exp(-t / 0.045)


def rise():
    length = 1.4
    t = seconds(length)
    freq = 330 * 2 ** (t / length)
    phase = 2 * np.pi * np.cumsum(freq) / RATE
    tone = np.sin(phase) + 0.25 * np.sin(2 * phase) + 0.1 * np.sin(3 * phase)
    envelope = np.minimum(1, t / 0.35) * np.clip((length - t) / 0.3, 0, 1)
    shimmer = 1 + 0.12 * np.sin(2 * np.pi * 9 * t)
    return sosfilt(butter(2, 3000, fs=RATE, output="sos"), tone * envelope * shimmer)


def bell(freq, length):
    t = seconds(length)
    partials = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * 2.76 * freq * t) * np.exp(-t / 0.25) + 0.12 * np.sin(2 * np.pi * 5.4 * freq * t) * np.exp(-t / 0.12)
    return partials * (1 - np.exp(-t / 0.002)) * np.exp(-t / 0.7)


def chime():
    out = np.zeros(int(1.8 * RATE))
    place(out, 0.0, bell(880.0, 1.6))
    place(out, 0.09, 0.85 * bell(1318.5, 1.6))
    return out


def typing():
    out = np.zeros(int((KEYSTROKES * KEY_INTERVAL + 0.2) * RATE))
    for index in range(KEYSTROKES):
        t = seconds(0.04)
        clack = band(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t / 0.004)
        thock = np.sin(2 * np.pi * rng.uniform(260, 340) * t) * np.exp(-t / 0.012)
        place(out, index * KEY_INTERVAL + rng.normal(0, 0.004) + 0.01, rng.uniform(0.7, 1.0) * (0.7 * clack + 0.5 * thock))
    return out


SOUNDS = {"click": mouse_click, "whoosh": whoosh, "pop": pop, "rise": rise, "chime": chime, "typing": typing}

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    for name, make in SOUNDS.items():
        audio = make()
        audio = audio * 10 ** ((LEVEL_DB - loudest_block_db(audio)) / 20)
        peak = np.abs(audio).max()
        if peak > 0.89:
            raise SystemExit(f"{name}: peak {peak:.2f} above -1 dBFS at the target level")
        data = (audio.T if audio.ndim == 2 else audio) * 32767
        wavfile.write(os.path.join(folder, f"{name}.wav"), RATE, data.astype(np.int16))
        print(f"{name}.wav  {audio.shape[-1] / RATE:.2f} s  peak {20 * np.log10(peak):.1f} dBFS")
