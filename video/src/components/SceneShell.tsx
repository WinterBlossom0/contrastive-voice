import React from "react";
import { AbsoluteFill } from "remotion";
import { color, font } from "../theme";

// Every scene sits under a faint version of the dashboard's dusk sky: night at the top, a low ember glow, then the ground.
export const SceneShell: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ backgroundColor: color.base, color: color.ink, fontFamily: font.text }}>
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${color.night} 0%, ${color.dusk}66 18%, ${color.base} 46%)` }} />
    <AbsoluteFill style={{ background: "radial-gradient(40% 26% at 78% 30%, rgba(168, 116, 104, 0.16), transparent 70%)" }} />
    {children}
  </AbsoluteFill>
);

export const Heading: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => (
  <div
    style={{
      fontFamily: font.display,
      fontWeight: 400,
      fontSize: 64,
      lineHeight: 1.1,
      letterSpacing: "-0.015em",
      color: color.ink,
      ...style,
    }}
  >
    {children}
  </div>
);
