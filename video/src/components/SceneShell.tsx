import React from "react";
import { AbsoluteFill } from "remotion";
import { color, font } from "../theme";

// Every scene shares the dashboard's base colour and its one faint accent glow in the top-left corner.
export const SceneShell: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ backgroundColor: color.base, color: color.ink, fontFamily: font.text }}>
    <AbsoluteFill style={{ background: "radial-gradient(34% 34% at 12% 16%, rgba(135, 132, 226, 0.08), transparent 70%)" }} />
    {children}
  </AbsoluteFill>
);

export const Heading: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => (
  <div
    style={{
      fontFamily: font.display,
      fontWeight: 600,
      fontSize: 64,
      lineHeight: 1.15,
      letterSpacing: "-0.01em",
      wordSpacing: "0.14em",
      color: color.ink,
      ...style,
    }}
  >
    {children}
  </div>
);
