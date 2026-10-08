# Source of every number

This file gives the source of each number in `docs/technical.md` and in the headline sections of `README.md`. Each row names a file and a JSON path, a table section or a code constant. It describes the frozen detector (`models/detector.json`, sha256 `d5935d3f8eeaf928a143b9b04db0c4250604a6c17f5336af87ef124c090758b6`, configuration `782d7df7589164fa7d06e10571369a28aaee6149834a346cfbe4d90e3832f092`) and its final evaluation (Kaggle kernel cvoice-build version 19, 2026-10-07 IST).

## Short names

The short names are the ones `docs/GROUNDING.md` uses. Run-output paths are relative to the output folder of the final Kaggle run, which is not part of the repository. The files that a reader needs are copied, byte for byte, to `docs/evidence_final_782d7df7/` (checksums in its `SHA256SUMS`).

| Short name | Repository copy | Run output it copies (same sha256) |
|---|---|---|
| R | `docs/evidence_final_782d7df7/results.json` | `eval/results.json` (sha256 `49a306d9…`) |
| A | `docs/evidence_final_782d7df7/addendum.json` and `addendum.md` | `eval/addendum.json`, `eval/addendum.md`; computed after the final evaluation from saved outputs (`src/cvoice/addendum.py`) |
| T | `docs/evidence_final_782d7df7/tables_rendered.md` (cited by section title) | `eval/tables_rendered.md`, re-rendered from R |
| D | `models/detector.json` | `models/detector.json` (sha256 `d5935d3f…`) |
| K | `docs/evidence_final_782d7df7/calibration/report.json` | `calibration/report.json` (sha256 `0f25392b…`) |
| S | `docs/evidence_final_782d7df7/STATUS.json` | `../STATUS.json` |
| F | `models/final_evaluations.json` (also `docs/evidence_final_782d7df7/final_evaluations.json`) | `models/final_evaluations.json` (sha256 `4d13595c…`) |
| C | `docs/evidence_final_782d7df7/dataset_card.md` | `data/dataset/dataset_card.md` |
| M | not copied (5.8 MB) | `data/dataset/manifest.json` (sha256 `d67c9cd9…`); C lists the same recordings |
| G | `gallery/results/<item>.json`, `gallery/index.json`, `gallery/evaluation.json` | rebuilt on CPU with the frozen detector after the final evaluation (`gallery/index.json` `provenance`) |
| E1 | `docs/evidence_final_32cdd86f3d6e/results.json` | the earlier final evaluation (2026-10-02, configuration `32cdd86f…`) |
| L | section 9 of `docs/technical.md` (stated limits, verbatim, numbered as in the review) | the review's stated-limits file with a numbers-and-sources list per limit (not in the repository; the sources are repeated in section 9 below) |

Notation: `rows[split=test, levels=headline (L2+L3)]` means the row of a list whose fields have these values. "Pre-registered" = all predictions counted; "one per change" = one detection per change, same-change duplicates reported separately (introduced after the plan).

## Summary and section 1 (problem, regimes)

| Number | Meaning | Source |
|---|---|---|
| D1 to D9, nine quantities | keys of the comparison | `src/cvoice/config.py` `DIMS`; D `regimes.R1.scales` |
| 0.812; TP 28, FP 9, FN 4; 0.800 and 0.824 | core-8 test F1, L2+L3, pre-registered; per speaker (mobama_weekly_2014, nixon_resignation_1974) | A `accounting.rows[tier=core8, levels=headline (L2+L3), split=test].pre_registered` and `.pre_registered_per_speaker`; A §1 table |
| 0.879 (one per change) | core-8 test F1, L2+L3 | R `headline.groups.core8.by_split_strict[group=all, split=test, levels=headline (L2+L3)]`; A `accounting.rows[…test].count_once` |
| 0.879 (earlier final) | test F1 of configuration `32cdd86f…`, all predictions counted | A `accounting.rows[…test].first_final`; E1 `headline.by_split_strict` (test); F entry `32cdd86f…` |
| 0.46, upper 95 % 0.54 | R2 lockbox, one reference, false regions per comparison-minute, equal source weights | R `lockbox.modes.single.total_local.rate` (0.4601), `.bootstrap_upper95` (0.5377) |
| 1 of 18, 4 of 17 | R2 check readers, single reference, level 3: RUSH, PAUSE_DROPPED detected | R `cross_speaker.modes.single.by_type`; A `r2_by_reader.single`; A §5 "R2 check readers (single)" |
| 30 % | two expert raters gave the same "vocal expression" score | [2], `docs/GROUNDING.md` "Reference-relative comparison" |
| 985 readers (fit set) | R2 fit set size | M `r2_pool.groups[].entries[].null_set` = fit (count); C table, split column |
| six readings (Gettysburg bank), median of five | upload reference bank | `gallery/index.json` `baselines[id=gettysburg_address]` (`consensus_k` 5, 6 `references`) |
| `UPLOAD_REGIME = "R2"` | every upload is R2 | `src/cvoice/app.py` |

## Section 2 (data engineering)

| Number | Meaning | Source |
|---|---|---|
| 9 baselines, split 5 / 2 / 2 | baseline speeches by split | C first table (split column); R `n.<split>.speakers` |
| 21.4–31.1 s, 51–91 words | baseline passage durations and word counts | C first table, columns "passage (s)" and "words" (rows with split train/val/test) |
| 10 (6 + 3 + 1) | LibriVox calibration, check readers, Greenman | C first table rows `gettysburg_*` (calibration, check), `greenman_reagan`; M `readers[].role` |
| 779, 856, 308; 1943 | R2 null-pool readings: Speech Accent Archive (CC BY-NC-SA 4.0), EARS (CC BY-NC 4.0), LibriVox poetry and Gettysburg (public domain); total | M `readers[role=null_reader]` counted by `licence_basis`; C table rows `null_*` by licence column |
| 19 source recordings | entries of the source manifest | `data/sources_manifest.json` `entries` |
| `d67c9cd9…`, byte-identical | dataset manifest of development run v13 (2026-10-06) and of the final run | S `dataset_manifest_sha256`; `STATUS.json` `dataset_manifest_sha256` of development run v13 (not in the repository); `sha256sum` of both `manifest.json` files |
| Core recipe levels (1.20/1.45/1.90; 0.40/0.20/0.06 s; 0.35/0.60/1.20 s; 0.50/0.25/0; 0.5/0.75/1.0; 4/8/14 dB; 0.3/0.6/1.0) | core-8 edit magnitudes | `src/cvoice/config.py` `LEVEL_PARAM`, `PAUSE_FLOOR_S` (0.06), `PAUSE_DROP_MIN_BASE_S` (0.5) |
| fifteen further types | extra recipe types | `src/cvoice/config.py` `FLAW_REGISTRY` entries added after the core 8 (`EXTRA_SINGLE_LEVEL_SETS`) |
| ×1/1.13 to ×1/1.18 | natural-rush word-time compression | `src/cvoice/config.py` `RUSH_RATE` (1.13, 1.15, 1.18) |
| 118; 53, 28, 21, 9, 7 | realisation shortfalls by type | M `realisation_shortfalls` (count by `type`) |
| 82 | events excluded from evaluation truth | R `realisation_shortfalls.excluded_events` |
| 2410 files, 1109.2 min, 9, 1953, 448 | dataset counts | S `dataset_counts` |
| 162, 27, 9, 130, 116, 4 | edited clips by kind: single, ladder, identity, extra_botched, cross, cross_botched | M `clips[].kind` (count) |
| 90 (5), 36 (2), 36 (2) | R1 single-level clips (speakers) per split | R `n.train`, `n.val`, `n.test` (`clips`, `speakers`) |
| 30 groups: 1, 8, 20, 1 | same-text groups by source (accent, EARS, poetry, Gettysburg) | M `r2_pool.groups` (source prefix of `group`) |
| 985, 707, 251 | planned fit, select, lockbox readers | M `r2_pool.groups[].entries[].null_set` (count); C split column |
| 192, 45, 14 | lockbox readers measured (accent, poetry); poetry readings excluded, text not located | R `lockbox.readers_by_source`; R `lockbox.excluded` |

## Section 3 (feature extraction)

| Number | Meaning | Source |
|---|---|---|
| 20 ms | CTC frame | `src/cvoice/config.py` `CTC_FRAME_S` |
| 48 ms, 89 ms | published word-boundary error of wav2vec 2.0 CTC alignment (TIMIT, Buckeye) | [100]; `docs/GROUNDING.md` §11 "Forced alignment" |
| 25 ms, 10 ms | frame and hop | `src/cvoice/config.py` `WIN` = 400 and `HOP` = 160 samples at `SR` = 16 kHz |
| 0.20 s | pause minimum | `src/cvoice/config.py` `PAUSE_MIN_S` |
| five words | window | `src/cvoice/config.py` `WINDOW_WORDS` |
| 0.5 s | dropped-pause eligibility | `src/cvoice/config.py` `PAUSE_DROP_MIN_BASE_S` |
| +1 st, P90 − P10 | pitch-range regulariser and percentiles | `src/cvoice/compare.py` `d3_pitch`; `docs/GROUNDING.md` §3 System |
| MFCC 1–12 | clarity proxy coefficients | `src/cvoice/features.py` `mfcc_delta_magnitude`; `docs/GROUNDING.md` §6 System |
| 0.20 s (D8 final part) | final window of a sentence-final word | `src/cvoice/features.py` `final_pitch_word`; `docs/GROUNDING.md` §8 System |
| scored / shown / listed per regime | keys per regime | D `regimes.R1.enabled`, `regimes.R2.enabled`; `src/cvoice/config.py` `REGIME_DIMS`, `LISTED_DIMS`, `OWNER_LISTED` |
| 0.39 at 0.10 false | D7 lab gate, LibriStutter word-duration ratio | R `real_validation.D7+.reason`; `docs/research/design/LAB_DECISIONS.md` |
| 2 eligible ending events | reason D8 is listed | `src/cvoice/config.py` `OWNER_LISTED['R1']['D8']` |
| 0 of 68 | development run v13 R2 rush positives, reason D9 is listed in R2 | `src/cvoice/config.py` `OWNER_LISTED['R2']['D9']` |
| 12,868 recordings, 48 tests | lab kernel v2 | `docs/research/design/LAB_DECISIONS.md` (source line) |
| precision 0.54, recall 0.15; six labels failed | filled-pause candidate on PodcastFillers; other pattern labels | R `real_validation.labels`; D `regimes.R1.pattern_labels`; `docs/research/design/LAB_DECISIONS.md` |

## Section 4 (detection and calibration)

| Number | Meaning | Source |
|---|---|---|
| 1.4826, 68th percentile | robust scale terms | `src/cvoice/detect.py` module docstring and `fit_scales`; [104] |
| h/2, 0.5 × peak; pitch range h/2 only | region extension rule | `src/cvoice/config.py` `HYSTERESIS_LOW`, `REGION_PEAK_FRACTION` |
| h = 2.15; F1 0.835, TP 76, FP 16, FN 14 | R1 common h and train objective | D `regimes.R1.selected_operating_point` (`h`, `F1`, `TP`, `FP`, `FN`) |
| 680 of 1000 | bootstrap draws choosing 2.15 | D `regimes.R1.selection_bootstrap.chosen_h_counts["2.15"]`, `.draws` |
| h = 3.05; 0.1484 ln | D9 h; clean alignment-noise floor | D `regimes.R1.natural_rush_selection` (`h`, `grid_min_h`, `noise_floor_ln`) |
| 0.0833, 0.5/min | R2 per-key share and budget | D `regimes.R2.null.budget_per_key`; `src/cvoice/config.py` `FALSE_RATE_BUDGET` |
| 0.05 per clip, 0.025 per key | R2 clip budget | `src/cvoice/config.py` `FALSE_CLIP_RATE_BUDGET`; D `regimes.R2.null.clip_budget_per_key` |
| R1 thresholds ×1.227 / ×0.815, ±0.3225 s, ×0.485, 1.075 p, ×0.619, −4.3 dB, ×0.862 | h × scale | D `regimes.R1.h` × `regimes.R1.scales` (D1 0.09531, D2 0.15, D3 0.336472, D4- 0.5, D5 2.0, D6 0.223144, D9 0.04879); ratios are exp(±threshold) |
| R2 single ×2.194 / ×0.452, +0.981 / −1.504 s, ×0.273, −10.08 dB | h × scale | D `regimes.R2.h` × `regimes.R2.scales`; K `R2_modes.single.physical_thresholds` |
| R2 consensus ×2.052 / ×0.581, +1.008 / −0.805 s, ×0.303, −9.0 dB | h × scale | D `regimes.R2_consensus.h` × `.scales`; K `R2_modes.consensus5.physical_thresholds` |
| whole clip 0.223 / 0.693; 0.612 / 0.702; 0.392 / 0.506 | D1 / D3 clip thresholds, ln | D `regimes.R1.clip`, `regimes.R2.clip`, `regimes.R2_consensus.clip` |
| L3 edit ×1.90, +1.20 s, to 0.06 s, 0, 1.0, −14 dB, ×1/1.18 | level-3 magnitudes | `src/cvoice/config.py` `LEVEL_PARAM`, `PAUSE_FLOOR_S`, `RUSH_RATE` |
| 2θ | R2 minimum saturation | `src/cvoice/config.py` `R2_SAT_THRESHOLD_FACTOR` |
| 0.4584 | Pmax factor | D `report.pmax_factor`; D `score.pmax` = `PMAX_START` × 0.4584 |
| 100, 90, 50 | score gates | `src/cvoice/config.py` `GATE_IDENTITY`, `GATE_L1_MIN`, `GATE_G5_MAX` |
| 0 violations train, val, test | gate check | D `report.gates_train` (50 clips), `report.gates_val` (20 clips); T "Score by rung of the bad spectrum (R1)", "Score gates (violations)" |
| 100, 100, 99.3, 96.1, 94.7, 76.5, 45.9 | test median scores: identity, G1, L1, G3, L2, L3, G5 | R `ladder.rows[split=test]` (median column); T "Score by rung of the bad spectrum (R1)" |

## Section 5 (causal explainability and temporal grounding)

| Number | Meaning | Source |
|---|---|---|
| 0.20 s, 0.775 | natural-rush rule: reference pause minimum and kept-fraction limit | `src/cvoice/config.py` `PAUSE_MIN_S`, `NATURAL_RUSH_PAUSE_KEPT_MAX` = sqrt(`RUSH_PAUSE_KEEP[0]`) |
| 56 of 59; DEEMPHASIS 4 of 7 (2 MONOTONE, 1 RUSH) | core-8 cause labels, val+test, L2+L3 | A `labels["core8|headline (L2+L3)|val+test"]`; A §2 tables (confusion) |
| 7 of 13; HESITATION 7 of 8 | synthetic-only cause labels, val+test, L2+L3 | A `labels["synthetic_only|headline (L2+L3)|val+test"]`; A §2 |
| every rush and natural-rush edit | RUSH/NATURAL_RUSH label | A `rush_confusion` |
| D1→D9 cell | activation matrix | `docs/evidence_final_782d7df7/figures/activation_matrix.png`; R `headline.activation` |
| 16 events; 10 ms, 29 ms; 128 ms, 149 ms | pause edge errors, val+test, L2+L3 | R `headline.groups.core8.pause_localisation`; T "Pause localisation error (matched boundary events)"; L 16 |
| 14 of 35; 4/7, 4/8, 0/6, 3/6, 3/8; 867 ms | window regions with both edges within 0.20 s, by type; MONOTONE onset 90th percentile | R `headline.groups.core8.grounding[split=val+test]` (`both_edges_within_tolerance`, `matched`, `onset_p90_ms`); L 16 |
| 15.80-17.14 s, 0.87 s, 1.62 s, 86 %, 3.0x, 23 %, 91.0 | quoted explanation | G `L3A.json` `flaws[id=d1-003]` (`text`, `p`, `participant`, `baseline`, `overall_if_fixed`) |
| 12 of 12, 10 of 10 | repairs removing the flag; placebos keeping it (val, test) | R `repair.by_type`; T "Repair test (inverse edit vs placebo)" |

## Section 6 (evaluation)

### 6.1 and 6.2: R1

| Number | Meaning | Source |
|---|---|---|
| 2026-10-02 | date of the plan and of the earlier final evaluation | `docs/FINAL_EVALUATION_PLAN.md` |
| IoU 0.5; 0.20 s | matching rules | `src/cvoice/config.py` `IOU_MIN`, `EVENT_TOL_S` |
| train 74/20/6, 0.851 [0.795, 0.907] | pre-registered, train L2+L3 | A `accounting.rows[core8, headline (L2+L3), train].pre_registered`, `.pre_registered_per_speaker.f1_ci95` |
| train 76/8/10/4, 0.927 [0.885, 0.969] | one per change, train | A `accounting.rows[…train].count_once`, `.count_once_interval`; R `headline.groups.core8.by_split_strict[group=all, split=train]` |
| train 76/16/4, 0.884 | earlier final, train | A `accounting.rows[…train].first_final` |
| val 30/13/2, 0.800 (0.769, 0.833) | pre-registered, val, per speaker (eisenhower, lbush) | A `accounting.rows[…val].pre_registered`, `.pre_registered_per_speaker` |
| val 30/9/4/2, 0.845 (0.811, 0.882) | one per change, val | A `accounting.rows[…val].count_once`; T "Recovery of the synthetic edit: R1 event F1" |
| val 30/12/2, 0.811 | earlier final, val | A `accounting.rows[…val].first_final` |
| test 28/9/4, 0.812 (0.800, 0.824); 29/5/3/3, 0.879 (0.848, 0.909); 29/5/3, 0.879 | test, three accountings | A `accounting.rows[…test]`; A §1 table |
| test L1 3/2/13, 0.286; 5/0/0/11, 0.476; 10/0/6, 0.769 | level 1, test | A `accounting.rows[core8, sensitivity (L1), test]` |
| 4 of 4 except MONOTONE 2 of 4, DEEMPHASIS 3 of 4; RUSH 3 of 4 pre-registered | per type, test L2+L3 | R `headline.groups.core8.magnitude` (count `detected` by type, split test, levels 2–3); A §1 "Count-once rule" table (1 same-change detection, RUSH, test) |
| 31 of 32; 32 of 34 | overlap view, test L2+L3 | A `overlap[split=test, levels=headline (L2+L3)]`; T "Overlap view" |
| 2/10, 1/4, 1/4; 0.167 | NATURAL_RUSH detected (train, val, test); lab-passed tier test F1, both accountings | R `headline.groups.lab_passed.magnitude`; A `accounting.rows[lab_passed, headline (L2+L3), test]` |
| 0.211 | synthetic-only tier test F1 | A `accounting.rows[synthetic_only, headline (L2+L3), test]` |
| 0 of 28; 0.3225 s; 0.15–0.30 s | WORD_BY_WORD detected on test; D2 threshold; recipe silences | R `headline.groups.synthetic_only.magnitude` (type WORD_BY_WORD, split test); D `regimes.R1`; `src/cvoice/config.py` `READING_PAUSE_S` |
| 0 in 5.89 min; 0 in 5.93 min | R1 null false regions, test and val | R `nulls.rows`; T "False flags per minute on nulls" |

### 6.3: R2

| Number | Meaning | Source |
|---|---|---|
| fit 0.491 (0.450) [0.545], met; 0.468 (0.457) [0.564], met | fit set, single and median of five | K `R2_modes.single.fit.total_local`, `R2_modes.consensus5.fit.total_local` (`rate`, `pooled_rate`, `bootstrap_upper95`, `budget_status`) |
| select 0.549 (0.482) [0.640], not met; 0.536 (0.401) [0.670], not met on covered sources | select set | K `R2_modes.<mode>.select.total_local` |
| lockbox 0.460 (0.522) [0.538]; 0.516 (0.530) [0.684]; statuses | lockbox | R `lockbox.modes.<mode>.total_local`; A `lockbox`; T "R2 lockbox false regions (final evaluation, both modes)" |
| clip 0.046 / 0.050; 0.046 / 0.068; 0.057 / 0.084 | whole-clip false flags per null clip (single / five) | K `R2_modes.<mode>.{fit,select}.false_clip_flags_per_clip`; R `lockbox.modes.<mode>.false_clip_flags_per_clip` |
| MONOTONE 17/18, PAUSE_INTRUSIVE 14/18, FADE 13/18, HESITATION 13/18, LOW_EFFORT 11/18, DRAG 6/17, PAUSE_DROPPED 4/17, RUSH 1/18 | check readers, single reference, level 3 | R `cross_speaker.modes.single.by_type`; A `r2_by_reader.single`; A §5 table |
| 4 of 36 | Greenman against Reagan | R `cross_speaker.modes.single.summary.train` (`detected`, `truth`) |
| rush 0/1/11, monotone 14/18/18 of 18; 2 of 18 unedited | whole-passage edits, single reference | R `cross_botched.ladder` |
| 2 flags in 7.76 min | check-reader nulls (both D3- whole clip) | R `nulls.rows`; T "False flags per minute on nulls", reader-level table |

### 6.4: stress

| Number | Meaning | Source |
|---|---|---|
| eleven conditions | stress conditions | R `stress.rows` (distinct `condition`); T "Stress matrix" |
| every R1 val and test cell (added/min, kept) and every R2 check-reader cell | stress table | A `stress_rows[split, condition, regime]` (columns: added/min, kept count, kept fraction); A §6 "Stress matrix (all rows)"; R `stress.rows` |
| val added/min: gain +6 0.21, gain −6 0.28, MP3 0.07, low-pass 0.38, WORLD 0.94, reverb 0.89, white noise 2.63, phone 1.84, compression 6.48, babble 20 dB 8.41, babble 10 dB 24.5; kept 1.00, 1.00, 1.00, 0.96, 0.96, 0.95, 0.91, 0.89, 0.78, 0.89, 0.65 | R1 val rows, rounded to 2 decimals or 3 significant digits | A `stress_rows[split=val, regime=R1]` (`added/min`, kept fraction); A §6 "Stress matrix (all rows)" |
| test added/min: 0.14, 0.28, 0.14, 1.46, 0.76, 0.61, 1.85, 5.52, 2.60, 13.2, 26.2; kept 1.00, 1.00, 1.00, 0.94, 0.99, 0.99, 0.91, 0.87, 0.76, 0.85, 0.60 (same order) | R1 test rows | A `stress_rows[split=test, regime=R1]` |
| check readers, one reference, added/min: 0 for gain, MP3, low-pass, WORLD, reverb and compression; white noise 0.26, phone 0.39, babble 20 dB 0.13, babble 10 dB 2.06 | R2 check-reader rows | A `stress_rows[split=check readers, regime=R2, reference mode=single]` |
| 7.76 min | check-reader comparison-minutes, single reference | R `stress.rows[split=check readers]` minutes; L 17 |

### 6.5: baselines

| Number | Meaning | Source |
|---|---|---|
| 0.800 / 0.845; 0.812 / 0.879 | detector, both accountings, val / test | A `baselines`; A §6 "Trivial baselines" |
| 0.016 / 0.045; 0.016 / 0.056 | flag everything / random | A `baselines` (methods `flag_all`, `random`); R `trivial` |
| 0.217 / 0.218; 0.247 / 0.261; h 2.75 | reference-free, detector h / train-chosen h | A `baselines` (method `reference_free (detector h)`, `reference_free (train-chosen h=2.75)`); R `trivial.reference_free` |
| 0.295; 0.407; TP 12, FP 15, FN 20 | reference-free with own scales and h (added after the final evaluation) | A `baselines` (method `reference_free (own scales and h; …)`); A `local.reference_free_fair`; A §4 |

### 6.6: further checks

| Number | Meaning | Source |
|---|---|---|
| 5 violations in 205 cells; causes | directional test | R `directional.violations`, `directional.cells`; T "Directional test" |
| 24 pairs, 22 and 22 | chain A against chain B | R `chain_b.rows`; T "Chain A versus chain B" |
| 0.436 | lowest median ratio, test MONOTONE L3 | T "Feature internal consistency"; R `validity.rows` |
| 6 clips, 8 recordings, 0 ms | GPU against CPU | R `device_agreement.rows[split=val+test]` (or the val and test rows) |
| 89,227 bytes, identical | repeatability | R `reproducibility` |

## Section 7 (dashboard)

| Number | Meaning | Source |
|---|---|---|
| 180 s | upload length limit | `src/cvoice/config.py` `MAX_UPLOAD_S` |
| 17 examples | gallery items | `gallery/index.json` `items` |
| 320 to 1440 px; 0 failures, 0 console errors | browser harness result (2026-10-08 07:29 IST) | browser harness output `checks.json` (`passed`, `consoleErrors`, `gallery.items`, `gallery.failures`; not in the repository) |
| 86.11 and the figure values | screenshot of example L3A | G `L3A.json` `scores.overall`, `flaws[]` |

## Section 8 (reproducibility)

| Number | Meaning | Source |
|---|---|---|
| version 19, 2 × T4 | Kaggle kernel version and devices | the Kaggle kernel page of cvoice-build (version 19, private); S `device_plan.gpus` |
| 1364.8, 1135.8, 4402.5, 51.3, 167.7, 7228.9 s | stage seconds, bootstrap, total | S `stages[].seconds`, `bootstrap_seconds`, `total_seconds` |
| 117.8 s | lockbox time inside evaluation | R `lockbox.seconds` |
| `d67c9cd9…`, `d5935d3f…`, `782d7df7…`, `49a306d9…` | hashes | S `dataset_manifest_sha256`, `detector.config_sha256`; `sha256sum models/detector.json`, `sha256sum docs/evidence_final_782d7df7/results.json`; F entry `782d7df7…` (`detector_sha256`) |
| 162 clips, 24 of 24 rows | CPU re-run of the frozen detector | A `local.reproduction`, `local.clips`; A §7 |
| 561 passed, 2 deselected | `pytest -q` on 2026-10-08 IST (about 21:45 IST) | command output; `README.md` "Tests" |
| ruff clean | `ruff check --select F,E9 src kaggle tests` on 2026-10-08 IST | command output |

## Section 9 (limits)

Each limit gives, in `L`, a "Numbers and sources" list. The numbers of the limits come from these sources (repository copies as above):

| Limit | Sources |
|---|---|
| 1 | `src/cvoice/config.py` `RUSH_RATE`; R `validity.natural_rush_recovery`; D `regimes.R1.natural_rush_selection` (`threshold_ln` 0.14881, `noise_floor_ln` 0.14842, `control_max_abs_x_ln` 0.318); K `report.alignment_noise_floor.rows`; R `headline.groups.lab_passed.magnitude`, `.grounding`; R `real_validation.labels.natural_rush.product_measure` |
| 4 | G `natural_rush.json` (`flaws[id=d1-003]` text and `points_lost` 3.25; `flaws[id=d9-002]` evidence); R `stress.rows[…].added_by_key`; A `stress_by_speaker[].added_by_key_per_speaker`; K `report.alignment_noise_floor.identity_shift_640ms` |
| 8 | R `cross_speaker.modes.single.summary.train`, `cross_speaker.modes.single.by_type`; A `r2_by_reader.single`; R `lockbox`; R `expectation_table.R2` |
| 11 | K `R2_modes.single.physical_thresholds`; D `regimes.R2.clip.D1`; R `cross_speaker.modes.single.by_type`; A `r2_by_reader.single`; A `accounting.rows` |
| 12 | R `lockbox.modes.<mode>.total_local`, `.false_clip_flags_per_clip`, `.source_weights`; R `lockbox.limits`; A `lockbox` |
| 13 | D `regimes.R1.natural_rush_selection`; R `headline.groups.lab_passed.magnitude`, `.grounding`; R `stress.rows[val, white noise 20 dB SNR, R1].added_by_key.D9-`; A `stress_by_speaker` |
| 16 | R `headline.groups.core8.grounding` (split val+test); R `headline.groups.core8.pause_localisation` |
| 17 | R `stress.rows`; A `stress_by_speaker`; R `stress.rows[split=train, regime=R2]`; R `stress.rows[split=check readers]`; R `device_agreement` |
| 18 | T "Expectation table" (no listening check); R `real_validation.labels`; A `labels`, `rush_confusion`; `src/cvoice/config.py` `NATURAL_RUSH_PAUSE_KEPT_MAX` |
| 19 | A `accounting.rows`; R `headline.groups.core8.by_split_strict[test]`; E1 `headline.by_split_strict[test]`; F entry `32cdd86f…`; R `n.test.speakers`; C baselines table |

## README.md headline sections

| Number in README.md | Source |
|---|---|
| 17 examples; 86.11; six flagged regions; 0.87 s against 1.62 s; 4.89 points | G `index.json` `items`; G `L3A.json` `scores.overall`, `flaws` (6), `flaws[id=d1-003]` (`participant`, `baseline`, `points_lost`) |
| ×2.19 slower, ×0.45 faster (R2 local pace) | D `regimes.R2.h` × `regimes.R2.scales` (D1); K `R2_modes.single.physical_thresholds` |
| six LibriVox readings, median of five | `gallery/index.json` `baselines[id=gettysburg_address]` |
| `782d7df7…`, `d5935d3f…`, 2 × T4, 2026-10-07 IST | as section 8 |
| val 30/13/2, 0.800 (0.769, 0.833); 30/9/4/2, 0.845 (0.811, 0.882) | as section 6.2 |
| test 28/9/4, 0.812 (0.800, 0.824); 29/5/3/3, 0.879 (0.848, 0.909) | as section 6.2 |
| 2026-10-02, `32cdd86f…`, 0.879 (29/5/3) | as section 6.2 |
| level 1 test 0.286 and 0.476 | A `accounting.rows[core8, sensitivity (L1), test]` |
| 0 false regions in 5.89 comparison-minutes | R `nulls.rows` |
| 4 of 18 (train 2/10, validation 1/4, test 1/4) | R `headline.groups.lab_passed.magnitude` |
| 0.46 (0.54), 0.057; 0.52 (0.68), 0.084 | R `lockbox.modes.<mode>.total_local`, `.false_clip_flags_per_clip` |
| 0.5 per minute, 0.05 per clip | `src/cvoice/config.py` `FALSE_RATE_BUDGET`, `FALSE_CLIP_RATE_BUDGET` |
| monotone 17 of 18, fade 13 of 18, dropped pause 4 of 17, rush 1 of 18 | R `cross_speaker.modes.single.by_type` |
| Limits list: 1.3/min Amharic, 1.0/min Arabic; 0.15 s; others | dashboard wording of limits 1, 4, 8, 11, 12, 13, 16, 17, 18, 19 in L; sources as section 9 above |
