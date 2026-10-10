/* Fails when a held camera view of video/src/data/captures.json cuts a text line, a control or a waveform at its edge.

     node video/scripts/check-framing.cjs                 check every capture; exit code 1 on a fault
     node video/scripts/check-framing.cjs ID FRAME        list the boxes of capture ID at its own FRAME (for choosing rects)

   The boxes come from video/out/capture_raw/<id>.json (scripts/capture.cjs). A view is held from the end of its camera move
   to the start of the next one; frames in which the page scrolls are skipped, because there the content moves past the edge
   on purpose. Scene timing follows video/src/timeline.ts. */
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const FPS = 30;
const DEFAULT_MOVE_FRAMES = 30;
// A box that is inside the view must keep this many capture px from the view edge.
const INSET = 4;
const narration = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/data/narration.json'), 'utf8'));
const captures = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/data/captures.json'), 'utf8'));
const toFrame = (sec) => Math.round(sec * FPS);

function sceneTiming(id) {
  const scene = narration.scenes.find((s) => s.id === id);
  let cursor = 0;
  const lines = [];
  let clip = null;
  scene.lines.forEach((line, index) => {
    lines.push(toFrame(cursor));
    cursor += line.durationSec;
    if (scene.clip && index === scene.clipAfterLine - 1) {
      clip = toFrame(cursor);
      cursor += scene.clip.durationSec;
    }
  });
  return { lines, clip, end: Math.max(1, toFrame(cursor + scene.gapAfterSec)) };
}

const raw = (id) => JSON.parse(fs.readFileSync(path.join(ROOT, 'out/capture_raw', `${id}.json`), 'utf8'));

// The latest box sample at or before the capture frame.
function boxesAt(info, frame) {
  const frames = Object.keys(info.boxes).map(Number).filter((f) => f <= frame).sort((a, b) => a - b);
  return info.boxes[frames.length ? frames[frames.length - 1] : Math.min(...Object.keys(info.boxes).map(Number))];
}

function faults(rect, boxes) {
  const [left, top, right, bottom] = rect;
  return boxes.filter(([x, y, w, h]) => {
    const meets = x < right && x + w > left && y < bottom && y + h > top;
    const inside = x >= left + INSET && x + w <= right - INSET && y >= top + INSET && y + h <= bottom - INSET;
    return meets && !inside;
  });
}

function check() {
  let failures = 0;
  for (const capture of captures.filter((c) => c.durationSec > 0)) {
    const timing = sceneTiming(capture.scene);
    const siblings = captures.filter((c) => c.scene === capture.scene && c.durationSec > 0);
    const from = timing.lines[capture.atLine];
    const next = siblings[siblings.indexOf(capture) + 1];
    const to = next ? timing.lines[next.atLine] : timing.end;
    const info = raw(capture.id);
    const keys = capture.camera.map((key) => ({ ...key, frame: (key.at === 'clip' ? timing.clip : timing.lines[key.at]) + toFrame(key.sec ?? 0) }));
    const [width, height] = capture.size;
    keys.forEach((key, index) => {
      const [left, top, right, bottom] = key.rect;
      if (left < 0 || top < 0 || right > width || bottom > height || right <= left || bottom <= top) {
        console.log(`FAIL ${capture.id} key ${index}: rect ${key.rect} leaves the media ${width}x${height}`);
        failures += 1;
      }
      const holdFrom = Math.max(from, index === 0 ? from : key.frame + (key.moveFrames ?? DEFAULT_MOVE_FRAMES));
      const holdTo = index + 1 < keys.length ? keys[index + 1].frame : to;
      const samples = new Set();
      for (let frame = holdFrom; frame < holdTo; frame += 1) {
        const own = Math.min(frame - from, (info.frames ?? 1) - 1);
        if ((info.scrolls ?? []).some(([a, b]) => own >= a && own < b)) continue;
        samples.add(info.frames === undefined ? 0 : Math.max(0, own));
      }
      const cut = new Map();
      for (const own of samples) for (const box of faults(key.rect, boxesAt(info, own))) cut.set(box.slice(0, 4).join(','), [own, box]);
      if (cut.size) {
        failures += 1;
        console.log(`FAIL ${capture.id} key ${index} (scene frames ${holdFrom}-${holdTo}): ${cut.size} cut boxes`);
        for (const [own, box] of [...cut.values()].slice(0, 8)) console.log(`     capture frame ${own}: ${JSON.stringify(box)}`);
      }
    });
  }
  console.log(failures ? `${failures} framing faults` : 'framing: no cut text or controls in any held view');
  process.exit(failures ? 1 : 0);
}

if (process.argv.length > 3) {
  const [id, frame] = process.argv.slice(2);
  for (const box of [...boxesAt(raw(id), Number(frame))].sort((a, b) => a[1] - b[1] || a[0] - b[0])) console.log(JSON.stringify(box));
} else {
  check();
}
