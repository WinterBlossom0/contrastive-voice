"""Consensus references, speech tempo (D9), R2 reference modes and check-reader evaluation; CPU fixtures, no corpus or
lockbox."""
import dataclasses
from collections import Counter

import numpy as np
import pytest
from runs import check_reader_dataset, two_modes
from synth import label, local, with_x

from cvoice import calibrate, config as C, evaluate, pipeline, r2pool
from cvoice.compare import compare
from cvoice.detect import decode
from cvoice.events import eval_clip, run_pair, truths
from cvoice.features import speech_time_ratio
from cvoice.lab.evaluate import median_reference as lab_median
from cvoice.lab.measures import speech_time_ratio as lab_speech
from cvoice.reference import consensus_reference, median_reference
from cvoice.uncertainty import wilson


def test_lab_imports_product_rules():
    assert lab_median is median_reference
    assert lab_speech is speech_time_ratio


def test_speech_tempo_ignores_pause_removal(base):
    end = base.al.end.copy()
    start = base.al.start.copy()
    # Remove one pause and shift every following word by the same amount.
    pause = base.sil[7]
    start[8:] -= pause
    end[8:] -= pause
    sil = base.sil.copy()
    sil[7] = 0.
    clean = {'start': base.al.start, 'end': base.al.end, 'sil': base.sil}
    changed = {'start': start, 'end': end, 'sil': sil}
    assert speech_time_ratio(changed, clean) == pytest.approx(0., abs=1e-12)


def test_consensus_is_word_anchored_and_robust_to_one_reference(base):
    refs = [dataclasses.replace(base, win_T=base.win_T*f, win_E=base.win_E+f) for f in (1.,1.1,1.2,1.3,20.)]
    B = consensus_reference(refs)
    assert B.win_T == pytest.approx(base.win_T*1.2)
    assert B.win_E == pytest.approx(base.win_E+1.2)
    assert B.tr is base.tr and np.array_equal(B.al.start,base.al.start)
    assert np.array_equal(refs[0].win_T,base.win_T)


@pytest.mark.parametrize('count,mode,h', [(1,'single',2.),(4,'single',2.),(5,'consensus5',4.),(6,'consensus5',4.)])
def test_pipeline_selects_calibrated_mode_by_reference_count(base,count,mode,h):
    refs = [dataclasses.replace(base) for _ in range(count)]
    result = pipeline.analyze(base,base.tr,base,regime='R2',detector=two_modes(),references=refs)
    assert result['detection']['reference_mode'] == mode
    assert result['detection']['reference_count'] == (5 if count >= 5 else 1)
    assert mode in result['scores']['detection_note'] and mode in result['notices'][0]
    assert next(r for r in result['rows'] if r['key']=='speech_tempo')['tol'][0] is None  # D9 listed in R2


def test_r1_d7_truth_and_empty_list_are_unscored(base):
    det = two_modes()
    det['regimes']['R1']['enabled'].remove('D7')
    det['regimes']['R1']['h']['D7+'] = None
    det['regimes']['R1']['clip']['D7'] = None
    result = pipeline.analyze(base,base.tr,base,regime='R1',detector=det,
                              truth=[{'type':'WORD_REPETITION','dimension':'D7'}])
    assert not result['truth'][0]['available'] and result['truth'][0]['detector_status']=='unscored'
    assert not result['detection']['show_listed'] and not result['differences']
    assert all('appear' not in n and 'dimensions are scored' not in n for n in result['notices'])
    run = run_pair(base,base,det,'R1')
    assert not eval_clip(run,label(base,'WORD_REPETITION',(10,10)))['truth'][0]['available']
    assert not truths(label(base,'WORD_REPETITION',(10,10)),enabled=run.enabled)[0]['available']


def test_coarse_window_tp_is_named_as_such(base,pinned_detector):
    run = run_pair(base,base,pinned_detector(),'R1')
    run.regions = [local('D5',9,15)]
    lab = label(base,'FADE',(10,15))
    lab['flaws'][0]['span'][0] += int(.05*C.SR)
    truth = eval_clip(run,lab)['truth'][0]
    assert truth['detected'] and truth['edge_error_above_tolerance']
    assert truth['grounding_status'] == 'true positive with coarse edges'


def test_accent_l1_and_seen_strata_have_proportional_splits():
    rows = [dict(id=f'{language}{i}',source='accent',speaker_id=f'{language}{i}',text='We read one text.',duration_s=30.)
            for language in ('english','arabic') for i in range(40)]
    seen = {f'accent:english{i}' for i in range(20)} | {f'accent:arabic{i}' for i in range(20)}
    pool = r2pool.inventory(rows,seen)
    counts = Counter((r['first_language'],r['lab_seen'],r['null_set']) for g in pool['groups'] for r in g['entries'])
    for language in ('english','arabic'):
        for status in (False,True):
            assert [counts[language,status,phase] for phase in ('fit','select','lockbox')] == [10,5,5]


def test_grouped_consensus_uses_five_other_readers(base,monkeypatch):
    rows = [dict(id=f'p{i}',source='accent',speaker_id=f'english{i}',reader_id=f'accent:english{i}',
                 duration_s=base.duration,clip_offset_s=0.) for i in range(6)]
    group = {'id':'accent:g','sets': {'fit':[r['id'] for r in rows], 'select':[], 'lockbox':[]}, 'entries':rows}
    pool = {'seed':42,'references_per_participant':5,'groups':[group]}
    pool['split_sha256'] = r2pool.partition_hash([group])
    class DS:
        manifest = {'r2_pool': pool, 'readers': rows}
        _recs = {}
        def recs(self,entries):
            return [dataclasses.replace(base,win_E=base.win_E+int(r['id'][1:])) for r in entries]
    monkeypatch.setattr(calibrate,'prepare_null_readers',lambda *args: None)
    ds = DS()
    single = calibrate.grouped_nulls(ds,'fit')
    consensus = calibrate.grouped_nulls(ds,'fit',consensus=True)
    assert len(single) == 30 and len(consensus) == 6
    for n in consensus:
        refs,p = n.id.split('>')
        assert len(set(refs.split(','))) == 5 and p not in refs.split(',')
    with pytest.raises(ValueError,match='lockbox'):
        calibrate.grouped_nulls(ds,'lockbox',consensus=True)


def test_r2_separate_modes_use_same_budget(base,monkeypatch):
    monkeypatch.setattr(C,'H_GRID',(1.,2.))
    nulls = [calibrate.Null('r>p',compare(base,base),base.tr.sentence,8.,group='accent:g',reader='p',source='accent')]
    reg,_ = calibrate.fit_r2(nulls)
    assert reg['null']['budget_per_key'] == pytest.approx(.5/6)  # D9 listed in R2
    assert reg['null']['clip_budget_per_key'] == pytest.approx(.05/2)
    assert 'D9-' not in reg['null']['local_by_key']


def test_d9_recovers_lab_scale_change_with_decomposition(base):
    P = dataclasses.replace(base,win_W=base.win_W/1.15)
    det = two_modes()
    det['regimes']['R1']['pattern_labels'] = {'natural_rush': True}
    result = pipeline.analyze(P,base.tr,base,regime='R1',detector=det)
    flags = [f for f in result['flaws'] if f['dimension']=='D9']
    assert flags and all(f['type']=='RUSH' for f in flags)  # pause rule: faster words with kept pauses are the RUSH change
    assert 'The words themselves were spoken faster' in flags[0]['text'] and 'pauses are reported separately' not in flags[0]['text']
    assert {e['key'] for e in flags[0]['evidence']} == {'word_time_ln','word_time_p_s','word_time_b_s','pause_p_s','pause_b_s'}
    assert not decode(with_x(base,'D9',[]),det['regimes']['R1'],base.tr.sentence)


def test_wilson_is_informative_at_zero_and_full_recall():
    assert wilson(0,2)[1] > .5
    assert wilson(2,2)[0] < .5


def test_check_away_edit_report_uses_both_calibrated_modes(base):
    ids = [f'cal{i}' for i in range(6)]
    entries = [dict(id=i,role='reader_calibration') for i in ids] + [dict(id='check',role='reader_check')]
    times = base.win_W.copy()
    times[10:16] /= 1.18
    P = dataclasses.replace(base,win_W=times)
    clip = dict(id='check__natural',baseline=ids[0],parent='check',split='check',regime='R2')
    lab = label(base,'NATURAL_RUSH',(10,15))
    result = evaluate.cross_section(check_reader_dataset(entries, clip, lab, base, P), two_modes(), ('val',))
    assert result['modes']['single']['summary']['check']['truth'] == 6
    assert result['modes']['consensus5']['summary']['check']['truth'] == 1
    assert result['modes']['single']['summary']['check']['detected'] == 0  # D9 is listed, never flagged, in R2 (config.LISTED_DIMS)
    assert result['modes']['consensus5']['summary']['check']['detected'] == 0
    assert result['modes']['consensus5']['curve']['minutes'] == pytest.approx(base.duration/60)
