"""Stress transforms of the evaluation matrix (cvoice.stress)."""
import numpy as np
import pytest

from cvoice import audio, config as C, stress


def test_stress_transforms_do_what_they_say():
    t = np.arange(32000) / C.SR
    x = audio.quantize(0.2 * np.sin(2 * np.pi * 300 * t) * (0.2 + 0.8 * (t > 1)) + 0.1 * np.sin(2 * np.pi * 6000 * t))
    assert np.abs(stress.gain(6.0)(x, 0)).max() == pytest.approx(np.abs(x).max() * 10 ** (6 / 20), rel=1e-6)
    lp = stress.lowpass(x, 0)
    assert np.std(lp - 0.2 * np.sin(2 * np.pi * 300 * t) * (0.2 + 0.8 * (t > 1))) < 0.03 and np.abs(np.fft.rfft(lp))[int(6000 * 2)] < 0.05 * np.abs(np.fft.rfft(x))[int(6000 * 2)]
    n = stress.noise(x, 1)
    snr = 10 * np.log10(np.mean(x ** 2) / np.mean((n - x) ** 2))
    assert snr == pytest.approx(C.NOISE_SNR_DB, abs=0.1) and np.array_equal(n, stress.noise(x, 1)) and not np.array_equal(n, stress.noise(x, 2))
    c = stress.compress(x, 0)
    rms = lambda v, m: np.sqrt(np.mean(v[m] ** 2))
    quiet, loud = (t > 0.2) & (t < 0.8), t > 1.2
    assert rms(c, loud) / rms(c, quiet) < 0.9 * rms(x, loud) / rms(x, quiet)  # the level step between the two halves shrinks
    assert np.mean(c[t < 1] ** 2) / np.mean(c[t > 1] ** 2) > np.mean(x[t < 1] ** 2) / np.mean(x[t > 1] ** 2) * 0.99  # quiet part relatively louder


def test_compressor_reports_achieved_reduction_before_makeup():
    x = .4 * np.sin(2 * np.pi * 300 * np.arange(C.SR) / C.SR)
    assert stress.compression_reduction(x) > 3
    assert np.mean(stress.compress(x, 1) ** 2) == pytest.approx(np.mean(x ** 2), rel=0.05)  # make-up gain restores the RMS (the attack transient clips)


def test_apply_puts_the_result_on_the_int16_grid_and_the_matrix_names_its_transforms():
    x = 0.1 * np.sin(2 * np.pi * 300 * np.arange(8000) / C.SR)
    y = stress.apply(stress.noise, x, 3)
    assert len(y) == len(x) and np.array_equal(y, audio.quantize(stress.noise(x, 3)))
    assert [name for name, _ in stress.MATRIX][:2] == ["gain +6 dB", "gain -6 dB"] and stress.noise in dict(stress.MATRIX).values()
