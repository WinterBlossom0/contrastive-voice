"""Forced word alignment: transcript parsing, wav2vec2 emissions, numpy CTC Viterbi, word spans, compatibility,
acoustic pause rule, syllables.

Timing source = raw CTC spans (first-character spike .. last-character spike), 20 ms frames; energy snapping is not
used (it erased inserted pauses in research). All times are seconds from the start of the audio passed in.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np

from . import config as C

# wav2vec2-base-960h CTC vocabulary (blank = 0, word separator '|'); checked against the bundle at load time (K)
LABELS = ("-", "|", "E", "T", "A", "O", "N", "I", "H", "S", "R", "D", "L", "U", "M", "W", "C", "F", "G", "Y", "P", "B",
          "V", "K", "'", "X", "J", "Q", "Z")
VOCAB = {c: i for i, c in enumerate(LABELS)}
NEG = -1e30


class TranscriptError(ValueError):
    """The transcript cannot be turned into spoken words (trust boundary)."""


MISMATCH_WORDS, MISMATCH_SHORT, MISMATCH_PART = "words", "short", "part"


class TranscriptMismatch(ValueError):
    """The transcript does not match the audio. kind: MISMATCH_WORDS (mean word compatibility below the floor),
    MISMATCH_SHORT (the audio has fewer CTC frames than the transcript needs) or MISMATCH_PART (one stretch of the
    recording does not match its part of the transcript); needed_s: the shortest audio (s) that the transcript needs, for
    MISMATCH_SHORT; at_s, near: for MISMATCH_PART, the evidence-weighted centre (s) of that stretch and the transcript
    words at it; roles: the recordings that fail ("baseline", "participant", "reference k" for the k-th reading of a
    bank), which the pipeline sets."""

    def __init__(self, message: str, kind: str = MISMATCH_WORDS, needed_s: float | None = None, roles: tuple[str, ...] = (),
                 at_s: float | None = None, near: str | None = None):
        super().__init__(message)
        self.kind, self.needed_s, self.roles, self.at_s, self.near = kind, needed_s, roles, at_s, near


# ============================================================================================ text
_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "zero ten twenty thirty forty fifty sixty seventy eighty ninety".split()
_ORD = {"one": "first", "two": "second", "three": "third", "five": "fifth", "eight": "eighth", "nine": "ninth", "twelve": "twelfth"}


def cardinal(n: int) -> list[str]:
    """Spoken words of a non-negative integer below 10**12."""
    if n < 20:
        return [_ONES[n]]
    if n < 100:
        return [_TENS[n // 10]] + (_ONES[n % 10:n % 10 + 1] if n % 10 else [])
    for unit, name in ((10 ** 9, "billion"), (10 ** 6, "million"), (1000, "thousand"), (100, "hundred")):
        if n >= unit:
            rest = n % unit
            return cardinal(n // unit) + [name] + (cardinal(rest) if rest else [])
    raise TranscriptError(f"The transcript has a number too large to read aloud: {n}. Write it in words.")


def ordinal(words: list[str]) -> list[str]:
    last = words[-1]
    if last in _ORD:
        last = _ORD[last]
    elif last.endswith("y"):
        last = last[:-1] + "ieth"
    else:
        last += "th"
    return words[:-1] + [last]


def spell_number(tok: str) -> list[str]:
    """Spoken words for a numeric token such as 1989, 1,000, 34th, 3.5, $5, 5%. Years 1100-1999 and 2010-2099 are
    read as two pairs. Raises TranscriptError for digit tokens that cannot be spelled."""
    m = re.fullmatch(r"([$£€]?)(\d[\d,]*)(?:\.(\d+))?(st|nd|rd|th)?(%?)", tok)
    if not m:
        raise TranscriptError(f"The transcript has {tok!r}, which cannot be read aloud as written. Write it in words.")
    cur, whole, frac, suffix, pct = m.groups()
    digits = whole.replace(",", "")
    n = int(digits)
    if "," not in whole and len(digits) == 4 and not suffix and not frac and (1100 <= n <= 1999 or 2010 <= n <= 2099):
        hi, lo = divmod(n, 100)
        words = cardinal(hi) + (["hundred"] if lo == 0 else (["oh"] + cardinal(lo) if lo < 10 else cardinal(lo)))
    else:
        words = cardinal(n)
    if frac:
        words += ["point"] + [_ONES[int(d)] for d in frac]
    if suffix:
        words = ordinal(words)
    if pct:
        words.append("percent")
    if cur:
        words.append("dollars" if cur == "$" else "pounds" if cur == "£" else "euros")
    return words


def normalize_word(tok: str) -> str:
    """Upper-case letters and apostrophes only (the wav2vec2-base-960h vocabulary)."""
    tok = tok.replace("’", "'").replace("‘", "'")
    tok = unicodedata.normalize("NFKD", tok)
    tok = "".join(ch for ch in tok if not unicodedata.combining(ch))
    return re.sub(r"[^A-Z']", "", tok.upper()).strip("'")


@dataclass(frozen=True)
class Transcript:
    """Spoken words of a transcript. disp: display token (no trailing punctuation); norm: vocabulary form;
    sentence: sentence index per word; punct: punctuation straight after the word ('' or one of . , ; : ! ? ... --)."""
    disp: tuple[str, ...]
    norm: tuple[str, ...]
    sentence: tuple[int, ...]
    punct: tuple[str, ...]
    syll: tuple[int, ...]
    syll_heuristic: tuple[bool, ...]

    def __len__(self) -> int:
        return len(self.norm)

    def text(self, i0: int = 0, i1: int | None = None) -> str:
        """Display text of words i0..i1 (inclusive) with their punctuation."""
        i1 = len(self) - 1 if i1 is None else i1
        return " ".join(self.disp[i] + self.punct[i] for i in range(i0, i1 + 1))

    def slice(self, i0: int, i1: int) -> "Transcript":
        """Words i0..i1 (inclusive) as a transcript of their own (sentence indices rebased)."""
        s = slice(i0, i1 + 1)
        sent = self.sentence[s]
        return Transcript(self.disp[s], self.norm[s], tuple(v - sent[0] for v in sent), self.punct[s], self.syll[s],
                          self.syll_heuristic[s])

    def sentence_words(self, k: int) -> tuple[int, int]:
        """(first, last) word index of sentence k."""
        idx = [i for i, s in enumerate(self.sentence) if s == k]
        return idx[0], idx[-1]

    @property
    def n_sentences(self) -> int:
        return self.sentence[-1] + 1 if self.sentence else 0


_CLAUSE_SEP = re.compile(r"(--+|[—–―]|…)")
_EDGE = re.compile(r"^([^\w$£€]*)(.*?)([^\w%]*)$", re.S)


def _clean(text: str) -> str:
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"\[[^\]]*\]|\([^)]*\)", " ", text)  # stage directions: [applause], (Laughter.)
    text = re.sub(r"\s*(?:\.\s){2,}\.\s*|\s*\.{3,}\s*", "… ", text)  # ". . ." and "..." -> one ellipsis
    text = re.sub(r"\s+-\s+", " -- ", text)
    return text


@lru_cache(maxsize=1)
def _cmudict() -> dict:
    import cmudict
    return cmudict.dict()


def count_syllables(norm: str) -> tuple[int, bool]:
    """(syllables, heuristic): CMUdict first pronunciation (stress-marked vowels); orthographic fallback is flagged."""
    prons = _cmudict().get(norm.lower())
    if prons:
        return max(1, sum(ph[-1].isdigit() for ph in prons[0])), False
    w = norm.lower().replace("'", "")
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(1, n), True


def parse_transcript(text: str, strict: bool = True) -> Transcript:
    """Tokenise a transcript: words, numbers spelled out, sentence index and punctuation per word. Raises TranscriptError when
    nothing speakable remains or (strict, the default for uploads) a digit token cannot be spelled; with strict=False such
    tokens are dropped (scraped official pages hold times, decades and other page furniture)."""
    pieces: list[list] = []  # [core, trailing punctuation, ends-sentence-candidate]
    for tok in _clean(text).split():
        for j, part in enumerate(_CLAUSE_SEP.split(tok)):
            if j % 2 == 1:
                if pieces:
                    pieces[-1][1] += "..." if part == "…" else "--"
                continue
            m = _EDGE.match(part)
            if not m or not m.group(2):
                continue
            _, core, trail = m.groups()
            pieces.append([core, "".join(ch for ch in trail if ch in ".,;:!?"), "." in trail or "!" in trail or "?" in trail])
    disp, norm, sent, punct = [], [], [], []
    k = 0
    for n, (core, trail, terminal) in enumerate(pieces):
        words: list[tuple[str, str]] = []
        for sub in re.split(r"[-‐-―/]+", core):
            if not sub:
                continue
            if re.search(r"\d", sub):
                try:
                    words += [(w, w.upper()) for w in spell_number(sub)]
                except TranscriptError:
                    if strict:
                        raise
            elif normalize_word(sub):
                words.append((sub, normalize_word(sub)))
        if not words:
            continue
        for i, (d, nw) in enumerate(words):
            disp.append(d)
            norm.append(nw)
            sent.append(k)
            punct.append(trail if i == len(words) - 1 else "")
        nxt = pieces[n + 1][0] if n + 1 < len(pieces) else ""
        abbr = trail == "." and core.lower().rstrip(".") in C.ABBREVIATIONS
        if terminal and not abbr and (not nxt or nxt[0].isupper() or nxt[0].isdigit()):
            k += 1
    if not norm:
        raise TranscriptError("The transcript has no words to read.")
    syl = [count_syllables(w) for w in norm]
    return Transcript(tuple(disp), tuple(norm), tuple(sent), tuple(punct), tuple(s for s, _ in syl), tuple(h for _, h in syl))


# ============================================================================================ emissions
class Aligner:
    """wav2vec2-base-960h on one device ('cpu' or 'cuda:N'), float32, inference mode."""

    def __init__(self, model, device: str = "cpu") -> None:
        self.model, self.device = model, device

    def emissions(self, wav: np.ndarray) -> np.ndarray:
        """Log-probabilities (frames, 29) float32. Audio longer than CHUNK_S is processed in CHUNK_S ownership chunks with
        CONTEXT_S of context on each side, snapped to 320-sample multiples. Frame f covers samples [320 f, 320 f + 400)."""
        import torch
        n = len(wav)
        step = int(C.CHUNK_S * C.SR) // C.CTC_STRIDE * C.CTC_STRIDE
        ctx = int(C.CONTEXT_S * C.SR) // C.CTC_STRIDE * C.CTC_STRIDE
        parts = []
        with torch.inference_mode():
            a = 0
            while a < n:
                b = min(a + step, n)
                if n - b < C.CTC_STRIDE:  # do not leave a sliver for a last chunk
                    b = n
                context_start, context_end = max(0, a - ctx), min(n, b + ctx)
                x = torch.from_numpy(np.ascontiguousarray(wav[context_start:context_end], dtype=np.float32))[None].to(self.device)
                em, _ = self.model(x)
                em = em[0]
                first_frame = (a - context_start) // C.CTC_STRIDE
                keep = em.shape[0] - first_frame if b == n else (b - a) // C.CTC_STRIDE
                parts.append(em[first_frame:first_frame + keep])
                a = b
            lp = torch.log_softmax(torch.cat(parts, 0), -1)
        return lp.cpu().numpy().astype(np.float32)


def verify_checkpoint() -> str:
    """SHA-256 of the cached checkpoint must match the pinned one; returns the hash."""
    import torch
    path = Path(torch.hub.get_dir()) / "checkpoints" / C.CHECKPOINT_NAME
    if not path.exists():
        raise FileNotFoundError(f"aligner checkpoint missing after load: {path}")
    if path.stat().st_size != C.CHECKPOINT_BYTES:
        raise RuntimeError(f"aligner checkpoint size {path.stat().st_size} != {C.CHECKPOINT_BYTES}")
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    if h.hexdigest() != C.CHECKPOINT_SHA256:
        raise RuntimeError(f"aligner checkpoint SHA-256 {h.hexdigest()} != pinned {C.CHECKPOINT_SHA256}")
    return h.hexdigest()


@lru_cache(maxsize=None)
def load_aligner(device: str = "cpu", threads: int = C.TORCH_THREADS) -> Aligner:
    """The aligner on `device`, loaded once per (device, threads). The checkpoint is verified by SHA-256 before use."""
    import torch
    import torchaudio
    torch.set_num_threads(threads)
    torch.manual_seed(C.SEED)
    if device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError(f"aligner device {device} requested but this torch build sees no CUDA device")
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    if tuple(bundle.get_labels()) != LABELS:
        raise RuntimeError("aligner label set differs from the pinned vocabulary")
    model = bundle.get_model().eval()
    verify_checkpoint()
    return Aligner(model.to(device).float(), device)


def emissions(aligner: Aligner, wav: np.ndarray) -> np.ndarray:
    """Log-probabilities of a recording (see Aligner.emissions)."""
    return aligner.emissions(wav)


def greedy_words(logp: np.ndarray) -> list[dict]:
    """Greedy CTC decode -> words [{norm, start, end}] (seconds, frame times)."""
    ids = logp.argmax(1)
    cuts = np.r_[0, np.flatnonzero(ids[1:] != ids[:-1]) + 1, len(ids)]
    words, chars = [], []

    def flush():
        if chars:
            words.append({"norm": "".join(c[0] for c in chars), "start": chars[0][1], "end": chars[-1][2]})
            chars.clear()

    for a, b in zip(cuts[:-1], cuts[1:]):
        k = int(ids[a])
        if k == 0:
            continue
        if LABELS[k] == "|":
            flush()
        else:
            chars.append((LABELS[k], float(a * C.CTC_FRAME_S), float(b * C.CTC_FRAME_S)))
    flush()
    return words


# ============================================================================================ Viterbi
def build_targets(norm: tuple[str, ...] | list[str]) -> tuple[np.ndarray, list[list[int]]]:
    """CTC targets (word chars separated by '|') and the target positions of each word's characters."""
    tg: list[int] = []
    idx: list[list[int]] = []
    for i, w in enumerate(norm):
        if i:
            tg.append(VOCAB["|"])
        pos = []
        for ch in w:
            pos.append(len(tg))
            tg.append(VOCAB[ch])
        idx.append(pos)
    return np.asarray(tg, dtype=np.int64), idx


def ctc_viterbi(logp: np.ndarray, targets: np.ndarray, blank: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """CTC forced alignment (max-product, float64 DP, int8 back-pointers; same tie order as torchaudio's op).
    Returns (states[T], ext[S]): states[t] indexes the blank-extended label sequence; target position l <-> state 2l+1."""
    logp = np.asarray(logp, dtype=np.float64)
    T, L = logp.shape[0], len(targets)
    S = 2 * L + 1
    n_rep = int((targets[1:] == targets[:-1]).sum())
    if T < L + n_rep:
        raise TranscriptMismatch(f"audio too short for the transcript: {T} frames < {L + n_rep} needed", MISMATCH_SHORT,
                                 (L + n_rep) * C.CTC_FRAME_S)
    ext = np.full(S, blank, dtype=np.int64)
    ext[1::2] = targets
    can_skip = np.zeros(S, dtype=bool)
    can_skip[3::2] = targets[1:] != targets[:-1]
    em = logp[:, ext]
    alpha = np.full(S, NEG)
    alpha[0], alpha[1] = em[0, 0], em[0, 1]
    bp = np.zeros((T, S), dtype=np.int8)
    ar = np.arange(S)
    for t in range(1, T):
        p1 = np.empty(S)
        p1[0], p1[1:] = NEG, alpha[:-1]
        p2 = np.empty(S)
        p2[:2], p2[2:] = NEG, alpha[:-2]
        p2[~can_skip] = NEG
        cand = np.stack((alpha, p1, p2))
        k = cand.argmax(0)
        alpha = cand[k, ar] + em[t]
        bp[t] = k
    s = S - 1 if alpha[S - 1] >= alpha[S - 2] else S - 2
    states = np.empty(T, dtype=np.int64)
    for t in range(T - 1, -1, -1):
        states[t] = s
        s -= int(bp[t, s])  # int(): int8 would overflow once S > 127
    return states, ext


def _token_frames(states: np.ndarray, n_targets: int) -> tuple[np.ndarray, np.ndarray]:
    """First and last frame (inclusive) on which each target position is emitted."""
    first = np.full(n_targets, -1, dtype=np.int64)
    last = np.full(n_targets, -1, dtype=np.int64)
    t_idx = np.nonzero(states % 2 == 1)[0]
    l_idx = (states[t_idx] - 1) // 2
    last[l_idx] = t_idx
    first[l_idx[::-1]] = t_idx[::-1]
    return first, last


@dataclass
class Alignment:
    """Raw CTC word timing of one recording. start/end in seconds; compat = per-word posterior compatibility, reported
    (notice, QA), never used to exclude a word. missing/extra: per-frame evidence (nats, >= 0) of transcript characters
    that the audio does not contain and of speech that the transcript does not contain (`mismatch_evidence`); used only
    by `require_full_match`."""
    start: np.ndarray
    end: np.ndarray
    compat: np.ndarray
    mean_compat: float
    decoded: list[dict] = field(default_factory=list)
    char_spans: np.ndarray = field(default_factory=lambda: np.empty((0, 2)))
    missing: np.ndarray = field(default_factory=lambda: np.empty(0))
    extra: np.ndarray = field(default_factory=lambda: np.empty(0))

    def __len__(self) -> int:
        return len(self.start)


def mismatch_evidence(logp: np.ndarray, targets: np.ndarray, states: np.ndarray, ext: np.ndarray, first: np.ndarray,
                      last: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(missing, extra), one value per frame in nats, from a forced path.
    missing: at the first frame of each transcript character, minus the best log-probability of its label within
    MISMATCH_TOL_FRAMES frames of its forced span. extra: on each spike frame (a letter is the most probable label, with
    probability above MISMATCH_SPIKE_P) whose letter the forced path does not give within MISMATCH_TOL_FRAMES frames, the
    best log-probability minus the log-probability of the forced label. The tolerance keeps a forced path that runs a few
    frames behind the spikes (fast speech) from counting as a mismatch. Both are log-likelihood ratios of the free
    best label to the transcript, as in the goodness-of-pronunciation score (Witt and Young 2000, Speech Communication
    30:95-108)."""
    n_frames, tol = len(logp), C.MISMATCH_TOL_FRAMES
    forced = ext[states]
    best, label = logp.max(1), logp.argmax(1)
    missing = np.zeros(n_frames)
    for p in np.flatnonzero(targets != VOCAB["|"]):
        a, b = max(0, first[p] - tol), min(n_frames, last[p] + tol + 1)
        missing[first[p]] -= float(logp[a:b, targets[p]].max())
    covered = np.zeros(n_frames, dtype=bool)
    padded = np.concatenate((np.full(tol, -1), forced, np.full(tol, -1)))
    for shift in range(2 * tol + 1):
        covered |= padded[shift:shift + n_frames] == label
    spike = (label > VOCAB["|"]) & (best > np.log(C.MISMATCH_SPIKE_P))
    extra = np.where(spike & ~covered, best - logp[np.arange(n_frames), forced], 0.0)
    return missing.astype(np.float32), extra.astype(np.float32)


def align_emissions(logp: np.ndarray, norm: tuple[str, ...]) -> Alignment:
    """Forced alignment of the words `norm` against log-probabilities. Records the mean compatibility; the refusal below
    MEAN_COMPAT_MIN is `require_match`, applied only at trust boundaries (uploads, passage selection)."""
    targets, idx = build_targets(norm)
    states, ext = ctc_viterbi(logp, targets)
    first, last = _token_frames(states, len(targets))
    start = np.array([first[p[0]] * C.CTC_FRAME_S for p in idx])
    end = np.array([(last[p[-1]] + 1) * C.CTC_FRAME_S for p in idx])
    compat = np.empty(len(idx))
    for w, pos in enumerate(idx):
        peaks = [float(logp[first[token]:last[token] + 1, ext[2 * token + 1]].max()) for token in pos]
        compat[w] = float(np.exp(np.mean(peaks)))
    chars = np.flatnonzero(targets != VOCAB["|"])
    spans = np.column_stack((first[chars], last[chars] + 1)) * C.CTC_FRAME_S
    missing, extra = mismatch_evidence(logp, targets, states, ext, first, last)
    return Alignment(start, end, compat, float(compat.mean()), greedy_words(logp), spans, missing, extra)


def require_match(al: Alignment) -> Alignment:
    """Trust-boundary check: refuse a recording whose mean word compatibility is below MEAN_COMPAT_MIN."""
    if al.mean_compat < C.MEAN_COMPAT_MIN:
        raise TranscriptMismatch(f"transcript does not match the audio (mean word compatibility {al.mean_compat:.3f} < {C.MEAN_COMPAT_MIN})")
    return al


def worst_window(values: np.ndarray, window_s: float) -> tuple[float, int]:
    """(sum, first frame) of the window of window_s seconds with the largest sum of the per-frame values."""
    frames = int(round(window_s / C.CTC_FRAME_S))
    values = np.asarray(values, dtype=np.float64)
    if len(values) <= frames:
        return float(values.sum()), 0
    total = np.concatenate(([0.0], np.cumsum(values)))
    sums = total[frames:] - total[:-frames]
    first = int(sums.argmax())
    return float(sums[first]), first


def words_near(al: Alignment, t: float) -> tuple[int, int]:
    """First and last index of the MISMATCH_QUOTE_WORDS words (fewer at the end) from the word at time t s, or from the
    nearest word when t falls between words."""
    inside = np.flatnonzero((al.start <= t) & (al.end > t))
    if len(inside):
        word = int(inside[0])
    else:
        word = int(np.argmin(np.minimum(np.abs(al.start - t), np.abs(al.end - t))))
    return word, min(len(al) - 1, word + C.MISMATCH_QUOTE_WORDS - 1)


def evidence_centre(values: np.ndarray, first: int, window_s: float) -> float:
    """Evidence-weighted mean time (s) of the window that starts at frame `first`."""
    frames = int(round(window_s / C.CTC_FRAME_S))
    part = np.asarray(values[first:first + frames], dtype=np.float64)
    return float((first + np.average(np.arange(len(part)), weights=part)) * C.CTC_FRAME_S)


def spread_rate(extra: np.ndarray) -> float:
    """Extra evidence outside the worst MISMATCH_SPREAD_EXCLUDE_S window, in nats per second of the recording: high when
    the speech that the transcript does not contain is spread over the reading (every second word left out), low for one
    added phrase (a restart, a spoken title)."""
    if len(extra) == 0:
        return 0.0
    rest = float(np.sum(extra, dtype=np.float64)) - worst_window(extra, C.MISMATCH_SPREAD_EXCLUDE_S)[0]
    return rest / (len(extra) * C.CTC_FRAME_S)


def require_full_match(al: Alignment, tr: Transcript) -> Alignment:
    """Upload trust boundary: `require_match`, then refuse a recording when, in one MISMATCH_WINDOW_S window, the missing
    evidence is above MISMATCH_MISSING_MAX (transcript words that the audio does not contain) or the extra evidence is
    above MISMATCH_EXTRA_MAX (speech that the transcript does not contain), or when the extra evidence outside the worst
    window is above MISMATCH_SPREAD_MAX per second (`spread_rate`). The quote comes from the window of the failed check
    with the largest ratio to its limit (for the spread check, the worst extra window)."""
    require_match(al)
    if len(al.missing) == 0 or len(al.extra) == 0:
        raise ValueError("the alignment has no mismatch evidence: align it again with align_emissions")
    missing, missing_at = worst_window(al.missing, C.MISMATCH_WINDOW_S)
    extra, extra_at = worst_window(al.extra, C.MISMATCH_WINDOW_S)
    spread = spread_rate(al.extra)
    checks = [("missing", missing, C.MISMATCH_MISSING_MAX, al.missing, missing_at),
              ("extra", extra, C.MISMATCH_EXTRA_MAX, al.extra, extra_at),
              ("spread extra", spread, C.MISMATCH_SPREAD_MAX, al.extra, extra_at)]
    failed = [c for c in checks if c[1] > c[2]]
    if not failed:
        return al
    side, value, limit, values, first = max(failed, key=lambda c: c[1] / c[2])
    centre = evidence_centre(values, first, C.MISMATCH_WINDOW_S)
    i0, i1 = words_near(al, centre)
    raise TranscriptMismatch(f"part of the transcript does not match the audio: {side} evidence {value:.1f} > {limit} "
                             f"(missing {missing:.1f} nats, extra {extra:.1f} nats in {C.MISMATCH_WINDOW_S} s windows, "
                             f"spread {spread:.2f} nats/s), centre {centre:.2f} s (words {i0}-{i1})",
                             MISMATCH_PART, at_s=centre, near=" ".join(tr.disp[i0:i1 + 1]))


def align_audio(aligner: Aligner, wav: np.ndarray, tr: Transcript) -> Alignment:
    """Emissions + forced alignment of a recording (already cropped to the passage)."""
    return align_emissions(emissions(aligner, wav), tr.norm)


# ============================================================================================ pauses
def frame_index(t: float) -> int:
    """First frame whose centre is at or after time t (s); the 1e-9 margin keeps a time on a frame centre on that frame."""
    return int(np.ceil(t / C.HOP_S - 1e-9))


def pause_threshold(L: np.ndarray) -> float:
    """theta = max(Q5(L) + clip(0.3 * (Q95(L) - Q5(L)), 6, 15), Q99(L) - 35) dB: a margin above the noise floor, but never
    more than 35 dB below the speech peaks (the floor of a gated recording says nothing about the breath noise in its pauses)."""
    q5, q95, peak = np.percentile(L, (*C.PAUSE_Q, C.PAUSE_PEAK_Q))
    return float(max(q5 + np.clip(C.PAUSE_FRAC * (q95 - q5), *C.PAUSE_CLIP_DB), peak - C.PAUSE_PEAK_DB))


def acoustic_pauses(al: Alignment, L: np.ndarray, voiced: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """For the boundary after word i: sil[i] (s) = the longest run of unvoiced frames with level below theta between the
    centre of word i and the centre of word i + 1, if it lasts at least PAUSE_MIN_S, else 0; span[i] = (start, end) of that
    run in s (NaN when sil is 0); raw[i] = the same run's length without the PAUSE_MIN_S cut (pause differences use it, so
    a 0.19 s gap against a 0.20 s gap is 0.01 s, not a new pause). The search runs centre to centre, not edge to edge,
    because the aligner sometimes stretches a word edge across a pause; breaks of at most PAUSE_BRIDGE_FRAMES frames (a
    click, one mis-tracked frame) do not split a run. All have n_words - 1 entries."""
    silent = (L < pause_threshold(L)) & ~voiced
    k = np.flatnonzero(silent)
    for a, b in zip(k[:-1], k[1:]):
        if 1 < b - a <= C.PAUSE_BRIDGE_FRAMES + 1:
            silent[a:b] = True
    n = len(al)
    sil = np.zeros(max(n - 1, 0))
    raw = np.zeros(max(n - 1, 0))
    span = np.full((max(n - 1, 0), 2), np.nan)
    eps = 1e-9
    mid = 0.5 * (al.start + al.end)
    for i in range(n - 1):
        k0 = frame_index(mid[i])
        k1 = frame_index(mid[i + 1])  # frames k0 .. k1-1 have centres between the two word centres
        run = best = best_end = 0
        for k in range(k0, min(k1, len(silent))):
            run = (run + 1) if silent[k] else 0
            if run > best:
                best, best_end = run, k + 1
        raw[i] = best * C.HOP_S
        dur = raw[i]
        if dur >= C.PAUSE_MIN_S - eps:
            sil[i] = dur
            span[i] = ((best_end - best) * C.HOP_S, best_end * C.HOP_S)
    return sil, span, raw
