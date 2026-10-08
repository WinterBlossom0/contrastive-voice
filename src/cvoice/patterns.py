"""Evidence labels and groups after decoding; regions and false-alarm counts stay unchanged."""
from __future__ import annotations

import math
from typing import NamedTuple

import numpy as np

from . import config as C
from .compare import final_span, pause_span
from .detect import key, parse_key, whole_clip_key
from .features import frame_slice, mean, sentence_final


def evidence(key, label, value, unit):
    return {'key': key, 'label': label, 'value': value, 'unit': unit}


def _spans(values, a, b):
    return [(max(a, s), min(b, e)) for s, e in values if s < b and e > a] if values is not None else []


def _longest(spans):
    return max(spans, key=lambda se: se[1] - se[0], default=None)


def _length(span):
    return span[1] - span[0] if span else 0.0


def word_time(comp, B, P, i):
    """D7 evidence precedence from the disfluency report, before validation switches."""
    a, b = float(P.al.start[i]), float(P.al.end[i])
    ba, bb = float(B.al.start[i]), float(B.al.end[i])
    out = {'pattern': 'LENGTHENED_WORD', 'p': (a, b), 'b': (ba, bb), 'words': [i, i],
           'span_kind': 'word', 'candidate': False,
           'evidence': word_time_fallback(P, B, i)}
    silence = _longest(_spans(P.word_silence_spans, a, b))
    ref = _longest(_spans(B.word_silence_spans, ba, bb))
    if _length(silence) - _length(ref) >= C.BLOCK_S:
        return {**out, 'pattern': 'BLOCK', 'p': silence, 'b': ref or out['b'], 'span_kind': 'sub-word',
                'evidence': [evidence('silence_s', 'Silence inside the word', _length(silence), 's'),
                             evidence('reference_silence_s', 'Silence inside the word, reference', _length(ref), 's'), *out['evidence']]}
    ref_indices = {v['prompt_index'] for v in B.inserted}
    for ins in P.inserted:
        j, form = ins['prompt_index'], ins['norm']
        if j not in (i - 1, i) or j in ref_indices:
            continue
        near = B.tr.norm[max(0, j - 1):min(len(B.tr), j + 1)]
        if not form or not any(w.startswith(form) for w in near):
            continue
        s, e = float(ins['start']), float(ins['end'])
        gap = s + e < 2 * a
        return {**out, 'pattern': 'WORD_REPETITION' if form in near else 'SOUND_REPETITION', 'p': (s, e),
                'b': (float(B.al.end[i - 1]) if i else 0.0, ba) if gap else out['b'],
                'words': [max(0, i - 1), i] if gap else [i, i], 'span_kind': 'boundary' if gap else 'sub-word',
                'candidate': True, 'evidence': [evidence('inserted_text', 'Inserted material', form, None),
                                               evidence('inserted_s', 'Inserted material length', e - s, 's')]}
    left = float(P.al.end[i - 1]) if i else a
    orphan = _longest(_spans(P.orphan_spans, left, a))
    if _length(orphan) >= C.ORPHAN_MIN_S:
        return {**out, 'pattern': 'FILLED_PAUSE', 'p': orphan,
                'b': (float(B.al.end[i - 1]) if i else 0.0, ba), 'words': [max(0, i - 1), i],
                'span_kind': 'boundary', 'evidence': [evidence('voiced_run_s', 'Extra voiced run', _length(orphan), 's')]}
    held = _longest(_spans(P.stable_spans, a, b))
    ref_held = _longest(_spans(B.stable_spans, ba, bb))
    if _length(held) >= C.STABLE_S and _length(held) > _length(ref_held):
        return {**out, 'pattern': 'ONSET_PROLONGATION' if sum(held) < a + b else 'RHYME_PROLONGATION',
                'p': held, 'b': ref_held or out['b'], 'span_kind': 'sub-word', 'candidate': True,
                'evidence': [evidence('run_s', 'Held-sound run', _length(held), 's')]}
    return out


class Group(NamedTuple):
    """Member region indices of one group. anchor: the member that carries the group's one penalty, None when the largest
    mass carries it, or the whole-clip flag key whose penalty covers every member. cause: the members are measures of one
    change (shown under the group's type), not a pattern built from separate events."""
    pattern: str
    members: tuple[int, ...]
    anchor: int | str | None
    cause: bool


def groups(comp, regions, clip=None) -> list[Group]:
    """Disjoint groups; word-by-word takes precedence over hesitation. `clip`: the whole-clip flags {dimension: g}.
    One change, one cause, one penalty: same-change regions join the change they measure (same_change), and regions of
    an expected secondary dimension (frozen registry) join a region of the type's primary key within half a window."""
    out, used = [], set()
    for sentence in sorted(set(comp.sentence)):
        members = tuple(j for j, r in enumerate(regions) if r.dim == 'D2' and r.sign > 0 and comp.sentence[r.i0] == sentence)
        if len(members) >= C.WORD_BY_WORD_MIN_EVENTS:
            out.append(Group('WORD_BY_WORD', members, None, False))
            used.update(members)
    if 'D7' in comp.dims:
        for j, r in enumerate(regions):
            if j in used or r.dim != 'D2' or r.sign < 0:
                continue
            i = r.i0 + 1
            if comp.dims['D7'].x[i] < C.HESITATION_STRETCH_MIN or not np.isfinite(comp.dims['D7'].x[i]):
                continue
            k = next((k for k, v in enumerate(regions) if k not in used and v.dim == 'D7' and v.sign > 0 and v.i0 == i), None)
            if k is not None:
                out.append(Group('HESITATION', (j, k), None, False))
                used.update((j, k))
    clip = clip or {}
    for target, anchor, words in change_anchors(comp, regions, clip):
        if anchor in used:
            continue
        members = tuple(k for k in range(len(regions)) if k not in used and k != anchor and
                        same_change(comp, regions, clip, k, target, words))
        if members:
            head = () if isinstance(anchor, str) else (anchor,)
            out.append(Group(_core_type(target), head + members, anchor, True))
            used.update(head + members)
    for j, r in enumerate(regions):
        anchored = next((n for n, g in enumerate(out) if g.anchor == j), None)
        cause = _cause_type(comp, regions, clip, j)
        if cause is None or (j in used and anchored is None):
            continue
        members = tuple(k for k, v in enumerate(regions) if k not in used and k != j and
                        v.dim in C.EXPECTED_SECONDARY[cause] and within_half_window(v, (r.i0, r.i1)))
        if not members:
            continue
        if anchored is None:
            out.append(Group(cause, (j, *members), j, True))
        else:
            out[anchored] = out[anchored]._replace(members=out[anchored].members + members)
        used.update((j, *members))
    return out


def change_anchors(comp, regions, clip) -> list[tuple[str, int | str, tuple[int, int]]]:
    """Order of the changes that another key measures (one detection per change, config.SAME_CHANGE), as (flag key, anchor, words), for scoring, display and
    evaluation: each region of the key, then its whole-clip flag ('<key> whole clip'), then each same-change region that
    measures the change alone, largest |z| first (the count_once choice)."""
    out = []
    for target in sorted(set(C.SAME_CHANGE.values())):
        out += [(target, j, (r.i0, r.i1)) for j, r in enumerate(regions) if key(r.dim, r.sign) == target]
        dim, sign = parse_key(target)
        if dim in clip and np.sign(clip[dim]) == sign:
            out.append((target, whole_clip_key(dim, sign), (0, max((r.i1 for r in regions), default=0))))
        alone = [j for j, r in enumerate(regions)
                 if C.SAME_CHANGE.get(key(r.dim, r.sign)) == target and _rush_member(comp, regions, clip, j, target)]
        out += [(target, j, (regions[j].i0, regions[j].i1)) for j in sorted(alone, key=lambda j: (-abs(regions[j].z), j))]
    return out


def within_half_window(region, words) -> bool:
    """The region's units lie within half a window of words (first, last), so its windows can contain those words."""
    half = C.WINDOW_WORDS // 2
    return region.i0 <= words[1] + half and region.i1 >= words[0] - half


def paired_pause_time(comp, region) -> tuple[float, float]:
    """(reference, participant) pause time in s over the paired pause boundaries (D2 b and p) of the words the region's
    windows cover, i0 - 2 .. i1 + 2."""
    d2, half = comp.dims['D2'], C.WINDOW_WORDS // 2
    span = slice(max(0, region.i0 - half), region.i1 + half)
    return float(np.nansum(d2.b[span])), float(np.nansum(d2.p[span]))


def natural_rush(comp, region) -> bool:
    """Pause rule of a D9- region alone: natural rushing shrinks the pauses with the words (recipe
    edits_extra.natural_rushing), the RUSH change keeps them (flaws.stretch_speech). True when the reference has
    PAUSE_MIN_S of paired pause time and the kept fraction p/b is below both the words' ratio (exp of D9 x at the peak)
    and NATURAL_RUSH_PAUSE_KEPT_MAX."""
    b, p = paired_pause_time(comp, region)
    if b < C.PAUSE_MIN_S:
        return False
    return p / b < min(math.exp(float(comp.dims['D9'].x[region.peak])), C.NATURAL_RUSH_PAUSE_KEPT_MAX)


def same_change(comp, regions, clip, j, target: str, words) -> bool:
    """The one same-change rule of scoring, display and evaluation: region j measures the change of flag key `target` on
    words (first, last) with a linked key (config.SAME_CHANGE, both directions), within half a window of the words.
    A D9- region measures the D1- change only when it is part of the RUSH change: a D1- region lies within half a window
    of it, the clip has a whole-clip D1- flag, or it is not natural rushing (natural_rush). `clip`: {dimension: g}."""
    r = regions[j]
    own = key(r.dim, r.sign)
    if not within_half_window(r, words):
        return False
    if C.SAME_CHANGE.get(target) == own:
        return True
    return C.SAME_CHANGE.get(own) == target and _rush_member(comp, regions, clip, j, target)


def _rush_member(comp, regions, clip, j, target) -> bool:
    r = regions[j]
    dim, sign = parse_key(target)
    return (any(key(v.dim, v.sign) == target and within_half_window(r, (v.i0, v.i1)) for v in regions) or
            (dim in (clip or {}) and np.sign(clip[dim]) == sign) or not natural_rush(comp, r))


def count_once(comp, regions, clip, target: str, words, matched: int | None = None, taken=()) -> tuple[int | None, tuple[int, ...]]:
    """One detection per change of flag key `target` on words (first, last): (detection, duplicates). The detection
    is `matched` (the region matched to the change by its own key) when there is one; otherwise the same-change region
    with the largest |z| detects the change. Every other same-change region is a duplicate. Regions in `taken`
    (matched to another change) are neither."""
    linked = [k for k in range(len(regions)) if k != matched and k not in taken and same_change(comp, regions, clip, k, target, words)]
    if matched is None and linked:
        matched = max(linked, key=lambda k: (abs(regions[k].z), -k))
        linked.remove(matched)
    return matched, tuple(linked)


def _core_type(flag):
    return next((t for t in C.CORE8_TYPES if key(C.FLAW_REGISTRY[t]['primary'], C.FLAW_REGISTRY[t]['sign']) == flag), None)


def rush_type(comp, regions, clip, j) -> str:
    """Type of the D9- region j by the pause rule (natural_rush) among `regions` with the whole-clip flags `clip`: RUSH or NATURAL_RUSH."""
    return 'RUSH' if _rush_member(comp, regions, clip, j, C.SAME_CHANGE['D9-']) else 'NATURAL_RUSH'


def _cause_type(comp, regions, clip, j):
    """Registry type of region j whose expected secondaries join it: a windowed core type by the region's key, or RUSH /
    NATURAL_RUSH for a D9- region by the pause rule (natural_rush). Event types (pauses, emphasis) take no members, so that a windowed
    change is never shown as a secondary of a one-word event."""
    r = regions[j]
    if r.dim == 'D9':
        return rush_type(comp, regions, clip, j)
    t = _core_type(key(r.dim, r.sign))
    return t if t is not None and C.FLAW_REGISTRY[t]['event'] == 'span' else None


def counted(comp, regions, masses, clip=None):
    """Indices of the regions that carry a penalty: per group the anchor, or the largest mass (ties: unit, then dimension,
    hence the earliest finding id); no member of a group under a whole-clip flag, whose penalty covers the change."""
    keep = set(range(len(regions)))
    for g in groups(comp, regions, clip):
        winner = g.anchor if g.anchor is not None else min(g.members, key=lambda j: (-masses[j], regions[j].i0, regions[j].dim))
        keep.difference_update(j for j in g.members if j != winner)
    return keep


def describe(region, comp, B, P, labels=None):
    """One label; report switches apply only to labels requiring Real validation."""
    r, i = region, region.peak
    out = {'pattern': None, 'evidence': [], 'span_kind': 'boundary' if r.dim == 'D2' else 'word',
           'candidate': False, 'words': [r.i0, r.i0 + 1] if r.dim == 'D2' else [r.i0, r.i1],
           'p': pause_span(B, P, i, comp) if r.dim == 'D2' else (P.al.start[r.i0], P.al.end[r.i1]),
           'b': pause_span(B, B, i, comp) if r.dim == 'D2' else (B.al.start[r.i0], B.al.end[r.i1])}
    if r.dim == 'D7':
        out = word_time(comp, B, P, i)
    elif r.dim == 'D8':
        fp, fb = float(P.final_df0[i]), float(B.final_df0[i])
        pattern = 'RISING_ENDING' if fp >= 1. else 'FLAT_FINAL_FALL' if fb < fp <= 0 else None
        out.update(pattern=pattern, span_kind='sub-word', p=final_span(P, i), b=final_span(B, i))
        if pattern:
            out['evidence'] = [evidence('final_change_p_st', 'Final pitch change, this recording', fp, 'st'),
                               evidence('final_change_b_st', 'Final pitch change, reference', fb, 'st'),
                               evidence('stretch', 'Comparison stretch', f"last {C.FINAL_WINDOW_S:.2f} s against the earlier part of the final word", None)]
    elif r.dim == 'D2' and r.sign > 0 and i + 1 < len(P.tr):
        stretch = float(comp.dims['D7'].x[i + 1])
        if stretch >= C.HESITATION_STRETCH_MIN:
            out.update(pattern='HESITATION', evidence=[evidence('pause_s', 'Pause', float(P.sil_raw[i]), 's'),
                       evidence('reference_pause_s', 'Pause, reference', float(B.sil_raw[i]), 's'),
                       evidence('next_word_stretch_ln', 'Word time of the next word', stretch, 'ln')])
    elif r.dim == 'D9' and r.sign < 0:
        d9 = comp.dims['D9']
        b, p = paired_pause_time(comp, r)
        out['evidence'] = [evidence('word_time_ln', 'Word-time ln ratio', float(d9.x[i]), 'ln'),
                           evidence('word_time_p_s', 'Aligned word time, this recording', float(d9.p[i]), 's'),
                           evidence('word_time_b_s', 'Aligned word time, reference', float(d9.b[i]), 's'),
                           evidence('pause_p_s', 'Paired pause time around the span (2 words each side), this recording', p, 's'),
                           evidence('pause_b_s', 'Paired pause time around the span (2 words each side), reference', b, 's')]
        if natural_rush(comp, r):
            out['pattern'] = 'NATURAL_RUSH'
        else:
            out['type'] = 'RUSH'
    elif r.dim == 'D5' and r.sign < 0:
        last = r.i1
        def drop(rec):
            a, b = rec.tr.sentence_words(rec.tr.sentence[last])
            sl = frame_slice(rec.al.start[a], rec.al.end[b], len(rec.fr))
            lw = frame_slice(*rec.regions[last], len(rec.fr))
            return mean(rec.fr.L[lw][rec.fr.voiced[lw]]) - mean(rec.fr.L[sl][rec.fr.voiced[sl]])
        dp, db = drop(P), drop(B)
        alpha = mean(P.alpha_word[r.i0:r.i1 + 1]) - mean(B.alpha_word[r.i0:r.i1 + 1])
        if sentence_final(P.tr)[last] and dp < db:
            out.update(pattern='TRAILING_OFF', evidence=[evidence('last_word_drop_db', 'Last-word drop', dp, 'dB'),
                                                        evidence('reference_last_word_drop_db', 'Last-word drop, reference', db, 'dB')])
        elif alpha <= -C.ALPHA_DROP_DB:
            pitch = mean(P.ws.med_s[r.i0:r.i1 + 1]) - mean(B.ws.med_s[r.i0:r.i1 + 1])
            out.update(pattern='LOW_EFFORT', evidence=[evidence('alpha_change_db', 'Alpha-ratio change', alpha, 'dB'),
                                                      evidence('f0_change_st', 'Pitch change (supporting evidence)', pitch, 'st')])
    gate = C.PATTERN_GATES.get(out['pattern'])
    if gate and not (labels or {}).get(gate, False):
        if r.dim == 'D7':
            out = {**out, 'pattern': 'LENGTHENED_WORD', 'evidence': word_time_fallback(P, B, i),
                   'span_kind': 'word', 'candidate': False, 'words': [i, i],
                   'p': (P.al.start[i], P.al.end[i]), 'b': (B.al.start[i], B.al.end[i])}
        else:
            out.update(pattern=None, evidence=[], candidate=False)
    return out


def word_time_fallback(P, B, i):
    return [evidence('occupancy_p_s', 'Word occupancy, this recording (measured)', float(P.occ[i]), 's'),
            evidence('occupancy_b_s', 'Word occupancy, reference (measured, not scaled)', float(B.occ[i]), 's')]


def annotate(comp, regions, B, P, labels=None, clip=None):
    out = [describe(r, comp, B, P, labels) for r in regions]
    for g in groups(comp, regions, clip):
        for j in g.members:
            out[j].update(group=g.members, group_pattern=g.pattern)
            if g.cause and j != g.anchor:
                # A second measure or an expected secondary of the group's change takes the change's type, not a label of its own.
                out[j].update(type=g.pattern, pattern=None, candidate=False)
            if g.pattern == 'WORD_BY_WORD':
                indices = sorted(regions[k].i0 for k in g.members)
                run = float(np.mean(np.diff(indices)))
                out[j].update(pattern=g.pattern, evidence=[evidence('events', 'Pause events', len(g.members), 'count'),
                                                         evidence('mean_run_words', 'Mean run length', run, 'words')])
    return out
