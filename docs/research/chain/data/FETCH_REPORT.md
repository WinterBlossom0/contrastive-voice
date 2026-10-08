1. Written artifacts and source plan

[PLAN.md](PLAN.md) contains 51 tests covering SYNTHESIS sections 3–4, exact subset rules, licence quotes and the per-file URL/size/hash catalogue. Kernel: `kaggle/data/fetch.py`; metadata: `kaggle/data/kernel-metadata.json`; tests: `tests/test_data_fetch.py`. No Kaggle operation beyond the two permitted read-only dataset commands was performed.

| Source | Subset | Download | Kept | Licence | URL verified / route |
|---|---|---|---|---|---|
| Gettysburg | 6 remaining anniversary + 4 solo takes | 24.24 MB | ≈48.3 MB | PD | yes; HTTPS |
| Poetry | 34 Jabberwocky + 16 Hope takes | 74.03 MB | ≈147.8 MB | PD | yes; HTTPS |
| speechocean762 | 10 adults + 10 children; 400 sentences | 75.15 MB fallback | ≈75.2 MB | BY 4.0 | yes; mount / HTTPS fallback |
| EARS | p001–p004; 8 chunks × 5 styles | 434.76 MB ranges | ≈72.6 MB | BY-NC 4.0 | yes; HTTPS ranges |
| AVID | sp1–sp8; session 1, sentences 1–5 × 4 efforts | 5.69 MB ranges | ≈9.1 MB | BY 4.0 | yes; HTTPS ranges |
| DisfluencySpeech | 250 test utterances, one actor | 70.87 MB | unknown; cap 150 MB | Apache-2.0 | API yes; no local decode |
| PodcastFillers | 40 each: uh, um, breath, repeats, words | 12.34 MB ranges | ≈28.2 MB | Adobe + episode CC | yes; HTTPS ranges |
| SEP-28k | labels + episode table only | 2.26 MB | ≈2.3 MB | BY-NC 4.0 labels | yes; HTTPS |
| Expresso | 4 default/enunciated pairs + 4 emphasis demos | 8.19 MB | ≈2.0 MB | BY-NC 4.0 | HEAD yes; HTTPS |
| LibriTTS prominence | all 3,626 annotated utterances | 18.28 MB labels + mount | ≈758 MB; cap 900 MB | BY 4.0 | listing only for audio; mount |
| VCTK | all speakers, IDs 001–005, mic1 | mount; selected bytes unknown | unknown; cap 100 MB | BY 4.0 | listing only; mount |
| Accent Archive | english1–20 + spanish1–20 | mount; selected bytes unknown | unknown; cap 100 MB | BY-NC-SA 4.0 | listing only; mount |
| MDVR-KCL | all 37 ReadText recordings | 315.17 MB ranges | ≈165.9 MB | BY 4.0 | yes; HTTPS ranges |
| Lombard GRID | available s1–s4; 300 recordings | 39.24 MB ranges | ≈25.6 MB | BY 4.0 | range yes; HTTPS |
| LibriStutter | first 100 audio paths + matching CSVs | mount; selected bytes unknown | unknown; cap 100 MB | BY-NC 4.0 | listing only; mount |

Sizes use decimal MB. Kept values marked ≈ are calculations from source durations/header formats, not measured full-corpus outputs. Mounted selected sizes remain unknown. Exact URLs/statuses/reported sizes: `sources/fetch_resolution.json`, `fetch_url_checks.json`, `fetch_kaggle_mirrors.txt`. The four mount-only audio selections have no local download proof.

2. Capacity and time

Planned output allocation: 3.355 GB; enforced total below 18 GB; uncompressed source tar parts at most 4 GB. Expected output is roughly 1.4 GB plus four unknown mount selections and decoded DisfluencySpeech, bounded by the 3.355 GB source allocations plus small global metadata; hard total cap 18 GB. Estimated run time: priority 1 about 5–15 minutes; all sources 20–60 minutes, conditional on mounts/libraries/network. No full Kaggle benchmark.
No selected source was refused for output size. Whole EARS, AVID raw/EGG, PodcastFillers episodes, full Expresso tar and wholesale mounted corpora are excluded from output. All priority 2 sources are on by default; `CVOICE_PRIORITY2=0` disables them.

3. Full dry-run output

Command: `.venv/bin/python kaggle/data/fetch.py --dry-run` (exit 0).
```text
[fetch    0.0s] planned output cap=3,355,000,000 B; hard total=18,000,000,000 B; priority2=True; sources=15; refused=[]
[fetch    0.0s] startup: ffmpeg=available, ffprobe=available; pyarrow=absent (only DisfluencySpeech needs it)
[fetch    6.4s] gettysburg: checked; audio=10 labels=5 selected-transfer=24,236,559 B output-cap=90,000,000 B; HTTPS
[fetch    9.1s] poetry: checked; audio=50 labels=2 selected-transfer=74,034,707 B output-cap=180,000,000 B; HTTPS
[fetch    9.4s] speechocean: checked; audio=400 labels=18 selected-transfer=75,151,925 B output-cap=150,000,000 B; mount preferred; HTTPS fallback
[fetch   12.4s] ears: checked; audio=160 labels=4 selected-transfer=434,762,790 B output-cap=500,000,000 B; HTTPS
[fetch   23.0s] avid: checked; audio=160 labels=3 selected-transfer=5,689,888 B output-cap=500,000,000 B; HTTPS
[fetch   23.5s] disfluencyspeech: checked; audio=0 labels=2 selected-transfer=70,871,754 B output-cap=150,000,000 B; HTTPS
[fetch   62.6s] podcastfillers: checked; audio=200 labels=5 selected-transfer=12,341,785 B output-cap=250,000,000 B; HTTPS
[fetch   63.5s] sep28k: checked; audio=0 labels=3 selected-transfer=2,256,580 B output-cap=5,000,000 B; HTTPS
[fetch   65.1s] expresso: checked; audio=12 labels=2 selected-transfer=8,191,668 B output-cap=20,000,000 B; HTTPS
[fetch   65.6s] prominence: checked; audio=on mount labels=2 selected-transfer=18,278,339 B output-cap=900,000,000 B; mount required (audio sizes checked on Kaggle)
[fetch   66.5s] vctk: checked; audio=on mount labels=1 selected-transfer=17,416 B output-cap=100,000,000 B; mount required (audio sizes checked on Kaggle)
[fetch   67.8s] accent: checked; audio=on mount labels=1 selected-transfer=12,811 B output-cap=100,000,000 B; mount required (audio sizes checked on Kaggle)
[fetch   70.3s] mdvr: checked; audio=37 labels=1 selected-transfer=315,169,485 B output-cap=250,000,000 B; HTTPS
[fetch   73.8s] lombard: checked; audio=300 labels=3 selected-transfer=39,243,212 B output-cap=60,000,000 B; HTTPS
[fetch   75.0s] libristutter: checked; audio=on mount labels=1 selected-transfer=6,599 B output-cap=100,000,000 B; mount required (audio sizes checked on Kaggle)
[fetch   75.0s] dry-run complete: checked=15/15; no audio payloads downloaded; mounted audio enumerated only on Kaggle
```

Each pilot used `.venv/bin/python kaggle/data/fetch.py --only SOURCE --limit 2 --out /tmp/cvoice-pilot-SOURCE` (SOURCE below). All returned exit 0, `complete: true`, two WAVs and one uncompressed source tar. Wave-format checks and ffprobe confirmed 16 kHz mono PCM16. Manifest and archive hashes/status/stdout are saved in `sources/fetch_pilots.json`.

| SOURCE | Wall time | Tar bytes | Result |
|---|---:|---:|---|
| gettysburg | 22.3s | 9,349,120 | complete, 2 WAVs |
| poetry | 22.3s | 7,700,480 | complete, 2 WAVs |
| speechocean | 11.1s | 31,109,120 | complete, 2 WAVs |
| ears | 2.8s | 614,400 | complete, 2 WAVs |
| avid | 18.2s | 3,573,760 | complete, 2 WAVs |
| podcastfillers | 53.2s | 21,800,960 | complete, 2 WAVs |
| mdvr | 61.6s | 10,096,640 | complete, 2 WAVs |

Pilot HTTP payloads totalled 92,816,715 B, including original labels. Including research metadata, ZIP indexes and repeated dry-runs, conservative local-download accounting stays below 270 MB (300 MB limit). All pilot audio, label downloads, probe WAV and temporary research downloads were deleted after retaining audit records; no audio payload remains in the repository.

4. Unverified/unfetched data and attempts

- Prominence/VCTK/Accent/LibriStutter: successful permitted Kaggle searches/file listings; selected mounted audio cannot be enumerated locally. Kernel checks it on Kaggle and records missing data independently.
- DisfluencySpeech: API verifies test parquet 70,868,626 B and SHA-256; local pyarrow absent. No install/download attempted. Kernel checks the library before source download.
- SEP audio: mirror exists, but original rights remain with podcast owners and the mirror mixes FluencyBank. Only labels are ingested; natural block/prolongation validation remains pending.
- VerBIO and StressID access pages HEAD 200; no direct data URL verified. Academic request/signatory conditions remain; no request sent. CHAINS HEAD timed out; LUCID HEAD 404.
- UCLASS homepage/release pages GET 200; no subtype-labelled reading-file pair verified. DeepFry WAV/TextGrid HEAD 200 (2,818,482 / 411,612 B), but third-party audio licence coverage unconfirmed. Respiro labels HEAD 200 (19,615 B); its reachable sample is from a different split and is not claimed as matched test data.
- CC canonical legal-page HEADs returned 403/17 B. Actual upstream licence files/metadata were read; these legal URLs are reported blocked, not verified 200.

5. Tests

- `.venv/bin/python -m pytest -q tests/test_data_fetch.py`: 9 passed.
- `.venv/bin/python -m pytest -q`: 207 passed, 2 deselected (198 existing fast tests + 9 new tests).
- `.venv/bin/ruff check --select F,E9 kaggle tests`: all checks passed.

6. Decisions the owner might change

- Small subsets: four EARS speakers; eight AVID speakers (one female, seven male); balanced 20-speaker speechocean selection. This proves access/paired tests and does not establish population norms.
- Two weekly poems, retaining repeated-reader takes but grouping their speaker IDs. Volunteer introductions remain; Gettysburg uses a canonical target transcript, poetry text is null where no ready transcript was verified.
- PodcastFillers enabled for private research; Adobe terms specifically limit metadata use to academic research/teaching. One-second clips serve event acoustics/filler insertion; episode-context tests are deferred because longer events are truncated.
- Expresso uses small official demo pairs rather than its 36 GB tar. DisfluencySpeech uses the test parquet; LibriStutter is explicitly synthetic. These subsets do not supply all natural disfluency subtypes.
- Five mirrors are mounted; SEP podcast audio is excluded. Priority 2 remains enabled by default because its allocations fit.
