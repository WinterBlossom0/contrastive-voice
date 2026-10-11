import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { fadeOut, pop, rise } from "../components/anim";
import { lineTokens, type TimedToken } from "../components/cues";
import { Landscape } from "../components/Landscape";
import { KineticLine, LogoMark, type KineticWord } from "../components/Type";
import { color, font } from "../theme";
import { beatFrame, type SceneTiming } from "../timeline";

const TITLE = "Contrastive Voice";
const ACCENTS: Record<string, string> = { "off.": color.youText, which: color.action, "words,": color.action };

const toWords = (tokens: TimedToken[]): KineticWord[] => tokens.map((token) => ({ text: token.text, at: token.from, tint: ACCENTS[token.text] }));

// A beat of type: it holds until the next line starts, then lifts away.
const Beat: React.FC<{ end: number; top: number; children: React.ReactNode }> = ({ end, top, children }) => {
  const frame = useCurrentFrame();
  const leaving = 1 - fadeOut(frame, end + 8, 14);
  return (
    <div
      style={{
        position: "absolute",
        left: 160,
        right: 160,
        top,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        opacity: 1 - leaving,
        translate: `0px ${-40 * leaving}px`,
        filter: `blur(${6 * leaving}px)`,
      }}
    >
      {children}
    </div>
  );
};

// The three questions, one per row; each gets the site's pink tint under it, like a flagged stretch.
const Questions: React.FC<{ tokens: TimedToken[] }> = ({ tokens }) => {
  const frame = useCurrentFrame();
  const rows: TimedToken[][] = [];
  let row: TimedToken[] = [];
  tokens.forEach((token) => {
    row.push(token);
    if (token.text.endsWith("?")) {
      rows.push(row);
      row = [];
    }
  });
  if (row.length > 0) {
    rows.push(row);
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 22 }}>
      {rows.map((words, index) => {
        const start = words[0].from;
        const tint = rise(frame, start + 4, 18);
        return (
          <div key={index} style={{ position: "relative", padding: "2px 18px 10px" }}>
            <div
              style={{
                position: "absolute",
                left: 0,
                right: `${100 - 100 * tint}%`,
                top: 0,
                bottom: 0,
                borderRadius: "10px 10px 0 0",
                backgroundColor: color.tint,
                borderBottom: `3px solid ${color.flagBar}`,
                opacity: 0.9,
              }}
            />
            <KineticLine words={toWords(words)} style={{ position: "relative", fontFamily: font.display, fontSize: 70, fontWeight: 400, letterSpacing: "-0.01em", justifyContent: "center" }} />
          </div>
        );
      })}
    </div>
  );
};

const Title: React.FC<{ start: number }> = ({ start }) => {
  const frame = useCurrentFrame();
  const settle = rise(frame, start, 50);
  return (
    <div
      style={{
        display: "flex",
        fontFamily: font.display,
        fontWeight: 400,
        fontSize: 156,
        lineHeight: 1,
        letterSpacing: `${interpolate(settle, [0, 1], [0.06, -0.02])}em`,
        whiteSpace: "pre",
      }}
    >
      {TITLE.split("").map((letter, index) => {
        const shown = pop(frame, start + index * 1.6);
        return (
          <span
            key={index}
            style={{
              display: "inline-block",
              opacity: shown,
              translate: `0px ${interpolate(shown, [0, 1], [0.35, 0])}em`,
              filter: `blur(${interpolate(shown, [0, 1], [10, 0])}px)`,
            }}
          >
            {letter}
          </span>
        );
      })}
    </div>
  );
};

export const S01Hook: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const lines = scene.lines.map(lineTokens);
  const [first, second, questions, answer] = [0, 1, 2, 3].map((index) => lines[Math.min(index, lines.length - 1)]);
  const answerStart = beatFrame(scene, 3);
  // The answer line opens with the name; the title stands for it, and the rest of the line follows under it.
  const nameWords = TITLE.split(" ").length;
  const tagline = answer.slice(nameWords);
  const push = interpolate(frame, [0, scene.durationInFrames], [0, 1], { easing: Easing.bezier(0.33, 0, 0.2, 1), extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ color: color.ink, fontFamily: font.text }}>
      <Landscape push={push} rise={rise(frame, 0, 75)} glow={rise(frame, answerStart, 40)} />
      <Beat end={beatFrame(scene, 1)} top={300}>
        <KineticLine words={toWords(first)} style={{ fontFamily: font.display, fontSize: 92, letterSpacing: "-0.015em", justifyContent: "center" }} />
      </Beat>
      <Beat end={beatFrame(scene, 2)} top={300}>
        <KineticLine words={toWords(second)} style={{ fontFamily: font.display, fontSize: 80, letterSpacing: "-0.015em", justifyContent: "center", maxWidth: 1400 }} />
      </Beat>
      <Beat end={beatFrame(scene, 3)} top={190}>
        <Questions tokens={questions} />
      </Beat>
      <div style={{ position: "absolute", left: 0, right: 0, top: 170, display: "flex", flexDirection: "column", alignItems: "center", gap: 34 }}>
        <div style={{ opacity: rise(frame, answerStart - 6, 12) }}>
          <LogoMark size={150} draw={rise(frame, answerStart - 6, 36)} drawReading={rise(frame, answerStart, 36)} />
        </div>
        <Title start={answer.length > 0 ? answer[0].from : answerStart} />
        <KineticLine words={toWords(tagline)} style={{ fontFamily: font.display, fontSize: 52, color: color.ink2, justifyContent: "center", maxWidth: 1500 }} />
      </div>
      <AbsoluteFill style={{ backgroundColor: "#000", opacity: interpolate(frame, [0, 24], [1, 0], { extrapolateRight: "clamp" }) }} />
    </AbsoluteFill>
  );
};
