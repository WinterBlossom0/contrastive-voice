# Final integration design: new flaw families in the detector (schema 4)

The design starts from the "calibration" design, which got the highest score from both critics. It adds the best ideas from the other two designs and fixes every defect the critics listed, or shows from the code that a defect is not one. I did not edit any file. All line numbers refer to the current tree (2026-10-03, after the wiring engineer's edits).

**Facts I checked again in the code before writing:**
- **The 1.03/min is all local regions.** In `build/work/kaggle_runs/dev_v8/x/eval/results.json` → `nulls/detail/R2 held-out/by_pair`, all 8 flags are local keys: D1± 5, D2+ 3. No whole-clip key appears, and all 3 D2+ flags come from one reader (`gettysburg_sa`). The whole-clip accounting therefore is not the cause.
- **The interval is wide.** An exact Poisson 95 % interval on 8 flags in 7.76 min is 0.44 to 2.03/min.
- **The fit rests on about one null region per key.** The fit gave 5 flags in 13.6 min, with budget_per_key 0.083 (`models/detector.json`, R2 `null`).
- **The documentation and the code agree.** DESIGN.md:338 ("Whole-clip thresholds are fitted separately") matches calibrate.py:116. The minimal design's claim of a contradiction is wrong. The judge is right.
- **A cause of weak R2 dropped-pause detection, found in the code:**
  - D2 has one scale, pooled over every eligible boundary of both signs (detect.py:57-70, compare.py:88-90).
  - The R2 threshold for D2- is 2.95 × 0.415 s = 1.22 s (`models/detector.json`).
  - A drop is at most the baseline pause, so only baseline pauses longer than 1.22 s can ever be flagged.
- **New constants are not hashed.** `as_dict()` returns the snapshot `_DETECTOR_CONFIG` taken at config.py:193 (config.py:299-301). A constant written after line 193 is not in the hash.
- **The registry now lives in config.py.** `FLAW_REGISTRY` is at config.py:247-280. `HESITATION` has primary D1 (config.py:256), and the disfluency and ending types have the primaries "DISFLUENCY" and "ENDINGS" (config.py:258-270).
- **New types are kept out of R1 selection.** `CALIBRATE_EXTRA = False` (config.py:295), and calibrate.py:302-303 excludes the new types.
- **The lab already has a written pass rule.** The rule is: held-out false rate ≤ 0.05 per contrast and found share ≥ 0.5 on every corpus (lab/evaluate.py:399; FALSE_RATE at lab/__init__.py:4).

## 1. Summary table

**Kinds:**
- **W**: windowed, five-word window.
- **E**: word event.
- **B**: boundary event.
- **S**: sentence-final event.
- **C**: whole clip.

**Calibration data:**
- **R1n**: identity, placebo and noise nulls.
- **R1s**: train single-level clips.
- **R2p**: same-text reader pairs.
- **Real**: real-flaw corpora, used for validation only.

**Sub = subtype.** A subtype only changes the explanation. It adds no flag key and takes no budget share.

| Flaw pattern | Measure | Kind | R1 | R2 | Calibration data | Conditional on lab? |
|---|---|---|---|---|---|---|
| Natural rushing | D1- region; the explanation splits it into speech-time, pause-count and mean-pause terms, with add-one counts | Sub of D1- | on | on (D1 is enabled) | R1n, R2p | yes (decomposition text) |
| Dropped pauses (open R2 problem) | D2- with a per-key scale fitted on countable drop units only. Variant: relative drop (rp−rb)/rb | B | on | on | R1n, R2p | the variant only |
| Hesitation | D2+ event plus a D7 stretch at the next word, merged into one finding | Sub of D2+ | on | on (D2+) | R1n, R2p | yes |
| Word-by-word reading | at least 3 D2+ events in one sentence give one grouped finding | Sub of D2+ | on | on | R1n, R2p | yes |
| Uneven tempo | clip key D7: g = 1.4826·MAD of the D7 per-word x | C | on | listed | R1n | yes |
| Word repetition, sound repetition, prolongation, block | **D7+ word time**: x = ln(occupancy_p/occupancy_b), median-centred. Occupancy = aligned word span plus orphan voiced time in the gap before the word. The subtype label comes from evidence (§4) | E | on | listed until promoted | R1n, R2p, Real | yes |
| Filled pause | D7 subtype: an orphan voiced run of at least ORPHAN_MIN_S | E | off unless Real precision passes | listed | Real only | yes |
| Rising ending, flattened final fall | **D8+ ending**: x = F_p − F_b, where F = final pitch change at "." in st | S | on | listed until promoted | R1n, R2p, Real | yes (which comparison stretch) |
| Low vocal effort | D5- region where the alpha ratio also falls; the F0 drop is supporting evidence only | Sub of D5- | on | on (D5) | R1n, R2p, Real (AVID) | yes |
| Trailing off | D5- region that ends at a sentence-final word, with a last-word drop larger than the reference's | Sub of D5- | on | on | R1n, R2p | yes |
| Misplaced emphasis | D4- (registry primary, sign −1). Optional D4+: stress at a function word that the reference does not stress | E | on | off (D4 is R1 only, config.py:17) | R1n | D4+ only |
| Repeated contour | not shipped. No validating study exists (pitch_emphasis REPORT:22, 105), and the only test is the recipe's own operation | none | off | off | none | stays in the lab |

**Why there is no D9 phrasing dimension.**
- At eligible boundaries, D2 already uses `sil_raw_p − sil_raw_b` (compare.py:88-90). A windowed sum of that same difference counts each pause change twice: once in the score and once in the budget (judge defect 1).
- At recipe L2 and L3 the word-by-word silences are 0.225 and 0.30 s (config.py:200). These sit at or above `PAUSE_MIN_S` = 0.20, so D2+ sees each one.
- Only at L1 (0.15 s) are some gaps below the cut-off. That weakness is expected and is reported.

## 2. Code changes per file

**config.py**
- **Hash.** Put every new detector constant above line 193, or compute `_base_dict()` after the registry and exclude the dataset-only names from it. Add a test (step 1) that every `C.X` name read in detect, compare, score, explain, features and patterns is in `as_dict()`.
- **Dimension tables.**
  - `DIMS += ("D7","D8")`.
  - Add labels: D7 "Word time" (brief word "Cadence"), D8 "Ending" (brief word "Tone"). These are design values that the owner can change.
  - `FLAG_SIGNS`: D7 (1,), D8 (1,).
  - Add `FLOORS`, `MIN_REGION_WORDS` = 1, `X_SAT` and `PMAX_START` entries.
  - `CLIP_DIMS += ("D7",)` and `CLIP_LN["D7"]`. The clip key is required, because load_detector checks the clip keys (detect.py:241).
- **New table `UNIT_KIND`.** D2 → boundary; D4, D7, D8 → word event; all others → window. Also `is_event(dim)` and `dim_of(key)`.
- **New constants:** `BLOCK_S`, `STABLE_*`, `ORPHAN_MIN_S`, `FINAL_WINDOW_S`, `MIN_FINAL_VOICED`, `ALPHA_DROP_DB`, `F0_DROP_ST`, `WORD_BY_WORD_MIN_EVENTS` and `HESITATION_STRETCH_MIN`. They move from lab/__init__.py:6-12 into config.py, and the lab imports them.
- **`FUNCTION_WORDS` in one place.** It is now duplicated at edits_extra.py:20 and lab/__init__.py:20.
- **Registry primaries (a declared change, agreed with the wiring engineer before any evaluation run):**
  - The 5 DISFLUENCY types get primary D7. ENDINGS gets primary D8. The `family` names stay.
  - **HESITATION gets primary D2 (sign +1) with secondaries D1, D4 and D7.**
  - Reason: a word stretched ×1.2 inside a five-word window changes D1 by about ln 1.04. That is far below the R2 D1 threshold of 3.0 × 0.152 = 0.46 ln. D2+ sees the inserted 0.2 to 1.0 s of silence directly (R2 threshold 1.15 × 0.415 = 0.48 s).
  - UNEVEN_TEMPO is scored as the D7 clip flag, with sign +1.

**features.py / align.py / pipeline.py:42-49**
- Cache `greedy_words(logp)` (align.py:284) and the character spans together with start, end and compat. The cache key gets a version suffix.
- `Recording` gains these fields: `occ`, `orphan_spans`, `word_silence_spans`, `stable_spans`, `inserted`, `alpha_word` and `final_df0`.
- Move the code from lab/measures.py:392-507 into features.py. The lab imports the product version, so one implementation exists.
- Also add to `stability_run` the low-F0 condition that the report requires (disfluency REPORT:322; it is missing at measures.py:447).

**compare.py**
- `d7_word_time` (E):
  - countable at every word with finite occupancy in both clips
  - `w = 1/n`
  - g = MAD spread, which is the clip value for uneven tempo
- `d8_ending` (S):
  - x is NaN except at the final words of "." sentences
  - countable only when both clips have at least `MIN_FINAL_VOICED` voiced frames in each stretch
  - `w = 1/(number of "." sentences)`
- Add `reference()` branches for D7 (p/exp(x)) and D8 (p−x) at compare.py:33-43.
- Add coverage overrides so that "no event" counts as measured (pattern of compare.py:172-177).
- Add `event_span(comp, dim, i)`, which generalises `pause_span`. It returns the sub-word evidence span.
- Optional D4+ units in `d4_emphasis` (compare.py:106-116).

**detect.py**
- Replace the literal at detect.py:125 with `is_event`.
- Event scales are per key and come from countable units only: `fit_scales` keys D2, D4, D7 and D8 by (dim, sign) and pools units where `countable` is true. Windowed dimensions keep the per-dimension scale.
  - This gives D7 and D8 their own robust z units, which is the events design's idea without a second pipeline.
  - It removes the pooled-D2 cause above.
- `choose_h` takes a counting callable.
- `SCHEMA = 4`. `load_detector` checks the new key set.

**calibrate.py**
- Use `dim_of(k)` in place of `k[:2]` (calibrate.py:172-173).
- Same-text grouped nulls and leave-one-group-out stability (§3).
- A separate per-clip rate for whole-clip flags (§3).
- The promotion test (§3).

**patterns.py (new)** runs after `decode`.
- It assigns subtypes and groups regions into findings.
- It never removes or adds regions. Calibration and evaluation therefore count the same regions as before the grouping, which fixes judge defect 3.

**score.py**
- One penalty per location: inside a finding group, only the largest member mass counts (academic defect 9).
- The score gates are refitted through the existing uniform Pmax factor (calibrate.py:221-232).

**explain.py**
- Replace the if/elif chain with a table: `EXPLAIN[(dim, sign, subtype)]`.
- The silent `else` → D6 (explain.py:141) and `else` → D3 (explain.py:170) become `KeyError`.

**events.py / evaluate.py**
- Use `is_event` at events.py:56/95/115/136/140 and evaluate.py:297/301/348/384/501-502/515-516/736/759/763.
- `dim_of` at evaluate.py:131.
- `range(len(C.DIMS))` at evaluate.py:1014.
- Extend `OKABE` (evaluate.py:964) and `span_realised`.
- Make the botched pair general.

**pipeline.py**
- `_ROWS` from `C.DIMS`, so that D7 and D8 are rows of kind "word", NaN except at candidate words.
- Extend `_DIFF_LABEL`.
- Build the notices and `detection_note` from `REGIME_DIMS` and from the detector's `enabled` list, not from literal text (pipeline.py:301-312).
- Result schema 2.

## 3. R2 calibration with the larger reader pool

1. **Keep the user's values.**
   - The local budget stays `FALSE_RATE_BUDGET` = 0.5 regions per comparison-minute, split equally over the enabled R2 keys (calibrate.py:109). There is no `R2_RATE_SHARE` table: it has no fitting rule, which was academic defect C1.
   - Whole-clip flags get their own rate, false clip flags per null clip, because a once-per-clip flag does not fit a per-minute budget (academic defect 5). The proposed design value is 0.05, the lab convention. **Owner decision.**
2. **Null pool.**
   - **Groups:** one group per `(source, text_key)`:
     - Gettysburg (19 readers)
     - the LibriVox poems
     - the Speech Accent Archive paragraph
     - EARS regular reads
   - The build needs these changes: `Group` per text (dataset.py:188-194), ids without "gettysburg_" (dataset.py:210), same-text pairs in `r2_nulls` (calibrate.py:77-91), and the corpus mount in the build kernel's `dataset_sources`.
   - **Native-English filter:** use only the native-English Speech Accent Archive readers, the same as the lab's `normal_reader` (lab/evaluate.py:90-97). This is a data-scope choice. **Owner decision.**
   - **Sampling:** k = 5 seeded references per participant. Each group has equal weight in the rate. Reader ids must not contain ">" (calibrate.py:166).
3. **Three reader-disjoint sets per group, fixed by a hashed id list before any lab result is read (academic defect 3).**
   - **fit:** used for scales and h.
   - **select:** used for the promotion test and the measure choices.
   - **lockbox:** used once, at the final gate.
   - The lab has already seen its own bank and held readers (lab/evaluate.py:121-138). The lockbox therefore comes only from readers absent from the lab feature table. If a group has no such readers, it has no lockbox. If the lockbox total is under 20 readers: **owner decision**.
   - The current 9 Gettysburg check readers become select-set readers, because they are contaminated (DESIGN.md:103).
4. **Statistics (academic defect 4).**
   - Report every per-key rate with a reader-cluster bootstrap 95 % upper bound and the rule-of-three bound.
   - Choosing h on the bootstrap bound instead of the point rate is a protocol change. **Owner decision.** The default is the point rate plus the reported bound.
   - `r2_stability` becomes leave-one-group-out.
5. **Promotion test (from calibration, criteria fixed in §8).**
   - D7+ and D8+ start as "listed": the unscored `differences` panel at no budget cost (pipeline.py:168-212).
   - A key is promoted only if all of these hold:
     - With the key enabled, refit all keys at the new equal share.
     - On the select set, the null rate is within budget.
     - The candidate meets its recall criterion.
     - No existing key loses more than one away-edit detection.
6. **Consensus reference** (K bank references, flag if at least m of K flag; the lab's `median_reference` is at lab/evaluate.py:100-115): this is an API change. **Owner decision.** It stays off by default.

## 4. Explanations

- **Fields.** Every finding keeps the full `build()` key set and gains these fields:
  - `pattern`
  - `evidence`: the secondary numbers
  - `span_kind`: word, sub-word, boundary or sentence
  - `group`: the ids of the member findings
  - `candidate`: true for any label that comes from the decode or from the stability run
- **D7 label order.** The first test that holds sets the label. Each label shows its evidence span:

  | Order | Label | Test |
  |---|---|---|
  | 1 | block | within-word silence ≥ BLOCK_S, minus the reference's silence in the same word |
  | 2 | word or sound repetition | a decode insertion that copies the word or a prefix of it at prompt index i−1 or i, with no insertion by the reference at that index |
  | 3 | filled pause | an orphan voiced run |
  | 4 | prolongation | a stability run that passes the low-F0 condition; the onset or rhyme form comes from the half of the word that holds the run |
  | 5 | lengthened word | none of the tests above holds |

- **Thresholds are not tuned to the recipes.** The thresholds for these labels come from report values and lab nulls, not from the recipe levels. The text never claims a cause that only the synthetic data supports.
- **Template:** "At 12.31–12.95 s, 'liberty': a silence of 0.64 s inside the word before its release; the reference has none (2.6 × the normal reader-to-reader spread). This is the pattern of a block [WHY quote, source]. Try: …"
- **Candidate clause.** Labels marked candidate add: "Automatic label; low precision on real speech; listen to the span." This uses the D6 pattern (explain.py:155).
- **Subtype text for existing keys.** These subtypes add their evidence to the text of the existing key:
  - natural rushing: the tempo decomposition
  - low effort: alpha down, with the F0 drop as supporting evidence
  - trailing off: the last-word drop
  - hesitation: pause plus stretch
  - word-by-word: the number of events and the mean run length

## 5. Evaluation and dataset interplay

- **R1 claims count as synthetic sensitivity only (academic defect 1).** Most new measures copy the recipe operation:
  - block silence ≥ 0.5 s
  - uneven tempo = `word_duration_ratio_sd`
  - ending window 0.25 s
  - the effort knobs

  R1 F1 and the pattern confusion matrix are reported under the heading "recovery of the synthetic edit". Claims of "detects X" come only from Real results:
  - AVID soft vs normal (effort)
  - EARS styles
  - LibriStutter, SEP-28k and DisfluencySpeech events (D7)
  - PodcastFillers (filled pause)

  On Real data, matching uses the lab's both-edges rule (lab/evaluate.py:67-78).
- **Matching.** For D7 and D8 the headline uses the both-edges rule (0.20 s). The current index-or-overlap rule (events.py:95-99) is reported as a secondary column.
- **Base rate.** Report PPV at 0.21 % stuttered syllables (disfluency REPORT:332) for D7 on fluent readers.
- **R1 selection.** `select_r1` keeps its no-recall-loss eligibility rule over the 8 core types only (calibrate.py:153-155), and `CALIBRATE_EXTRA` stays False. This keeps the released protocol and the cap from weak extra types.
  - D7 and D8 take the common R1 h. D2 and D4 already do this as event keys. With per-key robust scales, every z is in robust units, so this does not mix units (minimal defect).
  - Their control firings count as FP in the objective (calibrate.py:149-150).
  - Setting `CALIBRATE_EXTRA = True` is a protocol change. **Owner decision.**
- **Leakage controls:**
  - All iteration happens on val.
  - `final_gate` allows one test run per hash and needs the calibration manifest hash (evaluate.py:995-1010).
  - The lockbox is used once.
  - Real corpora are never used for fitting.
  - The recipe constants stay outside the detector hash; they are covered by the manifest hash.
  - The §8 criteria go into DESIGN.md before any lab result is read.
- **Dataset.** The wiring engineer adds the extra clips (dataset.py:291-305; `EXTRA_SINGLE_LEVEL_SETS` and `EXTRA_CROSS_CLIPS`, config.py:281-293). This design changes only the registry primaries (§2), and they must be agreed with that engineer before their work is merged.

## 6. Dashboard needs (app.js)

- Add D7 and D8 to `ROWS`, `ROW_OF_DIM`, `VALUE_UNIT` and `TYPE_TEXT` (app.js:20-39). They are "word" rows with markers at their finite units.
- Draw a sub-word wash from the finding's `p` span (in s). Draw an outline around the members of a `group`.
- Add a pattern chip and a filter beside the dimension filter (app.js:160, 187), and a candidate badge.
- Add a "Listed, not scored" panel for the unpromoted R2 keys.
- Add a clip card for the D7 clip flag. Detect a whole-passage finding by `context` only (app.js:49).
- Show the notices from the detector's `enabled` list.

## 7. Implementation steps, each with its test

1. **Refactor with no change in behaviour:** `UNIT_KIND`, `is_event`, `dim_of`, `KeyError` explanations, hash placement.
   - Test: with the current detector.json, decode, scores and findings on the fixture pairs are byte-identical, and the hash is unchanged.
   - Test: the hash-coverage test from §2 passes.
2. **Alignment cache with greedy words and character spans.**
   - Test: a cache round trip, and the greedy words are equal to the lab's (lab/extract.py:98).
3. **Move the features from the lab into features.py.**
   - Test: the lab measures are numerically unchanged on the lab fixtures.
4. **Per-key event scales (D2 first).**
   - Test: recalibrate R1 and R2 on the current data and report the D2- threshold and the recall on dropped pauses against the release.
   - This is a protocol change on existing keys: **ask the owner before the run.**
5. **Grouped null pool with fit, select and lockbox sets, k-sampling, the per-clip rate and leave-one-group-out stability.**
   - Test: on synthetic nulls, the fitted rate is within the share for each key.
   - Test: the select-set rate is recorded against 1.03.
6. **`d7_word_time` and `d8_ending`, with coverage and `reference()`.**
   - Test: on an identity pair, every x ≈ 0.
   - Test: for each recipe at L3, the peak of the primary dimension is at the labelled unit, and the placebo gives no unit above h.
7. **patterns.py and the one-penalty score rule.**
   - Test: the decoded regions are unchanged by the grouping.
   - Test: identity = 100, and the score gates hold on train.
8. **Explanations and pipeline schema 2.**
   - Test: every (dim, sign, subtype) renders, an unknown key raises, and the JSON has the full key set.
9. **events.py and evaluate.py: literals, new types, the both-edges matching column, PPV and the Real section.**
   - Test: an evaluation smoke run on a small set; `truths()` accepts every registry type.
10. **Apply the §8 lab decisions** and run the promotion test on the select set.
    - Test: the promotion table is written, with rate, bound and recall for each key.
11. **Kaggle:** dataset build, calibrate, evaluate on val. Then the critics.
12. **Dashboard.**
    - Test: an API smoke run on a WORD_REPETITION clip shows a sub-word wash, a pattern chip and the listed panel.
13. **After the owner's review:** one final run (test plus lockbox).

## 8. Decisions the lab results must settle, with acceptance thresholds

Write these criteria into DESIGN.md before any lab result is read. They are design values.

**Lab gate.** Every measure must first pass the lab's own rule (lab/evaluate.py:399): held-out false rate ≤ 0.05 per contrast and found share ≥ 0.5 on every corpus. The product gate then also applies, after the measure is ported and decoded with the product's region rule on the select set:
- the null rate is within the key's equal share, and the bootstrap upper bound is reported
- L3 cross-clip recall ≥ 0.5
- for measures with Real data: AUC ≥ 0.70, with a reader-cluster bootstrap lower bound > 0.5

**Decisions per measure:**

| Measure | Lab inputs | Accept if | Fallback |
|---|---|---|---|
| D7 timing | `word_duration_ratio`, `orphan_voiced_gap` | lab gate on LibriStutter, SEP-28k and DisfluencySpeech | R1 only; R2 listed |
| D7 repetition label | `inserted_material` with the reference floor | precision ≥ 0.5 on Real | label dropped; shows "lengthened word" |
| D7 prolongation label | `stability_run`, tested with and without the low-F0 condition | the better variant passes | label dropped |
| D7 block label | `within_word_silence` | passes on Real | label dropped |
| Filled pause | orphan run at 0.15 s and at 0.20 s | precision ≥ 0.5 on PodcastFillers | not shipped |
| D8 comparison stretch | earlier part of the final word against the preceding word | the stretch with the higher held AUC, if it passes | declination slope as text only; R1 only |
| Low-effort subtype | `alpha_ratio` on AVID soft vs normal | passes | "quieter (level only)" text |
| Trailing-off subtype | `last_word_drop` with pause-delimited phrases | passes | plain D5 text |
| Natural-rushing text | `speech_time_ratio`, count difference | passes | plain D1 text |
| D2- relative unit | the pause measures | recall on dropped pauses improves with no loss in the null rate | absolute unit with the per-key scale |
| Uneven-tempo clip key | `tempo_irregularity` (MAD form) | passes | not shipped |
| D4+ | `two_sided_emphasis` | passes | D4- only |
| Repeated contour | none | none | not shipped (fixed) |

**Owner decisions still open:**
- the per-clip false rate
- the native-English filter
- selecting h on the bootstrap bound
- the size of the lockbox if it is small
- `CALIBRATE_EXTRA`
- consensus reference
- the per-key D2 scale (step 4)
- the change of the HESITATION primary to D2 (agree with the wiring engineer)

**Main files:**
- src/cvoice/config.py
- src/cvoice/compare.py
- src/cvoice/detect.py
- src/cvoice/calibrate.py
- src/cvoice/events.py
- src/cvoice/evaluate.py
- src/cvoice/explain.py
- src/cvoice/pipeline.py
- src/cvoice/lab/evaluate.py
- build/work/kaggle_runs/dev_v8/x/eval/results.json
- models/detector.json