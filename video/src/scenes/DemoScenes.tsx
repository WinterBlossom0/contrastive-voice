import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
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
      { text: "Delivery score: 86.11", atLine: 4 },
    ]} />
);

// Lavender is this recording and its edited take, lake the reference (the dashboard's colour jobs).
const SEGMENT_TINT: Record<string, { line: string; text: string; wash: string }> = {
  Yours: { line: color.you, text: color.youText, wash: color.youWash },
  Edited: { line: color.you, text: color.youText, wash: color.youWash },
  Target: { line: color.ref, text: color.refText, wash: "rgba(33, 155, 161, 0.14)" },
};
const PLAYING_TINT = { line: color.action, text: color.action, wash: color.actionWash };

// The pill names what the clip plays: "Listen", or the take of a clip of several takes (it keeps a take's name through the gap after it).
const ListeningPill: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (scene.clip === null) {
    return null;
  }
  const { from, durationInFrames, segments } = scene.clip;
  const visible = rise(frame, from, 12) * fadeOut(frame, from + durationInFrames, 12);
  const playing = (segments ?? []).filter((segment) => frame >= from + Math.round(segment.startSec * fps)).pop();
  const label = playing === undefined ? "Listen" : playing.label;
  const tint = playing === undefined ? PLAYING_TINT : SEGMENT_TINT[playing.label] ?? PLAYING_TINT;
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
        backgroundColor: tint.wash,
        border: `1px solid ${tint.line}`,
        color: tint.text,
        fontSize: 30,
        fontWeight: 700,
        opacity: visible,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 4, height: 28 }}>
        {[0, 1, 2, 3, 4].map((bar) => (
          <div key={bar} style={{ width: 5, borderRadius: 3, backgroundColor: tint.line, height: 8 + 18 * Math.abs(Math.sin(frame / 5 + bar * 1.3)) }} />
        ))}
      </div>
      {label}
    </div>
  );
};

// The features that came after the frozen evaluation say so on screen while the narration introduces them.
const AddedLaterBadge: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const end = scene.lines.length > 1 ? scene.lines[1].from : scene.durationInFrames;
  return (
    <div
      style={{
        position: "absolute",
        right: FRAME.left,
        top: 36,
        padding: "8px 20px",
        borderRadius: 999,
        border: `1px solid ${color.line}`,
        backgroundColor: color.surface,
        color: color.ink2,
        fontSize: 26,
        opacity: rise(frame, 8, 14) * fadeOut(frame, end, 10),
      }}
    >
      Added after the frozen evaluation
    </div>
  );
};

export const S4DemoListen: React.FC<{ scene: SceneTiming }> = ({ scene }) => (
  <DemoScene scene={scene} headings={[
      { text: "The transcript follows the audio", atLine: 0 },
      { text: "Flags mark the exact words", atLine: 2 },
    ]}>
    <ListeningPill scene={scene} />
  </DemoScene>
);

export const S5DemoFinding: React.FC<{ scene: SceneTiming }> = ({ scene }) => (
  <DemoScene scene={scene} headings={[
      { text: "One finding in detail", atLine: 0 },
      { text: "Measured against the reference", atLine: 1 },
      { text: "One concrete fix", atLine: 3 },
    ]} />
);

export const S5bDemoHearFixed: React.FC<{ scene: SceneTiming }> = ({ scene }) => (
  <DemoScene scene={scene} headings={[
      { text: "Hear it fixed", atLine: 0 },
      { text: "Yours, edited, target", atLine: "clip" },
      { text: "Still flagged · partly changed", atLine: 2 },
      { text: "An edited preview, not a guarantee", atLine: 3 },
    ]}>
    <AddedLaterBadge scene={scene} />
    <ListeningPill scene={scene} />
  </DemoScene>
);

export const S5cDemoFixAll: React.FC<{ scene: SceneTiming }> = ({ scene }) => (
  <DemoScene scene={scene} headings={[
      { text: "Fix everything and listen", atLine: 0 },
      { text: "What each fix did", atLine: 1 },
    ]}>
    <AddedLaterBadge scene={scene} />
  </DemoScene>
);

export const S6DemoCleanAndUpload: React.FC<{ scene: SceneTiming }> = ({ scene }) => (
  <DemoScene scene={scene} headings={[
      { text: "Placebo check", atLine: 0 },
      { text: "Upload your own pair", atLine: 1 },
    ]} />
);

export const S6bDemoNoReference: React.FC<{ scene: SceneTiming }> = ({ scene }) => (
  <DemoScene scene={scene} headings={[
      { text: "Without a reference", atLine: 0 },
      { text: "A rough check", atLine: 1 },
    ]}>
    <AddedLaterBadge scene={scene} />
  </DemoScene>
);
