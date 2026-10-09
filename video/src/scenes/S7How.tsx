import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { fadeOut, rise } from "../components/anim";
import { Heading, SceneShell } from "../components/SceneShell";
import { GETTYSBURG, referenceWords, yourWords } from "../components/words";
import { color, font } from "../theme";
import { beatFrame, type SceneTiming } from "../timeline";

const STEPS = ["Align", "Window", "Measure", "Compare"];
const DIMENSIONS = ["Pace", "Pauses", "Pitch variation", "Emphasis", "Volume", "Clarity", "Word time", "Ending", "Speech tempo"];
const LEFT = 160;
const WIDTH = 1600;

const Panel: React.FC<{ visible: number; children: React.ReactNode }> = ({ visible, children }) => (
  <div style={{ position: "absolute", left: LEFT, top: 250, width: WIDTH, height: 640, opacity: visible, translate: `0px ${interpolate(visible, [0, 1], [18, 0])}px` }}>
    {children}
  </div>
);

const WordRow: React.FC<{ words: typeof yourWords; top: number; tint: string; label: string; progress: number }> = ({ words, top, tint, label, progress }) => (
  <>
    <div style={{ position: "absolute", left: 0, top: top - 44, fontSize: 28, fontWeight: 700, color: tint }}>{label}</div>
    {words.map((word, index) => (
      <div
        key={index}
        style={{
          position: "absolute",
          left: word.start * WIDTH,
          top,
          width: (word.end - word.start) * WIDTH - 4,
          height: 72,
          borderRadius: 10,
          border: `1.5px solid ${tint}`,
          backgroundColor: color.surface,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: Math.min(28, ((word.end - word.start) * WIDTH - 10) / (word.text.length * 0.55)),
          color: color.ink,
          overflow: "hidden",
          opacity: Math.min(1, Math.max(0, progress * 1.5 - index * 0.05)),
        }}
      >
        {word.text}
      </div>
    ))}
  </>
);

export const S7How: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  // Narration order: intro, alignment (two lines), windows and measures (one line), then the comparison lines.
  const windowLine = scene.lines[Math.min(3, scene.lines.length - 1)];
  const starts = [beatFrame(scene, 1), windowLine.from, windowLine.from + Math.round(windowLine.durationInFrames / 2), beatFrame(scene, 4)];
  const ends = [...starts.slice(1), scene.durationInFrames];
  const visibility = starts.map((start, index) => rise(frame, start, 18) * (index === STEPS.length - 1 ? 1 : fadeOut(frame, ends[index] + 6, 12)));
  const active = starts.filter((start) => frame >= start).length - 1;

  const windowStart = Math.min(GETTYSBURG.length - 5, Math.floor(Math.max(0, frame - starts[1]) / 14));
  const lastWord = referenceWords[windowStart + 4];

  return (
    <SceneShell>
      <Heading style={{ position: "absolute", left: LEFT, top: 70, fontSize: 64, opacity: rise(frame, 0, 18) }}>How it works</Heading>
      <div style={{ position: "absolute", left: LEFT, top: 165, display: "flex", gap: 14 }}>
        {STEPS.map((step, index) => (
          <div
            key={step}
            style={{
              padding: "8px 22px",
              borderRadius: 999,
              fontSize: 28,
              fontWeight: 700,
              border: `1px solid ${index === active ? color.accent : color.line}`,
              backgroundColor: index === active ? color.accentWash : "transparent",
              color: index === active ? color.accentText : color.muted,
            }}
          >
            {index + 1}. {step}
          </div>
        ))}
      </div>

      <Panel visible={visibility[0]}>
        <div style={{ fontSize: 40, fontFamily: font.display, fontWeight: 600 }}>Forced alignment finds every word in both recordings</div>
        <div style={{ fontSize: 30, color: color.ink2, marginTop: 14 }}>wav2vec2 CTC model: a start and end time for every word, at 20 ms resolution</div>
        <div style={{ position: "relative", marginTop: 110 }}>
          <WordRow words={yourWords} top={0} tint={color.accent} label="You" progress={rise(frame, starts[0], 40)} />
          <WordRow words={referenceWords} top={190} tint={color.reference} label="Reference" progress={rise(frame, starts[0] + 10, 40)} />
        </div>
      </Panel>

      <Panel visible={visibility[1]}>
        <div style={{ fontSize: 40, fontFamily: font.display, fontWeight: 600 }}>A window of five words slides along the text</div>
        <div style={{ fontSize: 30, color: color.ink2, marginTop: 14 }}>Each window is compared with the same five words in the reference</div>
        <div style={{ position: "relative", marginTop: 150 }}>
          <div
            style={{
              position: "absolute",
              left: referenceWords[windowStart].start * WIDTH - 12,
              top: -16,
              width: (lastWord.end - referenceWords[windowStart].start) * WIDTH + 20,
              height: 96,
              borderRadius: 16,
              backgroundColor: color.accentWash,
              border: `2px solid ${color.accent}`,
            }}
          />
          <WordRow words={referenceWords} top={0} tint={color.line} label="" progress={1} />
        </div>
      </Panel>

      <Panel visible={visibility[2]}>
        <div style={{ fontSize: 40, fontFamily: font.display, fontWeight: 600 }}>Nine delivery measures, on the same words in both readings</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 26, marginTop: 70, width: 1300 }}>
          {DIMENSIONS.map((dimension, index) => {
            const pop = spring({ frame: frame - starts[2] - 8 - index * 5, fps, config: { damping: 200 } });
            return (
              <div
                key={dimension}
                style={{
                  padding: "24px 30px",
                  borderRadius: 16,
                  backgroundColor: color.surface,
                  border: `1px solid ${color.line}`,
                  fontSize: 38,
                  opacity: pop,
                  scale: interpolate(pop, [0, 1], [0.92, 1]),
                }}
              >
                <span style={{ color: color.muted, marginRight: 16 }}>D{index + 1}</span>
                {dimension}
              </div>
            );
          })}
        </div>
      </Panel>

      <Panel visible={visibility[3]}>
        <div style={{ fontSize: 40, fontFamily: font.display, fontWeight: 600 }}>Every value is scored against the reference</div>
        <div style={{ display: "flex", alignItems: "center", gap: 40, marginTop: 60, fontFamily: font.display, fontSize: 60, fontWeight: 600 }}>
          <span>change</span>
          <span style={{ color: color.muted }}>=</span>
          <span>
            ln(<span style={{ color: color.accentText }}>you</span>
            <span style={{ color: color.muted }}> / </span>
            <span style={{ color: color.ink2 }}>reference</span>)
          </span>
        </div>
        <div style={{ marginTop: 30, fontSize: 30, color: color.ink2 }}>Volume against your own median level, pitch against your own median pitch</div>
        <div style={{ marginTop: 56, fontSize: 38, lineHeight: 1.45, maxWidth: 1450, opacity: rise(frame, beatFrame(scene, 5), 20) }}>
          Not a flaw: a quiet microphone, a deep voice
        </div>
        <div style={{ marginTop: 30, fontSize: 34, lineHeight: 1.45, color: color.ink2, maxWidth: 1450, opacity: rise(frame, beatFrame(scene, 6), 20) }}>
          Flag threshold: fitted on flawless comparisons
        </div>
      </Panel>
    </SceneShell>
  );
};
