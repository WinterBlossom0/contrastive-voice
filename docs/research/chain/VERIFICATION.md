# Citation verification of the four chain reports (2026-10-02)

**Result:** 109 claims checked against primary text (30 pace/pauses, 26 disfluency, 25 pitch/emphasis, 28 volume/clarity). No paper is missing or misattributed, and no invented number was found. Six claims need correcting and nine need a wording or context fix; the two that change a ranked measure are the Gao 2024 precision figure (disfluency #1) and the Chung & Bidelman finding (pitch sentence-final measure).

**Method.** PDFs were fetched with `curl` and searched with `pdftotext` (`-layout` and `-raw`). PMC articles came as raw HTML with tags stripped, as Europe PMC XML, or as NCBI BioC JSON. PubMed abstracts came as text from E-utilities; OpenAlex, Crossref and arXiv records came from their APIs. No model-written summary was used. Everything fetched is in the scratchpad under `v/` (`pp`, `df`, `pe`, `vc`); no project file was touched.

**Existence.** All six 2026 arXiv preprints resolve with the stated titles and authors: 2607.13721, 2606.23232, 2603.08097, 2602.12723, 2606.27543, 2607.19645. Abur 2026 (PLOS One), Han 2026 (Children), Sandoval 2025 (Behav Sci), Wang Q 2025, Rood & de Jong 2023, Talkar 2025 and Cao 2024 resolve in Crossref or Europe PMC.

## 1. pace_pauses

| Claim | Source | Verdict | What the source says | How checked |
|---|---|---|---|---|
| Quartile pauses 661/604/411/369 ms between sentences, 688/518/313/365 ms within | [21] Schwanenflugel 2004 (full-F) | CONFIRMED | Table 1 gives the same means (SDs 231/234/149/195 and 450/243/236/267) | PMC2748352 HTML |
| Sample size "123 and 24" versus "120 and 34" unresolved | [21] | RESOLVED | Abstract: "(N = 123) and 24 adults". Method: "Participants were 120 second- and third-grade children". Footnote 1: "4 out of 34 adults" excluded. The paper is internally inconsistent; the fetched text was accurate | same |
| Adults 189.0 correct words per minute, SD 38.0 | [21] | CONFIRMED | "at least 95 correct words per minute (M = 189.0, SD = 38.0)" (footnote 1) | same |
| Adult pauses: sentence end 446 ms (145-685); phrase-final comma 59 (0-454); adjective comma 53 (0-337) | [22] Miller & Schwanenflugel 2006 (full-F) | CONFIRMED | Table: 145/685/446/SD 162; 0/454/59/SD 128; 0/337/53/SD 105. Minimum 0 means no pause; only pauses over 100 ms were measured | PMC2748355 HTML |
| Skilled children: shorter pauses "at commas (R2 = .328)" | [22] | WRONG CONTEXT (minor) | .328 is the first comma of the complex adjectival phrase. Phrase-final commas: "R2 = .144". Sentence ends .251 is correct | same |
| 3.40 syll/s, SD 0.42; differences 8 %, 11 %, 4.5 % | [41] Jacewicz 2009 (full-F) | CONFIRMED | "3.40 syll/s (s.d.=0.42)"; "8% faster"; "11% faster"; "4.5% faster" (read sentences) | PMC2790192 HTML |
| Correlation 0.745, mean error 0.339, SD of error 0.796 (Switchboard) | [44] Wang & Narayanan 2007 (full-F) | CONFIRMED | Table III, proposed approach: ".745 / .339 / 0.796" | PMC2860302 HTML |
| Four of five talkers shortened the phrase, one lengthened; no consistent result across talkers | [17] Lively 1993 (full-F) | CONFIRMED | "Four of the five talkers had significantly shorter overall phrase durations ... One talker demonstrated the opposite pattern"; "We did not obtain consistent results across all five talkers" | PMC3499954 HTML |
| 250 ms threshold: no misses, false alarms 43/408, accuracy .895 | [2] Wang 2010 loci (full-F) | CONFIRMED, with caveat | Table 2 at 250 ms: TPR .999, FPR .319, accuracy .895, d′ 3.561. The same table gives accuracy .922 at 300 ms and .914 at 350 ms; 250 ms is best by d′, although the text calls it best "in terms of accuracy" | PMC3645855 HTML |
| "About 10 % of such pauses are not breaths" (section 4, #7) | [2] | WRONG CONTEXT | 316 pauses were ≥250 ms and 43 of them were not breaths, which is 13.6 %. The paper's "approximately 10% (43/408)" divides by all pauses over 150 ms | same, Table 2 |
| 300 ms in spontaneous speech: true positive 99.55 %, false positive 35.06 % | [3] Wang 2012 (full-F) | CONFIRMED | Table: 300 ms, TPR 0.9955, FPR 0.3506, accuracy 0.817, d′ 2.994 | BioC PMC3394888 |
| Parkinson readers 9.2 % against 3.7 %, attached to "breaths at locations unrelated to a syntactic boundary" | [6] Huber 2012 (full-F) | WRONG CONTEXT | 9.2 / 3.7 is "Locations without Punctuation", which was not significant: "No Punctuation: χ2(1) = 2.37, p = .124". The significant effect is "Locations Unrelated to Syntax" 6.3 % against 0.8 %, χ2(1) = 4.38, p = .036. The source file pairs 9.2/3.7 with the wrong test | BioC PMC3804060, table and results |
| 43 speakers, seven octave bands, six variables per band, 84-100 % | [47] Liss 2010 (full-F) | CONFIRMED | "84%–100% classification accuracy"; five-group 84 % (67.4 % cross-validated); control versus dysarthric 100 % (95.3 %) | BioC PMC3738168 |
| Pauses roughly 378-709 ms before, 417-743 ms after, short against long phrases | [53] Krivokapic 2007 (full-F) | CONFIRMED | Table values 378, 709, 417, 743 are extremes across dyads; within a dyad e.g. 414→709, 378→560 | PMC2131696 HTML |
| "none of the metrics could differentiate" | [48] Lowit 2014 (full-F) | CONFIRMED (abstract only) | Sentence is in the PubMed abstract; full text not reached | PubMed efetch |
| 22 studies, 263 effect sizes; r .62, −.59, −.46, −.20, .72, .76; Q(2) = 4.25, p = .119 | [31] Suzuki 2021 | CONFIRMED | Results table matches every value and interval. The included studies are L2, mostly picture narration | Lancaster accepted manuscript PDF |
| Articulation rate +18 %, +13 %, about 0; speaking rate +28 %; Table 2 pause counts and durations | [36] Trouvain & Grice 1999 | CONFIRMED | Table 2 fast: 6,7/646, 6,0/465, 13,3/475 with −23 %/+9 %, −47 %/−13 %, +2 %/−13 % | author PDF |
| Table II: 49.3, 31.7, 37.3, 43.5, 43.6, 44.9 | [49] McIntosh 2026 | CONFIRMED | Rhythm (sentence), ERJ, column r | arXiv PDF |
| Table 8: 0.902, 0.768, 0.281, 0.448; intraclass .798/.681/.283/.721 and .593/.535/.398; adjusted R2 0.6 | [24] Duong 2011 | CONFIRMED | All values present; "for want of a reliable human gold standard" present. No kappa values in the PDF | CMU PDF |
| Silences 57/117/212/403 ms → 12.5/34.4/71.9/93.8 % judged disfluent | [56] Lovgren & van Doorn 2005 | CONFIRMED | Table 3 | ISCA PDF |
| Adjusted R2 0.5917, 0.5449, 0.1583, 0.7825 | [30] Bosker 2013 | CONFIRMED | Model table | MPG PDF |
| 191 ms, d = 1.14; 80 ms matched-word; d = 0.89 | [52] Camara 2026 | CONFIRMED | Abstract; turn-final words | arXiv PDF |
| Breath group 4.05 s (SD 1.5); pause 0.64 s (0.25-1.8); inspiration 0.54 s; 5/273 (1.8 %) | [1] Wang 2010 | CONFIRMED | Verbatim in results | PMC2945274 HTML |
| Correlations .81-.93; rate of speech .90-.93 | [28] Cucchiarini 2000 | CONFIRMED (abstract) | Verbatim | PubMed |
| r = .36 percentage of silence, r = −.24 F0 SD | [11] Laukka via [12] | CONFIRMED as secondary | Teferra 2022 reports exactly these for Laukka's 71 patients | Europe PMC XML |
| Within-clause pauses: [19], [33], [34], [32] | abstracts | CONFIRMED, context missing | All four quotes are verbatim. Tavakoli is picture narration and Suzuki & Kormos argumentative speech; none is stated to be read speech | OpenAlex, Crossref |
| Smaller items: precision 0.87 / recall 0.86 [8]; inbreath 291 (112) and 418 (89) ms [7]; r 0.81/0.73/0.88, 625 ms [43]; 183 wpm, 77 studies, 5,965 participants [27]; ".85" [50]; filled pauses p = 0.013, d = 0.58 [13]; "No consistent acoustic patterns" [14]; last-sentence acceleration [9] | various | CONFIRMED | All present | PDFs, HTML, OpenAlex |

Kahng 2018's DOI, which the report says it could not see, is 10.1017/S0142716417000534.

## 2. disfluency

| Claim | Source | Verdict | What the source says | How checked |
|---|---|---|---|---|
| 80.9 % of errors are insertions; r = .73 part-word, .60 whole-word repetitions | lea2023_chi | CONFIRMED | "80.9% were word insertions"; "(r(39) = .73, p < .001)"; "(r(39) = .60 ...)". Speaker-level, 41 moderate or severe speakers, production recogniser | arXiv PDF |
| Severity bands 0-5 %, 6-20 %, over 20 % | lea2023_chi | CONFIRMED | Verbatim | same |
| Section 4 #1: "miscue recall 0.83" with "precision about 0.5 in children" | gao2024_miscue | WRONG CONTEXT | Table: Wav2Vec2 Large precision 0.29, recall 0.83, F1 0.43. Whisper precision 0.52, recall 0.53, F1 0.52. The 0.5 belongs to Whisper. Section M2 states it correctly | arXiv PDF |
| Event F1 92.8, 71.0 without recogniser, 70.4 forced aligner; "um" 91.0 against "uh" 84.3; candidates 150-400 ms | zhu2022 | CONFIRMED | Tables 1-2 and Sec. 2.2 | arXiv PDF |
| Recall 84.9 % (107/126), precision 91.5 % (107/117); R = 0.034, W = 0.575; threshold 7e^-1; 53.8 % hoarse speaker | goto1999 | CONFIRMED | All present | ISCA PDF |
| Recall 71.43 % at 1.44 %; 92.86 % at 2.36 %; "uh" mean 165 ms, median 180, range 20-1200; 83.72 % adjacent pause | gabrea2000 | CONFIRMED | "165.45 ms ... median of about 180 ms"; "54706 (83.72%) had an adjacent pause"; table rows | ISCA PDF |
| 4.77 %, 2.25 %, 2.32 %, 1.78 %, 0.94 %; 220 ms; 15 % miss at 5 % false alarm; weights "minimum of 1%" | proenca2015 | CONFIRMED | Table and text | ISCA PDF |
| Recall 0.47-0.60, F1 0.52-0.60, F1 loss 17.4 → 3.8 %; UCLASS F1 0.53-0.54; α ≥ 0.9 | kouzelis2023 | CONFIRMED | Table 1 | arXiv PDF |
| Repetition 100 %, deletion 50 %, insertion 12 %; phoneme error 34.13 → 9.95 %; 9.43 → 74.06 at σ 0.1 | guo2025 | CONFIRMED | Tables 1-3; simulated data | arXiv PDF |
| Word repetition 0 % missed at 0.29 % false positives; sound repetition 60 % missed; prompt-only 100 % missed; 63 → 70 %; 0.9 | alharbi2018 | CONFIRMED | Table 2 and text | ISCA PDF |
| F1 55.9/68.5/63.2/60.4/71.3; kappa 0.25 block, 0.11 prolongation | lea2021_sep28k | CONFIRMED | Present | arXiv PDF |
| Kappa 0.37 block, 0.42 prolongation | bayerl2022_ksof | CONFIRMED | Table 2 | arXiv PDF |
| 0.21 % (SD 0.53, max 2) fluent adults reading; 16.84 / 12.91 / 1.47 % adults who stutter | ritto2016 | CONFIRMED | Tables; 17 per group, 200 syllables, Brazilian Portuguese | Europe PMC XML |
| Base rates and durations: 6 per 100 words, 0.18-6.66, 96 %, 6-10 %, about 1 s, 80 / 220 ms | lickley2017 | CONFIRMED | All present | AISV PDF |
| 5.97 per 100 words; "41% increase in fillers" | bortfeld2001 | CONFIRMED | Present | author PDF |
| "under 1% ... 5-10%"; 700 against 40,000; 88 %; 20-50 ms creak | shriberg1999 | CONFIRMED | Present | SRI PDF |
| r = 0.78 with a fluency test | beck2004 | CONFIRMED | "correlated, within-grade, at 0.78 on average" | CMU PDF |
| Whisper MCC .01; forced-decoding confidence r = .45 | molenaar2023 | CONFIRMED | Table and abstract | arXiv PDF |
| Insertions rose more than 13 times | mitra2021 | CONFIRMED | "(>13 times)"; 1.02 against 13.51 | arXiv PDF |
| AUC 0.61 / 0.66 reading, 0.70 / 0.87 monologue; 32 patients | tomisato2024 | CONFIRMED | Table | Europe PMC XML |
| MOS 2.22 against 4.13 | zhou2024 | CONFIRMED | Table 2 | arXiv PDF |
| "61 to 29%"; 8.98 against 2.06 fillers per minute | clark_foxtree2002 | CONFIRMED | Present | Stanford PDF |
| Brown factors; position not significant in oral reading | max2019_loci (W) | CONFIRMED | Quotes verbatim; weights 2.51/2.39 against 1.86/1.81; position t(34) = 0.20, p = 0.84 | PMC11513192 HTML |
| Miscue list and self-correction definition | nguyen2020 (W) | CONFIRMED | Verbatim; Table 1 M = 43.72 / 2.20 | BioC PMC7954224 |
| 59 %, 54 %, 16 % of variance | bosker2013_2014 | CONFIRMED | 0.5917, 0.5449, 0.1583 in the 2013 paper itself, which is openly available | MPG PDF |
| Abstract quotes: Howell 1997, Zebrowski 1994, Buchanan 2014, Christenfeld 1996, Hofmann 1997, Jani 2013, Tichenor 2019 | abstracts | CONFIRMED | Verbatim | PubMed efetch |

## 3. pitch_emphasis

| Claim | Source | Verdict | What the source says | How checked |
|---|---|---|---|---|
| SMD 0.55, not significant after trim-and-fill (0.17) | veiga_2025 (tool summary) | CONFIRMED | "SMD = 0.5504, 95% CI [0.3014, 0.7995]"; I2 = 69.2 %; "SMD = 0.1710; 95% CI: −0.1472 to 0.4891; p = 0.2923" | Europe PMC XML PMC12531429 |
| PVQ below .15 "monotone side"; r = .83; .70 men, .64 women; ranges .06-.34 and .11-.24; 18 speakers, 8 raters | hincks_2005 | CONFIRMED | All present | ISCA PDF |
| 80-percentile range .52 (women .71, men .62); SD .35; SD/mean .02; max-min .04; kurtosis −.43; skewness −.42 | niebuhr_skarnitzl_2019 | CONFIRMED | Table 2 row by row; N = 51, 42 listeners, 40-98 s | ICPhS PDF |
| "monotonous" −.91; range .61; interquartile range 2.44-8.78 st, median 4.7; 498 speakers 2-5 st; focus F0 max .87 / .76 | strangert_gustafson_2008 | CONFIRMED | Present | ISCA PDF |
| r .337 / .351 with 82 native readings; .335 / .328 best single; model .365-.368 against human .529 / .42 | wang_evanini_yoon_2015 | CONFIRMED | Tables 3 and 5 (China set). "1-best" is the best-matching of 82 natives, not an arbitrary single reference | ISCA PDF |
| Sentence-boundary words r about .27-.28 | same | CONFIRMED (India set only) | India 0.27 / 0.282; China 0.261 / 0.255 | Table 4 |
| "pitch match and sentence-final pitch change predicted fluency and comprehension in 109 children" | chung_bidelman_2022 | WRONG CONTEXT | Mandarin-speaking Taiwanese third-graders. Sentence-final pitch change explained 6.5 % of reading rate only: it "did not explain significant variance in reading accuracy" and "did not explain significant variance in reading comprehension in Grades 3 and 4". Pitch match predicted rate (3.4 %), accuracy and comprehension | lab PDF, results and discussion |
| Pitch correlation raised adjusted R2 from .652 to .674; "factor out ... baseline F0"; undefined values penalised | duong_mostow_2011 | CONFIRMED | Table 11 (posttest comprehension); quotes present | CMU PDF |
| 71.5 % negative slopes; 2.68 st/s at 2.0 s, 1.23 at 4.0 s (1.04-2.04 trimmed); 0.51 st per second | yuan_liberman_2014 | CONFIRMED | Present; 5652 utterances | author PDF |
| "45% of floor holding ended in uptalk vs. 16% of statements"; 34 % and 20 %; 5 Hz rule | ritchart_arvaniti_2014 | CONFIRMED | Verbatim | ISCA PDF |
| Boundary tones 54.95 %; accents 82.9 %; 51.2 % accent-bearing; final 200 ms; human about 85 / 91 % | rosenberg_autobi_2010 | CONFIRMED | Present | ISCA PDF |
| 79.2 % raw sum, 84.6 %, 84.0 % unsupervised; f0 80.9, energy 79.5, duration 79.5; majority 54.5 | suni_2015_2017 | CONFIRMED | Table | arXiv PDF |
| Weights 1.0 / 0.5 / 1.0 give 85.3 %; majority per word 80.2 %, BERT 83.2 % | talman_2019 | CONFIRMED | Present | arXiv PDF |
| Accent-ratio threshold 0.38; 75.59 % (majority 58 %); 82 % broadcast news | nenkova_2007 | CONFIRMED | Present | ACL PDF |
| SD/mean 0.134 / 0.142 and 0.142 / 0.146 in L1; 0.119 / 0.13 and 0.118 / 0.133 in L2 | zimmerer_2014 | CONFIRMED | Verbatim | author PDF |
| Prominence similarity 4.19-5.60 %; fluency 11.8 %; "best" native correlation | kallio_2022 | CONFIRMED | Percentages are derived from AIC against the null model in the paper | Europe PMC XML |
| IQR 2.93, st-IQR 2.87, SD 3.62, st-SD 2.72; cleaned SD 8.32, st-SD 6.37, IQR 3.20; "16 readers" | portnova_2025 | CONFIRMED, context missing | Values present. The 16 readers are "Eight speakers with PD and eight neurotypical speakers" | PMC12337113 HTML |
| r = .84 random forest; Fleiss kappa .53 | baumann_winter_2018 | CONFIRMED | Present | accepted manuscript PDF |
| 86.95 %, kappa .61 | kakouros_rasanen_2015 | CONFIRMED | Table | author PDF |
| Duration r = .72 Dutch, .48 French; "F0 .40, energy .35" | kakouros_tilt_2018 | CONFIRMED, ambiguous | .40 / .35 belong to the second corpus; first corpus F0 .56, energy .46 | author PDF |
| Smaller items: kappa .373-.421 and .544-.621 [mo_2008]; 9.3 against 6.9 st [xu_xu_2005]; 40-70 Hz, F1 .57, below 10 % for 9 of 11 [drugman_2014]; wiggliness 0.6-8.07, spaciousness 0.28-14.75 st [wehrle]; 35 % no declination [lieberman_1985]; 15 of 19 studies [schewski_2025] | various | CONFIRMED | All present | PDFs, PubMed |

## 4. volume_clarity

| Claim | Source | Verdict | What the source says | How checked |
|---|---|---|---|---|
| AUC 0.824, 0.988, 0.989 / 0.986 (simulated errors, child speech) | cao2024 | CONFIRMED | Table 1, CMU-Kids. Real errors: 0.796, 0.905, 0.891, 0.915 | ISCA PDF |
| ArtP mean r = 0.71 with text, equal to the best audio-reference method; 0.66 without text | halpern2026pathbench | CONFIRMED | "ArtP and NAD, both achieving r = 0.71"; DArtP 0.66. Table 1 in v2 prints 0.72 for ArtP. Speaker-level, pathological speech | arXiv PDF |
| r = 0.77 with a clinical speech sub-score | talkar2025 | CONFIRMED | "0.77 with the ALSFRS-R speech subscore" | ISCA PDF |
| Leq range about 28 dB; alpha 19.0 / 11.7 dB; alpha = ratio above and below 1000 Hz | sundberg2006 (A) | CONFIRMED | Verbatim | PubMed |
| Mean absolute errors 0.1-0.7 dB | sundberg2006 | CONFIRMED (merged) | "between 0.1 and 0.6 dB" (quadratic); "between 0.2 and 0.7 dB" (linear) | PubMed |
| 5 Hz/dB F0, 3.5 Hz/dB F1; +10 dB gives A1-A3 +11 / 12.4 / 13 | lienard1999 (A) | CONFIRMED | Verbatim | PubMed |
| EE −7.3 dB/s declaratives (R2 0.49); −7.8 and −9.5 in questions; "limited" | nichasaide2015 | CONFIRMED | Table 1 | ICPhS PDF |
| "intensity decay is not a robust symptom" | rosen2005 (A) | CONFIRMED | Verbatim | PubMed |
| Machine and human word recognition "not strongly correlated"; "one-to-one proxy"; ceiling; 52 ALS, 20 controls | gutz2022 (A) | CONFIRMED | Verbatim | PubMed |
| P-ESTOI R = 0.95 (CP, English) and 0.95 (ALS, French); 15 bands, 15 frames; gender-specific references | janbakhshi2019 | CONFIRMED | Speaker-level; P-STOI 0.90 and 0.87 | Idiap PDF |
| r = −0.87 against −0.71 MFCC; −0.34 MFCC on second dataset; reference and device statements | bartelds2022 | CONFIRMED | Table: w2v2-en −0.87 / −0.71; MFCC −0.71 / −0.34 | arXiv PDF |
| 50 speakers; level "intentionally removed"; mel-spectrogram 64 ± 2 %; +5 % | kodali2023 | CONFIRMED | Present | ISCA PDF |
| WavLM-Base 78.2 % non-calibrated | omidi2026 | CONFIRMED | Abstract | arXiv PDF |
| Slopes −6.71, −8.29, −8.27, −7.51; 12 speakers; AGC sentence | zhang_hansen2007 | CONFIRMED | Table 1 | ISCA PDF |
| Vowel centre of gravity 916 → 1204 Hz; obstruents less affected; energy ratio worst | harwardt2011 | CONFIRMED | 916.068 → 1203.671; "the energy ratio seems to be worst" | ISCA PDF |
| Entropy and confidence correlate 0.76-0.79, LibriSpeech ensemble | tu2022 | CONFIRMED | Table 1, LibriSpeech rows: normalised cross-correlation 0.762 and 0.788; Kendall 0.572 / 0.595 | arXiv PDF |
| Level table 48 / 54 / 60 / 66 / 72 / 78 dB(A) at 1 m | rindel2019 | CONFIRMED | Table 2, "Adapted from Lazarus" | PDF |
| Spectral emphasis definition (1.5 F0, 4th-order Butterworth, L − L0) | eriksson2001, heldner2001 | CONFIRMED | Verbatim | ISCA PDFs |
| Jitter 1.040 %, shimmer 3.810 % | vanpuyvelde2018 | CONFIRMED | "These thresholds are set on 1.040% for jitter and 3.810% for shimmer" | Europe PMC XML PMC6255927 |
| Physical load leads to "inappropriate breathing pause placements" "(Table 2, as extracted)" | vanpuyvelde2018 | CONFIRMED, wrong location | Body text: "When combining exercise with speech ... the occurrence of linguistic inappropriate breathing pause placements". Not Table 2 | same |
| Cut-offs 9.33 dB (Praat) and 6.11 dB (ADSV), Rainbow Passage; 94.5 %; 295 patients, 50 controls | murton2020 (A) | CONFIRMED | Verbatim | PubMed |
| FCR formula; VSA "highly sensitive to interspeaker variability" | sapir2010 | CONFIRMED | Verbatim | BioC PMC2821466 |
| Smaller items: 1-3 kHz energy and word duration predict 61 % [hazan2004]; jitter and shimmer rise below 75 / 80 dB [brockmann2008]; SPL, L/H ratio, HNR [mckenna2018]; same-gender references [lee_glass2012]; greedy against language-model decode [halpern2026asric]; stress F0 pooled result [veiga2025] | various | CONFIRMED | All present | PubMed, PDFs |

## Claims to correct or drop

1. **pace_pauses, Reason L and source file `huber2012`.** Replace "(full-F: 9.2 % against 3.7 %)" after the unrelated-to-syntax quote with 6.3 % against 0.8 %, χ2(1) = 4.38, p = .036. In the summary table keep 9.2 % against 3.7 % as "without punctuation" and add that it was not significant (p = .124).
2. **pace_pauses, section 4 #7.** "About 10 % of such pauses are not breaths" should be 13.6 % (43 of 316 pauses ≥250 ms). The FPR was .319.
3. **pace_pauses, section 3 point 2 and Reason L methods.** "250 ms was the most accurate of 150-350" follows the paper's text, but its Table 2 gives accuracy .922 at 300 ms and .914 at 350 ms against .895 at 250 ms. 250 ms is best by d′ only. The spontaneous-speech paper shows the same thing (350 ms accuracy 0.854 against 0.817 at 300 ms).
4. **pace_pauses, Reason J.** "at commas (R2 = .328)" should read: complex-adjective comma .328, phrase-final comma .144.
5. **pace_pauses, open question 9.** Close the sample-size item: the body says 120 children and 34 adults (4 excluded); the abstract says 123 and 24.
6. **pace_pauses, section 4 #1.** State that the within-clause pause evidence [19, 32, 33, 34] and the meta-analysis [31] are L2 speech, mostly picture narration or argumentative speech, not read text. The numbers stand.
7. **pace_pauses, minor.** Moers [18] has three age groups (8-12, 12-18, 62-95), not a continuous "8 to 95". Add the Kahng DOI.
8. **disfluency, section 4 #1.** Replace "precision about 0.5 in children" with: at recall 0.83 the wav2vec 2.0 model had precision 0.29 (F1 0.43); 0.52 is Whisper at recall 0.53.
9. **disfluency, bosker2013_2014.** Status can be raised to full text: the 2013 paper is at pure.mpg.de and contains the three R2 values.
10. **pitch_emphasis, Reason P-D.** Rewrite the Chung & Bidelman sentence: Mandarin-speaking children; pitch match predicted reading rate, accuracy and comprehension; sentence-final pitch change predicted reading rate only (6.5 %), not accuracy or comprehension.
11. **pitch_emphasis, section 2.3 methods.** ".27-.28" is the India set; China is .26 / .255.
12. **pitch_emphasis, portnova_2025.** Add that 8 of the 16 readers have Parkinson's disease.
13. **pitch_emphasis, cue weights.** For Kakouros 2018, say that F0 .40 / energy .35 belong to the second corpus (first corpus .56 / .46).
14. **volume_clarity, 2.1.** Alpha errors: 0.1-0.6 dB quadratic, 0.2-0.7 dB linear.
15. **volume_clarity, 2.2.** The Van Puyvelde breathing statement is body text about exercise combined with speech, not "Table 2".

## Candidate measures whose support did not hold up

- **pitch_emphasis, sentence-final pitch change (rank 4 / 3).** The first cited source, Chung & Bidelman 2022, found no relation of this measure to reading accuracy or comprehension, in a tone language. Its English support is secondary: four Schwanenflugel-group studies quoted in that paper's introduction, not opened. Remaining direct support is Ritchart & Arvaniti (pattern only), AuToBI (54.95 % five-way) and Wang et al. (r about .26-.28).
- **disfluency, inserted material count (#1).** The measure stands, but its precision evidence is weaker than stated: 0.29 for the wav2vec 2.0 model nearest the project's decoder, not about 0.5.
- **pace_pauses, breath-pause location (#7).** The Parkinson contrast used as pattern evidence is 6.3 % against 0.8 %, not 9.2 % against 3.7 %. The 250 ms threshold is not the most accurate by the paper's own accuracy column, and 13.6 % of such pauses are not breaths.
- **pace_pauses, within-phrase pause count (#1) and mean length of run (#4).** Numbers confirmed, but the validation population is L2 spontaneous speech; "strong" applies to that population, not to read speech.
- All other top-five measures in the four reports: the cited numbers and definitions were confirmed as stated.

## Read-status honesty

- pace_pauses: 10 of the 11 "full-F" sources were re-read in primary text. The fetched passages were accurate except the Huber statistic pairing. Lowit [48] was checked on its abstract only.
- pitch_emphasis: the Veiga numbers returned by the fetch tool are exact.
- disfluency: the two "W" papers (Max 2019, Nguyen 2020) are verbatim-accurate.
- volume_clarity: the `vanpuyvelde2018` passages relied on are correct despite the interleaved columns.

## Not checked

- pace_pauses: Lowit 2014 full text; NAEP scale wording [23]; Zvonik & Cummins [54]; Tanaka [57]; Janse [37] quotes; Sabu & Rao secondary 0.794 [26]; abstract quotes of [4, 5, 9, 16, 25, 35, 38-40, 42, 45, 46, 51, 55] beyond the keyword hits listed above; the seven-syllable sentence detail of [41].
- disfluency: torchaudio tutorial (W); Bayerl wav2vec 2.0 figures beyond locating them in the table; Harvill, Kourkounakis, Lian (edit recipes); Sandoval 2025 VR numbers; Han 2026 and Tomisato quotes; Kasl & Mahl secondary; Wagner, Smith, Pratap, Gao OTC, Tam, Mostow beyond one quote; de Jong 2021, Shriberg 2001, Laukka abstracts.
- pitch_emphasis: Busà & Urbani, Patterson & Ladd, De Looze & Hirst, Lindh & Eriksson, Mertens, Hincks & Edlund, Arvaniti & Godjevac, Ferrer, Morrison, Wang & Narayanan 2007 (862 / 768 / 3247), Kaland, Scherer, Low 2020, Vogel 2010, Baird 2020; all `abstracts_openalex` items (Traunmüller, Mennen, Breen, Kochanski, Kang, Cole, Chen, Miller & Schwanenflugel 2008, Anderson, Linneman, Paunović, 't Hart); the report's own derived conversions.
- volume_clarity: Sandoval 2013 (0.78, 12 centres, 15 %) — PMC returned a captcha and the PubMed abstract lacks the numbers; Hunter 2021; Fletcher, Lansford, Thompson variance figures; Abur 2026 content (existence confirmed); Smiljanic 2009, Ernestus & Warner, Yun 2020, Keating 2015, Drugman quotes; Parikh papers; Janbakhshi 2020; Sun 2026 quotes; Brückl 2012; about 35 of the 46 PubMed abstracts; the 7 OpenAlex-reconstructed abstracts.
