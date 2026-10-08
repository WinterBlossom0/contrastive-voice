# Acoustic features and speaker normalization — final research report

Research date: 2026-10-01. Topic: `features`. This is a research specification, not a product implementation.

Evidence labels: **VERIFIED_BY_RUNNING (VR)** identifies a retained output; **VERIFIED_BY_SOURCE (VS)** identifies a fetched primary source; **UNVERIFIED (UV)** identifies an untested design decision or unresolved claim. Recommendations are design choices informed by evidence, not validated human grading rules. Relative paths below are relative to this directory.

## Recommendation

Use **Praat raw autocorrelation through `praat-parselmouth==0.4.7`**, recording-adaptive two-pass bounds, and robust pitch summaries; Hann-weighted frame RMS in dB with recording-level centering; transcript-based duration/rate and energy-confirmed gaps; explicit word prominence markers; and **one clarity proxy, MFCC-delta magnitude**. Keep spectral alpha ratio as an optional vocal-effort/channel diagnostic, with no automatic penalty. Exclude HNR, CPP, jitter, shimmer, formants, centroid, flux and Hammarberg index from the scoring path. No GPU or neural pitch model is needed at runtime.

This supports D1 Pace, D2 Pauses, D3 Pitch variation, D4 Emphasis, D5 Volume and D7 Endings. D6 Clarity is experimental and scoreable only for a recording and its matched synthetic mirror (R1); across archival/TTS/microphone recordings (R2), display it without a deduction. Describe all indices as **distance from the reference rendition**, not rhetorical quality or speaker-independent human grades. Energy measures acoustic recording level, not calibrated sound pressure or vocal effort.

**VR:** feature extraction is inexpensive; the largest risks are measurement validity, channel effects and alignment error. A fixed gain is removable, whereas compression, noise and bandwidth changes are not. Existing normalization demonstrations and FDA pitch truth are in `kaggle_out/v1/out/` and `kaggle_out/v2/out/`. The additional critic-focused validation is documented below.

## 1. Signal conventions and exact recommended definitions

### 1.1 Shared definitions and parameters

Let the canonical PCM be mono float64 `x[n]`, full scale 1, sample rate `Fs=16000 Hz`. Select a channel before resampling: the Reagan source has anti-phase stereo; plain averaging cancels speech. Resample with `soxr==1.1.0`, `quality="HQ"`; remove the recording mean once, and store the canonical PCM hash and channel choice. Do not dynamically normalize/compress the audio. For a mono source this is simply `x[n]=y[n]−mean(y)` after resampling. Source selection is a recording-QA decision, not an inference about delivery.

Time grid `t_k=kH/Fs`, `H=160` samples (10 ms). For energy and spectra, `N=400` (25 ms), `w[n]=0.5−0.5 cos(2πn/(N−1))`, `0≤n<N`; centered frame `x_k[n]=x[kH+n−N/2]`, zero padding at file edges. Exclude edge-padded frames from quantitative summaries. Quantile `Q_p` uses linear interpolation: sorted values `a_(0)…a_(m−1)`, `h=(m−1)p/100`, `Q_p=(1−h+floor(h))a_(floor(h))+(h−floor(h))a_(ceil(h))`. Empty populations are missing, never zero. SD below uses divisor `m`.

Word `i` has independently aligned participant/baseline span `[a_i,b_i)`, duration `d_i=b_i−a_i`, syllable count `s_i≥1`; `K_i={k:a_i≤t_k<b_i}`. Phrase/window `W_i` contains up to five consecutive words, `i−2…i+2`; its frame population is the union of their `K_i`, with edge-padded frames excluded. A phrase may instead be delimited by transcript punctuation. Always retain participant true timestamps. Frame centers spaced by 10 ms do not imply 10 ms boundary accuracy.

The earlier probe's `word_regions()` extends CTC spikes by 50 ms and splits gaps shorter than 150 ms; this is **not validated word-boundary correction**. Use its results as sensitivity evidence, not as ground truth. The product must use the alignment topic's validated boundaries. Quantitative report tables distinguish actual Reagan words from JFK's 88 pseudo-units.

### 1.2 Definition → consumer → evidence table

Every feature retained in the recommended runtime has a consumer here. Formula details and validity masks are part of the definition, not optional implementation details.

| Feature | Exact mathematical definition | Consumer and restrictions | Evidence |
|---|---|---|---|
| F0, Hz; voicing | `f_k=Fs/τ*_k`, where `τ*_k` is the candidate lag selected by Praat's autocorrelation/path algorithm; unvoiced is missing in display and `v_k=0` internally. Precise estimator/version/settings in §2. | D3, D4, D7; raw-Hz toggle and extraction QA. | VS [Praat algorithm](https://www.fon.hum.uva.nl/praat/manual/pitch_analysis_by_raw_autocorrelation.html); VR FDA files in §2. |
| Centered F0 contour, st | `S_k=12log2(f_k/Q50({f:v=1}))`, only when `v_k=1`. | D3 melody overlay; D4 prominence; D7 final movement. Never fill unvoiced spans for scoring. | VR v3 uses this exact Hz-median convention; v2 uses the log-median variant described below. VS [Nolan 2003](https://www.internationalphoneticassociation.org/icphs-proceedings/ICPhS2003/papers/p15_0771.pdf). |
| Word pitch median and high excursion | `M_i=Q50({S_k:k∈K_i,v_k=1})`; `F_i=Q90` of the same set. | D3 local level diagnostic, D4 high-pitch prominence; replace raw maximum. | VR word aggregation and targeted prominence check; robust choice UV for perceptual accuracy. |
| Pitch range | `R_W=Q90({S_k:k∈W,v_k=1})−Q10(...)`. Global `R_recording` uses all valid voiced frames. Local/global deltas `R_W^P−R_W^B`, `R_recording^P−R_recording^B`, in st. | D3 monotone/exaggerated range. Preserve amplitude of variation; no per-recording variance division. | VR F0-compression tests; v1/v2 also report a **different**, legacy P95−P5 range. Do not relabel that as P90−P10. |
| Voiced coverage and availability | `V_W=Σ_{k∈W}v_k / #K_W`; a word requires ≥5 valid voiced frames; five-word D3 range requires ≥50 (0.5 s); D7 final/preceding populations each require ≥5. Otherwise missing. | QA/abstention for D3, D4, D7, never a rubric penalty. | VR `voiced_frac` values; stricter validity gates are UV design choices. |
| Final pitch movement | `T_j=median(S on final word j)−median(S on words j−2,j−1)`, at `.`, `?`, `!`; delta `T_j^P−T_j^B`. | D7 Endings; direction interpreted against that reference and punctuation. | Definition matches rubric research; UV ending-detection accuracy here. |
| Frame energy / RMS dBFS | `P_k=Σ_n w[n]x_k[n]^2 / Σ_n w[n]`; `L_k=10 log10(P_k+10^−12)`. Equivalent weighted RMS `sqrt(P_k)`. | D5 raw energy-contour overlay and acoustic-pause support; D4 intensity. | VR `frame_level_db()` and energy recovery; 25 ms convention VS [Kaldi feature docs](https://kaldi-asr.org/doc/feat.html). |
| Gain-normalized energy | `E_k=L_k−median_{v=1}L`; require ≥10 voiced reference frames, else missing. Word `Emean_i=mean_{k∈K_i}E_k`, `E90_i=Q90_{k∈K_i}E_k`. D5 window mean uses aligned word frames, excluding confirmed gaps. | D5 mean level/contour; D4 intensity prominence. No global absolute-volume score. | VR gain tests in v2 and targeted ramp tests. Existing v2 `e_rel_med` exactly implements centering but has a fallback mask that should not silently permit failed-pitch clips. |
| Phrase energy range and slope | `ER_W=Q90(E_W)−Q10(E_W)`; `β_W=Σ(t_k−t̄)(E_k−Ē)/Σ(t_k−t̄)^2`, at least 5 speech frames at distinct times, dB/s. | D5 fade/compression diagnostics; same data as energy overlay, not independent added penalties. | VR injected-ramp recovery for contour; automatic phrase-end decision UV. |
| Word duration and length per syllable | `d_i=b_i−a_i`; `D_i=ln(d_i/s_i)` (d in seconds; reference unit 1 s). | D1 and D4. Duration carries alignment uncertainty. | VR analytic time-scaling in v2; syllables in those probes are heuristic, not dictionary truth. |
| Speaking rate | Over elapsed window `[a,b)`, `SR_W=Σ_{i∈W}s_i/(b−a)` syllables/s; `WPM_W=60 #W/(b−a)`. Includes internal pauses; remove leading/trailing silence by using passage endpoints. | D1 Pace display and global tempo. | VS [De Jong & Wempe](https://doi.org/10.3758/BRM.41.2.385); VR rate values in v2 are not accuracy-validated boundaries. |
| Articulation rate and local pace | `A_W=(b−a)−Σ B_i g_i` over internal gaps; `AR_W=Σs_i/A_W`, require `A_W>0`. Primary local pace `f_i=ln A_W`; global tempo `Gpace=median_i ln(A_W^P/A_W^B)`. Centered local difference `(f_i^P−median f^P)−(f_i^B−median f^B)` on matched word windows. | D1 Pace; separately keep global tempo so centering does not hide uniform rushing. | UV pause/refined-boundary accuracy; mathematical definition and known-time-map sensitivity verified, §5. |
| Pause presence, duration and transformed duration | Gap `G_i=[b_i,a_(i+1))`; find longest contiguous run of frame centers in `G_i` with `L_k<θ` and `v_k=0`; duration `g_i=0.01 #run` (0 if none); `B_i=1[g_i≥0.25]`; `Y_i=ln(max(g_i,0.1)/0.1)`. Compare presence first; compare seconds/log-duration if present in either. | D2 Pauses. Only eligible inter-word gaps; a short stop closure is not a rhetorical pause. | VS [De Jong & Bosker 2013](https://www.isca-archive.org/diss_2013/jong13_diss.pdf); v2 threshold probe supports adaptive threshold but has no manual pause truth. |
| Word prominence and stress marker | `u_i=(D_i,F_i,E90_i)`; baseline component centers `m_j=median_i u_ij^B`, scales `σ_j=max(1.4826 median_i\|u_ij^B−m_j\|, ε_j)` using each component's available population, with `ε=(ln1.15,3 st,3 dB)`; `p_i=(1/3)Σ_j(u_ij−m_j)/σ_j`, requiring all three components. A marker is `p_i≥0.75` and a local maximum within ±1 word, ignoring unavailable neighbors; ties choose earlier word. | D4 Emphasis, visible stress-point candidates on both plots; baseline landmarks used for lost-emphasis comparisons. Frozen centers/scales and threshold are design conventions, not human stress labels. | VR targeted R1 recovery; §6. Physically grounded components VS Fry, Sluijter, Kochanski; weights/threshold UV perceptually. |
| MFCC and temporal delta intermediates | Spectrum/filterbank/DCT definition in §3; `Δc_kj=[(c_(k+1),j−c_(k−1),j)+2(c_(k+2),j−c_(k−2),j)]/10`, edge replication. | Only intermediate inputs to D6 proxy; c0 excluded, no raw-MFCC speaker-distance penalty. | VR v1/v2 hashes and channel/smoothing tests. |
| Spectral-change / clarity proxy | `Q_k=sqrt(Σ_(j=1)^12 Δc_kj^2)`; `Q_W=mean_{aligned word frames∈W}Q_k`; comparison `C_W=ln((Q_W^P+10^−6)/(Q_W^B+10^−6))`; report global `C_recording` as well. | D6 Clarity, R1 only. Display name: **spectral-change proxy**; slower articulation/noise can reduce it without mumbling. | VR matched WORLD smoothing lowers Q; nuisance changes also lower it (§4). Log-comparison formulation is UV as a detector calibration. |
| Optional alpha ratio | `α_k=10log10[(Σ_(1000≤f_r<5000)P_kr+10^−12)/(Σ_(50≤f_r<1000)P_kr+10^−12)]`; display word voiced-frame mean and recording-centered `α_k−median_voiced α`. | D4/D5 effort diagnostic and D6 channel-QA context **only**, no deduction. Helps explain that a gain fade alone leaves spectral balance unchanged. | VR v2 EQ/gain/smoothing tests; VS [Sluijter & van Heuven](https://doi.org/10.1121/1.417955). |

For temporal emphasis localization, marker time is the earliest `t_k∈K_i` attaining maximal `L_k` (intensity peak), with `[a_i,b_i)` as uncertainty span; a word-center fallback `(a_i+b_i)/2` must be labeled as such. This marker-time rule is **UV**: marker recovery below tests word identity, not manually labeled intra-word peak timing. Do not advertise sample-accurate rhetorical stress times.

**Prominence across renditions:** the exact tested score above freezes centers/scales from the original for R1. Before interpreting R2 emphasis, compensate overall tempo by replacing participant `D_i` with `D_i−Gdur`, `Gdur=median_i(D_i^P−D_i^B)` over matched valid words. Use the same baseline scales, not participant SD/MAD. This additional tempo correction is **UV**; preserve `Gdur` separately for D1. Re-estimating each component scale on flattened speech would normalize the flaw away. Content/function status provides context, not a rule that all function words are unstressed.

### 1.3 Recording and local normalization

Center F0 and energy over the **whole matched 20–40 s passage**, separately for each recording. Cache these reference values; never recenter each five-word window when measuring a fade. For level/gain, `L(gx)≈L(x)+20log10|g|`, and median centering cancels the additive constant; epsilon, clipping and changing validity masks prevent exact invariance at very low levels. Likewise `S(cf)=S(f)` algebraically for positive constant c and unchanged voiced decisions. These are algebraic properties, not invariance to a new human voice. Earlier v1/v2 extraction centers using `12(log2 f−Q50(log2 f))`; v3 and the recommended definition use `12log2(f/Q50(f))`. They coincide for odd counts, but interpolation and log do not commute for even counts. Do not claim byte-identical centers across those conventions; the v2 shift demonstration is evidence for its explicitly stated variant.

For comparison, `Zf_k=(log2 f_k−μ_logf)/σ_logf` and `Ze_k=(L_k−μ_L)/σ_L` were tested but **are not recommended scoring features**: self variance scaling hides pitch flattening and dynamics compression. CMN/CMVN definitions for MFCC j are `c'_kj=c_kj−μ_j`, `c''_kj=(c_kj−μ_j)/max(σ_j,10^−6)`, with population statistics over speech frames. CMN reduces stationary channel offsets approximately; CMVN is not speaker invariance and may erase spectrum-dynamics edits. No per-recording normalization can reconstruct information removed by band-limiting, AGC or noise suppression.

**VR:** in `kaggle_out/v2/out/misc.json/refstab`, using 5 s windows rather than full speech gives JFK median-F0 absolute deviations of 1.408 st median/3.141 st p90 and integrated-level deviations 1.770/4.352 LU; at 30 s these are 0.841/2.000 st and 1.038/3.427 LU. These are within-speech variation, not error against biological truth. **VS:** [Arantes & Eriksson 2014](https://www.isca-archive.org/speechprosody_2014/arantes14_speechprosody.pdf), saved `papers/arantes_eriksson_2014.txt`, found mean/median stabilization around 10 s on their materials; not a universal guarantee. Require sufficient speech and expose reference-duration/voiced-count QA.

## 2. F0 comparison, exact tracker and accuracy

### 2.1 Estimator and recommended settings

**VS:** corrected autocorrelation is `r_x(τ)≈r_(xw)(τ)/r_w(τ)`, normalized to strength at lag zero. Praat finds interpolated peaks in lags corresponding to permitted F0, includes an unvoiced candidate, and chooses a minimum-cost path balancing candidate strength, octave preference, octave transitions and V/UV transitions. The exact executable definition is the pinned bundled Praat algorithm, not a bare `argmax autocorrelation`. See [Praat manual](https://www.fon.hum.uva.nl/praat/manual/pitch_analysis_by_raw_autocorrelation.html), `papers/boersma_1993.txt` and `src_refs/praat_Sound_to_Pitch.cpp`.

`parselmouth.Sound(..., sampling_frequency=16000).to_pitch_ac`: `time_step=0.01`, initial `pitch_floor=60`, `pitch_ceiling=700`, `max_number_of_candidates=15`, `very_accurate=False`, `silence_threshold=0.03`, `voicing_threshold=0.45`, `octave_cost=0.01`, `octave_jump_cost=0.35`, `voiced_unvoiced_cost=0.14`. Collect positive first-pass values; if ≥20, second bounds `floor=max(50,0.75 Q25(f))`, `ceiling=min(800,1.5 Q75(f))`; otherwise use `75–600 Hz` and mark range estimation uncertain. Same settings on second pass. Map native Praat times to nearest 10 ms grid center, ties earlier, tolerance ≤10 ms, otherwise missing. Then a five-frame median filter **within each contiguous voiced run only**, with replicated run endpoints, defines the final `f_k` used for display and summaries: for a voiced run `[a,b]`, `f_k=median{f_raw[clip(k+j,a,b)]:j=−2…2}`. Leave gaps missing and retain the raw track for QA.

**VR:** Parselmouth 0.4.7 bundles **Praat 6.1.38 (2021-01-02)**. Current standalone Praat's preferred *filtered* autocorrelation is not the method bundled in that package. The research's FFT Gaussian prefilter was an approximation, not a verified replacement for current Praat. It performed badly under telephone band-limiting. Keep the measured raw method. **VS:** adaptive quartile bounds are supported by [Hirst 2011](https://econtents.sbu.unicamp.br/inpec/index.php/joss/article/view/15011), saved `papers/hirst_2011_joss.txt`; that paper also discusses a wider `2.5 Q75` ceiling.

For unknown adult male/female voices, data-driven bounds avoid needing sex labels; they do not guarantee children, shouting or creaky voice. Reject/report abrupt octave-scale transitions rather than automatically doubling/halving: provisional QA marks both frames of any adjacent voiced pair with `|12log2(f_k/f_(k−1))|>6 st`; this rule needs validation and is **UV**, so it must not silently change measured numbers in the present evidence. Do not use Praat `Kill octave jumps`: **VR** FDA clean GPE increases from 0.831% to 6.681%, octave-error rate from 0.329% to 5.798% (`v1/out/fda_classical.json`). A five-frame median did not improve clean GPE (0.831→0.848%); smoothing is not established error correction.

### 2.2 Common ground-truth comparison

**VR:** FDA database has 100 utterances, one male/one female, 331.6 s total (146.6/185.0 s), laryngograph-derived `.fx` reference. Audio big-endian PCM 20 kHz, resampled 4/5 to 16 kHz. Reference is linearly interpolated only within each voiced `.fx` segment; gaps remain unvoiced. 10 ms evaluation grid, 33,260 frames including endpoints. Archive SHA256 `7f619d673c6ac09e698da9c57df76ad28f48638697fbfaf81db9759c6bd8b512`; [FDA primary dataset](https://www.cstr.ed.ac.uk/research/projects/fda/fda_eval.tar.gz), retained `fda/README` and sample references. This clean read-speech corpus is not representative of all oratory/channels.

Define B = frames reference and estimate both voiced; `GPE20=100 #{k∈B:|fhat/fref−1|>0.2}/#B`; `VDE=100 #(vhat≠vref)/N`; `FFE=100 [#V/UV mismatch+#gross-on-B]/N`; `octave=100 #{k∈B:|1200log2(fhat/fref)−1200|<100 or |...+1200|<100}/#B`. GPE excludes missed voicing; always report VDE/FFE beside it. Fine cents are mean absolute cents only on nongross B. These definitions differ from some published FFE implementations; do not mix their numbers.

| Tracker / setting | Clean GPE % | VDE % | FFE % | Octave % | CPU seconds/audio-second | Evidence/environment |
|---|---:|---:|---:|---:|---:|---|
| Praat AC 75–600 | 0.831 | 4.531 | 4.820 | 0.329 | 0.0020 | v1/classical, AMD |
| Praat CC 75–600 | 1.640 | 4.693 | 5.271 | 0.624 | 0.0042 | v1/classical, AMD |
| AC two-pass per utterance, Q75×1.5 | 0.470 | 4.290 | 4.453 | 0.043 | 0.0076 | v2/f0x, Intel; unsmoothed |
| AC two-pass per speaker Q75×1.5 | 0.441 | 4.113 | 4.266 | 0.052 | 0.0016 | v1/classical; pools clean references; not the per-upload method |
| pYIN 75–600, 1024 samples | 1.127 | 13.984 | 14.366 | 0.115 | 0.0532 | v1/classical; librosa 1.0.0 |
| DIO+StoneMask 75–600 | 0.805 | 8.070 | 8.355 | 0.068 | 0.0056 | v1/classical |
| Harvest 75–600 | 1.132 | 23.031 | 23.449 | 0.147 | 0.1774 | v1/classical |
| SWIPE, threshold 0.3 | 0.481 | 7.956 | 8.121 | 0.035 | 0.0285 | v2/fda_extras |
| RAPT, voice_bias 0 | 1.959 | 5.550 | 6.224 | 0.525 | 0.0030 | v2/fda_extras |
| YAAPT | 1.385 | 4.756 | 5.259 | 0.149 | 0.0723 | v2/fda_extras |
| FCPE, threshold 0.006 | 1.093 | 8.139 | 8.542 | 0.114 | 0.0247 | v1/neural; all 100 files |
| CREPE tiny | 0.972 | 10.000 | 10.331 | 0 | 0.1813 | v1/neural; **20 files only** |
| CREPE full | 1.852 | 8.176 | 8.805 | 0 | 4.9634 | v1/neural; **4 files only** |

All rows VR from `kaggle_out/v1/out/fda_classical.json`, `fda_neural.json`, `kaggle_out/v2/out/fda_extras.json`, `f0x.json`; subset/CPU/environment differences prevent a single ranked speed contest. pYIN's 1024-sample frame is 64 ms, not the 25 ms spectral window. Neural thresholds influence VDE strongly. CREPE full/tiny zero observed octave errors on small subsets is not a zero-error guarantee.

| Unselected option | Accuracy/source, cost and installation assessment |
|---|---|
| RMVPE | VS [paper](https://arxiv.org/abs/2306.15412), `papers/rmvpe_2306.15412.txt`: designed for vocals in polyphonic music. UV speech CPU accuracy/determinism here; heavier torch/checkpoint path, no reason to replace measured AC. |
| FCPE | VS [paper](https://arxiv.org/abs/2509.15140), `papers/fcpe_2509.15140.txt`: music-oriented RPA and GPU speed do not predict FDA speech results. VR installed 40.22 MB pure wheel plus torch/dependencies; useful **offline independent verifier**, not runtime default. |
| PENN | VS [paper](https://arxiv.org/abs/2301.12258): speech/music estimator, reported 11.2× real time on a 10-core i9. VR earlier local import failed because torbi had no matching `pt214cpu` binary; no working benchmark here. UV on Kaggle/current CPU stack; do not promise its published speed. |
| CREPE/torchcrepe | VR torchcrepe wheel 72.33 MB plus torch, librosa/resampy; earlier CPU runs not bit-identical. v1 neural test used **two torch threads** and CREPE-tiny repeats differed by up to 2.751 Hz (`fda_neural.json`). Deterministic runtime choice remains AC. |
| SWIPE/YAAPT | VR useful independent classical comparisons, but SWIPE's telephone-band GPE 16.267% and YAAPT's slower cost; pysptk has no cp312/313/314 wheels. v1 pysptk failed on missing `pkg_resources`; v2 worked with older setuptools. |

**VS published triangulation:** [Strömbergsson 2016](https://www.isca-archive.org/interspeech_2016/strombergsson16_interspeech.pdf), Table 2, all-speaker FFE 7.05% for default Praat and 6.20% with sex-adapted range, versus default RAPT 12.53% and YIN 26.86% (YIN is not pYIN). [Jouvet & Laprie 2017](https://www.eurasip.org/Proceedings/Eusipco/Eusipco2017/papers/1570342455.pdf) found clean AC FFE 5.05%, while real noisy speech favored RAPT around 8.5–8.6% over AC 10.2%. Saved paper texts in `papers/`. These support conditional, dataset-specific selection rather than universal superiority.

### 2.3 Noisy/band-limited failure evidence (I-12)

**VR:** v1 per-utterance adaptive AC on 10 dB additive noise: GPE 0.303%, VDE 5.129%, FFE 5.229%; clean 0.470/4.290/4.453%. Lower GPE with noise partly reflects harder frames becoming unvoiced. For clean per-utterance q1.5 in v2, male/female GPE 0.301/0.615%, VDE 5.337/3.461%, FFE 5.445/3.666% (`f0x.json`).

The same adaptive AC on FDA telephone 300–3400 Hz: GPE 1.148%, VDE 8.548%, FFE 8.891%; FCPE 25.069/19.910/29.179%. Critically, on real band-limited Reagan, v2 per-word centered F0 changes by **6.780 st MAE**, despite FDA's much smaller aggregate gross error. JFK changes by 0.217 st. FDA does not settle missing-fundamental errors in archival speech. `f0x.json/files` compares with original AC, **not independent truth**, for those two clips.

At q1.5 vs q2.5, 1.011% of JFK's wider-pass voiced frames exceed the narrow ceiling: 112 become unvoiced and 144 become approximately halved. The wider tracker is not truth; its outliers may also be erroneous. Do not automatically widen the range to recover supposed emphasis. Report bounds, edge hits, valid-frame availability and tracker disagreement, and abstain on suspect narrowband recordings. Manual/human oratory pitch truth is absent.

## 3. Energy/loudness and spectral definitions

### 3.1 RMS, LUFS and normalization choice

Use RMS for the time-local energy contour; median centering removes uniform gain while keeping physical dB differences. Perceptual loudness is useful recording metadata, not an extra D5 penalty. A-weighting is a frequency-weighting convention and is not an integrated speech loudness or stress estimator; it is not selected.

If LUFS metadata is retained, use the independent library `pyloudnorm==0.2.0`, default K-weighting and 0.4 s block size. The BS.1770 mono definition is `z_b=mean(y_K^2)` over 400 ms blocks every 100 ms, `l_b=−0.691+10log10 z_b`; retain `A={b:l_b>−70}`; `L_A=−0.691+10log10(mean_A z_b)`; final `G={b∈A:l_b>L_A−10}`; `L_I=−0.691+10log10(mean_G z_b)`. Empty G => missing. K-weighting is high shelf followed by RLB high-pass. For a canonical 48 kHz reference, biquads are `(b0,b1,b2;a0,a1,a2)`:

```text
(1.53512485958697,-2.69169618940638,1.19839281085285;1,-1.69065929318241,0.73248077421585)
(1,-2,1;1,-1.99004745483398,0.99007225036621)
```

Sample-rate-adapted formulas used by the *probe's custom* implementation are in `worker.py/k_weight_sos()`: shelf `(f0,G,Q)=(1681.974450955533,3.999843853973347,0.7071752369554196)` and HP `(f0,Q)=(38.13547087602444,0.5003270373238773)`, bilinear transform. **Do not treat that custom 16 kHz meter as certified LUFS:** it differs from pyloudnorm by approximately 0.12–0.13 LU; its 48 kHz implementation is closer. The 25 ms `lk_db` frame contour in the probe is not a BS.1770 momentary loudness measurement. The selected contour is explicitly RMS dBFS.

**VS:** [ITU-R BS.1770-5](https://www.itu.int/rec/R-REC-BS.1770-5-202311-I/en), `papers/itu_bs1770_5.txt`; [EBU Tech 3342](https://tech.ebu.ch/docs/tech/tech3342.pdf), `papers/ebu_tech3342.txt`. EBU LRA, if shown only as recording metadata, is `Q95−Q10` of 3 s short-term loudness after absolute −70 LUFS/relative −20 LU gating; too few blocks => missing. The probe's 100 ms stepping is stated and is not a guarantee of full EBU conformance.

**VR:** `v2/out/misc.json/loudness` and timing output cross-check Reagan full: custom 16 kHz −31.500, 48 kHz reference −31.584, pyloudnorm −31.627 LUFS; ffmpeg ebur128 rounds to −31.6, LRA 6.1. JFK: −17.718/−17.786/−17.837, ffmpeg −17.8, LRA 8.8. This verifies implementation agreement to about 0.13 LU, not perceptual energy-contour correctness.

### 3.2 Exact MFCC path and alternatives

`X_kr=Σ_(n=0)^399 w[n]x_k[n] exp(−2πirn/512)`, `P_kr=|X_kr|²`, `r=0…256`, `f_r=rFs/512`. Zero padding to 512 gives bin spacing 31.25 Hz; true resolving power is governed by the 25 ms window. This is a conventional speech frame duration/hop, not pitch's 3/floor period-dependent window. **No pre-emphasis, dither, spectrum normalization or per-frame peak normalization** in the defined probe path.

Mel `m(f)=2595log10(1+f/700)`; 42 equally spaced mel points from 50 to 7600 Hz converted back to Hz. For filter j=0…39 with consecutive points `(l_j,c_j,h_j)`, `B_j(f)=max(0,min((f−l_j)/(c_j−l_j),(h_j−f)/(h_j−c_j)))`; no area normalization. `A_kj=Σ_r B_j(f_r)P_kr`; `a_kj=ln(A_kj+10^−10)`; orthonormal DCT-II `c_kq=γ_q Σ_(j=0)^39 a_kj cos[πq(j+1/2)/40]`, `γ_0=1/sqrt40`, `γ_(q>0)=sqrt(2/40)`, q=0…12. Feed c1…c12 into §1 delta/Q. Values are per-frame cepstral-change units, not changes per second; 10 ms hop is fixed. For negligible mel energy the epsilon breaks ideal gain cancellation. The defined Q uses all eligible aligned-word frames, including unvoiced consonants; an added quiet-frame mask would be a different, untested feature.

| Candidate examined but not scored | Definition/comparison and decision |
|---|---|
| Normalized spectral flux | `M_kr=sqrt(P_kr)/sqrt(Σ_r P_kr)`; `flux_k=\|\|M_k−M_(k−1)\|\|2`, first frame 0. Redundant dynamics cue; remove because D6 already has Q. |
| Power centroid | `Σ_r f_r P_kr/Σ_r P_kr`, Hz. Strong channel/speaker dependence; remove. |
| Hammarberg index | `10log10[max_(0≤f<2000)P / max_(2000≤f<5000)P]`, eps as alpha. Peaks/window/channel confounds; remove. |
| Spectral slopes | Least-squares slope of `10log10(P+eps)` vs f in kHz, over 0–500 and 500–1500 Hz. Useful effort-related descriptors, but alpha already serves diagnostic role; remove. |
| eGeMAPSv02 | VR opensmile 2.6.0 produced 25 low-level descriptors, 88 functionals per its feature inventory; §4/§7 contain cost/license. Standardized feature inventory is not stress ground truth; not runtime default. |

## 4. Articulation/clarity: what the probe actually supports (I-19)

**VS:** clear speech is a bundle of segmental and temporal properties, not spectral smoothness alone: [Picheny et al. 1986](https://doi.org/10.1044/jshr.2904.434) and [Krause & Braida 2004](https://doi.org/10.1121/1.1635842), fetched abstracts retained in `papers/pubmed_abstracts.txt`. Low-frequency envelope modulations are relevant to intelligibility, but that association does not identify mumbling for a few words.

| Proxy | Suitability for short connected speech and channels | Decision |
|---|---|---|
| MFCC-delta magnitude Q | Works on short windows, deterministic, gain resistant except floor effects. Sensitive to speed, bandwidth, noise/reverb and codec; no proved human intelligibility scale. | One experimental D6 R1 proxy. Preserve uncentered global Q so whole-passage smoothing remains detectable. |
| Aligner path posterior | Given aligned target token c_t, `conf_i=exp[(1/#T_i)Σ_(t∈T_i)ln p_t(c_t)]`, nonblank target frames in word; missing if none. This is confidence, **not phonemic GOP**. A phone-GOP likelihood ratio would require competing-phone likelihoods. | QA/abstention and optional display only; exclude from D6 score. |
| HNR | `10log10(r/(1−r))` for estimated periodic-energy fraction r; probe uses Praat CC, 75 Hz floor, 10 ms hop, 1 period/window. Noise, reverb, bandwidth and phonation confound articulation. | Remove from clarity/delivery scoring. |
| CPP/CPPS | Cepstral peak above fitted baseline, with parameter-dependent smoothing; connected-speech voice quality rather than articulation. Probe's custom CPP and Praat CPPS are different measurements. | Remove custom estimator; no dysphonia inference. |
| Jitter/shimmer | Cycle-duration variability divided by mean duration; cycle-amplitude variability divided by mean amplitude. Periodic segments/appropriate vowel material needed; short-word definitions fail often. | Exclude. VR defined only ~40% Reagan/~65% JFK pseudo-units on full speeches, not proof of valid measurement when defined. |
| Formants/vowel-space | Articulatory vowel-space dispersion depends on vowel identity, speaker anatomy and tracking. A short phrase does not balance phonemes or remove bandwidth effects. | Exclude automatic clarity; phone-conditioned vowel studies would require additional labels. |
| Envelope modulation 2–8 Hz | Probe normalized RMS envelope `e=10^(L/20)`; `M(f)=2\|FFT[(e/mean(e)−1)Hann]\|²/(NΣHann²)`, 256 envelope frames (2.56 s), 0.5 s hop; ratio `Σ_(2≤f≤8)M / Σ_(0.5≤f≤20)M`. Poor few-word temporal precision, speed/channel confounds. | Optional research corroboration only; not recommended runtime feature. |

**VR posterior evidence:** `v1/out/gop_sys.json` original mean word log-posterior −0.223; 7/74 words below −1, worst original −2.814. Identity WORLD copy −0.342; telephone −0.384; 20 dB noise −0.513; mild/strong smoothing −0.539/−2.041; uniform speedup −0.498. Noise and speed imitate decreased clarity; high forced-alignment likelihood does not establish clear pronunciation. Runtime CPU forward-pass RTF ~0.12–0.13 plus model load 4.1 s; using it as a clarity classifier buys no validated construct.

**VR channel/energy table:** mean absolute word differences vs original, v2 `inv_reagan.json` / `inv_jfk.json`. JFK has pseudo-units, not genuine word annotation. Q is in cepstral-change units; E is RMS normalized to voiced-frame median, dB. These are feature differences, not detector false-positive rates.

| Perturbation | Reagan E MAE dB | JFK E MAE dB | Reagan Q MAE | JFK Q MAE | Interpretation |
|---|---:|---:|---:|---:|---|
| −9 dB uniform gain | <0.00001 | <0.00001 | <0.00001 | <0.00001 | Gain cancellation works on these floats. |
| MP3 32 kbit/s, lag corrected | 0.053 | 0.067 | 0.097 | 0.222 | Small E error; Q more codec sensitive. |
| 300–3400 Hz band-limit | 1.774 | 1.832 | 0.078 | 0.090 | Channel changes can imitate level differences; Reagan F0 fails badly too. |
| White noise, whole-clip SNR 20 dB | 0.392 | 1.178 | 0.498 | 0.200 | Particularly affects quiet frames and Q. |
| Synthetic reverb RT60 .4 s, DRR 5 dB | 0.933 | 2.465 | 0.320 | 0.214 | Energy dynamics and spectrum dynamics change. |
| Envelope compression amount .6 | 2.430 | 5.177 | 0.001 | 0.001 | Gain normalization cannot cancel time-varying processing. |
| WORLD mild smoothing | 0.927 | 0.766 | 0.845 | 0.529 | Compare also with matched WORLD identity. |
| WORLD strong smoothing | 0.909 | 0.576 | 1.387 | 0.899 | Synthetic Q sensitivity, not validation of human mumble. |

Matched identity Q mean shifts are +0.001 Reagan/+0.145 JFK; smoothing variants mean shifts −0.845/−0.498 (mild), −1.387/−0.887 (strong), so intended smoothing response remains relative to identity. By contrast CPP **increases** by ~4.96–7.00 dB with these “mumbles”; it would reward the flawed spectrum if “larger means clearer.” Custom CPP/Praat CPPS chunk correlation using voiced means is only .645 Reagan/.517 JFK, versus .960/.987 for all-frame means (`misc.json`); masks matter as much as estimator. No superiority claim for custom CPP is justified.

For R2, exclude D6 from totals; show its value and channel condition. D5 must carry a channel-confound flag on AGC/compressed/mismatched recordings; pure-gain normalization does not prove that D5 is valid across microphones. Require matched nuisance nulls and detector-level false regions/minute before claiming robustness. These are open build validations, not owner permission blockers.

## 5. Rates, pauses and aggregations

**VS:** speaking rate includes pauses; articulation rate excludes them. [De Jong & Bosker 2013](https://www.isca-archive.org/diss_2013/jong13_diss.pdf) documents thresholds spanning 100–1000 ms, the classic 250 ms convention, and limitations in equating every short gap with a stop closure. [Campione & Véronis 2002](https://www.isca-archive.org/speechprosody_2002/campione02_speechprosody.pdf), saved paper, describes brief <200 ms, medium 200–1000 ms and long >1000 ms, warning that thresholds bias cross-style comparisons. Choose **250 ms**, report raw gaps too, and distinguish the feature convention from the rubric report's 200 ms choice. Changing this value requires recomputing calibration and all numbers.

Pause threshold proposal: `q5=Q5(L)`, `q95=Q95(L)`, `θ=q5+clip(0.3(q95−q5),6,15) dB`; only inspect eligible aligned gaps and reject voiced intervals, as §1 specifies. Absolute `−40 dBFS` thresholds are gain dependent. The adaptive threshold remains noise-floor dependent and is **UV for manual pause accuracy**. Do not call low-energy unvoiced speech “silence” merely because a threshold accepts it.

**VR:** `v2/out/misc.json/pause` Reagan excerpt has 11 CTC-derived ≥250 ms gaps, 7.406 s, whereas the earlier extractor using `K-level < integrated LUFS−25` detects only 2 pauses/1.130 s; on full Reagan it detects only 1/0.28 s. Adaptive threshold finds 10 candidates/7.16 s, overlapping 8 of the 11 alignment gaps, with 2 unmatched candidates. This is agreement with biased CTC spans, **not precision/recall against truth**. An energy check is necessary but the fixed −25 LU threshold is rejected.

For text syllables, use `cmudict==1.1.3` during dataset preparation, count stress-marked vowel phones (`0`, `1`, `2`) in the first dictionary pronunciation, and save per-token counts with pronunciation choices in metadata. Preserve a reviewed exception map for names/numbers. OOV fallback exactly matches the probe: strip nonletters, count transitions into `[aeiouy]`, subtract one iff the word ends `e`, does not end `le`, and the count is >1, then clamp ≥1. Mark fallback counts. **VS:** [PyPI metadata](https://pypi.org/pypi/cmudict/json), retained `cmudict_pypi.json`, pure wheel 0.94 MB, Python ≥3.9,<4; no G2P model needed. First-pronunciation/OOV policy is a UV convention. The existing 101-syllable Reagan count is entirely heuristic and must not be presented as dictionary-verified.

Alignment-free nucleus cross-check: five-frame boxcar smoothing of L; peaks exceeding `Q99(L_smoothed)−25 dB` with topographic prominence ≥2 dB, retain only voiced peaks; count divided by elapsed speech seconds. **VS:** [De Jong & Wempe 2009](https://doi.org/10.3758/BRM.41.2.385), saved paper. **VR:** simplified probe yields 65 nuclei vs 101 heuristic syllables on Reagan (2.599 vs 4.237 syllables/s); it is not reliable enough here to replace transcript rate or “verify” absolute articulation rate.

Use median/P10/P90/range for pitch, mean and P90 for word energy, mean Q over a five-word window for clarity, and explicit event durations for pauses. Avoid per-word F0 SD/max and maxima over tiny voiced populations. Phrase stats are recomputed over the union of eligible frames, not an unweighted mean of word percentiles. Missing features stay missing and remove that span/dimension from scoring; record the denominator. Avoid smoothing a one-word flaw over five units without showing that context-window support.

**VR alignment sensitivity:** a +30 ms word-boundary translation on identical Reagan audio changes mean word energy by MAE 1.573 dB; +50 ms changes it by 2.333 dB; F0 median MAE .261/.350 st. JFK pseudo-unit energy MAE 2.057/3.161 dB. `v2/out/inv_*.json/boundary`. These are deliberate perturbation sensitivities, not measured aligner errors. The energy window itself spans ±12.5 ms; pitch windows span about `3/floor`, often 20–60 ms; boundary/display resolution must state both effects.

## 6. Energy-contour and stress-point accuracy: critic-focused validation

### 6.1 What existing evidence did and did not establish

**VS:** [Fry 1955](https://doi.org/10.1121/1.1908022) is the duration/intensity stress precedent (citation corroborated in saved Sluijter paper; full Fry text was not fetched); [Sluijter & van Heuven 1996](https://doi.org/10.1121/1.417955), `papers/sluijter_vanheuven_1996.txt`, distinguishes lexical stress/spectral balance from accent/F0 excursions; [Kochanski et al. 2005](https://pubmed.ncbi.nlm.nih.gov/16158659/), fetched abstract in `papers/pubmed_abstracts.txt`, found loudness/duration stronger prominence cues than F0 across their materials. Equal thirds in §1 are transparent conventions, not fitted or literature-derived optimal weights. The marker denotes **word-level acoustic prominence**, not lexical syllable stress, semantic correctness or human-rated emphasis.

**VS:** [Suni et al. 2017](https://research.aalto.fi/en/publications/hierarchical-representation-and-estimation-of-prosody-using-conti/) uses multiscale CWT and lines of maximum amplitude for prosodic structure, evaluated on Boston Radio News. [Talman et al. 2019](https://arxiv.org/abs/1908.02262), saved text, cites 85.3% accent-detection accuracy for that method. Our probe's **single Mexican-hat scale** on `z(pitch)+z(energy)+.5 duration` is only a simplified comparator: it does not implement Suni's multiscale method and cannot inherit 85.3%. Its correlation .711 with the earlier Reagan z-sum is agreement between two heuristics, not stress accuracy. Reject the earlier JFK prominence results: duration MAD≈0 in artificial equal-duration units produced scores/SD on the order of 10^11; adding 10^−12 is not an adequate tolerance floor.

### 6.2 Additional run and preserved artifacts

The same private CPU kernel was pushed once more, version 3, with `kaggle_src/validation_v3.py` embedded alongside the existing worker in the single `kaggle/probe.py`; v2 source is preserved as `kaggle_src/probe_v2.py`. No local DSP/model execution was performed in this finishing session. Protocol precedes results and is stored in the script/JSON. Output: `kaggle_out/v3/validation.json`, stress-marker plot, energy-ramp plot and an edited example WAV.

**VR:** `kaggle_out/v3/validation.json` has no section errors. Run environment: Python 3.12.13, numpy 2.0.2, scipy 1.16.3, soundfile 0.13.1, Parselmouth 0.4.7, pyworld-prebuilt 0.3.6.post1, torch/torchaudio 2.10.0+cpu, torchfcpe .0.4; CPU Intel Xeon 2.20 GHz, four available vCPUs, torch and numerical thread environment set to one. This is the Kaggle system stack, distinct from the newer pinned primitive-feature stack in §7. The v3 excerpt checks read the supplied mono 16 kHz float PCM directly without an additional DC-removal pass; they validate the specified extraction/intervention mechanisms on those inputs, not the entire proposed preprocessing/alignment pipeline.

**Stress-point intervention/control test (J-07, I-23):** on Reagan's 25 s excerpt, 70/74 words meet the five-voiced-frame validity gate. The predeclared three-component score identifies **12 candidates**: LADIES, GENTLEMEN, SPEAK, REPORT, STATE, EVENTS, EARLIER, CHANGE, TODAY, CORE, SHARE, THIS. It uses the §1 formulas with the probe's heuristic syllable counts and extended CTC spans, and includes zero-padded edge energy frames. The build's proposed dictionary counts, refined boundaries and edge exclusion require recalibration; this is not a test of those refinements. Estimated component scales are `(0.350988 ln-seconds/syllable, 3.000000 st, 3.765978 dB)`. Each candidate is edited in its own separate copy: flatten its Praat pitch tier toward the recording median and attenuate only that word by 9 dB with 10 ms edge ramps; keep duration unchanged and freeze baseline component centers/scales. Resynthesis is spliced into only the word, with original PCM outside it.

- **12/12 target markers disappear**; edited scores range −0.519…+0.257, all below .75. All edited targets still have ≥8 voiced frames, so disappearance is not a missing-pitch shortcut.
- **12/12 identity-resynthesis controls retain the target marker**. Each edited copy retains all **11 other baseline markers**. Outside the word, sample maximum absolute difference is **0** before subsequent analysis.
- Examples: STATE score 1.596→0.257 (identity 1.594), SHARE 1.379→0.125 (identity 1.372); true stored spans are in the JSON. Those spans derive from extended CTC boundaries and are not human-corrected stress times.
- Content/function plausibility check uses the explicit function-word list in the script, 32 content/38 function words with valid scores: mean score .497/−.262; **AUC .853618**. AUC is the fraction of content/function pairs with the content score higher, plus half-credit for ties; no POS model or human stress label was used. THIS is an identified function-word candidate, showing the detector does not forbid function-word prominence.

This establishes response to a **strong combined pitch/intensity intervention**, compared with an identity synthesis control, on one source speech. It does not establish weak-edit sensitivity, contribution of pitch alone, independent F0 measurement for this PSOLA test, or human stress precision/recall. Duration is one component but was not changed here. Frozen scales and nonzero floors fix the previous degeneracy; R2 tempo compensation and a different human speaker remain untested.

![Stress-point candidates by word](kaggle_out/v3/stress_markers.png)

**Energy-contour recovery (J-07, I-19):** inject `g_d(t)=−d(t−8)/10 dB` on `8≤t<18 s`, zero before/after, with a 20 ms linear release from −d to 0 at 18 s; `d∈{3,6,9}`. PCM multiplier is `10^(g_d/20)`. Compare measured `ΔL_k=L_k(edited)−L_k(original)` with injected gain at frame centers. Evaluate 8.05–17.95 s, excluding transition/window support; outside support is t<7.95 or t>18.07 s.

| Source | Injected depth dB | MAE dB | P95 absolute error dB | Measured-vs-injected regression slope |
|---|---:|---:|---:|---:|
| Reagan | 3 | .000263 | .000755 | .999993 |
| Reagan | 6 | .000527 | .001510 | .999993 |
| Reagan | 9 | .000790 | .002265 | .999993 |
| JFK | 3 | .000255 | .000812 | 1.000006 |
| JFK | 6 | .000510 | .001623 | 1.000006 |
| JFK | 9 | .000765 | .002435 | 1.000006 |

Outside-support raw energy differences are **0 dB**. Normalization in this check uses the **original voiced mask for both copies**; each copy's median level is separately recomputed. Subtracting the constant difference observed outside the edit gives the same normalized shape errors as above. Crucially the outside normalized contour has shifted: at 9 dB depth, +2.300 dB Reagan/+1.911 dB JFK. Whole-passage centering couples a local edit to other words. Display both raw/relative contours and use matched outside context when explaining magnitude; do not claim normalized Δ equals injected gain pointwise without accounting for that offset. Re-estimating voicing or automatic region boundaries adds errors not tested here. This is a numerical RMS recovery test with known timestamps, not energy-based detection F1 or perceptual vocal-effort truth.

![Injected versus measured energy-contour deltas](kaggle_out/v3/energy_contour_recovery.png)

**Independent F0-compression recovery (I-12):** analyze each original with WORLD Harvest (5 ms, 60–600 Hz), synthesize a matched identity and compressed copies with `f'(t)=median(f)(f(t)/median(f))^c`, c=.6/.3 on voiced frames. Re-extract using both adaptive Praat and **FCPE**, which was not used for injection (CPU local_argmax, threshold .006, 60–700 Hz, unvoiced interpolation disabled). Compute ratio of P90−P10 semitone ranges on common voiced frames of compressed/identity copies; also report slope `Σ(S0−median S0)(S1−median S1)/Σ(S0−median S0)^2`.

| Source | Nominal c | FCPE range ratio | FCPE centered-st slope | Praat range ratio | FCPE common voiced frames |
|---|---:|---:|---:|---:|---:|
| Reagan | .6 | .6260 | .6004 | .6075 | 1695 |
| Reagan | .3 | .3090 | .3009 | .3072 | 1692 |
| JFK | .6 | .5890 | .6157 | .5818 | 1845 |
| JFK | .3 | .3040 | .3042 | .2874 | 1843 |

This checks nominal-versus-realized acoustic variation with a different tracker and matched resynthesis. Both robust range and centered regression recover compression closely here; SD ratios in JSON depart more. It does not establish independent physiological truth or accurate stress marking under every vocoder. WORLD copies can have more voiced frames than original Praat, so use the reported denominators rather than assuming original voicing. The retained kernel log includes a nonfatal FCPE input-range warning (minimum −1.0577): floating-point WORLD copies were not clipped to ±1. Outputs completed, but this is not a clipping/PCM-upload robustness test.

**Chosen tracker on FDA clean/noisy/vocoded material (I-12):** version 3 tests the **actual recommended two-pass + median5** on all 100 FDA utterances, 331.6 s; v2's narrower accuracy table above omits that smoothing.

| Condition | GPE20 % | VDE % | FFE % | Octave % | Male/female FFE % |
|---|---:|---:|---:|---:|---:|
| Clean original | .505 | 4.290 | 4.465 | .052 | 5.459 / 3.677 |
| White noise SNR 10 dB | .266 | 5.177 | 5.265 | .018 | 6.411 / 4.356 |
| Matched WORLD identity | .808 | 6.335 | 6.621 | .077 | 8.144 / 5.412 |

Clean/noisy rows use independent laryngograph truth. WORLD identity is evaluated against the **original** laryngograph contour as the preservation target: it measures combined synthesis plus tracking error, not tracker-only accuracy on newly measured vocal folds. The identity resynthesis increases FFE appreciably and must be included in synthetic nulls. FDA still contains only two speakers and clean read texts; the real archival telephone-band failure in §2 remains decisive.

### 6.3 Critic resolution and remaining limits

| Item | What this research settles | What remains unverified |
|---|---|---|
| **I-12 F0 measurement** | Laryngograph GPE/VDE/octave/FFE; noisy, band-limited and vocoded checks; independent estimator for pitch-compression recovery; robust summaries/missingness rules; rejection of automatic octave killing. | FDA has only two speakers; vocoded original `.fx` is an identity target, not new physiological truth; no archival/TTS human F0 labels; automatic outlier/abstention calibration. |
| **I-19 clarity/energy across channels** | Measured codec, noise, bandwidth, reverb, gain and compression rows; one selected clarity proxy; evidence requires D6 exclusion on R2 and explicit D5 channel caveats. | Human clarity/effort validity, end-to-end false regions/minute and browser AGC/noise-suppression tests. R1 feature tests cannot establish R2 construct validity. |
| **J-07 formulas/jobs/stress/energy** | Exact consumer table; visible stress candidates; intervention/control marker test; content/function sanity check; injected-vs-measured energy plot; raw/normalized demo measurements. | Human-stress precision/recall and manually timed peak localization; arbitrary marker threshold/weights are not validated human annotations. |
| **I-23 prominence, I-24 unused features** | New score with nonzero floors; content/function proxy check; no maxima/SD in recommended scoring; every retained feature has a consumer, redundant descriptors removed. | Content/function AUC is linguistic plausibility, not human stress truth; not all content words are stressed and function words can be accented. |

## 7. Verified by running: timing, normalization, determinism and pins

### 7.1 Where and how

Existing commands: `kaggle kernels push -p kaggle --timeout 1800`, `kaggle kernels status electroknight/cvoice-probe-features`, `kaggle kernels output electroknight/cvoice-probe-features -p kaggle_out/vN`. v1/v2 metadata: `is_private=true`, `enable_gpu=false`, `enable_tpu=false`, `enable_internet=true`, dataset `electroknight/cvoice-probe-audio`. Final research preserved the previous runs and downloaded complete v2 outputs, then submitted the focused v3 validation. All computational results below are from prior local probe or private Kaggle CPU sessions, cited individually.

| Full extraction (includes **unselected** CPP/HNR/formants/modulation) | Duration s | CPU wall s | seconds/audio-second | Machine |
|---|---:|---:|---:|---|
| Reagan full, v1 | 255.791 | 7.632 | .02983 | 4 vCPU AMD EPYC 7B12 |
| JFK full, v1 | 840.228 | 26.257 | .03125 | same |
| Reagan full, v2, thread env=1 | 255.791 | 11.707 | .04577 | 4 vCPU Intel Xeon 2.20 GHz |
| JFK full, v2, thread env=1 | 840.228 | 39.977 | .04758 | same |

**VR:** `v1/out/timing_v312.json`, `v2/out/timing_v312_threads1.json`; includes decode/resample and pseudo-word aggregation, **excludes forced alignment**, installation/model loading and optional jitter/shimmer. v2 process max RSS 1176 MiB. Do not attribute machine differences to thread count alone. For JFK v2, F0 .00569 s/s; spectrum+MFCC .00085; energy .00113; spectral descriptors .00130; word aggregation .00506. Dropping CPP/formants/HNR should reduce costs, but the exact final reduced runtime was not separately benchmarked (UV). A 30 s projection from the measured full pipeline is ~1.4 s, not a measured upload latency.

### 7.2 Speaker-normalization demonstration

**VR:** `v2/out/inv_reagan.json`, `inv_jfk.json`, using PSOLA +5 st and gain −9 dB; compare independently re-extracted features. The transformation also changes waveform energy/voicing slightly, so it is not a pure biological speaker change.

| Recording | Measured global median pitch shift st | Raw word RMS mean shift dB | Centered word F0 MAE st | Centered word RMS MAE dB | Integrated-relative K-energy MAE LU (unselected alternative) |
|---|---:|---:|---:|---:|---:|
| Reagan, 74 actual words | +5.109 | −8.957 | .285 | .435 | .250 |
| JFK, 88 pseudo-units | +5.026 | −9.718 | .172 | .765 | .578 |

Pure −9 dB gain gives −9.000 raw word dB and <10^−5 normalized dB MAE on both. For Reagan identity PSOLA alone centered F0 MAE .250 st, energy .206 dB; much of the shifted-copy residual is resynthesis, not centering failure. WORLD pitch+formant×1.15+gain transform centered pitch MAE .404/.273 st Reagan/JFK, energy .899/1.097 dB. Speaker-normalized does not mean invariant to voice conversion or new humans. Raw c1…c12 MFCC distance under WORLD speaker transform .538/.729, CMN .382/.434, CMVN .629/.628, in the probe's defined normalized-distance metric; CMVN does not remove speaker identity.

### 7.3 Repeatability and cross-environment precision

**VR:** `v1/out/det_summary.json`: 93 retained array hashes per configuration; repeated process and Python 3.12/3.13/3.14 pinned environments have 0 exact hash mismatches against v312 run1. System preinstalled stack and one-thread variant each have 12 exact mismatches, **0 at six decimal places**. Same-process repeats are identical. `v2/out/det_summary.json`: BLAS-free sums/closed-form fits change 13 hashes vs standard path but 0 rounded-six differences. Direct standard-library comparison of `det_v312_blasfree.json` with `det_v312_blasfree_threads1.json` finds identical frame hashes for all three recordings and identical Reagan word hashes; do not infer equality merely from the shared reference-mismatch list.

Praat legacy AC hash matches earlier local output for Reagan/JFK; CC and DIO have tiny cross-build differences on Reagan; Harvest/pYIN legacy hashes match. `out_f0_run1.md` consensus is an inter-tracker reference only, never accuracy truth. Preserve float64 internal values, round output measurements to 6 decimals with explicit JSON nulls for missing, pin threads/BLAS and decoder, and compare final scores/timestamps after deployment. Equality of rounded primitive arrays does not prove equal thresholds/regions at decision boundaries. No Docker-versus-Kaggle end-to-end reproduction was performed here.

### 7.4 Exact pins and wheel support

Recommended tested feature environment: **Python 3.12.13**, `numpy==2.5.3`, `scipy==1.18.1`, `soundfile==0.14.0` (observed libsndfile 1.2.2), `soxr==1.1.0`, `praat-parselmouth==0.4.7`; optional loudness QA `pyloudnorm==0.2.0`; dataset syllables `cmudict==1.1.3`. Core does not need torch/librosa/numba/openSMILE. Reuse project's alignment torch pin separately; installing the newest torch is not necessary for these features.

Offline/synthesis/research extras verified: `pyworld-prebuilt==0.3.6.post1` (import `pyworld`, do not install competing `pyworld` distribution), `librosa==1.0.0`, `numba==0.68.0`, `llvmlite==0.50.0`, `scikit-learn==1.9.1`; independent CPU FCPE `torchfcpe==0.0.4` with Kaggle system `torch==2.10.0+cpu`, `torchaudio==2.10.0+cpu`, librosa 0.11.0. These are distinct environments, not one tested lockfile. Full freezes: `v1/out/freeze_312.txt`, `freeze_313.txt`, `freeze_314.txt`, v2 equivalents. Set `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=NUMBA_NUM_THREADS=1` before imports for primitive-feature reproducibility.

**VS PyPI release metadata**, captured earlier `pypi_wheels_py312_313_314.out` and `pypi_wheels.out`; **VR** actual v1 Kaggle isolated installs and extraction at Python 3.12.13, 3.13.15, 3.14.7. Wheel presence is not whole dependency-stack compatibility.

| Distribution/pin | Linux x86_64 3.12 | 3.13 | 3.14 | Notes |
|---|---|---|---|---|
| numpy 2.5.3 / scipy 1.18.1 | yes | yes | yes | cp-specific wheels; actually executed all three. |
| praat-parselmouth 0.4.7 | yes | yes | yes | ~10.7 MB; no Linux aarch64 wheels in snapshot; GPLv3. |
| soundfile 0.14.0 | pure wheel | pure wheel | pure wheel | Requires native libsndfile; actual Kaggle library 1.2.2. |
| soxr 1.1.0 | cp312 abi3 | compatible abi3 | compatible abi3 | manylinux x86_64 floor 2.27/2.28; actual install success. |
| pyloudnorm 0.2.0 | pure | pure | pure | scipy/numpy dependencies; optional QA. |
| cmudict 1.1.3 | pure | pure | pure | metadata verified this finishing session; not included in acoustic install probe. |
| pyworld-prebuilt 0.3.6.post1 | yes | yes | yes | research synthesis only; upstream pyworld 0.3.6 lacked these Linux wheels. |
| librosa 1.0.0 / numba .68 / llvmlite .50 | yes | yes | yes | librosa pure, numba/LLVM binary; research only, actual runs. |
| opensmile 2.6.0 | py3 platform wheel | same | same | Separate audEERING research license; dependency stack matters. |
| torchfcpe .0.4 / torchcrepe .0.24 / penn 1.0.0 | pure distribution | pure | pure | Does **not** establish torch/torbi availability; PENN import failed previously. |
| pysptk 1.0.1 | no | no | no | source build and old setuptools requirement; not recommended runtime. |

**VS licenses:** openSMILE/openSMILE Python fetched license `src_refs/opensmile_LICENSE`, `opensmile_python_LICENSE`; [audEERING license](https://github.com/audeering/opensmile/blob/master/LICENSE) permits noncommercial research/public demonstrations with conditions, commercial research only in the specified evaluative/publication context, and requires extra commercial rights for direct **or indirect use of models/features in products**. “Free Python wrapper” does not remove the core restriction. Keep it as an offline cross-check. Its proprietary research license is not GPL/MIT/Apache. For Parselmouth GPLv3 distribution, preserve notices/source obligations appropriate to the eventual distribution; this report does not establish the whole project's license compliance. `src_refs/wpt_LICENSE` is a failed 404 response, **not license evidence**; do not infer a wavelet-toolkit license from it.

## 8. Disagreements with DESIGN_v0 and risks

1. Replace raw per-word F0 maximum/SD with quantiles and coverage gates; do not treat tracker consensus as truth or smooth gaps into voiced evidence.
2. Separate robust **centering** from per-recording variance normalization. Preserve global range/tempo/dynamics so whole-passage flaws remain measurable. Add real denominator floors; epsilon alone caused a large prominence failure.
3. Remove unused descriptors and the three-way “clarity” blend in `../rubric_explain/REPORT.md`: phonetic confidence, spectrum dynamics and high-band energy respond to different confounds. One explicit Q proxy is better supported, restricted to R1.
4. Never infer breath support/vocal effort from synthetic gain attenuation alone. Alpha is gain invariant; a DSP fade manipulates recording amplitude, not physiology.
5. Replace constant −25 LU acoustic activity/pause threshold; it failed on Reagan. Adaptive/inter-word pause checks still need labeled boundaries and must not be reported as validated precision.
6. Visible stress markers and a named energy-contour recovery plot are required for J-07; a list of F0/RMS/MFCC features is insufficient. Synthetic recovery is mechanism verification, not perceptual validation.
7. Channel robustness is dimension-specific; conservative abstention/display-only handling is needed. FDA is small and read speech; the two archival clips are both male, and JFK pseudo-word findings are not word-level rhetoric findings.
8. Deviation indices cannot determine good content, appropriate rhetorical style, or whether alternative stress patterns are legitimate. Scope is English same-transcript/reference comparison; dialects, accents, disfluencies and children require additional validation.

**Owner-only open decision:** whether to annotate stressed words and approximately 150 word boundaries in a few passages by ear/Praat (labeling only, no self-recording). If not, the deliverable must retain “acoustic stress candidates” and synthetic recovery wording; human stress/timing accuracy remains UV. Engineering calibration on the fixed automated dataset is ordinary remaining build work, not an owner preference question.

## 9. Source trail

Primary material has been retained in `papers/`, `src_refs/`, `fda/`, the PyPI snapshot outputs and run logs. Failed/404 fetches are not evidence. Formula recommendations above are fully specified even when their perceptual validity is UV.

- VS [Boersma 1993](https://www.fon.hum.uva.nl/paul/papers/Proceedings_1993.pdf), `papers/boersma_1993.txt`; [Praat raw AC settings/algorithm](https://www.fon.hum.uva.nl/praat/manual/pitch_analysis_by_raw_autocorrelation.html), refreshed this session.
- VS [Hirst 2011](https://econtents.sbu.unicamp.br/inpec/index.php/joss/article/view/15011), `papers/hirst_2011_joss.txt`; [Nolan 2003](https://www.internationalphoneticassociation.org/icphs-proceedings/ICPhS2003/papers/p15_0771.pdf), `papers/nolan_2003_icphs.txt`; [Arantes/Eriksson](https://www.isca-archive.org/speechprosody_2014/arantes14_speechprosody.pdf), saved paper.
- VS [Strömbergsson 2016](https://www.isca-archive.org/interspeech_2016/strombergsson16_interspeech.pdf), [Jouvet/Laprie 2017](https://www.eurasip.org/Proceedings/Eusipco/Eusipco2017/papers/1570342455.pdf), [PENN](https://arxiv.org/abs/2301.12258); previously fetched PDFs converted to retained text this session.
- VS [Sluijter/van Heuven 1996](https://doi.org/10.1121/1.417955), saved paper; Fry 1955 citation in that paper, full text unavailable; [Kochanski 2005](https://pubmed.ncbi.nlm.nih.gov/16158659/) and voice-quality/clear-speech studies, fetched abstracts in `papers/pubmed_abstracts*.txt`.
- VS [Suni 2017 primary author record](https://research.aalto.fi/en/publications/hierarchical-representation-and-estimation-of-prosody-using-conti/), refreshed; [Talman 2019](https://arxiv.org/abs/1908.02262), retained text; toolkit configuration/code saved in `src_refs/wpt_default.yaml`, `wpt_prosody_labeller.py`; toolkit license fetch failed.
- VS [ITU BS.1770-5](https://www.itu.int/rec/R-REC-BS.1770-5-202311-I/en), [EBU LRA](https://tech.ebu.ch/docs/tech/tech3342.pdf), retained texts; implementation sources `src_refs/libebur128_ebur128.c`, `pyloudnorm_meter.py`, `pyloudnorm_iirfilter.py`.
- VS [De Jong/Wempe 2009](https://doi.org/10.3758/BRM.41.2.385), [De Jong/Bosker 2013](https://www.isca-archive.org/diss_2013/jong13_diss.pdf), [Campione/Véronis 2002](https://www.isca-archive.org/speechprosody_2002/campione02_speechprosody.pdf), retained papers.
- VS [PyPI](https://pypi.org/) package JSON snapshots, versions/wheel filenames retained in `pypi_wheels_py312_313_314.out`, `cmudict_pypi.json`; [openSMILE license](https://github.com/audeering/opensmile/blob/master/LICENSE) refreshed and retained.
