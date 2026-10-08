# Pace and pauses: flaw -> reasons -> patterns -> detection methods

> **Corrections after the citation check (`../VERIFICATION.md`, 2026-10-02).** (1) Huber 2012: the Parkinson contrast for breaths at
> locations unrelated to syntax is 6.3 % against 0.8 % (p = .036); 9.2 % against 3.7 % is "locations without punctuation" and was not
> significant (p = .124). (2) Wang 2010: 13.6 % of pauses of 250 ms or more are not breaths (43 of 316), not "about 10 %"; 250 ms is best
> by d-prime only, accuracy is higher at 300 ms (.922) and 350 ms (.914). (3) Miller & Schwanenflugel 2006: R2 = .328 is the
> complex-adjective comma; the phrase-final comma is .144. (4) Schwanenflugel 2004: the body says 120 children and 34 adults (4
> excluded), the abstract 123 and 24. (5) The within-clause pause evidence [19, 32, 33, 34] and the meta-analysis [31] are
> second-language speech, mostly picture narration or argumentative speech, not read text. (6) Moers [18] has three age groups, not a
> continuous range. Kahng 2018 DOI: 10.1017/S0142716417000534. Ten of the eleven "full-F" sources were re-read in primary text and
> were accurate apart from item 1.

Research report, 2026-10-02. Topic: timing of fluent read speech (pace, pauses). Literature only; no code was run on the project.
Source passages are in `sources/<name>.txt` (one file per source, 57 files). Numbers in square brackets refer to section 6.

How to read the evidence labels:
- **full** = text downloaded and searched locally (passages copied verbatim into the source file).
- **full-F** = full text opened only through the fetch tool, which returns a model-written extraction. The wording and the numbers of those passages are not guaranteed verbatim. One fetch result in this session was wrong (it invented kappa values for [24]; the PDF was then read directly). For every full-F source the PubMed abstract was fetched as an independent check and is saved in the same source file; where the two disagree it is said below. Treat full-F numbers as "to re-check".
- **abs** = abstract only. **sec** = secondary (read through another paper).

## 1. Summary table

| Flaw | Reason | Pattern the reason leaves | Best detection method(s) | Computable now? | Training? | Evidence |
|---|---|---|---|---|---|---|
| Pace | Deliberate fast reading, time pressure | Articulation rate up 13-18 % (one of three readers: about 0 %), speaking rate up to 28 %; pauses deleted or shortened; phrase breaks removed; unstressed syllables and vowels shortened more than stressed syllables and consonants [36, 37, 5] | Split tempo into articulation rate, pause count, pause duration against the reference; count reference pauses that are missing | Yes (all three parts exist as separate numbers) | No | Moderate: 1 full study with 3 readers, 1 full article introduction, 1 abs |
| Pace | Nervousness, speech anxiety | Not a speed-up of articulation. More silence: more and longer silent pauses [10]; share of silence correlates with state anxiety r = .36 [11]; one review: "No consistent acoustic patterns were identified for fear or anxiety" [14]; induced anxiety changed only filled pauses [13] | Share of silence (phonation-time ratio), pause count per second, against the speaker's own baseline | Yes, but only against the speaker's own calm reading; not against the reference | No | Weak for read speech: abs, sec, 2 full studies on spontaneous speech |
| Pace | Cognitive load, lexical difficulty | Local: longer word durations for low-frequency and low-predictability words in reading aloud [18]; a pause is more likely before a low-frequency word [19]. Global under a concurrent task: faster in 4 of 5 talkers, one slower, talker-specific [17] | Per-word duration and per-word preceding silence ("production" and "latency"), each as a contour correlated with the reference contour [24]; duration against an expected-duration model [24, 51] | Per-word contours: yes. Expected-duration model: no (needs a duration model) | Contours: no. Duration model: yes | Moderate: 1 full method paper, 2 abs, 1 full-F |
| Pace | Low reading skill (word-by-word reading) | "Reads primarily word-by-word", two-word groups, "awkward" groupings [23]; long pauses inside sentences (688 ms in the slowest quartile against 313-365 ms) [21] | Words per run between pauses (mean length of run), count of within-sentence pauses, per-word latency contour against the reference [24, 28, 31] | Yes | No | Moderate to strong for children; no adult study found |
| Pace | Second-language processing | Lower articulation rate, shorter runs, more pauses; correlations with rated fluency: articulation rate r = .62, mean length of run .72, speech rate .76 [31]; read speech: rate of speech r = .90-.93 with expert fluency ratings [28] | Rate of speech, articulation rate, phonation-time ratio, mean length of run | Yes | No | Strong (meta-analysis of 22 studies, full) |
| Pace | Irregular rhythm (dysarthria, learner speech) | Uneven local tempo; abnormal vowel/consonant interval variability | (a) dispersion of the local tempo ratio along the alignment with a reference ("tempo irregularity") [49]; (b) interval metrics %V, VarcoV, nPVI [45, 46, 48]; (c) envelope modulation spectrum [47] | (a) yes from the existing five-word ln-ratio; (b) needs vowel/consonant boundaries; (c) yes from level frames | (a) no; (b) no; (c) the published use needs a trained discriminant | (a) moderate, 1 full preprint; (b) contradictory [46 vs 48]; (c) 1 study |
| Pace | Tempo drift over the passage | Both healthy and Parkinson readers faster in the last sentence than the first; patients more [9] | Articulation rate of the last part divided by that of the first part, against the same ratio in the reference | Yes | No | Weak (abs only; size of the healthy drift not seen) |
| Pace | Missing or misplaced phrase-final lengthening | Lengthening sits in the rhyme of the last syllable before a boundary [51]; final words 80 ms longer than the same word mid-sentence, within speaker [52] | Duration of the word before each punctuation mark, relative to the speaker's own tempo, against the reference | Partly: the 80 ms effect is the same size as the aligner's word-boundary error (48-89 ms, docs/PAPERS.md [21]) | No | Moderate for the pattern; no detection study on a reader's error found |
| Pauses | Planning at syntactic boundaries (normal) | Pause length grows with the length of the phrases on both sides [53, 54]; skilled adults: long pauses only at sentence ends (mean 446 ms), commas mean 59 ms, range 0-454 ms [22] | Classify every pause by text position (sentence end, comma, none) and compare duration within class | Yes with punctuation; clause boundaries need a parser | No | Strong for the pattern |
| Pauses | Lexical retrieval, L2, online planning | Pauses inside clauses, not at their ends [19, 33]; within-clause pause rate has the strongest correlation with fluency ratings [34, 32] | Count and summed duration of pauses at positions with no punctuation and no clause boundary | Yes (this is the existing "inserted pause" rule, as a count) | No | Strong (several studies, 1 with phonetic manipulation) |
| Pauses | Low reading skill | Longer between-sentence pauses (661 against 369 ms) and "pausal intrusions" inside sentences [21, 22] | Same as above, plus pause-duration contour against the reference [24] | Yes | No | Moderate (children only) |
| Pauses | Nervousness | More frequent and longer silent pauses, more time pausing [10]; share of silence r = .36 with state anxiety [11] | Share of silence; pause count; mean pause duration | Yes; needs own baseline | No | Weak for read speech |
| Pauses | Breathing | Reading: breath groups 4.05 s (SD 1.5), inter-breath pause 0.64 s (0.25-1.8 s), inspiration 0.54 s; 1.8 % of breaths at ungrammatical places [1]; 2.1-3.2 % in other studies [1, citing others]; Parkinson readers 9.2 % against 3.7 % at places without punctuation [6] | Breath pause = pause of at least 250 ms (misses 0, false alarms about 10 % in reading) [2]; inbreath noise 291-418 ms with silent edges of 23-75 ms, softer than aspiration noise [7]; trained 4-class pause classifier, precision .87, recall .86 [8] | Pause threshold: yes. Inbreath noise rule from level, voicing and MFCC frames: possible, untested | Rule: no. Classifier: yes | Strong for the pattern; moderate for audio-only detection |
| Pauses | Fast reading | Fewer pauses (-23 % and -47 % in two of three readers); mean pause duration -13 % in two readers, +9 % in the third [36]; at fast rates "the physiological need to breathe is the sole determinant of pausing" [5] | Reference pauses of any class that are missing or shortened | Yes (the existing "shortened pause" rule covers reference pauses of 0.5 s or more) | No | Moderate |
| Pauses | Listener side | Silences inside fluent newsreader speech: mean 57 ms -> 12.5 % of samples judged disfluent; 117 ms -> 34.4 %; 212 ms -> 71.9 %; 403 ms -> 93.8 % [56]. Pause frequency r = -.59, pause duration r = -.46 with rated fluency [31] | Use as the perceptual scale for within-phrase silences | Yes | No | Moderate (one small manipulation study, one meta-analysis) |

## 2. Reasons, patterns and methods per flaw

### 2.1 Pace

#### Reason A. Deliberate fast (or slow) reading; time pressure
Pattern. Trouvain & Grice [36, full] had three German speakers read one text at self-chosen normal, fast and slow tempo.
- "relative to her normal speed, she increased her articulation rate by 18% to achieve a fast tempo and decreased it by 13% to produce a slow tempo. Speaker AT's values involved an increase of 13% and decrease of 8% ... By contrast, PS hardly increased her articulation rate at all for her fast readings." (sec. 3.1)
- "for all speakers there are greater differences amongst the three speeds for speaking rate than for articulation rate ... speaker CZ, where fast speech has a speaking rate increase of 28% as opposed to 18% for the articulation rate." (Table 1 text)
- Pauses (Table 2; count / mean duration in ms, three speakers): fast 6.7 / 646, 6.0 / 465, 13.3 / 475; normal 8.7 / 592, 11.3 / 533, 13.0 / 548; slow 11.7 / 583, 13.3 / 608, 17.0 / 772. "All three speakers increased the number of pauses to slow down, whereas only two of the three ... reduced their number to speed up." The third "did, however, reduce their mean duration by 13%".
- Conclusion (sec. 4): "articulation and speaking rate cannot be used as sole indicators of an achieved rate change".

Natural fast speech is not a uniform compression. Janse [37, full], introduction: "When people speak faster, consonant durations are reduced less, relatively, than vowel durations"; "durations of unstressed syllables in polysyllabic words are reduced more than those of stressed syllables". Abstract: listeners "preferred artificially time-compressed speech over naturally produced fast speech", and natural fast speech "slows down processing, relative to linearly time-compressed speech".

Reading with breathing [5, abs]: "At slow and normal rates, speakers accommodate their need to inhale to the preplanned pause patterns. At fast rates, however, the physiological need to breathe is the sole determinant of pausing."

Difference from the other reasons: fast reading removes pauses at boundaries and keeps the rest fluent; anxiety and retrieval difficulty add pauses; low reading skill adds pauses inside phrases.

Methods.
- Articulation rate against speaking rate (already in docs/PAPERS.md [14]). The decomposition the pattern asks for is three numbers against the reference: ln ratio of speech time (pauses removed), ratio of pause count, ratio of mean pause duration.
- Between-talker comparability on one text. Crystal & House [39, abs], six talkers reading two scripts: "variability of articulation rate, measured as the average syllable duration for interpause intervals (runs), is not random, but is the natural consequence of the content of the run. Durations of comparable runs of different talkers are highly correlated." This supports comparing participant and reference run by run on the same text, and argues against an absolute rate per run.
- Within one talker, rate still varies: "substantial variation in articulation rate for these speakers, even within a single utterance of a single talker" [38, abs, spontaneous speech]; tempo "depends mainly on phrase length, due to anticipatory shortening" [42, abs, spontaneous Dutch]. On a fixed text phrase length is the same for both readers, so this source of variation cancels.
- Habitual rate differs by speaker: [40, abs] 100 readers of one passage; habitual and maximum articulation rate are linearly related, taken as "a neuromuscular component". [41, full-F] read sentences: 3.40 syll/s, SD 0.42 across speakers (about 12 %); group differences 8 % (dialect), 11 % (age), 4.5 % (sex). The abstract of [41] confirms the direction of the three effects, not the values.
- Absolute norms: adult oral reading averages 183 wpm (77 studies, 5,965 participants) [27, full, abstract]; the same article states "audiobooks are spoken at a rate of 140-180 wpm". Adults reading a children's test passage: mean 189.0 correct words per minute, SD 38.0 [21, full-F].

#### Reason B. Nervousness, speech anxiety, stage fright
Pattern. None of the sources opened reports a faster articulation rate in anxious speakers. What is reported is more silence.
- Hofmann et al. [10, abs], speech to two listeners, 24 social phobics, 25 controls: "Phobics showed more filled pauses, had longer silent pauses, paused more frequently, and spent more time pausing than controls".
- Laukka et al. 2008 [11, sec, through 12 p. 2]: features included "articulation rate and percentage of silence"; significant change after treatment in "F0 mean, F0 maximum, HF 500, and percentage of silence"; correlations with state anxiety "F0 SD (r=-0.24; P<.05) and percentage of silence (r=0.36; P<.01)". Articulation rate is not among the significant features in that description.
- Rood & de Jong [13, full], 22 learners, anxiety induced within subjects (d = 0.86 on reported anxiety): "Of all fluency indices, results showed an effect for filled pauses only" (p = 0.013; d = 0.58). "Additionally, heightened anxiety was significantly related to more use of silent pauses."
- Schewski et al. [14, full], systematic review: stress "was associated with increased F0 and intensity, and reduced speech duration"; "No consistent acoustic patterns were identified for fear or anxiety."
- Wang Q et al. [15, abs], 316 students, picture description: jitter was "the sole speech parameter consistently linked to state anxiety"; speech rate was measured and was not.
- Giddens et al. [16, abs], review of more than 50 studies: "Increase in fundamental frequency is the most commonly reported effect of stress"; findings otherwise "primarily equivocal".

All of these are spontaneous or prepared speaking, not reading a given text. No study of anxiety in read-aloud speech was opened.

Methods. Share of silence ("percentage of silence" [11]; "phonation/time ratio" [28]); number of silent pauses per second of speaking time and mean silent pause length (definitions in [30]: NSP, MLP, with a log transform of MLP). All computable now. The project's own test (pause share 0.10 to 0.28 between readers of one text) and the size of the published effect (r = .36) point the same way: share of silence does not separate an anxious reading from a calm one across speakers. It is only usable against the same speaker's baseline.

#### Reason C. Cognitive load, planning and lexical retrieval
Pattern.
- Local slowing on hard words in reading aloud: Moers et al. [18, abs], Dutch readers aged 8 to 95: "consistent effects of TP [transitional probability] on word durations for all age groups ... beyond the well-established effect of word frequency".
- Pause before the hard word: de Jong [19, abs], spontaneous: "both L1 and L2 speakers are more likely to pause before lower frequency words".
- Global effect of a concurrent task: Lively et al. [17, abstract verified]: "some talkers produced utterances with increased amplitude and amplitude variability, decreased spectral tilt and F0 variability and increased speaking rate". Full-F: four of five talkers shortened the phrase, one lengthened it; "we did not obtain consistent results across all five talkers for any of the variables".
- In reading aloud the eye runs ahead of the voice and the reader regulates the distance by longer fixations or regressions [20, full, abstract]. No timing number for the voice was taken from this paper.

Difference from Reason A: the unit is one word (longer word, or silence before it), not a run; the direction of the global effect is not fixed.

Methods.
- Word-level contour against a reference reading (Duong, Mostow & Sitaram [24, full]). "We represent a prosodic contour of a read sentence as the sequence of values, one for each word in the sentence, of a prosodic feature such as the word's latency, duration, mean pitch, or mean intensity." Latency is the silence before the word; "production time to say each word"; reading time = latency + production; each "also normalized by word length as time per letter". Score: "simply compute the correlation between the two contours", which "serves to factor out differences between children and adults in baseline F0 ..., individual variations in intensity, and fluctuations in recording conditions". Validation: predicting human rubric scores, 10 children, leave-one-out (Table 8): Expression and Volume 0.902, Smoothness 0.768 (both p < 0.01), Phrasing 0.281, Pace 0.448 (not significant). The human rubric itself was unreliable: intraclass correlation at student level Expression 0.798, Phrasing 0.681, Smoothness 0.283, Pace 0.721; at sentence level 0.593, 0.535, 0.398 for the first three (Tables 5, 6). The authors: "direct comparison fared poorly for want of a reliable human gold standard".
- Expected-duration model [24]: "Regression trees to map text features to adult phoneme durations", trained on adult narrations, then used without a narration of the sentence; durational features alone predicted fluency and comprehension post-test scores of 55 children with "adjusted R2 of 0.6". Needs training data (adult readings) and phone-level timing.
- Normalised segment duration with speaking-rate compensation [51, abs]; the formula was not seen (abstract only).
- Trained regression on many prosodic features for learner speech: correlations "of up to .85" with listener ratings [50, full]; the feature set includes duration norms, PVI and percentage of vocalic intervals. Needs rated training data.
- Local rate without alignment: perceived local rate needs a window of about 0.5 to 0.7 s ("segments of less than 500 ms hindered the assessment of speech rate, while segments of more than 700 ms could contain strong changes"; 625 ms chosen); perceived local rate correlates with syllable rate r = 0.81, phone rate r = 0.73, their linear combination r = 0.88 [43, full]. Signal-only syllable-rate estimation on Switchboard: correlation 0.745 [44, abstract verified]; mean error 0.339 syll/s, SD of error 0.796 (full-F). With a known text and an alignment the project does not need a signal-only estimator; the earlier feature report already found the nucleus counter unreliable (65 nuclei against 101 syllables).

#### Reason D. Low reading skill and prosodic phrasing
Pattern. NAEP oral reading fluency scale [23, full]: "Level 1 Reads primarily word-by-word. Occasional two-word or three-word phrases may occur - but these are infrequent"; "Level 2 Reads primarily in two-word phrases ... Word groupings may seem awkward and unrelated to larger context"; "Level 3 Reads primarily in three- or four-word phrase groups"; "Level 4 Reads primarily in larger, meaningful phrase groups ... Preservation of the author's syntax is consistent." Rate bands: "less than 80, 80-104, 105-129, and 130 or more words per minute" (fourth grade). Schwanenflugel et al. [21, abstract verified]: "Children with faster decoding speed made shorter and less variable intersentential pauses, shorter intrasentential pauses, larger sentence-final fundamental frequency (F0) declinations, and better matched the adult prosodic F0 profile." Quartile means are in section 2.2 (full-F). Sample size: the abstract says 123 children and 24 adults, the fetched text 120 and 34; unresolved.

Methods. Template correlation of latency and production contours [24]; words per run; count of within-sentence pauses; a rating scale built from spectrographic measures (CORFS), where "Intraclass correlations among raters were strong" [25, abs]. A feature-based system for children's reading reached Pearson 0.794 with manual scores [26, sec]; it uses trained boundary and prominence detectors.

#### Reason E. Second-language processing
Pattern and method are the same objects here (temporal measures correlated with ratings).
- Read speech, 20 native and 60 non-native speakers of Dutch [28, abs]: "for six automatic measures the magnitude of the correlations with the fluency scores varies between 0.81 and 0.93. Rate of speech appears to be the best predictor: correlations vary between 0.90 and 0.93. Two other important determinants of reading fluency are the rate at which speakers articulate the sounds and the number of pauses they make." Predictive power "is stronger for read speech than for spontaneous speech" [29, abs].
- Meta-analysis, 22 studies, 263 effect sizes [31, full, Table 8]: articulation rate 0.62 [.45, .74]; pause frequency -0.59 [-.69, -.48]; pause duration -0.46 [-.59, -.31]; disfluency rate -0.20; mean length of run 0.72; speech rate 0.76 [.64, .85].
- Bosker et al. [30, full]: pause measures alone adjusted R2 = 0.5917; speed (mean length of syllables) alone 0.5449; repairs alone 0.1583; pauses plus speed 0.7825.
- Listener side: ratings are highest for speech "somewhat faster than the rates generally used by L2 users; however, both very fast and very slow speech tended to be less highly rated"; shown causally with compression and expansion [35, abs].

#### Reason F. Irregular rhythm
Interval metrics. Wiget et al. [45, abs], five sentences read by six speakers: "Differences between sentences were responsible for the greatest variation in rhythm scores. Inter-speaker differences were also a source of significant variability ... relatively little variation due to segmentation"; automatic phone alignment "showed good agreement with the human measurers". On one fixed text the sentence effect is removed; the speaker effect is not. Liss et al. [46, abs], 55 speakers: "The majority of classification functions were more than 80% successful". Lowit [48, abstract verified]: "none of the metrics could differentiate disordered from healthy speakers, despite clear perceptual differences, suggesting that factors beyond segment duration impacted on rhythm perception." The two clinical studies disagree. The metrics need vowel and consonant interval boundaries, which the project's character-level CTC spikes do not give reliably.

Envelope modulation spectrum [47, abstract verified; details full-F]: spectra of amplitude modulation up to 10 Hz of the full signal and seven octave bands; six variables per band (peak frequency, peak amplitude, energy 3-6 Hz, below 4 Hz, above 4 Hz, ratio); "84%-100% classification accuracy for group membership"; "automated and requires no editing or linguistic assumptions". The published result is a discriminant analysis trained on 43 speakers; no threshold for one clip exists.

Reference-based tempo irregularity (McIntosh et al. [49, full, preprint]): align learner and native template by DTW; "Horizontal steps in this path represent time dilation (the learner is locally slower than the template), and vertical steps represent time compression"; "We define the warp angle as the instantaneous pacing ratio between the two utterances ... we first approximate the warp angle at each frame and then calculate the dispersion of these angles about their mean." Sentence-level rhythm scores, English (ERJ), Pearson r x 100 (Table II): human benchmark 49.3; duration-ratio baseline (Rdur) 31.7; tempo irregularity 37.3; Rdur + tempo irregularity 43.5; interval distortion 43.6; Rdur + interval distortion 44.9. No training on rated learner speech; the paper computes the alignment on WavLM-Large features and averages over several native templates. The measure itself only needs an alignment path, which the project already has through the transcript.

Tempo drift [9, abs]: first against last sentence of a 170-syllable text; "Both groups showed an accelerated speech rate in the last sentence compared to the first; however, PD patients had a higher speech acceleration".

#### Reason G. Phrase-final lengthening absent or misplaced
Pattern. Wightman et al. [51, abs]: lengthening is "restricted to the rhyme of the syllable preceding the boundary"; with "a normalized measure of segmental lengthening, and by compensating for differences in speaking rate ... at least four distinct types of boundaries can be distinguished". Camara et al. [52, full, preprint], four corpora including read radio news: final words "longer (mean about 191 ms; d = 1.14). The effect persists in matched-word, within-speaker comparisons (80 ms; p < 0.001) and is localized mainly to the final syllable (d = 0.89)". These are turn-final or utterance-final words; phrase-internal boundaries were not measured there. Lengthening can itself make a listener hear a pause: "in certain acoustic environments (such as prepausal lengthening) a pause could be perceived in the absence of any silent period" [56, introduction, citing others; sec].

No study was found that detects a reader's missing final lengthening as an error.

### 2.2 Pauses

#### Reason H. Planning at syntactic and prosodic boundaries (the normal case)
- Krivokapic [53, abstract verified], read sentences, synchronous dyads: "a significant post-boundary effect of prosodic branching and significant pre- and post-boundary phrase length effects". Full-F: mean pauses of roughly 378-709 ms before and 417-743 ms after, short against long phrases (to re-check).
- Zvonik & Cummins [54, full]: the lengths of the phrase before and after a pause "combine superadditively"; the probability of a short pause (about 300 ms; the comparison sign was lost in text extraction) "rises greatly if both the preceding and the following phrases are short" (about 10 syllables).
- Miller & Schwanenflugel [22, full-F], 29 adults reading a syntactically complex text, pauses over 100 ms: sentence-final mean 446 ms (range 145-685); phrase-final commas mean 59 ms (range 0-454); complex-adjective commas mean 53 ms (0-337); "long pauses seemed to be relegated to the ends of basic declarative sentences only". The abstract confirms only that skilled children had "shorter and more adultlike pause structures".
- Earlier research (docs/PAPERS.md [12]): read English median pause 493 ms, modes 126 and 512 ms.

Consequence: a comma does not predict a pause in a skilled adult reading; a sentence end does. Pause length at a boundary is partly fixed by the text (phrase lengths), which is the part a same-text reference removes.

#### Reason I. Retrieval difficulty and online planning (hesitation)
- Tavakoli [33, abs]: learners' "distinctive feature ... is that they pause frequently in the middle of clauses rather than at the end".
- de Jong [19, abs]: learners "paused more often than L1 speakers within utterances; but not between utterances ... only within utterances, L2 pauses were longer"; "when using fluency for L2 testing, pause locations must be taken into account".
- Kahng [34, abs]: "silent pause rate within a clause demonstrated the strongest correlation with L2 fluency ratings"; a second experiment moved pauses by phonetic manipulation and "perceived fluency of L1 and L2 speech was influenced by pause location".
- Suzuki & Kormos [32, abs]: "perceived fluency was most strongly associated with the frequency of mid-clause pauses".
- The meta-analysis found the moderator "pause location" not significant overall (Q(2) = 4.25, p = .119) [31, full].

Method: count pauses by position class. Needs clause boundaries; punctuation is a subset of them.

#### Reason J. Low reading skill
Schwanenflugel et al. [21, full-F, Table 1] by decoding-speed quartile, slowest to fastest: between-sentence pause 661, 604, 411, 369 ms; within-sentence pause 688, 518, 313, 365 ms. Within-sentence pauses "ranged in length from 150 ms to over 1,000 ms". Miller & Schwanenflugel [22, full-F]: more skilled children had shorter pauses at sentence ends (R2 = .251) and at commas (R2 = .328). Method: as Reason I, plus the pause-duration contour against the reference [24].

#### Reason K. Nervousness
See Reason B: more frequent and longer silent pauses and more time pausing [10]; share of silence r = .36 with state anxiety [11]; silent pauses related to anxiety in [13]. The location of these pauses relative to syntax was not reported in what was opened.

#### Reason L. Breathing
Pattern in healthy reading. Wang et al. [1, full], 16 adults reading two passages with airflow measured:
- "The number of inappropriate breathing locations was 5 out of 273 (1.8%) and 143 out of 1,106 (13%) for the passage reading and the spontaneous speech task"; none within words. Earlier values quoted there: 2.1 % (reading, 24 speakers), 3.2 % reading and 15.3 % spontaneous (6 women), 19 % (6 older adults, extemporaneous).
- Appropriate = "at the end of a sentence or punctuation points such as comma or colon, or before noun, verb, adverbial phrases"; "Inspirations occurring within phrases or words are considered syntactically inappropriate."
- Reading: breath group duration mean 4.05 s, SD 1.5, range 0.93-9.36 s; inter-breath-group pause mean 0.64 s, SD 0.24, range 0.25-1.8 s; inspiratory duration mean 0.54 s, SD 0.18, range 0.19-1.21 s.
- "The noninspiratory pause, defined as IBP minus actual ID, might be an index of ... cognitive load".

Winkworth et al. [4, abs]: inspirations in reading "occurred almost exclusively at grammatically appropriate places"; lung volume was higher for "longer utterances" and for "initial breaths compared to final breaths". Huber et al. [6, abstract verified]: older adults "produced shorter utterances, a smaller percentage of breaths at major boundaries, and a greater percentage of breaths at minor boundaries"; Parkinson readers "took a greater percentage of breaths at locations unrelated to a syntactic boundary" (full-F: 9.2 % against 3.7 %).

Not found: any measurement of speeding up toward the end of a breath group, or of "running out of air", in healthy readers.

Methods.
- Pause-duration threshold as breath detector [2, abstract verified]: "the most accurate pause duration threshold for detecting inspiratory loci was 250 msec" in reading (full-F: no misses, false alarms 43/408, accuracy .895); 300 ms in spontaneous speech [3] (full-F: true positive 99.55 %, false positive 35.06 %). Listening by three judges was more accurate than the threshold.
- Acoustic description of the inbreath [7, full], 20 German speakers: "the majority of pauses contain inbreath noises, which are typically soft in intensity and extremely variable in duration"; silent "edges to the left and right of the breath noises have an average duration of 50 ms, whereas the breath noises themselves have a duration between 200 and 500 ms"; centre of gravity "below 2 kHz" in read speech. Table: inbreath noise 291 ms (SD 112) for professional newsreaders, 418 ms (89) for read narrations; left edge 67-75 ms, right edge 23-42 ms.
- Trained classifier [8, full]: each aligned pause is classified as silent pause, inhalation breath pause, noisy pause or no pause from F0 (voicing), RMS amplitude and spectral energy distribution in parts of the pause; 10-fold cross-validation, "Average precision was 0.87 +-0.014 and average recall 0.86 +-0.014". In their audiobook test sentences 79 % of 174 pauses were breath pauses, mean pause duration 354.9 ms (SD 155.3). Single-speaker audiobook data.

#### Reason M. Fast reading
See Reason A: pauses are deleted or shortened and phrase breaks demoted [36]; breathing alone decides pauses at fast rates [5].

#### Listener side for pauses
- Lovgren & van Doorn [56, full]: newsreader speech with its natural silences stretched. Table 3: mean silent period 57 ms (natural) -> 12.5 % of samples judged disfluent; 117 ms -> 34.4 %; 212 ms -> 71.9 %; 403 ms -> 93.8 %. Differences between the natural condition and the two longest conditions were significant. All silences in a sample were stretched together.
- Tanaka et al. [57, full], Japanese sentences: intelligibility was higher "with a relatively short time expansion (i.e., 100 ms) when the pause between phrases was long enough (i.e., 300 and 400 ms)". Pauses at phrase boundaries help the listener.
- Meta-analysis [31]: pause frequency -0.59, pause duration -0.46 with rated fluency.

Pause-duration distributions. Rosen et al. [55, abs]: pauses "measured from the intensity contour and fit with bimodal lognormal distributions using the Expectation-Maximization algorithm"; samples "of approximately 3 minutes"; in the patient group "both modes ... had significantly larger means, with disproportionately fewer pauses associated with the first mode". A 20-40 s clip holds too few pauses to fit two modes; not usable per clip.

## 3. What the current product covers, partly covers, misses

| Pattern | Status | Note |
|---|---|---|
| Uniform faster or slower stretch of 5-8 words (time-scale modification) | Covered | This is linear compression, which listeners prefer to natural fast speech [37]; it is the least natural form of rushing |
| Whole-passage tempo offset | Covered | Habitual rate differs about 12 % between speakers [41]; the 3.5-unit whole-clip threshold is the guard |
| Fast reading done by dropping or shortening pauses [36] | Partly | Only reference pauses of 0.5 s or more are checked; with normal-tempo mean pauses of 533-592 ms [36] and comma pauses near 59 ms [22], many shortenable pauses are below the rule |
| Non-uniform compression (unstressed syllables and vowels shortened more) [37] | Missed | Needs sub-word timing; not in the dataset |
| One word slowed, or one word preceded by a hesitation silence [18, 19] | Partly | The pause part is the "inserted pause" rule; the single-word slowing is averaged away over five words |
| Word-by-word reading: many short silences, short runs [23, 21] | Missed | Each silence may be under the rule's size; no count of pauses, no words-per-run measure |
| Tempo irregularity (dispersion of the local ratio) [49] | Missed | The local ln-ratio exists; its spread over the clip is not reported |
| Acceleration over the passage [9] | Missed | The clip median hides a drift; first-part against last-part ratio is not computed |
| Phrase-final lengthening missing [51, 52] | Missed | Effect size (80 ms) is at the aligner's error level |
| One pause shortened (0.5 s or more in the reference) | Covered | |
| One pause inserted where the reference has none and the text has no punctuation | Covered | Matches the best-supported harmful pattern (within-clause pause) [34, 19, 33] |
| Pause at a comma where the reference has none | Not flagged (by design) | Consistent with [22]: adults pause 0-454 ms at commas |
| Pause location relative to clause boundaries that carry no punctuation | Missed | A pause before a noun, verb or adverbial phrase is "appropriate" by [1]; the rule treats it as inserted |
| Breath in the wrong place; audible inbreath [1, 6, 7] | Missed | Also a measurement risk: an audible inbreath inside a pause raises the level, so the "longest silent run" can split and under-measure a breath pause (inbreath 291-418 ms between silent edges of 23-75 ms [7]) |
| Overall pause share, pause rate (anxiety, L2) [10, 11, 31] | Missed | Not separable across speakers (project test 0.10-0.28; r = .36 [11]) |
| Pause-duration distribution [55] | Missed | Not estimable from one short clip |

Points where this report differs from the earlier research:
1. docs/PAPERS.md item 7 calls the 1.2 s inserted pause longer than read-speech pauses. Inter-breath pauses in passage reading reach 1.8 s (mean 0.64 s, SD 0.24) [1], so 1.2 s is inside the observed range, about 2.3 SD above the mean.
2. Pause minimum 0.20 s against 0.25 s: for breath pauses in reading, 250 ms was the most accurate of 150-350 ms [2]. Studies of reading prosody used lower floors: 150 ms for within-sentence pauses [21], 100 ms [22], 100 ms and 150 ms before stops [36]. The perceptual data [56] show silences near 0.2 s already judged disfluent in 72 % of samples. No source supports one value for all uses.
3. The earlier feature report set the envelope-modulation measure aside as "optional research corroboration". [47] and [48] support that: the only positive result is a trained discriminant on clinical groups, and interval metrics failed in [48].

## 4. Candidate measures, ranked

Ranking is by (a) evidence, then (b) feasibility under the constraints (no training, CPU, 20-40 s clip, different speaker).

| # | Measure | Definition | Evidence | Feasibility | Confounds with a different speaker | Controlled edit that imitates the pattern |
|---|---|---|---|---|---|---|
| 1 | Within-phrase pause count and total duration | Pauses at word gaps with no punctuation (later: no clause boundary), per clip, against the same count in the reference | Strong [19, 33, 34, 32]; perceptual scale [56] | Uses existing pause detector and transcript | Readers differ in optional phrase breaks; a single reference over-constrains (docs/PAPERS.md [24]); positions before noun, verb or adverbial phrases are legitimate [1] | Insert silence of 0.2-1.0 s at one or several word gaps without punctuation (already built for one gap) |
| 2 | Tempo decomposition | ln ratio of speech time, ratio of pause count, ratio of mean pause duration, each participant over reference | Strong [28, 31, 36] | All inputs exist | Habitual rate (about 12 % SD [41]); pause habits | Time-scale modification of speech only; separately delete or scale all pauses; combine both for "natural" rushing |
| 3 | Per-word latency and production contours | For each word: silence before it, and its duration, each divided by the clip's own median; Pearson correlation with the reference contour over a sentence, plus the largest single-word residual | Moderate [24]; pattern support [18, 19] | Word timing exists; CTC word spans are short (docs/PAPERS.md [21]) so durations carry 48-89 ms error | Correlation removes overall speed [24]; differences in emphasis placement remain | Stretch one content word by time-scale modification; insert silence before it; do both for a "hesitation" |
| 4 | Mean length of run | Words (or syllables) between pauses of at least the pause minimum, clip mean, against the reference | Strong for learner speech (r = .72 [31]); scale wording for reading [23] | Trivial | Breath capacity and age change run length [6] | Insert short silences (0.15-0.3 s) after every word or every second word in a stretch |
| 5 | Tempo irregularity | Dispersion (SD or MAD) of the local ln tempo ratio over the clip, after removing its median | Moderate [49] (r = .37 alone, .44 with duration ratio; human agreement .49) | The local ratio already exists per five-word window; a shorter window raises alignment noise | Emphasis and phrasing choices of both readers add spread; a floor from reader-to-reader pairs is needed | Random per-word time-scale factors with mean 1 over a stretch |
| 6 | Tempo drift | ln ratio of speech-time ratio in the last third over the first third | Weak [9] | Trivial | Both readers may drift; short clips give few words per third | Time-scale factor ramped linearly across the clip |
| 7 | Breath-pause location | Pauses of 250 ms or more [2] taken as candidate breaths; share at punctuation against share elsewhere; breath-group length in seconds | Strong for the pattern [1, 4, 6]; threshold accuracy .895 in reading [2] | Threshold: exists. Confirming an inbreath from level, voicing and spectrum [7, 8] needs a new rule and validation | About 10 % of such pauses are not breaths [2]; recordings with noise gates or close editing have no audible breath | Move a recorded inbreath of the same speaker into a mid-phrase gap; if the clean clip has no audible breath this cannot be imitated beyond a plain silence |
| 8 | Pre-boundary lengthening | Duration of the word before each punctuation mark over the speaker's median word duration per syllable, minus the same for the reference | Moderate for the pattern [51, 52]; none for detection of an error | Word timing exists; effect (80 ms) about equals boundary error | Speakers differ in how strongly they mark boundaries | Compress the last word (or last syllable) before a punctuation mark by about 80 ms |
| 9 | Share of silence, pause rate | Silent time over total time; pauses per second of speech | Weak across speakers [11]; strong within learner groups [28, 31] | Trivial | Reader range 0.10-0.28 on one text (project test); professional 9 % against 28 % (docs/PAPERS.md [35]) | Scale all pauses by one factor |
| 10 | Interval rhythm metrics, envelope modulation spectrum | %V, VarcoV, nPVI; modulation energy 0-10 Hz | Contradictory [46, 48]; [47] needs training | Vowel/consonant boundaries not available; EMS computable but has no threshold | Significant speaker effect [45]; channel affects band envelopes | Not targeted by a simple edit |

Notes on the ranking.
- Measures 1, 2 and 4 are counts and ratios the detector already has the parts for; they change what is reported, not what is measured.
- Measure 3 is the only one of the top group that adds resolution (one word). Its ceiling is the aligner's word-boundary error.
- For all reference-relative measures the same-text design removes the largest known sources of variation (sentence content for rhythm metrics [45]; run content for articulation rate [39]; phrase length for tempo [42] and for pause duration [53, 54]). What remains is speaker habit, which one reference reading cannot separate from error. The sources that handled this used several readers: adults averaged into one profile in [21]; several native templates averaged in [49]; models "trained on multiple adult voices, so they are not specific to the idiosyncrasies of any one speaker" [24].
- Published absolute norms usable as sanity bounds only: 183 wpm adult oral reading [27]; breath group 4.05 s and inter-breath pause 0.64 s in reading [1]; sentence-final pause near 450 ms and comma pause near 60 ms in skilled adults [22, full-F]; tempo just-noticeable difference 5 % (docs/PAPERS.md [9]); within-speech silences near 0.2 s judged disfluent in most samples [56].

## 5. Open questions; searched and not found

1. Does nervousness speed up read speech? The rubric tradition says "hurried"; no opened source measured it. Every opened anxiety study used spontaneous or prepared speech and found more silence, not faster articulation. Goberman et al. 2011, the one acoustic study of public speaking anxiety with practice effects, could not be opened.
2. Speeding up toward the end of a breath group or phrase in healthy readers: searched; found only the first-to-last-sentence acceleration in [9].
3. A perceptual threshold for local tempo change inside a sentence (as opposed to whole-utterance tempo, 5 %): not found. [43] gives only the window length needed to judge local rate.
4. Detection of missing phrase-final lengthening as a reading error: not found. Boundary detection work exists for children's read speech (Sabu & Rao 2021, not opened) but uses trained models.
5. Thresholds for "too long" pauses by position (sentence end, comma, mid-phrase) in read speech: only the single-factor data of [56] and the adult means of [22]. Classic threshold studies (Butcher 1981; Duez 1985; Ruder 1973; Zellner 1994) could not be opened.
6. Inbreath detection from 10 ms level and MFCC frames without training: [7] gives the acoustic description, [8] a trained classifier; no published rule with thresholds was opened (Ruinskiy & Lavner 2007 is the likely source; not opened).
7. Whether one reference reading is enough for pause location. The opened sources that compare with adult readers average many adults [21] or several templates [49].
8. Adult (not child, not learner) studies of poor oral reading phrasing: none found.
9. Sample size in [21] (123 and 24 in the abstract; 120 and 34 in the fetched text) and the table values of [21, 22, 41, 53] need a direct re-read.

## 6. References

Read status as defined at the top. Source file names are in `sources/` (each with `.txt`).

1. Wang Y-T, Green JR, Nip ISB, Kent RD, Kent JF (2010). Breath group analysis for reading and spontaneous speech in healthy adults. Folia Phoniatr Logop 62(6):297-302. doi:10.1159/000316976. **full**. `wang2010_breath_groups`
2. Wang Y-T, Green JR, Nip ISB, Kent RD, Kent JF, Ullman C (2010). Accuracy of perceptually based and acoustically based inspiratory loci in reading. Behav Res Methods 42(3):791-797. doi:10.3758/BRM.42.3.791. **full-F**, abstract verified. `wang2010_inspiratory_loci_reading`
3. Wang Y-T, Nip ISB, Green JR, Kent RD, Kent JF, Ullman C (2012). Accuracy of perceptual and acoustic methods for the detection of inspiratory loci in spontaneous speech. Behav Res Methods 44(4):1121-1128. doi:10.3758/s13428-012-0194-0. **full-F**, abstract verified. `wang2012_inspiratory_loci_spontaneous`
4. Winkworth AL, Davis PJ, Ellis E, Adams RD (1994). Variability and consistency in speech breathing during reading. J Speech Hear Res 37(3):535-556. doi:10.1044/jshr.3703.535. **abs**. `winkworth1994_breathing_reading`
5. Grosjean F, Collins M (1979). Breathing, pausing and reading. Phonetica 36(2):98-114. doi:10.1159/000259950. **abs**. `grosjean_collins1979_breathing_pausing_reading`
6. Huber JE, Darling M, Francis EJ, Zhang D (2012). Impact of typical aging and Parkinson's disease on the relationship among breath pausing, syntax, and punctuation. Am J Speech Lang Pathol 21(4):368-379. doi:10.1044/1058-0360(2012/11-0059). **full-F**, abstract verified. `huber2012_breath_pausing_syntax_punctuation`
7. Trouvain J, Werner R, Moebius B (2020). An acoustic analysis of inbreath noises in read and spontaneous speech. Speech Prosody 2020, 789-793. doi:10.21437/SpeechProsody.2020-161. **full**. `trouvain2020_inbreath_noises`
8. Braunschweiler N, Chen L (2013). Automatic detection of inhalation breath pauses for improved pause modelling in HMM-TTS. 8th ISCA Speech Synthesis Workshop. https://www.isca-archive.org/ssw_2013/braunschweiler13_ssw.pdf. **full**. `braunschweiler2013_inhalation_breath_pause_detection`
9. Skodda S, Schlegel U (2008). Speech rate and rhythm in Parkinson's disease. Mov Disord 23(7):985-992. doi:10.1002/mds.21996. **abs**. `skodda2008_pd_rate_rhythm`
10. Hofmann SG, Gerlach AL, Wender A, Roth WT (1997). Speech disturbances and gaze behavior during public speaking in subtypes of social phobia. J Anxiety Disord 11(6):573-585. doi:10.1016/S0887-6185(97)00040-6. **abs**. `hofmann1997_social_phobia_speech`
11. Laukka P et al. (2008). In a nervous voice: acoustic analysis and perception of anxiety in social phobics' speech. J Nonverbal Behav 32(4):195-214. doi:10.1007/s10919-008-0055-9. **sec** (through [12]). `laukka2008_nervous_voice_SECONDARY`
12. Teferra BG, Borwein S, DeSouza DD, Simpson W, Rheault L, Rose J (2022). Acoustic and linguistic features of impromptu speech and their association with anxiety. JMIR Ment Health 9(7):e36828. doi:10.2196/36828. **full**. `teferra2022_anxiety_impromptu_speech`
13. Rood MMSJ, de Jong NH (2023). A mixed-methods study on the effects of manipulated speaking anxiety on L2 utterance and L2 cognitive fluency. J Eur Second Lang Assoc 7(1). doi:10.22599/jesla.96. **full**. `rood_dejong2023_anxiety_l2_fluency`
14. Schewski L, Doss MM, Beldi G, Keller S (2025). Measuring negative emotions and stress through acoustic correlates in speech: a systematic review. PLOS ONE 20(7):e0328833. doi:10.1371/journal.pone.0328833. **full**. `schewski2025_stress_acoustic_review`
15. Wang Q, Xu F, Wang X, Wu S, Ren L, Liu X (2025). How anxiety state influences speech parameters. Brain Sci 15(3):262. doi:10.3390/brainsci15030262. **abs** (full text downloaded, abstract relied on). `wang2025_anxiety_speech_network`
16. Giddens CL, Barron KW, Byrd-Craven J, Clark KF, Winter AS (2013). Vocal indices of stress: a review. J Voice 27(3):390.e21-29. doi:10.1016/j.jvoice.2012.12.010. **abs**. `giddens2013_vocal_stress_review`
17. Lively SE, Pisoni DB, Van Summers W, Bernacki RH (1993). Effects of cognitive workload on speech production. J Acoust Soc Am 93(5):2962-2973. doi:10.1121/1.405815. **full-F**, abstract verified. `lively1993_cognitive_workload`
18. Moers C, Meyer A, Janse E (2017). Effects of word frequency and transitional probability on word reading durations of younger and older speakers. Lang Speech 60(2):289-317. doi:10.1177/0023830916649215. **abs**. `moers2017_word_frequency_reading_durations`
19. de Jong NH (2016). Predicting pauses in L1 and L2 speech: the effects of utterance boundaries and word frequency. IRAL 54(2):113-132. doi:10.1515/iral-2016-9993. **abs**. `dejong2016_pauses_boundaries_word_frequency`
20. Laubrock J, Kliegl R (2015). The eye-voice span during reading aloud. Front Psychol 6:1432. doi:10.3389/fpsyg.2015.01432. **full** (abstract relied on). `laubrock_kliegl2015_eye_voice_span`
21. Schwanenflugel PJ, Hamilton AM, Kuhn MR, Wisenbaker JM, Stahl SA (2004). Becoming a fluent reader. J Educ Psychol 96(1):119-129. doi:10.1037/0022-0663.96.1.119. **full-F**, abstract verified (sample sizes differ). `schwanenflugel2004_fluent_reader`
22. Miller J, Schwanenflugel PJ (2006). Prosody of syntactically complex sentences in the oral reading of young children. J Educ Psychol 98(4):839-853. doi:10.1037/0022-0663.98.4.839. **full-F**, abstract verified. `miller_schwanenflugel2006_complex_sentences`
23. Daane MC, Campbell JR, Grigg WS, Goodman MJ, Oranje A (2005). Fourth-grade students reading aloud: NAEP 2002 special study of oral reading. NCES 2006-469. https://files.eric.ed.gov/fulltext/ED488962.pdf. **full**. `naep2002_oral_reading_study`
24. Duong M, Mostow J, Sitaram S (2011). Two methods for assessing oral reading prosody. ACM Trans Speech Lang Process 7(4):14. doi:10.1145/1998384.1998388. **full**. `duong2011_oral_reading_prosody`
25. Benjamin RG et al. (2013). A spectrographically grounded scale for evaluating reading expressiveness. Read Res Q 48(2):105-133. doi:10.1002/rrq.43. **abs**. `benjamin2013_corfs`
26. Sabu K, Rao P (2024). Predicting children's perceived reading proficiency with prosody modeling. Comput Speech Lang 84:101557. **sec** (through arXiv:2405.19426, full). `sabu_rao2024_SECONDARY`
27. Brysbaert M (2019). How many words do we read per minute? J Mem Lang 109:104047. doi:10.1016/j.jml.2019.104047. **full** (abstract and one passage). `brysbaert2019_reading_rate_meta_analysis`
28. Cucchiarini C, Strik H, Boves L (2000). Quantitative assessment of second language learners' fluency by means of automatic speech recognition technology. J Acoust Soc Am 107(2):989-999. doi:10.1121/1.428279. **abs**. `cucchiarini2000_fluency_asr`
29. Cucchiarini C, Strik H, Boves L (2002). Quantitative assessment of second language learners' fluency: comparisons between read and spontaneous speech. J Acoust Soc Am 111(6):2862-2873. doi:10.1121/1.1471894. **abs**. `cucchiarini2002_read_vs_spontaneous`
30. Bosker HR, Pinget A-F, Quene H, Sanders T, de Jong NH (2013). What makes speech sound fluent? Lang Test 30(2):159-175. doi:10.1177/0265532212455394. **full**. `bosker2013_what_makes_speech_sound_fluent`
31. Suzuki S, Kormos J, Uchihara T (2021). The relationship between utterance and perceived fluency: a meta-analysis. Mod Lang J 105(2):435-463. doi:10.1111/modl.12706. **full** (accepted manuscript). `suzuki2021_fluency_meta_analysis`
32. Suzuki S, Kormos J (2020). Linguistic dimensions of comprehensibility and perceived fluency. Stud Second Lang Acquis 42(1):143-167. doi:10.1017/S0272263119000421. **abs**. `suzuki_kormos2020_midclause_pauses`
33. Tavakoli P (2011). Pausing patterns: differences between L2 learners and native speakers. ELT J 65(1):71-79. doi:10.1093/elt/ccq020. **abs**. `tavakoli2011_pausing_patterns`
34. Kahng J (2018). The effect of pause location on perceived fluency. Appl Psycholinguist 39(3):569-591. **abs** (DOI not shown on the page opened). `kahng2018_pause_location_perceived_fluency`
35. Munro MJ, Derwing TM (2001). Modeling perceptions of the accentedness and comprehensibility of L2 speech: the role of speaking rate. Stud Second Lang Acquis 23(4):451-468. doi:10.1017/S0272263101004016. **abs**. `munro_derwing2001_rate_ratings`
36. Trouvain J, Grice M (1999). The effect of tempo on prosodic structure. Proc. 14th ICPhS, 1067-1070. https://www.coli.uni-saarland.de/trouvain/trouvain_grice_1999.pdf. **full**. `trouvain_grice1999_tempo_prosodic_structure`
37. Janse E (2004). Word perception in fast speech: artificially time-compressed vs. naturally produced fast speech. Speech Commun 42(2):155-173. doi:10.1016/j.specom.2003.07.001. **full**. `janse2004_fast_speech`
38. Miller JL, Grosjean F, Lomanto C (1984). Articulation rate and its variability in spontaneous speech. Phonetica 41(4):215-225. doi:10.1159/000261728. **abs**. `miller_grosjean_lomanto1984_artic_rate_variability`
39. Crystal TH, House AS (1990). Articulation rate and the duration of syllables and stress groups in connected speech. J Acoust Soc Am 88(1):101-112. doi:10.1121/1.399955. **abs**. `crystal_house1990_articulation_rate`
40. Tsao Y-C, Weismer G (1997). Interspeaker variation in habitual speaking rate. J Speech Lang Hear Res 40(4):858-866. doi:10.1044/jslhr.4004.858. **abs**. `tsao_weismer1997_habitual_rate`
41. Jacewicz E, Fox RA, O'Neill C, Salmons J (2009). Articulation rate across dialect, age, and gender. Lang Var Change 21(2):233-256. doi:10.1017/S0954394509990093. **full-F**, abstract verified. `jacewicz2009_articulation_rate`
42. Quene H (2008). Multilevel modeling of between-speaker and within-speaker variation in spontaneous speech tempo. J Acoust Soc Am 123(2):1104-1113. doi:10.1121/1.2821762. **abs**. `quene2008_tempo_multilevel`
43. Pfitzinger HR (1998). Local speech rate as a combination of syllable and phone rate. Proc. ICSLP 1998. https://www.isca-archive.org/icslp_1998/pfitzinger98_icslp.pdf. **full**. `pfitzinger1998_local_speech_rate`
44. Wang D, Narayanan SS (2007). Robust speech rate estimation for spontaneous speech. IEEE Trans Audio Speech Lang Process 15(8):2190-2201. doi:10.1109/TASL.2007.905178. **full-F**, abstract verified. `wang_narayanan2007_speech_rate_estimation`
45. Wiget L, White L, Schuppler B, Grenon I, Rauch O, Mattys SL (2010). How stable are acoustic metrics of contrastive speech rhythm? J Acoust Soc Am 127(3):1559-1569. doi:10.1121/1.3293004. **abs**. `wiget2010_rhythm_metric_stability`
46. Liss JM et al. (2009). Quantifying speech rhythm abnormalities in the dysarthrias. J Speech Lang Hear Res 52(5):1334-1352. doi:10.1044/1092-4388(2009/08-0208). **abs**. `liss2009_rhythm_metrics_dysarthria`
47. Liss JM, LeGendre S, Lotto AJ (2010). Discriminating dysarthria type from envelope modulation spectra. J Speech Lang Hear Res 53(5):1246-1255. doi:10.1044/1092-4388(2010/09-0121). **full-F**, abstract verified. `liss2010_envelope_modulation_spectra`
48. Lowit A (2014). Quantification of rhythm problems in disordered speech: a re-evaluation. Philos Trans R Soc B 369(1658):20130404. doi:10.1098/rstb.2013.0404. **full-F**, abstract verified. `lowit2014_rhythm_metrics_reevaluation`
49. McIntosh S, Smit R, Saito D, Minematsu N, Kamper H (2026). Self-supervised speech comparison for L2 phone, rhythm, and intonation scoring. arXiv:2607.13721. **full** (preprint). `mcintosh2026_ssl_speech_comparison_rhythm`
50. Honig F, Batliner A, Weilhammer K, Noth E (2010). Automatic assessment of non-native prosody for English as L2. Speech Prosody 2010. https://www.isca-archive.org/speechprosody_2010/honig10_speechprosody.pdf. **full**. `honig2010_nonnative_prosody_assessment`
51. Wightman CW, Shattuck-Hufnagel S, Ostendorf M, Price PJ (1992). Segmental durations in the vicinity of prosodic phrase boundaries. J Acoust Soc Am 91(3):1707-1717. doi:10.1121/1.402450. **abs**. `wightman1992_preboundary_lengthening`
52. Camara M, Blanco JL, Godino JI, Choi J-Y, Shattuck-Hufnagel S (2026). Word lengthening as a function of utterance position: a multi-corpus study. arXiv:2606.23232. **full** (preprint). `camara2026_word_lengthening_position`
53. Krivokapic J (2007). Prosodic planning: effects of phrasal length and complexity on pause duration. J Phon 35(2):162-179. doi:10.1016/j.wocn.2006.04.001. **full-F**, abstract verified. `krivokapic2007_prosodic_planning_pause`
54. Zvonik E, Cummins F (2003). The effect of surrounding phrase lengths on pause duration. Eurospeech 2003, 777-780. https://www.isca-archive.org/eurospeech_2003/zvonik03_eurospeech.pdf. **full**. `zvonik_cummins2003_pause_duration_phrase_length`
55. Rosen K et al. (2010). Automatic method of pause measurement for normal and dysarthric speech. Clin Linguist Phon 24(2):141-154. doi:10.3109/02699200903440983. **abs**. `rosen2010_pause_measurement`
56. Lovgren T, van Doorn J (2005). Influence of manipulation of short silent pause duration on speech fluency. DiSS'05, 123-126. https://www.isca-archive.org/diss_2005/lovgren05_diss.pdf. **full**. `lovgren_vandoorn2005_pause_duration_fluency`
57. Tanaka A, Sakamoto S, Suzuki Y (2011). Effects of pause duration and speech rate on sentence intelligibility in younger and older adult listeners. Acoust Sci Technol 32(6):264-267. doi:10.1250/ast.32.264. **full**. `tanaka2011_pause_rate_intelligibility`

### Could not open (not cited; what was wanted from each)
- Goberman, Hughes & Haydock 2011, Speech Communication 53:867-876 (403): acoustic measures of anxiety in student speeches; whether rate rises or falls.
- Laukka et al. 2008, primary text (login wall): definition of "percentage of silence" and the articulation-rate result.
- Lewin, McNeil & Lipson 1996, J Psychopathol Behav Assess 18:387-402: pauses in speech-fearful speakers.
- Muller, Grossmann-Hutter, Jameson, Rummer & Wittig 2001, User Modeling 2001: articulation rate and pauses under time pressure against cognitive load.
- Ruinskiy & Lavner 2007, IEEE TASLP 15(3):838-850: MFCC template matching rule for breath sounds and its thresholds.
- Fuchs, Petrone, Krivokapic & Hoole 2013, J Phon: inhalation depth and pause duration against upcoming sentence length.
- Arvaniti 2012 and White & Mattys 2007, J Phon: stability and definitions of rhythm metrics.
- Bolanos et al. 2013, Speech Communication 55:221-236; Bailly et al. 2022 (HAL, bot wall); Sabu & Rao 2021 and 2024 primary texts: features and accuracy of automatic oral reading prosody scoring.
- de Jong, Groenhout, Schoonen & Hulstijn 2015, Appl Psycholinguist 36:223-243: correcting fluency measures for the speaker's own L1 baseline.
- de Jong, Pacilly & Heeren 2021, Assessment in Education 28(4): current Praat scripts for speed and breakdown fluency.
- Tilsen & Tiede 2023, J Phon: "local relative rate" from warping curves.
- Zellner 1994; Duez 1985 (no abstract in PubMed); Butcher 1981; Ruder 1973; Grosjean & Lane 1974 and 1976: perceptual thresholds for pauses and the weight of pauses against articulation in perceived reading rate.
- Turk & Shattuck-Hufnagel 2007, J Phon: size and domain of phrase-final lengthening.
- St. Louis & Schulte 2011: definition of cluttering.
- Rodero 2012, Text & Talk 32(3): radio reading rates. Two MDPI Languages 2023 papers on pauses against tempo and on pause length perception (403).
- Liss et al. 2009 full text (captcha): metric definitions and which metrics discriminated.

### Unsourced, to verify (general knowledge or search-result summaries only; not evidence)
- That anxious public speakers "speak too fast": common in rubrics and coaching texts; not confirmed by any source opened here.
- Goberman et al. 2011: higher anxiety went with slower speech, more pauses and a higher share of pause time (search summary only).
- Muller et al. 2001: faster articulation under time pressure; silent pause defined as 200 ms or more (search summary only).
- Ruinskiy & Lavner 2007: 98 % correct identification, 96 % specificity (search summary only).
- Ruder 1973: pause-detection threshold 23 ms, optimal fluent pause 186 ms, minimal hesitation pause 505 ms (search summary only).
- Butcher 1981: listeners need about 80 ms to hear a pause at a tone-group boundary and about 220 ms within one (from memory).
- Goldman-Eisler 1968: most variation in overall speaking rate comes from pausing, not articulation (from memory; [38] alludes to this view and disputes it).
- Rodero 2012: 160-180 words per minute recommended for radio news (search summary only).
- de Jong et al. 2015: fluency measures corrected for the speaker's L1 behaviour predict proficiency better for syllable duration (search summary only).
- St. Louis & Schulte 2011: cluttering as speech "too fast overall, too irregular, or both", with excessive disfluencies, collapsed syllables or abnormal pauses (search summary only).