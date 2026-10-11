import { Audio } from "@remotion/media";
import React from "react";
import { staticFile, useVideoConfig } from "remotion";
import { CUT_AFTER } from "../cuts";
import { chapterFrame, DEMO_SCENES } from "../scenes/DemoScenes";
import { COUNT_FRAMES, evidenceBeats } from "../scenes/S14Evidence";
import { cardFrames, terminalBeats } from "../scenes/S15Open";
import { sceneStarts, type SceneTiming } from "../timeline";

// Synthesized for this video, CC0 (public/sfx/LICENSE.txt).
const FILES = {
  click: "sfx/click.wav",
  whoosh: "sfx/whoosh.wav",
  pop: "sfx/pop.wav",
  rise: "sfx/rise.wav",
  chime: "sfx/chime.wav",
  typing: "sfx/typing.wav",
} as const;
type Sound = keyof typeof FILES;
const LENGTH_FRAMES: Record<Sound, number> = { click: 5, whoosh: 23, pop: 5, rise: 42, chime: 54, typing: 166 };
// The loudest 100 ms block of every file (LEVEL_DB of public/sfx/make_sfx.py).
const FILE_LEVEL_DB = -26;
// The loudest block of each effect against the voice level, in dB: always well under the voice.
const LEVEL_DB: Record<Sound, number> = { click: -10, whoosh: -14, pop: -12, rise: -12, chime: -10, typing: -12 };
// A fade between two demo scenes changes only the window content, so its whoosh is quieter than a slide's.
const FADE_WHOOSH_DB = -18;
// The whoosh starts before the cut so that its middle falls in the middle of the cut.
const WHOOSH_LEAD = 4;

type Effect = { frame: number; sound: Sound; levelDb: number; durationInFrames: number };

const effect = (frame: number, sound: Sound, durationInFrames = LENGTH_FRAMES[sound], levelDb = LEVEL_DB[sound]): Effect => ({ frame, sound, levelDb, durationInFrames });

// Every effect comes from the timeline: narration cues, captures.json clicks, callouts and sounds, and the scene cuts.
const effectsOf = (scenes: SceneTiming[]): Effect[] => {
  const starts = sceneStarts(scenes);
  return scenes.flatMap((scene, index) => {
    const start = starts[index];
    const list: Effect[] = [];
    const previous = scenes[index - 1];
    const cut = previous === undefined ? undefined : CUT_AFTER[previous.id];
    if (cut !== undefined) {
      list.push(effect(start - WHOOSH_LEAD, "whoosh", LENGTH_FRAMES.whoosh, cut.moves ? LEVEL_DB.whoosh : FADE_WHOOSH_DB));
    }
    if (DEMO_SCENES[scene.id] !== undefined) {
      list.push(effect(start + chapterFrame(scene.id), "pop"));
    }
    for (const capture of scene.captures) {
      list.push(...capture.clickFrames.map((click) => effect(start + click.frame, "click")));
      list.push(...capture.timedCallouts.map((callout) => effect(start + callout.from, "pop")));
      list.push(...capture.soundFrames.map((cue) => effect(start + cue.frame, cue.sound)));
    }
    if (scene.id === "s14_evidence") {
      const beats = evidenceBeats(scene);
      list.push(...[beats.files, beats.scores, beats.once].map((frame) => effect(start + frame, "rise", COUNT_FRAMES + 2)));
      list.push(effect(start + beats.clean, "chime"));
    }
    if (scene.id === "s15_open") {
      const beats = terminalBeats(scene);
      list.push(effect(start + beats.buildStart, "typing", beats.buildDone - beats.buildStart));
      list.push(effect(start + beats.runStart, "typing", beats.runDone - beats.runStart));
      list.push(...cardFrames(scene).map((frame) => effect(start + frame, "pop")));
    }
    return list;
  });
};

export const SoundEffects: React.FC<{ scenes: SceneTiming[]; voiceDb: number }> = ({ scenes, voiceDb }) => {
  const { fps } = useVideoConfig();
  return (
    <>
      {effectsOf(scenes)
        .filter((item) => item.frame >= 0 && item.durationInFrames > 0)
        .map((item, index) => (
          <Audio
            key={`${item.sound}-${item.frame}-${index}`}
            name={`Sound ${item.sound}`}
            src={staticFile(FILES[item.sound])}
            from={item.frame}
            durationInFrames={item.durationInFrames}
            premountFor={fps}
            volume={Math.min(1, 10 ** ((voiceDb + item.levelDb - FILE_LEVEL_DB) / 20))}
          />
        ))}
    </>
  );
};
