# Evaluation rubric, scoring methodology and causal explanations

Research report for Track C (Contrastive Speech Analytics & Temporal Flaw Grounding). Date: 2026-10-01.
Researcher topic: rubric, scoring, explanations. This run resumed an interrupted run; no compute was needed and none was run on Kaggle (0 kernel pushes).

Evidence tags used throughout:

- **VR** = VERIFIED_BY_RUNNING (executed; output file cited).
- **VS** = VERIFIED_BY_SOURCE (page / paper / API response fetched by this run or the previous run; URL or local file cited).
- **UV** = UNVERIFIED (memory, or a search-engine summary of a page that could not be fetched). Never used as the sole basis of a constant.

All files cited as `sources/...` are under
`(a temporary session folder, not kept)`.

---

## 1. Summary

1. Real ballots agree on a small set of vocal delivery criteria: rate/pace, pauses, pitch variety, emphasis, volume, articulation (plus fillers, which this dataset cannot produce). None gives a numeric threshold. Section 2.
2. Published numbers exist for perceptual floors (tempo 5 % JND and 15 % attitude change; pitch 3 semitones; level 1.5-3 dB; pause 0.2 s) and for typical values of skilled speakers. No primary source gives a numeric cut-off for "monotone" or a norm for loudness variability. Section 3.
3. Proposed rubric: 7 dimensions (Pace, Pauses, Pitch variation, Emphasis, Volume, Clarity, Endings), each mapped 1:1 to a flaw recipe already present in the flaw-synthesis probe. All features are in log-like units, each recording is centred on its own median, and a deviation counts only if it exceeds both the natural reader-to-reader difference and a sourced perceptual floor. Section 4.
4. Recommended scoring: per-dimension linear capped point deduction on severity x share of speech, equal weights, no learned regressor. It is deterministic, bounded in [0, 100], monotone, and exactly additive, so every lost point is assigned to one listed flaw region and "score if fixed" is exact. Section 5.
5. Explanations: deterministic templates over a fixed JSON schema; no LLM at runtime. The vendor documentation itself states that identical outputs are not guaranteed, and current models reject `temperature` settings other than the default. Section 6.
6. "Causal": three claims are honest (measurement, exact score attribution/counterfactual, and injected-cause recovery on DSP pairs). Claims about listeners must be worded as cited findings, never as effects the system observed. Section 7.
7. Six points of disagreement with the preliminary direction. Section 8.

---

## 2. Q1 - Real judging rubrics: delivery dimensions and level descriptors

### 2.1 Exact wording (all VS)

| Instrument (event) | Delivery wording, verbatim | Scale / levels | Source |
|---|---|---|---|
| NSDA comment sheet, **Declamation** | "Delivery: Is the speech, as performed, appropriate for the situation? Does the student use voice, posture, and gestures to enhance the message?" | Rank + "Speaker Points ___ (out of 100)" | `sources/nsda_sample_ballot_all_speech.txt` l.29-34, 51; https://www.speechanddebate.org/wp-content/uploads/Sample-Ballot-All-Speech-Events-Blank.pdf |
| NSDA comment sheet, **Extemporaneous** (same text on Impromptu) | "Delivery: Is the student using voice, movement, and expression effectively? Is the speaker confident? Is there consistent eye contact? Is the volume appropriate?" | same | same file l.91-97 |
| NSDA comment sheet, **Original Oratory** | Three prompts: Importance ("Does the delivery assist in establishing the importance of the topic?"), Relatability ("Is the delivery personable?"), Originality. No separate delivery box. | same | same file l.291-315 |
| NSDA comment sheet, **Prose/Poetry** (interpretive reading from a manuscript) | "Vocalization: Does the presenter bring the words to life? In Prose: does the presenter's use of vocal qualities like diction, pausing, and volume advance the narrative? In Poetry: does the presenter's use of vocal qualities like rhythm, pacing, and volume advance the performance?" | same | same file l.407-415 |
| NSDA "How to Judge Declamation" | "The event is not designed for students to mimic the original author of the speech. Instead, speakers are to develop an oration that delivers the message of the author in an original and engaging manner." | - | `sources/nsda_how_to_judge_declamation.txt`; https://www.speechanddebate.org/how-to-judge-declamation/ |
| NSDA "How to Judge Prose" | "Does the presenter's use of vocal qualities like diction, pausing, and volume advance the narrative?"; "speaker points, typically in a range from 90 and 100, with 100 being outstanding" | 90-100 in practice | `sources/nsda_how-to-judge-prose.txt`; https://www.speechanddebate.org/how-to-judge-prose/ |
| NSDA Declamation Starter Kit | "Every word you deliver should come across loud and clear to the audience."; "If your speech is too fast paced, your audience won't catch a word you say. And if it's monotonous, your audience won't recall a word you said"; "by mastering inflection, intonation, and dramatic pausing, we can adjust the pace"; "No two people are the same, which means no two performers should ever perform a speech the exact same way." | coaching text | `sources/nsda_declamation_starter_kit.txt` l.197-260; https://www.speechanddebate.org/wp-content/uploads/Declamation-Starter-Kit.pdf |
| Original Oratory ballot instructions (NC affiliate copy of the NSDA text) | "Delivery should be judged for mastery of the usual mechanics of speech -- poise, quality and use of voice, bodily expressiveness, and for the qualities of directness and sincerity which impress the oration upon the minds of the audience."; "No particular style of delivery is to be set up as the one correct style to which all contestants must conform." | rank | `sources/ncsda_judging_oo.txt`; http://www.ncspeechanddebate.org/uploads/5/4/1/3/54138439/judging_original_oratory.pdf |
| UIL (Texas) Extemporaneous, **Informative** and **Persuasive** | "Vocal Delivery: Was enunciation clear? Was volume appropriate? Was there sufficient variety in rate, pause, and pitch?" | checklist | `sources/uil_informative.txt` l.517-527, `sources/uil_persuasive.txt`; https://www.uiltexas.org/speech/extemp/criteria-for-evaluating-persuasive-speakers |
| Toastmasters International Speech Contest ballot, Item 1172 Rev. 05/2024 | "Voice is the sound that carries the message. It should be flexible, moving from one pitch level to another for emphasis, and should have a variety of rate and volume. A good voice can be clearly heard and the words easily understood." | Delivery 30 of 100 points; "Voice - Flexibility, Volume" = 10 points: Excellent 10, Very Good 7-9, Good 4-6, Fair 0-3 | `sources/toastmasters_1172_intl_ballot.txt`; https://content.toastmasters.org/image/upload/1172-international-speech-contest-ballot-ff.pdf |
| Public Speaking Competence Rubric (Schreiber, Paul & Shibley 2012), item 7 "Effectively uses vocal expression and paralanguage to engage the audience" (as reproduced in ETS RR-15-36, Appendix B) | Advanced (4): "Excellent use of vocal variation, intensity, and pacing; vocal expression natural and enthusiastic; avoids fillers". Proficient (3): "Good vocal variation and pace; vocal expression suited to assignment; generally avoids fillers (e.g., um, uh, like)". Basic (2): "Demonstrates some vocal variation; enunciates clearly and speaks audibly; fillers ... present but do not detract from the message". Minimal (1): "Sometimes uses a voice too soft or articulation too indistinct for listeners to comfortably hear; often uses fillers". Deficient (0): "Speaks inaudibly; enunciates poorly; speaks in monotone; poor pacing; distracts listeners with fillers" | 0-4, plus an "N/A" column | `sources/eric_EJ1109251.txt` l.1069-1082; https://files.eric.ed.gov/fulltext/EJ1109251.pdf |
| NCA Competent Speaker Speech Evaluation Form (2nd ed., 2007), Competency Six "Uses vocal variety in rate, pitch, and intensity (volume) to heighten and maintain interest" | Excellent: "vocals are exceptionally and appropriately well-paced, easily heard by all audience members, and varied in pitch to enhance the message". Satisfactory: "only occasional weakness in pace, volume, pitch, etc., thereby not detracting significantly from the overall quality or impact". Unsatisfactory: "frequent weakness in controlling and adapting pace, volume, pitch, etc." | 3 levels | `sources/nca_competent_speaker_une.txt` l.514-531; https://www.une.edu/sites/default/files/Public-Speaking2013.pdf |
| NCA, Competency Seven "Uses pronunciation, grammar, and articulation" | Excellent: "exceptional fluency, properly formed sounds which enhance the message". Satisfactory: "most sounds are properly formed, there are only minor vocalized disfluencies". Unsatisfactory: "nonfluencies and disfluencies interfere with the message" | 3 levels | same file l.537-554 |
| AAC&U Oral Communication VALUE rubric, "Delivery" | Capstone 4: "Delivery techniques (posture, gesture, eye contact, and vocal expressiveness) make the presentation compelling, and speaker appears polished and confident." 3: "... interesting, and speaker appears comfortable." 2: "... understandable, and speaker appears tentative." 1: "... detract from the understandability of the presentation, and speaker appears uncomfortable." Glossary: "uses the voice expressively, and uses few vocal fillers" | 4 levels; "not for grading" | `sources/aacu_oral_comm_value_utah.txt`; https://us.utah.edu/_resources/documents/general-education/rubrics/Oral%20Communication%20Value%20Rubric.pdf ; https://www.aacu.org/initiatives/value-initiative/value-rubrics/value-rubrics-oral-communication |
| Poetry Out Loud Judge's Guide 2021-22 (recitation; closest published rubric to interpretive reading) "Voice and Articulation" | "Consider the student's projection, pace, intonation, rhythm, and proper pronunciation."; "Decide whether the pauses come in suitable places for the poem. A recitation that is at a too slow or hurried pace, poorly projected, has a distracting rhythm or monotone delivery will obscure a poem's meaning for the audience." Rubric row, Weak to Outstanding: "No projection; slow pace; distracting rhythm; singsong; hurried; mispronunciations" / "Insufficient or excessive projection; monotone; paced unevenly; affected tone" / "Clear, adequate intonation, even pacing" / "Clear, appropriate intonation and pacing" / "Very clear, crisp, effective use of projection, intonation, rhythm, and pacing" / "Very clear, crisp, mastery of rhythm and pace, skillful use of projection and intonation" | 1-6 per category (max 41 total) | `sources/pol_judges_guide_2021_22.txt` l.167-178, 335-362; https://vca.virginia.gov/wp-content/uploads/2022/12/POL-Judge_s-Guide-2021-22-1.pdf |
| 4-H **Interpretive Reading** (Colorado, Arapahoe County 2022 guidelines) | "will deliver a rendition of a piece of pre-written material ... Members may choose which selection or multiple portions of a text to present, but may not change the content." | ribbons; voice criteria are on a separate score sheet that was not retrieved | fetched PDF text (this run); https://arapahoe.extension.colostate.edu/wp-content/uploads/sites/10/2021/11/2022-speech-demo-interpretive-reading-guidelines.doc.pdf |

Not found: the current NSDA High School Unified Manual (2024-25, `sources/nsda_hs_unified_manual_2024_25.txt`) contains event rules for Original Oratory but no delivery judging criteria; the "mechanics of speech" wording survives only on the affiliate ballot copy above (VS for the affiliate copy; its presence in a current NSDA document: no source found).

### 2.2 Which vocal dimension each instrument names

| Instrument | Rate / pace | Pauses | Pitch / intonation | Emphasis | Volume / projection | Articulation | Fillers / fluency |
|---|---|---|---|---|---|---|---|
| NSDA Prose/Poetry ballot | pacing, rhythm | pausing | - | - | volume | diction | - |
| NSDA Extemp ballot | - | - | - | - | "Is the volume appropriate?" | - | - |
| NSDA Declamation Starter Kit | pacing | dramatic pausing | inflection, intonation, "monotonous" | "what you choose to put emphasis on" | "loud and clear" | enunciation | - |
| UIL Extemp | rate | pause | pitch | - | volume | enunciation | - |
| Toastmasters 1172 | variety of rate | - | "one pitch level to another" | "for emphasis" | variety of volume; clearly heard | "words easily understood" | - |
| PSCR item 7 | pacing | - | vocal variation; monotone | - | intensity; too soft; inaudible | enunciates | fillers |
| NCA Comp. 6 / 7 | rate, pace | - | pitch | - | intensity (volume) | articulation, pronunciation | disfluencies |
| AAC&U Delivery | - | - | vocal expressiveness | - | - | - | vocal fillers |
| Poetry Out Loud | pace, rhythm | "pauses come in suitable places" | intonation; monotone; singsong | emphasis (in "Evidence of Understanding") | projection | pronunciation; "clear, crisp" | - |

### 2.3 Three facts from these sources that shape the design

1. **No instrument gives a numeric threshold.** Levels are separated by words such as "occasional" versus "frequent" (NCA) or by lists of faults (POL, PSCR). Every number in Section 4 therefore comes from the phonetics literature or is a declared design choice.
2. **Human raters disagree most on exactly this dimension.** Two expert raters gave the same PSCR "vocal expression" score on 30 % of presentations (exact agreement; 100 % within one point), the lowest exact agreement of all dimensions together with "adapts to audience" (VS: `sources/eric_EJ1109251.txt` l.466, 494; ETS RR-15-36). Between-rater ICC for holistic public-speaking scores was 0.385 on 56 videos (VS: `sources/eric_EJ1126866.txt` l.430-431; Chen et al. 2016, doi:10.18608/jla.2016.32.13). This supports the brief's premise and is citable in the 6-page document.
3. **The competitive events explicitly reject imitation.** NSDA Declamation is "not designed for students to mimic the original author"; the OO ballot says no "one correct style". A reference-based system must therefore tolerate legitimate differences from the baseline (Section 4.2) and must word its output as "differs from the reference rendition", not "wrong" (Section 7).

---

## 3. Q2 - Empirical norms that can anchor thresholds

### 3.1 Speaking and articulation rate

| Quantity | Value | Population | Tag | Source |
|---|---|---|---|---|
| Just-noticeable difference for speech tempo | "about 5%" overall (-4 % for accelerations, +6 % for decelerations) | Dutch read speech, 2IAX and 2IFC | VS | Quene 2007, author preprint `sources/quene_2007_jnd_tempo_preprint.txt` l.23, 323-324; https://hugoquene.nl/onderzoek/q.jphon.20060912.pdf |
| Tempo change that shifted listener attitudes | time-compression to 85 % gave "a more positive attitude to the speaker"; expansion to 115 % "a more positive attitude to the message" (Megehee, Dobie & Grant 2003, as reported by Quene) | spoken advertisement | VS (secondary) | same file l.473-480 |
| Phrase-to-phrase tempo range of one "highly trained professional speaker" | average syllable duration 118-289 ms per phrase, mean 176, sd 35 (Nooteboom & Eefting 1994, as reported by Quene) | Dutch | VS (secondary) | same file l.455-457 |
| Intelligibility under compression | compressed to 65 % of original duration is "still reported to be 'perfectly intelligible'" (Janse 2004, as reported by Quene) | - | VS (secondary) | same file l.482-483 |
| TED talks, words per minute | 180.7 wpm over aligned speech (4.9 M words / 452 h); 151.2 wpm over all audio (540 h); 213.6 wpm over pure speech excluding silence (4437 K words / 346.17 h) | 2351 talks | VR (arithmetic) on VS (table values) | `derived_numbers.out` section B; TED-LIUM 3 Tables 3-4, `sources/tedlium3_1805.04699.txt`; https://arxiv.org/abs/1805.04699 |
| TED talks vs university lectures | 169 wpm vs 145 wpm | 49 TED talks, 727 lectures | UV (two search-engine summaries of the abstract; publisher page returned 403) | Wingrove 2017, https://www.sciencedirect.com/science/article/abs/pii/S1475158517301029 |
| TED speakers, articulation rate | 5.2 syll/s (American English TED speakers); read speech 4.9 syll/s (Baese-Berk & Morrill 2015) | 10 speakers | VS | Skarnitzl & Hledikova 2022, `sources/niebuhr_2022_fpsyg_857647.txt` l.487; https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.857647/full |
| Conversational English | speech rate median 175.9 wpm (IQR 156.0-195.9); articulation rate median 237.8 wpm (IQR 216.1-259.5) | 3,045 h dyadic conversation | VS | Hallur et al. 2026, `sources/arxiv_2606.31055.txt` Table I; https://arxiv.org/abs/2606.31055 |
| British English by situation | "150-190 words per minute" (average speaker); "140 (lecture) to 210 wpm (conversation)" | Tauroza & Allison 1990, cited by two later papers | VS (secondary; the original abstract contains no numbers) | `sources/frontiers_2018_02308.txt` l.113; `sources/tannander_edlund_2021_ssw.txt` l.157-158 |
| Coaching exemplar tempo used by prior systems | anchor "120-140 WPM", optional target "150-170 WPM" | survey of 15 systems | VS | Liang et al. 2026, `sources/arxiv_2606.27380.txt` l.516-517; https://arxiv.org/abs/2606.27380 |
| Steve Jobs vs Mark Zuckerberg | 4.4 vs 5.9 syll/s | keynote speech | VS (secondary table) | Fischer et al. 2021 Table 1 (after Niebuhr et al. 2016), `sources/fischer_2021_frobt_680509.txt`; https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2021.680509/full |
| Lowest-rated political speaker | 3.46 syll/s including pauses ("extremely slow") | Swedish parliament | VS | Strangert & Gustafson 2008, `sources/strangert_gustafson_2008.pdf`; https://www.isca-archive.org/interspeech_2008/strangert08_interspeech.pdf |
| Reagan, Challenger address opening (probe excerpt) | 187.0 wpm including pauses (74 words in 23.74 s) | this project's baseline | VR | `derived_numbers.out` section A (CTC word timings from `../kaggle_probe_audio/reagan_excerpt_words.json`) |
| Rate stabilisation time for free (non-anchored) rate estimates | "average stabilization time of 12.1 s (most values between 7.9 and 16.2 s)" | - | VS (secondary) | Hallur et al. 2026, same file l.112-114 |
| Comprehension limit | declines faster beyond about 275 wpm (Foulke & Sticht 1969) | - | UV (search summary only) | doi:10.1037/h0027575 |
| Same text, 15 different readers | total file duration 115.5-214.8 s, median 137.4 s, max/min 1.86; SD of ln(duration) 0.169 | LibriVox Gettysburg Address, public domain; durations include the LibriVox intro/outro | VS (archive.org metadata) + VR (arithmetic) | `sources/archive_meta_gettysburgaddress_150anniv_1311_librivox.json`; `derived_numbers.out` section C; https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |

Consequence: overall tempo differs by about 17 % (1 SD) between ordinary readers of the same text, more than three times the 5 % JND. Overall tempo must be normalised out before local pacing is compared, and the overall-tempo check needs a wide band.

### 3.2 Pauses

| Quantity | Value | Tag | Source |
|---|---|---|---|
| Pause categories | "brief (< 200 ms), medium (200-1000 ms) and long (> 1000 ms) pauses, the latter occurring only in spontaneous speech"; durations are log-normal | VS | Campione & Veronis 2002, `sources/campione_veronis_2002.txt`; https://www.isca-archive.org/speechprosody_2002/campione02_speechprosody.pdf |
| English read speech | 747 pauses in 43.9 min (17.0 per min, derived); median 493 ms, geometric mean 453 ms; fitted modes 126 ms and 512 ms, crossover 220 ms | VS | same, Tables 1-2 |
| Operational pause threshold | "inter-word gaps >= 0.2 s, a common practical threshold because shorter silences are difficult to distinguish from stop closures"; speech rate = 60 W/T, articulation rate = 60 W/(T-P), pause ratio = P/T | VS | Hallur et al. 2026, `sources/arxiv_2606.31055.txt` l.118-132 |
| Conversational English | pause ratio median 0.2575 (IQR 0.2166-0.2996); mean pause duration median 0.5845 s | VS | same, Table I |
| Professional vs non-professional reading (Swedish) | silence-to-speech ratio 9 % vs 28 %; pauses 40-600 ms vs 245-2040 ms; articulation rate 5.8 syll/s in both | VS | Strangert 2005, `sources/strangert_2005.pdf`; https://www.isca-archive.org/interspeech_2005/strangert05_interspeech.pdf |
| Prepared political speeches (French) | "The total time of silent pauses was 50% greater in political speeches than in either type of interview"; pauses mostly "at clause or phrase boundaries"; long ones "must have a predominantly stylistic function" | VS (abstract) | Duez 1982, doi:10.1177/002383098202500102; `sources/openalex_abstracts.json` key `duez1982` |
| Silences inside clauses | "mean of the silences within clauses" correlated with human holistic public-speaking scores at abs(r) = 0.479 (sign not reported; impromptu task, n = 28) | VS | Chen et al. 2016, `sources/eric_EJ1126866.txt` l.628-631 |
| Jobs vs Zuckerberg | mean silent pause 200 ms vs 500 ms | VS (secondary table) | Fischer et al. 2021 Table 1 |
| Reagan excerpt | 12 gaps >= 0.2 s in 23.74 s (30.3 per min); median 0.54 s; sentence-boundary gaps 0.80-1.16 s; pause ratio 0.32 | VR, with a caveat: CTC word ends are early, so gaps overstate acoustic silence (the implied 275 wpm articulation rate is implausibly high) | `derived_numbers.out` section A |

### 3.3 Pitch variability

| Quantity | Value | Tag | Source |
|---|---|---|---|
| Pitch-distance discrimination | "average jnd's of about 1.5 to 2 semitones"; "only differences of more than 3 semitones play a part in communicative situations" | VS (abstract) | 't Hart 1981, `sources/thart_1981_efetch.txt`; https://pubmed.ncbi.nlm.nih.gov/7240562/ |
| F0 range of political speakers, 25th-75th percentile | 2.44-8.78 st, median 4.7; correlation with good-speaker rating r = .61 (p = .01) | VS | Strangert & Gustafson 2008 |
| Ordinary non-professional speakers, same measure | "a range of 2-5 semitones" (498 speakers) | VS | same |
| Lowest-rated ("monotonous") speaker | 2.84 st; "monotonous" correlated r = -.91 with good-speaker rating | VS | same |
| Newsreaders, 10th-90th percentile range | 7.1 st (British female), 8.1 st (British male) (Volin et al. 2015); TED speakers, English: 7.05 st | VS (secondary / primary) | Skarnitzl & Hledikova 2022, l.186 and Table 2 |
| Project baselines, 5th-95th percentile | Reagan 78.0-128.1 Hz = 8.59 st; JFK 174.5-265.8 Hz = 7.29 st (30 s clips, Praat autocorrelation) | VR (sibling features probe, previous local run) + VR (conversion) | `../features/out_f0_run1.md`; `derived_numbers.out` section D |
| Normal-distribution equivalents (assumption: semitone values roughly normal, as argued by Hincks & Edlund) | IQR 2-5 st is SD 1.5-3.7 st; 7.05 st (P10-P90) is SD 2.75 st; Reagan 2.6 st; JFK 2.2 st | VR (arithmetic) | `derived_numbers.out` section D |
| Pitch-variation feedback metric with a track record | "standard deviation of fundamental frequency as measured in semitones" over "a moving 10-second window"; semitones give "a kind of perceptual speaker normalization" | VS | Hincks & Edlund 2009, `sources/hincks_edlund_2009.txt`; https://www.lltjournal.org/item/10125-44190/ |
| Conversational English | F0 SD (10-90 % trimmed) median 20.84 Hz at mean 157.4 Hz | VS | Hallur et al. 2026 Table I |
| Jobs vs Zuckerberg "mean pitch range" | 22.9 st vs 12.1 st (range definition differs from the percentile ranges above; not comparable) | VS (secondary table) | Fischer et al. 2021 Table 1 |
| Numeric cut-off for "monotone" | **No primary source found.** The only number located ("below 1.5 semitones SD") is on a non-scholarly web page and is not used. | - | - |

### 3.4 Loudness, final lowering, and perception studies

| Finding | Type of evidence | Tag | Source |
|---|---|---|---|
| JND for broadband level increments in speech-shaped noise: 1.5 dB at d' = 1; "noticeable fine-tuning adjustments of 3 dB" | psychoacoustic, 38 hearing-impaired listeners | VS | Caswell-Midwinter & Whitmer 2019, doi:10.1177/2331216518820220; `sources/pmc6351966_efetch.xml` |
| Speakers attempting to persuade "speak louder and vary their volume ... both of which signal confidence and, in turn, facilitate persuasion" | experiments + exploratory analysis | VS (abstract) | Van Zant & Berger 2020, doi:10.1037/pspi0000193 |
| Mean and SD of RMS intensity over phrases correlate positively with charisma ratings (r = .14 to .35 across five rater/language combinations); disfluency negatively (r = -.18 to -.48) | correlational | VS | Biadsy et al. 2008, `sources/biadsy_2008_sp.pdf`; https://www.isca-archive.org/speechprosody_2008/biadsy08_speechprosody.pdf |
| Energy features separate TED talks from classroom lectures better than pitch features; TED talks "spend less time in silence and filler"; recording quality is a confound the author names | classifier study | VS | Tsai 2015, `sources/tsai_2015_ted.pdf`; https://www.isca-archive.org/interspeech_2015/tsai15b_interspeech.pdf |
| Norm for loudness variability (dB SD) of effective speakers | **No source found.** | - | - |
| English broadcast-news utterances: 71.5 % have a negative F0 regression slope; contour consists of "initial rising, middle declination, and final lowering" | corpus, 5,652 utterances | VS | Yuan & Liberman 2010, `sources/yuan_liberman_2010_declination.txt`; https://www.isca-archive.org/interspeech_2010/yuan10_interspeech.pdf |
| Magnitude of final lowering (4-27 Hz below prediction; last ~250 ms) (Liberman & Pierrehumbert 1984) | - | UV (search summary) | - |
| "falling (vs. rising) vocal intonation at the ends of sentences can signal speaker confidence"; manipulation: pitch on "only the last word of the chosen sentences" raised or lowered "by 35 hertz"; confidence rating 5.55 vs 4.82, F(1, 273) = 14.25, p < .001. The benefit for persuasion held only for strong arguments. | experimental (resynthesis) | VS | Vaughan-Johnston et al., Pers. Soc. Psychol. Bull. 52(1) 3-21, doi:10.1177/01461672241262180; `sources/pmc12681368_vaughan_johnston.txt`. +35 Hz is +4.1 to +5.2 st for a 100-130 Hz voice (`derived_numbers.out` D) |
| Vocal speed (fast vs slow) and intonation (falling vs rising) "influenced global perceptions of speaker confidence" | experimental | VS (abstract) | Guyer, Fabrigar & Vaughan-Johnston 2019, doi:10.1177/0146167218787805 |
| "rapid speech enhances persuasion" (speech rate as a credibility cue) | field experiments, 449 participants | VS (abstract) | Miller et al. 1976, https://experts.umn.edu/en/publications/speed-of-speech-and-persuasion |
| Resynthesis of the lowest-rated speaker: doubling the F0 standard deviation (+2 st mean), removing disfluencies, and +5 % rate with shortened hesitation pauses; listeners preferred modified versions, "F0 dynamics > fluency > speech rate" in perceptual weight | experimental (12 listeners, Kendall W = .48) | VS | Strangert & Gustafson 2008 |
| F0 mean and SD, speaking rate positively correlated with charisma ratings in American political speech (exact coefficients not recoverable from the PDF text) | correlational | VS (direction only) | Rosenberg & Hirschberg 2005, `sources/rosenberg_hirschberg_2005_interspeech.txt`; https://www.isca-archive.org/interspeech_2005/rosenberg05_interspeech.pdf |
| Primary stress: with correct stress listeners "recalled significantly more content and evaluated the speaker significantly more favorably than when primary stress was aberrant or missing" | experimental | VS (abstract) | Hahn 2004, doi:10.2307/3588378 |
| Emphatic accents per minute: Jobs 8.4, Zuckerberg 1.6 | descriptive | VS (secondary table) | Fischer et al. 2021 Table 1 |
| "Overdose": above a threshold, more of a prosodic parameter reduces perceived charisma ("too high-pitched or too fast") | perception experiments summarised by the authors | VS | Niebuhr, Tegtmeier & Schweisfurth 2019, `sources/niebuhr_2019_fcomm_00012.txt` l.131; https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2019.00012/full |

Reading of this table: effects are directional and mostly small (correlations of .1-.6), language- and culture-dependent (Biadsy et al. report rate correlating positively for American and Swedish raters of English and not for Palestinian raters of Arabic), and non-monotone at the extremes (overdose). They justify the choice of dimensions and the wording of "why it matters"; they do not justify absolute "ideal" values. This is the reason the rubric is defined relative to a reference rendition with two-sided tolerances.

---

## 4. Q3 - Proposed rubric

### 4.1 Seven dimensions

Unit conventions: `B` = baseline rendition, `P` = participant. Word timings come from forced alignment of both recordings to the same transcript. "Window" = 5 consecutive words centred on word i (about 1.6 s at 187 wpm). Tilde = median over all scorable units of one recording.

| # | Dimension (rubric wording it answers) | Definition | Acoustic operationalisation (feature f, unit) | "Deviation from baseline" | Flaw types (sign) | Flaw recipe in `../flaw_synthesis/flawlib.py` |
|---|---|---|---|---|---|---|
| D1 | **Pace** ("well-paced", "variety in rate", "hurried", "too slow") | Where the speaker speeds up and slows down, and overall tempo | f_i = ln(speech time of the window, pauses >= 0.2 s removed). Local: x_i = (f_i^P - f~^P) - (f_i^B - f~^B) = log duration ratio with overall tempo removed. Global: g = median over i of ln(window time P / window time B) | x_i < 0: these words are faster than the reference pacing; x_i > 0: slower | RUSH (-), DRAG (+), TEMPO_FAST / TEMPO_SLOW (global) | `rate_span_*` |
| D2 | **Pauses** ("pauses come in suitable places", "pausing", "variety in ... pause") | Presence and length of silence at each word boundary | y_j = ln(max(silence_j, 0.1 s) / 0.1 s), silence = acoustic silence inside the inter-word gap, counted from 0.2 s. Event unit = word boundary. x_j = y_j^P - y_j^B | x_j < 0 at a boundary where the reference holds >= 0.5 s: pause dropped or shortened. x_j > 0 where the transcript has no punctuation and the reference has no pause: break inside a phrase. x_j > 0 at punctuation: over-long pause | PAUSE_DROPPED (-), PAUSE_INTRUSIVE (+, no punctuation), PAUSE_OVERLONG (+, punctuation) | `insert_pause`, `remove_pause` |
| D3 | **Pitch variation** ("varied in pitch", "monotone", "singsong", "vocal variation") | How much the melody moves | F0 in semitones re the recording's own median: st = 12 log2(F0 / F0~). f_i = P90 - P10 of st over voiced frames in the window (needs >= 0.5 s voiced). Local x_i as in D1; global g = f~^P - f~^B | x_i < 0: flatter than the reference here; x_i > 0: more exaggerated | MONOTONE (-), OVER_INFLECTED (+), RANGE_NARROW / RANGE_WIDE (global) | `flatten_f0_*` |
| D4 | **Emphasis** ("for emphasis", "what you choose to put emphasis on") | Whether the words the reference makes prominent are made prominent | Per word, prominence p_i = mean of three robust within-recording z-scores: F0 peak (st above window median), energy peak (dB above window median), lengthening (ln word duration / window mean). Landmarks = baseline content words with p_i^B >= 1.0. x_i = p_i^P - p_i^B on landmarks only | x_i < 0: the reference stressed this word, the participant did not | DEEMPHASIS (-) | `deemphasize_psola` |
| D5 | **Volume** ("Is the volume appropriate?", "voice too soft", "trails off") | Level relative to the speaker's own typical level, along the text | f_i = mean level (dB) of speech frames in the window. Local x_i as in D1. No global term: absolute gain of an uploaded file is unknown | x_i < 0: quieter than the reference at this point relative to own level; x_i > 0: louder | FADE / TRAIL_OFF (-), SURGE (+) | `gain_ramp` |
| D6 | **Clarity** ("enunciates clearly", "properly formed sounds", "words easily understood") | Distinctness of articulation | f_i = clarity index of the window = mean of (a) forced-aligner per-word confidence (log-posterior; a Goodness-of-Pronunciation-style score), (b) MFCC-delta magnitude (rate of spectral change), (c) 2-8 kHz to total energy ratio in dB; each expressed as a robust z within the recording. Local x_i as in D1; global g = difference of medians of component (a) | x_i < 0: less distinct than the reference here | MUMBLE (-) only; positive values are not penalised | `mumble`, `mumble_world` |
| D7 | **Endings** (the brief's "cadence"; falling vs rising sentence ends) | Direction and size of the final pitch movement of each sentence | For each sentence-final word (transcript `.`, `?`, `!`): m_j = median st over the final word minus median st over the two preceding words. x_j = m_j^P - m_j^B | x_j > 0 where the reference falls: rising ending; x_j < 0 where the reference rises: flattened question | UPTALK (+), FLAT_QUESTION (-) | `uptalk_psola` |

Notes on the choices:

- Seven dimensions give a 1:1 map to the injected flaw types, which makes a per-dimension confusion matrix and the explanation templates direct. D7 has the weakest rubric basis (no ballot names it; the basis is experimental, Section 3.4). If the final dataset contains no uptalk edits, fold D7 into D3 and use six dimensions.
- **Fillers and disfluencies are not scored.** They appear in PSCR, NCA and AAC&U, but a DSP + TTS bad spectrum of the exact same transcript contains none, and a transcript-anchored aligner assumes the words are as written. State this as a limitation.
- **Absolute loudness is not scored**: an uploaded file has unknown gain. Poetry Out Loud gives judges the same instruction for virtual contests ("judge based on the official evaluation criteria and not the quality of the audio or video").
- The survey of 15 coaching systems uses the same top-level split - prosody (F0, rhythm, phrasing), pacing (WPM, pauses, articulation rate), pronunciation - and reports that "assessment typically compares log-F0 contours and duration patterns between learner and reference utterances" (VS: `sources/arxiv_2606.27380.txt` l.98, 185-191).

### 4.2 Normalisation rule (speaker-agnostic by construction)

One rule for all dimensions:

1. Express every feature in a log-like unit: ln(seconds), semitones, dB.
2. Subtract the recording's own median (location only, never scale). In these units that removes overall tempo, pitch level (male/female/pitch-shifted) and gain/channel level exactly. A pitch-ratio, gain or tempo transform of a recording leaves every local feature unchanged.
3. Compare the centred local patterns: x_i = (f_i^P - f~^P) - (f_i^B - f~^B).
4. Where the median itself is meaningful, compare it once as a global term g with a wide tolerance (D1 tempo, D3 range, D6 clarity).

Why not divide by the speaker's own spread (z-scoring per speaker): a participant who is flat throughout would then look normal. Why a separate global term: natural same-text differences between readers are large in level (tempo SD 17 %, Section 3.1) and small in pattern, so one tolerance cannot serve both.

Deviation is then expressed in null units:

```
z = x / s_k            s_k = max( s_null_k , MMD_k / z_hi )
s_null_k = 1.4826 * MAD( x over all units of all good-vs-good pairs, both orderings )
```

so the flag threshold in physical units is `max(z_hi * s_null_k, MMD_k)`: a deviation is flagged only if it is larger than what two competent readers of the same text typically differ by AND larger than a sourced perceptual floor. z has a plain-language reading for the user: "z times the typical reader-to-reader difference".

`MMD_k` (minimum meaningful difference) per dimension:

| Dimension | MMD | Basis | Tag |
|---|---|---|---|
| D1 local pace | ln 1.15 = 0.140 (15 %) | JND 5 %; +-15 % manipulation changed attitudes (Quene 2007, citing Megehee et al.) | VS |
| D1 global tempo | ln 1.40 = 0.336 (x0.71 to x1.40) | 14 of 15 LibriVox readers of the same text lie within [0.70, 1.40] x the median duration; SD of ln = 0.169 | VS + VR; the band itself is a design choice |
| D2 pauses | presence 0.2 s; landmark pause 0.5 s; x floor ln 2 | 0.2 s: Campione & Veronis, Hallur et al.; 0.5 s: medium-pause mode 512 ms; factor 2: design choice | VS / design |
| D3 pitch variation | 3 st | 't Hart 1981 | VS |
| D4 emphasis | 1.0 (in prominence z units) | design choice; components individually use 3 st and 3 dB | design |
| D5 volume | 3 dB | Caswell-Midwinter & Whitmer 2019 (1.5 dB JND; 3 dB "noticeable"); listeners were hearing-impaired, stimuli noise | VS, with caveat |
| D6 clarity | none (null-based only) | no perceptual unit found | no source found |
| D7 endings | 3 st | 't Hart 1981; +-35 Hz (about 4-5 st) on the last word changed perceived confidence | VS |

### 4.3 Level descriptors

Levels are bands of the dimension score S_k of Section 5 (band edges 90 / 75 / 50 / 25 are a design choice; no ballot supplies numeric edges). A dimension with no scorable units is reported "N/A" and dropped from the total, as PSCR does.

| Level | S_k | Generic descriptor (modelled on NCA "occasional / frequent weakness") |
|---|---|---|
| 5 On reference | >= 90 | No flagged region, or one brief mild one. Delivery on this dimension is within reader-to-reader tolerance of the reference. |
| 4 Minor | 75 - 89.9 | Occasional mild deviation; the reference pattern is clearly followed. |
| 3 Noticeable | 50 - 74.9 | Repeated mild deviations or one strong, sustained one. |
| 2 Major | 25 - 49.9 | Frequent or strong deviations; the reference pattern is only partly recognisable. |
| 1 Severe | < 25 | Pervasive or egregious deviation across most of the speech. |

Dimension-specific wording for the dashboard and the rubric page:

| Dim | Level 5 | Level 3 | Level 1 |
|---|---|---|---|
| D1 Pace | Speeds up and slows down where the reference does; overall tempo within x0.71-x1.40 | One long or several short passages rushed or dragged by more than 15 % | Most of the speech rushed or dragged, or overall tempo about half / double the reference |
| D2 Pauses | Holds the reference's major pauses; no breaks inside phrases | Some major pauses dropped or halved, or a few breaks inside phrases | Most major pauses missing, or frequent mid-phrase breaks |
| D3 Pitch variation | Melody moves as much as the reference, passage by passage | Clearly flatter (or more exaggerated) than the reference in several passages | Flat (or sing-song) through most of the speech |
| D4 Emphasis | The reference's stressed words are stressed | About a third of the reference's stressed words pass unstressed | Hardly any of the reference's stressed words are stressed |
| D5 Volume | Level holds up where the reference's does | Some passages or sentence ends fade by more than 3 dB relative to the reference | Level collapses through much of the speech |
| D6 Clarity | Articulation as distinct as the reference | Some passages clearly less distinct | Indistinct through most of the speech |
| D7 Endings | Sentences end with the reference's direction of pitch movement | Several statements end on a rise where the reference falls | Most statements end on a rise |

---

## 5. Q4 - Scoring methodology

### 5.1 Comparison of the three options

| Criterion | A. Deduction per flaw region (severity x share x weight), linear, capped | B. Similarity (distance to baseline through exp / logistic) | C. Small learned regressor on the dataset's severity levels |
|---|---|---|---|
| Deterministic | yes (arithmetic) | yes | yes at inference if the fitted model is frozen; training reproducibility is an extra burden |
| Monotone in severity | yes by construction (5.3) | yes in the distance; the distance itself is not zero for good renditions | only if constrained (isotonic, monotone GBM, non-negative weights) |
| Bounded | yes, [0, 100] by clipping | yes | needs clipping or a link function |
| Good different-speaker rendition scores high | yes: deviations inside the reader-to-reader tolerance contribute exactly 0 | needs an offset for the non-zero null distance | not guaranteed; depends on negatives seen in training |
| Constants to set | per dimension: s_null, z_sat, P_max; global: z_hi | tau (and an offset) per dimension | all model parameters |
| Examples needed | null pairs for s_null; 1 anchor file per dimension | same | many graded files per flaw type; labels are the designer's own DSP parameters |
| Every lost point traceable to a time span | yes, exactly (score is a sum over listed regions) | no (needs a separate attribution step) | only for linear models (phi_i = w_i (x_i - E[x_i]), Lundberg & Lee 2017, Corollary 1, VS: `sources/shap_1705.07874.txt` l.388-399) |
| Counterfactual "score if fixed" | exact and equal to the attributed points | exact but not additive | exact for linear models |
| Risk specific to this project | hard thresholds give a step when a region first opens | steep near zero: with the same anchor the exponential gives 77.0 where the linear rule gives 87.0 (golden vector, `derived_numbers.out` E) | can learn vocoder / PSOLA artefacts instead of delivery ("shortcut learning", Geirhos et al. 2020, VS abstract: https://arxiv.org/abs/2004.07780) |

Recommendation: **A**. B is A with a different final curve and worse behaviour for near-perfect renditions. C adds training without adding validity, because its target (the severity level) is the designer's own edit parameter.

### 5.2 Formulas

Inputs per dimension k: units u (words for D1, D3, D5, D6; events for D2, D4, D7), standardised deviations z_u (Section 4.2), and flaw regions r (sets of consecutive units) produced by the grounding stage with hysteresis thresholds z_hi (open) and z_lo (extend).

```
severity          sev(z)  = clip( (|z| - z_lo) / (z_sat_k - z_lo), 0, 1 )

unit weight       w_u     = d_u^B / sum of d^B over scorable units      (D1, D3, D5, D6; d^B = baseline word duration)
                  w_u     = 1 / N_k^B                                    (D2: N = baseline pauses >= 0.2 s;
                                                                          D4: N = baseline landmark words;
                                                                          D7: N = sentence ends)

region mass       m_r     = sum over u in r of  w_u * sev(z_u)
global mass       m_g     = 0.25 * sev(z_g)                              (D1, D3, D6 only; z_g = g / s_g)

penalty           P_k     = sum of m_r over regions of k  +  m_g
dimension score   S_k     = 100 * max(0, 1 - P_k / Pmax_k)
overall score     S       = sum over available k of  W_k * S_k ,   W_k = 1 / (number of available dimensions)

points lost by r  L_r     = W_k * 100 * m_r / max(P_k, Pmax_k)           (sum of all L_r = 100 - S, exactly)
score if r fixed  S^(-r)  = S + W_k * ( S_k(P_k - m_r) - S_k(P_k) )      (equals S + L_r while P_k <= Pmax_k)
```

Two details that are easy to get wrong:

- **Weights use baseline durations, not participant durations.** If participant time were used, a stronger RUSH would shorten its own region and could lower the penalty, breaking monotonicity. Timestamps shown to the user are participant time; weights are reference time.
- **Round once.** Quantise z to 0.01 before thresholding and store every reported number already rounded in the JSON; the text templates read the same rounded values. This keeps region boundaries and text identical across machines whose floating-point results differ in the last bits.

### 5.3 Properties

- Bounded: 0 <= S_k <= 100 and 0 <= S <= 100 by the max and the convex combination.
- Monotone: sev is non-decreasing in abs(z); if every abs(z_u) grows, regions can only grow or merge (thresholding of a pointwise larger sequence, with a non-negative smoothing kernel or a running median), every m_r is a sum of non-negative terms with fixed weights, so P_k is non-decreasing and S_k non-increasing. It is strictly decreasing between the detection threshold and saturation.
- Deterministic: closed-form arithmetic, no random numbers, no iteration.
- Additive: 100 - S = sum of L_r. Checked numerically in the golden vector (assertion in `derived_numbers.py`, VR).
- Different good speaker: units with abs(z) < z_lo contribute 0, regions open only at z_hi, and s_k is at least the reader-to-reader scale; pitch, gain and tempo transforms cancel exactly in the local terms.

### 5.4 Constants: defaults and how to set each from very few examples

| Constant | Default | How to set it | Examples needed |
|---|---|---|---|
| z_hi | 3.5 | Convention for robust z: "modified Z-scores with an absolute value of greater than 3.5 be labeled as potential outliers" (Iglewicz & Hoaglin via NIST, VS: https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm). Replace by the value the grounding research derives for its target false-region rate | none |
| z_lo | 0.5 * z_hi = 1.75 | same ratio as `LOW_RATIO` in `../grounding_model/sim_region_rules.py` | none |
| s_null_k | fallback MMD_k / z_hi | 1.4826 x MAD of x over good-vs-good pairs, both orderings, leave-one-reader-out. Available public-domain set: 15 readers of the Gettysburg Address (105 pairs, about 270 words each) | 3-5 pairs already give several hundred unit deltas per dimension |
| MMD_k | Section 4.2 table | fixed from literature; not tuned | none |
| z_sat_k | 8.0 | median abs(z) inside the injected spans of the highest severity level of that flaw type; keep within [z_hi + 1, 20] | 1 file per dimension |
| Pmax_k | 0.40 (D1, D3, D5, D6); 0.50 (D2, D4, D7) | Pmax_k = P_k(anchor) / 0.8, where the anchor is the dataset's worst exemplar for dimension k and should score 20 | 1 file per dimension |
| global mass weight | 0.25 | design choice: a global-only flaw can remove at most 62.5 % of a duration-type dimension | none |
| W_k | 1/7 each | no source supports unequal numeric weights. Ordinal evidence only: F0 dynamics > fluency > rate (Strangert & Gustafson 2008) | none |
| level bands | 90 / 75 / 50 / 25 | design choice | none |
| window, minimum region | 5 words; 3 words | defer to grounding and features research | none |

Precision of s_null (rule of thumb, UV, from memory): relative standard error of a MAD-based scale is about 1.16 / sqrt(n), i.e. about 8 % at n = 200 and 4 % at n = 750.

### 5.5 Worked example (golden test vector, VR)

Produced by `/usr/bin/python3 derived_numbers.py` (standard library, local, < 1 s), output in `derived_numbers.out` section E.

```
severity(|z|=3.50) = 0.280    severity(|z|=5.00) = 0.520    severity(|z|>=8.00) = 1.000
pace     P=0.0520 S=87.00     (RUSH: baseline-time share 0.10, mean |z| 5.0)
pauses   P=0.1333 S=73.33     (2 of 12 landmark pauses dropped, |z| 9.0 and 5.5)
pitch    P=0.2000 S=50.00     (MONOTONE: baseline-time share 0.20, |z| 9.0)
other four dimensions S=100
OVERALL = 87.19
points lost: RUSH 1.857 | pause 1: 2.381 | pause 2: 1.429 | MONOTONE 7.143   (sum 12.81 = 100 - 87.19)
score if MONOTONE fixed = 94.33
```

### 5.6 Acceptance tests to run on Kaggle before the constants are frozen

1. Invariance: baseline vs its own pitch-ratio, formant-ratio and gain transforms scores >= 99.
2. Null: held-out good-vs-good pairs (leave-one-reader-out). Design target: median >= 95, minimum >= 85. If it fails, raise z_hi; do not add per-speaker scale normalisation.
3. Monotone ladder: for every (speech, flaw type), S_k is non-increasing over severity levels and strictly decreasing over the detected ones.
4. Specificity: a flaw of type k lowers S_k more than any other dimension.
5. Determinism: two runs give byte-identical JSON.

### 5.7 Severity ladder anchors for the dataset (input to the flaw-synthesis design; proposal)

Defining the levels of each DSP edit as multiples of the perceptual floor makes "near-perfect" mean "just above what a listener can notice" and keeps the score monotone across flaw types.

| Flaw | L1 near-perfect | L2 | L3 | L4 | L5 egregious | Anchors |
|---|---|---|---|---|---|---|
| RUSH / DRAG (rate factor) | x1.10 | x1.20 | x1.35 | x1.6 | x2.0 | JND 5 %; 15 % shifts attitudes; x1.54 (65 % duration) still intelligible |
| MONOTONE (fraction of range kept) | 0.75 | 0.50 | 0.35 | 0.20 | 0.0 | with a 7-8.6 st baseline range, 0.75 removes about 2 st (below the 3 st floor), 0.5 about 4 st |
| PAUSE_DROPPED (landmark pause shortened to) | 0.75x | 0.5x | 0.33x | 0.2 s | 0.1 s | log-normal durations; 0.2 s presence threshold |
| PAUSE_INTRUSIVE (inserted, mid-phrase) | 0.3 s | 0.5 s | 0.8 s | 1.2 s | 2.0 s | > 1 s pauses "only in spontaneous speech" (Campione & Veronis) |
| FADE (level change by span end) | -3 dB | -6 | -9 | -12 | -18 | 3 dB noticeable |
| UPTALK (final-word rise) | +2 st | +3.5 | +5 | +7 | +9 | 3 st communicative threshold; published manipulations 35 Hz and 75 Hz (about 4-5 and 8-10 st) |
| DEEMPHASIS / MUMBLE (recipe strength) | 0.2 | 0.4 | 0.6 | 0.8 | 1.0 | no perceptual unit found |

---

## 6. Q5 - Causal explanations

### 6.1 Schema (one object per flaw region; all numbers pre-rounded)

```json
{
  "region_id": "pitch-003",
  "dimension": "pitch_variation",
  "flaw_type": "MONOTONE",
  "where": {
    "participant_span_s": [12.40, 24.10],
    "baseline_span_s": [11.95, 23.20],
    "word_index_range": [41, 78],
    "words": "we know we share this pain ... a national loss",
    "context": {"sentence_index": 4, "position": "sentence-medial to sentence-final",
                "baseline_landmarks": ["emphasis: 'share'", "pause 0.84 s after 'country'"]}
  },
  "how_much": {
    "feature": "pitch range P10-P90 in 5-word windows",
    "unit": "st",
    "baseline_value": 7.4,
    "participant_value": 2.1,
    "delta": -5.3,
    "null_scale": 0.9,
    "z": -5.89,
    "threshold": {"z_hi": 3.5, "physical": 3.2, "rule": "max(z_hi * s_null, MMD)"},
    "severity": 0.66,
    "severity_label": "major",
    "share_of_speech": 0.20
  },
  "score_effect": {"dimension_score": 67.0, "points_lost": 4.71, "overall_if_fixed": 91.9},
  "why": {"template_id": "why.monotone.v1",
          "basis": [{"cite": "Strangert & Gustafson 2008", "evidence": "experimental"},
                    {"cite": "NCA Competent Speaker form, Competency Six", "evidence": "rubric"}]},
  "fix": {"template_id": "fix.monotone.v1", "target": {"feature": "pitch range", "value": 7.4, "unit": "st"}},
  "audio": {"participant_clip": "clips/p_pitch-003.wav", "baseline_clip": "clips/b_pitch-003.wav"},
  "provenance": {"config_sha256": "...", "templates_version": "1.0.0", "feature_version": "..."}
}
```

The five parts answer the task's list: where (time span, words, context), what (flaw type, dimension), how much (baseline, participant, delta, z, threshold), why (listener impact with basis and evidence type), how to fix (with a numeric target). `score_effect` adds the exact counterfactual. The numbers in this example are illustrative.

### 6.2 Template sentences per flaw type

Each explanation is four fixed sentences: what/where, how much, why, fix. Formatting is fixed: seconds 2 decimals, semitones and dB 1 decimal, percentages integer, z 1 decimal.

| Flaw | What / where + how much | Why it matters (hedged, cited) | Fix |
|---|---|---|---|
| RUSH | "Rushed: {t0}-{t1} ('{words}'). You took {p_dur} s for these {n} words; the reference took {b_dur} s at your overall tempo - {pct} % faster ({z}x the typical reader-to-reader difference; flagged above {thr_pct} %)." | "Poetry Out Loud's judging guide says a 'hurried pace ... will obscure a poem's meaning for the audience', and NSDA's Declamation guide warns that if a speech is 'too fast paced, your audience won't catch a word you say'." | "Give this passage about {b_dur} s. Lengthen the stressed words rather than adding gaps." |
| DRAG | same, "{pct} % slower" | "In a listening experiment, speeding up a slow speaker and shortening hesitation pauses raised listeners' rankings (Strangert & Gustafson 2008); Poetry Out Loud lists a 'too slow' pace as a weakness." | "Tighten to about {b_dur} s; keep the pauses at punctuation and close the gaps inside the phrase." |
| MONOTONE | "Flat pitch: {t0}-{t1}. Your pitch moved {p_val} st here; the reference moved {b_val} st - {delta} st narrower (flagged above {thr} st)." | "Listeners rated narrow-range political speakers as 'monotonous', the quality most negatively related to being judged a good speaker, and widening the pitch range was the strongest cue when recordings were resynthesised (Strangert & Gustafson 2008). The NCA form expects pitch 'varied ... to enhance the message'." | "Lift your pitch on '{landmark_words}' and let it fall at the phrase end; aim for about {b_val} st of movement." |
| PAUSE_DROPPED | "Missing pause after '{prev}' at {t}. The reference holds {b_val} s of silence before '{next}'; you hold {p_val} s." | "In prepared political speeches silent pauses were more frequent and longer than in interviews, and the long ones served a stylistic function (Duez 1982, French). Judges are told to 'decide whether the pauses come in suitable places'." | "Stop fully after '{prev}' and hold about {b_val} s before '{next}'." |
| PAUSE_INTRUSIVE | "Break inside a phrase: {p_val} s of silence between '{prev}' and '{next}' at {t}. The reference runs these words together and the transcript has no punctuation here." | "Silences inside clauses were among the features most correlated with human scores of public-speaking performance (Chen et al. 2016), and removing hesitation pauses raised listeners' rankings in a resynthesis experiment (Strangert & Gustafson 2008)." | "Carry '{phrase}' on one breath; move the breath to '{nearest_punctuation}'." |
| DEEMPHASIS | "Key word not stressed: '{word}' at {t}. The reference lifts it {b_st} st above its phrase and {b_db} dB louder; you: {p_st} st, {p_db} dB." | "When primary stress was missing or misplaced, listeners recalled significantly less content and rated the speaker less favourably (Hahn 2004). Toastmasters asks for a voice 'moving from one pitch level to another for emphasis'." | "Stress '{word}': step up about {target_st} st and lengthen its stressed syllable." |
| FADE / TRAIL_OFF | "Volume drops: {t0}-{t1}. Relative to your own typical level you are at {p_val} dB; the reference stays at {b_val} dB - {delta} dB lower (flagged above {thr} dB)." | "Ballots ask 'Is the volume appropriate?' (NSDA) and rate 'a voice too soft ... for listeners to comfortably hear' as Minimal (PSCR). Speakers who spoke louder and varied their volume were judged more confident (Van Zant & Berger 2020)." | "Keep the last {n} words at the level of the first; breathe before '{first_word}'." |
| MUMBLE | "Unclear articulation: {t0}-{t1}. Clarity index {p_val} against {b_val} for the reference ({z}x the typical reader-to-reader difference)." | "Rubrics require 'properly formed sounds' (NCA) and penalise 'articulation too indistinct for listeners to comfortably hear' (PSCR). Basis: rubric only." | "Over-articulate the consonants in '{words}'; slow slightly if needed." |
| UPTALK | "Rising ending: '{word}' at {t}. Your pitch rises {p_val} st into the last word; the reference falls {b_val} st." | "In experiments, statements ending on a fall rather than a rise made the speaker sound more confident (Guyer et al. 2019; Vaughan-Johnston et al. 2024). The benefit for persuasion held only when the arguments were strong." | "Land the sentence: step down about {target} st on the last stressed syllable." |
| TEMPO_FAST / TEMPO_SLOW | "Overall tempo: your speech time is {ratio}x the reference ({p_wpm} vs {b_wpm} wpm). Tolerance: x0.71 to x1.40." | per direction, as RUSH / DRAG | "Re-record at roughly {b_wpm} wpm." |

Rules for the "why" sentence: one rubric quotation plus at most one research finding; state the kind of evidence; state the language or population when it is not English oratory; never promise an outcome.

### 6.3 Deterministic templates versus LLM generation

The brief's text: "Solution should remain reproducible across repeated runs and deployment environments" (Technical Considerations) and "Reproducibility & Code Quality (10%)". Nothing in the brief forbids an LLM; the constraint comes from this requirement and from the entrant's own choice of a light model.

| Criterion | Templates filled from the JSON | LLM at runtime (hosted API) | LLM at runtime (local, CPU) |
|---|---|---|---|
| Same input, same text | yes, byte-identical | not guaranteed. Vendor documentation: "even with `temperature` of `0.0`, the results will not be fully deterministic"; "Models released after Claude Opus 4.6 do not support setting temperature ... all other values will be rejected with a 400 error" (VS: https://platform.claude.com/docs/en/api/messages); "If you were using `temperature = 0` for determinism, note that it never guaranteed identical outputs on prior models" (VS: https://platform.claude.com/docs/en/models/opus-5-5/migration-guide). Measured: across five LLMs set to be deterministic, "none of the LLMs consistently delivers repeatable accuracy across all tasks, much less identical output strings" (Atil et al. 2024, VS abstract: https://arxiv.org/abs/2408.04667) | greedy decoding can repeat on one machine; identity across CPUs and library builds is not established (UV) |
| Numbers match measurements | by construction | must be checked; the 2026 survey names "grounding LLM outputs in acoustically verified evidence, rather than generating plausible-sounding but inaccurate feedback" as an open challenge (VS) | same |
| Works offline, in a CPU container, without keys | yes | no | yes, with a model of hundreds of MB to GB (UV) |
| Weight | a dictionary of strings | network dependency | conflicts with "as light as possible" |
| Wording variety | fixed | high | high |

Recommendation: templates at runtime. If varied wording is wanted, write several variants per template and choose one by a hash of `region_id`; the output stays reproducible.

### 6.4 What makes feedback actionable (basis for the schema and the dashboard)

| Principle | Basis | Tag | Consequence here |
|---|---|---|---|
| Feedback must show the goal, the current state relative to it, and the next step ("feed-up", "feed-back", "feed-forward"); its purpose is "to reduce discrepancies between current understandings and performance and a goal" (Sadler 1989) | Hattie & Timperley 2007 as summarised by Wisniewski, Zierer & Hattie 2020 | VS: `sources/wisniewski_2020_fpsyg_03087.txt`; https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full | baseline value = goal; participant value and delta = current state; fix with numeric target = next step |
| "Feedback is more effective the more information it contains"; learners benefit when it helps them "not only to understand what mistakes they made, but also why they made these mistakes and what they can do to avoid them the next time" | meta-analysis, 435 studies, d = 0.48 | VS, same file | what / how much / why / fix in every item |
| Over one third of feedback interventions lowered performance; effectiveness "decreases as attention moves up the hierarchy closer to the self and away from the task" | Kluger & DeNisi 1996 (607 effect sizes, d = .41) | VS (abstract), doi:10.1037/0033-2909.119.2.254 | describe the delivery, never the person; no praise lines |
| "Focus feedback on the task, not the learner"; "Be specific and clear"; "Present elaborated feedback in manageable units"; "Keep feedback as simple as possible but no simpler"; "Do not give normative comparisons"; "Be cautious about providing overall grades"; "Use praise sparingly, if at all"; "Do not limit the mode of feedback presentation to text"; "Minimize use of extensive error analyses" | Shute 2007/2008, Tables 2-3 | VS: `sources/shute_2007_RR-07-11.txt` l.1124-1221; https://myweb.fsu.edu/vshute/pdf/shute%202007_f.pdf | show the top 3 regions by points lost first, the rest collapsed; pair the score with "score if fixed"; offer A/B audio of the region next to the text; keep z and thresholds in an expandable "math" line |
| Sparse beats continuous: speakers were "significantly more pleased (p < 0.05) with their speech while using the sparse feedback strategy over the continuous one" | Tanveer, Lin & Hoque 2015 (Rhema, 30 speakers) | VS (abstract), doi:10.1145/2678025.2701386 | same cap on items |
| Explanations people accept are contrastive ("why event P happened instead of some event Q") and selected ("one or two causes"); "referring to probabilities or statistical relationships in explanation is not as effective as referring to causes" | Miller 2019 | VS: `sources/miller_2019_1706.07269.txt` l.275-289; https://arxiv.org/abs/1706.07269 | the reference rendition is the foil; one primary dimension per region; physical units first, z second |
| Explanations should tell the person "what would need to change in order to receive a desired result" | Wachter, Mittelstadt & Russell 2017 | VS (abstract), https://arxiv.org/abs/1711.00399 | `overall_if_fixed` |
| Short exemplars (< 12 s) and a re-record loop | Liang et al. 2026 survey | VS | region clips; re-upload and compare |

The exact wording of Sadler's three conditions and of Nicol & Macfarlane-Dick's seven principles was not fetched (publisher pages blocked); only the paraphrase above is verified.

---

## 7. Q6 - "Causal": what can be claimed

Pearl's hierarchy has three levels, "1. Association, 2. Intervention, and 3. Counterfactual", and "questions at level i can only be answered if information from level i or higher is available" (VS: `sources/pearl_2019_r481.txt`; Commun. ACM 62(3) 54-60).

| Claim | Level | Honest? | Basis | Wording to use |
|---|---|---|---|---|
| "Between 12.40 and 24.10 s your pitch range was 2.1 st; the reference's was 7.4 st." | measurement | yes | deterministic feature extraction | state it plainly, with units |
| "This region accounts for 4.7 of the 12.8 points lost." / "If this passage matched the reference, the score would be 91.9." | counterfactual about the scoring function | yes, exactly | the score is a known closed-form function; the counterfactual is computed, not estimated | "accounts for", "would be" |
| "The system located the injected flaw and identified its type." | intervention, on DSP pairs only | yes | each flawed file is the baseline plus one known edit in a known span, all else equal; this is a do-operation on one acoustic parameter | report as detection accuracy against the edit log |
| "This deviation makes listeners find you less confident / less persuasive." | causal claim about listeners | no. The system has no listener in the loop | prior studies only; some are experimental (resynthesis: Strangert & Gustafson 2008; Guyer et al. 2019; Vaughan-Johnston et al. 2024; Hahn 2004; Miller et al. 1976), many are correlational with r of .1-.6 (Biadsy et al. 2008; Rosenberg & Hirschberg 2005; Chen et al. 2016), in specific languages and genres, with reversals at extremes (Niebuhr et al. 2019) | "In a listening experiment, ... (citation)"; "is associated with ..."; name the population |
| "A judge would deduct points here." | prediction of human scoring | no | no judge scores in the dataset; expert raters agree exactly on vocal expression only 30 % of the time | do not say it. Say: "ballots list this as a fault: '...'" |
| "You rushed because you were nervous." | cause inside the speaker | no | not observable | never |
| "This is wrong." | normative | no | the events reject a single correct delivery (NSDA) | "differs from the reference rendition by ..." |
| Attribution to one parameter for TTS or other-speaker uploads | - | only as measurement and score attribution | many things differ at once; nothing is held equal | no "the cause is"; list the deviations |

Phrasing rules for the documentation and the UI:

1. Define the term once: "causal explanation" in this system means the measured acoustic deviation that produces a flag and a score deduction under the published rubric function, together with the exact counterfactual score.
2. Keep three vocabularies apart: measured ("is", "was"), computed ("accounts for", "would score"), cited ("in a study of ..., listeners ...").
3. State the reference: every delta is "relative to the reference rendition of the same text", every z is "relative to the typical difference between two readers of the same text".
4. State the validation scope: temporal accuracy and flaw-type recovery are measured on DSP edits with known spans; no perceptual validation was run. The reference-based evaluation paper of 2026 words the same limit: such outputs are "behavioral plausibility checks" that "do not yet map deviations to perceptual thresholds" (VS: Hallur et al. 2026).

---

## 8. Disagreements with the preliminary direction

1. **Word-by-word comparison is too fine as the scoring unit.** Use 5-word windows for continuous features and events (pause boundaries, landmark words, sentence ends) for the rest; keep single words for display. The baseline must not be treated as the single correct read: the 2026 survey lists "over-constraining style when exemplars are treated as a single correct read" as a known limitation, and NSDA says Declamation is "not designed for students to mimic the original author".
2. **A deviation needs two thresholds, not one.** A purely statistical threshold against the null is either too strict (null from DSP copies of one speaker) or uninterpretable. Use max(z_hi x reader-to-reader scale, sourced perceptual floor).
3. **Normalise location only, and add a global term.** Per-speaker z-scoring hides a participant who is flat or fast throughout; no normalisation flags every different speaker. Centre each recording on its own median in log-like units, compare local patterns, and check the medians once with a wide band.
4. **TTS renditions are not the "good different speaker".** They are a neutral synthetic reading and belong in the stress test. The good-vs-good null should come from real same-text recordings (15 public-domain LibriVox readers of the Gettysburg Address were located) plus pitch/formant/gain transforms as an exact-invariance check.
5. **The tiny learned model is not needed for scoring or for flaw typing.** The score is a closed-form deduction; the flaw type follows from dimension, sign and transcript context. A learned regressor on severity levels fits the designer's own DSP parameter and can latch onto vocoder artefacts. If a learned part is kept for a multi-feature dimension (D6), constrain it: `IsotonicRegression` or `HistGradientBoostingRegressor(monotonic_cst=...)`; `LogisticRegression` in scikit-learn 1.9.1 has no non-negativity option (VS, Section 10).
6. **Templates should lead with physical units and a counterfactual, not with z.** "5.3 st narrower than the reference" and "score would be 91.9 if fixed" first; z and threshold in a secondary line (Miller 2019).

Agreement: text-anchored comparison, a null-based robust statistic with hysteresis, deterministic templates with no LLM at runtime.

---

## 9. Recommendation

Build a reference-relative rubric of seven dimensions (Pace, Pauses, Pitch variation, Emphasis, Volume, Clarity, Endings), one per injected flaw type. Compute every feature in ln-seconds, semitones or dB, subtract each recording's own median, and compare local patterns over 5-word windows or at events; add one global check for tempo, pitch range and clarity. Standardise each deviation by s_k = max(reader-to-reader robust scale, perceptual floor / z_hi) with floors of 15 % tempo, 3 st, 3 dB and 0.2 s. Score by linear capped deduction: severity rises linearly from z_lo = 1.75 to saturation, region mass = severity x baseline-time share, S_k = 100 max(0, 1 - P_k / Pmax_k), overall = equal-weight mean. Set the few constants from the null pairs and one anchor file per dimension. Emit one JSON object per region with where / what / how much / why / fix plus exact points lost and score-if-fixed, and render it with fixed templates whose "why" line quotes a ballot and at most one study with its evidence type. Describe the output as a causal explanation of the score, validated against injected edits, and cite the listening literature for listener impact rather than claiming it.

---

## 10. Verified by running

No Kaggle kernel was pushed (topic needed no compute). Everything below ran locally, single-threaded, standard library or `curl` / `pdftotext` only.

| What | Where | Command | Observed |
|---|---|---|---|
| Derived statistics and scoring golden vector | local, `/usr/bin/python3`, < 1 s | `/usr/bin/python3 derived_numbers.py > derived_numbers.out` | exit 0. Reagan excerpt: 74 words, 23.74 s, 187.0 wpm, 12 gaps >= 0.2 s (median 0.54 s), pause ratio 0.320. TED-LIUM 3: 180.7 / 151.2 / 213.6 wpm. LibriVox: 15 durations, SD ln 0.169, 1 reader outside [0.70, 1.40]. Scoring: overall 87.19, attributions sum to the loss, monotone and bounded self-check passed |
| Abstract retrieval | local, stdlib `urllib` | `/usr/bin/python3 fetch_abstracts.py key=DOI ...` | `sources/openalex_abstracts.json` (abstracts for Van Zant & Berger, Kluger & DeNisi, Hattie & Timperley, Shute, Nicol & Macfarlane-Dick, Hahn, Duez, Guyer et al., Vaughan-Johnston et al., Tanveer et al.; none for Quene, Wingrove, Sadler, Hincks, Foulke & Sticht) |
| PyPI metadata (not an install test) | local, `curl` PyPI JSON API | - | scikit-learn 1.9.1 (requires Python >= 3.11, wheels cp311-cp315 manylinux x86_64), scipy 1.18.1 (>= 3.12), numpy 2.5.3 (>= 3.12); files `sources/pypi_*.json` |
| scikit-learn API (documentation, not executed) | WebFetch of scikit-learn 1.9.1 docs | - | `IsotonicRegression(*, y_min=None, y_max=None, increasing=True, out_of_bounds='nan')`; `HistGradientBoostingRegressor(..., monotonic_cst=None, ...)` with 1 / 0 / -1; `LogisticRegression(penalty='deprecated', *, C=1.0, l1_ratio=0.0, ...)` has no `positive` parameter |
| F0 statistics of the project baselines | sibling features probe, previous local run (not re-run) | - | `../features/out_f0_run1.md`: Reagan median 102.5 Hz, p05-p95 78.0-128.1 Hz; JFK 213.9 Hz, 174.5-265.8 Hz (Praat autocorrelation) |

Working install: n/a. No package was installed by this run or by the previous run on this topic.

---

## 11. Risks

1. **Null set mismatch.** LibriVox volunteers are fluent readers, not champion orators, and the text differs from the hackathon baselines. Their reader-to-reader scale may be too wide (hiding mild flaws) or too narrow. Mitigation: perceptual floors bound it from below; report sensitivity per severity level.
2. **Mild levels of the DSP gradient may score 100** under a speaker-agnostic tolerance. That is correct for "almost perfect" but weakens a per-level sensitivity table. Report detection separately for "same speaker as baseline" and "different speaker" conditions.
3. **Alignment-derived pauses are biased.** In the probe excerpt CTC gaps imply an articulation rate of 275 wpm. Pause thresholds (0.2 s, 0.5 s) refer to acoustic silence; take silence from an energy criterion inside the gap.
4. **Short words and unvoiced stretches** give unreliable F0 and duration. Mark units unscorable rather than flawed, and renormalise weights.
5. **Clarity (D6) has no perceptual anchor** and its recipe (spectral smoothing) may be detected through artefacts rather than articulation. It is the dimension most in need of a probe on Kaggle.
6. **Step at detection.** With hysteresis a region contributes nothing until its peak reaches z_hi, then a finite amount. Two near-identical uploads can differ by a few points. Quantising z reduces cross-machine flips but not this step.
7. **Cited effects are small, partly non-English (Swedish, French, Dutch) and non-monotone.** A "why" sentence that overstates them would be the least defensible part of the submission.
8. **Unverified numbers**: TED 169 wpm vs lectures 145 wpm (Wingrove 2017), 275 wpm comprehension limit (Foulke & Sticht 1969), Liberman & Pierrehumbert's final-lowering magnitudes, the 1.16 / sqrt(n) rule. None is used as a constant.
9. **Design choices without a source**: level bands (90/75/50/25), Pmax defaults (0.40/0.50), global mass weight 0.25, equal dimension weights, factor-2 pause floor, null acceptance targets (95/85). They are labelled as such and exposed in the config.
10. **Scores can demotivate.** Shute advises caution with overall grades; the brief requires a score. Showing "score if fixed" next to the score is the mitigation.

---

## 12. Sources

Rubrics and ballots

- NSDA sample ballots, all speech events: https://www.speechanddebate.org/wp-content/uploads/Sample-Ballot-All-Speech-Events-Blank.pdf
- NSDA How to Judge Declamation: https://www.speechanddebate.org/how-to-judge-declamation/
- NSDA How to Judge Prose: https://www.speechanddebate.org/how-to-judge-prose/
- NSDA How to Judge Program Oral Interpretation: https://www.speechanddebate.org/how-to-judge-program-oral-interpretation/
- NSDA Declamation Starter Kit: https://www.speechanddebate.org/wp-content/uploads/Declamation-Starter-Kit.pdf
- NSDA High School Unified Manual 2024-25: https://s3.amazonaws.com/tabroom-files/tourns/34243/postings/59702/HighSchoolUnifiedManual202425.pdf
- Judging Original Oratory, ballot instructions (North Carolina affiliate): http://www.ncspeechanddebate.org/uploads/5/4/1/3/54138439/judging_original_oratory.pdf
- UIL criteria for evaluating informative / persuasive speakers: https://www.uiltexas.org/speech/extemp/criteria-for-evaluating-informative-speakers , https://www.uiltexas.org/speech/extemp/criteria-for-evaluating-persuasive-speakers
- Toastmasters International Speech Contest Judge's Guide and Ballot, Item 1172 (Rev. 05/2024): https://content.toastmasters.org/image/upload/1172-international-speech-contest-ballot-ff.pdf ; Rev. 3/2011 copy: https://toastmastersd17.org/wp-content/uploads/1172-IntlSpchContBallot.pdf
- Joe, Kitchen, Chen & Feng (2015), ETS RR-15-36, reproducing the Public Speaking Competence Rubric of Schreiber, Paul & Shibley (2012): https://files.eric.ed.gov/fulltext/EJ1109251.pdf
- Morreale, Moore, Surges-Tatum & Webster (2007), The Competent Speaker Speech Evaluation Form, 2nd ed., NCA: https://www.une.edu/sites/default/files/Public-Speaking2013.pdf
- AAC&U Oral Communication VALUE rubric: https://www.aacu.org/initiatives/value-initiative/value-rubrics/value-rubrics-oral-communication ; copy used: https://us.utah.edu/_resources/documents/general-education/rubrics/Oral%20Communication%20Value%20Rubric.pdf
- Poetry Out Loud Judge's Guide 2021-22: https://vca.virginia.gov/wp-content/uploads/2022/12/POL-Judge_s-Guide-2021-22-1.pdf
- Colorado 4-H (Arapahoe County) 2022 Speech, Demonstration and Interpretive Reading guidelines: https://arapahoe.extension.colostate.edu/wp-content/uploads/sites/10/2021/11/2022-speech-demo-interpretive-reading-guidelines.doc.pdf
- Chen, Feng, Leong et al. (2016), Designing an automated assessment of public speaking skills using multimodal cues, J. Learning Analytics 3(2): https://files.eric.ed.gov/fulltext/EJ1126866.pdf

Acoustic norms and perception

- Quene (2007), On the just noticeable difference for tempo in speech, J. Phonetics 35(3) 353-362, preprint: https://hugoquene.nl/onderzoek/q.jphon.20060912.pdf
- 't Hart (1981), Differential sensitivity to pitch distance, JASA 69(3) 811-821: https://pubmed.ncbi.nlm.nih.gov/7240562/
- Caswell-Midwinter & Whitmer (2019), Discrimination of gain increments in speech-shaped noises, Trends in Hearing: https://doi.org/10.1177/2331216518820220
- Campione & Veronis (2002), A large-scale multilingual study of silent pause duration: https://www.isca-archive.org/speechprosody_2002/campione02_speechprosody.pdf
- Duez (1982), Silent and non-silent pauses in three speech styles, Language and Speech 25(1): https://doi.org/10.1177/002383098202500102
- Strangert (2005), Prosody in public speech: https://www.isca-archive.org/interspeech_2005/strangert05_interspeech.pdf
- Strangert & Gustafson (2008), What makes a good speaker?: https://www.isca-archive.org/interspeech_2008/strangert08_interspeech.pdf
- Rosenberg & Hirschberg (2005), Acoustic/prosodic and lexical correlates of charismatic speech: https://www.isca-archive.org/interspeech_2005/rosenberg05_interspeech.pdf
- Biadsy, Rosenberg, Carlson, Hirschberg & Strangert (2008): https://www.isca-archive.org/speechprosody_2008/biadsy08_speechprosody.pdf
- Tsai (2015), Are you TED talk material?: https://www.isca-archive.org/interspeech_2015/tsai15b_interspeech.pdf
- Hincks & Edlund (2009), Promoting increased pitch variation in oral presentations with transient visual feedback, LLT 13(3): https://www.lltjournal.org/item/10125-44190/
- Skarnitzl & Hledikova (2022), Front. Psychol.: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.857647/full
- Niebuhr, Tegtmeier & Schweisfurth (2019), Front. Commun.: https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2019.00012/full
- Fischer et al. (2021), Front. Robot. AI (Table 1, Jobs / Zuckerberg values): https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2021.680509/full
- Hernandez et al. (2018), TED-LIUM 3: https://arxiv.org/abs/1805.04699
- Hallur et al. (2026), Reference-based prosody and rhythm evaluation for spoken dialogue systems: https://arxiv.org/abs/2606.31055
- Liang, Li, Rackauckas & Hirschberg (2026), A survey of automated presentation coaching: https://arxiv.org/abs/2606.27380
- Yuan & Liberman (2010), F0 declination in English and Mandarin broadcast news speech: https://www.isca-archive.org/interspeech_2010/yuan10_interspeech.pdf
- Vaughan-Johnston, Guyer, Fabrigar, Lamprinakos & Brinol, Falling vocal intonation signals speaker confidence and conditionally boosts persuasion, PSPB 52(1) 3-21: https://doi.org/10.1177/01461672241262180 (full text via https://pmc.ncbi.nlm.nih.gov/articles/PMC12681368/)
- Guyer, Fabrigar & Vaughan-Johnston (2019), PSPB 45(3) 389-405: https://doi.org/10.1177/0146167218787805
- Van Zant & Berger (2020), How the voice persuades, JPSP 118(4) 661-682: https://doi.org/10.1037/pspi0000193
- Miller, Maruyama, Beaber & Valone (1976), Speed of speech and persuasion: https://experts.umn.edu/en/publications/speed-of-speech-and-persuasion
- Hahn (2004), Primary stress and intelligibility, TESOL Quarterly 38(2): https://doi.org/10.2307/3588378
- Tannander & Edlund (2021), Methods of slowing down speech: https://www.isca-archive.org/ssw_2021/tannander21_ssw.pdf
- Cardillo et al. (2018), Front. Psychol. (cites Tauroza & Allison 1990): https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2018.02308/full
- Tauroza & Allison (1990), Speech rates in British English (abstract only): https://academic.oup.com/applij/article-abstract/11/1/90/183388
- Wang et al. (2020), VoiceCoach: https://arxiv.org/abs/2001.07876
- LibriVox, The Gettysburg Address 150th Anniversary (15 readers, public domain): https://archive.org/details/gettysburgaddress_150anniv_1311_librivox
- Not fetched (cited as UV): Wingrove (2017) https://www.sciencedirect.com/science/article/abs/pii/S1475158517301029 ; Foulke & Sticht (1969) https://doi.org/10.1037/h0027575

Feedback, explanation, causality, reproducibility

- Wisniewski, Zierer & Hattie (2020), The power of feedback revisited: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full
- Hattie & Timperley (2007), The power of feedback, RER 77(1): https://doi.org/10.3102/003465430298487
- Shute (2007), Focus on formative feedback, ETS RR-07-11: https://myweb.fsu.edu/vshute/pdf/shute%202007_f.pdf (journal version RER 78(1), https://doi.org/10.3102/0034654307313795)
- Kluger & DeNisi (1996), Psychological Bulletin 119(2): https://doi.org/10.1037/0033-2909.119.2.254
- Nicol & Macfarlane-Dick (2006), Studies in Higher Education 31(2): https://doi.org/10.1080/03075070600572090
- Tanveer, Lin & Hoque (2015), Rhema: https://doi.org/10.1145/2678025.2701386
- Miller (2019), Explanation in artificial intelligence: https://arxiv.org/abs/1706.07269
- Wachter, Mittelstadt & Russell (2017), Counterfactual explanations without opening the black box: https://arxiv.org/abs/1711.00399
- Lundberg & Lee (2017), A unified approach to interpreting model predictions: https://arxiv.org/abs/1705.07874
- Pearl (2019), The seven tools of causal inference, CACM 62(3): https://ftp.cs.ucla.edu/pub/stat_ser/r481.pdf
- Geirhos et al. (2020), Shortcut learning in deep neural networks: https://arxiv.org/abs/2004.07780
- Atil et al. (2024), Non-determinism of "deterministic" LLM settings: https://arxiv.org/abs/2408.04667
- Claude API reference, Messages (`temperature`): https://platform.claude.com/docs/en/api/messages
- Migrating to Claude Opus 5.5 (sampling parameters): https://platform.claude.com/docs/en/models/opus-5-5/migration-guide
- NIST/SEMATECH e-Handbook, Detection of outliers (modified Z-score): https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm
- scikit-learn 1.9.1 documentation: https://scikit-learn.org/stable/modules/generated/sklearn.isotonic.IsotonicRegression.html , https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html , https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
- PyPI JSON API: https://pypi.org/pypi/scikit-learn/json , https://pypi.org/pypi/scipy/json , https://pypi.org/pypi/numpy/json

Files produced by this topic (all under the `rubric_explain/` directory): `REPORT.md`, `derived_numbers.py`, `derived_numbers.out`, `fetch_abstracts.py`, `PREVIOUS_RUN_condensed.md`, `sources/` (PDF, text, JSON and XML of every fetched source).
