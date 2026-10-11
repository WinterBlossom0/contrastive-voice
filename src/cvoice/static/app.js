"use strict";
/* Contrastive Voice dashboard. One render path: render(result, base) draws a gallery result and an upload result alike.
   Text from results is user data: it is only ever inserted with textContent. */

// ---------------------------------------------------------------------------------------------------- constants
const PLOT_L = 64, PLOT_R = 16;          // px; the wavesurfer strip uses the same insets (style.css .wave)
const DISPLAY_HOP_S = 0.02;              // s; frame rows are thinned to this hop before drawing
const MIN_PLAY_S = 0.6;                  // s; a flaw's span is padded to this length for A/B playback
const BAND_ALPHA = 0.16, BAND_ALPHA_SEL = 0.20;   // flag wash; the recording line keeps >= 3:1 on it up to 0.20
const ROW_GAP_PX = 32;                   // room for each row's heading, clear of the lowest tick label of the row above
const HATCH_STEP_PX = 7;                 // px between the hatch lines of a sub-word span
const GROUP_PAD_PX = 4;                  // px between a group outline and its members' washes
const LABEL_PAD_PX = 3, LABEL_CHAR_PX = 7;   // a wash number's padding and its width per character at 11 px
const LABEL_GAP_PX = 4, LABEL_SHIFT_PX = 6;  // px between two wash numbers; px a number may move right past a wash narrower than that
const POLL_MS = 500;
const BOTH_GAP_MS = 350;                 // ms of silence between the two spans of "Play both"
const TL_REF_TRACK_PX = 8, TL_TRACK_PX = 16;   // px; the reference word track (quiet) and this recording's word track
const TL_LINK_GAP_PX = 10, TL_LABEL_PX = 20;  // px; gap under the reference track, and the row of the "This recording" label
const TL_MIN_SPAN_PX = 4;                // px; a shorter span (a pause point) is widened to stay visible and clickable
const TL_MARK_H = 22, TL_MARK_GAP = 4;   // px; height of a fault label and the gap kept around it
const TL_MARK_FONT = 12.5;               // px; must equal .tl-mk text in style.css
const TL_MARK_ROWS = 3;                  // label rows above this recording's track; a label that fits in none is counted under the panel
const TL_MARK_REACH_PX = 48;            // px a full label may move sideways off its region; a number alone may move three times as far
const TL_JOIN_S = 0.5;                   // s; members of one finding group closer than this share one label
const TL_EDGE_PX = 3, TL_LANE_PX = 4;    // px from this recording's track up to a fault's marker line; px between the lines of overlapping faults
const WAVE_BARS = { barWidth: 2, barGap: 1, barRadius: 2 };   // px; fault colours snap to the gaps between these bars
// How a fault span looks on this recording's waveform, from calm to strong: bar colour as a share of the way from lavender
// (--you) to bramble (--flag-bar), then on to the light bramble (--flag-text); bar opacity; opacity of the soft wash behind.
// A piece under several faults takes the strongest look. "calm" is any fault while another one is selected or hovered.
const FAULT_LOOKS = ["calm", "dot", "dash", "solid", "grp", "peek", "sel", "diff"];
const FAULT_LOOK = {
  calm: { bramble: 0.8, light: 0, alpha: 0.62, wash: 0.04 },
  dot: { bramble: 0.55, light: 0, alpha: 0.82, wash: 0.06 },
  dash: { bramble: 0.8, light: 0, alpha: 0.9, wash: 0.09 },
  solid: { bramble: 1, light: 0, alpha: 0.96, wash: 0.12 },
  grp: { bramble: 1, light: 0.25, alpha: 1, wash: 0.13 },
  peek: { bramble: 1, light: 0.35, alpha: 1, wash: 0.16 },
  sel: { bramble: 1, light: 1, alpha: 1, wash: 0.22 },
};
const SVG_NS = "http://www.w3.org/2000/svg";
const RING_C = 2 * Math.PI * 52;         // circumference of the score ring (r 52 in index.html)
const COUNT_MS = 1000;                   // ms of the score count-up on the first load
const INTRO_MS = 2500;                   // ms of the first-load sequence: waveforms draw in, then the bands light one by one
// Simple line icons per dimension key, as SVG path data on a 20 x 20 grid.
const DIM_ICON = {
  D1: "M4 16 L10 3 L16 16 M7 10 H13", D7: "M4 16 L10 3 L16 16 M7 10 H13", D9: "M4 16 L10 3 L16 16 M7 10 H13",
  D2: "M6 4 V16 M14 4 V16", D3: "M2 12 C5 4 8 4 10 10 S15 16 18 8", D4: "M10 3 V12 M10 16 V16.5", D8: "M3 14 C7 14 9 6 17 5",
  D5: "M3 8 H7 L12 4 V16 L7 12 H3 Z M15 7 C17 9 17 11 15 13", D6: "M3 10 H5 M7 5 V15 M10 7 V13 M13 3 V17 M16 8 V12",
};
const SEVERITY_STYLES = [[1 / 3, "dot", "dotted"], [2 / 3, "dash", "dashed"], [Infinity, "solid", "solid"]];

const LIBS = [  // [is it loaded?, fallback file]; the wavesurfer core must come before its plugins
  [() => typeof Plotly !== "undefined", "vendor/plotly-cartesian.min.js"],
  [() => typeof WaveSurfer === "function", "vendor/wavesurfer.min.js"],
  [() => typeof WaveSurfer === "function" && WaveSurfer.Regions, "vendor/regions.min.js"],
  [() => typeof WaveSurfer === "function" && WaveSurfer.Timeline, "vendor/timeline.min.js"],
];
const ROWS = {  // heading (wide, narrow), dimension, kind of drawing
  pitch: { t: "Pitch, semitones from each speaker's median", own: "Pitch, semitones from your median", s: "Pitch (st)", h: 120, frame: true },
  energy: { t: "Level, dB from each speaker's median voiced level", own: "Level, dB from your median voiced level", s: "Level (dB)", h: 100, frame: true },
  pace: { t: "Pace: ln ratio of speech time, below 0 is faster", s: "Pace (ln)", h: 84, dim: "D1" },
  pauses: { t: "Pauses: length difference, below 0 is shorter", s: "Pauses (s)", h: 76, dim: "D2", bars: true },
  pitch_range: { t: "Pitch range: ln ratio at your overall range, below 0 is flatter", s: "Pitch range (ln)", h: 84, dim: "D3" },
  stress: { t: "Stress points: words that carry stress", s: "Stress", h: 52 },
  emphasis: { t: "Emphasis: stress-point difference at the reference's stress words", s: "Emphasis", h: 76, dim: "D4", bars: true },
  volume: { t: "Volume: level difference, below 0 is quieter", s: "Volume (dB)", h: 84, dim: "D5" },
  clarity: { t: "Clarity: ln ratio of spectral change", s: "Clarity proxy (ln)", h: 84, dim: "D6" },
  speech_tempo: { t: "Speech tempo: ln ratio of aligned word time (pauses not included), below 0 is faster", s: "Speech tempo (ln)", h: 84, dim: "D9" },
  word_time: { t: "Word time: ln ratio at your overall tempo", s: "Word time (ln)", h: 90, dim: "D7", markers: true },
  ending: { t: "Ending: final pitch-change difference", s: "Ending (st)", h: 90, dim: "D8", markers: true },
};
const ROW_OF_DIM = { D1: "pace", D2: "pauses", D3: "pitch_range", D4: "emphasis", D5: "volume", D6: "clarity", D7: "word_time", D8: "ending", D9: "speech_tempo" };
const ALSO_ROW = { D3: "pitch", D5: "energy", D8: "pitch" };   // the contour row a delta row summarises
const UNIT = { ln: "ln ratio", s: "s", p: "stress units", dB: "dB", st: "st", count: "", words: "words" };
const VALUE_UNIT = { D1: "s", D2: "s", D3: "st", D4: "", D5: "dB", D6: "", D7: "s", D8: "st", D9: "s" };   // unit of the baseline / participant values
const TYPE_TEXT = {
  RUSH: "Rushed", DRAG: "Dragged", PAUSE_DROPPED: "Missing pause", PAUSE_INTRUSIVE: "Pause inside a phrase", MONOTONE: "Flat pitch",
  DEEMPHASIS: "Key word not stressed", FADE: "Volume drops", MUMBLE: "Reduced spectral change", TEMPO_FAST: "Overall tempo too fast",
  TEMPO_SLOW: "Overall tempo too slow", RANGE_NARROW: "Overall pitch range too narrow",
  WORD_TIME: "Word takes longer than the reference", ENDING_HIGH: "Sentence ending higher than the reference", UNEVEN_TEMPO: "Uneven word timing",
  NATURAL_RUSH: "Words spoken faster",
};
const PATTERN_TEXT = {
  RUSH: "Rushed", NATURAL_RUSH: "Natural rushing", WORD_BY_WORD: "Word-by-word reading", HESITATION: "Hesitation", TRAILING_OFF: "Trailing off",
  LOW_EFFORT: "Low vocal effort", BLOCK: "Block", WORD_REPETITION: "Word repetition", SOUND_REPETITION: "Sound repetition",
  FILLED_PAUSE: "Filled pause", ONSET_PROLONGATION: "Prolonged first sound", RHYME_PROLONGATION: "Prolonged end of the word",
  LENGTHENED_WORD: "Lengthened word", DRAG: "Slower stretch", RISING_ENDING: "Rising ending", FLAT_FINAL_FALL: "Flattened final fall", UNEVEN_TEMPO: "Uneven word timing",
};
// compare.py adds a constant to both values before the ln ratio of these dimensions (RANGE_REG_ST, D7_REG_S), so exp(delta)
// is not the ratio of the two printed values.
const REGULARISED = new Set(["D3", "D7"]);
// A whole-passage ratio value (participant / reference): the quantity, then the meaning of a value below 1 and above 1.
const WHOLE_RATIO = { D1: ["speech time", "faster", "slower"], D3: ["pitch range", "narrower", "wider"] };
const CANDIDATE_TEXT = "Automatic label; low precision on real speech; listen to the span.";
const SYNTHETIC_TEXT = "Synthetic-only family; unvalidated on real speech.";   // explain.SYNTHETIC_ONLY_CLAUSE
const OWN_EVIDENCE = { D9: "word_time_ln" };
// One plain name per measure group; the result JSON's brief words are Cadence, Pauses, Tone, Volume and Clarity.
const GROUP_NAME = { Cadence: "Pace", Tone: "Pitch range", Clarity: "Clarity" };
const groupLabel = (word) => GROUP_NAME[word] || word;
const SUB_NAME = { D3: "Pitch range", D6: "Clarity" };
// The finding's own measure (a group can join two measures of one brief word, e.g. Pace and Speech tempo under Cadence).
const measureName = (f) => SUB_NAME[f.dimension] || S.result.scores.dims.find((d) => d.key === f.dimension)?.label || groupLabel(f.brief_word);
// Bundled examples named by what a listener hears, in order of how clearly they show the tool; the first ones open the menu and
// the rest sit under "More examples". Items without an entry show their group and label.
const EXAMPLES = [
  ["L3A", "Rushed in the middle, then fading"], ["L3B", "A pause mid-phrase and mumbled words"], ["G5", "Rushed and flat all the way through"],
  ["natural_rush", "Speeding up mid-sentence"], ["L2A", "A fade and a skipped pause, milder"], ["L2B", "A pause mid-phrase and a dragged opening, milder"],
  ["greenman_edited", "Another speaker, with a pause mid-phrase"], ["identity", "The reference itself: nothing to fix"],
  ["greenman", "A natural reading of the same text by another speaker"],
  ["greenman_botched", "Another speaker, flat throughout"], ["r2_consensus", "Against five readers: a narrow pitch range"],
  ["G3", "Slightly rushed and flat in places"], ["L1A", "One skipped pause"], ["L1B", "A short pause mid-phrase"], ["G1", "One slightly rushed phrase"],
  ["r2_listed", "Another speaker, with repeated words and sounds"], ["channel_mp3", "The reference through MP3 compression"],
];
const EXAMPLE_NAME = Object.fromEntries(EXAMPLES);
const FEATURED_COUNT = 9;
const TWIN_NAME = "Same reading, no reference";
const TWINS = new Set();                 // ids of no-reference examples that read the audio of an example with a reference
const exampleName = (it) => TWINS.has(it.id) ? TWIN_NAME : EXAMPLE_NAME[it.id] || `${it.group}, ${it.label}`;
const TOP_N = 3;
const TICK_MS = 380;                     // ms of the points tick when an example opens
const BAND_STEPS = 7;                    // intro: at most this many band steps (style.css .intro .tl-band: 1 s, then 0.16 s each)
const FIX_COUNT_WORDS = ["", "Your biggest fix", "Your two biggest fixes", "Your three biggest fixes"];
const reducedMotion = () => matchMedia("(prefers-reduced-motion: reduce)").matches;   // the evidence row that holds the finding's own measured difference
// A reading graded without a reference reading (pipeline SELF mode): its words compare with the reader's own typical delivery.
const SELF_MODE = "none";
const isSelf = (r = S.result) => r?.detection?.reference_mode === SELF_MODE;
const TYPICAL = "your typical delivery";
// Page copy that names the reference, with its no-reference wording; the reference wording is read from the page at start.
const SELF_COPY = {
  "#hero-title": "Hear where your reading drifts from your typical delivery.",
  "#value-line": "Your reading is graded against itself: each stretch is compared with how you read the rest of it. Hear the spots that stand out, and fix the ones that cost you the most first.",
  "#footer-scope": "Scores are relative to your own typical delivery in this reading.",
  "#hero-wave@aria-label": "Your reading over time",
  "#key-ref": "Your typical delivery",
};
const SELF_LIMIT = "A rough check: your reading is graded against itself. For better results, use a reference reading of the same text.";
// What a fix did to one finding, in the words the page shows (app.plain_outcome gives the reason).
const FIX_STAGES = ["edit", "check"];   // app.FIX_STAGES (tests/test_app.py compares them)
const FIX_STAGE_TEXT = { edit: "Editing your recording…", check: "Checking the result…" };
// "Edited", never "Fixed": an edit can leave a spot flagged or apply only part of the change (build/work/repair/FIX_CONTRACT.md).
const LISTEN_SIDES = [["yours", "Yours"], ["fixed", "Edited"], ["target", "Target"]];
const HEAR_FIXED = { reference: "Hear it fixed", self: "Hear it closer to your typical delivery" };

// ---------------------------------------------------------------------------------------------------- helpers
const $ = (s) => document.querySelector(s);
const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const rgba = (hex, a) => `rgba(${parseInt(hex.slice(1, 3), 16)},${parseInt(hex.slice(3, 5), 16)},${parseInt(hex.slice(5, 7), 16)},${a})`;
const num = (v, d) => (v == null ? "-" : v.toFixed(d));
const signed = (v, d = 2) => (v == null ? "-" : (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v).toFixed(d));
const span = (s) => !s ? "whole passage" : s[0].toFixed(2) === s[1].toFixed(2) ? `at ${s[0].toFixed(2)} s` : `${s[0].toFixed(2)}–${s[1].toFixed(2)} s`;
const sevStyle = (v) => SEVERITY_STYLES.find((x) => v < x[0]) || SEVERITY_STYLES[2];
const wholePassage = (f) => f.context === "whole passage" || f.words == null;
// Beside a whole-clip tempo finding a local pace flag is relative to the speaker's own overall tempo, not a second tempo verdict.
const typeText = (f) => f.dimension === "D1" && (f.type === "RUSH" || f.type === "DRAG") && S.result.flaws.some((x) => x.type.startsWith("TEMPO"))
  ? (f.type === "RUSH" ? "Faster than the rest of your reading" : "Slower than the rest of your reading") : TYPE_TEXT[f.type] || f.type;
const valUnit = (f) => f.value_unit === "x" ? "×" : f.value_unit ?? (f.words == null ? "×" : VALUE_UNIT[f.dimension] || "");
const withUnit = (v, unit) => v == null ? "-" : unit === "×" ? `×${num(v, 2)}` : `${num(v, 2)} ${unit}`.trim();
const factor = (v) => `×${Math.exp(v).toFixed(2)}`;   // an ln ratio as a plain factor
// Points are rounded to 2 decimals, so a stored 0.00 is a loss below MIN_SHOWN_POINTS, not a zero (gallery.MIN_SHOWN_POINTS).
const MIN_SHOWN_POINTS = 0.005;
const shownLoss = (v) => (v ?? 0) >= MIN_SHOWN_POINTS;
const ptsText = (v) => v == null ? "" : !shownLoss(v) ? "<0.01 pts" : `−${num(v, 2)} pts`;
// A counted finding can lose 0 points while its dimension still costs points (explain.dimension_loss). The dimension's loss is
// shown once: on the finding of that dimension that carries points, else on this finding as the dimension's total.
const zeroLoss = (f) => f.counted !== false && !shownLoss(f.points_lost) && shownLoss(f.dimension_points_lost);
const lossCarrier = (f) => S.result.flaws.findIndex((x) => x !== f && x.dimension === f.dimension && x.counted !== false && shownLoss(x.points_lost));
const saturated = (f) => zeroLoss(f) && lossCarrier(f) < 0;
const dimText = (f) => S.result.scores.dims.find((d) => d.key === f.dimension)?.label || f.dimension;
const findingPts = (f) => saturated(f) ? `${dimText(f)} −${num(f.dimension_points_lost, 2)} pts in total`
  : zeroLoss(f) ? `<0.01 pts (${dimText(f)} loss on #${lossCarrier(f) + 1})` : ptsText(f.points_lost);
const synthetic = (f) => (f.text || "").toLowerCase().includes(SYNTHETIC_TEXT.toLowerCase());
// Scores and multiples are shown at their stored 2 decimals: a second rounding makes them disagree with points_lost and the text.
const scoreText = (v) => v == null ? "n/a" : num(v, 2);
const multipleText = (v) => v == null ? "-" : `×${num(v, 2)}`;
const patternText = (p) => PATTERN_TEXT[p] || TYPE_TEXT[p] || p || "Other findings";
const groupName = (f) => f.group_pattern ? patternText(f.group_pattern) : "Finding";
// The pattern has its own chip (patternTags), so the title names the measured departure.
const findingText = (f) => f.type ? typeText(f) : f.label || f.brief_word || f.dimension;
const unevenTempo = (f) => f.pattern === "UNEVEN_TEMPO" || f.type === "UNEVEN_TEMPO";
// ln values carry 2 decimals (contract §1), so exp() can miss the factor that the text states from the unrounded value by 0.01.
const statedFactor = (f, pattern, v) => { const m = (f.text || "").match(pattern); return m ? `×${m[1]}` : factor(v); };
const spreadFactor = (f) => statedFactor(f, /typical factor of x(\d+(?:\.\d+)?)/, f.participant);
const thresholdFactor = (f) => statedFactor(f, /flagged above x(\d+(?:\.\d+)?)/, f.threshold);

function el(tag, attrs = {}, ...kids) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v;
    else if (k === "text") e.textContent = v;
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else e.setAttribute(k, v);
  }
  e.append(...kids.filter((x) => x != null));
  return e;
}

function svgEl(tag, attrs = {}, ...kids) {
  const e = document.createElementNS(SVG_NS, tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "text") e.textContent = v;
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else e.setAttribute(k, v);
  }
  e.append(...kids.filter((x) => x != null));
  return e;
}

let measureContext = null;
function scratchContext() {
  if (!measureContext) measureContext = document.createElement("canvas").getContext("2d");
  return measureContext;
}
function textWidth(text, px, weight = 400) {
  scratchContext().font = `${weight} ${px}px ${css("--sans")}`;
  return measureContext.measureText(text).width;
}

/** Piecewise-linear map xs -> ys (xs non-decreasing); clamps outside the range. */
function interp(x, xs, ys) {
  const n = xs.length;
  if (x <= xs[0]) return ys[0];
  if (x >= xs[n - 1]) return ys[n - 1];
  let lo = 0, hi = n - 1;
  while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (xs[mid] <= x) lo = mid; else hi = mid; }
  const w = xs[hi] - xs[lo];
  return w === 0 ? ys[hi] : ys[lo] + (ys[hi] - ys[lo]) * (x - xs[lo]) / w;
}

function loadScript(src) {
  return new Promise((res) => document.head.append(el("script", { src, onload: res, onerror: res })));
}

async function ensureLibs() {
  for (const [loaded, file] of LIBS) if (!loaded()) await loadScript(file);   // CDN failed or SRI mismatch: vendored copy
}

function showAlert(msg) {
  const a = $("#alert");
  a.textContent = msg;
  a.hidden = !msg;
}

// ---------------------------------------------------------------------------------------------------- state
const S = { fix: { info: null, source: null, jobs: new Map(), busy: null, player: null }, copy: null, result: null, sel: null, filter: null, rid: 0, limits: null, flagLimits: null, ws: null, regions: null, ref: new Audio(),
  refTimer: null, bothTimer: null, tl: null, chart: null, hasLibs: false, selKind: "flaw", allDimensions: false, openId: 0,
  mediaId: 0, youReady: false, refReady: false, inSpan: new Set(), listenAt: null, audio: null, sources: new WeakMap(), levelOn: false, countId: 0, counted: false, side: "you", wsRef: null, playId: 0, priority: null, pattern: null, peekI: null, paintFrame: 0 };

// Graded on its own, the overall articulation rate is not shown: it compares the reader with other speakers, not with themselves.
const articulationRate = (d) => d.unit === "syllables/s" || /articulation rate/i.test(d.label || "");
function differences() {
  if (!(S.result.regime === "R2" || isSelf()) || !Array.isArray(S.result.differences)) return [];
  return isSelf() ? S.result.differences.filter((d) => !articulationRate(d)) : S.result.differences;
}
function selected() { return (S.selKind === "difference" ? differences() : S.result.flaws)[S.sel]; }
function mediaSpan(f, who) { return f[who === "you" ? "p" : "b"] || [0, S.result[who === "you" ? "participant" : "baseline"].duration]; }

function noRegions(r) {
  if (isSelf(r)) return "Nothing stands out from your typical delivery.";
  return r.regime === "R2" ? "Nothing crosses the threshold set for a different speaker." : "Nothing crosses its threshold: this reading matches the reference.";
}

// ---------------------------------------------------------------------------------------------------- scores
/**
 * A row's flag thresholds, or null when the row has none: "below ×0.82, above ×1.23", "below −0.323 s"; compact for a
 * phone-width heading, whose short name already gives the unit: "< ×0.82 or > ×1.23", "< −0.323".
 */
function thresholdText(row, compact = false) {
  const [below, above] = row.tol || [null, null];
  if (below == null && above == null) return null;
  // ln rows state the thresholds as plain factors; both forms use the precision of the R2 detection note (x%.2f, %.3g).
  const ln = row.unit === "ln", plain = (v) => String(Number(v.toPrecision(3)));
  const parts = [below != null ? [compact ? "<" : "below", ln ? factor(-below) : "−" + plain(below)] : null,
    above != null ? [compact ? ">" : "above", ln ? factor(above) : "+" + plain(above)] : null].filter(Boolean).map((x) => x.join(" "));
  return compact ? parts.join(" or ") : parts.join(", ") + (ln ? "" : ` ${UNIT[row.unit] || row.unit}`);
}

function dimGroups(r) {
  const groups = [];
  for (const d of r.scores.dims) {
    let g = groups.find((x) => x.word === d.brief_word);
    if (!g) groups.push(g = { word: d.brief_word, dims: [] });
    g.dims.push(d);
  }
  return groups;
}

/** The score ring's arc, and on the first load a count-up of the score that ends on the stored value. */
function showScore(o) {
  const arc = `${(RING_C * Math.max(0, Math.min(100, o ?? 0)) / 100).toFixed(2)} ${RING_C.toFixed(2)}`;
  for (const id of ["#ring-value", "#ring-glow"]) $(id).style.strokeDasharray = arc;
  S.countId += 1;
  const fig = $("#overall-fig"), run = S.countId;
  if (S.counted || o == null || matchMedia("(prefers-reduced-motion: reduce)").matches) { S.counted = true; fig.textContent = scoreText(o); return; }
  S.counted = true;
  const start = performance.now();
  const step = (now) => {
    if (run !== S.countId) return;
    const k = Math.min(1, (now - start) / COUNT_MS);
    fig.textContent = k < 1 ? num(o * (1 - (1 - k) ** 3), 2) : scoreText(o);
    fig.classList.toggle("ticking", k < 1);
    if (k < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

/** The regime and reference mode as a short badge beside the example name. */
function regimeBadge(r) {
  if (isSelf(r)) return "Graded on its own";
  return r.regime === "R1" ? "Same speaker as the reference" : "Different speaker from the reference";
}

/** The counted findings that cost the most points, largest first; ties keep time order. */
function topFindings(r) {
  return r.flaws.map((f, i) => [f, i]).filter(([f]) => f.counted !== false && shownLoss(f.points_lost))
    .sort((a, b) => b[0].points_lost - a[0].points_lost || a[1] - b[1]).slice(0, TOP_N);
}

/** A stored ratio in words where it is close to a simple fraction, else the ratio itself. */
function ratioWords(x) {
  const near = [[0.25, "about a quarter of"], [1 / 3, "about a third of"], [0.5, "about half"], [2, "about twice"]].find(([v]) => Math.abs(x - v) <= 0.05 * v);
  return near ? near[1] : `${num(x, 2)} times`;
}

/**
 * Counts each points figure up to its stored text in TICK_MS, then writes the exact stored text; the "ticking" class marks
 * the figures that are still moving, so a reader of the page can wait for the final values.
 */
function tickPoints(nodes) {
  if (reducedMotion() || !S.tickOn) return;
  for (const node of nodes) {
    const text = node.firstChild?.nodeType === 3 ? node.firstChild : null, match = text?.data.match(/(\d+\.\d{2})/);
    if (!match) continue;
    const target = +match[1], start = performance.now(), final = text.data;
    node.classList.add("ticking");
    const step = (now) => {
      const k = Math.min(1, (now - start) / TICK_MS);
      text.data = k < 1 ? final.replace(match[1], (target * (1 - (1 - k) ** 3)).toFixed(2)) : final;
      if (k < 1) requestAnimationFrame(step); else node.classList.remove("ticking");
    };
    requestAnimationFrame(step);
  }
}

/** One line of what happened, in plain words, from the stored values only. */
function plainLine(f) {
  if (unevenTempo(f)) return `Typical word-to-word factor ${spreadFactor(f)}`;
  const q = WHOLE_RATIO[f.dimension];
  if (listedContext(f)) return f.text || "";
  const theirs = isSelf() ? "your typical" : "the reference's";
  if (wholeRatio(f) && q) return `Your ${q[0]} is ${ratioWords(f.participant)} ${theirs}${f.participant === 1 ? "" : `: ${f.participant < 1 ? q[1] : q[2]}`}`;
  // Levels in dB are relative to each speaker's median, so the stored difference says more than the two levels.
  if (f.unit === "dB" && f.delta != null) return `About ${num(Math.abs(f.delta), 1)} dB ${f.delta < 0 ? "quieter" : "louder"} than ${isSelf() ? "your typical level" : "the reference"}`;
  const v = (x) => withUnit(x, valUnit(f));
  if (isSelf()) return `${v(f.participant)} here, ${v(f.baseline)} is typical for you`;
  return `${v(f.participant)} in your reading, ${v(f.baseline)} in the ${referenceText(f)}`;
}

function quotedWords(r, f) {
  return wholePassage(f) ? "The whole passage" : `‘${r.words.slice(f.words[0], f.words[1] + 1).map((w) => w.w).join(" ")}’`;
}

function renderSummary(r) {
  const top = topFindings(r), mode = r.detection?.reference_mode, against = isSelf(r) ? TYPICAL : MODE_TEXT[mode] && mode !== "single" ? `the ${MODE_TEXT[mode]}` : "the reference reading";
  $("#summary-line").textContent = !r.flaws.length ? noRegions(r)
    : top.length === 1 && isSelf(r) ? `Compared with ${against}, one spot stands out the most.`
    : top.length === 1 ? `Compared with ${against}, one finding costs you the most points.`
    : top.length && isSelf(r) ? `Compared with ${against}, these ${top.length} spots stand out the most.`
    : top.length ? `Compared with ${against}, these ${top.length} findings cost you the most points.`
    : `Compared with ${against}, every finding costs less than 0.01 points.`;
  $("#fixes-title").textContent = FIX_COUNT_WORDS[top.length] || "Your biggest fixes";
  $(".fixes").hidden = !top.length;
  $("#top-cards").replaceChildren(...top.map(([f, i], rank) => el("article", { class: rank ? "top-card" : "top-card lead", "data-finding": f.id, "data-i": i, "data-peek": i },
    el("button", { type: "button", class: "card-open", "data-i": i, "data-kind": "flaw", "aria-pressed": "false", onclick: () => select(i, { scroll: true }) },
      el("span", { class: "rank", text: `${rank + 1}` }), el("span", { class: "card-title" }, dimIcon(f.dimension), findingText(f)),
      el("span", { class: "card-pts", text: findingPts(f) })),
    el("p", { class: "card-words", text: quotedWords(r, f) }),
    el("p", { class: "card-line", text: plainLine(f) }),
    thresholdGauge(f),
    f.fix ? el("p", { class: "card-fix", text: f.fix }) : null,
    el("div", { class: "card-actions" },
      el("button", { type: "button", class: "listen-btn", "data-audio": listenAudio(), "data-listen": i, onclick: () => listen(i),
        title: isSelf(r) ? "Plays this spot" : "Plays yours, then the reference" }, "Listen"),
      fixButton(f, i, { scroll: true })))));
  tickPoints(document.querySelectorAll("#top-cards .card-pts"));
  // the same count as the "Every finding" heading (#flaw-count): flagged findings only; differences sit under their own headings
  const n = r.flaws.length;
  $("#see-all").hidden = !n && !differences().length;
  $("#see-all").textContent = !n ? "See every finding" : `See all ${n} ${n === 1 ? "finding" : "findings"}`;
}

// Rows whose flag threshold is a plain physical change; the same rows as app.LIMIT_ROWS (tests/test_app.py compares them).
const LIMIT_ROWS = ["pace", "pauses", "volume"];
const roughFactor = (v) => `×${Math.exp(v).toFixed(1)}`;   // an ln threshold as a speed factor

/** "about ×1.7 faster or ×2.1 slower" from a row's [below, above] thresholds; one number when both round the same; null without either. */
function pairWords(below, above, show, lower, higher) {
  if (below == null && above == null) return null;
  if (below == null) return `about ${show(above)} ${higher}`;
  if (above == null) return `about ${show(below)} ${lower}`;
  return show(below) === show(above) ? `about ${show(below)} ${lower} or ${higher}` : `about ${show(below)} ${lower} or ${show(above)} ${higher}`;
}

const paceWords = (tol) => pairWords(...(tol || []), roughFactor, "faster", "slower");

/** The smallest flagged change of each LIMIT_ROWS row in plain words, from {row key: [below, above]}. */
function limitWords(tol) {
  const pace = paceWords(tol.pace);
  const pauses = pairWords(...(tol.pauses || []), (v) => `${v.toFixed(1)} s`, "shorter", "longer");
  const volume = pairWords(...(tol.volume || []), (v) => `${Math.round(v)} dB`, "quieter", "louder");
  return [pace && `pace ${pace}`, pauses && `a pause ${pauses}`, volume && `volume ${volume}`].filter(Boolean);
}

/** The reference mode used and the smallest changes it flags, from the result's own row thresholds; null when no row has one. */
function limitLine(r) {
  if (isSelf(r)) return SELF_LIMIT;
  const tol = Object.fromEntries((r.rows || []).filter((row) => LIMIT_ROWS.includes(row.key)).map((row) => [row.key, row.tol]));
  const parts = limitWords(tol);
  if (!parts.length) return null;
  const d = r.detection || {}, consensus = d.reference_mode === "consensus5";
  const unused = !consensus && d.references_available > 1 ? `Only the first of ${d.references_available} reference readings was used: five are needed to combine them. ` : "";
  const lead = consensus ? `With ${d.reference_count} reference readings` : "With one reference reading";
  const five = r.regime === "R2" && !consensus ? paceWords(S.flagLimits?.consensus5?.pace) : null;
  return `${unused}${lead}, changes smaller than these may not be flagged: ${parts.join(", ")}.` + (five ? ` With five readings, pace ${five} can be flagged.` : "");
}

function renderLimit(r) {
  const line = limitLine(r);
  $("#detect-limit").hidden = !line;
  $("#detect-limit").textContent = line || "";
}

/** Graded on its own, the ring holds the number of spots that stand out: a score against your own typical delivery is not a grade. */
function showSpots(r) {
  const n = r.flaws.length;
  S.countId += 1;
  for (const id of ["#ring-value", "#ring-glow"]) $(id).style.strokeDasharray = `0 ${RING_C.toFixed(2)}`;
  $("#overall-fig").textContent = String(n);
  $("#overall-fig").classList.remove("ticking");
  $(".ring-label").textContent = n === 1 ? "spot stands out" : "spots stand out";
}

function renderLedger(r) {
  $(".ring-wrap").classList.toggle("spots", isSelf(r));
  if (isSelf(r)) showSpots(r);
  else { $(".ring-label").textContent = "Delivery score"; showScore(r.scores.overall); }
  $("#regime-badge").textContent = regimeBadge(r);
  $("#regime-badge").hidden = false;
  // Only a combined reference needs saying; one reading is the default.
  const consensus = r.detection?.reference_mode === "consensus5";
  $("#reference-mode").hidden = !consensus;
  $("#reference-mode .badge").textContent = consensus ? `Compared with ${r.detection.reference_count} readings of the same text` : "";
  applyCopy(r);
  if (!isSelf(r)) $("#key-ref").textContent = r.detection?.reference_mode === "consensus5" ? `Reference: median of ${r.detection.reference_count} readings` : "Reference rendition";
  $("#key-stress").hidden = isSelf(r);
  renderSummary(r);
  renderLimit(r);
  const cards = $("#cards");
  cards.replaceChildren();
  for (const g of dimGroups(r)) {
    const scored = g.dims.filter((d) => d.scored);
    if (!scored.length) continue;   // only measures that score are shown; the notes name the others
    const value = scored.reduce((a, d) => a + d.score, 0) / scored.length;
    const keys = g.dims.map((d) => d.key);
    const n = r.flaws.filter((f) => keys.includes(f.dimension)).length;
    const card = el("button", { type: "button", class: "card", "aria-pressed": "false", "data-dims": keys.join(",") },
      el("div", { class: "word", text: groupLabel(g.word) }),
      el("div", { class: "fig", text: num(value, 1) }),
      el("div", { class: "bar" }, el("i", { style: `width:${Math.max(0, Math.min(100, value))}%` })),
      scored.length > 1 ? el("div", { class: "lines" }, ...scored.map((d) => el("div", { class: "line", title: `${d.note || ""} Coverage: ${num(d.coverage * 100, 0)}%.` },
        el("span", { text: SUB_NAME[d.key] || d.label }), el("span", { text: num(d.score, 1) })))) : null,
      n ? el("div", { class: "count flagged", text: `${n} ${n === 1 ? "finding" : "findings"}` }) : null);
    card.addEventListener("click", () => setFilter(S.filter && S.filter.join() === keys.join() ? null : keys));
    cards.append(card);
  }
}


function renderFilters(r) {
  const dimension = $("#dimension-filter"), pattern = $("#pattern-filter");
  dimension.replaceChildren(el("option", { value: "", text: "All measures" }));
  for (const g of dimGroups(r)) {
    if (g.dims.length > 1) dimension.append(el("option", { value: g.dims.map((d) => d.key).join(","), text: `${groupLabel(g.word)}, all` }));
    dimension.append(...g.dims.map((d) => el("option", { value: d.key, text: SUB_NAME[d.key] || d.label })));
  }
  const patterns = new Set([...r.flaws, ...differences()].flatMap((f) => [f.pattern, f.group_pattern]).filter(Boolean));
  pattern.replaceChildren(el("option", { value: "", text: "All patterns" }),
    ...[...patterns].sort().map((p) => el("option", { value: p, text: patternText(p) })),
    el("option", { value: "unlabelled", text: "Other findings" }));
}

function setFilter(keys) {
  S.filter = keys;
  document.querySelectorAll(".card").forEach((c) => c.setAttribute("aria-pressed", String(!!keys && c.dataset.dims === keys.join())));
  $("#dimension-filter").value = keys ? keys.join(",") : "";
  refreshLists();
}

function setPattern(pattern) {
  const chip = document.activeElement?.closest(".pattern-chip");
  const list = chip?.closest("#flaws, #differences, #listed, #clip-cards")?.id, finding = chip?.closest("[data-finding]")?.dataset.finding;
  S.pattern = pattern;
  $("#pattern-filter").value = pattern || "";
  refreshLists();
  if (!list) return;   // a chip outside the rebuilt lists keeps its focus
  // The lists are rebuilt, so keyboard focus moves to the same finding's new chip.
  const again = document.querySelector(`#${list} [data-finding="${CSS.escape(finding || "")}"] .pattern-chip`);
  (again || $("#pattern-filter")).focus();
}

function matchesFilter(f) {
  return (!S.filter || S.filter.includes(f.dimension)) && (!S.pattern ||
    (S.pattern === "unlabelled" ? !f.pattern : f.pattern === S.pattern || f.group_pattern === S.pattern));
}

function refreshLists() {
  $("#clear-filter").hidden = !S.filter && !S.pattern;
  renderFlawList();
  renderDifferenceList();
  renderClipCards();
  document.querySelectorAll(".pattern-chip").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.pattern === S.pattern)));
}

// A finding without a pattern label gets no chip; the pattern filter still offers "No pattern label".
function patternTags(f) {
  const p = f.pattern;
  const repeats = !!p && patternText(p) === findingText(f);   // e.g. uneven word timing: type and pattern share one name
  return el("div", { class: "finding-tags" },
    !p || repeats ? null : el("button", { type: "button", class: "pattern-chip", "data-pattern": p, "aria-pressed": String(S.pattern === p),
      "aria-label": `Filter by pattern: ${patternText(f.pattern)}`, onclick: () => setPattern(S.pattern === p ? null : p), text: patternText(f.pattern) }),
    f.candidate ? el("span", { class: "candidate", title: CANDIDATE_TEXT, text: "Candidate" }) : null,
    synthetic(f) ? el("span", { class: "candidate", title: SYNTHETIC_TEXT, text: "Synthetic only" }) : null);
}

function dimIcon(key) {
  const d = DIM_ICON[key];
  return d ? svgEl("svg", { class: "dim-icon", viewBox: "0 0 20 20", "aria-hidden": "true" }, svgEl("path", { d })) : null;
}

function findingGroups(r) {
  const groups = [], seen = new Set();
  r.flaws.forEach((f, i) => {
    if (seen.has(f.id)) return;
    const members = f.group ? r.flaws.map((x, j) => [x, j]).filter(([x]) => f.group.includes(x.id)) : [[f, i]];
    members.forEach(([x]) => seen.add(x.id));
    groups.push(members);
  });
  return groups;
}

function renderFlawList() {
  const r = S.result, list = $("#flaws");
  const shown = findingGroups(r).filter((members) => members.some(([f]) => matchesFilter(f)));
  const counted = (members) => members.find(([f]) => f.counted !== false) || members[0];
  if (S.priority != null && wholePassage(r.flaws[S.priority])) shown.sort((a, b) => Number(counted(b)[1] === S.priority) - Number(counted(a)[1] === S.priority));
  const n = shown.reduce((total, members) => total + members.length, 0);
  $("#flaw-count").textContent = `(${n}${n === r.flaws.length ? "" : " of " + r.flaws.length})`;
  list.replaceChildren();
  if (!shown.length) list.append(el("li", { class: "empty", text: r.flaws.length ? "No findings match these filters." : noRegions(r) }));
  const item = ([f, i]) => {
    const st = sevStyle(f.severity ?? 0);
    return el("li", { class: "finding-item", "data-finding": f.id },
      el("button", { type: "button", class: "finding-select", "aria-pressed": String(S.selKind === "flaw" && S.sel === i), "data-i": i,
        "data-kind": "flaw", "data-peek": i, onclick: () => select(i) },
        el("span", { class: "n", text: `#${i + 1}` }), el("span", { class: "t" }, dimIcon(f.dimension), findingText(f)),
        el("span", { class: "pts", text: f.counted === false ? "shared" : findingPts(f) }),
        el("span", { class: "m" }, el("span", { text: `${measureName(f)}, ${wholePassage(f) ? "whole passage" : span(f.p)}` }),
          el("i", { class: `dash ${st[2]}`, "aria-label": `Severity: ${st[2]}` }))), patternTags(f));
  };
  const groupItem = (members) => {
    if (members.length === 1) return item(members[0]);
    const [f, i] = counted(members);
    return el("li", { class: "finding-group" },
      el("button", { type: "button", class: "group-select", "data-i": i, "data-kind": "flaw",
        "aria-pressed": String(S.selKind === "flaw" && members.some(([, j]) => S.sel === j)), onclick: () => select(i) },
        el("span", { class: "t", text: `${groupName(f)} group` }), el("span", { class: "pts", text: findingPts(f) }),
        el("span", { class: "m", text: `${members.length} findings share one penalty` })),
      el("ul", { class: "flaws group-members" }, ...members.map(item)));
  };
  const minor = (members) => !saturated(counted(members)[0]) && (counted(members)[0].points_lost ?? 1) < 0.05;
  list.append(...shown.filter((members) => !minor(members)).map(groupItem));
  const folded = shown.filter(minor);
  if (folded.length) list.append(el("li", {}, el("details", {}, el("summary", { text: `Small findings (${folded.length}), under 0.05 points each` }),
    el("ul", { class: "flaws" }, ...folded.map(groupItem)))));
}

function renderDifferenceList() {
  const items = differences(), detection = S.result.detection;
  $("#differences-wrap").hidden = S.result.regime !== "R2";   // a reading graded on its own has listed context only
  $("#listed-wrap").hidden = !items.some((f) => f.status === "listed");
  $("#listed-count").textContent = `(${items.filter((f) => f.status === "listed" && matchesFilter(f)).length})`;
  const dimLabel = (key) => S.result.scores.dims.find((d) => d.key === key.replace(/[+-]$/, ""))?.label || key;
  $("#listed-note").textContent = isSelf() ? "Context for your reading from published reading norms; it does not change the score." : [...detection.listed_keys.map((k) => `${dimLabel(k)} (${k})`),
    ...detection.listed_clip_keys.map((k) => `${dimLabel(k)}, whole clip (${k})`)].join(", ") +
    ". Departures are shown without flags or point penalties. " +
    [...new Set(detection.listed_keys.map((k) => k.replace(/[+-]$/, "")))].map((k) => S.result.scores.dims.find((d) => d.key === k))
      .filter(Boolean).map((d) => `${d.label}: ${d.note}.`).join(" ");
  $("#key-difference").hidden = !items.length;
  for (const [selector, status] of [["#differences", "difference"], ["#listed", "listed"]]) {
    const list = $(selector);
    list.replaceChildren();
    items.forEach((f, i) => {
      if (f.status !== status || !matchesFilter(f)) return;
      list.append(el("li", { class: "finding-item", "data-finding": f.id },
        el("button", { type: "button", class: "finding-select", "data-i": i, "data-kind": "difference",
          "aria-pressed": String(S.selKind === "difference" && S.sel === i), onclick: () => select(i, { kind: "difference" }) },
          el("span", { class: "t", text: findingText(f) }), el("span", { class: "m", text: diffLine(f) })), patternTags(f)));
    });
    if (!list.children.length) list.append(el("li", { class: "empty", text: status === "listed" ? "No listed departures match these filters." : "No unscored differences match these filters." }));
  }
}

function renderClipCards() {
  const entries = [...S.result.flaws.map((f, i) => [f, i, "flaw"]), ...differences().map((f, i) => [f, i, "difference"])]
    .filter(([f]) => wholePassage(f) && matchesFilter(f));
  $("#clip-wrap").hidden = !entries.length;
  $("#clip-cards").replaceChildren(...entries.map(([f, i, kind]) => el("div", { class: "clip-card", "data-finding": f.id },
    el("button", { type: "button", "data-i": i, "data-kind": kind, "aria-pressed": String(S.selKind === kind && S.sel === i),
      onclick: () => select(i, { kind }) }, el("b", { text: findingText(f) }),
      el("span", { class: "note", text: kind === "flaw" ? `Whole clip, ${findingPts(f)}` : f.status === "listed" ? "Whole clip, listed, not scored" : "Whole clip difference, not scored" }),
      el("span", { text: unevenTempo(f) ? `Typical word-to-word factor: ${spreadFactor(f)}` : diffLine(f) }),
      unevenTempo(f) && f.threshold != null ? el("span", { class: "note", text: `Flag threshold: ${thresholdFactor(f)}` }) : null), patternTags(f))));
}

/** A whole-passage ratio as one statement, e.g. "speech time ×0.54 the reference's (faster)", or null for other values. */
function wholeRatio(f) {
  const q = WHOLE_RATIO[f.dimension];
  if (!q || !wholePassage(f) || valUnit(f) !== "×" || f.participant == null) return null;
  return `${q[0]} ×${num(f.participant, 2)} the reference's${f.participant === 1 ? "" : ` (${f.participant < 1 ? q[1] : q[2]})`}`;
}

// The reference value of D7 is carried to this recording's overall tempo; its evidence also lists the measured value.
const referenceText = (f) => isSelf() ? TYPICAL : f.dimension === "D7" ? "reference at this recording's tempo" : "reference";
// A no-reference result lists context against published norms, not against the reader: its own unit and text say what it is.
const listedContext = (f) => isSelf() && f.status === "listed";

function diffLine(f) {
  if (unevenTempo(f)) return `Whole passage: typical word-to-word factor ${spreadFactor(f)}${f.status === "listed" ? "; listed, not scored" : ""}.`;
  if (listedContext(f)) return `${wholePassage(f) ? "Whole passage" : span(f.p)}: ${num(f.participant, 2)} ${f.unit} in this reading`;
  const valueUnit = valUnit(f), v = (x) => withUnit(x, valueUnit);
  // A ratio value already states the factor, so the ln difference is not repeated as a second factor.
  const by = f.delta == null || valueUnit === "×" || REGULARISED.has(f.dimension) ? "" : f.unit === "ln" ? ` (${factor(f.delta)} ${isSelf() ? "your typical" : "the reference"})`
    : ` (${signed(f.delta)} ${UNIT[f.unit] || f.unit || ""})`;
  const values = wholeRatio(f) || `${referenceText(f)} ${v(f.baseline)}, this recording ${v(f.participant)}${by}`;
  return `${wholePassage(f) ? "Whole passage" : span(f.p)}: ${values}`;
}

function fact(dl, term, value) {
  dl.append(el("div", {}, el("dt", { text: term }), el("dd", { text: value })));
}

/** How far the measured departure lies past its flag threshold, drawn from the stored multiple of the threshold. */
function thresholdGauge(f) {
  const multiple = f.tolerance_multiple;
  if (multiple == null || !(multiple >= 0)) return null;
  const end = Math.max(2, Math.ceil(multiple * 1.15 * 2) / 2);   // scale end, in multiples of the threshold
  const at = (v) => 100 * Math.min(v, end) / end;
  const pct = (v) => `${at(v).toFixed(2)}%`;
  const over = multiple >= 1;
  const valueLabel = at(multiple) < 70 ? `left:calc(${pct(multiple)} + 6px)` : `right:calc(${(100 - at(multiple)).toFixed(2)}% + 0px)`;
  return el("div", { class: "gauge", "aria-hidden": "true" },
    el("p", { class: "note", text: "Distance past the flag threshold" }),
    el("div", { class: "gauge-track" }, el("i", { class: "gauge-tol", style: `width:${pct(1)}` }),
      over ? el("i", { class: "gauge-over", style: `left:${pct(1)};width:${(at(multiple) - at(1)).toFixed(2)}%` })
        : el("i", { class: "gauge-under", style: `width:${pct(multiple)}` }),
      el("i", { class: "gauge-tick", style: `left:${pct(1)}` }), el("i", { class: "gauge-knob", style: `left:${pct(multiple)}` })),
    el("div", { class: "gauge-labels" },
      el("span", { style: `right:calc(${(100 - at(1)).toFixed(2)}% + 6px)`, text: "Flag threshold" }),
      el("span", { class: "gauge-value", style: valueLabel, text: multipleText(multiple) })));
}

function evidenceValue(e) {
  if (e.value == null) return "Unavailable";
  if (typeof e.value === "boolean") return e.value ? "yes" : "no";
  if (typeof e.value !== "number") return String(e.value);
  if (e.unit === "ln") return factor(e.value);
  if (e.unit === "dB" || e.unit === "st") return `${signed(e.value, 1)} ${e.unit}`;
  if (e.unit === "count") return num(e.value, 0);
  return `${num(e.value, e.unit === "s" ? 2 : 1)} ${e.unit || ""}`.trim();
}

function renderExplain() {
  const box = $("#explain"), r = S.result, f = selected(), diff = S.selKind === "difference";
  box.replaceChildren();
  box.classList.remove("slide");
  void box.offsetWidth;   // restart the slide on every new selection
  box.classList.add("slide");
  $("#player-finding").textContent = !f ? "-" : diff ? findingText(f) : `#${S.sel + 1} ${findingText(f)}`;
  box.classList.toggle("neutral", diff);
  if (!f) {
    box.append(el("h3", { text: "Your reading" }), el("p", { class: "empty", text: r.flaws.length ? "Select a finding to read it." : noRegions(r) }));
    return;
  }
  const valueUnit = valUnit(f), deltaUnit = UNIT[f.unit] || f.unit || "";
  const ratio = f.unit !== "ln" || f.delta == null ? "" : REGULARISED.has(f.dimension) && valUnit(f) !== "×"
    ? ` (${factor(f.delta)} after the same small constant is added to both values)` : ` (${factor(f.delta)})`;
  const dl = el("dl", { class: "facts" });
  if (unevenTempo(f)) {
    fact(dl, "Typical word-to-word factor", spreadFactor(f));
    fact(dl, "Robust spread", `${num(f.participant, 2)} ln`);
  } else if (listedContext(f)) {
    fact(dl, "This reading", `${num(f.participant, 2)} ${f.unit}`);
  } else {
    const whole = wholeRatio(f);
    if (whole) fact(dl, "This recording", whole);
    else {
      fact(dl, referenceText(f)[0].toUpperCase() + referenceText(f).slice(1), withUnit(f.baseline, valueUnit));
      fact(dl, "This recording", withUnit(f.participant, valueUnit));
    }
    fact(dl, "Difference", `${signed(f.delta)} ${deltaUnit}${ratio}`);
  }
  if (!diff) {
    fact(dl, "Points lost", f.points_lost == null ? "-" : !shownLoss(f.points_lost) ? "<0.01" : num(f.points_lost, 2));
    if (saturated(f)) fact(dl, `${dimText(f)}, points lost in total`, num(f.dimension_points_lost, 2));
    else if (zeroLoss(f)) fact(dl, `${dimText(f)} loss carried by`, `#${lossCarrier(f) + 1} (${ptsText(r.flaws[lossCarrier(f)].points_lost)})`);
    fact(dl, "Score if fixed", f.overall_if_fixed == null ? "-" : scoreText(f.overall_if_fixed));
    fact(dl, "Times the flag threshold", multipleText(f.tolerance_multiple));
    fact(dl, "Flag threshold", f.threshold == null ? "-" : unevenTempo(f) ? thresholdFactor(f) : `${f.delta < 0 ? "−" : "+"}${num(f.threshold, 2)} ${deltaUnit}`);
  }
  const pts = diff ? null : f.counted === false ? "shared" : findingPts(f);
  const why = diff ? (isSelf() ? "Shown as context; it does not change the score." : "Shown for comparison with the reference; it does not change the score.")
    : f.tolerance_multiple != null ? `It counts because it is ${multipleText(f.tolerance_multiple)} the flag threshold for this measure.` : "";
  box.append(
    el("div", { class: "ex-head" },
      el("div", {},
        el("h3", {}, diff ? null : el("span", { class: "ex-num", text: `#${S.sel + 1}` }), diff ? null : " ", findingText(f)),
        el("p", { class: "ex-status", text: `${measureName(f)}, ${wholePassage(f) ? "whole passage" : span(f.p)}` }),
        patternTags(f)),
      pts ? el("p", { class: "ex-pts" }, pts, el("small", { text: f.counted === false ? "carried by the group" : "from your score" })) : null),
    el("p", { class: "ex-words", text: quotedWords(r, f) }),
    el("p", { class: "ex-what", text: plainLine(f) }),
    why ? el("p", { class: "ex-why", text: why }) : "",
    diff ? "" : thresholdGauge(f) ?? "",
    el("div", { class: "card-actions" },
      el("button", { type: "button", class: "listen-btn", "data-audio": listenAudio(), ...(diff ? {} : { "data-listen": S.sel }), onclick: () => listen(S.sel, S.selKind) }, "Listen"),
      diff ? null : fixButton(f, S.sel)),
    // what Listen plays, as a caption under the buttons, so the time ranges never wrap inside a button
    el("p", { class: "listen-caption" }, ...(isSelf() ? (f.p ? ["Listen plays this spot, ", el("span", { class: "nowrap", text: span(f.p) }), "."] : ["Listen plays from the start."])
      : ["Listen plays yours, ", el("span", { class: "nowrap", text: span(f.p) }), ", then the reference, ", el("span", { class: "nowrap", text: span(f.b) }), "."])),
    diff ? "" : fixerView(f));
  if (!diff && f.fix) box.append(el("p", { class: "fix" }, el("b", { text: "How to fix" }), f.fix));
  tickPoints(box.querySelectorAll(".ex-pts"));
  if (f.candidate) box.append(el("p", { class: "candidate-note", text: CANDIDATE_TEXT }));
  if (f.group) {
    const members = r.flaws.filter((x) => f.group.includes(x.id));
    box.append(el("p", { class: "group-note", text: `${groupName(f)} group: ${members.length} findings share one penalty. ${f.counted === false ? "This member adds no points lost; the counted member carries the group's penalty." : "The score if fixed removes the whole group's penalty."}` }),
      el("div", { class: "group-links" }, ...members.map((member) => el("button", { type: "button", class: "plain",
        onclick: () => select(r.flaws.indexOf(member)), text: `#${r.flaws.indexOf(member) + 1} ${findingText(member)} (${measureName(member)})` }))));
  }
  const detail = el("details", { class: "measure-details" }, el("summary", { text: "Details" }), dl,
    listedContext(f) ? null : el("p", { class: "what", text: (f.candidate ? f.text.replace(CANDIDATE_TEXT, "").trim() : f.text) || "" }));
  if (f.evidence?.length) {
    const evidence = el("dl", { class: "facts evidence" });
    // The finding's own measure shows the Difference row's factor: a second rounding of the stored value can differ by 0.01.
    f.evidence.forEach((e) => fact(evidence, e.label || e.key, unevenTempo(f) && e.key === "spread_ln" ? spreadFactor(f)
      : e.key === OWN_EVIDENCE[f.dimension] && f.delta != null ? factor(f.delta) : evidenceValue(e)));
    detail.append(el("h4", { text: "Measured evidence" }), evidence);
  }
  if (f.span_kind) detail.append(el("p", { class: "measure", text: `Evidence span: ${f.span_kind}.` }));
  if (f.context) detail.append(el("p", { class: "measure", text: f.context }));
  if (!diff) {
    if (f.overall_if_fixed != null) detail.append(el("p", { class: "measure", text: "The score if fixed removes this finding's points arithmetically; it does not predict the score of a new recording." }));
    if (f.measure) detail.append(el("p", { class: "measure", text: `Measured as: ${f.measure}.` }));
    if (f.why && f.dimension !== "D6") detail.append(el("blockquote", { class: "why", text: f.why }));
  }
  box.append(detail);
  updatePlayback();
}

/**
 * Scroll each scroll box from the button out to the list column (the column beside the chart on wide screens, the
 * lists under it on narrow screens) until the button shows, without moving the page. A box puts `head` at its top
 * when the button then also shows, so the heading of the button's list stays in view.
 */
function revealInSide(btn, head = btn) {
  const side = btn?.closest(".side");
  if (!side) return;
  for (let box = btn.parentElement; box && side.contains(box); box = box.parentElement) {
    if (box.scrollHeight <= box.clientHeight || getComputedStyle(box).overflowY === "visible") continue;
    const b = btn.getBoundingClientRect(), s = box.getBoundingClientRect();
    if (b.top >= s.top && b.bottom <= s.bottom) continue;
    const h = box.contains(head) ? head.getBoundingClientRect() : b;
    box.scrollTop += (b.bottom - h.top + 16 <= s.height ? h.top : b.top) - s.top - 8;
  }
}

// reveal: false on a page load without a focus id, where scrolling the list column would hide its heading above the fold.
function select(i, { scroll = false, kind = "flaw", reveal = true } = {}) {
  const before = rowDefs(S.result).map((d) => d.key).join();
  S.sel = i; S.selKind = kind;
  document.querySelectorAll("button[data-kind]").forEach((b) => {
    const isItem = +b.dataset.i === i && b.dataset.kind === kind;
    const isGroup = kind === "flaw" && b.classList.contains("group-select") && selected()?.group?.includes(S.result.flaws[+b.dataset.i].id);
    b.setAttribute("aria-pressed", String(isItem || isGroup));
  });
  const selector = `button[data-i="${i}"][data-kind="${kind}"]`;
  const btn = document.querySelector(kind === "difference" ? `#differences ${selector}, #listed ${selector}` : `#flaws ${selector}`);
  if (btn?.closest("details")) btn.closest("details").open = true;
  if (reveal) revealInSide(btn);
  if (scroll) revealSelection();
  renderExplain();
  markWords();
  markTimeline();
  if (S.chart && before !== rowDefs(S.result).map((d) => d.key).join()) drawChart();
  else highlight();
  updateWaveRegions();
  const f = selected();
  if (S.youReady && f) S.ws.setTime(mediaSpan(f, "you")[0]);
}

/** On a wide screen the panel sits beside the text, so the words scroll into view; on a narrow one the panel does. */
function revealSelection() {
  const f = selected(), behavior = reducedMotion() ? "auto" : "smooth";
  const word = f && !wholePassage(f) ? document.querySelector(`#transcript .w[data-i="${f.words[0]}"]`) : null;
  if (matchMedia("(min-width: 1061px)").matches && word) word.scrollIntoView({ block: "nearest", behavior });
  else $("#explain").scrollIntoView({ block: "nearest", behavior });
}

// ---------------------------------------------------------------------------------------------------- transcript
function renderTranscript(r) {
  const box = $("#transcript");
  box.replaceChildren();
  const wordStyle = new Array(r.words.length).fill(null), wordFinding = new Array(r.words.length).fill(-1);
  r.flaws.forEach((f, k) => {
    if (wholePassage(f)) return;   // clip-level: no word run to underline
    const st = sevStyle(f.severity ?? 0);
    for (let i = f.words[0]; i <= f.words[1]; i++) {
      if (wordFinding[i] < 0 || (f.points_lost ?? 0) > (r.flaws[wordFinding[i]].points_lost ?? 0)) wordFinding[i] = k;
      if (!wordStyle[i] || SEVERITY_STYLES.indexOf(st) > SEVERITY_STYLES.indexOf(wordStyle[i])) wordStyle[i] = st;
    }
  });
  r.words.forEach((w, i) => {
    const k = wordFinding[i];
    if (k >= 0 && wordFinding[i - 1] !== k) box.append(dimIcon(r.flaws[k].dimension) || "");
    const b = el("button", { type: "button", class: "w" + (wordStyle[i] ? ` f-${wordStyle[i][1]}` : ""), "data-i": i, text: w.w });
    if (k >= 0) {
      b.dataset.peek = k;
      b.setAttribute("aria-label", `${w.w}: finding #${k + 1} ${findingText(r.flaws[k])}`);
      b.addEventListener("click", () => select(k, { scroll: true }));
    } else {
      b.dataset.audio = "you";
      b.addEventListener("click", () => playSpan("you", [w.p[0], w.p[1] + 0.25]));
    }
    box.append(b, " ");
  });
}

function markWords() {
  const f = selected();
  $("#whole-note").hidden = !(f && wholePassage(f));
  document.querySelectorAll("#transcript .w").forEach((b) => {
    const i = +b.dataset.i;
    const on = !!f && !wholePassage(f) && i >= f.words[0] && i <= f.words[1];
    b.classList.toggle("sel", on && S.selKind === "flaw");
    b.classList.toggle("neutral-sel", on && S.selKind === "difference");
    const grouped = S.selKind === "flaw" && f?.group && S.result.flaws.some((member) => f.group.includes(member.id) &&
      i >= member.words[0] && i <= member.words[1]);
    b.classList.toggle("group-word", !!grouped);
  });
}

/** Karaoke: the word at time t of the playing reading (who: "you" or "ref") lights up and the words before it dim. */
function markPlaying(t, who = "you") {
  const ws = S.result.words, key = who === "ref" ? "b" : "p";
  if (!ws.length || !ws[0][key]) return;
  let lo = 0, hi = ws.length - 1;
  while (lo < hi) { const m = (lo + hi + 1) >> 1; if (ws[m][key][0] <= t) lo = m; else hi = m - 1; }
  const on = t >= ws[lo][key][0] && t <= ws[lo][key][1] + 0.2;
  document.querySelectorAll("#transcript .w").forEach((b) => {
    const i = +b.dataset.i;
    if (i === lo && on) b.setAttribute("aria-current", "true"); else b.removeAttribute("aria-current");
    b.classList.toggle("spoken", i < lo);
  });
  pulseEntered(who === "ref" ? interp(t, S.result.map.b, S.result.map.p) : t);
}

/** When the playhead enters a flagged span, that finding's card, list entry and band pulse once. */
function pulseEntered(tp) {
  const now = new Set(S.result.flaws.map((f, i) => [f, i]).filter(([f]) => !wholePassage(f) && tp >= f.p[0] && tp <= f.p[1]).map(([, i]) => i));
  for (const i of now) {
    if (S.inSpan.has(i)) continue;
    document.querySelectorAll(`.top-card[data-i="${i}"], #flaws button[data-i="${i}"][data-kind="flaw"], .tl-band[data-i="${i}"], .tl-mk[data-i="${i}"]`).forEach((n) => {
      n.classList.remove("pulse");
      void n.getBoundingClientRect();   // restart the animation on a repeated entry
      n.classList.add("pulse");
    });
  }
  S.inSpan = now;
}

function clearKaraoke() {
  document.querySelectorAll("#transcript .w").forEach((b) => { b.removeAttribute("aria-current"); b.classList.remove("spoken"); });
  S.inSpan = new Set();
}

// ---------------------------------------------------------------------------------------------------- timeline
/** A finding's span in the reference: its own b span, else its recording span carried through the word map. */
function referenceSpan(f) {
  const m = S.result.map;
  return f.b || [interp(f.p[0], m.p, m.b), interp(f.p[1], m.p, m.b)];
}

const SEVERITY_DASH = { dot: "1.5 2.5", dash: "5 3", solid: "none" };
const severityTier = (f) => sevStyle(f.severity ?? 0)[1];

const atOnePoint = (p) => p[1] - p[0] < DISPLAY_HOP_S;   // a missing pause starts and ends at the same time
const widenSpan = (a, b) => b - a >= TL_MIN_SPAN_PX ? [a, b] : [(a + b) / 2 - TL_MIN_SPAN_PX / 2, (a + b) / 2 + TL_MIN_SPAN_PX / 2];

/** Marker-line lanes: a fault that overlaps an earlier one on the timeline gets its own line above it, so each span stays legible. */
function edgeLanes(r, x) {
  const ends = [], lane = new Map();
  r.flaws.map((f, i) => [i, ...widenSpan(...f.p.map(x))]).filter(([i]) => !wholePassage(r.flaws[i]))
    .sort((a, b) => a[1] - b[1] || b[2] - a[2]).forEach(([i, x0, x1]) => {
      let k = ends.findIndex((end) => end + TL_LANE_PX <= x0);
      if (k < 0) { k = ends.length; ends.push(x1); } else ends[k] = x1;
      lane.set(i, k);
    });
  return { lane, count: Math.max(1, ends.length) };
}

/** The local findings that each word of this recording belongs to (word index -> finding indices). */
function faultsByWord(r) {
  const out = new Map();
  r.flaws.forEach((f, i) => {
    if (wholePassage(f)) return;
    for (let w = f.words[0]; w <= f.words[1]; w++) out.set(w, [...(out.get(w) || []), i]);
  });
  return out;
}

/** One finding on this recording's track: a thin marker line in the severity style (dotted, dashed, solid) above the word
 *  ticks, in its own lane where faults overlap, over a clear hit area; with a reference, its reference span and a thin link
 *  to it, which style.css shows only while the finding is hovered or selected. The waveform below recolours its bars. */
function bandParts(f, i) {
  const g = S.tl, [p0, p1] = widenSpan(...f.p.map(g.x)), tier = severityTier(f), edgeY = g.edgeY(i), mid = (p0 + p1) / 2;
  // a fault at one point in time (a missing pause) gets an upright pin down to the track, as its hairline on the waveform
  const point = atOnePoint(f.p);
  const parts = [svgEl("rect", { class: "hit", x: p0, y: edgeY - TL_LANE_PX, width: p1 - p0, height: g.youBot - edgeY + TL_LANE_PX }),
    svgEl("line", { class: `edge sev-${tier}${point ? " pin" : ""}`, x1: point ? mid : p0, x2: point ? mid : p1, y1: edgeY, y2: point ? g.youTop - 1 : edgeY,
      "stroke-dasharray": SEVERITY_DASH[tier] })];
  if (!g.own) {
    const [b0, b1] = widenSpan(...referenceSpan(f).map(g.x)), bx = (b0 + b1) / 2, bend = (g.refBot + edgeY) / 2;
    parts.push(svgEl("g", { class: "tl-link" },
      svgEl("rect", { class: "ref-span", x: b0, y: g.refTop, width: b1 - b0, height: TL_REF_TRACK_PX, rx: TL_REF_TRACK_PX / 2 }),
      svgEl("path", { class: "link", d: `M${bx},${g.refBot} C${bx},${bend} ${mid},${bend} ${mid},${edgeY}` })));
  }
  return { p0, p1, parts };
}

/**
 * The fault labels: members of one finding group that touch share one label ("×2"). Each label sits over its region,
 * the most costly first, in the lowest of TL_MARK_ROWS rows where it touches no other label; a label that does not fit
 * at full length tries its number alone; one that still does not fit is counted under the panel.
 */
function placeMarks(r, x, width) {
  const top = new Map(topFindings(r).map(([, i], rank) => [i, rank]));
  const marks = [];
  r.flaws.forEach((f, i) => {
    if (wholePassage(f)) return;
    const joined = f.group && marks.find((m) => m.members.some((j) => f.group.includes(r.flaws[j].id))
      && f.p[0] <= m.t1 + TL_JOIN_S && f.p[1] >= m.t0 - TL_JOIN_S);
    if (joined) { joined.members.push(i); joined.t0 = Math.min(joined.t0, f.p[0]); joined.t1 = Math.max(joined.t1, f.p[1]); }
    else marks.push({ members: [i], t0: f.p[0], t1: f.p[1] });
  });
  const cost = (i) => r.flaws[i].counted === false ? 0 : r.flaws[i].points_lost ?? 0;
  for (const m of marks) {
    m.main = m.members.reduce((best, i) => cost(i) > cost(best) ? i : best, m.members[0]);
    m.rank = Math.min(...m.members.map((i) => top.get(i) ?? Infinity));
    const f = r.flaws[m.main];
    m.number = `#${m.main + 1}`;
    m.title = `${findingText(f)}${m.members.length > 1 ? ` ×${m.members.length}` : ""}`;
    m.points = Number.isFinite(m.rank) ? `−${num(f.points_lost, 2)}` : "";
    m.cx = (x(m.t0) + x(m.t1)) / 2;
  }
  const rows = Array.from({ length: TL_MARK_ROWS }, () => []), hidden = [];
  const order = [...marks].sort((a, b) => a.rank - b.rank || cost(b.main) - cost(a.main) || a.t0 - b.t0);
  const fits = (row, x0, x1) => rows[row].every((o) => x1 + TL_MARK_GAP <= o.x0 || x0 >= o.x1 + TL_MARK_GAP);
  for (const m of order) {
    const full = textWidth(m.number, TL_MARK_FONT, 700) + textWidth(` ${m.title}`, TL_MARK_FONT)
      + (m.points ? textWidth(` ${m.points}`, TL_MARK_FONT, 700) + 4 : 0) + 18;
    const short = textWidth(m.number, TL_MARK_FONT, 700) + 16;
    // a candidate costs its row and its sideways shift; a full label may move a little, a number alone further, with a leader
    const candidates = (w, compact, reach) => rows.flatMap((_, row) => Array.from({ length: 2 * Math.floor(reach / 8) + 1 }, (__, k) => {
      const shift = (k % 2 ? 1 : -1) * Math.ceil(k / 2) * 8, x0 = Math.min(Math.max(m.cx - w / 2 + shift, 0), width - w);
      return fits(row, x0, x0 + w) ? { row, x0, w, compact, cost: row * 24 + Math.abs(x0 + w / 2 - m.cx) } : null;
    })).filter(Boolean).sort((a, b) => a.cost - b.cost)[0];
    const spot = candidates(full, false, TL_MARK_REACH_PX) || candidates(short, true, 3 * TL_MARK_REACH_PX);
    if (!spot) { hidden.push(m); continue; }
    Object.assign(m, spot);
    rows[spot.row].push({ x0: spot.x0, x1: spot.x0 + spot.w });
  }
  return { marks: marks.filter((m) => !hidden.includes(m)), hidden, rows: Math.max(1, ...marks.filter((m) => !hidden.includes(m)).map((m) => m.row + 1)) };
}

/**
 * The reference reading above this recording, word by word on one time scale (the longer reading sets the scale). Each local
 * finding is one region on this recording's track, labelled above it; the waveform below uses the same scale.
 */
function drawTimeline() {
  const host = $("#tl-host"), r = S.result;
  S.tl = null;
  if (!r || !host.clientWidth) return;
  const width = host.clientWidth, own = isSelf(r);
  const pxPerS = Math.max(width - PLOT_R, 1) / Math.max(r.participant.duration, r.baseline.duration);
  const x = (t) => t * pxPerS, layout = placeMarks(r, x, width - PLOT_R), lanes = edgeLanes(r, x);
  // rows from the top: reference track, gap, the "This recording" label, the fault labels, the marker lines, this recording's track
  const refTop = 0, refBot = own ? 0 : TL_REF_TRACK_PX, labelMid = refBot + (own ? 0 : TL_LINK_GAP_PX) + TL_LABEL_PX / 2;
  const marksTop = labelMid + TL_LABEL_PX / 2;
  const youTop = marksTop + layout.rows * (TL_MARK_H + TL_MARK_GAP) + TL_EDGE_PX + lanes.count * TL_LANE_PX, youBot = youTop + TL_TRACK_PX;
  const edgeY = (i) => youTop - TL_EDGE_PX - (lanes.lane.get(i) ?? 0) * TL_LANE_PX;
  S.tl = { x, refTop, refBot, youTop, youBot, edgeY, width, own, chipOf: new Map() };
  const g = S.tl;
  const svg = svgEl("svg", { width, height: youBot, viewBox: `0 0 ${width} ${youBot}`, role: "group",
    "aria-label": own ? "This recording, word by word, with numbered flagged regions" : "Reference and this recording, word by word, with numbered flagged regions" });
  $("#lane-ref").hidden = own;
  svg.append(svgEl("text", { class: "tl-label you", x: 0, y: labelMid, "dominant-baseline": "central", text: "This recording" }));
  // the words of a finding keep their ticks, tinted in the strongest severity among their findings
  const faults = faultsByWord(r), tiers = ["dot", "dash", "solid"];
  const tickClass = (who, k) => {
    const of = who === "you" ? faults.get(k) : null;
    if (!of) return { class: `tl-word ${who}` };
    const tier = tiers[Math.max(...of.map((i) => tiers.indexOf(severityTier(r.flaws[i]))))];
    return { class: `tl-word ${who} flag sev-${tier}`, "data-faults": of.join(",") };
  };
  const track = (who, key, top, height) => svgEl("g", { "aria-hidden": "true" }, ...r.words.map((w, k) => [w, k]).filter(([w]) => w[key]).map(([w, k]) => {
    const x0 = g.x(w[key][0]), wide = Math.max(g.x(w[key][1]) - x0 - 1, 1);
    return svgEl("g", { ...tickClass(who, k), onclick: () => playSpan(who, [w[key][0], w[key][1] + 0.25]),
      onpointerenter: (e) => showTip(e.currentTarget, `${w.w}  ${span(w[key])}`), onpointerleave: hideTip },
      svgEl("rect", { x: x0, y: top, width: wide, height, rx: Math.min(4, height / 2) }));
  }));
  svg.append(own ? "" : track("ref", "b", refTop, TL_REF_TRACK_PX), track("you", "p", youTop, TL_TRACK_PX));
  const bands = svgEl("g", {}), stems = svgEl("g", { class: "tl-stems", "aria-hidden": "true" }), markers = svgEl("g", {});
  const order = r.flaws.map((f, i) => i).filter((i) => !wholePassage(r.flaws[i]));   // intro order: by time
  const seq = (i) => `--seq:${Math.min(order.indexOf(i), BAND_STEPS)}`;
  layout.marks.concat(layout.hidden).forEach((m, k) => m.members.forEach((i) => g.chipOf.set(i, k)));
  r.flaws.forEach((f, i) => {
    if (wholePassage(f)) return;   // listed and explained in the whole-clip cards, not painted over the readings
    bands.append(svgEl("g", { class: "tl-band", "data-i": i, "data-chip": g.chipOf.get(i), "data-peek": i, style: seq(i), onclick: () => select(i, { scroll: true }), "aria-hidden": "true" },
      svgEl("title", { text: `#${i + 1} ${findingText(f)}` }), ...bandParts(f, i).parts));
  });
  layout.marks.forEach((m) => {
    const f = r.flaws[m.main], y = marksTop + (layout.rows - 1 - m.row) * (TL_MARK_H + TL_MARK_GAP) + TL_MARK_H / 2;
    const pick = () => select(m.main, { scroll: true }), tier = severityTier(f), cx = m.x0 + m.w / 2;
    const name = `${m.number} ${m.title}${m.points ? `, ${m.points} points` : ""}`;
    // a label moved off its region keeps a leader from its own middle to the region
    const from = Math.min(Math.max(m.cx, m.x0 + TL_MARK_H / 2), m.x0 + m.w - TL_MARK_H / 2);
    stems.append(svgEl("line", { class: "tl-stem", "data-chip": g.chipOf.get(m.main), style: seq(m.main), x1: from, x2: m.cx, y1: y + TL_MARK_H / 2, y2: g.edgeY(m.main) }));
    markers.append(svgEl("g", { class: `tl-mk${Number.isFinite(m.rank) ? " top" : ""}${m.compact ? " compact" : ""}`, "data-i": m.main, "data-members": m.members.join(","),
      "data-chip": g.chipOf.get(m.main), "data-peek": m.main, style: seq(m.main), tabindex: 0, role: "button", "aria-pressed": "false",
      "aria-label": `${name}: this recording ${span([m.t0, m.t1])}${f.b && !own ? `, reference ${span(referenceSpan(f))}` : ""}`,
      onclick: pick, onkeydown: (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); } },
      onpointerenter: m.compact ? (e) => showTip(e.currentTarget, name) : null, onpointerleave: m.compact ? hideTip : null },
      svgEl("rect", { x: m.x0, y: y - TL_MARK_H / 2, width: m.w, height: TL_MARK_H, rx: TL_MARK_H / 2, "stroke-dasharray": SEVERITY_DASH[tier] }),
      svgEl("text", { x: m.compact ? cx : m.x0 + 9, y, "text-anchor": m.compact ? "middle" : "start" },
        svgEl("tspan", { class: "n", text: m.number }),
        ...(m.compact ? [] : [svgEl("tspan", { text: ` ${m.title}` }), m.points ? svgEl("tspan", { class: "pts", dx: 4, text: ` ${m.points}` }) : null]))));
  });
  svg.append(svgEl("g", { id: "tl-diff" }), bands, stems, markers,
    own ? "" : svgEl("line", { id: "tl-cur-ref", class: "tl-cursor", y1: refTop - 3, y2: refBot + 3, style: "display:none" }),
    svgEl("line", { id: "tl-cur-you", class: "tl-cursor", y1: youTop - 3, y2: youBot + 3, style: "display:none" }));
  host.replaceChildren(svg);
  const more = layout.hidden.reduce((n, m) => n + m.members.length, 0);
  $("#tl-more").hidden = !more;
  $("#tl-more").textContent = `${more} more ${more === 1 ? "finding" : "findings"} in the list`;
  for (const [id, seconds] of [["#wave", r.participant.duration], ["#wave-ref", r.baseline.duration]]) {
    $(id).style.width = `${Math.max(seconds * pxPerS, 1)}px`;
  }
  markTimeline();
  paintWave();
}

function markTimeline() {
  const svg = $("#tl-host svg");
  if (!svg || !S.tl || !S.result) return;
  const f = selected(), flaw = S.selKind === "flaw";
  const inGroup = (i) => flaw && !!f?.group?.includes(S.result.flaws[i].id);
  svg.classList.toggle("has-sel", flaw && S.sel != null && S.tl.chipOf.has(S.sel));
  svg.querySelectorAll(".tl-band[data-i]").forEach((band) => {
    const i = +band.dataset.i, on = flaw && S.sel === i;
    band.classList.toggle("sel", on);
    band.classList.toggle("grp", !on && inGroup(i));
  });
  svg.querySelectorAll(".tl-mk").forEach((mk) => {
    const members = mk.dataset.members.split(",").map(Number), on = flaw && members.includes(S.sel);
    mk.classList.toggle("sel", on);
    mk.classList.toggle("grp", !on && members.some(inGroup));
    mk.setAttribute("aria-pressed", String(on));
  });
  svg.querySelectorAll(".tl-stem").forEach((stem) => stem.classList.toggle("sel", flaw && +stem.dataset.chip === S.tl.chipOf.get(S.sel)));
  svg.querySelectorAll(".tl-word.flag").forEach((tick) => {
    const of = tick.dataset.faults.split(",").map(Number), on = flaw && of.includes(S.sel);
    tick.classList.toggle("sel", on);
    tick.classList.toggle("grp", !on && of.some(inGroup));
  });
  const layer = svg.querySelector("#tl-diff");
  layer.replaceChildren();
  if (!flaw && f && !wholePassage(f)) layer.append(svgEl("g", { class: "tl-band tl-diff sel", "aria-hidden": "true" }, ...bandParts(f, null).parts));
}

/** Playhead on both tracks: tp in this recording, tb in the reference (s). */
function moveTimelineCursor(tp, tb) {
  if (!S.tl) return;
  for (const [id, t] of [["#tl-cur-you", tp], ["#tl-cur-ref", tb]]) {
    const line = $(id);
    if (!line) continue;
    line.setAttribute("x1", S.tl.x(t));
    line.setAttribute("x2", S.tl.x(t));
    line.style.display = "";
  }
}

/** Linked highlighting: one finding's words and band stay bright while the other flagged words and bands fade. */
function peek(i) {
  const on = i != null && i !== "";
  const waveFault = on && S.result?.flaws[+i] && !wholePassage(S.result.flaws[+i]) ? +i : null;
  if (waveFault !== S.peekI) { S.peekI = waveFault; paintWaveSoon(); }
  document.body.classList.toggle("peeking", on);
  document.querySelectorAll(".peek").forEach((n) => n.classList.remove("peek"));
  if (!on) return;
  const f = S.result?.flaws[+i];
  if (!f) return;
  const chip = S.tl?.chipOf.get(+i);
  document.querySelectorAll(`.tl-band[data-i="${i}"], .tl-mk[data-i="${i}"], .top-card[data-i="${i}"]${chip == null ? "" : `, [data-chip="${chip}"]`}`).forEach((n) => n.classList.add("peek"));
  document.querySelectorAll("#tl-host .tl-word.flag").forEach((tick) => { if (tick.dataset.faults.split(",").includes(String(i))) tick.classList.add("peek"); });
  if (!wholePassage(f)) for (let w = f.words[0]; w <= f.words[1]; w++) document.querySelector(`#transcript .w[data-i="${w}"]`)?.classList.add("peek");
}

function linkPeek() {
  const target = (e) => e.target.closest?.("[data-peek]");
  for (const [enter, leave] of [["pointerover", "pointerout"], ["focusin", "focusout"]]) {
    document.addEventListener(enter, (e) => { const t = target(e); if (t) peek(t.dataset.peek); });
    document.addEventListener(leave, (e) => { const t = target(e); if (t && !t.contains(e.relatedTarget)) peek(null); });
  }
}

function showTip(target, text) {
  const tip = $("#tl-tip"), box = target.getBoundingClientRect(), host = $(".tl-stage").getBoundingClientRect();
  tip.textContent = text;
  tip.hidden = false;
  const left = Math.min(Math.max(box.left + box.width / 2 - host.left - tip.offsetWidth / 2, 8), host.width - tip.offsetWidth - 8);
  tip.style.left = `${left}px`;
  tip.style.top = `${box.top - host.top - tip.offsetHeight - 6}px`;
}

function hideTip() {
  $("#tl-tip").hidden = true;
}

function hideTimelineCursor() {
  document.querySelectorAll(".tl-cursor").forEach((line) => { line.style.display = "none"; });
}

// ---------------------------------------------------------------------------------------------------- chart
function rowDefs(r) {
  const defs = [], dims = new Set(r.flaws.map((f) => f.dimension));
  const f = selected();
  if (f) dims.add(f.dimension);
  for (const x of differences()) dims.add(x.dimension);   // a listed difference earns its row
  for (const row of r.rows) {
    if (row.status === "absent") continue;   // a measure this mode does not take (no reference reading)
    if (!S.allDimensions && !ROWS[row.key]?.frame && !dims.has(ROWS[row.key]?.dim)) continue;
    if (row.key === "emphasis" && r.stress) defs.push({ key: "stress", row: { key: "stress", unit: "" } });
    if (ROWS[row.key]) defs.push({ key: row.key, row });
  }
  return defs;
}

/** Diagonal lines clipped to [x0, x1] in data x and [0, 1] in domain y, as one SVG path; slant is the x run of one line. */
function hatchPath(x0, x1, step, slant) {
  const parts = [];
  for (let u = x0 - slant; u < x1; u += step) {
    const t0 = Math.max(0, (x0 - u) / slant), t1 = Math.min(1, (x1 - u) / slant);
    if (t1 > t0) parts.push(`M${u + t0 * slant},${t0}L${u + t1 * slant},${t1}`);
  }
  return parts.join("");
}

/** Segments of constant value across each word (x: start, middle, end, gap), the delta rows' form. */
function wordSegments(words, vals) {
  const x = [], y = [], c = [];
  vals.forEach((v, i) => {
    if (v == null || !words[i]) return;
    const [s, e] = words[i].p;
    x.push(s, (s + e) / 2, e, null); y.push(v, v, v, null); c.push(words[i].w, words[i].w, words[i].w, "");
  });
  return { x, y, c };
}

function eventBars(words, vals, isGap) {
  const x = [], y = [], w = [], c = [];
  vals.forEach((v, i) => {
    if (v == null || !words[i]) return;
    if (isGap) {
      if (!words[i + 1]) return;
      const a = words[i].p[1], b = words[i + 1].p[0];
      x.push((a + b) / 2); w.push(Math.max(b - a, 0.06)); c.push(`between ${words[i].w} and ${words[i + 1].w}`);
    } else {
      x.push((words[i].p[0] + words[i].p[1]) / 2); w.push(Math.max(words[i].p[1] - words[i].p[0], 0.06)); c.push(words[i].w);
    }
    y.push(v);
  });
  return { x, y, w, c };
}

function chartModel(r) {
  const c = { ink: css("--ink"), ink2: css("--ink2"), muted: css("--muted"), rule: css("--rule"), surface: css("--surface"),
    ref: css("--ref"), you: css("--you"), flag: css("--flag"), flagText: css("--flag-text"), neutral: css("--neutral"), tol: css("--tol") };
  const width = $("#chart-host").clientWidth, narrow = width < 620;
  const pxPerS = Math.max(width - PLOT_L - PLOT_R, 1) / r.participant.duration;
  const defs = rowDefs(r), n = defs.length;
  const stride = Math.max(1, Math.round(DISPLAY_HOP_S / r.hop));
  const plotH = defs.reduce((a, d) => a + ROWS[d.key].h, 0) + ROW_GAP_PX * (n - 1);
  const margin = { l: PLOT_L, r: PLOT_R, t: 24, b: 48 };   // the top margin holds the first row's heading
  const axisId = (k) => (k === 0 ? "y" : `y${k + 1}`);
  const traces = [], shapes = [], annotations = [], layout = {};
  const rowAxis = {}, rowHeight = {}, flawShapes = r.flaws.map(() => []), differenceShapes = differences().map(() => []);
  let top = 0;
  defs.forEach((d, k) => {
    const spec = ROWS[d.key], row = d.row, ax = axisId(k);
    const hi = 1 - top / plotH, lo = 1 - (top + spec.h) / plotH;
    top += spec.h + ROW_GAP_PX;
    rowAxis[d.key] = ax;
    rowHeight[d.key] = spec.h;
    const yaxis = { domain: [lo, hi], fixedrange: true, gridcolor: c.rule, showline: false, zeroline: false, nticks: 4,
      tickfont: { color: c.ink2, size: 10.5 }, automargin: false };
    const unit = UNIT[row.unit] || row.unit;
    let head = narrow ? spec.s : isSelf(r) && spec.own ? spec.own : spec.t;
    if (spec.frame) {
      const times = (a) => a.map((_, i) => i * r.hop).filter((_, i) => i % stride === 0);
      const thin = (a) => a.filter((_, i) => i % stride === 0);
      const x = times(row.p);
      // the dashed reference is drawn over this recording, so it stays visible where the two lines meet
      for (const [name, vals, color, dash, width] of [["This recording", row.p, c.you, "solid", 2], [isSelf(r) ? "Your typical" : "Reference", row.b, c.ref, "dash", 2.4]]) {
        traces.push({ type: "scatter", mode: "lines", name: `${name}, ${spec.s.split(" (")[0].toLowerCase()}`, x, y: thin(vals), yaxis: ax, connectgaps: false,
          line: { color, width, dash }, hovertemplate: `%{y:.1f} ${unit}<extra></extra>` });
      }
    } else if (d.key === "stress") {
      const mid = (i) => (r.words[i].p[0] + r.words[i].p[1]) / 2;
      for (const [name, idx, y, color] of [["Reference stress", r.stress.b, 1, c.ref], ["This recording stress", r.stress.p, 0, c.you]]) {
        traces.push({ type: "scatter", mode: "markers", name, x: idx.map(mid), y: idx.map(() => y), yaxis: ax, customdata: idx.map((i) => r.words[i].w),
          marker: { symbol: "diamond", size: 10, color, line: { color: c.surface, width: 1.5 } }, hovertemplate: "%{customdata}<extra></extra>" });
      }
      Object.assign(yaxis, { range: [-0.8, 1.8], tickvals: [0, 1], ticktext: ["You", "Ref"] });
    } else {
      const vals = row.p, finite = vals.filter((v) => v != null);
      const [below, above] = row.tol || [null, null];   // flag thresholds per direction, null where never flagged
      const m = Math.max(below || 0, above || 0, ...finite.map(Math.abs), 1e-6) * 1.2;
      Object.assign(yaxis, { range: [-m, m], zeroline: true, zerolinecolor: c.muted });
      const name = `${spec.s.split(" (")[0]} vs ${isSelf(r) ? "your typical" : "reference"}`;
      if (spec.markers) {
        const points = eventBars(r.words, vals, false);
        traces.push({ type: "scatter", mode: "markers", name, x: points.x, y: points.y, yaxis: ax, customdata: points.c,
          marker: { size: 8, color: c.you, line: { width: 1, color: c.surface } },
          hovertemplate: `%{y:+.2f} ${unit} (%{customdata})<extra></extra>` });
      } else if (spec.bars) {
        const b = eventBars(r.words, vals, d.key === "pauses");
        traces.push({ type: "bar", name, x: b.x, y: b.y, width: b.w, yaxis: ax, customdata: b.c, marker: { color: c.you },
          hovertemplate: `%{y:+.2f} ${unit} (%{customdata})<extra></extra>` });
      } else {
        const segments = wordSegments(r.words, vals);
        traces.push({ type: "scatter", mode: "lines", name, x: segments.x, y: segments.y, yaxis: ax, customdata: segments.c, connectgaps: false,
          line: { color: c.you, width: 2 }, hovertemplate: `%{y:+.2f} ${unit} (%{customdata})<extra></extra>` });
      }
      if (below != null || above != null) {
        shapes.push({ type: "rect", xref: "x domain", yref: ax, x0: 0, x1: 1, y0: below != null ? -below : -m, y1: above != null ? above : m,
          layer: "below", line: { width: 0 }, fillcolor: rgba(c.tol, 0.14) });
        head += narrow ? ` · flag ${thresholdText(row, true)}` : `. Flagged ${thresholdText(row)}`;
      } else {
        head += row.status === "listed" ? ". Listed, not scored" : row.status === "scored" ? ". Flag threshold unavailable" : ". Shown, not scored";
      }
    }
    layout[ax === "y" ? "yaxis" : `yaxis${k + 1}`] = yaxis;
    // The heading starts at the chart's left edge, over the tick labels, to leave the most width on a phone.
    annotations.push({ xref: "paper", yref: "paper", x: -PLOT_L / Math.max(width - PLOT_L - PLOT_R, 1), y: hi, xanchor: "left", yanchor: "bottom", yshift: 3, showarrow: false,
      text: head, font: { size: 12, color: c.ink2 } });
  });
  const hatch = (key, x0, x1, color, width) => ({ type: "path", xref: "x", yref: `${rowAxis[key]} domain`, layer: "below",
    path: hatchPath(x0, x1, HATCH_STEP_PX / pxPerS, rowHeight[key] / pxPerS), line: { color, width } });
  const labelEnds = {};   // row key -> right edge (px) of the last wash number at the top and at the bottom
  // A wash number goes on the side opposite the departure, else on the free side, else after the earlier number while it
  // still starts on its wash; otherwise it is left out, because the list and the waveform region also carry it.
  const placeNumber = (key, text, delta, x0, x1) => {
    const start = x0 * pxPerS, width = LABEL_CHAR_PX * text.length + 2 * LABEL_PAD_PX;
    const taken = labelEnds[key] || (labelEnds[key] = { top: -Infinity, bottom: -Infinity });
    const preferred = (delta ?? 0) < 0 ? "top" : "bottom", other = preferred === "top" ? "bottom" : "top";
    const free = (s) => taken[s] + LABEL_GAP_PX;
    const side = [preferred, other].find((s) => free(s) <= start) || (taken.top <= taken.bottom ? "top" : "bottom");
    const left = Math.min(Math.max(start, free(side)), r.participant.duration * pxPerS - width);   // inside the plot's right edge
    if (left < free(side) || left > Math.max(x1 * pxPerS, start + LABEL_SHIFT_PX)) return null;
    taken[side] = left + width;
    return { xref: "x", yref: `${rowAxis[key]} domain`, x: left / pxPerS, y: side === "top" ? 1 : 0, xanchor: "left",
      yanchor: side, yshift: side === "top" ? -3 : 1, showarrow: false, text, font: { size: 11, color: c.flagText, weight: 700 }, bgcolor: rgba(c.surface, 0.85), borderpad: 1 };
  };
  r.flaws.forEach((f, i) => {   // flagged regions: a wash in the dimension's row (and the contour row it summarises)
    if (wholePassage(f)) return;   // listed and explained, not painted over the whole chart
    const [a, b] = mediaSpan(f, "you");
    const subword = f.span_kind === "sub-word";
    const widen = !subword && b - a < 0.12;
    const x0 = widen ? (a + b) / 2 - 0.06 : a, x1 = widen ? (a + b) / 2 + 0.06 : b;
    const st = sevStyle(f.severity ?? 0);
    for (const key of [ROW_OF_DIM[f.dimension], ALSO_ROW[f.dimension]]) {
      if (!rowAxis[key]) continue;
      flawShapes[i].push(shapes.length);
      const shape = { type: "rect", xref: "x", yref: `${rowAxis[key]} domain`, x0, x1, y0: 0, y1: 1, layer: "below",
        fillcolor: rgba(c.flag, BAND_ALPHA), line: { color: c.flag, width: 1, dash: st[1] } };
      // The flagged value lies on the side of the departure, so the number goes on the other side. An annotation, not a
      // shape label, because the data bars paint over every shape layer that the number could use.
      if (key === ROW_OF_DIM[f.dimension]) {
        const number = placeNumber(key, `#${i + 1}`, f.delta, x0, x1);
        if (number) annotations.push(number);
      }
      shapes.push(shape);
      if (subword) shapes.push(hatch(key, x0, x1, rgba(c.ink2, 0.55), 1));
    }
  });
  differences().forEach((f, i) => {
    if (wholePassage(f)) return;
    const [a, b] = mediaSpan(f, "you");
    const x1 = f.span_kind === "sub-word" ? b : Math.max(b, a + 0.12);
    for (const key of [ROW_OF_DIM[f.dimension], ALSO_ROW[f.dimension]]) {
      if (!rowAxis[key]) continue;
      differenceShapes[i].push(shapes.length);
      shapes.push({ type: "rect", xref: "x", yref: `${rowAxis[key]} domain`, x0: a, x1, y0: 0, y1: 1,
        layer: "below", fillcolor: rgba(c.neutral, 0), line: { color: c.neutral, width: 0 } });
      if (f.span_kind === "sub-word") { differenceShapes[i].push(shapes.length); shapes.push(hatch(key, a, x1, c.neutral, 0)); }
    }
  });
  // One outline per row that holds members: a box across the rows between them would also enclose unrelated rows.
  const groupShapes = [];
  for (const members of findingGroups(r).filter((m) => m.length > 1)) {
    const byRow = {};
    for (const [f] of members) {
      const key = ROW_OF_DIM[f.dimension];
      if (!rowAxis[key] || wholePassage(f)) continue;
      if (!byRow[key]) byRow[key] = [];
      byRow[key].push(f);
    }
    const keys = defs.map((d) => d.key).filter((key) => byRow[key]);   // top row first
    if (!keys.length) continue;
    const order = members.map(([, j]) => j + 1).sort((x, y) => x - y);
    const run = order.length > 2 && order[order.length - 1] - order[0] === order.length - 1;   // consecutive numbers as a range keep the heading short
    const numbers = run ? `#${order[0]}–#${order[order.length - 1]}` : order.map((j) => `#${j}`).join(", ");
    const indices = keys.map((key, k) => {
      const padX = GROUP_PAD_PX / pxPerS, padY = GROUP_PAD_PX / rowHeight[key];
      const shape = { type: "rect", xref: "x", yref: `${rowAxis[key]} domain`, x0: Math.min(...byRow[key].map((f) => f.p[0])) - padX,
        x1: Math.max(...byRow[key].map((f) => f.p[1])) + padX, y0: -padY, y1: 1 + padY, fillcolor: "rgba(0,0,0,0)",
        line: { color: c.ink2, width: 2, dash: "dashdot" }, layer: "above" };
      // The group is named in the topmost member row's heading: a label on the outline can cover that heading.
      // A phone-width heading has no room for it; the legend, the list and the explain panel name the group there.
      if (k === 0 && !narrow) annotations[defs.findIndex((d) => d.key === key)].text += ` · ${patternText(members[0][0].group_pattern)} group (${numbers})`;
      shapes.push(shape);
      return shapes.length - 1;
    });
    groupShapes.push({ indices, ids: members.map(([f]) => f.id) });
  }
  layout.xaxis = { anchor: axisId(n - 1), range: [0, r.participant.duration], gridcolor: c.rule, showline: false, zeroline: false,
    ticks: "outside", tickcolor: c.rule, tickfont: { color: c.ink2, size: 10.5 }, hoverformat: ".2f",
    title: { text: "Time in this recording (s)", font: { size: 12, color: c.ink2 }, standoff: 6 } };
  Object.assign(layout, { width, height: plotH + margin.t + margin.b, margin, paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)", showlegend: false,
    font: { family: css("--sans"), color: c.ink, size: 12 }, hovermode: "x unified", hoversubplots: "axis", clickanywhere: true,
    dragmode: "zoom", uirevision: S.rid, shapes, annotations, bargap: 0,
    hoverlabel: { bgcolor: c.surface, bordercolor: c.rule, font: { color: c.ink, size: 12 } } });
  // The page redraws on resize (init) because Plotly's own resize keeps stale subplot drag layers and the wide row headings.
  const config = { responsive: false, displaylogo: false, showSendToCloud: false, modeBarButtonsToRemove: ["select2d", "lasso2d", "toImage"],
    doubleClick: "reset" };
  return { traces, layout, config, flawShapes, differenceShapes, groupShapes, colors: c, margin, plotH, width, rows: defs.map((d) => d.key).join() };
}

function drawChart() {
  if (!S.hasLibs || !S.result) return Promise.resolve();
  const before = S.chart;
  S.chart = chartModel(S.result);
  const gd = $("#chart"), rid = S.rid;
  // Plotly.react keeps the x-axis drag strip of a former bottom subplot at its old width, so a new row set or width is drawn afresh.
  const fresh = !before || before.rows !== S.chart.rows || before.width !== S.chart.width;
  return (fresh ? Plotly.newPlot : Plotly.react)(gd, S.chart.traces, S.chart.layout, S.chart.config).then(() => {
    if (fresh) { gd.removeAllListeners("plotly_click"); gd.on("plotly_click", onChartClick); }   // two quick redraws must not bind twice
    if (rid === S.rid) highlight();
  });
}

function highlight() {
  if (!S.chart || !$("#chart").data) return;
  const c = S.chart.colors, updates = {};
  S.result.flaws.forEach((f, i) => {
    const on = S.selKind === "flaw" && (S.sel === i || selected()?.group?.includes(f.id));
    for (const k of S.chart.flawShapes[i]) {
      updates[`shapes[${k}].line.width`] = on ? 2 : 1;
      updates[`shapes[${k}].line.color`] = on ? c.ink : c.flag;
      updates[`shapes[${k}].fillcolor`] = rgba(c.flag, on ? BAND_ALPHA_SEL : BAND_ALPHA);
    }
  });
  S.chart.groupShapes.forEach((g) => {
    const on = S.selKind === "flaw" && g.ids.includes(selected()?.id);
    for (const k of g.indices) {
      updates[`shapes[${k}].line.width`] = on ? 3 : 2;
      updates[`shapes[${k}].line.color`] = on ? c.ink : c.ink2;
    }
  });
  S.chart.differenceShapes.forEach((indices, i) => {
    const on = S.selKind === "difference" && S.sel === i;
    for (const k of indices) {
      updates[`shapes[${k}].line.width`] = on ? (S.chart.layout.shapes[k].type === "path" ? 1 : 2) : 0;
      if (S.chart.layout.shapes[k].type !== "path") updates[`shapes[${k}].fillcolor`] = rgba(c.neutral, on ? 0.18 : 0);
    }
  });
  if (Object.keys(updates).length) Plotly.relayout($("#chart"), updates);
}

function onChartClick(ev) {   // clickanywhere: off-trace clicks carry xvals in axis units
  const x = ev.xvals && ev.xvals.length ? +ev.xvals[0] : ev.points && ev.points[0] ? +ev.points[0].x : NaN;
  if (Number.isNaN(x)) return;
  const hits = [...S.result.flaws.map((f, i) => [f, i, "flaw"]), ...differences().map((f, i) => [f, i, "difference"])]
    .filter(([f]) => { const p = mediaSpan(f, "you"); return x >= p[0] - 0.05 && x <= Math.max(p[1], p[0] + 0.15); });
  if (!hits.length) return;
  const width = (f) => { const p = mediaSpan(f, "you"); return p[1] - p[0]; };
  hits.sort((a, b) => width(a[0]) - width(b[0]));   // the narrowest region under the click
  select(hits[0][1], { scroll: true, kind: hits[0][2] });
}

function moveCursor(tp) {
  const cur = $("#cursor"), gd = $("#chart");
  if (!gd._fullLayout || !gd.layout.xaxis.range) return;
  const [r0, r1] = gd.layout.xaxis.range, size = gd._fullLayout._size;
  const frac = (tp - r0) / (r1 - r0);
  cur.style.display = frac < 0 || frac > 1 ? "none" : "block";
  cur.style.transform = `translateX(${size.l + frac * size.w - 1}px)`;
  cur.style.top = `${size.t}px`;
  cur.style.height = `${size.h}px`;
}

// ---------------------------------------------------------------------------------------------------- audio
/** The audio a Listen button needs: both readings, or this recording only when there is no reference reading. */
function listenAudio() { return isSelf() ? "you" : "both"; }

function updatePlayback() {
  $("#play-all").disabled = !(S.side === "you" ? S.youReady : S.refReady);
  const ready = { you: S.youReady, ref: S.refReady, both: S.youReady && S.refReady };
  document.querySelectorAll("[data-audio]").forEach((b) => { b.disabled = !ready[b.dataset.audio]; });
}

function invalidateMedia() {
  stopAll();
  S.mediaId += 1;
  S.youReady = false; S.refReady = false; S.peekI = null;
  $("#wave .wave-wash")?.replaceChildren();
  setPlaying(false);
  $("#clock").textContent = "Loading audio…";
  $("#cursor").style.display = "none";
  hideTimelineCursor();
  clearKaraoke();
  updatePlayback();
}

function updateWaveRegions() {
  if (!S.youReady || !S.regions) return;
  S.regions.clearRegions();
  const add = (f, i, kind) => {
    const p = mediaSpan(f, "you"), duration = S.ws.getDuration();
    // clear: the recoloured bars and the wash layer show the fault; the region only takes the click and the hover
    const reg = S.regions.addRegion({ start: Math.min(p[0], duration), end: Math.min(Math.max(p[1], p[0] + 0.05), duration), drag: false, resize: false,
      color: "rgba(0, 0, 0, 0)" });
    reg.findingIndex = i; reg.findingKind = kind;
    if (kind === "flaw") { reg.on("over", () => peek(i)); reg.on("leave", () => peek(null)); }
  };
  // the narrowest region last, so it lies on top and stays reachable inside a longer one
  const local = S.result.flaws.map((f, i) => [f, i]).filter(([f]) => !wholePassage(f));   // a whole-passage finding has no region to mark
  local.sort(([a], [b]) => (b.p[1] - b.p[0]) - (a.p[1] - a.p[0])).forEach(([f, i]) => add(f, i, "flaw"));
  if (S.selKind === "difference" && selected() && !wholePassage(selected())) add(selected(), S.sel, "difference");
  paintWave();
}

function mixHex(a, b, share) {
  const channel = (hex, k) => parseInt(hex.slice(1 + 2 * k, 3 + 2 * k), 16);
  return `#${[0, 1, 2].map((k) => Math.round(channel(a, k) + (channel(b, k) - channel(a, k)) * share).toString(16).padStart(2, "0")).join("")}`;
}

/** Bar, heard-bar and wash colours of one fault look (FAULT_LOOK); "diff" is a selected reference difference, in the neutral. */
function lookColors(look) {
  if (look === "diff") {
    const neutral = css("--neutral");
    return { bar: rgba(neutral, 1), played: mixHex(neutral, css("--ink"), 0.45), wash: rgba(neutral, 0.14) };
  }
  const spec = FAULT_LOOK[look], light = css("--flag-text");
  const hex = mixHex(mixHex(css("--you"), css("--flag-bar"), spec.bramble), light, spec.light);
  return { bar: rgba(hex, spec.alpha), played: rgba(mixHex(hex, css("--ink"), 0.4), Math.min(1, spec.alpha + 0.3)), wash: rgba(css("--flag"), spec.wash) };
}

/** The renderer draws whole bars only: its canvas is the wrapper width rounded down to a whole number of bar steps (px). */
function waveGeometry() {
  const step = WAVE_BARS.barWidth + WAVE_BARS.barGap, width = Math.floor(S.ws.getWrapper().clientWidth / step) * step;
  const edge = (k) => Math.min(Math.max(k * step - WAVE_BARS.barGap / 2, 0), width);   // the gap before bar k, so no bar is split
  return { dpr: Math.max(1, devicePixelRatio || 1), width, bars: width / step, edge };
}

/** Fault spans on this recording's waveform as touching pieces [first bar, end bar, look], and the faults at one point in
 *  time (a missing pause: no bars to recolour) as points [x px, look]. A span shorter than two bars is widened to two; where
 *  faults overlap, the strongest look in FAULT_LOOKS order wins. */
function wavePieces(geo) {
  const r = S.result, f = selected(), flaw = S.selKind === "flaw", duration = S.ws.getDuration();
  const busy = (flaw && S.sel != null) || S.peekI != null, best = new Int8Array(Math.ceil(geo.bars)).fill(-1), points = [];
  const mark = (p, look) => {
    const k0 = Math.min(Math.max(Math.round((p[0] / duration) * geo.bars), 0), best.length - 2);
    const k1 = Math.min(Math.max(Math.round((p[1] / duration) * geo.bars), k0 + 2), best.length);
    for (let k = k0; k < k1; k++) best[k] = Math.max(best[k], FAULT_LOOKS.indexOf(look));
    if (atOnePoint(p)) points.push([((p[0] + p[1]) / 2 / duration) * geo.width, look]);
  };
  r.flaws.forEach((x, i) => {
    if (wholePassage(x)) return;
    const look = flaw && S.sel === i ? "sel" : S.peekI === i ? "peek" : flaw && f?.group?.includes(x.id) ? "grp" : busy ? "calm" : severityTier(x);
    mark(x.p, look);
  });
  if (!flaw && f && !wholePassage(f)) mark(mediaSpan(f, "you"), "diff");
  const pieces = [];
  best.forEach((rank, k) => {
    if (rank < 0) return;
    const last = pieces.at(-1);
    if (last && last[1] === k && last[2] === FAULT_LOOKS[rank]) last[1] = k + 1;
    else pieces.push([k, k + 1, FAULT_LOOKS[rank]]);
  });
  return { pieces, points };
}

/** A horizontal gradient with hard stops in the bar gaps: plain bars outside the faults, each piece's colour inside. */
function barGradient(pieces, geo, plain, colorOf) {
  const grad = scratchContext().createLinearGradient(0, 0, geo.width * geo.dpr, 0), at = (k) => geo.edge(k) / geo.width;
  grad.addColorStop(0, plain);
  for (const [k0, k1, look] of pieces) {
    grad.addColorStop(at(k0), plain); grad.addColorStop(at(k0), colorOf(look));
    grad.addColorStop(at(k1), colorOf(look)); grad.addColorStop(at(k1), plain);
  }
  grad.addColorStop(1, plain);
  return grad;
}

/** The faults on this recording's waveform: the bars inside a span take the fault's colour (stronger when selected, a
 *  little lighter when hovered, calmer while another fault is selected or hovered), over a soft wash that fades out toward
 *  the top and the bottom. The voice stays visible: nothing is drawn over the bars. */
function paintWave() {
  cancelAnimationFrame(S.paintFrame);
  if (!S.ws || !S.youReady || !S.result || !S.ws.getWrapper().clientWidth) return;
  const geo = waveGeometry(), { pieces, points } = wavePieces(geo), colors = new Map(FAULT_LOOKS.map((look) => [look, lookColors(look)]));
  const plain = waveColors();
  S.ws.setOptions(pieces.length ? { ...plain, waveColor: barGradient(pieces, geo, plain.waveColor, (look) => colors.get(look).bar),
    progressColor: barGradient(pieces, geo, plain.progressColor, (look) => colors.get(look).played) } : plain);
  let layer = $("#wave .wave-wash");
  if (!layer) { layer = el("div", { class: "wave-wash", "aria-hidden": "true" }); $("#wave").prepend(layer); }
  const runs = [];   // touching pieces share one rounded band whose colour changes along it
  for (const piece of pieces) {
    const run = runs.at(-1);
    if (run && run.at(-1)[1] === piece[0]) run.push(piece); else runs.push([piece]);
  }
  layer.replaceChildren(...runs.map((run) => {
    const x0 = geo.edge(run[0][0]), x1 = geo.edge(run.at(-1)[1]);
    const stops = run.map(([k0, k1, look]) => `${colors.get(look).wash} ${geo.edge(k0) - x0}px ${geo.edge(k1) - x0}px`).join(", ");
    return el("div", { class: "wash-run", style: `left:${x0}px;width:${x1 - x0}px;background-image:linear-gradient(90deg, ${stops})` });
  }), ...points.map(([x, look]) => el("div", { class: "wash-point", style: `left:${x}px;--c:${colors.get(look).bar}` })));
}

/** Hovering repaints the waveform once per frame at most. */
function paintWaveSoon() {
  cancelAnimationFrame(S.paintFrame);
  S.paintFrame = requestAnimationFrame(paintWave);
}

function loadMedia(r, base) {
  invalidateMedia();
  const token = S.mediaId;
  $("#wave-msg").textContent = "";
  showSide("you");
  const ref = S.ref = new Audio();
  const own = !r.baseline?.audio;   // no reference reading: nothing to load or draw in the reference lane
  const refCurrent = () => token === S.mediaId && S.ref === ref;
  ref.addEventListener("canplay", () => { if (refCurrent()) { S.refReady = true; updatePlayback(); } });
  ref.addEventListener("play", () => { if (refCurrent()) setPlaying(true); });
  ref.addEventListener("pause", () => { if (refCurrent()) setPlaying(false); });
  ref.addEventListener("error", () => { if (refCurrent()) { S.refReady = false; updatePlayback(); $("#wave-msg").textContent = "The reference audio could not be loaded."; } });
  ref.preload = "auto";
  if (!own) ref.src = base + r.baseline.audio;
  if (!S.hasLibs) { $("#clock").textContent = "Recording playback unavailable"; return; }
  if (S.ws) S.ws.destroy();
  if (S.wsRef) S.wsRef.destroy();
  S.wsRef = null;
  S.ws = WaveSurfer.create({ container: "#wave", height: WAVE_H, normalize: true, cursorWidth: 2, ...WAVE_BARS, ...waveColors() });
  const ws = S.ws;
  // The reference waveform is drawn only; the reference audio element plays it, and setTime shows its progress.
  if (!own) {
    S.wsRef = WaveSurfer.create({ container: "#wave-ref", height: 44, normalize: true, cursorWidth: 0, ...WAVE_BARS,
      interact: false, ...refWaveColors() });
    S.wsRef.on("error", () => {});
    S.wsRef.load(base + r.baseline.audio).catch(() => {});
  }
  const current = () => token === S.mediaId && S.ws === ws;
  S.regions = ws.registerPlugin(WaveSurfer.Regions.create());
  ws.registerPlugin(WaveSurfer.Timeline.create({ height: 16, style: { color: css("--muted"), fontSize: "11px" } }));
  S.regions.on("region-clicked", (region, e) => { if (current()) { e.stopPropagation(); select(region.findingIndex, { scroll: true, kind: region.findingKind }); } });
  ws.on("ready", () => {
    if (!current()) return;
    S.youReady = ws.getDuration() > 0;
    $("#clock").textContent = S.youReady ? `0.00 / ${ws.getDuration().toFixed(2)} s` : "Audio unavailable";
    updatePlayback(); updateWaveRegions();
  });
  ws.on("timeupdate", (t) => {
    if (!current() || !S.youReady) return;
    $("#clock").textContent = `${t.toFixed(2)} / ${ws.getDuration().toFixed(2)} s`;
    showProgress("you", t / ws.getDuration());
    moveCursor(t); markPlaying(t);
    showReferenceAt(interp(t, S.result.map.p, S.result.map.b));
    moveTimelineCursor(t, interp(t, S.result.map.p, S.result.map.b));
  });
  ws.on("play", () => { if (current()) setPlaying(true); });
  ws.on("pause", () => { if (current()) setPlaying(false); });
  const failed = (e) => {
    if (!current() || e?.name === "AbortError") return;
    S.youReady = false; updatePlayback();
    $("#clock").textContent = "Audio unavailable";
    $("#wave-msg").textContent = "The recording audio could not be loaded.";
  };
  ws.on("error", failed);
  ws.load(base + r.participant.audio).catch(failed);
}

/** This recording in the accent at moderate opacity; heard bars at full accent. paintWave adds the fault colours. */
const waveColors = () => ({ waveColor: rgba(css("--you"), 0.66), progressColor: css("--you-text"), cursorColor: css("--ink") });
const refWaveColors = () => ({ waveColor: rgba(css("--ink2"), 0.22), progressColor: rgba(css("--ink2"), 0.7) });   // the reference stays neutral

/** The analyser of the playing element, made once per element; null where Web Audio is missing or the element is taken. */
function analyserFor(media) {
  if (!media || reducedMotion()) return null;
  if (S.sources.has(media)) return S.sources.get(media);
  let node = null;
  try {
    S.audio = S.audio || new AudioContext();
    const source = S.audio.createMediaElementSource(media);
    node = S.audio.createAnalyser();
    node.fftSize = 256;
    node.smoothingTimeConstant = 0.75;
    source.connect(node);
    node.connect(S.audio.destination);
  } catch {
    node = null;   // no Web Audio, or the element already feeds another graph: no level effect
  }
  S.sources.set(media, node);
  return node;
}

/** While audio plays, its live level drives --level (0 to 1) for the wordmark and the ring glow, and the five meter bars. */
function watchLevel(on) {
  S.levelOn = on;
  if (!on) {
    document.documentElement.style.setProperty("--level", "0");
    document.querySelectorAll(".meter i").forEach((bar) => { bar.style.transform = ""; });
    return;
  }
  const media = !S.ref.paused ? S.ref : S.ws?.getMediaElement?.();
  const node = analyserFor(media);
  if (!node) return;
  S.audio.resume?.();
  const wave = new Uint8Array(node.fftSize), bins = new Uint8Array(node.frequencyBinCount), bars = [...document.querySelectorAll(".meter i")];
  let level = 0;
  const frame = () => {
    if (!S.levelOn) return;
    node.getByteTimeDomainData(wave);
    let sum = 0;
    for (const v of wave) sum += ((v - 128) / 128) ** 2;
    level = 0.8 * level + 0.2 * Math.min(1, Math.sqrt(sum / wave.length) * 6);   // RMS, scaled so speech reaches about 1
    document.documentElement.style.setProperty("--level", level.toFixed(3));
    node.getByteFrequencyData(bins);
    bars.forEach((bar, k) => { bar.style.transform = `scaleY(${(0.15 + 0.85 * bins[2 + k * 6] / 255).toFixed(3)})`; });
    requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);
}

function showReferenceAt(tb) {
  if (S.wsRef && S.wsRef.getDuration() > 0) S.wsRef.setTime(Math.min(tb, S.wsRef.getDuration()));
}

/** The player's progress groove: the share of the playing reading heard so far, in its own colour. */
function showProgress(who, share) {
  const bar = $("#player-progress");
  const clamped = Math.min(Math.max(share, 0), 1);
  bar.classList.toggle("ref", who === "ref");
  bar.firstElementChild.style.width = `${(100 * clamped).toFixed(2)}%`;
  document.documentElement.style.setProperty("--t", clamped.toFixed(4));   // the hero light follows the playback position
}

// ---------------------------------------------------------------------------------------------------- hero panels
const WAVE_H = 72;                 // px, this recording's waveform at rest
const WAVE_MAX_H = 180;            // px, the tallest it grows beside a tall score card
const REF_LANE_H = 70;             // px, about the height of the reference lane; a reading without one may grow by it

/** On a wide screen the score card and the timeline panel sit side by side: the waveform grows until the panel ends
 *  with the card, so no blank stays under the shorter one. */
function fitHeroWave() {
  if (!S.ws) return;
  const panel = $("#hero-wave"), current = S.ws.options.height;
  let target = WAVE_H;
  if (matchMedia("(min-width: 1061px)").matches) {
    const shown = [...panel.children].filter((child) => child.offsetParent);
    const content = Math.max(...shown.map((child) => child.getBoundingClientRect().bottom)) - panel.getBoundingClientRect().top
      + parseFloat(getComputedStyle(panel).paddingBottom);
    const tallest = isSelf() ? WAVE_MAX_H + REF_LANE_H : WAVE_MAX_H;
    target = Math.round(Math.max(WAVE_H, Math.min(tallest, current + $("#ledger").offsetHeight - content)));
  }
  if (Math.abs(target - current) > 1) S.ws.setOptions({ height: target });
}

// ---------------------------------------------------------------------------------------------------- hero horizon
const RIDGE_DB = [-40, 10];        // loudness range (dB re voiced median) mapped from silence to the loudest
const LIGHT_AT = 0.7;              // rest position of the low light, as a share of the width (style.css .glow, --t)
const RANGE_PAD = 24;              // px of range beyond each side of the hero, so no edge shows
// Three mountain ranges, back to front. top, low: summit height as a share of the horizon height for the loudest and the
// quietest summit; spacing: px of width per summit (a narrow screen gets fewer summits); smooth: Gaussian smoothing of
// the contour as a share of the spacing; snow: depth of the snow cap as a share of the summit's relief, on summits
// higher than snowAt (share of the horizon height).
const RANGES = {
  far: { top: 0.9, low: 0.52, spacing: 150, smooth: 0.22, snow: 0.46, snowAt: 0.5 },
  mid: { top: 0.7, low: 0.38, spacing: 196, smooth: 0.24, snow: 0.4, snowAt: 0.44 },
  near: { top: 0.54, low: 0.3, spacing: 270, smooth: 0.26, snow: 0.3, snowAt: 0.36 },
};
const SLOPE_STEPS = [0.18, 0.45, 0.74];   // where a slope bends, as a share of the way from the summit down to the col
const SLOPE_CURVE = 1.35;                // > 1: steep under the summit, flatter towards the col, so the tip is sharp
const MIN_SLOPE = 0.5;                   // px of drop per px of width from a summit: about 27 degrees
const VERTS_PER_SUMMIT = 2 * SLOPE_STEPS.length + 2;   // the summit, its slope vertices on both sides, and one col

/** A loudness contour as `samples` values from 0 to 1: the loudest frame per sample, a Gaussian smoothing over `sigma`
 *  samples (so only features as wide as a mountain stay), then the 10th to the 95th percentile scaled to 0 to 1. */
function loudnessContour(frames, samples, sigma) {
  const per = frames.length / samples;
  const raw = Array.from({ length: samples }, (_, k) => {
    let loudest = RIDGE_DB[0];
    for (let i = Math.floor(k * per); i < Math.min(frames.length, Math.ceil((k + 1) * per)); i++) {
      if (Number.isFinite(frames[i])) loudest = Math.max(loudest, frames[i]);
    }
    return (Math.min(loudest, RIDGE_DB[1]) - RIDGE_DB[0]) / (RIDGE_DB[1] - RIDGE_DB[0]);
  });
  const reach = Math.ceil(3 * sigma);
  const weights = Array.from({ length: 2 * reach + 1 }, (_, j) => Math.exp(-((j - reach) ** 2) / (2 * sigma * sigma)));
  const smooth = raw.map((_, k) => {
    let sum = 0, total = 0;
    weights.forEach((weight, j) => {
      const i = k + j - reach;
      if (i < 0 || i >= samples) return;
      sum += weight * raw[i];
      total += weight;
    });
    return sum / total;
  });
  const sorted = [...smooth].sort((a, b) => a - b);
  const low = sorted[Math.floor(0.1 * (samples - 1))], high = sorted[Math.floor(0.95 * (samples - 1))];
  return smooth.map((v) => Math.min(1, Math.max(0, (v - low) / Math.max(high - low, 1e-6))));
}

/** `count` summit positions (sample indices): the loudest local maxima at least `apart` samples apart. A long even
 *  stretch without a maximum gets its loudest free sample, so a width always has the same number of summits and the
 *  ranges of a new reading morph point by point. */
function pickSummits(contour, count, apart) {
  const n = contour.length;
  const chosen = [];
  const free = (i) => i >= apart / 2 && i <= n - 1 - apart / 2 && chosen.every((j) => Math.abs(i - j) >= apart);
  const maxima = contour.map((_, i) => i).filter((i) => i > 0 && i < n - 1 && contour[i] >= contour[i - 1] && contour[i] > contour[i + 1]);
  for (const i of maxima.sort((a, b) => contour[b] - contour[a])) {
    if (chosen.length === count) break;
    if (free(i)) chosen.push(i);
  }
  while (chosen.length < count) {
    let best = -1;
    for (let i = 0; i < n; i++) if (free(i) && (best < 0 || contour[i] > contour[best])) best = i;
    if (best < 0) break;
    chosen.push(best);
  }
  return chosen.sort((a, b) => a - b);
}

/** Pseudo-random 0 to 1, fixed per (index, salt), so a reading always draws the same rocks. */
function rockNoise(index, salt) {
  const v = Math.sin(index * 12.9898 + salt * 78.233) * 43758.5453;
  return v - Math.floor(v);
}

/** One range as a list of vertices {x, h} (h in px above the horizon floor), left to right: a col, then per summit its
 *  left slope, the summit, its right slope and the next col. The summits sit on the loudest stretches of the contour,
 *  the cols on the quietest stretch between two summits; the slope vertices follow the contour, so a second loud word
 *  near a summit shows as a shoulder. cap(x) is the highest a range may reach at x (it stays under the hero text). */
function rangeVertices(contour, spec, width, height, cap) {
  const n = contour.length;
  const count = Math.max(2, Math.round(width / spec.spacing));
  const xAt = (i) => (i + 0.5) * width / n;
  const indexAt = (x) => Math.min(n - 1, Math.max(0, Math.floor(x / width * n)));
  const summitH = (v) => height * (spec.low + (spec.top - spec.low) * v);
  const summits = pickSummits(contour, count, Math.round(0.62 * n / count)).map((i) => ({ x: xAt(i), h: summitH(contour[i]) }));
  const cols = summits.concat([null]).map((right, k) => {
    const left = summits[k - 1];
    const from = left ? indexAt(left.x) : 0, to = right ? indexAt(right.x) : n - 1;
    let quiet = from;
    for (let i = from; i <= to; i++) if (contour[i] < contour[quiet]) quiet = i;
    const lowest = Math.min(...[left, right].filter(Boolean).map((s) => s.h));
    const h = Math.min(height * spec.low * (0.3 + 0.5 * contour[quiet]), 0.68 * lowest);
    if (!left) return { x: -RANGE_PAD, h };
    if (!right) return { x: width + RANGE_PAD, h };
    const span = right.x - left.x;
    return { x: Math.min(Math.max(xAt(quiet), left.x + 0.32 * span), left.x + 0.68 * span), h };
  });
  const slope = (peak, col, k, side) => SLOPE_STEPS.map((t, j) => {
    const x = peak.x + (col.x - peak.x) * t, relief = peak.h - col.h;
    const shaped = col.h + relief * (1 - t) ** SLOPE_CURVE;
    const measured = Math.min(peak.h - 0.14 * relief, Math.max(col.h, summitH(contour[indexAt(x)])));
    // the contour counts for more further down, so a shoulder forms on the slope and the summit stays a point
    const weight = 0.55 * t;
    const h = (1 - weight) * shaped + weight * measured + 0.08 * relief * (rockNoise(8 * k + j, side) - 0.5);
    // near the summit never flatter than MIN_SLOPE, so no summit turns into a table; lower down a slope may level out
    if (t > 0.5) return { x, h };
    return { x, h: Math.max(col.h + 0.3 * relief * (1 - t), Math.min(h, peak.h - MIN_SLOPE * Math.abs(x - peak.x))) };
  });
  const vertices = [cols[0]];
  summits.forEach((peak, k) => vertices.push(...slope(peak, cols[k], k, 1).reverse(), peak, ...slope(peak, cols[k + 1], k, 2), cols[k + 1]));
  // a summit and its slopes shrink by one factor, taken at the summit, so a slope keeps its angle under the text edge
  const shrink = (x) => Math.min(1, cap(x) / (height * spec.top));
  return vertices.map(({ x, h }, i) => ({ x, h: h * shrink(i % VERTS_PER_SUMMIT ? vertices[i - (i % VERTS_PER_SUMMIT) + SLOPE_STEPS.length + 1].x : x) }));
}

const pathOf = (points, height) => `M${points.map(({ x, h }) => `${x.toFixed(1)} ${(height - h).toFixed(1)}`).join(" L")} Z`;

/** The snow cap of each summit: the top edge follows the range, the lower edge is a snow line with gullies that run
 *  down the slope. A summit under the snow height gets an empty cap, so every cap path keeps the same commands. */
function snowPath(vertices, spec, height) {
  const caps = [];
  for (let at = SLOPE_STEPS.length + 1, k = 0; at < vertices.length; at += VERTS_PER_SUMMIT, k++) {
    const peak = vertices[at];
    const relief = peak.h - Math.max(vertices[at - SLOPE_STEPS.length - 1].h, vertices[at + SLOPE_STEPS.length + 1].h);
    const depth = Math.max(0, relief * spec.snow), line = peak.h - depth;
    const reach = SLOPE_STEPS.length + 1;
    if (peak.h < height * spec.snowAt || depth < 3) {
      caps.push(pathOf(Array(2 * reach + 8).fill(peak), height));
      continue;
    }
    // vertices on one side from the summit outwards while they lie above the snow line and within reach, then the
    // point where the slope leaves either; the reach keeps a long gentle shoulder from turning into a flat snow slab
    const limit = 0.4 * Math.min(Math.abs(vertices[at - reach].x - peak.x), Math.abs(vertices[at + reach].x - peak.x));
    const side = (dir) => {
      const above = [];
      let prev = peak;
      for (let j = 1; j <= reach; j++) {
        const cur = vertices[at + dir * j];
        const byLine = cur.h <= line ? (prev.h - line) / (prev.h - cur.h) : Infinity;
        const byReach = Math.abs(cur.x - peak.x) > limit ? (limit - Math.abs(prev.x - peak.x)) / Math.abs(cur.x - prev.x) : Infinity;
        const t = Math.min(byLine, byReach);
        if (Number.isFinite(t)) return { above, cross: { x: prev.x + (cur.x - prev.x) * t, h: prev.h + (cur.h - prev.h) * t } };
        above.push(cur);
        prev = cur;
      }
      return { above: above.slice(0, -1), cross: prev };
    };
    const left = side(-1), right = side(1);
    const pad = (list, cross) => list.concat(Array(reach - list.length).fill(cross));
    const top = [...pad(left.above, left.cross).reverse(), peak, ...pad(right.above, right.cross)];
    const gullies = [0.16, 0.33, 0.5, 0.67, 0.84].map((f, j) => ({
      x: right.cross.x + (left.cross.x - right.cross.x) * f,
      h: right.cross.h + (left.cross.h - right.cross.h) * f - depth * [0.26, 0.04, 0.6, 0.1, 0.24][j] * (0.6 + 0.8 * rockNoise(k * 5 + j, 3)),
    }));
    caps.push(pathOf([left.cross, ...top, right.cross, ...gullies], height));
  }
  return caps.join(" ");
}

/** The face of each summit turned away from the low light: from the summit down the slope to the col, then back up a
 *  crest line that leans a little into the shade. */
function shadePath(vertices, width, height) {
  const faces = [];
  for (let at = SLOPE_STEPS.length + 1, k = 0; at < vertices.length; at += VERTS_PER_SUMMIT, k++) {
    const peak = vertices[at], dir = peak.x < LIGHT_AT * width ? -1 : 1;
    const slopeDown = Array.from({ length: SLOPE_STEPS.length + 1 }, (_, j) => vertices[at + dir * (j + 1)]);
    const col = slopeDown[slopeDown.length - 1];
    const crest = [1, 0.62, 0.3].map((f, j) => ({ x: peak.x + dir * 0.16 * f * peak.h * (0.7 + 0.6 * rockNoise(k * 3 + j, 5)), h: peak.h * (1 - f) - (f === 1 ? 2 : 0) }));
    faces.push(pathOf([peak, ...slopeDown, { x: col.x, h: -2 }, ...crest], height));
  }
  return faces.join(" ");
}

/** The right end of the widest line of an element's text, in viewport px (the element box can be wider than its text). */
function textRight(el) {
  const range = document.createRange();
  range.selectNodeContents(el);
  return Math.max(...[...range.getClientRects()].map((r) => r.right));
}

/** The hero horizon: three snow-capped ranges drawn from loudness. The near range is this recording; the middle and the
 *  far range are the time-aligned reference (or, with no reference, longer averages of this recording: its typical
 *  delivery). Decorative only. */
function drawHorizon(r) {
  const energy = r.rows?.find((row) => row.key === "energy");
  if (!energy?.p?.length) return;
  S.horizon = { energy, self: isSelf(r) };
  drawRanges();
  drawClouds(energy, isSelf(r));
}

function drawRanges() {
  const { energy, self } = S.horizon;
  const box = $(".horizon"), width = Math.round(box.clientWidth), height = Math.round(box.clientHeight);
  if (!width || !height) return;
  S.horizon.width = width;
  const at = box.getBoundingClientRect();
  const right = Math.max(textRight($("#hero-title")), textRight($("#value-line"))) - at.left;
  const bottom = $("#value-line").getBoundingClientRect().bottom - at.top;
  box.style.setProperty("--text-right", `${Math.round(right)}px`);
  box.style.setProperty("--text-bottom", `${Math.round(bottom)}px`);
  document.body.style.setProperty("--floor", `${Math.round(at.bottom - document.body.getBoundingClientRect().top)}px`);
  // under the text a range stays 14 px below the value line; it rises to full height over 200 px right of the text
  const clear = Math.max(24, height - bottom - 14);
  const cap = (x) => {
    const f = Math.min(1, Math.max(0, (x - right - 16) / 200));
    return clear + f * f * (3 - 2 * f) * Math.max(0, height - clear);
  };
  const samples = Math.max(64, Math.round(width / 4)), pxPerSample = width / samples;
  const source = { near: [energy.p, 1], mid: self ? [energy.p, 1.7] : [energy.b, 1], far: self ? [energy.p, 2.4] : [energy.b, 1.4] };
  for (const [name, spec] of Object.entries(RANGES)) {
    const svg = $(`#range-${name}`);
    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    if (!svg.firstChild) svg.append(...["rock", "snow", "shade"].map((part) => svgEl("path", { class: part })));
    const [frames, longer] = source[name];
    const contour = loudnessContour(frames, samples, (spec.smooth * longer * spec.spacing) / pxPerSample);
    const vertices = rangeVertices(contour, spec, width, height, cap);
    svg.querySelector(".rock").setAttribute("d", `M${-RANGE_PAD} ${height + 2} L${pathOf(vertices, height).slice(1, -2)} L${width + RANGE_PAD} ${height + 2} Z`);
    svg.querySelector(".snow").setAttribute("d", snowPath(vertices, spec, height));
    svg.querySelector(".shade").setAttribute("d", shadePath(vertices, width, height));
  }
}

// ---------------------------------------------------------------------------------------------------- hero clouds
const CLOUD_PAD = 40;           // px of cloud image beyond each side of the hero, so the sway never shows a cut edge
const CLOUD_GAP = 0.1;          // columns quieter than this share of the loud level get no puff: a pause splits the clouds
// Per layer; at phone width the sizes scale by 0.8 and the columns widen by 1.5, so the clouds keep a cloud shape. at: puff
// baseline above the horizon floor, as a share of the horizon height; spacing: px per time column; r: puff radius range
// in px; blur: body and haze blur in px; haze: haze opacity; colours from the lit underside to the top.
const CLOUD_LAYERS = {
  far: { at: 0.6, spacing: 15, r: [4, 26], blur: [4.5, 13], haze: 0.6, lit: "#a07e88", mid: "#635874", top: "#3d3953" },
  near: { at: 0.34, spacing: 12, r: [5, 32], blur: [3.6, 12], haze: 0.55, lit: "#b08a86", mid: "#76657f", top: "#4a425e" },
  glow: { at: 0.34, spacing: 12, r: [5, 32], blur: [4, 12], haze: 0.6, lit: "#f2d4bf", mid: "#d9b6b8", top: "#a893c0" },
};

/** Amplitude per time column from a level contour (dB per 10 ms frame): the RMS of the linear amplitude, a moving mean,
 *  then scaled so the 95th percentile is 1 and one loud word does not flatten the rest. */
function cloudAmplitudes(frames, columns, smoothing) {
  const per = frames.length / columns;
  const rms = Array.from({ length: columns }, (_, k) => {
    let power = 0, count = 0;
    for (let i = Math.floor(k * per); i < Math.min(frames.length, Math.ceil((k + 1) * per)); i++) {
      power += Number.isFinite(frames[i]) ? 10 ** (frames[i] / 10) : 0;
      count += 1;
    }
    return count ? Math.sqrt(power / count) : 0;
  });
  const smooth = rms.map((_, k) => {
    const window = rms.slice(Math.max(0, k - smoothing), k + smoothing + 1);
    return window.reduce((a, v) => a + v, 0) / window.length;
  });
  const loud = [...smooth].sort((a, b) => a - b)[Math.floor(0.95 * (smooth.length - 1))] || 1;
  return smooth.map((v) => Math.min(1.15, v / loud));
}

/** One cloud layer as an SVG document: a puff per time column, sized by the amplitude, lit from below, blurred. */
function cloudSvg(amplitudes, layer, width, height, scale, rangeH) {
  const inner = width - 2 * CLOUD_PAD, spacing = inner / amplitudes.length;
  const base = height - layer.at * rangeH, [rMin, rMax] = layer.r.map((v) => v * scale);
  const jitter = (k, salt) => { const v = Math.sin(k * 12.9898 + salt * 78.233) * 43758.5453; return v - Math.floor(v); };
  // the baseline rises and falls slowly, so the bank is a row of separate clouds, not beads on a line
  const lift = (x) => scale * (7 * Math.sin(x / 173 + 1.3) + 4 * Math.sin(x / 61));
  const puffs = [], rims = [];
  amplitudes.forEach((a, k) => {
    if (a < CLOUD_GAP) return;
    const x = CLOUD_PAD + (k + 0.5) * spacing, y = base - lift(x), r = rMin + (rMax - rMin) * a ** 1.2;
    puffs.push(`<ellipse cx="${x.toFixed(1)}" cy="${(y - 0.3 * r).toFixed(1)}" rx="${(1.45 * r + spacing * 0.4).toFixed(1)}" ry="${(0.8 * r).toFixed(1)}"/>`);
    if (a < 0.45) return;
    // a smaller billow on top, offset by a fixed pseudo-random amount, so the crest is cumulus, not a smooth curve
    const billow = r * (0.5 + 0.3 * jitter(k, 2)), bx = x + (jitter(k, 1) - 0.5) * spacing * 2, by = y - 0.75 * r - 0.3 * billow;
    puffs.push(`<circle cx="${bx.toFixed(1)}" cy="${by.toFixed(1)}" r="${billow.toFixed(1)}"/>`);
    // the billow's underside catches the low light, so the crest reads as lobes in front of one another
    rims.push(`<ellipse cx="${bx.toFixed(1)}" cy="${(by + 0.62 * billow).toFixed(1)}" rx="${(0.85 * billow).toFixed(1)}" ry="${(0.3 * billow).toFixed(1)}"/>`);
  });
  const [body, haze] = layer.blur.map((v) => (v * scale).toFixed(1));
  const top = (base - 2.2 * rMax).toFixed(1), bottom = (base + 0.5 * rMax).toFixed(1);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" preserveAspectRatio="none">`
    + `<defs><linearGradient id="lit" gradientUnits="userSpaceOnUse" x1="0" y1="${bottom}" x2="0" y2="${top}">`
    + `<stop offset="0" stop-color="${layer.lit}"/><stop offset="0.4" stop-color="${layer.mid}"/><stop offset="1" stop-color="${layer.top}"/></linearGradient>`
    + `<linearGradient id="base" gradientUnits="userSpaceOnUse" x1="0" y1="${(base - 0.1 * rMax).toFixed(1)}" x2="0" y2="${bottom}">`
    + `<stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>`
    + `<mask id="fade"><rect width="${width}" height="${height}" fill="url(#base)"/></mask>`
    + `<filter id="soft" x="-2%" y="-40%" width="104%" height="180%" color-interpolation-filters="sRGB">`
    + `<feGaussianBlur stdDeviation="${body}" result="body"/><feGaussianBlur in="SourceGraphic" stdDeviation="${haze}"/>`
    + `<feComponentTransfer result="haze"><feFuncA type="linear" slope="${layer.haze}"/></feComponentTransfer>`
    + `<feMerge><feMergeNode in="haze"/><feMergeNode in="body"/></feMerge></filter></defs>`
    + `<g filter="url(#soft)"><g mask="url(#fade)"><g fill="url(#lit)">${puffs.join("")}</g>`
    + `<g fill="${layer.lit}" opacity="0.32">${rims.join("")}</g></g></g></svg>`;
}

/** The hero clouds are the reading's sound: the near bank is this recording's amplitude, the far bank the time-aligned
 *  reference (or, with no reference, a long average of this recording). Each bank is an image, so its blur is drawn once. */
function drawClouds(energy, self) {
  const box = $(".clouds-near");
  const width = Math.round(box.clientWidth) + 2 * CLOUD_PAD, height = Math.round(box.clientHeight);
  if (!width || !height) return;
  S.clouds = { energy, self, width };
  const narrow = innerWidth < 640, scale = narrow ? 0.8 : 1;
  const columns = (layer) => Math.max(16, Math.round((width - 2 * CLOUD_PAD) / (layer.spacing * (narrow ? 1.5 : 1))));
  const near = cloudAmplitudes(energy.p, columns(CLOUD_LAYERS.near), 0);
  const far = self ? cloudAmplitudes(energy.p, columns(CLOUD_LAYERS.far), 6) : cloudAmplitudes(energy.b, columns(CLOUD_LAYERS.far), 1);
  const show = (id, amplitudes, layer) => {
    const img = $(id);
    if (img.dataset.url) URL.revokeObjectURL(img.dataset.url);
    img.dataset.url = URL.createObjectURL(new Blob([cloudSvg(amplitudes, layer, width, height, scale, $(".horizon").clientHeight)], { type: "image/svg+xml" }));
    img.src = img.dataset.url;
  };
  show("#cloud-far", far, CLOUD_LAYERS.far);
  show("#cloud-near", near, CLOUD_LAYERS.near);
  show("#cloud-lit", near, CLOUD_LAYERS.glow);
}

function setPlaying(on) {
  if (!on && !S.bothTimer) S.listenAt = null;
  markListening();
  watchLevel(on);
  const btn = $("#play-all");
  btn.classList.toggle("playing", on);
  btn.textContent = on ? "Pause" : S.side === "you" ? "Play recording" : "Play reference";
}

/** The main play button plays the chosen reading from its current position, or stops any playback. */
function togglePlay() {
  if (S.ws?.isPlaying() || !S.ref.paused) return stopAll();
  if (S.side === "you") {
    if (S.youReady) playSpan("you", [S.ws.getCurrentTime(), S.ws.getDuration()]);
    return;
  }
  if (!S.refReady) return;
  const at = S.ref.currentTime >= S.ref.duration - 0.05 ? 0 : S.ref.currentTime;
  playSpan("ref", [at, S.ref.duration]);
}

/** The A/B switch: while playing, the other reading continues from the aligned time. */
function setSide(side) {
  if (side === S.side) return;
  const m = S.result?.map, playingYou = !!S.ws?.isPlaying(), playingRef = !S.ref.paused;
  const tp = playingYou ? S.ws.getCurrentTime() : null, tb = playingRef ? S.ref.currentTime : null;
  S.side = side;
  $("#ab-you").setAttribute("aria-pressed", String(side === "you"));
  $("#ab-ref").setAttribute("aria-pressed", String(side === "ref"));
  updatePlayback();
  setPlaying(playingYou || playingRef);
  if (!m || !(playingYou || playingRef)) return;
  if (side === "ref" && playingYou) playSpan("ref", [interp(tp, m.p, m.b), S.ref.duration]);
  if (side === "you" && playingRef) playSpan("you", [interp(tb, m.b, m.p), S.ws.getDuration()]);
}

function stopAll() {
  S.fix.player?.stop();
  S.playId += 1;
  S.listenAt = null;
  clearTimeout(S.refTimer);
  clearTimeout(S.bothTimer);
  S.bothTimer = null;
  S.ref.pause();
  if (S.ws) S.ws.pause();
}

function padSpan([a, b]) {
  const need = MIN_PLAY_S - (b - a);
  return need > 0 ? [Math.max(0, a - need / 2), b + need / 2] : [a, b];
}

/** Select a finding and play it in the player: your span, then the reference span. */
function listen(i, kind = "flaw") {
  if (S.sel !== i || S.selKind !== kind) select(i, { kind });
  const played = isSelf() ? playSpan("you", mediaSpan(selected(), "you")) : playBoth(selected());
  played.then(() => { S.listenAt = `${kind}:${i}`; markListening(); });
}

/** The Listen button of the finding that plays shows playing bars instead of its arrow. */
function markListening() {
  const playing = !!S.ws?.isPlaying() || !S.ref.paused;
  document.querySelectorAll("[data-listen]").forEach((b) => b.classList.toggle("playing", playing && S.listenAt === `flaw:${b.dataset.listen}`));
}

function showSide(who) {
  S.side = who;
  $("#ab-you").setAttribute("aria-pressed", String(who === "you"));
  $("#ab-ref").setAttribute("aria-pressed", String(who === "ref"));
}

async function playSpan(who, s) {
  if (!(who === "you" ? S.youReady : S.refReady)) return;
  stopAll();
  showSide(who);
  const token = S.mediaId, playId = S.playId, ws = S.ws, ref = S.ref, m = S.result.map;
  const current = () => token === S.mediaId && playId === S.playId;
  const [a, end] = padSpan(s), b = Math.min(end, who === "you" ? ws.getDuration() : ref.duration);
  try {
    if (who === "you") { await ws.play(a, b); return; }
    ref.currentTime = a;
    await ref.play();
    if (!current()) { ref.pause(); return; }
    S.refTimer = setTimeout(() => { if (current()) ref.pause(); }, (b - a) * 1000);
    const tick = () => {
      if (current() && !ref.paused) {
        const tp = interp(ref.currentTime, m.b, m.p);
        moveCursor(tp); markPlaying(ref.currentTime, "ref"); moveTimelineCursor(tp, ref.currentTime); showReferenceAt(ref.currentTime);
        $("#clock").textContent = `Reference ${ref.currentTime.toFixed(2)} / ${ref.duration.toFixed(2)} s`;
        showProgress("ref", ref.currentTime / ref.duration);
        requestAnimationFrame(tick);
      }
    };
    tick();
  } catch (e) {
    if (current()) $("#wave-msg").textContent = "The browser blocked playback: press the button again.";
  }
}

/** This recording's span, then the reference's span of the same words. */
async function playBoth(f) {
  await playSpan("you", mediaSpan(f, "you"));
  const playId = S.playId, [a, b] = padSpan(mediaSpan(f, "you"));
  S.bothTimer = setTimeout(() => {
    S.bothTimer = null;
    if (playId !== S.playId) return;
    const at = S.listenAt;
    playSpan("ref", mediaSpan(f, "ref")).then(() => { S.listenAt = at; markListening(); });
  }, (b - a) * 1000 + BOTH_GAP_MS);
}

/** A collapsed section keeps its content laid out (the charts keep their width) at zero height, and inert. */
function setFold(fold, open) {
  fold.classList.toggle("open", open);
  fold.querySelector(".fold-toggle").setAttribute("aria-expanded", String(open));
  fold.querySelector(".fold-body").inert = !open;
}

// ---------------------------------------------------------------------------------------------------- copy per mode
function copyTarget(key) { const [selector, attr] = key.split("@"); return [$(selector), attr]; }
function readCopy(key) { const [node, attr] = copyTarget(key); return attr ? node.getAttribute(attr) : node.textContent; }
function writeCopy(key, text) { const [node, attr] = copyTarget(key); if (attr) node.setAttribute(attr, text); else node.textContent = text; }

/** The page copy that names the reference, in the wording of the result's mode; the reference lane and switch only with a reference. */
function applyCopy(r) {
  const own = isSelf(r);
  if (!S.copy) S.copy = Object.fromEntries(Object.keys(SELF_COPY).map((key) => [key, readCopy(key)]));
  for (const [key, text] of Object.entries(SELF_COPY)) writeCopy(key, own ? text : S.copy[key]);
  $("#wave-ref").hidden = own;
  $(".ab-toggle").hidden = own;
}

// ---------------------------------------------------------------------------------------------------- fix your speech
/** Where a fix of the open result runs (an upload's analysis job or a bundled example), or null where this page cannot fix it. */
function fixSource() {
  const info = S.fix.info, source = S.fix.source;
  if (!info?.available || !source || !S.result?.flaws.length) return null;
  return source.kind === "job" || info.examples.includes(source.id) ? source : null;
}

/** The finding's index in the stored result: render() orders the findings by time. */
const storedIndex = (f) => S.rawIds.indexOf(f.id);
const findingNumber = (id) => S.result.flaws.findIndex((f) => f.id === id) + 1;

function fixButton(f, i, { scroll = false } = {}) {
  if (!fixSource()) return null;
  const button = el("button", { type: "button", class: "fix-btn", "data-fix": f.id, onclick: () => hearFixed(i, scroll) }, HEAR_FIXED[isSelf() ? "self" : "reference"]);
  button.disabled = !!S.fix.busy;
  return button;
}

/** Starts the fix job of key (a finding id or "all") once per result; its entry holds the state, the summary and the player. */
function startFix(key, body) {
  const known = S.fix.jobs.get(key);
  if (known && known.state !== "error") return known;
  const source = fixSource(), rid = S.rid, entry = { state: "running", stage: FIX_STAGES[0], fix: null, audio: null, error: null, player: null };
  if (!source || S.fix.busy) return null;
  S.fix.jobs.set(key, entry);
  S.fix.busy = key;
  const url = source.kind === "job" ? `api/jobs/${source.id}/fix` : `api/gallery/${encodeURIComponent(source.id)}/fix`;
  entry.done = (async () => {
    try {
      const res = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const made = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(failText(res.status, made.detail));
      for (;;) {
        const poll = await fetch(`api/jobs/${made.job_id}`), job = await poll.json().catch(() => ({}));
        if (!poll.ok) throw new Error(failText(poll.status, job.detail));
        if (job.state === "error") throw new Error(job.error);
        if (job.state === "done") { Object.assign(entry, { state: "done", fix: job.fix, audio: job.audio }); break; }
        if (job.stage !== entry.stage) { entry.stage = job.stage; refreshFix(); }
        await new Promise((resolve) => setTimeout(resolve, POLL_MS));
      }
    } catch (e) {
      Object.assign(entry, { state: "error", error: e.message });
    } finally {
      S.fix.busy = null;
      refreshFix();   // also after another result opened: its buttons were disabled while this job ran
    }
    return rid === S.rid && entry.state === "done";
  })();
  refreshFix();
  return entry;
}

/** "Hear it fixed": select the finding, fix it on the server, then loop the fixed region. */
async function hearFixed(i, scroll = false) {
  if (S.sel !== i || S.selKind !== "flaw") select(i, { scroll });
  const f = S.result.flaws[i], entry = startFix(f.id, { finding: storedIndex(f) });
  if (!entry || !(await entry.done) || selected()?.id !== f.id) return;
  entry.player?.play("fixed");
}

const melodyKey = (f) => `${f.id}:contour`;

/** "Try the reference's melody": the same finding fixed again with the reference's pitch contour, then looped. */
async function tryMelody(i) {
  const f = S.result.flaws[i], entry = startFix(melodyKey(f), { finding: storedIndex(f), pitch_method: "contour" });
  if (!entry || !(await entry.done) || selected()?.id !== f.id) return;
  entry.player?.play("fixed");
}

async function fixEverything() {
  const entry = startFix("all", { all: true });
  if (entry && (await entry.done)) entry.player?.play("fixed");
}

/** Redraws what the fix state changes: the buttons, the selected finding's fix and the whole-reading panel. */
function refreshFix() {
  document.querySelectorAll("[data-fix]").forEach((b) => { b.disabled = !!S.fix.busy; });
  const f = selected(), box = document.querySelector("#explain .fixer");
  if (box && f && S.selKind === "flaw" && box.dataset.fixer === f.id) box.replaceWith(fixerView(f));
  renderFixAll();
}

/** Place on the original time axis of a track time, and back; a region track uses the share of its span instead. */
function regionTrack(url, span) {
  const [a, b] = span, w = Math.max(b - a, 1e-3);
  return { url, span, toCommon: (t) => (t - a) / w, fromCommon: (c) => a + c * w };
}

/** Original -> edited time through the edited regions (listen pairs): pieces between regions keep their length. */
function editMap(pairs, originalS, editedS) {
  const xs = [0], ys = [0];
  for (const p of [...pairs].sort((a, b) => a.original[0] - b.original[0])) {
    for (const k of [0, 1]) if (p.original[k] > xs[xs.length - 1] && p.edited[k] > ys[ys.length - 1]) { xs.push(p.original[k]); ys.push(p.edited[k]); }
  }
  xs.push(Math.max(originalS, xs[xs.length - 1])); ys.push(Math.max(editedS, ys[ys.length - 1]));
  return { xs, ys };
}

/**
 * Plays one of several recordings over its span, looped or once; switching keeps the place (the same share of a region,
 * or the same moment of the reading). A start stops every other playback on the page.
 */
class LoopPlayer {
  constructor(tracks, loop, onchange) {
    Object.assign(this, { tracks, loop, onchange, side: "fixed", playing: false, token: 0, media: {} });
  }

  element(side) {
    if (!this.media[side]) this.media[side] = Object.assign(new Audio(this.tracks[side].url), { preload: "auto" });
    return this.media[side];
  }

  async play(side = this.side) {
    const at = this.playing ? this.tracks[this.side].toCommon(this.element(this.side).currentTime) : null;
    stopAll();
    S.fix.player = this;
    this.side = side;
    const token = ++this.token, track = this.tracks[side], media = this.element(side), [a, b] = track.span;
    this.playing = true;
    this.onchange();
    const current = () => token === this.token;
    try {
      if (media.readyState < 1) await new Promise((resolve, reject) => { media.addEventListener("loadedmetadata", resolve, { once: true }); media.addEventListener("error", reject, { once: true }); });
      if (!current()) return;
      media.currentTime = at == null ? a : Math.min(Math.max(track.fromCommon(at), a), b);
      await media.play();
    } catch {
      if (current()) { this.playing = false; this.onchange(); }
      return;
    }
    const tick = () => {
      if (!current()) return;
      // A seek can fail before the audio is seekable (a server without range requests): the region start is set again.
      if (media.currentTime < a - 0.25) media.currentTime = a;
      else if (media.currentTime >= b - 0.02 || media.ended) {
        if (!this.loop) { this.stop(); return; }
        media.currentTime = a;
        if (media.paused) media.play().catch(() => {});
      }
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  stop() {
    this.token += 1;
    Object.values(this.media).forEach((m) => m.pause());
    if (!this.playing) return;
    this.playing = false;
    this.onchange();
  }

  toggle() { if (this.playing) this.stop(); else this.play(); }
}

/** The side switch and the play button of a player; their state follows the player. */
function playerControls(player, sides, note) {
  const buttons = sides.filter(([side]) => player.tracks[side]).map(([side, label]) => el("button", { type: "button", class: "ab-opt", "data-side": side,
    "aria-pressed": "false", onclick: () => player.play(side) }, label));
  const play = el("button", { type: "button", class: "loop-btn", onclick: () => player.toggle() });
  const show = () => {
    buttons.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.side === player.side)));
    play.classList.toggle("playing", player.playing);
    play.textContent = player.playing ? "Stop" : player.loop ? "Play, looping" : "Play";
  };
  player.onchange = show;
  show();
  return el("div", { class: "abc" }, el("div", { class: "ab-toggle", role: "group", "aria-label": "Listen to" }, ...buttons), play,
    note ? el("p", { class: "note", text: note }) : null);
}

/** The heading of one fix (app.fix_entry outcomes). It never says "Fixed" alone: a spot can stop being flagged with only part of the change. */
function outcomeHead(x) {
  if (x.outcome === "no_longer_flagged") return x.share != null && x.share < 1 ? `No longer flagged · ${Math.round(x.share * 100)}% of the change applied` : "No longer flagged";
  if (x.outcome === "still_flagged") return "Still flagged · partly changed";
  if (x.outcome === "unfixable") return `Can't be fixed by editing: ${numbered(x.reason || "")}`;
  return `Not edited · ${numbered(x.reason || "")}`;
}

/** The fix's reason below its heading; the applied share is already in the heading, and an unfixable or skipped reason is the heading. */
function outcomeReason(x) {
  if (!x.reason || x.outcome === "unfixable" || x.outcome === "skipped") return "";
  return numbered(x.reason.replace(/^\d+% of the change toward the target was applied\.\s*/, ""));
}

const playable = (x) => x && (x.outcome === "no_longer_flagged" || x.outcome === "still_flagged");

/** The score before and after when the job states a change; graded on its own, the flagged spots before and after. */
const changeText = (v) => `${v < 0 ? "−" : "+"}${Math.abs(v).toFixed(2)}`;

/** The score change when the job states one (reference mode, reproduced); graded on its own, the flagged spots before and after. */
function scoreLine(done) {
  if (done.score_change != null) return el("p", { class: "fix-score" }, "Score change ", el("b", { text: changeText(done.score_change) }), " points");
  if (done.mode === "self" && done.flags_after != null) return el("p", { class: "fix-score" }, "Spots that stand out ", el("b", { text: String(done.flags_before) }), " → ", el("b", { text: String(done.flags_after) }));
  return done.score_change_note ? el("p", { class: "note", text: done.score_change_note }) : null;
}

/** One fix job of a finding (own pitch or the reference's melody) in plain words, with its three-way player. */
function fixResult(f, entry, key) {
  const parts = [];
  if (entry.state !== "done") return [entry.state === "running" ? progressLine(entry) : el("p", { class: "fix-error", text: entry.error })];
  const done = entry.fix, fx = done.fixes.find((x) => x.finding === f.id) || { outcome: "unfixable", reason: "" };
  parts.push(el("p", { class: "fix-head", text: outcomeHead(fx) }));
  if (outcomeReason(fx)) parts.push(el("p", { class: "fix-reason", text: outcomeReason(fx) }));
  if (playable(fx)) parts.push(scoreLine(done));
  if (done.caution) parts.push(el("p", { class: "fix-caution", text: done.caution }));
  if (playable(fx) && fx.limit) parts.push(el("p", { class: "note", text: fx.limit }));
  parts.push(...fixNotes(done));
  const pair = done.listen.find((p) => p.finding === f.id);
  if (pair && playable(fx)) {
    if (!entry.player) {
      const r = S.result, context = Math.max(pair.original[0] - pair.original_context[0], pair.original_context[1] - pair.original[1]);
      const tracks = { yours: regionTrack(S.base + r.participant.audio, pair.original_context), fixed: regionTrack(entry.audio, pair.edited_context) };
      if (!isSelf(r) && r.baseline.audio && f.b) tracks.target = regionTrack(S.base + r.baseline.audio, [Math.max(0, f.b[0] - context), Math.min(r.baseline.duration, f.b[1] + context)]);
      entry.player = new LoopPlayer(tracks, true, () => {});
    }
    parts.push(playerControls(entry.player, LISTEN_SIDES, "Loops these words with a second before and after."));
  }
  if (fx.alt_pitch_available && key === f.id && !S.fix.jobs.has(melodyKey(f))) {
    const button = el("button", { type: "button", class: "fix-btn", "data-fix": `${f.id}-melody`, onclick: () => tryMelody(S.result.flaws.indexOf(f)) }, "Try the reference's melody");
    button.disabled = !!S.fix.busy;
    parts.push(el("div", { class: "melody" }, button,
      el("p", { class: "note", text: "Changes your intonation pattern on these words to the reference's, instead of widening your own." })));
  }
  return parts.filter(Boolean);
}

/** The fix of one finding, and below it the fix with the reference's melody once asked for. */
function fixerView(f) {
  const entry = fixSource() ? S.fix.jobs.get(f.id) : null;
  if (!entry) return el("div", { class: "fixer", "data-fixer": f.id, hidden: "" });
  const box = el("div", { class: "fixer", "data-fixer": f.id }, ...fixResult(f, entry, f.id));
  const fx = entry.state === "done" ? entry.fix.fixes.find((x) => x.finding === f.id) : null;
  box.classList.add(`is-${fx?.outcome || entry.state}`);
  const melody = S.fix.jobs.get(melodyKey(f));
  if (melody) box.append(el("div", { class: "fixer-melody" }, el("p", { class: "fix-sub", text: "With the reference's melody" }), ...fixResult(f, melody, melodyKey(f))));
  return box;
}

function progressLine(entry) {
  return el("p", { class: "fix-progress", role: "status" }, el("span", { class: "spin", "aria-hidden": "true" }), FIX_STAGE_TEXT[entry.stage] || FIX_STAGE_TEXT.edit);
}

/** Under a fix: spots the edit made stand out, the checks of the re-analysis that passed (quiet), and a caution when one did not. */
function fixNotes(done) {
  const passed = (done.checks || []).filter((c) => c.passed);
  return [done.new_findings ? el("p", { class: "note", text: done.new_findings === 1 ? "The edit made one other spot stand out." : `The edit made ${done.new_findings} other spots stand out.` }) : null,
    passed.length ? el("ul", { class: "fix-checks", "aria-label": "Checks that passed" }, ...passed.map((c) => el("li", { text: c.label }))) : null,
    done.checks_passed ? null : el("p", { class: "note", text: "Listen before you rely on this: one check of the edited recording did not pass." })].filter(Boolean);
}

/** A repair reason names findings by id; the page numbers them. */
const numbered = (text) => text.replace(/\b(d\d-\d{3})\b/g, (id) => `#${findingNumber(id)}`);

function fixAllLine(fix) {
  const n = (k) => fix.fixes.filter((x) => x.outcome === k).length, parts = [];
  const spots = (k) => `${k} ${k === 1 ? "spot" : "spots"}`;
  const partial = fix.fixes.filter((x) => x.outcome === "no_longer_flagged" && x.share != null && x.share < 1).length;
  if (n("no_longer_flagged")) parts.push(`${spots(n("no_longer_flagged"))} no longer flagged${partial ? ` (${partial} with part of the change)` : ""}`);
  if (n("still_flagged")) parts.push(`${n("still_flagged")} still flagged`);
  if (n("unfixable")) parts.push(`${n("unfixable")} can't be fixed by editing`);
  if (n("skipped")) parts.push(`${n("skipped")} not edited`);
  return parts.join(", ") + ".";
}

/** "Fix everything and listen": the button, then the score change (or the flagged spots), the whole reading as yours or edited, and each edit. */
function renderFixAll() {
  const wrap = $("#fix-all"), body = $("#fix-all-body"), r = S.result;
  wrap.hidden = !fixSource();
  if (wrap.hidden) return;
  const entry = S.fix.jobs.get("all");
  $("#fix-all-btn").hidden = entry?.state === "done";
  $("#fix-all-btn").disabled = !!S.fix.busy;
  body.replaceChildren();
  if (!entry) return;
  if (entry.state !== "done") {
    body.append(entry.state === "running" ? progressLine(entry) : el("p", { class: "fix-error", text: entry.error }));
    return;
  }
  const fix = entry.fix;
  if (!entry.player) {
    const map = editMap(fix.listen, r.participant.duration, fix.duration);
    entry.player = new LoopPlayer({ yours: { url: S.base + r.participant.audio, span: [0, r.participant.duration], toCommon: (t) => t, fromCommon: (t) => t },
      fixed: { url: entry.audio, span: [0, fix.duration], toCommon: (t) => interp(t, map.ys, map.xs), fromCommon: (t) => interp(t, map.xs, map.ys) } }, false, () => {});
  }
  const items = r.flaws.map((f, i) => [f, i, fix.fixes.find((x) => x.finding === f.id)]).filter(([, , x]) => x);
  // Each edit of the whole reading as its own loop (yours or fixed, with a second of context), kept across redraws.
  entry.edits = entry.edits || new Map();
  const editControls = (f) => {
    const pair = fix.listen.find((p) => p.finding === f.id);
    if (!pair) return null;
    if (!entry.edits.has(f.id)) entry.edits.set(f.id, new LoopPlayer({ yours: regionTrack(S.base + r.participant.audio, pair.original_context),
      fixed: regionTrack(entry.audio, pair.edited_context) }, true, () => {}));
    return playerControls(entry.edits.get(f.id), LISTEN_SIDES.slice(0, 2), null);
  };
  const spots = fix.score_change == null && fix.mode === "self" && fix.flags_after != null;
  body.append(...[
    fix.score_change != null ? el("p", { class: "fix-all-score", "aria-label": `Score ${num(fix.score_before, 2)} before the edits, ${num(fix.score_after, 2)} after` },
      el("span", { class: "from", text: num(fix.score_before, 2) }), el("span", { class: "arrow", text: "→" }), el("span", { class: "to", text: num(fix.score_after, 2) }),
      el("span", { class: "unit", text: `${changeText(fix.score_change)} points` }))
    : spots ? el("p", { class: "fix-all-score", "aria-label": `${fix.flags_before} spots stood out before the edits, ${fix.flags_after} after` },
      el("span", { class: "from", text: String(fix.flags_before) }), el("span", { class: "arrow", text: "→" }), el("span", { class: "to", text: String(fix.flags_after) }),
      el("span", { class: "unit", text: fix.flags_after === 1 ? "spot stands out" : "spots stand out" }))
    : fix.score_change_note ? el("p", { class: "note", text: fix.score_change_note }) : null,
    el("p", { class: "note", text: `Your whole reading with every fix applied. ${fixAllLine(fix)}` }),
    fix.caution ? el("p", { class: "fix-caution", text: fix.caution }) : null,
    playerControls(entry.player, LISTEN_SIDES.slice(0, 2), null),
    ...fixNotes(fix),
    el("details", { class: "fix-list" }, el("summary", { text: "What each fix did" }),
      el("ul", {}, ...items.map(([f, i, x]) => el("li", { class: `is-${x.outcome}` },
        el("button", { type: "button", class: "plain", onclick: () => select(i, { scroll: true }), text: `#${i + 1} ${findingText(f)}` }),
        el("span", { text: [outcomeHead(x), outcomeReason(x)].filter(Boolean).join(". ") }),
        playable(x) ? editControls(f) : null))))].filter(Boolean));
}

// ---------------------------------------------------------------------------------------------------- render
/**
 * [index, kind, focused] of the item a page opens on: the gallery item's `focus` id, else the costliest finding, else
 * the first difference. focused is true only for the `focus` id.
 */
function initialSelection(r, focus) {
  const flaw = r.flaws.findIndex((f) => f.id === focus), difference = differences().findIndex((d) => d.id === focus);
  if (flaw >= 0) return [flaw, "flaw", true];
  if (difference >= 0) return [difference, "difference", true];
  if (S.priority != null) return [S.priority, "flaw", false];
  return [differences().length ? 0 : null, "difference", false];
}

/** source: where a fix of this result runs ({kind: "gallery" | "job", id}). */
function render(r, base, focus = null, source = null) {
  stopAll();
  S.rawIds = r.flaws.map((f) => f.id);   // a fix request names a finding by its index in the stored result
  // Temporal numbers are stable even when the highest-impact whole-passage finding leads the list.
  r = { ...r, flaws: [...r.flaws].sort((a, b) => (a.p?.[0] ?? 0) - (b.p?.[0] ?? 0)) };
  S.base = base;
  S.fix.source = source;
  S.fix.jobs = new Map();
  S.fix.player = null;
  S.result = r; S.sel = null; S.selKind = "flaw"; S.filter = null; S.chart = null; S.rid += 1;
  S.allDimensions = false;
  S.pattern = null;
  S.priority = r.flaws.length ? r.flaws.reduce((best, f, i) => (f.points_lost ?? 0) > (r.flaws[best].points_lost ?? 0) ? i : best, 0) : null;
  $("#all-dimensions").setAttribute("aria-pressed", "false");
  $("#all-dimensions").textContent = "Show all dimensions";
  $("#clear-filter").hidden = true;
  $("#key-group").hidden = !r.flaws.some((f) => f.group);
  $("#key-subword").hidden = ![...r.flaws, ...differences()].some((f) => f.span_kind === "sub-word");
  $("#listed-wrap").open = false;   // one panel element and one list column serve every example
  for (const box of [$(".side"), $("#flaws"), $("#differences"), $("#listed")]) box.scrollTop = 0;
  renderLedger(r);
  drawHorizon(r);
  renderFixAll();
  renderFilters(r);
  renderFlawList();
  renderDifferenceList();
  renderClipCards();
  renderTranscript(r);
  drawTimeline();
  loadMedia(r, base);
  const [first, kind, focused] = initialSelection(r, focus);
  // A gallery item opens on the item it shows, so that item must show in the list column; a list heading stays above it.
  select(first, { kind, reveal: false });
  drawChart();
  if (focused) {
    const btn = document.querySelector(`.side button[data-i="${first}"][data-kind="${kind}"][aria-pressed="true"]`);
    revealInSide(btn, btn?.closest("#listed-wrap")?.querySelector("summary") || btn?.closest(".side")?.querySelector(".side-head"));
  }
}

// ---------------------------------------------------------------------------------------------------- gallery
async function getJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url}: HTTP ${res.status}`);
  return res.json();
}

/** Generated cover art for an example: a mini waveform on a flat tile, seeded by the example id. */
function coverArt(id) {
  let seed = 0;
  for (const ch of id) seed = (seed * 31 + ch.charCodeAt(0)) >>> 0;
  const random = () => { seed = (seed * 1103515245 + 12345) >>> 0; return seed / 2 ** 32; };
  const bars = Array.from({ length: 9 }, (_, k) => {
    const h = 6 + random() * 24;
    return svgEl("rect", { x: 5 + k * 4, y: 22 - h / 2, width: 2.2, height: h, rx: 1.1, fill: css("--you-text") });
  });
  return svgEl("svg", { viewBox: "0 0 44 44" }, svgEl("rect", { width: 44, height: 44, fill: css("--panel") }), ...bars);
}

/** The example with a reference whose reading a no-reference example grades on its own (gallery index `reference_version`). */
const referenceTwin = (it, items) => it.reference_version ? items.find((x) => x.id === it.reference_version) : undefined;

function buildChips(index) {
  const twinOf = new Map(index.items.map((it) => [it, referenceTwin(it, index.items)]).filter(([, twin]) => twin));
  twinOf.forEach((_, it) => TWINS.add(it.id));
  // graded on its own, an example shows its flagged spots, as its page does
  const chipScore = (it) => it.regime !== "SELF" || it.n_flaws == null ? scoreText(it.overall) : `${it.n_flaws} ${it.n_flaws === 1 ? "spot" : "spots"}`;
  const chip = (it) => el("button", { type: "button", class: "chip", "aria-pressed": "false", "data-id": it.id, title: it.title, onclick: () => openExample(it) },
    el("span", { class: "art", "aria-hidden": "true" }, coverArt(it.id)), el("span", { class: "name", text: exampleName(it) }),
    el("span", { class: "score", text: chipScore(it) }));
  // each no-reference twin follows the example it reads
  const withTwins = (list) => list.flatMap((it) => [it, ...[...twinOf].filter(([, twin]) => twin === it).map(([own]) => own)]);
  const ranked = withTwins(EXAMPLES.map(([id]) => index.items.find((it) => it.id === id)).filter(Boolean));
  const featured = ranked.slice(0, FEATURED_COUNT);
  const rest = [...ranked.slice(FEATURED_COUNT), ...withTwins(index.items.filter((it) => !ranked.includes(it) && !twinOf.has(it)))];
  $("#chips").replaceChildren(...(featured.length ? featured : rest).map(chip));
  $("#chips-more").replaceChildren(...(featured.length ? rest : []).map(chip));
  $("#more-examples").hidden = !featured.length || !rest.length;
}

/** The hero's title names the open example. */
function showPicked(name) {
  $("#picker-current").textContent = name;
}

/** Fades the page content out and in around a content change; reduced motion swaps at once. */
async function crossFade(change) {
  const main = document.querySelector("main");
  if (reducedMotion() || !S.result) { change(); return; }
  main.classList.add("fading");
  await new Promise((resolve) => setTimeout(resolve, 140));
  S.tickOn = true;
  change();
  requestAnimationFrame(() => main.classList.remove("fading"));
}

async function openExample(it) {
  $("#picker-menu").open = false;
  const request = ++S.openId;
  invalidateMedia();
  try {
    const r = await getJSON("gallery/" + it.result);
    if (request !== S.openId) return;
    document.querySelectorAll(".chip").forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.id === it.id)));
    showPicked(exampleName(it));
    showAlert("");
    await crossFade(() => render(r, "gallery/", it.focus, { kind: "gallery", id: it.id }));
  } catch (e) {
    if (request === S.openId) { $("#clock").textContent = "Audio unavailable"; showAlert(`The example could not be loaded: ${e.message}`); }
  }
}

// Reference modes in plain words; the same text as gallery.MODE_TEXT (tests/test_app.py compares them).
const MODE_TEXT = { single: "one reference", consensus5: "median of five references" };

// ---------------------------------------------------------------------------------------------------- upload
function disableUpload(reason) {
  $("#fields").disabled = true;
  $("#upload-note").textContent = reason;
}

/** Picker label and mode sentence of a bundled baseline: one reading, or a bank compared through the median of its readings. */
function baselineText(b) {
  const refs = b.references || [];
  if (!refs.length) return { label: `${b.title}: bundled, one reading`, note: "Compared with one reference reading." };
  const k = b.consensus_k || 5;
  return { label: `${b.title}: bundled bank of ${refs.length} readings`,
    note: refs.length >= k ? `Compared with ${k} readings of this text by different people (LibriVox, public domain); you hear and see the first, by ${refs[0].reader}. Readers: ${refs.slice(0, k).map((r) => r.reader).join(", ")}.`
      : `Compared with the first of ${refs.length} readings, by ${refs[0].reader}: five are needed to combine them.` };
}

const NO_REFERENCE = "none";   // the picker value of an upload without a reference reading
const NO_REFERENCE_NOTE = "Without a reference, your reading is graded against itself: each stretch is compared with how you read the rest. This is a rough check; for better results, use a reference reading of the same text.";
const OWN_REFERENCE_NOTE = "Add up to five readings of the same text by different people. With five, the comparison catches far more timing problems.";

/** The note under the reference field when the user uploads their own references: the advice, then what the chosen files give. */
function ownReferenceNote(files) {
  const n = files.length;
  if (n > 5) return "Choose at most five reference recordings.";
  if (n === 5) return `All five readings are combined; you hear and see the first, ${files[0].name}.`;
  if (n > 1) return `${OWN_REFERENCE_NOTE} With ${n}, only the first, ${files[0].name}, is used: five are needed to combine them.`;
  return OWN_REFERENCE_NOTE;
}

async function setupUpload(index) {
  const sel = $("#f-baseline");
  const bundled = index.baselines || [index.baseline];
  sel.replaceChildren(...bundled.map((b) => el("option", { value: b.id, text: baselineText(b).label })),
    el("option", { value: "", text: "Upload my own reference recordings" }), el("option", { value: NO_REFERENCE, text: "No reference: grade my reading on its own" }));
  const prefill = () => {
    const own = sel.value === "", none = sel.value === NO_REFERENCE, b = bundled.find((x) => x.id === sel.value);
    $("#own-baseline").hidden = !own;
    $("#baseline-note").textContent = none ? NO_REFERENCE_NOTE : own ? ownReferenceNote($("#f-baseline-audio").files) : baselineText(b).note;
    $("#text-label").textContent = none ? "Transcript: the exact words you read" : "Transcript: the exact words both recordings read";
    $("#compare-note").textContent = none ? "Your recording is graded against itself." : "Your recording is compared as a different speaker from the reference reading.";
    if (b && !$("#f-text").dataset.edited) $("#f-text").value = b.text || "";
  };
  sel.addEventListener("change", prefill);
  $("#f-baseline-audio").addEventListener("change", prefill);
  $("#f-text").addEventListener("input", () => { $("#f-text").dataset.edited = "1"; });
  $("#f-text-file").addEventListener("change", async (e) => {
    const f = e.target.files[0];
    if (f) { $("#f-text").value = await f.text(); $("#f-text").dataset.edited = "1"; }
  });
  prefill();
  $("#form").addEventListener("submit", submitUpload);
  let health;
  try {
    const res = await fetch("api/health");
    if (!res.ok) throw new Error(String(res.status));
    health = await res.json();
  } catch {
    return disableUpload("Uploads need the local server. Run `python -m cvoice.app` and open http://127.0.0.1:7860 (see the README); this static copy only shows the bundled examples.");
  }
  S.limits = health.limits;
  S.flagLimits = health.flag_limits || {};
  S.fix.info = health.fix || null;
  sel.querySelector(`option[value="${NO_REFERENCE}"]`).disabled = health.self?.available === false;
  if (S.result) { renderSummary(S.result); renderFixAll(); if (selected()) renderExplain(); }   // an example opened before the server answered gains its fix buttons
  if (S.result) renderLimit(S.result);   // an example that loaded before the server answered gains its five-reading line
  const mb = (bytes) => Math.round(bytes / 2 ** 20);
  $("#limits").textContent = `${mb(health.limits.max_bytes)} MB per file` + (health.limits.max_total_bytes ? `, ${mb(health.limits.max_total_bytes)} MB in all` : "")
    + `, ${health.limits.max_seconds} s of audio per recording`;
  if (!health.analysis.available) disableUpload(health.analysis.reason);
}

function showStages(stages, now, failed) {
  const ol = $("#stages");
  ol.hidden = false;
  const at = stages.indexOf(now);
  ol.replaceChildren(...stages.map((s, i) => el("li", { class: i < at || now === "done" ? "done" : i === at && !failed ? "now" : "", text: s })));
}

function failText(status, detail) {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return "The form is incomplete: choose your recording and enter the transcript.";
  return `The request failed (HTTP ${status}).`;
}

async function submitUpload(ev) {
  ev.preventDefault();
  const msg = $("#stage-msg");
  msg.className = "note"; msg.textContent = "";
  const audio = $("#f-audio").files[0], own = $("#f-baseline").value === "", none = $("#f-baseline").value === NO_REFERENCE;
  const ownFiles = own ? [...$("#f-baseline-audio").files] : [];
  if (!audio) return fail("Choose your recording.");
  if (own && !ownFiles.length) return fail("Choose your reference recordings, or pick a bundled one.");
  if (ownFiles.length > (S.limits?.max_references || 5)) return fail("Choose at most five reference recordings.");
  if (!$("#f-text").value.trim()) return fail(none ? "Enter the transcript: the exact words you read." : "Enter the transcript: the exact words both recordings read.");
  const files = [audio, ...ownFiles];
  if (S.limits && files.some((f) => f.size > S.limits.max_bytes)) return fail(`A file is larger than ${Math.round(S.limits.max_bytes / 2 ** 20)} MB.`);
  if (S.limits?.max_total_bytes && files.reduce((sum, f) => sum + f.size, 0) > S.limits.max_total_bytes) return fail(`The files together are larger than ${Math.round(S.limits.max_total_bytes / 2 ** 20)} MB.`);
  const fd = new FormData();
  fd.append("audio", audio);
  fd.append("transcript", $("#f-text").value);
  if (own) for (const f of ownFiles) fd.append("baseline_audio", f);
  else if (!none) fd.append("baseline_id", $("#f-baseline").value);
  $("#submit").disabled = true;
  document.body.classList.add("busy");
  showStages(["decode", "align", "features", "compare", "detect"], "decode");
  try {
    const res = await fetch("api/analyze", { method: "POST", body: fd });
    const body = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(failText(res.status, body.detail));
    await poll(body.job_id);
  } catch (e) {
    fail(e.message);
  } finally {
    $("#submit").disabled = false;
    document.body.classList.remove("busy");
  }
}

function fail(text) {
  const msg = $("#stage-msg");
  msg.className = "err"; msg.textContent = text;
}

async function poll(id) {
  for (;;) {
    const res = await fetch(`api/jobs/${id}`);
    const job = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(failText(res.status, job.detail));
    showStages(job.stages, job.stage, job.state === "error");
    if (job.state === "error") throw new Error(job.error);
    if (job.state === "done") {
      const r = await getJSON(job.result);
      S.openId += 1;
      document.querySelectorAll(".chip").forEach((c) => c.setAttribute("aria-pressed", "false"));
      showPicked("Your analysis");
      render(r, "", null, { kind: "job", id });
      $("#ledger").scrollIntoView({ block: "start" });
      return;
    }
    await new Promise((resolve) => setTimeout(resolve, POLL_MS));
  }
}

// ---------------------------------------------------------------------------------------------------- start
async function init() {
  $("#jump-upload").addEventListener("click", () => { $("#upload").open = true; });
  for (const fold of document.querySelectorAll(".fold")) fold.querySelector(".fold-toggle").addEventListener("click", () => setFold(fold, !fold.classList.contains("open")));
  const openAllFindings = () => { setFold($("#all-findings"), true); $("#all-findings").scrollIntoView({ block: "start" }); };
  $("#see-all").addEventListener("click", openAllFindings);
  $("#tl-more").addEventListener("click", openAllFindings);
  const menu = $("#picker-menu");
  document.addEventListener("click", (e) => { if (menu.open && !menu.contains(e.target)) menu.open = false; });
  menu.addEventListener("keydown", (e) => { if (e.key === "Escape" && menu.open) { menu.open = false; menu.querySelector("summary").focus(); } });
  $("#clear-filter").addEventListener("click", () => { S.pattern = null; $("#pattern-filter").value = ""; setFilter(null); });
  $("#dimension-filter").addEventListener("change", (e) => setFilter(e.target.value ? e.target.value.split(",") : null));
  $("#pattern-filter").addEventListener("change", (e) => setPattern(e.target.value || null));
  $("#play-all").addEventListener("click", togglePlay);
  linkPeek();
  $("#ab-you").addEventListener("click", () => setSide("you"));
  $("#ab-ref").addEventListener("click", () => setSide("ref"));
  $("#fix-all-btn").addEventListener("click", fixEverything);
  setTimeout(() => document.body.classList.remove("intro"), INTRO_MS);
  if (reducedMotion()) document.body.classList.remove("intro");
  // The page keeps room for the fixed player bar, whose height changes when it wraps at phone width.
  const player = $(".player");   // the whole sticky strip, padding included, so a heading scrolled to lands below it
  new ResizeObserver(() => document.documentElement.style.setProperty("--player-h", `${player.offsetHeight}px`)).observe(player);
  let fitFrame = 0;
  const heroFit = new ResizeObserver(() => { cancelAnimationFrame(fitFrame); fitFrame = requestAnimationFrame(fitHeroWave); });
  for (const box of [$("#ledger"), $(".tl-stage"), $("#hero-wave")]) heroFit.observe(box);
  $("#all-dimensions").addEventListener("click", () => {
    S.allDimensions = !S.allDimensions;
    $("#all-dimensions").setAttribute("aria-pressed", String(S.allDimensions));
    $("#all-dimensions").textContent = S.allDimensions ? "Show relevant dimensions" : "Show all dimensions";
    drawChart();
  });
  let resizeTimer = 0;
  addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      if (S.tl && $("#tl-host").clientWidth !== S.tl.width) drawTimeline();
      if (S.chart && $("#chart-host").clientWidth !== S.chart.width) drawChart();
      if (S.horizon && $(".horizon").clientWidth !== S.horizon.width) drawRanges();
      if (S.clouds && $(".clouds-near").clientWidth + 2 * CLOUD_PAD !== S.clouds.width) drawClouds(S.clouds.energy, S.clouds.self);
    }, 150);
  });
  document.fonts?.ready.then(() => {
    if (S.result) drawTimeline();
    if (S.horizon) drawRanges();   // the serif changes where the hero text ends, which bounds the ranges under it
  });
  await ensureLibs();
  S.hasLibs = typeof Plotly !== "undefined" && typeof WaveSurfer === "function" && !!WaveSurfer.Regions && !!WaveSurfer.Timeline;
  if (!S.hasLibs) showAlert("The chart and audio libraries could not be loaded, so the chart and the waveform are unavailable. Scores, flagged regions and the transcript still work.");
  let index;
  try {
    index = await getJSON("gallery/index.json");
  } catch (e) {
    return showAlert(`The bundled examples could not be loaded (${e.message}).`);
  }
  buildChips(index);
  setupUpload(index);
  await openExample(index.items.find((i) => i.id === index.default) || index.items[0]);
}

init();
