"""Owner decisions O1 (word-time D9) and O2 (one detection per change), and the v12 verifier follow-ups."""
import dataclasses
import inspect
import math
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
from synth import label, local, recording, regime, with_x

from cvoice import calibrate, config as C, evaluate, explain, patterns
from cvoice.calibrate import Null, select_r1
from cvoice.compare import compare
from cvoice.events import Run, eval_clip
from cvoice.features import recording_arrays
from cvoice.lab.extract import recording_view
from cvoice.protocol import STRICT_ACCOUNTING, exemption_policy
from cvoice.reference import consensus_reference
from cvoice.score import score

R1_ENABLED = tuple(C.REGIME_DIMS['R1'])
APP_JS = Path(evaluate.__file__).with_name('static') / 'app.js'


def _run(base, comp, regions=()):
    return Run(base, base, comp, list(regions), score(comp, [], regime('R1'), C.PMAX_START), 'R1', {},
               regime('R1')['scales'], R1_ENABLED)


# ------------------------------------------------------------------------------------------------ O1: D9 measure
def test_d9_is_the_ln_ratio_of_aligned_word_time_when_the_pauses_are_kept():
    B = recording(40, pauses={7: 0.7, 19: 0.8})
    P = recording(40, pauses={7: 0.7, 19: 0.8}, word_s=0.25)  # every word 0.21 s instead of 0.26 s; gaps and pauses kept
    d9 = compare(B, P).dims['D9']
    ok = np.isfinite(d9.x)
    assert ok.any() and d9.x[ok] == pytest.approx(math.log(0.21 / 0.26), abs=1e-9)
    assert d9.g == pytest.approx(math.log(0.21 / 0.26), abs=1e-9)


def test_consensus_reference_takes_the_median_window_word_time(base):
    refs = [dataclasses.replace(base, win_W=base.win_W * f) for f in (1., 1.1, 1.2, 1.3, 20.)]
    assert consensus_reference(refs).win_W == pytest.approx(base.win_W * 1.2, nan_ok=True)


def test_lab_recording_view_carries_the_word_time_of_the_alignment(base):
    view = recording_view({k: v for k, v in recording_arrays(base).items()})
    assert view.win_W == pytest.approx(base.win_W, nan_ok=True)
    assert np.nanmax(np.abs(compare(view, view).dims['D9'].x)) == 0.0


def test_d9_evidence_is_the_aligned_word_time_of_the_peak_window(base):
    P = recording(40, pauses={7: 0.7, 19: 0.8}, word_s=0.25)
    comp = compare(base, P)
    info = patterns.describe(local('D9', 10, 15, -6), comp, base, P, {'natural_rush': True})
    values = {e['key']: e['value'] for e in info['evidence']}
    # K1: the reference has no paired pause time around the span, so the region is part of the RUSH change
    assert info['pattern'] is None and info['type'] == 'RUSH'
    assert set(values) == {'word_time_ln', 'word_time_p_s', 'word_time_b_s', 'pause_p_s', 'pause_b_s'}
    assert values['word_time_p_s'] == comp.dims['D9'].p[10] and values['word_time_b_s'] == comp.dims['D9'].b[10]
    assert values['word_time_p_s'] != pytest.approx(P.win_T[10]) and values['word_time_ln'] == comp.dims['D9'].x[10]


def test_d9_explanation_says_the_words_were_faster(base):
    comp = with_x(base, 'D9', [(10, 15, -0.3)])
    region = local('D9', 10, 15, -6)
    reg = regime('R1')
    sc = score(comp, [region], reg, C.PMAX_START)
    flaw = explain.build(region, comp, base, base, reg, sc.masses[0], sc, 'f')
    assert 'The words themselves were spoken faster' in flaw['text'] and 'pauses are reported separately' not in flaw['text']
    assert 'aligned word durations' in flaw['measure'] and 'pause-free' not in flaw['text'].lower()


# ------------------------------------------------------------------------------------------------ O2: duplicates
def test_strict_headline_counts_one_detection_per_change_and_reports_duplicates(base, pinned_detector, monkeypatch):
    clips = [{"id": "rush", "split": "val", "level": 2, "parent": "s", "kind": "single", "spectrum": "core8"}]
    run = _run(base, compare(base, base), [local('D1', 10, 15, -5), local('D9', 10, 15, -9)])
    monkeypatch.setattr(evaluate, "clip_runs", lambda ds, det, cl: [(c, run, label(base, 'RUSH', (10, 15))) for c in cl])
    out = evaluate.headline_section(SimpleNamespace(clips=lambda **kw: clips), pinned_detector(), ("val",))
    core = out['groups']['core8']
    for field in ('by_split_strict', 'by_split'):
        rows = [r for r in core[field] if r['levels'] == 'headline (L2+L3)' and r['split'] == 'val']
        assert {r['group'] for r in rows} == {'D1-', 'all'}
        assert all(r['tp'] == 1 and r['fp'] == 0 and r['same_change_duplicates'] == 1 for r in rows)
    assert all(r['accounting'] == STRICT_ACCOUNTING for r in core['by_split_strict'])
    speech = core['per_speech'][0]
    assert speech['strict_false_regions'] == 0 and speech['same_change_duplicates'] == 1
    for table in (out['table_f1'], core['table_f1'], core['table_per_speech']):
        assert 'same-change duplicates' in table and 'all predictions counted' not in table
    assert STRICT_ACCOUNTING in exemption_policy()['scope']


def test_no_strict_label_says_that_every_prediction_is_counted():
    source = inspect.getsource(evaluate)
    assert 'all predictions counted' not in source and '(all counted)' not in source
    assert source.count('STRICT_ACCOUNTING') >= 6


def test_select_r1_reports_same_change_duplicates_beside_its_counts(base, monkeypatch):
    monkeypatch.setattr(C, 'H_GRID', (1.0, 2.0))
    comp = with_x(base, 'D9', [(10, 15, -0.6)])
    comp.dims['D1'].x[10:16] = -0.5
    reg = regime('R1')
    curve = select_r1([(_run(base, comp), label(base, 'RUSH', (10, 15)))], [], reg)
    # K2: the D9 region detects the rush when D1 is not decoded (speech-tempo component), so it is never a duplicate there.
    assert all(row['same_change_duplicates'] == 0 and row['FP'] == 0 for row in curve)
    assert STRICT_ACCOUNTING in reg['selected_operating_point']['objective']


# ------------------------------------------------------------------------------------------------ follow-ups
def test_same_change_uses_one_half_window_test_in_scoring_display_and_evaluation(base):
    comp = compare(base, base)
    regions = [local('D1', 10, 15, -5), local('D9', 17, 20, -6)]  # the D9 region starts two words after the D1 region
    assert [(g.pattern, g.members) for g in patterns.groups(comp, regions)] == [('RUSH', (0, 1))]
    assert patterns.counted(comp, regions, [1., 9.]) == {0}
    ev = eval_clip(_run(base, comp, regions), label(base, 'RUSH', (10, 15)), secondary_exempt=False)
    assert ev['false'] == [] and [(d['group'], d['change'], d['units']) for d in ev['duplicates']] == [('D9-', 'D1-', [17, 20])]
    beyond = [local('D1', 10, 15, -5), local('D9', 18, 21, -6)]
    assert patterns.groups(comp, beyond) == []
    assert len(eval_clip(_run(base, comp, beyond), label(base, 'RUSH', (10, 15)), secondary_exempt=False)['false']) == 1


def test_d9_member_of_a_rush_group_is_shown_as_rushed(base):
    comp = with_x(base, 'D9', [(10, 15, -0.3)])
    comp.dims['D1'].x[10:16] = -0.5
    regions = [local('D1', 10, 15, -5), local('D9', 10, 15, -6)]
    reg = {**regime('R1'), 'pattern_labels': {'natural_rush': True}}
    info = patterns.annotate(comp, regions, base, base, reg['pattern_labels'])
    assert info[1]['group_pattern'] == 'RUSH' and info[1]['type'] == 'RUSH' and info[1]['pattern'] is None
    sc = score(comp, regions, reg, C.PMAX_START)
    flaw = explain.build(regions[1], comp, base, base, reg, sc.masses[1], sc, 'f', info[1])
    assert flaw['type'] == 'RUSH' and flaw['pattern'] is None and flaw['group_pattern'] == 'RUSH'
    alone = patterns.annotate(comp, regions[1:], base, base, reg['pattern_labels'])[0]
    assert alone['pattern'] is None and alone['type'] == 'RUSH'  # K1: no paired pause time, so not natural rushing
    pattern_text = APP_JS.read_text().split('const PATTERN_TEXT = {', 1)[1].split('};', 1)[0]
    assert 'RUSH: "Rushed"' in pattern_text


def test_fit_r2_records_a_whole_clip_threshold_set_by_the_clip_budget_quantile(base):
    nulls = [Null(f'n{i}', compare(base, base), base.tr.sentence, 1.0) for i in range(40)]
    for n in nulls[:2]:  # 5 % of the null clips are a third of the reference tempo: above the 2.5 % clip share
        n.comp.dims['D1'].g = -math.log(3.0)
    reg, _ = calibrate.fit_r2(nulls, full_curve=False)
    assert reg['null']['clip_threshold_choice']['D1']['clip_budget_quantile'] == pytest.approx(math.log(3.0))
    assert reg['clip']['D1'] == pytest.approx(math.log(3.0))


def test_cross_section_qualifies_the_select_rate_columns_with_their_sources(base):
    ids = [f'cal{i}' for i in range(6)]
    entries = [dict(id=i, role='reader_calibration') for i in ids] + [dict(id='check', role='reader_check')]
    clip = dict(id='check__natural', baseline=ids[0], parent='check', split='check', regime='R2')
    lab = label(base, 'NATURAL_RUSH', (10, 15))

    class DS:
        manifest = {'readers': entries}
        def clips(self, **kw): return [clip]
        def entry(self, kind, id): return {'id': id}
        def any_entry(self, id): return {'id': id}
        def parent_entry(self, c): return {'id': c['parent']}
        def rec(self, e): return base
        def recs(self, entries): return [base for e in entries]
        def clip_recs(self, clips): return [base for c in clips]
        def load(self, **kw): pass
        def labels(self, c): return lab

    single, consensus = regime('R2'), regime('R2', 4.)
    single['reference_mode'], consensus['reference_mode'] = 'single', 'consensus5'
    from cvoice.detect import make_detector
    det = make_detector({'R1': regime('R1'), 'R2': single, 'R2_consensus': consensus}, C.PMAX_START, {'calibrated': False})
    scope = 'consensus select rates cover accent with equal source weights; poetry is not covered: no consensus readers'
    det['report'] = {'R2_modes': {'single': {'select': {'total_local': {'sources': ['accent', 'poetry']}}},
                                  'consensus5': {'select': {'scope': scope, 'local_by_key': {'D9-': {'rate': 0.1, 'sources': ['accent']}}}}}}
    result = evaluate.cross_section(DS(), det, ('val',))
    assert result['select_scope'] == {'single': 'select rates cover accent, poetry', 'consensus5': scope}
    assert '| select sources |' in result['table'] and 'Select rate scope: single: select rates cover accent, poetry; consensus5: ' + scope in result['table']
