# Evaluation tables

Re-rendered from the saved build/work/kaggle_runs/last_run/x/eval/results.json by `python -m cvoice.evaluate render` (src/cvoice/evaluate.py), after the evaluation that wrote it: no number is measured again. The headline F1 table is rebuilt from the saved rows with the pre-registered accounting first; raw floats are printed to 3 significant digits and equal interval bounds as degenerate.

Detector config 782d7df7589164fa7d06e10571369a28aaee6149834a346cfbe4d90e3832f092. Splits train, val, test; alignment on cuda. Regimes are never pooled and train is never pooled with validation or test; counts are k of n; exposure beside every rate.

## Sample sizes (evaluated single-level clips)

| split | speakers | clips | type | level | trials |
|---|---|---|---|---|---|
| test | 2 | 36 | BLOCK | 1 | 2 |
| test | 2 | 36 | BLOCK | 2 | 2 |
| test | 2 | 36 | BLOCK | 3 | 2 |
| test | 2 | 36 | DEEMPHASIS | 1 | 2 |
| test | 2 | 36 | DEEMPHASIS | 2 | 2 |
| test | 2 | 36 | DEEMPHASIS | 3 | 2 |
| test | 2 | 36 | DRAG | 1 | 2 |
| test | 2 | 36 | DRAG | 2 | 2 |
| test | 2 | 36 | DRAG | 3 | 2 |
| test | 2 | 36 | FADE | 1 | 2 |
| test | 2 | 36 | FADE | 2 | 2 |
| test | 2 | 36 | FADE | 3 | 2 |
| test | 2 | 36 | FLAT_FINAL_FALL | 1 | 2 |
| test | 2 | 36 | FLAT_FINAL_FALL | 2 | 2 |
| test | 2 | 36 | FLAT_FINAL_FALL | 3 | 2 |
| test | 2 | 36 | HESITATION | 1 | 2 |
| test | 2 | 36 | HESITATION | 2 | 2 |
| test | 2 | 36 | HESITATION | 3 | 2 |
| test | 2 | 36 | LOW_EFFORT | 1 | 2 |
| test | 2 | 36 | LOW_EFFORT | 2 | 2 |
| test | 2 | 36 | LOW_EFFORT | 3 | 2 |
| test | 2 | 36 | MISPLACED_EMPHASIS | 1 | 1 |
| test | 2 | 36 | MISPLACED_EMPHASIS | 2 | 2 |
| test | 2 | 36 | MISPLACED_EMPHASIS | 3 | 2 |
| test | 2 | 36 | MONOTONE | 1 | 2 |
| test | 2 | 36 | MONOTONE | 2 | 2 |
| test | 2 | 36 | MONOTONE | 3 | 2 |
| test | 2 | 36 | MUMBLE | 1 | 2 |
| test | 2 | 36 | MUMBLE | 2 | 2 |
| test | 2 | 36 | MUMBLE | 3 | 2 |
| test | 2 | 36 | NATURAL_RUSH | 1 | 2 |
| test | 2 | 36 | NATURAL_RUSH | 2 | 2 |
| test | 2 | 36 | NATURAL_RUSH | 3 | 2 |
| test | 2 | 36 | ONSET_PROLONGATION | 1 | 2 |
| test | 2 | 36 | ONSET_PROLONGATION | 2 | 2 |
| test | 2 | 36 | ONSET_PROLONGATION | 3 | 2 |
| test | 2 | 36 | PAUSE_DROPPED | 1 | 2 |
| test | 2 | 36 | PAUSE_DROPPED | 2 | 2 |
| test | 2 | 36 | PAUSE_DROPPED | 3 | 2 |
| test | 2 | 36 | PAUSE_INTRUSIVE | 1 | 2 |
| test | 2 | 36 | PAUSE_INTRUSIVE | 2 | 2 |
| test | 2 | 36 | PAUSE_INTRUSIVE | 3 | 2 |
| test | 2 | 36 | REPEATED_CONTOUR | 1 | 2 |
| test | 2 | 36 | REPEATED_CONTOUR | 2 | 2 |
| test | 2 | 36 | REPEATED_CONTOUR | 3 | 2 |
| test | 2 | 36 | RHYME_PROLONGATION | 1 | 2 |
| test | 2 | 36 | RHYME_PROLONGATION | 2 | 2 |
| test | 2 | 36 | RHYME_PROLONGATION | 3 | 2 |
| test | 2 | 36 | RISING_ENDING | 1 | 2 |
| test | 2 | 36 | RISING_ENDING | 2 | 2 |
| test | 2 | 36 | RISING_ENDING | 3 | 2 |
| test | 2 | 36 | RUSH | 1 | 2 |
| test | 2 | 36 | RUSH | 2 | 2 |
| test | 2 | 36 | RUSH | 3 | 2 |
| test | 2 | 36 | SOUND_REPETITION | 1 | 2 |
| test | 2 | 36 | SOUND_REPETITION | 2 | 2 |
| test | 2 | 36 | SOUND_REPETITION | 3 | 2 |
| test | 2 | 36 | TRAILING_OFF | 1 | 2 |
| test | 2 | 36 | TRAILING_OFF | 2 | 2 |
| test | 2 | 36 | TRAILING_OFF | 3 | 2 |
| test | 2 | 36 | UNEVEN_TEMPO | 1 | 2 |
| test | 2 | 36 | UNEVEN_TEMPO | 2 | 2 |
| test | 2 | 36 | UNEVEN_TEMPO | 3 | 2 |
| test | 2 | 36 | WORD_BY_WORD | 1 | 2 |
| test | 2 | 36 | WORD_BY_WORD | 2 | 2 |
| test | 2 | 36 | WORD_BY_WORD | 3 | 2 |
| test | 2 | 36 | WORD_REPETITION | 1 | 2 |
| test | 2 | 36 | WORD_REPETITION | 2 | 2 |
| test | 2 | 36 | WORD_REPETITION | 3 | 2 |
| train | 5 | 90 | BLOCK | 1 | 4 |
| train | 5 | 90 | BLOCK | 2 | 4 |
| train | 5 | 90 | BLOCK | 3 | 4 |
| train | 5 | 90 | DEEMPHASIS | 1 | 5 |
| train | 5 | 90 | DEEMPHASIS | 2 | 5 |
| train | 5 | 90 | DEEMPHASIS | 3 | 5 |
| train | 5 | 90 | DRAG | 1 | 5 |
| train | 5 | 90 | DRAG | 2 | 5 |
| train | 5 | 90 | DRAG | 3 | 5 |
| train | 5 | 90 | FADE | 1 | 5 |
| train | 5 | 90 | FADE | 2 | 5 |
| train | 5 | 90 | FADE | 3 | 5 |
| train | 5 | 90 | FLAT_FINAL_FALL | 1 | 5 |
| train | 5 | 90 | FLAT_FINAL_FALL | 2 | 5 |
| train | 5 | 90 | FLAT_FINAL_FALL | 3 | 5 |
| train | 5 | 90 | HESITATION | 1 | 5 |
| train | 5 | 90 | HESITATION | 2 | 5 |
| train | 5 | 90 | HESITATION | 3 | 5 |
| train | 5 | 90 | LOW_EFFORT | 1 | 5 |
| train | 5 | 90 | LOW_EFFORT | 2 | 5 |
| train | 5 | 90 | LOW_EFFORT | 3 | 5 |
| train | 5 | 90 | MISPLACED_EMPHASIS | 1 | 4 |
| train | 5 | 90 | MISPLACED_EMPHASIS | 2 | 4 |
| train | 5 | 90 | MISPLACED_EMPHASIS | 3 | 5 |
| train | 5 | 90 | MONOTONE | 1 | 5 |
| train | 5 | 90 | MONOTONE | 2 | 5 |
| train | 5 | 90 | MONOTONE | 3 | 5 |
| train | 5 | 90 | MUMBLE | 1 | 5 |
| train | 5 | 90 | MUMBLE | 2 | 5 |
| train | 5 | 90 | MUMBLE | 3 | 5 |
| train | 5 | 90 | NATURAL_RUSH | 1 | 5 |
| train | 5 | 90 | NATURAL_RUSH | 2 | 5 |
| train | 5 | 90 | NATURAL_RUSH | 3 | 5 |
| train | 5 | 90 | ONSET_PROLONGATION | 1 | 5 |
| train | 5 | 90 | ONSET_PROLONGATION | 2 | 5 |
| train | 5 | 90 | ONSET_PROLONGATION | 3 | 5 |
| train | 5 | 90 | PAUSE_DROPPED | 1 | 5 |
| train | 5 | 90 | PAUSE_DROPPED | 2 | 5 |
| train | 5 | 90 | PAUSE_DROPPED | 3 | 5 |
| train | 5 | 90 | PAUSE_INTRUSIVE | 1 | 5 |
| train | 5 | 90 | PAUSE_INTRUSIVE | 2 | 5 |
| train | 5 | 90 | PAUSE_INTRUSIVE | 3 | 5 |
| train | 5 | 90 | REPEATED_CONTOUR | 1 | 5 |
| train | 5 | 90 | REPEATED_CONTOUR | 2 | 5 |
| train | 5 | 90 | REPEATED_CONTOUR | 3 | 5 |
| train | 5 | 90 | RHYME_PROLONGATION | 1 | 5 |
| train | 5 | 90 | RHYME_PROLONGATION | 2 | 5 |
| train | 5 | 90 | RHYME_PROLONGATION | 3 | 5 |
| train | 5 | 90 | RISING_ENDING | 1 | 5 |
| train | 5 | 90 | RISING_ENDING | 2 | 5 |
| train | 5 | 90 | RISING_ENDING | 3 | 5 |
| train | 5 | 90 | RUSH | 1 | 5 |
| train | 5 | 90 | RUSH | 2 | 5 |
| train | 5 | 90 | RUSH | 3 | 5 |
| train | 5 | 90 | SOUND_REPETITION | 1 | 5 |
| train | 5 | 90 | SOUND_REPETITION | 2 | 5 |
| train | 5 | 90 | SOUND_REPETITION | 3 | 5 |
| train | 5 | 90 | TRAILING_OFF | 1 | 5 |
| train | 5 | 90 | TRAILING_OFF | 2 | 5 |
| train | 5 | 90 | TRAILING_OFF | 3 | 5 |
| train | 5 | 90 | UNEVEN_TEMPO | 1 | 5 |
| train | 5 | 90 | UNEVEN_TEMPO | 2 | 5 |
| train | 5 | 90 | UNEVEN_TEMPO | 3 | 5 |
| train | 5 | 90 | WORD_BY_WORD | 1 | 5 |
| train | 5 | 90 | WORD_BY_WORD | 2 | 5 |
| train | 5 | 90 | WORD_BY_WORD | 3 | 5 |
| train | 5 | 90 | WORD_REPETITION | 1 | 5 |
| train | 5 | 90 | WORD_REPETITION | 2 | 5 |
| train | 5 | 90 | WORD_REPETITION | 3 | 5 |
| val | 2 | 36 | BLOCK | 1 | 1 |
| val | 2 | 36 | BLOCK | 2 | 1 |
| val | 2 | 36 | BLOCK | 3 | 1 |
| val | 2 | 36 | DEEMPHASIS | 1 | 2 |
| val | 2 | 36 | DEEMPHASIS | 2 | 2 |
| val | 2 | 36 | DEEMPHASIS | 3 | 2 |
| val | 2 | 36 | DRAG | 1 | 2 |
| val | 2 | 36 | DRAG | 2 | 2 |
| val | 2 | 36 | DRAG | 3 | 2 |
| val | 2 | 36 | FADE | 1 | 2 |
| val | 2 | 36 | FADE | 2 | 2 |
| val | 2 | 36 | FADE | 3 | 2 |
| val | 2 | 36 | FLAT_FINAL_FALL | 1 | 2 |
| val | 2 | 36 | FLAT_FINAL_FALL | 2 | 2 |
| val | 2 | 36 | FLAT_FINAL_FALL | 3 | 2 |
| val | 2 | 36 | HESITATION | 1 | 2 |
| val | 2 | 36 | HESITATION | 2 | 2 |
| val | 2 | 36 | HESITATION | 3 | 2 |
| val | 2 | 36 | LOW_EFFORT | 1 | 2 |
| val | 2 | 36 | LOW_EFFORT | 2 | 2 |
| val | 2 | 36 | LOW_EFFORT | 3 | 2 |
| val | 2 | 36 | MISPLACED_EMPHASIS | 1 | 2 |
| val | 2 | 36 | MISPLACED_EMPHASIS | 2 | 2 |
| val | 2 | 36 | MISPLACED_EMPHASIS | 3 | 2 |
| val | 2 | 36 | MONOTONE | 1 | 2 |
| val | 2 | 36 | MONOTONE | 2 | 2 |
| val | 2 | 36 | MONOTONE | 3 | 2 |
| val | 2 | 36 | MUMBLE | 1 | 2 |
| val | 2 | 36 | MUMBLE | 2 | 2 |
| val | 2 | 36 | MUMBLE | 3 | 2 |
| val | 2 | 36 | NATURAL_RUSH | 1 | 2 |
| val | 2 | 36 | NATURAL_RUSH | 2 | 2 |
| val | 2 | 36 | NATURAL_RUSH | 3 | 2 |
| val | 2 | 36 | ONSET_PROLONGATION | 1 | 2 |
| val | 2 | 36 | ONSET_PROLONGATION | 2 | 2 |
| val | 2 | 36 | ONSET_PROLONGATION | 3 | 2 |
| val | 2 | 36 | PAUSE_DROPPED | 1 | 2 |
| val | 2 | 36 | PAUSE_DROPPED | 2 | 2 |
| val | 2 | 36 | PAUSE_DROPPED | 3 | 2 |
| val | 2 | 36 | PAUSE_INTRUSIVE | 1 | 2 |
| val | 2 | 36 | PAUSE_INTRUSIVE | 2 | 2 |
| val | 2 | 36 | PAUSE_INTRUSIVE | 3 | 2 |
| val | 2 | 36 | REPEATED_CONTOUR | 1 | 1 |
| val | 2 | 36 | REPEATED_CONTOUR | 2 | 1 |
| val | 2 | 36 | REPEATED_CONTOUR | 3 | 1 |
| val | 2 | 36 | RHYME_PROLONGATION | 1 | 2 |
| val | 2 | 36 | RHYME_PROLONGATION | 2 | 2 |
| val | 2 | 36 | RHYME_PROLONGATION | 3 | 2 |
| val | 2 | 36 | RISING_ENDING | 1 | 2 |
| val | 2 | 36 | RISING_ENDING | 2 | 2 |
| val | 2 | 36 | RISING_ENDING | 3 | 2 |
| val | 2 | 36 | RUSH | 1 | 2 |
| val | 2 | 36 | RUSH | 2 | 2 |
| val | 2 | 36 | RUSH | 3 | 2 |
| val | 2 | 36 | SOUND_REPETITION | 1 | 2 |
| val | 2 | 36 | SOUND_REPETITION | 2 | 2 |
| val | 2 | 36 | SOUND_REPETITION | 3 | 2 |
| val | 2 | 36 | TRAILING_OFF | 1 | 2 |
| val | 2 | 36 | TRAILING_OFF | 2 | 2 |
| val | 2 | 36 | TRAILING_OFF | 3 | 2 |
| val | 2 | 36 | UNEVEN_TEMPO | 1 | 2 |
| val | 2 | 36 | UNEVEN_TEMPO | 2 | 2 |
| val | 2 | 36 | UNEVEN_TEMPO | 3 | 2 |
| val | 2 | 36 | WORD_BY_WORD | 1 | 2 |
| val | 2 | 36 | WORD_BY_WORD | 2 | 2 |
| val | 2 | 36 | WORD_BY_WORD | 3 | 2 |
| val | 2 | 36 | WORD_REPETITION | 1 | 2 |
| val | 2 | 36 | WORD_REPETITION | 2 | 2 |
| val | 2 | 36 | WORD_REPETITION | 3 | 2 |
| val+test | 4 | 72 | BLOCK | 1 | 3 |
| val+test | 4 | 72 | BLOCK | 2 | 3 |
| val+test | 4 | 72 | BLOCK | 3 | 3 |
| val+test | 4 | 72 | DEEMPHASIS | 1 | 4 |
| val+test | 4 | 72 | DEEMPHASIS | 2 | 4 |
| val+test | 4 | 72 | DEEMPHASIS | 3 | 4 |
| val+test | 4 | 72 | DRAG | 1 | 4 |
| val+test | 4 | 72 | DRAG | 2 | 4 |
| val+test | 4 | 72 | DRAG | 3 | 4 |
| val+test | 4 | 72 | FADE | 1 | 4 |
| val+test | 4 | 72 | FADE | 2 | 4 |
| val+test | 4 | 72 | FADE | 3 | 4 |
| val+test | 4 | 72 | FLAT_FINAL_FALL | 1 | 4 |
| val+test | 4 | 72 | FLAT_FINAL_FALL | 2 | 4 |
| val+test | 4 | 72 | FLAT_FINAL_FALL | 3 | 4 |
| val+test | 4 | 72 | HESITATION | 1 | 4 |
| val+test | 4 | 72 | HESITATION | 2 | 4 |
| val+test | 4 | 72 | HESITATION | 3 | 4 |
| val+test | 4 | 72 | LOW_EFFORT | 1 | 4 |
| val+test | 4 | 72 | LOW_EFFORT | 2 | 4 |
| val+test | 4 | 72 | LOW_EFFORT | 3 | 4 |
| val+test | 4 | 72 | MISPLACED_EMPHASIS | 1 | 3 |
| val+test | 4 | 72 | MISPLACED_EMPHASIS | 2 | 4 |
| val+test | 4 | 72 | MISPLACED_EMPHASIS | 3 | 4 |
| val+test | 4 | 72 | MONOTONE | 1 | 4 |
| val+test | 4 | 72 | MONOTONE | 2 | 4 |
| val+test | 4 | 72 | MONOTONE | 3 | 4 |
| val+test | 4 | 72 | MUMBLE | 1 | 4 |
| val+test | 4 | 72 | MUMBLE | 2 | 4 |
| val+test | 4 | 72 | MUMBLE | 3 | 4 |
| val+test | 4 | 72 | NATURAL_RUSH | 1 | 4 |
| val+test | 4 | 72 | NATURAL_RUSH | 2 | 4 |
| val+test | 4 | 72 | NATURAL_RUSH | 3 | 4 |
| val+test | 4 | 72 | ONSET_PROLONGATION | 1 | 4 |
| val+test | 4 | 72 | ONSET_PROLONGATION | 2 | 4 |
| val+test | 4 | 72 | ONSET_PROLONGATION | 3 | 4 |
| val+test | 4 | 72 | PAUSE_DROPPED | 1 | 4 |
| val+test | 4 | 72 | PAUSE_DROPPED | 2 | 4 |
| val+test | 4 | 72 | PAUSE_DROPPED | 3 | 4 |
| val+test | 4 | 72 | PAUSE_INTRUSIVE | 1 | 4 |
| val+test | 4 | 72 | PAUSE_INTRUSIVE | 2 | 4 |
| val+test | 4 | 72 | PAUSE_INTRUSIVE | 3 | 4 |
| val+test | 4 | 72 | REPEATED_CONTOUR | 1 | 3 |
| val+test | 4 | 72 | REPEATED_CONTOUR | 2 | 3 |
| val+test | 4 | 72 | REPEATED_CONTOUR | 3 | 3 |
| val+test | 4 | 72 | RHYME_PROLONGATION | 1 | 4 |
| val+test | 4 | 72 | RHYME_PROLONGATION | 2 | 4 |
| val+test | 4 | 72 | RHYME_PROLONGATION | 3 | 4 |
| val+test | 4 | 72 | RISING_ENDING | 1 | 4 |
| val+test | 4 | 72 | RISING_ENDING | 2 | 4 |
| val+test | 4 | 72 | RISING_ENDING | 3 | 4 |
| val+test | 4 | 72 | RUSH | 1 | 4 |
| val+test | 4 | 72 | RUSH | 2 | 4 |
| val+test | 4 | 72 | RUSH | 3 | 4 |
| val+test | 4 | 72 | SOUND_REPETITION | 1 | 4 |
| val+test | 4 | 72 | SOUND_REPETITION | 2 | 4 |
| val+test | 4 | 72 | SOUND_REPETITION | 3 | 4 |
| val+test | 4 | 72 | TRAILING_OFF | 1 | 4 |
| val+test | 4 | 72 | TRAILING_OFF | 2 | 4 |
| val+test | 4 | 72 | TRAILING_OFF | 3 | 4 |
| val+test | 4 | 72 | UNEVEN_TEMPO | 1 | 4 |
| val+test | 4 | 72 | UNEVEN_TEMPO | 2 | 4 |
| val+test | 4 | 72 | UNEVEN_TEMPO | 3 | 4 |
| val+test | 4 | 72 | WORD_BY_WORD | 1 | 4 |
| val+test | 4 | 72 | WORD_BY_WORD | 2 | 4 |
| val+test | 4 | 72 | WORD_BY_WORD | 3 | 4 |
| val+test | 4 | 72 | WORD_REPETITION | 1 | 4 |
| val+test | 4 | 72 | WORD_REPETITION | 2 | 4 |
| val+test | 4 | 72 | WORD_REPETITION | 3 | 4 |

## Expectation table (fixed before evaluation)

| level | R1 same performance | R2 different speaker |
|---|---|---|
| 1 | marginal: detection near or below 50 %; clip score >= 90 | must stay silent |
| 2 | flagged | marginal |
| 3 | flagged | flagged for pace, pauses, pitch, volume; D4 and D6 not scored |

Development limits: train F1 is in-sample; val has two reused speakers. All baseline speeches are US political addresses; R2 positives use Gettysburg. Earlier test speakers were used before redesign. This final evaluation measures the test split and the R2 lockbox once for this detector config. F1 intervals resample source speakers only with at least 5 speakers (train); with fewer (val, test, val+test) the tables give each speaker's value and the range, which is not a confidence interval. k/n intervals use Wilson and do not remove shared-reference dependence. No blinded listening check has been completed.

Calibration policy: {"R1": "joint in-sample strict F1 maximum on core8 + NATURAL_RUSH (one detection per change; same-change duplicates reported separately); independent speech-tempo h; synthetic-only families evaluated separately", "R2": "single and median-of-five same-text references; equal-source comparison-minute point rate; separate clip budget", "new_types_in_R1": ["NATURAL_RUSH"]}

Frozen secondary exemptions: {"lists": {"BLOCK": ["D1", "D2", "D6"], "DEEMPHASIS": ["D1", "D3", "D5"], "DRAG": ["D2", "D4", "D6", "D7"], "FADE": ["D4"], "FLAT_FINAL_FALL": ["D3", "D4"], "HESITATION": ["D1", "D4", "D7"], "LOW_EFFORT": ["D3", "D4", "D6"], "MISPLACED_EMPHASIS": ["D1", "D3", "D5", "D7"], "MONOTONE": ["D4", "D8"], "MUMBLE": [], "NATURAL_RUSH": ["D2", "D4"], "ONSET_PROLONGATION": ["D1", "D6"], "PAUSE_DROPPED": ["D1"], "PAUSE_INTRUSIVE": ["D1"], "REPEATED_CONTOUR": ["D4"], "RHYME_PROLONGATION": ["D1", "D4"], "RISING_ENDING": ["D3", "D4"], "RUSH": ["D4"], "SOUND_REPETITION": ["D1", "D2", "D6"], "TRAILING_OFF": ["D4", "D6"], "UNEVEN_TEMPO": ["D4", "D6", "D7"], "WORD_BY_WORD": ["D1"], "WORD_REPETITION": ["D1", "D2"]}, "same_change": {"D9-": "D1-"}, "scope": "registry frozen before the run; strict headline: one detection per change; same-change duplicates reported separately. A region of a same_change key within half a window of a truth of its value key duplicates that change's detection: it is not a false region, and every strict count reports the number of such duplicates beside it", "sha256": "d385a9c6ef8b106cc993593d3bb59492077343283a6d2271fb0d3aaf47e50d02"}

Count-once rule as the code applies it (the frozen scope text above states only the duplicate case): One detection per change. A truth of a linked key (config.SAME_CHANGE: D9- measures the D1- change) is detected by its own-key region (IoU >= 0.5) or its own-key whole-clip flag; when there is none, the same-change region with the largest |z| within half a window (2 words) is the detection, without an IoU test. Every other same-change region of that change is a duplicate, not a false region. A second own-key region on the same edit that fails IoU is a false region.

## Real-data lab evidence

Lab-passed natural-rush text and filled-pause candidate labels do not establish product event accuracy. Synthetic-only families remain unvalidated; filled pause has no synthetic recipe.

{"D7+": {"lab_pass": false, "reason": "word_duration_ratio LibriStutter clip 0.39 found at 0.10 false; orphan_voiced_gap 0.34 at 0.07"}, "D8+": {"lab_pass": false, "reason": "no real ending labels"}, "labels": {"block": {"evidence": "within_word_silence LibriStutter events precision 0", "lab_pass": false}, "filled_pause": {"evidence": "stability_run on PodcastFillers events, +-0.20 s", "lab_pass": true, "precision": 0.54, "recall": 0.15}, "low_effort": {"evidence": "alpha_ratio AVID soft vs normal 0.07 found", "lab_pass": false}, "natural_rush": {"evidence": "speech_time_ratio EARS fast 0.54 found at 0.03 false, AUC 0.90", "lab_pass": true, "product_measure": "D9 is the ln ratio of aligned word durations per five-word window (owner decision O1); the lab evidence measured speech_time_ratio (aligned span minus pauses), not the D9 measure"}, "prolongation": {"evidence": "stability_run LibriStutter events precision 0.02", "lab_pass": false, "low_f0": true}, "repetition": {"evidence": "inserted_material LibriStutter events", "lab_pass": false, "precision": 0.04}, "trailing_off": {"evidence": "last_word_drop: no real labels; contrasts 0.05-0.25", "lab_pass": false}, "uneven_tempo": {"evidence": "tempo_irregularity EARS fast 0.17, slow 0.35", "lab_pass": false}}, "source": "Kaggle cvoice-lab v2 (2026-10-04), applied to DETECTOR_EXTENSION.md section 8; see build/work/design/LAB_DECISIONS.md"}

## Recovery of the synthetic edit: R1 event F1 (unmatched whole-clip flags count as false; windows IoU >= 0.5, D7/D8 both edges within 0.20 s, other events by labelled index or time)

| tier | validation | split | levels | accounting | TP | FP | same-change duplicates (not FP) | FN | F1 | F1 interval (speaker bootstrap with >= 5 speakers: train, in-sample, 5 speakers, coverage not assured; else per-speaker F1 and range, no interval) |
|---|---|---|---|---|---|---|---|---|---|---|
| core8 | synthetic recovery | train | headline (L2+L3) | pre-registered: every region not matched by its own key is false | 74 | 20 | 0 | 6 | 0.851 | n/a |
| core8 | synthetic recovery | train | headline (L2+L3) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 76 | 8 | 10 | 4 | 0.927 | 95% [0.885, 0.969] |
| core8 | synthetic recovery | val | headline (L2+L3) | pre-registered: every region not matched by its own key is false | 30 | 13 | 0 | 2 | 0.8 | n/a |
| core8 | synthetic recovery | val | headline (L2+L3) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 30 | 9 | 4 | 2 | 0.845 | per speaker: eisenhower_farewell_1961 0.811, lbush_radio_2001 0.882; range [0.811, 0.882] |
| core8 | synthetic recovery | test | headline (L2+L3) | pre-registered: every region not matched by its own key is false | 28 | 9 | 0 | 4 | 0.812 | n/a |
| core8 | synthetic recovery | test | headline (L2+L3) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 29 | 5 | 3 | 3 | 0.879 | per speaker: mobama_weekly_2014 0.848, nixon_resignation_1974 0.909; range [0.848, 0.909] |
| core8 | synthetic recovery | val+test | headline (L2+L3) | pre-registered: every region not matched by its own key is false | 58 | 22 | 0 | 6 | 0.806 | n/a |
| core8 | synthetic recovery | val+test | headline (L2+L3) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 59 | 14 | 7 | 5 | 0.861 | per speaker: eisenhower_farewell_1961 0.811, lbush_radio_2001 0.882, mobama_weekly_2014 0.848, nixon_resignation_1974 0.909; range [0.811, 0.909] |
| core8 | synthetic recovery | train | sensitivity (L1) | pre-registered: every region not matched by its own key is false | 9 | 2 | 0 | 31 | 0.353 | n/a |
| core8 | synthetic recovery | train | sensitivity (L1) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 11 | 0 | 0 | 29 | 0.431 | 95% [0.333, 0.519] |
| core8 | synthetic recovery | val | sensitivity (L1) | pre-registered: every region not matched by its own key is false | 3 | 0 | 0 | 13 | 0.316 | n/a |
| core8 | synthetic recovery | val | sensitivity (L1) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 3 | 0 | 0 | 13 | 0.316 | per speaker: eisenhower_farewell_1961 0.222, lbush_radio_2001 0.4; range [0.222, 0.4] |
| core8 | synthetic recovery | test | sensitivity (L1) | pre-registered: every region not matched by its own key is false | 3 | 2 | 0 | 13 | 0.286 | n/a |
| core8 | synthetic recovery | test | sensitivity (L1) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 5 | 0 | 0 | 11 | 0.476 | per speaker: mobama_weekly_2014 0.4, nixon_resignation_1974 0.545; range [0.4, 0.545] |
| core8 | synthetic recovery | val+test | sensitivity (L1) | pre-registered: every region not matched by its own key is false | 6 | 2 | 0 | 26 | 0.3 | n/a |
| core8 | synthetic recovery | val+test | sensitivity (L1) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 8 | 0 | 0 | 24 | 0.4 | per speaker: eisenhower_farewell_1961 0.222, lbush_radio_2001 0.4, mobama_weekly_2014 0.4, nixon_resignation_1974 0.545; range [0.222, 0.545] |
| core8 | synthetic recovery | train | headline (L2+L3) | secondary firings exempt | 76 | 5 | 10 | 4 | 0.944 | 95% [0.907, 0.981] |
| core8 | synthetic recovery | val | headline (L2+L3) | secondary firings exempt | 30 | 5 | 4 | 2 | 0.896 | per speaker: eisenhower_farewell_1961 0.857, lbush_radio_2001 0.938; range [0.857, 0.938] |
| core8 | synthetic recovery | test | headline (L2+L3) | secondary firings exempt | 29 | 5 | 3 | 3 | 0.879 | per speaker: mobama_weekly_2014 0.848, nixon_resignation_1974 0.909; range [0.848, 0.909] |
| core8 | synthetic recovery | val+test | headline (L2+L3) | secondary firings exempt | 59 | 10 | 7 | 5 | 0.887 | per speaker: eisenhower_farewell_1961 0.857, lbush_radio_2001 0.938, mobama_weekly_2014 0.848, nixon_resignation_1974 0.909; range [0.848, 0.938] |
| core8 | synthetic recovery | train | sensitivity (L1) | secondary firings exempt | 11 | 0 | 0 | 29 | 0.431 | 95% [0.333, 0.519] |
| core8 | synthetic recovery | val | sensitivity (L1) | secondary firings exempt | 3 | 0 | 0 | 13 | 0.316 | per speaker: eisenhower_farewell_1961 0.222, lbush_radio_2001 0.4; range [0.222, 0.4] |
| core8 | synthetic recovery | test | sensitivity (L1) | secondary firings exempt | 5 | 0 | 0 | 11 | 0.476 | per speaker: mobama_weekly_2014 0.4, nixon_resignation_1974 0.545; range [0.4, 0.545] |
| core8 | synthetic recovery | val+test | sensitivity (L1) | secondary firings exempt | 8 | 0 | 0 | 24 | 0.4 | per speaker: eisenhower_farewell_1961 0.222, lbush_radio_2001 0.4, mobama_weekly_2014 0.4, nixon_resignation_1974 0.545; range [0.222, 0.545] |
| lab_passed | synthetic recovery | train | headline (L2+L3) | pre-registered: every region not matched by its own key is false | 2 | 6 | 0 | 8 | 0.222 | n/a |
| lab_passed | synthetic recovery | train | headline (L2+L3) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 2 | 6 | 0 | 8 | 0.222 | 95% [0, 0.348] |
| lab_passed | synthetic recovery | val | headline (L2+L3) | pre-registered: every region not matched by its own key is false | 1 | 6 | 0 | 3 | 0.182 | n/a |
| lab_passed | synthetic recovery | val | headline (L2+L3) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 1 | 6 | 0 | 3 | 0.182 | per speaker: eisenhower_farewell_1961 0.25, lbush_radio_2001 0; range [0, 0.25] |
| lab_passed | synthetic recovery | test | headline (L2+L3) | pre-registered: every region not matched by its own key is false | 1 | 7 | 0 | 3 | 0.167 | n/a |
| lab_passed | synthetic recovery | test | headline (L2+L3) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 1 | 7 | 0 | 3 | 0.167 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.286; range [0, 0.286] |
| lab_passed | synthetic recovery | val+test | headline (L2+L3) | pre-registered: every region not matched by its own key is false | 2 | 13 | 0 | 6 | 0.174 | n/a |
| lab_passed | synthetic recovery | val+test | headline (L2+L3) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 2 | 13 | 0 | 6 | 0.174 | per speaker: eisenhower_farewell_1961 0.25, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.286; range [0, 0.286] |
| lab_passed | synthetic recovery | train | sensitivity (L1) | pre-registered: every region not matched by its own key is false | 0 | 2 | 0 | 5 | 0 | n/a |
| lab_passed | synthetic recovery | train | sensitivity (L1) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 0 | 2 | 0 | 5 | 0 | degenerate [0, 0] (no spread across the resampled clusters) |
| lab_passed | synthetic recovery | val | sensitivity (L1) | pre-registered: every region not matched by its own key is false | 0 | 0 | 0 | 2 | 0 | n/a |
| lab_passed | synthetic recovery | val | sensitivity (L1) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 0 | 0 | 0 | 2 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0; range [0, 0] |
| lab_passed | synthetic recovery | test | sensitivity (L1) | pre-registered: every region not matched by its own key is false | 0 | 2 | 0 | 2 | 0 | n/a |
| lab_passed | synthetic recovery | test | sensitivity (L1) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 0 | 2 | 0 | 2 | 0 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] |
| lab_passed | synthetic recovery | val+test | sensitivity (L1) | pre-registered: every region not matched by its own key is false | 0 | 2 | 0 | 4 | 0 | n/a |
| lab_passed | synthetic recovery | val+test | sensitivity (L1) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 0 | 2 | 0 | 4 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] |
| lab_passed | synthetic recovery | train | headline (L2+L3) | secondary firings exempt | 2 | 1 | 0 | 8 | 0.308 | 95% [0, 0.571] |
| lab_passed | synthetic recovery | val | headline (L2+L3) | secondary firings exempt | 1 | 2 | 0 | 3 | 0.286 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 0; range [0, 0.5] |
| lab_passed | synthetic recovery | test | headline (L2+L3) | secondary firings exempt | 1 | 1 | 0 | 3 | 0.333 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.667; range [0, 0.667] |
| lab_passed | synthetic recovery | val+test | headline (L2+L3) | secondary firings exempt | 2 | 3 | 0 | 6 | 0.308 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.667; range [0, 0.667] |
| lab_passed | synthetic recovery | train | sensitivity (L1) | secondary firings exempt | 0 | 1 | 0 | 5 | 0 | degenerate [0, 0] (no spread across the resampled clusters) |
| lab_passed | synthetic recovery | val | sensitivity (L1) | secondary firings exempt | 0 | 0 | 0 | 2 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0; range [0, 0] |
| lab_passed | synthetic recovery | test | sensitivity (L1) | secondary firings exempt | 0 | 0 | 0 | 2 | 0 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] |
| lab_passed | synthetic recovery | val+test | sensitivity (L1) | secondary firings exempt | 0 | 0 | 0 | 4 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] |
| synthetic_only | unvalidated | train | headline (L2+L3) | pre-registered: every region not matched by its own key is false | 20 | 55 | 0 | 75 | 0.235 | n/a |
| synthetic_only | unvalidated | train | headline (L2+L3) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 20 | 55 | 0 | 75 | 0.235 | 95% [0.195, 0.27] |
| synthetic_only | unvalidated | val | headline (L2+L3) | pre-registered: every region not matched by its own key is false | 5 | 19 | 0 | 23 | 0.192 | n/a |
| synthetic_only | unvalidated | val | headline (L2+L3) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 5 | 19 | 0 | 23 | 0.192 | per speaker: eisenhower_farewell_1961 0.16, lbush_radio_2001 0.222; range [0.16, 0.222] |
| synthetic_only | unvalidated | test | headline (L2+L3) | pre-registered: every region not matched by its own key is false | 8 | 28 | 0 | 32 | 0.211 | n/a |
| synthetic_only | unvalidated | test | headline (L2+L3) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 8 | 28 | 0 | 32 | 0.211 | per speaker: mobama_weekly_2014 0.176, nixon_resignation_1974 0.238; range [0.176, 0.238] |
| synthetic_only | unvalidated | val+test | headline (L2+L3) | pre-registered: every region not matched by its own key is false | 13 | 47 | 0 | 55 | 0.203 | n/a |
| synthetic_only | unvalidated | val+test | headline (L2+L3) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 13 | 47 | 0 | 55 | 0.203 | per speaker: eisenhower_farewell_1961 0.16, lbush_radio_2001 0.222, mobama_weekly_2014 0.176, nixon_resignation_1974 0.238; range [0.16, 0.238] |
| synthetic_only | unvalidated | train | sensitivity (L1) | pre-registered: every region not matched by its own key is false | 0 | 26 | 0 | 47 | 0 | n/a |
| synthetic_only | unvalidated | train | sensitivity (L1) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 0 | 26 | 0 | 47 | 0 | degenerate [0, 0] (no spread across the resampled clusters) |
| synthetic_only | unvalidated | val | sensitivity (L1) | pre-registered: every region not matched by its own key is false | 0 | 6 | 0 | 14 | 0 | n/a |
| synthetic_only | unvalidated | val | sensitivity (L1) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 0 | 6 | 0 | 14 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0; range [0, 0] |
| synthetic_only | unvalidated | test | sensitivity (L1) | pre-registered: every region not matched by its own key is false | 0 | 9 | 0 | 19 | 0 | n/a |
| synthetic_only | unvalidated | test | sensitivity (L1) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 0 | 9 | 0 | 19 | 0 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] |
| synthetic_only | unvalidated | val+test | sensitivity (L1) | pre-registered: every region not matched by its own key is false | 0 | 15 | 0 | 33 | 0 | n/a |
| synthetic_only | unvalidated | val+test | sensitivity (L1) | one detection per change; same-change duplicates reported separately (introduced after the plan) | 0 | 15 | 0 | 33 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] |
| synthetic_only | unvalidated | train | headline (L2+L3) | secondary firings exempt | 20 | 12 | 0 | 75 | 0.315 | 95% [0.26, 0.359] |
| synthetic_only | unvalidated | val | headline (L2+L3) | secondary firings exempt | 5 | 3 | 0 | 23 | 0.278 | per speaker: eisenhower_farewell_1961 0.25, lbush_radio_2001 0.3; range [0.25, 0.3] |
| synthetic_only | unvalidated | test | headline (L2+L3) | secondary firings exempt | 8 | 6 | 0 | 32 | 0.296 | per speaker: mobama_weekly_2014 0.25, nixon_resignation_1974 0.333; range [0.25, 0.333] |
| synthetic_only | unvalidated | val+test | headline (L2+L3) | secondary firings exempt | 13 | 9 | 0 | 55 | 0.289 | per speaker: eisenhower_farewell_1961 0.25, lbush_radio_2001 0.3, mobama_weekly_2014 0.25, nixon_resignation_1974 0.333; range [0.25, 0.333] |
| synthetic_only | unvalidated | train | sensitivity (L1) | secondary firings exempt | 0 | 8 | 0 | 47 | 0 | degenerate [0, 0] (no spread across the resampled clusters) |
| synthetic_only | unvalidated | val | sensitivity (L1) | secondary firings exempt | 0 | 2 | 0 | 14 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0; range [0, 0] |
| synthetic_only | unvalidated | test | sensitivity (L1) | secondary firings exempt | 0 | 2 | 0 | 19 | 0 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] |
| synthetic_only | unvalidated | val+test | sensitivity (L1) | secondary firings exempt | 0 | 4 | 0 | 33 | 0 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0] |

Recipe families recovered by dimension match (not by product pattern label): DEEMPHASIS, DRAG, FADE, HESITATION, LOW_EFFORT, MISPLACED_EMPHASIS, MONOTONE, MUMBLE, NATURAL_RUSH, PAUSE_DROPPED, PAUSE_INTRUSIVE, RUSH, TRAILING_OFF. Of these, the product pattern label is switched off for: LOW_EFFORT, TRAILING_OFF. Attempted families with no recovered eligible events: BLOCK, FLAT_FINAL_FALL, ONSET_PROLONGATION, REPEATED_CONTOUR, RHYME_PROLONGATION, RISING_ENDING, SOUND_REPETITION, UNEVEN_TEMPO, WORD_BY_WORD, WORD_REPETITION. Lab-passed status describes the lab contrast, not product recall.

Development val at the two most frequent joint bootstrap thresholds (all levels; one detection per change; same-change duplicates reported separately):

| h | speech-tempo h | bootstrap draws | val F1 | F1 interval (95% speaker bootstrap with >= 5 speakers; else per-speaker F1 and range, no interval) | same-change duplicates | recall by type |
|---|---|---|---|---|---|---|
| 2.15 | 3.05 | 566 | 0.66 | per speaker: eisenhower_farewell_1961 0.618, lbush_radio_2001 0.708; range [0.618, 0.708] | 4 | {'NATURAL_RUSH': '1/6 (95% Wilson [0.0301, 0.564])', 'RUSH': '4/6 (95% Wilson [0.3, 0.903])', 'PAUSE_DROPPED': '6/6 (95% Wilson [0.61, 1])', 'MONOTONE': '4/6 (95% Wilson [0.3, 0.903])', 'FADE': '2/6 (95% Wilson [0.0968, 0.7])', 'DRAG': '4/6 (95% Wilson [0.3, 0.903])', 'PAUSE_INTRUSIVE': '5/6 (95% Wilson [0.436, 0.97])', 'DEEMPHASIS': '4/6 (95% Wilson [0.3, 0.903])', 'MUMBLE': '4/6 (95% Wilson [0.3, 0.903])'} |
| 2.15 | 3.9 | 114 | 0.647 | per speaker: eisenhower_farewell_1961 0.593, lbush_radio_2001 0.708; range [0.593, 0.708] | 4 | {'NATURAL_RUSH': '0/6 (95% Wilson [0, 0.39])', 'RUSH': '4/6 (95% Wilson [0.3, 0.903])', 'PAUSE_DROPPED': '6/6 (95% Wilson [0.61, 1])', 'MONOTONE': '4/6 (95% Wilson [0.3, 0.903])', 'FADE': '2/6 (95% Wilson [0.0968, 0.7])', 'DRAG': '4/6 (95% Wilson [0.3, 0.903])', 'PAUSE_INTRUSIVE': '5/6 (95% Wilson [0.436, 0.97])', 'DEEMPHASIS': '4/6 (95% Wilson [0.3, 0.903])', 'MUMBLE': '4/6 (95% Wilson [0.3, 0.903])'} |

Detector, core8, TP/FP/FN under the accounting the evaluation plan fixed (pre-registered: every region not matched by its own key is false): train headline (L2+L3) 74/20/6, F1 0.851; val headline (L2+L3) 30/13/2, F1 0.8; train sensitivity (L1) 9/2/31, F1 0.353; val sensitivity (L1) 3/0/13, F1 0.316. The detector F1 in the next table counts one detection per change (one detection per change; same-change duplicates reported separately), an accounting adopted after the plan.

Change against dev_v9 (Oct 2), strict core8 L1 and L2+L3. v9 counted every region not matched by its own key as false; the current headline counts one detection per change (one detection per change; same-change duplicates reported separately). To compare like with like, the current FP are also given under the v9 accounting and on the keys v9 had (D1, D2, D3, D4, D5, D6); the current FP alone is a different accounting and is not a change in false regions:

| split | levels | v9 F1 | current F1 | current F1 interval | v9 FP | current FP (one per change) | current same-change duplicates | current FP, v9 accounting (all keys) | current FP, v9 accounting, v9 keys | FP change, v9 accounting, v9 keys | current TP, v9 accounting |
|---|---|---|---|---|---|---|---|---|---|---|---|
| train | headline (L2+L3) | 0.918 | 0.927 | 95% [0.885, 0.969] | 12 | 8 | 10 | 20 | 8 | -4 | 74 |
| val | headline (L2+L3) | 0.822 | 0.845 | per speaker: eisenhower_farewell_1961 0.811, lbush_radio_2001 0.882; range [0.811, 0.882] | 11 | 9 | 4 | 13 | 9 | -2 | 30 |
| train | sensitivity (L1) | 0.746 | 0.431 | 95% [0.333, 0.519] | 2 | 0 | 0 | 2 | 0 | -2 | 9 |
| val | sensitivity (L1) | 0.64 | 0.316 | per speaker: eisenhower_farewell_1961 0.222, lbush_radio_2001 0.4; range [0.222, 0.4] | 1 | 0 | 0 | 0 | 0 | -1 | 3 |

Current selected h by key: {'D1+': 2.15, 'D1-': 2.15, 'D2+': 2.15, 'D2-': 2.15, 'D3-': 2.15, 'D4-': 2.15, 'D5-': 2.15, 'D6-': 2.15, 'D7+': None, 'D8+': 2.15, 'D9-': 3.05}; historical v9 common h=1.70. The R1 h objective uses only L2+L3 training clips, so the L1 rows are measured at an h that was not chosen for L1. Verified v9-to-v10 FP decomposition: train +31 = D7 +21 and non-D7 +10; val +17 = D7 +11 and non-D7 +6. The threshold grid adds 11 training FP, but is a different metric.

## Overlap view (a flaw counts as found when a flag of its dimension lies on it)

core8:

| levels | split | flaws touched | flaws | flags on flaw | all local flags | overlap recall | flag precision | recall 95% Wilson | precision 95% Wilson |
|---|---|---|---|---|---|---|---|---|---|
| headline (L2+L3) | train | 77 | 80 | 80 | 84 | 0.963 | 0.952 | [0.895, 0.987] | [0.884, 0.981] |
| headline (L2+L3) | val | 32 | 32 | 32 | 39 | 1 | 0.821 | [0.893, 1] | [0.673, 0.91] |
| headline (L2+L3) | test | 31 | 32 | 32 | 34 | 0.969 | 0.941 | [0.843, 0.994] | [0.809, 0.984] |
| headline (L2+L3) | val+test | 63 | 64 | 64 | 73 | 0.984 | 0.877 | [0.917, 0.997] | [0.782, 0.934] |
| sensitivity (L1) | train | 11 | 40 | 11 | 11 | 0.275 | 1 | [0.161, 0.428] | [0.741, 1] |
| sensitivity (L1) | val | 3 | 16 | 3 | 3 | 0.188 | 1 | [0.0659, 0.43] | [0.439, 1] |
| sensitivity (L1) | test | 5 | 16 | 5 | 5 | 0.312 | 1 | [0.142, 0.556] | [0.566, 1] |
| sensitivity (L1) | val+test | 8 | 32 | 8 | 8 | 0.25 | 1 | [0.133, 0.421] | [0.676, 1] |

lab_passed:

| levels | split | flaws touched | flaws | flags on flaw | all local flags | overlap recall | flag precision | recall 95% Wilson | precision 95% Wilson |
|---|---|---|---|---|---|---|---|---|---|
| headline (L2+L3) | train | 2 | 10 | 2 | 21 | 0.2 | 0.0952 | [0.0567, 0.51] | [0.0265, 0.289] |
| headline (L2+L3) | val | 1 | 4 | 1 | 18 | 0.25 | 0.0556 | [0.0456, 0.699] | [0.00988, 0.258] |
| headline (L2+L3) | test | 1 | 4 | 1 | 16 | 0.25 | 0.0625 | [0.0456, 0.699] | [0.0111, 0.283] |
| headline (L2+L3) | val+test | 2 | 8 | 2 | 34 | 0.25 | 0.0588 | [0.0715, 0.591] | [0.0163, 0.191] |
| sensitivity (L1) | train | 0 | 5 | 0 | 5 | 0 | 0 | [0, 0.434] | [0, 0.434] |
| sensitivity (L1) | val | 0 | 2 | 0 | 0 | 0 |  | [0, 0.658] | [n/a, n/a] |
| sensitivity (L1) | test | 0 | 2 | 0 | 3 | 0 | 0 | [0, 0.658] | [0, 0.561] |
| sensitivity (L1) | val+test | 0 | 4 | 0 | 3 | 0 | 0 | [0, 0.49] | [0, 0.561] |

synthetic_only (unvalidated):

| levels | split | flaws touched | flaws | flags on flaw | all local flags | overlap recall | flag precision | recall 95% Wilson | precision 95% Wilson |
|---|---|---|---|---|---|---|---|---|---|
| headline (L2+L3) | train | 22 | 95 | 22 | 85 | 0.232 | 0.259 | [0.158, 0.326] | [0.178, 0.361] |
| headline (L2+L3) | val | 6 | 28 | 6 | 40 | 0.214 | 0.15 | [0.102, 0.395] | [0.0706, 0.291] |
| headline (L2+L3) | test | 8 | 40 | 8 | 50 | 0.2 | 0.16 | [0.105, 0.348] | [0.0834, 0.285] |
| headline (L2+L3) | val+test | 14 | 68 | 14 | 90 | 0.206 | 0.156 | [0.127, 0.316] | [0.095, 0.244] |
| sensitivity (L1) | train | 0 | 47 | 0 | 28 | 0 | 0 | [0, 0.0756] | [0, 0.121] |
| sensitivity (L1) | val | 0 | 14 | 0 | 6 | 0 | 0 | [0, 0.215] | [0, 0.39] |
| sensitivity (L1) | test | 0 | 19 | 0 | 11 | 0 | 0 | [0, 0.168] | [0, 0.259] |
| sensitivity (L1) | val+test | 0 | 33 | 0 | 17 | 0 | 0 | [0, 0.104] | [0, 0.184] |

## Per speech, k of n (L2 + L3)

core8:

| speech | split | clip | level | detected k | of n | false regions (one detection per change; same-change duplicates reported separately) | same-change duplicates | 95% Wilson |
|---|---|---|---|---|---|---|---|---|
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__single_L2A | 2 | 3 | 4 | 1 | 1 | [0.301, 0.954] |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__single_L2B | 2 | 4 | 4 | 0 | 0 | [0.51, 1] |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__single_L3A | 3 | 4 | 4 | 4 | 1 | [0.51, 1] |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__single_L3B | 3 | 4 | 4 | 1 | 0 | [0.51, 1] |
| gwbush_911_2001 | train | gwbush_911_2001__single_L2A | 2 | 4 | 4 | 0 | 1 | [0.51, 1] |
| gwbush_911_2001 | train | gwbush_911_2001__single_L2B | 2 | 4 | 4 | 0 | 0 | [0.51, 1] |
| gwbush_911_2001 | train | gwbush_911_2001__single_L3A | 3 | 4 | 4 | 2 | 2 | [0.51, 1] |
| gwbush_911_2001 | train | gwbush_911_2001__single_L3B | 3 | 3 | 4 | 0 | 0 | [0.301, 0.954] |
| harris_uncsw_2021 | train | harris_uncsw_2021__single_L2A | 2 | 4 | 4 | 0 | 1 | [0.51, 1] |
| harris_uncsw_2021 | train | harris_uncsw_2021__single_L2B | 2 | 4 | 4 | 1 | 0 | [0.51, 1] |
| harris_uncsw_2021 | train | harris_uncsw_2021__single_L3A | 3 | 4 | 4 | 0 | 1 | [0.51, 1] |
| harris_uncsw_2021 | train | harris_uncsw_2021__single_L3B | 3 | 4 | 4 | 0 | 0 | [0.51, 1] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__single_L2A | 2 | 4 | 4 | 0 | 1 | [0.51, 1] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__single_L2B | 2 | 4 | 4 | 0 | 0 | [0.51, 1] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__single_L3A | 3 | 4 | 4 | 0 | 1 | [0.51, 1] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__single_L3B | 3 | 4 | 4 | 0 | 0 | [0.51, 1] |
| lbush_radio_2001 | val | lbush_radio_2001__single_L2A | 2 | 3 | 4 | 1 | 1 | [0.301, 0.954] |
| lbush_radio_2001 | val | lbush_radio_2001__single_L2B | 2 | 4 | 4 | 1 | 0 | [0.51, 1] |
| lbush_radio_2001 | val | lbush_radio_2001__single_L3A | 3 | 4 | 4 | 1 | 1 | [0.51, 1] |
| lbush_radio_2001 | val | lbush_radio_2001__single_L3B | 3 | 4 | 4 | 0 | 0 | [0.51, 1] |
| mobama_weekly_2014 | test | mobama_weekly_2014__single_L2A | 2 | 3 | 4 | 1 | 1 | [0.301, 0.954] |
| mobama_weekly_2014 | test | mobama_weekly_2014__single_L2B | 2 | 4 | 4 | 1 | 0 | [0.51, 1] |
| mobama_weekly_2014 | test | mobama_weekly_2014__single_L3A | 3 | 3 | 4 | 1 | 1 | [0.301, 0.954] |
| mobama_weekly_2014 | test | mobama_weekly_2014__single_L3B | 3 | 4 | 4 | 0 | 0 | [0.51, 1] |
| nixon_resignation_1974 | test | nixon_resignation_1974__single_L2A | 2 | 4 | 4 | 1 | 0 | [0.51, 1] |
| nixon_resignation_1974 | test | nixon_resignation_1974__single_L2B | 2 | 3 | 4 | 0 | 0 | [0.301, 0.954] |
| nixon_resignation_1974 | test | nixon_resignation_1974__single_L3A | 3 | 4 | 4 | 1 | 1 | [0.51, 1] |
| nixon_resignation_1974 | test | nixon_resignation_1974__single_L3B | 3 | 4 | 4 | 0 | 0 | [0.51, 1] |
| obama_weekly_2009 | train | obama_weekly_2009__single_L2A | 2 | 4 | 4 | 0 | 1 | [0.51, 1] |
| obama_weekly_2009 | train | obama_weekly_2009__single_L2B | 2 | 3 | 4 | 2 | 0 | [0.301, 0.954] |
| obama_weekly_2009 | train | obama_weekly_2009__single_L3A | 3 | 4 | 4 | 1 | 0 | [0.51, 1] |
| obama_weekly_2009 | train | obama_weekly_2009__single_L3B | 3 | 4 | 4 | 0 | 0 | [0.51, 1] |
| reagan_farewell_1989 | train | reagan_farewell_1989__single_L2A | 2 | 3 | 4 | 1 | 1 | [0.301, 0.954] |
| reagan_farewell_1989 | train | reagan_farewell_1989__single_L2B | 2 | 3 | 4 | 0 | 0 | [0.301, 0.954] |
| reagan_farewell_1989 | train | reagan_farewell_1989__single_L3A | 3 | 4 | 4 | 1 | 1 | [0.51, 1] |
| reagan_farewell_1989 | train | reagan_farewell_1989__single_L3B | 3 | 4 | 4 | 0 | 0 | [0.51, 1] |

lab_passed:

| speech | split | clip | level | detected k | of n | false regions (one detection per change; same-change duplicates reported separately) | same-change duplicates | 95% Wilson |
|---|---|---|---|---|---|---|---|---|
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__extra_L2A | 2 | 0 | 1 | 2 | 0 | [0, 0.793] |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__extra_L3A | 3 | 1 | 1 | 3 | 0 | [0.207, 1] |
| gwbush_911_2001 | train | gwbush_911_2001__extra_L2A | 2 | 1 | 1 | 1 | 0 | [0.207, 1] |
| gwbush_911_2001 | train | gwbush_911_2001__extra_L3A | 3 | 0 | 1 | 2 | 0 | [0, 0.793] |
| harris_uncsw_2021 | train | harris_uncsw_2021__extra_L2A | 2 | 0 | 1 | 0 | 0 | [0, 0.793] |
| harris_uncsw_2021 | train | harris_uncsw_2021__extra_L3A | 3 | 0 | 1 | 0 | 0 | [0, 0.793] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__extra_L2A | 2 | 0 | 1 | 1 | 0 | [0, 0.793] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__extra_L3A | 3 | 1 | 1 | 1 | 0 | [0.207, 1] |
| lbush_radio_2001 | val | lbush_radio_2001__extra_L2A | 2 | 0 | 1 | 0 | 0 | [0, 0.793] |
| lbush_radio_2001 | val | lbush_radio_2001__extra_L3A | 3 | 0 | 1 | 1 | 0 | [0, 0.793] |
| mobama_weekly_2014 | test | mobama_weekly_2014__extra_L2A | 2 | 0 | 1 | 1 | 0 | [0, 0.793] |
| mobama_weekly_2014 | test | mobama_weekly_2014__extra_L3A | 3 | 0 | 1 | 2 | 0 | [0, 0.793] |
| nixon_resignation_1974 | test | nixon_resignation_1974__extra_L2A | 2 | 0 | 1 | 2 | 0 | [0, 0.793] |
| nixon_resignation_1974 | test | nixon_resignation_1974__extra_L3A | 3 | 1 | 1 | 2 | 0 | [0.207, 1] |
| obama_weekly_2009 | train | obama_weekly_2009__extra_L2A | 2 | 0 | 1 | 0 | 0 | [0, 0.793] |
| obama_weekly_2009 | train | obama_weekly_2009__extra_L3A | 3 | 0 | 1 | 0 | 0 | [0, 0.793] |
| reagan_farewell_1989 | train | reagan_farewell_1989__extra_L2A | 2 | 0 | 1 | 0 | 0 | [0, 0.793] |
| reagan_farewell_1989 | train | reagan_farewell_1989__extra_L3A | 3 | 0 | 1 | 1 | 0 | [0, 0.793] |

synthetic_only (unvalidated):

| speech | split | clip | level | detected k | of n | false regions (one detection per change; same-change duplicates reported separately) | same-change duplicates | 95% Wilson |
|---|---|---|---|---|---|---|---|---|
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__extra_L2A | 2 | 0 | 0 | 0 | 0 | [n/a, n/a] |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__extra_L2B | 2 | 1 | 2 | 1 | 0 | [0.0945, 0.905] |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__extra_L2C | 2 | 0 | 5 | 1 | 0 | [0, 0.434] |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__extra_L2D | 2 | 0 | 0 | 2 | 0 | [n/a, n/a] |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__extra_L3A | 3 | 0 | 0 | 1 | 0 | [n/a, n/a] |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__extra_L3B | 3 | 1 | 2 | 1 | 0 | [0.0945, 0.905] |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__extra_L3C | 3 | 0 | 5 | 1 | 0 | [0, 0.434] |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__extra_L3D | 3 | 0 | 0 | 2 | 0 | [n/a, n/a] |
| gwbush_911_2001 | train | gwbush_911_2001__extra_L2A | 2 | 1 | 1 | 0 | 0 | [0.207, 1] |
| gwbush_911_2001 | train | gwbush_911_2001__extra_L2B | 2 | 1 | 2 | 2 | 0 | [0.0945, 0.905] |
| gwbush_911_2001 | train | gwbush_911_2001__extra_L2C | 2 | 0 | 8 | 1 | 0 | [0, 0.324] |
| gwbush_911_2001 | train | gwbush_911_2001__extra_L2D | 2 | 0 | 0 | 2 | 0 | [n/a, n/a] |
| gwbush_911_2001 | train | gwbush_911_2001__extra_L3A | 3 | 1 | 1 | 1 | 0 | [0.207, 1] |
| gwbush_911_2001 | train | gwbush_911_2001__extra_L3B | 3 | 1 | 2 | 2 | 0 | [0.0945, 0.905] |
| gwbush_911_2001 | train | gwbush_911_2001__extra_L3C | 3 | 1 | 8 | 1 | 0 | [0.0224, 0.471] |
| gwbush_911_2001 | train | gwbush_911_2001__extra_L3D | 3 | 0 | 0 | 2 | 0 | [n/a, n/a] |
| harris_uncsw_2021 | train | harris_uncsw_2021__extra_L2A | 2 | 0 | 0 | 0 | 0 | [n/a, n/a] |
| harris_uncsw_2021 | train | harris_uncsw_2021__extra_L2B | 2 | 1 | 1 | 1 | 0 | [0.207, 1] |
| harris_uncsw_2021 | train | harris_uncsw_2021__extra_L2C | 2 | 0 | 8 | 1 | 0 | [0, 0.324] |
| harris_uncsw_2021 | train | harris_uncsw_2021__extra_L2D | 2 | 0 | 0 | 2 | 0 | [n/a, n/a] |
| harris_uncsw_2021 | train | harris_uncsw_2021__extra_L3A | 3 | 0 | 0 | 0 | 0 | [n/a, n/a] |
| harris_uncsw_2021 | train | harris_uncsw_2021__extra_L3B | 3 | 2 | 2 | 3 | 0 | [0.342, 1] |
| harris_uncsw_2021 | train | harris_uncsw_2021__extra_L3C | 3 | 0 | 8 | 1 | 0 | [0, 0.324] |
| harris_uncsw_2021 | train | harris_uncsw_2021__extra_L3D | 3 | 0 | 0 | 2 | 0 | [n/a, n/a] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__extra_L2A | 2 | 0 | 1 | 0 | 0 | [0, 0.793] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__extra_L2B | 2 | 1 | 2 | 0 | 0 | [0.0945, 0.905] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__extra_L2C | 2 | 0 | 6 | 1 | 0 | [0, 0.39] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__extra_L2D | 2 | 0 | 0 | 2 | 0 | [n/a, n/a] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__extra_L3A | 3 | 1 | 1 | 1 | 0 | [0.207, 1] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__extra_L3B | 3 | 1 | 2 | 1 | 0 | [0.0945, 0.905] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__extra_L3C | 3 | 1 | 6 | 1 | 0 | [0.0301, 0.564] |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__extra_L3D | 3 | 0 | 0 | 2 | 0 | [n/a, n/a] |
| lbush_radio_2001 | val | lbush_radio_2001__extra_L2A | 2 | 0 | 0 | 0 | 0 | [n/a, n/a] |
| lbush_radio_2001 | val | lbush_radio_2001__extra_L2B | 2 | 1 | 2 | 0 | 0 | [0.0945, 0.905] |
| lbush_radio_2001 | val | lbush_radio_2001__extra_L2C | 2 | 0 | 5 | 3 | 0 | [0, 0.434] |
| lbush_radio_2001 | val | lbush_radio_2001__extra_L2D | 2 | 0 | 0 | 1 | 0 | [n/a, n/a] |
| lbush_radio_2001 | val | lbush_radio_2001__extra_L3A | 3 | 0 | 0 | 1 | 0 | [n/a, n/a] |
| lbush_radio_2001 | val | lbush_radio_2001__extra_L3B | 3 | 2 | 2 | 0 | 0 | [0.342, 1] |
| lbush_radio_2001 | val | lbush_radio_2001__extra_L3C | 3 | 0 | 5 | 3 | 0 | [0, 0.434] |
| lbush_radio_2001 | val | lbush_radio_2001__extra_L3D | 3 | 0 | 0 | 2 | 0 | [n/a, n/a] |
| mobama_weekly_2014 | test | mobama_weekly_2014__extra_L2A | 2 | 0 | 0 | 0 | 0 | [n/a, n/a] |
| mobama_weekly_2014 | test | mobama_weekly_2014__extra_L2B | 2 | 1 | 2 | 1 | 0 | [0.0945, 0.905] |
| mobama_weekly_2014 | test | mobama_weekly_2014__extra_L2C | 2 | 0 | 7 | 1 | 0 | [0, 0.354] |
| mobama_weekly_2014 | test | mobama_weekly_2014__extra_L2D | 2 | 0 | 0 | 3 | 0 | [n/a, n/a] |
| mobama_weekly_2014 | test | mobama_weekly_2014__extra_L3A | 3 | 0 | 0 | 1 | 0 | [n/a, n/a] |
| mobama_weekly_2014 | test | mobama_weekly_2014__extra_L3B | 3 | 2 | 2 | 3 | 0 | [0.342, 1] |
| mobama_weekly_2014 | test | mobama_weekly_2014__extra_L3C | 3 | 0 | 7 | 1 | 0 | [0, 0.354] |
| mobama_weekly_2014 | test | mobama_weekly_2014__extra_L3D | 3 | 0 | 0 | 3 | 0 | [n/a, n/a] |
| nixon_resignation_1974 | test | nixon_resignation_1974__extra_L2A | 2 | 1 | 1 | 1 | 0 | [0.207, 1] |
| nixon_resignation_1974 | test | nixon_resignation_1974__extra_L2B | 2 | 1 | 2 | 2 | 0 | [0.0945, 0.905] |
| nixon_resignation_1974 | test | nixon_resignation_1974__extra_L2C | 2 | 0 | 8 | 1 | 0 | [0, 0.324] |
| nixon_resignation_1974 | test | nixon_resignation_1974__extra_L2D | 2 | 0 | 0 | 2 | 0 | [n/a, n/a] |
| nixon_resignation_1974 | test | nixon_resignation_1974__extra_L3A | 3 | 1 | 1 | 2 | 0 | [0.207, 1] |
| nixon_resignation_1974 | test | nixon_resignation_1974__extra_L3B | 3 | 1 | 2 | 3 | 0 | [0.0945, 0.905] |
| nixon_resignation_1974 | test | nixon_resignation_1974__extra_L3C | 3 | 1 | 8 | 1 | 0 | [0.0224, 0.471] |
| nixon_resignation_1974 | test | nixon_resignation_1974__extra_L3D | 3 | 0 | 0 | 3 | 0 | [n/a, n/a] |
| obama_weekly_2009 | train | obama_weekly_2009__extra_L2A | 2 | 0 | 1 | 1 | 0 | [0, 0.793] |
| obama_weekly_2009 | train | obama_weekly_2009__extra_L2B | 2 | 1 | 2 | 2 | 0 | [0.0945, 0.905] |
| obama_weekly_2009 | train | obama_weekly_2009__extra_L2C | 2 | 0 | 6 | 1 | 0 | [0, 0.39] |
| obama_weekly_2009 | train | obama_weekly_2009__extra_L2D | 2 | 0 | 0 | 2 | 0 | [n/a, n/a] |
| obama_weekly_2009 | train | obama_weekly_2009__extra_L3A | 3 | 0 | 1 | 1 | 0 | [0, 0.793] |
| obama_weekly_2009 | train | obama_weekly_2009__extra_L3B | 3 | 1 | 2 | 2 | 0 | [0.0945, 0.905] |
| obama_weekly_2009 | train | obama_weekly_2009__extra_L3C | 3 | 1 | 6 | 1 | 0 | [0.0301, 0.564] |
| obama_weekly_2009 | train | obama_weekly_2009__extra_L3D | 3 | 0 | 0 | 3 | 0 | [n/a, n/a] |
| reagan_farewell_1989 | train | reagan_farewell_1989__extra_L2A | 2 | 1 | 1 | 0 | 0 | [0.207, 1] |
| reagan_farewell_1989 | train | reagan_farewell_1989__extra_L2B | 2 | 1 | 2 | 2 | 0 | [0.0945, 0.905] |
| reagan_farewell_1989 | train | reagan_farewell_1989__extra_L2C | 2 | 0 | 6 | 1 | 0 | [0, 0.39] |
| reagan_farewell_1989 | train | reagan_farewell_1989__extra_L2D | 2 | 0 | 0 | 2 | 0 | [n/a, n/a] |
| reagan_farewell_1989 | train | reagan_farewell_1989__extra_L3A | 3 | 1 | 1 | 2 | 0 | [0.207, 1] |
| reagan_farewell_1989 | train | reagan_farewell_1989__extra_L3B | 3 | 1 | 2 | 2 | 0 | [0.0945, 0.905] |
| reagan_farewell_1989 | train | reagan_farewell_1989__extra_L3C | 3 | 1 | 6 | 1 | 0 | [0.0301, 0.564] |
| reagan_farewell_1989 | train | reagan_farewell_1989__extra_L3D | 3 | 0 | 0 | 3 | 0 | [n/a, n/a] |

## Whole-clip flags on flawed clips

core8:

| split | whole-clip flags on flawed clips | clips |
|---|---|---|
| train | 0 | none |
| val | 0 | none |
| test | 0 | none |
| val+test | 0 | none |

lab_passed:

| split | whole-clip flags on flawed clips | clips |
|---|---|---|
| train | 0 | none |
| val | 0 | none |
| test | 0 | none |
| val+test | 0 | none |

synthetic_only (unvalidated):

| split | whole-clip flags on flawed clips | clips |
|---|---|---|
| train | 0 | none |
| val | 0 | none |
| test | 0 | none |
| val+test | 0 | none |

## Pause localisation error (matched boundary events)

core8:

| split | clip | type | pause onset error (ms) | pause offset error (ms) |
|---|---|---|---|---|
| val | eisenhower_farewell_1961__single_L2A | PAUSE_DROPPED | -19.3 | -149 |
| val | eisenhower_farewell_1961__single_L2B | PAUSE_INTRUSIVE | 0 | 10 |
| val | eisenhower_farewell_1961__single_L3A | PAUSE_DROPPED | 58.9 | -1.1 |
| val | eisenhower_farewell_1961__single_L3B | PAUSE_INTRUSIVE | -10 | 20 |
| train | gwbush_911_2001__single_L2A | PAUSE_DROPPED | -3.4 | -1.4 |
| train | gwbush_911_2001__single_L2B | PAUSE_INTRUSIVE | -40 | 20 |
| train | gwbush_911_2001__single_L3A | PAUSE_DROPPED | -10.8 | -70.8 |
| train | gwbush_911_2001__single_L3B | PAUSE_INTRUSIVE | 10 | 0 |
| train | harris_uncsw_2021__single_L2A | PAUSE_DROPPED | 0 | 0 |
| train | harris_uncsw_2021__single_L2B | PAUSE_INTRUSIVE | -2.3 | 7.7 |
| train | harris_uncsw_2021__single_L3A | PAUSE_DROPPED | 6 | -54 |
| train | harris_uncsw_2021__single_L3B | PAUSE_INTRUSIVE | 10 | 0 |
| train | hclinton_tomorrow_2010__single_L2A | PAUSE_DROPPED | 30 | -80 |
| train | hclinton_tomorrow_2010__single_L2B | PAUSE_INTRUSIVE | 10 | 0 |
| train | hclinton_tomorrow_2010__single_L3A | PAUSE_DROPPED | 58.2 | -1.8 |
| train | hclinton_tomorrow_2010__single_L3B | PAUSE_INTRUSIVE | 11 | 1 |
| val | lbush_radio_2001__single_L2A | PAUSE_DROPPED | 128 | -53.6 |
| val | lbush_radio_2001__single_L2B | PAUSE_INTRUSIVE | 3.2 | 23.2 |
| val | lbush_radio_2001__single_L3A | PAUSE_DROPPED | 4.5 | -55.5 |
| val | lbush_radio_2001__single_L3B | PAUSE_INTRUSIVE | -126 | 34 |
| test | mobama_weekly_2014__single_L2A | PAUSE_DROPPED | 36.7 | -77.3 |
| test | mobama_weekly_2014__single_L2B | PAUSE_INTRUSIVE | -10 | 10 |
| test | mobama_weekly_2014__single_L3A | PAUSE_DROPPED | 5 | -55 |
| test | mobama_weekly_2014__single_L3B | PAUSE_INTRUSIVE | 11 | 1 |
| test | nixon_resignation_1974__single_L2A | PAUSE_DROPPED | 33.6 | -108 |
| test | nixon_resignation_1974__single_L2B | PAUSE_INTRUSIVE | 10 | 0 |
| test | nixon_resignation_1974__single_L3A | PAUSE_DROPPED | -10.9 | -70.9 |
| test | nixon_resignation_1974__single_L3B | PAUSE_INTRUSIVE | 10 | 0 |
| train | obama_weekly_2009__single_L2A | PAUSE_DROPPED | 65.5 | -68.5 |
| train | obama_weekly_2009__single_L2B | PAUSE_INTRUSIVE | 247 | -2.7 |
| train | obama_weekly_2009__single_L3A | PAUSE_DROPPED | 21.1 | -38.9 |
| train | obama_weekly_2009__single_L3B | PAUSE_INTRUSIVE | 10 | 0 |
| train | reagan_farewell_1989__single_L2A | PAUSE_DROPPED | 70.4 | -41.6 |
| train | reagan_farewell_1989__single_L2B | PAUSE_INTRUSIVE | 12 | 2 |
| train | reagan_farewell_1989__single_L3A | PAUSE_DROPPED | 5.1 | -54.9 |
| train | reagan_farewell_1989__single_L3B | PAUSE_INTRUSIVE | 10 | 0 |

lab_passed:

| split | clip | type | pause onset error (ms) | pause offset error (ms) |
|---|---|---|---|---|

synthetic_only (unvalidated):

| split | clip | type | pause onset error (ms) | pause offset error (ms) |
|---|---|---|---|---|
| val | eisenhower_farewell_1961__extra_L2B | HESITATION | 6.4 | 6.4 |
| val | eisenhower_farewell_1961__extra_L3B | HESITATION | 0.4 | 0.4 |
| train | gwbush_911_2001__extra_L2B | HESITATION | 10 | 0 |
| train | gwbush_911_2001__extra_L3B | HESITATION | 10 | 0 |
| train | harris_uncsw_2021__extra_L2B | HESITATION | -3.1 | 6.9 |
| train | harris_uncsw_2021__extra_L3B | HESITATION | -3.5 | 6.5 |
| train | hclinton_tomorrow_2010__extra_L2B | HESITATION | -40 | 20 |
| train | hclinton_tomorrow_2010__extra_L3B | HESITATION | -40 | 10 |
| val | lbush_radio_2001__extra_L2B | HESITATION | 10 | 0 |
| val | lbush_radio_2001__extra_L3B | HESITATION | 10 | 0 |
| test | mobama_weekly_2014__extra_L2B | HESITATION | -4 | 16 |
| test | mobama_weekly_2014__extra_L3B | HESITATION | -0.3 | 19.7 |
| test | nixon_resignation_1974__extra_L2B | HESITATION | -80 | 30 |
| test | nixon_resignation_1974__extra_L3B | HESITATION | -80 | 30 |
| train | obama_weekly_2009__extra_L2B | HESITATION | -20 | 20 |
| train | obama_weekly_2009__extra_L3B | HESITATION | -20 | 20 |
| train | reagan_farewell_1989__extra_L2B | HESITATION | 8.4 | -1.6 |
| train | reagan_farewell_1989__extra_L3B | HESITATION | 11.1 | 1.1 |

## Onset / offset absolute error of matched regions (FADE late onset is expected)

core8:

| split | type | n matched | onset median (ms) | onset P90 (ms) | offset median (ms) | offset P90 (ms) |
|---|---|---|---|---|---|---|
| train | DRAG | 10 | 79 | 275 | 172 | 493 |
| train | FADE | 10 | 101 | 342 | 69.5 | 294 |
| train | MONOTONE | 9 | 337 | 971 | 60 | 262 |
| train | MUMBLE | 10 | 202 | 461 | 260 | 334 |
| train | RUSH | 8 | 72 | 136 | 106 | 290 |
| val | DRAG | 4 | 65.6 | 83.4 | 206 | 530 |
| val | FADE | 2 | 495 | 587 | 900 | 1400 |
| val | MONOTONE | 4 | 375 | 964 | 415 | 964 |
| val | MUMBLE | 4 | 322 | 369 | 163 | 630 |
| val | RUSH | 4 | 20 | 307 | 11.5 | 59.3 |
| test | DRAG | 4 | 74 | 252 | 210 | 586 |
| test | FADE | 4 | 186 | 248 | 124 | 292 |
| test | MONOTONE | 2 | 306 | 501 | 134 | 201 |
| test | MUMBLE | 4 | 70 | 188 | 35 | 698 |
| test | RUSH | 3 | 10 | 38.8 | 232 | 294 |
| val+test | DRAG | 8 | 69 | 161 | 206 | 672 |
| val+test | FADE | 6 | 231 | 495 | 234 | 931 |
| val+test | MONOTONE | 6 | 375 | 867 | 259 | 840 |
| val+test | MUMBLE | 8 | 200 | 354 | 100 | 868 |
| val+test | RUSH | 7 | 20 | 200 | 14.7 | 263 |

Grounding of IoU true positives; an edge outside EVENT_TOL_S remains a coarse-edge TP:

| split | type | matched | coarse-edge TP | both edges within 0.20 s | onset median (ms); interval | onset P90; interval | offset median; interval | offset P90; interval |
|---|---|---|---|---|---|---|---|---|
| train | RUSH | 8 | 1 | 7 | 72; 95% [20, 114] | 136; 95% [122, 150] | 106; 95% [52, 150] | 290; 95% [138, 590] |
| train | DRAG | 10 | 6 | 4 | 79; 95% [51.9, 144] | 275; 95% [86, 320] | 172; 95% [90.5, 216] | 493; 95% [222, 727] |
| train | MONOTONE | 9 | 7 | 2 | 337; 95% [70, 430] | 971; 95% [355, 976] | 60; 95% [60, 132] | 262; 95% [129, 350] |
| train | FADE | 10 | 6 | 4 | 101; 95% [39.4, 186] | 342; 95% [205, 1260] | 69.5; 95% [40.6, 180] | 294; 95% [79.9, 510] |
| train | MUMBLE | 10 | 9 | 1 | 202; 95% [132, 410] | 461; 95% [215, 924] | 260; 95% [221, 309] | 334; 95% [321, 373] |
| val | RUSH | 4 | 1 | 3 | 20; per speaker: eisenhower_farewell_1961 20, lbush_radio_2001 220; range [20, 220] | 307; per speaker: eisenhower_farewell_1961 20, lbush_radio_2001 388; range [20, 388] | 11.5; per speaker: eisenhower_farewell_1961 40.2, lbush_radio_2001 11.5; range [11.5, 40.2] | 59.3; per speaker: eisenhower_farewell_1961 70.8, lbush_radio_2001 14.1; range [14.1, 70.8] |
| val | DRAG | 4 | 2 | 2 | 65.6; per speaker: eisenhower_farewell_1961 59, lbush_radio_2001 76.6; range [59, 76.6] | 83.4; per speaker: eisenhower_farewell_1961 66.2, lbush_radio_2001 87.3; range [66.2, 87.3] | 206; per speaker: eisenhower_farewell_1961 448, lbush_radio_2001 132; range [132, 448] | 530; per speaker: eisenhower_farewell_1961 611, lbush_radio_2001 160; range [160, 611] |
| val | MONOTONE | 4 | 4 | 0 | 375; per speaker: eisenhower_farewell_1961 165, lbush_radio_2001 817; range [165, 817] | 964; per speaker: eisenhower_farewell_1961 273, lbush_radio_2001 1110; range [273, 1110] | 415; per speaker: eisenhower_farewell_1961 840, lbush_radio_2001 172; range [172, 840] | 964; per speaker: eisenhower_farewell_1961 1090, lbush_radio_2001 274; range [274, 1090] |
| val | FADE | 2 | 2 | 0 | 495; per speaker: eisenhower_farewell_1961 610, lbush_radio_2001 380; range [380, 610] | 587; per speaker: eisenhower_farewell_1961 610, lbush_radio_2001 380; range [380, 610] | 900; per speaker: eisenhower_farewell_1961 1530, lbush_radio_2001 270; range [270, 1530] | 1400; per speaker: eisenhower_farewell_1961 1530, lbush_radio_2001 270; range [270, 1530] |
| val | MUMBLE | 4 | 3 | 1 | 322; per speaker: eisenhower_farewell_1961 235, lbush_radio_2001 362; range [235, 362] | 369; per speaker: eisenhower_farewell_1961 288, lbush_radio_2001 376; range [288, 376] | 163; per speaker: eisenhower_farewell_1961 480, lbush_radio_2001 123; range [123, 480] | 630; per speaker: eisenhower_farewell_1961 751, lbush_radio_2001 174; range [174, 751] |
| test | RUSH | 3 | 2 | 1 | 10; per speaker: mobama_weekly_2014 28, nixon_resignation_1974 10; range [10, 28] | 38.8; per speaker: mobama_weekly_2014 42.4, nixon_resignation_1974 10; range [10, 42.4] | 232; per speaker: mobama_weekly_2014 161, nixon_resignation_1974 232; range [161, 232] | 294; per speaker: mobama_weekly_2014 279, nixon_resignation_1974 232; range [232, 279] |
| test | DRAG | 4 | 2 | 2 | 74; per speaker: mobama_weekly_2014 188, nixon_resignation_1974 74; range [74, 188] | 252; per speaker: mobama_weekly_2014 298, nixon_resignation_1974 77.1; range [77.1, 298] | 210; per speaker: mobama_weekly_2014 405, nixon_resignation_1974 210; range [210, 405] | 586; per speaker: mobama_weekly_2014 658, nixon_resignation_1974 257; range [257, 658] |
| test | MONOTONE | 2 | 2 | 0 | 306; per speaker: nixon_resignation_1974 306; range [306, 306] | 501; per speaker: nixon_resignation_1974 501; range [501, 501] | 134; per speaker: nixon_resignation_1974 134; range [134, 134] | 201; per speaker: nixon_resignation_1974 201; range [201, 201] |
| test | FADE | 4 | 1 | 3 | 186; per speaker: mobama_weekly_2014 186, nixon_resignation_1974 161; range [161, 186] | 248; per speaker: mobama_weekly_2014 190, nixon_resignation_1974 250; range [190, 250] | 124; per speaker: mobama_weekly_2014 124, nixon_resignation_1974 191; range [124, 191] | 292; per speaker: mobama_weekly_2014 183, nixon_resignation_1974 304; range [183, 304] |
| test | MUMBLE | 4 | 2 | 2 | 70; per speaker: mobama_weekly_2014 140, nixon_resignation_1974 60; range [60, 140] | 188; per speaker: mobama_weekly_2014 212, nixon_resignation_1974 84; range [84, 212] | 35; per speaker: mobama_weekly_2014 35, nixon_resignation_1974 495; range [35, 495] | 698; per speaker: mobama_weekly_2014 39, nixon_resignation_1974 883; range [39, 883] |
| val+test | RUSH | 7 | 3 | 4 | 20; per speaker: eisenhower_farewell_1961 20, lbush_radio_2001 220, mobama_weekly_2014 28, nixon_resignation_1974 10; range [10, 220] | 200; per speaker: eisenhower_farewell_1961 20, lbush_radio_2001 388, mobama_weekly_2014 42.4, nixon_resignation_1974 10; range [10, 388] | 14.7; per speaker: eisenhower_farewell_1961 40.2, lbush_radio_2001 11.5, mobama_weekly_2014 161, nixon_resignation_1974 232; range [11.5, 232] | 263; per speaker: eisenhower_farewell_1961 70.8, lbush_radio_2001 14.1, mobama_weekly_2014 279, nixon_resignation_1974 232; range [14.1, 279] |
| val+test | DRAG | 8 | 4 | 4 | 69; per speaker: eisenhower_farewell_1961 59, lbush_radio_2001 76.6, mobama_weekly_2014 188, nixon_resignation_1974 74; range [59, 188] | 161; per speaker: eisenhower_farewell_1961 66.2, lbush_radio_2001 87.3, mobama_weekly_2014 298, nixon_resignation_1974 77.1; range [66.2, 298] | 206; per speaker: eisenhower_farewell_1961 448, lbush_radio_2001 132, mobama_weekly_2014 405, nixon_resignation_1974 210; range [132, 448] | 672; per speaker: eisenhower_farewell_1961 611, lbush_radio_2001 160, mobama_weekly_2014 658, nixon_resignation_1974 257; range [160, 658] |
| val+test | MONOTONE | 6 | 6 | 0 | 375; per speaker: eisenhower_farewell_1961 165, lbush_radio_2001 817, nixon_resignation_1974 306; range [165, 817] | 867; per speaker: eisenhower_farewell_1961 273, lbush_radio_2001 1110, nixon_resignation_1974 501; range [273, 1110] | 259; per speaker: eisenhower_farewell_1961 840, lbush_radio_2001 172, nixon_resignation_1974 134; range [134, 840] | 840; per speaker: eisenhower_farewell_1961 1090, lbush_radio_2001 274, nixon_resignation_1974 201; range [201, 1090] |
| val+test | FADE | 6 | 3 | 3 | 231; per speaker: eisenhower_farewell_1961 610, lbush_radio_2001 380, mobama_weekly_2014 186, nixon_resignation_1974 161; range [161, 610] | 495; per speaker: eisenhower_farewell_1961 610, lbush_radio_2001 380, mobama_weekly_2014 190, nixon_resignation_1974 250; range [190, 610] | 234; per speaker: eisenhower_farewell_1961 1530, lbush_radio_2001 270, mobama_weekly_2014 124, nixon_resignation_1974 191; range [124, 1530] | 931; per speaker: eisenhower_farewell_1961 1530, lbush_radio_2001 270, mobama_weekly_2014 183, nixon_resignation_1974 304; range [183, 1530] |
| val+test | MUMBLE | 8 | 5 | 3 | 200; per speaker: eisenhower_farewell_1961 235, lbush_radio_2001 362, mobama_weekly_2014 140, nixon_resignation_1974 60; range [60, 362] | 354; per speaker: eisenhower_farewell_1961 288, lbush_radio_2001 376, mobama_weekly_2014 212, nixon_resignation_1974 84; range [84, 376] | 100; per speaker: eisenhower_farewell_1961 480, lbush_radio_2001 123, mobama_weekly_2014 35, nixon_resignation_1974 495; range [35, 495] | 868; per speaker: eisenhower_farewell_1961 751, lbush_radio_2001 174, mobama_weekly_2014 39, nixon_resignation_1974 883; range [39, 883] |

lab_passed:

| split | type | n matched | onset median (ms) | onset P90 (ms) | offset median (ms) | offset P90 (ms) |
|---|---|---|---|---|---|---|
| train | NATURAL_RUSH | 2 | 180 | 324 | 259 | 466 |
| val | NATURAL_RUSH | 1 | 5.7 | 5.7 | 681 | 681 |
| test | NATURAL_RUSH | 1 | 477 | 477 | 3.8 | 3.8 |
| val+test | NATURAL_RUSH | 2 | 242 | 430 | 342 | 613 |

Grounding of IoU true positives; an edge outside EVENT_TOL_S remains a coarse-edge TP:

| split | type | matched | coarse-edge TP | both edges within 0.20 s | onset median (ms); interval | onset P90; interval | offset median; interval | offset P90; interval |
|---|---|---|---|---|---|---|---|---|
| train | NATURAL_RUSH | 2 | 2 | 0 | 180; per speaker: gwbush_911_2001 0, hclinton_tomorrow_2010 360; range [0, 360] | 324; per speaker: gwbush_911_2001 0, hclinton_tomorrow_2010 360; range [0, 360] | 259; per speaker: gwbush_911_2001 518, hclinton_tomorrow_2010 0.3; range [0.3, 518] | 466; per speaker: gwbush_911_2001 518, hclinton_tomorrow_2010 0.3; range [0.3, 518] |
| val | NATURAL_RUSH | 1 | 1 | 0 | 5.7; per speaker: eisenhower_farewell_1961 5.7; range [5.7, 5.7] | 5.7; per speaker: eisenhower_farewell_1961 5.7; range [5.7, 5.7] | 681; per speaker: eisenhower_farewell_1961 681; range [681, 681] | 681; per speaker: eisenhower_farewell_1961 681; range [681, 681] |
| test | NATURAL_RUSH | 1 | 1 | 0 | 477; per speaker: nixon_resignation_1974 477; range [477, 477] | 477; per speaker: nixon_resignation_1974 477; range [477, 477] | 3.8; per speaker: nixon_resignation_1974 3.8; range [3.8, 3.8] | 3.8; per speaker: nixon_resignation_1974 3.8; range [3.8, 3.8] |
| val+test | NATURAL_RUSH | 2 | 2 | 0 | 242; per speaker: eisenhower_farewell_1961 5.7, nixon_resignation_1974 477; range [5.7, 477] | 430; per speaker: eisenhower_farewell_1961 5.7, nixon_resignation_1974 477; range [5.7, 477] | 342; per speaker: eisenhower_farewell_1961 681, nixon_resignation_1974 3.8; range [3.8, 681] | 613; per speaker: eisenhower_farewell_1961 681, nixon_resignation_1974 3.8; range [3.8, 681] |

synthetic_only (unvalidated):

| split | type | n matched | onset median (ms) | onset P90 (ms) | offset median (ms) | offset P90 (ms) |
|---|---|---|---|---|---|---|
| train | LOW_EFFORT | 5 | 60 | 192 | 400 | 784 |
| train | TRAILING_OFF | 4 | 0 | 0 | 20 | 62 |
| test | LOW_EFFORT | 2 | 300 | 300 | 140 | 156 |
| test | TRAILING_OFF | 1 | 0 | 0 | 0 | 0 |
| val+test | LOW_EFFORT | 2 | 300 | 300 | 140 | 156 |
| val+test | TRAILING_OFF | 1 | 0 | 0 | 0 | 0 |

Grounding of IoU true positives; an edge outside EVENT_TOL_S remains a coarse-edge TP:

| split | type | matched | coarse-edge TP | both edges within 0.20 s | onset median (ms); interval | onset P90; interval | offset median; interval | offset P90; interval |
|---|---|---|---|---|---|---|---|---|
| train | LOW_EFFORT | 5 | 3 | 2 | 60; per speaker: gwbush_911_2001 60, hclinton_tomorrow_2010 280, reagan_farewell_1989 6.9; range [6.9, 280] | 192; per speaker: gwbush_911_2001 60, hclinton_tomorrow_2010 280, reagan_farewell_1989 11.5; range [11.5, 280] | 400; per speaker: gwbush_911_2001 400, hclinton_tomorrow_2010 1040, reagan_farewell_1989 15.7; range [15.7, 1040] | 784; per speaker: gwbush_911_2001 400, hclinton_tomorrow_2010 1040, reagan_farewell_1989 18.2; range [18.2, 1040] |
| train | TRAILING_OFF | 4 | 0 | 4 | 0; per speaker: gwbush_911_2001 0, hclinton_tomorrow_2010 0, obama_weekly_2009 0, reagan_farewell_1989 0; range [0, 0] | 0; per speaker: gwbush_911_2001 0, hclinton_tomorrow_2010 0, obama_weekly_2009 0, reagan_farewell_1989 0; range [0, 0] | 20; per speaker: gwbush_911_2001 20, hclinton_tomorrow_2010 20, obama_weekly_2009 80, reagan_farewell_1989 20; range [20, 80] | 62; per speaker: gwbush_911_2001 20, hclinton_tomorrow_2010 20, obama_weekly_2009 80, reagan_farewell_1989 20; range [20, 80] |
| test | LOW_EFFORT | 2 | 2 | 0 | 300; per speaker: nixon_resignation_1974 300; range [300, 300] | 300; per speaker: nixon_resignation_1974 300; range [300, 300] | 140; per speaker: nixon_resignation_1974 140; range [140, 140] | 156; per speaker: nixon_resignation_1974 156; range [156, 156] |
| test | TRAILING_OFF | 1 | 0 | 1 | 0; per speaker: nixon_resignation_1974 0; range [0, 0] | 0; per speaker: nixon_resignation_1974 0; range [0, 0] | 0; per speaker: nixon_resignation_1974 0; range [0, 0] | 0; per speaker: nixon_resignation_1974 0; range [0, 0] |
| val+test | LOW_EFFORT | 2 | 2 | 0 | 300; per speaker: nixon_resignation_1974 300; range [300, 300] | 300; per speaker: nixon_resignation_1974 300; range [300, 300] | 140; per speaker: nixon_resignation_1974 140; range [140, 140] | 156; per speaker: nixon_resignation_1974 156; range [156, 156] |
| val+test | TRAILING_OFF | 1 | 0 | 1 | 0; per speaker: nixon_resignation_1974 0; range [0, 0] | 0; per speaker: nixon_resignation_1974 0; range [0, 0] | 0; per speaker: nixon_resignation_1974 0; range [0, 0] | 0; per speaker: nixon_resignation_1974 0; range [0, 0] |

## D7/D8 both-edges matching beside index or overlap

| clip | split | type | level | both edges +/-0.20 s | index or overlap |
|---|---|---|---|---|---|
| eisenhower_farewell_1961__extra_L1A | val | WORD_REPETITION | 1 |  | False |
| eisenhower_farewell_1961__extra_L1B | val | SOUND_REPETITION | 1 |  | False |
| eisenhower_farewell_1961__extra_L1C | val | RHYME_PROLONGATION | 1 |  | False |
| eisenhower_farewell_1961__extra_L1D | val | ONSET_PROLONGATION | 1 |  | False |
| eisenhower_farewell_1961__extra_L1D | val | BLOCK | 1 |  | False |
| eisenhower_farewell_1961__extra_L2A | val | WORD_REPETITION | 2 |  | False |
| eisenhower_farewell_1961__extra_L2B | val | SOUND_REPETITION | 2 |  | False |
| eisenhower_farewell_1961__extra_L2C | val | RHYME_PROLONGATION | 2 |  | False |
| eisenhower_farewell_1961__extra_L2D | val | ONSET_PROLONGATION | 2 |  | False |
| eisenhower_farewell_1961__extra_L2D | val | BLOCK | 2 |  | False |
| eisenhower_farewell_1961__extra_L3A | val | WORD_REPETITION | 3 |  | False |
| eisenhower_farewell_1961__extra_L3B | val | SOUND_REPETITION | 3 |  | False |
| eisenhower_farewell_1961__extra_L3C | val | RHYME_PROLONGATION | 3 |  | False |
| eisenhower_farewell_1961__extra_L3D | val | ONSET_PROLONGATION | 3 |  | False |
| eisenhower_farewell_1961__extra_L3D | val | BLOCK | 3 |  | False |
| gwbush_911_2001__extra_L1A | train | WORD_REPETITION | 1 |  | False |
| gwbush_911_2001__extra_L1B | train | SOUND_REPETITION | 1 |  | False |
| gwbush_911_2001__extra_L1C | train | RHYME_PROLONGATION | 1 |  | False |
| gwbush_911_2001__extra_L1D | train | ONSET_PROLONGATION | 1 |  | False |
| gwbush_911_2001__extra_L1D | train | BLOCK | 1 |  | False |
| gwbush_911_2001__extra_L2A | train | WORD_REPETITION | 2 |  | False |
| gwbush_911_2001__extra_L2B | train | SOUND_REPETITION | 2 |  | False |
| gwbush_911_2001__extra_L2B | train | FLAT_FINAL_FALL | 2 |  | False |
| gwbush_911_2001__extra_L2C | train | RHYME_PROLONGATION | 2 |  | False |
| gwbush_911_2001__extra_L2D | train | ONSET_PROLONGATION | 2 |  | False |
| gwbush_911_2001__extra_L2D | train | BLOCK | 2 |  | False |
| gwbush_911_2001__extra_L3A | train | WORD_REPETITION | 3 |  | False |
| gwbush_911_2001__extra_L3B | train | SOUND_REPETITION | 3 |  | False |
| gwbush_911_2001__extra_L3B | train | FLAT_FINAL_FALL | 3 |  | False |
| gwbush_911_2001__extra_L3C | train | RHYME_PROLONGATION | 3 |  | False |
| gwbush_911_2001__extra_L3D | train | ONSET_PROLONGATION | 3 |  | False |
| gwbush_911_2001__extra_L3D | train | BLOCK | 3 |  | False |
| harris_uncsw_2021__extra_L1A | train | WORD_REPETITION | 1 |  | False |
| harris_uncsw_2021__extra_L1B | train | SOUND_REPETITION | 1 |  | False |
| harris_uncsw_2021__extra_L1C | train | RHYME_PROLONGATION | 1 |  | False |
| harris_uncsw_2021__extra_L1D | train | ONSET_PROLONGATION | 1 |  | False |
| harris_uncsw_2021__extra_L1D | train | BLOCK | 1 |  | False |
| harris_uncsw_2021__extra_L2A | train | WORD_REPETITION | 2 |  | False |
| harris_uncsw_2021__extra_L2B | train | SOUND_REPETITION | 2 |  | False |
| harris_uncsw_2021__extra_L2B | train | FLAT_FINAL_FALL | 2 |  | False |
| harris_uncsw_2021__extra_L2C | train | RHYME_PROLONGATION | 2 |  | False |
| harris_uncsw_2021__extra_L2D | train | ONSET_PROLONGATION | 2 |  | False |
| harris_uncsw_2021__extra_L2D | train | BLOCK | 2 |  | False |
| harris_uncsw_2021__extra_L3A | train | WORD_REPETITION | 3 |  | False |
| harris_uncsw_2021__extra_L3A | train | RISING_ENDING | 3 |  | False |
| harris_uncsw_2021__extra_L3B | train | SOUND_REPETITION | 3 |  | False |
| harris_uncsw_2021__extra_L3B | train | FLAT_FINAL_FALL | 3 |  | False |
| harris_uncsw_2021__extra_L3C | train | RHYME_PROLONGATION | 3 |  | False |
| harris_uncsw_2021__extra_L3D | train | ONSET_PROLONGATION | 3 |  | False |
| harris_uncsw_2021__extra_L3D | train | BLOCK | 3 |  | False |
| hclinton_tomorrow_2010__extra_L1A | train | WORD_REPETITION | 1 |  | False |
| hclinton_tomorrow_2010__extra_L1B | train | SOUND_REPETITION | 1 |  | False |
| hclinton_tomorrow_2010__extra_L1C | train | RHYME_PROLONGATION | 1 |  | False |
| hclinton_tomorrow_2010__extra_L1D | train | ONSET_PROLONGATION | 1 |  | False |
| hclinton_tomorrow_2010__extra_L1D | train | BLOCK | 1 |  | False |
| hclinton_tomorrow_2010__extra_L2A | train | WORD_REPETITION | 2 |  | False |
| hclinton_tomorrow_2010__extra_L2B | train | SOUND_REPETITION | 2 |  | False |
| hclinton_tomorrow_2010__extra_L2C | train | RHYME_PROLONGATION | 2 |  | False |
| hclinton_tomorrow_2010__extra_L2D | train | ONSET_PROLONGATION | 2 |  | False |
| hclinton_tomorrow_2010__extra_L2D | train | BLOCK | 2 |  | False |
| hclinton_tomorrow_2010__extra_L3A | train | WORD_REPETITION | 3 |  | False |
| hclinton_tomorrow_2010__extra_L3B | train | SOUND_REPETITION | 3 |  | False |
| hclinton_tomorrow_2010__extra_L3C | train | RHYME_PROLONGATION | 3 |  | False |
| hclinton_tomorrow_2010__extra_L3D | train | ONSET_PROLONGATION | 3 |  | False |
| hclinton_tomorrow_2010__extra_L3D | train | BLOCK | 3 |  | False |
| lbush_radio_2001__extra_L1A | val | WORD_REPETITION | 1 |  | False |
| lbush_radio_2001__extra_L1B | val | SOUND_REPETITION | 1 |  | False |
| lbush_radio_2001__extra_L1C | val | RHYME_PROLONGATION | 1 |  | False |
| lbush_radio_2001__extra_L1D | val | ONSET_PROLONGATION | 1 |  | False |
| lbush_radio_2001__extra_L2A | val | WORD_REPETITION | 2 |  | False |
| lbush_radio_2001__extra_L2B | val | SOUND_REPETITION | 2 |  | False |
| lbush_radio_2001__extra_L2C | val | RHYME_PROLONGATION | 2 |  | False |
| lbush_radio_2001__extra_L2D | val | ONSET_PROLONGATION | 2 |  | False |
| lbush_radio_2001__extra_L3A | val | WORD_REPETITION | 3 |  | False |
| lbush_radio_2001__extra_L3A | val | RISING_ENDING | 3 |  | False |
| lbush_radio_2001__extra_L3B | val | SOUND_REPETITION | 3 |  | False |
| lbush_radio_2001__extra_L3C | val | RHYME_PROLONGATION | 3 |  | False |
| lbush_radio_2001__extra_L3D | val | ONSET_PROLONGATION | 3 |  | False |
| mobama_weekly_2014__extra_L1A | test | WORD_REPETITION | 1 |  | False |
| mobama_weekly_2014__extra_L1B | test | SOUND_REPETITION | 1 |  | False |
| mobama_weekly_2014__extra_L1B | test | FLAT_FINAL_FALL | 1 |  | False |
| mobama_weekly_2014__extra_L1C | test | RHYME_PROLONGATION | 1 |  | False |
| mobama_weekly_2014__extra_L1D | test | ONSET_PROLONGATION | 1 |  | False |
| mobama_weekly_2014__extra_L1D | test | BLOCK | 1 |  | False |
| mobama_weekly_2014__extra_L2A | test | WORD_REPETITION | 2 |  | False |
| mobama_weekly_2014__extra_L2B | test | SOUND_REPETITION | 2 |  | False |
| mobama_weekly_2014__extra_L2B | test | FLAT_FINAL_FALL | 2 |  | False |
| mobama_weekly_2014__extra_L2C | test | RHYME_PROLONGATION | 2 |  | False |
| mobama_weekly_2014__extra_L2D | test | ONSET_PROLONGATION | 2 |  | False |
| mobama_weekly_2014__extra_L2D | test | BLOCK | 2 |  | False |
| mobama_weekly_2014__extra_L3A | test | WORD_REPETITION | 3 |  | False |
| mobama_weekly_2014__extra_L3A | test | RISING_ENDING | 3 |  | False |
| mobama_weekly_2014__extra_L3B | test | SOUND_REPETITION | 3 |  | False |
| mobama_weekly_2014__extra_L3B | test | FLAT_FINAL_FALL | 3 |  | False |
| mobama_weekly_2014__extra_L3C | test | RHYME_PROLONGATION | 3 |  | False |
| mobama_weekly_2014__extra_L3D | test | ONSET_PROLONGATION | 3 |  | False |
| mobama_weekly_2014__extra_L3D | test | BLOCK | 3 |  | False |
| nixon_resignation_1974__extra_L1A | test | WORD_REPETITION | 1 |  | False |
| nixon_resignation_1974__extra_L1B | test | SOUND_REPETITION | 1 |  | False |
| nixon_resignation_1974__extra_L1B | test | FLAT_FINAL_FALL | 1 |  | False |
| nixon_resignation_1974__extra_L1C | test | RHYME_PROLONGATION | 1 |  | False |
| nixon_resignation_1974__extra_L1D | test | ONSET_PROLONGATION | 1 |  | False |
| nixon_resignation_1974__extra_L1D | test | BLOCK | 1 |  | False |
| nixon_resignation_1974__extra_L2A | test | WORD_REPETITION | 2 |  | False |
| nixon_resignation_1974__extra_L2B | test | SOUND_REPETITION | 2 |  | False |
| nixon_resignation_1974__extra_L2B | test | FLAT_FINAL_FALL | 2 |  | False |
| nixon_resignation_1974__extra_L2C | test | RHYME_PROLONGATION | 2 |  | False |
| nixon_resignation_1974__extra_L2D | test | ONSET_PROLONGATION | 2 |  | False |
| nixon_resignation_1974__extra_L2D | test | BLOCK | 2 |  | False |
| nixon_resignation_1974__extra_L3A | test | WORD_REPETITION | 3 |  | False |
| nixon_resignation_1974__extra_L3A | test | RISING_ENDING | 3 |  | False |
| nixon_resignation_1974__extra_L3B | test | SOUND_REPETITION | 3 |  | False |
| nixon_resignation_1974__extra_L3B | test | FLAT_FINAL_FALL | 3 |  | False |
| nixon_resignation_1974__extra_L3C | test | RHYME_PROLONGATION | 3 |  | False |
| nixon_resignation_1974__extra_L3D | test | ONSET_PROLONGATION | 3 |  | False |
| nixon_resignation_1974__extra_L3D | test | BLOCK | 3 |  | False |
| obama_weekly_2009__extra_L1A | train | WORD_REPETITION | 1 |  | False |
| obama_weekly_2009__extra_L1B | train | SOUND_REPETITION | 1 |  | False |
| obama_weekly_2009__extra_L1B | train | FLAT_FINAL_FALL | 1 |  | False |
| obama_weekly_2009__extra_L1C | train | RHYME_PROLONGATION | 1 |  | False |
| obama_weekly_2009__extra_L1D | train | ONSET_PROLONGATION | 1 |  | False |
| obama_weekly_2009__extra_L1D | train | BLOCK | 1 |  | False |
| obama_weekly_2009__extra_L2A | train | WORD_REPETITION | 2 |  | False |
| obama_weekly_2009__extra_L2B | train | SOUND_REPETITION | 2 |  | False |
| obama_weekly_2009__extra_L2B | train | FLAT_FINAL_FALL | 2 |  | False |
| obama_weekly_2009__extra_L2C | train | RHYME_PROLONGATION | 2 |  | False |
| obama_weekly_2009__extra_L2D | train | ONSET_PROLONGATION | 2 |  | False |
| obama_weekly_2009__extra_L2D | train | BLOCK | 2 |  | False |
| obama_weekly_2009__extra_L3A | train | WORD_REPETITION | 3 |  | False |
| obama_weekly_2009__extra_L3B | train | SOUND_REPETITION | 3 |  | False |
| obama_weekly_2009__extra_L3B | train | FLAT_FINAL_FALL | 3 |  | False |
| obama_weekly_2009__extra_L3C | train | RHYME_PROLONGATION | 3 |  | False |
| obama_weekly_2009__extra_L3D | train | ONSET_PROLONGATION | 3 |  | False |
| obama_weekly_2009__extra_L3D | train | BLOCK | 3 |  | False |
| reagan_farewell_1989__extra_L1A | train | WORD_REPETITION | 1 |  | False |
| reagan_farewell_1989__extra_L1B | train | SOUND_REPETITION | 1 |  | False |
| reagan_farewell_1989__extra_L1B | train | FLAT_FINAL_FALL | 1 |  | False |
| reagan_farewell_1989__extra_L1C | train | RHYME_PROLONGATION | 1 |  | False |
| reagan_farewell_1989__extra_L1D | train | ONSET_PROLONGATION | 1 |  | False |
| reagan_farewell_1989__extra_L2A | train | WORD_REPETITION | 2 |  | False |
| reagan_farewell_1989__extra_L2B | train | SOUND_REPETITION | 2 |  | False |
| reagan_farewell_1989__extra_L2B | train | FLAT_FINAL_FALL | 2 |  | False |
| reagan_farewell_1989__extra_L2C | train | RHYME_PROLONGATION | 2 |  | False |
| reagan_farewell_1989__extra_L2D | train | ONSET_PROLONGATION | 2 |  | False |
| reagan_farewell_1989__extra_L3A | train | WORD_REPETITION | 3 |  | False |
| reagan_farewell_1989__extra_L3B | train | SOUND_REPETITION | 3 |  | False |
| reagan_farewell_1989__extra_L3B | train | FLAT_FINAL_FALL | 3 |  | False |
| reagan_farewell_1989__extra_L3C | train | RHYME_PROLONGATION | 3 |  | False |
| reagan_farewell_1989__extra_L3D | train | ONSET_PROLONGATION | 3 |  | False |

## Label groups and event truth counts

| clip | labels | event truths | word-by-word groups | eligible clips | detected clips | inserted silence truths |
|---|---|---|---|---|---|---|
| eisenhower_farewell_1961__extra_L1A | 4 | 2 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__extra_L1B | 4 | 3 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__extra_L1C | 3 | 6 | 1 | 1 | 0 | 4 |
| eisenhower_farewell_1961__extra_L1D | 3 | 3 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__extra_L2A | 4 | 2 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__extra_L2B | 4 | 3 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__extra_L2C | 3 | 6 | 1 | 1 | 0 | 4 |
| eisenhower_farewell_1961__extra_L2D | 3 | 3 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__extra_L3A | 4 | 2 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__extra_L3B | 4 | 3 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__extra_L3C | 3 | 6 | 1 | 1 | 0 | 4 |
| eisenhower_farewell_1961__extra_L3D | 3 | 3 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__single_L1A | 4 | 4 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__single_L1B | 4 | 4 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__single_L2A | 4 | 4 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__single_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__single_L3A | 4 | 4 | 0 | 0 | 0 | 0 |
| eisenhower_farewell_1961__single_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__extra_L1A | 4 | 3 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__extra_L1B | 4 | 3 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__extra_L1C | 3 | 9 | 1 | 1 | 0 | 7 |
| gwbush_911_2001__extra_L1D | 4 | 4 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__extra_L2A | 4 | 3 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__extra_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__extra_L2C | 3 | 9 | 1 | 1 | 0 | 7 |
| gwbush_911_2001__extra_L2D | 4 | 4 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__extra_L3A | 4 | 3 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__extra_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__extra_L3C | 3 | 9 | 1 | 1 | 0 | 7 |
| gwbush_911_2001__extra_L3D | 4 | 4 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__single_L1A | 4 | 4 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__single_L1B | 4 | 4 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__single_L2A | 4 | 4 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__single_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__single_L3A | 4 | 4 | 0 | 0 | 0 | 0 |
| gwbush_911_2001__single_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__extra_L1A | 4 | 2 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__extra_L1B | 3 | 2 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__extra_L1C | 3 | 9 | 1 | 1 | 0 | 7 |
| harris_uncsw_2021__extra_L1D | 4 | 4 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__extra_L2A | 4 | 2 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__extra_L2B | 3 | 3 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__extra_L2C | 3 | 9 | 1 | 1 | 0 | 7 |
| harris_uncsw_2021__extra_L2D | 4 | 4 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__extra_L3A | 4 | 3 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__extra_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__extra_L3C | 3 | 9 | 1 | 1 | 0 | 7 |
| harris_uncsw_2021__extra_L3D | 4 | 4 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__single_L1A | 4 | 4 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__single_L1B | 4 | 4 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__single_L2A | 4 | 4 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__single_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__single_L3A | 4 | 4 | 0 | 0 | 0 | 0 |
| harris_uncsw_2021__single_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__extra_L1A | 4 | 3 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__extra_L1B | 4 | 3 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__extra_L1C | 3 | 7 | 1 | 1 | 0 | 5 |
| hclinton_tomorrow_2010__extra_L1D | 4 | 3 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__extra_L2A | 4 | 3 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__extra_L2B | 4 | 3 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__extra_L2C | 3 | 7 | 1 | 1 | 0 | 5 |
| hclinton_tomorrow_2010__extra_L2D | 4 | 3 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__extra_L3A | 4 | 3 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__extra_L3B | 4 | 3 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__extra_L3C | 3 | 7 | 1 | 1 | 0 | 5 |
| hclinton_tomorrow_2010__extra_L3D | 4 | 3 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__single_L1A | 4 | 4 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__single_L1B | 4 | 4 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__single_L2A | 4 | 4 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__single_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__single_L3A | 4 | 4 | 0 | 0 | 0 | 0 |
| hclinton_tomorrow_2010__single_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__extra_L1A | 4 | 2 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__extra_L1B | 4 | 3 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__extra_L1C | 3 | 6 | 1 | 1 | 0 | 4 |
| lbush_radio_2001__extra_L1D | 3 | 3 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__extra_L2A | 4 | 2 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__extra_L2B | 4 | 3 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__extra_L2C | 3 | 6 | 1 | 1 | 0 | 4 |
| lbush_radio_2001__extra_L2D | 3 | 3 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__extra_L3A | 4 | 3 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__extra_L3B | 4 | 3 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__extra_L3C | 3 | 6 | 1 | 1 | 0 | 4 |
| lbush_radio_2001__extra_L3D | 3 | 3 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__single_L1A | 4 | 4 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__single_L1B | 4 | 4 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__single_L2A | 4 | 4 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__single_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__single_L3A | 4 | 4 | 0 | 0 | 0 | 0 |
| lbush_radio_2001__single_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__extra_L1A | 4 | 2 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__extra_L1B | 3 | 3 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__extra_L1C | 3 | 8 | 1 | 1 | 0 | 7 |
| mobama_weekly_2014__extra_L1D | 4 | 4 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__extra_L2A | 4 | 2 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__extra_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__extra_L2C | 3 | 8 | 1 | 1 | 0 | 7 |
| mobama_weekly_2014__extra_L2D | 4 | 4 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__extra_L3A | 4 | 3 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__extra_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__extra_L3C | 3 | 8 | 1 | 1 | 0 | 7 |
| mobama_weekly_2014__extra_L3D | 4 | 4 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__single_L1A | 4 | 4 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__single_L1B | 4 | 4 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__single_L2A | 4 | 4 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__single_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__single_L3A | 4 | 4 | 0 | 0 | 0 | 0 |
| mobama_weekly_2014__single_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__extra_L1A | 4 | 3 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__extra_L1B | 4 | 4 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__extra_L1C | 3 | 9 | 1 | 1 | 0 | 7 |
| nixon_resignation_1974__extra_L1D | 4 | 4 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__extra_L2A | 4 | 3 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__extra_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__extra_L2C | 3 | 9 | 1 | 1 | 0 | 7 |
| nixon_resignation_1974__extra_L2D | 4 | 4 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__extra_L3A | 4 | 4 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__extra_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__extra_L3C | 3 | 9 | 1 | 1 | 0 | 7 |
| nixon_resignation_1974__extra_L3D | 4 | 4 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__single_L1A | 4 | 4 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__single_L1B | 4 | 4 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__single_L2A | 4 | 4 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__single_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__single_L3A | 4 | 4 | 0 | 0 | 0 | 0 |
| nixon_resignation_1974__single_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__extra_L1A | 4 | 3 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__extra_L1B | 4 | 4 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__extra_L1C | 3 | 7 | 1 | 1 | 0 | 5 |
| obama_weekly_2009__extra_L1D | 4 | 3 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__extra_L2A | 4 | 3 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__extra_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__extra_L2C | 3 | 7 | 1 | 1 | 0 | 5 |
| obama_weekly_2009__extra_L2D | 4 | 3 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__extra_L3A | 4 | 3 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__extra_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__extra_L3C | 3 | 7 | 1 | 1 | 0 | 5 |
| obama_weekly_2009__extra_L3D | 4 | 3 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__single_L1A | 4 | 4 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__single_L1B | 4 | 4 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__single_L2A | 4 | 4 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__single_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__single_L3A | 4 | 4 | 0 | 0 | 0 | 0 |
| obama_weekly_2009__single_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__extra_L1A | 4 | 3 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__extra_L1B | 4 | 4 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__extra_L1C | 3 | 7 | 1 | 1 | 0 | 5 |
| reagan_farewell_1989__extra_L1D | 3 | 3 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__extra_L2A | 4 | 3 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__extra_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__extra_L2C | 3 | 7 | 1 | 1 | 0 | 5 |
| reagan_farewell_1989__extra_L2D | 3 | 3 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__extra_L3A | 4 | 3 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__extra_L3B | 4 | 4 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__extra_L3C | 3 | 7 | 1 | 1 | 0 | 5 |
| reagan_farewell_1989__extra_L3D | 3 | 3 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__single_L1A | 4 | 4 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__single_L1B | 4 | 4 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__single_L2A | 4 | 4 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__single_L2B | 4 | 4 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__single_L3A | 4 | 4 | 0 | 0 | 0 | 0 |
| reagan_farewell_1989__single_L3B | 4 | 4 | 0 | 0 | 0 | 0 |

WORD_BY_WORD group recovery counts each eligible clip once (any labelled boundary detected); boundary localisation is reported separately. This synthetic-only family does not select h.

## Recovery of the synthetic edit: detection versus magnitude

core8:

| type | level | magnitude | train k/n | val k/n | test k/n | expected (R1) |
|---|---|---|---|---|---|---|
| RUSH | 1 | 1.2 | 2/5 (95% Wilson [0.118, 0.769]) | 0/2 (95% Wilson [0, 0.658]) | 2/2 (95% Wilson [0.342, 1]) | marginal: detection near or below 50 %; clip score >= 90 |
| RUSH | 2 | 1.45 | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| RUSH | 3 | 1.9 | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| DRAG | 1 | 1.2 | 0/5 (95% Wilson [0, 0.434]) | 0/2 (95% Wilson [0, 0.658]) | 0/2 (95% Wilson [0, 0.658]) | marginal: detection near or below 50 %; clip score >= 90 |
| DRAG | 2 | 1.45 | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| DRAG | 3 | 1.9 | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| PAUSE_DROPPED | 1 | 0.4 | 4/5 (95% Wilson [0.376, 0.964]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | marginal: detection near or below 50 %; clip score >= 90 |
| PAUSE_DROPPED | 2 | 0.2 | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| PAUSE_DROPPED | 3 | 0 | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| PAUSE_INTRUSIVE | 1 | 0.35 | 5/5 (95% Wilson [0.566, 1]) | 1/2 (95% Wilson [0.0945, 0.905]) | 1/2 (95% Wilson [0.0945, 0.905]) | marginal: detection near or below 50 %; clip score >= 90 |
| PAUSE_INTRUSIVE | 2 | 0.6 | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| PAUSE_INTRUSIVE | 3 | 1.2 | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| MONOTONE | 1 | 0.5 | 0/5 (95% Wilson [0, 0.434]) | 0/2 (95% Wilson [0, 0.658]) | 0/2 (95% Wilson [0, 0.658]) | marginal: detection near or below 50 %; clip score >= 90 |
| MONOTONE | 2 | 0.25 | 4/5 (95% Wilson [0.376, 0.964]) | 2/2 (95% Wilson [0.342, 1]) | 1/2 (95% Wilson [0.0945, 0.905]) | flagged |
| MONOTONE | 3 | 0 | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 1/2 (95% Wilson [0.0945, 0.905]) | flagged |
| DEEMPHASIS | 1 | 0.5 | 0/5 (95% Wilson [0, 0.434]) | 0/2 (95% Wilson [0, 0.658]) | 0/2 (95% Wilson [0, 0.658]) | marginal: detection near or below 50 %; clip score >= 90 |
| DEEMPHASIS | 2 | 0.75 | 3/5 (95% Wilson [0.231, 0.882]) | 2/2 (95% Wilson [0.342, 1]) | 1/2 (95% Wilson [0.0945, 0.905]) | flagged |
| DEEMPHASIS | 3 | 1 | 4/5 (95% Wilson [0.376, 0.964]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| FADE | 1 | 4 | 0/5 (95% Wilson [0, 0.434]) | 0/2 (95% Wilson [0, 0.658]) | 0/2 (95% Wilson [0, 0.658]) | marginal: detection near or below 50 %; clip score >= 90 |
| FADE | 2 | 8 | 5/5 (95% Wilson [0.566, 1]) | 0/2 (95% Wilson [0, 0.658]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| FADE | 3 | 14 | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| MUMBLE | 1 | 0.3 | 0/5 (95% Wilson [0, 0.434]) | 0/2 (95% Wilson [0, 0.658]) | 0/2 (95% Wilson [0, 0.658]) | marginal: detection near or below 50 %; clip score >= 90 |
| MUMBLE | 2 | 0.6 | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| MUMBLE | 3 | 1 | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |

lab_passed:

| type | level | magnitude | train k/n | val k/n | test k/n | expected (R1) |
|---|---|---|---|---|---|---|
| NATURAL_RUSH | 1 | {'speech_rate': 1.13, 'pause_kept_fraction': 0.6} | 0/5 (95% Wilson [0, 0.434]) | 0/2 (95% Wilson [0, 0.658]) | 0/2 (95% Wilson [0, 0.658]) | marginal: detection near or below 50 %; clip score >= 90 |
| NATURAL_RUSH | 2 | {'speech_rate': 1.15, 'pause_kept_fraction': 0.3} | 1/5 (95% Wilson [0.0362, 0.624]) | 0/2 (95% Wilson [0, 0.658]) | 0/2 (95% Wilson [0, 0.658]) | flagged |
| NATURAL_RUSH | 3 | {'speech_rate': 1.18, 'pause_kept_fraction': 0.0} | 1/5 (95% Wilson [0.0362, 0.624]) | 1/2 (95% Wilson [0.0945, 0.905]) | 1/2 (95% Wilson [0.0945, 0.905]) | flagged |

synthetic_only (unvalidated):

| type | level | magnitude | train k/n | val k/n | test k/n | expected (R1) |
|---|---|---|---|---|---|---|
| HESITATION | 1 | {'word_duration_factor': 1.2, 'silence_s': 0.2} | 0/5 (95% Wilson [0, 0.434]) | 0/2 (95% Wilson [0, 0.658]) | 0/2 (95% Wilson [0, 0.658]) | marginal: detection near or below 50 %; clip score >= 90 |
| HESITATION | 2 | {'word_duration_factor': 1.5, 'silence_s': 0.5} | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| HESITATION | 3 | {'word_duration_factor': 1.8, 'silence_s': 1.0} | 5/5 (95% Wilson [0.566, 1]) | 2/2 (95% Wilson [0.342, 1]) | 2/2 (95% Wilson [0.342, 1]) | flagged |
| WORD_BY_WORD | 1 | {'silence_s': 0.15, 'every_words': 1} | 0/29 (95% Wilson [0, 0.117]) | 0/8 (95% Wilson [0, 0.324]) | 0/14 (95% Wilson [0, 0.215]) | marginal: detection near or below 50 %; clip score >= 90 |
| WORD_BY_WORD | 2 | {'silence_s': 0.225, 'every_words': 1} | 0/29 (95% Wilson [0, 0.117]) | 0/8 (95% Wilson [0, 0.324]) | 0/14 (95% Wilson [0, 0.215]) | flagged |
| WORD_BY_WORD | 3 | {'silence_s': 0.3, 'every_words': 1} | 0/29 (95% Wilson [0, 0.117]) | 0/8 (95% Wilson [0, 0.324]) | 0/14 (95% Wilson [0, 0.215]) | flagged |
| UNEVEN_TEMPO | 1 | {'max_duration_deviation': 0.15} | no detector (5) | no detector (2) | no detector (2) | marginal: detection near or below 50 %; clip score >= 90 |
| UNEVEN_TEMPO | 2 | {'max_duration_deviation': 0.3} | no detector (5) | no detector (2) | no detector (2) | flagged |
| UNEVEN_TEMPO | 3 | {'max_duration_deviation': 0.45} | no detector (5) | no detector (2) | no detector (2) | flagged |
| WORD_REPETITION | 1 | {'first_token_duration_factor': 1.3, 'silence_s': 0.1, 'inserted_copies': 1} | no detector (5) | no detector (2) | no detector (2) | marginal: detection near or below 50 %; clip score >= 90 |
| WORD_REPETITION | 2 | {'first_token_duration_factor': 1.6, 'silence_s': 0.225, 'inserted_copies': 1} | no detector (5) | no detector (2) | no detector (2) | flagged |
| WORD_REPETITION | 3 | {'first_token_duration_factor': 1.9, 'silence_s': 0.35, 'inserted_copies': 1} | no detector (5) | no detector (2) | no detector (2) | flagged |
| SOUND_REPETITION | 1 | {'inserted_copies': 2, 'silence_s': 0.1} | no detector (5) | no detector (2) | no detector (2) | marginal: detection near or below 50 %; clip score >= 90 |
| SOUND_REPETITION | 2 | {'inserted_copies': 3, 'silence_s': 0.1} | no detector (5) | no detector (2) | no detector (2) | flagged |
| SOUND_REPETITION | 3 | {'inserted_copies': 4, 'silence_s': 0.1} | no detector (5) | no detector (2) | no detector (2) | flagged |
| RHYME_PROLONGATION | 1 | {'added_duration_s': 0.18} | no detector (5) | no detector (2) | no detector (2) | marginal: detection near or below 50 %; clip score >= 90 |
| RHYME_PROLONGATION | 2 | {'added_duration_s': 0.36} | no detector (5) | no detector (2) | no detector (2) | flagged |
| RHYME_PROLONGATION | 3 | {'added_duration_s': 0.54} | no detector (5) | no detector (2) | no detector (2) | flagged |
| ONSET_PROLONGATION | 1 | {'onset_target_s': 0.35} | no detector (5) | no detector (2) | no detector (2) | marginal: detection near or below 50 %; clip score >= 90 |
| ONSET_PROLONGATION | 2 | {'onset_target_s': 0.65} | no detector (5) | no detector (2) | no detector (2) | flagged |
| ONSET_PROLONGATION | 3 | {'onset_target_s': 1.0} | no detector (5) | no detector (2) | no detector (2) | flagged |
| BLOCK | 1 | {'silence_s': 0.5} | no detector (4) | no detector (1) | no detector (2) | marginal: detection near or below 50 %; clip score >= 90 |
| BLOCK | 2 | {'silence_s': 1.25} | no detector (4) | no detector (1) | no detector (2) | flagged |
| BLOCK | 3 | {'silence_s': 2.0} | no detector (4) | no detector (1) | no detector (2) | flagged |
| LOW_EFFORT | 1 | {'attenuation_db': 3.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 0.5} | 0/4 (95% Wilson [0, 0.49]) |  | 0/1 (95% Wilson [0, 0.793]) | marginal: detection near or below 50 %; clip score >= 90 |
| LOW_EFFORT | 2 | {'attenuation_db': 6.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 1.0} | 2/4 (95% Wilson [0.15, 0.85]) |  | 1/1 (95% Wilson [0.207, 1]) | flagged |
| LOW_EFFORT | 3 | {'attenuation_db': 9.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 1.5} | 3/4 (95% Wilson [0.301, 0.954]) |  | 1/1 (95% Wilson [0.207, 1]) | flagged |
| TRAILING_OFF | 1 | {'final_attenuation_db': 4.0, 'alpha_drop_per_db': 0.55} | 0/5 (95% Wilson [0, 0.434]) | 0/2 (95% Wilson [0, 0.658]) | 0/1 (95% Wilson [0, 0.793]) | marginal: detection near or below 50 %; clip score >= 90 |
| TRAILING_OFF | 2 | {'final_attenuation_db': 8.0, 'alpha_drop_per_db': 0.55} | 0/5 (95% Wilson [0, 0.434]) | 0/2 (95% Wilson [0, 0.658]) | 0/1 (95% Wilson [0, 0.793]) | flagged |
| TRAILING_OFF | 3 | {'final_attenuation_db': 12.0, 'alpha_drop_per_db': 0.55} | 4/5 (95% Wilson [0.376, 0.964]) | 0/2 (95% Wilson [0, 0.658]) | 1/1 (95% Wilson [0.207, 1]) | flagged |
| MISPLACED_EMPHASIS | 1 | {'function_duration_factor': 1.1, 'function_pitch_st': 2.0, 'function_gain_db': 2.0, 'stressed_removal_strength': 0.3} | 0/4 (95% Wilson [0, 0.49]) | 0/2 (95% Wilson [0, 0.658]) | 0/1 (95% Wilson [0, 0.793]) | marginal: detection near or below 50 %; clip score >= 90 |
| MISPLACED_EMPHASIS | 2 | {'function_duration_factor': 1.2, 'function_pitch_st': 4.0, 'function_gain_db': 4.0, 'stressed_removal_strength': 0.6} | 0/4 (95% Wilson [0, 0.49]) | 0/2 (95% Wilson [0, 0.658]) | 0/2 (95% Wilson [0, 0.658]) | flagged |
| MISPLACED_EMPHASIS | 3 | {'function_duration_factor': 1.3, 'function_pitch_st': 6.0, 'function_gain_db': 6.0, 'stressed_removal_strength': 0.9} | 1/5 (95% Wilson [0.0362, 0.624]) | 1/2 (95% Wilson [0.0945, 0.905]) | 1/2 (95% Wilson [0.0945, 0.905]) | flagged |
| RISING_ENDING | 1 | {'rise_st': 2.0} |  |  |  | marginal: detection near or below 50 %; clip score >= 90 |
| RISING_ENDING | 2 | {'rise_st': 4.0} |  |  |  | flagged |
| RISING_ENDING | 3 | {'rise_st': 6.0} | no detector (1) | no detector (1) | no detector (2) | flagged |
| FLAT_FINAL_FALL | 1 | {'strength': 0.333} | no detector (2) |  | no detector (2) | marginal: detection near or below 50 %; clip score >= 90 |
| FLAT_FINAL_FALL | 2 | {'strength': 0.667} | no detector (4) |  | no detector (2) | flagged |
| FLAT_FINAL_FALL | 3 | {'strength': 1.0} | no detector (4) |  | no detector (2) | flagged |
| REPEATED_CONTOUR | 1 | {'contour_strength': 0.333} | no detector (3) | no detector (1) | no detector (2) | no detector |
| REPEATED_CONTOUR | 2 | {'contour_strength': 0.667} | no detector (3) | no detector (1) | no detector (2) | no detector |
| REPEATED_CONTOUR | 3 | {'contour_strength': 1.0} | no detector (3) | no detector (1) | no detector (2) | no detector |

Excluded shortfall stratum (not truth or h-selection positives):

| split | type | level | excluded events |
|---|---|---|---|
| test | LOW_EFFORT | 1 | 1 |
| test | LOW_EFFORT | 2 | 1 |
| test | LOW_EFFORT | 3 | 1 |
| test | RISING_ENDING | 1 | 2 |
| test | RISING_ENDING | 2 | 2 |
| test | TRAILING_OFF | 1 | 1 |
| test | TRAILING_OFF | 2 | 1 |
| test | TRAILING_OFF | 3 | 1 |
| train | FLAT_FINAL_FALL | 1 | 3 |
| train | FLAT_FINAL_FALL | 2 | 1 |
| train | FLAT_FINAL_FALL | 3 | 1 |
| train | LOW_EFFORT | 1 | 1 |
| train | LOW_EFFORT | 2 | 1 |
| train | LOW_EFFORT | 3 | 1 |
| train | REPEATED_CONTOUR | 1 | 2 |
| train | REPEATED_CONTOUR | 2 | 2 |
| train | REPEATED_CONTOUR | 3 | 2 |
| train | RISING_ENDING | 1 | 5 |
| train | RISING_ENDING | 2 | 5 |
| train | RISING_ENDING | 3 | 4 |
| val | FLAT_FINAL_FALL | 1 | 2 |
| val | FLAT_FINAL_FALL | 2 | 2 |
| val | FLAT_FINAL_FALL | 3 | 2 |
| val | LOW_EFFORT | 1 | 2 |
| val | LOW_EFFORT | 2 | 2 |
| val | LOW_EFFORT | 3 | 2 |
| val | RISING_ENDING | 1 | 2 |
| val | RISING_ENDING | 2 | 2 |
| val | RISING_ENDING | 3 | 1 |

Detection by realised magnitude (recipe units):

| tier | split | speech | type | nominal level | realised value | unit | detected |
|---|---|---|---|---|---|---|---|
| core8 | val | eisenhower_farewell_1961 | RUSH | 1 | -0.182 | ln | False |
| core8 | val | eisenhower_farewell_1961 | PAUSE_DROPPED | 1 | -0.342 | s | True |
| core8 | val | eisenhower_farewell_1961 | MONOTONE | 1 | -5.25 | st | False |
| core8 | val | eisenhower_farewell_1961 | FADE | 1 | -2.58 | dB | False |
| core8 | val | eisenhower_farewell_1961 | DRAG | 1 | 0.182 | ln | False |
| core8 | val | eisenhower_farewell_1961 | PAUSE_INTRUSIVE | 1 | 0.35 | s | False |
| core8 | val | eisenhower_farewell_1961 | DEEMPHASIS | 1 | -0.531 | p | False |
| core8 | val | eisenhower_farewell_1961 | MUMBLE | 1 | -0.313 | ln | False |
| core8 | val | eisenhower_farewell_1961 | RUSH | 2 | -0.372 | ln | True |
| core8 | val | eisenhower_farewell_1961 | PAUSE_DROPPED | 2 | -0.52 | s | True |
| core8 | val | eisenhower_farewell_1961 | MONOTONE | 2 | -9.28 | st | True |
| core8 | val | eisenhower_farewell_1961 | FADE | 2 | -4.35 | dB | False |
| core8 | val | eisenhower_farewell_1961 | DRAG | 2 | 0.372 | ln | True |
| core8 | val | eisenhower_farewell_1961 | PAUSE_INTRUSIVE | 2 | 0.6 | s | True |
| core8 | val | eisenhower_farewell_1961 | DEEMPHASIS | 2 | -1.28 | p | True |
| core8 | val | eisenhower_farewell_1961 | MUMBLE | 2 | -0.618 | ln | True |
| core8 | val | eisenhower_farewell_1961 | RUSH | 3 | -0.642 | ln | True |
| core8 | val | eisenhower_farewell_1961 | PAUSE_DROPPED | 3 | -1.65 | s | True |
| core8 | val | eisenhower_farewell_1961 | MONOTONE | 3 | -10.8 | st | True |
| core8 | val | eisenhower_farewell_1961 | FADE | 3 | -8.87 | dB | True |
| core8 | val | eisenhower_farewell_1961 | DRAG | 3 | 0.642 | ln | True |
| core8 | val | eisenhower_farewell_1961 | PAUSE_INTRUSIVE | 3 | 1.2 | s | True |
| core8 | val | eisenhower_farewell_1961 | DEEMPHASIS | 3 | -1.8 | p | True |
| core8 | val | eisenhower_farewell_1961 | MUMBLE | 3 | -0.821 | ln | True |
| core8 | train | gwbush_911_2001 | RUSH | 1 | -0.182 | ln | False |
| core8 | train | gwbush_911_2001 | PAUSE_DROPPED | 1 | -0.45 | s | True |
| core8 | train | gwbush_911_2001 | MONOTONE | 1 | -2.03 | st | False |
| core8 | train | gwbush_911_2001 | FADE | 1 | -3.32 | dB | False |
| core8 | train | gwbush_911_2001 | DRAG | 1 | 0.182 | ln | False |
| core8 | train | gwbush_911_2001 | PAUSE_INTRUSIVE | 1 | 0.35 | s | True |
| core8 | train | gwbush_911_2001 | DEEMPHASIS | 1 | -0.529 | p | False |
| core8 | train | gwbush_911_2001 | MUMBLE | 1 | -0.357 | ln | False |
| core8 | train | gwbush_911_2001 | RUSH | 2 | -0.372 | ln | True |
| core8 | train | gwbush_911_2001 | PAUSE_DROPPED | 2 | -1.03 | s | True |
| core8 | train | gwbush_911_2001 | MONOTONE | 2 | -2.22 | st | True |
| core8 | train | gwbush_911_2001 | FADE | 2 | -4.52 | dB | True |
| core8 | train | gwbush_911_2001 | DRAG | 2 | 0.372 | ln | True |
| core8 | train | gwbush_911_2001 | PAUSE_INTRUSIVE | 2 | 0.6 | s | True |
| core8 | train | gwbush_911_2001 | DEEMPHASIS | 2 | -1.19 | p | True |
| core8 | train | gwbush_911_2001 | MUMBLE | 2 | -0.737 | ln | True |
| core8 | train | gwbush_911_2001 | RUSH | 3 | -0.642 | ln | True |
| core8 | train | gwbush_911_2001 | PAUSE_DROPPED | 3 | -0.58 | s | True |
| core8 | train | gwbush_911_2001 | MONOTONE | 3 | -4.69 | st | True |
| core8 | train | gwbush_911_2001 | FADE | 3 | -11.5 | dB | True |
| core8 | train | gwbush_911_2001 | DRAG | 3 | 0.642 | ln | True |
| core8 | train | gwbush_911_2001 | PAUSE_INTRUSIVE | 3 | 1.2 | s | True |
| core8 | train | gwbush_911_2001 | DEEMPHASIS | 3 | -0.921 | p | False |
| core8 | train | gwbush_911_2001 | MUMBLE | 3 | -0.896 | ln | True |
| core8 | train | harris_uncsw_2021 | RUSH | 1 | -0.182 | ln | False |
| core8 | train | harris_uncsw_2021 | PAUSE_DROPPED | 1 | -0.582 | s | True |
| core8 | train | harris_uncsw_2021 | MONOTONE | 1 | -1.31 | st | False |
| core8 | train | harris_uncsw_2021 | FADE | 1 | -2.77 | dB | False |
| core8 | train | harris_uncsw_2021 | DRAG | 1 | 0.182 | ln | False |
| core8 | train | harris_uncsw_2021 | PAUSE_INTRUSIVE | 1 | 0.35 | s | True |
| core8 | train | harris_uncsw_2021 | DEEMPHASIS | 1 | -0.816 | p | False |
| core8 | train | harris_uncsw_2021 | MUMBLE | 1 | -0.348 | ln | False |
| core8 | train | harris_uncsw_2021 | RUSH | 2 | -0.372 | ln | True |
| core8 | train | harris_uncsw_2021 | PAUSE_DROPPED | 2 | -1 | s | True |
| core8 | train | harris_uncsw_2021 | MONOTONE | 2 | -5.2 | st | True |
| core8 | train | harris_uncsw_2021 | FADE | 2 | -4.84 | dB | True |
| core8 | train | harris_uncsw_2021 | DRAG | 2 | 0.372 | ln | True |
| core8 | train | harris_uncsw_2021 | PAUSE_INTRUSIVE | 2 | 0.6 | s | True |
| core8 | train | harris_uncsw_2021 | DEEMPHASIS | 2 | -1.21 | p | True |
| core8 | train | harris_uncsw_2021 | MUMBLE | 2 | -0.673 | ln | True |
| core8 | train | harris_uncsw_2021 | RUSH | 3 | -0.642 | ln | True |
| core8 | train | harris_uncsw_2021 | PAUSE_DROPPED | 3 | -1.19 | s | True |
| core8 | train | harris_uncsw_2021 | MONOTONE | 3 | -4.83 | st | True |
| core8 | train | harris_uncsw_2021 | FADE | 3 | -9.25 | dB | True |
| core8 | train | harris_uncsw_2021 | DRAG | 3 | 0.642 | ln | True |
| core8 | train | harris_uncsw_2021 | PAUSE_INTRUSIVE | 3 | 1.2 | s | True |
| core8 | train | harris_uncsw_2021 | DEEMPHASIS | 3 | -1.18 | p | True |
| core8 | train | harris_uncsw_2021 | MUMBLE | 3 | -0.813 | ln | True |
| core8 | train | hclinton_tomorrow_2010 | RUSH | 1 | -0.182 | ln | True |
| core8 | train | hclinton_tomorrow_2010 | PAUSE_DROPPED | 1 | -0.684 | s | True |
| core8 | train | hclinton_tomorrow_2010 | MONOTONE | 1 | -2.53 | st | False |
| core8 | train | hclinton_tomorrow_2010 | FADE | 1 | -3.08 | dB | False |
| core8 | train | hclinton_tomorrow_2010 | DRAG | 1 | 0.182 | ln | False |
| core8 | train | hclinton_tomorrow_2010 | PAUSE_INTRUSIVE | 1 | 0.35 | s | True |
| core8 | train | hclinton_tomorrow_2010 | DEEMPHASIS | 1 | -0.711 | p | False |
| core8 | train | hclinton_tomorrow_2010 | MUMBLE | 1 | -0.341 | ln | False |
| core8 | train | hclinton_tomorrow_2010 | RUSH | 2 | -0.372 | ln | True |
| core8 | train | hclinton_tomorrow_2010 | PAUSE_DROPPED | 2 | -0.44 | s | True |
| core8 | train | hclinton_tomorrow_2010 | MONOTONE | 2 | -4.85 | st | True |
| core8 | train | hclinton_tomorrow_2010 | FADE | 2 | -6.35 | dB | True |
| core8 | train | hclinton_tomorrow_2010 | DRAG | 2 | 0.372 | ln | True |
| core8 | train | hclinton_tomorrow_2010 | PAUSE_INTRUSIVE | 2 | 0.6 | s | True |
| core8 | train | hclinton_tomorrow_2010 | DEEMPHASIS | 2 | -1.24 | p | True |
| core8 | train | hclinton_tomorrow_2010 | MUMBLE | 2 | -0.675 | ln | True |
| core8 | train | hclinton_tomorrow_2010 | RUSH | 3 | -0.642 | ln | True |
| core8 | train | hclinton_tomorrow_2010 | PAUSE_DROPPED | 3 | -1.08 | s | True |
| core8 | train | hclinton_tomorrow_2010 | MONOTONE | 3 | -4.83 | st | True |
| core8 | train | hclinton_tomorrow_2010 | FADE | 3 | -10.5 | dB | True |
| core8 | train | hclinton_tomorrow_2010 | DRAG | 3 | 0.642 | ln | True |
| core8 | train | hclinton_tomorrow_2010 | PAUSE_INTRUSIVE | 3 | 1.2 | s | True |
| core8 | train | hclinton_tomorrow_2010 | DEEMPHASIS | 3 | -1.77 | p | True |
| core8 | train | hclinton_tomorrow_2010 | MUMBLE | 3 | -0.81 | ln | True |
| core8 | val | lbush_radio_2001 | RUSH | 1 | -0.182 | ln | False |
| core8 | val | lbush_radio_2001 | PAUSE_DROPPED | 1 | -0.456 | s | True |
| core8 | val | lbush_radio_2001 | MONOTONE | 1 | -3.22 | st | False |
| core8 | val | lbush_radio_2001 | FADE | 1 | -2.5 | dB | False |
| core8 | val | lbush_radio_2001 | DRAG | 1 | 0.182 | ln | False |
| core8 | val | lbush_radio_2001 | PAUSE_INTRUSIVE | 1 | 0.35 | s | True |
| core8 | val | lbush_radio_2001 | DEEMPHASIS | 1 | -0.998 | p | False |
| core8 | val | lbush_radio_2001 | MUMBLE | 1 | -0.276 | ln | False |
| core8 | val | lbush_radio_2001 | RUSH | 2 | -0.372 | ln | True |
| core8 | val | lbush_radio_2001 | PAUSE_DROPPED | 2 | -0.728 | s | True |
| core8 | val | lbush_radio_2001 | MONOTONE | 2 | -5.28 | st | True |
| core8 | val | lbush_radio_2001 | FADE | 2 | -4.63 | dB | False |
| core8 | val | lbush_radio_2001 | DRAG | 2 | 0.372 | ln | True |
| core8 | val | lbush_radio_2001 | PAUSE_INTRUSIVE | 2 | 0.6 | s | True |
| core8 | val | lbush_radio_2001 | DEEMPHASIS | 2 | -1.41 | p | True |
| core8 | val | lbush_radio_2001 | MUMBLE | 2 | -0.599 | ln | True |
| core8 | val | lbush_radio_2001 | RUSH | 3 | -0.642 | ln | True |
| core8 | val | lbush_radio_2001 | PAUSE_DROPPED | 3 | -0.63 | s | True |
| core8 | val | lbush_radio_2001 | MONOTONE | 3 | -7.76 | st | True |
| core8 | val | lbush_radio_2001 | FADE | 3 | -8.69 | dB | True |
| core8 | val | lbush_radio_2001 | DRAG | 3 | 0.642 | ln | True |
| core8 | val | lbush_radio_2001 | PAUSE_INTRUSIVE | 3 | 1.2 | s | True |
| core8 | val | lbush_radio_2001 | DEEMPHASIS | 3 | -1.58 | p | True |
| core8 | val | lbush_radio_2001 | MUMBLE | 3 | -0.673 | ln | True |
| core8 | test | mobama_weekly_2014 | RUSH | 1 | -0.182 | ln | True |
| core8 | test | mobama_weekly_2014 | PAUSE_DROPPED | 1 | -0.384 | s | True |
| core8 | test | mobama_weekly_2014 | MONOTONE | 1 | -2.16 | st | False |
| core8 | test | mobama_weekly_2014 | FADE | 1 | -3.26 | dB | False |
| core8 | test | mobama_weekly_2014 | DRAG | 1 | 0.182 | ln | False |
| core8 | test | mobama_weekly_2014 | PAUSE_INTRUSIVE | 1 | 0.35 | s | False |
| core8 | test | mobama_weekly_2014 | DEEMPHASIS | 1 | -1.01 | p | False |
| core8 | test | mobama_weekly_2014 | MUMBLE | 1 | -0.339 | ln | False |
| core8 | test | mobama_weekly_2014 | RUSH | 2 | -0.372 | ln | True |
| core8 | test | mobama_weekly_2014 | PAUSE_DROPPED | 2 | -0.456 | s | True |
| core8 | test | mobama_weekly_2014 | MONOTONE | 2 | -3.8 | st | False |
| core8 | test | mobama_weekly_2014 | FADE | 2 | -6.45 | dB | True |
| core8 | test | mobama_weekly_2014 | DRAG | 2 | 0.372 | ln | True |
| core8 | test | mobama_weekly_2014 | PAUSE_INTRUSIVE | 2 | 0.6 | s | True |
| core8 | test | mobama_weekly_2014 | DEEMPHASIS | 2 | -1.28 | p | True |
| core8 | test | mobama_weekly_2014 | MUMBLE | 2 | -0.674 | ln | True |
| core8 | test | mobama_weekly_2014 | RUSH | 3 | -0.642 | ln | True |
| core8 | test | mobama_weekly_2014 | PAUSE_DROPPED | 3 | -0.58 | s | True |
| core8 | test | mobama_weekly_2014 | MONOTONE | 3 | -7.57 | st | False |
| core8 | test | mobama_weekly_2014 | FADE | 3 | -10.1 | dB | True |
| core8 | test | mobama_weekly_2014 | DRAG | 3 | 0.642 | ln | True |
| core8 | test | mobama_weekly_2014 | PAUSE_INTRUSIVE | 3 | 1.2 | s | True |
| core8 | test | mobama_weekly_2014 | DEEMPHASIS | 3 | -1.35 | p | True |
| core8 | test | mobama_weekly_2014 | MUMBLE | 3 | -0.835 | ln | True |
| core8 | test | nixon_resignation_1974 | RUSH | 1 | -0.182 | ln | True |
| core8 | test | nixon_resignation_1974 | PAUSE_DROPPED | 1 | -0.708 | s | True |
| core8 | test | nixon_resignation_1974 | MONOTONE | 1 | -2.62 | st | False |
| core8 | test | nixon_resignation_1974 | FADE | 1 | -2.93 | dB | False |
| core8 | test | nixon_resignation_1974 | DRAG | 1 | 0.182 | ln | False |
| core8 | test | nixon_resignation_1974 | PAUSE_INTRUSIVE | 1 | 0.35 | s | True |
| core8 | test | nixon_resignation_1974 | DEEMPHASIS | 1 | -0.638 | p | False |
| core8 | test | nixon_resignation_1974 | MUMBLE | 1 | -0.349 | ln | False |
| core8 | test | nixon_resignation_1974 | RUSH | 2 | -0.372 | ln | True |
| core8 | test | nixon_resignation_1974 | PAUSE_DROPPED | 2 | -0.568 | s | True |
| core8 | test | nixon_resignation_1974 | MONOTONE | 2 | -3.68 | st | True |
| core8 | test | nixon_resignation_1974 | FADE | 2 | -6.56 | dB | True |
| core8 | test | nixon_resignation_1974 | DRAG | 2 | 0.372 | ln | True |
| core8 | test | nixon_resignation_1974 | PAUSE_INTRUSIVE | 2 | 0.6 | s | True |
| core8 | test | nixon_resignation_1974 | DEEMPHASIS | 2 | -0.957 | p | False |
| core8 | test | nixon_resignation_1974 | MUMBLE | 2 | -0.662 | ln | True |
| core8 | test | nixon_resignation_1974 | RUSH | 3 | -0.642 | ln | True |
| core8 | test | nixon_resignation_1974 | PAUSE_DROPPED | 3 | -1.11 | s | True |
| core8 | test | nixon_resignation_1974 | MONOTONE | 3 | -6.9 | st | True |
| core8 | test | nixon_resignation_1974 | FADE | 3 | -7.05 | dB | True |
| core8 | test | nixon_resignation_1974 | DRAG | 3 | 0.642 | ln | True |
| core8 | test | nixon_resignation_1974 | PAUSE_INTRUSIVE | 3 | 1.2 | s | True |
| core8 | test | nixon_resignation_1974 | DEEMPHASIS | 3 | -1.51 | p | True |
| core8 | test | nixon_resignation_1974 | MUMBLE | 3 | -0.917 | ln | True |
| core8 | train | obama_weekly_2009 | RUSH | 1 | -0.182 | ln | False |
| core8 | train | obama_weekly_2009 | PAUSE_DROPPED | 1 | -0.306 | s | False |
| core8 | train | obama_weekly_2009 | MONOTONE | 1 | -3.81 | st | False |
| core8 | train | obama_weekly_2009 | FADE | 1 | -2.33 | dB | False |
| core8 | train | obama_weekly_2009 | DRAG | 1 | 0.182 | ln | False |
| core8 | train | obama_weekly_2009 | PAUSE_INTRUSIVE | 1 | 0.35 | s | True |
| core8 | train | obama_weekly_2009 | DEEMPHASIS | 1 | -0.509 | p | False |
| core8 | train | obama_weekly_2009 | MUMBLE | 1 | -0.357 | ln | False |
| core8 | train | obama_weekly_2009 | RUSH | 2 | -0.372 | ln | True |
| core8 | train | obama_weekly_2009 | PAUSE_DROPPED | 2 | -0.536 | s | True |
| core8 | train | obama_weekly_2009 | MONOTONE | 2 | -5.83 | st | True |
| core8 | train | obama_weekly_2009 | FADE | 2 | -6.31 | dB | True |
| core8 | train | obama_weekly_2009 | DRAG | 2 | 0.372 | ln | True |
| core8 | train | obama_weekly_2009 | PAUSE_INTRUSIVE | 2 | 0.6 | s | True |
| core8 | train | obama_weekly_2009 | DEEMPHASIS | 2 | -0.954 | p | False |
| core8 | train | obama_weekly_2009 | MUMBLE | 2 | -0.766 | ln | True |
| core8 | train | obama_weekly_2009 | RUSH | 3 | -0.642 | ln | True |
| core8 | train | obama_weekly_2009 | PAUSE_DROPPED | 3 | -0.45 | s | True |
| core8 | train | obama_weekly_2009 | MONOTONE | 3 | -6.47 | st | True |
| core8 | train | obama_weekly_2009 | FADE | 3 | -7.47 | dB | True |
| core8 | train | obama_weekly_2009 | DRAG | 3 | 0.642 | ln | True |
| core8 | train | obama_weekly_2009 | PAUSE_INTRUSIVE | 3 | 1.2 | s | True |
| core8 | train | obama_weekly_2009 | DEEMPHASIS | 3 | -1.24 | p | True |
| core8 | train | obama_weekly_2009 | MUMBLE | 3 | -0.91 | ln | True |
| core8 | train | reagan_farewell_1989 | RUSH | 1 | -0.182 | ln | True |
| core8 | train | reagan_farewell_1989 | PAUSE_DROPPED | 1 | -0.51 | s | True |
| core8 | train | reagan_farewell_1989 | MONOTONE | 1 | -3.52 | st | False |
| core8 | train | reagan_farewell_1989 | FADE | 1 | -3.3 | dB | False |
| core8 | train | reagan_farewell_1989 | DRAG | 1 | 0.182 | ln | False |
| core8 | train | reagan_farewell_1989 | PAUSE_INTRUSIVE | 1 | 0.35 | s | True |
| core8 | train | reagan_farewell_1989 | DEEMPHASIS | 1 | -0.894 | p | False |
| core8 | train | reagan_farewell_1989 | MUMBLE | 1 | -0.347 | ln | False |
| core8 | train | reagan_farewell_1989 | RUSH | 2 | -0.372 | ln | True |
| core8 | train | reagan_farewell_1989 | PAUSE_DROPPED | 2 | -0.448 | s | True |
| core8 | train | reagan_farewell_1989 | MONOTONE | 2 | -4.04 | st | False |
| core8 | train | reagan_farewell_1989 | FADE | 2 | -6.48 | dB | True |
| core8 | train | reagan_farewell_1989 | DRAG | 2 | 0.372 | ln | True |
| core8 | train | reagan_farewell_1989 | PAUSE_INTRUSIVE | 2 | 0.6 | s | True |
| core8 | train | reagan_farewell_1989 | DEEMPHASIS | 2 | -0.894 | p | False |
| core8 | train | reagan_farewell_1989 | MUMBLE | 2 | -0.809 | ln | True |
| core8 | train | reagan_farewell_1989 | RUSH | 3 | -0.642 | ln | True |
| core8 | train | reagan_farewell_1989 | PAUSE_DROPPED | 3 | -0.71 | s | True |
| core8 | train | reagan_farewell_1989 | MONOTONE | 3 | -5.42 | st | True |
| core8 | train | reagan_farewell_1989 | FADE | 3 | -11.1 | dB | True |
| core8 | train | reagan_farewell_1989 | DRAG | 3 | 0.642 | ln | True |
| core8 | train | reagan_farewell_1989 | PAUSE_INTRUSIVE | 3 | 1.2 | s | True |
| core8 | train | reagan_farewell_1989 | DEEMPHASIS | 3 | -1.24 | p | True |
| core8 | train | reagan_farewell_1989 | MUMBLE | 3 | -1.01 | ln | True |
| lab_passed | val | eisenhower_farewell_1961 | NATURAL_RUSH | 1 | -0.731 | s | False |
| lab_passed | val | eisenhower_farewell_1961 | NATURAL_RUSH | 2 | -1.15 | s | False |
| lab_passed | val | eisenhower_farewell_1961 | NATURAL_RUSH | 3 | -1.58 | s | True |
| lab_passed | train | gwbush_911_2001 | NATURAL_RUSH | 1 | -0.567 | s | False |
| lab_passed | train | gwbush_911_2001 | NATURAL_RUSH | 2 | -0.882 | s | True |
| lab_passed | train | gwbush_911_2001 | NATURAL_RUSH | 3 | -1.21 | s | False |
| lab_passed | train | harris_uncsw_2021 | NATURAL_RUSH | 1 | -0.259 | s | False |
| lab_passed | train | harris_uncsw_2021 | NATURAL_RUSH | 2 | -0.382 | s | False |
| lab_passed | train | harris_uncsw_2021 | NATURAL_RUSH | 3 | -0.512 | s | False |
| lab_passed | train | hclinton_tomorrow_2010 | NATURAL_RUSH | 1 | -0.374 | s | False |
| lab_passed | train | hclinton_tomorrow_2010 | NATURAL_RUSH | 2 | -0.552 | s | False |
| lab_passed | train | hclinton_tomorrow_2010 | NATURAL_RUSH | 3 | -0.74 | s | True |
| lab_passed | val | lbush_radio_2001 | NATURAL_RUSH | 1 | -0.297 | s | False |
| lab_passed | val | lbush_radio_2001 | NATURAL_RUSH | 2 | -0.44 | s | False |
| lab_passed | val | lbush_radio_2001 | NATURAL_RUSH | 3 | -0.591 | s | False |
| lab_passed | test | mobama_weekly_2014 | NATURAL_RUSH | 1 | -0.361 | s | False |
| lab_passed | test | mobama_weekly_2014 | NATURAL_RUSH | 2 | -0.55 | s | False |
| lab_passed | test | mobama_weekly_2014 | NATURAL_RUSH | 3 | -0.747 | s | False |
| lab_passed | test | nixon_resignation_1974 | NATURAL_RUSH | 1 | -1.17 | s | False |
| lab_passed | test | nixon_resignation_1974 | NATURAL_RUSH | 2 | -1.9 | s | False |
| lab_passed | test | nixon_resignation_1974 | NATURAL_RUSH | 3 | -2.64 | s | True |
| lab_passed | train | obama_weekly_2009 | NATURAL_RUSH | 1 | -0.367 | s | False |
| lab_passed | train | obama_weekly_2009 | NATURAL_RUSH | 2 | -0.544 | s | False |
| lab_passed | train | obama_weekly_2009 | NATURAL_RUSH | 3 | -0.731 | s | False |
| lab_passed | train | reagan_farewell_1989 | NATURAL_RUSH | 1 | -0.184 | s | False |
| lab_passed | train | reagan_farewell_1989 | NATURAL_RUSH | 2 | -0.256 | s | False |
| lab_passed | train | reagan_farewell_1989 | NATURAL_RUSH | 3 | -0.333 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_REPETITION | 1 | 0.179 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | HESITATION | 1 | 0.232 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | SOUND_REPETITION | 1 | 0.294 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | MISPLACED_EMPHASIS | 1 | 0.65 | p | False |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_BY_WORD | 1 | 0.6 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_BY_WORD | 1 | 0.6 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_BY_WORD | 1 | 0.6 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_BY_WORD | 1 | 0.6 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | RHYME_PROLONGATION | 1 | 0.18 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | TRAILING_OFF | 1 | -0.939 | dB | False |
| synthetic_only | val | eisenhower_farewell_1961 | UNEVEN_TEMPO | 1 | 0.113 | ratio |  |
| synthetic_only | val | eisenhower_farewell_1961 | ONSET_PROLONGATION | 1 | 0.25 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | BLOCK | 1 | 0.5 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_REPETITION | 2 | 0.322 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | HESITATION | 2 | 0.58 | s | True |
| synthetic_only | val | eisenhower_farewell_1961 | SOUND_REPETITION | 2 | 0.44 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | MISPLACED_EMPHASIS | 2 | 1.23 | p | False |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_BY_WORD | 2 | 0.9 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_BY_WORD | 2 | 0.9 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_BY_WORD | 2 | 0.9 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_BY_WORD | 2 | 0.9 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | RHYME_PROLONGATION | 2 | 0.36 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | TRAILING_OFF | 2 | -1.78 | dB | False |
| synthetic_only | val | eisenhower_farewell_1961 | UNEVEN_TEMPO | 2 | 0.225 | ratio |  |
| synthetic_only | val | eisenhower_farewell_1961 | ONSET_PROLONGATION | 2 | 0.55 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | BLOCK | 2 | 1.25 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_REPETITION | 3 | 0.466 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | HESITATION | 3 | 1.13 | s | True |
| synthetic_only | val | eisenhower_farewell_1961 | SOUND_REPETITION | 3 | 0.589 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | MISPLACED_EMPHASIS | 3 | 1.76 | p | False |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_BY_WORD | 3 | 1.2 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_BY_WORD | 3 | 1.2 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_BY_WORD | 3 | 1.2 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | WORD_BY_WORD | 3 | 1.2 | s | False |
| synthetic_only | val | eisenhower_farewell_1961 | RHYME_PROLONGATION | 3 | 0.54 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | TRAILING_OFF | 3 | -2.54 | dB | False |
| synthetic_only | val | eisenhower_farewell_1961 | UNEVEN_TEMPO | 3 | 0.338 | ratio |  |
| synthetic_only | val | eisenhower_farewell_1961 | ONSET_PROLONGATION | 3 | 0.9 | s |  |
| synthetic_only | val | eisenhower_farewell_1961 | BLOCK | 3 | 2 | s |  |
| synthetic_only | train | gwbush_911_2001 | WORD_REPETITION | 1 | 0.206 | s |  |
| synthetic_only | train | gwbush_911_2001 | LOW_EFFORT | 1 | -2.67 | dB | False |
| synthetic_only | train | gwbush_911_2001 | HESITATION | 1 | 0.224 | s | False |
| synthetic_only | train | gwbush_911_2001 | SOUND_REPETITION | 1 | 0.273 | s |  |
| synthetic_only | train | gwbush_911_2001 | MISPLACED_EMPHASIS | 1 | 0.833 | p | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | gwbush_911_2001 | RHYME_PROLONGATION | 1 | 0.18 | s |  |
| synthetic_only | train | gwbush_911_2001 | TRAILING_OFF | 1 | -0.876 | dB | False |
| synthetic_only | train | gwbush_911_2001 | UNEVEN_TEMPO | 1 | 0.104 | ratio |  |
| synthetic_only | train | gwbush_911_2001 | ONSET_PROLONGATION | 1 | 0.25 | s |  |
| synthetic_only | train | gwbush_911_2001 | BLOCK | 1 | 0.5 | s |  |
| synthetic_only | train | gwbush_911_2001 | REPEATED_CONTOUR | 1 | -0.329 | st |  |
| synthetic_only | train | gwbush_911_2001 | WORD_REPETITION | 2 | 0.355 | s |  |
| synthetic_only | train | gwbush_911_2001 | LOW_EFFORT | 2 | -5.25 | dB | True |
| synthetic_only | train | gwbush_911_2001 | HESITATION | 2 | 0.56 | s | True |
| synthetic_only | train | gwbush_911_2001 | SOUND_REPETITION | 2 | 0.407 | s |  |
| synthetic_only | train | gwbush_911_2001 | MISPLACED_EMPHASIS | 2 | 1.62 | p | False |
| synthetic_only | train | gwbush_911_2001 | FLAT_FINAL_FALL | 2 | -1.3 | st |  |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | gwbush_911_2001 | RHYME_PROLONGATION | 2 | 0.36 | s |  |
| synthetic_only | train | gwbush_911_2001 | TRAILING_OFF | 2 | -1.6 | dB | False |
| synthetic_only | train | gwbush_911_2001 | UNEVEN_TEMPO | 2 | 0.208 | ratio |  |
| synthetic_only | train | gwbush_911_2001 | ONSET_PROLONGATION | 2 | 0.55 | s |  |
| synthetic_only | train | gwbush_911_2001 | BLOCK | 2 | 1.25 | s |  |
| synthetic_only | train | gwbush_911_2001 | REPEATED_CONTOUR | 2 | -0.588 | st |  |
| synthetic_only | train | gwbush_911_2001 | WORD_REPETITION | 3 | 0.505 | s |  |
| synthetic_only | train | gwbush_911_2001 | LOW_EFFORT | 3 | -7.49 | dB | True |
| synthetic_only | train | gwbush_911_2001 | HESITATION | 3 | 1.1 | s | True |
| synthetic_only | train | gwbush_911_2001 | SOUND_REPETITION | 3 | 0.543 | s |  |
| synthetic_only | train | gwbush_911_2001 | MISPLACED_EMPHASIS | 3 | 2.4 | p | False |
| synthetic_only | train | gwbush_911_2001 | FLAT_FINAL_FALL | 3 | -1.96 | st |  |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | gwbush_911_2001 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | gwbush_911_2001 | RHYME_PROLONGATION | 3 | 0.54 | s |  |
| synthetic_only | train | gwbush_911_2001 | TRAILING_OFF | 3 | -2.21 | dB | True |
| synthetic_only | train | gwbush_911_2001 | UNEVEN_TEMPO | 3 | 0.312 | ratio |  |
| synthetic_only | train | gwbush_911_2001 | ONSET_PROLONGATION | 3 | 0.9 | s |  |
| synthetic_only | train | gwbush_911_2001 | BLOCK | 3 | 2 | s |  |
| synthetic_only | train | gwbush_911_2001 | REPEATED_CONTOUR | 3 | -0.932 | st |  |
| synthetic_only | train | harris_uncsw_2021 | WORD_REPETITION | 1 | 0.149 | s |  |
| synthetic_only | train | harris_uncsw_2021 | HESITATION | 1 | 0.256 | s | False |
| synthetic_only | train | harris_uncsw_2021 | SOUND_REPETITION | 1 | 0.36 | s |  |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | train | harris_uncsw_2021 | RHYME_PROLONGATION | 1 | 0.18 | s |  |
| synthetic_only | train | harris_uncsw_2021 | TRAILING_OFF | 1 | -1.09 | dB | False |
| synthetic_only | train | harris_uncsw_2021 | UNEVEN_TEMPO | 1 | 0.111 | ratio |  |
| synthetic_only | train | harris_uncsw_2021 | ONSET_PROLONGATION | 1 | 0.25 | s |  |
| synthetic_only | train | harris_uncsw_2021 | BLOCK | 1 | 0.5 | s |  |
| synthetic_only | train | harris_uncsw_2021 | REPEATED_CONTOUR | 1 | -1.03 | st |  |
| synthetic_only | train | harris_uncsw_2021 | WORD_REPETITION | 2 | 0.285 | s |  |
| synthetic_only | train | harris_uncsw_2021 | HESITATION | 2 | 0.64 | s | True |
| synthetic_only | train | harris_uncsw_2021 | SOUND_REPETITION | 2 | 0.543 | s |  |
| synthetic_only | train | harris_uncsw_2021 | FLAT_FINAL_FALL | 2 | -1.79 | st |  |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | train | harris_uncsw_2021 | RHYME_PROLONGATION | 2 | 0.36 | s |  |
| synthetic_only | train | harris_uncsw_2021 | TRAILING_OFF | 2 | -2 | dB | False |
| synthetic_only | train | harris_uncsw_2021 | UNEVEN_TEMPO | 2 | 0.221 | ratio |  |
| synthetic_only | train | harris_uncsw_2021 | ONSET_PROLONGATION | 2 | 0.55 | s |  |
| synthetic_only | train | harris_uncsw_2021 | BLOCK | 2 | 1.25 | s |  |
| synthetic_only | train | harris_uncsw_2021 | REPEATED_CONTOUR | 2 | -2 | st |  |
| synthetic_only | train | harris_uncsw_2021 | WORD_REPETITION | 3 | 0.421 | s |  |
| synthetic_only | train | harris_uncsw_2021 | RISING_ENDING | 3 | 5.69 | st |  |
| synthetic_only | train | harris_uncsw_2021 | HESITATION | 3 | 1.22 | s | True |
| synthetic_only | train | harris_uncsw_2021 | SOUND_REPETITION | 3 | 0.72 | s |  |
| synthetic_only | train | harris_uncsw_2021 | MISPLACED_EMPHASIS | 3 | 2.1 | p | True |
| synthetic_only | train | harris_uncsw_2021 | FLAT_FINAL_FALL | 3 | -2.61 | st |  |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | harris_uncsw_2021 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | train | harris_uncsw_2021 | RHYME_PROLONGATION | 3 | 0.54 | s |  |
| synthetic_only | train | harris_uncsw_2021 | TRAILING_OFF | 3 | -2.76 | dB | False |
| synthetic_only | train | harris_uncsw_2021 | UNEVEN_TEMPO | 3 | 0.332 | ratio |  |
| synthetic_only | train | harris_uncsw_2021 | ONSET_PROLONGATION | 3 | 0.9 | s |  |
| synthetic_only | train | harris_uncsw_2021 | BLOCK | 3 | 2 | s |  |
| synthetic_only | train | harris_uncsw_2021 | REPEATED_CONTOUR | 3 | -2.86 | st |  |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_REPETITION | 1 | 0.392 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | LOW_EFFORT | 1 | -2.26 | dB | False |
| synthetic_only | train | hclinton_tomorrow_2010 | HESITATION | 1 | 0.256 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | SOUND_REPETITION | 1 | 0.307 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | MISPLACED_EMPHASIS | 1 | 0.734 | p | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | RHYME_PROLONGATION | 1 | 0.18 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | TRAILING_OFF | 1 | -1.08 | dB | False |
| synthetic_only | train | hclinton_tomorrow_2010 | UNEVEN_TEMPO | 1 | 0.102 | ratio |  |
| synthetic_only | train | hclinton_tomorrow_2010 | ONSET_PROLONGATION | 1 | 0.25 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | BLOCK | 1 | 0.5 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_REPETITION | 2 | 0.585 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | LOW_EFFORT | 2 | -4.27 | dB | False |
| synthetic_only | train | hclinton_tomorrow_2010 | HESITATION | 2 | 0.64 | s | True |
| synthetic_only | train | hclinton_tomorrow_2010 | SOUND_REPETITION | 2 | 0.461 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | MISPLACED_EMPHASIS | 2 | 1.37 | p | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | RHYME_PROLONGATION | 2 | 0.36 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | TRAILING_OFF | 2 | -2.05 | dB | False |
| synthetic_only | train | hclinton_tomorrow_2010 | UNEVEN_TEMPO | 2 | 0.204 | ratio |  |
| synthetic_only | train | hclinton_tomorrow_2010 | ONSET_PROLONGATION | 2 | 0.55 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | BLOCK | 2 | 1.25 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_REPETITION | 3 | 0.777 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | LOW_EFFORT | 3 | -6.03 | dB | True |
| synthetic_only | train | hclinton_tomorrow_2010 | HESITATION | 3 | 1.22 | s | True |
| synthetic_only | train | hclinton_tomorrow_2010 | SOUND_REPETITION | 3 | 0.61 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | MISPLACED_EMPHASIS | 3 | 2.1 | p | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | hclinton_tomorrow_2010 | RHYME_PROLONGATION | 3 | 0.54 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | TRAILING_OFF | 3 | -2.96 | dB | True |
| synthetic_only | train | hclinton_tomorrow_2010 | UNEVEN_TEMPO | 3 | 0.306 | ratio |  |
| synthetic_only | train | hclinton_tomorrow_2010 | ONSET_PROLONGATION | 3 | 0.9 | s |  |
| synthetic_only | train | hclinton_tomorrow_2010 | BLOCK | 3 | 2 | s |  |
| synthetic_only | val | lbush_radio_2001 | WORD_REPETITION | 1 | 0.208 | s |  |
| synthetic_only | val | lbush_radio_2001 | HESITATION | 1 | 0.244 | s | False |
| synthetic_only | val | lbush_radio_2001 | SOUND_REPETITION | 1 | 0.25 | s |  |
| synthetic_only | val | lbush_radio_2001 | MISPLACED_EMPHASIS | 1 | 1.06 | p | False |
| synthetic_only | val | lbush_radio_2001 | WORD_BY_WORD | 1 | 0.6 | s | False |
| synthetic_only | val | lbush_radio_2001 | WORD_BY_WORD | 1 | 0.6 | s | False |
| synthetic_only | val | lbush_radio_2001 | WORD_BY_WORD | 1 | 0.6 | s | False |
| synthetic_only | val | lbush_radio_2001 | WORD_BY_WORD | 1 | 0.6 | s | False |
| synthetic_only | val | lbush_radio_2001 | RHYME_PROLONGATION | 1 | 0.18 | s |  |
| synthetic_only | val | lbush_radio_2001 | TRAILING_OFF | 1 | -1.88 | dB | False |
| synthetic_only | val | lbush_radio_2001 | UNEVEN_TEMPO | 1 | 0.0897 | ratio |  |
| synthetic_only | val | lbush_radio_2001 | ONSET_PROLONGATION | 1 | 0.25 | s |  |
| synthetic_only | val | lbush_radio_2001 | REPEATED_CONTOUR | 1 | -1.34 | st |  |
| synthetic_only | val | lbush_radio_2001 | WORD_REPETITION | 2 | 0.357 | s |  |
| synthetic_only | val | lbush_radio_2001 | HESITATION | 2 | 0.61 | s | True |
| synthetic_only | val | lbush_radio_2001 | SOUND_REPETITION | 2 | 0.374 | s |  |
| synthetic_only | val | lbush_radio_2001 | MISPLACED_EMPHASIS | 2 | 2.01 | p | False |
| synthetic_only | val | lbush_radio_2001 | WORD_BY_WORD | 2 | 0.9 | s | False |
| synthetic_only | val | lbush_radio_2001 | WORD_BY_WORD | 2 | 0.9 | s | False |
| synthetic_only | val | lbush_radio_2001 | WORD_BY_WORD | 2 | 0.9 | s | False |
| synthetic_only | val | lbush_radio_2001 | WORD_BY_WORD | 2 | 0.9 | s | False |
| synthetic_only | val | lbush_radio_2001 | RHYME_PROLONGATION | 2 | 0.36 | s |  |
| synthetic_only | val | lbush_radio_2001 | TRAILING_OFF | 2 | -3.62 | dB | False |
| synthetic_only | val | lbush_radio_2001 | UNEVEN_TEMPO | 2 | 0.179 | ratio |  |
| synthetic_only | val | lbush_radio_2001 | ONSET_PROLONGATION | 2 | 0.55 | s |  |
| synthetic_only | val | lbush_radio_2001 | REPEATED_CONTOUR | 2 | -2.66 | st |  |
| synthetic_only | val | lbush_radio_2001 | WORD_REPETITION | 3 | 0.507 | s |  |
| synthetic_only | val | lbush_radio_2001 | RISING_ENDING | 3 | 6.21 | st |  |
| synthetic_only | val | lbush_radio_2001 | HESITATION | 3 | 1.18 | s | True |
| synthetic_only | val | lbush_radio_2001 | SOUND_REPETITION | 3 | 0.497 | s |  |
| synthetic_only | val | lbush_radio_2001 | MISPLACED_EMPHASIS | 3 | 2.51 | p | True |
| synthetic_only | val | lbush_radio_2001 | WORD_BY_WORD | 3 | 1.2 | s | False |
| synthetic_only | val | lbush_radio_2001 | WORD_BY_WORD | 3 | 1.2 | s | False |
| synthetic_only | val | lbush_radio_2001 | WORD_BY_WORD | 3 | 1.2 | s | False |
| synthetic_only | val | lbush_radio_2001 | WORD_BY_WORD | 3 | 1.2 | s | False |
| synthetic_only | val | lbush_radio_2001 | RHYME_PROLONGATION | 3 | 0.54 | s |  |
| synthetic_only | val | lbush_radio_2001 | TRAILING_OFF | 3 | -5.22 | dB | False |
| synthetic_only | val | lbush_radio_2001 | UNEVEN_TEMPO | 3 | 0.269 | ratio |  |
| synthetic_only | val | lbush_radio_2001 | ONSET_PROLONGATION | 3 | 0.9 | s |  |
| synthetic_only | val | lbush_radio_2001 | REPEATED_CONTOUR | 3 | -2.84 | st |  |
| synthetic_only | test | mobama_weekly_2014 | WORD_REPETITION | 1 | 0.268 | s |  |
| synthetic_only | test | mobama_weekly_2014 | HESITATION | 1 | 0.28 | s | False |
| synthetic_only | test | mobama_weekly_2014 | SOUND_REPETITION | 1 | 0.33 | s |  |
| synthetic_only | test | mobama_weekly_2014 | FLAT_FINAL_FALL | 1 | -0.713 | st |  |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | mobama_weekly_2014 | RHYME_PROLONGATION | 1 | 0.18 | s |  |
| synthetic_only | test | mobama_weekly_2014 | UNEVEN_TEMPO | 1 | 0.0976 | ratio |  |
| synthetic_only | test | mobama_weekly_2014 | ONSET_PROLONGATION | 1 | 0.25 | s |  |
| synthetic_only | test | mobama_weekly_2014 | BLOCK | 1 | 0.5 | s |  |
| synthetic_only | test | mobama_weekly_2014 | REPEATED_CONTOUR | 1 | -1.55 | st |  |
| synthetic_only | test | mobama_weekly_2014 | WORD_REPETITION | 2 | 0.432 | s |  |
| synthetic_only | test | mobama_weekly_2014 | HESITATION | 2 | 0.7 | s | True |
| synthetic_only | test | mobama_weekly_2014 | SOUND_REPETITION | 2 | 0.49 | s |  |
| synthetic_only | test | mobama_weekly_2014 | MISPLACED_EMPHASIS | 2 | 2.01 | p | False |
| synthetic_only | test | mobama_weekly_2014 | FLAT_FINAL_FALL | 2 | -1.4 | st |  |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | mobama_weekly_2014 | RHYME_PROLONGATION | 2 | 0.36 | s |  |
| synthetic_only | test | mobama_weekly_2014 | UNEVEN_TEMPO | 2 | 0.195 | ratio |  |
| synthetic_only | test | mobama_weekly_2014 | ONSET_PROLONGATION | 2 | 0.55 | s |  |
| synthetic_only | test | mobama_weekly_2014 | BLOCK | 2 | 1.25 | s |  |
| synthetic_only | test | mobama_weekly_2014 | REPEATED_CONTOUR | 2 | -3.11 | st |  |
| synthetic_only | test | mobama_weekly_2014 | WORD_REPETITION | 3 | 0.595 | s |  |
| synthetic_only | test | mobama_weekly_2014 | RISING_ENDING | 3 | 6.04 | st |  |
| synthetic_only | test | mobama_weekly_2014 | HESITATION | 3 | 1.32 | s | True |
| synthetic_only | test | mobama_weekly_2014 | SOUND_REPETITION | 3 | 0.657 | s |  |
| synthetic_only | test | mobama_weekly_2014 | MISPLACED_EMPHASIS | 3 | 3.21 | p | True |
| synthetic_only | test | mobama_weekly_2014 | FLAT_FINAL_FALL | 3 | -2.04 | st |  |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | mobama_weekly_2014 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | mobama_weekly_2014 | RHYME_PROLONGATION | 3 | 0.54 | s |  |
| synthetic_only | test | mobama_weekly_2014 | UNEVEN_TEMPO | 3 | 0.293 | ratio |  |
| synthetic_only | test | mobama_weekly_2014 | ONSET_PROLONGATION | 3 | 0.9 | s |  |
| synthetic_only | test | mobama_weekly_2014 | BLOCK | 3 | 2 | s |  |
| synthetic_only | test | mobama_weekly_2014 | REPEATED_CONTOUR | 3 | -4.42 | st |  |
| synthetic_only | test | nixon_resignation_1974 | WORD_REPETITION | 1 | 0.297 | s |  |
| synthetic_only | test | nixon_resignation_1974 | LOW_EFFORT | 1 | -2.91 | dB | False |
| synthetic_only | test | nixon_resignation_1974 | HESITATION | 1 | 0.256 | s | False |
| synthetic_only | test | nixon_resignation_1974 | SOUND_REPETITION | 1 | 0.326 | s |  |
| synthetic_only | test | nixon_resignation_1974 | MISPLACED_EMPHASIS | 1 | 0.789 | p | False |
| synthetic_only | test | nixon_resignation_1974 | FLAT_FINAL_FALL | 1 | -1.13 | st |  |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 1 | 1.05 | s | False |
| synthetic_only | test | nixon_resignation_1974 | RHYME_PROLONGATION | 1 | 0.18 | s |  |
| synthetic_only | test | nixon_resignation_1974 | TRAILING_OFF | 1 | -1.2 | dB | False |
| synthetic_only | test | nixon_resignation_1974 | UNEVEN_TEMPO | 1 | 0.0768 | ratio |  |
| synthetic_only | test | nixon_resignation_1974 | ONSET_PROLONGATION | 1 | 0.25 | s |  |
| synthetic_only | test | nixon_resignation_1974 | BLOCK | 1 | 0.5 | s |  |
| synthetic_only | test | nixon_resignation_1974 | REPEATED_CONTOUR | 1 | -0.984 | st |  |
| synthetic_only | test | nixon_resignation_1974 | WORD_REPETITION | 2 | 0.467 | s |  |
| synthetic_only | test | nixon_resignation_1974 | LOW_EFFORT | 2 | -5.58 | dB | True |
| synthetic_only | test | nixon_resignation_1974 | HESITATION | 2 | 0.64 | s | True |
| synthetic_only | test | nixon_resignation_1974 | SOUND_REPETITION | 2 | 0.492 | s |  |
| synthetic_only | test | nixon_resignation_1974 | MISPLACED_EMPHASIS | 2 | 1.74 | p | False |
| synthetic_only | test | nixon_resignation_1974 | FLAT_FINAL_FALL | 2 | -2.16 | st |  |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 2 | 1.57 | s | False |
| synthetic_only | test | nixon_resignation_1974 | RHYME_PROLONGATION | 2 | 0.36 | s |  |
| synthetic_only | test | nixon_resignation_1974 | TRAILING_OFF | 2 | -2.28 | dB | False |
| synthetic_only | test | nixon_resignation_1974 | UNEVEN_TEMPO | 2 | 0.154 | ratio |  |
| synthetic_only | test | nixon_resignation_1974 | ONSET_PROLONGATION | 2 | 0.55 | s |  |
| synthetic_only | test | nixon_resignation_1974 | BLOCK | 2 | 1.25 | s |  |
| synthetic_only | test | nixon_resignation_1974 | REPEATED_CONTOUR | 2 | -1.98 | st |  |
| synthetic_only | test | nixon_resignation_1974 | WORD_REPETITION | 3 | 0.637 | s |  |
| synthetic_only | test | nixon_resignation_1974 | LOW_EFFORT | 3 | -7.98 | dB | True |
| synthetic_only | test | nixon_resignation_1974 | RISING_ENDING | 3 | 5.46 | st |  |
| synthetic_only | test | nixon_resignation_1974 | HESITATION | 3 | 1.22 | s | True |
| synthetic_only | test | nixon_resignation_1974 | SOUND_REPETITION | 3 | 0.652 | s |  |
| synthetic_only | test | nixon_resignation_1974 | MISPLACED_EMPHASIS | 3 | 2.6 | p | False |
| synthetic_only | test | nixon_resignation_1974 | FLAT_FINAL_FALL | 3 | -3.13 | st |  |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | nixon_resignation_1974 | WORD_BY_WORD | 3 | 2.1 | s | False |
| synthetic_only | test | nixon_resignation_1974 | RHYME_PROLONGATION | 3 | 0.54 | s |  |
| synthetic_only | test | nixon_resignation_1974 | TRAILING_OFF | 3 | -3.25 | dB | True |
| synthetic_only | test | nixon_resignation_1974 | UNEVEN_TEMPO | 3 | 0.231 | ratio |  |
| synthetic_only | test | nixon_resignation_1974 | ONSET_PROLONGATION | 3 | 0.9 | s |  |
| synthetic_only | test | nixon_resignation_1974 | BLOCK | 3 | 2 | s |  |
| synthetic_only | test | nixon_resignation_1974 | REPEATED_CONTOUR | 3 | -2.03 | st |  |
| synthetic_only | train | obama_weekly_2009 | WORD_REPETITION | 1 | 0.178 | s |  |
| synthetic_only | train | obama_weekly_2009 | LOW_EFFORT | 1 | -3.11 | dB | False |
| synthetic_only | train | obama_weekly_2009 | HESITATION | 1 | 0.24 | s | False |
| synthetic_only | train | obama_weekly_2009 | SOUND_REPETITION | 1 | 0.384 | s |  |
| synthetic_only | train | obama_weekly_2009 | MISPLACED_EMPHASIS | 1 | 0.743 | p | False |
| synthetic_only | train | obama_weekly_2009 | FLAT_FINAL_FALL | 1 | -0.521 | st |  |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | obama_weekly_2009 | RHYME_PROLONGATION | 1 | 0.18 | s |  |
| synthetic_only | train | obama_weekly_2009 | TRAILING_OFF | 1 | -1.01 | dB | False |
| synthetic_only | train | obama_weekly_2009 | UNEVEN_TEMPO | 1 | 0.106 | ratio |  |
| synthetic_only | train | obama_weekly_2009 | ONSET_PROLONGATION | 1 | 0.25 | s |  |
| synthetic_only | train | obama_weekly_2009 | BLOCK | 1 | 0.5 | s |  |
| synthetic_only | train | obama_weekly_2009 | WORD_REPETITION | 2 | 0.321 | s |  |
| synthetic_only | train | obama_weekly_2009 | LOW_EFFORT | 2 | -6.24 | dB | False |
| synthetic_only | train | obama_weekly_2009 | HESITATION | 2 | 0.6 | s | True |
| synthetic_only | train | obama_weekly_2009 | SOUND_REPETITION | 2 | 0.579 | s |  |
| synthetic_only | train | obama_weekly_2009 | MISPLACED_EMPHASIS | 2 | 1.33 | p | False |
| synthetic_only | train | obama_weekly_2009 | FLAT_FINAL_FALL | 2 | -1.14 | st |  |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | obama_weekly_2009 | RHYME_PROLONGATION | 2 | 0.36 | s |  |
| synthetic_only | train | obama_weekly_2009 | TRAILING_OFF | 2 | -1.86 | dB | False |
| synthetic_only | train | obama_weekly_2009 | UNEVEN_TEMPO | 2 | 0.212 | ratio |  |
| synthetic_only | train | obama_weekly_2009 | ONSET_PROLONGATION | 2 | 0.55 | s |  |
| synthetic_only | train | obama_weekly_2009 | BLOCK | 2 | 1.25 | s |  |
| synthetic_only | train | obama_weekly_2009 | WORD_REPETITION | 3 | 0.463 | s |  |
| synthetic_only | train | obama_weekly_2009 | LOW_EFFORT | 3 | -9.02 | dB | False |
| synthetic_only | train | obama_weekly_2009 | HESITATION | 3 | 1.16 | s | True |
| synthetic_only | train | obama_weekly_2009 | SOUND_REPETITION | 3 | 0.774 | s |  |
| synthetic_only | train | obama_weekly_2009 | MISPLACED_EMPHASIS | 3 | 2.06 | p | False |
| synthetic_only | train | obama_weekly_2009 | FLAT_FINAL_FALL | 3 | -2.86 | st |  |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | obama_weekly_2009 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | obama_weekly_2009 | RHYME_PROLONGATION | 3 | 0.54 | s |  |
| synthetic_only | train | obama_weekly_2009 | TRAILING_OFF | 3 | -2.57 | dB | True |
| synthetic_only | train | obama_weekly_2009 | UNEVEN_TEMPO | 3 | 0.319 | ratio |  |
| synthetic_only | train | obama_weekly_2009 | ONSET_PROLONGATION | 3 | 0.9 | s |  |
| synthetic_only | train | obama_weekly_2009 | BLOCK | 3 | 2 | s |  |
| synthetic_only | train | reagan_farewell_1989 | WORD_REPETITION | 1 | 0.225 | s |  |
| synthetic_only | train | reagan_farewell_1989 | LOW_EFFORT | 1 | -2.01 | dB | False |
| synthetic_only | train | reagan_farewell_1989 | HESITATION | 1 | 0.248 | s | False |
| synthetic_only | train | reagan_farewell_1989 | SOUND_REPETITION | 1 | 0.299 | s |  |
| synthetic_only | train | reagan_farewell_1989 | MISPLACED_EMPHASIS | 1 | 0.739 | p | False |
| synthetic_only | train | reagan_farewell_1989 | FLAT_FINAL_FALL | 1 | -0.968 | st |  |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 1 | 0.75 | s | False |
| synthetic_only | train | reagan_farewell_1989 | RHYME_PROLONGATION | 1 | 0.18 | s |  |
| synthetic_only | train | reagan_farewell_1989 | TRAILING_OFF | 1 | -1.68 | dB | False |
| synthetic_only | train | reagan_farewell_1989 | UNEVEN_TEMPO | 1 | 0.0924 | ratio |  |
| synthetic_only | train | reagan_farewell_1989 | ONSET_PROLONGATION | 1 | 0.25 | s |  |
| synthetic_only | train | reagan_farewell_1989 | REPEATED_CONTOUR | 1 | -1.09 | st |  |
| synthetic_only | train | reagan_farewell_1989 | WORD_REPETITION | 2 | 0.379 | s |  |
| synthetic_only | train | reagan_farewell_1989 | LOW_EFFORT | 2 | -3.94 | dB | True |
| synthetic_only | train | reagan_farewell_1989 | HESITATION | 2 | 0.62 | s | True |
| synthetic_only | train | reagan_farewell_1989 | SOUND_REPETITION | 2 | 0.447 | s |  |
| synthetic_only | train | reagan_farewell_1989 | MISPLACED_EMPHASIS | 2 | 1.48 | p | False |
| synthetic_only | train | reagan_farewell_1989 | FLAT_FINAL_FALL | 2 | -2.36 | st |  |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 2 | 1.12 | s | False |
| synthetic_only | train | reagan_farewell_1989 | RHYME_PROLONGATION | 2 | 0.36 | s |  |
| synthetic_only | train | reagan_farewell_1989 | TRAILING_OFF | 2 | -3.16 | dB | False |
| synthetic_only | train | reagan_farewell_1989 | UNEVEN_TEMPO | 2 | 0.185 | ratio |  |
| synthetic_only | train | reagan_farewell_1989 | ONSET_PROLONGATION | 2 | 0.55 | s |  |
| synthetic_only | train | reagan_farewell_1989 | REPEATED_CONTOUR | 2 | -2 | st |  |
| synthetic_only | train | reagan_farewell_1989 | WORD_REPETITION | 3 | 0.533 | s |  |
| synthetic_only | train | reagan_farewell_1989 | LOW_EFFORT | 3 | -5.58 | dB | True |
| synthetic_only | train | reagan_farewell_1989 | HESITATION | 3 | 1.19 | s | True |
| synthetic_only | train | reagan_farewell_1989 | SOUND_REPETITION | 3 | 0.594 | s |  |
| synthetic_only | train | reagan_farewell_1989 | MISPLACED_EMPHASIS | 3 | 2.24 | p | False |
| synthetic_only | train | reagan_farewell_1989 | FLAT_FINAL_FALL | 3 | -3.74 | st |  |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | reagan_farewell_1989 | WORD_BY_WORD | 3 | 1.5 | s | False |
| synthetic_only | train | reagan_farewell_1989 | RHYME_PROLONGATION | 3 | 0.54 | s |  |
| synthetic_only | train | reagan_farewell_1989 | TRAILING_OFF | 3 | -4.46 | dB | True |
| synthetic_only | train | reagan_farewell_1989 | UNEVEN_TEMPO | 3 | 0.277 | ratio |  |
| synthetic_only | train | reagan_farewell_1989 | ONSET_PROLONGATION | 3 | 0.9 | s |  |
| synthetic_only | train | reagan_farewell_1989 | REPEATED_CONTOUR | 3 | -2.58 | st |  |

## Activation matrix

core8:

Split train:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| D1 | 21 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 12 |
| D2 | 1 | 20 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| D3 | 0 | 0 | 10 | 0 | 1 | 0 | 0 | 0 | 0 |
| D4 | 0 | 0 | 0 | 7 | 1 | 0 | 0 | 0 | 0 |
| D5 | 0 | 0 | 0 | 1 | 10 | 0 | 0 | 0 | 0 |
| D6 | 0 | 0 | 0 | 0 | 1 | 10 | 0 | 0 | 0 |

Split val:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| D1 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 |
| D2 | 0 | 8 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| D3 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| D4 | 0 | 0 | 2 | 4 | 0 | 0 | 0 | 0 | 0 |
| D5 | 1 | 2 | 0 | 2 | 4 | 0 | 0 | 0 | 0 |
| D6 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 |

Split test:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| D1 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 |
| D2 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| D3 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| D4 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 1 |
| D5 | 1 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 |
| D6 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 |

Split val+test:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| D1 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| D2 | 0 | 16 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| D3 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| D4 | 0 | 0 | 2 | 7 | 0 | 0 | 0 | 0 | 1 |
| D5 | 2 | 2 | 0 | 2 | 8 | 0 | 0 | 0 | 0 |
| D6 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 |

lab_passed:

Split train:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| D9 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| none | 2 | 1 | 0 | 1 | 9 | 0 | 0 | 0 | 1 |

Split val:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| D9 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| none | 2 | 5 | 0 | 2 | 3 | 0 | 0 | 0 | 1 |

Split test:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| D9 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| none | 2 | 2 | 0 | 1 | 4 | 0 | 0 | 0 | 0 |

Split val+test:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| D9 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| none | 4 | 7 | 0 | 3 | 7 | 0 | 0 | 0 | 1 |

synthetic_only (unvalidated):

Split train:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| D2 | 1 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| D4 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| D5 | 0 | 0 | 0 | 1 | 11 | 0 | 0 | 0 | 0 |
| D7 | 29 | 10 | 0 | 0 | 7 | 0 | 0 | 0 | 1 |
| NO_DETECTOR | 0 | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| none | 1 | 4 | 0 | 0 | 2 | 0 | 0 | 0 | 3 |

Split val:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| D2 | 8 | 4 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| D4 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| D5 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| D7 | 8 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| none | 2 | 7 | 0 | 2 | 3 | 0 | 0 | 0 | 2 |

Split test:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| D2 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| D4 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| D5 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| D7 | 14 | 6 | 0 | 0 | 3 | 0 | 0 | 0 | 3 |
| D8 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| none | 2 | 6 | 0 | 1 | 2 | 0 | 0 | 0 | 3 |

Split val+test:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| D2 | 9 | 8 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| D4 | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 |
| D5 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 |
| D7 | 22 | 12 | 1 | 0 | 3 | 0 | 0 | 0 | 3 |
| D8 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| none | 4 | 13 | 0 | 3 | 5 | 0 | 0 | 0 | 5 |

## Select-set promotion and PPV at the stated base rate

| candidate key | status | rate | bootstrap upper95 | rule of three | L3 recall | found | away edits |
|---|---|---|---|---|---|---|---|
| D7+ | listed |  |  |  |  |  |  |
| D8+ | listed |  |  |  |  |  |  |
| D9- | listed |  |  |  |  |  |  |

Whole-clip candidate diagnostics:

| key | rate | bootstrap upper95 | rule of three | L3 recall | found | away edits |
|---|---|---|---|---|---|---|

D7 PPV at 0.21% stuttered syllables:

| Real sensitivity | false regions / measured syllable (proxy) | expected PPV | scope |
|---|---|---|---|
|  |  |  | requires an enabled D7 key and Real syllable sensitivity |

Fit and select null reports of both R2 modes:

| mode | set | weighted total/min | pooled total/min | weighted upper95 | budget status | budget statement | scope |
|---|---|---|---|---|---|---|---|
| consensus5 | fit | 0.468 | 0.457 | 0.564 | met | 0.5/min budget holds at the point rate; upper95 does not establish the budget | all fit sources |
| consensus5 | select | 0.536 | 0.401 | 0.67 | not met on covered sources only | consensus select rates cover accent, ears, gettysburg with equal source weights; poetry is not covered: no consensus readers: 20 texts with 0-5 readers of the set each, so a reader has at most 4 distinct same-text references; 5 are needed (6 readers of one text). over the covered sources only, 0.5/min budget is not met at the point rate; upper95 does not establish the budget | consensus select rates cover accent, ears, gettysburg with equal source weights; poetry is not covered: no consensus readers: 20 texts with 0-5 readers of the set each, so a reader has at most 4 distinct same-text references; 5 are needed (6 readers of one text) |
| single | fit | 0.491 | 0.45 | 0.545 | met | 0.5/min budget holds at the point rate; upper95 does not establish the budget | all fit sources |
| single | select | 0.549 | 0.482 | 0.64 | not met | 0.5/min budget is not met at the point rate; upper95 does not establish the budget | all fit sources |

Per key, beside the per-key share:

| mode | set | key | share/min | weighted/min | pooled/min | weighted upper95 | pooled upper95 | point within share | upper95 within share | valid units |
|---|---|---|---|---|---|---|---|---|---|---|
| consensus5 | fit | D1+ | 0.0833 | 0.0817 | 0.079 | 0.116 | 0.102 | True | False | 67262 |
| consensus5 | fit | D1- | 0.0833 | 0.0752 | 0.0571 | 0.126 | 0.0784 | True | False | 67262 |
| consensus5 | fit | D2+ | 0.0833 | 0.075 | 0.079 | 0.109 | 0.108 | True | False | 3478 |
| consensus5 | fit | D2- | 0.0833 | 0.0753 | 0.0615 | 0.112 | 0.0832 | True | False | 3478 |
| consensus5 | fit | D3- | 0.0833 | 0.0791 | 0.0944 | 0.118 | 0.134 | True | False | 61066 |
| consensus5 | fit | D5- | 0.0833 | 0.0819 | 0.0856 | 0.112 | 0.111 | True | False | 67262 |
| consensus5 | select | D1+ | 0.0833 | 0.141 | 0.121 | 0.197 | 0.157 | False | False | 33585 |
| consensus5 | select | D1- | 0.0833 | 0.0787 | 0.0627 | 0.126 | 0.0964 | True | False | 33585 |
| consensus5 | select | D2+ | 0.0833 | 0.164 | 0.121 | 0.242 | 0.173 | False | False | 1160 |
| consensus5 | select | D2- | 0.0833 | 0.0469 | 0.0193 | 0.0905 | 0.0343 | True | False | 1160 |
| consensus5 | select | D3- | 0.0833 | 0.0307 | 0.0434 | 0.0616 | 0.0834 | True | True | 29930 |
| consensus5 | select | D5- | 0.0833 | 0.0734 | 0.0338 | 0.127 | 0.058 | True | False | 33585 |
| single | fit | D1+ | 0.0833 | 0.0826 | 0.0702 | 0.106 | 0.0876 | True | False | 336310 |
| single | fit | D1- | 0.0833 | 0.0812 | 0.0707 | 0.1 | 0.0818 | True | False | 336310 |
| single | fit | D2+ | 0.0833 | 0.0828 | 0.0812 | 0.124 | 0.112 | True | False | 20997 |
| single | fit | D2- | 0.0833 | 0.082 | 0.0487 | 0.12 | 0.0613 | True | False | 20997 |
| single | fit | D3- | 0.0833 | 0.08 | 0.09 | 0.104 | 0.122 | True | False | 290987 |
| single | fit | D5- | 0.0833 | 0.0826 | 0.0891 | 0.106 | 0.107 | True | False | 336310 |
| single | select | D1+ | 0.0833 | 0.127 | 0.109 | 0.164 | 0.136 | False | False | 211940 |
| single | select | D1- | 0.0833 | 0.103 | 0.094 | 0.127 | 0.114 | False | False | 211940 |
| single | select | D2+ | 0.0833 | 0.118 | 0.0955 | 0.164 | 0.131 | False | False | 10383 |
| single | select | D2- | 0.0833 | 0.0497 | 0.0525 | 0.0642 | 0.0671 | True | True | 10383 |
| single | select | D3- | 0.0833 | 0.0491 | 0.0459 | 0.0699 | 0.0677 | True | True | 181892 |
| single | select | D5- | 0.0833 | 0.102 | 0.0846 | 0.138 | 0.111 | False | False | 211940 |

Per source:

| mode | set | key | source | rate/min (texts by comparison-minutes) | pooled/min | flags | comparison-minutes |
|---|---|---|---|---|---|---|---|
| consensus5 | fit | D1+ | accent | 0.132 | 0.132 | 22 | 167 |
| consensus5 | fit | D1+ | ears | 0.0804 | 0.0804 | 9 | 112 |
| consensus5 | fit | D1+ | gettysburg | 0.0952 | 0.0952 | 2 | 21 |
| consensus5 | fit | D1+ | poetry | 0.0193 | 0.0193 | 3 | 156 |
| consensus5 | fit | D1- | accent | 0.0659 | 0.0659 | 11 | 167 |
| consensus5 | fit | D1- | ears | 0.0536 | 0.0536 | 6 | 112 |
| consensus5 | fit | D1- | gettysburg | 0.143 | 0.143 | 3 | 21 |
| consensus5 | fit | D1- | poetry | 0.0385 | 0.0385 | 6 | 156 |
| consensus5 | fit | D2+ | accent | 0.186 | 0.186 | 31 | 167 |
| consensus5 | fit | D2+ | ears | 0 | 0 | 0 | 112 |
| consensus5 | fit | D2+ | gettysburg | 0.0952 | 0.0952 | 2 | 21 |
| consensus5 | fit | D2+ | poetry | 0.0193 | 0.0193 | 3 | 156 |
| consensus5 | fit | D2- | accent | 0.03 | 0.03 | 5 | 167 |
| consensus5 | fit | D2- | ears | 0 | 0 | 0 | 112 |
| consensus5 | fit | D2- | gettysburg | 0.143 | 0.143 | 3 | 21 |
| consensus5 | fit | D2- | poetry | 0.128 | 0.128 | 20 | 156 |
| consensus5 | fit | D3- | accent | 0.15 | 0.15 | 25 | 167 |
| consensus5 | fit | D3- | ears | 0.0357 | 0.0357 | 4 | 112 |
| consensus5 | fit | D3- | gettysburg | 0.0476 | 0.0476 | 1 | 21 |
| consensus5 | fit | D3- | poetry | 0.0835 | 0.0835 | 13 | 156 |
| consensus5 | fit | D5- | accent | 0.108 | 0.108 | 18 | 167 |
| consensus5 | fit | D5- | ears | 0.00893 | 0.00893 | 1 | 112 |
| consensus5 | fit | D5- | gettysburg | 0.0952 | 0.0952 | 2 | 21 |
| consensus5 | fit | D5- | poetry | 0.116 | 0.116 | 18 | 156 |
| consensus5 | fit | total | accent | 0.671 | 0.671 | 112 | 167 |
| consensus5 | fit | total | ears | 0.179 | 0.179 | 20 | 112 |
| consensus5 | fit | total | gettysburg | 0.619 | 0.619 | 13 | 21 |
| consensus5 | fit | total | poetry | 0.405 | 0.405 | 63 | 156 |
| consensus5 | select | D1+ | accent | 0.187 | 0.187 | 15 | 80.4 |
| consensus5 | select | D1+ | ears | 0.0639 | 0.0639 | 7 | 110 |
| consensus5 | select | D1+ | gettysburg | 0.174 | 0.174 | 3 | 17.3 |
| consensus5 | select | D1- | accent | 0.0747 | 0.0747 | 6 | 80.4 |
| consensus5 | select | D1- | ears | 0.0456 | 0.0456 | 5 | 110 |
| consensus5 | select | D1- | gettysburg | 0.116 | 0.116 | 2 | 17.3 |
| consensus5 | select | D2+ | accent | 0.261 | 0.261 | 21 | 80.4 |
| consensus5 | select | D2+ | ears | 0 | 0 | 0 | 110 |
| consensus5 | select | D2+ | gettysburg | 0.232 | 0.232 | 4 | 17.3 |
| consensus5 | select | D2- | accent | 0.0249 | 0.0249 | 2 | 80.4 |
| consensus5 | select | D2- | ears | 0 | 0 | 0 | 110 |
| consensus5 | select | D2- | gettysburg | 0.116 | 0.116 | 2 | 17.3 |
| consensus5 | select | D3- | accent | 0.0373 | 0.0373 | 3 | 80.4 |
| consensus5 | select | D3- | ears | 0.0547 | 0.0547 | 6 | 110 |
| consensus5 | select | D3- | gettysburg | 0 | 0 | 0 | 17.3 |
| consensus5 | select | D5- | accent | 0.0373 | 0.0373 | 3 | 80.4 |
| consensus5 | select | D5- | ears | 0.00912 | 0.00912 | 1 | 110 |
| consensus5 | select | D5- | gettysburg | 0.174 | 0.174 | 3 | 17.3 |
| consensus5 | select | total | accent | 0.622 | 0.622 | 50 | 80.4 |
| consensus5 | select | total | ears | 0.173 | 0.173 | 19 | 110 |
| consensus5 | select | total | gettysburg | 0.811 | 0.811 | 14 | 17.3 |
| single | fit | D1+ | accent | 0.0887 | 0.0887 | 74 | 835 |
| single | fit | D1+ | ears | 0.0858 | 0.0858 | 48 | 560 |
| single | fit | D1+ | gettysburg | 0.124 | 0.124 | 13 | 105 |
| single | fit | D1+ | poetry | 0.0321 | 0.0321 | 25 | 778 |
| single | fit | D1- | accent | 0.103 | 0.103 | 86 | 835 |
| single | fit | D1- | ears | 0.0661 | 0.0661 | 37 | 560 |
| single | fit | D1- | gettysburg | 0.124 | 0.124 | 13 | 105 |
| single | fit | D1- | poetry | 0.0321 | 0.0321 | 25 | 778 |
| single | fit | D2+ | accent | 0.187 | 0.187 | 156 | 835 |
| single | fit | D2+ | ears | 0 | 0 | 0 | 560 |
| single | fit | D2+ | gettysburg | 0.124 | 0.124 | 13 | 105 |
| single | fit | D2+ | poetry | 0.0206 | 0.0206 | 16 | 778 |
| single | fit | D2- | accent | 0.0551 | 0.0551 | 46 | 835 |
| single | fit | D2- | ears | 0 | 0 | 0 | 560 |
| single | fit | D2- | gettysburg | 0.219 | 0.219 | 23 | 105 |
| single | fit | D2- | poetry | 0.054 | 0.054 | 42 | 778 |
| single | fit | D3- | accent | 0.138 | 0.138 | 115 | 835 |
| single | fit | D3- | ears | 0.0322 | 0.0322 | 18 | 560 |
| single | fit | D3- | gettysburg | 0.0666 | 0.0666 | 7 | 105 |
| single | fit | D3- | poetry | 0.0835 | 0.0835 | 65 | 778 |
| single | fit | D5- | accent | 0.104 | 0.104 | 87 | 835 |
| single | fit | D5- | ears | 0.0107 | 0.0107 | 6 | 560 |
| single | fit | D5- | gettysburg | 0.0856 | 0.0856 | 9 | 105 |
| single | fit | D5- | poetry | 0.13 | 0.13 | 101 | 778 |
| single | fit | total | accent | 0.676 | 0.676 | 564 | 835 |
| single | fit | total | ears | 0.195 | 0.195 | 109 | 560 |
| single | fit | total | gettysburg | 0.742 | 0.742 | 78 | 105 |
| single | fit | total | poetry | 0.352 | 0.352 | 274 | 778 |
| single | select | D1+ | accent | 0.207 | 0.207 | 83 | 402 |
| single | select | D1+ | ears | 0.0547 | 0.0547 | 30 | 548 |
| single | select | D1+ | gettysburg | 0.185 | 0.185 | 16 | 86.3 |
| single | select | D1+ | poetry | 0.0626 | 0.0626 | 21 | 336 |
| single | select | D1- | accent | 0.164 | 0.164 | 66 | 402 |
| single | select | D1- | ears | 0.0529 | 0.0529 | 29 | 548 |
| single | select | D1- | gettysburg | 0.127 | 0.127 | 11 | 86.3 |
| single | select | D1- | poetry | 0.0685 | 0.0685 | 23 | 336 |
| single | select | D2+ | accent | 0.239 | 0.239 | 96 | 402 |
| single | select | D2+ | ears | 0 | 0 | 0 | 548 |
| single | select | D2+ | gettysburg | 0.174 | 0.174 | 15 | 86.3 |
| single | select | D2+ | poetry | 0.0596 | 0.0596 | 20 | 336 |
| single | select | D2- | accent | 0.124 | 0.124 | 50 | 402 |
| single | select | D2- | ears | 0 | 0 | 0 | 548 |
| single | select | D2- | gettysburg | 0.0116 | 0.0116 | 1 | 86.3 |
| single | select | D2- | poetry | 0.0626 | 0.0626 | 21 | 336 |
| single | select | D3- | accent | 0.0224 | 0.0224 | 9 | 402 |
| single | select | D3- | ears | 0.0474 | 0.0474 | 26 | 548 |
| single | select | D3- | gettysburg | 0.0579 | 0.0579 | 5 | 86.3 |
| single | select | D3- | poetry | 0.0685 | 0.0685 | 23 | 336 |
| single | select | D5- | accent | 0.0572 | 0.0572 | 23 | 402 |
| single | select | D5- | ears | 0.0474 | 0.0474 | 26 | 548 |
| single | select | D5- | gettysburg | 0.139 | 0.139 | 12 | 86.3 |
| single | select | D5- | poetry | 0.164 | 0.164 | 55 | 336 |
| single | select | total | accent | 0.814 | 0.814 | 327 | 402 |
| single | select | total | ears | 0.203 | 0.203 | 111 | 548 |
| single | select | total | gettysburg | 0.695 | 0.695 | 60 | 86.3 |
| single | select | total | poetry | 0.486 | 0.486 | 163 | 336 |

Per participant first language (Accent Archive readers):

| mode | set | key | L1 | readers | flags | comparison-minutes | rate/min | 95% CI (reader clusters; none for zero events) |
|---|---|---|---|---|---|---|---|---|
| consensus5 | fit | D1+ | afrikaans | 3 | 0 | 1.18 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | agni | 1 | 0 | 0.585 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | akan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | albanian | 5 | 1 | 2.04 | 0.491 | [0, 1.32] |
| consensus5 | fit | D1+ | amazigh | 1 | 0 | 0.385 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | amharic | 10 | 0 | 5.25 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | arabic | 51 | 10 | 29.5 | 0.339 | [0.164, 0.547] |
| consensus5 | fit | D1+ | armenian | 4 | 1 | 2.08 | 0.481 | [0, 1.35] |
| consensus5 | fit | D1+ | ashanti | 1 | 0 | 0.389 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | azerbaijani | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | bafang | 1 | 0 | 0.612 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | baga | 1 | 0 | 0.703 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | bai | 1 | 0 | 1.01 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | bambara | 3 | 0 | 1.6 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | bamun | 1 | 0 | 0.531 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | bari | 1 | 1 | 0.421 | 2.37 | [n/a, n/a] |
| consensus5 | fit | D1+ | basque | 1 | 1 | 1.08 | 0.93 | [n/a, n/a] |
| consensus5 | fit | D1+ | bavarian | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | belarusan | 1 | 0 | 0.423 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | bengali | 9 | 0 | 4.13 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | bosnian | 5 | 0 | 2.34 | 0 | [n/a, n/a] |
| consensus5 | fit | D1+ | bulgarian | 1 | 1 | 0.552 | 1.81 | [n/a, n/a] |
| consensus5 | fit | D1+ | english | 290 | 7 | 111 | 0.0632 | [0.018, 0.119] |
| consensus5 | fit | D1- | afrikaans | 3 | 0 | 1.18 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | agni | 1 | 0 | 0.585 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | akan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | albanian | 5 | 0 | 2.04 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | amazigh | 1 | 0 | 0.385 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | amharic | 10 | 2 | 5.25 | 0.381 | [0, 1.09] |
| consensus5 | fit | D1- | arabic | 51 | 6 | 29.5 | 0.203 | [0.0349, 0.41] |
| consensus5 | fit | D1- | armenian | 4 | 0 | 2.08 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | ashanti | 1 | 0 | 0.389 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | azerbaijani | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | bafang | 1 | 0 | 0.612 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | baga | 1 | 0 | 0.703 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | bai | 1 | 0 | 1.01 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | bambara | 3 | 0 | 1.6 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | bamun | 1 | 0 | 0.531 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | bari | 1 | 0 | 0.421 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | basque | 1 | 0 | 1.08 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | bavarian | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | belarusan | 1 | 0 | 0.423 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | bengali | 9 | 0 | 4.13 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | bosnian | 5 | 0 | 2.34 | 0 | [n/a, n/a] |
| consensus5 | fit | D1- | bulgarian | 1 | 2 | 0.552 | 3.62 | [n/a, n/a] |
| consensus5 | fit | D1- | english | 290 | 1 | 111 | 0.00903 | [0, 0.0273] |
| consensus5 | fit | D2+ | afrikaans | 3 | 0 | 1.18 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | agni | 1 | 0 | 0.585 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | akan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | albanian | 5 | 1 | 2.04 | 0.491 | [0, 1.32] |
| consensus5 | fit | D2+ | amazigh | 1 | 0 | 0.385 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | amharic | 10 | 1 | 5.25 | 0.191 | [0, 0.547] |
| consensus5 | fit | D2+ | arabic | 51 | 21 | 29.5 | 0.712 | [0.388, 1.07] |
| consensus5 | fit | D2+ | armenian | 4 | 0 | 2.08 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | ashanti | 1 | 0 | 0.389 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | azerbaijani | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | bafang | 1 | 0 | 0.612 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | baga | 1 | 0 | 0.703 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | bai | 1 | 2 | 1.01 | 1.97 | [n/a, n/a] |
| consensus5 | fit | D2+ | bambara | 3 | 0 | 1.6 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | bamun | 1 | 1 | 0.531 | 1.88 | [n/a, n/a] |
| consensus5 | fit | D2+ | bari | 1 | 0 | 0.421 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | basque | 1 | 1 | 1.08 | 0.93 | [n/a, n/a] |
| consensus5 | fit | D2+ | bavarian | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | belarusan | 1 | 1 | 0.423 | 2.37 | [n/a, n/a] |
| consensus5 | fit | D2+ | bengali | 9 | 1 | 4.13 | 0.242 | [0, 0.702] |
| consensus5 | fit | D2+ | bosnian | 5 | 0 | 2.34 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | bulgarian | 1 | 0 | 0.552 | 0 | [n/a, n/a] |
| consensus5 | fit | D2+ | english | 290 | 2 | 111 | 0.0181 | [0, 0.0454] |
| consensus5 | fit | D2- | afrikaans | 3 | 0 | 1.18 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | agni | 1 | 0 | 0.585 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | akan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | albanian | 5 | 0 | 2.04 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | amazigh | 1 | 0 | 0.385 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | amharic | 10 | 0 | 5.25 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | arabic | 51 | 2 | 29.5 | 0.0678 | [0, 0.215] |
| consensus5 | fit | D2- | armenian | 4 | 0 | 2.08 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | ashanti | 1 | 0 | 0.389 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | azerbaijani | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | bafang | 1 | 0 | 0.612 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | baga | 1 | 0 | 0.703 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | bai | 1 | 0 | 1.01 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | bambara | 3 | 0 | 1.6 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | bamun | 1 | 0 | 0.531 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | bari | 1 | 0 | 0.421 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | basque | 1 | 0 | 1.08 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | bavarian | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | belarusan | 1 | 0 | 0.423 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | bengali | 9 | 0 | 4.13 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | bosnian | 5 | 0 | 2.34 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | bulgarian | 1 | 0 | 0.552 | 0 | [n/a, n/a] |
| consensus5 | fit | D2- | english | 290 | 3 | 111 | 0.0271 | [0, 0.0721] |
| consensus5 | fit | D3- | afrikaans | 3 | 0 | 1.18 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | agni | 1 | 0 | 0.585 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | akan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | albanian | 5 | 0 | 2.04 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | amazigh | 1 | 0 | 0.385 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | amharic | 10 | 1 | 5.25 | 0.191 | [0, 0.628] |
| consensus5 | fit | D3- | arabic | 51 | 1 | 29.5 | 0.0339 | [0, 0.105] |
| consensus5 | fit | D3- | armenian | 4 | 0 | 2.08 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | ashanti | 1 | 0 | 0.389 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | azerbaijani | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | bafang | 1 | 0 | 0.612 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | baga | 1 | 0 | 0.703 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | bai | 1 | 0 | 1.01 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | bambara | 3 | 0 | 1.6 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | bamun | 1 | 0 | 0.531 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | bari | 1 | 0 | 0.421 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | basque | 1 | 0 | 1.08 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | bavarian | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | belarusan | 1 | 0 | 0.423 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | bengali | 9 | 5 | 4.13 | 1.21 | [0, 3.39] |
| consensus5 | fit | D3- | bosnian | 5 | 0 | 2.34 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | bulgarian | 1 | 0 | 0.552 | 0 | [n/a, n/a] |
| consensus5 | fit | D3- | english | 290 | 18 | 111 | 0.163 | [0.0632, 0.283] |
| consensus5 | fit | D5- | afrikaans | 3 | 0 | 1.18 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | agni | 1 | 0 | 0.585 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | akan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | albanian | 5 | 0 | 2.04 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | amazigh | 1 | 0 | 0.385 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | amharic | 10 | 0 | 5.25 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | arabic | 51 | 5 | 29.5 | 0.169 | [0, 0.378] |
| consensus5 | fit | D5- | armenian | 4 | 0 | 2.08 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | ashanti | 1 | 0 | 0.389 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | azerbaijani | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | bafang | 1 | 0 | 0.612 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | baga | 1 | 0 | 0.703 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | bai | 1 | 3 | 1.01 | 2.96 | [n/a, n/a] |
| consensus5 | fit | D5- | bambara | 3 | 0 | 1.6 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | bamun | 1 | 0 | 0.531 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | bari | 1 | 0 | 0.421 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | basque | 1 | 0 | 1.08 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | bavarian | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | belarusan | 1 | 0 | 0.423 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | bengali | 9 | 3 | 4.13 | 0.726 | [0, 1.98] |
| consensus5 | fit | D5- | bosnian | 5 | 0 | 2.34 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | bulgarian | 1 | 0 | 0.552 | 0 | [n/a, n/a] |
| consensus5 | fit | D5- | english | 290 | 7 | 111 | 0.0632 | [0.0181, 0.11] |
| consensus5 | fit | total | afrikaans | 3 | 0 | 1.18 | 0 | [n/a, n/a] |
| consensus5 | fit | total | agni | 1 | 0 | 0.585 | 0 | [n/a, n/a] |
| consensus5 | fit | total | akan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | fit | total | albanian | 5 | 2 | 2.04 | 0.982 | [0, 2.65] |
| consensus5 | fit | total | amazigh | 1 | 0 | 0.385 | 0 | [n/a, n/a] |
| consensus5 | fit | total | amharic | 10 | 4 | 5.25 | 0.762 | [0, 1.86] |
| consensus5 | fit | total | arabic | 51 | 45 | 29.5 | 1.52 | [0.975, 2.13] |
| consensus5 | fit | total | armenian | 4 | 1 | 2.08 | 0.481 | [0, 1.35] |
| consensus5 | fit | total | ashanti | 1 | 0 | 0.389 | 0 | [n/a, n/a] |
| consensus5 | fit | total | azerbaijani | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | fit | total | bafang | 1 | 0 | 0.612 | 0 | [n/a, n/a] |
| consensus5 | fit | total | baga | 1 | 0 | 0.703 | 0 | [n/a, n/a] |
| consensus5 | fit | total | bai | 1 | 5 | 1.01 | 4.94 | [n/a, n/a] |
| consensus5 | fit | total | bambara | 3 | 0 | 1.6 | 0 | [n/a, n/a] |
| consensus5 | fit | total | bamun | 1 | 1 | 0.531 | 1.88 | [n/a, n/a] |
| consensus5 | fit | total | bari | 1 | 1 | 0.421 | 2.37 | [n/a, n/a] |
| consensus5 | fit | total | basque | 1 | 2 | 1.08 | 1.86 | [n/a, n/a] |
| consensus5 | fit | total | bavarian | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | fit | total | belarusan | 1 | 1 | 0.423 | 2.37 | [n/a, n/a] |
| consensus5 | fit | total | bengali | 9 | 9 | 4.13 | 2.18 | [0.466, 4.31] |
| consensus5 | fit | total | bosnian | 5 | 0 | 2.34 | 0 | [n/a, n/a] |
| consensus5 | fit | total | bulgarian | 1 | 3 | 0.552 | 5.43 | [n/a, n/a] |
| consensus5 | fit | total | english | 290 | 38 | 111 | 0.343 | [0.206, 0.486] |
| consensus5 | select | D1+ | afrikaans | 1 | 0 | 0.366 | 0 | [n/a, n/a] |
| consensus5 | select | D1+ | albanian | 2 | 2 | 1.12 | 1.79 | [1.6, 2.02] |
| consensus5 | select | D1+ | amazigh | 1 | 0 | 0.711 | 0 | [n/a, n/a] |
| consensus5 | select | D1+ | amharic | 5 | 2 | 3.09 | 0.647 | [0, 1.42] |
| consensus5 | select | D1+ | arabic | 25 | 5 | 13.8 | 0.363 | [0.131, 0.658] |
| consensus5 | select | D1+ | armenian | 2 | 0 | 0.665 | 0 | [n/a, n/a] |
| consensus5 | select | D1+ | azerbaijani | 1 | 0 | 0.487 | 0 | [n/a, n/a] |
| consensus5 | select | D1+ | bafang | 1 | 0 | 0.679 | 0 | [n/a, n/a] |
| consensus5 | select | D1+ | bambara | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | select | D1+ | basque | 1 | 0 | 0.554 | 0 | [n/a, n/a] |
| consensus5 | select | D1+ | belarusan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | select | D1+ | bengali | 4 | 0 | 2.19 | 0 | [n/a, n/a] |
| consensus5 | select | D1+ | bosnian | 2 | 1 | 0.777 | 1.29 | [0, 2.26] |
| consensus5 | select | D1+ | bulgarian | 1 | 0 | 0.435 | 0 | [n/a, n/a] |
| consensus5 | select | D1+ | english | 145 | 5 | 54.5 | 0.0917 | [0.0185, 0.18] |
| consensus5 | select | D1- | afrikaans | 1 | 0 | 0.366 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | albanian | 2 | 0 | 1.12 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | amazigh | 1 | 0 | 0.711 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | amharic | 5 | 0 | 3.09 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | arabic | 25 | 0 | 13.8 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | armenian | 2 | 0 | 0.665 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | azerbaijani | 1 | 0 | 0.487 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | bafang | 1 | 0 | 0.679 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | bambara | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | basque | 1 | 0 | 0.554 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | belarusan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | bengali | 4 | 0 | 2.19 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | bosnian | 2 | 0 | 0.777 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | bulgarian | 1 | 0 | 0.435 | 0 | [n/a, n/a] |
| consensus5 | select | D1- | english | 145 | 6 | 54.5 | 0.11 | [0.018, 0.256] |
| consensus5 | select | D2+ | afrikaans | 1 | 0 | 0.366 | 0 | [n/a, n/a] |
| consensus5 | select | D2+ | albanian | 2 | 2 | 1.12 | 1.79 | [1.6, 2.02] |
| consensus5 | select | D2+ | amazigh | 1 | 3 | 0.711 | 4.22 | [n/a, n/a] |
| consensus5 | select | D2+ | amharic | 5 | 4 | 3.09 | 1.29 | [0.381, 1.97] |
| consensus5 | select | D2+ | arabic | 25 | 8 | 13.8 | 0.581 | [0.0882, 1.2] |
| consensus5 | select | D2+ | armenian | 2 | 0 | 0.665 | 0 | [n/a, n/a] |
| consensus5 | select | D2+ | azerbaijani | 1 | 1 | 0.487 | 2.05 | [n/a, n/a] |
| consensus5 | select | D2+ | bafang | 1 | 0 | 0.679 | 0 | [n/a, n/a] |
| consensus5 | select | D2+ | bambara | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | select | D2+ | basque | 1 | 0 | 0.554 | 0 | [n/a, n/a] |
| consensus5 | select | D2+ | belarusan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | select | D2+ | bengali | 4 | 2 | 2.19 | 0.912 | [0, 2.95] |
| consensus5 | select | D2+ | bosnian | 2 | 0 | 0.777 | 0 | [n/a, n/a] |
| consensus5 | select | D2+ | bulgarian | 1 | 0 | 0.435 | 0 | [n/a, n/a] |
| consensus5 | select | D2+ | english | 145 | 1 | 54.5 | 0.0183 | [0, 0.0558] |
| consensus5 | select | D2- | afrikaans | 1 | 0 | 0.366 | 0 | [n/a, n/a] |
| consensus5 | select | D2- | albanian | 2 | 0 | 1.12 | 0 | [n/a, n/a] |
| consensus5 | select | D2- | amazigh | 1 | 0 | 0.711 | 0 | [n/a, n/a] |
| consensus5 | select | D2- | amharic | 5 | 0 | 3.09 | 0 | [n/a, n/a] |
| consensus5 | select | D2- | arabic | 25 | 0 | 13.8 | 0 | [n/a, n/a] |
| consensus5 | select | D2- | armenian | 2 | 2 | 0.665 | 3.01 | [2.48, 3.81] |
| consensus5 | select | D2- | azerbaijani | 1 | 0 | 0.487 | 0 | [n/a, n/a] |
| consensus5 | select | D2- | bafang | 1 | 0 | 0.679 | 0 | [n/a, n/a] |
| consensus5 | select | D2- | bambara | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | select | D2- | basque | 1 | 0 | 0.554 | 0 | [n/a, n/a] |
| consensus5 | select | D2- | belarusan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | select | D2- | bengali | 4 | 0 | 2.19 | 0 | [n/a, n/a] |
| consensus5 | select | D2- | bosnian | 2 | 0 | 0.777 | 0 | [n/a, n/a] |
| consensus5 | select | D2- | bulgarian | 1 | 0 | 0.435 | 0 | [n/a, n/a] |
| consensus5 | select | D2- | english | 145 | 0 | 54.5 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | afrikaans | 1 | 0 | 0.366 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | albanian | 2 | 0 | 1.12 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | amazigh | 1 | 0 | 0.711 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | amharic | 5 | 0 | 3.09 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | arabic | 25 | 0 | 13.8 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | armenian | 2 | 0 | 0.665 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | azerbaijani | 1 | 0 | 0.487 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | bafang | 1 | 0 | 0.679 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | bambara | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | basque | 1 | 0 | 0.554 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | belarusan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | bengali | 4 | 0 | 2.19 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | bosnian | 2 | 0 | 0.777 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | bulgarian | 1 | 0 | 0.435 | 0 | [n/a, n/a] |
| consensus5 | select | D3- | english | 145 | 3 | 54.5 | 0.055 | [0, 0.167] |
| consensus5 | select | D5- | afrikaans | 1 | 0 | 0.366 | 0 | [n/a, n/a] |
| consensus5 | select | D5- | albanian | 2 | 0 | 1.12 | 0 | [n/a, n/a] |
| consensus5 | select | D5- | amazigh | 1 | 0 | 0.711 | 0 | [n/a, n/a] |
| consensus5 | select | D5- | amharic | 5 | 0 | 3.09 | 0 | [n/a, n/a] |
| consensus5 | select | D5- | arabic | 25 | 0 | 13.8 | 0 | [n/a, n/a] |
| consensus5 | select | D5- | armenian | 2 | 0 | 0.665 | 0 | [n/a, n/a] |
| consensus5 | select | D5- | azerbaijani | 1 | 2 | 0.487 | 4.11 | [n/a, n/a] |
| consensus5 | select | D5- | bafang | 1 | 0 | 0.679 | 0 | [n/a, n/a] |
| consensus5 | select | D5- | bambara | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | select | D5- | basque | 1 | 0 | 0.554 | 0 | [n/a, n/a] |
| consensus5 | select | D5- | belarusan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | select | D5- | bengali | 4 | 0 | 2.19 | 0 | [n/a, n/a] |
| consensus5 | select | D5- | bosnian | 2 | 0 | 0.777 | 0 | [n/a, n/a] |
| consensus5 | select | D5- | bulgarian | 1 | 0 | 0.435 | 0 | [n/a, n/a] |
| consensus5 | select | D5- | english | 145 | 1 | 54.5 | 0.0183 | [0, 0.0554] |
| consensus5 | select | total | afrikaans | 1 | 0 | 0.366 | 0 | [n/a, n/a] |
| consensus5 | select | total | albanian | 2 | 4 | 1.12 | 3.58 | [3.21, 4.04] |
| consensus5 | select | total | amazigh | 1 | 3 | 0.711 | 4.22 | [n/a, n/a] |
| consensus5 | select | total | amharic | 5 | 6 | 3.09 | 1.94 | [0.796, 2.85] |
| consensus5 | select | total | arabic | 25 | 13 | 13.8 | 0.944 | [0.325, 1.6] |
| consensus5 | select | total | armenian | 2 | 2 | 0.665 | 3.01 | [2.48, 3.81] |
| consensus5 | select | total | azerbaijani | 1 | 3 | 0.487 | 6.16 | [n/a, n/a] |
| consensus5 | select | total | bafang | 1 | 0 | 0.679 | 0 | [n/a, n/a] |
| consensus5 | select | total | bambara | 1 | 0 | 0.545 | 0 | [n/a, n/a] |
| consensus5 | select | total | basque | 1 | 0 | 0.554 | 0 | [n/a, n/a] |
| consensus5 | select | total | belarusan | 1 | 0 | 0.42 | 0 | [n/a, n/a] |
| consensus5 | select | total | bengali | 4 | 2 | 2.19 | 0.912 | [0, 2.95] |
| consensus5 | select | total | bosnian | 2 | 1 | 0.777 | 1.29 | [0, 2.26] |
| consensus5 | select | total | bulgarian | 1 | 0 | 0.435 | 0 | [n/a, n/a] |
| consensus5 | select | total | english | 145 | 16 | 54.5 | 0.293 | [0.111, 0.487] |
| single | fit | D1+ | afrikaans | 3 | 0 | 5.88 | 0 | [n/a, n/a] |
| single | fit | D1+ | agni | 1 | 0 | 2.92 | 0 | [n/a, n/a] |
| single | fit | D1+ | akan | 1 | 0 | 2.1 | 0 | [n/a, n/a] |
| single | fit | D1+ | albanian | 5 | 4 | 10.2 | 0.393 | [0, 1.06] |
| single | fit | D1+ | amazigh | 1 | 0 | 1.93 | 0 | [n/a, n/a] |
| single | fit | D1+ | amharic | 10 | 0 | 26.2 | 0 | [n/a, n/a] |
| single | fit | D1+ | arabic | 51 | 36 | 148 | 0.244 | [0.111, 0.386] |
| single | fit | D1+ | armenian | 4 | 5 | 10.4 | 0.481 | [0, 1.35] |
| single | fit | D1+ | ashanti | 1 | 0 | 1.95 | 0 | [n/a, n/a] |
| single | fit | D1+ | azerbaijani | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | fit | D1+ | bafang | 1 | 0 | 3.06 | 0 | [n/a, n/a] |
| single | fit | D1+ | baga | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | fit | D1+ | bai | 1 | 0 | 5.07 | 0 | [n/a, n/a] |
| single | fit | D1+ | bambara | 3 | 0 | 8 | 0 | [n/a, n/a] |
| single | fit | D1+ | bamun | 1 | 0 | 2.66 | 0 | [n/a, n/a] |
| single | fit | D1+ | bari | 1 | 4 | 2.11 | 1.9 | [n/a, n/a] |
| single | fit | D1+ | basque | 1 | 1 | 5.38 | 0.186 | [n/a, n/a] |
| single | fit | D1+ | bavarian | 1 | 0 | 2.72 | 0 | [n/a, n/a] |
| single | fit | D1+ | belarusan | 1 | 0 | 2.11 | 0 | [n/a, n/a] |
| single | fit | D1+ | bengali | 9 | 0 | 20.7 | 0 | [n/a, n/a] |
| single | fit | D1+ | bosnian | 5 | 2 | 11.7 | 0.171 | [0, 0.335] |
| single | fit | D1+ | bulgarian | 1 | 1 | 2.76 | 0.362 | [n/a, n/a] |
| single | fit | D1+ | english | 290 | 21 | 554 | 0.0379 | [0.00907, 0.085] |
| single | fit | D1- | afrikaans | 3 | 0 | 5.88 | 0 | [n/a, n/a] |
| single | fit | D1- | agni | 1 | 0 | 2.92 | 0 | [n/a, n/a] |
| single | fit | D1- | akan | 1 | 1 | 2.1 | 0.476 | [n/a, n/a] |
| single | fit | D1- | albanian | 5 | 1 | 10.2 | 0.0982 | [0, 0.322] |
| single | fit | D1- | amazigh | 1 | 0 | 1.93 | 0 | [n/a, n/a] |
| single | fit | D1- | amharic | 10 | 3 | 26.2 | 0.114 | [0, 0.245] |
| single | fit | D1- | arabic | 51 | 12 | 148 | 0.0813 | [0.0319, 0.136] |
| single | fit | D1- | armenian | 4 | 1 | 10.4 | 0.0963 | [0, 0.274] |
| single | fit | D1- | ashanti | 1 | 0 | 1.95 | 0 | [n/a, n/a] |
| single | fit | D1- | azerbaijani | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | fit | D1- | bafang | 1 | 1 | 3.06 | 0.327 | [n/a, n/a] |
| single | fit | D1- | baga | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | fit | D1- | bai | 1 | 1 | 5.07 | 0.197 | [n/a, n/a] |
| single | fit | D1- | bambara | 3 | 1 | 8 | 0.125 | [0, 0.349] |
| single | fit | D1- | bamun | 1 | 0 | 2.66 | 0 | [n/a, n/a] |
| single | fit | D1- | bari | 1 | 0 | 2.11 | 0 | [n/a, n/a] |
| single | fit | D1- | basque | 1 | 0 | 5.38 | 0 | [n/a, n/a] |
| single | fit | D1- | bavarian | 1 | 0 | 2.72 | 0 | [n/a, n/a] |
| single | fit | D1- | belarusan | 1 | 0 | 2.11 | 0 | [n/a, n/a] |
| single | fit | D1- | bengali | 9 | 1 | 20.7 | 0.0484 | [0, 0.136] |
| single | fit | D1- | bosnian | 5 | 2 | 11.7 | 0.171 | [0, 0.59] |
| single | fit | D1- | bulgarian | 1 | 4 | 2.76 | 1.45 | [n/a, n/a] |
| single | fit | D1- | english | 290 | 58 | 554 | 0.105 | [0.0779, 0.133] |
| single | fit | D2+ | afrikaans | 3 | 0 | 5.88 | 0 | [n/a, n/a] |
| single | fit | D2+ | agni | 1 | 0 | 2.92 | 0 | [n/a, n/a] |
| single | fit | D2+ | akan | 1 | 0 | 2.1 | 0 | [n/a, n/a] |
| single | fit | D2+ | albanian | 5 | 5 | 10.2 | 0.491 | [0, 1.32] |
| single | fit | D2+ | amazigh | 1 | 0 | 1.93 | 0 | [n/a, n/a] |
| single | fit | D2+ | amharic | 10 | 5 | 26.2 | 0.191 | [0, 0.547] |
| single | fit | D2+ | arabic | 51 | 113 | 148 | 0.766 | [0.42, 1.15] |
| single | fit | D2+ | armenian | 4 | 0 | 10.4 | 0 | [n/a, n/a] |
| single | fit | D2+ | ashanti | 1 | 0 | 1.95 | 0 | [n/a, n/a] |
| single | fit | D2+ | azerbaijani | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | fit | D2+ | bafang | 1 | 0 | 3.06 | 0 | [n/a, n/a] |
| single | fit | D2+ | baga | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | fit | D2+ | bai | 1 | 7 | 5.07 | 1.38 | [n/a, n/a] |
| single | fit | D2+ | bambara | 3 | 0 | 8 | 0 | [n/a, n/a] |
| single | fit | D2+ | bamun | 1 | 5 | 2.66 | 1.88 | [n/a, n/a] |
| single | fit | D2+ | bari | 1 | 0 | 2.11 | 0 | [n/a, n/a] |
| single | fit | D2+ | basque | 1 | 5 | 5.38 | 0.93 | [n/a, n/a] |
| single | fit | D2+ | bavarian | 1 | 0 | 2.72 | 0 | [n/a, n/a] |
| single | fit | D2+ | belarusan | 1 | 3 | 2.11 | 1.42 | [n/a, n/a] |
| single | fit | D2+ | bengali | 9 | 5 | 20.7 | 0.242 | [0, 0.702] |
| single | fit | D2+ | bosnian | 5 | 0 | 11.7 | 0 | [n/a, n/a] |
| single | fit | D2+ | bulgarian | 1 | 0 | 2.76 | 0 | [n/a, n/a] |
| single | fit | D2+ | english | 290 | 8 | 554 | 0.0144 | [0, 0.0363] |
| single | fit | D2- | afrikaans | 3 | 0 | 5.88 | 0 | [n/a, n/a] |
| single | fit | D2- | agni | 1 | 0 | 2.92 | 0 | [n/a, n/a] |
| single | fit | D2- | akan | 1 | 0 | 2.1 | 0 | [n/a, n/a] |
| single | fit | D2- | albanian | 5 | 0 | 10.2 | 0 | [n/a, n/a] |
| single | fit | D2- | amazigh | 1 | 0 | 1.93 | 0 | [n/a, n/a] |
| single | fit | D2- | amharic | 10 | 1 | 26.2 | 0.0381 | [0, 0.113] |
| single | fit | D2- | arabic | 51 | 3 | 148 | 0.0203 | [0, 0.056] |
| single | fit | D2- | armenian | 4 | 0 | 10.4 | 0 | [n/a, n/a] |
| single | fit | D2- | ashanti | 1 | 0 | 1.95 | 0 | [n/a, n/a] |
| single | fit | D2- | azerbaijani | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | fit | D2- | bafang | 1 | 0 | 3.06 | 0 | [n/a, n/a] |
| single | fit | D2- | baga | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | fit | D2- | bai | 1 | 1 | 5.07 | 0.197 | [n/a, n/a] |
| single | fit | D2- | bambara | 3 | 1 | 8 | 0.125 | [0, 0.392] |
| single | fit | D2- | bamun | 1 | 0 | 2.66 | 0 | [n/a, n/a] |
| single | fit | D2- | bari | 1 | 0 | 2.11 | 0 | [n/a, n/a] |
| single | fit | D2- | basque | 1 | 0 | 5.38 | 0 | [n/a, n/a] |
| single | fit | D2- | bavarian | 1 | 0 | 2.72 | 0 | [n/a, n/a] |
| single | fit | D2- | belarusan | 1 | 0 | 2.11 | 0 | [n/a, n/a] |
| single | fit | D2- | bengali | 9 | 2 | 20.7 | 0.0967 | [0, 0.318] |
| single | fit | D2- | bosnian | 5 | 0 | 11.7 | 0 | [n/a, n/a] |
| single | fit | D2- | bulgarian | 1 | 0 | 2.76 | 0 | [n/a, n/a] |
| single | fit | D2- | english | 290 | 38 | 554 | 0.0686 | [0.0431, 0.0999] |
| single | fit | D3- | afrikaans | 3 | 1 | 5.88 | 0.17 | [0, 0.446] |
| single | fit | D3- | agni | 1 | 0 | 2.92 | 0 | [n/a, n/a] |
| single | fit | D3- | akan | 1 | 0 | 2.1 | 0 | [n/a, n/a] |
| single | fit | D3- | albanian | 5 | 0 | 10.2 | 0 | [n/a, n/a] |
| single | fit | D3- | amazigh | 1 | 0 | 1.93 | 0 | [n/a, n/a] |
| single | fit | D3- | amharic | 10 | 5 | 26.2 | 0.191 | [0, 0.477] |
| single | fit | D3- | arabic | 51 | 1 | 148 | 0.00678 | [0, 0.0213] |
| single | fit | D3- | armenian | 4 | 0 | 10.4 | 0 | [n/a, n/a] |
| single | fit | D3- | ashanti | 1 | 0 | 1.95 | 0 | [n/a, n/a] |
| single | fit | D3- | azerbaijani | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | fit | D3- | bafang | 1 | 0 | 3.06 | 0 | [n/a, n/a] |
| single | fit | D3- | baga | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | fit | D3- | bai | 1 | 0 | 5.07 | 0 | [n/a, n/a] |
| single | fit | D3- | bambara | 3 | 0 | 8 | 0 | [n/a, n/a] |
| single | fit | D3- | bamun | 1 | 0 | 2.66 | 0 | [n/a, n/a] |
| single | fit | D3- | bari | 1 | 0 | 2.11 | 0 | [n/a, n/a] |
| single | fit | D3- | basque | 1 | 0 | 5.38 | 0 | [n/a, n/a] |
| single | fit | D3- | bavarian | 1 | 0 | 2.72 | 0 | [n/a, n/a] |
| single | fit | D3- | belarusan | 1 | 1 | 2.11 | 0.473 | [n/a, n/a] |
| single | fit | D3- | bengali | 9 | 23 | 20.7 | 1.11 | [0, 3.12] |
| single | fit | D3- | bosnian | 5 | 0 | 11.7 | 0 | [n/a, n/a] |
| single | fit | D3- | bulgarian | 1 | 0 | 2.76 | 0 | [n/a, n/a] |
| single | fit | D3- | english | 290 | 84 | 554 | 0.152 | [0.0774, 0.247] |
| single | fit | D5- | afrikaans | 3 | 1 | 5.88 | 0.17 | [0, 0.593] |
| single | fit | D5- | agni | 1 | 0 | 2.92 | 0 | [n/a, n/a] |
| single | fit | D5- | akan | 1 | 0 | 2.1 | 0 | [n/a, n/a] |
| single | fit | D5- | albanian | 5 | 1 | 10.2 | 0.0982 | [0, 0.322] |
| single | fit | D5- | amazigh | 1 | 0 | 1.93 | 0 | [n/a, n/a] |
| single | fit | D5- | amharic | 10 | 1 | 26.2 | 0.0381 | [0, 0.116] |
| single | fit | D5- | arabic | 51 | 13 | 148 | 0.0881 | [0.0326, 0.155] |
| single | fit | D5- | armenian | 4 | 0 | 10.4 | 0 | [n/a, n/a] |
| single | fit | D5- | ashanti | 1 | 0 | 1.95 | 0 | [n/a, n/a] |
| single | fit | D5- | azerbaijani | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | fit | D5- | bafang | 1 | 0 | 3.06 | 0 | [n/a, n/a] |
| single | fit | D5- | baga | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | fit | D5- | bai | 1 | 7 | 5.07 | 1.38 | [n/a, n/a] |
| single | fit | D5- | bambara | 3 | 1 | 8 | 0.125 | [0, 0.349] |
| single | fit | D5- | bamun | 1 | 1 | 2.66 | 0.376 | [n/a, n/a] |
| single | fit | D5- | bari | 1 | 0 | 2.11 | 0 | [n/a, n/a] |
| single | fit | D5- | basque | 1 | 0 | 5.38 | 0 | [n/a, n/a] |
| single | fit | D5- | bavarian | 1 | 0 | 2.72 | 0 | [n/a, n/a] |
| single | fit | D5- | belarusan | 1 | 0 | 2.11 | 0 | [n/a, n/a] |
| single | fit | D5- | bengali | 9 | 11 | 20.7 | 0.532 | [0, 1.59] |
| single | fit | D5- | bosnian | 5 | 0 | 11.7 | 0 | [n/a, n/a] |
| single | fit | D5- | bulgarian | 1 | 0 | 2.76 | 0 | [n/a, n/a] |
| single | fit | D5- | english | 290 | 51 | 554 | 0.0921 | [0.0643, 0.123] |
| single | fit | total | afrikaans | 3 | 2 | 5.88 | 0.34 | [0, 0.593] |
| single | fit | total | agni | 1 | 0 | 2.92 | 0 | [n/a, n/a] |
| single | fit | total | akan | 1 | 1 | 2.1 | 0.476 | [n/a, n/a] |
| single | fit | total | albanian | 5 | 11 | 10.2 | 1.08 | [0, 2.56] |
| single | fit | total | amazigh | 1 | 0 | 1.93 | 0 | [n/a, n/a] |
| single | fit | total | amharic | 10 | 15 | 26.2 | 0.572 | [0.236, 0.88] |
| single | fit | total | arabic | 51 | 178 | 148 | 1.21 | [0.793, 1.65] |
| single | fit | total | armenian | 4 | 6 | 10.4 | 0.578 | [0, 1.38] |
| single | fit | total | ashanti | 1 | 0 | 1.95 | 0 | [n/a, n/a] |
| single | fit | total | azerbaijani | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | fit | total | bafang | 1 | 1 | 3.06 | 0.327 | [n/a, n/a] |
| single | fit | total | baga | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | fit | total | bai | 1 | 16 | 5.07 | 3.16 | [n/a, n/a] |
| single | fit | total | bambara | 3 | 3 | 8 | 0.375 | [0, 0.699] |
| single | fit | total | bamun | 1 | 6 | 2.66 | 2.26 | [n/a, n/a] |
| single | fit | total | bari | 1 | 4 | 2.11 | 1.9 | [n/a, n/a] |
| single | fit | total | basque | 1 | 6 | 5.38 | 1.12 | [n/a, n/a] |
| single | fit | total | bavarian | 1 | 0 | 2.72 | 0 | [n/a, n/a] |
| single | fit | total | belarusan | 1 | 4 | 2.11 | 1.89 | [n/a, n/a] |
| single | fit | total | bengali | 9 | 42 | 20.7 | 2.03 | [0.332, 4.12] |
| single | fit | total | bosnian | 5 | 4 | 11.7 | 0.343 | [0.0769, 0.712] |
| single | fit | total | bulgarian | 1 | 5 | 2.76 | 1.81 | [n/a, n/a] |
| single | fit | total | english | 290 | 260 | 554 | 0.47 | [0.368, 0.58] |
| single | select | D1+ | afrikaans | 1 | 0 | 1.83 | 0 | [n/a, n/a] |
| single | select | D1+ | albanian | 2 | 4 | 5.59 | 0.715 | [0.404, 0.962] |
| single | select | D1+ | amazigh | 1 | 0 | 3.56 | 0 | [n/a, n/a] |
| single | select | D1+ | amharic | 5 | 12 | 15.5 | 0.776 | [0.272, 1.3] |
| single | select | D1+ | arabic | 25 | 29 | 68.9 | 0.421 | [0.178, 0.682] |
| single | select | D1+ | armenian | 2 | 1 | 3.33 | 0.301 | [0, 0.497] |
| single | select | D1+ | azerbaijani | 1 | 0 | 2.44 | 0 | [n/a, n/a] |
| single | select | D1+ | bafang | 1 | 0 | 3.4 | 0 | [n/a, n/a] |
| single | select | D1+ | bambara | 1 | 1 | 2.73 | 0.367 | [n/a, n/a] |
| single | select | D1+ | basque | 1 | 0 | 2.77 | 0 | [n/a, n/a] |
| single | select | D1+ | belarusan | 1 | 0 | 2.1 | 0 | [n/a, n/a] |
| single | select | D1+ | bengali | 4 | 3 | 11 | 0.274 | [0, 0.861] |
| single | select | D1+ | bosnian | 2 | 0 | 3.88 | 0 | [n/a, n/a] |
| single | select | D1+ | bulgarian | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | select | D1+ | english | 145 | 33 | 273 | 0.121 | [0.0618, 0.191] |
| single | select | D1- | afrikaans | 1 | 2 | 1.83 | 1.09 | [n/a, n/a] |
| single | select | D1- | albanian | 2 | 1 | 5.59 | 0.179 | [0, 0.404] |
| single | select | D1- | amazigh | 1 | 0 | 3.56 | 0 | [n/a, n/a] |
| single | select | D1- | amharic | 5 | 2 | 15.5 | 0.129 | [0, 0.286] |
| single | select | D1- | arabic | 25 | 5 | 68.9 | 0.0726 | [0.0155, 0.131] |
| single | select | D1- | armenian | 2 | 1 | 3.33 | 0.301 | [0, 0.497] |
| single | select | D1- | azerbaijani | 1 | 0 | 2.44 | 0 | [n/a, n/a] |
| single | select | D1- | bafang | 1 | 0 | 3.4 | 0 | [n/a, n/a] |
| single | select | D1- | bambara | 1 | 1 | 2.73 | 0.367 | [n/a, n/a] |
| single | select | D1- | basque | 1 | 1 | 2.77 | 0.361 | [n/a, n/a] |
| single | select | D1- | belarusan | 1 | 0 | 2.1 | 0 | [n/a, n/a] |
| single | select | D1- | bengali | 4 | 0 | 11 | 0 | [n/a, n/a] |
| single | select | D1- | bosnian | 2 | 0 | 3.88 | 0 | [n/a, n/a] |
| single | select | D1- | bulgarian | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | select | D1- | english | 145 | 53 | 273 | 0.194 | [0.115, 0.307] |
| single | select | D2+ | afrikaans | 1 | 0 | 1.83 | 0 | [n/a, n/a] |
| single | select | D2+ | albanian | 2 | 10 | 5.59 | 1.79 | [1.6, 2.02] |
| single | select | D2+ | amazigh | 1 | 13 | 3.56 | 3.65 | [n/a, n/a] |
| single | select | D2+ | amharic | 5 | 20 | 15.5 | 1.29 | [0.242, 2] |
| single | select | D2+ | arabic | 25 | 36 | 68.9 | 0.523 | [0.125, 1.04] |
| single | select | D2+ | armenian | 2 | 0 | 3.33 | 0 | [n/a, n/a] |
| single | select | D2+ | azerbaijani | 1 | 5 | 2.44 | 2.05 | [n/a, n/a] |
| single | select | D2+ | bafang | 1 | 0 | 3.4 | 0 | [n/a, n/a] |
| single | select | D2+ | bambara | 1 | 0 | 2.73 | 0 | [n/a, n/a] |
| single | select | D2+ | basque | 1 | 0 | 2.77 | 0 | [n/a, n/a] |
| single | select | D2+ | belarusan | 1 | 0 | 2.1 | 0 | [n/a, n/a] |
| single | select | D2+ | bengali | 4 | 8 | 11 | 0.73 | [0, 2.36] |
| single | select | D2+ | bosnian | 2 | 0 | 3.88 | 0 | [n/a, n/a] |
| single | select | D2+ | bulgarian | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | select | D2+ | english | 145 | 4 | 273 | 0.0147 | [0, 0.0446] |
| single | select | D2- | afrikaans | 1 | 0 | 1.83 | 0 | [n/a, n/a] |
| single | select | D2- | albanian | 2 | 0 | 5.59 | 0 | [n/a, n/a] |
| single | select | D2- | amazigh | 1 | 0 | 3.56 | 0 | [n/a, n/a] |
| single | select | D2- | amharic | 5 | 2 | 15.5 | 0.129 | [0, 0.43] |
| single | select | D2- | arabic | 25 | 4 | 68.9 | 0.0581 | [0.0137, 0.114] |
| single | select | D2- | armenian | 2 | 7 | 3.33 | 2.1 | [1.52, 2.48] |
| single | select | D2- | azerbaijani | 1 | 0 | 2.44 | 0 | [n/a, n/a] |
| single | select | D2- | bafang | 1 | 0 | 3.4 | 0 | [n/a, n/a] |
| single | select | D2- | bambara | 1 | 0 | 2.73 | 0 | [n/a, n/a] |
| single | select | D2- | basque | 1 | 1 | 2.77 | 0.361 | [n/a, n/a] |
| single | select | D2- | belarusan | 1 | 2 | 2.1 | 0.953 | [n/a, n/a] |
| single | select | D2- | bengali | 4 | 0 | 11 | 0 | [n/a, n/a] |
| single | select | D2- | bosnian | 2 | 1 | 3.88 | 0.257 | [0, 0.597] |
| single | select | D2- | bulgarian | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | select | D2- | english | 145 | 33 | 273 | 0.121 | [0.0659, 0.182] |
| single | select | D3- | afrikaans | 1 | 0 | 1.83 | 0 | [n/a, n/a] |
| single | select | D3- | albanian | 2 | 0 | 5.59 | 0 | [n/a, n/a] |
| single | select | D3- | amazigh | 1 | 0 | 3.56 | 0 | [n/a, n/a] |
| single | select | D3- | amharic | 5 | 0 | 15.5 | 0 | [n/a, n/a] |
| single | select | D3- | arabic | 25 | 1 | 68.9 | 0.0145 | [0, 0.0465] |
| single | select | D3- | armenian | 2 | 0 | 3.33 | 0 | [n/a, n/a] |
| single | select | D3- | azerbaijani | 1 | 0 | 2.44 | 0 | [n/a, n/a] |
| single | select | D3- | bafang | 1 | 0 | 3.4 | 0 | [n/a, n/a] |
| single | select | D3- | bambara | 1 | 0 | 2.73 | 0 | [n/a, n/a] |
| single | select | D3- | basque | 1 | 0 | 2.77 | 0 | [n/a, n/a] |
| single | select | D3- | belarusan | 1 | 0 | 2.1 | 0 | [n/a, n/a] |
| single | select | D3- | bengali | 4 | 0 | 11 | 0 | [n/a, n/a] |
| single | select | D3- | bosnian | 2 | 0 | 3.88 | 0 | [n/a, n/a] |
| single | select | D3- | bulgarian | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | select | D3- | english | 145 | 8 | 273 | 0.0293 | [0, 0.0761] |
| single | select | D5- | afrikaans | 1 | 0 | 1.83 | 0 | [n/a, n/a] |
| single | select | D5- | albanian | 2 | 0 | 5.59 | 0 | [n/a, n/a] |
| single | select | D5- | amazigh | 1 | 0 | 3.56 | 0 | [n/a, n/a] |
| single | select | D5- | amharic | 5 | 0 | 15.5 | 0 | [n/a, n/a] |
| single | select | D5- | arabic | 25 | 2 | 68.9 | 0.029 | [0, 0.0713] |
| single | select | D5- | armenian | 2 | 0 | 3.33 | 0 | [n/a, n/a] |
| single | select | D5- | azerbaijani | 1 | 4 | 2.44 | 1.64 | [n/a, n/a] |
| single | select | D5- | bafang | 1 | 0 | 3.4 | 0 | [n/a, n/a] |
| single | select | D5- | bambara | 1 | 0 | 2.73 | 0 | [n/a, n/a] |
| single | select | D5- | basque | 1 | 0 | 2.77 | 0 | [n/a, n/a] |
| single | select | D5- | belarusan | 1 | 0 | 2.1 | 0 | [n/a, n/a] |
| single | select | D5- | bengali | 4 | 1 | 11 | 0.0912 | [0, 0.203] |
| single | select | D5- | bosnian | 2 | 0 | 3.88 | 0 | [n/a, n/a] |
| single | select | D5- | bulgarian | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | select | D5- | english | 145 | 16 | 273 | 0.0587 | [0.0289, 0.0949] |
| single | select | total | afrikaans | 1 | 2 | 1.83 | 1.09 | [n/a, n/a] |
| single | select | total | albanian | 2 | 15 | 5.59 | 2.68 | [2.57, 2.83] |
| single | select | total | amazigh | 1 | 13 | 3.56 | 3.65 | [n/a, n/a] |
| single | select | total | amharic | 5 | 36 | 15.5 | 2.33 | [1.19, 3.04] |
| single | select | total | arabic | 25 | 77 | 68.9 | 1.12 | [0.548, 1.74] |
| single | select | total | armenian | 2 | 9 | 3.33 | 2.7 | [1.52, 3.48] |
| single | select | total | azerbaijani | 1 | 9 | 2.44 | 3.69 | [n/a, n/a] |
| single | select | total | bafang | 1 | 0 | 3.4 | 0 | [n/a, n/a] |
| single | select | total | bambara | 1 | 2 | 2.73 | 0.734 | [n/a, n/a] |
| single | select | total | basque | 1 | 2 | 2.77 | 0.723 | [n/a, n/a] |
| single | select | total | belarusan | 1 | 2 | 2.1 | 0.953 | [n/a, n/a] |
| single | select | total | bengali | 4 | 12 | 11 | 1.09 | [0.172, 2.59] |
| single | select | total | bosnian | 2 | 1 | 3.88 | 0.257 | [0, 0.597] |
| single | select | total | bulgarian | 1 | 0 | 2.17 | 0 | [n/a, n/a] |
| single | select | total | english | 145 | 147 | 273 | 0.539 | [0.399, 0.689] |

Sources retain equal weights by owner decision; texts are weighted by comparison-minutes within a source. These rates describe that mixture, not a deployment population. In v11 Gettysburg had ten fit readers and 4.8% of fit exposure but 25% of weight; it supplied 72% of the weighted D2- rate. The Accent-driven select gap is associated with L1/lab-seen composition; those effects are confounded. Select results were inspected during redesign; the estimator was the owner decision. The lockbox rates are measured only by the final evaluation (lockbox section).

0.5/min budget is not met at the point rate; upper95 does not establish the budget. Weighted total: 0.549/min; pooled total: 0.482/min.

## False flags per minute on nulls

| population | false flags | exposure (min) | observed per comparison-minute | rule of three (R1 unique recordings only; R2 dependent) |
|---|---|---|---|---|
| R1 val: identity + 5 placebo seeds (12 variants; 2 source recordings / readers) | 0 | 5.93 | 0 | 3.03 |
| R1 test: identity + 5 placebo seeds (12 variants; 2 source recordings / readers) | 0 | 5.89 | 0 | 3.06 |
| R1 val+test: identity + 5 placebo seeds (24 variants; 4 source recordings / readers) | 0 | 11.8 | 0 | 1.52 |
| R2 check-reader pairs, not fitted but seen during the detector redesign (18 ordered pairs; 9 recordings / readers) | 2 | 7.76 | 0.258 |  |
| R2 orator-reference row: Greenman vs Reagan (2 recordings / readers; never fitted) | 0 | 0.54 | 0 |  |

Reader-level R2 null counts:

| participant reader | comparisons | comparison-minutes | flags | by flag key |
|---|---|---|---|---|
| gettysburg_dj | 6 | 2.29 | 0 | {} |
| gettysburg_sa | 6 | 3.02 | 2 | {'D3- whole clip': 2} |
| gettysburg_tg | 6 | 2.45 | 0 | {} |

## Score by rung of the bad spectrum (R1)

| split | rung | clips | lowest score | median score | highest score |
|---|---|---|---|---|---|
| train | identity | 5 | 100 | 100 | 100 |
| train | G1 | 5 | 99.2 | 99.9 | 100 |
| train | level 1 (four edits) | 10 | 95.8 | 99.7 | 100 |
| train | G3 | 5 | 95.7 | 96.3 | 98.8 |
| train | level 2 (four edits) | 10 | 92.1 | 93.7 | 95.7 |
| train | level 3 (four edits) | 10 | 72.5 | 82.7 | 86.1 |
| train | G5 | 5 | 42.9 | 48.3 | 49.5 |
| train | extra level 1 | 20 | 89.6 | 99.6 | 100 |
| train | extra level 2 | 20 | 91.2 | 98.3 | 99.9 |
| train | extra level 3 | 20 | 87.6 | 96 | 99.9 |
| val | identity | 2 | 100 | 100 | 100 |
| val | G1 | 2 | 99.9 | 100 | 100 |
| val | level 1 (four edits) | 4 | 98.2 | 99.7 | 100 |
| val | G3 | 2 | 95.6 | 96.6 | 97.5 |
| val | level 2 (four edits) | 4 | 90.9 | 93.2 | 94.9 |
| val | level 3 (four edits) | 4 | 77.2 | 81 | 84.8 |
| val | G5 | 2 | 48.5 | 48.6 | 48.7 |
| val | extra level 1 | 8 | 98.6 | 99.9 | 100 |
| val | extra level 2 | 8 | 93.8 | 98.3 | 99.9 |
| val | extra level 3 | 8 | 85 | 94.3 | 98.6 |
| test | identity | 2 | 100 | 100 | 100 |
| test | G1 | 2 | 100 | 100 | 100 |
| test | level 1 (four edits) | 4 | 94.8 | 99.3 | 100 |
| test | G3 | 2 | 95.7 | 96.1 | 96.6 |
| test | level 2 (four edits) | 4 | 92 | 94.7 | 96 |
| test | level 3 (four edits) | 4 | 62 | 76.5 | 87.5 |
| test | G5 | 2 | 43.8 | 45.9 | 48 |
| test | extra level 1 | 8 | 95.6 | 97.6 | 100 |
| test | extra level 2 | 8 | 83.9 | 96.6 | 99.6 |
| test | extra level 3 | 8 | 86.2 | 94.2 | 97.8 |

Score gates (violations):

| split | identity below 100 | level-1 clip below 90 | G5 above 50 | ladder G1 >= G3 >= G5 broken |
|---|---|---|---|---|
| train | 0 | 0 | 0 | 0 |
| val | 0 | 0 | 0 | 0 |
| test | 0 | 0 | 0 | 0 |

## Excluded realisation shortfall stratum

Excluded realisation shortfalls are not truth or h-selection positives. Non-monotone ladders are excluded at every affected rung.

| regime | split | type | level | excluded events |
|---|---|---|---|---|
| R1 | test | FLAT_FINAL_FALL | 3 | 1 |
| R1 | test | LOW_EFFORT | 1 | 1 |
| R1 | test | LOW_EFFORT | 2 | 1 |
| R1 | test | LOW_EFFORT | 3 | 1 |
| R1 | test | RISING_ENDING | 1 | 2 |
| R1 | test | RISING_ENDING | 2 | 2 |
| R1 | test | RISING_ENDING | 3 | 2 |
| R1 | test | TRAILING_OFF | 1 | 1 |
| R1 | test | TRAILING_OFF | 2 | 1 |
| R1 | test | TRAILING_OFF | 3 | 1 |
| R1 | train | FLAT_FINAL_FALL | 1 | 3 |
| R1 | train | FLAT_FINAL_FALL | 2 | 1 |
| R1 | train | FLAT_FINAL_FALL | 3 | 2 |
| R1 | train | LOW_EFFORT | 1 | 1 |
| R1 | train | LOW_EFFORT | 2 | 1 |
| R1 | train | LOW_EFFORT | 3 | 1 |
| R1 | train | REPEATED_CONTOUR | 1 | 2 |
| R1 | train | REPEATED_CONTOUR | 2 | 2 |
| R1 | train | REPEATED_CONTOUR | 3 | 3 |
| R1 | train | RISING_ENDING | 1 | 5 |
| R1 | train | RISING_ENDING | 2 | 5 |
| R1 | train | RISING_ENDING | 3 | 8 |
| R1 | val | FLAT_FINAL_FALL | 1 | 2 |
| R1 | val | FLAT_FINAL_FALL | 2 | 2 |
| R1 | val | FLAT_FINAL_FALL | 3 | 2 |
| R1 | val | LOW_EFFORT | 1 | 2 |
| R1 | val | LOW_EFFORT | 2 | 2 |
| R1 | val | LOW_EFFORT | 3 | 2 |
| R1 | val | RISING_ENDING | 1 | 2 |
| R1 | val | RISING_ENDING | 2 | 2 |
| R1 | val | RISING_ENDING | 3 | 3 |
| R2 | calibration | LOW_EFFORT | 2 | 3 |
| R2 | calibration | LOW_EFFORT | 3 | 3 |
| R2 | calibration | RISING_ENDING | 3 | 3 |
| R2 | check | FLAT_FINAL_FALL | 3 | 2 |
| R2 | check | RISING_ENDING | 3 | 2 |
| R2 | train | RISING_ENDING | 3 | 3 |

## Cross-speaker flawed pairs, flawed minus clean (R2)

Single reference:

| reader group | new flags | worsened | pre-existing | away-edits | away-edits detected | away-edits flagged or among the 5 listed differences | repair controls | controls flagged | unmeasurable |
|---|---|---|---|---|---|---|---|---|---|
| calibration | 170 | 12 | 8 | 738 | 27 | 205 | 185 | 0 | 77 |
| check | 125 | 0 | 0 | 625 | 85 | 275 | 121 | 0 | 46 |
| train | 10 | 0 | 0 | 36 | 4 | 14 | 5 | 0 | 2 |

Away-edits by type and level (a check reader's clip counts once per calibration reference):

| reader group | type | level | detected | flagged or among the 5 listed differences | away-edits | 95% Wilson |
|---|---|---|---|---|---|---|
| calibration | BLOCK | 2 | 0 | 1 | 18 | [0, 0.176] |
| calibration | BLOCK | 3 | 0 | 1 | 17 | [0, 0.184] |
| calibration | FLAT_FINAL_FALL | 3 | 0 | 6 | 11 | [0, 0.259] |
| calibration | HESITATION | 2 | 0 | 0 | 30 | [0, 0.114] |
| calibration | HESITATION | 3 | 17 | 26 | 30 | [0.392, 0.726] |
| calibration | LOW_EFFORT | 2 | 0 | 6 | 14 | [0, 0.215] |
| calibration | LOW_EFFORT | 3 | 5 | 15 | 15 | [0.152, 0.583] |
| calibration | MISPLACED_EMPHASIS | 3 | 0 | 0 | 2 | [0, 0.658] |
| calibration | NATURAL_RUSH | 2 | 0 | 6 | 19 | [0, 0.168] |
| calibration | NATURAL_RUSH | 3 | 0 | 6 | 19 | [0, 0.168] |
| calibration | ONSET_PROLONGATION | 2 | 0 | 25 | 29 | [0, 0.117] |
| calibration | ONSET_PROLONGATION | 3 | 0 | 30 | 30 | [0, 0.114] |
| calibration | RHYME_PROLONGATION | 2 | 0 | 17 | 27 | [0, 0.125] |
| calibration | RHYME_PROLONGATION | 3 | 0 | 19 | 27 | [0, 0.125] |
| calibration | RISING_ENDING | 3 | 0 | 6 | 10 | [0, 0.278] |
| calibration | SOUND_REPETITION | 2 | 0 | 1 | 15 | [0, 0.204] |
| calibration | SOUND_REPETITION | 3 | 0 | 0 | 14 | [0, 0.215] |
| calibration | TRAILING_OFF | 2 | 1 | 6 | 20 | [0.00888, 0.236] |
| calibration | TRAILING_OFF | 3 | 4 | 11 | 21 | [0.0767, 0.4] |
| calibration | UNEVEN_TEMPO | 2 | 0 | 6 | 23 | [0, 0.143] |
| calibration | UNEVEN_TEMPO | 3 | 0 | 5 | 19 | [0, 0.168] |
| calibration | WORD_BY_WORD | 2 | 0 | 0 | 142 | [0, 0.0263] |
| calibration | WORD_BY_WORD | 3 | 0 | 0 | 151 | [0, 0.0248] |
| calibration | WORD_REPETITION | 2 | 0 | 2 | 16 | [0, 0.194] |
| calibration | WORD_REPETITION | 3 | 0 | 10 | 19 | [0, 0.168] |
| check | BLOCK | 2 | 0 | 0 | 8 | [0, 0.324] |
| check | BLOCK | 3 | 0 | 0 | 8 | [0, 0.324] |
| check | DRAG | 3 | 6 | 16 | 17 | [0.173, 0.587] |
| check | FADE | 3 | 13 | 18 | 18 | [0.491, 0.875] |
| check | FLAT_FINAL_FALL | 3 | 0 | 1 | 4 | [0, 0.49] |
| check | HESITATION | 2 | 0 | 0 | 18 | [0, 0.176] |
| check | HESITATION | 3 | 13 | 16 | 18 | [0.491, 0.875] |
| check | LOW_EFFORT | 2 | 4 | 13 | 17 | [0.0956, 0.473] |
| check | LOW_EFFORT | 3 | 11 | 18 | 18 | [0.386, 0.797] |
| check | MISPLACED_EMPHASIS | 3 | 0 | 0 | 5 | [0, 0.434] |
| check | MONOTONE | 3 | 17 | 18 | 18 | [0.742, 0.99] |
| check | NATURAL_RUSH | 2 | 0 | 4 | 10 | [0, 0.278] |
| check | NATURAL_RUSH | 3 | 0 | 6 | 10 | [0, 0.278] |
| check | ONSET_PROLONGATION | 2 | 0 | 18 | 18 | [0, 0.176] |
| check | ONSET_PROLONGATION | 3 | 0 | 18 | 18 | [0, 0.176] |
| check | PAUSE_DROPPED | 2 | 2 | 6 | 14 | [0.0401, 0.399] |
| check | PAUSE_DROPPED | 3 | 4 | 6 | 17 | [0.0956, 0.473] |
| check | PAUSE_INTRUSIVE | 3 | 14 | 17 | 18 | [0.548, 0.91] |
| check | RHYME_PROLONGATION | 2 | 0 | 12 | 18 | [0, 0.176] |
| check | RHYME_PROLONGATION | 3 | 0 | 13 | 18 | [0, 0.176] |
| check | RISING_ENDING | 3 | 0 | 7 | 10 | [0, 0.278] |
| check | RUSH | 2 | 0 | 7 | 13 | [0, 0.228] |
| check | RUSH | 3 | 1 | 18 | 18 | [0.00988, 0.258] |
| check | SOUND_REPETITION | 2 | 0 | 6 | 11 | [0, 0.259] |
| check | SOUND_REPETITION | 3 | 0 | 6 | 13 | [0, 0.228] |
| check | TRAILING_OFF | 2 | 0 | 0 | 7 | [0, 0.354] |
| check | TRAILING_OFF | 3 | 0 | 0 | 8 | [0, 0.324] |
| check | UNEVEN_TEMPO | 2 | 0 | 9 | 11 | [0, 0.259] |
| check | UNEVEN_TEMPO | 3 | 0 | 10 | 15 | [0, 0.204] |
| check | WORD_BY_WORD | 2 | 0 | 0 | 104 | [0, 0.0356] |
| check | WORD_BY_WORD | 3 | 0 | 0 | 108 | [0, 0.0343] |
| check | WORD_REPETITION | 2 | 0 | 6 | 9 | [0, 0.299] |
| check | WORD_REPETITION | 3 | 0 | 6 | 8 | [0, 0.324] |
| train | BLOCK | 2 | 0 | 0 | 1 | [0, 0.793] |
| train | BLOCK | 3 | 0 | 1 | 1 | [0, 0.793] |
| train | DRAG | 3 | 0 | 1 | 1 | [0, 0.793] |
| train | FADE | 3 | 1 | 1 | 1 | [0.207, 1] |
| train | HESITATION | 2 | 0 | 0 | 1 | [0, 0.793] |
| train | HESITATION | 3 | 1 | 1 | 1 | [0.207, 1] |
| train | LOW_EFFORT | 2 | 1 | 1 | 1 | [0.207, 1] |
| train | LOW_EFFORT | 3 | 0 | 1 | 1 | [0, 0.793] |
| train | MISPLACED_EMPHASIS | 3 | 0 | 0 | 1 | [0, 0.793] |
| train | MONOTONE | 3 | 0 | 1 | 1 | [0, 0.793] |
| train | ONSET_PROLONGATION | 2 | 0 | 1 | 1 | [0, 0.793] |
| train | ONSET_PROLONGATION | 3 | 0 | 1 | 1 | [0, 0.793] |
| train | PAUSE_DROPPED | 2 | 0 | 0 | 1 | [0, 0.793] |
| train | PAUSE_DROPPED | 3 | 0 | 0 | 1 | [0, 0.793] |
| train | PAUSE_INTRUSIVE | 3 | 1 | 1 | 1 | [0.207, 1] |
| train | RHYME_PROLONGATION | 2 | 0 | 1 | 1 | [0, 0.793] |
| train | RHYME_PROLONGATION | 3 | 0 | 1 | 1 | [0, 0.793] |
| train | RUSH | 2 | 0 | 0 | 1 | [0, 0.793] |
| train | RUSH | 3 | 0 | 1 | 1 | [0, 0.793] |
| train | TRAILING_OFF | 2 | 0 | 0 | 1 | [0, 0.793] |
| train | TRAILING_OFF | 3 | 0 | 0 | 1 | [0, 0.793] |
| train | UNEVEN_TEMPO | 2 | 0 | 0 | 1 | [0, 0.793] |
| train | UNEVEN_TEMPO | 3 | 0 | 0 | 1 | [0, 0.793] |
| train | WORD_BY_WORD | 2 | 0 | 0 | 6 | [0, 0.39] |
| train | WORD_BY_WORD | 3 | 0 | 0 | 6 | [0, 0.39] |
| train | WORD_REPETITION | 3 | 0 | 1 | 1 | [0, 0.793] |

| reader group | type | level | count | expected secondary firings | status |
|---|---|---|---|---|---|
| calibration | REPEATED_CONTOUR | 3 | 30 | 0 | no detector |
| check | REPEATED_CONTOUR | 3 | 18 | 0 | no detector |
| train | REPEATED_CONTOUR | 3 | 1 | 0 | no detector |

Per clip and reference:

| clip | reference | reader group | new flags | worsened | pre-existing | away-edits | away-edits detected | away-edits flagged or among the 5 listed differences | repair controls | controls flagged | unmeasurable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gettysburg_amb__extra_x10_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_amb__extra_x10_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_amb__extra_x10_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_amb__extra_x10_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_amb__extra_x10_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_amb__extra_x1_L2 | gettysburg_dl | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_amb__extra_x1_L2 | gettysburg_fb | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_amb__extra_x1_L2 | gettysburg_jn | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_amb__extra_x1_L2 | gettysburg_pc | calibration | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_amb__extra_x1_L2 | gettysburg_wt | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_amb__extra_x2_L2 | gettysburg_dl | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_amb__extra_x2_L2 | gettysburg_fb | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_amb__extra_x2_L2 | gettysburg_jn | calibration | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_amb__extra_x2_L2 | gettysburg_pc | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_amb__extra_x2_L2 | gettysburg_wt | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_amb__extra_x3_L2 | gettysburg_dl | calibration | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_amb__extra_x3_L2 | gettysburg_fb | calibration | 0 | 0 | 0 | 7 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_amb__extra_x3_L2 | gettysburg_jn | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 3 | 0 | 0 |
| gettysburg_amb__extra_x3_L2 | gettysburg_pc | calibration | 0 | 0 | 0 | 7 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_amb__extra_x3_L2 | gettysburg_wt | calibration | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_amb__extra_x4_L2 | gettysburg_dl | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_amb__extra_x4_L2 | gettysburg_fb | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_amb__extra_x4_L2 | gettysburg_jn | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_amb__extra_x4_L2 | gettysburg_pc | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_amb__extra_x4_L2 | gettysburg_wt | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_amb__extra_x5_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_amb__extra_x5_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_amb__extra_x5_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_amb__extra_x5_L3 | gettysburg_pc | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_amb__extra_x5_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_amb__extra_x6_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_amb__extra_x6_L3 | gettysburg_fb | calibration | 1 | 0 | 0 | 1 | 1 | 1 | 2 | 0 | 0 |
| gettysburg_amb__extra_x6_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_amb__extra_x6_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_amb__extra_x6_L3 | gettysburg_wt | calibration | 1 | 0 | 0 | 1 | 1 | 1 | 2 | 0 | 0 |
| gettysburg_amb__extra_x7_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 8 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_amb__extra_x7_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 8 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_amb__extra_x7_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 7 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_amb__extra_x7_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 7 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_amb__extra_x7_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_amb__extra_x8_L3 | gettysburg_dl | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_amb__extra_x8_L3 | gettysburg_fb | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_amb__extra_x8_L3 | gettysburg_jn | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_amb__extra_x8_L3 | gettysburg_pc | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_amb__extra_x8_L3 | gettysburg_wt | calibration | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_amb__extra_x9_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_amb__extra_x9_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_amb__extra_x9_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_amb__extra_x9_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_amb__extra_x9_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_dj__extra_x10_L3 | gettysburg_amb | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_dj__extra_x10_L3 | gettysburg_dl | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_dj__extra_x10_L3 | gettysburg_fb | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_dj__extra_x10_L3 | gettysburg_jn | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_dj__extra_x10_L3 | gettysburg_pc | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_dj__extra_x10_L3 | gettysburg_wt | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_dj__extra_x1_L2 | gettysburg_amb | check | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dj__extra_x1_L2 | gettysburg_dl | check | 0 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_dj__extra_x1_L2 | gettysburg_fb | check | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x1_L2 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x1_L2 | gettysburg_pc | check | 0 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_dj__extra_x1_L2 | gettysburg_wt | check | 1 | 0 | 0 | 3 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_dj__extra_x2_L2 | gettysburg_amb | check | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__extra_x2_L2 | gettysburg_dl | check | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_dj__extra_x2_L2 | gettysburg_fb | check | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__extra_x2_L2 | gettysburg_jn | check | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__extra_x2_L2 | gettysburg_pc | check | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__extra_x2_L2 | gettysburg_wt | check | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__extra_x3_L2 | gettysburg_amb | check | 0 | 0 | 0 | 7 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x3_L2 | gettysburg_dl | check | 0 | 0 | 0 | 6 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_dj__extra_x3_L2 | gettysburg_fb | check | 0 | 0 | 0 | 7 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x3_L2 | gettysburg_jn | check | 0 | 0 | 0 | 8 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_dj__extra_x3_L2 | gettysburg_pc | check | 0 | 0 | 0 | 7 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x3_L2 | gettysburg_wt | check | 0 | 0 | 0 | 8 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_dj__extra_x4_L2 | gettysburg_amb | check | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x4_L2 | gettysburg_dl | check | 1 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_dj__extra_x4_L2 | gettysburg_fb | check | 1 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_dj__extra_x4_L2 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dj__extra_x4_L2 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dj__extra_x4_L2 | gettysburg_wt | check | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x5_L3 | gettysburg_amb | check | 1 | 0 | 0 | 3 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_dj__extra_x5_L3 | gettysburg_dl | check | 1 | 0 | 0 | 3 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_dj__extra_x5_L3 | gettysburg_fb | check | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x5_L3 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x5_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_dj__extra_x5_L3 | gettysburg_wt | check | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_dj__extra_x6_L3 | gettysburg_amb | check | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x6_L3 | gettysburg_dl | check | 0 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_dj__extra_x6_L3 | gettysburg_fb | check | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__extra_x6_L3 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x6_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x6_L3 | gettysburg_wt | check | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x7_L3 | gettysburg_amb | check | 0 | 0 | 0 | 7 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x7_L3 | gettysburg_dl | check | 0 | 0 | 0 | 7 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x7_L3 | gettysburg_fb | check | 0 | 0 | 0 | 7 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x7_L3 | gettysburg_jn | check | 0 | 0 | 0 | 8 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_dj__extra_x7_L3 | gettysburg_pc | check | 0 | 0 | 0 | 7 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x7_L3 | gettysburg_wt | check | 0 | 0 | 0 | 8 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_dj__extra_x8_L3 | gettysburg_amb | check | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_dj__extra_x8_L3 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dj__extra_x8_L3 | gettysburg_fb | check | 1 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_dj__extra_x8_L3 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dj__extra_x8_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dj__extra_x8_L3 | gettysburg_wt | check | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_dj__extra_x9_L3 | gettysburg_amb | check | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__extra_x9_L3 | gettysburg_dl | check | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_dj__extra_x9_L3 | gettysburg_fb | check | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_dj__extra_x9_L3 | gettysburg_jn | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_dj__extra_x9_L3 | gettysburg_pc | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_dj__extra_x9_L3 | gettysburg_wt | check | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_dj__x1_L2 | gettysburg_amb | check | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_dj__x1_L2 | gettysburg_dl | check | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__x1_L2 | gettysburg_fb | check | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_dj__x1_L2 | gettysburg_jn | check | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__x1_L2 | gettysburg_pc | check | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__x1_L2 | gettysburg_wt | check | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dj__x2_L3 | gettysburg_amb | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x2_L3 | gettysburg_dl | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x2_L3 | gettysburg_fb | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x2_L3 | gettysburg_jn | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x2_L3 | gettysburg_pc | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x2_L3 | gettysburg_wt | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x3_L3 | gettysburg_amb | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x3_L3 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x3_L3 | gettysburg_fb | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x3_L3 | gettysburg_jn | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x3_L3 | gettysburg_pc | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x3_L3 | gettysburg_wt | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x4_L3 | gettysburg_amb | check | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dj__x4_L3 | gettysburg_dl | check | 0 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x4_L3 | gettysburg_fb | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_dj__x4_L3 | gettysburg_jn | check | 0 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x4_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x4_L3 | gettysburg_wt | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_dl__extra_x10_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_dl__extra_x10_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_dl__extra_x10_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_dl__extra_x10_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_dl__extra_x10_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_dl__extra_x1_L2 | gettysburg_amb | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_dl__extra_x1_L2 | gettysburg_fb | calibration | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dl__extra_x1_L2 | gettysburg_jn | calibration | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dl__extra_x1_L2 | gettysburg_pc | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dl__extra_x1_L2 | gettysburg_wt | calibration | 0 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_dl__extra_x2_L2 | gettysburg_amb | calibration | 0 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_dl__extra_x2_L2 | gettysburg_fb | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_dl__extra_x2_L2 | gettysburg_jn | calibration | 0 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_dl__extra_x2_L2 | gettysburg_pc | calibration | 1 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dl__extra_x2_L2 | gettysburg_wt | calibration | 1 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dl__extra_x3_L2 | gettysburg_amb | calibration | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_dl__extra_x3_L2 | gettysburg_fb | calibration | 0 | 0 | 0 | 5 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dl__extra_x3_L2 | gettysburg_jn | calibration | 0 | 0 | 0 | 4 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_dl__extra_x3_L2 | gettysburg_pc | calibration | 0 | 0 | 0 | 5 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dl__extra_x3_L2 | gettysburg_wt | calibration | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_dl__extra_x4_L2 | gettysburg_amb | calibration | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dl__extra_x4_L2 | gettysburg_fb | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_dl__extra_x4_L2 | gettysburg_jn | calibration | 2 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dl__extra_x4_L2 | gettysburg_pc | calibration | 2 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_dl__extra_x4_L2 | gettysburg_wt | calibration | 1 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_dl__extra_x5_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dl__extra_x5_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dl__extra_x5_L3 | gettysburg_jn | calibration | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dl__extra_x5_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_dl__extra_x5_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 3 | 0 | 3 | 0 | 0 | 0 |
| gettysburg_dl__extra_x6_L3 | gettysburg_amb | calibration | 2 | 0 | 0 | 3 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_dl__extra_x6_L3 | gettysburg_fb | calibration | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dl__extra_x6_L3 | gettysburg_jn | calibration | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_dl__extra_x6_L3 | gettysburg_pc | calibration | 2 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dl__extra_x6_L3 | gettysburg_wt | calibration | 1 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_dl__extra_x7_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_dl__extra_x7_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 5 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dl__extra_x7_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 5 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dl__extra_x7_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 5 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dl__extra_x7_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_dl__extra_x8_L3 | gettysburg_amb | calibration | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_dl__extra_x8_L3 | gettysburg_fb | calibration | 2 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dl__extra_x8_L3 | gettysburg_jn | calibration | 2 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dl__extra_x8_L3 | gettysburg_pc | calibration | 2 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dl__extra_x8_L3 | gettysburg_wt | calibration | 2 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_dl__extra_x9_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dl__extra_x9_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_dl__extra_x9_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_dl__extra_x9_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_dl__extra_x9_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_fb__extra_x10_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_fb__extra_x10_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_fb__extra_x10_L3 | gettysburg_jn | calibration | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_fb__extra_x10_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_fb__extra_x10_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_fb__extra_x1_L2 | gettysburg_amb | calibration | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_fb__extra_x1_L2 | gettysburg_dl | calibration | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_fb__extra_x1_L2 | gettysburg_jn | calibration | 1 | 0 | 1 | 0 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_fb__extra_x1_L2 | gettysburg_pc | calibration | 3 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_fb__extra_x1_L2 | gettysburg_wt | calibration | 2 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x2_L2 | gettysburg_amb | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_fb__extra_x2_L2 | gettysburg_dl | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_fb__extra_x2_L2 | gettysburg_jn | calibration | 0 | 0 | 1 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_fb__extra_x2_L2 | gettysburg_pc | calibration | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_fb__extra_x2_L2 | gettysburg_wt | calibration | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_fb__extra_x3_L2 | gettysburg_amb | calibration | 0 | 0 | 0 | 4 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x3_L2 | gettysburg_dl | calibration | 0 | 0 | 0 | 4 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x3_L2 | gettysburg_jn | calibration | 0 | 1 | 0 | 4 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x3_L2 | gettysburg_pc | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x3_L2 | gettysburg_wt | calibration | 0 | 0 | 0 | 4 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x4_L2 | gettysburg_amb | calibration | 2 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x4_L2 | gettysburg_dl | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x4_L2 | gettysburg_jn | calibration | 2 | 1 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x4_L2 | gettysburg_pc | calibration | 2 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x4_L2 | gettysburg_wt | calibration | 2 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x5_L3 | gettysburg_amb | calibration | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_fb__extra_x5_L3 | gettysburg_dl | calibration | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_fb__extra_x5_L3 | gettysburg_jn | calibration | 1 | 0 | 1 | 0 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_fb__extra_x5_L3 | gettysburg_pc | calibration | 3 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_fb__extra_x5_L3 | gettysburg_wt | calibration | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_fb__extra_x6_L3 | gettysburg_amb | calibration | 2 | 0 | 0 | 3 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x6_L3 | gettysburg_dl | calibration | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x6_L3 | gettysburg_jn | calibration | 1 | 0 | 1 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_fb__extra_x6_L3 | gettysburg_pc | calibration | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_fb__extra_x6_L3 | gettysburg_wt | calibration | 2 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_fb__extra_x7_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 4 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x7_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 4 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x7_L3 | gettysburg_jn | calibration | 0 | 1 | 0 | 5 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x7_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x7_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x8_L3 | gettysburg_amb | calibration | 2 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x8_L3 | gettysburg_dl | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x8_L3 | gettysburg_jn | calibration | 2 | 1 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x8_L3 | gettysburg_pc | calibration | 2 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x8_L3 | gettysburg_wt | calibration | 2 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x9_L3 | gettysburg_amb | calibration | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_fb__extra_x9_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_fb__extra_x9_L3 | gettysburg_jn | calibration | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_fb__extra_x9_L3 | gettysburg_pc | calibration | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_fb__extra_x9_L3 | gettysburg_wt | calibration | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_jn__extra_x10_L3 | gettysburg_amb | calibration | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_jn__extra_x10_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_jn__extra_x10_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_jn__extra_x10_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_jn__extra_x10_L3 | gettysburg_wt | calibration | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_jn__extra_x1_L2 | gettysburg_amb | calibration | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_jn__extra_x1_L2 | gettysburg_dl | calibration | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x1_L2 | gettysburg_fb | calibration | 0 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_jn__extra_x1_L2 | gettysburg_pc | calibration | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_jn__extra_x1_L2 | gettysburg_wt | calibration | 0 | 0 | 1 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_jn__extra_x2_L2 | gettysburg_amb | calibration | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_jn__extra_x2_L2 | gettysburg_dl | calibration | 1 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_jn__extra_x2_L2 | gettysburg_fb | calibration | 1 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_jn__extra_x2_L2 | gettysburg_pc | calibration | 1 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_jn__extra_x2_L2 | gettysburg_wt | calibration | 1 | 1 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_jn__extra_x3_L2 | gettysburg_amb | calibration | 0 | 0 | 0 | 6 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_jn__extra_x3_L2 | gettysburg_dl | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x3_L2 | gettysburg_fb | calibration | 0 | 0 | 0 | 6 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_jn__extra_x3_L2 | gettysburg_pc | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x3_L2 | gettysburg_wt | calibration | 0 | 1 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x4_L2 | gettysburg_amb | calibration | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_jn__extra_x4_L2 | gettysburg_dl | calibration | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_jn__extra_x4_L2 | gettysburg_fb | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_jn__extra_x4_L2 | gettysburg_pc | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x4_L2 | gettysburg_wt | calibration | 1 | 1 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_jn__extra_x5_L3 | gettysburg_amb | calibration | 1 | 0 | 0 | 3 | 1 | 3 | 0 | 0 | 0 |
| gettysburg_jn__extra_x5_L3 | gettysburg_dl | calibration | 1 | 0 | 0 | 3 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_jn__extra_x5_L3 | gettysburg_fb | calibration | 1 | 0 | 0 | 3 | 1 | 3 | 0 | 0 | 0 |
| gettysburg_jn__extra_x5_L3 | gettysburg_pc | calibration | 1 | 0 | 0 | 3 | 1 | 3 | 0 | 0 | 0 |
| gettysburg_jn__extra_x5_L3 | gettysburg_wt | calibration | 1 | 0 | 1 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_jn__extra_x6_L3 | gettysburg_amb | calibration | 2 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x6_L3 | gettysburg_dl | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x6_L3 | gettysburg_fb | calibration | 3 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x6_L3 | gettysburg_pc | calibration | 2 | 0 | 0 | 1 | 1 | 1 | 2 | 0 | 0 |
| gettysburg_jn__extra_x6_L3 | gettysburg_wt | calibration | 1 | 1 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x7_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 6 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_jn__extra_x7_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x7_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 6 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_jn__extra_x7_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x7_L3 | gettysburg_wt | calibration | 0 | 1 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x8_L3 | gettysburg_amb | calibration | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_jn__extra_x8_L3 | gettysburg_dl | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x8_L3 | gettysburg_fb | calibration | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_jn__extra_x8_L3 | gettysburg_pc | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_jn__extra_x8_L3 | gettysburg_wt | calibration | 1 | 1 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_jn__extra_x9_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_jn__extra_x9_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_jn__extra_x9_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_jn__extra_x9_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_jn__extra_x9_L3 | gettysburg_wt | calibration | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_pc__extra_x10_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_pc__extra_x10_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_pc__extra_x10_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_pc__extra_x10_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_pc__extra_x10_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_pc__extra_x1_L2 | gettysburg_amb | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_pc__extra_x1_L2 | gettysburg_dl | calibration | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_pc__extra_x1_L2 | gettysburg_fb | calibration | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_pc__extra_x1_L2 | gettysburg_jn | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_pc__extra_x1_L2 | gettysburg_wt | calibration | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x2_L2 | gettysburg_amb | calibration | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x2_L2 | gettysburg_dl | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_pc__extra_x2_L2 | gettysburg_fb | calibration | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x2_L2 | gettysburg_jn | calibration | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x2_L2 | gettysburg_wt | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_pc__extra_x3_L2 | gettysburg_amb | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x3_L2 | gettysburg_dl | calibration | 1 | 0 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x3_L2 | gettysburg_fb | calibration | 0 | 0 | 0 | 6 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_pc__extra_x3_L2 | gettysburg_jn | calibration | 0 | 0 | 0 | 6 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_pc__extra_x3_L2 | gettysburg_wt | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x4_L2 | gettysburg_amb | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x4_L2 | gettysburg_dl | calibration | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_pc__extra_x4_L2 | gettysburg_fb | calibration | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_pc__extra_x4_L2 | gettysburg_jn | calibration | 2 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_pc__extra_x4_L2 | gettysburg_wt | calibration | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_pc__extra_x5_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_pc__extra_x5_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_pc__extra_x5_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x5_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x5_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_pc__extra_x6_L3 | gettysburg_amb | calibration | 2 | 0 | 0 | 2 | 2 | 2 | 1 | 0 | 0 |
| gettysburg_pc__extra_x6_L3 | gettysburg_dl | calibration | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x6_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x6_L3 | gettysburg_jn | calibration | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_pc__extra_x6_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_pc__extra_x7_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x7_L3 | gettysburg_dl | calibration | 1 | 0 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x7_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 6 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_pc__extra_x7_L3 | gettysburg_jn | calibration | 1 | 0 | 0 | 6 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_pc__extra_x7_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 6 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_pc__extra_x8_L3 | gettysburg_amb | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x8_L3 | gettysburg_dl | calibration | 2 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_pc__extra_x8_L3 | gettysburg_fb | calibration | 2 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_pc__extra_x8_L3 | gettysburg_jn | calibration | 2 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_pc__extra_x8_L3 | gettysburg_wt | calibration | 2 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_pc__extra_x9_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_pc__extra_x9_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_pc__extra_x9_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_pc__extra_x9_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_pc__extra_x9_L3 | gettysburg_wt | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_sa__extra_x10_L3 | gettysburg_amb | check | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_sa__extra_x10_L3 | gettysburg_dl | check | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_sa__extra_x10_L3 | gettysburg_fb | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_sa__extra_x10_L3 | gettysburg_jn | check | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_sa__extra_x10_L3 | gettysburg_pc | check | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_sa__extra_x10_L3 | gettysburg_wt | check | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_sa__extra_x1_L2 | gettysburg_amb | check | 0 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_sa__extra_x1_L2 | gettysburg_dl | check | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x1_L2 | gettysburg_fb | check | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x1_L2 | gettysburg_jn | check | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x1_L2 | gettysburg_pc | check | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x1_L2 | gettysburg_wt | check | 0 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_sa__extra_x2_L2 | gettysburg_amb | check | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_sa__extra_x2_L2 | gettysburg_dl | check | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_sa__extra_x2_L2 | gettysburg_fb | check | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_sa__extra_x2_L2 | gettysburg_jn | check | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_sa__extra_x2_L2 | gettysburg_pc | check | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_sa__extra_x2_L2 | gettysburg_wt | check | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_sa__extra_x3_L2 | gettysburg_amb | check | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_sa__extra_x3_L2 | gettysburg_dl | check | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_sa__extra_x3_L2 | gettysburg_fb | check | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_sa__extra_x3_L2 | gettysburg_jn | check | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_sa__extra_x3_L2 | gettysburg_pc | check | 0 | 0 | 0 | 6 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_sa__extra_x3_L2 | gettysburg_wt | check | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_sa__extra_x4_L2 | gettysburg_amb | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x4_L2 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x4_L2 | gettysburg_fb | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x4_L2 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_sa__extra_x4_L2 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x4_L2 | gettysburg_wt | check | 1 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_sa__extra_x5_L3 | gettysburg_amb | check | 0 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_sa__extra_x5_L3 | gettysburg_dl | check | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x5_L3 | gettysburg_fb | check | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x5_L3 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x5_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x5_L3 | gettysburg_wt | check | 1 | 0 | 0 | 3 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__extra_x6_L3 | gettysburg_amb | check | 1 | 0 | 0 | 3 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__extra_x6_L3 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x6_L3 | gettysburg_fb | check | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x6_L3 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x6_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x6_L3 | gettysburg_wt | check | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x7_L3 | gettysburg_amb | check | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__extra_x7_L3 | gettysburg_dl | check | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__extra_x7_L3 | gettysburg_fb | check | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_sa__extra_x7_L3 | gettysburg_jn | check | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_sa__extra_x7_L3 | gettysburg_pc | check | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__extra_x7_L3 | gettysburg_wt | check | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_sa__extra_x8_L3 | gettysburg_amb | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x8_L3 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x8_L3 | gettysburg_fb | check | 1 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_sa__extra_x8_L3 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_sa__extra_x8_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x8_L3 | gettysburg_wt | check | 1 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_sa__extra_x9_L3 | gettysburg_amb | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__extra_x9_L3 | gettysburg_dl | check | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_sa__extra_x9_L3 | gettysburg_fb | check | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_sa__extra_x9_L3 | gettysburg_jn | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__extra_x9_L3 | gettysburg_pc | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_sa__extra_x9_L3 | gettysburg_wt | check | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_sa__x1_L2 | gettysburg_amb | check | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_sa__x1_L2 | gettysburg_dl | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x1_L2 | gettysburg_fb | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x1_L2 | gettysburg_jn | check | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_sa__x1_L2 | gettysburg_pc | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x1_L2 | gettysburg_wt | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x2_L3 | gettysburg_amb | check | 2 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x2_L3 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x2_L3 | gettysburg_fb | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x2_L3 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x2_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x2_L3 | gettysburg_wt | check | 2 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x3_L3 | gettysburg_amb | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x3_L3 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x3_L3 | gettysburg_fb | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x3_L3 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x3_L3 | gettysburg_pc | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x3_L3 | gettysburg_wt | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x4_L3 | gettysburg_amb | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x4_L3 | gettysburg_dl | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x4_L3 | gettysburg_fb | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x4_L3 | gettysburg_jn | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x4_L3 | gettysburg_pc | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x4_L3 | gettysburg_wt | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__extra_x10_L3 | gettysburg_amb | check | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_tg__extra_x10_L3 | gettysburg_dl | check | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_tg__extra_x10_L3 | gettysburg_fb | check | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_tg__extra_x10_L3 | gettysburg_jn | check | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_tg__extra_x10_L3 | gettysburg_pc | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_tg__extra_x10_L3 | gettysburg_wt | check | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_tg__extra_x1_L2 | gettysburg_amb | check | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_tg__extra_x1_L2 | gettysburg_dl | check | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 |
| gettysburg_tg__extra_x1_L2 | gettysburg_fb | check | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 1 |
| gettysburg_tg__extra_x1_L2 | gettysburg_jn | check | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_tg__extra_x1_L2 | gettysburg_pc | check | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_tg__extra_x1_L2 | gettysburg_wt | check | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_tg__extra_x2_L2 | gettysburg_amb | check | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_tg__extra_x2_L2 | gettysburg_dl | check | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_tg__extra_x2_L2 | gettysburg_fb | check | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_tg__extra_x2_L2 | gettysburg_jn | check | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_tg__extra_x2_L2 | gettysburg_pc | check | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_tg__extra_x2_L2 | gettysburg_wt | check | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_tg__extra_x3_L2 | gettysburg_amb | check | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x3_L2 | gettysburg_dl | check | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x3_L2 | gettysburg_fb | check | 0 | 0 | 0 | 6 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_tg__extra_x3_L2 | gettysburg_jn | check | 0 | 0 | 0 | 5 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_tg__extra_x3_L2 | gettysburg_pc | check | 0 | 0 | 0 | 6 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_tg__extra_x3_L2 | gettysburg_wt | check | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x4_L2 | gettysburg_amb | check | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_tg__extra_x4_L2 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_tg__extra_x4_L2 | gettysburg_fb | check | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_tg__extra_x4_L2 | gettysburg_jn | check | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x4_L2 | gettysburg_pc | check | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_tg__extra_x4_L2 | gettysburg_wt | check | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_tg__extra_x5_L3 | gettysburg_amb | check | 0 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 1 |
| gettysburg_tg__extra_x5_L3 | gettysburg_dl | check | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 1 |
| gettysburg_tg__extra_x5_L3 | gettysburg_fb | check | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 1 |
| gettysburg_tg__extra_x5_L3 | gettysburg_jn | check | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 1 |
| gettysburg_tg__extra_x5_L3 | gettysburg_pc | check | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 1 |
| gettysburg_tg__extra_x5_L3 | gettysburg_wt | check | 0 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 1 |
| gettysburg_tg__extra_x6_L3 | gettysburg_amb | check | 1 | 0 | 0 | 3 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x6_L3 | gettysburg_dl | check | 1 | 0 | 0 | 3 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x6_L3 | gettysburg_fb | check | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_tg__extra_x6_L3 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_tg__extra_x6_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_tg__extra_x6_L3 | gettysburg_wt | check | 0 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x7_L3 | gettysburg_amb | check | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_tg__extra_x7_L3 | gettysburg_dl | check | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x7_L3 | gettysburg_fb | check | 1 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_tg__extra_x7_L3 | gettysburg_jn | check | 0 | 0 | 0 | 6 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_tg__extra_x7_L3 | gettysburg_pc | check | 0 | 0 | 0 | 6 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_tg__extra_x7_L3 | gettysburg_wt | check | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x8_L3 | gettysburg_amb | check | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x8_L3 | gettysburg_dl | check | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x8_L3 | gettysburg_fb | check | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_tg__extra_x8_L3 | gettysburg_jn | check | 1 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_tg__extra_x8_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_tg__extra_x8_L3 | gettysburg_wt | check | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_tg__extra_x9_L3 | gettysburg_amb | check | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_tg__extra_x9_L3 | gettysburg_dl | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_tg__extra_x9_L3 | gettysburg_fb | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_tg__extra_x9_L3 | gettysburg_jn | check | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_tg__extra_x9_L3 | gettysburg_pc | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_tg__extra_x9_L3 | gettysburg_wt | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_tg__x1_L2 | gettysburg_amb | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x1_L2 | gettysburg_dl | check | 0 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x1_L2 | gettysburg_fb | check | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_tg__x1_L2 | gettysburg_jn | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x1_L2 | gettysburg_pc | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x1_L2 | gettysburg_wt | check | 1 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x2_L3 | gettysburg_amb | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x2_L3 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x2_L3 | gettysburg_fb | check | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_tg__x2_L3 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x2_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x2_L3 | gettysburg_wt | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x3_L3 | gettysburg_amb | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x3_L3 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x3_L3 | gettysburg_fb | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x3_L3 | gettysburg_jn | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x3_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x3_L3 | gettysburg_wt | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x4_L3 | gettysburg_amb | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x4_L3 | gettysburg_dl | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x4_L3 | gettysburg_fb | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x4_L3 | gettysburg_jn | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x4_L3 | gettysburg_pc | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x4_L3 | gettysburg_wt | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_wt__extra_x10_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_wt__extra_x10_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_wt__extra_x10_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_wt__extra_x10_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_wt__extra_x10_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_wt__extra_x1_L2 | gettysburg_amb | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_wt__extra_x1_L2 | gettysburg_dl | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_wt__extra_x1_L2 | gettysburg_fb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_wt__extra_x1_L2 | gettysburg_jn | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_wt__extra_x1_L2 | gettysburg_pc | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_wt__extra_x2_L2 | gettysburg_amb | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x2_L2 | gettysburg_dl | calibration | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_wt__extra_x2_L2 | gettysburg_fb | calibration | 1 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_wt__extra_x2_L2 | gettysburg_jn | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x2_L2 | gettysburg_pc | calibration | 1 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_wt__extra_x3_L2 | gettysburg_amb | calibration | 0 | 0 | 0 | 7 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_wt__extra_x3_L2 | gettysburg_dl | calibration | 0 | 0 | 0 | 6 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_wt__extra_x3_L2 | gettysburg_fb | calibration | 0 | 0 | 0 | 7 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_wt__extra_x3_L2 | gettysburg_jn | calibration | 0 | 0 | 0 | 5 | 0 | 0 | 3 | 0 | 0 |
| gettysburg_wt__extra_x3_L2 | gettysburg_pc | calibration | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_wt__extra_x4_L2 | gettysburg_amb | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x4_L2 | gettysburg_dl | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x4_L2 | gettysburg_fb | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x4_L2 | gettysburg_jn | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_wt__extra_x4_L2 | gettysburg_pc | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_wt__extra_x5_L3 | gettysburg_amb | calibration | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_wt__extra_x5_L3 | gettysburg_dl | calibration | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_wt__extra_x5_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_wt__extra_x5_L3 | gettysburg_jn | calibration | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_wt__extra_x5_L3 | gettysburg_pc | calibration | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_wt__extra_x6_L3 | gettysburg_amb | calibration | 3 | 0 | 0 | 3 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_wt__extra_x6_L3 | gettysburg_dl | calibration | 3 | 0 | 0 | 3 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_wt__extra_x6_L3 | gettysburg_fb | calibration | 2 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_wt__extra_x6_L3 | gettysburg_jn | calibration | 3 | 0 | 0 | 3 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_wt__extra_x6_L3 | gettysburg_pc | calibration | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_wt__extra_x7_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 7 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_wt__extra_x7_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 6 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_wt__extra_x7_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_wt__extra_x7_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 6 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_wt__extra_x7_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_wt__extra_x8_L3 | gettysburg_amb | calibration | 1 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_wt__extra_x8_L3 | gettysburg_dl | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_wt__extra_x8_L3 | gettysburg_fb | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x8_L3 | gettysburg_jn | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x8_L3 | gettysburg_pc | calibration | 1 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_wt__extra_x9_L3 | gettysburg_amb | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x9_L3 | gettysburg_dl | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x9_L3 | gettysburg_fb | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x9_L3 | gettysburg_jn | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x9_L3 | gettysburg_pc | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| greenman_reagan__extra_x10_L3 | reagan_farewell_1989 | train | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| greenman_reagan__extra_x1_L2 | reagan_farewell_1989 | train | 1 | 0 | 0 | 1 | 1 | 1 | 2 | 0 | 0 |
| greenman_reagan__extra_x2_L2 | reagan_farewell_1989 | train | 1 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| greenman_reagan__extra_x3_L2 | reagan_farewell_1989 | train | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| greenman_reagan__extra_x4_L2 | reagan_farewell_1989 | train | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| greenman_reagan__extra_x5_L3 | reagan_farewell_1989 | train | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| greenman_reagan__extra_x6_L3 | reagan_farewell_1989 | train | 2 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| greenman_reagan__extra_x7_L3 | reagan_farewell_1989 | train | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| greenman_reagan__extra_x8_L3 | reagan_farewell_1989 | train | 2 | 0 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| greenman_reagan__extra_x9_L3 | reagan_farewell_1989 | train | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| greenman_reagan__x1_L2 | reagan_farewell_1989 | train | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| greenman_reagan__x2_L3 | reagan_farewell_1989 | train | 1 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 0 |
| greenman_reagan__x3_L3 | reagan_farewell_1989 | train | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| greenman_reagan__x4_L3 | reagan_farewell_1989 | train | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |

Detected is the success metric. The top-five list is descriptive and unscored.

R2 change against dev_v9 on the fixed check-reader population:

| key | v9 h | current h | v9 detected by type | current detected by type | v9 null/min | current null/min | current null regions | current null comparison-minutes |
|---|---|---|---|---|---|---|---|---|
| D1- | 3 | 5.35 | {'RUSH': '20/31'} | {'RUSH': '1/31 (95% Wilson [0.00572, 0.162])'} | 0.387 | 0 | 0 | 7.76 |
| D1+ | 3 | 5.3 | {'DRAG': '14/17'} | {'DRAG': '6/17 (95% Wilson [0.173, 0.587])'} | 0.258 | 0 | 0 | 7.76 |
| D2- | 2.95 | 3.2 | {'PAUSE_DROPPED': '9/31'} | {'PAUSE_DROPPED': '6/31 (95% Wilson [0.0919, 0.363])'} | 0 | 0 | 0 | 7.76 |
| D2+ | 1.15 | 2.65 | {'PAUSE_INTRUSIVE': '14/18'} | {'HESITATION': '13/36 (95% Wilson [0.225, 0.524])', 'WORD_BY_WORD': '0/212 (95% Wilson [0, 0.0178])', 'PAUSE_INTRUSIVE': '14/18 (95% Wilson [0.548, 0.91])'} | 0.387 | 0 | 0 | 7.76 |
| D3- | 3.25 | 3.85 | {'MONOTONE': '18/18'} | {'MONOTONE': '17/18 (95% Wilson [0.742, 0.99])'} | 0 | 0 | 0 | 7.76 |
| D5- | 4 | 4.1 | {'FADE': '13/18'} | {'LOW_EFFORT': '15/35 (95% Wilson [0.28, 0.591])', 'TRAILING_OFF': '0/15 (95% Wilson [0, 0.204])', 'FADE': '13/18 (95% Wilson [0.491, 0.875])'} | 0 | 0 | 0 | 7.76 |

Verified v9-to-v10: RUSH 20/31 to 6/31, DRAG 14/17 to 8/17; check null unchanged at 1.03/min. EARS had the highest v10 D1 fit-source rate (0.126–0.137/min), driving the pace threshold upward. Current fit-source rates appear in the fit/select diagnostics; the fixed check population is separate from the expanded select pool.

Median of five references:

| reader group | new flags | worsened | pre-existing | away-edits | away-edits detected | away-edits flagged or among the 5 listed differences | repair controls | controls flagged | unmeasurable |
|---|---|---|---|---|---|---|---|---|---|
| calibration | 39 | 2 | 3 | 153 | 6 | 43 | 34 | 0 | 13 |
| check | 25 | 0 | 0 | 103 | 19 | 50 | 21 | 0 | 8 |

Away-edits by type and level (a check reader's clip counts once per calibration reference):

| reader group | type | level | detected | flagged or among the 5 listed differences | away-edits | 95% Wilson |
|---|---|---|---|---|---|---|
| calibration | BLOCK | 2 | 0 | 0 | 4 | [0, 0.49] |
| calibration | BLOCK | 3 | 0 | 0 | 3 | [0, 0.561] |
| calibration | FLAT_FINAL_FALL | 3 | 0 | 1 | 4 | [0, 0.49] |
| calibration | HESITATION | 2 | 0 | 0 | 6 | [0, 0.39] |
| calibration | HESITATION | 3 | 2 | 4 | 6 | [0.0968, 0.7] |
| calibration | LOW_EFFORT | 2 | 1 | 2 | 3 | [0.0615, 0.792] |
| calibration | LOW_EFFORT | 3 | 1 | 3 | 3 | [0.0615, 0.792] |
| calibration | NATURAL_RUSH | 2 | 0 | 1 | 4 | [0, 0.49] |
| calibration | NATURAL_RUSH | 3 | 0 | 1 | 4 | [0, 0.49] |
| calibration | ONSET_PROLONGATION | 2 | 0 | 5 | 6 | [0, 0.39] |
| calibration | ONSET_PROLONGATION | 3 | 0 | 6 | 6 | [0, 0.39] |
| calibration | RHYME_PROLONGATION | 2 | 0 | 3 | 6 | [0, 0.39] |
| calibration | RHYME_PROLONGATION | 3 | 0 | 4 | 6 | [0, 0.39] |
| calibration | RISING_ENDING | 3 | 0 | 3 | 4 | [0, 0.49] |
| calibration | SOUND_REPETITION | 2 | 0 | 0 | 4 | [0, 0.49] |
| calibration | SOUND_REPETITION | 3 | 0 | 0 | 3 | [0, 0.561] |
| calibration | TRAILING_OFF | 2 | 0 | 2 | 4 | [0, 0.49] |
| calibration | TRAILING_OFF | 3 | 2 | 4 | 4 | [0.15, 0.85] |
| calibration | UNEVEN_TEMPO | 2 | 0 | 0 | 2 | [0, 0.658] |
| calibration | UNEVEN_TEMPO | 3 | 0 | 2 | 4 | [0, 0.49] |
| calibration | WORD_BY_WORD | 2 | 0 | 0 | 29 | [0, 0.117] |
| calibration | WORD_BY_WORD | 3 | 0 | 0 | 32 | [0, 0.107] |
| calibration | WORD_REPETITION | 2 | 0 | 0 | 2 | [0, 0.658] |
| calibration | WORD_REPETITION | 3 | 0 | 2 | 4 | [0, 0.49] |
| check | BLOCK | 2 | 0 | 0 | 1 | [0, 0.793] |
| check | BLOCK | 3 | 0 | 0 | 1 | [0, 0.793] |
| check | DRAG | 3 | 1 | 3 | 3 | [0.0615, 0.792] |
| check | FADE | 3 | 3 | 3 | 3 | [0.439, 1] |
| check | FLAT_FINAL_FALL | 3 | 0 | 0 | 1 | [0, 0.793] |
| check | HESITATION | 2 | 0 | 0 | 3 | [0, 0.561] |
| check | HESITATION | 3 | 2 | 3 | 3 | [0.208, 0.939] |
| check | LOW_EFFORT | 2 | 1 | 2 | 2 | [0.0945, 0.905] |
| check | LOW_EFFORT | 3 | 2 | 3 | 3 | [0.208, 0.939] |
| check | MONOTONE | 3 | 3 | 3 | 3 | [0.439, 1] |
| check | NATURAL_RUSH | 2 | 0 | 1 | 1 | [0, 0.793] |
| check | NATURAL_RUSH | 3 | 0 | 1 | 1 | [0, 0.793] |
| check | ONSET_PROLONGATION | 2 | 0 | 3 | 3 | [0, 0.561] |
| check | ONSET_PROLONGATION | 3 | 0 | 3 | 3 | [0, 0.561] |
| check | PAUSE_DROPPED | 2 | 1 | 1 | 3 | [0.0615, 0.792] |
| check | PAUSE_DROPPED | 3 | 2 | 2 | 3 | [0.208, 0.939] |
| check | PAUSE_INTRUSIVE | 3 | 2 | 3 | 3 | [0.208, 0.939] |
| check | RHYME_PROLONGATION | 2 | 0 | 2 | 3 | [0, 0.561] |
| check | RHYME_PROLONGATION | 3 | 0 | 3 | 3 | [0, 0.561] |
| check | RISING_ENDING | 3 | 0 | 2 | 2 | [0, 0.658] |
| check | RUSH | 2 | 0 | 2 | 2 | [0, 0.658] |
| check | RUSH | 3 | 2 | 3 | 3 | [0.208, 0.939] |
| check | SOUND_REPETITION | 2 | 0 | 1 | 2 | [0, 0.658] |
| check | SOUND_REPETITION | 3 | 0 | 1 | 1 | [0, 0.793] |
| check | TRAILING_OFF | 2 | 0 | 0 | 1 | [0, 0.793] |
| check | TRAILING_OFF | 3 | 0 | 0 | 2 | [0, 0.658] |
| check | UNEVEN_TEMPO | 2 | 0 | 2 | 2 | [0, 0.658] |
| check | UNEVEN_TEMPO | 3 | 0 | 1 | 2 | [0, 0.658] |
| check | WORD_BY_WORD | 2 | 0 | 0 | 18 | [0, 0.176] |
| check | WORD_BY_WORD | 3 | 0 | 0 | 18 | [0, 0.176] |
| check | WORD_REPETITION | 2 | 0 | 1 | 2 | [0, 0.658] |
| check | WORD_REPETITION | 3 | 0 | 1 | 2 | [0, 0.658] |

| reader group | type | level | count | expected secondary firings | status |
|---|---|---|---|---|---|
| calibration | REPEATED_CONTOUR | 3 | 6 | 0 | no detector |
| check | REPEATED_CONTOUR | 3 | 3 | 0 | no detector |

Per clip and reference:

| clip | reference | reader group | new flags | worsened | pre-existing | away-edits | away-edits detected | away-edits flagged or among the 5 listed differences | repair controls | controls flagged | unmeasurable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gettysburg_amb__extra_x10_L3 | gettysburg_dl,gettysburg_jn,gettysburg_pc,gettysburg_wt,gettysburg_fb | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_amb__extra_x1_L2 | gettysburg_dl,gettysburg_jn,gettysburg_pc,gettysburg_wt,gettysburg_fb | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_amb__extra_x2_L2 | gettysburg_dl,gettysburg_jn,gettysburg_pc,gettysburg_wt,gettysburg_fb | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_amb__extra_x3_L2 | gettysburg_dl,gettysburg_jn,gettysburg_pc,gettysburg_wt,gettysburg_fb | calibration | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_amb__extra_x4_L2 | gettysburg_dl,gettysburg_jn,gettysburg_pc,gettysburg_wt,gettysburg_fb | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_amb__extra_x5_L3 | gettysburg_dl,gettysburg_jn,gettysburg_pc,gettysburg_wt,gettysburg_fb | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_amb__extra_x6_L3 | gettysburg_dl,gettysburg_jn,gettysburg_pc,gettysburg_wt,gettysburg_fb | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_amb__extra_x7_L3 | gettysburg_dl,gettysburg_jn,gettysburg_pc,gettysburg_wt,gettysburg_fb | calibration | 0 | 0 | 0 | 8 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_amb__extra_x8_L3 | gettysburg_dl,gettysburg_jn,gettysburg_pc,gettysburg_wt,gettysburg_fb | calibration | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_amb__extra_x9_L3 | gettysburg_dl,gettysburg_jn,gettysburg_pc,gettysburg_wt,gettysburg_fb | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_dj__extra_x10_L3 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_dj__extra_x1_L2 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 1 | 0 | 0 | 3 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_dj__extra_x2_L2 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_dj__extra_x3_L2 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 0 | 0 | 0 | 7 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x4_L2 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dj__extra_x5_L3 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 1 | 0 | 0 | 3 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_dj__extra_x6_L3 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x7_L3 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 0 | 0 | 0 | 7 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dj__extra_x8_L3 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_dj__extra_x9_L3 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_dj__x1_L2 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__x2_L3 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x3_L3 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x4_L3 | gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_dl__extra_x10_L3 | gettysburg_fb,gettysburg_wt,gettysburg_jn,gettysburg_pc,gettysburg_amb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_dl__extra_x1_L2 | gettysburg_fb,gettysburg_wt,gettysburg_jn,gettysburg_pc,gettysburg_amb | calibration | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dl__extra_x2_L2 | gettysburg_fb,gettysburg_wt,gettysburg_jn,gettysburg_pc,gettysburg_amb | calibration | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_dl__extra_x3_L2 | gettysburg_fb,gettysburg_wt,gettysburg_jn,gettysburg_pc,gettysburg_amb | calibration | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_dl__extra_x4_L2 | gettysburg_fb,gettysburg_wt,gettysburg_jn,gettysburg_pc,gettysburg_amb | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_dl__extra_x5_L3 | gettysburg_fb,gettysburg_wt,gettysburg_jn,gettysburg_pc,gettysburg_amb | calibration | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dl__extra_x6_L3 | gettysburg_fb,gettysburg_wt,gettysburg_jn,gettysburg_pc,gettysburg_amb | calibration | 2 | 0 | 0 | 3 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_dl__extra_x7_L3 | gettysburg_fb,gettysburg_wt,gettysburg_jn,gettysburg_pc,gettysburg_amb | calibration | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_dl__extra_x8_L3 | gettysburg_fb,gettysburg_wt,gettysburg_jn,gettysburg_pc,gettysburg_amb | calibration | 2 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_dl__extra_x9_L3 | gettysburg_fb,gettysburg_wt,gettysburg_jn,gettysburg_pc,gettysburg_amb | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x10_L3 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_wt,gettysburg_jn | calibration | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_fb__extra_x1_L2 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_wt,gettysburg_jn | calibration | 3 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_fb__extra_x2_L2 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_wt,gettysburg_jn | calibration | 0 | 0 | 1 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_fb__extra_x3_L2 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_wt,gettysburg_jn | calibration | 0 | 0 | 0 | 4 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x4_L2 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_wt,gettysburg_jn | calibration | 2 | 0 | 1 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x5_L3 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_wt,gettysburg_jn | calibration | 3 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_fb__extra_x6_L3 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_wt,gettysburg_jn | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x7_L3 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_wt,gettysburg_jn | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_fb__extra_x8_L3 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_wt,gettysburg_jn | calibration | 2 | 0 | 1 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_fb__extra_x9_L3 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_wt,gettysburg_jn | calibration | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_jn__extra_x10_L3 | gettysburg_wt,gettysburg_amb,gettysburg_dl,gettysburg_fb,gettysburg_pc | calibration | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_jn__extra_x1_L2 | gettysburg_wt,gettysburg_amb,gettysburg_dl,gettysburg_fb,gettysburg_pc | calibration | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_jn__extra_x2_L2 | gettysburg_wt,gettysburg_amb,gettysburg_dl,gettysburg_fb,gettysburg_pc | calibration | 1 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_jn__extra_x3_L2 | gettysburg_wt,gettysburg_amb,gettysburg_dl,gettysburg_fb,gettysburg_pc | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x4_L2 | gettysburg_wt,gettysburg_amb,gettysburg_dl,gettysburg_fb,gettysburg_pc | calibration | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_jn__extra_x5_L3 | gettysburg_wt,gettysburg_amb,gettysburg_dl,gettysburg_fb,gettysburg_pc | calibration | 1 | 0 | 0 | 3 | 1 | 3 | 0 | 0 | 0 |
| gettysburg_jn__extra_x6_L3 | gettysburg_wt,gettysburg_amb,gettysburg_dl,gettysburg_fb,gettysburg_pc | calibration | 1 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_jn__extra_x7_L3 | gettysburg_wt,gettysburg_amb,gettysburg_dl,gettysburg_fb,gettysburg_pc | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_jn__extra_x8_L3 | gettysburg_wt,gettysburg_amb,gettysburg_dl,gettysburg_fb,gettysburg_pc | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_jn__extra_x9_L3 | gettysburg_wt,gettysburg_amb,gettysburg_dl,gettysburg_fb,gettysburg_pc | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_pc__extra_x10_L3 | gettysburg_wt,gettysburg_fb,gettysburg_jn,gettysburg_dl,gettysburg_amb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| gettysburg_pc__extra_x1_L2 | gettysburg_wt,gettysburg_fb,gettysburg_jn,gettysburg_dl,gettysburg_amb | calibration | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_pc__extra_x2_L2 | gettysburg_wt,gettysburg_fb,gettysburg_jn,gettysburg_dl,gettysburg_amb | calibration | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x3_L2 | gettysburg_wt,gettysburg_fb,gettysburg_jn,gettysburg_dl,gettysburg_amb | calibration | 0 | 0 | 0 | 5 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x4_L2 | gettysburg_wt,gettysburg_fb,gettysburg_jn,gettysburg_dl,gettysburg_amb | calibration | 1 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| gettysburg_pc__extra_x5_L3 | gettysburg_wt,gettysburg_fb,gettysburg_jn,gettysburg_dl,gettysburg_amb | calibration | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_pc__extra_x6_L3 | gettysburg_wt,gettysburg_fb,gettysburg_jn,gettysburg_dl,gettysburg_amb | calibration | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_pc__extra_x7_L3 | gettysburg_wt,gettysburg_fb,gettysburg_jn,gettysburg_dl,gettysburg_amb | calibration | 1 | 0 | 0 | 6 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_pc__extra_x8_L3 | gettysburg_wt,gettysburg_fb,gettysburg_jn,gettysburg_dl,gettysburg_amb | calibration | 2 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_pc__extra_x9_L3 | gettysburg_wt,gettysburg_fb,gettysburg_jn,gettysburg_dl,gettysburg_amb | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_sa__extra_x10_L3 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_sa__extra_x1_L2 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 0 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x2_L2 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_sa__extra_x3_L2 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_sa__extra_x4_L2 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x5_L3 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x6_L3 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 1 | 0 | 0 | 2 | 1 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x7_L3 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__extra_x8_L3 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 1 | 0 | 0 | 2 | 0 | 2 | 1 | 0 | 0 |
| gettysburg_sa__extra_x9_L3 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| gettysburg_sa__x1_L2 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x2_L3 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x3_L3 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x4_L3 | gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_tg__extra_x10_L3 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_tg__extra_x1_L2 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 |
| gettysburg_tg__extra_x2_L2 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_tg__extra_x3_L2 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x4_L2 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_tg__extra_x5_L3 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 1 |
| gettysburg_tg__extra_x6_L3 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_tg__extra_x7_L3 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x8_L3 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__extra_x9_L3 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_tg__x1_L2 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x2_L3 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x3_L3 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x4_L3 | gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x10_L3 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_fb,gettysburg_jn | calibration | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| gettysburg_wt__extra_x1_L2 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_fb,gettysburg_jn | calibration | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_wt__extra_x2_L2 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_fb,gettysburg_jn | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x3_L2 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_fb,gettysburg_jn | calibration | 0 | 0 | 0 | 7 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_wt__extra_x4_L2 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_fb,gettysburg_jn | calibration | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_wt__extra_x5_L3 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_fb,gettysburg_jn | calibration | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| gettysburg_wt__extra_x6_L3 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_fb,gettysburg_jn | calibration | 4 | 0 | 0 | 3 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_wt__extra_x7_L3 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_fb,gettysburg_jn | calibration | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_wt__extra_x8_L3 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_fb,gettysburg_jn | calibration | 1 | 0 | 0 | 3 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_wt__extra_x9_L3 | gettysburg_amb,gettysburg_pc,gettysburg_dl,gettysburg_fb,gettysburg_jn | calibration | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |

Detected is the success metric. The top-five list is descriptive and unscored.

R2 change against dev_v9 on the fixed check-reader population:

| key | v9 h | current h | v9 detected by type | current detected by type | v9 null/min | current null/min | current null regions | current null comparison-minutes |
|---|---|---|---|---|---|---|---|---|
| D1- | 3 | 4.35 | {'RUSH': '20/31'} | {'RUSH': '2/5 (95% Wilson [0.118, 0.769])'} | 0.387 | 0 | 0 | 1.29 |
| D1+ | 3 | 5.75 | {'DRAG': '14/17'} | {'DRAG': '1/3 (95% Wilson [0.0615, 0.792])'} | 0.258 | 0 | 0 | 1.29 |
| D2- | 2.95 | 2.3 | {'PAUSE_DROPPED': '9/31'} | {'PAUSE_DROPPED': '3/6 (95% Wilson [0.188, 0.812])'} | 0 | 0 | 0 | 1.29 |
| D2+ | 1.15 | 2.8 | {'PAUSE_INTRUSIVE': '14/18'} | {'HESITATION': '2/6 (95% Wilson [0.0968, 0.7])', 'WORD_BY_WORD': '0/36 (95% Wilson [0, 0.0964])', 'PAUSE_INTRUSIVE': '2/3 (95% Wilson [0.208, 0.939])'} | 0.387 | 0 | 0 | 1.29 |
| D3- | 3.25 | 3.55 | {'MONOTONE': '18/18'} | {'MONOTONE': '3/3 (95% Wilson [0.439, 1])'} | 0 | 0 | 0 | 1.29 |
| D5- | 4 | 4.5 | {'FADE': '13/18'} | {'LOW_EFFORT': '3/5 (95% Wilson [0.231, 0.882])', 'TRAILING_OFF': '0/3 (95% Wilson [0, 0.561])', 'FADE': '3/3 (95% Wilson [0.439, 1])'} | 0 | 0 | 0 | 1.29 |

Verified v9-to-v10: RUSH 20/31 to 6/31, DRAG 14/17 to 8/17; check null unchanged at 1.03/min. EARS had the highest v10 D1 fit-source rate (0.126–0.137/min), driving the pace threshold upward. Current fit-source rates appear in the fit/select diagnostics; the fixed check population is separate from the expanded select pool.

Threshold, select false rate and check-reader away-edit recall at the same operating point:

| mode | key | h | physical threshold magnitude | unit | select/min | select upper95 | select sources | away recall (95% Wilson) | per type |
|---|---|---|---|---|---|---|---|---|---|
| single | D1- | 5.35 | 0.793 | ln | 0.103 | 0.127 | accent, ears, gettysburg, poetry | 1/31 (95% Wilson [0.00572, 0.162]) | {'RUSH': '1/31 (95% Wilson [0.00572, 0.162])'} |
| single | D1+ | 5.3 | 0.786 | ln | 0.127 | 0.164 | accent, ears, gettysburg, poetry | 6/17 (95% Wilson [0.173, 0.587]) | {'DRAG': '6/17 (95% Wilson [0.173, 0.587])'} |
| single | D2- | 3.2 | 1.5 | s | 0.0497 | 0.0642 | accent, ears, gettysburg, poetry | 6/31 (95% Wilson [0.0919, 0.363]) | {'PAUSE_DROPPED': '6/31 (95% Wilson [0.0919, 0.363])'} |
| single | D2+ | 2.65 | 0.98 | s | 0.118 | 0.164 | accent, ears, gettysburg, poetry | 27/266 (95% Wilson [0.0707, 0.144]) | {'HESITATION': '13/36 (95% Wilson [0.225, 0.524])', 'WORD_BY_WORD': '0/212 (95% Wilson [0, 0.0178])', 'PAUSE_INTRUSIVE': '14/18 (95% Wilson [0.548, 0.91])'} |
| single | D3- | 3.85 | 1.3 | ln | 0.0491 | 0.0699 | accent, ears, gettysburg, poetry | 17/18 (95% Wilson [0.742, 0.99]) | {'MONOTONE': '17/18 (95% Wilson [0.742, 0.99])'} |
| single | D5- | 4.1 | 10.1 | dB | 0.102 | 0.138 | accent, ears, gettysburg, poetry | 28/68 (95% Wilson [0.303, 0.53]) | {'LOW_EFFORT': '15/35 (95% Wilson [0.28, 0.591])', 'TRAILING_OFF': '0/15 (95% Wilson [0, 0.204])', 'FADE': '13/18 (95% Wilson [0.491, 0.875])'} |
| consensus5 | D1- | 4.35 | 0.544 | ln | 0.0787 | 0.126 | accent, ears, gettysburg | 2/5 (95% Wilson [0.118, 0.769]) | {'RUSH': '2/5 (95% Wilson [0.118, 0.769])'} |
| consensus5 | D1+ | 5.75 | 0.719 | ln | 0.141 | 0.197 | accent, ears, gettysburg | 1/3 (95% Wilson [0.0615, 0.792]) | {'DRAG': '1/3 (95% Wilson [0.0615, 0.792])'} |
| consensus5 | D2- | 2.3 | 0.805 | s | 0.0469 | 0.0905 | accent, ears, gettysburg | 3/6 (95% Wilson [0.188, 0.812]) | {'PAUSE_DROPPED': '3/6 (95% Wilson [0.188, 0.812])'} |
| consensus5 | D2+ | 2.8 | 1.01 | s | 0.164 | 0.242 | accent, ears, gettysburg | 4/45 (95% Wilson [0.0351, 0.207]) | {'HESITATION': '2/6 (95% Wilson [0.0968, 0.7])', 'WORD_BY_WORD': '0/36 (95% Wilson [0, 0.0964])', 'PAUSE_INTRUSIVE': '2/3 (95% Wilson [0.208, 0.939])'} |
| consensus5 | D3- | 3.55 | 1.19 | ln | 0.0307 | 0.0616 | accent, ears, gettysburg | 3/3 (95% Wilson [0.439, 1]) | {'MONOTONE': '3/3 (95% Wilson [0.439, 1])'} |
| consensus5 | D5- | 4.5 | 9 | dB | 0.0734 | 0.127 | accent, ears, gettysburg | 6/11 (95% Wilson [0.28, 0.787]) | {'LOW_EFFORT': '3/5 (95% Wilson [0.231, 0.882])', 'TRAILING_OFF': '0/3 (95% Wilson [0, 0.561])', 'FADE': '3/3 (95% Wilson [0.439, 1])'} |

Select rate scope: single: select rates cover accent, ears, gettysburg, poetry; consensus5: consensus select rates cover accent, ears, gettysburg with equal source weights; poetry is not covered: no consensus readers: 20 texts with 0-5 readers of the set each, so a reader has at most 4 distinct same-text references; 5 are needed (6 readers of one text).

Whole-clip thresholds (fit clip-budget quantile; the CLIP_H robust start beside it) and select false rates (separate 0.05/clip budget):

| mode | dimension | threshold (ln) | fit clip-budget quantile | CLIP_H robust start | clip share | select/clip | select upper95 | select sources |
|---|---|---|---|---|---|---|---|---|
| single | D1 | 0.612 | 0.612 | 0.793 | 0.025 | 0.0142 | 0.02 | accent, ears, gettysburg, poetry |
| single | D3 | 0.702 | 0.702 | 1.22 | 0.025 | 0.0316 | 0.0458 | accent, ears, gettysburg, poetry |
| single | D7 |  |  |  |  |  |  |  |
| consensus5 | D1 | 0.392 | 0.392 | 0.592 | 0.025 | 0.0368 | 0.0539 | accent, ears, gettysburg |
| consensus5 | D3 | 0.506 | 0.506 | 1.18 | 0.025 | 0.0315 | 0.0453 | accent, ears, gettysburg |
| consensus5 | D7 |  |  |  |  |  |  |  |

Select rate scope: single: select rates cover accent, ears, gettysburg, poetry; consensus5: consensus select rates cover accent, ears, gettysburg with equal source weights; poetry is not covered: no consensus readers: 20 texts with 0-5 readers of the set each, so a reader has at most 4 distinct same-text references; 5 are needed (6 readers of one text).

Stated R2 limits (measured, not tuned on select):

- single: check-reader away-edits detected in fewer than 50%: BLOCK L2 0/8, BLOCK L3 0/8, DRAG L3 6/17, FLAT_FINAL_FALL L3 0/4, HESITATION L2 0/18, LOW_EFFORT L2 4/17, MISPLACED_EMPHASIS L3 0/5, NATURAL_RUSH L2 0/10, NATURAL_RUSH L3 0/10, ONSET_PROLONGATION L2 0/18, ONSET_PROLONGATION L3 0/18, PAUSE_DROPPED L2 2/14, PAUSE_DROPPED L3 4/17, RHYME_PROLONGATION L2 0/18, RHYME_PROLONGATION L3 0/18, RISING_ENDING L3 0/10, RUSH L2 0/13, RUSH L3 1/18, SOUND_REPETITION L2 0/11, SOUND_REPETITION L3 0/13, TRAILING_OFF L2 0/7, TRAILING_OFF L3 0/8, UNEVEN_TEMPO L2 0/11, UNEVEN_TEMPO L3 0/15, WORD_BY_WORD L2 0/104, WORD_BY_WORD L3 0/108, WORD_REPETITION L2 0/9, WORD_REPETITION L3 0/8
- single select: false-region budget not met (weighted 0.549/min, bootstrap upper95 0.64, budget 0.5/min); sources above the budget: accent 0.814/min, gettysburg 0.695/min; first languages above it: albanian 2.68/min (2 readers, 5.59 min), amharic 2.33/min (5 readers, 15.5 min), arabic 1.12/min (25 readers, 68.9 min), bengali 1.09/min (4 readers, 11 min), english 0.539/min (145 readers, 273 min)
- consensus5: check-reader away-edits detected in fewer than 50%: BLOCK L2 0/1, BLOCK L3 0/1, DRAG L3 1/3, FLAT_FINAL_FALL L3 0/1, HESITATION L2 0/3, NATURAL_RUSH L2 0/1, NATURAL_RUSH L3 0/1, ONSET_PROLONGATION L2 0/3, ONSET_PROLONGATION L3 0/3, PAUSE_DROPPED L2 1/3, RHYME_PROLONGATION L2 0/3, RHYME_PROLONGATION L3 0/3, RISING_ENDING L3 0/2, RUSH L2 0/2, SOUND_REPETITION L2 0/2, SOUND_REPETITION L3 0/1, TRAILING_OFF L2 0/1, TRAILING_OFF L3 0/2, UNEVEN_TEMPO L2 0/2, UNEVEN_TEMPO L3 0/2, WORD_BY_WORD L2 0/18, WORD_BY_WORD L3 0/18, WORD_REPETITION L2 0/2, WORD_REPETITION L3 0/2
- consensus5 select: false-region budget not met on covered sources only (weighted 0.536/min, bootstrap upper95 0.67, budget 0.5/min); sources above the budget: accent 0.622/min, gettysburg 0.811/min; first languages above it: arabic 0.944/min (25 readers, 13.8 min)

## Cross-speaker whole-clip detection (R2): graded whole-passage edits and botched readings

Check readers against every calibration reader, by rung (whole-clip flag of the edited dimension; botched: both flags):

| rung | level | magnitude | whole-clip flag raised | pairs | median score |
|---|---|---|---|---|---|
| unedited |  |  | 2 | 18 | 100 |
| whole-passage RUSH | 1 | 1.2 | 0 | 18 | 100 |
| whole-passage RUSH | 2 | 1.45 | 1 | 18 | 100 |
| whole-passage RUSH | 3 | 1.9 | 11 | 18 | 90.4 |
| whole-passage MONOTONE | 1 | 0.5 | 14 | 18 | 75 |
| whole-passage MONOTONE | 2 | 0.25 | 18 | 18 | 75 |
| whole-passage MONOTONE | 3 | 0 | 18 | 18 | 75 |
| botched (G5) |  |  | 11 | 18 | 71.8 |

| reader group | pairs | overall tempo flagged | overall pitch range flagged | median score unedited | median score botched | highest score botched |
|---|---|---|---|---|---|---|
| check | 18 | 11 | 18 | 100 | 71.8 | 75 |
| train | 1 | 0 | 1 | 100 | 73.7 | 73.7 |

| clip | reference | score unedited | flags unedited | score botched | flags botched |
|---|---|---|---|---|---|
| gettysburg_dj__G5 | gettysburg_amb | 100 |  | 50 | D5-, D1- whole clip, D3- whole clip |
| gettysburg_dj__G5 | gettysburg_dl | 100 |  | 50 | D1- whole clip, D3- whole clip |
| gettysburg_dj__G5 | gettysburg_fb | 100 |  | 50.4 | D5-, D5-, D1- whole clip, D3- whole clip |
| gettysburg_dj__G5 | gettysburg_jn | 100 |  | 59.6 | D5-, D1- whole clip, D3- whole clip |
| gettysburg_dj__G5 | gettysburg_pc | 100 |  | 47.6 | D2-, D5-, D1- whole clip, D3- whole clip |
| gettysburg_dj__G5 | gettysburg_wt | 100 |  | 43.9 | D2-, D2-, D1- whole clip, D3- whole clip |
| gettysburg_sa__G5 | gettysburg_amb | 100 |  | 74 | D5-, D5-, D3- whole clip |
| gettysburg_sa__G5 | gettysburg_dl | 93.5 | D3- whole clip | 74.3 | D5-, D5-, D3- whole clip |
| gettysburg_sa__G5 | gettysburg_fb | 100 |  | 74.8 | D5-, D3- whole clip |
| gettysburg_sa__G5 | gettysburg_jn | 100 |  | 74.2 | D5-, D3- whole clip |
| gettysburg_sa__G5 | gettysburg_pc | 79.2 | D3- whole clip | 73.8 | D5-, D2-, D5-, D3- whole clip |
| gettysburg_sa__G5 | gettysburg_wt | 100 |  | 60.5 | D5-, D2-, D2-, D1- whole clip, D3- whole clip |
| gettysburg_tg__G5 | gettysburg_amb | 100 |  | 71.1 | D5-, D1- whole clip, D3- whole clip |
| gettysburg_tg__G5 | gettysburg_dl | 100 |  | 74.6 | D1- whole clip, D3- whole clip |
| gettysburg_tg__G5 | gettysburg_fb | 100 |  | 75 | D3- whole clip |
| gettysburg_tg__G5 | gettysburg_jn | 100 |  | 72.5 | D5-, D5-, D3- whole clip |
| gettysburg_tg__G5 | gettysburg_pc | 100 |  | 73.1 | D2-, D1- whole clip, D3- whole clip |
| gettysburg_tg__G5 | gettysburg_wt | 100 |  | 50 | D2-, D5-, D5-, D2-, D1- whole clip, D3- whole clip |
| greenman_reagan__G5 | reagan_farewell_1989 | 100 |  | 73.7 | D5-, D5-, D3- whole clip |

New-type local rungs (stored cross clips):

| reader | reference | type | level | local event detected | dimension score | status |
|---|---|---|---|---|---|---|
| gettysburg_amb | gettysburg_dl | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_amb | gettysburg_dl | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_amb | gettysburg_fb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_amb | gettysburg_jn | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_amb | gettysburg_pc | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_amb | gettysburg_wt | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_amb | gettysburg_dl | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | BLOCK | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_amb | gettysburg_fb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | BLOCK | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_amb | gettysburg_jn | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | BLOCK | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_amb | gettysburg_pc | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | BLOCK | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_amb | gettysburg_wt | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | BLOCK | 2 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | HESITATION | 3 | True | 98.5 | local event rung |
| gettysburg_amb | gettysburg_fb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | HESITATION | 3 | True | 99.4 | local event rung |
| gettysburg_amb | gettysburg_wt | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_dl | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_fb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_jn | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_pc | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_amb | gettysburg_wt | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_amb | gettysburg_dl | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | BLOCK | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_amb | gettysburg_fb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | BLOCK | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_amb | gettysburg_jn | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | BLOCK | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_amb | gettysburg_pc | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | BLOCK | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_amb | gettysburg_wt | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | BLOCK | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_dl | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_fb | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_jn | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_pc | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_amb | gettysburg_wt | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_dj | gettysburg_dl | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_dj | gettysburg_fb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_dj | gettysburg_jn | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_dj | gettysburg_pc | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_dj | gettysburg_wt | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_dj | gettysburg_amb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | LOW_EFFORT | 2 | True | 90.6 | local event rung |
| gettysburg_dj | gettysburg_jn | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | LOW_EFFORT | 2 | True | 97.9 | local event rung |
| gettysburg_dj | gettysburg_pc | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | LOW_EFFORT | 2 | True | 97.6 | local event rung |
| gettysburg_dj | gettysburg_amb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_dj | gettysburg_amb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | BLOCK | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_dj | gettysburg_dl | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | BLOCK | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_dj | gettysburg_fb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | BLOCK | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_dj | gettysburg_jn | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | BLOCK | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_dj | gettysburg_pc | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | BLOCK | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_dj | gettysburg_wt | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | BLOCK | 2 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | LOW_EFFORT | 3 | True | 97.7 | local event rung |
| gettysburg_dj | gettysburg_dl | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | LOW_EFFORT | 3 | True | 99.4 | local event rung |
| gettysburg_dj | gettysburg_fb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | LOW_EFFORT | 3 | True | 79.2 | local event rung |
| gettysburg_dj | gettysburg_jn | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | LOW_EFFORT | 3 | True | 89.7 | local event rung |
| gettysburg_dj | gettysburg_pc | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | LOW_EFFORT | 3 | True | 97.6 | local event rung |
| gettysburg_dj | gettysburg_wt | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | LOW_EFFORT | 3 | True | 90.1 | local event rung |
| gettysburg_dj | gettysburg_amb | HESITATION | 3 | True | 97.8 | local event rung |
| gettysburg_dj | gettysburg_amb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | HESITATION | 3 | True | 98.5 | local event rung |
| gettysburg_dj | gettysburg_jn | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | HESITATION | 3 | True | 99.6 | local event rung |
| gettysburg_dj | gettysburg_pc | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | HESITATION | 3 | True | 98.1 | local event rung |
| gettysburg_dj | gettysburg_wt | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_amb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_dl | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_fb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_jn | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_pc | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dj | gettysburg_wt | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_dj | gettysburg_amb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | BLOCK | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_dj | gettysburg_dl | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | BLOCK | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_dj | gettysburg_fb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | BLOCK | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_dj | gettysburg_jn | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | BLOCK | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_dj | gettysburg_pc | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | BLOCK | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_dj | gettysburg_wt | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | BLOCK | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_amb | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_dl | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_fb | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_jn | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_pc | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_dj | gettysburg_wt | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_dl | gettysburg_amb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_dl | gettysburg_fb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_dl | gettysburg_jn | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_dl | gettysburg_pc | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_dl | gettysburg_wt | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_amb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_amb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | TRAILING_OFF | 2 | False | 98 | local event rung |
| gettysburg_dl | gettysburg_wt | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | TRAILING_OFF | 2 | False | 99.8 | local event rung |
| gettysburg_dl | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_amb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_dl | gettysburg_amb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | BLOCK | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_dl | gettysburg_fb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | BLOCK | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_dl | gettysburg_jn | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | BLOCK | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_dl | gettysburg_pc | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | BLOCK | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_dl | gettysburg_wt | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | BLOCK | 2 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | LOW_EFFORT | 3 | False | 98.1 | local event rung |
| gettysburg_dl | gettysburg_pc | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_amb | HESITATION | 3 | True | 97.8 | local event rung |
| gettysburg_dl | gettysburg_amb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | HESITATION | 3 | True | 98.5 | local event rung |
| gettysburg_dl | gettysburg_fb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | HESITATION | 3 | True | 98.5 | local event rung |
| gettysburg_dl | gettysburg_jn | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | HESITATION | 3 | True | 98.7 | local event rung |
| gettysburg_dl | gettysburg_pc | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | TRAILING_OFF | 3 | False | 96.1 | local event rung |
| gettysburg_dl | gettysburg_wt | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | TRAILING_OFF | 3 | False | 96.8 | local event rung |
| gettysburg_dl | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_amb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_fb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_jn | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_pc | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_dl | gettysburg_wt | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_dl | gettysburg_amb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | BLOCK | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_dl | gettysburg_fb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | BLOCK | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_dl | gettysburg_jn | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | BLOCK | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_dl | gettysburg_pc | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | BLOCK | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_dl | gettysburg_wt | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | BLOCK | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_amb | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_fb | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_jn | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_pc | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_dl | gettysburg_wt | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_fb | gettysburg_amb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_fb | gettysburg_dl | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_fb | gettysburg_jn | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_fb | gettysburg_pc | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_fb | gettysburg_wt | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_amb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_dl | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_dl | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_jn | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_jn | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | TRAILING_OFF | 2 | False | 99.3 | local event rung |
| gettysburg_fb | gettysburg_pc | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_pc | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_wt | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_wt | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | TRAILING_OFF | 2 | False | 98.3 | local event rung |
| gettysburg_fb | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_amb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_dl | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_jn | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_pc | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_wt | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_fb | gettysburg_amb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | BLOCK | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_fb | gettysburg_dl | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | BLOCK | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_fb | gettysburg_jn | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | BLOCK | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_fb | gettysburg_pc | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | BLOCK | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_fb | gettysburg_wt | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | BLOCK | 2 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | HESITATION | 3 | True | 98.6 | local event rung |
| gettysburg_fb | gettysburg_amb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | TRAILING_OFF | 3 | False | 99.6 | local event rung |
| gettysburg_fb | gettysburg_dl | HESITATION | 3 | True | 99.3 | local event rung |
| gettysburg_fb | gettysburg_dl | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_jn | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_jn | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | TRAILING_OFF | 3 | False | 99.7 | local event rung |
| gettysburg_fb | gettysburg_pc | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_pc | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | TRAILING_OFF | 3 | False | 99.9 | local event rung |
| gettysburg_fb | gettysburg_wt | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_wt | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | TRAILING_OFF | 3 | False | 96.5 | local event rung |
| gettysburg_fb | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_amb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_dl | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_jn | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_pc | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_fb | gettysburg_wt | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_fb | gettysburg_amb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | BLOCK | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_fb | gettysburg_dl | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | BLOCK | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_fb | gettysburg_jn | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | BLOCK | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_fb | gettysburg_pc | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | BLOCK | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_fb | gettysburg_wt | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | BLOCK | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_amb | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_dl | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_jn | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_pc | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_fb | gettysburg_wt | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_jn | gettysburg_amb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_jn | gettysburg_dl | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_jn | gettysburg_fb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_jn | gettysburg_pc | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_jn | gettysburg_wt | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_dl | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_fb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_wt | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | LOW_EFFORT | 2 | False | 99.9 | local event rung |
| gettysburg_jn | gettysburg_amb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_amb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | TRAILING_OFF | 2 | False | 98 | local event rung |
| gettysburg_jn | gettysburg_dl | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_dl | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | TRAILING_OFF | 2 | False | 95.8 | local event rung |
| gettysburg_jn | gettysburg_fb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_fb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | TRAILING_OFF | 2 | False | 98.4 | local event rung |
| gettysburg_jn | gettysburg_wt | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_wt | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | TRAILING_OFF | 2 | False | 88 | local event rung |
| gettysburg_jn | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_amb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_dl | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_fb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_wt | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_jn | gettysburg_amb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | BLOCK | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_jn | gettysburg_dl | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | BLOCK | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_jn | gettysburg_fb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | BLOCK | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_jn | gettysburg_pc | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | BLOCK | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_jn | gettysburg_wt | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | BLOCK | 2 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | LOW_EFFORT | 3 | True | 98.4 | local event rung |
| gettysburg_jn | gettysburg_dl | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | LOW_EFFORT | 3 | True | 95 | local event rung |
| gettysburg_jn | gettysburg_fb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | LOW_EFFORT | 3 | True | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | LOW_EFFORT | 3 | True | 98 | local event rung |
| gettysburg_jn | gettysburg_wt | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | LOW_EFFORT | 3 | True | 96.6 | local event rung |
| gettysburg_jn | gettysburg_amb | HESITATION | 3 | True | 98.6 | local event rung |
| gettysburg_jn | gettysburg_amb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | TRAILING_OFF | 3 | False | 91.4 | local event rung |
| gettysburg_jn | gettysburg_dl | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_dl | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | TRAILING_OFF | 3 | False | 87.9 | local event rung |
| gettysburg_jn | gettysburg_fb | HESITATION | 3 | True | 98.5 | local event rung |
| gettysburg_jn | gettysburg_fb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | TRAILING_OFF | 3 | False | 99.9 | local event rung |
| gettysburg_jn | gettysburg_pc | HESITATION | 3 | True | 98.7 | local event rung |
| gettysburg_jn | gettysburg_pc | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | TRAILING_OFF | 3 | False | 88.9 | local event rung |
| gettysburg_jn | gettysburg_wt | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_wt | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | TRAILING_OFF | 3 | False | 78.8 | local event rung |
| gettysburg_jn | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_amb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_dl | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_fb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_pc | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_jn | gettysburg_wt | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_jn | gettysburg_amb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | BLOCK | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_jn | gettysburg_dl | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | BLOCK | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_jn | gettysburg_fb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | BLOCK | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_jn | gettysburg_pc | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | BLOCK | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_jn | gettysburg_wt | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | BLOCK | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_amb | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_dl | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_fb | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_pc | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_jn | gettysburg_wt | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_amb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_pc | gettysburg_amb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_dl | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_pc | gettysburg_dl | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_fb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_pc | gettysburg_fb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_jn | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_pc | gettysburg_jn | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_wt | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_pc | gettysburg_wt | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_amb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_amb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_amb | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_dl | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_dl | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_fb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_fb | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_jn | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_jn | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_wt | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_wt | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_amb | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_dl | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_fb | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_jn | TRAILING_OFF | 2 | True | 99.5 | local event rung |
| gettysburg_pc | gettysburg_wt | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_wt | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_amb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_pc | gettysburg_amb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_amb | BLOCK | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_dl | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_pc | gettysburg_dl | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_dl | BLOCK | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_fb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_pc | gettysburg_fb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_fb | BLOCK | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_jn | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_pc | gettysburg_jn | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_jn | BLOCK | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_wt | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_pc | gettysburg_wt | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_wt | BLOCK | 2 | False |  | local event rung |
| gettysburg_pc | gettysburg_amb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_amb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_amb | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_dl | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_dl | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_fb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_fb | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_jn | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_jn | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_wt | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_wt | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | HESITATION | 3 | True | 97.8 | local event rung |
| gettysburg_pc | gettysburg_amb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_amb | TRAILING_OFF | 3 | True | 99.1 | local event rung |
| gettysburg_pc | gettysburg_dl | HESITATION | 3 | True | 99 | local event rung |
| gettysburg_pc | gettysburg_dl | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_dl | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_fb | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_jn | TRAILING_OFF | 3 | True | 97.3 | local event rung |
| gettysburg_pc | gettysburg_wt | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_wt | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_amb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_dl | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_fb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_jn | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_pc | gettysburg_wt | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_amb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_pc | gettysburg_amb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_amb | BLOCK | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_dl | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_pc | gettysburg_dl | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_dl | BLOCK | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_fb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_pc | gettysburg_fb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_fb | BLOCK | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_jn | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_pc | gettysburg_jn | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_jn | BLOCK | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_wt | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_pc | gettysburg_wt | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_pc | gettysburg_wt | BLOCK | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_sa | gettysburg_amb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_sa | gettysburg_dl | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_sa | gettysburg_fb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_sa | gettysburg_jn | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_sa | gettysburg_pc | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_sa | gettysburg_wt | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | LOW_EFFORT | 2 | True | 98.8 | local event rung |
| gettysburg_sa | gettysburg_jn | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_sa | gettysburg_amb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | BLOCK | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_sa | gettysburg_dl | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | BLOCK | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_sa | gettysburg_fb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | BLOCK | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_sa | gettysburg_jn | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | BLOCK | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_sa | gettysburg_pc | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | BLOCK | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_sa | gettysburg_wt | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | BLOCK | 2 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | LOW_EFFORT | 3 | True | 89.7 | local event rung |
| gettysburg_sa | gettysburg_jn | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | LOW_EFFORT | 3 | True | 96.1 | local event rung |
| gettysburg_sa | gettysburg_pc | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | LOW_EFFORT | 3 | True | 99.9 | local event rung |
| gettysburg_sa | gettysburg_wt | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | LOW_EFFORT | 3 | True | 98.3 | local event rung |
| gettysburg_sa | gettysburg_amb | HESITATION | 3 | True | 95.6 | local event rung |
| gettysburg_sa | gettysburg_amb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | HESITATION | 3 | True | 98 | local event rung |
| gettysburg_sa | gettysburg_dl | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | HESITATION | 3 | True | 96.1 | local event rung |
| gettysburg_sa | gettysburg_fb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | HESITATION | 3 | True | 97.1 | local event rung |
| gettysburg_sa | gettysburg_jn | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | HESITATION | 3 | True | 96.9 | local event rung |
| gettysburg_sa | gettysburg_pc | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_amb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_dl | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_fb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_jn | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_pc | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_sa | gettysburg_wt | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_sa | gettysburg_amb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | BLOCK | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_sa | gettysburg_dl | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | BLOCK | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_sa | gettysburg_fb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | BLOCK | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_sa | gettysburg_jn | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | BLOCK | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_sa | gettysburg_pc | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | BLOCK | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_sa | gettysburg_wt | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | BLOCK | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_amb | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_dl | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_fb | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_jn | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_pc | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_sa | gettysburg_wt | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_tg | gettysburg_amb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_tg | gettysburg_dl | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_tg | gettysburg_fb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_tg | gettysburg_jn | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_tg | gettysburg_pc | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_tg | gettysburg_wt | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | LOW_EFFORT | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | TRAILING_OFF | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_tg | gettysburg_amb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | BLOCK | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_tg | gettysburg_dl | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | BLOCK | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_tg | gettysburg_fb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | BLOCK | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_tg | gettysburg_jn | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | BLOCK | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_tg | gettysburg_pc | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | BLOCK | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_tg | gettysburg_wt | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | BLOCK | 2 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | LOW_EFFORT | 3 | True | 98.9 | local event rung |
| gettysburg_tg | gettysburg_jn | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | LOW_EFFORT | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | HESITATION | 3 | True | 94.8 | local event rung |
| gettysburg_tg | gettysburg_amb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | HESITATION | 3 | True | 99.7 | local event rung |
| gettysburg_tg | gettysburg_dl | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | HESITATION | 3 | True | 98.5 | local event rung |
| gettysburg_tg | gettysburg_jn | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | HESITATION | 3 | True | 98.2 | local event rung |
| gettysburg_tg | gettysburg_pc | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | TRAILING_OFF | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_amb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_dl | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_fb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_jn | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_pc | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_tg | gettysburg_wt | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_tg | gettysburg_amb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | BLOCK | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_tg | gettysburg_dl | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | BLOCK | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_tg | gettysburg_fb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | BLOCK | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_tg | gettysburg_jn | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | BLOCK | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_tg | gettysburg_pc | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | BLOCK | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_tg | gettysburg_wt | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | BLOCK | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_amb | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_dl | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_fb | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_jn | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_pc | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_tg | gettysburg_wt | MISPLACED_EMPHASIS | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_wt | gettysburg_amb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_wt | gettysburg_dl | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_wt | gettysburg_fb | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_wt | gettysburg_jn | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | REPEATED_CONTOUR | 3 |  |  | no detector |
| gettysburg_wt | gettysburg_pc | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | NATURAL_RUSH | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_REPETITION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | TRAILING_OFF | 2 | False | 96.9 | local event rung |
| gettysburg_wt | gettysburg_dl | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | TRAILING_OFF | 2 | False | 93.9 | local event rung |
| gettysburg_wt | gettysburg_fb | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | TRAILING_OFF | 2 | False | 91.1 | local event rung |
| gettysburg_wt | gettysburg_jn | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | TRAILING_OFF | 2 | False | 96.9 | local event rung |
| gettysburg_wt | gettysburg_pc | HESITATION | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | SOUND_REPETITION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | TRAILING_OFF | 2 | False | 98.1 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 2 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | RHYME_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_wt | gettysburg_amb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | BLOCK | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_wt | gettysburg_dl | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | BLOCK | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_wt | gettysburg_fb | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | BLOCK | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_wt | gettysburg_jn | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | BLOCK | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| gettysburg_wt | gettysburg_pc | ONSET_PROLONGATION | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | BLOCK | 2 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | NATURAL_RUSH | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_REPETITION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | HESITATION | 3 | True | 97.1 | local event rung |
| gettysburg_wt | gettysburg_amb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | TRAILING_OFF | 3 | True | 93.2 | local event rung |
| gettysburg_wt | gettysburg_dl | HESITATION | 3 | True | 98.6 | local event rung |
| gettysburg_wt | gettysburg_dl | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | TRAILING_OFF | 3 | False | 90.3 | local event rung |
| gettysburg_wt | gettysburg_fb | HESITATION | 3 | True | 98 | local event rung |
| gettysburg_wt | gettysburg_fb | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | TRAILING_OFF | 3 | False | 86.1 | local event rung |
| gettysburg_wt | gettysburg_jn | HESITATION | 3 | True | 99.5 | local event rung |
| gettysburg_wt | gettysburg_jn | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | TRAILING_OFF | 3 | True | 92.4 | local event rung |
| gettysburg_wt | gettysburg_pc | HESITATION | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | SOUND_REPETITION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | TRAILING_OFF | 3 | False | 95.4 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_amb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_dl | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_fb | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_jn | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | WORD_BY_WORD | 3 | False | 100 | local event rung |
| gettysburg_wt | gettysburg_pc | RHYME_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_wt | gettysburg_amb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | BLOCK | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_wt | gettysburg_dl | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | BLOCK | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_wt | gettysburg_fb | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | BLOCK | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_wt | gettysburg_jn | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | BLOCK | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| gettysburg_wt | gettysburg_pc | ONSET_PROLONGATION | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | BLOCK | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_amb | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_dl | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_fb | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_jn | RISING_ENDING | 3 | False |  | local event rung |
| gettysburg_wt | gettysburg_pc | RISING_ENDING | 3 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | REPEATED_CONTOUR | 3 |  |  | no detector |
| greenman_reagan | reagan_farewell_1989 | FLAT_FINAL_FALL | 3 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | NATURAL_RUSH | 2 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_REPETITION | 2 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | LOW_EFFORT | 2 | True | 99.9 | local event rung |
| greenman_reagan | reagan_farewell_1989 | HESITATION | 2 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | SOUND_REPETITION | 2 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | TRAILING_OFF | 2 | False | 99.6 | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_BY_WORD | 2 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_BY_WORD | 2 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_BY_WORD | 2 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_BY_WORD | 2 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_BY_WORD | 2 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_BY_WORD | 2 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | RHYME_PROLONGATION | 2 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | UNEVEN_TEMPO | 2 | False |  | whole-clip rung |
| greenman_reagan | reagan_farewell_1989 | ONSET_PROLONGATION | 2 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | BLOCK | 2 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | NATURAL_RUSH | 3 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_REPETITION | 3 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | LOW_EFFORT | 3 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | HESITATION | 3 | True | 99.6 | local event rung |
| greenman_reagan | reagan_farewell_1989 | SOUND_REPETITION | 3 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | TRAILING_OFF | 3 | False | 98.8 | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_BY_WORD | 3 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_BY_WORD | 3 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_BY_WORD | 3 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_BY_WORD | 3 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_BY_WORD | 3 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | WORD_BY_WORD | 3 | False | 100 | local event rung |
| greenman_reagan | reagan_farewell_1989 | RHYME_PROLONGATION | 3 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | UNEVEN_TEMPO | 3 | False |  | whole-clip rung |
| greenman_reagan | reagan_farewell_1989 | ONSET_PROLONGATION | 3 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | BLOCK | 3 | False |  | local event rung |
| greenman_reagan | reagan_farewell_1989 | MISPLACED_EMPHASIS | 3 | False |  | local event rung |

Stated limits (whole-clip flag raised in fewer than 50% of the pairs):

- whole-passage RUSH L1: whole-clip flag raised in 0/18 check-reader pairs
- whole-passage RUSH L2: whole-clip flag raised in 1/18 check-reader pairs

## Trivial baselines (L2 + L3, splits not used for fitting)

Detector, core8, TP/FP/FN under the accounting the evaluation plan fixed (pre-registered: every region not matched by its own key is false): val headline (L2+L3) 30/13/2, F1 0.8; test headline (L2+L3) 28/9/4, F1 0.812; val+test headline (L2+L3) 58/22/6, F1 0.806. The detector F1 in the next table counts one detection per change (one detection per change; same-change duplicates reported separately), an accounting adopted after the plan.

The detector row equals the strict headline row of each tier (same truths: unscored dimensions are not truths). flag_all flags every five-word window and every event unit of each scored dimension: a recall ceiling at IoU >= 0.5. reference_free is the same detector with no reference reading: every measure is taken against the participant's own median over the clip (pauses: per punctuation class); emphasis and the whole-clip measures need a reference and are absent. The difference between the detector and reference_free rows is what the reference reading adds. Train-chosen reference-free h: 2.75 (in-sample train core8 L2+L3 strict F1 maximum on the R1 common grid; ties use smaller h).

core8:

| split | method | TP | FP | FN | same-change duplicates (not FP) | F1 |
|---|---|---|---|---|---|---|
| val | detector | 30 | 9 | 2 | 4 | 0.845 |
| val | no_flags | 0 | 0 | 32 | 0 | 0 |
| val | flag_all | 32 | 4000 | 0 | 492 | 0.016 |
| val | random | 1.45 | 30.6 | 30.6 | 0 | 0.045 |
| val | reference_free (detector h) | 20 | 132 | 12 | 31 | 0.217 |
| val | reference_free (train-chosen h=2.75) | 17 | 107 | 15 | 31 | 0.218 |
| test | detector | 29 | 5 | 3 | 3 | 0.879 |
| test | no_flags | 0 | 0 | 32 | 0 | 0 |
| test | flag_all | 32 | 3940 | 0 | 484 | 0.016 |
| test | random | 1.8 | 30.2 | 30.2 | 0 | 0.056 |
| test | reference_free (detector h) | 19 | 103 | 13 | 33 | 0.247 |
| test | reference_free (train-chosen h=2.75) | 18 | 88 | 14 | 30 | 0.261 |
| val+test | detector | 59 | 14 | 5 | 7 | 0.861 |
| val+test | no_flags | 0 | 0 | 64 | 0 | 0 |
| val+test | flag_all | 64 | 7940 | 0 | 976 | 0.016 |
| val+test | random | 3.25 | 60.8 | 60.8 | 0 | 0.051 |
| val+test | reference_free (detector h) | 39 | 235 | 25 | 64 | 0.231 |
| val+test | reference_free (train-chosen h=2.75) | 35 | 195 | 29 | 61 | 0.238 |

lab_passed:

| split | method | TP | FP | FN | same-change duplicates (not FP) | F1 |
|---|---|---|---|---|---|---|
| val | detector | 1 | 6 | 3 | 0 | 0.182 |
| val | no_flags | 0 | 0 | 4 | 0 | 0 |
| val | flag_all | 4 | 1500 | 0 | 225 | 0.005 |
| val | random | 0.25 | 2.4 | 3.75 | 0 | 0.075 |
| val | reference_free (detector h) | 4 | 55 | 0 | 14 | 0.127 |
| val | reference_free (train-chosen h=2.75) | 2 | 41 | 2 | 14 | 0.085 |
| test | detector | 1 | 7 | 3 | 0 | 0.167 |
| test | no_flags | 0 | 0 | 4 | 0 | 0 |
| test | flag_all | 4 | 1510 | 0 | 228 | 0.005 |
| test | random | 0.35 | 2.5 | 3.65 | 0 | 0.102 |
| test | reference_free (detector h) | 2 | 40 | 2 | 14 | 0.087 |
| test | reference_free (train-chosen h=2.75) | 2 | 33 | 2 | 14 | 0.103 |
| val+test | detector | 2 | 13 | 6 | 0 | 0.174 |
| val+test | no_flags | 0 | 0 | 8 | 0 | 0 |
| val+test | flag_all | 8 | 3010 | 0 | 453 | 0.005 |
| val+test | random | 0.6 | 4.9 | 7.4 | 0 | 0.089 |
| val+test | reference_free (detector h) | 6 | 95 | 2 | 28 | 0.11 |
| val+test | reference_free (train-chosen h=2.75) | 4 | 74 | 4 | 28 | 0.093 |

synthetic_only (unvalidated):

| split | method | TP | FP | FN | same-change duplicates (not FP) | F1 |
|---|---|---|---|---|---|---|
| val | detector | 5 | 19 | 23 | 0 | 0.192 |
| val | no_flags | 0 | 0 | 28 | 0 | 0 |
| val | flag_all | 26 | 7320 | 2 | 877 | 0.007 |
| val | random | 1.1 | 44.5 | 26.9 | 0 | 0.03 |
| val | reference_free (detector h) | 9 | 250 | 19 | 70 | 0.063 |
| val | reference_free (train-chosen h=2.75) | 6 | 203 | 22 | 71 | 0.051 |
| test | detector | 8 | 28 | 32 | 0 | 0.211 |
| test | no_flags | 0 | 0 | 40 | 0 | 0 |
| test | flag_all | 40 | 7380 | 0 | 892 | 0.011 |
| test | random | 3.5 | 60.2 | 36.5 | 0 | 0.067 |
| test | reference_free (detector h) | 9 | 225 | 31 | 67 | 0.066 |
| test | reference_free (train-chosen h=2.75) | 7 | 188 | 33 | 64 | 0.06 |
| val+test | detector | 13 | 47 | 55 | 0 | 0.203 |
| val+test | no_flags | 0 | 0 | 68 | 0 | 0 |
| val+test | flag_all | 66 | 14700 | 2 | 1770 | 0.009 |
| val+test | random | 4.6 | 105 | 63.4 | 0 | 0.052 |
| val+test | reference_free (detector h) | 18 | 475 | 50 | 137 | 0.064 |
| val+test | reference_free (train-chosen h=2.75) | 13 | 391 | 55 | 135 | 0.055 |

## Stress matrix

| split | condition | regime | reference mode | recordings | seeds | comparison-minutes (all seeds) | added/min | interval | removed/min | interval | detections before (unique) | kept (all seeds) | kept fraction | interval | kept in every seed | max score change |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| train | gain +6 dB | R1 |  | 145 | [1] | 65.3 | 0.199 | 95% [0.093, 0.321] | 0.184 | 95% [0.031, 0.408] | 198 | 195/198 | 0.985 | 95% [0.965, 1] | 195/198 | 5.92 |
| train | gain +6 dB | R2 | single | 22 | [1] | 11.9 | 0 | 95% [0, 0.31] | 0 | 95% [0, 0.31] | 8 | 8/8 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 8/8 | 0.146 |
| train | gain -6 dB | R1 |  | 145 | [1] | 65.3 | 0.0918 | 95% [0.03, 0.182] | 0.107 | 95% [0.031, 0.201] | 198 | 196/198 | 0.99 | 95% [0.974, 1] | 196/198 | 7.46 |
| train | gain -6 dB | R2 | single | 22 | [1] | 11.9 | 0 | 95% [0, 0.31] | 0 | 95% [0, 0.31] | 8 | 8/8 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 8/8 | 9.8 |
| train | low-pass 3.4 kHz | R1 |  | 145 | [1] | 65.3 | 1.61 | 95% [1.31, 1.95] | 0.49 | 95% [0.27, 0.737] | 198 | 192/198 | 0.97 | 95% [0.942, 0.99] | 192/198 | 7.65 |
| train | low-pass 3.4 kHz | R2 | single | 22 | [1] | 11.9 | 0 | 95% [0, 0.31] | 0.0842 | 95% [0, 0.263] | 8 | 7/8 | 0.875 | 95% [0.5, 1] | 7/8 | 9.81 |
| train | white noise 20 dB SNR | R1 |  | 145 | [1, 2, 3] | 196 | 2.39 | 95% [1.83, 3.07] | 1.01 | 95% [0.659, 1.4] | 198 | 525/594 | 0.884 | 95% [0.839, 0.922] | 171/198 | 10.2 |
| train | white noise 20 dB SNR | R2 | single | 22 | [1, 2, 3] | 35.6 | 0 | 95% [0, 0.31] | 0.589 | 95% [0.174, 1.09] | 8 | 18/24 | 0.75 | 95% [0.429, 1] | 6/8 | 9.91 |
| train | MP3 64 kbit/s | R1 |  | 145 | [1] | 65.3 | 0.0765 | 95% [0.015, 0.151] | 0.0612 | 95% [0.015, 0.126] | 198 | 195/198 | 0.985 | 95% [0.966, 1] | 195/198 | 2.11 |
| train | MP3 64 kbit/s | R2 | single | 22 | [1] | 11.9 | 0.0842 | 95% [0, 0.26] | 0 | 95% [0, 0.31] | 8 | 8/8 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 8/8 | 0.761 |
| train | dynamic-range compression | R1 |  | 145 | [1] | 65.3 | 2.94 | 95% [2.47, 3.49] | 1.32 | 95% [0.98, 1.67] | 198 | 157/198 | 0.793 | 95% [0.724, 0.851] | 157/198 | 14.2 |
| train | dynamic-range compression | R2 | single | 22 | [1] | 11.9 | 0 | 95% [0, 0.31] | 0.421 | 95% [0.082, 0.905] | 8 | 4/8 | 0.5 | 95% [0.111, 0.875] | 4/8 | 1.27 |
| train | room reverb RT60 0.4 s | R1 |  | 145 | [1, 2, 3] | 196 | 0.964 | 95% [0.711, 1.24] | 0.633 | 95% [0.39, 0.895] | 198 | 563/594 | 0.948 | 95% [0.912, 0.976] | 184/198 | 12 |
| train | room reverb RT60 0.4 s | R2 | single | 22 | [1, 2, 3] | 35.6 | 0.365 | 95% [0.056, 0.754] | 0.73 | 95% [0.253, 1.3] | 8 | 15/24 | 0.625 | 95% [0.142, 1] | 5/8 | 9.34 |
| train | phone band + mu-law (participant only) | R1 |  | 145 | [1] | 65.3 | 1.99 | 95% [1.63, 2.35] | 0.735 | 95% [0.428, 1.11] | 198 | 185/198 | 0.934 | 95% [0.898, 0.966] | 185/198 | 10.5 |
| train | phone band + mu-law (participant only) | R2 | single | 22 | [1] | 11.9 | 0.0842 | 95% [0, 0.26] | 0.253 | 95% [0, 0.569] | 8 | 6/8 | 0.75 | 95% [0.375, 1] | 6/8 | 9.86 |
| train | WORLD speaker transform | R1 |  | 145 | [1] | 65.3 | 0.52 | 95% [0.346, 0.695] | 0.428 | 95% [0.225, 0.692] | 198 | 193/198 | 0.975 | 95% [0.951, 0.995] | 193/198 | 6.11 |
| train | WORLD speaker transform | R2 | single | 22 | [1] | 11.9 | 0 | 95% [0, 0.31] | 0.337 | 95% [0.083, 0.66] | 8 | 6/8 | 0.75 | 95% [0.429, 1] | 6/8 | 0.739 |
| train | babble 10 dB SNR | R1 |  | 145 | [1, 2, 3] | 196 | 30.4 | 95% [28.2, 32.4] | 2.71 | 95% [2.21, 3.23] | 198 | 359/594 | 0.604 | 95% [0.509, 0.691] | 93/198 | 33.8 |
| train | babble 10 dB SNR | R2 | single | 22 | [1, 2, 3] | 35.6 | 0.982 | 95% [0.656, 1.47] | 1.46 | 95% [0.8, 2.19] | 8 | 1/24 | 0.0417 | 95% [0, 0.111] | 0/8 | 25.7 |
| train | babble 20 dB SNR | R1 |  | 145 | [1, 2, 3] | 196 | 13.6 | 95% [12, 15.2] | 0.969 | 95% [0.666, 1.31] | 198 | 522/594 | 0.879 | 95% [0.826, 0.919] | 156/198 | 23.5 |
| train | babble 20 dB SNR | R2 | single | 22 | [1, 2, 3] | 35.6 | 0.112 | 95% [0, 0.311] | 1.09 | 95% [0.557, 1.69] | 8 | 5/24 | 0.208 | 95% [0, 0.481] | 1/8 | 2.6 |
| val | gain +6 dB | R1 |  | 58 | [1] | 28.9 | 0.208 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.069; range [0.069, 0.346] | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] | 73 | 73/73 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 73/73 | 0.835 |
| val | gain -6 dB | R1 |  | 58 | [1] | 28.9 | 0.277 | per speaker: eisenhower_farewell_1961 0.415, lbush_radio_2001 0.139; range [0.139, 0.415] | 0.104 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069; range [0.069, 0.138] | 73 | 73/73 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 73/73 | 2.86 |
| val | low-pass 3.4 kHz | R1 |  | 58 | [1] | 28.9 | 0.381 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 0.278; range [0.278, 0.484] | 0.416 | per speaker: eisenhower_farewell_1961 0.623, lbush_radio_2001 0.208; range [0.208, 0.623] | 73 | 70/73 | 0.959 | per speaker: eisenhower_farewell_1961 0.973, lbush_radio_2001 0.944; range [0.944, 0.973] | 70/73 | 5.61 |
| val | white noise 20 dB SNR | R1 |  | 58 | [1, 2, 3] | 86.6 | 2.63 | per speaker: eisenhower_farewell_1961 1.96, lbush_radio_2001 3.31; range [1.96, 3.31] | 0.739 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 0.879; range [0.6, 0.879] | 73 | 199/219 | 0.909 | per speaker: eisenhower_farewell_1961 0.928, lbush_radio_2001 0.889; range [0.889, 0.928] | 64/73 | 10.1 |
| val | MP3 64 kbit/s | R1 |  | 58 | [1] | 28.9 | 0.0693 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0; range [0, 0.138] | 0.0693 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0; range [0, 0.138] | 73 | 73/73 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 73/73 | 0.527 |
| val | dynamic-range compression | R1 |  | 58 | [1] | 28.9 | 6.48 | per speaker: eisenhower_farewell_1961 8.03, lbush_radio_2001 4.93; range [4.93, 8.03] | 1.56 | per speaker: eisenhower_farewell_1961 1.94, lbush_radio_2001 1.18; range [1.18, 1.94] | 73 | 57/73 | 0.781 | per speaker: eisenhower_farewell_1961 0.757, lbush_radio_2001 0.806; range [0.757, 0.806] | 57/73 | 18.5 |
| val | room reverb RT60 0.4 s | R1 |  | 58 | [1, 2, 3] | 86.6 | 0.889 | per speaker: eisenhower_farewell_1961 0.969, lbush_radio_2001 0.81; range [0.81, 0.969] | 0.635 | per speaker: eisenhower_farewell_1961 0.784, lbush_radio_2001 0.486; range [0.486, 0.784] | 73 | 208/219 | 0.95 | per speaker: eisenhower_farewell_1961 0.964, lbush_radio_2001 0.935; range [0.935, 0.964] | 68/73 | 14.7 |
| val | phone band + mu-law (participant only) | R1 |  | 58 | [1] | 28.9 | 1.84 | per speaker: eisenhower_farewell_1961 2.91, lbush_radio_2001 0.764; range [0.764, 2.91] | 0.624 | per speaker: eisenhower_farewell_1961 0.623, lbush_radio_2001 0.625; range [0.623, 0.625] | 73 | 65/73 | 0.89 | per speaker: eisenhower_farewell_1961 0.946, lbush_radio_2001 0.833; range [0.833, 0.946] | 65/73 | 6.17 |
| val | WORLD speaker transform | R1 |  | 58 | [1] | 28.9 | 0.936 | per speaker: eisenhower_farewell_1961 1.45, lbush_radio_2001 0.417; range [0.417, 1.45] | 0.485 | per speaker: eisenhower_farewell_1961 0.692, lbush_radio_2001 0.278; range [0.278, 0.692] | 73 | 70/73 | 0.959 | per speaker: eisenhower_farewell_1961 0.973, lbush_radio_2001 0.944; range [0.944, 0.973] | 70/73 | 14.8 |
| val | babble 10 dB SNR | R1 |  | 58 | [1, 2, 3] | 86.6 | 24.5 | per speaker: eisenhower_farewell_1961 27.2, lbush_radio_2001 21.8; range [21.8, 27.2] | 2.33 | per speaker: eisenhower_farewell_1961 2.7, lbush_radio_2001 1.97; range [1.97, 2.7] | 73 | 143/219 | 0.653 | per speaker: eisenhower_farewell_1961 0.694, lbush_radio_2001 0.611; range [0.611, 0.694] | 38/73 | 26.8 |
| val | babble 20 dB SNR | R1 |  | 58 | [1, 2, 3] | 86.6 | 8.41 | per speaker: eisenhower_farewell_1961 10.6, lbush_radio_2001 6.18; range [6.18, 10.6] | 1.18 | per speaker: eisenhower_farewell_1961 1.5, lbush_radio_2001 0.856; range [0.856, 1.5] | 73 | 194/219 | 0.886 | per speaker: eisenhower_farewell_1961 0.91, lbush_radio_2001 0.861; range [0.861, 0.91] | 61/73 | 19.7 |
| test | gain +6 dB | R1 |  | 58 | [1] | 28.8 | 0.139 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.138, 0.139] | 0.173 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.346; range [0, 0.346] | 78 | 78/78 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 78/78 | 3.71 |
| test | gain -6 dB | R1 |  | 58 | [1] | 28.8 | 0.278 | per speaker: mobama_weekly_2014 0.418, nixon_resignation_1974 0.138; range [0.138, 0.418] | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] | 78 | 78/78 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 78/78 | 15.5 |
| test | low-pass 3.4 kHz | R1 |  | 58 | [1] | 28.8 | 1.46 | per speaker: mobama_weekly_2014 2.44, nixon_resignation_1974 0.484; range [0.484, 2.44] | 0.659 | per speaker: mobama_weekly_2014 0.836, nixon_resignation_1974 0.484; range [0.484, 0.836] | 78 | 73/78 | 0.936 | per speaker: mobama_weekly_2014 0.895, nixon_resignation_1974 0.975; range [0.895, 0.975] | 73/78 | 16.6 |
| test | white noise 20 dB SNR | R1 |  | 58 | [1, 2, 3] | 86.5 | 1.85 | per speaker: mobama_weekly_2014 1.39, nixon_resignation_1974 2.31; range [1.39, 2.31] | 0.729 | per speaker: mobama_weekly_2014 0.603, nixon_resignation_1974 0.853; range [0.603, 0.853] | 78 | 213/234 | 0.91 | per speaker: mobama_weekly_2014 0.895, nixon_resignation_1974 0.925; range [0.895, 0.925] | 71/78 | 16.6 |
| test | MP3 64 kbit/s | R1 |  | 58 | [1] | 28.8 | 0.139 | per speaker: mobama_weekly_2014 0.279, nixon_resignation_1974 0; range [0, 0.279] | 0.104 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.207; range [0, 0.207] | 78 | 78/78 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 78/78 | 11.8 |
| test | dynamic-range compression | R1 |  | 58 | [1] | 28.8 | 2.6 | per speaker: mobama_weekly_2014 2.16, nixon_resignation_1974 3.04; range [2.16, 3.04] | 1.49 | per speaker: mobama_weekly_2014 1.46, nixon_resignation_1974 1.52; range [1.46, 1.52] | 78 | 59/78 | 0.756 | per speaker: mobama_weekly_2014 0.737, nixon_resignation_1974 0.775; range [0.737, 0.775] | 59/78 | 13.2 |
| test | room reverb RT60 0.4 s | R1 |  | 58 | [1, 2, 3] | 86.5 | 0.613 | per speaker: mobama_weekly_2014 0.743, nixon_resignation_1974 0.484; range [0.484, 0.743] | 0.44 | per speaker: mobama_weekly_2014 0.186, nixon_resignation_1974 0.691; range [0.186, 0.691] | 78 | 231/234 | 0.987 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0.975; range [0.975, 1] | 75/78 | 14.3 |
| test | phone band + mu-law (participant only) | R1 |  | 58 | [1] | 28.8 | 5.52 | per speaker: mobama_weekly_2014 2.3, nixon_resignation_1974 8.71; range [2.3, 8.71] | 0.763 | per speaker: mobama_weekly_2014 0.557, nixon_resignation_1974 0.968; range [0.557, 0.968] | 78 | 68/78 | 0.872 | per speaker: mobama_weekly_2014 0.842, nixon_resignation_1974 0.9; range [0.842, 0.9] | 68/78 | 32.1 |
| test | WORLD speaker transform | R1 |  | 58 | [1] | 28.8 | 0.763 | per speaker: mobama_weekly_2014 0.836, nixon_resignation_1974 0.691; range [0.691, 0.836] | 0.798 | per speaker: mobama_weekly_2014 0.766, nixon_resignation_1974 0.83; range [0.766, 0.83] | 78 | 77/78 | 0.987 | per speaker: mobama_weekly_2014 0.974, nixon_resignation_1974 1; range [0.974, 1] | 77/78 | 14.9 |
| test | babble 10 dB SNR | R1 |  | 58 | [1, 2, 3] | 86.5 | 26.2 | per speaker: mobama_weekly_2014 20.4, nixon_resignation_1974 31.9; range [20.4, 31.9] | 2.66 | per speaker: mobama_weekly_2014 1.81, nixon_resignation_1974 3.5; range [1.81, 3.5] | 78 | 141/234 | 0.603 | per speaker: mobama_weekly_2014 0.693, nixon_resignation_1974 0.517; range [0.517, 0.693] | 40/78 | 28.9 |
| test | babble 20 dB SNR | R1 |  | 58 | [1, 2, 3] | 86.5 | 13.2 | per speaker: mobama_weekly_2014 2.81, nixon_resignation_1974 23.6; range [2.81, 23.6] | 1.25 | per speaker: mobama_weekly_2014 0.743, nixon_resignation_1974 1.75; range [0.743, 1.75] | 78 | 200/234 | 0.855 | per speaker: mobama_weekly_2014 0.947, nixon_resignation_1974 0.767; range [0.767, 0.947] | 59/78 | 28.3 |
| val+test | gain +6 dB | R1 |  | 116 | [1] | 57.7 | 0.173 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.069, mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.069, 0.346] | 0.104 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.346; range [0, 0.346] | 151 | 151/151 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 151/151 | 3.71 |
| val+test | gain -6 dB | R1 |  | 116 | [1] | 57.7 | 0.277 | per speaker: eisenhower_farewell_1961 0.415, lbush_radio_2001 0.139, mobama_weekly_2014 0.418, nixon_resignation_1974 0.138; range [0.138, 0.418] | 0.0867 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.138] | 151 | 151/151 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 151/151 | 15.5 |
| val+test | low-pass 3.4 kHz | R1 |  | 116 | [1] | 57.7 | 0.919 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 0.278, mobama_weekly_2014 2.44, nixon_resignation_1974 0.484; range [0.278, 2.44] | 0.537 | per speaker: eisenhower_farewell_1961 0.623, lbush_radio_2001 0.208, mobama_weekly_2014 0.836, nixon_resignation_1974 0.484; range [0.208, 0.836] | 151 | 143/151 | 0.947 | per speaker: eisenhower_farewell_1961 0.973, lbush_radio_2001 0.944, mobama_weekly_2014 0.895, nixon_resignation_1974 0.975; range [0.895, 0.975] | 143/151 | 16.6 |
| val+test | white noise 20 dB SNR | R1 |  | 116 | [1, 2, 3] | 173 | 2.24 | per speaker: eisenhower_farewell_1961 1.96, lbush_radio_2001 3.31, mobama_weekly_2014 1.39, nixon_resignation_1974 2.31; range [1.39, 3.31] | 0.734 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 0.879, mobama_weekly_2014 0.603, nixon_resignation_1974 0.853; range [0.6, 0.879] | 151 | 412/453 | 0.909 | per speaker: eisenhower_farewell_1961 0.928, lbush_radio_2001 0.889, mobama_weekly_2014 0.895, nixon_resignation_1974 0.925; range [0.889, 0.928] | 135/151 | 16.6 |
| val+test | MP3 64 kbit/s | R1 |  | 116 | [1] | 57.7 | 0.104 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0, mobama_weekly_2014 0.279, nixon_resignation_1974 0; range [0, 0.279] | 0.0867 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.207; range [0, 0.207] | 151 | 151/151 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 151/151 | 11.8 |
| val+test | dynamic-range compression | R1 |  | 116 | [1] | 57.7 | 4.54 | per speaker: eisenhower_farewell_1961 8.03, lbush_radio_2001 4.93, mobama_weekly_2014 2.16, nixon_resignation_1974 3.04; range [2.16, 8.03] | 1.53 | per speaker: eisenhower_farewell_1961 1.94, lbush_radio_2001 1.18, mobama_weekly_2014 1.46, nixon_resignation_1974 1.52; range [1.18, 1.94] | 151 | 116/151 | 0.768 | per speaker: eisenhower_farewell_1961 0.757, lbush_radio_2001 0.806, mobama_weekly_2014 0.737, nixon_resignation_1974 0.775; range [0.737, 0.806] | 116/151 | 18.5 |
| val+test | room reverb RT60 0.4 s | R1 |  | 116 | [1, 2, 3] | 173 | 0.751 | per speaker: eisenhower_farewell_1961 0.969, lbush_radio_2001 0.81, mobama_weekly_2014 0.743, nixon_resignation_1974 0.484; range [0.484, 0.969] | 0.537 | per speaker: eisenhower_farewell_1961 0.784, lbush_radio_2001 0.486, mobama_weekly_2014 0.186, nixon_resignation_1974 0.691; range [0.186, 0.784] | 151 | 439/453 | 0.969 | per speaker: eisenhower_farewell_1961 0.964, lbush_radio_2001 0.935, mobama_weekly_2014 1, nixon_resignation_1974 0.975; range [0.935, 1] | 143/151 | 14.7 |
| val+test | phone band + mu-law (participant only) | R1 |  | 116 | [1] | 57.7 | 3.68 | per speaker: eisenhower_farewell_1961 2.91, lbush_radio_2001 0.764, mobama_weekly_2014 2.3, nixon_resignation_1974 8.71; range [0.764, 8.71] | 0.693 | per speaker: eisenhower_farewell_1961 0.623, lbush_radio_2001 0.625, mobama_weekly_2014 0.557, nixon_resignation_1974 0.968; range [0.557, 0.968] | 151 | 133/151 | 0.881 | per speaker: eisenhower_farewell_1961 0.946, lbush_radio_2001 0.833, mobama_weekly_2014 0.842, nixon_resignation_1974 0.9; range [0.833, 0.946] | 133/151 | 32.1 |
| val+test | WORLD speaker transform | R1 |  | 116 | [1] | 57.7 | 0.85 | per speaker: eisenhower_farewell_1961 1.45, lbush_radio_2001 0.417, mobama_weekly_2014 0.836, nixon_resignation_1974 0.691; range [0.417, 1.45] | 0.641 | per speaker: eisenhower_farewell_1961 0.692, lbush_radio_2001 0.278, mobama_weekly_2014 0.766, nixon_resignation_1974 0.83; range [0.278, 0.83] | 151 | 147/151 | 0.974 | per speaker: eisenhower_farewell_1961 0.973, lbush_radio_2001 0.944, mobama_weekly_2014 0.974, nixon_resignation_1974 1; range [0.944, 1] | 147/151 | 14.9 |
| val+test | babble 10 dB SNR | R1 |  | 116 | [1, 2, 3] | 173 | 25.3 | per speaker: eisenhower_farewell_1961 27.2, lbush_radio_2001 21.8, mobama_weekly_2014 20.4, nixon_resignation_1974 31.9; range [20.4, 31.9] | 2.5 | per speaker: eisenhower_farewell_1961 2.7, lbush_radio_2001 1.97, mobama_weekly_2014 1.81, nixon_resignation_1974 3.5; range [1.81, 3.5] | 151 | 284/453 | 0.627 | per speaker: eisenhower_farewell_1961 0.694, lbush_radio_2001 0.611, mobama_weekly_2014 0.693, nixon_resignation_1974 0.517; range [0.517, 0.694] | 78/151 | 28.9 |
| val+test | babble 20 dB SNR | R1 |  | 116 | [1, 2, 3] | 173 | 10.8 | per speaker: eisenhower_farewell_1961 10.6, lbush_radio_2001 6.18, mobama_weekly_2014 2.81, nixon_resignation_1974 23.6; range [2.81, 23.6] | 1.21 | per speaker: eisenhower_farewell_1961 1.5, lbush_radio_2001 0.856, mobama_weekly_2014 0.743, nixon_resignation_1974 1.75; range [0.743, 1.75] | 151 | 394/453 | 0.87 | per speaker: eisenhower_farewell_1961 0.91, lbush_radio_2001 0.861, mobama_weekly_2014 0.947, nixon_resignation_1974 0.767; range [0.767, 0.947] | 120/151 | 28.3 |
| check readers | gain +6 dB | R2 | single | 3 | [1] | 7.76 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 3.45 |
| check readers | gain +6 dB | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 3.1 |
| check readers | gain -6 dB | R2 | single | 3 | [1] | 7.76 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 0.153 |
| check readers | gain -6 dB | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 0.343 |
| check readers | low-pass 3.4 kHz | R2 | single | 3 | [1] | 7.76 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 1.19 |
| check readers | low-pass 3.4 kHz | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 1.77 |
| check readers | white noise 20 dB SNR | R2 | single | 3 | [1, 2, 3] | 23.3 | 0.258 | per recording: gettysburg_dj 0, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.662] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 3.21 |
| check readers | white noise 20 dB SNR | R2 | consensus5 | 3 | [1, 2, 3] | 3.88 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 1.32 |
| check readers | MP3 64 kbit/s | R2 | single | 3 | [1] | 7.76 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 0.058 |
| check readers | MP3 64 kbit/s | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 1.02 |
| check readers | dynamic-range compression | R2 | single | 3 | [1] | 7.76 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 4.76 |
| check readers | dynamic-range compression | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 2.41 |
| check readers | room reverb RT60 0.4 s | R2 | single | 3 | [1, 2, 3] | 23.3 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 15.5 |
| check readers | room reverb RT60 0.4 s | R2 | consensus5 | 3 | [1, 2, 3] | 3.88 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 8.28 |
| check readers | phone band + mu-law (participant only) | R2 | single | 3 | [1] | 7.76 | 0.387 | per recording: gettysburg_dj 0.437, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.662] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 18.3 |
| check readers | phone band + mu-law (participant only) | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 8.28 |
| check readers | WORLD speaker transform | R2 | single | 3 | [1] | 7.76 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 5.28 |
| check readers | WORLD speaker transform | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 3.41 |
| check readers | babble 10 dB SNR | R2 | single | 3 | [1, 2, 3] | 23.3 | 2.06 | per recording: gettysburg_dj 3.79, gettysburg_sa 1.77, gettysburg_tg 0.817; range [0.817, 3.79] | 0.258 | per recording: gettysburg_dj 0, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.662] | 0 | 0/0 |  | n/a | 0/0 | 20.6 |
| check readers | babble 10 dB SNR | R2 | consensus5 | 3 | [1, 2, 3] | 3.88 | 5.41 | per recording: gettysburg_dj 8.73, gettysburg_sa 5.3, gettysburg_tg 2.45; range [2.45, 8.73] | 1.55 | per recording: gettysburg_dj 2.62, gettysburg_sa 1.99, gettysburg_tg 0; range [0, 2.62] | 0 | 0/0 |  | n/a | 0/0 | 8.25 |
| check readers | babble 20 dB SNR | R2 | single | 3 | [1, 2, 3] | 23.3 | 0.129 | per recording: gettysburg_dj 0.146, gettysburg_sa 0, gettysburg_tg 0.272; range [0, 0.272] | 0.0859 | per recording: gettysburg_dj 0, gettysburg_sa 0.221, gettysburg_tg 0; range [0, 0.221] | 0 | 0/0 |  | n/a | 0/0 | 14.9 |
| check readers | babble 20 dB SNR | R2 | consensus5 | 3 | [1, 2, 3] | 3.88 | 1.8 | per recording: gettysburg_dj 0.873, gettysburg_sa 1.99, gettysburg_tg 2.45; range [0.873, 2.45] | 0.516 | per recording: gettysburg_dj 0.873, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.873] | 0 | 0/0 |  | n/a | 0/0 | 15.6 |

Conditions that break keys (stated limits; added local regions above the per-key share of the false-region budget, or detections kept below 95%):

| split | condition | regime | reference mode | limit |
|---|---|---|---|---|
| train | low-pass 3.4 kHz | R1 |  | adds D1- regions: 1.21/min [0.96, 1.49] against the per-key share 0.0556/min |
| train | low-pass 3.4 kHz | R2 | single | loses D5- detections: kept 3/4 (0.75) (no interval: fewer than 5 recordings) |
| train | white noise 20 dB SNR | R1 |  | adds D1+ regions: 0.178/min [0.063, 0.336] against the per-key share 0.0556/min |
| train | white noise 20 dB SNR | R1 |  | adds D1- regions: 0.76/min [0.561, 0.998] against the per-key share 0.0556/min |
| train | white noise 20 dB SNR | R1 |  | adds D2+ regions: 0.485/min [0.226, 0.873] against the per-key share 0.0556/min |
| train | white noise 20 dB SNR | R1 |  | adds D9- regions: 0.837/min [0.555, 1.12] against the per-key share 0.0556/min |
| train | white noise 20 dB SNR | R1 |  | loses D5- detections: kept 99/135 (0.733) [0.626, 0.83] |
| train | white noise 20 dB SNR | R1 |  | loses D6- detections: kept 10/30 (0.333) [0.067, 0.6] |
| train | white noise 20 dB SNR | R1 |  | loses D9- detections: kept 6/9 (0.667) (no interval: fewer than 5 recordings) |
| train | white noise 20 dB SNR | R2 | single | loses D5- detections: kept 6/12 (0.5) (no interval: fewer than 5 recordings) |
| train | MP3 64 kbit/s | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 recordings) |
| train | dynamic-range compression | R1 |  | adds D1+ regions: 0.597/min [0.401, 0.804] against the per-key share 0.0556/min |
| train | dynamic-range compression | R1 |  | adds D2- regions: 0.857/min [0.577, 1.15] against the per-key share 0.0556/min |
| train | dynamic-range compression | R1 |  | adds D5- regions: 0.857/min [0.702, 1.04] against the per-key share 0.0556/min |
| train | dynamic-range compression | R1 |  | adds D9- regions: 0.306/min [0.172, 0.464] against the per-key share 0.0556/min |
| train | dynamic-range compression | R1 |  | loses D4- detections: kept 5/11 (0.455) [0.2, 0.727] |
| train | dynamic-range compression | R1 |  | loses D5- detections: kept 13/45 (0.289) [0.163, 0.444] |
| train | dynamic-range compression | R2 | single | loses D5- detections: kept 0/4 (0) (no interval: fewer than 5 recordings) |
| train | room reverb RT60 0.4 s | R1 |  | adds D1+ regions: 0.362/min [0.223, 0.524] against the per-key share 0.0556/min |
| train | room reverb RT60 0.4 s | R1 |  | adds D5- regions: 0.214/min [0.113, 0.339] against the per-key share 0.0556/min |
| train | room reverb RT60 0.4 s | R1 |  | adds D9- regions: 0.173/min [0.101, 0.253] against the per-key share 0.0556/min |
| train | room reverb RT60 0.4 s | R2 | single | loses D2+ detections: kept 3/12 (0.25) (no interval: fewer than 5 recordings) |
| train | phone band + mu-law (participant only) | R1 |  | adds D1- regions: 0.903/min [0.709, 1.12] against the per-key share 0.0556/min |
| train | phone band + mu-law (participant only) | R1 |  | adds D2+ regions: 0.214/min [0.12, 0.323] against the per-key share 0.0556/min |
| train | phone band + mu-law (participant only) | R1 |  | adds D5- regions: 0.199/min [0.104, 0.324] against the per-key share 0.0556/min |
| train | phone band + mu-law (participant only) | R1 |  | adds D9- regions: 0.428/min [0.247, 0.634] against the per-key share 0.0556/min |
| train | phone band + mu-law (participant only) | R1 |  | loses D5- detections: kept 38/45 (0.844) [0.744, 0.935] |
| train | phone band + mu-law (participant only) | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 recordings) |
| train | phone band + mu-law (participant only) | R2 | single | loses D5- detections: kept 2/4 (0.5) (no interval: fewer than 5 recordings) |
| train | WORLD speaker transform | R1 |  | adds D1+ regions: 0.168/min [0.078, 0.272] against the per-key share 0.0556/min |
| train | WORLD speaker transform | R1 |  | adds D5- regions: 0.153/min [0.076, 0.244] against the per-key share 0.0556/min |
| train | WORLD speaker transform | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 recordings) |
| train | WORLD speaker transform | R2 | single | loses D2+ detections: kept 2/4 (0.5) (no interval: fewer than 5 recordings) |
| train | babble 10 dB SNR | R1 |  | adds D1+ regions: 8.94/min [8.27, 9.63] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | adds D1- regions: 3.76/min [3.04, 4.47] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | adds D2- regions: 11.9/min [11.2, 12.6] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | adds D3- regions: 0.24/min [0.09, 0.449] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | adds D4- regions: 0.99/min [0.691, 1.34] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | adds D5- regions: 2.59/min [2.21, 2.93] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | adds D9- regions: 1.61/min [1.31, 1.9] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | loses D1- detections: kept 67/81 (0.827) [0.716, 0.926] |
| train | babble 10 dB SNR | R1 |  | loses D2+ detections: kept 9/105 (0.0857) [0.027, 0.171] |
| train | babble 10 dB SNR | R1 |  | loses D3- detections: kept 11/36 (0.306) [0.139, 0.472] |
| train | babble 10 dB SNR | R1 |  | loses D4- detections: kept 22/33 (0.667) [0.5, 0.867] |
| train | babble 10 dB SNR | R1 |  | loses D5- detections: kept 74/135 (0.548) [0.435, 0.667] |
| train | babble 10 dB SNR | R1 |  | loses D6- detections: kept 9/30 (0.3) [0.133, 0.533] |
| train | babble 10 dB SNR | R1 |  | loses D9- detections: kept 6/9 (0.667) (no interval: fewer than 5 recordings) |
| train | babble 10 dB SNR | R2 | single | adds D1+ regions: 0.365/min [0.195, 0.543] against the per-key share 0.0833/min |
| train | babble 10 dB SNR | R2 | single | adds D5- regions: 0.477/min [0.304, 0.651] against the per-key share 0.0833/min |
| train | babble 10 dB SNR | R2 | single | loses D2+ detections: kept 0/12 (0) (no interval: fewer than 5 recordings) |
| train | babble 10 dB SNR | R2 | single | loses D5- detections: kept 1/12 (0.0833) (no interval: fewer than 5 recordings) |
| train | babble 20 dB SNR | R1 |  | adds D1+ regions: 4.38/min [3.84, 4.9] against the per-key share 0.0556/min |
| train | babble 20 dB SNR | R1 |  | adds D1- regions: 0.408/min [0.211, 0.659] against the per-key share 0.0556/min |
| train | babble 20 dB SNR | R1 |  | adds D2+ regions: 0.265/min [0.168, 0.373] against the per-key share 0.0556/min |
| train | babble 20 dB SNR | R1 |  | adds D2- regions: 5.71/min [4.85, 6.58] against the per-key share 0.0556/min |
| train | babble 20 dB SNR | R1 |  | adds D5- regions: 2.18/min [1.78, 2.56] against the per-key share 0.0556/min |
| train | babble 20 dB SNR | R1 |  | adds D9- regions: 0.536/min [0.372, 0.701] against the per-key share 0.0556/min |
| train | babble 20 dB SNR | R1 |  | loses D2+ detections: kept 75/105 (0.714) [0.616, 0.806] |
| train | babble 20 dB SNR | R1 |  | loses D5- detections: kept 110/135 (0.815) [0.723, 0.906] |
| train | babble 20 dB SNR | R2 | single | loses D2+ detections: kept 1/12 (0.0833) (no interval: fewer than 5 recordings) |
| train | babble 20 dB SNR | R2 | single | loses D5- detections: kept 4/12 (0.333) (no interval: fewer than 5 recordings) |
| val | gain +6 dB | R1 |  | adds D1+ regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | gain -6 dB | R1 |  | adds D1+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | gain -6 dB | R1 |  | adds D9- regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | low-pass 3.4 kHz | R1 |  | adds D1- regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | low-pass 3.4 kHz | R1 |  | adds D2+ regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | low-pass 3.4 kHz | R1 |  | adds D9- regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | low-pass 3.4 kHz | R1 |  | loses D6- detections: kept 1/4 (0.25) (no interval: fewer than 5 speakers) |
| val | white noise 20 dB SNR | R1 |  | adds D1+ regions: 0.15/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | white noise 20 dB SNR | R1 |  | adds D1- regions: 0.462/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | white noise 20 dB SNR | R1 |  | adds D2+ regions: 0.589/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | white noise 20 dB SNR | R1 |  | adds D4- regions: 0.0924/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | white noise 20 dB SNR | R1 |  | adds D5- regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | white noise 20 dB SNR | R1 |  | adds D9- regions: 1.2/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | white noise 20 dB SNR | R1 |  | loses D5- detections: kept 26/33 (0.788) (no interval: fewer than 5 speakers) |
| val | white noise 20 dB SNR | R1 |  | loses D6- detections: kept 1/12 (0.0833) (no interval: fewer than 5 speakers) |
| val | white noise 20 dB SNR | R1 |  | loses D9- detections: kept 8/9 (0.889) (no interval: fewer than 5 speakers) |
| val | MP3 64 kbit/s | R1 |  | adds D1+ regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | adds D1+ regions: 1.49/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | adds D1- regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | adds D2- regions: 1.98/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | adds D4- regions: 0.346/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | adds D5- regions: 2.22/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | adds D9- regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | loses D1- detections: kept 7/9 (0.778) (no interval: fewer than 5 speakers) |
| val | dynamic-range compression | R1 |  | loses D2+ detections: kept 12/13 (0.923) (no interval: fewer than 5 speakers) |
| val | dynamic-range compression | R1 |  | loses D4- detections: kept 5/7 (0.714) (no interval: fewer than 5 speakers) |
| val | dynamic-range compression | R1 |  | loses D5- detections: kept 2/11 (0.182) (no interval: fewer than 5 speakers) |
| val | dynamic-range compression | R1 |  | loses D6- detections: kept 3/4 (0.75) (no interval: fewer than 5 speakers) |
| val | dynamic-range compression | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 speakers) |
| val | room reverb RT60 0.4 s | R1 |  | adds D1+ regions: 0.335/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | room reverb RT60 0.4 s | R1 |  | adds D2+ regions: 0.0578/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | room reverb RT60 0.4 s | R1 |  | adds D3- regions: 0.0924/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | room reverb RT60 0.4 s | R1 |  | adds D4- regions: 0.15/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | room reverb RT60 0.4 s | R1 |  | adds D9- regions: 0.15/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | room reverb RT60 0.4 s | R1 |  | loses D1- detections: kept 25/27 (0.926) (no interval: fewer than 5 speakers) |
| val | room reverb RT60 0.4 s | R1 |  | loses D2+ detections: kept 36/39 (0.923) (no interval: fewer than 5 speakers) |
| val | room reverb RT60 0.4 s | R1 |  | loses D6- detections: kept 9/12 (0.75) (no interval: fewer than 5 speakers) |
| val | room reverb RT60 0.4 s | R1 |  | loses D9- detections: kept 7/9 (0.778) (no interval: fewer than 5 speakers) |
| val | phone band + mu-law (participant only) | R1 |  | adds D1+ regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | adds D2+ regions: 0.208/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | adds D2- regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | adds D3- regions: 0.589/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | adds D4- regions: 0.243/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | adds D5- regions: 0.243/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | adds D9- regions: 0.243/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | loses D2+ detections: kept 12/13 (0.923) (no interval: fewer than 5 speakers) |
| val | phone band + mu-law (participant only) | R1 |  | loses D5- detections: kept 6/11 (0.545) (no interval: fewer than 5 speakers) |
| val | phone band + mu-law (participant only) | R1 |  | loses D6- detections: kept 2/4 (0.5) (no interval: fewer than 5 speakers) |
| val | WORLD speaker transform | R1 |  | adds D1+ regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | WORLD speaker transform | R1 |  | adds D2+ regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | WORLD speaker transform | R1 |  | adds D4- regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | WORLD speaker transform | R1 |  | adds D9- regions: 0.589/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | WORLD speaker transform | R1 |  | loses D2+ detections: kept 12/13 (0.923) (no interval: fewer than 5 speakers) |
| val | WORLD speaker transform | R1 |  | loses D6- detections: kept 3/4 (0.75) (no interval: fewer than 5 speakers) |
| val | WORLD speaker transform | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | adds D1+ regions: 7.42/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D1- regions: 3.29/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D2+ regions: 0.0809/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D2- regions: 9.73/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D3- regions: 0.266/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D4- regions: 0.543/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D5- regions: 1.21/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D9- regions: 1.41/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | loses D1+ detections: kept 9/12 (0.75) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | loses D1- detections: kept 22/27 (0.815) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | loses D2+ detections: kept 5/39 (0.128) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | loses D3- detections: kept 11/15 (0.733) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | loses D5- detections: kept 16/33 (0.485) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | loses D6- detections: kept 1/12 (0.0833) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | loses D9- detections: kept 8/9 (0.889) (no interval: fewer than 5 speakers) |
| val | babble 20 dB SNR | R1 |  | adds D1+ regions: 2.56/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | adds D1- regions: 0.254/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | adds D2+ regions: 0.543/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | adds D2- regions: 3.4/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | adds D4- regions: 0.127/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | adds D5- regions: 0.878/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | adds D9- regions: 0.578/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | loses D1- detections: kept 24/27 (0.889) (no interval: fewer than 5 speakers) |
| val | babble 20 dB SNR | R1 |  | loses D2+ detections: kept 36/39 (0.923) (no interval: fewer than 5 speakers) |
| val | babble 20 dB SNR | R1 |  | loses D5- detections: kept 23/33 (0.697) (no interval: fewer than 5 speakers) |
| val | babble 20 dB SNR | R1 |  | loses D6- detections: kept 4/12 (0.333) (no interval: fewer than 5 speakers) |
| val | babble 20 dB SNR | R1 |  | loses D9- detections: kept 8/9 (0.889) (no interval: fewer than 5 speakers) |
| test | gain -6 dB | R1 |  | adds D1- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | gain -6 dB | R1 |  | adds D2+ regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | gain -6 dB | R1 |  | adds D2- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | gain -6 dB | R1 |  | adds D9- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | low-pass 3.4 kHz | R1 |  | adds D1+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | low-pass 3.4 kHz | R1 |  | adds D1- regions: 0.833/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | low-pass 3.4 kHz | R1 |  | adds D2+ regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | low-pass 3.4 kHz | R1 |  | adds D2- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | low-pass 3.4 kHz | R1 |  | adds D9- regions: 0.208/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | low-pass 3.4 kHz | R1 |  | loses D2- detections: kept 18/19 (0.947) (no interval: fewer than 5 speakers) |
| test | low-pass 3.4 kHz | R1 |  | loses D4- detections: kept 5/6 (0.833) (no interval: fewer than 5 speakers) |
| test | low-pass 3.4 kHz | R1 |  | loses D5- detections: kept 17/19 (0.895) (no interval: fewer than 5 speakers) |
| test | low-pass 3.4 kHz | R1 |  | loses D6- detections: kept 3/4 (0.75) (no interval: fewer than 5 speakers) |
| test | white noise 20 dB SNR | R1 |  | adds D1+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | white noise 20 dB SNR | R1 |  | adds D1- regions: 0.497/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | white noise 20 dB SNR | R1 |  | adds D2+ regions: 0.625/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | white noise 20 dB SNR | R1 |  | adds D2- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | white noise 20 dB SNR | R1 |  | adds D9- regions: 0.474/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | white noise 20 dB SNR | R1 |  | loses D2- detections: kept 54/57 (0.947) (no interval: fewer than 5 speakers) |
| test | white noise 20 dB SNR | R1 |  | loses D5- detections: kept 48/57 (0.842) (no interval: fewer than 5 speakers) |
| test | white noise 20 dB SNR | R1 |  | loses D6- detections: kept 3/12 (0.25) (no interval: fewer than 5 speakers) |
| test | dynamic-range compression | R1 |  | adds D1+ regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | dynamic-range compression | R1 |  | adds D2- regions: 1.18/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | dynamic-range compression | R1 |  | adds D4- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | dynamic-range compression | R1 |  | adds D5- regions: 1.01/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | dynamic-range compression | R1 |  | adds D9- regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | dynamic-range compression | R1 |  | loses D4- detections: kept 2/6 (0.333) (no interval: fewer than 5 speakers) |
| test | dynamic-range compression | R1 |  | loses D5- detections: kept 4/19 (0.21) (no interval: fewer than 5 speakers) |
| test | room reverb RT60 0.4 s | R1 |  | adds D1+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | room reverb RT60 0.4 s | R1 |  | adds D1- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | room reverb RT60 0.4 s | R1 |  | adds D3- regions: 0.081/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | room reverb RT60 0.4 s | R1 |  | adds D5- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | room reverb RT60 0.4 s | R1 |  | adds D9- regions: 0.127/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | room reverb RT60 0.4 s | R1 |  | loses D3- detections: kept 5/6 (0.833) (no interval: fewer than 5 speakers) |
| test | room reverb RT60 0.4 s | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 speakers) |
| test | phone band + mu-law (participant only) | R1 |  | adds D1+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | adds D1- regions: 1.04/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | adds D2+ regions: 0.278/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | adds D3- regions: 2.84/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | adds D4- regions: 0.659/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | adds D5- regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | adds D9- regions: 0.312/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | loses D1- detections: kept 9/10 (0.9) (no interval: fewer than 5 speakers) |
| test | phone band + mu-law (participant only) | R1 |  | loses D2- detections: kept 18/19 (0.947) (no interval: fewer than 5 speakers) |
| test | phone band + mu-law (participant only) | R1 |  | loses D3- detections: kept 0/2 (0) (no interval: fewer than 5 speakers) |
| test | phone band + mu-law (participant only) | R1 |  | loses D4- detections: kept 5/6 (0.833) (no interval: fewer than 5 speakers) |
| test | phone band + mu-law (participant only) | R1 |  | loses D5- detections: kept 15/19 (0.789) (no interval: fewer than 5 speakers) |
| test | phone band + mu-law (participant only) | R1 |  | loses D6- detections: kept 3/4 (0.75) (no interval: fewer than 5 speakers) |
| test | WORLD speaker transform | R1 |  | adds D1+ regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | WORLD speaker transform | R1 |  | adds D1- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | WORLD speaker transform | R1 |  | adds D2+ regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | WORLD speaker transform | R1 |  | adds D2- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | WORLD speaker transform | R1 |  | adds D3- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | WORLD speaker transform | R1 |  | adds D9- regions: 0.208/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | WORLD speaker transform | R1 |  | loses D4- detections: kept 5/6 (0.833) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | adds D1+ regions: 7.17/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D1- regions: 3.1/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D2+ regions: 0.15/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D2- regions: 11.5/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D3- regions: 0.416/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D4- regions: 0.243/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D5- regions: 1.61/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D9- regions: 1.43/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | loses D1+ detections: kept 6/12 (0.5) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | loses D1- detections: kept 21/30 (0.7) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | loses D2+ detections: kept 4/39 (0.103) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | loses D3- detections: kept 4/6 (0.667) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | loses D4- detections: kept 13/18 (0.722) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | loses D5- detections: kept 30/57 (0.526) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | loses D6- detections: kept 3/12 (0.25) (no interval: fewer than 5 speakers) |
| test | babble 20 dB SNR | R1 |  | adds D1+ regions: 3.34/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | adds D1- regions: 0.37/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | adds D2+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | adds D2- regions: 6.53/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | adds D4- regions: 0.081/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | adds D5- regions: 2.36/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | adds D9- regions: 0.335/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | loses D1+ detections: kept 11/12 (0.917) (no interval: fewer than 5 speakers) |
| test | babble 20 dB SNR | R1 |  | loses D1- detections: kept 24/30 (0.8) (no interval: fewer than 5 speakers) |
| test | babble 20 dB SNR | R1 |  | loses D2+ detections: kept 24/39 (0.615) (no interval: fewer than 5 speakers) |
| test | babble 20 dB SNR | R1 |  | loses D4- detections: kept 17/18 (0.944) (no interval: fewer than 5 speakers) |
| test | babble 20 dB SNR | R1 |  | loses D5- detections: kept 49/57 (0.86) (no interval: fewer than 5 speakers) |
| test | babble 20 dB SNR | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 speakers) |
| val+test | gain -6 dB | R1 |  | adds D1+ regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | gain -6 dB | R1 |  | adds D9- regions: 0.0867/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | low-pass 3.4 kHz | R1 |  | adds D1+ regions: 0.0867/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | low-pass 3.4 kHz | R1 |  | adds D1- regions: 0.468/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | low-pass 3.4 kHz | R1 |  | adds D2+ regions: 0.121/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | low-pass 3.4 kHz | R1 |  | adds D9- regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | low-pass 3.4 kHz | R1 |  | loses D4- detections: kept 12/13 (0.923) (no interval: fewer than 5 speakers) |
| val+test | low-pass 3.4 kHz | R1 |  | loses D5- detections: kept 28/30 (0.933) (no interval: fewer than 5 speakers) |
| val+test | low-pass 3.4 kHz | R1 |  | loses D6- detections: kept 4/8 (0.5) (no interval: fewer than 5 speakers) |
| val+test | white noise 20 dB SNR | R1 |  | adds D1+ regions: 0.144/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | white noise 20 dB SNR | R1 |  | adds D1- regions: 0.48/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | white noise 20 dB SNR | R1 |  | adds D2+ regions: 0.607/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | white noise 20 dB SNR | R1 |  | adds D2- regions: 0.0578/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | white noise 20 dB SNR | R1 |  | adds D4- regions: 0.0636/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | white noise 20 dB SNR | R1 |  | adds D9- regions: 0.838/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | white noise 20 dB SNR | R1 |  | loses D5- detections: kept 74/90 (0.822) (no interval: fewer than 5 speakers) |
| val+test | white noise 20 dB SNR | R1 |  | loses D6- detections: kept 4/24 (0.167) (no interval: fewer than 5 speakers) |
| val+test | white noise 20 dB SNR | R1 |  | loses D9- detections: kept 11/12 (0.917) (no interval: fewer than 5 speakers) |
| val+test | dynamic-range compression | R1 |  | adds D1+ regions: 0.832/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | dynamic-range compression | R1 |  | adds D1- regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | dynamic-range compression | R1 |  | adds D2- regions: 1.58/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | dynamic-range compression | R1 |  | adds D4- regions: 0.208/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | dynamic-range compression | R1 |  | adds D5- regions: 1.61/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | dynamic-range compression | R1 |  | adds D9- regions: 0.121/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | dynamic-range compression | R1 |  | loses D1- detections: kept 17/19 (0.895) (no interval: fewer than 5 speakers) |
| val+test | dynamic-range compression | R1 |  | loses D4- detections: kept 7/13 (0.538) (no interval: fewer than 5 speakers) |
| val+test | dynamic-range compression | R1 |  | loses D5- detections: kept 6/30 (0.2) (no interval: fewer than 5 speakers) |
| val+test | dynamic-range compression | R1 |  | loses D6- detections: kept 7/8 (0.875) (no interval: fewer than 5 speakers) |
| val+test | dynamic-range compression | R1 |  | loses D9- detections: kept 3/4 (0.75) (no interval: fewer than 5 speakers) |
| val+test | room reverb RT60 0.4 s | R1 |  | adds D1+ regions: 0.237/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | room reverb RT60 0.4 s | R1 |  | adds D3- regions: 0.0867/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | room reverb RT60 0.4 s | R1 |  | adds D4- regions: 0.0982/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | room reverb RT60 0.4 s | R1 |  | adds D9- regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | room reverb RT60 0.4 s | R1 |  | loses D1- detections: kept 54/57 (0.947) (no interval: fewer than 5 speakers) |
| val+test | room reverb RT60 0.4 s | R1 |  | loses D6- detections: kept 21/24 (0.875) (no interval: fewer than 5 speakers) |
| val+test | room reverb RT60 0.4 s | R1 |  | loses D9- detections: kept 9/12 (0.75) (no interval: fewer than 5 speakers) |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D1+ regions: 0.156/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D1- regions: 0.537/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D2+ regions: 0.243/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D2- regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D3- regions: 1.72/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D4- regions: 0.451/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D5- regions: 0.208/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D9- regions: 0.277/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | loses D1- detections: kept 18/19 (0.947) (no interval: fewer than 5 speakers) |
| val+test | phone band + mu-law (participant only) | R1 |  | loses D3- detections: kept 5/7 (0.714) (no interval: fewer than 5 speakers) |
| val+test | phone band + mu-law (participant only) | R1 |  | loses D4- detections: kept 12/13 (0.923) (no interval: fewer than 5 speakers) |
| val+test | phone band + mu-law (participant only) | R1 |  | loses D5- detections: kept 21/30 (0.7) (no interval: fewer than 5 speakers) |
| val+test | phone band + mu-law (participant only) | R1 |  | loses D6- detections: kept 5/8 (0.625) (no interval: fewer than 5 speakers) |
| val+test | WORLD speaker transform | R1 |  | adds D1+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | WORLD speaker transform | R1 |  | adds D2+ regions: 0.0867/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | WORLD speaker transform | R1 |  | adds D9- regions: 0.399/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | WORLD speaker transform | R1 |  | loses D4- detections: kept 12/13 (0.923) (no interval: fewer than 5 speakers) |
| val+test | WORLD speaker transform | R1 |  | loses D6- detections: kept 7/8 (0.875) (no interval: fewer than 5 speakers) |
| val+test | WORLD speaker transform | R1 |  | loses D9- detections: kept 3/4 (0.75) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | adds D1+ regions: 7.29/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D1- regions: 3.2/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D2+ regions: 0.116/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D2- regions: 10.6/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D3- regions: 0.341/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D4- regions: 0.393/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D5- regions: 1.41/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D9- regions: 1.42/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | loses D1+ detections: kept 15/24 (0.625) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D1- detections: kept 43/57 (0.754) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D2+ detections: kept 9/78 (0.115) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D3- detections: kept 15/21 (0.714) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D4- detections: kept 33/39 (0.846) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D5- detections: kept 46/90 (0.511) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D6- detections: kept 4/24 (0.167) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D9- detections: kept 11/12 (0.917) (no interval: fewer than 5 speakers) |
| val+test | babble 20 dB SNR | R1 |  | adds D1+ regions: 2.95/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | adds D1- regions: 0.312/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | adds D2+ regions: 0.341/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | adds D2- regions: 4.96/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | adds D4- regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | adds D5- regions: 1.62/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | adds D9- regions: 0.457/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | loses D1- detections: kept 48/57 (0.842) (no interval: fewer than 5 speakers) |
| val+test | babble 20 dB SNR | R1 |  | loses D2+ detections: kept 60/78 (0.769) (no interval: fewer than 5 speakers) |
| val+test | babble 20 dB SNR | R1 |  | loses D5- detections: kept 72/90 (0.8) (no interval: fewer than 5 speakers) |
| val+test | babble 20 dB SNR | R1 |  | loses D6- detections: kept 16/24 (0.667) (no interval: fewer than 5 speakers) |
| val+test | babble 20 dB SNR | R1 |  | loses D9- detections: kept 10/12 (0.833) (no interval: fewer than 5 speakers) |
| check readers | white noise 20 dB SNR | R2 | single | adds D2+ regions: 0.258/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | phone band + mu-law (participant only) | R2 | single | adds D2+ regions: 0.258/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | phone band + mu-law (participant only) | R2 | single | adds D5- regions: 0.129/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 10 dB SNR | R2 | single | adds D1+ regions: 1.03/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 10 dB SNR | R2 | single | adds D1- regions: 0.0859/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 10 dB SNR | R2 | single | adds D2- regions: 0.902/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 10 dB SNR | R2 | consensus5 | adds D1+ regions: 1.29/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 10 dB SNR | R2 | consensus5 | adds D2- regions: 4.12/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 20 dB SNR | R2 | single | adds D2- regions: 0.0859/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 20 dB SNR | R2 | consensus5 | adds D2- regions: 1.8/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |

Added regions per key:

| split | condition | regime | reference mode | key | added (all seeds) | per min | interval |
|---|---|---|---|---|---|---|---|
| train | gain +6 dB | R1 |  | D1+ | 2 | 0.0306 | 95% [0, 0.076] |
| train | gain +6 dB | R1 |  | D2+ | 2 | 0.0306 | 95% [0, 0.077] |
| train | gain +6 dB | R1 |  | D3- | 1 | 0.0153 | 95% [0, 0.047] |
| train | gain +6 dB | R1 |  | D4- | 2 | 0.0306 | 95% [0, 0.078] |
| train | gain +6 dB | R1 |  | D9- | 6 | 0.0918 | 95% [0.03, 0.17] |
| train | gain -6 dB | R1 |  | D1- | 1 | 0.0153 | 95% [0, 0.047] |
| train | gain -6 dB | R1 |  | D4- | 2 | 0.0306 | 95% [0, 0.078] |
| train | gain -6 dB | R1 |  | D9- | 3 | 0.0459 | 95% [0, 0.108] |
| train | low-pass 3.4 kHz | R1 |  | D1+ | 6 | 0.0918 | 95% [0.016, 0.185] |
| train | low-pass 3.4 kHz | R1 |  | D1+ whole clip | 1 | 0.0153 | 95% [0, 0.046] |
| train | low-pass 3.4 kHz | R1 |  | D1- | 79 | 1.21 | 95% [0.96, 1.49] |
| train | low-pass 3.4 kHz | R1 |  | D2+ | 5 | 0.0765 | 95% [0.015, 0.151] |
| train | low-pass 3.4 kHz | R1 |  | D2- | 1 | 0.0153 | 95% [0, 0.047] |
| train | low-pass 3.4 kHz | R1 |  | D4- | 2 | 0.0306 | 95% [0, 0.078] |
| train | low-pass 3.4 kHz | R1 |  | D5- | 3 | 0.0459 | 95% [0, 0.108] |
| train | low-pass 3.4 kHz | R1 |  | D9- | 8 | 0.122 | 95% [0.031, 0.224] |
| train | white noise 20 dB SNR | R1 |  | D1+ | 35 | 0.178 | 95% [0.063, 0.336] |
| train | white noise 20 dB SNR | R1 |  | D1- | 149 | 0.76 | 95% [0.561, 0.998] |
| train | white noise 20 dB SNR | R1 |  | D2+ | 95 | 0.485 | 95% [0.226, 0.873] |
| train | white noise 20 dB SNR | R1 |  | D2- | 1 | 0.0051 | 95% [0, 0.016] |
| train | white noise 20 dB SNR | R1 |  | D3- | 2 | 0.0102 | 95% [0, 0.03] |
| train | white noise 20 dB SNR | R1 |  | D4- | 15 | 0.0765 | 95% [0.015, 0.142] |
| train | white noise 20 dB SNR | R1 |  | D5- | 3 | 0.0153 | 95% [0, 0.047] |
| train | white noise 20 dB SNR | R1 |  | D6- | 5 | 0.0255 | 95% [0, 0.062] |
| train | white noise 20 dB SNR | R1 |  | D9- | 164 | 0.837 | 95% [0.555, 1.12] |
| train | MP3 64 kbit/s | R1 |  | D1+ | 1 | 0.0153 | 95% [0, 0.046] |
| train | MP3 64 kbit/s | R1 |  | D5- | 1 | 0.0153 | 95% [0, 0.047] |
| train | MP3 64 kbit/s | R1 |  | D9- | 3 | 0.0459 | 95% [0, 0.108] |
| train | MP3 64 kbit/s | R2 | single | D5- | 1 | 0.0842 | 95% [0, 0.26] |
| train | dynamic-range compression | R1 |  | D1+ | 39 | 0.597 | 95% [0.401, 0.804] |
| train | dynamic-range compression | R1 |  | D1+ whole clip | 2 | 0.0306 | 95% [0, 0.077] |
| train | dynamic-range compression | R1 |  | D1- | 6 | 0.0918 | 95% [0, 0.238] |
| train | dynamic-range compression | R1 |  | D2+ | 3 | 0.0459 | 95% [0, 0.105] |
| train | dynamic-range compression | R1 |  | D2- | 56 | 0.857 | 95% [0.577, 1.15] |
| train | dynamic-range compression | R1 |  | D3- | 5 | 0.0765 | 95% [0.015, 0.149] |
| train | dynamic-range compression | R1 |  | D4- | 5 | 0.0765 | 95% [0.015, 0.17] |
| train | dynamic-range compression | R1 |  | D5- | 56 | 0.857 | 95% [0.702, 1.04] |
| train | dynamic-range compression | R1 |  | D9- | 20 | 0.306 | 95% [0.172, 0.464] |
| train | room reverb RT60 0.4 s | R1 |  | D1+ | 71 | 0.362 | 95% [0.223, 0.524] |
| train | room reverb RT60 0.4 s | R1 |  | D1+ whole clip | 3 | 0.0153 | 95% [0, 0.046] |
| train | room reverb RT60 0.4 s | R1 |  | D1- | 19 | 0.0969 | 95% [0.03, 0.192] |
| train | room reverb RT60 0.4 s | R1 |  | D2+ | 2 | 0.0102 | 95% [0, 0.026] |
| train | room reverb RT60 0.4 s | R1 |  | D2- | 3 | 0.0153 | 95% [0, 0.047] |
| train | room reverb RT60 0.4 s | R1 |  | D3- | 7 | 0.0357 | 95% [0.005, 0.076] |
| train | room reverb RT60 0.4 s | R1 |  | D4- | 8 | 0.0408 | 95% [0.01, 0.077] |
| train | room reverb RT60 0.4 s | R1 |  | D5- | 42 | 0.214 | 95% [0.113, 0.339] |
| train | room reverb RT60 0.4 s | R1 |  | D9- | 34 | 0.173 | 95% [0.101, 0.253] |
| train | room reverb RT60 0.4 s | R2 | single | D5- | 13 | 0.365 | 95% [0.056, 0.754] |
| train | phone band + mu-law (participant only) | R1 |  | D1+ | 8 | 0.122 | 95% [0.016, 0.249] |
| train | phone band + mu-law (participant only) | R1 |  | D1+ whole clip | 1 | 0.0153 | 95% [0, 0.046] |
| train | phone band + mu-law (participant only) | R1 |  | D1- | 59 | 0.903 | 95% [0.709, 1.12] |
| train | phone band + mu-law (participant only) | R1 |  | D2+ | 14 | 0.214 | 95% [0.12, 0.323] |
| train | phone band + mu-law (participant only) | R1 |  | D2- | 3 | 0.0459 | 95% [0, 0.106] |
| train | phone band + mu-law (participant only) | R1 |  | D3- | 1 | 0.0153 | 95% [0, 0.047] |
| train | phone band + mu-law (participant only) | R1 |  | D4- | 3 | 0.0459 | 95% [0, 0.106] |
| train | phone band + mu-law (participant only) | R1 |  | D5- | 13 | 0.199 | 95% [0.104, 0.324] |
| train | phone band + mu-law (participant only) | R1 |  | D9- | 28 | 0.428 | 95% [0.247, 0.634] |
| train | phone band + mu-law (participant only) | R2 | single | D5- | 1 | 0.0842 | 95% [0, 0.26] |
| train | WORLD speaker transform | R1 |  | D1+ | 11 | 0.168 | 95% [0.078, 0.272] |
| train | WORLD speaker transform | R1 |  | D1- | 2 | 0.0306 | 95% [0, 0.077] |
| train | WORLD speaker transform | R1 |  | D2+ | 2 | 0.0306 | 95% [0, 0.077] |
| train | WORLD speaker transform | R1 |  | D2- | 1 | 0.0153 | 95% [0, 0.047] |
| train | WORLD speaker transform | R1 |  | D3- | 1 | 0.0153 | 95% [0, 0.047] |
| train | WORLD speaker transform | R1 |  | D4- | 3 | 0.0459 | 95% [0, 0.105] |
| train | WORLD speaker transform | R1 |  | D5- | 10 | 0.153 | 95% [0.076, 0.244] |
| train | WORLD speaker transform | R1 |  | D9- | 4 | 0.0612 | 95% [0.015, 0.123] |
| train | babble 10 dB SNR | R1 |  | D1+ | 1753 | 8.94 | 95% [8.27, 9.63] |
| train | babble 10 dB SNR | R1 |  | D1+ whole clip | 55 | 0.281 | 95% [0.186, 0.38] |
| train | babble 10 dB SNR | R1 |  | D1- | 737 | 3.76 | 95% [3.04, 4.47] |
| train | babble 10 dB SNR | R1 |  | D2+ | 11 | 0.0561 | 95% [0.021, 0.097] |
| train | babble 10 dB SNR | R1 |  | D2- | 2333 | 11.9 | 95% [11.2, 12.6] |
| train | babble 10 dB SNR | R1 |  | D3- | 47 | 0.24 | 95% [0.09, 0.449] |
| train | babble 10 dB SNR | R1 |  | D4- | 194 | 0.99 | 95% [0.691, 1.34] |
| train | babble 10 dB SNR | R1 |  | D5- | 507 | 2.59 | 95% [2.21, 2.93] |
| train | babble 10 dB SNR | R1 |  | D9- | 316 | 1.61 | 95% [1.31, 1.9] |
| train | babble 10 dB SNR | R2 | single | D1+ | 13 | 0.365 | 95% [0.195, 0.543] |
| train | babble 10 dB SNR | R2 | single | D3- | 5 | 0.14 | 95% [0, 0.448] |
| train | babble 10 dB SNR | R2 | single | D5- | 17 | 0.477 | 95% [0.304, 0.651] |
| train | babble 20 dB SNR | R1 |  | D1+ | 859 | 4.38 | 95% [3.84, 4.9] |
| train | babble 20 dB SNR | R1 |  | D1+ whole clip | 8 | 0.0408 | 95% [0, 0.096] |
| train | babble 20 dB SNR | R1 |  | D1- | 80 | 0.408 | 95% [0.211, 0.659] |
| train | babble 20 dB SNR | R1 |  | D2+ | 52 | 0.265 | 95% [0.168, 0.373] |
| train | babble 20 dB SNR | R1 |  | D2- | 1119 | 5.71 | 95% [4.85, 6.58] |
| train | babble 20 dB SNR | R1 |  | D3- | 6 | 0.0306 | 95% [0.005, 0.071] |
| train | babble 20 dB SNR | R1 |  | D4- | 19 | 0.0969 | 95% [0.036, 0.181] |
| train | babble 20 dB SNR | R1 |  | D5- | 427 | 2.18 | 95% [1.78, 2.56] |
| train | babble 20 dB SNR | R1 |  | D9- | 105 | 0.536 | 95% [0.372, 0.701] |
| train | babble 20 dB SNR | R2 | single | D1+ | 1 | 0.0281 | 95% [0, 0.086] |
| train | babble 20 dB SNR | R2 | single | D5- | 3 | 0.0842 | 95% [0, 0.224] |
| val | gain +6 dB | R1 |  | D1+ | 2 | 0.0693 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0; range [0, 0.138] |
| val | gain +6 dB | R1 |  | D2+ | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | gain +6 dB | R1 |  | D2- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | gain +6 dB | R1 |  | D4- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | gain +6 dB | R1 |  | D9- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069; range [0, 0.069] |
| val | gain -6 dB | R1 |  | D1+ | 4 | 0.139 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0.069; range [0.069, 0.208] |
| val | gain -6 dB | R1 |  | D2+ | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | gain -6 dB | R1 |  | D9- | 3 | 0.104 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069; range [0.069, 0.138] |
| val | low-pass 3.4 kHz | R1 |  | D1+ | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | low-pass 3.4 kHz | R1 |  | D1- | 3 | 0.104 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069; range [0.069, 0.138] |
| val | low-pass 3.4 kHz | R1 |  | D2+ | 2 | 0.0693 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0; range [0, 0.138] |
| val | low-pass 3.4 kHz | R1 |  | D5- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069; range [0, 0.069] |
| val | low-pass 3.4 kHz | R1 |  | D9- | 4 | 0.139 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.139; range [0.138, 0.139] |
| val | white noise 20 dB SNR | R1 |  | D1+ | 13 | 0.15 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.162; range [0.138, 0.162] |
| val | white noise 20 dB SNR | R1 |  | D1- | 40 | 0.462 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 0.324; range [0.324, 0.6] |
| val | white noise 20 dB SNR | R1 |  | D2+ | 51 | 0.589 | per speaker: eisenhower_farewell_1961 0.438, lbush_radio_2001 0.74; range [0.438, 0.74] |
| val | white noise 20 dB SNR | R1 |  | D2- | 4 | 0.0462 | per speaker: eisenhower_farewell_1961 0.092, lbush_radio_2001 0; range [0, 0.092] |
| val | white noise 20 dB SNR | R1 |  | D3- | 1 | 0.0116 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.023; range [0, 0.023] |
| val | white noise 20 dB SNR | R1 |  | D4- | 8 | 0.0924 | per speaker: eisenhower_farewell_1961 0.115, lbush_radio_2001 0.069; range [0.069, 0.115] |
| val | white noise 20 dB SNR | R1 |  | D5- | 6 | 0.0693 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.139; range [0, 0.139] |
| val | white noise 20 dB SNR | R1 |  | D6- | 1 | 0.0116 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0; range [0, 0.023] |
| val | white noise 20 dB SNR | R1 |  | D9- | 104 | 1.2 | per speaker: eisenhower_farewell_1961 0.553, lbush_radio_2001 1.85; range [0.553, 1.85] |
| val | MP3 64 kbit/s | R1 |  | D1+ | 2 | 0.0693 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0; range [0, 0.138] |
| val | dynamic-range compression | R1 |  | D1+ | 43 | 1.49 | per speaker: eisenhower_farewell_1961 2.84, lbush_radio_2001 0.139; range [0.139, 2.84] |
| val | dynamic-range compression | R1 |  | D1+ whole clip | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | dynamic-range compression | R1 |  | D1- | 5 | 0.173 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0; range [0, 0.346] |
| val | dynamic-range compression | R1 |  | D2+ | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | dynamic-range compression | R1 |  | D2- | 57 | 1.98 | per speaker: eisenhower_farewell_1961 3.94, lbush_radio_2001 0; range [0, 3.94] |
| val | dynamic-range compression | R1 |  | D3- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069; range [0, 0.069] |
| val | dynamic-range compression | R1 |  | D4- | 10 | 0.346 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.555; range [0.138, 0.555] |
| val | dynamic-range compression | R1 |  | D5- | 64 | 2.22 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 3.96; range [0.484, 3.96] |
| val | dynamic-range compression | R1 |  | D6- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069; range [0, 0.069] |
| val | dynamic-range compression | R1 |  | D9- | 4 | 0.139 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.139; range [0.138, 0.139] |
| val | room reverb RT60 0.4 s | R1 |  | D1+ | 29 | 0.335 | per speaker: eisenhower_farewell_1961 0.323, lbush_radio_2001 0.347; range [0.323, 0.347] |
| val | room reverb RT60 0.4 s | R1 |  | D1- | 2 | 0.0231 | per speaker: eisenhower_farewell_1961 0.046, lbush_radio_2001 0; range [0, 0.046] |
| val | room reverb RT60 0.4 s | R1 |  | D2+ | 5 | 0.0578 | per speaker: eisenhower_farewell_1961 0.092, lbush_radio_2001 0.023; range [0.023, 0.092] |
| val | room reverb RT60 0.4 s | R1 |  | D2- | 4 | 0.0462 | per speaker: eisenhower_farewell_1961 0.092, lbush_radio_2001 0; range [0, 0.092] |
| val | room reverb RT60 0.4 s | R1 |  | D3- | 8 | 0.0924 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0.162; range [0.023, 0.162] |
| val | room reverb RT60 0.4 s | R1 |  | D4- | 13 | 0.15 | per speaker: eisenhower_farewell_1961 0.277, lbush_radio_2001 0.023; range [0.023, 0.277] |
| val | room reverb RT60 0.4 s | R1 |  | D5- | 3 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069; range [0, 0.069] |
| val | room reverb RT60 0.4 s | R1 |  | D9- | 13 | 0.15 | per speaker: eisenhower_farewell_1961 0.115, lbush_radio_2001 0.185; range [0.115, 0.185] |
| val | phone band + mu-law (participant only) | R1 |  | D1+ | 5 | 0.173 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0; range [0, 0.346] |
| val | phone band + mu-law (participant only) | R1 |  | D1- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069; range [0, 0.069] |
| val | phone band + mu-law (participant only) | R1 |  | D2+ | 6 | 0.208 | per speaker: eisenhower_farewell_1961 0.415, lbush_radio_2001 0; range [0, 0.415] |
| val | phone band + mu-law (participant only) | R1 |  | D2- | 3 | 0.104 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0; range [0, 0.208] |
| val | phone band + mu-law (participant only) | R1 |  | D3- | 17 | 0.589 | per speaker: eisenhower_farewell_1961 1.11, lbush_radio_2001 0.069; range [0.069, 1.11] |
| val | phone band + mu-law (participant only) | R1 |  | D4- | 7 | 0.243 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.139; range [0.139, 0.346] |
| val | phone band + mu-law (participant only) | R1 |  | D5- | 7 | 0.243 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.139; range [0.139, 0.346] |
| val | phone band + mu-law (participant only) | R1 |  | D9- | 7 | 0.243 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.347; range [0.138, 0.347] |
| val | WORLD speaker transform | R1 |  | D1+ | 3 | 0.104 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069; range [0.069, 0.138] |
| val | WORLD speaker transform | R1 |  | D1- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | WORLD speaker transform | R1 |  | D2+ | 2 | 0.0693 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0; range [0, 0.138] |
| val | WORLD speaker transform | R1 |  | D2- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | WORLD speaker transform | R1 |  | D4- | 2 | 0.0693 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0.069; range [0.069, 0.069] |
| val | WORLD speaker transform | R1 |  | D5- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | WORLD speaker transform | R1 |  | D9- | 17 | 0.589 | per speaker: eisenhower_farewell_1961 0.899, lbush_radio_2001 0.278; range [0.278, 0.899] |
| val | babble 10 dB SNR | R1 |  | D1+ | 642 | 7.42 | per speaker: eisenhower_farewell_1961 6.66, lbush_radio_2001 8.17; range [6.66, 8.17] |
| val | babble 10 dB SNR | R1 |  | D1+ whole clip | 49 | 0.566 | per speaker: eisenhower_farewell_1961 0.992, lbush_radio_2001 0.139; range [0.139, 0.992] |
| val | babble 10 dB SNR | R1 |  | D1- | 285 | 3.29 | per speaker: eisenhower_farewell_1961 5.03, lbush_radio_2001 1.55; range [1.55, 5.03] |
| val | babble 10 dB SNR | R1 |  | D2+ | 7 | 0.0809 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0.139; range [0.023, 0.139] |
| val | babble 10 dB SNR | R1 |  | D2- | 842 | 9.73 | per speaker: eisenhower_farewell_1961 12, lbush_radio_2001 7.47; range [7.47, 12] |
| val | babble 10 dB SNR | R1 |  | D3- | 23 | 0.266 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0.324; range [0.208, 0.324] |
| val | babble 10 dB SNR | R1 |  | D4- | 47 | 0.543 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 0.486; range [0.486, 0.6] |
| val | babble 10 dB SNR | R1 |  | D5- | 105 | 1.21 | per speaker: eisenhower_farewell_1961 1.25, lbush_radio_2001 1.18; range [1.18, 1.25] |
| val | babble 10 dB SNR | R1 |  | D9- | 122 | 1.41 | per speaker: eisenhower_farewell_1961 0.438, lbush_radio_2001 2.38; range [0.438, 2.38] |
| val | babble 20 dB SNR | R1 |  | D1+ | 222 | 2.56 | per speaker: eisenhower_farewell_1961 3.27, lbush_radio_2001 1.85; range [1.85, 3.27] |
| val | babble 20 dB SNR | R1 |  | D1+ whole clip | 3 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | babble 20 dB SNR | R1 |  | D1- | 22 | 0.254 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 0.023; range [0.023, 0.484] |
| val | babble 20 dB SNR | R1 |  | D2+ | 47 | 0.543 | per speaker: eisenhower_farewell_1961 0.507, lbush_radio_2001 0.579; range [0.507, 0.579] |
| val | babble 20 dB SNR | R1 |  | D2- | 294 | 3.4 | per speaker: eisenhower_farewell_1961 4.87, lbush_radio_2001 1.92; range [1.92, 4.87] |
| val | babble 20 dB SNR | R1 |  | D3- | 2 | 0.0231 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0.023; range [0.023, 0.023] |
| val | babble 20 dB SNR | R1 |  | D4- | 11 | 0.127 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.116; range [0.116, 0.138] |
| val | babble 20 dB SNR | R1 |  | D5- | 76 | 0.878 | per speaker: eisenhower_farewell_1961 1.04, lbush_radio_2001 0.717; range [0.717, 1.04] |
| val | babble 20 dB SNR | R1 |  | D6- | 1 | 0.0116 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0; range [0, 0.023] |
| val | babble 20 dB SNR | R1 |  | D9- | 50 | 0.578 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0.949; range [0.208, 0.949] |
| test | gain +6 dB | R1 |  | D1+ | 1 | 0.0347 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.069] |
| test | gain +6 dB | R1 |  | D1- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | gain +6 dB | R1 |  | D2- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.069] |
| test | gain +6 dB | R1 |  | D9- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | gain -6 dB | R1 |  | D1- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| test | gain -6 dB | R1 |  | D2+ | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | gain -6 dB | R1 |  | D2- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | gain -6 dB | R1 |  | D9- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| test | low-pass 3.4 kHz | R1 |  | D1+ | 4 | 0.139 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.138, 0.139] |
| test | low-pass 3.4 kHz | R1 |  | D1- | 24 | 0.833 | per speaker: mobama_weekly_2014 1.6, nixon_resignation_1974 0.069; range [0.069, 1.6] |
| test | low-pass 3.4 kHz | R1 |  | D2+ | 5 | 0.173 | per speaker: mobama_weekly_2014 0.279, nixon_resignation_1974 0.069; range [0.069, 0.279] |
| test | low-pass 3.4 kHz | R1 |  | D2- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | low-pass 3.4 kHz | R1 |  | D5- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | low-pass 3.4 kHz | R1 |  | D9- | 6 | 0.208 | per speaker: mobama_weekly_2014 0.279, nixon_resignation_1974 0.138; range [0.138, 0.279] |
| test | white noise 20 dB SNR | R1 |  | D1+ | 12 | 0.139 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.138, 0.139] |
| test | white noise 20 dB SNR | R1 |  | D1- | 43 | 0.497 | per speaker: mobama_weekly_2014 0.487, nixon_resignation_1974 0.507; range [0.487, 0.507] |
| test | white noise 20 dB SNR | R1 |  | D2+ | 54 | 0.625 | per speaker: mobama_weekly_2014 0.348, nixon_resignation_1974 0.899; range [0.348, 0.899] |
| test | white noise 20 dB SNR | R1 |  | D2- | 6 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | white noise 20 dB SNR | R1 |  | D4- | 3 | 0.0347 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.069] |
| test | white noise 20 dB SNR | R1 |  | D6- | 1 | 0.0116 | per speaker: mobama_weekly_2014 0.023, nixon_resignation_1974 0; range [0, 0.023] |
| test | white noise 20 dB SNR | R1 |  | D9- | 41 | 0.474 | per speaker: mobama_weekly_2014 0.325, nixon_resignation_1974 0.622; range [0.325, 0.622] |
| test | MP3 64 kbit/s | R1 |  | D1- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | MP3 64 kbit/s | R1 |  | D2+ | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | MP3 64 kbit/s | R1 |  | D2- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | MP3 64 kbit/s | R1 |  | D9- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | dynamic-range compression | R1 |  | D1+ | 5 | 0.173 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.277; range [0.07, 0.277] |
| test | dynamic-range compression | R1 |  | D1- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | dynamic-range compression | R1 |  | D2- | 34 | 1.18 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 2.35; range [0, 2.35] |
| test | dynamic-range compression | R1 |  | D3- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | dynamic-range compression | R1 |  | D4- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | dynamic-range compression | R1 |  | D5- | 29 | 1.01 | per speaker: mobama_weekly_2014 1.74, nixon_resignation_1974 0.277; range [0.277, 1.74] |
| test | dynamic-range compression | R1 |  | D9- | 3 | 0.104 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.069; range [0.069, 0.139] |
| test | room reverb RT60 0.4 s | R1 |  | D1+ | 12 | 0.139 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.207; range [0.07, 0.207] |
| test | room reverb RT60 0.4 s | R1 |  | D1- | 6 | 0.0694 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| test | room reverb RT60 0.4 s | R1 |  | D2+ | 4 | 0.0463 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.023; range [0.023, 0.07] |
| test | room reverb RT60 0.4 s | R1 |  | D2- | 3 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | room reverb RT60 0.4 s | R1 |  | D3- | 7 | 0.081 | per speaker: mobama_weekly_2014 0.116, nixon_resignation_1974 0.046; range [0.046, 0.116] |
| test | room reverb RT60 0.4 s | R1 |  | D4- | 4 | 0.0463 | per speaker: mobama_weekly_2014 0.023, nixon_resignation_1974 0.069; range [0.023, 0.069] |
| test | room reverb RT60 0.4 s | R1 |  | D5- | 6 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | room reverb RT60 0.4 s | R1 |  | D9- | 11 | 0.127 | per speaker: mobama_weekly_2014 0.186, nixon_resignation_1974 0.069; range [0.069, 0.186] |
| test | phone band + mu-law (participant only) | R1 |  | D1+ | 4 | 0.139 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.138, 0.139] |
| test | phone band + mu-law (participant only) | R1 |  | D1- | 30 | 1.04 | per speaker: mobama_weekly_2014 0.418, nixon_resignation_1974 1.66; range [0.418, 1.66] |
| test | phone band + mu-law (participant only) | R1 |  | D2+ | 8 | 0.278 | per speaker: mobama_weekly_2014 0.418, nixon_resignation_1974 0.138; range [0.138, 0.418] |
| test | phone band + mu-law (participant only) | R1 |  | D2- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | phone band + mu-law (participant only) | R1 |  | D3- | 82 | 2.84 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 5.53; range [0.139, 5.53] |
| test | phone band + mu-law (participant only) | R1 |  | D4- | 19 | 0.659 | per speaker: mobama_weekly_2014 0.279, nixon_resignation_1974 1.04; range [0.279, 1.04] |
| test | phone band + mu-law (participant only) | R1 |  | D5- | 5 | 0.173 | per speaker: mobama_weekly_2014 0.279, nixon_resignation_1974 0.069; range [0.069, 0.279] |
| test | phone band + mu-law (participant only) | R1 |  | D6- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | phone band + mu-law (participant only) | R1 |  | D9- | 9 | 0.312 | per speaker: mobama_weekly_2014 0.487, nixon_resignation_1974 0.138; range [0.138, 0.487] |
| test | WORLD speaker transform | R1 |  | D1+ | 5 | 0.173 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.207; range [0.139, 0.207] |
| test | WORLD speaker transform | R1 |  | D1- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | WORLD speaker transform | R1 |  | D2+ | 3 | 0.104 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.069; range [0.069, 0.139] |
| test | WORLD speaker transform | R1 |  | D2- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | WORLD speaker transform | R1 |  | D3- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| test | WORLD speaker transform | R1 |  | D4- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.069] |
| test | WORLD speaker transform | R1 |  | D5- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | WORLD speaker transform | R1 |  | D9- | 6 | 0.208 | per speaker: mobama_weekly_2014 0.209, nixon_resignation_1974 0.207; range [0.207, 0.209] |
| test | babble 10 dB SNR | R1 |  | D1+ | 620 | 7.17 | per speaker: mobama_weekly_2014 6.24, nixon_resignation_1974 8.09; range [6.24, 8.09] |
| test | babble 10 dB SNR | R1 |  | D1+ whole clip | 49 | 0.567 | per speaker: mobama_weekly_2014 0.116, nixon_resignation_1974 1.01; range [0.116, 1.01] |
| test | babble 10 dB SNR | R1 |  | D1- | 268 | 3.1 | per speaker: mobama_weekly_2014 0.998, nixon_resignation_1974 5.19; range [0.998, 5.19] |
| test | babble 10 dB SNR | R1 |  | D2+ | 13 | 0.15 | per speaker: mobama_weekly_2014 0.116, nixon_resignation_1974 0.184; range [0.116, 0.184] |
| test | babble 10 dB SNR | R1 |  | D2- | 993 | 11.5 | per speaker: mobama_weekly_2014 10.2, nixon_resignation_1974 12.7; range [10.2, 12.7] |
| test | babble 10 dB SNR | R1 |  | D3- | 36 | 0.416 | per speaker: mobama_weekly_2014 0.093, nixon_resignation_1974 0.738; range [0.093, 0.738] |
| test | babble 10 dB SNR | R1 |  | D4- | 21 | 0.243 | per speaker: mobama_weekly_2014 0.116, nixon_resignation_1974 0.369; range [0.116, 0.369] |
| test | babble 10 dB SNR | R1 |  | D5- | 139 | 1.61 | per speaker: mobama_weekly_2014 0.487, nixon_resignation_1974 2.72; range [0.487, 2.72] |
| test | babble 10 dB SNR | R1 |  | D9- | 124 | 1.43 | per speaker: mobama_weekly_2014 2.04, nixon_resignation_1974 0.83; range [0.83, 2.04] |
| test | babble 20 dB SNR | R1 |  | D1+ | 289 | 3.34 | per speaker: mobama_weekly_2014 0.72, nixon_resignation_1974 5.95; range [0.72, 5.95] |
| test | babble 20 dB SNR | R1 |  | D1+ whole clip | 6 | 0.0694 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.138; range [0, 0.138] |
| test | babble 20 dB SNR | R1 |  | D1- | 32 | 0.37 | per speaker: mobama_weekly_2014 0.209, nixon_resignation_1974 0.53; range [0.209, 0.53] |
| test | babble 20 dB SNR | R1 |  | D2+ | 12 | 0.139 | per speaker: mobama_weekly_2014 0.186, nixon_resignation_1974 0.092; range [0.092, 0.186] |
| test | babble 20 dB SNR | R1 |  | D2- | 565 | 6.53 | per speaker: mobama_weekly_2014 1.23, nixon_resignation_1974 11.8; range [1.23, 11.8] |
| test | babble 20 dB SNR | R1 |  | D4- | 7 | 0.081 | per speaker: mobama_weekly_2014 0.023, nixon_resignation_1974 0.138; range [0.023, 0.138] |
| test | babble 20 dB SNR | R1 |  | D5- | 204 | 2.36 | per speaker: mobama_weekly_2014 0.209, nixon_resignation_1974 4.5; range [0.209, 4.5] |
| test | babble 20 dB SNR | R1 |  | D9- | 29 | 0.335 | per speaker: mobama_weekly_2014 0.232, nixon_resignation_1974 0.438; range [0.232, 0.438] |
| val+test | gain +6 dB | R1 |  | D1+ | 3 | 0.052 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.138] |
| val+test | gain +6 dB | R1 |  | D1- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | gain +6 dB | R1 |  | D2+ | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.069] |
| val+test | gain +6 dB | R1 |  | D2- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.069] |
| val+test | gain +6 dB | R1 |  | D4- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.069] |
| val+test | gain +6 dB | R1 |  | D9- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | gain -6 dB | R1 |  | D1+ | 4 | 0.0693 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0.069, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.208] |
| val+test | gain -6 dB | R1 |  | D1- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| val+test | gain -6 dB | R1 |  | D2+ | 3 | 0.052 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.07] |
| val+test | gain -6 dB | R1 |  | D2- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.07] |
| val+test | gain -6 dB | R1 |  | D9- | 5 | 0.0867 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069, mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| val+test | low-pass 3.4 kHz | R1 |  | D1+ | 5 | 0.0867 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0, 0.139] |
| val+test | low-pass 3.4 kHz | R1 |  | D1- | 27 | 0.468 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069, mobama_weekly_2014 1.6, nixon_resignation_1974 0.069; range [0.069, 1.6] |
| val+test | low-pass 3.4 kHz | R1 |  | D2+ | 7 | 0.121 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0, mobama_weekly_2014 0.279, nixon_resignation_1974 0.069; range [0, 0.279] |
| val+test | low-pass 3.4 kHz | R1 |  | D2- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.07] |
| val+test | low-pass 3.4 kHz | R1 |  | D5- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | low-pass 3.4 kHz | R1 |  | D9- | 10 | 0.173 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.139, mobama_weekly_2014 0.279, nixon_resignation_1974 0.138; range [0.138, 0.279] |
| val+test | white noise 20 dB SNR | R1 |  | D1+ | 25 | 0.144 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.162, mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.138, 0.162] |
| val+test | white noise 20 dB SNR | R1 |  | D1- | 83 | 0.48 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 0.324, mobama_weekly_2014 0.487, nixon_resignation_1974 0.507; range [0.324, 0.6] |
| val+test | white noise 20 dB SNR | R1 |  | D2+ | 105 | 0.607 | per speaker: eisenhower_farewell_1961 0.438, lbush_radio_2001 0.74, mobama_weekly_2014 0.348, nixon_resignation_1974 0.899; range [0.348, 0.899] |
| val+test | white noise 20 dB SNR | R1 |  | D2- | 10 | 0.0578 | per speaker: eisenhower_farewell_1961 0.092, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.092] |
| val+test | white noise 20 dB SNR | R1 |  | D3- | 1 | 0.0058 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.023, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.023] |
| val+test | white noise 20 dB SNR | R1 |  | D4- | 11 | 0.0636 | per speaker: eisenhower_farewell_1961 0.115, lbush_radio_2001 0.069, mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.115] |
| val+test | white noise 20 dB SNR | R1 |  | D5- | 6 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.139, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.139] |
| val+test | white noise 20 dB SNR | R1 |  | D6- | 2 | 0.0116 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0, mobama_weekly_2014 0.023, nixon_resignation_1974 0; range [0, 0.023] |
| val+test | white noise 20 dB SNR | R1 |  | D9- | 145 | 0.838 | per speaker: eisenhower_farewell_1961 0.553, lbush_radio_2001 1.85, mobama_weekly_2014 0.325, nixon_resignation_1974 0.622; range [0.325, 1.85] |
| val+test | MP3 64 kbit/s | R1 |  | D1+ | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.138] |
| val+test | MP3 64 kbit/s | R1 |  | D1- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | MP3 64 kbit/s | R1 |  | D2+ | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | MP3 64 kbit/s | R1 |  | D2- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | MP3 64 kbit/s | R1 |  | D9- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | dynamic-range compression | R1 |  | D1+ | 48 | 0.832 | per speaker: eisenhower_farewell_1961 2.84, lbush_radio_2001 0.139, mobama_weekly_2014 0.07, nixon_resignation_1974 0.277; range [0.07, 2.84] |
| val+test | dynamic-range compression | R1 |  | D1+ whole clip | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.069] |
| val+test | dynamic-range compression | R1 |  | D1- | 6 | 0.104 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.346] |
| val+test | dynamic-range compression | R1 |  | D2+ | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.069] |
| val+test | dynamic-range compression | R1 |  | D2- | 91 | 1.58 | per speaker: eisenhower_farewell_1961 3.94, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 2.35; range [0, 3.94] |
| val+test | dynamic-range compression | R1 |  | D3- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | dynamic-range compression | R1 |  | D4- | 12 | 0.208 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.555, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.555] |
| val+test | dynamic-range compression | R1 |  | D5- | 93 | 1.61 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 3.96, mobama_weekly_2014 1.74, nixon_resignation_1974 0.277; range [0.277, 3.96] |
| val+test | dynamic-range compression | R1 |  | D6- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.069] |
| val+test | dynamic-range compression | R1 |  | D9- | 7 | 0.121 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.139, mobama_weekly_2014 0.139, nixon_resignation_1974 0.069; range [0.069, 0.139] |
| val+test | room reverb RT60 0.4 s | R1 |  | D1+ | 41 | 0.237 | per speaker: eisenhower_farewell_1961 0.323, lbush_radio_2001 0.347, mobama_weekly_2014 0.07, nixon_resignation_1974 0.207; range [0.07, 0.347] |
| val+test | room reverb RT60 0.4 s | R1 |  | D1- | 8 | 0.0462 | per speaker: eisenhower_farewell_1961 0.046, lbush_radio_2001 0, mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| val+test | room reverb RT60 0.4 s | R1 |  | D2+ | 9 | 0.052 | per speaker: eisenhower_farewell_1961 0.092, lbush_radio_2001 0.023, mobama_weekly_2014 0.07, nixon_resignation_1974 0.023; range [0.023, 0.092] |
| val+test | room reverb RT60 0.4 s | R1 |  | D2- | 7 | 0.0405 | per speaker: eisenhower_farewell_1961 0.092, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.092] |
| val+test | room reverb RT60 0.4 s | R1 |  | D3- | 15 | 0.0867 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0.162, mobama_weekly_2014 0.116, nixon_resignation_1974 0.046; range [0.023, 0.162] |
| val+test | room reverb RT60 0.4 s | R1 |  | D4- | 17 | 0.0982 | per speaker: eisenhower_farewell_1961 0.277, lbush_radio_2001 0.023, mobama_weekly_2014 0.023, nixon_resignation_1974 0.069; range [0.023, 0.277] |
| val+test | room reverb RT60 0.4 s | R1 |  | D5- | 9 | 0.052 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.07] |
| val+test | room reverb RT60 0.4 s | R1 |  | D9- | 24 | 0.139 | per speaker: eisenhower_farewell_1961 0.115, lbush_radio_2001 0.185, mobama_weekly_2014 0.186, nixon_resignation_1974 0.069; range [0.069, 0.186] |
| val+test | phone band + mu-law (participant only) | R1 |  | D1+ | 9 | 0.156 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0, mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0, 0.346] |
| val+test | phone band + mu-law (participant only) | R1 |  | D1- | 31 | 0.537 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069, mobama_weekly_2014 0.418, nixon_resignation_1974 1.66; range [0, 1.66] |
| val+test | phone band + mu-law (participant only) | R1 |  | D2+ | 14 | 0.243 | per speaker: eisenhower_farewell_1961 0.415, lbush_radio_2001 0, mobama_weekly_2014 0.418, nixon_resignation_1974 0.138; range [0, 0.418] |
| val+test | phone band + mu-law (participant only) | R1 |  | D2- | 4 | 0.0693 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.208] |
| val+test | phone band + mu-law (participant only) | R1 |  | D3- | 99 | 1.72 | per speaker: eisenhower_farewell_1961 1.11, lbush_radio_2001 0.069, mobama_weekly_2014 0.139, nixon_resignation_1974 5.53; range [0.069, 5.53] |
| val+test | phone band + mu-law (participant only) | R1 |  | D4- | 26 | 0.451 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.139, mobama_weekly_2014 0.279, nixon_resignation_1974 1.04; range [0.139, 1.04] |
| val+test | phone band + mu-law (participant only) | R1 |  | D5- | 12 | 0.208 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.139, mobama_weekly_2014 0.279, nixon_resignation_1974 0.069; range [0.069, 0.346] |
| val+test | phone band + mu-law (participant only) | R1 |  | D6- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | phone band + mu-law (participant only) | R1 |  | D9- | 16 | 0.277 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.347, mobama_weekly_2014 0.487, nixon_resignation_1974 0.138; range [0.138, 0.487] |
| val+test | WORLD speaker transform | R1 |  | D1+ | 8 | 0.139 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069, mobama_weekly_2014 0.139, nixon_resignation_1974 0.207; range [0.069, 0.207] |
| val+test | WORLD speaker transform | R1 |  | D1- | 3 | 0.052 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.07] |
| val+test | WORLD speaker transform | R1 |  | D2+ | 5 | 0.0867 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0, mobama_weekly_2014 0.139, nixon_resignation_1974 0.069; range [0, 0.139] |
| val+test | WORLD speaker transform | R1 |  | D2- | 3 | 0.052 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.07] |
| val+test | WORLD speaker transform | R1 |  | D3- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| val+test | WORLD speaker transform | R1 |  | D4- | 3 | 0.052 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0.069, mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.069] |
| val+test | WORLD speaker transform | R1 |  | D5- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | WORLD speaker transform | R1 |  | D9- | 23 | 0.399 | per speaker: eisenhower_farewell_1961 0.899, lbush_radio_2001 0.278, mobama_weekly_2014 0.209, nixon_resignation_1974 0.207; range [0.207, 0.899] |
| val+test | babble 10 dB SNR | R1 |  | D1+ | 1262 | 7.29 | per speaker: eisenhower_farewell_1961 6.66, lbush_radio_2001 8.17, mobama_weekly_2014 6.24, nixon_resignation_1974 8.09; range [6.24, 8.17] |
| val+test | babble 10 dB SNR | R1 |  | D1+ whole clip | 98 | 0.566 | per speaker: eisenhower_farewell_1961 0.992, lbush_radio_2001 0.139, mobama_weekly_2014 0.116, nixon_resignation_1974 1.01; range [0.116, 1.01] |
| val+test | babble 10 dB SNR | R1 |  | D1- | 553 | 3.2 | per speaker: eisenhower_farewell_1961 5.03, lbush_radio_2001 1.55, mobama_weekly_2014 0.998, nixon_resignation_1974 5.19; range [0.998, 5.19] |
| val+test | babble 10 dB SNR | R1 |  | D2+ | 20 | 0.116 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0.139, mobama_weekly_2014 0.116, nixon_resignation_1974 0.184; range [0.023, 0.184] |
| val+test | babble 10 dB SNR | R1 |  | D2- | 1835 | 10.6 | per speaker: eisenhower_farewell_1961 12, lbush_radio_2001 7.47, mobama_weekly_2014 10.2, nixon_resignation_1974 12.7; range [7.47, 12.7] |
| val+test | babble 10 dB SNR | R1 |  | D3- | 59 | 0.341 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0.324, mobama_weekly_2014 0.093, nixon_resignation_1974 0.738; range [0.093, 0.738] |
| val+test | babble 10 dB SNR | R1 |  | D4- | 68 | 0.393 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 0.486, mobama_weekly_2014 0.116, nixon_resignation_1974 0.369; range [0.116, 0.6] |
| val+test | babble 10 dB SNR | R1 |  | D5- | 244 | 1.41 | per speaker: eisenhower_farewell_1961 1.25, lbush_radio_2001 1.18, mobama_weekly_2014 0.487, nixon_resignation_1974 2.72; range [0.487, 2.72] |
| val+test | babble 10 dB SNR | R1 |  | D9- | 246 | 1.42 | per speaker: eisenhower_farewell_1961 0.438, lbush_radio_2001 2.38, mobama_weekly_2014 2.04, nixon_resignation_1974 0.83; range [0.438, 2.38] |
| val+test | babble 20 dB SNR | R1 |  | D1+ | 511 | 2.95 | per speaker: eisenhower_farewell_1961 3.27, lbush_radio_2001 1.85, mobama_weekly_2014 0.72, nixon_resignation_1974 5.95; range [0.72, 5.95] |
| val+test | babble 20 dB SNR | R1 |  | D1+ whole clip | 9 | 0.052 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.138; range [0, 0.138] |
| val+test | babble 20 dB SNR | R1 |  | D1- | 54 | 0.312 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 0.023, mobama_weekly_2014 0.209, nixon_resignation_1974 0.53; range [0.023, 0.53] |
| val+test | babble 20 dB SNR | R1 |  | D2+ | 59 | 0.341 | per speaker: eisenhower_farewell_1961 0.507, lbush_radio_2001 0.579, mobama_weekly_2014 0.186, nixon_resignation_1974 0.092; range [0.092, 0.579] |
| val+test | babble 20 dB SNR | R1 |  | D2- | 859 | 4.96 | per speaker: eisenhower_farewell_1961 4.87, lbush_radio_2001 1.92, mobama_weekly_2014 1.23, nixon_resignation_1974 11.8; range [1.23, 11.8] |
| val+test | babble 20 dB SNR | R1 |  | D3- | 2 | 0.0116 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0.023, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.023] |
| val+test | babble 20 dB SNR | R1 |  | D4- | 18 | 0.104 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.116, mobama_weekly_2014 0.023, nixon_resignation_1974 0.138; range [0.023, 0.138] |
| val+test | babble 20 dB SNR | R1 |  | D5- | 280 | 1.62 | per speaker: eisenhower_farewell_1961 1.04, lbush_radio_2001 0.717, mobama_weekly_2014 0.209, nixon_resignation_1974 4.5; range [0.209, 4.5] |
| val+test | babble 20 dB SNR | R1 |  | D6- | 1 | 0.0058 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.023] |
| val+test | babble 20 dB SNR | R1 |  | D9- | 79 | 0.457 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0.949, mobama_weekly_2014 0.232, nixon_resignation_1974 0.438; range [0.208, 0.949] |
| check readers | white noise 20 dB SNR | R2 | single | D2+ | 6 | 0.258 | per recording: gettysburg_dj 0, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.662] |
| check readers | phone band + mu-law (participant only) | R2 | single | D2+ | 2 | 0.258 | per recording: gettysburg_dj 0, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.662] |
| check readers | phone band + mu-law (participant only) | R2 | single | D5- | 1 | 0.129 | per recording: gettysburg_dj 0.437, gettysburg_sa 0, gettysburg_tg 0; range [0, 0.437] |
| check readers | babble 10 dB SNR | R2 | single | D1+ | 24 | 1.03 | per recording: gettysburg_dj 2.77, gettysburg_sa 0.552, gettysburg_tg 0; range [0, 2.77] |
| check readers | babble 10 dB SNR | R2 | single | D1- | 2 | 0.0859 | per recording: gettysburg_dj 0, gettysburg_sa 0.221, gettysburg_tg 0; range [0, 0.221] |
| check readers | babble 10 dB SNR | R2 | single | D2- | 21 | 0.902 | per recording: gettysburg_dj 0.873, gettysburg_sa 0.993, gettysburg_tg 0.817; range [0.817, 0.993] |
| check readers | babble 10 dB SNR | R2 | single | D5- | 1 | 0.043 | per recording: gettysburg_dj 0.146, gettysburg_sa 0, gettysburg_tg 0; range [0, 0.146] |
| check readers | babble 10 dB SNR | R2 | consensus5 | D1+ | 5 | 1.29 | per recording: gettysburg_dj 3.49, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 3.49] |
| check readers | babble 10 dB SNR | R2 | consensus5 | D2- | 16 | 4.12 | per recording: gettysburg_dj 5.24, gettysburg_sa 4.64, gettysburg_tg 2.45; range [2.45, 5.24] |
| check readers | babble 20 dB SNR | R2 | single | D2- | 2 | 0.0859 | per recording: gettysburg_dj 0, gettysburg_sa 0, gettysburg_tg 0.272; range [0, 0.272] |
| check readers | babble 20 dB SNR | R2 | single | D5- | 1 | 0.043 | per recording: gettysburg_dj 0.146, gettysburg_sa 0, gettysburg_tg 0; range [0, 0.146] |
| check readers | babble 20 dB SNR | R2 | consensus5 | D2- | 7 | 1.8 | per recording: gettysburg_dj 0.873, gettysburg_sa 1.99, gettysburg_tg 2.45; range [0.873, 2.45] |

Detections kept per truth key:

| split | condition | regime | key | kept / found (all seeds) | fraction | interval | kept in every seed / unique |
|---|---|---|---|---|---|---|---|
| train | gain +6 dB | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | gain +6 dB | R1 | D1- | 26/27 | 0.963 | 95% [0.889, 1] | 26/27 |
| train | gain +6 dB | R1 | D2+ | 35/35 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 35/35 |
| train | gain +6 dB | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | gain +6 dB | R1 | D3- | 12/12 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | gain +6 dB | R1 | D4- | 11/11 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 11/11 |
| train | gain +6 dB | R1 | D5- | 44/45 | 0.978 | 95% [0.935, 1] | 44/45 |
| train | gain +6 dB | R1 | D6- | 9/10 | 0.9 | 95% [0.7, 1] | 9/10 |
| train | gain +6 dB | R1 | D9- | 3/3 | 1 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [1, 1] | 3/3 |
| train | gain +6 dB | R2 | D2+ | 4/4 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | gain +6 dB | R2 | D5- | 4/4 | 1 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | gain -6 dB | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | gain -6 dB | R1 | D1- | 27/27 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 27/27 |
| train | gain -6 dB | R1 | D2+ | 34/35 | 0.971 | 95% [0.903, 1] | 34/35 |
| train | gain -6 dB | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | gain -6 dB | R1 | D3- | 12/12 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | gain -6 dB | R1 | D4- | 10/11 | 0.909 | 95% [0.769, 1] | 10/11 |
| train | gain -6 dB | R1 | D5- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | gain -6 dB | R1 | D6- | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | gain -6 dB | R1 | D9- | 3/3 | 1 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [1, 1] | 3/3 |
| train | gain -6 dB | R2 | D2+ | 4/4 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | gain -6 dB | R2 | D5- | 4/4 | 1 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | low-pass 3.4 kHz | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | low-pass 3.4 kHz | R1 | D1- | 26/27 | 0.963 | 95% [0.889, 1] | 26/27 |
| train | low-pass 3.4 kHz | R1 | D2+ | 35/35 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 35/35 |
| train | low-pass 3.4 kHz | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | low-pass 3.4 kHz | R1 | D3- | 12/12 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | low-pass 3.4 kHz | R1 | D4- | 10/11 | 0.909 | 95% [0.769, 1] | 10/11 |
| train | low-pass 3.4 kHz | R1 | D5- | 43/45 | 0.956 | 95% [0.898, 1] | 43/45 |
| train | low-pass 3.4 kHz | R1 | D6- | 8/10 | 0.8 | 95% [0.5, 1] | 8/10 |
| train | low-pass 3.4 kHz | R1 | D9- | 3/3 | 1 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [1, 1] | 3/3 |
| train | low-pass 3.4 kHz | R2 | D2+ | 4/4 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | low-pass 3.4 kHz | R2 | D5- | 3/4 | 0.75 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 0, greenman_reagan__x3_L3 1; range [0, 1] | 3/4 |
| train | white noise 20 dB SNR | R1 | D1+ | 30/30 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | white noise 20 dB SNR | R1 | D1- | 81/81 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 27/27 |
| train | white noise 20 dB SNR | R1 | D2+ | 102/105 | 0.971 | 95% [0.909, 1] | 34/35 |
| train | white noise 20 dB SNR | R1 | D2- | 132/135 | 0.978 | 95% [0.931, 1] | 44/45 |
| train | white noise 20 dB SNR | R1 | D3- | 36/36 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | white noise 20 dB SNR | R1 | D4- | 29/33 | 0.879 | 95% [0.692, 1] | 9/11 |
| train | white noise 20 dB SNR | R1 | D5- | 99/135 | 0.733 | 95% [0.626, 0.83] | 31/45 |
| train | white noise 20 dB SNR | R1 | D6- | 10/30 | 0.333 | 95% [0.067, 0.6] | 3/10 |
| train | white noise 20 dB SNR | R1 | D9- | 6/9 | 0.667 | per recording: gwbush_911_2001__extra_L2A 0.333, harris_uncsw_2021__extra_botched_D1 0.667, hclinton_tomorrow_2010__extra_L3A 1; range [0.333, 1] | 1/3 |
| train | white noise 20 dB SNR | R2 | D2+ | 12/12 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | white noise 20 dB SNR | R2 | D5- | 6/12 | 0.5 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 0, greenman_reagan__x3_L3 0; range [0, 1] | 2/4 |
| train | MP3 64 kbit/s | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | MP3 64 kbit/s | R1 | D1- | 27/27 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 27/27 |
| train | MP3 64 kbit/s | R1 | D2+ | 34/35 | 0.971 | 95% [0.903, 1] | 34/35 |
| train | MP3 64 kbit/s | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | MP3 64 kbit/s | R1 | D3- | 12/12 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | MP3 64 kbit/s | R1 | D4- | 10/11 | 0.909 | 95% [0.769, 1] | 10/11 |
| train | MP3 64 kbit/s | R1 | D5- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | MP3 64 kbit/s | R1 | D6- | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | MP3 64 kbit/s | R1 | D9- | 2/3 | 0.667 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 0, hclinton_tomorrow_2010__extra_L3A 1; range [0, 1] | 2/3 |
| train | MP3 64 kbit/s | R2 | D2+ | 4/4 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | MP3 64 kbit/s | R2 | D5- | 4/4 | 1 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | dynamic-range compression | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | dynamic-range compression | R1 | D1- | 26/27 | 0.963 | 95% [0.889, 1] | 26/27 |
| train | dynamic-range compression | R1 | D2+ | 34/35 | 0.971 | 95% [0.903, 1] | 34/35 |
| train | dynamic-range compression | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | dynamic-range compression | R1 | D3- | 12/12 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | dynamic-range compression | R1 | D4- | 5/11 | 0.455 | 95% [0.2, 0.727] | 5/11 |
| train | dynamic-range compression | R1 | D5- | 13/45 | 0.289 | 95% [0.163, 0.444] | 13/45 |
| train | dynamic-range compression | R1 | D6- | 9/10 | 0.9 | 95% [0.7, 1] | 9/10 |
| train | dynamic-range compression | R1 | D9- | 3/3 | 1 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [1, 1] | 3/3 |
| train | dynamic-range compression | R2 | D2+ | 4/4 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | dynamic-range compression | R2 | D5- | 0/4 | 0 | per recording: greenman_reagan__G5 0, greenman_reagan__extra_x1_L2 0, greenman_reagan__x3_L3 0; range [0, 0] | 0/4 |
| train | room reverb RT60 0.4 s | R1 | D1+ | 30/30 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | room reverb RT60 0.4 s | R1 | D1- | 80/81 | 0.988 | 95% [0.963, 1] | 26/27 |
| train | room reverb RT60 0.4 s | R1 | D2+ | 90/105 | 0.857 | 95% [0.735, 0.952] | 29/35 |
| train | room reverb RT60 0.4 s | R1 | D2- | 135/135 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | room reverb RT60 0.4 s | R1 | D3- | 36/36 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | room reverb RT60 0.4 s | R1 | D4- | 26/33 | 0.788 | 95% [0.564, 1] | 7/11 |
| train | room reverb RT60 0.4 s | R1 | D5- | 127/135 | 0.941 | 95% [0.884, 1] | 42/45 |
| train | room reverb RT60 0.4 s | R1 | D6- | 30/30 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | room reverb RT60 0.4 s | R1 | D9- | 9/9 | 1 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [1, 1] | 3/3 |
| train | room reverb RT60 0.4 s | R2 | D2+ | 3/12 | 0.25 | per recording: greenman_reagan__extra_botched_D2 0, greenman_reagan__extra_x6_L3 0, greenman_reagan__x3_L3 1; range [0, 1] | 1/4 |
| train | room reverb RT60 0.4 s | R2 | D5- | 12/12 | 1 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | phone band + mu-law (participant only) | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | phone band + mu-law (participant only) | R1 | D1- | 27/27 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 27/27 |
| train | phone band + mu-law (participant only) | R1 | D2+ | 35/35 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 35/35 |
| train | phone band + mu-law (participant only) | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | phone band + mu-law (participant only) | R1 | D3- | 12/12 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | phone band + mu-law (participant only) | R1 | D4- | 9/11 | 0.818 | 95% [0.545, 1] | 9/11 |
| train | phone band + mu-law (participant only) | R1 | D5- | 38/45 | 0.844 | 95% [0.744, 0.935] | 38/45 |
| train | phone band + mu-law (participant only) | R1 | D6- | 7/10 | 0.7 | 95% [0.4, 1] | 7/10 |
| train | phone band + mu-law (participant only) | R1 | D9- | 2/3 | 0.667 | per recording: gwbush_911_2001__extra_L2A 0, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [0, 1] | 2/3 |
| train | phone band + mu-law (participant only) | R2 | D2+ | 4/4 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | phone band + mu-law (participant only) | R2 | D5- | 2/4 | 0.5 | per recording: greenman_reagan__G5 0.5, greenman_reagan__extra_x1_L2 0, greenman_reagan__x3_L3 1; range [0, 1] | 2/4 |
| train | WORLD speaker transform | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | WORLD speaker transform | R1 | D1- | 27/27 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 27/27 |
| train | WORLD speaker transform | R1 | D2+ | 34/35 | 0.971 | 95% [0.903, 1] | 34/35 |
| train | WORLD speaker transform | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | WORLD speaker transform | R1 | D3- | 11/12 | 0.917 | 95% [0.75, 1] | 11/12 |
| train | WORLD speaker transform | R1 | D4- | 10/11 | 0.909 | 95% [0.7, 1] | 10/11 |
| train | WORLD speaker transform | R1 | D5- | 44/45 | 0.978 | 95% [0.935, 1] | 44/45 |
| train | WORLD speaker transform | R1 | D6- | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | WORLD speaker transform | R1 | D9- | 2/3 | 0.667 | per recording: gwbush_911_2001__extra_L2A 0, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [0, 1] | 2/3 |
| train | WORLD speaker transform | R2 | D2+ | 2/4 | 0.5 | per recording: greenman_reagan__extra_botched_D2 0.5, greenman_reagan__extra_x6_L3 0, greenman_reagan__x3_L3 1; range [0, 1] | 2/4 |
| train | WORLD speaker transform | R2 | D5- | 4/4 | 1 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | babble 10 dB SNR | R1 | D1+ | 26/30 | 0.867 | 95% [0.667, 1] | 8/10 |
| train | babble 10 dB SNR | R1 | D1- | 67/81 | 0.827 | 95% [0.716, 0.926] | 18/27 |
| train | babble 10 dB SNR | R1 | D2+ | 9/105 | 0.0857 | 95% [0.027, 0.171] | 1/35 |
| train | babble 10 dB SNR | R1 | D2- | 135/135 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | babble 10 dB SNR | R1 | D3- | 11/36 | 0.306 | 95% [0.139, 0.472] | 0/12 |
| train | babble 10 dB SNR | R1 | D4- | 22/33 | 0.667 | 95% [0.5, 0.867] | 4/11 |
| train | babble 10 dB SNR | R1 | D5- | 74/135 | 0.548 | 95% [0.435, 0.667] | 14/45 |
| train | babble 10 dB SNR | R1 | D6- | 9/30 | 0.3 | 95% [0.133, 0.533] | 1/10 |
| train | babble 10 dB SNR | R1 | D9- | 6/9 | 0.667 | per recording: gwbush_911_2001__extra_L2A 0, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [0, 1] | 2/3 |
| train | babble 10 dB SNR | R2 | D2+ | 0/12 | 0 | per recording: greenman_reagan__extra_botched_D2 0, greenman_reagan__extra_x6_L3 0, greenman_reagan__x3_L3 0; range [0, 0] | 0/4 |
| train | babble 10 dB SNR | R2 | D5- | 1/12 | 0.0833 | per recording: greenman_reagan__G5 0.167, greenman_reagan__extra_x1_L2 0, greenman_reagan__x3_L3 0; range [0, 0.167] | 0/4 |
| train | babble 20 dB SNR | R1 | D1+ | 30/30 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | babble 20 dB SNR | R1 | D1- | 77/81 | 0.951 | 95% [0.901, 0.988] | 23/27 |
| train | babble 20 dB SNR | R1 | D2+ | 75/105 | 0.714 | 95% [0.616, 0.806] | 16/35 |
| train | babble 20 dB SNR | R1 | D2- | 135/135 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | babble 20 dB SNR | R1 | D3- | 36/36 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | babble 20 dB SNR | R1 | D4- | 27/33 | 0.818 | 95% [0.667, 1] | 8/11 |
| train | babble 20 dB SNR | R1 | D5- | 110/135 | 0.815 | 95% [0.723, 0.906] | 33/45 |
| train | babble 20 dB SNR | R1 | D6- | 23/30 | 0.767 | 95% [0.567, 0.967] | 6/10 |
| train | babble 20 dB SNR | R1 | D9- | 9/9 | 1 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [1, 1] | 3/3 |
| train | babble 20 dB SNR | R2 | D2+ | 1/12 | 0.0833 | per recording: greenman_reagan__extra_botched_D2 0.167, greenman_reagan__extra_x6_L3 0, greenman_reagan__x3_L3 0; range [0, 0.167] | 0/4 |
| train | babble 20 dB SNR | R2 | D5- | 4/12 | 0.333 | per recording: greenman_reagan__G5 0.667, greenman_reagan__extra_x1_L2 0, greenman_reagan__x3_L3 0; range [0, 0.667] | 1/4 |
| val | gain +6 dB | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | gain +6 dB | R1 | D1- | 9/9 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 9/9 |
| val | gain +6 dB | R1 | D2+ | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 13/13 |
| val | gain +6 dB | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | gain +6 dB | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | gain +6 dB | R1 | D4- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | gain +6 dB | R1 | D5- | 11/11 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 11/11 |
| val | gain +6 dB | R1 | D6- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | gain +6 dB | R1 | D9- | 3/3 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 3/3 |
| val | gain -6 dB | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | gain -6 dB | R1 | D1- | 9/9 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 9/9 |
| val | gain -6 dB | R1 | D2+ | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 13/13 |
| val | gain -6 dB | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | gain -6 dB | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | gain -6 dB | R1 | D4- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | gain -6 dB | R1 | D5- | 11/11 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 11/11 |
| val | gain -6 dB | R1 | D6- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | gain -6 dB | R1 | D9- | 3/3 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 3/3 |
| val | low-pass 3.4 kHz | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | low-pass 3.4 kHz | R1 | D1- | 9/9 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 9/9 |
| val | low-pass 3.4 kHz | R1 | D2+ | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 13/13 |
| val | low-pass 3.4 kHz | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | low-pass 3.4 kHz | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | low-pass 3.4 kHz | R1 | D4- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | low-pass 3.4 kHz | R1 | D5- | 11/11 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 11/11 |
| val | low-pass 3.4 kHz | R1 | D6- | 1/4 | 0.25 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 0; range [0, 0.5] | 1/4 |
| val | low-pass 3.4 kHz | R1 | D9- | 3/3 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 3/3 |
| val | white noise 20 dB SNR | R1 | D1+ | 12/12 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | white noise 20 dB SNR | R1 | D1- | 26/27 | 0.963 | per speaker: eisenhower_farewell_1961 0.933, lbush_radio_2001 1; range [0.933, 1] | 8/9 |
| val | white noise 20 dB SNR | R1 | D2+ | 39/39 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 13/13 |
| val | white noise 20 dB SNR | R1 | D2- | 51/51 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | white noise 20 dB SNR | R1 | D3- | 15/15 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | white noise 20 dB SNR | R1 | D4- | 21/21 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | white noise 20 dB SNR | R1 | D5- | 26/33 | 0.788 | per speaker: eisenhower_farewell_1961 0.917, lbush_radio_2001 0.714; range [0.714, 0.917] | 8/11 |
| val | white noise 20 dB SNR | R1 | D6- | 1/12 | 0.0833 | per speaker: eisenhower_farewell_1961 0.167, lbush_radio_2001 0; range [0, 0.167] | 0/4 |
| val | white noise 20 dB SNR | R1 | D9- | 8/9 | 0.889 | per speaker: eisenhower_farewell_1961 0.833, lbush_radio_2001 1; range [0.833, 1] | 2/3 |
| val | MP3 64 kbit/s | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | MP3 64 kbit/s | R1 | D1- | 9/9 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 9/9 |
| val | MP3 64 kbit/s | R1 | D2+ | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 13/13 |
| val | MP3 64 kbit/s | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | MP3 64 kbit/s | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | MP3 64 kbit/s | R1 | D4- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | MP3 64 kbit/s | R1 | D5- | 11/11 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 11/11 |
| val | MP3 64 kbit/s | R1 | D6- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | MP3 64 kbit/s | R1 | D9- | 3/3 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 3/3 |
| val | dynamic-range compression | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | dynamic-range compression | R1 | D1- | 7/9 | 0.778 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 1; range [0.6, 1] | 7/9 |
| val | dynamic-range compression | R1 | D2+ | 12/13 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857; range [0.857, 1] | 12/13 |
| val | dynamic-range compression | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | dynamic-range compression | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | dynamic-range compression | R1 | D4- | 5/7 | 0.714 | per speaker: eisenhower_farewell_1961 0.333, lbush_radio_2001 1; range [0.333, 1] | 5/7 |
| val | dynamic-range compression | R1 | D5- | 2/11 | 0.182 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.286; range [0, 0.286] | 2/11 |
| val | dynamic-range compression | R1 | D6- | 3/4 | 0.75 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.5; range [0.5, 1] | 3/4 |
| val | dynamic-range compression | R1 | D9- | 2/3 | 0.667 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 1; range [0.5, 1] | 2/3 |
| val | room reverb RT60 0.4 s | R1 | D1+ | 12/12 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | room reverb RT60 0.4 s | R1 | D1- | 25/27 | 0.926 | per speaker: eisenhower_farewell_1961 0.867, lbush_radio_2001 1; range [0.867, 1] | 8/9 |
| val | room reverb RT60 0.4 s | R1 | D2+ | 36/39 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857; range [0.857, 1] | 12/13 |
| val | room reverb RT60 0.4 s | R1 | D2- | 51/51 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | room reverb RT60 0.4 s | R1 | D3- | 15/15 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | room reverb RT60 0.4 s | R1 | D4- | 21/21 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | room reverb RT60 0.4 s | R1 | D5- | 32/33 | 0.97 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.952; range [0.952, 1] | 10/11 |
| val | room reverb RT60 0.4 s | R1 | D6- | 9/12 | 0.75 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.5; range [0.5, 1] | 3/4 |
| val | room reverb RT60 0.4 s | R1 | D9- | 7/9 | 0.778 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 1; range [0.667, 1] | 2/3 |
| val | phone band + mu-law (participant only) | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | phone band + mu-law (participant only) | R1 | D1- | 9/9 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 9/9 |
| val | phone band + mu-law (participant only) | R1 | D2+ | 12/13 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857; range [0.857, 1] | 12/13 |
| val | phone band + mu-law (participant only) | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | phone band + mu-law (participant only) | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | phone band + mu-law (participant only) | R1 | D4- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | phone band + mu-law (participant only) | R1 | D5- | 6/11 | 0.545 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 0.571; range [0.5, 0.571] | 6/11 |
| val | phone band + mu-law (participant only) | R1 | D6- | 2/4 | 0.5 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0; range [0, 1] | 2/4 |
| val | phone band + mu-law (participant only) | R1 | D9- | 3/3 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 3/3 |
| val | WORLD speaker transform | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | WORLD speaker transform | R1 | D1- | 9/9 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 9/9 |
| val | WORLD speaker transform | R1 | D2+ | 12/13 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857; range [0.857, 1] | 12/13 |
| val | WORLD speaker transform | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | WORLD speaker transform | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | WORLD speaker transform | R1 | D4- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | WORLD speaker transform | R1 | D5- | 11/11 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 11/11 |
| val | WORLD speaker transform | R1 | D6- | 3/4 | 0.75 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.5; range [0.5, 1] | 3/4 |
| val | WORLD speaker transform | R1 | D9- | 2/3 | 0.667 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 1; range [0.5, 1] | 2/3 |
| val | babble 10 dB SNR | R1 | D1+ | 9/12 | 0.75 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 0.833; range [0.667, 0.833] | 1/4 |
| val | babble 10 dB SNR | R1 | D1- | 22/27 | 0.815 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 1; range [0.667, 1] | 7/9 |
| val | babble 10 dB SNR | R1 | D2+ | 5/39 | 0.128 | per speaker: eisenhower_farewell_1961 0.111, lbush_radio_2001 0.143; range [0.111, 0.143] | 0/13 |
| val | babble 10 dB SNR | R1 | D2- | 51/51 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | babble 10 dB SNR | R1 | D3- | 11/15 | 0.733 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.333; range [0.333, 1] | 3/5 |
| val | babble 10 dB SNR | R1 | D4- | 20/21 | 0.952 | per speaker: eisenhower_farewell_1961 0.889, lbush_radio_2001 1; range [0.889, 1] | 6/7 |
| val | babble 10 dB SNR | R1 | D5- | 16/33 | 0.485 | per speaker: eisenhower_farewell_1961 0.583, lbush_radio_2001 0.429; range [0.429, 0.583] | 2/11 |
| val | babble 10 dB SNR | R1 | D6- | 1/12 | 0.0833 | per speaker: eisenhower_farewell_1961 0.167, lbush_radio_2001 0; range [0, 0.167] | 0/4 |
| val | babble 10 dB SNR | R1 | D9- | 8/9 | 0.889 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.667; range [0.667, 1] | 2/3 |
| val | babble 20 dB SNR | R1 | D1+ | 12/12 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | babble 20 dB SNR | R1 | D1- | 24/27 | 0.889 | per speaker: eisenhower_farewell_1961 0.8, lbush_radio_2001 1; range [0.8, 1] | 8/9 |
| val | babble 20 dB SNR | R1 | D2+ | 36/39 | 0.923 | per speaker: eisenhower_farewell_1961 0.889, lbush_radio_2001 0.952; range [0.889, 0.952] | 11/13 |
| val | babble 20 dB SNR | R1 | D2- | 51/51 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | babble 20 dB SNR | R1 | D3- | 15/15 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | babble 20 dB SNR | R1 | D4- | 21/21 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | babble 20 dB SNR | R1 | D5- | 23/33 | 0.697 | per speaker: eisenhower_farewell_1961 0.833, lbush_radio_2001 0.619; range [0.619, 0.833] | 6/11 |
| val | babble 20 dB SNR | R1 | D6- | 4/12 | 0.333 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 0; range [0, 0.667] | 1/4 |
| val | babble 20 dB SNR | R1 | D9- | 8/9 | 0.889 | per speaker: eisenhower_farewell_1961 0.833, lbush_radio_2001 1; range [0.833, 1] | 2/3 |
| test | gain +6 dB | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | gain +6 dB | R1 | D1- | 10/10 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | gain +6 dB | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | gain +6 dB | R1 | D2- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | gain +6 dB | R1 | D3- | 2/2 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | gain +6 dB | R1 | D4- | 6/6 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 6/6 |
| test | gain +6 dB | R1 | D5- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | gain +6 dB | R1 | D6- | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | gain +6 dB | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | gain -6 dB | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | gain -6 dB | R1 | D1- | 10/10 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | gain -6 dB | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | gain -6 dB | R1 | D2- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | gain -6 dB | R1 | D3- | 2/2 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | gain -6 dB | R1 | D4- | 6/6 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 6/6 |
| test | gain -6 dB | R1 | D5- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | gain -6 dB | R1 | D6- | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | gain -6 dB | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | low-pass 3.4 kHz | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | low-pass 3.4 kHz | R1 | D1- | 10/10 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | low-pass 3.4 kHz | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | low-pass 3.4 kHz | R1 | D2- | 18/19 | 0.947 | per speaker: mobama_weekly_2014 0.889, nixon_resignation_1974 1; range [0.889, 1] | 18/19 |
| test | low-pass 3.4 kHz | R1 | D3- | 2/2 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | low-pass 3.4 kHz | R1 | D4- | 5/6 | 0.833 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0; range [0, 1] | 5/6 |
| test | low-pass 3.4 kHz | R1 | D5- | 17/19 | 0.895 | per speaker: mobama_weekly_2014 0.778, nixon_resignation_1974 1; range [0.778, 1] | 17/19 |
| test | low-pass 3.4 kHz | R1 | D6- | 3/4 | 0.75 | per speaker: mobama_weekly_2014 0.5, nixon_resignation_1974 1; range [0.5, 1] | 3/4 |
| test | low-pass 3.4 kHz | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | white noise 20 dB SNR | R1 | D1+ | 12/12 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | white noise 20 dB SNR | R1 | D1- | 30/30 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | white noise 20 dB SNR | R1 | D2+ | 39/39 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | white noise 20 dB SNR | R1 | D2- | 54/57 | 0.947 | per speaker: mobama_weekly_2014 0.889, nixon_resignation_1974 1; range [0.889, 1] | 18/19 |
| test | white noise 20 dB SNR | R1 | D3- | 6/6 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | white noise 20 dB SNR | R1 | D4- | 18/18 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 6/6 |
| test | white noise 20 dB SNR | R1 | D5- | 48/57 | 0.842 | per speaker: mobama_weekly_2014 0.778, nixon_resignation_1974 0.9; range [0.778, 0.9] | 16/19 |
| test | white noise 20 dB SNR | R1 | D6- | 3/12 | 0.25 | per speaker: mobama_weekly_2014 0.5, nixon_resignation_1974 0; range [0, 0.5] | 1/4 |
| test | white noise 20 dB SNR | R1 | D9- | 3/3 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | MP3 64 kbit/s | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | MP3 64 kbit/s | R1 | D1- | 10/10 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | MP3 64 kbit/s | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | MP3 64 kbit/s | R1 | D2- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | MP3 64 kbit/s | R1 | D3- | 2/2 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | MP3 64 kbit/s | R1 | D4- | 6/6 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 6/6 |
| test | MP3 64 kbit/s | R1 | D5- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | MP3 64 kbit/s | R1 | D6- | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | MP3 64 kbit/s | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | dynamic-range compression | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | dynamic-range compression | R1 | D1- | 10/10 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | dynamic-range compression | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | dynamic-range compression | R1 | D2- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | dynamic-range compression | R1 | D3- | 2/2 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | dynamic-range compression | R1 | D4- | 2/6 | 0.333 | per speaker: mobama_weekly_2014 0.4, nixon_resignation_1974 0; range [0, 0.4] | 2/6 |
| test | dynamic-range compression | R1 | D5- | 4/19 | 0.21 | per speaker: mobama_weekly_2014 0.222, nixon_resignation_1974 0.2; range [0.2, 0.222] | 4/19 |
| test | dynamic-range compression | R1 | D6- | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | dynamic-range compression | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | room reverb RT60 0.4 s | R1 | D1+ | 12/12 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | room reverb RT60 0.4 s | R1 | D1- | 29/30 | 0.967 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0.933; range [0.933, 1] | 9/10 |
| test | room reverb RT60 0.4 s | R1 | D2+ | 39/39 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | room reverb RT60 0.4 s | R1 | D2- | 57/57 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | room reverb RT60 0.4 s | R1 | D3- | 5/6 | 0.833 | per speaker: nixon_resignation_1974 0.833; range [0.833, 0.833] | 1/2 |
| test | room reverb RT60 0.4 s | R1 | D4- | 18/18 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 6/6 |
| test | room reverb RT60 0.4 s | R1 | D5- | 57/57 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | room reverb RT60 0.4 s | R1 | D6- | 12/12 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | room reverb RT60 0.4 s | R1 | D9- | 2/3 | 0.667 | per speaker: nixon_resignation_1974 0.667; range [0.667, 0.667] | 0/1 |
| test | phone band + mu-law (participant only) | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | phone band + mu-law (participant only) | R1 | D1- | 9/10 | 0.9 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0.8; range [0.8, 1] | 9/10 |
| test | phone band + mu-law (participant only) | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | phone band + mu-law (participant only) | R1 | D2- | 18/19 | 0.947 | per speaker: mobama_weekly_2014 0.889, nixon_resignation_1974 1; range [0.889, 1] | 18/19 |
| test | phone band + mu-law (participant only) | R1 | D3- | 0/2 | 0 | per speaker: nixon_resignation_1974 0; range [0, 0] | 0/2 |
| test | phone band + mu-law (participant only) | R1 | D4- | 5/6 | 0.833 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0; range [0, 1] | 5/6 |
| test | phone band + mu-law (participant only) | R1 | D5- | 15/19 | 0.789 | per speaker: mobama_weekly_2014 0.556, nixon_resignation_1974 1; range [0.556, 1] | 15/19 |
| test | phone band + mu-law (participant only) | R1 | D6- | 3/4 | 0.75 | per speaker: mobama_weekly_2014 0.5, nixon_resignation_1974 1; range [0.5, 1] | 3/4 |
| test | phone band + mu-law (participant only) | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | WORLD speaker transform | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | WORLD speaker transform | R1 | D1- | 10/10 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | WORLD speaker transform | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | WORLD speaker transform | R1 | D2- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | WORLD speaker transform | R1 | D3- | 2/2 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | WORLD speaker transform | R1 | D4- | 5/6 | 0.833 | per speaker: mobama_weekly_2014 0.8, nixon_resignation_1974 1; range [0.8, 1] | 5/6 |
| test | WORLD speaker transform | R1 | D5- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | WORLD speaker transform | R1 | D6- | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | WORLD speaker transform | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | babble 10 dB SNR | R1 | D1+ | 6/12 | 0.5 | per speaker: mobama_weekly_2014 0.5, nixon_resignation_1974 0.5; range [0.5, 0.5] | 2/4 |
| test | babble 10 dB SNR | R1 | D1- | 21/30 | 0.7 | per speaker: mobama_weekly_2014 0.8, nixon_resignation_1974 0.6; range [0.6, 0.8] | 7/10 |
| test | babble 10 dB SNR | R1 | D2+ | 4/39 | 0.103 | per speaker: mobama_weekly_2014 0.167, nixon_resignation_1974 0.048; range [0.048, 0.167] | 0/13 |
| test | babble 10 dB SNR | R1 | D2- | 57/57 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | babble 10 dB SNR | R1 | D3- | 4/6 | 0.667 | per speaker: nixon_resignation_1974 0.667; range [0.667, 0.667] | 1/2 |
| test | babble 10 dB SNR | R1 | D4- | 13/18 | 0.722 | per speaker: mobama_weekly_2014 0.733, nixon_resignation_1974 0.667; range [0.667, 0.733] | 3/6 |
| test | babble 10 dB SNR | R1 | D5- | 30/57 | 0.526 | per speaker: mobama_weekly_2014 0.741, nixon_resignation_1974 0.333; range [0.333, 0.741] | 6/19 |
| test | babble 10 dB SNR | R1 | D6- | 3/12 | 0.25 | per speaker: mobama_weekly_2014 0.5, nixon_resignation_1974 0; range [0, 0.5] | 1/4 |
| test | babble 10 dB SNR | R1 | D9- | 3/3 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | babble 20 dB SNR | R1 | D1+ | 11/12 | 0.917 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0.833; range [0.833, 1] | 3/4 |
| test | babble 20 dB SNR | R1 | D1- | 24/30 | 0.8 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0.6; range [0.6, 1] | 8/10 |
| test | babble 20 dB SNR | R1 | D2+ | 24/39 | 0.615 | per speaker: mobama_weekly_2014 0.944, nixon_resignation_1974 0.333; range [0.333, 0.944] | 5/13 |
| test | babble 20 dB SNR | R1 | D2- | 55/57 | 0.965 | per speaker: mobama_weekly_2014 0.926, nixon_resignation_1974 1; range [0.926, 1] | 18/19 |
| test | babble 20 dB SNR | R1 | D3- | 6/6 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | babble 20 dB SNR | R1 | D4- | 17/18 | 0.944 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0.667; range [0.667, 1] | 5/6 |
| test | babble 20 dB SNR | R1 | D5- | 49/57 | 0.86 | per speaker: mobama_weekly_2014 0.889, nixon_resignation_1974 0.833; range [0.833, 0.889] | 14/19 |
| test | babble 20 dB SNR | R1 | D6- | 12/12 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | babble 20 dB SNR | R1 | D9- | 2/3 | 0.667 | per speaker: nixon_resignation_1974 0.667; range [0.667, 0.667] | 0/1 |
| val+test | gain +6 dB | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | gain +6 dB | R1 | D1- | 19/19 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| val+test | gain +6 dB | R1 | D2+ | 26/26 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 26/26 |
| val+test | gain +6 dB | R1 | D2- | 36/36 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | gain +6 dB | R1 | D3- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | gain +6 dB | R1 | D4- | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| val+test | gain +6 dB | R1 | D5- | 30/30 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 30/30 |
| val+test | gain +6 dB | R1 | D6- | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | gain +6 dB | R1 | D9- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| val+test | gain -6 dB | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | gain -6 dB | R1 | D1- | 19/19 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| val+test | gain -6 dB | R1 | D2+ | 26/26 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 26/26 |
| val+test | gain -6 dB | R1 | D2- | 36/36 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | gain -6 dB | R1 | D3- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | gain -6 dB | R1 | D4- | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| val+test | gain -6 dB | R1 | D5- | 30/30 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 30/30 |
| val+test | gain -6 dB | R1 | D6- | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | gain -6 dB | R1 | D9- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| val+test | low-pass 3.4 kHz | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | low-pass 3.4 kHz | R1 | D1- | 19/19 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| val+test | low-pass 3.4 kHz | R1 | D2+ | 26/26 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 26/26 |
| val+test | low-pass 3.4 kHz | R1 | D2- | 35/36 | 0.972 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 0.889, nixon_resignation_1974 1; range [0.889, 1] | 35/36 |
| val+test | low-pass 3.4 kHz | R1 | D3- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | low-pass 3.4 kHz | R1 | D4- | 12/13 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0; range [0, 1] | 12/13 |
| val+test | low-pass 3.4 kHz | R1 | D5- | 28/30 | 0.933 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 0.778, nixon_resignation_1974 1; range [0.778, 1] | 28/30 |
| val+test | low-pass 3.4 kHz | R1 | D6- | 4/8 | 0.5 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 0, mobama_weekly_2014 0.5, nixon_resignation_1974 1; range [0, 1] | 4/8 |
| val+test | low-pass 3.4 kHz | R1 | D9- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| val+test | white noise 20 dB SNR | R1 | D1+ | 24/24 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | white noise 20 dB SNR | R1 | D1- | 56/57 | 0.983 | per speaker: eisenhower_farewell_1961 0.933, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.933, 1] | 18/19 |
| val+test | white noise 20 dB SNR | R1 | D2+ | 78/78 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 26/26 |
| val+test | white noise 20 dB SNR | R1 | D2- | 105/108 | 0.972 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 0.889, nixon_resignation_1974 1; range [0.889, 1] | 35/36 |
| val+test | white noise 20 dB SNR | R1 | D3- | 21/21 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | white noise 20 dB SNR | R1 | D4- | 39/39 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| val+test | white noise 20 dB SNR | R1 | D5- | 74/90 | 0.822 | per speaker: eisenhower_farewell_1961 0.917, lbush_radio_2001 0.714, mobama_weekly_2014 0.778, nixon_resignation_1974 0.9; range [0.714, 0.917] | 24/30 |
| val+test | white noise 20 dB SNR | R1 | D6- | 4/24 | 0.167 | per speaker: eisenhower_farewell_1961 0.167, lbush_radio_2001 0, mobama_weekly_2014 0.5, nixon_resignation_1974 0; range [0, 0.5] | 1/8 |
| val+test | white noise 20 dB SNR | R1 | D9- | 11/12 | 0.917 | per speaker: eisenhower_farewell_1961 0.833, lbush_radio_2001 1, nixon_resignation_1974 1; range [0.833, 1] | 3/4 |
| val+test | MP3 64 kbit/s | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | MP3 64 kbit/s | R1 | D1- | 19/19 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| val+test | MP3 64 kbit/s | R1 | D2+ | 26/26 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 26/26 |
| val+test | MP3 64 kbit/s | R1 | D2- | 36/36 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | MP3 64 kbit/s | R1 | D3- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | MP3 64 kbit/s | R1 | D4- | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| val+test | MP3 64 kbit/s | R1 | D5- | 30/30 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 30/30 |
| val+test | MP3 64 kbit/s | R1 | D6- | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | MP3 64 kbit/s | R1 | D9- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| val+test | dynamic-range compression | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | dynamic-range compression | R1 | D1- | 17/19 | 0.895 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.6, 1] | 17/19 |
| val+test | dynamic-range compression | R1 | D2+ | 25/26 | 0.962 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.857, 1] | 25/26 |
| val+test | dynamic-range compression | R1 | D2- | 36/36 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | dynamic-range compression | R1 | D3- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | dynamic-range compression | R1 | D4- | 7/13 | 0.538 | per speaker: eisenhower_farewell_1961 0.333, lbush_radio_2001 1, mobama_weekly_2014 0.4, nixon_resignation_1974 0; range [0, 1] | 7/13 |
| val+test | dynamic-range compression | R1 | D5- | 6/30 | 0.2 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.286, mobama_weekly_2014 0.222, nixon_resignation_1974 0.2; range [0, 0.286] | 6/30 |
| val+test | dynamic-range compression | R1 | D6- | 7/8 | 0.875 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.5, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.5, 1] | 7/8 |
| val+test | dynamic-range compression | R1 | D9- | 3/4 | 0.75 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 1, nixon_resignation_1974 1; range [0.5, 1] | 3/4 |
| val+test | room reverb RT60 0.4 s | R1 | D1+ | 24/24 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | room reverb RT60 0.4 s | R1 | D1- | 54/57 | 0.947 | per speaker: eisenhower_farewell_1961 0.867, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0.933; range [0.867, 1] | 17/19 |
| val+test | room reverb RT60 0.4 s | R1 | D2+ | 75/78 | 0.962 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.857, 1] | 25/26 |
| val+test | room reverb RT60 0.4 s | R1 | D2- | 108/108 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | room reverb RT60 0.4 s | R1 | D3- | 20/21 | 0.952 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 0.833; range [0.833, 1] | 6/7 |
| val+test | room reverb RT60 0.4 s | R1 | D4- | 39/39 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| val+test | room reverb RT60 0.4 s | R1 | D5- | 89/90 | 0.989 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.952, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.952, 1] | 29/30 |
| val+test | room reverb RT60 0.4 s | R1 | D6- | 21/24 | 0.875 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.5, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.5, 1] | 7/8 |
| val+test | room reverb RT60 0.4 s | R1 | D9- | 9/12 | 0.75 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 1, nixon_resignation_1974 0.667; range [0.667, 1] | 2/4 |
| val+test | phone band + mu-law (participant only) | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | phone band + mu-law (participant only) | R1 | D1- | 18/19 | 0.947 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0.8; range [0.8, 1] | 18/19 |
| val+test | phone band + mu-law (participant only) | R1 | D2+ | 25/26 | 0.962 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.857, 1] | 25/26 |
| val+test | phone band + mu-law (participant only) | R1 | D2- | 35/36 | 0.972 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 0.889, nixon_resignation_1974 1; range [0.889, 1] | 35/36 |
| val+test | phone band + mu-law (participant only) | R1 | D3- | 5/7 | 0.714 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 0; range [0, 1] | 5/7 |
| val+test | phone band + mu-law (participant only) | R1 | D4- | 12/13 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0; range [0, 1] | 12/13 |
| val+test | phone band + mu-law (participant only) | R1 | D5- | 21/30 | 0.7 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 0.571, mobama_weekly_2014 0.556, nixon_resignation_1974 1; range [0.5, 1] | 21/30 |
| val+test | phone band + mu-law (participant only) | R1 | D6- | 5/8 | 0.625 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0, mobama_weekly_2014 0.5, nixon_resignation_1974 1; range [0, 1] | 5/8 |
| val+test | phone band + mu-law (participant only) | R1 | D9- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| val+test | WORLD speaker transform | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | WORLD speaker transform | R1 | D1- | 19/19 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| val+test | WORLD speaker transform | R1 | D2+ | 25/26 | 0.962 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.857, 1] | 25/26 |
| val+test | WORLD speaker transform | R1 | D2- | 36/36 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | WORLD speaker transform | R1 | D3- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | WORLD speaker transform | R1 | D4- | 12/13 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 0.8, nixon_resignation_1974 1; range [0.8, 1] | 12/13 |
| val+test | WORLD speaker transform | R1 | D5- | 30/30 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 30/30 |
| val+test | WORLD speaker transform | R1 | D6- | 7/8 | 0.875 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.5, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.5, 1] | 7/8 |
| val+test | WORLD speaker transform | R1 | D9- | 3/4 | 0.75 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 1, nixon_resignation_1974 1; range [0.5, 1] | 3/4 |
| val+test | babble 10 dB SNR | R1 | D1+ | 15/24 | 0.625 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 0.833, mobama_weekly_2014 0.5, nixon_resignation_1974 0.5; range [0.5, 0.833] | 3/8 |
| val+test | babble 10 dB SNR | R1 | D1- | 43/57 | 0.754 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 1, mobama_weekly_2014 0.8, nixon_resignation_1974 0.6; range [0.6, 1] | 14/19 |
| val+test | babble 10 dB SNR | R1 | D2+ | 9/78 | 0.115 | per speaker: eisenhower_farewell_1961 0.111, lbush_radio_2001 0.143, mobama_weekly_2014 0.167, nixon_resignation_1974 0.048; range [0.048, 0.167] | 0/26 |
| val+test | babble 10 dB SNR | R1 | D2- | 108/108 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | babble 10 dB SNR | R1 | D3- | 15/21 | 0.714 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.333, nixon_resignation_1974 0.667; range [0.333, 1] | 4/7 |
| val+test | babble 10 dB SNR | R1 | D4- | 33/39 | 0.846 | per speaker: eisenhower_farewell_1961 0.889, lbush_radio_2001 1, mobama_weekly_2014 0.733, nixon_resignation_1974 0.667; range [0.667, 1] | 9/13 |
| val+test | babble 10 dB SNR | R1 | D5- | 46/90 | 0.511 | per speaker: eisenhower_farewell_1961 0.583, lbush_radio_2001 0.429, mobama_weekly_2014 0.741, nixon_resignation_1974 0.333; range [0.333, 0.741] | 8/30 |
| val+test | babble 10 dB SNR | R1 | D6- | 4/24 | 0.167 | per speaker: eisenhower_farewell_1961 0.167, lbush_radio_2001 0, mobama_weekly_2014 0.5, nixon_resignation_1974 0; range [0, 0.5] | 1/8 |
| val+test | babble 10 dB SNR | R1 | D9- | 11/12 | 0.917 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.667, nixon_resignation_1974 1; range [0.667, 1] | 3/4 |
| val+test | babble 20 dB SNR | R1 | D1+ | 23/24 | 0.958 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0.833; range [0.833, 1] | 7/8 |
| val+test | babble 20 dB SNR | R1 | D1- | 48/57 | 0.842 | per speaker: eisenhower_farewell_1961 0.8, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0.6; range [0.6, 1] | 16/19 |
| val+test | babble 20 dB SNR | R1 | D2+ | 60/78 | 0.769 | per speaker: eisenhower_farewell_1961 0.889, lbush_radio_2001 0.952, mobama_weekly_2014 0.944, nixon_resignation_1974 0.333; range [0.333, 0.952] | 16/26 |
| val+test | babble 20 dB SNR | R1 | D2- | 106/108 | 0.982 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 0.926, nixon_resignation_1974 1; range [0.926, 1] | 35/36 |
| val+test | babble 20 dB SNR | R1 | D3- | 21/21 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | babble 20 dB SNR | R1 | D4- | 38/39 | 0.974 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0.667; range [0.667, 1] | 12/13 |
| val+test | babble 20 dB SNR | R1 | D5- | 72/90 | 0.8 | per speaker: eisenhower_farewell_1961 0.833, lbush_radio_2001 0.619, mobama_weekly_2014 0.889, nixon_resignation_1974 0.833; range [0.619, 0.889] | 20/30 |
| val+test | babble 20 dB SNR | R1 | D6- | 16/24 | 0.667 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 0, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0, 1] | 5/8 |
| val+test | babble 20 dB SNR | R1 | D9- | 10/12 | 0.833 | per speaker: eisenhower_farewell_1961 0.833, lbush_radio_2001 1, nixon_resignation_1974 0.667; range [0.667, 1] | 2/4 |

The result is the measured degradation; there is no pass rule. Rates and kept fractions pool every seed; the seeds of one recording are not independent trials, so each interval resamples participant recordings (a row with per-speaker values uses speakers as clusters). Babble, compression and phone-band conditions are not supported invariances. R2 flawed clips use the single-reference mode; the check readers (no injected flaw, so no retention) are measured with the single and the median-of-five references.

All transforms affect the participant only. Synthetic diffuse room RT60=0.4 s; babble uses four other dataset baseline speakers (ids below), seeded offsets, at 10/20 dB SNR. Phone: 300-3400 Hz, 8 kHz sampling, G.711 mu-law.

| clip | babble donor speakers |
|---|---|
| eisenhower_farewell_1961__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_amb>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_amb>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_amb>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_dl>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_dl>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_dl>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_fb>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_fb>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_fb>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_jn>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_jn>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_jn>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_pc>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_pc>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_pc>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_wt>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_wt>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_wt>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x10_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x1_L2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x2_L2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x3_L2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x4_L2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x5_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x6_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x7_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x8_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x9_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__x1_L2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__x2_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__x3_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__x4_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gwbush_911_2001__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__G1 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__G3 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__G5 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L1A | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L1B | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L1C | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L1D | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L2A | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L2B | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L2C | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L2D | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L3A | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L3B | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L3C | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L3D | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_CONTOUR | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_D1 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_D2 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_D4 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_D5 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_DISFLUENCY | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_ENDINGS | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__identity | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__single_L1A | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__single_L1B | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__single_L2A | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__single_L2B | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__single_L3A | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__single_L3B | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__G1 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__G3 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__G5 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L1A | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L1B | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L1C | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L1D | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L2A | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L2B | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L2C | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L2D | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L3A | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L3B | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L3C | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L3D | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_CONTOUR | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_D1 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_D2 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_D4 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_D5 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_ENDINGS | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__identity | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__single_L1A | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__single_L1B | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__single_L2A | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__single_L2B | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__single_L3A | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__single_L3B | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| lbush_radio_2001__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| obama_weekly_2009__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| reagan_farewell_1989__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |

Unperturbed identity-chain/null reference:

| clip | split | reference mode | minutes | flags | by key |
|---|---|---|---|---|---|
| eisenhower_farewell_1961__identity | val | single | 0.495 | 0 | [] |
| gwbush_911_2001__identity | train | single | 0.468 | 0 | [] |
| harris_uncsw_2021__identity | train | single | 0.518 | 0 | [] |
| hclinton_tomorrow_2010__identity | train | single | 0.39 | 0 | [] |
| lbush_radio_2001__identity | val | single | 0.494 | 0 | [] |
| mobama_weekly_2014__identity | test | single | 0.487 | 0 | [] |
| nixon_resignation_1974__identity | test | single | 0.495 | 0 | [] |
| obama_weekly_2009__identity | train | single | 0.357 | 0 | [] |
| reagan_farewell_1989__identity | train | single | 0.493 | 0 | [] |
| gettysburg_amb>gettysburg_dj | check readers | single | 0.382 | 0 | [] |
| gettysburg_amb>gettysburg_sa | check readers | single | 0.503 | 0 | [] |
| gettysburg_amb>gettysburg_tg | check readers | single | 0.408 | 0 | [] |
| gettysburg_dl>gettysburg_dj | check readers | single | 0.382 | 0 | [] |
| gettysburg_dl>gettysburg_sa | check readers | single | 0.503 | 1 | ['D3- whole clip'] |
| gettysburg_dl>gettysburg_tg | check readers | single | 0.408 | 0 | [] |
| gettysburg_fb>gettysburg_dj | check readers | single | 0.382 | 0 | [] |
| gettysburg_fb>gettysburg_sa | check readers | single | 0.503 | 0 | [] |
| gettysburg_fb>gettysburg_tg | check readers | single | 0.408 | 0 | [] |
| gettysburg_jn>gettysburg_dj | check readers | single | 0.382 | 0 | [] |
| gettysburg_jn>gettysburg_sa | check readers | single | 0.503 | 0 | [] |
| gettysburg_jn>gettysburg_tg | check readers | single | 0.408 | 0 | [] |
| gettysburg_pc>gettysburg_dj | check readers | single | 0.382 | 0 | [] |
| gettysburg_pc>gettysburg_sa | check readers | single | 0.503 | 1 | ['D3- whole clip'] |
| gettysburg_pc>gettysburg_tg | check readers | single | 0.408 | 0 | [] |
| gettysburg_wt>gettysburg_dj | check readers | single | 0.382 | 0 | [] |
| gettysburg_wt>gettysburg_sa | check readers | single | 0.503 | 0 | [] |
| gettysburg_wt>gettysburg_tg | check readers | single | 0.408 | 0 | [] |
| gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt>gettysburg_dj | check readers | consensus5 | 0.382 | 1 | ['D3- whole clip'] |
| gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb>gettysburg_sa | check readers | consensus5 | 0.503 | 1 | ['D3- whole clip'] |
| gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn>gettysburg_tg | check readers | consensus5 | 0.408 | 0 | [] |

## Chain A versus chain B

| speech | split | type | level | chain | words | TP | truths | false regions (one detection per change; same-change duplicates reported separately) | same-change duplicates | onset error (ms) | offset error (ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| lbush_radio_2001 | val | RUSH | 2 | A | [69, 75] | 1 | 1 | 0 | 1 | -150 | -14.1 |
| lbush_radio_2001 | val | RUSH | 2 | B | [69, 75] | 1 | 1 | 0 | 1 | -150 | -14 |
| eisenhower_farewell_1961 | val | RUSH | 2 | A | [40, 47] | 1 | 1 | 0 | 1 | 1140 | 6.6 |
| eisenhower_farewell_1961 | val | RUSH | 2 | B | [40, 47] | 1 | 1 | 0 | 1 | 20.1 | -213 |
| mobama_weekly_2014 | test | RUSH | 2 | A | [65, 71] | 1 | 1 | 0 | 1 | 270 | 10.7 |
| mobama_weekly_2014 | test | RUSH | 2 | B | [65, 71] | 1 | 1 | 0 | 1 | 250 | -9.1 |
| nixon_resignation_1974 | test | RUSH | 2 | A | [33, 40] | 1 | 1 | 0 | 1 | 30 | -17.9 |
| nixon_resignation_1974 | test | RUSH | 2 | B | [33, 40] | 1 | 1 | 0 | 1 | 30.1 | -17.4 |
| lbush_radio_2001 | val | RUSH | 3 | A | [69, 75] | 1 | 1 | 0 | 1 | -150 | 8.9 |
| lbush_radio_2001 | val | RUSH | 3 | B | [69, 75] | 1 | 1 | 0 | 1 | -150 | -10.8 |
| eisenhower_farewell_1961 | val | RUSH | 3 | A | [40, 47] | 1 | 1 | 0 | 1 | 1040 | 29.9 |
| eisenhower_farewell_1961 | val | RUSH | 3 | B | [40, 47] | 1 | 1 | 0 | 1 | 1040 | 11.2 |
| mobama_weekly_2014 | test | RUSH | 3 | A | [65, 71] | 1 | 1 | 0 | 1 | 210 | 17.4 |
| mobama_weekly_2014 | test | RUSH | 3 | B | [65, 71] | 1 | 1 | 0 | 1 | 190 | 17.6 |
| nixon_resignation_1974 | test | RUSH | 3 | A | [33, 40] | 1 | 1 | 0 | 1 | 10 | -11.6 |
| nixon_resignation_1974 | test | RUSH | 3 | B | [33, 40] | 1 | 1 | 0 | 1 | 10.2 | -90.9 |
| lbush_radio_2001 | val | DRAG | 2 | A | [2, 8] | 1 | 1 | 0 | 0 | 30 | -118 |
| lbush_radio_2001 | val | DRAG | 2 | B | [2, 8] | 1 | 1 | 0 | 0 | 49.7 | -98.3 |
| eisenhower_farewell_1961 | val | DRAG | 2 | A | [35, 40] | 1 | 1 | 0 | 0 | -130 | 816 |
| eisenhower_farewell_1961 | val | DRAG | 2 | B | [35, 40] | 1 | 1 | 0 | 0 | -130 | -45.3 |
| mobama_weekly_2014 | test | DRAG | 2 | A | [11, 18] | 1 | 1 | 0 | 0 | 40 | -104 |
| mobama_weekly_2014 | test | DRAG | 2 | B | [11, 18] | 1 | 1 | 0 | 0 | 39.8 | -84.7 |
| nixon_resignation_1974 | test | DRAG | 2 | A | [40, 47] | 1 | 1 | 0 | 0 | 70 | -125 |
| nixon_resignation_1974 | test | DRAG | 2 | B | [40, 47] | 1 | 1 | 0 | 0 | 89.8 | -106 |
| lbush_radio_2001 | val | DRAG | 3 | A | [2, 8] | 1 | 1 | 0 | 0 | 50 | -166 |
| lbush_radio_2001 | val | DRAG | 3 | B | [2, 8] | 1 | 1 | 0 | 0 | 69.6 | -146 |
| eisenhower_farewell_1961 | val | DRAG | 3 | A | [35, 40] | 1 | 1 | 0 | 0 | -130 | 823 |
| eisenhower_farewell_1961 | val | DRAG | 3 | B | [35, 40] | 1 | 1 | 0 | 0 | -130 | 819 |
| mobama_weekly_2014 | test | DRAG | 3 | A | [11, 18] | 1 | 1 | 0 | 0 | 40 | -139 |
| mobama_weekly_2014 | test | DRAG | 3 | B | [11, 18] | 1 | 1 | 0 | 0 | 59.6 | -119 |
| nixon_resignation_1974 | test | DRAG | 3 | A | [40, 47] | 1 | 1 | 0 | 0 | 90 | -190 |
| nixon_resignation_1974 | test | DRAG | 3 | B | [40, 47] | 1 | 1 | 0 | 0 | 110 | -151 |
| lbush_radio_2001 | val | MONOTONE | 2 | A | [46, 51] | 1 | 1 | 0 | 0 | 240 | -390 |
| lbush_radio_2001 | val | MONOTONE | 2 | B | [46, 51] | 1 | 1 | 0 | 0 | 420 | -370 |
| eisenhower_farewell_1961 | val | MONOTONE | 2 | A | [44, 51] | 1 | 1 | 0 | 0 | 50 | -120 |
| eisenhower_farewell_1961 | val | MONOTONE | 2 | B | [44, 51] | 1 | 1 | 0 | 0 | 1250 | -20 |
| mobama_weekly_2014 | test | MONOTONE | 2 | A | [42, 46] | 0 | 1 | 1 | 0 |  |  |
| mobama_weekly_2014 | test | MONOTONE | 2 | B | [42, 46] | 0 | 1 | 1 | 0 |  |  |
| nixon_resignation_1974 | test | MONOTONE | 2 | A | [49, 54] | 1 | 1 | 0 | 0 | 50 | -310 |
| nixon_resignation_1974 | test | MONOTONE | 2 | B | [49, 54] | 1 | 1 | 0 | 0 | 70 | -430 |
| lbush_radio_2001 | val | MONOTONE | 3 | A | [46, 51] | 1 | 1 | 0 | 0 | 40 | -370 |
| lbush_radio_2001 | val | MONOTONE | 3 | B | [46, 51] | 1 | 1 | 0 | 0 | 240 | -370 |
| eisenhower_farewell_1961 | val | MONOTONE | 3 | A | [44, 51] | 1 | 1 | 0 | 0 | 330 | -120 |
| eisenhower_farewell_1961 | val | MONOTONE | 3 | B | [44, 51] | 1 | 1 | 0 | 0 | 1250 | 80 |
| mobama_weekly_2014 | test | MONOTONE | 3 | A | [42, 46] | 0 | 1 | 1 | 0 |  |  |
| mobama_weekly_2014 | test | MONOTONE | 3 | B | [42, 46] | 0 | 1 | 1 | 0 |  |  |
| nixon_resignation_1974 | test | MONOTONE | 3 | A | [49, 54] | 1 | 1 | 0 | 0 | 50 | -310 |
| nixon_resignation_1974 | test | MONOTONE | 3 | B | [49, 54] | 1 | 1 | 0 | 0 | 70 | -310 |

## Directional test: a higher level never raises the dimension score

| speech | split | type | L1 | L2 | L3 | cause |
|---|---|---|---|---|---|---|
| eisenhower_farewell_1961 | val | BLOCK |  |  |  |  |
| eisenhower_farewell_1961 | val | DEEMPHASIS | 100 | 100 | 96.6 |  |
| eisenhower_farewell_1961 | val | DRAG | 100 | 74.6 | 24.8 |  |
| eisenhower_farewell_1961 | val | FADE | 100 | 93.4 | 64.5 |  |
| eisenhower_farewell_1961 | val | FLAT_FINAL_FALL |  |  |  |  |
| eisenhower_farewell_1961 | val | HESITATION | 100 | 91 | 64.2 |  |
| eisenhower_farewell_1961 | val | LOW_EFFORT | 100 | 97.7 | 84 |  |
| eisenhower_farewell_1961 | val | MISPLACED_EMPHASIS | 100 | 100 | 100 |  |
| eisenhower_farewell_1961 | val | MONOTONE | 100 | 90.8 | 63.7 |  |
| eisenhower_farewell_1961 | val | MUMBLE | 100 | 91.4 | 84.4 |  |
| eisenhower_farewell_1961 | val | NATURAL_RUSH | 100 | 100 | 99.4 |  |
| eisenhower_farewell_1961 | val | ONSET_PROLONGATION |  |  |  |  |
| eisenhower_farewell_1961 | val | PAUSE_DROPPED | 63.6 | 63.6 | 63.6 |  |
| eisenhower_farewell_1961 | val | PAUSE_INTRUSIVE | 99.1 | 85.6 | 63.6 |  |
| eisenhower_farewell_1961 | val | REPEATED_CONTOUR |  |  |  | no detector |
| eisenhower_farewell_1961 | val | RHYME_PROLONGATION |  |  |  |  |
| eisenhower_farewell_1961 | val | RISING_ENDING |  |  |  |  |
| eisenhower_farewell_1961 | val | RUSH | 100 | 85.7 | 59.7 |  |
| eisenhower_farewell_1961 | val | SOUND_REPETITION |  |  |  |  |
| eisenhower_farewell_1961 | val | TRAILING_OFF | 100 | 100 | 100 |  |
| eisenhower_farewell_1961 | val | UNEVEN_TEMPO |  |  |  |  |
| eisenhower_farewell_1961 | val | WORD_BY_WORD | 100 | 100 | 100 |  |
| eisenhower_farewell_1961 | val | WORD_REPETITION |  |  |  |  |
| gwbush_911_2001 | train | BLOCK |  |  |  |  |
| gwbush_911_2001 | train | DEEMPHASIS | 100 | 100 | 0 |  |
| gwbush_911_2001 | train | DRAG | 100 | 90.8 | 69.9 |  |
| gwbush_911_2001 | train | FADE | 100 | 93.6 | 65.4 |  |
| gwbush_911_2001 | train | FLAT_FINAL_FALL |  |  |  |  |
| gwbush_911_2001 | train | HESITATION | 100 | 89.2 | 57 |  |
| gwbush_911_2001 | train | LOW_EFFORT | 100 | 96 | 80.9 |  |
| gwbush_911_2001 | train | MISPLACED_EMPHASIS | 100 | 100 | 100 |  |
| gwbush_911_2001 | train | MONOTONE | 100 | 90.5 | 74.7 |  |
| gwbush_911_2001 | train | MUMBLE | 100 | 75.7 | 67.2 |  |
| gwbush_911_2001 | train | NATURAL_RUSH | 100 | 100 | 100 |  |
| gwbush_911_2001 | train | ONSET_PROLONGATION |  |  |  |  |
| gwbush_911_2001 | train | PAUSE_DROPPED | 87.3 | 76.3 | 69.2 |  |
| gwbush_911_2001 | train | PAUSE_INTRUSIVE | 98.2 | 82.1 | 56.4 |  |
| gwbush_911_2001 | train | REPEATED_CONTOUR |  |  |  | no detector |
| gwbush_911_2001 | train | RHYME_PROLONGATION |  |  |  |  |
| gwbush_911_2001 | train | RISING_ENDING |  |  |  |  |
| gwbush_911_2001 | train | RUSH | 100 | 90.1 | 63.1 |  |
| gwbush_911_2001 | train | SOUND_REPETITION |  |  |  |  |
| gwbush_911_2001 | train | TRAILING_OFF | 100 | 100 | 97.2 |  |
| gwbush_911_2001 | train | UNEVEN_TEMPO |  |  |  |  |
| gwbush_911_2001 | train | WORD_BY_WORD | 100 | 100 | 100 |  |
| gwbush_911_2001 | train | WORD_REPETITION |  |  |  |  |
| harris_uncsw_2021 | train | BLOCK |  |  |  |  |
| harris_uncsw_2021 | train | DEEMPHASIS | 100 | 100 | 98.9 |  |
| harris_uncsw_2021 | train | DRAG | 100 | 87 | 54.7 |  |
| harris_uncsw_2021 | train | FADE | 100 | 86.3 | 60.8 |  |
| harris_uncsw_2021 | train | FLAT_FINAL_FALL |  |  |  |  |
| harris_uncsw_2021 | train | HESITATION | 100 | 91.8 | 100 | penalty charged to the change's linked dimension or whole-clip flag (one change, one penalty) |
| harris_uncsw_2021 | train | LOW_EFFORT | 100 | 99.5 | 93.6 |  |
| harris_uncsw_2021 | train | MISPLACED_EMPHASIS | 100 | 100 | 100 |  |
| harris_uncsw_2021 | train | MONOTONE | 100 | 88.3 | 69.1 |  |
| harris_uncsw_2021 | train | MUMBLE | 100 | 76.8 | 65.5 |  |
| harris_uncsw_2021 | train | NATURAL_RUSH | 100 | 100 | 99.6 |  |
| harris_uncsw_2021 | train | ONSET_PROLONGATION |  |  |  |  |
| harris_uncsw_2021 | train | PAUSE_DROPPED | 100 | 96.4 | 94.6 |  |
| harris_uncsw_2021 | train | PAUSE_INTRUSIVE | 98.3 | 87.2 | 68.8 |  |
| harris_uncsw_2021 | train | REPEATED_CONTOUR |  |  |  | no detector |
| harris_uncsw_2021 | train | RHYME_PROLONGATION |  |  |  |  |
| harris_uncsw_2021 | train | RISING_ENDING |  |  |  |  |
| harris_uncsw_2021 | train | RUSH | 100 | 90.3 | 70.4 |  |
| harris_uncsw_2021 | train | SOUND_REPETITION |  |  |  |  |
| harris_uncsw_2021 | train | TRAILING_OFF | 100 | 100 | 99 |  |
| harris_uncsw_2021 | train | UNEVEN_TEMPO |  |  |  |  |
| harris_uncsw_2021 | train | WORD_BY_WORD | 100 | 100 | 100 |  |
| harris_uncsw_2021 | train | WORD_REPETITION |  |  |  |  |
| hclinton_tomorrow_2010 | train | BLOCK |  |  |  |  |
| hclinton_tomorrow_2010 | train | DEEMPHASIS | 100 | 100 | 82.2 |  |
| hclinton_tomorrow_2010 | train | DRAG | 100 | 75.8 | 18.9 |  |
| hclinton_tomorrow_2010 | train | FADE | 100 | 87 | 77.6 |  |
| hclinton_tomorrow_2010 | train | FLAT_FINAL_FALL |  |  |  |  |
| hclinton_tomorrow_2010 | train | HESITATION | 100 | 85.7 | 45.5 |  |
| hclinton_tomorrow_2010 | train | LOW_EFFORT | 100 | 91.6 | 67.6 |  |
| hclinton_tomorrow_2010 | train | MISPLACED_EMPHASIS | 100 | 100 | 100 |  |
| hclinton_tomorrow_2010 | train | MONOTONE | 100 | 86 | 48.9 |  |
| hclinton_tomorrow_2010 | train | MUMBLE | 100 | 81.5 | 69.2 |  |
| hclinton_tomorrow_2010 | train | NATURAL_RUSH | 100 | 100 | 96.4 |  |
| hclinton_tomorrow_2010 | train | ONSET_PROLONGATION |  |  |  |  |
| hclinton_tomorrow_2010 | train | PAUSE_DROPPED | 76.9 | 60 | 48.7 |  |
| hclinton_tomorrow_2010 | train | PAUSE_INTRUSIVE | 97 | 76.9 | 45.5 |  |
| hclinton_tomorrow_2010 | train | REPEATED_CONTOUR |  |  |  | no detector |
| hclinton_tomorrow_2010 | train | RHYME_PROLONGATION |  |  |  |  |
| hclinton_tomorrow_2010 | train | RISING_ENDING |  |  |  |  |
| hclinton_tomorrow_2010 | train | RUSH | 100 | 81.8 | 48.8 |  |
| hclinton_tomorrow_2010 | train | SOUND_REPETITION |  |  |  |  |
| hclinton_tomorrow_2010 | train | TRAILING_OFF | 100 | 100 | 100 |  |
| hclinton_tomorrow_2010 | train | UNEVEN_TEMPO |  |  |  |  |
| hclinton_tomorrow_2010 | train | WORD_BY_WORD | 100 | 100 | 100 |  |
| hclinton_tomorrow_2010 | train | WORD_REPETITION |  |  |  |  |
| lbush_radio_2001 | val | DEEMPHASIS | 100 | 100 | 100 |  |
| lbush_radio_2001 | val | DRAG | 100 | 90.5 | 72.9 |  |
| lbush_radio_2001 | val | FADE | 100 | 99.9 | 81.3 |  |
| lbush_radio_2001 | val | FLAT_FINAL_FALL |  |  |  |  |
| lbush_radio_2001 | val | HESITATION | 100 | 84.6 | 38.6 |  |
| lbush_radio_2001 | val | LOW_EFFORT | 100 | 93.3 | 79.4 |  |
| lbush_radio_2001 | val | MISPLACED_EMPHASIS | 100 | 100 | 100 |  |
| lbush_radio_2001 | val | MONOTONE | 100 | 91.1 | 71 |  |
| lbush_radio_2001 | val | MUMBLE | 100 | 94.3 | 91.5 |  |
| lbush_radio_2001 | val | NATURAL_RUSH | 100 | 100 | 99.5 |  |
| lbush_radio_2001 | val | ONSET_PROLONGATION |  |  |  |  |
| lbush_radio_2001 | val | PAUSE_DROPPED | 97.5 | 86.4 | 80.9 |  |
| lbush_radio_2001 | val | PAUSE_INTRUSIVE | 99.3 | 76.3 | 37.7 |  |
| lbush_radio_2001 | val | REPEATED_CONTOUR |  |  |  | no detector |
| lbush_radio_2001 | val | RHYME_PROLONGATION |  |  |  |  |
| lbush_radio_2001 | val | RISING_ENDING |  |  |  |  |
| lbush_radio_2001 | val | RUSH | 100 | 79.8 | 42.7 |  |
| lbush_radio_2001 | val | SOUND_REPETITION |  |  |  |  |
| lbush_radio_2001 | val | TRAILING_OFF | 100 | 100 | 99.5 |  |
| lbush_radio_2001 | val | UNEVEN_TEMPO |  |  |  |  |
| lbush_radio_2001 | val | WORD_BY_WORD | 100 | 100 | 100 |  |
| lbush_radio_2001 | val | WORD_REPETITION |  |  |  |  |
| mobama_weekly_2014 | test | BLOCK |  |  |  |  |
| mobama_weekly_2014 | test | DEEMPHASIS | 100 | 89.9 | 61.2 |  |
| mobama_weekly_2014 | test | DRAG | 100 | 82.3 | 48.9 |  |
| mobama_weekly_2014 | test | FADE | 100 | 94.6 | 79.7 |  |
| mobama_weekly_2014 | test | FLAT_FINAL_FALL |  |  |  |  |
| mobama_weekly_2014 | test | HESITATION | 100 | 84.9 | 100 | penalty charged to the change's linked dimension or whole-clip flag (one change, one penalty) |
| mobama_weekly_2014 | test | LOW_EFFORT | 100 | 98 | 91.7 |  |
| mobama_weekly_2014 | test | MISPLACED_EMPHASIS | 100 | 100 | 100 |  |
| mobama_weekly_2014 | test | MONOTONE | 100 | 91.3 | 80.5 |  |
| mobama_weekly_2014 | test | MUMBLE | 100 | 91.4 | 84.7 |  |
| mobama_weekly_2014 | test | NATURAL_RUSH | 100 | 100 | 100 |  |
| mobama_weekly_2014 | test | ONSET_PROLONGATION |  |  |  |  |
| mobama_weekly_2014 | test | PAUSE_DROPPED | 76.1 | 60 | 48.7 |  |
| mobama_weekly_2014 | test | PAUSE_INTRUSIVE | 97 | 76.9 | 45.5 |  |
| mobama_weekly_2014 | test | REPEATED_CONTOUR |  |  |  | no detector |
| mobama_weekly_2014 | test | RHYME_PROLONGATION |  |  |  |  |
| mobama_weekly_2014 | test | RISING_ENDING |  |  |  |  |
| mobama_weekly_2014 | test | RUSH | 100 | 91.3 | 72.2 |  |
| mobama_weekly_2014 | test | SOUND_REPETITION |  |  |  |  |
| mobama_weekly_2014 | test | TRAILING_OFF | 100 | 100 | 97.3 |  |
| mobama_weekly_2014 | test | UNEVEN_TEMPO |  |  |  |  |
| mobama_weekly_2014 | test | WORD_BY_WORD | 100 | 100 | 100 |  |
| mobama_weekly_2014 | test | WORD_REPETITION |  |  |  |  |
| nixon_resignation_1974 | test | BLOCK |  |  |  |  |
| nixon_resignation_1974 | test | DEEMPHASIS | 100 | 100 | 100 |  |
| nixon_resignation_1974 | test | DRAG | 100 | 75.7 | 26.4 |  |
| nixon_resignation_1974 | test | FADE | 100 | 92.1 | 69.6 |  |
| nixon_resignation_1974 | test | FLAT_FINAL_FALL |  |  |  |  |
| nixon_resignation_1974 | test | HESITATION | 100 | 82.8 | 37.7 |  |
| nixon_resignation_1974 | test | LOW_EFFORT | 100 | 95.7 | 79.5 |  |
| nixon_resignation_1974 | test | MISPLACED_EMPHASIS | 100 | 100 | 100 |  |
| nixon_resignation_1974 | test | MONOTONE | 100 | 97.5 | 91.4 |  |
| nixon_resignation_1974 | test | MUMBLE | 100 | 95.5 | 91.5 |  |
| nixon_resignation_1974 | test | NATURAL_RUSH | 100 | 100 | 100 |  |
| nixon_resignation_1974 | test | ONSET_PROLONGATION |  |  |  |  |
| nixon_resignation_1974 | test | PAUSE_DROPPED | 90.1 | 77.2 | 69.9 |  |
| nixon_resignation_1974 | test | PAUSE_INTRUSIVE | 96.6 | 73.6 | 37.7 |  |
| nixon_resignation_1974 | test | REPEATED_CONTOUR |  |  |  | no detector |
| nixon_resignation_1974 | test | RHYME_PROLONGATION |  |  |  |  |
| nixon_resignation_1974 | test | RISING_ENDING |  |  |  |  |
| nixon_resignation_1974 | test | RUSH | 100 | 70.6 | 23.7 |  |
| nixon_resignation_1974 | test | SOUND_REPETITION |  |  |  |  |
| nixon_resignation_1974 | test | TRAILING_OFF | 100 | 100 | 96.8 |  |
| nixon_resignation_1974 | test | UNEVEN_TEMPO |  |  |  |  |
| nixon_resignation_1974 | test | WORD_BY_WORD | 100 | 100 | 98.4 |  |
| nixon_resignation_1974 | test | WORD_REPETITION |  |  |  |  |
| obama_weekly_2009 | train | BLOCK |  |  |  |  |
| obama_weekly_2009 | train | DEEMPHASIS | 100 | 100 | 100 |  |
| obama_weekly_2009 | train | DRAG | 100 | 78.1 | 25.3 |  |
| obama_weekly_2009 | train | FADE | 100 | 90.1 | 51.5 |  |
| obama_weekly_2009 | train | FLAT_FINAL_FALL |  |  |  |  |
| obama_weekly_2009 | train | HESITATION | 100 | 89.2 | 57 |  |
| obama_weekly_2009 | train | LOW_EFFORT | 100 | 99.4 | 86.8 |  |
| obama_weekly_2009 | train | MISPLACED_EMPHASIS | 100 | 100 | 100 |  |
| obama_weekly_2009 | train | MONOTONE | 100 | 100 | 88.5 |  |
| obama_weekly_2009 | train | MUMBLE | 100 | 90.2 | 83 |  |
| obama_weekly_2009 | train | NATURAL_RUSH | 100 | 100 | 99.7 |  |
| obama_weekly_2009 | train | ONSET_PROLONGATION |  |  |  |  |
| obama_weekly_2009 | train | PAUSE_DROPPED | 80.8 | 68 | 58.3 |  |
| obama_weekly_2009 | train | PAUSE_INTRUSIVE | 98.9 | 100 | 56.4 | pause not measured at the labelled boundary |
| obama_weekly_2009 | train | REPEATED_CONTOUR |  |  |  | no detector |
| obama_weekly_2009 | train | RHYME_PROLONGATION |  |  |  |  |
| obama_weekly_2009 | train | RISING_ENDING |  |  |  |  |
| obama_weekly_2009 | train | RUSH | 100 | 89.7 | 69.9 |  |
| obama_weekly_2009 | train | SOUND_REPETITION |  |  |  |  |
| obama_weekly_2009 | train | TRAILING_OFF | 100 | 100 | 87.9 |  |
| obama_weekly_2009 | train | UNEVEN_TEMPO |  |  |  |  |
| obama_weekly_2009 | train | WORD_BY_WORD | 100 | 100 | 100 |  |
| obama_weekly_2009 | train | WORD_REPETITION |  |  |  |  |
| reagan_farewell_1989 | train | DEEMPHASIS | 100 | 100 | 100 |  |
| reagan_farewell_1989 | train | DRAG | 100 | 86.7 | 55.9 |  |
| reagan_farewell_1989 | train | FADE | 100 | 95.7 | 79.9 |  |
| reagan_farewell_1989 | train | FLAT_FINAL_FALL |  |  |  |  |
| reagan_farewell_1989 | train | HESITATION | 100 | 89.2 | 100 | pause not measured at the labelled boundary |
| reagan_farewell_1989 | train | LOW_EFFORT | 100 | 98.3 | 93.2 |  |
| reagan_farewell_1989 | train | MISPLACED_EMPHASIS | 100 | 100 | 98.5 |  |
| reagan_farewell_1989 | train | MONOTONE | 100 | 98.1 | 92.3 |  |
| reagan_farewell_1989 | train | MUMBLE | 100 | 79.3 | 69.7 |  |
| reagan_farewell_1989 | train | NATURAL_RUSH | 100 | 99.8 | 99.9 | measured change not monotone across levels |
| reagan_farewell_1989 | train | ONSET_PROLONGATION |  |  |  |  |
| reagan_farewell_1989 | train | PAUSE_DROPPED | 81.5 | 68.6 | 59.6 |  |
| reagan_farewell_1989 | train | PAUSE_INTRUSIVE | 98.9 | 82.8 | 56.4 |  |
| reagan_farewell_1989 | train | REPEATED_CONTOUR |  |  |  | no detector |
| reagan_farewell_1989 | train | RHYME_PROLONGATION |  |  |  |  |
| reagan_farewell_1989 | train | RISING_ENDING |  |  |  |  |
| reagan_farewell_1989 | train | RUSH | 100 | 89 | 71.1 |  |
| reagan_farewell_1989 | train | SOUND_REPETITION |  |  |  |  |
| reagan_farewell_1989 | train | TRAILING_OFF | 100 | 100 | 100 |  |
| reagan_farewell_1989 | train | UNEVEN_TEMPO |  |  |  |  |
| reagan_farewell_1989 | train | WORD_BY_WORD | 100 | 100 | 100 |  |
| reagan_farewell_1989 | train | WORD_REPETITION |  |  |  |  |

## Repair test (inverse edit vs placebo)

| split | type | flags tested | removed by repair | kept after placebo |
|---|---|---|---|---|
| val | RUSH | 2 | 2 | 2 |
| val | DRAG | 2 | 2 | 2 |
| val | PAUSE_DROPPED | 2 | 2 | 2 |
| val | PAUSE_INTRUSIVE | 2 | 2 | 2 |
| val | FADE | 2 | 2 | 2 |
| val | MONOTONE | 2 | 2 | 2 |
| test | RUSH | 1 | 1 | 1 |
| test | DRAG | 2 | 2 | 2 |
| test | PAUSE_DROPPED | 2 | 2 | 2 |
| test | PAUSE_INTRUSIVE | 2 | 2 | 2 |
| test | FADE | 2 | 2 | 2 |
| test | MONOTONE | 1 | 1 | 1 |
| val+test | RUSH | 3 | 3 | 3 |
| val+test | DRAG | 4 | 4 | 4 |
| val+test | PAUSE_DROPPED | 4 | 4 | 4 |
| val+test | PAUSE_INTRUSIVE | 4 | 4 | 4 |
| val+test | FADE | 4 | 4 | 4 |
| val+test | MONOTONE | 3 | 3 | 3 |

| clip | split | type | placebo | flag removed (word index) | score before | score after | new flags | error |
|---|---|---|---|---|---|---|---|---|
| eisenhower_farewell_1961__single_L2A | val | RUSH | False | True | 94.3 | 95.7 | [] |  |
| eisenhower_farewell_1961__single_L2A | val | RUSH | True | False | 94.3 | 94.3 | [] |  |
| eisenhower_farewell_1961__single_L2A | val | PAUSE_DROPPED | False | True | 94.3 | 95.8 | [] |  |
| eisenhower_farewell_1961__single_L2A | val | PAUSE_DROPPED | True | False | 94.3 | 94.3 | [] |  |
| eisenhower_farewell_1961__single_L2A | val | MONOTONE | False | True | 94.3 | 96.5 | [] |  |
| eisenhower_farewell_1961__single_L2A | val | MONOTONE | True | False | 94.3 | 94.3 | [] |  |
| eisenhower_farewell_1961__single_L2B | val | PAUSE_INTRUSIVE | False | True | 92.1 | 94.5 | [] |  |
| eisenhower_farewell_1961__single_L2B | val | PAUSE_INTRUSIVE | True | False | 92.1 | 92.1 | [] |  |
| eisenhower_farewell_1961__single_L2B | val | DRAG | False | True | 92.1 | 94.7 | [] |  |
| eisenhower_farewell_1961__single_L2B | val | DRAG | True | False | 92.1 | 92.1 | [] |  |
| lbush_radio_2001__single_L2A | val | RUSH | False | True | 90.9 | 92.8 | [] |  |
| lbush_radio_2001__single_L2A | val | RUSH | True | False | 90.9 | 90.9 | [] |  |
| lbush_radio_2001__single_L2A | val | PAUSE_DROPPED | False | True | 90.9 | 95.7 | [] |  |
| lbush_radio_2001__single_L2A | val | PAUSE_DROPPED | True | False | 90.9 | 90.9 | [] |  |
| lbush_radio_2001__single_L2A | val | MONOTONE | False | True | 90.9 | 92.4 | [] |  |
| lbush_radio_2001__single_L2A | val | MONOTONE | True | False | 90.9 | 91.3 | [] |  |
| lbush_radio_2001__single_L2B | val | PAUSE_INTRUSIVE | False | True | 94.9 | 98.5 | [] |  |
| lbush_radio_2001__single_L2B | val | PAUSE_INTRUSIVE | True | False | 94.9 | 94.9 | [] |  |
| lbush_radio_2001__single_L2B | val | DRAG | False | True | 94.9 | 95.3 | [] |  |
| lbush_radio_2001__single_L2B | val | DRAG | True | False | 94.9 | 94.9 | [] |  |
| mobama_weekly_2014__single_L2A | test | RUSH | False | True | 96 | 97 | [] |  |
| mobama_weekly_2014__single_L2A | test | RUSH | True | False | 96 | 96 | [] |  |
| mobama_weekly_2014__single_L2A | test | FADE | False | True | 96 | 97.3 | [] |  |
| mobama_weekly_2014__single_L2A | test | FADE | True | False | 96 | 96 | [] |  |
| mobama_weekly_2014__single_L2A | test | PAUSE_DROPPED | False | True | 96 | 97.2 | [] |  |
| mobama_weekly_2014__single_L2A | test | PAUSE_DROPPED | True | False | 96 | 96 | [] |  |
| mobama_weekly_2014__single_L2B | test | PAUSE_INTRUSIVE | False | True | 95.4 | 94.1 | [] |  |
| mobama_weekly_2014__single_L2B | test | PAUSE_INTRUSIVE | True | False | 95.4 | 95.4 | [] |  |
| mobama_weekly_2014__single_L2B | test | DRAG | False | True | 95.4 | 93.1 | [] |  |
| mobama_weekly_2014__single_L2B | test | DRAG | True | False | 95.4 | 95.4 | [] |  |
| nixon_resignation_1974__single_L2A | test | FADE | False | True | 93.9 | 95.7 | [] |  |
| nixon_resignation_1974__single_L2A | test | FADE | True | False | 93.9 | 93.9 | [] |  |
| nixon_resignation_1974__single_L2A | test | PAUSE_DROPPED | False | True | 93.9 | 97.1 | [] |  |
| nixon_resignation_1974__single_L2A | test | PAUSE_DROPPED | True | False | 93.9 | 93.9 | [] |  |
| nixon_resignation_1974__single_L2A | test | MONOTONE | False | True | 93.9 | 94.7 | [] |  |
| nixon_resignation_1974__single_L2A | test | MONOTONE | True | False | 93.9 | 93.8 | [] |  |
| nixon_resignation_1974__single_L2B | test | PAUSE_INTRUSIVE | False | True | 92 | 95.5 | [] |  |
| nixon_resignation_1974__single_L2B | test | PAUSE_INTRUSIVE | True | False | 92 | 92 | [] |  |
| nixon_resignation_1974__single_L2B | test | DRAG | False | True | 92 | 94.6 | [] |  |
| nixon_resignation_1974__single_L2B | test | DRAG | True | False | 92 | 92 | [] |  |
| eisenhower_farewell_1961__single_L3A | val | FADE | False | True | 78.9 | 86.2 | ['D9-'] |  |
| eisenhower_farewell_1961__single_L3A | val | FADE | True | False | 78.9 | 78.9 | [] |  |
| lbush_radio_2001__single_L3A | val | FADE | False | True | 77.2 | 79.6 | [] |  |
| lbush_radio_2001__single_L3A | val | FADE | True | False | 77.2 | 77.2 | [] |  |

## Feature internal consistency

| split | type | level | n | recipe setting | realised measure | realised (recipe metric units) | detector measurement (dimension units; window centres inside the span) | median of paired ratios (independent measures only) |
|---|---|---|---|---|---|---|---|---|
| train | RUSH | 1 | 5 | 1.2 | independent | -0.182 | -0.139 | 0.761 |
| train | RUSH | 2 | 5 | 1.45 | independent | -0.372 | -0.258 | 0.697 |
| train | RUSH | 3 | 5 | 1.9 | independent | -0.634 | -0.52 | 0.823 |
| train | DRAG | 1 | 5 | 1.2 | independent | 0.176 | 0.143 | 0.816 |
| train | DRAG | 2 | 5 | 1.45 | independent | 0.359 | 0.309 | 0.862 |
| train | DRAG | 3 | 5 | 1.9 | independent | 0.632 | 0.57 | 0.952 |
| train | PAUSE_DROPPED | 1 | 5 | 0.4 | independent | -0.51 | -0.51 | 1 |
| train | PAUSE_DROPPED | 2 | 5 | 0.2 | independent | -0.54 | -0.54 | 1 |
| train | PAUSE_DROPPED | 3 | 5 | 0 | independent | -0.71 | -0.71 | 1 |
| train | PAUSE_INTRUSIVE | 1 | 5 | 0.35 | independent | 0.35 | 0.35 | 1 |
| train | PAUSE_INTRUSIVE | 2 | 5 | 0.6 | independent | 0.59 | 0.59 | 1 |
| train | PAUSE_INTRUSIVE | 3 | 5 | 1.2 | independent | 1.19 | 1.19 | 1 |
| train | MONOTONE | 1 | 5 | 0.5 | independent | -0.582 | -0.352 | 0.713 |
| train | MONOTONE | 2 | 5 | 0.25 | independent | -0.941 | -0.777 | 0.856 |
| train | MONOTONE | 3 | 5 | 0 | independent | -1.7 | -0.906 | 0.534 |
| train | DEEMPHASIS | 1 | 5 | 0.5 | independent | -0.774 | -0.774 | 1 |
| train | DEEMPHASIS | 2 | 5 | 0.75 | independent | -1.14 | -1.14 | 1 |
| train | DEEMPHASIS | 3 | 5 | 1 | independent | -1.2 | -1.2 | 1 |
| train | FADE | 1 | 5 | 4 | independent | -2.81 | -2.84 | 1.01 |
| train | FADE | 2 | 5 | 8 | independent | -5.68 | -5.15 | 0.933 |
| train | FADE | 3 | 5 | 14 | independent | -9.41 | -8.4 | 0.96 |
| train | MUMBLE | 1 | 5 | 0.3 | independent | -0.347 | -0.305 | 0.854 |
| train | MUMBLE | 2 | 5 | 0.6 | independent | -0.737 | -0.514 | 0.697 |
| train | MUMBLE | 3 | 5 | 1 | independent | -0.896 | -0.64 | 0.765 |
| train | NATURAL_RUSH | 1 | 5 | {'speech_rate': 1.13, 'pause_kept_fraction': 0.6} | independent | -0.122 | -0.0572 | 0.468 |
| train | NATURAL_RUSH | 2 | 5 | {'speech_rate': 1.15, 'pause_kept_fraction': 0.3} | independent | -0.14 | -0.0802 | 0.574 |
| train | NATURAL_RUSH | 3 | 5 | {'speech_rate': 1.18, 'pause_kept_fraction': 0.0} | independent | -0.165 | -0.0953 | 0.576 |
| train | HESITATION | 1 | 4 | {'word_duration_factor': 1.2, 'silence_s': 0.2} | circular (detector measure) | 0.205 | 0.205 |  |
| train | HESITATION | 2 | 5 | {'word_duration_factor': 1.5, 'silence_s': 0.5} | circular (detector measure) | 0.5 | 0.5 |  |
| train | HESITATION | 3 | 5 | {'word_duration_factor': 1.8, 'silence_s': 1.0} | circular (detector measure) | 1 | 1 |  |
| train | WORD_BY_WORD | 1 | 0 | {'silence_s': 0.15, 'every_words': 1} | circular (detector measure) |  |  |  |
| train | WORD_BY_WORD | 2 | 5 | {'silence_s': 0.225, 'every_words': 1} | circular (detector measure) | 0.22 | 0.22 |  |
| train | WORD_BY_WORD | 3 | 5 | {'silence_s': 0.3, 'every_words': 1} | circular (detector measure) | 0.29 | 0.29 |  |
| train | UNEVEN_TEMPO | 1 | 5 | {'max_duration_deviation': 0.15} | circular (detector measure) | 0 | 0 |  |
| train | UNEVEN_TEMPO | 2 | 5 | {'max_duration_deviation': 0.3} | circular (detector measure) | 0 | 0 |  |
| train | UNEVEN_TEMPO | 3 | 5 | {'max_duration_deviation': 0.45} | circular (detector measure) | 0 | 0 |  |
| train | WORD_REPETITION | 1 | 4 | {'first_token_duration_factor': 1.3, 'silence_s': 0.1, 'inserted_copies': 1} | circular (detector measure) | 0.0771 | 0.0771 |  |
| train | WORD_REPETITION | 2 | 4 | {'first_token_duration_factor': 1.6, 'silence_s': 0.225, 'inserted_copies': 1} | circular (detector measure) | 0.168 | 0.168 |  |
| train | WORD_REPETITION | 3 | 4 | {'first_token_duration_factor': 1.9, 'silence_s': 0.35, 'inserted_copies': 1} | circular (detector measure) | 0 | 0 |  |
| train | SOUND_REPETITION | 1 | 5 | {'inserted_copies': 2, 'silence_s': 0.1} | circular (detector measure) | 0 | 0 |  |
| train | SOUND_REPETITION | 2 | 5 | {'inserted_copies': 3, 'silence_s': 0.1} | circular (detector measure) | 0 | 0 |  |
| train | SOUND_REPETITION | 3 | 5 | {'inserted_copies': 4, 'silence_s': 0.1} | circular (detector measure) | -0.0426 | -0.0426 |  |
| train | RHYME_PROLONGATION | 1 | 5 | {'added_duration_s': 0.18} | circular (detector measure) | 0.194 | 0.194 |  |
| train | RHYME_PROLONGATION | 2 | 5 | {'added_duration_s': 0.36} | circular (detector measure) | 0.381 | 0.381 |  |
| train | RHYME_PROLONGATION | 3 | 5 | {'added_duration_s': 0.54} | circular (detector measure) | 0.499 | 0.499 |  |
| train | ONSET_PROLONGATION | 1 | 5 | {'onset_target_s': 0.35} | circular (detector measure) | 0.49 | 0.49 |  |
| train | ONSET_PROLONGATION | 2 | 5 | {'onset_target_s': 0.65} | circular (detector measure) | 0.906 | 0.906 |  |
| train | ONSET_PROLONGATION | 3 | 5 | {'onset_target_s': 1.0} | circular (detector measure) | 1.21 | 1.21 |  |
| train | BLOCK | 1 | 4 | {'silence_s': 0.5} | circular (detector measure) | -0.0679 | -0.0679 |  |
| train | BLOCK | 2 | 4 | {'silence_s': 1.25} | circular (detector measure) | 0 | 0 |  |
| train | BLOCK | 3 | 4 | {'silence_s': 2.0} | circular (detector measure) | 0 | 0 |  |
| train | LOW_EFFORT | 1 | 5 | {'attenuation_db': 3.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 0.5} | circular (detector measure) | -1.99 | -1.99 |  |
| train | LOW_EFFORT | 2 | 5 | {'attenuation_db': 6.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 1.0} | circular (detector measure) | -4.17 | -4.17 |  |
| train | LOW_EFFORT | 3 | 5 | {'attenuation_db': 9.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 1.5} | circular (detector measure) | -6.5 | -6.5 |  |
| train | TRAILING_OFF | 1 | 5 | {'final_attenuation_db': 4.0, 'alpha_drop_per_db': 0.55} | circular (detector measure) | -1.61 | -1.61 |  |
| train | TRAILING_OFF | 2 | 5 | {'final_attenuation_db': 8.0, 'alpha_drop_per_db': 0.55} | circular (detector measure) | -3.21 | -3.21 |  |
| train | TRAILING_OFF | 3 | 5 | {'final_attenuation_db': 12.0, 'alpha_drop_per_db': 0.55} | circular (detector measure) | -4.73 | -4.73 |  |
| train | MISPLACED_EMPHASIS | 1 | 2 | {'function_duration_factor': 1.1, 'function_pitch_st': 2.0, 'function_gain_db': 2.0, 'stressed_removal_strength': 0.3} | circular (detector measure) | -0.333 | -0.333 |  |
| train | MISPLACED_EMPHASIS | 2 | 2 | {'function_duration_factor': 1.2, 'function_pitch_st': 4.0, 'function_gain_db': 4.0, 'stressed_removal_strength': 0.6} | circular (detector measure) | -0.647 | -0.647 |  |
| train | MISPLACED_EMPHASIS | 3 | 3 | {'function_duration_factor': 1.3, 'function_pitch_st': 6.0, 'function_gain_db': 6.0, 'stressed_removal_strength': 0.9} | circular (detector measure) | -0.883 | -0.883 |  |
| train | RISING_ENDING | 1 | 3 | {'rise_st': 2.0} | circular (detector measure) | 0.901 | 0.901 |  |
| train | RISING_ENDING | 2 | 3 | {'rise_st': 4.0} | circular (detector measure) | 1.84 | 1.84 |  |
| train | RISING_ENDING | 3 | 3 | {'rise_st': 6.0} | circular (detector measure) | 3.12 | 3.12 |  |
| train | FLAT_FINAL_FALL | 1 | 2 | {'strength': 0.333} | circular (detector measure) | 0.98 | 0.98 |  |
| train | FLAT_FINAL_FALL | 2 | 2 | {'strength': 0.667} | circular (detector measure) | 0.548 | 0.548 |  |
| train | FLAT_FINAL_FALL | 3 | 2 | {'strength': 1.0} | circular (detector measure) | 2.42 | 2.42 |  |
| train | REPEATED_CONTOUR | 1 | 0 | {'contour_strength': 0.333} | circular (detector measure) |  |  |  |
| train | REPEATED_CONTOUR | 2 | 0 | {'contour_strength': 0.667} | circular (detector measure) |  |  |  |
| train | REPEATED_CONTOUR | 3 | 0 | {'contour_strength': 1.0} | circular (detector measure) |  |  |  |
| val | RUSH | 1 | 2 | 1.2 | independent | -0.171 | -0.112 | 0.666 |
| val | RUSH | 2 | 2 | 1.45 | independent | -0.393 | -0.33 | 0.844 |
| val | RUSH | 3 | 2 | 1.9 | independent | -0.639 | -0.529 | 0.828 |
| val | DRAG | 1 | 2 | 1.2 | independent | 0.171 | 0.137 | 0.804 |
| val | DRAG | 2 | 2 | 1.45 | independent | 0.287 | 0.344 | 1.29 |
| val | DRAG | 3 | 2 | 1.9 | independent | 0.595 | 0.547 | 0.925 |
| val | PAUSE_DROPPED | 1 | 2 | 0.4 | independent | -0.405 | -0.405 | 1 |
| val | PAUSE_DROPPED | 2 | 2 | 0.2 | independent | -0.625 | -0.625 | 1 |
| val | PAUSE_DROPPED | 3 | 2 | 0 | independent | -1.15 | -1.15 | 1 |
| val | PAUSE_INTRUSIVE | 1 | 2 | 0.35 | independent | 0.31 | 0.31 | 1 |
| val | PAUSE_INTRUSIVE | 2 | 2 | 0.6 | independent | 0.605 | 0.605 | 1 |
| val | PAUSE_INTRUSIVE | 3 | 2 | 1.2 | independent | 1.18 | 1.18 | 1 |
| val | MONOTONE | 1 | 2 | 0.5 | independent | -0.555 | -0.501 | 0.901 |
| val | MONOTONE | 2 | 2 | 0.25 | independent | -1.11 | -1.02 | 0.919 |
| val | MONOTONE | 3 | 2 | 0 | independent | -2.08 | -1.6 | 0.767 |
| val | DEEMPHASIS | 1 | 2 | 0.5 | independent | -0.673 | -0.673 | 1 |
| val | DEEMPHASIS | 2 | 2 | 0.75 | independent | -1.31 | -1.31 | 1 |
| val | DEEMPHASIS | 3 | 2 | 1 | independent | -1.47 | -1.47 | 1 |
| val | FADE | 1 | 2 | 4 | independent | -2.25 | -2.33 | 1.03 |
| val | FADE | 2 | 2 | 8 | independent | -4.22 | -4.6 | 1.1 |
| val | FADE | 3 | 2 | 14 | independent | -8.22 | -7.89 | 0.966 |
| val | MUMBLE | 1 | 2 | 0.3 | independent | -0.295 | -0.274 | 0.925 |
| val | MUMBLE | 2 | 2 | 0.6 | independent | -0.639 | -0.392 | 0.607 |
| val | MUMBLE | 3 | 2 | 1 | independent | -0.757 | -0.641 | 0.847 |
| val | NATURAL_RUSH | 1 | 2 | {'speech_rate': 1.13, 'pause_kept_fraction': 0.6} | independent | -0.122 | -0.0628 | 0.514 |
| val | NATURAL_RUSH | 2 | 2 | {'speech_rate': 1.15, 'pause_kept_fraction': 0.3} | independent | -0.14 | -0.0291 | 0.208 |
| val | NATURAL_RUSH | 3 | 2 | {'speech_rate': 1.18, 'pause_kept_fraction': 0.0} | independent | -0.166 | -0.101 | 0.61 |
| val | HESITATION | 1 | 0 | {'word_duration_factor': 1.2, 'silence_s': 0.2} | circular (detector measure) |  |  |  |
| val | HESITATION | 2 | 2 | {'word_duration_factor': 1.5, 'silence_s': 0.5} | circular (detector measure) | 0.495 | 0.495 |  |
| val | HESITATION | 3 | 2 | {'word_duration_factor': 1.8, 'silence_s': 1.0} | circular (detector measure) | 0.995 | 0.995 |  |
| val | WORD_BY_WORD | 1 | 1 | {'silence_s': 0.15, 'every_words': 1} | circular (detector measure) | 0.15 | 0.15 |  |
| val | WORD_BY_WORD | 2 | 2 | {'silence_s': 0.225, 'every_words': 1} | circular (detector measure) | 0.22 | 0.22 |  |
| val | WORD_BY_WORD | 3 | 2 | {'silence_s': 0.3, 'every_words': 1} | circular (detector measure) | 0.295 | 0.295 |  |
| val | UNEVEN_TEMPO | 1 | 2 | {'max_duration_deviation': 0.15} | circular (detector measure) | 0 | 0 |  |
| val | UNEVEN_TEMPO | 2 | 2 | {'max_duration_deviation': 0.3} | circular (detector measure) | 0 | 0 |  |
| val | UNEVEN_TEMPO | 3 | 2 | {'max_duration_deviation': 0.45} | circular (detector measure) | 0 | 0 |  |
| val | WORD_REPETITION | 1 | 2 | {'first_token_duration_factor': 1.3, 'silence_s': 0.1, 'inserted_copies': 1} | circular (detector measure) | 0.0912 | 0.0912 |  |
| val | WORD_REPETITION | 2 | 1 | {'first_token_duration_factor': 1.6, 'silence_s': 0.225, 'inserted_copies': 1} | circular (detector measure) | 0.182 | 0.182 |  |
| val | WORD_REPETITION | 3 | 1 | {'first_token_duration_factor': 1.9, 'silence_s': 0.35, 'inserted_copies': 1} | circular (detector measure) | 0.182 | 0.182 |  |
| val | SOUND_REPETITION | 1 | 2 | {'inserted_copies': 2, 'silence_s': 0.1} | circular (detector measure) | -0.117 | -0.117 |  |
| val | SOUND_REPETITION | 2 | 2 | {'inserted_copies': 3, 'silence_s': 0.1} | circular (detector measure) | -0.04 | -0.04 |  |
| val | SOUND_REPETITION | 3 | 2 | {'inserted_copies': 4, 'silence_s': 0.1} | circular (detector measure) | -0.117 | -0.117 |  |
| val | RHYME_PROLONGATION | 1 | 2 | {'added_duration_s': 0.18} | circular (detector measure) | 0.327 | 0.327 |  |
| val | RHYME_PROLONGATION | 2 | 2 | {'added_duration_s': 0.36} | circular (detector measure) | 0.657 | 0.657 |  |
| val | RHYME_PROLONGATION | 3 | 2 | {'added_duration_s': 0.54} | circular (detector measure) | 0.936 | 0.936 |  |
| val | ONSET_PROLONGATION | 1 | 2 | {'onset_target_s': 0.35} | circular (detector measure) | 0.661 | 0.661 |  |
| val | ONSET_PROLONGATION | 2 | 2 | {'onset_target_s': 0.65} | circular (detector measure) | 0.934 | 0.934 |  |
| val | ONSET_PROLONGATION | 3 | 2 | {'onset_target_s': 1.0} | circular (detector measure) | 1.57 | 1.57 |  |
| val | BLOCK | 1 | 1 | {'silence_s': 0.5} | circular (detector measure) | 0 | 0 |  |
| val | BLOCK | 2 | 1 | {'silence_s': 1.25} | circular (detector measure) | -0.0741 | -0.0741 |  |
| val | BLOCK | 3 | 1 | {'silence_s': 2.0} | circular (detector measure) | 0 | 0 |  |
| val | LOW_EFFORT | 1 | 2 | {'attenuation_db': 3.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 0.5} | circular (detector measure) | -2.17 | -2.17 |  |
| val | LOW_EFFORT | 2 | 2 | {'attenuation_db': 6.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 1.0} | circular (detector measure) | -3.56 | -3.56 |  |
| val | LOW_EFFORT | 3 | 2 | {'attenuation_db': 9.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 1.5} | circular (detector measure) | -5.62 | -5.62 |  |
| val | TRAILING_OFF | 1 | 2 | {'final_attenuation_db': 4.0, 'alpha_drop_per_db': 0.55} | circular (detector measure) | -0.924 | -0.924 |  |
| val | TRAILING_OFF | 2 | 2 | {'final_attenuation_db': 8.0, 'alpha_drop_per_db': 0.55} | circular (detector measure) | -1.77 | -1.77 |  |
| val | TRAILING_OFF | 3 | 2 | {'final_attenuation_db': 12.0, 'alpha_drop_per_db': 0.55} | circular (detector measure) | -2.75 | -2.75 |  |
| val | MISPLACED_EMPHASIS | 1 | 2 | {'function_duration_factor': 1.1, 'function_pitch_st': 2.0, 'function_gain_db': 2.0, 'stressed_removal_strength': 0.3} | circular (detector measure) | -0.188 | -0.188 |  |
| val | MISPLACED_EMPHASIS | 2 | 2 | {'function_duration_factor': 1.2, 'function_pitch_st': 4.0, 'function_gain_db': 4.0, 'stressed_removal_strength': 0.6} | circular (detector measure) | -0.29 | -0.29 |  |
| val | MISPLACED_EMPHASIS | 3 | 2 | {'function_duration_factor': 1.3, 'function_pitch_st': 6.0, 'function_gain_db': 6.0, 'stressed_removal_strength': 0.9} | circular (detector measure) | -0.409 | -0.409 |  |
| val | RISING_ENDING | 1 | 1 | {'rise_st': 2.0} | circular (detector measure) | 1.14 | 1.14 |  |
| val | RISING_ENDING | 2 | 1 | {'rise_st': 4.0} | circular (detector measure) | -3.77 | -3.77 |  |
| val | RISING_ENDING | 3 | 1 | {'rise_st': 6.0} | circular (detector measure) | -1.99 | -1.99 |  |
| val | FLAT_FINAL_FALL | 1 | 1 | {'strength': 0.333} | circular (detector measure) | -2.23 | -2.23 |  |
| val | FLAT_FINAL_FALL | 2 | 2 | {'strength': 0.667} | circular (detector measure) | -3.19 | -3.19 |  |
| val | FLAT_FINAL_FALL | 3 | 2 | {'strength': 1.0} | circular (detector measure) | -0.15 | -0.15 |  |
| val | REPEATED_CONTOUR | 1 | 0 | {'contour_strength': 0.333} | circular (detector measure) |  |  |  |
| val | REPEATED_CONTOUR | 2 | 0 | {'contour_strength': 0.667} | circular (detector measure) |  |  |  |
| val | REPEATED_CONTOUR | 3 | 0 | {'contour_strength': 1.0} | circular (detector measure) |  |  |  |
| test | RUSH | 1 | 2 | 1.2 | independent | -0.182 | -0.156 | 0.854 |
| test | RUSH | 2 | 2 | 1.45 | independent | -0.374 | -0.242 | 0.647 |
| test | RUSH | 3 | 2 | 1.9 | independent | -0.642 | -0.517 | 0.805 |
| test | DRAG | 1 | 2 | 1.2 | independent | 0.182 | 0.159 | 0.871 |
| test | DRAG | 2 | 2 | 1.45 | independent | 0.372 | 0.328 | 0.883 |
| test | DRAG | 3 | 2 | 1.9 | independent | 0.644 | 0.605 | 0.941 |
| test | PAUSE_DROPPED | 1 | 2 | 0.4 | independent | -0.55 | -0.55 | 1 |
| test | PAUSE_DROPPED | 2 | 2 | 0.2 | independent | -0.51 | -0.51 | 1 |
| test | PAUSE_DROPPED | 3 | 2 | 0 | independent | -0.85 | -0.85 | 1 |
| test | PAUSE_INTRUSIVE | 1 | 2 | 0.35 | independent | 0.335 | 0.335 | 1 |
| test | PAUSE_INTRUSIVE | 2 | 2 | 0.6 | independent | 0.595 | 0.595 | 1 |
| test | PAUSE_INTRUSIVE | 3 | 2 | 1.2 | independent | 1.19 | 1.19 | 1 |
| test | MONOTONE | 1 | 2 | 0.5 | independent | -0.533 | -0.483 | 0.907 |
| test | MONOTONE | 2 | 2 | 0.25 | independent | -0.965 | -0.553 | 0.577 |
| test | MONOTONE | 3 | 2 | 0 | independent | -2.01 | -0.881 | 0.436 |
| test | DEEMPHASIS | 1 | 2 | 0.5 | independent | -0.818 | -0.818 | 1 |
| test | DEEMPHASIS | 2 | 2 | 0.75 | independent | -1.14 | -1.14 | 1 |
| test | DEEMPHASIS | 3 | 2 | 1 | independent | -1.41 | -1.41 | 1 |
| test | FADE | 1 | 2 | 4 | independent | -1.65 | -1.96 | 1.5 |
| test | FADE | 2 | 2 | 8 | independent | -5.78 | -6.11 | 1.06 |
| test | FADE | 3 | 2 | 14 | independent | -9.13 | -6.3 | 0.708 |
| test | MUMBLE | 1 | 2 | 0.3 | independent | -0.345 | -0.315 | 0.913 |
| test | MUMBLE | 2 | 2 | 0.6 | independent | -0.72 | -0.471 | 0.648 |
| test | MUMBLE | 3 | 2 | 1 | independent | -0.876 | -0.804 | 0.919 |
| test | NATURAL_RUSH | 1 | 2 | {'speech_rate': 1.13, 'pause_kept_fraction': 0.6} | independent | -0.122 | -0.058 | 0.475 |
| test | NATURAL_RUSH | 2 | 2 | {'speech_rate': 1.15, 'pause_kept_fraction': 0.3} | independent | -0.14 | -0.0866 | 0.62 |
| test | NATURAL_RUSH | 3 | 2 | {'speech_rate': 1.18, 'pause_kept_fraction': 0.0} | independent | -0.166 | -0.111 | 0.673 |
| test | HESITATION | 1 | 2 | {'word_duration_factor': 1.2, 'silence_s': 0.2} | circular (detector measure) | 0.2 | 0.2 |  |
| test | HESITATION | 2 | 2 | {'word_duration_factor': 1.5, 'silence_s': 0.5} | circular (detector measure) | 0.5 | 0.5 |  |
| test | HESITATION | 3 | 2 | {'word_duration_factor': 1.8, 'silence_s': 1.0} | circular (detector measure) | 1 | 1 |  |
| test | WORD_BY_WORD | 1 | 1 | {'silence_s': 0.15, 'every_words': 1} | circular (detector measure) | 0.15 | 0.15 |  |
| test | WORD_BY_WORD | 2 | 2 | {'silence_s': 0.225, 'every_words': 1} | circular (detector measure) | 0.22 | 0.22 |  |
| test | WORD_BY_WORD | 3 | 2 | {'silence_s': 0.3, 'every_words': 1} | circular (detector measure) | 0.295 | 0.295 |  |
| test | UNEVEN_TEMPO | 1 | 2 | {'max_duration_deviation': 0.15} | circular (detector measure) | 0 | 0 |  |
| test | UNEVEN_TEMPO | 2 | 2 | {'max_duration_deviation': 0.3} | circular (detector measure) | 0 | 0 |  |
| test | UNEVEN_TEMPO | 3 | 2 | {'max_duration_deviation': 0.45} | circular (detector measure) | 0 | 0 |  |
| test | WORD_REPETITION | 1 | 2 | {'first_token_duration_factor': 1.3, 'silence_s': 0.1, 'inserted_copies': 1} | circular (detector measure) | 0.444 | 0.444 |  |
| test | WORD_REPETITION | 2 | 2 | {'first_token_duration_factor': 1.6, 'silence_s': 0.225, 'inserted_copies': 1} | circular (detector measure) | 0.466 | 0.466 |  |
| test | WORD_REPETITION | 3 | 2 | {'first_token_duration_factor': 1.9, 'silence_s': 0.35, 'inserted_copies': 1} | circular (detector measure) | 0.0668 | 0.0668 |  |
| test | SOUND_REPETITION | 1 | 2 | {'inserted_copies': 2, 'silence_s': 0.1} | circular (detector measure) | 0 | 0 |  |
| test | SOUND_REPETITION | 2 | 2 | {'inserted_copies': 3, 'silence_s': 0.1} | circular (detector measure) | 0 | 0 |  |
| test | SOUND_REPETITION | 3 | 2 | {'inserted_copies': 4, 'silence_s': 0.1} | circular (detector measure) | 0.0286 | 0.0286 |  |
| test | RHYME_PROLONGATION | 1 | 2 | {'added_duration_s': 0.18} | circular (detector measure) | 0.148 | 0.148 |  |
| test | RHYME_PROLONGATION | 2 | 2 | {'added_duration_s': 0.36} | circular (detector measure) | 0.408 | 0.408 |  |
| test | RHYME_PROLONGATION | 3 | 2 | {'added_duration_s': 0.54} | circular (detector measure) | 0.607 | 0.607 |  |
| test | ONSET_PROLONGATION | 1 | 2 | {'onset_target_s': 0.35} | circular (detector measure) | 0.367 | 0.367 |  |
| test | ONSET_PROLONGATION | 2 | 2 | {'onset_target_s': 0.65} | circular (detector measure) | 0.723 | 0.723 |  |
| test | ONSET_PROLONGATION | 3 | 2 | {'onset_target_s': 1.0} | circular (detector measure) | 1.01 | 1.01 |  |
| test | BLOCK | 1 | 2 | {'silence_s': 0.5} | circular (detector measure) | -0.0762 | -0.0762 |  |
| test | BLOCK | 2 | 2 | {'silence_s': 1.25} | circular (detector measure) | 0 | 0 |  |
| test | BLOCK | 3 | 2 | {'silence_s': 2.0} | circular (detector measure) | -0.0286 | -0.0286 |  |
| test | LOW_EFFORT | 1 | 2 | {'attenuation_db': 3.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 0.5} | circular (detector measure) | -1.98 | -1.98 |  |
| test | LOW_EFFORT | 2 | 2 | {'attenuation_db': 6.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 1.0} | circular (detector measure) | -4.17 | -4.17 |  |
| test | LOW_EFFORT | 3 | 2 | {'attenuation_db': 9.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 1.5} | circular (detector measure) | -6.19 | -6.19 |  |
| test | TRAILING_OFF | 1 | 2 | {'final_attenuation_db': 4.0, 'alpha_drop_per_db': 0.55} | circular (detector measure) | -1.48 | -1.48 |  |
| test | TRAILING_OFF | 2 | 2 | {'final_attenuation_db': 8.0, 'alpha_drop_per_db': 0.55} | circular (detector measure) | -2.39 | -2.39 |  |
| test | TRAILING_OFF | 3 | 2 | {'final_attenuation_db': 12.0, 'alpha_drop_per_db': 0.55} | circular (detector measure) | -3.96 | -3.96 |  |
| test | MISPLACED_EMPHASIS | 1 | 0 | {'function_duration_factor': 1.1, 'function_pitch_st': 2.0, 'function_gain_db': 2.0, 'stressed_removal_strength': 0.3} | circular (detector measure) |  |  |  |
| test | MISPLACED_EMPHASIS | 2 | 0 | {'function_duration_factor': 1.2, 'function_pitch_st': 4.0, 'function_gain_db': 4.0, 'stressed_removal_strength': 0.6} | circular (detector measure) |  |  |  |
| test | MISPLACED_EMPHASIS | 3 | 0 | {'function_duration_factor': 1.3, 'function_pitch_st': 6.0, 'function_gain_db': 6.0, 'stressed_removal_strength': 0.9} | circular (detector measure) |  |  |  |
| test | RISING_ENDING | 1 | 1 | {'rise_st': 2.0} | circular (detector measure) | 1.12 | 1.12 |  |
| test | RISING_ENDING | 2 | 1 | {'rise_st': 4.0} | circular (detector measure) | 2.47 | 2.47 |  |
| test | RISING_ENDING | 3 | 1 | {'rise_st': 6.0} | circular (detector measure) | 3.6 | 3.6 |  |
| test | FLAT_FINAL_FALL | 1 | 1 | {'strength': 0.333} | circular (detector measure) | 0.508 | 0.508 |  |
| test | FLAT_FINAL_FALL | 2 | 1 | {'strength': 0.667} | circular (detector measure) | 0.917 | 0.917 |  |
| test | FLAT_FINAL_FALL | 3 | 1 | {'strength': 1.0} | circular (detector measure) | 1.05 | 1.05 |  |
| test | REPEATED_CONTOUR | 1 | 0 | {'contour_strength': 0.333} | circular (detector measure) |  |  |  |
| test | REPEATED_CONTOUR | 2 | 0 | {'contour_strength': 0.667} | circular (detector measure) |  |  |  |
| test | REPEATED_CONTOUR | 3 | 0 | {'contour_strength': 1.0} | circular (detector measure) |  |  |  |
| val+test | RUSH | 1 | 4 | 1.2 | independent | -0.182 | -0.144 | 0.839 |
| val+test | RUSH | 2 | 4 | 1.45 | independent | -0.374 | -0.293 | 0.74 |
| val+test | RUSH | 3 | 4 | 1.9 | independent | -0.642 | -0.522 | 0.814 |
| val+test | DRAG | 1 | 4 | 1.2 | independent | 0.182 | 0.155 | 0.851 |
| val+test | DRAG | 2 | 4 | 1.45 | independent | 0.372 | 0.336 | 0.959 |
| val+test | DRAG | 3 | 4 | 1.9 | independent | 0.635 | 0.58 | 0.941 |
| val+test | PAUSE_DROPPED | 1 | 4 | 0.4 | independent | -0.425 | -0.425 | 1 |
| val+test | PAUSE_DROPPED | 2 | 4 | 0.2 | independent | -0.55 | -0.55 | 1 |
| val+test | PAUSE_DROPPED | 3 | 4 | 0 | independent | -0.875 | -0.875 | 1 |
| val+test | PAUSE_INTRUSIVE | 1 | 4 | 0.35 | independent | 0.33 | 0.33 | 1 |
| val+test | PAUSE_INTRUSIVE | 2 | 4 | 0.6 | independent | 0.6 | 0.6 | 1 |
| val+test | PAUSE_INTRUSIVE | 3 | 4 | 1.2 | independent | 1.19 | 1.19 | 1 |
| val+test | MONOTONE | 1 | 4 | 0.5 | independent | -0.533 | -0.483 | 0.901 |
| val+test | MONOTONE | 2 | 4 | 0.25 | independent | -1 | -0.851 | 0.858 |
| val+test | MONOTONE | 3 | 4 | 0 | independent | -2.07 | -1.26 | 0.607 |
| val+test | DEEMPHASIS | 1 | 4 | 0.5 | independent | -0.741 | -0.741 | 1 |
| val+test | DEEMPHASIS | 2 | 4 | 0.75 | independent | -1.31 | -1.31 | 1 |
| val+test | DEEMPHASIS | 3 | 4 | 1 | independent | -1.41 | -1.41 | 1 |
| val+test | FADE | 1 | 4 | 4 | independent | -2.25 | -2.33 | 1.05 |
| val+test | FADE | 2 | 4 | 8 | independent | -5.18 | -5.3 | 1.06 |
| val+test | FADE | 3 | 4 | 14 | independent | -8.65 | -7.18 | 0.889 |
| val+test | MUMBLE | 1 | 4 | 0.3 | independent | -0.326 | -0.295 | 0.925 |
| val+test | MUMBLE | 2 | 4 | 0.6 | independent | -0.675 | -0.419 | 0.622 |
| val+test | MUMBLE | 3 | 4 | 1 | independent | -0.837 | -0.753 | 0.873 |
| val+test | NATURAL_RUSH | 1 | 4 | {'speech_rate': 1.13, 'pause_kept_fraction': 0.6} | independent | -0.122 | -0.06 | 0.491 |
| val+test | NATURAL_RUSH | 2 | 4 | {'speech_rate': 1.15, 'pause_kept_fraction': 0.3} | independent | -0.14 | -0.0554 | 0.396 |
| val+test | NATURAL_RUSH | 3 | 4 | {'speech_rate': 1.18, 'pause_kept_fraction': 0.0} | independent | -0.166 | -0.111 | 0.673 |
| val+test | HESITATION | 1 | 2 | {'word_duration_factor': 1.2, 'silence_s': 0.2} | circular (detector measure) | 0.2 | 0.2 |  |
| val+test | HESITATION | 2 | 4 | {'word_duration_factor': 1.5, 'silence_s': 0.5} | circular (detector measure) | 0.5 | 0.5 |  |
| val+test | HESITATION | 3 | 4 | {'word_duration_factor': 1.8, 'silence_s': 1.0} | circular (detector measure) | 1 | 1 |  |
| val+test | WORD_BY_WORD | 1 | 2 | {'silence_s': 0.15, 'every_words': 1} | circular (detector measure) | 0.15 | 0.15 |  |
| val+test | WORD_BY_WORD | 2 | 4 | {'silence_s': 0.225, 'every_words': 1} | circular (detector measure) | 0.22 | 0.22 |  |
| val+test | WORD_BY_WORD | 3 | 4 | {'silence_s': 0.3, 'every_words': 1} | circular (detector measure) | 0.295 | 0.295 |  |
| val+test | UNEVEN_TEMPO | 1 | 4 | {'max_duration_deviation': 0.15} | circular (detector measure) | 0 | 0 |  |
| val+test | UNEVEN_TEMPO | 2 | 4 | {'max_duration_deviation': 0.3} | circular (detector measure) | 0 | 0 |  |
| val+test | UNEVEN_TEMPO | 3 | 4 | {'max_duration_deviation': 0.45} | circular (detector measure) | 0 | 0 |  |
| val+test | WORD_REPETITION | 1 | 4 | {'first_token_duration_factor': 1.3, 'silence_s': 0.1, 'inserted_copies': 1} | circular (detector measure) | 0.0912 | 0.0912 |  |
| val+test | WORD_REPETITION | 2 | 3 | {'first_token_duration_factor': 1.6, 'silence_s': 0.225, 'inserted_copies': 1} | circular (detector measure) | 0.182 | 0.182 |  |
| val+test | WORD_REPETITION | 3 | 3 | {'first_token_duration_factor': 1.9, 'silence_s': 0.35, 'inserted_copies': 1} | circular (detector measure) | 0.182 | 0.182 |  |
| val+test | SOUND_REPETITION | 1 | 4 | {'inserted_copies': 2, 'silence_s': 0.1} | circular (detector measure) | -0.04 | -0.04 |  |
| val+test | SOUND_REPETITION | 2 | 4 | {'inserted_copies': 3, 'silence_s': 0.1} | circular (detector measure) | 0 | 0 |  |
| val+test | SOUND_REPETITION | 3 | 4 | {'inserted_copies': 4, 'silence_s': 0.1} | circular (detector measure) | -0.04 | -0.04 |  |
| val+test | RHYME_PROLONGATION | 1 | 4 | {'added_duration_s': 0.18} | circular (detector measure) | 0.327 | 0.327 |  |
| val+test | RHYME_PROLONGATION | 2 | 4 | {'added_duration_s': 0.36} | circular (detector measure) | 0.657 | 0.657 |  |
| val+test | RHYME_PROLONGATION | 3 | 4 | {'added_duration_s': 0.54} | circular (detector measure) | 0.936 | 0.936 |  |
| val+test | ONSET_PROLONGATION | 1 | 4 | {'onset_target_s': 0.35} | circular (detector measure) | 0.473 | 0.473 |  |
| val+test | ONSET_PROLONGATION | 2 | 4 | {'onset_target_s': 0.65} | circular (detector measure) | 0.835 | 0.835 |  |
| val+test | ONSET_PROLONGATION | 3 | 4 | {'onset_target_s': 1.0} | circular (detector measure) | 1.17 | 1.17 |  |
| val+test | BLOCK | 1 | 3 | {'silence_s': 0.5} | circular (detector measure) | -0.0572 | -0.0572 |  |
| val+test | BLOCK | 2 | 3 | {'silence_s': 1.25} | circular (detector measure) | 0 | 0 |  |
| val+test | BLOCK | 3 | 3 | {'silence_s': 2.0} | circular (detector measure) | 0 | 0 |  |
| val+test | LOW_EFFORT | 1 | 4 | {'attenuation_db': 3.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 0.5} | circular (detector measure) | -2.17 | -2.17 |  |
| val+test | LOW_EFFORT | 2 | 4 | {'attenuation_db': 6.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 1.0} | circular (detector measure) | -4.17 | -4.17 |  |
| val+test | LOW_EFFORT | 3 | 4 | {'attenuation_db': 9.0, 'alpha_drop_per_db': 0.55, 'pitch_lowering_st': 1.5} | circular (detector measure) | -6.19 | -6.19 |  |
| val+test | TRAILING_OFF | 1 | 4 | {'final_attenuation_db': 4.0, 'alpha_drop_per_db': 0.55} | circular (detector measure) | -1.32 | -1.32 |  |
| val+test | TRAILING_OFF | 2 | 4 | {'final_attenuation_db': 8.0, 'alpha_drop_per_db': 0.55} | circular (detector measure) | -1.82 | -1.82 |  |
| val+test | TRAILING_OFF | 3 | 4 | {'final_attenuation_db': 12.0, 'alpha_drop_per_db': 0.55} | circular (detector measure) | -2.97 | -2.97 |  |
| val+test | MISPLACED_EMPHASIS | 1 | 2 | {'function_duration_factor': 1.1, 'function_pitch_st': 2.0, 'function_gain_db': 2.0, 'stressed_removal_strength': 0.3} | circular (detector measure) | -0.188 | -0.188 |  |
| val+test | MISPLACED_EMPHASIS | 2 | 2 | {'function_duration_factor': 1.2, 'function_pitch_st': 4.0, 'function_gain_db': 4.0, 'stressed_removal_strength': 0.6} | circular (detector measure) | -0.29 | -0.29 |  |
| val+test | MISPLACED_EMPHASIS | 3 | 2 | {'function_duration_factor': 1.3, 'function_pitch_st': 6.0, 'function_gain_db': 6.0, 'stressed_removal_strength': 0.9} | circular (detector measure) | -0.409 | -0.409 |  |
| val+test | RISING_ENDING | 1 | 2 | {'rise_st': 2.0} | circular (detector measure) | 1.13 | 1.13 |  |
| val+test | RISING_ENDING | 2 | 2 | {'rise_st': 4.0} | circular (detector measure) | -0.651 | -0.651 |  |
| val+test | RISING_ENDING | 3 | 2 | {'rise_st': 6.0} | circular (detector measure) | 0.808 | 0.808 |  |
| val+test | FLAT_FINAL_FALL | 1 | 2 | {'strength': 0.333} | circular (detector measure) | -0.859 | -0.859 |  |
| val+test | FLAT_FINAL_FALL | 2 | 3 | {'strength': 0.667} | circular (detector measure) | -1.82 | -1.82 |  |
| val+test | FLAT_FINAL_FALL | 3 | 3 | {'strength': 1.0} | circular (detector measure) | 0.38 | 0.38 |  |
| val+test | REPEATED_CONTOUR | 1 | 0 | {'contour_strength': 0.333} | circular (detector measure) |  |  |  |
| val+test | REPEATED_CONTOUR | 2 | 0 | {'contour_strength': 0.667} | circular (detector measure) |  |  |  |
| val+test | REPEATED_CONTOUR | 3 | 0 | {'contour_strength': 1.0} | circular (detector measure) |  |  |  |

The table is circular for the recipe families marked "circular": their realised value is the detector's own measurement, so it cannot show that the detector measures the edit. NATURAL_RUSH realised is independent: the applied word-time ln ratio from the label's stretch sample counts (pauses excluded); its paired ratio is the share of the applied compression that D9 recovers:

| split | level | n | applied word time (ln) | D9 measured (ln) | median share recovered |
|---|---|---|---|---|---|
| train | 1 | 5 | -0.122 | -0.0572 | 0.468 |
| train | 2 | 5 | -0.14 | -0.0802 | 0.574 |
| train | 3 | 5 | -0.165 | -0.0953 | 0.576 |
| val | 1 | 2 | -0.122 | -0.0628 | 0.514 |
| val | 2 | 2 | -0.14 | -0.0291 | 0.208 |
| val | 3 | 2 | -0.166 | -0.101 | 0.61 |
| test | 1 | 2 | -0.122 | -0.058 | 0.475 |
| test | 2 | 2 | -0.14 | -0.0866 | 0.62 |
| test | 3 | 2 | -0.166 | -0.111 | 0.673 |
| val+test | 1 | 4 | -0.122 | -0.06 | 0.491 |
| val+test | 2 | 4 | -0.14 | -0.0554 | 0.396 |
| val+test | 3 | 4 | -0.166 | -0.111 | 0.673 |

| split | type | level | count | status |
|---|---|---|---|---|
| test | REPEATED_CONTOUR | 1 | 2 | no detector |
| test | REPEATED_CONTOUR | 2 | 2 | no detector |
| test | REPEATED_CONTOUR | 3 | 2 | no detector |
| train | REPEATED_CONTOUR | 1 | 5 | no detector |
| train | REPEATED_CONTOUR | 2 | 5 | no detector |
| train | REPEATED_CONTOUR | 3 | 5 | no detector |
| val | REPEATED_CONTOUR | 1 | 1 | no detector |
| val | REPEATED_CONTOUR | 2 | 1 | no detector |
| val | REPEATED_CONTOUR | 3 | 1 | no detector |

## Device agreement: GPU versus CPU alignment

| split | GPU | clips | recordings aligned | max word-time difference (ms) | flags identical |
|---|---|---|---|---|---|
| val | cuda:0 | 3 | 4 | 0 | True |
| test | cuda:0 | 3 | 4 | 0 | True |
| val+test | cuda:0 | 6 | 8 | 0 | True |

## R2 lockbox false regions (final evaluation, both modes)

Lockbox readers by source: {'accent': 192, 'ears': 0, 'gettysburg': 0, 'poetry': 45}; comparisons: {'single': 1175, 'consensus5': 211}; 14 lockbox readings excluded when located. Measured once, after calibration, with the select estimator (equal sources over the covered sources; comparison-minutes within a source).

| mode | set | weighted total/min | pooled total/min | weighted upper95 | budget status | budget statement | scope |
|---|---|---|---|---|---|---|---|
| single | lockbox | 0.46 | 0.522 | 0.538 | met on covered sources only | lockbox single rates cover accent, poetry with equal source weights; ears is not covered: the R2 pool partition has no lockbox reader of this source; gettysburg is not covered: the R2 pool partition has no lockbox reader of this source. over the covered sources only, 0.5/min budget holds at the point rate; upper95 does not establish the budget | lockbox single rates cover accent, poetry with equal source weights; ears is not covered: the R2 pool partition has no lockbox reader of this source; gettysburg is not covered: the R2 pool partition has no lockbox reader of this source |
| consensus5 | lockbox | 0.516 | 0.53 | 0.684 | not met on covered sources only | lockbox consensus5 rates cover accent, poetry with equal source weights; ears is not covered: the R2 pool partition has no lockbox reader of this source; gettysburg is not covered: the R2 pool partition has no lockbox reader of this source. over the covered sources only, 0.5/min budget is not met at the point rate; upper95 does not establish the budget | lockbox consensus5 rates cover accent, poetry with equal source weights; ears is not covered: the R2 pool partition has no lockbox reader of this source; gettysburg is not covered: the R2 pool partition has no lockbox reader of this source |

Per key, beside the per-key share:

| mode | set | key | share/min | weighted/min | pooled/min | weighted upper95 | pooled upper95 | point within share | upper95 within share | valid units |
|---|---|---|---|---|---|---|---|---|---|---|
| single | lockbox | D1- | 0.0833 | 0.1 | 0.128 | 0.123 | 0.159 | False | False | 92705 |
| single | lockbox | D1+ | 0.0833 | 0.0817 | 0.104 | 0.125 | 0.162 | True | False | 92705 |
| single | lockbox | D2- | 0.0833 | 0.00977 | 0.0129 | 0.015 | 0.0202 | True | True | 6774 |
| single | lockbox | D2+ | 0.0833 | 0.0695 | 0.0873 | 0.105 | 0.134 | True | False | 6774 |
| single | lockbox | D3- | 0.0833 | 0.0761 | 0.0744 | 0.105 | 0.107 | True | False | 76004 |
| single | lockbox | D5- | 0.0833 | 0.123 | 0.116 | 0.162 | 0.151 | False | False | 92705 |
| consensus5 | lockbox | D1- | 0.0833 | 0.0641 | 0.0699 | 0.122 | 0.115 | True | False | 15581 |
| consensus5 | lockbox | D1+ | 0.0833 | 0.131 | 0.18 | 0.21 | 0.267 | False | False | 15581 |
| consensus5 | lockbox | D2- | 0.0833 | 0.00611 | 0.00999 | 0.0184 | 0.0302 | True | True | 846 |
| consensus5 | lockbox | D2+ | 0.0833 | 0.0824 | 0.0999 | 0.143 | 0.162 | True | False | 846 |
| consensus5 | lockbox | D3- | 0.0833 | 0.113 | 0.0799 | 0.188 | 0.135 | False | False | 13357 |
| consensus5 | lockbox | D5- | 0.0833 | 0.119 | 0.0899 | 0.223 | 0.151 | False | False | 15581 |

Per source:

| mode | set | key | source | rate/min (texts by comparison-minutes) | pooled/min | flags | comparison-minutes |
|---|---|---|---|---|---|---|---|
| single | lockbox | D1- | accent | 0.186 | 0.186 | 76 | 409 |
| single | lockbox | D1- | poetry | 0.0144 | 0.0144 | 3 | 209 |
| single | lockbox | D1+ | accent | 0.149 | 0.149 | 61 | 409 |
| single | lockbox | D1+ | poetry | 0.0144 | 0.0144 | 3 | 209 |
| single | lockbox | D2- | accent | 0.0195 | 0.0195 | 8 | 409 |
| single | lockbox | D2- | poetry | 0 | 0 | 0 | 209 |
| single | lockbox | D2+ | accent | 0.125 | 0.125 | 51 | 409 |
| single | lockbox | D2+ | poetry | 0.0144 | 0.0144 | 3 | 209 |
| single | lockbox | D3- | accent | 0.0709 | 0.0709 | 29 | 409 |
| single | lockbox | D3- | poetry | 0.0813 | 0.0813 | 17 | 209 |
| single | lockbox | D5- | accent | 0.103 | 0.103 | 42 | 409 |
| single | lockbox | D5- | poetry | 0.144 | 0.144 | 30 | 209 |
| single | lockbox | total | accent | 0.652 | 0.652 | 267 | 409 |
| single | lockbox | total | poetry | 0.268 | 0.268 | 56 | 209 |
| consensus5 | lockbox | D1- | accent | 0.0733 | 0.0733 | 6 | 81.9 |
| consensus5 | lockbox | D1- | poetry | 0.0549 | 0.0549 | 1 | 18.2 |
| consensus5 | lockbox | D1+ | accent | 0.208 | 0.208 | 17 | 81.9 |
| consensus5 | lockbox | D1+ | poetry | 0.0549 | 0.0549 | 1 | 18.2 |
| consensus5 | lockbox | D2- | accent | 0.0122 | 0.0122 | 1 | 81.9 |
| consensus5 | lockbox | D2- | poetry | 0 | 0 | 0 | 18.2 |
| consensus5 | lockbox | D2+ | accent | 0.11 | 0.11 | 9 | 81.9 |
| consensus5 | lockbox | D2+ | poetry | 0.0549 | 0.0549 | 1 | 18.2 |
| consensus5 | lockbox | D3- | accent | 0.0611 | 0.0611 | 5 | 81.9 |
| consensus5 | lockbox | D3- | poetry | 0.165 | 0.165 | 3 | 18.2 |
| consensus5 | lockbox | D5- | accent | 0.0733 | 0.0733 | 6 | 81.9 |
| consensus5 | lockbox | D5- | poetry | 0.165 | 0.165 | 3 | 18.2 |
| consensus5 | lockbox | total | accent | 0.538 | 0.538 | 44 | 81.9 |
| consensus5 | lockbox | total | poetry | 0.494 | 0.494 | 9 | 18.2 |

Per participant first language (Accent Archive readers):

| mode | set | key | L1 | readers | flags | comparison-minutes | rate/min | 95% CI (reader clusters; none for zero events) |
|---|---|---|---|---|---|---|---|---|
| single | lockbox | D1- | afrikaans | 1 | 0 | 1.73 | 0 | [n/a, n/a] |
| single | lockbox | D1- | albanian | 2 | 1 | 4.3 | 0.233 | [0, 0.442] |
| single | lockbox | D1- | amharic | 5 | 3 | 14.1 | 0.213 | [0, 0.428] |
| single | lockbox | D1- | arabic | 26 | 6 | 72.2 | 0.0831 | [0.0273, 0.141] |
| single | lockbox | D1- | armenian | 2 | 1 | 4.64 | 0.215 | [0, 0.417] |
| single | lockbox | D1- | azerbaijani | 1 | 0 | 4.54 | 0 | [n/a, n/a] |
| single | lockbox | D1- | bambara | 1 | 0 | 2.97 | 0 | [n/a, n/a] |
| single | lockbox | D1- | bari | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | lockbox | D1- | bavarian | 1 | 1 | 1.99 | 0.503 | [n/a, n/a] |
| single | lockbox | D1- | belarusan | 1 | 1 | 2.16 | 0.462 | [n/a, n/a] |
| single | lockbox | D1- | bengali | 4 | 0 | 9.21 | 0 | [n/a, n/a] |
| single | lockbox | D1- | bosnian | 2 | 4 | 4.76 | 0.841 | [0, 1.68] |
| single | lockbox | D1- | bulgarian | 1 | 0 | 2.09 | 0 | [n/a, n/a] |
| single | lockbox | D1- | english | 144 | 59 | 281 | 0.21 | [0.154, 0.278] |
| single | lockbox | D1+ | afrikaans | 1 | 1 | 1.73 | 0.578 | [n/a, n/a] |
| single | lockbox | D1+ | albanian | 2 | 3 | 4.3 | 0.698 | [0, 1.47] |
| single | lockbox | D1+ | amharic | 5 | 5 | 14.1 | 0.356 | [0, 0.951] |
| single | lockbox | D1+ | arabic | 26 | 13 | 72.2 | 0.18 | [0, 0.401] |
| single | lockbox | D1+ | armenian | 2 | 0 | 4.64 | 0 | [n/a, n/a] |
| single | lockbox | D1+ | azerbaijani | 1 | 2 | 4.54 | 0.441 | [n/a, n/a] |
| single | lockbox | D1+ | bambara | 1 | 0 | 2.97 | 0 | [n/a, n/a] |
| single | lockbox | D1+ | bari | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | lockbox | D1+ | bavarian | 1 | 0 | 1.99 | 0 | [n/a, n/a] |
| single | lockbox | D1+ | belarusan | 1 | 0 | 2.16 | 0 | [n/a, n/a] |
| single | lockbox | D1+ | bengali | 4 | 5 | 9.21 | 0.543 | [0, 1.6] |
| single | lockbox | D1+ | bosnian | 2 | 0 | 4.76 | 0 | [n/a, n/a] |
| single | lockbox | D1+ | bulgarian | 1 | 5 | 2.09 | 2.39 | [n/a, n/a] |
| single | lockbox | D1+ | english | 144 | 27 | 281 | 0.096 | [0.0213, 0.208] |
| single | lockbox | D2- | afrikaans | 1 | 0 | 1.73 | 0 | [n/a, n/a] |
| single | lockbox | D2- | albanian | 2 | 1 | 4.3 | 0.233 | [0, 0.49] |
| single | lockbox | D2- | amharic | 5 | 0 | 14.1 | 0 | [n/a, n/a] |
| single | lockbox | D2- | arabic | 26 | 1 | 72.2 | 0.0139 | [0, 0.045] |
| single | lockbox | D2- | armenian | 2 | 0 | 4.64 | 0 | [n/a, n/a] |
| single | lockbox | D2- | azerbaijani | 1 | 0 | 4.54 | 0 | [n/a, n/a] |
| single | lockbox | D2- | bambara | 1 | 0 | 2.97 | 0 | [n/a, n/a] |
| single | lockbox | D2- | bari | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | lockbox | D2- | bavarian | 1 | 0 | 1.99 | 0 | [n/a, n/a] |
| single | lockbox | D2- | belarusan | 1 | 0 | 2.16 | 0 | [n/a, n/a] |
| single | lockbox | D2- | bengali | 4 | 0 | 9.21 | 0 | [n/a, n/a] |
| single | lockbox | D2- | bosnian | 2 | 0 | 4.76 | 0 | [n/a, n/a] |
| single | lockbox | D2- | bulgarian | 1 | 0 | 2.09 | 0 | [n/a, n/a] |
| single | lockbox | D2- | english | 144 | 6 | 281 | 0.0213 | [0.00699, 0.0401] |
| single | lockbox | D2+ | afrikaans | 1 | 0 | 1.73 | 0 | [n/a, n/a] |
| single | lockbox | D2+ | albanian | 2 | 0 | 4.3 | 0 | [n/a, n/a] |
| single | lockbox | D2+ | amharic | 5 | 4 | 14.1 | 0.285 | [0, 0.742] |
| single | lockbox | D2+ | arabic | 26 | 37 | 72.2 | 0.513 | [0.166, 0.882] |
| single | lockbox | D2+ | armenian | 2 | 0 | 4.64 | 0 | [n/a, n/a] |
| single | lockbox | D2+ | azerbaijani | 1 | 1 | 4.54 | 0.22 | [n/a, n/a] |
| single | lockbox | D2+ | bambara | 1 | 2 | 2.97 | 0.673 | [n/a, n/a] |
| single | lockbox | D2+ | bari | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | lockbox | D2+ | bavarian | 1 | 0 | 1.99 | 0 | [n/a, n/a] |
| single | lockbox | D2+ | belarusan | 1 | 0 | 2.16 | 0 | [n/a, n/a] |
| single | lockbox | D2+ | bengali | 4 | 0 | 9.21 | 0 | [n/a, n/a] |
| single | lockbox | D2+ | bosnian | 2 | 0 | 4.76 | 0 | [n/a, n/a] |
| single | lockbox | D2+ | bulgarian | 1 | 0 | 2.09 | 0 | [n/a, n/a] |
| single | lockbox | D2+ | english | 144 | 7 | 281 | 0.0249 | [0, 0.0678] |
| single | lockbox | D3- | afrikaans | 1 | 0 | 1.73 | 0 | [n/a, n/a] |
| single | lockbox | D3- | albanian | 2 | 1 | 4.3 | 0.233 | [0, 0.442] |
| single | lockbox | D3- | amharic | 5 | 2 | 14.1 | 0.142 | [0, 0.461] |
| single | lockbox | D3- | arabic | 26 | 5 | 72.2 | 0.0693 | [0, 0.229] |
| single | lockbox | D3- | armenian | 2 | 0 | 4.64 | 0 | [n/a, n/a] |
| single | lockbox | D3- | azerbaijani | 1 | 0 | 4.54 | 0 | [n/a, n/a] |
| single | lockbox | D3- | bambara | 1 | 0 | 2.97 | 0 | [n/a, n/a] |
| single | lockbox | D3- | bari | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | lockbox | D3- | bavarian | 1 | 0 | 1.99 | 0 | [n/a, n/a] |
| single | lockbox | D3- | belarusan | 1 | 0 | 2.16 | 0 | [n/a, n/a] |
| single | lockbox | D3- | bengali | 4 | 0 | 9.21 | 0 | [n/a, n/a] |
| single | lockbox | D3- | bosnian | 2 | 0 | 4.76 | 0 | [n/a, n/a] |
| single | lockbox | D3- | bulgarian | 1 | 0 | 2.09 | 0 | [n/a, n/a] |
| single | lockbox | D3- | english | 144 | 21 | 281 | 0.0747 | [0.0219, 0.146] |
| single | lockbox | D5- | afrikaans | 1 | 0 | 1.73 | 0 | [n/a, n/a] |
| single | lockbox | D5- | albanian | 2 | 0 | 4.3 | 0 | [n/a, n/a] |
| single | lockbox | D5- | amharic | 5 | 4 | 14.1 | 0.285 | [0, 0.761] |
| single | lockbox | D5- | arabic | 26 | 10 | 72.2 | 0.139 | [0.0275, 0.296] |
| single | lockbox | D5- | armenian | 2 | 0 | 4.64 | 0 | [n/a, n/a] |
| single | lockbox | D5- | azerbaijani | 1 | 3 | 4.54 | 0.661 | [n/a, n/a] |
| single | lockbox | D5- | bambara | 1 | 0 | 2.97 | 0 | [n/a, n/a] |
| single | lockbox | D5- | bari | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | lockbox | D5- | bavarian | 1 | 0 | 1.99 | 0 | [n/a, n/a] |
| single | lockbox | D5- | belarusan | 1 | 0 | 2.16 | 0 | [n/a, n/a] |
| single | lockbox | D5- | bengali | 4 | 0 | 9.21 | 0 | [n/a, n/a] |
| single | lockbox | D5- | bosnian | 2 | 0 | 4.76 | 0 | [n/a, n/a] |
| single | lockbox | D5- | bulgarian | 1 | 0 | 2.09 | 0 | [n/a, n/a] |
| single | lockbox | D5- | english | 144 | 25 | 281 | 0.0889 | [0.0501, 0.134] |
| single | lockbox | total | afrikaans | 1 | 1 | 1.73 | 0.578 | [n/a, n/a] |
| single | lockbox | total | albanian | 2 | 6 | 4.3 | 1.4 | [0.885, 1.96] |
| single | lockbox | total | amharic | 5 | 18 | 14.1 | 1.28 | [0.373, 1.96] |
| single | lockbox | total | arabic | 26 | 72 | 72.2 | 0.997 | [0.527, 1.49] |
| single | lockbox | total | armenian | 2 | 1 | 4.64 | 0.215 | [0, 0.417] |
| single | lockbox | total | azerbaijani | 1 | 6 | 4.54 | 1.32 | [n/a, n/a] |
| single | lockbox | total | bambara | 1 | 2 | 2.97 | 0.673 | [n/a, n/a] |
| single | lockbox | total | bari | 1 | 0 | 3.51 | 0 | [n/a, n/a] |
| single | lockbox | total | bavarian | 1 | 1 | 1.99 | 0.503 | [n/a, n/a] |
| single | lockbox | total | belarusan | 1 | 1 | 2.16 | 0.462 | [n/a, n/a] |
| single | lockbox | total | bengali | 4 | 5 | 9.21 | 0.543 | [0, 1.6] |
| single | lockbox | total | bosnian | 2 | 4 | 4.76 | 0.841 | [0, 1.68] |
| single | lockbox | total | bulgarian | 1 | 5 | 2.09 | 2.39 | [n/a, n/a] |
| single | lockbox | total | english | 144 | 145 | 281 | 0.516 | [0.373, 0.692] |
| consensus5 | lockbox | D1- | afrikaans | 1 | 0 | 0.346 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1- | albanian | 2 | 0 | 0.86 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1- | amharic | 5 | 0 | 2.81 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1- | arabic | 26 | 0 | 14.4 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1- | armenian | 2 | 0 | 0.929 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1- | azerbaijani | 1 | 0 | 0.908 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1- | bambara | 1 | 0 | 0.594 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1- | bari | 1 | 0 | 0.702 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1- | bavarian | 1 | 0 | 0.398 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1- | belarusan | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1- | bengali | 4 | 0 | 1.84 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1- | bosnian | 2 | 1 | 0.951 | 1.05 | [0, 2.1] |
| consensus5 | lockbox | D1- | bulgarian | 1 | 0 | 0.418 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1- | english | 144 | 5 | 56.2 | 0.0889 | [0.0181, 0.173] |
| consensus5 | lockbox | D1+ | afrikaans | 1 | 0 | 0.346 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1+ | albanian | 2 | 2 | 0.86 | 2.33 | [0, 4.9] |
| consensus5 | lockbox | D1+ | amharic | 5 | 1 | 2.81 | 0.356 | [0, 0.951] |
| consensus5 | lockbox | D1+ | arabic | 26 | 4 | 14.4 | 0.277 | [0, 0.602] |
| consensus5 | lockbox | D1+ | armenian | 2 | 0 | 0.929 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1+ | azerbaijani | 1 | 1 | 0.908 | 1.1 | [n/a, n/a] |
| consensus5 | lockbox | D1+ | bambara | 1 | 0 | 0.594 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1+ | bari | 1 | 0 | 0.702 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1+ | bavarian | 1 | 0 | 0.398 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1+ | belarusan | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1+ | bengali | 4 | 1 | 1.84 | 0.543 | [0, 1.6] |
| consensus5 | lockbox | D1+ | bosnian | 2 | 0 | 0.951 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D1+ | bulgarian | 1 | 1 | 0.418 | 2.39 | [n/a, n/a] |
| consensus5 | lockbox | D1+ | english | 144 | 7 | 56.2 | 0.124 | [0.0181, 0.266] |
| consensus5 | lockbox | D2- | afrikaans | 1 | 0 | 0.346 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2- | albanian | 2 | 0 | 0.86 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2- | amharic | 5 | 0 | 2.81 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2- | arabic | 26 | 0 | 14.4 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2- | armenian | 2 | 0 | 0.929 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2- | azerbaijani | 1 | 0 | 0.908 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2- | bambara | 1 | 0 | 0.594 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2- | bari | 1 | 0 | 0.702 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2- | bavarian | 1 | 0 | 0.398 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2- | belarusan | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2- | bengali | 4 | 0 | 1.84 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2- | bosnian | 2 | 0 | 0.951 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2- | bulgarian | 1 | 0 | 0.418 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2- | english | 144 | 1 | 56.2 | 0.0178 | [0, 0.0543] |
| consensus5 | lockbox | D2+ | afrikaans | 1 | 0 | 0.346 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2+ | albanian | 2 | 0 | 0.86 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2+ | amharic | 5 | 1 | 2.81 | 0.356 | [0, 0.927] |
| consensus5 | lockbox | D2+ | arabic | 26 | 7 | 14.4 | 0.485 | [0.13, 0.882] |
| consensus5 | lockbox | D2+ | armenian | 2 | 0 | 0.929 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2+ | azerbaijani | 1 | 0 | 0.908 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2+ | bambara | 1 | 0 | 0.594 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2+ | bari | 1 | 0 | 0.702 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2+ | bavarian | 1 | 0 | 0.398 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2+ | belarusan | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2+ | bengali | 4 | 0 | 1.84 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2+ | bosnian | 2 | 0 | 0.951 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2+ | bulgarian | 1 | 0 | 0.418 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D2+ | english | 144 | 1 | 56.2 | 0.0178 | [0, 0.0539] |
| consensus5 | lockbox | D3- | afrikaans | 1 | 0 | 0.346 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D3- | albanian | 2 | 0 | 0.86 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D3- | amharic | 5 | 0 | 2.81 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D3- | arabic | 26 | 1 | 14.4 | 0.0693 | [0, 0.229] |
| consensus5 | lockbox | D3- | armenian | 2 | 0 | 0.929 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D3- | azerbaijani | 1 | 0 | 0.908 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D3- | bambara | 1 | 0 | 0.594 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D3- | bari | 1 | 0 | 0.702 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D3- | bavarian | 1 | 0 | 0.398 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D3- | belarusan | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D3- | bengali | 4 | 0 | 1.84 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D3- | bosnian | 2 | 0 | 0.951 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D3- | bulgarian | 1 | 0 | 0.418 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D3- | english | 144 | 4 | 56.2 | 0.0711 | [0, 0.163] |
| consensus5 | lockbox | D5- | afrikaans | 1 | 0 | 0.346 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D5- | albanian | 2 | 0 | 0.86 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D5- | amharic | 5 | 2 | 2.81 | 0.711 | [0, 1.9] |
| consensus5 | lockbox | D5- | arabic | 26 | 1 | 14.4 | 0.0693 | [0, 0.228] |
| consensus5 | lockbox | D5- | armenian | 2 | 0 | 0.929 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D5- | azerbaijani | 1 | 1 | 0.908 | 1.1 | [n/a, n/a] |
| consensus5 | lockbox | D5- | bambara | 1 | 0 | 0.594 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D5- | bari | 1 | 0 | 0.702 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D5- | bavarian | 1 | 0 | 0.398 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D5- | belarusan | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D5- | bengali | 4 | 0 | 1.84 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D5- | bosnian | 2 | 0 | 0.951 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D5- | bulgarian | 1 | 0 | 0.418 | 0 | [n/a, n/a] |
| consensus5 | lockbox | D5- | english | 144 | 2 | 56.2 | 0.0356 | [0, 0.0889] |
| consensus5 | lockbox | total | afrikaans | 1 | 0 | 0.346 | 0 | [n/a, n/a] |
| consensus5 | lockbox | total | albanian | 2 | 2 | 0.86 | 2.33 | [0, 4.9] |
| consensus5 | lockbox | total | amharic | 5 | 4 | 2.81 | 1.42 | [0, 2.95] |
| consensus5 | lockbox | total | arabic | 26 | 13 | 14.4 | 0.9 | [0.405, 1.45] |
| consensus5 | lockbox | total | armenian | 2 | 0 | 0.929 | 0 | [n/a, n/a] |
| consensus5 | lockbox | total | azerbaijani | 1 | 2 | 0.908 | 2.2 | [n/a, n/a] |
| consensus5 | lockbox | total | bambara | 1 | 0 | 0.594 | 0 | [n/a, n/a] |
| consensus5 | lockbox | total | bari | 1 | 0 | 0.702 | 0 | [n/a, n/a] |
| consensus5 | lockbox | total | bavarian | 1 | 0 | 0.398 | 0 | [n/a, n/a] |
| consensus5 | lockbox | total | belarusan | 1 | 0 | 0.433 | 0 | [n/a, n/a] |
| consensus5 | lockbox | total | bengali | 4 | 1 | 1.84 | 0.543 | [0, 1.6] |
| consensus5 | lockbox | total | bosnian | 2 | 1 | 0.951 | 1.05 | [0, 2.1] |
| consensus5 | lockbox | total | bulgarian | 1 | 1 | 0.418 | 2.39 | [n/a, n/a] |
| consensus5 | lockbox | total | english | 144 | 20 | 56.2 | 0.356 | [0.144, 0.614] |

Stated limits:

- single lockbox: false-region budget met on covered sources only (weighted 0.46/min, bootstrap upper95 0.538, budget 0.5/min); sources above the budget: accent 0.652/min; first languages above it: amharic 1.28/min (5 readers, 14.1 min), arabic 0.997/min (26 readers, 72.2 min), bengali 0.543/min (4 readers, 9.21 min), english 0.516/min (144 readers, 281 min)
- consensus5 lockbox: false-region budget not met on covered sources only (weighted 0.516/min, bootstrap upper95 0.684, budget 0.5/min); sources above the budget: accent 0.538/min; first languages above it: arabic 0.9/min (26 readers, 14.4 min)

## Cross-speaker operating curve (threshold h versus false regions and detection)

| flag key | h | threshold | fitted on null fit pool | observed false regions per comparison-minute | reader counts | away-edits detected | by type |
|---|---|---|---|---|---|---|---|
| D1- | 1 | 0.148 | False | 6.7 | {'gettysburg_dj': 19, 'gettysburg_sa': 13, 'gettysburg_tg': 20} | 29/31 (95% Wilson [0.793, 0.982]) | {'RUSH': '29/31 (95% Wilson [0.793, 0.982])'} |
| D1- | 1.5 | 0.222 | False | 3.48 | {'gettysburg_dj': 8, 'gettysburg_sa': 7, 'gettysburg_tg': 12} | 29/31 (95% Wilson [0.793, 0.982]) | {'RUSH': '29/31 (95% Wilson [0.793, 0.982])'} |
| D1- | 2 | 0.297 | False | 1.8 | {'gettysburg_dj': 5, 'gettysburg_sa': 3, 'gettysburg_tg': 6} | 25/31 (95% Wilson [0.637, 0.908]) | {'RUSH': '25/31 (95% Wilson [0.637, 0.908])'} |
| D1- | 2.5 | 0.371 | False | 1.29 | {'gettysburg_dj': 5, 'gettysburg_sa': 1, 'gettysburg_tg': 4} | 23/31 (95% Wilson [0.568, 0.863]) | {'RUSH': '23/31 (95% Wilson [0.568, 0.863])'} |
| D1- | 3 | 0.445 | False | 0.387 | {'gettysburg_dj': 1, 'gettysburg_sa': 1, 'gettysburg_tg': 1} | 21/31 (95% Wilson [0.501, 0.814]) | {'RUSH': '21/31 (95% Wilson [0.501, 0.814])'} |
| D1- | 3.5 | 0.519 | False | 0.258 | {'gettysburg_dj': 0, 'gettysburg_sa': 1, 'gettysburg_tg': 1} | 14/31 (95% Wilson [0.292, 0.622]) | {'RUSH': '14/31 (95% Wilson [0.292, 0.622])'} |
| D1- | 4 | 0.593 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 10/31 (95% Wilson [0.186, 0.499]) | {'RUSH': '10/31 (95% Wilson [0.186, 0.499])'} |
| D1- | 4.5 | 0.667 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 7/31 (95% Wilson [0.114, 0.398]) | {'RUSH': '7/31 (95% Wilson [0.114, 0.398])'} |
| D1- | 5 | 0.741 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 3/31 (95% Wilson [0.0335, 0.249]) | {'RUSH': '3/31 (95% Wilson [0.0335, 0.249])'} |
| D1- | 5.35 | 0.793 | True | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 1/31 (95% Wilson [0.00572, 0.162]) | {'RUSH': '1/31 (95% Wilson [0.00572, 0.162])'} |
| D1- | 5.5 | 0.815 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/31 (95% Wilson [0, 0.11]) | {'RUSH': '0/31 (95% Wilson [0, 0.11])'} |
| D1- | 6 | 0.89 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/31 (95% Wilson [0, 0.11]) | {'RUSH': '0/31 (95% Wilson [0, 0.11])'} |
| D1+ | 1 | 0.148 | False | 6.44 | {'gettysburg_dj': 14, 'gettysburg_sa': 17, 'gettysburg_tg': 19} | 17/17 (95% Wilson [0.816, 1]) | {'DRAG': '17/17 (95% Wilson [0.816, 1])'} |
| D1+ | 1.5 | 0.222 | False | 3.35 | {'gettysburg_dj': 9, 'gettysburg_sa': 7, 'gettysburg_tg': 10} | 17/17 (95% Wilson [0.816, 1]) | {'DRAG': '17/17 (95% Wilson [0.816, 1])'} |
| D1+ | 2 | 0.297 | False | 1.8 | {'gettysburg_dj': 6, 'gettysburg_sa': 3, 'gettysburg_tg': 5} | 16/17 (95% Wilson [0.73, 0.99]) | {'DRAG': '16/17 (95% Wilson [0.73, 0.99])'} |
| D1+ | 2.5 | 0.371 | False | 0.644 | {'gettysburg_dj': 1, 'gettysburg_sa': 1, 'gettysburg_tg': 3} | 16/17 (95% Wilson [0.73, 0.99]) | {'DRAG': '16/17 (95% Wilson [0.73, 0.99])'} |
| D1+ | 3 | 0.445 | False | 0.387 | {'gettysburg_dj': 1, 'gettysburg_sa': 0, 'gettysburg_tg': 2} | 15/17 (95% Wilson [0.657, 0.967]) | {'DRAG': '15/17 (95% Wilson [0.657, 0.967])'} |
| D1+ | 3.5 | 0.519 | False | 0.258 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 2} | 13/17 (95% Wilson [0.527, 0.904]) | {'DRAG': '13/17 (95% Wilson [0.527, 0.904])'} |
| D1+ | 4 | 0.593 | False | 0.258 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 2} | 11/17 (95% Wilson [0.413, 0.827]) | {'DRAG': '11/17 (95% Wilson [0.413, 0.827])'} |
| D1+ | 4.5 | 0.667 | False | 0.129 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 1} | 8/17 (95% Wilson [0.262, 0.69]) | {'DRAG': '8/17 (95% Wilson [0.262, 0.69])'} |
| D1+ | 5 | 0.741 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 6/17 (95% Wilson [0.173, 0.587]) | {'DRAG': '6/17 (95% Wilson [0.173, 0.587])'} |
| D1+ | 5.3 | 0.786 | True | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 6/17 (95% Wilson [0.173, 0.587]) | {'DRAG': '6/17 (95% Wilson [0.173, 0.587])'} |
| D1+ | 5.5 | 0.815 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 5/17 (95% Wilson [0.133, 0.531]) | {'DRAG': '5/17 (95% Wilson [0.133, 0.531])'} |
| D1+ | 6 | 0.89 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 1/17 (95% Wilson [0.0105, 0.27]) | {'DRAG': '1/17 (95% Wilson [0.0105, 0.27])'} |
| D2- | 1 | 0.47 | False | 3.35 | {'gettysburg_dj': 5, 'gettysburg_sa': 6, 'gettysburg_tg': 15} | 29/31 (95% Wilson [0.793, 0.982]) | {'PAUSE_DROPPED': '29/31 (95% Wilson [0.793, 0.982])'} |
| D2- | 1.5 | 0.705 | False | 1.55 | {'gettysburg_dj': 2, 'gettysburg_sa': 3, 'gettysburg_tg': 7} | 25/31 (95% Wilson [0.637, 0.908]) | {'PAUSE_DROPPED': '25/31 (95% Wilson [0.637, 0.908])'} |
| D2- | 2 | 0.94 | False | 0.516 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 4} | 14/31 (95% Wilson [0.292, 0.622]) | {'PAUSE_DROPPED': '14/31 (95% Wilson [0.292, 0.622])'} |
| D2- | 2.5 | 1.17 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 10/31 (95% Wilson [0.186, 0.499]) | {'PAUSE_DROPPED': '10/31 (95% Wilson [0.186, 0.499])'} |
| D2- | 3 | 1.41 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 7/31 (95% Wilson [0.114, 0.398]) | {'PAUSE_DROPPED': '7/31 (95% Wilson [0.114, 0.398])'} |
| D2- | 3.2 | 1.5 | True | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 6/31 (95% Wilson [0.0919, 0.363]) | {'PAUSE_DROPPED': '6/31 (95% Wilson [0.0919, 0.363])'} |
| D2- | 3.5 | 1.65 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 4/31 (95% Wilson [0.0513, 0.289]) | {'PAUSE_DROPPED': '4/31 (95% Wilson [0.0513, 0.289])'} |
| D2- | 4 | 1.88 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/31 (95% Wilson [0, 0.11]) | {'PAUSE_DROPPED': '0/31 (95% Wilson [0, 0.11])'} |
| D2- | 4.5 | 2.11 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/31 (95% Wilson [0, 0.11]) | {'PAUSE_DROPPED': '0/31 (95% Wilson [0, 0.11])'} |
| D2- | 5 | 2.35 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/31 (95% Wilson [0, 0.11]) | {'PAUSE_DROPPED': '0/31 (95% Wilson [0, 0.11])'} |
| D2- | 5.5 | 2.58 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/31 (95% Wilson [0, 0.11]) | {'PAUSE_DROPPED': '0/31 (95% Wilson [0, 0.11])'} |
| D2- | 6 | 2.82 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/31 (95% Wilson [0, 0.11]) | {'PAUSE_DROPPED': '0/31 (95% Wilson [0, 0.11])'} |
| D2+ | 1 | 0.37 | False | 0.902 | {'gettysburg_dj': 0, 'gettysburg_sa': 7, 'gettysburg_tg': 0} | 54/266 (95% Wilson [0.159, 0.255]) | {'HESITATION': '34/36 (95% Wilson [0.819, 0.985])', 'WORD_BY_WORD': '6/212 (95% Wilson [0.013, 0.0604])', 'PAUSE_INTRUSIVE': '14/18 (95% Wilson [0.548, 0.91])'} |
| D2+ | 1.5 | 0.555 | False | 0.387 | {'gettysburg_dj': 0, 'gettysburg_sa': 3, 'gettysburg_tg': 0} | 33/266 (95% Wilson [0.0897, 0.169]) | {'HESITATION': '19/36 (95% Wilson [0.37, 0.68])', 'WORD_BY_WORD': '0/212 (95% Wilson [0, 0.0178])', 'PAUSE_INTRUSIVE': '14/18 (95% Wilson [0.548, 0.91])'} |
| D2+ | 2 | 0.74 | False | 0.387 | {'gettysburg_dj': 0, 'gettysburg_sa': 3, 'gettysburg_tg': 0} | 31/266 (95% Wilson [0.0833, 0.161]) | {'HESITATION': '17/36 (95% Wilson [0.32, 0.63])', 'WORD_BY_WORD': '0/212 (95% Wilson [0, 0.0178])', 'PAUSE_INTRUSIVE': '14/18 (95% Wilson [0.548, 0.91])'} |
| D2+ | 2.5 | 0.925 | False | 0.387 | {'gettysburg_dj': 0, 'gettysburg_sa': 3, 'gettysburg_tg': 0} | 31/266 (95% Wilson [0.0833, 0.161]) | {'HESITATION': '17/36 (95% Wilson [0.32, 0.63])', 'WORD_BY_WORD': '0/212 (95% Wilson [0, 0.0178])', 'PAUSE_INTRUSIVE': '14/18 (95% Wilson [0.548, 0.91])'} |
| D2+ | 2.65 | 0.98 | True | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 27/266 (95% Wilson [0.0707, 0.144]) | {'HESITATION': '13/36 (95% Wilson [0.225, 0.524])', 'WORD_BY_WORD': '0/212 (95% Wilson [0, 0.0178])', 'PAUSE_INTRUSIVE': '14/18 (95% Wilson [0.548, 0.91])'} |
| D2+ | 3 | 1.11 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 11/266 (95% Wilson [0.0232, 0.0725]) | {'HESITATION': '0/36 (95% Wilson [0, 0.0964])', 'WORD_BY_WORD': '0/212 (95% Wilson [0, 0.0178])', 'PAUSE_INTRUSIVE': '11/18 (95% Wilson [0.386, 0.797])'} |
| D2+ | 3.5 | 1.29 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/266 (95% Wilson [0, 0.0142]) | {'HESITATION': '0/36 (95% Wilson [0, 0.0964])', 'WORD_BY_WORD': '0/212 (95% Wilson [0, 0.0178])', 'PAUSE_INTRUSIVE': '0/18 (95% Wilson [0, 0.176])'} |
| D2+ | 4 | 1.48 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/266 (95% Wilson [0, 0.0142]) | {'HESITATION': '0/36 (95% Wilson [0, 0.0964])', 'WORD_BY_WORD': '0/212 (95% Wilson [0, 0.0178])', 'PAUSE_INTRUSIVE': '0/18 (95% Wilson [0, 0.176])'} |
| D2+ | 4.5 | 1.67 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/266 (95% Wilson [0, 0.0142]) | {'HESITATION': '0/36 (95% Wilson [0, 0.0964])', 'WORD_BY_WORD': '0/212 (95% Wilson [0, 0.0178])', 'PAUSE_INTRUSIVE': '0/18 (95% Wilson [0, 0.176])'} |
| D2+ | 5 | 1.85 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/266 (95% Wilson [0, 0.0142]) | {'HESITATION': '0/36 (95% Wilson [0, 0.0964])', 'WORD_BY_WORD': '0/212 (95% Wilson [0, 0.0178])', 'PAUSE_INTRUSIVE': '0/18 (95% Wilson [0, 0.176])'} |
| D2+ | 5.5 | 2.04 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/266 (95% Wilson [0, 0.0142]) | {'HESITATION': '0/36 (95% Wilson [0, 0.0964])', 'WORD_BY_WORD': '0/212 (95% Wilson [0, 0.0178])', 'PAUSE_INTRUSIVE': '0/18 (95% Wilson [0, 0.176])'} |
| D2+ | 6 | 2.22 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/266 (95% Wilson [0, 0.0142]) | {'HESITATION': '0/36 (95% Wilson [0, 0.0964])', 'WORD_BY_WORD': '0/212 (95% Wilson [0, 0.0178])', 'PAUSE_INTRUSIVE': '0/18 (95% Wilson [0, 0.176])'} |
| D3- | 1 | 0.337 | False | 6.32 | {'gettysburg_dj': 17, 'gettysburg_sa': 15, 'gettysburg_tg': 17} | 17/18 (95% Wilson [0.742, 0.99]) | {'MONOTONE': '17/18 (95% Wilson [0.742, 0.99])'} |
| D3- | 1.5 | 0.506 | False | 2.71 | {'gettysburg_dj': 6, 'gettysburg_sa': 6, 'gettysburg_tg': 9} | 17/18 (95% Wilson [0.742, 0.99]) | {'MONOTONE': '17/18 (95% Wilson [0.742, 0.99])'} |
| D3- | 2 | 0.674 | False | 1.29 | {'gettysburg_dj': 4, 'gettysburg_sa': 3, 'gettysburg_tg': 3} | 17/18 (95% Wilson [0.742, 0.99]) | {'MONOTONE': '17/18 (95% Wilson [0.742, 0.99])'} |
| D3- | 2.5 | 0.843 | False | 0.516 | {'gettysburg_dj': 3, 'gettysburg_sa': 0, 'gettysburg_tg': 1} | 18/18 (95% Wilson [0.824, 1]) | {'MONOTONE': '18/18 (95% Wilson [0.824, 1])'} |
| D3- | 3 | 1.01 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 18/18 (95% Wilson [0.824, 1]) | {'MONOTONE': '18/18 (95% Wilson [0.824, 1])'} |
| D3- | 3.5 | 1.18 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 18/18 (95% Wilson [0.824, 1]) | {'MONOTONE': '18/18 (95% Wilson [0.824, 1])'} |
| D3- | 3.85 | 1.3 | True | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 17/18 (95% Wilson [0.742, 0.99]) | {'MONOTONE': '17/18 (95% Wilson [0.742, 0.99])'} |
| D3- | 4 | 1.35 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 17/18 (95% Wilson [0.742, 0.99]) | {'MONOTONE': '17/18 (95% Wilson [0.742, 0.99])'} |
| D3- | 4.5 | 1.52 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 14/18 (95% Wilson [0.548, 0.91]) | {'MONOTONE': '14/18 (95% Wilson [0.548, 0.91])'} |
| D3- | 5 | 1.69 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 7/18 (95% Wilson [0.203, 0.614]) | {'MONOTONE': '7/18 (95% Wilson [0.203, 0.614])'} |
| D3- | 5.5 | 1.85 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 4/18 (95% Wilson [0.09, 0.452]) | {'MONOTONE': '4/18 (95% Wilson [0.09, 0.452])'} |
| D3- | 6 | 2.02 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 2/18 (95% Wilson [0.031, 0.328]) | {'MONOTONE': '2/18 (95% Wilson [0.031, 0.328])'} |
| D5- | 1 | 2.46 | False | 9.41 | {'gettysburg_dj': 21, 'gettysburg_sa': 22, 'gettysburg_tg': 30} | 58/68 (95% Wilson [0.75, 0.918]) | {'LOW_EFFORT': '34/35 (95% Wilson [0.855, 0.995])', 'TRAILING_OFF': '9/15 (95% Wilson [0.357, 0.802])', 'FADE': '15/18 (95% Wilson [0.608, 0.942])'} |
| D5- | 1.5 | 3.69 | False | 5.8 | {'gettysburg_dj': 14, 'gettysburg_sa': 10, 'gettysburg_tg': 21} | 53/68 (95% Wilson [0.667, 0.862]) | {'LOW_EFFORT': '33/35 (95% Wilson [0.814, 0.984])', 'TRAILING_OFF': '5/15 (95% Wilson [0.152, 0.583])', 'FADE': '15/18 (95% Wilson [0.608, 0.942])'} |
| D5- | 2 | 4.92 | False | 3.48 | {'gettysburg_dj': 10, 'gettysburg_sa': 3, 'gettysburg_tg': 14} | 47/68 (95% Wilson [0.574, 0.788]) | {'LOW_EFFORT': '31/35 (95% Wilson [0.74, 0.955])', 'TRAILING_OFF': '1/15 (95% Wilson [0.0119, 0.298])', 'FADE': '15/18 (95% Wilson [0.608, 0.942])'} |
| D5- | 2.5 | 6.14 | False | 2.19 | {'gettysburg_dj': 4, 'gettysburg_sa': 2, 'gettysburg_tg': 11} | 45/68 (95% Wilson [0.543, 0.763]) | {'LOW_EFFORT': '30/35 (95% Wilson [0.706, 0.937])', 'TRAILING_OFF': '0/15 (95% Wilson [0, 0.204])', 'FADE': '15/18 (95% Wilson [0.608, 0.942])'} |
| D5- | 3 | 7.37 | False | 0.644 | {'gettysburg_dj': 2, 'gettysburg_sa': 2, 'gettysburg_tg': 1} | 41/68 (95% Wilson [0.484, 0.711]) | {'LOW_EFFORT': '26/35 (95% Wilson [0.579, 0.858])', 'TRAILING_OFF': '0/15 (95% Wilson [0, 0.204])', 'FADE': '15/18 (95% Wilson [0.608, 0.942])'} |
| D5- | 3.5 | 8.6 | False | 0.258 | {'gettysburg_dj': 2, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 36/68 (95% Wilson [0.412, 0.643]) | {'LOW_EFFORT': '21/35 (95% Wilson [0.436, 0.744])', 'TRAILING_OFF': '0/15 (95% Wilson [0, 0.204])', 'FADE': '15/18 (95% Wilson [0.608, 0.942])'} |
| D5- | 4 | 9.83 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 30/68 (95% Wilson [0.329, 0.559]) | {'LOW_EFFORT': '16/35 (95% Wilson [0.305, 0.618])', 'TRAILING_OFF': '0/15 (95% Wilson [0, 0.204])', 'FADE': '14/18 (95% Wilson [0.548, 0.91])'} |
| D5- | 4.1 | 10.1 | True | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 28/68 (95% Wilson [0.303, 0.53]) | {'LOW_EFFORT': '15/35 (95% Wilson [0.28, 0.591])', 'TRAILING_OFF': '0/15 (95% Wilson [0, 0.204])', 'FADE': '13/18 (95% Wilson [0.491, 0.875])'} |
| D5- | 4.5 | 11.1 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 25/68 (95% Wilson [0.263, 0.486]) | {'LOW_EFFORT': '12/35 (95% Wilson [0.208, 0.508])', 'TRAILING_OFF': '0/15 (95% Wilson [0, 0.204])', 'FADE': '13/18 (95% Wilson [0.491, 0.875])'} |
| D5- | 5 | 12.3 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 18/68 (95% Wilson [0.174, 0.38]) | {'LOW_EFFORT': '6/35 (95% Wilson [0.081, 0.327])', 'TRAILING_OFF': '0/15 (95% Wilson [0, 0.204])', 'FADE': '12/18 (95% Wilson [0.437, 0.837])'} |
| D5- | 5.5 | 13.5 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 9/68 (95% Wilson [0.0712, 0.233]) | {'LOW_EFFORT': '4/35 (95% Wilson [0.0454, 0.26])', 'TRAILING_OFF': '0/15 (95% Wilson [0, 0.204])', 'FADE': '5/18 (95% Wilson [0.125, 0.509])'} |
| D5- | 6 | 14.7 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 5/68 (95% Wilson [0.0318, 0.161]) | {'LOW_EFFORT': '1/35 (95% Wilson [0.00506, 0.145])', 'TRAILING_OFF': '0/15 (95% Wilson [0, 0.204])', 'FADE': '4/18 (95% Wilson [0.09, 0.452])'} |

## Reproducibility

Two analyze() runs on eisenhower_farewell_1961__extra_L3A: identical = True

