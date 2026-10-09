import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { fadeOut, rise } from "../components/anim";
import { CaptureFrame, FRAME } from "../components/CaptureFrame";
import { Heading, SceneShell } from "../components/SceneShell";
import { color } from "../theme";
import { beatFrame, type SceneTiming } from "../timeline";

// A heading appears with the narration line `atLine`, or with the clip when `atLine` is "clip".
type DemoHeading = { text: string; atLine: number | "clip" };

const headingStart = (scene: SceneTiming, heading: DemoHeading): number => {
  if (heading.atLine === "clip") {
    return scene.clip === null ? scene.durationInFrames : scene.clip.from;
  }
  return heading.atLine === 0 ? 0 : beatFrame(scene, heading.atLine);
};

const DemoScene: React.FC<{ scene: SceneTiming; headings: DemoHeading[]; children?: React.ReactNode }> = ({ scene, headings, children }) => {
  const frame = useCurrentFrame();
  return (
    <SceneShell>
      {headings.map((heading, index) => {
        const start = headingStart(scene, heading);
        const end = index === headings.length - 1 ? scene.durationInFrames : headingStart(scene, headings[index + 1]);
        return (
          <Heading
            key={heading.text}
            style={{
              position: "absolute",
              left: FRAME.left,
              top: 30,
              fontSize: 50,
              opacity: rise(frame, start, 16) * fadeOut(frame, end, 10),
              translate: `0px ${interpolate(rise(frame, start, 16), [0, 1], [14, 0])}px`,
            }}
          >
            {heading.text}
          </Heading>
        );
      })}
      <CaptureFrame captures={scene.captures} sceneDuration={scene.durationInFrames} />
      {children}
    </SceneShell>
  );
};

export const S3DemoSummary: React.FC<{ scene: SceneTiming }> = ({ scene }) => (
  <DemoScene scene={scene} headings={[
      { text: "A gallery example: an edited speech", atLine: 0 },
      { text: "Biggest fixes first", atLine: 3 },
      { text: "Delivery score: 86.11", atLine: 5 },
    ]} />
);

const ListeningPill: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  if (scene.clip === null) {
    return null;
  }
  const { from, durationInFrames } = scene.clip;
  const visible = rise(frame, from, 12) * fadeOut(frame, from + durationInFrames, 12);
  return (
    <div
      style={{
        position: "absolute",
        right: FRAME.left,
        top: 30,
        display: "flex",
        alignItems: "center",
        gap: 14,
        padding: "10px 22px",
        borderRadius: 999,
        backgroundColor: color.accentWash,
        border: `1px solid ${color.accent}`,
        color: color.accentText,
        fontSize: 30,
        fontWeight: 700,
        opacity: visible,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 4, height: 28 }}>
        {[0, 1, 2, 3, 4].map((bar) => (
          <div key={bar} style={{ width: 5, borderRadius: 3, backgroundColor: color.accent, height: 8 + 18 * Math.abs(Math.sin(frame / 5 + bar * 1.3)) }} />
        ))}
      </div>
      Listen
    </div>
  );
};

export const S4DemoListen: React.FC<{ scene: SceneTiming }> = ({ scene }) => (
  <DemoScene scene={scene} headings={[
      { text: "The transcript follows the audio", atLine: 0 },
      { text: "Flags mark the exact words", atLine: 3 },
    ]}>
    <ListeningPill scene={scene} />
  </DemoScene>
);

export const S5DemoFinding: React.FC<{ scene: SceneTiming }> = ({ scene }) => (
  <DemoScene scene={scene} headings={[
      { text: "One finding in detail", atLine: 0 },
      { text: "Measured against the reference", atLine: 1 },
      { text: "A/B playback", atLine: "clip" },
      { text: "One concrete fix", atLine: 4 },
    ]} >
    <ListeningPill scene={scene} />
  </DemoScene>
);

export const S6DemoCleanAndUpload: React.FC<{ scene: SceneTiming }> = ({ scene }) => (
  <DemoScene scene={scene} headings={[
      { text: "Placebo check", atLine: 0 },
      { text: "Upload your own pair", atLine: 2 },
    ]} />
);
