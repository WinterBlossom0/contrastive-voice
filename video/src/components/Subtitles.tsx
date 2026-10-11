import React from "react";
import { AbsoluteFill, interpolate, Sequence, useCurrentFrame, useVideoConfig } from "remotion";
import { color, font, SUBTITLE_TOP } from "../theme";
import type { SceneTiming, TimedLine } from "../timeline";
import { hasWordTimes, lineTokens, type TimedToken } from "./cues";

const MAX_CHARS = 60;

type Chunk = { tokens: TimedToken[]; from: number; durationInFrames: number };

// A quoted name opens with a word that starts with a quote mark and closes with a word that ends with one before its punctuation.
const opensQuote = (word: string): boolean => /^['‘"“]/.test(word);
const closesQuote = (word: string): boolean => /['’"”][.,:;!?]*$/.test(word);
const endsClause = (word: string): boolean => /[.,:;!?…]['’"”]?$/.test(word);
// Cost of a break that is not after punctuation, in squared characters of length difference.
const MID_CLAUSE_COST = 400;

// Long lines become one-line chunks of about equal length, broken after punctuation where it costs little length balance
// (dynamic programming over the break points); a chunk never ends inside a quoted name. A chunk shows from its first
// word to the next chunk's first word, so the band never goes blank inside a line.
export const splitLine = (line: TimedLine): Chunk[] => {
  const tokens = lineTokens(line);
  const pieces = Math.max(1, Math.ceil(line.text.length / MAX_CHARS));
  const target = line.text.length / pieces;
  const insideQuote: boolean[] = [];
  let open = false;
  tokens.forEach((token) => {
    if (opensQuote(token.text)) {
      open = true;
    }
    if (closesQuote(token.text)) {
      open = false;
    }
    insideQuote.push(open);
  });
  const length = (from: number, to: number) => tokens.slice(from, to).reduce((sum, token) => sum + token.text.length + 1, -1);
  const mostPieces = pieces + 1;
  // best[k][i]: the lowest cost of the first i tokens in k chunks, and where its last chunk starts.
  const best: { cost: number; start: number }[][] = Array.from({ length: mostPieces + 1 }, () => tokens.map(() => ({ cost: Number.POSITIVE_INFINITY, start: 0 })).concat([{ cost: Number.POSITIVE_INFINITY, start: 0 }]));
  best[0][0] = { cost: 0, start: 0 };
  for (let k = 1; k <= mostPieces; k += 1) {
    for (let end = 1; end <= tokens.length; end += 1) {
      const last = end === tokens.length;
      if (!last && insideQuote[end - 1]) {
        continue;
      }
      for (let start = 0; start < end; start += 1) {
        const before = best[k - 1][start].cost;
        if (!Number.isFinite(before) || length(start, end) > MAX_CHARS + 8) {
          continue;
        }
        const cost = before + (length(start, end) - target) ** 2 + (last || endsClause(tokens[end - 1].text) ? 0 : MID_CLAUSE_COST);
        if (cost < best[k][end].cost) {
          best[k][end] = { cost, start };
        }
      }
    }
  }
  const chunkCount = [pieces, mostPieces].find((k) => Number.isFinite(best[k][tokens.length].cost)) ?? 0;
  const groups: TimedToken[][] = [];
  let end = tokens.length;
  for (let k = chunkCount; k >= 1 && Number.isFinite(best[k][end].cost); k -= 1) {
    const start = best[k][end].start;
    groups.unshift(tokens.slice(start, end));
    end = start;
  }
  if (groups.length === 0) {
    groups.push(tokens);
  }
  const lineEnd = line.from + line.durationInFrames;
  return groups.map((group, index) => {
    const from = index === 0 ? line.from : group[0].from;
    const to = index === groups.length - 1 ? lineEnd : groups[index + 1][0].from;
    return { tokens: group, from, durationInFrames: Math.max(1, to - from) };
  });
};

// The band fades in at the start of a line; the next chunks of the same line replace the text in place.
const Band: React.FC<{ children: React.ReactNode; quiet?: boolean; fade: boolean }> = ({ children, quiet, fade }) => {
  const frame = useCurrentFrame();
  const shown = fade ? interpolate(frame, [0, 5], [0, 1], { extrapolateRight: "clamp" }) : 1;
  return (
    <AbsoluteFill style={{ top: SUBTITLE_TOP, height: 1080 - SUBTITLE_TOP, alignItems: "center", justifyContent: "center" }}>
      <div
        style={{
          maxWidth: 1640,
          padding: "10px 28px 12px",
          borderRadius: 14,
          backgroundColor: "rgba(24, 23, 22, 0.82)",
          border: "1px solid rgba(237, 230, 218, 0.06)",
          color: quiet ? color.ink2 : color.ink,
          fontFamily: font.text,
          fontSize: quiet ? 34 : 42,
          lineHeight: 1.25,
          textAlign: "center",
          whiteSpace: quiet ? "normal" : "nowrap",
          opacity: shown,
          translate: `0px ${interpolate(shown, [0, 1], [6, 0])}px`,
        }}
      >
        {children}
      </div>
    </AbsoluteFill>
  );
};

// Karaoke: spoken words in full cream, the word being spoken underlined in clay as it is said, words to come dimmed.
const KaraokeChunk: React.FC<{ chunk: Chunk; karaoke: boolean; fade: boolean }> = ({ chunk, karaoke, fade }) => {
  const frame = useCurrentFrame() + chunk.from;
  return (
    <Band fade={fade}>
      {chunk.tokens.map((token, index) => {
        const said = !karaoke || frame >= token.from;
        const saying = karaoke && frame >= token.from && frame < Math.max(token.to, token.from + 4);
        const sweep = saying ? interpolate(frame, [token.from, Math.max(token.to, token.from + 4)], [0, 1]) : said ? 1 : 0;
        return (
          <React.Fragment key={index}>
            {index > 0 ? " " : null}
            <span
              style={{
                position: "relative",
                display: "inline-block",
                color: said ? color.ink : "rgba(237, 230, 218, 0.42)",
              }}
            >
              {token.text}
              {karaoke ? (
                <span
                  style={{
                    position: "absolute",
                    left: 0,
                    bottom: -3,
                    height: 3,
                    width: `${100 * sweep}%`,
                    borderRadius: 2,
                    backgroundColor: color.action,
                    opacity: saying ? 1 : 0,
                  }}
                />
              ) : null}
            </span>
          </React.Fragment>
        );
      })}
    </Band>
  );
};

export const Subtitles: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const { fps } = useVideoConfig();
  return (
    <>
      {scene.lines.flatMap((line, lineIndex) =>
        splitLine(line).map((chunk, chunkIndex) => (
          <Sequence key={`${lineIndex}-${chunkIndex}`} name={`Subtitle ${lineIndex + 1}.${chunkIndex + 1}`} from={chunk.from} durationInFrames={chunk.durationInFrames} premountFor={fps}>
            <KaraokeChunk chunk={chunk} karaoke={hasWordTimes(line)} fade={chunkIndex === 0} />
          </Sequence>
        )),
      )}
      {scene.clip !== null && scene.clip.caption.length > 0 ? (
        <Sequence name="Clip caption" from={scene.clip.from} durationInFrames={scene.clip.durationInFrames} premountFor={fps}>
          <Band quiet fade>
            {scene.clip.caption}
          </Band>
        </Sequence>
      ) : null}
    </>
  );
};
