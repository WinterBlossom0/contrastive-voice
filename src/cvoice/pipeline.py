"""analyze(): participant audio + transcript + baseline rendition -> result JSON of DESIGN 9 (schema 2).

    python -m cvoice.pipeline --participant p.wav --baseline b.wav --transcript t.txt --regime R1 --out result.json

Stages (the dashboard shows them): decode, align, features, compare, detect.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import __version__
from . import config as C
from .detect import scale
from . import audio, explain, patterns
from .align import (Alignment, Transcript, TranscriptMismatch, align_audio, emissions, load_aligner, parse_transcript,
                    require_match)
from .compare import Comparison, compare, time_map, warp
from .detect import clip_flags, decode, decode_dim, flagged_dims, key as flag_key, load_detector, threshold
from .features import Recording, make_recording
from .score import Scored, score

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DETECTOR = ROOT / "models" / "detector.json"


# ============================================================================================ preparation
def cache_key(wav: np.ndarray, tr: Transcript | None = None) -> str:
    """Hash of the samples and (when given) the transcript words: the alignment cache key."""
    return hashlib.sha256((audio.sha256_pcm(wav) + "|" + (" ".join(tr.norm) if tr is not None else "")).encode()).hexdigest()[:32]


def align_wav(wav: np.ndarray, tr: Transcript, aligner=None, cache_dir: Path | None = None) -> tuple[np.ndarray, Alignment]:
    """Forced alignment of one recording (canonical 16 kHz mono). With cache_dir the alignment is cached by the hash of
    the samples and the transcript words (the alignment is the expensive stage). Returns (wav, alignment)."""
    cache = None if cache_dir is None else Path(cache_dir) / f"align_{cache_key(wav, tr)}_v2.npz"
    if cache is not None and cache.exists():
        with np.load(cache) as z:
            decoded = [{"norm": str(w), "start": float(a), "end": float(b)}
                       for w, a, b in zip(z["decode_norm"], z["decode_start"], z["decode_end"])]
            return wav, Alignment(z["start"], z["end"], z["compat"], float(z["compat"].mean()), decoded, z["char_spans"])
    al = align_audio(aligner or load_aligner(), wav, tr)
    if cache is not None:
        cache.parent.mkdir(parents=True, exist_ok=True)
        np.savez(cache, start=al.start, end=al.end, compat=al.compat, char_spans=al.char_spans,
                 decode_norm=np.array([w["norm"] for w in al.decoded], dtype=str),
                 decode_start=np.array([w["start"] for w in al.decoded]), decode_end=np.array([w["end"] for w in al.decoded]))
    return wav, al


def prepare(wav: np.ndarray, tr: Transcript, aligner=None, cache_dir: Path | None = None) -> Recording:
    """Align and featurise one recording (canonical 16 kHz mono)."""
    wav, al = align_wav(wav, tr, aligner, cache_dir)
    return make_recording(wav, tr, al)


# ============================================================================================ batches
@dataclass(frozen=True, eq=False)
class Job:
    """One unit of alignment work: kind 'prepare' -> Recording (alignment + features), 'align' -> Alignment, 'emit' ->
    log-probabilities (tr is None). key = cache key (also names the job in errors and identifies duplicates)."""
    wav: np.ndarray
    tr: Transcript | None
    key: str
    kind: str = "prepare"


def make_job(wav: np.ndarray, tr: Transcript | None = None, kind: str = "prepare") -> Job:
    return Job(wav, tr, cache_key(wav, tr), kind)


def execute(job: Job, aligner=None, cache_dir: Path | None = None):
    """Run one job in this process (the sequential path and the pool workers share this function)."""
    if job.kind == "prepare":
        return prepare(job.wav, job.tr, aligner, cache_dir)
    if job.kind == "align":
        return align_wav(job.wav, job.tr, aligner, cache_dir)[1]
    if job.kind == "emit":
        return emissions(aligner or load_aligner(), job.wav)
    raise ValueError(f"unknown job kind {job.kind!r}")


def detach(result):
    """A Recording without its samples: the parent already has them, so they need not cross the pipe twice."""
    return dataclasses.replace(result, wav=None) if isinstance(result, Recording) else result


def attach(result, job: Job):
    return dataclasses.replace(result, wav=job.wav) if isinstance(result, Recording) else result


def run_jobs(jobs: list[Job], pool=None, aligner=None, cache_dir: Path | None = None) -> list:
    """Results in input order. Without a pool: plain in-process calls (the dashboard, tests and the one-clip smoke test use
    this path); with a PreparePool the same jobs are spread over its workers and give the same results."""
    if pool is not None:
        return pool.map(jobs)
    return [execute(j, aligner, cache_dir) for j in jobs]


def map_calls(fn: Callable, args: list[tuple], pool=None) -> list:
    """[fn(*a) for a in args] in input order, spread over the pool's workers when there is one (fn: a module-level function)."""
    return pool.starmap(fn, args) if pool is not None else [fn(*a) for a in args]


def device_class(pool=None) -> str:
    """'cpu' or 'cuda': the kind of device the alignments were computed on (recorded in detector.json and every result)."""
    return "cpu" if pool is None else pool.device_class


# ============================================================================================ JSON helpers
def canon(o):
    """Plain JSON types: numpy -> python, NaN / inf -> None."""
    if isinstance(o, dict):
        return {str(k): canon(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, np.ndarray)):
        return [canon(v) for v in (o.tolist() if isinstance(o, np.ndarray) else o)]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def dumps(result: dict) -> str:
    """Deterministic serialisation: sorted keys, compact, UTF-8."""
    return json.dumps(canon(result), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _arr(a, nd: int) -> list:
    return [None if not np.isfinite(v) else round(float(v), nd) for v in a]


# ============================================================================================ rows
_ROWS = (("D1", "pace", "Pace (delta, ln ratio)"), ("D2", "pauses", "Pauses (delta, s)"),
         ("D3", "pitch_range", "Pitch range (delta, ln ratio)"), ("D4", "emphasis", "Emphasis (delta, p-units)"),
         ("D5", "volume", "Volume (delta, dB)"), ("D6", "clarity", "Clarity (spectral-change proxy, delta, ln ratio)"),
         ("D9", "speech_tempo", "Speech tempo: aligned word time (ln ratio)"), ("D7", "word_time", "Word time (delta, ln ratio)"), ("D8", "ending", "Ending (delta, st)"))
_ROWS = {d: (k, label) for d, k, label in _ROWS}


def rows(comp: Comparison, B: Recording, P: Recording, regime: dict) -> list[dict]:
    """Frame rows (pitch, energy) on the participant's true time axis with the baseline warped through the word map,
    then one delta row per dimension (indexed by word, or by boundary after word i for pauses) with its tolerance per
    direction: tol = [below, above], None where that direction is never flagged."""
    n = len(P.fr)
    t = np.arange(n) * C.HOP_S
    tb = warp(t, comp.map_p, comp.map_b)
    idx = np.rint(tb / C.HOP_S).astype(int)
    inside = (idx >= 0) & (idx < len(B.fr))
    out = []
    for key, label, unit, bs, ps in (("pitch", "Pitch re median", "st", B.fr.S, P.fr.S), ("energy", "Level re voiced median", "dB", B.fr.E, P.fr.E)):
        b = np.where(inside, bs[np.clip(idx, 0, len(B.fr) - 1)], np.nan)
        out.append({"key": key, "label": label, "unit": unit, "kind": "frame", "b": _arr(b, 2), "p": _arr(ps, 2), "tol": None})
    for dim in C.DIMS:
        key, label = _ROWS[dim]
        hs = [threshold(regime, dim, sign) if dim in regime["enabled"] else None for sign in (-1, 1)]
        out.append({"key": key, "label": label, "unit": C.DIM_UNIT[dim], "kind": "boundary" if dim == "D2" else "word",
                    "status": "scored" if dim in regime["enabled"] else "listed" if dim in listed_dims(regime) else "displayed",
                    "coverage": round(comp.coverage[dim], 4), "b": [], "p": _arr(comp.dims[dim].x, 2),  # D2: every eligible boundary
                    "tol": [None if h is None else round(float(h * scale(regime, dim, sign)), 6) for sign, h in zip((-1, 1), hs)]})
    return out


_DIFF_LABEL = {"D9": ("Slower speech", "Faster speech"), "D1": ("Slower", "Faster"), "D2": ("Longer pause", "Shorter pause"), "D3": ("Wider pitch range", "Narrower pitch range"),
               "D4": ("Higher stress points", "Lower stress points"), "D6": ("Higher spectral change", "Lower spectral change"),
               "D5": ("Higher level", "Lower level"), "D7": ("Longer word time",), "D8": ("Higher ending",)}


def listed_dims(reg):
    return tuple(d for d in C.LISTED_DIMS[reg['name']] if d not in reg['enabled'] and
                 (d in reg['scales'] or all(flag_key(d, sign) in reg['scales'] for sign in C.FLAG_SIGNS[d])))


def detector_status(dim: str, reg: dict) -> str:
    return 'enabled' if dim in reg['enabled'] else 'unscored' if dim in listed_dims(reg) else 'no detector'


def detection_block(det, reg):
    listed = listed_dims(reg)
    return {'enabled': list(reg['enabled']),
            'flag_keys': [flag_key(d, sign) for d in reg['enabled'] for sign in C.FLAG_SIGNS[d] if threshold(reg, d, sign) is not None],
            'listed_keys': [flag_key(d, sign) for d in listed for sign in C.FLAG_SIGNS[d]],
            'clip_keys': [d for d in C.CLIP_DIMS if d in reg['enabled'] and reg['clip'].get(d) is not None],
            'listed_clip_keys': [d for d in C.CLIP_DIMS if d in listed and reg['clip'].get(d) is not None],
            'calibrated': bool(det.get('report', {}).get('calibrated', True))}


def _difference_regions(comp, P, reg, dims, flagged):
    candidates = []
    for k in dims:
        if k not in reg['scales'] and not any(flag_key(k, sign) in reg['scales'] for sign in C.FLAG_SIGNS[k]):
            continue  # A schema-3 artifact has no fitted D7/D8 tolerance scale.
        d = comp.dims[k]
        x = d.x.copy()
        for r in flagged:
            if r.dim == k:
                x[list(r.units)] = np.nan
        display = dataclasses.replace(d, x=x, countable=np.isfinite(x))
        decoded = [r for sign in (C.FLAG_SIGNS[k] if C.is_event(k) else (-1, 1))
                   for r in decode_dim(display, scale(reg, k, sign), C.DIFFERENCE_H, P.tr.sentence, (sign,))]
        runs = {}
        for r in decoded:
            start = r.peak
            if not C.is_event(k):
                while start > 0 and P.tr.sentence[start - 1] == P.tr.sentence[r.peak] and r.sign * x[start - 1] / scale(reg, k, r.sign) >= C.DIFFERENCE_H * C.HYSTERESIS_LOW:
                    start -= 1
            token = (r.sign, start)
            if token not in runs or abs(r.z) > abs(runs[token].z):
                runs[token] = r
        candidates += list(runs.values())
    return sorted(candidates, key=lambda r: (-abs(r.z), r.i0, r.dim))[:C.MAX_DIFFERENCES]


def exemplar_view(B: Recording, exemplar: Recording, P: Recording, comp: Comparison) -> tuple[Recording, Comparison]:
    """The reference and the comparison on the timeline of the audio that the page plays. A consensus reference has
    median word times but the frames, pause spans and audio of its first reading, so the page needs the first reading's times."""
    if B is exemplar:
        return B, comp
    shown = dataclasses.replace(B, al=exemplar.al, regions=exemplar.regions)
    map_p, map_b = time_map(shown, P)
    return shown, dataclasses.replace(comp, map_p=map_p, map_b=map_b)


def shown_info(info: dict, shown: dict, shown_ref: Recording) -> dict:
    """info with its reference span from `shown` (the same region described on the exemplar view). When the timeline
    changes the pattern, the span falls back to the words on the exemplar."""
    if (shown['pattern'], list(shown['words'])) == (info['pattern'], list(info['words'])):
        return {**info, 'b': shown['b']}
    w0, w1 = info['words']
    return {**info, 'b': (float(shown_ref.al.start[w0]), float(shown_ref.al.end[w1]))}


def _signed(v: float, unit: str) -> str:
    return f"{'+' if v > 0 else '−'}{abs(v):.3g} {unit}"


def threshold_text(reg: dict, k: str, sign: int, status: str) -> str:
    """The flag rule of a local difference in the units that the chart headings use: a factor for ln keys."""
    if status != 'difference' or k not in reg['enabled']:
        return 'This dimension is not scored.'
    h = threshold(reg, k, sign)
    if h is None:
        flagged = [s for s in C.FLAG_SIGNS[k] if threshold(reg, k, s) is not None]
        if not flagged:
            return 'Flags are disabled for this dimension.'
        return f"Only the other direction ({_DIFF_LABEL[k][min(0 if flagged[0] > 0 else 1, len(_DIFF_LABEL[k]) - 1)].lower()}) is flagged."
    thr = h * scale(reg, k, sign)
    side = 'below' if sign < 0 else 'above'
    return f"Flagged {side} ×{np.exp(sign * thr):.2f}." if C.DIM_UNIT[k] == 'ln' else f"Flagged {side} {_signed(sign * thr, C.DIM_UNIT[k])}."


# Reader-facing reasons of the owner decisions in config.OWNER_LISTED (that text is inside the detector hash, so the page
# maps it here). The R2 speech-tempo numbers: build/work/kaggle_runs/last_run/x/eval/results.json
# cross_speaker.modes.single.by_type, check readers, NATURAL_RUSH levels 2 and 3, column "flagged or among the 5 listed
# differences" (4 of 10 and 6 of 10); dev v13: 0 of 68 R2 rush edits when the key was scored.
LISTED_REASON = {
    ('R1', 'D7'): 'on unedited copies of the training speeches its measured word times changed too much to set a threshold, '
                  'so no word-time detector is available for these edits',
    ('R1', 'D8'): 'in the dataset build most rising-ending edits did not raise the measured ending by 1 semitone, so too few '
                  'ending edits remain to set and test a threshold',
    ('R2', 'D9'): 'for a different speaker it did not separate rushed words from normal speaker differences: scored in '
                  'development, it flagged 0 of 68 rush edits of other readers. In the final run, as a listed entry, it lies '
                  'on 10 of 20 natural-rush edits of the check readers (one reference, levels 2 and 3)',
}


def listed_reason(regime: str, k: str) -> str | None:
    """Why a listed dimension is unscored; None for an R2 listing without an owner decision (not yet calibrated)."""
    reason = LISTED_REASON.get((regime, k)) or C.OWNER_LISTED[regime].get(k)
    return reason or ('its validation gate failed' if regime == 'R1' else None)


def differences(comp: Comparison, B: Recording, P: Recording, reg: dict, flagged: list,
                view: tuple[Recording, Comparison] | None = None) -> list[dict]:
    """view: the exemplar view (see exemplar_view) that gives the reference spans; None means B and comp."""
    shown_ref, shown_comp = view or (B, comp)
    out = []
    for status, dims in [('difference', reg['enabled']), ('listed', listed_dims(reg))]:
        for r in _difference_regions(comp, P, reg, dims, flagged if status == 'difference' else []):
            d, k, pk = comp.dims[r.dim], r.dim, r.peak
            info = patterns.describe(r, comp, B, P, reg.get('pattern_labels'))
            info = shown_info(info, patterns.describe(r, shown_comp, shown_ref, P, reg.get('pattern_labels')), shown_ref)
            if r.dim == 'D9' and r.sign < 0 and patterns.rush_type(comp, [*flagged, r], clip_flags(comp, reg), len(flagged)) == 'RUSH':
                info = {**info, 'pattern': None}
            label = _DIFF_LABEL[k][min(0 if r.sign > 0 else 1, len(_DIFF_LABEL[k])-1)] + (' here relative to your own overall tempo' if k == 'D1' else ' here than the reference')
            baseline, participant, delta = d.reference(pk), float(d.p[pk]), float(d.x[pk])
            h = threshold(reg, k, r.sign)
            text = f"{label}: reference {baseline:.3g}, participant {participant:.3g}, delta {delta:.3g} {C.DIM_UNIT[k]}."
            text += ' ' + threshold_text(reg, k, r.sign, status)
            detail = explain.pattern_text(info, P.tr.disp[pk])
            if detail:
                text += ' ' + detail
            if info['candidate']:
                text += ' ' + explain.CANDIDATE_CLAUSE
            if explain.synthetic_only(k, info['pattern']):
                text += ' ' + explain.SYNTHETIC_ONLY_CLAUSE
            out.append({'status': status, 'dimension': k, 'brief_word': C.DIM_BRIEF[k], 'label': label,
                        'words': info['words'], 'p': _arr(info['p'], 3), 'b': _arr(info['b'], 3),
                        'baseline': round(baseline, 3), 'participant': round(participant, 3), 'delta': round(delta, 3),
                        'unit': C.DIM_UNIT[k],
                        'flag_thresholds': [r.sign * h * scale(reg, k, r.sign)] if h is not None and status == 'difference' else None,
                        'text': text,
                        'context': explain.context(P.tr, *info['words'], k), **explain.pattern_fields(info)})
        for k in C.CLIP_DIMS:
            g, thr = comp.dims[k].g, reg['clip'].get(k)
            if k not in dims or thr is None or not np.isfinite(g) or (status == 'difference' and k in clip_flags(comp, reg)) or abs(g) < C.DIFFERENCE_H * thr / C.CLIP_H:
                continue
            label = 'More uneven word timing than the reference' if k == 'D7' else _DIFF_LABEL[k][0 if g > 0 else 1] + ' overall than the reference'
            text = (f"{label}: word-time spread {g:.3g} ln, typical factor x{np.exp(g):.2f}." if k == 'D7' else
                    f"{label}: median ratio {np.exp(g):.3g}, ln difference {g:.3g}.")
            text += (f" Flagged above ×{np.exp(thr):.2f}." if k == 'D7' else f" Flagged outside ×{np.exp(-thr):.2f} to ×{np.exp(thr):.2f}."
                     if 1 in C.FLAG_SIGNS[k] else f" Flagged below ×{np.exp(-thr):.2f}.")
            out.append({'status': status, 'dimension': k, 'brief_word': C.DIM_BRIEF[k], 'label': label,
                        'words': None, 'p': None, 'b': None, 'baseline': None if k == 'D7' else 1.0,
                        'participant': round(float(g if k == 'D7' else np.exp(g)), 3), 'delta': round(float(g), 3),
                        'unit': 'ln', 'flag_thresholds': [sign * thr for sign in C.FLAG_SIGNS[k]] if status == 'difference' else None,
                        'text': text, 'context': 'whole passage',
                        'pattern': 'UNEVEN_TEMPO' if k == 'D7' and reg.get('pattern_labels', {}).get('uneven_tempo', False) else None,
                        'evidence': explain.clip_evidence(comp) if k == 'D7' else [], 'span_kind': None, 'candidate': False,
                        **({'value_unit': 'ln'} if k == 'D7' else {})})
    for i, item in enumerate(out):
        item['id'] = f'x{i + 1}'
    return out


# ============================================================================================ analyze
def _load(x) -> np.ndarray:
    if isinstance(x, np.ndarray):
        return x
    try:
        return audio.read_wav(Path(x))
    except audio.AudioError:
        return audio.load_audio(Path(x), C.MAX_UPLOAD_BYTES, C.MAX_UPLOAD_S)[0]


def analyze(participant, transcript, baseline, *, regime: str, detector: dict | None = None,
            baseline_meta: dict | None = None, participant_meta: dict | None = None, truth: list | None = None,
            aligner=None, cache_dir: Path | None = None, progress: Callable[[str], None] = lambda stage: None,
            refuse_mismatch: bool = False, alignment_device: str = "cpu", references: list | None = None) -> dict:
    """Run the pipeline. participant / baseline: canonical 16 kHz mono samples, a path, or an analysed Recording;
    transcript: text or a parsed Transcript (the words both recordings read). regime: "R1" (participant derived from the
    baseline performance) or "R2" (another performance). progress(stage) is called with "align", "features", "compare" and
    "detect" as the stages begin. refuse_mismatch (uploads): refuse a recording that does not match the transcript.
    alignment_device: device class that aligned the recordings, recorded in the result. references: optional complete ordered bank of same-text readings; the first is the display exemplar and single-reference fallback. Returns the result dict (see `dumps`)."""
    if regime not in C.REGIMES:
        raise ValueError(f"regime must be one of {C.REGIMES}, got {regime!r}")
    det = detector or load_detector(DEFAULT_DETECTOR)
    tr = transcript if isinstance(transcript, Transcript) else parse_transcript(transcript)
    progress("align")
    parts = []
    for name, x in (("baseline", baseline), ("participant", participant)):
        try:
            part = x if isinstance(x, Recording) else align_wav(_load(x), tr, aligner, cache_dir)
            if refuse_mismatch and not isinstance(part, Recording):
                require_match(part[1])
            parts.append(part)
        except TranscriptMismatch as e:
            raise TranscriptMismatch(f"{name} recording: {e}") from e
    progress("features")
    B, P = (x if isinstance(x, Recording) else make_recording(x[0], tr, x[1]) for x in parts)
    from .reference import select_reference
    refs = [B] if references is None else [x if isinstance(x, Recording) else prepare(_load(x), tr, aligner, cache_dir) for x in references]
    B, reg, mode, reference_count = select_reference(refs, det, regime)
    progress("compare")
    comp = compare(B, P)
    view = exemplar_view(B, refs[0], P, comp)
    shown_ref, shown_comp = view
    progress("detect")
    regions = decode(comp, reg, tr.sentence)
    scored = score(comp, regions, reg, det["score"]["pmax"])
    whole = clip_flags(comp, reg)
    info = [shown_info(a, s, shown_ref) for a, s in zip(patterns.annotate(comp, regions, B, P, reg.get('pattern_labels'), whole),
                                                        patterns.annotate(shown_comp, regions, shown_ref, P, reg.get('pattern_labels'), whole))]
    counted = patterns.counted(comp, regions, scored.masses, whole)
    local_flaws = [explain.build(r, comp, B, P, reg, scored.masses[i], scored, '', info[i], i in counted)
                   for i, r in enumerate(regions)]
    flaws = list(local_flaws)
    clip_entries = {k: explain.build_clip(k, comp, shown_ref, P, reg, scored) for k in scored.clip}
    flaws += list(clip_entries.values())
    flaws.sort(key=lambda f: (f["p"][0], f["dimension"], f["type"]))
    for i, f in enumerate(flaws):
        f["id"] = f"{f['dimension'].lower()}-{i + 1:03d}"
    for g in patterns.groups(comp, regions, whole):
        anchor = clip_entries.get(C.dim_of(g.anchor)) if isinstance(g.anchor, str) else None
        ids = sorted([local_flaws[j]['id'] for j in g.members] + ([anchor['id']] if anchor else []))
        for f in [local_flaws[j] for j in g.members] + ([anchor] if anchor else []):
            f['group'] = ids
            f['group_pattern'] = g.pattern
    difference_list = differences(comp,B,P,reg,regions,view) if regime == 'R2' else []
    detection = detection_block(det, reg)
    detection.update(reference_mode=mode, reference_count=reference_count, references_available=len(refs),
                     listed_entries=sum(d['status'] == 'listed' for d in difference_list),
                     show_listed=False)
    detection['show_listed'] = detection['listed_entries'] > 0
    truth = [{**t, 'available': t.get('dim', t.get('dimension')) in reg['enabled'],
              'detector_status': detector_status(t.get('dim', t.get('dimension')), reg)} for t in truth or []]
    scores = scores_block(scored, reg, regime)
    mode_note = f"Reference mode: {mode}; {reference_count} reference reading(s)."
    if mode == "consensus5":
        mode_note += " Word and window features use the median; the reference audio, waveform and word times are the first reading."
    scores['detection_note'] = mode_note + ' ' + scores.get('detection_note', '')
    return {
        "schema": 2,
        "detection": detection,
        "pipeline": {"version": __version__, "config_sha256": det["config_sha256"], "alignment_device": alignment_device},
        "regime": regime,
        "baseline": {**(baseline_meta or {}), "duration": round(B.duration, 3)},
        "participant": {**(participant_meta or {}), "duration": round(P.duration, 3)},
        "words": [{"w": tr.disp[i], "b": [round(float(shown_ref.al.start[i]), 3), round(float(shown_ref.al.end[i]), 3)],
                   "p": [round(float(P.al.start[i]), 3), round(float(P.al.end[i]), 3)]}
                  for i in range(len(tr))],
        "map": {"b": _arr(shown_comp.map_b, 3), "p": _arr(shown_comp.map_p, 3)},
        "hop": C.HOP_S,
        "rows": rows(shown_comp, shown_ref, P, reg),
        "stress": {"b": comp.stress_b, "p": comp.stress_p},
        "flaws": flaws,
        "differences": difference_list,
        "truth": truth or [],
        "scores": scores,
        "notices": [mode_note] + notices(det, regime, reg, B, P, flaws, tr),
    }


def scores_block(scored: Scored, reg: dict, regime: str = "R1") -> dict:
    dims = []
    for k in C.DIMS:
        s = scored.S[k]
        note = ((f"scored on partial coverage ({100 * scored.coverage[k]:.0f} %)" if scored.coverage[k] < C.MIN_MEASUREMENT_COVERAGE else "") if s is not None else
                "flags disabled for this dimension: no calibrated threshold" if k in reg["enabled"] and k not in flagged_dims(reg) else
                "not scored: too little measurable speech" if k in reg["enabled"] and scored.coverage[k] < C.MIN_MEASUREMENT_COVERAGE else
                f"listed, unscored: {listed_reason(regime, k)}" if k in listed_dims(reg) and listed_reason(regime, k) else
                "listed for a different performance: shown in the 'Listed, not scored' panel, not yet calibrated for scoring" if k in listed_dims(reg) else
                "not calibrated in this detector" if regime == "R1" else
                "not scored for a different performance: emphasis depends on reference stress" if k == "D4" else
                "not scored for a different performance: the clarity proxy is not comparable across speakers")
        dims.append({"key": k, "label": C.DIM_LABEL[k], "brief_word": C.DIM_BRIEF[k], "score": None if s is None else round(s, 2),
                     "scored": s is not None, "note": note, "coverage": round(scored.coverage[k], 4)})
    out = {"overall": None if scored.overall is None else round(scored.overall, 2), "dims": dims, "label": "Reference-relative delivery index"}
    if regime == 'R2':
        parts = []
        for k in reg["enabled"]:
            hs = {sign: threshold(reg, k, sign) for sign in C.FLAG_SIGNS[k]}
            ln = C.DIM_UNIT[k] == "ln"  # ln ratios are stated as plain factors
            parts.append(C.DIM_LABEL[k] + " " + ("flags disabled" if all(h is None for h in hs.values()) else
                         " / ".join(f"×{np.exp(sign * h * scale(reg, k, sign)):.2f}" if ln else f"{'+' if sign > 0 else '−'}{h * scale(reg, k, sign):.3g}"
                                    for sign, h in hs.items() if h is not None) + ("" if ln else f" {C.DIM_UNIT[k]}")))
        clip = [f"overall {name} ×{np.exp(-reg['clip'][k]):.2f}" + (f" to ×{np.exp(reg['clip'][k]):.2f}" if 1 in C.FLAG_SIGNS[k] else "")
                for k, name in (("D1", "tempo outside"), ("D3", "pitch range below")) if k in reg['enabled'] and reg["clip"].get(k) is not None]
        if 'D7' in reg['enabled'] and reg['clip'].get('D7') is not None:
            clip.append(f"word-time unevenness above ×{np.exp(reg['clip']['D7']):.2f}")
        listed = [C.DIM_LABEL[d] for d in listed_dims(reg)]
        if 'D7' in listed_dims(reg) and reg['clip'].get('D7') is not None:
            listed.append('word-time unevenness')
        out["detection_note"] = "Flag thresholds for reference departures: " + "; ".join(parts + clip) + "." + (' Listed, not scored: ' + ', '.join(listed) + '.' if listed else '')
    return out


def notices(det: dict, regime: str, reg: dict, B: Recording, P: Recording, flaws: list, tr: Transcript) -> list[str]:
    detection = detection_block(det, reg)
    name = lambda k: 'clarity' if k == 'D6' else C.DIM_LABEL[k].lower()
    enabled = ', '.join(name(k) for k in detection['enabled'])
    displayed = ', '.join(name(k) for k in C.DIMS if k not in reg['enabled'] and k not in listed_dims(reg))
    clip_names = {'D1': 'tempo', 'D3': 'pitch range', 'D7': 'word-time evenness'}
    clip = ' and '.join(clip_names[k] for k in detection['clip_keys'])
    first = (f"Regime R1: the participant is derived from the baseline performance; {len(detection['enabled'])} dimensions are enabled." if regime == 'R1' else
             f"Regime R2: a different performance; {enabled} are scored" + (f"; {displayed} are displayed only." if displayed else '.') +
             " Local pace, pitch-range and volume flags compare each stretch with the recording's own overall tempo, pitch range or level. " +
             ("Speech-tempo flags compare the aligned word time with the reference; pauses are reported separately. " if 'D9' in reg['enabled'] else '') +
             (f"A whole-clip difference in {clip} is flagged separately. " if clip else '') +
             "Pauses are compared one by one only: a shortened pause is flagged beyond the threshold in the note below. The same physical deviation scores differently in R1 and R2.")
    out = [first, 'Flags are acoustic departures from reference features; pattern names describe the measured evidence, not a diagnosis. Timing is word-boundary resolution, except evidence spans: a silence or a held sound inside a word comes from 10 ms frame measures, and inserted material or a voiced run in a gap comes from the 20 ms speech-recogniser decode.']
    if regime == 'R1':
        out += [f"{C.DIM_LABEL[k]} is unscored: {listed_reason('R1', k)}." for k in listed_dims(reg)]
    elif detection['listed_keys'] or detection['listed_clip_keys']:
        names = ', '.join(C.DIM_LABEL[k].lower() for k in listed_dims(reg))
        if detection['listed_clip_keys']:
            names += ' and ' + ', '.join(clip_names[k] for k in detection['listed_clip_keys'])
        out.append("Listed, not scored for a different performance: " + names + ". Their departures appear in the 'Listed, not scored' panel and cost no points." +
                   ''.join(f" {C.DIM_LABEL[k]}: {listed_reason('R2', k)}." for k in listed_dims(reg) if k in C.OWNER_LISTED['R2']))
    if not det.get("report", {}).get("calibrated", True):
        out.append("Uncalibrated detector (pinned threshold): for tests and fixtures only.")
    disabled = [C.DIM_LABEL[k] for k in reg["enabled"] if k not in flagged_dims(reg)]
    if disabled:
        out.append("No calibrated threshold for " + ", ".join(disabled) + "; flags disabled for these dimensions.")
    for name, rec in (("baseline", B), ("participant", P)):
        low = int((rec.al.compat < C.LOW_COMPAT_NOTICE).sum())
        if low > 0:
            out.append(f"{low} {name} word(s) have low aligner confidence (common in rushed or unclear speech); their timing is less certain.")
        if rec.fr.f0_fallback:
            out.append(f"{name}: too few voiced frames for the two-pass F0 range; the fallback range was used.")
    heur = int(sum(tr.syll_heuristic))
    if heur:
        out.append(f"{heur} word(s) use a heuristic syllable count (not in the pronunciation dictionary).")
    covered = len({i for f in flaws if f["context"] != "whole passage" for i in range(f["words"][0], f["words"][1] + 1)})
    if covered / len(tr) > C.COVERAGE_CAP:
        out.append(f"Flags cover {covered / len(tr):.0%} of the words; localisation is validated only up to {C.COVERAGE_CAP:.0%} edited-word coverage.")
    return out


# ============================================================================================ CLI
def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="python -m cvoice.pipeline", description=__doc__.splitlines()[0])
    ap.add_argument("--participant", required=True, type=Path)
    ap.add_argument("--baseline", required=True, type=Path)
    ap.add_argument("--transcript", required=True, type=Path, help="text file with the words both recordings read")
    ap.add_argument("--regime", required=True, choices=C.REGIMES)
    ap.add_argument("--detector", type=Path, default=DEFAULT_DETECTOR)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    res = analyze(a.participant, a.transcript.read_text(), a.baseline, regime=a.regime, detector=load_detector(a.detector),
                  baseline_meta={"id": a.baseline.stem, "audio": a.baseline.name},
                  participant_meta={"id": a.participant.stem, "audio": a.participant.name})
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(dumps(res) + "\n")
    print(f"{a.out}: reference-relative delivery index {res['scores']['overall']}, {len(res['flaws'])} acoustic departure(s)")


if __name__ == "__main__":
    main()
