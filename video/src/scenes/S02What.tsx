import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { pop, rise } from "../components/anim";
import { cueFrame } from "../components/cues";
import { Heading, SceneShell } from "../components/SceneShell";
import { Waveform, type WordSpan } from "../components/Waveform";
import { FADE_FIRST, referenceWords, RUSH_FIRST, RUSH_LAST, yourWords } from "../components/words";
import { color, font } from "../theme";
import { beatFrame, type SceneTiming } from "../timeline";

const LEFT = 160;
const WIDTH = 1600;
const YOU_TOP = 330;
const REF_TOP = 590;
const WAVE_HEIGHT = 120;
const STRIP_GAP = 10;
const STRIP_HEIGHT = 10;
// How far the reading starts out of step with the reference, in px.
const START_OFFSET = 110;

const fadingGain = (position: number) => interpolate(position, [yourWords[FADE_FIRST].start, 1], [1, 0.32], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

type Drift = { measure: string; label: string; start: number; end: number; severity: number; row: number };

// The drifts of the demonstration reading, in the order the page would list them by time.
const DRIFTS: Drift[] = [
  { measure: "Pace", label: "Rushed", start: yourWords[RUSH_FIRST].start, end: yourWords[RUSH_LAST].end, severity: 1, row: 0 },
  { measure: "Pauses", label: "Pause dropped", start: yourWords[RUSH_LAST].end - 0.012, end: yourWords[FADE_FIRST].start + 0.012, severity: 0.75, row: 1 },
  { measure: "Volume", label: "Fading", start: yourWords[FADE_FIRST].start, end: yourWords[yourWords.length - 1].end, severity: 0.85, row: 0 },
];
const MEASURES = ["Pace", "Pauses", "Pitch", "Emphasis", "Volume", "Clarity"];
const SOURCES = ["your best take", "a coach", "a speaker you admire"];
const SOURCE_CUES = ["best", "coach", "speaker"];

const WordLabels: React.FC<{ words: WordSpan[]; top: number; shift: number; opacity: number; hidden?: (index: number) => number }> = ({ words, top, shift, opacity, hidden }) => (
  <>
    {words.map((word, index) => (
      <div
        key={index}
        style={{
          position: "absolute",
          left: LEFT + shift + ((word.start + word.end) / 2) * WIDTH,
          top,
          translate: "-50% 0px",
          fontSize: 24,
          color: color.ink2,
          whiteSpace: "nowrap",
          opacity: opacity * (hidden === undefined ? 1 : 1 - hidden(index)),
        }}
      >
        {word.text}
      </div>
    ))}
  </>
);

const severityColor = (severity: number) => (severity > 0.9 ? color.flagBar : severity > 0.8 ? color.flag : "#8f3b68");

export const S02What: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const youIn = pop(frame, 4);
  const refIn = pop(frame, 14);
  const reveal = interpolate(frame, [6, 60], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const alignStart = beatFrame(scene, 1);
  const align = pop(frame, alignStart);
  const shift = START_OFFSET * (1 - align);
  const marks = cueFrame(scene, 1, "marks");
  const driftShown = DRIFTS.map((_, index) => rise(frame, marks + index * 9, 16));
  const chipsStart = cueFrame(scene, 1, "drifts");
  const rushLabelHidden = (index: number) => (index >= RUSH_FIRST ? Math.max(driftShown[0], driftShown[2]) : 0);
  return (
    <SceneShell>
      <Heading style={{ position: "absolute", left: LEFT, top: 92, fontSize: 60, opacity: rise(frame, 0, 20), translate: `0px ${interpolate(rise(frame, 0, 20), [0, 1], [16, 0])}px` }}>
        Your reading, against a <span style={{ color: color.refText }}>reference</span> of the same text
      </Heading>

      {/* Yours: lavender, a little out of step until the alignment pulls it into place. */}
      <div style={{ position: "absolute", left: LEFT, top: YOU_TOP - 108, fontSize: 28, fontWeight: 700, color: color.youText, opacity: youIn }}>Yours</div>
      <WordLabels words={yourWords} top={YOU_TOP - 38} shift={shift} opacity={youIn * rise(frame, 30, 20)} hidden={rushLabelHidden} />
      <div style={{ position: "absolute", left: LEFT + shift, top: YOU_TOP, opacity: youIn, translate: `${interpolate(youIn, [0, 1], [-240, 0])}px 0px` }}>
        <Waveform words={yourWords} width={WIDTH} height={WAVE_HEIGHT} seed={3} barColor={color.you} reveal={reveal} gain={fadingGain} />
        <div style={{ position: "absolute", left: 0, top: WAVE_HEIGHT + STRIP_GAP, width: WIDTH, height: STRIP_HEIGHT, borderRadius: 5, backgroundColor: color.stripCalm, opacity: rise(frame, marks - 10, 12) }} />
        {DRIFTS.map((drift, index) => (
          <React.Fragment key={drift.label}>
            <div
              style={{
                position: "absolute",
                left: drift.start * WIDTH,
                width: (drift.end - drift.start) * WIDTH,
                top: -6,
                height: WAVE_HEIGHT + STRIP_GAP + 6,
                borderRadius: "6px 6px 0 0",
                backgroundColor: color.tintFirm,
                mixBlendMode: "screen",
                opacity: driftShown[index],
                scale: `1 ${interpolate(driftShown[index], [0, 1], [0.6, 1])}`,
                transformOrigin: "50% 100%",
              }}
            />
            <div
              style={{
                position: "absolute",
                left: drift.start * WIDTH,
                width: (drift.end - drift.start) * WIDTH * driftShown[index],
                top: WAVE_HEIGHT + STRIP_GAP,
                height: STRIP_HEIGHT,
                borderRadius: 5,
                backgroundColor: severityColor(drift.severity),
              }}
            />
            <div
              style={{
                position: "absolute",
                left: ((drift.start + drift.end) / 2) * WIDTH,
                top: -48 - drift.row * 50,
                translate: `-50% ${interpolate(driftShown[index], [0, 1], [10, 0])}px`,
                padding: "4px 14px",
                borderRadius: 999,
                backgroundColor: "rgba(178, 73, 129, 0.22)",
                border: `1px solid ${color.flag}`,
                color: color.flagText,
                fontSize: 24,
                fontWeight: 700,
                whiteSpace: "nowrap",
                opacity: driftShown[index],
              }}
            >
              {drift.label}
            </div>
          </React.Fragment>
        ))}
      </div>

      {/* Word-by-word links, drawn left to right while the reading slides into step. */}
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
        {referenceWords.map((word, index) => {
          const fromX = LEFT + shift + ((yourWords[index].start + yourWords[index].end) / 2) * WIDTH;
          const toX = LEFT + ((word.start + word.end) / 2) * WIDTH;
          const progress = rise(frame, alignStart + index * 2, 18);
          const y1 = YOU_TOP + WAVE_HEIGHT + STRIP_GAP + STRIP_HEIGHT + 10;
          const y2 = REF_TOP - 12;
          const drifting = index >= RUSH_FIRST;
          const flagged = drifting ? Math.max(...DRIFTS.map((drift, k) => (yourWords[index].start < drift.end && yourWords[index].end > drift.start ? driftShown[k] : 0))) : 0;
          return (
            <line
              key={index}
              x1={fromX}
              y1={y1}
              x2={fromX + (toX - fromX) * progress}
              y2={y1 + (y2 - y1) * progress}
              stroke={flagged > 0 ? color.flagText : "rgba(237, 230, 218, 0.28)"}
              strokeOpacity={flagged > 0 ? 0.4 + 0.6 * flagged : 1}
              strokeWidth={flagged > 0 ? 2.5 : 1.6}
            />
          );
        })}
      </svg>

      {/* Reference: lake, from the right. */}
      <div style={{ position: "absolute", left: LEFT, top: REF_TOP, opacity: refIn, translate: `${interpolate(refIn, [0, 1], [240, 0])}px 0px` }}>
        <Waveform words={referenceWords} width={WIDTH} height={WAVE_HEIGHT} seed={5} barColor={color.ref} reveal={reveal} />
      </div>
      <WordLabels words={referenceWords} top={REF_TOP + WAVE_HEIGHT + 12} shift={0} opacity={refIn * rise(frame, 36, 20)} />
      <div style={{ position: "absolute", left: LEFT, top: REF_TOP + WAVE_HEIGHT + 62, display: "flex", alignItems: "center", gap: 16, opacity: refIn }}>
        <div style={{ fontSize: 28, fontWeight: 700, color: color.refText, marginRight: 8 }}>Reference</div>
        {SOURCES.map((source, index) => {
          const shown = pop(frame, cueFrame(scene, 0, SOURCE_CUES[index]));
          return (
            <div
              key={source}
              style={{
                padding: "5px 16px",
                borderRadius: 999,
                border: "1px solid rgba(33, 155, 161, 0.6)",
                backgroundColor: "rgba(33, 155, 161, 0.12)",
                color: color.refText,
                fontSize: 24,
                opacity: shown,
                translate: `0px ${interpolate(shown, [0, 1], [10, 0])}px`,
              }}
            >
              {source}
            </div>
          );
        })}
      </div>

      {/* The measures; the ones that drift here light up in the flag colour. */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 850, display: "flex", justifyContent: "center", gap: 18 }}>
        {MEASURES.map((measure, index) => {
          const shown = pop(frame, chipsStart + index * 3, true);
          const driftIndex = DRIFTS.findIndex((drift) => drift.measure === measure);
          const lit = driftIndex < 0 ? 0 : driftShown[driftIndex] * rise(frame, chipsStart + 8, 12);
          return (
            <div
              key={measure}
              style={{
                padding: "8px 24px",
                borderRadius: 999,
                fontFamily: font.text,
                fontSize: 28,
                fontWeight: 700,
                color: lit > 0.5 ? color.flagText : color.ink2,
                backgroundColor: `rgba(178, 73, 129, ${0.2 * lit})`,
                border: `1px solid ${lit > 0.5 ? color.flag : color.line}`,
                opacity: shown,
                scale: String(interpolate(shown, [0, 1], [0.7, 1])),
              }}
            >
              {measure}
            </div>
          );
        })}
      </div>
    </SceneShell>
  );
};
