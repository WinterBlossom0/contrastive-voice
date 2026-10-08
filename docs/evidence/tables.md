# Evaluation tables

Detector config 3af9697668e4a581b8c14fb4d242c8b89578de59ae551b40a3e1930ac104366d. Splits train, val; alignment on cuda. Regimes are never pooled and train is never pooled with validation or test; counts are k of n; exposure beside every rate.

## Sample sizes (evaluated single-level clips)

| split | speakers | clips | type | level | trials |
|---|---|---|---|---|---|
| train | 5 | 30 | RUSH | 1 | 5 |
| train | 5 | 30 | RUSH | 2 | 5 |
| train | 5 | 30 | RUSH | 3 | 5 |
| train | 5 | 30 | DRAG | 1 | 5 |
| train | 5 | 30 | DRAG | 2 | 5 |
| train | 5 | 30 | DRAG | 3 | 5 |
| train | 5 | 30 | PAUSE_DROPPED | 1 | 5 |
| train | 5 | 30 | PAUSE_DROPPED | 2 | 5 |
| train | 5 | 30 | PAUSE_DROPPED | 3 | 5 |
| train | 5 | 30 | PAUSE_INTRUSIVE | 1 | 5 |
| train | 5 | 30 | PAUSE_INTRUSIVE | 2 | 5 |
| train | 5 | 30 | PAUSE_INTRUSIVE | 3 | 5 |
| train | 5 | 30 | MONOTONE | 1 | 5 |
| train | 5 | 30 | MONOTONE | 2 | 5 |
| train | 5 | 30 | MONOTONE | 3 | 5 |
| train | 5 | 30 | DEEMPHASIS | 1 | 5 |
| train | 5 | 30 | DEEMPHASIS | 2 | 5 |
| train | 5 | 30 | DEEMPHASIS | 3 | 5 |
| train | 5 | 30 | FADE | 1 | 5 |
| train | 5 | 30 | FADE | 2 | 5 |
| train | 5 | 30 | FADE | 3 | 5 |
| train | 5 | 30 | MUMBLE | 1 | 5 |
| train | 5 | 30 | MUMBLE | 2 | 5 |
| train | 5 | 30 | MUMBLE | 3 | 5 |
| val | 2 | 12 | RUSH | 1 | 2 |
| val | 2 | 12 | RUSH | 2 | 2 |
| val | 2 | 12 | RUSH | 3 | 2 |
| val | 2 | 12 | DRAG | 1 | 2 |
| val | 2 | 12 | DRAG | 2 | 2 |
| val | 2 | 12 | DRAG | 3 | 2 |
| val | 2 | 12 | PAUSE_DROPPED | 1 | 2 |
| val | 2 | 12 | PAUSE_DROPPED | 2 | 2 |
| val | 2 | 12 | PAUSE_DROPPED | 3 | 2 |
| val | 2 | 12 | PAUSE_INTRUSIVE | 1 | 2 |
| val | 2 | 12 | PAUSE_INTRUSIVE | 2 | 2 |
| val | 2 | 12 | PAUSE_INTRUSIVE | 3 | 2 |
| val | 2 | 12 | MONOTONE | 1 | 2 |
| val | 2 | 12 | MONOTONE | 2 | 2 |
| val | 2 | 12 | MONOTONE | 3 | 2 |
| val | 2 | 12 | DEEMPHASIS | 1 | 2 |
| val | 2 | 12 | DEEMPHASIS | 2 | 2 |
| val | 2 | 12 | DEEMPHASIS | 3 | 2 |
| val | 2 | 12 | FADE | 1 | 2 |
| val | 2 | 12 | FADE | 2 | 2 |
| val | 2 | 12 | FADE | 3 | 2 |
| val | 2 | 12 | MUMBLE | 1 | 2 |
| val | 2 | 12 | MUMBLE | 2 | 2 |
| val | 2 | 12 | MUMBLE | 3 | 2 |

## Expectation table (fixed before evaluation)

| level | R1 same performance | R2 different speaker |
|---|---|---|
| 1 | marginal: detection near or below 50 %; clip score >= 90 | must stay silent |
| 2 | flagged | marginal |
| 3 | flagged | flagged for pace, pauses, pitch, volume; D4 and D6 not scored |

## Event F1 by dimension and split (all predictions counted first, whole-clip flags included as false; windows IoU >= 0.5, events by labelled index or time)

| accounting | levels | split | dimension/sign | TP | FP | FN | precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| all predictions counted | headline (L2+L3) | train | D1+ | 10 | 1 | 0 | 0.909 | 1 | 0.952 |
| all predictions counted | headline (L2+L3) | train | D1- | 8 | 6 | 2 | 0.571 | 0.8 | 0.667 |
| all predictions counted | headline (L2+L3) | train | D2+ | 10 | 0 | 0 | 1 | 1 | 1 |
| all predictions counted | headline (L2+L3) | train | D2- | 10 | 0 | 0 | 1 | 1 | 1 |
| all predictions counted | headline (L2+L3) | train | D3- | 10 | 0 | 0 | 1 | 1 | 1 |
| all predictions counted | headline (L2+L3) | train | D4- | 10 | 1 | 0 | 0.909 | 1 | 0.952 |
| all predictions counted | headline (L2+L3) | train | D5- | 10 | 4 | 0 | 0.714 | 1 | 0.833 |
| all predictions counted | headline (L2+L3) | train | D6- | 10 | 0 | 0 | 1 | 1 | 1 |
| all predictions counted | headline (L2+L3) | train | all | 78 | 12 | 2 | 0.867 | 0.975 | 0.918 |
| all predictions counted | headline (L2+L3) | val | D1+ | 4 | 1 | 0 | 0.8 | 1 | 0.889 |
| all predictions counted | headline (L2+L3) | val | D1- | 4 | 0 | 0 | 1 | 1 | 1 |
| all predictions counted | headline (L2+L3) | val | D2+ | 4 | 2 | 0 | 0.667 | 1 | 0.8 |
| all predictions counted | headline (L2+L3) | val | D2- | 4 | 1 | 0 | 0.8 | 1 | 0.889 |
| all predictions counted | headline (L2+L3) | val | D3- | 4 | 2 | 0 | 0.667 | 1 | 0.8 |
| all predictions counted | headline (L2+L3) | val | D4- | 4 | 3 | 0 | 0.571 | 1 | 0.727 |
| all predictions counted | headline (L2+L3) | val | D5- | 2 | 2 | 2 | 0.5 | 0.5 | 0.5 |
| all predictions counted | headline (L2+L3) | val | D6- | 4 | 0 | 0 | 1 | 1 | 1 |
| all predictions counted | headline (L2+L3) | val | all | 30 | 11 | 2 | 0.732 | 0.938 | 0.822 |
| all predictions counted | sensitivity (L1) | train | D1+ | 5 | 0 | 0 | 1 | 1 | 1 |
| all predictions counted | sensitivity (L1) | train | D1- | 4 | 1 | 1 | 0.8 | 0.8 | 0.8 |
| all predictions counted | sensitivity (L1) | train | D2+ | 5 | 0 | 0 | 1 | 1 | 1 |
| all predictions counted | sensitivity (L1) | train | D2- | 5 | 0 | 0 | 1 | 1 | 1 |
| all predictions counted | sensitivity (L1) | train | D3- | 3 | 0 | 2 | 1 | 0.6 | 0.75 |
| all predictions counted | sensitivity (L1) | train | D4- | 1 | 0 | 4 | 1 | 0.2 | 0.333 |
| all predictions counted | sensitivity (L1) | train | D5- | 2 | 1 | 3 | 0.667 | 0.4 | 0.5 |
| all predictions counted | sensitivity (L1) | train | D6- | 0 | 0 | 5 |  | 0 | 0 |
| all predictions counted | sensitivity (L1) | train | all | 25 | 2 | 15 | 0.926 | 0.625 | 0.746 |
| all predictions counted | sensitivity (L1) | val | D1+ | 1 | 0 | 1 | 1 | 0.5 | 0.667 |
| all predictions counted | sensitivity (L1) | val | D1- | 1 | 1 | 1 | 0.5 | 0.5 | 0.5 |
| all predictions counted | sensitivity (L1) | val | D2+ | 2 | 0 | 0 | 1 | 1 | 1 |
| all predictions counted | sensitivity (L1) | val | D2- | 2 | 0 | 0 | 1 | 1 | 1 |
| all predictions counted | sensitivity (L1) | val | D3- | 2 | 0 | 0 | 1 | 1 | 1 |
| all predictions counted | sensitivity (L1) | val | D4- | 0 | 0 | 2 |  | 0 | 0 |
| all predictions counted | sensitivity (L1) | val | D5- | 0 | 0 | 2 |  | 0 | 0 |
| all predictions counted | sensitivity (L1) | val | D6- | 0 | 0 | 2 |  | 0 | 0 |
| all predictions counted | sensitivity (L1) | val | all | 8 | 1 | 8 | 0.889 | 0.5 | 0.64 |
| secondary firings exempt | headline (L2+L3) | train | D1+ | 10 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | headline (L2+L3) | train | D1- | 8 | 6 | 2 | 0.571 | 0.8 | 0.667 |
| secondary firings exempt | headline (L2+L3) | train | D2+ | 10 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | headline (L2+L3) | train | D2- | 10 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | headline (L2+L3) | train | D3- | 10 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | headline (L2+L3) | train | D4- | 10 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | headline (L2+L3) | train | D5- | 10 | 2 | 0 | 0.833 | 1 | 0.909 |
| secondary firings exempt | headline (L2+L3) | train | D6- | 10 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | headline (L2+L3) | train | all | 78 | 8 | 2 | 0.907 | 0.975 | 0.94 |
| secondary firings exempt | headline (L2+L3) | val | D1+ | 4 | 1 | 0 | 0.8 | 1 | 0.889 |
| secondary firings exempt | headline (L2+L3) | val | D1- | 4 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | headline (L2+L3) | val | D2+ | 4 | 2 | 0 | 0.667 | 1 | 0.8 |
| secondary firings exempt | headline (L2+L3) | val | D2- | 4 | 1 | 0 | 0.8 | 1 | 0.889 |
| secondary firings exempt | headline (L2+L3) | val | D3- | 4 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | headline (L2+L3) | val | D4- | 4 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | headline (L2+L3) | val | D5- | 2 | 2 | 2 | 0.5 | 0.5 | 0.5 |
| secondary firings exempt | headline (L2+L3) | val | D6- | 4 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | headline (L2+L3) | val | all | 30 | 6 | 2 | 0.833 | 0.938 | 0.882 |
| secondary firings exempt | sensitivity (L1) | train | D1+ | 5 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | sensitivity (L1) | train | D1- | 4 | 1 | 1 | 0.8 | 0.8 | 0.8 |
| secondary firings exempt | sensitivity (L1) | train | D2+ | 5 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | sensitivity (L1) | train | D2- | 5 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | sensitivity (L1) | train | D3- | 3 | 0 | 2 | 1 | 0.6 | 0.75 |
| secondary firings exempt | sensitivity (L1) | train | D4- | 1 | 0 | 4 | 1 | 0.2 | 0.333 |
| secondary firings exempt | sensitivity (L1) | train | D5- | 2 | 1 | 3 | 0.667 | 0.4 | 0.5 |
| secondary firings exempt | sensitivity (L1) | train | D6- | 0 | 0 | 5 |  | 0 | 0 |
| secondary firings exempt | sensitivity (L1) | train | all | 25 | 2 | 15 | 0.926 | 0.625 | 0.746 |
| secondary firings exempt | sensitivity (L1) | val | D1+ | 1 | 0 | 1 | 1 | 0.5 | 0.667 |
| secondary firings exempt | sensitivity (L1) | val | D1- | 1 | 1 | 1 | 0.5 | 0.5 | 0.5 |
| secondary firings exempt | sensitivity (L1) | val | D2+ | 2 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | sensitivity (L1) | val | D2- | 2 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | sensitivity (L1) | val | D3- | 2 | 0 | 0 | 1 | 1 | 1 |
| secondary firings exempt | sensitivity (L1) | val | D4- | 0 | 0 | 2 |  | 0 | 0 |
| secondary firings exempt | sensitivity (L1) | val | D5- | 0 | 0 | 2 |  | 0 | 0 |
| secondary firings exempt | sensitivity (L1) | val | D6- | 0 | 0 | 2 |  | 0 | 0 |
| secondary firings exempt | sensitivity (L1) | val | all | 8 | 1 | 8 | 0.889 | 0.5 | 0.64 |

## Overlap view (a flaw counts as found when a flag of its dimension lies on it)

| levels | split | flaws touched | flaws | flags on flaw | all local flags | overlap recall | flag precision |
|---|---|---|---|---|---|---|---|
| headline (L2+L3) | train | 80 | 80 | 81 | 90 | 1 | 0.9 |
| headline (L2+L3) | val | 32 | 32 | 32 | 41 | 1 | 0.78 |
| sensitivity (L1) | train | 26 | 40 | 26 | 27 | 0.65 | 0.963 |
| sensitivity (L1) | val | 9 | 16 | 9 | 9 | 0.562 | 1 |

## Per speech, k of n (L2 + L3)

| speech | split | clip | level | detected k | of n | false regions (secondary firings exempt) |
|---|---|---|---|---|---|---|
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__single_L2A | 2 | 3 | 4 | 1 |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__single_L2B | 2 | 4 | 4 | 0 |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__single_L3A | 3 | 4 | 4 | 4 |
| eisenhower_farewell_1961 | val | eisenhower_farewell_1961__single_L3B | 3 | 4 | 4 | 0 |
| gwbush_911_2001 | train | gwbush_911_2001__single_L2A | 2 | 4 | 4 | 0 |
| gwbush_911_2001 | train | gwbush_911_2001__single_L2B | 2 | 4 | 4 | 0 |
| gwbush_911_2001 | train | gwbush_911_2001__single_L3A | 3 | 3 | 4 | 2 |
| gwbush_911_2001 | train | gwbush_911_2001__single_L3B | 3 | 4 | 4 | 0 |
| harris_uncsw_2021 | train | harris_uncsw_2021__single_L2A | 2 | 4 | 4 | 0 |
| harris_uncsw_2021 | train | harris_uncsw_2021__single_L2B | 2 | 4 | 4 | 0 |
| harris_uncsw_2021 | train | harris_uncsw_2021__single_L3A | 3 | 4 | 4 | 1 |
| harris_uncsw_2021 | train | harris_uncsw_2021__single_L3B | 3 | 4 | 4 | 0 |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__single_L2A | 2 | 4 | 4 | 0 |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__single_L2B | 2 | 4 | 4 | 0 |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__single_L3A | 3 | 4 | 4 | 0 |
| hclinton_tomorrow_2010 | train | hclinton_tomorrow_2010__single_L3B | 3 | 4 | 4 | 0 |
| lbush_radio_2001 | val | lbush_radio_2001__single_L2A | 2 | 3 | 4 | 1 |
| lbush_radio_2001 | val | lbush_radio_2001__single_L2B | 2 | 4 | 4 | 0 |
| lbush_radio_2001 | val | lbush_radio_2001__single_L3A | 3 | 4 | 4 | 0 |
| lbush_radio_2001 | val | lbush_radio_2001__single_L3B | 3 | 4 | 4 | 0 |
| obama_weekly_2009 | train | obama_weekly_2009__single_L2A | 2 | 4 | 4 | 0 |
| obama_weekly_2009 | train | obama_weekly_2009__single_L2B | 2 | 4 | 4 | 1 |
| obama_weekly_2009 | train | obama_weekly_2009__single_L3A | 3 | 3 | 4 | 2 |
| obama_weekly_2009 | train | obama_weekly_2009__single_L3B | 3 | 4 | 4 | 1 |
| reagan_farewell_1989 | train | reagan_farewell_1989__single_L2A | 2 | 4 | 4 | 0 |
| reagan_farewell_1989 | train | reagan_farewell_1989__single_L2B | 2 | 4 | 4 | 0 |
| reagan_farewell_1989 | train | reagan_farewell_1989__single_L3A | 3 | 4 | 4 | 1 |
| reagan_farewell_1989 | train | reagan_farewell_1989__single_L3B | 3 | 4 | 4 | 0 |

## Whole-clip flags on flawed clips

| split | whole-clip flags on flawed clips | clips |
|---|---|---|
| train | 0 |  |
| val | 0 |  |

## Pause localisation error (matched boundary events)

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
| train | obama_weekly_2009__single_L2A | PAUSE_DROPPED | 65.5 | -68.5 |
| train | obama_weekly_2009__single_L2B | PAUSE_INTRUSIVE | 247 | -2.7 |
| train | obama_weekly_2009__single_L3A | PAUSE_DROPPED | 21.1 | -38.9 |
| train | obama_weekly_2009__single_L3B | PAUSE_INTRUSIVE | 10 | 0 |
| train | reagan_farewell_1989__single_L2A | PAUSE_DROPPED | 70.4 | -41.6 |
| train | reagan_farewell_1989__single_L2B | PAUSE_INTRUSIVE | 12 | 2 |
| train | reagan_farewell_1989__single_L3A | PAUSE_DROPPED | 5.1 | -54.9 |
| train | reagan_farewell_1989__single_L3B | PAUSE_INTRUSIVE | 10 | 0 |

## Onset / offset absolute error of matched regions (FADE late onset is expected)

| split | type | n matched | onset median (ms) | onset P90 (ms) | offset median (ms) | offset P90 (ms) |
|---|---|---|---|---|---|---|
| train | DRAG | 10 | 79 | 275 | 172 | 493 |
| train | FADE | 10 | 101 | 342 | 69.5 | 294 |
| train | MONOTONE | 10 | 328 | 971 | 85 | 287 |
| train | MUMBLE | 10 | 202 | 461 | 260 | 334 |
| train | RUSH | 8 | 72 | 136 | 106 | 290 |
| val | DRAG | 4 | 65.6 | 83.4 | 206 | 530 |
| val | FADE | 2 | 495 | 587 | 900 | 1.4e+03 |
| val | MONOTONE | 4 | 375 | 964 | 415 | 964 |
| val | MUMBLE | 4 | 322 | 369 | 163 | 630 |
| val | RUSH | 4 | 20 | 307 | 11.5 | 59.3 |

## Detection versus physical magnitude, with the expectation beside it

| type | level | magnitude | train k/n | val k/n | test k/n | expected (R1) |
|---|---|---|---|---|---|---|
| RUSH | 1 | 1.2 | 4/5 | 1/2 |  | marginal: detection near or below 50 %; clip score >= 90 |
| RUSH | 2 | 1.45 | 5/5 | 2/2 |  | flagged |
| RUSH | 3 | 1.9 | 3/5 | 2/2 |  | flagged |
| DRAG | 1 | 1.2 | 5/5 | 1/2 |  | marginal: detection near or below 50 %; clip score >= 90 |
| DRAG | 2 | 1.45 | 5/5 | 2/2 |  | flagged |
| DRAG | 3 | 1.9 | 5/5 | 2/2 |  | flagged |
| PAUSE_DROPPED | 1 | 0.4 | 5/5 | 2/2 |  | marginal: detection near or below 50 %; clip score >= 90 |
| PAUSE_DROPPED | 2 | 0.2 | 5/5 | 2/2 |  | flagged |
| PAUSE_DROPPED | 3 | 0 | 5/5 | 2/2 |  | flagged |
| PAUSE_INTRUSIVE | 1 | 0.35 | 5/5 | 2/2 |  | marginal: detection near or below 50 %; clip score >= 90 |
| PAUSE_INTRUSIVE | 2 | 0.6 | 5/5 | 2/2 |  | flagged |
| PAUSE_INTRUSIVE | 3 | 1.2 | 5/5 | 2/2 |  | flagged |
| MONOTONE | 1 | 0.5 | 3/5 | 2/2 |  | marginal: detection near or below 50 %; clip score >= 90 |
| MONOTONE | 2 | 0.25 | 5/5 | 2/2 |  | flagged |
| MONOTONE | 3 | 0 | 5/5 | 2/2 |  | flagged |
| DEEMPHASIS | 1 | 0.5 | 1/5 | 0/2 |  | marginal: detection near or below 50 %; clip score >= 90 |
| DEEMPHASIS | 2 | 0.75 | 5/5 | 2/2 |  | flagged |
| DEEMPHASIS | 3 | 1 | 5/5 | 2/2 |  | flagged |
| FADE | 1 | 4 | 2/5 | 0/2 |  | marginal: detection near or below 50 %; clip score >= 90 |
| FADE | 2 | 8 | 5/5 | 0/2 |  | flagged |
| FADE | 3 | 14 | 5/5 | 2/2 |  | flagged |
| MUMBLE | 1 | 0.3 | 0/5 | 0/2 |  | marginal: detection near or below 50 %; clip score >= 90 |
| MUMBLE | 2 | 0.6 | 5/5 | 2/2 |  | flagged |
| MUMBLE | 3 | 1 | 5/5 | 2/2 |  | flagged |

## Activation matrix

Split train:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 |
|---|---|---|---|---|---|---|
| D1 | 21 | 0 | 0 | 0 | 0 | 0 |
| D2 | 1 | 20 | 0 | 0 | 2 | 0 |
| D3 | 0 | 0 | 10 | 0 | 1 | 0 |
| D4 | 0 | 0 | 0 | 10 | 2 | 0 |
| D5 | 3 | 0 | 0 | 1 | 10 | 0 |
| D6 | 0 | 0 | 0 | 0 | 2 | 10 |

Split val:

| injected \ fired | D1 | D2 | D3 | D4 | D5 | D6 |
|---|---|---|---|---|---|---|
| D1 | 8 | 0 | 0 | 0 | 0 | 0 |
| D2 | 0 | 8 | 1 | 0 | 0 | 1 |
| D3 | 0 | 0 | 4 | 1 | 0 | 0 |
| D4 | 0 | 0 | 2 | 4 | 0 | 0 |
| D5 | 1 | 3 | 0 | 2 | 4 | 0 |
| D6 | 0 | 0 | 0 | 0 | 0 | 4 |

## False flags per minute on nulls

| population | false flags | exposure (min) | observed per comparison-minute | rule of three: assuming independent minutes (not established) |
|---|---|---|---|---|
| R1 val: identity + 5 placebo seeds (12 variants; 2 source recordings / readers) | 0 | 5.93 | 0 | 0.506 |
| R2 check-reader pairs, not fitted but seen during the detector redesign (18 ordered pairs; 9 recordings / readers) | 8 | 7.76 | 1.03 |  |
| R2 orator-reference row: Greenman vs Reagan (2 recordings / readers; never fitted) | 1 | 0.54 | 1.87 |  |

Reader-level R2 null counts:

| participant reader | comparisons | comparison-minutes | flags | by flag key |
|---|---|---|---|---|
| gettysburg_dj | 6 | 2.29 | 1 | {'D1-': 1} |
| gettysburg_sa | 6 | 3.02 | 4 | {'D1-': 1, 'D2+': 3} |
| gettysburg_tg | 6 | 2.45 | 3 | {'D1-': 1, 'D1+': 2} |

## Score by rung of the bad spectrum (R1)

| split | rung | clips | lowest score | median score | highest score |
|---|---|---|---|---|---|
| train | identity | 5 | 100 | 100 | 100 |
| train | G1 | 5 | 99.9 | 99.9 | 100 |
| train | level 1 (four edits) | 10 | 97.3 | 99.3 | 99.7 |
| train | G3 | 5 | 96.5 | 96.9 | 98.8 |
| train | level 2 (four edits) | 10 | 90.9 | 95.1 | 96.5 |
| train | level 3 (four edits) | 10 | 83.2 | 89 | 90.6 |
| train | G5 | 5 | 24.1 | 45.8 | 49.9 |
| val | identity | 2 | 100 | 100 | 100 |
| val | G1 | 2 | 99.7 | 99.8 | 100 |
| val | level 1 (four edits) | 4 | 98.5 | 99.4 | 99.9 |
| val | G3 | 2 | 96.6 | 97.3 | 98 |
| val | level 2 (four edits) | 4 | 93.4 | 93.5 | 95.6 |
| val | level 3 (four edits) | 4 | 82.5 | 85 | 89.6 |
| val | G5 | 2 | 42.9 | 43.9 | 44.8 |

Score gates (violations):

| split | identity below 100 | level-1 clip below 90 | G5 above 50 | ladder G1 >= G3 >= G5 broken |
|---|---|---|---|---|
| train | 0 | 0 | 0 | 0 |
| val | 0 | 0 | 0 | 0 |

## Cross-speaker flawed pairs, flawed minus clean (R2)

| reader group | new flags | worsened | pre-existing | away-edits | away-edits detected | away-edits flagged or among the 5 listed differences | repair controls | controls flagged | unmeasurable |
|---|---|---|---|---|---|---|---|---|---|
| check | 97 | 6 | 22 | 133 | 88 | 109 | 11 | 0 | 0 |
| train | 5 | 2 | 2 | 8 | 5 | 5 | 0 | 0 | 0 |

Away-edits by type and level (a check reader's clip counts once per calibration reference):

| reader group | type | level | detected | flagged or among the 5 listed differences | away-edits |
|---|---|---|---|---|---|
| check | DRAG | 3 | 14 | 16 | 17 |
| check | FADE | 3 | 13 | 18 | 18 |
| check | MONOTONE | 3 | 18 | 18 | 18 |
| check | PAUSE_DROPPED | 2 | 3 | 6 | 14 |
| check | PAUSE_DROPPED | 3 | 6 | 9 | 17 |
| check | PAUSE_INTRUSIVE | 3 | 14 | 16 | 18 |
| check | RUSH | 2 | 3 | 8 | 13 |
| check | RUSH | 3 | 17 | 18 | 18 |
| train | DRAG | 3 | 1 | 1 | 1 |
| train | FADE | 3 | 1 | 1 | 1 |
| train | MONOTONE | 3 | 1 | 1 | 1 |
| train | PAUSE_DROPPED | 2 | 0 | 0 | 1 |
| train | PAUSE_DROPPED | 3 | 0 | 0 | 1 |
| train | PAUSE_INTRUSIVE | 3 | 1 | 1 | 1 |
| train | RUSH | 2 | 0 | 0 | 1 |
| train | RUSH | 3 | 1 | 1 | 1 |

Per clip and reference:

| clip | reference | reader group | new flags | worsened | pre-existing | away-edits | away-edits detected | away-edits flagged or among the 5 listed differences | repair controls | controls flagged | unmeasurable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gettysburg_dj__x1_L2 | gettysburg_amb | check | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| gettysburg_dj__x1_L2 | gettysburg_dl | check | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__x1_L2 | gettysburg_fb | check | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| gettysburg_dj__x1_L2 | gettysburg_jn | check | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__x1_L2 | gettysburg_pc | check | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_dj__x1_L2 | gettysburg_wt | check | 2 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dj__x2_L3 | gettysburg_amb | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x2_L3 | gettysburg_dl | check | 2 | 0 | 1 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x2_L3 | gettysburg_fb | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x2_L3 | gettysburg_jn | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x2_L3 | gettysburg_pc | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x2_L3 | gettysburg_wt | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x3_L3 | gettysburg_amb | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x3_L3 | gettysburg_dl | check | 1 | 1 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x3_L3 | gettysburg_fb | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x3_L3 | gettysburg_jn | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x3_L3 | gettysburg_pc | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x3_L3 | gettysburg_wt | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x4_L3 | gettysburg_amb | check | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_dj__x4_L3 | gettysburg_dl | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x4_L3 | gettysburg_fb | check | 2 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x4_L3 | gettysburg_jn | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x4_L3 | gettysburg_pc | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_dj__x4_L3 | gettysburg_wt | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x1_L2 | gettysburg_amb | check | 1 | 0 | 2 | 1 | 0 | 1 | 1 | 0 | 0 |
| gettysburg_sa__x1_L2 | gettysburg_dl | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x1_L2 | gettysburg_fb | check | 1 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x1_L2 | gettysburg_jn | check | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_sa__x1_L2 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x1_L2 | gettysburg_wt | check | 0 | 0 | 1 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x2_L3 | gettysburg_amb | check | 2 | 1 | 1 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x2_L3 | gettysburg_dl | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x2_L3 | gettysburg_fb | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x2_L3 | gettysburg_jn | check | 2 | 1 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x2_L3 | gettysburg_pc | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x2_L3 | gettysburg_wt | check | 2 | 1 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x3_L3 | gettysburg_amb | check | 1 | 0 | 2 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x3_L3 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x3_L3 | gettysburg_fb | check | 3 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x3_L3 | gettysburg_jn | check | 1 | 0 | 1 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x3_L3 | gettysburg_pc | check | 3 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x3_L3 | gettysburg_wt | check | 1 | 0 | 1 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x4_L3 | gettysburg_amb | check | 0 | 0 | 2 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x4_L3 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x4_L3 | gettysburg_fb | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x4_L3 | gettysburg_jn | check | 1 | 0 | 1 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_sa__x4_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_sa__x4_L3 | gettysburg_wt | check | 2 | 0 | 1 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x1_L2 | gettysburg_amb | check | 1 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x1_L2 | gettysburg_dl | check | 0 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x1_L2 | gettysburg_fb | check | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| gettysburg_tg__x1_L2 | gettysburg_jn | check | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x1_L2 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x1_L2 | gettysburg_wt | check | 1 | 1 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x2_L3 | gettysburg_amb | check | 2 | 0 | 1 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x2_L3 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x2_L3 | gettysburg_fb | check | 2 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| gettysburg_tg__x2_L3 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x2_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x2_L3 | gettysburg_wt | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x3_L3 | gettysburg_amb | check | 2 | 0 | 1 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x3_L3 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x3_L3 | gettysburg_fb | check | 2 | 0 | 1 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x3_L3 | gettysburg_jn | check | 2 | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x3_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x3_L3 | gettysburg_wt | check | 1 | 0 | 1 | 2 | 1 | 2 | 0 | 0 | 0 |
| gettysburg_tg__x4_L3 | gettysburg_amb | check | 1 | 0 | 1 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x4_L3 | gettysburg_dl | check | 1 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x4_L3 | gettysburg_fb | check | 1 | 0 | 1 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x4_L3 | gettysburg_jn | check | 1 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x4_L3 | gettysburg_pc | check | 1 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |
| gettysburg_tg__x4_L3 | gettysburg_wt | check | 2 | 0 | 1 | 2 | 2 | 2 | 0 | 0 | 0 |
| greenman_reagan__x1_L2 | reagan_farewell_1989 | train | 0 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| greenman_reagan__x2_L3 | reagan_farewell_1989 | train | 2 | 0 | 1 | 2 | 2 | 2 | 0 | 0 | 0 |
| greenman_reagan__x3_L3 | reagan_farewell_1989 | train | 2 | 0 | 1 | 2 | 2 | 2 | 0 | 0 | 0 |
| greenman_reagan__x4_L3 | reagan_farewell_1989 | train | 1 | 1 | 0 | 2 | 1 | 1 | 0 | 0 | 0 |

## Cross-speaker whole-clip detection (R2): graded whole-passage edits and botched readings

Check readers against every calibration reader, by rung (whole-clip flag of the edited dimension; botched: both flags):

| rung | level | magnitude | whole-clip flag raised | pairs | median score |
|---|---|---|---|---|---|
| unedited |  |  | 0 | 18 | 100 |
| whole-passage RUSH | 1 | 1.2 | 2 | 18 | 100 |
| whole-passage RUSH | 2 | 1.45 | 8 | 18 | 94.1 |
| whole-passage RUSH | 3 | 1.9 | 18 | 18 | 75 |
| whole-passage MONOTONE | 1 | 0.5 | 2 | 18 | 99.9 |
| whole-passage MONOTONE | 2 | 0.25 | 14 | 18 | 89.2 |
| whole-passage MONOTONE | 3 | 0 | 18 | 18 | 75 |
| botched (G5) |  |  | 18 | 18 | 49.4 |

| reader group | pairs | overall tempo flagged | overall pitch range flagged | median score unedited | median score botched | highest score botched |
|---|---|---|---|---|---|---|
| check | 18 | 18 | 18 | 100 | 49.4 | 67 |
| train | 1 | 1 | 1 | 99.9 | 61.3 | 61.3 |

| clip | reference | score unedited | flags unedited | score botched | flags botched |
|---|---|---|---|---|---|
| gettysburg_dj__G5 | gettysburg_amb | 100 |  | 50 | D1- whole clip, D3- whole clip |
| gettysburg_dj__G5 | gettysburg_dl | 99.9 | D1- | 48.7 | D2-, D2-, D1- whole clip, D3- whole clip |
| gettysburg_dj__G5 | gettysburg_fb | 100 |  | 49.2 | D5-, D1- whole clip, D3- whole clip |
| gettysburg_dj__G5 | gettysburg_jn | 100 |  | 49.6 | D2-, D1- whole clip, D3- whole clip |
| gettysburg_dj__G5 | gettysburg_pc | 100 |  | 47.9 | D2-, D5-, D1- whole clip, D3- whole clip |
| gettysburg_dj__G5 | gettysburg_wt | 100 |  | 41.4 | D2-, D2-, D2-, D1+, D1- whole clip, D3- whole clip |
| gettysburg_sa__G5 | gettysburg_amb | 91.4 | D1-, D2+ | 49.8 | D5-, D5-, D1- whole clip, D3- whole clip |
| gettysburg_sa__G5 | gettysburg_dl | 100 |  | 48.6 | D5-, D2-, D5-, D2-, D1- whole clip, D3- whole clip |
| gettysburg_sa__G5 | gettysburg_fb | 100 |  | 62.6 | D5-, D1- whole clip, D3- whole clip |
| gettysburg_sa__G5 | gettysburg_jn | 94.7 | D2+ | 67 | D2-, D5-, D1- whole clip, D3- whole clip |
| gettysburg_sa__G5 | gettysburg_pc | 100 |  | 48.2 | D2-, D5-, D1- whole clip, D3- whole clip |
| gettysburg_sa__G5 | gettysburg_wt | 92.7 | D2+ | 41.5 | D2-, D2-, D2-, D1- whole clip, D3- whole clip |
| gettysburg_tg__G5 | gettysburg_amb | 99.8 | D1- | 50 | D1- whole clip, D3- whole clip |
| gettysburg_tg__G5 | gettysburg_dl | 100 |  | 49.7 | D2-, D1- whole clip, D3- whole clip |
| gettysburg_tg__G5 | gettysburg_fb | 99.7 | D1+ | 50 | D1+, D1- whole clip, D3- whole clip |
| gettysburg_tg__G5 | gettysburg_jn | 100 |  | 53.9 | D2-, D5-, D1- whole clip, D3- whole clip |
| gettysburg_tg__G5 | gettysburg_pc | 100 |  | 48.4 | D2-, D1- whole clip, D3- whole clip |
| gettysburg_tg__G5 | gettysburg_wt | 99.6 | D1+ | 43.2 | D2-, D2-, D1+, D1- whole clip, D3- whole clip |
| greenman_reagan__G5 | reagan_farewell_1989 | 99.9 | D1+ | 61.3 | D1+, D5-, D5-, D1- whole clip, D3- whole clip |

## Trivial baselines (L2 + L3, splits not used for fitting)

| split | method | TP | FP | FN | F1 |
|---|---|---|---|---|---|
| val | detector | 30 | 11 | 2 | 0.822 |
| val | no_flags | 0 | 0 | 32 | 0 |
| val | flag_all | 12 | 1.58e+03 | 20 | 0.015 |
| val | random | 1.45 | 30.6 | 30.6 | 0.045 |

## Stress matrix

| split / population | condition | regime | added /min | removed /min | exposure (min) | max |delta score| | measurable score pairs | missing score pairs | flaws found before | flaws found after | achieved compression reduction (dB) | expected |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| val | gain +6 dB | R1 | 0 | 0 | 0.99 | 0 | 2 | 0 |  |  |  | invariant |
| val | gain -6 dB | R1 | 0 | 0 | 0.99 | 0 | 2 | 0 |  |  |  | invariant |
| val | low-pass 3.4 kHz | R1 | 0 | 0 | 0.99 | 0 | 2 | 0 |  |  |  | invariant |
| val | white noise 20 dB SNR | R1 | 1.01 | 0 | 0.99 | 0.01 | 2 | 0 |  |  |  | invariant |
| val | MP3 64 kbit/s | R1 | 0 | 0 | 0.99 | 0 | 2 | 0 |  |  |  | invariant |
| val | dynamic-range compression | R1 | 5.06 | 0 | 0.99 | 3.94 | 2 | 0 |  |  | 10.2 | invariant |
| val | WORLD speaker transform (baseline vs its own transform, absolute regions) | R2 | 0 |  | 0.99 |  |  |  |  |  |  | silent |
| val | white noise 20 dB SNR (flawed L2+L3) | R1 | 1.51 | 1.01 | 3.97 | 3.93 | 8 | 0 | 30 | 28 |  | retained detection |
| val | dynamic-range compression (flawed L2+L3) | R1 | 7.8 | 1.51 | 3.97 | 6.05 | 8 | 0 | 30 | 28 | 10.2 | retained detection |
| check readers | gain +6 dB | R2 | 0 | 0 | 7.76 | 0 | 18 | 0 |  |  |  | invariant |
| check readers | gain -6 dB | R2 | 0 | 0 | 7.76 | 0.04 | 18 | 0 |  |  |  | invariant |
| check readers | low-pass 3.4 kHz | R2 | 0.258 | 0 | 7.76 | 0.15 | 18 | 0 |  |  |  | invariant |
| check readers | white noise 20 dB SNR | R2 | 0 | 0 | 7.76 | 0.64 | 18 | 0 |  |  |  | invariant |
| check readers | MP3 64 kbit/s | R2 | 0 | 0 | 7.76 | 0.05 | 18 | 0 |  |  |  | invariant |
| check readers | dynamic-range compression | R2 | 0.129 | 0 | 7.76 | 0.57 | 18 | 0 |  |  | 11.1 | invariant |
| check readers | real second speaker (check-reader pairs, unmodified) | R2 | 1.03 |  | 7.76 |  |  |  |  |  |  | false regions of the null |
| val | identity clips (reference) | R1 | 0 |  | 0.99 |  |  |  |  |  |  | reference |

## Chain A versus chain B

| speech | split | type | level | chain | words | TP | truths | false regions (all counted) | onset error (ms) | offset error (ms) |
|---|---|---|---|---|---|---|---|---|---|---|
| lbush_radio_2001 | val | RUSH | 2 | A | [69, 75] | 1 | 1 | 0 | -150 | -14.1 |
| lbush_radio_2001 | val | RUSH | 2 | B | [69, 75] | 1 | 1 | 0 | -150 | -14 |
| eisenhower_farewell_1961 | val | RUSH | 2 | A | [40, 47] | 1 | 1 | 0 | 1.14e+03 | 6.6 |
| eisenhower_farewell_1961 | val | RUSH | 2 | B | [40, 47] | 1 | 1 | 0 | 20.1 | -213 |
| lbush_radio_2001 | val | RUSH | 3 | A | [69, 75] | 1 | 1 | 0 | -150 | 8.9 |
| lbush_radio_2001 | val | RUSH | 3 | B | [69, 75] | 1 | 1 | 0 | -150 | -10.8 |
| eisenhower_farewell_1961 | val | RUSH | 3 | A | [40, 47] | 1 | 1 | 0 | 1.04e+03 | 29.9 |
| eisenhower_farewell_1961 | val | RUSH | 3 | B | [40, 47] | 1 | 1 | 0 | 1.04e+03 | 11.2 |
| lbush_radio_2001 | val | DRAG | 2 | A | [2, 8] | 1 | 1 | 0 | 30 | -118 |
| lbush_radio_2001 | val | DRAG | 2 | B | [2, 8] | 1 | 1 | 0 | 49.7 | -98.3 |
| eisenhower_farewell_1961 | val | DRAG | 2 | A | [35, 40] | 1 | 1 | 0 | -130 | 816 |
| eisenhower_farewell_1961 | val | DRAG | 2 | B | [35, 40] | 1 | 1 | 0 | -130 | -45.3 |
| lbush_radio_2001 | val | DRAG | 3 | A | [2, 8] | 1 | 1 | 0 | 50 | -166 |
| lbush_radio_2001 | val | DRAG | 3 | B | [2, 8] | 1 | 1 | 0 | 69.6 | -146 |
| eisenhower_farewell_1961 | val | DRAG | 3 | A | [35, 40] | 1 | 1 | 0 | -130 | 823 |
| eisenhower_farewell_1961 | val | DRAG | 3 | B | [35, 40] | 1 | 1 | 1 | -130 | 819 |
| lbush_radio_2001 | val | MONOTONE | 2 | A | [46, 51] | 1 | 1 | 0 | 40 | -390 |
| lbush_radio_2001 | val | MONOTONE | 2 | B | [46, 51] | 1 | 1 | 0 | 240 | -370 |
| eisenhower_farewell_1961 | val | MONOTONE | 2 | A | [44, 51] | 1 | 1 | 0 | 50 | -120 |
| eisenhower_farewell_1961 | val | MONOTONE | 2 | B | [44, 51] | 1 | 1 | 0 | 1.25e+03 | -20 |
| lbush_radio_2001 | val | MONOTONE | 3 | A | [46, 51] | 1 | 1 | 0 | 40 | -370 |
| lbush_radio_2001 | val | MONOTONE | 3 | B | [46, 51] | 1 | 1 | 0 | 40 | -370 |
| eisenhower_farewell_1961 | val | MONOTONE | 3 | A | [44, 51] | 1 | 1 | 0 | 50 | -120 |
| eisenhower_farewell_1961 | val | MONOTONE | 3 | B | [44, 51] | 1 | 1 | 0 | 1.25e+03 | 80 |

## Directional test: a higher level never raises the dimension score

| speech | split | type | L1 | L2 | L3 | cause |
|---|---|---|---|---|---|---|
| eisenhower_farewell_1961 | val | DEEMPHASIS | 100 | 94.1 | 92.5 |  |
| eisenhower_farewell_1961 | val | DRAG | 100 | 84.3 | 61.3 |  |
| eisenhower_farewell_1961 | val | FADE | 100 | 94.1 | 81 |  |
| eisenhower_farewell_1961 | val | MONOTONE | 99.9 | 92.5 | 80.7 |  |
| eisenhower_farewell_1961 | val | MUMBLE | 100 | 93.8 | 89.9 |  |
| eisenhower_farewell_1961 | val | PAUSE_DROPPED | 81.6 | 81.6 | 81.6 |  |
| eisenhower_farewell_1961 | val | PAUSE_INTRUSIVE | 97.9 | 91.7 | 81.6 |  |
| eisenhower_farewell_1961 | val | RUSH | 99.2 | 91 | 79 |  |
| gwbush_911_2001 | train | DEEMPHASIS | 100 | 76.8 | 40.2 |  |
| gwbush_911_2001 | train | DRAG | 99.8 | 94 | 84.3 |  |
| gwbush_911_2001 | train | FADE | 99.4 | 95.2 | 81.4 |  |
| gwbush_911_2001 | train | MONOTONE | 99.2 | 93.6 | 86.5 |  |
| gwbush_911_2001 | train | MUMBLE | 100 | 85.1 | 81.8 |  |
| gwbush_911_2001 | train | PAUSE_DROPPED | 92.2 | 87.1 | 83.9 |  |
| gwbush_911_2001 | train | PAUSE_INTRUSIVE | 97.2 | 89.8 | 78 |  |
| gwbush_911_2001 | train | RUSH | 99.4 | 92.8 | 80.4 |  |
| harris_uncsw_2021 | train | DEEMPHASIS | 100 | 100 | 92 |  |
| harris_uncsw_2021 | train | DRAG | 100 | 91.2 | 76.3 |  |
| harris_uncsw_2021 | train | FADE | 99.9 | 89.4 | 76.8 |  |
| harris_uncsw_2021 | train | MONOTONE | 100 | 92.1 | 83.2 |  |
| harris_uncsw_2021 | train | MUMBLE | 100 | 85.4 | 80.6 |  |
| harris_uncsw_2021 | train | PAUSE_DROPPED | 99 | 96.9 | 96.1 |  |
| harris_uncsw_2021 | train | PAUSE_INTRUSIVE | 97.8 | 92.7 | 84.3 |  |
| harris_uncsw_2021 | train | RUSH | 99.9 | 93.7 | 84.6 |  |
| hclinton_tomorrow_2010 | train | DEEMPHASIS | 100 | 98.4 | 83.3 |  |
| hclinton_tomorrow_2010 | train | DRAG | 99.5 | 84.2 | 58 |  |
| hclinton_tomorrow_2010 | train | FADE | 99.9 | 90.5 | 86.3 |  |
| hclinton_tomorrow_2010 | train | MONOTONE | 100 | 90.3 | 72.8 |  |
| hclinton_tomorrow_2010 | train | MUMBLE | 100 | 86 | 80.5 |  |
| hclinton_tomorrow_2010 | train | PAUSE_DROPPED | 86.9 | 79.1 | 73.9 |  |
| hclinton_tomorrow_2010 | train | PAUSE_INTRUSIVE | 96.1 | 86.9 | 72.5 |  |
| hclinton_tomorrow_2010 | train | RUSH | 99.1 | 88.6 | 73.7 |  |
| lbush_radio_2001 | val | DEEMPHASIS | 100 | 91.3 | 80.8 |  |
| lbush_radio_2001 | val | DRAG | 99.6 | 93.9 | 85.6 |  |
| lbush_radio_2001 | val | FADE | 100 | 99.1 | 89.2 |  |
| lbush_radio_2001 | val | MONOTONE | 100 | 94 | 85.3 |  |
| lbush_radio_2001 | val | MUMBLE | 100 | 95.1 | 93.3 |  |
| lbush_radio_2001 | val | PAUSE_DROPPED | 96 | 90.9 | 88.4 |  |
| lbush_radio_2001 | val | PAUSE_INTRUSIVE | 96.8 | 86.3 | 68.5 |  |
| lbush_radio_2001 | val | RUSH | 99.1 | 87.7 | 70.6 |  |
| obama_weekly_2009 | train | DEEMPHASIS | 100 | 100 | 100 |  |
| obama_weekly_2009 | train | DRAG | 99.7 | 85.5 | 61.3 |  |
| obama_weekly_2009 | train | FADE | 100 | 92.4 | 74.9 |  |
| obama_weekly_2009 | train | MONOTONE | 100 | 100 | 92.5 | other |
| obama_weekly_2009 | train | MUMBLE | 100 | 93 | 89.9 |  |
| obama_weekly_2009 | train | PAUSE_DROPPED | 89.2 | 83.3 | 78.9 |  |
| obama_weekly_2009 | train | PAUSE_INTRUSIVE | 97.5 | 100 | 78 | pause not measured at the labelled boundary |
| obama_weekly_2009 | train | RUSH | 99.8 | 93.4 | 84.2 |  |
| reagan_farewell_1989 | train | DEEMPHASIS | 100 | 100 | 95.6 |  |
| reagan_farewell_1989 | train | DRAG | 99.6 | 91.3 | 77.1 |  |
| reagan_farewell_1989 | train | FADE | 100 | 96.6 | 89.2 |  |
| reagan_farewell_1989 | train | MONOTONE | 100 | 98.2 | 95.6 |  |
| reagan_farewell_1989 | train | MUMBLE | 100 | 88 | 83.9 |  |
| reagan_farewell_1989 | train | PAUSE_DROPPED | 89.5 | 83.6 | 79.4 |  |
| reagan_farewell_1989 | train | PAUSE_INTRUSIVE | 97.5 | 90.1 | 78 |  |
| reagan_farewell_1989 | train | RUSH | 99.5 | 92.7 | 85 |  |

## Repair test (inverse edit vs placebo)

| split | type | flags tested | removed by repair | kept after placebo |
|---|---|---|---|---|
| val | RUSH | 2 | 2 | 2 |
| val | DRAG | 2 | 2 | 2 |
| val | PAUSE_DROPPED | 2 | 2 | 2 |
| val | PAUSE_INTRUSIVE | 2 | 2 | 2 |
| val | FADE | 2 | 1 | 2 |
| val | MONOTONE | 2 | 2 | 2 |

| clip | split | type | placebo | flag removed (word index) | score before | score after | new flags | error |
|---|---|---|---|---|---|---|---|---|
| eisenhower_farewell_1961__single_L2A | val | RUSH | False | True | 95.6 | 96.6 | [] |  |
| eisenhower_farewell_1961__single_L2A | val | RUSH | True | False | 95.6 | 95.6 | [] |  |
| eisenhower_farewell_1961__single_L2A | val | PAUSE_DROPPED | False | True | 95.6 | 96.8 | [] |  |
| eisenhower_farewell_1961__single_L2A | val | PAUSE_DROPPED | True | False | 95.6 | 95.6 | [] |  |
| eisenhower_farewell_1961__single_L2A | val | MONOTONE | False | True | 95.6 | 97.2 | [] |  |
| eisenhower_farewell_1961__single_L2A | val | MONOTONE | True | False | 95.6 | 95.7 | [] |  |
| eisenhower_farewell_1961__single_L2B | val | PAUSE_INTRUSIVE | False | True | 93.4 | 95 | [] |  |
| eisenhower_farewell_1961__single_L2B | val | PAUSE_INTRUSIVE | True | False | 93.4 | 93.4 | [] |  |
| eisenhower_farewell_1961__single_L2B | val | DRAG | False | True | 93.4 | 95.4 | [] |  |
| eisenhower_farewell_1961__single_L2B | val | DRAG | True | False | 93.4 | 93.4 | [] |  |
| lbush_radio_2001__single_L2A | val | RUSH | False | True | 93.6 | 95 | [] |  |
| lbush_radio_2001__single_L2A | val | RUSH | True | False | 93.6 | 93.6 | [] |  |
| lbush_radio_2001__single_L2A | val | PAUSE_DROPPED | False | True | 93.6 | 96.6 | [] |  |
| lbush_radio_2001__single_L2A | val | PAUSE_DROPPED | True | False | 93.6 | 93.6 | [] |  |
| lbush_radio_2001__single_L2A | val | MONOTONE | False | True | 93.6 | 94.8 | [] |  |
| lbush_radio_2001__single_L2A | val | MONOTONE | True | False | 93.6 | 93.8 | [] |  |
| lbush_radio_2001__single_L2B | val | PAUSE_INTRUSIVE | False | True | 93.4 | 95.9 | [] |  |
| lbush_radio_2001__single_L2B | val | PAUSE_INTRUSIVE | True | False | 93.4 | 93.4 | [] |  |
| lbush_radio_2001__single_L2B | val | DRAG | False | True | 93.4 | 94.4 | [] |  |
| lbush_radio_2001__single_L2B | val | DRAG | True | False | 93.4 | 93.4 | [] |  |
| eisenhower_farewell_1961__single_L3A | val | FADE | False | True | 83.9 | 88.6 | [] |  |
| eisenhower_farewell_1961__single_L3A | val | FADE | True | False | 83.9 | 83.9 | [] |  |
| lbush_radio_2001__single_L3A | val | FADE | False | False | 82.5 | 87.4 | [] |  |
| lbush_radio_2001__single_L3A | val | FADE | True | False | 82.5 | 82.5 | [] |  |

## Feature internal consistency

| split | type | level | n | recipe setting | realised (measured by the same extractor on the edit span) | detector measurement (window centres inside the span) | median of paired ratios |
|---|---|---|---|---|---|---|---|
| train | RUSH | 1 | 5 | 1.2 | -0.182 | -0.139 | 0.761 |
| train | RUSH | 2 | 5 | 1.45 | -0.372 | -0.258 | 0.697 |
| train | RUSH | 3 | 5 | 1.9 | -0.634 | -0.52 | 0.823 |
| train | DRAG | 1 | 5 | 1.2 | 0.176 | 0.143 | 0.816 |
| train | DRAG | 2 | 5 | 1.45 | 0.359 | 0.309 | 0.862 |
| train | DRAG | 3 | 5 | 1.9 | 0.632 | 0.57 | 0.952 |
| train | PAUSE_DROPPED | 1 | 5 | 0.4 | -0.51 | -0.51 | 1 |
| train | PAUSE_DROPPED | 2 | 5 | 0.2 | -0.54 | -0.54 | 1 |
| train | PAUSE_DROPPED | 3 | 5 | 0 | -0.71 | -0.71 | 1 |
| train | PAUSE_INTRUSIVE | 1 | 5 | 0.35 | 0.35 | 0.35 | 1 |
| train | PAUSE_INTRUSIVE | 2 | 5 | 0.6 | 0.59 | 0.59 | 1 |
| train | PAUSE_INTRUSIVE | 3 | 5 | 1.2 | 1.19 | 1.19 | 1 |
| train | MONOTONE | 1 | 5 | 0.5 | -0.582 | -0.352 | 0.713 |
| train | MONOTONE | 2 | 5 | 0.25 | -0.941 | -0.777 | 0.856 |
| train | MONOTONE | 3 | 5 | 0 | -1.7 | -0.906 | 0.534 |
| train | DEEMPHASIS | 1 | 5 | 0.5 | -0.774 | -0.774 | 1 |
| train | DEEMPHASIS | 2 | 5 | 0.75 | -1.14 | -1.14 | 1 |
| train | DEEMPHASIS | 3 | 5 | 1 | -1.2 | -1.2 | 1 |
| train | FADE | 1 | 5 | 4 | -2.81 | -2.84 | 1.01 |
| train | FADE | 2 | 5 | 8 | -5.68 | -5.15 | 0.933 |
| train | FADE | 3 | 5 | 14 | -9.41 | -8.4 | 0.96 |
| train | MUMBLE | 1 | 5 | 0.3 | -0.347 | -0.305 | 0.854 |
| train | MUMBLE | 2 | 5 | 0.6 | -0.737 | -0.514 | 0.697 |
| train | MUMBLE | 3 | 5 | 1 | -0.896 | -0.64 | 0.765 |
| val | RUSH | 1 | 2 | 1.2 | -0.171 | -0.112 | 0.666 |
| val | RUSH | 2 | 2 | 1.45 | -0.393 | -0.33 | 0.844 |
| val | RUSH | 3 | 2 | 1.9 | -0.639 | -0.529 | 0.828 |
| val | DRAG | 1 | 2 | 1.2 | 0.171 | 0.137 | 0.804 |
| val | DRAG | 2 | 2 | 1.45 | 0.287 | 0.344 | 1.29 |
| val | DRAG | 3 | 2 | 1.9 | 0.595 | 0.547 | 0.925 |
| val | PAUSE_DROPPED | 1 | 2 | 0.4 | -0.405 | -0.405 | 1 |
| val | PAUSE_DROPPED | 2 | 2 | 0.2 | -0.625 | -0.625 | 1 |
| val | PAUSE_DROPPED | 3 | 2 | 0 | -1.15 | -1.15 | 1 |
| val | PAUSE_INTRUSIVE | 1 | 2 | 0.35 | 0.31 | 0.31 | 1 |
| val | PAUSE_INTRUSIVE | 2 | 2 | 0.6 | 0.605 | 0.605 | 1 |
| val | PAUSE_INTRUSIVE | 3 | 2 | 1.2 | 1.18 | 1.18 | 1 |
| val | MONOTONE | 1 | 2 | 0.5 | -0.555 | -0.501 | 0.901 |
| val | MONOTONE | 2 | 2 | 0.25 | -1.11 | -1.02 | 0.92 |
| val | MONOTONE | 3 | 2 | 0 | -2.08 | -1.59 | 0.766 |
| val | DEEMPHASIS | 1 | 2 | 0.5 | -0.673 | -0.673 | 1 |
| val | DEEMPHASIS | 2 | 2 | 0.75 | -1.31 | -1.31 | 1 |
| val | DEEMPHASIS | 3 | 2 | 1 | -1.47 | -1.47 | 1 |
| val | FADE | 1 | 2 | 4 | -2.25 | -2.33 | 1.03 |
| val | FADE | 2 | 2 | 8 | -4.22 | -4.6 | 1.1 |
| val | FADE | 3 | 2 | 14 | -8.22 | -7.89 | 0.966 |
| val | MUMBLE | 1 | 2 | 0.3 | -0.295 | -0.274 | 0.925 |
| val | MUMBLE | 2 | 2 | 0.6 | -0.639 | -0.392 | 0.607 |
| val | MUMBLE | 3 | 2 | 1 | -0.756 | -0.641 | 0.847 |

## Device agreement: GPU versus CPU alignment

| split | GPU | clips | recordings aligned | max word-time difference (ms) | flags identical |
|---|---|---|---|---|---|
| val | cuda:0 | 6 | 7 | 0 | True |

## Cross-speaker operating curve (threshold h versus false regions and detection)

| flag key | h | threshold | fitted on train | observed false regions per comparison-minute | reader counts | away-edits detected | by type |
|---|---|---|---|---|---|---|---|
| D1- | 1 | 0.152 | False | 6.32 | {'gettysburg_dj': 17, 'gettysburg_sa': 13, 'gettysburg_tg': 19} | 29/31 | {'RUSH': '29/31'} |
| D1- | 1.5 | 0.228 | False | 3.35 | {'gettysburg_dj': 8, 'gettysburg_sa': 6, 'gettysburg_tg': 12} | 29/31 | {'RUSH': '29/31'} |
| D1- | 2 | 0.305 | False | 1.8 | {'gettysburg_dj': 5, 'gettysburg_sa': 3, 'gettysburg_tg': 6} | 24/31 | {'RUSH': '24/31'} |
| D1- | 2.5 | 0.381 | False | 1.03 | {'gettysburg_dj': 4, 'gettysburg_sa': 1, 'gettysburg_tg': 3} | 23/31 | {'RUSH': '23/31'} |
| D1- | 3 | 0.457 | True | 0.387 | {'gettysburg_dj': 1, 'gettysburg_sa': 1, 'gettysburg_tg': 1} | 20/31 | {'RUSH': '20/31'} |
| D1- | 3.5 | 0.533 | False | 0.258 | {'gettysburg_dj': 0, 'gettysburg_sa': 1, 'gettysburg_tg': 1} | 13/31 | {'RUSH': '13/31'} |
| D1- | 4 | 0.609 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 8/31 | {'RUSH': '8/31'} |
| D1- | 4.5 | 0.685 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 4/31 | {'RUSH': '4/31'} |
| D1- | 5 | 0.761 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 2/31 | {'RUSH': '2/31'} |
| D1- | 5.5 | 0.837 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/31 | {'RUSH': '0/31'} |
| D1- | 6 | 0.914 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/31 | {'RUSH': '0/31'} |
| D1+ | 1 | 0.152 | False | 6.44 | {'gettysburg_dj': 14, 'gettysburg_sa': 17, 'gettysburg_tg': 19} | 17/17 | {'DRAG': '17/17'} |
| D1+ | 1.5 | 0.228 | False | 3.35 | {'gettysburg_dj': 9, 'gettysburg_sa': 7, 'gettysburg_tg': 10} | 17/17 | {'DRAG': '17/17'} |
| D1+ | 2 | 0.305 | False | 1.68 | {'gettysburg_dj': 5, 'gettysburg_sa': 3, 'gettysburg_tg': 5} | 16/17 | {'DRAG': '16/17'} |
| D1+ | 2.5 | 0.381 | False | 0.644 | {'gettysburg_dj': 1, 'gettysburg_sa': 1, 'gettysburg_tg': 3} | 15/17 | {'DRAG': '15/17'} |
| D1+ | 3 | 0.457 | True | 0.258 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 2} | 14/17 | {'DRAG': '14/17'} |
| D1+ | 3.5 | 0.533 | False | 0.258 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 2} | 12/17 | {'DRAG': '12/17'} |
| D1+ | 4 | 0.609 | False | 0.258 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 2} | 10/17 | {'DRAG': '10/17'} |
| D1+ | 4.5 | 0.685 | False | 0.129 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 1} | 7/17 | {'DRAG': '7/17'} |
| D1+ | 5 | 0.761 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 6/17 | {'DRAG': '6/17'} |
| D1+ | 5.5 | 0.837 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 5/17 | {'DRAG': '5/17'} |
| D1+ | 6 | 0.914 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 1/17 | {'DRAG': '1/17'} |
| D2- | 1 | 0.415 | False | 3.74 | {'gettysburg_dj': 6, 'gettysburg_sa': 6, 'gettysburg_tg': 17} | 30/31 | {'PAUSE_DROPPED': '30/31'} |
| D2- | 1.5 | 0.623 | False | 1.68 | {'gettysburg_dj': 2, 'gettysburg_sa': 3, 'gettysburg_tg': 8} | 25/31 | {'PAUSE_DROPPED': '25/31'} |
| D2- | 2 | 0.83 | False | 0.644 | {'gettysburg_dj': 0, 'gettysburg_sa': 1, 'gettysburg_tg': 4} | 19/31 | {'PAUSE_DROPPED': '19/31'} |
| D2- | 2.5 | 1.04 | False | 0.258 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 2} | 12/31 | {'PAUSE_DROPPED': '12/31'} |
| D2- | 2.95 | 1.22 | True | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 9/31 | {'PAUSE_DROPPED': '9/31'} |
| D2- | 3 | 1.25 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 9/31 | {'PAUSE_DROPPED': '9/31'} |
| D2- | 3.5 | 1.45 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 7/31 | {'PAUSE_DROPPED': '7/31'} |
| D2- | 4 | 1.66 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 2/31 | {'PAUSE_DROPPED': '2/31'} |
| D2- | 4.5 | 1.87 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/31 | {'PAUSE_DROPPED': '0/31'} |
| D2- | 5 | 2.08 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/31 | {'PAUSE_DROPPED': '0/31'} |
| D2- | 5.5 | 2.28 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/31 | {'PAUSE_DROPPED': '0/31'} |
| D2- | 6 | 2.49 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/31 | {'PAUSE_DROPPED': '0/31'} |
| D2+ | 1 | 0.415 | False | 0.773 | {'gettysburg_dj': 0, 'gettysburg_sa': 6, 'gettysburg_tg': 0} | 14/18 | {'PAUSE_INTRUSIVE': '14/18'} |
| D2+ | 1.15 | 0.477 | True | 0.387 | {'gettysburg_dj': 0, 'gettysburg_sa': 3, 'gettysburg_tg': 0} | 14/18 | {'PAUSE_INTRUSIVE': '14/18'} |
| D2+ | 1.5 | 0.623 | False | 0.387 | {'gettysburg_dj': 0, 'gettysburg_sa': 3, 'gettysburg_tg': 0} | 14/18 | {'PAUSE_INTRUSIVE': '14/18'} |
| D2+ | 2 | 0.83 | False | 0.387 | {'gettysburg_dj': 0, 'gettysburg_sa': 3, 'gettysburg_tg': 0} | 14/18 | {'PAUSE_INTRUSIVE': '14/18'} |
| D2+ | 2.5 | 1.04 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 13/18 | {'PAUSE_INTRUSIVE': '13/18'} |
| D2+ | 3 | 1.25 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 3/18 | {'PAUSE_INTRUSIVE': '3/18'} |
| D2+ | 3.5 | 1.45 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/18 | {'PAUSE_INTRUSIVE': '0/18'} |
| D2+ | 4 | 1.66 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/18 | {'PAUSE_INTRUSIVE': '0/18'} |
| D2+ | 4.5 | 1.87 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/18 | {'PAUSE_INTRUSIVE': '0/18'} |
| D2+ | 5 | 2.08 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/18 | {'PAUSE_INTRUSIVE': '0/18'} |
| D2+ | 5.5 | 2.28 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/18 | {'PAUSE_INTRUSIVE': '0/18'} |
| D2+ | 6 | 2.49 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 0/18 | {'PAUSE_INTRUSIVE': '0/18'} |
| D3- | 1 | 0.336 | False | 6.32 | {'gettysburg_dj': 17, 'gettysburg_sa': 15, 'gettysburg_tg': 17} | 17/18 | {'MONOTONE': '17/18'} |
| D3- | 1.5 | 0.505 | False | 2.71 | {'gettysburg_dj': 6, 'gettysburg_sa': 6, 'gettysburg_tg': 9} | 17/18 | {'MONOTONE': '17/18'} |
| D3- | 2 | 0.673 | False | 1.29 | {'gettysburg_dj': 4, 'gettysburg_sa': 3, 'gettysburg_tg': 3} | 17/18 | {'MONOTONE': '17/18'} |
| D3- | 2.5 | 0.841 | False | 0.516 | {'gettysburg_dj': 3, 'gettysburg_sa': 0, 'gettysburg_tg': 1} | 18/18 | {'MONOTONE': '18/18'} |
| D3- | 3 | 1.01 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 18/18 | {'MONOTONE': '18/18'} |
| D3- | 3.25 | 1.09 | True | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 18/18 | {'MONOTONE': '18/18'} |
| D3- | 3.5 | 1.18 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 18/18 | {'MONOTONE': '18/18'} |
| D3- | 4 | 1.35 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 17/18 | {'MONOTONE': '17/18'} |
| D3- | 4.5 | 1.51 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 15/18 | {'MONOTONE': '15/18'} |
| D3- | 5 | 1.68 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 7/18 | {'MONOTONE': '7/18'} |
| D3- | 5.5 | 1.85 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 4/18 | {'MONOTONE': '4/18'} |
| D3- | 6 | 2.02 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 2/18 | {'MONOTONE': '2/18'} |
| D5- | 1 | 2.73 | False | 8.64 | {'gettysburg_dj': 20, 'gettysburg_sa': 17, 'gettysburg_tg': 30} | 15/18 | {'FADE': '15/18'} |
| D5- | 1.5 | 4.09 | False | 5.03 | {'gettysburg_dj': 13, 'gettysburg_sa': 9, 'gettysburg_tg': 17} | 15/18 | {'FADE': '15/18'} |
| D5- | 2 | 5.45 | False | 2.84 | {'gettysburg_dj': 8, 'gettysburg_sa': 2, 'gettysburg_tg': 12} | 15/18 | {'FADE': '15/18'} |
| D5- | 2.5 | 6.82 | False | 1.03 | {'gettysburg_dj': 2, 'gettysburg_sa': 2, 'gettysburg_tg': 4} | 15/18 | {'FADE': '15/18'} |
| D5- | 3 | 8.18 | False | 0.387 | {'gettysburg_dj': 2, 'gettysburg_sa': 0, 'gettysburg_tg': 1} | 15/18 | {'FADE': '15/18'} |
| D5- | 3.5 | 9.55 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 14/18 | {'FADE': '14/18'} |
| D5- | 4 | 10.9 | True | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 13/18 | {'FADE': '13/18'} |
| D5- | 4.5 | 12.3 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 12/18 | {'FADE': '12/18'} |
| D5- | 5 | 13.6 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 5/18 | {'FADE': '5/18'} |
| D5- | 5.5 | 15 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 4/18 | {'FADE': '4/18'} |
| D5- | 6 | 16.4 | False | 0 | {'gettysburg_dj': 0, 'gettysburg_sa': 0, 'gettysburg_tg': 0} | 2/18 | {'FADE': '2/18'} |

## Reproducibility

Two analyze() runs on eisenhower_farewell_1961__single_L3A: identical = True

