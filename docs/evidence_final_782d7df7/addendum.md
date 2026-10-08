# Evaluation addendum (computed after the final evaluation)

Computed after the final evaluation by `python -m cvoice.addendum` (src/cvoice/addendum.py) from the saved outputs of the final run; no number below was measured on Kaggle again.

Inputs: `eval/results.json` sha256 49a306d9cf9f, `models/detector.json` sha256 d5935d3f8eea, `models/final_evaluations.json` sha256 4d13595cc067, `calibration/report.json` sha256 0f25392b9629, `docs/evidence_final_32cdd86f3d6e/results.json` sha256 caf05846ac35. Detector config 782d7df75891; detector.json sha256 d5935d3f8eea equals the final-evaluation entry of that config in models/final_evaluations.json.

## 1. Headline accounting: pre-registered first (findings 0, 2)

Pre-registered accounting (pre-registered: every region not matched by its own key is false; the plan calls it "all predictions counted" (docs/FINAL_EVALUATION_PLAN.md item 4)): core8 L2+L3 test F1 0.812 (TP 28 / FP 9 / FN 4). One-detection-per-change accounting (introduced after the plan: one detection per change; same-change duplicates reported separately): 0.879. The test split was evaluated twice: the first final evaluation (config 32cdd86f3d6e, an earlier detector without the speech-tempo key D9, all predictions counted) gave 0.879 (29/5/3); that result was seen before the redesign.

Pre-registered: TP = count-once TP minus same-change detections; FP = every region not matched by its own key (count-once FP + duplicates + same-change detections); FN = count-once FN plus same-change detections. Per-speaker values come from the local re-run, whose counts equal the saved ones (section 7).

| tier | levels | split | pre-registered TP/FP/FN | pre-registered F1 | pre-registered F1 interval or per speaker | count-once TP/FP/dup/FN | count-once F1 | count-once F1 interval (saved) | same-change detections | first final (32cdd86f) TP/FP/FN | first final F1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| core8 | headline (L2+L3) | train | 74/20/6 | 0.851 | percentile bootstrap [0.795, 0.907] (in-sample, 5 speaker clusters, coverage not assured) | 76/8/10/4 | 0.927 | percentile bootstrap [0.885, 0.969] (in-sample, 5 speaker clusters, coverage not assured) | 2 | 76/16/4 | 0.884 |
| core8 | headline (L2+L3) | val | 30/13/2 | 0.8 | per speaker: eisenhower_farewell_1961 0.769, lbush_radio_2001 0.833; range [0.769, 0.833] | 30/9/4/2 | 0.845 | per speaker: eisenhower_farewell_1961 0.811, lbush_radio_2001 0.882; range [0.811, 0.882] | 0 | 30/12/2 | 0.811 |
| core8 | headline (L2+L3) | test | 28/9/4 | 0.812 | per speaker: mobama_weekly_2014 0.8, nixon_resignation_1974 0.824; range [0.8, 0.824] | 29/5/3/3 | 0.879 | per speaker: mobama_weekly_2014 0.848, nixon_resignation_1974 0.909; range [0.848, 0.909] | 1 | 29/5/3 | 0.879 |
| core8 | headline (L2+L3) | val+test | 58/22/6 | 0.806 | per speaker: eisenhower_farewell_1961 0.769, lbush_radio_2001 0.833, mobama_weekly_2014 0.8, nixon_resignation_1974 0.824; range [0.769, 0.833] | 59/14/7/5 | 0.861 | per speaker: eisenhower_farewell_1961 0.811, lbush_radio_2001 0.882, mobama_weekly_2014 0.848, nixon_resignation_1974 0.909; range [0.811, 0.909] | 1 | 59/17/5 | 0.843 |
| core8 | sensitivity (L1) | train | 9/2/31 | 0.353 | percentile bootstrap [0.292, 0.392] (in-sample, 5 speaker clusters, coverage not assured) | 11/0/0/29 | 0.431 | percentile bootstrap [0.333, 0.519] (in-sample, 5 speaker clusters, coverage not assured) | 2 | 23/3/17 | 0.697 |
| core8 | sensitivity (L1) | val | 3/0/13 | 0.316 | per speaker: eisenhower_farewell_1961 0.222, lbush_radio_2001 0.4; range [0.222, 0.4] | 3/0/0/13 | 0.316 | per speaker: eisenhower_farewell_1961 0.222, lbush_radio_2001 0.4; range [0.222, 0.4] | 0 | 8/1/8 | 0.64 |
| core8 | sensitivity (L1) | test | 3/2/13 | 0.286 | per speaker: mobama_weekly_2014 0.2, nixon_resignation_1974 0.364; range [0.2, 0.364] | 5/0/0/11 | 0.476 | per speaker: mobama_weekly_2014 0.4, nixon_resignation_1974 0.545; range [0.4, 0.545] | 2 | 10/0/6 | 0.769 |
| core8 | sensitivity (L1) | val+test | 6/2/26 | 0.3 | per speaker: eisenhower_farewell_1961 0.222, lbush_radio_2001 0.4, mobama_weekly_2014 0.2, nixon_resignation_1974 0.364; range [0.2, 0.4] | 8/0/0/24 | 0.4 | per speaker: eisenhower_farewell_1961 0.222, lbush_radio_2001 0.4, mobama_weekly_2014 0.4, nixon_resignation_1974 0.545; range [0.222, 0.545] | 2 | 18/1/14 | 0.706 |
| lab_passed | headline (L2+L3) | train | 2/6/8 | 0.222 | percentile bootstrap [0, 0.348] (in-sample, 5 speaker clusters, coverage not assured) | 2/6/0/8 | 0.222 | percentile bootstrap [0, 0.348] (in-sample, 5 speaker clusters, coverage not assured) | 0 | n/a | n/a |
| lab_passed | headline (L2+L3) | val | 1/6/3 | 0.182 | per speaker: eisenhower_farewell_1961 0.25, lbush_radio_2001 0; range [0, 0.25] | 1/6/0/3 | 0.182 | per speaker: eisenhower_farewell_1961 0.25, lbush_radio_2001 0; range [0, 0.25] | 0 | n/a | n/a |
| lab_passed | headline (L2+L3) | test | 1/7/3 | 0.167 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.286; range [0, 0.286] | 1/7/0/3 | 0.167 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.286; range [0, 0.286] | 0 | n/a | n/a |
| lab_passed | headline (L2+L3) | val+test | 2/13/6 | 0.174 | per speaker: eisenhower_farewell_1961 0.25, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.286; range [0, 0.286] | 2/13/0/6 | 0.174 | per speaker: eisenhower_farewell_1961 0.25, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.286; range [0, 0.286] | 0 | n/a | n/a |
| lab_passed | sensitivity (L1) | train | 0/2/5 | 0 | degenerate [0, 0] (no spread across the resampled clusters) (in-sample, 5 speaker clusters, coverage not assured) | 0/2/0/5 | 0 | degenerate [0, 0] (no spread across the resampled clusters) (in-sample, 5 speaker clusters, coverage not assured) | 0 | n/a | n/a |
| lab_passed | sensitivity (L1) | val | 0/0/2 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0; range [0, 0] | 0/0/0/2 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0; range [0, 0] | 0 | n/a | n/a |
| lab_passed | sensitivity (L1) | test | 0/2/2 | 0 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] | 0/2/0/2 | 0 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] | 0 | n/a | n/a |
| lab_passed | sensitivity (L1) | val+test | 0/2/4 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] | 0/2/0/4 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] | 0 | n/a | n/a |
| synthetic_only | headline (L2+L3) | train | 20/55/75 | 0.235 | percentile bootstrap [0.195, 0.27] (in-sample, 5 speaker clusters, coverage not assured) | 20/55/0/75 | 0.235 | percentile bootstrap [0.195, 0.27] (in-sample, 5 speaker clusters, coverage not assured) | 0 | n/a | n/a |
| synthetic_only | headline (L2+L3) | val | 5/19/23 | 0.192 | per speaker: eisenhower_farewell_1961 0.16, lbush_radio_2001 0.222; range [0.16, 0.222] | 5/19/0/23 | 0.192 | per speaker: eisenhower_farewell_1961 0.16, lbush_radio_2001 0.222; range [0.16, 0.222] | 0 | n/a | n/a |
| synthetic_only | headline (L2+L3) | test | 8/28/32 | 0.211 | per speaker: mobama_weekly_2014 0.176, nixon_resignation_1974 0.238; range [0.176, 0.238] | 8/28/0/32 | 0.211 | per speaker: mobama_weekly_2014 0.176, nixon_resignation_1974 0.238; range [0.176, 0.238] | 0 | n/a | n/a |
| synthetic_only | headline (L2+L3) | val+test | 13/47/55 | 0.203 | per speaker: eisenhower_farewell_1961 0.16, lbush_radio_2001 0.222, mobama_weekly_2014 0.176, nixon_resignation_1974 0.238; range [0.16, 0.238] | 13/47/0/55 | 0.203 | per speaker: eisenhower_farewell_1961 0.16, lbush_radio_2001 0.222, mobama_weekly_2014 0.176, nixon_resignation_1974 0.238; range [0.16, 0.238] | 0 | n/a | n/a |
| synthetic_only | sensitivity (L1) | train | 0/26/47 | 0 | degenerate [0, 0] (no spread across the resampled clusters) (in-sample, 5 speaker clusters, coverage not assured) | 0/26/0/47 | 0 | degenerate [0, 0] (no spread across the resampled clusters) (in-sample, 5 speaker clusters, coverage not assured) | 0 | n/a | n/a |
| synthetic_only | sensitivity (L1) | val | 0/6/14 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0; range [0, 0] | 0/6/0/14 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0; range [0, 0] | 0 | n/a | n/a |
| synthetic_only | sensitivity (L1) | test | 0/9/19 | 0 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] | 0/9/0/19 | 0 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] | 0 | n/a | n/a |
| synthetic_only | sensitivity (L1) | val+test | 0/15/33 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] | 0/15/0/33 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] | 0 | n/a | n/a |

### Count-once rule as the code applies it (finding 21)

One detection per change. A truth of a linked key (config.SAME_CHANGE: D9- measures the D1- change) is detected by its own-key region (IoU >= 0.5) or its own-key whole-clip flag; when there is none, the same-change region with the largest |z| within half a window (2 words) is the detection, without an IoU test. Every other same-change region of that change is a duplicate, not a false region. A second own-key region on the same edit that fails IoU is a false region. The frozen registry text printed in tables.md ("A region of a same_change key within half a window of a truth of its value key duplicates that change's detection") describes only the duplicate case; the registry string and its sha256 are unchanged.

### Stated limits of the count-once rule (finding 2)

- Asymmetry: a speech-tempo (D9-) region within two words of a rush edit counts as its detection without the IoU test, while a second own-key region on the same edit that fails IoU counts as a false region.
- The h selection counted D1- and D9- separately (detector.json regimes.R1.natural_rush_selection.limit: "the common (D9 off) and speech-tempo (D9 only) components are decoded and counted separately, so a D1- and a D9- false region on the same words count as two false regions in this objective"); it reports 2 same-change duplicates on train (calibration/report.json R1_selected), against 10 in the evaluation train row.

| levels | split | count-once TP | of them same-change detections (no IoU test) | by type | false regions | of them own-key regions on the injected edit | by key |
|---|---|---|---|---|---|---|---|
| headline (L2+L3) | train | 76 | 2 | {"RUSH": 2} | 8 | 4 | {"D1-": 3, "D3-": 1} |
| headline (L2+L3) | val | 30 | 0 | {} | 9 | 2 | {"D5-": 2} |
| headline (L2+L3) | test | 29 | 1 | {"RUSH": 1} | 5 | 3 | {"D3-": 2, "D1-": 1} |
| headline (L2+L3) | val+test | 59 | 1 | {"RUSH": 1} | 14 | 5 | {"D5-": 2, "D3-": 2, "D1-": 1} |
| sensitivity (L1) | train | 11 | 2 | {"RUSH": 2} | 0 | 0 | {} |
| sensitivity (L1) | val | 3 | 0 | {} | 0 | 0 | {} |
| sensitivity (L1) | test | 5 | 2 | {"RUSH": 2} | 0 | 0 | {} |
| sensitivity (L1) | val+test | 8 | 2 | {"RUSH": 2} | 0 | 0 | {} |

## 2. Cause-label accuracy (finding 3)

For each detected truth: the title type the product shows for the detecting region (after grouping; patterns.annotate) and its pattern chip, against the injected type. Correct = the injected type is the title type or the pattern chip. Recovery elsewhere is scored by dimension and direction only. The RUSH / NATURAL_RUSH rule constant NATURAL_RUSH_PAUSE_KEPT_MAX = sqrt(RUSH_PAUSE_KEEP[0]) = 0.775 comes from the recipe parameters (config.RUSH_PAUSE_KEEP), and the rule is checked here only on clips made by those recipes.

| tier | levels | split | correct label / detected truths | interval | by injected type |
|---|---|---|---|---|---|
| core8 | headline (L2+L3) | train | 73/76 | 95% Wilson (pooled; clusters ignored) [0.89, 0.986] | DEEMPHASIS 6/7; DRAG 10/10; FADE 10/10; MONOTONE 9/9; MUMBLE 9/10; PAUSE_DROPPED 10/10; PAUSE_INTRUSIVE 9/10; RUSH 10/10 |
| core8 | sensitivity (L1) | train | 11/11 | 95% Wilson (pooled; clusters ignored) [0.741, 1] | PAUSE_DROPPED 4/4; PAUSE_INTRUSIVE 5/5; RUSH 2/2 |
| core8 | headline (L2+L3) | val | 28/30 | 95% Wilson (pooled; clusters ignored) [0.787, 0.982] | DEEMPHASIS 2/4; DRAG 4/4; FADE 2/2; MONOTONE 4/4; MUMBLE 4/4; PAUSE_DROPPED 4/4; PAUSE_INTRUSIVE 4/4; RUSH 4/4 |
| core8 | sensitivity (L1) | val | 3/3 | 95% Wilson (pooled; clusters ignored) [0.439, 1] | PAUSE_DROPPED 2/2; PAUSE_INTRUSIVE 1/1 |
| core8 | headline (L2+L3) | test | 28/29 | 95% Wilson (pooled; clusters ignored) [0.828, 0.994] | DEEMPHASIS 2/3; DRAG 4/4; FADE 4/4; MONOTONE 2/2; MUMBLE 4/4; PAUSE_DROPPED 4/4; PAUSE_INTRUSIVE 4/4; RUSH 4/4 |
| core8 | sensitivity (L1) | test | 5/5 | 95% Wilson (pooled; clusters ignored) [0.566, 1] | PAUSE_DROPPED 2/2; PAUSE_INTRUSIVE 1/1; RUSH 2/2 |
| core8 | headline (L2+L3) | val+test | 56/59 | 95% Wilson (pooled; clusters ignored) [0.861, 0.983] | DEEMPHASIS 4/7; DRAG 8/8; FADE 6/6; MONOTONE 6/6; MUMBLE 8/8; PAUSE_DROPPED 8/8; PAUSE_INTRUSIVE 8/8; RUSH 8/8 |
| core8 | sensitivity (L1) | val+test | 8/8 | 95% Wilson (pooled; clusters ignored) [0.676, 1] | PAUSE_DROPPED 4/4; PAUSE_INTRUSIVE 2/2; RUSH 2/2 |
| lab_passed | headline (L2+L3) | train | 2/2 | 95% Wilson (pooled; clusters ignored) [0.342, 1] | NATURAL_RUSH 2/2 |
| lab_passed | headline (L2+L3) | val | 1/1 | 95% Wilson (pooled; clusters ignored) [0.207, 1] | NATURAL_RUSH 1/1 |
| lab_passed | headline (L2+L3) | test | 1/1 | 95% Wilson (pooled; clusters ignored) [0.207, 1] | NATURAL_RUSH 1/1 |
| lab_passed | headline (L2+L3) | val+test | 2/2 | 95% Wilson (pooled; clusters ignored) [0.342, 1] | NATURAL_RUSH 2/2 |
| synthetic_only | headline (L2+L3) | train | 5/20 | 95% Wilson (pooled; clusters ignored) [0.112, 0.469] | HESITATION 5/10; LOW_EFFORT 0/5; MISPLACED_EMPHASIS 0/1; TRAILING_OFF 0/4 |
| synthetic_only | headline (L2+L3) | val | 4/5 | 95% Wilson (pooled; clusters ignored) [0.376, 0.964] | HESITATION 4/4; MISPLACED_EMPHASIS 0/1 |
| synthetic_only | headline (L2+L3) | test | 3/8 | 95% Wilson (pooled; clusters ignored) [0.137, 0.694] | HESITATION 3/4; LOW_EFFORT 0/2; MISPLACED_EMPHASIS 0/1; TRAILING_OFF 0/1 |
| synthetic_only | headline (L2+L3) | val+test | 7/13 | 95% Wilson (pooled; clusters ignored) [0.291, 0.768] | HESITATION 7/8; LOW_EFFORT 0/2; MISPLACED_EMPHASIS 0/2; TRAILING_OFF 0/1 |

Confusion, val+test, all levels (injected type -> shown title type, with the pattern chip where it differs):

| injected type | shown labels (count) |
|---|---|
| DEEMPHASIS | DEEMPHASIS 4; MONOTONE 2; RUSH 1 |
| DRAG | DRAG 8 |
| FADE | FADE 6 |
| HESITATION | DRAG 1; PAUSE_INTRUSIVE (HESITATION chip) 7 |
| LOW_EFFORT | FADE 2 |
| MISPLACED_EMPHASIS | DEEMPHASIS 2 |
| MONOTONE | MONOTONE 6 |
| MUMBLE | MUMBLE 8 |
| NATURAL_RUSH | NATURAL_RUSH 2 |
| PAUSE_DROPPED | PAUSE_DROPPED 12 |
| PAUSE_INTRUSIVE | PAUSE_INTRUSIVE 10 |
| RUSH | RUSH 10 |
| TRAILING_OFF | FADE 1 |

RUSH against NATURAL_RUSH (all levels): the shown title type of the detecting region, and of every D9- region within half a window of the edit:

| split | injected | detecting region | D9- regions near the edit |
|---|---|---|---|
| train | RUSH | {"RUSH": 12, "not detected": 3} | {"RUSH": 14} |
| train | NATURAL_RUSH | {"NATURAL_RUSH": 2, "not detected": 13} | {"NATURAL_RUSH": 2} |
| val | RUSH | {"RUSH": 4, "not detected": 2} | {"RUSH": 4} |
| val | NATURAL_RUSH | {"NATURAL_RUSH": 1, "not detected": 5} | {"NATURAL_RUSH": 1} |
| test | RUSH | {"RUSH": 6} | {"RUSH": 6} |
| test | NATURAL_RUSH | {"NATURAL_RUSH": 1, "not detected": 5} | {"NATURAL_RUSH": 1} |
| val+test | RUSH | {"RUSH": 10, "not detected": 2} | {"RUSH": 10} |
| val+test | NATURAL_RUSH | {"NATURAL_RUSH": 2, "not detected": 10} | {"NATURAL_RUSH": 2} |

## 3. Regions on excluded edit spans (finding 5)

Single-level clips. A region that overlaps the words of an excluded (unrealised) edit is dropped from both TP and FP in every tier (events.on_shortfall), whatever its dimension. These regions are not counted as false. "Other dimension, unclaimed" regions would be false regions if only same-dimension responses were excluded.

| split | levels | clips | regions on excluded spans | by key | other dimension | other dimension, unclaimed | excluded edit types |
|---|---|---|---|---|---|---|---|
| train | headline (L2+L3) | 2 | 4 | {"D1-": 1, "D5-": 2, "D9-": 1} | 2 | 2 | {"LOW_EFFORT": 4} |
| train | sensitivity (L1) | 0 | 0 | {} | 0 | 0 | {} |
| val | headline (L2+L3) | 4 | 11 | {"D1-": 2, "D2+": 2, "D2-": 1, "D4-": 2, "D5-": 3, "D9-": 1} | 8 | 8 | {"LOW_EFFORT": 11} |
| val | sensitivity (L1) | 0 | 0 | {} | 0 | 0 | {} |
| test | headline (L2+L3) | 4 | 7 | {"D1-": 2, "D4-": 1, "D5-": 2, "D9-": 2} | 5 | 5 | {"LOW_EFFORT": 3, "TRAILING_OFF": 4} |
| test | sensitivity (L1) | 0 | 0 | {} | 0 | 0 | {} |
| val+test | headline (L2+L3) | 8 | 18 | {"D1-": 4, "D2+": 2, "D2-": 1, "D4-": 3, "D5-": 5, "D9-": 3} | 13 | 13 | {"LOW_EFFORT": 14, "TRAILING_OFF": 4} |
| val+test | sensitivity (L1) | 0 | 0 | {} | 0 | 0 | {} |

## 4. Reference-free baseline with its own scales and h (finding 6)

The existing reference_free rows reuse the detector's scales (fitted on identity nulls, all at their floors) and its h grid. The added row fits its own scales on the reference-free comparisons of the 30 train identity and placebo nulls (detect.fit_scales) and chooses its own common and speech-tempo h with the detector's objective (calibrate.select_r1: joint train strict F1 on core8 + NATURAL_RUSH L2+L3 with the 35 train controls). No text (syllable) normalisation is applied, so it is a reference-free lower bound.

Own scales: {"D1": "0.309", "D2-": "0.225", "D2+": "0.44", "D3": "0.336", "D5": "2.5", "D6": "0.223", "D9": "0.342"}; common h 2.7, speech-tempo h 5.3 (D9 noise floor 1.76 ln); train TP/FP/FN 31/112/59, F1 0.266.

| tier | split | method | TP | FP | same-change duplicates | FN | F1 |
|---|---|---|---|---|---|---|---|
| core8 | test | detector (pre-registered: all predictions counted) | 28 | 9 | n/a (counted in FP) | 4 | 0.812 |
| core8 | test | detector | 29 | 5 | 3 | 3 | 0.879 |
| core8 | test | reference_free (detector h) | 19 | 103 | 33 | 13 | 0.247 |
| core8 | test | reference_free (train-chosen h=2.75) | 18 | 88 | 30 | 14 | 0.261 |
| core8 | test | reference_free (own scales and h; added after the final evaluation) | 12 | 15 | 0 | 20 | 0.407 |
| core8 | val | detector (pre-registered: all predictions counted) | 30 | 13 | n/a (counted in FP) | 2 | 0.8 |
| core8 | val | detector | 30 | 9 | 4 | 2 | 0.845 |
| core8 | val | reference_free (detector h) | 20 | 132 | 31 | 12 | 0.217 |
| core8 | val | reference_free (train-chosen h=2.75) | 17 | 107 | 31 | 15 | 0.218 |
| core8 | val | reference_free (own scales and h; added after the final evaluation) | 9 | 20 | 0 | 23 | 0.295 |
| core8 | val+test | detector (pre-registered: all predictions counted) | 58 | 22 | n/a (counted in FP) | 6 | 0.806 |
| core8 | val+test | detector | 59 | 14 | 7 | 5 | 0.861 |
| core8 | val+test | reference_free (detector h) | 39 | 235 | 64 | 25 | 0.231 |
| core8 | val+test | reference_free (train-chosen h=2.75) | 35 | 195 | 61 | 29 | 0.238 |
| core8 | val+test | reference_free (own scales and h; added after the final evaluation) | 21 | 35 | 0 | 43 | 0.35 |
| lab_passed | test | detector (pre-registered: all predictions counted) | 1 | 7 | n/a (counted in FP) | 3 | 0.167 |
| lab_passed | test | detector | 1 | 7 | 0 | 3 | 0.167 |
| lab_passed | test | reference_free (detector h) | 2 | 40 | 14 | 2 | 0.087 |
| lab_passed | test | reference_free (train-chosen h=2.75) | 2 | 33 | 14 | 2 | 0.103 |
| lab_passed | test | reference_free (own scales and h; added after the final evaluation) | 0 | 8 | 0 | 4 | 0 |
| lab_passed | val | detector (pre-registered: all predictions counted) | 1 | 6 | n/a (counted in FP) | 3 | 0.182 |
| lab_passed | val | detector | 1 | 6 | 0 | 3 | 0.182 |
| lab_passed | val | reference_free (detector h) | 4 | 55 | 14 | 0 | 0.127 |
| lab_passed | val | reference_free (train-chosen h=2.75) | 2 | 41 | 14 | 2 | 0.085 |
| lab_passed | val | reference_free (own scales and h; added after the final evaluation) | 0 | 7 | 0 | 4 | 0 |
| lab_passed | val+test | detector (pre-registered: all predictions counted) | 2 | 13 | n/a (counted in FP) | 6 | 0.174 |
| lab_passed | val+test | detector | 2 | 13 | 0 | 6 | 0.174 |
| lab_passed | val+test | reference_free (detector h) | 6 | 95 | 28 | 2 | 0.11 |
| lab_passed | val+test | reference_free (train-chosen h=2.75) | 4 | 74 | 28 | 4 | 0.093 |
| lab_passed | val+test | reference_free (own scales and h; added after the final evaluation) | 0 | 15 | 0 | 8 | 0 |
| synthetic_only | test | detector (pre-registered: all predictions counted) | 8 | 28 | n/a (counted in FP) | 32 | 0.211 |
| synthetic_only | test | detector | 8 | 28 | 0 | 32 | 0.211 |
| synthetic_only | test | reference_free (detector h) | 9 | 225 | 67 | 31 | 0.066 |
| synthetic_only | test | reference_free (train-chosen h=2.75) | 7 | 188 | 64 | 33 | 0.06 |
| synthetic_only | test | reference_free (own scales and h; added after the final evaluation) | 2 | 39 | 0 | 38 | 0.049 |
| synthetic_only | val | detector (pre-registered: all predictions counted) | 5 | 19 | n/a (counted in FP) | 23 | 0.192 |
| synthetic_only | val | detector | 5 | 19 | 0 | 23 | 0.192 |
| synthetic_only | val | reference_free (detector h) | 9 | 250 | 70 | 19 | 0.063 |
| synthetic_only | val | reference_free (train-chosen h=2.75) | 6 | 203 | 71 | 22 | 0.051 |
| synthetic_only | val | reference_free (own scales and h; added after the final evaluation) | 2 | 40 | 0 | 26 | 0.057 |
| synthetic_only | val+test | detector (pre-registered: all predictions counted) | 13 | 47 | n/a (counted in FP) | 55 | 0.203 |
| synthetic_only | val+test | detector | 13 | 47 | 0 | 55 | 0.203 |
| synthetic_only | val+test | reference_free (detector h) | 18 | 475 | 137 | 50 | 0.064 |
| synthetic_only | val+test | reference_free (train-chosen h=2.75) | 13 | 391 | 135 | 55 | 0.055 |
| synthetic_only | val+test | reference_free (own scales and h; added after the final evaluation) | 4 | 79 | 0 | 64 | 0.053 |

The detector row of each split is given first under the pre-registered accounting; every other row counts one detection per change, an accounting adopted after the plan.

## 5. Intervals relabelled (finding 7)

Val and test have 2 speakers each. A percentile bootstrap over the 58 edited recordings of 2 speakers, or a Wilson interval on pooled events, is not a 95% interval for a new speaker; the tables below give per-speaker values and their range instead. The train F1 bootstrap resamples 5 speakers (in-sample; 126 distinct resamples), so its coverage is not assured.

### Stress (R1, val and test): per speaker

| split | condition | added/min | added/min per speaker | saved interval (58 recordings, 2 speakers) | kept | kept per speaker | pooled Wilson (clusters ignored) |
|---|---|---|---|---|---|---|---|
| val | gain +6 dB | 0.208 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.069; range [0.069, 0.346] | recording percentile [0, 0.587] | 73/73 (1) | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | Wilson [0.95, 1] |
| val | gain -6 dB | 0.277 | per speaker: eisenhower_farewell_1961 0.415, lbush_radio_2001 0.139; range [0.139, 0.415] | recording percentile [0.07, 0.531] | 73/73 (1) | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | Wilson [0.95, 1] |
| val | low-pass 3.4 kHz | 0.381 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 0.278; range [0.278, 0.484] | recording percentile [0.141, 0.651] | 70/73 (0.959) | per speaker: eisenhower_farewell_1961 0.973, lbush_radio_2001 0.944; range [0.944, 0.973] | Wilson [0.886, 0.986] |
| val | white noise 20 dB SNR | 2.63 | per speaker: eisenhower_farewell_1961 1.96, lbush_radio_2001 3.31; range [1.96, 3.31] | recording percentile [2, 3.34] | 199/219 (0.909) | per speaker: eisenhower_farewell_1961 0.928, lbush_radio_2001 0.889; range [0.889, 0.928] | Wilson [0.863, 0.94] |
| val | MP3 64 kbit/s | 0.0693 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0; range [0, 0.138] | recording percentile [0, 0.209] | 73/73 (1) | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | Wilson [0.95, 1] |
| val | dynamic-range compression | 6.48 | per speaker: eisenhower_farewell_1961 8.03, lbush_radio_2001 4.93; range [4.93, 8.03] | recording percentile [5.62, 7.46] | 57/73 (0.781) | per speaker: eisenhower_farewell_1961 0.757, lbush_radio_2001 0.806; range [0.757, 0.806] | Wilson [0.673, 0.86] |
| val | room reverb RT60 0.4 s | 0.889 | per speaker: eisenhower_farewell_1961 0.969, lbush_radio_2001 0.81; range [0.81, 0.969] | recording percentile [0.472, 1.39] | 208/219 (0.95) | per speaker: eisenhower_farewell_1961 0.964, lbush_radio_2001 0.935; range [0.935, 0.964] | Wilson [0.912, 0.972] |
| val | phone band + mu-law (participant only) | 1.84 | per speaker: eisenhower_farewell_1961 2.91, lbush_radio_2001 0.764; range [0.764, 2.91] | recording percentile [1.23, 2.52] | 65/73 (0.89) | per speaker: eisenhower_farewell_1961 0.946, lbush_radio_2001 0.833; range [0.833, 0.946] | Wilson [0.798, 0.943] |
| val | WORLD speaker transform | 0.936 | per speaker: eisenhower_farewell_1961 1.45, lbush_radio_2001 0.417; range [0.417, 1.45] | recording percentile [0.547, 1.41] | 70/73 (0.959) | per speaker: eisenhower_farewell_1961 0.973, lbush_radio_2001 0.944; range [0.944, 0.973] | Wilson [0.886, 0.986] |
| val | babble 10 dB SNR | 24.5 | per speaker: eisenhower_farewell_1961 27.2, lbush_radio_2001 21.8; range [21.8, 27.2] | recording percentile [23.2, 25.8] | 143/219 (0.653) | per speaker: eisenhower_farewell_1961 0.694, lbush_radio_2001 0.611; range [0.611, 0.694] | Wilson [0.588, 0.713] |
| val | babble 20 dB SNR | 8.41 | per speaker: eisenhower_farewell_1961 10.6, lbush_radio_2001 6.18; range [6.18, 10.6] | recording percentile [7.44, 9.42] | 194/219 (0.886) | per speaker: eisenhower_farewell_1961 0.91, lbush_radio_2001 0.861; range [0.861, 0.91] | Wilson [0.837, 0.921] |
| test | gain +6 dB | 0.139 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.138, 0.139] | recording percentile [0, 0.318] | 78/78 (1) | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | Wilson [0.953, 1] |
| test | gain -6 dB | 0.278 | per speaker: mobama_weekly_2014 0.418, nixon_resignation_1974 0.138; range [0.138, 0.418] | recording percentile [0, 0.683] | 78/78 (1) | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | Wilson [0.953, 1] |
| test | low-pass 3.4 kHz | 1.46 | per speaker: mobama_weekly_2014 2.44, nixon_resignation_1974 0.484; range [0.484, 2.44] | recording percentile [1.05, 1.93] | 73/78 (0.936) | per speaker: mobama_weekly_2014 0.895, nixon_resignation_1974 0.975; range [0.895, 0.975] | Wilson [0.859, 0.972] |
| test | white noise 20 dB SNR | 1.85 | per speaker: mobama_weekly_2014 1.39, nixon_resignation_1974 2.31; range [1.39, 2.31] | recording percentile [1.11, 2.75] | 213/234 (0.91) | per speaker: mobama_weekly_2014 0.895, nixon_resignation_1974 0.925; range [0.895, 0.925] | Wilson [0.867, 0.941] |
| test | MP3 64 kbit/s | 0.139 | per speaker: mobama_weekly_2014 0.279, nixon_resignation_1974 0; range [0, 0.279] | recording percentile [0, 0.426] | 78/78 (1) | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | Wilson [0.953, 1] |
| test | dynamic-range compression | 2.6 | per speaker: mobama_weekly_2014 2.16, nixon_resignation_1974 3.04; range [2.16, 3.04] | recording percentile [2.24, 2.98] | 59/78 (0.756) | per speaker: mobama_weekly_2014 0.737, nixon_resignation_1974 0.775; range [0.737, 0.775] | Wilson [0.651, 0.838] |
| test | room reverb RT60 0.4 s | 0.613 | per speaker: mobama_weekly_2014 0.743, nixon_resignation_1974 0.484; range [0.484, 0.743] | recording percentile [0.298, 1.1] | 231/234 (0.987) | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0.975; range [0.975, 1] | Wilson [0.963, 0.996] |
| test | phone band + mu-law (participant only) | 5.52 | per speaker: mobama_weekly_2014 2.3, nixon_resignation_1974 8.71; range [2.3, 8.71] | recording percentile [4.37, 6.7] | 68/78 (0.872) | per speaker: mobama_weekly_2014 0.842, nixon_resignation_1974 0.9; range [0.842, 0.9] | Wilson [0.78, 0.929] |
| test | WORLD speaker transform | 0.763 | per speaker: mobama_weekly_2014 0.836, nixon_resignation_1974 0.691; range [0.691, 0.836] | recording percentile [0.34, 1.27] | 77/78 (0.987) | per speaker: mobama_weekly_2014 0.974, nixon_resignation_1974 1; range [0.974, 1] | Wilson [0.931, 0.998] |
| test | babble 10 dB SNR | 26.2 | per speaker: mobama_weekly_2014 20.4, nixon_resignation_1974 31.9; range [20.4, 31.9] | recording percentile [24.2, 28] | 141/234 (0.603) | per speaker: mobama_weekly_2014 0.693, nixon_resignation_1974 0.517; range [0.517, 0.693] | Wilson [0.539, 0.663] |
| test | babble 20 dB SNR | 13.2 | per speaker: mobama_weekly_2014 2.81, nixon_resignation_1974 23.6; range [2.81, 23.6] | recording percentile [10.3, 16.2] | 200/234 (0.855) | per speaker: mobama_weekly_2014 0.947, nixon_resignation_1974 0.767; range [0.767, 0.947] | Wilson [0.804, 0.894] |
| val+test | gain +6 dB | 0.173 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.069, mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.069, 0.346] | recording percentile [0.034, 0.399] | 151/151 (1) | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | Wilson [0.975, 1] |
| val+test | gain -6 dB | 0.277 | per speaker: eisenhower_farewell_1961 0.415, lbush_radio_2001 0.139, mobama_weekly_2014 0.418, nixon_resignation_1974 0.138; range [0.138, 0.418] | recording percentile [0.104, 0.495] | 151/151 (1) | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | Wilson [0.975, 1] |
| val+test | low-pass 3.4 kHz | 0.919 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 0.278, mobama_weekly_2014 2.44, nixon_resignation_1974 0.484; range [0.278, 2.44] | recording percentile [0.662, 1.2] | 143/151 (0.947) | per speaker: eisenhower_farewell_1961 0.973, lbush_radio_2001 0.944, mobama_weekly_2014 0.895, nixon_resignation_1974 0.975; range [0.895, 0.975] | Wilson [0.899, 0.973] |
| val+test | white noise 20 dB SNR | 2.24 | per speaker: eisenhower_farewell_1961 1.96, lbush_radio_2001 3.31, mobama_weekly_2014 1.39, nixon_resignation_1974 2.31; range [1.39, 3.31] | recording percentile [1.8, 2.79] | 412/453 (0.909) | per speaker: eisenhower_farewell_1961 0.928, lbush_radio_2001 0.889, mobama_weekly_2014 0.895, nixon_resignation_1974 0.925; range [0.889, 0.928] | Wilson [0.88, 0.933] |
| val+test | MP3 64 kbit/s | 0.104 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0, mobama_weekly_2014 0.279, nixon_resignation_1974 0; range [0, 0.279] | recording percentile [0, 0.276] | 151/151 (1) | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | Wilson [0.975, 1] |
| val+test | dynamic-range compression | 4.54 | per speaker: eisenhower_farewell_1961 8.03, lbush_radio_2001 4.93, mobama_weekly_2014 2.16, nixon_resignation_1974 3.04; range [2.16, 8.03] | recording percentile [3.98, 5.16] | 116/151 (0.768) | per speaker: eisenhower_farewell_1961 0.757, lbush_radio_2001 0.806, mobama_weekly_2014 0.737, nixon_resignation_1974 0.775; range [0.737, 0.806] | Wilson [0.695, 0.828] |
| val+test | room reverb RT60 0.4 s | 0.751 | per speaker: eisenhower_farewell_1961 0.969, lbush_radio_2001 0.81, mobama_weekly_2014 0.743, nixon_resignation_1974 0.484; range [0.484, 0.969] | recording percentile [0.475, 1.08] | 439/453 (0.969) | per speaker: eisenhower_farewell_1961 0.964, lbush_radio_2001 0.935, mobama_weekly_2014 1, nixon_resignation_1974 0.975; range [0.935, 1] | Wilson [0.949, 0.982] |
| val+test | phone band + mu-law (participant only) | 3.68 | per speaker: eisenhower_farewell_1961 2.91, lbush_radio_2001 0.764, mobama_weekly_2014 2.3, nixon_resignation_1974 8.71; range [0.764, 8.71] | recording percentile [2.91, 4.44] | 133/151 (0.881) | per speaker: eisenhower_farewell_1961 0.946, lbush_radio_2001 0.833, mobama_weekly_2014 0.842, nixon_resignation_1974 0.9; range [0.833, 0.946] | Wilson [0.819, 0.923] |
| val+test | WORLD speaker transform | 0.85 | per speaker: eisenhower_farewell_1961 1.45, lbush_radio_2001 0.417, mobama_weekly_2014 0.836, nixon_resignation_1974 0.691; range [0.417, 1.45] | recording percentile [0.57, 1.18] | 147/151 (0.974) | per speaker: eisenhower_farewell_1961 0.973, lbush_radio_2001 0.944, mobama_weekly_2014 0.974, nixon_resignation_1974 1; range [0.944, 1] | Wilson [0.934, 0.99] |
| val+test | babble 10 dB SNR | 25.3 | per speaker: eisenhower_farewell_1961 27.2, lbush_radio_2001 21.8, mobama_weekly_2014 20.4, nixon_resignation_1974 31.9; range [20.4, 31.9] | recording percentile [24.2, 26.5] | 284/453 (0.627) | per speaker: eisenhower_farewell_1961 0.694, lbush_radio_2001 0.611, mobama_weekly_2014 0.693, nixon_resignation_1974 0.517; range [0.517, 0.694] | Wilson [0.582, 0.67] |
| val+test | babble 20 dB SNR | 10.8 | per speaker: eisenhower_farewell_1961 10.6, lbush_radio_2001 6.18, mobama_weekly_2014 2.81, nixon_resignation_1974 23.6; range [2.81, 23.6] | recording percentile [9.34, 12.5] | 394/453 (0.87) | per speaker: eisenhower_farewell_1961 0.91, lbush_radio_2001 0.861, mobama_weekly_2014 0.947, nixon_resignation_1974 0.767; range [0.767, 0.947] | Wilson [0.836, 0.898] |

### Overlap view (core8): per speaker

| levels | split | flaws touched | flags on flaw / flags | pooled Wilson recall (clusters ignored) | per speaker touched/flaws; on flaw/flags |
|---|---|---|---|---|---|
| headline (L2+L3) | train | 77/80 | 80/84 | Wilson [0.895, 0.987] | gwbush_911_2001 15/16, 17/17; harris_uncsw_2021 16/16, 16/17; hclinton_tomorrow_2010 16/16, 16/16; obama_weekly_2009 15/16, 16/18; reagan_farewell_1989 15/16, 15/16 |
| headline (L2+L3) | val | 32/32 | 32/39 | Wilson [0.893, 1] | eisenhower_farewell_1961 16/16, 16/21; lbush_radio_2001 16/16, 16/18 |
| headline (L2+L3) | test | 31/32 | 32/34 | Wilson [0.843, 0.994] | mobama_weekly_2014 16/16, 16/17; nixon_resignation_1974 15/16, 16/17 |
| headline (L2+L3) | val+test | 63/64 | 64/73 | Wilson [0.917, 0.997] | eisenhower_farewell_1961 16/16, 16/21; lbush_radio_2001 16/16, 16/18; mobama_weekly_2014 16/16, 16/17; nixon_resignation_1974 15/16, 16/17 |
| sensitivity (L1) | train | 11/40 | 11/11 | Wilson [0.161, 0.428] | gwbush_911_2001 2/8, 2/2; harris_uncsw_2021 2/8, 2/2; hclinton_tomorrow_2010 3/8, 3/3; obama_weekly_2009 1/8, 1/1; reagan_farewell_1989 3/8, 3/3 |
| sensitivity (L1) | val | 3/16 | 3/3 | Wilson [0.0659, 0.43] | eisenhower_farewell_1961 1/8, 1/1; lbush_radio_2001 2/8, 2/2 |
| sensitivity (L1) | test | 5/16 | 5/5 | Wilson [0.142, 0.556] | mobama_weekly_2014 2/8, 2/2; nixon_resignation_1974 3/8, 3/3 |
| sensitivity (L1) | val+test | 8/32 | 8/8 | Wilson [0.133, 0.421] | eisenhower_farewell_1961 1/8, 1/1; lbush_radio_2001 2/8, 2/2; mobama_weekly_2014 2/8, 2/2; nixon_resignation_1974 3/8, 3/3 |

### R2 check readers (consensus5), away-edits by type: per reader and the pre-registered expectation

Each check reader is compared once with the median of 5 calibration readers; the per-reader k/n are not independent trials either. "Majority detected" (more than half of the away-edits) applies to level 3 of pace, pause, pitch-range and volume types only; it is an addendum criterion, not pre-registered.

| type | level | dimension | detected | per check reader | pre-registered R2 expectation | majority detected |
|---|---|---|---|---|---|---|
| BLOCK | 2 | D7 | 0/1 | gettysburg_tg 0/1 | marginal | n/a |
| BLOCK | 3 | D7 | 0/1 | gettysburg_tg 0/1 | D7 is listed in R2 | n/a |
| DRAG | 3 | D1 | 1/3 | gettysburg_dj 1/1; gettysburg_sa 0/1; gettysburg_tg 0/1 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | no |
| FADE | 3 | D5 | 3/3 | gettysburg_dj 1/1; gettysburg_sa 1/1; gettysburg_tg 1/1 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | yes |
| FLAT_FINAL_FALL | 3 | D8 | 0/1 | gettysburg_sa 0/1 | D8 is listed in R2 | n/a |
| HESITATION | 2 | D2 | 0/3 | gettysburg_dj 0/1; gettysburg_sa 0/1; gettysburg_tg 0/1 | marginal | n/a |
| HESITATION | 3 | D2 | 2/3 | gettysburg_dj 0/1; gettysburg_sa 1/1; gettysburg_tg 1/1 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | yes |
| LOW_EFFORT | 2 | D5 | 1/2 | gettysburg_dj 1/1; gettysburg_sa 0/1 | marginal | n/a |
| LOW_EFFORT | 3 | D5 | 2/3 | gettysburg_dj 1/1; gettysburg_sa 1/1; gettysburg_tg 0/1 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | yes |
| MONOTONE | 3 | D3 | 3/3 | gettysburg_dj 1/1; gettysburg_sa 1/1; gettysburg_tg 1/1 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | yes |
| NATURAL_RUSH | 2 | D9 | 0/1 | gettysburg_dj 0/1 | marginal | n/a |
| NATURAL_RUSH | 3 | D9 | 0/1 | gettysburg_dj 0/1 | D9 is listed in R2 | n/a |
| ONSET_PROLONGATION | 2 | D7 | 0/3 | gettysburg_dj 0/1; gettysburg_sa 0/1; gettysburg_tg 0/1 | marginal | n/a |
| ONSET_PROLONGATION | 3 | D7 | 0/3 | gettysburg_dj 0/1; gettysburg_sa 0/1; gettysburg_tg 0/1 | D7 is listed in R2 | n/a |
| PAUSE_DROPPED | 2 | D2 | 1/3 | gettysburg_dj 0/1; gettysburg_sa 0/1; gettysburg_tg 1/1 | marginal | n/a |
| PAUSE_DROPPED | 3 | D2 | 2/3 | gettysburg_dj 1/1; gettysburg_sa 1/1; gettysburg_tg 0/1 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | yes |
| PAUSE_INTRUSIVE | 3 | D2 | 2/3 | gettysburg_dj 1/1; gettysburg_sa 1/1; gettysburg_tg 0/1 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | yes |
| RHYME_PROLONGATION | 2 | D7 | 0/3 | gettysburg_dj 0/1; gettysburg_sa 0/1; gettysburg_tg 0/1 | marginal | n/a |
| RHYME_PROLONGATION | 3 | D7 | 0/3 | gettysburg_dj 0/1; gettysburg_sa 0/1; gettysburg_tg 0/1 | D7 is listed in R2 | n/a |
| RISING_ENDING | 3 | D8 | 0/2 | gettysburg_dj 0/1; gettysburg_sa 0/1 | D8 is listed in R2 | n/a |
| RUSH | 2 | D1 | 0/2 | gettysburg_sa 0/1; gettysburg_tg 0/1 | marginal | n/a |
| RUSH | 3 | D1 | 2/3 | gettysburg_dj 0/1; gettysburg_sa 1/1; gettysburg_tg 1/1 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | yes |
| SOUND_REPETITION | 2 | D7 | 0/2 | gettysburg_sa 0/1; gettysburg_tg 0/1 | marginal | n/a |
| SOUND_REPETITION | 3 | D7 | 0/1 | gettysburg_sa 0/1 | D7 is listed in R2 | n/a |
| TRAILING_OFF | 2 | D5 | 0/1 | gettysburg_tg 0/1 | marginal | n/a |
| TRAILING_OFF | 3 | D5 | 0/2 | gettysburg_dj 0/1; gettysburg_tg 0/1 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | no |
| UNEVEN_TEMPO | 2 | D7 | 0/2 | gettysburg_dj 0/1; gettysburg_sa 0/1 | marginal | n/a |
| UNEVEN_TEMPO | 3 | D7 | 0/2 | gettysburg_sa 0/1; gettysburg_tg 0/1 | D7 is listed in R2 | n/a |
| WORD_BY_WORD | 2 | D2 | 0/18 | gettysburg_dj 0/6; gettysburg_sa 0/6; gettysburg_tg 0/6 | marginal | n/a |
| WORD_BY_WORD | 3 | D2 | 0/18 | gettysburg_dj 0/6; gettysburg_sa 0/6; gettysburg_tg 0/6 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | no |
| WORD_REPETITION | 2 | D7 | 0/2 | gettysburg_dj 0/1; gettysburg_sa 0/1 | marginal | n/a |
| WORD_REPETITION | 3 | D7 | 0/2 | gettysburg_dj 0/1; gettysburg_sa 0/1 | D7 is listed in R2 | n/a |

### R2 check readers (single), away-edits by type: per reader and the pre-registered expectation

Each of the 3 check readers counts once per calibration reference; the per-reader k/n are not independent trials either. "Majority detected" (more than half of the away-edits) applies to level 3 of pace, pause, pitch-range and volume types only; it is an addendum criterion, not pre-registered.

| type | level | dimension | detected | per check reader | pre-registered R2 expectation | majority detected |
|---|---|---|---|---|---|---|
| BLOCK | 2 | D7 | 0/8 | gettysburg_dj 0/3; gettysburg_sa 0/2; gettysburg_tg 0/3 | marginal | n/a |
| BLOCK | 3 | D7 | 0/8 | gettysburg_dj 0/2; gettysburg_sa 0/3; gettysburg_tg 0/3 | D7 is listed in R2 | n/a |
| DRAG | 3 | D1 | 6/17 | gettysburg_dj 6/6; gettysburg_sa 0/6; gettysburg_tg 0/5 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | no |
| FADE | 3 | D5 | 13/18 | gettysburg_dj 6/6; gettysburg_sa 2/6; gettysburg_tg 5/6 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | yes |
| FLAT_FINAL_FALL | 3 | D8 | 0/4 | gettysburg_sa 0/3; gettysburg_tg 0/1 | D8 is listed in R2 | n/a |
| HESITATION | 2 | D2 | 0/18 | gettysburg_dj 0/6; gettysburg_sa 0/6; gettysburg_tg 0/6 | marginal | n/a |
| HESITATION | 3 | D2 | 13/18 | gettysburg_dj 4/6; gettysburg_sa 5/6; gettysburg_tg 4/6 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | yes |
| LOW_EFFORT | 2 | D5 | 4/17 | gettysburg_dj 3/6; gettysburg_sa 1/6; gettysburg_tg 0/5 | marginal | n/a |
| LOW_EFFORT | 3 | D5 | 11/18 | gettysburg_dj 6/6; gettysburg_sa 4/6; gettysburg_tg 1/6 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | yes |
| MISPLACED_EMPHASIS | 3 | D4 | 0/5 | gettysburg_dj 0/1; gettysburg_sa 0/2; gettysburg_tg 0/2 | D4 is not scored in R2 | n/a |
| MONOTONE | 3 | D3 | 17/18 | gettysburg_dj 5/6; gettysburg_sa 6/6; gettysburg_tg 6/6 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | yes |
| NATURAL_RUSH | 2 | D9 | 0/10 | gettysburg_dj 0/6; gettysburg_sa 0/2; gettysburg_tg 0/2 | marginal | n/a |
| NATURAL_RUSH | 3 | D9 | 0/10 | gettysburg_dj 0/6; gettysburg_sa 0/2; gettysburg_tg 0/2 | D9 is listed in R2 | n/a |
| ONSET_PROLONGATION | 2 | D7 | 0/18 | gettysburg_dj 0/6; gettysburg_sa 0/6; gettysburg_tg 0/6 | marginal | n/a |
| ONSET_PROLONGATION | 3 | D7 | 0/18 | gettysburg_dj 0/6; gettysburg_sa 0/6; gettysburg_tg 0/6 | D7 is listed in R2 | n/a |
| PAUSE_DROPPED | 2 | D2 | 2/14 | gettysburg_dj 1/4; gettysburg_sa 0/4; gettysburg_tg 1/6 | marginal | n/a |
| PAUSE_DROPPED | 3 | D2 | 4/17 | gettysburg_dj 2/5; gettysburg_sa 1/6; gettysburg_tg 1/6 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | no |
| PAUSE_INTRUSIVE | 3 | D2 | 14/18 | gettysburg_dj 5/6; gettysburg_sa 6/6; gettysburg_tg 3/6 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | yes |
| RHYME_PROLONGATION | 2 | D7 | 0/18 | gettysburg_dj 0/6; gettysburg_sa 0/6; gettysburg_tg 0/6 | marginal | n/a |
| RHYME_PROLONGATION | 3 | D7 | 0/18 | gettysburg_dj 0/6; gettysburg_sa 0/6; gettysburg_tg 0/6 | D7 is listed in R2 | n/a |
| RISING_ENDING | 3 | D8 | 0/10 | gettysburg_dj 0/5; gettysburg_sa 0/5 | D8 is listed in R2 | n/a |
| RUSH | 2 | D1 | 0/13 | gettysburg_dj 0/2; gettysburg_sa 0/6; gettysburg_tg 0/5 | marginal | n/a |
| RUSH | 3 | D1 | 1/18 | gettysburg_dj 1/6; gettysburg_sa 0/6; gettysburg_tg 0/6 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | no |
| SOUND_REPETITION | 2 | D7 | 0/11 | gettysburg_dj 0/2; gettysburg_sa 0/6; gettysburg_tg 0/3 | marginal | n/a |
| SOUND_REPETITION | 3 | D7 | 0/13 | gettysburg_dj 0/2; gettysburg_sa 0/6; gettysburg_tg 0/5 | D7 is listed in R2 | n/a |
| TRAILING_OFF | 2 | D5 | 0/7 | gettysburg_dj 0/3; gettysburg_tg 0/4 | marginal | n/a |
| TRAILING_OFF | 3 | D5 | 0/8 | gettysburg_dj 0/3; gettysburg_sa 0/1; gettysburg_tg 0/4 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | no |
| UNEVEN_TEMPO | 2 | D7 | 0/11 | gettysburg_dj 0/5; gettysburg_sa 0/5; gettysburg_tg 0/1 | marginal | n/a |
| UNEVEN_TEMPO | 3 | D7 | 0/15 | gettysburg_dj 0/5; gettysburg_sa 0/5; gettysburg_tg 0/5 | D7 is listed in R2 | n/a |
| WORD_BY_WORD | 2 | D2 | 0/104 | gettysburg_dj 0/37; gettysburg_sa 0/35; gettysburg_tg 0/32 | marginal | n/a |
| WORD_BY_WORD | 3 | D2 | 0/108 | gettysburg_dj 0/38; gettysburg_sa 0/36; gettysburg_tg 0/34 | flagged for pace, pauses, pitch, volume; D4 and D6 not scored | no |
| WORD_REPETITION | 2 | D7 | 0/9 | gettysburg_dj 0/3; gettysburg_sa 0/6 | marginal | n/a |
| WORD_REPETITION | 3 | D7 | 0/8 | gettysburg_dj 0/2; gettysburg_sa 0/6 | D7 is listed in R2 | n/a |

## 6. Main tables rebuilt from results.json (finding 15)

No raw floats: 3 significant digits, |v| < 1e-6 printed as 0, and equal interval bounds printed as degenerate.

### Trivial baselines (L2+L3, val and test): the detector under the pre-registered accounting first; the other rows count one detection per change (adopted after the plan)

| tier | split | method | TP | FP | same-change duplicates | FN | F1 |
|---|---|---|---|---|---|---|---|
| core8 | test | detector (pre-registered: all predictions counted) | 28 | 9 | n/a (counted in FP) | 4 | 0.812 |
| core8 | test | detector | 29 | 5 | 3 | 3 | 0.879 |
| core8 | test | flag_all | 32 | 3936 | 484 | 0 | 0.016 |
| core8 | test | no_flags | 0 | 0 | 0 | 32 | 0 |
| core8 | test | random | 1.8 | 30.2 | 0 | 30.2 | 0.056 |
| core8 | test | reference_free (detector h) | 19 | 103 | 33 | 13 | 0.247 |
| core8 | test | reference_free (train-chosen h=2.75) | 18 | 88 | 30 | 14 | 0.261 |
| core8 | test | reference_free (own scales and h; added after the final evaluation) | 12 | 15 | 0 | 20 | 0.407 |
| core8 | val | detector (pre-registered: all predictions counted) | 30 | 13 | n/a (counted in FP) | 2 | 0.8 |
| core8 | val | detector | 30 | 9 | 4 | 2 | 0.845 |
| core8 | val | flag_all | 32 | 4000 | 492 | 0 | 0.016 |
| core8 | val | no_flags | 0 | 0 | 0 | 32 | 0 |
| core8 | val | random | 1.45 | 30.5 | 0 | 30.5 | 0.045 |
| core8 | val | reference_free (detector h) | 20 | 132 | 31 | 12 | 0.217 |
| core8 | val | reference_free (train-chosen h=2.75) | 17 | 107 | 31 | 15 | 0.218 |
| core8 | val | reference_free (own scales and h; added after the final evaluation) | 9 | 20 | 0 | 23 | 0.295 |
| core8 | val+test | detector (pre-registered: all predictions counted) | 58 | 22 | n/a (counted in FP) | 6 | 0.806 |
| core8 | val+test | detector | 59 | 14 | 7 | 5 | 0.861 |
| core8 | val+test | flag_all | 64 | 7936 | 976 | 0 | 0.016 |
| core8 | val+test | no_flags | 0 | 0 | 0 | 64 | 0 |
| core8 | val+test | random | 3.25 | 60.7 | 0 | 60.7 | 0.051 |
| core8 | val+test | reference_free (detector h) | 39 | 235 | 64 | 25 | 0.231 |
| core8 | val+test | reference_free (train-chosen h=2.75) | 35 | 195 | 61 | 29 | 0.238 |
| core8 | val+test | reference_free (own scales and h; added after the final evaluation) | 21 | 35 | 0 | 43 | 0.35 |
| lab_passed | test | detector (pre-registered: all predictions counted) | 1 | 7 | n/a (counted in FP) | 3 | 0.167 |
| lab_passed | test | detector | 1 | 7 | 0 | 3 | 0.167 |
| lab_passed | test | flag_all | 4 | 1510 | 228 | 0 | 0.005 |
| lab_passed | test | no_flags | 0 | 0 | 0 | 4 | 0 |
| lab_passed | test | random | 0.35 | 2.5 | 0 | 3.65 | 0.102 |
| lab_passed | test | reference_free (detector h) | 2 | 40 | 14 | 2 | 0.087 |
| lab_passed | test | reference_free (train-chosen h=2.75) | 2 | 33 | 14 | 2 | 0.103 |
| lab_passed | test | reference_free (own scales and h; added after the final evaluation) | 0 | 8 | 0 | 4 | 0 |
| lab_passed | val | detector (pre-registered: all predictions counted) | 1 | 6 | n/a (counted in FP) | 3 | 0.182 |
| lab_passed | val | detector | 1 | 6 | 0 | 3 | 0.182 |
| lab_passed | val | flag_all | 4 | 1497 | 225 | 0 | 0.005 |
| lab_passed | val | no_flags | 0 | 0 | 0 | 4 | 0 |
| lab_passed | val | random | 0.25 | 2.4 | 0 | 3.75 | 0.075 |
| lab_passed | val | reference_free (detector h) | 4 | 55 | 14 | 0 | 0.127 |
| lab_passed | val | reference_free (train-chosen h=2.75) | 2 | 41 | 14 | 2 | 0.085 |
| lab_passed | val | reference_free (own scales and h; added after the final evaluation) | 0 | 7 | 0 | 4 | 0 |
| lab_passed | val+test | detector (pre-registered: all predictions counted) | 2 | 13 | n/a (counted in FP) | 6 | 0.174 |
| lab_passed | val+test | detector | 2 | 13 | 0 | 6 | 0.174 |
| lab_passed | val+test | flag_all | 8 | 3007 | 453 | 0 | 0.005 |
| lab_passed | val+test | no_flags | 0 | 0 | 0 | 8 | 0 |
| lab_passed | val+test | random | 0.6 | 4.9 | 0 | 7.4 | 0.089 |
| lab_passed | val+test | reference_free (detector h) | 6 | 95 | 28 | 2 | 0.11 |
| lab_passed | val+test | reference_free (train-chosen h=2.75) | 4 | 74 | 28 | 4 | 0.093 |
| lab_passed | val+test | reference_free (own scales and h; added after the final evaluation) | 0 | 15 | 0 | 8 | 0 |
| synthetic_only | test | detector (pre-registered: all predictions counted) | 8 | 28 | n/a (counted in FP) | 32 | 0.211 |
| synthetic_only | test | detector | 8 | 28 | 0 | 32 | 0.211 |
| synthetic_only | test | flag_all | 40 | 7376 | 892 | 0 | 0.011 |
| synthetic_only | test | no_flags | 0 | 0 | 0 | 40 | 0 |
| synthetic_only | test | random | 3.5 | 60.3 | 0 | 36.5 | 0.067 |
| synthetic_only | test | reference_free (detector h) | 9 | 225 | 67 | 31 | 0.066 |
| synthetic_only | test | reference_free (train-chosen h=2.75) | 7 | 188 | 64 | 33 | 0.06 |
| synthetic_only | test | reference_free (own scales and h; added after the final evaluation) | 2 | 39 | 0 | 38 | 0.049 |
| synthetic_only | val | detector (pre-registered: all predictions counted) | 5 | 19 | n/a (counted in FP) | 23 | 0.192 |
| synthetic_only | val | detector | 5 | 19 | 0 | 23 | 0.192 |
| synthetic_only | val | flag_all | 26 | 7322 | 877 | 2 | 0.007 |
| synthetic_only | val | no_flags | 0 | 0 | 0 | 28 | 0 |
| synthetic_only | val | random | 1.1 | 44.5 | 0 | 26.9 | 0.03 |
| synthetic_only | val | reference_free (detector h) | 9 | 250 | 70 | 19 | 0.063 |
| synthetic_only | val | reference_free (train-chosen h=2.75) | 6 | 203 | 71 | 22 | 0.051 |
| synthetic_only | val | reference_free (own scales and h; added after the final evaluation) | 2 | 40 | 0 | 26 | 0.057 |
| synthetic_only | val+test | detector (pre-registered: all predictions counted) | 13 | 47 | n/a (counted in FP) | 55 | 0.203 |
| synthetic_only | val+test | detector | 13 | 47 | 0 | 55 | 0.203 |
| synthetic_only | val+test | flag_all | 66 | 14698 | 1769 | 2 | 0.009 |
| synthetic_only | val+test | no_flags | 0 | 0 | 0 | 68 | 0 |
| synthetic_only | val+test | random | 4.6 | 105 | 0 | 63.4 | 0.052 |
| synthetic_only | val+test | reference_free (detector h) | 18 | 475 | 137 | 50 | 0.064 |
| synthetic_only | val+test | reference_free (train-chosen h=2.75) | 13 | 391 | 135 | 55 | 0.055 |
| synthetic_only | val+test | reference_free (own scales and h; added after the final evaluation) | 4 | 79 | 0 | 64 | 0.053 |

### Stress matrix (all rows)

| split | condition | regime | reference mode | recordings | added/min | interval | kept | kept fraction | interval | max score change |
|---|---|---|---|---|---|---|---|---|---|---|
| train | gain +6 dB | R1 |  | 145 | 0.199 | recording percentile (6 speakers) [0.093, 0.321] | 195/198 | 0.985 | recording percentile (6 speakers) [0.965, 1] | 5.92 |
| train | gain +6 dB | R2 | single | 22 | 0 | Poisson upper [0, 0.31] | 8/8 | 1 | degenerate [1, 1] (no spread across the resampled clusters); Wilson [0.676, 1] | 0.146 |
| train | gain -6 dB | R1 |  | 145 | 0.0918 | recording percentile (6 speakers) [0.03, 0.182] | 196/198 | 0.99 | recording percentile (6 speakers) [0.974, 1] | 7.46 |
| train | gain -6 dB | R2 | single | 22 | 0 | Poisson upper [0, 0.31] | 8/8 | 1 | degenerate [1, 1] (no spread across the resampled clusters); Wilson [0.676, 1] | 9.8 |
| train | low-pass 3.4 kHz | R1 |  | 145 | 1.61 | recording percentile (6 speakers) [1.31, 1.95] | 192/198 | 0.97 | recording percentile (6 speakers) [0.942, 0.99] | 7.65 |
| train | low-pass 3.4 kHz | R2 | single | 22 | 0 | Poisson upper [0, 0.31] | 7/8 | 0.875 | recording percentile (6 speakers) [0.5, 1] | 9.81 |
| train | white noise 20 dB SNR | R1 |  | 145 | 2.39 | recording percentile (6 speakers) [1.83, 3.07] | 525/594 | 0.884 | recording percentile (6 speakers) [0.839, 0.922] | 10.2 |
| train | white noise 20 dB SNR | R2 | single | 22 | 0 | Poisson upper [0, 0.31] | 18/24 | 0.75 | recording percentile (6 speakers) [0.429, 1] | 9.91 |
| train | MP3 64 kbit/s | R1 |  | 145 | 0.0765 | recording percentile (6 speakers) [0.015, 0.151] | 195/198 | 0.985 | recording percentile (6 speakers) [0.966, 1] | 2.11 |
| train | MP3 64 kbit/s | R2 | single | 22 | 0.0842 | recording percentile (6 speakers) [0, 0.26] | 8/8 | 1 | degenerate [1, 1] (no spread across the resampled clusters); Wilson [0.676, 1] | 0.761 |
| train | dynamic-range compression | R1 |  | 145 | 2.94 | recording percentile (6 speakers) [2.47, 3.49] | 157/198 | 0.793 | recording percentile (6 speakers) [0.724, 0.851] | 14.2 |
| train | dynamic-range compression | R2 | single | 22 | 0 | Poisson upper [0, 0.31] | 4/8 | 0.5 | recording percentile (6 speakers) [0.111, 0.875] | 1.27 |
| train | room reverb RT60 0.4 s | R1 |  | 145 | 0.964 | recording percentile (6 speakers) [0.711, 1.24] | 563/594 | 0.948 | recording percentile (6 speakers) [0.912, 0.976] | 12 |
| train | room reverb RT60 0.4 s | R2 | single | 22 | 0.365 | recording percentile (6 speakers) [0.056, 0.754] | 15/24 | 0.625 | recording percentile (6 speakers) [0.142, 1] | 9.34 |
| train | phone band + mu-law (participant only) | R1 |  | 145 | 1.99 | recording percentile (6 speakers) [1.63, 2.35] | 185/198 | 0.934 | recording percentile (6 speakers) [0.898, 0.966] | 10.5 |
| train | phone band + mu-law (participant only) | R2 | single | 22 | 0.0842 | recording percentile (6 speakers) [0, 0.26] | 6/8 | 0.75 | recording percentile (6 speakers) [0.375, 1] | 9.86 |
| train | WORLD speaker transform | R1 |  | 145 | 0.52 | recording percentile (6 speakers) [0.346, 0.695] | 193/198 | 0.975 | recording percentile (6 speakers) [0.951, 0.995] | 6.11 |
| train | WORLD speaker transform | R2 | single | 22 | 0 | Poisson upper [0, 0.31] | 6/8 | 0.75 | recording percentile (6 speakers) [0.429, 1] | 0.739 |
| train | babble 10 dB SNR | R1 |  | 145 | 30.4 | recording percentile (6 speakers) [28.2, 32.4] | 359/594 | 0.604 | recording percentile (6 speakers) [0.509, 0.691] | 33.8 |
| train | babble 10 dB SNR | R2 | single | 22 | 0.982 | recording percentile (6 speakers) [0.656, 1.47] | 1/24 | 0.0417 | recording percentile (6 speakers) [0, 0.111] | 25.7 |
| train | babble 20 dB SNR | R1 |  | 145 | 13.6 | recording percentile (6 speakers) [12, 15.2] | 522/594 | 0.879 | recording percentile (6 speakers) [0.826, 0.919] | 23.5 |
| train | babble 20 dB SNR | R2 | single | 22 | 0.112 | recording percentile (6 speakers) [0, 0.311] | 5/24 | 0.208 | recording percentile (6 speakers) [0, 0.481] | 2.6 |
| val | gain +6 dB | R1 |  | 58 | 0.208 | recording percentile (2 speakers) [0, 0.587] | 73/73 | 1 | degenerate [1, 1] (no spread across the resampled clusters); Wilson [0.95, 1] | 0.835 |
| val | gain -6 dB | R1 |  | 58 | 0.277 | recording percentile (2 speakers) [0.07, 0.531] | 73/73 | 1 | degenerate [1, 1] (no spread across the resampled clusters); Wilson [0.95, 1] | 2.86 |
| val | low-pass 3.4 kHz | R1 |  | 58 | 0.381 | recording percentile (2 speakers) [0.141, 0.651] | 70/73 | 0.959 | recording percentile (2 speakers) [0.912, 1] | 5.61 |
| val | white noise 20 dB SNR | R1 |  | 58 | 2.63 | recording percentile (2 speakers) [2, 3.34] | 199/219 | 0.909 | recording percentile (2 speakers) [0.841, 0.962] | 10.1 |
| val | MP3 64 kbit/s | R1 |  | 58 | 0.0693 | recording percentile (2 speakers) [0, 0.209] | 73/73 | 1 | degenerate [1, 1] (no spread across the resampled clusters); Wilson [0.95, 1] | 0.527 |
| val | dynamic-range compression | R1 |  | 58 | 6.48 | recording percentile (2 speakers) [5.62, 7.46] | 57/73 | 0.781 | recording percentile (2 speakers) [0.631, 0.885] | 18.5 |
| val | room reverb RT60 0.4 s | R1 |  | 58 | 0.889 | recording percentile (2 speakers) [0.472, 1.39] | 208/219 | 0.95 | recording percentile (2 speakers) [0.892, 0.989] | 14.7 |
| val | phone band + mu-law (participant only) | R1 |  | 58 | 1.84 | recording percentile (2 speakers) [1.23, 2.52] | 65/73 | 0.89 | recording percentile (2 speakers) [0.787, 0.964] | 6.17 |
| val | WORLD speaker transform | R1 |  | 58 | 0.936 | recording percentile (2 speakers) [0.547, 1.41] | 70/73 | 0.959 | recording percentile (2 speakers) [0.902, 1] | 14.8 |
| val | babble 10 dB SNR | R1 |  | 58 | 24.5 | recording percentile (2 speakers) [23.2, 25.8] | 143/219 | 0.653 | recording percentile (2 speakers) [0.509, 0.766] | 26.8 |
| val | babble 20 dB SNR | R1 |  | 58 | 8.41 | recording percentile (2 speakers) [7.44, 9.42] | 194/219 | 0.886 | recording percentile (2 speakers) [0.788, 0.95] | 19.7 |
| test | gain +6 dB | R1 |  | 58 | 0.139 | recording percentile (2 speakers) [0, 0.318] | 78/78 | 1 | degenerate [1, 1] (no spread across the resampled clusters); Wilson [0.953, 1] | 3.71 |
| test | gain -6 dB | R1 |  | 58 | 0.278 | recording percentile (2 speakers) [0, 0.683] | 78/78 | 1 | degenerate [1, 1] (no spread across the resampled clusters); Wilson [0.953, 1] | 15.5 |
| test | low-pass 3.4 kHz | R1 |  | 58 | 1.46 | recording percentile (2 speakers) [1.05, 1.93] | 73/78 | 0.936 | recording percentile (2 speakers) [0.875, 0.984] | 16.6 |
| test | white noise 20 dB SNR | R1 |  | 58 | 1.85 | recording percentile (2 speakers) [1.11, 2.75] | 213/234 | 0.91 | recording percentile (2 speakers) [0.839, 0.968] | 16.6 |
| test | MP3 64 kbit/s | R1 |  | 58 | 0.139 | recording percentile (2 speakers) [0, 0.426] | 78/78 | 1 | degenerate [1, 1] (no spread across the resampled clusters); Wilson [0.953, 1] | 11.8 |
| test | dynamic-range compression | R1 |  | 58 | 2.6 | recording percentile (2 speakers) [2.24, 2.98] | 59/78 | 0.756 | recording percentile (2 speakers) [0.603, 0.861] | 13.2 |
| test | room reverb RT60 0.4 s | R1 |  | 58 | 0.613 | recording percentile (2 speakers) [0.298, 1.1] | 231/234 | 0.987 | recording percentile (2 speakers) [0.971, 1] | 14.3 |
| test | phone band + mu-law (participant only) | R1 |  | 58 | 5.52 | recording percentile (2 speakers) [4.37, 6.7] | 68/78 | 0.872 | recording percentile (2 speakers) [0.783, 0.943] | 32.1 |
| test | WORLD speaker transform | R1 |  | 58 | 0.763 | recording percentile (2 speakers) [0.34, 1.27] | 77/78 | 0.987 | recording percentile (2 speakers) [0.954, 1] | 14.9 |
| test | babble 10 dB SNR | R1 |  | 58 | 26.2 | recording percentile (2 speakers) [24.2, 28] | 141/234 | 0.603 | recording percentile (2 speakers) [0.431, 0.75] | 28.9 |
| test | babble 20 dB SNR | R1 |  | 58 | 13.2 | recording percentile (2 speakers) [10.3, 16.2] | 200/234 | 0.855 | recording percentile (2 speakers) [0.772, 0.919] | 28.3 |
| val+test | gain +6 dB | R1 |  | 116 | 0.173 | recording percentile (4 speakers) [0.034, 0.399] | 151/151 | 1 | degenerate [1, 1] (no spread across the resampled clusters); Wilson [0.975, 1] | 3.71 |
| val+test | gain -6 dB | R1 |  | 116 | 0.277 | recording percentile (4 speakers) [0.104, 0.495] | 151/151 | 1 | degenerate [1, 1] (no spread across the resampled clusters); Wilson [0.975, 1] | 15.5 |
| val+test | low-pass 3.4 kHz | R1 |  | 116 | 0.919 | recording percentile (4 speakers) [0.662, 1.2] | 143/151 | 0.947 | recording percentile (4 speakers) [0.906, 0.976] | 16.6 |
| val+test | white noise 20 dB SNR | R1 |  | 116 | 2.24 | recording percentile (4 speakers) [1.8, 2.79] | 412/453 | 0.909 | recording percentile (4 speakers) [0.854, 0.95] | 16.6 |
| val+test | MP3 64 kbit/s | R1 |  | 116 | 0.104 | recording percentile (4 speakers) [0, 0.276] | 151/151 | 1 | degenerate [1, 1] (no spread across the resampled clusters); Wilson [0.975, 1] | 11.8 |
| val+test | dynamic-range compression | R1 |  | 116 | 4.54 | recording percentile (4 speakers) [3.98, 5.16] | 116/151 | 0.768 | recording percentile (4 speakers) [0.662, 0.851] | 18.5 |
| val+test | room reverb RT60 0.4 s | R1 |  | 116 | 0.751 | recording percentile (4 speakers) [0.475, 1.08] | 439/453 | 0.969 | recording percentile (4 speakers) [0.942, 0.99] | 14.7 |
| val+test | phone band + mu-law (participant only) | R1 |  | 116 | 3.68 | recording percentile (4 speakers) [2.91, 4.44] | 133/151 | 0.881 | recording percentile (4 speakers) [0.813, 0.933] | 32.1 |
| val+test | WORLD speaker transform | R1 |  | 116 | 0.85 | recording percentile (4 speakers) [0.57, 1.18] | 147/151 | 0.974 | recording percentile (4 speakers) [0.941, 0.994] | 14.9 |
| val+test | babble 10 dB SNR | R1 |  | 116 | 25.3 | recording percentile (4 speakers) [24.2, 26.5] | 284/453 | 0.627 | recording percentile (4 speakers) [0.509, 0.725] | 28.9 |
| val+test | babble 20 dB SNR | R1 |  | 116 | 10.8 | recording percentile (4 speakers) [9.34, 12.5] | 394/453 | 0.87 | recording percentile (4 speakers) [0.808, 0.919] | 28.3 |
| check readers | gain +6 dB | R2 | single | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 3.45 |
| check readers | gain +6 dB | R2 | consensus5 | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 3.1 |
| check readers | gain -6 dB | R2 | single | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 0.153 |
| check readers | gain -6 dB | R2 | consensus5 | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 0.343 |
| check readers | low-pass 3.4 kHz | R2 | single | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 1.19 |
| check readers | low-pass 3.4 kHz | R2 | consensus5 | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 1.77 |
| check readers | white noise 20 dB SNR | R2 | single | 3 | 0.258 | per recording: gettysburg_dj 0, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.662] | 0/0 |  | n/a | 3.21 |
| check readers | white noise 20 dB SNR | R2 | consensus5 | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 1.32 |
| check readers | MP3 64 kbit/s | R2 | single | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 0.058 |
| check readers | MP3 64 kbit/s | R2 | consensus5 | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 1.02 |
| check readers | dynamic-range compression | R2 | single | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 4.76 |
| check readers | dynamic-range compression | R2 | consensus5 | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 2.41 |
| check readers | room reverb RT60 0.4 s | R2 | single | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 15.5 |
| check readers | room reverb RT60 0.4 s | R2 | consensus5 | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 8.28 |
| check readers | phone band + mu-law (participant only) | R2 | single | 3 | 0.387 | per recording: gettysburg_dj 0.437, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.662] | 0/0 |  | n/a | 18.3 |
| check readers | phone band + mu-law (participant only) | R2 | consensus5 | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 8.28 |
| check readers | WORLD speaker transform | R2 | single | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 5.28 |
| check readers | WORLD speaker transform | R2 | consensus5 | 3 | 0 | Poisson upper [0, 2.85] | 0/0 |  | n/a | 3.41 |
| check readers | babble 10 dB SNR | R2 | single | 3 | 2.06 | per recording: gettysburg_dj 3.79, gettysburg_sa 1.77, gettysburg_tg 0.817; range [0.817, 3.79] | 0/0 |  | n/a | 20.6 |
| check readers | babble 10 dB SNR | R2 | consensus5 | 3 | 5.41 | per recording: gettysburg_dj 8.73, gettysburg_sa 5.3, gettysburg_tg 2.45; range [2.45, 8.73] | 0/0 |  | n/a | 8.25 |
| check readers | babble 20 dB SNR | R2 | single | 3 | 0.129 | per recording: gettysburg_dj 0.146, gettysburg_sa 0, gettysburg_tg 0.272; range [0, 0.272] | 0/0 |  | n/a | 14.9 |
| check readers | babble 20 dB SNR | R2 | consensus5 | 3 | 1.8 | per recording: gettysburg_dj 0.873, gettysburg_sa 1.99, gettysburg_tg 2.45; range [0.873, 2.45] | 0/0 |  | n/a | 15.6 |

### R2 lockbox

| mode | weighted total/min | pooled total/min | weighted upper95 | budget status | whole-clip flags per clip |
|---|---|---|---|---|---|
| consensus5 | 0.516 | 0.53 | 0.684 | not met on covered sources only | 0.084 |
| single | 0.46 | 0.522 | 0.538 | met on covered sources only | 0.0569 |

## 7. Local re-run check

The frozen detector was re-run on the saved audio of 162 single-level clips on CPU (4 workers, word alignments read from the --cache directory when present, 12.5 s). Strict TP/FP/duplicates/FN and the pre-registered counts equal the saved results in 24 of 24 rows (tier x levels x split). The existing reference_free (detector h) rows are reproduced in 9 of 9 (tier x split) cells (TP/FP/FN/duplicates).

