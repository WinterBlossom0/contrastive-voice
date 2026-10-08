import dataclasses

import numpy as np
import pytest
from synth import recording, regime

from cvoice import config as C
from cvoice.compare import compare, time_map, warp
from cvoice.detect import clip_flags, decode


def pair(**kw):
    B = recording(30, pauses={9: 0.7, 19: 0.8})
    return B, dataclasses.replace(B, **kw)


def test_time_map_is_monotone_and_warps_word_boundaries():
    B = recording(30, word_s=0.30)
    P = recording(30, word_s=0.45)
    mp, mb = time_map(B, P)
    assert np.all(np.diff(mp) > 0) and np.all(np.diff(mb) >= 0)
    np.testing.assert_allclose(warp(P.al.start, mp, mb), B.al.start, atol=1e-6)
    np.testing.assert_allclose(warp(P.al.end, mp, mb), B.al.end, atol=1e-6)
    assert warp(mp[0] - 1.0, mp, mb) == pytest.approx(mb[0] - 1.0)  # slope 1 outside
    assert warp(mp[-1] + 2.0, mp, mb) == pytest.approx(mb[-1] + 2.0)


def test_identity_has_zero_deltas():
    B = recording(30, pauses={9: 0.7, 19: 0.8})
    c = compare(B, B)
    for k in ("D1", "D3", "D5", "D6"):
        x = c.dims[k].x
        assert np.nanmax(np.abs(x)) < 1e-9 and np.isfinite(x).sum() > 20
    assert c.dims["D1"].g == pytest.approx(0.0)
    assert np.nansum(np.abs(c.dims["D2"].x)) == 0.0
    assert c.stress_b == c.stress_p


def test_d1_pace_is_window_speech_time_ratio_centred_on_its_median():
    B, _ = pair()
    T = B.win_T.copy()
    T2 = T.copy()
    T2[10:14] *= 0.5  # the participant rushes four windows
    c = compare(B, dataclasses.replace(B, win_T=T2))
    d = c.dims["D1"]
    r = np.log(T2 / T)
    g = np.nanmedian(r)
    assert g == pytest.approx(0.0)
    np.testing.assert_allclose(d.x[10:14], np.log(0.5))
    assert d.g == pytest.approx(g)
    # a uniform slowdown is global tempo, not a regional deviation
    c2 = compare(B, dataclasses.replace(B, win_T=T * 1.6))
    assert c2.dims["D1"].g == pytest.approx(np.log(1.6)) and np.nanmax(np.abs(c2.dims["D1"].x)) < 1e-9


def test_d1_window_excludes_pauses_and_clips_at_sentences():
    B = recording(30, pauses={9: 0.7})
    assert B.tr.sentence[7] == 0 and B.tr.sentence[8] == 1
    assert B.win[0] == (0, 2) and B.win[7] == (5, 7) and B.win[8] == (8, 10) and B.win[15] == (13, 17)
    lo, hi = B.win[10]
    spoken = B.al.end[hi] - B.al.start[lo] - B.sil[lo:hi].sum()
    assert B.sil[9] > 0.5 and B.win_T[10] == pytest.approx(spoken)  # the in-window pause is removed from the speech time


def test_d2_pause_rules():
    B, P = pair()
    sb, sp = np.zeros(29), np.zeros(29)
    sb[3], sp[3] = 0.0, 0.4  # intrusive: no baseline pause, no punctuation
    sb[5], sp[5] = 0.8, 0.1  # dropped: baseline pause >= 0.5
    sb[6], sp[6] = 0.3, 0.0  # shortened but baseline < 0.5 s: neutral
    sb[7], sp[7] = 0.0, 0.5  # intrusive but at a sentence boundary (punctuation): neutral
    sb[8], sp[8] = 0.6, 0.6
    c = compare(dataclasses.replace(B, sil=sb, sil_raw=sb), dataclasses.replace(P, sil=sp, sil_raw=sp))
    d = c.dims["D2"]
    assert d.x[3] == pytest.approx(0.4) and d.countable[3]
    assert d.x[5] == pytest.approx(-0.7) and d.countable[5]
    # x is defined at every eligible boundary (the R2 scale fit sees all of them); countable gates flagging only
    assert d.x[6] == pytest.approx(-0.3) and not d.countable[6]
    assert d.x[7] == pytest.approx(0.5) and not d.countable[7]
    assert d.x[8] == pytest.approx(0.0) and not d.countable[8]  # equal pauses: eligible but nothing to flag
    assert np.isnan(d.x[0])  # not eligible: neither recording has a pause there
    n_events = (sb >= C.PAUSE_MIN_S).sum()
    assert d.w[0] == pytest.approx(1 / n_events)


def test_d3_pitch_is_the_ln_ratio_of_regularised_window_ranges_centred_on_its_median():
    B, _ = pair()
    Rb = np.full(len(B.tr), 6.0)
    Rp = np.full(len(B.tr), 4.0)
    Rp[10:14] = 1.0  # a uniformly narrower participant, flatter still in four windows
    d = compare(dataclasses.replace(B, win_R=Rb), dataclasses.replace(B, win_R=Rp)).dims["D3"]
    g = np.log((4.0 + C.RANGE_REG_ST) / (6.0 + C.RANGE_REG_ST))
    assert d.g == pytest.approx(g) and np.abs(d.x[:10]).max() < 1e-9 and np.abs(d.x[14:]).max() < 1e-9
    np.testing.assert_allclose(d.x[10:14], np.log((1.0 + C.RANGE_REG_ST) / (6.0 + C.RANGE_REG_ST)) - g)
    np.testing.assert_allclose(d.b, Rb)
    np.testing.assert_allclose(d.p, Rp)  # the underlying measures stay in semitones
    # reference(i): the baseline range carried to the participant's overall range, so that p against it is exactly x
    assert d.reference(12) == pytest.approx((1.0 + C.RANGE_REG_ST) / np.exp(d.x[12]) - C.RANGE_REG_ST)
    assert d.reference(2) == pytest.approx(4.0)  # unflagged unit: the participant's own range


def test_d3_is_unchanged_by_scaling_the_participants_ranges_except_for_g():
    B, _ = pair()
    Rb = np.random.default_rng(0).uniform(20.0, 40.0, len(B.tr))  # ranges far above RANGE_REG_ST: the ratio is scale-free
    ds = {c: compare(dataclasses.replace(B, win_R=Rb), dataclasses.replace(B, win_R=c * Rb)).dims["D3"] for c in (1.0, 0.8, 0.5)}
    for c in (0.8, 0.5):
        np.testing.assert_allclose(ds[c].x, ds[1.0].x, atol=0.05)
        assert ds[c].g == pytest.approx(np.log(c), abs=0.05)
    assert ds[1.0].g == pytest.approx(0.0, abs=0.03) and ds[0.5].g < ds[0.8].g < ds[1.0].g


def test_d3_flags_a_locally_flattened_window_and_not_a_uniformly_narrow_or_a_wider_one():
    B, _ = pair()
    Rb = np.full(len(B.tr), 30.0)
    flat = 0.4 * Rb
    flat[10:15] = 0.05 * Rb[10:15]  # 40 % of the range overall, almost none in five windows
    reg = regime("R1", 2.0, enabled=["D3"])
    comp = compare(dataclasses.replace(B, win_R=Rb), dataclasses.replace(B, win_R=flat))
    regs = decode(comp, reg, B.tr.sentence)
    assert [(r.dim, r.sign) for r in regs] == [("D3", -1)] and 10 <= regs[0].peak < 15 and regs[0].i0 >= 9 and regs[0].i1 <= 15
    assert clip_flags(comp, reg) == {"D3": pytest.approx(comp.dims["D3"].g)}  # and the whole clip is narrower than the reference
    uniform = compare(dataclasses.replace(B, win_R=Rb), dataclasses.replace(B, win_R=0.4 * Rb))
    assert decode(uniform, reg, B.tr.sentence) == []  # uniform narrowing is the whole-clip flag, not a local one
    wider = compare(dataclasses.replace(B, win_R=Rb), dataclasses.replace(B, win_R=np.where(np.arange(len(Rb)) == 12, 3 * Rb, Rb)))
    assert decode(wider, reg, B.tr.sentence) == [] and clip_flags(wider, reg) == {}


def test_d4_stress_markers_lost():
    B, _ = pair()
    n = len(B.tr)
    u = np.zeros((n, 3))
    u[:, 0] += np.random.default_rng(0).normal(0, 0.01, n)
    u[5] = [1.0, 6.0, 6.0]
    Bs = dataclasses.replace(B, ws=dataclasses.replace(B.ws, u=u), m=np.zeros(3), sigma=np.asarray(C.STRESS_SIGMA_FLOOR))
    u2 = u.copy()
    u2[5] = 0
    Ps = dataclasses.replace(Bs, ws=dataclasses.replace(Bs.ws, u=u2))
    c = compare(Bs, Ps)
    assert c.stress_b == [5] and c.stress_p == []
    d = c.dims["D4"]
    expected_pb = np.mean([1.0 / C.STRESS_SIGMA_FLOOR[0], 6 / 3, 6 / 3])
    assert d.b[5] == pytest.approx(expected_pb) and d.x[5] == pytest.approx(-expected_pb, abs=0.1)
    assert d.w[5] == 1.0 and np.isnan(d.x[4])


def test_d5_d6_centred_and_signed():
    B, _ = pair()
    E = B.win_E.copy()
    c = compare(B, dataclasses.replace(B, win_E=E - 3.0))  # uniform gain change is not a flaw
    assert np.nanmax(np.abs(c.dims["D5"].x)) < 1e-9
    E2 = E.copy()
    E2[12:15] -= 5.0
    d = compare(B, dataclasses.replace(B, win_E=E2)).dims["D5"]
    np.testing.assert_allclose(d.x[12:15], -5.0)
    Q2 = B.win_Q.copy()
    Q2[12:15] *= np.exp(-0.7)
    d6 = compare(B, dataclasses.replace(B, win_Q=Q2)).dims["D6"]
    np.testing.assert_allclose(d6.x[12:15], -0.7, atol=1e-4)


def test_event_absence_is_valid_measurement_coverage(base):
    comp = compare(base, base)
    assert np.isfinite(comp.dims["D2"].x).mean() < .5
    assert comp.coverage["D2"] == pytest.approx(1) and comp.coverage["D4"] == pytest.approx(1)


def test_pause_coverage_excludes_boundaryless_last_word(base):
    regions = base.regions.copy()
    regions[-1, 1] += 100  # most support duration belongs to the boundaryless word
    raw = np.full_like(base.sil_raw, np.nan)
    B = dataclasses.replace(base, regions=regions, sil_raw=raw)
    comp = compare(B, B)
    assert not np.isfinite(comp.dims["D2"].x).any() and comp.coverage["D2"] == 0
    raw[:10] = 0
    comp = compare(B, B)
    supports = regions[:-1, 1] - regions[:-1, 0]
    assert comp.coverage["D2"] == pytest.approx(supports[:10].sum() / supports.sum())


def test_d3_reference_is_never_negative():
    B = recording(40, pauses={7: 0.7, 19: 0.8})
    comp = compare(B, B)
    d = comp.dims["D3"]
    d.x[10], d.p[10] = 5.0, 0.0  # a regularised ratio this large would put the reference below zero
    assert d.reference(10) == 0.0
