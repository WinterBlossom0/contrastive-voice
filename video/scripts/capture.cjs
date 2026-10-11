/* Records the dashboard shots for the launch video, frame by frame, and encodes them for the Remotion project.

     node video/scripts/capture.cjs [PORT] [SHOT ...]   (needs a Chromium: npx playwright-core install chromium-headless-shell, or CHROME_PATH)

   Output in video/public/captures: <id>.webm (30 fps VP9) and <id>.png (the last frame) for each moving shot, <id>_first.png (the first frame) for
   each shot whose entry in video/src/data/captures.json has a "firstStill", and s3_page.png
   (the full L3A page). The fix shots run real fix jobs on the server; the recording holds the progress line for a fixed time.
   raw/<id>.json also keeps "boxes": every visible text line and control, sampled every BOX_EVERY frames, for
   scripts/check-framing.cjs, which fails a camera view that cuts one of them at its edge. raw/<id>.json keeps the frame count, the sync second and the element rects (capture px) that the camera
   keyframes in video/src/data/captures.json use.

   Stop motion: each output frame is one screenshot after the pointer and the page are set for that frame. A real-time
   screencast drops to about 5 frames per second when other jobs load the CPU, so the shot timing would not be reliable.
   The page runs with reduced motion, so its CSS animations do not move between two screenshots. */
const { chromium } = require('playwright-core');
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

const PORT = process.argv[2] || '7871';
const ONLY = process.argv.slice(3);
const URL = `http://127.0.0.1:${PORT}/`;
const ROOT = path.resolve(__dirname, '../..');
const RAW = path.join(ROOT, 'video/out/capture_raw');
const OUT = path.join(ROOT, 'video/public/captures');
const AUDIO = path.join(ROOT, 'gallery/audio');
const NARRATION = JSON.parse(fs.readFileSync(path.join(ROOT, 'video/src/data/narration.json'), 'utf8'));
// The video shows a first frame only where a capture names it, so other shots get no unused PNG.
const FIRST_STILLS = new Set(JSON.parse(fs.readFileSync(path.join(ROOT, 'video/src/data/captures.json'), 'utf8')).filter((c) => c.firstStill).map((c) => c.id));
const FPS = 30;
const EXAMPLE = 'L3A';
const CLEAN = 'identity';
const NO_REFERENCE = 'L3A_self';
const RUSHED = 2;   // the index of the Rushed finding of the example on the page (findings sorted by time)
// The fix job runs for about ten seconds; the video shows its progress line for this many frames.
const PROGRESS_FRAMES = 30;
const BOX_EVERY = 6;

// Each visible line of text, each control and each drawn waveform as [x, y, width, height, label] in capture px; pageY
// is the viewport offset of a full-page shot. A box under another element (the sticky player bar) is not visible, so it is left out.
const BOX_SCRIPT = (pageY) => {
  const atomic = '#wave, #wave-ref, .tl-host svg, .strip-track, .ring-wrap, .meter';
  const skip = '.horizon, .defs';
  const controls = 'button, input, select, summary, textarea, .chip, a';
  const out = [];
  // A closed <details> keeps a layout box for its content, so elementFromPoint alone would count that content as visible.
  const folded = (owner) => { const closed = owner.closest('details:not([open])'); return !!closed && !owner.closest('summary'); };
  const seen = (r, owner) => {
    if (folded(owner)) return false;
    const left = Math.max(r.left, 0), right = Math.min(r.right, innerWidth), top = Math.max(r.top, 0), bottom = Math.min(r.bottom, innerHeight);
    if (r.width < 1 || r.height < 1 || right <= left || bottom <= top) return false;
    const hit = document.elementFromPoint((left + right) / 2, (top + bottom) / 2);
    return !!hit && (owner.contains(hit) || hit.contains(owner));
  };
  const add = (r, label) => out.push([Math.round(r.left), Math.round(r.top + pageY), Math.round(r.width), Math.round(r.height), label.trim().slice(0, 24)]);
  for (const element of document.querySelectorAll(`${atomic}, ${controls}`)) {
    if (element.closest(skip) || element.parentElement?.closest(atomic)) continue;
    const r = element.getBoundingClientRect();
    if (seen(r, element)) add(r, element.textContent || element.tagName);
  }
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    const owner = node.parentElement;
    if (!node.textContent.trim() || !owner || owner.closest(`${skip}, ${atomic}, ${controls}, script, style`)) continue;
    const range = document.createRange();
    range.selectNodeContents(node);
    for (const r of range.getClientRects()) if (seen(r, owner)) add(r, node.textContent);
  }
  return out;
};
// The 1920 px layout of the dashboard shows a 1400x750 CSS px page area; CSS zoom 1.6 renders that area at 2240x1200 px.
// A screenshot has the size of the viewport in CSS px, so CSS zoom adds detail where deviceScaleFactor would not change the layout.
const ZOOM = 1.6;
const VIEW = { width: 2240, height: 1200 };

// Mouse events give viewport px, but the pointer element sits inside the zoomed page, so its position is divided by the zoom.
const PAGE_SETUP = `addEventListener('DOMContentLoaded', () => {
  document.documentElement.style.zoom = '${ZOOM}';
  const c = document.createElement('div');
  c.innerHTML = '<svg width="24" height="28" viewBox="0 0 26 30"><path d="M3 2 L3 24 L9 18.5 L13 28 L17 26.3 L13 17 L21 17 Z" fill="#ede6da" stroke="#1f1e1d" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  Object.assign(c.style, { position: 'fixed', left: '0', top: '0', zIndex: 2147483647, pointerEvents: 'none', transform: 'translate(-100px,-100px)', filter: 'drop-shadow(0 2px 4px rgba(0,0,0,.45))' });
  document.body.append(c);
  addEventListener('mousemove', (e) => { c.style.transform = 'translate(' + (e.clientX / ${ZOOM} - 3) + 'px,' + (e.clientY / ${ZOOM} - 2) + 'px)'; }, true);
});`;

// Rects of these elements, in capture px, go to raw/<id>.json for the camera keyframes.
const RECT_SELECTORS = {
  player: '.player', playAll: '#play-all', ledger: '#ledger', ring: '.ring-wrap', summary: '.summary-line', kicker: '.sum-text .kicker',
  limit: '#detect-limit', fixAllButton: '#fix-all-btn', picker: '#picker-menu', heroTitle: '.hero h1', heroWave: '#hero-wave',
  timeView: '.tl-stage', strip: '#fault-strip', fixesTitle: '.fixes h2', card1: '.top-card.lead', card2: '.top-card:nth-child(2)', card3: '.top-card:nth-child(3)',
  textView: '#text-view', transcript: '#transcript', explain: '#explain', explainHead: '#explain h3', gauge: '#explain .gauge',
  listen: '#explain [data-listen]', hearFixed: '#explain [data-fix]', fixer: '#explain .fixer', fixHead: '#explain .fix-head',
  fixScore: '#explain .fix-score', fixPlayer: '#explain .abc', fix: '#explain .fix', chips: '#picker-menu[open]',
  fixAll: '#fix-all-body', fixAllScore: '#fix-all-body .fix-all-score', fixList: '#fix-all-body .fix-list',
  upload: '#upload', submit: '#submit', fAudio: '#f-audio', fBaseline: '#f-baseline', fBaselineAudio: '#f-baseline-audio',
};

// Scene line start frames, computed as video/src/timeline.ts computes them.
function sceneFrames(id) {
  const scene = NARRATION.scenes.find((s) => s.id === id);
  const toFrame = (sec) => Math.round(sec * FPS);
  let cursor = 0;
  const lines = [];
  let clip = null;
  scene.lines.forEach((line, index) => {
    lines.push(toFrame(cursor));
    cursor += line.durationSec;
    if (scene.clip && index === scene.clipAfterLine - 1) {
      clip = { from: toFrame(cursor), to: toFrame(cursor + scene.clip.durationSec) };
      cursor += scene.clip.durationSec;
    }
  });
  if (clip) clip.segments = (scene.clip.segments || []).map((seg) => ({ ...seg, from: clip.from + toFrame(seg.startSec), to: clip.from + toFrame(seg.endSec) }));
  return { lines, clip, end: toFrame(cursor + scene.gapAfterSec) };
}

const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

class StopMotion {
  constructor(page, dir) {
    this.page = page;
    this.dir = dir;
    this.count = 0;
    this.pointer = { x: VIEW.width + 50, y: VIEW.height + 50 };
    this.syncFrame = null;
    this.rects = null;
    this.boxes = {};
    this.lastBoxes = -Infinity;
    this.scrolls = [];
  }

  file(index) { return path.join(this.dir, String(index).padStart(5, '0') + '.jpg'); }

  async shoot() {
    await this.page.mouse.move(this.pointer.x, this.pointer.y);
    await this.page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))));
    await this.page.screenshot({ path: this.file(this.count), type: 'jpeg', quality: 95 });
    if (this.count % BOX_EVERY === 0 || this.count - this.lastBoxes >= BOX_EVERY) await this.sampleBoxes();
    this.count += 1;
  }

  async sampleBoxes() {
    this.boxes[this.count] = await this.page.evaluate(BOX_SCRIPT, 0);
    this.lastBoxes = this.count;
  }

  // A still page gives the same picture, so one screenshot fills every frame of the hold.
  async holdUntil(frame) {
    if (this.count >= frame) return;
    this.lastBoxes = -Infinity;
    await this.shoot();
    while (this.count < frame) {
      fs.copyFileSync(this.file(this.count - 1), this.file(this.count));
      this.count += 1;
    }
  }

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

  async click() {
    await this.page.mouse.move(this.pointer.x, this.pointer.y);
    await this.page.mouse.down();
    await this.page.mouse.up();
    await wait(300);
  }

  async measure() { this.rects = await rects(this.page); }

  // Scrolls the page by `by` CSS px over the frames up to endFrame; the pointer keeps its place on the screen.
  async scrollBy(by, endFrame) {
    const from = await this.page.evaluate(() => scrollY);
    const startFrame = this.count;
    this.scrolls.push([startFrame, endFrame]);
    const span = Math.max(1, endFrame - startFrame);
    while (this.count < endFrame) {
      const t = easeInOut((this.count - startFrame + 1) / span);
      await this.page.evaluate((y) => scrollTo(0, y), from + by * t);
      await this.shoot();
    }
  }
}

// The scroll distance that puts the element top `gap` px below the sticky player bar. With CSS zoom on the root, element
// rects and scroll offsets both use capture px.
async function scrollToBelowPlayer(page, selector, gap = 30) {
  return page.evaluate(({ selector, gap }) => {
    const top = document.querySelector(selector).getBoundingClientRect().top;
    const bar = document.querySelector('.player').getBoundingClientRect().bottom;
    return top - bar - gap;
  }, { selector, gap });
}

// Runs a fix job from a button: the progress line shows for PROGRESS_FRAMES, then the recording waits for the result
// without frames, and the page's automatic playback of the edited take stops, so the clip can choose the sides.
async function runFix(page, motion, doneSelector) {
  await motion.click();
  await motion.holdUntil(motion.count + PROGRESS_FRAMES);
  await page.waitForSelector(doneSelector, { timeout: 180000 });
  await page.evaluate(() => S.fix.player?.stop());
  await wait(500);
}

async function center(page, selector) {
  const box = await page.locator(selector).first().boundingBox();
  if (!box) throw new Error(`no box for ${selector}`);
  return { x: box.x + box.width / 2, y: box.y + box.height / 2 };
}

async function ready(page) {
  await page.waitForFunction(() => !document.querySelector('#play-all').disabled && document.querySelectorAll('#transcript .w').length > 0, null, { timeout: 30000 });
}

async function openExample(page, id) {
  const sel = `.chip[data-id="${id}"]`;
  if (!(await page.locator(sel).isVisible())) await page.click('#picker-menu > summary');
  if (!(await page.locator(sel).isVisible())) await page.click('#more-examples > summary');
  await page.click(sel);
  await page.waitForFunction((id) => document.querySelector(`.chip[data-id="${id}"]`)?.getAttribute('aria-pressed') === 'true', id);
  await wait(400);
  await ready(page);
}

// Scrolls so the text view starts just below the sticky player bar.
async function scrollToText(page) {
  await page.evaluate(() => document.querySelector('#text-view').scrollIntoView({ block: 'start' }));
  await page.evaluate(() => scrollBy(0, -110));
  await wait(300);
}

async function rects(page) {
  return page.evaluate((selectors) => {
    const out = {};
    for (const [name, selector] of Object.entries(selectors)) {
      const element = document.querySelector(selector);
      if (!element) continue;
      const r = element.getBoundingClientRect();
      if (r.width === 0) continue;
      out[name] = [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)];
    }
    return out;
  }, RECT_SELECTORS);
}

// The play button and the Listen button show their playing state while the page stays paused between screenshots.
async function showPlaying(page, selector, on) {
  await page.evaluate(({ selector, on }) => {
    const button = document.querySelector(selector);
    button.classList.toggle('playing', on);
    if (selector === '#play-all') button.textContent = on ? 'Pause' : 'Play recording';
  }, { selector, on });
}

const SHOTS = {
  // The full L3A page; scene s3 pans over it.
  async s3_page(page) {
    await page.goto(URL);
    await ready(page);
    // The drawn pointer stays at the top left until a mouse event, so it is moved off the page.
    await page.mouse.move(VIEW.width + 50, VIEW.height + 50);
    await wait(1500);
    await page.screenshot({ path: path.join(OUT, 's3_page.png'), fullPage: true });
    // The full-page screenshot shows the sticky bars only at the top. Below the first viewport they would cover the content
    // under them, so the rest of the page is sampled with them hidden, one viewport at a time.
    const boxes = (await page.evaluate(BOX_SCRIPT, 0)).map((box) => JSON.stringify(box));
    await page.addStyleTag({ content: '.player, header.top { visibility: hidden !important; }' });
    const height = await page.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 600; y < height; y += 600) {
      await page.evaluate((y) => scrollTo(0, y), y);
      await wait(150);
      const pageY = await page.evaluate(() => scrollY);
      for (const box of await page.evaluate(BOX_SCRIPT, pageY)) boxes.push(JSON.stringify(box));
    }
    await page.evaluate(() => scrollTo(0, 0));
    return { boxes: { 0: [...new Set(boxes)].map((box) => JSON.parse(box)) }, rects: await page.evaluate((selectors) => {
      const out = {};
      for (const [name, selector] of Object.entries(selectors)) {
        const r = document.querySelector(selector)?.getBoundingClientRect();
        if (r && r.width > 0) out[name] = [Math.round(r.x), Math.round(r.y + scrollY), Math.round(r.width), Math.round(r.height)];
      }
      return out;
    }, RECT_SELECTORS) };
  },

  // Scene s4: the pointer presses Play, then the word highlight follows the clip second by second.
  async transcript_karaoke(page, motion) {
    const scene = sceneFrames('s4_demo_listen');
    const source = NARRATION.scenes.find((s) => s.id === 's4_demo_listen').clip;
    await page.goto(URL);
    await ready(page);
    await openExample(page, EXAMPLE);
    await scrollToText(page);
    await page.evaluate((sec) => S.ws.setTime(sec), source.sourceStartSec);
    await wait(300);
    await motion.measure();
    // The pointer waits in the player bar, so its path to Play does not cross the transcript and light words on hover.
    motion.pointer = { x: 1150, y: 150 };
    await motion.holdUntil(Math.max(12, scene.clip.from - 60));
    await motion.glideToSelector('#play-all', scene.clip.from - 8);
    await motion.holdUntil(scene.clip.from - 2);
    await showPlaying(page, '#play-all', true);
    motion.syncFrame = scene.clip.from;
    const away = { x: 1000, y: 1130 };
    const from = { ...motion.pointer };
    for (let frame = motion.count; frame < scene.clip.to; frame++) {
      const sec = source.sourceStartSec + (frame - scene.clip.from) / FPS;
      await page.evaluate((sec) => S.ws.setTime(sec), Math.max(source.sourceStartSec, sec));
      await page.waitForFunction((text) => document.querySelector('#clock').textContent.startsWith(text), Math.max(source.sourceStartSec, sec).toFixed(2), { timeout: 1000 }).catch(() => {});
      const t = easeInOut(Math.min(1, Math.max(0, (frame - scene.clip.from) / 30)));
      motion.pointer = { x: from.x + (away.x - from.x) * t, y: from.y + (away.y - from.y) * t };
      await motion.shoot();
    }
    await showPlaying(page, '#play-all', false);
    await motion.holdUntil(scene.clip.to + 6);
  },

  // Scene s5: a flagged word opens its finding.
  async finding(page, motion) {
    const scene = sceneFrames('s5_demo_finding');
    await page.goto(URL);
    await ready(page);
    await openExample(page, EXAMPLE);
    await page.click('#transcript .w[data-peek="4"]');
    await scrollToText(page);
    motion.pointer = { x: 760, y: 1050 };
    await motion.holdUntil(8);
    await motion.glideToSelector(`#transcript .w[data-peek="${RUSHED}"]`, 44);
    await motion.holdUntil(48);
    await motion.click();
    await scrollToText(page);
    await motion.measure();
    await motion.holdUntil(56);
    await motion.glideTo({ x: 1300, y: 1120 }, 90);
    await motion.holdUntil(scene.end + 4);
  },

  // Scene s5b: "Hear it fixed" on the Rushed finding, then Yours, Edited and Target in step with the clip.
  async hear_fixed(page, motion) {
    const scene = sceneFrames('s5b_demo_hear_fixed');
    await page.goto(URL);
    await ready(page);
    await openExample(page, EXAMPLE);
    await page.click(`#transcript .w[data-peek="${RUSHED}"]`);
    await scrollToText(page);
    await motion.measure();
    motion.pointer = { x: 1300, y: 1120 };
    await motion.holdUntil(10);
    await motion.glideToSelector('#explain [data-fix]', 40);
    await motion.holdUntil(44);
    await runFix(page, motion, '#explain .fixer .abc');
    // The whole fix result comes into view under the player bar, with the Hear it fixed button above it.
    const by = await scrollToBelowPlayer(page, '#explain .fixer', 160);
    await motion.holdUntil(motion.count + 6);
    await motion.glideTo({ x: 2150, y: 1150 }, motion.count + 14);
    await motion.scrollBy(by, motion.count + 26);
    motion.rectsEnd = await rects(page);
    const sides = { Yours: 'yours', Edited: 'fixed', Target: 'target' };
    for (const seg of scene.clip.segments) {
      const button = `#explain .fixer .abc [data-side="${sides[seg.label]}"]`;
      if (motion.count < seg.from - 14) {
        await motion.holdUntil(seg.from - 14);
      }
      await motion.glideToSelector(button, seg.from - 1);
      await motion.click();
      if (seg.label === 'Yours') motion.syncFrame = seg.from;
      await motion.holdUntil(seg.from + 3);
    }
    await motion.holdUntil(scene.clip.to - 12);
    await motion.glideToSelector('#explain .fixer .loop-btn', scene.clip.to);
    await motion.click();
    await motion.holdUntil(scene.clip.to + 4);
    await motion.glideTo({ x: 2150, y: 1150 }, scene.clip.to + 30);
    await motion.holdUntil(scene.end + 4);
  },

  // Scene s5c: "Fix everything and listen" on the whole reading, then the list of what each fix did.
  async fix_all(page, motion) {
    const scene = sceneFrames('s5c_demo_fix_all');
    await page.goto(URL);
    await ready(page);
    await openExample(page, EXAMPLE);
    await page.evaluate((y) => scrollTo(0, y), await scrollToBelowPlayer(page, '#ledger', 40));
    await wait(300);
    await motion.measure();
    motion.pointer = { x: 1500, y: 1120 };
    await motion.holdUntil(6);
    await motion.glideToSelector('#fix-all-btn', 34);
    await motion.holdUntil(38);
    await runFix(page, motion, '#fix-all-body .fix-all-score');
    await motion.holdUntil(motion.count + 4);
    await motion.glideTo({ x: 1900, y: 1150 }, motion.count + 12);
    await motion.scrollBy(await scrollToBelowPlayer(page, '#fix-all-body', 30), motion.count + 28);
    motion.rectsMid = await rects(page);
    await motion.holdUntil(Math.max(motion.count, scene.lines[1] - 22));
    await motion.glideToSelector('#fix-all-body .fix-list > summary', scene.lines[1] + 2);
    await motion.click();
    await motion.holdUntil(scene.lines[1] + 6);
    await motion.glideTo({ x: 2150, y: 1150 }, scene.lines[1] + 30);
    motion.rectsEnd = await rects(page);
    await motion.holdUntil(scene.end + 4);
  },

  // Scene s6, first part: the example menu opens and the placebo copy loads; a full score and no flags.
  async clean(page, motion) {
    const scene = sceneFrames('s6_demo_clean_and_upload');
    await page.goto(URL);
    await ready(page);
    motion.pointer = { x: 1500, y: 420 };
    await motion.holdUntil(6);
    await motion.glideToSelector('#picker-menu > summary', 30);
    await motion.holdUntil(34);
    await motion.click();
    const chip = `.chip[data-id="${CLEAN}"]`;
    if (!(await page.locator(chip).isVisible())) {
      await motion.holdUntil(42);
      await motion.glideToSelector('#more-examples > summary', 60);
      await motion.holdUntil(63);
      await motion.click();
    }
    await motion.measure();
    await motion.holdUntil(motion.count + 6);
    await motion.glideToSelector(chip, motion.count + 26);
    await motion.holdUntil(motion.count + 4);
    await motion.click();
    await page.waitForFunction((id) => document.querySelector(`.chip[data-id="${id}"]`)?.getAttribute('aria-pressed') === 'true', CLEAN);
    await ready(page);
    await wait(600);
    await motion.holdUntil(motion.count + 4);
    await motion.glideTo({ x: 2150, y: 1150 }, motion.count + 20);
    await motion.scrollBy(await scrollToBelowPlayer(page, '#ledger', 40), motion.count + 24);
    motion.rectsEnd = await rects(page);
    await motion.holdUntil(scene.lines[1] + 6);
  },

  // Scene s6, second part: the upload form with your reading and your own reference reading chosen; nothing is submitted.
  async upload(page, motion) {
    await page.goto(URL);
    await ready(page);
    // The form is the last section, so extra room below it lets the whole form scroll into view.
    await page.addStyleTag({ content: 'footer { padding-bottom: 420px; }' });
    await page.evaluate(() => { document.querySelector('#upload').open = true; });
    await page.evaluate(() => document.querySelector('.upload-wrap').scrollIntoView({ block: 'start' }));
    await page.evaluate(() => scrollBy(0, -90));
    await wait(400);
    await motion.measure();
    motion.pointer = { x: 1500, y: 1100 };
    await motion.holdUntil(4);
    await motion.glideToSelector('#f-audio', 24);
    await page.setInputFiles('#f-audio', path.join(AUDIO, `${EXAMPLE}.wav`));
    await motion.holdUntil(34);
    await motion.glideToSelector('#f-baseline', 52);
    await page.selectOption('#f-baseline', '');
    await motion.holdUntil(62);
    await motion.glideToSelector('#f-baseline-audio', 80);
    await page.setInputFiles('#f-baseline-audio', path.join(AUDIO, 'reagan_farewell_1989.wav'));
    await motion.holdUntil(92);
    // The reference file field makes the form taller, so the page scrolls until the Analyse button is in view.
    await motion.scrollBy(await page.evaluate(() => Math.max(0, document.querySelector('#submit').getBoundingClientRect().bottom - 1130)), 112);
    await motion.glideToSelector('#submit', 135);
    motion.rectsEnd = await rects(page);
    await motion.holdUntil(180);
  },

  // Scene s6b: the same reading graded without a reference, chosen from the example menu.
  async no_reference(page, motion) {
    const scene = sceneFrames('s6b_demo_no_reference');
    await page.goto(URL);
    await ready(page);
    motion.pointer = { x: 1500, y: 420 };
    await motion.holdUntil(6);
    await motion.glideToSelector('#picker-menu > summary', 30);
    await motion.holdUntil(34);
    await motion.click();
    const chip = `.chip[data-id="${NO_REFERENCE}"]`;
    await motion.measure();
    await motion.holdUntil(motion.count + 6);
    await motion.glideToSelector(chip, motion.count + 24);
    await motion.holdUntil(motion.count + 4);
    await motion.click();
    await page.waitForFunction((id) => document.querySelector(`.chip[data-id="${id}"]`)?.getAttribute('aria-pressed') === 'true', NO_REFERENCE);
    await ready(page);
    await wait(800);
    await motion.holdUntil(motion.count + 4);
    await motion.glideTo({ x: 2150, y: 1150 }, motion.count + 20);
    await motion.scrollBy(await scrollToBelowPlayer(page, '#ledger', 40), motion.count + 24);
    motion.rectsEnd = await rects(page);
    await motion.holdUntil(scene.end + 4);
  },
};

function encode(id, motion) {
  const webm = path.join(OUT, id + '.webm');
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS), '-i', path.join(motion.dir, '%05d.jpg'), '-an', '-c:v', 'libvpx-vp9', '-crf', '18', '-b:v', '0', '-row-mt', '1', '-cpu-used', '2', '-pix_fmt', 'yuv420p', webm]);
  if (FIRST_STILLS.has(id)) execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', motion.file(0), path.join(OUT, id + '_first.png')]);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', motion.file(motion.count - 1), path.join(OUT, id + '.png')]);
}

(async () => {
  fs.mkdirSync(RAW, { recursive: true });
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}), args: ['--no-sandbox'] });
  for (const [id, shot] of Object.entries(SHOTS)) {
    if (ONLY.length && !ONLY.includes(id)) continue;
    const dir = path.join(RAW, id + '_frames');
    fs.rmSync(dir, { recursive: true, force: true });
    fs.mkdirSync(dir, { recursive: true });
    const ctx = await browser.newContext({ viewport: VIEW, deviceScaleFactor: 1, colorScheme: 'dark', reducedMotion: 'reduce' });
    await ctx.addInitScript(PAGE_SETUP);
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', (e) => errors.push(String(e)));
    const started = Date.now();
    const motion = new StopMotion(page, dir);
    const result = await shot(page, motion);
    await ctx.close();
    let info;
    if (motion.count > 0) {
      encode(id, motion);
      info = { durationSec: +(motion.count / FPS).toFixed(3), frames: motion.count, alignSec: motion.syncFrame === null ? null : +(motion.syncFrame / FPS).toFixed(3), rects: motion.rects, rectsMid: motion.rectsMid ?? null, rectsEnd: motion.rectsEnd ?? null, boxes: motion.boxes, scrolls: motion.scrolls, errors };
    } else {
      info = { ...result, errors };
    }
    fs.rmSync(dir, { recursive: true, force: true });
    fs.writeFileSync(path.join(RAW, id + '.json'), JSON.stringify(info, null, 1));
    console.log(id, JSON.stringify({ frames: info.frames, alignSec: info.alignSec, seconds: Math.round((Date.now() - started) / 1000) }), errors.length ? errors : 'no console errors');
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
