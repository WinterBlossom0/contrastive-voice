"""Standalone research recipes: each returns (PCM audio, analytic Chain, make_labels-shaped labels).

Level None is a bit-identical null-parameter control. Word indices are inclusive; sound_span and
release_sample, when supplied, are parent sample coordinates. The shared registry is in config.py.
The monotone map follows retained tokens; inserted copies have separate source/clip spans in labels.
Filled pauses require a recorded filler and are outside this module's scope.
"""
from __future__ import annotations

import numpy as np
from scipy import signal

from . import audio, config as C
from .features import Recording, frame_features, frame_slice
from .flaws import (Chain, EditError, Warp, _ramp_window, deemphasis, insert_pause,
                    parent_pauses, psola, remove_pause, room_tone, splice_whole, stretch_span, wsola)

from .config import (
    RUSH_RATE, RUSH_PAUSE_KEEP, HESITATION_STRETCH, HESITATION_PAUSE_S, READING_PAUSE_S,
    TEMPO_DEVIATION, WORD_REPEAT_STRETCH, WORD_REPEAT_PAUSE_S, SOUND_REPEAT_COPIES, SOUND_REPEAT_PAUSE_S,
    ONSET_TARGET_S, ONSET_FRACTION, BLOCK_PAUSE_S,
    EFFORT_GAIN_DB, EFFORT_PITCH_ST, TRAIL_GAIN_DB,
    TILT_KNEE_HZ, EMPH_DURATION, EMPH_PITCH_ST, EMPH_GAIN_DB,
    EMPH_REMOVE, ENDING_WINDOW_S, ENDING_RISE_ST, CONTOUR_STRENGTH, ALIGNMENT_ERROR_S,
)

FUNCTION_WORDS = C.FUNCTION_WORDS



RECIPE_EVIDENCE = {
    "NATURAL_RUSH": ("pace_pauses §1/§4: rate 13–18%; pause fractions chosen", "uniform word compression omits selective unstressed/vowel shortening; short unclassified gaps unchanged"),
    "HESITATION": ("pace_pauses §4: silence 0.2–1 s; stretch factors chosen", "content word; 30 ms non-pausal gap energy minimum; no retrieval physiology"),
    "WORD_BY_WORD": ("pace_pauses §4: silence 0.15–0.3 s", "internal eligible gaps only; L1 may be below 200 ms pause threshold"),
    "UNEVEN_TEMPO": ("pace_pauses §4: mean-one factors; deviation chosen", "nominal mean one; integer rounding; no syllable rhythm model"),
    "WORD_REPETITION": ("disfluency §2.2/§4: first token lengthened; factors chosen; gap 100–350 ms", "function-word copy; duration ±8% and gain ±1 dB chosen; no tension/F0 variation"),
    "SOUND_REPETITION": ("disfluency §2.1/§4: 2–5 copies; gap 100–350 ms", "first 20% onset copy; stress fallback recorded; no tension; duration/level variation chosen"),
    "RHYME_PROLONGATION": ("disfluency §4: phones 2–4x, WSOLA 5–10x; added seconds chosen above 89 ms error", "voiced stable edge run ≥90 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted"),
    "ONSET_PROLONGATION": ("disfluency §2.1/§4: up to about 1 s; 2–10x bound; targets chosen", "100 ms voiced stable onset run; stress fallback; unvoiced continuants omitted"),
    "BLOCK": ("disfluency §2.1/§4: gap 0.5–2 s", "signal closure-to-burst energy/flux rise within 80 ms; no tense closure or enhanced burst"),
    "LOW_EFFORT": ("volume_clarity §2.1/§4: alpha/level 0.4–0.7; 0.55 chosen; gain and F0 shift chosen", "tilt fitted after room mixing on parent voiced speech above floor; source/formants/vowel duration omitted; 5 Hz/dB not established for sentences"),
    "TRAILING_OFF": ("volume_clarity §2.2/§4: end-word gain/tilt ramp; magnitudes chosen", "last three words; 100 ms release; tilt fitted after mixing; lax/irregular phonation omitted"),
    "MISPLACED_EMPHASIS": ("pitch_emphasis §4: boost function word and remove stressed prominence; magnitudes chosen", "stress/text prior; no accent dictionary; natural legitimate function-word accents not modelled"),
    "RISING_ENDING": ("pitch_emphasis §4: last 200–300 ms; 250 ms and rises chosen", "add ramp to natural contour; clipped to final word; PSOLA approximate; no syllable annotation"),
    "FLAT_FINAL_FALL": ("pitch_emphasis §4: preceding-word target; strengths chosen", "last 250 ms clipped to final word; preceding median; PSOLA approximate"),
    "REPEATED_CONTOUR": ("pitch_emphasis §4: time-normalised sentence contour; strengths chosen", "template/target ≥0.5 s chosen; linear time warp; interpolate across unvoiced template gaps; no syntactic matching"),
}


def _params(level, **values):
    if level is None:
        return None
    if level not in (1, 2, 3):
        raise ValueError("level must be 1, 2, 3 or None (placebo)")
    return {k: v[level - 1] for k, v in values.items()}


def _words(rec, words):
    i, j = words
    if not 0 <= i <= j < len(rec.tr):
        raise ValueError("invalid inclusive word span")
    a, b = round(rec.al.start[i] * C.SR), round(rec.al.end[j] * C.SR)
    if not 0 <= a < b <= len(rec.wav):
        raise ValueError("word times must lie inside the recording")
    return a, b


def _content(rec, word):
    _words(rec, (word, word))
    if rec.tr.norm[word] in FUNCTION_WORDS:
        raise ValueError("select a content word")


def _sentence(rec, sentence):
    if not 0 <= sentence < rec.tr.n_sentences:
        raise ValueError("invalid sentence index")
    words = rec.tr.sentence_words(sentence)
    if rec.tr.punct[words[1]] != ".":
        raise ValueError("select a sentence ending in a full stop")
    return words


def gap_point(rec, left):
    if not 0 <= left < len(rec.tr) - 1:
        raise EditError("no internal boundary")
    if rec.sil[left] != 0 or rec.tr.punct[left] or rec.al.start[left + 1] - rec.al.end[left] < C.INSERT_MIN_GAP_S:
        raise EditError("boundary lacks a non-pausal 30 ms gap")
    k0 = int(np.ceil(rec.al.end[left] / C.HOP_S - 1e-9))
    k1 = max(int(np.ceil(rec.al.start[left + 1] / C.HOP_S - 1e-9)), k0 + 1)
    return min((k0 + int(np.argmin(rec.fr.L[k0:k1]))) * C.HOP, len(rec.wav))


def continuant_span(rec, word, onset):
    cache = rec.__dict__.setdefault("_recipe_continuants", {})
    key = (word, onset)
    if key not in cache:
        a, b = _words(rec, (word, word))
        hop, frame = C.HOP, round(C.WSOLA_FRAME_MS * C.SR / 1000)
        starts = np.arange(a, b - frame + 1, hop)
        if len(starts):
            windows = np.array([rec.wav[t:t + frame] for t in starts])
            power = np.abs(np.fft.rfft(windows * np.hanning(frame), axis=1))
            bands = np.array([v.sum(1) for v in np.array_split(power, C.CONTINUANT_BANDS, axis=1)]).T
            bands /= np.maximum(np.linalg.norm(bands, axis=1, keepdims=True), 1e-12)
            change = np.r_[0, np.linalg.norm(np.diff(bands, axis=0), axis=1)]
            idx = np.clip(np.rint((starts + frame / 2) / C.HOP).astype(int), 0, len(rec.fr) - 1)
            good = rec.fr.voiced[idx] & (change <= C.CONTINUANT_CHANGE)
            edges = np.diff(np.r_[False, good, False].astype(int))
            spans = [(int(starts[i]), int(starts[j - 1] + frame))
                     for i, j in zip(np.flatnonzero(edges == 1), np.flatnonzero(edges == -1))
                     if starts[j - 1] + frame - starts[i] >= C.CONTINUANT_MIN_S * C.SR]
            spans = [(lo, hi) for lo, hi in spans if
                     (lo - a if onset else b - hi) <= C.BURST_WINDOW_S * C.SR]
            cache[key] = ((spans[0][0], spans[0][0] + round(C.CONTINUANT_ONSET_S * C.SR)) if onset and spans and
                          spans[0][1] - spans[0][0] >= C.CONTINUANT_ONSET_S * C.SR else
                          (spans[-1][1] - round(C.CONTINUANT_MIN_S * C.SR), spans[-1][1]) if spans and not onset else None)
        else:
            cache[key] = None
    if cache[key] is None:
        raise EditError("no voiced stable continuant of at least 90 ms near word edge")
    return cache[key]


def onset_burst(rec, word):
    cache = rec.__dict__.setdefault("_recipe_bursts", {})
    if word not in cache:
        a, b = _words(rec, (word, word))
        stop = min(b, a + round(C.BURST_WINDOW_S * C.SR))
        n, hop = round(C.BURST_FRAME_S * C.SR), round(C.BURST_STEP_S * C.SR)
        starts = np.arange(a + n, stop - 2 * n, hop)
        scores = []
        for t in starts:
            pre, post = rec.wav[max(a, t - 3*n):t], rec.wav[t:t + n]
            rise = 10 * np.log10((np.mean(post ** 2) + 1e-12) / (np.mean(pre ** 2) + 1e-12))
            flux = np.mean(np.diff(post) ** 2) / (np.mean(np.diff(pre) ** 2) + 1e-12)
            spectrum = np.abs(np.fft.rfft(post * np.hanning(len(post)))) ** 2
            freq = np.fft.rfftfreq(len(post), 1 / C.SR)
            high_share = spectrum[freq > C.BURST_HIGH_HZ].sum() / max(spectrum.sum(), 1e-12)
            scores.append(rise if rise >= C.BURST_RISE_DB and flux >= C.BURST_FLUX_RATIO and high_share > C.BURST_HIGH_SHARE
                          and np.sqrt(np.mean(post ** 2)) > C.BURST_MIN_RMS else -np.inf)
        cache[word] = int(starts[np.argmax(scores)]) if scores and np.isfinite(max(scores)) else None
    if cache[word] is None:
        raise EditError("no closure-to-burst energy/flux rise in first 80 ms")
    return cache[word]


def _sound(rec, word, sound_span, onset, prolong=False):
    a, b = _words(rec, (word, word))
    if sound_span is not None:
        s, e = sound_span
        if not a <= s < e <= b or s != int(s) or e != int(e):
            raise ValueError("sound_span must contain integer samples inside the aligned word")
        span = int(s), int(e)
        method = "caller-supplied sound span"
        if prolong:
            stable = continuant_span(rec, word, onset)
            if e - s < C.CONTINUANT_MIN_S * C.SR or s < stable[0] or e > stable[1]:
                raise EditError("annotation lacks verified voiced stable continuant material")
    elif prolong:
        span, method = continuant_span(rec, word, onset), "voiced stable-spectrum edge run"
    else:
        span, method = (a, a + max(1, round((b - a) * ONSET_FRACTION))), "first 20% onset copy; phone boundary unknown"
    return span, {"method": method, "alignment_error_s_empirical": list(ALIGNMENT_ERROR_S),
                  "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded" if prolong else
                                "no articulatory tension synthesis; onset may include more than one phone"}


class _Builder:
    def __init__(self, rec, measurements=None):
        self.measurements = measurements
        self.rec, self.x, self.chain = rec, rec.wav.copy(), Chain()
        self.supports, self.events = [], []

    def support(self, a, b, pad=0):
        self.supports.append((max(0, a - pad), min(len(self.rec.wav), b + pad)))

    def stretch(self, a, b, factor, isolated=False):
        s, e = self.chain.cur(a, b)
        if min(e - s, round((e - s) * factor)) < round(C.XFADE_S * C.SR):
            raise EditError("sound too short for the WSOLA exit fade")
        if isolated:
            pad = round(0.08 * C.SR)
            local = np.pad(self.x[s:e], (pad, pad), mode="reflect")
            changed, _, n = stretch_span(local, pad, pad + e - s, 1 / factor)
            self.x = np.r_[self.x[:s], changed[pad:pad + n], self.x[e:]]
            w = Warp([0, s, e, len(self.x) - n + e - s], [0, s, s + n, len(self.x)])
        else:
            self.x, w, n = stretch_span(self.x, s, e, 1 / factor)
        self.chain.warps.append(w)
        self.support(a, b)
        self.events.append({"kind": "stretch", "parent_span": [a, b], "output_samples": n})

    def insert(self, point, seconds):
        i = round(float(self.chain(point, "left")))
        n = round(seconds * C.SR)
        f = round(C.PAUSE_FADE_S * C.SR)
        # Padding permits the existing cross-fade primitive even at the clip's edges.
        xp = np.pad(self.x, (f, f))
        yp, _ = insert_pause(xp, i + f, n, room_tone(self.rec))
        self.x = yp[f:-f]
        self.chain.warps.append(Warp([0, i, i, len(xp) - 2 * f], [0, i, i + n, len(self.x)]))
        self.support(point, point, f)
        self.events.append({"kind": "silence", "parent_span": [point, point], "output_samples": n})

    def pitch(self, a, b, fn):
        s, e = self.chain.cur(a, b)
        f = round(C.SPLICE_FADE_S * C.SR)
        xp = np.pad(self.x, (f, f))
        y, _ = psola(xp, pitch_fn=lambda t, v, m: fn(t - f / C.SR, v, m, s / C.SR, e / C.SR))
        y = np.pad(y, (0, max(0, len(xp) - len(y))))[:len(xp)]
        self.x = splice_whole(xp, y, s + f, e + f, e + f)[f:-f]
        self.support(a, b, f)

    def copies(self, a, b, count, factor, pause_s):
        s, e = self.chain.cur(a, b)
        from .flaws import clip_seed
        rng = np.random.default_rng(clip_seed(f"copies:{audio.sha256_pcm(self.rec.wav)}:{a}:{b}"))
        edge = round(C.PAUSE_FADE_S * C.SR)
        tone = room_tone(self.rec)
        pieces, sizes = [], []
        for _ in range(count):
            duration = factor * rng.uniform(1 - C.REPEAT_DURATION_JITTER, 1 + C.REPEAT_DURATION_JITTER)
            gain = rng.uniform(-C.REPEAT_GAIN_JITTER_DB, C.REPEAT_GAIN_JITTER_DB)
            copy = wsola(self.x, s, e, 1 / duration) * 10 ** (gain / 20)
            f = min(edge, len(copy) // 2)
            fade = np.sin(np.linspace(0, np.pi / 2, f)) ** 2
            copy[:f] *= fade
            copy[-f:] *= fade[::-1]
            offset = int(rng.integers(0, C.SR))
            pause_n = round(pause_s * C.SR)
            pause = tone(pause_n + offset)[offset:]
            pieces.extend((copy, pause))
            sizes.append((len(copy), pause_n, duration, gain))
        material = np.concatenate(pieces)
        fill = np.r_[tone(edge), material, tone(edge)]
        xp = np.pad(self.x, (edge, edge))
        yp, _ = insert_pause(xp, s + edge, len(material), lambda n: fill.copy())
        self.x = yp[edge:-edge]
        self.chain.warps.append(Warp([0, s, s, len(xp) - 2 * edge], [0, s, s + len(material), len(self.x)]))
        self.support(a, a, edge)
        lo = s
        for n, pause_n, duration, gain in sizes:
            self.events.append({"kind": "copy", "source_span": [a, b], "clip_span": [lo, lo + n],
                                "pause_span": [lo + n, lo + n + pause_n],
                                "duration_factor": duration, "gain_db": gain})
            lo += n + pause_n


def _f0(fr, a, b):
    sl = frame_slice(a / C.SR, b / C.SR, len(fr))
    t = np.arange(len(fr))[sl] * C.HOP_S
    ok = fr.voiced[sl]
    if ok.sum() < C.MIN_VOICED_WORD:
        raise EditError("too few voiced frames to measure the recipe")
    return t[ok], 12 * np.log2(fr.f0[sl][ok])


def _level(x, a, b):
    return float(10 * np.log10(np.mean(x[a:b] ** 2) + C.LEVEL_EPS))


def _alpha(x, a, b, fr, parent_a=None):
    _, times, spec = signal.stft(x[a:b], C.SR, nperseg=C.NFFT, noverlap=C.NFFT // 2)
    freq = np.fft.rfftfreq(C.NFFT, 1 / C.SR)
    idx = np.clip(np.rint((times + (a if parent_a is None else parent_a) / C.SR) / C.HOP_S).astype(int), 0, len(fr) - 1)
    floor = float(np.percentile(fr.L, 10))
    voiced = fr.voiced[idx] & (fr.L[idx] > floor + C.ALPHA_SPEECH_MARGIN_DB)
    if not voiced.any():
        raise EditError("no voiced speech 15 dB above room floor for alpha")
    power = np.abs(spec[:, voiced]) ** 2
    return float(10 * np.log10((power[(freq >= 1000) & (freq <= 5000)].sum() + 1e-20) /
                              (power[(freq >= 50) & (freq < 1000)].sum() + 1e-20)))


def _finish(builder, typ, level, params, words, metric, *, approximation=None, details=None, seed=0,
            parent_span=None):
    rec, chain = builder.rec, builder.chain
    y = audio.quantize(builder.x)
    a, b = _words(rec, words) if parent_span is None else parent_span
    span = (round(float(chain(a, "left"))), round(float(chain(b, "right"))))
    supports = builder.supports or [(a, b)]
    outside = np.ones(len(rec.wav), bool)
    for lo, hi in supports:
        outside[lo:hi] = False
    mapped = np.rint(chain(np.arange(len(rec.wav)), "right")).astype(np.int64)
    ok = outside & (mapped >= 0) & (mapped < len(y))
    identical = bool(np.array_equal(rec.wav[ok], y[mapped[ok]]))
    if not identical:
        raise EditError("recipe changed samples outside its declared support")
    fy = frame_features(y) if params is not None else rec.fr
    # Reuse the same metric on composed audio; earlier edits shift the measurement frame grid.
    if builder.measurements is not None:
        builder.measurements.append(metric)
    realised = metric(y, fy, chain) if params is not None else {"name": "null_change", "value": 0.0, "unit": "identity"}
    dim, secondary = C.FLAW_DIM[typ], C.EXPECTED_SECONDARY[typ]
    lo, hi = min(s[0] for s in supports), max(s[1] for s in supports)
    flaw = {"type": typ, "dimension": dim, "dimension_name": C.DIM_LABEL.get(dim, dim.title()),
            "level": level, "placebo": params is None, "parameter": params,
            "magnitude": {"name": "recipe_parameters", "value": params, "unit": "named_units"},
            "words": list(words), "family": C.FLAW_FAMILY[typ], "event": C.FLAW_REGISTRY[typ]["event"],
            "parent_span": [a, b], "span": list(span),
            "support": [round(float(chain(lo, "left"))), round(float(chain(hi, "right")))],
            "parent_supports": [list(s) for s in supports], "realised": realised,
            "expected_secondary": list(secondary), "approximation": approximation or {"method": {
                "HESITATION": "aligned content-word prior", "WORD_BY_WORD": "aligned word boundaries",
                "WORD_REPETITION": "function-word prior; copied waveform"}.get(typ, "aligned word spans")},
            "details": details or {}, "events": builder.events, "source": RECIPE_EVIDENCE[typ][0]}
    flaw["approximation"].setdefault("omissions", RECIPE_EVIDENCE[typ][1])
    starts, ends = np.rint(rec.al.start * C.SR), np.rint(rec.al.end * C.SR)
    labels = {"clip": typ.lower(), "parent": {"id": "recording", "sha256": audio.sha256_pcm(rec.wav)},
              "sha256": audio.sha256_pcm(y), "recipe": typ, "seed": seed, "chain": "A", "sr": C.SR,
              "n_samples": len(y), "words": {"start": [round(float(chain(s, "right"))) for s in starts],
                                              "end": [round(float(chain(e, "left"))) for e in ends]},
              "parent_words": {"start": starts.astype(int).tolist(), "end": ends.astype(int).tolist()},
              "flaws": [flaw], "skipped": [], "outside_support_identical": identical,
              "chain_warps": [{"src": w.src.tolist(), "dst": w.dst.tolist()} for w in chain.warps]}
    return y, chain, labels


def _duration_metric(rec, words, name="duration_change", unit="s", parent_span=None):
    a, b = _words(rec, words) if parent_span is None else parent_span
    def metric(y, fy, chain):
        s = round(float(chain(a, "left")))
        e = round(float(chain(b, "right")))
        return {"name": name, "value": ((e - s) - (b - a)) / C.SR, "unit": unit}
    return metric


def natural_rushing(rec: Recording, words: tuple[int, int], level: int | None = 2, *, measurements=None):
    """Compress each aligned speech word and shorten detected pauses between them; require a pause."""
    a, b = _words(rec, words)
    p = _params(level, speech_rate=RUSH_RATE, pause_kept_fraction=RUSH_PAUSE_KEEP)
    build = _Builder(rec, measurements)
    pauses = []
    for i in range(words[0], words[1]):
        left, right = round(rec.al.end[i] * C.SR), round(rec.al.start[i + 1] * C.SR)
        pauses += [(max(s, left), min(e, right)) for s, e in parent_pauses(rec)
                   if min(e, right) > max(s, left)]
    if p is not None:
        if not pauses:
            raise EditError("natural rushing needs an internal acoustic pause")
        for i in reversed(range(words[0], words[1] + 1)):
            build.stretch(*_words(rec, (i, i)), 1 / p["speech_rate"])
        for s, e in reversed(pauses):
            lo, hi = build.chain.cur(s, e)
            keep = round((hi - lo) * p["pause_kept_fraction"])
            build.x, w = remove_pause(build.x, lo, hi, keep)
            build.chain.warps.append(w)
            build.support(s, e, round(C.PAUSE_FADE_S * C.SR))
            build.events.append({"kind": "pause_cut", "parent_span": [s, e], "output_samples": keep})
    return _finish(build, "NATURAL_RUSH", level, p, words, _duration_metric(rec, words),
                   approximation={"method": "uniform word compression omits greater shortening of unstressed syllables and vowels; short unclassified gaps unchanged"})


def hesitation_before_word(rec: Recording, word: int, level: int | None = 2, *, measurements=None):
    _content(rec, word)
    a, b = _words(rec, (word, word))
    p = _params(level, word_duration_factor=HESITATION_STRETCH, silence_s=HESITATION_PAUSE_S)
    build = _Builder(rec, measurements)
    point = gap_point(rec, word - 1) if p is not None else a
    if p is not None:
        build.stretch(a, b, p["word_duration_factor"])
        build.insert(point, p["silence_s"])
    return _finish(build, "HESITATION", level, p, (word, word),
                   _duration_metric(rec, (word, word), parent_span=(point, b)), parent_span=(point, b),
                   approximation={"method": "30 ms non-pausal gap energy minimum before content word"})


def word_by_word_reading(rec: Recording, words: tuple[int, int], level: int | None = 2, *, every: int = 1, measurements=None):
    _words(rec, words)
    if every not in (1, 2):
        raise ValueError("every must be 1 or 2")
    p = _params(level, silence_s=READING_PAUSE_S)
    if p is not None:
        p["every_words"] = every
    build = _Builder(rec, measurements)
    if p is not None:
        for i in reversed(range(words[0] + every - 1, words[1], every)):
            build.insert(gap_point(rec, i), p["silence_s"])
    return _finish(build, "WORD_BY_WORD", level, p, words, _duration_metric(rec, words),
                   approximation={"method": "internal 30 ms non-pausal gap energy minima",
                                  "limitation": "L1 inserted 150 ms can be below 200 ms pause threshold including raw gap"})


def uneven_tempo(rec: Recording, words: tuple[int, int], level: int | None = 2, *, seed: int = 0, measurements=None):
    _words(rec, words)
    n = words[1] - words[0] + 1
    if n < 2:
        raise ValueError("uneven tempo needs at least two words")
    p = _params(level, max_duration_deviation=TEMPO_DEVIATION)
    build = _Builder(rec, measurements)
    z = np.random.default_rng(seed).uniform(-1, 1, n)
    z -= z.mean()
    z /= np.max(np.abs(z))
    factors = np.ones(n) if p is None else 1 + z * p["max_duration_deviation"]
    if p is not None:
        for i, factor in reversed(list(zip(range(words[0], words[1] + 1), factors))):
            build.stretch(*_words(rec, (i, i)), factor)
    def metric(y, fy, chain):
        ratios = []
        for i in range(words[0], words[1] + 1):
            a, b = _words(rec, (i, i))
            s, e = chain.cur(a, b)
            ratios.append((e - s) / (b - a))
        return {"name": "word_duration_ratio_sd", "value": float(np.std(ratios)), "unit": "ratio",
                "mean_ratio": float(np.mean(ratios))}
    return _finish(build, "UNEVEN_TEMPO", level, p, words, metric, seed=seed,
                   details={"word_duration_factors": factors.tolist(), "rounding_samples_per_word": 0.5})


def word_repetition(rec: Recording, word: int, level: int | None = 2, *, measurements=None):
    a, b = _words(rec, (word, word))
    if rec.tr.norm[word] not in FUNCTION_WORDS:
        raise ValueError("typical repetition needs a function word")
    p = _params(level, first_token_duration_factor=WORD_REPEAT_STRETCH, silence_s=WORD_REPEAT_PAUSE_S)
    build = _Builder(rec, measurements)
    if p is not None:
        p["inserted_copies"] = 1
        build.copies(a, b, 1, p["first_token_duration_factor"], p["silence_s"])
    return _finish(build, "WORD_REPETITION", level, p, (word, word), _duration_metric(rec, (word, word)))


def sound_repetition(rec: Recording, word: int, level: int | None = 2, *, sound_span=None, measurements=None):
    """Copy the onset of a selected content word."""
    _content(rec, word)
    (a, b), approximation = _sound(rec, word, sound_span, True)
    p = _params(level, inserted_copies=SOUND_REPEAT_COPIES, silence_s=SOUND_REPEAT_PAUSE_S)
    build = _Builder(rec, measurements)
    if p is not None:
        build.copies(a, b, p["inserted_copies"], 1.0, p["silence_s"])
    return _finish(build, "SOUND_REPETITION", level, p, (word, word),
                   _duration_metric(rec, (word, word)), approximation=approximation, parent_span=(a, a))


def rhyme_prolongation(rec: Recording, word: int, level: int | None = 2, *, sound_span=None, measurements=None):
    (a, b), approximation = _sound(rec, word, sound_span, False, True)
    p = _params(level, added_duration_s=C.RHYME_ADDED_S)
    build = _Builder(rec, measurements)
    if p is not None:
        factor = 1 + p["added_duration_s"] * C.SR / (b - a)
        if not 2 <= factor <= C.PROLONG_MAX_FACTOR:
            raise EditError("rhyme stretch outside published 2–10x range")
        build.stretch(a, b, factor, isolated=True)
        approximation["pre_pausal"] = bool(word == len(rec.tr) - 1 or rec.sil[word] > 0)
        approximation["following_gap_s"] = None if word == len(rec.tr) - 1 else float(rec.al.start[word + 1] - rec.al.end[word])
        approximation["context_rule"] = "at least 30 ms aligned gap; typical pre-interruption context not synthesised"
        approximation["realised_factor"] = factor
    return _finish(build, "RHYME_PROLONGATION", level, p, (word, word),
                   _duration_metric(rec, (word, word)), approximation=approximation, parent_span=(a, b))


def onset_prolongation(rec: Recording, word: int, level: int | None = 2, *, sound_span=None, measurements=None):
    _content(rec, word)
    (a, b), approximation = _sound(rec, word, sound_span, True, True)
    p = _params(level, onset_target_s=ONSET_TARGET_S)
    build = _Builder(rec, measurements)
    if p is not None:
        if b - a >= p["onset_target_s"] * C.SR:
            raise EditError("selected onset already exceeds the target; choose a shorter continuant span")
        factor = p["onset_target_s"] * C.SR / (b - a)
        if not 2 <= factor <= C.PROLONG_MAX_FACTOR:
            raise EditError("onset stretch outside published 2–10x range")
        build.stretch(a, b, factor, isolated=True)
        approximation["realised_factor"] = factor
    return _finish(build, "ONSET_PROLONGATION", level, p, (word, word),
                   _duration_metric(rec, (word, word)), approximation=approximation, parent_span=(a, b))


def block_before_release(rec: Recording, word: int, level: int | None = 2, *, release_sample=None, measurements=None):
    a, b = _words(rec, (word, word))
    point = onset_burst(rec, word) if release_sample is None else release_sample
    if not a < point < b or point != int(point):
        raise ValueError("release_sample must be an integer sample strictly inside the word")
    point = int(point)
    p = _params(level, silence_s=BLOCK_PAUSE_S)
    build = _Builder(rec, measurements)
    if p is not None:
        build.insert(point, p["silence_s"])
    approximation = {"method": "closure-to-burst energy/flux rise in first 80 ms" if release_sample is None else "caller-supplied stop release",
                     "search_window_s": C.BURST_WINDOW_S,
                     "alignment_error_s_empirical": list(ALIGNMENT_ERROR_S),
                     "limitation": "gap only; no tense closure or enhanced release burst is synthesised"}
    return _finish(build, "BLOCK", level, p, (word, word), _duration_metric(rec, (word, word)),
                   approximation=approximation, parent_span=(point, point))


def _voice_metric(rec, words, pitch=False):
    a, b = _words(rec, words)
    def metric(y, fy, chain):
        s, e = chain.cur(a, b)
        result = {"name": "level_change", "value": _level(y, s, e) - _level(rec.wav, a, b), "unit": "dB",
                  "alpha_change_db": _alpha(y, s, e, rec.fr, parent_a=a) - _alpha(rec.wav, a, b, rec.fr)}
        if pitch:
            result["pitch_change_st"] = float(np.median(_f0(fy, s, e)[1]) - np.median(_f0(rec.fr, a, b)[1]))
        return result
    return metric


def _effort_shape(build, a, b, attenuation, alpha_per_db, trailing=False):
    rec = build.rec
    end = min(len(rec.wav), b + round(C.FADE_RELEASE_S * C.SR))
    t = np.arange(a, end) / C.SR
    if trailing:
        weight = np.clip((t - a / C.SR) / ((b - a) / C.SR), 0, 1)
    else:
        weight = np.minimum((t - a / C.SR) / ((b - a) / C.SR * C.FADE_RAMP_FRACTION), 1).clip(0, 1)
    tail = t >= b / C.SR
    weight[tail] = 0.5 + 0.5 * np.cos(np.pi * (t[tail] - b / C.SR) / C.FADE_RELEASE_S)
    original = build.x[a:end].copy()
    freq, times, spec = signal.stft(original, C.SR, nperseg=C.MUMBLE_NFFT,
                                  noverlap=C.MUMBLE_NFFT - C.MUMBLE_HOP)
    spectral_weight = np.interp(times, np.arange(len(weight)) / C.SR, weight, left=0, right=0)
    octaves = np.maximum(np.log2(np.maximum(freq, TILT_KNEE_HZ) / TILT_KNEE_HZ), 0)
    gain = 10 ** (-attenuation * weight / 20)
    tone = room_tone(rec)(len(original))
    before_alpha = _alpha(rec.wav, a, b, rec.fr)
    target_level = _level(original[:b-a] * gain[:b-a], 0, b-a)
    drop = max(0, _level(rec.wav, a, b) - target_level)
    target_alpha = before_alpha - alpha_per_db * drop
    def render(tilt):
        changed = spec * 10 ** (-tilt * octaves[:, None] * spectral_weight[None, :] / 20)
        changed *= np.sqrt(np.sum(np.abs(spec) ** 2, axis=0) / np.maximum(np.sum(np.abs(changed) ** 2, axis=0), 1e-20))
        _, filtered = signal.istft(changed, C.SR, nperseg=C.MUMBLE_NFFT,
                                   noverlap=C.MUMBLE_NFFT - C.MUMBLE_HOP)
        out = filtered[:len(original)] * gain + tone * (C.EFFORT_ROOM_FILL * np.sqrt(1 - gain ** 2))
        correction = 10 ** ((target_level - _level(out, 0, b-a)) / 20)
        out *= 1 + (correction - 1) * np.minimum(weight * 20, 1)
        fade = min(round(C.XFADE_S * C.SR), len(out) // 2)
        mix = np.ones(len(out))
        mix[:fade] = np.linspace(0, 1, fade)
        mix[-fade:] = np.linspace(1, 0, fade)
        return original * (1 - mix) + out * mix
    lo, hi = -10.0, 20.0
    for _ in range(16):
        tilt = (lo + hi) / 2
        out = render(tilt)
        trial = rec.wav.copy()
        trial[a:end] = out
        alpha = _alpha(trial, a, b, rec.fr)
        target_alpha = before_alpha + alpha_per_db * (_level(out, 0, b-a) - _level(rec.wav, a, b))
        if alpha > target_alpha:
            lo = tilt
        else:
            hi = tilt
    build.x[a:end] = render((lo + hi) / 2)
    build.support(a, end)
    return {"fitted_tilt_db_oct": (lo + hi) / 2, "target_alpha_change_db": target_alpha - before_alpha,
            "room_fill_scale": C.EFFORT_ROOM_FILL, "release_s": (end - b) / C.SR}


def low_vocal_effort(rec: Recording, words: tuple[int, int], level: int | None = 2, *, measurements=None):
    a, b = _words(rec, words)
    p = _params(level, attenuation_db=EFFORT_GAIN_DB, alpha_drop_per_db=(C.EFFORT_ALPHA_PER_DB,) * 3,
                pitch_lowering_st=EFFORT_PITCH_ST)
    build = _Builder(rec, measurements)
    details = {}
    if p is not None:
        build.pitch(a, b, lambda t, v, m, s, e: v * 2 ** (-p["pitch_lowering_st"] *
                    _ramp_window(t, s, e, C.FLATTEN_RAMP_S) / 12))
        details = _effort_shape(build, a, b, p["attenuation_db"], p["alpha_drop_per_db"])
    return _finish(build, "LOW_EFFORT", level, p, words, _voice_metric(rec, words, True), details=details,
                   approximation={"method": "alpha fitted after room-tone mixing on parent voiced speech above floor",
                                  "limitation": "small F0 shift chosen; isolated-vowel 5 Hz/dB not imposed; glottal source, formants and vowel duration omitted"})


def trailing_off(rec: Recording, sentence: int, level: int | None = 2, *, measurements=None):
    first, last = _sentence(rec, sentence)
    words = (max(first, last - C.TRAIL_WORDS + 1), last)
    a, b = _words(rec, words)
    p = _params(level, final_attenuation_db=TRAIL_GAIN_DB, alpha_drop_per_db=(C.EFFORT_ALPHA_PER_DB,) * 3)
    build = _Builder(rec, measurements)
    details = {}
    if p is not None:
        details = _effort_shape(build, a, b, p["final_attenuation_db"], C.EFFORT_ALPHA_PER_DB, True)
    def metric(y, fy, chain):
        result = _voice_metric(rec, words)(y, fy, chain)
        s, e = chain.cur(a, b)
        sl = frame_slice(s / C.SR, e / C.SR, len(fy))
        t = np.arange(len(fy))[sl] * C.HOP_S
        idx = np.clip(np.rint((t - (s - a) / C.SR) / C.HOP_S).astype(int), 0, len(rec.fr) - 1)
        ok = rec.fr.voiced[idx] & fy.voiced[sl]
        if ok.sum() < 2:
            raise EditError("too few speech frames for trailing level slope")
        result["level_slope_change_db_s"] = float(np.polyfit(t[ok], fy.L[sl][ok] - rec.fr.L[idx][ok], 1)[0])
        wa, wb = _words(rec, (last, last))
        result["last_word_level_change_db"] = _level(y, *chain.cur(wa, wb)) - _level(rec.wav, wa, wb)
        return result
    return _finish(build, "TRAILING_OFF", level, p, words, metric, details=details,
                   approximation={"method": "last three words gain/tilt ramp with 100 ms release; final-waveform alpha on parent speech",
                                  "limitation": "lax/irregular phonation omitted; tilt fitted to alpha coupling; no published severity cutoffs"})


def misplaced_emphasis(rec: Recording, function_word: int, stressed_word: int, level: int | None = 2, *, measurements=None):
    """The caller identifies the reference-stressed word; equal-cue prominence uses parent scales."""
    fa, fb = _words(rec, (function_word, function_word))
    sa, sb = _words(rec, (stressed_word, stressed_word))
    _content(rec, stressed_word)
    if rec.tr.norm[function_word] not in FUNCTION_WORDS or rec.tr.sentence[function_word] != rec.tr.sentence[stressed_word]:
        raise ValueError("select a function word and a stressed content word in the same sentence")
    p = _params(level, function_duration_factor=EMPH_DURATION, function_pitch_st=EMPH_PITCH_ST,
                function_gain_db=EMPH_GAIN_DB, stressed_removal_strength=EMPH_REMOVE)
    build = _Builder(rec, measurements)
    if p is not None:
        s, e = build.chain.cur(sa, sb)
        build.x, warps, _ = deemphasis(build.x, s, e, p["stressed_removal_strength"])
        build.chain.warps += warps
        s2, e2 = build.chain.cur(sa, sb)
        build.events.append({"kind": "stretch", "parent_span": [sa, sb], "output_samples": e2 - s2})
        build.support(sa, sb, round(C.SPLICE_FADE_S * C.SR))
        build.stretch(fa, fb, p["function_duration_factor"])
        build.pitch(fa, fb, lambda t, v, m, s, e: v * 2 ** (p["function_pitch_st"] *
                    _ramp_window(t, s, e, C.DEEMPH_RAMP_S) / 12))
        s, e = build.chain.cur(fa, fb)
        t = np.arange(e - s) / C.SR + s / C.SR
        build.x[s:e] *= 10 ** (p["function_gain_db"] * _ramp_window(t, s / C.SR, e / C.SR, C.DEEMPH_RAMP_S) / 20)
    def prominence(y, fr, chain, word):
        a, b = _words(rec, (word, word))
        s, e = chain.cur(a, b)
        _, st = _f0(fr, s, e)
        sl = frame_slice(s / C.SR, e / C.SR, len(fr))
        median_pitch = 12 * np.log2(np.median(rec.fr.f0[rec.fr.voiced]))
        median_level = np.median(rec.fr.L[rec.fr.voiced])
        u = np.array([np.log((e - s) / C.SR / rec.tr.syll[word]),
                      np.percentile(st, 90) - median_pitch, np.percentile(fr.L[sl], 90) - median_level])
        return float(np.mean((u - rec.m) / rec.sigma))
    def metric(y, fy, chain):
        shifts = [prominence(y, fy, chain, w) - prominence(rec.wav, rec.fr, Chain(), w)
                  for w in (function_word, stressed_word)]
        return {"name": "prominence_transfer", "value": shifts[0] - shifts[1], "unit": "p",
                "function_change_p": shifts[0], "stressed_change_p": shifts[1]}
    words = (min(function_word, stressed_word), max(function_word, stressed_word))
    return _finish(build, "MISPLACED_EMPHASIS", level, p, words, metric,
                   details={"function_word": function_word, "reference_stressed_word": stressed_word})


def _ending(rec, sentence, level, flat, measurements=None):
    words = _sentence(rec, sentence)
    wa, b = _words(rec, (words[1], words[1]))
    a = max(wa, b - round(ENDING_WINDOW_S * C.SR))
    p = _params(level, strength=CONTOUR_STRENGTH) if flat else _params(level, rise_st=ENDING_RISE_ST)
    build = _Builder(rec, measurements)
    approximation = {"method": "last 250 ms, clipped to final word; no syllable boundary assumed",
                     "actual_window_s": (b - a) / C.SR,
                     "rise_extent": "first to last parent voiced frame inside window",
                     "alignment_error_s_empirical": list(ALIGNMENT_ERROR_S)}
    if p is not None:
        t0, st0 = _f0(rec.fr, a, b)
        if flat:
            if words[0] == words[1]:
                raise EditError("flattened final fall needs a preceding word")
            pa, pb = _words(rec, (words[1] - 1, words[1] - 1))
            target = float(np.median(_f0(rec.fr, pa, pb)[1]))
            def fn(t, v, med, s, e):
                st = 12 * np.log2(v)
                inside = (t >= s) & (t <= e)
                st[inside] += p["strength"] * (target - st[inside])
                return 2 ** (st / 12)
        else:
            def fn(t, v, med, s, e):
                st = 12 * np.log2(v)
                inside = (t >= s) & (t <= e)
                start = s + t0[0] - a / C.SR
                duration = t0[-1] - t0[0]
                st[inside] += p["rise_st"] * np.clip((t[inside] - start) / duration, 0, 1)
                return 2 ** (st / 12)
        build.pitch(a, b, fn)
    def metric(y, fy, chain):
        s, e = chain.cur(a, b)
        t, st = _f0(fy, s, e)
        t0, st0 = _f0(rec.fr, a, b)
        if flat:
            pa, pb = _words(rec, (words[1] - 1, words[1] - 1))
            target = float(np.median(_f0(rec.fr, pa, pb)[1]))
            value = float(np.sqrt(np.mean((st - target) ** 2)) - np.sqrt(np.mean((st0 - target) ** 2)))
            return {"name": "final_target_rmse_change", "value": value, "unit": "st",
                    "before_rmse_st": float(np.sqrt(np.mean((st0 - target) ** 2)))}
        slope = float(np.polyfit(t, st, 1)[0])
        parent_t = t - (s - a) / C.SR
        idx = np.clip(np.rint(parent_t / C.HOP_S).astype(int), 0, len(rec.fr) - 1)
        common = rec.fr.voiced[idx] & (parent_t >= t0[0]) & (parent_t <= t0[-1])
        if common.sum() < C.MIN_VOICED_WORD:
            raise EditError("too few common voiced frames to measure added rise")
        parent_st = np.interp(parent_t[common], t0, st0)
        delta = st[common] - parent_st
        ramp = np.clip((parent_t[common] - t0[0]) / (t0[-1] - t0[0]), 0, 1)
        value = float(np.dot(ramp - ramp.mean(), delta - delta.mean()) / max(np.sum((ramp - ramp.mean()) ** 2), 1e-12))
        return {"name": "added_endpoint_rise", "value": value, "unit": "st",
                "slope_change_st_s": slope - float(np.polyfit(t0, st0, 1)[0]),
                "final_slope_st_s": slope, "final_change_st": slope * float(t[-1]-t[0])}
    return _finish(build, "FLAT_FINAL_FALL" if flat else "RISING_ENDING", level, p,
                   (words[1], words[1]), metric, approximation=approximation, parent_span=(a, b))


def rising_ending(rec: Recording, sentence: int, level: int | None = 2, *, measurements=None):
    return _ending(rec, sentence, level, False, measurements)


def flattened_final_fall(rec: Recording, sentence: int, level: int | None = 2, *, measurements=None):
    return _ending(rec, sentence, level, True, measurements)


def repeated_contour(rec: Recording, template_sentence: int = 0, level: int | None = 2, *, target_sentences=None, measurements=None):
    """Copy absolute log-F0 by linear normalised sentence time; unvoiced regions stay unvoiced."""
    template = _sentence(rec, template_sentence)
    ta, tb = _words(rec, template)
    targets = list(range(rec.tr.n_sentences)) if target_sentences is None else list(target_sentences)
    targets = [s for s in targets if s != template_sentence]
    if not targets or len(set(targets)) != len(targets):
        raise ValueError("choose distinct target sentences other than the template")
    target_words = [_sentence(rec, s) for s in targets]
    p = _params(level, contour_strength=CONTOUR_STRENGTH)
    build = _Builder(rec, measurements)
    if p is not None:
        tt, template_st = _f0(rec.fr, ta, tb)
        norm = (tt - ta / C.SR) / ((tb - ta) / C.SR)
        for words in target_words:
            a, b = _words(rec, words)
            def fn(t, v, med, s, e):
                st = 12 * np.log2(v)
                inside = (t >= s) & (t <= e)
                target = np.interp((t[inside] - s) / (e - s), norm, template_st)
                st[inside] += p["contour_strength"] * (target - st[inside])
                return 2 ** (st / 12)
            build.pitch(a, b, fn)
    def error(fr, chain):
        errors = []
        for words in target_words:
            a, b = _words(rec, words)
            s, e = chain.cur(a, b)
            t, st = _f0(fr, s, e)
            target = np.interp((t - s / C.SR) / ((e - s) / C.SR), norm, template_st)
            errors.extend((st - target) ** 2)
        return float(np.sqrt(np.mean(errors)))
    def metric(y, fy, chain):
        return {"name": "template_contour_rmse_change", "value": error(fy, chain) - error(rec.fr, Chain()), "unit": "st",
                "after_rmse_st": error(fy, chain)}
    words = (min(w[0] for w in target_words), max(w[1] for w in target_words))
    return _finish(build, "REPEATED_CONTOUR", level, p, words, metric,
                   approximation={"method": "linear time-normalised voiced F0; interpolation across unvoiced template gaps",
                                  "pitch_measurement_grid_s": C.HOP_S},
                   details={"template_sentence": template_sentence, "target_sentences": targets})
