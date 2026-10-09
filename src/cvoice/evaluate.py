"""Evaluation (Kaggle): every metric and table of docs/technical.md section 6 on the frozen split, as JSON + Markdown tables + PNG figures.

    python -m cvoice.evaluate --dataset /kaggle/working/data --models /kaggle/working/out/models/detector.json \
        --cache /kaggle/working/cache --out /kaggle/working/out [--splits train,val] [--final [--force]]

Splits: --splits (default train,val). The test split and the R2 lockbox (both reference modes) are evaluated only with
--final, which records the config hash in final_evaluations.json beside detector.json and refuses a second run for the
same hash unless --force. Regimes are never
pooled, and train is never pooled with held-out (val, test) in any table, matrix or figure. Every number carries its k-of-n
counts and exposure. Chain A is the headline; chain B, the stress matrix, the repair test, trivial baselines, the
reproducibility check and the GPU/CPU device agreement follow. Batch-first: every section collects its clip variants, analyses
them in one pool batch, then scores. Sections are isolated: a failing section is recorded in results.json, everything that
worked is written, and the exit code is non-zero.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import math
import re
import sys
import traceback
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from . import audio, flaws, stress
from . import config as C
from .detect import scale
from .calibrate import (Null, best_by_f1, calibration_policy, g5_gate_fails, grouped_nulls, identity_gate_fails, l1_gate_fails,
                        lockbox_null_report, null_check, r1_common_grid, r1_nulls, r2_nulls, reader_ids)
from .dataset import Dataset, load_dataset, sha256_file
from .detect import KEYS, Region, clip_flags, decode, decode_dim, flagged_dims, key, load_detector, threshold
from .events import Run, clip_key, eval_clip, f1, false_change_duplicates, match, near, overlaps, run_pair, truths
from .compare import Comparison, _speech_time
from .features import Recording
from .pipeline import ROOT, analyze, differences, device_class, dumps, make_job, map_calls
from .pool import PreparePool, worker_aligner
from .protocol import STRICT_ACCOUNTING, exemption_policy, tiers
from .uncertainty import MIN_BOOTSTRAP_CLUSTERS, cluster_summary, wilson, proportion, poisson

EXPECTED = {  # expectation table, fixed before evaluation: level -> expectation per regime
    "R1": {1: "marginal: detection near or below 50 %; clip score >= 90", 2: "flagged", 3: "flagged"},
    "R2": {1: "must stay silent", 2: "marginal", 3: "flagged for pace, pauses, pitch, volume; D4 and D6 not scored"},
}
HELD_OUT = ("val", "test")
DEFAULT_SPLITS = ("train", "val")
ALL_SPLITS = ("train", "val", "test")
LEVEL_GROUPS = {"headline (L2+L3)": C.HEADLINE_LEVELS, "sensitivity (L1)": (1,)}
FINAL_LOG = "final_evaluations.json"
# Kaggle T4 x2 forecast per stage, s [low, high]: measured development-run times (STAGE_FORECAST_BASIS), plus the test split and the R2 lockbox.
STAGE_FORECAST_SECONDS = {'dataset': [1260, 1380], 'calibrate': [1140, 1320], 'evaluate': [4400, 5200], 'gallery': [55, 70],
                          'bootstrap_packaging': [180, 240]}
STAGE_FORECAST_BASIS = ('v13 measured on T4 x2: dataset 1299.7 s, calibrate 1179.0, evaluate 3374.4 (stress about 2500 of it), gallery '
                        '57.4, bootstrap and packaging 200; the final evaluation adds the test split (stress cases x1.25, held-out sections '
                        'x2, directional x1.3) and the R2 lockbox (251 readers, both modes)')


def log(msg: str) -> None:
    print(f"[evaluate] {msg}", flush=True)


def held_out(splits: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(s for s in splits if s in HELD_OUT)


def split_groups(splits: tuple[str, ...]) -> list[tuple[str, tuple[str, ...]]]:
    """Report groups: every split on its own, and val+test when both ran. Train is never pooled with held-out."""
    groups = [(s, (s,)) for s in splits]
    if "val" in splits and "test" in splits:
        groups.append(("val+test", ("val", "test")))
    return groups


# ============================================================================================ helpers
def number_text(v) -> str:
    """A float to 3 significant digits in positional notation, whole numbers (counts stored as floats) in full; |v| < 1e-6
    is 0 (residue of a bound at 0 or 1)."""
    if not np.isfinite(v):
        return "n/a"
    if abs(v) < 1e-6:
        return "0"
    if float(v).is_integer():
        return str(int(v))
    return np.format_float_positional(float(f"{v:.3g}"), trim="-")


def bounds_text(ci, label: str = "95%") -> str:
    """An interval with both bounds; equal bounds are a degenerate interval and are printed as such."""
    if not ci or ci[0] is None or ci[1] is None:
        return "n/a"
    lo, hi = md_cell(ci[0]), md_cell(ci[1])
    if lo == hi:
        return f"degenerate [{lo}, {hi}] (no spread across the resampled clusters)"
    return f"{label} [{lo}, {hi}]".strip()


def md_cell(v) -> str:
    """Floats to three significant digits, also inside interval lists."""
    if v is None:
        return ""
    if isinstance(v, float):
        return number_text(v)
    if isinstance(v, (list, tuple)) and v and all(x is None or isinstance(x, (int, float)) for x in v):
        return "[" + ", ".join(md_cell(x) or "n/a" for x in v) + "]"
    return str(v)


def interval_text(ci, per_cluster=None, span=None, unit='speaker') -> str:
    """An interval cell: the 95% cluster-bootstrap interval, or (fewer than MIN_BOOTSTRAP_CLUSTERS clusters) the value of
    each cluster and their range, which is not a confidence interval."""
    if per_cluster:
        values = ", ".join(f"{k} {md_cell(v) or 'n/a'}" for k, v in per_cluster.items())
        return f"per {unit}: {values}; range {md_cell(span)}" if span else f"per {unit}: {values}"
    return bounds_text(ci)


def f1_interval(row: dict) -> str:
    return interval_text(row.get("f1_ci95"), row.get("f1_per_speaker"), row.get("f1_range"))


def md_table(headers: list[str], rows: list[list]) -> str:
    cell = md_cell
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    return "\n".join(out + ["| " + " | ".join(cell(v) for v in r) + " |" for r in rows])


def rate_row(label: str, regions: int, minutes: float) -> list:
    ub = None if regions else C.RULE_OF_THREE / minutes if minutes else None
    return [label, regions, round(minutes, 2), round(regions / minutes, 3) if minutes else None, None if ub is None else round(ub, 3)]


def regime_rate_row(label: str, reg: dict, regions: int, minutes: float) -> list:
    """A rate row, or "flags disabled" when the regime has no calibrated h (a disabled detector is not a clean null)."""
    return [label, "flags disabled", round(minutes, 2), None, None] if not flagged_dims(reg) else rate_row(label, regions, minutes)


def stored_pair(ds: Dataset, B: Recording, P: Recording, det: dict, regime: str) -> Run:
    """Memoise stored comparisons across evaluation sections, scoped to one Dataset and detector."""
    if not hasattr(ds, "_runs"):
        ds._runs = {}
    token = (id(B), id(P), det["config_sha256"], regime)
    if token not in ds._runs:
        ds._runs[token] = run_pair(B, P, det, regime)
    return ds._runs[token]


def clip_runs(ds: Dataset, det: dict, clips: list[dict]) -> list[tuple[dict, Run, dict]]:
    """(clip, run, labels) for stored clips against their baseline (R1 for baseline clips, R2 for reader clips); the clean
    recordings and the clips are analysed in one batch."""
    ds.load(entries=[ds.any_entry(c["baseline"]) for c in clips], clips=clips)
    Bs, Ps = ds.recs([ds.any_entry(c["baseline"]) for c in clips]), ds.clip_recs(clips)
    return [(c, stored_pair(ds, B, P, det, c["regime"]), ds.labels(c)) for c, B, P in zip(clips, Bs, Ps)]


def warm(ds: Dataset, splits: tuple[str, ...]) -> None:
    """One batch for every recording and stored clip the sections will want (they are memoised afterwards)."""
    entries = [b for b in ds.manifest["baselines"] if b["split"] in splits] + [r for r in ds.manifest["readers"] if not r.get("null_set")]
    entries += [ds.entry("baselines", r["paired_baseline"]) for r in ds.manifest["readers"] if r["role"] == "orator_reference"]
    clips = [c for c in ds.manifest["clips"] if c["kind"] in ("cross", "cross_botched") or c["split"] in splits]
    ds.load(entries=entries, clips=clips)


# ============================================================================================ nulls
def null_section(ds: Dataset, det: dict, splits: tuple[str, ...]) -> dict:
    """False flags per minute on nulls that were not fitted (a whole-clip flag counts as one), exposure beside each rate,
    rule-of-three bound where zero."""
    held = held_out(splits)
    rows, detail = [], {}
    r1, r2 = det["regimes"]["R1"], det["regimes"]["R2"]
    nulls = r1_nulls(ds, held)
    for name, gs in split_groups(held):
        sel = [n for n in nulls if n.split in gs]
        regs = [(n, null_flags(n, r1)) for n in sel]
        total, minutes = sum(len(f) for _, f in regs), sum(n.minutes for n in sel)
        rows.append(regime_rate_row(f"R1 {name}: identity + {C.PLACEBO_SEEDS} placebo seeds ({len(sel)} variants; {len({n.id.split('__')[0] for n in sel})} source recordings / readers)", r1, total, minutes))
        independent = {}
        for n in sel:
            reader = n.reader or n.id.split('__')[0]
            independent[reader] = max(independent.get(reader, 0.), n.minutes)
        rows[-1][4] = C.RULE_OF_THREE / sum(independent.values()) if not total and independent else None
        checked = {**r1, 'null': {}}
        null_check(checked, sel)
        detail[f"R1 {name}"] = {"regions": total, "minutes": round(minutes, 3),
                                "unique_source_recordings": len({n.id.split("__")[0] for n in sel}), "unique_readers": len({n.id.split("__")[0] for n in sel}),
                                "unique_variant_recordings": len(sel), "by_clip": dict((n.id, f) for n, f in regs),
                                'per_key': checked['null'], 'independent_recording_minutes': sum(independent.values())}
    cal, chk = reader_ids(ds, "reader_calibration"), reader_ids(ds, "reader_check")
    n2 = r2_nulls(ds, cal, chk)
    regs = [(n, null_flags(n, r2)) for n in n2]
    rows.append(regime_rate_row(f"R2 check-reader pairs, not fitted but seen during the detector redesign ({len(n2)} ordered pairs; {len(set(cal + chk))} recordings / readers)", r2, sum(len(f) for _, f in regs),
                                sum(n.minutes for n in n2)))
    rows[-1][4] = None
    reader_rows = [{"reader": p, "comparisons": sum(participant_of(n.id) == p for n in n2),
                    "minutes": sum(n.minutes for n in n2 if participant_of(n.id) == p),
                    "regions": sum(len(f) for n, f in regs if participant_of(n.id) == p),
                    "by_key": dict(Counter(k for n, f in regs if participant_of(n.id) == p for k in f))} for p in chk]
    detail["R2 check readers"] = {"unique_recordings": len(set(cal + chk)), "unique_readers": len(set(cal + chk)),
                             "disabled_keys": [k for k in KEYS if C.dim_of(k) in r2["enabled"] and r2["h"][k] is None], "reader_counts": reader_rows,
                             "by_pair": dict((n.id, f) for n, f in regs)}
    g = ds.entry("readers", "greenman_reagan")
    gB, gP = ds.recs([ds.entry("baselines", g["paired_baseline"]), g])
    gr = run_pair(gB, gP, det, "R2")
    rows.append(regime_rate_row("R2 orator-reference row: Greenman vs Reagan (2 recordings / readers; never fitted)", r2, gr.n_flags, gr.P.duration / 60))
    rows[-1][4] = None
    detail["orator_reference"] = {"regions": gr.flag_keys, "overall": gr.scored.overall}
    tab = md_table(["population", "false flags", "exposure (min)", "observed per comparison-minute", "rule of three (R1 unique recordings only; R2 dependent)"], rows)
    tab += "\n\nReader-level R2 null counts:\n\n" + md_table(["participant reader", "comparisons", "comparison-minutes", "flags", "by flag key"],
                        [[r["reader"], r["comparisons"], r["minutes"], r["regions"], r["by_key"]] for r in reader_rows])
    return {"rows": rows, "detail": detail, "table": tab}


def participant_of(pair_id: str) -> str:
    """The participant of an R2 pair id '<reference>><participant>'."""
    return pair_id.split(">")[1]


def null_flags(n, regime: dict) -> list[str]:
    """Flag keys fired on one null comparison, one per change (events.false_change_duplicates): local regions, then
    whole-clip flags."""
    regions, whole = decode(n.comp, regime, n.sentence), clip_flags(n.comp, regime)
    duplicated = {d['index'] for d in false_change_duplicates(n.comp, regions, whole)}
    return [key(r.dim, r.sign) for j, r in enumerate(regions) if j not in duplicated] + [clip_key(k, g) for k, g in whole.items()]


# ============================================================================================ headline
def duplicates(evs, group='all') -> int:
    """Same-change duplicate regions of the given per-clip evaluations: all of them, or those of the change of one flag key."""
    return sum(group == 'all' or d['change'] == group for ev in evs for d in ev['duplicates'])


def every_prediction(evs) -> dict:
    """The pre-registered accounting, which counts every region not matched by its own key as false: per region key
    the false regions, whole-clip flags, same-change duplicates and same-change detections (these are FN there)."""
    keys = Counter()
    for ev in evs:
        keys.update(f['group'] for f in ev['false'])
        keys.update(k + ' whole clip' for k in ev['false_clip'])
        keys.update(d['group'] for d in ev['duplicates'])
        keys.update(d['group'] for d in ev['same_change_detections'])
    return {'false_by_key': dict(sorted(keys.items())), 'same_change_detections': sum(len(ev['same_change_detections']) for ev in evs)}


F1_INTERVAL_HEADER = ('F1 interval (speaker bootstrap with >= 5 speakers: train, in-sample, 5 speakers, coverage not assured; '
                      'else per-speaker F1 and range, no interval)')
PRE_REGISTERED = 'pre-registered: every region not matched by its own key is false'
# The one-detection-per-change rule as events.truth_changes and events.false_change_duplicates apply it; the frozen registry
# scope (protocol.exemption_policy) states only the duplicate case and stays unchanged with its sha256.
COUNT_ONCE_RULE = ('One detection per change. A truth of a linked key (config.SAME_CHANGE: D9- measures the D1- change) is '
                   'detected by its own-key region (IoU >= 0.5) or its own-key whole-clip flag; when there is none, the '
                   'same-change region with the largest |z| within half a window (2 words) is the detection, without an IoU '
                   'test. Every other same-change region of that change is a duplicate, not a false region. A second '
                   'own-key region on the same edit that fails IoU is a false region.')


def pre_registered(row: dict) -> dict:
    """TP / FP / FN / F1 of a strict 'all' row under the pre-registered accounting (every region not matched by its own
    key is false): same-change detections become FN, and they and the duplicates are false regions."""
    every = row['every_prediction']
    detections = every['same_change_detections']
    tp, fn, fp = row['tp'] - detections, row['fn'] + detections, sum(every['false_by_key'].values())
    if fp != row['fp'] + row['same_change_duplicates'] + detections:
        raise ValueError(f"{row['split']} {row['levels']}: every_prediction does not add up to FP + duplicates + detections")
    return {'tp': tp, 'fp': fp, 'fn': fn, 'f1': f1(tp, fp, fn)['f1'], 'same_change_detections': detections,
            'false_by_key': every['false_by_key']}


def event_clusters(selected, strict=None, group='all'):
    clusters = defaultdict(list)
    for c, ev in selected:
        ev = strict[c['id']] if strict is not None else ev
        truth = [t for t in ev['truth'] if t['available'] and (group == 'all' or t['group'] == group)]
        tp = sum(bool(t['detected']) for t in truth)
        fp = sum(group == 'all' or f['group'] == group for f in ev['false'])
        fp += len(ev['false_clip']) if group in ('all', 'whole clip') else 0
        clusters[c['parent']].append((tp, fp, len(truth)-tp))
    return clusters


def _headline_section(ds: Dataset, det: dict, splits: tuple[str, ...], types=None) -> dict:
    """Chain A single-level clips (R1): event F1, onset / offset errors, detection versus magnitude, activation matrix, false
    regions on flawed clips. Per split (and val+test) and per speech with k-of-n counts; L2 + L3 headline, L1 sensitivity."""
    types = C.CORE8_TYPES if types is None else types
    runs = [(c, run, tier_labels(lab, types))
            for c, run, lab in clip_runs(ds, det, [c for c in ds.clips(kind="single") if c["split"] in splits])
            if any(f['type'] in types for f in lab['flaws'])]
    results = [(c, eval_clip(r, lab)) for c, r, lab in runs]
    strict = {c["id"]: eval_clip(r, lab, secondary_exempt=False) for c, r, lab in runs}
    dur = {c["id"]: r.P.duration for c, r, _ in runs}  # exposure = the participant clip's own minutes
    groups = split_groups(splits)
    out = {"per_speech": [], "by_split": [], "by_split_strict": [], "overlap": [], "clip_flags": [], "pause_localisation": [], "magnitude": [], "onset_offset": [], "activation": {}, "false_on_flawed": []}
    for lname, lv in LEVEL_GROUPS.items():
        for split, gs in groups:
            sel = [(c, e) for c, e in results if c["level"] in lv and c["split"] in gs]
            tally: dict[str, list[int]] = {}
            for _, e in sel:
                for t in e["truth"]:
                    if not t["available"]:
                        continue
                    g = tally.setdefault(t["group"], [0, 0, 0])
                    g[0] += t["detected"]
                    g[2] += not t["detected"]
                for f in e["false"]:
                    tally.setdefault(f["group"], [0, 0, 0])[1] += 1
            allg = [sum(v[i] for v in tally.values()) for i in range(3)]
            stally = {k: list(v) for k, v in tally.items()}
            for c, ev in sel:
                secondary = Counter(f["group"] for f in strict[c["id"]]["false"])
                secondary.subtract(f["group"] for f in ev["false"])
                for k, n in secondary.items():
                    stally.setdefault(k, [0, 0, 0])[1] += n
            whole = sum(len(e["false_clip"]) for c, e in sel)
            if whole:
                stally.setdefault("whole clip", [0, 0, 0])[1] += whole
            strict_sel = [strict[c["id"]] for c, _ in sel]
            for k, v in sorted(stally.items()):
                out["by_split_strict"].append({"levels": lname, "split": split, "group": k, "accounting": STRICT_ACCOUNTING,
                                               "same_change_duplicates": duplicates(strict_sel, k), **f1(*v, clusters=event_clusters(sel, strict, k))})
            out["by_split_strict"].append({"levels": lname, "split": split, "group": "all", "accounting": STRICT_ACCOUNTING,
                                           "same_change_duplicates": duplicates(strict_sel),
                                           'every_prediction': every_prediction(strict_sel),
                                           **f1(*(sum(v[i] for v in stally.values()) for i in range(3)), clusters=event_clusters(sel, strict))})
            nt = sum(t["available"] for _, e in sel for t in e["truth"])
            touched = sum(bool(t["touched"]) for _, e in sel for t in e["truth"] if t["available"])
            nf = sum(e["n_regions"] for _, e in sel)
            on = sum(e["flags_on_flaw"] for _, e in sel)
            out["overlap"].append({"levels": lname, "split": split, "touched": touched, "truths": nt,
                                   "flags_on_flaw": on, "flags": nf, "overlap_recall": touched / nt if nt else None,
                                   "flag_precision": on / nf if nf else None, "overlap_recall_ci95": wilson(touched,nt), "flag_precision_ci95": wilson(on,nf)})
            for g, v in sorted(tally.items()):
                out["by_split"].append({"levels": lname, "split": split, "group": g, "accounting": "secondary firings exempt",
                                        "same_change_duplicates": duplicates([e for _, e in sel], g), **f1(*v, clusters=event_clusters(sel, group=g))})
            out["by_split"].append({"levels": lname, "split": split, "group": "all", "accounting": "secondary firings exempt",
                                    "same_change_duplicates": duplicates([e for _, e in sel]), **f1(*allg, clusters=event_clusters(sel))})
            out["false_on_flawed"].append({"levels": lname, "split": split, "false_regions": allg[1], "minutes": round(sum(dur[c["id"]] for c, _ in sel) / 60, 2),
                                           "secondary_not_counted": sum(e["secondary"] for _, e in sel),
                                           "same_change_duplicates_not_counted": sum(e["duplicate"] for _, e in sel)})
    out['true_positive_detail'] = [{'clip': c['id'], 'split': c['split'], **t} for c,e in results for t in e['truth'] if t['detected']]
    out["missed_detail"] = [{"clip": c["id"], "split": c["split"], **t} for c, e in results for t in e["truth"] if t["available"] and not t["detected"]]
    out["false_detail"] = [{"clip": c["id"], "split": c["split"], "level": c["level"], **f} for c, _ in results for f in strict[c["id"]]["false"]]
    for c, e in results:  # per speech k-of-n at L2+L3
        if c["level"] in C.HEADLINE_LEVELS:
            k = sum(bool(t["detected"]) for t in e["truth"] if t["available"])
            out["per_speech"].append({"speech": c["parent"], "split": c["split"], "clip": c["id"], "level": c["level"], "detected": k, "of": sum(t["available"] for t in e["truth"]),
                                      "false_regions": len(e["false"]), "strict_false_regions": len(strict[c["id"]]["false"]),
                                      "same_change_duplicates": strict[c["id"]]["duplicate"], "detected_ci95": wilson(k, sum(t["available"] for t in e["truth"]))})
    for c, e in results:
        for t in e["truth"]:
            out["magnitude"].append({"split": c["split"], "speech": c["parent"], "type": t["type"], "level": t["level"], "detected": t["detected"], "status": t["status"], "realised": t["realised"]})
            if "pause_onset_ms" in t and c["level"] in C.HEADLINE_LEVELS:
                out["pause_localisation"].append({"split": c["split"], "clip": c["id"], **t})
            if "onset_ms" in t and c["level"] in C.HEADLINE_LEVELS:
                out["onset_offset"].append({"split": c["split"], "type": t["type"], "speech": c["parent"], "clip": c["id"], "onset_ms": t["onset_ms"], "offset_ms": t["offset_ms"], "edge_error_above_tolerance": t["edge_error_above_tolerance"], "grounding_status": t["grounding_status"]})
    # activation matrix per split group (never train with held-out): injected dimension x fired dimension (fired regions
    # within two words of an injected edit), L2 + L3
    for gname, gs in groups:
        mat: dict[str, dict[str, int]] = {}
        for c, run, lab in runs:
            if c["level"] not in C.HEADLINE_LEVELS or c["split"] not in gs:
                continue
            tr = truths(lab)
            for r in run.regions:
                hit = [t for t in tr if near(r, t)]  # by word index, not time: a removed pause has no duration to overlap
                for t in hit or [{"dim": "none"}]:
                    mat.setdefault(t["dim"], {}).setdefault(r.dim, 0)
                    mat[t["dim"]][r.dim] += 1
        out["activation"][gname] = mat
    # tables
    t_rows = [[r["accounting"], r["levels"], r["split"], r["group"], r["tp"], r["fp"], r["same_change_duplicates"], r["fn"], r["precision"], r["recall"], r["f1"], f1_interval(r), r["precision_ci95"], r["recall_ci95"]]
              for entries in (out["by_split_strict"], out["by_split"]) for r in entries]
    out["table_f1"] = md_table(["accounting", "levels", "split", "dimension/sign", "TP", "FP", "same-change duplicates (not FP)", "FN", "precision", "recall", "F1", F1_INTERVAL_HEADER, "precision 95% Wilson", "recall 95% Wilson"], t_rows)
    out["table_overlap"] = md_table(["levels", "split", "flaws touched", "flaws", "flags on flaw", "all local flags", "overlap recall", "flag precision", "recall 95% Wilson", "precision 95% Wilson"],
                                    [[r["levels"], r["split"], r["touched"], r["truths"], r["flags_on_flaw"], r["flags"], r["overlap_recall"], r["flag_precision"], r["overlap_recall_ci95"], r["flag_precision_ci95"]] for r in out["overlap"]])
    for split, gs in groups:
        clips = [c["id"] for c, run, _ in runs if c["split"] in gs and run.clip]
        out["clip_flags"].append({"split": split, "count": len(clips), "clips": clips})
    out["table_clip"] = md_table(["split", "whole-clip flags on flawed clips", "clips"], [[r["split"], r["count"], ", ".join(r["clips"]) or "none"] for r in out["clip_flags"]])
    out["table_pause"] = md_table(["split", "clip", "type", "pause onset error (ms)", "pause offset error (ms)"],
                                  [[r["split"], r["clip"], r["type"], r["pause_onset_ms"], r["pause_offset_ms"]] for r in out["pause_localisation"]])
    out["table_per_speech"] = md_table(["speech", "split", "clip", "level", "detected k", "of n", f"false regions ({STRICT_ACCOUNTING})", "same-change duplicates", "95% Wilson"],
                                       [[r["speech"], r["split"], r["clip"], r["level"], r["detected"], r["of"], r["strict_false_regions"], r["same_change_duplicates"], r["detected_ci95"]] for r in out["per_speech"]])
    on_rows = []
    for gname, gs in groups:
        on: dict[str, list] = {}
        for r in out["onset_offset"]:
            if r["split"] in gs:
                on.setdefault(r["type"], []).append(r)
        on_rows += [[gname, t, len(v), float(np.median([abs(x["onset_ms"]) for x in v])), float(np.percentile([abs(x["onset_ms"]) for x in v], 90)),
                     float(np.median([abs(x["offset_ms"]) for x in v])), float(np.percentile([abs(x["offset_ms"]) for x in v], 90))]
                    for t, v in sorted(on.items())]
    grounding = []
    for gname, gs in groups:
        for typ in types:
            rows = [r for r in out['onset_offset'] if r['split'] in gs and r['type'] == typ]
            if not rows:
                continue
            clusters = defaultdict(list)
            for r in rows:
                clusters[r['speech']].append(r)
            row = {'split': gname, 'type': typ, 'matched': len(rows), 'within_edge_tolerance_ci95': wilson(sum(not r['edge_error_above_tolerance'] for r in rows),len(rows)),
                   'coarse_edge_tp': sum(r['edge_error_above_tolerance'] for r in rows),
                   'both_edges_within_tolerance': sum(not r['edge_error_above_tolerance'] for r in rows)}
            for edge in ('onset', 'offset'):
                for quantile in (50,90):
                    field = f'{edge}_p{quantile}_ms'
                    fn = lambda v, e=edge, q=quantile: float(np.percentile([abs(r[e+'_ms']) for r in v], q))
                    row[field] = fn(rows)
                    summary = cluster_summary(clusters, fn)
                    row[field+'_ci95'], row[field+'_per_speaker'], row[field+'_range'] = summary['ci95'], summary['per_cluster'], summary['range']
                    row['ci_method'] = summary['method']
            grounding.append(row)
    out['grounding'] = grounding
    out["table_onset"] = md_table(["split", "type", "n matched", "onset median (ms)", "onset P90 (ms)", "offset median (ms)", "offset P90 (ms)"], on_rows)
    out['table_onset'] += '\n\nGrounding of IoU true positives; an edge outside EVENT_TOL_S remains a coarse-edge TP:\n\n' + md_table(
        ['split','type','matched','coarse-edge TP','both edges within 0.20 s','onset median (ms); interval','onset P90; interval','offset median; interval','offset P90; interval'],
        [[r['split'],r['type'],r['matched'],r['coarse_edge_tp'],r['both_edges_within_tolerance'],
          *[f"{md_cell(r[f])}; {interval_text(r[f+'_ci95'], r[f+'_per_speaker'], r[f+'_range'])}" for f in ('onset_p50_ms','onset_p90_ms','offset_p50_ms','offset_p90_ms')]] for r in grounding])
    mag = []
    for typ in types:
        for lv in C.LEVELS:
            cells = {}
            for split in ALL_SPLITS:
                sel = [m for m in out["magnitude"] if m["type"] == typ and m["level"] == lv and m["split"] == split]
                cells[split] = (proportion(sum(bool(m['detected']) for m in sel), len(sel)) if not any(m['status'] == 'no detector' for m in sel) else f"no detector ({len(sel)})") if sel else ""
            mag.append([typ, lv, C.LEVEL_PARAM[typ][lv - 1], cells["train"], cells["val"], cells["test"], EXPECTED["R1"][lv] if C.FLAW_DIM[typ] in C.DIMS else "no detector"])
    out["table_magnitude"] = md_table(["type", "level", "magnitude", "train k/n", "val k/n", "test k/n", "expected (R1)"], mag)
    out["table_activation"] = "\n\n".join(f"Split {g}:\n\n" + md_table(["injected \\ fired"] + list(C.DIMS), [[k] + [v.get(d, 0) for d in C.DIMS] for k, v in sorted(m.items())])
                                          for g, m in out["activation"].items())
    return out


def ppv(sensitivity, false_positive_rate, base_rate=C.STUTTER_BASE_RATE):
    if sensitivity is None or false_positive_rate is None:
        return None
    numerator = sensitivity * base_rate
    denominator = numerator + false_positive_rate * (1 - base_rate)
    return numerator / denominator if denominator else None


def promotion_section(ds, det, splits):
    """Select-set reporting only; promotion decisions belong to calibration."""
    reg = det['regimes']['R2']
    select = grouped_nulls(ds, 'select') if ds.manifest.get('r2_pool') else []
    report = {**reg, 'null': {}}
    null_check(report, select)
    syllables = sum(sum(np.asarray(n.comp.syllables)[np.isfinite(n.comp.dims['D7'].x)]) for n in select)
    flags = sum(r.dim == 'D7' for n in select for r in decode(n.comp, reg, n.sentence))
    false_rate = flags / syllables if syllables and 'D7' in reg['enabled'] and threshold(reg, 'D7', 1) is not None else None
    real = det.get('report', {}).get('real_validation', {}).get('D7+', {})
    sensitivity = real.get('syllable_sensitivity')
    rows = det.get('report', {}).get('promotion', {}).get('rows', [])
    ppv_report = {'base_rate': C.STUTTER_BASE_RATE, 'base_rate_unit': 'stuttered syllables',
                  'sensitivity': sensitivity, 'false_flags': flags, 'measured_syllables': int(syllables),
                  'false_flags_per_syllable': false_rate, 'ppv': ppv(sensitivity, false_rate),
                  'scope': 'expected PPV using false regions per measured syllable as an FPR proxy; repeated reader comparisons are dependent',
                  'reason': None if sensitivity is not None and false_rate is not None else 'requires an enabled D7 key and Real syllable sensitivity'}
    table = md_table(['candidate key', 'status', 'rate', 'bootstrap upper95', 'rule of three', 'L3 recall', 'found', 'away edits'],
                     [[r.get(k) for k in ('key', 'status', 'rate', 'bootstrap_upper95', 'rule_of_three', 'recall', 'found', 'away_edits')] for r in rows])
    whole = [r['whole_clip'] for r in rows if r.get('whole_clip')]
    table += '\n\nWhole-clip candidate diagnostics:\n\n' + md_table(
        ['key', 'rate', 'bootstrap upper95', 'rule of three', 'L3 recall', 'found', 'away edits'],
        [[r.get(k) for k in ('key', 'rate', 'bootstrap_upper95', 'rule_of_three', 'recall', 'found', 'away_edits')] for r in whole])
    table += '\n\nD7 PPV at 0.21% stuttered syllables:\n\n' + md_table(['Real sensitivity', 'false regions / measured syllable (proxy)', 'expected PPV', 'scope'],
                                        [[sensitivity, false_rate, ppv_report['ppv'], ppv_report['reason'] or ppv_report['scope']]])
    null = report['null']
    modes = det.get('report', {}).get('R2_modes', {'single': {'fit': reg.get('null', {}), 'select': null}})
    table += '\n\nFit and select null reports of both R2 modes:\n\n' + null_tables(
        [(mode, phase, record.get(phase, {})) for mode, record in modes.items() for phase in ('fit', 'select')])
    table += '\n\nSources retain equal weights by owner decision; texts are weighted by comparison-minutes within a source. These rates describe that mixture, not a deployment population. In v11 Gettysburg had ten fit readers and 4.8% of fit exposure but 25% of weight; it supplied 72% of the weighted D2- rate. The Accent-driven select gap is associated with L1/lab-seen composition; those effects are confounded. Select results were inspected during redesign; the estimator was the owner decision. The lockbox rates are measured only by the final evaluation (lockbox section).'
    table += '\n\n' + null['budget_statement'] + '. Weighted total: ' + str(null['total_local']['rate']) + '/min; pooled total: ' + str(null['total_local']['pooled_rate']) + '/min.'
    return {'set': 'select', 'rows': rows, 'null': report['null'], 'ppv': ppv_report, 'table': table}


def null_tables(reports: list[tuple[str, str, dict]]) -> str:
    """Totals, per-key, per-source and per-first-language false rates of R2 null reports [(mode, set, null report)]; the
    select and the lockbox reports print these same tables."""
    totals = md_table(['mode', 'set', 'weighted total/min', 'pooled total/min', 'weighted upper95', 'budget status', 'budget statement', 'scope'],
                      [[mode, phase, null.get('total_local', {}).get('rate'), null.get('total_local', {}).get('pooled_rate'),
                        null.get('total_local', {}).get('bootstrap_upper95'), null.get('total_local', {}).get('budget_status'),
                        null.get('budget_statement'), null.get('scope', 'all fit sources')] for mode, phase, null in reports])
    keys = md_table(['mode', 'set', 'key', 'share/min', 'weighted/min', 'pooled/min', 'weighted upper95', 'pooled upper95', 'point within share', 'upper95 within share', 'valid units'],
                    [[mode, phase, k, *[r.get(f) for f in ('budget_share', 'rate', 'pooled_rate', 'bootstrap_upper95', 'pooled_bootstrap_upper95', 'point_within_share', 'upper95_within_share', 'valid_units')]]
                     for mode, phase, null in reports for k, r in null.get('local_by_key', {}).items()])
    def rows_of(null):
        return [*null.get('local_by_key', {}).items(), ('total', null.get('total_local', {}))]
    sources = md_table(['mode', 'set', 'key', 'source', 'rate/min (texts by comparison-minutes)', 'pooled/min', 'flags', 'comparison-minutes'],
                       [[mode, phase, k, source, r['rate'], r['pooled_rate'], r['flags'], r['exposure']]
                        for mode, phase, null in reports for k, row in rows_of(null) for source, r in row.get('by_source', {}).items()])
    languages = md_table(['mode', 'set', 'key', 'L1', 'readers', 'flags', 'comparison-minutes', 'rate/min', '95% CI (reader clusters; none for zero events)'],
                         [[mode, phase, k, lang, r['readers'], r['flags'], r['comparison_minutes'], r['rate'], r['ci95']]
                          for mode, phase, null in reports for k, row in rows_of(null) for lang, r in row.get('by_L1', {}).items()])
    return (totals + '\n\nPer key, beside the per-key share:\n\n' + keys + '\n\nPer source:\n\n' + sources +
            '\n\nPer participant first language (Accent Archive readers):\n\n' + languages)


def lockbox_section(ds, det, splits) -> dict:
    """Final evaluation: R2 false regions per comparison-minute of both modes on the lockbox readers
    (calibrate.lockbox_null_report, final task only), with the select report's tables and stated limits."""
    report = lockbox_null_report(ds, det, final=True)
    if 'modes' not in report:
        return {**report, 'limits': [], 'table': report['status']}
    report['limits'] = [v for mode, null in report['modes'].items() for v in budget_limits(f'{mode} lockbox', null)]
    report['table'] = (f"Lockbox readers by source: {report['readers_by_source']}; comparisons: {report['comparisons']}; "
                       f"{len(report['excluded'])} lockbox readings excluded when located. Measured once, after calibration, with the "
                       "select estimator (equal sources over the covered sources; comparison-minutes within a source).\n\n" +
                       null_tables([(mode, 'lockbox', null) for mode, null in report['modes'].items()]) +
                       '\n\nStated limits:\n\n' + ('\n'.join('- ' + v for v in report['limits']) or '- none'))
    return report


def headline_section(ds, det, splits):
    groups = {name: _headline_section(ds, det, splits, types=types) for name, types in tiers(det.get('report', {}).get('real_validation')).items()}
    core = groups['core8']
    magnitude = [{**m, 'tier': name, 'validation': 'unvalidated' if name == 'synthetic_only' else 'synthetic recovery'}
                 for name, group in groups.items() for m in group['magnitude']]
    pending = Counter((m['split'], m['type'], m['level']) for m in magnitude if m['status'] == 'no detector')
    out = {**core, 'claim': 'recovery of realised synthetic edits; train is in-sample; val is a reused two-speaker development estimate; all baselines are US political speeches; earlier test speakers were used before redesign; no perceptual listening validation', 'groups': groups,
           'magnitude': magnitude, 'exemptions': exemption_policy(),
           'no_detector': [dict(split=sp,type=t,level=lv,count=n,status='no detector',validation='unvalidated') for (sp,t,lv),n in sorted(pending.items())]}
    out['table_f1'] = f1_table(groups)
    for name in ('table_overlap', 'table_per_speech', 'table_clip', 'table_pause', 'table_onset', 'table_magnitude', 'table_activation'):
        out[name] = '\n\n'.join(tier + (' (unvalidated)' if tier == 'synthetic_only' else '') + ':\n\n' + group[name] for tier, group in groups.items())
    shortfalls = []
    for c, _, lab in clip_runs(ds, det, [c for c in ds.clips(kind='single') if c['split'] in splits]):
        for t in truths(lab, excluded=True):
            shortfalls.append({'clip': c['id'], 'split': c['split'], **t})
    counts_by = Counter((r['split'], r['type'], r['level']) for r in shortfalls)
    out['realisation_shortfalls'] = {'events': shortfalls, 'counts': [dict(split=sp, type=t, level=lv, count=n) for (sp,t,lv), n in sorted(counts_by.items())]}
    out['table_magnitude'] += '\n\nExcluded shortfall stratum (not truth or h-selection positives):\n\n' + md_table(
        ['split', 'type', 'level', 'excluded events'], [[sp,t,lv,n] for (sp,t,lv),n in sorted(counts_by.items())])
    out['table_magnitude'] += '\n\nDetection by realised magnitude (recipe units):\n\n' + md_table(
        ['tier', 'split', 'speech', 'type', 'nominal level', 'realised value', 'unit', 'detected'],
        [[m['tier'],m['split'],m['speech'],m['type'],m['level'],m['realised'].get('value'),m['realised'].get('unit'),m['detected']] for m in magnitude])
    matching, counts = [], []
    for c, run, lab in clip_runs(ds, det, [c for c in ds.clips(kind='single') if c['split'] in splits]):
        ev = eval_clip(run, lab)
        matching += [{'clip': c['id'], 'split': c['split'], 'type': t['type'], 'level': t['level'],
                      'both_edges_020s': t['detected'], 'index_or_overlap': t['detected_index_or_overlap']}
                     for t in ev['truth'] if C.FLAW_DIM[t['type']] in ('D7', 'D8') and t['event'] != 'clip']
        counts.append({'clip': c['id'], 'label_count': ev['label_count'], 'event_count': ev['event_count'], **ev['word_by_word']})
    out['matching'] = matching
    out['truth_counts'] = counts
    out['table_matching'] = md_table(['clip', 'split', 'type', 'level', 'both edges +/-0.20 s', 'index or overlap'],
                                    [[r[k] for k in ('clip', 'split', 'type', 'level', 'both_edges_020s', 'index_or_overlap')] for r in matching])
    out['table_truth_counts'] = md_table(['clip', 'labels', 'event truths', 'word-by-word groups', 'eligible clips', 'detected clips', 'inserted silence truths'],
                                       [[r[k] for k in ('clip', 'label_count', 'event_count', 'label_groups', 'eligible_clips', 'detected_clips', 'boundary_truths')] for r in counts])
    out['table_truth_counts'] += '\n\nWORD_BY_WORD group recovery counts each eligible clip once (any labelled boundary detected); boundary localisation is reported separately. This synthetic-only family does not select h.'
    out['recovered_types'] = sorted({m['type'] for m in magnitude if m['detected']})
    out['attempted_types'] = sorted({m['type'] for m in magnitude})
    out['negative_families'] = sorted(set(out['attempted_types']) - set(out['recovered_types']))
    labels = det['regimes']['R1'].get('pattern_labels', {})
    out['recovered_types_scope'] = 'dimension and direction match of a region; not the product pattern label'
    out['recovered_label_off'] = [t for t in out['recovered_types'] if C.PATTERN_GATES.get(t) and not labels.get(C.PATTERN_GATES[t], False)]
    out['table_f1'] += ('\n\nRecipe families recovered by dimension match (not by product pattern label): ' + ', '.join(out['recovered_types']) +
                        '. Of these, the product pattern label is switched off for: ' + (', '.join(out['recovered_label_off']) or 'none') +
                        '. Attempted families with no recovered eligible events: ' + ', '.join(out['negative_families']) + '. Lab-passed status describes the lab contrast, not product recall.')
    out['bootstrap_modes_val'] = []
    fitted = det['regimes']['R1']
    joint = sorted(fitted.get('selection_bootstrap', {}).get('joint_h_counts', []),key=lambda r:-r['draws'])[:2]
    val_clips = [c for c in ds.clips(kind='single') if c['split'] == 'val' and any(t in (*C.CORE8_TYPES, 'NATURAL_RUSH') for t in c.get('types', []))]
    for mode in joint:
        trial_reg = {**fitted, 'h': {**{k: mode['h'] if C.dim_of(k) in fitted['enabled'] else None for k in fitted['h']}, 'D9-': mode['natural_rush_h']}}
        clusters = defaultdict(list)
        found,total = Counter(),Counter()
        evs = []
        for c,run,lab in clip_runs(ds,det,val_clips):
            changed = dataclasses.replace(run,regions=decode(run.comp,trial_reg,run.B.tr.sentence))
            ev = eval_clip(changed,lab,secondary_exempt=False)
            evs.append(ev)
            truth = [t for t in ev['truth'] if t['available']]
            tp = sum(bool(t['detected']) for t in truth)
            clusters[c['parent']].append((tp,len(ev['false'])+len(ev['false_clip']),len(truth)-tp))
            for t in truth:
                found[t['type']] += bool(t['detected'])
                total[t['type']] += 1
        sums = [sum(v[i] for rows in clusters.values() for v in rows) for i in range(3)]
        out['bootstrap_modes_val'].append({**mode, **f1(*sums,clusters=clusters), 'accounting': STRICT_ACCOUNTING,
                                           'same_change_duplicates': duplicates(evs), 'recall_by_type': {t: proportion(found[t],n) for t,n in total.items()}})
    out['table_f1'] += '\n\nDevelopment val at the two most frequent joint bootstrap thresholds (all levels; ' + STRICT_ACCOUNTING + '):\n\n' + md_table(
        ['h','speech-tempo h','bootstrap draws','val F1',F1_INTERVAL_HEADER,'same-change duplicates','recall by type'],
        [[r['h'],r['natural_rush_h'],r['draws'],r['f1'],f1_interval(r),r['same_change_duplicates'],r['recall_by_type']] for r in out['bootstrap_modes_val']])
    out['selected_h'] = fitted['h']
    out['dev_v9_change'] = dev_v9_change(out)
    out['table_f1'] += '\n\n' + out['dev_v9_change']['table']
    return out


def f1_table(groups: dict) -> str:
    """The headline F1 table: per tier, split and levels, the pre-registered accounting first, then the count-once row."""
    rows = []
    for name, group in groups.items():
        for field in ('by_split_strict', 'by_split'):
            for r in group[field]:
                if r['group'] != 'all':
                    continue
                validation = 'unvalidated' if name == 'synthetic_only' else 'synthetic recovery'
                if 'every_prediction' in r:
                    pre = pre_registered(r)
                    rows.append([name, validation, r['split'], r['levels'], PRE_REGISTERED, pre['tp'], pre['fp'], 0, pre['fn'], pre['f1'], 'n/a'])
                rows.append([name, validation, r['split'], r['levels'], r['accounting'] + (' (introduced after the plan)' if field == 'by_split_strict' else ''),
                             *[r[k] for k in ('tp', 'fp', 'same_change_duplicates', 'fn', 'f1')], f1_interval(r)])
    return md_table(['tier', 'validation', 'split', 'levels', 'accounting', 'TP', 'FP', 'same-change duplicates (not FP)', 'FN', 'F1', F1_INTERVAL_HEADER], rows)


def shortfall_section(ds, det, splits):
    rows = []
    for c in ds.manifest['clips']:
        if c['split'] not in splits and not (c['kind'] in ('cross', 'cross_botched', 'extra_botched') and c['split'] in ('calibration', 'check')):
            continue
        if c.get('missing'):
            continue
        for t in truths(ds.labels(c), excluded=True):
            rows.append({'clip': c['id'], 'regime': c['regime'], 'split': c['split'], **t})
    counts = Counter((r['regime'],r['split'],r['type'],r['level']) for r in rows)
    return {'events': rows, 'excluded_events': len(rows), 'counts': [dict(regime=reg,split=sp,type=t,level=lv,count=n) for (reg,sp,t,lv),n in sorted(counts.items())],
            'table': 'Excluded realisation shortfalls are not truth or h-selection positives. Non-monotone ladders are excluded at every affected rung.\n\n' +
                     md_table(['regime','split','type','level','excluded events'], [[reg,sp,t,lv,n] for (reg,sp,t,lv),n in sorted(counts.items())])}


def dev_v9_change(headline):
    """Strict core8 against dev_v9 under v9's accounting (every region not matched by its own key is false), on the flag
    keys v9 had; the current one-detection-per-change counts stand beside it. The difference is not a change in false
    regions caused by the detector alone: thresholds, keys and accounting changed together."""
    path = Path(__file__).with_name('dev_v9_reference.json')
    reference = json.loads(path.read_text())
    previous = reference['headline']
    v9_dims = {r['group'][:2] for r in previous['by_split_strict'] if r['group'] != 'all'}
    rows = []
    for r in headline['groups']['core8']['by_split_strict']:
        if r['group'] != 'all':
            continue
        old = next((x for x in previous['by_split_strict'] if x['split'] == r['split'] and x['levels'] == r['levels'] and x['group'] == 'all'), None)
        if old is None:
            continue
        every = r.get('every_prediction', {'false_by_key': {}, 'same_change_detections': 0})
        on_v9_keys = sum(n for k, n in every['false_by_key'].items() if k[:2] in v9_dims)
        rows.append({'split': r['split'], 'levels': r['levels'], 'v9_f1': old['f1'], 'current_f1': r['f1'], 'current_f1_interval': f1_interval(r),
                     'v9_fp': old['fp'], 'current_fp': r['fp'], 'current_same_change_duplicates': r['same_change_duplicates'],
                     'current_fp_v9_accounting': sum(every['false_by_key'].values()),
                     'current_fp_v9_accounting_v9_keys': on_v9_keys,
                     'v9_keys_fp_change_v9_accounting': on_v9_keys - old['fp'],
                     'current_tp_v9_accounting': r['tp'] - every['same_change_detections']})
    keys = ', '.join(sorted(v9_dims))
    return {'available': True, 'source': reference['source'], 'artifact_sha256': reference['sha256'], 'rows': rows, 'v9_dims': sorted(v9_dims),
            'verified_v9_to_v10': {'train': {'FP_change':31, 'D7':21, 'non_D7':10}, 'val': {'FP_change':17, 'D7':11, 'non_D7':6}},
            'scope': 'v9 accounting on v9 keys against v9; thresholds, keys and accounting changed together, so no change is attributed to h alone',
            'table': 'Change against dev_v9 (Oct 2), strict core8 L1 and L2+L3. v9 counted every region not matched by its own key as '
                     f'false; the current headline counts one detection per change ({STRICT_ACCOUNTING}). To compare like with like, '
                     f'the current FP are also given under the v9 accounting and on the keys v9 had ({keys}); the current FP alone is '
                     'a different accounting and is not a change in false regions:\n\n' + md_table(
                ['split','levels','v9 F1','current F1','current F1 interval','v9 FP','current FP (one per change)','current same-change duplicates',
                 'current FP, v9 accounting (all keys)','current FP, v9 accounting, v9 keys','FP change, v9 accounting, v9 keys','current TP, v9 accounting'],
                [[r[k] for k in ('split','levels','v9_f1','current_f1','current_f1_interval','v9_fp','current_fp','current_same_change_duplicates',
                                 'current_fp_v9_accounting','current_fp_v9_accounting_v9_keys','v9_keys_fp_change_v9_accounting','current_tp_v9_accounting')] for r in rows]) +
                f"\n\nCurrent selected h by key: {headline.get('selected_h', {})}; historical v9 common h=1.70. " +
                'The R1 h objective uses only L2+L3 training clips, so the L1 rows are measured at an h that was not chosen for L1. ' +
                'Verified v9-to-v10 FP decomposition: train +31 = D7 +21 and non-D7 +10; val +17 = D7 +11 and non-D7 +6. The threshold grid adds 11 training FP, but is a different metric.'}


# ============================================================================================ cross-speaker
def cross_matches(clean, edited, truth, reg):
    """New/worsened local detections and whole-clip detections; shared by the cross and rung reports."""
    regions = new_worsened(clean, edited, reg)
    matches = set(match(truth, edited.with_regions(regions)))
    clips = {dim for dim, g in edited.clip.items() if dim not in clean.clip or
             abs(g) > abs(clean.clip[dim]) + 1e-9}
    matches.update(i for i, t in enumerate(truth) if t['event'] == 'clip' and t['dim'] in clips)
    return regions, matches, clips


def edit_direction(run0: Run, run1: Run, t: dict) -> dict:
    """Classify an injection from the labelled word/boundary units on both recordings."""
    if t["dim"] not in run0.comp.dims:
        return {"type": t["type"], "dimension": t["dim"], "words": t["words"], "x_clean": None,
                "x_edited": None, "direction": "no detector"}
    w0, w1 = t["words"]
    if t.get('event') == 'clip':
        a, b = run0.comp.dims[t['dim']].g, run1.comp.dims[t['dim']].g
        direction = 'unmeasurable' if not np.isfinite(a + b) else 'away from the reference' if abs(b) > abs(a) else 'toward the reference (repair control)'
        return {'type': t['type'], 'dimension': t['dim'], 'words': t['words'], 'x_clean': float(a), 'x_edited': float(b), 'direction': direction}
    end = w0 + 1 if C.is_event(t["dim"]) else w1 + 1
    x0 = run0.comp.dims[t["dim"]].x[w0:end]
    x1 = run1.comp.dims[t["dim"]].x[w0:end]
    # A missing D2 delta at a non-pause boundary is a measured zero, not a missing word start.
    if t["dim"] == "D2":
        x0 = run0.P.sil_raw[w0:end] - run0.B.sil_raw[w0:end]
        x1 = run1.P.sil_raw[w0:end] - run1.B.sil_raw[w0:end]
    ok = np.isfinite(x0) & np.isfinite(x1)
    a, b = (float(np.median(x0[ok])), float(np.median(x1[ok]))) if ok.any() else (None, None)
    direction = ("unmeasurable" if a is None else "away from the reference" if abs(b) > abs(a) else "toward the reference (repair control)")
    return {"type": t["type"], "dimension": t["dim"], "words": t["words"], "x_clean": a, "x_edited": b, "direction": direction}


def new_worsened(run0: Run, run1: Run, reg: dict) -> list[Region]:
    """New or larger signed deviations, compared by shared word indices."""
    old = decode(run0.comp, reg, run0.B.tr.sentence)
    out = []
    for r in decode(run1.comp, reg, run1.B.tr.sentence):
        prior = [q for q in old if overlaps(r, q)]
        if not prior or abs(r.z) > max(abs(q.z) for q in prior) + 1e-9:
            out.append(r)
    return out


def consensus_of(ds: Dataset, parent: str, refs: list[str]):
    """(reference ids, median-of-CONSENSUS_K reference) of a participant: the references in seeded order, the first
    CONSENSUS_K of them; None with fewer. Memoised on the dataset."""
    from .reference import consensus_reference
    from .r2pool import digest
    refs = sorted(refs, key=lambda b: digest([C.SEED, parent, b]))
    if len(refs) < C.CONSENSUS_K:
        return None
    if not hasattr(ds, '_consensus_refs'):
        ds._consensus_refs = {}
    token = tuple(refs[:C.CONSENSUS_K])
    if token not in ds._consensus_refs:
        ds._consensus_refs[token] = consensus_reference([ds.rec(ds.any_entry(b)) for b in token])
    return token, ds._consensus_refs[token]


def cross_pairs(ds: Dataset, det: dict, clips: list[dict], consensus=False) -> list[tuple[dict, str, Run, Run, dict]]:
    """(clip, reference id, edited run, unedited run, labels) under R2: a check reader's clip against every calibration reader,
    any other clip against its stored reference."""
    cal = reader_ids(ds, "reader_calibration")
    ds.load(entries=[ds.parent_entry(c) for c in clips] + [ds.any_entry(c["baseline"]) for c in clips] + [ds.entry("readers", i) for i in cal], clips=clips)
    out = []
    for c, P1, P0 in zip(clips, ds.clip_recs(clips), ds.recs([ds.parent_entry(c) for c in clips])):
        refs = [i for i in cal if i != c['parent']] if c['split'] in ('check', 'calibration') else [c['baseline']]
        if consensus:
            made = consensus_of(ds, c['parent'], refs)
            if made is None:
                continue
            token, B = made
            out.append((c, ','.join(token), stored_pair(ds, B, P1, det, 'R2'), stored_pair(ds, B, P0, det, 'R2'), ds.labels(c)))
        else:
            for b in refs:
                B = ds.rec(ds.any_entry(b))
                out.append((c, b, stored_pair(ds, B, P1, det, 'R2'), stored_pair(ds, B, P0, det, 'R2'), ds.labels(c)))
    return out


def _cross_section(ds: Dataset, det: dict, splits: tuple[str, ...], consensus=False) -> dict:
    """R2 sensitivity uses away-edits as denominator; toward-edits are separate repair controls. The check readers' clips are
    compared with every calibration reader as the reference."""
    rows, summary, kept, detail = [], {}, [], []
    for c, ref, run1, run0, lab in cross_pairs(ds, det, ds.clips(kind="cross"), consensus=consensus):
        kept.append((c, run1, run0, lab))
        tr = truths(lab)
        classified = [edit_direction(run0, run1, t) for t in tr]
        nw, m, clips = cross_matches(run0, run1, tr, det["regimes"]["R2"])
        new = sum(not any(overlaps(r, q) for q in run0.regions) for r in nw)
        worse, pre = len(nw) - new, len(run1.regions) - len(nw)
        away = [i for i, d in enumerate(classified) if d["direction"] == "away from the reference"]
        controls = [i for i, d in enumerate(classified) if d["direction"].startswith("toward")]
        unmeasurable = len(tr) - len(away) - len(controls)
        diffs = differences(run1.comp, run1.B, run1.P, det["regimes"]["R2"], run1.regions)
        ranks = [listed_rank(diffs, t) for t in tr]  # place of the edit in the unscored 'largest differences' list, None when absent
        visible = [(t['dim'] in clips if t['event'] == 'clip' else any(r.dim == t["dim"] and t["sign"] in (0, r.sign) and
                       (t["words"][0] in r.units if C.is_event(t["dim"]) else
                        any(t["words"][0] <= u <= t["words"][1] for u in r.units)) for r in nw)) for t in tr]
        shown = sum(visible[i] or ranks[i] is not None for i in away)
        vals = (new, worse, pre, len(away), sum(i in m for i in away), shown, len(controls), sum(i in m for i in controls), unmeasurable)
        tally = summary.setdefault(c["split"], dict.fromkeys(("new", "worsened", "pre_existing", "truth", "detected", "flagged_or_listed", "repair_controls", "controls_detected", "unmeasurable"), 0))
        for k, v in zip(tally, vals):
            tally[k] += v
        rows.append([c["id"], ref, c["split"], *vals])
        detail += [{"clip": c["id"], "reference": ref, "reader_group": c["split"], "level": tr[i]["level"], **d, "detected": i in m,
                    "flagged": visible[i], "difference_rank": ranks[i],
                    "expected_secondary_firings": sum(r.dim in tr[i]["secondary"] and near(r, tr[i]) for r in nw)} for i, d in enumerate(classified)]
    by_type = Counter()
    for d in detail:
        if d["direction"] == "away from the reference":
            by_type[(d["reader_group"], d["type"], d["level"], "n")] += 1
            by_type[(d["reader_group"], d["type"], d["level"], "detected")] += d["detected"]
            by_type[(d["reader_group"], d["type"], d["level"], "shown")] += d["flagged"] or d["difference_rank"] is not None
    cells = sorted({k[:3] for k in by_type})
    type_rows = [[g, t, lv, by_type[(g, t, lv, "detected")], by_type[(g, t, lv, "shown")], by_type[(g, t, lv, "n")], wilson(by_type[(g,t,lv,"detected")], by_type[(g,t,lv,"n")])] for g, t, lv in cells]
    pending = Counter((d["reader_group"], d["type"], d["level"]) for d in detail if d["direction"] == "no detector")
    pending_secondary = Counter()
    for d in detail:
        if d["direction"] == "no detector":
            pending_secondary[(d["reader_group"], d["type"], d["level"])] += d["expected_secondary_firings"]
    pending_rows = [[g, t, lv, n, pending_secondary[(g, t, lv)], "no detector"] for (g, t, lv), n in sorted(pending.items())]
    headers = ["new flags", "worsened", "pre-existing", "away-edits", "away-edits detected", f"away-edits flagged or among the {C.MAX_DIFFERENCES} listed differences", "repair controls", "controls flagged", "unmeasurable"]
    tab = md_table(["reader group"] + headers, [[g, *v.values()] for g, v in summary.items()])
    tab += "\n\nAway-edits by type and level (a check reader's clip counts once per calibration reference):\n\n"
    tab += md_table(["reader group", "type", "level", "detected", f"flagged or among the {C.MAX_DIFFERENCES} listed differences", "away-edits", "95% Wilson"], type_rows)
    tab += "\n\n" + md_table(["reader group", "type", "level", "count", "expected secondary firings", "status"], pending_rows)
    tab += "\n\nPer clip and reference:\n\n" + md_table(["clip", "reference", "reader group"] + headers, rows)
    curve = r2_curve(ds, det, kept, consensus=True) if consensus else r2_curve(ds,det,kept)
    comparison = r2_dev_v9_change(curve)
    tab += '\n\nDetected is the success metric. The top-five list is descriptive and unscored.\n\n' + comparison['table']
    family_tiers = tiers(det.get('report', {}).get('real_validation'))
    for d in detail:
        d['tier'] = next(name for name,types in family_tiers.items() if d['type'] in types)
        d['validation'] = 'unvalidated' if d['tier'] == 'synthetic_only' else 'synthetic recovery'
    return {"summary": summary, "by_type": type_rows, "edits": detail, "no_detector": pending_rows, "table": tab, "curve": curve,
            'success_metric': 'detected away-edits', 'listed_scope': 'descriptive, unscored', 'dev_v9_change': comparison}


def cross_section(ds, det, splits):
    single = _cross_section(ds, det, splits)
    if 'R2_consensus' not in det['regimes']:
        single['limitations'] = r2_limits({'single': single}, det.get('report', {}).get('R2_modes', {}))
        return single
    consensus_det = {**det, 'regimes': {**det['regimes'], 'R2': det['regimes']['R2_consensus']}}
    consensus = _cross_section(ds, consensus_det, splits, consensus=True)
    single['modes'] = {'single': {k: v for k,v in single.items() if k != 'modes'}, 'consensus5': consensus}
    single['table'] = 'Single reference:\n\n' + single['table'] + '\n\nMedian of five references:\n\n' + consensus['table']
    diagnostics = det.get('report', {}).get('R2_modes', {})
    scopes = {mode: select_scope(diagnostics.get(mode, {}).get('select', {})) for mode in ('single', 'consensus5')}
    scope_note = '\n\nSelect rate scope: ' + '; '.join(f'{mode}: {text}' for mode, text in scopes.items()) + '.'
    rows = []
    for mode, result in (('single', single), ('consensus5', consensus)):
        for row in result['curve']['rows']:
            if not row['fitted']:
                continue
            rate = diagnostics.get(mode, {}).get('select', {}).get('local_by_key', {}).get(row['key'], {})
            rows.append([mode, row['key'], row['h'], row['threshold'], C.DIM_UNIT[C.dim_of(row['key'])], rate.get('rate'), rate.get('bootstrap_upper95'),
                         ', '.join(rate.get('sources', [])), proportion(row['detected'], row['injected']), row['detected_by_type']])
    single['table'] += '\n\nThreshold, select false rate and check-reader away-edit recall at the same operating point:\n\n' + md_table(
        ['mode','key','h','physical threshold magnitude','unit','select/min','select upper95','select sources','away recall (95% Wilson)','per type'], rows) + scope_note
    clip_rows = []
    for mode in ('single', 'consensus5'):
        diagnostic = diagnostics.get(mode, {})
        for dim, value in diagnostic.get('clip_thresholds', {}).items():
            rate = diagnostic.get('select', {}).get('clip_by_key', {}).get(dim, {})
            choice = diagnostic.get('clip_threshold_choice', {}).get(dim, {})
            clip_rows.append([mode, dim, value, choice.get('clip_budget_quantile'), choice.get('robust_start'), choice.get('clip_budget_per_key'),
                              rate.get('rate'), rate.get('bootstrap_upper95'), ', '.join(rate.get('sources', []))])
    single['table'] += '\n\nWhole-clip thresholds (fit clip-budget quantile; the CLIP_H robust start beside it) and select false rates (separate 0.05/clip budget):\n\n' + md_table(
        ['mode','dimension','threshold (ln)','fit clip-budget quantile','CLIP_H robust start','clip share','select/clip','select upper95','select sources'], clip_rows) + scope_note
    single['select_scope'] = scopes
    single['limitations'] = r2_limits({'single': single, 'consensus5': consensus}, diagnostics)
    single['table'] += '\n\nStated R2 limits (measured, not tuned on select):\n\n' + ('\n'.join('- ' + v for v in single['limitations']) or '- none')
    return single


R2_LIMIT_RECALL = 0.5  # an away-edit type detected in fewer than half of its check-reader edits is a stated limit
R2_LIMIT_L1_MINUTES = 5.0  # first-language groups with less select exposure are too small to state


def r2_limits(modes: dict, diagnostics: dict) -> list[str]:
    """Stated limits of R2 from the measured numbers: away-edit types that the check readers' clips detect in fewer than
    R2_LIMIT_RECALL of their edits, and each mode's select budget when it is not met, with the sources and the first
    languages (at least R2_LIMIT_L1_MINUTES comparison-minutes) whose rate is above the budget."""
    out = []
    for mode, result in modes.items():
        missed = [f'{t} L{lv} {k}/{n}' for g, t, lv, k, _, n, _ in result['by_type'] if g == 'check' and n and k / n < R2_LIMIT_RECALL]
        if missed:
            out.append(f'{mode}: check-reader away-edits detected in fewer than {R2_LIMIT_RECALL:.0%}: ' + ', '.join(missed))
        out += budget_limits(f'{mode} select', diagnostics.get(mode, {}).get('select', {}))
    return out


def languages_above_budget(total: dict) -> list[dict]:
    """First-language groups of a null report (at least R2_LIMIT_L1_MINUTES comparison-minutes) whose rate is above the budget."""
    return [{'language': lang, 'rate': r['rate'], 'readers': r['readers'], 'comparison_minutes': r['comparison_minutes']}
            for lang, r in sorted(total.get('by_L1', {}).items())
            if r['comparison_minutes'] >= R2_LIMIT_L1_MINUTES and r['rate'] > C.FALSE_RATE_BUDGET]


def budget_limits(name: str, null: dict) -> list[str]:
    """The budget statement of one null report when the budget is not met, with the sources and first languages above it."""
    total = null.get('total_local', {})
    if not total or total.get('budget_status') == 'met':
        return []
    sources = [f"{s} {md_cell(r['rate'])}/min" for s, r in sorted(total.get('by_source', {}).items())
               if r.get('rate') is not None and r['rate'] > C.FALSE_RATE_BUDGET]
    languages = [f"{r['language']} {md_cell(r['rate'])}/min ({r['readers']} readers, {md_cell(float(r['comparison_minutes']))} min)"
                 for r in languages_above_budget(total)]
    return [(f"{name}: false-region budget {total.get('budget_status')} (weighted {md_cell(total.get('rate'))}/min, bootstrap upper95 "
             f"{md_cell(total.get('bootstrap_upper95'))}, budget {C.FALSE_RATE_BUDGET}/min); sources above the budget: "
             f"{', '.join(sources) or 'none'}; first languages above it: {', '.join(languages) or 'none'}")]


def select_scope(select: dict) -> str:
    """The sources that a mode's select rates cover; the consensus report also names each fit source it leaves out and why."""
    if select.get('scope'):
        return select['scope']
    sources = select.get('total_local', {}).get('sources')
    return 'select rates cover ' + ', '.join(sources) if sources else 'select rates not measured'


def r2_dev_v9_change(curve):
    old = json.loads(Path(__file__).with_name('dev_v9_reference.json').read_text())
    rows = []
    for r in curve.get('rows', []):
        if not r['fitted']:
            continue
        previous = next((v for v in old['cross_curve'] if v['key'] == r['key'] and v['fitted']), None)
        if previous:
            rows.append({'key': r['key'], 'v9_h': previous['h'], 'current_h': r['h'], 'v9_detected': previous['detected_by_type'],
                         'current_detected': r['detected_by_type'], 'v9_null_per_min': previous['null_per_min'], 'current_null_per_min': r['null_per_min'],
                         'current_null_regions': r['null_regions'], 'current_null_minutes': curve.get('minutes')})
    return {'rows': rows, 'source': old['source'], 'artifact_sha256': old['sha256'],
            'verified_v9_to_v10': 'Pace sensitivity fell: RUSH 20/31 to 6/31; DRAG 14/17 to 8/17. The fixed check-reader null stayed 8/7.76 min = 1.03/min. Other keys did not show a general sensitivity collapse.',
            'table': 'R2 change against dev_v9 on the fixed check-reader population:\n\n' + md_table(
                ['key','v9 h','current h','v9 detected by type','current detected by type','v9 null/min','current null/min','current null regions','current null comparison-minutes'],
                [[r[k] for k in ('key','v9_h','current_h','v9_detected','current_detected','v9_null_per_min','current_null_per_min','current_null_regions','current_null_minutes')] for r in rows]) +
                '\n\nVerified v9-to-v10: RUSH 20/31 to 6/31, DRAG 14/17 to 8/17; check null unchanged at 1.03/min. EARS had the highest v10 D1 fit-source rate (0.126–0.137/min), driving the pace threshold upward. Current fit-source rates appear in the fit/select diagnostics; the fixed check population is separate from the expanded select pool.'}


def listed_rank(diffs: list[dict], t: dict) -> int | None:
    """1-based place of an injected edit in the unscored differences list: same dimension and sign, on its words (pauses:
    its boundary)."""
    for rank, d in enumerate(diffs, 1):
        if t.get('event') == 'clip' and d['words'] is None and d['dimension'] == t['dim']:
            return rank
        if d["words"] is None or d["dimension"] != t["dim"] or (t["sign"] != 0 and (d["delta"] > 0) != (t["sign"] > 0)):
            continue
        w0, w1 = t["words"]
        if d["words"][0] <= w1 and d["words"][1] >= w0:
            return rank
    return None


def r2_curve(ds: Dataset, det: dict, kept: list[tuple], consensus=False) -> dict:
    """Each R2 flag key (dimension and direction) has its own diagnostic curve on the check readers, with the fitted h marked."""
    reg = det["regimes"]["R2"]
    nulls = r2_nulls(ds, reader_ids(ds, "reader_calibration"), reader_ids(ds, "reader_check"))
    if consensus:
        unique = {c['parent']: run0 for c,run1,run0,lab in kept if c['split'] == 'check'}
        nulls = [Null('consensus>'+p, run.comp, run.B.tr.sentence, run.P.duration/60, reader=p) for p,run in unique.items()]
    minutes = sum(n.minutes for n in nulls)
    check = [k for k in kept if k[0]["split"] == "check"]
    readers = sorted({participant_of(n.id) for n in nulls})
    rows = []
    for dim in reg["enabled"]:
        for sign in C.FLAG_SIGNS[dim]:
            fitted = threshold(reg, dim, sign)
            for h in sorted(set(float(h) for h in np.arange(1, 6.01, 0.5)) | ({fitted} if fitted is not None else set())):
                trial = {**reg, "enabled": [dim], "h": {key(dim, sign): h}}
                counts = {n.id: len(decode_dim(n.comp.dims[dim], scale(reg, dim, sign), h, n.sentence, (sign,))) for n in nulls}
                found, total = Counter(), Counter()
                for _, run1, run0, lab in check:
                    tr = [t for t in truths(lab) if t["dim"] == dim and t["sign"] in (0, sign) and edit_direction(run0, run1, t)["direction"] == "away from the reference"]
                    m = match(tr, run1.with_regions(new_worsened(run0, run1, trial)))
                    for i, t in enumerate(tr):
                        total[t["type"]] += 1
                        found[t["type"]] += i in m
                rows.append({"key": key(dim, sign), "h": h, "threshold": h * scale(reg, dim, sign), "fitted": h == fitted, "null_regions": sum(counts.values()),
                             "null_per_min": sum(counts.values()) / minutes if minutes else None,
                             "reader_counts": {p: sum(n for pair, n in counts.items() if participant_of(pair) == p) for p in readers},
                             "detected": sum(found.values()), "injected": sum(total.values()),
                             "detected_by_type": {t: proportion(found[t],n) for t, n in total.items()}})
    tab = md_table(["flag key", "h", "threshold", "fitted on null fit pool", "observed false regions per comparison-minute", "reader counts", "away-edits detected", "by type"],
                   [[r["key"], r["h"], r["threshold"], r["fitted"], r["null_per_min"], r["reader_counts"], proportion(r['detected'],r['injected']), r["detected_by_type"]] for r in rows])
    return {"calibrated_h": reg["h"], "minutes": minutes, "rows": rows, "table": tab}


def whole_passage_clip(rec: Recording, reader_id: str, typ: str, lv: int) -> np.ndarray:
    """A reader's recording with one edit over the whole passage (a pool worker runs this)."""
    cid = f"{reader_id}__whole_{typ}_L{lv}"
    plan = flaws.Plan([flaws.make_edit(rec, typ, lv, (0, len(rec.tr) - 1))])
    return flaws.inject(rec, plan, cid, reader_id, recipe=f"whole_{typ}_L{lv}", seed=flaws.clip_seed(cid))[0]


WHOLE_CLIP_TYPES = {"RUSH": "D1", "MONOTONE": "D3"}  # whole-passage edit -> the whole-clip flag it should raise


def botched_section(ds: Dataset, det: dict, splits: tuple[str, ...]) -> dict:
    """R2 whole-clip detection. Bottom rung: each reader's botched clip (whole-passage rush and flat pitch, dropped pauses,
    fades) against a different speaker's reference, beside the same pair unedited. Graded rungs: each check reader with one
    whole-passage edit (rush or flat pitch) at levels 1 to 3, generated on the fly, against every calibration reader."""
    rows = []
    for c, ref, bad, clean, _ in cross_pairs(ds, det, ds.clips(kind="cross_botched")):
        rows.append({"clip": c["id"], "reader_group": c["split"], "reference": ref, "clean_score": clean.scored.overall, "clean_flags": clean.flag_keys,
                     "botched_score": bad.scored.overall, "botched_flags": bad.flag_keys,
                     "whole_clip": sorted(clip_key(k, g) for k, g in bad.clip.items())})
    summary = {}
    for group in dict.fromkeys(r["reader_group"] for r in rows):
        sel = [r for r in rows if r["reader_group"] == group]
        summary[group] = {"pairs": len(sel), "tempo_flagged": sum(any(k.startswith("D1-") for k in r["whole_clip"]) for r in sel),
                          "range_flagged": sum(any(k.startswith("D3") for k in r["whole_clip"]) for r in sel),
                          "median_clean_score": float(np.median([r["clean_score"] for r in sel])),
                          "median_botched_score": float(np.median([r["botched_score"] for r in sel])),
                          "max_botched_score": float(max(r["botched_score"] for r in sel))}
    cal, chk = reader_ids(ds, "reader_calibration"), reader_ids(ds, "reader_check")
    recs = dict(zip(cal + chk, ds.recs([ds.entry("readers", i) for i in cal + chk])))
    cells = [(p, typ, lv) for p in chk for typ in WHOLE_CLIP_TYPES for lv in C.LEVELS]
    wavs = map_calls(whole_passage_clip, [(recs[p], p, typ, lv) for p, typ, lv in cells], ds.pool)
    graded = []
    for (p, typ, lv), P in zip(cells, ds.prepare_many([(w, recs[p].tr) for w, (p, _, _) in zip(wavs, cells)])):
        for b in cal:
            run = run_pair(recs[b], P, det, "R2")
            graded.append({"reader": p, "reference": b, "type": typ, "level": lv, "flagged": run.clip.get(WHOLE_CLIP_TYPES[typ], 0.0) < 0,
                           "score": run.scored.overall, "flags": run.flag_keys})
    ladder = [["unedited", "", "", sum(bool(clip_flags(stored_pair(ds, recs[b], recs[p], det, "R2").comp, det["regimes"]["R2"])) for p in chk for b in cal),
               len(chk) * len(cal), float(np.median([stored_pair(ds, recs[b], recs[p], det, "R2").scored.overall for p in chk for b in cal]))]]
    for typ in WHOLE_CLIP_TYPES:
        for lv in C.LEVELS:
            sel = [g for g in graded if (g["type"], g["level"]) == (typ, lv)]
            ladder.append([f"whole-passage {typ}", lv, C.LEVEL_PARAM[typ][lv - 1], sum(g["flagged"] for g in sel), len(sel), float(np.median([g["score"] for g in sel]))])
    check = [r for r in rows if r["reader_group"] == "check"]
    ladder.append(["botched (G5)", "", "", sum({"D1- whole clip", "D3- whole clip"} <= set(r["whole_clip"]) for r in check), len(check), float(np.median([r["botched_score"] for r in check])) if check else None])
    tab = "Check readers against every calibration reader, by rung (whole-clip flag of the edited dimension; botched: both flags):\n\n"
    tab += md_table(["rung", "level", "magnitude", "whole-clip flag raised", "pairs", "median score"], ladder)
    tab += "\n\n" + md_table(["reader group", "pairs", "overall tempo flagged", "overall pitch range flagged", "median score unedited", "median score botched", "highest score botched"],
                             [[g, v["pairs"], v["tempo_flagged"], v["range_flagged"], v["median_clean_score"], v["median_botched_score"], v["max_botched_score"]] for g, v in summary.items()])
    tab += "\n\n" + md_table(["clip", "reference", "score unedited", "flags unedited", "score botched", "flags botched"],
                              [[r["clip"], r["reference"], r["clean_score"], ", ".join(r["clean_flags"]), r["botched_score"], ", ".join(r["botched_flags"])] for r in rows])
    extra_graded = []
    clips = [c for c in ds.manifest.get("clips", []) if c["kind"] == "cross" and c.get("spectrum") == "extra"]
    for c, ref, edited, clean, lab in cross_pairs(ds, det, clips) if clips else []:
        tr = truths(lab)
        _, matches, _ = cross_matches(clean, edited, tr, det["regimes"]["R2"])
        extra_graded += [{"reader": c["parent"], "reference": ref, "type": t["type"], "level": t["level"],
                          "flagged": i in matches if t["available"] else None,
                          "status": ('whole-clip rung' if t['event'] == 'clip' else 'local event rung') if t["available"] else "no detector",
                          "score": edited.scored.S.get(t["dim"])} for i, t in enumerate(tr)]
    tab += "\n\nNew-type local rungs (stored cross clips):\n\n" + md_table(
        ["reader", "reference", "type", "level", "local event detected", "dimension score", "status"],
        [[r[k] for k in ("reader", "reference", "type", "level", "flagged", "score", "status")] for r in extra_graded])
    limits = [f"{r[0]}{' L' + str(r[1]) if r[1] else ''}: whole-clip flag raised in {r[3]}/{r[4]} check-reader pairs"
              for r in ladder[1:] if r[4] and r[3] / r[4] < R2_LIMIT_RECALL]
    tab += "\n\nStated limits (whole-clip flag raised in fewer than " + f"{R2_LIMIT_RECALL:.0%} of the pairs):\n\n" + ("\n".join("- " + v for v in limits) or "- none")
    return {"rows": rows, "summary": summary, "graded": graded, "extra_graded": extra_graded, "ladder": ladder, "limits": limits, "table": tab}


def ladder_section(ds: Dataset, det: dict, splits: tuple[str, ...]) -> dict:
    """R1 score by rung of the bad spectrum, per split: identity, level-1 to level-3 clips, and the ladder clips G1, G3, G5."""
    clips = [c for c in ds.manifest["clips"] if c["kind"] in ("identity", "single", "ladder") and c["split"] in splits]
    scores, by_speech, split_of = defaultdict(list), defaultdict(dict), {}
    for c, run, _ in clip_runs(ds, det, clips):
        rung = f"extra level {c['level']}" if c.get("spectrum") == "extra" else "identity" if c["kind"] == "identity" else f"level {c['level']} (four edits)" if c["kind"] == "single" else c["recipe"]
        scores[(c["split"], rung)].append(run.scored.overall)
        by_speech[c["parent"]][rung], split_of[c["parent"]] = run.scored.overall, c["split"]
    order = ["identity", "G1", "level 1 (four edits)", "G3", "level 2 (four edits)", "level 3 (four edits)", "G5", "extra level 1", "extra level 2", "extra level 3"]
    rows = []
    for sp in splits:
        for rung in order:
            values = scores.get((sp, rung))
            if values:
                rows.append([sp, rung, len(values), float(min(values)), float(np.median(values)), float(max(values))])
    gates = []  # the score gates of calibration (fitted on train), checked on every split evaluated
    for sp in splits:
        got = {rung: scores.get((sp, rung), []) for rung in order}
        gates.append([sp, len([v for v in got["identity"] if identity_gate_fails(v)]),
                      len([v for v in got["G1"] + got["level 1 (four edits)"] if l1_gate_fails(v)]),
                      len([v for v in got["G5"] if g5_gate_fails(v)]), sum(by_speech[b].get("G1", 100) < by_speech[b].get("G3", 0) or by_speech[b].get("G3", 100) < by_speech[b].get("G5", 0)
                                                               for b in by_speech if split_of[b] == sp)])
    tab = md_table(["split", "rung", "clips", "lowest score", "median score", "highest score"], rows)
    tab += "\n\nScore gates (violations):\n\n" + md_table(["split", f"identity below {C.GATE_IDENTITY:.0f}", f"level-1 clip below {C.GATE_L1_MIN:.0f}", f"G5 above {C.GATE_G5_MAX:.0f}", "ladder G1 >= G3 >= G5 broken"], gates)
    return {"rows": rows, "gates": gates, "table": tab}


# ============================================================================================ trivial baselines
def tier_labels(lab: dict, types) -> dict:
    """Labels with the flaws of other reporting tiers excluded from truth."""
    return {**lab, 'flaws': [f if f['type'] in types else {**f, 'evaluation_excluded': ['other reporting tier']} for f in lab['flaws']]}


def _flag_all(n: int, dims) -> list[Region]:
    """Every unit flagged in the dimensions `dims`: one region per five-word window (every start) per windowed dimension and
    sign, so that any truth of up to two windows can be matched; every boundary / word for events."""
    regs = []
    for dim in dims:
        for sign in C.FLAG_SIGNS[dim]:
            if C.is_event(dim):
                regs += [Region(dim, sign, i, i, i, 9.9, (i,)) for i in range(n - 1 if C.UNIT_KIND[dim] == "boundary" else n)]
            else:
                width = min(C.WINDOW_WORDS, n)
                regs += [Region(dim, sign, i, i + width - 1, i, 9.9, tuple(range(i, i + width))) for i in range(n - width + 1)]
    return regs


def _random_regions(tr: list[dict], n: int, rng) -> list[Region]:
    """As many regions as injected flaws, of the same dimension, sign and word length, at random positions (every start
    position that fits, the last included)."""
    regs = []
    for t in tr:
        if t["dim"] not in C.DIMS or t.get('event') == 'clip':
            continue
        w = 1 if C.is_event(t["dim"]) else t["words"][1] - t["words"][0] + 1
        units = n - 1 if C.UNIT_KIND[t["dim"]] == "boundary" else n
        i0 = int(rng.integers(0, units - w + 1))
        regs.append(Region(t["dim"], t["sign"], i0, i0 + w - 1, i0, 9.9, tuple(range(i0, i0 + w))))
    return regs


def _own_median(v: np.ndarray) -> tuple[np.ndarray, float]:
    """(v minus its median over finite entries, the median)."""
    ok = np.isfinite(v)
    centre = float(np.median(v[ok])) if ok.any() else float('nan')
    return v - centre, centre


def reference_free(comp: Comparison, P: Recording) -> Comparison:
    """The comparison without a reference reading: the participant's own recording is the reference, each measure taken
    against the participant's own median over the clip (pauses: over the boundaries with and over those without
    punctuation, separately). Emphasis (D4) needs the reference's stress words and the whole-clip measures need a
    reference, so they are absent; D7 and D8 are listed in R1 and are absent too."""
    dims = dict(comp.dims)
    tp = _speech_time(P, P.sil >= C.PAUSE_MIN_S)
    for dim, measure, values in (('D1', np.log(tp), tp), ('D3', np.log(P.win_R + C.RANGE_REG_ST), P.win_R), ('D5', P.win_E, P.win_E),
                                 ('D6', np.log(P.win_Q + 1e-6), P.win_Q), ('D9', np.log(P.win_W), P.win_W)):
        x, centre = _own_median(np.asarray(measure, float))
        dims[dim] = dataclasses.replace(comp.dims[dim], x=x, b=np.full(len(x), centre), p=np.asarray(values, float), g=float('nan'))
    n = len(P.tr)
    punct = np.array([P.tr.punct[i] != "" for i in range(n - 1)])
    rp = np.asarray(P.sil_raw, float)
    rb = np.full(n - 1, np.nan)
    for group in (punct, ~punct):
        rb[group] = _own_median(rp[group])[1] if group.any() else np.nan
    elig = (rb >= C.PAUSE_MIN_S) | (P.sil >= C.PAUSE_MIN_S)
    x = np.where(elig, rp - rb, np.nan)
    countable = elig & (((x < 0) & (rb >= C.PAUSE_DROP_MIN_BASE_S)) | ((x > 0) & (rb < C.PAUSE_MIN_S) & ~punct))
    dims['D2'] = dataclasses.replace(comp.dims['D2'], x=x, b=np.where(elig, rb, np.nan), p=np.where(elig, rp, np.nan), countable=countable,
                                     w=np.full(n - 1, 1.0 / max(1, int((rb >= C.PAUSE_MIN_S).sum()))))
    for dim in ('D4', 'D7', 'D8'):
        nan = np.full(len(comp.dims[dim].x), np.nan)
        dims[dim] = dataclasses.replace(comp.dims[dim], x=nan, countable=np.zeros(len(nan), bool), g=float('nan'))
    return dataclasses.replace(comp, dims=dims)


def _decoded_view(run: Run, comp: Comparison, reg: dict) -> Run:
    """The run with `comp` decoded under the regime `reg`; no whole-clip flag."""
    return Run(run.B, run.P, comp, decode(comp, reg, run.P.tr.sentence), run.scored, run.regime, {}, run.scale, run.enabled)


def reference_free_run(run: Run, reg: dict) -> Run:
    """The run decoded on its reference-free comparison under the regime `reg`; no whole-clip flag."""
    return _decoded_view(run, reference_free(run.comp, run.P), reg)


def strict_counts(run: Run, lab: dict) -> tuple[list[int], int]:
    """([TP, FP, FN], same-change duplicates) of one clip under the strict headline accounting."""
    e = eval_clip(run, lab, secondary_exempt=False)
    tp = sum(bool(t["detected"]) for t in e["truth"] if t["available"])
    return [tp, len(e["false"]) + len(e['false_clip']), sum(t["available"] for t in e["truth"]) - tp], e["duplicate"]


def reference_free_h(ds: Dataset, det: dict) -> dict:
    """The common h of the reference-free baseline, chosen like the detector's: train core8 L2+L3 strict F1 maximum over
    the R1 common grid (one h for every flag key, D9 included), ties to the smaller h."""
    reg = det['regimes']['R1']
    clips = [c for c in ds.clips(kind='single') if c['split'] == 'train' and c['level'] in C.HEADLINE_LEVELS]
    pairs = [(run, tier_labels(lab, C.CORE8_TYPES)) for c, run, lab in clip_runs(ds, det, clips)]
    pairs = [(run, lab) for run, lab in pairs if any(not f.get('evaluation_excluded') for f in lab['flaws'])]
    if not pairs:
        return {'h': None, 'reason': 'no train clips evaluated'}
    comps = [(run, reference_free(run.comp, run.P), lab) for run, lab in pairs]
    curve = []
    for h in r1_common_grid():
        trial = {**reg, 'h': {k: None if v is None else h for k, v in reg['h'].items()}}
        total = np.zeros(3)
        for run, comp, lab in comps:
            total += strict_counts(_decoded_view(run, comp, trial), lab)[0]
        curve.append({'h': h, 'tp': int(total[0]), 'fp': int(total[1]), 'fn': int(total[2]), 'f1': f1(*total)['f1'] or 0.0})
    best = best_by_f1(curve, 'f1')
    return {'h': best['h'], 'train': best, 'rule': 'in-sample train core8 L2+L3 strict F1 maximum on the R1 common grid; ties use smaller h',
            'curve': curve}


def _trivial_section(ds: Dataset, det: dict, splits: tuple[str, ...], types, free_h=None) -> dict:
    """Flag-all, no-flags, random spans / events (RANDOM_SEEDS repetitions, averaged) and the reference-free detector
    (the same detector with the participant's own recording as the reference: at the detector's h, and at the h chosen
    for it on train) against the detector, all scored by the strict headline accounting (unscored dimensions are not
    truths) on held-out single-level L2 + L3 clips."""
    held = held_out(splits)
    reg = det['regimes']['R1']
    cl = [c for c in ds.clips(kind="single") if c["split"] in held and c["level"] in C.HEADLINE_LEVELS]
    free = {'reference_free (detector h)': reg}
    if free_h is not None:
        free[f'reference_free (train-chosen h={free_h})'] = {**reg, 'h': {k: None if v is None else free_h for k, v in reg['h'].items()}}
    methods = ("detector", "no_flags", "flag_all", "random", *free)
    tot = {sp: {k: [0.0, 0.0, 0.0] for k in methods} for sp in held}
    dup = {sp: dict.fromkeys(methods, 0.0) for sp in held}

    def add(split: str, name: str, view: Run, lab: dict, weight: float = 1.0) -> None:
        counts, duplicated = strict_counts(view, lab)
        for i, v in enumerate(counts):
            tot[split][name][i] += weight * v
        dup[split][name] += weight * duplicated

    dims = flagged_dims(reg)
    for c, run, lab in clip_runs(ds, det, cl):
        if not any(f['type'] in types for f in lab['flaws']):
            continue
        lab = tier_labels(lab, types)
        tr, n = truths(lab), len(run.P.tr)
        everything = {k: run.comp.dims[k].g for k in C.CLIP_DIMS if k in dims and np.isfinite(run.comp.dims[k].g)}
        add(c["split"], "detector", run, lab)
        add(c["split"], "no_flags", dataclasses.replace(run, regions=[], clip={}), lab)
        add(c["split"], "flag_all", dataclasses.replace(run, regions=_flag_all(n, dims), clip=everything), lab)
        for rep in range(C.RANDOM_SEEDS):
            add(c["split"], "random", dataclasses.replace(run, regions=_random_regions(tr, n, np.random.default_rng([flaws.clip_seed(c["id"]), rep])), clip={}),
                lab, 1.0 / C.RANDOM_SEEDS)
        for name, trial in free.items():
            add(c["split"], name, reference_free_run(run, trial), lab)
    for name, gs in split_groups(held):
        if len(gs) > 1:
            tot[name] = {k: [sum(tot[sp][k][i] for sp in gs) for i in range(3)] for k in methods}
            dup[name] = {k: sum(dup[sp][k] for sp in gs) for k in methods}
    rows = [[sp, k, *[round(v, 2) for v in vals], round(dup[sp][k], 2), f1(*vals)["f1"]] for sp, methods in tot.items() for k, vals in methods.items()]
    return {"totals": tot, "same_change_duplicates": dup, "accounting": STRICT_ACCOUNTING,
            "table": md_table(["split", "method", "TP", "FP", "FN", "same-change duplicates (not FP)", "F1"], rows)}


def trivial_section(ds, det, splits):
    free = reference_free_h(ds, det) if 'train' in splits else {'h': None, 'reason': 'train not evaluated'}
    groups = {name: _trivial_section(ds, det, splits, types, free['h']) for name, types in tiers(det.get('report', {}).get('real_validation')).items()}
    note = ('The detector row equals the strict headline row of each tier (same truths: unscored dimensions are not truths). '
            'flag_all flags every five-word window and every event unit of each scored dimension: a recall ceiling at IoU >= 0.5. '
            'reference_free is the same detector with no reference reading: every measure is taken against the participant\'s own '
            'median over the clip (pauses: per punctuation class); emphasis and the whole-clip measures need a reference and are '
            'absent. reference_free reuses the detector\'s scales and h grid and has no text normalisation: it is a lower bound '
            'without a reference, and it does not measure the full value of the reference reading. '
            f"Train-chosen reference-free h: {free['h']} ({free.get('rule') or free.get('reason')}).")
    return {**groups['core8'], 'groups': groups, 'reference_free': {k: v for k, v in free.items() if k != 'curve'}, 'reference_free_curve': free.get('curve'),
            'table': note + '\n\n' + '\n\n'.join(name + (' (unvalidated)' if name == 'synthetic_only' else '') + ':\n\n' + group['table'] for name,group in groups.items())}


# ============================================================================================ stress matrix
def diff_regions(ref: Run, new: Run) -> tuple[list[str], int]:
    """(added, removed): the (dimension, sign) keys of the regions of `new` with no same-key overlapping region in `ref`, and
    the number of regions of `ref` with none in `new`."""
    added = [key(r.dim, r.sign) for r in new.regions if not any(overlaps(r, q) for q in ref.regions)]
    removed = sum(not any(overlaps(r, q) for q in new.regions) for r in ref.regions)
    added += [clip_key(k, g) for k, g in new.clip.items() if k not in ref.clip]
    removed += sum(k not in new.clip for k in ref.clip)
    return added, removed


STRESS_BATCH = 8  # transform jobs per pool batch; it bounds the transformed audio held in memory at one time
STRESS_SECONDS_PER_AUDIO_SECOND = 0.008  # forecast: preparation seconds per second of transformed audio on four T4 x2 workers
STRESS_SECONDS_PER_JOB = 0.08  # forecast: fixed seconds per transform job on four T4 x2 workers
STRESS_RETENTION_LIMIT = 0.95  # a key whose detections are kept less often than this under a condition is stated as broken by it


def stress_rate(records: list[dict], count, cluster: str = 'participant_recording') -> dict:
    """Events count(record) per comparison-minute, pooled over every seed, with a 95% bootstrap interval over `cluster`
    (participant recordings: the seeds of one recording are one cluster, never independent trials). With fewer than
    MIN_BOOTSTRAP_CLUSTERS clusters, the rate of each cluster and no interval; with no event, the exact Poisson upper
    bound on the minutes of one seed per recording."""
    unit = CLUSTER_UNIT[cluster]
    clusters = defaultdict(list)
    for r in records:
        clusters[r[cluster]].append((count(r), r['minutes']))
    events = sum(c for rows in clusters.values() for c, _ in rows)
    minutes = sum(m for rows in clusters.values() for _, m in rows)
    if not events:
        first_seed = {}
        for r in records:
            first_seed.setdefault(r['participant_recording'], r['minutes'])
        return {'rate': 0.0, 'events': 0, 'ci95': [0.0, round(poisson(0, sum(first_seed.values()))[1], 3)], 'per_cluster': None, 'range': None,
                'method': 'no event: exact Poisson 95% upper bound on the minutes of one seed per recording', 'unit': unit}
    summary = cluster_summary(clusters, lambda rows: sum(c for c, _ in rows) / sum(m for _, m in rows), unit=unit)
    return {'rate': round(events / minutes, 4), 'events': events, 'ci95': summary['ci95'], 'per_cluster': summary['per_cluster'],
            'range': summary['range'], 'method': summary['method'], 'unit': unit}


def stress_retention(records: list[dict], key_filter=None, cluster: str = 'participant_recording') -> dict:
    """Detections found on the unperturbed clip that the perturbed clip keeps, pooled over every seed, with a 95% bootstrap
    interval over `cluster` (fewer than MIN_BOOTSTRAP_CLUSTERS: per-cluster values, no interval); also over unique
    detections, those kept in every seed. `key_filter`: only the detections of one truth key."""
    unit = CLUSTER_UNIT[cluster]
    keep = (lambda keys: keys) if key_filter is None else (lambda keys: [k for k in keys if k == key_filter])
    clusters, by_recording = defaultdict(list), defaultdict(list)
    for r in records:
        found = [i for i, k in zip(r['found_before_ids'], r['found_before_keys']) if keep([k])]
        clusters[r[cluster]].append((sum(i in found for i in r['retained_ids']), len(found)))
        by_recording[r['participant_recording']].append((set(found), {i for i in r['retained_ids'] if i in found}))
    found = sum(f for rows in clusters.values() for _, f in rows)
    unique = sum(len(rows[0][0]) for rows in by_recording.values())
    every_seed = sum(len(set.intersection(*[kept for _, kept in rows])) for rows in by_recording.values())
    if not found:
        return {'fraction': None, 'retained': 0, 'found': 0, 'unique_found': 0, 'retained_every_seed': 0, 'ci95': [None, None],
                'per_cluster': None, 'range': None, 'method': 'no detection before the transform', 'unit': unit}
    summary = cluster_summary({k: v for k, v in clusters.items() if sum(f for _, f in v)},
                              lambda rows: sum(k for k, _ in rows) / sum(f for _, f in rows), unit=unit)
    retained = sum(k for rows in clusters.values() for k, _ in rows)
    return {'fraction': round(retained / found, 4), 'retained': retained, 'found': found, 'unique_found': unique,
            'retained_every_seed': every_seed, 'ci95': summary['ci95'], 'per_cluster': summary['per_cluster'],
            'range': summary['range'], 'method': summary['method'], 'unit': unit}


CLUSTER_UNIT = {'participant_recording': 'recording', 'speaker': 'speaker'}
STRESS_SCOPE = {
    'participant_recording': 'rates and retention pooled over every seed; 95% bootstrap over participant recordings (seeds of one '
                             f'recording are one cluster) with >= {MIN_BOOTSTRAP_CLUSTERS} recordings, else per-recording values; zero '
                             'events: Poisson bound on one seed per recording',
    'speaker': 'rates and retention pooled over every seed; per-speaker values and their range, no interval (fewer than '
               f'{MIN_BOOTSTRAP_CLUSTERS} speakers); zero events: Poisson bound on one seed per recording; recomputed after the final '
               'evaluation from the saved stress records'}


def stress_intervals(records: list[dict], share: float, cluster: str = 'participant_recording') -> dict:
    """The interval fields of one stress-matrix row (records of one split, condition, regime and reference mode), with
    `cluster` as the resampling unit, and the limits that they give (stress_limits)."""
    added = stress_rate(records, lambda r: r['added'], cluster)
    removed = stress_rate(records, lambda r: r['removed'], cluster)
    retention = stress_retention(records, cluster=cluster)
    added_by_key = {k: stress_rate(records, lambda r, k=k: r['regions_added'].count(k), cluster)
                    for k in sorted({k for r in records for k in r['regions_added']})}
    retention_by_key = {k: stress_retention(records, k, cluster) for k in sorted({k for r in records for k in r['found_before_keys']})}
    return {'added_per_min': added['rate'], 'added_ci95': added['ci95'], 'added_interval': added,
            'removed_per_min': removed['rate'], 'removed_ci95': removed['ci95'], 'removed_interval': removed,
            'retention': retention['fraction'], 'retention_ci95': retention['ci95'], 'retention_interval': retention,
            'added_by_key': added_by_key, 'retention_by_key': retention_by_key, 'limits': stress_limits(added_by_key, retention_by_key, share),
            'interval_scope': STRESS_SCOPE[cluster]}


def stress_records(row: dict, detail: list[dict]) -> list[dict]:
    """The saved per-comparison records of one stress-matrix row."""
    gs = row['split'].split('+')
    return [r for r in detail if r['split'] in gs and r['condition'] == row['condition'] and r['regime'] == row['regime']
            and r['reference_mode'] == row['reference_mode']]


def speaker_stress_row(row: dict, detail: list[dict]) -> dict:
    """A stress-matrix row with speakers, not participant recordings, as clusters: the rows of val and test (2 speakers
    each) then give per-speaker values and no interval."""
    return {**row, **stress_intervals(stress_records(row, detail), row['key_share_per_min'], 'speaker')}


def speaker_stress_rows(stress: dict) -> list[dict]:
    """The stress rows with speakers as clusters for val, test and val+test (2 speakers each: per-speaker values, no
    interval) and the saved recording-cluster rows for train."""
    return [speaker_stress_row(r, stress['flawed_clips']) if r['split'] in ('val', 'test', 'val+test') else r for r in stress['rows']]


def key_share(reg: dict) -> float:
    """The per-key share of the false-region budget: the regime's own (R2), or the budget split over the flag keys with a
    threshold (R1)."""
    keys = [k for k in KEYS if C.dim_of(k) in reg['enabled'] and reg['h'].get(k) is not None]
    return reg.get('null', {}).get('budget_per_key') or C.FALSE_RATE_BUDGET / max(1, len(keys))


def stress_limits(added_by_key: dict, retention_by_key: dict, share: float) -> list[str]:
    """Keys a condition breaks: added local regions per minute whose 95% lower bound (the rate where no interval exists)
    is above the per-key share of the budget, or detections kept with a 95% upper bound (or fraction) below
    STRESS_RETENTION_LIMIT. Whole-clip flags are counted per clip, not per minute, and are reported without this rule."""
    def interval(v):
        return md_cell(v['ci95']) if v['ci95'][0] is not None else f"(no interval: fewer than {MIN_BOOTSTRAP_CLUSTERS} {v.get('unit', 'recording')}s)"
    out = []
    for k, v in added_by_key.items():
        bound = v['ci95'][0] if v['ci95'][0] is not None else v['rate']
        if not k.endswith('whole clip') and bound > share:
            out.append(f"adds {k} regions: {md_cell(v['rate'])}/min {interval(v)} against the per-key share {md_cell(share)}/min")
    for k, v in retention_by_key.items():
        bound = v['ci95'][1] if v['ci95'][1] is not None else v['fraction']
        if v['fraction'] is not None and bound < STRESS_RETENTION_LIMIT:
            out.append(f"loses {k} detections: kept {v['retained']}/{v['found']} ({md_cell(v['fraction'])}) {interval(v)}")
    return out


def stress_section(ds: Dataset, det: dict, splits: tuple[str, ...]) -> dict:
    """The measured degradation per condition and key, participant-only transforms on every selected clip and on the
    check readers (R2 single and median-of-five references): added false regions per minute and the retention of the
    detections found on the unperturbed clip, with intervals clustered by recording. No pass rule: the rows state which
    conditions break which keys (stress_limits)."""
    import functools
    bs = [b for b in ds.manifest['baselines'] if b['split'] in splits]
    baselines = dict(zip([b['id'] for b in bs], ds.recs(bs)))
    selected = [c for c in ds.clips() if c['split'] in splits]
    runs = clip_runs(ds, det, selected)
    dets = {'single': det}
    if 'R2_consensus' in det['regimes']:
        dets['consensus5'] = {**det, 'regimes': {**det['regimes'], 'R2': det['regimes']['R2_consensus']}}
    cases = [(c['id'], c['split'], c['parent'], c.get('kind', 'single'), run, lab, 'single') for c, run, lab in runs]
    cal, chk = reader_ids(ds, 'reader_calibration'), reader_ids(ds, 'reader_check')
    ids = cal + chk
    readers = dict(zip(ids, ds.recs([ds.entry('readers', i) for i in ids])))
    cases += [(f'{b}>{p}', 'check readers', p, 'null', stored_pair(ds, readers[b], readers[p], det, 'R2'), {'flaws': []}, 'single') for b in cal for p in chk]
    for p in chk if 'consensus5' in dets else ():
        made = consensus_of(ds, p, [b for b in cal if b != p])
        if made is not None:
            cases.append((f"{','.join(made[0])}>{p}", 'check readers', p, 'null', stored_pair(ds, made[1], readers[p], dets['consensus5'], 'R2'),
                          {'flaws': []}, 'consensus5'))
    matrix = [*stress.MATRIX, ('babble 10 dB SNR', None), ('babble 20 dB SNR', None)]
    draws = sum(len(stress.seeds(fn)) if fn is not None else len(stress.RANDOM_SEEDS) for _, fn in matrix)
    audio_seconds = sum(case[4].P.duration for case in cases) * draws
    jobs = len(cases) * draws
    forecast = {'clips': len(selected), 'transform_jobs': jobs, 'transformed_audio_minutes': audio_seconds / 60,
                'expected_seconds': STRESS_SECONDS_PER_AUDIO_SECOND * audio_seconds + STRESS_SECONDS_PER_JOB * jobs,
                'basis': 'v10 pooled preparation 233.5 s / 1329 jobs, evaluation 541.6 s / 1458 jobs; 0.008 s/audio-s plus 0.08 s/job on four T4 x2 workers',
                'batch_size': STRESS_BATCH}
    forecast['stage_seconds'] = dict(STAGE_FORECAST_SECONDS)
    forecast['run_seconds'] = [sum(v[i] for v in forecast['stage_seconds'].values()) for i in (0, 1)]
    forecast['v13_run_seconds'] = 6115.4
    forecast['assumptions'] = STAGE_FORECAST_BASIS
    log('forecast T4 x2 (s): ' + ', '.join(f'{k} {v[0]}-{v[1]}' for k, v in forecast['stage_seconds'].items()) +
        f"; total {forecast['run_seconds'][0] / 60:.0f}-{forecast['run_seconds'][1] / 60:.0f} min")
    detail, babble_sources, before = [], {}, {}
    for name, transform in matrix:
        pending = []
        for cid, split, speaker, kind, ref, lab, mode in cases:
            fn = transform
            if fn is None:
                donors = [b for b in bs if b['id'] != speaker and b['id'] != cid.split('>')[0]][:4]
                if len(donors) < 2:
                    raise ValueError('babble requires at least two other dataset speakers')
                babble_sources[cid] = [b['id'] for b in donors]
                fn = functools.partial(stress.babble, speakers=[baselines[b['id']].wav for b in donors], snr=10 if '10 dB' in name else 20)
            pending.extend((cid, split, speaker, kind, ref, lab, mode, fn, seed) for seed in stress.seeds(fn))
        for start in range(0, len(pending), STRESS_BATCH):
            batch = pending[start:start + STRESS_BATCH]
            wavs = map_calls(stress.apply, [(fn, ref.P.wav, seed) for _, _, _, _, ref, _, _, fn, seed in batch], ds.pool)
            recs = ds.prepare_many([(wav, row[4].P.tr) for wav, row in zip(wavs, batch)])
            for (cid, split, speaker, kind, ref, lab, mode, fn, seed), P in zip(batch, recs):
                new = run_pair(ref.B, P, dets[mode], ref.regime)
                added, removed = diff_regions(ref, new)
                scores = (ref.scored.overall, new.scored.overall)
                delta = abs(scores[1] - scores[0]) if all(v is not None and np.isfinite(v) for v in scores) else None
                if (cid, mode) not in before:
                    before[(cid, mode)] = eval_clip(ref, lab, secondary_exempt=False)['truth']
                found = [i for i, t in enumerate(before[(cid, mode)]) if t['available'] and t['detected']]
                after = eval_clip(new, lab, secondary_exempt=False)['truth']
                detail.append({'condition': name, 'clip': cid, 'split': split, 'speaker': speaker, 'kind': kind, 'regime': ref.regime,
                               'reference_mode': mode if ref.regime == 'R2' else None, 'seed': seed,
                               'minutes': P.duration / 60, 'added': len(added), 'removed': removed, 'regions_added': added,
                               'abs_score_change': delta, 'participant_recording': cid.split('>')[-1],
                               'found_before_ids': found, 'found_before_keys': [before[(cid, mode)][i]['group'] for i in found],
                               'retained_ids': [i for i in found if after[i]['detected']],
                               'flaws_found_before': len(found), 'flaws_found_after': sum(bool(t['detected']) for t in after if t['available']),
                               'truths': sum(t['available'] for t in after),
                               'compression_reduction_db': stress.compression_reduction(ref.P.wav) if fn == stress.compress else None})
            del wavs, recs
        log(f"stress {name}: {len(pending)} comparisons complete")
    rows = []
    for split, gs in split_groups(splits) + [('check readers', ('check readers',))]:
        for name, _ in matrix:
            for regime, mode in (('R1', None), ('R2', 'single'), ('R2', 'consensus5')):
                records = [r for r in detail if r['split'] in gs and r['condition'] == name and r['regime'] == regime and r['reference_mode'] == mode]
                if not records:
                    continue
                deltas = [r['abs_score_change'] for r in records if r['abs_score_change'] is not None]
                share = key_share(dets[mode or 'single']['regimes'][regime])
                intervals = stress_intervals(records, share)
                retention = intervals['retention_interval']
                units = {r['participant_recording']: r['minutes'] for r in records}
                rows.append({'split': split, 'condition': name, 'regime': regime, 'reference_mode': mode,
                             'recordings': len(units), 'clips': len({r['clip'] for r in records}), 'seeds': sorted({r['seed'] for r in records}),
                             'minutes': sum(r['minutes'] for r in records), 'recording_minutes': sum(units.values()),
                             'added': intervals['added_interval']['events'], 'removed': intervals['removed_interval']['events'],
                             'retained_detections': retention['retained'], 'flaws_found_before': retention['found'],
                             'flaws_found_after': sum(r['flaws_found_after'] for r in records),
                             'unique_detections_before': retention['unique_found'], 'retained_every_seed': retention['retained_every_seed'],
                             'key_share_per_min': share, **intervals,
                             'max_abs_delta_score': max(deltas) if deltas else None, 'measurable_score_pairs': len(deltas),
                             'missing_score_pairs': len(records) - len(deltas)})
    baseline = []
    for cid, split, speaker, kind, ref, _, mode in cases:
        if kind in ('identity', 'null'):
            baseline.append({'clip': cid, 'split': split, 'speaker': speaker, 'reference_mode': mode, 'minutes': ref.P.duration/60, 'flags': ref.n_flags,
                             'by_key': ref.flag_keys, 'scope': 'unperturbed chain; excluded from added/removed counts'})
    table = stress_tables(rows, babble_sources, baseline)
    return {'rows': rows, 'flawed_clips': detail, 'reference': baseline, 'babble_sources': babble_sources, 'forecast': forecast, 'table': table}


def stress_tables(rows: list[dict], babble_sources: dict, baseline: list[dict]) -> str:
    """The stress section's Markdown: the matrix, the limits, the per-key tables, the transforms and the unperturbed reference."""
    table = md_table(['split', 'condition', 'regime', 'reference mode', 'recordings', 'seeds', 'comparison-minutes (all seeds)', 'added/min', 'interval',
                      'removed/min', 'interval', 'detections before (unique)', 'kept (all seeds)', 'kept fraction', 'interval', 'kept in every seed', 'max score change'],
                     [[r['split'], r['condition'], r['regime'], r['reference_mode'], r['recordings'], r['seeds'], r['minutes'],
                       r['added_per_min'], stress_interval(r['added_interval']), r['removed_per_min'], stress_interval(r['removed_interval']),
                       r['unique_detections_before'], f"{r['retained_detections']}/{r['flaws_found_before']}", r['retention'],
                       stress_interval(r['retention_interval']), f"{r['retained_every_seed']}/{r['unique_detections_before']}", r['max_abs_delta_score']] for r in rows])
    table += '\n\nConditions that break keys (stated limits; added local regions above the per-key share of the false-region budget, or detections kept below ' + \
             f'{STRESS_RETENTION_LIMIT:.0%}):\n\n' + md_table(['split', 'condition', 'regime', 'reference mode', 'limit'],
                                                            [[r['split'], r['condition'], r['regime'], r['reference_mode'], v] for r in rows for v in r['limits']])
    table += '\n\nAdded regions per key:\n\n' + md_table(['split', 'condition', 'regime', 'reference mode', 'key', 'added (all seeds)', 'per min', 'interval'],
                                                         [[r['split'], r['condition'], r['regime'], r['reference_mode'], k, v['events'], v['rate'], stress_interval(v)]
                                                          for r in rows for k, v in r['added_by_key'].items()])
    table += '\n\nDetections kept per truth key:\n\n' + md_table(['split', 'condition', 'regime', 'key', 'kept / found (all seeds)', 'fraction', 'interval', 'kept in every seed / unique'],
                                                                [[r['split'], r['condition'], r['regime'], k, f"{v['retained']}/{v['found']}", v['fraction'], stress_interval(v),
                                                                  f"{v['retained_every_seed']}/{v['unique_found']}"] for r in rows for k, v in r['retention_by_key'].items()])
    table += ('\n\nThe result is the measured degradation; there is no pass rule. Rates and kept fractions pool every seed; the seeds of one '
              'recording are not independent trials, so each interval resamples participant recordings (a row with per-speaker values uses speakers as clusters). Babble, compression and phone-band '
              'conditions are not supported invariances. R2 flawed clips use the single-reference mode; the check readers (no injected '
              'flaw, so no retention) are measured with the single and the median-of-five references.\n\nAll transforms affect the '
              'participant only. Synthetic diffuse room RT60=0.4 s; babble uses four other dataset baseline speakers (ids below), seeded '
              'offsets, at 10/20 dB SNR. Phone: 300-3400 Hz, 8 kHz sampling, G.711 mu-law.\n\n')
    table += md_table(['clip', 'babble donor speakers'], [[cid, ids] for cid, ids in sorted(babble_sources.items())])
    table += '\n\nUnperturbed identity-chain/null reference:\n\n' + md_table(['clip', 'split', 'reference mode', 'minutes', 'flags', 'by key'],
                                                                          [[r[k] for k in ('clip', 'split', 'reference_mode', 'minutes', 'flags', 'by_key')] for r in baseline])
    return table


def stress_interval(summary: dict) -> str:
    return interval_text(summary['ci95'], summary['per_cluster'], summary['range'], unit=summary.get('unit', 'recording'))


# ============================================================================================ chain B
def chain_b_clip(rec: Recording, baseline_id: str, typ: str, lv: int):
    """One chain-B clip (Praat PSOLA duration + WORLD pitch): (audio, labels), or None when no span fits (a pool worker runs this)."""
    cid = f"{baseline_id}__chainB_{typ}_L{lv}"
    seed = flaws.clip_seed(f"{baseline_id}__dir_{typ}")
    plan = flaws.plan_clip(rec, [(typ, lv)], seed)
    if not plan.edits:
        return None
    return flaws.inject(rec, plan, cid, baseline_id, recipe=f"chainB_{typ}_L{lv}", seed=seed, chain_name="B")


def chain_b_section(ds: Dataset, det: dict, splits: tuple[str, ...]) -> dict:
    """Both chains render the same single-flaw plan; reuse A's directional recordings."""
    bs = [b for b in ds.manifest["baselines"] if b["split"] in held_out(splits)]
    Bs = dict(zip([b["id"] for b in bs], ds.recs(bs)))
    cells = [(typ, lv, b) for typ in C.CHAIN_B_TYPES for lv in (2, 3) for b in bs]
    made = map_calls(chain_b_clip, [(Bs[b["id"]], b["id"], typ, lv) for typ, lv, b in cells], ds.pool)
    todo = [(cell, m) for cell, m in zip(cells, made) if m is not None]
    Ps = ds.prepare_many([(m[0], ds.transcript(cell[2])) for cell, m in todo])
    reference = getattr(ds, "_directional", {})
    rows = []
    missing = [cell for cell, _ in todo if (cell[2]["id"], cell[0], cell[1]) not in reference]
    made_a = map_calls(directional_clip, [(Bs[b["id"]], b["id"], typ, lv) for typ, lv, b in missing], ds.pool)
    prepared_a = ds.prepare_many([(m[0], ds.transcript(cell[2])) for cell, m in zip(missing, made_a)])
    for cell, m, rec in zip(missing, made_a, prepared_a):
        reference[(cell[2]["id"], cell[0], cell[1])] = (rec, m[1])
    for ((typ, lv, b), (_, lab)), P in zip(todo, Ps):
        a = reference[(b["id"], typ, lv)]
        for chain, rec, labels in (("A", a[0], a[1]), ("B", P, lab)):
            e = eval_clip(run_pair(Bs[b["id"]], rec, det, "R1"), labels, secondary_exempt=False)
            hit = next((t for t in e["truth"] if t["detected"]), {})
            rows.append({"speech": b["id"], "split": b["split"], "type": typ, "level": lv, "chain": chain, "words": labels["flaws"][0]["words"],
                         "TP": sum(t["detected"] for t in e["truth"]), "truths": len(e["truth"]), "false_regions": len(e["false"]),
                         "same_change_duplicates": e["duplicate"],
                         "onset_ms": hit.get("onset_ms"), "offset_ms": hit.get("offset_ms")})
    return {"rows": rows, "table": md_table(["speech", "split", "type", "level", "chain", "words", "TP", "truths", f"false regions ({STRICT_ACCOUNTING})", "same-change duplicates", "onset error (ms)", "offset error (ms)"],
                         [[r[k] for k in ("speech", "split", "type", "level", "chain", "words", "TP", "truths", "false_regions", "same_change_duplicates", "onset_ms", "offset_ms")] for r in rows])}


# ============================================================================================ directional, repair, validity
def labelled_boundary(first_word: int, flaw_type: str) -> int:
    """The pause boundary that an edit changes: a HESITATION inserts its pause before the first labelled word."""
    return first_word - 1 if flaw_type == 'HESITATION' else first_word


def directional_clip(rec: Recording, baseline_id: str, typ: str, lv: int):
    """One single-flaw chain-A clip whose span depends on (speech, type) only, so the three levels edit the same words
    (a pool worker runs this). None when no span fits."""
    seed = flaws.clip_seed(f"{baseline_id}__dir_{typ}")
    plan = flaws.plan_clip(rec, [(typ, lv)], seed)
    if not plan.edits:
        return None
    return flaws.inject(rec, plan, f"{baseline_id}__dir_{typ}_L{lv}", baseline_id, recipe=f"dir_{typ}_L{lv}", seed=seed)


def directional_section(ds: Dataset, det: dict, splits: tuple[str, ...]) -> dict:
    """A higher level never raises the corresponding dimension score (per speech and flaw type, R1). The stored clips place
    each level on different words, so the three levels are generated on the fly on one span, one flaw per clip."""
    bs = [b for b in ds.manifest["baselines"] if b["split"] in splits]
    ds.load(entries=bs)
    Bs = dict(zip([b["id"] for b in bs], ds.recs(bs)))
    cells = [(b, typ, lv) for b in bs for typ in C.FLAW_TYPES for lv in (1, 2, 3)]
    made = map_calls(directional_clip, [(Bs[b["id"]], b["id"], typ, lv) for b, typ, lv in cells], ds.pool)
    todo = [(cell, m) for cell, m in zip(cells, made) if m is not None and m[1]['flaws']]
    skipped = [{'speech': b['id'], 'type': typ, 'level': lv, 'reason': 'no realised edit'}
               for (b, typ, lv), m in zip(cells, made) if m is None or not m[1]['flaws']]
    Ps = ds.prepare_many([(m[0], ds.transcript(cell[0])) for cell, m in todo])
    sc: dict[tuple, dict[int, float]] = {}
    cells: dict[tuple, dict[int, tuple]] = {}
    pause_missing = set()
    ds._directional = {}
    for ((b, typ, lv), (_, lab)), P in zip(todo, Ps):
        run = run_pair(Bs[b["id"]], P, det, "R1")
        f = lab["flaws"][0]
        sc.setdefault((b["id"], typ), {})[lv] = run.scored.S.get(f["dimension"])
        # Only the comparison and the flags: the recordings of every level and type would hold their audio in memory.
        cells.setdefault((b["id"], typ), {})[lv] = (SimpleNamespace(comp=run.comp, regions=run.regions, clip=run.clip), f)
        if typ in C.CHAIN_B_TYPES and lv in (2, 3) and b["split"] in held_out(splits):
            ds._directional[(b["id"], typ, lv)] = (P, lab)
        if f["dimension"] == "D2":
            values, w = run.comp.dims['D2'].x, labelled_boundary(f['words'][0], typ)
            value = values[w] if w < len(values) else np.nan
            realised = f["realised"]["value"]
            if not np.isfinite(value) or (realised is not None and abs(value) < C.PAUSE_DIAGNOSIS_FRACTION * abs(realised)):
                pause_missing.add((b["id"], typ))
    cause = {k: directional_cause(cells[k], k in pause_missing)
             for k, v in sc.items() if len(v) == 3 and all(x is not None for x in v.values()) and not (v[1] >= v[2] >= v[3])}
    speech_split = {b["id"]: b["split"] for b in bs}
    bad = [{"speech": k[0], "split": speech_split[k[0]], "type": k[1], "scores": sc[k], "cause": c} for k, c in cause.items()]
    return {"cells": len(sc), "violations": bad, "skipped": skipped, "table": md_table(["speech", "split", "type", "L1", "L2", "L3", "cause"],
                                                                     [[k[0], speech_split[k[0]], k[1], *(None if v.get(i) is None else round(v[i], 1) for i in (1, 2, 3)), cause.get(k, "no detector" if C.FLAW_DIM[k[1]] not in C.DIMS else "")] for k, v in sorted(sc.items())])}


def non_decreasing(values) -> bool:
    return all(a <= b + 1e-9 for a, b in zip(values, values[1:]))


def charged_elsewhere(run, f: dict) -> bool:
    """A region of the edit's dimension on its words is a member of a cause group whose penalty another dimension or a
    whole-clip flag carries (one change, one penalty: patterns.groups)."""
    from .patterns import groups, within_half_window
    regions = run.regions
    for g in groups(run.comp, regions, run.clip):
        if not g.cause:
            continue
        owner = g.anchor if isinstance(g.anchor, str) or g.anchor is None else regions[g.anchor].dim
        if any(regions[j].dim == f['dimension'] and owner != f['dimension'] and within_half_window(regions[j], f['words'])
               for j in g.members if j != g.anchor):
            return True
    return False


def directional_cause(cells: dict[int, tuple], pause_missing: bool) -> str:
    """The named cause of a directional violation; cells {level: (run, flaw label)}. In order: the pause was not measured;
    the penalty of a level moved to the linked dimension of the change; the realised edit (label) or the measured change
    (median |x| of the dimension over the edited words) is not monotone across levels; else 'other'."""
    if pause_missing:
        return "pause not measured at the labelled boundary"
    levels = sorted(cells)
    if any(charged_elsewhere(*cells[lv]) for lv in levels[1:]):
        return "penalty charged to the change's linked dimension or whole-clip flag (one change, one penalty)"
    realised = [cells[lv][1].get("realised", {}).get("value") for lv in levels]
    if all(isinstance(v, (int, float)) and np.isfinite(v) for v in realised) and not non_decreasing([abs(v) for v in realised]):
        return "realised edit not monotone across levels"
    measured = []
    for lv in levels:
        run, f = cells[lv]
        x = run.comp.dims[f["dimension"]].x[f["words"][0]:f["words"][-1] + 1] if f["dimension"] in run.comp.dims else np.array([])
        measured.append(float(np.nanmedian(np.abs(x))) if np.isfinite(x).any() else np.nan)
    if np.isfinite(measured).all() and not non_decreasing(measured):
        return "measured change not monotone across levels"
    return "other"


def repair_audio(run: Run, r: Region, placebo: bool) -> np.ndarray | None:
    """Inverse edit of a flagged region built from the system's own measured delta (placebo: null parameters, same span)."""
    P, d, pk = run.P, run.comp.dims[r.dim], r.peak
    x = P.wav.copy()
    N = len(x)
    a = max(int(round(P.regions[r.i0, 0] * C.SR)), 0)
    b = min(int(round(P.regions[r.i1, 1] * C.SR)), N)
    if r.dim == "D1":
        rate = 1.0 if placebo else math.exp(float(d.x[pk]))
        return flaws.stretch_speech(x, a, b, rate, flaws.parent_pauses(P))[0]
    if r.dim == "D2" and r.sign < 0:
        n = 0 if placebo else int(round((d.b[pk] - d.p[pk]) * C.SR))
        i = int(round(0.5 * (P.al.end[r.i0] + P.al.start[r.i0 + 1]) * C.SR))
        return flaws.insert_pause(x, i, n, flaws.room_tone(P))[0] if n > 0 else x
    if r.dim == "D2":
        s, e = P.sil_span[r.i0]
        if not np.isfinite(s):
            return None
        p0, p1 = int(round(s * C.SR)), int(round(e * C.SR))
        keep = int(round(C.PAUSE_FLOOR_S * C.SR))
        return x if placebo or p1 - p0 <= keep else flaws.remove_pause(x, p0, p1, keep)[0]
    if r.dim == "D5":
        t = np.arange(N) / C.SR
        gain = 0.0 if placebo else abs(float(d.x[pk]))
        return x * 10 ** (gain * flaws._ramp_window(t, a / C.SR, b / C.SR, 0.05) / 20)
    if r.dim == "D3":
        k = float(d.p[pk] / d.b[pk]) if d.b[pk] else 1.0
        return flaws.flatten_span(x, a, b, 0.0 if placebo else min(0.0, 1.0 - 1.0 / max(k, 0.05)))
    return None


def repair_section(ds: Dataset, det: dict, splits: tuple[str, ...]) -> dict:
    """Repair test: the inverse edit removes the flag; a placebo edit on the same span leaves it (held-out, L2, invertible
    types). Flags are compared by word index: the repaired clip has a different length. All repairs are generated first (parallel),
    analysed in one batch, then scored."""
    wanted = ("RUSH", "DRAG", "PAUSE_DROPPED", "PAUSE_INTRUSIVE", "FADE", "MONOTONE")
    held = held_out(splits)
    todo = []  # (clip id, split, truth type, run, region)
    for c, run, lab in clip_runs(ds, det, [c for c in ds.clips(kind="single", level=2) if c["split"] in held]):
        tr = truths(lab)
        for ti, rj in match(tr, run).items():
            if tr[ti]["type"] in wanted:
                todo.append((c["id"], c["split"], tr[ti]["type"], run, run.regions[rj]))
    fade_speeches = {cid.split("__")[0] for cid, _, typ, _, _ in todo if typ == "FADE"}
    for c, run, lab in clip_runs(ds, det, [c for c in ds.clips(kind="single", level=3) if c["split"] in held and "FADE" in c["types"] and c["parent"] not in fade_speeches]):
        tr = truths(lab)
        for ti, rj in match(tr, run).items():
            if tr[ti]["type"] == "FADE":
                todo.append((c["id"], c["split"], "FADE", run, run.regions[rj]))
    jobs = [(run, r, placebo) for _, _, _, run, r in todo for placebo in (False, True)]
    audios = map_calls(repair_audio, jobs, ds.pool)
    keep = [(i, y) for i, y in enumerate(audios) if y is not None]
    recs = dict(zip([i for i, _ in keep], ds.prepare_many([(audio.quantize(y), jobs[i][0].P.tr) for i, y in keep])))
    rows = []
    for k, (cid, split, typ, run, r) in enumerate(todo):
        row = {"clip": cid, "split": split, "type": typ, "words": [r.i0, r.i1], "repaired": None, "placebo_kept": None,
               "score_before": run.scored.overall, "score_after": None, "new_flags": None, "attempts": []}
        for placebo, name in ((False, "repaired"), (True, "placebo_kept")):
            i = 2 * k + int(placebo)
            if i not in recs:
                row["attempts"].append({"placebo": placebo, "flag_removed": None, "score_before": run.scored.overall, "score_after": None, "new_flags": None, "error": "inverse edit unavailable"})
                continue
            new = run_pair(run.B, recs[i], det, "R1")
            still = any(overlaps(q, r) for q in new.regions)
            row[name] = (not still) if name == "repaired" else still
            added = diff_regions(run, new)[0]
            row["attempts"].append({"placebo": placebo, "flag_removed": not still, "score_before": run.scored.overall,
                                    "score_after": new.scored.overall, "new_flags": added})
            if not placebo:
                row["score_after"], row["new_flags"] = new.scored.overall, added
        rows.append(row)
    summ = {}
    for sp, gs in split_groups(held):
        sel = [r for r in rows if r["split"] in gs]
        summ[sp] = {t: {"n": sum(r["type"] == t for r in sel), "repaired": sum(bool(r["repaired"]) for r in sel if r["type"] == t),
                       "placebo_kept": sum(bool(r["placebo_kept"]) for r in sel if r["type"] == t)} for t in wanted}
    return {"rows": rows, "by_type": summ, "table": md_table(["split", "type", "flags tested", "removed by repair", "kept after placebo"],
                                                              [[sp, t, v["n"], v["repaired"], v["placebo_kept"]] for sp, types in summ.items() for t, v in types.items()]) + "\n\n" +
            md_table(["clip", "split", "type", "placebo", "flag removed (word index)", "score before", "score after", "new flags", "error"],
                     [[r["clip"], r["split"], r["type"], a["placebo"], a["flag_removed"], a["score_before"], a["score_after"], a["new_flags"], a.get("error", "")]
                      for r in rows for a in r["attempts"]])}


def applied_word_time_ln(f: dict) -> float:
    """ln of the word-time ratio a word-compression edit applied, from the label's own sample counts: output samples over
    parent samples of its stretch events (pauses excluded). Independent of the detector."""
    stretch = [e for e in f.get('events', []) if e.get('kind') == 'stretch' and 'output_samples' in e and 'parent_span' in e]
    parent = sum(e['parent_span'][1] - e['parent_span'][0] for e in stretch)
    output = sum(e['output_samples'] for e in stretch)
    return math.log(output / parent) if parent > 0 and output > 0 else float('nan')


INDEPENDENT_REALISED = {'NATURAL_RUSH': applied_word_time_ln}  # recipe families with a realised measure not taken by the detector


def span_realised(run: Run, f: dict) -> float:
    """Re-measure the edit support with the same extractor; internal consistency, not accuracy. Recipe families without an
    independent measure (INDEPENDENT_REALISED) return the detector's own median, which is circular."""
    if f['type'] in INDEPENDENT_REALISED:
        return INDEPENDENT_REALISED[f['type']](f)
    if f['type'] in C.EXTRA_TYPES:
        dim = C.FLAW_DIM[f['type']]
        if dim not in C.DIMS:
            return float('nan')
        d = run.comp.dims[dim]
        if C.FLAW_REGISTRY[f['type']]['event'] == 'clip':
            return float(d.g)
        if C.is_event(dim):
            w = labelled_boundary(f['words'][0], f['type'])
            return float(d.x[w]) if 0 <= w < len(d.x) else float('nan')
        return float(np.nanmedian(d.x[f['words'][0]:f['words'][-1] + 1]))
    typ, w = f["type"], f["words"][0]
    if typ.startswith("PAUSE"):
        return float(run.P.sil_raw[w] - run.B.sil_raw[w]) if w < len(run.P.sil_raw) else float('nan')
    if typ == "DEEMPHASIS":
        return float(run.comp.pts_p[w] - run.comp.pts_b[w])
    vals = []
    for rec, span in ((run.B, f["parent_span"]), (run.P, f["span"])):
        a, b = np.asarray(span) / C.SR
        if typ in ("RUSH", "DRAG"):
            pauses = rec.sil_span
            lengths = np.maximum(0, np.minimum(b, pauses[:, 1]) - np.maximum(a, pauses[:, 0]))
            vals.append(max(b - a - np.nansum(lengths), 1e-6))
            continue
        times = np.arange(len(rec.fr)) * C.HOP_S
        mask = (times >= a) & (times < b)
        if typ == "MONOTONE":
            pitch = rec.fr.S[mask & rec.fr.voiced]
            vals.append(float(np.percentile(pitch, 90) - np.percentile(pitch, 10)) + C.RANGE_REG_ST - 1e-6 if pitch.size else np.nan)
        else:
            for ps, pe in rec.sil_span:
                if np.isfinite(ps + pe):
                    mask &= ~((times >= ps) & (times < pe))
            vals.append(float(np.mean((rec.fr.E if typ == "FADE" else rec.fr.Q)[mask])) if mask.any() else np.nan)
    return float(np.log((vals[1] + 1e-6) / (vals[0] + 1e-6))) if typ in ("RUSH", "DRAG", "MONOTONE", "MUMBLE") else vals[1] - vals[0]


def validity_section(ds: Dataset, det: dict, splits: tuple[str, ...]) -> dict:
    """Internal consistency: recipe setting, span extraction, and detector delta at the labelled unit, per split, type and level (R1).
    Pauses: the labelled boundary. Windowed types: finite measurements whose word centres lie inside the edited span,
    including edge windows diluted by unedited words."""
    rows, detail = [], []
    unit_dim = C.FLAW_DIM
    acc: dict[tuple, list] = {}
    for c, run, lab in clip_runs(ds, det, [c for c in ds.clips(kind="single") if c["split"] in splits]):
        for f in lab["flaws"]:
            if f["type"] not in unit_dim:
                continue
            if unit_dim[f["type"]] not in run.comp.dims:
                detail.append({"clip": c["id"], "split": c["split"], "type": f["type"], "level": f["level"],
                               "recipe_setting": f.get("parameter"), "realised": f["realised"], "status": "no detector"})
                continue
            d = run.comp.dims[unit_dim[f["type"]]]
            w0, w1 = f["words"]
            if C.FLAW_REGISTRY[f['type']]['event'] == 'clip':
                meas = [float(d.g)] if np.isfinite(d.g) else []
            elif C.UNIT_KIND[d.key] == 'boundary':
                boundary = labelled_boundary(w0, f["type"])
                meas = [float(run.P.sil_raw[boundary] - run.B.sil_raw[boundary])] if 0 <= boundary < len(run.P.sil_raw) else []
            elif C.is_event(d.key):
                meas = [float(d.x[w0])] if np.isfinite(d.x[w0]) else []
            else:
                meas = [float(x) for x in d.x[w0:w1 + 1] if np.isfinite(x)]
            realised = span_realised(run, f)
            measured = float(np.median(meas)) if meas else np.nan
            detail.append({"clip": c.get("id"), "split": c["split"], "type": f["type"], "level": f["level"],
                           "recipe_setting": C.LEVEL_PARAM[f["type"]][f["level"] - 1],
                           "realised": float(realised) if np.isfinite(realised) else None,
                           "detector_measurement": measured if np.isfinite(measured) else None})
            if np.isfinite(realised) and np.isfinite(measured):
                acc.setdefault((c["split"], f["type"], f["level"]), []).append((realised, measured))
    for sp, gs in split_groups(splits):
        for t in C.FLAW_TYPES:
            for lv in C.LEVELS:
                v = [pair for s in gs for pair in acc.get((s, t, lv), [])]
                inj, mea = np.array([a for a, _ in v]), np.array([b for _, b in v])
                ratios = mea[inj != 0] / inj[inj != 0]
                independent = t in C.CORE8_TYPES or t in INDEPENDENT_REALISED
                rows.append([sp, t, lv, len(v), C.LEVEL_PARAM[t][lv - 1], 'independent' if independent else 'circular (detector measure)',
                             float(np.median(inj)) if v else None, float(np.median(mea)) if v else None,
                             float(np.median(ratios)) if ratios.size and independent else None])
    pending = Counter((r["split"], r["type"], r["level"]) for r in detail if r.get("status") == "no detector")
    tab = md_table(["split", "type", "level", "n", "recipe setting", "realised measure", "realised (recipe metric units)",
                    "detector measurement (dimension units; window centres inside the span)", "median of paired ratios (independent measures only)"], rows)
    recovery = [{'split': r[0], 'level': r[2], 'n': r[3], 'applied_word_time_ln': r[6], 'd9_measured_ln': r[7], 'recovered_share': r[8]}
                for r in rows if r[1] == 'NATURAL_RUSH']
    tab += ('\n\nThe table is circular for the recipe families marked "circular": their realised value is the detector\'s own '
            'measurement, so it cannot show that the detector measures the edit. NATURAL_RUSH realised is independent: the applied '
            'word-time ln ratio from the label\'s stretch sample counts (pauses excluded); its paired ratio is the share of the '
            'applied compression that D9 recovers:\n\n' + md_table(
                ['split', 'level', 'n', 'applied word time (ln)', 'D9 measured (ln)', 'median share recovered'],
                [[r[k] for k in ('split', 'level', 'n', 'applied_word_time_ln', 'd9_measured_ln', 'recovered_share')] for r in recovery]))
    tab += "\n\n" + md_table(["split", "type", "level", "count", "status"],
                              [[sp, t, lv, n, "no detector"] for (sp, t, lv), n in sorted(pending.items())])
    return {"rows": rows, "detail": detail, "natural_rush_recovery": recovery,
            "no_detector": dict((f"{sp}/{t}/L{lv}", n) for (sp, t, lv), n in pending.items()), "table": tab}


def repro_task(wav: np.ndarray, tr, bwav: np.ndarray, det: dict, device: str) -> tuple[bool, int]:
    """Two full analyze() runs (alignment included, no cache) on this process's aligner: (identical, bytes)."""
    al = worker_aligner()
    a = dumps(analyze(wav, tr, bwav, regime="R1", detector=det, aligner=al, alignment_device=device))
    b = dumps(analyze(wav, tr, bwav, regime="R1", detector=det, aligner=al, alignment_device=device))
    return a == b, len(a)


def reproducibility_section(ds: Dataset, det: dict, splits: tuple[str, ...]) -> dict:
    """Two runs of analyze() on one held-out flawed clip give byte-identical JSON."""
    held = held_out(splits) or splits
    c = next(c for c in ds.clips(kind="single", level=3) if c["split"] in held)
    B = ds.entry("baselines", c["parent"])
    same, n = map_calls(repro_task, [(ds.wav(c), ds.clip_transcript(c), ds.wav(B), det, device_class(ds.pool))], ds.pool)[0]
    return {"clip": c["id"], "identical": same, "bytes": n}


# ============================================================================================ device agreement
def device_section(ds: Dataset, det: dict, splits: tuple[str, ...]) -> dict:
    """GPU versus CPU alignment of a handful of held-out clips (and their baselines): maximum word-time difference in ms and
    whether the flags are identical. Skipped on CPU-only runs. Both sides use fresh single-worker pools without the alignment cache."""
    if ds.pool is None or ds.pool.device_class != "cuda":
        return {"skipped": "no GPU in this run: nothing to compare", "table": "Skipped: this run used no GPU."}
    held = held_out(splits) or splits
    by_split = [sorted([c for c in ds.clips(kind="single") if c["split"] == sp], key=lambda c: c["id"]) for sp in held]
    clips = [cs[i] for i in range(C.DEVICE_AGREEMENT_CLIPS) for cs in by_split if i < len(cs)][:C.DEVICE_AGREEMENT_CLIPS]
    bs = {c["parent"]: ds.entry("baselines", c["parent"]) for c in clips}
    items = [(ds.wav(b), ds.transcript(b)) for b in bs.values()] + [(ds.wav(c), ds.clip_transcript(c)) for c in clips]
    jobs = [make_job(w, tr) for w, tr in items]
    out = {}
    for name, dev in (("gpu", ds.pool.devices[0]), ("cpu", "cpu")):
        with PreparePool(workers=1, devices=[dev]) as p:  # no cache_dir: both sides really align
            out[name] = p.map(jobs)
    nb = len(bs)
    diffs, agreement = [], []
    for i in range(len(jobs)):
        g, c = out["gpu"][i].al, out["cpu"][i].al
        diffs.append(max(float(np.max(np.abs(g.start - c.start))), float(np.max(np.abs(g.end - c.end)))) * 1000.0)
    for k, cl in enumerate(clips):
        j = nb + k
        bi = list(bs).index(cl["parent"])
        flags = []
        for name in ("gpu", "cpu"):
            run = run_pair(out[name][bi], out[name][j], det, "R1")
            flags.append((sorted((r.dim, r.sign, r.i0, r.i1) for r in run.regions), sorted(clip_key(k, g) for k, g in run.clip.items())))
        agreement.append(flags[0] == flags[1])
    rows = []
    for split, gs in split_groups(held):
        selected = [i for i, c in enumerate(clips) if c["split"] in gs]
        indices = sorted({list(bs).index(clips[i]["parent"]) for i in selected} | {nb + i for i in selected})
        ds_diffs = [diffs[i] for i in indices]
        rows.append({"split": split, "gpu_device": ds.pool.devices[0], "clips": len(selected), "recordings": len(indices),
                     "max_word_time_diff_ms": round(max(ds_diffs), 1) if ds_diffs else None,
                     "median_recording_max_diff_ms": round(float(np.median(ds_diffs)), 1) if ds_diffs else None,
                     "flags_identical": all(agreement[i] for i in selected) if selected else None})
    return {"rows": rows, "table": md_table(["split", "GPU", "clips", "recordings aligned", "max word-time difference (ms)", "flags identical"],
                       [[r["split"], r["gpu_device"], r["clips"], r["recordings"], r["max_word_time_diff_ms"], r["flags_identical"]] for r in rows])}


# ============================================================================================ figures
OKABE = {"RUSH": "#0072B2", "DRAG": "#56B4E9", "PAUSE_DROPPED": "#E69F00", "PAUSE_INTRUSIVE": "#D55E00", "MONOTONE": "#009E73",
         "DEEMPHASIS": "#CC79A7", "FADE": "#444444", "MUMBLE": "#999999"}
OKABE.update({t: OKABE.get(C.FLAW_DIM[t], ('#0072B2', '#E69F00', '#009E73', '#CC79A7')[i % 4]) for i, t in enumerate(C.EXTRA_TYPES)})


def figures(res: dict, out: Path) -> list[str]:
    """Held-out figures only (val, test, or val+test): train is never pooled into them."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out.mkdir(parents=True, exist_ok=True)
    written = []
    plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25, "font.size": 9})
    held = held_out(tuple(res["splits"]))
    gname = "+".join(held)
    mag = [m for m in res.get("headline", {}).get("magnitude", []) if m["split"] in held]
    if mag:
        measured_types = [t for t in C.FLAW_TYPES if any(m['type'] == t and m.get('realised', {}).get('value') is not None for m in mag)]
        if measured_types:
            fig, axes = plt.subplots(math.ceil(len(measured_types)/4), 4, figsize=(12, 2.2 * math.ceil(len(measured_types)/4)), squeeze=False)
            for ax, typ in zip(axes.flat, measured_types):
                values = [m for m in mag if m['type'] == typ and m.get('realised', {}).get('value') is not None and m['detected'] is not None]
                ax.scatter([m['realised']['value'] for m in values], [int(m['detected']) for m in values], s=16, color=OKABE[typ])
                ax.set(title=typ, xlabel=values[0]['realised'].get('unit', '') if values else '', yticks=[0,1], ylabel='detected', ylim=(-.1,1.1))
            for ax in list(axes.flat)[len(measured_types):]:
                ax.set_visible(False)
            fig.tight_layout()
            fig.savefig(out / 'detection_vs_realised.png', dpi=140)
            plt.close(fig)
            written.append('detection_vs_realised.png')
        fig, ax = plt.subplots(figsize=(6.5, 3.8))
        for typ in C.FLAW_TYPES:
            ys = []
            for lv in C.LEVELS:
                sel = [m["detected"] for m in mag if m["type"] == typ and m["level"] == lv and m["detected"] is not None]
                ys.append(100 * sum(sel) / len(sel) if sel else np.nan)
            ax.plot(C.LEVELS, ys, marker="o", lw=1.5, color=OKABE.get(typ), label=typ)
        ax.set(xticks=C.LEVELS, xlabel="nominal level (eligible realised edits only)", ylabel=f"detected (% of injected flaws, {gname} speeches)", ylim=(-3, 103),
               title=f"Detection rate by level, R1, chain A ({gname})")
        ax.legend(fontsize=7, ncol=2, frameon=False)
        fig.tight_layout()
        fig.savefig(out / "detection_vs_level.png", dpi=140)
        plt.close(fig)
        written.append("detection_vs_level.png")
    rows = res.get("nulls", {}).get("rows")
    if rows:
        fig, ax = plt.subplots(figsize=(6.5, 3.2))
        labels = [r[0].split(":")[0].split(" (")[0] for r in rows]
        ax.barh(range(len(rows)), [r[3] or 0 for r in rows], color="#0072B2", height=0.55)
        for i, r in enumerate(rows):
            ax.text((r[3] or 0) + 0.01, i, f"{r[1]} regions / {r[2]} min" if r[3] is not None or r[1] == 0 else str(r[1]), va="center", fontsize=7)
        ax.set(yticks=range(len(rows)), yticklabels=labels, xlabel="observed false regions per comparison-minute", title="Nulls not used for fitting (train operating target 0.50 / min)")
        ax.axvline(C.FALSE_RATE_BUDGET, color="#D55E00", lw=1, ls="--")
        ax.invert_yaxis()
        fig.tight_layout()
        fig.savefig(out / "false_regions_per_minute.png", dpi=140)
        plt.close(fig)
        written.append("false_regions_per_minute.png")
    act = res.get("headline", {}).get("activation", {}).get(gname)
    if act:
        keys = sorted(act)
        m = np.array([[act[k].get(d, 0) for d in C.DIMS] for k in keys], dtype=float)
        fig, ax = plt.subplots(figsize=(4.8, 3.2))
        im = ax.imshow(m, cmap="Blues")
        ax.set(xticks=range(len(C.DIMS)), xticklabels=C.DIMS, yticks=range(len(keys)), yticklabels=keys, xlabel="fired dimension", ylabel="injected dimension",
               title=f"Activation matrix (L2 + L3, {gname})")
        ax.grid(False)
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                ax.text(j, i, int(m[i, j]), ha="center", va="center", fontsize=8, color="white" if m[i, j] > m.max() / 2 else "#222")
        fig.colorbar(im, ax=ax, fraction=0.046)
        fig.tight_layout()
        fig.savefig(out / "activation_matrix.png", dpi=140)
        plt.close(fig)
        written.append("activation_matrix.png")
    return written


# ============================================================================================ run
SECTIONS = [("nulls", null_section), ("headline", headline_section), ('realisation_shortfalls', shortfall_section), ("ladder", ladder_section), ("cross_speaker", cross_section), ("cross_botched", botched_section),
            ("trivial", trivial_section),
            ("stress", stress_section), ("directional", directional_section), ("chain_b", chain_b_section), ("repair", repair_section),
            ("validity", validity_section), ("reproducibility", reproducibility_section), ("device_agreement", device_section)]


def final_gate(models: Path, det: dict, splits: tuple[str, ...], device: str, force: bool, manifest: Path) -> None:
    """The test split and the R2 lockbox are evaluated once per config hash: record the hash (beside detector.json) before
    any test or lockbox number exists, and refuse a repeat unless forced."""
    manifest_hash = sha256_file(manifest)
    if manifest_hash != det.get("report", {}).get("manifest_sha256"):
        raise RuntimeError("dataset manifest hash differs from calibration; final evaluation refused")
    project = ROOT / "project_sha256.txt"
    hashes = {"manifest_sha256": manifest_hash, "project_sha256": sha256_file(project) if project.exists() else None,
              "detector_sha256": sha256_file(models)}
    path = Path(models).parent / FINAL_LOG
    seen = json.loads(path.read_text()) if path.exists() else {}
    config_sha256 = det["config_sha256"]
    if config_sha256 in seen and not force:
        raise RuntimeError(f"the test split was already evaluated for config {config_sha256[:12]} ({seen[config_sha256]}); --force repeats it knowingly")
    seen[config_sha256] = {**hashes, "history": seen.get(config_sha256, {}).get("history", []) + [hashes], "splits": list(splits),
                           "r2_lockbox_modes": ["single", "consensus5"], "alignment_device": device,
                           "runs": seen.get(config_sha256, {}).get("runs", 0) + 1}
    path.write_text(json.dumps(seen, indent=1, sort_keys=True) + "\n")


def run(dataset: Path, models: Path, cache: Path | None, out: Path, splits: tuple[str, ...] = DEFAULT_SPLITS, final: bool = False,
        force: bool = False, pool=None, aligner=None) -> dict:
    if "test" in splits and not final:
        raise ValueError("the test split is evaluated only with --final (once per config hash)")
    if final:
        splits = tuple(dict.fromkeys(splits + ("test",)))
    det = load_detector(models)
    device = device_class(pool)
    ds = load_dataset(dataset, cache, pool, aligner)
    if final:
        final_gate(models, det, splits, device, force, ds.root / "manifest.json")
    sample_sizes = {}
    for split, gs in split_groups(splits):
        clips = [c for c in ds.clips(kind="single") if c["split"] in gs]
        counts = Counter((f["type"], f["level"]) for c in clips for f in ds.labels(c)["flaws"] if not f.get("placebo"))
        sample_sizes[split] = {"speakers": len({c["parent"] for c in clips}), "clips": len(clips),
                               "trials_per_type_level": {typ: {str(lv): counts[(typ, lv)] for lv in C.LEVELS} for typ in C.FLAW_TYPES}}
    res: dict = {"detector_config_sha256": det["config_sha256"], "alignment_device": device, "splits": list(splits), "final": final,
                 "n": sample_sizes, "registry_version": C.REGISTRY_VERSION, "calibration_policy": calibration_policy(), "exemptions": exemption_policy(), "expectation_table": EXPECTED, "errors": {}}
    res['real_validation'] = det.get('report', {}).get('real_validation', {})
    try:
        log(f"splits {list(splits)}{' (final: test included)' if final else ''}; analysing every clip the sections need")
        warm(ds, splits)
    except Exception:
        res["errors"]["warm"] = traceback.format_exc()
        log(f"warm-up FAILED\n{res['errors']['warm']}")
    for name, fn in (*SECTIONS, ("promotion", promotion_section), *((("lockbox", lockbox_section),) if final else ())):
        log(name)
        try:
            res[name] = fn(ds, det, splits)
        except Exception:
            res["errors"][name] = traceback.format_exc()
            log(f"{name} FAILED\n{res['errors'][name]}")
    ev = out / "eval"
    ev.mkdir(parents=True, exist_ok=True)
    try:
        res["figures"] = figures(res, ev / "figures")
    except Exception:
        res["errors"]["figures"] = traceback.format_exc()
    (ev / "tables.md").write_text(tables_markdown(res))
    (ev / "results.json").write_text(json.dumps(res, indent=1, sort_keys=True, default=lambda o: o.item() if hasattr(o, "item") else str(o)) + "\n")
    return res


def preregistered_note(groups: dict, levels: tuple[str, ...], splits: tuple[str, ...]) -> str:
    """The detector's core8 rows under the pre-registered accounting, printed before a table that gives its count-once F1."""
    rows = [r for r in groups['core8']['by_split_strict'] if r['group'] == 'all' and r['levels'] in levels and r['split'] in splits]
    parts = [f"{r['split']} {r['levels']} {p['tp']}/{p['fp']}/{p['fn']}, F1 {md_cell(p['f1'])}" for r in rows for p in [pre_registered(r)]]
    return (f"Detector, core8, TP/FP/FN under the accounting the evaluation plan fixed ({PRE_REGISTERED}): "
            + "; ".join(parts) + f". The detector F1 in the next table counts one detection per change ({STRICT_ACCOUNTING}), "
            "an accounting adopted after the plan.")


def tables_markdown(res: dict) -> str:
    """tables.md from the saved results only (evaluate.run, and `python -m cvoice.evaluate render` for a saved results.json). The
    headline F1 table is rebuilt from the saved per-split rows; every other table is the saved text, with raw floats
    formatted by format_floats."""
    expected = {regime: {int(lv): v for lv, v in table.items()} for regime, table in res["expectation_table"].items()}
    md = ["# Evaluation tables", "", (f"Detector config {res['detector_config_sha256']}. Splits {', '.join(res['splits'])}; alignment on {res['alignment_device']}. Regimes are never pooled and "
          "train is never pooled with validation or test; counts are k of n; exposure beside every rate."), "",
          "## Sample sizes (evaluated single-level clips)", "", md_table(["split", "speakers", "clips", "type", "level", "trials"],
              [[sp, n["speakers"], n["clips"], typ, lv, count] for sp, n in res['n'].items()
               for typ, levels in n["trials_per_type_level"].items() for lv, count in levels.items()]), "",
          "## Expectation table (fixed before evaluation)", "", md_table(["level", "R1 same performance", "R2 different speaker"],
                                                                       [[lv, expected["R1"][lv], expected["R2"][lv]] for lv in C.LEVELS]), ""]
    md += ["Development limits: train F1 is in-sample; val has two reused speakers. All baseline speeches are US political addresses; R2 positives use Gettysburg. Earlier test speakers were used before redesign. " +
           ("This final evaluation measures the test split and the R2 lockbox once for this detector config. " if res['final'] else "This run leaves test and lockbox untouched. ") +
           f"F1 intervals resample source speakers only with at least {MIN_BOOTSTRAP_CLUSTERS} speakers (train); with fewer (val, test, val+test) the tables give each speaker's value and the range, which is not a confidence interval. k/n intervals use Wilson and do not remove shared-reference dependence. No blinded listening check has been completed.", "", "Calibration policy: " + json.dumps(res["calibration_policy"], sort_keys=True), "", "Frozen secondary exemptions: " + json.dumps(res["exemptions"], sort_keys=True), "",
           "Count-once rule as the code applies it (the frozen scope text above states only the duplicate case): " + COUNT_ONCE_RULE, ""]
    md += ['## Real-data lab evidence', '', 'Lab-passed natural-rush text and filled-pause candidate labels do not establish product event accuracy. Synthetic-only families remain unvalidated; filled pause has no synthetic recipe.', '',
           json.dumps(res['real_validation'], sort_keys=True), '']
    h = res.get("headline")
    if h:
        if "groups" in h:
            rest = h["table_f1"][h["table_f1"].index("\n\n"):]
            v9 = sorted({(r["split"], r["levels"]) for r in h.get("dev_v9_change", {}).get("rows", [])})
            if v9:
                note = preregistered_note(h["groups"], tuple({lv for _, lv in v9}), tuple({sp for sp, _ in v9}))
                rest = rest.replace("Change against dev_v9", note + "\n\nChange against dev_v9", 1)
            h = {**h, "table_f1": f1_table(h["groups"]) + rest}
        for k, t in (("table_f1", "Recovery of the synthetic edit: R1 event F1 (unmatched whole-clip flags count as false; windows IoU >= 0.5, D7/D8 both edges within 0.20 s, other events by labelled index or time)"),
                     ("table_overlap", "Overlap view (a flaw counts as found when a flag of its dimension lies on it)"), ("table_per_speech", "Per speech, k of n (L2 + L3)"),
                     ("table_clip", "Whole-clip flags on flawed clips"), ("table_pause", "Pause localisation error (matched boundary events)"),
                     ("table_onset", "Onset / offset absolute error of matched regions (FADE late onset is expected)"),
                     ("table_matching", "D7/D8 both-edges matching beside index or overlap"), ("table_truth_counts", "Label groups and event truth counts"),
                     ("table_magnitude", "Recovery of the synthetic edit: detection versus magnitude"), ("table_activation", "Activation matrix")):
            md += [f"## {t}", "", h[k], ""]
    titles = {"promotion": "Select-set promotion and PPV at the stated base rate", "nulls": "False flags per minute on nulls", "ladder": "Score by rung of the bad spectrum (R1)",
              'realisation_shortfalls': 'Excluded realisation shortfall stratum',
              "cross_speaker": "Cross-speaker flawed pairs, flawed minus clean (R2)",
              "cross_botched": "Cross-speaker whole-clip detection (R2): graded whole-passage edits and botched readings",
              "trivial": "Trivial baselines (L2 + L3, splits not used for fitting)", "stress": "Stress matrix", "chain_b": "Chain A versus chain B",
              "directional": "Directional test: a higher level never raises the dimension score", "repair": "Repair test (inverse edit vs placebo)",
              "validity": "Feature internal consistency", "device_agreement": "Device agreement: GPU versus CPU alignment",
              "lockbox": "R2 lockbox false regions (final evaluation, both modes)"}
    groups = (res.get("headline") or {}).get("groups")
    for k, t in titles.items():
        if k not in res:
            continue
        table = res[k]["table"]
        if k == "trivial" and groups:
            table = preregistered_note(groups, ("headline (L2+L3)",), ("val", "test", "val+test")) + "\n\n" + table
        if k == "stress" and res[k].get("flawed_clips"):
            table = stress_tables(speaker_stress_rows(res[k]), res[k]["babble_sources"], res[k]["reference"])
        md += [f"## {t}", "", table, ""]
    if res.get("cross_speaker", {}).get("curve"):
        md += ["## Cross-speaker operating curve (threshold h versus false regions and detection)", "", res["cross_speaker"]["curve"]["table"], ""]
    if "reproducibility" in res:
        md += ["## Reproducibility", "", f"Two analyze() runs on {res['reproducibility']['clip']}: identical = {res['reproducibility']['identical']}", ""]
    return format_floats("\n".join(md)) + "\n"


# A float with five or more decimals or an exponent (a Python repr inside saved text), and an interval labelled 95%.
RAW_FLOAT = re.compile(r"(?<![\w.])-?\d+(?:\.\d{5,}(?:e[-+]?\d+)?|(?:\.\d+)?e[-+]?\d+)(?![\w.])")
LABELLED_INTERVAL = re.compile(r"(95%[^\[\]|()']{0,40}?)\s*\[(-?\d+(?:\.\d+)?(?:e[-+]?\d+)?), (-?\d+(?:\.\d+)?(?:e[-+]?\d+)?)\]")


def format_floats(text: str) -> str:
    """Saved table text with each labelled 95% interval printed by bounds_text (equal bounds as degenerate) and each other
    raw float by number_text."""
    text = LABELLED_INTERVAL.sub(lambda m: bounds_text([float(m[2]), float(m[3])], m[1].strip()), text)
    return RAW_FLOAT.sub(lambda m: number_text(float(m[0])), text)


def render(results: Path, out: Path) -> None:
    """tables.md re-rendered from a saved results.json, labelled as computed after the evaluation that wrote it."""
    res = json.loads(results.read_text())
    note = (f"Re-rendered from the saved {results} by `python -m cvoice.evaluate render` (src/cvoice/evaluate.py), after the "
            "evaluation that wrote it: no number is measured again. The headline F1 table is rebuilt from the saved rows with the "
            "pre-registered accounting first; raw floats are printed to 3 significant digits and equal interval bounds as degenerate.")
    title, rest = tables_markdown(res).split("\n", 1)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(title + "\n\n" + note + "\n" + rest)
    log(f"wrote {out}")


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["render"]:
        ap = argparse.ArgumentParser(prog="python -m cvoice.evaluate render")
        ap.add_argument("results", type=Path, help="eval/results.json of a saved evaluation")
        ap.add_argument("out", type=Path, help="the Markdown file to write")
        a = ap.parse_args(argv[1:])
        return render(a.results, a.out)
    ap = argparse.ArgumentParser(prog="python -m cvoice.evaluate")
    ap.add_argument("--dataset", type=Path, default=ROOT / "data")
    ap.add_argument("--models", type=Path, default=ROOT / "models" / "detector.json")
    ap.add_argument("--cache", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=ROOT)
    ap.add_argument("--splits", default=",".join(DEFAULT_SPLITS), help="comma-separated: train, val (test only with --final)")
    ap.add_argument("--final", action="store_true", help="also evaluate the test split and the R2 lockbox; records the config hash, once per hash")
    ap.add_argument("--force", action="store_true", help="with --final: repeat a final evaluation for a config hash already evaluated")
    a = ap.parse_args(argv)
    splits = tuple(s for s in a.splits.split(",") if s)
    if not set(splits) <= {"train", "val", "test"}:
        ap.error(f"--splits takes train, val, test; got {a.splits}")
    with PreparePool(cache_dir=a.cache) as pool:
        res = run(a.dataset, a.models, a.cache, a.out, splits, a.final, a.force, pool)
    if res["errors"]:
        print("[evaluate] sections failed: " + ", ".join(res["errors"]), file=sys.stderr, flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
