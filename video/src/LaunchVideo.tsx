import { Audio } from "@remotion/media";
import { TransitionSeries } from "@remotion/transitions";
import React from "react";
import { AbsoluteFill, Series, staticFile, useVideoConfig } from "remotion";
import { MusicBed } from "./components/MusicBed";
import { SoundEffects } from "./components/SoundEffects";
import { CUT_AFTER, cutFrames } from "./cuts";
import { Backdrop } from "./components/SceneShell";
import { Subtitles } from "./components/Subtitles";
import { DEMO_SCENES, DemoScene } from "./scenes/DemoScenes";
import { S01Hook } from "./scenes/S01Hook";
import { S02What } from "./scenes/S02What";
import { S13How } from "./scenes/S13How";
import { S14Evidence } from "./scenes/S14Evidence";
import { S15Open } from "./scenes/S15Open";
import { S16Close } from "./scenes/S16Close";
import type { LaunchVideoProps, SceneId, SceneTiming } from "./timeline";

const SceneVisual: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const demo = DEMO_SCENES[scene.id];
  if (demo !== undefined) {
    return <DemoScene scene={scene} spec={demo} />;
  }
  switch (scene.id) {
    case "s1_hook":
      return <S01Hook scene={scene} />;
    case "s2_what":
      return <S02What scene={scene} />;
    case "s13_how":
      return <S13How scene={scene} />;
    case "s14_evidence":
      return <S14Evidence scene={scene} />;
    case "s15_open":
      return <S15Open scene={scene} />;
    case "s16_close":
      return <S16Close scene={scene} />;
    default:
      throw new Error(`No visual for scene ${scene.id}`);
  }
};

// The closing scene shows its narration as on-screen type, and so does the opening scene, so subtitles there would repeat it.
const SCENES_WITHOUT_SUBTITLES: ReadonlySet<SceneId> = new Set<SceneId>(["s1_hook", "s16_close"]);

// Missing audio files are skipped, so the video still renders before the narration exists.
const SceneAudio: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const { fps } = useVideoConfig();
  return (
    <>
      {scene.lines.map((line, index) =>
        line.fileExists ? <Audio key={line.file} name={`Voice ${index + 1}`} src={staticFile(line.file)} from={line.from} durationInFrames={line.durationInFrames} premountFor={fps} /> : null,
      )}
      {scene.clip !== null && scene.clip.fileExists ? (
        <Audio name="Clip" src={staticFile(scene.clip.file)} from={scene.clip.from} durationInFrames={scene.clip.durationInFrames} premountFor={fps} />
      ) : null}
    </>
  );
};

export const LaunchVideo: React.FC<LaunchVideoProps> = ({ scenes, voiceDb }) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      <Backdrop />
      {/* Each scene runs on for the length of the cut after it, so a cut never takes time from the narration: scene n + 1
          starts at the sum of the earlier scene lengths, the same frame as in the audio and subtitle track below. */}
      <TransitionSeries name="Scenes">
        {scenes.flatMap((scene) => {
          const cut = CUT_AFTER[scene.id];
          const items = [
            <TransitionSeries.Sequence key={scene.id} name={scene.id} durationInFrames={scene.durationInFrames + cutFrames(scene.id)} premountFor={fps}>
              <SceneVisual scene={scene} />
            </TransitionSeries.Sequence>,
          ];
          if (cut !== undefined) {
            items.push(<TransitionSeries.Transition key={`${scene.id}-cut`} presentation={cut.presentation} timing={cut.timing} />);
          }
          return items;
        })}
      </TransitionSeries>
      <Series>
        {scenes.map((scene) => (
          <Series.Sequence key={scene.id} name={`${scene.id} voice`} durationInFrames={scene.durationInFrames} premountFor={fps}>
            <SceneAudio scene={scene} />
            {SCENES_WITHOUT_SUBTITLES.has(scene.id) ? null : <Subtitles scene={scene} />}
          </Series.Sequence>
        ))}
      </Series>
      <MusicBed scenes={scenes} voiceDb={voiceDb} />
      <SoundEffects scenes={scenes} voiceDb={voiceDb} />
    </AbsoluteFill>
  );
};
