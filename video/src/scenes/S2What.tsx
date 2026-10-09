import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { rise } from "../components/anim";
import { Heading, SceneShell } from "../components/SceneShell";
import { Waveform, type WordSpan } from "../components/Waveform";
import { referenceWords, RUSH_FIRST, RUSH_LAST, yourWords } from "../components/words";
import { color } from "../theme";
import { beatFrame, type SceneTiming } from "../timeline";

const LEFT = 160;
const WIDTH = 1600;
const YOU_TOP = 300;
const REF_TOP = 600;
const WAVE_HEIGHT = 130;

const Label: React.FC<{ text: string; center: number; top: number; tint: string }> = ({ text, center, top, tint }) => (
  <div style={{ position: "absolute", left: LEFT + center * WIDTH, top, translate: "-50% 0px", fontSize: 28, color: tint, whiteSpace: "nowrap" }}>{text}</div>
);

// The rushed words sit too close for separate labels, so the flagged phrase gets one label.
const WordLabels: React.FC<{ words: WordSpan[]; top: number; mergeFlagged: boolean; flagged: number }> = ({ words, top, mergeFlagged, flagged }) => {
  const rushed = words.slice(RUSH_FIRST, RUSH_LAST + 1);
  const rushedTint = flagged > 0 ? color.flagText : color.ink2;
  return (
    <>
      {words.map((word, index) => {
        const inRush = index >= RUSH_FIRST && index <= RUSH_LAST;
        if (inRush && mergeFlagged) {
          return null;
        }
        return <Label key={index} text={word.text} center={(word.start + word.end) / 2} top={top} tint={color.ink2} />;
      })}
      {mergeFlagged ? (
        <Label text={rushed.map((word) => word.text).join(" ")} center={(rushed[0].start + rushed[rushed.length - 1].end) / 2} top={top} tint={rushedTint} />
      ) : null}
    </>
  );
};

export const S2What: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const align = rise(frame, beatFrame(scene, 1), 40);
  const flag = rise(frame, beatFrame(scene, 2), 24);
  const reveal = interpolate(frame, [10, 70], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <SceneShell>
      <Heading style={{ position: "absolute", left: LEFT, top: 100, fontSize: 58, opacity: rise(frame, 0, 20) }}>
        Your reading, against a reference of the <span style={{ color: color.accentText }}>same text</span>
      </Heading>
      <div style={{ position: "absolute", left: LEFT, top: YOU_TOP - 46, fontSize: 30, color: color.accentText, fontWeight: 700 }}>You</div>
      <div style={{ position: "absolute", left: LEFT, top: YOU_TOP }}>
        <Waveform words={yourWords} width={WIDTH} height={WAVE_HEIGHT} seed={3} barColor={color.accent} reveal={reveal} flag={{ start: yourWords[RUSH_FIRST].start, end: yourWords[RUSH_LAST].end }} flagStrength={flag} />
      </div>
      <WordLabels words={yourWords} top={YOU_TOP + WAVE_HEIGHT + 10} mergeFlagged flagged={flag} />
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, pointerEvents: "none" }}>
        {referenceWords.map((word, index) => {
          const fromX = LEFT + ((yourWords[index].start + yourWords[index].end) / 2) * WIDTH;
          const toX = LEFT + ((word.start + word.end) / 2) * WIDTH;
          const progress = Math.min(1, Math.max(0, align * 1.6 - index * 0.04));
          const y1 = YOU_TOP + WAVE_HEIGHT + 50;
          const y2 = REF_TOP - 16;
          const isFlagged = index >= RUSH_FIRST && index <= RUSH_LAST && flag > 0;
          return (
            <line
              key={index}
              x1={fromX}
              y1={y1}
              x2={fromX + (toX - fromX) * progress}
              y2={y1 + (y2 - y1) * progress}
              stroke={isFlagged ? color.flag : color.line}
              strokeOpacity={isFlagged ? 0.5 + 0.5 * flag : 1}
              strokeWidth={isFlagged ? 2.5 : 2}
            />
          );
        })}
      </svg>
      <div style={{ position: "absolute", left: LEFT, top: REF_TOP }}>
        <Waveform words={referenceWords} width={WIDTH} height={WAVE_HEIGHT} seed={5} barColor={color.reference} reveal={reveal} />
      </div>
      <WordLabels words={referenceWords} top={REF_TOP + WAVE_HEIGHT + 10} mergeFlagged={false} flagged={0} />
      <div style={{ position: "absolute", left: LEFT, top: REF_TOP + WAVE_HEIGHT + 56, fontSize: 30, color: color.ink2, fontWeight: 700 }}>Reference</div>
      <div
        style={{
          position: "absolute",
          right: 1920 - LEFT - WIDTH,
          top: YOU_TOP - 70,
          padding: "10px 22px",
          borderRadius: 12,
          backgroundColor: color.flagWash,
          border: `1px solid ${color.flag}`,
          color: color.ink,
          fontSize: 30,
          opacity: flag,
          translate: `0px ${interpolate(flag, [0, 1], [12, 0])}px`,
          whiteSpace: "nowrap",
        }}
      >
        Rushed, and the pause before “a new nation” is gone
      </div>
      <div
        style={{
          position: "absolute",
          right: 1920 - LEFT - WIDTH,
          top: REF_TOP + WAVE_HEIGHT + 56,
          fontSize: 32,
          color: color.ink,
          opacity: rise(frame, beatFrame(scene, 4), 20),
        }}
      >
        Fix: give “brought forth on this continent” the reference’s time, and keep the pause.
      </div>
    </SceneShell>
  );
};
