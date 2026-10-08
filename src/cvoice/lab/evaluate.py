"""Exploratory, speaker-separated calibration; failures are retained, never used to select measures."""
from __future__ import annotations

from collections import defaultdict
import json
import traceback

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.stats import rankdata, spearmanr

from . import EVENT_TOLERANCE_S, FALSE_RATE, NORMAL_SOURCES, REFERENCE_COUNTS, SEEDS, SOURCE_ORDER
from .measures import MEASURES, FAMILIES, finite, mean, decode_edits
from cvoice.reference import median_reference
from cvoice.align import parse_transcript

ACOUSTIC_ONLY = frozenset(('percentile_span', 'silence_share', 'modulation_depth', 'pitch_level_baseline', 'silence_baseline', 'stability_run', 'breath_candidates', 'alpha_ratio', 'spectral_emphasis', 'mid_band_share'))
OWN_BASELINE = frozenset(('pitch_level_baseline', 'silence_baseline'))
MAXIMUM = frozenset(('latency_residual', 'production_residual', 'word_duration_ratio', 'character_duration_ratio',
                     'within_word_silence', 'greedy_word_error', 'two_sided_emphasis'))
RATIO = frozenset(('pause_count_ratio', 'mean_pause_ratio'))
EVENT_KEYS = {'inserted_material':'inserted_spans', 'orphan_voiced_gap':'orphan_spans',
              'stability_run':'stable_spans', 'within_word_silence':'word_silence_spans',
              'breath_candidates':'sil', 'breath_position':'sil'}
PAIR_STYLES = {'ears': ('regular', ('fast','slow','loud','whisper')), 'avid': ('normal', ('soft','loud','veryloud')),
               'expresso': ('default', ('enunciated','emphasis')), 'lombard': ('plain', ('lombard',))}
PRODUCT_NAMES = frozenset(('five_word_pace','five_word_pause','five_word_range','five_word_level','tempo_irregularity'))
TEXT_REQUIRED = 'independent prompt text, compatible word alignment, and same normalised words for reference comparisons'


def isolated(name, fn, *args):
    try:
        return {'test':name, 'complete':True, 'result':fn(*args)}
    except Exception:
        return {'test':name, 'complete':False, 'error':traceback.format_exc()}


def summary(a):
    a = finite(a)
    if not len(a):
        return {'n':0, 'missing':'no finite measurements'}
    q = np.percentile(a,[5,25,50,75,95])
    return dict(n=len(a), mean=mean(a), sd=float(a.std()), p05=q[0], p25=q[1], median=q[2], p75=q[3], p95=q[4], iqr=q[3]-q[1])


def auc(negative, positive):
    a,z = finite(negative),finite(positive)
    if not len(a) or not len(z):
        return np.nan
    ranks = rankdata(np.r_[a,z])
    return float((ranks[len(a):].sum()-len(z)*(len(z)+1)/2)/(len(a)*len(z)))


def fixed_rate(calibration, held, flaws):
    """Strict > empirical upper order statistic; 5% is a target, held-out achieved rate is reported with counts."""
    cal, held, flaws = finite(calibration), finite(held), finite(flaws)
    if len(cal) < 20 or len(held) < 5:
        return {'available':False, 'missing':'need ≥20 calibration contrasts and ≥5 held-out contrasts',
                'calibration_n':len(cal), 'held_n':len(held), 'flaw_n':len(flaws)}
    index = min(len(cal)-1, int(np.ceil((1-FALSE_RATE)*(len(cal)+1)))-1)
    threshold = float(np.sort(cal)[index])
    nf, tp = int((held>threshold).sum()),int((flaws>threshold).sum())
    return dict(available=True, target_false_rate=FALSE_RATE, threshold=threshold, rule='strict greater than',
                calibration_n=len(cal), false_flags=nf, normal_n=len(held), false_rate=nf/len(held),
                found=tp, flaw_n=len(flaws), found_share=tp/len(flaws) if len(flaws) else None)


def event_metrics(predicted, labelled, tolerance=EVENT_TOLERANCE_S):
    """One-to-one maximum-cardinality interval match: both start and end within ±0.20 s; no overlap-only credit."""
    p,z = np.asarray(predicted,float).reshape(-1,2),np.asarray(labelled,float).reshape(-1,2)
    tp = 0
    if len(p) and len(z):
        distance = np.max(np.abs(p[:,None]-z[None]),axis=2)
        cost = np.where(distance<=tolerance,distance,1e6)
        a,b = linear_sum_assignment(cost)
        tp = int((distance[a,b]<=tolerance).sum())
    return dict(tp=tp,fp=len(p)-tp,fn=len(z)-tp,predicted_n=len(p),labelled_n=len(z),
                precision=tp/len(p) if len(p) else None,recall=tp/len(z) if len(z) else None,
                tolerance_seconds=tolerance,matching='both interval edges within tolerance; one-to-one')


def reader(row):
    speaker = row.get('speaker_id')
    if row['source'] == 'poetry' and speaker:
        # IA takes sometimes suffix a repeat number to the same reader's initials.
        import re
        speaker = re.sub(r'\d+$','',speaker)
    return speaker


def normal_reader(row):
    if row['source'] not in NORMAL_SOURCES:
        return False
    if row['source'] == 'ears':
        return row['condition']=='regular'
    if row['source'] == 'accent':
        return (row.get('speaker_id') or '').startswith('english')
    return True



def case_reference(case, features, band_envelopes):
    """Median reference of a normal case, kept on the case: it is the same for every measure test (Kaggle lab v1:
    recomputing it took about 210 s per test)."""
    key = '_reference_band' if band_envelopes else '_reference'
    if key not in case:
        refs = [features[clip] for clip in case['references']]
        if not band_envelopes:
            refs = [{name: value for name, value in ref.items() if name != 'band_envelopes'} for ref in refs]
        case[key] = median_reference(refs)
    return case[key]


def normal_plan(rows, features):
    groups=defaultdict(dict)
    for r in rows:
        if normal_reader(r) and r['id'] in features and r.get('text_key') and reader(r):
            groups[(r['source'],r['text_key'])].setdefault(reader(r),r)
    tasks, inventory = [],[]
    splits={}
    for source in NORMAL_SOURCES:
        speakers=sorted({speaker for (s,_),group in groups.items() if s==source for speaker in group})
        np.random.default_rng(SEEDS[0]).shuffle(speakers)
        split=min(max(1,len(speakers)-1),max(2,int(np.ceil(.7*len(speakers)))))
        splits[source]=set(speakers[:split])
    for (source,text), speakers in sorted(groups.items()):
        members=[speakers[s] for s in sorted(speakers)]
        # Disjoint participant speakers; fixed training reference bank, no held-out speaker in any reference.
        bank=[r for r in members if reader(r) in splits[source]]
        held=[r for r in members if reader(r) not in splits[source]]
        inventory.append({'source':source,'text':text,'readers':len(members),'bank':len(bank),'held':len(held)})
        if not held:
            continue
        for k in REFERENCE_COUNTS:
            for phase,targets in (('calibration',bank),('held',held)):
                for row in targets:
                    refs=[r for r in bank if reader(r)!=reader(row)]
                    if len(refs)<k:continue
                    for seed in SEEDS:
                        rng=np.random.default_rng(seed+int(row['id'][:6],16))
                        chosen=[refs[i] for i in rng.choice(len(refs),k,replace=False)]
                        tasks.append({'source':source,'k':k,'phase':phase,'participant':row['id'],
                                      'references':[r['id'] for r in chosen], 'seed':seed,'reader':reader(row),
                                      'x':features[row['id']], 'b':None})
    return tasks,inventory


def pair_plan(rows,features):
    groups=defaultdict(list)
    for r in rows:
        if r['source'] in PAIR_STYLES and r['id'] in features and r.get('text_key') and reader(r):
            groups[(r['source'],reader(r),r['text_key'])].append(r)
    pairs=[]
    for (source,speaker,text),group in groups.items():
        base,styles=PAIR_STYLES[source]
        for p in group:
            if p['condition'] not in styles:
                continue
            refs=[r for r in group if r['condition']==base]
            if source=='avid':
                import re
                session=re.search(r'_s([12])_',p['original_path'])
                refs=[r for r in refs if session and '_s'+session[1]+'_' in r['original_path']]
            if not refs:
                continue
            ref=sorted(refs,key=lambda r:r['original_path'])[0]
            pairs.append({'source':source,'style':p['condition'] + '_vs_' + base,'speaker':speaker,
                          'participant':p['id'],'reference':ref['id'],'x':features[p['id']],'b':features[ref['id']]})
    for (source,speaker,text),group in groups.items():
        if source != 'avid':continue
        import re
        for p in group:
            if p['condition'] != 'soft':continue
            session = re.search(r'_s([12])_',p['original_path'])
            refs = [r for r in group if r['condition'] == 'loud' and session and '_s'+session[1]+'_' in r['original_path']]
            if refs:
                ref = sorted(refs,key=lambda r:r['original_path'])[0]
                pairs.append({'source':source,'style':'soft_vs_loud','speaker':speaker,'participant':p['id'],
                              'reference':ref['id'],'x':features[p['id']],'b':features[ref['id']]})
    return pairs


def severity(name, value, reference=True):
    v=finite(value)
    if not len(v):
        return np.nan
    if reference and name in RATIO:
        v=v-1
    v=np.abs(v)
    return float(v.max()) if name in MAXIMUM else mean(v)


def eligible(name,row,features):
    return row['id'] in features and (not row['missing_text'] or name in ACOUSTIC_ONLY)


REFERENCE_MEASURES = frozenset(('latency_contour','production_contour','latency_residual','production_residual',
    'tempo_irregularity','five_word_pace','five_word_pause','five_word_range','pitch_match','prominence_agreement',
    'two_sided_emphasis','band_envelope_match','five_word_level','word_duration_ratio','character_duration_ratio',
    'speech_time_ratio','pause_count_ratio','mean_pause_ratio'))


def rank_scores(name,fn,rows,features,fixed):
    by=defaultdict(list); scored_departures=defaultdict(list); references=defaultdict(list)
    speech=[r for r in rows if r['source']=='speechocean' and eligible(name,r,features)]
    for r in speech:
        s=r['scores']
        if all(s.get(k,-1)>=8 for k in ('fluency','prosodic','accuracy','completeness')):
            references[r['text_key']].append(r)
    missing_reference=0
    for r in speech:
        x=features[r['id']]
        refs=sorted((ref for ref in references[r['text_key']] if reader(ref)!=reader(r)),key=lambda v:v['id'])
        b=features[refs[0]['id']] if refs else None
        if b is None and name in REFERENCE_MEASURES:
            missing_reference+=1; continue
        values=fn(x,b)
        value=mean(values)
        for key,score in r['scores'].items():
            if np.isscalar(score):
                by['sentence_'+key].append((value,float(score),r['id']))
                if b is not None and float(score)<=5:
                    scored_departures['sentence_'+key].append(severity(name,values))
        word=r.get('word_scores',[])
        if word:
            stress=[w['stress'] for w in word if 'stress' in w]
            phones=[phone for w in word for phone in w.get('phones-accuracy',w.get('phones_accuracy',[]))]
            if stress:by['sentence_mean_word_stress'].append((value,mean(stress),r['id']))
            if phones:by['sentence_mean_phone_accuracy'].append((value,mean(phones),r['id']))
            if len(word)!=len(x['norm']):
                missing_reference += 1
                continue
            vals=np.asarray(values)
            if vals.shape==(len(word),):
                for i,w in enumerate(word):
                    for key in ('accuracy','stress','total'):
                        if key in w:
                            by['word_'+key].append((vals[i],float(w[key]),r['id']))
                    phones=w.get('phones-accuracy',w.get('phones_accuracy',[]))
                    if phones:
                        by['word_mean_phone_accuracy'].append((vals[i],mean(phones),r['id']))
    output={}
    for key,vals in by.items():
        a,z,_=zip(*vals); a,z=np.asarray(a),np.asarray(z);ok=np.isfinite(a)&np.isfinite(z)
        output[key]={'n':int(ok.sum()),'recordings':len({v[2] for v in vals}),
            'rho':float(spearmanr(a[ok],z[ok]).statistic) if ok.sum()>=3 and np.std(a[ok]) and np.std(z[ok]) else None,
            'missing_n':int((~ok).sum()),
            'predictor':'same-text high-score reference if present, otherwise intrinsic measure; no replacement proxy',
            'found_at_fixed_rate':{k:fixed_rate(v['cal'],v['held'],scored_departures[key])
                for k,v in fixed.items() if k.endswith(':k1') and key.startswith('sentence_')},
            'low_score_rule':'original sentence score ≤5/10; derived mean stress/phone scores are correlation targets only'}
    if not output:
        return {'available':False,'missing':'scored SpeechOcean audio/labels or required same-text high-score reference absent',
                'missing_reference_n':missing_reference}
    output['missing_reference_n']=missing_reference
    output['phone_level']={'available':False,'missing':'character CTC is not phone alignment; word-mean phone scores only'}
    return output


def prominence_scores(name,rows,features):
    if name == 'two_sided_emphasis':
        return {'available':False,'missing':'prominence annotations do not label misplaced/omitted emphasis; same-text normative reference absent'}
    if name not in ('prominence_agreement','stress_spread'):
        return {'available':False,'missing':'not a prominence predictor'}
    values=[];labels=[];recordings=set()
    for r in rows:
        if r['source']!='prominence' or r['id'] not in features:continue
        x=features[r['id']]
        annotations=r.get('prominence_labels',[])
        if name=='stress_spread' and annotations:
            values.append(MEASURES[name](x))
            labels.append(mean([np.std(a['score']) for a in annotations]))
            recordings.add(r['id']);continue
        for a in annotations:
            if len(a['words'])!=len(a['score']):raise ValueError('prominence word/score length mismatch')
            for (word,start,end),label in zip(a['words'],a['score']):
                mid=(x['start']+x['end'])/2
                ix=np.flatnonzero((mid>=start)&(mid<end))
                if len(ix):
                    values.append(mean(x['prominence'][ix]));labels.append(float(label));recordings.add(r['id'])
    a,z=np.asarray(values),np.asarray(labels);ok=np.isfinite(a)&np.isfinite(z);a,z=a[ok],z[ok]
    result={'available':bool(len(a)),'recordings':len(recordings),'n':len(a),
            'rho':float(spearmanr(a,z).statistic) if len(a)>=3 and np.std(a) and np.std(z) else None,
            'target':'annotation spread per clip' if name=='stress_spread' else 'raw prominence component vs prominent-word annotation',
            'component_only':name=='prominence_agreement',
            'flaw_labels':False,'missing':None if len(a) else 'LibriTTS prominence-labelled audio absent'}
    if name=='prominence_agreement':
        pred=a>=.75;truth=z>=.5;tp=int((pred&truth).sum())
        result.update(auc=auc(a[~truth],a[truth]),tp=tp,fp=int((pred&~truth).sum()),fn=int((~pred&truth).sum()),
            precision=tp/int(pred.sum()) if pred.any() else None,recall=tp/int(truth.sum()) if truth.any() else None,
            prediction_threshold=.75,annotation_threshold=.5)
    return result


def candidate_spans(name,x):
    key=EVENT_KEYS[name]
    if key.endswith('spans'):
        return x[key]
    if key=='word_silence':
        ix=np.flatnonzero(x[key]>0)
        return np.column_stack([x['start'][ix],x['end'][ix]])
    ix=np.flatnonzero(x['sil']>=.25)
    return x['sil_span'][ix]


def labelled_events(name,rows,features):
    if name not in EVENT_KEYS:
        return {'available':False,'missing':'no timestamp event detector is defined for this measure'}
    results=[]
    for source in ('podcastfillers','libristutter'):
        tp=fp=fn=clips=0
        for r in rows:
            if r['source']!=source or not eligible(name,r,features) or not r['events']:
                continue
            labels=r['events']
            if source=='podcastfillers':
                kinds=('Breath',) if name.startswith('breath') else ('Uh','Um','Repetitions')
                labels=[e for e in labels if e['kind'] in kinds]
            pred=candidate_spans(name,features[r['id']])
            score=event_metrics(pred,[(e['start'],e['end']) for e in labels])
            tp+=score['tp']; fp+=score['fp']; fn+=score['fn']; clips+=1
        results.append({'source':source,'available':bool(clips),'recordings':clips,'tp':tp,'fp':fp,'fn':fn,
                        'precision':tp/(tp+fp) if tp+fp else None,'recall':tp/(tp+fn) if tp+fn else None,
                        'tolerance_seconds':EVENT_TOLERANCE_S,
                        'threshold':'stated candidate rule, not a fitted event threshold',
                        'missing':None if clips else 'independent transcript and compatible timestamp labels absent',
                        'synthetic':source=='libristutter'})
    return results


def attach_product_deltas(name,case,reference):
    """The six product deltas share one compare call per contrast across all measure tests."""
    if name not in PRODUCT_NAMES:return
    if 'product_deltas' not in case:
        from cvoice.compare import compare
        from .extract import recording_view
        comparison = compare(recording_view(reference),recording_view(case['x']))
        case['product_deltas'] = {key:dim.x for key,dim in comparison.dims.items()}
    reference['_product_deltas'] = case['product_deltas']


def measure_test(name,rows,features,normals,inventory,pairs):
    fn=MEASURES[name]
    usable=[r for r in rows if eligible(name,r,features)]
    errors=[]; raw={}
    for r in usable:
        test=isolated('recording:'+r['id'],fn,features[r['id']])
        if test['complete']:
            raw[r['id']]=test['result']
        else:
            errors.append(test)
    normal={}; responses={}; fixed={}
    for source in NORMAL_SOURCES:
        normal[source]={}
        for k in REFERENCE_COUNTS:
            cases=[t for t in normals if t['source']==source and t['k']==k]
            phases=defaultdict(list); values=[]; participant_scores=defaultdict(list); seed_scores=defaultdict(list)
            for t in cases:
                if bool(t['x'].get('prompt_proxy', False)) and name not in ACOUSTIC_ONLY:
                    continue
                reference = case_reference(t, features, name == 'band_envelope_match')
                if bool(t['x'].get('prompt_proxy', False)) and name == 'breath_candidates':
                    refs = [features[clip] for clip in t['references']]
                    result=isolated('normal:'+t['participant'],lambda: fn(t['x'])-np.median([fn(ref) for ref in refs]))
                else:
                    def normal_measure():
                        attach_product_deltas(name,t,reference)
                        return fn(t['x'],reference)
                    result=isolated('normal:'+t['participant'],normal_measure)
                if not result['complete']:
                    errors.append(result); continue
                score=severity(name,result['result'])
                participant_scores[(t['phase'],t['reader'])].append(score); values.append(score)
                seed_scores[t['seed']].append(score)
            for (phase,participant),scores_by_seed in participant_scores.items():
                phases[phase].append(mean(scores_by_seed))
            normal[source][str(k)]={'spread':summary(values), 'calibration':summary(phases['calibration']),
                                    'held':summary(phases['held']), 'participants':len({t['reader'] for t in cases}),
                                    'spread_by_seed':{str(seed):summary(v) for seed,v in seed_scores.items()},
                                    'calibration_unit':'participant mean across reference draws; repeats do not inflate counts',
                                    'comparison_unit':'mean absolute departure; largest residual for local event measures',
                                    'missing':None if cases else f'need >{k} distinct bank readers and held-out readers of same text'}
            fixed[f'{source}:k{k}']={'cal':phases['calibration'],'held':phases['held']}
    by=defaultdict(list)
    for p in pairs:
        def paired_measure():
            reference = dict(p['b'])
            attach_product_deltas(name,p,reference)
            return fn(p['x'],reference)
        result=isolated('pair:'+p['participant'],paired_measure)
        if result['complete']:
            value = mean(result['result']) - (1 if name in RATIO else 0)
            by[p['source']+':'+p['style']].append((value,severity(name,result['result']),p['speaker']))
        else:
            errors.append(result)
    verdicts=[]
    for key,items in by.items():
        signed,departures,_=zip(*items)
        signed=finite(signed); departures=finite(departures)
        sd=float(signed.std(ddof=1)) if len(signed)>1 else 0
        delta=mean(signed)
        dz=delta/sd if sd>0 else None
        grouped=defaultdict(list)
        for v,_,speaker in items:grouped[speaker].append(v)
        speaker_values=finite([mean(v) for v in grouped.values()])
        speaker_sd=float(speaker_values.std(ddof=1)) if len(speaker_values)>1 else 0
        responses[key]={'n':len(departures),'speakers':len({v[2] for v in items}),'signed_response':summary(signed),
                        'departure':summary(departures),'paired_dz':dz,
                        'speaker_mean_response':summary(speaker_values),
                        'paired_dz_by_speaker':mean(speaker_values)/speaker_sd if speaker_sd else None,
                        'effect_unit':'mean signed participant/reference response; paired dz uses response SD',
                        'direction':'style contrast, not a human flaw judgement', 'auc_against_normal':{},'found_at_fixed_rate':{}}
        for normkey,v in fixed.items():
            responses[key]['auc_against_normal'][normkey]=auc(v['held'],departures)
            found=fixed_rate(v['cal'],v['held'],departures)
            responses[key]['found_at_fixed_rate'][normkey]=found
            if found.get('available') and found['normal_n']>=20 and found['flaw_n']>=10:
                verdicts.append(found)
    for source in NORMAL_SOURCES:
        base_iqr=normal[source]['1']['spread'].get('iqr',0)
        for k in REFERENCE_COUNTS:
            spread=normal[source][str(k)]['spread']
            normal[source][str(k)]['iqr_relative_to_k1']=spread.get('iqr',np.nan)/base_iqr if base_iqr else None
    raw_detection={}
    for source in NORMAL_SOURCES:
        cal_ids={t['participant'] for t in normals if t['source']==source and t['k']==1 and t['phase']=='calibration'}
        held_ids={t['participant'] for t in normals if t['source']==source and t['k']==1 and t['phase']=='held'}
        cal=[severity(name,raw[c],False) for c in cal_ids if c in raw]
        held=[severity(name,raw[c],False) for c in held_ids if c in raw]
        targets = [('podcastfillers',kind) for kind in ('Uh','Um','Breath','Repetitions')]
        targets += [('libristutter',None),('mdvr','PD')]
        for target,kind in targets:
            target_rows=[r for r in usable if r['source']==target and r['id'] in raw and
                         (r['condition']==kind if target=='mdvr' else bool(r['events']))]
            flaw_rows=[r for r in target_rows if target=='mdvr' or any(
                       e['kind']==kind if kind is not None else e['kind']!='Words' for e in r['events'])]
            detection=fixed_rate(cal,held,[severity(name,raw[r['id']],False) for r in flaw_rows])
            if detection.get('available') and name in EVENT_KEYS and target!='mdvr':
                tp=fp=fn_count=0
                for r in target_rows:
                    x=features[r['id']]
                    pred=candidate_spans(name,x) if severity(name,raw[r['id']],False)>detection['threshold'] else []
                    truth=[(e['start'],e['end']) for e in r['events'] if kind is None or e['kind']==kind]
                    score=event_metrics(pred,truth)
                    tp+=score['tp'];fp+=score['fp'];fn_count+=score['fn']
                detection['localized_events']={'tp':tp,'fp':fp,'fn':fn_count,'recordings':len(target_rows),
                    'precision':tp/(tp+fp) if tp+fp else None,'recall':tp/(tp+fn_count) if tp+fn_count else None,
                    'tolerance_seconds':EVENT_TOLERANCE_S,
                    'threshold_scope':'clip departure gates the stated event-candidate rule; transferred reader calibration'}
            raw_detection[source+':'+target+(':'+kind if kind is not None else '')]=detection
    scores=isolated('scores',rank_scores,name,fn,rows,features,fixed)
    prominence=isolated('prominence',prominence_scores,name,rows,features)
    events=isolated('events',labelled_events,name,rows,features)
    if not scores['complete']: errors.append(scores)
    if not events['complete']: errors.append(events)
    if not prominence['complete']: errors.append(prominence)
    clinical={}
    for condition in ('HC','PD'):
        clinical[condition]=[mean(raw[r['id']]) for r in usable if r['source']=='mdvr'
                            and condition.upper() in r['condition'].upper() and r['id'] in raw]
    patient,control=finite(clinical['PD']),finite(clinical['HC'])
    pooled=np.sqrt(((len(patient)-1)*np.var(patient,ddof=1)+(len(control)-1)*np.var(control,ddof=1))
                   /(len(patient)+len(control)-2)) if len(patient)>1 and len(control)>1 else 0.
    clinical={'cohen_d':(mean(patient)-mean(control))/pooled if pooled else None,'patient_n':len(patient),'control_n':len(control),'auc':auc(control,patient),
              'missing':None if len(patient) and len(control) else 'MDVR audio, cohort label or independent transcript absent',
              'confounds':'patient/control group contrast; no same-speaker pairing, not a diagnosis'}
    verbatim=[]
    if name=='inserted_material':
        for r in usable:
            if r.get('verbatim'):
                words=[{'norm':w} for w in parse_transcript(r['verbatim']).norm]
                independent=len(decode_edits(features[r['id']]['norm'],words)[0])
                verbatim.append((mean(raw.get(r['id'],np.nan)),independent))
    transcript_test={'n':len(verbatim),'rho':None,'missing':'verbatim event counts only, no timestamps'}
    if len(verbatim)>=3:
        a,z=np.asarray(verbatim).T
        if np.std(a) and np.std(z):transcript_test['rho']=float(spearmanr(a,z).statistic)
    if name in OWN_BASELINE:
        verdict='Anxiety labels missing'
    elif not usable:
        verdict='Required data missing'
    elif not verdicts:
        verdict='More readers needed'
    else:
        # No universal winner from pooling different normal corpora; the table uses the conservative all-corpora result.
        verdict='Separates tested contrast' if all(v['false_rate']<=FALSE_RATE and v['found_share']>=.5 for v in verdicts) else 'Overlaps reader variation'
    requirements=[]
    if name not in ACOUSTIC_ONLY:
        requirements.append(TEXT_REQUIRED)
    if name in OWN_BASELINE:
        requirements.append('same speaker calm/anxious pairs with anxiety labels; EARS/AVID styles only test cue response')
    if name=='character_duration_ratio' or name=='rhythm_metrics':
        requirements.append('character timing is computable; phone/vowel interval validation needs phone alignment')
    data_used={s:{'recordings':[r['id'] for r in usable if r['source']==s],
                  'licences':sorted({r['licence'] for r in usable if r['source']==s})}
               for s in SOURCE_ORDER if any(r['source']==s for r in usable)}
    return {'definition':fn.__doc__, 'computable':any(len(finite(value)) for value in raw.values()), 'requirements':requirements,'data_used':data_used,
            'counts':{'selected':len(rows),'usable':len(usable),'computed':sum(bool(len(finite(v))) for v in raw.values()),'executed':len(raw),'errors':len(errors),
                      'pairs':sum(len(v) for v in by.values())},
            'normal':normal,'normal_groups':inventory,'paired':responses,'scores':scores,'events':events,
            'clip_detection_at_fixed_rate':raw_detection,
            'clip_detection_scope':'intrinsic raw measure against competent-reader raw distribution; cross-corpus transfer, duration/channel confounds',
            'clinical':clinical,'prominence_labels':prominence,'verbatim':transcript_test,'errors':errors,'verdict':verdict,
            'missing_sources':[s for s in SOURCE_ORDER if not any(r['source']==s for r in rows)],
            'untested_ground_truth':['healthy trailing-off judgements','monotone/repeated-contour/ending direction labels',
                                    'real anxious vs calm reading','natural stuttering subtype audio (SEP-28k labels only)'],
            'per_recording_values':{key:summary(value) for key,value in raw.items()},
            'computability_by_source':{s:{'usable_n':sum(r['source']==s for r in usable),
                'missing_text_n':sum(r['source']==s and r['missing_text'] for r in rows),
                'missing':None if any(r['source']==s for r in usable) else 'audio, independent text or alignment absent'}
                for s in SOURCE_ORDER},
            'pairing_gaps':{s:{'required_baseline':baseline,'conditions':styles,
                'matched_n':sum(p['source']==s for p in pairs),
                'missing':'requires same speaker/session and exactly the same parsed words, including emphasis demos'}
                for s,(baseline,styles) in PAIR_STYLES.items()},
            'units_missing':{key:int(np.size(value)-len(finite(value))) for key,value in raw.items()}}


def canon(value):
    if isinstance(value,dict):return {str(k):canon(v) for k,v in value.items()}
    if isinstance(value,np.ndarray):return [canon(v) for v in value] if value.ndim else canon(value.item())
    if isinstance(value,(list,tuple)):return [canon(v) for v in value]
    if isinstance(value,(float,np.floating)):return float(value) if np.isfinite(value) else None
    if isinstance(value,(np.integer,np.bool_)):return value.item()
    return value


def write_json(path,value):
    path.write_text(json.dumps(canon(value),ensure_ascii=False,indent=1,allow_nan=False))


def tables(results):
    lines=['Exploratory results. False-rate target 5%; held participants never enter the training reference bank.',
           'Style instructions and synthetic stutters are identified as contrasts; they are not rated healthy delivery flaws.',
           'The compact row shows EARS normal k=1; results.json retains every source, k, contrast, count and error.','']
    for family,fns in FAMILIES.items():
        lines+=['## '+family,'','| Measure | Computable? | Normal spread | Real contrast response | Found at fixed false rate | Verdict |',
                '|---|---|---|---|---|---|']
        for fn in fns:
            record=results['measures'][fn.__name__]
            if not record['complete']:
                lines.append(f'| {fn.__name__} | error | — | — | — | Test execution failed |');continue
            r=record['result']; normal=r['normal']['ears']['1']['held']
            spread=f"IQR {normal['iqr']:.3g}; n={normal['n']}" if normal['n'] else 'insufficient readers'
            responses=[];found=[]
            for key,p in r['paired'].items():
                dz=p['paired_dz']; a=p['auc_against_normal'].get('ears:k1')
                responses.append(f"{key} n={p['n']}, dz={dz:.2g}, AUC={a:.2g}" if dz is not None and np.isfinite(a)
                                 else f"{key} n={p['n']}")
                f=p['found_at_fixed_rate'].get('ears:k1',{})
                if f.get('available'):
                    found.append(f"{key} {f['found']}/{f['flaw_n']}; false {f['false_flags']}/{f['normal_n']}")
            score_result=r['scores'].get('result',{})
            for key,v in score_result.items():
                if isinstance(v,dict) and 'rho' in v:
                    rho=v['rho'];responses.append(f"{key} n={v['n']}, rho={rho:.2g}" if rho is not None else f"{key} n={v['n']}, rho undefined")
            for v in r['events'].get('result',[]) if isinstance(r['events'].get('result'),list) else []:
                if v.get('available'):
                    responses.append(f"{v['source']} events TP/FP/FN={v['tp']}/{v['fp']}/{v['fn']} ±{v['tolerance_seconds']}s")
            c=r['clinical']
            if c['patient_n'] and c['control_n']:
                responses.append(f"MDVR PD/HC={c['patient_n']}/{c['control_n']}, AUC={c['auc']:.2g}")
            for key,v in r['clip_detection_at_fixed_rate'].items():
                if key.startswith('ears:') and v.get('available') and v['flaw_n']:
                    found.append(f"{key} clips {v['found']}/{v['flaw_n']}; false {v['false_flags']}/{v['normal_n']}")
            for v in score_result.values():
                if isinstance(v,dict):
                    f=v.get('found_at_fixed_rate',{}).get('ears:k1',{})
                    if f.get('available') and f['flaw_n']:
                        found.append(f"low score {f['found']}/{f['flaw_n']}; false {f['false_flags']}/{f['normal_n']}")
            lines.append(f"| {fn.__name__} | {'yes' if r['computable'] else 'no'} ({r['counts']['computed']}) | {spread} | "
                         f"{'<br>'.join(responses) or 'ground truth absent'} | {'<br>'.join(found) or 'threshold unavailable'} | {r['verdict']} |")
        lines.append('')
    return '\n'.join(lines)
