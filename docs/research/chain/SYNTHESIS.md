# Research round 2: synthesis across the four chain reports (2026-10-02)

Method, as the owner set it: for each flaw, (1) the reasons behind it, (2) the pattern each reason leaves in the signal, taken from
that reason's own literature, (3) the method that captures that pattern, searched for by the pattern and often found in another
field under another name, (4) whether the project can compute it.

Reports (each with `sources/*.txt` holding URL, read status and the passages relied on):
`pace_pauses/REPORT.md` (57 sources), `disfluency/REPORT.md` (52), `pitch_emphasis/REPORT.md` (about 60), `volume_clarity/REPORT.md` (103).
Citation check: `VERIFICATION.md` in this folder (section 7 below summarises it). No code was changed in this round.

## 1. What the chain changed in our picture of each flaw

### Pace
- **Rushing is not uniform compression.** A reader who speeds up raises articulation rate by 13 to 18 % and mostly gains time by
  deleting or shortening pauses and removing phrase breaks; unstressed syllables and vowels shrink more than stressed ones
  (Trouvain & Grice 1999; Janse 2004). Our edit (uniform time-scale modification of 5 to 8 words) is the least natural form.
- **Nervousness does not show as faster articulation in any source opened.** It shows as more silence: more and longer silent
  pauses, a higher share of silence (r = .36 with state anxiety), and a raised pitch level. One 2025 systematic review: "No consistent
  acoustic patterns were identified for fear or anxiety." All anxiety studies used spontaneous or prepared speech, none read speech.
  The one paper on public-speaking anxiety acoustics (Goberman et al. 2011) could not be opened by any of the four agents.
- **Processing difficulty is local:** single words lengthen (low frequency, low predictability) and a pause is more likely before a
  hard word. The method is in the reading-tutor literature: per-word "latency" (silence before the word) and "production" (word
  duration) contours, each correlated with a fluent reading of the same text (Duong, Mostow & Sitaram 2011).
- **Low reading skill:** word-by-word reading, two-word groups, long pauses inside sentences. Method from second-language fluency
  research: mean length of run (words between pauses), r = .72 with rated fluency in a meta-analysis (Suzuki et al. 2021).
- Other patterns with a published measure: tempo irregularity (spread of the local tempo ratio along an alignment with a reference),
  tempo drift over the passage, missing phrase-final lengthening (80 ms effect, the same size as our aligner's boundary error).

### Pauses
- **Where the pause falls matters more than how long it is.** Pauses inside a clause have the strongest link to rated disfluency;
  pauses at sentence ends and commas are normal and their length grows with the length of the neighbouring phrases.
  Listener data: silences inside fluent speech of about 0.06 / 0.12 / 0.21 / 0.40 s were judged disfluent in 13 / 34 / 72 / 94 % of
  samples (Lövgren & van Doorn 2005). Our "inserted pause" rule matches the best-supported harmful pattern, but it reports single
  events; the literature's measure is the count and total duration of within-phrase pauses.
- **Breathing:** readers breathe every 4 s on average, inter-breath pause 0.64 s (0.25 to 1.8 s), and only about 2 to 3 % of breaths
  fall at ungrammatical places (Wang et al. 2010). A pause of 250 ms or more is a breath candidate (13.6 % of such pauses are not breaths). An audible inbreath inside a
  pause can split our "longest silent run" and under-measure the pause.
- A simple pause share does not separate readers (our own test 0.10 to 0.28; literature agrees).

### Disfluency (not in the product today)
- The owner's example holds. A developmental stutter and a planning or nervous hesitation differ in unit, repeat count, position,
  duration and accompaniment:
  - stuttering: several rapid repeats of an onset consonant or syllable, prolonged continuants at syllable onsets (can exceed 1 s),
    blocks (silence inside a word or before its onset with a strong release), on stressed word-initial content-word positions;
  - planning: filled pauses (schwa-like, long, low and flat pitch, steady spectrum, 84 % next to a silence), single repeats of
    function words with the first token lengthened, restarts;
  - nervousness: more and longer silent pauses and higher pitch; fillers do not reliably rise;
  - misreading: false start then correction, back-step of one or two words.
- **The methods are in other fields:** reading-tutor miscue detection (compare what was decoded with the known text; insertions track
  repetitions, r = .73 across speakers; one reading-miscue study with a wav2vec 2.0 model: recall 0.83 at precision 0.29), filled-pause detection by pitch slope and spectral stability (Goto et al. 1999; Gabrea & O'Shaughnessy
  2000), alignment graphs with go-back, part-word and skip arcs (Kouzelis et al. 2023; Dysfluent WFST 2025; reading-tutor lattices),
  star-token CTC training criteria.
- **Not separable from audio alone, by the clinical sources:** tense against plain repetition, block against pause (annotator kappa
  0.25 to 0.37), prolongation against sound repetition. The product can label form and size, not cause.
- For fluent adults reading a prepared text the base rate is very low (0.21 % stuttered syllables; under 1 % of words disfluent in
  constrained speech), so this is a rare-event detector.

### Pitch variation
- **"Monotone" has at least five different patterns:** whole-passage span compressed (second-language readers, low arousal); contour
  that does not follow a skilled reading of the same text (unskilled or unengaged reading); the same contour repeated on every
  sentence (span normal); range present but on the wrong words; and raised level from nervousness (range not narrowed in any source
  opened). Long-term range measures cannot see contour shape: a slow rise and a repeated up-down give the same value.
- **Method from reading-fluency assessment and language testing: "pitch match"**, the correlation of word-level pitch values with a
  reference reading of the same words (r 0.34 to 0.39 with human intonation scores; unstable with fewer than 10 to 20 reference
  readers). This is the one measure of where the movement is, not how much.
- Our percentile range (P90 - P10) is the best uncorrected long-term measure in the charisma literature (r .52; SD .35; max-min .04),
  but no source validates it on a five-word window (validated windows: 10 s and 40 to 98 s), and centring on the clip median removes
  the whole-passage compression pattern, which then rests on the whole-clip check alone.
- A published monotone cut-off exists (pitch variation quotient below .15 over 10 s, Hincks 2005) but does not transfer to read
  text, where native readers sit at 0.13 to 0.15.

### Emphasis
- Patterns: no focus marking at all (prominence pattern flat), every word stressed alike, stress on a given or function word, one
  cue only (higher pitch without length). Focus is realised by a higher peak, a longer stressed syllable, more intensity and lowered
  pitch after the focus.
- Methods: prominence from the signal with no training (equal-weight sum of pitch, energy and duration z-scores, 79 % on read
  news; wavelet version 84 to 85 %), prominence-vector correlation with a reference reading, a text prior for which words should be
  accented (function-word list or accent-ratio dictionary).
- Correction to earlier research: for read English the three cues are within 1.4 points of each other and equal weights lose about
  0.7 points to tuned ones; spectral tilt ranks last or adds little in three of four sources. Our equal weights are defensible.

### Sentence endings (not in the product today)
- Patterns: rising ending on a statement (late rise on the last word), weak final fall in unskilled reading, no declination across
  the sentence (norm 1.2 to 2.7 st/s for 2 to 4 s news utterances; only 71.5 % of professional phrases fall), creak at the end.
- Methods: sentence-final pitch change at full stops (direction only is defensible), per-sentence regression slope.

### Volume and projection
- **A quiet voice is not just a lower level.** Lower vocal effort tilts the spectrum toward low frequencies, lowers pitch and first
  formant and shortens vowels; a gain change leaves these untouched, and listeners use that to tell effort from distance.
  Our gain-fade edit is the recording pattern, not the speaker pattern. The method is spectral balance (alpha ratio, spectral
  emphasis) together with pitch, relative to the speaker's own median.
- **Trailing off:** amplitude downdrift across the phrase and a final drop, with laxer phonation; it also occurs in good speakers, so
  only "more than the reference" or "more than the speaker's other phrases" is defensible. Measure: per-phrase level slope and
  last-word drop, minus the reference's own.
- Absolute loudness and projection to a room cannot be measured from an upload.

### Clarity
- Patterns of mumbling: smaller vowel space, unreleased final stops, weaker consonants, less energy at 1 to 3 kHz, shallower slow
  envelope modulation, formants pulled toward neighbouring sounds as vowels get shorter, missing segments.
- **The method was already in our hands under another name.** The per-word aligned posterior that the aligner produces is, by the
  published definition, a goodness-of-pronunciation score ("GOP-CTC-align", "articulatory precision"), r about 0.7 with rated
  intelligibility per speaker on pathological speech. The earlier feature research dismissed it as "confidence, not a validated
  construct". Its confounds (noise, tempo, accent) stand; the proposal is to use it relative to the clip's own median and to the
  reference's score for the same word. Untested on healthy readers, short windows, or character-level models.
- Other methods: greedy decode against the transcript for dropped sounds, reference distance on aligned words (band-envelope
  correlation, wav2vec 2.0 feature distance).

### Voice quality under nervousness
- Not supported as a detectable flaw from one clip of a new speaker: jitter and shimmer directions disagree between studies and
  follow loudness, tremor measures are defined on sustained vowels, raised pitch needs the speaker's own calm baseline.

## 2. Findings that cut across flaws

1. **Nervousness.** Across three reports the evidence is the same: more and longer silent pauses and a raised pitch level; nothing
   reliable about rate, range or voice quality in read speech. It can only be judged against the speaker's own baseline, which an
   upload does not give. The rubric word "hurried" has no acoustic study behind it in what was opened.
2. **One reference reading is the weak configuration.** The studies that compare a reading with a template used several fluent
   readers (averaged profiles; 10 to 20 native readings; models trained on many adult voices). With one reference, legitimate
   differences in phrasing and emphasis count as error. The project has six calibration readers of one text and one reference per
   speech.
3. **Much of what the literature measures is already computed and not reported:** pause counts by position, words per run,
   decomposition of tempo into articulation and pausing, spread of the local tempo ratio, the word posterior, spectral balance.
4. **The aligner's word-boundary error (48 to 89 ms) is the ceiling** for per-word duration measures; effects of that size
   (phrase-final lengthening, 80 ms) are out of reach.
5. **Almost every method was validated on another population** (children, second-language speakers, patients, spontaneous speech).
   No opened study validates any of them on fluent adults reading a prepared text.
6. **Synthetic flaws:** published recipes exist for word and part-word repetition, prolongation, silence "blocks" and inserted
   recorded fillers. Reported limits: waveform edits sound unnatural (opinion score 2.2 against 4.1), transfer to real speech is
   partial, and artificial prolongation hurt one detector.

## 3. Candidate measures, all four reports together

"Now" = computable from what the pipeline already produces, thresholds only, no training.

| Tier | Measure | Flaw and pattern it captures | Field it comes from | Evidence | Now? |
|---|---|---|---|---|---|
| 1 | Within-phrase pause count and total duration, against the reference | Pauses: hesitation inside a clause | second-language fluency, reading research | strong for second-language spontaneous speech; not tested on read text | yes |
| 1 | Tempo decomposition: speech-time ratio, pause-count ratio, mean-pause-duration ratio | Pace: rushing by dropping pauses versus by faster articulation | fluency assessment by ASR | strong | yes |
| 1 | Mean length of run (words between pauses) | Pace: word-by-word reading | second-language fluency | strong (learners) | yes |
| 1 | Inserted material: greedy decode against the transcript | Disfluency: repetition, restart, some fillers | reading tutors, miscue detection | strong for the idea; precision low (0.29 at recall 0.83 for a wav2vec 2.0 model) | yes |
| 1 | Word posterior relative to clip median and to the reference word | Clarity: mumbling, dropped sounds | pronunciation scoring, clinical intelligibility | strong elsewhere, untested here | yes |
| 1 | Pitch match: per-sentence correlation of word-level pitch with the reference | Pitch: movement on the wrong words, unengaged reading | reading-fluency assessment, language testing | moderate (r 0.34 to 0.39) | yes |
| 1 | Whole-clip percentile span (existing) | Pitch: whole-passage compression | forensic and charisma phonetics | moderate | yes |
| 2 | Per-word latency and production contours against the reference | Pace: slowing or hesitating before a hard word | reading tutors | moderate | yes |
| 2 | Tempo irregularity (spread of the local tempo ratio) | Pace: uneven rhythm | second-language scoring | moderate, one preprint | yes |
| 2 | Orphan voiced gap plus pitch and spectral stability run | Disfluency: filled pause, prolonged vowel | spoken-dialogue filled-pause detection | moderate, other languages | yes |
| 2 | Silence inside a word's aligned span, against the reference word | Disfluency: block, syllable-by-syllable reading | stuttering literature (pattern), no validated detector | weak for detection | partly |
| 2 | Spectral balance and pitch against own median | Volume: low effort versus recording gain | vocal-effort phonetics | strong pattern, no threshold | yes |
| 2 | Per-phrase level slope and last-word drop, minus the reference's | Volume: trailing off | clinical voice, declination studies | moderate, no norms | yes |
| 2 | Sentence-final pitch change at full stops (direction) | Endings: rising or weak endings | reading research, uptalk phonetics | weak to moderate after the check (the main study found it predicts reading rate only, in Mandarin-speaking children) | yes |
| 2 | Prominence-vector agreement with the reference, and spread of stress points | Emphasis: none, or everything stressed | language testing | moderate, small effect | yes |
| 3 | Per-sentence declination slope | Endings: flat sentence | intonation phonetics | moderate | yes |
| 3 | Two-sided emphasis check with a function-word prior | Emphasis: stress on the wrong word | prominence prediction from text | moderate | yes (list) |
| 3 | Alignment graph with repeat, part-word and skip arcs | Disfluency with time stamps and a corrected alignment | disfluent forced alignment | strong on synthetic data | no: new decoder |
| 3 | Reference distance on aligned words (band envelope, wav2vec features) | Clarity | intelligibility assessment | strong with several references | to add |
| 3 | Breath-pause location | Pauses: breath in the wrong place | speech breathing research | strong pattern | partly |
| open | Nervousness cues (raised pitch level, share of silence, voice quality) | needs the speaker's own calm recording | stress and anxiety research | contradictory for voice quality; level and silence consistent | data question answered in section 8: own baseline can be asked for; open anxious-reading corpora need an academic request |
| open | Interval rhythm metrics, pause share across speakers, vowel space, creak detection, trained disfluency / prominence / breath detectors, absolute effort class | needs phone alignment, many readers of one text, or a pretrained model | various | mixed | data question answered in section 8: all obtainable in days |
| no | Absolute loudness of an upload | - | - | no calibration tone in an upload; no dataset fixes this | no |

## 4. New patterns for the bad spectrum (controlled edits the literature describes)

- Natural rushing: speed-up plus deletion or shortening of the pauses in the stretch (not uniform compression alone).
- Hesitation: one content word stretched and a silence inserted before it.
- Word-by-word reading: short silences (0.15 to 0.3 s) after every word or every second word of a stretch.
- Uneven tempo: random per-word time-scale factors with mean 1.
- Repetition: one copy of a function word with the first token stretched and a short pause (typical speaker), or two or more rapid
  copies of the onset of a stressed content word (stuttering form).
- Prolongation: word-final rhyme stretched (typical), onset continuant stretched up to about 1 s (stuttering form).
- Block: silence inside a word before a stop release.
- Filled pause: needs a recorded or synthesised filler; cannot be made from the clip itself.
- Low effort: gain fade plus spectral tilt plus slight pitch lowering (instead of gain alone).
- Trailing off: gain and tilt ramp anchored at the sentence end.
- Misplaced emphasis: move the pitch peak to another word; boost a function word; de-emphasise all stressed words.
- Rising ending: linear rise over the last syllable; flattened final fall.
- Repeated contour: impose one sentence's contour on the others.

## 5. Corrections to the earlier research (docs/PAPERS.md and the round-1 reports)

1. A numeric monotone cut-off does exist (Hincks 2005, PVQ below .15), contrary to the rubric report; it does not transfer to read text.
2. Departure 3 in `docs/PAPERS.md` (pitch is the weakest emphasis cue, spectral balance missing) rests on one study of conversational
   dialects; for read English equal weights are defensible.
3. Departure 7 (the 1.2 s inserted pause is longer than read-speech pauses): inter-breath pauses in passage reading reach 1.8 s.
4. The aligned word posterior is a published articulation measure, not merely "confidence".
5. Spectral balance (alpha) is the main level-independent correlate of vocal effort; the feature report kept it as a diagnostic only.
6. The alignment report's star-token test used the zero-score form; the published criteria use averaged non-blank probability with a
   penalty, which was not tested.
7. No single minimum pause length is supported for all uses: 250 ms is best for breath pauses, reading-prosody studies use 100 to
   150 ms, and listeners judge 0.2 s silences inside phrases as disfluent in most samples.

## 6. What could not be sourced

- Goberman, Hughes & Haydock 2011 (acoustics of public-speaking anxiety): blocked for all four agents. It is the one paper most
  likely to answer "does nervousness speed up or flatten a prepared speech".
- Any norm for fluent adults reading a prepared text (disfluency rate, intensity declination, local range ratio between readers).
- A perceptual threshold for local tempo change inside a sentence, for "emphasis lost", and for an uptalk rise.
- A validated measure of between-sentence contour repetition; any study of "uneven loudness" or "mumbling" as rated flaws in healthy
  speakers; tremor or breathiness in nervous public speakers.
- Validation of posterior scores or reference distances on short windows, healthy readers, a single other-speaker reference, or
  character-level CTC.

## 7. Verification of citations

A separate agent checked 109 claims against primary text fetched directly (PDFs searched locally, PubMed, PMC, arXiv, Crossref), not
through model-written summaries: 30 pace and pauses, 26 disfluency, 25 pitch and emphasis, 28 volume and clarity. Full tables are in
`VERIFICATION.md`.
- No paper is missing or misattributed and no invented number was found. All six 2026 preprints resolve.
- Six claims needed a correction and nine a wording or context fix. The corrections are noted at the top of each report and applied
  in this file and in `docs/PAPERS.md` Part 2.
- Two corrections change how much a ranked measure can be trusted: the precision of decode-against-transcript miscue detection
  (0.29, not about 0.5) and the sentence-final pitch change (its main study found a link to reading rate only).
- Not checked: about 35 of the 46 PubMed abstracts in the volume and clarity report, the abstract-only items of the pitch report,
  the edit-recipe papers of the disfluency report, and a dozen smaller sources listed at the end of `VERIFICATION.md`.

## 8. Can the required data be obtained? (added after the owner's correction: ask this first)

Survey in `data/REPORT.md` (licences read directly; items marked VERIFIED or UNVERIFIED there). Result: for every measure and edit
pattern above, including everything first set aside, data or a pretrained model can be had within days, with one exception.

- **Many readers of one text (the weak single reference):** LibriVox Gettysburg collection has 15 readers plus 4 solo items (the
  project uses 9); LibriVox weekly poetry has about 1,400 items with a median of 14 readers each, public domain; VCTK (110 speakers,
  Rainbow passage, CC BY 4.0); Speech Accent Archive (2,140 readers of one paragraph, 579 native, non-commercial share-alike); EARS
  (107 speakers, Rainbow passage in regular, fast, slow, loud, whisper; non-commercial).
- **Real flaws, same speaker with and without:** fast against regular readings (EARS, CHAINS); soft against normal effort (AVID, 50
  speakers, CC BY 4.0, with calibration tone; Lombard GRID); enunciated against default (Expresso, 4 speakers); emphasis-marked words
  (Expresso); read sentences with expert fluency and prosody scores (speechocean762, CC BY 4.0, redistributable).
- **Disfluency:** time-stamped fillers and repeated words (PodcastFillers, 145 h, research licence on annotations), stuttering clips
  (SEP-28k labels non-commercial; UCLASS for research), acted verbatim disfluent speech (DisfluencySpeech, Apache-2.0).
- **Labels for prominence, breath, creak:** crowdsourced LibriTTS prominence (CC BY 4.0), Respiro-en breath labels and model (MIT),
  DeepFry creak detector (MIT).
- **Pretrained models that stand in for training data** (all small enough for a laptop CPU on a 20-40 s clip unless noted):
  prominence (`emphases`, 3 MB, MIT; wavelet prosody toolkit, no weights), breath (Respiro-en, 35 MB), creak (DeepFry), phoneme-level
  CTC for goodness of pronunciation (wav2vec 2.0 phoneme models, Apache-2.0, 0.4 to 1.3 GB), phone aligner (Montreal Forced Aligner
  English model, CC BY 4.0), disfluency classifiers (1.3 GB, OpenRAIL / Apache-2.0), verbatim transcription with fillers
  (CrisperWhisper, non-commercial). No pretrained vocal-effort classifier was found; AVID would be its training data.
- **Own baseline:** a published stress-detection app asks each user for a calm recording of at least a minute and scores against it.
  The team can also record its own protocol the way EARS, CHAINS and AVID do: one passage read habitually, then fast, flat, mumbled,
  quiet, trailing off, with planted repeats and fillers. Rights are then the team's own. Caveat from the literature: acted flaws are
  more exaggerated than natural ones.
- **The exception:** real nervous or anxious speech with the same speaker calm exists only behind academic requests that forbid
  redistribution (VerBIO, StressID, BESST, SUSAS). Also not openly available: adult read-aloud speech with time-stamped miscue labels,
  professional read news with human pitch-accent labels (LDC, paid), healthy clear-versus-mumbled style pairs with ratings (LUCID page
  dead), English public-speaking recordings with delivery ratings.
- **Licence classes matter for the release:** public domain and CC BY sources can be redistributed in the dataset; non-commercial
  sources can be used for calibration and validation but derived clips would carry the non-commercial term.
