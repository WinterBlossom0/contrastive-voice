import { staticFile } from "remotion";
import captureData from "./data/captures.json";
import narrationData from "./data/narration.json";

export const FPS = 30;

export type NarrationLine = { text: string; file: string; durationSec: number };
// A clip of several takes names each take and its place in the clip, in seconds.
export type ClipSegment = { label: string; startSec: number; endSec: number };
export type NarrationClip = { file: string; durationSec: number; caption: string; segments?: ClipSegment[] };
export type NarrationScene = {
  id: SceneId;
  lines: NarrationLine[];
  clip: NarrationClip | null;
  // The number of lines that play before the clip.
  clipAfterLine?: number;
  gapAfterSec: number;
};
export type Narration = { voice: string; scenes: NarrationScene[] };

export type Capture = {
  id: string;
  file: string;
  durationSec: number;
  scene: SceneId;
  description: string;
  // The capture second at which the dashboard starts the audio that the scene clip contains; the recording waits so both start together.
  alignSec?: number;
  // The first frame of the recording, shown while the recording waits for the clip.
  firstStill?: string;
  // The narration line at which the capture starts; without it, captures share the scene in proportion to their durations.
  atLine?: number;
  playbackRate?: number;
  // The size of the media in capture px; the camera keyframes use the same px.
  size: [number, number];
  camera?: CameraKey[];
};

// The camera shows `rect` = [left, top, right, bottom] of the media in capture px; the browser window takes the shape of the
// rect at the largest size that fits CAPTURE_VIEW. The move starts at narration line `at` (or at the clip) plus `sec`.
export type CameraKey = { at: number | "clip"; sec?: number; rect: [number, number, number, number]; moveFrames?: number };
export type CameraRect = CameraKey["rect"];
export type TimedCameraKey = { frame: number; rect: CameraRect; moveFrames: number };

// The largest page area of the browser window in output px: the frame of CaptureFrame without its title bar.
export const CAPTURE_VIEW = { width: 1760, height: 764 } as const;

// (x, y): the rect centre in capture px; zoom: output px per capture px; view: the window's page area in output px.
export const cameraFromRect = (rect: CameraRect) => {
  const [left, top, right, bottom] = rect;
  const zoom = Math.min(CAPTURE_VIEW.width / (right - left), CAPTURE_VIEW.height / (bottom - top));
  return { x: (left + right) / 2, y: (top + bottom) / 2, zoom, viewWidth: (right - left) * zoom, viewHeight: (bottom - top) * zoom };
};

export const SCENE_IDS = [
  "s1_hook",
  "s2_what",
  "s3_demo_summary",
  "s4_demo_listen",
  "s5_demo_finding",
  "s5b_demo_hear_fixed",
  "s5c_demo_fix_all",
  "s6_demo_clean_and_upload",
  "s6b_demo_no_reference",
  "s7_how",
  "s8_evidence",
  "s9_open",
  "s10_close",
] as const;
export type SceneId = (typeof SCENE_IDS)[number];

export type TimedLine = NarrationLine & { from: number; durationInFrames: number; fileExists: boolean };
export type TimedClip = NarrationClip & { from: number; durationInFrames: number; fileExists: boolean };
export type TimedCapture = Capture & {
  from: number;
  durationInFrames: number;
  fileExists: boolean;
  still: string | null;
  leadFrames: number;
  cameraKeys: TimedCameraKey[];
};

export type SceneTiming = {
  id: SceneId;
  durationInFrames: number;
  lines: TimedLine[];
  clip: TimedClip | null;
  captures: TimedCapture[];
};

export type LaunchVideoProps = { scenes: SceneTiming[] };

export const narration = narrationData as Narration;
export const captures = captureData as Capture[];

const toFrame = (seconds: number) => Math.round(seconds * FPS);
const DEFAULT_MOVE_FRAMES = 30;

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
  try {
    const response = await fetch(staticFile(file), { method: "HEAD", signal });
    return response.ok;
  } catch {
    return false;
  }
};

// Each scene: its lines back to back, the clip (if any) after its cue line, then gapAfterSec of silence.
// Frame positions are rounded from cumulative seconds inside a scene, so rounding never drifts across lines.
export const computeTimeline = async (signal?: AbortSignal): Promise<SceneTiming[]> => {
  const byId = new Map(narration.scenes.map((scene) => [scene.id, scene]));
  const missing = SCENE_IDS.filter((id) => !byId.has(id));
  if (missing.length > 0) {
    throw new Error(`narration.json lacks scenes: ${missing.join(", ")}`);
  }
  const allFiles = [
    ...narration.scenes.flatMap((scene) => [...scene.lines.map((line) => line.file), ...(scene.clip ? [scene.clip.file] : [])]),
    ...captures.map((capture) => capture.file),
  ];
  const existence = new Map(
    await Promise.all(allFiles.map(async (file) => [file, await fileExists(file, signal)] as const)),
  );

  return SCENE_IDS.map((id) => {
    const scene = byId.get(id) as NarrationScene;
    let cursorSec = 0;
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
    cursorSec += scene.gapAfterSec;
    const durationInFrames = Math.max(1, toFrame(cursorSec));

    // Moving captures share the scene in proportion to their own durations, or start at their narration line; a zero-length entry is the still of another.
    const sceneCaptures = captures.filter((capture) => capture.scene === id && capture.durationSec > 0);
    const captureTotalSec = sceneCaptures.reduce((sum, capture) => sum + capture.durationSec, 0);
    const startFrame = (index: number): number => {
      if (index >= sceneCaptures.length) {
        return durationInFrames;
      }
      const atLine = sceneCaptures[index].atLine;
      if (atLine !== undefined) {
        return lines[atLine].from;
      }
      const before = sceneCaptures.slice(0, index).reduce((sum, capture) => sum + capture.durationSec, 0);
      return Math.round((before / captureTotalSec) * durationInFrames);
    };
    const timedCaptures = sceneCaptures.map((capture, index) => {
      const from = startFrame(index);
      const to = startFrame(index + 1);
      const still = captures.find((other) => other.id === `${capture.id}_still` && existence.get(other.file) === true);
      const leadFrames = capture.alignSec !== undefined && clip !== null ? Math.max(0, (clip as TimedClip).from - from - toFrame(capture.alignSec)) : 0;
      const cameraKeys = (capture.camera ?? []).map((key) => {
        if (key.at === "clip" && clip === null) {
          throw new Error(`captures.json: ${capture.id} has a camera key at the clip, but scene ${id} has no clip`);
        }
        const base = key.at === "clip" ? (clip as TimedClip).from : lines[key.at].from;
        return { frame: base + toFrame(key.sec ?? 0), rect: key.rect, moveFrames: key.moveFrames ?? DEFAULT_MOVE_FRAMES };
      });
      return {
        ...capture,
        from,
        durationInFrames: Math.max(1, to - from),
        fileExists: existence.get(capture.file) === true,
        still: still === undefined ? null : still.file,
        leadFrames,
        cameraKeys,
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
  const index = Math.min(beat, scene.lines.length - 1);
  if (beat < scene.lines.length) {
    return scene.lines[index].from;
  }
  // More visual beats than lines: spread the extra beats over the last line.
  const last = scene.lines[index];
  const extra = beat - index;
  return last.from + Math.round((extra * last.durationInFrames) / (extra + 1));
};
