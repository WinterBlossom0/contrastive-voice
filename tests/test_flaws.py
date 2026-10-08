import numpy as np
import pytest
from synth import recording

from cvoice import audio, config as C, flaws
from cvoice.features import frame_features

SR = C.SR


@pytest.fixture(scope="module")
def rec():
    return recording(40, pauses={7: 0.7, 19: 0.8, 30: 0.6})


def run(rec, edit, chain_name="A"):
    plan = flaws.Plan([edit])
    y, lab = flaws.inject(rec, plan, "t", "p", recipe="t", seed=1, chain_name=chain_name)
    return y, lab, lab["flaws"][0]


def window_edit(rec, typ, level, i0, i1):
    ed = flaws.make_edit(rec, typ, level, (i0, i1))
    return ed


def test_warp_sides_and_chain_composition():
    w = flaws.Warp([0, 20, 20, 50, 60, 100], [0, 20, 30, 60, 60, 100])  # 10 inserted at 20, [50, 60) removed
    assert w(20, "left") == 20 and w(20, "right") == 30 and w(55) == 60 and w(100) == 100 and w(5) == 5
    chain = flaws.Chain()
    chain.warps += [flaws.Warp([0, 40, 80, 200], [0, 40, 60, 180]), flaws.Warp([0, 10, 10, 180], [0, 10, 15, 185])]
    assert chain(40, "right") == 40 + 5 and chain(80, "left") == 60 + 5 and chain(5) == 5
    assert chain.cur(10, 80) == (15, 65)
    with pytest.raises(ValueError):
        flaws.Warp([0, 10, 5], [0, 1, 2])


@pytest.mark.parametrize("typ,r", [("RUSH", 1.9), ("RUSH", 1.2), ("DRAG", 1.45), ("DRAG", 1.9)])
def test_time_scaling_scales_speech_only_and_labels_follow(rec, typ, r):
    i0, i1 = 5, 10  # contains the 0.7 s pause after word 7
    ed = window_edit(rec, typ, 3, i0, i1)
    ed.param = r
    assert len(ed.pauses) == 1
    y, lab, f = run(rec, ed)
    a, b = ed.a, ed.b
    pause = ed.pauses[0][1] - ed.pauses[0][0]
    rate = r if typ == "RUSH" else 1 / r
    speech = (b - a) - pause
    expected_len = pause + speech / rate
    assert len(y) == len(rec.wav) - (b - a) + round(f["span"][1] - f["span"][0])
    assert abs((f["span"][1] - f["span"][0]) - expected_len) <= 3 * 2  # a few samples of rounding per piece
    assert f["realised"]["value"] == pytest.approx(np.log(1 / rate), abs=2e-3)
    assert lab["outside_support_identical"] and f["parent_span"] == [a, b]
    assert f["span"][0] == a  # the span starts where the parent span started (nothing before it changed)
    ws, we = np.array(lab["words"]["start"]), np.array(lab["words"]["end"])
    assert np.all(np.diff(ws) >= 0) and np.all(we >= ws)
    shift = len(y) - len(rec.wav)
    assert lab["words"]["start"][-1] - lab["parent_words"]["start"][-1] == shift  # words after the edit move by the length change


def test_dropped_pause_keeps_exactly_the_floor_and_cuts_the_rest(rec):
    ed = flaws.make_edit(rec, "PAUSE_DROPPED", 3, (7, 8))
    dur = ed.b - ed.a
    y, lab, f = run(rec, ed)
    keep = round(C.PAUSE_FLOOR_S * SR)
    assert f["span"][1] - f["span"][0] == keep and len(y) == len(rec.wav) - (dur - keep)
    assert f["realised"]["value"] == pytest.approx(-(dur - keep) / SR) and f["event"] == "boundary"
    assert lab["outside_support_identical"]
    for level, frac in ((1, 0.4), (2, 0.2)):
        e = flaws.make_edit(rec, "PAUSE_DROPPED", level, (7, 8))
        y2, _, f2 = run(rec, e)
        assert f2["span"][1] - f2["span"][0] == max(round(frac * dur), keep)


def test_intrusive_pause_inserts_room_tone_of_the_exact_length(rec):
    ed = flaws.make_edit(rec, "PAUSE_INTRUSIVE", 3, (3, 4))
    assert ed.a == ed.b
    y, lab, f = run(rec, ed)
    n = round(1.2 * SR)
    assert f["span"] == [ed.a, ed.a + n] and len(y) == len(rec.wav) + n
    inside = y[ed.a + 400:ed.a + n - 400]
    assert np.sqrt(np.mean(inside ** 2)) < 5e-3  # room tone, not speech
    assert lab["outside_support_identical"] and f["realised"]["value"] == pytest.approx(1.2)
    assert f["support"][0] < f["span"][0] and f["support"][1] > f["span"][1]
    # the words after the insertion move by exactly n
    assert lab["words"]["start"][10] - lab["parent_words"]["start"][10] == n and lab["words"]["start"][2] == lab["parent_words"]["start"][2]


def test_monotone_preserves_length_compresses_pitch_and_is_deterministic(rec):
    ed = window_edit(rec, "MONOTONE", 3, 11, 16)
    y, lab, f = run(rec, ed)
    assert len(y) == len(rec.wav) and f["span"] == [ed.a, ed.b] and lab["outside_support_identical"]
    fy = frame_features(y)
    before = flaws._pitch_range(rec.fr, ed.a, ed.b)
    after = flaws._pitch_range(fy, ed.a, ed.b)
    assert after < 0.5 * before and f["realised"]["value"] == pytest.approx(after - before)
    y2, lab2, _ = run(rec, ed)
    assert audio.sha256_pcm(y) == audio.sha256_pcm(y2) and lab["sha256"] == lab2["sha256"]  # seeded Praat: identical regeneration


def test_deemphasis_shortens_lowers_and_flattens_one_word(rec):
    ed = window_edit(rec, "DEEMPHASIS", 3, 12, 12)
    y, lab, f = run(rec, ed)
    old = ed.b - ed.a
    new = f["span"][1] - f["span"][0]
    assert new == pytest.approx(old / 1.25, abs=2) and len(y) == len(rec.wav) - (old - new)
    assert lab["outside_support_identical"] and f["event"] == "word"
    lev0 = rec.fr.L[flaws._frames(ed.a, ed.b, len(rec.fr))].mean()
    lev1 = frame_features(y).L[flaws._frames(*f["span"], len(y) // C.HOP + 1)].mean()
    assert lev1 < lev0 - 3.0


def test_fade_ramps_holds_releases_and_the_release_is_in_the_support(rec):
    ed = window_edit(rec, "FADE", 3, 25, 31)
    y, lab, f = run(rec, ed)
    assert len(y) == len(rec.wav) and f["span"] == [ed.a, ed.b] and lab["outside_support_identical"]
    assert f["support"] == [ed.a, ed.b + round(C.FADE_RELEASE_S * SR)]
    third = ed.a + (ed.b - ed.a) // 3
    hold = slice(third + 800, ed.b - 800)
    gain = 20 * np.log10(np.sqrt(np.mean(y[hold] ** 2)) / np.sqrt(np.mean(rec.wav[hold] ** 2)))
    assert gain == pytest.approx(-14.0, abs=1.5)
    early = slice(ed.a, ed.a + 800)
    assert abs(20 * np.log10(np.sqrt(np.mean(y[early] ** 2)) / np.sqrt(np.mean(rec.wav[early] ** 2)))) < 2.0
    assert f["realised"]["value"] < -6.0


def test_mumble_changes_only_the_span(rec):
    ed = window_edit(rec, "MUMBLE", 3, 14, 19)
    y, lab, f = run(rec, ed)
    assert len(y) == len(rec.wav) and f["span"] == [ed.a, ed.b] and lab["outside_support_identical"]
    assert not np.array_equal(y[ed.a:ed.b], rec.wav[ed.a:ed.b]) and f["realised"]["name"] == "ln_mfcc_delta_ratio"


def test_chain_b_psola_duration_labels(rec):
    ed = window_edit(rec, "RUSH", 3, 12, 16)
    y, lab, f = run(rec, ed, "B")
    assert lab["chain"] == "B" and lab["outside_support_identical"]
    span = f["span"][1] - f["span"][0]
    assert span == pytest.approx((ed.b - ed.a) / 1.9, rel=0.03)
    assert len(y) - len(rec.wav) == pytest.approx(span - (ed.b - ed.a), abs=8)  # the label warp matches the realised length change


def test_composite_clip_outside_supports_identical_and_words_monotone(rec):
    plan = flaws.plan_botched(rec, 7)
    y, lab = flaws.inject(rec, plan, "g5", "p", recipe="G5", seed=7)
    types = [f["type"] for f in lab["flaws"]]
    assert types.count("RUSH") == 1 and types.count("MONOTONE") == 1 and types.count("PAUSE_DROPPED") == 3 and types.count("FADE") == 2
    assert lab["outside_support_identical"]
    ws, we = np.array(lab["words"]["start"]), np.array(lab["words"]["end"])
    assert np.all(np.diff(ws) >= 0) and we[-1] <= len(y) and len(y) < len(rec.wav)
    assert lab["words"]["start"][0] < lab["parent_words"]["start"][0] + 1


def test_identity_plan_runs_every_recipe_with_null_parameters(rec):
    plan = flaws.identity_plan(rec, 5)
    assert all(e.param is None for e in plan.edits) and len(plan.edits) >= 6
    y, lab = flaws.inject(rec, plan, "id", "p", recipe="identity", seed=5)
    assert all(f["placebo"] for f in lab["flaws"]) and len(y) == len(rec.wav) and lab["outside_support_identical"]
    fy = frame_features(y)  # PSOLA re-phases the waveform, so compare level and pitch, not samples
    assert np.abs(fy.L - rec.fr.L).mean() < 0.3
    both = rec.fr.voiced & fy.voiced
    assert both.sum() > 0.95 * rec.fr.voiced.sum() and np.median(np.abs(fy.S[both] - rec.fr.S[both])) < 0.3


def test_span_policy_is_seeded_nonoverlapping_and_capped():
    rec = recording(70, pauses={7: 0.7, 19: 0.8, 30: 0.6, 45: 0.7})
    specs = [("RUSH", 2), ("PAUSE_DROPPED", 2), ("MONOTONE", 2), ("FADE", 2)]
    p1, p2 = flaws.plan_clip(rec, specs, 11), flaws.plan_clip(rec, specs, 11)
    assert p1.edits == p2.edits and flaws.plan_clip(rec, specs, 12).edits != p1.edits
    assert not p1.skipped
    words = [e for e in p1.edits if e.kind != "boundary"]
    for e in words:
        assert 5 <= e.words[1] - e.words[0] + 1 <= 8 and rec.tr.sentence[e.words[0]] == rec.tr.sentence[e.words[1]]
    spans = sorted(e.words for e in p1.edits)
    assert all(b[0] - a[1] > C.EDIT_GAP_WORDS for a, b in zip(spans, spans[1:]))
    assert sum(e.words[1] - e.words[0] + 1 for e in words) / len(rec.tr) <= C.COVERAGE_CAP
    dropped = next(e for e in p1.edits if e.type == "PAUSE_DROPPED")
    assert rec.sil[dropped.words[0]] >= C.PAUSE_DROP_MIN_BASE_S  # only where the event exists
    ints = flaws.plan_clip(rec, [("PAUSE_INTRUSIVE", 2)], 3).edits[0]
    assert rec.sil[ints.words[0]] == 0 and rec.tr.punct[ints.words[0]] == ""


def test_cross_speaker_events_must_exist_in_both_recordings():
    B = recording(40, pauses={7: 0.7, 19: 0.8})
    P0 = recording(40, pauses={7: 0.7, 30: 0.9})
    plan = flaws.plan_clip(P0, [("PAUSE_DROPPED", 3)], 1, ref=B)
    assert [e.words[0] for e in plan.edits] == [7]
    none = flaws.plan_clip(P0, [("PAUSE_DROPPED", 3), ("DEEMPHASIS", 3)], 1, ref=B)
    assert any(s["type"] == "DEEMPHASIS" for s in none.skipped)  # no stress word in either synthetic recording


def test_coverage_cap_is_hard_even_when_every_attempt_is_over_it():
    rec = recording(36, pauses={7: 0.7, 19: 0.8})  # the three edits need at least 15 of 36 words: 42 % > 35 % in every attempt
    order = ["RUSH", "MONOTONE", "FADE"]
    specs = [(t, 2) for t in order]
    reasons = set()
    for seed in range(5):
        plan = flaws.plan_clip(rec, specs, seed)
        words = sum(e.words[1] - e.words[0] + 1 for e in plan.edits if e.kind != "boundary")
        assert words / len(rec.tr) <= C.COVERAGE_CAP  # never an over-cap plan, whatever the seed
        kept = [e.type for e in plan.edits]
        assert kept == order[:len(kept)] and sorted(s["type"] for s in plan.skipped) == sorted(order[len(kept):])  # the last windowed edits go
        reasons |= {s["reason"].split(" 0")[0] for s in plan.skipped}
    assert "coverage cap" in reasons  # seed 1 exercises the drop path
    assert len(flaws.plan_clip(rec, specs, 1, cap=None).edits) == 3  # the botched rung and identity clips are exempt by passing no cap


def test_drag_lists_pauses_among_its_expected_secondary_dimensions():
    assert "D2" in C.EXPECTED_SECONDARY["DRAG"]  # a gap of 0.11-0.19 s inside a dragged span grows to a pause: not a false region


def test_unedited_stretches_of_a_warp_map_exactly_so_an_inserted_pause_keeps_its_span():
    from cvoice.flaws import Chain, Warp
    ch = Chain()
    ch.warps = [Warp([0, 252960, 256800, 474880], [0, 252960, 256194, 474274]), Warp([0, 108000, 108000, 474274], [0, 108000, 117600, 483874])]
    assert float(ch(108000, "left")) == 108000 and float(ch(108000, "right")) == 117600


def test_registry_is_complete_and_extra_recipes_use_its_parameters():
    from cvoice import edits_extra as E
    from test_edits_extra import CASES, recipe_recording
    assert len(C.CORE8_TYPES) == 8 and len(C.EXTRA_TYPES) == 15 and len(C.FLAW_REGISTRY) == 23
    assert set(C.FLAW_TYPES) == set(C.FLAW_DIM) == set(C.LEVEL_PARAM) == set(C.EXPECTED_SECONDARY)
    rec = recipe_recording()
    for recipe, args, _ in CASES:
        _, _, lab = recipe(rec, *args, level=2)
        f = lab["flaws"][0]
        r = C.FLAW_REGISTRY[f["type"]]
        assert f["dimension"] == r["primary"] and f["family"] == r["family"]
        assert f["parameter"] == r["levels"][1] and tuple(f["expected_secondary"]) == r["secondary"]
        assert f["event"] == r["event"]
    assert not hasattr(E, "DIMENSIONS")


def test_no_eligible_extra_type_is_recorded_as_skipped(rec):
    plan = flaws.plan_clip(rec, [("BLOCK", 3)], 7)
    assert not plan.edits and plan.skipped == [{"type": "BLOCK", "level": 3, "reason": "no eligible position"}]
