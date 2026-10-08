# Disfluency: flaw -> reasons -> patterns -> detection methods (2026-10-02)

> **Corrections after the citation check (`../VERIFICATION.md`, 2026-10-02).** (1) Section 4, measure 1: at recall 0.83 the wav2vec 2.0
> model in Gao et al. 2024 had precision 0.29 (F1 0.43); precision 0.52 belongs to Whisper at recall 0.53. (2) Bosker et al. 2013 is
> openly available and contains the three R2 values, so its status is full text. All other checked claims (26) were confirmed.

Scope: stutters, hesitations, fillers, repetitions, restarts in read or prepared speech. Literature research only. Every quoted
passage is in `sources/<name>.txt` with its URL and read status; the file name is given in brackets after each claim. "Abstract"
after a claim means only the abstract was read. Nothing here was run on project data.

Short answer: the literature separates five surface forms (filled pause, repetition, prolongation, block or misplaced silence,
restart with correction) and four reasons that matter for a read-aloud task (developmental stuttering, planning or word-access
trouble, state anxiety, misreading with self-correction), plus cluttering as a contrast. The reasons differ in which forms they
produce, where the forms fall, how long they last and how many times a unit is repeated. They do not differ in a way that audio
alone can assign with confidence: the clinical sources say tension, the speaker's sense of losing control and physical signs
carry the distinction. A product can therefore label the form and its size, not the cause.

## 1. Summary table

Evidence strength: A = full text read, measured on real speech, numbers given; B = full text read but simulated data, children,
another language, or one small study; C = abstract or secondary only.

| Form (flaw) | Reason | Pattern the reason leaves | Best detection method(s) | Computable now? | Training? | Evidence |
|---|---|---|---|---|---|---|
| Filled pause "uh/um" | Planning, word access (typical) | Schwa-like vowel, much longer than the same vowel in words; low, flat or slowly falling F0; steady spectrum; 84 % next to a silence; more at unit boundaries; "um" followed by a longer delay than "uh" | (a) voiced material in an inter-word gap that the aligner did not assign to a word, then (b) Goto / Gabrea rule: F0 slope small, spectral change small, F0 low for the speaker, duration floor | Yes: gaps, voicing, F0, MFCC frames exist. Gap (a) is unreliable when the aligner absorbs the filler into a neighbour | No (thresholds) | A for acoustics; B for the detector (Japanese, Switchboard, preliminary) |
| Filled pause | State anxiety | Mixed: "ah" did not rise under anxiety in Kasl & Mahl; rose with evaluation apprehension in Christenfeld; phobics showed more | Same detector; cause not separable | Yes | No | C |
| Filled pause | Reading aloud | Rare; children reading "tend to use a silent pause instead" | Same | Yes | No | B (children, Portuguese) |
| Word / phrase repetition | Planning (typical) | One repeat, on unstressed function words (96 %); first token lengthened, second normal; same pitch level; often a pause at the interruption | Alignment graph with go-back arcs (Kouzelis, Alharbi, Proença, Guo); or insertions in free decode vs transcript | Decode-vs-transcript: yes. Graph: needs a Viterbi over a modified graph (k2 or own code) | No | A for pattern; A/B for method |
| Sound / part-word repetition | Developmental stuttering | Several rapid iterations of an onset consonant, cluster or syllable; on stressed or utterance-initial syllables, content words, word onsets; with tension; event about 1 s | Same graph with part-word arcs; phoneme-level "revisit" rule | Graph: to add. Character-level CTC variant untested in the literature | No | A for pattern; B for method (simulated data, 100 % only on TTS) |
| Prolongation | Planning (typical) | Short, at word ends, before a pause; rhyme before the interruption point lengthened | Segment duration against the reference reading of the same word; spectral-stability run | Yes: character timing and MFCC frames | No | A for pattern; B for method |
| Prolongation | Developmental stuttering | Long (can exceed 1 s), on continuants at syllable onsets | Frame-to-frame similarity >= 0.9 for a run longer than a rate-scaled length (Alharbi); F0 + envelope stability (Goto) | Yes | No | A pattern; B method (no accuracy for the detector alone) |
| Block | Developmental stuttering | Tense closure on a stop or glottal closure before a word-onset vowel; silence inside a word or before its onset; intense burst at release | Silence inside a word's aligned span or abnormal pre-onset gap; "irregular pause" rule (UDM) | Partly: level frames exist, within-word silence is not measured today | No | A pattern; C method (human kappa 0.25 to 0.37; best trained F1 0.3 to 0.57) |
| Silent hesitation | State anxiety; planning | More and longer silent pauses, higher share of time silent, higher F0 | Already the product's pause criterion | Yes (covered) | No | C (abstracts), consistent across three studies |
| False start + self-correction | Misreading (decoding), monitoring | Word begun, cut off, then said correctly; whole-word repeat; back-step of one or two words; syllable-by-syllable reading with intra-word pauses | Task lattice with syllable false-start arcs and one- or two-word back-step (Proença); inter-word latency (Beck) | Latency: yes. Lattice: to add | No | B (children; 15 % miss at 5 % false alarm) |
| Collapsed / fast irregular speech | Cluttering | Rate perceived "too fast overall, too irregular, or both"; collapsed syllables; more typical than stuttering-like disfluencies | Articulation rate on fluent stretches; ratio of disfluency types | Rate: yes | No | B; not revealed by oral reading (AUC 0.61 to 0.66) |

## 2. Reasons, patterns, methods

### 2.0 Base rates: how much disfluency a read-aloud task contains

- Spontaneous speech of typical speakers: "at a rate of around 6 per 100 words" [lickley2017]; "5.97 disfluencies every 100
  words" for repeats, restarts and fillers together [bortfeld2001]; "under 1% for constrained human-computer dialog, to 5-10% for
  natural conversations" [shriberg1999_phonetic]. Filled pauses alone: 1.3 per 100 words (range 0.18 to 6.66 across 64 speakers),
  2.6 and 1.6 to 2.2 in American corpora [lickley2017].
- Reading aloud: "it is relatively rare for fluency to break down" [lickley2017]. Adults who do not stutter: 0.0 % stuttered
  syllables in monologue and 0.21 % (SD 0.53, max 2) in oral reading of a 200-syllable text, n = 17 [ritto2016_speech_tasks].
- Stuttering: "around 10 stuttering events per 100 words", up to 50 % in severe cases [lickley2017]. Adults who stutter: 16.84 %
  stuttered syllables in monologue, 12.91 % in oral reading, 1.47 % in choral reading [ritto2016_speech_tasks]. "in reading out
  loud - typical speakers are only rarely disfluent, whereas many AWS stutter at a higher rate than in spontaneous speech"
  [lickley2017]. So reading removes planning disfluency and leaves stuttering in place.
- Children reading sentences (age 6 to 10, Portuguese): false start with correction 4.77 % of words, word repetition 2.25 %,
  intra-word pause 2.32 %, phoneme extension 1.78 %, insertion 0.94 % [proenca2015]. A reading authority quoted by Mostow puts
  the "frustration level" at "more than one miscue per 10 text words - including not just missed words but hesitations,
  repetitions, and self-corrections" [mostow2006].
- No norm for fluent adults reading aloud a prepared text was found (section 5).

### 2.1 Reason: developmental stuttering (motor execution)

Pattern, in the clinical literature's words [lickley2017 unless marked]:
- One cause, three realisations: "the three types are articulatory realizations of the same underlying difficulty: An inability
  to progress from one sound to the next." The speaker knows the word; "the main problem lies in executing the plan".
- Repetition: "an oral stop consonant or cluster (electr-tr-tr-tronically), or a whole syllable (au-au-au-australia) or short
  word (I I I work in an office). Such repetitions are typically very rapid and may consist of just one repeated token or (more
  often) several repeated tokens."
- Block: "a long, tense articulatory closure on a stop consonant ... But blocks also occur on the glottal closure before a
  word-onset vowel". Annotation schemes define it as "Gasps for air or stuttered pauses" [lea2021_sep28k] and "inappropriate
  breaks in different parts of the sentence in between or within words" [alharbi2017_wocci].
- Prolongation: "a sound that can be prolonged easily, like a continuant (ssssssssseven)".
- Release: "there is likely to be an intense burst, because of the extended build-up of subglottal pressure."
- Position: "stutters mostly occur on stressed syllables, or on utterance-initial syllables". Brown's factors as restated by Max
  et al.: more stuttering on consonant-initial words, on nouns, adjectives, verbs and adverbs, on words of five or more letters,
  and on the first three words of a sentence; in their oral-reading data the length, phonetic and grammatical factors were
  significant and the position factor was not [max2019_loci, WebFetch extraction]. Adults who stutter are dysfluent on content
  words; fluent speakers and young children on the function word before the content word [howell1999_abstract, abstract].
- Duration: "instances of stutters average around 1 second in duration, while rarely extending beyond 5 seconds" (Bloodstein via
  Guitar, secondary) [lickley2017]; in school-age children "approximately three-quarters of a second" [zebrowski1994_abstract,
  abstract].
- Contrast with typical disfluency: "it is relatively rare for a word or sound to be repeated more than once"; typical
  prolongation "is relatively short ... and it is more common at the ends of words in typical speech, rather than at the
  syllable onsets that are affected by stuttering. Blocking is not considered by researchers examining typical disfluency.
  There is no evidence of physical tension associated with typical disfluency".
- Variability: forms blend ("a tense prolongation of /s/ may vary in intensity, giving the impression of the rapid repetition
  of the sound"), and learned behaviours add fillers and starters ("So", "I mean", "well"), "monotone or unusual intonation",
  and deliberate slow prolongation [lickley2017]. Symptoms depend on "the communication situation, psychological factors, the
  linguistic complexity of an utterance" [bayerl2022_ksof].
- Anxiety is not the cause: "there is little support for theories of stuttering that place anxiety about speech at the centre",
  though anticipation raises the chance of stuttering on a word [lickley2017].

### 2.2 Reason: planning and word access in fluent speakers (typical disfluency)

- Structure: reparandum, interruption point, editing phase (empty, silent pause, or "I mean", "um", "uh"), repair
  [shriberg1999_phonetic, terms from Levelt 1983, which was not opened].
- Before the interruption point: "a lengthening of rhymes or syllables immediately preceding the interruption point"; in "the
  the" the first token "is lengthened considerably ... whereas the repair (Rep2) has about the same duration as the fluent
  counterpart"; the first token keeps the pitch contour "but just stretched out over more time"; cut-off words show "creaky
  voice on the last 20-50 ms"; 88 % of repeats of "the" / "I" had no coarticulatory transition, "most cases contained a pause at
  interruption"; "a" and "to" surface as full [ey], [t uw] in the reparandum [shriberg1999_phonetic].
- Repetition unit and place: "Lickley (1994) found that 96% of disfluent repetitions were on function words (very often the
  definite article, "the")"; they "typically repeat the pitch level as well as the word" [lickley2017]. Fluent speakers repeat
  the function word to delay the next content word [howell1999_abstract, abstract].
- Filled pause acoustics: vowel "typically close to schwa"; "vowels in filled pauses have much longer durations than the same
  vowels in fluent contexts" (700 filled pauses against 40,000 other tokens); "low in F0, and display a gradual, roughly linear
  ... fall"; F0 "about halfway between the preceding peak value and the speaker baseline" [shriberg1999_phonetic]. Switchboard
  "uh": mean 165 ms, median 180 ms, range 20 to 1200 ms; 83.72 % had an adjacent silent pause; "a long, steady vowel with low
  fundamental frequency F0 relative to the calculated average F0 for each speaker", with the caveat that F0 "was not very low"
  and "many examples with rising F0" exist [gabrea2000_filled_pause]. "um" is "just over 400 ms" [lickley2017]. Candidate
  fillers in podcasts mostly 150 to 400 ms; under 150 ms listeners could not tell them from other sounds
  [zhu2022_podcastfillers].
- Filled pause position and what follows: rate 43 per 1000 opportunities at an intonation-unit boundary, 27 after the first
  word, 13 later; "Um was followed by delays far more often than uh, 61 to 29% of the time"; fillers attach to the preceding
  word ("and-uh"), never the following one [clark_foxtree2002]. Only "6-10%" of repetitions and repairs have a filled pause at
  the interruption point [lickley2017].
- What triggers it: longer and more complex utterances; "Late-learned, less frequent words ... are therefore more likely to be
  preceded by hesitations"; "the probability of a word given the local context was inversely related to the probability of a
  hesitation preceding that word" [lickley2017]. Rates rise with planning load (director role, unfamiliar domain)
  [bortfeld2001].
- Reading removes most of this reason (2.0). What remains for a prepared reading is word-access trouble on hard words and the
  misreadings of 2.4.

### 2.3 Reason: nervousness / state anxiety in fluent speakers

- Mahl's split: "Under anxiety, the frequency of all speech disturbances, except the familiar "ah," showed a sizable increase.
  The frequency of ah's increased strikingly in a change from normal to a telephonelike conversation. ... the ah is functionally
  distinct from the other speech disturbances." [kasl_mahl1965_secondary: abstract as reproduced on a bibliography page].
  Bortfeld et al. report the same study as "a 41% increase in fillers (but not other kinds of disfluencies)" without visual
  contact [bortfeld2001].
- Fillers and anxiety are not simply linked: "numerous failures make it impossible to believe that the two are linked in any
  simple way"; ums rose when anxiety made the speaker attend to the speech (evaluation apprehension, self-consciousness)
  [christenfeld1996_abstract, abstract]. Speaking to a metronome cut fillers from 8.98 to 2.06 per minute at the same rate
  [clark_foxtree2002, reporting Christenfeld].
- Public speaking: social phobics "showed more filled pauses, had longer silent pauses, paused more frequently, and spent more
  time pausing than controls" [hofmann1997_abstract, abstract]. After treatment, lower state anxiety went with lower "mean and
  maximum voice pitch, high-frequency components in the energy spectrum, and proportion of silent pauses" and lower perceived
  nervousness, N = 71 [laukka2008_abstract, abstract]. Under the Trier stress test "participants paused more" while producing
  more words [buchanan2014_abstract, abstract].
- A small VR presentation pilot (10 speakers per cell) found syllable repetitions of 0.1 to 0.4 per 200 words in every stress
  condition while words per minute fell from 134 to 74; its prolongation and hesitation counts were non-monotonic
  [sandoval2025_vr_stress]. Weak, but it agrees with the clinical statement that multi-iteration sound repetition is not what
  nervous fluent speakers produce.
- Pattern, as far as the opened sources support it: more and longer silent pauses, higher pitch, and more of the typical forms
  (single repeats, false starts, sentence changes); not blocks, not multi-iteration part-word repetition, no tension. The owner's
  example therefore holds in the literature: a "nervous stutter" and a developmental stutter differ in unit (word or phrase
  against sound or syllable), count (one repeat against several), position (function word or unit boundary against stressed
  word-onset), duration (a fraction of a second against about a second) and accompaniment (silence and raised pitch against
  tension and a burst).

### 2.4 Reason: misreading and self-correction in oral reading; second language

- Miscue taxonomy: "addition, mispronunciation, omission, reversal, word provided, and repetition"; "An unprompted correction
  following each miscue was a self-correction", which shows the reader "has both detected and corrected a reading error"
  [nguyen2020_miscues, WebFetch extraction, children].
- Surface forms in read sentences: false start followed by correction is the most common; "children do not use filled pauses in
  this type of discourse ... tend to use a silent pause instead"; some pronounce "syllable by syllable" with silence between;
  children restart "a sentence from the beginning if a mispronunciation happens on the second or third word" [proenca2015].
  Readers "often jump back to the beginning of the phrase or sentence and reread, or skip hard words" [tam2003]; "a reading
  mistake is often accompanied by halting, disfluent reading" [mostow2006].
- Second language: fluency ratings of read speech are better predicted by objective temporal measures than those of spontaneous
  speech [cucchiarini2002_abstract, abstract]. In L2 Dutch spontaneous speech, pause measures explained 59 % and speed 54 % of
  perceived-fluency variance, repair measures (corrections, repetitions) 16 % [bosker2013_2014: abstract plus the first
  author's research note]. So listeners weight repairs less than pauses and speed.

### 2.5 Reason: cluttering (contrast)

- Definition: "segments of a conversation ... typically are perceived as too fast overall, too irregular, or both" (St Louis et
  al. 2007, quoted in [tomisato2024_cluttering]); "variable syllable durations, abrupt shifts in tempo", "collapsed syllables"
  [han2026_cluttering_review].
- Its disfluencies are the typical kind: ratio of normal to stuttering-like disfluencies below 1 indicates stuttering, 3 or more
  cluttering (Van Zaalen, quoted in [tomisato2024_cluttering]).
- It does not show in reading: oral-reading AUC 0.61 (ratio) and 0.66 (articulation rate) against 0.70 and 0.87 in monologue,
  32 patients; "oral reading is not useful for differential diagnosis" [tomisato2024_cluttering]. Objectively measured rate in
  people who clutter is sometimes within the normal range (same source, citing Bakker et al.).
- For this product cluttering reduces to the pace and clarity criteria (fast, irregular, reduced syllables) and adds no new
  disfluency form.

### 2.6 Methods per pattern

**M1. Forced alignment that tolerates repetition and omission (name in the field: weakly-supervised forced alignment, task-oriented
lattice, dysfluent WFST).**
- Definition: alignment graph A = T o Y o E_x (CTC topology, transcript acceptor, emissions). Replace the linear transcript
  acceptor Y by a modified one with non-consuming arcs: back to a word start (word and phrase repetition), from a later phone
  back to the word start (part-word repetition), forward over a word (deletion). Each forward arc has probability alpha, the
  extra arcs share 1 - alpha; "effective when alpha >= 0.9", alpha = 1 - 10^-beta, beta chosen per clip as 10(1 - OER)
  [kouzelis2023_wsfa]. Guo et al. scale the extra-arc weight by a Gaussian of the jump distance and read the events off the
  best path: revisiting a state is a repetition, skipping one is a deletion [guo2025_dysfluent_wfst].
- Data and accuracy: pretrained wav2vec 2.0 emissions, no training. Synthetic DisfluenTIMIT: phone-boundary recall 0.47 to 0.60,
  F1 0.52 to 0.60, F1 loss against a verbatim transcript 17.4 % to 3.8 %; real UCLASS: F1 0.53 to 0.54; "precision is only
  marginally affected due to the presence of false alarms" [kouzelis2023_wsfa]. Simulated (TTS) repetitions: detection "100%
  accuracy at the count level", deletions 50 %, insertions 12 %; phoneme error 34.13 % greedy against 9.95 % with the graph;
  adding Gaussian noise of sigma 0.1 to the emissions raised weighted error from 9.43 to 74.06 [guo2025_dysfluent_wfst].
  Children who stutter reading a passage (HMM lattice with sound, part-word and go-back arcs): word repetition 0 % missed at
  0.29 % false positives, sound repetition 60 % missed; a prompt-only language model missed 100 % [alharbi2018_lightly_supervised].
  Children reading (syllable false-start arcs, back-step of one or two words, arc weights "minimum of 1%"): 15 % miss at 5 %
  false alarm [proenca2015].
- Confounds: needs phone-level emissions in the published forms; fragile to emission noise; false alarms on text that itself
  repeats; does not model fillers or prolongation; "Intra-word repetitions are not modeled" [kouzelis2023_wsfa].

**M2. Free decode compared with the known transcript (name: post-hoc miscue detection, prompt-ASR alignment).**
- Definition: align the recogniser output to the prompt (SCTK-style edit alignment); insertions that match a prefix or a copy of
  nearby prompt words are restarts or repetitions; other insertions are added words or fillers [gao2024_miscue].
- Accuracy: Dutch children, wav2vec 2.0 large recall 0.83, Whisper precision 0.52 and F1 0.52; wav2vec-family models
  over-detect [gao2024_miscue]. Whisper with no prompt had no agreement with human word-correctness scores (MCC .01); forced
  decoding confidence correlated r = .45 with word correctness [molenaar2023_oral_reading]. For people who stutter (self-formulated
  short commands, not read text), 80.9 % of ASR errors were insertions, correlating r = .73 with part-word repetitions and .60
  with whole-word repetitions; blocks, prolongations and interjections did not raise the error rate significantly [lea2023_chi];
  insertions rose more than 13 times [mitra2021_va_dysfluent].
- Confounds: recognisers trained on clean text smooth disfluency out ("I-I-I am" becomes "I am" [lea2021_sep28k]; Whisper
  "eliminates many filler words, recurring utterances" [wagner2024_crisperwhisper]); "post-hoc methods perform poorly when ASR
  inaccurately transcribes verbatim speech" [smith2025_whisper_miscue]; a greedy decode "can introduce random phoneme
  insertions or jumps" [guo2025_dysfluent_wfst]. Detection without the text mislabels words such as "dodo" (same source).

**M3. Orphan acoustics: speech that no transcript word accounts for (names: VAD-minus-ASR candidates, garbage or star token,
inter-word latency).**
- Definition: "fillers such as 'uh' and 'um' will trigger the VAD model, but appear as silent gaps in the ASR output. These
  regions where VAD activates but ASR does not are candidate locations for fillers" [zhu2022_podcastfillers]. Reading-tutor
  form: inter-word latency = start of text word i minus end of text word i-1, "including "false starts, sounding out,
  repetitions, and other insertions, whether spoken or silent"" [beck2004]. Alignment-graph form: a self-loop star token at
  every state, scored as "the average probability of all non-blank tokens" with a penalty, aligned to "orphan" acoustics
  [gao2023_otc_btc, pratap2022_stc].
- Accuracy: candidates plus a trained classifier reach event F1 92.8 %; without the recogniser 71.0 %; a forced-aligner
  baseline 70.4 %; "um" is easier than "uh" (91.0 against 84.3) [zhu2022_podcastfillers]. A model on recogniser-derived data
  that includes latency correlates 0.78 with a human fluency test in children [beck2004]. The star token has no published
  accuracy as an alignment-time filler detector; in OTC and STC it is a training criterion.
- Confounds: candidates also include breaths, laughter and agreement sounds [zhu2022_podcastfillers]; a filled pause "has a bad
  influence on the phone alignment" [goto1999_filled_pause], so the aligner may stretch a neighbouring word over the filler
  instead of leaving a gap.

**M4. Filled pause and lengthening by F0 and spectral stability (name: filled-pause detection, bottom-up).**
- Definition (Goto): 10 ms frames; A_f = absolute slope of a least-squares line through log-F0 over 5 frames; A_s = combined
  slope and fit error of each band of the amplitude-normalised spectral envelope (below 3200 Hz, 200 Hz bands) over 10 frames;
  S_f, S_s = 10-frame means; P_fp(t) = exp(-(R S_f + (1 - R) S_s)^2 / W^2) with R = 0.034, W = 0.575; accumulate P_fp while it
  exceeds e^-1; a filled pause is declared when the sum exceeds 7e^-1 [goto1999_filled_pause]. Gabrea & O'Shaughnessy: voiced
  zones, keep low F0 relative to the speaker's mean, segment into vowel-sized units, keep units whose cepstral distance to a
  steady central vowel is small, keep those "bordered by silence with a minimal duration" [gabrea2000_filled_pause].
- Accuracy: recall 84.9 % (107/126), precision 91.5 % (107/117), 10 Japanese speakers [goto1999_filled_pause]. Switchboard:
  recall 71.43 % at 1.44 % false alarms, 92.86 % at 2.36 % (called preliminary; thresholds not printed)
  [gabrea2000_filled_pause].
- Confounds: misses on short fillers, "too large F0 changes", and "hoarse voices" (53.8 % recall for one male speaker with a
  low-frequency hoarse voice); false alarms on "continuous unvaried voiced sounds within words uttered with a flat F0"
  [goto1999_filled_pause]. Goto's method deliberately detects word lengthening too, so it does not separate a filler from a
  prolonged vowel. A Praat script for filled pauses without training data exists for Dutch and English, with the authors'
  warning that it "should not (yet) be used" for high-stakes assessment [dejong2021_abstract, abstract; algorithm not read].

**M5. Prolongation by frame similarity and duration (name: prolongation detection, autocorrelation of successive frames).**
- Definition: mark silence, then "two thresholds to decide whether two successive frames were similar, and whether the duration
  of similar frames was sufficient to count as a prolongation ... 0.9 was the best value for the first; but the second threshold
  had to be set dynamically, according to speaking rate" [alharbi2018_lightly_supervised].
- Accuracy: only the system-level figure is given: preserved stuttering events rose from 63 % to 70 % with the detector added
  [alharbi2018_lightly_supervised]. A neural net on read text by children who stutter, with word boundaries supplied, classified
  95 % of fluent and 78 % of dysfluent words [howell1997_abstract, abstract].
- Confounds: "prolongations are hard to classify in a rule-based way, since syllables vary in duration in fluent speech
  according to context" [lickley2017]; phrase-final lengthening and emphasis are legitimate lengthening; human agreement on
  prolongation is the lowest of all types (kappa 0.11 and 0.42) [lea2021_sep28k, bayerl2022_ksof].

**M6. Block and within-word silence (names: irregular pause, intra-word pause, stop-gap).**
- Definition: "any pauses occurring within a complete sentence are identified as irregular pauses", 20 ms resolution
  [lian2023_udm]; for syllable-by-syllable reading, low-energy segments of at least 220 ms inside the utterance are found by an
  energy threshold [proenca2015].
- Accuracy: no rule-based figure found. Trained detectors: block F1 55.9 and 56.8 [lea2021_sep28k]; 0.30 to 0.33 and 0.51 to
  0.54 with wav2vec 2.0 features [bayerl2022_w2v2]; block accuracy 54 to 72 % for a detector trained on synthetic data
  [zhou2024_yolo_stutter].
- Confounds: "a short silence can occur during the closure phase of a stop consonant"; "an absolute value for a hesitation is
  hard to justify" (a pause of 80 ms inside a tone group was judged excessive, 220 ms between groups) [lickley2017]; "the gasp
  for breath or pause is often inaudible" [lea2021_sep28k].

**M7. Repetition by similarity of adjacent segments (DTW on MFCC).** Only secondary reports were opened: syllable repetition
accuracy 83 % and 94.35 % on small sets with manual segmentation [sheikh2022_review], removal "through correlation analysis of
MFCC and Linear Predictive Coefficients" [harvill2022_frame_level]. Not relied on.

**M8. Trained detectors (context only).** Clip-level F1 on SEP-28k: block 55.9, prolongation 68.5, sound repetition 63.2, word
repetition 60.4, interjection 71.3 [lea2021_sep28k]. wav2vec 2.0 features plus SVM: interjection 0.84, the rest 0.33 to 0.60,
with fold-to-fold swings "up to +-0.46" [bayerl2022_w2v2]. Verbatim Whisper large-v2 fine-tune with word times
[wagner2024_crisperwhisper]. All need training data or a large model, so they fall outside the project's constraints.

### 2.7 What cannot be told apart from audio alone, per the clinical literature

- Tense against plain repetition: "it was impossible to distinguish objectively between "tense word repetition" and "word
  repetition" and between "tense part-word repetition" and "part-word repetition." No method to distinguish between them has
  been clearly demonstrated ... the present study was based on speech-only recordings" [tomisato2024_cluttering].
- Block against pause: "Blocks can be difficult to assess from audio alone; clinicians often rely on physical signs"; Fleiss
  kappa 0.25 for blocks and 0.11 for prolongations among three annotators [lea2021_sep28k]; 0.37 and 0.42 after training
  [bayerl2022_ksof].
- Prolongation against sound repetition: "some sound or part-word repetitions (e.g., "s-s-snake") were conflated with
  prolongations (e.g., "ssssnake") and vice versa" [lea2023_chi].
- Disfluent against deliberate repetition: "Repetitions ... can occur during stuttering events or when an individual wants to
  emphasize a word or phrase" [lea2021_sep28k]; these are separable only by prosody and text [lickley2017].
- Stuttering as such: to the speaker it is "a sensation of anticipation, feeling stuck, or losing control", "beyond the
  observable speech disfluency behaviors" [tichenor2019_abstract, abstract]; covert stuttering sounds fluent [lickley2017];
  even trained listeners' "accuracy of stutter event identification was low" [jani2013_abstract, abstract].
- Cause of a filler or hesitation: anxiety and planning both raise pausing; fillers follow attention to one's speech rather
  than anxiety as such [christenfeld1996_abstract]. No opened source offers an acoustic test that assigns a single hesitation to
  nervousness or to planning.

## 3. What the product covers, partly covers and misses

| Pattern | Today | Why |
|---|---|---|
| Silent hesitation between words (anxiety, planning, reading) | Covered | PAUSE_INTRUSIVE measures unvoiced low-level runs of at least 0.25 s in inter-word gaps against the reference |
| Block between words | Partly | Appears as an intrusive pause; not named as a block, and cannot be (2.7) |
| Block or silence inside a word; syllable-by-syllable reading | Missed | Pauses are searched only in gaps between aligned words |
| Filled pause | Missed, and hidden | A voiced filler in a gap breaks the unvoiced run, so the gap is not a pause; if the aligner absorbs it, the neighbouring word looks slow or unclear |
| Prolongation | Partly | A long word raises the local pace deviation (DRAG) at phrase level; not located to the sound, not separated from emphasis |
| Word / phrase repetition, restart, self-correction | Missed; side effects only | The aligner assumes the transcript; earlier test E4 in `alignment/REPORT.md` showed neighbouring boundaries move by up to 150 ms and confidence stays near 1 |
| Sound / part-word repetition | Missed | Same; may lower the word's posterior compatibility and be reported as a clarity problem |
| Raised pitch, faster or slower rate under nervousness | Covered as pitch and pace, not as disfluency | Existing criteria |

Agreement and disagreement with earlier reports: `rubric_explain/REPORT.md` line 174 says fillers and disfluencies "are not
scored" because the synthetic bad spectrum contains none; this report agrees and adds that published edit recipes exist for four
of the five forms (section 4). `alignment/REPORT.md` E4 tested the star token as a zero log-score column, which is the torchaudio
tutorial's form [torchaudio_star_tutorial]; the published training criteria score the star as the averaged non-blank
probability with a penalty [gao2023_otc_btc], a form E4 did not test. `grounding_model/REPORT.md` line 226 cites YOLO-Stutter
and FluentNet for synthetic-to-real transfer; the numbers are in section 4 below.

## 4. Candidate measures, ranked

Ranking is by (a) evidence, then (b) feasibility under: thresholds only, laptop CPU, pretrained model only, different speaker
from the reference. None has been validated on adults reading a prepared text.

| # | Measure | Detects | Evidence | Feasibility | Judged against | Confounds in a different-speaker comparison |
|---|---|---|---|---|---|---|
| 1 | Inserted material count: edit alignment of the greedy decode against the transcript; insertions that copy or prefix nearby transcript words = repetition / restart, others = extra speech | Word and part-word repetition, restart, some fillers | A (ASR insertions track repetitions, r = .73; miscue recall 0.83) | Uses existing decode; edit alignment is stdlib-level code | Absolute (count per 100 words); reference decode gives the model's own false-insertion floor | Accent or noise raises insertions for reasons other than disfluency; character CTC without a language model inserts spurious letters; precision about 0.5 in children |
| 2 | Orphan voiced gap: voiced frames inside an inter-word gap, duration at least 150 ms, then the stability test of #3 | Filled pause | A for acoustics, B for detectors | All inputs exist | Reference (same gap in the reference has no voiced run) and absolute | Breath noise, laughter; aligner absorbing the filler into a neighbour (then use #5) |
| 3 | Stability run: |log-F0 slope| and MFCC frame-to-frame change both small for a run; F0 below the speaker's median | Filled pause, prolonged vowel or sonorant | B (84.9 % / 91.5 %; 92.86 % at 2.36 % false alarms; other languages or preliminary) | F0 and MFCC frames exist; Goto's constants are tied to his envelope and need re-setting | Speaker's own baseline (F0 relative to the speaker; run length relative to the speaker's rate) | Creaky or hoarse voice; flat-pitched speakers trigger inside words, which collides with the monotone criterion; prolonged fricatives have no F0 |
| 4 | Within-word silence: low-level run inside a word's aligned span, excluding stop closures by a length floor, compared with the same word in the reference | Block, syllable-by-syllable reading | B for the pattern, C for detection | Level frames and word spans exist | Reference (same word) and absolute floor; the literature gives 220 ms (reading) and 250 ms (hesitation) as conventions, not validated cut-offs | Word boundaries shift when the transcript does not match; geminate or long stop closures; noise floor differences between recordings |
| 5 | Segment duration ratio: aligned character or word duration against the reference for the same word, normalised by each speaker's overall rate; flag isolated large ratios | Prolongation; filler or repeat absorbed into a word | A for the pattern (first token of a repeat and pre-interruption rhyme lengthen; stuttered prolongation can pass 1 s), C as a detector | Exists already at phrase level in the pace criterion | Reference plus own rate | Emphasis and phrase-final lengthening are legitimate; CTC character times are spikes, not segment edges |
| 6 | Alignment graph with go-back, part-word and skip arcs | Word, phrase and part-word repetition, omissions, with time stamps and a corrected alignment for the other criteria | A/B (recall 0.47 to 0.60 on synthetic; 0 % missed word repeats on children's reading; 100 % only on TTS data) | Largest change: new Viterbi over a modified graph; published only for phoneme emissions; no training | Absolute | False alarms where the text itself repeats; sensitivity to emission noise; arc weight alpha has to be set (>= 0.9 published) |
| 7 | Inter-word latency against the reference | Any insertion, spoken or silent, located to a word boundary | B (children, r = 0.78 with a fluency test) | Exists (gap durations) | Reference | Does not name the form; overlaps the pause criterion |

Weight in scoring: listeners' fluency judgements depend more on pauses and speed than on repairs (59 %, 54 %, 16 % of variance,
L2 spontaneous speech) [bosker2013_2014]; `docs/PAPERS.md` [6] already records that removing disfluencies raised listener
rankings. The evidence supports reporting disfluencies as located events with a count; it does not supply a weight for a score.

Published norms usable as absolute anchors (each from a different population than the product's): 0.21 % stuttered syllables
for adults who do not stutter reading aloud [ritto2016_speech_tasks]; under 1 % of words disfluent in constrained speech
[shriberg1999_phonetic]; 1.3 to 2.6 filled pauses per 100 words in spontaneous speech [lickley2017]; severity bands 0 to 5 %,
6 to 20 %, over 20 % of words dysfluent [lea2023_chi]; more than one miscue per 10 words as the reading "frustration level"
[mostow2006].

### Imitating each pattern by a controlled edit

| Pattern | Published recipe | Notes for the project's bad spectrum |
|---|---|---|
| Word / phrase repetition | Copy a word 1 to 2 times (LibriStutter), 1 to 3 (DisfluenTIMIT), 2 to 5 (Harvill), 1 to 4 with silence of 70 % of the word after each (VCTK-Stutter); phrase of 2 to 3 words; pause of 100 to 350 ms after each copy; interpolate the joins [kourkounakis2020_fluentnet_libristutter, kouzelis2023_wsfa, harvill2022_frame_level, zhou2024_yolo_stutter] | Exact labels come free. Typical-speaker form per 2.2: one copy, function word, first token stretched, short pause between |
| Sound / part-word repetition | Copy "the first fraction" of a word 1 to 3 times with 100 to 350 ms pauses; copy the first phones before the word; repeat a phone 2 to 5 times; silence 200 to 500 ms after each [same sources, lian2023_udm] | Stuttering form per 2.1: 2 or more rapid copies of the onset consonant or first syllable of a stressed content word |
| Prolongation | Stretch the last 20 % of a word by 5 and restore pitch; stretch a phone 2 to 4 times; 5 to 10 times with WSOLA, excluding "hard consonants"; 10 to 15 times in TTS [same sources] | Project already has WSOLA / PSOLA. Typical form: word-final rhyme; stuttering form: onset continuant, up to about 1 s |
| Block | Silence of 0.5 to 2.0 s after a word (YOLO-Stutter); phones from "a list of commonly blocked sounds" (UDM); LibriStutter omits blocks | A real block is a tense closure with a strong release burst; inserted silence imitates only the gap, and at a word boundary it is identical to PAUSE_INTRUSIVE. Inside a word, before a stop release, is the closer imitation |
| Filled pause | Insert a recorded filler from a pool between two words, pitch-matched to the clip, followed by a short pause [kourkounakis2020_fluentnet_libristutter] | Needs a recorded or synthesised "uh/um"; cannot be made from the clip itself. A different voice or channel in the insert is a detectable artefact |
| Restart with correction | Not generated by any opened recipe ("Revisions were excluded") | A false start can be imitated by copying the first syllable(s) of a word plus a pause, which is the part-word recipe |

What the literature reports about training or testing on such edits:
- Acoustic-space edits sound unnatural: mean opinion score 2.22 for waveform-edited VCTK-Stutter against 4.13 for TTS-generated
  data [zhou2024_yolo_stutter]. LibriStutter's authors state that "the notion of "realism" itself is not a focus".
- Transfer to real speech is partial: a detector trained only on synthetic data scored 82 to 92 % on repetition for UCLASS and
  SEP-28k but 54 to 72 % on blocks and 54 % average accuracy on aphasia speech; "a significant gap between simulated and real
  dysfluency" [zhou2024_yolo_stutter].
- Synthetic prolongation can hurt: pretraining on artificial stutters helped sound and word repetition "but not prolongation
  ... pretraining with artificial prolongations might bias the system against the natural prolongation examples"
  [harvill2022_frame_level].
- Artefacts as shortcuts: Harvill et al. "add in distracting artifacts so that the model must learn to recognize repetitions or
  extensions of sounds instead of the artifact" rather than smoothing joins. This matches the project's existing concern
  (`docs/PAPERS.md` [51]) and its placebo-clip control.
- The alignment methods of M1 were themselves evaluated mostly on such edits (DisfluenTIMIT, simulated sets), so their headline
  numbers are best-case.

## 5. Open questions; searched for and not found

- No norm for disfluency or miscue rate in fluent adults reading a prepared text aloud. The nearest figures are 0.21 % stuttered
  syllables (17 Brazilian adults) and "under 1%" for constrained speech.
- No study that separates nervousness-caused from planning-caused hesitations acoustically on single events; the anxiety
  sources report group or within-speaker rate changes only, and all were read as abstracts.
- No published accuracy for a rule-based block or within-word-silence detector, and no validated duration cut-off that separates
  a block from a stop closure.
- No published use of the modified alignment graph with character-level CTC emissions; Kouzelis and Guo use phoneme models.
  Whether part-word arcs work on characters is untested.
- No published accuracy for the star token as an alignment-time detector of fillers. The MMS paper (arXiv 2305.13516) was
  downloaded and contains no description of the star token; the description is in the torchaudio tutorial only.
- The Mahl "non-ah" category list and the speech-disturbance ratio definition were not seen in any opened source.
- Thresholds of Gabrea & O'Shaughnessy's detector are not printed; Goto's constants are tied to his envelope estimate and to
  Japanese fillers.
- Position of filled pauses and repeats in read (as opposed to spontaneous) speech of adults: not found.
- Transcript-based disfluency tagging (Switchboard-style sequence labelling) was not pursued: it needs a verbatim transcript,
  which is the missing piece here.
- One opened paper was not used: Romana et al. 2023 (arXiv 2311.00867, trained multimodal detector; abstract and headings read).

## 6. References

Read status: F = full text, A = abstract only, S = secondary, W = full page through the fetch tool (quotes model-extracted, not
re-checked against a local copy). Source files are in `sources/`.

| Source | Venue, URL | Status | File |
|---|---|---|---|
| Alharbi, Hasan, Simons, Brumfitt, Green 2018, A lightly supervised approach to detect stuttering in children's speech | Interspeech; isca-archive.org/interspeech_2018/alharbi18_interspeech.pdf | F | alharbi2018_lightly_supervised |
| Alharbi, Simons, Brumfitt, Green 2017, Automatic recognition of children's read speech for stuttering application | WOCCI; isca-archive.org/wocci_2017/alharbi17_wocci.pdf | F (parts) | alharbi2017_wocci |
| Bayerl et al. 2022, KSoF | LREC; arxiv.org/abs/2203.05383 | F (parts) | bayerl2022_ksof |
| Bayerl, Wagner, Nöth, Riedhammer 2022, Detecting dysfluencies in stuttering therapy using wav2vec 2.0 | Interspeech; arxiv.org/abs/2204.03417 | F (parts) | bayerl2022_w2v2 |
| Beck, Jia, Mostow 2004, Automatically assessing oral reading fluency in a computer tutor that listens | TICL 2; cs.cmu.edu/~listen2/pdfs/TICL2004-latency-61-81pp (Beck).pdf | F (parts) | beck2004 |
| Bortfeld, Leon, Bloom, Schober, Brennan 2001, Disfluency rates in conversation | Language and Speech 44; doi 10.1177/00238309010440020101 | F (parts) | bortfeld2001 |
| Bosker, Pinget, Quené, Sanders, De Jong 2013, What makes speech sound fluent? | Language Testing 30; doi 10.1177/0265532212455394 | A; numbers from Bosker 2014 research note (F) | bosker2013_2014 |
| Buchanan, Laures-Gore, Duff 2014, Acute stress reduces speech fluency | Biol Psychol 97; PMID 24555989 | A | buchanan2014_abstract |
| Christenfeld & Creager 1996, Anxiety, alcohol, aphasia, and ums | JPSP 70; PMID 8851740 | A | christenfeld1996_abstract |
| Clark & Fox Tree 2002, Using uh and um in spontaneous speaking | Cognition 84; web.stanford.edu/~clark | F (parts) | clark_foxtree2002 |
| Cucchiarini, Strik, Boves 2002, Quantitative assessment of second language learners' fluency | JASA 111; PMID 12083220 | A | cucchiarini2002_abstract |
| de Jong, Pacilly, Heeren 2021, PRAAT scripts to measure speed fluency and breakdown fluency | Assessment in Education 28; eric.ed.gov/?id=EJ1322458 | A | dejong2021_abstract |
| Gabrea & O'Shaughnessy 2000, Detection of filled pauses in spontaneous conversational speech | ICSLP; doi 10.21437/ICSLP.2000-626 | F | gabrea2000_filled_pause |
| Gao, Xu, Raj, Garcia, Povey, Khudanpur 2023, OTC; Gao et al. 2023, BTC | ASRU, Interspeech; arxiv.org/abs/2309.15796, 2306.01031 | F (parts) | gao2023_otc_btc |
| Gao, Tejedor-Garcia, Strik, Cucchiarini 2024, Reading miscue detection in primary school through ASR | Interspeech; arxiv.org/abs/2406.07060 | F (parts) | gao2024_miscue |
| Goto, Itou, Hayamizu 1999, A real-time filled pause detection system | Eurospeech; doi 10.21437/Eurospeech.1999-60 | F | goto1999_filled_pause |
| Guo, Lian, Zhou et al. 2025, Dysfluent WFST | Interspeech; arxiv.org/abs/2505.16351 | F | guo2025_dysfluent_wfst |
| Han, Zhou, Lu, Pill 2026, Cluttering in children and adolescents | Children 13; PMC12839606 | F (parts) | han2026_cluttering_review |
| Harvill, Hasegawa-Johnson, Yoo 2022, Frame-level stutter detection | Interspeech; isca-archive.org/interspeech_2022/harvill22_interspeech.pdf | F | harvill2022_frame_level |
| Hofmann, Gerlach, Wender, Roth 1997, Speech disturbances and gaze behavior during public speaking | J Anxiety Disord 11; PMID 9455720 | A | hofmann1997_abstract |
| Howell, Au-Yeung, Sackin 1999, Exchange of stuttering from function words to content words with age | JSLHR 42; PMID 10229451 | A | howell1999_abstract |
| Howell, Sackin, Glenn 1997, ANN recognition of repetitions and prolongations | JSLHR 40; PMID 9328879 | A | howell1997_abstract |
| Jani, Huckvale, Howell 2013, Procedures used for assessment of stuttering frequency and duration | Clin Linguist Phon 27; PMID 23848369 | A | jani2013_abstract |
| Kasl & Mahl 1965, Disturbances and hesitations in spontaneous speech and anxiety | JPSP 1; doi 10.1037/h0021918 | S (abstract reproduced at filledpause.org; also via Bortfeld 2001) | kasl_mahl1965_secondary |
| Kourkounakis, Hajavi, Etemad 2021, FluentNet / LibriStutter | IEEE/ACM TASLP 29; arxiv.org/abs/2009.11394 | F (parts) | kourkounakis2020_fluentnet_libristutter |
| Kouzelis, Paraskevopoulos, Katsamanis, Katsouros 2023, Weakly-supervised forced alignment of disfluent speech | Interspeech; arxiv.org/abs/2306.00996 | F | kouzelis2023_wsfa |
| Laukka et al. 2008, In a nervous voice | J Nonverbal Behav 32; doi 10.1007/s10919-008-0055-9 | A | laukka2008_abstract |
| Lea, Mitra, Joshi, Kajarekar, Bigham 2021, SEP-28k | ICASSP; arxiv.org/abs/2102.12394 | F | lea2021_sep28k |
| Lea, Huang, Narain et al. 2023, Enabling people who stutter to better use speech recognition | CHI; arxiv.org/abs/2302.09044 | F (parts) | lea2023_chi |
| Lian, Feng, Farooqi et al. 2023, Unconstrained dysfluency modeling | ASRU; arxiv.org/abs/2312.12810 | F (parts) | lian2023_udm |
| Lickley 2017, Disfluency in typical and stuttered speech | Studi AISV 3; doi 10.17469/O2103AISV000019 | F | lickley2017 |
| Max, Kadri, Mitsuya, Balasubramanian 2019, Similar within-utterance loci of dysfluency | Brain and Language 189; PMC11513192 | W | max2019_loci |
| Mitra, Huang, Lea et al. 2021, Analysis and tuning of a voice assistant system for dysfluent speech | Interspeech; arxiv.org/abs/2106.11759 | F (parts) | mitra2021_va_dysfluent |
| Molenaar, Tejedor-Garcia, Cucchiarini, Strik 2023, Automatic assessment of oral reading accuracy | Interspeech; arxiv.org/abs/2306.03444 | F (parts) | molenaar2023_oral_reading |
| Mostow 2006, Is ASR accurate enough for automated reading tutors? | Interspeech; isca-archive.org/interspeech_2006/mostow06_interspeech.pdf | F (parts) | mostow2006 |
| Nguyen, Del Tufo, Cutting 2020, Readers recruit executive functions to self-correct miscues | Sci Stud Reading 24; PMC7954224 | W | nguyen2020_miscues |
| Pratap, Hannun, Synnaeve, Collobert 2022, Star Temporal Classification | NeurIPS; arxiv.org/abs/2201.12208 | F (parts) | pratap2022_stc |
| Proença, Celorico, Candeias, Lopes, Perdigão 2015, Children's reading aloud performance | Interspeech; isca-archive.org/interspeech_2015/proenca15_interspeech.pdf | F | proenca2015 |
| Ritto, Costa, Juste, de Andrade 2016, Comparison of different speech tasks among adults who stutter and who do not | Clinics 71; PMC4785848 | F | ritto2016_speech_tasks |
| Sandoval, Farías, Gajardo, Quezada Cáceres, Lagos, Rojas 2025, Stress situations and speech fluency (VR pilot) | Behav Sci 15; PMC12729271 | F (parts) | sandoval2025_vr_stress |
| Sheikh, Sahidullah, Hirsch, Ouni 2022, Machine learning for stuttering identification: review | Neurocomputing; arxiv.org/abs/2107.04057 | F (parts); used as secondary pointer | sheikh2022_review |
| Shriberg 1999, Phonetic consequences of speech disfluency | ICPhS; sri.com/wp-content/uploads/2021/12/phonetic_consequences_of_speech_disfluency.pdf | F | shriberg1999_phonetic |
| Shriberg 2001, To 'errrr' is human | JIPA 31; doi 10.1017/S0025100301001128 | A | shriberg2001_abstract |
| Smith, Yee, Chen, Findlater 2025, Prompting Whisper for verbatim transcription and miscue detection | Interspeech; arxiv.org/abs/2505.23627 | F (parts) | smith2025_whisper_miscue |
| Tam, Mostow, Beck, Banerjee 2003, Training a confidence measure for a reading tutor that listens | Eurospeech; ri.cmu.edu/pub_files/pub4/tam_y_c_2003_1 | F (parts) | tam2003 |
| Tichenor & Yaruss 2019, Stuttering as defined by adults who stutter | JSLHR 62; PMID 31830837 | A | tichenor2019_abstract |
| Tomisato et al. 2024, Speech characteristics that differentiate stuttering and cluttering | Front Psychol 15; PMC11602310 | F | tomisato2024_cluttering |
| torchaudio CTC forced alignment API tutorial (star token) | docs.pytorch.org/audio | W | torchaudio_star_tutorial |
| Wagner, Thallinger, Zusag 2024, CrisperWhisper | Interspeech; arxiv.org/abs/2408.16589 | F (parts) | wagner2024_crisperwhisper |
| Zebrowski 1994, Duration of sound prolongation and sound/syllable repetition in children who stutter | JSHR 37; PMID 8028307 | A | zebrowski1994_abstract |
| Zhou, Kashyap, Li et al. 2024, YOLO-Stutter | Interspeech; arxiv.org/abs/2408.15297 | F | zhou2024_yolo_stutter |
| Zhu, Caceres, Salamon 2022, Filler word detection and classification (PodcastFillers) | Interspeech; arxiv.org/abs/2203.15135 | F | zhu2022_podcastfillers |

### Could not open (not cited as sources)

| Paper | What was wanted | What happened |
|---|---|---|
| Levelt 1983, Monitoring and self-repair in speech, Cognition 14 | Main Interruption Rule wording; share of within-word interruptions; editing terms by repair type | pure.mpg.de returned a bot challenge and HTTP 403; used only through Shriberg 1999 and Lickley 2017 |
| Goberman, Hughes, Haydock 2011, Acoustic characteristics of public speaking: anxiety and practice effects, Speech Communication 53 | Pause and filled-pause measures against speaking anxiety in a real public-speaking task | Publisher page returned a redirect stub; no abstract available from Crossref or Semantic Scholar |
| de Jong, Pacilly, Heeren 2021 (full text) | The filled-pause rule and thresholds of the Praat script, accuracy against manual counts | HTTP 403 at the publisher; bot challenge at the Leiden repository; abstract only |
| Mahl 1956; Kasl & Mahl 1965 (full text) | The eight speech-disturbance categories and the non-ah ratio | ResearchGate blocked; PubMed has no abstract |
| Shriberg 1994 thesis; Shriberg 2001 (full text) | Disfluency type rates by corpus, position effects | Thesis URL dead; journal page abstract only |
| Shriberg & Lickley 1993, Intonation of clause-internal filled pauses | The filled-pause F0 model | Not attempted beyond the secondary report in Clark & Fox Tree |
| Audhkhasi et al. 2009, Formant-based technique for automatic filled-pause detection | Formant-stability rule and accuracy for English | Download returned an error page |
| Cucchiarini et al. 2002 (full text); Bosker et al. 2013 (full text) | Disfluency measures in read L2 speech; regression table | Publisher or repository blocked; abstracts only |
| Howell et al. 1999, 1997 (PMC full texts) | Function/content word figures; acoustic features of the classifier | Europe PMC returned no full-text XML; abstracts only |
| Ravikumar et al.; Arjun et al. 2020; "Repetition detection in stuttered speech" (Springer 2016) | DTW or correlation rules for repetition, thresholds | Not opened; known only through Sheikh 2022 and Harvill 2022 |

### Unsourced, to verify (general knowledge, not found in an opened source)

- Mahl's non-ah categories are usually listed as sentence change, repetition, stutter, omission, sentence incompletion, tongue
  slip and intruding incoherent sound, and the speech-disturbance ratio as disturbances divided by words spoken.
- The usual clinical criterion for stuttering in children is three or more stuttering-like disfluencies per 100 syllables
  (Yairi and Ambrose); the SSI-4 scores the mean of the three longest events on a duration scale.
- The adaptation effect: stuttering frequency falls over repeated oral readings of the same passage. Relevant because the
  product's users rehearse a known text; no opened source stated it.
- Phrase-final lengthening and stop-closure durations (tens of milliseconds up to roughly 100 ms) as the fluent baseline that a
  within-word silence floor must exceed.