"""D9 pause rule and RUSH duplicates, consensus select weights, budget status, gallery truth markers."""
import math
from types import SimpleNamespace

import numpy as np
import pytest
from runs import r1_run
from synth import label, local, recording, regime, with_x

from cvoice import audio, calibrate, config as C, evaluate, gallery, patterns, r2pool, stress
from cvoice.calibrate import Null, null_check, select_r1
from cvoice.compare import compare
from cvoice.events import Run, eval_clip, run_pair
from cvoice.score import score

def test_d9_reads_only_aligned_word_durations():
    # Same words; the pauses and gaps differ (a 0.3 s pause cut below PAUSE_MIN_S, longer gaps), the word durations do not.
    B = recording(40, pauses={7: 0.7, 19: 0.8, 12: 0.3})
    P = recording(40, pauses={7: 0.4, 19: 1.2, 12: 0.12}, gap_s=0.1)
    d9 = compare(B, P).dims['D9']
    words = [w for w in B.win if w is not None]
    assert np.nanmax(np.abs(d9.x)) < 1e-12
    assert d9.p[np.isfinite(d9.p)] == pytest.approx([np.sum(P.al.end[a:b + 1] - P.al.start[a:b + 1]) for a, b in words])
    assert abs(d9.g) < 1e-12


def test_d9_region_on_a_rush_edit_is_a_duplicate_not_a_false_region(base):
    comp = compare(base, base)
    run = r1_run(base, comp, scored=False).with_regions([local('D1', 10, 15, -5), local('D9', 10, 15, -9)])
    for strict in (False, True):
        ev = eval_clip(run, label(base, 'RUSH', (10, 15)), secondary_exempt=not strict)
        assert ev['false'] == [] and ev['duplicate'] == 1
    # Away from the RUSH words the same D9 region stays a false region.
    far = r1_run(base, comp, scored=False).with_regions([local('D9', 30, 35, -9)])
    assert len(eval_clip(far, label(base, 'RUSH', (10, 15)), secondary_exempt=False)['false']) == 1


def test_natural_rush_h_is_not_set_by_d9_firing_on_rush_edits(base, monkeypatch):
    monkeypatch.setattr(C, 'H_GRID', (1.0, 2.0, 5.0, 13.0))
    pairs = []
    for _ in range(3):  # RUSH edits: D1 finds them and D9 fires far above the NATURAL_RUSH evidence
        comp = with_x(base, 'D9', [(10, 15, -0.6)])
        comp.dims['D1'].x[10:16] = -0.5
        pairs.append((r1_run(base, comp, scored=False), label(base, 'RUSH', (10, 15))))
    comp = with_x(base, 'D9', [(25, 30, -0.15)])  # z about 3 at the D9 floor scale
    pairs.append((r1_run(base, comp, scored=False), label(base, 'NATURAL_RUSH', (25, 30))))
    reg = regime('R1')
    select_r1(pairs, [], reg)
    assert reg['selected_operating_point']['per_type_recall']['NATURAL_RUSH'] == 1.0
    assert reg['h']['D9-'] <= 2.0 and reg['selected_operating_point']['FP'] == 0


def test_d1_and_d9_on_the_same_words_form_one_rush_group_with_one_penalty(base):
    comp = compare(base, base)
    regions = [local('D1', 10, 15, -5), local('D9', 11, 14, -6), local('D9', 30, 33, -6)]
    assert [(g.pattern, g.members) for g in patterns.groups(comp, regions)] == [('RUSH', (0, 1))]
    assert patterns.counted(comp, regions, [1., 9., 1.]) == {0, 2}  # the D1 region carries the group's penalty


def _null(base, source, minutes=4.0, clip_g=None):
    comp = compare(base, base)
    if clip_g is not None:
        comp.dims['D1'].g = clip_g
    return Null(f'r>{source}', comp, base.tr.sentence, minutes, 'select', f'{source}:t', f'{source}:p', f'{source}:r', source)


def _pool(select_sizes):
    groups = [{'id': f'{source}:{i}', 'source': source, 'entries': [{'id': f'{source}{i}r{k}', 'reader_id': f'{source}:{i}:{k}'} for k in range(n)],
               'sets': {'fit': [], 'select': [f'{source}{i}r{k}' for k in range(n)], 'lockbox': []}}
              for source, sizes in select_sizes.items() for i, n in enumerate(sizes)]
    return {'groups': groups, 'split_sha256': r2pool.partition_hash(groups), 'seed': 1, 'references_per_participant': C.CONSENSUS_K}


def test_consensus_select_weights_the_sources_that_have_consensus_rows(base):
    r2c = {**regime('R2', 2.0), 'null': {}, 'weighting': {'source_weights': dict.fromkeys(('accent', 'ears', 'poetry'), 1 / 3)}}
    nulls = [_null(base, 'accent'), _null(base, 'ears', clip_g=-math.log(3.0))]
    availability = calibrate.consensus_availability(_pool({'accent': [6], 'ears': [7], 'poetry': [5, 3]}), 'select')
    out = calibrate.consensus_select_report(r2c, nulls, availability)['null']
    assert out['total_local']['rate'] == 0.0 and out['total_local']['budget_status'] == 'met on covered sources only'
    assert not out['total_local']['budget_holds_point'] and not out['total_local']['budget_holds_upper95']
    assert out['source_weights'] == {'accent': 0.5, 'ears': 0.5}
    assert set(out['uncovered_sources']) == {'poetry'}
    assert out['clip_by_key']['D1']['rate'] == pytest.approx(0.5) and out['false_clip_flags_per_clip'] == pytest.approx(0.5)
    assert r2c['weighting']['source_weights']['poetry'] == pytest.approx(1 / 3)  # the fit weights stay unchanged


def test_consensus_select_scope_names_its_sources_and_the_counted_cause_of_a_gap(base):
    r2c = {**regime('R2', 2.0), 'null': {}, 'weighting': {'source_weights': dict.fromkeys(('accent', 'poetry'), 0.5)}}
    availability = calibrate.consensus_availability(_pool({'accent': [6], 'poetry': [5, 3, 0]}), 'select')
    assert availability['poetry'] == {'texts': 3, 'readers_per_text': [0, 3, 5], 'max_distinct_references': 4,
                                      'references_per_participant': C.CONSENSUS_K}
    assert availability['accent']['max_distinct_references'] == C.CONSENSUS_K
    out = calibrate.consensus_select_report(r2c, [_null(base, 'accent')], availability)['null']
    reason = out['uncovered_sources']['poetry']
    assert 'no consensus readers' in reason and '0-5 readers of the set' in reason and 'at most 4 distinct' in reason
    assert out['budget_statement'] == ('consensus select rates cover accent with equal source weights; poetry is not covered: ' +
                                       reason + '. over the covered sources only, 0.5/min budget holds at the point rate; upper95 '
                                       'does not establish the budget')
    assert out['total_local']['scope'] == out['scope'] and out['total_local']['budget_status'] == 'met on covered sources only'


def test_consensus_gap_names_the_draw_count_when_a_text_has_enough_readers():
    pool = {**_pool({'ears': [8, 4]}), 'references_per_participant': C.CONSENSUS_K - 2}
    reason = calibrate.consensus_gap(calibrate.consensus_availability(pool, 'select')['ears'])
    assert reason.startswith(f'no consensus readers: each reader draws {C.CONSENSUS_K - 2} references')
    assert f'at most {C.CONSENSUS_K - 2} distinct' in reason and 'select readers each' not in reason


def test_unmeasured_clip_rate_and_budget_are_reported_as_not_measurable(base):
    reg = {**regime('R2', 2.0), 'null': {}, 'weighting': {'source_weights': dict.fromkeys(('accent', 'poetry'), 0.5)}}
    null_check(reg, [_null(base, 'accent', clip_g=-math.log(3.0))])
    assert reg['null']['false_clip_flags_per_clip'] is None
    assert reg['null']['total_local']['budget_status'] == 'not measurable'
    assert 'not measurable' in reg['null']['budget_statement'] and 'poetry' in reg['null']['budget_statement']


def test_budget_status_separates_not_met_from_not_measurable(base):
    busy = with_x(base, 'D5', [(10, 15, -6), (25, 30, -6)])
    reg = {**regime('R2', 2.0), 'null': {}}
    null_check(reg, [Null('a>b', busy, base.tr.sentence, 1.0, group='accent:t', reader='p', source='accent')])
    assert reg['null']['total_local']['budget_status'] == 'not met'
    assert 'is not met at the point rate' in reg['null']['budget_statement']
    r1 = {**regime('R1', 2.0), 'null': {}}
    null_check(r1, [Null('b__identity', compare(base, base), base.tr.sentence, base.duration / 60, 'train', reader='b')])
    assert r1['null']['total_local']['budget_status'] == 'not measurable'
    assert 'independent recording-minutes' in r1['null']['budget_statement']


def test_gallery_truth_marker_of_an_unscored_dimension_is_not_available(base, monkeypatch):
    comp = compare(base, base)
    reg = regime('R2')
    assert 'D7' not in reg['enabled']
    run = Run(base, base, comp, [], score(comp, [], reg, C.PMAX_START), 'R2', {}, reg['scales'], tuple(reg['enabled']))
    monkeypatch.setattr(gallery, 'run_pair', lambda *a: run)
    lab = label(base, 'WORD_REPETITION', (10, 10))
    out = gallery.truth_markers(lab, base, base, {'regimes': {'R2': reg}}, 'R2', {'flaws': [], 'differences': []})
    assert [t['available'] for t in out] == [False]
    assert out[0]['detector_status'] == 'unscored'


def test_fit_r2_records_which_rule_sets_each_whole_clip_threshold(base):
    reg, _ = calibrate.fit_r2([Null(f'n{i}', compare(base, base), base.tr.sentence, 1.0) for i in range(3)], full_curve=False)
    choice = reg['null']['clip_threshold_choice']
    assert set(choice) == {'D1', 'D3'}  # the fit clip-budget quantile, floored, sets each whole-clip threshold
    assert all(row['threshold'] == reg['clip'][k] == pytest.approx(max(row['clip_budget_quantile'], C.FLOORS[k]), abs=1e-6)
               and row['robust_start'] is not None for k, row in choice.items())


def test_r2_dev_v9_table_gives_the_check_null_exposure():
    row = {'key': 'D1-', 'fitted': True, 'h': 4.45, 'detected_by_type': {}, 'null_per_min': 0.0, 'null_regions': 0}
    out = evaluate.r2_dev_v9_change({'minutes': 1.293, 'rows': [row]})
    assert out['rows'][0]['current_null_minutes'] == 1.293 and out['rows'][0]['current_null_regions'] == 0
    assert 'current null comparison-minutes' in out['table']


def test_dev_v9_table_does_not_claim_that_a_higher_h_only_removes_regions():
    table = evaluate.dev_v9_change({'groups': {'core8': {'by_split_strict': []}}})['table']
    assert 'can only remove regions' not in table and 'measured at an h that was not chosen for L1' in table


def test_headline_qualifies_recovered_families_and_fills_the_clip_column(base, pinned_detector, monkeypatch):
    clips = [{"id": t, "split": "val", "level": 2, "parent": "s", "kind": "single", "spectrum": spectrum}
             for t, spectrum in (("FADE", "core8"), ("LOW_EFFORT", "extra"))]
    comp = compare(base, base)
    run = r1_run(base, comp, [local('D5', 10, 15, -5)])
    monkeypatch.setattr(evaluate, "clip_runs", lambda ds, det, cl: [(c, run, label(base, typ=c["id"])) for c in cl])
    out = evaluate.headline_section(SimpleNamespace(clips=lambda **kw: clips), pinned_detector(), ("val",))
    assert 'LOW_EFFORT' in out['recovered_types'] and out['recovered_label_off'] == ['LOW_EFFORT']
    assert 'not by product pattern label' in out['table_f1'] and 'switched off for: LOW_EFFORT' in out['table_f1']
    assert '| val | 0 | none |' in out['groups']['core8']['table_clip']


def test_stress_rows_name_the_reference_mode_and_the_missing_consensus_coverage(base, pinned_detector, monkeypatch):
    clips = [dict(id='c0', parent='s0', split='train', kind='single', regime='R1')]
    det = pinned_detector()
    ref = run_pair(base, base, det, 'R1')
    ds = SimpleNamespace(manifest={'baselines': [dict(id=f's{i}', split='train') for i in range(3)]}, pool=None,
                         clips=lambda **kw: clips, recs=lambda rows: [base] * len(rows), prepare_many=lambda items: [base] * len(items))
    monkeypatch.setattr(evaluate, 'reader_ids', lambda *args: [])
    monkeypatch.setattr(evaluate, 'clip_runs', lambda *args: [(c, ref, {'flaws': []}) for c in clips])
    monkeypatch.setattr(stress, 'MATRIX', [('white noise 20 dB SNR', stress.noise)])
    monkeypatch.setattr(stress, 'apply', lambda fn, w, seed: audio.quantize(w))
    out = evaluate.stress_section(ds, det, ('train',))
    assert out['rows'] and all('reference_mode' in r and r['reference_mode'] is None for r in out['rows'] if r['regime'] == 'R1')
    assert 'the check readers (no injected flaw, so no retention) are measured with the single and the median-of-five references' in out['table']
