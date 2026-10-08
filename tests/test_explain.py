"""Result-JSON explanations (cvoice.explain)."""
import dataclasses
import math

import numpy as np
import pytest
from synth import local, regime, with_x

from cvoice import config as C, explain
from cvoice.compare import compare
from cvoice.score import score


def test_local_pace_wording_is_relative_to_own_global_tempo(base, pinned_detector):
    comp = with_x(base, "D1", [(10, 15, -.4)])
    comp.dims["D1"].g = math.log(1.5)
    r = local("D1", 10, 15)
    reg = pinned_detector()["regimes"]["R1"]
    sc = score(comp, [r], reg, C.PMAX_START)
    item = explain.build(r, comp, base, base, reg, sc.masses[0], sc, "x")
    assert "Faster than your own overall tempo here" in item["text"]
    assert "score with this penalty removed" in item["text"] and "overall if fixed" not in item["text"]
    comp.dims["D1"].g = 0.0  # no whole-clip tempo flag: the wording is plain
    sc = score(comp, [r], reg, C.PMAX_START)
    assert "own overall tempo" not in explain.build(r, comp, base, base, reg, sc.masses[0], sc, "x")["text"]


def test_pace_explanation_names_actual_peak_window(base, pinned_detector):
    comp = with_x(base, "D1", [(10, 11, -.4)])
    r = local("D1", 10, 11)
    reg = pinned_detector()["regimes"]["R1"]
    sc = score(comp, [r], reg, C.PMAX_START)
    item = explain.build(r, comp, base, base, reg, sc.masses[0], sc, "pace")
    a, b = base.win[r.peak]
    assert f"peak window of {b - a + 1} words ('{base.tr.text(a, b)}')" in item["text"]
    assert "speech for these 2 words" not in item["text"] and item["words"] == [10, 11]


def test_pitch_explanation_carries_the_baseline_range_to_the_participants_overall_range(base, pinned_detector):
    comp = with_x(base, "D3", [(10, 15, -1.2)])  # ln ratio of window ranges, relative to the clip median
    r = local("D3", 10, 15)
    reg = pinned_detector()["regimes"]["R1"]
    sc = score(comp, [r], reg, C.PMAX_START)
    item = explain.build(r, comp, base, base, reg, sc.masses[0], sc, "pitch")
    d = comp.dims["D3"]
    assert item["type"] == "MONOTONE" and item["unit"] == "ln" and item["delta"] == pytest.approx(-1.2)
    assert item["baseline"] == pytest.approx(d.reference(10), abs=.005) and item["participant"] == pytest.approx(d.p[10], abs=.005)
    assert "% narrower" not in item["text"] and "the ranges are compared as a ratio with 1 st added to each" in item["text"]
    assert f"{item['participant']:.1f} st here" in item["text"] and f"{item['baseline']:.1f} st at your overall pitch range" in item["text"]
    assert item["threshold"] == pytest.approx(2.0 * C.FLOORS["D3"], abs=.005) and f"{1.2 / item['threshold']:.1f}x the threshold" in item["text"]


def test_whole_clip_tempo_explanation_uses_detector_median_ratio(base, pinned_detector):
    reg = pinned_detector()["regimes"]["R1"]
    for g, ftype in ((math.log(2), "TEMPO_SLOW"), (-math.log(2), "TEMPO_FAST")):
        comp = compare(base, base)
        comp.dims["D1"].g = g
        sc = score(comp, [], reg, C.PMAX_START)
        item = explain.build_clip("D1", comp, base, base, reg, sc)
        assert item["type"] == ftype and item["context"] == "whole passage" and item["dimension"] == "D1" and item["baseline"] == 1
        assert item["participant"] == pytest.approx(math.exp(g), abs=.005) and item["delta"] == pytest.approx(g, abs=.005)
        assert "median window speech-time ratio" in item["measure"] and f"{math.exp(g):.2f}x" in item["text"]
        assert item["threshold"] == pytest.approx(math.log(1.25), abs=.005) and item["words"] == [0, len(base.tr) - 1]


def test_whole_clip_pitch_range_explanation_for_d3(base):
    reg = regime("R1", clip={"D1": math.log(1.25), "D3": math.log(2.0)})
    comp = compare(base, base)
    comp.dims["D3"].g = -math.log(3.0)  # the participant's median window range is a third of the reference's
    sc = score(comp, [], reg, C.PMAX_START)
    part = dataclasses.replace(base, win_R=base.win_R / 3)
    item = explain.build_clip("D3", comp, base, part, reg, sc)
    assert item["type"] == "RANGE_NARROW" and item["label"] == "RANGE_NARROW (whole clip)" and item["dimension"] == "D3"
    assert item["context"] == "whole passage" and item["unit"] == "ln" and item["brief_word"] == "Tone"
    b, p = float(np.nanmedian(base.win_R)), float(np.nanmedian(base.win_R)) / 3  # median window pitch ranges in st
    assert item["value_unit"] == "st" and item["baseline"] == pytest.approx(b, abs=.005) and item["participant"] == pytest.approx(p, abs=.005) and item["delta"] == pytest.approx(-math.log(3.0), abs=.005)
    assert item["threshold"] == pytest.approx(math.log(2.0), abs=.005) and item["tolerance_multiple"] == pytest.approx(math.log(3.0) / math.log(2.0), abs=.005)
    assert "median pitch range P90-P10 over five-word windows, st" == item["measure"] and f"Overall pitch range: your typical five-word pitch range is {p:.1f} st against {b:.1f} st in the reference rendition" in item["text"]
    assert "x0.33" in item["text"] and "flagged below x0.50" in item["text"]
    assert item["severity"] == pytest.approx(sc.clip["D3"], abs=.005) and item["points_lost"] > 0 and item["overall_if_fixed"] > sc.overall
    assert f"the reference moves about {b:.1f} st" in item["fix"] and item["why"].startswith('"')


def test_tolerance_multiple_is_relative_to_the_flag_threshold(base, pinned_detector):
    comp = with_x(base, "D1", [(10, 15, -.4)])
    r = local("D1", 10, 15)
    reg = pinned_detector(3.0)["regimes"]["R1"]
    sc = score(comp, [r], reg, C.PMAX_START)
    item = explain.build(r, comp, base, base, reg, sc.masses[0], sc, "x")
    assert item["threshold"] == pytest.approx(3.0 * C.FLOORS["D1"], abs=.005) and item["tolerance_multiple"] == pytest.approx(.4 / (3.0 * C.FLOORS["D1"]), abs=.01)
    assert f"{item['tolerance_multiple']:.1f}x the threshold" in item["text"] and "tolerance" not in item["text"]
