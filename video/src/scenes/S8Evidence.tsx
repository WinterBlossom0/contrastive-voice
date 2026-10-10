import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { fadeOut, rise } from "../components/anim";
import { Heading, SceneShell } from "../components/SceneShell";
import { color, font } from "../theme";
import { beatFrame, type SceneTiming } from "../timeline";

// Every number below is copied from docs/NUMBERS.md and docs/technical.md at the committed revision.
const DATASET = [
  { value: "2,410", label: "audio files" },
  { value: "1,109", label: "minutes" },
  { value: "9", label: "public-domain speeches, split 5 / 2 / 2 by speaker" },
];
// R1 test rows of the stress matrix: share of detections kept, technical.md section 6.4.
const STRESS = [
  { condition: "Gain +6 dB", kept: 1.0 },
  { condition: "Gain −6 dB", kept: 1.0 },
  { condition: "MP3 64 kbit/s", kept: 1.0 },
  { condition: "Low-pass 3.4 kHz", kept: 0.94 },
  { condition: "WORLD speaker transform", kept: 0.99 },
  { condition: "Room reverb", kept: 0.99 },
  { condition: "White noise 20 dB", kept: 0.91 },
  { condition: "Phone band", kept: 0.87 },
  { condition: "Compression", kept: 0.76 },
  { condition: "Babble 20 dB", kept: 0.85 },
  { condition: "Babble 10 dB", kept: 0.6 },
];

// The share of the scores line spoken before "point eight seven nine" (narration s8_evidence_02).
const COUNT_ONCE_SHARE = 0.57;

const CountUp: React.FC<{ value: number; start: number; decimals: number; size: number; tint: string }> = ({ value, start, decimals, size, tint }) => {
  const frame = useCurrentFrame();
  const shown = value * rise(frame, start, 36);
  return <span style={{ fontFamily: font.display, fontWeight: 500, fontSize: size, color: tint, fontVariantNumeric: "lining-nums tabular-nums" }}>{shown.toFixed(decimals)}</span>;
};

export const S8Evidence: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  // The second F1 is spoken in the second half of the scores line.
  const scores = beatFrame(scene, 1);
  const countOnce = scores + Math.round(scene.lines[1].durationInFrames * COUNT_ONCE_SHARE);
  const clean = beatFrame(scene, 2);
  const stress = beatFrame(scene, 3);
  const firstPhase = fadeOut(frame, stress + 6, 14);
  const secondPhase = rise(frame, stress + 4, 20);
  return (
    <SceneShell>
      <div style={{ position: "absolute", left: 160, top: 90, width: 1600, opacity: firstPhase }}>
        <Heading style={{ fontSize: 64, opacity: rise(frame, 0, 18) }}>Measured on speakers it never saw</Heading>
        <div style={{ display: "flex", gap: 70, marginTop: 44 }}>
          {DATASET.map((item, index) => (
            <div key={item.label} style={{ opacity: rise(frame, 8 + index * 8, 18) }}>
              <div style={{ fontFamily: font.display, fontWeight: 500, fontSize: 56 }}>{item.value}</div>
              <div style={{ fontSize: 30, color: color.ink2 }}>{item.label}</div>
            </div>
          ))}
        </div>
        <div style={{ display: "flex", alignItems: "flex-end", gap: 90, marginTop: 70, opacity: rise(frame, scores, 18) }}>
          <div>
            <CountUp value={0.812} start={scores} decimals={3} size={150} tint={color.action} />
            <div style={{ fontSize: 32, color: color.ink }}>Test F1, pre-registered</div>
            <div style={{ fontSize: 28, color: color.ink2 }}>every prediction counted</div>
          </div>
          <div style={{ paddingBottom: 4, opacity: rise(frame, countOnce, 18) }}>
            <CountUp value={0.879} start={countOnce} decimals={3} size={96} tint={color.ink} />
            <div style={{ fontSize: 32, color: color.ink }}>Test F1, one detection per change</div>
            <div style={{ fontSize: 28, color: color.ink2 }}>same-change duplicates counted once</div>
          </div>
        </div>
        <div
          style={{
            display: "flex",
            alignItems: "baseline",
            gap: 26,
            marginTop: 56,
            padding: "22px 32px",
            borderRadius: 16,
            backgroundColor: color.surface,
            border: `1px solid ${color.border}`,
            width: "fit-content",
            opacity: rise(frame, clean, 18),
          }}
        >
          <CountUp value={0} start={clean} decimals={0} size={72} tint={color.action} />
          <span style={{ fontSize: 36 }}>false flags in 5.89 minutes of unedited and placebo test copies</span>
        </div>
      </div>

      <div style={{ position: "absolute", left: 160, top: 90, width: 1600, opacity: secondPhase }}>
        <Heading style={{ fontSize: 64 }}>Stress test: detections kept</Heading>
        <div style={{ fontSize: 30, color: color.ink2, marginTop: 10 }}>Test speakers, eleven channel conditions applied to the reading</div>
        <div style={{ marginTop: 40, display: "flex", flexDirection: "column", gap: 13 }}>
          {STRESS.map((row, index) => {
            const grow = rise(frame, stress + 10 + index * 4, 24);
            return (
              <div key={row.condition} style={{ display: "flex", alignItems: "center", gap: 24 }}>
                <div style={{ width: 430, fontSize: 28, color: color.ink2, textAlign: "right" }}>{row.condition}</div>
                <div style={{ width: 900, height: 34, borderRadius: 8, backgroundColor: color.panel }}>
                  <div style={{ width: `${row.kept * 100 * grow}%`, height: "100%", borderRadius: 8, backgroundColor: color.you, opacity: interpolate(row.kept, [0.6, 1], [0.6, 1]) }} />
                </div>
                <div style={{ width: 90, fontSize: 28, fontVariantNumeric: "tabular-nums", opacity: grow }}>{row.kept.toFixed(2)}</div>
              </div>
            );
          })}
        </div>
      </div>
    </SceneShell>
  );
};
