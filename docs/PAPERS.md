# Papers used and what was taken from each

One row per source cited in `docs/GROUNDING.md`, with the same number. Each row gives the read status, what was taken from the source, where it sits in the system, and the research report that records it as read. The full citation is in the reference list of `docs/GROUNDING.md`.

**Read status.** *full* = the full text was read; *full-F* = full text read through a fetch tool that returns a model-written extraction (the report marks its numbers "to re-check"; the citation check confirmed those used here); *abstract* = only the abstract was read; *secondary* = read through the named source; *metadata* = only the bibliographic record. A claim from an abstract or a secondary source is weaker support.

**Report keys** (all under `build/work/research/`):

| Key | Report | Round |
|---|---|---|
| RE | `rubric_explain/REPORT.md` | first round, 2026-10-01 |
| FE | `features/REPORT.md` | first round |
| AL | `alignment/REPORT.md` | first round |
| GM | `grounding_model/REPORT.md` | first round |
| PP | `chain/pace_pauses/REPORT.md` (source numbers [n] of its section 6) | chain round, 2026-10-02 |
| DF | `chain/disfluency/REPORT.md` (source keys of its section 6) | chain round |
| PE | `chain/pitch_emphasis/REPORT.md` (source keys of its section 6) | chain round |
| VC | `chain/volume_clarity/REPORT.md` (source keys of its section 6) | chain round |
| SY | `chain/SYNTHESIS.md` | chain round |
| VF | `chain/VERIFICATION.md`: 109 claims re-checked against primary text; no paper missing or misattributed, no invented number | chain round |

Every chain-report source has a file `sources/<key>.txt` in its report folder with the URL, the read status and the passages relied on.

**Used in:** D1 pace, D2 pauses, D3 pitch range, D4 emphasis, D5 volume, D6 clarity proxy, D7 word time and disfluency, D8 sentence ending, D9 speech tempo and natural rushing, FAM hesitation and word-by-word families, AL alignment, REF reference-relative comparison, SYN controlled edits, EVAL evaluation, EXP explanations.

## 1. What counts as a delivery flaw (rubrics and perception)

| # | Source | Read | What was taken | Used in | Report |
|---|---|---|---|---|---|
| 1 | Schreiber, Paul & Shibley 2012, Public Speaking Competence Rubric | secondary (reproduced in [2]) | Lowest levels: "poor pacing", "speaks in monotone", "a voice too soft", "speaks inaudibly", "articulation too indistinct", "distracts listeners with fillers" | D1, D3, D5, D6, D7 | RE §2.1 |
| 2 | Joe, Kitchen, Chen & Feng 2015, ETS RR-15-36 | full | Rubric text of [1]; two expert raters agreed exactly on "vocal expression" for 30 % of presentations | all, REF | RE §2.1, §2.3 |
| 3 | Morreale et al. 2007, Competent Speaker form | full | "vocal variety in rate, pitch, and intensity"; "properly formed sounds"; "nonfluencies and disfluencies interfere with the message"; levels separated by "occasional" against "frequent" | D1, D3, D6, D7 | RE §2.1 |
| 4 | Judging instruments: NSDA, Poetry Out Loud, Toastmasters 1172, UIL | full | Quotations shown beside each flag ("too slow or hurried pace", "pauses come in suitable places", "Is the volume appropriate?", "Was enunciation clear?", pitch change "for emphasis", "singsong", "monotone"); no numeric threshold; NSDA Declamation "is not designed for students to mimic the original author" | all, REF, EXP | RE §2.1, §2.3 |
| 5 | Chen et al. 2016, automated public-speaking assessment | full | Mean silence inside clauses vs holistic score, \|r\| = 0.479 (n = 28); inter-rater ICC 0.385 on 56 videos | D2, REF | RE §2.3, §3.2 |
| 6 | Strangert & Gustafson 2008 | full | "monotonous" r = −.91 and pitch range r = .61 with good-speaker ratings; resynthesis: pitch dynamics > fluency > rate; +5 % rate with shorter hesitation pauses raised rankings | D1, D3 | RE §3.1, §3.4; PE |
| 7 | Hahn 2004 | abstract | Correct primary stress: more content recalled, speaker rated higher | D4 | RE §3.4 |
| 8 | Van Zant & Berger 2020 | abstract | Persuaders "speak louder and vary their volume", signalling confidence | D5 | RE §3.4 |
| 9 | Biadsy et al. 2008 | full | Intensity mean and SD vs charisma r = .14 to .35; effects differ by rater language | D5, REF | RE §3.4 |
| 10 | Niebuhr, Tegtmeier & Schweisfurth 2019 | full | Effects reverse at the extremes ("too high-pitched or too fast"): the literature justifies dimensions, not ideal values | REF | RE §3.4 |
| 11 | Strangert 2005 | full | Silence-to-speech ratio 9 % (professional) against 28 % (non-professional reading), Swedish | D2 | RE §3.2 |
| 12 | Duez 1982 | abstract | Prepared political speeches: 50 % more silent-pause time than interviews, mostly at clause or phrase boundaries | D2 | RE §3.2 |
| 119 | Vaughan-Johnston et al. 2024 | full | Falling against rising intonation on the last word (±35 Hz) changed confidence ratings (5.55 vs 4.82); persuasion benefit only for strong arguments | D8 | RE §3.4 |

## 2. Pace, tempo and natural rushing

| # | Source | Read | What was taken | Used in | Report |
|---|---|---|---|---|---|
| 13 | Quené 2007, tempo JND | full (author preprint) | JND for speech tempo about 5 %; the D1 floor ln 1.10 lies above it | D1 | RE §3.1 |
| 14 | de Jong & Wempe 2009 | full | Speaking rate includes pauses, articulation rate excludes them: D1 removes pauses from speech time | D1 | FE §1.2 |
| 15 | Trouvain & Grice 1999 | full | Fast reading: articulation rate +13 % and +18 % (two of three readers), speaking rate up to +28 %, pauses removed or shortened. Source of the natural-rush recipe rates ×1.13 / ×1.15 / ×1.18 | D1, D2, D9 | PP [36]; VF |
| 16 | Janse 2004 | full | Natural fast speech is not uniform compression; unstressed syllables shrink more; listeners preferred linear compression | D1, D9 | PP [37] |
| 17 | Crystal & House 1990 | abstract | Durations of comparable runs of different talkers on one text are highly correlated: supports run-by-run comparison on a fixed text | D1, REF | PP [39] |
| 18 | Jacewicz et al. 2009 | full-F (confirmed) | Read sentences 3.40 syllables/s, SD 0.42 across speakers: habitual rate differs between speakers | D1 | PP [41]; VF |
| 19 | Cucchiarini, Strik & Boves 2000 | abstract | Read speech: rate of speech correlated 0.90–0.93 with expert fluency ratings | D9 | PP [28]; VF |
| 20 | Suzuki, Kormos & Uchihara 2021 | full (accepted manuscript) | Meta-analysis of 22 second-language studies: articulation rate r = .62, speech rate .76, pause frequency −.59 with rated fluency | D9 | PP [31]; VF |
| 21 | Hofmann et al. 1997 | abstract | Speakers with social phobia paused more often and longer in public speaking | D1, D7 | PP [10]; DF |
| 22 | Teferra et al. 2022 | full | Source through which Laukka et al. 2008 is read: share of silence r = .36 with state anxiety | D1 | PP [12]; VF |
| 23 | Schewski et al. 2025 | full | "No consistent acoustic patterns were identified for fear or anxiety"; mean F0 raised under stress in 15 of 19 studies | D1, D3 | PP [14]; PE; VC |
| 24 | Moers, Meyer & Janse 2017 | abstract | Longer reading durations for low-probability words: the processing-difficulty pattern behind HESITATION | D1, FAM | PP [18] |
| 25 | de Jong 2016 | abstract | Pauses more likely before low-frequency words | D1, FAM | PP [19] |
| 26 | Duong, Mostow & Sitaram 2011 | full | Word latency and duration contours correlated with a fluent reading of the same text; "F0 match" was among the best indicators of expressive reading (children). Not built | D1, D3, REF | PP [24]; PE |
| 27 | Daane et al. 2005, NAEP oral reading study | full | "Reads primarily word-by-word" (level 1): the WORD_BY_WORD pattern | FAM | PP [23] |
| 28 | McIntosh et al. 2026 | full (preprint) | Tempo irregularity along an alignment with a reference: r = .37 alone, human agreement .49. Source of the uneven-tempo measure, which failed its lab gate | FAM | PP [49]; VF |
| 29 | Camara et al. 2026 | full (preprint) | Utterance-final words 80 ms longer in matched within-speaker comparisons: an effect at the size of the aligner's boundary error | AL | PP [52]; VF |

## 3. Pauses

| # | Source | Read | What was taken | Used in | Report |
|---|---|---|---|---|---|
| 30 | Campione & Véronis 2002 | full | Pause classes brief < 200 ms, medium, long > 1000 ms "only in spontaneous speech"; English read speech median 493 ms, modes 126 and 512 ms (basis of the 0.5 s rule for dropped pauses) | D2 | RE §3.2; FE §5 |
| 31 | de Jong & Bosker 2013 | full | Published pause thresholds run from 100 to 1000 ms; 250 ms is the classic convention (the feature research recommended 250 ms; the build uses 0.20 s) | D2 | FE §1.2, §5 |
| 32 | Hallur et al. 2026 | full (preprint) | 0.2 s as a practical pause threshold; reference-based evaluation with speech rate, articulation rate and pause ratio; limit: does "not yet map deviations to perceptual thresholds" | D2, REF | RE §3.1, §3.2, §7 |
| 33 | Lövgren & van Doorn 2005 | full | Silences of 57 / 117 / 212 / 403 ms judged disfluent in 12.5 / 34.4 / 71.9 / 93.8 % of samples | D2, FAM | PP [56]; VF |
| 34 | Wang Y.-T. et al. 2010, breath groups | full | Reading: inter-breath pause 0.64 s (0.25–1.8 s); 1.8 % of breaths at ungrammatical places; pauses before noun, verb or adverbial phrases are "appropriate" | D2 | PP [1]; VF |
| 35 | Wang Y.-T. et al. 2010, inspiratory loci | full-F (confirmed, one figure corrected) | A 250 ms pause as breath candidate; 13.6 % of such pauses are not breaths | D2 | PP [2]; VF |
| 36 | Miller & Schwanenflugel 2006 | full-F (confirmed) | Skilled adult readers: sentence-end pauses mean 446 ms, comma pauses mean 59 ms (0–454 ms): no D2+ flag at punctuation | D2 | PP [22]; VF |
| 37 | Kahng 2018 | abstract | Within-clause silent pause rate had the strongest correlation with second-language fluency ratings | D2 | PP [34]; VF |
| 38 | Tavakoli 2011 | abstract | Learners pause in the middle of clauses rather than at the end | D2 | PP [33]; VF |
| 39 | Schwanenflugel et al. 2004 | full-F (confirmed) | Within-sentence pauses 688 ms (slowest readers) against 313–365 ms (children) | D2 | PP [21]; VF |

## 4. Pitch range

| # | Source | Read | What was taken | Used in | Report |
|---|---|---|---|---|---|
| 40 | 't Hart 1981 | abstract | Pitch-distance JND 1.5–2 st; only differences above 3 st matter in communication: basis of the 1 st regularisation of range ratios | D3 | RE §3.3; PE |
| 41 | Hincks & Edlund 2009 | full | Semitones relative to the speaker as perceptual normalisation; SD of semitones over a moving 10 s window | D3 | RE §3.3 |
| 42 | Hincks 2005 | full | PVQ below .15 over 10 s "generally rated as on the monotone side"; does not transfer to read text | D3 | PE; VF |
| 43 | Niebuhr & Skarnitzl 2019 | full | P90 − P10 range r = .52 with charisma, SD .35, max − min .04 (40–98 s excerpts): choice of the percentile range | D3 | PE; VF |
| 44 | Boersma 1993 | full | The Praat autocorrelation pitch tracker, used through parselmouth | D3, D4, D8 | FE §2.1 |
| 45 | Hirst 2011 | full | Pitch floor and ceiling from the recording's own quartiles (two-pass tracking) | D3 | FE §2.1 |
| 46 | Arantes & Eriksson 2014 | full | Long-term F0 averages settle after about 10 s: centring on the whole passage | D3 | FE §1.3 |
| 47 | Strömbergsson 2016 | full | Praat F0 frame error 7.05 % default, 6.20 % sex-adapted range | D3 | FE §2.2 |
| 48 | Jouvet & Laprie 2017 | full | Praat frame error 5.05 % clean; another tracker better on real noisy speech | D3 | FE §2.2 |
| 49 | Zimmerer et al. 2014 | full | Second-language reading compresses the whole-passage span (SD/mean 0.118–0.133 against 0.134–0.146) | D3 | PE |
| 50 | Patterson & Ladd 1999 | full | Percentile spans were weaker than landmark spans against listener judgements | D3 | PE |
| 51 | Wehrle et al. 2018 | full | Long-term measures cannot tell a slow rise from a repeated contour (sing-song); reason REPEATED_CONTOUR has no detector | D3, FAM | PE |
| 52 | Portnova et al. 2025 | full | Tracking errors inflate SD; IQR measures are more robust | D3 | PE |
| 53 | Wang, Evanini & Yoon 2015 | full | Pitch match with native readings: r .34–.39 with human scores; unstable with fewer than 10–20 reference readers | D3, REF | PE |
| 54 | Low, Bentley & Ghosh 2020 | full | Lower F0 and narrower F0 range in depression (low-arousal pattern) | D3 | PE |
| 55 | Traunmüller & Eriksson 1995 | abstract | F0 intervals judged equivalent when equal in semitones | D3 | PE |

## 5. Emphasis

| # | Source | Read | What was taken | Used in | Report |
|---|---|---|---|---|---|
| 56 | Xu & Xu 2005 | full | Focus: expanded range on the focused syllable, suppressed range after it | D4 | PE |
| 57 | Suni, Aalto & Vainio 2015 | full (preprint) | Equal-weight z-sum of F0, energy and duration: 79.2 % on read news; wavelet version 84.6 % | D4 | PE |
| 58 | Talman et al. 2019 | full | Tuned weights gain about 0.7 points over equal weights | D4 | PE |
| 59 | Kallio, Suni & Šimko 2022 | full | Less proficient readers: "prominence variation pattern is more flat"; prominence similarity explains 4.19–5.60 % of rating variance | D4 | PE |
| 60 | Sluijter & van Heuven 1996 | full | Spectral balance carries lexical stress; F0 excursions carry accent (spectral balance not used) | D4 | FE §6.1 |
| 61 | Kochanski et al. 2005 | abstract | Loudness and duration stronger than F0 as prominence cues in their materials | D4 | FE §6.1; PE |
| 62 | Baumann & Winter 2018 | full (accepted manuscript) | German read sentences: amplitude, F0 and spectral tilt among the important continuous cues; part of the cue-weight comparison | D4 | PE |
| 63 | Kakouros, Räsänen & Alku 2018 | full (author manuscript) | Duration best, tilt systematic but weaker; supports equal weights for read speech | D4 | PE; VF |
| 64 | Nenkova et al. 2007 | full | Content words far more likely accented than function words; text prior (not built; D4+ failed its lab gate) | D4, FAM | PE |
| 65 | Mo, Cole & Lee 2008 | full | Listener agreement on prominence: Fleiss kappa .373–.421 | D4 | PE |

## 6. Volume

| # | Source | Read | What was taken | Used in | Report |
|---|---|---|---|---|---|
| 66 | Caswell-Midwinter & Whitmer 2019 | full | Level JND 1.5 dB, 3 dB noticeable (hearing-impaired listeners, speech-shaped noise): above them lies the D5 floor of 2 dB | D5 | RE §3.4 |
| 67 | Liénard & Di Benedetto 1999 | abstract | Effort raises high-frequency harmonics more than level ("a change in spectral tilt"); F0 and F1 rise with effort | D5, FAM | VC lienard1999 |
| 68 | Sundberg & Nordenberg 2006 | abstract | Alpha ratio ranges 19.0 / 11.7 dB over about 28 dB of level (women / men): basis of the LOW_EFFORT tilt recipe (0.55 dB per dB) | D5, FAM | VC sundberg2006; VF |
| 69 | Eriksson & Traunmüller 1999 | full | Listeners tell increased effort from decreased distance on phonated vowels: effort and gain are separable | D5 | VC eriksson1999 |
| 70 | Pierrehumbert 1979 | abstract | Amplitude downdrift accompanies F0 declination (trailing-off pattern) | D5, FAM | VC pierrehumbert1979 |
| 71 | Ní Chasaide, Yanushevskaya & Gobl 2015 | full | Source strength declines −7.3 dB/s in short declaratives with laxer phonation | D5, FAM | VC nichasaide2015 |
| 72 | Zhang & Hansen 2007 | full | The absolute SPL of a recording may be unknown because of recording levels and AGC | D5 | VC zhang_hansen2007 |

## 7. Clarity

| # | Source | Read | What was taken | Used in | Report |
|---|---|---|---|---|---|
| 73 | Picheny, Durlach & Braida 1986 | abstract | Conversational speech: reduced vowels, unreleased final stops; clear speech is a bundle of properties | D6 | FE §4; VC picheny1986 |
| 74 | Krause & Braida 2004 | abstract | Clear speech at normal rate: more 1–3 kHz energy, deeper low-frequency envelope modulation | D6 | FE §4; VC krause2004 |
| 75 | Smiljanić & Bradlow 2009 | full | Full-text review of the clear-speech bundle | D6 | VC smiljanic2009 |
| 76 | Cao et al. 2024 | full | The aligned CTC posterior is GOP-CTC-align, a published pronunciation measure (not scored here) | D6 | VC cao2024; VF |
| 77 | Halpern et al. 2026, PathBench | full (preprint) | Articulatory precision (average aligned posterior) r = 0.71 with rated intelligibility over six pathological datasets | D6 | VC halpern2026pathbench; VF |

## 8. Disfluency

| # | Source | Read | What was taken | Used in | Report |
|---|---|---|---|---|---|
| 78 | Lickley 2017 | full | Stuttering forms (rapid onset repeats, prolongation, block) and positions; typical repeats 96 % on function words; events about 1 s | D7 | DF lickley2017; VF |
| 79 | Shriberg 1999 | full | First token of a repeat lengthened; filled pause schwa-like, long, low and falling F0; under 1 % of words disfluent in constrained speech | D7 | DF shriberg1999_phonetic; VF |
| 80 | Ritto et al. 2016 | full | Fluent adults reading aloud: 0.21 % stuttered syllables (n = 17): the base rate | D7 | DF ritto2016_speech_tasks; VF |
| 81 | Clark & Fox Tree 2002 | full | "Um" followed by delays more often than "uh" (61 vs 29 %) | D7 | DF clark_foxtree2002; VF |
| 82 | Christenfeld & Creager 1996 | abstract | Fillers and anxiety not linked "in any simple way"; ums rose with evaluation apprehension | D7 | DF christenfeld1996_abstract |
| 83 | Goto, Itou & Hayamizu 1999 | full | Filled-pause detection by F0 slope and spectral stability: recall 84.9 %, precision 91.5 % (Japanese). Basis of the stability run | D7 | DF goto1999_filled_pause; VF |
| 84 | Gabrea & O'Shaughnessy 2000 | full | Switchboard filled pauses: recall 92.86 % at 2.36 % false alarms (preliminary); 83.72 % next to a silence | D7 | DF gabrea2000_filled_pause; VF |
| 85 | Zhu, Caceres & Salamon 2022, PodcastFillers | full | Voiced material with no transcript word as filler candidates; event F1 92.8 % with a classifier. The PodcastFillers corpus is the lab test of the FILLED_PAUSE label | D7 | DF zhu2022_podcastfillers; VF |
| 86 | Gao et al. 2024 | full (parts) | Decode against the known text: wav2vec 2.0 recall 0.83 at precision 0.29 (corrected in VF). Basis of the repetition label, which failed its lab gate | D7 | DF gao2024_miscue; VF |
| 87 | Lea et al. 2021, SEP-28k | full | Annotator kappa 0.25 for blocks, 0.11 for prolongations: block and pause are hard to separate from audio | D7 | DF lea2021_sep28k; VF |
| 88 | Bayerl et al. 2022, KSoF | full (parts) | Kappa 0.37 for blocks, 0.42 for prolongations after training | D7 | DF bayerl2022_ksof; VF |
| 89 | Kourkounakis, Hajavi & Etemad 2021, LibriStutter | full (parts) | Synthetic stutter recipe (word and sound repetition, prolongation); LibriStutter is the lab corpus on which D7 failed | D7, SYN | DF kourkounakis2020_fluentnet_libristutter |
| 90 | Kouzelis et al. 2023 | full | Forced alignment with go-back and part-word arcs: recall 0.47–0.60 on synthetic data, F1 0.53–0.54 on UCLASS (not built) | D7 | DF kouzelis2023_wsfa; VF |
| 91 | Zhou et al. 2024, YOLO-Stutter | full | Waveform-edited stutters sound unnatural (MOS 2.22 vs 4.13); partial transfer to real speech; block recipe | D7, SYN | DF zhou2024_yolo_stutter; GM §6.1; VF |
| 92 | Harvill, Hasegawa-Johnson & Yoo 2022 | full | Repeat counts in recipes; pretraining on artificial prolongations hurt natural prolongation | D7, SYN | DF harvill2022_frame_level |
| 93 | Tomisato et al. 2024 | full | Cluttering is not revealed by oral reading (AUC 0.61–0.66); tense and plain repetition not separable from audio | D7 | DF tomisato2024_cluttering; VF |
| 94 | Bosker et al. 2013 | full (status corrected in VF) | Perceived fluency: pauses 59 %, speed 54 %, repairs 16 % of variance (second-language) | D7 | PP [30]; DF bosker2013_2014; VF |

## 9. Sentence endings

| # | Source | Read | What was taken | Used in | Report |
|---|---|---|---|---|---|
| 95 | Chung & Bidelman 2022 | full | Sentence-final pitch change as a reading-prosody measure (Mandarin-speaking children; predicted reading rate only, VF correction) | D8 | PE; VF |
| 96 | Ritchart & Arvaniti 2014 | full | Uptalk: late rise on the last word of statements; 45 % of floor-holding utterances | D8 | PE |
| 97 | Yuan & Liberman 2014 | full | Only 71.5 % of professional read-news phrases fall; slope 2.68 to 1.23 st/s by length | D8 | PE; VC |
| 98 | Rosenberg 2010, AuToBI | full | Final-200 ms features give 54.95 % on five boundary tones: only direction is defensible | D8 | PE |
| 99 | Drugman, Kane & Gobl 2014 | full | Phrase-final creak at 40–70 Hz damages pitch tracks | D8 | PE; VC |

## 10. Alignment, comparison, edits, evaluation, explanations

| # | Source | Read | What was taken | Used in | Report |
|---|---|---|---|---|---|
| 100 | Huang et al. 2024, label-prior CTC | full | Word-boundary error of wav2vec 2.0 CTC alignment 48 ms (TIMIT), 89 ms (Buckeye); CTC word spans shorter than hand labels (177 vs 241 ms) | AL, D2, D7 | AL "Published boundary errors"; GM §2 |
| 101 | McAuliffe et al. 2026, MFA in 2026 | full | Word-start errors MFA 19.93 / 21.75 ms, MMS 43.06 / 49.54 ms (accuracy the build gave up) | AL | AL "Published boundary errors" |
| 102 | Rousso et al. 2024 | full | Word ends within 50 ms on TIMIT: MFA 89.4 %, MMS 75.7 %, WhisperX 82.4 % | AL | AL; GM §2 |
| 103 | Liang et al. 2026, coaching survey | full (preprint) | Coaching systems compare learner and reference duration and F0; a single "correct read" over-constrains style | REF | RE §3.1, §6.4 |
| 104 | NIST/SEMATECH e-Handbook 1.3.5.17 | full | Robust spread 1.4826 × MAD (tolerance scales); modified z above 3.5 as outlier (robust start of the R2 whole-clip thresholds; the frozen whole-clip thresholds use the clip-budget quantile) | REF | RE §5.4; GM §4.2 |
| 105 | Korzekwa et al. 2022 | full | Synthetic errors raised real pronunciation-error detection from AUC 0.528 to 0.749 (learned models) | SYN | GM Recommendation, §6.1 |
| 106 | Geirhos et al. 2020 | abstract | Shortcut learning: a learned detector can key on synthesis artefacts; one reason for a threshold rule and placebo clips | SYN, EVAL | RE §5.1 |
| 107 | Heittola & Mesaros, sed_eval | full (source code) | Event matching: onset 0.2 s, offset max(0.2 s, half the event) | EVAL | GM §7.3 |
| 108 | Bilen et al. 2020 | full | Collar and operating-point choices change event scores | EVAL | GM §7.3 |
| 109 | Kim et al. 2022 | full | Point adjustment inflates results; not used | EVAL | GM §7.3 |
| 110 | Cawley & Talbot 2010 | full | Selection on a small test set overfits; reason for one final evaluation per config | EVAL | GM §1 |
| 111 | Wisniewski, Zierer & Hattie 2020 | full | Feedback states goal, current state, next step (435 studies) | EXP | RE §6.4 |
| 112 | Kluger & DeNisi 1996 | abstract | Over a third of feedback interventions lowered performance | EXP | RE §6.4 |
| 113 | Shute 2008 | full (ETS RR-07-11 version) | Focus on the task, be specific, be cautious with overall grades | EXP | RE §6.4 |
| 114 | Miller 2019 | full | Accepted explanations are contrastive and select one or two causes | EXP | RE §6.4 |
| 115 | Wachter, Mittelstadt & Russell 2018 | abstract | Counterfactual: what would need to change; basis of "score with this penalty removed" | EXP | RE §6.4 |
| 116 | Pearl 2019 | full | A claim at one causal level needs evidence from that level: repair test, no claims about listeners | EXP, EVAL | RE §7 |
| 117 | Atil et al. 2024 | abstract | LLM output not repeatable at "deterministic" settings: templates instead | EXP | RE §6.3 |
| 118 | Tanveer, Lin & Hoque 2015, Rhema | abstract | Speakers preferred sparse to continuous feedback | EXP | RE §6.4 |

## 11. Recorded as read and not cited

The chain reports list about 270 sources (PP 57, DF 52, PE about 60, VC 103); the first-round reports list more. Only the sources above carry a claim in `docs/GROUNDING.md`. The full lists, with read status, are in section 6 of each chain report and in the source sections of the first-round reports. Points to note:

- **Not cited because no research report records them as read.** Verhelst & Roelands 1993 (WSOLA), Moulines & Charpentier 1990 (PSOLA), Morise et al. 2016 (WORLD) and Baevski et al. 2020 (wav2vec 2.0) appear only in the condensed log of the flaw-synthesis research (`flaw_synthesis/RUN2_condensed.md`, which has no REPORT.md) or not at all. The edit tools and the acoustic model are named in `docs/GROUNDING.md` without a paper citation.
- **Could not be opened by any agent.** Goberman, Hughes & Haydock 2011 (acoustics of public-speaking anxiety), the one paper most likely to say whether nervousness speeds up or flattens a prepared speech (SY §6). Laukka et al. 2008 is read only through [22].
- **Read and set aside by the reports.** Interval rhythm metrics (contradictory, PP §2.1 Reason F); envelope modulation spectrum (needs a trained discriminant); trained disfluency, prominence, creak and breath detectors (outside the no-training constraint, DF §2.6 M8, PE §2.2); jitter, shimmer and tremor indices as nervousness cues (directions disagree, defined on sustained vowels, VC §2.3).
- **Read only through another source or as a search summary** (not cited): Fry 1955 (FE §6.1); Wingrove 2017 and Foulke & Sticht 1969 (RE §3.1); Megehee, Dobie & Grant 2003, Nooteboom & Eefting 1994 and Janse 2004 as reported in [13] (RE §3.1); Sadler 1989 and Nicol & Macfarlane-Dick 2006 (RE §6.4).

## 12. Corrections from the citation check that this file applies

From VF, applied in the rows above and in `docs/GROUNDING.md`:

1. Gao et al. 2024 [86]: at recall 0.83 the wav2vec 2.0 model had precision 0.29, not about 0.5.
2. Chung & Bidelman 2022 [95]: Mandarin-speaking children; the sentence-final pitch change predicted reading rate only.
3. Wang Y.-T. et al. 2010 [35]: 13.6 % (43 of 316) of pauses ≥ 250 ms are not breaths, not "about 10 %".
4. Within-clause pause evidence [37, 38] and the meta-analysis [20] are second-language speech, mostly picture narration or argumentative speech, not read text.
5. Bosker et al. 2013 [94]: full text available; read status full.
6. A numeric monotone cut-off exists (Hincks 2005 [42]); it does not transfer to read text (SY §5).
7. The aligned word posterior is a published articulation measure (GOP-CTC-align [76, 77]), not only "confidence" (SY §5).
