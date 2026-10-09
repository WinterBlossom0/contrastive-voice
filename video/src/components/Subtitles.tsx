import React from "react";
import { AbsoluteFill, Sequence, useVideoConfig } from "remotion";
import { color, font, SUBTITLE_TOP } from "../theme";
import type { SceneTiming } from "../timeline";

const MAX_CHARS = 62;

type Chunk = { text: string; from: number; durationInFrames: number };

// Long sentences become several one-line chunks; each chunk's time share follows its character count.
const splitLine = (text: string, from: number, durationInFrames: number): Chunk[] => {
  const words = text.split(/\s+/).filter((word) => word.length > 0);
  const pieces = Math.max(1, Math.ceil(text.length / MAX_CHARS));
  const target = text.length / pieces;
  const chunks: string[] = [];
  let current = "";
  for (const word of words) {
    const candidate = current.length === 0 ? word : `${current} ${word}`;
    if (current.length > 0 && candidate.length > target && chunks.length < pieces - 1) {
      chunks.push(current);
      current = word;
    } else {
      current = candidate;
    }
  }
  chunks.push(current);
  const totalChars = chunks.reduce((sum, chunk) => sum + chunk.length, 0);
  let charCursor = 0;
  return chunks.map((chunk) => {
    const start = from + Math.round((charCursor / totalChars) * durationInFrames);
    charCursor += chunk.length;
    const end = from + Math.round((charCursor / totalChars) * durationInFrames);
    return { text: chunk, from: start, durationInFrames: Math.max(1, end - start) };
  });
};

const SubtitleText: React.FC<{ text: string; quiet?: boolean }> = ({ text, quiet }) => (
  <AbsoluteFill style={{ top: SUBTITLE_TOP, height: 1080 - SUBTITLE_TOP, alignItems: "center", justifyContent: "center" }}>
    <div
      style={{
        maxWidth: 1600,
        padding: "10px 26px",
        borderRadius: 12,
        backgroundColor: "rgba(18, 18, 18, 0.82)",
        color: quiet ? color.ink2 : color.ink,
        fontFamily: font.text,
        fontStyle: quiet ? "italic" : "normal",
        fontSize: quiet ? 36 : 44,
        lineHeight: 1.25,
        textAlign: "center",
        whiteSpace: quiet ? "normal" : "nowrap",
      }}
    >
      {text}
    </div>
  </AbsoluteFill>
);

export const Subtitles: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const { fps } = useVideoConfig();
  return (
    <>
      {scene.lines.flatMap((line, lineIndex) =>
        splitLine(line.text, line.from, line.durationInFrames).map((chunk, chunkIndex) => (
          <Sequence
            key={`${lineIndex}-${chunkIndex}`}
            name={`Subtitle ${lineIndex + 1}.${chunkIndex + 1}`}
            from={chunk.from}
            durationInFrames={chunk.durationInFrames}
            premountFor={fps}
           
          >
            <SubtitleText text={chunk.text} />
          </Sequence>
        )),
      )}
      {scene.clip !== null && scene.clip.caption.length > 0 ? (
        <Sequence name="Clip caption" from={scene.clip.from} durationInFrames={scene.clip.durationInFrames} premountFor={fps}>
          <SubtitleText text={scene.clip.caption} quiet />
        </Sequence>
      ) : null}
    </>
  );
};
