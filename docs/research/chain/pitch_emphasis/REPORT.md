# Chain research: pitch variation, emphasis, sentence endings (2026-10-02)

> **Corrections after the citation check (`../VERIFICATION.md`, 2026-10-02).** (1) Chung & Bidelman 2022 studied Mandarin-speaking
> children; pitch match predicted reading rate, accuracy and comprehension, but sentence-final pitch change predicted reading rate
> only (6.5 %), not accuracy or comprehension. The sentence-final measure (rank 4 / 3) therefore has weaker support than stated: its
> English support is secondary. (2) The r of about .27-.28 for sentence-boundary words is the India set; the China set is .26 / .255.
> (3) Portnova 2025: 8 of the 16 readers have Parkinson's disease. (4) Kakouros 2018: F0 .40 / energy .35 belong to the second corpus
> (first corpus .56 / .46). The Veiga 2025 numbers were confirmed against the full text.

Scope: literature only. Every source cited here was opened in this session; the passages relied on are in `sources/<key>.txt`
(key given in square brackets). READ STATUS per source is in section 6. "Derived" marks arithmetic done here, "proposal" marks an
idea of this report with no source. Earlier research is referred to as `PAPERS.md #n`; those sources were not re-opened unless listed.

## 1. Summary table

| Flaw | Reason | Pattern left in the signal | Best detection method(s) found | Computable now? | Training? | Evidence |
|---|---|---|---|---|---|---|
| Pitch variation | P-A second-language speaker, "insecurity", attention on segments | Whole-passage span compressed (SD/mean 0.134-0.146 in L1 reading, 0.118-0.133 in L2); level sometimes raised | Whole-clip percentile span in semitones against a between-speaker norm (80-percentile range; PVQ) | yes | no | moderate (two read-speech studies, small group effect) |
| Pitch variation | P-B nervousness, stress | Pitch LEVEL raised (15 of 19 studies); variability direction inconsistent; more pause time; jitter/shimmer mixed | Level against the speaker's own baseline only; no cross-speaker measure found | no (needs own baseline) | no | weak for "monotone", moderate for level |
| Pitch variation | P-C low arousal, sadness, depression; fatigue | Lower level and narrower range; slower. Fatigue: F0 variation INCREASED after 16-24 h awake | Same span measure plus rate; not separable from P-A by pitch alone | yes | no | moderate (reviews); fatigue contradictory |
| Pitch variation | P-D unskilled or unengaged reading | Contour does not follow a skilled reading of the same text; smaller sentence-final fall | "Pitch match": correlation of word-level F0 values with the reference reading | yes | no | strong for children and L2 readers (r 0.34-0.39 with human intonation scores) |
| Pitch variation | P-E sing-song, same contour each sentence | Span normal or wide, shape repeats; long-term distribution identical to a lively reading | Wiggliness + spaciousness; contour self-similarity between phrases (DTW on first derivative) | yes (phrases from pauses/punctuation) | no | weak (measures exist, none validated for repetitiveness) |
| Pitch variation | P-F range present, not placed on the right words | Long-term span normal, low agreement with reference contour and with content words | Pitch match (P-D) plus emphasis measures | yes | no | moderate |
| Emphasis | E-A no focus marking (disengaged or low-skill reading, low proficiency) | "prominence variation pattern is more flat"; focused word lacks higher F0 peak, longer stressed syllable, higher intensity; no post-focus lowering | Correlation of per-word prominence vector with reference; spread of prominence scores | yes | no | moderate (small effect: 4-6 % of rating variance) |
| Emphasis | E-B every word stressed alike (L2 transfer) | Unstressed words with higher F0 and intensity; several primary stresses per word | Spread of prominence; content-minus-function prominence gap | yes | no | moderate |
| Emphasis | E-C stress on the wrong word (given or function word) | Prominence peak where the reference has none and the word has a low accent probability | Two-sided mismatch with reference; function-word list or accent-ratio dictionary | yes (list); dictionary needs a labelled corpus | no | moderate |
| Emphasis | E-D one cue only (e.g. pitch without length) | Stressed words higher F0 but shorter than native | Per-cue comparison instead of the mean of three | yes | no | weak (abstract) |
| Endings | N-A uptalk (floor holding, uncertainty, habit, L2) | Rise on the last word of a statement, starting late (often after the stressed vowel) | Final-word F0 slope or excursion versus reference; AuToBI final-200 ms features | yes (rule) | rule: no; AuToBI: yes | moderate for the pattern, weak for automatic accuracy (55 %) |
| Endings | N-B unskilled reading | Smaller sentence-final pitch fall in declaratives | Max minus min of the last fall on the sentence-final word, against reference | yes | no | moderate (children) |
| Endings | N-C no declination / no final lowering | Per-sentence regression slope near zero or positive (broadcast English: 71.5 % negative, 1.2-2.7 st/s) | All-points regression slope per sentence in st/s | yes | no | moderate |
| Endings | N-D trailing into creak | F0 40-70 Hz or irregular pulses at phrase end; rated less competent | Trained creak detector; cheap proxy = unvoiced or sub-70 Hz frames while level is above the pause floor | proxy only | detector: yes | weak for the proxy |

## 2. Flaws, reasons, patterns, methods

### 2.1 Pitch variation ("monotone")

**What listeners call monotone, and which measure predicted it.**
- [hincks_2005] PVQ = SD of F0 / mean F0 over 10 s. 18 Swedish students presenting in English, 8 raters: per-speaker r = .83 with
  liveliness; per-sample r = .70 (men), .64 (women). "Speech samples with PVQ values less than .15 were generally rated as on the
  monotone side". Range of 10 s samples .06 to .34; whole-presentation means .11 to .24. This is a published numeric cut-off, so the
  statement in `rubric_explain/REPORT.md` that no primary source gives one is no longer correct. Limits: 18 speakers, hand-cleaned
  pitch tracks, Hz-based, values changed with the tracker's floor and ceiling (sec 4.2), and proficient speakers "could be perceived
  as lively even when the PVQs were low".
- [niebuhr_skarnitzl_2019] 51 speakers, 40-98 s excerpts, 42 listeners, uncorrected Praat tracks. Correlation with charisma rating:
  80-percentile range (P90-P10) .52 (women .71, men .62); SD .35; SD/mean .02; max-min .04; kurtosis -.43; skewness -.42.
  "the traditional f0-range measure ... shows no correlation ... not very robust against typical octave errors". Recommendation:
  "use the 80-percentile range, perhaps along with kurtosis"; "kurtosis might need a longer stretch of speech".
- [strangert_gustafson_2008] "monotonous" r = -.91 with good-speaker rating; F0 range in st r = .61; interquartile range 2.44 to 8.78 st
  across 16 speakers (median 4.7); 498 ordinary speakers reading prompts: 2-5 st. "F0 dynamics is primarily associated with the
  extent to which the range is widened upwards".
- [abstracts_openalex: traunmuller_1995] listeners "judged F0 intervals to be equivalent if they were equal in semitones" across
  men, women and children; liveliness "strongly dependent on articulation rate".
- [portnova_2025] 16 readers, 80 sentences, 20 listeners rating expressiveness. With tracking errors left in: F0 range and relative
  range not significant; IQR 2.93, semitone IQR 2.87, SD 3.62, semitone SD 2.72 (% of scale per 1 SD). With errors removed: SD 8.32,
  semitone SD 6.37, IQR 3.20. "IQR measures were found to be more robust to outliers ... [but] had only a moderate relationship
  with listeners' perceptions". Tracking errors inflate SD by "over 2 Hz" on average.
- [patterson_ladd_1999] 32 speakers, 48 listeners: a span measured at linguistic landmarks (mean accent peak minus mean post-accent
  valley) "is far more successful in capturing the differences between listener judges' ratings" than +/-2 SD, P95-P5 or P90-P10.
  [abstracts_openalex: mennen_2012] same direction: effect sizes "larger ... for linguistic than for LTD measures".
- [wehrle_2018_2020] a slow monotonic rise and a repeated up-down contour over the same range "yield exactly the same result in an
  analysis of LTD measures". Long-term distributions cannot separate robotic from sing-song.

**Reason P-A: second-language speaker.** [zimmerer_2014] read sentences and stories in L1 and L2: mean SD/mean French L1 0.134 /
0.142, L2 0.119 / 0.13; German L1 0.142 / 0.146, L2 0.118 / 0.133; L1 > L2 significant; proficiency level not significant.
Explanation offered as speculation: "a factor of insecurity ... because they concentrate on other aspects, such as the correct
pronunciation of segments". [busa_urbani_2011] 18 Italian vs 18 American readers of 5 sentences: span difference significant only
for the 90 % range (p < .05), not for 80 % or 100 %; sentence type highly significant for every span measure. [hincks_2005] cites
Pickering: "an overall narrower pitch range, which made the identification of prosodic units difficult" (secondary).
[abstracts_openalex: kang_2010] suprasegmental measures together "accounted for 50% of the variance in oral proficiency and
comprehensibility ratings" (26 samples).
Pattern: uniform, whole-passage compression of about 10-15 % in SD/mean; not local.
Derived: SD/mean 0.15 is about 2.6 st SD (17.31 x CV) and about 6.7 st P90-P10 under a normal distribution; the L1 reading values
of [zimmerer_2014] (0.134-0.146) sit below Hincks' presentation cut-off, so that cut-off does not transfer to read passages.

**Reason P-B: nervousness.** [hincks_2005] asserts it without data ("It is likely that affect—nervousness—is a large reason").
The measured pattern is different: [stress_anxiety_fatigue: schewski_2025] "fifteen out of nineteen studies reported a significant
increase in mean F0"; for anxiety "findings on fundamental frequency (F0) were mixed", with "decreased intensity and increased
pause duration"; jitter and shimmer under stress "inconsistent". [low_2020] social and generalised anxiety: increased mean F0,
higher jitter and shimmer. [laukka_2008, abstract] after treatment of social phobics, mean and maximum pitch, high-frequency energy
and proportion of silent pauses fell with state anxiety and with perceived nervousness. [veiga_2025] pooled rise of mean F0
SMD 0.55, not significant after trim-and-fill (0.17). [baird_2020] sustained vowels only: within-vowel F0 SD 2.45 vs 3.03 Hz
(women, low vs high anxiety). No opened source shows that nervousness narrows pitch range in read speech.
Pattern: raised level, more pause time; range unchanged or wider. Differs from P-A/P-C, where range narrows.

**Reason P-C: low arousal.** [low_2020] "A decrease in f0 and f0 range in depressed individuals has repeatedly been observed ...
reflects the monotonous speech often seen in depression". [scherer_2003] in cue-manipulation studies "F0 range effected the
judgments the most, with narrow F0 range signaling sadness ... slow speech judged as a mark of sadness". Fatigue does not fit:
[vogel_2010] 18 adults, read passage included, "Between 16 – 24 hours post-baseline assessments, f0 variation was significantly
greater than baseline", against earlier perceptual reports of "monotonic or flattened voices".
Pattern: lower level + narrower range + slower rate together; P-A has narrower range with level unchanged or higher.

**Reason P-D: unskilled or unengaged reading.** Read speech as such is not flat: in [lieberman_1985, abstract] it is the
spontaneous sentences that vary ("35% of the spontaneous sentences did not show declination"). The flaw belongs to the reader.
[duong_mostow_2011] "the more expressive a child's reading of a text, the more its prosody tends to resemble fluent adult reading
of the same text"; "F0 match (correlation to adult intonational contour) and the number of pausal intrusions were the best
indicators"; adults reading the same text showed "extremely high correlation ... even across regions" (personal communication
reported there). [abstracts_openalex: miller_schwanenflugel_2008] "early acquisition of an adult-like intonation contour predicted
better comprehension later". [chung_bidelman_2022] pitch match and sentence-final pitch change predicted fluency and comprehension
in 109 children. [wang_evanini_yoon_2015] the same idea for adult L2 readers: "fluent non-native speakers tend to use F0 contours
that resemble the prosody of native speakers' readings of the same text".
Pattern: movement present or absent, but not where the skilled reading has it.

**Reason P-E: repeated contour.** [hincks_2005] "Lively speakers should also avoid following one intonational pattern utterance
after utterance"; a search for "repetitive pitch contours" was planned and not built. [wehrle_2018_2020] sing-song = "lively and
repeatedly spanning a large range". No study measuring repetition between sentences in human read speech was found.

**Methods for these patterns.**
1. *80-percentile range / percentile span* (forensic and charisma literature). P90-P10 of F0; [niebuhr_skarnitzl_2019] on 40-98 s.
   No training. Confounds: speaker (IQR 2.4-8.8 st between speakers, [strangert_gustafson_2008]), sex-specific tracker range, text
   ([busa_urbani_2011] sentence type; [zimmerer_2014] stories > sentences), creak ("could also exaggerate the F0 variation").
2. *PVQ / pitch dynamism quotient* (L2 presentation feedback). SD/mean over 10 s; cut-off .15 [hincks_2005]. Semitone SD over a
   moving 10 s window [hincks_edlund_2009]: "The standard deviation will decrease [sic] with increasing amounts of data, but if the
   amount of data under analysis is constant, it will reflect differing amounts of variation". Sensitive to tracking errors
   [portnova_2025].
3. *Pitch match / template model* (reading-fluency assessment, language testing). One F0 value per word (mean over the word),
   Pearson correlation with the same words of a reference reading. [duong_mostow_2011]: "an elegant way to normalize ... factor out
   differences ... in baseline F0"; words with undefined values are dropped and the score penalised by the proportion undefined;
   pitch correlation raised adjusted R2 for comprehension from .652 to .674. [wang_evanini_yoon_2015]: speaker z-scored F0, three
   word measures (mean; difference to neighbours; regression slope); r with human "intonation and stress" score .337-.351 with an
   average of 82 native readings, .335/.328 with the single best-matching native; full model .365-.368 against human-human
   .529/.42. "the feature performance fluctuates substantially when fewer than 10-20 speakers ... are used in the model". No
   training beyond the reference readings.
4. *Wiggliness and spaciousness* (autism prosody). Contour smoothed, stylised at 2 st; wiggliness = turning points per second;
   spaciousness = mean of the two largest excursions in st, per inter-pause unit of at least 1 s. German dialogue: wiggliness 0.6-8.07
   (mean 3.22, SD 1.02), spaciousness 0.28-14.75 st [wehrle_2018_2020]. Parameters "not ... theoretically motivated". Tracks were
   hand-corrected. Not validated against monotony ratings.
5. *Contour similarity and clustering* (intonation description). Time-normalised F0 vectors, Euclidean distance, complete-linkage
   clustering [kaland_2021_2023]; against listeners "dynamic time warping applied to the first derivative of the contour
   performing best", agreement "moderate" (abstract). Would give a repetition index (mean similarity between sentence contours);
   that use is a proposal.
6. *Speaker normalisation.* Semitones equalise intervals across sexes [traunmuller_1995]. Median-centred octave scale: "lower range
   ... half an octave below the median ... upper range ... between half an octave and one octave above" [delooze_hirst_2014].
   Percentile baseline (7.64th percentile) is the level measure least affected by style, vocal effort and channel
   [lindh_eriksson_2007]. Speaker z-scores before contour comparison [wang_evanini_yoon_2015].
7. *Perceptual floors.* JND for pitch distance 1.5-2 st, "only differences of more than 3 semitones play a part in communicative
   situations" ['t Hart, abstracts_openalex]; glissando threshold G = 0.16/T^2 st/s [mertens_2004]; "over 100 ms ... to raise or
   lower pitch by just 2 semitones" [xu_xu_2005, secondary].

### 2.2 Emphasis

**How emphasis is realised (information-structure literature).** [xu_xu_2005] 8 speakers: "a narrow focus is realized by expanding
the pitch range of the on-focus stressed syllables, suppressing the pitch range of postfocus syllables, and leaving the pitch range
of prefocus syllables largely intact"; peak 9.3 vs 6.9 st in final position; stressed syllable longer; faster rise.
[abstracts_openalex: breen_2010] focus marked by "greater intensity, longer duration, and higher mean and maximum F0"; contrastive
focus by "greater intensity, longer duration, and lower mean and maximum F0" than non-contrastive. [strangert_gustafson_2008] mean
F0 maximum of focused words correlated with good-speaker rating r = .87 (women), .76 (men); number of focused words r = .47 (n.s.).
[abstracts_openalex: schwanenflugel_2015] fluent third-grade readers marked contrastive words "with a higher pitch" and "greater
intensity".

**Reasons and patterns.**
- E-A no marking. [kallio_2022] L2 readers of one narrative, 7 native reference readers, 19-20 raters: "for the less proficient
  speaker (A1), the overall prominence variation pattern is more flat and less similar to the native realization".
- E-B all alike. [ferrer_2015] Japanese learners: "syllables are more similar in prominence than in English"; learners "pronounce
  most syllables with more prominence than native English speakers would"; "around one third of the incorrectly stressed words have
  primary stress in at least two syllables". [abstracts_openalex: chen_2001] Mandarin speakers: unstressed words with "a higher F0
  and greater intensity".
- E-C wrong word. [nenkova_2007] "content words are much more likely to be accented than function words"; given entities "need not
  be prominent". [wang_narayanan_2007] of 862 prominent words 768 were content words. No opened source gives the rate of misplaced
  stress in adult read speech (PAPERS.md #7 Hahn covers the listener cost, not re-opened).
- E-D single cue. [chen_2001] stressed words "significantly higher F0 and shorter duration" than native speakers.

**Methods: prominence from the signal.**

| Method (field) | Definition | Validation | Training | Note |
|---|---|---|---|---|
| Equal-weight z-sum, word maximum (baseline in [suni_2015_2017]) | F0, energy, duration each z-scored per utterance, summed, word max | 79.2 % accuracy, BURNC read news (majority 54.5 %) | none | Closest to the product's stress point |
| CWT + lines of maximum amplitude [suni_2015_2017; talman_2019] | Same composite, Mexican-hat wavelet at half-octave scales, strongest peak line per word | 84.6 % (f0+en+dur), 84.0 % fully unsupervised; f0 alone 80.9, energy 79.5, duration 79.5; tuned weights 1.0/0.5/1.0 (F0/energy/duration) give 85.3 % | none (threshold) | Open toolkit; gain over the raw sum about 5 points |
| Predictability of prosody [kakouros_rasanen_2015] | n-gram over quantised F0 and energy; low-probability words are prominent | 86.95 %, Fleiss kappa .61 vs 20 annotators (Dutch); F0 86.2, energy 86.2, duration lower | unlabeled speech corpus | Not usable without a corpus |
| Acoustic score, equal weights [wang_narayanan_2007] | Syllable duration, pitch-plateau shape, spectral intensity | 76.8 % (dialogs); content vs function separation significant | optional | Equal weights are their "no prior knowledge" option |
| Supervised: AuToBI [rosenberg_autobi_2010], lexical stress GMM [ferrer_2015], CNN [morrison_2024] | trained classifiers | accent detection 82.9 %; stress error 11 % native, 20 % L2; CNN beats wavelet baseline | yes | Outside the constraints |

**Cue weights.** The sources disagree, by corpus and by what was labelled. [abstracts_openalex: kochanski_2005] "f0 played a minor
role ... speakers primarily marked prominence with patterns of loudness and duration" (452 ms windows, British dialects).
[baumann_winter_2018] German read sentences, random forest (r = .84 with listener scores): accent presence, position and type far
ahead; among continuous cues "RMS AMPLITUDE, MEAN F0, MAXIMUM F0 and SPECTRAL TILT (H1-A3) were the most important ... duration
... relatively less important". [kakouros_tilt_2018] duration best (class separation r = .72 Dutch, .48 French; F0 .40, energy
.35); "tilt is a systematic correlate of prominence in Dutch ... energy, F0, and duration appear still to be the most robust".
[suni_2015_2017] on read news the three cues are within 1.4 points of each other and equal weights lose about 0.7 points to the
tuned weights reported in [talman_2019]. [ferrer_2015] for lexical stress: MFCC posteriors, then duration, energy, pitch, "and
finally, spectral tilt".
Reading: PAPERS.md departure 3 (pitch is the weakest cue, spectral balance missing) rests on one conversational-dialect study;
for read English the opened evidence does not support down-weighting pitch, and spectral tilt ranks last or adds little in three
of four sources. Equal weights are defensible; the gain to expect from tuning is about one point.
Within-word descriptor: "measures of dispersion, such as the SD and range, enable a better characterization ... min and max alone
cannot capture dynamic properties ... and might also lack in robustness" [kakouros_tilt_2018]. The product uses P90 (a maximum-type
descriptor) for pitch and level.
Ceiling: listener agreement on prominence is limited. Fleiss kappa .373-.421 (boundaries .544-.621) [mo_2008]; .53
[baumann_winter_2018]; Cohen kappa .226 for crowd annotators [morrison_2024]; trained labellers 84 % [wang_narayanan_2007], ~91 %
for accent presence [rosenberg_autobi_2010].

**Methods: which words should carry emphasis.**
- From a reference reading (template). Per-syllable or per-word prominence vector correlated with native readings of the same
  sentence; "using the 'best' correlation with a native speaker yielded the best results" over the mean of natives [kallio_2022].
  Effect: prominence similarity alone explains 4.19-5.60 % of rating variance, fluency measures 11.8 %, both 12.4 %. Best cue
  combination depends on the speaker's first language. For F0 the opposite holds: the average of many natives beats the best
  single one [wang_evanini_yoon_2015]. In both, one reference reader is the weak configuration.
- From text, no reference. Word-identity prior: accent ratio = share of a word's tokens that were accented in a labelled corpus,
  if significantly different from 0.5; threshold 0.38; 75.59 % on Switchboard (majority 58 %), 82 % on read broadcast news with a
  dictionary built from conversation [nenkova_2007]. "Majority class per word" 80.2 % against BERT 83.2 % on audiobooks
  (automatic labels) [talman_2019]. Human-marked "words ... expected to be emphasized", transitions and list items in the prompt
  [wang_evanini_yoon_2015]. Word frequency and repetition also raise perceived prominence independent of acoustics
  [abstracts_openalex: cole_2010].
- Expected density. 51.2 % of words accent-bearing in one corpus [rosenberg_autobi_2010]; 42 % accented in Switchboard
  [nenkova_2007]; 26.5 % (862 of 3247) marked prominent by labellers in dialogs [wang_narayanan_2007]. A reading with far fewer
  or far more prominent words than these, and than the reference, is the E-A or E-B pattern (proposal; no cut-off published).

### 2.3 Sentence endings

**Reasons and patterns.**
- N-A uptalk. [ritchart_arvaniti_2014] 23 speakers: statements with uptalk show "a smaller pitch excursion and a later rise that
  often started after vowel offset" than questions (L* L-H% vs L* H-H%); "45% of floor holding ended in uptalk vs. 16% of
  statements"; 34 % of map-task and 20 % of retell utterances. [abstracts_openalex: linneman_2013] 37 % of quiz answers.
  [paunovic_2022, abstract] in L2 academic speech uptalk is "a phonetically distinct signal, characterized by a larger pitch
  excursion, a steeper rise slope, a higher rise peak, and a longer post-IU pause" than the other rises; it is "still attributed
  to learners' inadequate mastery of intonation". Listener effect: PAPERS.md (Guyer et al.) falling endings signal confidence,
  not re-opened.
- N-B unskilled reading. Fluent readers show "larger sentence-final pitch change in declarative sentences"
  [chung_bidelman_2022, summarising four Schwanenflugel-group studies].
- N-C declination and final lowering. [yuan_liberman_2014] professional read news, 5652 utterances of 1-4 s: "only 71.5% of the
  phrases in English have a negative slope"; mean slope magnitude 2.68 st/s at 2.0 s falling to 1.23 st/s at 4.0 s (1.04-2.04
  excluding the first and last 500 ms); "The shorter the utterance, the steeper the slope"; initial peak rises 0.51 st per second
  of utterance length; final low independent of length. [arvaniti_godjevac_2003] "final lowering is independent of declination";
  size "not consistent across speakers". [lieberman_1985] 35 % of spontaneous sentences showed no declination.
- N-D creak. [drugman_2014] "frequently used as a phrase-boundary marker"; F0 "typically ranging from 40-70 Hz"; under 10 % of
  speech for 9 of 11 speakers. [abstracts_openalex: anderson_2014] fry voices "perceived as less competent, less educated, less
  trustworthy". Creak also damages the pitch track: irregular periodicity brings halved values and tracking errors [portnova_2025].
- Confound: continuation and listing rises are separate, normal categories [paunovic_2022], so only sentence-final positions of
  statements can be judged, and questions must be excluded by punctuation.

**Methods.**
- *Sentence-final pitch change* (reading research): "differences between maximum and minimum fundamental frequency ... around
  sentence-final words ... the last falling pattern"; mean over the first five declaratives [chung_bidelman_2022]. In Hz there;
  semitones needed across speakers.
- *Rise scaling and alignment* (uptalk phonetics): rise start = first point where "successive F0 values differed by more than 5 Hz";
  excursion = peak minus start; alignment = start relative to onset of the last stressed vowel [ritchart_arvaniti_2014]. Manual in
  the paper; numeric excursions only in figures.
- *Boundary-tone classification* (ToBI): features "from the final 200ms of phrase final words" (min, max, mean, SD, z-score of
  pitch and intensity and slopes); five-way tone classification 54.95 % against human agreement of about 85 %
  [rosenberg_autobi_2010]. A two-way rise/fall decision is easier than five-way; no accuracy for it was found.
- *Word-level slope at sentence boundaries* (language testing): features restricted to sentence-boundary words, correlated with the
  native model, r about .27-.28 with human scores [wang_evanini_yoon_2015, Table 4].
- *Declination slope*: least-squares line through all F0 points of the utterance, st re the speaker's 5th percentile
  [yuan_liberman_2014]; "all-points linear regression line was a better descriptor ... than either baselines or toplines"
  [lieberman_1985].
- *Creak detection*: H2-H1, residual peak prominence and related features into a trained tree or network, F1 per speaker down to
  .57 [drugman_2014].

## 3. Coverage of the current product, pattern by pattern

| Pattern | Status | Why |
|---|---|---|
| Local stretch flattened toward its median | covered | P90-P10 over five words, ratio to reference, relative to the clip's own median ratio |
| Whole passage narrow (P-A, P-C) | partly | Whole-clip median ratio exists; it is judged against six readers, not a published norm; the L2 effect (10-15 %) is small against between-reader differences (IQR 2.4-8.8 st) |
| Raised level from nervousness (P-B) | missed, by design | Median-centring removes level; no own-baseline recording |
| Contour not following the reference (P-D, P-F) | missed | Range is compared, shape and placement are not; a reading with normal range on the wrong words passes |
| Same contour every sentence (P-E) | missed | No between-sentence comparison; no turning-point measure |
| Narrow range with normal local movement vs wide range without placement | missed | Both collapse into one percentile range |
| Reference-stressed word loses stress (one word shortened, flattened, attenuated) | covered | Same-recording comparison only |
| Emphasis for a different speaker | missed | Judged only when participant and reference are the same recording |
| No emphasis anywhere / everything equal (E-A, E-B) | missed | No measure of the spread of stress points |
| Stress on a word the reference does not stress (E-C) | missed | One-sided check (losses only) |
| One-cue emphasis (E-D) | missed | Mean of three z-scores hides which cue is absent |
| Post-focus lowering | missed | Not measured |
| Rising endings, weak final fall, flat sentence, creak (N-A to N-D) | missed | Endings not measured |

## 4. Candidate measures, ranked

Ranking (a) by strength of evidence that the measure tracks listener judgments, (b) by feasibility with existing word timings and
10 ms F0/level frames. None needs training.

| Rank a / b | Measure | Evidence | Reference, own baseline or norm | Different-speaker confounds | Controlled edit that imitates the pattern |
|---|---|---|---|---|---|
| 1 / 1 | Pitch match: per sentence, Pearson correlation of word-level median F0 (st, clip-centred) with the reference; add neighbour-difference version | [duong_mostow_2011; wang_evanini_yoon_2015; chung_bidelman_2022; miller_schwanenflugel_2008] | reference | Several valid readings exist; with one reference the score is unstable (Wang: below 10-20 readers); words with too few voiced frames must be dropped and counted; insensitive to span, so it complements the range measure | Proposal: PSOLA re-assignment of word-level F0 offsets within a sentence (move the peak to another word), keeping the overall range |
| 2 / 2 | Whole-clip P90-P10 in st (existing) with a second reading against published values | [niebuhr_skarnitzl_2019; portnova_2025; strangert_gustafson_2008; hincks_2005] | norm + reference | Speaker span differs 2.4-8.8 st IQR; text and style change it; creak inflates it; Hz-based cut-offs (.15) do not transfer to read text | Existing compression toward the median |
| 3 / 4 | Prominence-vector agreement: correlation of the per-word stress points with the reference, plus spread (SD) of stress points | [kallio_2022; suni_2015_2017] | reference; spread also against own clip | Small effect (4-6 %); cue use depends on first language; tempo differences must be removed first; one reference | Proposal: apply the existing de-emphasis to all reference-stressed words (E-A) or boost unstressed words toward the stressed level (E-B) |
| 4 / 3 | Sentence-final pitch change: median of last 200 ms of the final word minus median of the preceding stretch, and max-min of the final fall, in st, at "." only | [chung_bidelman_2022; ritchart_arvaniti_2014; rosenberg_autobi_2010; wang_evanini_yoon_2015] | reference (direction) | Creak removes or halves final frames; final-word length; five-way tone accuracy is poor, only direction is defensible | Proposal: PSOLA linear rise over the last syllable or last 200-300 ms (N-A); flatten the final fall to the level of the preceding word (N-B) |
| 5 / 5 | Per-sentence declination slope (st/s, all voiced points) | [yuan_liberman_2014; lieberman_1985] | reference; norm 1.2-2.7 st/s for 2-4 s news utterances | Slope depends on sentence length; 28.5 % of professional phrases are not negative; short sentences give few voiced points | Proposal: remove the fitted line from one sentence's F0 (PSOLA) |
| 6 / 6 | Two-sided emphasis check with a text prior: flag a stress point on a function word (or low accent-ratio word) that the reference does not stress | [nenkova_2007; talman_2019; wang_narayanan_2007] | reference + text | Function words can be legitimately accented; accent-ratio dictionary not in hand | Proposal: boost duration, pitch and level of one function word |
| 7 / 7 | Wiggliness and spaciousness per inter-pause unit | [wehrle_2018_2020] | reference or own clip | Needs smoothed, error-free contour; parameters arbitrary; never tested against monotony ratings | Compression lowers both; contour copy (below) keeps both |
| 8 / 8 | Repetition index: mean DTW or correlation similarity between time-normalised sentence contours, against the reference's own index | [kaland_2021_2023] for the distance; use is a proposal | reference | Sentences of similar syntax are legitimately similar; 20-40 s gives few sentences | Proposal: impose one sentence's time-warped contour on the others |
| 9 / 9 | Within-word F0 range or SD in place of P90 | [kakouros_tilt_2018] | as now | More exposed to tracking errors on short words | none new |
| 10 / 10 | Spectral tilt as a fourth emphasis cue | [baumann_winter_2018; kakouros_tilt_2018; ferrer_2015]; PAPERS.md #17 | same recording only | Channel and microphone change tilt; weakest or absent cue in three sources | Proposal: high-shelf attenuation on the word |
| - | Creak proxy at sentence ends | [drugman_2014; portnova_2025] | own clip | Unvoiced consonants and low-level endings look the same; no accuracy known | not established: no source shows PSOLA can produce credible creak |
| - | Level raised by nervousness | [stress_anxiety_fatigue] | own baseline only | Cannot be judged against another speaker | global pitch shift, but undetectable by design |

On the product's design choice (range ratio to the reference, relative to the speaker's own typical ratio):
- Supported: semitone intervals are perceptually equivalent across speakers [traunmuller_1995]; span is a speaker dimension
  separate from level [patterson_ladd_1999; mennen_2012]; span depends on the text [busa_urbani_2011], so the same-text ratio is
  the right comparison; percentile ranges survive uncorrected tracking where max-min and SD/mean fail [niebuhr_skarnitzl_2019;
  portnova_2025]. Dividing by the speaker's own typical ratio is the span half of the "level + span" normalisation that
  [wang_evanini_yoon_2015] apply as speaker z-scores.
- Not supported or untested: no opened study validates a percentile range on windows as short as five words; the validated
  windows are 10 s [hincks_2005; hincks_edlund_2009] and 40-98 s [niebuhr_skarnitzl_2019]; inter-pause units of 1-3 s were used
  only for turning-point measures [wehrle_2018_2020]. Normalising by the clip's own median ratio removes exactly the whole-passage
  compression that the L2 and low-arousal literatures describe, so that pattern rests entirely on the separate whole-clip check.
  Percentile spans are also the family that [patterson_ladd_1999] found weakest against listener judgments and that
  [wehrle_2018_2020] show to be blind to contour shape.

## 5. Open questions; searched for and not found

1. No validated measure of between-sentence contour repetition in human read speech. Only a stated intention [hincks_2005] and
   generic contour-distance methods.
2. No published numeric threshold for an uptalk rise in statements (values in [ritchart_arvaniti_2014] are in figures), and no
   reported accuracy for a two-way rise/fall decision at sentence ends.
3. No source showing nervousness narrows pitch range in read speech. The one paper likely to hold data (Goberman et al. 2011)
   could not be opened; a search summary attributes narrower pitch variation to early practice, not to anxiety. Unverified.
4. No method for vocal tremor in connected read speech; only sustained-vowel evidence [baird_2020].
5. No study of how much the local range ratio varies between competent readers of the same text; the project's six-reader
   estimate has no published counterpart. [duong_mostow_2011] reports only "extremely high correlation among adults" second-hand.
6. No perceptual threshold for "emphasis lost" (how much shorter, flatter or quieter before listeners stop hearing the stress).
7. Reading-prosody evidence is from children and L2 adults; no opened study rates adult native read-aloud delivery against a
   template. Transfer to adult presenters is an assumption.
8. Kurtosis of the F0 distribution correlated -.43 with charisma [niebuhr_skarnitzl_2019]; its behaviour on 20-40 s is unknown.
9. Emotion cue tables for boredom ([scherer_2003] Table 1) did not survive text extraction; boredom is not sourced here.
10. Prosogram was consulted only for its perceptual thresholds; its pitch-variability profile measures were not opened.

## 6. References

Full text read (file in `sources/`):
- Hincks 2005, Interspeech [hincks_2005] · Hincks & Edlund 2009, SLaTE [hincks_edlund_2009]
- Niebuhr & Skarnitzl 2019, ICPhS [niebuhr_skarnitzl_2019] · Strangert & Gustafson 2008, Interspeech [strangert_gustafson_2008]
- Wehrle et al. 2018, Studi AISV; Wehrle et al. 2020, Speech Prosody [wehrle_2018_2020]
- Zimmerer et al. 2014, Speech Prosody [zimmerer_2014] · Busà & Urbani 2011, ICPhS [busa_urbani_2011]
- Patterson & Ladd 1999, ICPhS [patterson_ladd_1999] (tables not legible) · De Looze & Hirst 2014, Speech Prosody [delooze_hirst_2014]
- Lindh & Eriksson 2007, Interspeech [lindh_eriksson_2007] · Portnova et al. 2025, JSLHR [portnova_2025]
- Duong, Mostow & Sitaram 2011, ACM TSLP [duong_mostow_2011] · Chung & Bidelman 2022, JSLHR [chung_bidelman_2022]
- Wang, Evanini & Yoon 2015, SLaTE [wang_evanini_yoon_2015] · Kallio, Suni & Šimko 2022, Language and Speech [kallio_2022]
- Yuan & Liberman 2014, Speech Communication [yuan_liberman_2014] · Arvaniti & Godjevac 2003, ICPhS [arvaniti_godjevac_2003]
- Ritchart & Arvaniti 2014, Speech Prosody [ritchart_arvaniti_2014] · Rosenberg 2010, Interspeech [rosenberg_autobi_2010]
- Drugman, Kane & Gobl 2014, CSL (arXiv copy) [drugman_2014] · Mertens 2004, Speech Prosody [mertens_2004]
- Xu & Xu 2005, J. Phonetics [xu_xu_2005] · Baumann & Winter 2018, J. Phonetics (accepted manuscript) [baumann_winter_2018]
- Wang & Narayanan 2007, IEEE TASLP [wang_narayanan_2007] · Kakouros & Räsänen 2015, Interspeech [kakouros_rasanen_2015]
- Kakouros, Räsänen & Alku 2018, Speech Communication (author manuscript) [kakouros_tilt_2018]
- Suni, Aalto & Vainio 2015, arXiv preprint of the CWT prominence method [suni_2015_2017] · Talman et al. 2019, NoDaLiDa [talman_2019]
- Morrison et al. 2024, ICASSP [morrison_2024] · Nenkova et al. 2007, NAACL [nenkova_2007] · Ferrer et al. 2015, Speech Communication [ferrer_2015]
- Mo, Cole & Lee 2008, Speech Prosody [mo_2008] · Kaland 2021, JIPA [kaland_2021_2023]
- Schewski et al. 2025, PLOS ONE; Low, Bentley & Ghosh 2020, Laryngoscope Investig. Otolaryngol.; Vogel, Fletcher & Maruff 2010,
  SST; Baird et al. 2020, Interspeech [stress_anxiety_fatigue] · Scherer 2003, Speech Communication [scherer_2003] (Table 1 not legible)

Abstract only [abstracts_openalex unless noted]: Traunmüller & Eriksson 1995, JASA · Mennen, Schaeffler & Docherty 2012, JASA ·
Breen et al. 2010, Lang. Cogn. Processes · Kochanski et al. 2005, JASA · Kang, Rubin & Pickering 2010, Mod. Lang. J. · Cole, Mo &
Hasegawa-Johnson 2010, Lab. Phonology · Chen et al. 2001, JASA · Miller & Schwanenflugel 2008, Reading Res. Q. · Schwanenflugel,
Westmoreland & Benjamin 2015, Reading and Writing (ERIC record) · Anderson et al. 2014, PLoS ONE · Linneman 2013, Gender & Society ·
Paunović 2022, Phonetica · Kaland 2023, JASA [kaland_2021_2023] · 't Hart 1981, JASA · Lieberman et al. 1985, JASA [lieberman_1985] ·
Laukka et al. 2008, J. Nonverbal Behavior (abstract as quoted by a search result) [stress_anxiety_fatigue].

Read through a tool summary only: Veiga et al. 2025, Stress and Health [stress_anxiety_fatigue] (numbers as returned by the fetch
tool; to re-check against the page).

Secondary (reported inside an opened paper, named there): Schwanenflugel et al. 2004, Miller & Schwanenflugel 2006, Benjamin &
Schwanenflugel 2010 (in Chung & Bidelman, Duong et al.); Pickering 2004 (in Hincks 2005); Xu & Sun 2002 (in Xu & Xu); Harrison &
Horne (in Vogel et al.); De Looze & Hirst 2008 two-pass pitch bounds (in Portnova et al.); Kalinli & Narayanan, Ananthakrishnan
et al., Tamburini (in Suni et al., Kakouros & Räsänen); Liberman & Pierrehumbert 1984 (in Arvaniti & Godjevac).

Could not open (wanted for; full list in `sources/NOT_OPENED.txt`): Goberman, Hughes & Haydock 2011 (anxiety and pitch in public
speaking) · Cummins et al. 2015 (depression review) · Rosenberg & Hirschberg 2009 (charisma, F0 SD) · Bolaños et al. 2013 (features
of automatic expressive-reading scoring) · Heldner 2003 (spectral emphasis in focal accent) · Kakouros & Räsänen 2016 and Suni et
al. 2017 journal versions · full texts of Kochanski 2005, Breen 2010, Mennen 2012 · Liberman & Pierrehumbert 1984 · Keating & Kuo
2012 · Blaauw 1994, Howell & Kadi-Hanifi 1991 · Sabu & Rao 2018 · Lee et al. 2017 (sentence stress feedback) · Bowen et al. 2013 ·
Warren 2016 · Hirschberg 1993.

Unsourced, to verify:
- Conversion of PVQ .15 to about 2.6 st SD and about 6.7 st P90-P10 (derived here; first-order and normal-distribution assumptions).
- "Pitch sigma 2-4 st in connected speech; monotone below 1.5 st": seen only on a non-scholarly page; not used.
- A 20.7 % rate of sentence stress on function words by Korean learners: search snippet with no opened paper; not used.
- Physiological voice tremor band and any tremor measure for read speech: general knowledge only, no source opened.
- All "proposal" edits in section 4 (contour re-assignment, contour copy, detrending, final rise) are untested ideas.
- That the dropped rising-ending edit failed for reasons connected to creak or missing final frames: not investigated.
