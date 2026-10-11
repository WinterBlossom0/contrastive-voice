import React from "react";
import { CalculateMetadataFunction, Composition, continueRender, delayRender } from "remotion";
import { DEFAULT_VOICE_DB, voiceLevelDb } from "./audioLevel";
import { CaptureFrameCheck } from "./checks/CaptureFrameCheck";
import { LaunchVideo } from "./LaunchVideo";
import { fontsReady } from "./theme";
import { computeTimeline, FPS, type LaunchVideoProps } from "./timeline";

const fontHandle = delayRender("Loading fonts");
fontsReady.then(() => continueRender(fontHandle));

const calculateMetadata: CalculateMetadataFunction<LaunchVideoProps> = async ({ abortSignal }) => {
  const scenes = await computeTimeline(abortSignal);
  const voiceFiles = scenes.flatMap((scene) => scene.lines.filter((line) => line.fileExists).map((line) => line.file));
  return {
    durationInFrames: scenes.reduce((sum, scene) => sum + scene.durationInFrames, 0),
    props: { scenes, voiceDb: await voiceLevelDb(voiceFiles, abortSignal) },
  };
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="LaunchVideo"
        component={LaunchVideo}
        durationInFrames={6300}
        fps={FPS}
        width={1920}
        height={1080}
        defaultProps={{ scenes: [], voiceDb: DEFAULT_VOICE_DB }}
        calculateMetadata={calculateMetadata}
      />
      <Composition id="CaptureFrameCheck" component={CaptureFrameCheck} durationInFrames={300} fps={FPS} width={1920} height={1080} />
    </>
  );
};
