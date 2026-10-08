import numpy as np
import pytest
from synth import recording

from cvoice import audio, config as C
from cvoice.align import (LABELS, TranscriptError, TranscriptMismatch, VOCAB, align_emissions, build_targets, ctc_viterbi, parse_transcript,
                          pause_threshold, require_match, spell_number)


def planted_logp(norm, frames_per_char=3, gap=2, T_extra=4):
    """Emissions with one char spike block per target char, blanks in between; returns (logp, expected first/last frame per word)."""
    targets, idx = build_targets(norm)
    T = len(targets) * (frames_per_char + gap) + T_extra
    logp = np.full((T, len(LABELS)), np.log(0.01 / (len(LABELS) - 1)))
    pos = {}
    t = 2
    for l, tok in enumerate(targets):
        pos[l] = (t, t + frames_per_char - 1)
        logp[t:t + frames_per_char, :] = np.log(0.01 / (len(LABELS) - 1))
        logp[t:t + frames_per_char, tok] = np.log(0.99)
        t += frames_per_char + gap
    logp[logp.max(axis=1) < np.log(0.5)] = np.log(0.01 / (len(LABELS) - 1))
    blank_rows = np.array([logp[i].max() < np.log(0.5) for i in range(T)])
    logp[blank_rows, 0] = np.log(0.99)
    exp = [(pos[p[0]][0], pos[p[-1]][1]) for p in idx]
    return logp, exp


def test_viterbi_recovers_planted_path():
    logp, exp = planted_logp(("HELLO", "WORLD", "A"))
    al = align_emissions(logp, ("HELLO", "WORLD", "A"))
    np.testing.assert_allclose(al.start, [f0 * 0.02 for f0, _ in exp])
    np.testing.assert_allclose(al.end, [(f1 + 1) * 0.02 for _, f1 in exp])
    assert al.mean_compat > 0.95


def test_viterbi_path_is_monotone_and_covers_all_targets():
    targets = np.array([VOCAB[c] for c in "ABBA"])
    rng = np.random.default_rng(0)
    logp = np.log(rng.dirichlet(np.ones(len(LABELS)), size=40))
    states, ext = ctc_viterbi(logp, targets)
    assert np.all(np.diff(states) >= 0) and states[0] in (0, 1) and states[-1] in (len(ext) - 1, len(ext) - 2)
    assert set((states[states % 2 == 1] - 1) // 2) == {0, 1, 2, 3}  # repeated B B is separated by a blank state


def test_viterbi_rejects_audio_too_short():
    with pytest.raises(TranscriptMismatch):
        ctc_viterbi(np.zeros((3, len(LABELS))), np.array([VOCAB[c] for c in "ABCDE"]))


def test_mismatch_is_recorded_everywhere_and_refused_only_at_trust_boundaries():
    logp, _ = planted_logp(("HELLO", "WORLD"))
    al = align_emissions(logp, ("ZZZZZ", "QQQQQ"))  # internal paths (G5 clips, nulls) continue: the compatibility is just recorded
    assert al.mean_compat < C.MEAN_COMPAT_MIN
    with pytest.raises(TranscriptMismatch, match="does not match"):
        require_match(al)
    assert require_match(align_emissions(logp, ("HELLO", "WORLD"))).mean_compat > 0.95


def test_numbers_and_sentences():
    assert spell_number("1989") == ["nineteen", "eighty", "nine"]
    assert spell_number("2001") == ["two", "thousand", "one"]
    assert spell_number("34th") == ["thirty", "fourth"]
    assert spell_number("3.5%") == ["three", "point", "five", "percent"]
    with pytest.raises(TranscriptError):
        spell_number("12ab")
    tr = parse_transcript("Mr. Smith said so, then left... and returned -- late. Next one: 8 years.")
    assert tr.norm[:3] == ("MR", "SMITH", "SAID")
    assert tr.n_sentences == 2 and tr.sentence[0] == 0
    assert tr.punct[tr.norm.index("SO")] == "," and tr.punct[tr.norm.index("LEFT")] == "..."
    assert tr.disp[-2:] == ("eight", "years")
    assert tr.slice(5, len(tr) - 1).sentence[0] == 0
    with pytest.raises(TranscriptError):
        parse_transcript(" ... -- ")


def test_syllables_dictionary_and_fallback():
    tr = parse_transcript("union zzzzzzq")
    assert tr.syll[0] == 2 and not tr.syll_heuristic[0] and tr.syll_heuristic[1]


def test_acoustic_pause_rule():
    rec = recording(24, pauses={7: 0.6, 15: 0.12})
    assert rec.sil[7] == pytest.approx(0.6, abs=0.12)  # silent run inside the raw gap (word edges are 20 ms inside)
    assert rec.sil[15] == 0.0 and rec.sil[3] == 0.0  # 0.12 s gap < 0.20 s: no pause
    assert (rec.sil > 0).sum() == 1
    assert np.isfinite(rec.sil_span[7]).all() and np.isnan(rec.sil_span[3]).all()


def test_pause_threshold_uses_the_peak_rule_on_a_digital_silence_floor_and_the_floor_rule_on_a_noisy_one():
    speech = np.linspace(-30.0, -10.0, 600)  # frame levels in dB
    digital = np.r_[np.full(400, -120.0), speech]  # gated recording: Q5 at -120 dB would put the threshold at -105 dB
    q99 = np.percentile(digital, C.PAUSE_PEAK_Q)
    assert pause_threshold(digital) == pytest.approx(q99 - C.PAUSE_PEAK_DB) and -46 < pause_threshold(digital) < -44
    noisy = np.r_[np.full(400, -50.0), speech]  # a noise floor 20 dB below the quietest speech: Q5 + 0.3 * (Q95 - Q5), about 12 dB
    q5, q95 = np.percentile(noisy, C.PAUSE_Q)
    assert pause_threshold(noisy) == pytest.approx(q5 + 0.3 * (q95 - q5)) and -39 < pause_threshold(noisy) < -37
    assert pause_threshold(noisy) > np.percentile(noisy, C.PAUSE_PEAK_Q) - C.PAUSE_PEAK_DB  # the peak rule is the weaker one here


def test_pause_needs_silence_not_just_a_raw_gap():
    """A long raw gap that holds voiced sound (alignment gap over speech) is not a pause."""
    from cvoice.align import Alignment, acoustic_pauses
    from cvoice.features import frame_features
    wav, st, en = __import__("synth").synth(8, pauses={})
    fr = frame_features(wav)
    al = Alignment(np.array([st[0], en[0] + 0.5]), np.array([st[0] + 0.05, en[0] + 0.55]), np.ones(2), 1.0)
    sil, _, _ = acoustic_pauses(al, fr.L, fr.voiced)
    assert sil[0] == 0.0  # the raw gap covers the rest of word 0 and the next buzz


def test_canonical_audio_policy():
    t = np.arange(16000) / 16000
    voice = np.sin(2 * np.pi * 200 * t) * 0.3
    anti = np.stack([voice, -voice], 1)
    mono, rule = audio.to_mono(anti)
    assert rule == "left" and np.allclose(mono, voice)
    mono, rule = audio.to_mono(np.stack([voice, voice * 0.9], 1))
    assert rule == "mean"
    q = audio.quantize(voice)
    assert np.array_equal(q, audio.quantize(q))  # idempotent on the int16 grid
    assert audio.sha256_pcm(q) == audio.sha256_pcm(audio.quantize(q))


def test_scraped_pages_drop_unspellable_tokens_but_uploads_refuse_them():
    with pytest.raises(TranscriptError):
        parse_transcript("In the 1990s we met at 9:02 today.")
    tr = parse_transcript("In the 1990s we met at 9:02 today.", strict=False)
    assert tr.norm == ("IN", "THE", "WE", "MET", "AT", "TODAY")
