import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { fadeOut, pop, rise } from "../components/anim";
import { CaptureFrame, FRAME } from "../components/CaptureFrame";
import { ChapterMarker } from "../components/ChapterMarker";
import { SceneShell } from "../components/SceneShell";
import { color, font } from "../theme";
import type { SceneId, SceneTiming } from "../timeline";

type DemoSpec = { chapter: number; title: string; shows: string };

// One chapter per demo scene; `shows` is the placeholder text while the scene has no capture yet.
export const DEMO_SCENES: Partial<Record<SceneId, DemoSpec>> = {
  s3_open_example: { chapter: 1, title: "Try an example", shows: "The page loads; the examples menu opens; L3A scores 86.11, with its summary and the three biggest fixes." },
  s4_listen: { chapter: 2, title: "Pinned to the words", shows: "The waveform strip and the transcript; the recording plays over the rushed words." },
  s5_finding: { chapter: 3, title: "Open a finding", shows: "Finding #3, Rushed: 0.87 s against 1.62 s, the gauge, Listen to yours and the reference, How to fix." },
  s6_hear_fixed: { chapter: 4, title: "Hear it fixed", shows: "Hear it fixed: progress, the result card, Yours / Edited / Target, partly changed, +3.07." },
  s7_melody: { chapter: 5, title: "Borrow the melody", shows: "A pitch finding: Try the reference's melody, then the result." },
  s8_fix_all: { chapter: 6, title: "Fix everything", shows: "Fix everything and listen: 86.11 becomes 96.17; What each fix did." },
  s9_text_lists: { chapter: 7, title: "Transcript and charts", shows: "Transcript underlines, Every finding with a filter, Every measurement zoomed." },
  s10_fair: { chapter: 8, title: "No invented problems", shows: "The identity example scores 100 with nothing flagged; r2_consensus compares with five readers." },
  s11_upload: { chapter: 9, title: "Upload your own", shows: "Analyse your reading: file, bundled reference, transcript; a wrong transcript is refused; then the stages run." },
  s12_no_reference: { chapter: 10, title: "No reference", shows: "L3A_self: three spots stand out, with the rough-check note." },
};

// Lavender is this recording and its edited take, lake the reference (the dashboard's colour jobs).
const SEGMENT_TINT: Record<string, { line: string; text: string; wash: string }> = {
  Yours: { line: color.you, text: color.youText, wash: color.youWash },
  Edited: { line: color.you, text: color.youText, wash: color.youWash },
  Target: { line: color.ref, text: color.refText, wash: "rgba(33, 155, 161, 0.14)" },
  Reference: { line: color.ref, text: color.refText, wash: "rgba(33, 155, 161, 0.14)" },
};
const PLAYING_TINT = { line: color.action, text: color.action, wash: color.actionWash };

// While the scene's clip plays real app audio, a pill names what plays: "Listening", or the take of a clip of several takes.
const ListeningPill: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (scene.clip === null) {
    return null;
  }
  const { from, durationInFrames, segments } = scene.clip;
  const visible = rise(frame, from, 12) * fadeOut(frame, from + durationInFrames, 12);
  const playing = (segments ?? []).filter((segment) => frame >= from + Math.round(segment.startSec * fps)).pop();
  const label = playing === undefined ? "Listening" : playing.label;
  const tint = playing === undefined ? PLAYING_TINT : SEGMENT_TINT[playing.label] ?? PLAYING_TINT;
  const enter = pop(frame, from, true);
  return (
    <div
      style={{
        position: "absolute",
        right: FRAME.left,
        top: 34,
        display: "flex",
        alignItems: "center",
        gap: 14,
        padding: "9px 22px",
        borderRadius: 999,
        backgroundColor: tint.wash,
        border: `1.5px solid ${tint.line}`,
        color: tint.text,
        fontFamily: font.text,
        fontSize: 28,
        fontWeight: 700,
        opacity: visible,
        scale: String(interpolate(enter, [0, 1], [0.8, 1])),
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

// The first demo scene: the browser window springs into view there, and stays in place for the later demo scenes.
const FIRST_DEMO: SceneId = "s3_open_example";

// The frame of a demo scene at which its chapter marker pops in; later in the first scene, after the window's entry.
export const chapterFrame = (id: SceneId): number => (id === FIRST_DEMO ? 18 : 4);

export const DemoScene: React.FC<{ scene: SceneTiming; spec: DemoSpec }> = ({ scene, spec }) => (
  <SceneShell>
    <ChapterMarker index={spec.chapter} title={spec.title} left={FRAME.left} top={30} start={chapterFrame(scene.id)} />
    <CaptureFrame captures={scene.captures} enter={scene.id === FIRST_DEMO} pendingTitle={`Capture pending: ${scene.id}`} pendingDetail={spec.shows} />
    <ListeningPill scene={scene} />
  </SceneShell>
);
