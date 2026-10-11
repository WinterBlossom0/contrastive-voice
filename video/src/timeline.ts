import { staticFile } from "remotion";
import captureData from "./data/captures.json";
import narrationData from "./data/narration.json";
import { SCRIPT } from "./script";

export const FPS = 30;

export const SCENE_IDS = [
  "s1_hook",
  "s2_what",
  "s3_open_example",
  "s4_listen",
  "s5_finding",
  "s6_hear_fixed",
  "s7_melody",
  "s8_fix_all",
  "s9_text_lists",
  "s10_fair",
  "s11_upload",
  "s12_no_reference",
  "s13_how",
  "s14_evidence",
  "s15_open",
  "s16_close",
] as const;
export type SceneId = (typeof SCENE_IDS)[number];

// [word, startSec, endSec]; seconds from the start of the line's own audio file.
export type WordTiming = [string, number, number];
export type NarrationLine = { text: string; file: string; durationSec: number; words?: WordTiming[] };
// A clip of several takes names each take and its place in the clip, in seconds.
export type ClipSegment = { label: string; startSec: number; endSec: number };
export type NarrationClip = { file: string; durationSec: number; caption: string; segments?: ClipSegment[] };
export type NarrationScene = {
  id: string;
  lines: NarrationLine[];
  clip: NarrationClip | null;
  // The number of lines that play before the clip.
  clipAfterLine?: number;
  gapAfterSec: number;
};
export type Narration = { voice: string; scenes: NarrationScene[] };

// The camera shows `rect` = [left, top, right, bottom] of the media in capture px; the browser window takes the shape of the
// rect at the largest size that fits CAPTURE_VIEW. The move starts at narration line `at` (or at the clip) plus `sec`.
export type CameraRect = [number, number, number, number];
export type CameraKey = { at: number | "clip"; sec?: number; rect: CameraRect; moveFrames?: number };
// A ripple at capture frame `frame` (30 fps frames of the recording) at (x, y) in capture px.
export type ClickSpec = [number, number, number];
export type CalloutSpec = { at: number | "clip"; sec?: number; durSec?: number; rect: CameraRect; text: string };
// A sound effect at capture frame `frame` (30 fps frames of the recording), for a moment that only the recording shows,
// such as the score ring counting up ("rise") or a fix result appearing ("chime").
export const CAPTURE_SOUNDS = ["click", "pop", "rise", "chime"] as const;
export type CaptureSound = (typeof CAPTURE_SOUNDS)[number];
export type SoundSpec = [number, CaptureSound];

export type Capture = {
  id: string;
  file: string;
  durationSec: number;
  scene: string;
  description: string;
  // The capture second at which the dashboard starts the audio that the scene clip contains; the recording waits so both start together.
  alignSec?: number;
  // The first frame of the recording, shown while the recording waits for the clip.
  firstStill?: string;
  // The narration line at which the capture starts; without it, captures share the scene in proportion to their durations.
  atLine?: number;
  playbackRate?: number;
  // The size of the media in capture px; camera keys, clicks and callouts use the same px.
  size: [number, number];
  camera?: CameraKey[];
  clicks?: ClickSpec[];
  callouts?: CalloutSpec[];
  sounds?: SoundSpec[];
};

export type TimedCameraKey = { frame: number; rect: CameraRect; moveFrames: number };
export type TimedClick = { frame: number; x: number; y: number };
export type TimedCallout = { from: number; durationInFrames: number; rect: CameraRect; text: string };
export type TimedSound = { frame: number; sound: CaptureSound };

// The largest page area of the browser window in output px: the frame of CaptureFrame without its title bar.
export const CAPTURE_VIEW = { width: 1760, height: 764 } as const;

// (x, y): the rect centre in capture px; zoom: output px per capture px; view: the window's page area in output px.
export const cameraFromRect = (rect: CameraRect) => {
  const [left, top, right, bottom] = rect;
  const zoom = Math.min(CAPTURE_VIEW.width / (right - left), CAPTURE_VIEW.height / (bottom - top));
  return { x: (left + right) / 2, y: (top + bottom) / 2, zoom, viewWidth: (right - left) * zoom, viewHeight: (bottom - top) * zoom };
};

export type TimedLine = NarrationLine & { from: number; durationInFrames: number; fileExists: boolean };
export type TimedClip = NarrationClip & { from: number; durationInFrames: number; fileExists: boolean };
export type TimedCapture = Capture & {
  from: number;
  durationInFrames: number;
  fileExists: boolean;
  still: string | null;
  leadFrames: number;
  cameraKeys: TimedCameraKey[];
  clickFrames: TimedClick[];
  timedCallouts: TimedCallout[];
  soundFrames: TimedSound[];
};

export type SceneTiming = {
  id: SceneId;
  durationInFrames: number;
  lines: TimedLine[];
  clip: TimedClip | null;
  captures: TimedCapture[];
};

// voiceDb: the active level of the narration (audioLevel.ts); music and sound effects are set against it.
export type LaunchVideoProps = { scenes: SceneTiming[]; voiceDb: number };

// Through unknown: the JSON infers arrays where the types name tuples (word times, clicks, sounds).
const narration = narrationData as unknown as Narration;
const captures = captureData as unknown as Capture[];

export const toFrame = (seconds: number) => Math.round(seconds * FPS);
const DEFAULT_MOVE_FRAMES = 30;
// The pace of the narration voice, for scenes without audio yet.
const ESTIMATE_WORDS_PER_SEC = 2.6;
const ESTIMATE_GAP_SEC = 0.7;
const ESTIMATE_CLIP_SEC = 6;
// The closing scene holds the name on screen after the last line, then fades to black.
const CLOSE_HOLD_SEC = 2.5;
// The opening scene shows the landscape rising for this long before the first line.
const OPEN_LEAD_SEC = 1.5;
// A callout without durSec stays to the end of its line, but at least this long.
const CALLOUT_MIN_SEC = 2.5;

const normalized = (text: string) => text.toLowerCase().replace(/[^a-z0-9]/g, "");

// A scene of narration.json counts only if its lines say the script's words; an older narration of the same id does not.
const matchesScript = (scene: NarrationScene): boolean => {
  const script = SCRIPT.find((entry) => entry.id === scene.id);
  if (script === undefined || script.lines.length !== scene.lines.length) {
    return false;
  }
  return script.lines.every((line, index) => normalized(line) === normalized(scene.lines[index].text));
};

const estimatedScene = (id: SceneId): NarrationScene => {
  const script = SCRIPT.find((entry) => entry.id === id);
  if (script === undefined) {
    throw new Error(`script.ts lacks scene ${id}`);
  }
  return {
    id,
    lines: script.lines.map((text) => ({ text, file: "", durationSec: Math.max(1.4, text.split(/\s+/).length / ESTIMATE_WORDS_PER_SEC) })),
    clip: script.clipAfterLine === undefined ? null : { file: "", durationSec: ESTIMATE_CLIP_SEC, caption: "" },
    clipAfterLine: script.clipAfterLine,
    gapAfterSec: ESTIMATE_GAP_SEC,
  };
};

const clipLineIndex = (scene: NarrationScene): number => {
  if (scene.clip === null) {
    return -1;
  }
  if (scene.clipAfterLine === undefined) {
    throw new Error(`narration.json: scene ${scene.id} has a clip but no clipAfterLine`);
  }
  return scene.clipAfterLine - 1;
};

const fileExists = async (file: string, signal?: AbortSignal): Promise<boolean> => {
  if (file.length === 0) {
    return false;
  }
  try {
    const response = await fetch(staticFile(file), { method: "HEAD", signal });
    return response.ok;
  } catch {
    return false;
  }
};

// The frame at which line `at` (or the clip) starts, plus `sec`. An index past the last line uses the last line.
const anchorFrame = (lines: TimedLine[], clip: TimedClip | null, at: number | "clip", sec: number | undefined): number => {
  const offset = toFrame(sec ?? 0);
  if (at === "clip") {
    return (clip === null ? 0 : clip.from) + offset;
  }
  if (lines.length === 0) {
    return offset;
  }
  return lines[Math.min(Math.max(0, at), lines.length - 1)].from + offset;
};

const anchorEnd = (lines: TimedLine[], clip: TimedClip | null, at: number | "clip"): number => {
  if (at === "clip") {
    return clip === null ? 0 : clip.from + clip.durationInFrames;
  }
  const line = lines[Math.min(Math.max(0, at), lines.length - 1)];
  return line === undefined ? 0 : line.from + line.durationInFrames;
};

// Each scene: its lines back to back, the clip (if any) after its cue line, then gapAfterSec of silence.
// Frame positions are rounded from cumulative seconds inside a scene, so rounding never drifts across lines.
export const computeTimeline = async (signal?: AbortSignal): Promise<SceneTiming[]> => {
  const narrated = new Map(narration.scenes.filter(matchesScript).map((scene) => [scene.id, scene]));
  const estimatedIds = SCENE_IDS.filter((id) => !narrated.has(id));
  if (estimatedIds.length > 0) {
    console.warn(`narration.json lacks scenes that match the script; estimated lengths for: ${estimatedIds.join(", ")}`);
  }
  const sceneCaptures = captures.filter((capture) => (SCENE_IDS as readonly string[]).includes(capture.scene));
  const allFiles = [
    ...[...narrated.values()].flatMap((scene) => [...scene.lines.map((line) => line.file), ...(scene.clip ? [scene.clip.file] : [])]),
    ...sceneCaptures.map((capture) => capture.file),
  ];
  const existence = new Map(await Promise.all(allFiles.map(async (file) => [file, await fileExists(file, signal)] as const)));

  return SCENE_IDS.map((id) => {
    const scene = narrated.get(id) ?? estimatedScene(id);
    let cursorSec = id === SCENE_IDS[0] ? OPEN_LEAD_SEC : 0;
    const lines: TimedLine[] = [];
    let clip: TimedClip | null = null;
    const clipAfter = clipLineIndex(scene);
    scene.lines.forEach((line, index) => {
      const from = toFrame(cursorSec);
      cursorSec += line.durationSec;
      lines.push({ ...line, from, durationInFrames: toFrame(cursorSec) - from, fileExists: existence.get(line.file) === true });
      if (index === clipAfter && scene.clip !== null) {
        const clipFrom = toFrame(cursorSec);
        cursorSec += scene.clip.durationSec;
        clip = { ...scene.clip, from: clipFrom, durationInFrames: toFrame(cursorSec) - clipFrom, fileExists: existence.get(scene.clip.file) === true };
      }
    });
    cursorSec += scene.gapAfterSec + (id === SCENE_IDS[SCENE_IDS.length - 1] ? CLOSE_HOLD_SEC : 0);
    const durationInFrames = Math.max(1, toFrame(cursorSec));

    // Moving captures share the scene in proportion to their own durations, or start at their narration line; a zero-length entry is the still of another.
    const moving = sceneCaptures.filter((capture) => capture.scene === id && capture.durationSec > 0);
    const captureTotalSec = moving.reduce((sum, capture) => sum + capture.durationSec, 0);
    const startFrame = (index: number): number => {
      if (index >= moving.length) {
        return durationInFrames;
      }
      const atLine = moving[index].atLine;
      if (atLine !== undefined) {
        return anchorFrame(lines, clip, atLine, 0);
      }
      const before = moving.slice(0, index).reduce((sum, capture) => sum + capture.durationSec, 0);
      return Math.round((before / captureTotalSec) * durationInFrames);
    };
    const timedCaptures = moving.map((capture, index): TimedCapture => {
      const from = startFrame(index);
      const to = startFrame(index + 1);
      const still = sceneCaptures.find((other) => other.id === `${capture.id}_still` && existence.get(other.file) === true);
      const leadFrames = capture.alignSec !== undefined && clip !== null ? Math.max(0, (clip as TimedClip).from - from - toFrame(capture.alignSec)) : 0;
      const rate = capture.playbackRate ?? 1;
      const cameraKeys = (capture.camera ?? []).map((key) => ({
        frame: anchorFrame(lines, clip, key.at, key.sec),
        rect: key.rect,
        moveFrames: key.moveFrames ?? DEFAULT_MOVE_FRAMES,
      }));
      // A frame of the recording to a frame of the scene: the recording starts after its lead and plays at its rate.
      const captureFrame = (frame: number) => from + leadFrames + Math.round(frame / rate);
      const clickFrames = (capture.clicks ?? []).map(([frame, x, y]) => ({ frame: captureFrame(frame), x, y }));
      const soundFrames = (capture.sounds ?? [])
        .filter(([, sound]) => (CAPTURE_SOUNDS as readonly string[]).includes(sound))
        .map(([frame, sound]) => ({ frame: captureFrame(frame), sound }));
      const timedCallouts = (capture.callouts ?? []).map((callout) => {
        const start = anchorFrame(lines, clip, callout.at, callout.sec);
        const end = callout.durSec === undefined ? Math.max(anchorEnd(lines, clip, callout.at), start + toFrame(CALLOUT_MIN_SEC)) : start + toFrame(callout.durSec);
        return { from: start, durationInFrames: Math.max(1, end - start), rect: callout.rect, text: callout.text };
      });
      return {
        ...capture,
        from,
        durationInFrames: Math.max(1, to - from),
        fileExists: existence.get(capture.file) === true,
        still: still === undefined ? null : still.file,
        leadFrames,
        cameraKeys,
        clickFrames,
        timedCallouts,
        soundFrames,
      };
    });

    return { id, durationInFrames, lines, clip, captures: timedCaptures };
  });
};

// The frame at which the n-th narration line starts; scenes use it to time their visual beats to the voice.
export const beatFrame = (scene: SceneTiming, beat: number): number => {
  if (scene.lines.length === 0) {
    return Math.round((beat * scene.durationInFrames) / 4);
  }
  if (beat < scene.lines.length) {
    return scene.lines[beat].from;
  }
  const last = scene.lines[scene.lines.length - 1];
  return last.from + last.durationInFrames;
};

// The frame of the whole video at which each scene starts: scenes follow one another, and cuts take no time from them.
export const sceneStarts = (scenes: SceneTiming[]): number[] => {
  const starts: number[] = [];
  let sum = 0;
  for (const scene of scenes) {
    starts.push(sum);
    sum += scene.durationInFrames;
  }
  return starts;
};

// The frames of a line where the voice speaks: from its first spoken word to its last when narration.json gives word
// times, otherwise the whole line.
export const speechSpan = (line: TimedLine): [number, number] => {
  const words = line.words ?? [];
  if (words.length === 0) {
    return [line.from, line.from + line.durationInFrames];
  }
  return [line.from + Math.round(words[0][1] * FPS), line.from + Math.round(words[words.length - 1][2] * FPS)];
};
