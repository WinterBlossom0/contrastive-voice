# Data availability for the candidate measures (research only, 2026-10-02)

Nothing was downloaded beyond metadata, one 2 MB index file and one small speaker CSV; no code or project files were changed. Evidence notes (URL fetched and the text read) were kept in working notes that are not part of the repository.

**Short answer:** for every measure in SYNTHESIS sections 3 and 4, including the whole "no" tier, data or a pretrained model that stands in for it can be had within days. The one exception is real nervous or anxious read speech with the same speaker calm: it exists only behind academic-affiliation requests, and those licences forbid redistribution.

VERIFIED means I read the licence text or the data listing with `curl` or an API in this session. UNVERIFIED means the source is a search-result summary or the page could not be opened. "Internal" is use for calibration or validation without redistribution; "redistribute" is putting derived clips in the public repository. NC is a non-commercial licence; I did not judge whether a hackathon submission counts as non-commercial.

## 1. Table: measure or pattern against data

| Candidate measure / pattern | Data needed (build / calibrate / validate) | Best available source(s) | Licence and access | Obtainable in days? | Status |
|---|---|---|---|---|---|
| Within-phrase pause count and duration; tempo decomposition; mean length of run; per-word latency and production; tempo irregularity (tiers 1-2) | Build: none. Calibrate: many fluent readings of one text. Validate: read speech with human fluency scores, plus real fast or hesitant readings | LibriVox multi-reader poems and Gettysburg (15 readers); speechocean762 (5,000 read sentences, sentence fluency and prosodic scores 0-10 from five experts); EARS Rainbow passage in regular / fast / slow (107 speakers); CHAINS solo against fast (36 speakers) | LibriVox public domain (redistribute yes). speechocean762 CC BY 4.0, 520 MB direct (redistribute yes, with attribution). EARS CC BY-NC 4.0, 0.59 GB per speaker direct (internal yes; redistribute only under NC). CHAINS: Creative Commons, "free use for both commercial and non-commercial research", share-alike; site down, LDC lists it at $50 | yes (CHAINS: with a request or LDC) | VERIFIED |
| Several-reference comparison (pitch match, prominence vector, reference distance, clarity distance) | 10 to 20 fluent readings of the same text | See section 2 | See section 2 | yes | VERIFIED |
| Inserted material by greedy decode; alignment graph with repeat / part-word / skip arcs | Build: none (decoder). Calibrate and validate: read or prepared speech with labelled repetitions, restarts, fillers | SEP-28k (28,000 3-s podcast clips, clip-level labels, 3 annotators); UCLASS (people who stutter); LibriStutter (synthetic, 5.6 GB); PodcastFillers "repeated words" events; DisfluencySpeech (1 speaker, 10 h acted Switchboard, verbatim transcripts); self-recorded planted repeats | SEP-28k labels CC BY-NC 4.0, audio "copyright remains with the podcast owners" (internal yes; redistribute audio no). UCLASS "freely available to anyone for research and teaching purposes" with acknowledgment (redistribution not stated). LibriStutter CC BY-NC 4.0. DisfluencySpeech Apache-2.0 on Hugging Face, 1.5 GB | yes | VERIFIED |
| Trained disfluency / stutter-type detector ("no" tier) | Train: SEP-28k class data. Or use a pretrained checkpoint | Vox-Profile speech-flow, vocametrix wav2vec2, Romana et al., YOLO-Stutter (section 4) | OpenRAIL / Apache-2.0 / none stated / MIT | yes | VERIFIED |
| Filled-pause detection (orphan voiced gap plus pitch and spectral stability; filler insertion recipe) | Calibrate and validate: time-stamped real "uh / um"; a pool of real fillers for the edit recipe | PodcastFillers: 199 episodes, 145 h, about 35,000 fillers and 50,000 other events with timestamps | Open on Zenodo, 25.3 GB. Audio "CC-licensed"; annotations and the 1-s clips under an Adobe research licence that "prohibits commercial use". Internal yes; redistributing clips cut by the annotations falls under that licence | yes (large) | VERIFIED |
| Verbatim transcription that keeps fillers | Pretrained model | CrisperWhisper; CrisperWhisper 2.0 small; Whisper | CC BY-NC 4.0; nyra "Non-Commercial Research License" (no hosted service or API); Apache-2.0 | yes | VERIFIED |
| Block / silence inside a word | Validate: labelled blocks | SEP-28k "Block" label (3-s clip level); UCLASS; KSoF; FluencyBank | KSoF restricted, "upon request". FluencyBank "restricted to members", faculty only. Others as above | SEP-28k and UCLASS yes; KSoF with a request; FluencyBank no without a faculty member | VERIFIED |
| Reading miscues (back-step, false start then correction) | Read-aloud audio with miscue labels | Oral Reading in Young English Readers (63 children, 9 h, 10 error categories); CMU Kids; speechocean762 completeness score (sentence level only) | The 2026 corpus "will be deposited through the Linguistic Data Consortium". CMU Kids needs an LDC agreement | no for labelled miscues; yes for speechocean762 | VERIFIED |
| Word posterior / goodness of pronunciation; phoneme-level CTC | Build: phoneme CTC checkpoint. Validate: phone and word accuracy scores; low-intelligibility speech | speechocean762 phone 0-2 and word 0-10 scores; TORGO dysarthric speech (18 GB); MDVR-KCL (Parkinson's patients and controls reading "The North Wind and the Sun" by phone) | speechocean762 CC BY 4.0. TORGO "free for academic (non-profit) purposes" (internal only). MDVR-KCL CC BY 4.0, 606 MB (redistribute yes) | yes | VERIFIED |
| Reference distance on aligned words; clarity / mumbling; vowel space ("no" tier) | Build: phone alignment and formants. Validate: same speakers clear against casual, plus rated intelligibility | Expresso "enunciated" against "default" (4 speakers); EARS regular / fast / whisper; MDVR-KCL; TORGO; Montreal Forced Aligner model. LUCID (40 speakers, clear and casual, non-commercial research) | Expresso CC BY-NC 4.0 (mirror 5.8 GB). Aligner model CC BY 4.0. LUCID: page returned 404 | yes, except LUCID | VERIFIED; LUCID UNVERIFIED |
| Spectral balance and pitch against own median; absolute effort classification ("no" tier) | Same speakers at several effort levels, fixed microphone distance | AVID: 50 speakers, soft / normal / loud / very loud, calibration tone, sentence labels (the corpus behind Kodali 2023); EARS loud / whisper / regular; Lombard GRID (54 talkers, 50 Lombard and 50 plain each) | AVID CC BY 4.0, 12.4 GB. Lombard GRID CC BY 4.0, audio 653 MB. Both redistributable with attribution | yes | VERIFIED |
| Trailing off (level slope, last-word drop); sentence-final pitch; declination | Calibrate: many fluent readers of one text for the normal spread. Validate: real trailing-off | Many-reader sets (section 2); MDVR-KCL as real reduced-loudness reading (pathological); self-recorded | as above | yes for the spread; real labelled trailing-off in healthy readers was not found | VERIFIED for sources |
| Whole-clip pitch span; monotone patterns; repeated contour | Calibrate: span distribution over many readers of one text. Validate: real monotone readings | LibriVox poems; EARS; ParaSpeechCaps tags ("monotone", "hesitant", "stammering", "slurred", "vocal-fry", "hushed") on VoxCeleb / Expresso / EARS / Emilia audio; MDVR-KCL | ParaSpeechCaps tags CC BY-NC-SA 4.0, 368 MB, audio fetched from the source corpora | yes | VERIFIED |
| Prominence (signal-based, trained detector, function-word prior, accent ratio) | Word-level prominence labels on read speech | Crowdsourced LibriTTS prominence (3,626 utterances, 6.42 h, 69,809 words, 18 speakers); Helsinki Prosody Corpus (automatic labels on LibriTTS); Expresso emphasis substyle (marked words); Boston University Radio News | First two CC BY 4.0 (LibriTTS audio also CC BY 4.0). Expresso CC BY-NC 4.0. Boston corpus: LDC agreement, page shows $1,200 | yes, except Boston (paid) | VERIFIED |
| Breath-pause location; breath detection ("no" tier) | Frame-level breath labels, or a pretrained detector | Respiro-en (hand-annotated LibriTTS-R validation and test sets in the repository); PodcastFillers breath events | MIT; as above | yes | VERIFIED |
| Creak detection ("no" tier); creak at sentence ends | Creak-annotated speech, or a pretrained detector | DeepFry (American English, annotated by phoneticians); creapy; Vox-Profile "vocal-fry" label | MIT; GPL-3.0; OpenRAIL | yes | VERIFIED; creapy training data UNVERIFIED |
| Interval rhythm metrics ("no" tier) | Build: vowel / consonant segmentation. Calibrate: native and non-native readers of one passage | Speech Accent Archive (2,140 readers, 579 native English, one 69-word paragraph); VCTK; aligner model | Archive CC BY-NC-SA 4.0 (Kaggle mirror 907 MB); VCTK CC BY 4.0 | yes | VERIFIED |
| Nervousness / anxiety cues: raised pitch level, share of silence, jitter, shimmer, tremor ("no" tier) | Same speaker calm and anxious, ideally reading | VerBIO (55 participants, 344 public-speaking sessions, state-anxiety ratings); StressID (65 participants, includes public speaking); BESST (Czech); SUSAS (8 kHz); acted fear against neutral in CREMA-D and RAVDESS | VerBIO: "academic research only upon request", academic email, "can not redistribute". StressID: "only a person with a permanent position in academics can sign". BESST: signed licence. SUSAS: LDC agreement. CREMA-D Open Database License; RAVDESS CC BY-NC-SA 4.0 | real: with a request and an academic signatory, internal only; acted: yes | VERIFIED terms; BESST terms UNVERIFIED |
| Own-baseline comparison ("no" tier) | A calm recording of the same speaker | Product asks for it (section 3); open corpora with one speaker in several conditions: EARS, AVID, CHAINS, Expresso | as above | yes | VERIFIED |
| Pause share across speakers; absolute loudness | Many readers of one text; calibrated level | Section 2; AVID has a calibration tone, a user upload does not | as above | pause share yes; absolute loudness of an upload stays unmeasurable | VERIFIED |
| Section 4 edit recipes (natural rushing, hesitation, word-by-word, low effort, misplaced emphasis, rising ending) | Real counterparts to check each edit against | EARS and CHAINS fast readings; AVID soft against normal; Expresso emphasis and enunciated; low-fluency speechocean762 items; PodcastFillers for the filler recipe | as above | yes | VERIFIED |

## 2. Many readers of one text

| Source | Readers per text | Text | Licence and access | Status |
|---|---|---|---|---|
| LibriVox "Gettysburg Address 150th Anniversary" | 15 (the project uses 9) | full address, 1:55 to 3:34 | Public Domain Mark 1.0; archive.org direct; 127 MB | VERIFIED |
| LibriVox solo Gettysburg items | 4 more single readers, separate items | full address, 100 to 161 s | public-domain dedication | VERIFIED |
| LibriVox weekly and fortnightly poetry | 1,400 items; in a sample of 40: 5 to 24 readers, median 14, 34 of 40 with ten or more; "Jabberwocky" has 34 | one poem each; mean reading 35 to 281 s, median 75 s | Of the 1,400: 763 Public Domain Mark, 235 older public-domain dedication, 26 CC0, 176 with no licence field | VERIFIED |
| Speech Accent Archive | 2,140, of which 579 native English | one 69-word paragraph ("Please call Stella") | CC BY-NC-SA 4.0; Kaggle mirror 907 MB | VERIFIED |
| EARS | 107, each in 7 styles | Rainbow passage in 8 chunks, plus sentences | CC BY-NC 4.0; GitHub releases, 69 GB total, 0.59 GB per speaker | VERIFIED |
| VCTK 0.92 | 110 | Rainbow passage and the Accent Archive paragraph, "the same for all speakers" | CC BY 4.0; 10.9 GB, one zip | VERIFIED |
| CHAINS | 36, in solo, synchronous, whisper and fast conditions | Cinderella, Rainbow first paragraph, North Wind and the Sun, Members of the Body, 33 sentences | Creative Commons, commercial use allowed, share-alike; site unreachable today, archived page describes free FTP; LDC $50 | VERIFIED licence; access not confirmed |
| DAPS | 20, about 14 min each | 5 scripts; the segmented release holds script 1 for all 20 with word alignments | CC BY-NC 4.0; 16 GB full, 229 MB segmented | VERIFIED |
| OpenSLR 83 (UK and Ireland dialects) | 51 lines read 20 or more times; Rainbow sentences 120 times each | single sentences | CC BY-SA 4.0; zips of 100 MB to 1.7 GB per dialect | VERIFIED |
| CMU ARCTIC plus L2-ARCTIC | native voice talents plus 24 non-native speakers | about 1,132 sentences from out-of-copyright texts | ARCTIC "free for use for any purpose"; L2-ARCTIC CC BY-NC 4.0 behind a name / email form | VERIFIED |
| MDVR-KCL | Parkinson's patients and healthy controls | North Wind and the Sun, read over a phone | CC BY 4.0; 606 MB | VERIFIED (speaker count not read) |
| PTDB-TUG | 20 | TIMIT sentences, with laryngograph pitch | Open Database License | VERIFIED |
| TIMIT | 630 (from memory) | two shared sentences | LDC agreement; price not readable | UNVERIFIED count and price |
| Common Voice | varies by sentence | single sentences | described as "a CC0 public dataset"; Mozilla Data Collective account; per-sentence counts not checked | partly VERIFIED |
| ALLSSTAR, IViE | not confirmed | North Wind and the Sun; Cinderella | pages are JavaScript-only or carry no licence text | UNVERIFIED |

No collection of one public-domain speech read by many people was found beyond the Gettysburg items. The public-domain many-reader material is otherwise verse.

## 3. Real flaw recordings and self-recorded data

**Real recordings available now**

- **Rushed:** EARS "fast" and CHAINS "fast" readings of the Rainbow passage by the same speakers who also read it normally. These are instructed, not nervous.
- **Quiet / low effort:** AVID soft against normal; EARS whisper and regular. Lombard GRID covers the raised-effort side.
- **Monotone, mumbling, trailing off:** MDVR-KCL (Parkinson's readers and controls on one passage; the description does not label these traits per recording). ParaSpeechCaps points to clips tagged monotone, slurred, hesitant or stammering in other corpora.
- **Hesitant, word-by-word reading:** speechocean762 low-fluency items (human scores, redistributable); the 1,561 non-native Speech Accent Archive readers (unlabelled).
- **Fillers and repetitions:** PodcastFillers (time-stamped, spontaneous); SEP-28k and UCLASS (people who stutter); DisfluencySpeech (acted).
- **Public-domain source in the project's existing licence class:** unscripted US government recordings such as press conferences. The Supreme Court argument-audio page was opened but carries no copyright statement (UNVERIFIED as a licence).
- **Not found:** real nervous readings, and real fillers inside read text by fluent adults, in any open corpus.

**Self-recorded protocol, as the published corpora do it**

- EARS, CHAINS, AVID and the clear-speech studies all use the same design: each speaker reads one fixed text first in a habitual condition, then again under an instruction.
- Published instructions: fast, slow, loud, soft, whisper, high pitch, low pitch (EARS); soft / normal / loud / very loud at a fixed microphone distance (AVID); clear, "as if to a hearing-impaired listener", "overenunciate" (Lam, Tjaden & Wilding 2012).
- A team version of that design would be the same public-domain passage read habitually, then fast, flat, mumbled, quiet, trailing off, and with planted repeats and fillers, on the same device and position. The habitual take doubles as the speaker's own baseline, and the labels come from the instruction.
- Rights are the team's own, so redistribution is unrestricted; with one to four team members the speaker count is one to four unless others consent.

**Acted against natural, from sources opened**

- Jürgens, Hammerschmidt & Fischer 2011 (full text): play-acted and authentic expressions "differ in their voice quality" and acted tokens show "a more variable F0-contour". Acted flaws are therefore likely to be more exaggerated than natural ones.
- Lam, Tjaden & Wilding 2012 (abstract): "Different instructions for eliciting clear speech yielded acoustic adjustments of varying magnitude". The wording of the instruction changes the result.
- The project's own disfluency report already notes that detectors trained on simulated stutters transfer only partly to real speech.
- A search summary said listeners cannot tell practised pseudo-stuttering from real stuttering; I did not open that paper (UNVERIFIED).

**Own baseline**

- A published system does ask for one. In "Novel Deep Learning-Based Vocal Biomarkers for Stress Detection in Koreans" (full text): "Upon initial use, the application prompts the user to record their voice in a stress-free and relaxed state to establish a baseline reference ... The recording lasts for at least 1 min ... these values are set as user references", and a test against those references "enhances the detection accuracy".
- That study also had participants read a 141-word script relaxed and again after a stress task; its data was not found as an open release.
- Open corpora with the same speakers calm and stressed while reading or presenting: none without a request (VerBIO, StressID, BESST, SUSAS above).

## 4. Pretrained models

Measured here: wav2vec 2.0 base (94 M parameters, the project's current model) takes 0.91 s for a 30 s input on this laptop's CPU with 8 threads. No other model was run; "CPU est." is scaled from that by size.

| Need | Checkpoint | Licence | Size | Trained on | CPU est. for 20-40 s | Status |
|---|---|---|---|---|---|---|
| Prominence | `emphases` (pip; Morrison et al. 2024) | MIT | 3 MB | crowdsourced LibriTTS annotations | under 1 s | VERIFIED |
| Prominence, no training | wavelet_prosody_toolkit | MIT | no weights | – | under 1 s | VERIFIED |
| Breath | Respiro-en | MIT | 35 MB | LibriTTS-R | about 1 s | VERIFIED |
| Creak | DeepFry | MIT | weights in repo | American English, phonetician labels | seconds | VERIFIED |
| Creak | creapy (pip) | GPL-3.0 | small | Austrian German conversation (from search summary) | seconds | licence VERIFIED |
| Disfluency type, 3 s windows | tiantiaf/wavlm-large-speech-flow | OpenRAIL | 1.27 GB | SEP-28k and FluencyBank | about 5-10 s | VERIFIED |
| Stutter class per clip | vocametrix/wav2vec2-xlsr-53-stuttering-classification | Apache-2.0 | 1.26 GB | SEP-28k-Extended | about 3-5 s | VERIFIED |
| Frame-level disfluency (20 ms) | amritkromana/disfluency_detection_from_audio | no licence file | Google Drive | Switchboard | not estimated | VERIFIED |
| Disfluency regions | YOLO-Stutter | MIT | Google Drive, needs VITS | simulated VCTK-Stutter | not estimated | VERIFIED |
| Voice-quality tags (vocal-fry, monotone, slurred, hesitant, stammering, hushed) | tiantiaf/wavlm-large-voice-quality | OpenRAIL | 1.27 GB | ParaSpeechCaps | about 5 s; needs 3 s or more | VERIFIED |
| Verbatim transcript with fillers and word times | nyralabs/CrisperWhisper | CC BY-NC 4.0 | 3.2 GB | Whisper large-v3 base | tens of seconds to minutes | VERIFIED |
| Same | nyralabs/CrisperWhisper2.0_small | weights: non-commercial research licence, no hosted service; code MIT | 483 MB | not stated for the standard models | about 5-15 s | VERIFIED |
| Plain transcript | openai/whisper-base.en, small.en | Apache-2.0 | 290 / 966 MB | 680k h weakly labelled | seconds | VERIFIED |
| Phoneme CTC for goodness of pronunciation | facebook/wav2vec2-lv-60-espeak-cv-ft; wav2vec2-xlsr-53-espeak-cv-ft; vitouphy/wav2vec2-xls-r-300m-timit-phoneme | Apache-2.0 | 1.26 GB each | Common Voice; TIMIT | about 3-5 s | VERIFIED |
| Phoneme CTC, base size | mostafaashahin/wav2vec2-base-timit-phoneme-arpa-39; charsiu/en_w2v2_fc_10ms | no licence tag on Hugging Face (charsiu code is MIT) | 377 MB | TIMIT; not read | about 1 s | VERIFIED sizes |
| Phone alignment for vowel space and rhythm | Montreal Forced Aligner, English US ARPA v3 | code MIT, model CC BY 4.0 | small | LibriSpeech 982 h | seconds | VERIFIED |
| Prosody / fluency score | tiantiaf/childvox-speechocean762-prosody-whisper-base; JohnJumon/fluency_accuracy | OpenRAIL; Apache-2.0 | 5 MB heads on whisper-base; 82 MB | speechocean762; "unknown dataset" | seconds | VERIFIED |
| Arousal as a nervousness stand-in | audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim | CC BY-NC-SA 4.0, "research purpose only" | 661 MB | MSP-Podcast | about 3 s | VERIFIED |
| Reference-free quality estimates | torchaudio SQUIM_OBJECTIVE (already a dependency) | weights CC BY 4.0 | small | DNS 2020 | about 1 s | VERIFIED |

A pretrained vocal-effort classifier was not found: Hugging Face searches for "vocal-effort" and "lombard" returned nothing relevant. AVID would be the training data for one.

## 5. What remains unobtainable, and what was tried

1. **Real nervous or anxious readings with a calm baseline of the same speaker, open or redistributable.**
   - VerBIO needs an academic email and forbids redistribution.
   - StressID needs a signatory with a permanent academic post.
   - BESST is Czech and needs a signed licence; SUSAS is LDC-licensed and 8 kHz.
   - A Zenodo search for public-speaking anxiety audio returned only questionnaire studies.
   - The Korean stress study's read-script recordings were not found as an open release.
   - What can be had in days is acted fear against neutral (CREMA-D, RAVDESS) and self-recorded material.
2. **FluencyBank and KSoF.** FluencyBank is restricted to consortium members and faculty; KSoF is restricted on Zenodo, on request. Both are obtainable only through an academic contact.
3. **Read-aloud speech by fluent adults with time-stamped miscue or disfluency labels.** The 2026 children's oral-reading corpus is to go through LDC, and CMU Kids needs an LDC agreement. No adult equivalent was found; speechocean762 gives only sentence-level scores.
4. **Human pitch-accent labels on professional read news.** The Boston University Radio News Corpus is LDC-only, with $1,200 shown on its page. The open substitute is crowd-annotated LibriTTS prominence.
5. **A corpus of healthy speakers reading in clear and in casual or mumbled style, with ratings.** The LUCID page returned 404. The Clarity Speech Corpus (CC BY-SA 4.0 with a no-broadcast exception) is plain sentences, not style pairs. The open stand-ins are Expresso "enunciated" against "default" (4 speakers) and pathological speech.
6. **English public-speaking recordings with human delivery ratings.** 3MT_French is restricted and in French; Speak & Improve 2025 is non-commercial second-language spontaneous speech and its site would not open; TED was already excluded by the team. None found open.
7. **Norms for fluent adults reading prepared text** (disfluency rate, level declination). No labelled corpus exists; they can only be estimated from the unlabelled many-reader sets.
8. **Goberman, Hughes & Haydock 2011.** Searched again; only the paywalled DOI (10.1016/j.specom.2011.02.005) was found.
9. **Absolute loudness of an uploaded clip.** No dataset fixes this, because the upload has no calibration tone.

**Pages that could not be read:** chains.ucd.ie (no response), kaggle.com and PubMed Central HTML (CAPTCHA; the Kaggle CLI and the Europe PMC API were used instead), zenodo.org HTML (403; API used), oyez.org, the Northwestern SpeechBox site and speakandimprove.com (JavaScript only), and the LUCID page (404).

**Not checked:** LDC prices other than the two shown; Common Voice per-sentence reader counts; licences of the Kaggle SEP-28k mirrors (2.3 GB, audio included); UASpeech and the Speech Accessibility Project. The Hugging Face mirror of speechocean762 is tagged Apache-2.0, which differs from the CC BY 4.0 on the official OpenSLR page.
