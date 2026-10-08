"""Independent numerical examples; no checkpoint, network or pool."""
from dataclasses import replace
import json
from pathlib import Path

import numpy as np
import pytest

from cvoice.lab import measures as M
from cvoice.lab.data import annotate, select, audit, grid_text
from cvoice.lab.evaluate import (auc, event_metrics, fixed_rate, isolated, median_reference, normal_plan, labelled_events, rank_scores)
from cvoice.lab.extract import recording_arrays
from cvoice.lab.__main__ import save_features
from synth import recording


def test_pace_pause_definitions():
    x={'sil':np.array([.3,0.,.5]),'sil_raw':np.array([.3,.1,.5]),'punct':np.array([False,False,True,True]),
       'norm':['ONE','TWO','THREE','FOUR'],'start':np.array([0.,.7,1.2,2.]),'end':np.array([.4,1.,1.5,2.4])}
    assert M.within_phrase_count(x)==1
    assert M.within_phrase_duration(x)==pytest.approx(.3)
    assert M.speech_time_ratio(x)==pytest.approx(1.6)
    assert M.mean_run(x)==pytest.approx(4/3)
    assert M.breath_position(x)==pytest.approx(.5)
    assert M.speech_time_ratio(x,x)==0
    assert M.pause_count_ratio(x,x)==1
    assert M.mean_pause_ratio(x,x)==1


def test_duration_and_rhythm():
    x={'char_duration':np.array([.1,.2,.3,.4]),'chars':np.array(list('ABEC')),'production':np.array([1.,2.,3.])}
    percent,varco,npvi=M.rhythm_metrics(x)
    assert percent==pytest.approx(40)
    assert varco==pytest.approx(50)
    assert npvi==pytest.approx(100)
    np.testing.assert_allclose(M.word_duration_ratio(x,{**x,'production':x['production']*2}),0)


def test_decode_insertion_not_substitution():
    decode=[{'norm':s,'start':i*.2,'end':(i+1)*.2} for i,s in enumerate(['WE','WE','HOLD','TRUTHS'])]
    ins,errors=M.decode_edits(['WE','HOLD','TRUTHS'],decode)
    assert [v['norm'] for v in ins]==['WE']
    assert errors.sum()==0
    _,errors=M.decode_edits(['WE','HOLD','THESE','TRUTHS'],decode)
    assert errors.sum()>=1


def test_pitch_and_emphasis():
    x={'sentence':np.array([0,0,0,0]),'med_s':np.array([1.,2.,3.,np.nan]),
       'prominence':np.array([0.,1.,-1.,.2]),'norm':np.array(['THE','TRUTH','IS','CLEAR'])}
    b={**x,'med_s':np.array([2.,4.,6.,8.]),'prominence':np.array([0.,0.,2.,0.])}
    assert M.pitch_match(x,b)[0]==pytest.approx(.25)
    assert M.stress_spread(x)==pytest.approx(np.std(x['prominence']))
    np.testing.assert_allclose(M.two_sided_emphasis(x,b),[0,0,3,0])
    assert np.isnan(M.correlation([1,1,1],[2,3,4]))
    assert M.slope([0,1,2],[4,2,0])==pytest.approx(-2)


def test_spectral_gain_invariance():
    a=recording(8)
    b=replace(a,wav=a.wav*.5)
    aa,ae,ash,_,_=M.spectral_arrays(a)
    ba,be,bsh,_,_=M.spectral_arrays(b)
    valid=a.fr.voiced & b.fr.voiced
    assert np.median(np.abs(aa[valid]-ba[valid]))<.1
    assert np.median(np.abs(ae[valid]-be[valid]))<.1
    assert np.median(np.abs(ash[valid]-bsh[valid]))<.01
    np.testing.assert_allclose(M.alpha_relative({'alpha_relative':np.array([-2.,2.])},
                                               {'alpha_relative':np.array([-1.,1.])}),[-1,1])


def test_existing_product_deltas_reused():
    x=recording_arrays(recording(16))
    np.testing.assert_allclose(M.five_word_pace(x,x)[np.isfinite(x['win_T'])],0)
    np.testing.assert_allclose(M.five_word_range(x,x)[np.isfinite(x['win_R'])],0)
    np.testing.assert_allclose(M.five_word_level(x,x)[np.isfinite(x['win_E'])],0)


def test_failure_isolated_and_traceback():
    def fail():raise ValueError('planted failure')
    a=isolated('bad',fail)
    b=isolated('good',lambda:3)
    assert not a['complete'] and 'ValueError: planted failure' in a['error'] and 'Traceback' in a['error']
    assert b['complete'] and b['result']==3


def test_auc_fixed_rate_and_one_to_one_events():
    assert auc([0,0],[1,1])==1
    assert auc([1,1],[1,1])==.5
    score=fixed_rate(np.arange(100),np.arange(100),[0,100,101])
    assert score['false_rate']<=.05
    assert score['found']==2 and score['flaw_n']==3
    e=event_metrics([[1,2],[1.05,2.05]],[[1,2]])
    assert (e['tp'],e['fp'],e['fn'])==(1,1,0)
    assert event_metrics([[1,3]],[[1,2]])['tp']==0


def test_reference_bank_excludes_held_and_repeated_speakers():
    rows=[]
    features={}
    for i in range(16):
        r={'id':f'{i:016x}','source':'gettysburg','text_key':'ONE TWO','speaker_id':str(i),'condition':'volunteer_reading'}
        rows.append(r)
        features[r['id']]={'norm':np.array(['ONE','TWO']),'compat':np.array([i,i+1.])}
    rows.append(rows[0])
    tasks,inventory=normal_plan(rows,features)
    assert inventory[0]['readers']==16
    held={t['participant'] for t in tasks if t['phase']=='held'}
    assert tasks and {t['k'] for t in tasks}=={1,3,5,10}
    for t in tasks:
        assert t['participant'] not in t['references']
        assert not set(t['references'])&held
    ref=median_reference([features[rows[i]['id']] for i in range(3)])
    np.testing.assert_allclose(ref['compat'],[1,2])


def test_label_origin_and_npz_roundtrip(tmp_path):
    dest=tmp_path/'source.tar'/'labels'
    dest.mkdir(parents=True)
    (dest/'utterance.json').write_text(json.dumps({'transcript_a':'We we go.','transcript_b':'We go.'}))
    row={'source':'disfluencyspeech','text':'{D We } we go.','archive':'source.tar','audio_path':'a.wav',
         'label_files':[{'archive':'source.tar','path':'labels/utterance.json'}],'condition':'acted_disfluent'}
    a=annotate(row,tmp_path)
    assert a['text']=='We go.' and a['verbatim']=='We we go.'
    f=tmp_path/'features.npz'
    save_features(f,{'clip':{'array':np.array([1,2])}},[a])
    with np.load(f,allow_pickle=False) as z:
        np.testing.assert_array_equal(z['clip__array'],[1,2])
        assert 'disfluencyspeech' in z['index_json'].item()


def test_budget_keeps_higher_priority():
    rows=[{'source':'poetry','duration':30000,'speaker_id':'p','condition':'x','original_path':'x','audio_path':'p'},
          {'source':'ears','duration':20,'speaker_id':'e','condition':'regular','original_path':'x','audio_path':'e'}]
    kept,skipped,_=select(rows)
    assert [r['source'] for r in kept]==['ears']
    assert skipped[0]['reason']=='three-hour forecast budget'


def test_kernel_metadata_contract():
    root=Path(__file__).resolve().parents[1]
    d=json.loads((root/'kaggle/lab/kernel-metadata.json').read_text())
    assert d['id']=='electroknight/cvoice-lab' and d['is_private'] and d['enable_gpu'] and d['enable_internet']
    assert d['dataset_sources']==['electroknight/cvoice-project'] and d['kernel_sources']==['electroknight/cvoice-data','electroknight/cvoice-data-vctk']


def test_real_podcast_schema_and_negative_clip(tmp_path):
    labels=tmp_path/'podcast-001.tar'/'labels'
    labels.mkdir(parents=True)
    (labels/'PodcastFillers.csv').write_text('pfID,label_full_vocab,event_start_inclip,event_end_inclip\n2,Uh,0.275,0.725\n')
    row={'source':'podcastfillers','condition':'Uh','text':None,'archive':'podcast-001.tar','audio_path':'audio/00000.wav',
         'original_path':'PodcastFillers/audio/clip_wav/validation/00002.wav',
         'label_files':[{'archive':'podcast-001.tar','path':'labels/PodcastFillers.csv'}]}
    labelled=annotate(row,tmp_path)
    assert labelled['events']==[{'start':.275,'end':.725,'kind':'Uh'}]
    assert labelled['missing_text']
    assert grid_text('bbat9p')=='bin blue at t nine please'


def test_style_selection_keeps_baseline_and_balances_events():
    rows=[]
    for style in ('fast','regular','slow','loud','whisper'):
        rows.append({'source':'ears','duration':2,'speaker_id':'p1','condition':style,'text':'One two.',
                     'original_path':'rainbow_1_'+style,'audio_path':style})
    for style in ('Uh','Um','Breath','Repetitions','Words'):
        for i in range(500):
            rows.append({'source':'podcastfillers','duration':1,'speaker_id':None,'condition':style,'text':None,
                         'original_path':str(i),'audio_path':style+str(i)})
    selected,_,estimate=select(rows)
    assert {r['condition'] for r in selected if r['source']=='ears'}=={'fast','regular','slow','loud','whisper'}
    events={style:sum(r['source']=='podcastfillers' and r['condition']==style for r in selected)
            for style in ('Uh','Um','Breath','Repetitions','Words')}
    assert max(events.values())-min(events.values())<=1
    assert estimate<=9900


def test_manifest_audit_uses_real_field_contract():
    row={'source':'mdvr','archive':'mdvr-001.tar','audio_path':'audio/00000.wav','original_path':'ReadText/a.wav',
         'speaker_id':'a','condition':'PD','text':None,'duration':10.,'label_files':[],
         'licence':'CC BY','sha256':'x','sha256_basis':'canonical WAV file bytes'}
    status={'sources':[{'source':'mdvr','complete':True,'parts':[{'file':'mdvr-001.tar'}]}]}
    result=audit([row],status,[row])
    assert not result['schema_errors']
    assert result['selected']['tests']['measure:percentile_span']['potential_recordings']==1
    assert result['selected']['tests']['measure:word_duration_ratio']['potential_recordings']==0


def test_event_precision_includes_other_labelled_clips():
    rows=[{'id':'breath','source':'podcastfillers','missing_text':True,
           'events':[{'start':.3,'end':.8,'kind':'Breath'}]},
          {'id':'words','source':'podcastfillers','missing_text':True,
           'events':[{'start':.3,'end':.8,'kind':'Words'}]}]
    x={'sil':np.array([.5]),'sil_span':np.array([[.3,.8]])}
    result=labelled_events('breath_candidates',rows,{'breath':x,'words':x})[0]
    assert (result['tp'],result['fp'],result['fn'])==(1,1,0)
    assert result['precision']==.5 and result['recordings']==2


def test_phone_scores_can_be_correlated_without_phone_timing():
    rows=[]
    features={}
    for i in range(3):
        clip=str(i)
        rows.append({'id':clip,'source':'speechocean','missing_text':False,'speaker_id':clip,'text_key':'ONE TWO',
                     'scores':{'fluency':9,'prosodic':9,'accuracy':9,'completeness':9},
                     'word_scores':[{'stress':8,'phones-accuracy':[0,1+i*.5]},
                                    {'stress':9,'phones-accuracy':[1,2]}]})
        features[clip]={'value':float(i),'norm':np.array(['ONE','TWO'])}
    result=rank_scores('silence_share',lambda x,b=None:x['value'],rows,features,{})
    assert result['sentence_mean_phone_accuracy']['n']==3
    assert result['sentence_mean_phone_accuracy']['rho']==pytest.approx(1)
    assert not result['phone_level']['available']


def test_merge_data_joins_kernel_outputs(tmp_path, monkeypatch):
    import importlib.util
    spec = importlib.util.spec_from_file_location('lab_run', Path(__file__).parents[1] / 'kaggle' / 'lab' / 'run.py')
    run = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(run)
    mounts = []
    for name, source in (('cvoice-data', 'ears'), ('cvoice-data-vctk', 'vctk')):
        m = tmp_path / name
        m.mkdir()
        (m / f'{source}-001.tar').write_bytes(b'tar')
        (m / 'manifest.json').write_text(json.dumps([{'source': source}]))
        (m / 'STATUS.json').write_text(json.dumps({'sources': [{'source': source, 'complete': True}]}))
        mounts.append(m)
    assert run.merge_data(mounts[:1]) == mounts[0]
    monkeypatch.setattr(run, 'Path', lambda p: tmp_path / 'merged' if p == '/tmp/cvoice-lab-input' else Path(p))
    merged = run.merge_data(mounts)
    assert [r['source'] for r in json.loads((merged / 'manifest.json').read_text())] == ['ears', 'vctk']
    assert json.loads((merged / 'STATUS.json').read_text())['complete']
    assert (merged / 'vctk-001.tar').read_bytes() == b'tar'


def test_kaggle_lab_runner_helpers_equal_build_runner():
    """A Kaggle script kernel uploads one file, so the lab runner keeps a copy of these build-runner helpers."""
    import importlib.util
    import inspect
    modules = []
    for name, path in (('build_run', ('kaggle', 'run.py')), ('lab_run', ('kaggle', 'lab', 'run.py'))):
        spec = importlib.util.spec_from_file_location(name, Path(__file__).parents[1].joinpath(*path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules.append(module)
    shared = ('log', 'write_status', 'sha256_file', 'find_mount', 'unpack_project_zips', 'find_project_root', 'verify_project',
              'child_env', 'sh', 'nvidia_smi', 'detect_gpus', 'device_plan', 'load_config')
    for name in shared:
        assert inspect.getsource(getattr(modules[0], name)) == inspect.getsource(getattr(modules[1], name)), name
