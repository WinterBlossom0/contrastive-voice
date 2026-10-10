import { Audio } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Sequence, Series, staticFile, useVideoConfig } from "remotion";
import { Subtitles } from "./components/Subtitles";
import { S3DemoSummary, S4DemoListen, S5bDemoHearFixed, S5cDemoFixAll, S5DemoFinding, S6bDemoNoReference, S6DemoCleanAndUpload } from "./scenes/DemoScenes";
import { S1Hook } from "./scenes/S1Hook";
import { S2What } from "./scenes/S2What";
import { S7How } from "./scenes/S7How";
import { S8Evidence } from "./scenes/S8Evidence";
import { S9Open } from "./scenes/S9Open";
import { S10Close } from "./scenes/S10Close";
import { color } from "./theme";
import type { LaunchVideoProps, SceneId, SceneTiming } from "./timeline";

const SCENE_COMPONENTS: Record<SceneId, React.FC<{ scene: SceneTiming }>> = {
  s1_hook: S1Hook,
  s2_what: S2What,
  s3_demo_summary: S3DemoSummary,
  s4_demo_listen: S4DemoListen,
  s5_demo_finding: S5DemoFinding,
  s5b_demo_hear_fixed: S5bDemoHearFixed,
  s5c_demo_fix_all: S5cDemoFixAll,
  s6_demo_clean_and_upload: S6DemoCleanAndUpload,
  s6b_demo_no_reference: S6bDemoNoReference,
  s7_how: S7How,
  s8_evidence: S8Evidence,
  s9_open: S9Open,
  s10_close: S10Close,
};

// The closing scene shows its narration as on-screen text, so subtitles there would repeat it word for word.
const SCENES_WITHOUT_SUBTITLES: ReadonlySet<SceneId> = new Set<SceneId>(["s10_close"]);

// Missing audio files are skipped, so the video still renders before the narration exists.
const SceneAudio: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const { fps } = useVideoConfig();
  return (
    <>
      {scene.lines.map((line, index) =>
        line.fileExists ? (
          <Sequence key={line.file} name={`Voice ${index + 1}`} from={line.from} durationInFrames={line.durationInFrames} premountFor={fps}>
            <Audio src={staticFile(line.file)} />
          </Sequence>
        ) : null,
      )}
      {scene.clip !== null && scene.clip.fileExists ? (
        <Sequence name="Clip" from={scene.clip.from} durationInFrames={scene.clip.durationInFrames} premountFor={fps}>
          <Audio src={staticFile(scene.clip.file)} />
        </Sequence>
      ) : null}
    </>
  );
};

export const LaunchVideo: React.FC<LaunchVideoProps> = ({ scenes }) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: color.base }}>
      <Series>
        {scenes.map((scene) => {
          const SceneComponent = SCENE_COMPONENTS[scene.id];
          return (
            <Series.Sequence key={scene.id} name={scene.id} durationInFrames={scene.durationInFrames} premountFor={fps}>
              <SceneComponent scene={scene} />
              <SceneAudio scene={scene} />
              {SCENES_WITHOUT_SUBTITLES.has(scene.id) ? null : <Subtitles scene={scene} />}
            </Series.Sequence>
          );
        })}
      </Series>
    </AbsoluteFill>
  );
};
