"""Fix your speech: apply the fix of each finding to the participant's own recording, then re-score the edited audio.

Each finding of a result (pipeline.analyze) states the participant's value and the target value of one measure (the
reference rendition carried to the speaker's own overall tempo, pitch range or level). An edit from the project's own
tool set (flaws.py: WSOLA time scaling, Praat PSOLA pitch, room-tone pauses, gain) moves the measure to the target, and
a Chain of Warps maps the original samples to the edited samples. `verify` analyses the edited audio again with the
settings of the original result and runs three checks: a reproduction check (the unedited audio and the chain with null
parameters must give the original result again; every null operation is an identity by construction, so this check
controls determinism and settings, not processing artefacts), a second pitch tracker for pitch edits, and the word
alignment of the edited audio against the time map. The detector that sets the targets also judges the result, so a
removed flag shows detector consistency, not a perceived improvement.

The caps are chosen limits, extrapolated from whole-utterance listening tests: Praat PSOLA loses about 0.2-0.4 MOS at
x1.5 duration or +-3 st and 1.1-1.4 MOS at x2 (Choi et al. 2021, NANSY, Tables 6-7). No listening test of local
word-level edits was found.
"""
from __future__ import annotations

import dataclasses
import math
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from . import audio
from . import config as C
from . import flaws
from .align import Alignment, Transcript, acoustic_pauses, parse_transcript
from .features import Frames, frame_features, frame_slice, pitch_track, stress_reference, word_regions, word_stats, windows

SR = C.SR

# Duration factors (> 1 slower). Slowing costs more quality than speeding (Rudresh et al. 2018; Roberts & Paliwal 2020).
MAX_SLOW_FACTOR = 1.4  # one round
MIN_FAST_FACTOR = 0.7  # one round
HARD_SLOW_FACTOR = 1.5  # all rounds together on one word
HARD_FAST_FACTOR = MIN_FAST_FACTOR
UNVOICED_STRETCH_LIMIT = 2.0  # Charpentier & Moulines 1989: slowing unvoiced speech by >= 2 gives tonal noise
# Pitch: the excursion scale around the region median, and the change of each frame.
MAX_PITCH_SCALE = 1.5  # all rounds together; 1 / MAX_PITCH_SCALE for compression
MAX_FRAME_ST = 3.0  # one round; speaker identity holds up to 3 st (Bae & Joo 2022)
HARD_FRAME_ST = 4.0  # all rounds together
MIN_AUDIBLE_ST = 1.5  # pitch-distance JND 1.5-2 st ('t Hart; docs/PAPERS.md #40): a smaller range change is not heard
# Level: smooth gain. The level JND (1.5 dB, docs/PAPERS.md #66) is a lower limit of audibility; the 6 dB cap has no
# quality source. Gain does not restore vocal effort, which changes spectral tilt and F0 (docs/PAPERS.md #69).
MAX_GAIN_DB = 6.0  # all rounds together
MAX_PEAK = 0.98  # full scale = 1; a gain stops before the region clips
GAIN_RAMP_S = 0.05
MAX_PAUSE_INSERT_S = 2.0  # all rounds together at one boundary
MAX_EMPHASIS_FACTOR = MAX_SLOW_FACTOR
MAX_EMPHASIS_ST = MAX_FRAME_ST
MAX_EMPHASIS_DB = MAX_GAIN_DB
CONTOUR_MIN_FRAMES = C.D3_MIN_VOICED_FRAMES
# PSOLA splice: a tier point that changes by less than 1 cent keeps the original audio; around a changed point the
# splice covers one tier step (linear tier interpolation) plus one period at the PSOLA F0 floor (the OLA window).
PITCH_SPLICE_MIN_ST = 0.01
PITCH_SPLICE_PAD_S = C.PSOLA_STEP_S + 1 / C.PSOLA_F0[0]
MAX_ROUNDS = 3

NULL_CHAIN_TOLERANCE = 0.5  # index points: the null-parameter chain of the reproduction check must not move the score more than this
TRACKER_TOLERANCE_LN = math.log(1.25)  # two pitch trackers agree when their range changes differ by less than a factor 1.25
BOUNDARY_TOLERANCE_S = 2 * C.CTC_FRAME_S  # the aligner resolves word edges to one CTC frame on each side

# Patterns that name a disfluency (inserted, repeated or held sounds): their fix removes speech, not a delivery setting.
DISFLUENCY_PATTERNS = {"WORD_REPETITION", "SOUND_REPETITION", "FILLED_PAUSE", "BLOCK", "ONSET_PROLONGATION",
                       "RHYME_PROLONGATION", "LOW_EFFORT"}
UNFIXABLE_REASON = {
    "D6": "Clarity is measured from how fast the spectrum changes during articulation. No edit of the recording "
          "can restore articulation that was not spoken; record these words again.",
    "D8": "The ending measure is listed, not scored, and this tool has no validated edit for a sentence ending.",
    "D7_whole": "Uneven word timing has no single inverse edit: each word would need its own time scale.",
    "disfluency": "The finding names an inserted, repeated or held sound, or a change of voice quality. Its fix "
                  "removes or re-voices speech, which is not a delivery setting that an edit can change.",
}
APPLIED, CAPPED, COVERED, SKIPPED, UNFIXABLE = "applied", "capped", "covered", "skipped", "unfixable"
# Fix.cause: why a fix stopped short (capped) or was skipped.
CAP, HEADROOM, FLAT_PITCH, INAUDIBLE, SHARED_CAP = "cap", "headroom", "flat_pitch", "inaudible", "shared_cap"
TIME_KINDS = ("stretch", "emphasis")
PITCH_KINDS = ("pitch_scale", "pitch_contour")


# ============================================================================================ records
@dataclass(frozen=True)
class Operation:
    """One edit in original sample coordinates. kind and value: 'stretch' duration factor (> 1 slower); 'pause_insert'
    seconds of room tone at sample `start` (== end); 'pause_shorten' seconds kept of the silent run [start, end);
    'pitch_scale' factor on the semitone excursions around the region median; 'pitch_contour' weight of the reference
    contour (1 = full); 'emphasis' (duration factor, semitones, dB); 'gain' dB. words: first and last word of the
    finding; measure: (participant, target) of the finding; limit_st: largest F0 change of one frame; round: 1 for the
    first fix of the recording."""
    kind: str
    start: int
    end: int
    value: float | tuple[float, float, float]
    finding: str
    whole_clip: bool = False
    contour: tuple[np.ndarray, np.ndarray] | None = None  # (original times s, zero-centred target st) for 'pitch_contour'
    words: tuple[int, int] | None = None
    measure: tuple[float, float] | None = None
    limit_st: float = MAX_FRAME_ST
    round: int = 1

    def scaled(self, strength: float) -> Operation:
        """The same operation at a fraction of its change: 0 changes nothing (the null chain), 1 is the planned edit. Factors
        scale in the log domain, seconds, semitones and dB linearly."""
        value = self.value
        if self.kind in ("stretch", "pitch_scale"):
            value = value ** strength
        elif self.kind in ("pause_insert", "pitch_contour", "gain"):
            value = value * strength
        elif self.kind == "pause_shorten":
            run = (self.end - self.start) / SR
            value = run - strength * (run - value)
        elif self.kind == "emphasis":
            value = (value[0] ** strength, value[1] * strength, value[2] * strength)
        return dataclasses.replace(self, value=value)

    def null(self) -> Operation:
        """The same operation with parameters that change nothing (the reproduction check)."""
        return self.scaled(0.0)


@dataclass(frozen=True)
class Fix:
    """What happened to one finding. status: applied, capped (a partial fix at the cap; `reason` says why), covered
    (charged to another finding of its group and fixed with it), skipped (the allowed change is too small to hear, or
    other fixes use the whole allowed change), unfixable. wanted / applied: the operation value that reaches the target
    and the value used. share: the part of the wanted change that was applied (factors in the log domain), 1 for a full
    fix. round: the fix round (1 = first). cause: CAP or HEADROOM for a capped fix; FLAT_PITCH, INAUDIBLE or SHARED_CAP
    for a skipped one; "" otherwise."""
    finding: str
    dimension: str
    type: str
    status: str
    operation: str | None
    wanted: float | tuple | None
    applied: float | tuple | None
    reason: str = ""
    share: float | None = None
    round: int = 1
    cause: str = ""

    @property
    def partial(self) -> bool:
        return self.status == CAPPED


# ============================================================================================ the speaker's own measures
@dataclass
class Speaker:
    """The participant recording with the word times of the result and its own frame features."""
    wav: np.ndarray
    start: np.ndarray  # s, aligned word starts
    end: np.ndarray
    frames: Frames
    pause_spans: np.ndarray  # (n - 1, 2) s, acoustic pause after word i (NaN where none)
    regions: np.ndarray  # word supports (s), as the pipeline measures words
    syllables: tuple[int, ...]
    sentence: tuple[int, ...]

    def samples(self, seconds: float) -> int:
        return int(round(seconds * SR))

    def word_span(self, first: int, last: int) -> tuple[int, int]:
        return self.samples(self.start[first]), self.samples(self.end[last])

    def pauses(self) -> list[tuple[int, int]]:
        return [(self.samples(begin), self.samples(finish)) for begin, finish in self.pause_spans if np.isfinite(begin)]


@dataclass
class FixOutcome:
    """audio: edited samples (16 kHz, int16 grid); time_map: original samples -> edited samples; speaker (the original
    recording and its measures) and operations let `verify` run the null chain. used: the value each operation used;
    peak_st: the largest F0 change of a frame per operation (0 for an operation without a pitch change)."""
    audio: np.ndarray
    fixes: list[Fix]
    time_map: flaws.Chain
    speaker: Speaker
    operations: list[Operation]
    used: list = dataclasses.field(default_factory=list)
    peak_st: list[float] = dataclasses.field(default_factory=list)

    @property
    def source(self) -> np.ndarray:
        return self.speaker.wav

    @property
    def rounds(self) -> int:
        return max((fx.round for fx in self.fixes), default=1)

    def to_edited(self, seconds, side: str = "left") -> np.ndarray:
        """Original times (s) -> edited times (s). side 'right' for interval starts, 'left' for interval ends."""
        return np.asarray(self.time_map(np.asarray(seconds, float) * SR, side)) / SR


def load(participant) -> np.ndarray:
    if isinstance(participant, np.ndarray):
        return participant
    try:
        return audio.read_wav(Path(participant))
    except audio.AudioError:
        return audio.load_audio(Path(participant), C.MAX_UPLOAD_BYTES, C.MAX_UPLOAD_S)[0]


def words_transcript(result: dict, transcript=None) -> Transcript:
    """The transcript of the result's words. The result keeps the words without punctuation, so the sentence index of
    each word comes from `transcript` (text or Transcript) when it is given; without it all words form one sentence."""
    words = result["words"]
    if transcript is not None:
        tr = transcript if isinstance(transcript, Transcript) else parse_transcript(transcript, strict=False)
        if len(tr) == len(words):
            return tr
    tr = parse_transcript(" ".join(w["w"] for w in words))
    if len(tr) != len(words):
        raise ValueError(f"the result words parse to {len(tr)} words, not {len(words)}")
    return tr


def speaker(result: dict, wav: np.ndarray, transcript=None) -> Speaker:
    words = result["words"]
    start = np.array([w["p"][0] for w in words], float)
    end = np.array([w["p"][1] for w in words], float)
    al = Alignment(start, end, np.ones(len(words)), 1.0)
    fr = frame_features(wav)
    tr = words_transcript(result, transcript)
    return Speaker(wav, start, end, fr, acoustic_pauses(al, fr.L, fr.voiced)[1], word_regions(al), tr.syll, tr.sentence)


# ============================================================================================ planning
@dataclass(frozen=True)
class Budget:
    """What other operations already change on the words of a finding: the largest and smallest duration factor of a
    word, the largest and smallest excursion scale, the largest and smallest gain (dB), the largest F0 change of a frame
    (st) and the pause time added at the boundary (s)."""
    time_max: float = 1.0
    time_min: float = 1.0
    scale_max: float = 1.0
    scale_min: float = 1.0
    gain_max: float = 0.0
    gain_min: float = 0.0
    peak_st: float = 0.0
    pause_s: float = 0.0


class Ledger:
    """The change of every word (duration factor, excursion scale, gain, largest frame change) and of every boundary
    (pause added) that the operations entered so far make; the caps of a new operation leave room for them."""

    def __init__(self, n_words: int) -> None:
        self.time, self.scale = np.ones(n_words), np.ones(n_words)
        self.gain, self.peak, self.pause = np.zeros(n_words), np.zeros(n_words), np.zeros(n_words)

    def add(self, op: Operation, used, peak_st: float) -> None:
        first, last = op.words
        words = slice(first, last + 1)
        if op.kind == "stretch":
            self.time[words] *= used
        elif op.kind == "emphasis":
            self.time[words] *= used[0]
            self.gain[words] += used[2]
        elif op.kind == "pitch_scale":
            self.scale[words] *= used
        elif op.kind == "gain":
            self.gain[words] += used
        elif op.kind == "pause_insert":
            self.pause[first] += used
        self.peak[words] = np.maximum(self.peak[words], peak_st)

    def span(self, first: int, last: int) -> Budget:
        words = slice(first, last + 1)
        return Budget(float(self.time[words].max()), float(self.time[words].min()), float(self.scale[words].max()),
                      float(self.scale[words].min()), float(self.gain[words].max()), float(self.gain[words].min()),
                      float(self.peak[words].max()), float(self.pause[first]))


def ledger_of(prior: FixOutcome | None, n_words: int) -> Ledger:
    """The ledger of the earlier rounds (the values and frame changes they used)."""
    ledger = Ledger(n_words)
    if prior is not None:
        for op, used, peak in zip(prior.operations, prior.used, prior.peak_st):
            ledger.add(op, used, peak)
    return ledger


def is_whole_clip(f: dict) -> bool:
    return f.get("context") == "whole passage"


def finding_words(f: dict, sp: Speaker) -> tuple[int, int]:
    return (0, len(sp.start) - 1) if is_whole_clip(f) else (f["words"][0], f["words"][1])


def clamp(value: float, low: float, high: float) -> tuple[float, bool]:
    clamped = min(max(value, low), high)
    return clamped, clamped != value


def log_share(wanted: float, applied: float) -> float:
    return 1.0 if wanted == applied or math.log(wanted) == 0 else round(math.log(applied) / math.log(wanted), 3)


def linear_share(wanted: float, applied: float) -> float:
    return 1.0 if wanted == applied or wanted == 0 else round(applied / wanted, 3)


def capped_fix(f: dict, kind: str, wanted, applied, capped: bool, cap_text: str, wanted_text: str, share: float) -> Fix:
    if capped:
        return Fix(f["id"], f["dimension"], f["type"], CAPPED, kind, wanted, applied,
                   f"partial fix: capped at {cap_text} where the full fix needs {wanted_text} ({share:.0%} of the "
                   "change); a larger change could sound processed, so the finding can remain", share, cause=CAP)
    return Fix(f["id"], f["dimension"], f["type"], APPLIED, kind, wanted, applied, share=1.0)


def unfixable(f: dict, key: str) -> tuple[None, Fix]:
    return None, Fix(f["id"], f["dimension"], f["type"], UNFIXABLE, None, None, None, UNFIXABLE_REASON[key])


def time_limits(spent: Budget) -> tuple[float, float]:
    """Duration-factor range of one operation: the per-operation caps, narrowed so that every word stays inside the hard
    caps; the range always holds 1 (no change), so a used-up cap never reverses the direction of a fix."""
    return (min(1.0, max(MIN_FAST_FACTOR, HARD_FAST_FACTOR / spent.time_min)),
            max(1.0, min(MAX_SLOW_FACTOR, HARD_SLOW_FACTOR / spent.time_max)))


def gain_limits(spent: Budget) -> tuple[float, float]:
    return min(0.0, -MAX_GAIN_DB - spent.gain_min), max(0.0, MAX_GAIN_DB - spent.gain_max)


def frame_limit(spent: Budget) -> float:
    return max(0.0, min(MAX_FRAME_ST, HARD_FRAME_ST - spent.peak_st))


def plan_time(f: dict, sp: Speaker, spent: Budget) -> tuple[Operation, Fix]:
    """Pace / speech tempo / word time (ln ratio of participant to target): scale the speech of the words to the target
    time; pauses inside the span keep their length."""
    wanted = math.exp(-f["delta"])
    factor, capped = clamp(wanted, *time_limits(spent))
    words = finding_words(f, sp)
    op = Operation("stretch", *sp.word_span(*words), factor, f["id"], is_whole_clip(f), words=words,
                   measure=(f["participant"], f["baseline"]))
    return op, capped_fix(f, op.kind, wanted, factor, capped, f"x{factor:.2f} duration", f"x{wanted:.2f}",
                          log_share(wanted, factor))


def quietest_point(sp: Speaker, left: int) -> int:
    """Sample of the lowest-level frame in the aligned gap after word `left`; the gap midpoint when the gap is shorter
    than one frame. The search stays inside the gap so that the room tone never splits a word onset."""
    lo, hi = sp.end[left], sp.start[left + 1]
    if hi - lo < C.HOP_S:
        return sp.samples(0.5 * (lo + hi))
    sl = frame_slice(lo, hi, len(sp.frames))
    return int(round((sl.start + int(np.argmin(sp.frames.L[sl]))) * C.HOP))


def plan_pause(f: dict, sp: Speaker, spent: Budget) -> tuple[Operation | None, Fix]:
    """Pause (s, participant minus target): add room tone at the boundary, or shorten the silent run to the target."""
    left = f["words"][0]
    words = (left, left + 1)
    if f["delta"] < 0:
        wanted = -f["delta"]
        seconds, capped = clamp(wanted, 0.0, max(0.0, MAX_PAUSE_INSERT_S - spent.pause_s))
        point = quietest_point(sp, left)
        op = Operation("pause_insert", point, point, seconds, f["id"], words=words, measure=(f["participant"], f["baseline"]))
        return op, capped_fix(f, op.kind, wanted, seconds, capped, f"{seconds:.2f} s", f"{wanted:.2f} s",
                              linear_share(wanted, seconds))
    run_start, run_end = sp.pause_spans[left]
    if not np.isfinite(run_start):
        return None, Fix(f["id"], f["dimension"], f["type"], UNFIXABLE, "pause_shorten", None, None,
                         "no silent run was found at this boundary in the recording")
    keep = max(f["baseline"], C.PAUSE_FLOOR_S)
    op = Operation("pause_shorten", sp.samples(run_start), sp.samples(run_end), keep, f["id"], words=words,
                   measure=(f["participant"], f["baseline"]))
    return op, capped_fix(f, op.kind, keep, keep, False, "", "", 1.0)


def reference_contour(result: dict, sp: Speaker, first: int, last: int, target_range: float) -> tuple[np.ndarray, np.ndarray] | None:
    """The reference pitch row of the result (st, on the participant's time axis through the word map) over the words,
    zero-centred and scaled so that its window pitch range equals the target. None without enough reference frames."""
    row = next((r for r in result.get("rows", []) if r.get("key") == "pitch"), None)
    if row is None or not row.get("b"):
        return None
    values = np.array([np.nan if v is None else v for v in row["b"]], float)
    times = np.arange(len(values)) * result.get("hop", C.HOP_S)
    inside = (times >= sp.regions[first, 0]) & (times < sp.regions[last, 1]) & np.isfinite(values)
    if inside.sum() < CONTOUR_MIN_FRAMES:
        return None
    measured = median_window_range(values, sp, first, last)
    if not np.isfinite(measured) or measured <= 0:
        return None
    centred = (values[inside] - np.median(values[inside])) * target_range / measured
    return times[inside], centred


def inaudible(f: dict, kind: str, wanted, change_st: float, limit_st: float, flat: bool = False) -> tuple[None, Fix]:
    """flat: the speaker's own range is so small that the largest allowed excursion scale cannot reach MIN_AUDIBLE_ST."""
    if flat:
        why = (f"the pitch range here is only {f['participant']:.1f} st, so even the largest allowed excursion scale "
               f"(x{MAX_PITCH_SCALE}) changes it by less than")
    else:
        why = (f"the allowed edit changes the pitch range by about {change_st:.1f} st (frame change at most {limit_st:.1f} st), "
               "below")
    return None, Fix(f["id"], f["dimension"], f["type"], SKIPPED, kind, wanted, None,
                     f"skipped: {why} the {MIN_AUDIBLE_ST} st that listeners can hear", 0.0, cause=FLAT_PITCH if flat else INAUDIBLE)


def plan_pitch(f: dict, sp: Speaker, result: dict, method: str, spent: Budget) -> tuple[Operation | None, Fix]:
    """Pitch range (st, participant and target window ranges). 'own': scale the speaker's own excursions around their
    median in the region; 'contour': lay the reference contour onto the words at the target range. The predicted change
    of the range (st) must reach MIN_AUDIBLE_ST; a frame changes by at most limit_st."""
    words = finding_words(f, sp)
    span = sp.word_span(*words)
    limit = frame_limit(spent)
    measure = (f["participant"], f["baseline"])
    if method == "contour":
        change = min(abs(f["baseline"] - f["participant"]), 2 * limit)
        if change < MIN_AUDIBLE_ST:
            return inaudible(f, "pitch_contour", 1.0, change, limit)
        contour = reference_contour(result, sp, *words, f["baseline"])
        if contour is None:
            return None, Fix(f["id"], f["dimension"], f["type"], UNFIXABLE, "pitch_contour", None, None,
                             "the result has too few reference pitch frames over these words for a contour")
        op = Operation("pitch_contour", *span, 1.0, f["id"], is_whole_clip(f), contour, words, measure, limit)
        return op, capped_fix(f, op.kind, 1.0, 1.0, False, "", "", 1.0)
    wanted = f["baseline"] / max(f["participant"], 1e-3)
    scale, capped = clamp(wanted, min(1.0, 1 / (MAX_PITCH_SCALE * spent.scale_min)), max(1.0, MAX_PITCH_SCALE / spent.scale_max))
    change = min(f["participant"] * abs(scale - 1), 2 * limit)
    if change < MIN_AUDIBLE_ST:
        flat = wanted > 1 and f["participant"] * (MAX_PITCH_SCALE - 1) < MIN_AUDIBLE_ST
        return inaudible(f, "pitch_scale", wanted, change, limit, flat)
    op = Operation("pitch_scale", *span, scale, f["id"], is_whole_clip(f), None, words, measure, limit)
    return op, capped_fix(f, op.kind, wanted, scale, capped, f"x{scale:.2f} pitch excursion", f"x{wanted:.2f}",
                          log_share(wanted, scale))


def plan_emphasis(f: dict, sp: Speaker, spent: Budget) -> tuple[Operation, Fix]:
    """Emphasis (stress points: the mean of three robust z-scores, ln duration per syllable, P90 pitch, P90 level). Each
    component rises by the missing points times the speaker's own scale of that component. The result's points use the
    reference's scales; in the same-speaker regime (R1) the two scales are close. Known limit: with another speaker's
    reference (R2) the scales can differ, so the edit size is checked only in R1."""
    word = f["words"][0]
    sigma = stress_reference(word_stats(sp.frames, sp.regions, sp.syllables).u)[1]
    points = f["baseline"] - f["participant"]
    wanted = (math.exp(points * sigma[0]), points * sigma[1], points * sigma[2])
    factor, capped_factor = clamp(wanted[0], 1.0, min(MAX_EMPHASIS_FACTOR, time_limits(spent)[1]))
    semitones, capped_st = clamp(wanted[1], 0.0, min(MAX_EMPHASIS_ST, frame_limit(spent)))
    gain, capped_db = clamp(wanted[2], 0.0, min(MAX_EMPHASIS_DB, gain_limits(spent)[1]))
    applied = (factor, semitones, gain)
    op = Operation("emphasis", *sp.word_span(word, word), applied, f["id"], words=(word, word),
                   measure=(f["participant"], f["baseline"]), limit_st=semitones)
    share = min(log_share(wanted[0], factor), linear_share(wanted[1], semitones), linear_share(wanted[2], gain))
    return op, capped_fix(f, op.kind, wanted, applied, capped_factor or capped_st or capped_db,
                          f"x{factor:.2f} duration, {semitones:.1f} st, {gain:.1f} dB",
                          f"x{wanted[0]:.2f}, {wanted[1]:.1f} st, {wanted[2]:.1f} dB", share)


def plan_gain(f: dict, sp: Speaker, spent: Budget) -> tuple[Operation, Fix]:
    """Volume (dB re the speaker's own median voiced level): gain over the words."""
    wanted = -f["delta"]
    gain, capped = clamp(wanted, *gain_limits(spent))
    words = (f["words"][0], f["words"][1])
    op = Operation("gain", *sp.word_span(*words), gain, f["id"], words=words, measure=(f["participant"], f["baseline"]))
    return op, capped_fix(f, op.kind, wanted, gain, capped, f"{gain:+.1f} dB", f"{wanted:+.1f} dB", linear_share(wanted, gain))


def plan(f: dict, sp: Speaker, result: dict, pitch_method: str = "own", ledger: Ledger | None = None) -> tuple[Operation | None, Fix]:
    """The operation and the fix record of one finding; ledger: the changes of the other operations (earlier rounds and
    the operations planned before this one), which count against the caps."""
    dim = f["dimension"]
    if f.get("pattern") in DISFLUENCY_PATTERNS:
        return unfixable(f, "disfluency")
    if dim in ("D6", "D8"):
        return unfixable(f, dim)
    if dim == "D7" and is_whole_clip(f):
        return unfixable(f, "D7_whole")
    spent = (ledger or Ledger(len(sp.start))).span(*finding_words(f, sp))
    if dim in ("D1", "D7", "D9"):
        op, fix = plan_time(f, sp, spent)
    elif dim == "D2":
        op, fix = plan_pause(f, sp, spent)
    elif dim == "D3":
        op, fix = plan_pitch(f, sp, result, pitch_method, spent)
    elif dim == "D4":
        op, fix = plan_emphasis(f, sp, spent)
    elif dim == "D5":
        op, fix = plan_gain(f, sp, spent)
    else:
        raise ValueError(f"no repair rule for dimension {dim}")
    if op is not None and op.null().value == op.value:
        return None, dataclasses.replace(fix, status=SKIPPED, applied=None, share=0.0, cause=SHARED_CAP, reason=(
            "skipped: other fixes of these words already use the whole allowed change"))
    return op, fix


# Dimensions whose measure each operation moves. A group member is fixed with its owner only when the owner's operation
# moves the member's measure: compressing speech cannot lengthen a dropped pause.
MOVES = {"stretch": {"D1", "D7", "D9"}, "pause_insert": {"D1", "D2"}, "pause_shorten": {"D1", "D2"}, "gain": {"D4", "D5"},
         "pitch_scale": {"D3"}, "pitch_contour": {"D3"}, "emphasis": {"D4"}}


def group_owner(f: dict, by_id: dict[str, dict], kinds: dict[str, str]) -> str | None:
    """The counted member of f's group that carries f's penalty (one change, one penalty) and whose operation (kinds:
    finding id -> operation kind) moves f's measure; None when f is counted or no such member exists."""
    if f.get("counted", True) or not f.get("group"):
        return None
    return next((g for g in f["group"] if g != f["id"] and by_id[g].get("counted", True) and f["dimension"] in MOVES.get(kinds.get(g), ())),
                None)


# ============================================================================================ edits
def limit_change(f0: np.ndarray, new_f0: np.ndarray, limit_st: float, stats: dict) -> np.ndarray:
    """Clip the F0 change of each frame to +-limit_st; stats gets the largest change used and the share of changed
    frames that the limit clipped."""
    change = 12 * np.log2(new_f0 / f0)
    clipped = np.clip(change, -limit_st, limit_st)
    moved = np.abs(change) > 1e-6
    stats["peak_st"] = max(stats.get("peak_st", 0.0), float(np.abs(clipped).max(initial=0.0)))
    stats["clipped"] = float((np.abs(change[moved]) > limit_st + 1e-9).mean()) if moved.any() else 0.0
    return f0 * 2 ** (clipped / 12)


def scale_pitch_fn(start: int, end: int, scale: float, ramp: float, limit_st: float = MAX_FRAME_ST, stats: dict | None = None):
    """st' = c + (st - c) * (1 + (scale - 1) * w(t)), c the median st of the region: the speaker's own melody, wider or
    narrower around their own centre."""
    stats = {} if stats is None else stats

    def fn(times, f0, med):
        semitones = 12 * np.log2(f0 / med)
        inside = (times >= start / SR) & (times <= end / SR)
        centre = float(np.median(semitones[inside])) if inside.any() else 0.0
        weight = flaws._ramp_window(times, start / SR, end / SR, ramp)
        return limit_change(f0, med * 2 ** ((centre + (semitones - centre) * (1 + (scale - 1) * weight)) / 12), limit_st, stats)
    return fn


def contour_pitch_fn(start: int, end: int, weight: float, times_now: np.ndarray, target: np.ndarray, ramp: float,
                     limit_st: float = MAX_FRAME_ST, stats: dict | None = None):
    """Blend toward the zero-centred target contour placed at the speaker's own median of the region."""
    stats = {} if stats is None else stats

    def fn(times, f0, med):
        semitones = 12 * np.log2(f0 / med)
        inside = (times >= start / SR) & (times <= end / SR)
        centre = float(np.median(semitones[inside])) if inside.any() else 0.0
        blend = weight * flaws._ramp_window(times, start / SR, end / SR, ramp)
        goal = centre + np.interp(times, times_now, target)
        return limit_change(f0, med * 2 ** (((1 - blend) * semitones + blend * goal) / 12), limit_st, stats)
    return fn


def shift_pitch_fn(start: int, end: int, semitones: float, ramp: float):
    def fn(times, f0, med):
        return f0 * 2 ** (semitones * flaws._ramp_window(times, start / SR, end / SR, ramp) / 12)
    return fn


def changed_spans(times: np.ndarray, change_st: np.ndarray, start: int, end: int) -> list[tuple[int, int]]:
    """Sample spans inside [start, end) that cover the pitch-tier points whose F0 changes, merged where two splice
    fades would overlap."""
    pad = int(round(PITCH_SPLICE_PAD_S * SR))
    fade = int(round(C.SPLICE_FADE_S * SR))
    spans: list[tuple[int, int]] = []
    for centre in np.round(np.sort(times[np.abs(change_st) > PITCH_SPLICE_MIN_ST]) * SR).astype(int):
        begin, finish = max(start, centre - pad), min(end, centre + pad)
        if finish <= begin:
            continue
        if spans and begin - spans[-1][1] < 2 * fade:
            spans[-1] = (spans[-1][0], finish)
        else:
            spans.append((begin, finish))
    return spans


def resynthesise(x: np.ndarray, start: int, end: int, pitch_fn) -> np.ndarray:
    """Whole-clip PSOLA with a new pitch tier, spliced back over [start, end) only around the tier points that change
    (length kept)."""
    # PSOLA with an unchanged tier still alters the waveform; over a whole clip that moves the clip pitch-range measure.
    tier = {}

    def recorded(times, f0, med):
        new_f0 = pitch_fn(times, f0, med)
        tier.update(times=np.asarray(times, float), change_st=12 * np.log2(new_f0 / f0))
        return new_f0
    y, _ = flaws.psola(x, pitch_fn=recorded)
    y = np.pad(y, (0, max(0, len(x) - len(y))))[:len(x)]
    out = x
    for begin, finish in changed_spans(tier["times"], tier["change_st"], start, end):
        out = flaws.splice_whole(out, y, begin, finish, finish)
    return out


def headroom_db(x: np.ndarray, start: int, end: int) -> float:
    peak = float(np.max(np.abs(x[start:end]))) if end > start else 0.0
    return math.inf if peak <= 0 else 20 * math.log10(MAX_PEAK / peak)


def apply_gain(x: np.ndarray, start: int, end: int, gain_db: float, ramp: float) -> tuple[np.ndarray, float]:
    """Gain with raised-cosine ramps inside [start, end); returns (audio, gain used), the gain kept below clipping."""
    gain_db = min(gain_db, headroom_db(x, start, end))
    if gain_db == 0:
        return x, 0.0
    t = np.arange(len(x)) / SR
    return x * 10 ** (gain_db * flaws._ramp_window(t, start / SR, end / SR, ramp) / 20), gain_db


@dataclass
class EditState:
    """The running edit: the time map so far, the insertion points (original samples) of the pauses it added, and the
    pitch statistics (largest frame change, clipped share) of each pitch operation."""
    sp: Speaker
    chain: flaws.Chain = dataclasses.field(default_factory=flaws.Chain)
    inserted: list[int] = dataclasses.field(default_factory=list)
    room_tone: object = None
    pitch: dict = dataclasses.field(default_factory=dict)

    def tone(self):
        if self.room_tone is None:
            self.room_tone = flaws.room_tone(SimpleNamespace(fr=self.sp.frames, wav=self.sp.wav))
        return self.room_tone

    def pauses(self) -> list[tuple[int, int]]:
        """Pauses in current samples: the recording's own and the added room tone, which a later stretch must not scale."""
        own = [self.chain.cur(begin, finish) for begin, finish in self.sp.pauses()]
        added = [(int(round(float(self.chain(point, "left")))), int(round(float(self.chain(point, "right"))))) for point in self.inserted]
        return own + added


def apply_one(x: np.ndarray, op: Operation, state: EditState, stats: dict) -> tuple[np.ndarray, object]:
    """Apply one operation to the current audio (coordinates through the state's chain, warps appended). Returns (audio,
    value used); stats gets the pitch statistics of a pitch edit."""
    chain = state.chain
    start, end = chain.cur(op.start, op.end)
    if op.kind == "stretch":
        x, warps, _ = flaws.stretch_speech(x, start, end, 1 / op.value, state.pauses())
        chain.warps += warps
        return x, op.value
    if op.kind == "pause_insert":
        n = int(round(op.value * SR))
        if n == 0:
            return x, 0.0
        x, warp = flaws.insert_pause(x, int(round(float(chain(op.start, "left")))), n, state.tone())
        chain.warps.append(warp)
        state.inserted.append(op.start)
        return x, op.value
    if op.kind == "pause_shorten":
        keep = int(round(op.value * SR))
        if end - start <= keep:
            return x, (end - start) / SR
        x, warp = flaws.remove_pause(x, start, end, keep)
        chain.warps.append(warp)
        return x, op.value
    if op.kind == "pitch_scale":
        return resynthesise(x, start, end, scale_pitch_fn(start, end, op.value, C.FLATTEN_RAMP_S, op.limit_st, stats)), op.value
    if op.kind == "pitch_contour":
        times_now = np.asarray(chain(op.contour[0] * SR, "left")) / SR
        fn = contour_pitch_fn(start, end, op.value, times_now, op.contour[1], C.FLATTEN_RAMP_S, op.limit_st, stats)
        return resynthesise(x, start, end, fn), op.value
    if op.kind == "emphasis":
        stats["peak_st"] = abs(op.value[1])
        return apply_emphasis(x, start, end, op.value, chain)
    if op.kind == "gain":
        return apply_gain(x, start, end, op.value, GAIN_RAMP_S)
    raise ValueError(f"unknown operation {op.kind}")


def apply_emphasis(x: np.ndarray, start: int, end: int, value: tuple, chain: flaws.Chain) -> tuple[np.ndarray, tuple]:
    """The inverse of flaws.deemphasis: raise the word's pitch, lengthen it, raise its level."""
    factor, semitones, gain = value
    if semitones != 0:
        x = resynthesise(x, start, end, shift_pitch_fn(start, end, semitones, C.DEEMPH_RAMP_S))
    x, warp, n_new = flaws.stretch_span(x, start, end, 1 / factor)
    chain.warps.append(warp)
    x, gain = apply_gain(x, start, start + n_new, gain, C.DEEMPH_RAMP_S)
    return x, (factor, semitones, gain)


def run_operations(sp: Speaker, ops: list[Operation]) -> tuple[np.ndarray, flaws.Chain, list, list[dict]]:
    """Local operations right to left (original start), whole-clip operations last: a local delta is relative to the
    speaker's own overall value, which the whole-clip operation then moves. Returns (audio on the int16 grid, chain,
    value used per operation, pitch statistics per operation; both in input order)."""
    x, state = sp.wav.copy(), EditState(sp)
    used, stats = [None] * len(ops), [{} for _ in ops]
    for k in sorted(range(len(ops)), key=lambda k: (ops[k].whole_clip, -ops[k].start, k)):
        x, used[k] = apply_one(x, ops[k], state, stats[k])
    return audio.quantize(x), state.chain, used, stats


def realised_fix(fix: Fix, used, stats: dict) -> Fix:
    """A gain stopped by the clipping limit, and a pitch edit whose frame change hit the limit, are partial fixes."""
    if fix.operation in PITCH_KINDS and stats.get("clipped", 0.0) > 0:
        share = fix.share if fix.share is not None else 1.0
        return dataclasses.replace(fix, status=CAPPED, reason=(
            f"partial fix: the pitch change of a frame is limited to {stats['limit_st']:.1f} st, which clipped "
            f"{stats['clipped']:.0%} of the changed frames; a larger change could sound processed"
            + (f"; {fix.reason}" if fix.reason else "")), share=round(share * (1 - stats["clipped"]), 3), cause=CAP)
    if fix.operation not in ("gain", "emphasis") or used == fix.applied:
        return fix
    wanted = fix.wanted if fix.operation == "gain" else fix.wanted[2]
    got = used if fix.operation == "gain" else used[2]
    return dataclasses.replace(fix, status=CAPPED, applied=used, share=min(1.0 if fix.share is None else fix.share, linear_share(wanted, got)), cause=HEADROOM,
                               reason=f"partial fix: capped at {got:+.1f} dB by the clipping limit; the region has no "
                                      "more headroom")


def inverse(chain: flaws.Chain) -> flaws.Chain:
    """Edited samples -> original samples. Inserted material maps to its insertion point."""
    back = flaws.Chain()
    back.warps = [flaws.Warp(w.dst, w.src) for w in reversed(chain.warps)]
    return back


def to_original(op: Operation, back: flaws.Chain) -> Operation:
    """An operation planned on edited audio, carried to original sample coordinates (for the null chain)."""
    start = int(round(float(back(op.start, "right"))))
    end = start if op.kind == "pause_insert" else int(round(float(back(op.end, "left"))))
    contour = None if op.contour is None else (np.asarray(back(op.contour[0] * SR, "left")) / SR, op.contour[1])
    return dataclasses.replace(op, start=start, end=end, contour=contour)


def repair(result: dict, participant, findings: list[dict], *, pitch_method: str = "own", grouped: bool = True,
           transcript=None, prior: FixOutcome | None = None) -> FixOutcome:
    """Fix `findings` of `result` on the participant recording. prior: the outcome of the earlier rounds; `result` is
    then the analysis of prior.audio, and the returned outcome covers all rounds (time map and operations relative to
    the original recording)."""
    if pitch_method not in ("own", "contour"):
        raise ValueError(f"pitch_method must be 'own' or 'contour', got {pitch_method!r}")
    sp = speaker(result, load(participant), transcript)
    first_pass = [(f, *plan(f, sp, result, pitch_method, ledger_of(prior, len(sp.start)))) for f in findings]
    by_id = {f["id"]: f for f in result["flaws"]}
    kinds = {f["id"]: op.kind for f, op, _ in first_pass if op is not None}
    this_round = 1 if prior is None else prior.rounds + 1
    ledger = ledger_of(prior, len(sp.start))
    ops, fixes = [], []
    for f, _, _ in first_pass:
        owner = group_owner(f, by_id, kinds) if grouped else None
        if owner is not None:
            fixes.append(Fix(f["id"], f["dimension"], f["type"], COVERED, None, None, None,
                             f"its penalty is charged to {owner}; the fix of {owner} covers it", round=this_round))
            continue
        op, fix = plan(f, sp, result, pitch_method, ledger)
        fixes.append(dataclasses.replace(fix, round=this_round))
        if op is not None:
            ops.append(dataclasses.replace(op, round=this_round))
            ledger.add(op, op.value, op.limit_st if op.kind in (*PITCH_KINDS, "emphasis") else 0.0)
    edited, chain, used, stats = run_operations(sp, ops)
    for op, st in zip(ops, stats):
        st["limit_st"] = op.limit_st
    by_finding = {op.finding: (u, st) for op, u, st in zip(ops, used, stats)}
    fixes = [realised_fix(fx, *by_finding[fx.finding]) if fx.finding in by_finding else fx for fx in fixes]
    peaks = [st.get("peak_st", 0.0) for st in stats]
    if prior is None:
        return FixOutcome(edited, fixes, chain, sp, ops, used, peaks)
    back = inverse(prior.time_map)
    total = flaws.Chain()
    total.warps = prior.time_map.warps + chain.warps
    return FixOutcome(edited, prior.fixes + fixes, total, prior.speaker, prior.operations + [to_original(op, back) for op in ops],
                      prior.used + used, prior.peak_st + peaks)


def fix_finding(result: dict, participant_wav, finding_index: int, *, pitch_method: str = "own", transcript=None) -> FixOutcome:
    """Apply the fix of one finding (result['flaws'][finding_index]) to the participant recording. transcript (text):
    gives the sentence of each word to the pitch windows; without it all words count as one sentence."""
    return repair(result, participant_wav, [result["flaws"][finding_index]], pitch_method=pitch_method, grouped=False,
                  transcript=transcript)


def fix_all(result: dict, participant_wav, *, pitch_method: str = "own", transcript=None, rounds: int = 1,
            analyze_kwargs: dict | None = None) -> FixOutcome:
    """Apply the fixes of all findings; a finding whose penalty its group charges to another finding is fixed with that one.
    rounds > 1: analyse the edited audio again (analyze_kwargs as for `verify`) and fix the findings that remain; the
    caps hold for all rounds together."""
    if not 1 <= rounds <= MAX_ROUNDS:
        raise ValueError(f"rounds must be 1 to {MAX_ROUNDS}, got {rounds}")
    if rounds > 1 and analyze_kwargs is None:
        raise ValueError("a second round needs analyze_kwargs to analyse the edited audio")
    transcript = transcript if transcript is not None else (analyze_kwargs or {}).get("transcript")
    outcome = repair(result, participant_wav, result["flaws"], pitch_method=pitch_method, transcript=transcript)
    for _ in range(rounds - 1):
        current = analyse(outcome.audio, result, analyze_kwargs)
        if not current["flaws"]:
            break
        outcome = repair(current, outcome.audio, current["flaws"], pitch_method=pitch_method, transcript=transcript,
                         prior=outcome)
    return outcome


# ============================================================================================ A/B/C listening
def listen_pairs(outcome: FixOutcome, context_s: float = 1.0) -> list[dict]:
    """Per operation: the finding's words in the original and in the edited audio (s), and the same spans widened by
    context_s on each side (clipped to the recordings), for an original / fixed / target player."""
    sp = outcome.speaker
    duration = (len(sp.wav) / SR, len(outcome.audio) / SR)
    out = []
    for op in outcome.operations:
        first, last = op.words if op.words is not None else (0, len(sp.start) - 1)
        region = (float(sp.start[first]), float(sp.end[last]))
        edited = (float(outcome.to_edited(region[0], "right")), float(outcome.to_edited(region[1], "left")))
        out.append({"finding": op.finding, "operation": op.kind, "round": op.round, "words": [first, last],
                    "original": [round(region[0], 3), round(region[1], 3)], "edited": [round(edited[0], 3), round(edited[1], 3)],
                    "original_context": [round(max(0.0, region[0] - context_s), 3), round(min(duration[0], region[1] + context_s), 3)],
                    "edited_context": [round(max(0.0, edited[0] - context_s), 3), round(min(duration[1], edited[1] + context_s), 3)]})
    return out


# ============================================================================================ verification
def analyse(x: np.ndarray, original_result: dict, analyze_kwargs: dict) -> dict:
    """pipeline.analyze with the settings of the original result (its regime unless analyze_kwargs names the same one)."""
    from .pipeline import analyze
    kwargs = {"regime": original_result["regime"], **analyze_kwargs}
    if kwargs["regime"] != original_result["regime"]:
        raise ValueError(f"regime {kwargs['regime']} differs from the original result's {original_result['regime']}")
    return analyze(x, **kwargs)


def null_chain_audio(outcome: FixOutcome) -> np.ndarray:
    """The same chain of operations with null parameters (stretch 1.0, gain 0 dB, pitch scale 1.0, no pause change): the
    audio of the reproduction check. Every null operation returns its input (the pitch splice covers no changed tier
    point), so the chain controls determinism, not processing artefacts."""
    return run_operations(outcome.speaker, [op.null() for op in outcome.operations])[0]


def direction(f: dict) -> int:
    return 1 if (f.get("delta") or 0) > 0 else -1


def same_finding(old: dict, new: dict) -> bool:
    """Same dimension and direction, and the same words within half a window (the peak of a windowed measure moves)."""
    if old["dimension"] != new["dimension"] or direction(old) != direction(new):
        return False
    if is_whole_clip(old) or is_whole_clip(new):
        return is_whole_clip(old) and is_whole_clip(new)
    slack = 0 if old["dimension"] in ("D2", "D4") else C.WINDOW_WORDS // 2
    return old["words"][0] - slack <= new["words"][1] and new["words"][0] - slack <= old["words"][1]


def finding_brief(f: dict) -> dict:
    return {k: f.get(k) for k in ("id", "dimension", "type", "words", "delta", "points_lost", "counted")}


def compare_findings(before: dict, after: dict) -> dict:
    removed = [f["id"] for f in before["flaws"] if not any(same_finding(f, g) for g in after["flaws"])]
    remaining = [{"id": f["id"], "now": [finding_brief(g) for g in after["flaws"] if same_finding(f, g)]}
                 for f in before["flaws"] if f["id"] not in removed]
    new = [finding_brief(g) for g in after["flaws"] if not any(same_finding(f, g) for f in before["flaws"])]
    return {"score": after["scores"]["overall"], "removed": removed, "remaining": remaining, "new_findings": new}


def row_values(f: dict, result: dict) -> list[float] | None:
    """The values of f's measure in `result` over f's words (boundaries for pauses), in f's unit and sign convention
    (participant minus target); None when the result has no row of that dimension. The rows index words, so they hold for
    an edited recording of the same transcript."""
    from .pipeline import _ROWS
    row = next((r for r in result.get("rows", []) if r.get("key") == _ROWS[f["dimension"]][0]), None)
    if row is None:
        return None
    first, last = f["words"][0], f["words"][1] - (1 if f["dimension"] == "D2" else 0)
    return [v for v in row["p"][first:last + 1] if v is not None]


def residual(f: dict, after: dict) -> float | None:
    """The departure that remains of finding f in the re-analysis `after`, in f's unit and sign convention: for a local
    finding the value furthest in f's direction over its words, for a whole-passage one the delta of the same whole-passage
    finding or difference. None when no value is measured there (for a shortened pause: no pause above the detection
    floor). A value of the other sign is an overshoot."""
    if is_whole_clip(f):
        same = [g for g in [*after.get("flaws", []), *after.get("differences", [])] if is_whole_clip(g) and g["dimension"] == f["dimension"]]
        return None if not same or same[0].get("delta") is None else float(same[0]["delta"])
    values = row_values(f, after)
    if not values:
        return None
    sign = direction(f)
    return float(sign * max(sign * v for v in values))


def cc_semitones(x: np.ndarray) -> np.ndarray:
    """Praat cross-correlation F0 (a second tracker beside the pipeline's autocorrelation) on the 10 ms frame grid, st re
    1 Hz; NaN where unvoiced or no estimate lies within one frame."""
    import parselmouth
    pitch = parselmouth.Sound(np.ascontiguousarray(x, dtype=np.float64), sampling_frequency=SR).to_pitch_cc(
        time_step=C.HOP_S, pitch_floor=C.PSOLA_F0[0], pitch_ceiling=C.PSOLA_F0[1])
    times, f0 = np.asarray(pitch.xs(), float), np.asarray(pitch.selected_array["frequency"], float)
    return on_frame_grid(times, f0, len(x))


def on_frame_grid(times: np.ndarray, f0: np.ndarray, n_samples: int) -> np.ndarray:
    """F0 estimates (Hz, 0 = unvoiced) at `times` -> st re 1 Hz on the 10 ms frame grid; NaN where no voiced estimate
    lies within one frame."""
    grid = np.arange(1 + n_samples // C.HOP) * C.HOP_S
    nearest = np.clip(np.searchsorted(times, grid), 0, len(times) - 1)
    out = np.where((np.abs(times[nearest] - grid) <= C.HOP_S) & (f0[nearest] > 0), f0[nearest], np.nan)
    return 12 * np.log2(out)


def ac_semitones(x: np.ndarray) -> np.ndarray:
    f0 = pitch_track(x)[0]
    return np.where(f0 > 0, 12 * np.log2(np.where(f0 > 0, f0, 1.0)), np.nan)


def median_window_range(semitones: np.ndarray, sp: Speaker, first: int, last: int, regions: np.ndarray | None = None) -> float:
    """Median P90-P10 pitch range (st, NaN = unvoiced) of the pipeline's five-word windows that lie inside words
    first..last; of the windows centred on those words when none lies inside."""
    regions = sp.regions if regions is None else regions
    centred = [w for w in windows(SimpleNamespace(sentence=sp.sentence))[first:last + 1] if w is not None]
    inside = [w for w in centred if w[0] >= first and w[1] <= last]
    ranges = []
    for lo, hi in inside or centred:
        sl = frame_slice(regions[lo, 0], regions[hi, 1], len(semitones))
        values = semitones[sl][np.isfinite(semitones[sl])]
        if values.size >= C.D3_MIN_VOICED_FRAMES:
            ranges.append(np.percentile(values, 90) - np.percentile(values, 10))
    return float(np.median(ranges)) if ranges else float("nan")


def range_ln_ratio(before: float, after: float) -> float:
    """The pipeline's pitch-range comparison: ln of the ratio with RANGE_REG_ST added to each range."""
    return math.log((after + C.RANGE_REG_ST) / (before + C.RANGE_REG_ST))


def edited_regions(outcome: FixOutcome) -> np.ndarray:
    sp = outcome.speaker
    return np.column_stack([outcome.to_edited(sp.regions[:, 0], "right"), outcome.to_edited(sp.regions[:, 1], "left")])


def pitch_check(outcome: FixOutcome, trackers: dict | None = None) -> list[dict]:
    """For each pitch operation: window pitch range before and after with each tracker (name -> function audio -> st on
    the frame grid; default the pipeline's autocorrelation and Praat cross-correlation), and whether the range changes of
    all trackers agree."""
    ops = [op for op in outcome.operations if op.kind in PITCH_KINDS]
    if not ops:
        return []
    sp = outcome.speaker
    moved = edited_regions(outcome)
    trackers = trackers or {"autocorrelation": ac_semitones, "cross_correlation": cc_semitones}
    tracks = {name: (fn(sp.wav), fn(outcome.audio)) for name, fn in trackers.items()}
    out = []
    for op in ops:
        row = {"finding": op.finding, "round": op.round, "operation": op.kind, "participant_st": op.measure[0], "target_st": op.measure[1]}
        for name, (before, after) in tracks.items():
            r0 = median_window_range(before, sp, *op.words)
            r1 = median_window_range(after, sp, *op.words, moved)
            row[name] = {"before_st": round(r0, 3), "after_st": round(r1, 3), "change_st": round(r1 - r0, 3),
                         "ln_ratio": round(range_ln_ratio(r0, r1), 3)}
        ratios = [row[name]["ln_ratio"] for name in tracks]
        row["agree"] = bool(np.isfinite(ratios).all()) and max(ratios) - min(ratios) < TRACKER_TOLERANCE_LN
        out.append(row)
    return out


def alignment_check(outcome: FixOutcome, before: dict, after: dict) -> dict:
    """Original word times carried through the time map against the re-alignment of the edited audio."""
    start = np.array([w["p"][0] for w in before["words"]])
    end = np.array([w["p"][1] for w in before["words"]])
    mapped = np.column_stack([outcome.to_edited(start, "right"), outcome.to_edited(end, "left")])
    aligned = np.array([w["p"] for w in after["words"]], float)
    error = np.abs(mapped - aligned)
    middle = mapped.mean(axis=1)
    inside = (middle >= aligned[:, 0] - BOUNDARY_TOLERANCE_S) & (middle <= aligned[:, 1] + BOUNDARY_TOLERANCE_S)
    return {"words": len(start), "median_boundary_error_s": round(float(np.median(error)), 4),
            "max_boundary_error_s": round(float(error.max()), 4),
            "boundaries_within_tolerance": round(float((error <= BOUNDARY_TOLERANCE_S).mean()), 4),
            "word_middles_inside_aligned_word": round(float(inside.mean()), 4),
            "words_off": [int(i) for i in np.flatnonzero(~inside)], "tolerance_s": BOUNDARY_TOLERANCE_S}


def verify(outcome: FixOutcome, original_result: dict, analyze_kwargs: dict) -> dict:
    """Analyse the edited audio and the null chain with the settings of the original result. analyze_kwargs: the
    pipeline.analyze arguments other than the participant (transcript, baseline, detector, references, aligner, cache_dir,
    ...); the regime defaults to the original's. `reproduced` is False when the unedited audio does not give the original
    score again, i.e. the settings differ from the original analysis and the comparison is not valid. "null_chain" holds the
    re-analysis of the null chain (part of the reproduction check)."""
    before = analyse(outcome.source, original_result, analyze_kwargs)
    after = analyse(outcome.audio, original_result, analyze_kwargs)
    null_chain = analyse(null_chain_audio(outcome), original_result, analyze_kwargs)
    score0 = original_result["scores"]["overall"]
    null_part = compare_findings(original_result, null_chain)
    delta = None if null_chain["scores"]["overall"] is None or score0 is None else round(null_chain["scores"]["overall"] - score0, 2)
    return {
        "score_before": score0,
        "reproduced": before["scores"]["overall"] == score0 and len(before["flaws"]) == len(original_result["flaws"]),
        **compare_findings(original_result, after),
        "null_chain": {**null_part, "score_delta": delta, "within_tolerance": delta is not None and abs(delta) <= NULL_CHAIN_TOLERANCE},
        "pitch_check": pitch_check(outcome),
        "alignment": alignment_check(outcome, original_result, after),
        "fixes": [dataclasses.asdict(fx) for fx in outcome.fixes],
        "result": after,
    }
