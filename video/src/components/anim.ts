import { Easing, interpolate, spring } from "remotion";
import { FPS } from "../timeline";

const ease = Easing.bezier(0.16, 1, 0.3, 1);

// 0 before `start`, 1 after `start + length`, eased in between.
export const rise = (frame: number, start: number, length = 18): number =>
  interpolate(frame, [start, start + length], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });

export const fadeOut = (frame: number, end: number, length = 12): number =>
  interpolate(frame, [end - length, end], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.quad) });

// A spring from 0 to 1 that starts at `start`; the default settles without overshoot, `bouncy` overshoots a little.
export const pop = (frame: number, start: number, bouncy = false): number =>
  spring({ frame: frame - start, fps: FPS, config: bouncy ? { damping: 14, stiffness: 120, mass: 0.8 } : { damping: 200 } });

// Small deterministic pseudo-random sequence, so every render draws the same shapes.
export const seeded = (seed: number) => {
  let state = seed % 2147483647;
  if (state <= 0) {
    state += 2147483646;
  }
  return () => {
    state = (state * 16807) % 2147483647;
    return (state - 1) / 2147483646;
  };
};
