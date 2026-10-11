import React, { useMemo } from "react";
import { useCurrentFrame } from "remotion";
import { seeded } from "./anim";

export type WordSpan = { text: string; start: number; end: number };

type Props = {
  words: WordSpan[];
  width: number;
  height: number;
  seed: number;
  barColor: string;
  // Share of the width drawn so far, 0 to 1.
  reveal?: number;
  // Loudness factor at a position 0 to 1 of the width, for a reading that fades.
  gain?: (position: number) => number;
};

const BAR_STEP = 7;

// Bars are loud inside words and near silent in the gaps, so pauses read as pauses.
export const Waveform: React.FC<Props> = ({ words, width, height, seed, barColor, reveal = 1, gain }) => {
  const frame = useCurrentFrame();
  const bars = useMemo(() => {
    const random = seeded(seed);
    const count = Math.floor(width / BAR_STEP);
    return Array.from({ length: count }, (_, index) => {
      const position = (index + 0.5) / count;
      const word = words.find((span) => position >= span.start && position <= span.end);
      if (word === undefined) {
        return { position, amplitude: 0.04 + random() * 0.04, phase: random() * Math.PI * 2 };
      }
      const inside = (position - word.start) / (word.end - word.start);
      const envelope = Math.sin(Math.PI * Math.min(1, Math.max(0, inside))) ** 0.6;
      const loudness = gain === undefined ? 1 : gain(position);
      return { position, amplitude: (0.18 + envelope * (0.45 + random() * 0.4)) * loudness, phase: random() * Math.PI * 2 };
    });
  }, [words, width, seed, gain]);

  return (
    <svg width={width} height={height} style={{ display: "block", overflow: "visible" }}>
      {bars.map((bar, index) => {
        if (bar.position > reveal) {
          return null;
        }
        const breathing = 1 + 0.06 * Math.sin(frame / 9 + bar.phase);
        const barHeight = Math.max(3, bar.amplitude * breathing * height);
        return <rect key={index} x={index * BAR_STEP} y={(height - barHeight) / 2} width={BAR_STEP - 3} height={barHeight} rx={2} fill={barColor} opacity={0.9} />;
      })}
    </svg>
  );
};
