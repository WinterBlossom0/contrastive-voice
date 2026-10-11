import { Audio } from "@remotion/media";
import React, { useMemo } from "react";
import { interpolate, staticFile, useVideoConfig } from "remotion";
import { sceneStarts, speechSpan, type SceneTiming } from "../timeline";

// The bed in use. activeDb: the track's active level, the measure of audioLevel.ts on the mean of its two channels.
// credit: the attribution its licence asks for, shown on the end card (null for a CC0 track); source in public/music/LICENSE.txt.
export const MUSIC: { file: string; activeDb: number; credit: string | null } = {
  file: "music/inspired.mp3",
  activeDb: -14.3,
  credit: "Music: “Inspired”, Kevin MacLeod (incompetech.com), CC BY 4.0",
};
// The music level against the voice level, in dB: clear where nobody speaks, well under the voice, and almost gone
// under the app's own audio in the demo clips, which must be heard clean.
const OPEN_DB = -7;
const UNDER_VOICE_DB = -18;
const UNDER_CLIP_DB = -32;
// Frames: the music is down this long before speech starts and stays down this long after it ends, so a pause shorter
// than both together keeps it down (no pumping); the steps are then smoothed over SMOOTH_FRAMES.
const ATTACK_FRAMES = 8;
const RELEASE_FRAMES = 18;
const SMOOTH_FRAMES = 14;
const FADE_IN_FRAMES = 45;
const FADE_OUT_FRAMES = 75;

const toGain = (db: number) => 10 ** (db / 20);

// The music level against the voice, in dB, for every frame of the video.
const levelsPerFrame = (scenes: SceneTiming[], total: number): Float64Array => {
  const target = new Float64Array(total).fill(OPEN_DB);
  const lower = (from: number, to: number, db: number) => {
    for (let frame = Math.max(0, from - ATTACK_FRAMES); frame < Math.min(total, to + RELEASE_FRAMES); frame += 1) {
      target[frame] = Math.min(target[frame], db);
    }
  };
  const starts = sceneStarts(scenes);
  scenes.forEach((scene, index) => {
    for (const line of scene.lines) {
      const [from, to] = speechSpan(line);
      lower(starts[index] + from, starts[index] + to, UNDER_VOICE_DB);
    }
    if (scene.clip !== null) {
      lower(starts[index] + scene.clip.from, starts[index] + scene.clip.from + scene.clip.durationInFrames, UNDER_CLIP_DB);
    }
  });
  const smooth = new Float64Array(total);
  const half = Math.floor(SMOOTH_FRAMES / 2);
  for (let frame = 0; frame < total; frame += 1) {
    let sum = 0;
    let count = 0;
    for (let k = Math.max(0, frame - half); k <= Math.min(total - 1, frame + half); k += 1) {
      sum += target[k];
      count += 1;
    }
    smooth[frame] = sum / count;
  }
  return smooth;
};

// One continuous bed under the whole video, so no scene change cuts it. A video longer than the track loops it.
export const MusicBed: React.FC<{ scenes: SceneTiming[]; voiceDb: number }> = ({ scenes, voiceDb }) => {
  const { fps } = useVideoConfig();
  const total = scenes.reduce((sum, scene) => sum + scene.durationInFrames, 0);
  const levels = useMemo(() => levelsPerFrame(scenes, total), [scenes, total]);
  if (total === 0) {
    return null;
  }
  return (
    <Audio
      name="Music"
      src={staticFile(MUSIC.file)}
      durationInFrames={total}
      loop
      premountFor={fps}
      volume={(frame) => {
        const index = Math.min(total - 1, Math.max(0, Math.round(frame)));
        const fade = interpolate(frame, [0, FADE_IN_FRAMES, total - FADE_OUT_FRAMES, total], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        return Math.min(1, fade * toGain(voiceDb + levels[index] - MUSIC.activeDb));
      }}
    />
  );
};
