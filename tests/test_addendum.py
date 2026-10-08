"""Evaluation addendum (cvoice.addendum): accounting, formatting, relabelled intervals, label and excluded-span rules."""
import json
from pathlib import Path

import pytest

from cvoice import addendum as A, evaluate as ev
from cvoice.detect import Region
from cvoice.events import on_shortfall
from cvoice.uncertainty import wilson

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'build/work/kaggle_runs/last_run/x'
FIRST_FINAL = ROOT / 'docs/evidence_final_32cdd86f3d6e/results.json'
TEST_ROW = {'split': 'test', 'levels': 'headline (L2+L3)', 'group': 'all', 'tp': 29, 'fp': 5, 'fn': 3, 'f1': 0.879, 'same_change_duplicates': 3,
            'every_prediction': {'false_by_key': {'D1-': 2, 'D3-': 2, 'D9-': 5}, 'same_change_detections': 1}}


def test_tables_print_no_raw_floats_and_name_degenerate_intervals():
    assert [ev.md_cell(v) for v in (wilson(0, 6)[0], 3990.0, 0.390334287, 7, None, 1e-7)] == ['0', '3990', '0.39', '7', '', '0']
    assert ev.md_cell([2.7755575615628914e-17, 0.3903342879021653]) == '[0, 0.39]' and ev.md_cell(3936.0) == '3936'
    assert ev.bounds_text([1.0, 1.0]).startswith('degenerate [1, 1]') and ev.bounds_text([0.2, 0.31], 'Wilson') == 'Wilson [0.2, 0.31]'
    assert ev.interval_text([0.0, 1e-9]).startswith('degenerate') and ev.interval_text([None, None]) == 'n/a'


def test_preregistered_accounting_of_the_test_row():
    assert {k: v for k, v in ev.pre_registered(TEST_ROW).items() if k in ('tp', 'fp', 'fn', 'f1')} == {'tp': 28, 'fp': 9, 'fn': 4, 'f1': 0.812}
    with pytest.raises(ValueError):
        ev.pre_registered({**TEST_ROW, 'same_change_duplicates': 2})


def test_accounting_rows_put_the_preregistered_count_first_beside_the_first_final():
    results = {'headline': {'groups': {'core8': {'by_split_strict': [TEST_ROW]}}}}
    first = {'detector_config_sha256': '32cdd86f', 'headline': {'by_split_strict': [
        {'split': 'test', 'levels': 'headline (L2+L3)', 'group': 'all', 'tp': 29, 'fp': 5, 'fn': 3, 'f1': 0.879, 'accounting': 'all predictions counted'}]}}
    acc = A.accounting_section(results, first, None)
    row = acc['rows'][0]
    assert (row['pre_registered']['f1'], row['count_once']['f1'], row['first_final']['f1']) == (0.812, 0.879, 0.879)
    header = A.accounting_md(acc).splitlines()[0]
    assert header.index('pre-registered F1') < header.index('count-once F1') < header.index('first final F1')


def test_regions_on_an_excluded_span_of_any_dimension_are_dropped():
    excluded = [{'words': [25, 31], 'dim': 'D5'}]
    assert on_shortfall(Region('D1', -1, 23, 27, 25, -3.0, (23, 27)), excluded)
    assert not on_shortfall(Region('D2', 1, 32, 32, 32, 3.0, (32,)), excluded)


def test_r2_expectation_applies_to_level_3_pace_pause_pitch_volume_only():
    edit = lambda typ, lv, reader, hit: {'reader_group': 'check', 'direction': 'away from the reference', 'type': typ, 'level': lv,  # noqa: E731
                                         'clip': f'{reader}__x', 'detected': hit}
    edits = [edit('RUSH', 3, 'a', True), edit('RUSH', 3, 'b', False), edit('RUSH', 3, 'b', False),
             edit('MONOTONE', 3, 'a', True), edit('NATURAL_RUSH', 3, 'a', False), edit('RUSH', 2, 'a', True)]
    rows = {(r['type'], r['level']): r for r in A.r2_by_reader({'cross_speaker': {'modes': {'single': {'edits': edits}}}}, 'single')}
    assert rows[('RUSH', 3)]['per_reader'] == {'a': [1, 1], 'b': [0, 2]} and rows[('RUSH', 3)]['majority_detected'] is False
    assert rows[('MONOTONE', 3)]['majority_detected'] is True and rows[('RUSH', 2)]['majority_detected'] is None
    assert rows[('NATURAL_RUSH', 3)]['majority_detected'] is None and 'listed' in rows[('NATURAL_RUSH', 3)]['expected']


def test_stress_rows_are_regrouped_by_speaker_and_must_reproduce_the_saved_row():
    record = lambda speaker, rec, added, kept: {'split': 'val', 'condition': 'noise', 'regime': 'R1', 'reference_mode': None, 'speaker': speaker,  # noqa: E731
                                                'participant_recording': rec, 'added': added, 'removed': 0, 'minutes': 0.5,
                                                'regions_added': ['D9-'] * added, 'found_before_ids': [0, 1], 'found_before_keys': ['D1-', 'D1-'],
                                                'retained_ids': list(range(kept)), 'flaws_found_before': 2}
    detail = [record('s1', 'r1', 1, 2), record('s1', 'r2', 3, 1), record('s2', 'r3', 0, 2)]
    row = {'split': 'val', 'condition': 'noise', 'regime': 'R1', 'reference_mode': None, 'added_per_min': round(4 / 1.5, 4), 'retained_detections': 5,
           'retention': 5 / 6, 'added_ci95': [1.0, 4.0], 'retention_ci95': [0.5, 1.0], 'added_interval': {'method': 'recording bootstrap'},
           'added_by_key': {'D9-': {}}, 'key_share_per_min': 0.0556}
    out = A.stress_by_speaker({'stress': {'flawed_clips': detail, 'rows': [row]}})[0]
    assert out['added_per_speaker'] == {'s1': 4.0, 's2': 0.0} and out['kept_per_speaker'] == {'s1': 0.75, 's2': 1.0}
    assert out['added_by_key_per_speaker'] == {'D9-': {'s1': 4.0, 's2': 0.0}}
    with pytest.raises(ValueError):
        A.stress_by_speaker({'stress': {'flawed_clips': detail[:2], 'rows': [row]}})


def test_r2_reader_unit_is_stated_per_reference_mode():
    assert 'once per calibration reference' in A.READER_UNIT['single'] and 'median of 5' in A.READER_UNIT['consensus5']


def test_label_summary_counts_title_or_chip_matches_per_tier():
    rows = [{'tier': 'core8', 'split': 'test', 'level': 3, 'type': 'DEEMPHASIS', 'detected_by': 'own key', 'shown_type': 'MONOTONE', 'shown_pattern': None, 'correct': False},
            {'tier': 'core8', 'split': 'test', 'level': 2, 'type': 'RUSH', 'detected_by': 'same change', 'shown_type': 'RUSH', 'shown_pattern': None, 'correct': True},
            {'tier': 'synthetic_only', 'split': 'val', 'level': 3, 'type': 'HESITATION', 'detected_by': 'own key', 'shown_type': 'PAUSE_INTRUSIVE',
             'shown_pattern': 'HESITATION', 'correct': True},
            {'tier': 'core8', 'split': 'val', 'level': 3, 'type': 'FADE', 'detected_by': None, 'shown_type': None, 'shown_pattern': None, 'correct': None}]
    out = A.label_summary(rows)
    assert (out['core8|headline (L2+L3)|test']['correct'], out['core8|headline (L2+L3)|test']['detected']) == (1, 2)
    assert out['core8|headline (L2+L3)|val']['detected'] == 0
    assert out['synthetic_only|headline (L2+L3)|val+test']['confusion'] == {'HESITATION': {'PAUSE_INTRUSIVE (HESITATION chip)': 1}}


@pytest.mark.skipif(not (RUN / 'eval/results.json').exists() or not FIRST_FINAL.exists(), reason='final-run outputs are not in this checkout')
def test_addendum_of_the_final_run():
    add = A.build(RUN, FIRST_FINAL, None)
    test = next(r for r in add['accounting']['rows'] if (r['tier'], r['levels'], r['split']) == ('core8', 'headline (L2+L3)', 'test'))
    assert [test['pre_registered'][k] for k in ('tp', 'fp', 'fn', 'f1')] == [28, 9, 4, 0.812]
    assert (test['count_once']['f1'], test['first_final']['f1']) == (0.879, 0.879)
    saved = RUN / 'eval/addendum.json'
    if saved.exists() and json.loads(saved.read_text()).get('local'):
        local = json.loads(saved.read_text())['local']
        assert all(r['local'] == r['saved'] and r['local_pre_registered'] == r['saved_pre_registered'] for r in local['reproduction'])
        assert all(r['equal'] for r in A.reference_free_reproduction(json.loads((RUN / 'eval/results.json').read_text()), local))


def test_rush_confusion_counts_shown_types_and_undetected_edits():
    rows = [{'type': 'RUSH', 'split': 'val', 'level': 2, 'shown_type': 'RUSH'},
            {'type': 'NATURAL_RUSH', 'split': 'val', 'level': 3, 'shown_type': 'RUSH'},
            {'type': 'NATURAL_RUSH', 'split': 'test', 'level': 3, 'shown_type': None},
            {'type': 'FADE', 'split': 'val', 'level': 3, 'shown_type': 'FADE'}]
    d9 = [{'type': 'RUSH', 'split': 'test', 'shown_type': 'NATURAL_RUSH'}]
    out = A.rush_confusion(rows, d9)
    assert out['val']['detecting_region'] == {'RUSH': {'RUSH': 1}, 'NATURAL_RUSH': {'RUSH': 1}}
    assert out['val+test']['detecting_region']['NATURAL_RUSH'] == {'RUSH': 1, 'not detected': 1}
    assert out['test']['d9_regions'] == {'RUSH': {'NATURAL_RUSH': 1}} and out['train']['detecting_region'] == {}


def test_excluded_summary_counts_regions_clips_and_unclaimed_other_dimensions():
    def row(clip, split, level, key, same, claimed):
        return {'clip': clip, 'split': split, 'level': level, 'key': key, 'same_dimension': same, 'claimed_by_a_truth': claimed,
                'excluded_types': ['LOW_EFFORT']}
    rows = [row('a', 'val', 3, 'D5-', True, False), row('a', 'val', 3, 'D1-', False, False), row('b', 'test', 2, 'D1-', False, True),
            row('c', 'test', 1, 'D3-', False, False)]
    out = {(r['split'], r['levels']): r for r in A.excluded_summary(rows)}
    head = out[('val+test', 'headline (L2+L3)')]
    assert (head['regions'], head['clips'], head['other_dimension'], head['other_dimension_unclaimed']) == (3, 2, 2, 1)
    assert head['by_key'] == {'D1-': 2, 'D5-': 1} and head['by_excluded_type'] == {'LOW_EFFORT': 3}
    assert out[('test', 'sensitivity (L1)')]['regions'] == 1 and out[('train', 'headline (L2+L3)')]['regions'] == 0


def test_fair_reference_free_fits_its_own_scales_and_chooses_h_by_the_detector_objective(monkeypatch, pinned_detector):
    from synth import recording

    from cvoice import calibrate
    from cvoice.compare import compare
    from cvoice.detect import fit_scales
    B = recording(30, pauses={7: 0.7, 19: 0.8})
    nulls = [A.NullWithP(f'n{i}', compare(B, P), (), 1.0, 'train', 'r', P)
             for i, P in enumerate([B, recording(30, pauses={7: 0.5, 19: 0.9}), recording(30, word_s=0.33)])]
    seen = {}

    def select(pairs, controls, regime, floor):
        seen.update(regime=regime, controls=len(controls), floor=floor)
        return [{'h': 2.0, 'natural_rush_h': 1.0, 'TP': 4, 'FP': 2, 'FN': 2, 'F1': 0.667, 'control_regions': 0},
                {'h': 3.0, 'natural_rush_h': 1.0, 'TP': 4, 'FP': 2, 'FN': 2, 'F1': 0.667, 'control_regions': 0},
                {'h': 2.5, 'natural_rush_h': 1.0, 'TP': 3, 'FP': 3, 'FN': 3, 'F1': 0.5, 'control_regions': 0}]
    monkeypatch.setattr(calibrate, 'select_r1', select)
    monkeypatch.setattr(ev, 'clip_runs', lambda ds, det, clips: [])
    ds = type('DS', (), {'clips': lambda self, kind: []})()
    out = A.fair_reference_free(ds, pinned_detector(), (nulls, nulls[:1]))
    own = fit_scales([ev.reference_free(n.comp, n.P) for n in nulls])[0]
    assert out['scales'] == {k: round(v, 6) for k, v in own.items()} and seen['regime']['scales'] == out['scales']
    assert seen['controls'] == 1 and out['d9_noise_floor_ln'] == seen['floor']
    assert out['train']['h'] == 2.0 and not out['at_grid_edge']   # an F1 tie takes the smaller h
