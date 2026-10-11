import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from "remotion";

// The dashboard hero, shot layer by layer from the running app (public/plates, 3840 x 2160, back to front).
// depth: how much a layer grows during the push-in; lift: px it rises from during the intro, like the site's own intro.
const LAYERS = [
  { file: "plates/sky.png", depth: 0.03, lift: 0 },
  { file: "plates/glow.png", depth: 0.05, lift: 10 },
  { file: "plates/range-far.png", depth: 0.07, lift: 40 },
  { file: "plates/range-mid.png", depth: 0.11, lift: 70 },
  { file: "plates/range-near.png", depth: 0.15, lift: 100 },
  { file: "plates/cloud-sea.png", depth: 0.2, lift: 130 },
] as const;

const SEA = 5;
const GLOW = 1;

type Props = {
  // 0 to 1: how far the camera has pushed in.
  push: number;
  // 0 to 1: how far the ranges have risen into place.
  rise: number;
  // Extra brightness of the low sun, 0 to 1.
  glow?: number;
};

export const Landscape: React.FC<Props> = ({ push, rise, glow = 0 }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: "#1f1e1d", overflow: "hidden" }}>
      {LAYERS.map((layer, index) => (
        <AbsoluteFill
          key={layer.file}
          style={{
            transformOrigin: "50% 78%",
            scale: String(1 + layer.depth * push),
            translate: `${index === SEA ? 14 * Math.sin(frame / 70) : 0}px ${(1 - rise) * layer.lift}px`,
            opacity: index === GLOW ? interpolate(rise, [0, 1], [0, 0.8]) + 0.2 * glow : 1,
          }}
        >
          <Img src={staticFile(layer.file)} style={{ width: "100%", height: "100%" }} />
        </AbsoluteFill>
      ))}
      {/* Darker towards the top and the edges, so the type over the sky keeps its contrast. */}
      <AbsoluteFill style={{ background: "radial-gradient(120% 90% at 50% 70%, transparent 45%, rgba(14, 13, 20, 0.55) 100%)" }} />
    </AbsoluteFill>
  );
};
