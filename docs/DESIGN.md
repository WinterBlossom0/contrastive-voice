# Contrastive Voice — build contract

> Written for the detector of 2026-10-02. The final detector (configuration `782d7df7…`, with the speech-tempo key D9) and its evaluation are described in `docs/technical.md`; its numbers are in `docs/NUMBERS.md`. Where this contract differs, those documents hold.

This contract describes the code after the detector rework of 2026-10-02.
Code comments cite its numbered sections as `DESIGN <section>`.
**[owner]** marks an owner decision.
Section 0 preserves earlier decisions and appends later decisions in order.
Later decisions supersede earlier decisions where stated.
Constants and fitted values come from `src/cvoice/config.py` and `models/detector.json`.
Published measurements cite `docs/PAPERS.md`.

## 0. Owner decisions

- As little data as possible; lightest possible model; no heavy compute on the laptop. **[owner]**
- Bad spectrum fully automated (DSP edits). No self-recording. **[owner]**
- Baselines: public domain only (TED dropped: Devpost Terms 7.B.iii(c), TED Terms 6.4). Public-domain LibriVox
  human readings are the second speakers. **[owner]**
- Detector: threshold detector only — no logistic regression, GBM or neural flaw model. **[owner]**
- 9 baseline speeches, one auto-selected ~30 s passage each; split by speaker 5 train / 2 val / 2 test; 3 severity
  levels; packed multi-flaw clips. **[owner]**
- Dashboard: FastAPI + one static HTML/JS page (Plotly + wavesurfer, no build step). **[owner]**
- Compute: source audio is downloaded on the laptop and staged as a private Kaggle dataset; dataset build,
  calibration, evaluation and gallery run in a private Kaggle kernel; laptop = unit tests + one-clip smoke. Kaggle with
  two T4 GPUs is the standard compute for the project and for teammates: the pipeline uses both GPUs when present and
  still runs on CPU. **[owner]**
- AI disclosure in README / Devpost "Built With": Claude Code. **[owner]**

Decisions recorded in the owner's handoff notes (not in the repository) on 2026-10-02:

- 2026-10-02: "Continue now building the project. You might need to refactor the code a bit since the repository has started looking messy. Make sure you discard the code which is not being used don't keep unwanted stuff." **[owner]**
- 2026-10-02: AI disclosure remains Claude Code only. HANDOFF records "settled, never ask or flag again". **[owner]**
- 2026-10-02: "focus on making the actual product itself with proper research and grounding; will do the documentation process at the very end". HANDOFF keeps documentation parked until the owner asks. **[owner]**
- 2026-10-02 ~15:00 UTC: HANDOFF records the lead's decision: "the second final (test-split) evaluation is NOT run now. It runs once when the detector is frozen, just before the documentation phase." Follow `docs/FINAL_EVALUATION_PLAN.md`. Until then, runs use train and validation only.
- 2026-10-02 ~15:40 UTC: HANDOFF records the owner's research chain: flaw -> its several reasons -> the pattern each reason leaves -> the method that captures that pattern, often in another paper under another name. The owner also said "now go do your research no code for today finish up your research once everything is done inform me I will compact you." **[owner]**
- 2026-10-02 (late): "your first question should be can I get the required data. Do not have an answer like I will not pursue before you even questions yourself." Check data availability before ranking or dropping an approach. **[owner]**
- 2026-10-02 (late): "non commercial is fine the comp doesn't forbid it". Non-commercial licences are acceptable for external research data. Each source's terms still apply. This broadens the earlier public-domain data restriction; the existing baseline set stays public domain. **[owner]**
- 2026-10-02 (night): "broaden the scope"; "no self recorded flaws for now will tell if my mind changes"; "data should be in kaggle for now". **[owner]**
- 2026-10-02 (night): HANDOFF temporarily records "every dataset this project uses must be PUBLIC on Kaggle" so recipients need no access grant. The later private-data decision below supersedes this. **[owner]**
- 2026-10-02 ~18:25 UTC: HANDOFF records "datasets stay PRIVATE". The owner said "build a method which will allow my friends to reconstruct that data" and chose "method 2 since they would be using kaggle as well". The build kernel reconstructs source data from origins without an owner access grant (§10). This supersedes the temporary public-data decision and the laptop-only download route. **[owner]**
- 2026-10-02 ~18:45 UTC: Keep copies of the transcript pages in the repository. The owner's reply was "sure do that". The reconstruction route uses those snapshots (§10). **[owner]**

## 1. What the system does, and its stated limits

Input is participant audio, a transcript, and a reference rendition of the same text.
Output is the result JSON in §9.
It contains word alignment, time-series rows, local flaw regions, whole-clip flags, explanations, and scores.
The rubric names map to D1 Pace (Cadence), D2 Pauses, D3 Pitch variation and D4 Emphasis (Tone), D5 Volume, and D6 Clarity (spectral-change proxy).

Departures are relative to one reference rendition.
Timing has word-boundary resolution.
The published boundary errors for this wav2vec 2.0 model are 48 ms on TIMIT and 89 ms on Buckeye (`docs/PAPERS.md`, entry 21).
These are published model measurements, not measurements on this dataset.
Localisation is evaluated for clips with at most 35 % edited-word coverage (`COVERAGE_CAP`).
Passage selection favours alignment quality.
Different-speaker calibration uses lay readers of one text.
Comparison-minutes share recordings and are not established independent observations.
Evaluation uses controlled acoustic edits without human ratings.
External research data (§10) has not entered detector evaluation.

## 2. Data

### 2.1 Baselines and splits

`data/sources_manifest.json` defines the public-domain baseline speeches.
Train: harris_uncsw_2021, hclinton_tomorrow_2010, gwbush_911_2001, obama_weekly_2009, reagan_farewell_1989.
Validation: lbush_radio_2001, eisenhower_farewell_1961.
Test: mobama_weekly_2014, nixon_resignation_1974.
Reagan Challenger and JFK inaugural probe clips are development material.

Scales and thresholds are fitted on train nulls and train labels as described in §5.2.
Score constants are fitted on train after threshold selection.
Validation speakers and check readers were inspected during the rework.
Their results are development evidence.
The second final evaluation waits for a frozen detector (§8).

### 2.2 Ingest and passage selection

ffmpeg decodes the source audio.
Stereo uses the left channel when side energy exceeds mid energy by more than 10 dB (`STEREO_SIDE_DB`).
Otherwise, channels are averaged.
Canonical audio is DC-removed, 16 kHz mono PCM16 WAV (`SR`).
Resampling uses soxr HQ.
Source audio hashes are checked before ingest.

Passages are selected automatically.
Chunked wav2vec 2.0 emissions produce greedy CTC words and frame times.
`SequenceMatcher(autojunk=False)` anchors those words to the official transcript.
Candidate windows contain consecutive sentences.
Each sentence needs at least 80 % anchored coverage (`SENTENCE_COVERAGE_MIN`).
Windows must last 20–40 s (`PASSAGE_S`).
They rank by minimum sentence coverage, distance from the 30 s target (`PASSAGE_TARGET_S`), then earliest position.
Forced alignment uses 0.5 s context on each side (`PASSAGE_CONTEXT_S`).
Reagan candidates must be anchored in both the original and Greenman readings.
Gettysburg readers share one token span.
The manifest stores sentence indices, source times, spoken text, and passage QA.

### 2.3 Human second speakers

Public-domain LibriVox Gettysburg readers supply the different-speaker comparisons.
Calibration readers are amb, dl, fb, jn, pc, and wt.
Check readers are dj, sa, and tg.
All ordered pairs of distinct calibration readers fit R2.
Each check reader is compared against every calibration reader for null and edited evaluation.
These check readers were seen during the redesign and are not held-out evidence.

Stored Gettysburg edits use amb as their reference for edit eligibility (`dataset.GETTYSBURG_REFERENCE`).
Evaluation then compares each edited clip with every calibration reference.
John Greenman's Reagan farewell reading uses the Reagan baseline as its reference.
That pair is never used to fit a scale.
Its clean null and edited results stay separate from the check-reader population.
The final evaluation plan records it as the only different-speaker pair not used in the rework.

### 2.4 Flaw injection

Edits change a word span or pause boundary and splice the result back.
Samples outside the edit support remain bit-identical.
Stored clips use chain A: numpy WSOLA for time and Praat PSOLA for pitch.
Evaluation generates chain B: Praat PSOLA duration and WORLD pitch.
Chain B covers RUSH, DRAG, and MONOTONE (`CHAIN_B_TYPES`).
Praat is seeded before each edit (`PRAAT_SEED`).
Time edits preserve in-span pauses of at least 0.20 s (`PAUSE_MIN_S`).

Recipe values below come from `LEVEL_PARAM` and `PAUSE_FLOOR_S` in `config.py`.
Ratios, fractions, and strengths are dimensionless.

| Flaw | Recipe | L1 | L2 | L3 |
|---|---|---|---|---|
| RUSH (D1) | speech duration divided by rate ratio | 1.20 × | 1.45 × | 1.90 × |
| DRAG (D1) | speech duration multiplied by duration ratio | 1.20 × | 1.45 × | 1.90 × |
| PAUSE_DROPPED (D2) | fraction of eligible pause kept | 0.40 fraction | 0.20 fraction | 0.06 s kept |
| PAUSE_INTRUSIVE (D2) | same-recording room tone inserted inside a phrase | 0.35 s | 0.60 s | 1.20 s |
| MONOTONE (D3) | fraction of F0 range kept around speaker median | 0.50 fraction | 0.25 fraction | 0.00 fraction |
| DEEMPHASIS (D4) | flatten F0 peak, lower gain, shorten stress word | 0.50 strength | 0.75 strength | 1.00 strength |
| FADE (D5) | ramp over first third, hold, then release | 4 dB | 8 dB | 14 dB |
| MUMBLE (D6) | smooth spectral envelope while preserving frame level | 0.30 strength | 0.60 strength | 1.00 strength |

FADE release lasts 0.10 s (`FADE_RELEASE_S`).
MUMBLE is used only in the same-performance regime.
Uptalk, fillers, and repetitions are absent from the current edit recipes.

Windowed edits use 5–8 words (`SPAN_WORDS`).
DEEMPHASIS uses one stress word.
Pause edits use one boundary.
Seeded placement samples eligible positions and keeps edits apart (`EDIT_GAP_WORDS`).
Edited-word coverage is capped at 35 % (`COVERAGE_CAP`).
Boundary edits are excluded from that word count.
Identity and botched clips are exempt.
If placement exceeds the cap, windowed edits are dropped and recorded as skipped.
PAUSE_DROPPED and DEEMPHASIS require an eligible event in the edited rendition.
Cross-speaker eligibility also checks the reference.

`EXPECTED_SECONDARY` records recipe effects in other dimensions.
Strict evaluation counts those firings.
The secondary-exempt view removes only firings in a labelled secondary dimension whose indices overlap the label expanded by half the comparison window (§8).

The expectation table remains fixed in `evaluate.EXPECTED`.
It states expectations, not measured results.

| Level | R1 same performance | R2 different performance |
|---|---|---|
| L1 | marginal detection near or below 50 %; clip score at least 90 index points | must stay silent |
| L2 | flagged | marginal |
| L3 | flagged | flagged for pace, pauses, pitch, volume; D4 and D6 unscored |

L2 and L3 form the localisation headline (`HEADLINE_LEVELS`).
L1 is reported separately.

Per baseline, `LEVELS` and `SINGLE_LEVEL_SETS` produce six single-level clips.
Each level has two clips with separate sets of four flaw types.
An identity clip runs the recipes with null parameters.
G1 contains one L1 RUSH (`G1_TYPE`).
G3 contains L2 RUSH, MONOTONE, and FADE (`G3_TYPES`).
G5 is botched: whole-passage L3 RUSH and MONOTONE, eligible dropped pauses, and fades (`G5_FADES`).
This gives ten derived clips per baseline.

`CROSS_SPEAKER_CLIPS` now produces four clips per check reader and per Greenman reading:

| Clip | Level | Types |
|---|---|---|
| x1 | L2 | RUSH, PAUSE_DROPPED |
| x2 | L3 | DRAG, MONOTONE |
| x3 | L3 | PAUSE_INTRUSIVE, FADE |
| x4 | L3 | RUSH, PAUSE_DROPPED |

Each also gets a G5 clip with kind `cross_botched`.
The current layout totals **129 audio files**: nine baselines, ninety baseline-derived clips, ten clean reader clips, and twenty reader-derived clips.
Skipped edits and missing clips are recorded in the manifest.
Chain-B variants, extra placebo seeds, stress transforms, and graded whole-passage rungs are generated during evaluation.
They do not add stored dataset audio files.

### 2.5 Labels

Each label file stores the parent hash, recipe, seed, chain, and analytic word time map.
Each flaw stores type, dimension, level, physical magnitude, realised change, expected secondary dimensions, word indices, and half-open sample spans in participant and parent audio.
Pause labels are boundary events.
The manifest reports the union of edit-support samples divided by participant samples.
This time share includes inserted silence and releases.
It is separate from the edited-word cap.
Label QA re-aligns every stored clip and compares boundaries with the analytic labels.
This is self-consistency, without human boundary truth.

## 3. Alignment

The aligner is `torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H` in float32 inference mode.
It runs on CPU or GPU.
Long recordings use 30 s chunks with 1 s context (`CHUNK_S`, `CONTEXT_S`).
Numpy CTC Viterbi uses float64 dynamic programming and int8 backpointers.
CTC frames last 20 ms (`CTC_FRAME_S`).
Raw CTC spans supply word timing.
Energy snapping is absent.
Published boundary-error limits are in §1.

An acoustic pause is the longest silent run between consecutive word centres.
A frame must be unvoiced and below the threshold from `align.pause_threshold`:

`theta = max(Q5(L) + clip(0.3 × (Q95(L) − Q5(L)), 6 dB, 15 dB), Q99(L) − 35 dB)`.

The floor rule and peak rule come from `PAUSE_Q`, `PAUSE_FRAC`, `PAUSE_CLIP_DB`, `PAUSE_PEAK_Q`, and `PAUSE_PEAK_DB`.
The peak rule keeps breath noise within pauses when the recording has a gated or digital-silence floor.
Breaks of at most 20 ms are bridged (`PAUSE_BRIDGE_FRAMES`, `HOP_S`).
A run of at least 0.20 s is stored as `sil` (`PAUSE_MIN_S`).
Shorter runs store zero there.
`sil_raw` retains the length without that duration cut.
D2 uses `sil_raw` so its difference is continuous around the cut.

Word posterior compatibility is reported and never excludes a word.
Values below 0.10 trigger a notice (`LOW_COMPAT_NOTICE`).
Mean compatibility below 0.10 causes refusal only at upload and passage-selection trust boundaries (`MEAN_COMPAT_MIN`).
Other paths record compatibility and continue.
Text normalisation retains uppercase letters and apostrophes and spells out numbers.
Display tokens remain available.
Syllable counts use `cmudict` with a flagged heuristic fallback.
Alignment device class is recorded in detector and result JSON.
GPU/CPU agreement is evaluated separately (§8).
Batch alignment uses `PreparePool` (§10).

## 4. Features

Audio is 16 kHz mono (`SR`).
Frames use a 400-sample Hann window, 160-sample hop, and 512-point FFT (`WIN`, `HOP`, `NFFT`).
The hop is 10 ms (`HOP_S`).
Level is `L = 10 log10(sum(w × x²) / sum(w) + LEVEL_EPS)` in dB re full scale.
Relative level E subtracts median voiced L, or median L over all frames when voicing is insufficient (`MIN_VOICED_REF`).

Praat autocorrelation starts at 60–700 Hz (`F0_PASS1`).
Its second-pass floor is `max(50 Hz, 0.75 × Q25(F0))`.
Its ceiling is `min(800 Hz, 1.5 × Q75(F0))`.
Insufficient first-pass voicing uses 75–600 Hz (`F0_FALLBACK`, `F0_MIN_FIRST_PASS`).
Median filtering uses five frames within voiced runs (`F0_MEDIAN_FRAMES`).
Unvoiced gaps are not interpolated.
Pitch is `S = 12 log2(F0 / median voiced F0)` in semitones (st).

MFCCs use forty mel filters over 50–7600 Hz (`N_MEL`, `MEL_FMIN`, `MEL_FMAX`).
DCT-II produces c0 through c12 (`N_CEPS`).
Spectral change Q is the norm of delta c1 through c12.
Per-word statistics use expanded acoustic support around raw CTC spans.
They include duration, syllables, median/P90 pitch, P90 relative level, and mean Q.
Word pitch needs five voiced frames (`MIN_VOICED_WORD`).

Stress inputs are `u = (ln(duration/syllables), P90(S), P90(E))`.
Stress points p average `(u − m) / sigma` across these inputs.
Each rendition uses its own medians and the baseline's robust scales.
Scale floors are ln(1.15), 3 st, and 3 dB respectively (`STRESS_SIGMA_FLOOR`).
A stress word has at least 0.75 p-units and is a neighbouring local maximum (`STRESS_P_MIN`).

## 5. Contrastive comparison and detector

### 5.1 Deltas

Participant P and baseline B share transcript word indices.
Windowed dimensions use centred five-word windows clipped at sentence boundaries.
A window needs at least three words (`WINDOW_WORDS`, `WINDOW_MIN_WORDS`).

- **D1 Pace:** `r_i = ln(T_i^P / T_i^B)` in ln units, where T is window speech time. Where either recording has an acoustic pause, each loses its own raw silent gap. `g = median finite r`; `x_i = r_i − g`. Negative x is RUSH; positive x is DRAG. g measures overall tempo.
- **D2 Pauses:** `x = sil_raw^P − sil_raw^B` in s. A value exists where either recording has a pause of at least 0.20 s (`PAUSE_MIN_S`). Negative x can flag PAUSE_DROPPED only when the baseline pause is at least 0.50 s (`PAUSE_DROP_MIN_BASE_S`). Positive x can flag PAUSE_INTRUSIVE only when the baseline pause is below 0.20 s and the transcript has no punctuation at that boundary. Scale fitting sees every eligible delta before these sign gates.
- **D3 Pitch variation:** R is P90−P10 of voiced S over a window, in st. It needs at least fifty voiced frames (`D3_MIN_VOICED_FRAMES`). `r_i = ln((R_i^P + 1 st) / (R_i^B + 1 st))`; `g = median finite r`; `x_i = r_i − g` in ln units. The 1 st regulariser is `RANGE_REG_ST`. Negative x can flag MONOTONE. g measures overall pitch range.
- **D4 Emphasis:** at each baseline stress word, `x = p^P − p^B` in p-units. A negative delta can flag DEEMPHASIS only if the participant loses the marker (`p^P < STRESS_P_MIN`).
- **D5 Volume:** d is participant minus baseline mean E over non-pause window frames, in dB. `x = d − median finite d`. Only negative x can flag FADE.
- **D6 Clarity (spectral-change proxy):** c is the ln ratio of participant to baseline window mean Q over non-pause frames. `x = c − median finite c`. Only negative x can flag MUMBLE.

Local explanations use `Dim.reference(i)`.
It carries the reference measurement to the participant's overall tempo, pitch range, level, or spectral-change ratio.
For D3 it inverts the regularised ratio and clamps the reference range at zero st.
Whole-clip flags retain g before centring (§5.2).
The word-time map is described in §9.

### 5.2 Decision rule and fitted state

Detector JSON has **schema 3**.
A local flag key combines dimension and direction: D1−, D1+, D2−, D2+, D3−, D4−, D5−, or D6−.
Stored keys use ASCII minus signs, for example `D2-`.
`regimes[regime].h` stores a threshold h or null per key.
`regimes[regime].clip` stores a threshold per whole-clip dimension.
Null disables that local direction.

Directions share a dimension scale.
`z = x / s_k`, where `s_k = max(floor_k, 1.4826 × weighted MAD, weighted Q68(|x|))` on regime nulls.
Each null pair has equal total weight after normalising its valid unit weights.
The fitted null median is stored and never subtracted.
Selection and decoding use rounded scales.

| Dimension | Minimum scale (`FLOORS`) | Local saturation (`X_SAT`) |
|---|---|---|
| D1 | ln(1.10) ln units | ln(1.90) ln units |
| D2 | 0.15 s | 1.00 s |
| D3 | ln(1.40) ln units | ln(5.00) ln units |
| D4 | 0.50 p-units | 1.50 p-units |
| D5 | 2.00 dB | 12.00 dB |
| D6 | ln(1.25) ln units | 1.00 ln units |

A candidate signed run requires `sign × z >= h / 2` (`HYSTERESIS_LOW`).
Sentence boundaries and missing values break runs.
There is no gap bridging.
A run opens a region only if its peak reaches h.
D1, D5, and D6 retain the contiguous part around the peak above `max(h / 2, 0.5 × peak)` (`REGION_PEAK_FRACTION`).
Remainders are processed recursively.
The neighbouring half-window units are shoulders and cannot open another region.
D3 has peak fraction zero.
Its region retains the full candidate run without half-maximum trimming.
Pitch percentile range already narrows the response to a flat stretch.
D1 and D3 need at least two region words (`MIN_REGION_WORDS`).
D5 and D6 need at least one word.
D2 and D4 decode as single events with their sign and marker gates.

R1 scales use train identity clips and additional placebo seeds (`PLACEBO_SEEDS`).
R1 selects one common h for every flag key.
Candidates use `H_GRID` restricted to 1.00–3.00 robust units (`R1_H_RANGE`).
Selection maximises strict local event F1 on train single-level L2 and L3 clips plus identity, placebo, and 20 dB SNR noisy identity controls (`NOISE_SNR_DB`).
All unmatched local regions count, including secondary firings.
No type may lose recall relative to h = 1.00 robust unit.
Ties select the smaller h.
Whole-clip flags are excluded from this selection objective.
The full curve and control counts are saved.

R2 scales use ordered calibration-reader pairs.
Each enabled flag key gets an equal share of the 0.50 false-region/comparison-minute budget (`FALSE_RATE_BUDGET`).
For each key, select the smallest h on the 1.00–12.00 robust-unit grid with 0.05 robust-unit steps (`H_GRID`) that meets its share.
No qualifying h disables only that key.
Whole-clip thresholds are fitted separately from this local budget.
Leave-one-reader-out refits exclude every pair touching the removed reader.
They refit scales, local thresholds, and whole-clip thresholds.
The report saves threshold ranges and disabled-refit counts.
Null checks count both local regions and whole-clip flags.

Whole-clip D1 flags are TEMPO_FAST for negative g and TEMPO_SLOW for positive g.
Whole-clip D3 flags are RANGE_NARROW for negative g only.
They require `abs(g) > clip threshold`.
They are scored in both regimes.
R1 thresholds are fixed at ln(1.25) ln units for D1 and ln(2.00) ln units for D3 (`CLIP_LN`).
The D1 interval is exp(−threshold) through exp(threshold) for the median speech-time ratio.
D3 thresholds apply to the median regularised window ratio.

For R2, collect finite g from calibration-reader pairs per whole-clip dimension.
Its threshold is `3.5 × max(FLOORS[k], 1.4826 × MAD(g), Q68(|g|))` in ln units (`CLIP_H`, `MAD_SCALE`, `Q68`).
The g median is used for MAD and is not subtracted at runtime.
This uses the robust-outlier convention recorded in `docs/PAPERS.md`, entry 53.

The checked-in fit in `models/detector.json` is:

| Local flag keys | R1 h (robust units) | R2 h (robust units) | R2 scale (physical units) |
|---|---|---|---|
| D1−, D1+ | 1.70 | 3.00 | 0.152261 ln units |
| D2− | 1.70 | 2.95 | 0.415128 s |
| D2+ | 1.70 | 1.15 | 0.415128 s |
| D3− | 1.70 | 3.25 | 0.336472 ln units |
| D4− | 1.70 | disabled | 0.665613 p-units |
| D5− | 1.70 | 4.00 | 2.727298 dB |
| D6− | 1.70 | disabled | 0.223144 ln units |

R2 whole-clip thresholds are 0.394989 ln units for D1 and 1.177653 ln units for D3 (`regimes.R2.clip`).

### 5.3 Regimes and unscored differences

R1 compares a participant derived from the baseline performance.
All dimensions can flag and score.
R2 compares another performance.
D1, D2, D3, and D5 can flag and score (`REGIME_DIMS`).
D4 and D6 rows are displayed and never flagged or scored in R2.
R2 volume retains a channel caveat.
There is no automatic channel exclusion.
The same physical departure can score differently in R1 and R2.

R2 also lists unscored differences.
Local candidates use both signs at h = 1.00 robust unit (`DIFFERENCE_H`).
They use the same dimension-specific region rule.
Only flagged regions of the same dimension mask candidates.
Pause candidates in this tier use finite deltas without the flaw sign gates.
The list keeps one largest candidate per signed run and ranks by absolute z.
At most five local differences are listed (`MAX_DIFFERENCES`).
Unflagged whole-clip D1 and D3 differences follow when `abs(g) >= clip threshold / CLIP_H`.
They have no word or time span.
These items report measurements and tolerance-scale multiples without penalties or fixes.
Flag explanations use threshold multiples instead (§6).

The dashboard uses R1 only for a bundled dataset clip against its own baseline.
Every other comparison, including an upload, uses R2.
A dimension without any calibrated local direction has a flags-disabled notice.

## 6. Scores and explanations

For each flagged local unit, `theta = h[flag key] × scale[dimension]`.
Severity is `clip((abs(x) − theta) / (saturation − theta), 0, 1)`.
Saturations are in §5.2.
R2 saturation is at least twice theta (`R2_SAT_THRESHOLD_FACTOR`).
When saturation is at or below theta, a value reaching theta has full severity.

Windowed weights are baseline word-support duration shares.
D2 weights are inverse baseline pause count, with a minimum denominator of one event.
D4 weights are inverse baseline stress-word count, with the same minimum.
Region mass is the sum of unit weight times severity.
Whole-clip mass is severity of g between its clip threshold and `CLIP_SAT`.
R2 also expands whole-clip saturation to at least twice its threshold.
Each dimension's penalty is the sum of local masses and any whole-clip mass.
Its score is `100 × max(0, 1 − penalty / Pmax)` index points.
Overall is the mean of scored dimension scores.

A dimension needs at least 50 % measurable baseline support or a flag (`MIN_MEASUREMENT_COVERAGE`).
A flag permits scoring on partial evidence, including a whole-clip flag.
Coverage is reported in delta and score rows.
D2 coverage uses finite raw boundary measurements with baseline support weights renormalised over actual boundaries.
D4 coverage uses finite stress-point inputs at all words.
Event absence is valid evidence.
Disabled or insufficiently measured dimensions are omitted from the mean.
No scored dimensions gives a null overall score.
Runtime, calibration gates, and Pmax candidates share the scored-dimension mask and averaging function.

`PMAX_START` is 0.40 penalty units for D1, D3, D5, and D6, and 0.50 penalty units for D2 and D4.
Calibration searches a uniform factor (`PMAX_FACTOR_GRID`).
It chooses the factor with the fewest gate violations, then the factor closest to one on a log scale.
Train gates use `GATE_IDENTITY`, `GATE_L1_MIN`, and `GATE_G5_MAX`.
Identity must score 100 index points.
L1-only clips and G1 must score at least 90 index points.
G5 must score at most 50 index points.
Each speech must satisfy G1 >= G3 >= G5.
A null overall score fails a gate.
Validation gates are checked without feeding the fit.
Evaluation reports gates per evaluated split (§8).
The current factor is 0.9076 dimensionless (`models/detector.json`, `report.pmax_factor`).
Fitted Pmax is 0.363040 penalty units for D1, D3, D5, and D6, and 0.453800 penalty units for D2 and D4 (`score.pmax`).
There are no grade bands.

Explanations use deterministic templates without an LLM.
Each local entry reports words, participant and reference spans, sentence or boundary context, recipe name, measurement, threshold, and score effect.
`points_lost` and `overall_if_fixed` remove that entry's mass arithmetically from the current result.
They do not re-analyse audio.
`tolerance_multiple` is `abs(x) / theta` for local flags and `abs(g) / clip threshold` for whole-clip flags.
Each explanation includes one rubric quotation and a fix.
D6 states that spectral change does not measure intelligibility.
The score label is "Reference-relative delivery index".

Local pace and pitch measurements describe the peak window against a reference scaled to the participant's overall measure.
Pace text gives the actual peak-window word count.
A local pace flag beside a whole-clip tempo flag refers to the participant's own overall tempo.
Whole-clip tempo reports exp(g), the median window speech-time ratio.
Whole-clip pitch reports median window ranges in st and exp(g), the regularised ratio.
The ratio median need not equal the ratio of those displayed medians.
Whole-clip entries span the aligned passage and have context "whole passage".
Pause entries use the participant acoustic pause span.
A removed pause uses a point mapped from the reference pause midpoint.
The repair test checks the system's score response (§8).
It does not establish listener effects.

## 7. Dashboard

FastAPI serves one static HTML/JS page.
The gallery supplies precomputed result JSON and audio for use without the backend.
Upload analysis takes audio, transcript, and a bundled or uploaded reference.
Visible stages are decode, align, features, compare, and detect.
The same renderer handles gallery and upload results.

Charts use participant time and warp reference contours through the word map.
Frame rows show pitch in st and level in dB.
Delta rows show the units in §5.1.
Tolerance is supplied per direction (§9).
Local findings, stress markers, and injected-truth markers support inspection.
Whole-passage findings are listed without colouring the full transcript or charts.
A/B playback and clickable words use the aligned spans.
Points lost is the primary finding score.
The R2 threshold note is collapsed.

`gallery.py` bundles identity, L1–L3 sets, G1/G3/G5, clean Greenman, edited Greenman x3_L3, botched Greenman, and an MP3 condition.
The next gallery build sets L3A as the default.
The stress-matrix table comes from evaluation output.
`gallery site` copies the static page and gallery into a Pages folder.
Upload caps are 50 MiB and 180 s (`MAX_UPLOAD_BYTES`, `MAX_UPLOAD_S`).
Magic-byte checks, ffmpeg timeout, and alignment refusal guard ingest.

## 8. Evaluation

Development evaluation defaults to train and validation.
Test requires `--final`, supplied by the kernel only when `CVOICE_FINAL=1`.
Before analysis, final evaluation checks the manifest against calibration.
It records config, detector-file, manifest, and optional project-hash-list hashes.
The ledger rejects repeated configs unless `--force` is supplied.
It does not enforce detector freeze or limit finals across different config hashes.
Those are workflow rules in §0 and `docs/FINAL_EVALUATION_PLAN.md`.

The second final waits for detector freeze and is disclosed as a second look at test.
Both finals must be reported side by side.
The plan allows no third final.
Validation and check readers remain development evidence.
The plan discloses that pause-constant selection checked unedited levels of all baselines, including test.

Regimes are never pooled.
Train is never pooled with validation/test.
Tables report each split and may add an explicit validation+test aggregate.
Figures use validation/test speeches only.
R2 check readers have no speech validation/test split.
Counts derive from evaluated clips and labels, including skipped-edit shortfalls.
Each section records output or an error.
The CLI writes results and exits nonzero on section errors.

`evaluate.SECTIONS` contains:

- **nulls:** R1 validation/test identity and placebo variants, R2 check-reader pairs, and a separate Greenman/Reagan null. Local regions and whole-clip flags each count as one false flag. Rates use participant comparison-minutes. Recordings, variants, readers, and per-reader counts are reported. Zero counts show `RULE_OF_THREE / exposure`. Independent minutes are not established. The train local budget is an operating target.
- **headline:** R1 stored single-level chain-A clips, with L2+L3 headline and separate L1 sensitivity. One-to-one matching uses dimension and sign. Windows need temporal IoU >= 0.50 dimensionless (`IOU_MIN`). Events match the labelled index, midpoint within 0.20 s (`EVENT_TOL_S`), or overlapping spans. Assignment prioritises qualifying matches, then overlap or event closeness. Strict F1 counts unmatched local regions and each whole-clip flag as false. Whole-clip flags cannot match these local edits and form a separate false-positive group. The secondary-exempt view counts local regions only. It exempts labelled secondary dimensions near the edited words (§2.4). Overlap recall and flag precision also use local flags only. Detail includes per-speech counts, misses, false regions, activation, and matched timing errors. Pause errors are separate. The whole-clip table counts flagged clips; strict F1 counts individual whole-clip flags.
- **ladder:** R1 identity, G1, L1 sets, G3, L2 sets, L3 sets, and G5 scores. Each split gets clip counts, minimum/median/maximum, and score-gate violations. Final evaluation checks test gates too.
- **cross_speaker:** stored R2 edits versus clean controls. Each check clip uses every calibration reference; Greenman uses Reagan. Median finite deltas over labelled indices classify direction. Away-edits increase absolute departure and form the detection denominator. Toward-edits and equal departures are repair controls. Unmeasurable cases are separate. Only new or worsened local regions count as flagged. Matching supplies detections. An overlapping new/worsened flag or listed difference supplies "flagged or listed". Detail retains x_clean, x_edited, and list rank. Diagnostic curves are per flag key with fitted thresholds and reader counts. Whole-clip flags are excluded here.
- **cross_botched:** stored R2 G5 scores and whole-clip flags beside clean pairs, separated into check readers and Greenman. Graded rungs generate whole-passage RUSH and MONOTONE at all configured levels on check readers. Each uses every calibration reference. Rows report pair counts and median scores for unedited, type/level, and botched rungs. Graded detection asks for the edited dimension's whole-clip flag. Botched detection asks for both flags. These rungs fit neither thresholds nor gates.
- **trivial:** detector, no flags, flag all, and random regions on validation/test L2+L3 clips. All unmatched local regions count without secondary exemptions. Random counts are averaged before F1 (`RANDOM_SEEDS`). Whole-clip flags are excluded here. No-flags F1 is zero where truths exist.
- **stress:** gain ±6 dB, low-pass 3.4 kHz, white noise 20 dB SNR, MP3 64 kbit/s, and compression (`GAIN_DB`, `LOWPASS_HZ`, `NOISE_SNR_DB`, `MP3_KBPS`, `COMPRESSION`). Compression is 20 dB below the P99 envelope at 4:1 with RMS make-up. Noise and compression also transform validation/test L2+L3 flawed clips. Tables report detections before/after, added/removed flags, exposure, finite/missing score pairs, maximum score change, and compression reduction in dB. Whole-clip additions/removals use dimension presence. WORLD reports absolute R2 flags with F0 ×1.25 and formants ×1.10 (`SPEAKER_TRANSFORM`). Missing finite score pairs give a null maximum.
- **directional:** single flaws use the same span across levels per speech/type. Dimension scores should not increase with level. Missing pauses or measurements below half the labelled change get a pause-measurement diagnosis (`PAUSE_DIAGNOSIS_FRACTION`). Other violations remain "other".
- **chain_b:** both chains render the same single-flaw RUSH/DRAG/MONOTONE plans on validation/test L2+L3 clips. It reports detections, all unmatched local regions, and matched timing errors. Whole-clip flags are excluded. Chain A directional preparations are reused.
- **repair:** detected invertible validation/test L2 edits get inverse and placebo attempts. Detected L3 FADE is the fallback where L2 FADE was not detected. Removal uses shared word indices. Each attempt records scores, new flags including whole-clip additions, and unavailable repairs.
- **validity:** recipe settings versus same-extractor edit-span and labelled-unit detector measurements, per split/type/level. Edge windows may include unedited neighbours. D3 is a regularised ln range ratio; D4 is stress-point change; D6 is ln Q ratio. Paired ratios need finite values and nonzero realised denominators. Empty cells have zero counts and null measurements. This is internal consistency, not independent accuracy.
- **reproducibility:** two uncached analyses compare result JSON for byte identity.
- **device_agreement:** fresh GPU/CPU alignment compares word times and local/whole-clip flag identity on six clips (`DEVICE_AGREEMENT_CLIPS`). CPU runs skip it. Results are per split with an optional validation+test aggregate.

The final evaluation tables are in `docs/evidence_final_782d7df7/`.
It also reports the check-reader populations.
It is not the second final evaluation.

## 9. Result JSON (schema 1)

`pipeline.analyze` returns these blocks:

- `pipeline`: version, detector config hash, alignment device class.
- `regime`, `baseline`, `participant`: comparison metadata and durations in s.
- `words`, `map`: aligned word spans and monotone piecewise-linear time-map knots in s.
- `hop`, `rows`: frame and delta rows. Each delta row includes measurement coverage and `tol = [below, above]`. Tolerances are positive magnitudes in the row's unit; null disables a direction. D3 delta rows use ln units.
- `stress`: baseline and participant stress-word indices.
- `flaws`: local entries and scored whole-clip entries from §6. Entries contain type, dimension, words, spans, severity, measurements, threshold, threshold multiple, points lost, `overall_if_fixed`, context, explanation, rubric text, and fix. Whole-clip entries additionally use `value_unit` to distinguish displayed ratios or st from ln deltas.
- `differences`: unscored R2 entries from §5.3. R1 returns an empty list. Whole-clip differences have null words and spans. Local entries and following whole-clip entries use x-prefixed IDs.
- `truth`: injected-truth markers supplied by the caller.
- `scores`: overall reference-relative delivery index, dimension scores, coverage, scoring notes, and the R2 threshold note.
- `notices`: regime, compatibility, feature fallback, coverage, and disabled-dimension notices.

The time map is piecewise linear through word starts and ends.
Knots that break monotonicity are discarded.
Outside the mapped interval, its slope is one.
Serialisation sorts keys and maps non-finite numbers to null.
Alignment spans are rounded to milliseconds.
Measurements and scores are rounded for display.
No wall-clock values enter result JSON.

Detector JSON is a separate schema-3 artifact (§5.2).
It stores scales, local thresholds per flag key, whole-clip thresholds, enabled dimensions, names, Pmax, config hash, and calibration summary with manifest hash.
`calibration/report.json` stores full R1 selection curves, R2 per-key curves, leave-one-reader-out refits, nuisance controls, and train/validation penalties.

## 10. Repository, compute, and reconstruction

Repository root: `'/home/vihaa/Contrastive voice'`.
Quote the path in shell commands.
Runtime modules cover audio through result JSON (§3–§9).
Build modules cover pooling, edits, passages, dataset, matching, calibration, evaluation, stress, and gallery.
The dashboard is app plus static HTML/JS/CSS.
Origins are in `data/sources_manifest.json`.
Transcript snapshots and hashes are in `data/transcripts/`.
`data/dataset/` holds audio, labels, manifest, QA, and dataset card.
`models/detector.json` holds the fit.

`PreparePool` uses spawn with one aligner per worker, pinned to a device.
CUDA is not initialised in the parent.
Defaults are two workers/GPU or at most four CPU workers (`POOL_WORKERS_PER_GPU`, `POOL_MAX_CPU_WORKERS`).
Workers use one torch thread (`POOL_TORCH_THREADS`).
The dashboard uses the in-process path with two threads (`TORCH_THREADS`).
`CVOICE_DEVICES` and `CVOICE_WORKERS` override the plan.
Batches preserve order and share the alignment cache.
The environment uses locked cpu/gpu extras and a hash-checked aligner checkpoint.

`scripts/stage_project.sh` creates metadata and `project/` under `build/cvoice-project/`.
It stages source, lockfile, manifest, transcripts, and any final ledger, without audio, tests, environments, or caches.
`project_sha256.txt` enables runner integrity checks.
`kaggle/run.py` is the private build kernel using `kaggle/kernel-metadata.json`.
It detects GPUs and selects cpu/gpu dependencies.
The separate CPU metadata file was removed.
Stages are dataset build -> calibrate -> evaluate -> gallery.
Logs record time in s, throughput, and GPU memory.
Dataset/calibration failure stops later stages.
Evaluation failure still permits gallery generation.
The runner exits zero; `STATUS.json` carries the outcome.
Outputs are checksum-listed zip chunks and status.
`scripts/import_run.sh` checks completion and checksums before importing.
It preserves earlier final evidence and its detector.
When both ledgers exist, it rejects an incoming ledger missing an existing entry.

Without `cvoice-sources`, the runner rebuilds nineteen source recordings in temporary storage from manifest origins.
Audio must match recorded SHA-256 hashes.
Downloads retry and honour numeric Retry-After responses.
Transcripts use repository snapshots checked against `data/transcripts/sha256.json`.
Download or reconstruction hash failure stops before dataset building.
Status records the route and checks.
HANDOFF proves the origins route and leaves the later snapshot-route Kaggle proof pending.

Another Kaggle user stages and uploads their own private project dataset.
They change metadata to their username and project source, remove the owner's source mount, and retain internet access.
Exact steps are in `kaggle/run.py`'s docstring.
No owner access grant is needed.
Compare manifest hash and counts for the same snapshot/device.
The reference manifest hash is `8db28b8bc970d1af7a3ce0ff38d80c72eae686b60920909007957dee35d7915c` (`models/detector.json`, `report.manifest_sha256`).
Equal counts alone do not establish identical data.

`kaggle/data/fetch.py` is a separate private CPU kernel for external research corpora.
It fetches inside Kaggle, using public mirrors where required.
It writes converted WAVs in source tars, manifest, licences, log, and status.
Source outcomes are independent; the exit code does not establish completeness.
`CVOICE_PRIORITY2=0` omits second-priority sources.
SEP-28k supplies labels only.
Subset and licence choices are in `docs/research/chain/data/PLAN.md`.
Outputs stay private with source-specific terms.
HANDOFF records partial success and ongoing fixes.
These corpora are separate from the detector dataset.

The delegated lab kernel is work in progress in HANDOFF.
`kaggle/lab/` is absent from the current repository and supplies no detector evidence.
Documentation utilities in `scripts/` do not authorise refreshing parked documents.

## 11. Not claimed

The build does not establish human-flaw accuracy, listener impact, judge validity, universal speaker independence, sub-word timing, or different-performance emphasis or clarity scoring.
It has no human ratings or hand-corrected boundaries for the controlled edits.
The dataset card records that no human has listened to the flawed clips.
A listening pass remains an owner task.
Research in `docs/PAPERS.md` Part 2 is not implemented detector behaviour.

## 12. Submission status

HANDOFF leaves listening, video recording, repository name and licence, repository creation, and publishing to the owner.
The second final evaluation precedes the documentation phase (§0 and §8).
README, technical report, grounding, numbers, and video documents remain parked until the owner asks.
This contract update does not establish that those deliverables are current.
