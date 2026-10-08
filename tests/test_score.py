import math

import numpy as np
import pytest
from synth import comparison as make_comparison, regime

from cvoice import config as C
from cvoice.compare import Dim
from cvoice.detect import KEYS, Region
from cvoice.score import clip_mass, score, severity, unit_severity

N = 10
SCALES = {"D1": 0.1, "D2": 0.2, "D3": 0.4, "D4": 0.5, "D5": 2.0, "D6": 0.2}
H = 2.0  # thresholds theta = h * s: D1 0.2, D2 0.4, D3 0.8, D4 1, D5 4, D6 0.4
REGIME = regime("R1", H, scales=SCALES, enabled=list(SCALES))


def dim(key, units, x, w):
    xs = np.full(N, np.nan)
    ws = np.zeros(N)
    for u, v in zip(units, x):
        xs[u] = v
        ws[u] = w
    return Dim(key, xs, np.zeros(N), np.zeros(N), np.isfinite(xs), ws)


def comparison(g=0.0, x_scale=1.0):
    d = {"D1": dim("D1", [2, 3], [0.4 * x_scale] * 2, 0.05), "D2": dim("D2", [4], [-0.9 * x_scale], 0.5),
         "D3": dim("D3", [4, 5, 6], [-1.2 * x_scale] * 3, 0.1), "D4": dim("D4", [6], [-1.2 * x_scale], 1 / 3),
         "D5": dim("D5", [7], [-5.0 * x_scale], 0.1), "D6": dim("D6", [8, 9], [-0.7 * x_scale] * 2, 0.1)}
    d["D1"].g = g
    return make_comparison(d, N)


REGIONS = [Region("D1", 1, 2, 3, 2, 4.0, (2, 3)), Region("D2", -1, 4, 4, 4, -4.5, (4,)), Region("D3", -1, 4, 6, 4, -3.0, (4, 5, 6)),
           Region("D4", -1, 6, 6, 6, -2.4, (6,)), Region("D5", -1, 7, 7, 7, -2.5, (7,)), Region("D6", -1, 8, 9, 8, -3.5, (8, 9))]


def test_hand_computed_vector_for_six_dimensions():
    sc = score(comparison(), REGIONS, REGIME, C.PMAX_START)
    # sev D1 = (0.4 - 0.2) / (ln 1.9 - 0.2) = 0.452638; mass = 2 * 0.05 * sev; P / 0.40
    # D2: (0.9 - 0.4) / 0.6 = 5/6, w 0.5 -> 5/12; D3: (1.2 - 0.8) / (ln 5 - 0.8) = 0.49417, 3 * 0.1; D4: (1.2 - 1) / 0.5 = 0.4, w 1/3
    # D5: (5 - 4) / (12 - 4) = 0.125, w 0.1; D6: (0.7 - 0.4) / 0.6 = 0.5, 2 * 0.1
    # K1 secondary registry: the D2 region is an expected secondary of the DRAG (D1+) region and the D4 region of the
    # MONOTONE (D3-) region within half a window, so each group carries one penalty: D2 and D4 lose nothing.
    expect = {"D1": 88.68404204, "D2": 100.0, "D3": 62.93724381, "D4": 100.0, "D5": 96.875, "D6": 75.0}
    assert {k: round(v, 8) for k, v in sc.S.items() if v is not None} == pytest.approx(expect, abs=1e-6)
    assert sc.overall == pytest.approx(sum(expect.values()) / 6, abs=1e-6)
    assert sc.masses == pytest.approx([0.045263832, 0.0, 0.148251025, 0.0, 0.0125, 0.1], abs=1e-8)


def test_identity_scores_100_and_regions_below_threshold_cost_nothing():
    sc = score(comparison(), [], REGIME, C.PMAX_START)
    assert sc.overall == 100.0 and all(v == 100.0 for v in sc.S.values() if v is not None)
    shoulder = Region("D1", 1, 2, 3, 2, 2.0, (2, 3))
    d = comparison()
    d.dims["D1"].x[[2, 3]] = 0.15  # inside hysteresis but below theta: no severity
    assert score(d, [shoulder], REGIME, C.PMAX_START).S["D1"] == 100.0


def test_monotonicity_larger_deviation_never_scores_higher():
    prev = None
    for k in (0.8, 1.0, 1.3, 1.8, 2.5, 4.0):
        sc = score(comparison(x_scale=k), REGIONS, REGIME, C.PMAX_START)
        if prev is not None:
            assert all(sc.S[d] <= prev.S[d] + 1e-12 for d in SCALES) and sc.overall <= prev.overall + 1e-12
        prev = sc
    assert score(comparison(x_scale=50), REGIONS, REGIME, C.PMAX_START).S["D3"] >= 0.0  # floor at zero


def test_points_lost_and_overall_if_fixed_are_closed_form():
    sc = score(comparison(), REGIONS, REGIME, C.PMAX_START)
    lost, fixed = sc.points_lost("D3", sc.masses[2])
    assert fixed == pytest.approx(sc.overall + (100.0 - sc.S["D3"]) / 6) and lost == pytest.approx(fixed - sc.overall)
    assert score(comparison(), [], REGIME, C.PMAX_START).points_lost("D1", 0.0) == (0.0, 100.0)


def test_clip_mass_and_scored_dimensions():
    lo, hi = math.log(1.25), math.log(1.9)
    assert clip_mass("D1", lo - 1e-9, lo) == 0.0 and clip_mass("D1", lo, lo) == 0.0
    assert clip_mass("D1", hi, lo) == pytest.approx(1.0) and clip_mass("D1", -hi, lo) == pytest.approx(1.0)
    mid = (lo + hi) / 2
    assert clip_mass("D1", mid, lo) == pytest.approx(0.5)
    sc = score(comparison(g=mid), [], REGIME, C.PMAX_START)
    assert sc.clip == {"D1": pytest.approx(0.5)} and sc.P["D1"] == pytest.approx(0.5) and sc.S["D1"] == 0.0  # 0.5 > Pmax 0.4: clipped at zero
    r2 = regime("R2", H, scales=SCALES)
    sc2 = score(comparison(), REGIONS[:3] + REGIONS[4:5], r2, C.PMAX_START)
    assert sc2.S["D4"] is None and sc2.S["D6"] is None
    assert sc2.overall == pytest.approx(np.mean([sc2.S[k] for k in ("D1", "D2", "D3", "D5")]))
    off = score(comparison(), [], regime("R1", dict.fromkeys(KEYS)), C.PMAX_START)
    assert off.overall is None  # flags disabled: no verdict


def test_clip_mass_saturation_rule_differs_between_regimes():
    theta = 2 * C.CLIP_SAT["D1"]  # an R2 threshold above the nominal saturation
    g = 1.5 * theta
    assert clip_mass("D1", g, theta) == 1.0  # R1 rule: saturated at CLIP_SAT, below the threshold: full mass
    assert clip_mass("D1", g, theta, r2=True) == pytest.approx(0.5)  # R2 rule: width R2_SAT_THRESHOLD_FACTOR * theta
    assert clip_mass("D1", theta, theta, r2=True) == 0.0 and clip_mass("D1", 2 * theta, theta, r2=True) == 1.0


def test_clip_masses_are_scored_in_both_regimes_and_by_direction():
    big = math.log(3.0)
    for name in ("R1", "R2"):
        reg = regime(name, H, scales=SCALES, clip={"D1": math.log(1.25), "D3": math.log(2.0)})
        sc = score(comparison(g=big), [], reg, C.PMAX_START)
        assert sc.clip["D1"] == pytest.approx(1.0 if name == "R1" else clip_mass("D1", big, math.log(1.25), True))
        assert sc.P["D1"] == sc.clip["D1"]
    wide = comparison()
    wide.dims["D3"].g = math.log(5.0)  # wider pitch range than the reference: no whole-clip flag
    assert score(wide, [], REGIME, C.PMAX_START).clip == {}
    wide.dims["D3"].g = -math.log(5.0)
    assert score(wide, [], REGIME, C.PMAX_START).clip == {"D3": pytest.approx(1.0)}


def test_severity_function():
    assert severity(0.2, 0.2, 1.0) == 0.0 and severity(-1.0, 0.2, 1.0) == 1.0 and severity(2.0, 0.2, 1.0) == 1.0
    assert severity(0.6, 0.2, 1.0) == pytest.approx(0.5)
    assert severity(0.5, 1.0, 0.8) == 0.0 and severity(1.2, 1.0, 0.8) == 1.0  # threshold above saturation


def test_r2_severity_has_width_above_nominal_saturation():
    d = dim("D5", [0], [0.0], 1.0)
    d.x[0] = -20
    assert unit_severity(d, 0, 2, 10, r2=True) == 0  # theta = 20: at the threshold
    d.x[0] = -30
    assert unit_severity(d, 0, 2, 10, r2=True) == .5  # the width is R2_SAT_THRESHOLD_FACTOR * theta, not X_SAT
    assert unit_severity(d, 0, 2, 10) == 1.0  # R1 rule: saturation already below the threshold, full severity beyond it
