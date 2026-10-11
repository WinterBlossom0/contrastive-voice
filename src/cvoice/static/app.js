"use strict";
/* Contrastive Voice dashboard. One render path: render(result, base) draws a gallery result and an upload result alike.
   Text from results is user data: it is only ever inserted with textContent. */

// ---------------------------------------------------------------------------------------------------- constants
const PLOT_L = 64, PLOT_R = 16;          // px; insets of the chart's plot; the hero timeline also keeps PLOT_R free on its right
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
const TL_HIT_PAD_PX = 4;                 // px a word's click target reaches above and below its bar
const TL_WORD_MIN_PX = 8;                // px; the least width of a word's click target where no neighbour limits it
const TL_MIN_SPAN_PX = 4;                // px; a shorter span (a pause point) is widened to stay visible and clickable
const TL_MARK_H = 20, TL_MARK_GAP = 4;   // px; height of a strip label and the gap kept around it
const TL_MARK_FONT = 12.5;               // px; must equal .strip-label text in style.css
const TL_MARK_ROWS = 2;                  // label rows under the strip; a label that fits in none is counted under the panel
const TL_MARK_REACH_PX = 48;            // px a full label may move sideways off its region; a number alone may move three times as far
const TL_JOIN_S = 0.5;                   // s; members of one finding group closer than this share one label
const STRIP_HIT_PX = 10;                 // px; a narrower span (a pause point) gets a hit area this wide
const STRIP_FREE_PX = 6;                 // px; a span with no free stretch this wide beside the spans over it is covered
const GAUGE_LABEL = "Flag threshold", GAUGE_LABEL_PX = 13;   // px; must equal .gauge-labels text in style.css
// Strip heat of each severity tier (0 calm to 1); a finding glows at least this much, and the costliest local finding at 1.
const TIER_HEAT = { dot: 0.35, dash: 0.55, solid: 0.75 };
const WAVE_BARS = { barWidth: 2, barGap: 1, barRadius: 2 };   // px
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
const OWN_EVIDENCE = { D9: "word_time_ln" };   // the evidence row that holds the finding's own measured difference
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
const BAND_STEPS = 7;                    // intro: at most this many strip steps (style.css .intro .strip-span: 1 s, then 0.16 s each)
const FIX_COUNT_WORDS = ["", "Your biggest fix", "Your two biggest fixes", "Your three biggest fixes"];
const SPOT_COUNT_WORDS = ["", "The spot that stands out most", "The two spots that stand out most", "The three spots that stand out most"];
const reducedMotion = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
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
  "#all-findings-word": "Every spot",
};
const SELF_LIMIT = "A rough check: your reading is graded against itself. For better results, use a reference reading of the same text.";
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
// Type of a local departure by its dimension and the sign of its difference: the same table as explain.FLAW_TYPE.
const FLAW_TYPE = { D1: ["RUSH", "DRAG"], D2: ["PAUSE_DROPPED", "PAUSE_INTRUSIVE"], D3: ["MONOTONE", null], D4: ["DEEMPHASIS", null],
  D5: ["FADE", null], D6: ["MUMBLE", null], D7: [null, "WORD_TIME"], D8: [null, "ENDING_HIGH"], D9: ["NATURAL_RUSH", null] };
/** The type that names what was measured. A group member's stored type is the group's recipe (a pause in a DRAG group is
 *  stored as DRAG), so a local finding takes the type of its own dimension and direction. The pause rule (patterns.rush_type)
 *  chooses RUSH or NATURAL_RUSH for a faster speech tempo, so both stay. */
function ownType(f) {
  if (wholePassage(f) || f.delta == null || !f.delta) return f.type;
  if (f.dimension === "D9" && (f.type === "RUSH" || f.type === "NATURAL_RUSH")) return f.type;
  return FLAW_TYPE[f.dimension]?.[f.delta < 0 ? 0 : 1] || f.type;
}
// Beside a whole-clip tempo finding a local pace flag is relative to the speaker's own overall tempo, not a second tempo verdict.
function typeText(f) {
  const type = ownType(f);
  const local = f.dimension === "D1" && (type === "RUSH" || type === "DRAG") && S.result.flaws.some((x) => x.type?.startsWith("TEMPO"));
  if (local) return type === "RUSH" ? "Faster than the rest of your reading" : "Slower than the rest of your reading";
  return TYPE_TEXT[type] || type;
}
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
const groupPart = (f) => `Part of the ${patternText(f.group_pattern)} group`;
// The pattern and the group have their own chips (patternTags), so the title names the measured departure.
const findingText = (f) => f.type ? typeText(f) : f.label || f.brief_word || f.dimension;
const findingName = (f, i) => `#${i + 1} ${findingText(f)}`;
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
function textWidth(text, px, weight = 400) {
  if (!measureContext) measureContext = document.createElement("canvas").getContext("2d");
  measureContext.font = `${weight} ${px}px ${css("--sans")}`;
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
const S = { fix: { info: null, source: null, jobs: new Map(), cache: new Map(), busy: null, player: null }, copy: null, result: null, sel: null, filter: null, rid: 0, limits: null, flagLimits: null, ws: null, ref: new Audio(),
  refTimer: null, bothTimer: null, tl: null, chart: null, hasLibs: false, selKind: "flaw", allDimensions: false, openId: 0,
  mediaId: 0, youReady: false, refReady: false, inSpan: new Set(), listenAt: null, audio: null, sources: new WeakMap(), levelId: 0, countId: 0, counted: false, side: "you", wsRef: null, playId: 0, priority: null, pattern: null };

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
  if (S.counted || o == null || reducedMotion()) { S.counted = true; fig.textContent = scoreText(o); return; }
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
  $("#fixes-title").textContent = (isSelf(r) ? SPOT_COUNT_WORDS : FIX_COUNT_WORDS)[top.length] || "Your biggest fixes";
  $(".fixes").hidden = !top.length;
  $("#top-cards").replaceChildren(...top.map(([f, i], rank) => el("article", { class: rank ? "top-card" : "top-card lead", "data-finding": f.id, "data-i": i, "data-peek": i },
    el("button", { type: "button", class: "card-open", "data-i": i, "data-kind": "flaw", "aria-pressed": "false", onclick: () => select(i, { scroll: true }) },
      el("span", { class: "rank", text: `${rank + 1}` }), el("span", { class: "card-title" }, dimIcon(f.dimension), findingText(f)),
      el("span", { class: "card-pts", text: findingPts(f) })),
    el("p", { class: "card-words", text: quotedWords(r, f) }),
    el("p", { class: "card-line", text: plainLine(f) }),
    f.group_pattern && !f.pattern ? el("p", { class: "card-group", text: groupPart(f) }) : null,
    thresholdGauge(f),
    f.fix ? el("p", { class: "card-fix", text: f.fix }) : null,
    el("div", { class: "card-actions" },
      el("button", { type: "button", class: "listen-btn", "data-audio": listenAudio(), "data-listen": i, onclick: () => listen(i),
        "aria-label": `Listen: ${findingName(f, i)}`, title: isSelf(r) ? "Plays this spot" : "Plays yours, then the reference" }, "Listen"),
      fixButton(f, i)),
    fixSource() ? el("div", { class: "card-status", "data-card-status": f.id, hidden: "" }) : null)));
  tickPoints(document.querySelectorAll("#top-cards .card-pts"));
  document.querySelectorAll("[data-card-status]").forEach(cardStatus);   // a fix finished in an earlier visit shows again
  // the same count as the "Every finding" heading (#flaw-count): flagged findings only; differences sit under their own headings
  const n = r.flaws.length;
  $("#see-all").hidden = !n && !differences().length;
  const [one, many] = isSelf(r) ? ["spot", "spots"] : ["finding", "findings"];
  $("#see-all").textContent = !n ? `See every ${one}` : `See all ${n} ${n === 1 ? one : many}`;
}

// Rows whose flag threshold is a plain physical change; the same rows as app.LIMIT_ROWS (tests/test_app.py compares them).
const LIMIT_ROWS = ["pace", "pauses", "volume"];
const roughFactor = (v) => `×${Math.exp(v).toFixed(1)}`;   // an ln threshold as a speed factor

/** "about ×1.7 faster or ×2.1 slower" from a row's [below, above] thresholds; one number when both round the same; null
 *  without either, also when the row has no thresholds at all (no tol, or no five-reading limits from the server). */
function pairWords(tol, show, lower, higher) {
  const [below, above] = Array.isArray(tol) ? tol : [];
  if (below == null && above == null) return null;
  if (below == null) return `about ${show(above)} ${higher}`;
  if (above == null) return `about ${show(below)} ${lower}`;
  return show(below) === show(above) ? `about ${show(below)} ${lower} or ${higher}` : `about ${show(below)} ${lower} or ${show(above)} ${higher}`;
}

const paceWords = (tol) => pairWords(tol, roughFactor, "faster", "slower");

/** The smallest flagged change of each LIMIT_ROWS row in plain words, from {row key: [below, above]}. */
function limitWords(tol) {
  const pace = paceWords(tol.pace);
  const pauses = pairWords(tol.pauses, (v) => `${v.toFixed(1)} s`, "shorter", "longer");
  const volume = pairWords(tol.volume, (v) => `${Math.round(v)} dB`, "quieter", "louder");
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
    const n = r.flaws.filter((f) => matchesFilter(f, keys, null)).length;
    const card = el("button", { type: "button", class: "card", "aria-pressed": "false", "data-dims": keys.join(",") },
      el("div", { class: "word", text: groupLabel(g.word) }),
      el("div", { class: "fig", text: num(value, 1) }),
      el("div", { class: "bar" }, el("i", { style: `width:${Math.max(0, Math.min(100, value))}%` })),
      scored.length > 1 ? el("div", { class: "lines" }, ...scored.map((d) => el("div", { class: "line", title: `${d.note || ""} Coverage: ${num(d.coverage * 100, 0)}%.` },
        el("span", { text: SUB_NAME[d.key] || d.label }), el("span", { text: num(d.score, 1) })))) : null,
      n ? el("div", { class: "count", text: `${n} ${n === 1 ? "finding" : "findings"}` }) : null);
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

/** One rule for every count and list: a finding matches by its own measure, and by its own or its group's pattern;
 *  "unlabelled" is a finding with neither. */
function matchesFilter(f, filter = S.filter, pattern = S.pattern) {
  return (!filter || filter.includes(f.dimension)) && (!pattern ||
    (pattern === "unlabelled" ? !f.pattern && !f.group_pattern : f.pattern === pattern || f.group_pattern === pattern));
}

function refreshLists() {
  $("#clear-filter").hidden = !S.filter && !S.pattern;
  renderFlawList();
  renderDifferenceList();
  renderClipCards();
  document.querySelectorAll(".pattern-chip").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.pattern === S.pattern)));
}

// A finding without a pattern label gets no chip; the pattern filter still offers "Other findings". A group member
// without its own pattern gets a chip of its group, which filters by the group's pattern.
function patternTags(f) {
  const p = f.pattern || f.group_pattern, own = !!f.pattern;
  const repeats = own && patternText(p) === findingText(f);   // e.g. uneven word timing: type and pattern share one name
  const text = own ? patternText(p) : groupPart(f);
  return el("div", { class: "finding-tags" },
    !p || repeats ? null : el("button", { type: "button", class: "pattern-chip", "data-pattern": p, "aria-pressed": String(S.pattern === p),
      "aria-label": `Filter by pattern: ${patternText(p)}`, onclick: () => setPattern(S.pattern === p ? null : p), text }),
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
  // each group keeps all its members (its heading and penalty) and the members that match the filters (its entries)
  const shown = findingGroups(r).map((all) => ({ all, members: all.filter(([f]) => matchesFilter(f)) })).filter((g) => g.members.length);
  const counted = (members) => members.find(([f]) => f.counted !== false) || members[0];
  if (S.priority != null && wholePassage(r.flaws[S.priority])) shown.sort((a, b) => Number(counted(b.all)[1] === S.priority) - Number(counted(a.all)[1] === S.priority));
  const n = shown.reduce((total, g) => total + g.members.length, 0);
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
  const groupItem = ({ all, members }) => {
    if (all.length === 1) return item(members[0]);
    const [f, i] = counted(all);
    return el("li", { class: "finding-group" },
      el("button", { type: "button", class: "group-select", "data-i": i, "data-kind": "flaw",
        "aria-pressed": String(S.selKind === "flaw" && all.some(([, j]) => S.sel === j)), onclick: () => select(i) },
        el("span", { class: "t", text: `${groupName(f)} group` }), el("span", { class: "pts", text: findingPts(f) }),
        el("span", { class: "m", text: `${all.length} findings share one penalty` })),
      el("ul", { class: "flaws group-members" }, ...members.map(item)));
  };
  const minor = ({ all }) => !saturated(counted(all)[0]) && (counted(all)[0].points_lost ?? 1) < 0.05;
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
  // Plain measure names only: the detection keys ("D7+") and the dimension notes (development statistics) are not for readers.
  const dimLabel = (key) => SUB_NAME[key] || S.result.scores.dims.find((d) => d.key === key)?.label || key;
  const names = [...new Set([...detection.listed_keys, ...detection.listed_clip_keys].map((k) => dimLabel(k.replace(/[+-]$/, ""))))];
  $("#listed-note").textContent = isSelf() ? "Context for your reading from published reading norms; it does not change the score."
    : `${names.join(", ")}: shown for comparison only. For a reader other than the reference speaker, these measures are not reliable enough to flag or to score.`;
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
      // the label ends at the threshold tick, but never starts left of the track (a large multiple puts the tick near the left)
      el("span", { style: `right:min(${(100 - at(1)).toFixed(2)}% + 6px, 100% - ${Math.ceil(textWidth(GAUGE_LABEL, GAUGE_LABEL_PX))}px)`, text: GAUGE_LABEL }),
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
      el("button", { type: "button", class: "listen-btn", "data-audio": listenAudio(), ...(diff ? {} : { "data-listen": S.sel }), onclick: () => listen(S.sel, S.selKind),
        "aria-label": `Listen: ${diff ? findingText(f) : findingName(f, S.sel)}` }, "Listen"),
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
// announce: false on a page load, where the new example is the news, not its first finding.
function select(i, { scroll = false, kind = "flaw", reveal = true, announce = true } = {}) {
  const before = rowDefs(S.result).map((d) => d.key).join();
  // a loop of another finding's fix must not play on under a new selection
  if (S.fix.player?.playing && (S.sel !== i || S.selKind !== kind)) S.fix.player.stop();
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
  const f = selected();
  if (S.youReady && f) S.ws.setTime(mediaSpan(f, "you")[0]);
  if (announce && f) say(kind === "difference" ? `${findingText(f)}, ${quotedWords(S.result, f)}, not scored.`
    : `#${i + 1} ${findingText(f)}, ${quotedWords(S.result, f)}, ${f.counted === false ? "shared penalty" : findingPts(f).replace(/ pts\b/, " points")}.`);
}

/** A short message for screen readers (#announce, polite); the panels themselves are not live regions. */
function say(text) {
  const box = $("#announce");
  box.textContent = "";
  requestAnimationFrame(() => { box.textContent = text; });
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
    // one tab stop for the whole text; the arrow keys move between the words (wordKeys)
    const b = el("button", { type: "button", class: "w" + (wordStyle[i] ? ` f-${wordStyle[i][1]}` : ""), "data-i": i, tabindex: i ? "-1" : "0", text: w.w });
    if (k >= 0) {
      b.dataset.peek = k;
      b.setAttribute("aria-label", `${w.w}: finding #${k + 1} ${findingText(r.flaws[k])}`);
      b.addEventListener("click", () => select(k, { scroll: true }));
    } else {
      b.dataset.audio = "you";
      b.addEventListener("click", () => playSpan("you", [w.p[0], w.p[1] + 0.25]));
    }
    // the icon of a finding stays on the line of its first word
    const icon = k >= 0 && wordFinding[i - 1] !== k ? dimIcon(r.flaws[k].dimension) : null;
    box.append(icon ? el("span", { class: "nowrap" }, icon, b) : b, " ");
  });
}

/** Roving focus in the transcript: Left and Right (also Up and Down) move to the next word, Home and End to the ends. */
function wordKeys(e) {
  const words = [...document.querySelectorAll("#transcript .w")], at = words.indexOf(e.target);
  if (at < 0) return;
  const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
  const to = e.key === "Home" ? 0 : e.key === "End" ? words.length - 1 : step ? Math.min(Math.max(at + step, 0), words.length - 1) : null;
  if (to == null) return;
  e.preventDefault();
  focusWord(words, to);
}

function focusWord(words, to) {
  words.forEach((w, k) => w.setAttribute("tabindex", k === to ? "0" : "-1"));
  words[to].focus();
}

function markWords() {
  const f = selected();
  $("#whole-note").hidden = !(f && wholePassage(f));
  const first = f && !wholePassage(f) ? f.words[0] : 0;
  document.querySelectorAll("#transcript .w").forEach((b) => b.setAttribute("tabindex", +b.dataset.i === first ? "0" : "-1"));
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
    document.querySelectorAll(`.top-card[data-i="${i}"], #flaws button[data-i="${i}"][data-kind="flaw"], .strip-span[data-i="${i}"], .strip-label[data-i="${i}"]`).forEach((n) => {
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
const severityTier = (f) => sevStyle(f.severity ?? 0)[1];

const atOnePoint = (p) => p[1] - p[0] < DISPLAY_HOP_S;   // a missing pause starts and ends at the same time
const widenSpan = (a, b) => b - a >= TL_MIN_SPAN_PX ? [a, b] : [(a + b) / 2 - TL_MIN_SPAN_PX / 2, (a + b) / 2 + TL_MIN_SPAN_PX / 2];
const faultCost = (f) => f.counted === false ? 0 : f.points_lost ?? 0;

/** The local findings that each word of this recording belongs to (word index -> finding indices). */
function faultsByWord(r) {
  const out = new Map();
  r.flaws.forEach((f, i) => {
    if (wholePassage(f)) return;
    for (let w = f.words[0]; w <= f.words[1]; w++) out.set(w, [...(out.get(w) || []), i]);
  });
  return out;
}

/** Heat of each finding on the strip, 0 to 1: at least its severity tier's level, and 1 for the costliest local finding. */
function faultHeats(r) {
  const top = Math.max(MIN_SHOWN_POINTS, ...r.flaws.filter((f) => !wholePassage(f)).map(faultCost));
  return r.flaws.map((f) => wholePassage(f) ? 0 : Math.min(1, Math.max(TIER_HEAT[severityTier(f)], faultCost(f) / top)));
}

/** Strip colour of a heat from 0 (calm, near the panel) through bramble to the light bramble of the worst fault. */
function heatColor(heat) {
  const stops = [[0, css("--strip-calm")], [0.3, css("--strip-low")], [0.6, css("--flag")], [0.85, css("--flag-bar")], [1, css("--flag-text")]];
  const k = Math.max(1, stops.findIndex(([at]) => heat <= at));
  const [a, from] = stops[k - 1], [b, to] = stops[k];
  return mixHex(from, to, Math.min(1, Math.max(0, (heat - a) / (b - a))));
}

/** A finding's span in the reference: its own b span, else its recording span carried through the word map. */
function referenceSpan(f) {
  const m = S.result.map;
  return f.b || [interp(f.p[0], m.p, m.b), interp(f.p[1], m.p, m.b)];
}

/** With a reference, a finding's reference span and a thin link down to its words on this recording's track; style.css
 *  shows it only while the finding is hovered or selected. */
function tlLink(f, i) {
  const g = S.tl, [p0, p1] = widenSpan(...f.p.map(g.x)), [b0, b1] = widenSpan(...referenceSpan(f).map(g.x));
  const bx = (b0 + b1) / 2, mid = (p0 + p1) / 2, bend = (g.refBot + g.youTop) / 2;
  return svgEl("g", { class: "tl-link", "data-i": i ?? "", "aria-hidden": "true" },
    svgEl("rect", { class: "ref-span", x: b0, y: g.refTop, width: b1 - b0, height: TL_REF_TRACK_PX, rx: TL_REF_TRACK_PX / 2 }),
    svgEl("path", { class: "link", d: `M${bx},${g.refBot} C${bx},${bend} ${mid},${bend} ${mid},${g.youTop}` }));
}

/**
 * The strip labels: members of one finding group that touch share one label ("×2"). Only the TOP_N costliest local
 * findings are labelled, under their region, in the highest of TL_MARK_ROWS rows where a label touches no other; a label
 * that does not fit at full length tries its number alone; the rest are counted by the "more" link under the panel.
 */
function placeMarks(r, x, width) {
  const ranked = r.flaws.map((f, i) => [f, i]).filter(([f]) => !wholePassage(f) && shownLoss(faultCost(f)))
    .sort(([a, i], [b, j]) => faultCost(b) - faultCost(a) || i - j).slice(0, TOP_N);
  const top = new Map(ranked.map(([, i], rank) => [i, rank]));
  const marks = [];
  r.flaws.forEach((f, i) => {
    if (wholePassage(f)) return;
    const joined = f.group && marks.find((m) => m.members.some((j) => f.group.includes(r.flaws[j].id))
      && f.p[0] <= m.t1 + TL_JOIN_S && f.p[1] >= m.t0 - TL_JOIN_S);
    if (joined) { joined.members.push(i); joined.t0 = Math.min(joined.t0, f.p[0]); joined.t1 = Math.max(joined.t1, f.p[1]); }
    else marks.push({ members: [i], t0: f.p[0], t1: f.p[1] });
  });
  for (const m of marks) {
    m.main = m.members.reduce((best, i) => faultCost(r.flaws[i]) > faultCost(r.flaws[best]) ? i : best, m.members[0]);
    m.rank = Math.min(...m.members.map((i) => top.get(i) ?? Infinity));
    const f = r.flaws[m.main];
    m.number = `#${m.main + 1}`;
    m.title = `${findingText(f)}${m.members.length > 1 ? ` ×${m.members.length}` : ""}`;
    m.points = `−${num(f.points_lost, 2)}`;
    m.cx = (x(m.t0) + x(m.t1)) / 2;
  }
  const rows = Array.from({ length: TL_MARK_ROWS }, () => []), hidden = [];
  const order = [...marks].sort((a, b) => a.rank - b.rank || a.t0 - b.t0);
  const fits = (row, x0, x1) => rows[row].every((o) => x1 + TL_MARK_GAP <= o.x0 || x0 >= o.x1 + TL_MARK_GAP);
  for (const m of order) {
    if (!Number.isFinite(m.rank)) { hidden.push(m); continue; }
    const full = textWidth(m.number, TL_MARK_FONT, 700) + textWidth(` ${m.title}`, TL_MARK_FONT) + textWidth(` ${m.points}`, TL_MARK_FONT, 700) + 22;
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
  const shown = marks.filter((m) => !hidden.includes(m));
  return { marks: shown, hidden, rows: shown.length ? Math.max(...shown.map((m) => m.row + 1)) : 0 };
}

/** The tooltip and accessible name of a finding on the strip: number, name, words, points and times. */
function stripText(f, i, own) {
  const points = f.counted === false ? "shared penalty" : findingPts(f).replace(/ pts\b/, " points");
  const words = quotedWords(S.result, f);
  const times = `this recording ${span(f.p)}${f.b && !own ? `, reference ${span(referenceSpan(f))}` : ""}`;
  return { tip: `#${i + 1} ${findingText(f)} · ${words} · ${points}`, label: `#${i + 1} ${findingText(f)}, ${words}, ${points}, ${times}` };
}

/**
 * The reference reading above this recording, word by word on one time scale (the longer reading sets the scale). Under
 * this recording's waveform, on the same scale, one strip glows where the findings are (style.css .fault-strip).
 */
function drawTimeline() {
  const host = $("#tl-host"), r = S.result;
  S.tl = null;
  if (!r || !host.clientWidth) return;
  const width = host.clientWidth, own = isSelf(r);
  const pxPerS = Math.max(width - PLOT_R, 1) / Math.max(r.participant.duration, r.baseline.duration);
  const x = (t) => t * pxPerS;
  // rows from the top: reference track, gap, the "This recording" label, this recording's track
  const refTop = 0, refBot = own ? 0 : TL_REF_TRACK_PX, labelMid = refBot + (own ? 0 : TL_LINK_GAP_PX) + TL_LABEL_PX / 2;
  const youTop = labelMid + TL_LABEL_PX / 2, youBot = youTop + TL_TRACK_PX;
  S.tl = { x, refTop, refBot, youTop, youBot, width, own, chipOf: new Map() };
  const svg = svgEl("svg", { width, height: youBot, viewBox: `0 0 ${width} ${youBot}`, role: "group",
    "aria-label": own ? "This recording, word by word" : "Reference and this recording, word by word" });
  $("#lane-ref").hidden = own;
  svg.append(svgEl("text", { class: "tl-label", x: 0, y: labelMid, "dominant-baseline": "central", text: "This recording" }));
  const faults = faultsByWord(r);
  const tickClass = (who, k) => who === "you" && faults.has(k) ? { class: "tl-word you flag", "data-faults": faults.get(k).join(",") } : { class: `tl-word ${who}` };
  // Each word's click target reaches halfway into the gaps to its neighbours and TL_HIT_PAD_PX above and below its bar,
  // because most bars are only a few px wide.
  const track = (who, key, top, height) => {
    const timed = r.words.map((w, k) => [w, k]).filter(([w]) => w[key]);
    return svgEl("g", { "aria-hidden": "true" }, ...timed.map(([w, k], n) => {
      const x0 = x(w[key][0]), wide = Math.max(x(w[key][1]) - x0 - 1, 1);
      const prev = timed[n - 1]?.[0][key], next = timed[n + 1]?.[0][key];
      // the first and the last word have no neighbour on one side, so a short one reaches TL_WORD_MIN_PX there
      const end = next ? (x(w[key][1]) + x(next[0])) / 2 : x0 + wide;
      const left = prev ? (x(prev[1]) + x0) / 2 : Math.max(0, Math.min(x0, end - TL_WORD_MIN_PX));
      const right = next ? end : Math.min(width, Math.max(end, left + TL_WORD_MIN_PX));
      return svgEl("g", { ...tickClass(who, k), onclick: () => playSpan(who, [w[key][0], w[key][1] + 0.25]),
        onpointerenter: (e) => showTip(e.currentTarget, `${w.w}  ${span(w[key])}`), onpointerleave: hideTip },
        svgEl("rect", { class: "hit", x: left, y: top - TL_HIT_PAD_PX, width: Math.max(right - left, wide), height: height + 2 * TL_HIT_PAD_PX }),
        svgEl("rect", { class: "bar", x: x0, y: top, width: wide, height, rx: Math.min(4, height / 2) }));
    }));
  };
  const links = own ? [] : r.flaws.map((f, i) => wholePassage(f) ? null : tlLink(f, i)).filter(Boolean);
  svg.append(own ? "" : track("ref", "b", refTop, TL_REF_TRACK_PX), track("you", "p", youTop, TL_TRACK_PX), ...links, svgEl("g", { id: "tl-diff" }),
    own ? "" : svgEl("line", { id: "tl-cur-ref", class: "tl-cursor", y1: refTop - 3, y2: refBot + 3, style: "display:none" }),
    svgEl("line", { id: "tl-cur-you", class: "tl-cursor", y1: youTop - 3, y2: youBot + 3, style: "display:none" }));
  host.replaceChildren(svg);
  for (const [id, seconds] of [["#wave", r.participant.duration], ["#wave-axis", r.participant.duration], ["#wave-ref", r.baseline.duration]]) {
    $(id).style.width = `${Math.max(seconds * pxPerS, 1)}px`;
  }
  drawStrip(r, x, width);
  markTimeline();
}

/** The severity strip under this recording's waveform: the heat, one focusable span per local finding (a tick for a
 *  finding at one point in time), the labels of the costliest findings, and the count of the others. */
function drawStrip(r, x, width) {
  const g = S.tl, trackW = Math.max(x(r.participant.duration), 1), heats = faultHeats(r), layout = placeMarks(r, x, width - PLOT_R);
  layout.marks.concat(layout.hidden).forEach((m, k) => m.members.forEach((i) => g.chipOf.set(i, k)));
  const local = r.flaws.map((f, i) => [f, i]).filter(([f]) => !wholePassage(f));
  const order = local.map(([, i]) => i);   // intro order: by time
  const seq = (i) => `--seq:${Math.min(order.indexOf(i), BAND_STEPS)}`;
  // narrower spans lie on top, so each stays reachable inside a longer one
  const widths = local.map(([f]) => { const [a, b] = widenSpan(...f.p.map(x)); return Math.max(b - a, STRIP_HIT_PX); });
  const lefts = local.map(([f], k) => { const [a, b] = widenSpan(...f.p.map(x)); return b - a >= STRIP_HIT_PX ? a : (a + b) / 2 - widths[k] / 2; });
  const halves = stripHalves(lefts, widths);
  const spans = local.map(([f, i], k) => {
    const w = widths[k], left = lefts[k];
    const text = stripText(f, i, g.own);
    return el("button", { type: "button", class: `strip-span${atOnePoint(f.p) ? " point" : ""}${halves.has(k) ? ` ${halves.get(k)}` : ""}`, "data-i": i, "data-peek": i, "data-chip": g.chipOf.get(i),
      "aria-pressed": "false", "aria-label": text.label, style: `left:${left.toFixed(1)}px;width:${w.toFixed(1)}px;z-index:${1 + widths.filter((v) => v > w).length};--c:${heatColor(heats[i])};${seq(i)}`,
      onclick: (e) => pickOnStrip(e, i), onpointerenter: (e) => showTip(e.currentTarget, text.tip), onpointerleave: hideTip,
      onfocus: (e) => showTip(e.currentTarget, text.tip), onblur: hideTip });
  });
  const stripTrack = el("div", { class: "strip-track", style: `width:${trackW.toFixed(1)}px` }, ...spans, el("div", { class: "strip-diff", hidden: "" }));
  const labelsH = layout.rows ? TL_MARK_GAP + layout.rows * (TL_MARK_H + TL_MARK_GAP) : 0;
  const labels = svgEl("svg", { class: "strip-labels", width, height: labelsH, viewBox: `0 0 ${width} ${labelsH}`, "aria-hidden": "true" });
  for (const m of layout.marks) {
    const f = r.flaws[m.main], top = TL_MARK_GAP + m.row * (TL_MARK_H + TL_MARK_GAP), y = top + TL_MARK_H / 2;
    const pick = () => select(m.main), name = `${m.number} ${m.title}, ${m.points} points`;
    // a label moved off its region keeps a leader from its region down to the label
    const to = Math.min(Math.max(m.cx, m.x0 + TL_MARK_H / 2), m.x0 + m.w - TL_MARK_H / 2);
    labels.append(svgEl("line", { class: "strip-leader", "data-chip": g.chipOf.get(m.main), style: seq(m.main), x1: m.cx, x2: to, y1: 0, y2: top }),
      svgEl("g", { class: `strip-label${m.compact ? " compact" : ""}`, "data-i": m.main, "data-members": m.members.join(","), "data-chip": g.chipOf.get(m.main),
        "data-peek": m.main, style: seq(m.main), onclick: pick,
        onpointerenter: m.compact ? (e) => showTip(e.currentTarget, name) : null, onpointerleave: m.compact ? hideTip : null },
      svgEl("rect", { x: m.x0, y: top, width: m.w, height: TL_MARK_H, rx: TL_MARK_H / 2 }),
      svgEl("text", { x: m.compact ? m.x0 + m.w / 2 : m.x0 + 10, y, "text-anchor": m.compact ? "middle" : "start" },
        svgEl("tspan", { class: "n", text: m.number }),
        ...(m.compact ? [] : [svgEl("tspan", { text: ` ${m.title}` }), svgEl("tspan", { class: "pts", dx: 4, text: ` ${m.points}` })]))));
  }
  $("#fault-strip").replaceChildren(stripTrack, labels);
  const more = layout.hidden.reduce((n, m) => n + m.members.length, 0);
  $("#tl-more").hidden = !more;
  $("#tl-more").textContent = `+${more} more`;
  $("#tl-more").setAttribute("aria-label", `${more} more ${more === 1 ? "finding" : "findings"} in the list`);
}

/**
 * A press on the strip selects the span on top. When the selected finding also lies under the pointer, it selects the next
 * span down at that point instead, so repeated presses reach a span that others cover at any width. A key selects its own span.
 */
function pickOnStrip(e, own) {
  const stack = e.detail ? document.elementsFromPoint(e.clientX, e.clientY).filter((n) => n.classList.contains("strip-span")).map((n) => +n.dataset.i) : [];
  const at = S.selKind === "flaw" ? stack.indexOf(S.sel) : -1;
  const pick = at < 0 ? own : stack[(at + 1) % stack.length];
  select(pick);
  // the focus, and with it the tooltip, moves to the span selected under the one pressed
  if (pick !== own) document.querySelector(`#fault-strip .strip-span[data-i="${pick}"]`).focus({ preventScroll: true });
}

/**
 * Half-height places on the strip (span index -> "lower" or "upper") that keep every span reachable. A span is drawn over
 * the wider spans and over an equal one earlier in time. When the spans over a span leave it no free stretch of
 * STRIP_FREE_PX, they move to the lower half and the covered span keeps the upper half; a lower span covered in the lower
 * half the same way moves to the upper half.
 */
function stripHalves(lefts, widths) {
  const above = (j, k) => widths[j] < widths[k] || (widths[j] === widths[k] && j > k);
  const covered = (k, pool) => {
    const right = lefts[k] + widths[k];
    const over = pool.filter((j) => above(j, k) && lefts[j] < right && lefts[j] + widths[j] > lefts[k]).sort((a, b) => lefts[a] - lefts[b]);
    let reach = lefts[k], gap = 0;
    for (const j of over) {
      gap = Math.max(gap, lefts[j] - reach);
      reach = Math.max(reach, lefts[j] + widths[j]);
    }
    return Math.max(gap, right - reach) < STRIP_FREE_PX ? over : null;
  };
  const all = lefts.map((_, k) => k), halves = new Map();
  for (const k of all) covered(k, all)?.forEach((j) => halves.set(j, "lower"));
  const lower = [...halves.keys()];
  for (const k of lower) if (covered(k, lower)) halves.set(k, "upper");
  return halves;
}

function markTimeline() {
  if (!S.tl || !S.result || !$("#tl-host svg")) return;
  const f = selected(), flaw = S.selKind === "flaw";
  const inGroup = (i) => flaw && !!f?.group?.includes(S.result.flaws[i].id);
  const mark = (node, members) => {
    const on = flaw && members.includes(S.sel);
    node.classList.toggle("sel", on);
    node.classList.toggle("grp", !on && members.some(inGroup));
    return on;
  };
  document.querySelectorAll("#fault-strip .strip-span").forEach((s) => s.setAttribute("aria-pressed", String(mark(s, [+s.dataset.i]))));
  document.querySelectorAll("#fault-strip .strip-label").forEach((m) => mark(m, m.dataset.members.split(",").map(Number)));
  document.querySelectorAll("#fault-strip .strip-leader").forEach((l) => l.classList.toggle("sel", flaw && S.sel != null && +l.dataset.chip === S.tl.chipOf.get(S.sel)));
  document.querySelectorAll("#tl-host .tl-link[data-i]").forEach((l) => mark(l, [+l.dataset.i]));
  document.querySelectorAll("#tl-host .tl-word.flag").forEach((t) => mark(t, t.dataset.faults.split(",").map(Number)));
  // a selected reference difference: a neutral span on the strip, and its link to the reference
  const diff = !flaw && f && !wholePassage(f), box = $("#fault-strip .strip-diff");
  $("#tl-diff").replaceChildren(diff && !S.tl.own ? tlLink(f, null) : "");
  box.hidden = !diff;
  if (diff) {
    const [a, b] = widenSpan(...f.p.map(S.tl.x));
    box.style.left = `${a.toFixed(1)}px`;
    box.style.width = `${(b - a).toFixed(1)}px`;
  }
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

/** Linked highlighting: one finding's words, strip span and label stay bright while the other flagged words and labels fade. */
function peek(i) {
  const on = i != null && i !== "";
  document.body.classList.toggle("peeking", on);
  document.querySelectorAll(".peek").forEach((n) => n.classList.remove("peek"));
  if (!on) return;
  const f = S.result?.flaws[+i];
  if (!f) return;
  const chip = S.tl?.chipOf.get(+i);
  document.querySelectorAll(`.strip-span[data-i="${i}"], .tl-link[data-i="${i}"], .top-card[data-i="${i}"]${chip == null ? "" : `, #fault-strip [data-chip="${chip}"]`}`).forEach((n) => n.classList.add("peek"));
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
  // still starts on its wash; otherwise it is left out, because the list and the severity strip also carry it.
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
  // no scroll: the chart stays under the pointer; the wide-screen panel is sticky, and the announcement names the finding
  select(hits[0][1], { kind: hits[0][2] });
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
  S.youReady = false; S.refReady = false;
  setPlaying();
  showProgress("you", 0);
  document.documentElement.style.removeProperty("--t");   // the hero light returns to its rest place (style.css .glow)
  clockStatus("Loading audio…");
  $("#cursor").style.display = "none";
  hideTimelineCursor();
  clearKaraoke();
  updatePlayback();
}

function mixHex(a, b, share) {
  const channel = (hex, k) => parseInt(hex.slice(1 + 2 * k, 3 + 2 * k), 16);
  return `#${[0, 1, 2].map((k) => Math.round(channel(a, k) + (channel(b, k) - channel(a, k)) * share).toString(16).padStart(2, "0")).join("")}`;
}

function loadMedia(r, base) {
  showSide("you");   // before invalidateMedia, whose setPlaying labels the main button by the side
  invalidateMedia();
  const token = S.mediaId;
  $("#wave-msg").textContent = "";
  const ref = S.ref = new Audio();
  const own = !r.baseline?.audio;   // no reference reading: nothing to load or draw in the reference lane
  const refCurrent = () => token === S.mediaId && S.ref === ref;
  ref.addEventListener("canplay", () => { if (refCurrent()) { S.refReady = true; updatePlayback(); } });
  ref.addEventListener("play", () => { if (refCurrent()) setPlaying(); });
  ref.addEventListener("pause", () => { if (refCurrent()) setPlaying(); });
  ref.addEventListener("error", () => { if (refCurrent()) { S.refReady = false; updatePlayback(); $("#wave-msg").textContent = "The reference audio could not be loaded."; } });
  ref.preload = "auto";
  if (!own) ref.src = base + r.baseline.audio;
  if (!S.hasLibs) { clockStatus("Recording playback unavailable"); return; }
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
  // the time axis goes under the severity strip, so the strip lies right under the bars
  ws.registerPlugin(WaveSurfer.Timeline.create({ container: "#wave-axis", height: 16, style: { color: css("--muted"), fontSize: "11px" } }));
  ws.on("ready", () => {
    if (!current()) return;
    S.youReady = ws.getDuration() > 0;
    if (S.youReady) clockAt("you", 0, ws.getDuration()); else clockStatus("Audio unavailable");
    updatePlayback();
  });
  ws.on("timeupdate", (t) => {
    if (!current() || !S.youReady) return;
    clockAt("you", t, ws.getDuration());
    showProgress("you", t / ws.getDuration());
    moveCursor(t); markPlaying(t);
    showReferenceAt(interp(t, S.result.map.p, S.result.map.b));
    moveTimelineCursor(t, interp(t, S.result.map.p, S.result.map.b));
  });
  ws.on("play", () => { if (current()) setPlaying(); });
  ws.on("pause", () => { if (current()) setPlaying(); });
  const failed = (e) => {
    if (!current() || e?.name === "AbortError") return;
    S.youReady = false; updatePlayback();
    clockStatus("Audio unavailable");
    $("#wave-msg").textContent = "The recording audio could not be loaded.";
  };
  ws.on("error", failed);
  ws.load(base + r.participant.audio).catch(failed);
}

/** This recording in the accent at moderate opacity; heard bars at full accent. */
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
function watchLevel(media) {
  const run = ++S.levelId;   // one frame loop at a time, on the element that plays now
  if (!media) {
    S.level = 0;
    document.documentElement.style.setProperty("--level", "0");
    document.querySelectorAll(".meter i").forEach((bar) => { bar.style.transform = ""; });
    return;
  }
  const node = analyserFor(media);
  if (!node) return;
  S.audio.resume?.();
  const wave = new Uint8Array(node.fftSize), bins = new Uint8Array(node.frequencyBinCount), bars = [...document.querySelectorAll(".meter i")];
  let level = 0;
  const frame = () => {
    if (run !== S.levelId) return;
    node.getByteTimeDomainData(wave);
    let sum = 0;
    for (const v of wave) sum += ((v - 128) / 128) ** 2;
    level = 0.8 * level + 0.2 * Math.min(1, Math.sqrt(sum / wave.length) * 6);   // RMS, scaled so speech reaches about 1
    S.level = level;
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

function clockStatus(text) {
  $("#clock").textContent = text;
  $("#player-progress").setAttribute("aria-valuetext", text);
}

/** The clock and the slider's spoken value at t (s) of a reading `length` s long; who: "you" or "ref". */
function clockAt(who, t, length) {
  const name = who === "ref" ? "Reference " : "";
  $("#clock").textContent = `${name}${t.toFixed(2)} / ${length.toFixed(2)} s`;
  $("#player-progress").setAttribute("aria-valuetext", `${name}${t.toFixed(2)} of ${length.toFixed(2)} seconds`);
}

/** The player's progress groove: the share of the playing reading heard so far, in its own colour. */
function showProgress(who, share) {
  const bar = $("#player-progress");
  const clamped = Number.isFinite(share) ? Math.min(Math.max(share, 0), 1) : 0;
  bar.classList.toggle("ref", who === "ref");
  bar.firstElementChild.style.width = `${(100 * clamped).toFixed(2)}%`;
  bar.setAttribute("aria-valuenow", (100 * clamped).toFixed(0));
  document.documentElement.style.setProperty("--t", clamped.toFixed(4));   // the hero light follows the playback position
  S.heroT = clamped;
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
// The hero is a sea of clouds at dusk: a snowy massif and a far range stand above rolling rows of cloud, a dark ridge rises
// out of them. Everything is drawn from the reading's loudness. Decorative only (aria-hidden).
const RIDGE_DB = [-40, 10];        // loudness range (dB re voiced median) mapped from silence to the loudest
const LIGHT_AT = 0.7;              // rest position of the low sun, as a share of the width (style.css .glow, --t)
const SKY_STEP = 2;                // px between the samples of a skyline
// Ranges, back to front. top, low: summit height as a share of the horizon height for the loudest and the quietest
// summit; spacing: px of width per main summit; rough: midpoint displacement of the ridge as a share of a segment's length;
// snowAt: snow lies above this share of the horizon height; snowShare: snow depth as a share of the height above snowAt.
const RANGES = {
  far: { top: 0.9, low: 0.5, spacing: 170, rough: 0.22, rock: "#6e6390", snow: "#e3d9e8", snowAt: 0.5, snowShare: 0.5 },
  mid: { top: 1, low: 0.5, spacing: 230, rough: 0.26, rock: "#221e2d", snow: "#f6ece8", snowAt: 0.46, snowShare: 0.55 },
  near: { top: 0.5, low: 0.3, spacing: 380, rough: 0.08, rock: "#141119" },
};
const SNOW_SHADE = "#2a2440";      // laid over the faces turned away from the sun, so rock and snow both fall into shade

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

/** A polyline refined by midpoint displacement: each round puts a point in the middle of every segment, moved up or down
 *  by up to rough x the segment's length; segments halve each round, so the moves halve too (Fournier, Fussell & Carpenter 1982). */
function displace(points, rounds, rough, salt) {
  let line = points;
  for (let round = 0; round < rounds; round++) {
    const next = [line[0]];
    for (let j = 1; j < line.length; j++) {
      const [[xa, ha], [xb, hb]] = [line[j - 1], line[j]];
      const move = (rockNoise(j + 97 * round, salt) - 0.5) * 2 * rough * (xb - xa);
      next.push([(xa + xb) / 2, Math.max(0, (ha + hb) / 2 + move)], line[j]);
    }
    line = next;
  }
  return line;
}

/** A skyline as [x, h] samples SKY_STEP px apart, by linear interpolation of a polyline. */
function sampleLine(line, width) {
  const out = [];
  let j = 1;
  for (let x = -8; x <= width + 8; x += SKY_STEP) {
    while (j < line.length - 1 && line[j][0] < x) j++;
    const [[xa, ha], [xb, hb]] = [line[j - 1], line[j]];
    out.push([x, ha + (hb - ha) * Math.min(1, Math.max(0, (x - xa) / Math.max(xb - xa, 1e-6)))]);
  }
  return out;
}

/** The main summits of a range from a loudness contour, then cols between them, then a jagged ridge by midpoint
 *  displacement. share(x) scales the heights down under the hero text. */
function rangeSkyline(contour, spec, width, height, share, salt) {
  // a narrow screen gets narrower summits too, so a phone shows a few peaks and not one long ridge
  const n = contour.length, count = Math.max(3, Math.round(width / (spec.spacing * Math.min(1, width / 1000))));
  const peaks = pickSummits(contour, count, Math.round(0.6 * n / count)).map((i) => {
    const x = (i + 0.5) * width / n;
    // the power spreads the summit heights: a contour scaled to its percentiles puts many summits near the top
    return [x, height * (spec.low + (spec.top - spec.low) * contour[i] ** 1.8) * share(x)];
  });
  const line = [[-8, 0.5 * peaks[0][1]]];
  peaks.forEach((peak, k) => {
    if (k > 0) {
      const prev = peaks[k - 1];
      // the col sits nearer the lower summit, so the higher summit keeps a long ridge
      const f = prev[1] > peak[1] ? 0.62 : 0.38;
      line.push([prev[0] + f * (peak[0] - prev[0]), (0.5 + 0.12 * rockNoise(k, salt + 1)) * Math.min(prev[1], peak[1])]);
    }
    line.push(peak);
  });
  line.push([width + 8, 0.5 * peaks.at(-1)[1]]);
  return { peaks, skyline: sampleLine(displace(line, 5, spec.rough, salt), width) };
}

/** Snow on a skyline above snowAt: a snowfield that thickens towards the summits, with a ragged lower edge. */
function snowDepths(skyline, spec, height, salt) {
  const line = height * spec.snowAt;
  // noise interpolated between random values every 7 px: straight runs between sharp turns, so the lower edge is a row
  // of pointed teeth like wind-blown snow, not a staircase
  const jag = (x) => {
    const t = (x + 8) / 7, i = Math.floor(t);
    return rockNoise(i, salt) + (rockNoise(i + 1, salt) - rockNoise(i, salt)) * (t - i);
  };
  return skyline.map(([x, h]) => {
    if (h < line) return 0;
    // never more than 24 % of the mountain's height, so a high range is not buried in snow
    return Math.min(0.24 * h, spec.snowShare * (h - line) + 2) * (0.55 + 0.9 * jag(x));
  });
}

/** Couloirs: streaks of snow down a gully from just under a summit, one on each side, as in a real face where snow lies in
 *  the gullies between ribs of rock. Each is a tapered ribbon with ragged edges, as [x, h] points around its outline. */
function couloirs(peaks, spec, height, salt) {
  return peaks.filter(([, h]) => h > height * spec.snowAt).flatMap(([x, h], k) => [-1, 1].map((side, j) => {
    const r = (m) => rockNoise(k * 2 + j, salt + m);
    const h0 = h * (0.8 - 0.08 * r(0)), x0 = x + side * (h - h0) * 0.75, length = h * (0.14 + 0.14 * r(1));
    // the fall line is steeper than the ridge: about 65 to 75 degrees from the horizontal
    const run = side * length * (0.28 + 0.16 * r(2)), top = 6 + 6 * r(3);
    const edge = (sideOfRibbon) => Array.from({ length: 6 }, (_, i) => {
      const f = i / 5, w = top * (1 - f) + 0.6;
      return [x0 + run * f + sideOfRibbon * w * (0.7 + 0.6 * rockNoise(i + 7 * k, salt + 4 + j + sideOfRibbon)), h0 - length * f];
    });
    return [...edge(-1), ...edge(1).reverse()];
  }));
}

const skyPath = (points, height) => `M${points.map(([x, h]) => `${x.toFixed(1)} ${(height - h).toFixed(1)}`).join(" L")} Z`;

/** The right end of the widest line of an element's text, in viewport px (the element box can be wider than its text). */
function textRight(el) {
  const range = document.createRange();
  range.selectNodeContents(el);
  return Math.max(...[...range.getClientRects()].map((r) => r.right));
}

/** The hero horizon for a result: the reference's loudness raises the far range and the massif (with no reference, longer
 *  averages of this recording: its typical delivery), this recording raises the dark ridge and the cloud sea. */
function drawHorizon(r) {
  const energy = r.rows?.find((row) => row.key === "energy");
  if (!energy?.p?.length) return;
  S.horizon = { energy, self: isSelf(r) };
  drawRanges();
  startSea();
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
  // behind the hero text the ranges stand a little lower and carry no snow: dark rock keeps the cream text readable
  // on a phone the horizon starts under the text, so no range stands behind it
  const pastText = (x) => {
    if (bottom <= 0) return 1;
    const f = Math.min(1, Math.max(0, (x - right - 16) / 200));
    return f * f * (3 - 2 * f);
  };
  const share = (x) => 0.82 + 0.18 * pastText(x);
  const samples = Math.max(64, Math.round(width / 4));
  const source = { far: self ? [energy.p, 14] : [energy.b, 8], mid: self ? [energy.p, 9] : [energy.b, 5], near: [energy.p, 10] };
  const sunX = LIGHT_AT * width;
  Object.entries(RANGES).forEach(([name, spec], salt) => {
    const [frames, sigma] = source[name];
    const { peaks, skyline } = rangeSkyline(loudnessContour(frames, samples, sigma), spec, width, height, share, 31 * salt + 5);
    const outline = skyPath([[-8, -2], ...skyline, [width + 8, -2]], height);
    const parts = [svgEl("path", { d: outline, fill: spec.rock })];
    if (spec.snow) {
      const depth = snowDepths(skyline, spec, height, 31 * salt + 9).map((d, j) => d * pastText(skyline[j][0]));
      const lower = skyline.map(([x, h], j) => [x, h - depth[j]]).reverse();
      const snowy = peaks.filter(([x]) => pastText(x) > 0.5);
      const streaks = couloirs(snowy, spec, height, 31 * salt + 13).map((ribbon) => skyPath(ribbon, height)).join(" ");
      parts.push(svgEl("path", { d: `${skyPath([...skyline, ...lower], height)} ${streaks}`, fill: spec.snow }));
      // the faces turned away from the sun: from each summit down to the floor on its far side
      const shade = peaks.map(([x, h]) => {
        const away = x < sunX ? -1 : 1;
        return skyPath([[x, h], [x + away * 1.2 * h, -2], [x + away * 0.12 * h, -2]], height);
      }).join(" ");
      parts.push(svgEl("path", { d: shade, fill: SNOW_SHADE, opacity: 0.5 }));
      parts.push(svgEl("rect", { class: "alpenglow", x: 0, y: 0, width, height }));
    }
    const svg = $(`#range-${name}`);
    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    const clip = svgEl("clipPath", { id: `clip-${name}` }, svgEl("path", { d: outline }));
    svg.replaceChildren(svgEl("defs", {}, clip), parts[0], svgEl("g", { "clip-path": `url(#clip-${name})` }, ...parts.slice(1)));
  });
}

// ---------------------------------------------------------------------------------------------------- hero cloud sea
// Rows of rolling cloud, back to front. Each billow's height is the loudness of the reading at the billow's time (the
// width of the hero is the whole reading), so the crests of the sea are its sound. While audio plays, the billows at the
// playback position swell with the live level, and the sea rolls slowly. at: the row's base as a share of the canvas
// height; w: billow width in px; amp: billow height in px for the loudest stretch; round: billow height to width, from
// flat far rolls to round near ones; blur: px of soft edge; colours of a billow from its sunlit top to its shadow.
// The hero cards cover about the lowest fifth of the canvas, so the nearest row sits above that.
const SEA_ROWS = [
  { at: 0.3, w: 84, amp: 12, round: 0.7, blur: 3, top: "#dcbccb", mid: "#9a8ab3", low: "#776c9b", source: "b" },
  { at: 0.46, w: 116, amp: 20, round: 0.85, blur: 2.5, top: "#eac4c6", mid: "#a291ba", low: "#74699a", source: "b" },
  { at: 0.64, w: 154, amp: 30, round: 1, blur: 2, top: "#f5cdc1", mid: "#ab99be", low: "#776c9c", source: "p" },
  { at: 0.84, w: 196, amp: 40, round: 1.05, blur: 1.7, top: "#fbd8c8", mid: "#b4a2c4", low: "#7c70a0", source: "p" },
];
const SEA_MIST = "#7f739f";        // the haze where the sea meets the mountains, fading out upwards
const SEA_SUN = "#ffd6bd";         // billow tops near the low sun take on its colour
const SEA_ROLL = 5;                // px per second the billows roll while idle; playback rolls them three times as fast
const SEA_SWELL = 1.8;             // extra billow height at the playback position, per unit of live level
const SEA_REACH = 90;              // px; how far the swell spreads from the playback position (Gaussian sigma)
const SEA_IDLE_MS = 50;            // ms between idle frames

/** Starts (or restarts) the cloud sea for the current result; one animation loop at a time. */
function startSea() {
  const canvas = $("#cloud-sea"), { energy, self } = S.horizon;
  const width = canvas.clientWidth, height = canvas.clientHeight;
  if (!width || !height) return;
  const ratio = Math.min(2, devicePixelRatio || 1);
  canvas.width = Math.round(width * ratio);
  canvas.height = Math.round(height * ratio);
  const columns = Math.max(64, Math.round(width / 6));
  const loud = { p: loudnessContour(energy.p, columns, 1.5), b: loudnessContour(self ? energy.p : energy.b, columns, self ? 6 : 1.5) };
  S.sea = { canvas, width, height, ratio, loud, ground: css("--base"), id: (S.sea?.id ?? 0) + 1, roll: 0, last: performance.now() };
  const id = S.sea.id;
  const frame = (now) => {
    if (!S.sea || S.sea.id !== id) return;
    const playing = !!playingMedia(), still = reducedMotion();
    // idle, the sea is redrawn about 20 times a second, and not at all while it is scrolled out of view
    const due = playing || now - S.sea.last >= SEA_IDLE_MS || still;
    if (due && canvas.getBoundingClientRect().bottom > 0) {
      S.sea.roll += still ? 0 : ((now - S.sea.last) / 1000) * SEA_ROLL * (playing ? 3 : 1);
      drawSea(playing && !still ? S.level || 0 : 0);
    }
    if (due) S.sea.last = now;
    if (!still && !document.hidden) requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);
}

/** One frame of the sea, back row first. A row is a band of shadowed cloud with billows on its crest; each billow is an
 *  ellipse lit from above and from the low sun, so the crest reads as rolling volumes and not as a cut-out line. */
function drawSea(level) {
  const { canvas, width, height, ratio, loud, roll } = S.sea;
  const ctx = canvas.getContext("2d");
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  ctx.clearRect(0, 0, width, height);
  const playX = (S.heroT ?? LIGHT_AT) * width, sunX = LIGHT_AT * width;
  const mist = ctx.createLinearGradient(0, 0, 0, 0.36 * height);
  mist.addColorStop(0, "rgba(127, 115, 159, 0)");
  mist.addColorStop(1, SEA_MIST);
  ctx.fillStyle = mist;
  ctx.fillRect(0, 0, width, height);
  SEA_ROWS.forEach((row, k) => {
    const base = row.at * height, contour = loud[row.source], n = contour.length;
    // the front rows roll faster than the back rows, so the sea has depth
    const shift = (roll * (0.4 + 0.6 * k / (SEA_ROWS.length - 1))) % (0.5 * row.w);
    ctx.filter = `blur(${row.blur}px)`;
    ctx.fillStyle = row.low;
    ctx.fillRect(0, base - 0.25 * row.amp, width, height);
    for (let c = -row.w + shift, j = 0; c < width + row.w; c += 0.5 * row.w, j++) {
      const x = c + (rockNoise(j, 50 + k) - 0.5) * 0.4 * row.w;
      const a = contour[Math.min(n - 1, Math.max(0, Math.floor(x / width * n)))];
      const voice = level * Math.exp(-(((x - playX) / SEA_REACH) ** 2) / 2), swell = 1 + SEA_SWELL * voice;
      // big rolls and small lobes alternate, each a little higher or lower, so the crest is not a row of scallops
      const big = j % 3 !== 1, lift = (rockNoise(j, 60 + k) - 0.5) * 0.35 * row.amp;
      const h = row.amp * (big ? 1 : 0.6) * (0.25 + 0.75 * a ** 1.2) * swell, w = row.w * (big ? 0.8 + 0.5 * rockNoise(j, 70 + k) : 0.5);
      // far rolls are long and flat, near ones rounder, as in a sea of cloud seen from a summit
      const cy = base - lift - 0.1 * h, ry = row.round * (0.85 * h + 0.25 * row.amp);
      const light = ctx.createRadialGradient(x + 0.2 * w, cy - 0.9 * ry, 0, x, cy - 0.3 * ry, w * 1.1);
      const sun = Math.exp(-(((x - sunX) / (0.3 * width)) ** 2));
      // the low sun warms the tops near it, and the voice lights the tops where it is speaking
      light.addColorStop(0, mixHex(row.top, SEA_SUN, Math.min(1, 0.55 * sun + 1.2 * voice)));
      light.addColorStop(0.4, row.mid);
      light.addColorStop(0.85, row.low);
      ctx.fillStyle = light;
      ctx.beginPath();
      ctx.ellipse(x, cy, w, ry, 0, 0, 2 * Math.PI);
      ctx.fill();
    }
  });
  ctx.filter = "none";
  // the voice lights the sea where it is speaking
  if (level > 0) {
    const glow = ctx.createRadialGradient(playX, 0.5 * height, 0, playX, 0.5 * height, 2 * SEA_REACH);
    glow.addColorStop(0, `rgba(255, 224, 202, ${(0.7 * level).toFixed(3)})`);
    glow.addColorStop(1, "rgba(255, 224, 202, 0)");
    // only on the cloud already drawn, so the light never shows on the empty sky above the sea
    ctx.globalCompositeOperation = "source-atop";
    ctx.fillStyle = glow;
    ctx.fillRect(0, 0, width, height);
    ctx.globalCompositeOperation = "source-over";
  }
  // the sea sinks into the page ground at the floor, so the horizon has no seam
  const ground = ctx.createLinearGradient(0, 0.62 * height, 0, height);
  ground.addColorStop(0, "rgba(31, 30, 29, 0)");
  ground.addColorStop(1, S.sea.ground);
  ctx.fillStyle = ground;
  ctx.fillRect(0, 0, width, height);
}

/** The one element that plays now: this recording, the reference, or a fix loop; null when nothing plays. */
function playingMedia() {
  if (!S.ref.paused) return S.ref;
  if (S.ws?.isPlaying()) return S.ws.getMediaElement();
  const loop = S.fix.player;
  return loop?.playing ? loop.element(loop.side) : null;
}

/** The main button, the level meter and the Listen marks show what plays now; every start and stop calls this. */
function setPlaying() {
  const media = playingMedia(), loop = !!media && media !== S.ref && !S.ws?.isPlaying();
  if (!media && !S.bothTimer) S.listenAt = null;
  markListening();
  watchLevel(media);
  const btn = $("#play-all");
  btn.classList.toggle("playing", !!media);
  // a fix loop cannot resume from the main button, so it offers Stop, not Pause
  btn.textContent = loop ? "Stop" : media ? "Pause" : S.side === "you" ? "Play recording" : "Play reference";
  updatePlayback();
}

// s; a position this close to the end counts as the end, so Play starts the reading again from 0
const END_S = 0.1;

/** The main play button plays the chosen reading from its current position (from 0 after the end), or stops any playback. */
function togglePlay() {
  if (playingMedia()) return stopAll();
  if (S.side === "you") {
    if (!S.youReady) return;
    const at = S.ws.getCurrentTime(), end = S.ws.getDuration();
    playSpan("you", [end - at < END_S ? 0 : at, end]);
    return;
  }
  if (!S.refReady) return;
  const at = S.ref.duration - S.ref.currentTime < END_S ? 0 : S.ref.currentTime;
  playSpan("ref", [at, S.ref.duration]);
}

/** The reference's position on the clock and the progress groove. */
function showReferenceClock(t) {
  if (!Number.isFinite(S.ref.duration)) return;
  clockAt("ref", t, S.ref.duration);
  showProgress("ref", t / S.ref.duration);
}

/**
 * Seek this recording to t (s). wavesurfer 8.0.1 keeps a seek made while the audio is not ready (readyState < 3, as during
 * an earlier seek) as pending, and the "seeking" event of that earlier seek drops it; so quick seeks (a drag, a held key)
 * kept only the first. The media element takes the time at once, so the pending time already matches it.
 */
function seekYours(t) {
  const media = S.ws.getMediaElement();
  if (media.readyState < 3) media.currentTime = t;
  S.ws.setTime(t);
}

/** Seek the chosen reading to a share (0 to 1) of its length; a reading that plays continues from there. */
function seekShare(share) {
  const at = Math.min(Math.max(share, 0), 1);
  if (S.side === "you") {
    if (S.youReady) seekYours(at * S.ws.getDuration());
    return;
  }
  if (!S.refReady) return;
  const t = at * S.ref.duration;
  if (!S.ref.paused) { playSpan("ref", [t, S.ref.duration]); return; }
  S.ref.currentTime = t;
  showReferenceClock(t);
  const m = S.result.map, tp = interp(t, m.b, m.p);
  moveCursor(tp); moveTimelineCursor(tp, t); showReferenceAt(t);
}

/** The A/B switch: the other reading takes the aligned time; while playing it continues from there. */
function setSide(side) {
  if (side === S.side) return;
  const m = S.result?.map, playingYou = !!S.ws?.isPlaying(), playingRef = !S.ref.paused;
  const tp = S.youReady ? S.ws.getCurrentTime() : null, tb = S.ref.currentTime;
  S.side = side;
  $("#ab-you").setAttribute("aria-pressed", String(side === "you"));
  $("#ab-ref").setAttribute("aria-pressed", String(side === "ref"));
  setPlaying();
  if (!m) return;
  if (side === "ref" && playingYou) playSpan("ref", [interp(tp, m.p, m.b), S.ref.duration]);
  else if (side === "you" && playingRef) playSpan("you", [interp(tb, m.b, m.p), S.ws.getDuration()]);
  else if (side === "ref" && tp != null && S.refReady) { const at = interp(tp, m.p, m.b); S.ref.currentTime = at; showReferenceClock(at); }
  else if (side === "you" && S.youReady) S.ws.setTime(interp(tb, m.b, m.p));   // its timeupdate shows this recording's clock
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
        showReferenceClock(ref.currentTime);
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

function fixButton(f, i) {
  if (!fixSource()) return null;
  const text = HEAR_FIXED[isSelf() ? "self" : "reference"];
  // the name says which finding: a page has one such button per card and one in the panel
  const button = el("button", { type: "button", class: "fix-btn", "data-fix": f.id, onclick: () => hearFixed(i), "aria-label": `${text}: ${findingName(f, i)}` }, text);
  showFixWait(button);
  return button;
}

/** Why a fix button is disabled: the server runs one fix at a time. */
function busyText() {
  if (!S.fix.busy) return "";
  return S.fix.busy.source === fixKey(S.fix.source) ? "One fix runs at a time: this button works again when the running fix has finished."
    : "A fix of another example is still running: this button works again when it has finished.";
}

function showFixWait(button) {
  // a finding that "Fix everything" has fixed shows that result instead of a second fix
  const f = S.result.flaws.find((x) => x.id === button.dataset.fix);
  if (f) button.hidden = !S.fix.jobs.has(f.id) && !!fixAllItem(f);
  button.disabled = !!S.fix.busy;
  if (S.fix.busy) button.title = busyText(); else button.removeAttribute("title");
}

/** The outcome of finding f in a finished "Fix everything" job of the open result, or null. */
function fixAllItem(f) {
  const all = S.fix.jobs.get("all");
  return all?.state === "done" ? all.fix.fixes.find((x) => x.finding === f.id) || null : null;
}

/** The session cache key of a result's fixes: the finished fixes of an example stay when the user opens it again. */
const fixKey = (source) => source ? `${source.kind}:${source.id}` : "";

/** Starts the fix job of key (a finding id or "all") once per result; its entry holds the state, the summary and the player. */
function startFix(key, body) {
  const known = S.fix.jobs.get(key);
  if (known && known.state !== "error") return known;
  const source = fixSource(), rid = S.rid, entry = { state: "running", stage: FIX_STAGES[0], fix: null, audio: null, error: null, player: null };
  if (!source || S.fix.busy) return null;
  S.fix.jobs.set(key, entry);
  S.fix.busy = { key, source: fixKey(source) };
  const url = source.kind === "job" ? `api/jobs/${source.id}/fix` : `api/gallery/${encodeURIComponent(source.id)}/fix`;
  entry.done = (async () => {
    try {
      const res = await request(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const made = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(failText(res.status, made.detail));
      for (;;) {
        const poll = await request(`api/jobs/${made.job_id}`), job = await poll.json().catch(() => ({}));
        if (!poll.ok) throw new Error(failText(poll.status, job.detail));
        if (job.state === "error") throw new Error(job.error);
        if (job.state === "done") { Object.assign(entry, { state: "done", fix: job.fix, audio: job.audio }); break; }
        if (job.stage !== entry.stage || (job.stage_labels && !entry.labels)) { entry.stage = job.stage; entry.labels = job.stage_labels; refreshFix(); }
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

/** "Hear it fixed": select the finding, fix it on the server, then loop the fixed region. The page stays where the user
 *  is: a top card shows the progress itself and then a link to the result in the finding panel. */
async function hearFixed(i) {
  if (S.sel !== i || S.selKind !== "flaw") select(i);
  const f = S.result.flaws[i], entry = startFix(f.id, { finding: storedIndex(f) });
  if (!entry || !(await entry.done) || selected()?.id !== f.id) return;
  const fx = entry.fix.fixes.find((x) => x.finding === f.id);
  if (fx) say(`${findingText(f)}: ${outcomeHead(fx)}.`);
  entry.player?.play("fixed");
}

/** Scroll to the fix result of finding id in the finding panel and move the keyboard focus to it. */
function showFixResult(id) {
  const i = S.result.flaws.findIndex((f) => f.id === id);
  if (i < 0) return;
  if (S.sel !== i || S.selKind !== "flaw") select(i, { announce: false });
  const box = document.querySelector(`#explain .fixer[data-fixer="${CSS.escape(id)}"]`);
  if (!box) return;
  box.tabIndex = -1;
  box.scrollIntoView({ block: "nearest", behavior: reducedMotion() ? "auto" : "smooth" });
  box.focus({ preventScroll: true });
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
  if (!entry) return;
  // the button is disabled while the job runs, so the focus moves to the progress beside it
  if (entry.state === "running") $("#fix-all-status").focus({ preventScroll: true });
  if (!(await entry.done)) return;
  // the button hides itself, so the focus moves to the result, which also scrolls into view
  const body = $("#fix-all-body");
  body.tabIndex = -1;
  body.scrollIntoView({ block: "nearest", behavior: reducedMotion() ? "auto" : "smooth" });
  body.focus({ preventScroll: true });
  const fix = entry.fix;
  say(fix.score_change != null ? `Every fix applied: score ${num(fix.score_before, 2)} before, ${num(fix.score_after, 2)} after. ${fixAllLine(fix)}` : `Every fix applied. ${fixAllLine(fix)}`);
  entry.player?.play("fixed");
}

/** Redraws what the fix state changes: the buttons, the top cards' status, the selected finding's fix and the whole-reading panel. */
function refreshFix() {
  document.querySelectorAll("[data-fix]").forEach(showFixWait);
  document.querySelectorAll("[data-card-status]").forEach(cardStatus);
  const f = selected(), box = document.querySelector("#explain .fixer");
  if (box && f && S.selKind === "flaw" && box.dataset.fixer === f.id) box.replaceWith(fixerView(f));
  renderFixAll();
}

/** The fix of a top card's finding at the card itself: progress while it runs, then its outcome and a link to the result. */
function cardStatus(box) {
  const id = box.dataset.cardStatus, entry = S.fix.jobs.get(id), fromAll = entry ? null : fixAllItem(S.result.flaws.find((f) => f.id === id));
  box.hidden = !entry && !fromAll;
  if (box.hidden) return box.replaceChildren();
  if (entry?.state === "running") return box.replaceChildren(progressLine(entry, false));
  if (entry?.state === "error") return box.replaceChildren(el("p", { class: "fix-error", text: entry.error }));
  const fx = fromAll || entry.fix.fixes.find((x) => x.finding === id);
  box.replaceChildren(el("p", { class: "fix-head", text: fx ? outcomeHead(fx) : "Finished" }),
    el("button", { type: "button", class: "text-btn", onclick: () => showFixResult(id) }, "See result"));
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
    setPlaying();
    const current = () => token === this.token;
    try {
      if (media.readyState < 1) await new Promise((resolve, reject) => { media.addEventListener("loadedmetadata", resolve, { once: true }); media.addEventListener("error", reject, { once: true }); });
      if (!current()) return;
      media.currentTime = at == null ? a : Math.min(Math.max(track.fromCommon(at), a), b);
      await media.play();
      if (current()) setPlaying();   // the level meter needs the element that now plays
    } catch {
      if (current()) { this.playing = false; this.onchange(); setPlaying(); }
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
    setPlaying();
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
  show();
  const root = el("div", { class: "abc" }, el("div", { class: "ab-toggle", role: "group", "aria-label": "Listen to" }, ...buttons), play,
    note ? el("p", { class: "note", text: note }) : null);
  // One player can show in two places (an edit of "Fix everything" in its list and in the finding panel); a redraw drops
  // the controls that left the page.
  player.views = (player.views || []).filter((view) => view.root.isConnected).concat({ root, show });
  player.onchange = () => player.views.forEach((view) => view.show());
  return root;
}

/** The heading of one fix (app.fix_entry outcomes). It never says "Fixed" alone: a spot can stop being flagged with only part of the change. */
function outcomeHead(x) {
  // a spot covered by another finding's edit states that edit's share in its reason (app.fix_entry)
  const share = x.share != null && x.share < 1 && x.covered_by == null;
  if (x.outcome === "no_longer_flagged") return share ? `No longer flagged · ${Math.round(x.share * 100)}% of the change applied` : "No longer flagged";
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

const changeText = (v) => `${v < 0 ? "−" : "+"}${Math.abs(v).toFixed(2)}`;

/** The score change when the job states one (reference mode, reproduced); graded on its own, the flagged spots before and after. */
function scoreLine(done) {
  if (done.score_change != null) return el("p", { class: "fix-score" }, "Score change ", el("b", { text: changeText(done.score_change) }), " points");
  if (done.mode === "self" && done.flags_after != null) return el("p", { class: "fix-score" }, "Spots that stand out ", el("b", { text: String(done.flags_before) }), " → ", el("b", { text: String(done.flags_after) }));
  return done.score_change_note ? el("p", { class: "note", text: done.score_change_note }) : null;
}

/** One fix job of a finding (own pitch or the reference's melody) in plain words, with its three-way player. A fix that
 *  made no edit ("Not edited", "Can't be fixed") shows its reason only: the checks and the caution are about an edit. */
function fixResult(f, entry, key) {
  const parts = [];
  if (entry.state !== "done") return [entry.state === "running" ? progressLine(entry) : el("p", { class: "fix-error", role: "alert", text: entry.error })];
  const done = entry.fix, fx = done.fixes.find((x) => x.finding === f.id) || { outcome: "unfixable", reason: "" };
  parts.push(el("p", { class: "fix-head", text: outcomeHead(fx) }));
  if (outcomeReason(fx)) parts.push(el("p", { class: "fix-reason", text: outcomeReason(fx) }));
  if (playable(fx)) {
    parts.push(scoreLine(done));
    if (done.caution) parts.push(el("p", { class: "fix-caution", text: done.caution }));
    if (fx.limit) parts.push(el("p", { class: "note", text: fx.limit }));
    parts.push(...fixNotes(done));
  }
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
    showFixWait(button);
    parts.push(el("div", { class: "melody" }, button,
      el("p", { class: "note", text: "Changes your intonation pattern on these words to the reference's, instead of widening your own." })));
  }
  return parts.filter(Boolean);
}

/** The fix of one finding, and below it the fix with the reference's melody once asked for. */
function fixerView(f) {
  const entry = fixSource() ? S.fix.jobs.get(f.id) : null;
  if (!entry && fixSource() && fixAllItem(f)) return fixAllView(f);
  if (!entry && fixSource() && S.fix.busy) return el("div", { class: "fixer is-waiting", "data-fixer": f.id }, el("p", { class: "note", text: busyText() }));
  if (!entry) return el("div", { class: "fixer", "data-fixer": f.id, hidden: "" });
  const box = el("div", { class: "fixer", "data-fixer": f.id }, ...fixResult(f, entry, f.id));
  const fx = entry.state === "done" ? entry.fix.fixes.find((x) => x.finding === f.id) : null;
  box.classList.add(`is-${fx?.outcome || entry.state}`);
  const melody = S.fix.jobs.get(melodyKey(f));
  if (melody) box.append(el("div", { class: "fixer-melody" }, el("p", { class: "fix-sub", text: "With the reference's melody" }), ...fixResult(f, melody, melodyKey(f))));
  if (fixAllItem(f)) box.append(el("div", { class: "fixer-all" }, ...fixAllParts(f)));
  return box;
}

/** Finding f as "Fix everything" edited it, in the panel of a finding without a fix of its own. */
function fixAllView(f) {
  return el("div", { class: `fixer is-${fixAllItem(f).outcome}`, "data-fixer": f.id }, ...fixAllParts(f));
}

/** The outcome of finding f in "Fix everything" and, for an edit, its own loop (the same player as in "What each fix did"). */
function fixAllParts(f) {
  const x = fixAllItem(f);
  return [el("p", { class: "fix-sub", text: "From “Fix everything”" }), el("p", { class: "fix-head", text: outcomeHead(x) }),
    outcomeReason(x) ? el("p", { class: "fix-reason", text: outcomeReason(x) }) : null, playable(x) ? editControls(S.fix.jobs.get("all"), f) : null].filter(Boolean);
}

/** One edit of the whole-reading fix as its own loop (yours or edited, with a second of context), kept across redraws. */
function editControls(entry, f) {
  const pair = entry.fix.listen.find((p) => p.finding === f.id);
  if (!pair) return null;
  entry.edits = entry.edits || new Map();
  if (!entry.edits.has(f.id)) entry.edits.set(f.id, new LoopPlayer({ yours: regionTrack(S.base + S.result.participant.audio, pair.original_context),
    fixed: regionTrack(entry.audio, pair.edited_context) }, true, () => {}));
  return playerControls(entry.edits.get(f.id), LISTEN_SIDES.slice(0, 2), null);
}

// live: false where the same progress also shows in the finding panel, so a screen reader hears it once
function progressLine(entry, live = true) {
  return el("p", { class: "fix-progress", ...(live ? { role: "status" } : {}) }, el("span", { class: "spin", "aria-hidden": "true" }),
    entry.labels?.[entry.stage] ? `${entry.labels[entry.stage]}…` : FIX_STAGE_TEXT[entry.stage] || FIX_STAGE_TEXT.edit);
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
  showFixWait($("#fix-all-btn"));
  // the reason shows in words too: a disabled button gets no hover in every browser
  const ownRun = S.fix.busy?.key === "all" && S.fix.busy.source === fixKey(S.fix.source);   // its progress shows in #fix-all-status instead
  $("#fix-wait").textContent = ownRun ? "" : busyText();
  $("#fix-wait").hidden = !$("#fix-wait").textContent || $("#fix-all-btn").hidden;
  body.replaceChildren();
  // progress and errors show beside the button, where the user pressed it; the result shows below
  const status = $("#fix-all-status");
  status.hidden = !entry || entry.state === "done";
  status.replaceChildren(...(status.hidden ? [] : [entry.state === "running" ? progressLine(entry) : el("p", { class: "fix-error", role: "alert", text: entry.error })]));
  if (entry?.state !== "done") return;
  const fix = entry.fix;
  if (!entry.player) {
    const map = editMap(fix.listen, r.participant.duration, fix.duration);
    entry.player = new LoopPlayer({ yours: { url: S.base + r.participant.audio, span: [0, r.participant.duration], toCommon: (t) => t, fromCommon: (t) => t },
      fixed: { url: entry.audio, span: [0, fix.duration], toCommon: (t) => interp(t, map.ys, map.xs), fromCommon: (t) => interp(t, map.xs, map.ys) } }, false, () => {});
  }
  const items = r.flaws.map((f, i) => [f, i, fix.fixes.find((x) => x.finding === f.id)]).filter(([, , x]) => x);
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
        el("button", { type: "button", class: "plain", onclick: () => showFixResult(f.id), text: findingName(f, i) }),
        el("span", { text: [outcomeHead(x), outcomeReason(x)].filter(Boolean).join(". ") }),
        playable(x) ? editControls(entry, f) : null))))].filter(Boolean));
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
  S.raw = r;
  S.rawIds = r.flaws.map((f) => f.id);   // a fix request names a finding by its index in the stored result
  // Temporal numbers are stable even when the highest-impact whole-passage finding leads the list.
  r = { ...r, flaws: [...r.flaws].sort((a, b) => (a.p?.[0] ?? 0) - (b.p?.[0] ?? 0)) };
  S.base = base;
  S.fix.source = source;
  const key = fixKey(source);
  if (!S.fix.cache.has(key)) S.fix.cache.set(key, new Map());
  S.fix.jobs = S.fix.cache.get(key);
  S.fix.player = null;
  S.result = r; S.sel = null; S.selKind = "flaw"; S.filter = null; S.chart = null; S.rid += 1;
  S.allDimensions = false;
  S.pattern = null;
  S.priority = r.flaws.length ? r.flaws.reduce((best, f, i) => (f.points_lost ?? 0) > (r.flaws[best].points_lost ?? 0) ? i : best, 0) : null;
  $("#all-dimensions").setAttribute("aria-pressed", "false");
  $("#all-dimensions").textContent = "Show all measures";
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
  select(first, { kind, reveal: false, announce: false });
  drawChart();
  if (focused) {
    const btn = document.querySelector(`.side button[data-i="${first}"][data-kind="${kind}"][aria-pressed="true"]`);
    revealInSide(btn, btn?.closest("#listed-wrap")?.querySelector("summary") || btn?.closest(".side")?.querySelector(".side-head"));
  }
}

// ---------------------------------------------------------------------------------------------------- gallery
const NETWORK_TEXT = "The server could not be reached. Check that it is still running and that you are online, then try again.";

/** fetch, with a network failure (a TypeError such as "Failed to fetch") turned into a plain message. */
async function request(url, options) {
  try {
    return await fetch(url, options);
  } catch {
    throw new Error(NETWORK_TEXT);
  }
}

async function getJSON(url) {
  const res = await request(url);
  if (!res.ok) throw new Error(`The file was not found or the server failed (HTTP ${res.status}).`);
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

/** Fades the page content out and in around a content change; reduced motion swaps at once. The fade always ends, also
 *  when the change throws. */
async function crossFade(change) {
  const main = document.querySelector("main");
  if (reducedMotion() || !S.result) { change(); return; }
  main.classList.add("fading");
  try {
    await new Promise((resolve) => setTimeout(resolve, 140));
    S.tickOn = true;
    change();
  } finally {
    requestAnimationFrame(() => main.classList.remove("fading"));
  }
}

/** Draws a result; if drawing fails, the result shown before is drawn again, so the page is never half of each. */
function show(r, base, focus, source, name) {
  const before = S.shown;
  try {
    render(r, base, focus, source);
    S.shown = { r: S.raw, base, focus, source, name };
    showPicked(name);
    return true;
  } catch (e) {
    console.error(e);
    if (before) {
      try { render(before.r, before.base, before.focus, before.source); showPicked(before.name); } catch (again) { console.error(again); }
    }
    return false;
  }
}

async function openExample(it) {
  $("#picker-menu").open = false;
  const opening = ++S.openId;
  invalidateMedia();
  let r;
  try {
    r = await getJSON("gallery/" + it.result);
  } catch (e) {
    if (opening === S.openId) loadFailed(`The example could not be loaded. ${e.message}`);
    return;
  }
  if (opening !== S.openId) return;
  showAlert("");
  let shown = false;
  await crossFade(() => { shown = show(r, "gallery/", it.focus, { kind: "gallery", id: it.id }, exampleName(it)); });
  if (!shown) { loadFailed("The example could not be shown. The page shows the example that was open before."); return; }
  document.querySelectorAll(".chip").forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.id === it.id)));
}

/** After a failed load the media of the page shown is loaded again, so its player works. */
function loadFailed(text) {
  showAlert(text);
  if (S.shown) loadMedia(S.shown.r, S.shown.base);
  else clockStatus("Audio unavailable");
}

// Reference modes in plain words.
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

const STATIC_NOTE = "Uploads need the local server. Run `python -m cvoice.app` and open http://127.0.0.1:7860 (see the README); this static copy only shows the bundled examples.";
const TRANSCRIPT_MAX = 20000;   // characters; app.TRANSCRIPT_MAX_CHARS
// Stage names when neither the job nor /api/health gives its stage_labels (app.STAGE_LABELS).
const STAGE_TEXT = { decode: "Reading the audio", align: "Finding each word", features: "Measuring the delivery", compare: "Comparing", detect: "Finding the spots to work on" };

/** The footer link to the technical report: the app's or the static site's own copy when there is one (relative URL). */
function setReportLink(url) {
  if (url) $("#report-link").href = url;
}

/** Without the server only the examples work: the upload form stays, disabled and explained, and nothing points to it. */
function staticMode() {
  disableUpload(STATIC_NOTE);
  $("#jump-upload").hidden = true;
  $("#limits-line").hidden = true;
}

/** The transcript as UTF-8 text, or an error in plain words: the server reads the transcript as UTF-8. */
async function readTranscript(file) {
  const bytes = await file.arrayBuffer();
  try {
    return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  } catch {
    throw new Error("The transcript file is not UTF-8 text. Save it as UTF-8 (plain text), or paste the words into the box.");
  }
}

function checkLength() {
  const over = $("#f-text").value.length - TRANSCRIPT_MAX;
  $("#text-warn").hidden = over <= 0;
  $("#text-warn").textContent = over > 0 ? `The transcript is ${over} characters over the limit of ${TRANSCRIPT_MAX}. Shorten it before you analyse.` : "";
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
  $("#f-text").addEventListener("input", () => { $("#f-text").dataset.edited = "1"; checkLength(); });
  $("#f-text-file").addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    showStageError("");
    try {
      $("#f-text").value = await readTranscript(file);
      $("#f-text").dataset.edited = "1";
      checkLength();
    } catch (error) {
      e.target.value = "";
      showStageError(error.message);
    }
  });
  prefill();
  $("#form").addEventListener("submit", submitUpload);
  // The static site's index says so, and the page sends no request that must fail. An older static copy without that
  // field serves a fixed file at api/health ({"static": true}); on the app server its own route answers first.
  if (index.static_mode) { setReportLink(index.report_url); return staticMode(); }
  let health;
  try {
    const res = await fetch("api/health");
    if (!res.ok) throw new Error(String(res.status));
    health = await res.json();
  } catch {
    health = { static: true };
  }
  if (health.static) return staticMode();
  setReportLink(health.report_url);
  S.stageLabels = health.stage_labels || null;
  S.limits = health.limits;
  S.flagLimits = health.flag_limits || {};
  S.fix.info = health.fix || null;
  sel.querySelector(`option[value="${NO_REFERENCE}"]`).disabled = health.self?.available === false;
  if (S.result) { renderSummary(S.result); renderFixAll(); if (selected()) renderExplain(); }   // an example opened before the server answered gains its fix buttons
  if (S.result) renderLimit(S.result);   // an example that loaded before the server answered gains its five-reading line
  const mb = (bytes) => Math.round(bytes / 2 ** 20);
  $("#limits-line").hidden = false;
  $("#limits").textContent = `${mb(health.limits.max_bytes)} MB per file` + (health.limits.max_total_bytes ? `, ${mb(health.limits.max_total_bytes)} MB in all` : "")
    + `, ${health.limits.max_seconds} s of audio per recording`;
  if (!health.analysis.available) disableUpload(health.analysis.reason);
}

/** The analysis stages in plain words: the stages before `now` are done, `now` runs, or it is where the analysis stopped. */
function showStages(stages, now, failed = false, labels = S.stageLabels) {
  const ol = $("#stages");
  ol.hidden = false;
  S.upload = { stages, now, labels };
  const at = stages.indexOf(now);
  ol.replaceChildren(...stages.map((stage, i) => {
    const state = i < at || now === "done" ? "done" : i === at ? (failed ? "failed" : "now") : "";
    return el("li", { class: state, ...(state === "now" ? { "aria-current": "step" } : {}) }, labels?.[stage] || STAGE_TEXT[stage] || stage,
      state === "failed" ? el("span", { class: "stage-fail", text: " (stopped here)" }) : null);
  }));
}

function failText(status, detail) {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return "The form is incomplete: choose your recording and enter the transcript.";
  if (status === 429) return "Another analysis or fix is running. Try again when it has finished.";
  return `The request failed (HTTP ${status}).`;
}

async function submitUpload(ev) {
  ev.preventDefault();
  showStageError("");
  $("#stages").hidden = true;   // the stages show once the server has taken the job
  S.upload = null;
  const audio = $("#f-audio").files[0], own = $("#f-baseline").value === "", none = $("#f-baseline").value === NO_REFERENCE;
  const ownFiles = own ? [...$("#f-baseline-audio").files] : [];
  if (!audio) return fail("Choose your recording.");
  if (own && !ownFiles.length) return fail("Choose your reference recordings, or pick a bundled one.");
  if (ownFiles.length > (S.limits?.max_references || 5)) return fail("Choose at most five reference recordings.");
  if (!$("#f-text").value.trim()) return fail(none ? "Enter the transcript: the exact words you read." : "Enter the transcript: the exact words both recordings read.");
  if ($("#f-text").value.length > TRANSCRIPT_MAX) return fail(`The transcript is longer than ${TRANSCRIPT_MAX} characters. Shorten it before you analyse.`);
  const files = [audio, ...ownFiles];
  // the same file names as the server's refusals (app.upload_label)
  const fileName = (k) => (k === 0 ? "Your recording" : ownFiles.length === 1 ? "Your reference recording" : `Your reference recording ${k}`);
  const large = S.limits ? files.findIndex((f) => f.size > S.limits.max_bytes) : -1;
  if (large >= 0) return fail(`${fileName(large)} is larger than ${Math.round(S.limits.max_bytes / 2 ** 20)} MB.`);
  if (S.limits?.max_total_bytes && files.reduce((sum, f) => sum + f.size, 0) > S.limits.max_total_bytes) return fail(`The files together are larger than ${Math.round(S.limits.max_total_bytes / 2 ** 20)} MB.`);
  const fd = new FormData();
  fd.append("audio", audio);
  fd.append("transcript", $("#f-text").value);
  if (own) for (const f of ownFiles) fd.append("baseline_audio", f);
  else if (!none) fd.append("baseline_id", $("#f-baseline").value);
  $("#submit").disabled = true;
  document.body.classList.add("busy");
  try {
    const res = await request("api/analyze", { method: "POST", body: fd });
    const body = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(failText(res.status, body.detail));
    showStages(["decode", "align", "features", "compare", "detect"], "decode");
    await poll(body.job_id);
  } catch (e) {
    if (S.upload) showStages(S.upload.stages, S.upload.now, true, S.upload.labels);
    fail(e.message);
    // the disabled Analyse button lost the focus during the request
    $("#stage-msg").tabIndex = -1;
    $("#stage-msg").focus();
  } finally {
    $("#submit").disabled = false;
    document.body.classList.remove("busy");
  }
}

function fail(text) {
  showStageError(text);
}

function showStageError(text) {
  const msg = $("#stage-msg");
  msg.className = text ? "err" : "note";
  msg.textContent = text;
}

async function poll(id) {
  for (;;) {
    const res = await request(`api/jobs/${id}`);
    const job = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(failText(res.status, job.detail));
    showStages(job.stages, job.stage, job.state === "error", job.stage_labels || S.stageLabels);   // on an error, stage is the failed one
    if (job.state === "error") throw new Error(job.error);
    if (job.state === "done") {
      const r = await getJSON(job.result);
      S.openId += 1;
      if (!show(r, "", null, { kind: "job", id }, "Your analysis")) throw new Error("The result could not be shown.");
      document.querySelectorAll(".chip").forEach((c) => c.setAttribute("aria-pressed", "false"));
      $("#ledger").scrollIntoView({ block: "start" });
      return;
    }
    await new Promise((resolve) => setTimeout(resolve, POLL_MS));
  }
}

// ---------------------------------------------------------------------------------------------------- start
const SEEK_STEP_S = 5;    // s per arrow key on the progress groove
const SEEK_PAGE_S = 15;   // s per Page Up or Page Down key

/** The slider's keys: Space plays and pauses (as on the page), the arrows and Page Up/Down seek, Home and End go to the ends. */
function grooveKeys(e) {
  if (e.key === " ") {
    e.preventDefault();
    togglePlay();
    return;
  }
  const length = S.side === "you" ? S.ws?.getDuration() : S.ref.duration, at = S.side === "you" ? S.ws?.getCurrentTime() : S.ref.currentTime;
  if (!(length > 0)) return;
  const to = { ArrowRight: at + SEEK_STEP_S, ArrowUp: at + SEEK_STEP_S, ArrowLeft: at - SEEK_STEP_S, ArrowDown: at - SEEK_STEP_S,
    PageUp: at + SEEK_PAGE_S, PageDown: at - SEEK_PAGE_S, Home: 0, End: length }[e.key];
  if (to == null) return;
  e.preventDefault();
  seekShare(to / length);
}

/** A press on the slider seeks there, and the position follows the pointer until it is released. */
function grooveDrag(groove) {
  const seekTo = (e) => { const box = groove.getBoundingClientRect(); seekShare((e.clientX - box.left) / box.width); };
  groove.addEventListener("pointerdown", (e) => {
    if (e.button !== 0) return;
    groove.setPointerCapture(e.pointerId);
    groove.focus({ preventScroll: true });
    seekTo(e);
  });
  groove.addEventListener("pointermove", (e) => { if (groove.hasPointerCapture(e.pointerId)) seekTo(e); });
}

/** Space plays or pauses, unless the focus is on a control that uses Space itself. */
function spaceToPlay(e) {
  if (e.key !== " " || e.ctrlKey || e.metaKey || e.altKey || e.defaultPrevented) return;
  if (e.target.closest?.("input, textarea, select, button, a, summary, [contenteditable], [role='slider']")) return;
  e.preventDefault();
  togglePlay();
}

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
  grooveDrag($("#player-progress"));
  $("#player-progress").addEventListener("keydown", grooveKeys);
  document.addEventListener("keydown", spaceToPlay);
  $("#transcript").addEventListener("keydown", wordKeys);
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
    $("#all-dimensions").textContent = S.allDimensions ? "Show relevant measures" : "Show all measures";
    drawChart();
  });
  let resizeTimer = 0;
  addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      if (S.tl && $("#tl-host").clientWidth !== S.tl.width) drawTimeline();
      if (S.chart && $("#chart-host").clientWidth !== S.chart.width) drawChart();
      if (S.horizon && $(".horizon").clientWidth !== S.horizon.width) drawRanges();
      if (S.sea && $("#cloud-sea").clientWidth !== S.sea.width) startSea();
    }, 150);
  });
  // a hidden tab stops the sea's frame loop; it starts again when the tab shows
  document.addEventListener("visibilitychange", () => { if (!document.hidden && S.sea) startSea(); });
  document.fonts?.ready.then(() => {
    if (S.result) drawTimeline();
    if (S.horizon) drawRanges();   // the serif changes where the hero text ends, which bounds the ranges under it
  });
  await ensureLibs();
  S.hasLibs = typeof Plotly !== "undefined" && typeof WaveSurfer === "function" && !!WaveSurfer.Timeline;
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
