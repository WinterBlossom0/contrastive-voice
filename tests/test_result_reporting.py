"""Reporting of saved results: tables rendered from a saved results.json, stress rows with speakers as clusters,
the evaluation panel texts, off-truth findings in a gallery description, and the window and aligner caveats of a finding."""
import dataclasses
import json
import re
from pathlib import Path

import numpy as np
import pytest
from synth import local, with_x

from cvoice import config as C, evaluate as ev, explain, gallery
from cvoice.score import score

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'build/work/kaggle_runs/last_run/x'
FIRST_FINAL = ROOT / 'docs/evidence_final_32cdd86f3d6e/results.json'
GALLERY = ROOT / 'gallery'
needs_run = pytest.mark.skipif(not (RUN / 'eval/results.json').exists(),
                               reason='the final-run folder (build/, git-ignored) is not distributed with the repository')
ROW = {'split': 'test', 'levels': 'headline (L2+L3)', 'group': 'all', 'tp': 29, 'fp': 5, 'fn': 3, 'f1': 0.879, 'same_change_duplicates': 3,
       'accounting': 'one detection per change', 'f1_ci95': [None, None], 'f1_per_speaker': {'a': 0.848, 'b': 0.909}, 'f1_range': [0.848, 0.909],
       'every_prediction': {'false_by_key': {'D1-': 2, 'D3-': 2, 'D9-': 5}, 'same_change_detections': 1}}


def minimal_results(table_f1: str) -> dict:
    return {'detector_config_sha256': 'c' * 64, 'splits': ['train', 'val', 'test'], 'alignment_device': 'cpu', 'final': True,
            'n': {'test': {'speakers': 2, 'clips': 1, 'trials_per_type_level': {'RUSH': {'1': 1}}}},
            'expectation_table': {'R1': {str(lv): 'flagged' for lv in C.LEVELS}, 'R2': {str(lv): 'flagged' for lv in C.LEVELS}},
            'calibration_policy': {}, 'exemptions': {}, 'real_validation': {},
            'headline': {'groups': {'core8': {'by_split_strict': [ROW], 'by_split': []}}, 'table_f1': table_f1,
                         **{k: '' for k in ('table_overlap', 'table_per_speech', 'table_clip', 'table_pause', 'table_onset', 'table_matching',
                                            'table_truth_counts', 'table_magnitude', 'table_activation')}},
            'stress': {'table': '| 95% recording [1.0, 1.0] | 0.30000000000000004 | 2.7755575615628914e-17 | 1.0.2 | d5935d3f |'}}


def test_f1_table_gives_the_preregistered_row_before_the_count_once_row():
    lines = [line for line in ev.f1_table({'core8': {'by_split_strict': [ROW], 'by_split': []}}).splitlines() if line.startswith('| core8')]
    assert ev.PRE_REGISTERED in lines[0] and 'introduced after the plan' in lines[1]
    assert lines[0].split(' | ')[5:10] == ['28', '9', '0', '4', '0.812'] and lines[1].split(' | ')[5:10] == ['29', '5', '3', '3', '0.879']


def test_tables_markdown_rebuilds_the_f1_table_prints_the_count_once_rule_and_formats_raw_floats():
    md = ev.tables_markdown(minimal_results('| old table |\n\nRecipe families recovered: RUSH.'))
    assert ev.COUNT_ONCE_RULE in md and '| old table |' not in md and 'Recipe families recovered: RUSH.' in md
    assert md.index(ev.PRE_REGISTERED) < md.index('introduced after the plan')
    assert 'degenerate [1, 1]' in md and '| 0.3 | 0 | 1.0.2 | d5935d3f |' in md and 'e-17' not in md


def test_format_floats_keeps_short_numbers_and_labels():
    assert ev.format_floats('95% Wilson [0.030053369748306635, 0.5635028221864702]') == '95% Wilson [0.0301, 0.564]'
    assert ev.format_floats('618.3 min, h 2.15, 0.812, [1, 1], 1109.2') == '618.3 min, h 2.15, 0.812, [1, 1], 1109.2'


@needs_run
def test_render_of_the_final_run_has_no_raw_floats_and_the_preregistered_test_row_first(tmp_path):
    ev.render(RUN / 'eval/results.json', tmp_path / 'tables.md')
    md = (tmp_path / 'tables.md').read_text()
    assert all(ev.number_text(float(m[0])) == m[0] for m in ev.RAW_FLOAT.finditer(md)) and 'Re-rendered from the saved' in md.splitlines()[2]
    test = [line for line in md.splitlines() if line.startswith('| core8 | synthetic recovery | test | headline (L2+L3) |')]
    assert ev.PRE_REGISTERED in test[0] and test[0].split(' | ')[5:10] == ['28', '9', '0', '4', '0.812']


@needs_run
def test_stress_intervals_reproduce_every_saved_row():
    stress = json.loads((RUN / 'eval/results.json').read_text())['stress']
    for row in stress['rows']:
        new = ev.stress_intervals(ev.stress_records(row, stress['flawed_clips']), row['key_share_per_min'])
        for k in ('added_ci95', 'removed_ci95', 'retention_ci95', 'limits', 'added_per_min', 'retention'):
            assert new[k] == row[k], (row['split'], row['condition'], k)
        assert {k: v['ci95'] for k, v in new['added_by_key'].items()} == {k: v['ci95'] for k, v in row['added_by_key'].items()}


def test_speaker_clusters_give_per_speaker_values_and_no_interval():
    record = lambda speaker, rec, added: {'split': 'val', 'condition': 'noise', 'regime': 'R1', 'reference_mode': None, 'speaker': speaker,  # noqa: E731
                                          'participant_recording': rec, 'added': added, 'removed': 0, 'minutes': 1.0, 'regions_added': ['D2-'] * added,
                                          'found_before_ids': [0], 'found_before_keys': ['D2-'], 'retained_ids': [0]}
    detail = [record('s1', f'r{i}', i % 2) for i in range(6)] + [record('s2', f'q{i}', 1) for i in range(6)]
    row = {'split': 'val', 'condition': 'noise', 'regime': 'R1', 'reference_mode': None, 'key_share_per_min': 0.0556}
    by_recording = ev.stress_intervals(ev.stress_records(row, detail), 0.0556)
    by_speaker = ev.speaker_stress_row(row, detail)
    assert by_recording['added_interval']['ci95'][0] is not None and by_recording['added_interval']['unit'] == 'recording'
    assert by_speaker['added_interval']['ci95'] == [None, None] and by_speaker['added_interval']['per_cluster'] == {'s1': 0.5, 's2': 1.0}
    assert 'fewer than 5 speakers' in by_speaker['limits'][0] and 'per-speaker values' in by_speaker['interval_scope']


def test_a_degenerate_kept_interval_carries_the_pooled_wilson_interval():
    block = {'ci95': [1.0, 1.0], 'retained': 73, 'found': 73}
    assert gallery.with_wilson(block)['wilson95'] == [0.95, 1.0]
    assert 'wilson95' not in gallery.with_wilson({**block, 'ci95': [0.9, 1.0]})


@needs_run
def test_shipped_stress_matrix_has_speaker_rows_for_val_and_test():
    rows = json.loads((GALLERY / 'stress_matrix.json').read_text())
    assert rows == json.loads(json.dumps(gallery.dashboard_stress(json.loads((RUN / 'eval/results.json').read_text())['stress'])))
    for row in rows:
        blocks = [row['added_interval'], row['removed_interval'], row['retention_interval'], *row['added_by_key'].values()]
        if row['split'] in gallery.SUMMARY_SPLITS:
            assert all(b['ci95'] == [None, None] or not b.get('events') for b in blocks if b.get('events') is not None), row['condition']
            assert row['retention_interval']['unit'] == 'speaker'
        elif row['retention_interval']['ci95'][0] is not None and row['retention_interval']['ci95'][0] == row['retention_interval']['ci95'][1]:
            assert row['retention_interval']['wilson95']


def lockbox_mode(**kw) -> dict:
    return {'mode': 'single', 'rate': 0.46, 'upper95': 0.538, 'budget': 0.5, 'budget_status': 'met on covered sources only',
            'source_weights': {'accent': 0.5, 'poetry': 0.5}, 'by_source': {'accent': 0.652, 'poetry': 0.268}, 'uncovered_sources': ['ears', 'gettysburg'],
            'languages_above_budget': [{'language': 'amharic', 'rate': 1.28, 'readers': 5, 'comparison_minutes': 14.1}], **kw}


def test_lockbox_note_is_plain_words_from_the_structured_fields():
    note = gallery.budget_note(lockbox_mode())
    assert note.startswith('Covers Speech Accent Archive readers and LibriVox poetry readers, weighted equally; EARS readers and')
    assert 'met at the point rate (0.460) on the covered sources only; the upper 95 % bound (0.538) does not establish' in note
    assert 'Amharic 1.28/min (5 readers)' in note and 'partition' not in note and 'upper95' not in note
    assert 'not met' in gallery.budget_note(lockbox_mode(budget_status='not met on covered sources only'))
    assert 'Amharic 1.28' in gallery.lockbox_text([lockbox_mode()])


def test_limits_give_the_preregistered_per_speaker_values_first():
    r1 = [{'split': 'test', 'speakers': 2, 'preregistered': {'f1_per_speaker': {'a': 0.8, 'b': 0.824}},
           'count_once': {'f1_per_speaker': {'a': 0.848, 'b': 0.909}}}]
    text = gallery.limits({'r1': r1, 'lockbox': [], 'r2_level3': [{'type': 'RUSH', 'detected': 1, 'edits': 18}]})
    assert text[0].index('0.800 and 0.824 under the pre-registered accounting') < text[0].index('0.848 and 0.909 counting one detection')
    assert 'rush 1 of 18' in text[1] and '625' not in text[1]


def test_level_one_text_gives_the_preregistered_count_first():
    rows = [{'split': 'val+test', 'preregistered': {'tp': 6, 'fn': 26}, 'count_once': {'tp': 8, 'fn': 24}}]
    assert 'finds 6 of 32 level-1 edits in val and test under the pre-registered accounting (8 of 32 counting one detection' in gallery.level_one_text(rows)


@needs_run
@pytest.mark.skipif(not (RUN / 'eval/addendum.json').exists(),
                    reason='the final-run folder (build/, git-ignored) is not distributed with the repository')
def test_panel_shows_the_own_scales_baseline_from_the_addendum():
    shipped = json.loads((GALLERY / gallery.EVALUATION).read_text())
    own = {r['split']: r['f1'] for r in shipped['reference_free'] if r['method'] == gallery.OWN_SCALES}
    assert own == {'val': 0.295, 'test': 0.407} and 'lower bound' in shipped['reference_free_note']
    test = next(r for r in shipped['r1'] if r['split'] == 'test')
    assert test['preregistered']['f1_per_speaker'] == {'mobama_weekly_2014': 0.8, 'nixon_resignation_1974': 0.824}


def test_off_truth_findings_are_counted_once_and_named_in_the_description():
    res = {'regime': 'R2', 'differences': [], 'flaws': [
        {'id': 'd3-001', 'context': 'whole passage', 'p': [0.0, 9.0], 'points_lost': 3.99},
        {'id': 'd1-001', 'context': '', 'p': [1.0, 2.0], 'points_lost': 1.0},
        {'id': 'd1-002', 'context': '', 'p': [1.5, 2.5], 'points_lost': 0.5},
        {'id': 'd5-001', 'context': '', 'p': [5.0, 6.0], 'points_lost': 0.2}],
        'truth': [{'type': 'RUSH', 'finding': 'd1-001', 'duplicate_findings': ['d1-002'], 'difference': None, 'detector_status': 'enabled', 'p': [1.0, 2.0]},
                  {'type': 'LOW_EFFORT', 'finding': None, 'difference': None, 'detector_status': 'enabled', 'p': [4.9, 6.1], 'excluded': ['x'], 'on_edit': ['d5-001']}]}
    assert [f['id'] for f in gallery.off_truth(res)] == ['d3-001']
    text = gallery.edits_text({'flaws': [{'type': 'RUSH'}, {'type': 'LOW_EFFORT', 'evaluation_excluded': True}]}, res)
    assert '1 finding matches no injected edit (over the whole passage) and cost 3.99 points' in text and 'it is a difference between the two readers' in text


@needs_run
def test_r2_gallery_descriptions_explain_their_off_truth_costs():
    index = json.loads((GALLERY / 'index.json').read_text())
    for item in ('r2_consensus', 'r2_listed'):
        assert 'match no injected edit' in next(it for it in index['items'] if it['id'] == item)['description'].replace('matches', 'match'), item
    assert index['provenance']['command'].startswith('python -m cvoice.gallery') and index['provenance']['note']


def finding(base, dim: str, x: float, a: int, b: int, pinned_detector, compat=None):
    reg = pinned_detector()['regimes']['R1']
    comp = with_x(base, dim, [(a, b, x)])
    P = base if compat is None else dataclasses.replace(base, al=dataclasses.replace(base.al, compat=compat))
    r = local(dim, a, b, z=-3)
    sc = score(comp, [r], reg, C.PMAX_START)
    return explain.build(r, comp, base, P, reg, sc.masses[0], sc, 'p')


def test_window_findings_are_approximate_and_timing_findings_name_low_aligner_confidence(base, pinned_detector):
    plain = finding(base, 'D1', -0.6, 10, 14, pinned_detector)
    assert explain.WINDOW_CLAUSE in plain['text'] and 'low aligner confidence' not in plain['text'] and 'You took' not in plain['text']
    low = np.array(base.al.compat, float)
    low[plain['words'][0]] = 0.0
    flagged = finding(base, 'D1', -0.6, 10, 14, pinned_detector, compat=low)
    assert re.search(r'1 word in this span has low aligner confidence', flagged['text'])
    fade = finding(base, 'D5', -6.0, 10, 14, pinned_detector, compat=low)
    assert explain.WINDOW_CLAUSE in fade['text'] and 'low aligner confidence' not in fade['text']
    pause = finding(base, 'D2', -0.6, 7, 7, pinned_detector)
    assert explain.WINDOW_CLAUSE not in pause['text'] and 'You hold' not in pause['text']
