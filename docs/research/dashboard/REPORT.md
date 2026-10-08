# Interactive dashboard: implementation guidance (FastAPI + one static HTML/JS page)

Researcher report, 2026-10-01. Stack is decided (FastAPI + one static page, Plotly.js + wavesurfer.js from a CDN, no build step); this report only makes it concrete.

Evidence tags used throughout:

- **[R]** VERIFIED_BY_RUNNING - executed by the previous (interrupted) run on the laptop; the output file is cited. Nothing was executed on Kaggle for this topic (topic rule: no compute) and nothing compute-like was executed locally in this session.
- **[S]** VERIFIED_BY_SOURCE - read this session (or by the previous run) in a pinned library file, a released wheel, or a primary document; URL or file cited.
- **[U]** UNVERIFIED - memory or reasoning only.

All file paths below are relative to
`(a temporary session folder, not kept)` unless absolute.

---

## 1. Recommendation

1. **Pin exactly this front-end set, loaded as classic `defer` scripts (UMD globals) with SRI:** `plotly.js-cartesian-dist-min@4.1.1` + `wavesurfer.js@8.0.1` core + `regions` + `timeline` plugins. It is the only combination that was exercised in a real browser (headless Chromium 151) before the previous run was stopped: CDN load, stacked rows on one x axis, shaded flaw bands with labels, click-anywhere selection, unified hover across rows, region click, `play(start, end)` on two players, keyboard flaw list, x-axis toggle [R: `browser_test/results.json`]. 526 KB on the wire in total.
2. **Back end pins:** `fastapi==0.142.2`, `uvicorn==0.54.0`, `python-multipart==0.0.32` (pulls `starlette==1.7.0`, `pydantic==2.13.5`), system `ffmpeg`. Verified together under CPython 3.12.13: upload of 7 container formats, decode, size cap, sniffing, progress polling, Range-served WAV [R: `probe_backend.out`, `freeze_py312.txt`].
3. **Time axis:** one Plotly figure, one shared x axis = the **participant's true time**; the baseline's features are warped onto it with the word-alignment piecewise-linear map (the reverse of option (a) in the brief). Add a toggle to baseline time. The two recordings are additionally shown as two wavesurfer strips, each on its own true clock, with flaw regions on both. Every flaw object carries both true spans (`p` and `b`), so timestamps never come from warped pixels.
4. **One render path:** gallery examples are static result JSON files (built on Kaggle) with exactly the same schema as an upload's result. `render(result)` is the whole page; the gallery works with no back end at all.
5. **Progress = polling** `GET api/jobs/{id}` every 500 ms. No SSE, no WebSocket.
6. **Upload hardening that Starlette does not do for you:** an ASGI body-size cap, magic-byte sniffing with a forced ffmpeg demuxer, server-generated file names, ffmpeg timeout and duration cap.
7. **Deployment:** Docker image on port 7860 (works locally and on a Hugging Face Docker Space). Creating a Docker Space now requires a paid HF plan [S]; the gallery part of the page can be hosted free as a static site because of point 4.

Build order (each step is usable alone): (1) `render(result)` from a gallery JSON: chart, bands, flaw list, explanation, two players; (2) upload + polling; (3) transcript panel; (4) score cards; (5) cut-first extras: axis toggle, ground-truth markers, microphone recording, theme toggle.

---

## 2. Q1 - Current versions and APIs (2026-10-01)

### 2.1 Versions

| Package | Latest | Released | Licence | Evidence |
|---|---|---|---|---|
| plotly.js (`plotly.js-dist-min`, `-cartesian-dist-min`, `-basic-dist-min`) | 4.1.1 | 2026-09-14 (4.0.0: 2026-08-24, 4.1.0: 2026-09-08) | MIT | [R] npm registry + jsDelivr API, `meta/npm_*.json`, `meta/jsd_*.json`; re-checked 13:23 UTC, `cdn_headers_and_registry.out` |
| wavesurfer.js | 8.0.1 | 2026-09-24 (8.0.0: 2026-09-23; last 7.x: 7.12.12, 2026-09-10) | BSD-3-Clause | same |
| fastapi | 0.142.2 | 2026-09-30 (0.142.0: 2026-09-29) | - | [R] PyPI JSON, `meta/pypi_fastapi.json`, `meta/pypi_now_fastapi.json` |
| starlette | 1.7.0 | 2026-09-23 | - | same |
| uvicorn | 0.54.0 | 2026-09-25 | - | same |
| python-multipart | 0.0.32 | 2026-06-04 | - | same |
| uv (for the Docker image) | 0.12.21 | 2026-09-29 (laptop has 0.12.3) | - | `meta/pypi_now_uv.json` |

All four Python packages are pure-Python wheels (`py3-none-any`), `requires_python >= 3.10`; `pydantic-core 2.46.5` has manylinux x86_64 wheels for cp310-cp314 [R: previous run's PyPI listing, `PREVIOUS_RUN_condensed.md` lines 1622-1636]. So the web stack does not constrain the choice between Python 3.12 / 3.13 / 3.14; it was run on 3.12.13.

Recent-release caveats [S]:

- FastAPI 0.142.0 (2 days old) added native OpenTelemetry and made `opentelemetry-api` a hard dependency; 0.142.1 and 0.142.2 are bug-fix releases for it (`docs_raw/fastapi_release-notes.md` lines 8-26). The stack as pinned ran correctly [R]. The previous stable line is 0.141.1 (2026-07-29), not run.
- wavesurfer 8.0.0 is a rewrite of teardown/ownership; "The public `WaveSurfer` API, events and plugin constructors stay the same" (`meta/gh_ws_releases.json`, release 8.0.0).
- plotly.js 4.0.0 breaking changes that touch this page: colour parsing moved to culori (`hsv()` strings rejected; `rgb(255,0,0,0.5)` is now translucent); `xvals`/`yvals` of click-anywhere events return data values; **the "Upload to Cloud" mode-bar button is shown by default** (`meta/gh_plotly_releases.json`, release v4.0.0).

### 2.2 Pinned CDN URLs, sizes, SRI

Sizes: raw bytes / bytes on the wire (brotli from jsDelivr) [R: `cdn_check.tsv`]. Integrity values: SHA-384 of the exact bytes; the SHA-256 of the same local bytes equals the hash jsDelivr reports for the npm file [R: `cdn_sri.tsv` (previous run) and `sri_crosscheck.out` (recomputed this session, all rows `YES`)].

| Use | URL | Raw | Wire | `integrity` |
|---|---|---|---|---|
| **Plotly (recommended)** | `https://cdn.jsdelivr.net/npm/plotly.js-cartesian-dist-min@4.1.1/plotly-cartesian.min.js` | 1,500,041 | 500,661 | `sha384-zc4SwKObGL/W0M3RUI09UPWjlgIZHfbwMgcZO6713mRh78tfUmIQKhzCyE2LIiUg` |
| Plotly basic (smaller, not browser-tested) | `https://cdn.jsdelivr.net/npm/plotly.js-basic-dist-min@4.1.1/plotly-basic.min.js` | 1,191,749 | 400,932 | `sha384-N2HZsG+IG/3J8CwhGGYz/kmzZ0sprpPWwjhor9ZI4lxuf47i9DXK2/NDGxMaJiEb` |
| Plotly full (not needed) | `https://cdn.jsdelivr.net/npm/plotly.js-dist-min@4.1.1/plotly.min.js` | 4,815,814 | 1,410,481 | `sha384-AFNp2MtSm5/oZbEs/J19F/Ah57MEiVsoed8nE3fq2Wnccdl1u/EkyJ9XKKU8rt7+` |
| **wavesurfer core (UMD)** | `https://cdn.jsdelivr.net/npm/wavesurfer.js@8.0.1/dist/wavesurfer.min.js` | 51,958 | 15,306 | `sha384-cFoZUUrlVjbDowT5/idDYja9T/OY8JaecFDFEt6O/CHQxJjjQR440T5VhilWib4U` |
| **Regions plugin (UMD)** | `https://cdn.jsdelivr.net/npm/wavesurfer.js@8.0.1/dist/plugins/regions.min.js` | 21,448 | 6,937 | `sha384-Tk81r51AIztO5k+iOj/eOq9ZEGD2XVkPnZR8QVxzq1dkyEmsBSCjYpdCoeD/AZQ9` |
| **Timeline plugin (UMD)** | `https://cdn.jsdelivr.net/npm/wavesurfer.js@8.0.1/dist/plugins/timeline.min.js` | 7,610 | 3,051 | `sha384-2l5/6KGTIt5kr+AcoXrcOzSiDUedbqv1LlHsFtQ5/ABj0cbzhpA2w6bCvc4Ns2vk` |
| Record plugin (UMD, optional) | `https://cdn.jsdelivr.net/npm/wavesurfer.js@8.0.1/dist/plugins/record.min.js` | 11,305 | 3,621 | `sha384-Lnv7IgMrpndF140D6YYSElYbDQUA4CUThmTZWriA5/yyc0BPwr6xyDFjjW+szcL7` |
| wavesurfer core (ESM) | `https://cdn.jsdelivr.net/npm/wavesurfer.js@8.0.1/dist/wavesurfer.esm.js` | 51,732 | 15,216 | `sha384-SKSpButoOlphH9yzETl+/N3F8cBzn5WX5v+pY+f5RbbIyvJhENOiFRCEGvrmy6LO` |
| Regions (ESM) | `https://cdn.jsdelivr.net/npm/wavesurfer.js@8.0.1/dist/plugins/regions.esm.js` | 21,186 | 6,833 | `sha384-3PWIGXRyba/QSXPcfAPU2VeC8Gg3BKBSj4jpNngO8FhEE3dFntfuT8CZ02uoTlsk` |
| Timeline (ESM) | `https://cdn.jsdelivr.net/npm/wavesurfer.js@8.0.1/dist/plugins/timeline.esm.js` | 7,347 | 2,930 | `sha384-CdLwB+wbjTciJzBtfS4AkavUWJ8ZcOUjnDdlwmLYuQLt2iasTU0Nb3KArMl6TNgP` |
| Fallback: wavesurfer 7.12.12 core / regions / timeline (UMD, not browser-tested) | `https://cdn.jsdelivr.net/npm/wavesurfer.js@7.12.12/dist/{wavesurfer.min.js, plugins/regions.min.js, plugins/timeline.min.js}` | 41,962 / 16,576 / 6,057 | 12,503 / 5,128 / 2,278 | `sha384-NpDZywZ+3n6NCeya3JpL5NKUchUD3LjUMLgBQPZYe+jEmYsW7J8akPFUqx7vW7Wc` / `sha384-6CctlpeosREFSMF8O+4A7M3weKP2oWuAN3QgASJm2ASROAa9iuTqqiTdTCy/HBQl` / `sha384-RPC49fbdO1o+V3mW9B2RhcdTMDNWvUJPADHw5F/ZG/EbZxvgRMwOfX7bA7yCBCTZ` |

Recommended set total: 1,581,057 bytes raw, 525,955 bytes on the wire.

CDN facts [R: `cdn_headers_and_registry.out`]: jsDelivr answers `access-control-allow-origin: *` (required for SRI on a cross-origin script, MDN [S]), `cache-control: public, max-age=31536000, s-maxage=31536000, immutable`, `content-encoding: br`. `https://cdn.plot.ly/plotly-cartesian-4.1.1.min.js` serves byte-identical content (same hash) with `access-control-allow-origin: *`, gzip 497,143 bytes [R: `cdn_sri.tsv`, `cdn_check.tsv`].

Head of the page (classic scripts keep `<script integrity>` simple; order matters, see 2.4):

```html
<script defer src="https://cdn.jsdelivr.net/npm/plotly.js-cartesian-dist-min@4.1.1/plotly-cartesian.min.js"
        integrity="sha384-zc4SwKObGL/W0M3RUI09UPWjlgIZHfbwMgcZO6713mRh78tfUmIQKhzCyE2LIiUg" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/wavesurfer.js@8.0.1/dist/wavesurfer.min.js"
        integrity="sha384-cFoZUUrlVjbDowT5/idDYja9T/OY8JaecFDFEt6O/CHQxJjjQR440T5VhilWib4U" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/wavesurfer.js@8.0.1/dist/plugins/regions.min.js"
        integrity="sha384-Tk81r51AIztO5k+iOj/eOq9ZEGD2XVkPnZR8QVxzq1dkyEmsBSCjYpdCoeD/AZQ9" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/wavesurfer.js@8.0.1/dist/plugins/timeline.min.js"
        integrity="sha384-2l5/6KGTIt5kr+AcoXrcOzSiDUedbqv1LlHsFtQ5/ABj0cbzhpA2w6bCvc4Ns2vk" crossorigin="anonymous"></script>
<link rel="icon" href="data:,">
<script defer src="app.js"></script>
```

The hash values are verified; the `integrity` attribute itself was not exercised in a browser (the probe page injected scripts without it) [U for browser enforcement].

Which Plotly bundle [S: package READMEs, `PREVIOUS_RUN_condensed.md` lines 1443-1462]:

| Bundle | Trace modules | Wire size | Note |
|---|---|---|---|
| basic | `bar`, `pie`, `scatter` | 401 KB | enough for lines and steps; not browser-tested |
| **cartesian** | basic + `box`, `contour`, `heatmap`, `histogram*`, `image`, `scatterternary`, `violin` | 501 KB | browser-tested; `heatmap` leaves room for a spectrogram/MFCC panel |
| full | 46 trace types incl. `scattergl`, maps, 3D | 1,410 KB | only needed for WebGL; not needed here |

`scattergl` is not in basic/cartesian. That is acceptable: WebGL traces have no area fills and a per-page context limit (plotly performance doc [S]); SVG `scatter` lines are simplified by default (`line.simplify`, default `true`: "Simplifies lines by removing nearly-collinear points" [S: schema types line 7270]).

### 2.3 plotly.js 4.1.1 API facts used by the page

Source for all rows unless noted: type declarations shipped in the package, `vendor/plotly4/types/*.d.ts` (fetched from `https://cdn.jsdelivr.net/npm/plotly.js-dist-min@4.1.1/...`).

| Need | API | Status |
|---|---|---|
| Global | UMD wrapper ends with `window.Plotly = Plotly`; no ESM build in the dist packages | [S] bundle head/tail |
| Draw / update | `Plotly.newPlot(gd, data, layout, config)`, `Plotly.react(gd, data, layout, config)` ("only changed attributes are reapplied"), `Plotly.relayout(gd, update)`, `Plotly.restyle`, `Plotly.purge`, `Plotly.Plots.resize(gd)` | [S] `src_types_core_api.d.ts`; `react` and `relayout` used in the probe [R] |
| `react` data detection | new array identity, or change `layout.datarevision` | [S] schema line 16041 |
| Keep zoom across redraws | `layout.uirevision` (unchanged value keeps user zoom) | [S] schema line 16540 |
| Stacked rows, shared x | ONE `xaxis` + `yaxis`, `yaxis2`, `yaxis3` with `domain: [lo, hi]`; `xaxis.anchor: "y3"` (bottom row) | [R] probe figure, `static/probe.js` lines 110-122 |
| One tooltip for all rows | `hovermode: "x unified"` + `hoversubplots: "axis"` ("also include stacked subplots using the same axis"). Requires the rows to share the same x-axis object, not `matches` | [S] schema line 16212; [R] hover text listed pitch, energy and rate rows together |
| Shaded region ("vrect") | `layout.shapes[]`: `{type:"rect", xref:"x", yref:"y2 domain", x0, x1, y0:0, y1:1, fillcolor, line:{color,width,dash}, layer:"below", label:{text, textposition:"top left", font, padding}}`. `yref:"paper"` spans all rows. `layer`: `below` \| `between` \| `above` (default `above`) | [S] schema lines 15462-15623; [R] 5 shapes and 4 labels rendered |
| Click | `gd.on("plotly_click", ev)`: `ev.points[]` (`curveNumber`, `pointIndex`, `x`, `y`, `customdata`), `ev.event`, `ev.xPixel`, `ev.yPixel`. With `layout.clickanywhere: true` the event also fires off-trace and carries `ev.xvals`/`ev.yvals` in data units (added 3.5.0; data values since 4.0.0) | [S] `events.d.ts`, schema line 16007, release notes; [R] click on an empty band area gave `xvals`, `xPixel: 258`, flaw hit |
| Hover | `plotly_hover` (`xvals`, `yvals`, `points`), `plotly_unhover`; `layout.hoveranywhere` | [S] |
| Range changes | `plotly_relayout` with keys `xaxis.range[0]`, `xaxis.range[1]`, `xaxis.autorange` | [S] `events.d.ts` lines 155-168 |
| Fast highlight | `Plotly.relayout(gd, {"shapes[2].line.width": 2, "shapes[2].fillcolor": ...})` | [R] shape 3 width 2, shape 1 width 1 after selection |
| Tooltip text | per-trace `hovertemplate` with `%{y:.2f}`, `%{customdata[0]:.2f}`, `<extra></extra>`; `customdata` is an array per point | [S]; [R] "Baseline : 2.66 st (baseline 5.98s / yours 5.24s)" |
| Gaps | `connectgaps: false` (default): `null` y values break the line (unvoiced F0, pauses) | [S] schema line 7126 |
| Step line | `line.shape`: `linear` \| `spline` \| `hv` \| `vh` \| `hvh` \| `vhv` | [S] schema line 7268 |
| Config defaults to override | `responsive` default **false**; `displaylogo` default true; `showSendToCloud` default **true** with `plotlyServerURL` `https://cloud.plotly.com/newchart` ("will (after a confirmation step) send chart data to an external server"); `doubleClickDelay` default 500 ms (was 300 before 4.1.0) | [S] schema lines 16703-16880; [R] default mode bar contains "Share chart...", configured one does not |
| Text safety | Plotly text accepts a whitelist of pseudo-HTML tags (`sup, sub, s, u, b, i, a, span, em`, `<br>`); link protocols limited to `http:`, `https:`, `mailto:` | [S] pinned bundle, constants `$P` and `jP` |

Config used and verified [R]: `{responsive: true, displaylogo: false, showSendToCloud: false, modeBarButtonsToRemove: ["select2d", "lasso2d", "toImage"], doubleClick: "reset"}` leaves exactly: Zoom, Pan, Zoom in, Zoom out, Autoscale, Reset axes.

Performance with ~6 traces x 3000 points: **not measured.** The previous run's timing step (`browser_test/run.mjs` step 6: 5 traces x 12,750 points) was cut off when the browser was closed; `results.json` has no `perf` key. What exists: page load to both waveforms decoded took 993 ms with 5 data traces x ~1000 points plus 4 helper traces, CDN fetches included [R]. Source guidance: Plotly Express switches to WebGL above 1,000 rows by default and WebGL "may not be possible ... more than 8 WebGL-involving figures on the same page" (`docs_raw/plotly_py_performance.md` lines 144, 184) [S]. Keep the knob: one server constant `DISPLAY_HOP_S` (section 7.3).

### 2.4 wavesurfer.js 8.0.1 API facts used by the page

Source: `vendor/ws8/dist/*.d.ts`, `vendor/ws8/package.json`, `vendor/ws8/README.md` and the pinned bundles in `vendor/`.

| Need | API | Status |
|---|---|---|
| UMD globals | core sets `WaveSurfer`; each plugin does `WaveSurfer = WaveSurfer \|\| {}; WaveSurfer.Regions = ...` (also `.Timeline`, `.Record`, `.Hover`, `.Zoom`). **Load the core before the plugins**, otherwise the core overwrites the plugin object | [S] bundle heads, `PREVIOUS_RUN_condensed.md` lines 677-690; [R] `typeof WaveSurfer.Regions === "function"` |
| ESM | `import WaveSurfer from ".../dist/wavesurfer.esm.js"`, `import Regions from ".../dist/plugins/regions.esm.js"`; the ESM files are self-contained (0 `import` statements, `export { X as default }`) | [S] vendored ESM files |
| Create | `WaveSurfer.create({container, url, height, waveColor, progressColor, cursorColor, cursorWidth, normalize, peaks, duration, media, backend, fetchParams, plugins, sampleRate, interact, dragToSeek, ...})`. Defaults: `waveColor "#999"`, `progressColor "#555"`, `cursorWidth 1`, `fillParent true`, `interact true`, `dragToSeek false`, `sampleRate 8000` (decode rate for drawing only), backend `MediaElement` | [S] `wavesurfer.d.ts`, bundle defaults |
| Plugins | `const regions = ws.registerPlugin(WaveSurfer.Regions.create())`. In v8 a plugin's API object (`addRegion`, ...) is attached when the plugin is initialised on an instance, so register (or pass in `plugins:`) before calling plugin methods | [S] bundle tail; [R] |
| Regions | `regions.addRegion({id, start, end, color, content, drag:false, resize:false})`, `getRegions()`, `clearRegions()`; region: `setOptions({color, start, end, ...})`, `play(stopAtEnd?)`, `remove()`. `start === end` renders a *marker* (`part="marker <id>"`) instead of a region. A string `content` is inserted with `textContent` | [S] `regions.d.ts`, regions bundle (`setPart`, `setContent`) |
| Region events | plugin: `region-clicked (region, MouseEvent)`, `region-double-clicked`, `region-in`, `region-out`, `region-created`, `region-updated`, `region-removed` | [S]; `region-clicked` [R] |
| Timeline | `WaveSurfer.Timeline.create({height, container, insertPosition, timeInterval, primaryLabelInterval, formatTimeCallback, ...})` | [S] `timeline.d.ts`; loaded [R] |
| Play a span | `await ws.play(start, end)`: seeks to `start`, plays, pauses when `currentTime >= end` and snaps to `end` (checked every animation frame and on the media `timeupdate` event). `setTime()` cancels a pending stop | [S] bundle (`play`, `stopAtPosition`); [R] span 13.30-16.30 s ended at 16.30 after 3,244 ms wall time; span 14-17 s ended at 17.00 after 3,218 ms |
| Transport | `setTime(s)`, `seekTo(0..1)`, `pause()`, `playPause()`, `skip(s)`, `stop()`, `getCurrentTime()`, `getDuration()`, `isPlaying()`, `setPlaybackRate(rate, preservePitch?)`, `setOptions(partial)`, `load(url, peaks?, duration?)`, `destroy()` | [S] |
| Events | `ready (duration)`, `decode (duration)`, `loading (percent)`, `play`, `pause`, `finish`, `timeupdate (t)`, `seeking (t)`, `interaction (t)`, `click (relX, relY)`, `error (Error)`, `destroy`; `on()` returns an unsubscribe function; `once()`, `un()` | [S] `wavesurfer.d.ts`, `event-emitter.d.ts`; `decode`, `timeupdate`, `pause` [R] |
| Loading model | without `peaks`: one `fetch` of the whole file -> Blob -> blob URL on the media element -> `decodeAudioData` at 8 kHz for the drawing. With `peaks` + `duration`: no fetch, the media element streams the URL (Range requests) | [S] bundle `loadAudio`, `setSrc`; README "Does wavesurfer support large files?" |
| Styling | rendered in a Shadow DOM; style with `::part(region)`, `::part(cursor)`, `::part(region-content)` | [S] README |
| v8 behaviour to respect | `destroy()` is final (create a new instance; or keep the instance and call `load()` again); a superseded `load()` rejects with `AbortError` (catch it); `getMediaElement()` may return `null` | [S] release notes 8.0.0 |
| Record plugin (optional) | `WaveSurfer.Record.create({mimeType, audioBitsPerSecond, ...})`, `startRecording(constraints)`, `stopRecording()`, event `record-end (blob)`; 8.0.1 reverted the default `mediaRecorderTimeslice` to `undefined` | [S] `record.d.ts`, release notes 8.0.1 |

Do not use the README's unpinned form `https://unpkg.com/wavesurfer.js@8` (floating major).

### 2.5 FastAPI / Starlette / uvicorn / python-multipart upload APIs

Read from the released wheels (`wheels/*.whl`, SHA-256 equal to PyPI's) and the docs at tag 0.142.2 (`docs_raw/fastapi_*.md`).

| Fact | Evidence |
|---|---|
| Uploads need `python-multipart` installed (not a FastAPI hard dependency) | [S] `fastapi_request-files.md` line 7; METADATA lists it only under extras |
| `async def f(audio: UploadFile, transcript: str = Form(...))` (or `Annotated[UploadFile, File()]`); `UploadFile` has `filename`, `content_type`, `size`, `headers`, `file` (a `SpooledTemporaryFile`), async `read/write/seek/close`; in a plain `def` endpoint use `audio.file.read()` | [S] docs; `fastapi/datastructures.py`; [R] the probe endpoint is a plain `def` |
| Starlette's multipart parser: `max_files=1000`, `max_fields=1000`, `max_part_size=1 MB` **for non-file fields only**; file parts go to `SpooledTemporaryFile(max_size=1 MB)` with **no size limit**; FastAPI calls `request.form()` with these defaults | [S] `starlette/formparsers.py` lines 149-245, `fastapi/routing.py` line 443 |
| `FileResponse` sets `accept-ranges: bytes`, answers `Range` with 206 (single and multi-range) and 416 | [S] `starlette/responses.py` lines 298-470; [R] `206`, `content-range: bytes 1000-1999/640078` |
| `StaticFiles(directory, html=True)` serves `index.html`, rejects paths that leave the directory (`os.path.commonpath` on the real path) | [S] `starlette/staticfiles.py` lines 160-175; [R] traversal attempts -> 404 |
| `JSONResponse.render` uses `json.dumps(..., allow_nan=False)`: a `NaN` in the payload raises `ValueError` | [S] `starlette/responses.py` lines 196-203 |
| `GZipMiddleware(minimum_size=500, compresslevel=9)` skips `audio/*`, `text/event-stream` and 206 responses | [S] `starlette/middleware/gzip.py` lines 13-27, 112-118 (not run) |
| Native SSE exists since FastAPI 0.135.0: `from fastapi.sse import EventSourceResponse, ServerSentEvent`, `response_class=EventSourceResponse` + `yield`; keep-alive comment every 15 s | [S] `fastapi/sse.py`, `fastapi_server-sent-events.md` (not needed, see 4.3) |
| New since 0.138.0: `app.frontend("/", directory="static")` serves a static front end after all path operations; built on `StaticFiles` (`follow_symlink=False`) | [S] `fastapi_frontend.md`, `fastapi/routing.py` lines 1942-2060 (not run) |
| FastAPI 0.132.0: JSON bodies require a JSON `Content-Type` by default (`strict_content_type`); 0.129.0 dropped Python 3.9; 0.131.0 deprecated `ORJSONResponse`/`UJSONResponse` | [S] release notes |
| uvicorn 0.54.0 defaults: `--host 127.0.0.1`, `--port 8000`, `--workers` = `$WEB_CONCURRENCY` or 1, `--proxy-headers` on, `--forwarded-allow-ips` = `$FORWARDED_ALLOW_IPS` or `127.0.0.1,::1`, `--timeout-keep-alive 5` | [S] `uvicorn/main.py`, `uvicorn/config.py` |

Static serving choice: `app.mount("/", StaticFiles(directory="static", html=True), name="static")` registered **after** the API routes is the run-verified form [R]. `app.frontend()` is the newer equivalent without the ordering constraint, source-verified only.

---

## 3. Q2 - Two timelines: which axis

### 3.1 The mapping

Anchors `(B_k, P_k)`, `k = 0..K`: `(0, 0)`, every aligned word start and end in both recordings, `(dur_b, dur_p)`; both sequences non-decreasing.

- baseline -> participant: `f(t) = P_k + (t - B_k) * (P_{k+1} - P_k) / (B_{k+1} - B_k)` for `B_k <= t <= B_{k+1}`; inverse `g` likewise.
- zero-length baseline segment (`B_{k+1} = B_k`, `P_{k+1} > P_k`: the participant inserted a pause): `f` jumps, `g` is constant on `[P_k, P_{k+1}]`. Symmetric for a removed pause.
- local tempo ratio of segment `k`: `r_k = (B_{k+1} - B_k) / (P_{k+1} - P_k)`; plot `log2 r_k` (`+1` = twice as fast, `-1` = half speed, 0 = same). This slope is the only place where pacing information survives any warp.

A 9-line binary-search `interp(x, xs, ys)` that clamps at the ends and handles zero spans is in `static/probe.js` lines 10-18; it ran in the browser test [R].

### 3.2 Comparison

| Criterion | (a) participant warped onto baseline time | (a') baseline warped onto participant time | (b) word-index axis | (c) two stacked true-time tracks |
|---|---|---|---|---|
| Design class (Gleicher et al. 2011) | superposition after registration | superposition after registration | superposition after registration | juxtaposition |
| Curves share one scale (difference visible as vertical gap) | yes | yes | yes | no |
| Participant's true timestamps readable on the axis | no | **yes** | no | yes |
| Band width equals the flaw's true duration | no | **yes** | no | yes |
| Click on chart maps straight to participant audio | via map | **direct** | via word | direct |
| Pause inserted by the participant | zero width (needs a marker) | true width | zero width | true width |
| Pause dropped by the participant | true (baseline) width | zero width | zero width | only in the baseline track |
| Pacing visible in the curves | no; needs the rate row | no; needs the rate row | no; needs the rate row | yes, as horizontal offsets that are hard to quantify |
| Reference stays fixed while stepping through a severity gradient | **yes** | no | **yes** | - |
| Shares the x axis with the participant waveform | no | **yes** | no | yes |
| Matches the detector's unit (per-word statistics) | partly | partly | exactly | no |
| A wrong alignment shows up as | distorted participant curve | distorted baseline curve | nothing | nothing |

Source basis [S: Gleicher, Albers, Walker, Jusufi, Hansen, Roberts, "Visual comparison for information visualization", Information Visualization 10(4), 2011, preprint pages 4, 6, 10, 11, 13]:

- Figure 1 uses exactly this case (two time series): juxtaposition, superposition, explicit encoding as difference, explicit encoding as a time-warp curve.
- "juxtaposition relies on memory to hold the multiple items and make connections; superposition may make comparison more efficient by keeping information in spatially local correspondence; explicit encodings parallel more analytic comparison".
- "superposition may use computation to find a common spatialization (e.g., an alignment or registration) between data objects ... used to define the space in which the objects themselves are shown."
- "registration can be used to remove inconsequential differences so that mental alignment of basic forms need not be done by the viewer".
- "Decontextualization is one reason why purely explicit encoding designs are rarely used alone" and "an explicit encoding ... may be superimposed on top of a visualization encoding of the objects".

Javed, McDonnel, Elmqvist (IEEE TVCG 16(6):927-934, 2010): shared-space line graphs are more efficient for comparisons over small visual spans; split-space techniques for large spans [S, abstract as returned by search; full text not read].

### 3.3 Decision

- **Main chart: (a') participant time, baseline warped onto it.** The brief scores the accuracy of flaw timestamps in the participant's recording; with this axis the band coordinates, the tick labels and the click position are those timestamps.
- **Toggle to (a) baseline time** for the gallery: when stepping through severity variants of the same speech the reference curve and word positions stay put. The probe implemented the toggle by swapping which x arrays go through the map; it returned range `[0, 20]` and band coordinates `[4, 8]` in baseline mode [R].
- **(c) is realised by the two wavesurfer strips**, each on its own true clock, with the flaw regions drawn at `flaw.b` and `flaw.p` respectively [R: 4 regions in each strip].
- **(b) is realised by the transcript panel** (one chip per word), not by a chart axis.
- **Explicit encoding of the delta:** the rate row (`log2` tempo ratio per word, step line) and the per-flaw numbers table.

How the page shows the participant's true timestamps for each flaw, in every mode [R unless noted]:

1. each flaw carries `p: [start, end]` and `b: [start, end]` computed on the server from word boundaries, in each recording's own seconds;
2. the flaw list button and the explanation panel print both ("Participant 13.30-16.30 s | Baseline 14.00-17.00 s");
3. the participant waveform region sits on true participant time;
4. every tooltip row carries both times through `customdata` ("baseline 5.98s / yours 5.24s");
5. in the default mode the x axis itself is participant time; on toggle the bands switch from `flaw.p` to `flaw.b`.

Details to implement that the probe did not cover [U]: after warping a series, insert a `null` where two consecutive warped x values are more than `0.25 s` apart, so a participant-only pause is a gap in the baseline line instead of a straight segment across it.

---

## 4. Q3 - Required capabilities, implementation notes

### 4.1 Upload audio + transcript

- Native form, one `fetch`: `<input type="file" name="audio" accept="audio/*,.wav,.mp3,.m4a,.ogg,.webm,.flac" required>`, `<textarea name="transcript" maxlength="20000">`, plus a second file input that only fills the textarea client-side (`textarea.value = await file.text()`), so the server receives one `transcript` field.
- `fetch("api/analyze", {method: "POST", body: new FormData(form)})` -> `{job_id}` [R: endpoint shape in `probe_app.py`].
- Use relative URLs everywhere (`api/...`, `gallery/...`), so the same page works at `/`, under a GitHub Pages sub-path and inside a Space.

### 4.2 Choose a bundled baseline or upload one

- `<select name="baseline_id">` filled from `gallery/index.json` (section 7.4); choosing one pre-fills the transcript (read-only until "edit" is ticked). A last option "Upload my own baseline" reveals `<input type="file" name="baseline_audio">`; then the transcript is required.
- Server rule: exactly one of `baseline_id` / `baseline_audio`; 422 otherwise.

### 4.3 Processing progress

- `POST api/analyze` returns immediately; the page polls `GET api/jobs/{id}` every 500 ms and renders `<progress max="1" value="0.4">` plus the stage name in a `role="status"` element. Stages: `queued`, `decode`, `align`, `features`, `compare`, `explain`, `done` / `error`. Verified trace: `decode 0.1 -> align 0.4 -> features 0.7 -> compare 0.9 -> done 1.0` [R: `probe_backend.out` section 2].
- Polling instead of SSE/WebSocket: every request is short (no proxy timeout to reason about), the job state is a dict lookup, and it is already verified. FastAPI's native SSE is available if polling ever proves too coarse [S].
- Run analysis jobs through one `ThreadPoolExecutor(max_workers=1)` (the probe started one thread per job) and start uvicorn with `--workers 1`: the job table is in memory. `# ponytail: in-memory jobs + one worker; move to a queue if this runs multi-process.`

### 4.4 Time-series overlay with shaded flaw regions

Figure structure (run-verified with three rows; the pause row is an addition) :

| Row | Content | Trace form |
|---|---|---|
| Pitch | baseline + participant, semitones relative to each speaker's median | 2 `scatter` lines, `null` where unvoiced |
| Energy | baseline + participant, dB relative to each speaker's median | 2 `scatter` lines |
| Pace | `log2` tempo ratio per word (what the detector thresholds) | 1 step line (`line.shape: "hvh"`), zero line on |
| Pauses | silent intervals of each recording as two thin horizontal tracks | 2 `scatter` traces, `x: [t0, t1, null, ...]`, `y` constant, `line.width: 6` [U] |

- Layout skeleton [R]: `hovermode: "x unified"`, `hoversubplots: "axis"`, `clickanywhere: true`, `dragmode: "zoom"`, y axes `fixedrange: true`, x axis zoomable, `height` 460 for three rows (about 560 for four), `margin: {l: 56, r: 16, t: 28, b: 40}`.
- Bands: one `rect` shape per flaw, drawn only in the row of its dimension (`yref: "<axis> domain"`), `layer: "below"`. Type is encoded by row position, so hue is free for severity and bands of different types never overlap [R].
- A zero-length span (for example an inserted pause seen on the baseline axis) is drawn as `[t - 0.1, t + 0.1]` [R: `flaw2: [11.9, 12.1]`].
- Selecting a flaw additionally zooms: `Plotly.relayout(gd, {"xaxis.range": [p0 - 3, p1 + 3]})`; double-click resets (`doubleClick: "reset"`) [S for the API; not run].
- Playback cursor: an absolutely positioned 1 px `<div>` over the chart, moved on every wavesurfer `timeupdate`: `left = plot.left - host.left + (x - r0) / (r1 - r0) * plot.width`, with `[r0, r1] = gd.layout.xaxis.range` and `plot` = bounding box of the first `.nsewdrag` rect; hidden when outside the range. No Plotly call per frame [R: cursor shown, baseline 17.00 s mapped to x = 16.30]. `.nsewdrag` is an internal class name; the pinned version keeps it stable.

### 4.5 Click a flaw -> explanation + play that span of both recordings

One function `selectFlaw(id, {play})` called from three places: chart click, waveform region click, flaw list button [R: `static/probe.js` lines 132-158, 177, 213-228].

- Chart: `plotly_click` -> `x = ev.xvals?.length ? +ev.xvals[0] : +ev.points[0].x` -> first flaw whose span (in the current axis mode, widened to at least 0.2 s) contains `x`.
- Waveform: `regions.on("region-clicked", (region, e) => { e.stopPropagation(); selectFlaw(region.flaw.id, {play: true}); })`.
- Effect: `Plotly.relayout` on shape line/fill only (no data redraw), `aria-pressed` on the list buttons, explanation panel filled with `textContent`, both players `setTime(span[0])`.
- Playback: participant span first, then the baseline span, never both at once: `await ws.play(start, Math.max(end, start + 0.3))`, then wait for the `pause` event, then the other player; a counter token cancels the sequence when another flaw is clicked [R].
- The second `play()` happens outside the click handler. Browsers allow that once "the user has interacted with the site", but "the exact situations ... vary from browser to browser", and a blocked `play()` rejects with `NotAllowedError` [S: MDN autoplay guide]. The test browser ran with autoplay restrictions disabled. Therefore put two explicit buttons in the panel ("Play yours 13.30-16.30", "Play baseline 14.00-17.00") and treat the automatic sequence as a convenience; catch the rejection.
- Explanation panel content: heading `#3 pitch - moderate`; both true spans; the server's sentence; a small table from the structured fields (measure, baseline value, participant value, delta or ratio, z, threshold); the suggested fix.

### 4.6 Transcript with highlighted words that seek the audio

- One `<span data-i="17">` per word inside one container, one delegated `click` listener: `players.p.setTime(words[i].p[0]); players.b.setTime(words[i].b[0])`.
- Words inside a flaw get a class per severity; the run of words of one flaw is wrapped in a focusable element (`tabindex="0"`, `role="button"`, Enter/Space -> `selectFlaw`).
- During playback: on `timeupdate`, binary-search the word by start time in the playing recording's clock and move an `aria-current="true"` marker; `scrollIntoView({block: "nearest"})`.
- Low-confidence alignments (`ok: false`) are shown dimmed; they are not used as map anchors.
- Words and explanations are user-derived text: `textContent` only.

### 4.7 Rubric score cards

- One hero number (overall) and one tile per rubric dimension: value, `/ max`, a native `<meter min="0" max="20" value="11">`, the number of flaws, and a one-line reason. Clicking a tile filters the flaw list to that dimension.
- Scores are stat tiles, not charts.

### 4.8 Gallery across the severity gradient (no upload needed)

- Static files produced by the Kaggle build: `gallery/index.json`, `gallery/results/<id>.json`, `gallery/audio/<id>.wav` (schema in 7.4).
- UI: a `<select>` for the speech, then one button per variant ordered from most to least severe, each showing its label and overall score, plus the untouched original as the "no flaw" case. Selecting one does `render(await (await fetch(url)).json())`.
- The first gallery example is loaded on page start, so the page never opens empty.
- Because DSP-edited examples have known edit spans, the result JSON for gallery items carries `truth[]`; draw each as a 4 px line at the top edge of the corresponding row and print overlap (IoU) next to the flaw in the list. It shows temporal-grounding accuracy directly. [U: drawing form not run.]
- If `fetch("api/health")` fails, hide the upload card and show how to start the back end; the gallery keeps working.

---

## 5. Q4 - Dataviz and usability

### 5.1 Palette (validated numerically)

Validator: OKLab distance x100 under Machado-Oliveira-Fernandes 2009 simulation, plus WCAG contrast; script from the dataviz skill; outputs in `palette_check.out`, `palette_alpha.out` [R].

| Role | Light | Dark | Evidence |
|---|---|---|---|
| Page / chart surface | `#f9f9f7` / `#fcfcfb` | `#0d0d0d` / `#1a1a19` | palette reference |
| Primary / secondary ink / muted | `#0b0b0b` / `#52514e` / `#898781` | `#ffffff` / `#c3c2b7` / `#898781` | palette reference |
| Gridline | `#e1e0d9` | `#2c2c2a` | palette reference |
| **Baseline line** (reference recedes) | `#52514e` | `#c3c2b7` | contrast 7.73:1 / 9.72:1 |
| **Participant line** (subject) | `#2a78d6` | `#3987e5` | contrast 4.30:1 / 4.79:1 |
| Baseline vs participant separation | worst case under protan/deutan/tritan: 18.9 | 21.0 | target >= 8 |
| Severity minor / moderate / severe | `#fab219` / `#ec835a` / `#d03b3b` (same in both modes) | | status palette |

Measured consequences:

- A blue/orange pair also separates well (24.7 / 26.8) but orange is only 3.12:1 on the light surface; gray for the reference keeps the participant as the single accent.
- **Severity cannot be carried by band colour.** The three washes composited on the surface differ by only 3.6-4.4 (light) and 0.6-4.3 (dark) even with full colour vision.
- Band opacity ceiling: at alpha `<= 0.20` the participant line keeps `>= 3.12:1` against every band in both modes; at 0.24 it drops to 2.82:1 (dark, minor) and at 0.32 to 2.68:1 (light, severe). Use `0.16` normal, `0.20` selected.
- Minor and moderate hues are 1.79:1 and 2.57:1 against the light surface: not usable as the only band outline.

### 5.2 Flaw regions without clutter

| Attribute | Encoding |
|---|---|
| Type | the row the band is drawn in |
| Identity | label `#3` (top-left of the band; type is implied by the row) and the same number in the list, transcript and waveform region |
| Severity | wash hue at alpha 0.16 **and** outline dash: `dot` minor, `dash` moderate, `solid` severe, outline in secondary ink (7.73:1); severity word in the list |
| Selected | outline primary ink, width 2, alpha 0.20 [R] |
| Ground truth (gallery) | 4 px ink line on the row's top edge |

WCAG basis [S: `https://www.w3.org/TR/WCAG22/`]: 1.4.1 "Color is not used as the only visual means of conveying information"; 1.4.11 non-text contrast "at least 3:1 against adjacent color(s)".

### 5.3 Tooltips carrying the mathematical delta

- Unified tooltip: one row per trace with value and unit and both true times through `customdata` [R]. Put the delta on the participant rows: `customdata = [t_baseline, t_participant, delta, z]`, template `%{y:.2f} st (delta %{customdata[2]:+.2f}, z %{customdata[3]:+.1f})`. The `+` format flag was fixed in 4.0.0 [S] and rendered correctly ("log2 rate +0.68") [R].
- One invisible helper trace per flaw (`opacity: 0`, points only inside the band) adds the line `#1 pace (severe)` to the tooltip while the pointer is inside a band [R].
- Everything a tooltip shows is also in the flaw panel table (tooltips are not reachable by keyboard).

### 5.4 Light and dark

- Colours are CSS custom properties on `:root`; dark values under `@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])` and again under `:root[data-theme="dark"]` (`static/probe.css` lines 2-23).
- Plotly and wavesurfer need literal colours: read them with `getComputedStyle(document.documentElement).getPropertyValue("--participant")` when building the figure; on theme change call the same `draw()` (`Plotly.react`) and `ws.setOptions({waveColor, progressColor, cursorColor})`.
- A Hugging Face Space loads the app as `https://<sub>.hf.space/?__theme=system` [S: Space page markup, `docs_raw/hf_space_page_fastapi_t5.html`]; honour `__theme=light|dark` by setting `data-theme`.
- The dark render and the 390 px phone render were scripted but not reached before the run was stopped [U].

### 5.5 Keyboard and screen readers

- Flaw list = native `<button aria-pressed>` elements; Tab, Enter and Space work with no code; Arrow Up/Down move focus (9 lines) [R: Enter selected #1, ArrowDown + Space selected #2].
- The Plotly chart is not keyboard-operable; the flaw list, the numbers table and the transcript are its equivalents (2.1.1 Keyboard).
- Global keys on the page: Space play/pause the participant, Left/Right `skip(-2)` / `skip(2)`.
- `aria-live="polite"` on the explanation panel [R], `role="status"` on the progress text, `role="alert"` on errors (4.1.3 Status Messages) [S].
- `:focus-visible` outline 2 px; targets at least 24 x 24 CSS px (2.5.8) [S].

### 5.6 Responsive

- CSS grid `minmax(0, 1fr) 320px`, one column below 860 px; `config.responsive: true` (default is false) [S]; wavesurfer fills its container (`fillParent` default true) [S].
- Give the waveform strips the same left/right inset as the Plotly margins (56 px / 16 px) so the participant strip lines up with the chart at full range [R: `probe.css` line 32].
- Reflow target: no two-dimensional scrolling at 320 CSS px (1.4.10) [S]. Not tested [U].

### 5.7 States

| State | What the page shows |
|---|---|
| First load | first gallery example rendered |
| Back end absent | upload card replaced by a one-line note; gallery works |
| Uploading / analysing | previous result stays visible at reduced opacity; `<progress>` + stage name; submit disabled |
| HTTP 413 | "File is larger than 50 MB." |
| HTTP 415 | "Unsupported audio. Use wav, mp3, m4a, ogg, flac or webm." [R wording] |
| HTTP 422 | "Transcript empty or too long." / field missing |
| Job `error` | the server's message: "Audio longer than 180 s", "Audio shorter than 1 s", "Could not decode audio" [R], alignment failure text |
| Job id unknown (server restarted) | "This analysis is no longer available. Upload again." |
| No flaws found | score cards + "No flaw regions above threshold" and the thresholds used |
| Audio load error | wavesurfer `error` event -> inline message; chart remains usable |

---

## 6. Q5 - Uploads

### 6.1 Formats and decoding

All seven decoded to 16 kHz mono PCM through the endpoint [R: `probe_backend.out` section 1, ffmpeg 6.1.1]:

| Upload | Magic bytes checked | Forced demuxer | Decoded duration (20.000 s source) |
|---|---|---|---|
| WAV | `RIFF....WAVE` | `wav` | 20.0 |
| MP3 | `ID3` or MPEG frame sync | `mp3` | 20.0 |
| Ogg Vorbis / Ogg Opus | `OggS` | `ogg` | 20.0 / 20.0 |
| M4A (AAC) | `ftyp` at offset 4 | `mov` | 20.015625 |
| WebM (Opus) | `1A 45 DF A3` | `matroska` | 20.0 |
| FLAC | `fLaC` | `flac` | 20.0 |

Decode command [R]:

```
ffmpeg -nostdin -hide_banner -v error -f <demuxer> -i <upload> -map 0:a:0 -vn -sn -dn \
       -ac 1 -ar 16000 -c:a pcm_s16le -t <MAX_SECONDS + 1> -y <job_id>.wav
```

run with `subprocess.run([...], capture_output=True, timeout=60)` (argument list, no shell), then the duration is read with the stdlib `wave` module.

Rule that follows from the M4A row: **analyse and play the same decoded WAV.** Lossy containers shift or pad the timeline (AAC here: +15.6 ms), so never play the user's original file against analysis timestamps. Serve `<job_id>.wav` back through `FileResponse` [R: 206 Range].

Gallery audio: WAV (16 kHz mono 16-bit = 1.92 MB per minute) is what the browser test decoded [R]. FLAC is lossless ("the decompressed audio is identical to the original", 40-50 % smaller, Chrome yes / Firefox 51 / Safari 11 [S: MDN audio codecs]) if repository size matters; not browser-tested here.

### 6.2 Limits

| Limit | Value | Basis |
|---|---|---|
| Request body | 50 MB (`52_428_800`) | mechanism verified with a 25 MB cap [R]; 180 s of 48 kHz 16-bit stereo WAV is 34.6 MB, so 25 MB would reject ordinary WAVs (arithmetic) |
| Decoded duration | 1 s <= d <= 180 s | [R] 255 s speech -> "Audio longer than 180 s" |
| Transcript | 20,000 characters, non-blank | [R] blank -> 422; Starlette caps a form field at 1 MB [S] |
| ffmpeg wall time | 60 s | probe value |
| Concurrent analyses | 1 | single executor |

### 6.3 Security basics

| Risk | Control | Evidence |
|---|---|---|
| Unbounded upload fills the disk (Starlette spools file parts with no limit) | pure-ASGI middleware: reject when `Content-Length` exceeds the cap, and count bytes in `receive()` for chunked bodies | [S] parser source; [R] 413 in 0.00 s with `Content-Length`, 413 for a chunked 30 MB body, 0 temp files left |
| ffmpeg format probing on hostile input (playlist formats that reference other files or URLs; CVE-2016-1897/1898 class) | sniff magic bytes, accept only the six containers, pass `-f <demuxer>` so ffmpeg never probes | [R] an `#EXTM3U` playlist named `.mp3` -> 415; [S] NVD CVE-2016-1897 |
| Path traversal / hostile file names | storage name is a server-generated UUID; the client `filename` is never used; audio is looked up by job id in a dict | [R] `..%2f` requests -> 404; upload named `../../evil.wav` wrote nothing outside the work directory |
| Static file escape | `StaticFiles` real-path check | [S], [R] |
| Hung or runaway decode | `timeout=60`, `-t`, `-nostdin`, duration check | [R] |
| Temp files | the raw upload is deleted in `finally`; decoded WAVs and results live in one work directory that is swept (delete entries older than 1 h) when a new job is created | deletion [R]; sweep [U] |
| XSS through transcript text | DOM insertion with `textContent` only; wavesurfer region `content` strings are inserted with `textContent`; Plotly text is limited to a tag whitelist and http/https/mailto links | [S] pinned bundles |
| Chart data leaving the page | `showSendToCloud: false` | [S], [R] |
| CPU exhaustion | one analysis at a time; `--workers 1` | design |

The ASGI middleware and the sniffer are in `probe_app.py` lines 29-78 [R]; copy them as they are.

### 6.4 Optional in-browser recording

Native API, no plugin needed:

```js
const stream = await navigator.mediaDevices.getUserMedia(
  {audio: {autoGainControl: false, noiseSuppression: false, echoCancellation: false}});
const type = ["audio/webm;codecs=opus", "audio/mp4", "audio/ogg;codecs=opus"].find(t => MediaRecorder.isTypeSupported(t));
const rec = new MediaRecorder(stream, type ? {mimeType: type} : {});
const chunks = []; rec.ondataavailable = e => chunks.push(e.data);
rec.onstop = () => { stream.getTracks().forEach(t => t.stop());
  form.set("audio", new Blob(chunks, {type: rec.mimeType}), "recording"); };
rec.start();   // rec.stop() on the second click
```

- `MediaRecorder`: Chrome 47, Firefox 25, Safari 14.1 [S: MDN browser-compat-data]. Whatever container the browser produces (WebM, Ogg, MP4) is covered by the server's sniffing.
- `getUserMedia` needs a secure context: HTTPS, or `localhost`; otherwise `navigator.mediaDevices` is `undefined`. Inside an `<iframe>` the embedding page must grant `allow="microphone"` [S: MDN]. So recording works at `http://localhost:7860` and at `https://<sub>.hf.space`; it does not work at `http://<LAN-IP>:7860`. Whether the huggingface.co Space page grants the microphone to its iframe was not verifiable from the page markup [U]; on `NotAllowedError` show a link to open the app URL in its own tab.
- Automatic gain control and noise suppression change the energy contour the system measures; the constraints above ask the browser to turn them off ("will attempt ... but will not fail if this can't be done") [S: MDN]. Whether they are on by default per browser: no source found.
- The run verified ffmpeg-encoded WebM/Opus and M4A files, not files produced by a real `MediaRecorder` [U for that last step].

---

## 7. Q6 - API between the page and FastAPI

### 7.1 Endpoints

| Method and path | Purpose | Response |
|---|---|---|
| `GET api/health` | page detects whether uploads are possible | `{"ok": true, "pipeline": "0.1.0", "limits": {"max_bytes": 52428800, "max_seconds": 180}}` |
| `POST api/analyze` (multipart) | fields: `audio` (file), `transcript` (text), `baseline_id` (text) or `baseline_audio` (file) | `{"job_id": "<32 hex>"}`; 413 / 415 / 422 |
| `GET api/jobs/{job_id}` | polling | `{"state": "running", "stage": "align", "progress": 0.4}`; when done adds `"result": "api/jobs/<id>/result.json"`; on failure `{"state": "error", "error": "..."}`; 404 if unknown |
| `GET api/jobs/{job_id}/result.json` | analysis result | a file on disk served with `FileResponse(media_type="application/json")` |
| `GET api/jobs/{job_id}/{participant\|baseline}.wav` | decoded audio, Range-capable | `audio/wav` |
| `GET gallery/index.json`, `gallery/results/*.json`, `gallery/audio/*.wav` | static files | - |
| `GET /` | `static/index.html` | - |

The first three were run in this shape (`/api/analyze`, `/api/jobs/{id}`, `/api/audio/{id}.wav`) [R].

Write the result to disk once and serve the file. That gives gallery and uploads the same code path, avoids re-serialisation, and avoids the `allow_nan=False` failure [S]. Write it with `json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False)` after converting every NaN to `None` and every numpy scalar to a Python number; keep wall-clock timestamps out of it so identical inputs give byte-identical results.

### 7.2 Result JSON (schema 1)

All times are seconds on the recording's own clock. Frame `i` of a line row is at `t = i * hop`. Missing values are `null`.

```json
{
  "schema": 1,
  "pipeline": {"version": "0.1.0"},
  "baseline":    {"id": "reagan_challenger_a", "title": "Reagan - Challenger address (excerpt)",
                  "audio": "gallery/audio/reagan_challenger_a.wav", "duration": 25.0},
  "participant": {"id": "reagan_challenger_a__pace_s3", "title": "Rushed middle, severity 3/5",
                  "audio": "gallery/audio/reagan_challenger_a__pace_s3.wav", "duration": 23.5},
  "words": [
    {"w": "Ladies", "b": [0.52, 0.91], "p": [0.48, 0.80], "ok": true}
  ],
  "map": {"b": [0.0, 0.52, 0.91, 25.0], "p": [0.0, 0.48, 0.80, 23.5]},
  "hop": 0.02,
  "rows": [
    {"key": "pitch",  "label": "Pitch",  "unit": "st", "kind": "line", "b": [null, 1.25], "p": [null, 0.90]},
    {"key": "energy", "label": "Energy", "unit": "dB", "kind": "line", "b": [-3.1, -2.8], "p": [-4.0, -3.7]},
    {"key": "pace",   "label": "Pace",   "unit": "log2 ratio", "kind": "word", "v": [0.05]},
    {"key": "pause",  "label": "Pauses", "unit": "s", "kind": "intervals", "b": [[5.10, 5.62]], "p": [[4.71, 4.80]]}
  ],
  "flaws": [
    {"id": 1, "type": "pace", "row": "pace", "severity": "severe",
     "words": [10, 19], "p": [4.00, 6.50], "b": [4.00, 8.00],
     "measure": "speech rate", "unit": "x", "baseline": 1.00, "participant": 1.60,
     "delta": 0.60, "z": 4.1, "threshold": 2.5,
     "text": "Rushed: 10 words in 2.50 s vs 4.00 s in the baseline (rate x1.60, z = +4.1).",
     "fix": "Slow down through this sentence; aim for about 4.0 s."}
  ],
  "truth": [
    {"type": "pace", "row": "pace", "severity": "severe", "p": [4.00, 6.50], "b": [4.00, 8.00]}
  ],
  "scores": {"overall": 62, "max": 100,
             "dims": [{"key": "pace", "label": "Pace", "score": 11, "max": 20, "flaws": [1],
                       "note": "1 severe region, 2.5 s"}]}
}
```

Field contract:

| Field | Rule |
|---|---|
| `words[i]` | index = word index in the transcript; `b`/`p` = `[start, end]`; `ok: false` when alignment confidence is low |
| `map` | anchors for section 3.1, built on the server from the `ok` words, made non-decreasing (running maximum), first point `(0, 0)`, last `(duration_b, duration_p)` |
| `rows` | data-driven: the page loops over them, so adding a feature needs no JavaScript change. `kind: "line"` has `b` and `p` arrays on `hop`; `"word"` has one value per word; `"intervals"` has `[start, end]` lists |
| `flaws[].row` | key of the row where the band is drawn |
| `flaws[].p`, `.b` | true spans from word boundaries; for a pause flaw the gap between two words |
| numeric explanation fields | sent separately from `text` so the page can build the table and tooltips |
| `truth` | only for gallery items with known injected flaws |
| rounding | times 3 decimals, values 2 decimals |

Size: a 60 s pair is about 2 x 2 x 3,000 numbers (about 72 KB) plus about 9 KB of words. `GZipMiddleware` is a one-line option that leaves audio and Range responses alone [S, not run].

### 7.3 Display resolution

`DISPLAY_HOP_S = 0.02` (50 points per second): 3,000 points per trace for 60 s, 9,000 at the 180 s cap. Rendering time at 9,000 points was not measured; the constant is the knob.

### 7.4 Gallery index

```json
{"schema": 1, "speeches": [
  {"id": "reagan_challenger_a", "title": "...", "speaker": "...", "source": "...", "licence": "...",
   "transcript": "...", "audio": "gallery/audio/reagan_challenger_a.wav", "duration": 25.0,
   "variants": [
     {"id": "reagan_challenger_a__pace_s5", "label": "Rushed, severity 5/5", "severity": 5,
      "kind": "dsp", "types": ["pace"], "score": 31, "result": "gallery/results/reagan_challenger_a__pace_s5.json"}
   ]}
]}
```

`speeches[]` doubles as the list of bundled baselines for the upload form.

---

## 8. Q7 - Deployment

### 8.1 Docker (not built: Docker builds were out of bounds for this run) [U as a whole; each line is from a cited source]

```dockerfile
FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.12.3 /uv /uvx /bin/
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1 UV_NO_CACHE=1 UV_PYTHON_DOWNLOADS=0 \
    PATH=/home/user/app/.venv/bin:$PATH
WORKDIR /home/user/app
COPY --chown=user pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project
COPY --chown=user . .
RUN uv sync --locked
EXPOSE 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1", "--forwarded-allow-ips", "*"]
```

Sources for each choice:

- `COPY --from=ghcr.io/astral-sh/uv:<version> /uv /uvx /bin/`, `uv sync --locked --no-install-project` then `uv sync --locked`, `UV_COMPILE_BYTECODE`, `UV_LINK_MODE=copy`, `UV_NO_DEV=1`, `UV_NO_CACHE`, `.venv` in `.dockerignore`: uv Docker guide [S: `docs_raw/uv_docker.md`]. Tags `ghcr.io/astral-sh/uv:0.12.3` (the laptop's uv, which writes the lock) and `:0.12.21` and `python:3.12-slim-trixie` exist [R: registry manifest requests returned 200].
- User id 1000, `--chown=user`, port 7860: Hugging Face Docker Spaces doc [S].
- `--host 0.0.0.0` (uvicorn default is 127.0.0.1), `--workers 1` (default follows `$WEB_CONCURRENCY`), `--forwarded-allow-ips "*"` so redirects use the proxy's scheme [S: uvicorn wheel].
- Debian trixie ships ffmpeg 7.1.5 [S: `sources.debian.org` API]; the decode command was run on 6.1.1 only.
- Run: `docker build -t cvoice . && docker run --rm -p 7860:7860 cvoice`, open `http://localhost:7860`.
- Without Docker: `uv run uvicorn app.main:app --port 7860`.

### 8.2 Hugging Face Spaces (Docker SDK)

Facts [S: `docs_raw/hf_spaces-*.md`, fetched from `huggingface/hub-docs` main]:

- README front matter: `sdk: docker`, `app_port: 7860` (7860 is the default).
- "The container runs with user ID 1000."
- CPU Basic: 2 vCPU, 16 GB RAM, 50 GB non-persistent disk; sleeps after 48 h without visits and restarts on the next visit; outbound requests only on ports 80, 443, 8080; `startup_duration_timeout` default 30 minutes.
- The app is served at `https://<space-subdomain>.hf.space`, "always served from the root of this subdomain".
- **"Gradio and Docker Spaces run on compute and require a paid plan to create: PRO for personal accounts, Team or Enterprise for organizations."** Added by hub-docs PR #2624, merged 2026-07-21: "Creating Gradio and Docker Spaces (anything that runs on compute, including CPU Basic) requires a paid plan". "Static Spaces are free for everyone."
- ZeroGPU: free personal accounts in good standing may host up to 2 ZeroGPU Spaces, but "ZeroGPU Spaces are exclusively compatible with the Gradio SDK".

Consequences:

| Target | Cost | What runs |
|---|---|---|
| Local Docker / `uv run` | free | everything |
| HF Docker Space | needs a paid plan to create | everything, 2 vCPU |
| HF Static Space (`sdk: static`, `index.html` at the root) or GitHub Pages | free | the gallery (static JSON + audio); upload card hidden |

The static target works only because gallery results are files and the page uses relative URLs.

---

## 9. Verified by running

Nothing was run on Kaggle for this topic (0 kernel pushes): the topic brief says no compute. The entries below were executed by the previous run on the laptop (WSL2, Ubuntu 24.04) before it was stopped.

| # | What ran | Where | Observed | File |
|---|---|---|---|---|
| 1 | `uv venv --python 3.12` + `uv pip install fastapi uvicorn python-multipart numpy` | laptop, CPython 3.12.13 | resolved to fastapi 0.142.2, starlette 1.7.0, uvicorn 0.54.0, python-multipart 0.0.32, pydantic 2.13.5, pydantic-core 2.46.5, anyio 4.15.1, h11 0.16.0, click 8.5.0, opentelemetry-api 1.45.0 | `freeze_py312.txt` |
| 2 | `uvicorn probe_app:app --port 8765` + `bash probe_backend.sh` | laptop, ffmpeg 6.1.1 | 7 formats decoded; progress trace; 206 Range on `FileResponse` and `StaticFiles`; 413 with and without `Content-Length`; 415 for a disguised playlist; "Audio longer than 180 s"; traversal 404; 422 for blank transcript and missing file | `probe_app.py`, `probe_backend.sh`, `probe_backend.out` |
| 3 | `node run.mjs matrix.html "4.1.1-cartesian,8.0.1"` (playwright-core 1.63.0, Chrome for Testing 151.0.7922.34, headless) | laptop | steps 1-5 complete: versions, 5 shapes + 4 labels, mode bar with and without config, 4 regions per strip, region click -> select + sequential span playback with exact stop times, chart click with `xvals`, unified hover text across rows, keyboard selection, x-axis toggle. Step 6 (timings) and later (dark, phone screenshots, other version combinations) did not run: "Target page, context or browser has been closed" | `browser_test/run.mjs`, `browser_test/results.json`, `static/probe.js`, `static/probe.css`, `static/matrix.html` |
| 4 | `node palette_check.mjs`, `node palette_alpha.mjs` | laptop | separations, contrasts and the band-opacity table quoted in 5.1 | `palette_check.out`, `palette_alpha.out` |
| 5 | `curl` of every candidate CDN URL | laptop | HTTP 200, raw and compressed sizes | `cdn_check.tsv`, `cdn_urls.txt` |
| 6 | `openssl dgst -sha384` over the downloaded files; `cmp` jsDelivr vs cdn.plot.ly | laptop | integrity values; plotly bytes identical on both CDNs | `cdn_sri.tsv` |
| 7 | `ffmpeg` encodes of one 20 s clip into 7 containers; `ffprobe` | laptop | magic bytes and durations per format | `media/`, `PREVIOUS_RUN_condensed.md` lines 1717-1722 |

This session (reading and light I/O only):

| What | Observed | File |
|---|---|---|
| SHA-256 of each vendored file vs jsDelivr metadata; SHA-384 recomputed, ESM files added | 13 of 13 match | `sri_crosscheck.out` |
| `curl -I` on the pinned URLs; npm dist-tags; PyPI versions | CORS `*`, immutable cache, brotli; versions unchanged at 13:23 UTC | `cdn_headers_and_registry.out` |
| Downloaded the four wheels (hash = PyPI) and read the sources quoted in 2.5 | - | `wheels/` |
| Raw documentation sources | - | `docs_raw/` |
| Registry manifest requests for the image tags | 200 for `uv:0.12.3`, `uv:0.12.21`, `python:3.12-slim-trixie` | (console only) |

### Not verified

- Render time for 6 traces x 3,000 (or 9,000) points.
- plotly basic bundle, plotly 3.7.0, wavesurfer 7.12.12 in a browser.
- Dark-mode render, 390 px layout.
- `integrity` attributes in a browser; `app.frontend()`; `GZipMiddleware`; the Dockerfile; ffmpeg 7.1.5.
- A real `MediaRecorder` blob end to end; microphone permission inside the huggingface.co iframe.
- Autoplay of the second recording under default browser policy (the test disabled the policy).
- The pause row, ground-truth markers, null-gap insertion after warping, auto-zoom on selection, job sweep.
- Two console 404s were logged in the browser run; the request log covers only media and CDN URLs (all 200), so the missing resources are unidentified (a favicon request is likely).

---

## 10. Risks

1. **Fresh major versions.** wavesurfer 8.0.1 is 7 days old, plotly 4.1.1 is 17 days old, FastAPI 0.142.2 is 1 day old. Mitigation: exact pins + SRI + `uv.lock`; never `@latest` or `@8`. Fallbacks (7.12.12, 0.141.1) are not run-tested.
2. **Chart performance unmeasured** at the 180 s cap. Knob: `DISPLAY_HOP_S`.
3. **CDN dependence.** With no network the page has no chart or player; SRI turns a tampered or changed file into a hard failure. Vendoring the four files into `static/vendor/` (1.58 MB) removes this but departs from "from a CDN".
4. **Hosted demo cost.** A Docker Space cannot be created on a free HF account any more.
5. **Alignment quality drives the picture.** A bad word alignment bends the warped curve and misplaces bands; the page can only dim low-confidence words.
6. **Lossy uploads** carry codec delay/padding (AAC +15.6 ms measured); handled by playing the decoded WAV, but timestamps then refer to the decoded file, not the user's original.
7. **Autoplay policy** may block the automatic baseline playback after the participant span on some browsers; explicit buttons cover it.
8. **Microphone** unavailable on plain-HTTP LAN addresses and possibly inside the Space iframe.
9. **In-memory job table**: results vanish on restart and break with more than one worker.
10. **ffmpeg version drift** between Kaggle, the laptop (6.1.1) and the image (7.1.5) can change decoded samples slightly, which touches the reproducibility criterion.
11. **Plotly internals** used by the cursor (`.nsewdrag`) can change on upgrade.
12. **Provenance of the browser evidence:** it comes from a run the laptop owner stopped; steps 1-5 finished and were written to `results.json` by the script's own error handler.

---

## 11. Where this differs from the preliminary direction

1. Direction 1 implies showing the participant on the baseline's timeline. For the dashboard the default should be the opposite: participant true time on the axis, baseline warped (section 3.3).
2. Direction 4 (template explanations): the JSON must also carry the numbers behind each sentence as separate fields; the page needs them for the table and tooltips.
3. Direction 5/6 assumed a Hugging Face Docker Space as a deployment target; that now needs a paid plan. A static gallery build is the free hosted option.
4. Severity should not be encoded by band colour; measured separations are too small (section 5.1).
5. "Plotly.js from a CDN" should mean the cartesian partial bundle (501 KB), not the full bundle (1,410 KB), with `showSendToCloud: false`.
6. Progress: plain polling is sufficient; nothing heavier is warranted.
7. Gallery items should carry the injected ground-truth spans so the page can show detected vs injected regions.

---

## 12. Sources

Pinned artefacts and registries
- npm registry and jsDelivr data API for `plotly.js-dist-min`, `plotly.js-cartesian-dist-min`, `plotly.js-basic-dist-min`, `wavesurfer.js`: `https://registry.npmjs.org/<pkg>`, `https://data.jsdelivr.com/v1/packages/npm/<pkg>@<version>?structure=flat`
- plotly.js type declarations 4.1.1: `https://cdn.jsdelivr.net/npm/plotly.js-dist-min@4.1.1/src/types/` (`core/api.d.ts`, `core/events.d.ts`, `core/config.d.ts`, `generated/schema.d.ts`)
- plotly.js releases: `https://github.com/plotly/plotly.js/releases` (v3.5.0, v3.6.0, v3.7.0, v4.0.0, v4.1.0, v4.1.1)
- wavesurfer.js 8.0.1 package files: `https://cdn.jsdelivr.net/npm/wavesurfer.js@8.0.1/` (`dist/*.d.ts`, `package.json`, `README.md`, bundles)
- wavesurfer.js releases: `https://github.com/katspaugh/wavesurfer.js/releases` (8.0.0, 8.0.1); docs `https://wavesurfer.xyz/docs/`
- PyPI: `https://pypi.org/pypi/fastapi/json`, `/starlette/`, `/uvicorn/`, `/python-multipart/`, `/uv/`; wheels read: `fastapi-0.142.2`, `starlette-1.7.0`, `uvicorn-0.54.0`, `python_multipart-0.0.32`

Documentation
- FastAPI docs at tag 0.142.2: `https://github.com/fastapi/fastapi/tree/0.142.2/docs/en/docs` (`tutorial/request-files.md`, `tutorial/server-sent-events.md`, `tutorial/frontend.md`, `tutorial/static-files.md`, `release-notes.md`)
- uv Docker and FastAPI guides: `https://docs.astral.sh/uv/guides/integration/docker/`, `https://docs.astral.sh/uv/guides/integration/fastapi/`
- Hugging Face Hub docs: `https://huggingface.co/docs/hub/spaces-sdks-docker`, `/spaces-config-reference`, `/spaces-overview`, `/spaces-gpus`, `/spaces-sdks-static`, `/spaces-zerogpu`, `/spaces-embed`, `/spaces-storage`; change record `https://github.com/huggingface/hub-docs/pull/2624`
- Plotly performance: `https://plotly.com/python/performance/` (source `https://github.com/plotly/plotly.py/blob/main/doc/python/performance.md`), `https://plotly.com/javascript/webgl-vs-svg/`
- MDN: `https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity`, `/Web/API/MediaDevices/getUserMedia`, `/Web/API/MediaRecorder/MediaRecorder`, `/Web/API/MediaRecorder/isTypeSupported_static`, `/Web/API/MediaTrackConstraints/autoGainControl`, `/Web/Media/Guides/Autoplay`, `/Web/Media/Guides/Formats/Audio_codecs`; browser-compat-data `https://github.com/mdn/browser-compat-data/blob/main/api/MediaRecorder.json`
- WCAG 2.2: `https://www.w3.org/TR/WCAG22/`, `https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html`, `https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html`
- Debian package versions: `https://sources.debian.org/api/src/ffmpeg/`
- CVE-2016-1897: `https://nvd.nist.gov/vuln/detail/CVE-2016-1897`

Papers
- Gleicher, Albers, Walker, Jusufi, Hansen, Roberts. Visual comparison for information visualization. Information Visualization 10(4):289-309, 2011. Preprint: `https://graphics.cs.wisc.edu/Papers/2011/GAWJHR11/paper.pdf`
- Javed, McDonnel, Elmqvist. Graphical Perception of Multiple Time Series. IEEE TVCG 16(6):927-934, 2010. `https://www.semanticscholar.org/paper/27493372f4581c3a0ef87a3242ce4ba123d451ff`

Local evidence files (this directory)
- `PREVIOUS_RUN_condensed.md`, `probe_app.py`, `probe_backend.sh`, `probe_backend.out`, `freeze_py312.txt`, `browser_test/run.mjs`, `browser_test/results.json`, `static/probe.js`, `static/probe.css`, `static/matrix.html`, `palette_check.out`, `palette_alpha.out`, `cdn_check.tsv`, `cdn_sri.tsv`, `sri_crosscheck.out`, `cdn_headers_and_registry.out`, `vendor/`, `wheels/`, `docs_raw/`, `meta/`
