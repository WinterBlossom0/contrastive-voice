"""Event matching and per-clip accounting (cvoice.events)."""
import dataclasses
import math

import numpy as np
import pytest
from synth import label, local, recording, regime

from cvoice import config as C, explain
from cvoice import events
from cvoice.compare import compare, pause_span
from cvoice.detect import Region
from cvoice.events import Run, clip_key, eval_clip, f1, overlaps, region_span, run_pair
from cvoice.score import score


def fake_run(regions):
    B = recording(40, pauses={7: 0.7, 19: 0.8})
    comp = compare(B, B)
    return Run(B, B, comp, regions, score(comp, [], regime("R1"), C.PMAX_START), "R1", {}), B


def truth_entry(dim, sign, span, secondary=(), typ="RUSH", words=(5, 9), event="span"):
    return {"type": typ, "level": 3, "dim": dim, "sign": sign, "span": span, "event": event, "secondary": list(secondary),
            "mid": 0.5 * sum(span), "words": list(words)}


def test_iou_matching_is_one_to_one_by_dimension_and_sign():
    run, B = fake_run([])
    al = B.al
    reg = lambda dim, sign, i0, i1: Region(dim, sign, i0, i1, i0, 5.0, tuple(range(i0, i1 + 1)))
    t = [truth_entry("D1", -1, (al.start[5], al.end[9]))]
    run.regions = [reg("D1", -1, 5, 9)]
    assert events.match(t, run) == {0: 0}
    run.regions = [reg("D1", 1, 5, 9)]  # right place, wrong sign
    assert events.match(t, run) == {}
    run.regions = [reg("D1", -1, 9, 13)]  # IoU < 0.5
    assert events.match(t, run) == {}
    run.regions = [reg("D1", -1, 3, 8), reg("D1", -1, 5, 9)]
    assert events.match(t, run) == {0: 1}  # the better overlap wins
    two = [t[0], truth_entry("D1", -1, (al.start[5], al.end[9]))]
    run.regions = [reg("D1", -1, 5, 9)]
    assert len(events.match(two, run)) == 1


def test_event_matching_uses_the_time_tolerance():
    run, B = fake_run([])
    al = B.al
    gap_mid = 0.5 * (al.end[7] + al.start[8])
    t = [truth_entry("D2", -1, (gap_mid - 0.03, gap_mid + 0.03), typ="PAUSE_DROPPED", event="boundary")]
    run.regions = [Region("D2", -1, 7, 7, 7, -5.0, (7,))]
    assert events.match(t, run) == {0: 0}
    run.regions = [Region("D2", -1, 12, 12, 12, -5.0, (12,))]
    assert events.match(t, run) == {}


def test_matching_prioritises_number_of_valid_matches(base, pinned_detector, monkeypatch):
    run = run_pair(base, base, pinned_detector(), "R1")
    run.regions = [local("D5", 10, 15), local("D5", 20, 25)]
    a = {"dim": "D5", "sign": -1, "span": (1, 2)}
    b = {"dim": "D5", "sign": -1, "span": (3, 4)}
    spans = [region_span(run, r) for r in run.regions]
    scores = [[.9, .5], [.5, .49]]
    monkeypatch.setattr(events, "iou", lambda p, t: scores[0 if t == a["span"] else 1][spans.index(p)])
    assert len(events.match([a, b], run)) == 2


def test_eval_clip_counts_false_regions_but_not_expected_secondary_firings():
    run, B = fake_run([])
    al = B.al
    lab = {"flaws": [{"type": "DEEMPHASIS", "dimension": "D4", "level": 3, "placebo": False, "span": [int(al.start[12] * C.SR), int(al.end[12] * C.SR)],
                      "event": "word", "expected_secondary": ["D1", "D3", "D5"], "words": [12, 12]}]}
    run.regions = [Region("D4", -1, 12, 12, 12, -4.0, (12,)), Region("D3", -1, 11, 13, 12, -4.0, (11, 12, 13)),  # secondary: not false
                   Region("D6", -1, 12, 14, 12, -4.0, (12, 13, 14)),  # D6 is not an expected secondary of DEEMPHASIS
                   Region("D5", -1, 30, 32, 30, -4.0, (30, 31, 32))]  # far away: false
    e = eval_clip(run, lab)
    assert e["truth"][0]["detected"] and e["secondary"] == 1 and sorted(f["group"] for f in e["false"]) == ["D5-", "D6-"]


def test_strict_secondary_exemption_is_by_word_index(base, pinned_detector):
    run = run_pair(base, base, pinned_detector(), "R1")
    # Event occurs far in time but at a shared labelled index: the secondary rule uses indices.
    lab = label(base, "DEEMPHASIS", (12, 12), ("D5",))
    run.regions = [local("D4", 12, 12), local("D5", 14, 14), local("D5", 15, 15)]
    adjusted = eval_clip(run, lab)
    strict = eval_clip(run, lab, secondary_exempt=False)
    assert adjusted["secondary"] == 1 and len(adjusted["false"]) == 1
    assert strict["secondary"] == 0 and len(strict["false"]) == 2


def test_flag_precision_counts_fragmented_predictions(base, pinned_detector):
    run = run_pair(base, base, pinned_detector(), "R1")
    run.regions = [local("D5", 10, 15), local("D5", 11, 14), local("D5", 30, 31)]
    ev = eval_clip(run, label(base), secondary_exempt=False)
    assert sum(t["touched"] for t in ev["truth"]) == 1
    assert ev["flags_on_flaw"] == 2 and ev["n_regions"] == 3
    assert len(ev["false"]) == 2  # strict one-to-one accounting keeps fragmentation false


def test_f1_counts_are_fractional_and_empty_cases_are_none_or_zero():
    assert f1(3, 1, 1)["f1"] == 0.75 and f1(0, 0, 0)["f1"] is None and f1(0, 2, 2)["f1"] == 0
    assert f1(1.45, 27.4, 30.55)["f1"] == .048
    assert f1(0, 0, 32)["f1"] == 0


def test_pause_span_and_result_use_acoustic_times(base, pinned_detector):
    comp = compare(base, base)
    r = local("D2", 7, 7)
    comp.dims["D2"].x[7] = -.5
    reg = pinned_detector()["regimes"]["R1"]
    run = Run(base, base, comp, [r], score(comp, [r], reg, C.PMAX_START), "R1", {})
    assert region_span(run, r) == tuple(base.sil_span[7])
    item = explain.build(r, comp, base, base, reg, 0, run.scored, "d2")
    assert item["p"] == pytest.approx(base.sil_span[7], abs=.001)
    missing = base.sil_span.copy()
    missing[7] = np.nan
    P = dataclasses.replace(base, sil_span=missing)
    a, b = pause_span(base, P, 7, comp)
    assert a == b and a == pytest.approx(float(base.sil_span[7].mean()))


def test_pause_localisation_errors_are_separate(base, pinned_detector):
    run = run_pair(base, base, pinned_detector(), "R1")
    run.regions = [local("D2", 7, 7)]
    lab = label(base, "PAUSE_DROPPED", (7, 8))
    ev = eval_clip(run, lab)
    assert ev["truth"][0]["detected"] and "pause_onset_ms" in ev["truth"][0] and "onset_ms" not in ev["truth"][0]


def test_flags_of_clips_with_different_lengths_are_compared_by_word_index():
    reg = lambda dim, sign, i0, i1: Region(dim, sign, i0, i1, i0, 5.0, tuple(range(i0, i1 + 1)))
    assert overlaps(reg("D1", -1, 5, 9), reg("D1", -1, 9, 12)) and not overlaps(reg("D1", -1, 5, 9), reg("D1", -1, 10, 12))
    assert not overlaps(reg("D1", -1, 5, 9), reg("D1", 1, 5, 9)) and not overlaps(reg("D1", -1, 5, 9), reg("D3", -1, 5, 9))


def test_a_run_counts_whole_clip_flags_beside_local_regions_and_can_swap_regions(base, pinned_detector):
    run = run_pair(base, base, pinned_detector(), "R1")
    run.regions, run.clip = [local("D5", 10, 15)], {"D1": math.log(1.5), "D3": -math.log(3.0)}
    assert run.n_flags == 3 and run.flag_keys == ["D5-", "D1+ whole clip", "D3- whole clip"]
    other = run.with_regions([])
    assert other.regions == [] and other.clip == run.clip and other.comp is run.comp and other.n_flags == 2 and run.n_flags == 3
    assert clip_key("D1", -0.2) == "D1- whole clip"


def test_run_pair_flags_the_whole_clip_when_the_clip_median_passes_the_regime_threshold(base, pinned_detector):
    P = dataclasses.replace(base, win_T=base.win_T * 0.5, win_W=base.win_W * 0.5)  # every window twice as fast: overall tempo, no local departure
    run = run_pair(base, P, pinned_detector(), "R1")
    assert all(r.dim == "D9" for r in run.regions) and set(run.clip) == {"D1"} and run.clip["D1"] == pytest.approx(math.log(0.5)) and run.flag_keys[-1] == "D1- whole clip" and set(run.flag_keys) == {"D9-", "D1- whole clip"}
    assert run.scored.clip["D1"] > 0 and run.scored.S["D1"] < 100


def test_pending_family_counts_only_registered_secondary_dimensions(base, pinned_detector):
    from synth import label, local
    from cvoice.events import eval_clip, run_pair
    lab = label(base, typ="REPEATED_CONTOUR", secondary=C.EXPECTED_SECONDARY["REPEATED_CONTOUR"])
    run = run_pair(base, base, pinned_detector(), "R1").with_regions([local("D4", 10, 15), local("D5", 10, 15)])
    ev = eval_clip(run, lab)
    assert ev["truth"][0]["status"] == "no detector" and ev["truth"][0]["detected"] is None
    assert ev["secondary"] == 1 and [f["group"] for f in ev["false"]] == ["D5-"]
    strict = eval_clip(run, lab, secondary_exempt=False)
    assert len(strict["false"]) == 2


def rush_truth_run(base, pinned_detector, typ, regions):
    run = run_pair(base, base, pinned_detector(), "R1")
    run.regions = regions
    return run, label(base, typ, (10, 14))


def test_one_detection_per_change_a_same_change_region_detects_a_change_no_own_key_region_detects(base, pinned_detector):
    # K2: no D1- region fired on the rush, so the D9- region (pauses not kept: part of the RUSH change) is its detection.
    run, lab = rush_truth_run(base, pinned_detector, "RUSH", [local("D9", 10, 14)])
    ev = eval_clip(run, lab, secondary_exempt=False)
    assert ev["truth"][0]["detected"] and ev["truth"][0]["detected_by"] == "same change: D9-"
    assert ev["false"] == [] and ev["duplicate"] == 0 and ev["n_regions"] == 1
    # The other direction: a D1- region detects a speech-tempo change that no D9- region detects.
    run, lab = rush_truth_run(base, pinned_detector, "NATURAL_RUSH", [local("D1", 10, 14)])
    ev = eval_clip(run, lab, secondary_exempt=False)
    assert ev["truth"][0]["detected"] and ev["truth"][0]["detected_by"] == "same change: D1-" and ev["false"] == []


def test_one_detection_per_change_a_same_change_region_is_a_duplicate_only_beside_a_detection(base, pinned_detector):
    run, lab = rush_truth_run(base, pinned_detector, "RUSH", [local("D1", 10, 14), local("D9", 10, 14)])
    ev = eval_clip(run, lab, secondary_exempt=False)
    assert ev["truth"][0]["detected_by"] == "own key" and ev["false"] == []
    assert [(d["group"], d["change"], d["on_truth"]) for d in ev["duplicates"]] == [("D9-", "D1-", True)]
    assert ev["n_regions"] == 1 and ev["flags_on_flaw"] == 1  # the overlap view counts the change once
    # Off every truth, a D1- and a D9- region of one false change are one false region and one duplicate.
    run, lab = rush_truth_run(base, pinned_detector, "FADE", [local("D1", 30, 34), local("D9", 30, 34)])
    ev = eval_clip(run, lab, secondary_exempt=False)
    assert [f["group"] for f in ev["false"]] == ["D1-"] and [(d["group"], d["on_truth"]) for d in ev["duplicates"]] == [("D9-", False)]


def test_f1_gives_per_speaker_values_and_no_interval_below_five_speakers():
    two = f1(30, 9, 2, clusters={"eisenhower": [(15, 6, 1)], "lbush": [(15, 3, 1)]})
    assert two["f1_ci95"] == [None, None] and two["f1_per_speaker"] == {"eisenhower": 0.811, "lbush": 0.882}
    assert two["f1_range"] == [0.811, 0.882] and "no interval" in two["ci_method"]
    five = f1(50, 10, 5, clusters={str(i): [(10, i, 1)] for i in range(5)})
    assert five["f1_per_speaker"] is None and five["f1_ci95"][0] < five["f1_ci95"][1] and "bootstrap" in five["ci_method"]
