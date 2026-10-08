"""Owner protocol and verified dev_v10 regressions."""
import dataclasses
import json
from types import SimpleNamespace

import numpy as np
import pytest

from cvoice import audio, calibrate, config as C, dataset, evaluate, patterns, pipeline, stress
from cvoice.align import parse_transcript
from cvoice.compare import compare
from cvoice.events import Run, eval_clip, run_pair, truths
from cvoice.passages import sentence_anchors, text_anchors
from cvoice.protocol import exemption_policy, label_eligibility, tiers
from cvoice.r2pool import inventory, partition_hash
from synth import label, local, regime, with_x


def test_source_minutes_do_not_give_a_tiny_text_extra_weight(base, monkeypatch):
    monkeypatch.setattr(C, 'R2_BOOTSTRAPS', 40)
    fit = [calibrate.Null(str(i), compare(base, base), base.tr.sentence, minutes,
                          group=g, source=s, reader=f'{s}:p{i}') for i,(g,s,minutes) in enumerate(
                          [('poetry:tiny','poetry',1.), ('poetry:long','poetry',99.), ('accent:text','accent',100.)])]
    assert calibrate.group_weights(fit) == {'poetry:tiny': .005, 'poetry:long': .495, 'accent:text': .5}
    assert calibrate.pair_weights(fit) == pytest.approx([.005,.495,.5])
    fixed = calibrate.source_weights(fit)
    select = [dataclasses.replace(n, minutes=v) for n,v in zip(fit,[2.,198.,100.])]
    report = calibrate.rate_report(select, [2,0,0], fixed=fixed)
    assert report['rate'] == .005
    assert report['pooled_rate'] == pytest.approx(2/300)
    assert report['bootstrap_upper95'] >= report['rate']
    missing = calibrate.rate_report(select[:2], [2,0], fixed=fixed)
    assert missing['rate'] is None and missing['missing_fit_sources'] == ['accent']


def test_r1_variants_are_one_cluster_and_zero_units_are_not_evidence(base, monkeypatch):
    monkeypatch.setattr(C, 'R2_BOOTSTRAPS', 20)
    nulls = [calibrate.Null(f's__{i}', compare(base,base),base.tr.sentence,1.,reader='s') for i in range(6)]
    reg = calibrate.base_regime('R1', nulls)
    reg['h'] = dict.fromkeys(reg['h'],2.)
    calibrate.null_check(reg, nulls)
    d7 = reg['null']['local_by_key']['D7+']
    assert d7['readers'] == 1 and d7['independent_recording_exposure'] == 1.
    assert d7['rule_of_three'] == 3. and d7['bootstrap_upper95'] is None
    d2 = reg['null']['local_by_key']['D2+']
    assert d2['valid_units'] == 0 and d2['rate'] is None and d2['rule_of_three'] is None
    assert reg['null']['valid_units']['D7+'] > reg['null']['signed_scale_units']['D7+']


def test_clip_null_weighting_uses_minutes_and_pooled_clips_are_separate(base, monkeypatch):
    monkeypatch.setattr(C, 'R2_BOOTSTRAPS', 40)
    nulls = [calibrate.Null(str(i), compare(base,base),base.tr.sentence,minutes,group='accent:text',source='accent',reader=f'accent:p{i}')
             for i,minutes in enumerate((1.,99.))]
    report = calibrate.rate_report(nulls, [1,0], clip=True)
    assert report['rate'] == pytest.approx(.01) and report['pooled_rate'] == .5
    assert report['by_source']['accent']['rate'] == pytest.approx(.01)
    assert report['by_source']['accent']['pooled_rate'] == .5
    assert report['groups']['accent:text']['comparison_minutes'] == 100.
    assert report['bootstrap_upper95'] == 1.


def test_singleton_inventory_exclusions_have_source_and_denominator():
    rows = [dict(id='solo',source='poetry',speaker_id='p',text='We go.',duration_s=30.)]
    pool = inventory(rows)
    assert pool['inventoried_by_source'] == {'poetry': 1}
    assert pool['excluded'][0]['reason'] == 'fewer than two same-text readers'


@pytest.mark.parametrize('seconds', [.02,.04])
def test_d7_short_words_cannot_flag_or_be_listed(base, seconds):
    b,p = base.occ.copy(),base.occ.copy()
    b[3],p[3] = seconds,2*seconds
    B,P = dataclasses.replace(base,occ=b),dataclasses.replace(base,occ=p)
    comp = compare(B,P)
    assert np.isnan(comp.dims['D7'].x[3]) and not comp.dims['D7'].countable[3]
    entries = pipeline.differences(comp,B,P,regime('R2'),[])
    assert not any(e['dimension']=='D7' and e['words']==[3,3] for e in entries)


def test_d7_identity_or_placebo_failure_lists_it_in_r1(base):
    comp = with_x(base,'D7',[(15,15,np.log((1.3+.02)/(.66+.02)))])
    reg = calibrate.base_regime('R1',[])
    gate = calibrate.d7_null_gate(reg,[calibrate.Null('s__identity',comp,base.tr.sentence,1.,'val')])
    assert not gate['passed'] and gate['status']=='listed' and 'D7' not in reg['enabled']
    assert pipeline.listed_dims(reg) == ('D7','D8')
    assert reg['clip']['D7'] is None and reg['h']['D7+'] is None
    clean = calibrate.base_regime('R1',[])
    assert calibrate.d7_null_gate(clean,[calibrate.Null('s__identity',compare(base,base),base.tr.sentence,1.)])['passed']


def test_threshold_selection_only_core_and_lab_passed_and_hashes_exemptions(monkeypatch):
    assert calibrate.calibration_types() == (*C.CORE8_TYPES,'NATURAL_RUSH')
    assert set(tiers()) == {'core8','lab_passed','synthetic_only'}
    assert not calibrate.calibration_clip({'spectrum':'extra','types':['NATURAL_RUSH','LOW_EFFORT']})
    before = exemption_policy()
    monkeypatch.setitem(C.EXPECTED_SECONDARY,'DRAG',('D2',))
    assert exemption_policy()['sha256'] != before['sha256']


def test_natural_rush_whole_clip_truth_is_in_h_objective(base, pinned_detector):
    run = run_pair(base,base,pinned_detector(),'R1')
    reg = regime('R1')
    curve = calibrate.select_r1([(run,label(base,'NATURAL_RUSH'))], [], reg)
    assert all(row['FN'] == 1 and row['per_type_recall']['NATURAL_RUSH'] == 0 for row in curve)
    assert 'fixed whole-clip' in reg['selected_operating_point']['objective']


@pytest.mark.parametrize('reason', ['non-monotone realised ladder','realised change below half target or wrong sign'])
def test_failed_edits_are_a_separate_stratum(base, reason):
    lab = label(base,'LOW_EFFORT')
    lab = label_eligibility(lab,[dict(type='LOW_EFFORT',level=2,reason=reason)])
    run = Run(base,base,with_x(base,'D5',[(10,15,-6.)]),[local('D5',10,15)],None,'R1',{})
    ev = eval_clip(run,lab,secondary_exempt=False)
    assert truths(lab) == [] and len(truths(lab,excluded=True)) == 1
    assert ev['truth'] == [] and ev['false'] == [] and len(ev['shortfalls']) == 1
    coupling = label_eligibility(label(base,'LOW_EFFORT'),[dict(type='LOW_EFFORT',reason='alpha/level coupling outside 0.4–0.7')])
    assert len(truths(coupling)) == 1


def test_unrelated_botched_instance_does_not_inherit_single_ladder_failure(base, tmp_path):
    path = tmp_path / 'lab.json'
    path.write_text(json.dumps(label(base,'LOW_EFFORT')))
    ds = dataset.Dataset(tmp_path, {'realisation_shortfalls': []})
    clip = dict(id='mixed',kind='extra_botched',labels='lab.json',ladder_qa=[dict(type='LOW_EFFORT',reason='non-monotone realised ladder')])
    assert len(truths(ds.labels(clip))) == 1
    clip['realisation_qa'] = [dict(type='LOW_EFFORT',reason='realised change below half target or wrong sign')]
    assert not truths(ds.labels(clip))


def test_gettysburg_outer_crop_does_not_require_internal_sentence_endpoints():
    tr = parse_transcript('We live here. We speak now. We all go home.')
    decoded = [dict(norm=w,start=i*.3,end=i*.3+.2) for i,w in enumerate(tr.norm) if i!=5]
    assert not all(a.eligible for a in sentence_anchors(tr,decoded))
    assert text_anchors(tr,decoded)[0].eligible


@pytest.mark.parametrize('source',['accent','ears','vctk'])
def test_passage_only_sources_never_use_crop_or_asr_filter(tmp_path, monkeypatch, source):
    entries = [dict(id=f'{source}_{sp}',source=source,group='g',reader_id=sp,null_set=sp,duration_s=10.,sha256='original',text='We go.',audio=sp+'.wav') for sp in ('fit','select','lockbox')]
    group = dict(id='g',entries=entries,sets={sp:[r['id'] for r in entries if r['null_set']==sp] for sp in ('fit','select','lockbox')},minutes={},reference_shortfalls={})
    pool = dict(groups=[group],excluded=[],split_sha256=partition_hash([group]))
    monkeypatch.setattr(dataset,'locate_many',lambda *args: pytest.fail('whole passage source sent to ASR crop'))
    dataset.crop_null_readers(tmp_path,pool)
    assert not pool['excluded']
    assert all(r['clip_offset_s']==0 and r['duration_s']==10 and r['sha256']=='original' for r in entries[:2])
    assert 'clip_offset_s' not in entries[-1]


def test_all_accent_readers_survive_inventory_even_over_forecast(monkeypatch):
    monkeypatch.setattr(C,'R2_ALIGNMENT_BUDGET_S',1.)
    rows = [dict(id=str(i),source='accent',speaker_id=str(i),text='We go.',duration_s=30.) for i in range(30)]
    pool = inventory(rows)
    assert sum(len(g['entries']) for g in pool['groups']) == 30 and pool['excluded'] == []


def test_drag_group_includes_word_on_window_shoulder_and_counts_once(base):
    comp = with_x(base,'D7',[(11,11,1.),(16,16,1.)])
    regions = [local('D1',10,14,3.),local('D7',11,11,3.),local('D7',16,16,3.)]
    assert [(g.pattern,g.members) for g in patterns.groups(comp,regions)] == [('DRAG',(0,1,2))]
    assert patterns.counted(comp,regions,[.1,.3,.3]) == {0}


def test_threshold_rows_keep_the_precision_used_in_notes(base):
    reg = regime('R2',h={'D1+':5.05,'D1-':5.05,'D2+':2.05,'D2-':2.5},scales={**C.FLOORS,'D1':.133034,'D2+':.3,'D2-':.39})
    rows = pipeline.rows(compare(base,base),base,base,reg)
    assert next(r for r in rows if r['key']=='pace')['tol'] == [.671822,.671822]
    assert next(r for r in rows if r['key']=='pauses')['tol'] == [.975,.615]


def test_babble_snr_phone_and_room_are_seeded_and_measurable():
    t = np.arange(2*C.SR)/C.SR
    x = .1*np.sin(2*np.pi*200*t)
    donors = [.2*np.sin(2*np.pi*f*t) for f in (317,499,731,887)]
    for snr in (10,20):
        y = stress.babble(x,1,donors,snr)
        assert 10*np.log10(np.mean(x*x)/np.mean((y-x)**2)) == pytest.approx(snr)
        np.testing.assert_array_equal(y,stress.babble(x,1,donors,snr))
        assert not np.array_equal(y,stress.babble(x,2,donors,snr))
    impulse = stress.room_impulse(1)
    tail = impulse[round(.1*C.SR):]
    times = np.arange(len(tail))/C.SR
    slope = np.polyfit(times,10*np.log10(np.cumsum((tail*tail)[::-1])[::-1]+1e-12),1)[0]
    assert -60/slope == pytest.approx(stress.ROOM_RT60_S,abs=.04)
    assert len(stress.phone(x,1))==len(x)


def test_stress_covers_all_kinds_and_seeds_in_bounded_batches(base, pinned_detector, monkeypatch):
    clips = [dict(id=f'c{i}',parent=f's{i%3}',split='train' if i<3 else 'val',kind=kind,regime='R1') for i,kind in enumerate(('identity','single','ladder','extra_botched'))]
    baselines = [dict(id=f's{i}',split='train') for i in range(3)]
    det = pinned_detector()
    ref = run_pair(base,base,det,'R1')
    batches = []
    ds = SimpleNamespace(manifest={'baselines':baselines},pool=None,clips=lambda **kw: clips,recs=lambda rows:[base]*len(rows),
                         prepare_many=lambda items:(batches.append(len(items)) or [base]*len(items)))
    monkeypatch.setattr(evaluate,'reader_ids',lambda *args:[])
    monkeypatch.setattr(evaluate,'clip_runs',lambda *args:[(c,ref,{'flaws':[]}) for c in clips])
    monkeypatch.setattr(stress,'MATRIX',[('white noise 20 dB SNR',stress.noise)])
    monkeypatch.setattr(stress,'apply',lambda fn,w,seed:audio.quantize(w))
    out = evaluate.stress_section(ds,det,('train','val'))
    for condition in ('white noise 20 dB SNR','babble 10 dB SNR','babble 20 dB SNR'):
        assert {(r['clip'],r['seed']) for r in out['flawed_clips'] if r['condition']==condition} == {(c['id'],seed) for c in clips for seed in (1,2,3)}
    assert max(batches)<=8 and all(len(r['added_ci95'])==2 and 'limits' in r and 'passed' not in r for r in out['rows'])
    assert all(c['parent'] not in out['babble_sources'][c['id']] for c in clips)
    assert len(json.dumps(out)) > 0


def test_v9_reference_has_the_verified_decomposition():
    report = evaluate.dev_v9_change({'groups':{'core8':{'by_split_strict':[]}}})
    assert report['verified_v9_to_v10']['train']=={'FP_change':31,'D7':21,'non_D7':10}
    assert report['verified_v9_to_v10']['val']=={'FP_change':17,'D7':11,'non_D7':6}
