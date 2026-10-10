"""Normal word timing of read speech, learned from people who read aloud (LibriTTS, CC BY 4.0). The mode that grades a
reading without a reference reading uses it in the place of a reference reading. A text-to-speech voice is never a source.

    python scripts/fetch_norms_corpus.py --dest build/work/norms/corpus
    python -m cvoice.norms measure --corpus build/work/norms/corpus/LibriTTS/dev-clean --out build/work/norms/rows_dev.pkl
    python -m cvoice.norms fit --rows build/work/norms/rows_dev.pkl build/work/norms/rows_test.pkl --out models/duration_norms.json
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import config as C
from .align import _cmudict, count_syllables, normalize_word

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATH = ROOT / "models" / "duration_norms.json"
SCHEMA = 1

# ARPAbet phone classes of the CMU dictionary; a vowel carries its lexical stress digit.
PHONE_CLASSES = {
    "stop": ("P", "B", "T", "D", "K", "G"),
    "affricate": ("CH", "JH"),
    "fricative": ("F", "V", "TH", "DH", "S", "Z", "SH", "ZH", "HH"),
    "nasal": ("M", "N", "NG"),
    "liquid": ("L", "R"),
    "glide": ("W", "Y"),
}
VOWEL_CLASSES = {"1": "vowel_primary", "2": "vowel_secondary", "0": "vowel_unstressed"}
CLASS_NAMES = tuple(VOWEL_CLASSES.values()) + tuple(PHONE_CLASSES)
_CONSONANT_CLASS = {ph: name for name, phones in PHONE_CLASSES.items() for ph in phones}

# Letter fallback for a word outside the CMU dictionary: digraphs first, then single consonant letters.
_LETTER_DIGRAPHS = (("TH", "fricative"), ("SH", "fricative"), ("PH", "fricative"), ("CH", "affricate"), ("NG", "nasal"),
                    ("CK", "stop"), ("QU", "stop"))
_LETTER_CLASS = {**dict.fromkeys("BDGKPTCQX", "stop"), **dict.fromkeys("FVSZH", "fricative"), "J": "affricate",
                 **dict.fromkeys("MN", "nasal"), **dict.fromkeys("LR", "liquid"), "W": "glide"}

BOUNDARY_END, BOUNDARY_COMMA, BOUNDARY_TIGHT, BOUNDARY_NONE = "end", "comma", "tight", "none"
PAUSE_CLASSES = (BOUNDARY_END, BOUNDARY_COMMA, BOUNDARY_TIGHT, BOUNDARY_NONE)
# A word that binds to the next word: determiners, prepositions and auxiliaries. Words with a frequent second role that ends
# a phrase (THAT, HER, AS, BEFORE, AFTER) are left out. No parser: a closed list only.
TIGHT_WORDS = ("A", "AN", "THE", "THIS", "THESE", "THOSE", "MY", "YOUR", "HIS", "ITS", "OUR", "THEIR", "EVERY", "EACH",
               "OF", "TO", "IN", "ON", "AT", "BY", "FOR", "FROM", "WITH", "INTO", "ONTO", "UPON", "ABOUT", "THROUGH",
               "IS", "AM", "ARE", "WAS", "WERE", "BE", "BEEN", "HAVE", "HAS", "HAD", "DO", "DOES", "DID", "CAN", "COULD",
               "WILL", "WOULD", "SHALL", "SHOULD", "MAY", "MIGHT", "MUST")


# ============================================================================================ text features
def phone_counts(norm: str) -> tuple[np.ndarray, bool]:
    """(counts per CLASS_NAMES entry, in_dictionary) of one word in vocabulary form: the first CMU dictionary
    pronunciation, else the letter estimate."""
    prons = _cmudict().get(norm.lower())
    if not prons:
        return letter_counts(norm), False
    counts = np.zeros(len(CLASS_NAMES))
    for ph in prons[0]:
        counts[CLASS_NAMES.index(VOWEL_CLASSES[ph[-1]] if ph[-1].isdigit() else _CONSONANT_CLASS[ph])] += 1
    return counts, True


def letter_counts(norm: str) -> np.ndarray:
    """Phone counts estimated from spelling: vowels from the orthographic syllable count (the first one primary-stressed),
    consonants from the consonant letters and digraphs."""
    counts = np.zeros(len(CLASS_NAMES))
    vowels, _ = count_syllables(norm)
    counts[CLASS_NAMES.index("vowel_primary")] = 1
    counts[CLASS_NAMES.index("vowel_unstressed")] = vowels - 1
    letters = re.sub(r"(.)\1", r"\1", re.sub(r"[^A-Z]", "", norm.upper()))  # a double letter is one phone
    if letters.startswith("Y"):  # elsewhere Y is a vowel letter, counted by the syllable rule
        counts[CLASS_NAMES.index("glide")] += 1
    for digraph, name in _LETTER_DIGRAPHS:
        counts[CLASS_NAMES.index(name)] += letters.count(digraph)
        letters = letters.replace(digraph, "")
    for ch in letters:
        if ch in _LETTER_CLASS:
            counts[CLASS_NAMES.index(_LETTER_CLASS[ch])] += 1
    return counts


def sentence_ends(punct: str, word: str) -> bool:
    """True when the mark after `word` ends a sentence, with the rules of align.parse_transcript: '.', '!' or '?', but
    not an ellipsis and not the full stop of an abbreviation."""
    marks = punct.replace("...", "")
    if not any(ch in marks for ch in ".!?"):
        return False
    return not (marks == "." and word.lower() in C.ABBREVIATIONS)


def boundary_classes(words: list[str], punct_after: list[str], tight_words=TIGHT_WORDS) -> list[str]:
    """Class of the boundary after each word in vocabulary form (len(words) entries; the last word counts as a sentence
    end)."""
    out = []
    for i, (word, punct) in enumerate(zip(words, punct_after)):
        mark = "" if (punct == "." and word.lower() in C.ABBREVIATIONS) else punct
        if i == len(words) - 1 or sentence_ends(mark, word):
            out.append(BOUNDARY_END)
        elif mark:
            out.append(BOUNDARY_COMMA)
        elif word in tight_words:
            out.append(BOUNDARY_TIGHT)
        else:
            out.append(BOUNDARY_NONE)
    return out


# ============================================================================================ corpus measurement
def libritts_utterances(root: Path) -> list[dict]:
    """Utterances of one LibriTTS subset folder: id, speaker, chapter, wav path, normalised text, duration (s)."""
    import soundfile as sf
    out = []
    for wav in sorted(Path(root).glob("*/*/*.wav")):
        text_path = wav.with_suffix(".normalized.txt")
        if not text_path.exists():
            continue
        speaker, chapter = wav.stem.split("_")[:2]
        out.append({"id": wav.stem, "speaker": speaker, "chapter": chapter, "wav": str(wav),
                    "text": text_path.read_text(encoding="utf-8").strip(), "seconds": sf.info(str(wav)).duration})
    return out


BLOCK_S = 60.0  # s, length of one corpus reading: consecutive utterances of one chapter, near the length of a product reading


def reading_blocks(utterances: list[dict], block_s: float = BLOCK_S) -> list[list[dict]]:
    """Consecutive utterances of each chapter in id order, cut when a block reaches block_s seconds."""
    blocks: list[list[dict]] = []
    current: list[dict] = []
    for utt in sorted(utterances, key=lambda u: u["id"]):
        if current and (current[0]["chapter"] != utt["chapter"] or current[0]["speaker"] != utt["speaker"]
                        or sum(u["seconds"] for u in current) >= block_s):
            blocks.append(current)
            current = []
        current.append(utt)
    if current:
        blocks.append(current)
    return blocks


def measure_block(block: list[dict], cache_dir: str | None) -> dict:
    """Product timing of one corpus reading: canonical audio, the product transcript parser, forced alignment, acoustic
    pauses. Runs in a pool worker (its aligner) or in-process. Returns compact per-word arrays and a status."""
    import soundfile as sf

    from .align import TranscriptError, TranscriptMismatch, acoustic_pauses, parse_transcript
    from .audio import canonical
    from .features import frame_level_db, pitch_track
    from .pipeline import align_wav
    from .pool import worker_aligner

    head = {"block": block[0]["id"], "speaker": block[0]["speaker"], "chapter": block[0]["chapter"]}
    # An utterance without speakable words (a bracketed caption such as "[Illustration: ROLLS.]") leaves the block with
    # its audio: no window or pause crosses an utterance cut, so the rest of the block stays usable.
    parts, kept, dropped = [], [], []
    for u in block:
        try:
            parts.append(parse_transcript(u["text"], strict=False))
            kept.append(u)
        except TranscriptError:
            dropped.append(u["id"])
    head = {**head, "utterances": [u["id"] for u in kept], "utterances_without_words": dropped}
    if not kept:
        return {**head, "status": "transcript: no utterance has speakable words"}
    block = kept
    tr = parse_transcript(" ".join(u["text"] for u in block), strict=False)
    sizes = [len(p) for p in parts]
    if sum(sizes) != len(tr):
        return {**head, "status": "word count of the joined transcript differs from its parts"}
    pieces = []
    for u in block:
        x, sr = sf.read(u["wav"], dtype="float64", always_2d=True)
        pieces.append(canonical(x.mean(axis=1), sr))
    wav = np.concatenate(pieces)
    try:
        wav, al = align_wav(wav, tr, worker_aligner(), Path(cache_dir) if cache_dir else None)
    except TranscriptMismatch as e:
        return {**head, "status": f"alignment: {e}"}
    level = frame_level_db(wav)
    f0, _ = pitch_track(wav)
    sil, _, sil_raw = acoustic_pauses(al, level, f0 > 0)
    utterance = np.repeat(np.arange(len(block)), sizes)
    utterance_compat = np.array([al.compat[utterance == k].mean() for k in range(len(block))])
    return {**head, "status": "ok", "norm": tr.norm, "punct": tr.punct, "sentence": tr.sentence, "utterance": utterance,
            "start": al.start, "end": al.end, "compat": al.compat, "mean_compat": al.mean_compat,
            "utterance_compat": utterance_compat, "sil": sil, "sil_raw": sil_raw, "seconds": len(wav) / C.SR}


def measure_corpus(root: Path, cache_dir: Path | None, workers: int) -> list[dict]:
    from .pipeline import map_calls
    from .pool import PreparePool
    blocks = reading_blocks(libritts_utterances(root))
    args = [(b, str(cache_dir) if cache_dir else None) for b in blocks]
    if workers <= 1:
        return map_calls(measure_block, args)
    with PreparePool(workers=workers, devices=["cpu"], cache_dir=cache_dir) as pool:
        return map_calls(measure_block, args, pool)


# ============================================================================================ corpus tables
def kept_utterances(row: dict) -> np.ndarray:
    """Per word: True when its utterance passes the product's trust-boundary check (mean word compatibility at least
    MEAN_COMPAT_MIN), applied to each utterance and to the whole block."""
    if row["status"] != "ok" or row["mean_compat"] < C.MEAN_COMPAT_MIN:
        return np.zeros(len(row.get("norm", ())), bool)
    return row["utterance_compat"][row["utterance"]] >= C.MEAN_COMPAT_MIN


def speech_shares(start: np.ndarray, end: np.ndarray, sil: np.ndarray) -> np.ndarray:
    """Share of each word in the speech time of a stretch (features.speech_time: the aligned span less the acoustic
    pauses): onset to the next onset less the pause between them; the last word: its aligned span. The shares of the
    words of a window add up to its speech time."""
    out = np.asarray(end, float) - np.asarray(start, float)
    out[:-1] = np.diff(start) - np.asarray(sil, float)
    return out


def row_features(row: dict) -> dict:
    """Text features of every word of one corpus reading. The boundary after the last word of an utterance is a sentence
    end; its speech share is NaN (the next onset lies in another utterance)."""
    words, utt = list(row["norm"]), np.asarray(row["utterance"])
    last = np.r_[utt[1:] != utt[:-1], True]
    rows = [phone_counts(w) for w in words]
    speech = speech_shares(row["start"], row["end"], row["sil"])
    return {"counts": np.array([c for c, _ in rows]).reshape(len(words), len(CLASS_NAMES)),
            "in_dict": np.array([d for _, d in rows], bool),
            "function": np.array([w in C.FUNCTION_WORDS for w in words], bool),
            "boundary": np.where(last, BOUNDARY_END, boundary_classes(words, list(row["punct"]))),
            "word": np.asarray(row["end"]) - np.asarray(row["start"]),
            "speech": np.where(last, np.nan, speech)}


def word_table(rows: list[dict]) -> dict:
    """One entry per kept corpus word: text features, the speech share and the aligned span (s), reading (block index
    in `rows`) and speaker."""
    parts = []
    for b, row in enumerate(rows):
        keep = kept_utterances(row)
        if not keep.any():
            continue
        f = {k: v[keep] for k, v in row_features(row).items()}
        f["block"] = np.full(int(keep.sum()), b)
        f["speaker"] = np.full(int(keep.sum()), row["speaker"], dtype=object)
        parts.append(f)
    return {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}


def pause_table(rows: list[dict]) -> dict:
    """One entry per kept boundary inside an utterance (a boundary between two utterances is a cut of the corpus, not a
    pause of the reader): class, raw silent run (s), speaker."""
    cls, raw, speaker = [], [], []
    for row in rows:
        keep = kept_utterances(row)
        if not keep.any():
            continue
        utt = row["utterance"]
        bounds = boundary_classes(list(row["norm"]), list(row["punct"]))
        for i in range(len(utt) - 1):
            if keep[i] and utt[i] == utt[i + 1]:
                cls.append(bounds[i])
                raw.append(row["sil_raw"][i])
                speaker.append(row["speaker"])
    return {"cls": np.array(cls), "raw": np.array(raw), "speaker": np.array(speaker)}


# ============================================================================================ duration model fit
def design(counts: np.ndarray, function: np.ndarray, boundary: np.ndarray, groups: dict, factors: tuple) -> tuple[np.ndarray, np.ndarray]:
    """(phone counts per model group, factor columns). groups: {group name: [CLASS_NAMES entries]}; factors: names out of
    FACTORS."""
    merged = np.column_stack([counts[:, [CLASS_NAMES.index(c) for c in members]].sum(1) for members in groups.values()])
    vowels = counts[:, [CLASS_NAMES.index(v) for v in VOWEL_CLASSES.values()]].sum(1)
    cols = {"function_word": function.astype(float),
            "comma_after": (boundary == BOUNDARY_COMMA).astype(float),
            "end_after": (boundary == BOUNDARY_END).astype(float),
            "end_after_per_syllable": (boundary == BOUNDARY_END) / np.maximum(vowels, 1),
            "comma_after_per_syllable": (boundary == BOUNDARY_COMMA) / np.maximum(vowels, 1)}
    return merged, np.column_stack([cols[f] for f in factors]) if factors else np.zeros((len(counts), 0))


def _centre(values: np.ndarray, block: np.ndarray) -> np.ndarray:
    """Values less the mean of their block (the reader's own rate at that reading); 2-D: per column."""
    _, inv = np.unique(block, return_inverse=True)
    n = np.bincount(inv).astype(float)
    if values.ndim == 1:
        return values - (np.bincount(inv, values) / n)[inv]
    return values - np.column_stack([np.bincount(inv, values[:, k]) / n for k in range(values.shape[1])])[inv]


def predict(theta: np.ndarray, beta: np.ndarray, merged: np.ndarray, factors: np.ndarray) -> np.ndarray:
    """ln(sum over groups of exp(theta) * count) + factors @ beta: Klatt-style multiplicative factors on a sum of phone
    durations (one duration per phone group)."""
    base = merged @ np.exp(theta)
    return np.log(np.maximum(base, 1e-9)) + factors @ beta


def fit_duration(table: dict, groups: dict, factors: tuple, target: str = "speech", mask: np.ndarray | None = None) -> dict:
    """Least squares on ln word duration with one free constant per reading (block): the reader's rate does not enter the
    fit. The last group is the unit (theta 0): only duration ratios are identified."""
    from scipy.optimize import least_squares
    m = np.isfinite(table[target]) & (table[target] > 0) & (True if mask is None else mask)
    merged, fac = design(table["counts"][m], table["function"][m], table["boundary"][m], groups, factors)
    y, block = np.log(table[target][m]), table["block"][m]
    k = len(groups) - 1

    def residual(p):
        theta = np.r_[p[:k], 0.0]
        return _centre(y - predict(theta, p[k:], merged, fac), block)

    def jac(p):
        theta = np.r_[p[:k], 0.0]
        share = merged * np.exp(theta) / (merged @ np.exp(theta))[:, None]
        return -_centre(np.column_stack([share[:, :k], fac]), block)

    sol = least_squares(residual, np.zeros(k + fac.shape[1]), jac=jac, method="lm")
    theta, beta = np.r_[sol.x[:k], 0.0], sol.x[k:]
    centre = float(np.mean(predict(theta, beta, merged, fac)))
    return {"target": target, "objective": "word", "groups": {g: list(v) for g, v in groups.items()}, "factors": list(factors),
            "theta": theta.tolist(), "beta": beta.tolist(), "centre": centre}


def window_table(rows: list[dict]) -> dict:
    """All words of the readings with at least one usable window, and the windows (window_measures rules) as a sparse
    word-membership matrix, with the measured window times."""
    from scipy.sparse import csr_matrix

    from .features import windows
    feats, block, data_rows, data_cols, times = [], [], [], [], {m: [] for m in MEASURES}
    offset = 0
    for b, row in enumerate(rows):
        keep = kept_utterances(row)
        if not keep.any():
            continue
        utt, f = np.asarray(row["utterance"]), row_features(row)
        span = np.asarray(row["end"]) - np.asarray(row["start"])
        used = False
        for w in windows(_SentenceOnly(tuple(row["sentence"]))):
            if w is None or utt[w[0]] != utt[w[1]] or not keep[w[0]:w[1] + 1].all():
                continue
            lo, hi = w
            k = len(block)
            data_rows += [k] * (hi - lo + 1)
            data_cols += list(range(offset + lo, offset + hi + 1))
            times["speech"].append(max(row["end"][hi] - row["start"][lo] - np.sum(row["sil"][lo:hi]), 1e-3))
            times["word"].append(span[lo:hi + 1].sum())
            block.append(b)
            used = True
        if used:
            feats.append(f)
            offset += len(f["word"])
    member = csr_matrix((np.ones(len(data_rows)), (data_rows, data_cols)), shape=(len(block), offset))
    words = {k: np.concatenate([f[k] for f in feats]) for k in ("counts", "function", "boundary")}
    return {"member": member, "block": np.array(block), **{f"time_{m}": np.array(v) for m, v in times.items()}, **words}


def fit_window_duration(rows: list[dict], groups: dict, factors: tuple, target: str = "speech") -> dict:
    """The duration model fitted to the five-word window times that the detector thresholds: least squares on
    ln(window time) - ln(sum of the expected word times), one free constant per reading."""
    from scipy.optimize import least_squares
    wt = window_table(rows)
    merged, fac = design(wt["counts"], wt["function"], wt["boundary"], groups, factors)
    y, block, member = np.log(wt[f"time_{target}"]), wt["block"], wt["member"]
    k = len(groups) - 1

    def parts(p):
        theta = np.r_[p[:k], 0.0]
        f = predict(theta, p[k:], merged, fac)
        return theta, np.exp(f)

    def residual(p):
        _, e = parts(p)
        return _centre(y - np.log(member @ e), block)

    def jac(p):
        theta, e = parts(p)
        share = merged * np.exp(theta) / (merged @ np.exp(theta))[:, None]
        d_word = np.column_stack([share[:, :k], fac]) * e[:, None]
        return -_centre((member @ d_word) / (member @ e)[:, None], block)

    sol = least_squares(residual, np.zeros(k + fac.shape[1]), jac=jac, method="lm")
    theta, beta = np.r_[sol.x[:k], 0.0], sol.x[k:]
    centre = float(np.mean(predict(theta, beta, merged, fac)))
    return {"target": target, "objective": "window", "groups": {g: list(v) for g, v in groups.items()},
            "factors": list(factors), "theta": theta.tolist(), "beta": beta.tolist(), "centre": centre}


def apply_duration(model: dict, counts: np.ndarray, function: np.ndarray, boundary: np.ndarray) -> np.ndarray:
    merged, fac = design(counts, function, boundary, model["groups"], tuple(model["factors"]))
    return predict(np.asarray(model["theta"]), np.asarray(model["beta"]), merged, fac) - model["centre"]


def r_squared(y: np.ndarray, pred: np.ndarray, block: np.ndarray) -> float:
    """Share of the within-reading variance of y that pred explains (each reading's own mean removed from both)."""
    resid = _centre(y - pred, block)
    total = _centre(y, block)
    return float(1.0 - np.sum(resid ** 2) / np.sum(total ** 2))


def robust_spread(values: np.ndarray) -> float:
    v = values[np.isfinite(values)]
    return float(C.MAD_SCALE * np.median(np.abs(v - np.median(v)))) if v.size else float("nan")


def window_measures(row: dict, expected_speech: np.ndarray, expected_word: np.ndarray) -> dict:
    """The five-word window measures of the no-reference mode for one reading, each against its expected window time and
    centred on the reading's median: D1 = ln(speech time / sum of expected speech shares), D9 = ln(word time / sum of
    expected word spans). expected_*: per-word expected time (any common scale). A window across an utterance cut of the
    corpus or with a dropped utterance is NaN."""
    from .features import windows
    keep, utt = kept_utterances(row), np.asarray(row["utterance"])
    sentence = tuple(row["sentence"])
    span = np.asarray(row["end"]) - np.asarray(row["start"])
    out = {"D1": [], "D9": []}
    for w in windows(_SentenceOnly(sentence)):
        if w is None or utt[w[0]] != utt[w[1]] or not keep[w[0]:w[1] + 1].all():
            out["D1"].append(np.nan)
            out["D9"].append(np.nan)
            continue
        lo, hi = w
        speech = max(row["end"][hi] - row["start"][lo] - np.sum(row["sil"][lo:hi]), 1e-3)
        out["D1"].append(np.log(speech / expected_speech[lo:hi + 1].sum()))
        out["D9"].append(np.log(span[lo:hi + 1].sum() / expected_word[lo:hi + 1].sum()))
    result = {}
    for k, v in out.items():
        x = np.array(v)
        result[k] = x - np.nanmedian(x) if np.isfinite(x).any() else x
    return result


@dataclass(frozen=True)
class _SentenceOnly:
    """The part of a Transcript that features.windows reads."""
    sentence: tuple


# ============================================================================================ pause model
PAUSE_STEP_S = C.HOP_S  # the raw pause is a whole number of 10 ms frames (align.acoustic_pauses)


def fit_pauses(pauses: dict) -> dict:
    """Empirical distribution of the raw pause (s) per boundary class: P(pause <= k * step) for k = 0 .. K, with K the
    first frame count at or above the longest corpus pause."""
    frames = np.round(pauses["raw"] / PAUSE_STEP_S).astype(int)
    top = int(frames.max())
    cdf, count = {}, {}
    for cls in PAUSE_CLASSES:
        v = frames[pauses["cls"] == cls]
        count[cls] = int(v.size)
        cdf[cls] = [round(float(x), 6) for x in np.searchsorted(np.sort(v), np.arange(top + 1), side="right") / max(v.size, 1)]
    return {"step_s": PAUSE_STEP_S, "count": count, "cdf": cdf}


# ============================================================================================ API
MEASURES = ("speech", "word")  # speech: share of the speech time (D1 window time); word: aligned word span (D9)


def parameters_sha256(parameters: dict) -> str:
    return hashlib.sha256(json.dumps(parameters, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class NormsError(ValueError):
    """The norms file is missing, malformed or its parameters do not match their recorded SHA-256."""


@dataclass(frozen=True)
class Norms:
    """Normal word timing of read speech (models/duration_norms.json)."""
    parameters: dict
    provenance: dict
    report: dict

    def word_features(self, words: list[str], punct_after: list[str]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """(phone counts per CLASS_NAMES entry, in_dictionary, function word, boundary class after the word)."""
        if len(words) != len(punct_after):
            raise ValueError(f"{len(words)} words but {len(punct_after)} punctuation entries")
        norm = [normalize_word(w) for w in words]
        rows = [phone_counts(w) for w in norm]
        counts = np.array([c for c, _ in rows]).reshape(len(norm), len(CLASS_NAMES))
        in_dict = np.array([d for _, d in rows], bool)
        function = np.array([w in self.parameters["function_words"] for w in norm], bool)
        boundary = np.array(self._boundaries(norm, punct_after))
        return counts, in_dict, function, boundary

    def _boundaries(self, norm: list[str], punct_after: list[str]) -> list[str]:
        return boundary_classes(norm, list(punct_after), frozenset(self.parameters["tight_words"]))

    def in_dictionary(self, words: list[str]) -> np.ndarray:
        """False where the phone counts are the letter-based estimate (the word is not in the CMU dictionary)."""
        return np.array([phone_counts(normalize_word(w))[1] for w in words], bool)

    def expected_word_log_duration(self, words: list[str], punct_after: list[str], measure: str = "speech") -> np.ndarray:
        """Expected ln duration of each word relative to the reader's own rate: mean zero over the corpus words, so only
        differences between words carry meaning. measure 'speech': the word's share of the speech time (onset to the next
        onset less the acoustic pause; the D1 window time is the sum of these shares); 'word': the aligned word span
        (the D9 window time is the sum of these spans). The last word counts as followed by a sentence end."""
        if measure not in MEASURES:
            raise ValueError(f"measure must be one of {MEASURES}, got {measure!r}")
        if not words:
            return np.zeros(0)
        counts, _, function, boundary = self.word_features(words, punct_after)
        return apply_duration(self.parameters["duration"][measure], counts, function, boundary)

    def pause_class(self, words: list[str], punct_after: list[str]) -> list[str]:
        """Class of each of the len(words) - 1 boundaries between consecutive words: 'end' (a sentence ends), 'comma'
        (other punctuation: , ; : -- ...), 'tight' (no mark, and the first word is a determiner, preposition or auxiliary
        of the closed list), 'none' (no mark)."""
        if len(words) != len(punct_after):
            raise ValueError(f"{len(words)} words but {len(punct_after)} punctuation entries")
        return self._boundaries([normalize_word(w) for w in words], list(punct_after))[:-1]

    def pause_quantile(self, cls: str, seconds: float) -> float:
        """Share of the corpus boundaries of class `cls` whose raw pause (align.acoustic_pauses) is at most `seconds`."""
        table = self.parameters["pause"]
        if cls not in table["cdf"]:
            raise ValueError(f"pause class must be one of {tuple(table['cdf'])}, got {cls!r}")
        if not np.isfinite(seconds) or seconds < 0:
            raise ValueError(f"pause length must be a finite number of seconds >= 0, got {seconds}")
        cdf = table["cdf"][cls]
        k = int(np.floor(seconds / table["step_s"] + 1e-6))
        return float(cdf[min(k, len(cdf) - 1)])


def build_document(parameters: dict, provenance: dict, report: dict) -> dict:
    return {"schema": SCHEMA, "name": "duration_norms", "parameters": parameters,
            "parameters_sha256": parameters_sha256(parameters), "provenance": provenance, "report": report}


def load(path: Path | str | None = None) -> Norms:
    """Read the norms file (default models/duration_norms.json) and verify the SHA-256 of its parameters."""
    path = Path(path) if path is not None else DEFAULT_PATH
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise NormsError(f"cannot read the norms file {path}: {e}") from e
    if doc.get("schema") != SCHEMA or "parameters" not in doc:
        raise NormsError(f"{path}: not a schema {SCHEMA} norms file")
    digest = parameters_sha256(doc["parameters"])
    if digest != doc.get("parameters_sha256"):
        raise NormsError(f"{path}: parameters SHA-256 {digest} != recorded {doc.get('parameters_sha256')}")
    return Norms(doc["parameters"], doc.get("provenance", {}), doc.get("report", {}))


# ============================================================================================ build and report
# The model form with the smallest held-out window spread of D1 and D9 in both directions (fit dev-clean, score test-clean,
# and the reverse; build/work/norms/STATUS.md): one duration per phone class, function word, comma-type mark after and
# sentence end after as multiplicative factors, fitted to the five-word window times that the detector thresholds.
MODEL_GROUPS = {name: (name,) for name in CLASS_NAMES}
MODEL_FACTORS = ("function_word", "comma_after", "end_after")
OBJECTIVES = ("word", "window")
MODEL_OBJECTIVE = "window"


def fit_model(rows: list[dict], measure: str, objective: str = MODEL_OBJECTIVE, groups: dict = MODEL_GROUPS,
              factors: tuple = MODEL_FACTORS) -> dict:
    if objective not in OBJECTIVES:
        raise ValueError(f"objective must be one of {OBJECTIVES}, got {objective!r}")
    if objective == "window":
        return fit_window_duration(rows, groups, factors, target=measure)
    return fit_duration(word_table(rows), groups, factors, target=measure)


def phones_slope(table: dict, measure: str) -> float:
    """Least-squares slope of ln duration on ln phone count with one constant per reading (the phones-only baseline)."""
    ok = np.isfinite(table[measure]) & (table[measure] > 0)
    x = _centre(np.log(table["counts"][ok].sum(1)), table["block"][ok])
    y = _centre(np.log(table[measure][ok]), table["block"][ok])
    return float(x @ y / (x @ x))


def evaluate_held_out(fit_rows: list[dict], eval_rows: list[dict], groups: dict = MODEL_GROUPS,
                      factors: tuple = MODEL_FACTORS, objective: str = MODEL_OBJECTIVE) -> dict:
    """Fit on the readers of fit_rows, score on the readers of eval_rows: within-reading R^2 of ln duration per measure
    against the phones-only baselines, and the robust spread of the D1 / D9 window measures."""
    ft, et = word_table(fit_rows), word_table(eval_rows)
    shared = set(ft["speaker"]) & set(et["speaker"])
    if shared:
        raise ValueError(f"speakers in both the fit and the evaluation readers: {sorted(shared)[:5]}")
    out = {"fit": table_counts(ft), "eval": table_counts(et), "objective": objective}
    models = {m: fit_model(fit_rows, m, objective, groups, factors) for m in MEASURES}
    for m in MEASURES:
        ok = np.isfinite(et[m]) & (et[m] > 0)
        y, block, phones = np.log(et[m][ok]), et["block"][ok], np.log(et["counts"][ok].sum(1))
        slope = phones_slope(ft, m)
        pred = apply_duration(models[m], et["counts"][ok], et["function"][ok], et["boundary"][ok])
        out[m] = {"words": int(ok.sum()), "r2_phones_proportional": round(r_squared(y, phones, block), 4),
                  "phones_slope": round(slope, 4), "r2_phones_fitted": round(r_squared(y, slope * phones, block), 4),
                  "r2_norms": round(r_squared(y, pred, block), 4)}
    windows = {"D1": {"raw": [], "phones": [], "norms": []}, "D9": {"raw": [], "phones": [], "norms": []}}
    for row in eval_rows:
        if not kept_utterances(row).any():
            continue
        f = row_features(row)
        expected = {"raw": (np.ones(len(f["word"])),) * 2, "phones": (f["counts"].sum(1),) * 2,
                    "norms": tuple(np.exp(apply_duration(models[m], f["counts"], f["function"], f["boundary"])) for m in MEASURES)}
        for name, (speech, word) in expected.items():
            x = window_measures(row, speech, word)
            for dim in windows:
                windows[dim][name].append(x[dim])
    out["window_spread"] = {dim: {name: round(robust_spread(np.concatenate(v)), 4) for name, v in d.items()}
                            for dim, d in windows.items()}
    out["windows"] = int(np.isfinite(np.concatenate(windows["D1"]["raw"])).sum())
    return out


def table_counts(table: dict) -> dict:
    return {"speakers": len(set(table["speaker"])), "readings": len(set(table["block"])), "words": len(table["word"]),
            "words_not_in_dictionary": int((~table["in_dict"]).sum())}


def pause_summary(pauses: dict) -> dict:
    out = {}
    for cls in PAUSE_CLASSES:
        v = pauses["raw"][pauses["cls"] == cls]
        out[cls] = {"boundaries": int(v.size), "share_at_least_pause_min": round(float((v >= C.PAUSE_MIN_S).mean()), 4),
                    "median_s": round(float(np.median(v)), 3), "q90_s": round(float(np.quantile(v, 0.9)), 3)} if v.size else {}
    return out


def archive_record(subset: str) -> dict:
    """URL and hashes of a corpus archive as pinned in scripts/fetch_norms_corpus.py."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("fetch_norms_corpus", ROOT / "scripts" / "fetch_norms_corpus.py")
    fetch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fetch)
    entry = fetch.ARCHIVES[subset]
    return {"subset": subset, "url": f"{fetch.MIRRORS[0]}/{entry['file']}", "sha256": entry["sha256"], "md5": entry["md5"],
            "bytes": entry["bytes"]}


def git_commit() -> str:
    import subprocess
    try:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, timeout=30,
                              check=False).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, capture_output=True,
                               text=True, timeout=30, check=False).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return "unknown"
    return head + ("+uncommitted" if dirty else "") if head else "unknown"


def build(subsets: dict[str, list[dict]]) -> dict:
    """The norms document from measured corpus readings {subset name: rows}: held-out reports (each subset against the
    others, so the readers never overlap), then the final fit on all readers."""
    import datetime
    report: dict = {"held_out": {}}
    names = list(subsets)
    for name in names:
        rest = [r for other in names if other != name for r in subsets[other]]
        if rest:
            report["held_out"][f"fit {'+'.join(n for n in names if n != name)} -> eval {name}"] = evaluate_held_out(rest, subsets[name])
    rows = [r for name in names for r in subsets[name]]
    table, pauses = word_table(rows), pause_table(rows)
    duration = {m: fit_model(rows, m) for m in MEASURES}
    for model in duration.values():
        for k in ("theta", "beta"):
            model[k] = [round(v, 6) for v in model[k]]
        model["centre"] = round(model["centre"], 6)
    parameters = {"duration": duration, "function_words": list(C.FUNCTION_WORDS), "tight_words": list(TIGHT_WORDS),
                  "pause": fit_pauses(pauses)}
    report["final_fit"] = {**table_counts(table), "pauses": pause_summary(pauses),
                           "factors": {m: {f: round(float(np.exp(b)), 4) for f, b in zip(MODEL_FACTORS, duration[m]["beta"])}
                                       for m in MEASURES},
                           "phone_duration_ratio": {m: {g: round(float(np.exp(t)), 4) for g, t in zip(MODEL_GROUPS, duration[m]["theta"])}
                                                    for m in MEASURES}}
    status = {}
    for r in rows:
        key = r["status"].split(":")[0]
        status[key] = status.get(key, 0) + 1
    utterances = [u for r in rows for u in r["utterances"]]
    without_words = [u for r in rows for u in r.get("utterances_without_words", ())]
    kept = sum(int((r["utterance_compat"] >= C.MEAN_COMPAT_MIN).sum()) for r in rows if r["status"] == "ok"
               and r["mean_compat"] >= C.MEAN_COMPAT_MIN)
    ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    provenance = {"corpus": "LibriTTS (Zen et al. 2019, arXiv:1904.02882), OpenSLR SLR60", "page": "https://www.openslr.org/60/",
                  "licence": "CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), as stated on the OpenSLR SLR60 page and in "
                             "LibriTTS/LICENSE.txt of the archives",
                  "archives": [archive_record(n) for n in names], "readings": len(rows), "reading_status": status,
                  "utterances": len(utterances), "utterances_without_words": len(without_words), "utterances_kept": kept,
                  "speakers": len(set(table["speaker"])),
                  "words": len(table["word"]), "boundaries": len(pauses["raw"]), "reading_block_s": BLOCK_S,
                  "aligner": f"{C.CHECKPOINT_NAME} sha256 {C.CHECKPOINT_SHA256[:16]}",
                  "fit_date": datetime.datetime.now(ist).strftime("%Y-%m-%d %H:%M IST"), "git_commit": git_commit(),
                  "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  "rebuild": "python scripts/fetch_norms_corpus.py --dest DIR; python -m cvoice.norms measure (each subset); "
                             "python -m cvoice.norms fit"}
    return build_document(parameters, provenance, report)


# ============================================================================================ CLI
def main(argv: list[str] | None = None) -> None:
    import argparse
    import pickle
    import time
    ap = argparse.ArgumentParser(prog="python -m cvoice.norms")
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("measure", help="align a LibriTTS subset folder with the product aligner")
    m.add_argument("--corpus", type=Path, required=True)
    m.add_argument("--out", type=Path, required=True)
    m.add_argument("--cache", type=Path, default=None)
    m.add_argument("--workers", type=int, default=1)
    f = sub.add_parser("fit", help="fit the norms on measured subsets and write the norms file")
    f.add_argument("--rows", type=Path, nargs="+", required=True, help="outputs of measure, one per subset")
    f.add_argument("--out", type=Path, default=DEFAULT_PATH)
    a = ap.parse_args(argv)
    if a.cmd == "measure":
        t0 = time.time()
        rows = measure_corpus(a.corpus, a.cache, a.workers)
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_bytes(pickle.dumps({"subset": a.corpus.name, "rows": rows}))
        ok = sum(r["status"] == "ok" for r in rows)
        print(f"{a.corpus}: {ok} of {len(rows)} readings aligned, {time.time() - t0:.0f} s")
    else:
        measured = [pickle.loads(p.read_bytes()) for p in a.rows]
        doc = build({m["subset"]: m["rows"] for m in measured})
        a.out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
        print(json.dumps(doc["report"], indent=1))


if __name__ == "__main__":
    main()
