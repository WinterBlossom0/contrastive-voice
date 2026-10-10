"""Calibration (cvoice.calibrate): regime fits, R1 selection, leave-one-reader-out, score gates and Pmax."""
import math

import pytest
from synth import label, recording, regime, with_x

from cvoice import calibrate, config as C
from cvoice.calibrate import Null, base_regime, fit_pmax, fit_r2, gate_violations, null_check, overall, select_r1
from cvoice.compare import compare
from cvoice.detect import KEYS, decode, key
from cvoice.events import Run
from cvoice.score import score

R2_KEYS = [k for k in KEYS if k[:2] in C.REGIME_DIMS["R2"]]


def identical_nulls(n=3):
    B = recording(40, pauses={7: 0.7, 19: 0.8})
    return [Null(f"n{i}", compare(B, B), B.tr.sentence, B.duration / 60) for i in range(n)]


def test_base_regime_on_identical_pairs_has_floor_scales_and_no_thresholds_yet():
    r1, r2 = base_regime("R1", identical_nulls()), base_regime("R2", identical_nulls())
    for entry, name in ((r1, "R1"), (r2, "R2")):
        assert entry["name"] == name and entry["enabled"] == list(C.REGIME_DIMS[name]) and entry["null"]["n_pairs"] == 3
        assert entry["scales"] == pytest.approx({key(d, sign) if C.is_event(d) else d: round(C.FLOORS[d], 6) for d in C.DIMS for sign in C.FLAG_SIGNS[d]}) and entry["h"] == dict.fromkeys(KEYS)
    assert r1["clip"] == C.CLIP_LN and r2["clip"] == dict.fromkeys(C.CLIP_DIMS)  # R1 keeps its design thresholds, R2 has to fit them


def test_fit_r2_on_identical_pairs_puts_h_at_the_grid_start_and_whole_clip_thresholds_at_the_floor():
    reg, tables = fit_r2(identical_nulls())
    assert {k: reg["h"][k] for k in R2_KEYS} == dict.fromkeys(R2_KEYS, 1.0) and all(reg["h"][k] is None for k in KEYS if k not in R2_KEYS)
    assert set(tables) == set(R2_KEYS) and all(len(t) == 221 for t in tables.values())
    assert reg["clip"]["D7"] is None
    assert {k: v for k, v in reg["clip"].items() if k != "D7"} == pytest.approx({k: round(C.FLOORS[k], 6) for k in ("D1", "D3")})
    assert reg["null"]["false_per_minute_at_h"] == 0.0 and reg["null"]["flags_by_key"] == {} and reg["name"] == "R2"


def test_fit_r2_gives_every_flag_key_its_share_of_the_budget_and_fits_whole_clip_thresholds(base, monkeypatch):
    monkeypatch.setattr(C, "H_GRID", (1.0, 2.0, 3.0))
    comp = with_x(base, "D5", [(10, 15, -3)])  # at the floor scale 2 dB: z = 1.5, one false region at h = 1 and none at h = 2
    comp.dims["D1"].g = math.log(1.5)
    nulls = [Null("a>b", comp, base.tr.sentence, 4.0)]
    reg, tables = fit_r2(nulls)
    share = C.FALSE_RATE_BUDGET / len(R2_KEYS)
    assert len(R2_KEYS) == 6 and reg["null"]["budget_per_key"] == share
    assert tables["D5-"][0] == {"h": 1.0, "regions": 1, "per_minute": 0.25}  # within the whole budget (0.5), above the key's share (1/12)
    assert reg["h"]["D5-"] == 2.0 and all(reg["h"][k] == 1.0 for k in R2_KEYS if k != "D5-")
    assert reg["h"]["D4-"] is None and reg["h"]["D6-"] is None and set(tables) == set(R2_KEYS)
    assert reg["clip"] == {"D1": round(math.log(1.5), 6), "D3": round(C.FLOORS["D3"], 6), "D7": None}
    # One fit clip: the clip-budget quantile is its own whole-clip value, so it is flagged at its own threshold.
    assert reg["null"]["flags_by_key"] == {"D1+ whole clip": 1} and reg["null"]["false_per_minute_at_h"] == 0.0


def test_null_check_counts_local_and_whole_clip_flags_by_key(base):
    comp = with_x(base, "D5", [(10, 15, -6)])
    comp.dims["D1"].g = -math.log(2.0)
    reg = {**regime("R2", 2.0), "null": {}}
    null_check(reg, [Null("a>b", comp, base.tr.sentence, 2.0)])
    assert reg["null"]["flags_by_key"] == {"D1- whole clip": 1, "D5-": 1} and reg["null"]["false_per_minute_at_h"] == .5
    assert reg["null"]["false_clip_flags_per_clip"] == 1.0


def test_leave_reader_out_removes_both_pair_roles(base, monkeypatch):
    seen = []

    def fit(nulls, full_curve=True):
        seen.append([n.id for n in nulls])
        return {"h": dict.fromkeys(KEYS, 2), "scales": C.FLOORS, "clip": {"D1": 1.0, "D3": 2.0}}, {}

    monkeypatch.setattr(calibrate, "fit_r2", fit)
    nulls = [Null(pair, compare(base, base), base.tr.sentence, 1) for pair in ("a>b", "b>a", "b>c", "c>b")]
    report = calibrate.r2_stability(nulls, ["a", "b"])
    assert seen == [["b>c", "c>b"], []]
    ranges = report["threshold_ranges"]
    assert set(ranges) == set(R2_KEYS) | {k + " whole clip" for k in C.CLIP_DIMS}
    assert ranges["D1-"] == {"min_threshold": 2 * C.FLOORS["D1"], "max_threshold": 2 * C.FLOORS["D1"], "disabled_refits": 0}
    assert ranges["D3 whole clip"] == {"min_threshold": 2.0, "max_threshold": 2.0, "disabled_refits": 0}


def test_leave_reader_out_reports_ranges_per_flag_key_in_physical_thresholds(monkeypatch):
    fits = iter([({"h": {**dict.fromkeys(KEYS, 2.0), "D2+": None}, "scales": {**C.FLOORS, "D2": 0.2}, "clip": {"D1": 0.3, "D3": 0.8}}, {}),
                 ({"h": {**dict.fromkeys(KEYS, 3.0), "D2+": 4.0}, "scales": {**C.FLOORS, "D2": 0.3}, "clip": {"D1": 0.5, "D3": 0.8}}, {})])
    monkeypatch.setattr(calibrate, "fit_r2", lambda nulls, full_curve=True: next(fits))
    ranges = calibrate.r2_stability([], ["a", "b"])["threshold_ranges"]
    assert ranges["D2+"] == {"min_threshold": pytest.approx(1.2), "max_threshold": pytest.approx(1.2), "disabled_refits": 1}
    assert ranges["D2-"] == {"min_threshold": pytest.approx(0.4), "max_threshold": pytest.approx(0.9), "disabled_refits": 0}
    assert ranges["D1 whole clip"] == {"min_threshold": 0.3, "max_threshold": 0.5, "disabled_refits": 0}


def test_r1_supervised_curve_counts_controls_and_breaks_ties_smallest(base, pinned_detector, monkeypatch):
    monkeypatch.setattr(C, "H_GRID", (1, 1.5, 2, 3, 3.05))
    reg = pinned_detector()["regimes"]["R1"]
    comp = with_x(base, "D5", [(10, 15, -4), (25, 26, -2.2)])
    run = Run(base, base, comp, [], score(comp, [], reg, C.PMAX_START), "R1", {}, scale=reg["scales"])
    control = Null("control", with_x(base, "D5", [(25, 26, -2.2)]), base.tr.sentence, 1)
    curve = select_r1([(run, label(base))], [control], reg)
    assert curve[0]["FP"] == 2 and curve[0]["control_regions"] == 1
    assert set(v for k,v in reg["h"].items() if k != "D9-") == {1.5} and set(reg["h"]) == set(KEYS) and len(curve) == 4  # one common h for every flag key
    assert curve[-1]["F1"] < max(r["F1"] for r in curve)


def test_r1_supervised_rule_selects_strict_f1_maximum(base, pinned_detector, monkeypatch):
    monkeypatch.setattr(C, "H_GRID", (1, 1.5, 2))
    reg = pinned_detector()["regimes"]["R1"]
    comp = with_x(base, "D5", [(10, 15, -2.2), (25, 26, -2.1)])
    run = Run(base, base, comp, [], score(comp, [], reg, C.PMAX_START), "R1", {})
    curve = select_r1([(run, label(base))], [], reg)
    assert set(reg["h"].values()) == {1} and curve[0]["F1"] > curve[1]["F1"]


# ---------------------------------------------------------------- score gates and Pmax
def rows(p1, p3, p5, ident=0.0, l1=0.02, b="s1"):
    z = {k: 0.0 for k in C.DIMS}
    mk = lambda d: {**z, **d}
    return [{"scored_dims": list(C.DIMS), **r} for r in [{"id": f"{b}-id", "baseline": b, "recipe": "identity", "P": z}, {"id": f"{b}-L1", "baseline": b, "recipe": "single_L1A", "P": mk({"D1": l1})},
            {"id": f"{b}-G1", "baseline": b, "recipe": "G1", "P": mk({"D1": p1})}, {"id": f"{b}-G3", "baseline": b, "recipe": "G3", "P": mk({"D1": p3, "D3": p3, "D5": p3})},
            {"id": f"{b}-G5", "baseline": b, "recipe": "G5", "P": {k: p5 for k in C.DIMS}}]]


def test_score_gates_and_pmax_fit():
    good = rows(0.03, 0.2, 0.6)
    pmax, factor, bad = fit_pmax(good)
    assert bad == [] and overall({k: 0.0 for k in C.DIMS}, pmax, C.DIMS) == 100.0
    viol = gate_violations(rows(0.03, 0.2, 0.01), C.PMAX_START)
    assert any("G5" in v for v in viol)  # a botched clip that barely loses points
    assert any("ladder" in v for v in gate_violations(rows(0.3, 0.05, 0.6), C.PMAX_START))
    assert any("L1-only" in v for v in gate_violations(rows(0.03, 0.2, 0.6, l1=1.0), C.PMAX_START))
    impossible = rows(0.03, 0.2, 0.0)  # G5 cannot score below 50 with zero penalty at any Pmax
    _, f2, bad2 = fit_pmax(impossible)
    assert bad2 and f2 in C.PMAX_FACTOR_GRID


def test_runtime_gates_and_pmax_share_coverage_mask(base, pinned_detector, monkeypatch):
    comp = with_x(base, "D2", [(7, 7, -.80)])  # gives 89 across seven scored dimensions (D3 partial coverage off, D8 listed)
    comp.dims["D2"].countable[7] = True
    comp.coverage["D3"] = .46
    reg = pinned_detector()["regimes"]["R1"]
    clip = {"id": "s_L1", "parent": "s", "recipe": "single_L1A"}

    class DS:
        def entry(self, *args): return {}
        def rec(self, entry): return base
        def labels(self, clip): return {"flaws": [{"level": 1}]}

    monkeypatch.setattr(calibrate, "compare", lambda *args: comp)
    rows_ = calibrate.clip_penalties(DS(), [clip], [base], reg)
    sc = score(comp, decode(comp, reg, base.tr.sentence), reg, C.PMAX_START)
    assert rows_[0]["scored_dims"] == [k for k in C.DIMS if k not in ("D3", "D8")]  # D8 listed in R1
    assert calibrate.overall(rows_[0]["P"], C.PMAX_START, rows_[0]["scored_dims"]) == sc.overall == pytest.approx(89, abs=1)
    assert "L1-only" in calibrate.gate_violations(rows_, C.PMAX_START)[0]
    monkeypatch.setattr(C, "PMAX_FACTOR_GRID", (1.0, 1.1))
    assert calibrate.fit_pmax(rows_)[1:] == (1.1, [])
    comp.dims["D3"].x[10:16] = -7
    regs = decode(comp, reg, base.tr.sentence)
    sc = score(comp, regs, reg, C.PMAX_START)
    from cvoice import pipeline
    partial = next(r for r in pipeline.scores_block(sc, reg)["dims"] if r["key"] == "D3")
    assert partial["scored"] and partial["score"] < 100
    assert partial["note"] == "scored on partial coverage (46 %)"
    rows_ = calibrate.clip_penalties(DS(), [clip], [base], reg)
    assert "D3" in rows_[0]["scored_dims"]
    assert calibrate.overall(rows_[0]["P"], C.PMAX_START, rows_[0]["scored_dims"]) == sc.overall


def test_r1_objective_always_includes_natural_rush_and_excludes_unvalidated_families(base, pinned_detector, monkeypatch):
    from copy import deepcopy
    monkeypatch.setattr(C, "H_GRID", (1, 1.5, 2))
    comp = with_x(base, "D5", [(10, 15, -4)])
    reg = pinned_detector()["regimes"]["R1"]
    run = Run(base, base, comp, [], score(comp, [], reg, C.PMAX_START), "R1", {})
    core = (run, label(base))
    extra = [(run, label(base, typ=t)) for t in C.EXTRA_TYPES if t != 'NATURAL_RUSH']
    before = deepcopy(reg)
    curve = select_r1([core], [], reg)
    assert select_r1([core, *extra], [], before) == curve and before == reg
    assert calibrate.calibration_types() == (*C.CORE8_TYPES, 'NATURAL_RUSH')
    assert not calibrate.calibration_clip({"spectrum": "extra", "types": ["LOW_EFFORT"]})
    assert calibrate.calibration_clip({"spectrum": "extra", "types": ["NATURAL_RUSH"]})
    assert calibrate.calibration_policy()["new_types_in_R1"] == ['NATURAL_RUSH']
    enabled = select_r1([core, (run, label(base, typ='NATURAL_RUSH'))], [], deepcopy(reg))
    assert set(enabled[0]['per_type_recall']) == {'FADE', 'NATURAL_RUSH'}


def test_bundled_lab_validation_opens_only_the_passed_labels():
    import json
    from cvoice.calibrate import LAB_VALIDATION, real_gate, validated_labels
    validation = json.loads(LAB_VALIDATION.read_text())
    labels = validated_labels(validation)
    assert {name for name, passed in labels.items() if passed} == {'filled_pause', 'natural_rush'}
    assert not real_gate(validation['D7+']) and not real_gate(validation['D8+'])
