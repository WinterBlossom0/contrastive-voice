"""python -m cvoice.lab --data DATA --out OUT [--local]; offline tests, no Kaggle operations."""
from __future__ import annotations

import argparse
from collections import Counter
import io
import json
import os
import hashlib
from pathlib import Path
import resource
import time
import traceback
import zipfile

import numpy as np

from cvoice.pool import PreparePool
from . import EXPECTED_WALL_PER_AUDIO, MAX_SECONDS, RESERVE_SECONDS, SOURCE_ORDER
from .data import annotate, select, unpack, audit
from .evaluate import isolated, normal_plan, pair_plan, measure_test, tables, write_json
from .extract import extract_one
from .measures import MEASURES


def save_features(path, features, rows):
    """NPZ without pickle: clip-id__field arrays plus a UTF-8 JSON index; reanalysis needs no emissions or model."""
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
        for clip,x in features.items():
            for key,value in x.items():
                b=io.BytesIO();np.lib.format.write_array(b,np.asarray(value),allow_pickle=False)
                z.writestr(clip+'__'+key+'.npy',b.getvalue())
        b=io.BytesIO()
        index=[{k:v for k,v in r.items() if k != 'path'} for r in rows]
        np.lib.format.write_array(b,np.asarray(json.dumps(index,ensure_ascii=False)),allow_pickle=False)
        z.writestr('index_json.npy',b.getvalue())


def lab_hashes():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')}


def load_features(path):
    """Inverse of save_features: (features by clip id, annotated rows without 'path')."""
    features={}
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            value=np.lib.format.read_array(io.BytesIO(z.read(name)),allow_pickle=False)
            if name=='index_json.npy':
                rows=json.loads(str(value))
                continue
            clip,key=name[:-len('.npy')].rsplit('__',1)
            features.setdefault(clip,{})[key]=value
    return features,rows


def run_tests(results,annotated,features,out,deadline):
    """Every measure test; results.json is rewritten after each test so that a cut run keeps the finished tests."""
    normal=isolated('normal_plan',normal_plan,annotated,features)
    paired=isolated('pair_plan',pair_plan,annotated,features)
    results['normal_plan']={k:v for k,v in normal.items() if k!='result'}
    results['pair_plan']={k:v for k,v in paired.items() if k!='result'}
    tasks,inventory=normal.get('result',([],[])); pairs=paired.get('result',[])
    for name in MEASURES:
        if deadline is not None and time.monotonic()>deadline:
            results['measures'][name]={'test':name,'complete':False,'error':'run-time budget: test not started; features retained'}
            continue
        results['measures'][name]=isolated(name,measure_test,name,annotated,features,tasks,inventory,pairs)
        print('[lab] test '+name+' '+('complete' if results['measures'][name]['complete'] else 'FAILED'),flush=True)
        write_json(out/'results.json',results)
    write_json(out/'results.json',results)
    (out/'tables.md').write_text(tables(results))
    return normal,paired


def reanalyse(path,out):
    """All measure tests from a saved features.npz; no audio, data mount, model or GPU."""
    out.mkdir(parents=True,exist_ok=True)
    start=time.monotonic()
    features,annotated=load_features(path)
    print(f'[lab] reanalysis of {path}: {len(features)} clips, {len(annotated)} rows',flush=True)
    results={'schema':1,'reanalysis_of':str(path),'provenance':{'lab_sha256':lab_hashes()},'measures':{}}
    normal,paired=run_tests(results,annotated,features,out,None)
    failed=[name for name,r in results['measures'].items() if not r['complete']]
    status={'schema':1,'complete':not failed and normal['complete'] and paired['complete'],'mode':'reanalysis',
            'tests_completed':[n for n,r in results['measures'].items() if r['complete']],'tests_failed':failed,
            'recordings':len(features),'seconds':time.monotonic()-start,
            'max_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
            'scientific_verdicts':dict(Counter(r['result']['verdict'] for r in results['measures'].values() if r['complete']))}
    write_json(out/'STATUS.json',status)
    print('[lab] '+json.dumps(status),flush=True)
    return status


def run(data,out,local=False):
    out.mkdir(parents=True,exist_ok=True)
    start=time.monotonic()
    rows=json.loads((data/'manifest.json').read_text())
    elapsed_bootstrap = 0. if local else max(0.,time.time()-float(os.environ.get('CVOICE_LAB_STARTED',time.time())))
    available = MAX_SECONDS-RESERVE_SECONDS-elapsed_bootstrap
    selected,skipped,estimate=select(rows,local,available)
    input_status=json.loads((data/'STATUS.json').read_text())
    manifest_audit=audit(rows,input_status,selected)
    write_json(out/'manifest_audit.json',manifest_audit)
    budget=dict(manifest_clips=len(rows),selected_clips=len(selected),audio_seconds=sum(r['duration'] for r in selected),
                clips_to_align=sum(bool(r.get('text')) or r['source'] in ('accent','disfluencyspeech','libristutter','lombard') for r in selected),
                expected_minutes=estimate/60,seconds_per_audio_second=EXPECTED_WALL_PER_AUDIO,
                maximum_minutes=180,analysis_reserve_minutes=RESERVE_SECONDS/60,
                bootstrap_seconds=elapsed_bootstrap,
                sources=dict(Counter(r['source'] for r in selected)),
                tests_available=manifest_audit['manifest']['tests'],
                tests_selected=manifest_audit['selected']['tests'],
                forecast='unbenchmarked conservative aggregate T4 x2 forecast; updated from each completed batch')
    print('[lab] time budget '+json.dumps(budget),flush=True)
    root=Path('/tmp/cvoice-lab-local' if local else '/tmp/cvoice-lab-data')
    cache=root/'cache'; cache.mkdir(parents=True,exist_ok=True)
    _,input_status=unpack(data,root,selected)
    annotated=[]; label_errors=[]
    for r in selected:
        test=isolated('labels:'+r['source']+':'+r['audio_path'],annotate,r,root)
        if test['complete']:
            annotated.append(test['result'])
        else:
            label_errors.append(test)
    features={}; extraction=[]; processed_audio=0.; alignment_start=time.monotonic()
    def accept(batch,done):
        nonlocal processed_audio
        for r,result in zip(batch,done):
            extraction.append({k:v for k,v in result.items() if k!='features'})
            if 'features' in result:features[r['id']]=result['features']
            processed_audio+=r['duration']
        print(f'[lab] prepared {len(extraction)}/{len(annotated)} clips; {time.monotonic()-start:.1f}s',flush=True)
    if local:
        for r in annotated:
            if time.monotonic()-start>540:
                skipped.append({'id':r['id'],'source':r['source'],'reason':'local nine-minute deadline'});continue
            accept([r],[extract_one(r,cache,True)])
        pool_stats={'workers':1,'devices':['cpu'],'mode':'in-process; no pool or child process'}
    else:
        with PreparePool(cache_dir=cache) as pool:
            for i in range(0,len(annotated),pool.workers):
                batch=annotated[i:i+pool.workers]
                rate=max(EXPECTED_WALL_PER_AUDIO,(time.monotonic()-alignment_start)/max(processed_audio,1))
                estimate_batch=sum(r['duration'] for r in batch)*rate
                if time.monotonic()-start+estimate_batch>available:
                    skipped.extend({'id':r['id'],'source':r['source'],'reason':'measured three-hour budget'} for r in annotated[i:])
                    break
                try:
                    done=pool.starmap(extract_one,[(r,cache,False) for r in batch])
                    accept(batch,done)
                except Exception:
                    extraction.append({'batch':[r['id'] for r in batch],'error':traceback.format_exc()})
            pool_stats=pool.stats()
    save_features(out/'features.npz',features,annotated)
    results={'schema':1,'budget':budget,'manifest_audit':manifest_audit,
             'normal_reference_scope':'regular EARS/native-English SAA/volunteer readers are competence proxies; no independent competence rating',
             'deferred_checkpoints':json.loads(Path(__file__).with_name('checkpoints.json').read_text()),
             'provenance':{'manifest_sha256':hashlib.sha256((data/'manifest.json').read_bytes()).hexdigest(),
                           'lab_sha256':lab_hashes()},'input_status':input_status,'source_inventory':{},'extraction':extraction,
             'label_errors':label_errors,'skipped':skipped,'measures':{}}
    for source in SOURCE_ORDER:
        source_rows=[r for r in annotated if r['source']==source]
        results['source_inventory'][source]={'manifest_n':sum(r['source']==source for r in rows),'selected_n':len(source_rows),
                                           'aligned_n':sum(r['id'] in features for r in source_rows),
                                           'missing_text_n':sum(r['missing_text'] for r in source_rows),
                                           'condition_counts':dict(Counter(r['condition'] for r in source_rows))}
    deadline=None if local else start+MAX_SECONDS-elapsed_bootstrap-60
    normal,paired=run_tests(results,annotated,features,out,deadline)
    failed=[name for name,r in results['measures'].items() if not r['complete']]
    partial=[name for name,r in results['measures'].items() if r['complete'] and r['result']['errors']]
    status={'schema':1,'complete':not failed and not partial and not label_errors and not input_status.get('lab_unpack_errors')
            and not manifest_audit['schema_errors'] and all('error' not in r for r in extraction)
            and normal['complete'] and paired['complete'],
            'tests_completed':[n for n,r in results['measures'].items() if r['complete']], 'tests_failed':failed, 'tests_with_subtest_errors':partial,
            'recordings_completed':len(features),'recordings_selected':len(annotated),'seconds':time.monotonic()-start,
            'max_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'pool':pool_stats,
            'label_warnings':{r['id']:r['label_errors'] for r in annotated if r['label_errors']},
            'outputs':['results.json','tables.md','features.npz','manifest_audit.json'],'scientific_verdicts':dict(Counter(
                r['result']['verdict'] for r in results['measures'].values() if r['complete'])),
            'input_complete':input_status.get('complete'), 'budget_skipped':len(skipped),
            'completion_meaning':'tests executed; data sufficiency and untested claims are reported separately'}
    write_json(out/'STATUS.json',status)
    print('[lab] '+json.dumps(status),flush=True)
    return status


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data',type=Path);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--features',type=Path,help='saved features.npz: rerun the tests only')
    p.add_argument('--local',action='store_true');a=p.parse_args(argv)
    if (a.data is None)==(a.features is None):
        p.error('give exactly one of --data and --features')
    try:
        if a.features is not None:
            reanalyse(a.features,a.out)
        else:
            run(a.data,a.out,a.local)
    except Exception:
        a.out.mkdir(parents=True,exist_ok=True)
        error=traceback.format_exc()
        write_json(a.out/'STATUS.json',{'complete':False,'error':error})
        print(error,flush=True)
    return 0


if __name__=='__main__':
    raise SystemExit(main())
