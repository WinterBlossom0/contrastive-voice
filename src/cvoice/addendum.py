"""Evaluation addendum, computed after the final evaluation from its saved outputs (no Kaggle run, no new measurement).

    python -m cvoice.addendum --run <final run folder> \
        --first-final docs/evidence_final_32cdd86f3d6e/results.json [--cache <alignment cache>]

Reads <run>/eval/results.json, <run>/models/{detector.json,final_evaluations.json}, <run>/calibration/report.json and the
saved dataset <run>/data/dataset; writes <run>/eval/addendum.json and <run>/eval/addendum.md. The tables from results.json
are rebuilt from its numbers. The local part re-runs the frozen detector on the saved audio on CPU; it first checks that
its strict counts equal the saved ones. --reuse-local takes the local part from an existing addendum.json.
"""
from __future__ import annotations

import argparse
import copy
import dataclasses
import json
import time
from collections import Counter, defaultdict
from pathlib import Path

from . import config as C
from .calibrate import Null, calibration_clip, r1_items, r1_noise_items
from .compare import compare
from .dataset import sha256_file
from .detect import fit_scales, key, load_detector
from .events import Run, cluster_f1, eval_clip, f1, on_shortfall, truths
from .evaluate import (ALL_SPLITS, COUNT_ONCE_RULE, EXPECTED, LEVEL_GROUPS, PRE_REGISTERED, bounds_text, every_prediction, interval_text, md_cell,
                       md_table, pre_registered, reference_free, reference_free_run, speaker_stress_row, split_groups, strict_counts,
                       tier_labels)
from .explain import FLAW_TYPE, clip_type
from .patterns import annotate, within_half_window
from .protocol import STRICT_ACCOUNTING, tiers
from .uncertainty import MIN_BOOTSTRAP_CLUSTERS, cluster_summary, wilson

COUNT_ONCE = 'introduced after the plan: ' + STRICT_ACCOUNTING
PLAN = 'docs/FINAL_EVALUATION_PLAN.md item 4'
PROVENANCE = ('Computed after the final evaluation by `python -m cvoice.addendum` (src/cvoice/addendum.py) from the saved '
              'outputs of the final run; no number below was measured on Kaggle again.')
EXPECTATION_DIMS = ('D1', 'D2', 'D3', 'D5')  # the dimensions the pre-registered R2 level-3 expectation names (pace, pauses, pitch, volume)
READER_UNIT = {'single': 'Each of the 3 check readers counts once per calibration reference',
               'consensus5': 'Each check reader is compared once with the median of 5 calibration readers'}


# ============================================================================================ formatting
def kn(k, n) -> str:
    return f'{md_cell(k)}/{md_cell(n)}'


def saved_f1_interval(row: dict, split: str) -> str:
    """The saved F1 interval of a headline row, labelled by what it is."""
    if row.get('f1_per_speaker'):
        return interval_text(None, row['f1_per_speaker'], row.get('f1_range'))
    ci = row.get('f1_ci95')
    if ci and ci[0] is not None:
        scope = 'in-sample, ' if split == 'train' else ''
        return f"{bounds_text(ci, 'percentile bootstrap')} ({scope}{MIN_BOOTSTRAP_CLUSTERS} speaker clusters, coverage not assured)"
    return 'n/a'


# ============================================================================================ accounting
def strict_rows(results: dict, tier: str) -> list[dict]:
    return [r for r in results['headline']['groups'][tier]['by_split_strict'] if r['group'] == 'all']


def accounting_section(results: dict, first: dict, per_speaker: dict | None) -> dict:
    """Per tier, levels and split (train, val, test, val+test): the pre-registered accounting first, the count-once
    accounting beside it, and for core8 the first final evaluation (all predictions counted, earlier config)."""
    first_rows = {(r['levels'], r['split']): r for r in first['headline']['by_split_strict'] if r['group'] == 'all'}
    rows = []
    for tier in results['headline']['groups']:
        for r in strict_rows(results, tier):
            pre = pre_registered(r)
            old = first_rows.get((r['levels'], r['split'])) if tier == 'core8' else None
            spk = (per_speaker or {}).get(f"{tier}|{r['levels']}|{r['split']}")
            rows.append({'tier': tier, 'levels': r['levels'], 'split': r['split'], 'pre_registered': pre,
                         'pre_registered_per_speaker': spk,
                         'count_once': {k: r[k] for k in ('tp', 'fp', 'fn', 'f1', 'same_change_duplicates')},
                         'count_once_interval': saved_f1_interval(r, r['split']),
                         'first_final': None if old is None else {k: old[k] for k in ('tp', 'fp', 'fn', 'f1', 'accounting')}})
    return {'rows': rows, 'first_final_config': first['detector_config_sha256'], 'pre_registered': f'{PRE_REGISTERED}; the plan calls it "all predictions counted" ({PLAN})',
            'count_once': COUNT_ONCE}


def same_change_section(results: dict, calibration: dict, detector: dict) -> dict:
    """Same-change detections (credited without the IoU test) per split and level, own-key regions
    on the injected edit that count as false, and the h-selection's separate D1- / D9- counting."""
    head = results['headline']
    rows = []
    for r in strict_rows(results, 'core8'):
        sel = [t for t in head['true_positive_detail'] if t['split'] in r['split'].split('+') and t['level'] in LEVEL_GROUPS[r['levels']]]
        false = [f for f in head['false_detail'] if f['split'] in r['split'].split('+') and f['level'] in LEVEL_GROUPS[r['levels']]]
        rows.append({'levels': r['levels'], 'split': r['split'], 'tp': r['tp'],
                     'same_change_detections': sum(str(t.get('detected_by', '')).startswith('same change') for t in sel),
                     'by_type': dict(Counter(t['type'] for t in sel if str(t.get('detected_by', '')).startswith('same change'))),
                     'false': len(false), 'false_on_injected_edit': sum(bool(f['on_flaw']) for f in false),
                     'false_on_edit_by_key': dict(Counter(f['group'] for f in false if f['on_flaw']))})
    selected = calibration['R1_selected']
    return {'rows': rows, 'selection_same_change_duplicates': selected['same_change_duplicates'],
            'selection_counts': {k: selected[k] for k in ('TP', 'FP', 'FN')},
            'selection_limit': detector['regimes']['R1']['natural_rush_selection']['limit']}


# ============================================================================================ intervals
def stress_by_speaker(results: dict) -> list[dict]:
    """Val and test stress rows (R1) with speakers, not edited recordings, as clusters (evaluate.speaker_stress_row): per-speaker
    added rate and kept fraction and their range, beside the saved recording-cluster intervals."""
    detail = results['stress']['flawed_clips']
    out = []
    for row in results['stress']['rows']:
        if row['split'] not in ('val', 'test', 'val+test') or row['regime'] != 'R1':
            continue
        spk = speaker_stress_row(row, detail)
        added, kept = spk['added_interval'], spk['retention_interval']
        if (spk['added_per_min'], kept['retained']) != (row['added_per_min'], row['retained_detections']):
            raise ValueError(f"stress {row['split']} {row['condition']}: records do not reproduce the saved row")
        out.append({'split': row['split'], 'condition': row['condition'], 'speakers': len(added['per_cluster'] or kept['per_cluster'] or {}),
                    'added_per_min': row['added_per_min'], 'added_per_speaker': added['per_cluster'], 'added_range': added['range'],
                    'saved_added_interval': row['added_ci95'], 'kept': [kept['retained'], kept['found']], 'kept_fraction': row['retention'],
                    'kept_per_speaker': kept['per_cluster'], 'kept_range': kept['range'], 'kept_wilson_pooled': wilson(kept['retained'], kept['found']),
                    'saved_kept_interval': row['retention_ci95'], 'saved_method': row['added_interval']['method'],
                    'added_by_key_per_speaker': {k: v['per_cluster'] for k, v in spk['added_by_key'].items()}})
    return out


def r2_by_reader(results: dict, mode: str) -> list[dict]:
    """R2 away-edits of the check readers by type and level: detected k/n per check reader (each reader's clip counts
    once per calibration reference), the pooled count, and the pre-registered R2 expectation."""
    edits = [e for e in results['cross_speaker']['modes'][mode]['edits']
             if e['reader_group'] == 'check' and e['direction'] == 'away from the reference']
    cells = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for e in edits:
        cell = cells[(e['type'], e['level'])][e['clip'].split('__')[0]]
        cell[0] += bool(e['detected'])
        cell[1] += 1
    rows = []
    for (typ, lv), readers in sorted(cells.items()):
        k, n = sum(v[0] for v in readers.values()), sum(v[1] for v in readers.values())
        rows.append({'type': typ, 'level': lv, 'dimension': C.FLAW_DIM[typ], 'detected': k, 'n': n,
                     'per_reader': {r: v for r, v in sorted(readers.items())},
                     'expected': EXPECTED['R2'][lv] if C.FLAW_DIM[typ] in EXPECTATION_DIMS or lv != 3 else
                     f"{C.FLAW_DIM[typ]} is {'listed' if C.FLAW_DIM[typ] in C.LISTED_DIMS['R2'] else 'not scored'} in R2",
                     'majority_detected': None if lv != 3 or C.FLAW_DIM[typ] not in EXPECTATION_DIMS or not n else 2 * k > n})
    return rows


def overlap_by_speaker(per_speaker_overlap: dict | None, results: dict) -> list[dict]:
    rows = []
    for r in results['headline']['groups']['core8']['overlap']:
        spk = (per_speaker_overlap or {}).get(f"{r['levels']}|{r['split']}")
        rows.append({'levels': r['levels'], 'split': r['split'], 'touched': r['touched'], 'truths': r['truths'],
                     'flags_on_flaw': r['flags_on_flaw'], 'flags': r['flags'], 'recall_wilson_pooled': r['overlap_recall_ci95'],
                     'precision_wilson_pooled': r['flag_precision_ci95'], 'per_speaker': spk})
    return rows


# ============================================================================================ local re-run
def shown_types(run: Run, labels: dict | None) -> list[dict]:
    """The cause label the product shows per region (pipeline.analyze: the title type, after grouping) and its pattern chip."""
    info = annotate(run.comp, run.regions, run.B, run.P, labels, run.clip)
    return [{'type': i.get('type', FLAW_TYPE[(r.dim, r.sign)]), 'pattern': i.get('pattern')} for r, i in zip(run.regions, info)]


def label_rows(c: dict, run: Run, ev: dict, labels: dict | None, tier: str) -> list[dict]:
    """Per available truth of the clip's evaluation `ev`: the label shown for the region or whole-clip flag that detects it."""
    shown = shown_types(run, labels)
    rows = []
    for t in ev['truth']:
        if not t['available']:
            continue
        j = t['detected_region']
        if j is None:
            label = pattern = None
        elif isinstance(j, str):  # a whole-clip flag: 'D1' or 'D1- whole clip'
            label, pattern = clip_type(j[:2], run.clip[j[:2]]), None
        else:
            label, pattern = shown[j]['type'], shown[j]['pattern']
        rows.append({'tier': tier, 'split': c['split'], 'clip': c['id'], 'speaker': c['parent'], 'level': t['level'], 'type': t['type'],
                     'detected_by': t['detected_by'], 'shown_type': label, 'shown_pattern': pattern,
                     'correct': None if label is None else t['type'] in (label, pattern)})
    return rows


def d9_near_rush(c: dict, run: Run, lab: dict, labels: dict | None) -> list[dict]:
    """Every D9- region within half a window of a RUSH or NATURAL_RUSH edit, with the label it is shown under (the natural-rush pause rule of patterns.annotate)."""
    shown = shown_types(run, labels)
    return [{'split': c['split'], 'clip': c['id'], 'level': t['level'], 'type': t['type'], 'shown_type': shown[j]['type']}
            for t in truths(lab) if t['type'] in ('RUSH', 'NATURAL_RUSH')
            for j, r in enumerate(run.regions) if key(r.dim, r.sign) == 'D9-' and within_half_window(r, t['words'])]


def excluded_span_rows(c: dict, run: Run, lab: dict, claimed: set[int]) -> list[dict]:
    """Regions on the words of an excluded realisation shortfall (events.on_shortfall): not counted as false in any tier."""
    shortfalls = truths(lab, excluded=True)
    rows = []
    for j, r in enumerate(run.regions):
        on = [t for t in shortfalls if on_shortfall(r, [t])]
        if not on:
            continue
        rows.append({'split': c['split'], 'clip': c['id'], 'level': c['level'], 'key': key(r.dim, r.sign),
                     'excluded_types': sorted({t['type'] for t in on}), 'excluded_dims': sorted({t['dim'] for t in on}),
                     'same_dimension': any(t['dim'] == r.dim for t in on), 'claimed_by_a_truth': j in claimed,
                     'reasons': sorted({x for t in on for x in t['exclusion_reasons']})})
    return rows


def claimed_regions(ev: dict) -> set[int]:
    """Region indices that detect, or duplicate the detection of, an available truth in the evaluation `ev`."""
    return {t['detected_region'] for t in ev['truth'] if isinstance(t.get('detected_region'), int)} | {d['index'] for d in ev['duplicates'] if d['on_truth']}


def counts(ev: dict) -> dict:
    """Strict per-clip counts under both accountings."""
    tp = sum(bool(t['detected']) for t in ev['truth'] if t['available'])
    fn = sum(t['available'] for t in ev['truth']) - tp
    fp = len(ev['false']) + len(ev['false_clip'])
    pre = pre_registered({'split': '', 'levels': '', 'tp': tp, 'fp': fp, 'fn': fn, 'same_change_duplicates': ev['duplicate'],
                          'every_prediction': every_prediction([ev])})
    return {'tp': tp, 'fp': fp, 'fn': fn, 'dup': ev['duplicate'], 'pre': [pre['tp'], pre['fp'], pre['fn']],
            'touched': sum(bool(t['touched']) for t in ev['truth'] if t['available']), 'truths': sum(t['available'] for t in ev['truth']),
            'flags_on_flaw': ev['flags_on_flaw'], 'flags': ev['n_regions']}


def fair_reference_free(ds, det: dict, nulls_and_controls) -> dict:
    """The reference-free baseline with its own scales (detect.fit_scales on the reference-free comparisons of
    the train identity and placebo nulls) and its own common and speech-tempo h, chosen by calibrate.select_r1 (the
    detector's objective: joint train strict F1 on core8 + NATURAL_RUSH L2+L3 with the train controls)."""
    from .calibrate import choose_r1_row, noise_floor, select_r1  # local imports, so tests can replace these functions
    from .evaluate import clip_runs
    n1, controls = nulls_and_controls
    free = lambda n: dataclasses.replace(n, comp=reference_free(n.comp, n.P))  # noqa: E731
    n1_free, controls_free = [free(n) for n in n1], [free(n) for n in controls]
    scales, _, _ = fit_scales([n.comp for n in n1_free])
    regime = copy.deepcopy(det['regimes']['R1'])
    regime['scales'] = {k: round(v, 6) for k, v in scales.items()}
    train = [c for c in ds.clips(kind='single') if c['split'] == 'train' and c['level'] in C.HEADLINE_LEVELS]
    pairs = [(reference_free_run(run, regime), lab) for c, run, lab in clip_runs(ds, det, train)]
    floor = noise_floor(n1_free, 'D9')
    curve = select_r1(pairs, controls_free, regime, floor)
    best = choose_r1_row(curve)[0]
    return {'regime': regime, 'scales': regime['scales'], 'h': regime['h'], 'd9_noise_floor_ln': floor,
            'train': {k: best[k] for k in ('h', 'natural_rush_h', 'TP', 'FP', 'FN', 'F1', 'control_regions')},
            'curve': [{k: r[k] for k in ('h', 'natural_rush_h', 'TP', 'FP', 'FN', 'F1')} for r in curve],
            'at_grid_edge': best['h'] == max(r['h'] for r in curve)}


@dataclasses.dataclass(kw_only=True)
class NullWithP(Null):
    """A calibrate.Null with its participant recording, which the reference-free view needs."""
    P: object


def train_nulls(ds) -> tuple[list[NullWithP], list[NullWithP]]:
    """The train R1 nulls (identity and placebo seeds) and controls (those plus the 20 dB noise identities), built as
    calibrate.run builds them."""
    items = r1_items(ds, ('train',))
    identities = [c for c in ds.clips(kind='identity') if ds.entry('baselines', c['parent'])['split'] == 'train' and calibration_clip(c)]
    noise_items = r1_noise_items(ds, identities)
    recs = ds.prepare_many([(i['wav'], i['tr']) for i in items + noise_items])
    nulls = [NullWithP(id=i['id'], comp=compare(i['B'], P), sentence=i['tr'].sentence, minutes=P.duration / 60, split='train',
                       reader=i['id'].split('__')[0], P=P)
             for i, P in zip(items + noise_items, recs)]
    return nulls[:len(items)], nulls


def local_section(run_dir: Path, results: dict, cache: Path | None, workers: int) -> dict:
    """The frozen detector re-run on the saved audio on CPU, computed after the final evaluation."""
    from .dataset import load_dataset
    from .evaluate import clip_runs  # a local import, so tests can replace this function
    from .pool import PreparePool
    started = time.monotonic()
    det = load_detector(run_dir / 'models' / 'detector.json')
    tier_types = tiers(det.get('report', {}).get('real_validation'))
    labels_on = det['regimes']['R1'].get('pattern_labels')
    with PreparePool(workers=workers, devices=['cpu'], cache_dir=cache) as pool:
        ds = load_dataset(run_dir / 'data' / 'dataset', cache, pool)
        clips = [c for c in ds.clips(kind='single') if c['split'] in ALL_SPLITS]
        runs = clip_runs(ds, det, clips)
        nulls = train_nulls(ds)
        fair = fair_reference_free(ds, det, nulls)
    per_clip, labels, d9, excluded = defaultdict(dict), [], [], []
    for c, run, lab in runs:
        excluded += excluded_span_rows(c, run, lab, claimed_regions(eval_clip(run, lab, secondary_exempt=False)))
        d9 += d9_near_rush(c, run, lab, labels_on)
        for tier, types in tier_types.items():
            if not any(f['type'] in types for f in lab['flaws']):
                continue
            ev = eval_clip(run, tier_labels(lab, types), secondary_exempt=False)
            per_clip[tier][c['id']] = counts(ev)
            labels += label_rows(c, run, ev, labels_on, tier)
    grouped, overlap, reproduction = {}, {}, []
    by_id = {c['id']: c for c in clips}
    for tier, rows in per_clip.items():
        saved = {(r['levels'], r['split']): r for r in strict_rows(results, tier)}
        for lname, lv in LEVEL_GROUPS.items():
            for split, gs in split_groups(ALL_SPLITS):
                sel = {cid: v for cid, v in rows.items() if by_id[cid]['level'] in lv and by_id[cid]['split'] in gs}
                total = {k: sum(v[k] for v in sel.values()) for k in ('tp', 'fp', 'fn', 'dup')}
                pre = [sum(v['pre'][i] for v in sel.values()) for i in range(3)]
                s = saved[(lname, split)]
                reproduction.append({'tier': tier, 'levels': lname, 'split': split, 'local': [total['tp'], total['fp'], total['dup'], total['fn']],
                                     'saved': [s['tp'], s['fp'], s['same_change_duplicates'], s['fn']], 'local_pre_registered': pre,
                                     'saved_pre_registered': [pre_registered(s)[k] for k in ('tp', 'fp', 'fn')]})
                speakers = defaultdict(list)
                for cid, v in sel.items():
                    speakers[by_id[cid]['parent']].append(v)
                pre_f1 = cluster_summary({k: [tuple(v['pre']) for v in vs] for k, vs in speakers.items()}, cluster_f1)
                grouped[f'{tier}|{lname}|{split}'] = {'per_speaker': {k: [sum(v['pre'][i] for v in vs) for i in range(3)] for k, vs in speakers.items()},
                                                      'f1_per_speaker': pre_f1['per_cluster'], 'f1_range': pre_f1['range'], 'f1_ci95': pre_f1['ci95'],
                                                      'method': pre_f1['method']}
                if tier == 'core8':
                    overlap[f'{lname}|{split}'] = {k: {'touched': sum(v['touched'] for v in vs), 'truths': sum(v['truths'] for v in vs),
                                                       'flags_on_flaw': sum(v['flags_on_flaw'] for v in vs), 'flags': sum(v['flags'] for v in vs)}
                                                   for k, vs in speakers.items()}
    held = [c for c, _, _ in runs if c['split'] in ('val', 'test') and c['level'] in C.HEADLINE_LEVELS]
    fair_totals = defaultdict(lambda: defaultdict(lambda: [0, 0, 0, 0]))
    for c, run, lab in runs:
        if c not in held:
            continue
        for tier, types in tier_types.items():
            if not any(f['type'] in types for f in lab['flaws']):
                continue
            tl = tier_labels(lab, types)
            for name, view in (('own scales and h', reference_free_run(run, fair['regime'])),
                               ('reference_free (detector h)', reference_free_run(run, det['regimes']['R1']))):
                (tp, fp, fn), dup = strict_counts(view, tl)
                for split in (c['split'], 'val+test'):
                    cell = fair_totals[f'{tier}|{split}'][name]
                    cell[0] += tp
                    cell[1] += fp
                    cell[2] += fn
                    cell[3] += dup
    fair.pop('regime')
    return {'device': 'cpu', 'workers': workers, 'seconds': round(time.monotonic() - started, 1),
            'detector_config_sha256': det['config_sha256'], 'clips': len(clips), 'reproduction': reproduction,
            'pre_registered_per_speaker': grouped, 'overlap_per_speaker': overlap, 'labels': labels, 'd9_near_rush': d9,
            'excluded_spans': excluded, 'reference_free_fair': {**fair, 'held_out': {k: dict(v) for k, v in fair_totals.items()}}}


# ============================================================================================ summaries of the local part
def label_summary(rows: list[dict]) -> dict:
    """Cause-label accuracy of detected truths per tier, split group and injected type, and the confusion of injected
    type against the shown title type."""
    out = {}
    for tier in sorted({r['tier'] for r in rows}):
        for split, gs in split_groups(ALL_SPLITS):
            for lname, lv in LEVEL_GROUPS.items():
                sel = [r for r in rows if r['tier'] == tier and r['split'] in gs and r['level'] in lv and r['detected_by']]
                by_type, confusion = defaultdict(lambda: [0, 0]), defaultdict(Counter)
                for r in sel:
                    by_type[r['type']][0] += bool(r['correct'])
                    by_type[r['type']][1] += 1
                    confusion[r['type']][shown_label(r)] += 1
                out[f'{tier}|{lname}|{split}'] = {'correct': sum(bool(r['correct']) for r in sel), 'detected': len(sel),
                                                  'by_type': dict(sorted(by_type.items())),
                                                  'confusion': {k: dict(v) for k, v in sorted(confusion.items())}}
    return out


def shown_label(row: dict) -> str:
    chip = row['shown_pattern']
    return row['shown_type'] + (f' ({chip} chip)' if chip and chip != row['shown_type'] else '')


def rush_confusion(rows: list[dict], d9: list[dict]) -> dict:
    """RUSH against NATURAL_RUSH: injected type x shown title type of the detecting region (or not detected), and of
    every D9- region within half a window of the edit."""
    out = {}
    for split, gs in split_groups(ALL_SPLITS):
        det_cells, d9_cells = defaultdict(Counter), defaultdict(Counter)
        for r in rows:
            if r['type'] in ('RUSH', 'NATURAL_RUSH') and r['split'] in gs and r['level'] in C.LEVELS:
                det_cells[r['type']][r['shown_type'] or 'not detected'] += 1
        for r in d9:
            if r['split'] in gs:
                d9_cells[r['type']][r['shown_type']] += 1
        out[split] = {'detecting_region': {k: dict(v) for k, v in det_cells.items()}, 'd9_regions': {k: dict(v) for k, v in d9_cells.items()}}
    return out


def excluded_summary(rows: list[dict]) -> list[dict]:
    out = []
    for split, gs in split_groups(ALL_SPLITS):
        for lname, lv in LEVEL_GROUPS.items():
            sel = [r for r in rows if r['split'] in gs and r['level'] in lv]
            out.append({'split': split, 'levels': lname, 'regions': len(sel), 'by_key': dict(sorted(Counter(r['key'] for r in sel).items())),
                        'other_dimension': sum(not r['same_dimension'] for r in sel),
                        'other_dimension_unclaimed': sum(not r['same_dimension'] and not r['claimed_by_a_truth'] for r in sel),
                        'by_excluded_type': dict(sorted(Counter('+'.join(r['excluded_types']) for r in sel).items())),
                        'clips': len({r['clip'] for r in sel})})
    return out


# ============================================================================================ markdown
def accounting_md(acc: dict) -> str:
    rows = []
    for r in acc['rows']:
        pre, once, old = r['pre_registered'], r['count_once'], r['first_final']
        spk = r['pre_registered_per_speaker']
        pre_int = saved_f1_interval(spk, r['split']) if spk else 'n/a'
        rows.append([r['tier'], r['levels'], r['split'], f"{pre['tp']}/{pre['fp']}/{pre['fn']}", pre['f1'], pre_int,
                     f"{once['tp']}/{once['fp']}/{once['same_change_duplicates']}/{once['fn']}", once['f1'], r['count_once_interval'],
                     pre['same_change_detections'], 'n/a' if old is None else f"{old['tp']}/{old['fp']}/{old['fn']}",
                     'n/a' if old is None else old['f1']])
    return md_table(['tier', 'levels', 'split', 'pre-registered TP/FP/FN', 'pre-registered F1', 'pre-registered F1 interval or per speaker',
                  'count-once TP/FP/dup/FN', 'count-once F1', 'count-once F1 interval (saved)', 'same-change detections',
                  f"first final ({acc['first_final_config'][:8]}) TP/FP/FN", 'first final F1'], rows)


def render(add: dict) -> str:
    acc, sc = add['accounting'], add['same_change']
    test = next(r for r in acc['rows'] if r['tier'] == 'core8' and r['split'] == 'test' and r['levels'].startswith('headline'))
    md = ['# Evaluation addendum (computed after the final evaluation)', '', PROVENANCE, '',
          (f"Inputs: {', '.join(f'`{k}` sha256 {v[:12]}' for k, v in add['inputs'].items())}. Detector config "
           f"{add['detector_config_sha256'][:12]}; detector.json sha256 {add['detector_sha256'][:12]} equals the final-evaluation "
           'entry of that config in models/final_evaluations.json.'), '',
          '## 1. Headline accounting: pre-registered first (findings 0, 2)', '',
          (f"Pre-registered accounting ({acc['pre_registered']}): core8 L2+L3 test F1 {md_cell(test['pre_registered']['f1'])} "
           f"(TP {test['pre_registered']['tp']} / FP {test['pre_registered']['fp']} / FN {test['pre_registered']['fn']}). "
           f"One-detection-per-change accounting ({acc['count_once']}): {md_cell(test['count_once']['f1'])}. "
           f"The test split was evaluated twice: the first final evaluation (config {acc['first_final_config'][:12]}, an earlier "
           f"detector without the speech-tempo key D9, all predictions counted) gave {md_cell(test['first_final']['f1'])} "
           f"({test['first_final']['tp']}/{test['first_final']['fp']}/{test['first_final']['fn']}); that result was seen before the redesign."), '',
          ('Pre-registered: TP = count-once TP minus same-change detections; FP = every region not matched by its own key '
           '(count-once FP + duplicates + same-change detections); FN = count-once FN plus same-change detections. '
           'Per-speaker values come from the local re-run, whose counts equal the saved ones (section 7).'), '',
          accounting_md(acc), '',
          '### Count-once rule as the code applies it (finding 21)', '',
          COUNT_ONCE_RULE + ' The frozen registry text printed in tables.md ("A region of a same_change key within half a '
          'window of a truth of its value key duplicates that change\'s detection") describes only the duplicate case; the '
          'registry string and its sha256 are unchanged.', '',
          '### Stated limits of the count-once rule (finding 2)', '',
          ('- Asymmetry: a speech-tempo (D9-) region within two words of a rush edit counts as its detection without the IoU '
           'test, while a second own-key region on the same edit that fails IoU counts as a false region.'),
          (f"- The h selection counted D1- and D9- separately (detector.json regimes.R1.natural_rush_selection.limit: "
           f"\"{sc['selection_limit']}\"); it reports {sc['selection_same_change_duplicates']} same-change duplicates on "
           f"train (calibration/report.json R1_selected), against "
           f"{next(r for r in acc['rows'] if r['tier'] == 'core8' and r['split'] == 'train' and r['levels'].startswith('headline'))['count_once']['same_change_duplicates']} "
           'in the evaluation train row.'), '',
          md_table(['levels', 'split', 'count-once TP', 'of them same-change detections (no IoU test)', 'by type',
                 'false regions', 'of them own-key regions on the injected edit', 'by key'],
                [[r['levels'], r['split'], r['tp'], r['same_change_detections'], json.dumps(r['by_type']), r['false'],
                  r['false_on_injected_edit'], json.dumps(r['false_on_edit_by_key'])] for r in sc['rows']]), '']
    loc = add.get('local')
    if loc:
        md += ['## 2. Cause-label accuracy (finding 3)', '',
               ('For each detected truth: the title type the product shows for the detecting region (after grouping; '
                'patterns.annotate) and its pattern chip, against the injected type. Correct = the injected type is the '
                'title type or the pattern chip. Recovery elsewhere is scored by dimension and direction only. '
                'The RUSH / NATURAL_RUSH rule constant NATURAL_RUSH_PAUSE_KEPT_MAX = sqrt(RUSH_PAUSE_KEEP[0]) = '
                f"{md_cell(C.NATURAL_RUSH_PAUSE_KEPT_MAX)} comes from the recipe parameters (config.RUSH_PAUSE_KEEP), and the rule "
                'is checked here only on clips made by those recipes.'), '']
        rows = []
        for k, v in add['labels'].items():
            tier, lname, split = k.split('|')
            if not v['detected']:
                continue
            rows.append([tier, lname, split, kn(v['correct'], v['detected']), bounds_text(wilson(v['correct'], v['detected']), '95% Wilson (pooled; clusters ignored)'),
                         '; '.join(f'{t} {kn(*c)}' for t, c in v['by_type'].items())])
        md += [md_table(['tier', 'levels', 'split', 'correct label / detected truths', 'interval', 'by injected type'], rows), '',
               'Confusion, val+test, all levels (injected type -> shown title type, with the pattern chip where it differs):', '',
               md_table(['injected type', 'shown labels (count)'],
                     [[t, '; '.join(f'{s} {n}' for s, n in sorted(c.items()))]
                      for t, c in sorted(merge_levels(add['labels'], 'val+test').items())]), '',
               ('RUSH against NATURAL_RUSH (all levels): the shown title type of the detecting region, and of every D9- region '
                'within half a window of the edit:'), '',
               md_table(['split', 'injected', 'detecting region', 'D9- regions near the edit'],
                     [[split, t, json.dumps(v['detecting_region'].get(t, {}), sort_keys=True), json.dumps(v['d9_regions'].get(t, {}), sort_keys=True)]
                      for split, v in add['rush_confusion'].items() for t in ('RUSH', 'NATURAL_RUSH')]), '']
        md += ['## 3. Regions on excluded edit spans (finding 5)', '',
               ('Single-level clips. A region that overlaps the words of an excluded (unrealised) edit is dropped from both '
                'TP and FP in every tier (events.on_shortfall), whatever its dimension. These regions are not counted as '
                'false. "Other dimension, unclaimed" regions would be false regions if only same-dimension responses were '
                'excluded.'), '',
               md_table(['split', 'levels', 'clips', 'regions on excluded spans', 'by key', 'other dimension', 'other dimension, unclaimed', 'excluded edit types'],
                     [[r['split'], r['levels'], r['clips'], r['regions'], json.dumps(r['by_key']), r['other_dimension'],
                       r['other_dimension_unclaimed'], json.dumps(r['by_excluded_type'])] for r in add['excluded_spans']]), '']
        fair = loc['reference_free_fair']
        md += ['## 4. Reference-free baseline with its own scales and h (finding 6)', '',
               ('The existing reference_free rows reuse the detector\'s scales (fitted on identity nulls, all at their floors) and '
                'its h grid. The added row fits its own scales on the reference-free comparisons of the 30 train identity and '
                'placebo nulls (detect.fit_scales) and chooses its own common and speech-tempo h with the detector\'s objective '
                '(calibrate.select_r1: joint train strict F1 on core8 + NATURAL_RUSH L2+L3 with the 35 train controls). '
                'No text (syllable) normalisation is applied, so it is a reference-free lower bound.'), '',
               f"Own scales: {json.dumps({k: md_cell(v) for k, v in fair['scales'].items() if k[:2] in ('D1', 'D2', 'D3', 'D5', 'D6', 'D9')})}; "
               f"common h {md_cell(fair['train']['h'])}, speech-tempo h {md_cell(fair['train']['natural_rush_h'])} (D9 noise floor "
               f"{md_cell(fair['d9_noise_floor_ln'])} ln); train TP/FP/FN {fair['train']['TP']}/{fair['train']['FP']}/{fair['train']['FN']}, "
               f"F1 {md_cell(fair['train']['F1'])}" + ('; the common h is at the top of the R1 grid (3.0)' if fair['at_grid_edge'] else '') + '.', '',
               md_table(['tier', 'split', 'method', 'TP', 'FP', 'same-change duplicates', 'FN', 'F1'],
                     [r for r in add['baselines'] if r[2].startswith(('detector', 'reference_free'))]), '',
               ('The detector row of each split is given first under the pre-registered accounting; every other row counts one '
                'detection per change, an accounting adopted after the plan.'), '']
    md += ['## 5. Intervals relabelled (finding 7)', '',
           ('Val and test have 2 speakers each. A percentile bootstrap over the 58 edited recordings of 2 speakers, or a '
            'Wilson interval on pooled events, is not a 95% interval for a new speaker; the tables below give per-speaker '
            'values and their range instead. The train F1 bootstrap resamples 5 speakers (in-sample; 126 distinct '
            'resamples), so its coverage is not assured.'), '',
           '### Stress (R1, val and test): per speaker', '',
           md_table(['split', 'condition', 'added/min', 'added/min per speaker', 'saved interval (58 recordings, 2 speakers)', 'kept',
                  'kept per speaker', 'pooled Wilson (clusters ignored)'],
                 [[r['split'], r['condition'], r['added_per_min'], interval_text(None, r['added_per_speaker'], r['added_range']),
                   bounds_text(r['saved_added_interval'], 'recording percentile'), f"{kn(*r['kept'])} ({md_cell(r['kept_fraction'])})",
                   interval_text(None, r['kept_per_speaker'], r['kept_range']), bounds_text(r['kept_wilson_pooled'], 'Wilson')]
                  for r in add['stress_by_speaker']]), '']
    if add['overlap']:
        md += ['### Overlap view (core8): per speaker', '',
               md_table(['levels', 'split', 'flaws touched', 'flags on flaw / flags', 'pooled Wilson recall (clusters ignored)', 'per speaker touched/flaws; on flaw/flags'],
                     [[r['levels'], r['split'], kn(r['touched'], r['truths']), kn(r['flags_on_flaw'], r['flags']),
                       bounds_text(r['recall_wilson_pooled'], 'Wilson'),
                       '; '.join(f"{s} {kn(v['touched'], v['truths'])}, {kn(v['flags_on_flaw'], v['flags'])}" for s, v in (r['per_speaker'] or {}).items()) or 'n/a']
                      for r in add['overlap']]), '']
    for mode, rows in add['r2_by_reader'].items():
        md += [f'### R2 check readers ({mode}), away-edits by type: per reader and the pre-registered expectation', '',
               READER_UNIT.get(mode, READER_UNIT['single']) + '; the per-reader k/n are not independent '
               'trials either. "Majority detected" (more than half of the away-edits) applies to level 3 of pace, pause, pitch-range '
               'and volume types only; it is an addendum criterion, not pre-registered.', '',
               md_table(['type', 'level', 'dimension', 'detected', 'per check reader', 'pre-registered R2 expectation', 'majority detected'],
                     [[r['type'], r['level'], r['dimension'], kn(r['detected'], r['n']),
                       '; '.join(f'{k} {kn(*v)}' for k, v in r['per_reader'].items()), r['expected'],
                       {None: 'n/a', True: 'yes', False: 'no'}[r['majority_detected']]] for r in rows]), '']
    md += ['## 6. Main tables rebuilt from results.json (finding 15)', '',
           'No raw floats: 3 significant digits, |v| < 1e-6 printed as 0, and equal interval bounds printed as degenerate.', '',
           '### Trivial baselines (L2+L3, val and test): the detector under the pre-registered accounting first; the other rows count one detection per change (adopted after the plan)', '',
           md_table(['tier', 'split', 'method', 'TP', 'FP', 'same-change duplicates', 'FN', 'F1'], add['baselines']), '',
           '### Stress matrix (all rows)', '',
           md_table(['split', 'condition', 'regime', 'reference mode', 'recordings', 'added/min', 'interval', 'kept', 'kept fraction', 'interval', 'max score change'],
                 add['stress_rows']), '',
           '### R2 lockbox', '',
           md_table(['mode', 'weighted total/min', 'pooled total/min', 'weighted upper95', 'budget status', 'whole-clip flags per clip'], add['lockbox']), '']
    if loc:
        bad = [r for r in loc['reproduction'] if r['local'] != r['saved'] or r['local_pre_registered'] != r['saved_pre_registered']]
        free = add['reference_free_reproduction']
        md += ['## 7. Local re-run check', '',
               f"The frozen detector was re-run on the saved audio of {loc['clips']} single-level clips on CPU ({loc['workers']} workers, word alignments read from the --cache directory when present, "
               f"{md_cell(loc['seconds'])} s). Strict TP/FP/duplicates/FN and the pre-registered counts equal the saved results in "
               f"{len(loc['reproduction']) - len(bad)} of {len(loc['reproduction'])} rows (tier x levels x split)." +
               ('' if not bad else ' Rows that differ: ' + json.dumps(bad)) +
               f" The existing reference_free (detector h) rows are reproduced in {sum(r['equal'] for r in free)} of {len(free)} "
               '(tier x split) cells (TP/FP/FN/duplicates).', '']
    return '\n'.join(md) + '\n'


def merge_levels(labels: dict, split: str) -> dict:
    out = defaultdict(Counter)
    for k, v in labels.items():
        if k.endswith('|' + split):
            for t, c in v['confusion'].items():
                out[t].update(c)
    return out


# ============================================================================================ assembly
PRE_REGISTERED_DETECTOR = 'detector (pre-registered: all predictions counted)'


def baseline_rows(results: dict, local: dict | None) -> list[list]:
    """The trivial-baseline rows: the detector's pre-registered row first, then the saved rows (one detection per change)."""
    rows = []
    strict = {(t, r['split']): r for t in results['headline']['groups'] for r in strict_rows(results, t) if r['levels'] == 'headline (L2+L3)'}
    for tier, group in results['trivial']['groups'].items():
        for split, methods in group['totals'].items():
            if (tier, split) in strict:
                pre = pre_registered(strict[(tier, split)])
                rows.append([tier, split, PRE_REGISTERED_DETECTOR, pre['tp'], pre['fp'], 'n/a (counted in FP)', pre['fn'], pre['f1']])
            for name, (tp, fp, fn) in methods.items():
                rows.append([tier, split, name, tp, fp, group['same_change_duplicates'][split][name], fn, f1(tp, fp, fn)['f1']])
            fair = (local or {}).get('reference_free_fair', {}).get('held_out', {}).get(f'{tier}|{split}', {}).get('own scales and h')
            if fair:
                tp, fp, fn, dup = fair
                rows.append([tier, split, 'reference_free (own scales and h; added after the final evaluation)', tp, fp, dup, fn, f1(tp, fp, fn)['f1']])
    return rows


def stress_rows(results: dict) -> list[list]:
    """The stress matrix; a recording-cluster interval is labelled with the number of speakers behind its recordings."""
    speakers = defaultdict(set)
    for r in results['stress']['flawed_clips']:
        speakers[r['split']].add(r['speaker'])
    out = []
    for r in results['stress']['rows']:
        n = len(set().union(*(speakers[s] for s in r['split'].split('+'))))
        label = f'recording percentile ({n} speakers)'
        added = r['added_interval']
        kept = r['retention_interval']
        added_text = interval_text(None, added['per_cluster'], added['range'], 'recording') if added['per_cluster'] else bounds_text(added['ci95'], label if added['events'] else 'Poisson upper')
        kept_text = interval_text(None, kept['per_cluster'], kept['range'], 'recording') if kept['per_cluster'] else bounds_text(kept['ci95'], label)
        if kept['ci95'][0] is not None and md_cell(kept['ci95'][0]) == md_cell(kept['ci95'][1]):
            kept_text += f"; Wilson {bounds_text(wilson(r['retained_detections'], r['flaws_found_before']), '')}"
        out.append([r['split'], r['condition'], r['regime'], r['reference_mode'] or '', r['recordings'], r['added_per_min'], added_text,
                    kn(r['retained_detections'], r['flaws_found_before']), r['retention'], kept_text, r['max_abs_delta_score']])
    return out


def lockbox_rows(results: dict) -> list[list]:
    return [[mode, null['total_local']['rate'], null['total_local']['pooled_rate'], null['total_local']['bootstrap_upper95'],
             null['total_local']['budget_status'], null.get('false_clip_flags_per_clip')]
            for mode, null in results['lockbox']['modes'].items()]


def reference_free_reproduction(results: dict, local: dict) -> list[dict]:
    rows = []
    for cell, methods in local['reference_free_fair']['held_out'].items():
        tier, split = cell.split('|')
        group = results['trivial']['groups'][tier]
        saved = [*group['totals'][split]['reference_free (detector h)'], group['same_change_duplicates'][split]['reference_free (detector h)']]
        rows.append({'tier': tier, 'split': split, 'local': methods['reference_free (detector h)'], 'saved': saved,
                     'equal': [float(v) for v in methods['reference_free (detector h)']] == [float(v) for v in saved]})
    return rows


def check_frozen(run_dir: Path, results: dict) -> tuple[str, str]:
    """The run's detector.json is the one the final evaluation of its config recorded."""
    det = json.loads((run_dir / 'models' / 'detector.json').read_text())
    log = json.loads((run_dir / 'models' / 'final_evaluations.json').read_text())
    digest = sha256_file(run_dir / 'models' / 'detector.json')
    if det['config_sha256'] != results['detector_config_sha256'] or log[det['config_sha256']]['detector_sha256'] != digest:
        raise ValueError('detector.json is not the detector of the final evaluation')
    return det['config_sha256'], digest


def build(run_dir: Path, first_final: Path, local: dict | None) -> dict:
    results = json.loads((run_dir / 'eval' / 'results.json').read_text())
    first = json.loads(first_final.read_text())
    log = json.loads((run_dir / 'models' / 'final_evaluations.json').read_text())
    if first['detector_config_sha256'] not in log or not first.get('final'):
        raise ValueError('the first final evaluation is not a recorded final evaluation of this run log')
    calibration = json.loads((run_dir / 'calibration' / 'report.json').read_text())
    detector = json.loads((run_dir / 'models' / 'detector.json').read_text())
    config, digest = check_frozen(run_dir, results)
    files = {'eval/results.json': run_dir / 'eval' / 'results.json', 'models/detector.json': run_dir / 'models' / 'detector.json',
             'models/final_evaluations.json': run_dir / 'models' / 'final_evaluations.json',
             'calibration/report.json': run_dir / 'calibration' / 'report.json', str(first_final): first_final}
    add = {'provenance': PROVENANCE, 'inputs': {k: sha256_file(p) for k, p in files.items()}, 'detector_config_sha256': config,
           'detector_sha256': digest,
           'accounting': accounting_section(results, first, (local or {}).get('pre_registered_per_speaker')),
           'same_change': same_change_section(results, calibration, detector), 'count_once_rule': COUNT_ONCE_RULE,
           'stress_by_speaker': stress_by_speaker(results),
           'overlap': overlap_by_speaker((local or {}).get('overlap_per_speaker'), results),
           'r2_by_reader': {mode: r2_by_reader(results, mode) for mode in results['cross_speaker']['modes']},
           'baselines': baseline_rows(results, local), 'stress_rows': stress_rows(results), 'lockbox': lockbox_rows(results),
           'local': local}
    if local:
        add['reference_free_reproduction'] = reference_free_reproduction(results, local)
        add['labels'] = label_summary(local['labels'])
        add['rush_confusion'] = rush_confusion(local['labels'], local['d9_near_rush'])
        add['excluded_spans'] = excluded_summary(local['excluded_spans'])
    return add


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog='python -m cvoice.addendum')
    ap.add_argument('--run', type=Path, required=True, help='the final run folder (eval/, models/, calibration/, data/dataset)')
    ap.add_argument('--first-final', type=Path, required=True, help='results.json of the first final evaluation')
    ap.add_argument('--cache', type=Path, default=None, help='alignment cache directory')
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--reuse-local', action='store_true', help='take the local re-run from the existing addendum.json')
    ap.add_argument('--no-local', action='store_true', help='only the parts computed from results.json')
    a = ap.parse_args(argv)
    out = a.run / 'eval'
    if a.no_local:
        local = None
    elif a.reuse_local:
        local = json.loads((out / 'addendum.json').read_text())['local']
    else:
        local = local_section(a.run, json.loads((out / 'results.json').read_text()), a.cache, a.workers)
    add = build(a.run, a.first_final, local)
    (out / 'addendum.json').write_text(json.dumps(add, indent=1, sort_keys=True, default=lambda o: o.item() if hasattr(o, 'item') else str(o)) + '\n')
    (out / 'addendum.md').write_text(render(add))
    print(f'[addendum] wrote {out / "addendum.json"} and {out / "addendum.md"}', flush=True)


if __name__ == '__main__':
    main()
