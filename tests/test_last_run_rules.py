import math
from types import SimpleNamespace

import numpy as np
import pytest
from synth import label, local, regime, with_x
from test_dev_v12_owner import _run

from cvoice import calibrate, config as C, patterns
from cvoice.compare import compare
from cvoice.events import eval_clip, false_change_duplicates


def _pause_comp(b, p, x, n=30):
    """D2 reference / participant pause time b, p (s) at boundary 12 and D9 x at every word."""
    d2b, d2p = np.zeros(n), np.zeros(n)
    d2b[12], d2p[12] = b, p
    return SimpleNamespace(dims={'D2': SimpleNamespace(b=d2b, p=d2p), 'D9': SimpleNamespace(x=np.full(n, x))})


def test_natural_rush_needs_reference_pauses_that_shrank_with_the_words():
    region = local('D9', 10, 14, -6)
    assert patterns.natural_rush(_pause_comp(0.4, 0.2, math.log(0.8)), region)  # p/b 0.5 < min(0.8, 0.775)
    assert not patterns.natural_rush(_pause_comp(0.4, 0.4, math.log(0.8)), region)  # pauses kept: RUSH
    assert not patterns.natural_rush(_pause_comp(0.4, 0.28, math.log(0.6)), region)  # p/b 0.7 above the word ratio 0.6
    assert not patterns.natural_rush(_pause_comp(0.4, 0.31, math.log(0.5)), region)  # p/b 0.775 not below the cap
    assert not patterns.natural_rush(_pause_comp(C.PAUSE_MIN_S / 2, 0.0, math.log(0.8)), region)  # no pause evidence
    assert C.NATURAL_RUSH_PAUSE_KEPT_MAX == pytest.approx(math.sqrt(0.6), abs=1e-3)


def test_d9_under_a_whole_clip_d1_flag_is_one_rush_change_with_one_penalty(base):
    comp = compare(base, base)
    regions = [local('D9', 10, 12, -3), local('D2', 30, 30, -3)]
    clip = {'D1': -0.3}
    group = next(g for g in patterns.groups(comp, regions, clip) if 0 in g.members)
    assert group.pattern == 'RUSH' and group.anchor == 'D1- whole clip'
    assert 0 not in patterns.counted(comp, regions, [1., 1.], clip)
    assert patterns.rush_type(comp, regions, clip, 0) == 'RUSH'


def test_d9_only_change_has_one_detection_in_scoring_display_and_evaluation(base):
    comp = compare(base, base)
    regions = [local('D9', 10, 12, -3), local('D9', 14, 16, -6)]
    group, = patterns.groups(comp, regions)
    detection, duplicates = patterns.count_once(comp, regions, {}, 'D1-', (10, 16))
    assert group.anchor == detection == 1 and duplicates == (0,)
    assert patterns.counted(comp, regions, [1., 1.]) == {1}
    non_duplicates = set(range(len(regions))) - {d['index'] for d in false_change_duplicates(comp, regions, {})}
    assert non_duplicates == patterns.counted(comp, regions, [1., 1.])


def test_d9_h_grid_stays_above_the_alignment_noise_floor(base, monkeypatch):
    monkeypatch.setattr(C, 'H_GRID', (1.0, 2.0, 3.0, 4.0))
    comp = with_x(base, 'D9', [(10, 15, -0.6)])
    reg = regime('R1')
    floor = 2.5 * reg['scales']['D9']
    calibrate.select_r1([(_run(base, comp), label(base, 'NATURAL_RUSH', (10, 15)))], [], reg, floor)
    chosen = reg['natural_rush_selection']
    assert chosen['grid_min_h'] == 3.0 and reg['h']['D9-'] * reg['scales']['D9'] > floor
    assert chosen['threshold_ln'] == pytest.approx(reg['h']['D9-'] * reg['scales']['D9'])


def test_d9_severity_saturates_at_the_rush_l3_ratio():
    assert C.X_SAT['D9'] == pytest.approx(math.log(1.90)) == pytest.approx(C.X_SAT['D1'])


def test_lockbox_is_read_only_by_the_final_task():
    with pytest.raises(ValueError):
        calibrate.lockbox_null_report(SimpleNamespace(manifest={'r2_pool': {}}), {}, final=False)
    with pytest.raises(ValueError):
        calibrate.grouped_nulls(SimpleNamespace(manifest={'r2_pool': {}}), 'lockbox')


def test_whole_passage_edit_is_detected_by_its_own_whole_clip_flag(base):
    comp = compare(base, base)
    regions = [local('D9', 10, 12, -3)]
    run = _run(base, comp, regions)
    run.clip = {'D1': -0.3}
    ev = eval_clip(run, label(base, 'RUSH', (0, len(base.tr) - 1)), secondary_exempt=False)
    rush = next(t for t in ev['truth'] if t['type'] == 'RUSH')
    assert rush['detected'] and rush['detected_by'] == 'whole clip'
    assert ev['false'] == [] and ev['false_clip'] == [] and [d['index'] for d in ev['duplicates']] == [0]
