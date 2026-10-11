import dataclasses
import json
import math

import numpy as np
import pytest
from synth import comparison, regime, with_x

from cvoice import config as C
from cvoice.align import parse_transcript
from cvoice.compare import Dim
from cvoice.detect import KEYS, config_hash, choose_h, clip_flags, decode, decode_dim, fit_clip, fit_scales, flagged_dims, key, load_detector, save_detector, threshold, wquantile
from cvoice.features import windows
from cvoice.score import score


def dim(key, x, p=None, countable=None, b=None):
    x = np.asarray(x, float)
    n = len(x)
    return Dim(key, x, np.zeros(n) if b is None else np.asarray(b, float), np.zeros(n) if p is None else np.asarray(p, float),
               np.ones(n, bool) if countable is None else np.asarray(countable, bool), np.full(n, 1.0 / n))


SENT = tuple([0] * 12 + [1] * 12)


def decode_regions(d, s, h, sentence=SENT):
    """decode_dim in the directions the dimension is flagged in."""
    return decode_dim(d, s, h, sentence, C.FLAG_SIGNS[d.key])


def test_region_opens_at_h_and_extends_to_the_larger_of_half_h_and_half_the_peak():
    x = np.zeros(24)
    x[[2, 3, 4]] = [0.5, 0.5, 0.16]  # s = 0.1, h = 3: z = 5, 5, 1.6: above h/2 = 1.5 but below half the peak (2.5)
    x[5] = 0.14  # z = 1.4 < h/2: ends the candidate run
    regs = decode_regions(dim("D1", x), 0.1, 3.0)
    assert len(regs) == 1 and (regs[0].i0, regs[0].i1) == (2, 3) and regs[0].sign == 1 and regs[0].peak in (2, 3)
    x = np.zeros(24)
    x[[2, 3, 4]] = [0.32, 0.2, 0.155]  # z = 3.2, 2.0, 1.55: half the peak is 1.6, above h/2 = 1.5
    assert [(r.i0, r.i1) for r in decode_regions(dim("D1", x), 0.1, 3.0)] == [(2, 3)]
    # a region only opens when its peak is >= h, so half the peak is never below h / 2: the h / 2 bound of the rule is implied


def test_pitch_range_regions_keep_their_shoulders_down_to_half_h():
    x = np.zeros(24)
    x[[2, 3, 4, 5, 6]] = [-0.16, -0.5, -0.5, -0.16, -0.14]  # s = 0.1, h = 3: z = -1.6, -5, -5, -1.6, -1.4
    assert [(r.i0, r.i1) for r in decode_regions(dim("D3", x), 0.1, 3.0)] == [(2, 5)]  # the range collapses only inside a flat stretch: no trim
    assert [(r.i0, r.i1) for r in decode_regions(dim("D5", x), 0.1, 3.0)] == [(3, 4)]  # a window mean is trimmed at half the peak


def test_a_run_holding_two_peaks_splits_at_the_half_maximum():
    x = np.zeros(24)
    x[[2, 3, 4, 5, 6]] = [-0.5, -0.26, -0.16, -0.4, -0.45]  # z = 5, 2.6, 1.6, 4.0, 4.5 (volume: one-sided, one-word minimum)
    regs = decode_regions(dim("D5", x), 0.1, 3.0)
    assert [(r.i0, r.i1, r.peak) for r in regs] == [(2, 3, 2), (5, 6, 6)]  # 4.0 and 4.5 clear half of their own peak (2.25), 1.6 does not


def test_run_without_a_crossing_is_not_a_region_and_h_is_the_opening_threshold():
    x = np.zeros(24)
    x[[2, 3]] = 0.2  # z = 2: above h/2 = 1.5 but below h = 3
    assert decode_regions(dim("D1", x), 0.1, 3.0) == []
    assert len(decode_regions(dim("D1", x), 0.1, 2.0)) == 1


def test_no_gap_bridging_and_signed_runs():
    x = np.zeros(24)
    x[[2, 3]] = 0.5
    x[5] = 0.0
    x[[6, 7]] = 0.5
    x[[9, 10]] = -0.5
    regs = decode_regions(dim("D1", x), 0.1, 3.0)
    assert sorted((r.i0, r.i1, r.sign) for r in regs) == [(2, 3, 1), (6, 7, 1), (9, 10, -1)]


def test_sentence_boundary_and_units_without_a_value_break_regions():
    x = np.zeros(24)
    x[10:14] = 0.5  # crosses the sentence boundary between words 11 and 12
    assert [(r.i0, r.i1) for r in decode_regions(dim("D1", x), 0.1, 3.0)] == [(10, 11), (12, 13)]
    x[:] = 0
    x[[2, 3, 4]] = [0.5, np.nan, 0.5]
    assert decode_regions(dim("D1", x), 0.1, 3.0) == []  # each side is a single word: below the two-word minimum


def test_minimum_words_for_pace_and_pitch_only():
    x = np.zeros(24)
    x[4] = 0.5
    assert decode_regions(dim("D1", x), 0.1, 3.0) == []
    x = np.zeros(24)
    x[4] = -9.0
    assert decode_regions(dim("D3", x), 2.0, 3.0) == []
    x = np.zeros(24)
    x[4] = -9.0
    assert len(decode_regions(dim("D5", x), 2.0, 3.0)) == 1  # single word is enough for volume


def test_one_sided_dimensions():
    x = np.zeros(24)
    x[[4, 5]] = 9.0
    for k, s in (("D3", 2.0), ("D5", 2.0), ("D6", 0.2)):
        assert decode_regions(dim(k, x), s, 3.0) == []  # positive: more varied / louder / clearer is not a flaw
        assert len(decode_regions(dim(k, -x), s, 3.0)) == 1


def test_pause_and_emphasis_are_single_events():
    x = np.full(23, np.nan)
    x[[3, 9]] = [-0.9, 0.5]
    countable = np.isfinite(x)
    regs = decode_regions(dim("D2", x, countable=countable), 0.15, 3.0)
    assert [(r.i0, r.i1, r.sign) for r in regs] == [(3, 3, -1), (9, 9, 1)]
    countable[9] = False
    assert len(decode_regions(dim("D2", x, countable=countable), 0.15, 3.0)) == 1
    x4 = np.full(24, np.nan)
    x4[[5, 8]] = [-2.0, -2.0]
    p4 = np.zeros(24)
    p4[5], p4[8] = 0.2, 1.1  # marker lost at 5, kept at 8
    regs = decode_regions(dim("D4", x4, p=p4, countable=np.isfinite(x4)), 0.5, 2.0)
    assert [r.i0 for r in regs] == [5]


def test_weighted_quantile_and_scales_never_below_the_floor():
    assert wquantile(np.array([1.0, 2.0, 3.0, 4.0]), np.ones(4), 0.5) == 2.0
    assert wquantile(np.array([1.0, 2.0, 3.0]), np.array([0.0, 0.0, 1.0]), 0.5) == 3.0
    comps = []
    for seed in range(3):
        rng = np.random.default_rng(seed)
        d = {k: dim(k, rng.normal(0, 1e-6, 24)) for k in C.DIMS}
        comps.append(comparison(d))
    scales, medians, counts = fit_scales(comps)
    assert scales == pytest.approx({key(d, sign) if C.is_event(d) else d: C.FLOORS[d] for d in C.DIMS for sign in C.FLAG_SIGNS[d]}) and counts["D1"] == 72
    d = {k: dim(k, np.random.default_rng(1).normal(0, 5, 200)) for k in C.DIMS}
    scales, _, _ = fit_scales([dataclasses.replace(comps[0], dims=d)])
    assert scales["D3"] == pytest.approx(5.0, rel=0.25)  # the data, not the floor, sets the tolerance


def test_choose_h_is_the_smallest_grid_value_within_the_budget():
    rng = np.random.default_rng(3)
    d = dim("D1", rng.normal(0, 0.1, 24))
    for sign in (-1, 1):
        h, table = choose_h([d], [SENT], 0.1, sign, 1.0, C.FALSE_RATE_BUDGET)
        assert h is not None and table[0]["h"] == 1.0 and table[-1]["h"] == 12.0 and len(table) == 221
        assert next(t for t in table if t["h"] == h)["per_minute"] <= C.FALSE_RATE_BUDGET
        assert all(t["per_minute"] > C.FALSE_RATE_BUDGET for t in table if t["h"] < h)
    assert choose_h([d], [SENT], 0.1, 1, 1.0, C.FALSE_RATE_BUDGET, full_curve=False)[1][-1]["h"] < 12.0  # stops at the first h within the budget
    far = dim("D1", np.full(24, 50.0))  # deviates at every unit: two regions at every h on the grid
    assert choose_h([far], [SENT], 0.1, 1, 1.0, C.FALSE_RATE_BUDGET)[0] is None  # no h qualifies: this direction's flags are disabled
    assert choose_h([far], [SENT], 0.1, -1, 1.0, C.FALSE_RATE_BUDGET)[0] == 1.0  # the other direction has no false region at all


def toy_rush(width: int, r: float, h: float, start: int = 25) -> float:
    """Noise-free toy of a rush over five to eight words (IoU >= 0.5 needed): 60 words of 0.30 s with 0.06 s gaps; words start .. start + width - 1 are sped
    up by r (gaps inside the span scale too, as WSOLA scales a whole speech piece); five-word windows, floor scale ln 1.10.
    Returns the best temporal IoU, in participant time, of a detected region with the edited span."""
    n, W, G = 60, 0.30, 0.06
    tr = parse_transcript(" ".join(["we"] * n) + ".")
    win = windows(tr)

    def times(rate: float):
        st, en, t = [], [], 0.0
        for i in range(n):
            inside = rate != 1.0 and start <= i < start + width
            d = W / rate if inside else W
            st.append(t)
            en.append(t + d)
            t += d + (G / rate if inside and start <= i + 1 < start + width else G)
        return np.array(st), np.array(en)

    (sb, eb), (sp, ep) = times(1.0), times(r)
    T = lambda s, e: np.array([e[w[1]] - s[w[0]] for w in win])
    x = np.log(T(sp, ep) / T(sb, eb))
    x -= np.median(x)
    d = Dim("D1", x, np.zeros(n), np.zeros(n), np.ones(n, bool), np.full(n, 1.0 / n))
    t0, t1 = sp[start], ep[start + width - 1]
    best = 0.0
    for g in decode_regions(d, C.FLOORS["D1"], h, tuple([0] * n)):
        a, b = sp[g.i0], ep[g.i1]
        inter = max(0.0, min(b, t1) - max(a, t0))
        best = max(best, inter / ((b - a) + (t1 - t0) - inter))
    return best


@pytest.mark.parametrize("h", [1.0, 2.0, 3.0])
def test_rush_spans_of_five_to_eight_words_reach_iou_half_at_l2_and_l3(h, monkeypatch):
    for r in (1.45, 1.90):  # L2, L3
        for width in (5, 6, 7, 8):
            assert toy_rush(width, r, h) >= C.IOU_MIN, (h, r, width)
    monkeypatch.setitem(C.REGION_PEAK_FRACTION, "D1", 0.0)  # extension to h / 2 only (the rule kept for the pitch range): 0.39-0.57 at h = 1
    if h == 1.0:
        assert toy_rush(5, 1.90, h) < C.IOU_MIN and toy_rush(6, 1.45, h) < 0.55


def test_detector_json_round_trip_and_hash(tmp_path, pinned_detector):
    det = pinned_detector(2.5)
    save_detector(det, tmp_path / "d.json")
    assert load_detector(tmp_path / "d.json") == json.loads((tmp_path / "d.json").read_text())
    bad = json.loads((tmp_path / "d.json").read_text())
    bad["regimes"]["R1"]["h"]["D2+"] = 3.0
    (tmp_path / "bad.json").write_text(json.dumps(bad))
    with pytest.raises(ValueError, match="hash"):
        load_detector(tmp_path / "bad.json")
    for edit, match in ((lambda d: d["regimes"]["R1"]["h"].pop("D2+"), "threshold entry"), (lambda d: d["regimes"]["R2"]["clip"].pop("D3"), "threshold entry"),
                        (lambda d: d.update(schema=2), "schema"), (lambda d: d.update(schema=3), "schema")):
        broken = json.loads((tmp_path / "d.json").read_text())
        edit(broken)
        (tmp_path / "broken.json").write_text(json.dumps(broken))
        with pytest.raises(ValueError, match=match):
            load_detector(tmp_path / "broken.json")
    with pytest.raises(FileNotFoundError):
        load_detector(tmp_path / "missing.json")
    assert (tmp_path / "d.json").read_text().endswith("\n") and list(json.loads((tmp_path / "d.json").read_text())) == sorted(det)


def test_decode_uses_regime_dims_and_disabled_flags(pinned_detector):
    det = pinned_detector(2.0)
    n = 24
    big = np.full(n, 0.0)
    big[[4, 5]] = 9.0
    d = {k: dim(k, np.full(n, np.nan)) for k in C.DIMS}
    d["D1"] = dim("D1", big)
    d["D6"] = dim("D6", -big)
    comp = comparison(d, n)
    assert {r.dim for r in decode(comp, det["regimes"]["R1"], SENT)} == {"D1", "D6"}
    assert {r.dim for r in decode(comp, det["regimes"]["R2"], SENT)} == {"D1"}  # D6 is displayed, never flagged, in R2
    off = dict(det["regimes"]["R1"], h=dict.fromkeys(KEYS))
    assert decode(comp, off, SENT) == [] and flagged_dims(off) == ()
    assert math.isclose(C.H_GRID[1] - C.H_GRID[0], 0.05)


def test_window_shoulders_of_a_region_open_no_flag_of_their_own():
    x = np.zeros(24)
    x[1:10] = [-0.14, -0.19, -0.5, -0.5, -0.5, -0.5, -0.5, -0.19, -0.14]  # z = 1.4, 1.9, 5 x5, 1.9, 1.4: an edit and its smear
    regs = decode_regions(dim("D5", x), 0.1, 1.0)
    assert [(r.i0, r.i1) for r in regs] == [(3, 7)]


def test_flag_keys_name_every_flagged_direction():
    assert KEYS == ("D1-", "D1+", "D2-", "D2+", "D3-", "D4-", "D5-", "D6-", "D7+", "D8+", "D9-") and key("D1", 1) == "D1+"
    reg = regime("R2", {"D1-": 2.0, "D2+": 3.0})
    assert threshold(reg, "D1", -1) == 2.0 and threshold(reg, "D1", 1) is None and flagged_dims(reg) == ("D1", "D2")


def test_decode_uses_a_different_threshold_for_longer_and_shorter_pauses():
    x = np.full(23, np.nan)
    x[[3, 9]] = [-0.9, 0.9]  # both are z = 6 at s = 0.15
    comp = comparison({**{k: dim(k, np.full(24, np.nan)) for k in C.DIMS}, "D2": dim("D2", x, countable=np.isfinite(x))})
    reg = regime("R1", {"D2-": 3.0, "D2+": 8.0}, enabled=["D2"])
    assert [(r.i0, r.sign) for r in decode(comp, reg, SENT)] == [(3, -1)]  # D2+ needs z >= 8
    reg["h"].update({"D2-": 8.0, "D2+": 3.0})
    assert [(r.i0, r.sign) for r in decode(comp, reg, SENT)] == [(9, 1)]


def comp_with_g(**g):
    d = {k: dim(k, np.zeros(24)) for k in C.DIMS}
    for k, v in g.items():
        d[k].g = v
    return comparison(d)


def test_clip_flags_follow_the_threshold_and_the_direction_rule():
    reg = regime("R1", clip={"D1": math.log(1.25), "D3": math.log(2.0)})
    assert clip_flags(comp_with_g(D1=math.log(1.3), D3=-math.log(2.5)), reg) == pytest.approx({"D1": math.log(1.3), "D3": -math.log(2.5)})
    assert set(clip_flags(comp_with_g(D1=-math.log(1.3)), reg)) == {"D1"}  # tempo: either direction
    assert clip_flags(comp_with_g(D3=math.log(3.0)), reg) == {}  # a wider pitch range is never flagged
    assert clip_flags(comp_with_g(D1=math.log(1.25)), reg) == {}  # not beyond the threshold
    assert clip_flags(comp_with_g(D1=math.log(3.0)), regime("R2", clip={"D1": None, "D3": None})) == {}  # no fitted threshold: no flag


def test_fit_clip_sets_thresholds_at_clip_h_robust_units_and_never_below_the_floor():
    zero = [comp_with_g(D1=0.0, D3=0.0)] * 3
    assert fit_clip(zero) == {k: pytest.approx(C.CLIP_H * C.FLOORS[k], abs=1e-5) for k in C.CLIP_DIMS}
    spread = [comp_with_g(D1=0.5 * (-1) ** i, D3=0.0) for i in range(10)]  # median 0, median |g| 0.5: spread 1.4826 * 0.5
    assert fit_clip(spread)["D1"] == pytest.approx(C.CLIP_H * C.MAD_SCALE * 0.5, abs=1e-5)
    assert fit_clip(spread)["D3"] == pytest.approx(C.CLIP_H * C.FLOORS["D3"], abs=1e-5)


def test_threshold_of_one_flag_key_disables_only_that_direction_of_its_dimension(base, pinned_detector):
    comp = with_x(base, "D5", [(10, 15, -6)])
    comp.dims["D1"].x[10:16] = -0.5
    reg = pinned_detector()["regimes"]["R2"]
    reg["h"].update({"D1-": None, "D1+": None, "D5-": 2.5})
    assert {r.dim for r in decode(comp, reg, base.tr.sentence)} == {"D5"}
    sc = score(comp, decode(comp, reg, base.tr.sentence), reg, C.PMAX_START)
    assert sc.S["D1"] is None and sc.S["D5"] < 100 and sc.S["D2"] == 100
    reg["h"].update({"D1-": 2.0})  # faster is flagged again, slower is not
    assert {(r.dim, r.sign) for r in decode(comp, reg, base.tr.sentence)} == {("D1", -1), ("D5", -1)}
    comp.dims["D1"].x[10:16] = 0.5
    assert {r.dim for r in decode(comp, reg, base.tr.sentence)} == {"D5"}


def test_hash_changes_when_one_threshold_changes(pinned_detector):
    det = pinned_detector()
    before = config_hash(det)
    assert det["schema"] == 4
    det["regimes"]["R2"]["h"]["D5-"] = 2.05
    after_h = config_hash(det)
    det["regimes"]["R2"]["clip"]["D1"] = 0.3
    assert before != after_h != config_hash(det)
