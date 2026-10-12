import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { fadeOut, pop, rise, seeded } from "../components/anim";
import { cueFrame } from "../components/cues";
import { Heading, SceneShell } from "../components/SceneShell";
import { referenceWords, yourWords } from "../components/words";
import { color, font } from "../theme";
import { FPS, type SceneTiming } from "../timeline";

const LEFT = 160;
const WIDTH = 1600;
const STEPS = ["Align", "Own voice", "Threshold"];
// The word of the narration line that starts each step.
const STEP_CUES = ["wav2vec", "Pitch", "only"];
// Both readings span this many seconds on the alignment panel's time labels.
const READING_SEC = 6.4;

const stepStarts = (scene: SceneTiming): number[] => STEP_CUES.map((cue, index) => (index === 0 ? 0 : cueFrame(scene, 0, cue)));

// Panel `index` slides in from the right at its step and out to the left at the next step.
const Panel: React.FC<{ starts: number[]; index: number; children: React.ReactNode }> = ({ starts, index, children }) => {
  const frame = useCurrentFrame();
  const start = starts[index];
  const last = index === STEPS.length - 1;
  const enter = pop(frame, start);
  const leave = last ? 0 : 1 - fadeOut(frame, starts[index + 1] + 10, 14);
  return (
    <div
      style={{
        position: "absolute",
        left: LEFT,
        top: 280,
        width: WIDTH,
        height: 620,
        opacity: enter * (1 - leave),
        translate: `${interpolate(enter, [0, 1], [80, 0]) - 80 * leave}px 0px`,
      }}
    >
      {children}
    </div>
  );
};

const Caption: React.FC<{ children: React.ReactNode; top: number }> = ({ children, top }) => (
  <div style={{ position: "absolute", left: 0, right: 0, top, textAlign: "center", fontFamily: font.display, fontSize: 40, color: color.ink }}>{children}</div>
);

const AlignPanel: React.FC<{ start: number; sweepFrames: number }> = ({ start, sweepFrames }) => {
  const frame = useCurrentFrame();
  const head = interpolate(frame, [start + 6, start + 6 + sweepFrames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const row = (words: typeof yourWords, top: number, tint: string, label: string) => (
    <>
      <div style={{ position: "absolute", left: 0, top: top - 70, fontSize: 26, fontWeight: 700, color: tint }}>{label}</div>
      {words.map((word, index) => {
        const shown = rise(frame, start + 6 + word.start * sweepFrames, 8);
        return (
          <React.Fragment key={index}>
            <div style={{ position: "absolute", left: word.start * WIDTH, top: top - 30, fontFamily: font.mono, fontSize: 15, color: color.muted, opacity: shown }}>
              {(word.start * READING_SEC).toFixed(2)}
            </div>
            <div
              style={{
                position: "absolute",
                left: word.start * WIDTH,
                top,
                width: Math.max(8, (word.end - word.start) * WIDTH - 4),
                height: 64,
                borderRadius: 10,
                border: `1.5px solid ${tint}`,
                backgroundColor: "rgba(38, 38, 36, 0.85)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                overflow: "hidden",
                fontSize: Math.min(24, ((word.end - word.start) * WIDTH - 10) / (word.text.length * 0.55)),
                color: color.ink,
                opacity: shown,
                scale: `${interpolate(shown, [0, 1], [0.3, 1])} 1`,
                transformOrigin: "0% 50%",
              }}
            >
              {word.text}
            </div>
          </React.Fragment>
        );
      })}
    </>
  );
  return (
    <>
      {row(yourWords, 110, color.you, "Yours")}
      {row(referenceWords, 310, color.ref, "Reference")}
      <div style={{ position: "absolute", left: head * WIDTH - 1, top: 20, width: 3, height: 380, borderRadius: 2, backgroundColor: color.action, boxShadow: `0 0 18px ${color.action}`, opacity: head > 0 && head < 1 ? 1 : 0 }} />
      <Caption top={470}>A wav2vec 2.0 aligner gives every word a start and an end</Caption>
    </>
  );
};

// A pitch contour around its own median, in px; `wobble` gives each voice its own melody.
const contour = (median: number, wobble: number, seed: number) => {
  const random = seeded(seed);
  const phases = [random() * 6, random() * 6];
  return Array.from({ length: 60 }, (_, index) => {
    const x = (index / 59) * 1200;
    const y = median - wobble * (Math.sin(index / 5 + phases[0]) * 0.7 + Math.sin(index / 2.3 + phases[1]) * 0.3);
    return `${index === 0 ? "M" : "L"}${x.toFixed(1)} ${y.toFixed(1)}`;
  }).join(" ");
};

const NormalisePanel: React.FC<{ scene: SceneTiming; start: number }> = ({ scene, start }) => {
  const frame = useCurrentFrame();
  const draw = rise(frame, start + 4, 30);
  const together = pop(frame, cueFrame(scene, 0, "against"));
  const verdict = pop(frame, cueFrame(scene, 0, "own"), true);
  const centre = 240;
  const deep = centre + 140 * (1 - together);
  const high = centre - 140 * (1 - together);
  return (
    <>
      <svg width={1200} height={440} style={{ position: "absolute", left: 200, top: 0, overflow: "visible" }}>
        <line x1={0} x2={1200} y1={centre} y2={centre} stroke={color.ink2} strokeDasharray="6 8" strokeOpacity={0.6 * together} />
        <line x1={0} x2={1200} y1={deep} y2={deep} stroke={color.ref} strokeDasharray="4 8" strokeOpacity={0.6 * (1 - together)} />
        <line x1={0} x2={1200} y1={high} y2={high} stroke={color.you} strokeDasharray="4 8" strokeOpacity={0.6 * (1 - together)} />
        <path d={contour(0, 60, 7)} transform={`translate(0 ${deep})`} fill="none" stroke={color.ref} strokeWidth={4} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
        <path d={contour(0, 66, 11)} transform={`translate(0 ${high})`} fill="none" stroke={color.you} strokeWidth={4} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
      </svg>
      <div style={{ position: "absolute", left: 200, top: -10, display: "flex", gap: 40, fontSize: 26, fontWeight: 700, opacity: draw }}>
        <span style={{ color: color.youText }}>━ Higher voice</span>
        <span style={{ color: color.refText }}>━ Deeper voice</span>
      </div>
      <div style={{ position: "absolute", left: 1420, top: centre - 18, fontSize: 24, color: color.ink2, whiteSpace: "nowrap", opacity: together }}>own median</div>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 480,
          display: "flex",
          justifyContent: "center",
          opacity: verdict,
          translate: `0px ${interpolate(verdict, [0, 1], [14, 0])}px`,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 16, fontFamily: font.display, fontSize: 40 }}>
          Pitch and volume against each speaker&apos;s own voice
        </div>
      </div>
    </>
  );
};

const HISTOGRAM = Array.from({ length: 28 }, (_, index) => Math.exp(-((index / 7) ** 2) / 2));
const THRESHOLD_AT = 0.62;
const DIFFERENCES = [0.12, 0.31, 0.47, 0.22, 0.83, 0.56, 0.09, 0.71, 0.38, 0.92];

const ThresholdPanel: React.FC<{ scene: SceneTiming; start: number }> = ({ scene, start }) => {
  const frame = useCurrentFrame();
  const chartWidth = 1300;
  const base = 360;
  const threshold = rise(frame, cueFrame(scene, 0, "thresholds"), 20);
  const drops = cueFrame(scene, 0, "differences");
  const fitted = cueFrame(scene, 0, "flawless");
  return (
    <>
      <div style={{ position: "absolute", left: 150, top: 0, width: chartWidth, height: 420 }}>
        {HISTOGRAM.map((height, index) => {
          const grow = rise(frame, start + 4 + index, 16);
          return (
            <div
              key={index}
              style={{
                position: "absolute",
                left: (index / HISTOGRAM.length) * chartWidth,
                bottom: 420 - base,
                width: chartWidth / HISTOGRAM.length - 6,
                height: height * 230 * grow,
                borderRadius: "6px 6px 0 0",
                backgroundColor: "rgba(237, 230, 218, 0.22)",
              }}
            />
          );
        })}
        <div style={{ position: "absolute", left: 0, top: base, width: chartWidth, height: 2, backgroundColor: color.line }} />
        <div style={{ position: "absolute", left: 0, top: base + 14, fontSize: 22, color: color.muted }}>difference from the reference →</div>
        <div style={{ position: "absolute", left: 0, top: base - 270, fontSize: 24, color: color.ink2, opacity: rise(frame, fitted, 16) }}>flawless comparisons</div>
        <div style={{ position: "absolute", left: THRESHOLD_AT * chartWidth - 2, top: base - 300 + 300 * (1 - threshold), width: 4, height: 300 * threshold, borderRadius: 2, backgroundColor: color.action, boxShadow: `0 0 16px ${color.action}` }} />
        <div style={{ position: "absolute", left: THRESHOLD_AT * chartWidth + 16, top: base - 300, fontSize: 26, fontWeight: 700, color: color.action, opacity: threshold }}>threshold</div>
        {DIFFERENCES.map((value, index) => {
          const fall = pop(frame, drops + index * 4, true);
          const flagged = value > THRESHOLD_AT;
          const settled = Math.min(rise(frame, drops + index * 4 + 10, 8), threshold);
          return (
            <div
              key={index}
              style={{
                position: "absolute",
                left: value * chartWidth - 13,
                top: interpolate(fall, [0, 1], [-60, base - 40]),
                width: 26,
                height: 26,
                borderRadius: 13,
                backgroundColor: flagged ? `rgba(238, 152, 191, ${0.4 + 0.6 * settled})` : color.ink2,
                boxShadow: flagged ? `0 0 ${18 * settled}px ${color.flag}` : "none",
                opacity: Math.min(1, fall * 2),
              }}
            />
          );
        })}
      </div>
      <Caption top={460}>
        Only differences past the threshold are <span style={{ color: color.flagText }}>flagged</span>
      </Caption>
    </>
  );
};

export const S13How: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const starts = stepStarts(scene);
  const active = starts.filter((start) => frame >= start).length - 1;
  const railProgress = interpolate(frame, starts, starts.map((_, index) => index / (STEPS.length - 1)), { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const railShown = rise(frame, 4, 20);
  const sweepFrames = Math.max(FPS, Math.round((starts[1] - starts[0]) * 0.8));
  return (
    <SceneShell>
      <Heading style={{ position: "absolute", left: LEFT, top: 80, fontSize: 60, opacity: rise(frame, 0, 18) }}>Under the hood</Heading>
      <div style={{ position: "absolute", left: LEFT + 40, top: 196, width: WIDTH - 80, height: 3, backgroundColor: color.line, opacity: railShown }}>
        <div style={{ width: `${railProgress * 100}%`, height: "100%", backgroundColor: color.action }} />
      </div>
      {STEPS.map((step, index) => {
        const x = LEFT + 40 + (index / (STEPS.length - 1)) * (WIDTH - 80);
        const lit = index <= active;
        const now = pop(frame, starts[index], true);
        return (
          <div key={step} style={{ position: "absolute", left: x, top: 197, translate: "-50% -50%", display: "flex", flexDirection: "column", alignItems: "center", opacity: railShown }}>
            <div
              style={{
                width: 26,
                height: 26,
                borderRadius: 13,
                backgroundColor: lit ? color.action : color.panel3,
                border: `3px solid ${lit ? "#f0a487" : color.panel3}`,
                scale: String(index === active ? interpolate(now, [0, 1], [1, 1.25]) : 1),
                boxShadow: index === active ? `0 0 22px ${color.action}` : "none",
              }}
            />
            <div style={{ position: "absolute", top: 36, fontSize: 26, fontWeight: 700, color: index === active ? color.ink : lit ? color.ink2 : color.muted, whiteSpace: "nowrap" }}>
              {step}
            </div>
          </div>
        );
      })}
      <Panel starts={starts} index={0}>
        <AlignPanel start={starts[0]} sweepFrames={sweepFrames} />
      </Panel>
      <Panel starts={starts} index={1}>
        <NormalisePanel scene={scene} start={starts[1]} />
      </Panel>
      <Panel starts={starts} index={2}>
        <ThresholdPanel scene={scene} start={starts[2]} />
      </Panel>
    </SceneShell>
  );
};
