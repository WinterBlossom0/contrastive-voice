# Lab results applied to the design §8 criteria (2026-10-04)

Source: Kaggle cvoice-lab v2 (12,868 recordings, 48 tests, 73 min); compact table
build/work/kaggle_runs/lab_v2/compact.json; full results.json beside it. Criteria: DETECTOR_EXTENSION.md §8, fixed
before any result was read (sha256 recorded in HANDOFF.md, 2026-10-03).
"found / false" = share of contrast items found at the threshold that keeps 5 % false flags on held normal readers of the
same corpus (EARS regular, k = 5 references), and the achieved held false rate.

| §8 decision | Lab evidence | Criterion | Outcome |
|---|---|---|---|
| Natural-rushing text (speech_time_ratio) | EARS fast 0.54 / 0.03, AUC 0.90; slow 0.53 / 0.03, AUC 0.82 | lab gate on its contrast | SHIP the tempo-decomposition text |
| Filled pause (stability_run) | PodcastFillers events precision 0.54, recall 0.15 (±0.20 s) | precision >= 0.5 | SHIP as a candidate label (D7 subtype FILLED_PAUSE) |
| D7 timing key in R2 (word_duration_ratio, orphan_voiced_gap) | LibriStutter clip 0.39 / 0.10 and 0.34 / 0.07 | lab gate | FAIL: D7 stays R1-only; R2 listed (unscored) |
| D7 repetition label (inserted_material) | LibriStutter events precision 0.04, recall 0.12 | precision >= 0.5 | FAIL: label dropped, shows "lengthened word" |
| D7 prolongation label (stability_run, low-F0 variant) | LibriStutter events precision 0.02 | lab gate | FAIL: label dropped |
| D7 block label (within_word_silence) | LibriStutter events precision 0, recall 0 | passes on Real | FAIL: label dropped |
| D8 comparison stretch (final_pitch_change) | no real ending labels; speechocean rho <= 0.09 | AUC >= 0.70 on Real | NO DATA: D8 R1-only; R2 listed; declination as text only |
| Low-effort subtype (alpha_ratio, AVID soft vs normal) | 0.07 / 0.21 | lab gate | FAIL: "quieter (level only)" text |
| Trailing-off subtype (last_word_drop) | no real labels; contrasts 0.05-0.25 | lab gate | FAIL: plain D5 text |
| Uneven-tempo clip key (tempo_irregularity) | EARS fast 0.17 / 0.09, slow 0.35 / 0.09 | lab gate | FAIL: not shipped |
| D4+ (two_sided_emphasis) | no misplaced-emphasis labels | lab gate | FAIL: D4- only |
| D2- relative unit | not a lab measure | dev-run recall without null loss | decided by the dev run |

Findings outside the §8 table (reported, not used to change the product):
- inserted_material flags 0.94 of LibriStutter (synthetic) stutter clips at 0.02 false rate against EARS readers (clip level).
- greedy_word_error: Spearman rho -0.58 with speechocean762 sentence total score (n 2,583); breath_candidates rho -0.57 with
  fluency; orphan_voiced_gap -0.46.
- Most AUCs of same-speaker style contrasts against different-reader normal variation are below 0.5: a same-speaker style
  change moves a measure less than the normal difference between two competent readers (the R2 problem in numbers).
