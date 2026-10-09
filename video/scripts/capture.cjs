/* Records the dashboard shots for the launch video, frame by frame, and encodes them for the Remotion project.

     node video/scripts/capture.cjs [PORT] [SHOT ...]   (needs a Chromium: npx playwright-core install chromium-headless-shell, or CHROME_PATH)

   Output in video/public/captures: <id>.webm (30 fps VP9), <id>_first.png and <id>.png (the first and last frames) for each moving shot, and s3_page.png
   (the full L3A page). raw/<id>.json keeps the frame count, the sync second and the element rects (capture px) that the camera
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
const FPS = 30;
const EXAMPLE = 'L3A';
const CLEAN = 'identity';
// The 1920 px layout of the dashboard shows a 1400x750 CSS px page area; CSS zoom 1.6 renders that area at 2240x1200 px.
// A screenshot has the size of the viewport in CSS px, so CSS zoom adds detail where deviceScaleFactor would not change the layout.
const ZOOM = 1.6;
const VIEW = { width: 2240, height: 1200 };

// Mouse events give viewport px, but the pointer element sits inside the zoomed page, so its position is divided by the zoom.
const PAGE_SETUP = `addEventListener('DOMContentLoaded', () => {
  document.documentElement.style.zoom = '${ZOOM}';
  const c = document.createElement('div');
  c.innerHTML = '<svg width="24" height="28" viewBox="0 0 26 30"><path d="M3 2 L3 24 L9 18.5 L13 28 L17 26.3 L13 17 L21 17 Z" fill="#f4f4f6" stroke="#121212" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  Object.assign(c.style, { position: 'fixed', left: '0', top: '0', zIndex: 2147483647, pointerEvents: 'none', transform: 'translate(-100px,-100px)', filter: 'drop-shadow(0 2px 4px rgba(0,0,0,.45))' });
  document.body.append(c);
  addEventListener('mousemove', (e) => { c.style.transform = 'translate(' + (e.clientX / ${ZOOM} - 3) + 'px,' + (e.clientY / ${ZOOM} - 2) + 'px)'; }, true);
});`;

// Rects of these elements, in capture px, go to raw/<id>.json for the camera keyframes.
const RECT_SELECTORS = {
  player: '.player', playAll: '#play-all', ring: '.ring', summary: '.summary-line', picker: '#picker-menu', heroTitle: '.hero h1',
  timeView: '.tl-host', fixesTitle: '.fixes h2', card1: '.top-card.lead', card2: '.top-card:nth-child(2)', card3: '.top-card:nth-child(3)',
  textView: '#text-view', transcript: '#transcript', explain: '#explain', explainHead: '#explain h3', gauge: '#explain .gauge',
  listen: '#explain [data-listen]', fix: '#explain .fix', chips: '#picker-menu[open]', upload: '#upload', submit: '#submit',
  fAudio: '#f-audio', fBaseline: '#f-baseline', fBaselineAudio: '#f-baseline-audio',
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
  }

  file(index) { return path.join(this.dir, String(index).padStart(5, '0') + '.jpg'); }

  async shoot() {
    await this.page.mouse.move(this.pointer.x, this.pointer.y);
    await this.page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))));
    await this.page.screenshot({ path: this.file(this.count), type: 'jpeg', quality: 95 });
    this.count += 1;
  }

  // A still page gives the same picture, so one screenshot fills every frame of the hold.
  async holdUntil(frame) {
    if (this.count >= frame) return;
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
    await wait(1500);
    await page.screenshot({ path: path.join(OUT, 's3_page.png'), fullPage: true });
    return { rects: await page.evaluate((selectors) => {
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
    await motion.holdUntil(scene.lines[1]);
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

  // Scene s5: a flagged word opens its finding; at the clip the pointer presses Listen.
  async finding(page, motion) {
    const scene = sceneFrames('s5_demo_finding');
    await page.goto(URL);
    await ready(page);
    await openExample(page, EXAMPLE);
    await page.click('#transcript .w[data-peek="4"]');
    await scrollToText(page);
    motion.pointer = { x: 760, y: 1050 };
    await motion.holdUntil(8);
    await motion.glideToSelector('#transcript .w[data-peek="2"]', 44);
    await motion.holdUntil(48);
    await motion.click();
    await motion.measure();
    await motion.holdUntil(56);
    await motion.glideTo({ x: 1300, y: 1120 }, 90);
    await motion.holdUntil(scene.clip.from - 40);
    await motion.glideToSelector('#explain [data-listen]', scene.clip.from - 4);
    await motion.holdUntil(scene.clip.from - 1);
    await showPlaying(page, '#explain [data-listen]', true);
    motion.syncFrame = scene.clip.from;
    await motion.holdUntil(scene.clip.from + 6);
    await motion.glideTo({ x: 1420, y: 1150 }, scene.clip.from + 36);
    await motion.holdUntil(scene.clip.to);
    await showPlaying(page, '#explain [data-listen]', false);
    await motion.holdUntil(scene.clip.to + 6);
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
    motion.rectsEnd = await rects(page);
    await motion.holdUntil(motion.count + 4);
    await motion.glideTo({ x: 2150, y: 1150 }, motion.count + 24);
    await motion.holdUntil(scene.lines[2] + 6);
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
    await motion.glideToSelector('#submit', 120);
    motion.rectsEnd = await rects(page);
    await motion.holdUntil(180);
  },
};

function encode(id, motion) {
  const webm = path.join(OUT, id + '.webm');
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS), '-i', path.join(motion.dir, '%05d.jpg'), '-an', '-c:v', 'libvpx-vp9', '-crf', '18', '-b:v', '0', '-row-mt', '1', '-cpu-used', '2', '-pix_fmt', 'yuv420p', webm]);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', motion.file(0), path.join(OUT, id + '_first.png')]);
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
      info = { durationSec: +(motion.count / FPS).toFixed(3), frames: motion.count, alignSec: motion.syncFrame === null ? null : +(motion.syncFrame / FPS).toFixed(3), rects: motion.rects, rectsEnd: motion.rectsEnd ?? null, errors };
    } else {
      info = { ...result, errors };
    }
    fs.rmSync(dir, { recursive: true, force: true });
    fs.writeFileSync(path.join(RAW, id + '.json'), JSON.stringify(info, null, 1));
    console.log(id, JSON.stringify({ frames: info.frames, alignSec: info.alignSec, seconds: Math.round((Date.now() - started) / 1000) }), errors.length ? errors : 'no console errors');
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
