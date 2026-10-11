import React from "react";
import { Easing, interpolate, useCurrentFrame } from "remotion";
import { pop, rise } from "../components/anim";
import { cueFrame } from "../components/cues";
import { Heading, SceneShell } from "../components/SceneShell";
import { color, font } from "../theme";
import { beatFrame, type SceneTiming } from "../timeline";

// Every number below is from docs/technical.md: 2,410 files; test F1 0.812 pre-registered and 0.879 with one detection
// per change; 0 false regions in 5.89 comparison-minutes of unedited test copies.
const FILES = 2410;
const F1_PLANNED = 0.812;
const F1_ONCE = 0.879;
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
  scores: beatFrame(scene, 1),
  once: cueFrame(scene, 1, "0.879"),
  clean: beatFrame(scene, 2) + 4,
});

export const S14Evidence: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { files: filesStart, speeches, scores, once, clean } = evidenceBeats(scene);
  const zero = pop(frame, clean, true);
  return (
    <SceneShell>
      <Heading style={{ position: "absolute", left: 160, top: 80, fontSize: 60, opacity: rise(frame, 0, 18) }}>How it was tested</Heading>

      <div style={{ position: "absolute", left: 160, top: 200, width: 760 }}>
        <div style={{ opacity: rise(frame, filesStart - 4, 10) }}>
          <div style={{ fontFamily: font.display, fontSize: 168, lineHeight: 1, color: color.action, fontVariantNumeric: "lining-nums tabular-nums" }}>
            {Math.round(FILES * counted(frame, filesStart)).toLocaleString("en-US")}
          </div>
          <div style={{ fontSize: 34, color: color.ink, marginTop: 10 }}>audio files</div>
        </div>
        <div style={{ display: "flex", alignItems: "baseline", gap: 18, marginTop: 44, opacity: rise(frame, speeches, 14), translate: `0px ${interpolate(rise(frame, speeches, 14), [0, 1], [12, 0])}px` }}>
          <span style={{ fontFamily: font.display, fontSize: 72, lineHeight: 1 }}>9</span>
          <span style={{ fontSize: 34 }}>public-domain speeches</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 14, marginTop: 22 }}>
          <span style={{ fontSize: 30, color: color.ink2, opacity: rise(frame, cueFrame(scene, 0, "edits"), 12) }}>edits of known</span>
          {EDIT_FACTS.map((fact) => {
            const shown = pop(frame, cueFrame(scene, 0, fact), true);
            return (
              <span
                key={fact}
                style={{
                  padding: "5px 18px",
                  borderRadius: 999,
                  border: `1px solid ${color.flag}`,
                  backgroundColor: "rgba(178, 73, 129, 0.18)",
                  color: color.flagText,
                  fontSize: 28,
                  fontWeight: 700,
                  opacity: shown,
                  scale: String(interpolate(shown, [0, 1], [0.7, 1])),
                }}
              >
                {fact}
              </span>
            );
          })}
        </div>
      </div>

      <div style={{ position: "absolute", left: 1000, top: 200, display: "flex", flexDirection: "column", gap: 40 }}>
        <Score value={F1_PLANNED} start={scores} tint={color.action} title="F1, pre-registered" detail="on speakers it never saw" />
        <Score value={F1_ONCE} start={once} tint={color.you} title="F1, one detection per edit" detail="duplicates of one edit counted once" />
      </div>

      <div
        style={{
          position: "absolute",
          left: 160,
          top: 730,
          width: 1600,
          height: 140,
          display: "flex",
          alignItems: "center",
          gap: 36,
          padding: "0 44px",
          borderRadius: 22,
          backgroundColor: "rgba(38, 38, 36, 0.88)",
          border: `1px solid ${color.line}`,
          opacity: Math.min(1, zero * 1.5),
          translate: `0px ${interpolate(zero, [0, 1], [30, 0])}px`,
        }}
      >
        <span style={{ fontFamily: font.display, fontSize: 110, lineHeight: 1, color: color.refText }}>0</span>
        <span style={{ fontSize: 40, lineHeight: 1.2 }}>
          false flags in <span style={{ fontFamily: font.display, fontSize: 48 }}>5.89</span> minutes of unedited and placebo copies
        </span>
      </div>
    </SceneShell>
  );
};
