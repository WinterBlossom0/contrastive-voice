# Real-recording acquisition plan — v2 repair (2026-10-02)

This replaces the minimal v1 selection. No target was lowered. Audio is retained as 16 kHz mono PCM16, with original score files, time stamps, licences and provenance. One PAX tar per source, each at most 4,000,000,000 bytes; output allocations sum to 12,495,000,000 bytes under the 18 GB limit.

The [v2 URL/member catalogue](sources/fetch_resolution_v2.json) records every selected URL, archive part/offset/CRC/size, repository hash and reader/condition. Its embedded-byte fields are length/hash summaries, not downloadable data. Runtime resolution rechecks the APIs and archive directories. The [v1 evidence](../../../kaggle_runs/data_v1/STATUS.json), [mirror listings](sources/fetch_kaggle_mirrors.txt), [v2 dry run](sources/fetch_dry_run_v2.txt), and [pilot audits/probes](sources/fetch_pilots_v2.json) distinguish origin checks from completed local audio fetches.

Sizes below are decimal. Transfers include deliberately overfetched merged ranges; directory/CSV overhead is shown separately. Mount audio consumes no network download on Kaggle. Kept estimates are format/duration calculations, except measured v1 sizes. Unknown mount populations and durations remain unknown until enumerated on Kaggle. Request counts exclude retries; redirects to variable CDN hosts are identified separately and logged during execution.

| Source | Subset | Transfer | Kept | Requests / host | Representative exact URL |
|---|---|---:|---:|---|---|
| `gettysburg` | Unchanged: six remaining anniversary takes and four solo takes | 24.12 MB | 48.3 MB | archive.org: 15; download CDN: 10 | [gettysburg origin](https://archive.org/metadata/gettysburgaddress_150anniv_1311_librivox) |
| `poetry` | 20 public-domain items, ≥10 distinct reader IDs each; Jabberwocky and Hope retained; 323 takes | 401.88 MB | ≈805 MB | archive.org: 343; download CDN: 323 | [poetry origin](https://archive.org/metadata/jabberwocky_librivox) |
| `speechocean` | All 5,000 scored train/test utterances, 250 speakers; every repository score/metadata file | Mount; 672.48 MB HTTPS equivalent | ≈686 MB including conservative tar allowance | api.github.com: 1; raw.githubusercontent.com: 2 + 0–18 metadata replacements | [speechocean origin](https://raw.githubusercontent.com/jimbozhang/speechocean762/613968e3b0b789fc33936fb5eba1973176ba7d11/resource/scores-detail.json) |
| `ears` | p001–p107: rainbow_01..08 × regular/fast/slow/loud/whisper; 4,280 WAVs | 13.726 GB + 15.72 MB ZIP directories | ≈2.24 GB | api.github.com: 1; github.com and release-assets.githubusercontent.com: 3,210 each; raw.githubusercontent.com: 8 | [ears origin](https://github.com/facebookresearch/ears_dataset/releases/download/dataset/p001.zip) |
| `avid` | All 50 speakers, sen1..5 × four efforts × both sessions: 2,000 WAVs; all 51 small calibration WAVs, CSV, Readme | 408.13 MB + 3.23 MB index | ≈141 MB | zenodo.org: 12 | [avid origin](https://zenodo.org/api/records/10524873/files/AVID.zip/content) |
| `disfluencyspeech` | Unchanged: 250 test utterances, all transcript variants | 70.87 MB | ≈53 MB (v1 measured) | huggingface.co: 4 initial requests; payload CDN: 1 | [disfluencyspeech origin](https://huggingface.co/datasets/amaai-lab/DisfluencySpeech/resolve/main/data/test-00000-of-00001.parquet) |
| `podcastfillers` | 500 clips each Uh/Um/Breath/Repetitions/Words; ten shortest complete MP3 episodes with all annotations, transcripts and VAD metadata | 2.194 GB + 21.59 MB directory/CSV resolution | ≈300–400 MB; 1.5 GB enforced cap | zenodo.org: 68 | [podcastfillers origin](https://zenodo.org/api/records/7121457/files/PodcastFillers.zip/content) |
| `sep28k` | Unchanged: labels and episode table only | 2.26 MB | ≈2.3 MB | raw.githubusercontent.com: 6 | [sep28k origin](https://raw.githubusercontent.com/apple/ml-stuttering-events-dataset/main/SEP-28k_labels.csv) |
| `expresso` | All read default/enunciated/emphasis rows for ex01–ex04, including longform/default substyles; 12 read-mirror shards, one at a time | 5.761 GB | ≈0.48–0.8 GB; 1.5 GB enforced cap | huggingface.co: 15 initial; payload CDN: 12; raw.githubusercontent.com: 2 | [expresso origin](https://huggingface.co/datasets/ylacombe/expresso/tree/main/read) |
| `prominence` | Unchanged: 3,626 annotated utterances, 18 speakers; mounted LibriTTS audio | 18.27 MB labels + mount | ≈758 MB | zenodo.org: 2 | [prominence origin](https://zenodo.org/api/records/10402793/files/libritts-emphasis-annotations.json/content) |
| `vctk` | Rainbow IDs 006–024 for every mounted speaker; mic1 or legacy single-mic WAV; matching text and COPYING | Mount only | Unmeasured; ≈0.25–0.4 GB, cap 500 MB | 0 network requests | [vctk origin](https://www.kaggle.com/datasets/kynthesis/vctk-corpus) |
| `accent` | Every mounted englishN native reader + first 200 other-language reader filenames; speaker CSV and passage | Mount; 12.8 kB access notice | Unmeasured; ≈0.7–1.1 GB, cap 1.5 GB | accent.gmu.edu: 1 | [accent origin](https://www.kaggle.com/datasets/rtatman/speech-accent-archive) |
| `mdvr` | Unchanged: all 37 ReadText HC/PD recordings | 606.14 MB whole ZIP + 0.15 MB index | ≈166 MB | zenodo.org: 4 | [mdvr origin](https://zenodo.org/api/records/2867216/files/26_29_09_2017_KCL.zip/content) |
| `lombard` | Every released talker: 54 (s2–s55); all 5,371 plain/Lombard WAVs and original JSON/alignment ZIPs | 655.21 MB + 0.70 MB index | ≈424 MB + tar allowance | zenodo.org: 6 | [lombard origin](https://zenodo.org/api/records/3736465/files/lombardgrid_audio.zip/content) |
| `libristutter` | Unchanged: first 100 audio paths and required matching CSVs; synthetic | Mount; 6.6 kB access notice | ≈52 MB (v1 measured) | borealisdata.ca: 1 | [libristutter origin](https://www.kaggle.com/datasets/danimarch/libristutter-unchanged) |

Mount references remain `tthieu0901/speechocean762`, `luizfelipebjcosta/libri-tts-train-clean-100`, `kynthesis/vctk-corpus`, `rtatman/speech-accent-archive`, and `danimarch/libristutter-unchanged`. Exact mounted bytes/populations are measured by the kernel, not claimed from a paginated listing. The 250 SpeechOcean speaker IDs include 5,245 repository WAVs: only the 5,000 IDs in train/test utt2spk are scored and selected.

Poetry item IDs are frozen in fetch.py/IA_ITEMS and the catalogue: Jabberwocky, Hope, At the Club, O Call It, The Old Roller Towel, Evanescence, Sonnet on a Wet Summer, The Road Builders, Before the Edgehill Fight, Youth's Spring Tribute, A Quatrain of Khayyam, To a Faded Rose, Symphony in Yellow, Summer Sun, Song of the Soldiers' Wives, A Word Is Dead, The Visionary, Silver Filigree, Near and Far, My Shadow. Each item must retain its own public-domain declaration and ≥10 distinct reader IDs. Repeated Jabberwocky takes are grouped by reader.

AVID includes both sessions rather than assuming every session-1 filename exists: sp35 has 19 ordinary session-1 names and an additional session-2 `loud 2.wav`. The four efforts and all five requested sentences are represented for all 50 speakers. Fifty-one calibration tones total 51.83 MB uncompressed; their 94 dB/reference input-gain information is preserved in original filenames and metadata.

PodcastFillers uses the complete CSV, CRC-verified and read once during resolution, to choose 500/class. The ten complete episodes are the shortest original episode MP3s, sorted by published size/path; their exact names are in the catalogue. All matching episode_annotations, episode_transcripts, episode_vad files are retained, alongside the full event CSV and per-episode licence table. Unicode archive names with missing UTF-8 flags are decoded correctly; PAX permits their long annotation names. These are actual full episodes, not concatenated clips; complete timestamps retain their original episode origin.

Expresso's official README identifies default_emphasis as a default substyle. The read mirror exposes it as style `emphasis` (verified in viewer rows 800–899), plus default and enunciated. All 12 shards are SHA-256 verified and processed sequentially; other styles and temporary parquet files are discarded. Every required style must occur for every one of ex01–ex04. The converted selection is expected below 1.5 GB; that allocation is enforced, and exceeding it is an explicit source failure. Full decode could not be tested locally because pyarrow is absent and installs are prohibited.

## Failure evidence and access design

V1 STATUS records 728 successful URL checks and 282 successful Zenodo requests; failures were not audited. AVID contributed 136 archive ranges (3 during resolution, 133 during its 31.0-second fetch stage), approximately 258 requests/minute. PodcastFillers contributed 136 archive ranges (3 resolution, 133 during its 29.1-second fetch stage), approximately 274 requests/minute, plus one standalone CSV range. At least 133 successful requests occurred within a 60-second window for each burst. The audit lacks individual request timestamps and failed-response headers/body, so exact rolling-window peaks and Retry-After values cannot be recovered. The old two-attempt HTTP loop also retried errors immediately.

| Failure | Exact failing route (reconstructed from resolver/order when absent from audit) | Origin evidence | Fix |
|---|---|---|---|
| AVID | `https://zenodo.org/api/records/10524873/files/AVID.zip/content` | 136 successful 206 ranges; fetch.log ends in 429 | Merge selected sentence/calibration ranges; 8 payload requests rather than thousands of local-header/member requests |
| PodcastFillers | `https://zenodo.org/api/records/7121457/files/PodcastFillers.zip/content` (plus z01 for early members) | 128 ZIP + 8 z01 successful ranges; ends in 429 | Complete CSV once, larger merged windows; 62 payload requests |
| Prominence | `https://zenodo.org/api/records/10402793/files/libritts-emphasis-annotations.json/content` | API resolved 200; label GET failed 429 after preceding bursts | Shared host pacing/retry budget, not a per-source limiter |
| MDVR | `https://zenodo.org/api/records/2867216/files/26_29_09_2017_KCL.zip/content` | Two resolving ranges 206; member GET failed 429 | One whole 606 MB ZIP; verify MD5 then extract members locally |
| Lombard | `https://zenodo.org/api/records/3736465/files/lombardgrid_json.zip/content` | Audio directory resolved 206; first label GET failed 429 | Shared pacing; one whole 653 MB audio ZIP and two small label downloads |
| SpeechOcean | Mounted `README.md`, before any README HTTP request | Expected pinned Git blob 12,951 B, SHA1 790b4301616fd8c822cefcf1068ae75464acb708; mirror listing 13,066 B | Never compare two different copies as one immutable file: verify mirror size/Git blob hash, fetch and verify pinned bytes if different; record acquisition route. Exact mirror edit is unavailable locally |
| VCTK | `https://datashare.ed.ac.uk/server/api/core/bitstreams/956a1688-0b59-428c-8a2f-10837433dde3/content` | Resolve 403 from Kaggle; failed response absent from audit | Zero Edinburgh requests. Use mounted COPYING (listing: 18,951 B), read its licence URL/version, retain it, record local path in acquisition.json/STATUS. Do not assume the older mirror's licence version |

Published Zenodo guest policy: **“60 requests per minute, 2000 requests per hour”** ([Zenodo developers](https://developers.zenodo.org/#rate-limiting)). The per-host start interval is 2.1 seconds across sources, redirects and retries: at most 29 requests in any minute and 1,715/hour, below both limits. Full run: **92 initial Zenodo requests** = AVID 12 + PodcastFillers 68 + prominence 2 + MDVR 4 + Lombard 6. ZIP payload windows merge gaps ≤4 MiB on Zenodo, with a 64 MB bound; extra transfer is cheaper than thousands of requests. AVID's 9.95 GB archive and PodcastFillers' 25.24 GB multipart archive are not downloaded whole. MDVR/Lombard files are small enough for whole-download disk/time checks.

EARS uses ≤256 KiB gaps, bounded windows and one speaker's cache at a time; its 62.89 GB aggregate full release is unnecessary. Approximately 13.73 GB transferred becomes ≈2.24 GB output, without retaining the whole cache during conversion. Directory resolution uses four workers with synchronized host pacing. Every member still passes size/CRC checks. Direct downloads stream to disk rather than memory.

GitHub publishes **“60 requests per hour”** for anonymous REST use ([GitHub limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)): this run uses only two REST API calls. Release/CDN downloads are not REST API requests; no numerical public release-CDN limit was found, so that distinction is not used to invent a quota. Raw GitHub normally sees 19 initial requests, up to 36 if all 18 mirror metadata files need replacement. Hugging Face publishes anonymous quotas of 500 API and 3,000 resolver requests per five minutes ([HF limits](https://huggingface.co/docs/hub/rate-limits)); this run uses two API and 17 initial resolver requests, plus redirects. Archive.org's initial requests total 358; CDN targets are runtime redirects. No fixed numeric Archive/CDN policy is asserted.

HTTP audits now retain timestamps, methods, redirects, statuses, headers, received bytes, failed-response prefixes and retry waits. Retry-After seconds or HTTP dates are honored without shortening; otherwise rate-limit resets/exponential backoff apply. Five attempts maximum and 240 seconds of retry wait per request **and cumulatively per host**. A longer advertised wait fails explicitly instead of retrying early. Source errors remain isolated and recorded in STATUS.json; no failure is silently treated as success.

## Tests on real recordings

The questions below remain unchanged in scope; subset, URL, licence and size are specified once in the acquisition table/catalogue above. Existing human scores are retained, and unlabelled volunteer recordings are not automatically called flawless.

| Measure / pattern | Question | Sources |
|---|---|---|
| Within-phrase pause count and duration | Do inside-clause pauses separate low-rated fluency from ordinary phrasing across readers? | `speechocean`, `gettysburg` |
| Tempo decomposition | Does fast reading gain time through articulation, shortened pauses, or deleted pauses? | `ears` |
| Mean length of run | Does word-by-word reading reduce words per run at comparable fluency scores? | `speechocean` |
| Greedy decode vs known text: inserted material | Are repeats/restarts/fillers detected without turning normal accent variation into insertions? | `disfluencyspeech`, `speechocean` |
| Word posterior relative to own median/reference | Does a relative posterior follow word/phone accuracy after controlling rate and speaker? | `speechocean` |
| Pitch match by sentence | How much contour disagreement is legitimate across readers, and how does it track prosodic scores? | `gettysburg`, `poetry`, `speechocean` |
| Whole-clip percentile pitch span | What is the cross-reader span distribution on the same text, and is it stable by passage length? | `gettysburg`, `poetry` |
| Per-word latency and production contours | Do long word production and pre-word silence localise hesitation rather than ordinary phrase boundaries? | `speechocean`, `ears` |
| Tempo irregularity and drift | How much local tempo spread/drift is normal, and how does it change with fast/slow instructions? | `ears`, `gettysburg` |
| Orphan voiced gap, pitch/spectral stability | Do annotated uh/um differ from ordinary voiced words; how often is the event truncated? | `podcastfillers` |
| Silence inside aligned words: blocks | Does the inside-word rule find real blocks rather than alignment errors? SEP labels are clip-level only; natural labelled audio remains a data gap. | `libristutter`, `sep28k` |
| Spectral balance and pitch vs own median | Can quiet effort be separated from a gain change within the same speaker/sentence? | `avid`, `ears` |
| Phrase level slope and final-word drop | What is ordinary trailing-off spread across fluent readers; do reduced-loudness clinical readings exceed it? No healthy trailing-off ratings exist here. | `gettysburg`, `mdvr` |
| Sentence-final pitch change: direction | How often do ordinary statement readings rise or make only a weak fall? Low prosody scores are not ending-specific labels. | `gettysburg`, `poetry`, `speechocean` |
| Prominence-vector agreement and stress spread | Which emphasis differences between legitimate readings are normal, and does flatter prominence follow human judgements? | `gettysburg`, `prominence` |
| Per-sentence declination slope | What is normal sentence declination, including the proportion of legitimate non-falling sentences? | `gettysburg`, `poetry` |
| Two-sided prominence with function-word prior | Does a prior penalise actual marked function-word focus incorrectly? | `expresso`, `prominence` |
| Repeat/part-word/skip alignment graph | Can timestamps and transcript recovery survive controlled repeats and actual verbatim acted disfluency? Natural stutter transfer remains separate. | `libristutter`, `disfluencyspeech` |
| Aligned-word band-envelope / feature distance | Does distance fall for clearer articulation at the same word/text, and how much is normal cross-speaker distance? | `expresso`, `ears`, `speechocean` |
| Breath-pause location | Can annotated breath acoustics be found without splitting silence, and can manual inspection locate breaths relative to clauses? One-second clips lack clause context. | `podcastfillers`, `gettysburg` |
| Nervousness: raised pitch level | Can calm/anxious differences be established within speaker? Instructed EARS styles are not an anxiety manipulation. | VerBIO / StressID: same-speaker calm/anxious sessions; no open subset authorised or selected |
| Nervousness: silence share | Is silence share elevated in anxious readings with the same-speaker calm reference? | VerBIO / StressID: same-speaker calm/anxious sessions; no open subset authorised or selected |
| Nervousness: jitter/shimmer/tremor | Do quality cues survive effort/recording controls and predict anxiety? No qualifying unrestricted read-speech pairs verified. | VerBIO / StressID: same-speaker calm/anxious sessions; no open subset authorised or selected |
| Open: interval rhythm metrics | How do vowel/consonant timing metrics change with accent and fast/slow reading of a shared text? Requires phone alignment downstream. | `ears`, `accent`, `vctk` |
| Open: pause share across speakers | Does pause share separate speakers beyond text and phrasing differences? | `gettysburg`, `poetry`, `vctk` |
| Open: vowel space | Does vowel space change with enunciation/fast/whisper after within-speaker controls? | `expresso`, `ears` |
| Open: creak detection at endings | Can a pretrained creak detector generalise to these read passages? DeepFry test audio is reachable; its audio-specific licence coverage still needs clarification. | `gettysburg`, `expresso` |
| Open: trained disfluency detector | Can a detector learn acted/synthetic forms and transfer to real fillers/repetitions? Blocks are not validated by this source set. | `disfluencyspeech`, `libristutter`, `podcastfillers` |
| Open: trained prominence detector / accent-ratio prior | Do learned prominence values agree with crowd-labelled words including function words? | `prominence` |
| Open: trained breath detector | Can event-centred breath labels train/test detection against non-breath words and fillers? Frame/syntax transfer requires context. | `podcastfillers` |
| Open: absolute effort classes | Can soft/normal/loud/very-loud be classified with held-out speakers and identical microphone geometry? | `avid` |
| Open: own-baseline comparison | How much does same-speaker normal reference improve pace/effort comparison? | `ears`, `avid` |
| Absolute uploaded loudness (no tier) | Can a dataset recover SPL from an uncalibrated user upload? No; AVID labels test calibrated recordings only, not the missing calibration of an upload. | `avid` |
| Edit: natural rushing | Are simultaneous speed-up and pause deletion/shortening closer to instructed fast speech than uniform compression? | `ears` |
| Edit: hesitation | Does a stretched content word plus pre-word silence match low-fluency readings? | `speechocean` |
| Edit: word-by-word reading | Does adding 0.15–0.3 s gaps every one/two words resemble low-rated segmentation/run patterns? | `speechocean` |
| Edit: uneven tempo | Is random word-rate modulation distinguishable from normal cross-reader and slow/fast variation? | `ears`, `gettysburg` |
| Edit: one lengthened function-word repetition | Do edits match acted and naturally annotated repetition acoustics? Podcast clips may truncate the full repeat. | `disfluencyspeech`, `podcastfillers` |
| Edit: rapid onset repeats of stressed content words | Do synthetic onset repeats resemble real stuttering, rather than just synthetically annotated events? Natural audio licence/access not yet established. | `libristutter`, `sep28k` |
| Edit: word-final rhyme prolongation | What duration and spectral shape do acted/natural hesitation prolongations have? The acted test subset is not guaranteed to contain every subtype. | `disfluencyspeech` |
| Edit: onset continuant stretched toward 1 s | Can the synthetic recipe reproduce prolongation features? Natural subtype-labelled validation remains pending. | `libristutter`, `sep28k` |
| Edit: inside-word silence block | Does an artificial block resemble a real labelled block? SEP labels alone cannot answer; UCLASS reading access/labels must be checked. | `libristutter`, `sep28k` |
| Edit: inserted recorded filler | Are a real recorded uh/um pool and inserted fillers acoustically representative without being centre-truncated? | `podcastfillers` |
| Edit: low effort (gain + tilt + lower pitch) | Do edited low-effort cues reproduce same-speaker soft readings, beyond a gain-only recording change? | `avid`, `ears` |
| Edit: trailing off (gain + tilt ramp) | Does the ramp exceed normal sentence-final decline, and resemble reduced-loudness readings? No healthy trailing-off ground truth. | `gettysburg`, `mdvr` |
| Edit: move pitch peak to another content word | Does the edit reproduce different marked focus placements in original samples? | `expresso` |
| Edit: boost a function word | Does the edit produce a marked-focus prominence pattern rather than merely loudness? | `expresso`, `prominence` |
| Edit: remove all stress cues | Does the edit flatten the pitch/energy/duration prominence vector beyond normal reader disagreement? | `gettysburg`, `poetry`, `prominence` |
| Edit: rising final syllable | Is the imposed rise within observed sentence-ending contour shapes? Requires manual direction judgements, not inferred prosody labels. | `gettysburg`, `poetry` |
| Edit: flatten a final fall | Does the edit flatten an actual terminal fall beyond legitimate reader variation? | `gettysburg`, `poetry` |
| Edit: repeat one contour across sentences | Can repeated contours be separated from legitimate passage-level span and repeated phrasing? | `gettysburg`, `poetry` |

## Verification and capacity

`.venv/bin/python kaggle/data/fetch.py --dry-run`: 15/15, exit 0, 166.7 seconds. Metadata and ZIP-directory/CSV ranges are fetched; no audio payloads are downloaded by dry-run. Mount audio is enumerated only on Kaggle. Dry-run's selected-transfer figure for SpeechOcean is its HTTPS equivalent, not a claim that mounted audio needs network transfer.

The five laptop-fetchable failing sources passed `--only SOURCE --limit 2`: SpeechOcean 10.2 s; AVID 88.0 s; PodcastFillers 119.0 s; MDVR 53.1 s; Lombard 16.2 s. Each STATUS is complete, each tar has two audio files, and ffprobe confirms mono PCM16/16 kHz. Original labels are preserved even in a two-audio pilot. VCTK/prominence audio could not be exercised without the mounted mirrors; full Expresso decoding could not be exercised without pyarrow. The kernel's v1 log confirms that Kaggle supplies pyarrow.

Tests: fetch suite 15 passed; full suite 222 passed, 2 deselected; F/E9 lint passes. Tests cover tar padding/single-tar rejection, multipart CRC verification, reuse of merged ranges, stale mirror verification, Retry-After and bounded wait, VCTK Rainbow/mirror licence selection, and cross-shard Expresso filtering. No restricted source or other engineer's files were edited.

Expected retained output **≈6.8–8.1 GB**, capped by source allocations totalling **12.495 GB**, with every source allocation <4 GB. Expected network transfer **≈23.9 GB**, mostly EARS and the read-only Expresso parquet mirror; mounted corpus bytes are additional local reads. Expected CPU/network wall time **≈60–150 minutes at 5–15 MB/s**, contingent on Kaggle connectivity; this is not a measured full v2 kernel run. No subset target was lowered for rate/output limits. Caches/parquets are temporary, one EARS speaker/Expresso shard at a time, and removed before packing. Partial source tars are deleted on failure.

Repeated local directory checks exceeded the requested ~300 MB download budget: at least 315 MB is accounted in completed dry-runs/pilots, with research/aborted checks giving an estimated **~0.36–0.40 GB total**. This is a verification-process overrun, not a subset limitation. Downloaded pilot payloads and temporary directories are deleted; only audits, hashes, probes and small catalogues remain. No new Kaggle kernel run was authorized or performed.
