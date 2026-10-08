# Demonstration video: shot list and narration

Length: **7 minutes 35 seconds**. Narration is spoken English at about 140 words per minute, with pauses for clicks and playback. `video.srt` contains the narration below, word for word, as English subtitles.

| Chapter | Time |
|---|---|
| Opening | 00:00–00:20 |
| Dataset collection | 00:20–02:10 |
| Stress testing across speech qualities | 02:10–03:55 |
| Dashboard catching deviations | 03:55–07:10 |
| Closing | 07:10–07:35 |

Audio from the recordings is heard three times: G5 against the reference (Shot 6), the flagged span of a gallery example in both recordings (Shot 11), and the flagged span of the live upload in both recordings (Shot 15).

## Before recording

- Start the server from the repository root and keep it running: `uv run --extra cpu python -m cvoice.app`. Open `http://127.0.0.1:7860`. Run one analysis beforehand so that the alignment checkpoint is already cached.
- Open in an editor: `data/sources_manifest.json`, `data/dataset/manifest.json`, one file from `data/dataset/labels/`, `docs/evidence/STATUS.json`, `docs/evidence/tables.md` and `docs/technical.pdf`.
- Open the Kaggle page of the kernel that produced the released evidence. Show its real log or output, not a mock terminal.
- For the upload in Shot 14 use `data/dataset/flawed/greenman_reagan__x2_L3.wav` (John Greenman's reading with a level-3 DRAG and a level-3 MONOTONE edit), the bundled reference and its prefilled transcript. An upload is analysed as a different performance (R2). The outcome was verified on the local server on 2 October 2026 and saved in `build/work/upload_result_x2.json`: regime R2, overall score 99.99, one flagged region, "Slower here: 11.42-13.48 s ('up there that I')", 153 % longer, flagged above 150 %, costing 0.01 points, and five listed differences. The narration of Shot 15 states these values; if the screen shows different values, stop and find the cause before recording. If the request fails, fix the cause and record it again; do not substitute a gallery result. If the wait is long, shorten it in the edit and label the cut "processing wait shortened".
- Before any A/B playback, wait until the clock beside **Play recording** shows the clip duration.

## Opening

### Shot 1 · 00:00–00:20

**On screen:** Browser at `http://127.0.0.1:7860` with the example **Level 3 → Set A** loaded: score row, **Flagged regions (6)**, selected finding, waveform and charts.

**Actions:** Click **Set A** under **Level 3**. Move the pointer from the score to the selected finding to the chart.

**Narration:**

Contrastive Voice compares a recording with a reference reading of the same words. It shows where the delivery departs, by how much, and what that costs in a reference-relative score. I will show the dataset, the stress tests, and the dashboard with a live analysis.

## Dataset collection

### Shot 2 · 00:20–00:45

**On screen:** `data/sources_manifest.json`: one entry.

**Actions:** Show one manifest entry (download URL, SHA-256, licence basis, split).

**Narration:**

The reference recordings are public domain: nine United States government speeches and ten LibriVox readings. The source manifest records each download address, checksum, licence basis and speaker split. The build selects one passage of about thirty seconds from each speech by matching recognised words to the official transcript. That favours passages the aligner handles well.

### Shot 3 · 00:45–01:10

**On screen:** The Kaggle kernel page (accelerator T4 x2) and its log; then `docs/evidence/STATUS.json`.

**Actions:** Show the device plan and the four stage lines in the log. In `STATUS.json` highlight `complete: true` and `total_seconds: 652.7`.

**Narration:**

The dataset is built in one Kaggle script kernel on two T4 graphics processors. The runner checks the staged source hashes, installs the locked environment, and runs four stages: dataset, calibration, evaluation and gallery. The final run took six hundred and fifty-three seconds, about eleven minutes. The status file shows four of four stages complete.

### Shot 4 · 01:10–01:40

**On screen:** `data/dataset/manifest.json` (counts), then one label file.

**Actions:** Expand `counts` (121 files, 54.1 minutes, 9 baselines, 10 readers, 102 flawed). Open a label file and point to type, level, word span and sample span.

**Narration:**

The dataset holds one hundred and twenty-one audio files, fifty-four point one minutes. Nine speakers are split five for training, two for validation and two for test. One hundred and two clips are generated: identity controls, single-level clips, a ladder from one small edit to a botched passage, and edited second readers. Each label stores the edit type, level, word span and sample span.

### Shot 5 · 01:40–02:10

**On screen:** Browser, **Examples** row. **Identity**, then **Level 2 → Set A** with the black **Injected edit** bars and the shaded flagged regions.

**Actions:** Click **Identity** (score 100.0, no flagged regions). Click **Set A** under **Level 2**. Point to a black bar and the shaded region under it.

**Narration:**

These flaws are controlled acoustic edits, not human errors, and nobody has listened to and rated them. There are eight edit types at three levels: faster or slower speech, dropped or inserted pauses, flattened pitch, removed emphasis, a fade, and spectral smoothing. On the page, black bars mark the injected edits, and shaded regions mark what the detector flagged.

## Stress testing across speech qualities

### Shot 6 · 02:10–02:50 (narration 02:10–02:38)

**On screen:** Browser, **Examples** row with the score on each chip: **Identity 100.0**, **Level 1 Set A 97.2**, **Level 2 Set A 95.0**, **Level 3 Set A 85.1**, **G5 40.2**.

**Actions:** Click **Identity**, **Level 1 → Set A**, **Level 2 → Set A**, **Level 3 → Set A**, then **G5**. From 02:38, without narration: play about 5 seconds of **G5** with **Play recording**, then the same opening words of the reference.

**Narration:**

The examples form a spectrum of quality. Identity runs every recipe with neutral settings and scores one hundred with no flags. From level one to level three the score falls from ninety-seven to eighty-five. G five is the botched end: the whole passage is rushed and flattened, with dropped pauses and fades, and it scores forty point two. Listen to G five, then to the reference.

### Shot 7 · 02:50–03:18

**On screen:** `docs/technical.pdf`, Results table (train, validation, test rows).

**Actions:** Highlight the **Test (final)** row: 0.879 (29 / 5 / 3).

**Narration:**

The test split has two speakers and was evaluated once, after the design was frozen. Of thirty-two edits at levels two and three, twenty-nine are matched one to one with at least half overlap. With five false flags and three misses, strict event F one is zero point eight seven nine. Matched region boundaries miss the label by up to zero point nine eight seconds.

### Shot 8 · 03:18–03:45

**On screen:** Browser: the link **Stress matrix: …** under the score row, then the opened table **Stress matrix: how much the output moves when only the recording conditions change**.

**Actions:** Click the stress-matrix link. Point to the test rows for gain, MP3, white noise, low-pass and dynamic-range compression, and to the column with the achieved compression reduction.

**Narration:**

The stress matrix changes only the recording channel. On the test recordings, a six decibel gain change and MP3 coding add no regions. White noise at twenty decibels signal-to-noise ratio adds one pace flag, and a low-pass filter adds two. Heavy compression, about ten decibels of gain reduction, is the failure: it adds five false pause and volume flags in about one minute.

### Shot 9 · 03:45–03:55

**On screen:** The same stress matrix: the two test rows "(flawed L2+L3)".

**Actions:** Highlight "flaws found before / after" 29 → 27 and 29 → 24.

**Narration:**

On edited test clips, twenty-nine edits are found before stress, twenty-seven after noise, and twenty-four after compression.

## Dashboard catching deviations

### Shot 10 · 03:55–04:25

**On screen:** Browser, **Level 3 → Set A**. Score row (**Delivery score (relative to this reference)** 85.1), **Flagged regions (6)**, selected finding **#3 Rushed**.

**Actions:** Click **Set A** under **Level 3**. Click **#3 Rushed** in **Flagged regions**. Open **Measurements and context**.

**Narration:**

This is level three, set A, compared with the recording it was edited from. The delivery score is eighty-five point one, with six flagged regions. I select Rushed. The explanation names the words, gives the span in both recordings, and says the speech took zero point eight seven seconds against one point six two in the reference. It costs four point one points.

### Shot 11 · 04:25–04:55 (narration 04:25–04:45)

**On screen:** The selected finding with the buttons **A This recording** and **B Reference**; the chart row **Pace** with the black bar and the shaded box; the **Transcript**.

**Actions:** During the narration point to the two buttons, the chart row, the **Cadence** card and a transcript word. From 04:45, without narration: click **A This recording** and listen, then **B Reference** and listen.

**Narration:**

Button A plays this span in the participant recording. Button B plays the same words in the reference. The black bar is the injected edit, and the shaded box is the flagged region. The category cards filter the list, and clicking a word in the transcript plays it.

### Shot 12 · 04:55–05:25

**On screen:** Browser, **Other performance → Greenman edited**. Score 100.0, **Flagged regions (0)**, the threshold note under the score, and **Largest differences from the reference (not scored)**.

**Actions:** Click **Greenman edited**. Point to "Regime R2" and the thresholds under the score. Scroll the list of largest differences to its end and click **Lower level here than the reference**, then **Longer pause here than the reference**.

**Narration:**

Now a different speaker. John Greenman reads the same passage, with an inserted pause and a fade. The regime is R two, and its thresholds are wide because two good readers differ a lot: twenty-two point eight decibels for volume. Nothing is flagged and the score stays at one hundred. The two edits are the last two of five listed differences, behind three that are not edits. The list is not scored.

### Shot 13 · 05:25–05:55

**On screen:** `docs/technical.pdf`, Results, the paragraph **R2, different speaker (development evidence)**.

**Actions:** Highlight "1 of the 15 is flagged", then "13 lie on an injected edit", then "6 false regions".

**Narration:**

On three check readers, eighteen edits were injected and one was flagged. Fourteen of the fifteen that move away from the reference were flagged or listed, but the list has five entries with or without an edit, so it does not separate edits from reader differences. Unedited reader pairs give six false regions in seven point seven six minutes. For another speaker, a score of one hundred means only that nothing crossed the thresholds.

### Shot 14 · 05:55–06:25

**On screen:** Browser, the section **Analyse your own recording**: **Your recording**, **Reference rendition**, **Transcript: the exact words both recordings read**, the **Analyse** button, then the stage list.

**Actions:** Click **Analyse your own recording**. Under **Your recording** choose `data/dataset/flawed/greenman_reagan__x2_L3.wav`. Keep the bundled **Reference rendition** and its transcript. Click **Analyse**. Keep the stages decode, align, features, compare, detect on screen.

**Narration:**

Now a live upload. I open Analyse your own recording and choose a file from the dataset: John Greenman's reading with two level-three edits, a slowed stretch and a flattened stretch. I keep the bundled Reagan reference and its transcript, and press Analyse. The stages run: decode, align, features, compare, detect. Every upload is treated as a different performance, so the R two thresholds apply.

### Shot 15 · 06:25–07:10 (narration 06:25–06:55)

**On screen:** The finished upload result: regime line (R2), threshold note, **Flagged regions (1)** with the finding "Slower here: 11.42-13.48 s", the list of largest differences (five entries), charts.

**Actions:** Select the flagged region and point to its measurement sentence and to the chart row **Pace**. From 06:55, without narration: click **A This recording** and listen to the span, then **B Reference** and listen to the same words.

**Narration:**

The result is regime R two, with one flagged region: slower here, from eleven point four to thirteen point five seconds, on the words up there that I. That stretch is one hundred and fifty-three percent longer than the reference at the reader's own tempo, and the flag threshold is one hundred and fifty percent. It costs one hundredth of a point. The flattened stretch is not flagged. Now both recordings.

## Closing

### Shot 16 · 07:10–07:35

**On screen:** `README.md`: the first paragraph, then the section **Grounding in prior work**, then Limits. End on the dashboard.

**Actions:** Scroll from the first paragraph to the grounding section, then to Limits.

**Narration:**

On the test split, strict event F one is zero point eight seven nine for edits of the same recording. Detection across speakers is weak, heavy compression causes false flags, and no listener has rated the synthetic flaws. The repository holds the dataset, the evidence, the link from each measurement to prior research, and commands to reproduce this.
