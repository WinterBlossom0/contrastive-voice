# Public-domain baselines and human parallel recordings

Research completed 2026-10-01. Deliverable: [sources_manifest.json](sources_manifest.json), with 58 ranked records, nine recommended original-delivery baselines, human calibration recommendations, and seven collection audits. No speech passage is selected or transcribed here; the build must select shared spoken words algorithmically.

Evidence labels throughout: **VERIFIED_BY_RUNNING** cites an output file; **VERIFIED_BY_SOURCE** cites a fetched primary page or saved source metadata; **UNVERIFIED** identifies a remaining uncertainty. Recommendations are engineering choices, not measured results.

## Recommendation and limits

Use nine original recordings, one speaker per baseline: four women and five men, 1961–2021. Use six Gettysburg readers for natural between-reader calibration and three other readers for a separate check. Add the verified Reagan/John Greenman parallel recording as a second text stratum. JFK/mkirkpat is a useful development comparison with a different original channel. Keep measurement repeatability, human variation, and synthetic perturbation effects separate.

The requested human recordings exist and are useful. All 15 Gettysburg anniversary files and four presidential farewell readings downloaded fully from Kaggle. JFK and Reagan have source-checked, automatically matched spoken-word runs. The six State of the Union collections exist, but their annual messages do **not** match the original-delivery candidates; shared president identity is insufficient. **VERIFIED_BY_RUNNING:** `kaggle_out/v2/verification_v2.json`, `kaggle_out/v3/human_text_diagnostic.json`, `kaggle_out/v4/human_text_diagnostic.json`, `local_out/human_text_source_check.json`, `local_out/reagan_text_source_check.json`.

Prominent speeches are curated reference performances, not validated “perfect” delivery. Volunteer readings likewise have no human flaw/severity annotations. No selected excerpt has been manually audited for delivery quality or word accuracy. Clean excerpt suitability remains a build check, explicitly recorded in every manifest grade.

## Ranked original recordings and Kaggle access

The first nine manifest records have `recommended: true`. Exact media URLs, licence-page URLs, transcript URLs, full known SHA-256 values and the URL each hash belongs to are in the manifest. `download_url` is the tested preferred encoding; `audio_url` preserves the earlier candidate URL. A different mirror encoding requires new word timings.

| Rank | Manifest ID; speaker | Gender/year; setting | Grade | Kaggle build strategy |
|---|---|---|---|---|
| 1 | `mobama_weekly_2014`; Michelle Obama | F/2014; White House camera address | A | Direct: `obamawhitehouse.archives.gov`, full HTTP 200 in v1/v2 |
| 2 | `harris_uncsw_2021`; Kamala Harris | F/2021; prerecorded UN address | A | **Stage** verified bytes; Wikimedia 200 in v1, 429 in v2 |
| 3 | `hclinton_tomorrow_2010`; Hillary Clinton | F/2010; State Department camera address | A | **Stage**; Wikimedia full 200 after earlier 429, unreliable |
| 4 | `gwbush_911_2001`; George W. Bush | M/2001; Oval Office | A | Direct mirror: `archive.org`, MP3 full 200 in v2 |
| 5 | `obama_weekly_2009`; Barack Obama | M/2009; White House camera address | A | Direct mirror: `obamawhitehouse.archives.gov`, full 200 in v2 |
| 6 | `lbush_radio_2001`; Laura Bush | F/2001; Crawford radio address | B | **Stage**; Wikimedia full 200 in v1/v2, unreliable host |
| 7 | `reagan_farewell_1989`; Ronald Reagan | M/1989; Oval Office | B | Direct mirror: `nara-media-001.s3.amazonaws.com`, full 200 in v2/v4 |
| 8 | `eisenhower_farewell_1961`; Dwight D. Eisenhower | M/1961; televised farewell | B | **Stage** locally verified Ogg; Wikimedia 429 in Kaggle |
| 9 | `nixon_resignation_1974`; Richard Nixon | M/1974; Oval Office | B | **Stage** locally verified raw Ogg; Wikimedia 429 in Kaggle |

**VERIFIED_BY_RUNNING:** host statuses and bytes in `kaggle_out/v1/probe_results.json`, `kaggle_out/v2/verification_v2.json`, `kaggle_out/v4/verification_v4.json`; local staged-file hashes in `download_log.tsv`. Successful historical downloads do not guarantee future availability. No source staging/upload was performed in this research. Miller Center media returned 403; its transcript pages can still be useful. Do not repeatedly retry Wikimedia in the build.

The direct URLs selected for the four dependable-host recommendations are:

- [Michelle Obama government MP3](https://obamawhitehouse.archives.gov/WeeklyAddress/2014/051014-LWRFRC/051014_WeeklyAddress.mp3).
- [George W. Bush Internet Archive MP3](https://archive.org/download/GWBush_Oval_Office_Address_20010911/GWBush_Oval_Office_Address_20010911.mp3).
- [Barack Obama government MP3](https://obamawhitehouse.archives.gov/videos/2009/January/20090124_WeeklyAddress.mp3).
- [Reagan farewell NARA MP3](https://nara-media-001.s3.amazonaws.com/arcmedia/presidential-libraries/reagan/5730597/reagan-PP9011B.mp3).

**VERIFIED_BY_RUNNING:** v2/v4. These are media links, not separate licence grants; item-level licence evidence is recorded independently.

Thirteen original recording candidates have file/property evidence below, including twelve provisionally graded A/B and one historical C reserve. They are **11 distinct named speakers**, counting Nancy separately after isolating her part; repeated Reagan and Obama speeches do not enlarge the independent speaker count. This answers the ≥12 recording-candidate requirement while preserving the requested nine-source build. It does not assert twelve already-selected clean excerpts.

| Manifest ID | Native audio codec/rate/channels/bitrate | Full duration (s) | R99 (Hz) | Channel/condition; grade |
|---|---|---:|---:|---|
| `mobama_weekly_2014` | mp3; 44100 Hz; 2 ch; 128 kb/s | 305.894 | 4141 | Modern camera/room; check channels; A |
| `harris_uncsw_2021` | vorbis; 44100 Hz; 2 ch; unknown kb/s | 337.336 | — | Modern camera/room; check channels; A |
| `hclinton_tomorrow_2010` | vorbis; 44100 Hz; 2 ch; 80 kb/s | 154.329 | 7062 | Modern camera/room; check channels; A |
| `gwbush_911_2001` | mp3; 44100 Hz; 2 ch; 128 kb/s | 262.087 | 5594 | Modern camera/room; check channels; A |
| `obama_weekly_2009` | mp3; 44100 Hz; 2 ch; 320 kb/s | 290.090 | 2344 | Modern camera/room; check channels; A |
| `lbush_radio_2001` | vorbis; 44100 Hz; 2 ch; 80 kb/s | 231.184 | 1953 | Prefer left; radio; B |
| `reagan_farewell_1989` | mp3; 44100 Hz; 2 ch; 256 kb/s | 1279.142 | 1062 | Left; archival; B |
| `eisenhower_farewell_1961` | vorbis; 44100 Hz; 2 ch; 160 kb/s | 930.267 | — | Stereo; archival; B |
| `nixon_resignation_1974` | vorbis; 44100 Hz; 1 ch; 96 kb/s | 922.096 | — | Mono; hum/raw transfer; B |
| `reagan_challenger_1986` | mp3; 44100 Hz; 2 ch; 256 kb/s | 255.510 | 1531 | Left; development; B |
| `obama_binladen_2011` | vorbis; 44100 Hz; 2 ch; 112 kb/s | 567.519 | — | Modern camera/room; check channels; A |
| `nreagan_drugabuse_1986` | mp3; 44100 Hz; 2 ch; 256 kb/s | 1136.069 | 1406 | Left; isolate Nancy; B |
| `fdr_fireside1_1933` | mp3; 44100 Hz; 1 ch; 128 kb/s | 782.404 | 2625 | Mono; 1933 radio; C |

**VERIFIED_BY_RUNNING:** properties from v2, Harris v1, and `local_out/audio_properties.json`. Rates are audio-stream rates, not video container bitrates; Harris audio bitrate is unknown. R99 is the frequency containing 99% of decoded energy, measured on the first 90 seconds at 16 kHz; it is **not** an independently verified effective speech bandwidth. “—” means unmeasured, not zero. Full source duration includes slates/silence.

Grade A: modern studio/camera address, provisionally useful. B: archival bandwidth/channel issues or variable volunteer channel. C: historical/crowd source for reserve/stress testing. U: audio unmeasured. Grades describe recording suitability, not rhetorical merit. AOC’s local file size differs from catalogue size; completeness is **UNVERIFIED**. All additional candidates, variants, and their measured/unmeasured status remain in the manifest.

Channel hazards are material: Reagan Challenger, Reagan farewell and the Reagan/Nancy address require the **left channel**, not a mean downmix. The farewell’s side/mid energy ratio is +21.49 dB; earlier Challenger whole-file mean downmix falls near −56.6 dBFS versus left near −32.1 dBFS. Laura’s left is about 3.8 dB louder than right. Hillary’s first-90-second recording is very quiet; gain is not a delivery flaw label. Nixon has hum/peak concerns; keep its raw transfer separate from the de-buzzed alternate. **VERIFIED_BY_RUNNING:** v2/v4; `local_out/volumedetect_local.tsv`.

## Human same-text recordings: I-03 and J-04

### Gettysburg Address, 150th anniversary

**VERIFIED_BY_SOURCE:** [LibriVox anniversary item](https://archive.org/details/gettysburgaddress_150anniv_1311_librivox), saved `meta/librivox_api_gettysburg.json` (book 8387) and IA metadata. Fifteen distinct catalogued human readers recorded the same 1863 text in 2013. The source edition is [Gutenberg 4](https://www.gutenberg.org/ebooks/4), fetched to `transcripts/gettysburg_gutenberg.txt`. Names/reader IDs establish catalogued readers; gender stays null rather than being inferred.

**VERIFIED_BY_RUNNING:** all 15 files full HTTP 200 from `archive.org` in v2; all are 44.1 kHz, mono, MP3, 128 kb/s. Each exact direct URL and full-file hash is in the manifest. The common URL stem is `https://archive.org/download/gettysburgaddress_150anniv_1311_librivox/`; filenames follow `gettysburgaddress_lincoln_CODE_128kb.mp3`.

| Code / manifest suffix | Reader | Full duration (s) | Proposed use |
|---|---|---:|---|
| `amb` | Ann Boulais | 124.552 | calibration |
| `dj` | Drew Johnson | 115.487 | test |
| `dl` | David Lawrence | 139.076 | calibration |
| `eep` | Ernst Pattynama | 171.050 | reserve |
| `fb` | Frances Brown | 130.638 | calibration |
| `jn` | Julia Niedermaier | 124.238 | calibration |
| `law` | Laurie Anne Walden | 116.767 | reserve |
| `lb` | Lucretia B. | 168.255 | reserve |
| `mas` | MaryAnn | 214.753 | reserve |
| `mk` | Maria Kasper | 134.844 | reserve |
| `pc` | Phil Chenevert | 137.404 | calibration |
| `rk` | Ray Kasper (1938-2017) | 143.151 | reserve |
| `sa` | Sue Anderson | 157.048 | test |
| `tg` | TriciaG | 122.201 | test |
| `wt` | Winston Tharp | 150.674 | calibration |

Durations are measured full-file durations, not speech-only durations. First-90-second measurements include introductions; they cannot select the final comparison region. Algorithmically exclude LibriVox boilerplate, locate shared words, and check omissions/substitutions before forced alignment. Human variation includes recording room/microphone, accent, phrasing and performance; this collection cannot identify an isolated effect of speaker identity.

Use `amb, dl, fb, jn, pc, wt` for calibration: six recordings yield 15 unordered pairs, but only six independent reader units. Keep `dj, sa, tg` for a held-out reader check; remaining six are reserves. These selections are reproducible diversity/availability choices, not optimal-reader claims. At 30 seconds per reader, calibration audio is three minutes. Match a common token span; if readers differ in pace, accept 20–40 seconds per rendering rather than time-stretching them to an artificial identical length.

### Original presidential delivery versus human re-reading

| LibriVox record | Human reader/recording year | Original candidate | Verification level |
|---|---|---|---|
| `lv_farewell_truman`, chapter 41 | John Greenman/2015 | `truman_farewell_1953` | Full audio downloaded; catalogue title match; exact spoken-token pairing **UNVERIFIED** |
| `lv_farewell_eisenhower`, chapter 42 | John Greenman/2015 | `eisenhower_farewell_1961` | Full audio downloaded; catalogue title match; exact spoken-token pairing **UNVERIFIED** |
| `lv_farewell_nixon`, chapter 45 | John Greenman/2015 | `nixon_resignation_1974` | Full audio downloaded; catalogue title match; exact spoken-token pairing **UNVERIFIED** |
| `lv_farewell_reagan`, chapter 48 | John Greenman/2015 | `reagan_farewell_1989` | Full audio downloaded; three-way source/ASR token match verified |
| `lv_jfk_inaugural_mkirkpat`, section 07 | mkirkpat/2025 | `ALT_jfk_inaugural_1961` | Full reading downloaded; three-way source/ASR token match verified |

**VERIFIED_BY_SOURCE:** [Presidential Farewell and Last Addresses catalogue](https://librivox.org/presidential-farewell-and-last-addresses-by-various/), saved `meta/ia_presidential_farewell_last_addresses_jg_1504_librivox.json`; [Short Nonfiction 106](https://librivox.org/short-nonfiction-collection-vol-106-by-various/), saved `meta/ia_snf106_2508_librivox.json`. The former’s IA item has a public-domain mark; the latter catalogue explicitly states public domain in the USA and links JFK’s text to [Gutenberg 925](https://www.gutenberg.org/ebooks/925).

**VERIFIED_BY_RUNNING:** farewell files are mono 44.1 kHz MP3, 128 kb/s, measured durations 1657.104, 1010.207, 872.124 and 1485.192 seconds respectively in v2; JFK reading is mono 44.1 kHz MP3, 128 kb/s, 597.995 seconds in v3. All five use Kaggle-reachable `archive.org`; originals may need staging as indicated above. John Greenman is **one** narrator across four texts, not four independent voices.

For JFK, the longest identical original/reader ASR run has 49 normalized tokens, lasting 31.02 seconds in the original and 21.32 seconds in the reading. This same sequence occurs once in the fetched Gutenberg source. For Reagan, the longest ASR agreement is 240 tokens, but that entire run does not exactly match the official transcript; a nested 237-token run does, lasting 78.14 and 91.42 seconds. These are automatic identity diagnostics, **not build passage selections**. No speech text is reproduced in the reports or manifest.

**VERIFIED_BY_RUNNING:** `kaggle_out/v3/human_text_diagnostic.json`, `local_out/human_text_source_check.json`, `kaggle_out/v4/human_text_diagnostic.json`, `local_out/reagan_text_source_check.json`; official Reagan text is saved in `transcripts/reagan_farewell_1989.txt`. ASR agreement does not prove human-rated good delivery, accurate word boundaries, or error-free transcription. The JFK source checked here is the pre-existing staged original, not a newly demonstrated Kaggle Commons download.

### State of the Union and other inaugural audit

**VERIFIED_BY_SOURCE:** saved IA metadata and catalogues; **VERIFIED_BY_RUNNING:** nine 65,536-byte range probes returned HTTP 206 in v2. Range success establishes access, not full-file integrity, quality or a hash.

| IA collection | Chapters | Relationship to existing originals |
|---|---:|---|
| [Truman 1946–1953](https://archive.org/details/sotu_19461953_2305_librivox) | 12 | Annual messages, including split written texts; not his farewell |
| [1953–1963](https://archive.org/details/sotu_19531963_2302_librivox) | 12 | Eisenhower/JFK annual messages; not farewell, test-ban, Cuba or inaugural |
| [Johnson 1964–1969](https://archive.org/details/state_union_addresses_lbj_2305_librivox) | 6 | No matching Johnson original in candidate list |
| [Nixon 1970–1974](https://archive.org/details/state_union_addresses_rmn_2306_librivox) | 5 | Annual/written messages; not resignation |
| [Ford 1975–1977](https://archive.org/details/sotu19751977_2401_librivox) | 3 | No matching Ford original; KevinS reads these chapters |
| [Carter 1978–1981](https://archive.org/details/stateunionaddressescarter_2404_librivox) | 9 | Annual/written messages; not Afghanistan address |

Carter’s catalogued January 21, 1980 written message must not be silently paired with the January 23 oral delivery. Several annual messages are written texts without equivalent original delivery. Some IA records lack `licenseurl`; the manifest does not invent one. Their catalogue policy supplies USA public-domain evidence, with item/text provenance still necessary.

[Short Nonfiction 096](https://librivox.org/short-nonfiction-collection-vol-096-by-various/) has Maurice Donegan’s human readings of Carter’s 1977 and Reagan’s 1981/1985 inaugurals. These three files passed range access checks, but none of those original inaugurals is in the existing candidate list. A Bush inaugural in volume 097 likewise does not match his Gulf War address. JFK’s volume 106 reading supplies the actual inaugural match. Do not substitute a same-president, different-text reading. `collection_checks` records the six SOTU audits and volume 096 filenames; the extra volume 097 evidence remains in `meta/ia_snf097_2305_librivox.json`.

## Existing datasets and the novelty claim

The blanket statement that no same-text comparison dataset exists is false. No exact, openly reusable dataset covering this project’s complete time-localized, graded rhetorical-flaw ladder was found in the sources searched. That narrower conclusion is a search result, not proof of nonexistence.

| Dataset / primary source | Useful supervision or design | Same-text deliberately flawed rhetoric? | Licence/access facts |
|---|---|---|---|
| [speechocean762](https://www.openslr.org/101/) | 5,000 English utterances from Mandarin L2 speakers; five expert assessors; pronunciation/fluency labels | No complete rhetorical flaw ladder | CC BY 4.0; downloadable |
| [L2-ARCTIC](https://psi.engr.tamu.edu/l2-arctic-corpus/) | 24 readers, balanced recorded genders, six L1 groups; shared prompts and phone/error alignment | Same prompts, naturally varying L2 speech; no intentional rhetoric gradient | CC BY-NC 4.0; access request; not fetched here |
| [TED-LIUM 3 paper](https://arxiv.org/abs/1805.04699), [dataset catalogue](https://www.tensorflow.org/datasets/catalog/tedlium) | 452 hours/2,351 talks; ASR/transcripts | No | Audio CC BY-NC-ND 3.0 in catalogue; OpenSLR 51 currently returned Resource Not Found |
| [TED rating prediction paper](https://arxiv.org/abs/1906.03940) | 2,200 talks, 14 audience tags; holistic reactions | No; topic/popularity/visual confounding | Underlying TED policy; paper/code licence does not grant media rights |
| [POM / official multimodal SDK](https://github.com/CMU-MultiComp-Lab/CMU-MultimodalSDK) | Opinion-video persuasion, personality and sentiment features | No matched rhetorical ladder | Media redistribution licence **UNVERIFIED**; SDK licence is separate |
| [MIT interview study](https://roc-hci.com/wp-content/uploads/tac16_job.pdf) | 138 sessions, 69 students, nine judges; communication/affect assessment | Repeated people/interviews, not controlled identical speech | Public research paper; dataset redistribution licence **UNVERIFIED** |
| [3MT French dataset](https://zenodo.org/records/7603511) | Research-presentation confidence, persuasion and engagement judgments | No controlled same-text perturbation ladder | Restricted access; redistribution licence **UNVERIFIED** |
| [Expresso](https://speechbot.github.io/expresso/), [EmphAssess](https://github.com/facebookresearch/emphassess) | Expressive reading and word emphasis; useful positive/negative controls | Controlled style/emphasis, not full rhetoric ladder | Expresso and EmphAssess data CC BY-NC 4.0; EmphAssess repo archived May 2025 |
| [ProsAudit](https://arxiv.org/abs/2302.12057) | Controlled prosodic-boundary and pause contrasts | Relevant correct/perturbed contrasts; narrower task | Paper establishes task; benchmark redistribution licence **UNVERIFIED** |
| [ParaPairAudioBench, 2026](https://github.com/jsujeon/ParaPairAudioBench), [paper](https://arxiv.org/abs/2606.24648) | 5,175 pairs; rate, emphasis, style, age, gender; A/B/Tie judgments | Explicit same-transcript rate/emphasis/style subsets; no time-localized multi-flaw severity ladder | Source-specific licences: SVC academic/noncommercial, LibriTTS CC BY 4.0, EARS/Expresso CC BY-NC 4.0; SVC access controlled |

**VERIFIED_BY_SOURCE:** linked primary dataset/paper pages fetched in this or the earlier runs. CMU ARCTIC is also a relevant studio same-prompt corpus; its current Festvox page returned 502, so current download/licence details are **UNVERIFIED** here and it is not a recommended dependency. Existing pronunciation, prosody and expressive datasets justify reusable alignment/labeling techniques, not automatic transfer of public-speaking “good/bad” labels. ParaPair’s paper licence is not a blanket licence over its constituent audio.

## Minimal size, split and calibration design

Nine baselines × nominal 30 seconds = 270 seconds before perturbations. A 20–40 second allowance balances several phrases/pauses with a small reproducible build; it is an engineering choice, not a statistically established minimum. More generated files do not increase the number of independent texts or speakers. This supports a demonstrator, ablations and deterministic feature tests; it cannot establish general human rhetorical assessment or justify fitting a large learner.

Proposed original split: train Harris, Hillary Clinton, George W. Bush, Barack Obama, Reagan; validation Laura Bush and Eisenhower; test Michelle Obama and Nixon. This is five/two/two distinct speakers and texts. Freeze after source QA and before detector tuning. Source research has inspected recordings; call this a proposed evaluation split, not an already untouched experimental test. Earlier Challenger and JFK probe material is development material; Reagan farewell must share the Reagan development/train group.

**I-05:** group every speech, subclip, DSP variant, TTS rendition and human re-reading linked to a text. Repeated original speakers also stay in one split. A new transcript is not automatically a new speaker. John Greenman readings across different texts cannot be split across calibration and test as if voices were independent. For the proposed partition, use only his Reagan reading in joint train/calibration; keep his other farewell readings as reserves. Using all four in joint calibration would connect Nixon/Eisenhower to the training group and invalidate the proposed test/validation partition. A broader comparison experiment must revise connected speaker/text splits or be reported separately, without feeding held-out text into detector calibration.

**I-03:** estimate within-recording measurement variability separately from between-reader/text variation. For a distance `d`, report the empirical human comparison distribution `D_human={d(x_i,x_j): i<j, same_text}` and each perturbation’s `d(x,T(x))`; do not pool identity and vocoder controls into a single claimed natural-human null. A descriptive median/MAD scale may be `z=(d-median(D_human))/(1.4826*MAD(D_human)+epsilon)`, with documented epsilon and zero-MAD handling chosen by the build. No thresholds or claimed confidence intervals are estimated here. Resample/report reader or speaker clusters, not dependent pair counts. Gettysburg’s one text cannot validate generalization to political broadcasts.

**J-04:** retain human-to-human comparisons as a separate evaluation stratum alongside DSP identity controls and TTS. A positive human distance is not a flaw label. Two renditions of the same words still differ in accent, context, audience and channel; use dimensions robust to these differences and report residual confounding. No human natural-flaw gold labels were created by this research.

## Licence facts

| Source category | Supported fact | Evidence |
|---|---|---|
| US-government work | Federal employee work made as part of official duties is outside US copyright protection; government possession alone is insufficient | **VERIFIED_BY_SOURCE:** [17 USC §105](https://www.copyright.gov/title17/92chap1.html#105), [NARA FAQ](https://www.archives.gov/faqs) |
| Commons public-domain tags | Item metadata identifies PD-USGov-POTUS/DOS or other basis; trace recording provenance separately from text. Chamber PD-CSPAN is not a blanket C-SPAN production licence | **VERIFIED_BY_SOURCE:** `commons_metadata_round1.jsonl`, `commons_metadata_round2.jsonl`; each exact file page in manifest |
| LibriVox | Catalogue declares recordings public domain in the USA; selected historical texts are also public domain. Do not state universal worldwide status | **VERIFIED_BY_SOURCE:** [volume 106 catalogue](https://librivox.org/short-nonfiction-collection-vol-106-by-various/), linked IA/catalogue records above |
| TED | Published usage policy uses CC BY-NC-ND and restricts alteration/remixing, including dubbing; research access is not a derivative redistribution grant | **VERIFIED_BY_SOURCE:** [TED usage policy](https://www.ted.com/about/our-organization/our-policies-terms/ted-talks-usage-policy) |
| Copyrighted famous speech | Fame/public delivery does not put the speech text or sound recording into the public domain; these are separate rights/provenance questions | **VERIFIED_BY_SOURCE:** [Copyright Act definitions and §105](https://www.copyright.gov/title17/92chap1.html) |

No ownership or policy change is requested. The public-domain dataset can be documented and distributed separately from TED-dependent work. TED sourcing remains the other research topic; its inclusion/permissions decision remains with the owner under the fixed project direction.

## Manifest, labels and documentation

`sources_manifest.json` schema 1.0 contains required `id`, `speaker`, nullable `gender`, `year`, `setting`, `audio_url`, nullable tested `mirror_url`, `sha256`, `sha256_url`, `licence_basis`, `licence_url`, `transcript_url`, `channel_note`, `quality_grade`, `rank` and `recommended`. Added fields specify role, text year, recording versus text provenance, proposed split, Kaggle strategy, measurements, and evidence. Unknown bitrate/gender/hash stays null. Collection range probes are separate from full-download source records. Rebuild this evidence manifest with `/usr/bin/python3 build_sources_manifest.py`; it uses only the standard library and chooses no passages.

The build’s **clip** manifest should additionally record source-byte hash, derived-byte hash, decoder/resampler versions, source start/end, original transcript/token hash, exact aligned token span, word alignment method, speaker/text/recording group IDs, channel extraction and gain, native and derived sample rates, source licence snapshot, parent clip ID, transform recipe/version/seed, time-warp map, and QC verdict. Do not copy file hashes or offsets between MP3/Ogg/video variants: Michelle government audio is shorter than the Commons video, and the Bush IA MP3 differs from its Ogg.

Canonical event labels should be UTF-8 JSON with `clip_id`, `dimension`, `start_s`, `end_s`, `severity_target`, `recipe_parameters`, `label_origin`, and optional annotator/agreement metadata. Use seconds in derived-audio coordinates; specify half-open intervals `[start,end)`, validate `0 <= start < end <= duration`, and support overlapping dimensions. Injection magnitude is a synthetic target, not a human severity judgment. Store the inverse time map for aligning transformed words; keep utterance-level and event-level labels distinct.

**VERIFIED_BY_SOURCE:** [Praat TextGrid formats](https://www.fon.hum.uva.nl/praat/manual/TextGrid_file_formats.html) support interval/point tiers; use one tier per dimension for overlapping dimensions. [Audacity labels](https://manual.audacityteam.org/man/importing_and_exporting_labels.html) use tab-separated start/end/text, with start=end for points. These are export views of canonical JSON, not replacements for provenance. Follow [dataset-card documentation](https://huggingface.co/docs/hub/datasets-cards) and [Datasheets for Datasets](https://arxiv.org/abs/1803.09010): motivation/composition, acquisition, preprocessing, uses/limits, licence, splits, distribution and maintenance. Explicitly document historic US-government selection bias, unknown reader demographics, recording variation, synthetic labels, and absence of natural human gold scores.

Store native downloaded media unchanged with its hash; derive 16 kHz mono audio after channel QA, use float intermediates, and distribute lossless FLAC or PCM WAV clips. Do not add an Opus/MP3 encoding step to analysis material. Existing lossy sources remain lossy; FLAC does not restore them. Keep native-rate evidence for clarity/spectral work: 16 kHz has an 8 kHz Nyquist limit and cannot characterize higher bands.

At 16 kHz/mono/16-bit, PCM uses 32,000 bytes/second: a nominal 30-second clip is 960,000 bytes; nine are 8.64 MB, and 400 are 384 MB before headers. These are arithmetic estimates, not measured FLAC sizes. Keep code/manifests/cards in Git; use release assets or an external dataset location for generated audio rather than repeatedly committing binary revisions.

**VERIFIED_BY_SOURCE, current 2026-10-01:** [GitHub file limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) warn above 50 MiB, block regular Git files above 100 MiB, and cap browser uploads at 25 MiB; repositories should ideally stay below 1 GB and are strongly recommended below 5 GB. These repository figures are recommendations, not a claimed universal 5 GB hard cap. [Git LFS billing](https://docs.github.com/en/billing/concepts/product-billing/git-lfs) currently includes 10 GiB storage and 10 GiB download bandwidth for Free/Pro/Free organizations, 250 GiB each for Team/Enterprise Cloud. Old 1 GB/data-pack claims are obsolete. Each binary revision counts as another full stored object; account allowances are shared, not a dedicated project grant.

## Verified by running: methods and reproducibility

All new DSP/ASR ran only in the authorized private Kaggle CPU kernel `electroknight/cvoice-probe-baseline-data`, internet enabled, GPU disabled, existing `electroknight/cvoice-probe-audio` attached. Exactly three further pushes were used (v2–v4). Local work was file/source reading, ffprobe and standard-library JSON/text handling; no local model or DSP stack was run.

| Output | What it establishes |
|---|---|
| `kaggle_out/v1/probe_results.json`, `summary.md` | Earlier full downloads/quality for Michelle, Laura, Hillary, Harris; whole-file loudness and limited F0; host failures |
| `local_out/audio_properties.json`, `download_log.tsv`, `volumedetect_local.tsv` | Earlier raw transfers’ codec/channel properties and known bytes/hashes; channel-cancellation hazard |
| `kaggle_out/v2/verification_v2.json` | 54 media targets: 28 full downloads with quality, nine range successes, 17 HTTP 429 failures; all 15 Gettysburg and four farewell readers verified |
| `kaggle_out/v3/verification_v3.json`, `human_text_diagnostic.json` | JFK human reading full download/hash/quality; two staged/source-recording ASRs and automatic same-token diagnostic |
| `kaggle_out/v4/verification_v4.json`, `human_text_diagnostic.json` | Reagan original and reader full downloads/hashes; left-channel original ASR and same-token diagnostic |
| `local_out/human_text_source_check.json`, `reagan_text_source_check.json` | Standard-library text checks against fetched source files; only source-matching runs claimed |

v2 used Python **3.12.13**, NumPy **2.0.2**, FFmpeg **4.4.2-0ubuntu0.22.04.1**. v3/v4 record the same versions. Earlier v1 lists SciPy **1.16.3** and faster-whisper **1.2.1**; the new ASR diagnostics explicitly installed faster-whisper **1.2.1**, model **tiny.en**, CPU **int8**, `cpu_threads=4`, `num_workers=1`, `beam_size=1`, `word_timestamps=True`, `condition_on_previous_text=False`, first **180 seconds** per recording. The model revision digest and v2–v4 SciPy version were not recorded; bit-identical future model output is **UNVERIFIED**. These are diagnostic pins, not a requirement to use tiny.en for final alignment.

New HTTP probes used descriptive UA `CvoiceDatasetResearch/0.2 (public-domain speech-source verification; low-volume sequential downloads) python-urllib`, sequential requests, 20-second response timeout, 40-second full-download budget, 650-second download-loop budget. Full download SHA-256 is over exact received bytes. Range probes request bytes 0–65535 and deliberately provide no whole-file hash. No automatic repeated 429 retries in v2.

Quality method in `meta/probe_v2.py` and current `kaggle/probe.py`: decode first 90 seconds, 16 kHz float32; select left when stereo side/mid power ratio exceeds 10 dB, otherwise mean (mono unchanged). This heuristic is source screening, not a universal polarity detector. Frame RMS uses 400 samples/25 ms with 160-sample/10 ms hop, floor power `1e-12` (−120 dBFS). Sliding surveys use 30-second windows with 5-second hop over this opening sample. Define `DR_proxy=P95(frame_dB)-P5(frame_dB)` and absolute RMS `10 log10(mean(x²))`; peak is `20 log10(max|x|)`.

| Recommended source measured in v2 | Opening RMS (dBFS) | Sample peak (dBFS) | Survey DR proxy range (dB) |
|---|---:|---:|---:|
| Michelle Obama | −27.55 | −3.62 | 30.79–33.29 |
| Hillary Clinton | −40.31 | −18.25 | 30.09–31.99 |
| George W. Bush | −18.77 | −1.33 | 37.72–38.35 |
| Barack Obama | −24.66 | −3.56 | 43.57–44.95 |
| Laura Bush | −27.45 | −6.74 | 38.84–42.32 |
| Reagan farewell, left | −20.33 | −1.91 | 35.50–39.16 |

**VERIFIED_BY_RUNNING:** v2. These are opening survey windows, not chosen dataset excerpts. Harris has earlier full-file v1 quality: −30.41 LUFS; Michelle/Laura/Hillary v1 values are −26.28/−28.19/−39.75 LUFS. v1's limited F0 analysis reports medians 184.6/196.2/160.9/182.8 Hz for Michelle/Laura/Hillary/Harris respectively; these estimator outputs establish neither a representative pitch range nor demographic identity. Eisenhower/Nixon have earlier channel/volume measurements but no new Kaggle window survey because downloads were rate-limited. All underlying numbers and caveats remain in the manifest's `quality_evidence`.

Welch LTAS uses `fs=16000`, `nperseg=1024`, `noverlap=512`. R99 is the first frequency where cumulative spectrum reaches 0.99; the second reported proxy is the highest bin within 60 dB of the spectrum peak. That latter proxy often reaches 8 kHz due to hiss/codec floor, so it is not clean-speech bandwidth. P95−P5 is **not true SNR**: pauses, fades, intros and digital silence confound it, sometimes producing very large values. Earlier v1 fields named “SNR” or “speech bandwidth” must be interpreted as their estimator definitions, not validated ground truth. RMS is not LUFS; v1 whole-file LUFS and v2 opening-window RMS are not interchangeable.

No final-excerpt bandwidth/SNR, manually checked WER, speech-only duration, human listening grade, forced-alignment error, or calibrated rhetorical threshold is claimed. Those depend on the algorithmically selected build excerpt and must be written to its QC report. The research supplies tested source bytes/hosts and methods rather than manufactured passage labels.

## Design changes, risks and owner-only questions

- **DESIGN_v0 §2.1–2.4 / I-03 / J-04:** add independent human-reader material; retain separate natural variation, measurement and synthetic-control distributions. Do not equate pooled DSP/TTS output with natural speaker variation.
- **I-05:** use nine distinct original speakers; enforce connected speaker/text groups for every child clip. Challenger/JFK are development material. Multiple Greenman chapters never become independent speaker holdouts.
- **J-04:** six SOTU collection existence claims are verified, but their claimed matches to current originals are rejected. Use actual farewell and JFK inaugural matches; three farewell passage identities still need build verification.
- **Brief novelty claim:** qualify it in light of ProsAudit and 2026 ParaPairAudioBench. Same-text prosodic comparisons already exist; the narrower combination of localized rhetorical dimensions, engineered severity and a public-domain provenance trail is the defensible scope.
- **Access:** stage five recommended Wikimedia sources and transcript files before build. Four tested direct hosts are available; no promise of perpetual access. Preserve hashes and retrieval provenance; never swap edits silently.
- **Scope:** nine short baselines are a demonstration corpus with substantial US-English/broadcast bias. The human null includes microphone/style differences and Gettysburg alone supplies one text. Results cannot establish speaker-agnostic real-world flaw accuracy without broader human evaluation.

Owner-only decisions: whether to include TED-derived artifacts under the fixed TED direction and any required permission, and whether to fund/collect human rhetorical ratings for a claim beyond synthetic recovery. Neither blocks delivery of this public-domain source manifest. Routine source staging, shared-word selection, alignment and excerpt QC are build responsibilities, not requests for new research permission.
