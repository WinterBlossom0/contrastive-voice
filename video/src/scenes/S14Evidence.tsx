import React from "react";
import { Easing, interpolate, useCurrentFrame } from "remotion";
import { pop, rise } from "../components/anim";
import { cueFrame } from "../components/cues";
import { Heading, SceneShell } from "../components/SceneShell";
import { color, font } from "../theme";
import type { SceneTiming } from "../timeline";

// Every number below is from docs/technical.md: 2,410 files = 9 baselines + 448 edited clips + 1,953 reader recordings;
// test F1 0.812 pre-registered; 22 of 22 repairs clear their flag while the placebo keeps it (section 10); zero false
// regions on unedited copies; 0.46 false regions per comparison-minute with a different reader (lockbox, one reference).
const FILES = 2410;
const F1_PLANNED = 0.812;
export const COUNT_FRAMES = 40;
const EDIT_FACTS = ["type", "place", "size"];

const countEase = Easing.bezier(0.16, 1, 0.3, 1);
const counted = (frame: number, start: number) => interpolate(frame, [start, start + COUNT_FRAMES], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: countEase });

const Ring: React.FC<{ value: number; progress: number; size: number; tint: string }> = ({ value, progress, size, tint }) => {
  const radius = size / 2 - 10;
  const circumference = 2 * Math.PI * radius;
  return (
    <div style={{ position: "relative", width: size, height: size }}>
      <svg width={size} height={size} style={{ position: "absolute", left: 0, top: 0, rotate: "-90deg" }}>
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke={color.panel3} strokeWidth={12} />
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke={tint} strokeWidth={12} strokeLinecap="round" strokeDasharray={circumference} strokeDashoffset={circumference * (1 - value * progress)} />
      </svg>
      <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: font.display, fontSize: size * 0.27, fontVariantNumeric: "lining-nums tabular-nums" }}>
        {(value * progress).toFixed(3)}
      </div>
    </div>
  );
};

const Score: React.FC<{ value: number; start: number; tint: string; title: string; detail: string }> = ({ value, start, tint, title, detail }) => {
  const frame = useCurrentFrame();
  const shown = pop(frame, start, true);
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 34, opacity: Math.min(1, shown * 1.5), scale: String(interpolate(shown, [0, 1], [0.85, 1])) }}>
      <Ring value={value} progress={counted(frame, start)} size={210} tint={tint} />
      <div>
        <div style={{ fontFamily: font.display, fontSize: 44, lineHeight: 1.1 }}>{title}</div>
        <div style={{ fontSize: 28, color: color.ink2, marginTop: 8 }}>{detail}</div>
      </div>
    </div>
  );
};

// The frames at which each number starts to count or appears; SoundEffects.tsx plays its sounds on the same frames.
export const evidenceBeats = (scene: SceneTiming) => ({
  files: cueFrame(scene, 0, "2,410"),
  speeches: cueFrame(scene, 0, "nine"),
  edited: cueFrame(scene, 0, "448"),
  readers: cueFrame(scene, 0, "1,953"),
  scores: cueFrame(scene, 1, "F1"),
  repairs: cueFrame(scene, 1, "22"),
  clean: cueFrame(scene, 2, "zero"),
  reader: cueFrame(scene, 2, "different"),
});

const Row: React.FC<{ start: number; value: string; children: React.ReactNode }> = ({ start, value, children }) => {
  const frame = useCurrentFrame();
  const shown = rise(frame, start - 3, 14);
  return (
    <div style={{ display: "flex", alignItems: "baseline", gap: 18, marginTop: 26, opacity: shown, translate: `0px ${interpolate(shown, [0, 1], [12, 0])}px` }}>
      <span style={{ fontFamily: font.display, fontSize: 64, lineHeight: 1, minWidth: 150, textAlign: "right", fontVariantNumeric: "lining-nums tabular-nums" }}>{value}</span>
      <span style={{ fontSize: 30, whiteSpace: "nowrap" }}>{children}</span>
    </div>
  );
};

const Panel: React.FC<{ start: number; left: number; width: number; children: React.ReactNode }> = ({ start, left, width, children }) => {
  const frame = useCurrentFrame();
  const shown = pop(frame, start - 3, true);
  return (
    <div
      style={{
        position: "absolute",
        left,
        top: 740,
        width,
        height: 140,
        display: "flex",
        alignItems: "center",
        gap: 30,
        padding: "0 40px",
        borderRadius: 22,
        backgroundColor: "rgba(38, 38, 36, 0.88)",
        border: `1px solid ${color.line}`,
        opacity: Math.min(1, shown * 1.5),
        translate: `0px ${interpolate(shown, [0, 1], [30, 0])}px`,
      }}
    >
      {children}
    </div>
  );
};

export const S14Evidence: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const beats = evidenceBeats(scene);
  const repairs = pop(frame, beats.repairs - 3, true);
  return (
    <SceneShell>
      <Heading style={{ position: "absolute", left: 160, top: 70, fontSize: 60, opacity: rise(frame, 0, 18) }}>How it was tested</Heading>

      <div style={{ position: "absolute", left: 160, top: 175, width: 880 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 22, opacity: rise(frame, beats.files - 8, 8) }}>
          <div style={{ fontFamily: font.display, fontSize: 150, lineHeight: 1, color: color.action, fontVariantNumeric: "lining-nums tabular-nums" }}>
            {Math.round(FILES * counted(frame, beats.files)).toLocaleString("en-US")}
          </div>
          <div style={{ fontSize: 36 }}>audio files</div>
        </div>
        <Row start={beats.speeches} value="9">public-domain speeches</Row>
        <Row start={beats.edited} value="448">
          edited copies of known
          {EDIT_FACTS.map((fact) => {
            const shown = pop(frame, cueFrame(scene, 0, fact), true);
            return (
              <span
                key={fact}
                style={{
                  display: "inline-block",
                  marginLeft: 10,
                  padding: "2px 13px",
                  borderRadius: 999,
                  border: `1px solid ${color.flag}`,
                  backgroundColor: "rgba(178, 73, 129, 0.18)",
                  color: color.flagText,
                  fontSize: 23,
                  fontWeight: 700,
                  opacity: shown,
                  scale: String(interpolate(shown, [0, 1], [0.7, 1])),
                }}
              >
                {fact}
              </span>
            );
          })}
        </Row>
        <Row start={beats.readers} value="1,953">readings by other people</Row>
      </div>

      <div style={{ position: "absolute", left: 1060, top: 190, display: "flex", flexDirection: "column", gap: 44 }}>
        <Score value={F1_PLANNED} start={beats.scores} tint={color.action} title="F1, pre-registered" detail="on unseen speakers" />
        <div style={{ display: "flex", alignItems: "center", gap: 30, opacity: Math.min(1, repairs * 1.5), scale: String(interpolate(repairs, [0, 1], [0.85, 1])) }}>
          <div style={{ width: 210, textAlign: "center", fontFamily: font.display, fontSize: 76, lineHeight: 1, color: color.refText }}>22/22</div>
          <div>
            <div style={{ fontFamily: font.display, fontSize: 44, lineHeight: 1.1 }}>repairs</div>
            <div style={{ fontSize: 28, color: color.ink2, marginTop: 8, maxWidth: 480 }}>undoing the edit removes the flag; a placebo keeps it</div>
          </div>
        </div>
      </div>

      <Panel start={beats.clean} left={160} width={760}>
        <span style={{ fontFamily: font.display, fontSize: 100, lineHeight: 1, color: color.refText }}>0</span>
        <span style={{ fontSize: 34, lineHeight: 1.2 }}>false flags on unedited copies</span>
      </Panel>
      <Panel start={beats.reader} left={960} width={800}>
        <span style={{ fontFamily: font.display, fontSize: 64, lineHeight: 1, color: color.flagText, whiteSpace: "nowrap" }}>≈ 1 / 2 min</span>
        <span style={{ fontSize: 29, lineHeight: 1.25 }}>false flag with a different reader (0.46 per minute)</span>
      </Panel>
    </SceneShell>
  );
};
