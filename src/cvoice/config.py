"""Every numeric constant of the build contract (docs/DESIGN.md), in one place.

Evidence tags in the trailing comments follow DESIGN.md: (K) measured on a Kaggle CPU kernel during research,
(S) from a fetched source, (D) design value fixed before any evaluation run. Units are stated per constant.
`as_dict()` feeds the released detector hash. Dataset recipe metadata is versioned separately.
"""
from __future__ import annotations

import math

# --------------------------------------------------------------------------------------------- dimensions
DIMS = ("D1", "D2", "D3", "D4", "D5", "D6")
DIM_LABEL = {"D1": "Pace", "D2": "Pauses", "D3": "Pitch variation", "D4": "Emphasis", "D5": "Volume", "D6": "Clarity (spectral-change proxy)"}
DIM_BRIEF = {"D1": "Cadence", "D2": "Pauses", "D3": "Tone", "D4": "Tone", "D5": "Volume", "D6": "Clarity"}  # brief's words
DIM_UNIT = {"D1": "ln", "D2": "s", "D3": "ln", "D4": "p", "D5": "dB", "D6": "ln"}
REGIMES = ("R1", "R2")
REGIME_DIMS = {"R1": DIMS, "R2": ("D1", "D2", "D3", "D5")}  # D4, D6 are displayed, never flagged or scored in R2 (D)
FLAG_SIGNS = {"D1": (-1, 1), "D2": (-1, 1), "D3": (-1,), "D4": (-1,), "D5": (-1,), "D6": (-1,)}  # (D) see DESIGN 5.1
CLIP_DIMS = ("D1", "D3")  # dimensions with a whole-clip measure next to the local one: overall tempo, overall pitch range


def is_event(dim: str) -> bool:
    return UNIT_KIND[dim] != "window"


def dim_of(key: str) -> str:
    tokens = key.split()
    dim = tokens[0].rstrip("+-") if tokens else ''
    if dim not in UNIT_KIND:
        raise KeyError(key)
    return dim

# --------------------------------------------------------------------------------------------- audio ingest
SR = 16000  # Hz, canonical sample rate (K)
STEREO_SIDE_DB = 10.0  # dB; side energy above mid by more than this -> left channel only (anti-phase NARA transfers) (K)
MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # bytes (D)
MAX_UPLOAD_S = 180.0  # s (D)
DECODE_TIMEOUT_S = 60  # s, ffmpeg decode (D)
THREAD_ENV = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMBA_NUM_THREADS")  # set to "1" (K)
TORCH_THREADS = 2  # (K) in-process aligner (dashboard, tests, one-clip smoke)
POOL_WORKERS_PER_GPU = 2  # (D) pool workers per visible GPU: feature extraction (Praat F0, MFCC) is CPU work on the T4 x2 machine's 4 vCPUs
POOL_MAX_CPU_WORKERS = 4  # (D) CPU-only pool: min(this, cpu count) workers
POOL_TORCH_THREADS = 1  # (D) torch threads inside one pool worker
SEED = 42  # numpy / torch / Praat seed (K)

# --------------------------------------------------------------------------------------------- features (K)
WIN = 400  # samples, symmetric Hann window
HOP = 160  # samples, 10 ms
HOP_S = HOP / SR  # s
NFFT = 512
LEVEL_EPS = 1e-12  # inside the log of the frame level
MIN_VOICED_REF = 10  # voiced frames needed before the voiced median is the level reference
F0_PASS1 = (60.0, 700.0)  # Hz
F0_FLOOR_MIN, F0_FLOOR_Q25_FACTOR = 50.0, 0.75  # floor = max(50, 0.75 * Q25)
F0_CEIL_MAX, F0_CEIL_Q75_FACTOR = 800.0, 1.5  # ceiling = min(800, 1.5 * Q75)
F0_FALLBACK = (75.0, 600.0)  # Hz, when the first pass has fewer than F0_MIN_FIRST_PASS voiced frames (flagged)
F0_MIN_FIRST_PASS = 20
F0_MEDIAN_FRAMES = 5
PRAAT_AC = dict(max_number_of_candidates=15, very_accurate=False, silence_threshold=0.03, voicing_threshold=0.45,
                octave_cost=0.01, octave_jump_cost=0.35, voiced_unvoiced_cost=0.14)
N_MEL, MEL_FMIN, MEL_FMAX = 40, 50.0, 7600.0  # Hz
N_CEPS, DELTA_HALF_WIDTH, MEL_LOG_EPS = 13, 2, 1e-10  # c0..c12; delta over +-2 frames
MIN_VOICED_WORD = 5  # voiced frames for a word's pitch statistics
REGION_MAX_EXT_S, REGION_SHARE_BELOW_S = 0.05, 0.15  # s; word support from the raw CTC spike span (K)
STRESS_P_MIN = 0.75  # stress word iff p >= this and a local maximum over +-1 word
STRESS_SIGMA_FLOOR = (math.log(1.15), 3.0, 3.0)  # (ln duration per syllable, P90 semitones, P90 dB)
MAD_SCALE = 1.4826

# --------------------------------------------------------------------------------------------- alignment (K)
CTC_FRAME_S = 0.02  # s, wav2vec2 stride 320 samples
CTC_STRIDE = 320
CHUNK_S, CONTEXT_S = 30.0, 1.0  # s, emission chunk and context on each side
CHECKPOINT_NAME = "wav2vec2_fairseq_base_ls960_asr_ls960.pth"
CHECKPOINT_SHA256 = "488fd4f16de84438ffc945334278c1b9fb9b7159a806c1080b16111a958c945d"
CHECKPOINT_BYTES = 377_664_473
# No word-level gate: rushed speech drives word compatibility to ~0 while word times stay accurate (K, stretch probe:
# 6-18 ms boundary error); per-word compatibility is reported, never used to exclude a word (DESIGN 3).
LOW_COMPAT_NOTICE = 0.10  # (D) words below this are counted in a low-confidence notice, still scored
MEAN_COMPAT_MIN = 0.10  # (D) refusal "transcript does not match the audio", enforced only at trust boundaries (uploads, passage selection)
PAUSE_MIN_S = 0.20  # s, acoustic pause
PAUSE_FRAC, PAUSE_CLIP_DB = 0.3, (6.0, 15.0)  # theta = Q5(L) + clip(0.3 * (Q95 - Q5), 6, 15) dB
PAUSE_Q = (5, 95)
PAUSE_PEAK_Q, PAUSE_PEAK_DB = 99, 35.0  # (D) ... and never below Q99(L) - 35 dB: a recording with a gated or digital-silence floor
#   (Q5 at -120 dB) keeps breath noise in its pauses, which the floor rule alone counts as speech
PAUSE_BRIDGE_FRAMES = 2  # frames (20 ms): a shorter break inside a silent run does not split the pause

# --------------------------------------------------------------------------------------------- comparison (5.1)
WINDOW_WORDS, WINDOW_MIN_WORDS = 5, 3  # centred window clipped at sentence boundaries
D3_MIN_VOICED_FRAMES = 50
RANGE_REG_ST = 1.0  # (D) st added to both pitch ranges before their ratio, so that ranges below the discrimination limit of pitch
#   movements (1.5 to 2 st) do not produce large ratios
PAUSE_DROP_MIN_BASE_S = 0.5  # x < 0 counts only where the baseline pause is at least this

# --------------------------------------------------------------------------------------------- detector (5.2)
FLOORS = {"D1": math.log(1.10), "D2": 0.15, "D3": math.log(1.4), "D4": 0.5, "D5": 2.0, "D6": math.log(1.25)}  # (D) minimum scale;
#   D3: a 2 st narrowing of a 6 st window range, ln((6 + 1) / (4 + 1))
Q68 = 0.682689492  # quantile of |x| used as a scale
HYSTERESIS_LOW = 0.5  # regions extend over |z| >= h * this ...
REGION_PEAK_FRACTION = {"D1": 0.5, "D3": 0.0, "D5": 0.5, "D6": 0.5}  # (D) ... and over |z| >= this * the run's peak |z| (half-maximum
#   rule, DESIGN 5.2); the larger bound applies. A window mean (D1, D5, D6) responds in proportion to how much of the window an edit
#   covers, so half the peak marks the edit's edge. The pitch range (D3) collapses only once the window lies inside a flat stretch:
#   its response is already narrower than the stretch and is not trimmed.
MIN_REGION_WORDS = {"D1": 2, "D2": 1, "D3": 2, "D4": 1, "D5": 1, "D6": 1}
H_GRID = tuple(round(1.0 + 0.05 * i, 2) for i in range(221))  # 1.00:0.05:12.00
R1_H_RANGE = (1.0, 3.0)  # train supervised selection keeps one bounded common threshold
MIN_MEASUREMENT_COVERAGE = 0.50  # below this coverage, a dimension is scored only if it has a flag
DIFFERENCE_H, MAX_DIFFERENCES = 1.0, 5  # unscored R2 local differences, ranked by absolute z
FALSE_RATE_BUDGET = 0.50  # false regions per minute on the regime's train nulls
CLIP_LN = {"D1": math.log(1.25), "D3": math.log(2.0)}  # (D) R1 whole-clip thresholds: overall tempo off by 25 %, overall pitch range halved
CLIP_H = 3.5  # (S) R2 whole-clip threshold in robust units of the reader-pair clip medians: the modified z-score outlier convention
#   of the NIST/SEMATECH handbook, section 1.3.5.17. The spread is floored like the local scale, so a threshold can be CLIP_H * floor.

# --------------------------------------------------------------------------------------------- scores (6)
X_SAT = {"D1": math.log(1.9), "D2": 1.0, "D3": math.log(5.0), "D4": 1.5, "D5": 12.0, "D6": 1.0}  # (D) L3 magnitude, physical units;
#   D3: a 4 st window range flattened to nothing, ln((4 + 1) / (0 + 1))
R2_SAT_THRESHOLD_FACTOR = 2.0  # keep positive severity width above every fitted R2 threshold
CLIP_SAT = {"D1": X_SAT["D1"], "D3": X_SAT["D3"]}  # whole-clip measures saturate where the local ones do
PMAX_START = {"D1": 0.40, "D2": 0.50, "D3": 0.40, "D4": 0.50, "D5": 0.40, "D6": 0.40}  # (D) refit on train
PMAX_FACTOR_GRID = tuple(round(0.20 * 1.05 ** i, 4) for i in range(0, 80))  # uniform factor searched by calibrate
GATE_IDENTITY, GATE_L1_MIN, GATE_G5_MAX = 100.0, 90.0, 50.0

# --------------------------------------------------------------------------------------------- flaws (2.4)
FLAW_TYPES = ("RUSH", "DRAG", "PAUSE_DROPPED", "PAUSE_INTRUSIVE", "MONOTONE", "DEEMPHASIS", "FADE", "MUMBLE")
FLAW_DIM = {"RUSH": "D1", "DRAG": "D1", "PAUSE_DROPPED": "D2", "PAUSE_INTRUSIVE": "D2", "MONOTONE": "D3",
            "DEEMPHASIS": "D4", "FADE": "D5", "MUMBLE": "D6"}
LEVELS = (1, 2, 3)
LEVEL_PARAM = {  # physical magnitude per level (D)
    "RUSH": (1.20, 1.45, 1.90),  # speech duration x 1/r
    "DRAG": (1.20, 1.45, 1.90),  # speech duration x r
    "PAUSE_DROPPED": (0.40, 0.20, 0.0),  # fraction f of the pause kept; level 3 keeps PAUSE_FLOOR_S
    "PAUSE_INTRUSIVE": (0.35, 0.6, 1.2),  # s of inserted room tone
    "MONOTONE": (0.50, 0.25, 0.0),  # F0 range kept k
    "DEEMPHASIS": (0.5, 0.75, 1.0),  # strength
    "FADE": (4.0, 8.0, 14.0),  # dB
    "MUMBLE": (0.3, 0.6, 1.0),  # strength m
}
PAUSE_FLOOR_S = 0.06  # s, level-3 PAUSE_DROPPED keeps this much
EXPECTED_SECONDARY = {  # (D) dimensions where a firing is not counted as a false region
    "RUSH": ("D4",), "DRAG": ("D2", "D4", "D6"), "PAUSE_DROPPED": ("D1",), "PAUSE_INTRUSIVE": ("D1",), "MONOTONE": ("D4",),
    "DEEMPHASIS": ("D1", "D3", "D5"), "FADE": ("D4",), "MUMBLE": (),
}
SPAN_WORDS = (5, 8)  # windowed dimensions, inclusive
EDIT_GAP_WORDS = 2  # edits stay at least this many words apart (D)
COVERAGE_CAP = 0.35  # edited word coverage per clip; the botched rung and identity clips are exempt
PRAAT_SEED = 42  # random_initializeWithSeedUnsafelyButPredictably before every edit (K)
PSOLA_F0 = (60.0, 400.0)  # Hz analysis range of the Praat Manipulation object (K)
PSOLA_STEP_S = 0.01
WSOLA_FRAME_MS, WSOLA_TOL_MS = 30.0, 10.0  # (K)
XFADE_S = 0.005  # s, WSOLA exit cross-fade (K)
SPLICE_FADE_S = 0.010  # s, cross-fade where a whole-clip PSOLA / WORLD result is spliced back (K)
WSOLA_MIN_PIECE_S = 0.12  # s, shorter speech pieces are left unscaled (D)
INSERT_MIN_GAP_S = 0.03  # s, raw gap needed to insert a pause at a word boundary (D)
PAUSE_FADE_S = 0.010  # s, pause insert / remove cross-fade (K)
FLATTEN_RAMP_S = 0.05  # s, raised-cosine ramps of F0 flattening and mumble (K)
DEEMPH_RAMP_S, DEEMPH_MAX_RATE, DEEMPH_MAX_GAIN_DB = 0.03, 1.25, -6.0  # (K)
FADE_RELEASE_S = 0.10  # s (K); the release belongs to the edit support
FADE_RAMP_FRACTION = 1 / 3  # the ramp takes the first third of the span
MUMBLE_NFFT, MUMBLE_HOP, MUMBLE_SIGMA_MS, MUMBLE_MAX_GAIN_DB = 512, 128, 60.0, 12.0  # (K)
ROOM_TONE_GUARD_S, ROOM_TONE_MIN_S, ROOM_TONE_XFADE_S, ROOM_TONE_DB_SPREAD = 0.08, 0.15, 0.02, 3.0  # (K)
G5_FADES = 2  # fade spans in the botched clip (D)
G1_TYPE, G3_TYPES = "RUSH", ("RUSH", "MONOTONE", "FADE")  # (D) ladder composition
SINGLE_LEVEL_SETS = (("RUSH", "PAUSE_DROPPED", "MONOTONE", "FADE"), ("DRAG", "PAUSE_INTRUSIVE", "DEEMPHASIS", "MUMBLE"))
CROSS_SPEAKER_CLIPS = ((2, ("RUSH", "PAUSE_DROPPED")), (3, ("DRAG", "MONOTONE")), (3, ("PAUSE_INTRUSIVE", "FADE")), (3, ("RUSH", "PAUSE_DROPPED")))
CHAIN_B_TYPES = ("RUSH", "DRAG", "MONOTONE")
PLACEBO_SEEDS = 5  # on-the-fly placebo seeds per baseline

# --------------------------------------------------------------------------------------------- passages (2.2)
PASSAGE_S = (20.0, 40.0)  # s, accepted window duration
PASSAGE_TARGET_S = 30.0
SENTENCE_COVERAGE_MIN = 0.80  # each sentence of a window must be anchored at least this much
PASSAGE_CONTEXT_S = 0.5  # s of audio context each side when force-aligning a window
CLIP_PAD_S = 0.5  # s of audio kept before the first and after the last word of a clip
ABBREVIATIONS = ("mr", "mrs", "ms", "dr", "st", "gen", "sen", "rep", "gov", "no", "vs", "u.s", "jr", "sr", "lt", "col", "mt")

# --------------------------------------------------------------------------------------------- evaluation (8)
IOU_MIN = 0.5
EVENT_TOL_S = 0.2
PAUSE_DIAGNOSIS_FRACTION = 0.50  # flag a boundary measurement missing over half the injected change
HEADLINE_LEVELS = (2, 3)
RULE_OF_THREE = 3.0  # upper 95 % bound of a rate with zero events is 3 / exposure
GAIN_DB, LOWPASS_HZ, NOISE_SNR_DB, MP3_KBPS = 6.0, 3400.0, 20.0, 64  # stress matrix (D)
COMPRESSION = (-20.0, 4.0)  # dB threshold below the clip's P99 envelope level, ratio (D) dynamic range compression
SPEAKER_TRANSFORM = (1.25, 1.10)  # WORLD (f0 ratio, formant ratio) used as a different-speaker proxy (D)
RANDOM_SEEDS = 20  # trivial random-span baseline repetitions (D)
DEVICE_AGREEMENT_CLIPS = 6  # (D) held-out clips aligned on GPU and on CPU for the device-agreement section


def _base_dict() -> dict:
    """All public constants as JSON-able values (tuples become lists); used for the config hash."""
    out = {}
    for k, v in globals().items():
        if k.isupper() and not k.startswith("_"):
            out[k] = _plain(v)
    return out


def _plain(v):
    if isinstance(v, (tuple, list)):
        return [_plain(i) for i in v]
    if isinstance(v, dict):
        return {str(k): _plain(i) for k, i in v.items()}
    return v


_DETECTOR_KEYS = tuple(_base_dict())
CORE8_TYPES = FLAW_TYPES
# pace_pauses REPORT §1/§4: articulation-rate rise 13–18%; 13/15/18% chosen within that range.
RUSH_RATE = (1.13, 1.15, 1.18)
# pace_pauses REPORT §4: shorten/delete pauses, no numeric fraction; chosen fractions ending in deletion.
RUSH_PAUSE_KEEP = (0.6, 0.3, 0.0)
# pace_pauses REPORT §4: stretch a content word, no factor; chosen duration factors.
HESITATION_STRETCH = (1.2, 1.5, 1.8)
# pace_pauses REPORT §4: within-phrase insertion 0.2–1.0 s; chosen lower/middle/upper anchors.
HESITATION_PAUSE_S = (0.2, 0.5, 1.0)
# pace_pauses REPORT §4: word-by-word silences 0.15–0.3 s (midpoint chosen).
READING_PAUSE_S = (0.15, 0.225, 0.3)
# pace_pauses REPORT §4: mean-one random factors, no dispersion; chosen maximum deviations.
TEMPO_DEVIATION = (0.15, 0.3, 0.45)
# disfluency REPORT §4: first typical token lengthened, no factor; chosen substantial stretches.
WORD_REPEAT_STRETCH = (1.3, 1.6, 1.9)
# disfluency REPORT §4: 100–350 ms between copies; chosen anchors (one copy at every level).
WORD_REPEAT_PAUSE_S = (0.1, 0.225, 0.35)
# disfluency REPORT §4: 2–5 phone copies; choose 2/3/4 rapid inserted copies.
SOUND_REPEAT_COPIES = (2, 3, 4)
# disfluency REPORT §4: 100–350 ms pauses; rapid form uses the published lower anchor at all levels.
SOUND_REPEAT_PAUSE_S = (0.1, 0.1, 0.1)
# disfluency REPORT §4/§2.1: onset continuant can exceed 1 s; chosen targets capped at 1 s.
ONSET_TARGET_S = (0.35, 0.65, 1.0)
# disfluency REPORT §4: "first fraction" unspecified; 20% onset proxy chosen, not a phone boundary.
ONSET_FRACTION = 0.2
# disfluency REPORT §4: inserted block gap 0.5–2.0 s; midpoint chosen, location moved inside word.
BLOCK_PAUSE_S = (0.5, 1.25, 2.0)
# Signal eligibility choices: 90 ms stable voiced material and onset search within 80 ms.
CONTINUANT_MIN_S, CONTINUANT_ONSET_S, BURST_WINDOW_S = 0.09, 0.10, 0.08
CONTINUANT_BANDS = 16
BURST_FRAME_S, BURST_STEP_S = 0.004, 0.001
BURST_FLUX_RATIO, BURST_HIGH_SHARE, BURST_HIGH_HZ, BURST_MIN_RMS = 4.0, 0.15, 1500.0, 0.003
REPEAT_DURATION_JITTER, REPEAT_GAIN_JITTER_DB = 0.08, 1.0
ALPHA_SPEECH_MARGIN_DB, EFFORT_ROOM_FILL = 15.0, 0.1
CONTINUANT_CHANGE, BURST_RISE_DB = 0.20, 6.0
# disfluency REPORT §4: WSOLA 5–10x, phones 2–4x; chosen added durations exceed alignment error.
RHYME_ADDED_S, PROLONG_MAX_FACTOR = (0.18, 0.36, 0.54), 10.0
# volume_clarity REPORT §2.1: alpha drop 0.4–0.7 dB per dB of attenuation; midpoint chosen.
EFFORT_ALPHA_PER_DB = 0.55
TRAIL_WORDS = 3
EXTRA_SENTENCE_MIN_S = 0.5  # chosen minimum for a contour template/target; not a published norm
# volume_clarity REPORT §2.1/§4: attenuation and small F0 shift chosen; tilt fitted to alpha coupling.
EFFORT_GAIN_DB, EFFORT_PITCH_ST = (3.0, 6.0, 9.0), (0.5, 1.0, 1.5)
# volume_clarity REPORT §4: sentence-end gain/tilt ramp, no magnitudes; chosen engineering levels.
TRAIL_GAIN_DB = (4.0, 8.0, 12.0)
# volume_clarity REPORT §4: tilt filter, no shelf knee; chosen knee in Hz, not a published cutoff.
TILT_KNEE_HZ = 250.0
# pitch_emphasis REPORT §4: duration/pitch/level boost + de-emphasis, no magnitudes; chosen levels.
EMPH_DURATION, EMPH_PITCH_ST, EMPH_GAIN_DB = (1.1, 1.2, 1.3), (2.0, 4.0, 6.0), (2.0, 4.0, 6.0)
EMPH_REMOVE = (0.3, 0.6, 0.9)  # pitch_emphasis REPORT §4: de-emphasis proposal, strengths chosen.
# pitch_emphasis REPORT §4: last 200–300 ms; midpoint chosen; rise size not published, chosen in st.
ENDING_WINDOW_S, ENDING_RISE_ST = 0.25, (2.0, 4.0, 6.0)
# pitch_emphasis REPORT §4: flatten fall / copy contour, no levels; chosen interpolation strengths.
CONTOUR_STRENGTH = (1 / 3, 2 / 3, 1.0)
# SYNTHESIS §2: word-boundary error 48–89 ms is empirical, NOT a guaranteed upper bound.
ALIGNMENT_ERROR_S = (0.048, 0.089)


FLAW_REGISTRY = {t: {"primary": FLAW_DIM[t], "family": FLAW_DIM[t], "levels": LEVEL_PARAM[t],
                     "secondary": EXPECTED_SECONDARY[t], "event": "boundary" if t.startswith("PAUSE") else "word" if t == "DEEMPHASIS" else "span",
                     "sign": 1 if t in ("DRAG", "PAUSE_INTRUSIVE") else -1} for t in CORE8_TYPES}


def _extra(primary, event, sign, secondary, **params):
    return {"primary": primary, "family": primary, "event": event, "sign": sign, "secondary": secondary,
            "levels": tuple({k: v[i] for k, v in params.items()} for i in range(3))}


# recipes_report.md: primary families, secondary effects and named recipe units.
FLAW_REGISTRY.update({
    "NATURAL_RUSH": _extra("D1", "span", -1, ("D2", "D4"), speech_rate=RUSH_RATE, pause_kept_fraction=RUSH_PAUSE_KEEP),
    "HESITATION": _extra("D1", "word", 1, ("D2", "D4"), word_duration_factor=HESITATION_STRETCH, silence_s=HESITATION_PAUSE_S),
    "WORD_BY_WORD": _extra("D2", "span", 1, ("D1",), silence_s=READING_PAUSE_S, every_words=(1, 1, 1)),
    "UNEVEN_TEMPO": _extra("D1", "span", 0, ("D4", "D6"), max_duration_deviation=TEMPO_DEVIATION),
    "WORD_REPETITION": _extra("DISFLUENCY", "word", 0, ("D1", "D2"), first_token_duration_factor=WORD_REPEAT_STRETCH,
                              silence_s=WORD_REPEAT_PAUSE_S, inserted_copies=(1, 1, 1)),
    "SOUND_REPETITION": _extra("DISFLUENCY", "word", 0, ("D1", "D2", "D6"), inserted_copies=SOUND_REPEAT_COPIES, silence_s=SOUND_REPEAT_PAUSE_S),
    "RHYME_PROLONGATION": _extra("DISFLUENCY", "word", 0, ("D1", "D4"), added_duration_s=RHYME_ADDED_S),
    "ONSET_PROLONGATION": _extra("DISFLUENCY", "word", 0, ("D1", "D6"), onset_target_s=ONSET_TARGET_S),
    "BLOCK": _extra("DISFLUENCY", "word", 0, ("D1", "D2", "D6"), silence_s=BLOCK_PAUSE_S),
    "LOW_EFFORT": _extra("D5", "span", -1, ("D3", "D4", "D6"), attenuation_db=EFFORT_GAIN_DB, alpha_drop_per_db=(EFFORT_ALPHA_PER_DB,) * 3,
                         pitch_lowering_st=EFFORT_PITCH_ST),
    "TRAILING_OFF": _extra("D5", "span", -1, ("D4", "D6"), final_attenuation_db=TRAIL_GAIN_DB, alpha_drop_per_db=(EFFORT_ALPHA_PER_DB,) * 3),
    "MISPLACED_EMPHASIS": _extra("D4", "span", -1, ("D1", "D3", "D5"), function_duration_factor=EMPH_DURATION,
                                 function_pitch_st=EMPH_PITCH_ST, function_gain_db=EMPH_GAIN_DB, stressed_removal_strength=EMPH_REMOVE),
    "RISING_ENDING": _extra("ENDINGS", "word", 0, ("D3", "D4"), rise_st=ENDING_RISE_ST),
    "FLAT_FINAL_FALL": _extra("ENDINGS", "word", 0, ("D3", "D4"), strength=CONTOUR_STRENGTH),
    "REPEATED_CONTOUR": _extra("D3", "span", -1, ("D4",), contour_strength=CONTOUR_STRENGTH),
})
EXTRA_SINGLE_LEVEL_SETS = (
    ("NATURAL_RUSH", "WORD_REPETITION", "LOW_EFFORT", "RISING_ENDING"),
    ("HESITATION", "SOUND_REPETITION", "MISPLACED_EMPHASIS", "FLAT_FINAL_FALL"),
    ("WORD_BY_WORD", "RHYME_PROLONGATION", "TRAILING_OFF"),
    ("UNEVEN_TEMPO", "ONSET_PROLONGATION", "BLOCK", "REPEATED_CONTOUR"),
)
EXTRA_CROSS_SETS = (
    ("NATURAL_RUSH", "WORD_REPETITION", "LOW_EFFORT"),
    ("HESITATION", "SOUND_REPETITION", "TRAILING_OFF"),
    ("WORD_BY_WORD", "RHYME_PROLONGATION"),
    ("UNEVEN_TEMPO", "ONSET_PROLONGATION", "BLOCK"),
    ("MISPLACED_EMPHASIS", "RISING_ENDING"),
    ("REPEATED_CONTOUR", "FLAT_FINAL_FALL"),
)
EXTRA_CROSS_CLIPS = tuple((lv, ts) for lv in (2, 3) for ts in EXTRA_CROSS_SETS if lv == 3 or ts[0] in
                          ("NATURAL_RUSH", "HESITATION", "WORD_BY_WORD", "UNEVEN_TEMPO"))
REGISTRY_VERSION = 3


def _released_dict() -> dict:
    """Released detector constants; dataset-only metadata must not invalidate the frozen detector."""
    out = {k: _plain(globals()[k]) for k in _DETECTOR_KEYS}
    out["FLAW_TYPES"] = list(CORE8_TYPES)
    for name in ("FLAW_DIM", "LEVEL_PARAM", "EXPECTED_SECONDARY"):
        out[name] = {t: out[name][t] for t in CORE8_TYPES}
    return out


UNIT_KIND = {dim: "boundary" if dim == "D2" else "word" if dim == "D4" else "window" for dim in DIMS}

# Schema 3 remains readable for the frozen artifact and the refactor regression check.
_LEGACY_CONFIG = _released_dict()
BLOCK_S, STABLE_S = 0.25, 0.20  # s, disfluency report duration floors
STABLE_PITCH_ST, STABLE_SPECTRUM = 0.50, 0.08  # lab stability limits; low F0 is below the voiced median
ORPHAN_MIN_S = 0.20  # s, lab voiced-gap floor
FINAL_WINDOW_S, MIN_FINAL_VOICED = 0.20, 5  # s and frames, sentence-ending comparison stretches
CONTOUR_POINTS = 32  # lab contour interpolation grid
STABLE_PITCH_FRAMES, STABLE_SPECTRUM_FRAMES = 5, 10  # Goto windows at the 10 ms frame hop
SPECTRAL_BATCH = 2048  # frames, bounded temporary FFT allocation
ALPHA_LOW_HZ, ALPHA_HIGH_HZ, MID_SHARE_HZ = (50, 1000), (1000, 5000), (1000, 3000)  # report frequency bands
ENVELOPE_BASE_HZ, ENVELOPE_BANDS, ENVELOPE_BANDS_PER_OCTAVE = 160, 16, 3  # third-octave envelopes
STABLE_BANDS, STABLE_BAND_HZ = 16, 200  # normalized narrow-band amplitudes for stability
EMPH_CUTOFF_F0, EMPH_CUTOFF_HZ, EMPH_FILTER_ORDER = 1.5, (50, 7000), 4  # spectral-emphasis high-pass complement
MODULATION_HZ, MODULATION_ORDER, MODULATION_MIN_FRAMES = (0.5, 10), 2, 100  # envelope bandpass and sample floor
INSERTION_CONTEXT_WORDS = 2  # word copies/prefixes near a greedy insertion
FUNCTION_WORDS = tuple('a an the and or but if as at by for from in into of on to with is am are was were be '
                       'been being do does did have has had can could will would shall should may might '
                       'must i you he she it we they me him her us them my your his its our their this '
                       'that these those not'.upper().split())
FALSE_CLIP_RATE_BUDGET = 0.05  # false whole-clip flags per null clip, separate from the local budget
R2_REFERENCES = 5  # seeded draws per participant; smaller sets repeat references without treating draws as readers
R2_BOOTSTRAPS = 1000  # participant-reader cluster resamples for the reported upper bound
R2_FIT_SHARE, R2_SELECT_SHARE = 0.50, 0.25  # reader-disjoint split; the remainder is lockbox
R2_ALIGNMENT_SECONDS_PER_AUDIO = 0.06  # conservative T4x2 lab forecast; wall s per audio s
R2_ALIGNMENT_SECONDS_PER_CLIP = 0.3  # forecast overhead per aligned reading
R2_ALIGNMENT_BUDGET_S = 5400  # reserve 30 minutes of the two-hour run for edits, calibration and evaluation
R2_SELECT_EDIT_CAP = 160  # maximum full-text select edits across all calibrated types
R2_SELECT_EDIT_BATCH = 8  # clips held during injection, preparation and matching
R2_SELECT_EDIT_BUDGET_S = 600  # wall s reserved inside the 30-minute calibration forecast
R2_PREPARE_BATCH = 64  # bound temporary WAV/job copies while using every pool worker
FLAW_REGISTRY['HESITATION'].update(primary='D2', secondary=('D1', 'D4', 'D7'))
DIMS += ('D7', 'D8')
DIM_LABEL.update(D7='Word time', D8='Ending')
DIM_BRIEF.update(D7='Cadence', D8='Tone')
DIM_UNIT.update(D7='ln', D8='st')
REGIME_DIMS['R1'] = tuple(d for d in DIMS if d != 'D8')  # (D) D8 is listed in R1: two eligible val ending events
LISTED_DIMS = {'R1': ('D7', 'D8'), 'R2': ('D7', 'D8')}
D7_REG_S = CTC_FRAME_S  # Occupancy is quantised in CTC frames.
D7_MIN_S = 3 * CTC_FRAME_S
D7_IDENTITY_TOL_LN = 0.05
FLAG_SIGNS.update(D7=(1,), D8=(1,))
CLIP_DIMS += ('D7',)
UNIT_KIND.update(D7='word', D8='word')
FLOORS.update(D7=math.log(1.25), D8=1.0)  # Design floors: timing ratio and pitch discrimination in st.
MIN_REGION_WORDS.update(D7=1, D8=1)
X_SAT.update(D7=math.log(5), D8=6.0)  # Design saturation; refit Pmax on train.
PMAX_START.update(D7=0.5, D8=0.4)
CLIP_LN['D7'] = math.log(1.25)  # Typical word-time ratio spread, ln.
CLIP_SAT['D7'] = math.log(1.9)
WORD_BY_WORD_MIN_EVENTS = 3  # Design: isolated pauses do not establish word-by-word reading.
HESITATION_STRETCH_MIN = math.log(1.25)  # Lab timing floor; independent of recipe levels.
ALPHA_DROP_DB = 1.0  # Lab alpha-ratio resolution for supporting effort evidence, dB.
STUTTER_BASE_RATE = 0.0021  # disfluency REPORT §3: 0.21% stuttered syllables in fluent readers.
PROMOTION_RECALL_MIN, PROMOTION_AUC_MIN = 0.5, 0.70  # Agreed select-set product gate.
LABEL_PRECISION_MIN, PROMOTION_AUC_LOWER_MIN = 0.5, 0.5  # Real precision and chance-AUC gates in design §8.
PROMOTION_MAX_EXISTING_LOSS = 1
# Real validation is supplied in the calibration report; unvalidated labels retain the fallback.
PATTERN_GATES = {'BLOCK': 'block', 'WORD_REPETITION': 'repetition', 'SOUND_REPETITION': 'repetition',
                 'ONSET_PROLONGATION': 'prolongation', 'RHYME_PROLONGATION': 'prolongation',
                 'FILLED_PAUSE': 'filled_pause', 'LOW_EFFORT': 'low_effort', 'TRAILING_OFF': 'trailing_off',
                 'NATURAL_RUSH': 'natural_rush', 'UNEVEN_TEMPO': 'uneven_tempo'}
FLAW_REGISTRY['HESITATION']['family'] = 'D2'
for _type in ('WORD_REPETITION', 'SOUND_REPETITION', 'RHYME_PROLONGATION', 'ONSET_PROLONGATION', 'BLOCK'):
    FLAW_REGISTRY[_type].update(primary='D7', sign=1)
for _type in ('RISING_ENDING', 'FLAT_FINAL_FALL'):
    FLAW_REGISTRY[_type].update(primary='D8', sign=1)
FLAW_REGISTRY['UNEVEN_TEMPO'].update(primary='D7', event='clip', sign=1)
FLAW_REGISTRY['REPEATED_CONTOUR'].update(primary='NO_DETECTOR', family='CONTOUR')
for _type, _dim in (('DRAG', 'D7'), ('MISPLACED_EMPHASIS', 'D7'), ('UNEVEN_TEMPO', 'D7'), ('MONOTONE', 'D8')):
    FLAW_REGISTRY[_type]['secondary'] = tuple(dict.fromkeys((*FLAW_REGISTRY[_type]['secondary'], _dim)))
EXTRA_TYPES = tuple(t for t in FLAW_REGISTRY if t not in CORE8_TYPES)
FLAW_TYPES = tuple(FLAW_REGISTRY)
FLAW_DIM = {t: r['primary'] for t, r in FLAW_REGISTRY.items()}
FLAW_FAMILY = {t: r['family'] for t, r in FLAW_REGISTRY.items()}
LEVEL_PARAM = {t: r['levels'] for t, r in FLAW_REGISTRY.items()}
EXPECTED_SECONDARY = {t: r['secondary'] for t, r in FLAW_REGISTRY.items()}
if any(d not in DIMS for r in FLAW_REGISTRY.values() for d in r['secondary']):
    raise ValueError('registry secondary dimension has no measure')


CONSENSUS_K = 5
DIMS += ('D9',)
DIM_LABEL['D9'] = 'Speech tempo'
DIM_BRIEF['D9'] = 'Cadence'
DIM_UNIT['D9'] = 'ln'
FLAG_SIGNS['D9'] = (-1,)
UNIT_KIND['D9'] = 'window'
FLOORS['D9'] = math.log(1.05)
MIN_REGION_WORDS['D9'] = 2
REGION_PEAK_FRACTION['D9'] = 0.5
X_SAT['D9'] = X_SAT['D1']  # (D) RUSH L3 word-time ratio 1.90, as D1: a ln(1.18) cap put a G1 rush below the G3 mix
PMAX_START['D9'] = 0.4
REGIME_DIMS['R1'] += ('D9',)
LISTED_DIMS['R2'] += ('D9',)
# (D) Owner decisions: listed and unscored whatever the validation gates give, with the reason shown in the API.
OWNER_LISTED = {'R1': {'D8': 'owner decision: the RISING_ENDING recipe mostly does not realise; val has 2 eligible ending events'},
                'R2': {'D9': 'owner decision: dev v13 found 0 of 68 R2 rush positives, at one seventh of the local budget'}}
# (D) natural-rushing rule (pace_pauses REPORT §1/§4; recipe edits_extra.natural_rushing): faster words and shorter pauses.
# A D9- region is natural rushing only when the paired pause time in its windows' words is below both the word-time ratio
# and this kept fraction, the ln midpoint between pauses kept (1.0) and the mildest recipe fraction (0.6).
NATURAL_RUSH_PAUSE_KEPT_MAX = math.sqrt(RUSH_PAUSE_KEEP[0])
FLAW_REGISTRY['NATURAL_RUSH']['primary'] = 'D9'
FLAW_DIM['NATURAL_RUSH'] = 'D9'
# (D) A region of the key flags the same change as a region or truth of the value key: duplicate, not false.
SAME_CHANGE = {'D9-': 'D1-'}


def as_dict(schema: int = 4) -> dict:
    if schema == 3:
        return _plain(_LEGACY_CONFIG)
    out = {k: _plain(globals()[k]) for k in _DETECTOR_KEYS}
    out.update({k: _plain(globals()[k]) for k in (
        'CONSENSUS_K', 'UNIT_KIND', 'BLOCK_S', 'STABLE_S', 'STABLE_PITCH_ST', 'STABLE_SPECTRUM', 'ORPHAN_MIN_S',
        'FINAL_WINDOW_S', 'MIN_FINAL_VOICED', 'CONTOUR_POINTS', 'STABLE_PITCH_FRAMES', 'STABLE_SPECTRUM_FRAMES',
        'SPECTRAL_BATCH', 'ALPHA_LOW_HZ', 'ALPHA_HIGH_HZ', 'MID_SHARE_HZ', 'ENVELOPE_BASE_HZ', 'ENVELOPE_BANDS',
        'ENVELOPE_BANDS_PER_OCTAVE', 'STABLE_BANDS', 'STABLE_BAND_HZ', 'EMPH_CUTOFF_F0', 'EMPH_CUTOFF_HZ',
        'EMPH_FILTER_ORDER', 'MODULATION_HZ', 'MODULATION_ORDER', 'MODULATION_MIN_FRAMES', 'INSERTION_CONTEXT_WORDS', 'FUNCTION_WORDS', 'FALSE_CLIP_RATE_BUDGET',
        'R2_REFERENCES', 'R2_BOOTSTRAPS', 'R2_FIT_SHARE', 'R2_SELECT_SHARE', 'R2_ALIGNMENT_SECONDS_PER_AUDIO',
        'R2_ALIGNMENT_SECONDS_PER_CLIP', 'R2_ALIGNMENT_BUDGET_S', 'R2_SELECT_EDIT_CAP', 'R2_SELECT_EDIT_BATCH', 'R2_SELECT_EDIT_BUDGET_S', 'R2_PREPARE_BATCH', 'FLAW_REGISTRY', 'CORE8_TYPES', 'EXTRA_TYPES',
        'LISTED_DIMS', 'D7_REG_S', 'D7_MIN_S', 'D7_IDENTITY_TOL_LN', 'WORD_BY_WORD_MIN_EVENTS', 'HESITATION_STRETCH_MIN', 'ALPHA_DROP_DB',
        'STUTTER_BASE_RATE', 'PROMOTION_RECALL_MIN', 'PROMOTION_AUC_MIN', 'LABEL_PRECISION_MIN', 'PROMOTION_AUC_LOWER_MIN', 'PROMOTION_MAX_EXISTING_LOSS', 'PATTERN_GATES', 'SAME_CHANGE', 'NATURAL_RUSH_PAUSE_KEPT_MAX', 'OWNER_LISTED')})
    return out
