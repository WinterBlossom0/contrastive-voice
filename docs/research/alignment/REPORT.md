# Alignment research: evidence and build recommendation

Date: 2026-10-01. Scope: research and probes, not product implementation.

## Recommendation

Use English `WAV2VEC2_ASR_BASE_960H` emissions plus the existing NumPy CTC Viterbi for the CPU build. Keep raw CTC spans, candidate acoustic boundaries, and measured silence intervals as separate fields. Do not deploy the current energy refinement as a trusted pause estimator: it erased four newly inserted 250 ms pauses. Use word and phrase units; phone timing is an optional validation upgrade, not a requirement for pitch, volume, pacing, and pausing comparisons.

**VERIFIED_BY_RUNNING:** base versus MMS, edit recovery, mismatch tests, confidence and repeatability are in [alignment_probe.json](kaggle_out/alignment_probe.json), produced by the lead's E1–E8 kernel. **VERIFIED_BY_RUNNING:** automatic selection using a fetched official transcript is in [automatic_passage_probe.json](kaggle_out/automatic_v5/automatic_passage_probe.json). Proposed production gates and refinement changes below are **UNVERIFIED**, explicitly chosen recommendations requiring validation.

MMS is useful as a multilingual alternative or cross-check, but its larger English inference cost did not buy independently established boundary accuracy here. MFA is the stronger published precision alternative for clean speech, with a more involved installation. Neither model agreement nor analytic propagation of this aligner's own labels establishes human word-boundary accuracy.

## Evidence, versions, and parameter contract

**VERIFIED_BY_RUNNING:** E1–E8 used Python 3.12.13, torch 2.10.0+cpu, torchaudio 2.10.0+cpu, NumPy 2.0.2, FFmpeg 4.4.2-0ubuntu0.22.04.1, four available vCPUs, AMD EPYC 7B12. Initial torch thread count was two; E1 subsequently sets four, so many later probes use four threads. E9 used the same Python/torch/torchaudio/NumPy/FFmpeg, SciPy 1.16.3 and **two torch threads**, on a four-vCPU Intel Xeon at 2.20 GHz. CPU timings between these two hosts are not a controlled comparison.

Recommended exact starting pins and settings:

| Component | Pin or setting | Status |
|---|---|---|
| Python | 3.12.13 | VERIFIED_BY_RUNNING on both kernels |
| torch / torchaudio | 2.10.0+cpu / 2.10.0+cpu; CPU wheel index | VERIFIED_BY_RUNNING; keep the pair together |
| NumPy / SciPy | 2.0.2 / 1.16.3 | NumPy both runs; SciPy recorded in E9 |
| Model | `torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H.get_model().eval()` | VERIFIED_BY_RUNNING |
| Torch inference | `torch.inference_mode()`, CPU float32, two threads, seed 0 | VERIFIED_BY_RUNNING in E9; inference needs no sampling |
| CTC | blank ID 0, separator `|`, uppercase letter/apostrophe targets; float64 DP, int8 backpointers | VERIFIED_BY_RUNNING in probe source |
| Canonical waveform | 16 kHz mono; preserve a channel explicitly for anti-phase transfers | VERIFIED_BY_RUNNING for Reagan left channel |
| Full-file emissions | 30 s ownership chunks, 1 s context each side; boundaries rounded to multiples of 320 samples | VERIFIED_BY_RUNNING E5/E9 |
| Time convention | frame start `0.020*f`; exclusive end `0.020*(f_last+1)` | VERIFIED_BY_RUNNING implementation convention; not a human edge guarantee |
| Syllables | `cmudict==1.1.3`; stress-marked vowels; explicit per-transcript pronunciation choices | Version verified in E7; pronunciation policy chosen |
| Refinement | retain raw; existing refinement only a candidate until pause QA passes | Chosen response to E2 failure |
| Passage anchors | `SequenceMatcher(autojunk=False)`; exact normalized-word matching; sentence coverage ≥0.80 and both endpoints matched | VERIFIED_BY_RUNNING E9 |
| Passage selection | 20–40 s, contiguous eligible sentences; maximize minimum sentence coverage, then proximity to 30 s, then earliest start | VERIFIED_BY_RUNNING E9 |

This is a verified starting environment, not a complete lockfile. E9 records SciPy explicitly; E1–E8 did not. Avoid claiming that unconstrained kernel-image packages or downloads are fully reproducible. Record checkpoint SHA-256, input PCM hashes, normalizer version, thread counts and the final dependency lock during the build.

## Aligner comparison

Package versions and Python declarations below are **VERIFIED_BY_SOURCE** from the saved [PyPI JSON files](web/pypi_torchaudio.json), fetched by the earlier researcher. A Python declaration or wheel tag does not establish successful installation of every compiled dependency. CPU measurements are **VERIFIED_BY_RUNNING** only where marked; other latency/RAM/disk gaps are **UNVERIFIED**, not guessed.

| Option | Boundary evidence | Weights / process RAM / CPU cost | Install, license, maintenance, Python |
|---|---|---|---|
| Base wav2vec2 + NumPy Viterbi | No human-labelled error measured for this exact probe configuration; published wav2vec2 WBE 48 ms TIMIT / 89 ms Buckeye under another protocol | 94,393,245 parameters; checkpoint 377,664,473 bytes; E1 peak 1,165 MiB. On 26 s: inference 3.66 s at 2 threads, 6.38 s at 1; Viterbi 0.043 s | CPU torch plus small torchaudio wheel and NumPy. TorchAudio BSD; this bundle's weights MIT. Maintenance mode; Python 3.12 run verified, 3.13/3.14 not run |
| TorchAudio `forced_align`, `MMS_FA` | C++ and NumPy paths agree exactly on both E1 models; MMS precision tables below | MMS: 315,466,396 parameters; checkpoint 1,262,047,414 bytes. Cumulative peak after loading both models 3,085 MiB. 26 s: 9.94 s at 4 threads / 16.56 s at 1; DP 0.039 s | MMS weights CC BY-NC 4.0; no separator token. Same torch stack. APIs remain present in examined 2.9–2.11 artifacts despite deprecation documentation |
| `ctc-forced-aligner` 1.0.2 | Depends on chosen model and postprocessing; no package-specific human error or Kaggle run here | Default repo model is MMS-300m; wrapper can use other CTC models. Actual package RAM/CPU/disk unmeasured; repo's “5× less memory” is an author claim, not our measurement | Saved PyPI release is source-only, ~0.02 MB, with ONNX Runtime and librosa dependencies; torch extras. Current GitHub README describes a torch/HF route. Repo BSD-2-Clause, default MMS model NC. No Requires-Python declaration; 3.12/13/14 installs unverified |
| WhisperX 3.8.6 | Wav2vec2 forced alignment after ASR; published results vary greatly by protocol | Known transcript can avoid ASR model inference, but no measured install/RAM/CPU here; full pipeline also loads Whisper and possibly diarization | BSD-2-Clause; saved metadata includes torch/torchaudio ~2.8, pyannote, transformers, CTranslate2, torchcodec. Python ≥3.10,<3.14, so 3.14 excluded; 3.12/13 runtime unverified here |
| Montreal Forced Aligner 3.4.2 | Strong clean-speech precision: MFA ARPA 3.0 onset means 19.93/21.75 ms, TIMIT/Buckeye | Acoustic models/dictionaries vary; checkpoint size, RAM and 30–60 s CPU latency not measured here | MIT toolkit; model licenses separate. Wrapper wheel ~0.44 MB does not include Kaldi/kalpy/Pynini stack. Official installation uses conda, including native dependencies. Metadata ≥3.8; 3.12/13/14 resolved stacks unverified |
| NeMo Forced Aligner / `nemo-toolkit` 3.0.0 | Token, word, segment alignment with CTC ASR; benchmark onset means 78.24/88.62 ms | Model-specific; actual disk/RAM/30–60 s CPU timing unmeasured. No evidence it requires a GPU for all inference, but no CPU deployment run here | Apache-2.0 toolkit, model license separate; broad ASR stack, CUDA bindings in saved Linux metadata. Python ≥3.10 declaration; native dependency support on 3.13/14 unverified |
| `faster-whisper` 1.2.1 | Decoder attention word timestamps accompany recognized words; no independent word-edge error found for this exact package/version | Official README: small/int8, 13 min transcription, 102 s and 1,477 MB on i7-12700K, 8 threads, beam 5; not a Kaggle 30 s force-alignment timing. Weights not measured | MIT; CTranslate2, PyAV, tokenizers, ONNX Runtime; lighter than a full torch ASR stack. Python ≥3.9; 3.12/13/14 resolved stack unverified |
| `whisper-timestamped` 1.15.9 | Cross-attention/DTW timestamps on decoded words; no independent boundary table for this exact package/version found | Adds Whisper; chosen-model disk/RAM/CPU cost unmeasured | GPLv3; Cython, dtw-python, openai-whisper. Python ≥3.7 declaration; compiled support and runtime on 3.12/13/14 unverified |
| `stable-ts` 2.19.1 | Alignment/refinement on Whisper routes; no exact-version human boundary table found | Chosen-model costs unmeasured | MIT; saved release source-only ~0.19 MB; openai-whisper constraints and optional faster-whisper/HF backends. Python ≥3.8 declaration only |
| `ctc-segmentation` 1.7.4 | Useful long-text localization backend; still needs emissions; no exact-version human word-edge benchmark found | No extra acoustic model; actual CPU/RAM unmeasured | Saved release source-only ~0.07 MB, Python ≥3.6. Compiled installation compatibility unverified; not necessary after successful E5/E9 |

Sources: [base bundle](https://docs.pytorch.org/audio/2.10.0/generated/torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H.html), [MMS bundle](https://docs.pytorch.org/audio/2.10.0/generated/torchaudio.pipelines.MMS_FA.html), [ctc-forced-aligner](https://github.com/MahmoudAshraf97/ctc-forced-aligner), [MFA installation](https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html), [NFA](https://github.com/NVIDIA-NeMo/Speech/blob/main/tools/nemo_forced_aligner/README.md), [faster-whisper benchmark](https://github.com/SYSTRAN/faster-whisper). Source text retained under `web/`, including README/license files fetched in this session.

### What happened to the TorchAudio APIs?

**VERIFIED_BY_SOURCE:** the [2.10 documentation](https://docs.pytorch.org/audio/2.10.0/generated/torchaudio.functional.forced_align.html) still says deprecated and scheduled for removal in 2.9. Treat that schedule as a compatibility warning, not evidence of actual removal.

| Version | Observed artifact | What is established |
|---|---|---|
| 2.9.0 | Downloaded 2,059,901-byte CPython 3.12 Linux wheel as a zip; inspected source without installing | `functional/_alignment.py` contains `forced_align`; pipeline source and exports contain MMS_FA and base. Source presence verified, C++ execution not run |
| 2.10.0+cpu | Kaggle E1–E8 and E9 | Both bundles load; `functional.forced_align` works and matches NumPy on E1 |
| 2.11.0+cpu | Previous local research, preserved API check and output JSON | Bundles and `forced_align` present and worked with that research environment's torch 2.14.1+cpu; not a recommended mismatched pair |

The 2.9 wheel audit and extracted source are saved in [ta29_wheel_audit.json](web/ta29_wheel_audit.json). The earlier 2.11 execution is recorded in [PREVIOUS_RUN_condensed.md](PREVIOUS_RUN_condensed.md) and [out_base_t1.json](out_base_t1.json). Do not rerun that local compute. Use NumPy Viterbi to reduce dependence on the deprecated C++ alignment entry point; emissions still depend on a pinned bundle API.

### Newer alternatives

**VERIFIED_BY_SOURCE:** these are research candidates, not tested substitutes for the CPU build.

| Candidate | Measured source result | Cost / availability implications |
|---|---|---|
| Label-prior CTC, Huang et al. 2024 v3 | WBE improves from standard CTC 58→43 ms Buckeye, 42→29 ms TIMIT; fine-tuned 34/28 ms | Changes training objective, not just our inference-time blank treatment; no reproduction here; do not claim MMS_FA already incorporates this objective |
| Bournemouth Forced Aligner | 2026 benchmark word-onset means 52.01/61.54 ms TIMIT/Buckeye | Not a clear precision upgrade from published MMS results; package/model cost, licence and Python deployment not established here |
| Qwen3-ForcedAligner-0.6B | Official repo human-labelled AAS: raw 27.8 ms, raw-noisy 41.8 ms, concat-300 s 24.8 ms | 0.6B advertised scale; package and model CPU RAM/disk/latency unmeasured. Supports supplied text, 11 languages, ≤5 min. Apache-2.0 repo; GPU-oriented examples; Python/native runtime unverified |
| Nyra (2026) | Authors report mean onset/offset MAE 20.6 ms on Buckeye; FuseAlign evaluation reports 13.67 ms asymmetric mean on TIMIT | WavLM-Large front end plus Kaldi GMM-HMM; not a small standalone NumPy aligner. No Kaggle CPU timing, exact released package pin or licence verified here |
| FuseAlign, Sept. 2026 v1 | AlignBench mean asymmetric error 17.16 ms, 0.38% words >300 ms | 213M trainable + 252M frozen Dia encoder ≈465M inference parameters; authors describe future benchmark release. No runnable checkpoint/release licence/CPU latency verified here; don't train this for the hackathon |

Sources: [Huang](https://arxiv.org/html/2406.02560v3), [MFA 2026 comparison](https://arxiv.org/html/2606.18466v1), [Qwen official repo](https://github.com/QwenLM/Qwen3-ASR), [Nyra authors](https://nyra-labs.com/research/nyra-forced-aligner), [FuseAlign](https://arxiv.org/html/2609.33650v1). Qwen AAS and other papers' errors have different evaluation sets and definitions; their numbers cannot be directly ranked.

## Published boundary errors: keep protocols distinct

**VERIFIED_BY_SOURCE:** [MFA 2026 Table 4](https://arxiv.org/html/2606.18466v1), retained in [arxiv_2606.18466v1.txt](web/arxiv_2606.18466v1.txt). These are **word-start** boundary errors, not both-edge errors or this probe's accuracy.

| System | TIMIT mean ms | TIMIT ≤50 ms % | Buckeye mean ms | Buckeye ≤50 ms % |
|---|---:|---:|---:|---:|
| MFA ARPA 3.0 | 19.93 | 91.61 | 21.75 | 91.35 |
| MFA Global 3.0 | 22.33 | 89.53 | 25.35 | 89.30 |
| Charsiu | 27.18 | 85.97 | 29.24 | 87.40 |
| MAPS | 18.86 | 91.97 | 54.44 | 71.96 |
| BFA | 52.01 | 57.00 | 61.54 | 48.03 |
| MMS | 43.06 | 63.73 | 49.54 | 61.85 |
| WhisperX | 110.04 | 15.55 | 110.90 | 13.48 |
| NeMo | 78.24 | 38.23 | 88.62 | 35.81 |

**VERIFIED_BY_SOURCE:** [Rousso 2024 Table 1](https://arxiv.org/html/2406.19363v1) evaluates **word-end** boundaries. On TIMIT, ≤50 ms coverage is MFA 89.4%, MMS 75.7%, WhisperX 82.4%. This is why WhisperX's apparently conflicting 2026 numbers must not be silently combined into one ranking. Saved paper text itself contains inconsistent qualitative prose; use its definitions and tables.

**VERIFIED_BY_SOURCE:** [Huang Table 1](https://arxiv.org/html/2406.02560v3), saved in [arxiv_2406.02560v3.txt](web/arxiv_2406.02560v3.txt), reports word-boundary error averaging both edges within utterances, then utterances; Wav2Vec2 has WBE 89/48 ms Buckeye/TIMIT, MMS 53/37 ms, MFA 41/23 ms. Mean word durations in Buckeye are 177 ms Wav2Vec2, 181 ms MMS, versus 241 ms annotated truth: spikes shorten duration. Published models and segmentation differ from our base excerpt.

**VERIFIED_BY_SOURCE:** [FuseAlign Table 3](https://arxiv.org/html/2609.33650v1), saved in [arxiv_2609.33650v1.txt](web/arxiv_2609.33650v1.txt), reports **asymmetric** boundary error: edges anywhere in the adjacent pause can incur zero error. Tail percentages use the worse edge of each word; the mean uses both boundaries. For corrected AlignBench transcripts:

| System | Mean asymmetric ms | Words >50 ms % | Words >300 ms % |
|---|---:|---:|---:|
| FuseAlign | 17.16 | 7.27 | 0.38 |
| Gentle | 31.43 | 12.61 | 2.11 |
| Nyra | 33.18 | 29.99 | 1.28 |
| MMS-FA | 48.91 | 46.69 | 2.49 |
| WhisperX aligner only | 49.04 | 53.25 | 1.41 |
| MFA | 73.00 | 34.16 | 4.15 |

This benchmark is 73 diverse clips, 8,072 words, median 53.2 s; its MFA baseline is 3.1, not the exact 2026 ARPA experiment above. It scores unplaced words through a fixed fallback. That fallback is an evaluation convention, **not permission to fabricate production labels**. The report does not equate asymmetric editing tolerance with precision for pause length or articulation rate.

## Verified by running: E1–E8 in depth

All numerical claims in this section are **VERIFIED_BY_RUNNING**, from [alignment_probe.json](kaggle_out/alignment_probe.json); interpretation is labelled inference where necessary. Original executed source is preserved as [probe_e1_e8.py](probe_e1_e8.py). Each experiment catches errors independently; all eight have successful result objects.

### E1: cost, agreement, and duration bias

There are 74 words in a 26 s Reagan opening, 1,299 output frames. Base has ~3.34× fewer parameters than MMS. At one thread base inference is 6.38 s versus 16.56 s, ~2.60× faster; compare these equal-thread measurements rather than base-two versus MMS-four. Model loading 1.7/5.1 s is not a documented cold-download benchmark. Checkpoint sizes are printed in the kernel log; memory readings are process high-water marks, not isolated model sizes.

Base/MMS raw start agreement: mean 14.9 ms, p90 40, max 40. Raw ends: mean 17.0, p90 40, max 60. After refinement, start/end mean disagreement becomes 12.2/12.6 ms, but both maxima worsen to **105 ms**. Refinement improves the mean agreement and worsens the tail; no human annotation was used.

Base mean word duration changes 163.5→239.9 ms; MMS 180.8→241.2 ms. Raw gaps ≥250 ms occur 11 times, versus eight after refinement. From the saved base spans, summed word durations are 12.100 s raw and 17.755 s refined. Dividing E7's 101 syllables by these sums yields 8.347 versus 5.689 syllables/s. These derived quantities illustrate denominator sensitivity, not independently verified articulation rates. Raw spikes are insufficient to estimate absolute speech occupancy.

### E2: pause refinement fails the important near-perfect case

Seven insertions are tested simultaneously per duration: three existing pauses and four previously continuous boundaries. Inserts are seeded Gaussian noise at floor RMS 0.0033478, with 5 ms edge fades. This is artificial noise, not sampled archival room tone.

| Inserted duration | Raw pause-increase MAE / max ms | Refined MAE / max ms | Raw within 50 ms | Refined within 50 ms |
|---|---:|---:|---:|---:|
| 250 ms | 12.9 / 30 | 144.3 / 250 | 7/7 | 3/7 |
| 500 ms | 14.3 / 40 | 40.0 / 120 | 7/7 | 5/7 |
| 1,000 ms | 11.4 / 40 | 42.9 / 120 | 7/7 | 4/7 |

At 250 ms, refined pause increases are zero after `I'd`, `led`, `the` (index 48), and `a` (index 71). Existing pauses increase correctly by 250/260/250 ms. Raw gaps recover all seven within 30 ms. At 500 and 1,000 ms, some refined pauses overestimate insertion by 100–120 ms.

**Inference from code and results:** original raw gaps at those four boundaries are 80/60/60/100 ms. After adding 250 ms, they fit the refinement's ≤400 ms branch. When no silence run is accepted, that branch assigns **both edges to one energy minimum**, forcing pause duration to zero. The use of the maximum of full-band and preemphasized speech margins may reject spectrally different synthetic floor noise; the output does not include the envelope values needed to establish that cause directly. The branch and its harmful output are established.

Word starts away from edit shifts are mostly stable, but `other_word_*` arrays include all words, including edited neighbors: the names do not designate an independent untouched subset. Avoid quoting their aggregate errors as “all untouched words were accurate.”

### E3: stretch recovery is good for spans, weaker for individual words

FFmpeg `atempo`, two 5 ms overlaps, nine-word spans. Ratios mean output duration / source duration; a ratio below one means faster speech.

| Variant | Requested / realized ratio | Measured span ratio | Median word-duration ratio | Inside raw / refined MAE ms | Refined max ms | Inside confidence, original→variant |
|---|---:|---:|---:|---:|---:|---:|
| events…change fast | 0.7000 / 0.6997 | 0.7103 | 0.7333 | 9.2 / 6.2 | 20.0 | 0.978→0.795 |
| the…Challenger slow | 1.4000 / 1.3770 | 1.3741 | 1.3398 | 19.5 / 16.5 | 67.0 | 0.809→0.698 |
| the…Challenger fast | 0.5500 / 0.5456 | 0.5635 | 0.5825 | 16.8 / 17.7 | 46.5 | 0.809→0.199 |

Span-ratio deviations from realized ratios are +0.0106, −0.0029 and +0.0179. Use realized sample lengths, not nominal speed settings. Individual word ratios are less faithful; phrase aggregation is preferable. Refinement helps inside-span mean recovery in two variants and hurts in the strongest speedup. Refined post-span maxima are 53.1/108.9/102.4 ms despite a shared known global shift.

The expected time map is piecewise linear, built from the original aligner's times. `atempo` changes local waveform timing through overlap-add; sample-exact output length does not prove every internal syllable follows a uniform warp. Crossfades also mix neighboring samples. Thus these are transform-consistency errors, not human-edge errors or an exact phonetic reproduction. No vocoder/TTS alignment was tested in E3.

### E4: transcript errors and star are not solved

Removing the *transcript* words `on`, `a`, `know` models extra spoken material; it does not synthesize an actual filler/repetition. Ordinary separator alignment has all-boundary mean displacement 3.0 ms, but neighboring-boundary MAE 35.4 ms and max 150. Both star layouts worsen these means to 8.1/8.2 ms globally and 40.4 ms locally. A shifted neighbor can still have confidence 0.995–1.000.

The custom star column has **log score zero at every frame**, i.e. an unnormalized wildcard score of one. It is appended after log-softmax and deliberately allows arbitrary acoustic content. This is a routing device, not a posterior probability or deletion mechanism. Adding it between every word perturbs correct transcripts: refined maxima 105–110 ms, with raw changes up to 80 ms for separator-star-separator. Use edge stars for locating a passage; do not enable interword stars by default.

When `absolutely`, `however`, `people` are added to the transcript but not spoken, alignment still assigns 240/195/120 ms durations. Their confidence rounds to zero and LPR is −14.23/−13.38/−13.93. Real-word boundaries move up to 205 ms; real-word low confidence also occurs. Confidence is useful evidence of mismatch, but a low score is not a calibrated absent-word probability. High neighboring scores do not protect their boundaries.

### E5: locating typed passage text inside the full speech

The left-channel full MP3 decodes to 255.79 s. Thirty-second chunks with one-second context produce 12,789 frames. Full emissions take 40.6 s as decoded or 38.4 s peak-normalized; edge-star passage DP takes 0.42 s. The opening is located at raw 1.64–25.34 s, consistent with the independently known 0.5 s offset of `reagan_open_16k.wav`. After removing that known offset, raw start disagreement is mean 1.4 ms/max 20 as decoded; refined mean 1.1/max 20. E5 does not report equivalent end-error arrays.

A typed middle sentence is found at 138.94–143.27 s, confidence mean 0.997/min 0.980. This is a plausible high-confidence localization, not independent timestamp truth.

Ten-second chunking of the opening gives identical frame count but maximum log-prob difference 13.272 and argmax agreement 92.841%. Refined edge disagreement is small on average but reaches 105 ms. Overlap/context avoids gaps and bounds model memory; it does not make contextual transformer outputs equivalent to whole-file inference. Cache full emissions once rather than recomputing them for each passage; E5 recomputed for diagnostics.

### E6: confidence is channel- and speed-sensitive

| Degradation | Mean confidence | Mean LPR | Refined start / end MAE ms | Maximum start / end shift ms |
|---|---:|---:|---:|---:|
| Original | 0.8909 | −0.143 | 0 / 0 | 0 / 0 |
| LP 3,000 Hz | 0.8685 | −0.232 | 7.3 / 8.9 | 120 / 120 |
| LP 2,000 Hz | 0.8415 | −0.275 | 10.6 / 15.0 | 105 / 155 |
| LP 1,500 Hz | 0.6541 | −0.626 | 11.2 / 17.4 | 120 / 175 |
| LP 1,000 Hz | 0.2583 | −1.551 | 13.6 / 19.9 | 115 / 195 |
| LP 700 Hz | 0.1589 | −2.021 | 18.9 / 25.5 | 220 / 220 |
| White noise 20 dB SNR | 0.8070 | −0.443 | 10.4 / 23.8 | 105 / 175 |
| White noise 10 dB SNR | 0.2548 | −1.595 | 25.9 / 61.1 | 175 / 915 |
| White noise 5 dB SNR | 0.0619 | −2.887 | 51.8 / 80.1 | 470 / 410 |
| White noise 0 dB SNR | 0.0145 | −4.850 | 241.4 / 231.1 | 1,545 / 1,340 |

Noise uses the whole-clip RMS, including pauses, rather than a speech-only SNR reference. Low-pass is sixth-order Butterworth with forward/backward filtering. The seeded noise draws differ across SNR conditions, so the table is a single exploratory series, not repeated-seed estimation.

Confidence falls monotonically across these filter/noise schedules, but also falls 0.809→0.199 under strong tempo change in E3. Correct original `of` can score 0.043. These observations reject an unqualified “GOP = articulation clarity” interpretation. Treat it as acoustic/transcript compatibility; assess bandwidth and noise separately, and don't explain a channel defect as a speaker's articulation problem.

### E7: count syllables from pronunciation, not hyphenation

Of 65 unique test words, CMUdict has no OOVs; pyphen disagrees on 14 (21.5%), the vowel-group heuristic on eight (12.3%). These are disagreements with a dictionary pronunciation, not gold pronunciation errors. CMUdict's first variant gives two syllables for `our`, `fire`, `hour`, and three for `every`; actual speech may reduce them. The opening totals 101 syllables under this policy.

`cmudict==1.1.3` is preferable to `pyphen==0.18.1` for English syllables. Count phones ending in 0/1/2 stress digits; keep alternate counts and mark ambiguous/OOV words. Pick one reviewed count per transcript and reuse it across paired recordings. The stdlib heuristic is the lightest dependency-free fallback; export fallback flags instead of pretending exact syllables. pyphen estimates typography, not spoken nuclei.

### E8: repeatability and gain sensitivity

At fixed four threads, repeated emission hashes match. One/two/four threads give different emission hashes but the same path and refined-word hashes (`dd3825a119d2b2d9`, `e6329fd64c94087b` prefixes). This is one waveform, one host, one model: it proves repeatability here, not bit identity everywhere.

For −30/−20/−10/+6/+12 dB gain, raw-start max shifts are 20/20/20/0/0 ms; refined-start maxima are 135/105/105/60/60 ms. Mean confidence at −30 dB drops to 0.858 from 0.8909. Every gain changes the detailed CTC path. Refinement is more gain-sensitive than raw starts despite its relative threshold. Gains are float multiplications; no clipping/re-encoding deployment test was performed.

Some `within_20ms` fractions are below one even when displayed max is 20 ms: comparisons use binary floating-point without tolerance, while displayed values are rounded. Read these fractions cautiously at exact grid thresholds. Hash identity tests are unaffected.

## E9: automatic passage selection without typed passages

**VERIFIED_BY_RUNNING:** final private CPU kernel version 5; [result JSON](kaggle_out/automatic_v5/automatic_passage_probe.json), [script](kaggle/probe.py), [fetched page](kaggle_out/automatic_v5/official_transcript.html), [speech text](kaggle_out/automatic_v5/official_transcript.txt), [decoded words](kaggle_out/automatic_v5/greedy_words.json), [selected text](kaggle_out/automatic_v5/selected_passage.txt), [word alignment](kaggle_out/automatic_v5/selected_alignment.json), [audio](kaggle_out/automatic_v5/selected_passage.wav).

The URL is copied from the first line of `../baseline_data/transcripts/reagan_challenger_1986.txt`; the kernel itself fetches the [Reagan Library page](https://www.reaganlibrary.gov/archives/speech/address-nation-explosion-space-shuttle-challenger), HTTP 200. It extracts paragraphs from the speech opening through the last speech paragraph, excludes the editorial Note and navigation, expands integers below 1,000 to English words, and splits sentences while preserving closing quotes. This extraction is specific to this page structure, not a general website scraper.

Greedy decode collapses identical consecutive frame IDs, removes blank, keeps separators as word breaks and preserves letter-run frame starts/exclusive ends. `difflib.SequenceMatcher` uses `autojunk=False`; leaving its default on is risky for common words in long transcripts. Exact matching blocks create monotonic official-word→decoded-time anchors. There is no interpolation across unmatched endpoints. Both sentence endpoints must match, coverage must be ≥80%, and every sentence in a candidate must pass. Candidate duration must be 20–40 s. Deterministic ranking prioritizes worst-sentence coverage, then distance from 30 s, then earliest start.

The selected interval is aligned again from waveform with 0.5 s context on both sides and a crop start snapped to the frame grid. Final edges come from first/last aligned words of the selected sentences; duration is checked again. Selection does not read `reagan_open.txt`, excerpt JSON, or their times. Those inputs are loaded **after** selection for secondary validation.

| Measurement | Observed result |
|---|---:|
| Full audio duration / frames | 255.791 s / 12,789 |
| Official normalized words / decoded words | 651 / 659 |
| Exact matched word anchors | 596/651 = 91.55% |
| Both sentence endpoints matched | 37/46 = 80.43% |
| Eligible sentences, including ≥80% word coverage | 35/46 = 76.09% |
| Eligible 20–40 s candidates | 17 |
| Selected sentences | indices 12–16, five sentences, 65 words |
| Minimum selected-sentence word coverage | 100% |
| Greedy window | 74.14–96.02 s, 21.88 s |
| Force-aligned final window | 74.14–96.20 s, 22.06 s |
| Endpoint movement from greedy | start 0 ms; end +180 ms |
| Selected passage mean confidence | 0.99024 |

The window begins with “But we feel the loss” and ends with the sentence ending “all of us”; the full content is in the selected-text artifact. It is not the existing opening excerpt, and has **zero temporal overlap** with it. This deliberate consequence of automatic coverage-first selection avoids claiming a direct selected-window comparison where none exists.

Final version 5 took **42.23 s** for full emissions, **3.35 s** for selected-clip inference, **0.051 s** selected DP, and **59.31 s** total including fetch, loading and comparisons; peak RSS **1,482.2 MiB**. Versions 4 and 5 selected identical normalized words and times; version 5 preserves closing quotation marks and adds the raw-to-raw legacy comparison. Version 3 had a comparison-field bug after selection; its artifacts remain under `kaggle_out/automatic/`, and version 4's valid metrics under `kaggle_out/automatic_v4/`. Three further pushes were used, CPU only; no model or DSP ran locally.

Boundary agreement must distinguish three references:

1. **Known-offset opening reference:** fetched official opening words force-aligned in full-file coordinates versus `reagan_open_16k.wav`, fixed offset 0.5 s. Final version matched all 74 words: raw start/end MAE 1.4/0.8 ms, maxima 20/20; refined MAE 1.6/1.6 ms, maxima 105/105. This measures context/decoding consistency with the existing E1 alignment, not human accuracy.
2. **Greedy opening anchors:** 58/74 words matched; compared with refined opening edges, start/end MAE 34.8/40.5 ms, p90 76.5/96.5, maxima 120/190. Greedy anchors are suitable for coarse routing, not final phonetic boundaries.
3. **Legacy `reagan_excerpt_words.json`:** 74 raw CTC word spans in a different 25 s crop. A fitted median start offset is required because its crop origin is not recorded in that JSON. **Raw-to-raw agreement:** fitted offset 1.190 s; start/end MAE **5.6/5.8 ms**, medians 5/5, p90 9/9, maxima **26/29 ms**; all 74 starts and ends within 50 ms. Refined-to-raw agreement is MAE 25.7/66.8 ms with its separately fitted 1.1635 s offset; this includes a boundary-definition difference and is not the preferred comparison. Final version stores relocated rows in `existing_excerpt_relocated_alignment.json`. A fitted offset cannot independently validate absolute passage origin.

Global anchor coverage is not WER, calibrated confidence, or recall against human annotation. The opening and astronaut-name sentence fail eligibility; common-word matches can be ambiguous even with difflib. Coverage-first ranking favors easy text and recording conditions. Freeze a diversity-aware sampling policy for the actual dataset, save rejected candidates, and avoid optimizing passage selection against evaluation scores.

## Formulas, granularity, refinement, and robustness

### CTC and confidence

**VERIFIED_BY_SOURCE / VERIFIED_BY_RUNNING:** CTC is monotonic transcript-constrained path search; the implementation is in the probe and the API contract in [TorchAudio docs](https://docs.pytorch.org/audio/2.10.0/generated/torchaudio.functional.forced_align.html). For targets `y`, insert blank between labels: `z=[blank,y1,blank,...,yL,blank]`. With emission log scores ℓ:

`A(t,s) = ℓ(t,z_s) + max(A(t−1,s), A(t−1,s−1), A(t−1,s−2))`.

The last transition is legal only into a nonblank label different from the previous target. Initialize only first blank/label; terminate at final label or blank; backtrack. Require `T ≥ L + consecutive_repeated_label_count`; reject empty/unrepresentable transcripts and invalid target IDs explicitly in product code. Our research core does not implement every such production check.

Cost is O(TL); current materialized emission matrix uses approximately `8*T*(2L+1)` bytes plus `T*(2L+1)` int8 backpointers and temporaries. Chunk acoustic inference and align selected clips rather than long full transcripts whenever possible. For very long DP, gather emissions per frame instead of constructing that whole matrix.

For word w with character positions j and assigned nonblank frame sets F_j, the implemented peak compatibility is:

`C_w = exp[(1/|w|) Σ_j max_(t∈F_j) ℓ(t,y_j)]`.

`LPR_w = (1/|w|) Σ_j max_(t∈F_j) [ℓ(t,y_j) − max_c ℓ(t,c)]`;
`min_char_w = exp[min_j max_(t∈F_j) ℓ(t,y_j)]`.

The competing classes in LPR include blank, exclude the synthetic star column, and the maximum is taken **after** subtracting each frame's competing maximum. This is character-level posterior compatibility, not traditional phone GOP or a calibrated pronunciation score. The forced path already assumes the supplied text, creating selection bias. Use confidence for QA/abstention, with calibration on held-out speeches and channel controls; exclude unreliable words and neighboring gaps from delivery features.

### Concrete refinement, and the proposed correction

**VERIFIED_BY_RUNNING:** existing candidate algorithm:

1. Compute 20 ms centered RMS windows at 5 ms hop on both waveform and `x[n]−0.97*x[n−1]`.
2. For each envelope, noise/speech estimates are 5th/95th dB percentiles; threshold `q5 + clip(0.30*(q95−q5),6,15)` dB.
3. Speech margin is the maximum of the two envelope-minus-threshold values; candidate silence requires margin <0 for at least 50 ms.
4. For each raw CTC gap, search silence onset ≤400 ms after its left edge and silence offset ≤200 ms before its right edge. Snap edges independently, retaining a nonnegative silence interval.
5. If neither is present and the gap is ≤400 ms, assign a shared energy minimum; otherwise retain CTC edges. Extend clip-leading/trailing edges only within the same search limits.

**UNVERIFIED chosen correction:** disable the unconditional shared-minimum branch when a pause cannot be acoustically ruled out. Store raw gap, accepted silence duration and an `uncertain_gap` flag. In confirmed connected speech, an energy minimum may be a useful approximate shared word edge; in uncertain/noisy gaps it must not assert “zero pause.” Use a calibrated VAD or a validated band-limited silence detector as an independent occupancy estimate; do not replace uncertainty with a hard default. Recheck 50–400 ms inserts using sampled room tone, noise and gain controls before promoting refined pause values.

Blank runs constrain where to search; they are not silence detectors. CTC emits blanks within voiced speech as well. Do not redistribute every blank equally or claim 5 ms output sampling establishes 5 ms accuracy. E3 establishes limited transform-consistency benefit from refinement, while E2 establishes a severe counterexample; independent before/after human error remains unmeasured.

### Rate and granularity

**UNVERIFIED chosen measurement definitions:** retain word indexes for text anchoring and phrase windows for delivery metrics. For a window of words a…b with stable transcript syllable counts σ_i:

`speech_rate = Σ_(i=a..b) σ_i / (end_b − start_a)` includes pauses;
`articulation_rate = Σ σ_i / estimated_speech_occupancy` excludes **verified** pauses;
`pause_i = start_(i+1) − end_i` is a boundary-derived estimate, not necessarily acoustic silence.

Do not call `Σσ_i/Σraw_word_duration_i` articulation rate. Use at least phrase-sized windows; ±2-word rate windows smear a one-word edit into up to five units. Preserve actual temporal support in the feature record. CMUdict phonemes specify pronunciations, not audio-aligned phone boundaries. Phone alignment is needed only for claims about phoneme-specific articulation/lengthening; this project has no validated phone-level clarity measure.

An independent syllable-nuclei detector can cross-check broad rate, but noise, voicing and pitch flattening/vocoding may change its detections. No such acoustic detector was run here; a second rate estimator would still need validation.

### Robustness actions

| Condition | Evidence and required behavior |
|---|---|
| Long pauses | E2 includes existing pauses plus up to 1 s extra; arbitrary very long pauses untested. CTC can stay blank, but acoustic pause estimates must pass separate QA |
| Fillers / repeats | E4 removes three short transcript words; actual repeated-word and long-filler audio untested. Compare greedy decode with transcript and align stable matched blocks; flag unmatched material |
| Skipped words | E4 proves nonexistent words receive fabricated durations. Mark absent/uncertain and abstain on affected words and neighboring gaps; never divide the interval uniformly for product labels |
| Numbers and punctuation | Existing tokenizer strips digits, silently losing numbers. Production normalizer must expand spoken forms and keep display-token→expanded-word mapping. Preserve contractions, split hyphens, normalize Unicode; reject unsupported forms explicitly |
| Archival audio | Reagan anti-phase stereo requires channel selection; E6 demonstrates noise/bandwidth confounds. JFK/outdoor PA not aligned in these probes; do not generalize studio results |
| Long files | E5/E9 verify 255.791 s with chunked emissions. Use selected-clip limits and chunking for model calls; a provisional participant cap of 60 s is a chosen product policy, not a measured performance guarantee |
| Time stretch / vocoder | E3 supports three atempo ratios on two nine-word spans only; vocoders, pitch edits and TTS remain untested. Exact edit provenance and unreliable-alignment flags must survive reanalysis |

All behavior proposals in this table are **UNVERIFIED** choices; evidence references are **VERIFIED_BY_RUNNING**. A page-to-speech numeric expansion of “390” can differ by optional “and”; don't silently force a dictionary normalization as verified speech. Log transcript diffs per passage.

## Error budget, design disagreements, and critics

**VERIFIED_BY_RUNNING:** CTC grid is 20 ms; refinement is sampled at 5 ms. E1 model disagreement reaches 105 ms after refinement; E2 misses entire 250 ms pauses; E3 post-span maxima reach 109 ms; E6 at 10 dB SNR has an end displacement of 915 ms. These are different failure scenarios, not an additive universal error budget or an estimated human median. No human-labelled boundary MAE/p90 is available for our materials.

For duration `d=e−s`, edge perturbations obey `|Δd|≤|Δs|+|Δe|`. For inverse-duration rate, small relative error is approximately `|Δr|/r≈|Δd|/d`; short words amplify timing noise. Two independently aligned recordings add further uncertainty to rate ratios. Evaluate sample-exact edit boundaries separately from estimated word boundaries; the causal edit interval can be exact while its phonetic interpretation is uncertain.

| Item | Answer supported by this research | Remaining work |
|---|---|---|
| I-04, near-perfect effects | Single-word durations are sensitive to spikes/refinement; even 250 ms new pauses can vanish. Phrase-rate features and explicit noise floors are required | Human acoustic validation and severity floor selection |
| I-11, alignment error propagation | Published errors and recovery tails refute exact word-edge claims; analytic-label QA is consistency testing. Preserve raw/refined/uncertain separately | Owner can hand-correct ~150 boundaries across two archival passages; report human MAE/p90 and duration bias before/after refinement |
| I-08, synthesis artifacts | At tempo and crossfade geometry affect realized length; synthetic white floor noise fools refinement | Same-recording room tone and identity/placebo transforms |
| I-21, repeatability | Same-thread emissions repeat; cross-thread outputs agree on tested words. No two-environment hash reproduction established | Canonical PCM/checkpoint hashes and Kaggle-versus-deployment tolerance checks |
| I-22, transcript fidelity | Fake words get time labels; high-confidence neighbors can shift; star is not a mismatch cure. E9 saves decoded/page text for review | Reviewed verbatim transcripts; calibrated abstention gates |
| J-06, stress tests | E2/E3/E6/E8 give a named recovery matrix for pause/stretch/gain/noise/bandwidth | MP3 re-encoding, real speaker, crowd/reverb and model score stability not tested |
| J-07, clarity | Confidence tracks channel degradation and speed, not isolated articulation | Channel gates, separate acoustic evidence, do not call the posterior human clarity |
| J-09, upload failures | Sentence routing, numeric/display mapping and mismatch abstention address long-file/transcript risks | Implement upload limits and useful unmatched-word messages |
| J-11, listening | No listening/hand-labelling done by this agent; numeric confidence cannot certify audible cuts | Owner listening and karaoke synchronization check |
| J-12/J-13 | Official-page fetch, decoded transcript and private kernel outputs demonstrate the acquisition and alignment path | Public reproducible artifacts belong to the build/publication task |

Disagreements with DESIGN_v0 §§2.1, 2.2, 3, 4, 9: full-speech passage selection must first acquire/normalize the official transcript and route sentences, rather than presuppose a typed passage/window; ordinary mono downmix can cancel this source; the current refinement must not supply trusted pauses; raw CTC durations must not be used for absolute articulation rate; posterior compatibility must not be presented as articulation clarity; injected-sample truth and alignment self-consistency must be reported separately; transcript mismatch requires partial abstention and matched-block comparison.

## Risks and unresolved owner decisions

- **UNVERIFIED:** all human boundary accuracy on these materials; most alternative CPU timings and resolved Python 3.13/3.14 installations; phone accuracy, vocoder/TTS/crowd robustness; calibrated word absence and clarity thresholds. The report deliberately leaves these cells unmeasured.
- **VERIFIED_BY_RUNNING:** automatic anchor coverage is incomplete, and selection prefers high-coverage text. One full studio speech does not establish cross-speaker, multilingual or generic-page robustness.
- **UNVERIFIED chosen policy:** flag word compatibility <0.10, unmatched words, and their neighboring gaps for review; abstain on a whole clip with mean compatibility <0.10. These exploratory floors are motivated by E4/E6 but not calibrated; false positives occur on correct short words. They cannot be advertised as measured sensitivity/specificity.
- Owner decisions: whether to spend a short labelling/listening pass on two archival passages; whether sub-100 ms or phoneme-level claims justify MFA/another aligner; whether the upload UX should reject mismatch or return partial results; diversity/coverage tradeoff for the final passage library. No confirmation is required to finish this research.

## Reproduction and retained artifacts

**VERIFIED_BY_RUNNING:** local work in this session was file reading/writing, stdlib text/JSON processing, modest source downloads and Kaggle CLI. Model inference, decode/resampling, DSP and syllable-package use ran only on private CPU Kaggle. No GPU, local environment installation, repository commit or account mutation outside the allowed kernel occurred.

Kernel ID: `electroknight/cvoice-probe-alignment`; private, GPU/TPU disabled, internet enabled; dataset `electroknight/cvoice-probe-audio`. Three additional pushes: versions 3–5. Final metadata is [kernel-metadata.json](kaggle/kernel-metadata.json).

```text
kaggle kernels push -p kaggle --timeout 1800
kaggle kernels status electroknight/cvoice-probe-alignment
kaggle kernels output electroknight/cvoice-probe-alignment -p kaggle_out/automatic_v5
```

Current `kaggle/probe.py` is the self-contained E9 kernel. E1–E8 source is `probe_e1_e8.py`; stage that file as the sole uploaded `probe.py` only if those diagnostics need reproduction. The earlier local timing evidence remains in `time_base_t1.txt`, `time_base_run2.txt`, `time_base_run3.txt` and output JSONs; it predates the compute restrictions and was not rerun.

## Sources

**VERIFIED_BY_SOURCE:** retained paper files and PyPI snapshots were fetched by the earlier researcher; new official docs/repos/page texts were fetched in this session. They support source claims, not verification of deployed runtime.

- [MFA 2026, v1](https://arxiv.org/html/2606.18466v1): `web/arxiv_2606.18466v1.txt`, Table 4 and alignment protocol.
- [Label-prior CTC, v3](https://arxiv.org/html/2406.02560v3): `web/arxiv_2406.02560v3.txt`, Tables 1–2, WBE definition.
- [Rousso comparison, v1](https://arxiv.org/html/2406.19363v1): `web/arxiv_2406.19363v1.txt`, word-end protocol.
- [FuseAlign, v1](https://arxiv.org/html/2609.33650v1): `web/arxiv_2609.33650v1.txt`, §§3/6 and Appendix G.
- [TorchAudio API](https://docs.pytorch.org/audio/2.10.0/generated/torchaudio.functional.forced_align.html): `web/ta_210_forced_align.html`; [2.9 package](https://pypi.org/pypi/torchaudio/2.9.0/json): `web/ta29_wheel_audit.json` and extracted sources.
- [Base model](https://docs.pytorch.org/audio/2.10.0/generated/torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H.html), [MMS model](https://docs.pytorch.org/audio/2.10.0/generated/torchaudio.pipelines.MMS_FA.html): versioned official model descriptions/licences; earlier bundle audit in condensed log.
- [CTC wrapper](https://github.com/MahmoudAshraf97/ctc-forced-aligner): `web/ctc_aligner_readme.md`, `web/ctc_aligner_license.txt`, saved PyPI metadata.
- [NeMo NFA](https://github.com/NVIDIA-NeMo/Speech/blob/main/tools/nemo_forced_aligner/README.md): `web/nemo_aligner_readme.md`; [MFA installation](https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html).
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper): `web/faster_whisper_readme.md`, official CPU benchmark with its own hardware/thread count.
- [Qwen](https://github.com/QwenLM/Qwen3-ASR): `web/qwen_asr_readme.md`; [Nyra](https://nyra-labs.com/research/nyra-forced-aligner): `web/nyra_page.html`, `web/nyra_page.txt`.
- [Reagan official transcript](https://www.reaganlibrary.gov/archives/speech/address-nation-explosion-space-shuttle-challenger): `kaggle_out/automatic_v5/official_transcript.html` and `.txt`; page acquisition independent of excerpt selection.
- PyPI package/license/version/Requires-Python declarations: retained `web/pypi_*.json`; [WhisperX](https://pypi.org/pypi/whisperx/json), [MFA](https://pypi.org/pypi/montreal-forced-aligner/json), [NeMo](https://pypi.org/pypi/nemo-toolkit/json), [faster-whisper](https://pypi.org/pypi/faster-whisper/json), [whisper-timestamped](https://pypi.org/pypi/whisper-timestamped/json), [stable-ts](https://pypi.org/pypi/stable-ts/json), [ctc-segmentation](https://pypi.org/pypi/ctc-segmentation/json).
