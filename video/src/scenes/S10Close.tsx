import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { rise } from "../components/anim";
import { SceneShell } from "../components/SceneShell";
import { color, font } from "../theme";
import type { SceneTiming } from "../timeline";

// The dashboard's mark: a reference stroke and a reading stroke that drift apart and meet again.
const REFERENCE_PATH = "M1 15 C5 15 6 5 10 5 S15 23 19 23 S24 9 28 9 S34 17 39 17";
const READING_PATH = "M1 13 C4 13 6 20 9 20 S14 4 18 4 S22 25 27 25 S34 11 39 11";
const PATH_LENGTH = 80;

export const S10Close: React.FC<{ scene: SceneTiming }> = () => {
  const frame = useCurrentFrame();
  const draw = rise(frame, 0, 40);
  return (
    <SceneShell>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 40, paddingBottom: 120 }}>
        <svg viewBox="0 0 40 28" width={260} height={182} style={{ overflow: "visible" }}>
          <path d={REFERENCE_PATH} fill="none" stroke={color.ink2} strokeWidth={2.2} strokeLinecap="round" pathLength={PATH_LENGTH} strokeDasharray={PATH_LENGTH} strokeDashoffset={PATH_LENGTH * (1 - draw)} />
          <path d={READING_PATH} fill="none" stroke={color.youText} strokeWidth={2.2} strokeLinecap="round" pathLength={PATH_LENGTH} strokeDasharray={PATH_LENGTH} strokeDashoffset={PATH_LENGTH * (1 - rise(frame, 6, 40))} />
        </svg>
        <div style={{ fontFamily: font.display, fontWeight: 500, fontSize: 120, letterSpacing: "-0.015em", opacity: rise(frame, 18, 22), translate: `0px ${interpolate(rise(frame, 18, 22), [0, 1], [18, 0])}px` }}>
          Contrastive Voice
        </div>
        <div style={{ fontSize: 44, color: color.ink2, opacity: rise(frame, 34, 22) }}>Record. Compare. Fix the exact words.</div>
      </AbsoluteFill>
    </SceneShell>
  );
};
