import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { rise } from "../components/anim";
import { lineTokens } from "../components/cues";
import { Landscape } from "../components/Landscape";
import { MUSIC } from "../components/MusicBed";
import { KineticLine, LogoMark } from "../components/Type";
import { color, font } from "../theme";
import { beatFrame, type SceneTiming } from "../timeline";

const TITLE = "Contrastive Voice";
// The last words of the tagline, in the action colour.
const ACCENT_FROM = "Fix";
const END_FADE = 30;

export const S16Close: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const tagline = scene.lines.length > 0 ? lineTokens(scene.lines[0]) : [];
  const accentAt = tagline.findIndex((token) => token.text === ACCENT_FROM);
  const nameStart = beatFrame(scene, 1);
  const push = interpolate(frame, [0, scene.durationInFrames], [0.55, 1], { easing: Easing.bezier(0.33, 0, 0.2, 1), extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ color: color.ink, fontFamily: font.text }}>
      <Landscape push={push} rise={1} glow={rise(frame, nameStart, 40)} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 170, display: "flex", flexDirection: "column", alignItems: "center", gap: 46 }}>
        <KineticLine
          words={tagline.map((token, index) => ({ text: token.text, at: token.from, tint: accentAt >= 0 && index >= accentAt ? color.action : undefined }))}
          style={{ fontFamily: font.display, fontSize: 88, letterSpacing: "-0.015em", justifyContent: "center" }}
        />
        <div style={{ display: "flex", alignItems: "center", gap: 30, opacity: rise(frame, nameStart - 4, 16), translate: `0px ${interpolate(rise(frame, nameStart - 4, 24), [0, 1], [20, 0])}px` }}>
          <LogoMark size={110} draw={rise(frame, nameStart - 4, 36)} drawReading={rise(frame, nameStart + 4, 36)} />
          <div style={{ fontFamily: font.display, fontSize: 96, letterSpacing: "-0.02em", lineHeight: 1 }}>{TITLE}</div>
        </div>
      </div>
      {MUSIC.credit === null ? null : (
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 34, display: "flex", justifyContent: "center", opacity: rise(frame, nameStart + 10, 20) }}>
          <div style={{ padding: "6px 18px", borderRadius: 999, backgroundColor: "rgba(20, 19, 24, 0.78)", color: color.ink, fontFamily: font.text, fontSize: 22 }}>{MUSIC.credit}</div>
        </div>
      )}
      <AbsoluteFill style={{ backgroundColor: "#000", opacity: interpolate(frame, [scene.durationInFrames - END_FADE, scene.durationInFrames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }} />
    </AbsoluteFill>
  );
};
