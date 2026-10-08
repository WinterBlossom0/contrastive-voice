"""Calibration (Kaggle): train-only scales, joint common/speech-tempo R1 h, budgeted R2 h per flag key, clip thresholds, Pmax
from the score gates on train, gates checked on val, config hash recorded -> models/detector.json (+ calibration/report.json).

    python -m cvoice.calibrate --dataset /kaggle/working/data --cache /kaggle/working/cache --out /kaggle/working/out

Train nulls. R1: the stored identity clip and PLACEBO_SEEDS on-the-fly placebo clips of every train baseline (the
participant is the same performance). R2: five seeded same-text references per participant in each fixed fit group. Batch-first: the placebo
clips are generated in parallel, then every clip to analyse (nulls and the score-gate clips) goes through one pool batch.
"""
from __future__ import annotations

import argparse
import copy
import json
import dataclasses
import tempfile
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import __version__
from . import config as C
from . import audio, flaws, stress
from .compare import Comparison, compare
from .dataset import Dataset, load_dataset, prepare_null_readers, sha256_file
from .detect import scale, KEYS, decode_dim, choose_h, clip_flags, decode, fit_clip, fit_scales, key, make_detector, save_detector, wquantile
from .events import Run, clip_key, eval_clip, run_pair
from .pipeline import ROOT, device_class, map_calls
from .pool import PreparePool
from .protocol import LAB_VALIDATION, STRICT_ACCOUNTING
from .score import score, overall


@dataclass
class Null:
    """One null comparison: id, comparison, sentence index per word, participant minutes, split of the baseline (R1)."""
    id: str
    comp: Comparison
    sentence: tuple[int, ...]
    minutes: float
    split: str = ""
    group: str = ""
    reader: str = ""
    reference: str = ""
    source: str = ""
    first_language: str = ""


def log(msg: str) -> None:
    print(f"[calibrate] {msg}", flush=True)


# ============================================================================================ nulls
def placebo_audio(rec, baseline_id: str, k: int):
    """Placebo seed k of a baseline (a pool worker runs this)."""
    return flaws.placebo_clip(rec, baseline_id, k)[0]


def r1_items(ds: Dataset, splits: tuple[str, ...], seeds: int = C.PLACEBO_SEEDS) -> list[dict]:
    """Work items of the R1 nulls of the baselines in `splits`: the stored identity clip and `seeds` placebo clips (generated
    in parallel), each {id, split, B, tr, wav}."""
    bs = [b for b in ds.manifest["baselines"] if b["split"] in splits]
    Bs = ds.recs(bs)
    ys = iter(map_calls(placebo_audio, [(B, b["id"], k) for b, B in zip(bs, Bs) for k in range(seeds)], ds.pool))
    out = []
    for b, B in zip(bs, Bs):
        tr = ds.transcript(b)
        ident = next(c for c in ds.clips(parent=b["id"], kind="identity"))
        out.append({"id": ident["id"], "split": b["split"], "B": B, "tr": tr, "wav": ds.wav(ident)})
        out += [{"id": f"{b['id']}__placebo{k}", "split": b["split"], "B": B, "tr": tr, "wav": next(ys)} for k in range(seeds)]
    return out


def null_list(items: list[dict], recs: list) -> list[Null]:
    return [Null(i["id"], compare(i["B"], P), i["tr"].sentence, P.duration / 60, i["split"], reader=i["id"].split("__")[0]) for i, P in zip(items, recs)]


def r1_nulls(ds: Dataset, splits: tuple[str, ...], seeds: int = C.PLACEBO_SEEDS) -> list[Null]:
    """R1 nulls of the baselines in `splits` (one analysis batch)."""
    items = r1_items(ds, splits, seeds)
    return null_list(items, ds.prepare_many([(i["wav"], i["tr"]) for i in items]))


def r2_nulls(ds: Dataset, b_ids: list[str], p_ids: list[str]) -> list[Null]:
    """R2 nulls: every ordered pair (B, P) of reader clips with B != P, B from b_ids and P from p_ids."""
    ids = sorted(set(b_ids) | set(p_ids))
    recs = dict(zip(ids, ds.recs([ds.entry("readers", i) for i in ids])))
    if not hasattr(ds, "_reader_nulls"):
        ds._reader_nulls = {}
    for b in b_ids:
        for p in p_ids:
            if b != p and (b, p) not in ds._reader_nulls:
                ds._reader_nulls[(b, p)] = Null(f"{b}>{p}", compare(recs[b], recs[p]), recs[b].tr.sentence, recs[p].duration / 60,
                                                reader=p, reference=b, source='gettysburg')
    return [ds._reader_nulls[(b, p)] for b in b_ids for p in p_ids if b != p]


def grouped_nulls(ds: Dataset, phase: str, consensus=False, pool: dict | None = None) -> list[Null]:
    """R2 null comparisons of a pool set. The lockbox needs `pool` from lockbox_pool, which only the final task prepares."""
    if phase == 'lockbox' and pool is None:
        raise ValueError('lockbox nulls require the final-evaluation task')
    from .r2pool import pair_ids, first_language
    from .reference import consensus_reference
    if consensus and hasattr(ds, '_consensus_nulls') and phase in ds._consensus_nulls:
        return ds._consensus_nulls[phase]
    consensus_rows = []
    pool = ds.manifest['r2_pool'] if pool is None else pool
    pairs = pair_ids(pool, phase)
    entries = {e['id']: e for e in ds.manifest['readers']}
    entries.update({e['id']: e for g in pool['groups'] for e in g['entries']})
    if any('clip_offset_s' not in entries[i] for _, b, p in pairs for i in (b, p)):
        raise ValueError('R2 null readings must be cropped before calibration; rebuild the dataset')
    grouped = defaultdict(list)
    for g, b, p in pairs:
        grouped[g].append((b, p))
    out = []
    for g, members in grouped.items():
        ids = sorted({i for b, p in members for i in (b, p)})
        prepare_null_readers(ds, [entries[i] for i in ids])
        recs = dict(zip(ids, ds.recs([entries[i] for i in ids])))
        out.extend(Null(f'{b}>{p}', compare(recs[b], recs[p]), recs[b].tr.sentence, entries[p]['duration_s'] / 60,
                        phase, g, entries[p]['reader_id'], entries[b]['reader_id'], entries[p].get('source', ''), first_language(entries[p]['reader_id']) if entries[p].get('source') == 'accent' else '') for b, p in members)
        bank = defaultdict(list)
        for b, p in members:
            if b not in bank[p]:
                bank[p].append(b)
        for p, refs in bank.items():
            if len(refs) < C.CONSENSUS_K:
                continue
            B = consensus_reference([recs[i] for i in refs])
            consensus_rows.append(Null(f'{",".join(refs[:C.CONSENSUS_K])}>{p}', compare(B, recs[p]), B.tr.sentence,
                                       entries[p]['duration_s'] / 60, phase, g, entries[p]['reader_id'],
                                       ','.join(entries[b]['reader_id'] for b in refs[:C.CONSENSUS_K]), entries[p].get('source', ''),
                                       first_language(entries[p]['reader_id']) if entries[p].get('source') == 'accent' else ''))
        for i in ids:
            ds._recs.pop(i, None)
    if not hasattr(ds, '_consensus_nulls'):
        ds._consensus_nulls = {}
    ds._consensus_nulls[phase] = consensus_rows
    return consensus_rows if consensus else out


def reader_ids(ds: Dataset, role: str) -> list[str]:
    return sorted(e["id"] for e in ds.manifest["readers"] if e.get("role") == role)


# ============================================================================================ regime fit
def source_weights(nulls):
    sources = sorted({n.source or n.group.split(':')[0] for n in nulls})
    return dict.fromkeys(sources, 1 / len(sources)) if sources else {}


def group_weights(nulls, fixed=None):
    fixed = source_weights(nulls) if fixed is None else fixed
    exposure, sources = Counter(), {}
    for n in nulls:
        exposure[n.group] += n.minutes
        sources[n.group] = n.source or n.group.split(':')[0]
    totals = Counter()
    for g, minutes in exposure.items():
        totals[sources[g]] += minutes
    return {g: fixed.get(sources[g], 0.) * minutes / totals[sources[g]] for g, minutes in exposure.items() if totals[sources[g]] > 0}


def pair_weights(nulls):
    weights = group_weights(nulls)
    exposure = Counter()
    for n in nulls:
        exposure[n.group] += n.minutes
    return [weights[n.group] * n.minutes / exposure[n.group] for n in nulls]


def base_regime(name: str, nulls: list[Null]) -> dict:
    weights = pair_weights(nulls) if name == 'R2' else None
    scales, medians, counts = fit_scales([n.comp for n in nulls], weights)
    return {"name": name, "enabled": list(C.REGIME_DIMS[name]), "scales": {k: round(v, 6) for k, v in scales.items()},
            "null_median": {k: None if v is None else round(v, 6) for k, v in medians.items()},
            "h": dict.fromkeys(KEYS), "clip": dict(C.CLIP_LN) if name == "R1" else dict.fromkeys(C.CLIP_DIMS),
            "null": {"n_pairs": len(nulls), "minutes": round(sum(n.minutes for n in nulls), 3), 'signed_scale_units': counts,
                     "valid_units": {key(d,s): sum(measured_units(n.comp,key(d,s)) for n in nulls)
                                     for d in C.DIMS for s in C.FLAG_SIGNS[d]}}}


def rate_counter(nulls, clip=False, fixed=None):
    weights = group_weights(nulls, fixed)
    names = list(weights)
    indices = {g: i for i, g in enumerate(names)}
    groups = np.array([indices[n.group] for n in nulls], int)
    exposure = np.bincount(groups, weights=[n.minutes for n in nulls], minlength=len(names))
    factors = np.divide([weights[g] for g in names], exposure, out=np.zeros(len(names)), where=exposure > 0)
    def rate(counts):
        weighted = np.asarray(counts) * np.array([n.minutes for n in nulls]) if clip else counts
        return float(np.dot(np.bincount(groups, weights=weighted, minlength=len(names)), factors)) if names else float('inf')
    return rate


def grouped_rate(nulls: list[Null], counts, clip=False, fixed=None) -> float:
    return rate_counter(nulls, clip, fixed)(counts)


def measured_units(comp, flag):
    d = comp.dims[C.dim_of(flag)]
    return int(np.sum(d.countable & np.isfinite(d.x)))


def language_rates(nulls,counts):
    from .uncertainty import cluster_interval
    out = {}
    for language in sorted({n.first_language for n in nulls if n.first_language}):
        rows = [(n,count) for n,count in zip(nulls,counts) if n.first_language == language]
        clusters = defaultdict(list)
        for n,count in rows:
            clusters[n.reader].append((count,n.minutes))
        exposure = sum(n.minutes for n,count in rows)
        flags = int(sum(count for n,count in rows))
        ci = cluster_interval(clusters,lambda values: sum(v[0] for v in values)/sum(v[1] for v in values)) if flags else [None,None]
        out[language] = {'flags': flags, 'comparison_minutes': exposure, 'rate': flags/exposure,
                         'ci95': ci, 'readers': len(clusters), 'ci_method': 'participant-reader cluster bootstrap; no bound for zero events',
                         'scope': 'participant first language; references may have different first languages; no causal attribution'}
    return out


def rate_report(nulls: list[Null], counts, clip=False, fixed=None, flag=None, r1=False) -> dict:
    fixed = source_weights(nulls) if fixed is None else fixed
    clusters, groups = defaultdict(lambda: defaultdict(lambda: np.zeros(2))), defaultdict(lambda: np.zeros(2))
    group_clusters = defaultdict(lambda: defaultdict(lambda: np.zeros(3)))
    independent, valid = {}, 0
    for n, count in zip(nulls, counts):
        reader = n.reader or n.id.split('>')[-1].split('__')[0]
        source = n.source or n.group.split(':')[0]
        units = measured_units(n.comp,flag) if flag else 1
        valid += units
        exposure = 1 if clip else n.minutes
        if units:
            independent[reader] = max(independent.get(reader, 0.), exposure)
        clusters[source][reader] += (count, exposure)
        groups[n.group] += (count, exposure)
        group_clusters[n.group][reader] += (count * n.minutes, n.minutes, n.minutes) if clip else (count, exposure, n.minutes)
    rng = np.random.default_rng(C.SEED)
    samples, pooled = [], []
    origins = defaultdict(set)
    for readers in clusters.values():
        for reader in readers:
            origins[reader.split(':')[0]].add(reader)
    ids = sorted({r for readers in origins.values() for r in readers})
    index = {r:i for i,r in enumerate(ids)}
    names = list(group_clusters)
    arrays = np.zeros((len(names), len(ids), 3))
    raw_arrays = np.zeros((len(names), len(ids), 2))
    for g, readers in group_clusters.items():
        for reader, values in readers.items():
            arrays[names.index(g), index[reader]] = values
    for n,count in zip(nulls,counts):
        reader = n.reader or n.id.split('>')[-1].split('__')[0]
        raw_arrays[names.index(n.group),index[reader]] += (count, 1 if clip else n.minutes)
    group_sources = {n.group: n.source or n.group.split(':')[0] for n in nulls}
    source_indices = {source: np.array([i for i,g in enumerate(names) if group_sources[g] == source]) for source in clusters}
    for _ in range(C.R2_BOOTSTRAPS if sum(counts) else 0):
        # Person-origin strata preserve shared LibriVox readers across text sources.
        multiplicity = np.zeros(len(ids))
        for readers in origins.values():
            indices = [index[r] for r in sorted(readers)]
            multiplicity[indices] = np.bincount(rng.integers(len(indices), size=len(indices)), minlength=len(indices))
        values = np.einsum('gri,r->gi', arrays, multiplicity)
        totals = {source: values[indices].sum(axis=0) for source, indices in source_indices.items()}
        if all(v[1] > 0 for v in totals.values()):
            rate = 0.
            for source, indices in source_indices.items():
                if clip:
                    v = values[indices]
                    text_rates = np.divide(v[:,0], v[:,1], out=np.zeros(len(v)), where=v[:,1] > 0)
                    rate += fixed.get(source, 0.) * np.dot(v[:,2], text_rates) / totals[source][2]
                else:
                    rate += fixed.get(source, 0.) * totals[source][0] / totals[source][1]
            samples.append(rate)
            total = np.einsum('gri,r->i', raw_arrays, multiplicity)
            pooled.append(total[0] / total[1])
    exposure = sum(1 if clip else n.minutes for n in nulls)
    represented = {n.source or n.group.split(':')[0] for n in nulls}
    complete = set(fixed) <= represented
    measured = bool(nulls) and (not r1 or valid > 0)
    weights = group_weights(nulls, fixed)
    independent_exposure = sum(independent.values())
    source_totals = {source: arrays[indices].sum(axis=(0, 1)) for source, indices in source_indices.items()}
    return {'rate': grouped_rate(nulls, counts, clip, fixed) if measured and complete else None,
            'pooled_rate': sum(counts) / exposure if measured and exposure else None, 'flags': int(sum(counts)),
            'measured_pause_boundaries': sum(int(np.isfinite(n.comp.dims['D2'].x).sum()) for n in nulls),
            'unit': 'minute-weighted fraction of null clips flagged' if clip else 'regions per comparison-minute',
            'exposure': exposure, 'valid_units': valid if flag else None, 'readers': len({r for readers in clusters.values() for r in readers}),
            'independent_recording_exposure': independent_exposure if r1 else None,
            'bootstrap_upper95': float(np.quantile(samples, .95)) if samples and complete else None,
            'pooled_bootstrap_upper95': float(np.quantile(pooled, .95)) if pooled else None,
            'bootstrap_scope': 'participant-person clusters; shared texts and reference draws retained; no bootstrap bound for zero events',
            'weighting': 'fixed equal source shares from fit; comparison-minute weights within source',
            'missing_fit_sources': sorted(set(fixed) - represented), 'sources': sorted(represented),
            'groups': {g: {'flags': int(v[0]), 'exposure': float(v[1]), 'weight': weights[g],
                           'comparison_minutes': float(arrays[names.index(g), :, 2].sum()),
                           'readers': len({n.reader or n.id.split('>')[-1].split('__')[0] for n in nulls if n.group == g})} for g, v in groups.items()},
            'by_L1': language_rates(nulls,counts),
            'by_source': {source: {'flags': int(sum(v[0] for v in readers.values())),
                          'exposure': float(sum(v[1] for v in readers.values())),
                          'rate': float(source_totals[source][0] / source_totals[source][1]),
                          'pooled_rate': float(sum(v[0] for v in readers.values()) / sum(v[1] for v in readers.values()))} for source, readers in clusters.items()},
            'rule_of_three': C.RULE_OF_THREE / independent_exposure if r1 and measured and not sum(counts) and independent_exposure else None,
            'rule_of_three_scope': 'unique source recordings with measurable units; variants count once' if r1 else 'not supplied: dependent reader/reference comparisons'}


def region_counter(nulls: list[Null], dim: str, scale_value: float, sign: int):
    """Batch event counts; window comparisons below the opening threshold need no region traversal."""
    dims = [n.comp.dims[dim] for n in nulls]
    if C.is_event(dim):
        width = max((len(d.x) for d in dims), default=0)
        values = np.full((len(dims), width), -np.inf)
        for i, d in enumerate(dims):
            values[i, :len(d.x)] = np.where(d.countable & np.isfinite(d.x), sign * d.x / scale_value, -np.inf)
        return lambda h: (values >= h).sum(axis=1)
    peaks = np.array([np.max(sign * d.x[np.isfinite(d.x)], initial=-np.inf) / scale_value for d in dims])
    def count(h):
        counts = np.zeros(len(nulls), int)
        for i in np.flatnonzero(peaks >= h):
            counts[i] = len(decode_dim(dims[i], scale_value, h, nulls[i].sentence, (sign,)))
        return counts
    return count


def fit_r2(nulls: list[Null], full_curve: bool = True, enabled=None, labels=None) -> tuple[dict, dict]:
    reg = base_regime('R2', nulls)
    if enabled is not None:
        reg['enabled'] = list(enabled)
    reg['pattern_labels'] = labels or {}
    keys = [(k, sign) for k in reg['enabled'] for sign in C.FLAG_SIGNS[k]]
    budget = C.FALSE_RATE_BUDGET / len(keys)
    minutes, sentences = sum(n.minutes for n in nulls), [n.sentence for n in nulls]
    tables = {}
    rate = rate_counter(nulls)
    for k, sign in keys:
        s = scale(reg, k, sign)
        count = region_counter(nulls, k, s, sign)
        def counting(h):
            counts = count(h)
            return int(sum(counts)), rate(counts)
        reg['h'][key(k, sign)], tables[key(k, sign)] = choose_h(
            [n.comp.dims[k] for n in nulls], sentences, s, sign, minutes, budget, full_curve, counting)
    # Owner decision: the whole-clip threshold is the fit quantile at the clip share (equal sources, comparison-minutes within
    # a source, as for local), floored like the local scale; the CLIP_H robust start is reported beside it.
    starts = fit_clip([n.comp for n in nulls], pair_weights(nulls))
    clip_dims = [k for k in C.CLIP_DIMS if k in reg['enabled'] and (k != 'D7' or reg['pattern_labels'].get('uneven_tempo', False))]
    reg['clip'] = dict.fromkeys(C.CLIP_DIMS)
    clip_share = C.FALSE_CLIP_RATE_BUDGET / len(clip_dims) if clip_dims else 0.0
    for k in clip_dims if nulls else ():
        values = np.array([abs(n.comp.dims[k].g) if np.isfinite(n.comp.dims[k].g) and
                           (1 if n.comp.dims[k].g > 0 else -1) in C.FLAG_SIGNS[k] else 0. for n in nulls])
        quantile = wquantile(values, np.array(pair_weights(nulls)), 1 - clip_share)
        reg['clip'][k] = round(max(quantile, C.FLOORS[k]), 6)
        reg['null'].setdefault('clip_threshold_choice', {})[k] = {
            'threshold': reg['clip'][k], 'clip_budget_quantile': quantile, 'robust_start': starts[k],
            'rule': 'fit clip-budget quantile, floored at FLOORS; the CLIP_H robust start is not used'}
    reg['null']['budget_per_key'] = budget
    reg['null']['clip_budget_per_key'] = clip_share
    reg['weighting'] = {'source_weights': source_weights(nulls), 'fit_group_weights': group_weights(nulls),
                        'fit_group_comparison_minutes': {g: sum(n.minutes for n in nulls if n.group == g) for g in group_weights(nulls)},
                        'rule': 'equal sources; every comparison-minute within a source has equal weight'}
    reg['selection'] = 'equal-source, comparison-minute point rate; bounds reported, not used to select h'
    if full_curve:
        null_check(reg, nulls)
    return reg, tables


def mode_report(reg, select):
    return {'thresholds': reg['h'], 'physical_thresholds': {k: None if h is None else h*scale(reg,C.dim_of(k),1 if k.endswith('+') else -1) for k,h in reg['h'].items()},
            'clip_thresholds': reg['clip'], 'fit': reg['null'], 'select': select,
            'clip_threshold_choice': {k: {**row, 'select_clip_rate': select.get('clip_by_key', {}).get(k, {}).get('rate'),
                                          'select_clip_upper95': select.get('clip_by_key', {}).get(k, {}).get('bootstrap_upper95'),
                                          'clip_budget_per_key': reg['null'].get('clip_budget_per_key')}
                                      for k, row in reg['null'].get('clip_threshold_choice', {}).items()},
            'weighting': reg.get('weighting', {})}


def null_check(regime: dict, nulls: list[Null]) -> None:
    local, clips, all_counts = defaultdict(list), defaultdict(list), Counter()
    keys = [key(k, s) for k in regime['enabled'] for s in C.FLAG_SIGNS[k]]
    for n in nulls:
        counts = Counter(key(r.dim, r.sign) for r in decode(n.comp, regime, n.sentence))
        whole = clip_flags(n.comp, regime)
        all_counts.update(counts)
        all_counts.update(clip_key(k, g) for k, g in whole.items())
        for k in keys:
            local[k].append(counts[k])
        for k in C.CLIP_DIMS:
            if k not in regime['enabled'] or regime['clip'].get(k) is None:
                continue
            clips[k].append(int(k in whole))
    report = regime['null']
    report['flags_by_key'] = dict(sorted(all_counts.items()))
    fixed = regime.get('weighting', {}).get('source_weights')
    r1 = regime.get('name') == 'R1'
    report['local_by_key'] = {k: rate_report(nulls, c, fixed=fixed, flag=k, r1=r1) for k, c in local.items()}
    report['clip_by_key'] = {k: rate_report(nulls, c, clip=True, fixed=fixed, r1=r1) for k, c in clips.items()}
    total_counts = np.sum(list(local.values()), axis=0) if local else np.zeros(len(nulls), int)
    report['total_local'] = rate_report(nulls, total_counts, fixed=fixed, r1=r1)
    share = regime.get('null', {}).get('budget_per_key', C.FALSE_RATE_BUDGET / max(1, len(keys)))
    for row in report['local_by_key'].values():
        row['budget_share'] = share
        row['point_within_share'] = row['rate'] is not None and row['rate'] <= share
        row['upper95_within_share'] = row['bootstrap_upper95'] is not None and row['bootstrap_upper95'] <= share
    total = report['total_local']
    report['false_per_minute_at_h'] = total['rate']
    total['budget'] = C.FALSE_RATE_BUDGET
    total['budget_status'], reason = budget_status(total, r1)
    total['budget_holds_point'] = total['budget_status'] == 'met'
    total['budget_holds_upper95'] = total['bootstrap_upper95'] is not None and total['bootstrap_upper95'] <= C.FALSE_RATE_BUDGET
    report['budget_statement'] = (f'{C.FALSE_RATE_BUDGET}/min budget {reason}' +
                                  (' and bootstrap upper95' if total['budget_holds_upper95'] else '; upper95 does not establish the budget'))
    clip_rates = [v['rate'] for v in report['clip_by_key'].values()]
    report['false_clip_flags_per_clip'] = None if None in clip_rates else sum(clip_rates)


def budget_status(total: dict, r1: bool) -> tuple[str, str]:
    """'met', 'not met' or 'not measurable', with the reason. R1 zero-event exposure below RULE_OF_THREE / budget cannot
    show the budget, because the zero-event upper bound is then above it."""
    if total['rate'] is None:
        missing = total['missing_fit_sources']
        return 'not measurable', 'is not measurable: ' + ('no rows for fit sources ' + ', '.join(missing) if missing else 'no measurable null comparison')
    if total['rate'] > C.FALSE_RATE_BUDGET:
        return 'not met', 'is not met at the point rate'
    needed = C.RULE_OF_THREE / C.FALSE_RATE_BUDGET
    if r1 and total['independent_recording_exposure'] < needed:
        return 'not measurable', (f"is not measurable: {total['independent_recording_exposure']:.2f} independent recording-minutes, "
                                  f"{needed:.2f} needed")
    return 'met', 'holds at the point rate'


def consensus_availability(pool: dict, phase: str) -> dict:
    """Per source of the R2 pool: the number of texts, the readers of each text in `phase`, and the largest number of
    distinct same-text references that one reader of the phase has (a consensus row needs CONSENSUS_K)."""
    from .r2pool import pair_ids
    references = defaultdict(set)
    for group, reference, participant in pair_ids(pool, phase):
        references[group, participant].add(reference)
    most = Counter()
    for (group, _), refs in references.items():
        most[group] = max(most[group], len(refs))
    out = {}
    for group in pool['groups']:
        row = out.setdefault(group.get('source') or group['id'].split(':')[0], {'texts': 0, 'readers_per_text': [], 'max_distinct_references': 0,
                                                                              'references_per_participant': pool['references_per_participant']})
        row['texts'] += 1
        row['readers_per_text'] = sorted(row['readers_per_text'] + [len(group['sets'][phase])])
        row['max_distinct_references'] = max(row['max_distinct_references'], most[group['id']])
    return out


def consensus_gap(row: dict | None) -> str:
    """Why a source has no consensus row, from its pool counts."""
    if row is None:
        return 'the source has no text in the R2 pool'
    readers, most = row['readers_per_text'], row['max_distinct_references']
    if most >= C.CONSENSUS_K:
        return (f"no consensus rows, although a reader has {most} distinct same-text references; "
                "the pool counts do not show the cause")
    if max(readers) > C.CONSENSUS_K:  # a text has enough readers, so the draw count per reader is the limit (r2pool.pair_ids)
        return (f"no consensus readers: each reader draws {row['references_per_participant']} references, so a reader has at most "
                f"{most} distinct same-text references; {C.CONSENSUS_K} are needed")
    return (f"no consensus readers: {row['texts']} texts with {min(readers)}-{max(readers)} readers of the set each, so a reader has "
            f"at most {most} distinct same-text references; {C.CONSENSUS_K} are needed ({C.CONSENSUS_K + 1} readers of one text)")


def consensus_select_report(r2c: dict, nulls: list[Null], availability: dict) -> dict:
    """Select null check of the consensus regime over the sources that have consensus rows (covered_null_report);
    `availability`: consensus_availability, which gives the cause for each fit source without consensus rows."""
    out = covered_null_report(r2c, nulls, lambda s: consensus_gap(availability.get(s)), 'consensus select')
    out['null']['consensus_availability'] = availability
    return out


def covered_null_report(regime: dict, nulls: list[Null], gap, name: str) -> dict:
    """Null check with equal weights over the sources that have rows (comparison-minutes within a source); the scope names
    those sources and, through gap(source), the cause for each fit source without rows. A rate over part of the fit
    sources cannot show the budget for the fit mixture."""
    measurable = source_weights(nulls)
    out = {**regime, 'null': {}, 'weighting': {**regime.get('weighting', {}), 'source_weights': measurable}}
    null_check(out, nulls)
    report = out['null']
    report['uncovered_sources'] = {s: gap(s) for s in sorted(set(regime.get('weighting', {}).get('source_weights', {})) - set(measurable))}
    report['source_weights'] = measurable
    report['scope'] = (f'{name} rates cover ' + (', '.join(measurable) or 'no source') + ' with equal source weights' +
                       ''.join(f'; {s} is not covered: {why}' for s, why in report['uncovered_sources'].items()))
    total = report['total_local']
    total['scope'] = report['scope']
    if report['uncovered_sources'] and total['budget_status'] != 'not measurable':
        # The fit mixture includes the uncovered sources, so this rate cannot show the budget for it.
        total['budget_status'] += ' on covered sources only'
        total['budget_holds_point'] = total['budget_holds_upper95'] = False
        report['budget_statement'] = 'over the covered sources only, ' + report['budget_statement']
    report['budget_statement'] = report['scope'] + '. ' + report['budget_statement']
    return out


def lockbox_pool(ds: Dataset, workdir: Path) -> dict:
    """A copy of the R2 pool whose lockbox readings are copied from the corpus mount to `workdir` and located like the fit
    and select readings at build time (poetry and Gettysburg cropped, others whole). The dataset and its manifest stay
    unchanged. Limit: the corpus mount of the dataset build must be present."""
    from .dataset import crop_null_readers
    from .r2pool import copy_audio
    pool = copy.deepcopy(ds.manifest['r2_pool'])
    entries = [r for g in pool['groups'] for r in g['entries'] if r['null_set'] == 'lockbox']
    for r in entries:
        r['audio'] = str(workdir / f"{r['id']}.wav")
    copy_audio(entries, workdir)
    built, planned = len(pool['excluded']), pool.get('planned_split_sha256')
    crop_null_readers(workdir, pool, ds.pool, ds.aligner, phases=('lockbox',), write_manifest=False)
    pool['planned_split_sha256'] = planned  # crop_null_readers sets it to the post-crop hash of the build
    pool['lockbox_excluded'] = pool['excluded'][built:]
    return pool


def lockbox_null_report(ds: Dataset, det: dict, *, final: bool) -> dict:
    """Final evaluation only (evaluate --final): false regions per comparison-minute of both R2 modes on the lockbox readers,
    with the select report's estimator, budget statement and per-source and per-L1 tables. The lockbox has no row for a fit
    source without lockbox readers, so each mode is weighted over the covered sources (covered_null_report)."""
    if not final:
        raise ValueError('the R2 lockbox is measured only by the final evaluation task')
    if not ds.manifest.get('r2_pool'):
        return {'set': 'lockbox', 'status': 'no R2 pool in the dataset'}
    started = time.monotonic()
    with tempfile.TemporaryDirectory(dir=ds.cache) as tmp:
        pool = lockbox_pool(ds, Path(tmp))
        log(f"R2 lockbox: {sum(len(g['sets']['lockbox']) for g in pool['groups'])} readings located; comparisons follow")
        single = grouped_nulls(ds, 'lockbox', pool=pool)
        consensus = grouped_nulls(ds, 'lockbox', consensus=True, pool=pool)
    readers = Counter()
    for g in pool['groups']:
        readers[g.get('source') or g['id'].split(':')[0]] += len(g['sets']['lockbox'])
    availability = consensus_availability(pool, 'lockbox')

    def gap(source):
        return (f'{readers[source]} lockbox readers of this source in the R2 pool' if readers[source]
                else 'the R2 pool partition has no lockbox reader of this source')

    modes = {'single': covered_null_report(det['regimes']['R2'], single, gap, 'lockbox single')['null'],
             'consensus5': covered_null_report(det['regimes']['R2_consensus'], consensus,
                                               lambda s: gap(s) if not readers[s] else consensus_gap(availability.get(s)),
                                               'lockbox consensus5')['null']}
    modes['consensus5']['consensus_availability'] = availability
    for mode, report in modes.items():
        log(f"R2 lockbox {mode}: {report['budget_statement']}; weighted={report['total_local']['rate']}/min")
    return {'set': 'lockbox', 'final_task': True, 'detector_config_sha256': det['config_sha256'],
            'split_sha256': pool['split_sha256'], 'planned_split_sha256': pool.get('planned_split_sha256'),
            'readers_by_source': dict(readers), 'comparisons': {'single': len(single), 'consensus5': len(consensus)},
            'excluded': pool['lockbox_excluded'],
            'modes': modes, 'seconds': round(time.monotonic() - started, 1)}


def choose_r1_row(curve):
    return max(curve, key=lambda r: (r['F1'], -r['h'])), 'in-sample strict F1 maximum; ties use smaller h'


def select_r1(pairs: list[tuple[Run, dict]], controls: list[Null], regime: dict, d9_floor: float = 0.0) -> list[dict]:
    """Joint train strict-F1 maximum for common h and independent speech-tempo h; ties use smaller thresholds. The
    speech-tempo grid keeps only physical thresholds above `d9_floor` (ln, noise_floor of the identity and placebo nulls),
    so that no such null reaches it; with no grid value left, D9 has no threshold."""
    allowed = calibration_types()
    pairs = [(run, {**lab, 'flaws': [f if f['type'] in allowed else {**f, 'evaluation_excluded': ['outside h-selection types']} for f in lab['flaws']]})
             for run, lab in pairs if any(f.get('type') in allowed for f in lab['flaws'])]
    common_grid = [h for h in C.H_GRID if C.R1_H_RANGE[0] <= h <= C.R1_H_RANGE[1]]
    natural_grid = [h for h in C.H_GRID if h * scale(regime, 'D9', -1) > d9_floor] or [None]
    components = []
    for natural, grid in ((False, common_grid), (True, natural_grid)):
        curve = []
        for h in grid:
            reg = {**regime, 'enabled': [d for d in regime['enabled'] if (d == 'D9') == natural], 'h': dict.fromkeys(KEYS,h)}
            cells = defaultdict(lambda: {'TP': 0, 'FP': 0, 'FN': 0, 'duplicates': 0, 'found': Counter(), 'total': Counter()})
            for run, lab in pairs:
                changed = dataclasses.replace(run, regions=decode(run.comp,reg,run.B.tr.sentence),
                                              clip={} if natural else clip_flags(run.comp,reg))
                ev = eval_clip(changed, lab, secondary_exempt=False)
                parent = lab.get('parent', {})
                speaker = parent.get('id') if isinstance(parent,dict) else parent
                cell = cells[speaker or lab.get('parent_id', str(id(run.B)))]
                for t in ev['truth']:
                    if not t['available'] or (t['type'] == 'NATURAL_RUSH') != natural:
                        continue
                    cell['TP'] += bool(t['detected'])
                    cell['FN'] += not t['detected']
                    cell['found'][t['type']] += bool(t['detected'])
                    cell['total'][t['type']] += 1
                cell['FP'] += len(ev['false']) + len(ev['false_clip'])
                cell['duplicates'] += ev['duplicate']
            control_regions = 0
            for n in controls:
                count = len(decode(n.comp,reg,n.sentence)) + (0 if natural else len(clip_flags(n.comp,reg)))
                cells[n.reader or n.id.split('__')[0]]['FP'] += count
                control_regions += count
            curve.append({'h': h, 'cells': cells, 'control_regions': control_regions})
        components.append(curve)
    ids = sorted({s for curve in components for row in curve for s in row['cells']})
    arrays = [np.array([[[row['cells'].get(s,{}).get(k,0) for k in ('TP','FP','FN')] for s in ids] for row in curve]) for curve in components]
    def optimum(common, natural):
        counts = common[:,None,:] + natural[None,:,:]
        denom = 2*counts[:,:,0]+counts[:,:,1]+counts[:,:,2]
        scores = np.divide(2*counts[:,:,0],denom,out=np.zeros_like(denom,dtype=float),where=denom>0)
        return scores, np.unravel_index(np.argmax(scores),scores.shape)
    scores, (best_i,best_j) = optimum(arrays[0].sum(axis=1),arrays[1].sum(axis=1))
    curve = []
    for i, common in enumerate(components[0]):
        j = int(np.argmax(scores[i]))
        natural = components[1][j]
        cells = list(common['cells'].values()) + list(natural['cells'].values())
        counts = [sum(c[k] for c in cells) for k in ('TP','FP','FN')]
        found, total = sum((c['found'] for c in cells),Counter()),sum((c['total'] for c in cells),Counter())
        curve.append({'h': common['h'], 'natural_rush_h': natural['h'], 'TP': int(counts[0]), 'FP': int(counts[1]), 'FN': int(counts[2]),
                      'F1': float(scores[i,j]), 'same_change_duplicates': sum(c['duplicates'] for c in cells),
                      'per_type_recall': {t: found[t]/n for t,n in total.items()},
                      'control_regions': common['control_regions']+natural['control_regions']})
    best, rule = choose_r1_row(curve)
    regime['h'] = {**dict.fromkeys(KEYS,best['h']), 'D9-': natural_grid[best_j]}
    regime['selection'] = rule
    regime['selected_operating_point'] = {**best, 'rule': rule, 'types': list(allowed),
                                         'objective': 'joint in-sample strict F1 on core8 + NATURAL_RUSH and train controls (' + STRICT_ACCOUNTING + '); independent D9 h; fixed whole-clip decisions'}
    regime['natural_rush_selection'] = {'h': natural_grid[best_j], 'objective': regime['selected_operating_point']['objective'],
                                        'noise_floor_ln': d9_floor, 'grid_min_h': natural_grid[0],
                                        'grid_rule': 'physical threshold h x scale above the largest |D9 x| of the train identity and placebo nulls '
                                                     '(clean); the noise-degraded identity variants are controls counted as false regions, not part of the floor',
                                        'threshold_ln': None if natural_grid[best_j] is None else natural_grid[best_j] * scale(regime, 'D9', -1),
                                        'control_max_abs_x_ln': noise_floor(controls, 'D9'),
                                        'limit': 'the common (D9 off) and speech-tempo (D9 only) components are decoded and counted separately, '
                                                 'so a D1- and a D9- false region on the same words count as two false regions in this objective'}
    selected, joint = Counter(), Counter()
    rng = np.random.default_rng(C.SEED)
    for _ in range(C.R2_BOOTSTRAPS if ids else 0):
        sample = rng.integers(len(ids),size=len(ids))
        _, (i,j) = optimum(arrays[0][:,sample,:].sum(axis=1),arrays[1][:,sample,:].sum(axis=1))
        selected[common_grid[i]] += 1
        joint[common_grid[i],natural_grid[j]] += 1
    regime['selection_bootstrap'] = {'unit': 'source speaker; controls retained with speaker; both thresholds refitted',
                                     'speakers': len(ids), 'draws': sum(selected.values()), 'chosen_h_counts': dict(sorted(selected.items())),
                                     'joint_h_counts': [{'h': h, 'natural_rush_h': nh, 'draws': n} for (h,nh),n in sorted(joint.items())]}
    return curve


def r2_stability(nulls: list[Null], readers: list[str] | None = None) -> dict:
    """Leave one source/text group out; legacy datasets can still request reader removal."""
    rows = []
    groups = sorted({n.group for n in nulls if n.group})
    for removed in groups or readers or []:
        kept = [n for n in nulls if n.group != removed] if groups else [n for n in nulls if removed not in n.id.split('>')]
        reg, _ = fit_r2(kept, full_curve=False)
        rows.append({'removed_group' if groups else 'removed_reader': removed, **{k: reg[k] for k in ('h', 'clip', 'scales')}})
    ranges = {}
    for k in (k for k in KEYS if C.dim_of(k) in C.REGIME_DIMS['R2']):
        vals = [r['h'][k] * scale(r, C.dim_of(k), 1 if k.endswith('+') else -1) for r in rows if r['h'][k] is not None]
        ranges[k] = {'min_threshold': min(vals) if vals else None, 'max_threshold': max(vals) if vals else None,
                     'disabled_refits': sum(r['h'][k] is None for r in rows)}
    for k in C.CLIP_DIMS:
        vals = [r['clip'][k] for r in rows if r['clip'].get(k) is not None]
        ranges[k + ' whole clip'] = {'min_threshold': min(vals) if vals else None, 'max_threshold': max(vals) if vals else None,
                                    'disabled_refits': sum(r['clip'].get(k) is None for r in rows)}
    return {'method': 'leave-one-group-out' if groups else 'leave-one-reader-out', 'rows': rows, 'threshold_ranges': ranges}


def noisy_identity(wav, baseline_id: str):
    """20 dB SNR white-noise identity control, same transform as evaluation."""
    return audio.quantize(stress.noise(wav, flaws.clip_seed(baseline_id)))


# ============================================================================================ score gates
def clip_penalties(ds: Dataset, clips: list[dict], recs: list, regime: dict) -> list[dict]:
    """Penalty P_k per dimension of every clip (`recs`: its analysed recording) under the R1 detector (independent of Pmax)."""
    rows = []
    pm = dict(C.PMAX_START)
    for c, P in zip(clips, recs):
        B = ds.rec(ds.entry("baselines", c["parent"]))
        comp = compare(B, P)
        sc = score(comp, decode(comp, regime, B.tr.sentence), regime, pm)
        lab = ds.labels(c)
        rows.append({"id": c["id"], "baseline": c["parent"], "recipe": c["recipe"], "P": sc.P,
                     "scored_dims": [k for k, v in sc.S.items() if v is not None],
                     "levels": sorted({f["level"] for f in lab["flaws"] if f["level"] is not None}), "n_regions": int(sum(m > 0 for m in sc.masses))})
    return rows


def gate_violations(rows: list[dict], pmax: dict[str, float]) -> list[str]:
    """Gates of DESIGN 6: identity = 100; every L1-only clip >= 90; G5 <= 50; each speech's ladder non-increasing."""
    bad = []
    by = {}
    for r in rows:
        o = overall(r["P"], pmax, r["scored_dims"])
        if o is None:
            bad.append(f"{r['id']}: no scored dimensions")
            continue
        by.setdefault(r["baseline"], {})[r["recipe"]] = o
        if r["recipe"] == "identity" and o < C.GATE_IDENTITY - 0.005:
            bad.append(f"{r['id']}: identity scores {o:.2f}")
        if (r["recipe"] == "G1" or r.get("levels") == [1] or r["recipe"] in ("single_L1A", "single_L1B")) and o < C.GATE_L1_MIN:
            bad.append(f"{r['id']}: L1-only clip scores {o:.2f} < {C.GATE_L1_MIN}")
        if r["recipe"] == "G5" and o > C.GATE_G5_MAX:
            bad.append(f"{r['id']}: G5 scores {o:.2f} > {C.GATE_G5_MAX}")
    for b, d in by.items():
        if all(k in d for k in ("G1", "G3", "G5")) and not d["G1"] >= d["G3"] >= d["G5"]:
            bad.append(f"{b}: ladder not non-increasing (G1 {d['G1']:.2f}, G3 {d['G3']:.2f}, G5 {d['G5']:.2f})")
    return bad


def fit_pmax(rows: list[dict]) -> tuple[dict[str, float], float, list[str]]:
    """Uniform factor on the starting Pmax meeting the gates on `rows` (closest to 1); if none does, the factor with the
    fewest violations. Returns (Pmax, factor, remaining violations)."""
    best = None
    for f in C.PMAX_FACTOR_GRID:
        pmax = {k: v * f for k, v in C.PMAX_START.items()}
        bad = gate_violations(rows, pmax)
        key = (len(bad), abs(np.log(f)))
        if best is None or key < best[0]:
            best = (key, pmax, f, bad)
    assert best is not None
    return best[1], best[2], best[3]


# ============================================================================================ run
def select_edit_sample(ds, nulls):
    """Seeded type/source/text round-robin sample, capped by clips and forecast seconds."""
    from .r2pool import digest
    entries = {e['id']: e for e in ds.manifest.get('readers', [])}
    by_reader = defaultdict(list)
    for n in nulls:
        b, p = n.id.split('>')
        by_reader[p].append(b)
    buckets = defaultdict(list)
    for p, refs in sorted(by_reader.items()):
        e = entries[p]
        for typ in (t for t in C.FLAW_TYPES if C.FLAW_DIM[t] in C.DIMS):
            token = (typ, e.get('source', ''), e.get('group', ''))
            buckets[token].append({'participant': p, 'references': refs, 'type': typ,
                                   'id': f'{p}__select_{typ}_L3'})
    for rows in buckets.values():
        rows.sort(key=lambda r: digest([C.SEED, r['id']]))
    selected, spent = [], 0.
    by_type = defaultdict(list)
    for k in sorted(buckets, key=lambda k: digest([C.SEED, k])):
        by_type[k[0]].append(k)
    types = sorted(by_type, key=lambda t: digest([C.SEED, t]))
    keys = [by_type[t][i] for i in range(max((len(v) for v in by_type.values()), default=0)) for t in types if i < len(by_type[t])]
    while keys and len(selected) < C.R2_SELECT_EDIT_CAP:
        remaining = []
        for k in keys:
            row = buckets[k].pop(0)
            duration = entries[row['participant']].get('duration_s', 30.)
            # Clean, references and edited preparation plus DSP; no worker speedup assumed.
            durations = [duration, duration, *[entries[b].get('duration_s', 30.) for b in set(row['references'])]]
            cost = 5. + sum(d * C.R2_ALIGNMENT_SECONDS_PER_AUDIO + C.R2_ALIGNMENT_SECONDS_PER_CLIP for d in durations)
            if spent + cost <= C.R2_SELECT_EDIT_BUDGET_S and len(selected) < C.R2_SELECT_EDIT_CAP:
                selected.append(row)
                spent += cost
            if buckets[k]:
                remaining.append(k)
        keys = remaining
    return selected, {'seed': C.SEED, 'method': 'seeded round-robin over type/source/text buckets',
                      'cap': C.R2_SELECT_EDIT_CAP, 'batch_size': C.R2_SELECT_EDIT_BATCH,
                      'budget_seconds': C.R2_SELECT_EDIT_BUDGET_S, 'expected_seconds': spent,
                      'candidate_edits': len(by_reader) * sum(C.FLAW_DIM[t] in C.DIMS for t in C.FLAW_TYPES), 'selected_edits': len(selected),
                      'by_type': dict(Counter(r['type'] for r in selected)), 'sample': selected}


def select_edit_task(clean, ref, row):
    cid = row['id']
    seed = flaws.clip_seed(cid)
    plan = flaws.plan_clip(clean, [(row['type'], 3)], seed, ref=ref)
    if not plan.edits:
        return None
    wav, lab = flaws.inject(clean, plan, cid, row['participant'], recipe='select_L3', seed=seed)
    return (wav, lab) if lab['flaws'] else None


def select_edit_pairs(ds, nulls, sample=None, report=None):
    """Yield pool-prepared edit batches; release participant/reference audio after matching."""
    entries = {e['id']: e for e in ds.manifest.get('readers', [])}
    if sample is None:
        sample, _ = select_edit_sample(ds, nulls)
    for start in range(0, len(sample), C.R2_SELECT_EDIT_BATCH):
        rows = sample[start:start + C.R2_SELECT_EDIT_BATCH]
        ids = sorted({i for row in rows for i in [row['participant'], *row['references']]})
        recs = dict(zip(ids, ds.recs([entries[i] for i in ids])))
        rendered = map_calls(select_edit_task, [(recs[row['participant']], recs[row['references'][0]], row) for row in rows], ds.pool)
        made = [(row, item) for row, item in zip(rows, rendered) if item is not None]
        edited = ds.prepare_many([(item[0], recs[row['participant']].tr) for row, item in made])
        if report is not None:
            report['placed_edits'] = report.get('placed_edits', 0) + len(made)
            report.setdefault('skipped', []).extend({'id': row['id'], 'reason': 'no eligible or realised edit'} for row, item in zip(rows, rendered) if item is None)
        try:
            yield [(recs[b], recs[row['participant']], P, item[1])
                   for (row, item), P in zip(made, edited) for b in row['references']]
        finally:
            for i in ids:
                ds._recs.pop(i, None)
        log(f"select positives: {min(start + len(rows), len(sample))}/{len(sample)} sampled edits processed")


def _away_outcomes(pairs, regimes):
    from .events import truths
    from .evaluate import cross_matches, edit_direction
    outcomes = {token: (Counter(), Counter()) for token in regimes}
    for B, clean, edited, lab in pairs:
        before, after = compare(B, clean), compare(B, edited)
        original = Run(B, clean, before, [], None, 'R2', {})
        changed = Run(B, edited, after, [], None, 'R2', {})
        tr = [t for t in truths(lab) if t['available'] and t['level'] == 3 and
              edit_direction(original, changed, t)['direction'] == 'away from the reference']
        for token, reg in regimes.items():
            run0 = dataclasses.replace(original, regions=decode(before, reg, B.tr.sentence), clip=clip_flags(before, reg))
            run1 = dataclasses.replace(changed, regions=decode(after, reg, B.tr.sentence), clip=clip_flags(after, reg))
            _, hits, _ = cross_matches(run0, run1, tr, reg)
            found, total = outcomes[token]
            for i, t in enumerate(tr):
                k = key(t['dim'], t['sign']) + (' whole clip' if t['event'] == 'clip' else '')
                total[k] += 1
                found[k] += i in hits
    return outcomes


def _away_hits(pairs, reg):
    return _away_outcomes(pairs, {'current': reg})['current']


def real_gate(gate):
    return gate.get('lab_pass') is True and gate.get('auc', 0) >= C.PROMOTION_AUC_MIN and gate.get('auc_lower95', 0) > C.PROMOTION_AUC_LOWER_MIN


def promote_r2(fit, select, pairs, current, validation):
    """Only refit open gates; aggregate new/worsened hits once per regime over bounded edit batches."""
    import itertools
    labels = validated_labels(validation)
    fixed = C.OWNER_LISTED['R2']
    candidates = [d for d in C.LISTED_DIMS['R2'] if d not in fixed and real_gate(validation.get(key(d, 1), {}))]
    regimes = {((), False): current}
    for size in range(1, len(candidates) + 1):
        for subset in itertools.combinations(candidates, size):
            variants = (False, True) if 'D7' in subset and labels.get('uneven_tempo', False) else (False,)
            for whole in variants:
                switches = {**labels, 'uneven_tempo': whole}
                regimes[subset, whole], _ = fit_r2(fit, full_curve=False, enabled=(*current['enabled'], *subset), labels=switches)
    outcomes = {token: (Counter(), Counter()) for token in regimes}
    if candidates:
        batches = [pairs] if isinstance(pairs, list) else pairs
        for batch in batches:
            for token, (found, total) in _away_outcomes(batch, regimes).items():
                outcomes[token][0].update(found)
                outcomes[token][1].update(total)
    rows, chosen = [], ((), False)
    for dim in C.LISTED_DIMS['R2']:
        flag = key(dim, 1)
        gate = validation.get(flag, {})
        if dim in fixed:
            rows.append({'key': next(k for k in KEYS if C.dim_of(k) == dim), 'status': 'listed', 'rate': None, 'bootstrap_upper95': None,
                         'rule_of_three': None, 'recall': None, 'lab_real_gate': False, 'validation': {}, 'reason': fixed[dim]})
            continue
        if dim not in candidates:
            rows.append({'key': flag, 'status': 'listed', 'rate': None, 'bootstrap_upper95': None,
                         'rule_of_three': None, 'recall': None, 'lab_real_gate': False,
                         'validation': gate, 'reason': 'lab/Real gate closed; refit and select edits skipped'})
            continue
        subset = tuple(d for d in candidates if d in (*chosen[0], dim))
        token = (subset, chosen[1])
        whole_key = 'D7+ whole clip'
        whole_pass = False
        whole_report = None
        whole_diagnostic = None
        if dim == 'D7' and (subset, True) in regimes:
            whole_trial = regimes[subset, True]
            whole_hits, whole_total = outcomes[subset, True]
            whole_diagnostic = (whole_hits[whole_key], whole_total[whole_key])
            whole_recall = whole_hits[whole_key] / whole_total[whole_key] if whole_total[whole_key] else None
            checked = {**whole_trial, 'null': {}}
            null_check(checked, select)
            whole_report = checked['null']['clip_by_key'].get('D7', {})
            baseline_hits = outcomes[chosen][0]
            whole_pass = (whole_recall is not None and whole_recall >= C.PROMOTION_RECALL_MIN and
                          whole_report.get('rate') is not None and whole_report['rate'] <= whole_trial['null']['clip_budget_per_key'] and
                          max((n - whole_hits[k] for k, n in baseline_hits.items()), default=0) <= C.PROMOTION_MAX_EXISTING_LOSS)
            if whole_pass:
                token = (subset, True)
        trial = regimes[token]
        h = trial['h'][flag]
        counts = region_counter(select, dim, scale(trial, dim, 1), 1)(h) if h is not None else np.zeros(len(select), int)
        report = rate_report(select, counts, fixed=trial.get('weighting', {}).get('source_weights', source_weights(fit)), flag=flag)
        baseline_hits, _ = outcomes[chosen]
        hits, total = outcomes[token]
        recall = hits[flag] / total[flag] if total[flag] else None
        whole_key = flag + ' whole clip'
        whole_found, whole_total = whole_diagnostic or (hits[whole_key], total[whole_key])
        whole_recall = whole_found / whole_total if whole_total else None
        losses = {k: max(0, n - hits[k]) for k, n in baseline_hits.items()}
        select_reg = {**trial, 'null': {}}
        null_check(select_reg, select)
        null_report = select_reg['null']
        within = bool(select) and all(r['rate'] is not None and r['rate'] <= trial['null']['budget_per_key']
                                     for r in null_report['local_by_key'].values())
        within &= all(r['rate'] is not None and r['rate'] <= trial['null']['clip_budget_per_key']
                      for r in null_report['clip_by_key'].values())
        promoted = h is not None and within and recall is not None and recall >= C.PROMOTION_RECALL_MIN and max(losses.values(), default=0) <= C.PROMOTION_MAX_EXISTING_LOSS
        whole_pass = whole_pass and promoted
        rows.append({'key': flag, 'status': 'promoted' if promoted else 'listed', 'h': h,
                     'budget': trial['null']['budget_per_key'], **report, 'recall': recall,
                     'found': hits[flag], 'away_edits': total[flag], 'lab_real_gate': True,
                     'whole_clip': {'key': whole_key, 'recall': whole_recall, 'found': whole_found,
                                    'away_edits': whole_total, 'status': 'promoted' if whole_pass else 'disabled',
                                    **(whole_report or null_report['clip_by_key'].get(dim, {}))} if dim in C.CLIP_DIMS else None,
                     'validation': gate, 'existing_losses': losses, 'within_budget': within,
                     'trial_enabled': trial['enabled'], 'select_null': null_report,
                     'reason': 'all gates passed' if promoted else 'failed null, L3 recall or existing-key gate'})
        if promoted:
            chosen, current = token, trial
    current['pattern_labels'] = {**labels, 'uneven_tempo': current.get('pattern_labels', {}).get('uneven_tempo', False)}
    null_check(current, fit)
    return current, {'set': 'select', 'criteria': {'recall_min': C.PROMOTION_RECALL_MIN,
                      'auc_min': C.PROMOTION_AUC_MIN, 'auc_lower95_above': C.PROMOTION_AUC_LOWER_MIN,
                      'existing_loss_max': C.PROMOTION_MAX_EXISTING_LOSS}, 'rows': rows}


def validated_labels(validation):
    out = {}
    for name in sorted(set(C.PATTERN_GATES.values())):
        row = validation.get('labels', {}).get(name, {})
        passed = row.get('lab_pass') is True
        if name in ('repetition', 'filled_pause'):
            passed &= row.get('precision', 0) >= C.LABEL_PRECISION_MIN
        if name == 'prolongation':
            passed &= row.get('low_f0') is True
        out[name] = passed
    return out


def noise_floor(nulls: list[Null], dim: str) -> float:
    """Alignment-noise floor of a dimension: the largest |x| over the nulls (identity and placebo variants), physical units."""
    return max((float(np.max(np.abs(n.comp.dims[dim].x[np.isfinite(n.comp.dims[dim].x)]), initial=0.)) for n in nulls), default=0.)


def alignment_noise(items, recs, nulls):
    rows = []
    for item, P, n in zip(items,recs,nulls):
        B = item['B']
        rows.append({'id': n.id, 'max_start_shift_ms': float(np.max(np.abs(P.al.start-B.al.start))*1000),
                     'max_end_shift_ms': float(np.max(np.abs(P.al.end-B.al.end))*1000),
                     'by_key_max_abs_delta': {k: float(np.max(np.abs(d.x[np.isfinite(d.x)]), initial=0.)) for k,d in n.comp.dims.items()}})
    return {'rows': rows, 'floor_by_key': {k: noise_floor(nulls, k) for k in C.DIMS}, 'scope': 'identity/placebo word-boundary and feature noise floor; train only',
            'identity_shift_640ms': {'status': 'open', 'evidence': 'v10 CPU reproduction: Eisenhower word 15 baseline 8.40–9.06 s, identity 7.76–9.06 s; word PCM identical',
                                    'cause': 'context-dependent CTC alignment; exact emission/path cause unresolved, beyond 20 ms frame rounding'}}


def d7_null_gate(regime, nulls):
    rows = []
    for n in nulls:
        d = n.comp.dims['D7']
        valid = d.countable & np.isfinite(d.x)
        flags = decode_dim(d, scale(regime, 'D7', 1), 1., n.sentence, (1,))
        identity = '__identity' in n.id
        peak = float(np.max(np.abs(d.x[valid]), initial=0.))
        rows.append({'id': n.id, 'split': n.split, 'valid_units': int(valid.sum()), 'regions_at_floor': len(flags),
                     'max_abs_x': peak, 'passed': not flags and (not identity or peak <= C.D7_IDENTITY_TOL_LN)})
    passed = bool(rows) and sum(r['valid_units'] for r in rows) > 0 and all(r['passed'] for r in rows)
    if not passed:
        regime['enabled'] = [d for d in regime['enabled'] if d != 'D7']
        regime['h']['D7+'] = None
        regime['clip']['D7'] = None
    return {'passed': passed, 'status': 'scored' if passed else 'listed', 'identity_tolerance_ln': C.D7_IDENTITY_TOL_LN,
            'rows': rows, 'reason': 'identity and placebo gates passed' if passed else 'identity deltas or placebo flags fail the gate; D7 listed and unscored in R1'}


def run(dataset: Path, cache: Path | None, out: Path, pool=None, aligner=None, validation=None) -> dict:
    started = time.monotonic()
    if validation is None:
        validation = json.loads(LAB_VALIDATION.read_text())
    ds = load_dataset(dataset, cache, pool, aligner)
    from .evaluate import STAGE_FORECAST_SECONDS
    log("forecast T4 x2 from v13: " + "; ".join(f"{stage} {low / 60:.0f}-{high / 60:.0f} min" for stage, (low, high) in STAGE_FORECAST_SECONDS.items()))
    cal = reader_ids(ds, "reader_calibration")
    gate_clips = {sp: [c for c in ds.clips(kind="single") + ds.clips(kind="identity") + ds.clips(kind="ladder")
                       if ds.entry("baselines", c["parent"])["split"] == sp and calibration_clip(c)] for sp in ("train", "val")}
    log("clean recordings (train + val baselines, calibration readers)")
    ds.recs([b for b in ds.manifest["baselines"] if b["split"] in ("train", "val")] + [ds.entry("readers", i) for i in cal])
    log("R1 train nulls (identity + placebo seeds): placebo clips")
    items = r1_items(ds, ("train",))
    identities = [c for c in gate_clips["train"] if c["kind"] == "identity"]
    noisy = map_calls(noisy_identity, [(ds.wav(c), c["id"]) for c in identities], ds.pool)
    noise_items = [{"id": c["id"] + "__noise20", "split": "train", "B": ds.rec(ds.entry("baselines", c["parent"])),
                    "tr": ds.clip_transcript(c), "wav": w} for c, w in zip(identities, noisy)]
    log(f"R1 preparation: {len(items)} null clips and {len(gate_clips['train']) + len(gate_clips['val'])} score-gate clips; expected 1-2 min on T4 x2")
    clips = gate_clips["train"] + gate_clips["val"]
    n_gate = len(clips)
    ids = {c['id'] for c in clips}
    clips += [c for c in ds.clips(kind='single') if c['id'] not in ids and c['split'] == 'train' and
              c['level'] in C.HEADLINE_LEVELS and any(t in calibration_types() for t in c.get('types', []))]
    recs = ds.prepare_many([(i["wav"], i["tr"]) for i in items] + [(ds.wav(c), ds.clip_transcript(c)) for c in clips] + [(i["wav"], i["tr"]) for i in noise_items])
    n1 = null_list(items, recs[:len(items)])
    nuisance = n1 + null_list(noise_items, recs[len(items) + len(clips):])
    log("R2 train nulls (calibration reader pairs)")
    log(f"R2 fit: {sum(len(g['sets']['fit']) for g in ds.manifest.get('r2_pool', {}).get('groups', []))} readings, five references each; expected 4-6 min including group refits")
    n2 = grouped_nulls(ds, 'fit') if ds.manifest.get('r2_pool') else r2_nulls(ds, cal, cal)
    r1 = base_regime("R1", n1)
    d7_gate = d7_null_gate(r1, n1)
    r1['pattern_labels'] = validated_labels(validation or {})
    if not r1['pattern_labels'].get('uneven_tempo', False):
        r1['clip']['D7'] = None
    r2, t2 = fit_r2(n2)
    consensus_fit = grouped_nulls(ds, "fit", consensus=True) if ds.manifest.get("r2_pool") else []
    r2c, t2c = fit_r2(consensus_fit)
    r2c["pattern_labels"] = {**validated_labels(validation), "uneven_tempo": False}
    r2c["reference_mode"] = "consensus5"
    r2["reference_mode"] = "single"
    det0 = make_detector({"R1": r1, "R2": r2}, C.PMAX_START, {})  # R1 without thresholds: select_r1 decodes at each candidate h
    pairs = [(run_pair(ds.rec(ds.entry("baselines", c["parent"])), P, det0, "R1"), ds.labels(c))
             for c, P in zip(clips, recs[len(items):len(items) + len(clips)])
             if c["split"] == "train" and c["kind"] == "single" and c["level"] in C.HEADLINE_LEVELS]
    log(f"R1 selection: {len(pairs)} train positives, {len(nuisance)} controls, {len(C.H_GRID)} grid points; expected <1 min")
    t1 = select_r1(pairs, nuisance, r1, noise_floor(n1, 'D9'))
    if not d7_gate['passed']:
        r1['h']['D7+'] = None
    null_check(r1, n1)
    log(f"R2 stability: {len({n.group for n in n2 if n.group})} group refits over {len(n2)} fit comparisons; expected 2-4 min")
    stability = r2_stability(n2, cal)
    log(f"R2 select: {sum(len(g['sets']['select']) for g in ds.manifest.get('r2_pool', {}).get('groups', []))} readings, five references each; expected 2-3 min")
    select = grouped_nulls(ds, 'select') if ds.manifest.get('r2_pool') else []
    consensus_select = grouped_nulls(ds, "select", consensus=True) if ds.manifest.get("r2_pool") else []
    availability = consensus_availability(ds.manifest['r2_pool'], 'select') if ds.manifest.get('r2_pool') else {}
    consensus_report = consensus_select_report(r2c, consensus_select, availability)
    log('R2 consensus select: ' + consensus_report['null']['budget_statement'] + '; weighted=' +
        str(consensus_report['null']['total_local']['rate']) + '/min; pooled=' + str(consensus_report['null']['total_local']['pooled_rate']) + '/min')
    validation = validation or {}
    open_gates = any(real_gate(validation.get(key(d, 1), {})) for d in C.LISTED_DIMS['R2'] if d not in C.OWNER_LISTED['R2'])
    sample, sample_report = select_edit_sample(ds, select) if open_gates else ([], {'selected_edits': 0, 'expected_seconds': 0, 'reason': 'lab/Real gates closed'})
    log(f"select positives: {len(sample)} edits, {sum(len(r['references']) for r in sample)} comparisons, batch {C.R2_SELECT_EDIT_BATCH}, seed {C.SEED}; expected {sample_report['expected_seconds'] / 60:.1f} min on T4 x2")
    positive_pairs = select_edit_pairs(ds, select, sample, sample_report)
    r2, promotion = promote_r2(n2, select, positive_pairs, r2, validation)
    promotion['positive_sample'] = sample_report
    select_report = {'null': {}}
    if select:
        select_report.update(r2)
        select_report['null'] = {}
        null_check(select_report, select)
        log('R2 select: ' + select_report['null']['budget_statement'] + '; weighted=' +
            str(select_report['null']['total_local']['rate']) + '/min; pooled=' + str(select_report['null']['total_local']['pooled_rate']) + '/min')
    log(f"R1 h={r1['h']['D1-']} ({r1['null']['false_per_minute_at_h']}/min over {r1['null']['total_local']['independent_recording_exposure']:.3f} "
        f"independent recording-minutes, {r1['null']['minutes']} comparison-minutes; {r1['null']['budget_statement']}); "
        f"R2 h={r2['h']} clip={r2['clip']} ({r2['null']['false_per_minute_at_h']}/min over {r2['null']['minutes']} min)")
    regimes = {"R1": r1, "R2": r2, "R2_consensus": r2c}
    rows = clip_penalties(ds, clips[:n_gate], recs[len(items):len(items) + n_gate], r1)
    n_train = len(gate_clips["train"])
    train_rows, val_rows = rows[:n_train], rows[n_train:]
    log(f"Pmax: {len(train_rows)} train and {len(val_rows)} validation clips; expected <1 min")
    pmax, factor, bad_train = fit_pmax(train_rows)
    bad_val = gate_violations(val_rows, pmax)  # val only reports; it never feeds the fit
    log(f"Pmax factor {factor:.3f}; train gate violations {len(bad_train)}; val gate violations {len(bad_val)}")
    report = {"manifest_sha256": sha256_file(ds.root / "manifest.json"), "calibrated": True, "pipeline_version": __version__, "alignment_device": device_class(pool), "pmax_factor": round(float(factor), 4), "extra_calibration": calibration_policy(),
              "gates_train": {"violations": bad_train, "n_clips": len(train_rows)}, "gates_val": {"violations": bad_val, "n_clips": len(val_rows)},
              "R1": r1["null"], "R2": r2["null"], 'promotion': promotion, 'real_validation': validation or {}, 'D7_R1_gate': d7_gate, 'alignment_noise_floor': alignment_noise(items,recs[:len(items)],n1), 'R2_modes': {'single': mode_report(r2,select_report['null']), 'consensus5': mode_report(r2c,consensus_report['null'])}}
    from .protocol import exemption_policy
    report['exemptions'] = exemption_policy()
    det = make_detector(regimes, pmax, report)
    save_detector(det, out / "models" / "detector.json")
    full = {"r2_partition": {k: ds.manifest.get('r2_pool', {}).get(k) for k in ('split_sha256', 'references_per_participant', 'reference_sampling', 'lab_readers')},
            "detector_config_sha256": det["config_sha256"], "alignment_device": device_class(pool), "R2_h_table": t2, "R2_consensus_h_table": t2c, "R2_consensus_select": consensus_report["null"], "R2_modes": {'single': mode_report(r2,select_report['null']), 'consensus5': mode_report(r2c,consensus_report['null'])},
            "R1_selection": t1, "R1_selected": r1["selected_operating_point"], 'R1_speaker_bootstrap': r1['selection_bootstrap'], "R2_stability": stability, "R2_select": select_report["null"], 'promotion': promotion, "nuisance_controls": [n.id for n in nuisance],
            "train_penalties": train_rows, "val_penalties": val_rows, "nulls": {"R1": [n.id for n in n1], "R2": [n.id for n in n2]}, "report": report}
    (out / "calibration").mkdir(parents=True, exist_ok=True)
    (out / "calibration" / "report.json").write_text(json.dumps(full, indent=1, sort_keys=True) + "\n")
    log(f"calibration complete: {time.monotonic() - started:.1f} s; {len(n2)} fit and {len(select)} select comparisons, {sample_report.get('placed_edits', 0)} select positives")
    log(f"wrote {out / 'models' / 'detector.json'} (config {det['config_sha256'][:12]})")
    return det


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="python -m cvoice.calibrate")
    ap.add_argument("--dataset", type=Path, default=ROOT / "data")
    ap.add_argument("--cache", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=ROOT)
    ap.add_argument('--validation', type=Path, help='select-independent lab/Real gate report; absent gates stay closed')
    a = ap.parse_args(argv)
    with PreparePool(cache_dir=a.cache) as pool:
        run(a.dataset, a.cache, a.out, pool, validation=json.loads(a.validation.read_text()) if a.validation else None)



def calibration_types():
    return (*C.CORE8_TYPES, 'NATURAL_RUSH')


def calibration_clip(clip):
    return clip.get("spectrum") != "extra" or (bool(clip.get('types')) and
           all(t in calibration_types() for t in clip['types']))


def calibration_policy():
    return {"new_types_in_R1": ['NATURAL_RUSH'],
            "R1": "joint in-sample strict F1 maximum on core8 + NATURAL_RUSH (" + STRICT_ACCOUNTING + "); independent speech-tempo h; synthetic-only families evaluated separately",
            "R2": "single and median-of-five same-text references; equal-source comparison-minute point rate; separate clip budget"}


if __name__ == "__main__":
    main()
