/* Records the live dashboard demo for the launch video, frame by frame, and makes the app audio clips of the demo scenes.

     node video/scripts/capture.cjs clips [PORT]            run the fix jobs, cut the clips, write the clip fields of narration.json
     node video/scripts/capture.cjs [PORT] [SCENE ...]      record the demo scenes (all of them without SCENE)
     node video/scripts/capture.cjs refit                   fit the camera keys again from video/out/capture_raw, without a new recording

   Needs the app on PORT (default 7871) and a Chromium headless shell (CHROME_PATH, else the one of ~/.cache/ms-playwright).

   Output: video/public/captures/<scene>.webm (30 fps VP9), video/public/clips/<scene>.wav (48 kHz mono, -20 LUFS) and the
   entries of video/src/data/captures.json. video/out/capture_raw/<scene>.json keeps the frame count, the camera targets,
   and "boxes": every visible text line and control, sampled every BOX_EVERY frames, for scripts/check-framing.cjs.

   Stop motion with virtual time: each output frame is one screenshot. Between two screenshots the page clock (timers,
   requestAnimationFrame, performance.now), the CSS animations and every playing media element advance by exactly one frame
   (1/30 s), so the page moves at its real speed in the video however long a screenshot takes. Media elements play muted at
   the lowest rate and their position follows the virtual clock; the live level that the page reads from Web Audio is
   computed from the same WAV files instead, so the clouds, the glow and the level meter move as with real playback.

   The page renders at deviceScaleFactor 1.6 on a 1400x750 CSS px viewport (2240x1200 capture px). A CSS zoom would change
   the hero: the page measures its text in zoomed px and writes them back as CSS px, so the cloud sea would hide behind the text. */
const { chromium } = require('playwright-core');
const { execFileSync, spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '../..');
const RAW = path.join(ROOT, 'video/out/capture_raw');
const OUT = path.join(ROOT, 'video/public/captures');
const CLIPS = path.join(ROOT, 'video/public/clips');
const NARRATION_FILE = path.join(ROOT, 'video/src/data/narration.json');
const CAPTURES_FILE = path.join(ROOT, 'video/src/data/captures.json');
const PACING_FILE = path.join(ROOT, 'video/src/data/pacing.json');
const AUDIO = path.join(ROOT, 'gallery/audio');
const CHROME = process.env.CHROME_PATH || path.join(os.homedir(), '.cache/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell');

const FPS = 30;
const VIEW = { width: 1400, height: 750 };   // CSS px
const SCALE = 1.6;                           // capture px per CSS px
const MEDIA = [VIEW.width * SCALE, VIEW.height * SCALE];
const BOX_EVERY = 4;
// The browser window of the video (timeline.ts CAPTURE_VIEW): a camera rect of this shape fills it.
const WINDOW_ASPECT = 1760 / 764;
// A box inside a camera rect keeps this many capture px from its edge (check-framing.cjs uses 4).
const FIT_INSET = 7;
// Output px per capture px at most: a closer view shows too little of the page around the words it frames.
const MAX_ZOOM = 1.6;
const CLIP_LUFS = -20;
const CLIP_RATE = 48000;

const EXAMPLE = 'L3A';
const REFERENCE_WAV = 'reagan_farewell_1989.wav';
// The upload scene's reading: another speaker's reading of the same passage, with two delivery edits.
const READING_WAV = 'greenman_edited.wav';
// The page orders findings by time; these are the stored indices of L3A's findings #3 (Rushed) and #1 (Flat pitch).
const RUSHED = { stored: 2, peek: 2, word: 'Washington' };
const FLAT = { stored: 0, peek: 0, word: 'few' };

// The pointer rests outside the page, so it hovers nothing that the page would highlight.
const OFF = { x: VIEW.width + 30, y: VIEW.height - 80 };
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const readJSON = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const toFrame = (sec) => Math.round(sec * FPS);
const round = (value, digits = 3) => Number(value.toFixed(digits));

// ---------------------------------------------------------------------------------------------------- page scripts
// Virtual time in the page: __vt.step(ms) advances the CSS animations, the media elements that play and an eased scroll.
// A smooth scrollIntoView of the page becomes that eased scroll, because the browser animates a smooth scroll in real time.
const PAGE_SETUP = `
window.__vt = { ms: 0, anims: new Map(), media: new Set(), scroll: null,
  step(ms) {
    this.ms += ms;
    for (const a of document.getAnimations()) {
      if (a.timeline !== document.timeline) continue;
      let s = this.anims.get(a);
      if (!s) { s = { base: a.currentTime ?? 0, at: this.ms - ms }; this.anims.set(a, s); a.pause(); }
      a.currentTime = s.base + (this.ms - s.at);
    }
    for (const m of this.media) {
      if (m.paused) { m.__vt = null; continue; }
      let s = m.__vt;
      // a jump of the position that this script did not make is a seek of the page: the clock restarts from there
      if (!s || Math.abs(m.currentTime - s.set) > 0.08) s = m.__vt = { t0: m.currentTime, v0: this.ms - ms, set: m.currentTime };
      const t = s.t0 + (this.ms - s.v0) / 1000;
      m.currentTime = t;
      s.set = t;
    }
    if (this.scroll) {
      const sc = this.scroll;
      sc.t += ms;
      const k = Math.min(1, sc.t / sc.dur), e = k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
      scrollTo({ top: sc.from + (sc.to - sc.from) * e, behavior: 'instant' });
      if (k >= 1) this.scroll = null;
    }
  },
  flush() { if (this.scroll) { scrollTo({ top: this.scroll.to, behavior: 'instant' }); this.scroll = null; } },
};
const play0 = HTMLMediaElement.prototype.play;
HTMLMediaElement.prototype.play = function () {
  __vt.media.add(this);
  this.muted = true;
  this.__vt = null;
  const started = play0.call(this);
  try { this.playbackRate = 0.0625; } catch (e) { /* a rate the element refuses keeps 1 */ }
  return started;
};
const intoView0 = Element.prototype.scrollIntoView;
Element.prototype.scrollIntoView = function (arg) {
  if (!arg || typeof arg !== 'object' || arg.behavior !== 'smooth') return intoView0.call(this, arg);
  __vt.flush();
  const from = scrollY;
  intoView0.call(this, { ...arg, behavior: 'instant' });
  const to = scrollY;
  scrollTo({ top: from, behavior: 'instant' });
  if (Math.abs(to - from) > 1) __vt.scroll = { from, to, t: 0, dur: Math.min(700, 320 + 0.5 * Math.abs(to - from)) };
};
addEventListener('DOMContentLoaded', () => {
  const c = document.createElement('div');
  c.innerHTML = '<svg width="24" height="28" viewBox="0 0 26 30"><path d="M3 2 L3 24 L9 18.5 L13 28 L17 26.3 L13 17 L21 17 Z" fill="#ede6da" stroke="#1f1e1d" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  Object.assign(c.style, { position: 'fixed', left: '0', top: '0', zIndex: 2147483647, pointerEvents: 'none', transform: 'translate(-100px,-100px)', filter: 'drop-shadow(0 2px 4px rgba(0,0,0,.45))' });
  document.body.append(c);
  window.__cursor = c;
});`;

// Each visible line of text, each control and each drawn waveform as [x, y, width, height, label, font px] in capture px.
// A box under another element (the sticky player bar) is not visible, so it is left out.
const BOX_SCRIPT = (scale) => {
  const atomic = '#wave, #wave-ref, .tl-host svg, .strip-track, .ring-wrap, .meter, #chart-host .cartesianlayer .subplot';
  const skip = '.horizon, .defs';
  const controls = 'button, input, select, summary, textarea, .chip, a';
  const out = [];
  // A closed <details> and a closed fold (inert) keep a layout box for their content, so elementFromPoint alone would count
  // that content as visible.
  const folded = (owner) => { const closed = owner.closest('details:not([open])'); return (!!closed && !owner.closest('summary')) || !!owner.closest('[inert]'); };
  const seen = (r, owner) => {
    if (folded(owner)) return false;
    const left = Math.max(r.left, 0), right = Math.min(r.right, innerWidth), top = Math.max(r.top, 0), bottom = Math.min(r.bottom, innerHeight);
    if (r.width < 1 || r.height < 1 || right <= left || bottom <= top) return false;
    const hit = document.elementFromPoint((left + right) / 2, (top + bottom) / 2);
    return !!hit && (owner.contains(hit) || hit.contains(owner));
  };
  const add = (r, label, owner) => out.push([Math.round(r.left * scale), Math.round(r.top * scale), Math.round(r.width * scale), Math.round(r.height * scale),
    label.trim().slice(0, 24), Math.round(parseFloat(getComputedStyle(owner).fontSize) * scale)]);
  for (const element of document.querySelectorAll(`${atomic}, ${controls}`)) {
    if (element.closest(skip) || element.parentElement?.closest(atomic)) continue;
    const r = element.getBoundingClientRect();
    if (seen(r, element)) add(r, element.textContent || element.tagName, element);
  }
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    const owner = node.parentElement;
    if (!node.textContent.trim() || !owner || owner.closest(`${skip}, ${atomic}, ${controls}, script, style`)) continue;
    const range = document.createRange();
    range.selectNodeContents(node);
    for (const r of range.getClientRects()) if (seen(r, owner)) add(r, node.textContent, owner);
  }
  return out;
};

// ---------------------------------------------------------------------------------------------------- narration timing
const narration = () => readJSON(NARRATION_FILE);
const normWord = (text) => text.toLowerCase().replace(/[^a-z0-9.]/g, '').replace(/\.$/, '');

// Scene line start frames, computed as video/src/timeline.ts computes them, and the frame of a spoken word.
function sceneFrames(id) {
  const scene = narration().scenes.find((s) => s.id === id);
  const pace = readJSON(PACING_FILE).scenes[id] ?? {};
  let cursor = pace.leadSec ?? 0;
  const lines = [];
  let clip = null;
  scene.lines.forEach((line, index) => {
    lines.push(toFrame(cursor));
    cursor += line.durationSec;
    if (scene.clip && index === scene.clipAfterLine - 1) {
      clip = { from: toFrame(cursor), to: toFrame(cursor + scene.clip.durationSec) };
      clip.segments = (scene.clip.segments || []).map((seg) => ({ ...seg, from: clip.from + toFrame(seg.startSec), to: clip.from + toFrame(seg.endSec) }));
      cursor += scene.clip.durationSec;
    }
  });
  const word = (line, text, nth = 0) => {
    const found = scene.lines[line].words.filter(([w]) => normWord(w) === normWord(text));
    if (!found[nth]) throw new Error(`${id}: line ${line} has no word ${text}`);
    return lines[line] + toFrame(found[nth][1]);
  };
  // The seconds from the first line's start to capture frame `frame`: camera keys and callouts are anchored to line 0.
  const rel = (frame) => (frame - lines[0]) / FPS;
  return { lines, clip, end: toFrame(cursor + scene.gapAfterSec + (pace.holdSec ?? 0)), word, rel };
}

// ---------------------------------------------------------------------------------------------------- audio
// Localhost on WSL resets some connections and can leave a request without an answer, so each request has a time limit
// and is tried again.
async function fetchBytes(url, attempts = 5) {
  for (let attempt = 1; ; attempt++) {
    try {
      const res = await fetch(url, { signal: AbortSignal.timeout(20000) });
      if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
      return Buffer.from(await res.arrayBuffer());
    } catch (e) {
      if (attempt >= attempts) throw e;
      await wait(1000 * attempt);
    }
  }
}

// A PCM WAV file as mono float samples; 16-bit integer and 32-bit float data.
function decodeWav(buffer) {
  let at = 12, format = null, data = null;
  while (at + 8 <= buffer.length) {
    const id = buffer.toString('ascii', at, at + 4), size = buffer.readUInt32LE(at + 4);
    if (id === 'fmt ') format = { code: buffer.readUInt16LE(at + 8), channels: buffer.readUInt16LE(at + 10), rate: buffer.readUInt32LE(at + 12), bits: buffer.readUInt16LE(at + 22) };
    if (id === 'data') data = buffer.subarray(at + 8, at + 8 + size);
    at += 8 + size + (size % 2);
  }
  if (!format || !data) throw new Error('not a WAV file');
  const width = format.bits / 8, frames = Math.floor(data.length / (width * format.channels)), samples = new Float32Array(frames);
  for (let i = 0; i < frames; i++) {
    const offset = i * width * format.channels;
    samples[i] = format.code === 3 ? data.readFloatLE(offset) : data.readInt16LE(offset) / 32768;
  }
  return { rate: format.rate, samples };
}

// The page's live level (app.js watchLevel): a 60 Hz loop of RMS * 6, capped at 1, smoothed 0.8 / 0.2; and its meter bars,
// bins 2, 8, 14, 20 and 26 of a 256-point analyser at 48 kHz (Blackman window, smoothing 0.75, -100 to -30 dB as 0 to 255).
class LevelMeter {
  constructor() { this.level = 0; this.mags = [0, 0, 0, 0, 0]; }

  reset() { this.level = 0; this.mags = [0, 0, 0, 0, 0]; }

  update(audio, t) {
    for (const at of [t - 1 / 60, t]) {
      const end = Math.round(at * audio.rate), start = Math.max(0, end - Math.round(0.05 * audio.rate));
      let sum = 0;
      for (let i = start; i < end && i < audio.samples.length; i++) sum += audio.samples[i] ** 2;
      const rms = end > start ? Math.sqrt(sum / (end - start)) : 0;
      this.level = 0.8 * this.level + 0.2 * Math.min(1, rms * 6);
      const n = 256, contextRate = 48000;
      [2, 8, 14, 20, 26].forEach((bin, k) => {
        let re = 0, im = 0;
        for (let j = 0; j < n; j++) {
          const sec = at - (n - j) / contextRate, index = Math.floor(sec * audio.rate);
          const x = index >= 0 && index < audio.samples.length ? audio.samples[index] : 0;
          const w = 0.42 - 0.5 * Math.cos((2 * Math.PI * j) / n) + 0.08 * Math.cos((4 * Math.PI * j) / n);
          re += x * w * Math.cos((2 * Math.PI * bin * j) / n);
          im -= x * w * Math.sin((2 * Math.PI * bin * j) / n);
        }
        this.mags[k] = 0.75 * this.mags[k] + 0.25 * (Math.hypot(re, im) / n);
      });
    }
    const bytes = this.mags.map((mag) => Math.max(0, Math.min(255, Math.floor((255 / 70) * (20 * Math.log10(mag + 1e-12) + 100)))));
    return { level: this.level, bars: bytes.map((b) => round(0.15 + (0.85 * b) / 255)) };
  }
}

// ---------------------------------------------------------------------------------------------------- camera fitting
const clampRect = ([l, t, r, b]) => [Math.max(0, l), Math.max(0, t), Math.min(MEDIA[0], r), Math.min(MEDIA[1], b)];

// The rect around `core` (padded) in the shape of the video window, kept on the media.
function windowRect(core, pad) {
  const cx = (core[0] + core[2]) / 2, cy = (core[1] + core[3]) / 2;
  let w = Math.max(core[2] - core[0] + 2 * pad, 1760 / MAX_ZOOM), h = core[3] - core[1] + 2 * pad;
  if (w / h < WINDOW_ASPECT) w = h * WINDOW_ASPECT; else h = w / WINDOW_ASPECT;
  w = Math.min(w, MEDIA[0]);
  h = Math.min(h, MEDIA[1]);
  const left = Math.min(Math.max(0, cx - w / 2), MEDIA[0] - w), top = Math.min(Math.max(0, cy - h / 2), MEDIA[1] - h);
  return [left, top, left + w, top + h];
}

const meets = ([l, t, r, b], [x, y, w, h]) => x < r && x + w > l && y < b && y + h > t;
const insideBy = ([l, t, r, b], [x, y, w, h], inset) => x >= l + inset && x + w <= r - inset && y >= t + inset && y + h <= b - inset;
const covers = ([l, t, r, b], [cl, ct, cr, cb]) => l <= cl && t <= ct && r >= cr && b >= cb;
const area = ([l, t, r, b]) => (r - l) * (b - t);

// Moves the edges of the window rect until no box sampled in the hold crosses an edge. Each crossing box is taken in or
// left out by one of the four edges; a beam search over these choices keeps the rects closest to the first one in size
// and shape, and the core always stays inside.
function fitRect(core, boxes, pad = 24) {
  const ideal = windowRect(core, pad);
  const inset = FIT_INSET + 1;
  const crossing = (rect) => boxes.filter((box) => meets(rect, box) && !insideBy(rect, box, FIT_INSET));
  const shape = ([l, t, r, b]) => (r - l) / (b - t);
  const zoom = ([l, t, r, b]) => Math.min(1760 / (r - l), 764 / (b - t));
  const cost = (rect) => Math.abs(Math.log(area(rect) / area(ideal))) + 0.3 * Math.abs(Math.log(shape(rect) / WINDOW_ASPECT)) + 5 * Math.max(0, zoom(rect) - MAX_ZOOM);
  const options = (rect, [x, y, w, h]) => {
    const [l, t, r, b] = rect;
    return [
      [Math.min(l, x - inset), Math.min(t, y - inset), Math.max(r, x + w + inset), Math.max(b, y + h + inset)],
      [l, Math.max(t, y + h + 1), r, b], [l, t, r, Math.min(b, y - 1)], [Math.max(l, x + w + 1), t, r, b], [l, t, Math.min(r, x - 1), b],
    ].filter((o) => o[0] >= 0 && o[1] >= 0 && o[2] <= MEDIA[0] && o[3] <= MEDIA[1] && o[2] > o[0] && o[3] > o[1] && covers(o, core));
  };
  let beam = [ideal];
  const solved = [];
  for (let depth = 0; depth < 40 && beam.length; depth++) {
    const children = new Map();
    for (const rect of beam) {
      const bad = crossing(rect).sort((p, q) => q[2] * q[3] - p[2] * p[3]);
      if (!bad.length) { solved.push(rect); continue; }
      for (const option of options(rect, bad[0])) children.set(option.map(Math.round).join(','), option);
    }
    beam = [...children.values()].sort((p, q) => crossing(p).length - crossing(q).length || cost(p) - cost(q)).slice(0, 24);
  }
  if (solved.length) return solved.sort((p, q) => cost(p) - cost(q))[0].map(Math.round);
  console.warn(`  fit: could not clear every edge of core ${core.map(Math.round)}`);
  return ideal.map(Math.round);
}

// The latest box sample at or before the capture frame.
function boxesAt(info, frame) {
  const frames = Object.keys(info.boxes).map(Number).filter((f) => f <= frame).sort((a, b) => a - b);
  return info.boxes[frames.length ? frames[frames.length - 1] : Math.min(...Object.keys(info.boxes).map(Number))];
}

// Camera keys from the recorded targets: each rect is fitted to the boxes of the frames it is held, as check-framing.cjs checks them.
function fitCamera(info, timing) {
  const keys = info.keys.map((key) => ({ ...key, frame: (key.at === 'clip' ? timing.clip.from : timing.lines[key.at]) + toFrame(key.sec ?? 0) }))
    .sort((a, b) => a.frame - b.frame);
  return keys.map((key, index) => {
    const holdFrom = index === 0 ? 0 : key.frame + (key.moveFrames ?? 30);
    const holdTo = index + 1 < keys.length ? keys[index + 1].frame : info.frames;
    const union = new Map();
    for (let frame = holdFrom; frame < Math.min(holdTo, info.frames); frame++) {
      if (info.scrolls.some(([a, b]) => frame >= a && frame < b)) continue;
      for (const box of boxesAt(info, frame)) union.set(box.slice(0, 4).join(','), box);
    }
    const rect = fitRect(key.core, [...union.values()], key.pad ?? 24);
    const zoom = Math.min(1760 / (rect[2] - rect[0]), 764 / (rect[3] - rect[1]));
    const fonts = [...union.values()].filter((box) => insideBy(rect, box, 0) && box[5]).map((box) => box[5]).sort((a, b) => a - b);
    const body = fonts.length ? fonts[Math.floor(fonts.length / 2)] : 0;
    console.log(`  key ${index} at ${key.at}+${key.sec ?? 0}s: rect ${rect} zoom ${zoom.toFixed(2)}, median text ${(body * zoom).toFixed(1)} px, smallest ${((fonts[0] ?? 0) * zoom).toFixed(1)} px`);
    const out = { at: key.at, rect };
    if (key.sec) out.sec = round(key.sec, 2);
    if (key.moveFrames) out.moveFrames = key.moveFrames;
    return out;
  });
}

// ---------------------------------------------------------------------------------------------------- callout labels
// Output px of a label (CaptureFrame.tsx CalloutPill): height, width per text, gap to the rect, and the rect's padding.
const PILL = { height: 50, width: (text) => 60 + text.length * 14.5, gap: 22, pad: 8 };
// Boxes larger than this (capture px squared) are panels, charts or waveforms: a label may cover a little of them.
const PANEL_AREA = 300000;

// The centre of each callout's label, in capture px, at the place around its rect that covers the least visible text. The
// label may sit outside the browser window, on the backdrop of the video, where no text is; it must stay clear of the
// chapter marker, the clip pill and the subtitle band (output px, CaptureFrame.tsx and DemoScenes.tsx). The rect itself
// counts as text, so the label never covers what it marks.
const KEEP_CLEAR = [[40, 20, 600, 100], [1480, 20, 1880, 95]];
const OUTPUT_AREA = [30, 0, 1890, 920];
// Capture px² of covered text that a label on the backdrop is worth.
const OUTSIDE_COST = 3000;
function placeLabels(info, timing, camera, callouts) {
  const anchor = (at, sec) => (at === 'clip' ? timing.clip.from : timing.lines[at]) + toFrame(sec ?? 0);
  const keys = camera.map((key) => ({ ...key, frame: anchor(key.at, key.sec) })).sort((a, b) => a.frame - b.frame);
  return callouts.map((callout) => {
    const start = anchor(callout.at, callout.sec);
    const view = (keys.filter((key) => key.frame <= start + 6).pop() ?? keys[0]).rect;
    const zoom = Math.min(1760 / (view[2] - view[0]), 764 / (view[3] - view[1]));
    // Capture px to output px, as CaptureFrame.tsx places the window in its frame (FRAME, chrome 36 px).
    const viewW = (view[2] - view[0]) * zoom, viewH = (view[3] - view[1]) * zoom;
    const pageLeft = 80 + (1760 - viewW) / 2, pageTop = 116 + (800 - 36 - viewH) / 2 + 36;
    const out = ([x, y]) => [pageLeft + (x - view[0]) * zoom, pageTop + (y - view[1]) * zoom];
    const [w, h, gap, pad] = [PILL.width(callout.text) / zoom, PILL.height / zoom, PILL.gap / zoom, PILL.pad / zoom];
    const [l, t, r, b] = callout.rect;
    const cx = (l + r) / 2, cy = (t + b) / 2;
    const candidates = [];
    for (const far of [1, 2.5, 4.5]) {
      const above = t - pad - far * gap - h / 2, below = b + pad + far * gap + h / 2;
      candidates.push([cx, above], [l + w / 2, above], [r - w / 2, above], [cx, below], [l + w / 2, below], [r - w / 2, below],
        [r + pad + far * gap + w / 2, cy], [l - pad - far * gap - w / 2, cy]);
    }
    const boxes = boxesAt(info, Math.min(start + 8, info.frames - 1));
    const overlap = (p, [x, y, bw, bh]) => Math.max(0, Math.min(p[2], x + bw, view[2]) - Math.max(p[0], x, view[0])) * Math.max(0, Math.min(p[3], y + bh, view[3]) - Math.max(p[1], y, view[1]));
    const meetsOut = (p, [ol, ot, or, ob]) => p[0] < or && p[2] > ol && p[1] < ob && p[3] > ot;
    const margin = 4 / zoom;
    const cost = ([x, y], index) => {
      const pill = [x - w / 2 - margin, y - h / 2 - margin, x + w / 2 + margin, y + h / 2 + margin];
      const [ol, ot] = out([pill[0], pill[1]]), [or, ob] = out([pill[2], pill[3]]);
      if (ol < OUTPUT_AREA[0] || ot < OUTPUT_AREA[1] || or > OUTPUT_AREA[2] || ob > OUTPUT_AREA[3]) return Infinity;
      if (KEEP_CLEAR.some((area) => meetsOut([ol, ot, or, ob], area))) return Infinity;
      let sum = 4 * overlap(pill, [l, t, r - l, b - t]);
      for (const box of boxes) sum += (box[2] * box[3] > PANEL_AREA ? 0.02 : 1) * overlap(pill, box);
      return sum + index;
    };
    // A label inside the window costs less than one on the backdrop, which is used only when the window has no free place.
    const inWindow = ([x, y]) => x - w / 2 - margin >= view[0] && y - h / 2 - margin >= view[1] && x + w / 2 + margin <= view[2] && y + h / 2 + margin <= view[3];
    const scored = candidates.map((c, index) => ({ c, cost: cost(c, index) + (inWindow(c) ? 0 : OUTSIDE_COST) })).sort((p, q) => p.cost - q.cost);
    if (!Number.isFinite(scored[0].cost)) {
      console.warn(`  callout "${callout.text}": no free place; the label goes above or below its rect`);
      return callout;
    }
    if (scored[0].cost % OUTSIDE_COST >= candidates.length) console.warn(`  callout "${callout.text}": its label covers ${Math.round(scored[0].cost)} capture px² of text`);
    return { ...callout, label: scored[0].c.map(Math.round) };
  });
}

// ---------------------------------------------------------------------------------------------------- stop motion
class StopMotion {
  constructor(page, dir, port) {
    this.page = page;
    this.dir = dir;
    this.port = port;
    this.count = 0;
    this.pointer = { x: VIEW.width + 40, y: VIEW.height + 40 };
    this.boxes = {};
    this.lastBoxes = -Infinity;
    this.scrollYs = [];
    this.keys = [];
    this.clicks = [];
    this.callouts = [];
    this.sounds = [];
    this.marks = {};
    this.meter = new LevelMeter();
    this.audio = new Map();
    this.beforeShoot = null;
    this.gateFrame = null;
  }

  file(index) { return path.join(this.dir, String(index).padStart(5, '0') + '.jpg'); }

  async audioOf(url) {
    if (!this.audio.has(url)) this.audio.set(url, decodeWav(await fetchBytes(url)));
    return this.audio.get(url);
  }

  // One frame of virtual time: the page clock, the CSS animations, the media positions and the live level.
  async tick() {
    const ms = Math.round(((this.count + 1) * 1000) / FPS) - Math.round((this.count * 1000) / FPS);
    // The drawn pointer follows this.pointer, not the mouse events: the browser drops a mouse event outside the viewport,
    // so a pointer that leaves the page would stay drawn at its last place on the edge.
    await this.page.evaluate(({ ms, x, y }) => {
      __vt.step(ms);
      if (window.__cursor) window.__cursor.style.transform = `translate(${x - 3}px,${y - 2}px)`;
    }, { ms, x: this.pointer.x, y: this.pointer.y });
    await this.page.clock.runFor(ms);
    await wait(12);
    const playing = await this.page.evaluate(() => {
      const media = playingMedia();
      if (!media) return null;
      const src = media.currentSrc || media.src;
      return { src: src.startsWith('blob:') ? new URL(S.base + S.result.participant.audio, location.href).href : src, t: media.currentTime };
    });
    if (!playing) { this.meter.reset(); return; }
    const { level, bars } = this.meter.update(await this.audioOf(playing.src), playing.t);
    await this.page.evaluate(({ level, bars }) => {
      S.level = level;
      document.documentElement.style.setProperty('--level', level.toFixed(3));
      document.querySelectorAll('.meter i').forEach((bar, k) => { bar.style.transform = `scaleY(${bars[k]})`; });
      if (S.sea && document.querySelector('#cloud-sea').getBoundingClientRect().bottom > 0) composeSea(level);
    }, { level, bars });
  }

  async shoot() {
    await this.page.mouse.move(this.pointer.x, this.pointer.y);
    await this.tick();
    if (this.beforeShoot) await this.beforeShoot();
    await this.page.screenshot({ path: this.file(this.count), type: 'jpeg', quality: 93 });
    this.scrollYs.push(await this.page.evaluate(() => [scrollY, document.querySelector('#explain')?.scrollTop ?? 0]));
    if (this.count - this.lastBoxes >= BOX_EVERY) await this.sampleBoxes();
    this.count += 1;
  }

  async sampleBoxes() {
    this.boxes[this.count] = await this.page.evaluate(BOX_SCRIPT, SCALE);
    this.lastBoxes = this.count;
  }

  async holdUntil(frame) { while (this.count < frame) await this.shoot(); }

  async glideTo(target, endFrame) {
    const from = { ...this.pointer };
    const startFrame = this.count;
    const span = Math.max(1, endFrame - startFrame);
    while (this.count < endFrame) {
      const t = easeInOut((this.count - startFrame + 1) / span);
      this.pointer = { x: from.x + (target.x - from.x) * t, y: from.y + (target.y - from.y) * t };
      await this.shoot();
    }
    this.pointer = { ...target };
  }

  async glideToSelector(selector, endFrame) { await this.glideTo(await center(this.page, selector), endFrame); }

  // A real click at the pointer; the video shows its ripple and plays its sound at the next frame. A playback started by a
  // click at frame F shows its first position at F + 1, so a click that starts the clip audio comes one frame after it.
  async click() {
    this.clicks.push([this.count, Math.round(this.pointer.x * SCALE), Math.round(this.pointer.y * SCALE)]);
    await this.page.mouse.move(this.pointer.x, this.pointer.y);
    await this.page.mouse.down();
    await this.page.mouse.up();
    this.lastBoxes = -Infinity;
    await wait(120);
  }

  // A real click on a file field: the file chooser of the click receives the file.
  async chooseFile(file) {
    const chooser = this.page.waitForEvent('filechooser');
    await this.click();
    await (await chooser).setFiles(file);
    await wait(150);
  }

  async clickAt(selector, glideEnd, clickFrame = glideEnd) {
    await this.glideToSelector(selector, glideEnd);
    await this.holdUntil(clickFrame);
    await this.click();
  }

  sound(name, frame = this.count) { this.sounds.push([frame, name]); }

  // Picks an example from the open menu. The page's fade and audio load run without frames, so the video cuts from the
  // click to the loaded example; the ripple ends with the click frame, as the chip it marks is gone in the next frame.
  async pick(id, glideEnd, clickFrame) {
    await this.clickAt(`.chip[data-id="${id}"]`, glideEnd, clickFrame);
    this.clicks[this.clicks.length - 1].push(0);
    const loaded = () => this.page.evaluate((id) => document.querySelector(`.chip[data-id="${id}"]`).getAttribute('aria-pressed') === 'true'
      && !document.querySelector('main').classList.contains('fading') && S.youReady && (S.refReady || !S.ref.src), id);
    await this.waitOffline(loaded, 60000, 40);
  }

  // Scrolls the page by `by` CSS px over the frames up to endFrame; the pointer keeps its place on the screen.
  async scrollBy(by, endFrame) {
    const from = await this.page.evaluate(() => scrollY);
    const startFrame = this.count;
    const span = Math.max(1, endFrame - startFrame);
    while (this.count < endFrame) {
      const t = easeInOut((this.count - startFrame + 1) / span);
      await this.page.evaluate((y) => scrollTo({ top: y, behavior: 'instant' }), from + by * t);
      await this.shoot();
    }
  }

  // Advances the page clock without frames until `ready` holds: the wait for a server job, which the video does not show.
  async waitOffline(ready, timeoutMs = 240000, stepMs = 100) {
    const started = Date.now();
    while (!(await ready())) {
      if (Date.now() - started > timeoutMs) throw new Error('timed out waiting for the server job');
      await this.page.clock.runFor(stepMs);
      await wait(60);
    }
  }

  // A camera target: `core` (capture px) must show from narration line `at` (or the clip) plus `sec`.
  key(at, sec, core, extra = {}) { this.keys.push({ at, sec, core: core.map(Math.round), ...extra }); }

  callout(at, sec, rect, text, durSec) { this.callouts.push({ at, sec: round(sec, 2), ...(durSec ? { durSec } : {}), rect: rect.map(Math.round), text }); }

  // The frames in which the page or the finding panel scrolls.
  scrolls() {
    const out = [];
    this.scrollYs.forEach((ys, frame) => {
      if (frame > 0 && ys.some((y, k) => Math.abs(y - this.scrollYs[frame - 1][k]) > 0.5)) out.push([frame, frame + 1]);
    });
    return out;
  }

  // Scrolls the finding panel (a scroll box of its own, held under the player bar) by `by` CSS px over the frames up to endFrame.
  async scrollPanel(by, endFrame) {
    const from = await this.page.evaluate(() => document.querySelector('#explain').scrollTop);
    const startFrame = this.count;
    const span = Math.max(1, endFrame - startFrame);
    while (this.count < endFrame) {
      const t = easeInOut((this.count - startFrame + 1) / span);
      await this.page.evaluate((y) => { document.querySelector('#explain').scrollTop = y; }, from + by * t);
      await this.shoot();
    }
  }
}

// ---------------------------------------------------------------------------------------------------- page helpers
async function center(page, selector) {
  const box = await page.locator(selector).first().boundingBox();
  if (!box) throw new Error(`no box for ${selector}`);
  return { x: box.x + box.width / 2, y: box.y + box.height / 2 };
}

// The capture px rect [left, top, right, bottom] of the union of the first visible match of each selector.
async function capRect(page, ...selectors) {
  const rects = await page.evaluate((selectors) => selectors.map((selector) => {
    const element = [...document.querySelectorAll(selector)].find((e) => e.getBoundingClientRect().width > 0);
    if (!element) return null;
    const r = element.getBoundingClientRect();
    return [r.left, r.top, r.right, r.bottom];
  }), selectors);
  const found = rects.filter(Boolean);
  if (found.length !== selectors.length) throw new Error(`no rect for ${selectors.filter((_, i) => !rects[i]).join(', ')}`);
  return clampRect([Math.min(...found.map((r) => r[0])), Math.min(...found.map((r) => r[1])), Math.max(...found.map((r) => r[2])), Math.max(...found.map((r) => r[3]))].map((v) => v * SCALE));
}

// The capture px rect of the text itself (not its block) of the first visible match of `selector`, or of the innermost
// element under `selector` whose text contains `text`: a callout outlines the words, not the width of their column.
async function inkRect(page, selector, text = null) {
  const r = await page.evaluate(({ selector, text }) => {
    const candidates = text === null ? [...document.querySelectorAll(selector)]
      : [...document.querySelectorAll(`${selector} *`)].filter((e) => e.textContent.includes(text) && ![...e.children].some((c) => c.textContent.includes(text)));
    const element = candidates.find((e) => e.getBoundingClientRect().width > 0);
    if (!element) return null;
    const range = document.createRange();
    range.selectNodeContents(element);
    const b = range.getBoundingClientRect();
    return [b.left, b.top, b.right, b.bottom];
  }, { selector, text });
  if (!r) throw new Error(`no text for ${selector} ${text ?? ''}`);
  return clampRect(r.map((v) => v * SCALE));
}

// The part of `rect` (capture px) that shows in the viewport below the sticky player bar.
async function visibleRect(page, rect) {
  const barBottom = await page.evaluate(() => document.querySelector('.player').getBoundingClientRect().bottom);
  return [rect[0], Math.max(rect[1], barBottom * SCALE + 4), rect[2], Math.min(rect[3], MEDIA[1])];
}

const textOf = (page, selector) => page.evaluate((selector) => document.querySelector(selector)?.innerText.trim().replace(/\s+/g, ' ') ?? '', selector);

async function ready(page) {
  await page.waitForFunction(() => !document.querySelector('#play-all').disabled && document.querySelectorAll('#transcript .w').length > 0, null, { timeout: 60000 });
}

// Loads the page (L3A is the default example) and lets the first-load sequence end; then the page clock stops.
async function setup(page, port) {
  for (let attempt = 1; ; attempt++) {
    try {
      await page.goto(`http://127.0.0.1:${port}/`, { waitUntil: 'domcontentloaded' });
      break;
    } catch (e) {
      if (attempt >= 6) throw e;
      await wait(1000 * attempt);
    }
  }
  await ready(page);
  await page.waitForFunction(() => !document.body.classList.contains('intro'), null, { timeout: 30000 });
  await page.mouse.move(VIEW.width + 40, VIEW.height + 40);
  await wait(800);
  await page.clock.pauseAt(await page.evaluate(() => Date.now()) + 50);
  await page.evaluate(() => __vt.flush());
}

// The scroll offset that puts the element top `gap` CSS px below the sticky player bar.
async function belowPlayer(page, selector, gap = 16) {
  return page.evaluate(({ selector, gap }) => {
    const top = document.querySelector(selector).getBoundingClientRect().top;
    const bar = document.querySelector('.player').getBoundingClientRect().bottom;
    return top - bar - gap;
  }, { selector, gap });
}

async function scrollNow(page, by) {
  await page.evaluate((by) => scrollBy({ top: by, behavior: 'instant' }), by);
  await wait(200);
}

// A click before the recording starts, with the page clock running for it.
async function setupClick(page, selector) {
  await page.click(selector);
  await page.clock.runFor(800);
  await page.evaluate(() => __vt.flush());
  await wait(300);
}

// The finding panel is a scroll box held under the player bar: the panel scrolls, then the page, until the bottom of
// `selector` shows with a margin.
async function revealInPanel(m, selector, frames) {
  const margin = 14;
  const panelBy = await m.page.evaluate(({ selector, margin }) => Math.max(0, document.querySelector(selector).getBoundingClientRect().bottom
    - (document.querySelector('#explain').getBoundingClientRect().bottom - margin)), { selector, margin });
  if (panelBy > 0) await m.scrollPanel(panelBy, m.count + frames);
  const pageBy = await m.page.evaluate(({ selector, margin }) => Math.max(0, document.querySelector(selector).getBoundingClientRect().bottom - (innerHeight - margin)), { selector, margin });
  if (pageBy > 0) await m.scrollBy(pageBy, m.count + frames);
}

const wordSelector = (peek, word) => `#transcript .w[data-peek="${peek}"]:text-is("${word}")`;

// A server job runs in real time while the recording takes several real seconds per video second, so a job would finish
// within a few video frames. The page's poll that reports the finished job (or its refusal) is held until `releaseFrame`,
// so the result shows when the narration reaches it; the stages before it show as the server reports them.
async function gateJobs(page, motion) {
  await page.route(/\/api\/jobs\/[0-9a-f]+$/, async (route) => {
    const response = await route.fetch();
    const body = await response.text();
    let state = null;
    try { state = JSON.parse(body).state; } catch { /* not JSON: passed on as it is */ }
    if (state === 'done' || state === 'error') while (motion.gateFrame !== null && motion.count < motion.gateFrame) await wait(40);
    await route.fulfill({ response, body });
  });
}

// Shoots frames while a job runs, until `done` holds; the result is released at releaseFrame. The page then plays an edited
// take on its own; the recording stops it before the first frame of the result, so the scene clip chooses the sides.
async function runJob(motion, done, releaseFrame, { stopPlayer = false, mark = 'result' } = {}) {
  const page = motion.page;
  const check = typeof done === 'string' ? () => page.evaluate((selector) => !!document.querySelector(selector), done) : done;
  const settle = async () => {
    if (stopPlayer) await page.evaluate(() => S.fix.player?.stop());
    motion.marks[mark] = motion.count;
  };
  motion.marks[mark] = undefined;
  motion.gateFrame = releaseFrame;
  motion.beforeShoot = async () => { if (motion.marks[mark] === undefined && (await check())) await settle(); };
  while (motion.marks[mark] === undefined && motion.count < releaseFrame + 3) await motion.shoot();
  motion.gateFrame = null;
  if (motion.marks[mark] === undefined) {
    await motion.waitOffline(check);
    await settle();
  }
  motion.beforeShoot = null;
  return motion.marks[mark];
}

// ---------------------------------------------------------------------------------------------------- shots
const SHOTS = {
  // The examples menu opens and L3A is picked; the whole result with its tinted findings, the score at "86", then the
  // three costliest fixes.
  async s3_open_example(page, m) {
    const sc = sceneFrames('s3_open_example');
    m.pointer = { x: 1120, y: 470 };
    m.key(0, sc.rel(0), [900, 0, MEDIA[0], 600]);
    await m.holdUntil(8);
    await m.clickAt('#picker-menu > summary', 20, 22);
    await m.holdUntil(25);
    m.key(0, sc.rel(25), await capRect(page, '#chips'), { moveFrames: 18 });
    // The score counts up on the first load of the page only; L3A is that first load, so the count runs again for the pick.
    await page.evaluate(() => { S.counted = false; });
    await m.pick(EXAMPLE, 44, 47);
    m.sound('rise', m.count + 2);
    const slipsAt = sc.word(0, 'delivery');
    // This move lasts until the next key, so no short hold of a half-loaded page comes between them.
    m.key(0, sc.rel(m.count + 1), await capRect(page, '#hero-title', '.ring-wrap', '#summary-line'), { moveFrames: slipsAt - 16 - (m.count + 1) });
    await m.glideTo(OFF, slipsAt - 16);
    await m.scrollBy(await belowPlayer(page, '#ledger', 150), slipsAt);
    m.key(0, sc.rel(slipsAt - 16), await capRect(page, '#ledger', '#hero-wave'), { moveFrames: 30 });
    const scoreAt = sc.word(0, 'It');
    await m.holdUntil(scoreAt);
    m.key(0, sc.rel(scoreAt), await capRect(page, '.ring-wrap', '#summary-line', '#regime-badge'), { moveFrames: 24 });
    const fixesAt = sc.word(0, 'three');
    m.callout(0, sc.rel(sc.word(0, 'scores')), await capRect(page, '.ring-wrap'), 'Score 86.11', round((fixesAt - 2 - sc.word(0, 'scores')) / FPS, 2));
    await m.holdUntil(fixesAt - 2);
    await m.scrollBy(await belowPlayer(page, '.fixes h2', 12), fixesAt + 22);
    m.key(0, sc.rel(fixesAt - 2), await capRect(page, '.fixes h2', '#top-cards'), { moveFrames: 30 });
    await m.holdUntil(sc.end + 4);
    m.description = `Page with L3A; the pointer opens "Try an example" ("${await textOf(page, '.chip[data-id="L3A"]')}" first) and picks it; the score counts up to ${await textOf(page, '#overall-fig')}, "${await textOf(page, '#summary-line')}", the waveforms with tinted findings; then "${await textOf(page, '.fixes h2')}": ${(await page.evaluate(() => [...document.querySelectorAll('#top-cards .top-card .card-title')].map((c) => c.innerText.replace(/\s+/g, ' ').trim()).join(' | ')))}.`;
  },

  // The waveform strip gives each finding its seconds and the transcript its words; then the recording plays over the
  // rushed words while the transcript follows.
  async s4_listen(page, m) {
    const sc = sceneFrames('s4_listen');
    const startSec = narration().scenes.find((s) => s.id === 's4_listen').clip.sourceStartSec ?? 13.8;
    await page.evaluate((t) => seekYours(t), startSec);
    await page.clock.runFor(300);
    await wait(200);
    await scrollNow(page, await belowPlayer(page, '#ledger', 14));
    await page.evaluate(() => __vt.flush());
    m.pointer = { x: 900, y: 700 };
    m.key(0, 0, await capRect(page, '.tl-stage'));
    const wordsAt = sc.word(0, 'words');
    m.callout(0, sc.rel(sc.word(0, 'pinned')), await capRect(page, '#fault-strip .strip-span[data-i="2"]', '#fault-strip .strip-label[data-i="2"]'), '#3 Rushed: 15.80–17.14 s', round((wordsAt - 8 - sc.word(0, 'pinned')) / FPS, 2));
    await m.holdUntil(wordsAt - 8);
    const scrollFrom = m.count;
    await m.scrollBy(await belowPlayer(page, '#text-view', 14), wordsAt + 8);
    m.key(0, sc.rel(scrollFrom), await capRect(page, '.player', '#text-view'), { moveFrames: 20 });
    await m.glideToSelector('#play-all', sc.clip.from - 2);
    await m.holdUntil(sc.clip.from + 1);
    await m.click();
    m.syncFrame = m.count - 1;
    await m.glideTo({ x: 900, y: 700 }, sc.clip.from + 24);
    await m.holdUntil(sc.clip.to - 12);
    await m.glideToSelector('#play-all', sc.clip.to - 2);
    await m.holdUntil(sc.clip.to + 1);
    await m.click();
    m.marks.paused = await page.evaluate(() => S.ws.getCurrentTime());
    await m.glideTo(OFF, sc.clip.to + 14);
    await m.holdUntil(sc.end + 4);
    m.description = `L3A waveform panel: the strip and the tinted findings, #3 Rushed at 15.80-17.14 s; then the transcript under the player bar; Play from ${startSec.toFixed(2)} s to ${m.marks.paused.toFixed(2)} s: the transcript highlight follows the voice over 'the Washington Monument and then'.`;
  },

  // Finding #3 opens from its word; 0.87 s against 1.62 s; Listen plays yours, then the reference; then How to fix.
  async s5_finding(page, m) {
    const sc = sceneFrames('s5_finding');
    await setupClick(page, wordSelector(4, 'humidity'));
    await scrollNow(page, await belowPlayer(page, '#text-view', 14));
    await page.evaluate(() => __vt.flush());
    m.pointer = { x: 760, y: 700 };
    m.key(0, sc.rel(0), await capRect(page, '#text-view', '#explain h3'));
    await m.clickAt(wordSelector(RUSHED.peek, RUSHED.word), 12, 15);
    await m.glideTo({ x: 720, y: 640 }, 26);
    m.key(0, sc.rel(20), await capRect(page, '#explain h3', '#explain .gauge'), { moveFrames: 24 });
    const numbersAt = sc.word(0, '0.87') - 4;
    m.callout(0, sc.rel(numbersAt), await inkRect(page, '#explain', '0.87 s in your reading'), '0.87 s vs 1.62 s', round((sc.clip.from - 34 - numbersAt) / FPS, 2));
    await m.holdUntil(sc.clip.from - 30);
    m.key(0, sc.rel(sc.clip.from - 30), await capRect(page, '.player', '#transcript', '#explain [data-listen]'), { moveFrames: 24 });
    await m.glideToSelector('#explain [data-listen]', sc.clip.from - 4);
    await m.holdUntil(sc.clip.from + 1);
    await m.click();
    m.syncFrame = m.count - 1;
    await m.glideTo({ x: 1000, y: 700 }, sc.clip.from + 30);
    m.marks.listen = await textOf(page, '#explain .listen-caption');
    await m.holdUntil(sc.lines[1]);
    m.key(1, 0, await capRect(page, '#explain .fix'), { moveFrames: 24 });
    await m.holdUntil(sc.end + 4);
    m.description = `L3A text and finding panel (#5 Volume drops open); the pointer clicks 'Washington': panel "#3 Rushed −4.89 pts", "${await textOf(page, '#explain .gauge')}" gauge, "0.87 s in your reading, 1.62 s in the reference"; Listen plays yours then the reference (${m.marks.listen}); then How to fix: "${await textOf(page, '#explain .fix')}".`;
  },

  // Hear it fixed on #3: progress, the result with its checks, Yours / Edited / Target in step with the clip, then the outcome.
  async s6_hear_fixed(page, m) {
    const sc = sceneFrames('s6_hear_fixed');
    await scrollNow(page, await belowPlayer(page, '#explain', 14));
    const button = await center(page, '#explain [data-fix]');
    m.pointer = { x: button.x + 70, y: button.y + 60 };
    m.key(0, 0, await capRect(page, '#explain h3', '#explain .listen-caption'));
    // The press waits until the cut into the scene has ended (DemoScenes cuts take 12 frames), so its ripple shows.
    await m.clickAt('#explain [data-fix]', 12, 14);
    await m.glideTo({ x: 1000, y: 700 }, m.count + 12);
    await runJob(m, '#explain .fixer .abc', sc.word(0, 'then'), { stopPlayer: true });
    m.sound('chime', m.marks.result);
    await m.glideTo(OFF, m.count + 6);
    await revealInPanel(m, '#explain .fixer', 10);
    m.key(0, sc.rel(m.marks.result), await capRect(page, '#explain [data-fix]', '#explain .fixer'), { moveFrames: m.count - m.marks.result + 6 });
    await m.holdUntil(sc.clip.from - 18);
    m.key('clip', 0, await capRect(page, '#explain .fixer .fix-head', '#explain .fixer .abc'), { moveFrames: 20 });
    const sides = { Yours: 'yours', Edited: 'fixed', Target: 'target' };
    for (const seg of sc.clip.segments) {
      await m.glideToSelector(`#explain .fixer .abc [data-side="${sides[seg.label]}"]`, seg.from + 1);
      await m.click();
      if (seg.label === 'Yours') m.syncFrame = m.count - 1;
    }
    const last = sc.clip.segments[sc.clip.segments.length - 1];
    await m.glideToSelector('#explain .fixer .loop-btn', last.to + 1);
    await m.click();
    await m.glideTo(OFF, sc.lines[1]);
    m.key(1, 0, await capRect(page, '#explain .fixer .fix-head', '#explain .fixer .fix-score'), { moveFrames: 24 });
    const scoreAt = sc.word(1, '3.07') - 4;
    const headAt = sc.word(1, 'still') - 4;
    m.callout(1, sc.rel(headAt) - sc.rel(sc.lines[1]), await inkRect(page, '#explain .fixer .fix-head'), await textOf(page, '#explain .fixer .fix-head'), round((scoreAt - 2 - headAt) / FPS, 2));
    m.callout(1, sc.rel(scoreAt) - sc.rel(sc.lines[1]), await inkRect(page, '#explain .fixer .fix-score'), '+3.07', round((sc.end - scoreAt - 8) / FPS, 2));
    await m.holdUntil(sc.end + 4);
    m.marks.audio = await page.evaluate(() => S.fix.jobs.get(S.result.flaws[2].id)?.audio);
    m.description = `L3A finding #3 Rushed: the pointer presses Hear it fixed; the progress line shows, then "${await textOf(page, '#explain .fixer .fix-head')}", "${await textOf(page, '#explain .fixer .fix-score')}", the two checks; Yours, Edited and Target are pressed in step with the clip, then Stop.`;
  },

  // Finding #1 (Flat pitch): Hear it fixed is not edited; Try the reference's melody is no longer flagged; Edited, then Yours.
  async s7_melody(page, m) {
    const sc = sceneFrames('s7_melody');
    await scrollNow(page, await belowPlayer(page, '#text-view', 14));
    m.pointer = { x: 760, y: 700 };
    m.key(0, sc.rel(0), await capRect(page, '#text-view', '#explain h3'));
    await m.clickAt(wordSelector(FLAT.peek, FLAT.word), 10, 12);
    await m.holdUntil(15);
    m.key(0, sc.rel(15), await capRect(page, '#explain h3', '#explain [data-fix]'), { moveFrames: 18 });
    await m.clickAt('#explain [data-fix]', 30, 33);
    await runJob(m, '#explain .fixer .fix-head', sc.word(0, 'too'));
    m.key(0, sc.rel(m.count + 1), await capRect(page, '#explain [data-fix]', '#explain .fixer'), { moveFrames: 20 });
    await m.clickAt('#explain [data-fix$="-melody"]', sc.word(0, 'borrow') - 2, sc.word(0, 'borrow'));
    await m.glideTo({ x: 1000, y: 720 }, m.count + 12);
    await runJob(m, '#explain .fixer-melody .abc', sc.word(0, 'voice'), { stopPlayer: true });
    m.sound('chime', m.marks.result);
    await m.glideTo(OFF, m.count + 8);
    await revealInPanel(m, '#explain .fixer-melody', 14);
    const panel = await capRect(page, '#explain'), card = await capRect(page, '#explain .fixer-melody');
    m.key(0, sc.rel(m.marks.result), [card[0], Math.max(card[1], panel[1]), card[2], Math.min(card[3], panel[3])], { moveFrames: m.count - m.marks.result + 6 });
    const flaggedAt = sc.word(0, 'no') - 4;
    m.callout(0, sc.rel(flaggedAt), await inkRect(page, '#explain .fixer-melody .fix-head'), 'No longer flagged', round((sc.clip.from - flaggedAt) / FPS, 2));
    const [edited, yours] = sc.clip.segments;
    await m.glideToSelector('#explain .fixer-melody .loop-btn', edited.from + 1);
    await m.click();
    m.syncFrame = m.count - 1;
    await m.glideToSelector('#explain .fixer-melody [data-side="yours"]', yours.from + 1);
    await m.click();
    await m.glideToSelector('#explain .fixer-melody .loop-btn', yours.to + 1);
    await m.click();
    await m.glideTo(OFF, yours.to + 14);
    await m.holdUntil(sc.end + 4);
    m.marks.audio = await page.evaluate(() => S.fix.jobs.get(`${S.result.flaws[0].id}:contour`)?.audio);
    m.description = `L3A: the pointer clicks 'few' (#1 Flat pitch) and presses Hear it fixed: "${await textOf(page, '#explain .fixer > .fix-head')}"; then Try the reference's melody: "${await textOf(page, '#explain .fixer-melody .fix-head')}", "${await textOf(page, '#explain .fixer-melody .fix-score')}"; Play (Edited) and Yours in step with the clip, then Stop.`;
  },

  // Fix everything and listen: 86.11 becomes 96.17; What each fix did opens.
  async s8_fix_all(page, m) {
    const sc = sceneFrames('s8_fix_all');
    await scrollNow(page, await belowPlayer(page, '#ledger', 14));
    const button = await center(page, '#fix-all-btn');
    m.pointer = { x: button.x + 80, y: button.y - 50 };
    m.key(0, 0, await capRect(page, '#ledger'));
    await m.clickAt('#fix-all-btn', sc.word(0, 'fix') - 2, sc.word(0, 'fix'));
    const scoreAt = sc.word(0, '86');
    await runJob(m, '#fix-all-body .fix-all-score', scoreAt - 8, { stopPlayer: true });
    m.sound('chime', m.marks.result);
    await m.glideTo(OFF, m.count + 8);
    // The box takes the line under the score too, so its edge runs between lines of text, not through one.
    const score = await inkRect(page, '#fix-all-body .fix-all-score'), under = await inkRect(page, '#fix-all-body', 'Your whole reading');
    m.key(0, sc.rel(m.marks.result + 2), [...(await capRect(page, '#ledger')).slice(0, 3), under[3] + 12], { moveFrames: 20 });
    const listAt = sc.word(0, 'with');
    m.callout(0, sc.rel(scoreAt), [Math.min(score[0], under[0]), score[1], Math.max(score[2], under[2]), under[3]], '86.11 → 96.17', round((listAt - 12 - scoreAt) / FPS, 2));
    // The summary row spans the card, so the pointer goes to its words; they are measured again just before the click,
    // because the result card is still settling when it first shows.
    const summaryWords = async () => {
      const r = await inkRect(page, '#fix-all-body .fix-list > summary');
      return { x: (r[0] + r[2]) / 2 / SCALE, y: (r[1] + r[3]) / 2 / SCALE };
    };
    await m.glideTo(await summaryWords(), listAt - 12);
    await m.glideTo(await summaryWords(), listAt - 9);
    await m.click();
    if (!(await page.evaluate(() => document.querySelector('#fix-all-body .fix-list').open))) throw new Error('What each fix did did not open');
    const opened = m.count;
    await m.glideTo(OFF, m.count + 6);
    await m.scrollBy(await belowPlayer(page, '#fix-all-body .fix-all-score', 20), m.count + 12);
    // The list alone, close enough to read: its first entries fill the window.
    const list = await visibleRect(page, await capRect(page, '#fix-all-body .fix-list'));
    m.key(0, sc.rel(opened), [list[0], list[1], list[2], Math.min(list[3], list[1] + (list[2] - list[0]) / WINDOW_ASPECT)], { moveFrames: m.count - opened + 6 });
    await m.holdUntil(sc.end + 4);
    m.description = `L3A score card; the pointer presses Fix everything and listen; progress, then "${await textOf(page, '#fix-all-body .fix-all-score')}" with "${(await textOf(page, '#fix-all-body')).match(/Your whole reading[^.]*\.[^.]*\./)?.[0] ?? ''}"; What each fix did opens: ${(await textOf(page, '#fix-all-body .fix-list')).slice(0, 220)}...`;
  },

  // From the transcript's underlined words to the measurement charts: Every measurement opens, and a drag zooms the pitch
  // chart onto the stretch of flag #1 (Flat pitch, 8.68-11.04 s).
  async s9_text_lists(page, m) {
    const sc = sceneFrames('s9_text_lists');
    await scrollNow(page, await belowPlayer(page, '#text-view', 14));
    // A little further, so the Every measurement toggle under the transcript shows whole.
    await scrollNow(page, await page.evaluate(() => Math.max(0, document.querySelector('#measures-toggle').getBoundingClientRect().bottom + 12 - innerHeight)));
    await page.evaluate(() => __vt.flush());
    m.pointer = { x: 1100, y: 640 };
    m.key(0, 0, await visibleRect(page, await capRect(page, '#text-view', '#measures-toggle')));
    await m.glideToSelector(wordSelector(FLAT.peek, FLAT.word), sc.word(0, 'transcript'));
    const chartAt = sc.word(0, 'chart');
    await m.clickAt('#measures-toggle', chartAt - 8, chartAt - 4);
    await m.holdUntil(m.count + 2);
    const scrollFrom = m.count;
    await m.scrollBy(await belowPlayer(page, '#chart-host', 0), m.count + 16);
    const plot = await page.evaluate(() => {
      const r = document.querySelector('#chart .nsewdrag').getBoundingClientRect();
      return { left: r.left, top: r.top, width: r.width, height: r.height };
    });
    m.key(0, sc.rel(scrollFrom), clampRect([plot.left * SCALE - 140, (plot.top - 40) * SCALE, (plot.left + plot.width) * SCALE + 30, (plot.top + plot.height + 30) * SCALE]), { moveFrames: 16 });
    const y = plot.top + plot.height * 0.5;
    const tracesAt = sc.word(0, 'traces');
    await m.glideTo({ x: plot.left + plot.width * 0.27, y }, tracesAt - 8);
    await page.mouse.move(m.pointer.x, m.pointer.y);
    m.clicks.push([m.count, Math.round(m.pointer.x * SCALE), Math.round(y * SCALE)]);
    await page.mouse.down();
    await m.glideTo({ x: plot.left + plot.width * 0.44, y: y + 3 }, tracesAt + 6);
    await page.mouse.up();
    m.marks.zoomed = m.count;
    await m.glideTo(OFF, m.count + 10);
    const measureAt = sc.word(0, 'measurement') - 4;
    m.callout(0, sc.rel(measureAt), clampRect([plot.left * SCALE, plot.top * SCALE, (plot.left + plot.width) * SCALE, (plot.top + plot.height) * SCALE]), 'Flag #1: the pitch range', round((sc.end - measureAt - 4) / FPS, 2));
    await m.holdUntil(sc.end + 4);
    m.description = `L3A transcript with its underlined findings; the pointer opens Every measurement; a drag across the pitch chart zooms onto flag #1 (Flat pitch, 8.68-11.04 s).`;
  },

  // The identity example: 100.00 and nothing flagged; the median-of-five example.
  async s10_fair(page, m) {
    const sc = sceneFrames('s10_fair');
    m.pointer = { x: 1120, y: 470 };
    m.key(0, 0, [900, 0, MEDIA[0], 600]);
    await m.clickAt('#picker-menu > summary', 6, 8);
    await m.holdUntil(10);
    m.key(0, sc.rel(10), await capRect(page, '#chips'), { moveFrames: 16 });
    await m.pick('identity', 30, 33);
    await m.glideTo(OFF, 45);
    m.key(0, sc.rel(40), await capRect(page, '.ring-wrap', '#summary-line', '#regime-badge'), { moveFrames: 24 });
    const fiveAt = sc.word(0, 'With');
    const hundredAt = sc.word(0, 'scores') - 4;
    m.callout(0, sc.rel(hundredAt), await capRect(page, '.ring-wrap', '#summary-line'), '100, nothing flagged', round((fiveAt - 4 - hundredAt) / FPS, 2));
    m.marks.identity = `${await textOf(page, '#overall-fig')}: "${await textOf(page, '#summary-line')}"`;
    await m.clickAt('#picker-menu > summary', fiveAt - 2, fiveAt);
    m.key(0, sc.rel(fiveAt + 2), await capRect(page, '#picker-menu .picker-panel'), { moveFrames: 15 });
    await m.clickAt('#more-examples > summary', fiveAt + 14, fiveAt + 16);
    // The camera follows the grown menu until the pick: a view of the whole menu would cut the waveform under it.
    const pickAt = fiveAt + 34;
    m.key(0, sc.rel(m.count + 1), await capRect(page, '#picker-menu .picker-panel'), { moveFrames: pickAt - (m.count + 1) });
    await m.pick('r2_consensus', fiveAt + 31, pickAt);
    const picked = m.count;
    await m.glideTo(OFF, picked + 14);
    m.key(0, sc.rel(picked), await capRect(page, '.ring-wrap', '#summary-line', '#reference-mode'), { moveFrames: 30 });
    const medianAt = sc.word(0, 'wordbyword') - 4;
    m.callout(0, sc.rel(medianAt), await inkRect(page, '#ledger', 'median of five'), 'Median of five readers', round((sc.end - medianAt - 4) / FPS, 2));
    await m.holdUntil(sc.end + 4);
    m.description = `The menu opens; "The reference itself: nothing to fix" (identity) scores ${m.marks.identity}; then More examples, "Against five readers: a narrow pitch range": ${await textOf(page, '#overall-fig')}, "${await textOf(page, '#summary-line')}", "${await textOf(page, '#reference-mode')}".`;
  },

  // Analyse your reading: the reading, a reference recording, a wrong transcript (refused, with the place), then the right one.
  // A bundled reference takes only its own text and refuses another text without a place, so the reference recording is
  // uploaded: the bundled public-domain Reagan recording, as a file.
  async s11_upload(page, m) {
    const sc = sceneFrames('s11_upload');
    const right = readJSON(path.join(ROOT, 'gallery/index.json')).baseline.text.trim();
    const wrong = right.replace('There are a few favorite windows I have up there that I like to stand and look out of early in the morning.',
      'There is a small garden down there that I like to walk through late in the evening.');
    if (wrong === right) throw new Error('the wrong transcript equals the right one');
    // The box starts empty, as for a reading of the user's own text, so the paste shows.
    await page.evaluate(() => { const box = document.querySelector('#f-text'); box.value = ''; box.dataset.edited = '1'; });
    // The form is the last section; room below it lets the whole form scroll into view.
    await page.addStyleTag({ content: 'footer { padding-bottom: 420px; }' });
    m.pointer = { x: 1000, y: 300 };
    m.key(0, sc.rel(0), [900, 0, MEDIA[0], 600]);
    await m.glideToSelector('#jump-upload', 18);
    await m.holdUntil(20);
    const before = await page.evaluate(() => scrollY);
    await m.click();
    m.clicks[m.clicks.length - 1].push(9);
    // The link jumps to the form at once. The recording holds the page on the pressed button for 0.3 s, then cuts to the form.
    const target = (await page.evaluate(() => scrollY)) + (await belowPlayer(page, '#upload', 8));
    await page.evaluate((y) => scrollTo({ top: y, behavior: 'instant' }), before);
    await m.holdUntil(m.count + 9);
    await page.evaluate((y) => scrollTo({ top: y, behavior: 'instant' }), target);
    m.lastBoxes = -Infinity;
    m.key(0, sc.rel(m.count), await visibleRect(page, await capRect(page, '#upload > summary', '#f-text')), { moveFrames: 1 });
    await m.glideToSelector('#f-audio', sc.word(0, 'For') - 6);
    await m.chooseFile(path.join(AUDIO, READING_WAV));
    await m.glideToSelector('#f-baseline', sc.word(0, 'speech') + 4);
    await m.click();
    await page.selectOption('#f-baseline', '');
    m.key(0, sc.rel(m.count + 1), await visibleRect(page, await capRect(page, '#f-audio', '#f-baseline-audio')), { moveFrames: 12 });
    await m.glideToSelector('#f-baseline-audio', sc.word(0, 'recordings') - 4);
    await m.chooseFile(path.join(AUDIO, REFERENCE_WAV));
    // Room under Analyse for the stages and the two lines of the refusal.
    const by = await page.evaluate(() => Math.max(0, document.querySelector('#submit').getBoundingClientRect().bottom + 170 - innerHeight));
    const roomFrom = m.count;
    await m.scrollBy(by, m.count + 8);
    m.key(0, sc.rel(roomFrom), await visibleRect(page, await capRect(page, '#f-baseline-audio', '#submit')), { moveFrames: 12 });
    await m.glideToSelector('#f-text', Math.max(m.count + 4, sc.word(0, 'transcript') - 2));
    await m.click();
    await page.fill('#f-text', wrong);
    await m.clickAt('#submit', sc.word(0, 'If') - 6, sc.word(0, 'If') - 4);
    const refusal = () => page.evaluate(() => document.querySelector('#stage-msg').textContent.length > 30);
    await m.glideTo({ x: 1000, y: 700 }, m.count + 10);
    await runJob(m, refusal, sc.word(0, 'tells') - 6, { mark: 'refused' });
    m.marks.refusal = await textOf(page, '#stage-msg');
    m.key(0, sc.rel(m.marks.refused), await capRect(page, '#f-text', '#stage-msg'), { moveFrames: 20 });
    const place = m.marks.refusal.match(/at about (\d+) s/);
    if (!place) throw new Error(`the refusal names no place: ${m.marks.refusal}`);
    const whereAt = sc.word(0, 'where') - 6;
    m.callout(0, sc.rel(whereAt), await inkRect(page, '#stage-msg'), `Says where: about ${place[1]} s`, round((sc.end - whereAt - 4) / FPS, 2));
    // The scene ends on the refusal: the narration says nothing about a second run.
    await m.holdUntil(sc.end + 4);
    m.description = `Analyse your reading opens from the header; the pointer chooses ${READING_WAV} as the reading, "Upload my own reference recordings" with ${REFERENCE_WAV}, and pastes the Reagan passage with one sentence changed; Analyse: "${m.marks.refusal}"; the page refuses it, naming the place.`;
  },

  // The same reading graded without a reference: graded on its own, with the rough-check note.
  async s12_no_reference(page, m) {
    const sc = sceneFrames('s12_no_reference');
    m.pointer = { x: 1120, y: 470 };
    m.key(0, sc.rel(0), [900, 0, MEDIA[0], 600]);
    await m.clickAt('#picker-menu > summary', 6, 8);
    await m.holdUntil(10);
    m.key(0, sc.rel(10), await capRect(page, '#chips'), { moveFrames: 14 });
    await m.pick('L3A_self', 26, 29);
    await m.glideTo(OFF, 40);
    m.key(0, sc.rel(40), await capRect(page, '.ring-wrap', '#summary-line', '#regime-badge'), { moveFrames: 24 });
    const itselfAt = sc.word(0, 'grades') - 2;
    const scrollAt = sc.word(0, 'as') - 8;
    m.callout(0, sc.rel(itselfAt), await inkRect(page, '#regime-badge'), 'Against itself', round((scrollAt - itselfAt) / FPS, 2));
    await m.holdUntil(scrollAt);
    await m.scrollBy(await belowPlayer(page, '#ledger', 14), scrollAt + 10);
    const note = await inkRect(page, '#ledger', 'A rough check'), ring = await capRect(page, '.ring-wrap');
    m.key(0, sc.rel(scrollAt), [Math.min(ring[0], note[0]), ring[1], Math.max(ring[2], note[2]), note[3]], { moveFrames: 24 });
    m.callout(0, sc.rel(sc.word(0, 'rough') - 2), note, 'A rough check', round((sc.end - sc.word(0, 'rough') - 4) / FPS, 2));
    await m.holdUntil(sc.end + 4);
    m.description = `The menu opens; "Same reading, no reference" (L3A_self) shows ${await textOf(page, '.ring-wrap')}, "${await textOf(page, '#summary-line')}", badge "${await textOf(page, '#regime-badge')}", and the note "${(await textOf(page, '#ledger')).match(/A rough check[^.]*\.[^.]*\./)?.[0] ?? ''}".`;
  },
};

// ---------------------------------------------------------------------------------------------------- output
function encode(id, motion) {
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS), '-i', path.join(motion.dir, '%05d.jpg'), '-an', '-c:v', 'libvpx-vp9', '-crf', '20', '-b:v', '0', '-row-mt', '1', '-cpu-used', '2', '-pix_fmt', 'yuv420p', path.join(OUT, id + '.webm')]);
}

// The captures.json entry of a scene from its raw recording data.
function captureEntry(id, info) {
  const timing = sceneFrames(id);
  const entry = {
    id, file: `captures/${id}.webm`, durationSec: round(info.frames / FPS), scene: id, description: info.description,
    ...(info.syncFrame != null && timing.clip ? { alignSec: round(timing.clip.from / FPS) } : {}),
    size: MEDIA, camera: fitCamera(info, timing), clicks: info.clicks, sounds: info.sounds,
  };
  entry.callouts = placeLabels(info, timing, entry.camera, info.callouts);
  if (info.syncFrame != null && timing.clip && Math.abs(info.syncFrame - timing.clip.from) > 1) console.warn(`  ${id}: playback starts at frame ${info.syncFrame}, the clip at ${timing.clip.from}`);
  return entry;
}

function writeCaptures(entries) {
  const known = fs.existsSync(CAPTURES_FILE) ? readJSON(CAPTURES_FILE) : [];
  const byId = new Map(known.filter((c) => Object.keys(SHOTS).includes(c.id)).map((c) => [c.id, c]));
  for (const entry of entries) byId.set(entry.id, entry);
  const ordered = Object.keys(SHOTS).filter((id) => byId.has(id)).map((id) => byId.get(id));
  fs.writeFileSync(CAPTURES_FILE, JSON.stringify(ordered, null, 2) + '\n');
}

async function record(port, only) {
  fs.mkdirSync(RAW, { recursive: true });
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required'] });
  const entries = [];
  for (const [id, shot] of Object.entries(SHOTS)) {
    if (only.length && !only.includes(id)) continue;
    const dir = path.join(RAW, id + '_frames');
    fs.rmSync(dir, { recursive: true, force: true });
    fs.mkdirSync(dir, { recursive: true });
    const ctx = await browser.newContext({ viewport: VIEW, deviceScaleFactor: SCALE, colorScheme: 'dark' });
    await ctx.addInitScript(PAGE_SETUP);
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', (message) => { if (message.type() === 'error') errors.push(message.text()); });
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.clock.install();
    const started = Date.now();
    const motion = new StopMotion(page, dir, port);
    motion.syncFrame = null;
    await gateJobs(page, motion);
    await setup(page, port);
    await shot(page, motion);
    await ctx.close();
    encode(id, motion);
    const info = {
      frames: motion.count, syncFrame: motion.syncFrame, description: motion.description, keys: motion.keys, clicks: motion.clicks,
      callouts: motion.callouts, sounds: motion.sounds, marks: motion.marks, boxes: motion.boxes, scrolls: motion.scrolls(), errors,
    };
    fs.rmSync(dir, { recursive: true, force: true });
    fs.writeFileSync(path.join(RAW, id + '.json'), JSON.stringify(info));
    console.log(id, JSON.stringify({ frames: info.frames, marks: info.marks, seconds: Math.round((Date.now() - started) / 1000) }), errors.length ? errors : 'no console errors');
    entries.push(captureEntry(id, info));
    writeCaptures(entries);
  }
  await browser.close();
}

function refit() {
  const entries = [];
  for (const id of Object.keys(SHOTS)) {
    const file = path.join(RAW, id + '.json');
    if (!fs.existsSync(file)) continue;
    console.log(id);
    entries.push(captureEntry(id, readJSON(file)));
  }
  writeCaptures(entries);
}

// ---------------------------------------------------------------------------------------------------- clips
// Runs a fix job of the L3A example on the server and keeps its result and its edited audio.
async function fixJob(port, body, name) {
  const base = `http://127.0.0.1:${port}/`;
  const made = await (await fetch(base + `api/gallery/${EXAMPLE}/fix`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })).json();
  if (!made.job_id) throw new Error(`fix ${name}: ${JSON.stringify(made)}`);
  for (;;) {
    const job = await (await fetch(base + `api/jobs/${made.job_id}`)).json();
    if (job.state === 'error') throw new Error(`fix ${name}: ${job.error}`);
    if (job.state === 'done') {
      const wav = path.join(RAW, `job_${name}.wav`);
      fs.writeFileSync(wav, Buffer.from(await (await fetch(base + job.audio)).arrayBuffer()));
      fs.writeFileSync(path.join(RAW, `job_${name}.json`), JSON.stringify(job, null, 1));
      return { fix: job.fix, wav };
    }
    await wait(500);
  }
}

// Cuts the pieces (source WAV, start s, end s, or a silence of `gap` s) into one 48 kHz mono clip with one gain for all
// pieces, so the takes keep their levels relative to each other; the clip then measures CLIP_LUFS, with its peaks kept
// below -1.5 dBFS.
function cutClip(out, pieces) {
  const inputs = [], filters = [], labels = [];
  pieces.forEach((piece, k) => {
    if (piece.gap) {
      filters.push(`anullsrc=r=${CLIP_RATE}:cl=mono,atrim=duration=${piece.gap}[p${k}]`);
    } else {
      inputs.push('-i', piece.file);
      // fadeOut: seconds of fade at the end of a piece that ends inside speech; 12 ms otherwise, against a click.
      const index = inputs.length / 2 - 1, fade = 0.012, fadeOut = piece.fadeOut ?? fade;
      filters.push(`[${index}:a]atrim=start=${piece.from}:end=${piece.to},asetpts=PTS-STARTPTS,aresample=${CLIP_RATE},aformat=channel_layouts=mono,afade=t=in:d=${fade},afade=t=out:st=${round(piece.to - piece.from - fadeOut, 4)}:d=${fadeOut}[p${k}]`);
    }
    labels.push(`[p${k}]`);
  });
  filters.push(`${labels.join('')}concat=n=${pieces.length}:v=0:a=1[cat]`);
  const raw = out + '.raw.wav';
  execFileSync('ffmpeg', ['-v', 'error', '-y', ...inputs, '-filter_complex', filters.join(';'), '-map', '[cat]', '-ar', String(CLIP_RATE), '-ac', '1', '-c:a', 'pcm_s16le', raw]);
  const measure = (file) => {
    const result = spawnSync('ffmpeg', ['-nostats', '-i', file, '-af', 'ebur128=peak=true', '-f', 'null', '-'], { encoding: 'utf8' });
    const summary = result.stderr.slice(result.stderr.lastIndexOf('Summary:'));
    return { lufs: Number(summary.match(/I:\s+(-?[\d.]+) LUFS/)[1]), peak: Number(summary.match(/Peak:\s+(-?[\d.]+) dBFS/)[1]) };
  };
  const before = measure(raw);
  const gain = CLIP_LUFS - before.lufs;
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', raw, '-af', `volume=${gain.toFixed(2)}dB,alimiter=limit=0.84:level=false:attack=2:release=40`, '-ar', String(CLIP_RATE), '-ac', '1', '-c:a', 'pcm_s16le', out]);
  fs.rmSync(raw);
  const after = measure(out);
  const duration = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out]).toString().trim());
  console.log(`  ${path.basename(out)}: ${duration.toFixed(3)} s, ${after.lufs} LUFS, true peak ${after.peak} dBFS (gain ${gain.toFixed(2)} dB)`);
  return duration;
}

async function makeClips(port) {
  fs.mkdirSync(RAW, { recursive: true });
  fs.mkdirSync(CLIPS, { recursive: true });
  const l3a = path.join(AUDIO, `${EXAMPLE}.wav`), reference = path.join(AUDIO, REFERENCE_WAV);
  const result = readJSON(path.join(ROOT, 'gallery/results', `${EXAMPLE}.json`));
  const rushed = result.flaws[RUSHED.stored], flat = result.flaws[FLAT.stored];
  const rushedJob = await fixJob(port, { finding: RUSHED.stored }, 'rushed');
  const melodyJob = await fixJob(port, { finding: FLAT.stored, pitch_method: 'contour' }, 'melody');
  // The A/B/C player's tracks (app.js fixResult), each with CONTEXT s around the words instead of the page's full second,
  // so the video plays each take once without a long run-up.
  const CONTEXT = 0.4;
  const tracks = (job, f) => {
    const pair = job.fix.listen.find((p) => p.finding === f.id);
    const around = ([a, b]) => [Math.max(0, a - CONTEXT), b + CONTEXT];
    return { yours: around(pair.original), fixed: around(pair.edited), target: around(f.b) };
  };
  // A take of the Rushed finding ends TAKE_TAIL s after the next word that ends a phrase ('Mall'), so it ends in the pause.
  const TAKE_TAIL = 0.2, TAKE_FADE = 0.07, TAKE_GAP = 0.25, CLIP_FADE = 0.05;
  const mall = result.words.find((w) => w.w === 'Mall' && w.p[0] > rushed.p[1]);
  const rushedPair = rushedJob.fix.listen.find((p) => p.finding === rushed.id);
  const shift = rushedPair.edited[1] - rushedPair.original[1];
  const rushedTakes = {
    yours: [rushed.p[0] - CONTEXT, mall.p[1] + TAKE_TAIL],
    fixed: [rushedPair.edited[0] - CONTEXT, mall.p[1] + shift + TAKE_TAIL],
    target: [rushed.b[0] - CONTEXT, mall.b[1] + TAKE_TAIL],
  };
  // The example clip ends after 'Memorial', in the pause before 'But'.
  const memorial = result.words.find((w) => w.w === 'Memorial');
  const melodyTracks = tracks(melodyJob, flat);
  const BOTH_GAP = 0.35;   // app.js BOTH_GAP_MS: the silence between yours and the reference in Listen
  const TAIL = 0.35;
  const plans = {
    s4_listen: { sourceStartSec: 14.3,
      pieces: [{ file: l3a, from: 14.3, to: round(memorial.p[1] + 0.08, 3), fadeOut: CLIP_FADE }] },
    s5_finding: {
      pieces: [{ file: l3a, from: rushed.p[0], to: rushed.p[1], label: 'Yours', fadeOut: CLIP_FADE }, { gap: BOTH_GAP }, { file: reference, from: rushed.b[0], to: rushed.b[1], label: 'Reference', fadeOut: CLIP_FADE }, { gap: TAIL }] },
    s6_hear_fixed: {
      pieces: [{ file: l3a, from: rushedTakes.yours[0], to: rushedTakes.yours[1], label: 'Yours', fadeOut: TAKE_FADE }, { gap: TAKE_GAP },
        { file: rushedJob.wav, from: rushedTakes.fixed[0], to: rushedTakes.fixed[1], label: 'Edited', fadeOut: TAKE_FADE }, { gap: TAKE_GAP },
        { file: reference, from: rushedTakes.target[0], to: rushedTakes.target[1], label: 'Target', fadeOut: TAKE_FADE }, { gap: TAIL }] },
    s7_melody: {
      pieces: [{ file: melodyJob.wav, from: melodyTracks.fixed[0], to: melodyTracks.fixed[1], label: 'Edited' }, { file: l3a, from: melodyTracks.yours[0], to: melodyTracks.yours[1], label: 'Yours' }, { gap: TAIL }] },
  };
  const AFTER_LINE = { s4_listen: 1, s5_finding: 1, s6_hear_fixed: 1, s7_melody: 1 };
  // The caption band stays empty during a clip: the video's pill names the take that plays.
  const updates = {};
  for (const [id, plan] of Object.entries(plans)) {
    const durationSec = cutClip(path.join(CLIPS, `${id}.wav`), plan.pieces);
    let at = 0;
    const segments = [];
    for (const piece of plan.pieces) {
      const length = piece.gap ?? piece.to - piece.from;
      if (piece.label) segments.push({ label: piece.label, startSec: round(at), endSec: round(at + length) });
      at += length;
    }
    updates[id] = { clip: { file: `clips/${id}.wav`, durationSec: round(durationSec), caption: '', ...(segments.length ? { segments } : {}), ...(plan.sourceStartSec ? { sourceStartSec: plan.sourceStartSec } : {}) },
      clipAfterLine: AFTER_LINE[id] };
  }
  // Python writes narration.json as its voice part wrote it (1.0 stays 1.0), so only the clip fields change.
  const merge = 'import json,sys\nf=sys.argv[1]\nd=json.load(open(f))\nu=json.load(sys.stdin)\nfor s in d["scenes"]:\n  s.update(u.get(s["id"],{}))\nopen(f,"w").write(json.dumps(d,indent=2,ensure_ascii=False)+"\\n")\n';
  execFileSync('python3', ['-c', merge, NARRATION_FILE], { input: JSON.stringify(updates) });
  console.log('rushed fix:', rushedJob.fix.fixes.find((x) => x.finding === rushed.id).outcome, rushedJob.fix.score_change, '| melody fix:', melodyJob.fix.fixes.find((x) => x.finding === flat.id).outcome, melodyJob.fix.score_change);
}

const [first, ...rest] = process.argv.slice(2);
const main = first === 'clips' ? () => makeClips(rest[0] || '7871')
  : first === 'refit' ? async () => refit()
    : () => (/^\d+$/.test(first ?? '') ? record(first, rest) : record('7871', process.argv.slice(2)));
main().catch((e) => { console.error(e); process.exit(1); });
