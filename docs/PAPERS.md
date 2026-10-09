# Papers used and what was taken from each

One row per cited source. The numbers are the reference numbers of `docs/technical.md`. Each row gives the read status, what was taken from the source and the part of the system that uses it. The chain table links each flaw to its detection method and to the module that implements it. Measured results are in `docs/technical.md` and `docs/evidence_final_782d7df7/`.

**Read status.** *full* = the full text was read; *full-F* = full text read through a fetch tool that returns a model-written extraction (numbers marked "to re-check"; the citation check confirmed those used here); *abstract* = only the abstract was read; *secondary* = read through the named source; *metadata* = only the bibliographic record. A claim from an abstract or a secondary source is weaker support.

**Used in:** D1 pace, D2 pauses, D3 pitch range, D4 emphasis, D5 volume, D6 clarity proxy, D7 word time and disfluency, D8 sentence ending, D9 speech tempo and natural rushing, FAM hesitation and word-by-word families, AL alignment, REF reference-relative comparison, SYN controlled edits, EVAL evaluation, EXP explanations.

## Chain from flaw to method to system part

| Dim | Flaw named by | Cause → pattern used | Method source | Module.function | R1 (same recording, synthetic edits; L2+L3 detected, train / val / test) | R2 (different speaker) |
|---|---|---|---|---|---|---|
| D1 Pace | [1–4, 6] | fast or slow reading → local tempo change [15, 16] | speech time without pauses [14]; same-text comparison [17, 26] | `compare.d1_pace` | RUSH 10/10, 4/4, 4/4; DRAG 10/10, 4/4, 4/4 | scored; check readers L3: RUSH 1/18, DRAG 6/17 |
| D2 Pauses | [4, 5] | planning, retrieval, fast reading → inserted or removed silence [15, 37, 38] | acoustic silence ≥ 0.20 s [30–32] | `compare.d2_pauses` | PAUSE_DROPPED 10/10, 4/4, 4/4; PAUSE_INTRUSIVE 10/10, 4/4, 4/4 | scored; L3: dropped 4/17, intrusive 14/18 |
| D3 Pitch range | [1–4, 6] | low arousal, second-language reading → compressed span [49, 54] | percentile range in semitones [41, 43] | `compare.d3_pitch` | MONOTONE 9/10, 4/4, 2/4 | scored; L3: MONOTONE 17/18 |
| D4 Emphasis | [4, 7] | no focus marking → flat prominence [56, 59] | equal-weight prominence z-sum [57, 58] | `compare.d4_emphasis` | DEEMPHASIS 7/10, 4/4, 3/4 | not scored |
| D5 Volume | [1, 2, 4, 8] | low effort, recording chain, trailing off → level drop [67–71] | level relative to own median [66] | `compare.d5_volume` | FADE 10/10, 2/4, 4/4 | scored; L3: FADE 13/18 |
| D6 Clarity proxy | [1–4] | hypo-articulation → bundle of changes [73–75] | none validates this proxy | `compare.d6_clarity` | MUMBLE 10/10, 4/4, 4/4 | not scored |
| D7 Word time | [1, 3] | stuttering, planning → repetition, prolongation, block, filler [78–82] | duration ratio, decode insertions, stability run [83–86] | `compare.d7_word_time`, `patterns.word_time` | listed, not scored | listed, not scored |
| D8 Sentence ending | [4, 119] | uptalk, unskilled reading → final rise, weak fall [95, 96] | final pitch change [95, 98] | `compare.d8_ending` | listed, not scored | listed, not scored |
| D9 Speech tempo | [4] | natural rushing → faster words, fewer pauses [15, 16] | articulation-rate decomposition [19, 20] | `compare.d9_speech_tempo`, `patterns.natural_rush` | NATURAL_RUSH 2/10, 1/4, 1/4 | listed, not scored |

## Where the system departs from the sources

1. The R2 thresholds (pace ×2.19 / ×0.45, dropped pause 1.50 s, single reference) are set by reader-to-reader variation and are far above the perceptual values in [13, 40, 66] (`docs/technical.md` limit 11).
2. The D2+ threshold in R1 (0.3225 s) is above the silences that listeners judged disfluent in 72 % of samples (212 ms) [33], and above every word-by-word recipe silence.
3. The pitch measure is a percentile-range ratio over five words; the validated windows are 10 s and longer [41–43].
4. Emphasis uses equal weights for three cues; spectral balance is not used. For read English this is defensible by [57, 58, 62, 63].
5. Clarity is one spectral-change proxy; the literature treats clear speech as a bundle [73–75], and the published articulation measure [76, 77] is not scored.
6. The aligner is the wav2vec 2.0 base model, with a published word-boundary error of 48–89 ms [100], not the more accurate Montreal Forced Aligner [101, 102].
7. One reference rendition is the comparison point (five in the median mode), against the 10–20 readers that [53] found necessary.
8. The natural-rushing evidence measured speech_time_ratio; the product measures D9.
9. Disfluency (D7) and sentence endings (D8) are measured and listed; neither is scored, and only the filled-pause label passed a real-data test.
10. An overall score is shown although [113] advises caution with grades; the per-finding penalty is shown beside it.

## 1. What counts as a delivery flaw (rubrics and perception)

| # | Source | Read | What was taken | Used in |
|---|---|---|---|---|
| 1 | Schreiber, Paul & Shibley 2012, Public Speaking Competence Rubric | secondary (reproduced in [2]) | Lowest levels: "poor pacing", "speaks in monotone", "a voice too soft", "speaks inaudibly", "articulation too indistinct", "distracts listeners with fillers" | D1, D3, D5, D6, D7 |
| 2 | Joe, Kitchen, Chen & Feng 2015, ETS RR-15-36 | full | Rubric text of [1]; two expert raters agreed exactly on "vocal expression" for 30 % of presentations | all, REF |
| 3 | Morreale et al. 2007, Competent Speaker form | full | "vocal variety in rate, pitch, and intensity"; "properly formed sounds"; "nonfluencies and disfluencies interfere with the message"; levels separated by "occasional" against "frequent" | D1, D3, D6, D7 |
| 4 | Judging instruments: NSDA, Poetry Out Loud, Toastmasters 1172, UIL | full | Quotations shown beside each flag ("too slow or hurried pace", "pauses come in suitable places", "Is the volume appropriate?", "Was enunciation clear?", pitch change "for emphasis", "singsong", "monotone"); no numeric threshold; NSDA Declamation "is not designed for students to mimic the original author" | all, REF, EXP |
| 5 | Chen et al. 2016, automated public-speaking assessment | full | Mean silence inside clauses vs holistic score, \|r\| = 0.479 (n = 28); inter-rater ICC 0.385 on 56 videos | D2, REF |
| 6 | Strangert & Gustafson 2008 | full | "monotonous" r = −.91 and pitch range r = .61 with good-speaker ratings; resynthesis: pitch dynamics > fluency > rate; +5 % rate with shorter hesitation pauses raised rankings | D1, D3 |
| 7 | Hahn 2004 | abstract | Correct primary stress: more content recalled, speaker rated higher | D4 |
| 8 | Van Zant & Berger 2020 | abstract | Persuaders "speak louder and vary their volume", signalling confidence | D5 |
| 9 | Biadsy et al. 2008 | full | Intensity mean and SD vs charisma r = .14 to .35; effects differ by rater language | D5, REF |
| 10 | Niebuhr, Tegtmeier & Schweisfurth 2019 | full | Effects reverse at the extremes ("too high-pitched or too fast"): the literature justifies dimensions, not ideal values | REF |
| 11 | Strangert 2005 | full | Silence-to-speech ratio 9 % (professional) against 28 % (non-professional reading), Swedish | D2 |
| 12 | Duez 1982 | abstract | Prepared political speeches: 50 % more silent-pause time than interviews, mostly at clause or phrase boundaries | D2 |
| 119 | Vaughan-Johnston et al. 2024 | full | Falling against rising intonation on the last word (±35 Hz) changed confidence ratings (5.55 vs 4.82); persuasion benefit only for strong arguments | D8 |

## 2. Pace, tempo and natural rushing

| # | Source | Read | What was taken | Used in |
|---|---|---|---|---|
| 13 | Quené 2007, tempo JND | full (author preprint) | JND for speech tempo about 5 %; the D1 floor ln 1.10 lies above it | D1 |
| 14 | de Jong & Wempe 2009 | full | Speaking rate includes pauses, articulation rate excludes them: D1 removes pauses from speech time | D1 |
| 15 | Trouvain & Grice 1999 | full | Fast reading: articulation rate +13 % and +18 % (two of three readers), speaking rate up to +28 %, pauses removed or shortened. Source of the natural-rush recipe rates ×1.13 / ×1.15 / ×1.18 | D1, D2, D9 |
| 16 | Janse 2004 | full | Natural fast speech is not uniform compression; unstressed syllables shrink more; listeners preferred linear compression | D1, D9 |
| 17 | Crystal & House 1990 | abstract | Durations of comparable runs of different talkers on one text are highly correlated: supports run-by-run comparison on a fixed text | D1, REF |
| 18 | Jacewicz et al. 2009 | full-F (confirmed) | Read sentences 3.40 syllables/s, SD 0.42 across speakers: habitual rate differs between speakers | D1 |
| 19 | Cucchiarini, Strik & Boves 2000 | abstract | Read speech: rate of speech correlated 0.90–0.93 with expert fluency ratings | D9 |
| 20 | Suzuki, Kormos & Uchihara 2021 | full (accepted manuscript) | Meta-analysis of 22 second-language studies: articulation rate r = .62, speech rate .76, pause frequency −.59 with rated fluency | D9 |
| 21 | Hofmann et al. 1997 | abstract | Speakers with social phobia paused more often and longer in public speaking | D1, D7 |
| 22 | Teferra et al. 2022 | full | Source through which Laukka et al. 2008 is read: share of silence r = .36 with state anxiety | D1 |
| 23 | Schewski et al. 2025 | full | "No consistent acoustic patterns were identified for fear or anxiety"; mean F0 raised under stress in 15 of 19 studies | D1, D3 |
| 24 | Moers, Meyer & Janse 2017 | abstract | Longer reading durations for low-probability words: the processing-difficulty pattern behind HESITATION | D1, FAM |
| 25 | de Jong 2016 | abstract | Pauses more likely before low-frequency words | D1, FAM |
| 26 | Duong, Mostow & Sitaram 2011 | full | Word latency and duration contours correlated with a fluent reading of the same text; "F0 match" was among the best indicators of expressive reading (children). Not built | D1, D3, REF |
| 27 | Daane et al. 2005, NAEP oral reading study | full | "Reads primarily word-by-word" (level 1): the WORD_BY_WORD pattern | FAM |
| 28 | McIntosh et al. 2026 | full (preprint) | Tempo irregularity along an alignment with a reference: r = .37 alone, human agreement .49. Source of the uneven-tempo measure, which failed its lab gate | FAM |
| 29 | Camara et al. 2026 | full (preprint) | Utterance-final words 80 ms longer in matched within-speaker comparisons: an effect at the size of the aligner's boundary error | AL |

## 3. Pauses

| # | Source | Read | What was taken | Used in |
|---|---|---|---|---|
| 30 | Campione & Véronis 2002 | full | Pause classes brief < 200 ms, medium, long > 1000 ms "only in spontaneous speech"; English read speech median 493 ms, modes 126 and 512 ms (basis of the 0.5 s rule for dropped pauses) | D2 |
| 31 | de Jong & Bosker 2013 | full | Published pause thresholds run from 100 to 1000 ms; 250 ms is the classic convention (the feature research recommended 250 ms; the build uses 0.20 s) | D2 |
| 32 | Hallur et al. 2026 | full (preprint) | 0.2 s as a practical pause threshold; reference-based evaluation with speech rate, articulation rate and pause ratio; limit: does "not yet map deviations to perceptual thresholds" | D2, REF |
| 33 | Lövgren & van Doorn 2005 | full | Silences of 57 / 117 / 212 / 403 ms judged disfluent in 12.5 / 34.4 / 71.9 / 93.8 % of samples | D2, FAM |
| 34 | Wang Y.-T. et al. 2010, breath groups | full | Reading: inter-breath pause 0.64 s (0.25–1.8 s); 1.8 % of breaths at ungrammatical places; pauses before noun, verb or adverbial phrases are "appropriate" | D2 |
| 35 | Wang Y.-T. et al. 2010, inspiratory loci | full-F (confirmed, one figure corrected) | A 250 ms pause as breath candidate; 13.6 % of such pauses are not breaths | D2 |
| 36 | Miller & Schwanenflugel 2006 | full-F (confirmed) | Skilled adult readers: sentence-end pauses mean 446 ms, comma pauses mean 59 ms (0–454 ms): no D2+ flag at punctuation | D2 |
| 37 | Kahng 2018 | abstract | Within-clause silent pause rate had the strongest correlation with second-language fluency ratings | D2 |
| 38 | Tavakoli 2011 | abstract | Learners pause in the middle of clauses rather than at the end | D2 |
| 39 | Schwanenflugel et al. 2004 | full-F (confirmed) | Within-sentence pauses 688 ms (slowest readers) against 313–365 ms (children) | D2 |

## 4. Pitch range

| # | Source | Read | What was taken | Used in |
|---|---|---|---|---|
| 40 | 't Hart 1981 | abstract | Pitch-distance JND 1.5–2 st; only differences above 3 st matter in communication: basis of the 1 st regularisation of range ratios | D3 |
| 41 | Hincks & Edlund 2009 | full | Semitones relative to the speaker as perceptual normalisation; SD of semitones over a moving 10 s window | D3 |
| 42 | Hincks 2005 | full | PVQ below .15 over 10 s "generally rated as on the monotone side"; does not transfer to read text | D3 |
| 43 | Niebuhr & Skarnitzl 2019 | full | P90 − P10 range r = .52 with charisma, SD .35, max − min .04 (40–98 s excerpts): choice of the percentile range | D3 |
| 44 | Boersma 1993 | full | The Praat autocorrelation pitch tracker, used through parselmouth | D3, D4, D8 |
| 45 | Hirst 2011 | full | Pitch floor and ceiling from the recording's own quartiles (two-pass tracking) | D3 |
| 46 | Arantes & Eriksson 2014 | full | Long-term F0 averages settle after about 10 s: centring on the whole passage | D3 |
| 47 | Strömbergsson 2016 | full | Praat F0 frame error 7.05 % default, 6.20 % sex-adapted range | D3 |
| 48 | Jouvet & Laprie 2017 | full | Praat frame error 5.05 % clean; another tracker better on real noisy speech | D3 |
| 49 | Zimmerer et al. 2014 | full | Second-language reading compresses the whole-passage span (SD/mean 0.118–0.133 against 0.134–0.146) | D3 |
| 50 | Patterson & Ladd 1999 | full | Percentile spans were weaker than landmark spans against listener judgements | D3 |
| 51 | Wehrle et al. 2018 | full | Long-term measures cannot tell a slow rise from a repeated contour (sing-song); reason REPEATED_CONTOUR has no detector | D3, FAM |
| 52 | Portnova et al. 2025 | full | Tracking errors inflate SD; IQR measures are more robust | D3 |
| 53 | Wang, Evanini & Yoon 2015 | full | Pitch match with native readings: r .34–.39 with human scores; unstable with fewer than 10–20 reference readers | D3, REF |
| 54 | Low, Bentley & Ghosh 2020 | full | Lower F0 and narrower F0 range in depression (low-arousal pattern) | D3 |
| 55 | Traunmüller & Eriksson 1995 | abstract | F0 intervals judged equivalent when equal in semitones | D3 |

## 5. Emphasis

| # | Source | Read | What was taken | Used in |
|---|---|---|---|---|
| 56 | Xu & Xu 2005 | full | Focus: expanded range on the focused syllable, suppressed range after it | D4 |
| 57 | Suni, Aalto & Vainio 2015 | full (preprint) | Equal-weight z-sum of F0, energy and duration: 79.2 % on read news; wavelet version 84.6 % | D4 |
| 58 | Talman et al. 2019 | full | Tuned weights gain about 0.7 points over equal weights | D4 |
| 59 | Kallio, Suni & Šimko 2022 | full | Less proficient readers: "prominence variation pattern is more flat"; prominence similarity explains 4.19–5.60 % of rating variance | D4 |
| 60 | Sluijter & van Heuven 1996 | full | Spectral balance carries lexical stress; F0 excursions carry accent (spectral balance not used) | D4 |
| 61 | Kochanski et al. 2005 | abstract | Loudness and duration stronger than F0 as prominence cues in their materials | D4 |
| 62 | Baumann & Winter 2018 | full (accepted manuscript) | German read sentences: amplitude, F0 and spectral tilt among the important continuous cues; part of the cue-weight comparison | D4 |
| 63 | Kakouros, Räsänen & Alku 2018 | full (author manuscript) | Duration best, tilt systematic but weaker; supports equal weights for read speech | D4 |
| 64 | Nenkova et al. 2007 | full | Content words far more likely accented than function words; text prior (not built; D4+ failed its lab gate) | D4, FAM |
| 65 | Mo, Cole & Lee 2008 | full | Listener agreement on prominence: Fleiss kappa .373–.421 | D4 |

## 6. Volume

| # | Source | Read | What was taken | Used in |
|---|---|---|---|---|
| 66 | Caswell-Midwinter & Whitmer 2019 | full | Level JND 1.5 dB, 3 dB noticeable (hearing-impaired listeners, speech-shaped noise): above them lies the D5 floor of 2 dB | D5 |
| 67 | Liénard & Di Benedetto 1999 | abstract | Effort raises high-frequency harmonics more than level ("a change in spectral tilt"); F0 and F1 rise with effort | D5, FAM |
| 68 | Sundberg & Nordenberg 2006 | abstract | Alpha ratio ranges 19.0 / 11.7 dB over about 28 dB of level (women / men): basis of the LOW_EFFORT tilt recipe (0.55 dB per dB) | D5, FAM |
| 69 | Eriksson & Traunmüller 1999 | full | Listeners tell increased effort from decreased distance on phonated vowels: effort and gain are separable | D5 |
| 70 | Pierrehumbert 1979 | abstract | Amplitude downdrift accompanies F0 declination (trailing-off pattern) | D5, FAM |
| 71 | Ní Chasaide, Yanushevskaya & Gobl 2015 | full | Source strength declines −7.3 dB/s in short declaratives with laxer phonation | D5, FAM |
| 72 | Zhang & Hansen 2007 | full | The absolute SPL of a recording may be unknown because of recording levels and AGC | D5 |

## 7. Clarity

| # | Source | Read | What was taken | Used in |
|---|---|---|---|---|
| 73 | Picheny, Durlach & Braida 1986 | abstract | Conversational speech: reduced vowels, unreleased final stops; clear speech is a bundle of properties | D6 |
| 74 | Krause & Braida 2004 | abstract | Clear speech at normal rate: more 1–3 kHz energy, deeper low-frequency envelope modulation | D6 |
| 75 | Smiljanić & Bradlow 2009 | full | Full-text review of the clear-speech bundle | D6 |
| 76 | Cao et al. 2024 | full | The aligned CTC posterior is GOP-CTC-align, a published pronunciation measure (not scored here) | D6 |
| 77 | Halpern et al. 2026, PathBench | full (preprint) | Articulatory precision (average aligned posterior) r = 0.71 with rated intelligibility over six pathological datasets | D6 |

## 8. Disfluency

| # | Source | Read | What was taken | Used in |
|---|---|---|---|---|
| 78 | Lickley 2017 | full | Stuttering forms (rapid onset repeats, prolongation, block) and positions; typical repeats 96 % on function words; events about 1 s | D7 |
| 79 | Shriberg 1999 | full | First token of a repeat lengthened; filled pause schwa-like, long, low and falling F0; under 1 % of words disfluent in constrained speech | D7 |
| 80 | Ritto et al. 2016 | full | Fluent adults reading aloud: 0.21 % stuttered syllables (n = 17): the base rate | D7 |
| 81 | Clark & Fox Tree 2002 | full | "Um" followed by delays more often than "uh" (61 vs 29 %) | D7 |
| 82 | Christenfeld & Creager 1996 | abstract | Fillers and anxiety not linked "in any simple way"; ums rose with evaluation apprehension | D7 |
| 83 | Goto, Itou & Hayamizu 1999 | full | Filled-pause detection by F0 slope and spectral stability: recall 84.9 %, precision 91.5 % (Japanese). Basis of the stability run | D7 |
| 84 | Gabrea & O'Shaughnessy 2000 | full | Switchboard filled pauses: recall 92.86 % at 2.36 % false alarms (preliminary); 83.72 % next to a silence | D7 |
| 85 | Zhu, Caceres & Salamon 2022, PodcastFillers | full | Voiced material with no transcript word as filler candidates; event F1 92.8 % with a classifier. The PodcastFillers corpus is the lab test of the FILLED_PAUSE label | D7 |
| 86 | Gao et al. 2024 | full (parts) | Decode against the known text: wav2vec 2.0 recall 0.83 at precision 0.29 (corrected in VF). Basis of the repetition label, which failed its lab gate | D7 |
| 87 | Lea et al. 2021, SEP-28k | full | Annotator kappa 0.25 for blocks, 0.11 for prolongations: block and pause are hard to separate from audio | D7 |
| 88 | Bayerl et al. 2022, KSoF | full (parts) | Kappa 0.37 for blocks, 0.42 for prolongations after training | D7 |
| 89 | Kourkounakis, Hajavi & Etemad 2021, LibriStutter | full (parts) | Synthetic stutter recipe (word and sound repetition, prolongation); LibriStutter is the lab corpus on which D7 failed | D7, SYN |
| 90 | Kouzelis et al. 2023 | full | Forced alignment with go-back and part-word arcs: recall 0.47–0.60 on synthetic data, F1 0.53–0.54 on UCLASS (not built) | D7 |
| 91 | Zhou et al. 2024, YOLO-Stutter | full | Waveform-edited stutters sound unnatural (MOS 2.22 vs 4.13); partial transfer to real speech; block recipe | D7, SYN |
| 92 | Harvill, Hasegawa-Johnson & Yoo 2022 | full | Repeat counts in recipes; pretraining on artificial prolongations hurt natural prolongation | D7, SYN |
| 93 | Tomisato et al. 2024 | full | Cluttering is not revealed by oral reading (AUC 0.61–0.66); tense and plain repetition not separable from audio | D7 |
| 94 | Bosker et al. 2013 | full (status corrected in VF) | Perceived fluency: pauses 59 %, speed 54 %, repairs 16 % of variance (second-language) | D7 |

## 9. Sentence endings

| # | Source | Read | What was taken | Used in |
|---|---|---|---|---|
| 95 | Chung & Bidelman 2022 | full | Sentence-final pitch change as a reading-prosody measure (Mandarin-speaking children; predicted reading rate only, VF correction) | D8 |
| 96 | Ritchart & Arvaniti 2014 | full | Uptalk: late rise on the last word of statements; 45 % of floor-holding utterances | D8 |
| 97 | Yuan & Liberman 2014 | full | Only 71.5 % of professional read-news phrases fall; slope 2.68 to 1.23 st/s by length | D8 |
| 98 | Rosenberg 2010, AuToBI | full | Final-200 ms features give 54.95 % on five boundary tones: only direction is defensible | D8 |
| 99 | Drugman, Kane & Gobl 2014 | full | Phrase-final creak at 40–70 Hz damages pitch tracks | D8 |

## 10. Alignment, comparison, edits, evaluation, explanations

| # | Source | Read | What was taken | Used in |
|---|---|---|---|---|
| 100 | Huang et al. 2024, label-prior CTC | full | Word-boundary error of wav2vec 2.0 CTC alignment 48 ms (TIMIT), 89 ms (Buckeye); CTC word spans shorter than hand labels (177 vs 241 ms) | AL, D2, D7 |
| 101 | McAuliffe et al. 2026, MFA in 2026 | full | Word-start errors MFA 19.93 / 21.75 ms, MMS 43.06 / 49.54 ms (accuracy the build gave up) | AL |
| 102 | Rousso et al. 2024 | full | Word ends within 50 ms on TIMIT: MFA 89.4 %, MMS 75.7 %, WhisperX 82.4 % | AL |
| 103 | Liang et al. 2026, coaching survey | full (preprint) | Coaching systems compare learner and reference duration and F0; a single "correct read" over-constrains style | REF |
| 104 | NIST/SEMATECH e-Handbook 1.3.5.17 | full | Robust spread 1.4826 × MAD (tolerance scales); modified z above 3.5 as outlier (robust start of the R2 whole-clip thresholds; the frozen whole-clip thresholds use the clip-budget quantile) | REF |
| 105 | Korzekwa et al. 2022 | full | Synthetic errors raised real pronunciation-error detection from AUC 0.528 to 0.749 (learned models) | SYN |
| 106 | Geirhos et al. 2020 | abstract | Shortcut learning: a learned detector can key on synthesis artefacts; one reason for a threshold rule and placebo clips | SYN, EVAL |
| 107 | Heittola & Mesaros, sed_eval | full (source code) | Event matching: onset 0.2 s, offset max(0.2 s, half the event) | EVAL |
| 108 | Bilen et al. 2020 | full | Collar and operating-point choices change event scores | EVAL |
| 109 | Kim et al. 2022 | full | Point adjustment inflates results; not used | EVAL |
| 110 | Cawley & Talbot 2010 | full | Selection on a small test set overfits; reason for one final evaluation per config | EVAL |
| 111 | Wisniewski, Zierer & Hattie 2020 | full | Feedback states goal, current state, next step (435 studies) | EXP |
| 112 | Kluger & DeNisi 1996 | abstract | Over a third of feedback interventions lowered performance | EXP |
| 113 | Shute 2008 | full (ETS RR-07-11 version) | Focus on the task, be specific, be cautious with overall grades | EXP |
| 114 | Miller 2019 | full | Accepted explanations are contrastive and select one or two causes | EXP |
| 115 | Wachter, Mittelstadt & Russell 2018 | abstract | Counterfactual: what would need to change; basis of "score with this penalty removed" | EXP |
| 116 | Pearl 2019 | full | A claim at one causal level needs evidence from that level: repair test, no claims about listeners | EXP, EVAL |
| 117 | Atil et al. 2024 | abstract | LLM output not repeatable at "deterministic" settings: templates instead | EXP |
| 118 | Tanveer, Lin & Hoque 2015, Rhema | abstract | Speakers preferred sparse to continuous feedback | EXP |

## Recorded as read and not cited

- **Not cited because no reading was recorded.** Verhelst & Roelands 1993 (WSOLA), Moulines & Charpentier 1990 (PSOLA), Morise et al. 2016 (WORLD) and Baevski et al. 2020 (wav2vec 2.0). The edit tools and the acoustic model are named without a paper citation.
- **Could not be opened.** Goberman, Hughes & Haydock 2011 (acoustics of public-speaking anxiety). Laukka et al. 2008 is read only through [22].
- **Read and set aside.** Interval rhythm metrics (contradictory results); envelope modulation spectrum (needs a trained discriminant); trained disfluency, prominence, creak and breath detectors (outside the no-training constraint); jitter, shimmer and tremor indices as nervousness cues (directions disagree; defined on sustained vowels).

## Corrections from the citation check

109 claims were re-checked against the primary text; no paper was missing or misattributed and no number was invented. These corrections are applied above:

1. Gao et al. 2024 [86]: at recall 0.83 the wav2vec 2.0 model had precision 0.29, not about 0.5.
2. Chung & Bidelman 2022 [95]: Mandarin-speaking children; the sentence-final pitch change predicted reading rate only.
3. Wang Y.-T. et al. 2010 [35]: 13.6 % (43 of 316) of pauses ≥ 250 ms are not breaths, not "about 10 %".
4. Within-clause pause evidence [37, 38] and the meta-analysis [20] are second-language speech, mostly picture narration or argumentative speech, not read text.
5. Bosker et al. 2013 [94]: full text available; read status full.
6. A numeric monotone cut-off exists (Hincks 2005 [42]); it does not transfer to read text.
7. The aligned word posterior is a published articulation measure (GOP-CTC-align [76, 77]), not only "confidence".

## Full references

**Rubrics and perception**

1. Schreiber, Paul & Shibley (2012). The development and test of the Public Speaking Competence Rubric. *Communication Education*, 61(3), 205–233. doi:10.1080/03634523.2012.670709. Secondary (reproduced in [2], Appendix B).
2. Joe, Kitchen, Chen & Feng (2015). A prototype public speaking skills assessment: An evaluation of human-scoring quality. *ETS Research Report Series*, RR-15-36. doi:10.1002/ets2.12083. Full.
3. Morreale, Moore, Surges-Tatum & Webster (Eds.) (2007). *The Competent Speaker Speech Evaluation Form* (2nd ed.). National Communication Association. Full.
4. Judging instruments: National Speech & Debate Association, *Declamation Starter Kit*, sample ballots and "How to Judge Declamation"; Poetry Out Loud, *Judge's Guide 2021–22*; Toastmasters International, *International Speech Contest Ballot*, Item 1172 (rev. 05/2024); University Interscholastic League (Texas), *Criteria for Evaluating Persuasive Speakers*. Full.
5. Chen, Feng, Leong, Joe, Kitchen & Lee (2016). Designing an automated assessment of public speaking skills using multimodal cues. *Journal of Learning Analytics*, 3(2), 261–281. doi:10.18608/jla.2016.32.13. Full.
6. Strangert & Gustafson (2008). What makes a good speaker? Subject ratings, acoustic measurements and perceptual evaluations. *Proc. Interspeech 2008*, 1688–1691. doi:10.21437/Interspeech.2008-368. Full.
7. Hahn (2004). Primary stress and intelligibility: Research to motivate the teaching of suprasegmentals. *TESOL Quarterly*, 38(2), 201–223. doi:10.2307/3588378. Abstract.
8. Van Zant & Berger (2020). How the voice persuades. *Journal of Personality and Social Psychology*, 118(4), 661–682. doi:10.1037/pspi0000193. Abstract.
9. Biadsy, Rosenberg, Carlson, Hirschberg & Strangert (2008). A cross-cultural comparison of American, Palestinian, and Swedish perception of charismatic speech. *Proc. Speech Prosody 2008*, 579–582. doi:10.21437/SpeechProsody.2008-131. Full.
10. Niebuhr, Tegtmeier & Schweisfurth (2019). Female speakers benefit more than male speakers from prosodic charisma training: A before-after analysis of 12-weeks and 4-h courses. *Frontiers in Communication*, 4, 12. doi:10.3389/fcomm.2019.00012. Full.
11. Strangert (2005). Prosody in public speech: Analyses of a news announcement and a political interview. *Proc. Interspeech 2005*, 3401–3404. doi:10.21437/Interspeech.2005-827. Full.
12. Duez (1982). Silent and non-silent pauses in three speech styles. *Language and Speech*, 25(1), 11–28. doi:10.1177/002383098202500102. Abstract.

**Pace and tempo**

13. Quené (2007). On the just noticeable difference for tempo in speech. *Journal of Phonetics*, 35(3), 353–362. doi:10.1016/j.wocn.2006.09.001. Full (author preprint).
14. de Jong & Wempe (2009). Praat script to detect syllable nuclei and measure speech rate automatically. *Behavior Research Methods*, 41(2), 385–390. doi:10.3758/BRM.41.2.385. Full.
15. Trouvain & Grice (1999). The effect of tempo on prosodic structure. *Proc. 14th ICPhS*, 1067–1070. Full.
16. Janse (2004). Word perception in fast speech: Artificially time-compressed vs. naturally produced fast speech. *Speech Communication*, 42(2), 155–173. doi:10.1016/j.specom.2003.07.001. Full.
17. Crystal & House (1990). Articulation rate and the duration of syllables and stress groups in connected speech. *Journal of the Acoustical Society of America*, 88(1), 101–112. doi:10.1121/1.399955. Abstract.
18. Jacewicz, Fox, O'Neill & Salmons (2009). Articulation rate across dialect, age, and gender. *Language Variation and Change*, 21(2), 233–256. doi:10.1017/S0954394509990093. Full-F, confirmed in VF.
19. Cucchiarini, Strik & Boves (2000). Quantitative assessment of second language learners' fluency by means of automatic speech recognition technology. *Journal of the Acoustical Society of America*, 107(2), 989–999. doi:10.1121/1.428279. Abstract.
20. Suzuki, Kormos & Uchihara (2021). The relationship between utterance and perceived fluency: A meta-analysis of correlational studies. *The Modern Language Journal*, 105(2), 435–463. doi:10.1111/modl.12706. Full (accepted manuscript).
21. Hofmann, Gerlach, Wender & Roth (1997). Speech disturbances and gaze behavior during public speaking in subtypes of social phobia. *Journal of Anxiety Disorders*, 11(6), 573–585. doi:10.1016/S0887-6185(97)00040-6. Abstract.
22. Teferra, Borwein, DeSouza, Simpson, Rheault & Rose (2022). Acoustic and linguistic features of impromptu speech and their association with anxiety. *JMIR Mental Health*, 9(7), e36828. doi:10.2196/36828. Full; the source through which Laukka et al. (2008) is read.
23. Schewski, Doss, Beldi & Keller (2025). Measuring negative emotions and stress through acoustic correlates in speech: A systematic review. *PLOS ONE*, 20(7), e0328833. doi:10.1371/journal.pone.0328833. Full.
24. Moers, Meyer & Janse (2017). Effects of word frequency and transitional probability on word reading durations of younger and older speakers. *Language and Speech*, 60(2), 289–317. doi:10.1177/0023830916649215. Abstract.
25. de Jong (2016). Predicting pauses in L1 and L2 speech: The effects of utterance boundaries and word frequency. *IRAL*, 54(2), 113–132. doi:10.1515/iral-2016-9993. Abstract.
26. Duong, Mostow & Sitaram (2011). Two methods for assessing oral reading prosody. *ACM Transactions on Speech and Language Processing*, 7(4), Article 14. doi:10.1145/1998384.1998388. Full.
27. Daane, Campbell, Grigg, Goodman & Oranje (2005). *Fourth-grade students reading aloud: NAEP 2002 special study of oral reading* (NCES 2006-469). National Center for Education Statistics. Full.
28. McIntosh, Smit, Saito, Minematsu & Kamper (2026). Self-supervised speech comparison for L2 phone, rhythm, and intonation scoring. arXiv:2607.13721. Full (preprint).
29. Camara, Blanco, Godino, Choi & Shattuck-Hufnagel (2026). Word lengthening as a function of utterance position: A multi-corpus study. arXiv:2606.23232. Full (preprint).

**Pauses**

30. Campione & Véronis (2002). A large-scale multilingual study of silent pause duration. *Proc. Speech Prosody 2002*, 199–202. doi:10.21437/SpeechProsody.2002-35. Full.
31. de Jong & Bosker (2013). Choosing a threshold for silent pauses to measure second language fluency. *Proc. DiSS 2013*, 17–20. Full.
32. Hallur, Thebaud, Tinchev, Ravichandran & Moro-Velazquez (2026). Reference-based prosody and rhythm evaluation for spoken dialogue systems. arXiv:2606.31055. Full (preprint).
33. Lövgren & van Doorn (2005). Influence of manipulation of short silent pause duration on speech fluency. *Proc. DiSS'05*, 123–126. Full.
34. Wang, Green, Nip, Kent & Kent (2010). Breath group analysis for reading and spontaneous speech in healthy adults. *Folia Phoniatrica et Logopaedica*, 62(6), 297–302. doi:10.1159/000316976. Full.
35. Wang, Green, Nip, Kent, Kent & Ullman (2010). Accuracy of perceptually based and acoustically based inspiratory loci in reading. *Behavior Research Methods*, 42(3), 791–797. doi:10.3758/BRM.42.3.791. Full-F, confirmed and corrected in VF.
36. Miller & Schwanenflugel (2006). Prosody of syntactically complex sentences in the oral reading of young children. *Journal of Educational Psychology*, 98(4), 839–853. doi:10.1037/0022-0663.98.4.839. Full-F, confirmed in VF.
37. Kahng (2018). The effect of pause location on perceived fluency. *Applied Psycholinguistics*, 39(3), 569–591. doi:10.1017/S0142716417000534. Abstract.
38. Tavakoli (2011). Pausing patterns: Differences between L2 learners and native speakers. *ELT Journal*, 65(1), 71–79. doi:10.1093/elt/ccq020. Abstract.
39. Schwanenflugel, Hamilton, Kuhn, Wisenbaker & Stahl (2004). Becoming a fluent reader: Reading skill and prosodic features in the oral reading of young readers. *Journal of Educational Psychology*, 96(1), 119–129. doi:10.1037/0022-0663.96.1.119. Full-F, confirmed in VF.

**Pitch**

40. 't Hart (1981). Differential sensitivity to pitch distance, particularly in speech. *Journal of the Acoustical Society of America*, 69(3), 811–821. doi:10.1121/1.385592. Abstract.
41. Hincks & Edlund (2009). Promoting increased pitch variation in oral presentations with transient visual feedback. *Language Learning & Technology*, 13(3), 32–50. Full.
42. Hincks (2005). Measuring liveliness in presentation speech. *Proc. Interspeech 2005*. doi:10.21437/Interspeech.2005-353. Full.
43. Niebuhr & Skarnitzl (2019). Measuring a speaker's acoustic correlates of pitch – but which? A contrastive analysis based on perceived speaker charisma. *Proc. ICPhS 2019*, 1774–1778. Full.
44. Boersma (1993). Accurate short-term analysis of the fundamental frequency and the harmonics-to-noise ratio of a sampled sound. *Proceedings of the Institute of Phonetic Sciences, University of Amsterdam*, 17, 97–110. Full.
45. Hirst (2011). The analysis by synthesis of speech melody: From data to models. *Journal of Speech Sciences*, 1(1), 55–83. doi:10.20396/joss.v1i1.15011. Full.
46. Arantes & Eriksson (2014). Temporal stability of long-term measures of fundamental frequency. *Proc. Speech Prosody 2014*, 1149–1152. doi:10.21437/SpeechProsody.2014-220. Full.
47. Strömbergsson (2016). Today's most frequently used F0 estimation methods, and their accuracy in estimating male and female pitch in clean speech. *Proc. Interspeech 2016*, 525–529. doi:10.21437/Interspeech.2016-240. Full.
48. Jouvet & Laprie (2017). Performance analysis of several pitch detection algorithms on simulated and real noisy speech data. *Proc. EUSIPCO 2017*, 1614–1618. doi:10.23919/EUSIPCO.2017.8081482. Full.
49. Zimmerer, Jügler, Andreeva, Möbius & Trouvain (2014). Too cautious to vary more? A comparison of pitch variation in native and non-native productions of French and German speakers. *Proc. Speech Prosody 2014*. Full.
50. Patterson & Ladd (1999). Pitch range modelling: Linguistic dimensions of variation. *Proc. ICPhS 1999*, 1169–1172. Full.
51. Wehrle, Cangemi, Krüger & Grice (2018). Somewhere over the spectrum: Between robotic and singsongy intonation. *Studi AISV*, 4, 179–194. doi:10.17469/O2104AISV000010. Full.
52. Portnova, Fletcher, Wisler & Borrie (2025). Assessing fundamental frequency variation in speakers with Parkinson's disease: Effects of tracking errors. *Journal of Speech, Language, and Hearing Research*, 68(7S), 3568–3582. doi:10.1044/2024_JSLHR-24-00381. Full.
53. Wang, Evanini & Yoon (2015). Word-level F0 modeling in the automated assessment of non-native read speech. *Proc. SLaTE 2015*. doi:10.21437/SLaTE.2015-5. Full.
54. Low, Bentley & Ghosh (2020). Automated assessment of psychiatric disorders using speech: A systematic review. *Laryngoscope Investigative Otolaryngology*, 5(1). PMC7042657. Full.
55. Traunmüller & Eriksson (1995). The perceptual evaluation of F0 excursions in speech as evidenced in liveliness estimations. *Journal of the Acoustical Society of America*, 97(3), 1905–1915. doi:10.1121/1.412942. Abstract.

**Emphasis**

56. Xu & Xu (2005). Phonetic realization of focus in English declarative intonation. *Journal of Phonetics*, 33, 159–197. doi:10.1016/j.wocn.2004.11.001. Full.
57. Suni, Aalto & Vainio (2015). Hierarchical representation of prosody for statistical speech synthesis. arXiv:1510.01949. Full (preprint of the method published in 2017).
58. Talman, Suni, Celikkanat, Kakouros, Tiedemann & Vainio (2019). Predicting prosodic prominence from text with pre-trained contextualized word representations. *Proc. NoDaLiDa 2019*. arXiv:1908.02262. Full.
59. Kallio, Suni & Šimko (2022). Fluency-related temporal features and syllable prominence as prosodic proficiency predictors for learners of English with different language backgrounds. *Language and Speech*, 65(3). PMC9326808. Full.
60. Sluijter & van Heuven (1996). Spectral balance as an acoustic correlate of linguistic stress. *Journal of the Acoustical Society of America*, 100(4), 2471–2485. doi:10.1121/1.417955. Full.
61. Kochanski, Grabe, Coleman & Rosner (2005). Loudness predicts prominence: Fundamental frequency lends little. *Journal of the Acoustical Society of America*, 118(2), 1038–1054. doi:10.1121/1.1923349. Abstract.
62. Baumann & Winter (2018). What makes a word prominent? Predicting untrained German listeners' perceptual judgments. *Journal of Phonetics*, 70, 20–38. doi:10.1016/j.wocn.2018.05.004. Full (accepted manuscript).
63. Kakouros, Räsänen & Alku (2018). Comparison of spectral tilt measures for sentence prominence in speech: Effects of dimensionality and adverse noise conditions. *Speech Communication*. Full (author manuscript).
64. Nenkova, Brenier, Kothari, Calhoun, Whitton, Beaver & Jurafsky (2007). To memorize or to predict: Prominence labeling in conversational speech. *Proc. NAACL HLT 2007*, 9–16. Full.
65. Mo, Cole & Lee (2008). Naïve listeners' prominence and boundary perception. *Proc. Speech Prosody 2008*. doi:10.21437/SpeechProsody.2008-163. Full.

**Volume**

66. Caswell-Midwinter & Whitmer (2019). Discrimination of gain increments in speech-shaped noises. *Trends in Hearing*, 23. doi:10.1177/2331216518820220. Full.
67. Liénard & Di Benedetto (1999). Effect of vocal effort on spectral properties of vowels. *Journal of the Acoustical Society of America*, 106(1), 411–422. doi:10.1121/1.428140. Abstract.
68. Sundberg & Nordenberg (2006). Effects of vocal loudness variation on spectrum balance as reflected by the alpha measure of long-term-average spectra of speech. *Journal of the Acoustical Society of America*, 120(1), 453–457. doi:10.1121/1.2208451. Abstract.
69. Eriksson & Traunmüller (1999). Perception of vocal effort and speaker distance on the basis of vowel utterances. *Proc. ICPhS 1999*. Full.
70. Pierrehumbert (1979). The perception of fundamental frequency declination. *Journal of the Acoustical Society of America*. doi:10.1121/1.383670. Abstract.
71. Ní Chasaide, Yanushevskaya & Gobl (2015). Prosody of voice: Declination, sentence mode and interaction with prominence. *Proc. ICPhS 2015*, paper 0476. Full.
72. Zhang & Hansen (2007). Analysis and classification of speech mode: Whispered through shouted. *Proc. Interspeech 2007*. Full.

**Clarity**

73. Picheny, Durlach & Braida (1986). Speaking clearly for the hard of hearing II: Acoustic characteristics of clear and conversational speech. *Journal of Speech and Hearing Research*, 29(4), 434–446. doi:10.1044/jshr.2904.434. Abstract.
74. Krause & Braida (2004). Acoustic properties of naturally produced clear speech at normal speaking rates. *Journal of the Acoustical Society of America*, 115(1), 362–378. doi:10.1121/1.1635842. Abstract.
75. Smiljanić & Bradlow (2009). Speaking and hearing clearly: Talker and listener factors in speaking style changes. *Language and Linguistics Compass*, 3(1), 236–264. PMC2747755. Full.
76. Cao, Fan, Svendsen & Salvi (2024). A framework for phoneme-level pronunciation assessment using CTC. *Proc. Interspeech 2024*, 302–306. doi:10.21437/Interspeech.2024-459. Full.
77. Halpern, Tienkamp, Abur & Toda (2026). PathBench: Speech intelligibility benchmark for automatic pathological speech assessment. arXiv:2603.08097. Full (preprint).

**Disfluency**

78. Lickley (2017). Disfluency in typical and stuttered speech. *Studi AISV*, 3, 373–387. doi:10.17469/O2103AISV000019. Full.
79. Shriberg (1999). Phonetic consequences of speech disfluency. *Proc. ICPhS 1999*, 619–622. Full.
80. Ritto, Costa, Juste & de Andrade (2016). Comparison of different speech tasks among adults who stutter and adults who do not stutter. *Clinics*, 71(3). doi:10.6061/clinics/2016(03)06. Full.
81. Clark & Fox Tree (2002). Using uh and um in spontaneous speaking. *Cognition*, 84, 73–111. doi:10.1016/S0010-0277(02)00017-3. Full.
82. Christenfeld & Creager (1996). Anxiety, alcohol, aphasia, and ums. *Journal of Personality and Social Psychology*, 70(3), 451–460. doi:10.1037/0022-3514.70.3.451. Abstract.
83. Goto, Itou & Hayamizu (1999). A real-time filled pause detection system for spontaneous speech recognition. *Proc. Eurospeech 1999*, 227–230. doi:10.21437/Eurospeech.1999-60. Full.
84. Gabrea & O'Shaughnessy (2000). Detection of filled pauses in spontaneous conversational speech. *Proc. ICSLP 2000*. doi:10.21437/ICSLP.2000-626. Full.
85. Zhu, Caceres & Salamon (2022). Filler word detection and classification: A dataset and benchmark. *Proc. Interspeech 2022*. arXiv:2203.15135. Full.
86. Gao, Tejedor-Garcia, Strik & Cucchiarini (2024). Reading miscue detection in primary school through automatic speech recognition. *Proc. Interspeech 2024*. arXiv:2406.07060. Full (parts).
87. Lea, Mitra, Joshi, Kajarekar & Bigham (2021). SEP-28k: A dataset for stuttering event detection from podcasts with people who stutter. *Proc. ICASSP 2021*. arXiv:2102.12394. Full.
88. Bayerl, Wolff von Gudenberg, Hönig, Nöth & Riedhammer (2022). KSoF: The Kassel State of Fluency dataset – a therapy centered dataset of stuttering. *Proc. LREC 2022*. arXiv:2203.05383. Full (parts).
89. Kourkounakis, Hajavi & Etemad (2021). FluentNet: End-to-end detection of stuttered speech disfluencies with deep learning. *IEEE/ACM Transactions on Audio, Speech, and Language Processing*, 29, 2986–2999. arXiv:2009.11394. Full (parts).
90. Kouzelis, Paraskevopoulos, Katsamanis & Katsouros (2023). Weakly-supervised forced alignment of disfluent speech using phoneme-level modeling. *Proc. Interspeech 2023*. arXiv:2306.00996. Full.
91. Zhou, Kashyap, Li, Sharma, Morin, Baquirin, Vonk, Ezzes, Miller, Gorno-Tempini, Lian & Anumanchipalli (2024). YOLO-Stutter: End-to-end region-wise speech dysfluency detection. *Proc. Interspeech 2024*, 937–941. doi:10.21437/Interspeech.2024-1855. Full.
92. Harvill, Hasegawa-Johnson & Yoo (2022). Frame-level stutter detection. *Proc. Interspeech 2022*, 2843–2847. Full.
93. Tomisato, Mori, Asano, Iimura, Yada, Takahashi, Wasano, Kono & Ozawa (2024). Speech characteristics that differentiate stuttering and cluttering in Japanese speakers. *Frontiers in Psychology*, 15, 1408929. doi:10.3389/fpsyg.2024.1408929. Full.
94. Bosker, Pinget, Quené, Sanders & de Jong (2013). What makes speech sound fluent? The contributions of pauses, speed and repairs. *Language Testing*, 30(2), 159–175. doi:10.1177/0265532212455394. Full (status corrected in VF).

**Sentence endings**

95. Chung & Bidelman (2022). Acoustic features of oral reading prosody and the relation with reading fluency and reading comprehension in Taiwanese children. *Journal of Speech, Language, and Hearing Research*, 65, 334–343. doi:10.1044/2021_JSLHR-21-00252. Full.
96. Ritchart & Arvaniti (2014). The form and use of uptalk in Southern Californian English. *Proc. Speech Prosody 2014*, 331–335. Full.
97. Yuan & Liberman (2014). F0 declination in English and Mandarin broadcast news speech. *Speech Communication*, 65, 67–74. Full.
98. Rosenberg (2010). AuToBI – a tool for automatic ToBI annotation. *Proc. Interspeech 2010*. Full.
99. Drugman, Kane & Gobl (2014). Data-driven detection and analysis of the patterns of creaky voice. *Computer Speech & Language*, 28(5), 1233–1253. arXiv:2006.00518. Full.

**Alignment, comparison, evaluation, explanation**

100. Huang, Zhang, Ni, Sun, Hira, Hwang, Manohar, Pratap, Wiesner, Watanabe, Povey & Khudanpur (2024). Less peaky and more accurate CTC forced alignment by label priors. arXiv:2406.02560. Full.
101. McAuliffe, Gunter, Wagner & Sonderegger (2026). Montreal Forced Aligner and the state of speech-to-text alignment in 2026. arXiv:2606.18466. Full.
102. Rousso, Cohen, Keshet & Chodroff (2024). Tradition or innovation: A comparison of modern ASR methods for forced alignment. *Proc. Interspeech 2024*. arXiv:2406.19363. Full.
103. Liang, Li, Rackauckas & Hirschberg (2026). A survey of automated presentation coaching: Systems, methods, and open challenges. arXiv:2606.27380. Full (preprint).
104. NIST/SEMATECH. *e-Handbook of Statistical Methods*, section 1.3.5.17, Detection of outliers. https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm. Full.
105. Korzekwa, Lorenzo-Trueba, Drugman & Kostek (2022). Computer-assisted pronunciation training: Speech synthesis is almost all you need. *Speech Communication*, 142, 22–33. doi:10.1016/j.specom.2022.06.003. Full.
106. Geirhos, Jacobsen, Michaelis, Zemel, Brendel, Bethge & Wichmann (2020). Shortcut learning in deep neural networks. *Nature Machine Intelligence*, 2(11), 665–673. doi:10.1038/s42256-020-00257-z. Abstract.
107. Heittola & Mesaros (n.d.). `sed_eval`: Evaluation toolbox for sound event detection, source file `sed_eval/sound_event.py`. https://github.com/TUT-ARG/sed_eval. Full (source code).
108. Bilen, Ferroni, Tuveri, Azcarreta & Krstulović (2020). A framework for the robust evaluation of sound event detection. *Proc. IEEE ICASSP 2020*, 61–65. doi:10.1109/ICASSP40776.2020.9052995. Full.
109. Kim, Choi, Choi, Lee & Yoon (2022). Towards a rigorous evaluation of time-series anomaly detection. *Proc. AAAI 2022*, 36(7), 7194–7201. doi:10.1609/aaai.v36i7.20680. Full.
110. Cawley & Talbot (2010). On over-fitting in model selection and subsequent selection bias in performance evaluation. *Journal of Machine Learning Research*, 11, 2079–2107. Full.
111. Wisniewski, Zierer & Hattie (2020). The power of feedback revisited: A meta-analysis of educational feedback research. *Frontiers in Psychology*, 10, 3087. doi:10.3389/fpsyg.2019.03087. Full.
112. Kluger & DeNisi (1996). The effects of feedback interventions on performance: A historical review, a meta-analysis, and a preliminary feedback intervention theory. *Psychological Bulletin*, 119(2), 254–284. doi:10.1037/0033-2909.119.2.254. Abstract.
113. Shute (2008). Focus on formative feedback. *Review of Educational Research*, 78(1), 153–189. doi:10.3102/0034654307313795. Full (read as ETS RR-07-11, 2007).
114. Miller (2019). Explanation in artificial intelligence: Insights from the social sciences. *Artificial Intelligence*, 267, 1–38. doi:10.1016/j.artint.2018.07.007. Full.
115. Wachter, Mittelstadt & Russell (2018). Counterfactual explanations without opening the black box: Automated decisions and the GDPR. *Harvard Journal of Law & Technology*, 31(2). arXiv:1711.00399. Abstract.
116. Pearl (2019). The seven tools of causal inference, with reflections on machine learning. *Communications of the ACM*, 62(3), 54–60. doi:10.1145/3241036. Full.
117. Atil, Aykent, Chittams, Fu, Passonneau, Radcliffe, Rajagopal, Sloan, Tudrej, Ture, Wu, Xu & Baldwin (2024). Non-determinism of "deterministic" LLM settings. arXiv:2408.04667. Abstract.
118. Tanveer, Lin & Hoque (2015). Rhema: A real-time in-situ intelligent interface to help people with public speaking. *Proc. ACM IUI 2015*, 286–295. doi:10.1145/2678025.2701386. Abstract.

**Added for sentence endings**

119. Vaughan-Johnston, Guyer, Fabrigar, Lamprinakos & Brinol (2024). Falling vocal intonation signals speaker confidence and conditionally boosts persuasion. *Personality and Social Psychology Bulletin*, 52(1), 3–21. doi:10.1177/01461672241262180. Full.
