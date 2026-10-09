import type { WordSpan } from "./Waveform";

export const GETTYSBURG = "Four score and seven years ago our fathers brought forth on this continent a new nation".split(" ");

// Lays words on a 0..1 time axis; `stretch` gives each word's relative length and `gapAfter` the pause after it.
export const layoutWords = (words: string[], stretch: (index: number) => number, gapAfter: (index: number) => number): WordSpan[] => {
  const raw: { text: string; start: number; end: number }[] = [];
  let cursor = 0.02;
  words.forEach((text, index) => {
    const length = (0.4 + text.length * 0.12) * stretch(index);
    raw.push({ text, start: cursor, end: cursor + length });
    cursor += length + gapAfter(index);
  });
  const total = cursor + 0.02;
  return raw.map((span) => ({ text: span.text, start: span.start / total, end: span.end / total }));
};

// The demonstration flaw: "brought forth on this continent" rushed, with the pause before "a new nation" dropped.
export const RUSH_FIRST = 8;
export const RUSH_LAST = 12;
export const referenceWords = layoutWords(GETTYSBURG, () => 1, (index) => (index === 5 || index === 12 ? 0.9 : 0.12));
export const yourWords = layoutWords(
  GETTYSBURG,
  (index) => (index >= RUSH_FIRST && index <= RUSH_LAST ? 0.7 : 1.0),
  (index) => (index === 5 ? 0.9 : index >= RUSH_FIRST && index <= RUSH_LAST ? 0.03 : 0.12),
);
