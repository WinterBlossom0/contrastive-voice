# Temporal grounding and the lightest defensible method

Date: 2026-10-01. Topic: `grounding_model`. Research only; no product implementation or audio/model/simulation computation was performed in this session.

## Recommendation

**Use a calibrated, signed, per-dimension threshold detector as the final method.** Force-align both recordings to the same verified transcript, compare physical acoustic quantities at matching words or inter-word boundaries, divide by a declared regime-specific tolerance scale, and decode regions with deterministic offline hysteresis. Keep pretrained alignment separate from the detector: “no learned flaw detector” does not mean “no pretrained acoustic model.” CPU-only is sufficient in principle; end-to-end Kaggle latency remains unmeasured here.

**UNVERIFIED — design recommendation:** remove the logistic regression and boosted detector from DESIGN_v0. The contribution is the labelled contrastive spectrum, calibration, measurement quality, and faithful temporal feedback. “Contrastive” means paired renditions and controlled interventions; do not call this contrastive learning. No runtime LLM, learned severity regressor, learned embeddings, or probability head is needed.

The critic is right **for this build**, not as a universal theorem about learned models. Published synthetic augmentation improves learned lexical-stress/pronunciation detection on real non-native speech. That is evidence that learning can help with a suitable target and validation set; it is not evidence that adding learning to eight synthetic oratory sources improves this method. There is no experiment here establishing superiority of thresholds either. This is a choice under data, explanation, and compute constraints. [Korzekwa et al. 2021](https://www.isca-archive.org/interspeech_2021/korzekwa21_interspeech.html), [Korzekwa et al. 2022](https://arxiv.org/abs/2207.00774). **VERIFIED_BY_SOURCE** for those published findings; the build decision is **UNVERIFIED**.

Claim to ship: “Localises controlled acoustic departures from a reference rendition, at word/boundary resolution, using tolerances calibrated on the stated comparison population.” No claim of human delivery-quality accuracy, judge agreement, exact inferred boundaries, or universal human speaker invariance.

## 1. Critic adjudication

The issue text is in `../../design/critique_academic_v0.md`; the lead draft is `../../design/DESIGN_v0.md`.

| Item | Decision and reason | What remains empirical |
|---|---|---|
| I-02, cross-speaker labels | Accept the mismatch diagnosis. Store intervention labels separately from reference-departure labels. Use clean/edited twins and signed difference-in-differences; classify edits that reduce a pre-existing departure as repairs. | R2 incremental detection, pre-existing regions, cancellations, and new flags outside the intervention. |
| I-03, null scale | Accept separate measurement and between-performance strata; speaker transforms are invariance tests. Add offset-aware dispersion while retaining zero as the reference origin (§4). TTS is a synthetic reference population, not a natural-human null. | Human–human spread and held-out-speaker false alarms. |
| I-05, leakage | Accept grouping by source speaker, holding out voices, and in-fold calibration. Freeze this architecture before results; all Reagan/JFK probe passages are development material. | Locked manifest, calibration artifacts, untouched test outputs. |
| I-09, A/B/C | Accept thresholds alone for shipping. Exact linear contributions are valid algebra, but do not establish stable causes or quality validity. Reject the implication that every learned model must be useless. | A later learned alternative would need matched false-alarm rates and an independent target. |
| I-13, meaning of z | Accept: this is a tolerance multiple, not a Gaussian significance or probability. Calibrate the complete multi-dimension decoder in false regions/minute. | Target versus achieved rate, tails, correlations, missingness. |
| C-01, C-02 | Cut boosted and logistic runtime detectors, including neighbour-mean inputs. Feature context and region decoding already provide smoothing. | No model-selection contest on the same tiny test set. |

**VERIFIED_BY_SOURCE:** Cawley–Talbot show that selection overfitting can be as large as differences between algorithms; this supports refusing a tiny A/B/C leaderboard, not an assertion of statistical impossibility. [Paper](https://www.jmlr.org/papers/v11/cawley10a.html).

Two refinements to the critic matter. First, a zero-centred MAD-only rule can still become intolerant when a null has a large systematic offset and tiny spread; account for absolute null magnitude (§4). Second, “present after, absent before” detects new threshold crossings only. It misses worsening of an already flagged region, so also report continuous signed change and existing-region escalation (§5). Neither correction requires a learned model.

## 2. Alignment and temporal coordinate system

**VERIFIED_BY_SOURCE:** FA maps the transcript to audio, but modern CTC boundaries are not sample-exact. Huang et al. Table 1 gives wav2vec2 word-boundary error 48 ms on TIMIT and 89 ms on Buckeye, with mean predicted word durations below manual durations. Those are benchmark observations, not this system's error bars. [Huang et al. 2024](https://arxiv.org/html/2406.02560v3), saved check `web/source_checks_2026-10-01.json`. Rousso et al. also found MFA more accurate than the compared MMS/WhisperX configurations. [Rousso et al. 2024](https://arxiv.org/abs/2406.19363), earlier fetched excerpts in `sources/tts_evaluation_prior_excerpt.txt`.

| Alignment | Benefit | Failure mode / timing consequence | Choice |
|---|---|---|---|
| Independent word FA on the common transcript | Semantic correspondence; retains real pace and pause differences; explains named words | Wrong transcript, omissions/repetitions, noise, short CTC word ends; confidence is not boundary accuracy | Primary. Reject unscorable spans rather than forcing correspondence. |
| Phone FA | Useful for pronunciation and phonetic duration | Pronunciation lexicon and extra uncertainty; not necessary for phrase-scale delivery | Optional QA, not a required detector input. |
| Global acoustic DTW | Aligns unequal lengths without a transcript | Can erase the pacing anomaly being detected; MFCCs encode speaker/channel; repeated sounds admit wrong paths | Diagnostic only. |
| Subsequence DTW | Can locate a short passage in longer audio | Partial/multiple matches; cannot certify missing words or exact boundaries | Passage-search aid, followed by transcript verification and FA. |
| Soft-DTW | Differentiable alignment loss | No benefit without training; smoothing is not a discrete timestamp path | Omit. |

**VERIFIED_BY_SOURCE:** for costs C(a,b), DTW minimizes `sum C(a,b)` over monotone paths with steps `(1,0),(0,1),(1,1)`. Soft-DTW uses `-γ log sum_path exp(-cost(path)/γ)` for γ>0 and approaches the minimum as γ→0. Its differentiability serves learned sequence objectives, not temporal-quality evidence. [Cuturi–Blondel](https://arxiv.org/abs/1703.01541); DTW controls and subsequence mode: [librosa API](https://librosa.org/doc/main/generated/librosa.sequence.dtw.html), previously fetched in `RUN2_condensed.md:1640–1745`.

**UNVERIFIED — precise proposed contract:** canonical comparison audio is 16 kHz mono; feature hop 10 ms. Store original sample/time mappings. FA emits `word_id, start_s, end_s, confidence, valid`; punctuate the verified transcript separately. Use the aligner chosen by the alignment topic, with its locked model checksum. Do not adopt this topic's historical mismatched torch/torchaudio install (§9) as a deployable pin. No second SSL encoder is required.

For the overlay, sorted paired word-start/end anchors `(t_B,k,t_P,k)` define `φ(t_P)=t_B,k+(t_P-t_P,k)(t_B,k+1-t_B,k)/(t_P,k+1-t_P,k)` between anchors. Require positive interval lengths; invalid or collapsed anchors break the map. The inverse map is similarly piecewise linear where strictly monotone. The dashboard plays **true participant times**, with baseline playback obtained from the associated word IDs. Do not use warped time to compute duration, pauses, or event metrics. See `../dashboard/REPORT.md` for the UI contract.

Deleted pauses need a semantic boundary ID: a missing interval has no participant-time extent. Return a boundary marker plus the reference gap and zero/short participant gap. Never fabricate a positive-duration ground-truth region to make IoU work.

### 2.1 Objective metrics used in synthesis / conversion

**VERIFIED_BY_SOURCE:** prior fetched ESPnet scripts use mel-cepstral DTW for MCD and log-F0 RMSE. The prosody-transfer paper also uses pitch/voicing errors and describes padding rather than making DTW universal. Sources: [ESPnet MCD](https://raw.githubusercontent.com/espnet/espnet/master/egs2/TEMPLATE/asr1/pyscripts/utils/evaluate_mcd.py), [ESPnet F0](https://raw.githubusercontent.com/espnet/espnet/master/egs2/TEMPLATE/asr1/pyscripts/utils/evaluate_f0.py), [Skerry-Ryan et al.](https://arxiv.org/abs/1803.09047); excerpts in `sources/tts_evaluation_prior_excerpt.txt`.

For alignment path `A={(a_l,b_l)}`, both-voiced subset V, and cepstra in the declared convention:

- `MCD = (1/|A|) Σ_l (10/ln 10) sqrt(2 Σ_{k=1}^K (c_B,a_l,k-c_P,b_l,k)^2)` dB. This report excludes c0; implementations differ, including the earlier fetched ESPnet script, so record the actual coefficient set and normalization. MFCC Euclidean distance is not automatically this MCD.
- `LF0_RMSE = sqrt((1/|V|) Σ_{l∈V} (ln F0_B,a_l-ln F0_P,b_l)^2)`. Semitone RMSE multiplies this by `12/ln 2`. Use speaker-centred semitones for this build's contour diagnostic.
- `ρ_F0 = Σ_V(x-x̄)(y-ȳ) / sqrt(Σ_V(x-x̄)^2 Σ_V(y-ȳ)^2)`. Undefined if either variance is zero. Correlation can be 1 despite a large scale difference; always show magnitude separately.
- `VUV_error = (1/|A|) Σ_l 1[v_B,a_l≠v_P,b_l]`; `GPE = Σ_V 1[|F0_P-F0_B|>0.2 F0_B]/|V|`.
- `FFE = (number of V/UV mismatches + number of both-voiced gross pitch errors)/|A|`; these two sets are disjoint. Empty voiced subsets produce NA, not zero.
- `duration_RMSE = sqrt((1/N) Σ_i ((e_P,i-s_P,i)-(e_B,i-s_B,i))^2)` seconds, using the original timelines. **UNVERIFIED — proposed diagnostic**, not evidence of human quality.

MCD is a spectral reconstruction diagnostic, not a cross-speaker delivery score. Raw pitch errors punish biological F0 differences. DTW distance cannot replace the preserved time-warp/duration measurements.

## 3. Final detector specification

All constants and feature decisions in this section are **UNVERIFIED — preregistration defaults**, not measured optima or literature-established flaw thresholds. Source-backed principles and remaining validation are distinguished below. No computed null scale or calibrated h exists yet.

### 3.1 Units and physical features

`B` is reference, `P` participant. A word window is five words centered at i, clipped at punctuation-defined sentence boundaries; require at least three words for pace/pitch. Inter-word pauses are a separate boundary stream. Evaluate only matching, valid units. Silence for pauses requires an independent acoustic silence/VAD check; CTC blanks are not a silence detector.

Pitch frames: `q_R,t=12 log2(F0_R,t/median_valid(F0_R))` semitones. Energy: `L_R,t=20 log10(max(RMS_R,t,10^-8))`, normalized as `ℓ_R,t=L_R,t-median_speech(L_R)`. Define `RMS_t=sqrt(Σ_n w_n x_t,n^2/Σ_n w_n)` with nonnegative Hann weights over 25 ms and a 10 ms hop; speech masks must exclude silence/noise-only frames. Pitch uses the chosen tracker's actual analysis window, not an assumed 25 ms window.

Do not divide pitch by its own SD or energy by its own SD: that would erase range reductions. Do not subtract a per-pair delta median after these definitions. Centre levels to tolerate F0 register and file gain, accepting their identifiability limits (§3.4). Normalizers are computed per submitted recording; this is deterministic preprocessing, not access to test labels.

| Dimension | Primary scalar and signed delta `δ_i` | Positive / negative directions | Scale floor `ε_d` |
|---|---|---|---|
| Pace | `r_R,i=n_words/(end_last-start_first)` in the word window; `δ=ln(r_P/r_B)` | Faster / slower reference-relative local speaking rate; includes within-window pauses | `ln(1.05)` |
| Pausing | Energy-verified gap `g_R,i`; retain gaps ≥0.20 s, otherwise zero; `δ=g_P-g_B` when either is present | Added/lengthened / shortened/missing gap | `0.10 s` |
| Pitch variation | `R_R,i=Q90(q_R)-Q10(q_R)` over voiced frames in the word window; `δ=R_P-R_B` | Wider / narrower contour span | `0.50 st` |
| Emphasis | `A_R,i=Q90(q_R over word i)-median(q_R over its window)`; `δ=A_P-A_B` | Increased / reduced **pitch-accent proxy** | `0.50 st` |
| Volume contour | `E_R,i=median_speech(ℓ_R over word i)`; `δ=E_P-E_B` | Local surge / local relative fade | `1.00 dB` |
| Spectral clarity proxy | `C_R,i=10 log10(E[2–7.5 kHz]/E[0.1–7.5 kHz])`, using speech-frame STFT band power; `δ=C_P-C_B` | Display both; detect reductions only, R1 only | `1.00 dB` |

The band-power denominator must be positive and numerator above numerical noise; otherwise missing. Use 512-point FFT at 16 kHz, Hann 400 samples, hop 160. This “clarity” quantity measures spectral balance, not intelligibility. It is a single auditable proxy for the synthetic spectral edit; do not label it GOP or mumbling accuracy. R2 clarity stays visible but is excluded from flags and aggregate indices pending channel validation. Spectrogram/MFCCs may be display diagnostics; no classifier consumes them.

For pitch window statistics require ≥10 voiced frames (100 ms nominal support); for the accent word require ≥5. Missing pitch, bad alignment, or invalid spectral power is missing evidence, never zero deviation. Report valid coverage and abstentions by dimension. Confidence thresholds depend on the aligner's score definition: obtain a training-only lower fifth-percentile threshold on verified-correct development words as an initial outlier gate; this gate alone cannot validate a transcript. Hard transcript mismatches stop scoring affected spans.

Using one primary quantity per dimension makes the decision faithful, but intentionally narrows the claim. Emphasis also involves duration/intensity, and a multi-cue or human-validated prominence estimator could help later; the pitch proxy is not a proof of semantic stress. Do not require content-word eligibility to score it: that would build a label-position shortcut into detection.

### 3.2 Region decoder

Compute `z_d,i=δ_d,i/s_d,regime` and decode each allowed sign separately; for one-sided spectral reduction use `-z`. No probabilities. For threshold h, low threshold is `h/2`.

1. Find maximal connected runs of valid units with signed `z>h/2`.
2. Retain a run only if at least one unit has signed `z>h`. This offline two-sided expansion recovers a low-amplitude shoulder before the first high crossing, unlike forward-only hysteresis.
3. Do not bridge a below-low word, missing unit, sentence boundary, or opposite sign. `merge_gap_words=0`; onset/offset padding `0 s`.
4. Minimum run: pace/pitch two consecutive scored words; emphasis/volume/clarity one word. Do not add a common 200 ms minimum that deletes valid short-word events.
5. Region endpoints are the first flagged word's start and last flagged word's end on **P**. Preserve the wider feature-support window in the explanation: five-word context can smear a boundary by up to two neighboring words. Pauses bypass the word decoder and receive boundary events with their measured gaps.

Runtime complexity after extraction is linear in units × dimensions. **UNVERIFIED:** no ranking of decoder boundary accuracy is established here. A direct one-feature threshold with the same support and false-alarm calibration is the mandatory simpler comparator.

### 3.3 Region alternatives, fairly compared

| Method | What it can add | Why not selected |
|---|---|---|
| Fixed threshold | Least code, sharp high crossings | Fragments gradual changes; retain as baseline. |
| Offline hysteresis | Contiguous moderate evidence around a strong departure | Adds low/high ratio; fixed here, not tuned to test F1. |
| CUSUM | Accumulates weak sustained shifts: `S_i^±=max(0,S_{i-1}^±±z_i-k)` | Best for sequential change alarms; onset/offset recovery needs another rule; correlated windows invalidate usual ARLs. |
| PELT | Global piecewise-constant fit minimizes `Σ segment_cost+β number_changes` | Fits normal phrase shifts too; penalty/cost need calibration; no inherent semantic labels. |
| Binary segmentation | Fast greedy change search, typical `O(n log n)` cost evaluations | May miss close/short changes; same labelling problem. |
| HMM/CRF | Can learn duration/transition or contextual behavior | Needs credible states/labels, transition priors and tuning; can suppress short prominence/pauses. |
| Moving/median smoothing | Reduces isolated fluctuations | Adds boundary blur; neighboring context already exists in selected features. |

**VERIFIED_BY_SOURCE:** CUSUM favors small mean shifts; PELT has conditional efficient pruning, not unconditional linear worst-case cost; post-processing choice matters in sound-event detection, without establishing an oratory winner. [NIST CUSUM](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm), [ruptures PELT](https://centre-borelli.github.io/ruptures-docs/user-guide/detection/pelt/), [Truong et al. review](https://arxiv.org/abs/1801.00718), [post-processing study](https://arxiv.org/abs/1906.06909). Earlier source texts: `sources/region_methods_prior_excerpt.txt`, `PREVIOUS_RUN_condensed.md:376–461`. The report does not repeat the earlier log's inconsistent numerical claim about that study's F1 gain.

### 3.4 Identifiability and explanation

F0 centering removes register, not range. Energy centering removes global gain: uniformly quiet uploads cannot be scored as a located fade. Global rate and F0 range remain measurable reference differences, but cannot be declared bad habits versus legitimate style from one reference. Report whole-recording descriptors separately. Median normalization can mask long edits and create apparent opposite changes outside them; restrict headline localized single-edit evaluation to ≤35% of scorable words and test coverage 10%, 25%, 35%, 50%, 75%, 90% separately. A small span policy does not solve long-coverage uploads; label that result out of the validated range.

Each output stores `dimension, sign, word_ids/boundary_id, participant_interval, reference_interval, feature_support, raw_B, raw_P, delta, units, scale, null_stratum, high_threshold, low_threshold, validity, context, explanation`. Include sentence/clause position and what the reference does. Say “0.4 s longer than the reference, 3.8 times the calibrated tolerance,” not “3.8 sigma significant” or a detection probability. Runtime feedback is a deterministic template.

An explanatory rule is faithful to **its own decision**. Counterfactual repair must reprocess repaired audio and be compared with a placebo; dropping a region from a score is only an arithmetic counterfactual. Literature supports associations with listeners, not individual causal judgments. This addresses I-11/I-17/I-19 and J-07/J-08/J-15 in addition to the requested critic items.

**UNVERIFIED — optional display index, no learned map:** for each accepted word region use nonoverlapping flagged-word speech durations `t_i` and excess `v_i=max(|z_i|/h-1,0)` (use the permitted sign for one-sided dimensions). `B_d=Σ_i t_i v_i/T_valid,d`. For pauses use eligible boundary terms `max(g_B,i,g_P,i) max(|z_i|/h-1,0)/T_valid,pause`; this is a stated burden convention for absent intervals, not participant flagged-time occupancy. Display `S_d=100 exp(-B_d)` as **reference-match index**, with k=1 fixed by convention, and equal weights across enabled valid dimensions. Report each dimension and coverage; never turn an unscorable dimension into 100. This is not a validated judge grade. Hysteresis shoulders below h remain regions but add zero excess burden. The separate flagged-time metric uses actual interval unions. The rubric report's seven-dimension, multi-cue emphasis/clarity and fitted-score proposals must be revised or kept as display-only diagnostics; do not silently mix those formulas with this six-dimension detector.

## 4. Null-scale estimation protocol

### 4.1 Declare the population before estimating anything

| Stratum | Pair construction | Proper role |
|---|---|---|
| Identity | Same PCM versus itself | Sanity check only; zero deltas cannot estimate tolerance. |
| R1 measurement / placebo | Same performance, neutral resynthesis/splice/re-encode chains; benign gains/F0 shifts tested separately | `s_meas` and artifact sensitivity; processing-chain null. |
| R2 TTS–TTS | Different voices, same transcript, clean native readings | Synthetic between-performance tolerance, conditioned on engine. |
| R2 human–TTS | Human orator versus clean TTS | Synthetic reference-mismatch tolerance, not natural human variability. |
| R2 human–human | Independently read same verified passage, matched language/task/channel as far as possible | Preferred empirical between-performance population; no claim that all readers are rhetorically ideal. |

Never combine identity/transform zeros with R2 values in one MAD. Never average the three R2 populations according to available file counts. Default unknown uploads to an R2 calibration; allow R1 only for declared same-performance comparisons. If only TTS calibration exists, name its population and mark human-upload inference exploratory. A DSP pitch/formant transform supplies no new timing/pause variation.

**VERIFIED_BY_SOURCE:** the earlier fetched metadata `web/gettysburg150_meta.json` and LibriVox page identify 15 readers of the same public-domain address: [collection](https://archive.org/details/gettysburgaddress_150anniv_1311_librivox). It is a feasible external null, not an executed experiment. Check lexical versions and strip announcements before pairing. Existing CMU ARCTIC speakers share prompts and can provide read-speech nulls; the archive differs from oratory. [Kominek–Black](https://www.isca-archive.org/ssw_2004/kominek04b_ssw.html). Do not treat L2 accent as ground-truth rhetorical flaw.

**UNVERIFIED — data allocation recommendation:** collect clean renditions from ≥3 TTS voices without full ladders; one supra-threshold single intervention per dimension on a selected voice is enough for an initial R2 demonstration. A six-reader, 30 s human excerpt pilot gives six independent readers, not 15 independent pair observations. Prefer all 15 if the owner allocates null-only material; split reader IDs 9 fit / 3 calibration / 3 untouched test, recording the assignment before processing. One shared text cannot establish cross-text generalization. No new recordings or acquisition was launched here.

### 4.2 Estimate scale without moving the reference origin

Within each outer training fold and each **separate** stratum, give each source-speaker group equal total weight, then equal weight to pairs in a group and valid units in a pair. Preserve grouping in all diagnostics. With weighted quantiles `Q_w`:

`m_d = median_w(δ_d)`

`a_d = 1.4826 median_w(|δ_d-m_d|)`

`b_d = Q_w,0.682689492(|δ_d|)`

`s_d = max(ε_d, a_d, b_d)`; `z_d=δ_d/s_d`.

**VERIFIED_BY_SOURCE:** `1.4826 MAD` is a Gaussian-consistent robust dispersion convention; [NIST modified z](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm) and Rousseeuw–Croux's prior fetched abstract in `web/oa_batch1.jsonl` support the MAD definition. **UNVERIFIED — proposed conservative rule:** the extra absolute quantile keeps a consistently offset null from acquiring a tiny tolerance while maintaining `δ=0 ⇒ z=0`. The quantile equals one SD for an ideal zero-mean normal distribution, but no normal model or calibrated tail probability is assumed. Store m as a mismatch diagnostic; do not subtract it at inference. No claim that this max estimator is optimal.

For pauses compute dispersion on eligible boundaries where either recording has a verified gap ≥0.20 s; store present/absent probabilities separately. Both-absent boundaries remain in full-recording false-alarm evaluation. If a stratum has no eligible pauses or valid pitch, use the stated floor only for exploratory display and mark that dimension uncalibrated; do not silently claim a measured null. Physical floors prevent degeneracy, not statistical sufficiency. In the initial rule, gap changes below 0.20 s can be quantized away: report raw gaps too and count this as a known sensitivity limit, especially for near-perfect edits.

Store `source_ids, voice_ids, text_ids, valid_counts, unique_recording_minutes, weighted_pair_minutes, m,a,b,s,zero_fraction,Q95_abs,lag1_corr,excluded_units`. Dependence and tail shape are diagnostic, not reasons to convert z to p. Report `s_between/s_meas` per dimension, using like-for-like feature definitions.

### 4.3 Calibrate the complete system's operating point

**UNVERIFIED — default false-alarm budget:** `λ*=0.50` typed regions per minute **across all enabled dimensions and both directions combined**, per declared population. Overlapping dimension events count separately; do not calibrate 0.50 for every dimension and claim 0.50 overall. Also report the time union of all flags.

Fit scales on fitting groups. On disjoint calibration groups, evaluate the entire decoder at `h=1.00,1.05,…,12.00`, with low=h/2 and all other constants fixed. Weighted rate is `Σ_p w_p number_regions_p / Σ_p w_p (duration_P,p/60)`. Use equal total weights for source groups; retain raw counts/minutes too. Select the smallest h such that the **maximum calibration rate over that h and every larger grid value** is ≤λ*. Hysteresis fragmentation means event count is not necessarily monotone in h; do not rely on binary search. If no finite value qualifies, disable flags for that population rather than return a fake threshold.

For mixed R2 deployment supported by multiple available strata, estimate each independently and choose the componentwise maximum scale, then calibrate a common h that meets the budget separately in every calibration stratum. This is a conservative envelope, not a pooled natural-null estimate. A held-out-human rate is still required for a human claim. Otherwise use the named available population only.

With very few groups, prefer this one shared h to twelve independently tuned sign thresholds. Use leave-one-group-out inner calibration if a fixed fitting/calibration split leaves too little data: each calibration recording must be normalized with scales fit without its group; final scale refit on outer training groups. Verify the frozen resulting rule again on outer held-out nulls. Do not recalibrate on the outer test result.

The budget is an empirical operating target, not a guarantee. Zero false events over T null minutes has Poisson upper 95% rate `-ln(0.05)/T ≈ 3/T` only under that count model; correlated re-pairings make this approximation optimistic. More word comparisons cannot replace more independent speakers/minutes. Empirical/conformal ranks have resolution `1/(M+1)` with M calibration blocks and require exchangeability; not recommended as significance badges here.

## 5. Dataset semantics and cross-speaker protocol

For each text maintain `B` (reference), `P0` (clean other rendition), `P1` (intervened other rendition), and `Pplacebo` (neutral chain at the identical sampled span). R1 uses a clean/placebo version of the same performance; R2 keeps B fixed while P0/P1 change. Do not train a null on flawed P1 clips or treat all unedited TTS as “ideal.”

Each intervention stores chain/version, seed, ordered edits, source and output sample intervals, word/boundary IDs, monotone time-warp pieces, transition/crossfade supports, nominal parameters and **independently measured realized changes**. Labels may be multi-dimension and overlap. Preserve the intervention target separately from collateral changes caused by the generator. Do not define all ground truth using the detector's feature extractor: independently verify duration/energy from the edit map and pitch with another tracker.

Let `δ^0_d,i=Delta_d(B,P0)` and `δ^1_d,i=Delta_d(B,P1)` on matched units, where Delta is the dimension's actual definition in §3.1 (including the log ratio for pace). Then `e_d,i=δ^1_d,i-δ^0_d,i` is the paired intervention response, with fold scale fixed. For pace this equals `ln(r_P1/r_P0)`, not an arithmetic rate difference. It is a controlled contrast, not proof that human performance worsened. If per-recording normalizers shift, e can change outside the edited span; measure that explicitly.

For each dimension/sign `u∈{-1,+1}`, decode masks `M^0_u, M^1_u`. Newly flagged evidence is `N_u=M^1_u \ M^0_u` **in word/boundary coordinates**, not seconds. Group N with the same minimum-run rules; compare it to intervention support warped to P1. Report new events, pre-existing `M^0`, retained overlap, expanded existing events, and removed flags separately.

Define response `outward_change_u = u(δ^1-δ^0)/s`; also show change in `|δ|/s` for the two-sided dimensions. An edit that brings P closer to B is a **reference-relative repair/cancellation**, even if its recipe is called “slow pace” or “flatten pitch.” Do not count the absence of a new flag there as a flaw-detection failure. Conversely, an already flagged departure can worsen without a new crossing: report its magnitude change and escalation separately, not as zero sensitivity.

Two explicit analyses prevent label laundering:

1. **Intervention sensitivity:** over all interventions, report signed recovery and counts of newly detected, pre-existing/worsened, repaired, and undetected responses. This asks whether the controlled change is measured, not whether it is bad.
2. **Additional-departure detection:** preregister eligible reference-relative outward interventions from independent realized labels; report incremental event F1/recall and non-target new regions/minute on clean/placebo twins. Disclose eligibility and exclusion counts. Include cancellations as directional controls. Never present this conditional result as detection of arbitrary cross-speaker flaws.

For clean TTS/human reference pairs, call flagged regions “reference departures/minute.” They become **false alarms** only relative to a declared acceptance-null convention, not human-quality labels. If no verified reference-departure labels exist, do not calculate unconditional R2 precision against injected spans alone. This is the central answer to I-02.

## 6. Learned alternatives and prior art

Parameter counts below are **UNVERIFIED — explicit architecture arithmetic**, except published SSL sizes. They are not trained prototypes. Exact seconds and minimum data requirements are **unmeasured**; no honest literature lookup yields this build's CPU training time. “Tiny head” is not “tiny pipeline.” D=6 scalar deltas, K=12 signed output heads for comparison; the shipping detector enables fewer directions where appropriate.

| Candidate | Exact illustrative size | Data / CPU / risk | Explanation and decision |
|---|---|---|---|
| Statistical detector | 0 trained classifier parameters; scales and a shared h are estimated | Needs clean independent nulls, not positive training labels; linear decode | Exact triggering physical delta; select. |
| Logistic per signed class | `K(D+1)=84` coefficients/intercepts; 180 if D=14 | Can learn weights with regularization; repeated words are not independent examples; wall time unmeasured | `logit p=b+Σ w_j x_j` exact in log-odds, not probability contributions or audience causes; cut now. |
| Tiny boosted trees | 32 depth≤2 trees/head: at most 1536 leaf values and 1152 split nodes for K=12 | Learns interactions/quality gates; risks channel/engine shortcut; time unmeasured | Tree SHAP is model attribution, not acoustic mechanism; cut now. |
| Additive EBM | Bin/interactions dependent; not a fixed count | Can expose nonlinear feature functions; still needs credible labels and selection | Stronger interpretability than opaque tagger, unnecessary here. |
| 1D CNN / dilated TCN | Two k=3 convs, 6→16→16, then 16→12: `304+784+204=1292` parameters, no norm layers | Context receptive field 5 units (CNN), 7 with dilation 1,2; duration prior may overfit | Less transparent boundaries; no supported advantage. |
| One-layer BiGRU | Hidden 16/direction, PyTorch two biases: `2×3×16×(6+16+2)+12×33=2700` | Can model contextual patterns; gains need held-out generators/speakers; CPU time unmeasured | State attribution harder; omit. |
| Shared Siamese MLP | 6→16→8: `112+136=248`; weighted distance adds 8 nonnegative weights | Needs aligned positive competent pairs and genuine negatives, not just identities; shared weights counted once | Distance still needs dimension explanations; omit. |
| Frozen SSL + linear head | HuBERT Base 94.68M, WavLM Base 94.70M, wav2vec2 Base 95.04M; 768→12 head adds 9228 | Encoder dominates extraction and memory; speaker/channel content retained | No claim of invariance from freezing; omit extra forward pass. |

**VERIFIED_BY_SOURCE:** [WavLM paper](https://arxiv.org/abs/2110.13900) sizes and 20 ms stride/768 Base dimensions were previously fetched (`RUN2_condensed.md:2394–2414`). [SUPERB](https://arxiv.org/abs/2105.01051) evaluates frozen representations with lightweight heads, including speaker identification: SSL embeddings are not inherently speaker-free (`sources/ssl_prior_excerpt.txt`). [InterpretML](https://interpret.ml/docs/ebm.html) documents additive contributions. No SSL throughput benchmark for this task exists here.

If learning is revisited, the lightest honest **contrastive learning** option is a nonnegative diagonal metric over already normalized physical features: `D_w(B,P)=Σ_d w_d (f_P,d-f_B,d)^2/s_d^2`, with only six fitted weights. A triplet objective `max(0,margin+D_w(B,Pgood)-D_w(B,Pbad))` can fit it; constrain `w≥0, Σw=1`. This is **UNVERIFIED — future proposal**, not required to satisfy a paired contrastive dataset brief. Positive/negative pairs must share text and span, include genuinely different competent performances, and avoid TTS-engine identity shortcuts. InfoNCE `-log(exp(sim(a,p)/τ)/Σ_j exp(sim(a,j)/τ))` needs appropriate negatives; “all other words/speakers” teaches content or voice instead of delivery. [CPC](https://arxiv.org/abs/1807.03748), [supervised contrastive learning](https://arxiv.org/abs/2004.11362), previously fetched in `sources/learning_prior_art_prior_excerpt.txt`.

### 6.1 What the literature actually supports

| Literature | Verified finding | Transfer limit here |
|---|---|---|
| Witt–Young GOP; Kaldi recipe | Phone likelihood/posterior pronunciation assessment; phone GOP is not word-alignment confidence | Speech sounds and pronunciation, not rhetorical clarity or quality. [Kaldi recipe](https://raw.githubusercontent.com/kaldi-asr/kaldi/master/egs/gop_speechocean762/README.md). |
| Arias–Yoma–Vivanco | Reference-based intonation assessment for language learning | Prior art for contour comparison; not an oratory-region benchmark. [DOI](https://doi.org/10.1016/j.specom.2009.11.001), metadata in `web/oa_search1.jsonl`. |
| Hincks; Hincks–Edlund | Pitch-variation feedback/liveliness and speaker-normalized semitones | Supports relative pitch measurement, not a universal monotone-flaw cutoff. [Hincks](https://www.isca-archive.org/interspeech_2005/hincks05_interspeech.html), [feedback study](https://www.lltjournal.org/item/10125-44190/). |
| Wörtwein et al.; VoiceCoach | Multimodal assessment against expert judgments; interactive voice modulation examples | Their validation target/context differ; cannot borrow judge-validity claims. [Wörtwein DOI](https://doi.org/10.1145/2818346.2820762), [VoiceCoach DOI](https://doi.org/10.1145/3313831.3376726); prior abstracts `web/oa_batch2.jsonl`, `web/oa_search2.jsonl`. |
| Rosenberg–Hirschberg; Niebuhr et al. | Associations between acoustic prosody and charisma | Population/style/context dependent; not individual causal explanations. [Charisma DOI](https://doi.org/10.1016/j.specom.2008.11.001). |
| Korzekwa 2021/2022 | TTS augmentation plus attention detects real lexical-stress errors; 2022 real pronunciation AUC improves from 0.528 to 0.749 | Direct counterexample to “synthetic learning adds nothing”; different labels, data and target. [2021](https://www.isca-archive.org/interspeech_2021/korzekwa21_interspeech.html), [2022](https://arxiv.org/abs/2207.00774). |
| YOLO-Stutter; FluentNet | Synthetic dysfluency construction with natural-speech evaluation exists | Supports a separate real-transfer test; stutters are not delivery-score labels. [YOLO-Stutter](https://www.isca-archive.org/interspeech_2024/zhou24e_interspeech.html), [FluentNet](https://arxiv.org/abs/2009.11394). |
| CutPaste; Outlier Exposure | Synthetic/auxiliary anomalies can aid learned anomaly detection | Vision/text results do not establish speech transfer. [CutPaste](https://arxiv.org/abs/2104.04015), [OE](https://arxiv.org/abs/1812.04606). |

All rows are **VERIFIED_BY_SOURCE** for their limited statements; implications for this architecture remain **UNVERIFIED**. CTC path confidence is neither classical phone GOP nor calibrated intelligibility. Do not count memorized synthetic parameters as independent validation. No universal “minimum number of words” for safe model fitting is asserted.

## 7. Evaluation protocol

Everything below is **UNVERIFIED — an executable analysis specification for the later build**, not results.

### 7.1 Freeze, split, and create controlled examples

- Freeze detector family, feature definitions, support lengths, floors, decoder constants, metrics, acceptance-null populations and expected detectability **before** evaluation. Save config/recipe hashes and timestamps; no git commit is performed by this research agent.
- Outer split is leave-one-source-**speaker**-out, encompassing every speech, passage, clean rendition, placebo, DSP variant and ladder descended from that speaker. If texts/reference speakers form connected shared-source groups, hold out the connected group. Never randomly split words or variants.
- R2 voice folds also exclude the test TTS/reader voice from scales, calibration, and any fitted model. Hold out the participant speaker as well as reference speaker where feasible. Report held-out-voice and held-out-engine tests separately; ≥3 voices permits a minimal voice holdout, not population coverage.
- Mark Reagan Challenger/JFK inaugural probes as development. Exclude them from untouched headline results; any table including them is labeled exploratory. If only those texts are available, report development evidence only.
- Inner training groups fit null scales and threshold only; no test-derived constants, feature selection, severity maps or calibration. Every comparator shares folds, population and false-alarm target. Known generator chains used in calibration cannot also be called held-out generators.
- Main localization set: single interventions, spans of one word, 3–5 words, or one phrase; fixed length within a magnitude sweep; uniform seeded sampling among eligible locations, stratified by sentence position. For pauses eligible boundaries are defined by actual gaps, not reference punctuation alone.
- Draw continuous magnitudes within the chosen synthesis schedule bounds and retain physical realized magnitude; use fixed recipes/seeds. Do not use identical discrete magnitudes as both calibration and all test points. Multi-flaw ladders test aggregate behavior, not headline localization.
- Held-out-generator tests: rate PSOLA versus WSOLA, pitch PSOLA versus WORLD, plus native TTS controls where available. Include same-span neutral resynthesis/splice/crossfade for every chain; identity alone is insufficient.

**VERIFIED_BY_SOURCE:** grouped splits prevent subjects sharing train/test; [scikit-learn grouped CV](https://scikit-learn.org/stable/modules/cross_validation.html), prior fetched excerpt `sources/grouped_evaluation_prior_excerpt.txt`. Those APIs alone do not solve crossed reference/participant speaker dependence; explicit manifests do.

### 7.2 Detection expectations and stress controls

Predeclare **before outputs**: identity/placebo should stay silent at the null budget; gain/F0-register changes should not create prosodic flags absent tracking failure; R2 near-perfect changes below natural spread should usually remain silent. Per dimension and regime, label the schedule cells “below tolerance,” “uncertain,” or “expect detection” from the fitted physical threshold `h s_d` and measured recovery uncertainty, using training information only. R1 low-level measurement sensitivity and R2 tolerance are different outcomes; do not pool them.

Report detection versus realized magnitude **and span length**, at the locked false-alarm budget. If enough trials support a monotone detection-curve fit, estimate 50% and 90% detection magnitudes by interpolation; otherwise report observed brackets or “not reached.” These are operational thresholds, not human psychometric thresholds. Published tempo/pitch JNDs contextualize perceptibility, not flaw or acceptability.

Stress suite: gain ±12 dB without clipping; F0 level ±4 st; formant warp factors 0.90/1.10; 4 kHz band-limit; codec re-encode; additive noise 20/30 dB SNR; leading/trailing silence ±0.5 s; dynamic-range compression; resampling and deployment thread/environment changes. Treat channel manipulations as robustness challenges, not automatically harmless to every acoustic feature. Tabulate added/removed flags/min, feature change, index change, valid coverage and boundary errors. All are Kaggle operations in the later build.

Directional controls: monotonic fixed-span magnitude sweep; coverage sweep; adding a second flaw; cancellation/repair; independent realized-versus-nominal feature recovery; absence of collateral clarity flags for neutral vocoding. For inverse edits, noninvertible transformations require the preserved clean source, not a claimed exact mathematical inverse. Placebo repairs must not yield the same apparent improvement. Separate failed extraction/alignment from successful analysis with zero detection.

### 7.3 Compact headline set and exact metric definitions

Use **event F1@tIoU0.50 + onset/offset error + held-out null false regions/minute + detection versus physical magnitude** as the main region evidence. Add unit AUPRC for ranking and per-speech ladder monotonicity as separate outcomes. Publish by dimension, regime and null stratum; no pooled R1/R2 score.

| Metric | Exact definition and convention |
|---|---|
| Temporal IoU | For positive-length intervals R,E on P's actual time: `I=max(0,min(end_R,end_E)-max(start_R,start_E))`; `IoU=I/(len_R+len_E-I)`. No IoU for deleted-pause points. |
| Event F1@0.50 | Match same dimension **and sign**, within the same recording, where IoU≥0.50. Maximum-cardinality one-to-one bipartite matching; among ties maximize summed IoU, then stable IDs. `TP=matches`, `FP=n_pred-TP`, `FN=n_ref-TP`; `P=TP/(TP+FP)`, `R=TP/(TP+FN)`, `F1=2TP/(2TP+FP+FN)`. Duplicates count as FP. |
| Strict collar F1 | Same matching, `\|on_E-on_R\|≤0.200 s` **and** `\|off_E-off_R\|≤0.200 s`. Supplement to IoU, explicitly not default sed_eval offset tolerance. |
| sed_eval-convention F1 | Onset ≤0.200 s; offset ≤`max(0.200 s,0.50×len_R)`; optimal one-to-one matching, dimension/sign labels. Label as secondary lenient convention. |
| Boundary errors | On matched events: signed and absolute `1000(on_E-on_R)`, `1000(off_E-off_R)` ms; report absolute median and p90 separately for onset/offset, signed median bias and matching recall. Conditional on detected/matched events; missed events cannot disappear from reporting. |
| Deleted-pause boundary recall/F1 | Same text boundary ID and sign; predicted participant anchor within 0.200 s of the analytically mapped edit anchor. One-to-one event counts, separate from interval IoU statistics. Report gap-duration MAE too. |
| False regions/min | On accepted-null recordings, `total typed decoded events/(total participant seconds/60)`; include all signs/dimensions. Report raw counts, minutes, distinct speakers/voices, source-balanced rate and per-recording any-flag fraction. No ground-truth events means precision/recall are NA. |
| Flagged-time fraction | Duration of the **union** of predicted intervals divided by analyzed valid duration; no double-counting overlapping dimensions. Boundary-only deletions counted separately. |
| Unit P/R/F1 | For nonpause words, truth active if >50% of the word's aligned extent overlaps positive-length intervention ground truth. Use that same rule to convert predictions; evaluate each dimension/sign separately. For pause units use boundary IDs. Do not treat context-window support as exact edit support. |
| Unit AUPRC / AP | Sweep raw signed `δ/s` scores on valid units. Group tied scores; `AP=Σ_k (recall_k-recall_{k-1}) precision_k`, no trapezoidal interpolation. Give positive prevalence and eligible-unit count; NA if no positives. Unsigned dimension AP may use `\|δ\|/s` but name it. |
| 10 ms frame F1 / AUROC | Optional diagnostics: midpoint truth/prediction at 10 ms frames on P; skip abstained frames and disclose excluded support. AUROC is pairwise rank probability that a positive score exceeds a negative, with ties 0.5. F1 at locked threshold; no adjustment that fills whole truth regions after one hit. |
| Temporal AP/mAP | Optional only: rank regions by `max signed z` within each region, stable tie IDs; greedily match highest-IoU unused same-label truth at threshold. Use all-point interpolated precision `p*(r)=sup_{r'≥r}p(r')`, AP=integral_0^1 p*(r) dr. Mean over eligible labels and τ∈{0.50,0.55,…,0.95}; report absent-label exclusions. This differs from unit AP above. |
| Severity response | Fixed span/chain: detection rate `matched interventions/eligible interventions` versus independently realized magnitude, with numerator/denominator and source points. Spearman `ρ=Corr(rank(magnitude),rank(burden))` with average ties; NA for constant ranks. Compute within each source sweep, not treating ladder rungs as independent speeches. |
| Ladder monotonicity | For penalty burden expected nondecreasing: fraction of adjacent level transitions satisfying `B_{l+1}≥B_l-10^-6`; also k-of-n source speeches with every transition passing. If displayed quality-like index falls with burden, reverse the inequality. Report magnitude/count/coverage separately. |
| Activation matrix | Row=intervened dimension, column=detected dimension; proportion of interventions with a matched activation per column. Multi-label realized changes can activate several columns; this is not forced eight-way classification. |

For all event/word F1, zero predicted and zero reference gives NA, not perfect accuracy. Aggregate raw TP/FP/FN for micro F1 and also show per-source values; macro average excludes only explicitly NA cells and discloses their count. Always report scorable coverage, processing failures and the all-intervention denominator alongside valid-only results.

**VERIFIED_BY_SOURCE:** exact sed_eval onset/offset tests were fetched earlier from [source](https://raw.githubusercontent.com/TUT-ARG/sed_eval/master/sed_eval/sound_event.py), preserved in `PREVIOUS_RUN_condensed.md:194–233`. The default offset is **not** ±200 ms for long events. ActivityNet's ranked temporal detections and thresholds are prior art for the optional mAP diagnostic: [official evaluation code](https://raw.githubusercontent.com/activitynet/ActivityNet/master/Evaluation/eval_detection.py), earlier fetched in `RUN2_condensed.md:2046–2190`. [Kim et al.](https://ojs.aaai.org/index.php/AAAI/article/view/20680) caution against inflated time-series anomaly metrics; no point adjustment is allowed. [Bilen et al.](https://arxiv.org/abs/1910.08440) discuss operating-point/collar limitations. Our strict collar, unit mapping and summary conventions are **UNVERIFIED design choices**.

Mandatory comparator outputs: flag-all; no-flags; random regions with fixed seed 20261001 and the same event counts/durations as the primary predictions, placed uniformly in valid support (do not constrain them to labels); direct one-feature high threshold without hysteresis. Any calibration-required comparator uses the identical null budget. Dense ladders are excluded from localization headlines because flag-all can appear good there.

### 7.4 Small-data uncertainty

Primary reporting unit is the independent source speaker; multiple speeches from one speaker remain one cluster. Show every cluster's metrics, median/range, counts and null exposure. A source-block bootstrap with 2000 resamples and seed 20261001 may give exploratory 2.5/97.5 percentiles, resampling all descendants together and recomputing the metric. Do not advertise nominal 95% coverage with 8–10 clusters. A single-source or constant bootstrap is not an informative interval.

R2 observations cross reference-speaker and participant-voice groups. Prefer disjoint held-out speaker/voice cells and per-cell reporting. If bootstrapping is used, resample both IDs with multiplicity-product cell weights and disclose its instability with few voices; do not bootstrap words or hundreds of derived pairs as independent. For any later learned comparison, show paired per-source differences at equal FP/min; do not claim improvement from a tiny average alone. [Grouped-bootstrap implementation discussion](https://raw.githubusercontent.com/luferrer/ConfidenceIntervals/main/README.md), earlier fetched `sources/grouped_evaluation_prior_excerpt.txt`, supports preserving correlated groups, not reliable small-cluster coverage.

## 8. Optional simulation decision

**Skipped.** `sim_region_rules.py` was read, not executed. It assumes constant/ramp shifts in Gaussian or t5 AR(1) word sequences, population-scale normalization and synthetic independent timings. A decoder ranking there cannot establish R2 label correctness, human null scales, alignment error or synthetic-to-real transfer; none would change the final architecture choice under the stated constraints. Therefore the user's condition for a Kaggle run is not met.

The historical script also defaults to 16 process workers, which is unsuitable for the stipulated 4-vCPU kernel without modification. No push, install, simulation, model forward pass, DSP, feature extraction or benchmark was started by this session. Do not use the legacy script's comment as an approved local command.

## 9. Verified by running / versions / provenance

No detector, null estimate, boundary metric or model comparison is VERIFIED_BY_RUNNING. There is no `kaggle_out/results.json` or simulation output in this topic. The user's “no probe has run” is the operative evidence status. Historical `push_v1.log` mentions queued/running states, but supplies no completion/result; it is not proof of an experiment. This session made **0 Kaggle pushes** and did not retrieve or treat undocumented remote results as findings.

| Evidence | Status | What it proves and what it does not |
|---|---|---|
| `pypi_wheels.out`, `pypi_wheels_round2.out`; fresh `web/pypi_*_checked.json` | VERIFIED_BY_SOURCE (package registry) | Current release metadata, Python constraints and CPython 3.12 wheels; not package compatibility or numerical results. |
| `PREVIOUS_RUN_condensed.md:96–142` | VERIFIED_BY_RUNNING (earlier local install log) | Historical numeric package installs, including numpy 2.5.3/scipy 1.18.1; does not verify this full pipeline. |
| `PREVIOUS_RUN_condensed.md:282–374` | VERIFIED_BY_RUNNING (earlier local import log) | sed-eval 0.2.1 failed without pkg_resources, then imported with setuptools 80.10.2; logged dcase-util package/import versions disagree, so no safe combined pin is established. |
| `PREVIOUS_RUN_condensed.md:463–494` | VERIFIED_BY_RUNNING (earlier local import log) | Reported forced_align availability in an unusual torch 2.14.1 / torchaudio 2.11.0 combination; not an endorsed ABI-compatible lock. Official maintenance docs/API branches and artifact versions must be reconciled by alignment/packaging. |
| `web/source_checks_2026-10-01.json`, source excerpts, prior logs and bibliography JSONL | VERIFIED_BY_SOURCE | Literature and documentation statements with the limitations stated above. |

**Proposed pins for this module:** Python 3.12; `numpy==2.5.3` for deterministic arrays/weighted statistics and `scipy==1.18.1` for one-to-one matching if already in the feature environment. Both registry pins were freshly checked; full Kaggle integration is **UNVERIFIED**. No scipy is needed for a small custom matching implementation, but use the existing dependency if present. `scikit-learn==1.9.1` is registry-verified for an optional offline comparator only; not a runtime requirement. Avoid `sed_eval`, `ruptures`, `lightgbm`, `interpret`, `shap`, DTW packages and a new SSL checkpoint in the shipping grounding module. Implement the stated small metric definitions in project code and validate later with toy and reference examples on Kaggle.

Do not copy all earlier “latest” pins into a lock. Feature tracker, alignment checkpoint, decoding and dependency compatibility belong to the feature/alignment/packaging artifacts; this report pins the grounding interface and detector parameters, not an untested full audio stack. Pin exact model revision/checksum before build evaluation.

## 10. Risks and owner decisions

- Calibration minutes/speakers, not classifier weight count, are the bottleneck. Clean TTS cannot certify human false-alarm control; one public-domain text cannot certify oratory-wide tolerance.
- A single famous reference defines similarity, not the unique correct performance. Alternate prominence, pitch range and rhetorical pauses can be competent. Biological pitch/channel normalization removes some effects and leaves others; age, dialect, sex, noise and style remain potential confounds.
- Silence extraction, CTC word duration bias and F0 octave/voicing errors can dominate small perturbations. A five-word detector has five-word feature support; sample-exact edit labels do not confer sample-exact inferred regions.
- Floors, h grid, false-alarm target, feature support and spectral proxy are concrete proposals requiring end-to-end validation. No numerical performance is established by this research.
- Learned models could help with multi-cue human-validated targets, but would not fix incorrect R2 labels, missing null diversity, or false quality claims automatically.
- The six-page documentation should prioritize two regimes, the trigger formula, calibration population, a results/stress table and the limitation sentence. Do not describe an experimental comparator as a deployed model.

Only owner decisions still needed for the later build: whether to allocate public-domain human multi-reader null material; whether to allocate brief human listening/boundary QA; what user-facing false-alarm tolerance is acceptable (0.50/min is the proposed default); and whether the product promises experimental synthetic-population tolerance or validated human-upload tolerance. None prevents completing this report. No user confirmation is needed for these research recommendations.

## 11. Source trail

Sources are linked next to their claims. Primary fetched texts/excerpts are retained in `PREVIOUS_RUN_condensed.md`, `RUN2_condensed.md`, `sources/*_prior_excerpt.txt`, `sources/cawley_talbot_2010.html`, `sources/korzekwa_2021.html`, and `web/source_checks_2026-10-01.json`; bibliographic records are `web/oa_*.jsonl` and `web/s2_batch1.jsonl`. The owner's brief, fixed decisions and complete eight-question topic were read from `track-c-research-v2-wf_60487e8b-9e5.js`. Critic/design source texts remain at the supplied `../../design/` paths. Additional context consulted: `../rubric_explain/REPORT.md` and the dashboard report. No long paper/rubric quotation is reproduced in this report.
