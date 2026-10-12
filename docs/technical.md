---
title: 'Contrastive Voice: reference-relative speech analytics'
subtitle: 'Multimodal AI Hackathon 2026, Track C: technical report'
author: 'Team Void'
date: 'Final evaluation of detector configuration 782d7df7 (Kaggle, 2026-10-07 IST); report of 10 October 2026'
fontsize: 10pt
papersize: a4
geometry: margin=1.15cm
colorlinks: true
header-includes:
  - \usepackage{microtype}
  - \setlength{\emergencystretch}{3em}
  - \setlength{\parskip}{1pt}
  - \setlength{\tabcolsep}{3pt}
  - \renewcommand{\arraystretch}{0.88}
  - \usepackage[nobottomtitles*]{titlesec}
  - \renewcommand{\bottomtitlespace}{0.05\textheight}
  - \usepackage{etoolbox}
  - \AtBeginEnvironment{longtable}{\footnotesize}
  - \setlength{\LTpre}{3pt}
  - \setlength{\LTpost}{3pt}
  - \titlespacing*{\section}{0pt}{5pt}{1pt}
  - \titlespacing*{\subsection}{0pt}{3pt}{1pt}
  - \usepackage{enumitem}
  - \setlist{nosep,leftmargin=*}
  - \usepackage{newunicodechar}
  - \newunicodechar{≥}{\ensuremath{\geq}}
  - \newunicodechar{≤}{\ensuremath{\leq}}
  - \newunicodechar{θ}{\ensuremath{\theta}}
  - \usepackage{multicol}
  - \usepackage{needspace}
  - \usepackage{titling}
  - \setlength{\droptitle}{-3em}
  - \setlength{\intextsep}{3pt}
  - \setlength{\textfloatsep}{3pt}
  - \setlength{\abovecaptionskip}{2pt}
---

**Summary.** Contrastive Voice aligns a reading with a reference reading of the same words, measures nine delivery quantities (D1 to D9) at the same words in both, and returns time-stamped flagged regions with a measured explanation, a cause label and a cost in points. In regime R1 (an edited copy of the reference recording), core-8 test event F1 at levels 2–3 is **0.812** under the pre-registered accounting (all predictions counted; TP 28, FP 9, FN 4; per speaker 0.800 and 0.824) and 0.879 when duplicate detections of one change count once (an accounting introduced after the plan). The test split was scored once before, on 2026-10-02 under an earlier configuration (`32cdd86f…`, all predictions counted: 0.879). In regime R2 (a different reader, the regime of every upload), held-out readers give 0.46 false regions per comparison-minute (upper 95 % bound 0.54) with one reference; level-3 rush and dropped-pause edits are mostly missed (1 of 18, 4 of 17). Every flaw is a synthetic signal edit; no listener has rated the clips. Two later features (section 10) leave every number above unchanged. Sources of numbers: `docs/evidence_final_782d7df7/`; papers and citation chains: `docs/PAPERS.md` (same reference numbers). Detail left out for length: [evidence_final_782d7df7/report_detail.txt](evidence_final_782d7df7/report_detail.txt) (sections 2–9) and [evidence_post_final/report_detail.txt](evidence_post_final/report_detail.txt) (section 10).

*Judging criteria:* data engineering and stress testing, sections 2 and 6.4; causal explainability and temporal grounding, 5; feature extraction, 3 and 4; dashboard, 7; reproducibility and code quality, 8.

# 1. Problem and approach

Judging rubrics name delivery problems ("poor pacing", "speaks in monotone", "too soft") but give no numeric thresholds [1–4], and trained raters agree poorly on vocal delivery: two expert raters gave the same "vocal expression" score on 30 % of presentations [2]. The system therefore compares a performance with a reference rendition of the same text, word by word, as coaching systems and reference-based prosody evaluation do [32, 103]: both recordings are force-aligned to the transcript, each quantity is measured on the same words, and a difference is flagged when it exceeds a threshold fitted on comparisons without flaws (nulls). The detector is a threshold rule; there is no trained classifier.

| Regime | Participant compared with | Thresholds fitted on | Scored keys | Used for |
|:------------------|:--------------------------------------------|:-------------------------------------------|:--------------|:------------------------------------------|
| R1 same recording | an edited copy of the reference recording | train identity and placebo nulls, edits | D1–D6, D9 | evaluation clips; gallery examples marked R1 |
| R2 single | one reading of the same text by another person | R2 null pool fit set (985 readings) | D1, D2, D3, D5 | uploads against the Reagan passage or an own reference |
| R2 consensus of 5 | the word-by-word median of five other readings | the same fit set, five references | D1, D2, D3, D5 | uploads against the Gettysburg bank (six readings) |

Regimes are never pooled. The R1 F1 measures recovery of edits inside one recording, not a comparison between two readers, which is what every upload is (`app.py`, `UPLOAD_REGIME = "R2"`).

# 2. Data engineering

**Sources and licences.** Baselines: 9 public-domain US government speeches (Wikimedia Commons), split by speaker 5 train / 2 val / 2 test. R2 calibration bank (6), check readers (3) and never-fitted pair (1): 10 readings under a public-domain dedication (LibriVox Gettysburg Address; Greenman reading of the Reagan passage). R2 null pool: Speech Accent Archive (779, CC BY-NC-SA 4.0), EARS (856, CC BY-NC 4.0), LibriVox poetry and Gettysburg (308, public domain). Non-commercial audio is used for calibration and evaluation only, in private Kaggle outputs.

**Rebuild from public origins.** `data/sources_manifest.json` lists the 19 source recordings with URL, SHA-256 and licence basis; the build stops on a hash mismatch. `kaggle/data/fetch.py` downloads the reader corpora from their origins and checks each member; `kaggle/run.py` builds the dataset, calibrates, evaluates and builds the gallery. The final build's dataset manifest has sha256 `d67c9cd9…` (`STATUS.json`); the development build of 2026-10-06 reported the same hash (its outputs are not published).

**Flaw synthesis.** A flaw is a controlled edit of a clean recording at one of three levels, spliced back with exact word, sample and time labels. Eight core types: RUSH and DRAG (D1), PAUSE_DROPPED and PAUSE_INTRUSIVE (D2), MONOTONE (D3), DEEMPHASIS (D4), FADE (D5) and MUMBLE (D6); at level 3, for example, speech time ×1.90, a pause cut to 0.06 s, 1.20 s of inserted room tone, no F0 range left and a 14 dB fade. Fifteen further types cover natural rushing (words ×1/1.13 to ×1/1.18, pauses shrunk), hesitation, disfluencies, low effort, trailing off, endings and others. Duration edits use waveform-similarity overlap-add and pitch edits Praat PSOLA; chain B (evaluation only) uses Praat duration and WORLD-vocoder pitch; identity and placebo clips pass the same processing. These tools are named without citation because their papers are not recorded as read. Each edit is measured again after synthesis: 118 realisation shortfalls are recorded and 82 events are excluded from truth. Synthetic errors helped learned detectors of real errors [105], but a learned detector can also key on synthesis artefacts [106]; this detector learns only its thresholds from the edits.

**Dataset.** 2410 audio files, 1109.2 minutes: 9 baselines, 1953 reader recordings and 448 edited clips. R1 single-level clips per split: train 90 (5 speakers), val 36 (2), test 36 (2). The dataset card lists every recording with its source and licence (`docs/evidence_final_782d7df7/dataset_card.md`).

**R2 null pool.** The 1943 null readings form 30 same-text groups from four sources. Readers are split once, before fitting, into fit (985: thresholds), select (707: budget check, not tuned) and lockbox (251 planned, Accent Archive and poetry only, opened only by `evaluate --final`; measured once on 192 accent and 45 poetry readers). Sources carry equal weight.

# 3. Feature extraction

**Alignment.** torchaudio `WAV2VEC2_ASR_BASE_960H` emissions and a CTC Viterbi pass over the supplied transcript give word start and end times at 20 ms resolution. The published word-boundary error of wav2vec 2.0 CTC alignment is 48 ms (TIMIT) and 89 ms (Buckeye) [100]; it was not measured on these recordings.

**Frames and windows.** Frames are 25 ms with a 10 ms hop. Level is frame dB minus the recording's median over voiced frames, so a uniform gain cancels. F0 is Praat's autocorrelation tracker [44] in two passes, the second with floor and ceiling from the recording's own quartiles [45], in semitones from the speaker's median [41]. A pause is the longest silent run of at least 0.20 s inside an inter-word gap [30, 32]. Window keys use five-word windows clipped at sentence boundaries, centred on the clip median g, which is a separate whole-clip measure for D1 and D3.

**Keys.** Each x is participant minus reference at the same words; status is given as R1 / R2.

- **D1 pace** (scored / scored): ln ratio of speech time (pauses removed) in the window, minus g; articulation rate [14], same-text comparison [26].
- **D2 pauses** (scored / scored): silence at a word boundary (s); drops only after reference pauses ≥ 0.5 s, insertions only at unpunctuated boundaries [30, 32].
- **D3 pitch range** (scored / scored): ln((P90 − P10 + 1 st) / same for reference), minus g; narrower only [41, 43].
- **D4 emphasis** (scored / shown): loss of a stress statistic (duration per syllable, P90 pitch, P90 level) at the reference's stress words [57].
- **D5 volume** (scored / scored): window mean level re own median in dB, minus g; drops only [66].
- **D6 clarity proxy** (scored / shown): ln ratio of frame-to-frame change of MFCC 1–12, minus g; drops only [75]; no source validates this proxy.
- **D7 word time** (listed): ln ratio of word occupancy (word plus orphan voiced time) [83, 85]. **D8 ending** (listed): final 0.20 s minus earlier part of a sentence-final word, in st [95].
- **D9 speech tempo** (scored / listed): ln ratio of summed word durations in the window, not centred [19, 20].

"Listed" means shown on the page and never scored: D7 because its lab gate failed on LibriStutter and no synthetic disfluency edit was recovered; D8 by owner decision (the RISING_ENDING recipe mostly does not realise, and val has 2 eligible ending events); D9 in R2 by owner decision after 0 of 68 R2 rush positives in development run v13. A pattern label is on only if it passed a real-data lab gate fixed before the results (12,868 recordings, 48 tests): natural rushing and the filled-pause candidate (PodcastFillers precision 0.54, recall 0.15) passed; six other labels failed and are off.

# 4. Detection and calibration

**Rule.** For key $k$, $z = x/s_k$ with $s_k = \max(\mathrm{floor}_k,\ 1.4826\,\mathrm{MAD},\ Q_{68}(|x|))$, weighted over the regime's nulls [104]. A region opens where $\mathrm{sign}\cdot z \geq h$ and extends over the contiguous run with $\mathrm{sign}\cdot z \geq \max(h/2,\ 0.5\,z_{\mathrm{peak}})$ (pitch range: $h/2$ only); sentence boundaries end runs; D2 and D4 are single events. Whole-clip flags compare g (D1, D3) with own thresholds.

**R1 selection (train only).** R1 nulls differ from the reference by almost nothing, so the scales sit at their floors. One h for D1–D6 maximises in-sample strict F1 on train core-8 and NATURAL_RUSH edits (L2+L3) plus the train controls: **h = 2.15** (F1 0.835; 680 of 1000 bootstrap draws choose 2.15). D9 has its own h, constrained to a threshold at or above the clean alignment-noise floor (0.1484 ln): **h = 3.05**, the lowest allowed grid value.

**R2 selection (fit set only).** Each enabled key takes the smallest h whose false regions per comparison-minute on the fit nulls stay within an equal share (0.0833) of a 0.5/min budget; whole-clip thresholds for D1 and D3 are the fit quantile of a separate clip budget (0.05 false clip flags per null clip, 0.025 per key). The bootstrap upper bound is reported, not used.

**Resulting thresholds.** R1: pace ×1.227 slower / ×0.815 faster, pause ±0.3225 s, pitch range kept ×0.485, volume −4.3 dB. R2 single reference: pace ×2.194 / ×0.452, pause +0.981 / −1.504 s, pitch range ×0.273, volume −10.08 dB. The R2 thresholds are set by how much two competent readers differ; they lie far above the perceptual values in [13, 40, 66] (limit 11). All thresholds: section 4 of the [detail file](evidence_final_782d7df7/report_detail.txt).

**Scores.** The severity of a flagged unit is $\mathrm{clip}((|x|-\theta)/(a_k-\theta),\,0,\,1)$ with threshold $\theta = h\,s_k$ and a fixed saturation $a_k$ near the L3 magnitude. Weighted severities sum to a penalty $P_k$; the key score is $S_k = 100\max(0,\,1 - P_k/P_{\max,k})$ and the overall score is the mean of the scored $S_k$. One factor (0.4584) scales every $P_{\max,k}$ and is fixed on train so that identity clips score 100, level-1 clips at least 90, G5 at most 50, and each ladder is non-increasing: 0 violations on train, val and test.

**Frozen detector.** `models/detector.json`, sha256 `d5935d3f…`, configuration `782d7df7…`; the repository file is byte-identical to the file the final evaluation measured.

# 5. Causal explainability and temporal grounding

**One change, one cause, one penalty.** One shared function (`patterns.py`) decides, for scoring, display and evaluation alike, which regions belong to one change: a D9 region near a D1 region of the same direction measures the same change (`SAME_CHANGE`), and a frozen registry links, for example, a fade to the emphasis loss it causes. Each group shows one title cause and costs one penalty. The rush cause follows the recipes' mechanism: core RUSH compresses words and keeps pauses; natural rushing also shrinks them [15, 16].

**Cause-label accuracy (R1, synthetic edits, val and test, L2+L3).** The shown label equals the injected type for 56 of 59 detected core-8 edits and for 7 of 13 detected synthetic-only edits (limit 18). Keys that fire per injected dimension: `docs/evidence_final_782d7df7/figures/activation_matrix.png`.

**Temporal grounding.** Pause findings have a median edge error of 10 ms (onset) and 29 ms (offset) over 16 val and test events; window findings have five-word resolution (limit 16). The errors are measured against analytic edit labels, not hand-marked boundaries.

**Explanations.** Each finding is a template filled from measured values, with no language model (model output is not repeatable at settings called deterministic [117]). It gives the words and times in both recordings, both values, the threshold, a next step (goal, current state and next step [111]; specific and task-focused [113]) with the reference as the contrast [114], and a counterfactual: the score with this penalty removed [115]. Example (gallery, L3 set A, R1): *"Faster here: 15.80-17.14 s … 86% faster (3.0x the threshold; flagged above 23%). … score with this penalty removed: 91.0."* A cause claim needs evidence at the interventional level [116]. The repair test supplies it for synthetic edits: undoing the edit removes the flag in 12 of 12 (val) and 10 of 10 (test) repairs, and a placebo edit keeps it in 12 of 12 and 10 of 10.

# 6. Evaluation

## 6.1 Plan and accountings

A plan written on 2026-10-02 ([text at commit c2204b2](https://github.com/WinterBlossom0/contrastive-voice/blob/c2204b2/docs/FINAL_EVALUATION_PLAN.md), first committed 2026-10-08), before any test number of this configuration existed, fixed the headline: R1, test split, levels 2–3, strict one-to-one event F1 with all predictions counted; windows match at IoU ≥ 0.5, pause and emphasis events by the labelled boundary or word [107, 108]. The test split and the R2 lockbox are evaluated only by `evaluate --final`, once per configuration hash (`models/final_evaluations.json`) [110]. The *one-detection-per-change* accounting, introduced after the plan, counts a same-change D9 region on a rush edit as its detection or as a duplicate, not as a false region. The earlier test evaluation (2026-10-02, configuration `32cdd86f…`, no D9 key; `docs/evidence_final_32cdd86f3d6e/`) was seen before the redesign; both results are reported side by side, there is no third test run, and no design choice of the rework used a test result.

## 6.2 R1 results (same recording, synthetic edits)

Counts are TP/FP/FN (pre-registered) and TP/FP/same-change duplicates/FN (one per change). Train intervals are speaker-bootstrap percentiles over 5 speakers (coverage not assured); val and test give the two per-speaker values, not intervals.

| Core 8 | Pre-registered: TP/FP/FN, F1 | One per change: TP/FP/dup/FN, F1 | Earlier final, 32cdd86f |
|:-------------------|:-------------------------------|:---------------------------|:-------------------|
| Train L2+L3 (in-sample) | 74/20/6, **0.851** [0.795, 0.907] | 76/8/10/4, 0.927 [0.885, 0.969] | 76/16/4, 0.884 |
| Val L2+L3 (development) | 30/13/2, **0.800** (0.769, 0.833) | 30/9/4/2, 0.845 (0.811, 0.882) | 30/12/2, 0.811 |
| **Test L2+L3** | 28/9/4, **0.812** (0.800, 0.824) | 29/5/3/3, 0.879 (0.848, 0.909) | 29/5/3, 0.879 |
| Test L1 (sensitivity) | 3/2/13, **0.286** | 5/0/0/11, 0.476 | 10/0/6, 0.769 |

Per type at test L2+L3 (one per change): 4 of 4 for each core type except MONOTONE 2 of 4 and DEEMPHASIS 3 of 4. Natural rushing (D9): test F1 0.167 (limit 1). Synthetic-only tier, test L2+L3: F1 0.211 in both accountings; WORD_BY_WORD 0 of 28, because the D2 threshold (0.3225 s) is above every recipe silence (0.15–0.30 s). Unedited test copies (identity and 5 placebo variants): **0 false regions in 5.89 comparison-minutes** (val 0 in 5.93); they come from 0.98 independent recording-minutes, so the 0.5/min budget is not measurable on them.

## 6.3 R2 results (different speaker)

| Null set (no edits) | One reference: false regions/min (pooled) [upper 95] | Median of five | Whole-clip flags per clip (one / five) |
|:----------------------|:----------------------------------------------|:-----------------------------------------------------|:---------------------|
| Fit (sets thresholds) | 0.491 (0.450) [0.545], met | 0.468 (0.457) [0.564], met | 0.046 / 0.050 |
| Select (checked, not tuned) | 0.549 (0.482) [0.640], not met | 0.536 (0.401) [0.670], not met on covered sources | 0.046 / 0.068 |
| **Lockbox (held out, once)** | **0.460** (0.522) [0.538], met on covered sources | **0.516** (0.530) [0.684], not met on covered sources | 0.057 / 0.084 |

Rates weight sources equally; the budget is 0.5/min and 0.05 per clip. The lockbox covers Speech Accent Archive and poetry readers only. R2 detection has no held-out positive test (limit 8; every check-reader type: section 6.3 of the [detail file](evidence_final_782d7df7/report_detail.txt)).

## 6.4 Stress matrix: measured degradation

Eleven channel conditions are applied to the participant only; each row gives false regions added per minute and the share of original detections kept. Val and test have 2 speakers each; per-speaker and per-key rates: `stress_by_speaker` in `docs/evidence_final_782d7df7/addendum.json`.

| Condition | R1 val: added/min, kept | R1 test: added/min, kept | R2, one reference: added/min |
|:---------------------------|:-----------------------|:-----------------------|:-----------------------|
| Gain +6 / −6 dB | 0.21, 1.00 / 0.28, 1.00 | 0.14, 1.00 / 0.28, 1.00 | 0 / 0 |
| MP3 64 kbit/s | 0.07, 1.00 | 0.14, 1.00 | 0 |
| Low-pass 3.4 kHz | 0.38, 0.96 | 1.46, 0.94 | 0 |
| WORLD speaker transform | 0.94, 0.96 | 0.76, 0.99 | 0 |
| Room reverb RT60 0.4 s | 0.89, 0.95 | 0.61, 0.99 | 0 |
| White noise 20 dB SNR | 2.63, 0.91 | 1.85, 0.91 | 0.26 |
| Phone band + mu-law | 1.84, 0.89 | 5.52, 0.87 | 0.39 |
| Dynamic-range compression | 6.48, 0.78 | 2.60, 0.76 | 0 |
| Babble 20 dB SNR | 8.41, 0.89 | 13.2, 0.85 | 0.13 |
| Babble 10 dB SNR | 24.5, 0.65 | 26.2, 0.60 | 2.06 |

The R2 column uses the check readers; its zeros rest on 7.76 comparison-minutes (limit 17).

\needspace{6\baselineskip}

## 6.5 Baselines

| Core 8, L2+L3, F1 | Val | Test |
|:---------------------------------------------------------------------|:--------------|:--------------|
| Detector, pre-registered / one per change | 0.800 / 0.845 | 0.812 / 0.879 |
| Flag everything / random regions | 0.016 / 0.045 | 0.016 / 0.056 |
| Reference-free (participant against itself), detector h / train-chosen h 2.75 | 0.217 / 0.218 | 0.247 / 0.261 |
| Reference-free with its own scales and h (added after the final evaluation) | 0.295 | 0.407 |

The baseline rows use the one-detection-per-change accounting; no pre-registered value was computed for them. Without a reference the same measurements find fewer edits with more false regions (test, own scales: TP 12, FP 15, FN 20).

## 6.6 Further checks

*Directional test:* a higher level should not raise the edited key's score; 5 violations in 205 cells. *Chain B:* 24 A/B pairs, 22 detections on each chain, equal false regions on every pair. *Device:* 6 clips, 8 recordings, GPU against CPU, 0 ms word-time difference, identical flags. *Repeatability:* two analyses of one clip give byte-identical JSON (89,227 bytes).

# 7. Dashboard

A FastAPI server and one static page. Cards follow the brief's categories (cadence, pauses, tone, volume, clarity proxy); each key is marked scored, listed or not scored, with the reason. Charts overlay both recordings on the participant's time axis with tolerance bands and flagged regions. Uploads (up to 180 s) are analysed in R2 against the Reagan passage, the Gettysburg bank (median of five) or an own reference, or with no reference (10.2); each finding can be edited and heard (10.1). A browser harness checks every gallery example against its result JSON at 320 to 1440 px: 0 failures, 0 console errors.

![The local app, gallery example "Level 3, set A" (R1): score, time view of both readings, and the button that edits every finding and analyses the result again.](img/tech_dashboard.png){width=72%}

# 8. Reproducibility and code quality

The final run was one Kaggle kernel (cvoice-build version 19, 2 × T4): 7228.9 s in total, `STATUS.json` complete with no failed stage. The kernel checks the staged source hashes and installs the locked environment (`uv.lock`). Hashes: dataset manifest `d67c9cd9…`, detector `d5935d3f…`, configuration `782d7df7…`, `results.json` `49a306d9…`. The evaluation addendum and the gallery were computed afterwards on CPU from the saved outputs (`scripts/rebuild_after_final.sh`); its re-run of the frozen detector on the saved audio of 162 clips reproduces the saved counts in 24 of 24 rows. Tests (CI, 2026-10-12 IST): 654 passed, 4 skipped (they need the final-run outputs), 11 slow deselected; the slow integration test (a mini dataset build through the gallery) passed in 1110.57\ s; `ruff check --select F,E9` is clean. Evidence: `docs/evidence_final_782d7df7/` with `SHA256SUMS`; `README.md` gives the rebuild steps.

# 9. Limits

Limits of the final run, numbered as in the review that confirmed them; breakdowns and full wording are in section 9 of the [detail file](evidence_final_782d7df7/report_detail.txt).

- **1. Speech tempo (D9) cannot resolve the natural-rush recipe.** The recipe shortens word time by ×1.13, ×1.15 and ×1.18 at levels 1–3 (ln −0.122, −0.140, −0.166); the R1 D9 threshold, 0.149 ln (×0.86), is above the level-1 and level-2 change and only 0.017 ln below the level-3 change. D9 measures 21–67 % of the applied compression and detects 4 of 18 natural-rush edits at levels 2–3 (train 2/10, val 1/4, test 1/4), none with both edges within 0.20 s. The lab evidence for natural rushing measured a different quantity.
- **4. Timing measures pick up aligner errors from non-timing changes.** Level, spectrum, noise or channel changes move the forced-alignment word boundaries, so faster or slower words can be reported where the timing did not change: in the gallery, a low-effort edit (pitch, spectral tilt and gain only) was reported as "91 % faster" (3.25 points). Under purely acoustic stress the timing keys add false regions well above their 0.0556/min share of the budget, for example 1.98/min (val compression, D2-). A 640 ms word-boundary shift on identical audio samples has no resolved cause.
- **8. R2 detection has no held-out positive evidence beyond one pair.** The R2 lockbox measures false regions only; R2 positives come from 3 check readers used during development, and the one never-fitted pair (Greenman against Reagan) detects 4 of 36 away-edits. With a single reference, level-3 pace and pause edits are mostly missed (rush 1/18, dropped pause 4/17, drag 6/17); pitch-range and volume edits are found (monotone 17/18, fade 13/18).
- **11. The R1 headline does not measure real use.** Every upload is compared as R2, where a local pace flag needs speech ×2.19 slower or ×0.45 faster than the reference reader and a dropped pause must be 1.50 s shorter. The level-3 rush edit is found in 1 of 18 check comparisons, the level-2 rush edit in 0 of 13 and the level-3 dropped pause in 4 of 17, so the expectation "level 3 flagged for pace and pauses" is not met in R2.
- **12. The R2 false-region budget holds only on covered sources with equal source weights.** Lockbox: 0.46 false regions per comparison-minute with one reference (0.52 pooled; upper95 0.54), 0.52 with the median of five (upper95 0.68); Accent Archive readers 0.65, poetry readers 0.27; four first languages exceed the budget, up to Amharic 1.28/min (5 readers). Whole-passage false flags (0.057 and 0.084 per clip) exceed the 0.05 budget. The 0.5/min budget is not established at upper95 in any R2 set; EARS and Gettysburg readers are not in the lockbox.
- **13. Speech tempo (D9) is scored in R1 at the noise floor and is the noise-sensitive key.** Its threshold is 0.0004 ln above the clean alignment-noise floor (h 3.05, the lowest grid value allowed); noise-degraded identity clips reach 0.318 ln, about twice the threshold; white noise at 20 dB SNR adds 1.2 speech-tempo regions per minute in val.
- **16. Temporal grounding of window findings is coarse.** Window findings (pace, pitch range, volume, clarity) have five-word resolution: 14 of 35 matched window regions have both edges within 0.20 s (monotone 0/6); the monotone onset error has a 90th percentile of 867 ms.
- **17. The stress test uses synthetic transforms only; R2 stress rests on 22 recordings and 7.8 check-reader minutes.** No condition is a real second channel (another microphone or room); device agreement covers GPU against CPU only. Babble, compression and phone-band audio break pauses, volume, pace and pitch range: up to 26.2 added regions per minute, 60–78 % of detections kept under babble 10 dB and compression; under babble 10 dB, R2 keeps 1 of 24. A 6 dB gain change moves one test clip's score by up to 15.5 points; only the maximum change was recorded.
- **18. No human judgement validates the delivery index or the cause labels.** No listener rating has been collected; scores and labels are checked only against synthetic edits of known cause. Deemphasis is the weak case (4 of 7; shown 2 times as monotone, 1 time as rush); low effort and trailing off are shown as fade. The rush / natural-rush label is correct for every detected rush and natural-rush edit, but its constant comes from the recipe parameters, and its lab evidence used a different timing measure.
- **19. The test split has 2 speakers and was evaluated once before; all baselines are US political addresses.** The per-speaker values are ranges, not confidence intervals. The earlier evaluation (0.879) was seen before the redesign, which raised the R1 h from 1.7 to 2.15 (speech tempo 3.05), halved the level-1 hits and added speech-tempo duplicates: test level 1 fell from 0.769 to 0.286 pre-registered (0.476 one per change); test L2+L3 fell from 0.879 to 0.812 pre-registered and is unchanged one per change. Train level 1 had already fallen (0.746 to 0.431) before the test run.

# 10. Added after the final evaluation

Detector `782d7df7…`, its thresholds and every pre-registered number above are unchanged. Evidence with checksums: `docs/evidence_post_final/` (`INDEX.txt`); full method, check rows and limits: [evidence_post_final/report_detail.txt](evidence_post_final/report_detail.txt).

## 10.1 Fix your speech: edit the reading, then analyse it again

**Method** (`repair.py`). For one finding or all, the participant's own recording is edited toward the finding's target and analysed again with the original settings: WSOLA time scaling (pace, speech tempo); room tone inserted or silence shortened (pauses); PSOLA scaling of the speaker's own pitch excursions or, as an option, the reference melody (pitch range) [128, 129]; pitch, length and gain together (emphasis); gain ramps (volume). Other keys are not edited, with the reason given. This is the interventional counterpart [116] of "score with this penalty removed". **Caps** are extrapolated from whole-utterance listening tests [120–124]: duration ×0.7 to ×1.4 per round and ×1.5 per word in all; pitch 3 st per round and 4 st in all; gain 6 dB per word, without a quality source [66, 69]; inserted pause 2.0 s. The page never says "Fixed": a finding is *No longer flagged*, *Still flagged · partly changed*, *Not edited* or *Can't be fixed by editing*.

**Evidence** (product setting: own pitch, one round; the 14 flagged gallery clips, all synthetic edits; no test data):

- Same detector after the edit: 37 of 62 findings no longer flagged (23 full edits, 10 capped, 4 covered by a capped edit); a new finding in 2 of 14 runs. Dose: flag gone at strength 1 in 42 of 59 findings, at 0.5 in 27.
- Controls: processing-only PSOLA on 17 whole clips, 0 flag changes; sham edits, 13 of 45 made a new flag, 0 in an unrelated dimension; clean regions (175 trials), 6 new flags in an unrelated dimension.
- Detector-free instruments: Praat pause change within 0.05 s in 19 of 25; A-weighted level within 1.5 dB in 19 of 24 (first criterion) and 24 of 24 (frame check, introduced after those 5 misses).
- Recovery on 10 R1 clips (median share of the injected change undone): PAUSE_DROPPED 0.97, RUSH 0.74, FADE 0.43, MONOTONE −0.04 with own pitch (0.96 with the reference melody).

**Limits.**

- Closed loop: the edit targets the detector's measure and the same detector judges it, so *no longer flagged* shows detector consistency and edit execution, not better delivery (as in a published re-score of corrected contours [130]).
- All clips are synthetic edits, repaired by inverse operators of the same tool set; no natural flaw was tested. Gain does not restore effort; an inserted pause has no boundary lengthening.
- No listening result: a blind MUSHRA-style test (12 spots) is designed and pending; there is no perceptual evidence yet.
- Own pitch rarely edits a flattened contour: all three gallery MONOTONE findings are skipped; the reference-melody option has no perceptual test.
- Without a reference only pause edits were checked: on 985 fit-phase readings, 32 longer-pause findings; 2 remove a majority phrase break.

**Novelty.** Own-voice prosody correction [125, 131] and scoring of modified learner audio [132, 133] exist; as far as the search found, the added part is the per-flag re-analysis by the same detector, with processing-only, sham, dose and detector-free controls.

## 10.2 No reference: a rough check

**Design** (`selfref.py`, `models/detector_selfref.json`). Each measure is compared with the speaker's own typical value: D1 and D9 window time against the time expected from CMUdict phone counts; D2 against the speaker's median pause of the boundary class [141]; D3 against the median less a declination offset [70, 97]; D5, D6 against the median. D4, D7 and D8 need a reference and are absent. One h per key maximises the R1 objective on train under a budget of 0.5 false regions per minute on train nulls and 167 Gettysburg and poetry fit-phase readers. Text-expected durations follow [138–140]; such pause and monotone checks exist commercially [146]; no novelty is claimed.

**Single test run** (2026-10-10 09:45 IST; `detector_selfref.json` sha256 `6dd3adc5…`, equal to the repository file). Core 8, levels 2–3, one detection per change; intervals are count-level bootstrap (`docs/evidence_post_final/f1_intervals.txt`), not clustered by the 2 test speakers. **What a reference adds:** with the same measures, test F1 is 0.36 without a reference and 0.812 / 0.879 with one.

| Test, core 8, L2+L3 | TP/FP/dup/FN | Precision | Recall | F1 [95 %] |
|:-------------------------------------------------------|:------------------|:------|:------|:----------------|
| Without a reference (pre-registered accounting: 0.353) | 9/9/1/23 | 0.50 | 0.28 | 0.36 [0.18, 0.51] |
| Reference-free lower bound (section 6.5) | 12/15/0/20 | 0.44 | 0.38 | 0.407 [0.23, 0.55] |
| R1 with a reference (pre-registered / one per change) | 28/9/–/4, 29/5/3/3 | | | 0.812 / 0.879 |

**Limits.**

- Validation core-8 decided 15 or more design choices, so its F1 (0.429) is optimistic; validation readers (Accent Archive 0.59/min, EARS 0.35/min) chose between variants.
- Level 1: 0 of 16; natural rushing 0 of 4. Unedited test copies: 12 false regions in 5.89 min (2.04/min), but these are 2 distinct events: exact 95 % interval 0.25–7.4/min, inconclusive against the 0.5/min budget. `results.json` keeps no per-change outcomes, so no paired comparison is possible.
- The score gate fails (G5 clips score 97.85–100 on train; gate ≤ 50), so the page counts flagged spots instead of a score and calls the mode a rough check.
- The listed, unscored articulation rate uses a published norm [18] that 15–47 % of clean fit-phase readers fall outside.

# 11. AI assistance

The AI tool used is Claude Code. The research reports, the source code and tests, the data pipeline and Kaggle kernels, the calibration and evaluation, the dashboard and the documents, this report included, were produced with Claude Code under the owner's direction. The owner made the design decisions: scope and flaw types, data sources, the threshold-only detector, the speaker splits, the evaluation rules and the single final evaluation.

\begingroup\scriptsize

# References

Full entries and the use of each paper: `docs/PAPERS.md`.
[1] Schreiber, Paul & Shibley (2012), The development and test of the Public Speaking Competence Rubric, *Communication Education* 61(3) (read in [2]).
[2] Joe, Kitchen, Chen & Feng (2015), A prototype public speaking skills assessment, *ETS Research Report* RR-15-36.
[3] Morreale et al. (eds.) (2007), *The Competent Speaker Speech Evaluation Form*, 2nd ed., NCA.
[4] Judging instruments: NSDA Declamation Starter Kit; Poetry Out Loud Judge's Guide 2021–22; Toastmasters ballot Item 1172; UIL Criteria for Evaluating Persuasive Speakers.
[13] Quené (2007), On the just noticeable difference for tempo in speech, *J. Phonetics* 35(3).
[14] de Jong & Wempe (2009), Praat script to detect syllable nuclei and measure speech rate automatically, *Behav. Res. Methods* 41(2).
[15] Trouvain & Grice (1999), The effect of tempo on prosodic structure, *Proc. 14th ICPhS*.
[16] Janse (2004), Word perception in fast speech, *Speech Communication* 42(2).
[18] Jacewicz, Fox, O'Neill & Salmons (2009), Articulation rate across dialect, age, and gender, *Language Variation and Change* 21(2).
[19] Cucchiarini, Strik & Boves (2000), Quantitative assessment of second language learners' fluency by means of ASR technology, *JASA* 107(2).
[20] Suzuki, Kormos & Uchihara (2021), The relationship between utterance and perceived fluency: a meta-analysis, *Modern Language Journal* 105(2).
[26] Duong, Mostow & Sitaram (2011), Two methods for assessing oral reading prosody, *ACM TSLP* 7(4).
[30] Campione & Véronis (2002), A large-scale multilingual study of silent pause duration, *Speech Prosody 2002*.
[32] Hallur et al. (2026), Reference-based prosody and rhythm evaluation for spoken dialogue systems, arXiv:2606.31055.
[40] 't Hart (1981), Differential sensitivity to pitch distance, particularly in speech, *JASA* 69(3).
[41] Hincks & Edlund (2009), Promoting increased pitch variation in oral presentations with transient visual feedback, *LLT* 13(3).
[43] Niebuhr & Skarnitzl (2019), Measuring a speaker's acoustic correlates of pitch – but which?, *ICPhS 2019*.
[44] Boersma (1993), Accurate short-term analysis of the fundamental frequency and the harmonics-to-noise ratio of a sampled sound, *Proc. IFA Amsterdam* 17.
[45] Hirst (2011), The analysis by synthesis of speech melody, *J. Speech Sciences* 1(1).
[57] Suni, Aalto & Vainio (2015), Hierarchical representation of prosody for statistical speech synthesis, arXiv:1510.01949.
[66] Caswell-Midwinter & Whitmer (2019), Discrimination of gain increments in speech-shaped noises, *Trends in Hearing* 23.
[69] Eriksson & Traunmüller (1999), Perception of vocal effort and speaker distance on the basis of vowel utterances, *ICPhS 1999*.
[70] Pierrehumbert (1979), The perception of fundamental frequency declination, *JASA*.
[75] Smiljanić & Bradlow (2009), Speaking and hearing clearly, *Language and Linguistics Compass* 3(1).
[83] Goto, Itou & Hayamizu (1999), A real-time filled pause detection system for spontaneous speech recognition, *Eurospeech 1999*.
[85] Zhu, Caceres & Salamon (2022), Filler word detection and classification: a dataset and benchmark, *Interspeech 2022*.
[95] Chung & Bidelman (2022), Acoustic features of oral reading prosody and the relation with reading fluency and reading comprehension…, *JSLHR* 65.
[97] Yuan & Liberman (2014), F0 declination in English and Mandarin broadcast news speech, *Speech Communication* 65.
[100] Huang et al. (2024), Less peaky and more accurate CTC forced alignment by label priors, arXiv:2406.02560.
[103] Liang, Li, Rackauckas & Hirschberg (2026), A survey of automated presentation coaching, arXiv:2606.27380.
[104] NIST/SEMATECH, *e-Handbook of Statistical Methods*, §1.3.5.17, Detection of outliers.
[105] Korzekwa et al. (2022), Computer-assisted pronunciation training: speech synthesis is almost all you need, *Speech Communication* 142.
[106] Geirhos et al. (2020), Shortcut learning in deep neural networks, *Nature Machine Intelligence* 2(11).
[107] Heittola & Mesaros, `sed_eval`: evaluation toolbox for sound event detection (source code).
[108] Bilen et al. (2020), A framework for the robust evaluation of sound event detection, *ICASSP 2020*.
[110] Cawley & Talbot (2010), On over-fitting in model selection and subsequent selection bias in performance evaluation, *JMLR* 11.
[111] Wisniewski, Zierer & Hattie (2020), The power of feedback revisited, *Frontiers in Psychology* 10.
[113] Shute (2008), Focus on formative feedback, *Review of Educational Research* 78(1).
[114] Miller (2019), Explanation in artificial intelligence: insights from the social sciences, *Artificial Intelligence* 267.
[115] Wachter, Mittelstadt & Russell (2018), Counterfactual explanations without opening the black box, *Harvard J. Law & Technology* 31(2).
[116] Pearl (2019), The seven tools of causal inference, with reflections on machine learning, *CACM* 62(3).
[117] Atil et al. (2024), Non-determinism of "deterministic" LLM settings, arXiv:2408.04667.
[120] Choi et al. (2021), Neural analysis and synthesis (NANSY), *NeurIPS 2021*.
[121] Rudresh, Vasisht, Vijayan & Seelamantula (2018), Epoch-synchronous overlap-add (ESOLA), arXiv:1801.06492.
[122] Roberts & Paliwal (2020), A time-scale modification dataset with subjective quality labels, *JASA* 148(1).
[123] Charpentier & Moulines (1989), Pitch-synchronous waveform processing techniques…, *Eurospeech 1989*.
[124] Bae & Joo (2022), Timbre-preserving pitch augmentation in FastPitch, arXiv:2204.05753.
[125] Hirose, Gendrin & Minematsu (2003), Japanese lexical accent training with corrective feedback in learner's voice, *Eurospeech 2003*.
[128] Bissiri, Pfitzinger & Tillmann (2006), Lexical stress training… by means of resynthesis and emphasis, *SST 2006*.
[129] Nolan (2003), Intonational equivalence: an experimental evaluation of pitch scales, *15th ICPhS*.
[130] Peabody & Seneff (2006), Towards automatic tone correction in non-native Mandarin, *ISCSLP 2006*.
[131] Ai & Xu (2015), A system demonstration of a framework for computer assisted pronunciation training, *ACL-IJCNLP 2015 System Demonstrations*.
[132] Zhao, Koh & Luke (2012), Accent reduction for computer-aided language learning, *EUSIPCO 2012*.
[133] Zhang et al. (2021), Masked acoustic unit for mispronunciation detection and correction, arXiv:2108.05517.
[138] Duong & Mostow (2010), Adapting a duration synthesis model to rate children's oral reading prosody, *Interspeech 2010*.
[139] Cheng (2011), Automatic assessment of prosody in high-stakes English tests, *Interspeech 2011*.
[140] Suzuki, Kato & Tamura (2022), Automatic prosody evaluation of L2 English read speech…, *Interspeech 2022*.
[141] Taylor & Black (1998), Assigning phrase breaks from part-of-speech sequences, *Computer Speech & Language* 12.
[146] Microsoft, Azure AI Speech pronunciation assessment, documentation.

\endgroup
