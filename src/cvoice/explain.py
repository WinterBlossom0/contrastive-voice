"""Deterministic explanation templates (no LLM): where / what / how much / score effect / why / fix.

Wording is relative to the reference rendition; the score effect is arithmetic on the current result. Rounding:
seconds 2 decimals, semitones and dB 1 decimal, percentages integers, multiples 1 decimal.
"""
from __future__ import annotations

import math

import numpy as np

from . import config as C
from . import patterns
from .detect import clip_flags, scale as get_scale, threshold
from .score import unit_severity

# One rubric quotation per flaw type: (verbatim quotation, source). Sources are quoted from the judging instruments
# collected in the rubric research (NSDA Declamation Starter Kit, Poetry Out Loud Judge's Guide 2021-22, Toastmasters
# International Speech Contest ballot Item 1172, UIL Texas Extemporaneous criteria).
_NSDA = "NSDA Declamation Starter Kit"
_POL = "Poetry Out Loud Judge's Guide 2021-22"
WHY = {
    "RUSH": ("If your speech is too fast paced, your audience won't catch a word you say.", _NSDA),
    "DRAG": ("A recitation that is at a too slow or hurried pace, poorly projected, has a distracting rhythm or monotone "
             "delivery will obscure a poem's meaning for the audience.", _POL),
    "PAUSE_DROPPED": ("Decide whether the pauses come in suitable places for the poem.", _POL),
    "PAUSE_INTRUSIVE": ("Decide whether the pauses come in suitable places for the poem.", _POL),
    "MONOTONE": ("if it's monotonous, your audience won't recall a word you said", _NSDA),
    "DEEMPHASIS": ("It should be flexible, moving from one pitch level to another for emphasis, and should have a "
                   "variety of rate and volume.", "Toastmasters International Speech Contest ballot, Item 1172"),
    "FADE": ("Every word you deliver should come across loud and clear to the audience.", _NSDA),
    "MUMBLE": ("Was enunciation clear?", "UIL Texas Extemporaneous criteria"),
}
WHY["NATURAL_RUSH"] = WHY["RUSH"]
WHY["WORD_TIME"], WHY["ENDING_HIGH"], WHY["UNEVEN_TEMPO"] = WHY["DRAG"], WHY["DEEMPHASIS"], WHY["DRAG"]
WHY["TEMPO_FAST"], WHY["TEMPO_SLOW"], WHY["RANGE_NARROW"] = WHY["RUSH"], WHY["DRAG"], WHY["MONOTONE"]

FLAW_TYPE = {  # (dimension, sign of x) -> type
    ("D1", -1): "RUSH", ("D1", 1): "DRAG", ("D2", -1): "PAUSE_DROPPED", ("D2", 1): "PAUSE_INTRUSIVE",
    ("D9", -1): "NATURAL_RUSH", ("D7", 1): "WORD_TIME", ("D8", 1): "ENDING_HIGH",
    ("D3", -1): "MONOTONE", ("D4", -1): "DEEMPHASIS", ("D5", -1): "FADE", ("D6", -1): "MUMBLE",
}
MEASURE = {
    "D1": "speech time of the five-word window at the peak, s (reference scaled to your overall tempo)",
    "D9": "sum of the aligned word durations of the five-word window at the peak, s (pauses are not included)",
    "D2": "silent pause at the word boundary, s",
    "D3": "pitch range P90-P10 over the five-word window at the peak, st (reference scaled to your overall pitch range)",
    "D4": "stress points p of the word",
    "D5": "mean level over the five-word window at the peak, dB re the recording's median voiced level (reference shifted by your overall level difference)",
    "D7": "word occupancy, s (reference scaled to your overall tempo)",
    "D8": "final pitch change at a full stop, st",
    "D6": "MFCC delta magnitude over the five-word window at the peak (reference scaled by your overall difference)",
}


def _r(v: float, nd: int) -> float | None:
    return None if v is None or not np.isfinite(v) else round(float(v), nd)


def _pct(v: float) -> str:
    return f"{abs(v) * 100:.0f}"


def context(tr, i0: int, i1: int, dim: str) -> str:
    """Sentence position and punctuation context of words i0..i1."""
    sent = tr.sentence[i0]
    first, last = tr.sentence_words(sent)
    if i0 == first and i1 < last:
        where = "start of the sentence"
    elif i1 == last and i0 > first:
        where = "end of the sentence"
    elif i0 == first and i1 == last:
        where = "whole sentence"
    else:
        where = "middle of the sentence"
    out = f"sentence {sent + 1} of {tr.n_sentences}, {where}"
    if dim == "D2":
        out += f"; punctuation after '{tr.disp[i0]}': {tr.punct[i0] or 'none'}"
    return out


def _nearest_punct_word(tr, i: int) -> str:
    cands = [j for j in range(len(tr) - 1) if tr.punct[j] and j != i]
    if not cands:
        return "the next natural break"
    j = min(cands, key=lambda j: (abs(j - i), j))
    return f"'{tr.disp[j]}{tr.punct[j]}'"


CANDIDATE_CLAUSE = 'Automatic label; low precision on real speech; listen to the span.'
SYNTHETIC_ONLY_CLAUSE = 'Synthetic-only family; unvalidated on real speech.'
SYNTHETIC_ONLY_PATTERNS = ('HESITATION', 'WORD_BY_WORD', 'LOW_EFFORT', 'TRAILING_OFF')


def synthetic_only(key: str, pattern: str | None) -> bool:
    """Measures and patterns that only the synthetic edits validate: no real-speech labels back them."""
    return key in ('D7', 'D8') or pattern in SYNTHETIC_ONLY_PATTERNS


def pattern_fields(info):
    out = {k: info[k] for k in ('pattern', 'evidence', 'span_kind', 'candidate')}
    out['evidence'] = [round_evidence(e) for e in info['evidence']]
    return out


def round_evidence(item):
    nd = {'s': 3, 'ln': 2, 'dB': 2, 'st': 2, 'words': 1}
    value = item['value']
    if item['unit'] in nd:
        value = _r(value, nd[item['unit']])
    elif item['unit'] == 'count':
        value = int(value)
    return {**item, 'value': value}


def clip_evidence(comp):
    return [patterns.evidence('spread_ln', 'Word-time spread', _r(comp.dims['D7'].g, 2), 'ln'),
            patterns.evidence('measured_words', 'Measured words', int(np.isfinite(comp.dims['D7'].x).sum()), 'count')]


def _ending_change(v):
    return 'stays level' if round(v, 1) == 0 else f"{'rises' if v > 0 else 'falls'} by {abs(v):.1f} st"


def pattern_text(info, word):
    name = info['pattern']
    if name is None:
        return ''
    values = {e['key']: e['value'] for e in info['evidence']}
    template = PATTERN_TEXT[name]
    return template.format(word=word, start=info['p'][0], end=info['p'][1],
                           reference_change=_ending_change(values.get('final_change_b_st', 0)),
                           participant_change=_ending_change(values.get('final_change_p_st', 0)), **values)


PATTERN_TEXT = {
    'BLOCK': "At {start:.2f}-{end:.2f} s, '{word}': a silence of {silence_s:.2f} s inside the word; the reference has {reference_silence_s:.2f} s. This is the pattern of a block.",
    'WORD_REPETITION': "At {start:.2f}-{end:.2f} s, extra '{inserted_text}' lasts {inserted_s:.2f} s; the reference has no insertion here. This is the pattern of a word repetition.",
    'SOUND_REPETITION': "At {start:.2f}-{end:.2f} s, extra '{inserted_text}' lasts {inserted_s:.2f} s. This is the pattern of a sound repetition.",
    'FILLED_PAUSE': "At {start:.2f}-{end:.2f} s, a voiced run of {voiced_run_s:.2f} s precedes '{word}'. This is the pattern of a filled pause.",
    'ONSET_PROLONGATION': "At {start:.2f}-{end:.2f} s, the first half of '{word}' holds a stable sound for {run_s:.2f} s. This is the pattern of a prolongation.",
    'RHYME_PROLONGATION': "At {start:.2f}-{end:.2f} s, the second half of '{word}' holds a stable sound for {run_s:.2f} s. This is the pattern of a prolongation.",
    'LENGTHENED_WORD': "At {start:.2f}-{end:.2f} s, '{word}' has measured word occupancy {occupancy_p_s:.2f} s against {occupancy_b_s:.2f} s in the reference. This is the pattern of a lengthened word.",
    'RISING_ENDING': "At {start:.2f}-{end:.2f} s, the end of '{word}' {participant_change}; the reference {reference_change}. This is the pattern of a rising ending.",
    'FLAT_FINAL_FALL': "At {start:.2f}-{end:.2f} s, the end of '{word}' {participant_change}; the reference {reference_change}. This is the pattern of a flattened final fall.",
    'HESITATION': "A {pause_s:.2f} s pause (reference {reference_pause_s:.2f} s) precedes a word-time stretch of {next_word_stretch_ln:.2f} ln. This is the pattern of a hesitation.",
    'WORD_BY_WORD': "There are {events} extra pauses in this sentence, with a mean run of {mean_run_words:.1f} words. This is the pattern of word-by-word reading.",
    'NATURAL_RUSH': "The pauses around it shrank with the words ({pause_p_s:.2f} s against {pause_b_s:.2f} s). This is the pattern of natural rushing.",
    'LOW_EFFORT': "Alpha-ratio change {alpha_change_db:.1f} dB; pitch change {f0_change_st:.1f} st is supporting evidence. This is the pattern of low vocal effort.",
    'TRAILING_OFF': "Last-word drop {last_word_drop_db:.1f} dB against {reference_last_word_drop_db:.1f} dB in the reference. This is the pattern of trailing off.",
}


def _d1(ftype, where, words, P, pk, tr, participant, baseline, x, theta, mult, whole, **_):
    pct_here, pct_thr = (math.exp(abs(x)) - 1) * 100, (math.exp(theta) - 1) * 100
    own = " than your own overall tempo" if "D1" in whole else ""
    what = f"{'Faster' if ftype == 'RUSH' else 'Slower'}{own} here: {where} ('{words}')."
    win0, win1 = P.win[pk]
    how = (f"The word alignment measures {participant:.2f} s of speech in the peak window of {win1 - win0 + 1} words "
           f"('{tr.text(win0, win1)}'); relative to the reference rendition "
           f"it took {baseline:.2f} s at your overall tempo, {pct_here:.0f}% {'faster' if ftype == 'RUSH' else 'longer'} "
           f"({mult:.1f}x the threshold; flagged above {pct_thr:.0f}%).")
    fix = (f"Keep these words in step with the rest of your reading: about {baseline:.1f} s at your overall tempo." if "D1" in whole
           else f"Give these words about {baseline:.1f} s; lengthen the stressed words rather than adding gaps." if ftype == "RUSH"
           else f"Tighten these words to about {baseline:.1f} s; keep the pauses at punctuation and close the gaps inside the phrase.")
    return what, how, fix


def _d2(tr, i0, sign, p_span, baseline, participant, mult, theta, **_):
    """The text follows the measured direction, not the finding type: a grouped member takes its group's type (a DRAG or
    NATURAL_RUSH group can hold a shortened pause)."""
    prev, nxt = tr.disp[i0], tr.disp[i0 + 1]
    if sign < 0:
        what = f"Shorter pause than the reference after '{prev}' at {p_span[0]:.2f} s."
        how = (f"Relative to the reference rendition the pause before '{nxt}' is {baseline:.2f} s; the word alignment measures {participant:.2f} s "
               f"({mult:.1f}x the threshold; flagged when {theta:.2f} s shorter).")
        fix = f"Stop fully after '{prev}' and hold about {baseline:.1f} s before '{nxt}'."
        return what, how, fix
    what = f"Longer pause than the reference after '{prev}' at {p_span[0]:.2f} s."
    unmarked = "" if tr.punct[i0] else " and the transcript has no punctuation here"
    how = (f"The word alignment measures {participant:.2f} s of silence between '{prev}' and '{nxt}'; the reference holds {baseline:.2f} s{unmarked} "
           f"({mult:.1f}x the threshold; flagged when {theta:.2f} s longer).")
    target = _nearest_punct_word(tr, i0)
    stop = "" if target.rstrip("'").endswith((".", "!", "?")) else "."  # the quoted word already ends the sentence
    fix = (f"Shorten the pause after '{prev}' to about {baseline:.1f} s." if tr.punct[i0] else
           f"Carry '{prev} {nxt}' on one breath; move the breath to {target}{stop}")
    return what, how, fix


def _d3(where, words, participant, baseline, mult, theta, **_):
    what = f"Narrower pitch range than the reference: {where} ('{words}')."
    how = (f"Your pitch range is {participant:.1f} st here; relative to the reference rendition it is {baseline:.1f} st at your "
           f"overall pitch range ({mult:.1f}x the threshold; the ranges are compared as a ratio with {C.RANGE_REG_ST:.0f} st added to each, "
           f"flagged below x{math.exp(-theta):.2f}).")
    fix = f"Let your pitch move about {baseline:.1f} st across these words: lift on the stressed words and fall at the phrase end."
    return what, how, fix


def _d4(tr, i0, p_span, baseline, participant, x, mult, theta, **_):
    what = f"Lower stress points than the reference: '{tr.disp[i0]}' at {p_span[0]:.2f} s."
    how = (f"The reference rendition stresses it (stress points {baseline:.2f}); yours are {participant:.2f}, {abs(x):.2f} lower "
           f"({mult:.1f}x the threshold; flagged above {theta:.2f}; a marker needs {C.STRESS_P_MIN:.2f}).")
    fix = f"Stress '{tr.disp[i0]}': lift its pitch, make it louder and lengthen its stressed syllable."
    return what, how, fix


def _d5(where, words, participant, baseline, x, mult, theta, **_):
    what = f"Lower level than the reference: {where} ('{words}')."
    how = (f"Relative to your own typical level you are at {participant:.1f} dB here; the reference rendition holds {baseline:.1f} dB, "
           f"{abs(x):.1f} dB lower ({mult:.1f}x the threshold; flagged above {theta:.1f} dB).")
    fix = f"Keep these words at the level of the rest of the passage, about {abs(x):.1f} dB louder."
    return what, how, fix


def _d6(where, words, participant, baseline, x, mult, theta, **_):
    what = f"Lower spectral change: {where} ('{words}')."
    how = (f"Spectral change per frame is {participant:.2f} against {baseline:.2f} at your overall level, {_pct(math.exp(x) - 1)}% lower "
           f"relative to the reference rendition ({mult:.1f}x the threshold; flagged above {(1 - math.exp(-theta)) * 100:.0f}%).")
    fix = "Compare the spectral-change contour with the reference; this proxy does not measure intelligibility."
    return what, how, fix


def _natural(where, words, participant, baseline, x, theta, mult, **_):
    return (f"The words themselves were spoken faster at {where} ('{words}').",
            f"Aligned word time {participant:.2f} s against {baseline:.2f} s; ln ratio {x:.3f}, threshold {-theta:.3f} ({mult:.1f}x the threshold).",
            'Repeat the phrase with time to articulate each word.')


def _event(key, where, words, participant, baseline, x, theta, mult, **_):
    what = f"{'Longer word time' if key == 'D7' else 'Higher ending'} than the reference: {where} ('{words}')."
    how = f"Relative to the reference rendition: {participant:.2f} against {baseline:.2f}; delta {x:.2f} {C.DIM_UNIT[key]} ({mult:.1f}x the threshold; flagged above {theta:.2f} {C.DIM_UNIT[key]})."
    fix = 'Listen to this span beside the reference and repeat the phrase with the intended timing or ending.'
    return what, how, fix


# (dimension, sign of x, pattern name or None) -> renderer of (what, how, fix). A pattern keeps the renderer of its
# dimension and direction; pattern_text adds the pattern sentence.
EXPLAIN = {(dim, sign, None): renderer for (dim, sign), renderer in {
    ('D9', -1): _natural, ('D1', -1): _d1, ('D1', 1): _d1, ('D2', -1): _d2, ('D2', 1): _d2, ('D3', -1): _d3,
    ('D4', -1): _d4, ('D5', -1): _d5, ('D6', -1): _d6, ('D7', 1): _event, ('D8', 1): _event}.items()}
for _dim, _sign, _names in [('D9', -1, ('NATURAL_RUSH',)), ('D2', 1, ('HESITATION', 'WORD_BY_WORD')),
                          ('D5', -1, ('LOW_EFFORT', 'TRAILING_OFF')),
                          ('D7', 1, ('BLOCK', 'WORD_REPETITION', 'SOUND_REPETITION', 'FILLED_PAUSE',
                                    'ONSET_PROLONGATION', 'RHYME_PROLONGATION', 'LENGTHENED_WORD')),
                          ('D8', 1, ('RISING_ENDING', 'FLAT_FINAL_FALL'))]:
    for _name in _names:
        EXPLAIN[(_dim, _sign, _name)] = EXPLAIN[(_dim, _sign, None)]


# Measures over five-word windows: a finding marks the window at the peak, not the exact edges of the change.
WINDOW_KEYS = ('D1', 'D3', 'D5', 'D6', 'D9')
WINDOW_CLAUSE = 'The span is approximate: this measure uses five-word windows.'
TIMING_KEYS = ('D1', 'D2', 'D9')  # measured from the word alignment's boundaries


def alignment_caveat(P, w0: int, w1: int) -> str:
    """A timing finding over words with low aligner confidence: a change of level, voice quality or noise can move word
    boundaries, so the measured timing change can be an alignment error."""
    low = int((P.al.compat[w0:w1 + 1] < C.LOW_COMPAT_NOTICE).sum())
    if not low:
        return ''
    return (f"{low} {'word' if low == 1 else 'words'} in this span {'has' if low == 1 else 'have'} low aligner confidence, so this "
            "timing can be an alignment error rather than a change of delivery; listen to the span.")


def dimension_loss(scored, dim: str) -> float | None:
    """Overall points lost to the whole penalty of a dimension. In a saturated dimension one region's own points_lost is 0,
    while the dimension still costs these points."""
    return _r(abs(scored.points_lost(dim, scored.P[dim])[0]), 2)


def build(region, comp, B, P, regime: dict, mass: float, scored, fid: str, info=None, counted=True) -> dict:
    """One flaw entry of the result JSON for a decoded region."""
    dim = comp.dims[region.dim]
    key, tr = region.dim, P.tr
    sign = 1 if dim.x[region.peak] > 0 else -1
    i0, pk = region.i0, region.peak
    scale, h = get_scale(regime, key, sign), threshold(regime, key, sign)
    x, theta = float(dim.x[pk]), h * scale
    baseline, participant = dim.reference(pk), float(dim.p[pk])
    info = info or patterns.describe(region, comp, B, P, regime.get('pattern_labels'))
    ftype = info.get('type', FLAW_TYPE[(key, sign)])
    w0, w1 = info['words']
    p_span, b_span = info['p'], info['b']
    words = tr.text(w0, w1)
    lost, fixed = scored.points_lost(key, mass)
    sev = max(unit_severity(dim, u, scale, h, regime["name"] == "R2") for u in region.units)
    mult = abs(x) / theta  # every "x the threshold" in the text and `tolerance_multiple` is relative to the flag threshold
    whole = clip_flags(comp, regime)
    where = f"{p_span[0]:.2f}-{p_span[1]:.2f} s"
    fields = dict(ftype=ftype, where=where, words=words, P=P, pk=pk, tr=tr, i0=i0, sign=sign, key=key, p_span=p_span,
                  participant=participant, baseline=baseline, x=x, theta=theta, mult=mult, whole=whole)
    what, how, fix = EXPLAIN[(key, sign, info["pattern"])](**fields)
    detail = pattern_text(info, tr.disp[pk])
    caveats = [WINDOW_CLAUSE if key in WINDOW_KEYS else '', alignment_caveat(P, w0, w1) if key in TIMING_KEYS else '']
    how = " ".join(t for t in (how, detail, *caveats) if t)
    quote, source = WHY[ftype]
    effect = f"Costs {abs(lost):.1f} points of the reference-relative delivery index; score with this penalty removed: {fixed:.1f}." if fixed is not None else ""
    return {
        "id": fid, "type": ftype, "label": ftype + (" (measure name)" if key in ("D7", "D8") else " (recipe name)"), "dimension": key, "brief_word": C.DIM_BRIEF[key], "severity": _r(sev, 2),
        "words": [w0, w1], "p": [_r(p_span[0], 3), _r(p_span[1], 3)], "b": [_r(b_span[0], 3), _r(b_span[1], 3)],
        "measure": MEASURE[key], "unit": C.DIM_UNIT[key], "baseline": _r(baseline, 2), "participant": _r(participant, 2),
        "delta": _r(x, 2), "tolerance_multiple": _r(mult, 2), "threshold": _r(theta, 2),
        "points_lost": _r(abs(lost), 2), "overall_if_fixed": _r(fixed, 2), "dimension_points_lost": dimension_loss(scored, key),
        "context": context(tr, w0, w1, key), "text": f"{what} {how} {effect}".strip() + (" " + CANDIDATE_CLAUSE if info["candidate"] else "") +
        (' ' + SYNTHETIC_ONLY_CLAUSE if synthetic_only(key, info['pattern']) else ''),
        **pattern_fields(info), "group": None, "group_pattern": info.get("group_pattern"), "counted": counted,
        "why": (f"\"{quote}\" ({source}); a rubric context only, not evidence that this proxy measures enunciation." if key == "D6" else f"\"{quote}\" ({source})"), "fix": fix,
    }


def clip_type(key: str, g: float) -> str:
    """Type of a whole-clip flag of dimension `key` whose clip median is g (ln)."""
    return {'D1': 'TEMPO_FAST' if g < 0 else 'TEMPO_SLOW', 'D3': 'RANGE_NARROW', 'D7': 'UNEVEN_TEMPO'}[key]


def build_clip(key: str, comp, B, P, regime: dict, scored) -> dict:
    """Whole-clip entry for a flagged clip median: overall tempo (TEMPO_FAST / TEMPO_SLOW), overall pitch range (RANGE_NARROW)
    or word-time unevenness (UNEVEN_TEMPO)."""
    if key not in C.CLIP_DIMS:
        raise KeyError(key)
    g, theta, mass = comp.dims[key].g, regime["clip"][key], scored.clip[key]
    lost, fixed = scored.points_lost(key, mass)
    ftype = clip_type(key, g)
    if key == "D1":
        baseline, participant, value_unit = 1.0, math.exp(g), "x"
        measure = "median window speech-time ratio (participant / reference)"
        what = (f"Overall tempo: your median window speech-time ratio is {participant:.2f}x the reference rendition; "
                f"flagged outside x{math.exp(-theta):.2f} to x{math.exp(theta):.2f}.")
        fix = f"Aim for window speech times about {1 / participant:.2f}x your current times, preserving the pauses."
    elif key == "D3":
        baseline, participant, value_unit = float(np.nanmedian(B.win_R)), float(np.nanmedian(P.win_R)), "st"
        measure = "median pitch range P90-P10 over five-word windows, st"
        what = (f"Overall pitch range: your typical five-word pitch range is {participant:.1f} st against {baseline:.1f} st in the reference "
                f"rendition (compared as a ratio with {C.RANGE_REG_ST:.0f} st added to each: x{math.exp(g):.2f}, flagged below x{math.exp(-theta):.2f}).")
        fix = f"Widen your pitch movement across the whole passage; the reference moves about {baseline:.1f} st within a phrase."
    else:
        baseline, participant, value_unit = None, g, 'ln'
        measure = 'word-time spread, 1.4826 MAD of median-centred ln occupancy ratios'
        what = f"Uneven word timing: your word times differ from the reference's by a typical factor of x{math.exp(g):.2f}."
        fix = 'Keep the relative word times more even across the passage; listen beside the reference.'
    quote, source = WHY[ftype]
    return {
        "id": "", "type": ftype, "label": ftype + " (whole clip)", "dimension": key, "brief_word": C.DIM_BRIEF[key], "severity": _r(mass, 2),
        "words": [0, len(P.tr) - 1], "p": [_r(P.al.start[0], 3), _r(P.al.end[-1], 3)], "b": [_r(B.al.start[0], 3), _r(B.al.end[-1], 3)],
        "measure": measure, "unit": "ln", "value_unit": value_unit, "baseline": _r(baseline, 2), "participant": _r(participant, 2), "delta": _r(g, 2),
        "tolerance_multiple": _r(abs(g) / theta, 2), "threshold": _r(theta, 2), "points_lost": _r(abs(lost), 2), "overall_if_fixed": _r(fixed, 2),
        "dimension_points_lost": dimension_loss(scored, key), "context": "whole passage", "pattern": 'UNEVEN_TEMPO' if key == 'D7' else None,
        "evidence": clip_evidence(comp) if key == 'D7' else [], "span_kind": None,
        "group": None, "group_pattern": None, "counted": True, "candidate": False,
        "text": f"{what} Costs {abs(lost):.1f} points of the reference-relative delivery index; score with this penalty removed: {fixed:.1f}." +
        (' ' + SYNTHETIC_ONLY_CLAUSE if synthetic_only(key, None) else ''),
        "why": f"\"{quote}\" ({source})", "fix": fix,
    }
