"use strict";
/* Contrastive Voice dashboard. One render path: render(result, base) draws a gallery result and an upload result alike.
   Text from results is user data: it is only ever inserted with textContent. */

// ---------------------------------------------------------------------------------------------------- constants
const PLOT_L = 64, PLOT_R = 16;          // px; the wavesurfer strip uses the same insets (style.css .wave)
const DISPLAY_HOP_S = 0.02;              // s; frame rows are thinned to this hop before drawing
const MIN_PLAY_S = 0.6;                  // s; a flaw's span is padded to this length for A/B playback
const BAND_ALPHA = 0.16, BAND_ALPHA_SEL = 0.20;   // flag wash; the recording line keeps >= 3:1 on it up to 0.20
const ROW_GAP_PX = 24;                   // room for each row's heading
const HATCH_STEP_PX = 7;                 // px between the hatch lines of a sub-word span
const GROUP_PAD_PX = 4;                  // px between a group outline and its members' washes
const LABEL_PAD_PX = 3, LABEL_CHAR_PX = 7;   // a wash number's padding and its width per character at 11 px
const LABEL_GAP_PX = 4, LABEL_SHIFT_PX = 6;  // px between two wash numbers; px a number may move right past a wash narrower than that
const POLL_MS = 500;
const SEVERITY_STYLES = [[1 / 3, "dot", "dotted"], [2 / 3, "dash", "dashed"], [Infinity, "solid", "solid"]];

const LIBS = [  // [is it loaded?, fallback file]; the wavesurfer core must come before its plugins
  [() => typeof Plotly !== "undefined", "vendor/plotly-cartesian.min.js"],
  [() => typeof WaveSurfer === "function", "vendor/wavesurfer.min.js"],
  [() => typeof WaveSurfer === "function" && WaveSurfer.Regions, "vendor/regions.min.js"],
  [() => typeof WaveSurfer === "function" && WaveSurfer.Timeline, "vendor/timeline.min.js"],
];
const ROWS = {  // heading (wide, narrow), dimension, kind of drawing
  pitch: { t: "Pitch, semitones from each speaker's median", s: "Pitch (st)", h: 120, frame: true },
  energy: { t: "Level, dB from each speaker's median voiced level", s: "Level (dB)", h: 100, frame: true },
  pace: { t: "Pace: ln ratio of speech time, below 0 is faster", s: "Pace (ln)", h: 84, dim: "D1" },
  pauses: { t: "Pauses: length difference, below 0 is shorter", s: "Pauses (s)", h: 76, dim: "D2", bars: true },
  pitch_range: { t: "Pitch range: ln ratio at your overall range, below 0 is flatter", s: "Pitch range (ln)", h: 84, dim: "D3" },
  stress: { t: "Stress points: words that carry stress", s: "Stress", h: 52 },
  emphasis: { t: "Emphasis: stress-point difference at the reference's stress words", s: "Emphasis", h: 76, dim: "D4", bars: true },
  volume: { t: "Volume: level difference, below 0 is quieter", s: "Volume (dB)", h: 84, dim: "D5" },
  clarity: { t: "Clarity (spectral-change proxy): ln ratio of spectral change", s: "Clarity proxy (ln)", h: 84, dim: "D6" },
  speech_tempo: { t: "Speech tempo: ln ratio of aligned word time (pauses not included), below 0 is faster", s: "Speech tempo (ln)", h: 84, dim: "D9" },
  word_time: { t: "Word time: ln ratio at your overall tempo", s: "Word time (ln)", h: 90, dim: "D7", markers: true },
  ending: { t: "Ending: final pitch-change difference", s: "Ending (st)", h: 90, dim: "D8", markers: true },
};
const ROW_OF_DIM = { D1: "pace", D2: "pauses", D3: "pitch_range", D4: "emphasis", D5: "volume", D6: "clarity", D7: "word_time", D8: "ending", D9: "speech_tempo" };
const ALSO_ROW = { D3: "pitch", D5: "energy", D8: "pitch" };   // the contour row a delta row summarises
const UNIT = { ln: "ln ratio", s: "s", p: "p-units", dB: "dB", st: "st", count: "", words: "words" };
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
const TRUTH_TEXT = { MISPLACED_EMPHASIS: "Misplaced emphasis", REPEATED_CONTOUR: "Repeated pitch contour" };
const CANDIDATE_TEXT = "Automatic label; low precision on real speech; listen to the span.";
const SYNTHETIC_TEXT = "Synthetic-only family; unvalidated on real speech.";   // explain.SYNTHETIC_ONLY_CLAUSE
const OWN_EVIDENCE = { D9: "word_time_ln" };   // the evidence row that holds the finding's own measured difference

// ---------------------------------------------------------------------------------------------------- helpers
const $ = (s) => document.querySelector(s);
const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const rgba = (hex, a) => `rgba(${parseInt(hex.slice(1, 3), 16)},${parseInt(hex.slice(3, 5), 16)},${parseInt(hex.slice(5, 7), 16)},${a})`;
const num = (v, d) => (v == null ? "-" : v.toFixed(d));
const signed = (v, d = 2) => (v == null ? "-" : (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v).toFixed(d));
const span = (s) => !s ? "whole passage" : s[0].toFixed(2) === s[1].toFixed(2) ? `at ${s[0].toFixed(2)} s` : `${s[0].toFixed(2)}–${s[1].toFixed(2)} s`;
const sevStyle = (v) => SEVERITY_STYLES.find((x) => v < x[0]) || SEVERITY_STYLES[2];
const wholePassage = (f) => f.context === "whole passage" || f.words == null;
const onSpan = (f, p) => !wholePassage(f) && f.p[1] >= p[0] && f.p[0] <= p[1];   // a local finding overlaps the span p (s)
// Beside a whole-clip tempo finding a local pace flag is relative to the speaker's own overall tempo, not a second tempo verdict.
const typeText = (f) => f.dimension === "D1" && (f.type === "RUSH" || f.type === "DRAG") && S.result.flaws.some((x) => x.type.startsWith("TEMPO"))
  ? (f.type === "RUSH" ? "Faster than the rest of your reading" : "Slower than the rest of your reading") : TYPE_TEXT[f.type] || f.type;
const valUnit = (f) => f.value_unit === "x" ? "×" : f.value_unit ?? (f.words == null ? "×" : VALUE_UNIT[f.dimension] || "");
const withUnit = (v, unit) => v == null ? "-" : unit === "×" ? `×${num(v, 2)}` : `${num(v, 2)} ${unit}`.trim();
const factor = (v) => `×${Math.exp(v).toFixed(2)}`;   // an ln ratio as a plain factor
// Points are rounded to 2 decimals, so a stored 0.00 is a loss below 0.005, not a zero.
const ptsText = (v) => v == null ? "" : v < 0.005 ? "<0.01 pts" : `−${num(v, 2)} pts`;
// A counted finding can lose 0 points while its dimension still costs points (explain.dimension_loss). The dimension's loss is
// shown once: on the finding of that dimension that carries points, else on this finding as the dimension's total.
const zeroLoss = (f) => f.counted !== false && (f.points_lost ?? 0) < 0.005 && (f.dimension_points_lost ?? 0) >= 0.005;
const lossCarrier = (f) => S.result.flaws.findIndex((x) => x !== f && x.dimension === f.dimension && x.counted !== false && (x.points_lost ?? 0) >= 0.005);
const saturated = (f) => zeroLoss(f) && lossCarrier(f) < 0;
const dimText = (f) => S.result.scores.dims.find((d) => d.key === f.dimension)?.label || f.dimension;
const findingPts = (f) => saturated(f) ? `${dimText(f)} −${num(f.dimension_points_lost, 2)} pts in total`
  : zeroLoss(f) ? `<0.01 pts (${dimText(f)} loss on #${lossCarrier(f) + 1})` : ptsText(f.points_lost);
const synthetic = (f) => (f.text || "").toLowerCase().includes(SYNTHETIC_TEXT.toLowerCase());
// Scores and multiples are shown at their stored 2 decimals: a second rounding makes them disagree with points_lost and the text.
const scoreText = (v) => v == null ? "n/a" : num(v, 2);
const multipleText = (v) => v == null ? "-" : `×${num(v, 2)}`;
const displayText = (t) => (t || "").replace(/overall if fixed/gi, "score with this penalty removed");
const patternText = (p) => PATTERN_TEXT[p] || TYPE_TEXT[p] || p || "No pattern label";
// The pattern has its own chip (patternTags), so the title names the measured departure.
const findingText = (f) => f.type ? typeText(f) : f.label || f.brief_word || f.dimension;
const unevenTempo = (f) => f.pattern === "UNEVEN_TEMPO" || f.type === "UNEVEN_TEMPO";
// ln values carry 2 decimals (contract §1), so exp() can miss the factor that the text states from the unrounded value by 0.01.
const statedFactor = (f, pattern, v) => { const m = (f.text || "").match(pattern); return m ? `×${m[1]}` : factor(v); };
const spreadFactor = (f) => statedFactor(f, /typical factor of x(\d+(?:\.\d+)?)/, f.participant);
const thresholdFactor = (f) => statedFactor(f, /flagged above x(\d+(?:\.\d+)?)/, f.threshold);

function resultDefaults(r) {
  if (r.schema >= 2) return r;
  return { ...r, detection: { listed_keys: [], listed_clip_keys: [] },
    rows: r.rows.map((row) => ({ ...row, status: row.tol?.some((v) => v != null) ? "scored" : "displayed" })),
    flaws: r.flaws.map((f) => ({ pattern: null, evidence: [], group: null, group_pattern: null, counted: true, candidate: false,
      span_kind: wholePassage(f) ? null : f.dimension === "D2" ? "boundary" : "word", ...f })),
    differences: (r.differences || []).map((f) => ({ status: "difference", context: f.words == null ? "whole passage" : "",
      pattern: null, span_kind: null, evidence: [], candidate: false, ...f })) };
}

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
const S = { result: null, base: "", sel: null, filter: null, rid: 0, index: null, ws: null, regions: null, ref: new Audio(),
  refTimer: null, chart: null, hasLibs: false, selKind: "flaw", allDimensions: false, openId: 0,
  mediaId: 0, youReady: false, refReady: false, playId: 0, priority: null, pattern: null, evaluation: null };

function differences() { return S.result.regime === "R2" && Array.isArray(S.result.differences) ? S.result.differences : []; }
function selected() { return (S.selKind === "difference" ? differences() : S.result.flaws)[S.sel]; }
function mediaSpan(f, who) { return f[who === "you" ? "p" : "b"] || [0, S.result[who === "you" ? "participant" : "baseline"].duration]; }
/** Badge and sentence for the result's reference mode, or null when the result does not state one (older results). */
function referenceMode(r) {
  const d = r.detection || {};
  if (!d.reference_mode) return null;
  const spare = d.references_available > d.reference_count ? ` of ${d.references_available} available` : "";
  if (d.reference_mode === "consensus5") {
    return { badge: `Reference: median of ${d.reference_count} readings${spare}`,
      text: `Consensus mode: word and window features are the median of ${d.reference_count} reference readings${spare}; the audio, waveform and reference word times are the first reading.` };
  }
  return { badge: "Reference: one reading",
    text: d.references_available > 1 ? `Single-reference mode: ${d.references_available} readings were given, fewer than consensus mode needs.` : "Single-reference mode: one reference reading." };
}

function noRegions(r) {
  return r.regime === "R2" ? "No region exceeds the calibrated threshold for a different speaker. The threshold is wide because two competent readers differ a lot; see the largest differences below."
    : "No region exceeds its tolerance.";
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

/** The "How flags are decided" text. A note without a threshold statement (the pipeline writes one only in R2) gets the local
    thresholds of the result's rows, the values that the chart headings state. */
function detectionNote(r) {
  const note = typeof r.scores.detection_note === "string" ? r.scores.detection_note.trim() : "";
  if (/Flag thresholds/.test(note)) return note;
  const label = (row) => r.scores.dims.find((d) => d.key === ROWS[row.key]?.dim)?.label || row.key;
  const local = r.rows.filter((row) => ROWS[row.key]?.dim && thresholdText(row)).map((row) => `${label(row)} ${thresholdText(row)}`);
  return [note, local.length ? `Local flag thresholds for reference departures: ${local.join("; ")}.` : ""].filter(Boolean).join(" ");
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

function renderLedger(r) {
  const o = r.scores.overall;
  $("#overall-fig").textContent = scoreText(o);
  const note = detectionNote(r);
  $("#detection-note p").textContent = note;
  $("#detection-note").hidden = !note;
  $("#regime").textContent = r.regime === "R1" ? "Regime R1: the same performance as the reference."
    : "Regime R2: a different performance from the reference.";
  const mode = referenceMode(r);
  $("#reference-mode").hidden = !mode;
  $("#reference-mode .badge").textContent = mode ? mode.badge : "";
  $("#reference-mode .badge").title = mode ? mode.text : "";
  $("#key-ref").textContent = r.detection?.reference_mode === "consensus5" ? `Reference: median of ${r.detection.reference_count} readings` : "Reference rendition";
  const cards = $("#cards");
  cards.replaceChildren();
  for (const g of dimGroups(r)) {
    const scored = g.dims.filter((d) => d.scored);
    const value = scored.length ? scored.reduce((a, d) => a + d.score, 0) / scored.length : null;
    const keys = g.dims.map((d) => d.key);
    const n = r.flaws.filter((f) => keys.includes(f.dimension)).length;
    const reason = value == null ? g.dims.find((d) => d.note)?.note : null;
    const card = el("button", { type: "button", class: "card", "aria-pressed": "false", "data-dims": keys.join(",") },
      el("div", { class: "word", text: keys.includes("D6") ? "Clarity (spectral-change proxy)" : g.word }),
      el("div", { class: value == null ? "fig unscored" : "fig", text: value == null ? `Not scored (${r.regime})` : num(value, 1) }),
      reason ? el("div", { class: "reason", text: reason[0].toUpperCase() + reason.slice(1) + "." }) : null,
      el("div", { class: "bar" }, el("i", { style: `width:${value == null ? 0 : Math.max(0, Math.min(100, value))}%` })),
      ...g.dims.map((d) => el("div", { class: "line", title: `${d.note || ""} Coverage: ${num(d.coverage * 100, 0)}%.` },
        el("span", { text: d.key === "D6" ? "Spectral change" : d.label }), el("span", { text: d.scored ? num(d.score, 1) : "not scored" }))),
      el("div", { class: "count", text: n ? `${n} flagged ${n === 1 ? "region" : "regions"}` : "No flagged regions" }));
    card.addEventListener("click", () => setFilter(S.filter && S.filter.join() === keys.join() ? null : keys));
    cards.append(card);
  }
}

function renderFix() {
  const f = selected();
  $("#overall-fix").textContent = S.selKind === "flaw" && f && f.overall_if_fixed != null ? `Score with this penalty removed: ${scoreText(f.overall_if_fixed)}` : "";
}

function renderFilters(r) {
  const dimension = $("#dimension-filter"), pattern = $("#pattern-filter");
  dimension.replaceChildren(el("option", { value: "", text: "All dimensions" }));
  for (const g of dimGroups(r)) {
    if (g.dims.length > 1) dimension.append(el("option", { value: g.dims.map((d) => d.key).join(","), text: g.word }));
    dimension.append(...g.dims.map((d) => el("option", { value: d.key, text: `${d.key} · ${d.label}` })));
  }
  const patterns = new Set([...r.flaws, ...differences()].flatMap((f) => [f.pattern, f.group_pattern]).filter(Boolean));
  pattern.replaceChildren(el("option", { value: "", text: "All patterns" }),
    ...[...patterns].sort().map((p) => el("option", { value: p, text: patternText(p) })),
    el("option", { value: "unlabelled", text: "No pattern label" }));
  pattern.closest("label").hidden = r.schema < 2;
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

function patternTags(f) {
  if (S.result.schema < 2) return document.createDocumentFragment();
  const p = f.pattern || "unlabelled";
  const repeats = !!f.pattern && patternText(f.pattern) === findingText(f);   // e.g. uneven word timing: type and pattern share one name
  return el("div", { class: "finding-tags" },
    repeats ? null : el("button", { type: "button", class: "pattern-chip", "data-pattern": p, "aria-pressed": String(S.pattern === p),
      "aria-label": `Filter by pattern: ${patternText(f.pattern)}`, onclick: () => setPattern(S.pattern === p ? null : p), text: patternText(f.pattern) }),
    f.candidate ? el("span", { class: "candidate", title: CANDIDATE_TEXT, text: "Candidate" }) : null,
    synthetic(f) ? el("span", { class: "candidate", title: SYNTHETIC_TEXT, text: "Synthetic only" }) : null);
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
        "data-kind": "flaw", onclick: () => select(i) },
        el("span", { class: "n", text: `#${i + 1}` }), el("span", { class: "t", text: findingText(f) }),
        el("span", { class: "pts", text: f.counted === false ? "shared" : findingPts(f) }),
        el("span", { class: "m" }, el("span", { text: `${f.brief_word}, ${wholePassage(f) ? "whole passage" : span(f.p)}` }),
          el("i", { class: `dash ${st[2]}`, "aria-label": `Severity: ${st[2]}` }))), patternTags(f));
  };
  const groupItem = (members) => {
    if (members.length === 1) return item(members[0]);
    const [f, i] = counted(members);
    return el("li", { class: "finding-group" },
      el("button", { type: "button", class: "group-select", "data-i": i, "data-kind": "flaw",
        "aria-pressed": String(S.selKind === "flaw" && members.some(([, j]) => S.sel === j)), onclick: () => select(i) },
        el("span", { class: "t", text: patternText(f.group_pattern) }), el("span", { class: "pts", text: findingPts(f) }),
        el("span", { class: "m", text: `${members.length} members · one shared penalty` })),
      el("ul", { class: "flaws group-members" }, ...members.map(item)));
  };
  const minor = (members) => !saturated(counted(members)[0]) && (counted(members)[0].points_lost ?? 1) < 0.05;
  list.append(...shown.filter((members) => !minor(members)).map(groupItem));
  const folded = shown.filter(minor);
  if (folded.length) list.append(el("li", {}, el("details", {}, el("summary", { text: `Minor departures (${folded.length}), under 0.05 points` }),
    el("ul", { class: "flaws" }, ...folded.map(groupItem)))));
}

function renderDifferenceList() {
  const items = differences(), detection = S.result.detection;
  $("#differences-wrap").hidden = S.result.regime !== "R2";
  $("#listed-wrap").hidden = !items.some((f) => f.status === "listed");
  $("#listed-count").textContent = `(${items.filter((f) => f.status === "listed" && matchesFilter(f)).length})`;
  const dimLabel = (key) => S.result.scores.dims.find((d) => d.key === key.replace(/[+-]$/, ""))?.label || key;
  $("#listed-note").textContent = [...detection.listed_keys.map((k) => `${dimLabel(k)} (${k})`),
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
      el("span", { class: "note", text: kind === "flaw" ? `Whole clip · ${findingPts(f)}` : f.status === "listed" ? "Listed, not scored · whole clip" : "Difference, not scored · whole clip" }),
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
const referenceText = (f) => f.dimension === "D7" ? "reference at this recording's tempo" : "reference";

function diffLine(f) {
  if (unevenTempo(f)) return `Whole passage: typical word-to-word factor ${spreadFactor(f)}${f.status === "listed" ? "; listed, not scored" : ""}.`;
  const vu = valUnit(f), v = (x) => withUnit(x, vu);
  // A ratio value already states the factor, so the ln difference is not repeated as a second factor.
  const by = f.delta == null || vu === "×" || REGULARISED.has(f.dimension) ? "" : f.unit === "ln" ? ` (${factor(f.delta)} the reference)`
    : ` (${signed(f.delta)} ${UNIT[f.unit] || f.unit || ""})`;
  const status = f.status === "listed" ? "not flagged for a different performance" : "flags start well above 1";
  const values = wholeRatio(f) || `${referenceText(f)} ${v(f.baseline)}, this recording ${v(f.participant)}${by}`;
  return `${wholePassage(f) ? "Whole passage" : span(f.p)}: ${values}${f.multiple == null ? "" : `. ${multipleText(f.multiple)} the tolerance scale (${status})`}`;
}

function fact(dl, term, value) {
  dl.append(el("dt", { text: term }), el("dd", { text: value }));
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
  box.classList.toggle("neutral", diff);
  if (!f) {
    box.append(el("h3", { text: "Listen and compare" }),
      el("p", { class: "empty", text: r.flaws.length ? "Select a region to read the explanation." : noRegions(r) }));
    return;
  }
  const words = wholePassage(f) ? "whole passage" : r.words.slice(f.words[0], f.words[1] + 1).map((w) => w.w).join(" ");
  const vu = valUnit(f), dunit = UNIT[f.unit] || f.unit || "";
  const ratio = f.unit !== "ln" || f.delta == null ? "" : REGULARISED.has(f.dimension) && valUnit(f) !== "×"
    ? ` (${factor(f.delta)} after the same small constant is added to both values)` : ` (${factor(f.delta)})`;
  const dl = el("dl", { class: "facts" });
  if (unevenTempo(f)) {
    fact(dl, "Typical word-to-word factor", spreadFactor(f));
    fact(dl, "Robust spread", `${num(f.participant, 2)} ln`);
  } else {
    const whole = wholeRatio(f);
    if (whole) fact(dl, "This recording", whole);
    else {
      fact(dl, referenceText(f)[0].toUpperCase() + referenceText(f).slice(1), withUnit(f.baseline, vu));
      fact(dl, "This recording", withUnit(f.participant, vu));
    }
    fact(dl, "Difference", `${signed(f.delta)} ${dunit}${ratio}`);
  }
  if (diff) {
    if (f.multiple != null) fact(dl, "Multiple of the tolerance scale", multipleText(f.multiple));
  } else {
    fact(dl, "Points lost", f.points_lost == null ? "-" : f.points_lost < 0.005 ? "<0.01" : num(f.points_lost, 2));
    if (saturated(f)) fact(dl, `${dimText(f)}, points lost in total`, num(f.dimension_points_lost, 2));
    else if (zeroLoss(f)) fact(dl, `${dimText(f)} loss carried by`, `#${lossCarrier(f) + 1} (${ptsText(r.flaws[lossCarrier(f)].points_lost)})`);
    fact(dl, "Score with this penalty removed", f.overall_if_fixed == null ? "-" : scoreText(f.overall_if_fixed));
    fact(dl, "Multiple of the flag threshold", multipleText(f.tolerance_multiple));
    fact(dl, "Flagged beyond", f.threshold == null ? "-" : unevenTempo(f) ? thresholdFactor(f) : `${f.delta < 0 ? "−" : "+"}${num(f.threshold, 2)} ${dunit}`);
  }
  box.append(
    el("p", { class: "eyebrow", text: diff ? f.status === "listed" ? "Listed, not scored · no point penalty" : "Reference difference · not scored" : "Selected finding · listen, then try the fix" }),
    el("h3", { text: diff ? findingText(f) : `#${S.sel + 1} ${findingText(f)}` }), patternTags(f),
    el("p", { class: "spans", text: `Words: ${wholePassage(f) ? words : `‘${words}’`}` }),
    el("p", { class: "spans", text: `This recording: ${span(f.p)} · Reference: ${span(f.b)}` }),
    el("div", { class: "ab-row" },
      el("button", { type: "button", class: "ab", "data-audio": "you", onclick: () => playSpan("you", mediaSpan(f, "you")) }, el("b", { text: "A" }), "This recording"),
      el("button", { type: "button", class: "ab", "data-audio": "ref", onclick: () => playSpan("ref", mediaSpan(f, "ref")) }, el("b", { text: "B" }), "Reference")),
    el("p", { class: "what", text: displayText(f.candidate ? f.text.replace(CANDIDATE_TEXT, "").trim() : f.text)
      .replace(/Unclear articulation/gi, "Reduced spectral change (spectral-change proxy)") }));
  if (f.candidate) box.append(el("p", { class: "candidate-note", text: CANDIDATE_TEXT }));
  if (f.group) {
    const members = r.flaws.filter((x) => f.group.includes(x.id));
    box.append(el("p", { class: "group-note", text: `${patternText(f.group_pattern)} group · ${members.length} members · one shared penalty. ${f.counted === false ? "This member adds no points lost; the counted member carries the group's penalty." : "The score with this penalty removed removes the whole group's penalty."}` }),
      el("div", { class: "group-links" }, ...members.map((member) => el("button", { type: "button", class: "plain",
        onclick: () => select(r.flaws.indexOf(member)), text: `#${r.flaws.indexOf(member) + 1} ${findingText(member)}` }))));
  }
  if (!diff && f.fix) box.append(el("p", { class: "fix" }, el("b", { text: "To fix: " }), f.fix));
  const detail = el("details", { class: "measure-details" }, el("summary", { text: "Measurements and context" }), dl);
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
    if (f.overall_if_fixed != null) detail.append(el("p", { class: "measure", text: "The score above removes this penalty arithmetically; it does not predict the score of a new recording." }));
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
  document.querySelectorAll("button[data-kind]").forEach((b) =>
    b.setAttribute("aria-pressed", String(+b.dataset.i === i && b.dataset.kind === kind ||
      kind === "flaw" && b.classList.contains("group-select") && selected()?.group?.includes(S.result.flaws[+b.dataset.i].id))));
  const selector = `button[data-i="${i}"][data-kind="${kind}"]`;
  const btn = document.querySelector(kind === "difference" ? `#differences ${selector}, #listed ${selector}` : `#flaws ${selector}`);
  if (btn?.closest("details")) btn.closest("details").open = true;
  if (reveal) revealInSide(btn);
  if (scroll) btn?.scrollIntoView({ block: "nearest" });
  renderExplain();
  renderFix();
  markWords();
  if (S.chart && before !== rowDefs(S.result).map((d) => d.key).join()) drawChart();
  else highlight();
  updateWaveRegions();
  const f = selected();
  if (S.youReady && f) S.ws.setTime(mediaSpan(f, "you")[0]);
}

// ---------------------------------------------------------------------------------------------------- transcript
function renderTranscript(r) {
  const box = $("#transcript");
  box.replaceChildren();
  const wordStyle = new Array(r.words.length).fill(null);
  r.flaws.forEach((f) => {
    if (wholePassage(f)) return;   // clip-level: no word run to underline
    const st = sevStyle(f.severity ?? 0);
    for (let i = f.words[0]; i <= f.words[1]; i++) if (!wordStyle[i] || SEVERITY_STYLES.indexOf(st) > SEVERITY_STYLES.indexOf(wordStyle[i])) wordStyle[i] = st;
  });
  r.words.forEach((w, i) => {
    const b = el("button", { type: "button", class: "w" + (wordStyle[i] ? ` f-${wordStyle[i][1]}` : ""), "data-i": i, text: w.w });
    b.dataset.audio = "you";
    b.addEventListener("click", () => playSpan("you", [w.p[0], w.p[1] + 0.25]));
    box.append(b, " ");
  });
  $("#truth-matches").replaceChildren(...truthEdits(r).map(renderTruthEdit));
}

/** Injected edits with their matched findings and listed differences. A gallery truth carries the evaluator's match
    (`finding`, `difference`); an older result without it falls back to the same type and an overlapping span. Truths of one
    labelled edit (the boundaries of a word-by-word edit) form one entry. */
function truthEdits(r) {
  const edits = [];
  for (const t of r.schema >= 2 ? r.truth || [] : []) {
    const flaws = "finding" in t ? [r.flaws.findIndex((f) => f.id === t.finding)].filter((i) => i >= 0)
      : r.flaws.map((f, i) => [f, i]).filter(([f]) => [f.type, f.pattern, f.group_pattern].includes(t.type) &&
        f.dimension === t.dimension && onSpan(f, t.p)).map(([, i]) => i);
    const diff = t.difference == null ? -1 : differences().findIndex((d) => d.id === t.difference);
    const shared = (t.duplicate_findings || []).map((id) => r.flaws.findIndex((f) => f.id === id)).filter((i) => i >= 0);
    const unit = { flaws, diff, sameChange: !!t.same_change, shared };
    const last = edits[edits.length - 1];
    const same = last && t.words && last.t.type === t.type && last.t.words?.join() === t.words.join();
    if (same) last.units.push(unit);
    else edits.push({ t, units: [unit] });
  }
  return edits;
}

/** The truth's detector_status (pipeline.detector_status); older truths without it get it from the result's detection lists. */
function truthStatus(t) {
  if (t.detector_status) return t.detector_status;
  const det = S.result.detection;
  if (!det.enabled || det.enabled.includes(t.dimension)) return "enabled";   // schema 1 has no enabled list: every dimension flags
  const listed = det.listed_keys.some((k) => k.replace(/[+-]$/, "") === t.dimension) || det.listed_clip_keys.includes(t.dimension);
  return listed ? "unscored" : "no detector";
}

/** Why an edit of this dimension cannot have a flag in this result, or null when it can. */
function noFlagReason(t) {
  const status = truthStatus(t), label = S.result.scores.dims.find((d) => d.key === t.dimension)?.label || t.dimension;
  if (status === "enabled") return null;
  if (status === "no detector") return `No detector for this edit: ${label} is displayed only in regime ${S.result.regime}`;
  const noEntry = differences().some((d) => d.status === "listed") ? "; no listed entry matches it" : "";
  return `No flag possible: ${label} is listed, not scored, in regime ${S.result.regime}${noEntry}`;
}

/** The expected detection of a level-1 edit, from the evaluation summary when the gallery has one (gallery.level_one_text). */
const levelOneText = () => " " + (S.evaluation?.texts?.level_one || "Level 1 is the smallest edit size.");

function renderTruthEdit({ t, units }) {
  const name = TYPE_TEXT[t.type] || PATTERN_TEXT[t.type] || TRUTH_TEXT[t.type] || t.type;
  const found = [...new Set(units.flatMap((u) => u.flaws))].sort((a, b) => a - b);
  const listed = [...new Set(units.filter((u) => !u.flaws.length && u.diff >= 0).map((u) => u.diff))];
  const missed = units.filter((u) => !u.flaws.length && u.diff < 0).length;
  const shared = [...new Set(units.flatMap((u) => u.shared))].filter((i) => !found.includes(i)).sort((a, b) => a - b);
  const findingButton = (i) => el("button", { type: "button", class: "plain", onclick: () => select(i, { scroll: true }), text: `Finding #${i + 1}` });
  const findingButtons = (list) => list.flatMap((i, k) => k ? [", ", findingButton(i)] : [findingButton(i)]);
  // An excluded edit failed the label checks, so the evaluation neither matches nor counts it; a flag on it is not a false flag.
  const missText = t.excluded ? `Excluded from evaluation (${t.excluded.join("; ")})` : noFlagReason(t) ||
    (units.length > 1 ? `${missed} of ${units.length} boundaries without a matching flag` : "No matching flag");
  // An excluded edit's findings come from the evaluation's own rule (gallery on_edit: events.on_shortfall); the span test is only a hint.
  const near = t.excluded && t.on_edit ? t.on_edit.map((id) => S.result.flaws.findIndex((f) => f.id === id)).filter((i) => i >= 0 && !found.includes(i))
    : S.result.flaws.map((f, i) => [f, i]).filter(([f, i]) => onSpan(f, t.p) && !found.includes(i) && !shared.includes(i) &&
      (t.excluded || f.dimension === t.dimension)).map(([, i]) => i);
  const nearText = !missed || !near.length ? null : t.excluded ? " Flags on this excluded edit (not counted as false): "
    : noFlagReason(t) ? null : " Partly covered by ";
  return el("span", { class: "truth-edit" }, el("span", { class: "note", text: `Injected ${name}: ` }),
    ...findingButtons(found),
    units.some((u) => u.sameChange && u.flaws.length) ? el("span", { class: "note", text: " (found by a region of the same change)" }) : null,
    ...(shared.length ? [el("span", { class: "note", text: " Same change, not counted again: " }),
      ...findingButtons(shared)] : []),
    ...listed.map((i) => el("button", { type: "button", class: "plain", onclick: () => select(i, { scroll: true, kind: "difference" }),
      text: `${differences()[i].status === "listed" ? "Listed entry" : "Difference"} (not scored)` })),
    missed ? el("span", { class: "note", text: missText + (t.level === 1 && !t.excluded && !noFlagReason(t) ? "." + levelOneText() : "") }) : null,
    ...(nearText ? [el("span", { class: "note", text: nearText }), ...findingButtons(near),
      t.excluded ? null : el("span", { class: "note", text: " (overlap below the match rule: time IoU 0.5)" })] : []));
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

function markPlaying(tp) {
  const ws = S.result.words;
  if (!ws.length) return;
  let lo = 0, hi = ws.length - 1;
  while (lo < hi) { const m = (lo + hi + 1) >> 1; if (ws[m].p[0] <= tp) lo = m; else hi = m - 1; }
  document.querySelectorAll("#transcript .w").forEach((b) => b.removeAttribute("aria-current"));
  const b = document.querySelector(`#transcript .w[data-i="${lo}"]`);
  if (b && tp >= ws[lo].p[0] && tp <= ws[lo].p[1] + 0.2) b.setAttribute("aria-current", "true");
}

// ---------------------------------------------------------------------------------------------------- chart
function rowDefs(r) {
  const defs = [], dims = new Set(r.flaws.map((f) => f.dimension));
  const f = selected();
  if (f) dims.add(f.dimension);
  for (const x of [...differences(), ...(r.truth || [])]) dims.add(x.dimension);   // a listed difference or injected edit earns its row
  for (const row of r.rows) {
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
    ref: css("--ref"), you: css("--you"), flag: css("--flag"), neutral: css("--neutral") };
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
    const yaxis = { domain: [lo, hi], fixedrange: true, gridcolor: c.rule, linecolor: c.rule, zeroline: false, nticks: 4,
      tickfont: { color: c.ink2, size: 11 }, automargin: false };
    const unit = UNIT[row.unit] || row.unit;
    let head = narrow ? spec.s : spec.t;
    if (spec.frame) {
      const times = (a) => a.map((_, i) => i * r.hop).filter((_, i) => i % stride === 0);
      const thin = (a) => a.filter((_, i) => i % stride === 0);
      const x = times(row.p);
      for (const [name, vals, color] of [["Reference", row.b, c.ref], ["This recording", row.p, c.you]]) {
        traces.push({ type: "scatter", mode: "lines", name: `${name}, ${spec.s.split(" (")[0].toLowerCase()}`, x, y: thin(vals), yaxis: ax, connectgaps: false,
          line: { color, width: 1.6, dash: name === "Reference" ? "dash" : "solid" }, hovertemplate: `%{y:.1f} ${unit}<extra></extra>` });
      }
    } else if (d.key === "stress") {
      const mid = (i) => (r.words[i].p[0] + r.words[i].p[1]) / 2;
      for (const [name, idx, y, color] of [["Reference stress", r.stress.b, 1, c.ref], ["This recording stress", r.stress.p, 0, c.you]]) {
        traces.push({ type: "scatter", mode: "markers", name, x: idx.map(mid), y: idx.map(() => y), yaxis: ax, customdata: idx.map((i) => r.words[i].w),
          marker: { symbol: "diamond", size: 10, color, line: { color: c.surface, width: 1.5 } }, hovertemplate: "%{customdata}<extra></extra>" });
      }
      Object.assign(yaxis, { range: [-0.8, 1.8], tickvals: [0, 1], ticktext: ["You", "Ref"] });
      head = narrow ? spec.s : `${spec.t}`;
    } else {
      const vals = row.p, finite = vals.filter((v) => v != null);
      const [below, above] = row.tol || [null, null];   // flag thresholds per direction, null where never flagged
      const m = Math.max(below || 0, above || 0, ...finite.map(Math.abs), 1e-6) * 1.2;
      Object.assign(yaxis, { range: [-m, m], zeroline: true, zerolinecolor: c.muted });
      const name = `${spec.s.split(" (")[0]} vs reference`;
      if (spec.markers) {
        const points = eventBars(r.words, vals, false);
        traces.push({ type: "scatter", mode: "markers", name, x: points.x, y: points.y, yaxis: ax, customdata: points.c,
          marker: { size: 9, color: c.you, line: { width: 1, color: c.ink } },
          hovertemplate: `%{y:+.2f} ${unit} (%{customdata})<extra></extra>` });
      } else if (spec.bars) {
        const b = eventBars(r.words, vals, d.key === "pauses");
        traces.push({ type: "bar", name, x: b.x, y: b.y, width: b.w, yaxis: ax, customdata: b.c, marker: { color: c.you },
          hovertemplate: `%{y:+.2f} ${unit} (%{customdata})<extra></extra>` });
      } else {
        const sgm = wordSegments(r.words, vals);
        traces.push({ type: "scatter", mode: "lines", name, x: sgm.x, y: sgm.y, yaxis: ax, customdata: sgm.c, connectgaps: false,
          line: { color: c.you, width: 3 }, hovertemplate: `%{y:+.2f} ${unit} (%{customdata})<extra></extra>` });
      }
      if (below != null || above != null) {
        shapes.push({ type: "rect", xref: "x domain", yref: ax, x0: 0, x1: 1, y0: below != null ? -below : -m, y1: above != null ? above : m,
          layer: "below", line: { width: 0 }, fillcolor: rgba(c.ink, 0.06) });
        head += narrow ? ` · flag ${thresholdText(row, true)}` : `. Flagged ${thresholdText(row)}`;
      } else {
        head += row.status === "listed" ? ". Listed, not scored" : row.status === "scored" ? ". Flag threshold unavailable" : ". Shown, not scored";
      }
    }
    layout[ax === "y" ? "yaxis" : `yaxis${k + 1}`] = yaxis;
    // The heading starts at the chart's left edge, over the tick labels, to leave the most width on a phone.
    annotations.push({ xref: "paper", yref: "paper", x: -PLOT_L / Math.max(width - PLOT_L - PLOT_R, 1), y: hi, xanchor: "left", yanchor: "bottom", yshift: 3, showarrow: false,
      text: head, font: { size: 11.5, color: c.ink2 } });
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
      yanchor: side, yshift: side === "top" ? -3 : 1, showarrow: false, text, font: { size: 11, color: c.ink }, bgcolor: rgba(c.surface, 0.85), borderpad: 1 };
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
        fillcolor: rgba(c.flag, BAND_ALPHA), line: { color: c.ink2, width: 1, dash: st[1] } };
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
  for (const t of r.truth || []) {   // injected truth (gallery clips): a thick rule on the row's top edge, dotted when excluded
    if (!rowAxis[ROW_OF_DIM[t.dimension]]) continue;
    shapes.push({ type: "line", xref: "x", yref: `${rowAxis[ROW_OF_DIM[t.dimension]]} domain`, x0: t.p[0], x1: t.p[1], y0: 1, y1: 1,
      line: { color: c.ink, width: 4, dash: t.excluded ? "dot" : "solid" }, layer: "above" });
  }
  layout.xaxis = { anchor: axisId(n - 1), range: [0, r.participant.duration], gridcolor: c.rule, linecolor: c.rule, zeroline: false,
    ticks: "outside", tickcolor: c.rule, tickfont: { color: c.ink2, size: 11 }, hoverformat: ".2f",
    title: { text: "Time in this recording (s)", font: { size: 11.5, color: c.ink2 }, standoff: 6 } };
  Object.assign(layout, { width, height: plotH + margin.t + margin.b, margin, paper_bgcolor: c.surface, plot_bgcolor: c.surface, showlegend: false,
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
  const c = S.chart.colors, upd = {};
  S.result.flaws.forEach((f, i) => {
    const on = S.selKind === "flaw" && (S.sel === i || selected()?.group?.includes(f.id));
    for (const k of S.chart.flawShapes[i]) {
      upd[`shapes[${k}].line.width`] = on ? 2.5 : 1;
      upd[`shapes[${k}].line.color`] = on ? c.ink : c.ink2;
      upd[`shapes[${k}].fillcolor`] = rgba(c.flag, on ? BAND_ALPHA_SEL : BAND_ALPHA);
    }
  });
  S.chart.groupShapes.forEach((g) => {
    const on = S.selKind === "flaw" && g.ids.includes(selected()?.id);
    for (const k of g.indices) {
      upd[`shapes[${k}].line.width`] = on ? 3 : 2;
      upd[`shapes[${k}].line.color`] = on ? c.ink : c.ink2;
    }
  });
  S.chart.differenceShapes.forEach((indices, i) => {
    const on = S.selKind === "difference" && S.sel === i;
    for (const k of indices) {
      upd[`shapes[${k}].line.width`] = on ? (S.chart.layout.shapes[k].type === "path" ? 1 : 2) : 0;
      if (S.chart.layout.shapes[k].type !== "path") upd[`shapes[${k}].fillcolor`] = rgba(c.neutral, on ? 0.18 : 0);
    }
  });
  if (Object.keys(upd).length) Plotly.relayout($("#chart"), upd);
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
function updatePlayback() {
  $("#play-all").disabled = !S.youReady;
  document.querySelectorAll("[data-audio]").forEach((b) => { b.disabled = !(b.dataset.audio === "you" ? S.youReady : S.refReady); });
}

function invalidateMedia() {
  stopAll();
  S.mediaId += 1;
  S.youReady = false; S.refReady = false;
  $("#play-all").textContent = "Play recording";
  $("#clock").textContent = "Loading audio…";
  $("#cursor").style.display = "none";
  updatePlayback();
}

function updateWaveRegions() {
  if (!S.youReady || !S.regions) return;
  S.regions.clearRegions();
  const add = (f, i, kind) => {
    const p = mediaSpan(f, "you"), duration = S.ws.getDuration();
    const reg = S.regions.addRegion({ start: Math.min(p[0], duration), end: Math.min(Math.max(p[1], p[0] + 0.05), duration), drag: false, resize: false,
      color: rgba(css(kind === "flaw" ? "--flag" : "--neutral"), 0.18), content: kind === "flaw" ? `#${i + 1}` : "Difference" });
    reg.findingIndex = i; reg.findingKind = kind;
  };
  S.result.flaws.forEach((f, i) => { if (!wholePassage(f)) add(f, i, "flaw"); });   // a whole-passage finding has no region to mark
  if (S.selKind === "difference" && selected() && !wholePassage(selected())) add(selected(), S.sel, "difference");
}

function loadMedia(r, base) {
  invalidateMedia();
  const token = S.mediaId;
  $("#wave-msg").textContent = "";
  const ref = S.ref = new Audio();
  const refCurrent = () => token === S.mediaId && S.ref === ref;
  ref.addEventListener("canplay", () => { if (refCurrent()) { S.refReady = true; updatePlayback(); } });
  ref.addEventListener("error", () => { if (refCurrent()) { S.refReady = false; updatePlayback(); $("#wave-msg").textContent = "The reference audio could not be loaded."; } });
  ref.preload = "auto";
  ref.src = base + r.baseline.audio;
  if (!S.hasLibs) { $("#clock").textContent = "Recording playback unavailable"; return; }
  if (S.ws) S.ws.destroy();
  const ws = S.ws = WaveSurfer.create({ container: "#wave", height: 64, normalize: true, cursorWidth: 2, waveColor: css("--you"),
    progressColor: css("--ink2"), cursorColor: css("--ink") });
  const current = () => token === S.mediaId && S.ws === ws;
  S.regions = ws.registerPlugin(WaveSurfer.Regions.create());
  ws.registerPlugin(WaveSurfer.Timeline.create({ height: 16 }));
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
    moveCursor(t); markPlaying(t);
  });
  ws.on("play", () => { if (current()) $("#play-all").textContent = "Pause"; });
  ws.on("pause", () => { if (current()) $("#play-all").textContent = "Play recording"; });
  const failed = (e) => {
    if (!current() || e?.name === "AbortError") return;
    S.youReady = false; updatePlayback();
    $("#clock").textContent = "Audio unavailable";
    $("#wave-msg").textContent = "The recording audio could not be loaded.";
  };
  ws.on("error", failed);
  ws.load(base + r.participant.audio).catch(failed);
}

function stopAll() {
  S.playId += 1;
  clearTimeout(S.refTimer);
  S.ref.pause();
  if (S.ws) S.ws.pause();
}

function padSpan([a, b]) {
  const need = MIN_PLAY_S - (b - a);
  return need > 0 ? [Math.max(0, a - need / 2), b + need / 2] : [a, b];
}

async function playSpan(who, s) {
  if (!(who === "you" ? S.youReady : S.refReady)) return;
  stopAll();
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
        moveCursor(tp); markPlaying(tp); requestAnimationFrame(tick);
      }
    };
    tick();
  } catch (e) {
    if (current()) $("#wave-msg").textContent = "The browser blocked playback: press the button again.";
  }
}

// ---------------------------------------------------------------------------------------------------- render
function renderNotices(r) {
  const ul = $("#notices");
  ul.replaceChildren(...r.notices.map((t) => el("li", { text: displayText(t) })));
  if (r.regime === "R2" && S.evaluation?.texts?.r2_lockbox) ul.append(el("li", { text: S.evaluation.texts.r2_lockbox }));
  ul.append(...r.scores.dims.filter((d) => d.note || d.coverage < 1).map((d) => el("li", {
    text: `${d.label}: ${d.note ? d.note + ". " : ""}Measurable coverage: ${num(d.coverage * 100, 0)}%.` })));
}

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

function render(r, base, focus = null) {
  stopAll();
  r = resultDefaults(r);
  // Temporal numbers are stable even when the highest-impact whole-passage finding leads the list.
  r = { ...r, flaws: [...r.flaws].sort((a, b) => (a.p?.[0] ?? 0) - (b.p?.[0] ?? 0)) };
  S.result = r; S.base = base; S.sel = null; S.selKind = "flaw"; S.filter = null; S.chart = null; S.rid += 1;
  S.allDimensions = false;
  S.pattern = null;
  S.priority = r.flaws.length ? r.flaws.reduce((best, f, i) => (f.points_lost ?? 0) > (r.flaws[best].points_lost ?? 0) ? i : best, 0) : null;
  $("#all-dimensions").setAttribute("aria-pressed", "false");
  $("#all-dimensions").textContent = "Show all dimensions";
  $("#clear-filter").hidden = true;
  $("#key-truth").hidden = !(r.truth && r.truth.length);
  $("#key-excluded").hidden = !(r.truth || []).some((t) => t.excluded);
  $("#key-group").hidden = !r.flaws.some((f) => f.group);
  $("#key-subword").hidden = ![...r.flaws, ...differences()].some((f) => f.span_kind === "sub-word");
  $("#listed-wrap").open = false;   // one panel element and one list column serve every example
  for (const box of [$(".side"), $("#flaws"), $("#differences"), $("#listed")]) box.scrollTop = 0;
  renderLedger(r);
  renderFilters(r);
  renderFlawList();
  renderDifferenceList();
  renderClipCards();
  renderTranscript(r);
  renderNotices(r);
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

function buildChips(index) {
  const chips = $("#chips");
  chips.replaceChildren();
  const groups = [];
  for (const it of index.items) {
    let g = groups.find((x) => x.name === it.group);
    if (!g) groups.push(g = { name: it.group, items: [] });
    g.items.push(it);
  }
  const oneReference = index.items.every((it) => !it.baseline || it.baseline === index.baseline.id);
  $("#picker-title").textContent = oneReference ? `Examples from ${index.baseline.title}` : "Examples";
  for (const g of groups) {
    chips.append(el("div", { class: "group" }, el("span", { class: "gname", text: g.name }),
      el("div", { class: "chips" }, ...g.items.map((it) => el("button", { type: "button", class: "chip", "aria-pressed": "false", "data-id": it.id,
        title: it.title, onclick: () => openExample(it) }, it.label, el("span", { class: "score", text: scoreText(it.overall) }))))));
  }
  const left = index.left_out || [];
  $("#left-out").hidden = !left.length;
  $("#left-out summary").textContent = `${left.length} planned ${left.length === 1 ? "example" : "examples"} left out with this detector`;
  $("#left-out-list").replaceChildren(...left.map((x) => el("li", { text: `${x.label}: ${x.reason}.` })));
}

async function openExample(it) {
  const request = ++S.openId;
  invalidateMedia();
  try {
    const r = await getJSON("gallery/" + it.result);
    if (request !== S.openId) return;
    document.querySelectorAll(".chip").forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.id === it.id)));
    $("#picker-note").textContent = `${it.title}. ${it.description}`;
    showAlert("");
    render(r, "gallery/", it.focus);
  } catch (e) {
    if (request === S.openId) { $("#clock").textContent = "Audio unavailable"; showAlert(`The example could not be loaded: ${e.message}`); }
  }
}

/** An uncertainty block of evaluate (uncertainty.cluster_summary): a 95% interval, or the value of each cluster (recording or
 * speaker) when there are too few clusters for an interval. An interval with equal bounds has no spread, so the pooled Wilson
 * interval (gallery.with_wilson) is shown instead. `scale` 100 shows a fraction as percent. */
function intervalText(iv, value, digits = 2, scale = 1) {
  if (value == null) return "-";
  const point = num(scale * value, digits), bound = (v) => num(scale * v, digits);
  if (Array.isArray(iv?.ci95) && iv.ci95[0] != null) {
    if (iv.ci95[0] === iv.ci95[1] && iv.wilson95) return `${point} (no spread across recordings; pooled Wilson 95% ${bound(iv.wilson95[0])} to ${bound(iv.wilson95[1])})`;
    return `${point} [${bound(iv.ci95[0])}, ${bound(iv.ci95[1])}]`;
  }
  if (iv?.per_cluster && iv.unit === "speaker") return `${point} (per speaker ${Object.values(iv.per_cluster).map((v) => v == null ? "-" : bound(v)).join(", ")}; no interval)`;
  if (Array.isArray(iv?.range) && iv.range[0] != null) return `${point} (range ${bound(iv.range[0])} to ${bound(iv.range[1])}, no interval)`;
  return point;
}

const foundCounts = (r) => r.flaws_found_before == null || r.flaws_found_after == null ? "-" : `${r.flaws_found_before} → ${r.flaws_found_after}`;

const keptText = (iv) => `${iv.retained} of ${iv.found}: ${intervalText(iv, iv.fraction, 0, 100)}`;

function retention(r) {
  const iv = r.retention_interval;
  if (!iv) return "-";
  return iv.found ? keptText(iv) : "none found before";
}

/** Per flag key: regions added per minute and detections kept, each with its interval. */
function byKey(r) {
  const keys = [...new Set([...Object.keys(r.added_by_key || {}), ...Object.keys(r.retention_by_key || {})])].sort();
  if (!keys.length) return "-";
  return keys.map((k) => {
    const added = r.added_by_key?.[k], kept = r.retention_by_key?.[k];
    const parts = [added ? `added ${intervalText(added, added.rate)}/min` : null, kept?.found ? `kept ${keptText(kept)} %` : null];
    return `${k}: ${parts.filter(Boolean).join("; ")}`;
  }).join(" · ");
}

function renderStress(rows) {
  const scopes = [...new Set(rows.map((r) => r.interval_scope).filter(Boolean))].map((t) =>
    `${[...new Set(rows.filter((r) => r.interval_scope === t).map((r) => r.split))].join(", ")}: ${t}`);
  const shares = [...new Set(rows.filter((r) => r.key_share_per_min != null).map((r) => `${r.regime} ${num(r.key_share_per_min, 3)}`))];
  const cols = [
    ["Population", (r) => r.split], ["Condition", (r) => r.condition], ["Regime", (r) => r.regime],
    ["Reference mode", (r) => r.reference_mode ?? "-"],
    ["Recordings", (r) => r.recordings ?? "-", "num"], ["Seeds", (r) => Array.isArray(r.seeds) ? r.seeds.join(", ") : "-"],
    ["Exposure, all seeds (min)", (r) => num(r.minutes, 1), "num"],
    ["Regions added per min", (r) => intervalText(r.added_interval, r.added_per_min), "num"],
    ["Regions removed per min", (r) => intervalText(r.removed_interval, r.removed_per_min), "num"],
    ["Largest score change (points)", (r) => num(r.max_abs_delta_score, 2) + (r.missing_score_pairs ? ` (${r.missing_score_pairs} pairs unmeasured)` : ""), "num"],
    ["Flaws found before → after", foundCounts, "num"],
    ["Detections kept (%)", retention, "num"],
    ["By flag key", byKey],
    ["Limits: what this condition breaks", (r) => r.limits?.length ? r.limits.join("; ") : "none"],
  ];
  const t = $("#stress-table");
  t.replaceChildren(el("thead", {}, el("tr", {}, ...cols.map(([h, , c]) => el("th", { text: h, class: c || "" })))),
    el("tbody", {}, ...rows.map((r) => el("tr", {}, ...cols.map(([, value, c]) => el("td", { text: String(value(r) ?? "-"), class: c || "" }))))));
  const broken = rows.filter((r) => r.limits?.length).length;
  const modes = new Set(rows.filter((r) => r.regime === "R2").map((r) => r.reference_mode));
  $("#stress-summary").textContent = [
    "Each row is the measured change under one recording condition; no pass rule applies.",
    rows.some((r) => "limits" in r) ? `${broken} of ${rows.length} rows break at least one flag key (column Limits).` : "Limits are not computed for this matrix.",
    shares.length ? `A key breaks when the 95% lower bound of its added local regions per minute (the rate where no interval exists) is above its share of the false-region budget (per minute: ${shares.join(", ")}), or when the 95% upper bound of its kept detections (the fraction where no interval exists) is below 95 %.` : "",
    modes.size && !modes.has("consensus5") ? "R2 rows use the single-reference mode; the consensus5 mode has no stress coverage." : "",
    scopes.length ? `Intervals (${scopes.join("; ")}).` : ""].filter(Boolean).join(" ");
  $("#stress").hidden = false;
  $("#jump-stress").hidden = false;
}

// ---------------------------------------------------------------------------------------------------- evaluation
const MODE_TEXT = { single: "one reference", consensus5: "median of five references" };
const METHOD_TEXT = { "detector (pre-registered)": "with the reference (the detector), pre-registered accounting: all predictions counted",
  detector: "with the reference (the detector), one detection per change", "reference_free (detector h)": "without a reference, at the detector's h",
  "reference_free (own scales and h)": "without a reference, own scales and h fitted on train (computed after the final evaluation)" };
const methodText = (m) => METHOD_TEXT[m] || m.replace(/^reference_free \(train-chosen h=([\d.]+)\)$/, "without a reference, at h $1 chosen on train");
const counts = (c) => [c.tp, c.fp, c.fn].map((v) => num(v, 0)).join(" / ");
const spread = (c) => c.f1_ci95?.[0] != null ? `95% interval ${num(c.f1_ci95[0], 3)} to ${num(c.f1_ci95[1], 3)}`
  : c.f1_range ? `per speaker ${num(c.f1_range[0], 3)} to ${num(c.f1_range[1], 3)}, no interval` : "";
const withSpread = (c) => spread(c) ? `${num(c.f1, 3)} (${spread(c)})` : num(c.f1, 3);

function evaluationTable(id, head, rows) {
  return el("div", { class: "scroll" }, el("table", { id },
    el("thead", {}, el("tr", {}, ...head.map((h) => el("th", { text: h })))),
    el("tbody", {}, ...rows.map((row) => el("tr", {}, ...row.map((v) => el("td", { text: v })))))));
}

/** The "How well it works" panel: the final run's measured numbers (gallery/evaluation.json, gallery.evaluation_summary). */
function renderEvaluation(ev) {
  const test = ev.r1.find((r) => r.split === "test");
  $("#evaluation > summary").textContent = `How well it works: test F1 ${num(test.preregistered.f1, 3)} (pre-registered accounting), ` +
    `${num(test.count_once.f1, 3)} (one detection per change)`;
  const r1 = ev.r1.map((r) => [r.split, String(r.speakers), counts(r.preregistered), withSpread(r.preregistered),
    `${counts(r.count_once)}; ${num(r.count_once.same_change_duplicates, 0)}`, withSpread(r.count_once)]);
  const first = ev.first_final;
  if (first) r1.push([`test, earlier final evaluation (detector ${first.config_sha256.slice(0, 12)})`, "-", counts(first), num(first.f1, 3), "-", "-"]);
  const lockbox = ev.lockbox.map((m) => [MODE_TEXT[m.mode] || m.mode, num(m.rate, 3), num(m.pooled_rate, 3), num(m.upper95, 3), num(m.budget, 2),
    m.budget_status, Object.entries(m.by_source).map(([k, v]) => `${k} ${num(v, 3)}`).join(", "), num(m.whole_clip_flags_per_clip, 3),
    `${num(m.comparison_minutes, 1)} min, ${m.comparisons} comparisons, ${m.readers} readers`]);
  $("#evaluation-body").replaceChildren(
    el("p", { class: "note" }, `${ev.scope}. `, el("a", { href: "#evaluation-limits", text: "Read the limits" }), "."),
    el("h3", { text: "Synthetic edits, same speaker (R1), levels 2 and 3" }),
    el("p", { class: "note", text: `Pre-registered accounting first: ${ev.accounting.preregistered}. Beside it: ${ev.accounting.count_once}.` }),
    evaluationTable("evaluation-r1", ["Split", "Speakers", "Pre-registered: TP / FP / FN", "F1", "One per change: TP / FP / FN; duplicates", "F1"], r1),
    el("h3", { text: "No edits (R1 identity and placebo clips)" }),
    evaluationTable("evaluation-null", ["Clips", "False flags", "Minutes", "95% upper bound per minute (rule of three)"],
      ev.r1_null.map((r) => [r.population, num(r.false_flags, 0), num(r.minutes, 2), num(r.rule_of_three, 2)])),
    el("h3", { text: "Without the reference reading (baseline)" }),
    el("p", { class: "note", text: "The detector is given first under the pre-registered accounting; every other row counts one detection per change, an accounting adopted after the plan." }),
    evaluationTable("evaluation-baseline", ["Split", "Method", "TP / FP / FN", "Same-change duplicates", "F1"],
      ev.reference_free.map((r) => [r.split, methodText(r.method), counts(r), r.same_change_duplicates == null ? "counted in FP" : num(r.same_change_duplicates, 0), num(r.f1, 3)])),
    ...(ev.reference_free_note ? [el("p", { class: "note", text: ev.reference_free_note })] : []),
    el("h3", { text: "Different speakers (R2): held-out lockbox readers, measured once" }),
    evaluationTable("evaluation-lockbox", ["Reference", "False regions per comparison-minute (source-weighted)", "Pooled", "Upper 95%", "Budget",
      "Budget status", "By source", "Whole-clip false flags per clip", "Exposure"], lockbox),
    ...ev.lockbox.map((m) => el("p", { class: "note", text: `${MODE_TEXT[m.mode] || m.mode}: ${m.budget_note}` })),
    el("h3", { id: "evaluation-limits", text: "Limits" }),
    el("ul", { class: "note" }, ...ev.limits.map((t) => el("li", { text: t }))),
    el("p", { class: "note", text: `Source: eval/results.json and models/final_evaluations.json of the final run (detector configuration ${ev.config_sha256.slice(0, 12)}). ` +
      "The pre-registered counts, their per-speaker values and the own-scales baseline are computed after the final evaluation from the saved " +
      "outputs (python -m cvoice.addendum, python -m cvoice.gallery evaluation)." }));
  if (ev.texts?.r2_lockbox) { $("#upload-lockbox").textContent = ev.texts.r2_lockbox; $("#upload-lockbox").hidden = false; }
  $("#evaluation").hidden = false;
  $("#jump-evaluation").hidden = false;
}

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
    note: refs.length >= k ? `Compared with the word-by-word median of the first ${k} of ${refs.length} LibriVox readings (public domain); you hear and see the first reading, by ${refs[0].reader}. Readers: ${refs.map((r) => r.reader).join(", ")}.`
      : `Compared with the first of ${refs.length} readings, by ${refs[0].reader}: consensus mode needs ${k}.` };
}

async function setupUpload(index) {
  const sel = $("#f-baseline");
  const bundled = index.baselines || [index.baseline];
  sel.replaceChildren(...bundled.map((b) => el("option", { value: b.id, text: baselineText(b).label })),
    el("option", { value: "", text: "Upload my own reference recording" }));
  const prefill = () => {
    const own = sel.value === "", b = bundled.find((x) => x.id === sel.value);
    $("#own-baseline").hidden = !own;
    $("#baseline-note").textContent = own ? "Compared with your one reference recording." : baselineText(b).note;
    if (!own && !$("#f-text").dataset.edited) $("#f-text").value = b.text || "";
  };
  sel.addEventListener("change", prefill);
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
  $("#limits").textContent = `${Math.round(health.limits.max_bytes / 2 ** 20)} MB per upload, ${health.limits.max_seconds} s of audio per recording`;
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
  const audio = $("#f-audio").files[0], own = $("#f-baseline").value === "", ownFile = $("#f-baseline-audio").files[0];
  if (!audio) return fail("Choose your recording.");
  if (own && !ownFile) return fail("Choose the reference recording, or pick the bundled one.");
  if (!$("#f-text").value.trim()) return fail("Enter the transcript: the exact words both recordings read.");
  if (S.limits && [audio, ownFile].some((f) => f && f.size > S.limits.max_bytes)) return fail(`A file is larger than ${Math.round(S.limits.max_bytes / 2 ** 20)} MB.`);
  const fd = new FormData();
  fd.append("audio", audio);
  fd.append("transcript", $("#f-text").value);
  if (own) fd.append("baseline_audio", ownFile); else fd.append("baseline_id", $("#f-baseline").value);
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
      const mode = referenceMode(r);
      $("#picker-note").textContent = `Your analysis (regime R2).${mode ? " " + mode.text : ""}`;
      render(r, "");
      $("#ledger").scrollIntoView({ block: "start" });
      return;
    }
    await new Promise((res2) => setTimeout(res2, POLL_MS));
  }
}

// ---------------------------------------------------------------------------------------------------- start
async function init() {
  $("#jump-upload").addEventListener("click", () => { $("#upload").open = true; });
  $("#clear-filter").addEventListener("click", () => { S.pattern = null; $("#pattern-filter").value = ""; setFilter(null); });
  $("#dimension-filter").addEventListener("change", (e) => setFilter(e.target.value ? e.target.value.split(",") : null));
  $("#pattern-filter").addEventListener("change", (e) => setPattern(e.target.value || null));
  $("#play-all").addEventListener("click", () => {
    if (!S.youReady) return;
    if (S.ws.isPlaying()) stopAll();
    else playSpan("you", [S.ws.getCurrentTime(), S.ws.getDuration()]);
  });
  $("#all-dimensions").addEventListener("click", () => {
    S.allDimensions = !S.allDimensions;
    $("#all-dimensions").setAttribute("aria-pressed", String(S.allDimensions));
    $("#all-dimensions").textContent = S.allDimensions ? "Show relevant dimensions" : "Show all dimensions";
    drawChart();
  });
  $("#jump-stress").addEventListener("click", () => { $("#stress").open = true; });
  $("#jump-evaluation").addEventListener("click", () => { $("#evaluation").open = true; });
  let resizeTimer = 0;
  addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => { if (S.chart && $("#chart-host").clientWidth !== S.chart.width) drawChart(); }, 150);
  });
  await ensureLibs();
  S.hasLibs = typeof Plotly !== "undefined" && typeof WaveSurfer === "function" && !!WaveSurfer.Regions && !!WaveSurfer.Timeline;
  if (!S.hasLibs) showAlert("The chart and audio libraries could not be loaded, so the chart and the waveform are unavailable. Scores, flagged regions and the transcript still work.");
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { if (S.ws) S.ws.setOptions({ waveColor: css("--you"), progressColor: css("--ink2"), cursorColor: css("--ink") }); drawChart(); });
  let index;
  try {
    index = S.index = await getJSON("gallery/index.json");
  } catch (e) {
    return showAlert(`The bundled examples could not be loaded (${e.message}).`);
  }
  buildChips(index);
  setupUpload(index);
  if (index.stress_matrix) getJSON("gallery/" + index.stress_matrix).then(renderStress).catch(() => {});
  if (index.evaluation) {
    try {
      S.evaluation = await getJSON("gallery/" + index.evaluation);
      renderEvaluation(S.evaluation);
    } catch (e) {
      showAlert(`The evaluation summary could not be loaded (${e.message}).`);
    }
  }
  await openExample(index.items.find((i) => i.id === index.default) || index.items[0]);
}

init();
