import { FPS, type SceneTiming, type TimedLine } from "../timeline";

// A word of the line text as shown on screen, with its spoken span in scene frames.
export type TimedToken = { text: string; from: number; to: number };

const normalized = (text: string) => text.toLowerCase().replace(/[^a-z0-9]/g, "");
// The spoken words may spell a number out ("0.87" as four words), so a match may skip this many spoken words.
const MATCH_REACH = 8;

// Tokens without a matched spoken word share the time between their matched neighbours by character count.
const fillByChars = (tokens: string[], spans: ([number, number] | null)[], lineSec: number): [number, number][] => {
  const filled = [...spans];
  let index = 0;
  while (index < tokens.length) {
    if (filled[index] !== null) {
      index += 1;
      continue;
    }
    let runEnd = index;
    while (runEnd < tokens.length && filled[runEnd] === null) {
      runEnd += 1;
    }
    const startSec = index === 0 ? 0 : (filled[index - 1] as [number, number])[1];
    const endSec = runEnd === tokens.length ? lineSec : (filled[runEnd] as [number, number])[0];
    const chars = tokens.slice(index, runEnd).map((token) => token.length + 1);
    const total = chars.reduce((sum, count) => sum + count, 0);
    let cursor = startSec;
    for (let k = index; k < runEnd; k += 1) {
      const length = ((endSec - startSec) * chars[k - index]) / total;
      filled[k] = [cursor, cursor + length];
      cursor += length;
    }
    index = runEnd;
  }
  return filled as [number, number][];
};

// The line text split at spaces; each token takes the time of its spoken word when narration.json gives word times.
export const lineTokens = (line: TimedLine): TimedToken[] => {
  const tokens = line.text.split(/\s+/).filter((token) => token.length > 0);
  const lineSec = line.durationInFrames / FPS;
  const words = line.words ?? [];
  const spans: ([number, number] | null)[] = tokens.map(() => null);
  let next = 0;
  tokens.forEach((token, index) => {
    const key = normalized(token);
    if (key.length === 0) {
      return;
    }
    for (let k = next; k < Math.min(words.length, next + MATCH_REACH); k += 1) {
      if (normalized(words[k][0]) === key) {
        spans[index] = [words[k][1], words[k][2]];
        next = k + 1;
        return;
      }
    }
  });
  return fillByChars(tokens, spans, lineSec).map(([start, end], index) => ({
    text: tokens[index],
    from: line.from + Math.round(start * FPS),
    to: line.from + Math.round(end * FPS),
  }));
};

export const hasWordTimes = (line: TimedLine): boolean => (line.words ?? []).length > 0;

const clampLine = (scene: SceneTiming, lineIndex: number): TimedLine | undefined =>
  scene.lines[Math.min(Math.max(0, lineIndex), scene.lines.length - 1)];

// The frame at which `phrase` starts to be spoken in line `lineIndex`; the line start when the phrase is not in it.
export const cueFrame = (scene: SceneTiming, lineIndex: number, phrase: string): number => {
  const line = clampLine(scene, lineIndex);
  if (line === undefined) {
    return 0;
  }
  const tokens = lineTokens(line);
  const wanted = phrase.split(/\s+/).map(normalized);
  const found = tokens.findIndex((_, index) => wanted.every((word, offset) => tokens[index + offset] !== undefined && normalized(tokens[index + offset].text) === word));
  return found < 0 ? line.from : tokens[found].from;
};
