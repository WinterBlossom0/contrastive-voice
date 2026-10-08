"""Calibration inputs and features: word occupancy, null crops, source weights, split isolation and bounded select calibration."""
import dataclasses
import json
from types import SimpleNamespace

import numpy as np
import pytest

from cvoice import audio, calibrate, config as C, dataset, features, patterns, pipeline
from cvoice.align import Alignment, parse_transcript
from cvoice.compare import compare, event_span
from cvoice.detect import clip_flags, decode, fit_clip
from cvoice.events import Run, match, on_flaw, truths
from cvoice.evaluate import edit_direction
from cvoice.passages import Anchor
from cvoice.r2pool import inventory, pair_ids, partition_hash, reader_id
from synth import label, local, regime, with_x


def test_first_word_ignores_voiced_introduction(base):
    voiced = base.fr.voiced.copy()
    voiced[:round(base.al.start[0] / C.HOP_S)] = True
    P = dataclasses.replace(base, fr=dataclasses.replace(base.fr, voiced=voiced))
    assert features.word_occupancy(P)[0] == base.al.end[0] - base.al.start[0]
    P.occ = features.word_occupancy(P)
    np.testing.assert_allclose(compare(base, P).dims['D7'].x, 0, atol=1e-12)


@pytest.mark.parametrize('gap', [.149, .151, .18, .4])
def test_word_edges_never_enter_occupancy(gap):
    rec = SimpleNamespace(al=Alignment(np.array([0., 1. + gap]), np.array([1., 2.]), np.ones(2), 1.),
                          regions=np.array([[0., 1.05], [1. + gap - .05, 2.]]),
                          fr=SimpleNamespace(voiced=np.ones(220, bool)))
    np.testing.assert_array_equal(features.word_occupancy(rec), rec.al.end - rec.al.start)


def test_occupancy_counts_only_isolated_long_gap_runs():
    voiced = np.zeros(250, bool)
    voiced[0:100] = True
    voiced[110:120] = True
    voiced[130:155] = True
    voiced[165:220] = True
    rec = SimpleNamespace(al=Alignment(np.array([0., 2.]), np.array([1., 2.2]), np.ones(2), 1.),
                          regions=np.array([[0., 1.05], [1.95, 2.2]]), fr=SimpleNamespace(voiced=voiced))
    np.testing.assert_allclose(features.word_occupancy(rec), [1., .45])
    np.testing.assert_allclose(features.orphan_voiced_spans(rec), [[1.3, 1.55]])


@pytest.mark.parametrize('width', [5, 10])
def test_stability_scores_use_window_centres(width):
    values = np.arange(30.) ** 2
    actual = features.window_stability(values, width)
    centre = (width - 1) // 2
    assert np.isnan(actual[:centre]).all()
    assert np.isnan(actual[centre + len(values) - width + 1:]).all()
    for start in range(len(values) - width + 1):
        block = values[start:start + width]
        t = np.arange(width) - (width - 1) / 2
        slope = np.dot(block, t) / np.dot(t, t)
        expected = abs(slope) + np.sqrt(np.mean((block - block.mean() - slope * t) ** 2))
        assert actual[start + centre] == pytest.approx(expected)


def test_long_final_word_matches_and_displays_measured_stretch(base):
    i = len(base.tr) - 1
    al = dataclasses.replace(base.al, start=base.al.start.copy())
    al.start[i] = al.end[i] - .8
    regions = base.regions.copy()
    regions[i] = [al.start[i], al.end[i]]
    P = dataclasses.replace(base, al=al, regions=regions)
    comp = with_x(P, 'D8', [(i, i, 3.)])
    reg = regime()
    run = Run(P, P, comp, [local('D8', i, i, 3)], None, 'R1', {})
    lab = label(P, 'RISING_ENDING', (i, i))
    lab['flaws'][0]['span'] = [round((al.end[i] - .25) * C.SR), round(al.end[i] * C.SR)]
    assert match(truths(lab), run) == {0: 0}
    span = event_span(comp, 'D8', i, P, P)
    assert span == pytest.approx((al.end[i] - C.FINAL_WINDOW_S, al.end[i]))
    info = patterns.describe(run.regions[0], comp, P, P, reg.get('pattern_labels'))
    assert info['p'] == span and info['b'] == span


def test_block_subtracts_short_reference_silence(base):
    i = 12
    a = base.al.start[i]
    B = dataclasses.replace(base, word_silence_spans=np.array([[a, a + .20]]))
    P = dataclasses.replace(base, word_silence_spans=np.array([[a, a + .40]]),
                            al=dataclasses.replace(base.al, end=base.al.end.copy()))
    P.al.end[i] = a + .5
    assert patterns.word_time(compare(B, P), B, P, i)['pattern'] == 'LENGTHENED_WORD'


def weighted_nulls(base):
    return [calibrate.Null(str(i), compare(base, base), base.tr.sentence, 1., group=g, reader=f'{s}:p{i}', source=s)
            for i, (s, g) in enumerate([('poetry', 'poetry:a'), ('poetry', 'poetry:b'), ('accent', 'accent:a')])]


def test_source_weights_rates_bounds_and_scales(base, monkeypatch):
    monkeypatch.setattr(C, 'R2_BOOTSTRAPS', 5)
    ns = weighted_nulls(base)
    weights = calibrate.pair_weights(ns)
    assert weights == [.25, .25, .5]
    assert calibrate.grouped_rate(ns, [4, 0, 0]) == 1.
    assert calibrate.grouped_rate(ns, [4, 0, 0], clip=True) == 1.
    report = calibrate.rate_report(ns, [4, 0, 0])
    assert report['rate'] == 1. and report['bootstrap_upper95'] >= 1.
    assert report['groups']['accent:a']['weight'] == .5
    captured = []
    original = calibrate.fit_scales
    monkeypatch.setattr(calibrate, 'fit_scales', lambda comps, ws: (captured.append(ws) or original(comps, ws)))
    calibrate.base_regime('R2', ns)
    assert captured == [weights]
    zero = calibrate.rate_report(ns, [0, 0, 0])
    assert zero['rule_of_three'] is None and zero['bootstrap_upper95'] is None


def test_clip_start_uses_source_weights(base):
    ns = weighted_nulls(base)
    for n, g in zip(ns, [10., 10., 0.]):
        n.comp.dims['D1'].g = g
    assert fit_clip([n.comp for n in ns], [.1, .1, .8])['D1'] == round(C.CLIP_H * C.FLOORS['D1'], 6)


def test_reader_identity_shared_across_librivox_sources():
    ids = [reader_id(r) for r in [dict(source='poetry', speaker_id='poem:eep2'),
           dict(source='gettysburg', speaker_id='gettysburgaddress_150anniv_1311_librivox:eep'),
           dict(source='gettysburg', speaker_id='lv_gettysburg150_eep')]]
    assert ids == ['librivox:eep'] * 3


def test_project_readers_and_their_poems_are_always_select():
    rows = [dict(id=f'{s}_{i}', source=s, speaker_id=f'poem:r{i}x' if s == 'poetry' else f'lv_gettysburg150_r{i}x',
                 text='We go.', duration_s=5.) for s in ['poetry', 'gettysburg'] for i in range(30)]
    rows[31]['id'] = 'null_project_dj'
    rows[32]['role'] = 'reader_check'
    pool = inventory(rows, {'poetry:r3x'})
    phases = {}
    for g in pool['groups']:
        for r in g['entries']:
            assert phases.setdefault(r['reader_id'], r['null_set']) == r['null_set']
            if r['reader_id'] in ['librivox:r1x', 'librivox:r2x']:
                assert r['null_set'] == 'select'
            if r['reader_id'] == 'librivox:r3x':
                assert r['null_set'] != 'lockbox'
    assert pair_ids(pool, 'fit') and pool == inventory(rows[::-1], {'poetry:r3x'})


@pytest.mark.parametrize('failure', ['anchor', 'alignment', None])
def test_null_crop_offsets_exclusions_and_lockbox_isolation(tmp_path, monkeypatch, failure):
    text = 'We go.'
    tr = parse_transcript(text)
    entries = [dict(id=i, source='poetry', speaker_id=i, group='g', reader_id=i, null_set=phase,
                    audio=i+'.wav', duration_s=10., sha256='source', text=text)
               for i, phase in [('fit', 'fit'), ('select', 'select'), ('lock', 'lockbox')]]
    for r in entries[:2]:
        audio.write_wav(tmp_path / r['audio'], np.zeros(10 * C.SR))
    group = dict(id='g', entries=entries, sets={s:[r['id'] for r in entries if r['null_set']==s] for s in ('fit','select','lockbox')},
                 minutes={}, reference_shortfalls={})
    pool = dict(groups=[group], excluded=[], split_sha256=partition_hash([group]))
    seen = []
    def locate(wavs, trs, *args):
        seen.append(len(wavs))
        return [[Anchor(0,0,len(tr)-1,1.,failure!='anchor',3.,5.)] for _ in wavs]
    def align(jobs, *args):
        return [Alignment(np.array([.5,1.5]),np.array([1.,2.5]),np.ones(2),0. if failure=='alignment' else 1.) for _ in jobs]
    monkeypatch.setattr(dataset, 'locate_many', locate)
    monkeypatch.setattr(dataset, 'run_jobs', align)
    dataset.crop_null_readers(tmp_path, pool)
    assert seen == [2] and not (tmp_path / 'lock.wav').exists()
    assert group['sets']['lockbox'] == ['lock']
    assert entries[-1]['duration_s'] == 10. and 'clip_offset_s' not in entries[-1]
    if failure:
        assert len(pool['excluded']) == 2 and group['sets']['fit'] == []
        assert failure in pool['excluded'][0]['reason']
    else:
        for r in entries[:2]:
            assert r['clip_offset_s'] == 2.5 and r['clip_end_s'] == 5.5
            assert r['duration_s'] == 3. and r['source_duration_s'] == 10.
            assert len(audio.read_wav(tmp_path/r['audio'])) == 3*C.SR
    assert pool['split_sha256'] == partition_hash(pool['groups'])
    json.loads((tmp_path/'manifest.json').read_text())


def test_select_sample_is_seeded_bounded_and_never_uses_fit(base, monkeypatch):
    monkeypatch.setattr(C, 'R2_SELECT_EDIT_CAP', 7)
    monkeypatch.setattr(C, 'R2_SELECT_EDIT_BUDGET_S', 60)
    ns = [calibrate.Null(f'b>p{i}', compare(base,base),base.tr.sentence,1.) for i in range(20)]
    ds = SimpleNamespace(manifest={'readers':[dict(id='b',duration_s=30.), *[dict(id=f'p{i}',duration_s=30.,source='poetry',group=f'poetry:{i%2}') for i in range(20)]]})
    a, report = calibrate.select_edit_sample(ds, ns)
    b, other = calibrate.select_edit_sample(ds, ns[::-1])
    assert a == b and report == other and len(a) <= 7 and report['expected_seconds'] <= 60
    assert all(r['references'] == ['b'] for r in a)
    assert len({r['id'] for r in a}) == len(a)


def test_closed_validation_never_iterates_edits_or_refits(base, monkeypatch):
    ns = weighted_nulls(base)
    monkeypatch.setattr(C, 'R2_BOOTSTRAPS', 5)
    reg, _ = calibrate.fit_r2(ns)
    def edits():
        raise AssertionError('edit preparation reached')
        yield
    monkeypatch.setattr(calibrate, 'fit_r2', lambda *a, **k: pytest.fail('closed-gate refit'))
    result, report = calibrate.promote_r2(ns, ns, edits(), reg, {})
    assert result['enabled'] == list(C.REGIME_DIMS['R2']) and len(report['rows']) == 3


def test_promotion_recall_uses_new_worsened_rule(base, monkeypatch):
    lab = label(base, 'UNEVEN_TEMPO', (0,len(base.tr)-1))
    lab['flaws'][0]['level'] = 3
    before = with_x(base,'D7',[])
    after = with_x(base,'D7',[])
    before.dims['D7'].g, after.dims['D7'].g = .8, 1.
    monkeypatch.setattr(calibrate, 'compare', lambda B,P: before if P is base else after)
    P = dataclasses.replace(base)
    found,total = calibrate._away_outcomes([(base,base,P,lab)], {'current': regime()})['current']
    assert found['D7+ whole clip'] == total['D7+ whole clip'] == 1
    after.dims['D7'].g = .8 + 1e-10
    found,total = calibrate._away_outcomes([(base,base,P,lab)], {'current': regime()})['current']
    assert total['D7+ whole clip'] == 1 and found['D7+ whole clip'] == 0


def test_uneven_tempo_needs_its_own_release_switch(base):
    comp = with_x(base,'D7',[])
    comp.dims['D7'].g = 1.
    reg = regime()
    reg['pattern_labels'] = {}
    assert 'D7' not in clip_flags(comp,reg)
    reg['pattern_labels']['uneven_tempo'] = True
    assert 'D7' in clip_flags(comp,reg)


@pytest.mark.parametrize('typ,dim', [('DRAG','D7'),('MONOTONE','D8'),('MISPLACED_EMPHASIS','D7'),('UNEVEN_TEMPO','D7')])
def test_registry_secondaries_merge_legacy_labels(base,typ,dim):
    lab = label(base,typ,(10,15))
    assert dim in truths(lab)[0]['secondary']
    if typ in C.CORE8_TYPES:
        assert dim not in C.as_dict(3)['EXPECTED_SECONDARY'][typ]


def test_word_by_word_next_boundary_is_not_an_exact_hit(base):
    i = 7
    comp = with_x(base,'D2',[(i+1,i+1,1.)])
    run = Run(base,base,comp,[local('D2',i+1,i+1,3.)],None,'R1',{})
    t = truths(label(base,'WORD_BY_WORD',(i,i+1)))[0]
    t['span'],t['mid'] = (100.,101.),100.5
    assert match([t],run) == {} and not on_flaw(run.regions[0],t)
    other = with_x(base,'D2',[(i,i,.1),(i+1,i+1,2.)])
    clean = dataclasses.replace(run,comp=with_x(base,'D2',[]))
    changed = dataclasses.replace(run,comp=other)
    assert edit_direction(clean,changed,t)['x_edited'] == pytest.approx(.0)


def test_schema3_has_no_empty_listed_panel_and_r1_note(base):
    reg = regime('R2')
    for k in ['D7+','D8+','D9']:
        reg['scales'].pop(k)
    reg['clip'].pop('D7')
    assert pipeline.listed_dims(reg) == ()
    assert pipeline.detection_block({},reg)['listed_keys'] == []
    reg = regime('R1',enabled=list(C.DIMS[:6]))
    from cvoice.score import score
    comp = compare(base,base)
    sc = score(comp,decode(comp,reg,base.tr.sentence),reg,C.PMAX_START)
    rows = pipeline.scores_block(sc,reg,'R1')['dims']
    assert next(r for r in rows if r['key'] == 'D7')['note'] == 'listed, unscored: ' + pipeline.listed_reason('R1', 'D7')
    assert 'gate' not in pipeline.listed_reason('R1', 'D7') and 'placebo' not in pipeline.listed_reason('R1', 'D7')
    assert next(r for r in rows if r['key'] == 'D8')['note'] == 'listed, unscored: ' + pipeline.listed_reason('R1', 'D8')


def test_r1_f1_maximum_accepts_integer_recall_loss():
    rows = [{'h': 1., 'F1': .5, 'per_type_recall': {'FADE': 1.}},
            {'h': 2., 'F1': .8, 'per_type_recall': {'FADE': .5}},
            {'h': 3., 'F1': .8, 'per_type_recall': {'FADE': .5}}]
    best, rule = calibrate.choose_r1_row(rows)
    assert best['h'] == 2. and rule == 'in-sample strict F1 maximum; ties use smaller h'
    assert all('eligible' not in row for row in rows)


def test_select_edits_prepare_through_pool_in_bounded_batches(base,monkeypatch):
    monkeypatch.setattr(C,'R2_SELECT_EDIT_BATCH',2)
    entries = [dict(id=i) for i in ['b', *[f'p{j}' for j in range(5)]]]
    cache, calls = {}, []
    def recs(rows):
        for r in rows:
            cache[r['id']] = base
        return [cache[r['id']] for r in rows]
    def prepare(items):
        assert len(items) <= 2
        return [base for _ in items]
    def task(clean,ref,row):
        lab = label(base,'BLOCK',(3,3))
        return base.wav,lab
    def mapped(fn,args,pool):
        calls.append((len(args),pool))
        return [fn(*arg) for arg in args]
    monkeypatch.setattr(calibrate,'select_edit_task',task)
    monkeypatch.setattr(calibrate,'map_calls',mapped)
    pool = object()
    ds = SimpleNamespace(manifest={'readers':entries},recs=recs,prepare_many=prepare,_recs=cache,pool=pool)
    sample = [dict(id=str(i),participant=f'p{i}',references=['b'],type='BLOCK') for i in range(5)]
    report = {}
    sizes = [len(batch) for batch in calibrate.select_edit_pairs(ds,[],sample,report)]
    assert sizes == [2,2,1] and calls == [(2,pool),(2,pool),(1,pool)]
    assert cache == {} and report['placed_edits'] == 5


@pytest.mark.parametrize('whole_found,enabled', [(2,False),(8,True)])
def test_tempo_clip_promotion_uses_own_recall_and_survives_next_candidate(base,monkeypatch,whole_found,enabled):
    from collections import Counter
    monkeypatch.setattr(C,'R2_BOOTSTRAPS',5)
    monkeypatch.setattr(C,'H_GRID',(1.,2.))
    ns = weighted_nulls(base)
    reg,_ = calibrate.fit_r2(ns)
    validation = {k:{'lab_pass':True,'auc':.8,'auc_lower95':.6} for k in ['D7+','D8+']}
    validation['labels'] = {'uneven_tempo':{'lab_pass':True}}
    def outcomes(pairs,regs):
        return {token:(Counter({'D7+':8 if 'D7' in token[0] else 0,'D8+':8 if 'D8' in token[0] else 0,
                               'D7+ whole clip':whole_found if token[1] else 0}),
                       Counter({'D7+':10,'D8+':10,'D7+ whole clip':10})) for token in regs}
    monkeypatch.setattr(calibrate,'_away_outcomes',outcomes)
    result,report = calibrate.promote_r2(ns,ns,[],reg,validation)
    assert 'D7' in result['enabled'] and 'D8' in result['enabled']
    assert (result['clip']['D7'] is not None) == enabled
    assert result['pattern_labels']['uneven_tempo'] == enabled
    assert result['null']['clip_budget_per_key'] == C.FALSE_CLIP_RATE_BUDGET / (3 if enabled else 2)
    assert report['rows'][0]['whole_clip']['recall'] == whole_found / 10


def test_uncropped_null_dataset_cannot_reach_calibration(tmp_path):
    rows = [dict(id=f'p{i}',source='accent',speaker_id=str(i),text='We go.',duration_s=10.) for i in range(20)]
    pool = inventory(rows)
    ds = dataset.Dataset(tmp_path,{'r2_pool':pool,'readers':[r for g in pool['groups'] for r in g['entries']]})
    with pytest.raises(ValueError,match='cropped before calibration'):
        calibrate.grouped_nulls(ds,'fit')
