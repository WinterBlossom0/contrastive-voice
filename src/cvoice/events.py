"""Shared event matching for train operating-point selection and evaluation."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from scipy.optimize import linear_sum_assignment
from . import config as C
from .compare import Comparison, compare, event_span
from .detect import Region, clip_flags, decode, key, scale, whole_clip_key
from .features import Recording
from .patterns import change_anchors, count_once, within_half_window
from .score import Scored, score

@dataclass
class Run:
    """B, P analysed under a regime: comparison, local regions, whole-clip flags {dimension: g} and score."""
    B: Recording
    P: Recording
    comp: Comparison
    regions: list[Region]
    scored: Scored
    regime: str
    clip: dict[str, float]
    scale: dict | None = None  # the regime's scales (diagnosis of missed flaws)
    enabled: tuple | None = None

    @property
    def n_flags(self) -> int:
        """False-alarm count unit: local regions plus whole-clip flags."""
        return len(self.regions) + len(self.clip)

    @property
    def flag_keys(self) -> list[str]:
        """Flag key per local region, then per whole-clip flag (e.g. "D1- whole clip")."""
        return [key(r.dim, r.sign) for r in self.regions] + [clip_key(k, g) for k, g in self.clip.items()]

    def with_regions(self, regions: list[Region]) -> "Run":
        """The same comparison scored against another set of local regions (threshold sweeps, trivial baselines)."""
        return Run(self.B, self.P, self.comp, regions, self.scored, self.regime, self.clip, self.scale, self.enabled)


def clip_key(dim: str, g: float) -> str:
    return whole_clip_key(dim, 1 if g > 0 else -1)


def run_pair(B: Recording, P: Recording, det: dict, regime: str) -> Run:
    comp = compare(B, P)
    reg = det["regimes"][regime]
    regions = decode(comp, reg, B.tr.sentence)
    return Run(B, P, comp, regions, score(comp, regions, reg, det["score"]["pmax"]), regime, clip_flags(comp, reg), reg["scales"], tuple(reg["enabled"]))


def region_span(run: Run, r: Region) -> tuple[float, float]:
    """Participant-time span (s) of a region: words i0..i1, or the gap after word i for pauses."""
    al = run.P.al
    if C.is_event(r.dim):
        return event_span(run.comp, r.dim, r.peak, run.B, run.P)
    return float(al.start[r.i0]), float(al.end[r.i1])


def iou(a: tuple[float, float], b: tuple[float, float]) -> float:
    inter = max(0.0, min(a[1], b[1]) - max(a[0], b[0]))
    union = (a[1] - a[0]) + (b[1] - b[0]) - inter
    return inter / union if union > 0 else 0.0


def overlaps(a: Region, b: Region) -> bool:
    """Same dimension and sign, and the unit (word / boundary) index ranges intersect. Used wherever two recordings of
    different length are compared: word indices are shared, time axes are not."""
    return (a.dim, a.sign) == (b.dim, b.sign) and a.i0 <= b.i1 and b.i0 <= a.i1


def truths(lab: dict, excluded=False, enabled=None) -> list[dict]:
    """Injected (non-placebo) flaws with participant-time spans (s) and (dimension, sign)."""
    out = []
    for f in lab["flaws"]:
        if f.get("placebo", False) or bool(f.get('evaluation_excluded')) != excluded:
            continue
        spec = C.FLAW_REGISTRY[f['type']]
        dim = spec['primary']
        words = ([f['details']['reference_stressed_word']] * 2 if f['type'] == 'MISPLACED_EMPHASIS' and
                 'reference_stressed_word' in f.get('details', {}) else f['words'])
        spans = [(f['span'], words)]
        events = f.get('events', [])
        if f['type'] == 'WORD_BY_WORD':
            silences = sorted((v for v in events if v['kind'] == 'silence' and 'clip_span' in v), key=lambda v: v['clip_span'][0])
            # Each inserted silence is one boundary truth; a label without silence events stays one group truth.
            if silences:
                starts = lab.get('words', {}).get('start')
                spans = []
                for j, v in enumerate(silences):
                    boundary = _boundary_before(starts, v['clip_span']) if starts else words[0] + j
                    spans.append((v['clip_span'], [boundary, boundary + 1]))
        elif f['type'] == 'HESITATION':
            silence = next((v['clip_span'] for v in events if v['kind'] == 'silence' and 'clip_span' in v), f['span'])
            spans = [(silence, [max(0, words[0] - 1), words[0]])]
        elif dim == 'D7' and spec['event'] != 'clip':
            kinds = ('silence',) if f['type'] == 'BLOCK' else ('copy',) if 'REPETITION' in f['type'] else ('stretch',)
            selected = [v['clip_span'] for v in events if v['kind'] in kinds and 'clip_span' in v]
            if selected:
                spans = [([min(v[0] for v in selected), max(v[1] for v in selected)], words)]
        for span, unit_words in spans:
            s, e = np.asarray(span, float) / C.SR
            out.append({'type': f['type'], 'level': f['level'], 'dim': dim, 'sign': spec['sign'], 'span': (s, e),
                        'event': spec['event'], 'available': dim in (C.DIMS if enabled is None else enabled), 'secondary': spec['secondary'],
                        'realised': f.get('realised', {}), 'exclusion_reasons': f.get('evaluation_excluded', []),
                        'mid': .5 * (s + e), 'words': unit_words, 'label_words': words})
    return out


def _boundary_before(starts, span) -> int:
    """Index of the word boundary that holds the span midpoint: the word that starts last before the midpoint."""
    return int(np.searchsorted(starts, .5 * sum(span)) - 1)


def match(truth: list[dict], run: Run, both_edges: bool = True) -> dict[int, int]:
    """One-to-one matching truth -> region by (dimension, sign): IoU >= 0.5 for windowed dimensions; for pauses and
    emphasis the event times (span midpoints) within EVENT_TOL_S, or overlapping spans. Returns {truth index: region index}."""
    pairs: dict[int, int] = {}
    spans = [region_span(run, r) for r in run.regions]
    for dim, sign in {(t["dim"], t["sign"]) for t in truth if t["dim"] in C.DIMS}:
        ti = [i for i, t in enumerate(truth) if (t["dim"], t["sign"]) == (dim, sign) and t.get('event') != 'clip']
        ri = [j for j, r in enumerate(run.regions) if r.dim == dim and sign in (0, r.sign) and j not in pairs.values()]
        if not ti or not ri:
            continue
        if both_edges and dim in ('D7', 'D8'):
            errors = np.array([[np.abs(np.asarray(spans[j]) - truth[i]['span']) for j in ri] for i in ti])
            ok = (errors <= C.EVENT_TOL_S).all(axis=2)
            cost = np.where(ok, errors.sum(axis=2), 1e3)
        elif C.is_event(dim):
            dt = np.array([[abs(0.5 * sum(spans[j]) - truth[i]["mid"]) for j in ri] for i in ti])
            same = np.array([[run.regions[j].i0 == truth[i]["words"][0] for j in ri] for i in ti])  # the labelled boundary / word itself
            ok = same | (dt <= C.EVENT_TOL_S) | np.array([[iou(spans[j], truth[i]["span"]) > 0 for j in ri] for i in ti])
            cost = np.where(same, 0.0, np.where(ok, dt + 1e-3, 1e3))
        else:
            sc = np.array([[iou(spans[j], truth[i]["span"]) for j in ri] for i in ti])
            ok = sc >= C.IOU_MIN
            cost = np.where(ok, -sc, 1e3)
        for a, b in zip(*linear_sum_assignment(cost)):
            if ok[a, b]:
                pairs[ti[a]] = ri[b]
    return pairs


def on_flaw(r: Region, t: dict) -> bool:
    """A region lies on an injected flaw: same dimension and sign, and it shares a word (windowed) or is the labelled event."""
    if r.dim != t["dim"] or t["sign"] not in (0, r.sign):
        return False
    w0, w1 = t["words"]
    return (r.i0 == w0) if C.is_event(t["dim"]) else (r.i0 <= w1 and r.i1 >= w0)


def near(r: Region, t: dict) -> bool:
    """The region's units lie within half a window of the truth's words, so its windows can contain edited words."""
    return within_half_window(r, t["words"])


LINKED_KEYS = frozenset(C.SAME_CHANGE) | frozenset(C.SAME_CHANGE.values())


def whole_passage(t: dict, n_words: int) -> bool:
    """The truth is a whole-clip truth or an edit of every word of the passage."""
    return t.get('event') == 'clip' or list(t.get('label_words', t['words'])) == [0, n_words - 1]


def truth_changes(run: Run, truth_rows: list[dict], matched: dict[int, int]) -> tuple[dict[int, int], list[dict]]:
    """One detection per change, by patterns.count_once (the rule of scoring and display): a truth of a linked key
    (config.SAME_CHANGE) is detected by its own-key match, else by its strongest same-change region; every other region
    of the change is a duplicate. The own-key whole-clip flag is the match of a whole-passage edit. Truths with an own-key
    match go first, so a region is a duplicate only when another region already detects the change. Returns
    ({truth index: same-change detection, or the whole-clip flag key}, duplicate rows)."""
    claimed, found, rows = set(matched.values()), {}, []
    linked = [i for i, t in enumerate(truth_rows) if t['available'] and t.get('event') != 'clip' and t['sign'] and
              key(t['dim'], t['sign']) in LINKED_KEYS]
    for i in sorted(linked, key=lambda i: (i not in matched, i)):
        truth = truth_rows[i]
        target = key(truth['dim'], truth['sign'])
        own = matched.get(i)
        whole = clip_key(truth['dim'], truth['sign'])
        clip_agrees = truth['dim'] in run.clip and np.sign(run.clip[truth['dim']]) == truth['sign']
        if own is None and whole_passage(truth, len(run.P.tr)) and whole not in claimed and clip_agrees:
            own = whole  # the edit's own-key whole-clip flag detects a whole-passage change
        detection, duplicates = count_once(run.comp, run.regions, run.clip, target, truth['words'], own, tuple(claimed))
        if detection is not None and i not in matched:
            found[i] = detection
            claimed.add(detection)
        claimed.update(duplicates)
        rows += [{'index': k, 'group': key(run.regions[k].dim, run.regions[k].sign), 'change': target, 'on_truth': True,
                  'units': [run.regions[k].i0, run.regions[k].i1]} for k in duplicates]
    return found, rows


def false_change_duplicates(comp, regions: list[Region], clip: dict[str, float], claimed=()) -> list[dict]:
    """One detection per change among the regions that no truth claims: each change of patterns.change_anchors (the order of patterns.groups) is one
    false change, and its same-change regions (patterns.count_once) are its duplicates."""
    claimed, rows = set(claimed), []
    for target, anchor, span in change_anchors(comp, regions, clip):
        if anchor in claimed:
            continue
        claimed.add(anchor)
        _, duplicates = count_once(comp, regions, clip, target, span, anchor, tuple(claimed))
        claimed.update(duplicates)
        rows += [{'index': k, 'group': key(regions[k].dim, regions[k].sign), 'change': target, 'on_truth': False,
                  'units': [regions[k].i0, regions[k].i1]} for k in duplicates]
    return rows


def on_shortfall(r: Region, shortfalls: list[dict]) -> bool:
    """The region shares a word with an excluded truth, whatever its dimension: it is neither a TP nor a false region."""
    return any(r.i0 <= t['words'][1] and r.i1 >= t['words'][0] for t in shortfalls)


def _truth_group(t: dict) -> str:
    """Flag key under which a truth is counted; a truth without a direction is counted under its dimension."""
    if not t["sign"]:
        return t["dim"] + "±"
    if t.get('event') == 'clip':
        return whole_clip_key(t["dim"], t["sign"])
    return key(t["dim"], t["sign"])


def _detected_by(run: Run, found, clip_hit: bool, own_match: bool) -> str | None:
    if isinstance(found, int):
        return 'same change: ' + key(run.regions[found].dim, run.regions[found].sign)
    if clip_hit:
        return 'whole clip'
    if own_match:
        return 'own key'
    return None


def _detected_region(t: dict, found, own_match, clip_hit: bool):
    """Index of the detecting region, the whole-clip flag key of a whole-passage change, or the dimension of a whole-clip truth."""
    if found is not None:
        return found
    if own_match is not None:
        return own_match
    if clip_hit:
        return t['dim']
    return None


def eval_clip(run: Run, lab: dict, secondary_exempt: bool = True) -> dict:
    """Per-clip TP / FN / FP by (dimension, sign) group, onset / offset errors of matched windows, and the false regions
    (those not matched and not an expected secondary dimension of a nearby injected flaw). One detection counts per change
    (truth_changes, false_change_duplicates): the other regions of a change are duplicates, listed in `duplicates` with
    their own flag key and the flag key of the change, under the strict and the exempt counting alike."""
    truth_rows = truths(lab, enabled=run.enabled)
    shortfalls = truths(lab, excluded=True)
    matches = match(truth_rows, run)
    overlap_matches = match(truth_rows, run, False)
    clip_matched = set()
    spans = [region_span(run, r) for r in run.regions]
    found, duplicates = truth_changes(run, truth_rows, matches)
    matched_r = set(matches.values()) | set(found.values())
    truth_report = []
    for i, t in enumerate(truth_rows):
        clip_hit = (t.get('event') == 'clip' and t['dim'] in run.clip) or isinstance(found.get(i), str)
        if clip_hit:
            clip_matched.add(t['dim'])
        row = {"type": t["type"], "level": t["level"], "group": _truth_group(t), "detected": i in matches or clip_hit or i in found,
               'detected_index_or_overlap': i in overlap_matches or clip_hit or i in found, 'event': t['event'], 'realised': t.get('realised', {}),
               "touched": i in found or any(on_flaw(r, t) for r in run.regions), "available": t["available"],
               "status": "measured" if t["available"] else "no detector",
               'detected_by': _detected_by(run, found.get(i), clip_hit, i in matches),
               'detected_region': _detected_region(t, found.get(i), matches.get(i), clip_hit)}
        if not t["available"]:
            row.update(detected=None, touched=None, group=t["dim"])
            truth_report.append(row)
            continue
        if i in found:
            row['grounding_status'] = 'same-change detection; edges not compared'
        if i in matches and t["dim"] != "D4":
            s, e = spans[matches[i]]
            row['edge_error_above_tolerance'] = max(abs(s-t['span'][0]), abs(e-t['span'][1])) > C.EVENT_TOL_S
            row['grounding_status'] = 'true positive with coarse edges' if row['edge_error_above_tolerance'] else 'true positive within edge tolerance'
            prefix = "pause_" if t["dim"] == "D2" else ""
            row[prefix + "onset_ms"], row[prefix + "offset_ms"] = round((s - t["span"][0]) * 1000, 1), round((e - t["span"][1]) * 1000, 1)
        if not row['detected']:  # diagnosis of a miss: the largest signed z over the labelled units
            d, (w0, w1) = run.comp.dims[t["dim"]], t["words"]
            end = max(w0 + 1, w1) if C.UNIT_KIND[t['dim']] == 'boundary' else w1 + 1
            zz = (t['sign'] or 1) * d.x[w0:end] / scale({'scales': run.scale}, t['dim'], t['sign'] or 1) if run.scale else np.array([])
            if t["sign"] == 0:
                zz = np.abs(zz)
            row["max_z"] = round(float(np.nanmax(zz)), 2) if zz.size and np.isfinite(zz).any() else None
            row["units"] = [w0, w1]
            row["same_dim_regions"] = [[r.i0, r.i1] for r in run.regions if r.dim == t["dim"] and t["sign"] in (0, r.sign)]
        truth_report.append(row)
    dropped = {j for j, r in enumerate(run.regions) if on_shortfall(r, shortfalls)}
    whole_false = {k: g for k, g in run.clip.items() if k not in clip_matched}
    duplicates += false_change_duplicates(run.comp, run.regions, whole_false,
                                          matched_r | dropped | {d['index'] for d in duplicates})
    duplicated = {d['index'] for d in duplicates}
    false, secondary = [], 0
    for j, r in enumerate(run.regions):
        if j in matched_r or j in dropped or j in duplicated:
            continue
        if secondary_exempt and any(r.dim in t["secondary"] and near(r, t) for t in truth_rows):
            secondary += 1
        else:
            d = run.comp.dims[r.dim]
            false.append({"group": key(r.dim, r.sign), "on_flaw": any(on_flaw(r, t) for t in truth_rows),
                          "span": [round(spans[j][0], 3), round(spans[j][1], 3)], "units": [r.i0, r.i1], "z": round(float(r.z), 2),
                          "x": round(float(d.x[r.peak]), 3), "baseline": round(float(d.b[r.peak]), 3), "participant": round(float(d.p[r.peak]), 3)})
    counted = [j for j in range(len(run.regions)) if j not in duplicated]
    return {"truth": truth_report, "false": false, "secondary": secondary, "duplicate": len(duplicates), "duplicates": duplicates,
            'same_change_detections': [{'type': truth_rows[i]['type'], 'change': key(truth_rows[i]['dim'], truth_rows[i]['sign']),
                                        'group': key(run.regions[j].dim, run.regions[j].sign)} for i, j in found.items() if isinstance(j, int)],
            "n_regions": len(counted),
            'false_clip': [k for k in run.clip if k not in clip_matched and not any(t['event'] == 'clip' and t['dim'] == k for t in shortfalls)],
            'shortfalls': shortfalls,
            'label_count': sum(not f.get('placebo', False) for f in lab['flaws']), 'event_count': len(truth_rows),
            'word_by_word': {'label_groups': sum(f['type'] == 'WORD_BY_WORD' and not f.get('placebo', False) for f in lab['flaws']),
                             'eligible_clips': int(any(t['type'] == 'WORD_BY_WORD' for t in truth_rows)),
                             'detected_clips': int(any(t['type'] == 'WORD_BY_WORD' and t['detected'] for t in truth_report)),
                             'boundary_truths': sum(t['type'] == 'WORD_BY_WORD' for t in truth_rows)},
            "flags_on_flaw": sum(j in matched_r or any(on_flaw(run.regions[j], t) for t in truth_rows) for j in counted)}


def cluster_f1(rows) -> float:
    """F1 of (TP, FP, FN) rows."""
    denominator = sum(2 * r[0] + r[1] + r[2] for r in rows)
    return 2 * sum(r[0] for r in rows) / denominator if denominator else np.nan


def f1(tp: float, fp: float, fn: float, clusters=None) -> dict:
    """Counts, precision, recall and F1. `clusters` {source speaker: [(TP, FP, FN)]}: a speaker-bootstrap F1 interval, or
    with fewer than MIN_BOOTSTRAP_CLUSTERS speakers the F1 of each speaker and their range (uncertainty.cluster_summary)."""
    p = tp / (tp + fp) if tp + fp else None
    r = tp / (tp + fn) if tp + fn else None
    from .uncertainty import wilson, cluster_summary
    summary = cluster_summary(clusters, cluster_f1) if clusters else {'ci95': [None, None], 'per_cluster': None, 'range': None,
                                                                      'method': 'speaker clusters unavailable'}
    return {'f1_ci95': summary['ci95'], 'f1_per_speaker': summary['per_cluster'], 'f1_range': summary['range'], 'ci_method': summary['method'],
            'precision_ci95': wilson(tp,tp+fp), 'recall_ci95': wilson(tp,tp+fn), "tp": tp, "fp": fp, "fn": fn, "precision": None if p is None else round(p, 3), "recall": None if r is None else round(r, 3),
            "f1": round(2 * tp / (2 * tp + fp + fn), 3) if 2 * tp + fp + fn else None}
