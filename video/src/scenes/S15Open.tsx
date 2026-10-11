import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { pop, rise } from "../components/anim";
import { cueFrame } from "../components/cues";
import { Heading, SceneShell } from "../components/SceneShell";
import { color, font } from "../theme";
import type { SceneTiming } from "../timeline";

// The two commands of the README section "Run with Docker".
const BUILD = "docker build -t cvoice .";
const RUN = "docker run --rm -p 7860:7860 cvoice";
// 15 characters per second; public/sfx/typing.wav has one keystroke every 1/15 s to match.
export const CHARS_PER_FRAME = 0.5;
const LEFT = 260;
const WIDTH = 1400;

const typed = (text: string, frame: number, start: number) => text.slice(0, Math.max(0, Math.min(text.length, Math.floor((frame - start) * CHARS_PER_FRAME))));

const ModelIcon: React.FC = () => (
  <svg width={46} height={46} viewBox="0 0 24 24" fill="none" stroke={color.action} strokeWidth={1.6} strokeLinejoin="round">
    <path d="M12 2.5 20.5 7v10L12 21.5 3.5 17V7z" />
    <path d="M3.5 7 12 11.5 20.5 7M12 11.5v10" />
  </svg>
);
const CodeIcon: React.FC = () => (
  <svg width={46} height={46} viewBox="0 0 24 24" fill="none" stroke={color.youText} strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round">
    <path d="M8 6 2.5 12 8 18M16 6l5.5 6-5.5 6M13.5 4l-3 16" />
  </svg>
);
const ReportIcon: React.FC = () => (
  <svg width={46} height={46} viewBox="0 0 24 24" fill="none" stroke={color.refText} strokeWidth={1.6} strokeLinejoin="round" strokeLinecap="round">
    <path d="M6 2.5h8.5L19 7v14.5H6z" />
    <path d="M14.5 2.5V7H19M9 11.5h7M9 15h7M9 18.5h4" />
  </svg>
);

const CARDS = [
  { icon: <ModelIcon />, place: "Hugging Face", address: "WinterBlossom/contrastive-voice", role: "The detector", cue: "Hugging" },
  { icon: <CodeIcon />, place: "GitHub", address: "WinterBlossom0/contrastive-voice", role: "The code", cue: "GitHub" },
  { icon: <ReportIcon />, place: "Technical report", address: "docs/technical.md", role: "Every number explained", cue: "technical" },
];

// When each command is typed; SoundEffects.tsx plays the keystrokes over the same frames.
export const terminalBeats = (scene: SceneTiming) => {
  const buildStart = 14;
  const buildDone = buildStart + Math.ceil(BUILD.length / CHARS_PER_FRAME);
  const runStart = Math.max(buildDone + 10, cueFrame(scene, 0, "run"));
  const runDone = runStart + Math.ceil(RUN.length / CHARS_PER_FRAME);
  return { buildStart, buildDone, runStart, runDone, openLine: Math.max(runDone + 6, cueFrame(scene, 0, "open")) };
};

// The frames at which the three cards pop up.
export const cardFrames = (scene: SceneTiming): number[] => CARDS.map((card) => cueFrame(scene, 1, card.cue));

export const S15Open: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const terminalIn = pop(frame, 2);
  const { buildStart, buildDone, runStart, runDone, openLine } = terminalBeats(scene);
  const cardStarts = cardFrames(scene);
  const caret = Math.floor(frame / 8) % 2 === 0;
  const typing = frame < runDone;
  return (
    <SceneShell>
      <Heading style={{ position: "absolute", left: LEFT, top: 80, fontSize: 64, opacity: rise(frame, 0, 18) }}>Run it yourself</Heading>
      <div
        style={{
          position: "absolute",
          left: LEFT,
          top: 190,
          width: WIDTH,
          borderRadius: 18,
          overflow: "hidden",
          backgroundColor: "rgba(26, 25, 24, 0.94)",
          border: `1px solid rgba(237, 230, 218, 0.14)`,
          boxShadow: "0 40px 100px rgba(0, 0, 0, 0.55)",
          opacity: terminalIn,
          translate: `0px ${interpolate(terminalIn, [0, 1], [40, 0])}px`,
        }}
      >
        <div style={{ height: 40, display: "flex", alignItems: "center", gap: 9, paddingLeft: 18, backgroundColor: color.panel2 }}>
          {[0, 1, 2].map((dot) => (
            <div key={dot} style={{ width: 12, height: 12, borderRadius: 6, backgroundColor: color.panel3 }} />
          ))}
          <div style={{ marginLeft: 18, color: color.muted, fontSize: 18, fontFamily: font.mono }}>contrastive-voice</div>
        </div>
        <div style={{ padding: "26px 36px 30px", fontFamily: font.mono, fontSize: 34, lineHeight: 1.75, whiteSpace: "pre" }}>
          <div>
            <span style={{ color: color.action }}>$ </span>
            {typed(BUILD, frame, buildStart)}
            {typing && frame < buildDone && caret ? <span style={{ color: color.action }}>▍</span> : null}
          </div>
          <div style={{ opacity: frame >= buildDone + 4 ? 1 : 0 }}>
            <span style={{ color: color.action }}>$ </span>
            {typed(RUN, frame, runStart)}
            {typing && frame >= buildDone && caret ? <span style={{ color: color.action }}>▍</span> : null}
          </div>
          <div style={{ color: color.ink2, opacity: rise(frame, openLine, 14) }}>
            <span style={{ color: color.refText }}>→ </span>open http://localhost:7860
          </div>
        </div>
      </div>
      <div style={{ position: "absolute", left: LEFT, top: 590, width: WIDTH, display: "flex", gap: 40 }}>
        {CARDS.map((card, index) => {
          const shown = pop(frame, cardStarts[index], true);
          return (
            <div
              key={card.place}
              style={{
                flex: 1,
                height: 270,
                padding: "30px 30px",
                borderRadius: 22,
                backgroundColor: "rgba(38, 38, 36, 0.92)",
                border: `1px solid ${color.line}`,
                boxShadow: "0 24px 60px rgba(0, 0, 0, 0.4)",
                display: "flex",
                flexDirection: "column",
                gap: 12,
                opacity: Math.min(1, shown * 1.5),
                translate: `0px ${interpolate(shown, [0, 1], [60, 0])}px`,
                scale: String(interpolate(shown, [0, 1], [0.92, 1])),
              }}
            >
              {card.icon}
              <div style={{ fontFamily: font.display, fontSize: 42, lineHeight: 1.1, marginTop: 6 }}>{card.place}</div>
              <div style={{ fontFamily: font.mono, fontSize: 18, color: color.ink2, whiteSpace: "nowrap" }}>{card.address}</div>
              <div style={{ fontSize: 26, color: color.muted }}>{card.role}</div>
            </div>
          );
        })}
      </div>
    </SceneShell>
  );
};
