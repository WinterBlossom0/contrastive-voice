import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { color, font } from "../theme";

// The dashboard hero landscape, blurred and dimmed (public/plates/backdrop.jpg, made from the plates). It sits under
// every scene and stays still during transitions, so a slide moves only the content. It drifts slowly over the whole video.
export const Backdrop: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const progress = frame / Math.max(1, durationInFrames);
  return (
    <AbsoluteFill style={{ backgroundColor: color.base, overflow: "hidden" }}>
      <Img
        src={staticFile("plates/backdrop.jpg")}
        style={{ width: "100%", height: "100%", scale: String(1.06 + 0.04 * progress), translate: `${-30 + 60 * progress}px 0px` }}
      />
    </AbsoluteFill>
  );
};

// A scene layer: transparent, so the backdrop shows through.
export const SceneShell: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ color: color.ink, fontFamily: font.text }}>{children}</AbsoluteFill>
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
