"""Schema-4 measures, post-decode grouping, schema-2 API and dev-only evaluation."""
import dataclasses
import json
import math
from types import SimpleNamespace

import numpy as np
import pytest

from cvoice import calibrate, config as C, edits_extra as E, evaluate, explain, patterns, pipeline
from cvoice.align import Alignment
from cvoice.compare import compare
from cvoice.detect import clip_flags, decode, make_detector, save_detector
from cvoice.events import eval_clip, match, run_pair, truths
from cvoice.features import make_recording
from cvoice.score import region_mass, score
from synth import label, local, regime, with_x
from test_edits_extra import recipe_recording


@pytest.fixture(scope='module')
def rec():
    return recipe_recording()


def edited(rec, recipe, args, level=3, **kwargs):
    y, chain, lab = recipe(rec, *args, level=level, **kwargs)
    for event in lab['flaws'][0]['events']:
        if event['kind'] == 'silence':
            point = event['parent_span'][0]
            event['clip_span'] = [round(float(chain(point, 'left'))), round(float(chain(point, 'right')))]
        elif event['kind'] != 'copy':
            event['clip_span'] = list(chain.cur(*event['parent_span']))
    al = Alignment(np.array(lab['words']['start']) / C.SR, np.array(lab['words']['end']) / C.SR, rec.al.compat, .9)
    return make_recording(y, rec.tr, al), lab


@pytest.mark.parametrize('recipe,args,dim,unit', [
    (E.word_repetition, (4,), 'D7', 4), (E.rhyme_prolongation, (3,), 'D7', 3),
    (E.onset_prolongation, (6,), 'D7', 6), (E.block_before_release, (3,), 'D7', 3),
    (E.rising_ending, (1,), 'D8', 15), (E.flattened_final_fall, (1,), 'D8', 15)])
def test_new_recipe_peak_and_placebo(rec, recipe, args, dim, unit):
    P, _ = edited(rec, recipe, args)
    d = compare(rec, P).dims[dim]
    assert np.nanargmax(d.x) == unit and d.x[unit] > 0
    N, _ = edited(rec, recipe, args, None)
    c = compare(rec, N)
    assert decode(c, regime('R1'), rec.tr.sentence) == []
    assert clip_flags(c, regime('R1')) == {}


def test_voiced_sound_repetition_peak(rec):
    a = round(rec.al.start[6] * C.SR)
    P, _ = edited(rec, E.sound_repetition, (6,), sound_span=(a, a + round(.16 * C.SR)))
    assert np.nanargmax(compare(rec, P).dims['D7'].x) == 6


def test_identity_coverage_references_and_whole_clip_timing(rec):
    c = compare(rec, rec)
    for d in c.dims.values():
        assert np.nanmax(np.abs(d.x), initial=0) < 1e-9
    assert c.coverage['D7'] == c.coverage['D8'] == 1
    occ = rec.occ * np.exp(np.tile([-.5, .5], len(rec.tr) // 2))
    P = dataclasses.replace(rec, occ=occ)
    d = compare(rec, P).dims['D7']
    ratios = np.log((occ + C.D7_REG_S) / (rec.occ + C.D7_REG_S))
    assert d.g == pytest.approx(C.MAD_SCALE * np.median(np.abs(ratios - np.median(ratios))))
    assert d.reference(3) == pytest.approx((d.p[3] + C.D7_REG_S) / np.exp(d.x[3]) - C.D7_REG_S)
    c = compare(rec, P)
    assert 'D7' in clip_flags(c, regime('R1')) and 'D7' not in clip_flags(c, regime('R2'))
    fp = rec.final_df0.copy()
    fp[-1] += 3
    d = compare(rec, dataclasses.replace(rec, final_df0=fp)).dims['D8']
    assert d.reference(len(rec.tr) - 1) == pytest.approx(fp[-1] - d.x[-1])
    missing = dataclasses.replace(rec, final_df0=np.full(len(rec.tr), np.nan))
    assert compare(rec, missing).coverage['D8'] == 0


def test_grouping_keeps_regions_and_one_mass_per_location(base):
    c = with_x(base, 'D7', [(11, 11, math.log(3))])
    c.dims['D2'].x[10], c.dims['D2'].countable[10] = .8, True
    reg = regime('R1')
    regions = decode(c, reg, base.tr.sentence)
    before = [dataclasses.asdict(r) for r in regions]
    info = patterns.annotate(c, regions, base, base)
    assert [dataclasses.asdict(r) for r in regions] == before
    assert [v['group_pattern'] for v in info] == ['HESITATION', 'HESITATION']
    sc = score(c, regions, reg, C.PMAX_START)
    raw = [region_mass(c.dims[r.dim], r, reg['scales'][r.dim + '+'], 2) for r in regions]
    assert sum(sc.masses) == pytest.approx(max(raw)) and sum(m > 0 for m in sc.masses) == 1


def test_word_by_word_truths_are_separate_and_group_precedes_hesitation(rec):
    P, lab = edited(rec, E.word_by_word_reading, ((8, 12),))
    ts = truths(lab)
    assert len(ts) == 4 and [t['words'] for t in ts] == [[i, i + 1] for i in range(8, 12)]
    det = make_detector({name: regime(name, 1) for name in C.REGIMES}, C.PMAX_START, {})
    run = run_pair(rec, P, det, 'R1')
    ev = eval_clip(run, lab)
    assert ev['word_by_word'] == {'label_groups': 1, 'eligible_clips': 1, 'detected_clips': 1, 'boundary_truths': 4}
    assert sum(t['detected'] for t in ev['truth']) == 4
    info = patterns.annotate(run.comp, run.regions, rec, P)
    assert sum(v['pattern'] == 'WORD_BY_WORD' for v in info) == 4
    assert len(run.regions) == len(info)


def test_both_edges_rule_has_the_index_overlap_secondary_column(rec, pinned_detector):
    P, lab = edited(rec, E.block_before_release, (3,))
    run = run_pair(rec, P, pinned_detector(), 'R1')
    ts = truths(lab)
    assert match(ts, run)
    ts[0]['span'] = (ts[0]['span'][0] + .4, ts[0]['span'][1])
    assert match(ts, run) == {} and match(ts, run, False)
    bad_lab = json.loads(json.dumps(lab))
    bad_lab['flaws'][0]['events'][0]['clip_span'][0] += round(.4 * C.SR)
    row = eval_clip(run, bad_lab)['truth'][0]
    assert not row['detected'] and row['detected_index_or_overlap']


@pytest.mark.parametrize('typ', C.FLAW_TYPES)
def test_registry_truths_and_no_detector(rec, typ):
    ts = truths(label(rec, typ, (3, 3)))
    assert ts[0]['dim'] == C.FLAW_REGISTRY[typ]['primary']
    assert ts[0]['available'] == (typ != 'REPEATED_CONTOUR')
    assert C.FLAW_FAMILY['HESITATION'] == C.FLAW_DIM['HESITATION'] == 'D2'
    assert all(d in C.DIMS for r in C.FLAW_REGISTRY.values() for d in r['secondary'])


@pytest.mark.parametrize('dim,sign,subtype', explain.EXPLAIN)
def test_every_explanation_table_key_renders(base, dim, sign, subtype):
    c = with_x(base, dim, [(10, 10, sign * (6 if dim in ('D5', 'D8') else 1))])
    r = local(dim, 10, 10, sign * 4)
    reg = regime('R1', enabled=list(C.DIMS))  # listed dimensions render too once promoted
    info = patterns.describe(r, c, base, base)
    info.update(pattern=subtype, candidate=subtype in ('WORD_REPETITION', 'SOUND_REPETITION', 'ONSET_PROLONGATION', 'RHYME_PROLONGATION'))
    values = dict(occupancy_p_s=1., occupancy_b_s=.3, silence_s=.5, reference_silence_s=0., inserted_text='truths',
                  inserted_s=.3, voiced_run_s=.3, run_s=.4, final_change_p_st=2., final_change_b_st=-2., stretch='last .20 s',
                  pause_s=.8, reference_pause_s=.02, next_word_stretch_ln=.5, events=3, mean_run_words=1.,
                  word_time_p_s=1., word_time_b_s=1.3, word_time_ln=-.26, pause_p_s=.1, pause_b_s=.6,
                  alpha_change_db=-3., f0_change_st=-1., last_word_drop_db=-6., reference_last_word_drop_db=-1.)
    info['evidence'] = [patterns.evidence(k, k, v, None) for k, v in values.items()] if subtype else []
    sc = score(c, [r], reg, C.PMAX_START)
    f = explain.build(r, c, base, base, reg, sc.masses[0], sc, 'f', info)
    assert f['pattern'] == subtype and f['why'].startswith('"') and f['text']
    assert ('Automatic label;' in f['text']) == info['candidate']
    if subtype is not None:
        info['pattern'] = 'UNKNOWN'
        with pytest.raises(KeyError):
            explain.build(r, c, base, base, reg, 0, sc, 'f', info)


def test_api_contract_listed_and_promoted_and_groups(rec, pinned_detector):
    P, _ = edited(rec, E.block_before_release, (3,))
    result = pipeline.analyze(P, rec.tr, rec, regime='R2', detector=pinned_detector())
    assert result['schema'] == 2
    assert set(result['detection']) >= {'enabled', 'flag_keys', 'listed_keys', 'clip_keys', 'listed_clip_keys', 'calibrated'}
    assert result['detection']['listed_keys'] == ['D7+', 'D8+', 'D9-'] and result['detection']['listed_clip_keys'] == ['D7']  # D9 listed in R2
    delta_rows = result['rows'][2:]
    assert len(delta_rows) == 9 and all('status' in r for r in delta_rows)
    assert [r['kind'] for r in delta_rows[-2:]] == ['word', 'word']
    assert all(r['tol'] == [None, None] for r in delta_rows if r['key'] in ('word_time','ending'))
    assert all(f['dimension'] != 'D7' for f in result['flaws'])
    listed = [f for f in result['differences'] if f['status'] == 'listed']
    assert listed and all('points_lost' not in f and 'group' not in f for f in listed)
    assert all(f['pattern'] == 'LENGTHENED_WORD' for f in listed if f['dimension'] == 'D7' and f['words'])
    det = pinned_detector()
    det['regimes']['R2'] = regime('R2', enabled=[*C.REGIME_DIMS['R2'], 'D7', 'D8'])
    promoted = pipeline.analyze(P, rec.tr, rec, regime='R2', detector=det)
    assert promoted['detection']['listed_keys'] == ['D9-'] and promoted['detection']['listed_clip_keys'] == []
    assert any(f['dimension'] == 'D7' for f in promoted['flaws'])
    required = {'id', 'type', 'label', 'dimension', 'brief_word', 'severity', 'words', 'p', 'b', 'measure', 'unit',
                'baseline', 'participant', 'delta', 'tolerance_multiple', 'threshold', 'points_lost', 'overall_if_fixed', 'dimension_points_lost',
                'context', 'text', 'why', 'fix', 'pattern', 'evidence', 'span_kind', 'group', 'group_pattern', 'counted', 'candidate'}
    assert all(set(f) == required or set(f) == required | {'value_unit'} for f in promoted['flaws'])
    json.loads(pipeline.dumps(promoted))
    H, _ = edited(rec, E.hesitation_before_word, (3,))
    grouped = pipeline.analyze(H, rec.tr, rec, regime='R1', detector=pinned_detector(1))
    members = [f for f in grouped['flaws'] if f['group_pattern'] == 'HESITATION']
    assert len(members) == 2 and sum(f['counted'] for f in members) == 1
    assert all(f['group'] == sorted(v['id'] for v in members) for f in members)
    assert all(f['points_lost'] == 0 and f['overall_if_fixed'] == grouped['scores']['overall'] for f in members if not f['counted'])


def test_promotion_gates_closed_without_real_evidence(rec, monkeypatch):
    monkeypatch.setattr(C, 'R2_BOOTSTRAPS', 5)
    monkeypatch.setattr(C, 'H_GRID', (1, 2, 3))
    ns = [calibrate.Null('ref>p', compare(rec, rec), rec.tr.sentence, 1, 'select', 'g', 'p', 'ref')]
    reg, _ = calibrate.fit_r2(ns)
    P, lab = edited(rec, E.block_before_release, (3,))
    reg, report = calibrate.promote_r2(ns, ns, [(rec, rec, P, lab)], reg, {})
    assert reg['enabled'] == list(C.REGIME_DIMS['R2'])
    assert {r['key'] for r in report['rows']} == {'D7+', 'D8+', 'D9-'}
    assert all({'rate', 'bootstrap_upper95', 'rule_of_three', 'recall'} <= r.keys() and r['status'] == 'listed' for r in report['rows'])
    assert evaluate.ppv(.8, .01) == pytest.approx(.8 * .0021 / (.8 * .0021 + .01 * .9979))


def test_select_edits_use_full_pool_text_and_select_references(rec, monkeypatch):
    monkeypatch.setattr(C, 'FLAW_TYPES', ('BLOCK', 'RISING_ENDING', 'REPEATED_CONTOUR'))
    entries = [dict(id=i, null_set=s) for i, s in (('p', 'select'), ('b1', 'select'), ('b2', 'select'), ('fit', 'fit'))]
    seen = []
    def recs(rows):
        seen.extend(e['id'] for e in rows)
        return [rec for _ in rows]
    def prepare(items):
        assert all(tr.norm == rec.tr.norm for _, tr in items)
        return [rec for _ in items]
    ds = SimpleNamespace(manifest={'readers': entries}, recs=recs, prepare_many=prepare, pool=None, _recs={})
    nulls = [calibrate.Null(f'{b}>p', compare(rec, rec), rec.tr.sentence, 1, 'select') for b in ('b1', 'b2')]
    pairs = [pair for batch in calibrate.select_edit_pairs(ds, nulls) for pair in batch]
    assert seen == ['b1', 'b2', 'p']
    assert len(pairs) == 4 and {lab['flaws'][0]['type'] for _, _, _, lab in pairs} == {'BLOCK', 'RISING_ENDING'}
    assert all(lab['flaws'][0]['level'] == 3 for _, _, _, lab in pairs)


def test_cross_whole_clip_truth_and_trivial_local_sampling(rec):
    det = make_detector({name: regime(name, enabled=list(C.DIMS)) for name in C.REGIMES}, C.PMAX_START, {})
    occ = rec.occ * np.exp(np.tile([-1., 1.], len(rec.tr) // 2))
    P = dataclasses.replace(rec, occ=occ)
    clean, changed = run_pair(rec, rec, det, 'R2'), run_pair(rec, P, det, 'R2')
    lab = label(rec, 'UNEVEN_TEMPO', (0, len(rec.tr) - 1))
    ts = truths(lab)
    _, matches, clips = evaluate.cross_matches(clean, changed, ts, det['regimes']['R2'])
    assert matches == {0} and clips == {'D7'}
    assert evaluate._random_regions(ts, len(rec.tr), np.random.default_rng(1)) == []
    assert eval_clip(changed, lab)['false_clip'] == []


def test_promotion_refits_all_shares_and_report_switches_are_hashed(rec, monkeypatch):
    from cvoice.detect import config_hash
    monkeypatch.setattr(C, 'R2_BOOTSTRAPS', 5)
    monkeypatch.setattr(C, 'H_GRID', (1, 2, 3))
    ns = [calibrate.Null('ref>p', compare(rec, rec), rec.tr.sentence, 1, 'select', 'g', 'p', 'ref')]
    pairs = [(rec, rec, P, lab) for P, lab in [edited(rec, E.block_before_release, (3,)), edited(rec, E.rising_ending, (1,))]]
    validation = {k: {'lab_pass': True, 'auc': .8, 'auc_lower95': .6} for k in ('D7+', 'D8+')}
    validation['labels'] = {'block': {'lab_pass': True}, 'repetition': {'lab_pass': True, 'precision': .49},
                            'prolongation': {'lab_pass': True, 'low_f0': False}}
    reg, _ = calibrate.fit_r2(ns)
    reg, report = calibrate.promote_r2(ns, ns, pairs, reg, validation)
    assert all(r['status'] == 'promoted' for r in report['rows'] if C.dim_of(r['key']) not in C.OWNER_LISTED['R2'])
    assert reg['null']['budget_per_key'] == C.FALSE_RATE_BUDGET / 8  # D9- stays listed in R2
    assert reg['null']['clip_budget_per_key'] == C.FALSE_CLIP_RATE_BUDGET / 2
    assert reg['clip']['D7'] is None
    assert reg['pattern_labels']['block'] and not reg['pattern_labels']['repetition'] and not reg['pattern_labels']['prolongation']
    det = make_detector({'R1': regime('R1'), 'R2': reg}, C.PMAX_START, {})
    old = config_hash(det)
    reg['pattern_labels']['block'] = False
    assert config_hash(det) != old


def test_subtype_reference_floor_and_candidate_spans(rec):
    i = 3
    a, b = rec.al.start[i], rec.al.end[i]
    P = dataclasses.replace(rec, word_silence_spans=np.array([[a, a + .26]]))
    assert patterns.word_time(rec, P, i)['pattern'] == 'BLOCK'
    assert patterns.word_time(P, P, i)['pattern'] == 'LENGTHENED_WORD'
    ins = dict(prompt_index=i, norm=rec.tr.norm[i], start=a - .3, end=a - .1)
    P = dataclasses.replace(rec, inserted=[ins])
    info = patterns.word_time(rec, P, i)
    assert info['pattern'] == 'WORD_REPETITION' and info['candidate'] and info['words'] == [i - 1, i]
    assert info['p'] == (a - .3, a - .1) and info['span_kind'] == 'boundary'
    assert patterns.word_time(P, P, i)['pattern'] == 'LENGTHENED_WORD'
    for held, subtype in [((a, a + .21), 'ONSET_PROLONGATION'), ((b - .21, b), 'RHYME_PROLONGATION')]:
        P = dataclasses.replace(rec, stable_spans=np.array([held]))
        info = patterns.word_time(rec, P, i)
        assert info['pattern'] == subtype and info['candidate'] and info['p'] == held


def test_small_synthetic_evaluation_smoke(rec, pinned_detector, monkeypatch, tmp_path):
    cases = [(E.block_before_release, (3,)), (E.rising_ending, (1,))]
    clips = [dict(id=str(i), split='val', level=3, parent='s', kind='single', spectrum='extra') for i in range(2)]
    made = [edited(rec, fn, args) for fn, args in cases]
    det = pinned_detector()
    models = tmp_path / 'detector.json'
    save_detector(det, models)
    ds = SimpleNamespace(manifest={}, clips=lambda **kw: clips, labels=lambda c: made[int(c['id'])][1])
    monkeypatch.setattr(evaluate, 'load_dataset', lambda *a: ds)
    monkeypatch.setattr(evaluate, 'warm', lambda *a: None)
    monkeypatch.setattr(evaluate, 'figures', lambda *a: [])
    monkeypatch.setattr(evaluate, 'SECTIONS', [('headline', evaluate.headline_section)])
    monkeypatch.setattr(evaluate, 'clip_runs', lambda ds, det, cs: [(c, run_pair(rec, made[int(c['id'])][0], det, 'R1'), made[int(c['id'])][1]) for c in cs])
    out = evaluate.run(tmp_path, models, None, tmp_path, splits=('val',))
    assert out['errors'] == {} and not out['final']
    assert set(out['headline']['groups']) == {'core8', 'lab_passed', 'synthetic_only'}
    assert len(out['headline']['matching']) == 2
    assert 'Recovery of the synthetic edit' in (tmp_path / 'eval/tables.md').read_text()
    assert not (tmp_path / evaluate.FINAL_LOG).exists()
