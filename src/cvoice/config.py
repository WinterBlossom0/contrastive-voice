"""Every numeric constant of the detector, the dataset recipes and the evaluation, in one place.

Evidence tags in the trailing comments: (K) measured on a Kaggle CPU kernel during research,
(S) from a fetched source, (D) design value fixed before any evaluation run. Units are stated per constant.
Each constant is defined once. `as_dict()` feeds the released detector hash (schema 4; `as_dict(3)` gives the schema-3
subset of the eight core types). Dataset recipe metadata is versioned separately (REGISTRY_VERSION).
"""
from __future__ import annotations

import math

# --------------------------------------------------------------------------------------------- dimensions
# D1-D6 are the dimensions of the eight core flaw types (detector schema 3); D7-D9 measure the extra types.
DIMS = ("D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9")
DIM_LABEL = {"D1": "Pace", "D2": "Pauses", "D3": "Pitch variation", "D4": "Emphasis", "D5": "Volume", "D6": "Clarity (spectral-change proxy)",
             "D7": "Word time", "D8": "Ending", "D9": "Speech tempo"}
DIM_BRIEF = {"D1": "Cadence", "D2": "Pauses", "D3": "Tone", "D4": "Tone", "D5": "Volume", "D6": "Clarity",
             "D7": "Cadence", "D8": "Tone", "D9": "Cadence"}  # brief's words
DIM_UNIT = {"D1": "ln", "D2": "s", "D3": "ln", "D4": "p", "D5": "dB", "D6": "ln", "D7": "ln", "D8": "st", "D9": "ln"}
REGIMES = ("R1", "R2")
# (D) D4, D6 are displayed, never flagged or scored in R2. D8 is listed in R1: val has two eligible ending events.
REGIME_DIMS = {"R1": ("D1", "D2", "D3", "D4", "D5", "D6", "D7", "D9"), "R2": ("D1", "D2", "D3", "D5")}
# Dimensions shown with their measures but never flagged or scored, whatever the validation gates give.
LISTED_DIMS = {"R1": ("D7", "D8"), "R2": ("D7", "D8", "D9")}
FLAG_SIGNS = {"D1": (-1, 1), "D2": (-1, 1), "D3": (-1,), "D4": (-1,), "D5": (-1,), "D6": (-1,),
              "D7": (1,), "D8": (1,), "D9": (-1,)}  # (D)
CLIP_DIMS = ("D1", "D3", "D7")  # dimensions with a whole-clip measure next to the local one: overall tempo, overall pitch range, uneven tempo
UNIT_KIND = {dim: "boundary" if dim == "D2" else "word" if dim in ("D4", "D7", "D8") else "window" for dim in DIMS}


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
# 6-18 ms boundary error); per-word compatibility is reported, never used to exclude a word.
LOW_COMPAT_NOTICE = 0.10  # (D) words below this are counted in a low-confidence notice, still scored
MEAN_COMPAT_MIN = 0.10  # (D) refusal "transcript does not match the audio", enforced only at trust boundaries (uploads, passage selection)
# Partial-mismatch refusal of uploads (align.require_full_match); outside the detector hash because it only refuses an upload.
MISMATCH_TOL_FRAMES = 4  # CTC frames (80 ms)
MISMATCH_SPIKE_P = 0.5  # posterior of the most probable letter on a spike frame
# Limits 1.25 x the largest value of 1936 real readings with their correct transcripts (gallery, train and val clips,
# EARS, Speech Accent Archive and LibriVox readers); the calibration record is not published.
MISMATCH_WINDOW_S = 2.0  # s
MISMATCH_MISSING_MAX, MISMATCH_EXTRA_MAX = 175.0, 360.0  # nats in one MISMATCH_WINDOW_S window
MISMATCH_SPREAD_EXCLUDE_S, MISMATCH_SPREAD_MAX = 3.0, 9.5  # s, nats per second
MISMATCH_QUOTE_WORDS = 4  # words of the transcript quoted in the refusal
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
FLOORS = {"D1": math.log(1.10), "D2": 0.15, "D3": math.log(1.4), "D4": 0.5, "D5": 2.0, "D6": math.log(1.25),
          "D7": math.log(1.25), "D8": 1.0, "D9": math.log(1.05)}  # (D) minimum scale;
#   D3: a 2 st narrowing of a 6 st window range, ln((6 + 1) / (4 + 1)); D7 a timing ratio; D8 pitch discrimination in st
Q68 = 0.682689492  # quantile of |x| used as a scale
HYSTERESIS_LOW = 0.5  # regions extend over |z| >= h * this ...
REGION_PEAK_FRACTION = {"D1": 0.5, "D3": 0.0, "D5": 0.5, "D6": 0.5, "D9": 0.5}  # (D) ... and over |z| >= this * the run's peak |z| (half-maximum
#   rule); the larger bound applies. A window mean (D1, D5, D6) responds in proportion to how much of the window an edit
#   covers, so half the peak marks the edit's edge (also D9). The pitch range (D3) collapses only once the window lies inside a flat stretch:
#   its response is already narrower than the stretch and is not trimmed.
MIN_REGION_WORDS = {"D1": 2, "D2": 1, "D3": 2, "D4": 1, "D5": 1, "D6": 1, "D7": 1, "D8": 1, "D9": 2}
H_GRID = tuple(round(1.0 + 0.05 * i, 2) for i in range(221))  # 1.00:0.05:12.00
R1_H_RANGE = (1.0, 3.0)  # train supervised selection keeps one bounded common threshold
MIN_MEASUREMENT_COVERAGE = 0.50  # below this coverage, a dimension is scored only if it has a flag
DIFFERENCE_H, MAX_DIFFERENCES = 1.0, 5  # unscored R2 local differences, ranked by absolute z
FALSE_RATE_BUDGET = 0.50  # false regions per minute on the regime's train nulls
# (D) R1 whole-clip thresholds: overall tempo off by 25 %, overall pitch range halved, typical word-time ratio spread 25 %
CLIP_LN = {"D1": math.log(1.25), "D3": math.log(2.0), "D7": math.log(1.25)}
CLIP_H = 3.5  # (S) R2 whole-clip threshold in robust units of the reader-pair clip medians: the modified z-score outlier convention
#   of the NIST/SEMATECH handbook, section 1.3.5.17. The spread is floored like the local scale, so a threshold can be CLIP_H * floor.

# --------------------------------------------------------------------------------------------- scores (6)
X_SAT = {"D1": math.log(1.9), "D2": 1.0, "D3": math.log(5.0), "D4": 1.5, "D5": 12.0, "D6": 1.0,
         "D7": math.log(5), "D8": 6.0, "D9": math.log(1.9)}  # (D) L3 magnitude, physical units;
#   D3: a 4 st window range flattened to nothing, ln((4 + 1) / (0 + 1)); D9: the RUSH L3 word-time ratio 1.90, as D1
#   (a ln(1.18) cap put a G1 rush below the G3 mix)
R2_SAT_THRESHOLD_FACTOR = 2.0  # keep positive severity width above every fitted R2 threshold
CLIP_SAT = {"D1": X_SAT["D1"], "D3": X_SAT["D3"], "D7": math.log(1.9)}  # D1, D3 saturate where the local measures do
PMAX_START = {"D1": 0.40, "D2": 0.50, "D3": 0.40, "D4": 0.50, "D5": 0.40, "D6": 0.40, "D7": 0.5, "D8": 0.4, "D9": 0.4}  # (D) refit on train
PMAX_FACTOR_GRID = tuple(round(0.20 * 1.05 ** i, 4) for i in range(0, 80))  # uniform factor searched by calibrate
GATE_IDENTITY, GATE_L1_MIN, GATE_G5_MAX = 100.0, 90.0, 50.0

# --------------------------------------------------------------------------------------------- flaws (2.4)
# The registry of all flaw types (FLAW_REGISTRY) and its tables (FLAW_TYPES, FLAW_DIM, ...) follow the recipe constants.
CORE8_TYPES = ("RUSH", "DRAG", "PAUSE_DROPPED", "PAUSE_INTRUSIVE", "MONOTONE", "DEEMPHASIS", "FADE", "MUMBLE")
LEVELS = (1, 2, 3)
PAUSE_FLOOR_S = 0.06  # s, level-3 PAUSE_DROPPED keeps this much
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

# --------------------------------------------------------------------------------------------- recipes of the extra flaw types
# Each range below is the published range of the recipe; "chosen" marks a design value inside or beyond it (docs/PAPERS.md).
# Trouvain & Grice 1999: articulation-rate rise 13–18%; 13/15/18% chosen within that range.
RUSH_RATE = (1.13, 1.15, 1.18)
# Trouvain & Grice 1999: shorten/delete pauses, no numeric fraction; chosen fractions ending in deletion.
RUSH_PAUSE_KEEP = (0.6, 0.3, 0.0)
# Moers, Meyer & Janse 2017: stretch a content word, no factor; chosen duration factors.
HESITATION_STRETCH = (1.2, 1.5, 1.8)
# Within-phrase insertion 0.2–1.0 s; chosen lower/middle/upper anchors.
HESITATION_PAUSE_S = (0.2, 0.5, 1.0)
# Word-by-word silences 0.15–0.3 s (midpoint chosen).
READING_PAUSE_S = (0.15, 0.225, 0.3)
# Mean-one random factors, no dispersion; chosen maximum deviations.
TEMPO_DEVIATION = (0.15, 0.3, 0.45)
# First typical token lengthened, no factor; chosen substantial stretches.
WORD_REPEAT_STRETCH = (1.3, 1.6, 1.9)
# 100–350 ms between copies; chosen anchors (one copy at every level).
WORD_REPEAT_PAUSE_S = (0.1, 0.225, 0.35)
# 2–5 phone copies; choose 2/3/4 rapid inserted copies.
SOUND_REPEAT_COPIES = (2, 3, 4)
# 100–350 ms pauses; rapid form uses the published lower anchor at all levels.
SOUND_REPEAT_PAUSE_S = (0.1, 0.1, 0.1)
# Lickley 2017: onset continuant can exceed 1 s; chosen targets capped at 1 s.
ONSET_TARGET_S = (0.35, 0.65, 1.0)
# "First fraction" unspecified; 20% onset proxy chosen, not a phone boundary.
ONSET_FRACTION = 0.2
# Inserted block gap 0.5–2.0 s; midpoint chosen, location moved inside word.
BLOCK_PAUSE_S = (0.5, 1.25, 2.0)
# Signal eligibility choices: 90 ms stable voiced material and onset search within 80 ms.
CONTINUANT_MIN_S, CONTINUANT_ONSET_S, BURST_WINDOW_S = 0.09, 0.10, 0.08
CONTINUANT_BANDS = 16
BURST_FRAME_S, BURST_STEP_S = 0.004, 0.001
BURST_FLUX_RATIO, BURST_HIGH_SHARE, BURST_HIGH_HZ, BURST_MIN_RMS = 4.0, 0.15, 1500.0, 0.003
REPEAT_DURATION_JITTER, REPEAT_GAIN_JITTER_DB = 0.08, 1.0
ALPHA_SPEECH_MARGIN_DB, EFFORT_ROOM_FILL = 15.0, 0.1
CONTINUANT_CHANGE, BURST_RISE_DB = 0.20, 6.0
# WSOLA 5–10x, phones 2–4x; chosen added durations exceed alignment error.
RHYME_ADDED_S, PROLONG_MAX_FACTOR = (0.18, 0.36, 0.54), 10.0
# Sundberg & Nordenberg 2006: alpha drop 0.4–0.7 dB per dB of attenuation; midpoint chosen.
EFFORT_ALPHA_PER_DB = 0.55
TRAIL_WORDS = 3
EXTRA_SENTENCE_MIN_S = 0.5  # chosen minimum for a contour template/target; not a published norm
# Attenuation and small F0 shift chosen; tilt fitted to alpha coupling.
EFFORT_GAIN_DB, EFFORT_PITCH_ST = (3.0, 6.0, 9.0), (0.5, 1.0, 1.5)
# Sentence-end gain/tilt ramp, no magnitudes; chosen engineering levels.
TRAIL_GAIN_DB = (4.0, 8.0, 12.0)
# Tilt filter, no shelf knee; chosen knee in Hz, not a published cutoff.
TILT_KNEE_HZ = 250.0
# Duration/pitch/level boost + de-emphasis, no magnitudes; chosen levels.
EMPH_DURATION, EMPH_PITCH_ST, EMPH_GAIN_DB = (1.1, 1.2, 1.3), (2.0, 4.0, 6.0), (2.0, 4.0, 6.0)
EMPH_REMOVE = (0.3, 0.6, 0.9)  # de-emphasis strengths chosen; no published magnitudes
# Last 200–300 ms; midpoint chosen; rise size not published, chosen in st.
ENDING_WINDOW_S, ENDING_RISE_ST = 0.25, (2.0, 4.0, 6.0)
# Flatten fall / copy contour, no levels; chosen interpolation strengths.
CONTOUR_STRENGTH = (1 / 3, 2 / 3, 1.0)
# Huang et al. 2024: word-boundary error 48–89 ms is empirical, NOT a guaranteed upper bound.
ALIGNMENT_ERROR_S = (0.048, 0.089)



def _core(primary, event, sign, secondary, levels):
    return {"primary": primary, "family": primary, "levels": levels, "secondary": secondary, "event": event, "sign": sign}


def _extra(primary, event, sign, secondary, family=None, **params):
    return {"primary": primary, "family": primary if family is None else family, "event": event, "sign": sign,
            "secondary": secondary, "levels": tuple({k: v[i] for k, v in params.items()} for i in range(3))}


# Per type: primary dimension (the flag key that detects it, with sign; sign 0 = either direction), family (the group it
# is reported under), event kind, expected secondary dimensions (D: a firing there is not counted as a false region) and
# the physical magnitude per level (D).
FLAW_REGISTRY = {
    "RUSH": _core("D1", "span", -1, ("D4",), (1.20, 1.45, 1.90)),  # speech duration x 1/r
    "DRAG": _core("D1", "span", 1, ("D2", "D4", "D6", "D7"), (1.20, 1.45, 1.90)),  # speech duration x r
    "PAUSE_DROPPED": _core("D2", "boundary", -1, ("D1",), (0.40, 0.20, 0.0)),  # fraction f of the pause kept; level 3 keeps PAUSE_FLOOR_S
    "PAUSE_INTRUSIVE": _core("D2", "boundary", 1, ("D1",), (0.35, 0.6, 1.2)),  # s of inserted room tone
    "MONOTONE": _core("D3", "span", -1, ("D4", "D8"), (0.50, 0.25, 0.0)),  # F0 range kept k
    "DEEMPHASIS": _core("D4", "word", -1, ("D1", "D3", "D5"), (0.5, 0.75, 1.0)),  # strength
    "FADE": _core("D5", "span", -1, ("D4",), (4.0, 8.0, 14.0)),  # dB
    "MUMBLE": _core("D6", "span", -1, (), (0.3, 0.6, 1.0)),  # strength m
    # D9 measures the words of a natural rush; the change is reported under pace (D1).
    "NATURAL_RUSH": _extra("D9", "span", -1, ("D2", "D4"), family="D1", speech_rate=RUSH_RATE, pause_kept_fraction=RUSH_PAUSE_KEEP),
    "HESITATION": _extra("D2", "word", 1, ("D1", "D4", "D7"), word_duration_factor=HESITATION_STRETCH, silence_s=HESITATION_PAUSE_S),
    "WORD_BY_WORD": _extra("D2", "span", 1, ("D1",), silence_s=READING_PAUSE_S, every_words=(1, 1, 1)),
    "UNEVEN_TEMPO": _extra("D7", "clip", 1, ("D4", "D6", "D7"), family="D1", max_duration_deviation=TEMPO_DEVIATION),
    "WORD_REPETITION": _extra("D7", "word", 1, ("D1", "D2"), family="DISFLUENCY", first_token_duration_factor=WORD_REPEAT_STRETCH,
                              silence_s=WORD_REPEAT_PAUSE_S, inserted_copies=(1, 1, 1)),
    "SOUND_REPETITION": _extra("D7", "word", 1, ("D1", "D2", "D6"), family="DISFLUENCY", inserted_copies=SOUND_REPEAT_COPIES,
                               silence_s=SOUND_REPEAT_PAUSE_S),
    "RHYME_PROLONGATION": _extra("D7", "word", 1, ("D1", "D4"), family="DISFLUENCY", added_duration_s=RHYME_ADDED_S),
    "ONSET_PROLONGATION": _extra("D7", "word", 1, ("D1", "D6"), family="DISFLUENCY", onset_target_s=ONSET_TARGET_S),
    "BLOCK": _extra("D7", "word", 1, ("D1", "D2", "D6"), family="DISFLUENCY", silence_s=BLOCK_PAUSE_S),
    "LOW_EFFORT": _extra("D5", "span", -1, ("D3", "D4", "D6"), attenuation_db=EFFORT_GAIN_DB, alpha_drop_per_db=(EFFORT_ALPHA_PER_DB,) * 3,
                         pitch_lowering_st=EFFORT_PITCH_ST),
    "TRAILING_OFF": _extra("D5", "span", -1, ("D4", "D6"), final_attenuation_db=TRAIL_GAIN_DB, alpha_drop_per_db=(EFFORT_ALPHA_PER_DB,) * 3),
    "MISPLACED_EMPHASIS": _extra("D4", "span", -1, ("D1", "D3", "D5", "D7"), function_duration_factor=EMPH_DURATION,
                                 function_pitch_st=EMPH_PITCH_ST, function_gain_db=EMPH_GAIN_DB, stressed_removal_strength=EMPH_REMOVE),
    "RISING_ENDING": _extra("D8", "word", 1, ("D3", "D4"), family="ENDINGS", rise_st=ENDING_RISE_ST),
    "FLAT_FINAL_FALL": _extra("D8", "word", 1, ("D3", "D4"), family="ENDINGS", strength=CONTOUR_STRENGTH),
    # No dimension measures a repeated contour: the type is generated, never detected.
    "REPEATED_CONTOUR": _extra("NO_DETECTOR", "span", -1, ("D4",), family="CONTOUR", contour_strength=CONTOUR_STRENGTH),
}
FLAW_TYPES = tuple(FLAW_REGISTRY)
EXTRA_TYPES = tuple(t for t in FLAW_REGISTRY if t not in CORE8_TYPES)
FLAW_DIM = {t: r['primary'] for t, r in FLAW_REGISTRY.items()}
FLAW_FAMILY = {t: r['family'] for t, r in FLAW_REGISTRY.items()}
LEVEL_PARAM = {t: r['levels'] for t, r in FLAW_REGISTRY.items()}
EXPECTED_SECONDARY = {t: r['secondary'] for t, r in FLAW_REGISTRY.items()}
if any(d not in DIMS for r in FLAW_REGISTRY.values() for d in r['secondary']):
    raise ValueError('registry secondary dimension has no measure')
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

# --------------------------------------------------------------------------------------------- measures of D7-D9 and the extra types
BLOCK_S, STABLE_S = 0.25, 0.20  # s, minimum durations of a block and of a stable run
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
D7_REG_S = CTC_FRAME_S  # Occupancy is quantised in CTC frames.
D7_MIN_S = 3 * CTC_FRAME_S
D7_IDENTITY_TOL_LN = 0.05
WORD_BY_WORD_MIN_EVENTS = 3  # Design: isolated pauses do not establish word-by-word reading.
HESITATION_STRETCH_MIN = math.log(1.25)  # Lab timing floor; independent of recipe levels.
ALPHA_DROP_DB = 1.0  # Lab alpha-ratio resolution for supporting effort evidence, dB.
STUTTER_BASE_RATE = 0.0021  # Ritto et al. 2016: 0.21% stuttered syllables in fluent readers.
# (D) natural-rushing rule (Trouvain & Grice 1999; recipe edits_extra.natural_rushing): faster words and shorter pauses.
# A D9- region is natural rushing only when the paired pause time in its windows' words is below both the word-time ratio
# and this kept fraction, the ln midpoint between pauses kept (1.0) and the mildest recipe fraction (0.6).
NATURAL_RUSH_PAUSE_KEPT_MAX = math.sqrt(RUSH_PAUSE_KEEP[0])
# (D) A region of the key flags the same change as a region or truth of the value key: duplicate, not false.
SAME_CHANGE = {'D9-': 'D1-'}

# --------------------------------------------------------------------------------------------- R2 reference pool
CONSENSUS_K = 5  # reference readings in a consensus reference
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

# --------------------------------------------------------------------------------------------- validation gates of the pattern labels
PROMOTION_RECALL_MIN, PROMOTION_AUC_MIN = 0.5, 0.70  # select-set recall and AUC that a label needs for the product
LABEL_PRECISION_MIN, PROMOTION_AUC_LOWER_MIN = 0.5, 0.5  # Real precision and chance-AUC gates, fixed before the lab results
PROMOTION_MAX_EXISTING_LOSS = 1
# Real validation is supplied in the calibration report; unvalidated labels retain the fallback.
PATTERN_GATES = {'BLOCK': 'block', 'WORD_REPETITION': 'repetition', 'SOUND_REPETITION': 'repetition',
                 'ONSET_PROLONGATION': 'prolongation', 'RHYME_PROLONGATION': 'prolongation',
                 'FILLED_PAUSE': 'filled_pause', 'LOW_EFFORT': 'low_effort', 'TRAILING_OFF': 'trailing_off',
                 'NATURAL_RUSH': 'natural_rush', 'UNEVEN_TEMPO': 'uneven_tempo'}
# (D) Dimensions listed and unscored whatever the validation gates give; the API shows the reason. The name and the
#   strings are inside the detector hash, so a change needs a new calibration.
OWNER_LISTED = {'R1': {'D8': 'owner decision: the RISING_ENDING recipe mostly does not realise; val has 2 eligible ending events'},
                'R2': {'D9': 'owner decision: dev v13 found 0 of 68 R2 rush positives, at one seventh of the local budget'}}


# --------------------------------------------------------------------------------------------- detector hash
# Constants of detector schema 3, in hash order; as_dict adds the later constants of schema 4.
_DETECTOR_KEYS = (
    "DIMS", "DIM_LABEL", "DIM_BRIEF", "DIM_UNIT", "REGIMES", "REGIME_DIMS", "FLAG_SIGNS", "CLIP_DIMS", "SR",
    "STEREO_SIDE_DB", "MAX_UPLOAD_BYTES", "MAX_UPLOAD_S", "DECODE_TIMEOUT_S", "THREAD_ENV", "TORCH_THREADS",
    "POOL_WORKERS_PER_GPU", "POOL_MAX_CPU_WORKERS", "POOL_TORCH_THREADS", "SEED", "WIN", "HOP", "HOP_S", "NFFT",
    "LEVEL_EPS", "MIN_VOICED_REF", "F0_PASS1", "F0_FLOOR_MIN", "F0_FLOOR_Q25_FACTOR", "F0_CEIL_MAX", "F0_CEIL_Q75_FACTOR",
    "F0_FALLBACK", "F0_MIN_FIRST_PASS", "F0_MEDIAN_FRAMES", "PRAAT_AC", "N_MEL", "MEL_FMIN", "MEL_FMAX", "N_CEPS",
    "DELTA_HALF_WIDTH", "MEL_LOG_EPS", "MIN_VOICED_WORD", "REGION_MAX_EXT_S", "REGION_SHARE_BELOW_S", "STRESS_P_MIN",
    "STRESS_SIGMA_FLOOR", "MAD_SCALE", "CTC_FRAME_S", "CTC_STRIDE", "CHUNK_S", "CONTEXT_S", "CHECKPOINT_NAME",
    "CHECKPOINT_SHA256", "CHECKPOINT_BYTES", "LOW_COMPAT_NOTICE", "MEAN_COMPAT_MIN", "PAUSE_MIN_S", "PAUSE_FRAC",
    "PAUSE_CLIP_DB", "PAUSE_Q", "PAUSE_PEAK_Q", "PAUSE_PEAK_DB", "PAUSE_BRIDGE_FRAMES", "WINDOW_WORDS", "WINDOW_MIN_WORDS",
    "D3_MIN_VOICED_FRAMES", "RANGE_REG_ST", "PAUSE_DROP_MIN_BASE_S", "FLOORS", "Q68", "HYSTERESIS_LOW",
    "REGION_PEAK_FRACTION", "MIN_REGION_WORDS", "H_GRID", "R1_H_RANGE", "MIN_MEASUREMENT_COVERAGE", "DIFFERENCE_H",
    "MAX_DIFFERENCES", "FALSE_RATE_BUDGET", "CLIP_LN", "CLIP_H", "X_SAT", "R2_SAT_THRESHOLD_FACTOR", "CLIP_SAT",
    "PMAX_START", "PMAX_FACTOR_GRID", "GATE_IDENTITY", "GATE_L1_MIN", "GATE_G5_MAX", "FLAW_TYPES", "FLAW_DIM", "LEVELS",
    "LEVEL_PARAM", "PAUSE_FLOOR_S", "EXPECTED_SECONDARY", "SPAN_WORDS", "EDIT_GAP_WORDS", "COVERAGE_CAP", "PRAAT_SEED",
    "PSOLA_F0", "PSOLA_STEP_S", "WSOLA_FRAME_MS", "WSOLA_TOL_MS", "XFADE_S", "SPLICE_FADE_S", "WSOLA_MIN_PIECE_S",
    "INSERT_MIN_GAP_S", "PAUSE_FADE_S", "FLATTEN_RAMP_S", "DEEMPH_RAMP_S", "DEEMPH_MAX_RATE", "DEEMPH_MAX_GAIN_DB",
    "FADE_RELEASE_S", "FADE_RAMP_FRACTION", "MUMBLE_NFFT", "MUMBLE_HOP", "MUMBLE_SIGMA_MS", "MUMBLE_MAX_GAIN_DB",
    "ROOM_TONE_GUARD_S", "ROOM_TONE_MIN_S", "ROOM_TONE_XFADE_S", "ROOM_TONE_DB_SPREAD", "G5_FADES", "G1_TYPE", "G3_TYPES",
    "SINGLE_LEVEL_SETS", "CROSS_SPEAKER_CLIPS", "CHAIN_B_TYPES", "PLACEBO_SEEDS", "PASSAGE_S", "PASSAGE_TARGET_S",
    "SENTENCE_COVERAGE_MIN", "PASSAGE_CONTEXT_S", "CLIP_PAD_S", "ABBREVIATIONS", "IOU_MIN", "EVENT_TOL_S",
    "PAUSE_DIAGNOSIS_FRACTION", "HEADLINE_LEVELS", "RULE_OF_THREE", "GAIN_DB", "LOWPASS_HZ", "NOISE_SNR_DB", "MP3_KBPS",
    "COMPRESSION", "SPEAKER_TRANSFORM", "RANDOM_SEEDS", "DEVICE_AGREEMENT_CLIPS",
)


def _plain(v):
    if isinstance(v, (tuple, list)):
        return [_plain(i) for i in v]
    if isinstance(v, dict):
        return {str(k): _plain(i) for k, i in v.items()}
    return v


def _released_dict() -> dict:
    """Schema-3 constants: the detector of the eight core types on D1-D6. They keep the core-8 label bytes (flaws)
    unchanged."""
    core_dims = ("D1", "D2", "D3", "D4", "D5", "D6")
    out = {k: _plain(globals()[k]) for k in _DETECTOR_KEYS}
    out["DIMS"] = list(core_dims)
    out["CLIP_DIMS"] = [d for d in out["CLIP_DIMS"] if d in core_dims]
    out["REGIME_DIMS"] = {r: [d for d in dims if d in core_dims] for r, dims in out["REGIME_DIMS"].items()}
    for name in ("DIM_LABEL", "DIM_BRIEF", "DIM_UNIT", "FLAG_SIGNS", "FLOORS", "REGION_PEAK_FRACTION", "MIN_REGION_WORDS",
                 "CLIP_LN", "X_SAT", "CLIP_SAT", "PMAX_START"):
        out[name] = {d: v for d, v in out[name].items() if d in core_dims}
    out["FLAW_TYPES"] = list(CORE8_TYPES)
    for name in ("FLAW_DIM", "LEVEL_PARAM"):
        out[name] = {t: out[name][t] for t in CORE8_TYPES}
    out["EXPECTED_SECONDARY"] = {t: [d for d in out["EXPECTED_SECONDARY"][t] if d in core_dims] for t in CORE8_TYPES}
    return out


_LEGACY_CONFIG = _released_dict()


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
