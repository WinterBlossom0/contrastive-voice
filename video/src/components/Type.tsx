import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { color } from "../theme";
import { pop } from "./anim";

export type KineticWord = { text: string; at: number; tint?: string };

// Each word rises out of a soft blur at its own frame (the frame it is spoken, when the narration has word times).
export const KineticLine: React.FC<{ words: KineticWord[]; style?: React.CSSProperties; rise?: number }> = ({ words, style, rise = 0.45 }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ display: "flex", flexWrap: "wrap", columnGap: "0.26em", ...style }}>
      {words.map((word, index) => {
        const shown = pop(frame, word.at);
        return (
          <span
            key={`${index}-${word.text}`}
            style={{
              display: "inline-block",
              color: word.tint,
              opacity: shown,
              translate: `0px ${interpolate(shown, [0, 1], [rise, 0])}em`,
              filter: `blur(${interpolate(shown, [0, 1], [8, 0])}px)`,
            }}
          >
            {word.text}
          </span>
        );
      })}
    </div>
  );
};

// The dashboard's mark: a reference stroke and a reading stroke that drift apart and meet again.
const REFERENCE_PATH = "M1 15 C5 15 6 5 10 5 S15 23 19 23 S24 9 28 9 S34 17 39 17";
const READING_PATH = "M1 13 C4 13 6 20 9 20 S14 4 18 4 S22 25 27 25 S34 11 39 11";
const PATH_LENGTH = 80;

export const LogoMark: React.FC<{ size: number; draw: number; drawReading?: number }> = ({ size, draw, drawReading = draw }) => (
  <svg viewBox="0 0 40 28" width={size} height={(size * 28) / 40} style={{ overflow: "visible", display: "block" }}>
    <path d={REFERENCE_PATH} fill="none" stroke={color.ink2} strokeWidth={2.2} strokeLinecap="round" pathLength={PATH_LENGTH} strokeDasharray={PATH_LENGTH} strokeDashoffset={PATH_LENGTH * (1 - draw)} />
    <path d={READING_PATH} fill="none" stroke={color.youText} strokeWidth={2.2} strokeLinecap="round" pathLength={PATH_LENGTH} strokeDasharray={PATH_LENGTH} strokeDashoffset={PATH_LENGTH * (1 - drawReading)} />
  </svg>
);
