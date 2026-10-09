import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { rise } from "../components/anim";
import { Heading, SceneShell } from "../components/SceneShell";
import { Waveform } from "../components/Waveform";
import { yourWords } from "../components/words";
import { color } from "../theme";
import { beatFrame, type SceneTiming } from "../timeline";

// Short tags, so the screen does not repeat the narrated questions word for word.
const GUESSES = ["Pace?", "Pauses?", "Volume?"];

export const S1Hook: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const guesses = beatFrame(scene, 2);
  const answer = rise(frame, beatFrame(scene, 3), 22);
  return (
    <SceneShell>
      <div style={{ position: "absolute", left: 160, top: 170, width: 1600 }}>
        <Heading style={{ fontSize: 112, opacity: rise(frame, 4, 24), translate: `0px ${interpolate(rise(frame, 4, 24), [0, 1], [24, 0])}px` }}>
          You practise a speech.
        </Heading>
        <div style={{ marginTop: 56, opacity: rise(frame, 14, 20) }}>
          <Waveform words={yourWords} width={1600} height={170} seed={11} barColor={color.accent} reveal={interpolate(frame, [14, 14 + 70], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })} />
        </div>
        <div style={{ display: "flex", gap: 22, marginTop: 44 }}>
          {GUESSES.map((remark, index) => (
            <div
              key={remark}
              style={{
                padding: "12px 26px",
                borderRadius: 999,
                border: `1px solid ${color.line}`,
                backgroundColor: color.surface,
                color: color.ink2,
                fontSize: 38,
                opacity: rise(frame, guesses + index * 22, 16) * interpolate(answer, [0, 1], [1, 0.35]),
              }}
            >
              {remark}
            </div>
          ))}
        </div>
        <Heading style={{ fontSize: 96, marginTop: 70, opacity: answer, translate: `0px ${interpolate(answer, [0, 1], [24, 0])}px` }}>
          Which <span style={{ color: color.accentText }}>words</span> to fix, and how
        </Heading>
      </div>
    </SceneShell>
  );
};
