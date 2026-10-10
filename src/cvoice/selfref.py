"""Self-relative mode: a reading graded with no reference reading (regime "SELF", detector models/detector_selfref.json).

Every measure is taken against the speaker's own typical value over the same reading, corrected for what the text
predicts at that place:
  D1 pace, D9 speech tempo: window time against the window's expected time from the text model ('phones': the CMUdict
         phone count of each word; 'norms': the learned word-duration norms of norms.py for both; 'norms_d1': the norms
         for D1 and the phone count for D9);
  D2 pauses: each boundary against the speaker's own median pause of its class (sentence end, other punctuation, none,
         and with the option tight_pauses: none inside a tight phrase);
  D3 pitch range: window value against the speaker's median, less the offset of the window's quarter of the sentence
         (declination);
  D5 volume, D6 clarity proxy: window value against the speaker's median.
Emphasis (D4), word time (D7) and endings (D8) need a reference reading: they are absent. There are no whole-clip flags.

    python -m cvoice.selfref calibrate --dataset RUN/data/dataset --cache CACHE [--workers N] [--out models/detector_selfref.json]
    python -m cvoice.selfref evaluate --dataset RUN/data/dataset --cache CACHE --splits train,val [--workers N]

Calibration is train-only: the D3 position offsets on the clean train baselines; scales on the train identity and placebo
nulls (detect.fit_scales); per-key thresholds by the R1 objective under the false-region budget on those nulls (select_h);
Pmax by the R1 score gates (calibrate.fit_pmax), with the gates reported on val.
"""
from __future__ import annotations

import argparse
import dataclasses
import functools
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

from . import __version__
from . import config as C
from .align import Transcript, _cmudict
from .compare import Comparison, _speech_time, compare
from .detect import KEYS, decode, fit_scales, scale, threshold
from .features import Recording, stress_points
from .score import score

NAME = "SELF"
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DETECTOR = ROOT / "models" / "detector_selfref.json"
NORMS_PATH = ROOT / "models" / "duration_norms.json"
SCHEMA = 1
ENABLED = ("D1", "D2", "D3", "D5", "D6", "D9")
ABSENT = ("D4", "D7", "D8")  # need a reference reading: the reference's stress words, word times or endings
# R1 objective: the same truths count as in the reference modes, so a DEEMPHASIS edit is a miss here.
EVALUATION_DIMS = ("D1", "D2", "D3", "D4", "D5", "D6", "D9")
TEXT_MODELS = ("phones", "norms", "norms_d1")
# Tempo dimensions whose expected word time comes from the learned norms, with the norms measure. 'norms_d1' keeps phones
# for D9: on the project train readings the norms raised the D9 window spread (build/work/norms/STATUS.md).
NORMS_DIMS = {"phones": {}, "norms": {"D1": "speech", "D9": "speech"}, "norms_d1": {"D1": "speech"}}
NORMS_PAUSE_MODELS = ("norms",)  # text models that take the pause classes of the norms instead of the punctuation rule

PHONES_PER_LETTER = 0.86  # median phones per letter over the CMU dictionary: phone count of a word not in it
POSITION_BINS = 4  # quarters of the sentence (relative position of the window's centre word)
POSITION_DIMS = ("D3",)  # D5 offsets lowered train and val F1 (build/work/selfref/STATUS.md)
MIN_CLASS_BOUNDARIES = 2  # a punctuation class with fewer boundaries takes the median of all punctuated boundaries
PAUSE_CLASSES = ("end", "comma", "none", "tight")
PUNCTUATED_CLASSES = ("end", "comma")
# Left word of a tight phrase (determiner or possessive + noun, preposition + object, auxiliary + verb): a pause after it
# splits a constituent (Dhamne et al. 2025 "forbidden" junctures; Taylor & Black 1998).
TIGHT_HEADS = frozenset("A AN THE MY YOUR HIS HER ITS OUR THEIR THIS THAT THESE THOSE EVERY EACH NO SOME ANY "
                        "OF IN ON AT BY FOR FROM TO WITH INTO ONTO UPON ABOUT AGAINST BETWEEN THROUGH DURING WITHOUT UNDER OVER "
                        "IS AM ARE WAS WERE BE BEEN BEING HAVE HAS HAD DO DOES DID WILL WOULD SHALL SHOULD CAN COULD MAY "
                        "MIGHT MUST".split())
FINAL_BINS = 2  # with the option final_bins: the last two words of a sentence (windows cut at the sentence end) get bins of their own
FINAL_BINS_MIN_WORDS = 4  # a shorter sentence keeps its quarter bins
TEMPO_DIMS = ("D1", "D9")
OPTIONS = {"tight_pauses": False, "boundary_strength": False, "final_bins": False, "tempo_position": False}
# Jacewicz et al. 2009 [18]: read sentences 3.40 syllables/s, SD 0.42 across speakers (articulation rate, pauses excluded).
READING_RATE_SYLL_S = (3.40, 0.42)
READING_RATE_SD = 2.0  # the listed range is the mean +- this many SDs
# Campione & Veronis 2002 [30]: pauses over 1 s occur "only in spontaneous speech", not in read speech.
LONG_PAUSE_S = 1.0


def constants() -> dict:
    """The selfref constants inside the detector hash."""
    return {"NAME": NAME, "SCHEMA": SCHEMA, "ENABLED": list(ENABLED), "ABSENT": list(ABSENT), "EVALUATION_DIMS": list(EVALUATION_DIMS),
            "TEXT_MODELS": list(TEXT_MODELS), "NORMS_DIMS": NORMS_DIMS,
            "NORMS_PAUSE_MODELS": list(NORMS_PAUSE_MODELS), "PHONES_PER_LETTER": PHONES_PER_LETTER, "POSITION_BINS": POSITION_BINS,
            "POSITION_DIMS": list(POSITION_DIMS), "FINAL_BINS": FINAL_BINS, "FINAL_BINS_MIN_WORDS": FINAL_BINS_MIN_WORDS,
            "TEMPO_DIMS": list(TEMPO_DIMS), "MIN_CLASS_BOUNDARIES": MIN_CLASS_BOUNDARIES, "PAUSE_CLASSES": list(PAUSE_CLASSES),
            "TIGHT_HEADS": sorted(TIGHT_HEADS), "OPTIONS": dict(OPTIONS), "READING_RATE_SYLL_S": list(READING_RATE_SYLL_S),
            "READING_RATE_SD": READING_RATE_SD, "LONG_PAUSE_S": LONG_PAUSE_S}


# ============================================================================================ text model
def make_model(text_model: str = "phones", position: dict | None = None, options: dict | None = None,
               norms_sha256: str | None = None) -> dict:
    """The text-model entry of the detector: the word-duration source, the sentence-position offsets and the options."""
    if text_model not in TEXT_MODELS:
        raise ValueError(f"text_model must be one of {TEXT_MODELS}, got {text_model!r}")
    unknown = set(options or {}) - set(OPTIONS)
    if unknown:
        raise ValueError(f"unknown selfref options {sorted(unknown)}")
    model = {"text_model": text_model, "position": dict(position or {}), "options": {**OPTIONS, **(options or {})}}
    if uses_norms(text_model):
        model["norms_sha256"] = norms_sha256
    return model


def uses_norms(text_model: str) -> bool:
    return bool(NORMS_DIMS[text_model])


def norms_available(path: Path = NORMS_PATH) -> bool:
    return Path(path).exists()


@functools.cache
def load_norms(path: str | None = None):
    """The learned norms (norms.load); a FileNotFoundError names the missing file."""
    target = Path(path) if path else NORMS_PATH
    if not target.exists():
        raise FileNotFoundError(f"{target} not found: the 'norms' text model needs the learned duration norms")
    from . import norms as learned  # the norms module is optional: the 'phones' text model never imports it
    return learned.load(str(target) if path else None)


def text_norms(model: dict, norms=None):
    """The norms object of a text model that uses the norms (the given one, else norms.load()); None for 'phones'."""
    if not uses_norms(model["text_model"]):
        return None
    return norms if norms is not None else load_norms()


def phone_count(norm: str) -> int:
    prons = _cmudict().get(norm.lower())
    if prons:
        return len(prons[0])
    return max(1, round(PHONES_PER_LETTER * len(norm.replace("'", ""))))


def norm_words(tr: Transcript) -> tuple[list[str], list[str]]:
    """The arguments of the norms interface: lower-case vocabulary words and the punctuation after each word."""
    return [w.lower() for w in tr.norm], list(tr.punct)


def word_weights(tr: Transcript, model: dict, norms=None, dim: str = "D1") -> np.ndarray:
    """Expected relative time of each word in the window time of the tempo dimension `dim`: exp of the norms' expected
    log duration where NORMS_DIMS names a norms measure for `dim`, else the phone count. Only ratios matter: the
    speaker's own rate is removed later."""
    measure = NORMS_DIMS[model["text_model"]].get(dim)
    if measure is None:
        return np.array([phone_count(w) for w in tr.norm], float)
    expected = np.asarray(text_norms(model, norms).expected_word_log_duration(*norm_words(tr), measure=measure), float)
    if expected.shape != (len(tr),):
        raise ValueError(f"norms gave {expected.shape} word durations for {len(tr)} words")
    return np.exp(expected)


def window_sum(values: np.ndarray, win: list) -> np.ndarray:
    return np.array([values[w[0]:w[1] + 1].sum() if w is not None else np.nan for w in win])


def sentence_bins(tr: Transcript, final_bins: bool = False) -> np.ndarray:
    """Position bin of each word: the quarter of its sentence (0..POSITION_BINS - 1) by relative position; with
    final_bins the second-to-last and last words of a sentence of FINAL_BINS_MIN_WORDS or more words take the bins
    POSITION_BINS and POSITION_BINS + 1 (final lowering and the cut windows at a sentence end, Trouvain et al. 1998)."""
    sent = np.asarray(tr.sentence)
    out = np.zeros(len(sent), int)
    for s in np.unique(sent):
        idx = np.flatnonzero(sent == s)
        rel = (idx - idx[0]) / max(1, len(idx) - 1)
        out[idx] = np.minimum((rel * POSITION_BINS).astype(int), POSITION_BINS - 1)
        if final_bins and len(idx) >= FINAL_BINS_MIN_WORDS:
            out[idx[-FINAL_BINS:]] = POSITION_BINS + np.arange(FINAL_BINS)
    return out


def position_bins(tr: Transcript, model: dict) -> np.ndarray:
    return sentence_bins(tr, bool(model["options"].get("final_bins")))


def norms_class(name: str) -> str:
    """One of PAUSE_CLASSES for a class name of the norms (sentence end, other punctuation, none, none inside a tight
    phrase); the names are matched by their words so that the two modules need not share constants."""
    text = str(name).lower()
    if "tight" in text or "inside" in text:
        return "tight"
    if "end" in text or "sentence" in text or "terminal" in text:
        return "end"
    if "punct" in text or "comma" in text or "other" in text:
        return "comma"
    return "none"


def pause_classes(tr: Transcript, model: dict | None = None, norms=None) -> np.ndarray:
    """Class of each word boundary: 'end' (a sentence ends), 'comma' (other punctuation), 'none', and with the option
    tight_pauses 'tight' (no punctuation, inside a tight phrase). A text model of NORMS_PAUSE_MODELS takes the norms' classes."""
    n = len(tr)
    tight = bool(model and model["options"].get("tight_pauses"))
    learned = text_norms(model, norms) if model and model["text_model"] in NORMS_PAUSE_MODELS else None
    if learned is not None:
        names = [norms_class(c) for c in learned.pause_class(*norm_words(tr))][:n - 1]
        if len(names) != n - 1:
            raise ValueError(f"norms gave {len(names)} pause classes for {n - 1} boundaries")
        return np.array([c if tight or c != "tight" else "none" for c in names])
    out = []
    for i in range(n - 1):
        if tr.sentence[i + 1] != tr.sentence[i]:
            out.append("end")
        elif tr.punct[i]:
            out.append("comma")
        elif tight and tr.norm[i] in TIGHT_HEADS:
            out.append("tight")
        else:
            out.append("none")
    return np.array(out)


# ============================================================================================ measures
def _against_own(measure: np.ndarray, expected: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(x, typical): x = measure - expected less its median over the reading; typical = expected + that median, the value
    the speaker shows at this place at their own overall level."""
    rel = measure - expected
    ok = np.isfinite(rel)
    centre = float(np.median(rel[ok])) if ok.any() else float("nan")
    return rel - centre, expected + centre


def _tempo(P: Recording, time_s: np.ndarray, weights: np.ndarray, offsets=None, bins=None) -> tuple[np.ndarray, np.ndarray]:
    """(x ln, typical time s) of a window time against its expected time at the speaker's own tempo (with `offsets`: ln
    offset per position bin)."""
    with np.errstate(divide="ignore", invalid="ignore"):
        expected = np.log(window_sum(weights, P.win))
        if offsets is not None:
            expected = expected + np.asarray(offsets, float)[bins]
        x, typical = _against_own(np.log(time_s), expected)
    return x, np.exp(typical)


def _position(P: Recording, values: np.ndarray, offsets, bins) -> tuple[np.ndarray, np.ndarray]:
    expected = np.asarray(offsets, float)[bins] if offsets is not None else np.zeros(len(values))
    return _against_own(values, expected)


def lengthening(P: Recording, weights: np.ndarray) -> np.ndarray:
    """Per word: aligned duration above its expected duration at the speaker's own median time per weight unit (s, >= 0)."""
    duration = np.asarray(P.al.end - P.al.start, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        per_unit = duration / weights
    ok = np.isfinite(per_unit)
    rate = float(np.median(per_unit[ok])) if ok.any() else 0.0
    return np.maximum(duration - weights * rate, 0.0)


def boundary_measure(P: Recording, classes: np.ndarray, weights: np.ndarray | None) -> np.ndarray:
    """Per boundary, s: the raw pause; with `weights` (option boundary_strength) the pause plus the lengthening of the
    word before a punctuated boundary, because a reader can mark a boundary by lengthening instead of silence
    (Ferreira 1993; Bailly et al. 2022)."""
    raw = np.asarray(P.sil_raw, float)
    if weights is None:
        return raw
    return np.where(np.isin(classes, PUNCTUATED_CLASSES), raw + lengthening(P, weights)[:-1], raw)


def expected_pauses(measure: np.ndarray, classes: np.ndarray) -> np.ndarray:
    """Per boundary: the speaker's own median of `measure` (s) over the boundaries of its class. A punctuated class with
    fewer than MIN_CLASS_BOUNDARIES boundaries takes the median over all punctuated boundaries."""
    out = np.full(len(measure), np.nan)
    punct = np.isin(classes, PUNCTUATED_CLASSES)
    for name in PAUSE_CLASSES:
        group = classes == name
        pool = group if group.sum() >= MIN_CLASS_BOUNDARIES or name not in PUNCTUATED_CLASSES else punct
        if group.any() and pool.any():
            out[group] = float(np.median(measure[pool]))
    return out


def _pauses(P: Recording, base: Comparison, classes: np.ndarray, measure: np.ndarray, tight_only: bool):
    """D2 under the reference rules (compare.d2_pauses) with the class median in the place of the reference pause. With
    tight_only, a longer pause counts only inside a tight phrase: a pause at another unpunctuated juncture can be a
    normal phrase break (Taylor & Black 1998: half the breaks of read speech are unpunctuated)."""
    n = len(P.tr)
    expected = expected_pauses(measure, classes)
    elig = (expected >= C.PAUSE_MIN_S) | (P.sil >= C.PAUSE_MIN_S)
    x = np.where(elig, measure - expected, np.nan)
    punct = np.isin(classes, PUNCTUATED_CLASSES)
    may_lengthen = (classes == "tight") if tight_only else ~punct
    countable = elig & (((x < 0) & (expected >= C.PAUSE_DROP_MIN_BASE_S)) | ((x > 0) & (expected < C.PAUSE_MIN_S) & may_lengthen))
    events = max(1, int((expected >= C.PAUSE_MIN_S).sum()))
    return dataclasses.replace(base.dims["D2"], x=x, b=np.where(elig, expected, np.nan), p=np.where(elig, measure, np.nan),
                               countable=countable, w=np.full(n - 1, 1.0 / events))


def self_dims(P: Recording, model: dict, base: Comparison, norms=None) -> dict:
    """The self-relative Dim of every dimension; `base` (P against itself) gives the weights."""
    dims = dict(base.dims)
    options = model["options"]
    weights = {dim: word_weights(P.tr, model, norms, dim) for dim in TEMPO_DIMS}
    bins = position_bins(P.tr, model)
    for dim, measured in zip(TEMPO_DIMS, tempo_times(P)):
        x, typical = _tempo(P, measured, weights[dim], model["position"].get(dim), bins)
        dims[dim] = dataclasses.replace(base.dims[dim], x=x, b=typical, p=np.asarray(measured, float), countable=np.isfinite(x), g=float("nan"))
    x, typical = _position(P, np.log(P.win_R + C.RANGE_REG_ST), model["position"].get("D3"), bins)
    dims["D3"] = dataclasses.replace(base.dims["D3"], x=x, b=np.exp(typical) - C.RANGE_REG_ST, p=np.asarray(P.win_R, float), g=float("nan"))
    x, typical = _against_own(np.asarray(P.win_E, float), np.zeros(len(P.win_E)))
    dims["D5"] = dataclasses.replace(base.dims["D5"], x=x, b=typical, p=np.asarray(P.win_E, float))
    x, typical = _against_own(np.log(P.win_Q + 1e-6), np.zeros(len(P.win_Q)))
    dims["D6"] = dataclasses.replace(base.dims["D6"], x=x, b=np.exp(typical) - 1e-6, p=np.asarray(P.win_Q, float))
    classes = pause_classes(P.tr, model, norms)
    measure = boundary_measure(P, classes, weights["D9"] if options.get("boundary_strength") else None)  # D9: aligned word spans
    dims["D2"] = _pauses(P, base, classes, measure, bool(options.get("tight_pauses")))
    for dim in ABSENT:
        nan = np.full(len(base.dims[dim].x), np.nan)
        dims[dim] = dataclasses.replace(base.dims[dim], x=nan, b=nan.copy(), p=nan.copy(), countable=np.zeros(len(nan), bool), g=float("nan"))
    return dims


def self_comparison(P: Recording, model: dict, norms=None) -> Comparison:
    """The comparison of a reading with its own expected delivery: P against itself for the time map, weights and stress
    words, then every dimension replaced by its self-relative measure (self_dims)."""
    base = compare(P, P)
    dims = self_dims(P, model, base, norms)
    share = base.dims["D1"].w
    coverage = {**base.coverage, **{k: float(share[np.isfinite(dims[k].x)].sum()) for k in ("D1", "D3", "D5", "D6", "D9")}}
    coverage.update({k: 0.0 for k in ABSENT})
    return dataclasses.replace(base, dims=dims, coverage=coverage)


def tempo_times(P: Recording) -> tuple[np.ndarray, np.ndarray]:
    """Window times of D1 (speech time without pauses) and D9 (sum of the aligned word durations), s."""
    return _speech_time(P, P.sil >= C.PAUSE_MIN_S), np.asarray(P.win_W, float)


def position_measure(P: Recording, dim: str, model: dict, norms=None) -> np.ndarray:
    if dim in TEMPO_DIMS:
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.log(tempo_times(P)[TEMPO_DIMS.index(dim)]) - np.log(window_sum(word_weights(P.tr, model, norms, dim), P.win))
    return np.log(P.win_R + C.RANGE_REG_ST) if dim == "D3" else np.asarray(P.win_E, float)


def fit_position(recs: list[Recording], dim: str, model: dict, norms=None) -> list[float]:
    """Offset per position bin: the median over clean readings of the measure less its reading's median."""
    rel, bins = [], []
    for P in recs:
        v = position_measure(P, dim, model, norms)
        rel.append(v - np.nanmedian(v))
        bins.append(position_bins(P.tr, model))
    rel, bins = np.concatenate(rel), np.concatenate(bins)
    count = POSITION_BINS + (FINAL_BINS if model["options"].get("final_bins") else 0)
    return [round(float(np.nanmedian(rel[bins == b])), 6) if (bins == b).any() else 0.0 for b in range(count)]


# ============================================================================================ listed context (not scored)
def emphasis_contrast(P: Recording) -> list[dict]:
    """Per sentence: median stress points of the content words less that of the function words, and the share of words
    at or above the stress-point marker. In read news a text prior of 'accent every content word' is right 82 % of the
    time (Nielsen et al. 2020), so a small contrast is a flat pattern; a large share is a uniform pattern (Sabu et al. 2018)."""
    points = stress_points(P.ws.u, P.m, P.sigma)
    function = np.array([w in C.FUNCTION_WORDS for w in P.tr.norm])
    out = []
    for s in range(P.tr.n_sentences):
        first, last = P.tr.sentence_words(s)
        idx = np.arange(first, last + 1)
        ok = np.isfinite(points[idx])
        content, func = idx[ok & ~function[idx]], idx[ok & function[idx]]
        contrast = float(np.median(points[content]) - np.median(points[func])) if content.size and func.size else float("nan")
        share = float(np.mean(points[idx[ok]] >= C.STRESS_P_MIN)) if ok.any() else float("nan")
        out.append({"sentence": s, "words": [int(first), int(last)], "contrast": contrast, "prominent_share": share})
    return out


def articulation_rate(P: Recording) -> float:
    """Syllables per second of speech: the span from the first word start to the last word end less the acoustic pauses."""
    speech = float(P.al.end[-1] - P.al.start[0] - np.sum(P.sil[P.sil >= C.PAUSE_MIN_S]))
    return float(sum(P.tr.syll)) / speech if speech > 0 else float("nan")


def long_pauses(P: Recording) -> list[int]:
    """Boundaries whose silent pause is longer than LONG_PAUSE_S."""
    return [int(i) for i in np.flatnonzero(np.asarray(P.sil_raw, float) > LONG_PAUSE_S)]


# ============================================================================================ regime and thresholds
def regime(scales: dict, h: dict | None = None) -> dict:
    """A regime entry in the shape of detector.json, so that detect.decode and score.score apply unchanged; no whole-clip
    thresholds and no pattern labels (each label compares with a reference)."""
    return {"name": NAME, "enabled": list(ENABLED), "scales": {k: round(float(v), 6) for k, v in scales.items()},
            "h": dict(h) if h is not None else dict.fromkeys(KEYS), "clip": dict.fromkeys(C.CLIP_DIMS), "pattern_labels": {}}


def flag_keys() -> list[str]:
    return [k for k in KEYS if C.dim_of(k) in ENABLED]


def train_counts(pairs: list, controls: list, reg: dict) -> dict:
    """Strict TP / FP / FN over the train positives (`pairs`: (Run, labels)) with every control region counted as false:
    the R1 selection objective (calibrate.select_r1) without its separate speech-tempo component."""
    from .events import eval_clip
    tp = fp = fn = 0
    for run, lab in pairs:
        ev = eval_clip(dataclasses.replace(run, regions=decode(run.comp, reg, run.P.tr.sentence), clip={}), lab, secondary_exempt=False)
        found = sum(bool(t["detected"]) for t in ev["truth"] if t["available"])
        tp, fn = tp + found, fn + sum(t["available"] for t in ev["truth"]) - found
        fp += len(ev["false"]) + len(ev["false_clip"])
    controls_fp = sum(len(decode(n.comp, reg, n.sentence)) for n in controls)
    fp += controls_fp
    return {"TP": tp, "FP": fp, "FN": fn, "F1": 2 * tp / (2 * tp + fp + fn) if tp + fp + fn else 0.0, "control_regions": controls_fp}


def null_regions(nulls: list, reg: dict) -> int:
    """False regions on null comparisons, one per change (evaluate.null_flags)."""
    from .evaluate import null_flags
    return sum(len(null_flags(n, reg)) for n in nulls)


def select_h(pairs: list, controls: list, nulls: list, reg: dict) -> dict:
    """Per-key thresholds: the R1 objective (train_counts) maximised under the product's false-region budget
    (FALSE_RATE_BUDGET per minute over the train nulls `nulls`). Start: the best common h on H_GRID within the budget; then
    coordinate ascent over the flag keys until no key changes; ties keep the smaller h sum."""
    budget = C.FALSE_RATE_BUDGET * sum(n.minutes for n in nulls)
    keys = flag_keys()

    def trial(h: dict) -> dict | None:
        reg["h"] = {k: h.get(k) for k in KEYS}
        if null_regions(nulls, reg) > budget:
            return None
        return train_counts(pairs, controls, reg)

    def rank(row: dict, h: dict) -> tuple:
        return row["F1"], -sum(h.values())

    best_h, best = None, None
    for value in C.H_GRID:
        h = dict.fromkeys(keys, value)
        row = trial(h)
        if row is not None and (best is None or rank(row, h) > rank(best, best_h)):
            best_h, best = h, row
    if best is None:
        raise ValueError("no common threshold meets the false-region budget on the train nulls")
    start = dict(best_h)
    changed, sweeps = True, 0
    while changed:
        changed, sweeps = False, sweeps + 1
        for k in keys:
            for value in C.H_GRID:
                h = {**best_h, k: value}
                row = trial(h)
                if row is not None and rank(row, h) > rank(best, best_h):
                    best_h, best, changed = h, row, True
    reg["h"] = {k: best_h.get(k) for k in KEYS}
    return {"common_start": start[keys[0]], "sweeps": sweeps, "train": best, "budget_regions": budget,
            "null_regions": null_regions(nulls, reg), "null_minutes": round(sum(n.minutes for n in nulls), 3),
            "rule": "per-key h: R1 objective (strict train F1, controls counted as false) under the train-null budget; "
                    "start at the best common h; coordinate ascent; ties keep the smaller h sum"}


def selection_labels(lab: dict) -> dict:
    """Labels for threshold selection: flaws outside the calibration types are excluded (calibrate.select_r1)."""
    from .calibrate import calibration_types
    allowed = calibration_types()
    return {**lab, "flaws": [f if f["type"] in allowed else {**f, "evaluation_excluded": ["outside h-selection types"]} for f in lab["flaws"]]}


def selection_clip(lab: dict) -> bool:
    from .calibrate import calibration_types
    return any(f.get("type") in calibration_types() for f in lab["flaws"])


def self_run(P: Recording, comp: Comparison, regions=()):
    from .events import Run
    return Run(P, P, comp, list(regions), None, NAME, {}, None, EVALUATION_DIMS)


# ============================================================================================ Pmax
def gate_row(clip_id: str, baseline: str, recipe: str, levels: list, comp: Comparison, reg: dict) -> dict:
    """One score-gate row (calibrate.clip_penalties) of a clip under the SELF regime."""
    sc = score(comp, decode(comp, reg, comp.sentence), reg, dict(C.PMAX_START))
    return {"id": clip_id, "baseline": baseline, "recipe": recipe, "P": sc.P, "scored_dims": [k for k, v in sc.S.items() if v is not None],
            "levels": levels, "n_regions": int(sum(m > 0 for m in sc.masses))}


def fit_pmax(train_rows: list[dict], val_rows: list[dict]) -> tuple[dict, dict]:
    """Pmax by the R1 score gates on the train rows (calibrate.fit_pmax); the val gates only report."""
    from .calibrate import fit_pmax as fit_gates, gate_violations
    pmax, factor, bad_train = fit_gates(train_rows)
    return ({k: round(float(v), 6) for k, v in pmax.items()},
            {"pmax_factor": round(float(factor), 4), "gates_train": {"violations": bad_train, "n_clips": len(train_rows)},
             "gates_val": {"violations": gate_violations(val_rows, pmax), "n_clips": len(val_rows)}})


# ============================================================================================ fit
def fit_text_model(model: dict, train_baselines: list[Recording], norms=None) -> dict:
    """The model with its sentence-position offsets fitted on clean readings (calibration: the train baselines); the
    option tempo_position adds offsets for D1 and D9 (phrase-final lengthening)."""
    dims = POSITION_DIMS + (TEMPO_DIMS if model["options"].get("tempo_position") else ())
    return {**model, "position": {dim: fit_position(train_baselines, dim, model, norms) for dim in dims}}


def fit_detector(model: dict, nulls: list, controls: list, pairs: list, gate_train: list[tuple], gate_val: list[tuple],
                 norms=None, scale_nulls: list | None = None) -> dict:
    """The SELF calibration on analysed train inputs, all compared under `model` (fit_text_model). nulls: calibrate.Null
    objects with self comparisons (train identity and placebo, and any extra clean readings); controls: the nulls plus the
    20 dB noise controls; pairs: (Run, labels) of the train positives; gate_*: (id, baseline, recipe, levels, Recording)
    score-gate clips; scale_nulls: the nulls of the scale fit when they differ from `nulls` (the budget nulls)."""
    scales, _, _ = fit_scales([n.comp for n in (nulls if scale_nulls is None else scale_nulls)])
    reg = regime(scales)
    selection = select_h(pairs, controls, nulls, reg)

    def rows(items):
        return [gate_row(i, b, r, lv, self_comparison(P, model, norms), reg) for i, b, r, lv, P in items]

    pmax, gates = fit_pmax(rows(gate_train), rows(gate_val))
    return make_detector(model, reg, pmax, {"calibrated": True, "selection": selection, **gates,
                                            "train_nulls": sorted({n.id for n in nulls}), "controls": len(controls)})


# ============================================================================================ detector file
def detector_hash(det: dict) -> str:
    """SHA-256 over the selfref constants, the config constants, the text model, the regime and Pmax (a SELF detector
    has its own hash: detect.config_hash and the reference detector stay untouched)."""
    reg = det["regime"]
    state = {"selfref": constants(), "config": C.as_dict(), "schema": det["schema"], "text_model": det["text_model"],
             "regime": {k: reg[k] for k in ("name", "enabled", "scales", "h", "clip", "pattern_labels")}, "pmax": det["score"]["pmax"]}
    return hashlib.sha256(json.dumps(state, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def make_detector(model: dict, reg: dict, pmax: dict, report: dict) -> dict:
    det = {"schema": SCHEMA, "name": NAME, "pipeline_version": __version__, "text_model": model, "regime": reg,
           "score": {"pmax": {k: round(float(v), 6) for k, v in pmax.items()}}, "report": report}
    det["selfref_sha256"] = detector_hash(det)
    return det


def save_detector(det: dict, path: Path = DEFAULT_DETECTOR) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(det, indent=1, sort_keys=True) + "\n")


def sha256_path(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@functools.cache
def _load_cached(path: str, stamp: float) -> dict:
    return load_detector(Path(path))


def load_default() -> dict:
    """The shipped SELF detector, read once per file version."""
    return _load_cached(str(DEFAULT_DETECTOR), DEFAULT_DETECTOR.stat().st_mtime if DEFAULT_DETECTOR.exists() else 0.0)


def load_detector(path: Path = DEFAULT_DETECTOR) -> dict:
    """Read and verify a SELF detector: schema, flag keys and hash; a 'norms' text model also needs the same norms file."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found: run `python -m cvoice.selfref calibrate` first")
    det = json.loads(path.read_text())
    if det.get("schema") != SCHEMA or det.get("name") != NAME:
        raise ValueError(f"{path}: not a SELF detector of schema {SCHEMA}")
    if set(det["regime"]["h"]) != set(KEYS):
        raise ValueError(f"{path}: needs a threshold entry per flag key")
    if det["selfref_sha256"] != detector_hash(det):
        raise ValueError(f"{path}: selfref hash mismatch (constants changed since calibration)")
    model = det["text_model"]
    if uses_norms(model["text_model"]) and model.get("norms_sha256") and (not norms_available() or sha256_path(NORMS_PATH) != model["norms_sha256"]):
        raise ValueError(f"{path}: the norms file {NORMS_PATH} is missing or differs from the one used in calibration")
    return det


# ============================================================================================ evaluation (train / val)
EVAL_LEVELS = {"L2+L3": (2, 3), "L1": (1,)}


def evaluate_items(reg: dict, clips: list[tuple], nulls: list[tuple], tiers: dict, splits=("train", "val")) -> dict:
    """Both accountings per split, tier and level group, and the false regions on the nulls. clips: (clip entry,
    Recording, comparison, labels) of single clips; nulls: (split, is_noise_control, Null)."""
    from .addendum import counts
    from .evaluate import null_flags, tier_labels
    from .events import eval_clip, f1
    out = {}
    for split in splits:
        for level_name, levels in EVAL_LEVELS.items():
            for tier, types in tiers.items():
                once, pre = np.zeros(4, int), np.zeros(3, int)
                for c, P, comp, lab in clips:
                    if c["split"] != split or c["level"] not in levels or not any(f["type"] in types for f in lab["flaws"]):
                        continue
                    ev = eval_clip(self_run(P, comp, decode(comp, reg, comp.sentence)), tier_labels(lab, types), secondary_exempt=False)
                    k = counts(ev)
                    once += [k["tp"], k["fp"], k["dup"], k["fn"]]
                    pre += k["pre"]
                out[f"{tier}|{level_name}|{split}"] = {"once_tp_fp_dup_fn": once.tolist(), "once_f1": f1(once[0], once[1], once[3])["f1"],
                                                       "pre_tp_fp_fn": pre.tolist(), "pre_f1": f1(*pre)["f1"]}
        clean = [n for sp, noise, n in nulls if sp == split and not noise]
        flags = [null_flags(n, reg) for n in clean]
        minutes = sum(n.minutes for n in clean)
        out[f"nulls|{split}"] = {"regions": sum(map(len, flags)), "minutes": round(minutes, 3),
                                 "per_minute": round(sum(map(len, flags)) / minutes, 3) if minutes else None,
                                 "by_key": dict(sorted(Counter(k for f in flags for k in f).items()))}
        noisy = [n for sp, noise, n in nulls if sp == split and noise]
        out[f"noise|{split}"] = sum(len(null_flags(n, reg)) for n in noisy)
    return out


# ============================================================================================ dataset driver
def _inputs(ds, splits: tuple[str, ...]):
    """Analysed inputs of the splits: baselines, single / identity / ladder clips with labels, and the R1 nulls (identity,
    placebo seeds, 20 dB noise controls of the identity clips)."""
    from .calibrate import calibration_clip, r1_items, r1_noise_items
    bases = [b for b in ds.manifest["baselines"] if b["split"] in splits]
    clips = [c for c in ds.manifest["clips"] if c["kind"] in ("single", "identity", "ladder") and c["split"] in splits]
    ds.load(entries=bases, clips=clips)
    clip_recs = ds.clip_recs(clips)
    items = r1_items(ds, splits)
    identities = [c for c in clips if c["kind"] == "identity" and calibration_clip(c)]
    noise = [{**item, "split": c["split"]} for item, c in zip(r1_noise_items(ds, identities), identities)]  # r1_noise_items marks every item train
    recs = ds.prepare_many([(i["wav"], i["tr"]) for i in items + noise])
    nulls = [(i, P, k >= len(items)) for k, (i, P) in enumerate(zip(items + noise, recs))]
    return {b["id"]: (b, ds.rec(b)) for b in bases}, list(zip(clips, clip_recs)), nulls


def null_of(item: dict, P: Recording, comp: Comparison):
    from .calibrate import Null
    return Null(item["id"], comp, P.tr.sentence, P.duration / 60, item["split"], reader=item["id"].split("__")[0])


def gate_items(ds, clips: list[tuple], split: str) -> list[tuple]:
    """Score-gate clips of a split (calibrate.run: single, identity and ladder clips of the calibration types)."""
    from .calibrate import calibration_clip
    out = []
    for c, P in clips:
        if c["split"] != split or not calibration_clip(c):
            continue
        lab = ds.labels(c)
        out.append((c["id"], c["parent"], c["recipe"], sorted({f["level"] for f in lab["flaws"] if f["level"] is not None}), P))
    return out


READER_ROLES = ("scales", "budget", "controls")


def reader_nulls(ds, model: dict, sources: tuple[str, ...], norms=None) -> list:
    """Extra clean nulls: the R2 fit-phase readings of `sources` (the select and lockbox readers stay untouched), each
    against its own expected delivery."""
    from .calibrate import Null
    groups = [g for g in ds.manifest.get("r2_pool", {}).get("groups", []) if g["source"] in sources]
    entries = [(g["source"], ds.entry("readers", rid)) for g in groups for rid in g["sets"]["fit"]]
    recs = ds.recs([e for _, e in entries])
    return [Null(e["id"], self_comparison(P, model, norms), P.tr.sentence, P.duration / 60, "train", reader=e["id"], source=source)
            for (source, e), P in zip(entries, recs)]


def calibrate(dataset: Path, cache: Path | None = None, workers: int | None = None, out: Path | None = DEFAULT_DETECTOR,
              text_model: str = "phones", options: dict | None = None, pool=None, norms=None,
              reader_sources: tuple[str, ...] = (), reader_roles: tuple[str, ...] = ("budget",)) -> dict:
    """Calibrate the SELF detector from the dataset (train only; val gates reported) and write it to `out`.
    reader_sources: R2 fit-phase sources whose readings join the train nulls in reader_roles (READER_ROLES: the scale
    fit, the false-region budget of select_h, the false regions of the selection objective)."""
    if set(reader_roles) - set(READER_ROLES):
        raise ValueError(f"reader_roles must be among {READER_ROLES}")
    from .dataset import load_dataset
    from .pool import PreparePool
    own_pool = pool is None
    pool = pool or PreparePool(workers=workers, devices=["cpu"], cache_dir=cache)
    try:
        ds = load_dataset(Path(dataset), cache, pool)
        norms_sha = sha256_path(NORMS_PATH) if uses_norms(text_model) and norms is None else None
        bases, clips, null_inputs = _inputs(ds, ("train", "val"))
        model = fit_text_model(make_model(text_model, options=options, norms_sha256=norms_sha),
                               [P for b, P in bases.values() if b["split"] == "train"], norms)
        nulls = [(i, null_of(i, P, self_comparison(P, model, norms)), noise) for i, P, noise in null_inputs if i["split"] == "train"]
        own = [n for i, n, noise in nulls if not noise]
        readers = reader_nulls(ds, model, tuple(reader_sources), norms) if reader_sources else []
        budget = own + (readers if "budget" in reader_roles else [])
        scale_nulls = own + (readers if "scales" in reader_roles else [])
        controls = own + (readers if "controls" in reader_roles else []) + [n for i, n, noise in nulls if noise]
        pairs = [(self_run(P, self_comparison(P, model, norms)), selection_labels(ds.labels(c))) for c, P in clips
                 if c["kind"] == "single" and c["split"] == "train" and c["level"] in C.HEADLINE_LEVELS and selection_clip(ds.labels(c))]
        det = fit_detector(model, budget, controls, pairs, gate_items(ds, clips, "train"), gate_items(ds, clips, "val"), norms, scale_nulls)
        det["report"]["readers"] = {"sources": list(reader_sources), "roles": list(reader_roles) if reader_sources else [],
                                    "readings": len(readers), "minutes": round(sum(n.minutes for n in readers), 3)}
        det["report"]["manifest_sha256"] = hashlib.sha256((Path(dataset) / "manifest.json").read_bytes()).hexdigest()
    finally:
        if own_pool:
            pool.close()
    if out is not None:
        save_detector(det, out)
    return det


def evaluate(det: dict, dataset: Path, cache: Path | None = None, workers: int | None = None, splits=("train", "val"),
             pool=None, norms=None) -> dict:
    """evaluate_items on the dataset's clips and R1 nulls of `splits`, with the tiers of the frozen reference detector."""
    from .dataset import load_dataset
    from .detect import load_detector as load_reference
    from .pool import PreparePool
    from .protocol import tiers
    own_pool = pool is None
    pool = pool or PreparePool(workers=workers, devices=["cpu"], cache_dir=cache)
    try:
        ds = load_dataset(Path(dataset), cache, pool)
        model = det["text_model"]
        _, clips, null_inputs = _inputs(ds, tuple(splits))
        singles = [(c, P, self_comparison(P, model, norms), ds.labels(c)) for c, P in clips if c["kind"] == "single"]
        nulls = [(i["split"], noise, null_of(i, P, self_comparison(P, model, norms))) for i, P, noise in null_inputs]
    finally:
        if own_pool:
            pool.close()
    reference = load_reference(ROOT / "models" / "detector.json")
    return evaluate_items(det["regime"], singles, nulls, tiers(reference["report"].get("real_validation")), tuple(splits))


# ============================================================================================ product texts
def describe_flaw(entry: dict, region, comp: Comparison, P: Recording, reg: dict, model: dict, norms=None) -> dict:
    """The flaw entry of explain.build with self-relative wording: measure, text and fix compare with the speaker's own
    typical delivery over this reading; no pattern label and no reference evidence."""
    k, sign, pk = region.dim, region.sign, region.peak
    dim = comp.dims[k]
    tr = P.tr
    w0, w1 = entry["words"]
    words, where = tr.text(w0, w1), f"{entry['p'][0]:.2f}-{entry['p'][1]:.2f} s"
    typical, measured, x = float(dim.reference(pk)), float(dim.p[pk]), float(dim.x[pk])
    theta = threshold(reg, k, sign) * scale(reg, k, sign)
    mult = abs(x) / theta
    if k in ("D1", "D9"):
        faster = sign < 0
        pct, pct_thr = (math.exp(abs(x)) - 1) * 100, (math.exp(theta) - 1) * 100
        what_measure = "speech time" if k == "D1" else "aligned word time (pauses not included)"
        basis = ("from the usual timing of these words in read speech" if NORMS_DIMS[model["text_model"]].get(k)
                 else "from their length in sounds")
        what = (f"{'Faster' if faster else 'Slower'} here than the rest of your reading: {where} ('{words}')." if k == "D1" else
                f"The words themselves were spoken faster here than in the rest of your reading: {where} ('{words}').")
        how = (f"The word alignment measures {measured:.2f} s of {what_measure} in the five-word window at the peak; at your own "
               f"typical pace these words take {typical:.2f} s (expected {basis}), {pct:.0f}% "
               f"{'faster' if faster else 'longer'} ({mult:.1f}x the threshold; flagged beyond {pct_thr:.0f}%).")
        fix = (f"Slow these words to about {typical:.1f} s, in step with the rest of your reading." if faster else
               f"Tighten these words to about {typical:.1f} s, in step with the rest of your reading.")
        measure = f"{what_measure} of the five-word window at the peak, s (expected time at your own typical pace)"
    elif k == "D2":
        prev, nxt = tr.disp[w0], tr.disp[w0 + 1]
        place = {"end": "sentence ends", "comma": "punctuation marks", "tight": "places without punctuation"}.get(
            str(pause_classes(tr, model, norms)[w0]), "places without punctuation")
        if sign < 0:
            what = f"Shorter pause after '{prev}' at {entry['p'][0]:.2f} s than your own pauses at {place}."
            how = (f"The word alignment measures {measured:.2f} s here; at {place} you typically pause {typical:.2f} s "
                   f"({mult:.1f}x the threshold; flagged when {theta:.2f} s shorter).")
            fix = f"Stop fully after '{prev}' and hold about {typical:.1f} s before '{nxt}', as you do at your other {place}."
        else:
            unmarked = "" if tr.punct[w0] else "; the transcript has no punctuation here"
            what = f"Longer pause after '{prev}' at {entry['p'][0]:.2f} s than your own pauses at {place}."
            how = (f"The word alignment measures {measured:.2f} s of silence between '{prev}' and '{nxt}'; at {place} you "
                   f"typically pause {typical:.2f} s{unmarked} ({mult:.1f}x the threshold; flagged when {theta:.2f} s longer).")
            fix = (f"Shorten the pause after '{prev}' to about {typical:.1f} s." if tr.punct[w0] else
                   f"Carry '{prev} {nxt}' on one breath; take the breath at the next punctuation mark.")
        measure = "silent pause at the word boundary, s (your own typical pause at boundaries of the same kind)"
    elif k == "D3":
        what = f"Narrower pitch range here than in the rest of your reading: {where} ('{words}')."
        how = (f"Your pitch range is {measured:.1f} st here; at this place in a sentence your typical range is {typical:.1f} st "
               f"({mult:.1f}x the threshold; the ranges are compared as a ratio with {C.RANGE_REG_ST:.0f} st added to each, "
               f"flagged below x{math.exp(-theta):.2f}).")
        fix = f"Let your pitch move about {typical:.1f} st across these words, as it does elsewhere in your reading."
        measure = "pitch range P90-P10 over the five-word window at the peak, st (your own typical range at this place in a sentence)"
    elif k == "D5":
        what = f"Quieter here than the rest of your reading: {where} ('{words}')."
        how = (f"You are at {measured:.1f} dB here relative to your median voiced level; your typical level is {typical:.1f} dB, "
               f"{abs(x):.1f} dB higher ({mult:.1f}x the threshold; flagged when {theta:.1f} dB lower).")
        fix = f"Keep these words at the level of the rest of your reading, about {abs(x):.1f} dB louder."
        measure = "mean level over the five-word window at the peak, dB re your median voiced level"
    else:
        what = f"Lower spectral change here than in the rest of your reading: {where} ('{words}')."
        how = (f"Spectral change per frame is {measured:.2f} against your typical {typical:.2f}, {(1 - math.exp(x)) * 100:.0f}% lower "
               f"({mult:.1f}x the threshold; flagged beyond {(1 - math.exp(-theta)) * 100:.0f}%).")
        fix = "Listen to this span; this proxy does not measure intelligibility."
        measure = "MFCC delta magnitude over the five-word window at the peak (your own typical value)"
    caveat = " The span is approximate: this measure uses five-word windows." if k in ("D1", "D3", "D5", "D6", "D9") else ""
    lost, fixed = entry["points_lost"], entry["overall_if_fixed"]
    effect = (f" Costs {lost:.1f} points of the delivery index relative to your own reading; score with this penalty removed: {fixed:.1f}."
              if fixed is not None and lost is not None else "")
    return {**entry, "measure": measure, "baseline": round(typical, 2), "text": f"{what} {how}{caveat}{effect}", "fix": fix,
            "pattern": None, "evidence": [], "candidate": False}


def listed_context(P: Recording, det: dict) -> list[dict]:
    """Listed, not scored: the overall articulation rate against read-speech norms [18], pauses longer than LONG_PAUSE_S [30],
    and (when the detector has emphasis thresholds) flat or uniform emphasis per sentence."""
    out = []
    rate = articulation_rate(P)
    mean, sd = READING_RATE_SYLL_S
    low, high = mean - READING_RATE_SD * sd, mean + READING_RATE_SD * sd
    if np.isfinite(rate) and not low <= rate <= high:
        side = "faster" if rate > high else "slower"
        out.append({"dimension": "D1", "label": f"Overall articulation rate {side} than typical read speech",
                    "words": None, "p": None, "b": None, "baseline": round(mean, 2), "participant": round(rate, 2),
                    "delta": round(rate - mean, 2), "unit": "syllables/s", "context": "whole passage", "span_kind": None,
                    "text": (f"Your articulation rate is {rate:.2f} syllables per second of speech (pauses removed); read sentences "
                             f"average {mean:.2f} (SD {sd:.2f}) across speakers (Jacewicz et al. 2009). Published norms differ "
                             f"with the method, so this is context only and costs no points.")})
    for i in long_pauses(P):
        span = P.sil_span[i]
        start, end = (float(span[0]), float(span[1])) if np.all(np.isfinite(span)) else (float(P.al.end[i]), float(P.al.start[i + 1]))
        out.append({"dimension": "D2", "label": "Pause longer than 1 s", "words": [i, i + 1], "p": [round(start, 3), round(end, 3)],
                    "b": None, "baseline": LONG_PAUSE_S, "participant": round(float(P.sil_raw[i]), 3),
                    "delta": round(float(P.sil_raw[i]) - LONG_PAUSE_S, 3), "unit": "s", "span_kind": "boundary",
                    "context": f"after '{P.tr.disp[i]}'",
                    "text": (f"A {float(P.sil_raw[i]):.2f} s pause after '{P.tr.disp[i]}'. In read speech, pauses over 1 s are rare "
                             f"(Campione & Veronis 2002); this is context only and costs no points.")})
    emphasis = det["text_model"].get("emphasis")
    if emphasis:
        for s in emphasis_contrast(P):
            flat = np.isfinite(s["contrast"]) and s["contrast"] < emphasis["flat_below"]
            uniform = np.isfinite(s["prominent_share"]) and s["prominent_share"] > emphasis["uniform_above"]
            if not (flat or uniform):
                continue
            w0, w1 = s["words"]
            out.append({"dimension": "D4", "label": "Flat emphasis pattern" if flat else "Uniform emphasis pattern",
                        "words": [w0, w1], "p": [round(float(P.al.start[w0]), 3), round(float(P.al.end[w1]), 3)], "b": None,
                        "baseline": emphasis["flat_below"] if flat else emphasis["uniform_above"],
                        "participant": round(s["contrast"] if flat else s["prominent_share"], 3), "delta": None,
                        "unit": "p-units" if flat else "share", "span_kind": "word", "context": f"sentence {s['sentence'] + 1}",
                        "text": ("Content words stand out little from the small words in this sentence." if flat else
                                 "Almost every word in this sentence is stressed.") + " This is context only and costs no points."})
    for j, item in enumerate(out):
        item.update(status="listed", brief_word=C.DIM_BRIEF[item["dimension"]], flag_thresholds=None, pattern=None, evidence=[],
                    candidate=False, id=f"x{j + 1}")
    return out


DIM_NOTE_ABSENT = "not measured in this mode: it needs a second reading of the same text (its stress, word times or endings)"


# ============================================================================================ CLI
def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m cvoice.selfref", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("calibrate", "evaluate"):
        p = sub.add_parser(name)
        p.add_argument("--dataset", type=Path, required=True)
        p.add_argument("--cache", type=Path)
        p.add_argument("--workers", type=int)
        p.add_argument("--detector", type=Path, default=DEFAULT_DETECTOR)
    sub.choices["calibrate"].add_argument("--text-model", choices=TEXT_MODELS, default="phones")
    sub.choices["calibrate"].add_argument("--reader-sources", default="", help="R2 fit-phase sources as extra clean nulls, e.g. gettysburg,poetry")
    sub.choices["calibrate"].add_argument("--reader-roles", default="budget", help=f"comma list among {READER_ROLES}")
    sub.choices["evaluate"].add_argument("--splits", default="train,val")
    args = parser.parse_args(argv)
    if args.command == "calibrate":
        det = calibrate(args.dataset, args.cache, args.workers, args.detector, args.text_model,
                        reader_sources=tuple(x for x in args.reader_sources.split(",") if x), reader_roles=tuple(args.reader_roles.split(",")))
        print(f"wrote {args.detector} (selfref {det['selfref_sha256'][:12]})")
        return
    result = evaluate(load_detector(args.detector), args.dataset, args.cache, args.workers, tuple(args.splits.split(",")))
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
