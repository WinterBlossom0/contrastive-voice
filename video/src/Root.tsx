import React from "react";
import { CalculateMetadataFunction, Composition, continueRender, delayRender } from "remotion";
import { LaunchVideo } from "./LaunchVideo";
import { fontsReady } from "./theme";
import { computeTimeline, FPS, type LaunchVideoProps } from "./timeline";

const fontHandle = delayRender("Loading fonts");
fontsReady.then(() => continueRender(fontHandle));

const calculateMetadata: CalculateMetadataFunction<LaunchVideoProps> = async ({ abortSignal }) => {
  const scenes = await computeTimeline(abortSignal);
  return {
    durationInFrames: scenes.reduce((sum, scene) => sum + scene.durationInFrames, 0),
    props: { scenes },
  };
};

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="LaunchVideo"
      component={LaunchVideo}
      durationInFrames={6300}
      fps={FPS}
      width={1920}
      height={1080}
      defaultProps={{ scenes: [] }}
      calculateMetadata={calculateMetadata}
    />
  );
};
