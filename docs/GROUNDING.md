# Grounding in prior work

This file gives, for each delivery dimension (D1 to D9) and each flaw family that Contrastive Voice measures, the chain from the literature to the frozen detector and to what the final evaluation shows:

1. **Flaw.** The source that names the delivery problem.
2. **Causes and patterns.** The causes the literature gives for the flaw, and the pattern each cause leaves in the signal, from that cause's own literature.
3. **Method.** The source that gives the detection or measurement method for that pattern. It is often in another field.
4. **System.** The module and function of `src/cvoice/` that implement the measure, with the frozen thresholds.
5. **Evaluation.** What the final evaluation shows, as a number with its source, and the regime it measures.

It describes the frozen detector: `models/detector.json`, sha256 d5935d3f…, detector config 782d7df7…, evaluated once on the test split and the R2 lockbox in the final run (Kaggle kernel v19, 2026-10-07 IST).

## How to read this file

**Two regimes. Their numbers are never pooled.**
- **R1, same recording.** A clean recording is compared with a copy of itself that carries synthetic edits at known places. R1 numbers measure recovery of synthetic edits.
- **R2, different speaker.** A recording is compared with a different reader of the same text. Every upload is analysed in R2 (`src/cvoice/app.py`, `UPLOAD_REGIME = "R2"`). The R2 positives come from 3 development check readers; the R2 lockbox measures false regions only (stated limit 8).

**Two F1 accountings.** Wherever an F1 appears, the pre-registered accounting (all predictions counted) comes first. The one-detection-per-change accounting follows; it was introduced after the evaluation plan. Per-type detection counts below are under the one-detection-per-change rule; where the pre-registered count differs, both are given.

**Earlier look at the test split.** The test split was also scored once in an earlier final evaluation (2026-10-02, config 32cdd86f…, no speech-tempo key, all predictions counted): core-8 test F1 0.879 (TP 29, FP 5, FN 3). That result was seen before the redesign. Its files are kept in `docs/evidence_final_32cdd86f3d6e/`.

**What a citation supports.** Each chain carries one tag per link:
- **[motivates]**: the paper is the reason for a choice. It did not test this system, this population or this form of the measure.
- **[method]**: the paper defines or validates the measurement method in its own population. This system has not repeated that validation.
- **[validated here: …]**: a number from this project's evaluation. The tag states the regime and whether the edits were synthetic or real.

No listener has rated the generated clips. No human marked flaws in these recordings. Every citation therefore motivates or defines a method; none validates a threshold, a severity value or a fix sentence of this system.

**Rules followed.** Every cited work is recorded as read in a research report under `build/work/research/` (the `*/REPORT.md` files and `chain/**`). Each claim is the claim that report attributes to the work. Read status (full text, abstract, secondary) is in the reference list and in `docs/PAPERS.md`. Numbers measured by this project are traced in `docs/NUMBERS.md`.

**Short names for sources of numbers.** Paths are under `build/work/kaggle_runs/last_run/x/` unless they start at the repository root.

| Short name | File |
|---|---|
| R | `eval/results.json` |
| A | `eval/addendum.json` and `eval/addendum.md` (computed after the final evaluation from saved outputs; its CPU re-run reproduces the saved counts in 24 of 24 rows) |
| T | `eval/tables.md` |
| D | `models/detector.json` (byte-identical to the repository `models/detector.json`) |
| K | `calibration/report.json` |
| M | `data/dataset/manifest.json` |
| L | `build/work/critics/last_run_limits.md` (stated limits, numbered as there) |

**Thresholds.** A physical threshold is h × scale. Both come from D: `regimes.R1.h`, `regimes.R1.scales`, `regimes.R2.*` (single reference) and `regimes.R2_consensus.*` (median of five references).

## Summary

| Dim | Flaw named by | Cause → pattern used | Method source | Module.function | R1 (same recording, synthetic edits; L2+L3 detected, train / val / test) | R2 (different speaker) |
|---|---|---|---|---|---|---|
| D1 Pace | [1–4, 6] | fast or slow reading → local tempo change [15, 16] | speech time without pauses [14]; same-text comparison [17, 26] | `compare.d1_pace` | RUSH 10/10, 4/4, 4/4; DRAG 10/10, 4/4, 4/4 | scored; check readers L3: RUSH 1/18, DRAG 6/17 |
| D2 Pauses | [4, 5] | planning, retrieval, fast reading → inserted or removed silence [15, 37, 38] | acoustic silence ≥ 0.20 s [30–32] | `compare.d2_pauses` | PAUSE_DROPPED 10/10, 4/4, 4/4; PAUSE_INTRUSIVE 10/10, 4/4, 4/4 | scored; L3: dropped 4/17, intrusive 14/18 |
| D3 Pitch range | [1–4, 6] | low arousal, second-language reading → compressed span [49, 54] | percentile range in semitones [41, 43] | `compare.d3_pitch` | MONOTONE 9/10, 4/4, 2/4 | scored; L3: MONOTONE 17/18 |
| D4 Emphasis | [4, 7] | no focus marking → flat prominence [56, 59] | equal-weight prominence z-sum [57, 58] | `compare.d4_emphasis` | DEEMPHASIS 7/10, 4/4, 3/4 | not scored |
| D5 Volume | [1, 2, 4, 8] | low effort, recording chain, trailing off → level drop [67–71] | level relative to own median [66] | `compare.d5_volume` | FADE 10/10, 2/4, 4/4 | scored; L3: FADE 13/18 |
| D6 Clarity proxy | [1–4] | hypo-articulation → bundle of changes [73–75] | none validates this proxy | `compare.d6_clarity` | MUMBLE 10/10, 4/4, 4/4 | not scored |
| D7 Word time | [1, 3] | stuttering, planning → repetition, prolongation, block, filler [78–82] | duration ratio, decode insertions, stability run [83–86] | `compare.d7_word_time`, `patterns.word_time` | listed, not scored | listed, not scored |
| D8 Sentence ending | [4, 119] | uptalk, unskilled reading → final rise, weak fall [95, 96] | final pitch change [95, 98] | `compare.d8_ending` | listed, not scored | listed, not scored |
| D9 Speech tempo | [4] | natural rushing → faster words, fewer pauses [15, 16] | articulation-rate decomposition [19, 20] | `compare.d9_speech_tempo`, `patterns.natural_rush` | NATURAL_RUSH 2/10, 1/4, 1/4 | listed, not scored |

Sources of the counts: R1 per type, R `headline.groups.<tier>.magnitude` (L2+L3, status "measured"); R2, R `cross_speaker.modes.single.by_type` and A `r2_by_reader.single` (check readers, single reference, level 3). Under the pre-registered accounting, RUSH is 8/10 on train and 3/4 on test, because 2 and 1 of those detections are same-change detections by D9 (A `count_once_rule` table).

A finding common to all dimensions: no judging instrument that was read gives a numeric threshold; levels are separated by words such as "occasional" and "frequent" [3] (RE §2.3). Every number in the detector therefore comes from reader pairs, from the labelled synthetic edits, or is a declared design value.

## 1. Pace (D1)

**Flaw.** The Public Speaking Competence Rubric puts "poor pacing" at its lowest level [1, 2]. The Competent Speaker form scores "vocal variety in rate, pitch, and intensity" [3]. Poetry Out Loud: "A recitation that is at a too slow or hurried pace … will obscure a poem's meaning"; NSDA: "If your speech is too fast paced, your audience won't catch a word you say" [4]. In a listening experiment, a 5 % faster rate together with shorter hesitation pauses raised the ranking of the lowest-rated political speaker; rate weighed less than pitch dynamics and fluency (12 listeners) [6].

**Causes and their patterns.**

| Cause | Pattern | Sources |
|---|---|---|
| Deliberate fast or slow reading, time pressure | Articulation rate up 13 % and 18 % in two of three readers, about 0 % in the third; speaking rate up to 28 %; pauses deleted or shortened | [15] |
| Natural fast speech | Not a uniform compression: "durations of unstressed syllables in polysyllabic words are reduced more than those of stressed syllables"; listeners preferred linear compression | [16] |
| Nervousness | No source opened reports faster articulation. Speakers with social phobia paused more often and longer in public speaking (abstract) [21]; share of silence correlated r = .36 with state anxiety (Laukka et al. 2008, reported in [22]); "No consistent acoustic patterns were identified for fear or anxiety" [23] | [21–23] |
| Processing difficulty | Local: longer durations of low-probability words in reading aloud [24]; a pause is more likely before a low-frequency word [25] | [24, 25] |
| Low reading skill | "Reads primarily word-by-word" (NAEP level 1) | [27] |

Habitual rate differs between speakers: read sentences 3.40 syllables/s, SD 0.42 across speakers [18]. "Durations of comparable runs of different talkers are highly correlated" on the same text [17], which supports comparing two readers run by run on one text.

**Method.**
- Speaking rate includes pauses; articulation rate excludes them [14] [method].
- The just-noticeable difference for speech tempo is about 5 % in Dutch read speech [13] [motivates the floor].
- Comparison with a fluent reading of the same text, word by word: "simply compute the correlation between the two contours" of word latency and duration [26] [method, children].

**System.**
- `compare.d1_pace`: ln ratio of speech time (aligned word span minus acoustic pauses; `compare.paired_speech_time`, `features.speech_time_ratio`) in a centred five-word window (`features.windows`, `WINDOW_WORDS = 5`), participant over reference, minus the clip median. The clip median is kept as the whole-clip tempo g.
- `detect.decode_dim` finds regions; `detect.clip_flags` gives the whole-clip flag.
- R1 threshold 0.205 ln (×1.227 slower, ×0.815 faster); whole-clip ln 1.25 (D `regimes.R1.h`, `.scales.D1`, `.clip.D1`).
- R2 single reference: ×2.194 slower, ×0.452 faster; whole clip 0.612 ln, ×0.542 to ×1.844 (D `regimes.R2`; L 11). Median-of-five mode: ×2.052 and ×0.581 (D `regimes.R2_consensus`).

**Evaluation.**
- [validated here: R1, synthetic] RUSH 10/10, 4/4, 4/4 and DRAG 10/10, 4/4, 4/4 at L2+L3 (R `headline.groups.core8.magnitude`). Pre-registered RUSH: 8/10 train, 3/4 test (A `count_once_rule`). Level 1, test: RUSH 2/2, both by same-change D9 regions, so 0/2 under the pre-registered accounting; DRAG 0/2 (R `headline.groups.core8.magnitude`; A `count_once_rule`).
- [validated here: R1, synthetic] Edge placement: both edges within 0.20 s for 4 of 7 RUSH and 4 of 8 DRAG regions, val and test (R `headline.groups.core8.grounding`, split val+test; L 16).
- [validated here: R2, development check readers] RUSH level 3: 1 of 18; level 2: 0 of 13; DRAG level 3: 6 of 17 (R `cross_speaker.modes.single.by_type`; A `r2_by_reader.single`; L 8, L 11). Whole-passage rush, single reference: L1/L2/L3 0/1/11 of 18 (R `cross_botched.ladder`).
- [validated here: R2 lockbox nulls] D1+ 0.082 and D1- 0.100 false regions per comparison-minute, equal source weights, against a per-key share of 0.083 (R `lockbox.modes.single.local_by_key`).

**What the citations do not support.** [13] is a whole-utterance tempo threshold; no source gives a perceptual threshold for a local tempo change inside a sentence (PP §5 item 3). The R2 thresholds are set by differences between readers of one text; they are far above any perceptual value and reflect reader-to-reader variation (L 11). The timing values rest on forced-alignment boundaries and pick up aligner errors from non-timing changes (L 4).

## 2. Pauses (D2)

**Flaw.** Poetry Out Loud: "Decide whether the pauses come in suitable places"; UIL: "Was there sufficient variety in rate, pause, and pitch?" [4]. The mean duration of silences inside clauses correlated with human holistic public-speaking scores at |r| = 0.479 (impromptu task, n = 28) [5]. Professional reading had a silence-to-speech ratio of 9 % against 28 % for non-professional reading (Swedish) [11]. Prepared political speeches had 50 % more silent-pause time than interviews, mostly at clause or phrase boundaries (abstract) [12].

**Causes and their patterns.**

| Cause | Pattern | Sources |
|---|---|---|
| Normal planning at boundaries | Skilled adult readers: long pauses at sentence ends (mean 446 ms), commas mean 59 ms (range 0–454 ms) | [36] |
| Retrieval difficulty, online planning | Pauses in the middle of clauses rather than at their end; within-clause silent pause rate had the strongest correlation with rated fluency (second-language spontaneous speech, not read text; VF §1) | [37, 38] |
| Low reading skill | Within-sentence pauses 688 ms in the slowest quartile against 313–365 ms (children) | [39] |
| Fast reading | Fewer pauses in two of three readers; mean pause duration −13 % in two readers | [15] |
| Breathing | Reading: inter-breath pause mean 0.64 s (0.25–1.8 s); 1.8 % of breaths at ungrammatical places | [34] |
| Listener side | Silences inside fluent newsreader speech of 57 / 117 / 212 / 403 ms were judged disfluent in 12.5 / 34.4 / 71.9 / 93.8 % of samples | [33] |

**Method.**
- Pause durations are log-normal; brief under 200 ms, medium 200–1000 ms, long over 1000 ms "only in spontaneous speech"; English read speech median 493 ms, modes 126 and 512 ms [30] [method].
- Published silent-pause thresholds run from 100 to 1000 ms; 250 ms is the classic convention [31] [method].
- 0.2 s is "a common practical threshold because shorter silences are difficult to distinguish from stop closures" [32] [method].
- CTC word spans are shorter than hand labels (177 ms against 241 ms mean on Buckeye), so the gap between two aligned words overstates silence [100] [motivates measuring silence acoustically].
- A pause of 250 ms or more as breath candidate: 13.6 % of such pauses were not breaths [35] (VF §1) [motivates; not used].

**System.**
- `align.acoustic_pauses` with `align.pause_threshold`: the longest acoustically silent run of at least 0.20 s (`PAUSE_MIN_S`) inside each inter-word gap.
- `compare.d2_pauses`: x = participant minus reference silence at each word boundary, in seconds. A shortened pause counts only where the reference pause is at least 0.5 s (`PAUSE_DROP_MIN_BASE_S`, near the 512 ms mode of [30]). A lengthened pause counts only where the reference has none and the transcript has no punctuation (the within-clause pattern of [37, 38]).
- Scales are fitted per sign from countable units only (`detect.fit_scales`).
- R1 threshold 0.3225 s for both signs (D `regimes.R1`). R2 single reference: +0.981 s inserted, −1.504 s removed; median of five: +1.008 s, −0.805 s (D `regimes.R2`, `regimes.R2_consensus`).

**Evaluation.**
- [validated here: R1, synthetic] PAUSE_DROPPED and PAUSE_INTRUSIVE 10/10, 4/4, 4/4 at L2+L3 (R `headline.groups.core8.magnitude`). Level 1, test: PAUSE_DROPPED 2/2, PAUSE_INTRUSIVE 1/2.
- [validated here: R1, synthetic] Over the 16 val and test pause events, median edge error 10 ms at the onset and 29 ms at the offset; largest 128 ms and 149 ms (R `headline.groups.core8.pause_localisation`; L 16).
- [validated here: R2, development check readers] Level 3: dropped pause 4 of 17, inserted pause 14 of 18 (R `cross_speaker.modes.single.by_type`; L 8).
- [validated here: R2 lockbox nulls] D2+ 0.069, D2- 0.010 false regions per comparison-minute (R `lockbox.modes.single.local_by_key`).
- [validated here: R1 stress, synthetic transforms] Babble at 10 dB SNR adds D2- regions at 9.73/min in val (eisenhower 11.97, lbush 7.47) and 11.5/min in test (mobama 10.24, nixon 12.72) (R `stress.rows[…].added_by_key`; A `stress_by_speaker`; L 17).

**What the citations do not support.** [33] measured silences stretched together in newsreader speech, not a single inserted pause. "Suitable places" is reduced to punctuation and the reference's own pauses; a pause before a noun, verb or adverbial phrase is "appropriate" by [34] but is treated as inserted when the reference has none (PP §3).

## 3. Pitch range (D3)

**Flaw.** Lowest rubric level: "speaks in monotone" [1, 2]; the Competent Speaker form expects a voice "varied in pitch to enhance the message" [3]; NSDA: "if it's monotonous, your audience won't recall a word you said" [4]. Among Swedish parliamentary speakers, "monotonous" correlated r = −.91 with good-speaker ratings, and pitch range r = .61; in resynthesis, wider pitch dynamics was the strongest of three cues [6].

**Causes and their patterns.**

| Cause | Pattern | Sources |
|---|---|---|
| Second-language reader | Whole-passage span compressed: SD/mean 0.134–0.146 in first-language reading against 0.118–0.133 in second-language reading | [49] |
| Low arousal, depression | "A decrease in f0 and f0 range in depressed individuals has repeatedly been observed" | [54] |
| Nervousness | Mean F0 raised in 15 of 19 studies; no opened source shows a narrower range | [23] |
| Unskilled or unengaged reading | Contour does not follow a skilled reading of the same text | [26, 53] |
| Sing-song, repeated contour | Range normal; a slow rise and a repeated up-down "yield exactly the same result" in long-term measures | [51] |

**Method.**
- Semitones relative to the speaker give "a kind of perceptual speaker normalization"; a tested feedback measure is the SD of pitch in semitones over a moving 10 s window [41] [method]. Listeners judge F0 intervals equal when they are equal in semitones (abstract) [55] [method].
- The 80-percentile range (P90 − P10) correlated .52 with charisma ratings on 40–98 s excerpts, against .35 for SD and .04 for max − min [43] [method]. Tracking errors inflate SD, and percentile ranges are more robust to them [52] [method].
- A numeric cut-off exists: PVQ below .15 over 10 s was "generally rated as on the monotone side" [42]. First-language read text sits at 0.134–0.146 [49], so the cut-off does not transfer to read passages (PE §2.1).
- Pitch-distance differences are discriminated at 1.5–2 st; "only differences of more than 3 semitones play a part in communicative situations" (abstract) [40] [motivates the 1 st regularisation].
- Tracker: Praat autocorrelation [44], floor and ceiling from the recording's own quartiles [45]; long-term F0 averages settle after about 10 s [46]. F0 frame error of Praat with default settings 7.05 %, 6.20 % with a sex-adapted range [47]; 5.05 % on clean speech, another tracker better on real noisy speech [48] [method].

**System.**
- `features.pitch_track` (two-pass Praat F0 through parselmouth; pass 1 60–700 Hz, pass 2 floor max(50, 0.75 Q25), ceiling min(800, 1.5 Q75)); `features.frame_features` gives semitones relative to the recording's median voiced F0.
- `features.make_recording`: `win_R` = P90 − P10 of voiced semitone frames in each five-word window, with at least 50 voiced frames.
- `compare.d3_pitch`: ln((P + 1 st) / (B + 1 st)) per window, minus the clip median; only a narrower range is flagged. The clip median is the whole-clip pitch-range ratio g.
- R1 threshold 0.723 ln: (range + 1 st) below ×0.485 of the reference's, after the clip ratio is removed; whole clip ln 2 (range halved). R2 single: ×0.273; whole clip 0.702 ln; median of five: ×0.303 (D `regimes.R1`, `regimes.R2`, `regimes.R2_consensus`).

**Evaluation.**
- [validated here: R1, synthetic] MONOTONE 9/10, 4/4, 2/4 at L2+L3 (R `headline.groups.core8.magnitude`). Test D3- is the lowest core key in test: F1 0.5 (TP 2, FP 2, FN 2), equal under both accountings because no duplicate or same-change detection involves D3- (R `headline.groups.core8.by_split_strict`, split test, group D3-).
- [validated here: R1, synthetic] Edge placement: 0 of 6 matched regions with both edges within 0.20 s in val and test; onset error 90th percentile 867 ms (R `headline.groups.core8.grounding`; L 16). Lowest internal-consistency ratio: test MONOTONE L3, median paired ratio 0.436 (T "Feature internal consistency").
- [validated here: R2, development check readers] MONOTONE level 3: 17 of 18 (R `cross_speaker.modes.single.by_type`). Whole-passage monotone, single reference, L1/L2/L3: 14/18/18 of 18 (R `cross_botched.ladder`).
- [validated here: R1 stress] Phone band with mu-law adds D3- regions at 2.84/min in test (mobama 0.139, nixon 5.53) (R `stress.rows`; A `stress_by_speaker`).

**What the citations do not support.** No opened study validates a percentile range on a five-word window; the validated windows are 10 s [41, 42] and 40–98 s [43] (PE §4). Centring on the clip median removes the whole-passage compression that [49, 54] describe; that pattern rests on the separate whole-clip check. Percentile spans were the weakest family against listener judgements in [50], and they cannot see contour shape [51]. Contour placement ("pitch match" [26, 53]) is not built.

## 4. Emphasis (D4)

**Flaw.** Toastmasters: a voice "moving from one pitch level to another for emphasis" [4]. With correct primary stress, listeners "recalled significantly more content and evaluated the speaker significantly more favorably than when primary stress was aberrant or missing" (abstract) [7].

**Causes and their patterns.**

| Cause | Pattern | Sources |
|---|---|---|
| No focus marking (disengaged or low-skill reading) | "the overall prominence variation pattern is more flat and less similar to the native realization" | [59] |
| How focus is realised | Expanded pitch range on the focused syllable, suppressed range after it, longer stressed syllable | [56] |
| Stress on the wrong word | "content words are much more likely to be accented than function words"; given entities "need not be prominent" | [64] |

**Method.**
- Equal-weight z-sum of F0, energy and duration, word maximum: 79.2 % accuracy on read news; the wavelet version 84.6 % [57]. Tuned weights gain about 0.7 points over equal weights [58] [method].
- Cue weights disagree by corpus: loudness and duration stronger than F0 (abstract) [61]; spectral balance carries lexical stress and F0 excursions carry accent [60]; spectral tilt ranks last or adds little in three of four sources [62, 63] (PE §2.2) [motivates equal weights].
- Listener agreement on prominence is limited: Fleiss kappa .373–.421 [65] [motivates caution].

**System.**
- `features.word_stats`: per word, ln duration per syllable, P90 semitones, P90 level.
- `features.stress_reference`, `features.stress_points`: mean of the three robust z-scores against the recording's own medians and robust scales (the participant uses its own medians and the reference's scales).
- `features.stress_words`: a stress point is a local maximum with p ≥ 0.75 (`STRESS_P_MIN`).
- `compare.d4_emphasis`: change of p at the reference's stress words; only a loss is flagged. R1 only: threshold 1.075 p-units (D `regimes.R1`). D4 is shown and not scored in R2 (`REGIME_DIMS`).

**Evaluation.**
- [validated here: R1, synthetic] DEEMPHASIS 7/10, 4/4, 3/4 at L2+L3 (R `headline.groups.core8.magnitude`).
- [validated here: R1, synthetic] The shown cause label is DEEMPHASIS for 4 of 7 detected val and test deemphasis edits; 2 are shown as MONOTONE and 1 as RUSH (A `labels`; L 18).
- MISPLACED_EMPHASIS (synthetic-only recipe, D4 primary): 1/9, 1/4, 1/4 at L2+L3, shown as DEEMPHASIS (R `headline.groups.synthetic_only.magnitude`; A `labels`). The two-sided check (D4+) failed its lab gate for lack of labels, so only losses are flagged (`build/work/design/LAB_DECISIONS.md`).

**What the citations do not support.** There are no human stress labels for these recordings; a stress point is an acoustic prominence candidate. [57] scored read news against labels, not a single reference reading. Emphasis edits are placed on words the detector's own statistic marks as stressed.

## 5. Volume (D5)

**Flaw.** NSDA: "Is the volume appropriate?"; "Every word you deliver should come across loud and clear" [4]. Public Speaking Competence Rubric: "a voice too soft … for listeners to comfortably hear" (Minimal), "Speaks inaudibly" (Deficient) [1, 2]. Speakers attempting to persuade "speak louder and vary their volume", which signals confidence (abstract) [8]. Mean and SD of intensity correlated with charisma ratings at r = .14 to .35 [9].

**Causes and their patterns.**

| Cause | Pattern | Sources |
|---|---|---|
| Low vocal effort | Level down and spectrum tilts: "when the overall amplitude is increased by 10 dB, A1, A2, and A3 are increased by 11, 12.4, and 13 dB"; F0 and F1 change with effort (abstract) | [67] |
| | Alpha ratio (energy above / below 1 kHz) ranges 19.0 and 11.7 dB over about 28 dB of level, women and men (abstract) | [68] |
| | Listeners tell increased effort from decreased distance on single phonated vowels | [69] |
| Recording chain (distance, gain, AGC) | Level changes; spectral balance and F0 do not | [69]; "it may not be possible to know the exact dB-SPL level since recording levels and an AGC may be used" [72] |
| Trailing off | "the amplitude downdrift which normally accompanies fundamental frequency declination" (abstract) [70]; source strength declines at −7.3 dB/s in short declaratives, with laxer phonation [71] | [70, 71] |

**Method.**
- Level JND for broadband increments 1.5 dB; 3 dB is a noticeable adjustment (hearing-impaired listeners, speech-shaped noise) [66] [motivates the floor of 2 dB].
- Level relative to the recording's own median cancels a uniform gain; time-varying processing is not: "A fixed gain is removable, whereas compression, noise and bandwidth changes are not" (FE §1.3, §3.1 and its summary) [method].
- Spectral balance relative to the speaker's own median separates effort from gain [68, 69] [method; lab test failed here, see below].

**System.**
- `features.frame_level_db` and `features.frame_features`: frame level in dB (25 ms Hann window, 10 ms hop) minus the median over voiced frames.
- `compare.d5_volume`: window mean, participant minus reference, minus the clip median; only a drop is flagged.
- R1 threshold 4.3 dB. R2 single: −10.08 dB; median of five: −9.0 dB (D `regimes.R1`, `regimes.R2`, `regimes.R2_consensus`).
- `patterns.describe` (D5 branch) tests the trailing-off pattern (last-word drop larger than the reference's) and the low-effort pattern (alpha ratio drop ≥ 1 dB, `ALPHA_DROP_DB`). Both labels are switched off, because neither passed its lab gate (D `regimes.R1.pattern_labels`).

**Evaluation.**
- [validated here: R1, synthetic] FADE 10/10, 2/4, 4/4 at L2+L3 (R `headline.groups.core8.magnitude`). Val D5- is the lowest core key in val: F1 0.5 (TP 2, FP 2, FN 2), equal under both accountings (R `headline.groups.core8.by_split_strict`, split val, group D5-).
- [validated here: R2, development check readers] FADE level 3: 13 of 18 (R `cross_speaker.modes.single.by_type`).
- [validated here: R2 lockbox nulls] D5- 0.123 false regions per comparison-minute, above the 0.083 per-key share (R `lockbox.modes.single.local_by_key`; L 12).
- [validated here: R1 stress] Dynamic-range compression adds D5- regions at 2.22/min in val (eisenhower 0.48, lbush 3.96) (R `stress.rows`; A `stress_by_speaker`). This is the limit the feature research named (FE summary and §4 table: "Gain normalization cannot cancel time-varying processing").
- [lab, real contrast, failed] Alpha ratio on AVID soft against normal speech found 0.07 of the contrast items at the 5 % false-flag point (R `real_validation.labels.low_effort`). LOW_EFFORT edits (synthetic-only recipe: gain, tilt and F0 lowering, VC §2.1) are recovered by dimension 5/8 on train and 2/2 on test, and shown as FADE (R `headline.groups.synthetic_only.magnitude`; A `labels`). TRAILING_OFF: 4/10, 0/4, 1/2.

**What the citations do not support.** The rubrics ask about audibility, an absolute property. The level of an upload is unknown, so only a local drop relative to the speaker's own level is measured (VC §2.5). The FADE edit is a gain change: it imitates the recording-chain pattern, not the effort pattern of [67–69] (VC §2.1).

## 6. Clarity proxy (D6)

**Flaw.** UIL: "Was enunciation clear?" [4]. Competent Speaker form: "properly formed sounds" [3]. Public Speaking Competence Rubric: "articulation too indistinct for listeners to comfortably hear" [1, 2].

**Causes and their patterns.** Hypo-articulation: "In conversational speech, vowels are modified or reduced, and word-final stop bursts are often not released" (abstract) [73]. Clear speech at normal rate differs by "increased energy in the 1000–3000-Hz range" and deeper low-frequency envelope modulation (abstract) [74]. The full review lists a bundle: slower rate, wider pitch range, higher level, stop releases, stronger obstruents, 1–3 kHz energy, vowel-space expansion [75].

**Method.**
- No source supports one spectral-change measure as a clarity measure (FE §4) [none].
- The aligned posterior of the known text is a published articulation measure: "GOP-CTC-align" [76]; average posterior of aligned phonemes reached r = 0.71 with rated intelligibility over six pathological datasets [77] [method, not built: the detector does not score it].

**System.**
- `features.mfcc_delta_magnitude`: Q = norm of the frame-to-frame change of cepstral coefficients 1–12 (40 mel filters, 50–7600 Hz).
- `compare.d6_clarity`: ln ratio of window means of Q, minus the clip median; only a reduction is flagged. R1 only: threshold 0.480 ln (×0.619) (D `regimes.R1`). Shown and not scored in R2. The page states beside every D6 flag that it is a spectral-change proxy.

**Evaluation.**
- [validated here: R1, synthetic] MUMBLE 10/10, 4/4, 4/4 at L2+L3 (R `headline.groups.core8.magnitude`); both edges within 0.20 s for 3 of 8 val and test regions (R `headline.groups.core8.grounding`).
- [validated here: R1 stress] Under white noise at 20 dB SNR, D6- keeps 1 of 12 (val) and 3 of 12 (test) detections (R `stress.rows[…].retention_by_key`).

**What the citations do not support.** D6 detects the system's own spectral-smoothing edit. Nothing in [73–75] links it to intelligibility or to a judge's view of enunciation.

## 7. Word time and the disfluency family (D7)

**Flaw.** Public Speaking Competence Rubric: "distracts listeners with fillers" [1, 2]. Competent Speaker form: "nonfluencies and disfluencies interfere with the message" [3].

**Causes and their patterns** (DF §2).

| Cause | Pattern | Sources |
|---|---|---|
| Developmental stuttering | Several rapid repeats of an onset consonant or syllable; prolongation of a continuant ("can exceed 1 s"); block: "a long, tense articulatory closure"; mostly on stressed or utterance-initial syllables; events average about 1 s | [78] |
| Planning and word access (typical speakers) | One repeat, 96 % on function words, first token lengthened [78, 79]; filled pause: schwa-like, low and falling F0, much longer than the same vowel in words [79]; "Um was followed by delays far more often than uh" [81] | [78, 79, 81] |
| Nervousness | Speakers with social phobia paused more often and longer in public speaking (abstract) [21]; fillers rose with evaluation apprehension, not with anxiety in a simple way (abstract) [82] | [21, 82] |
| Cluttering (contrast) | Fast or irregular rate; "oral reading is not useful for differential diagnosis" | [93] |

Base rate: adults who do not stutter, reading a 200-syllable text aloud, 0.21 % stuttered syllables (n = 17) [80]. The clinical sources state that audio alone cannot separate block from pause (annotator kappa 0.25 and 0.37) or prolongation from repetition [87, 88]. A product can label form and size, not cause (DF §2.7).

**Method** (DF §2.6, each validated in another population).
- Filled pause by F0 slope and spectral stability: recall 84.9 %, precision 91.5 %, 10 Japanese speakers [83]; Switchboard, recall 92.86 % at 2.36 % false alarms (preliminary) [84] [method].
- Voiced material that no transcript word accounts for, as filler candidates; with a trained classifier event F1 92.8 % [85] [method].
- Free decode against the known text: wav2vec 2.0 miscue detection recall 0.83 at precision 0.29 in children's reading [86] (VF §2) [method].
- Duration of the same word against the reference reading (DF §4 measure 5) [method, weak as a detector].
- Forced alignment with go-back, part-word and skip arcs: phone-boundary recall 0.47–0.60 on synthetic DisfluenTIMIT, F1 0.53–0.54 on real UCLASS [90] [method, not built: it needs a new decoder].
- Listeners weight repairs less than pauses and speed: pause measures explained 59 %, speed 54 % and repairs 16 % of perceived-fluency variance (second-language spontaneous speech) [94] [motivates reporting disfluency without a score weight].

**System.**
- `features.word_occupancy`: aligned word duration plus orphan voiced time in the preceding gap (`features.orphan_voiced_spans`).
- `compare.d7_word_time`: ln ratio of occupancies with a 20 ms regulariser, minus the clip median; the MAD of x is the whole-clip uneven-tempo measure.
- `patterns.word_time` assigns one label in fixed order: BLOCK (within-word silence ≥ 0.25 s more than the reference), WORD_REPETITION or SOUND_REPETITION (a greedy-decode insertion that copies or prefixes a nearby word; `align.greedy_words`, `features.decode_edits`), FILLED_PAUSE (orphan voiced run ≥ 0.20 s), ONSET or RHYME_PROLONGATION (stability run ≥ 0.20 s), else LENGTHENED_WORD.
- `patterns.describe` switches each label off unless its lab gate passed (`PATTERN_GATES`; D `regimes.R1.pattern_labels`): only FILLED_PAUSE is on, as a candidate label.
- D7 is listed (shown, not scored) in R1 and R2 (`LISTED_DIMS`). Its per-word x also gives the HESITATION evidence of section 10.

**Evaluation.**
- [lab, real contrast, failed] Word-duration ratio on LibriStutter clips: 0.39 found at 0.10 false; orphan voiced gap: 0.34 at 0.07 (R `real_validation.D7+`). LibriStutter is synthetic stuttering built on LibriSpeech [89]. D7 therefore stays listed.
- [lab, real events] Repetition label precision 0.04, prolongation 0.02, block 0 (LibriStutter events): labels off. Filled pause on PodcastFillers events (±0.20 s): precision 0.54, recall 0.15: shipped as a candidate label (R `real_validation.labels`). PodcastFillers is described in [85].
- No R1 or R2 detection number exists for D7, because the key is not scored: "Attempted families with no recovered eligible events: BLOCK, … ONSET_PROLONGATION, … RHYME_PROLONGATION, … SOUND_REPETITION, … WORD_REPETITION" (T "Recovery of the synthetic edit"). R2 check readers, level 3: every disfluency type 0 detected (A `r2_by_reader.single`).
- The disfluency recipes follow published edit recipes [89, 91, 92] (`config.py` constants marked "disfluency REPORT §4"). Their stated limits: waveform edits sound unnatural (opinion score 2.22 against 4.13 for TTS data) [91]; pretraining on artificial prolongations hurt natural prolongation [92].

**What the citations do not support.** Every method above was validated on children, patients, other languages or spontaneous speech, not on fluent adults reading aloud (DF §4). At 0.21 % stuttered syllables [80], any detector with a non-zero false-region rate has a low positive predictive value on fluent readers; T "Select-set promotion" leaves the D7 PPV row empty because no enabled D7 key exists. Whole-word timing has the aligner's 48–89 ms boundary error [100] as a floor.

## 8. Sentence ending (D8)

**Flaw.** In a resynthesis experiment, "falling (vs. rising) vocal intonation at the ends of sentences can signal speaker confidence": the pitch of only the last word was raised or lowered by 35 Hz, and confidence ratings were 5.55 against 4.82; the benefit for persuasion held only for strong arguments [119]. Poetry Out Loud lists "singsong" and "monotone" among the weak descriptors [4].

**Causes and their patterns.**

| Cause | Pattern | Sources |
|---|---|---|
| Uptalk | A late rise on the last word of a statement, often after the vowel; 45 % of floor-holding utterances ended in uptalk | [96] |
| Unskilled reading | Smaller sentence-final pitch change in declaratives (Mandarin-speaking children; the measure predicted reading rate only, VF §3) | [95] |
| No declination | Only 71.5 % of professional read-news phrases have a negative slope; 2.68 st/s at 2 s falling to 1.23 st/s at 4 s | [97] |
| Creak at the end | F0 "typically ranging from 40–70 Hz" | [99] |

**Method.** Sentence-final pitch change around the last word [95] [method, weak]. Features of the final 200 ms classify five boundary tones at 54.95 %, so only the direction is defensible [98] [method].

**System.** `features.final_pitch_word`: median semitones of the last 0.20 s of a sentence-final word minus the median of its earlier part, at "." only. `compare.d8_ending`: participant minus reference. `patterns.describe` labels RISING_ENDING or FLAT_FINAL_FALL. D8 is listed in R1 and R2 by owner decision ("the RISING_ENDING recipe mostly does not realise; val has 2 eligible ending events", `config.OWNER_LISTED`).

**Evaluation.**
- [lab] No real ending labels exist (R `real_validation.D8+`).
- Realisation: 53 RISING_ENDING and 21 FLAT_FINAL_FALL edits did not realise and are excluded from truth (M `realisation_shortfalls`). R2 check readers, level 3: RISING_ENDING 0 of 10 (A `r2_by_reader.single`).

**What the citations do not support.** No published threshold for an uptalk rise in read statements was found (PE §5 item 2).

## 9. Speech tempo and the natural-rushing family (D9)

**Flaw.** "too slow or hurried pace" [4]; "poor pacing" [1, 2].

**Cause and pattern.** A reader who speeds up raises articulation rate by 13 % and 18 % (two of three readers) and gains time by deleting or shortening pauses [15]; natural fast speech shortens unstressed syllables and vowels more than stressed ones [16]. The core RUSH edit compresses words and keeps the pauses; natural rushing compresses the words and shrinks the pauses (SYNTHESIS §1, §4).

**Method.** Decompose tempo into articulation rate, pause count and pause duration against the reference: for read speech, rate of speech correlated 0.90–0.93 with expert fluency ratings (abstract) [19]; articulation rate r = .62 and speech rate r = .76 with rated fluency in a meta-analysis of 22 second-language studies [20] [method].

**System.**
- Recipe (`edits_extra.natural_rushing`): word time shortened by ×1.13, ×1.15, ×1.18 at levels 1–3 (`RUSH_RATE`, "13/15/18 % chosen within that range" of [15]); pauses kept at 0.6, 0.3, 0.0 (`RUSH_PAUSE_KEEP`, design values; no source gives a fraction).
- `features.window_word_time` and `compare.d9_speech_tempo`: ln ratio of summed aligned word durations per five-word window, not centred (owner decision O1: words only, every pause left to D2).
- `patterns.natural_rush`: a D9- region is NATURAL_RUSH only when the reference has at least 0.20 s of paired pause time around its words (two words each side) and the kept pause fraction, participant over reference, is below both the word-time ratio at the peak and 0.775 (`NATURAL_RUSH_PAUSE_KEPT_MAX = sqrt(RUSH_PAUSE_KEEP[0])`). Otherwise `patterns.same_change` and `patterns.rush_type` join it to the RUSH change, with one penalty (`SAME_CHANGE = {'D9-': 'D1-'}`).
- R1 threshold 0.1488 ln (×0.862), h 3.05, which is the lowest grid value above the clean alignment-noise floor of 0.1484 ln (D `regimes.R1.natural_rush_selection`). D9 is listed in R2 (`config.OWNER_LISTED`).

**Evaluation.**
- [validated here: R1, synthetic] NATURAL_RUSH 2/10, 1/4, 1/4 at L2+L3; none of the 4 detections has both edges within 0.20 s (R `headline.groups.lab_passed.magnitude`, `.grounding`; L 1, L 13). Lab-passed tier F1, pre-registered and one-per-change equal: test 0.167 (TP 1, FP 7, FN 3) (A `accounting.rows`).
- [validated here: R1, synthetic] D9 measures 21–67 % of the applied compression (median per split and level; val level 2: 0.208) (R `validity.natural_rush_recovery`; L 1).
- [validated here: R1, synthetic] The RUSH / NATURAL_RUSH label is correct for every detected rush and natural-rush edit and for every D9- region near one, all splits (A `rush_confusion`). The rule constant comes from the recipe parameters (L 18).
- [lab, real contrast, passed, different measure] speech_time_ratio on EARS fast against regular: 0.54 found at 0.03 false, AUC 0.90. The product measure is D9, not speech_time_ratio (R `real_validation.labels.natural_rush.product_measure`).
- [validated here: R1 stress] White noise at 20 dB SNR adds D9- regions at 1.20/min in val (eisenhower 0.55, lbush 1.85) (R `stress.rows`; A `stress_by_speaker`; L 13).

**What the citations do not support.** [15] measured three German readers; [19, 20] are second-language fluency studies. The recipe level 1 and level 2 changes (ln −0.122 and −0.140) are smaller in size than the D9 threshold (0.149 ln), and level 3 (ln −0.166) exceeds it by only 0.017 ln before any measurement loss (L 1).

## 10. Families carried by D2 and D1: hesitation, word-by-word reading, uneven tempo

| Family | Pattern and source | System | Evaluation (R1, synthetic edits, L2+L3, train / val / test) |
|---|---|---|---|
| HESITATION | One word slowed and a silence before it [24, 25]; recipe word ×1.2–1.8, silence 0.2 / 0.5 / 1.0 s ("within-phrase insertion 0.2–1.0 s", PP §4) | D2+ region plus a D7 stretch ≥ ln 1.25 at the next word: `patterns.groups`, `patterns.describe`. Registry primary D2 (decision recorded in `build/work/design/DETECTOR_EXTENSION.md` §2) | 10/10, 4/4, 4/4 by dimension; label HESITATION on 7 of 8 detected val and test edits (R `headline.groups.synthetic_only.magnitude`; A `labels`). R2 check readers level 3: 13 of 18 |
| WORD_BY_WORD | "Reads primarily word-by-word" [27]; recipe silences 0.15 / 0.225 / 0.30 s after each word (PP §4) | ≥ 3 D2+ regions in one sentence form one group: `patterns.groups`, `WORD_BY_WORD_MIN_EVENTS = 3` | 0/58, 0/16, 0/28. The R1 D2+ threshold of 0.3225 s is above every recipe silence (D `regimes.R1`; `READING_PAUSE_S`) |
| UNEVEN_TEMPO | Dispersion of the local tempo ratio along an alignment with a reference: r = .37 alone with human rhythm scores, human agreement .49 [28] | Whole-clip D7 measure (`compare.d7_word_time`, g); not shipped | Lab: EARS fast 0.17, slow 0.35 found; failed (R `real_validation.labels.uneven_tempo`) |
| REPEATED_CONTOUR | Same contour on every sentence; no validating study [42, 51] (PE §5 item 1) | No detector (`FLAW_REGISTRY['REPEATED_CONTOUR']`, primary NO_DETECTOR) | none |

## 11. Cross-cutting parts

### Forced alignment

- **Method.** Published word-boundary error of wav2vec 2.0 CTC alignment: 48 ms on TIMIT read speech, 89 ms on Buckeye; MMS 37 / 53 ms; Montreal Forced Aligner 23 / 41 ms [100]. Word-start error, Montreal Forced Aligner 19.93 / 21.75 ms, MMS 43.06 / 49.54 ms [101]. Word ends within 50 ms on TIMIT: Montreal Forced Aligner 89.4 %, MMS 75.7 %, WhisperX 82.4 % [102]. These studies use different protocols and are not ranked against each other (AL "Published boundary errors").
- **System.** torchaudio `WAV2VEC2_ASR_BASE_960H` emissions and a NumPy CTC Viterbi over the supplied transcript, 20 ms frames (`align.emissions`, `align.ctc_viterbi`, `align.align_emissions`). The lighter model was chosen for installation and CPU cost (AL "Recommendation").
- **Evaluation.** No word boundary in these recordings was marked by hand. A gallery low-effort edit with no timing change was reported as "91 % faster"; a 640 ms word-boundary shift on identical audio samples has no resolved cause (L 4). GPU and CPU alignment of 8 recordings agreed to 0 ms with identical flags (R `device_agreement`).
- **Departure.** Effects of the size of the boundary error, such as phrase-final lengthening of 80 ms [29], are out of reach (SYNTHESIS §2 item 4).

### Reference-relative comparison

- **Flaw side.** Rubrics give no numeric levels, and trained raters disagree most on vocal expression: two expert raters gave the same score on 30 % of presentations [2]; holistic inter-rater ICC 0.385 on 56 videos [5]. Effects in the perception literature are small, language-dependent and reverse at the extremes ("too high-pitched or too fast") [9, 10] (RE §3.4).
- **Method.** Coaching systems compare duration patterns and log-F0 contours of a learner with a reference; treating the exemplar "as a single correct read" over-constrains style [103]. Reference-based prosody evaluation uses speech rate, articulation rate and pause ratio and states that it does "not yet map deviations to perceptual thresholds" [32]. With fewer than 10–20 reference readers, pitch-match features fluctuate substantially [53]. Robust spread = 1.4826 × MAD; modified z-scores above 3.5 are potential outliers [104].
- **System.** Every measure is participant minus reference at the same words; scales are the larger of a floor, 1.4826 × MAD and the 68th percentile of |x| on the regime's nulls (`detect.fit_scales`). R2 nulls are same-text reader pairs from four sources with equal source weights (`calibrate.grouped_nulls`, `calibrate.fit_r2`); uploads with a bank of five references use the median-of-five reference (`reference.select_reference`, `reference.consensus_reference`).
- **Evaluation.** [R1, synthetic] The same detector with the participant's own clip as reference, scored with its own scales and h (added after the final evaluation; one detection per change): core-8 test F1 0.407 (TP 12, FP 15, FN 20), against 0.812 for the detector under the pre-registered accounting and 0.879 under one detection per change (A `baselines`, addendum section 4). [R2 lockbox nulls] Single reference: 0.46 false regions per comparison-minute with equal source weights (0.52 pooled; upper95 0.54); readers whose first language is Amharic (1.28/min) or Arabic (1.00/min) get more (R `lockbox`; L 12).
- **Departure.** NSDA Declamation "is not designed for students to mimic the original author" (RE §2.3). The system measures departure from a reference rendition and cannot say that a departure is an error.

### Controlled edits as flaws

- **Method.** Training on synthetic errors raised pronunciation-error detection on real speech from AUC 0.528 to 0.749 [105]; a learned detector can key on synthesis artefacts ("shortcut learning", abstract) [106]; synthetic dysfluency transfers to real speech only partly [91]. The edit tools are waveform-similarity overlap-add time scaling, Praat PSOLA and the WORLD vocoder (`flaws.wsola`, `flaws.psola`, `flaws.world_flatten`); their original papers are not recorded as read in the research reports and are not cited.
- **System.** Eight core edit types and fifteen extra types at three levels, spliced with exact labels (`flaws.apply_edit`, `edits_extra.py`); identity and placebo clips pass the same processing. The detector is a threshold rule with no trained classifier.
- **Evaluation.** [R1, synthetic] Repair test: undoing the edit removes the flag in val 12/12 and test 10/10, and the placebo keeps it in 12/12 and 10/10 (R `repair.by_type`). Second generator (chain B): 22 = 22 detections over 24 pairs (R `chain_b.rows`).
- **Departure.** [105] supports synthetic errors for learned models tested on real speech; this build has no real-flaw test for the core types, so that support does not transfer (L 18).

### Event-based evaluation

- **Method.** In sed_eval an event matches when onset agrees within 0.2 s and offset within the larger of 0.2 s and half the event length [107]. Collar and operating-point choices change event scores [108]. Scoring a whole labelled region as found after one hit inflates results [109]. Selection on a small test set overfits [110].
- **System.** One-to-one matching, IoU ≥ 0.5 for windows, labelled boundary or word for pause and emphasis events, both edges within 0.20 s for D7 and D8 (`events.match`, `events.eval_clip`; `IOU_MIN`, `EVENT_TOL_S`). No point adjustment.
- **Evaluation.** Core-8 test F1, levels 2–3, pre-registered accounting 0.812 (TP 28, FP 9, FN 4; per speaker 0.800 and 0.824); one detection per change, introduced after the plan, 0.879 (per speaker 0.848 and 0.909). These are ranges over 2 speakers, not confidence intervals. The test split was scored once before under config 32cdd86f…: 0.879 (29/5/3) (A `accounting.rows`; L 19).

### Explanations

- **Method.** Feedback should state the goal, the current state and the next step (meta-analysis of 435 studies) [111]; more than a third of feedback interventions lowered performance (abstract) [112]; focus on the task, be specific, be cautious with overall grades [113]; sparse feedback was preferred to continuous (abstract) [118]. Accepted explanations are contrastive and select one or two causes [114]; a counterfactual states what would need to change (abstract) [115]. A claim at one level of the causal hierarchy needs evidence from that level [116]. LLM output is not repeatable at settings called deterministic (abstract) [117].
- **System.** Template text per finding from measured values (`explain.py`); "score with this penalty removed" is arithmetic on the score function (`score.py`). One change, one cause, one penalty (`patterns.groups`, `patterns.counted`). No language model is used.
- **Evaluation.** [R1, synthetic] The shown cause label equals the injected type for 56 of 59 detected core-8 edits in val and test; 7 of 13 for detected synthetic-only edits (A `labels`; L 18). No listener rating exists (T "Expectation table").

## 12. Where the system departs from the sources

1. The R2 thresholds (pace ×2.19 / ×0.45, dropped pause 1.50 s, single reference) are set by reader-to-reader variation and are far above the perceptual values in [13, 40, 66] (L 11).
2. The D2+ threshold in R1 (0.3225 s) is above the silences that listeners judged disfluent in 72 % of samples (212 ms) [33], and above every word-by-word recipe silence.
3. The pitch measure is a percentile-range ratio over five words; the validated windows are 10 s and longer [41–43].
4. Emphasis uses equal weights for three cues; spectral balance is not used. For read English this is defensible by [57, 58, 62, 63].
5. Clarity is one spectral-change proxy; the literature treats clear speech as a bundle [73–75], and the published articulation measure [76, 77] is not scored.
6. The aligner is the wav2vec 2.0 base model, with a published word-boundary error of 48–89 ms [100], not the more accurate Montreal Forced Aligner [101, 102].
7. One reference rendition is the comparison point (five in the median mode), against the 10–20 readers that [53] found necessary.
8. The natural-rushing evidence measured speech_time_ratio; the product measures D9.
9. Disfluency (D7) and sentence endings (D8) are measured and listed; neither is scored, and only the filled-pause label passed a real-data test.
10. An overall score is shown although [113] advises caution with grades; the per-finding penalty is shown beside it.

## 13. Stated limits that bear on these chains

The full agreed wording is in `build/work/critics/last_run_limits.md` and in the technical report. The opening sentence of each, verbatim:

| L | Chains | Opening sentence |
|---|---|---|
| 1 | D9 | "Speech tempo (D9) cannot separate mild natural rushing from alignment noise." |
| 4 | D1, D2, D9, alignment | "Pace, pause and speech-tempo values come from forced-alignment word boundaries." |
| 8 | D1–D5 in R2 | "Different-speaker (R2) detection has no held-out positive test." |
| 11 | D1, D2, regimes | "Every upload is compared as a different performance (R2)." |
| 12 | R2 false regions | "On held-out readers of the same texts (lockbox: Accent Archive and poetry readers only), the single-reference mode gives 0.46 false regions per comparison-minute with the two sources weighted equally (0.52 pooled; bootstrap upper95 0.54)." |
| 13 | D9 | "Speech tempo (D9) finds 2/10, 1/4 and 1/4 natural-rush edits (train/val/test, levels 2–3), with coarse edges." |
| 16 | all windowed keys | "Pause findings are placed close to the edit." |
| 17 | stress | "All stress conditions are synthetic transforms of the same recordings." |
| 18 | labels, explanations | "Scores and cause labels are validated only against synthetic edits whose cause is known." |
| 19 | evaluation | "Test F1 (core 8, levels 2–3) comes from 2 speakers." |

## References

Style: authors by surname, year, title, venue, identifier, read status, report. Bibliographic fields of the chain-report sources are taken from the report's reference list or its `sources/<key>.txt` file. The first-round reports (RE, FE, AL, GM) cite most sources by link or DOI; their remaining fields (author lists, titles, pages) are those confirmed against Crossref, arXiv, the ISCA archive or the publisher on 2026-10-02 for the earlier version of this file.

Read status: **full** = full text read; **full-F** = full text read through a fetch tool, numbers marked "to re-check" by the report; **abstract** = abstract only; **secondary** = read through the named source; **metadata** = bibliographic record only. Report keys: RE `rubric_explain/REPORT.md`, FE `features/REPORT.md`, AL `alignment/REPORT.md`, GM `grounding_model/REPORT.md`, PP `chain/pace_pauses/REPORT.md`, DF `chain/disfluency/REPORT.md`, PE `chain/pitch_emphasis/REPORT.md`, VC `chain/volume_clarity/REPORT.md`, VF `chain/VERIFICATION.md` (all under `build/work/research/`).

**Rubrics and perception**

1. Schreiber, Paul & Shibley (2012). The development and test of the Public Speaking Competence Rubric. *Communication Education*, 61(3), 205–233. doi:10.1080/03634523.2012.670709. Secondary (reproduced in [2], Appendix B). RE.
2. Joe, Kitchen, Chen & Feng (2015). A prototype public speaking skills assessment: An evaluation of human-scoring quality. *ETS Research Report Series*, RR-15-36. doi:10.1002/ets2.12083. Full. RE.
3. Morreale, Moore, Surges-Tatum & Webster (Eds.) (2007). *The Competent Speaker Speech Evaluation Form* (2nd ed.). National Communication Association. Full. RE.
4. Judging instruments: National Speech & Debate Association, *Declamation Starter Kit*, sample ballots and "How to Judge Declamation"; Poetry Out Loud, *Judge's Guide 2021–22*; Toastmasters International, *International Speech Contest Ballot*, Item 1172 (rev. 05/2024); University Interscholastic League (Texas), *Criteria for Evaluating Persuasive Speakers*. Full. RE §2.1 (URLs there).
5. Chen, Feng, Leong, Joe, Kitchen & Lee (2016). Designing an automated assessment of public speaking skills using multimodal cues. *Journal of Learning Analytics*, 3(2), 261–281. doi:10.18608/jla.2016.32.13. Full. RE.
6. Strangert & Gustafson (2008). What makes a good speaker? Subject ratings, acoustic measurements and perceptual evaluations. *Proc. Interspeech 2008*, 1688–1691. doi:10.21437/Interspeech.2008-368. Full. RE, PE.
7. Hahn (2004). Primary stress and intelligibility: Research to motivate the teaching of suprasegmentals. *TESOL Quarterly*, 38(2), 201–223. doi:10.2307/3588378. Abstract. RE.
8. Van Zant & Berger (2020). How the voice persuades. *Journal of Personality and Social Psychology*, 118(4), 661–682. doi:10.1037/pspi0000193. Abstract. RE.
9. Biadsy, Rosenberg, Carlson, Hirschberg & Strangert (2008). A cross-cultural comparison of American, Palestinian, and Swedish perception of charismatic speech. *Proc. Speech Prosody 2008*, 579–582. doi:10.21437/SpeechProsody.2008-131. Full. RE.
10. Niebuhr, Tegtmeier & Schweisfurth (2019). Female speakers benefit more than male speakers from prosodic charisma training: A before-after analysis of 12-weeks and 4-h courses. *Frontiers in Communication*, 4, 12. doi:10.3389/fcomm.2019.00012. Full. RE.
11. Strangert (2005). Prosody in public speech: Analyses of a news announcement and a political interview. *Proc. Interspeech 2005*, 3401–3404. doi:10.21437/Interspeech.2005-827. Full. RE.
12. Duez (1982). Silent and non-silent pauses in three speech styles. *Language and Speech*, 25(1), 11–28. doi:10.1177/002383098202500102. Abstract. RE.

**Pace and tempo**

13. Quené (2007). On the just noticeable difference for tempo in speech. *Journal of Phonetics*, 35(3), 353–362. doi:10.1016/j.wocn.2006.09.001. Full (author preprint). RE.
14. de Jong & Wempe (2009). Praat script to detect syllable nuclei and measure speech rate automatically. *Behavior Research Methods*, 41(2), 385–390. doi:10.3758/BRM.41.2.385. Full. FE.
15. Trouvain & Grice (1999). The effect of tempo on prosodic structure. *Proc. 14th ICPhS*, 1067–1070. Full. PP [36].
16. Janse (2004). Word perception in fast speech: Artificially time-compressed vs. naturally produced fast speech. *Speech Communication*, 42(2), 155–173. doi:10.1016/j.specom.2003.07.001. Full. PP [37].
17. Crystal & House (1990). Articulation rate and the duration of syllables and stress groups in connected speech. *Journal of the Acoustical Society of America*, 88(1), 101–112. doi:10.1121/1.399955. Abstract. PP [39].
18. Jacewicz, Fox, O'Neill & Salmons (2009). Articulation rate across dialect, age, and gender. *Language Variation and Change*, 21(2), 233–256. doi:10.1017/S0954394509990093. Full-F, confirmed in VF. PP [41].
19. Cucchiarini, Strik & Boves (2000). Quantitative assessment of second language learners' fluency by means of automatic speech recognition technology. *Journal of the Acoustical Society of America*, 107(2), 989–999. doi:10.1121/1.428279. Abstract. PP [28].
20. Suzuki, Kormos & Uchihara (2021). The relationship between utterance and perceived fluency: A meta-analysis of correlational studies. *The Modern Language Journal*, 105(2), 435–463. doi:10.1111/modl.12706. Full (accepted manuscript). PP [31].
21. Hofmann, Gerlach, Wender & Roth (1997). Speech disturbances and gaze behavior during public speaking in subtypes of social phobia. *Journal of Anxiety Disorders*, 11(6), 573–585. doi:10.1016/S0887-6185(97)00040-6. Abstract. PP [10], DF.
22. Teferra, Borwein, DeSouza, Simpson, Rheault & Rose (2022). Acoustic and linguistic features of impromptu speech and their association with anxiety. *JMIR Mental Health*, 9(7), e36828. doi:10.2196/36828. Full; the source through which Laukka et al. (2008) is read. PP [12].
23. Schewski, Doss, Beldi & Keller (2025). Measuring negative emotions and stress through acoustic correlates in speech: A systematic review. *PLOS ONE*, 20(7), e0328833. doi:10.1371/journal.pone.0328833. Full. PP [14], PE, VC.
24. Moers, Meyer & Janse (2017). Effects of word frequency and transitional probability on word reading durations of younger and older speakers. *Language and Speech*, 60(2), 289–317. doi:10.1177/0023830916649215. Abstract. PP [18].
25. de Jong (2016). Predicting pauses in L1 and L2 speech: The effects of utterance boundaries and word frequency. *IRAL*, 54(2), 113–132. doi:10.1515/iral-2016-9993. Abstract. PP [19].
26. Duong, Mostow & Sitaram (2011). Two methods for assessing oral reading prosody. *ACM Transactions on Speech and Language Processing*, 7(4), Article 14. doi:10.1145/1998384.1998388. Full. PP [24], PE.
27. Daane, Campbell, Grigg, Goodman & Oranje (2005). *Fourth-grade students reading aloud: NAEP 2002 special study of oral reading* (NCES 2006-469). National Center for Education Statistics. Full. PP [23].
28. McIntosh, Smit, Saito, Minematsu & Kamper (2026). Self-supervised speech comparison for L2 phone, rhythm, and intonation scoring. arXiv:2607.13721. Full (preprint). PP [49].
29. Camara, Blanco, Godino, Choi & Shattuck-Hufnagel (2026). Word lengthening as a function of utterance position: A multi-corpus study. arXiv:2606.23232. Full (preprint). PP [52].

**Pauses**

30. Campione & Véronis (2002). A large-scale multilingual study of silent pause duration. *Proc. Speech Prosody 2002*, 199–202. doi:10.21437/SpeechProsody.2002-35. Full. RE, FE.
31. de Jong & Bosker (2013). Choosing a threshold for silent pauses to measure second language fluency. *Proc. DiSS 2013*, 17–20. Full. FE.
32. Hallur, Thebaud, Tinchev, Ravichandran & Moro-Velazquez (2026). Reference-based prosody and rhythm evaluation for spoken dialogue systems. arXiv:2606.31055. Full (preprint). RE.
33. Lövgren & van Doorn (2005). Influence of manipulation of short silent pause duration on speech fluency. *Proc. DiSS'05*, 123–126. Full. PP [56].
34. Wang, Green, Nip, Kent & Kent (2010). Breath group analysis for reading and spontaneous speech in healthy adults. *Folia Phoniatrica et Logopaedica*, 62(6), 297–302. doi:10.1159/000316976. Full. PP [1].
35. Wang, Green, Nip, Kent, Kent & Ullman (2010). Accuracy of perceptually based and acoustically based inspiratory loci in reading. *Behavior Research Methods*, 42(3), 791–797. doi:10.3758/BRM.42.3.791. Full-F, confirmed and corrected in VF. PP [2].
36. Miller & Schwanenflugel (2006). Prosody of syntactically complex sentences in the oral reading of young children. *Journal of Educational Psychology*, 98(4), 839–853. doi:10.1037/0022-0663.98.4.839. Full-F, confirmed in VF. PP [22].
37. Kahng (2018). The effect of pause location on perceived fluency. *Applied Psycholinguistics*, 39(3), 569–591. doi:10.1017/S0142716417000534. Abstract. PP [34], VF.
38. Tavakoli (2011). Pausing patterns: Differences between L2 learners and native speakers. *ELT Journal*, 65(1), 71–79. doi:10.1093/elt/ccq020. Abstract. PP [33].
39. Schwanenflugel, Hamilton, Kuhn, Wisenbaker & Stahl (2004). Becoming a fluent reader: Reading skill and prosodic features in the oral reading of young readers. *Journal of Educational Psychology*, 96(1), 119–129. doi:10.1037/0022-0663.96.1.119. Full-F, confirmed in VF. PP [21].

**Pitch**

40. 't Hart (1981). Differential sensitivity to pitch distance, particularly in speech. *Journal of the Acoustical Society of America*, 69(3), 811–821. doi:10.1121/1.385592. Abstract. RE, PE.
41. Hincks & Edlund (2009). Promoting increased pitch variation in oral presentations with transient visual feedback. *Language Learning & Technology*, 13(3), 32–50. Full. RE.
42. Hincks (2005). Measuring liveliness in presentation speech. *Proc. Interspeech 2005*. doi:10.21437/Interspeech.2005-353. Full. PE.
43. Niebuhr & Skarnitzl (2019). Measuring a speaker's acoustic correlates of pitch – but which? A contrastive analysis based on perceived speaker charisma. *Proc. ICPhS 2019*, 1774–1778. Full. PE.
44. Boersma (1993). Accurate short-term analysis of the fundamental frequency and the harmonics-to-noise ratio of a sampled sound. *Proceedings of the Institute of Phonetic Sciences, University of Amsterdam*, 17, 97–110. Full. FE.
45. Hirst (2011). The analysis by synthesis of speech melody: From data to models. *Journal of Speech Sciences*, 1(1), 55–83. doi:10.20396/joss.v1i1.15011. Full. FE.
46. Arantes & Eriksson (2014). Temporal stability of long-term measures of fundamental frequency. *Proc. Speech Prosody 2014*, 1149–1152. doi:10.21437/SpeechProsody.2014-220. Full. FE.
47. Strömbergsson (2016). Today's most frequently used F0 estimation methods, and their accuracy in estimating male and female pitch in clean speech. *Proc. Interspeech 2016*, 525–529. doi:10.21437/Interspeech.2016-240. Full. FE.
48. Jouvet & Laprie (2017). Performance analysis of several pitch detection algorithms on simulated and real noisy speech data. *Proc. EUSIPCO 2017*, 1614–1618. doi:10.23919/EUSIPCO.2017.8081482. Full. FE.
49. Zimmerer, Jügler, Andreeva, Möbius & Trouvain (2014). Too cautious to vary more? A comparison of pitch variation in native and non-native productions of French and German speakers. *Proc. Speech Prosody 2014*. Full. PE.
50. Patterson & Ladd (1999). Pitch range modelling: Linguistic dimensions of variation. *Proc. ICPhS 1999*, 1169–1172. Full. PE.
51. Wehrle, Cangemi, Krüger & Grice (2018). Somewhere over the spectrum: Between robotic and singsongy intonation. *Studi AISV*, 4, 179–194. doi:10.17469/O2104AISV000010. Full. PE.
52. Portnova, Fletcher, Wisler & Borrie (2025). Assessing fundamental frequency variation in speakers with Parkinson's disease: Effects of tracking errors. *Journal of Speech, Language, and Hearing Research*, 68(7S), 3568–3582. doi:10.1044/2024_JSLHR-24-00381. Full. PE.
53. Wang, Evanini & Yoon (2015). Word-level F0 modeling in the automated assessment of non-native read speech. *Proc. SLaTE 2015*. doi:10.21437/SLaTE.2015-5. Full. PE.
54. Low, Bentley & Ghosh (2020). Automated assessment of psychiatric disorders using speech: A systematic review. *Laryngoscope Investigative Otolaryngology*, 5(1). PMC7042657. Full. PE.
55. Traunmüller & Eriksson (1995). The perceptual evaluation of F0 excursions in speech as evidenced in liveliness estimations. *Journal of the Acoustical Society of America*, 97(3), 1905–1915. doi:10.1121/1.412942. Abstract. PE.

**Emphasis**

56. Xu & Xu (2005). Phonetic realization of focus in English declarative intonation. *Journal of Phonetics*, 33, 159–197. doi:10.1016/j.wocn.2004.11.001. Full. PE.
57. Suni, Aalto & Vainio (2015). Hierarchical representation of prosody for statistical speech synthesis. arXiv:1510.01949. Full (preprint of the method published in 2017). PE.
58. Talman, Suni, Celikkanat, Kakouros, Tiedemann & Vainio (2019). Predicting prosodic prominence from text with pre-trained contextualized word representations. *Proc. NoDaLiDa 2019*. arXiv:1908.02262. Full. PE.
59. Kallio, Suni & Šimko (2022). Fluency-related temporal features and syllable prominence as prosodic proficiency predictors for learners of English with different language backgrounds. *Language and Speech*, 65(3). PMC9326808. Full. PE.
60. Sluijter & van Heuven (1996). Spectral balance as an acoustic correlate of linguistic stress. *Journal of the Acoustical Society of America*, 100(4), 2471–2485. doi:10.1121/1.417955. Full. FE.
61. Kochanski, Grabe, Coleman & Rosner (2005). Loudness predicts prominence: Fundamental frequency lends little. *Journal of the Acoustical Society of America*, 118(2), 1038–1054. doi:10.1121/1.1923349. Abstract. FE, PE.
62. Baumann & Winter (2018). What makes a word prominent? Predicting untrained German listeners' perceptual judgments. *Journal of Phonetics*, 70, 20–38. doi:10.1016/j.wocn.2018.05.004. Full (accepted manuscript). PE.
63. Kakouros, Räsänen & Alku (2018). Comparison of spectral tilt measures for sentence prominence in speech: Effects of dimensionality and adverse noise conditions. *Speech Communication*. Full (author manuscript). PE.
64. Nenkova, Brenier, Kothari, Calhoun, Whitton, Beaver & Jurafsky (2007). To memorize or to predict: Prominence labeling in conversational speech. *Proc. NAACL HLT 2007*, 9–16. Full. PE.
65. Mo, Cole & Lee (2008). Naïve listeners' prominence and boundary perception. *Proc. Speech Prosody 2008*. doi:10.21437/SpeechProsody.2008-163. Full. PE.

**Volume**

66. Caswell-Midwinter & Whitmer (2019). Discrimination of gain increments in speech-shaped noises. *Trends in Hearing*, 23. doi:10.1177/2331216518820220. Full. RE.
67. Liénard & Di Benedetto (1999). Effect of vocal effort on spectral properties of vowels. *Journal of the Acoustical Society of America*, 106(1), 411–422. doi:10.1121/1.428140. Abstract. VC.
68. Sundberg & Nordenberg (2006). Effects of vocal loudness variation on spectrum balance as reflected by the alpha measure of long-term-average spectra of speech. *Journal of the Acoustical Society of America*, 120(1), 453–457. doi:10.1121/1.2208451. Abstract. VC.
69. Eriksson & Traunmüller (1999). Perception of vocal effort and speaker distance on the basis of vowel utterances. *Proc. ICPhS 1999*. Full. VC.
70. Pierrehumbert (1979). The perception of fundamental frequency declination. *Journal of the Acoustical Society of America*. doi:10.1121/1.383670. Abstract. VC.
71. Ní Chasaide, Yanushevskaya & Gobl (2015). Prosody of voice: Declination, sentence mode and interaction with prominence. *Proc. ICPhS 2015*, paper 0476. Full. VC.
72. Zhang & Hansen (2007). Analysis and classification of speech mode: Whispered through shouted. *Proc. Interspeech 2007*. Full. VC.

**Clarity**

73. Picheny, Durlach & Braida (1986). Speaking clearly for the hard of hearing II: Acoustic characteristics of clear and conversational speech. *Journal of Speech and Hearing Research*, 29(4), 434–446. doi:10.1044/jshr.2904.434. Abstract. FE, VC.
74. Krause & Braida (2004). Acoustic properties of naturally produced clear speech at normal speaking rates. *Journal of the Acoustical Society of America*, 115(1), 362–378. doi:10.1121/1.1635842. Abstract. FE, VC.
75. Smiljanić & Bradlow (2009). Speaking and hearing clearly: Talker and listener factors in speaking style changes. *Language and Linguistics Compass*, 3(1), 236–264. PMC2747755. Full. VC.
76. Cao, Fan, Svendsen & Salvi (2024). A framework for phoneme-level pronunciation assessment using CTC. *Proc. Interspeech 2024*, 302–306. doi:10.21437/Interspeech.2024-459. Full. VC.
77. Halpern, Tienkamp, Abur & Toda (2026). PathBench: Speech intelligibility benchmark for automatic pathological speech assessment. arXiv:2603.08097. Full (preprint). VC.

**Disfluency**

78. Lickley (2017). Disfluency in typical and stuttered speech. *Studi AISV*, 3, 373–387. doi:10.17469/O2103AISV000019. Full. DF.
79. Shriberg (1999). Phonetic consequences of speech disfluency. *Proc. ICPhS 1999*, 619–622. Full. DF.
80. Ritto, Costa, Juste & de Andrade (2016). Comparison of different speech tasks among adults who stutter and adults who do not stutter. *Clinics*, 71(3). doi:10.6061/clinics/2016(03)06. Full. DF.
81. Clark & Fox Tree (2002). Using uh and um in spontaneous speaking. *Cognition*, 84, 73–111. doi:10.1016/S0010-0277(02)00017-3. Full. DF.
82. Christenfeld & Creager (1996). Anxiety, alcohol, aphasia, and ums. *Journal of Personality and Social Psychology*, 70(3), 451–460. doi:10.1037/0022-3514.70.3.451. Abstract. DF.
83. Goto, Itou & Hayamizu (1999). A real-time filled pause detection system for spontaneous speech recognition. *Proc. Eurospeech 1999*, 227–230. doi:10.21437/Eurospeech.1999-60. Full. DF.
84. Gabrea & O'Shaughnessy (2000). Detection of filled pauses in spontaneous conversational speech. *Proc. ICSLP 2000*. doi:10.21437/ICSLP.2000-626. Full. DF.
85. Zhu, Caceres & Salamon (2022). Filler word detection and classification: A dataset and benchmark. *Proc. Interspeech 2022*. arXiv:2203.15135. Full. DF.
86. Gao, Tejedor-Garcia, Strik & Cucchiarini (2024). Reading miscue detection in primary school through automatic speech recognition. *Proc. Interspeech 2024*. arXiv:2406.07060. Full (parts). DF, VF.
87. Lea, Mitra, Joshi, Kajarekar & Bigham (2021). SEP-28k: A dataset for stuttering event detection from podcasts with people who stutter. *Proc. ICASSP 2021*. arXiv:2102.12394. Full. DF.
88. Bayerl, Wolff von Gudenberg, Hönig, Nöth & Riedhammer (2022). KSoF: The Kassel State of Fluency dataset – a therapy centered dataset of stuttering. *Proc. LREC 2022*. arXiv:2203.05383. Full (parts). DF.
89. Kourkounakis, Hajavi & Etemad (2021). FluentNet: End-to-end detection of stuttered speech disfluencies with deep learning. *IEEE/ACM Transactions on Audio, Speech, and Language Processing*, 29, 2986–2999. arXiv:2009.11394. Full (parts). DF.
90. Kouzelis, Paraskevopoulos, Katsamanis & Katsouros (2023). Weakly-supervised forced alignment of disfluent speech using phoneme-level modeling. *Proc. Interspeech 2023*. arXiv:2306.00996. Full. DF.
91. Zhou, Kashyap, Li, Sharma, Morin, Baquirin, Vonk, Ezzes, Miller, Gorno-Tempini, Lian & Anumanchipalli (2024). YOLO-Stutter: End-to-end region-wise speech dysfluency detection. *Proc. Interspeech 2024*, 937–941. doi:10.21437/Interspeech.2024-1855. Full. DF, GM.
92. Harvill, Hasegawa-Johnson & Yoo (2022). Frame-level stutter detection. *Proc. Interspeech 2022*, 2843–2847. Full. DF.
93. Tomisato, Mori, Asano, Iimura, Yada, Takahashi, Wasano, Kono & Ozawa (2024). Speech characteristics that differentiate stuttering and cluttering in Japanese speakers. *Frontiers in Psychology*, 15, 1408929. doi:10.3389/fpsyg.2024.1408929. Full. DF.
94. Bosker, Pinget, Quené, Sanders & de Jong (2013). What makes speech sound fluent? The contributions of pauses, speed and repairs. *Language Testing*, 30(2), 159–175. doi:10.1177/0265532212455394. Full (status corrected in VF). PP [30], DF.

**Sentence endings**

95. Chung & Bidelman (2022). Acoustic features of oral reading prosody and the relation with reading fluency and reading comprehension in Taiwanese children. *Journal of Speech, Language, and Hearing Research*, 65, 334–343. doi:10.1044/2021_JSLHR-21-00252. Full. PE, VF.
96. Ritchart & Arvaniti (2014). The form and use of uptalk in Southern Californian English. *Proc. Speech Prosody 2014*, 331–335. Full. PE.
97. Yuan & Liberman (2014). F0 declination in English and Mandarin broadcast news speech. *Speech Communication*, 65, 67–74. Full. PE, VC.
98. Rosenberg (2010). AuToBI – a tool for automatic ToBI annotation. *Proc. Interspeech 2010*. Full. PE.
99. Drugman, Kane & Gobl (2014). Data-driven detection and analysis of the patterns of creaky voice. *Computer Speech & Language*, 28(5), 1233–1253. arXiv:2006.00518. Full. PE, VC.

**Alignment, comparison, evaluation, explanation**

100. Huang, Zhang, Ni, Sun, Hira, Hwang, Manohar, Pratap, Wiesner, Watanabe, Povey & Khudanpur (2024). Less peaky and more accurate CTC forced alignment by label priors. arXiv:2406.02560. Full. AL, GM.
101. McAuliffe, Gunter, Wagner & Sonderegger (2026). Montreal Forced Aligner and the state of speech-to-text alignment in 2026. arXiv:2606.18466. Full. AL.
102. Rousso, Cohen, Keshet & Chodroff (2024). Tradition or innovation: A comparison of modern ASR methods for forced alignment. *Proc. Interspeech 2024*. arXiv:2406.19363. Full. AL, GM.
103. Liang, Li, Rackauckas & Hirschberg (2026). A survey of automated presentation coaching: Systems, methods, and open challenges. arXiv:2606.27380. Full (preprint). RE.
104. NIST/SEMATECH. *e-Handbook of Statistical Methods*, section 1.3.5.17, Detection of outliers. https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm. Full. RE, GM.
105. Korzekwa, Lorenzo-Trueba, Drugman & Kostek (2022). Computer-assisted pronunciation training: Speech synthesis is almost all you need. *Speech Communication*, 142, 22–33. doi:10.1016/j.specom.2022.06.003. Full. GM.
106. Geirhos, Jacobsen, Michaelis, Zemel, Brendel, Bethge & Wichmann (2020). Shortcut learning in deep neural networks. *Nature Machine Intelligence*, 2(11), 665–673. doi:10.1038/s42256-020-00257-z. Abstract. RE.
107. Heittola & Mesaros (n.d.). `sed_eval`: Evaluation toolbox for sound event detection, source file `sed_eval/sound_event.py`. https://github.com/TUT-ARG/sed_eval. Full (source code). GM.
108. Bilen, Ferroni, Tuveri, Azcarreta & Krstulović (2020). A framework for the robust evaluation of sound event detection. *Proc. IEEE ICASSP 2020*, 61–65. doi:10.1109/ICASSP40776.2020.9052995. Full. GM.
109. Kim, Choi, Choi, Lee & Yoon (2022). Towards a rigorous evaluation of time-series anomaly detection. *Proc. AAAI 2022*, 36(7), 7194–7201. doi:10.1609/aaai.v36i7.20680. Full. GM.
110. Cawley & Talbot (2010). On over-fitting in model selection and subsequent selection bias in performance evaluation. *Journal of Machine Learning Research*, 11, 2079–2107. Full. GM.
111. Wisniewski, Zierer & Hattie (2020). The power of feedback revisited: A meta-analysis of educational feedback research. *Frontiers in Psychology*, 10, 3087. doi:10.3389/fpsyg.2019.03087. Full. RE.
112. Kluger & DeNisi (1996). The effects of feedback interventions on performance: A historical review, a meta-analysis, and a preliminary feedback intervention theory. *Psychological Bulletin*, 119(2), 254–284. doi:10.1037/0033-2909.119.2.254. Abstract. RE.
113. Shute (2008). Focus on formative feedback. *Review of Educational Research*, 78(1), 153–189. doi:10.3102/0034654307313795. Full (read as ETS RR-07-11, 2007). RE.
114. Miller (2019). Explanation in artificial intelligence: Insights from the social sciences. *Artificial Intelligence*, 267, 1–38. doi:10.1016/j.artint.2018.07.007. Full. RE.
115. Wachter, Mittelstadt & Russell (2018). Counterfactual explanations without opening the black box: Automated decisions and the GDPR. *Harvard Journal of Law & Technology*, 31(2). arXiv:1711.00399. Abstract. RE.
116. Pearl (2019). The seven tools of causal inference, with reflections on machine learning. *Communications of the ACM*, 62(3), 54–60. doi:10.1145/3241036. Full. RE.
117. Atil, Aykent, Chittams, Fu, Passonneau, Radcliffe, Rajagopal, Sloan, Tudrej, Ture, Wu, Xu & Baldwin (2024). Non-determinism of "deterministic" LLM settings. arXiv:2408.04667. Abstract. RE.
118. Tanveer, Lin & Hoque (2015). Rhema: A real-time in-situ intelligent interface to help people with public speaking. *Proc. ACM IUI 2015*, 286–295. doi:10.1145/2678025.2701386. Abstract. RE.

**Added for sentence endings**

119. Vaughan-Johnston, Guyer, Fabrigar, Lamprinakos & Brinol (2024). Falling vocal intonation signals speaker confidence and conditionally boosts persuasion. *Personality and Social Psychology Bulletin*, 52(1), 3–21. doi:10.1177/01461672241262180. Full. RE.
