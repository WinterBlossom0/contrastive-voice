import json

import numpy as np
import pytest
from synth import recording

from cvoice import audio, config as C, edits_extra as E
from cvoice.features import make_recording
from cvoice.flaws import EditError


def recipe_recording():
    rec = recording(16, text="We hold these truths to be self. Evident that all men are created equal and so.",
                    pauses={3: 0.7}, glide_st=-4)
    x = rec.wav.copy()
    a = round(rec.al.start[3] * C.SR)
    lo, hi = a + round(.012 * C.SR), a + round(.032 * C.SR)
    x[lo:hi] = 0.0001
    rng = np.random.default_rng(4)
    x[hi:hi + 96] = rng.normal(0, .12, 96)
    return make_recording(audio.quantize(x), rec.tr, rec.al)


@pytest.fixture(scope="module")
def rec():
    return recipe_recording()


CASES = [
    (E.natural_rushing, ((1, 5),), -1), (E.hesitation_before_word, (3,), 1),
    (E.word_by_word_reading, ((8, 12),), 1), (E.uneven_tempo, ((1, 5),), 1),
    (E.word_repetition, (0,), 1), (E.sound_repetition, (3,), 1),
    (E.rhyme_prolongation, (3,), 1), (E.onset_prolongation, (6,), 1),
    (E.block_before_release, (3,), 1), (E.low_vocal_effort, ((1, 5),), -1),
    (E.trailing_off, (1,), -1), (E.misplaced_emphasis, (4, 3), 1),
    (E.rising_ending, (1,), 1), (E.flattened_final_fall, (1,), -1),
    (E.repeated_contour, (0,), -1),
]


def expected_boundary(t, side, events):
    """Independent sum of sample insertions and replacements in parent coordinates."""
    result = float(t)
    for event in events:
        kind = event["kind"]
        if kind == "copy":
            point = event["source_span"][0]
            n = event["pause_span"][1] - event["clip_span"][0]
            if t > point or (t == point and side == "right"):
                result += n
        else:
            a, b = event["parent_span"]
            n = event["output_samples"]
            if a == b:
                if t > a or (t == a and side == "right"):
                    result += n
            elif t >= b:
                result += n - (b - a)
            elif t > a:
                assert kind == "stretch"  # no planted word boundary is inside a deleted pause
                result += (t - a) * (n / (b - a) - 1)
    return round(result)


def invariants(rec, y, chain, labels):
    flaw = labels["flaws"][0]
    assert labels["outside_support_identical"]
    for key, side, times in [("start", "right", rec.al.start), ("end", "left", rec.al.end)]:
        parent = np.rint(times * C.SR).astype(int)
        actual = [round(float(chain(t, side))) for t in parent]
        assert labels["words"][key] == actual
        assert actual == [expected_boundary(t, side, flaw["events"]) for t in parent]
    assert round(float(chain(len(rec.wav), "right"))) == len(y)
    assert np.all(np.diff(labels["words"]["start"]) >= 0)
    assert np.all(np.array(labels["words"]["end"]) >= labels["words"]["start"])
    outside = np.ones(len(rec.wav), bool)
    for a, b in flaw["parent_supports"]:
        outside[a:b] = False
    mapped = np.rint(chain(np.arange(len(rec.wav)), "right")).astype(int)
    assert np.array_equal(rec.wav[outside], y[mapped[outside]])
    assert all(k in flaw for k in ("type", "dimension", "dimension_name", "level", "magnitude", "parameter",
                                   "words", "span", "parent_span", "support", "realised"))
    json.dumps(labels, allow_nan=False)


@pytest.mark.parametrize("recipe,args,sign", CASES, ids=[f.__name__ for f, _, _ in CASES])
def test_recipe_levels_and_null(rec, recipe, args, sign):
    magnitudes = []
    secondary = []
    for level in (1, 2, 3):
        y, chain, labels = recipe(rec, *args, level=level)
        invariants(rec, y, chain, labels)
        realised = labels["flaws"][0]["realised"]
        value = realised["value"]
        assert value * sign > 0, realised
        magnitudes.append(value * sign)
        if recipe is E.low_vocal_effort:
            assert realised["alpha_change_db"] < 0 and realised["pitch_change_st"] < 0
            secondary.append(-realised["pitch_change_st"])
        if recipe is E.trailing_off:
            assert realised["level_slope_change_db_s"] < 0 and realised["last_word_level_change_db"] < 0
        if recipe is E.misplaced_emphasis:
            assert realised["function_change_p"] > 0 and realised["stressed_change_p"] < 0
    assert np.all(np.diff(magnitudes) > 0), magnitudes
    if secondary:
        assert np.all(np.diff(secondary, axis=0) > 0), secondary
    y, chain, labels = recipe(rec, *args, level=None)
    invariants(rec, y, chain, labels)
    assert np.array_equal(y, rec.wav) and not chain.warps
    assert labels["flaws"][0]["placebo"] and labels["flaws"][0]["parameter"] is None
    assert labels["flaws"][0]["realised"]["value"] == 0


def test_mean_one_factors_and_seed(rec):
    first = E.uneven_tempo(rec, (1, 5), 3, seed=14)
    second = E.uneven_tempo(rec, (1, 5), 3, seed=14)
    other = E.uneven_tempo(rec, (1, 5), 3, seed=15)
    f = first[2]["flaws"][0]
    assert np.mean(f["details"]["word_duration_factors"]) == pytest.approx(1, abs=1e-15)
    assert f["realised"]["mean_ratio"] == pytest.approx(1, abs=1 / (0.26 * C.SR))
    assert np.array_equal(first[0], second[0]) and not np.array_equal(first[0], other[0])


def test_rushing_compresses_words_and_shortens_pauses_separately(rec):
    for level, rate, keep in zip((1, 2, 3), E.RUSH_RATE, E.RUSH_PAUSE_KEEP):
        _, chain, lab = E.natural_rushing(rec, (1, 5), level)
        cuts = [e for e in lab["flaws"][0]["events"] if e["kind"] == "pause_cut"]
        assert cuts
        for event in cuts:
            a, b = event["parent_span"]
            assert chain.cur(a, b)[1] - chain.cur(a, b)[0] == round((b - a) * keep)
        for word in range(1, 6):
            a, b = round(rec.al.start[word] * C.SR), round(rec.al.end[word] * C.SR)
            assert chain.cur(a, b)[1] - chain.cur(a, b)[0] == round((b - a) / rate)


def test_effort_tilt_grows_when_high_band_speech_exceeds_the_room_floor():
    rec = recording(16, f0=180, pauses={3: 0.7}, glide_st=-4)
    changes = []
    for level in (1, 2, 3):
        y, chain, lab = E.low_vocal_effort(rec, (1, 5), level)
        invariants(rec, y, chain, lab)
        r = lab["flaws"][0]["realised"]
        changes.append([-r["value"], -r["alpha_change_db"], -r["pitch_change_st"]])
    assert np.all(np.diff(changes, axis=0) > 0)


def test_misplaced_emphasis_with_the_function_word_first(rec):
    y, chain, lab = E.misplaced_emphasis(rec, 0, 3, 3)
    invariants(rec, y, chain, lab)
    r = lab["flaws"][0]["realised"]
    assert r["function_change_p"] > 0 and r["stressed_change_p"] < 0


def test_reading_every_second_word_and_exact_silence(rec):
    y, chain, lab = E.word_by_word_reading(rec, (1, 5), 3, every=2)
    invariants(rec, y, chain, lab)
    assert len(y) - len(rec.wav) == 2 * round(0.3 * C.SR)
    # A block's inserted core has the recording floor, not voiced speech.
    y, chain, lab = E.block_before_release(rec, 3, 1)
    point = lab["flaws"][0]["events"][0]["parent_span"][0]
    a, b = round(float(chain(point, "left"))), round(float(chain(point, "right")))
    assert b - a == round(0.5 * C.SR)
    assert lab["flaws"][0]["span"] == [a, b]
    assert np.sqrt(np.mean(y[a + 160:b - 160] ** 2)) < 0.005


def test_copy_tokens_are_labelled_and_retained_word_beyond_join_is_exact(rec):
    for recipe, word, count in [(E.word_repetition, 0, 1), (E.sound_repetition, 3, 4)]:
        y, chain, lab = recipe(rec, word, 3)
        f = lab["flaws"][0]
        copies = f["events"]
        assert len(copies) == count
        a, b = round(rec.al.start[word] * C.SR), round(rec.al.end[word] * C.SR)
        s, e = chain.cur(a, b)
        fade = round(C.PAUSE_FADE_S * C.SR)
        assert np.array_equal(y[s + fade:e], rec.wav[a + fade:b])
        for copy in copies:
            lo, hi = copy["clip_span"]
            assert hi > lo and np.sqrt(np.mean(y[lo:hi] ** 2)) > 0.01
        assert f["span"][0] < s


def test_annotations_override_within_word_proxies(rec):
    b = round(rec.al.end[6] * C.SR)
    sound_span = E.continuant_span(rec, 6, True)
    y, chain, labels = E.onset_prolongation(rec, 6, 3, sound_span=sound_span)
    assert chain.cur(*sound_span)[1] - chain.cur(*sound_span)[0] == C.SR
    assert labels["flaws"][0]["approximation"]["method"] == "caller-supplied sound span"
    y, chain, labels = E.block_before_release(rec, 6, 2, release_sample=b - 100)
    assert labels["flaws"][0]["events"][0]["parent_span"] == [b - 100, b - 100]


def test_sentence_template_and_other_sentences_stay_exact(rec):
    y, _, _ = E.repeated_contour(rec, 0, 3)
    template_end = round(rec.al.end[6] * C.SR)
    assert np.array_equal(y[:template_end], rec.wav[:template_end])
    y, _, lab = E.trailing_off(rec, 1, 3)
    assert lab["flaws"][0]["words"] == [13, 15]
    assert np.array_equal(y[:template_end], rec.wav[:template_end])


def test_bad_selections_fail_explicitly(rec):
    with pytest.raises(EditError, match="internal acoustic pause"):
        E.natural_rushing(rec, (8, 12))
    with pytest.raises(ValueError, match="function word"):
        E.word_repetition(rec, 3)
    with pytest.raises(ValueError, match="content word"):
        E.hesitation_before_word(rec, 0)
    with pytest.raises(ValueError, match="inside"):
        E.block_before_release(rec, 3, release_sample=0)
    with pytest.raises(ValueError, match="level"):
        E.low_vocal_effort(rec, (1, 5), 4)
    with pytest.raises(ValueError, match="two words"):
        E.uneven_tempo(rec, (1, 1))
    with pytest.raises(ValueError, match="sound_span"):
        E.sound_repetition(rec, 3, sound_span=(0, 20))


def test_no_voice_is_not_silently_labelled_as_pitch_change(rec):
    silent = make_recording(np.zeros_like(rec.wav), rec.tr, rec.al)
    with pytest.raises(EditError):
        E.rising_ending(silent, 1)
    assert np.array_equal(E.rising_ending(silent, 1, None)[0], silent.wav)
    assert np.array_equal(E.repeated_contour(silent, 0, None)[0], silent.wav)


def test_signal_eligibility_and_prolongation_bounds(rec):
    for recipe, word, onset in [(E.onset_prolongation, 6, True), (E.rhyme_prolongation, 3, False)]:
        span = E.continuant_span(rec, word, onset)
        added = []
        for lv in C.LEVELS:
            _, chain, lab = recipe(rec, word, lv)
            n = chain.cur(*span)[1] - chain.cur(*span)[0]
            assert 2 <= n / (span[1] - span[0]) <= 10
            added.append(lab["flaws"][0]["realised"]["value"])
        assert min(added) > C.ALIGNMENT_ERROR_S[1]
        assert np.all(np.diff(added) > C.ALIGNMENT_ERROR_S[1])
    with pytest.raises(EditError, match="continuant"):
        E.onset_prolongation(rec, 6, 3, sound_span=(round(rec.al.start[6] * C.SR), round(rec.al.start[6] * C.SR) + 100))
    silent = make_recording(np.zeros_like(rec.wav), rec.tr, rec.al)
    with pytest.raises(EditError, match="continuant"):
        E.rhyme_prolongation(silent, 3)
    point = E.onset_burst(rec, 3)
    assert 0 < point - round(rec.al.start[3] * C.SR) < C.BURST_WINDOW_S * C.SR
    with pytest.raises(EditError, match="burst"):
        E.block_before_release(recording(), 3)


def test_repetition_variation_is_seeded_and_not_identical(rec):
    first = E.sound_repetition(rec, 3, 3)
    second = E.sound_repetition(rec, 3, 3)
    assert np.array_equal(first[0], second[0])
    events = first[2]["flaws"][0]["events"]
    assert len({(e["duration_factor"], e["gain_db"]) for e in events}) == 4
    copies = [first[0][a:b] for a, b in (e["clip_span"] for e in events)]
    assert all(not np.array_equal(a, b) for a, b in zip(copies, copies[1:]))
    assert all(.92 <= e["duration_factor"] <= 1.08 and abs(e["gain_db"]) <= 1 for e in events)


def test_extra_pause_gaps_use_core_energy_minimum(rec):
    for recipe, args in [(E.hesitation_before_word, (3,)), (E.word_by_word_reading, ((8, 12),))]:
        _, _, lab = recipe(rec, *args)
        for ev in lab["flaws"][0]["events"]:
            if ev["kind"] != "silence":
                continue
            point = ev["parent_span"][0]
            left = next(i for i in range(len(rec.tr)-1) if rec.al.end[i] * C.SR <= point <= rec.al.start[i+1] * C.SR)
            assert point == E.gap_point(rec, left)
    with pytest.raises(EditError, match="gap"):
        E.word_by_word_reading(rec, (1, 5))


def test_effort_alpha_coupling_and_trailing_release(rec):
    for lv in C.LEVELS:
        for recipe, args in [(E.low_vocal_effort, ((1, 5),)), (E.trailing_off, (1,))]:
            y, _, lab = recipe(rec, *args, lv)
            f = lab["flaws"][0]
            assert .4 <= f["realised"]["alpha_change_db"] / f["realised"]["value"] <= .7
            a, b = f["parent_span"]
            assert f["support"][1] >= b + round(C.FADE_RELEASE_S * C.SR)
            assert abs((y[b] - y[b-1]) - (rec.wav[b] - rec.wav[b-1])) < .02
