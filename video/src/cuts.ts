import { linearTiming, springTiming, type TransitionPresentation, type TransitionPresentationComponentProps, type TransitionTiming } from "@remotion/transitions";
import React from "react";
import { AbsoluteFill } from "remotion";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { FPS, type SceneId } from "./timeline";

// moves: true for a slide or a wipe, which gets a fuller whoosh than a fade.
export type Cut = { presentation: TransitionPresentation<Record<string, unknown>>; timing: TransitionTiming; moves: boolean };

// A dip through the backdrop: the old scene is gone before the new one shows, so two layers of text never mix.
const Dip: React.FC<TransitionPresentationComponentProps<Record<string, unknown>>> = ({ children, presentationProgress, presentationDirection }) => {
  const opacity = presentationDirection === "exiting" ? Math.max(0, 1 - 2 * presentationProgress) : Math.max(0, 2 * presentationProgress - 1);
  return React.createElement(AbsoluteFill, { style: { opacity } }, children);
};
const dipCut = (frames: number): Cut => ({ presentation: { component: Dip, props: {} }, timing: linearTiming({ durationInFrames: frames }), moves: false });
const slideCut = (direction: "from-left" | "from-right" | "from-top" | "from-bottom", frames: number): Cut => ({
  presentation: slide({ direction }) as TransitionPresentation<Record<string, unknown>>,
  timing: springTiming({ config: { damping: 200 }, durationInFrames: frames }),
  moves: true,
});
const wipeCut = (frames: number): Cut => ({
  presentation: wipe({ direction: "from-left" }) as TransitionPresentation<Record<string, unknown>>,
  timing: springTiming({ config: { damping: 200 }, durationInFrames: frames }),
  moves: true,
});

// The cut after each scene. Inside the demo the window stays where it is, so a short fade changes only its content; a new
// part of the story slides in over the still backdrop.
export const CUT_AFTER: Partial<Record<SceneId, Cut>> = {
  s1_hook: dipCut(18),
  s2_what: dipCut(15),
  s3_open_example: dipCut(12),
  s4_listen: dipCut(12),
  s5_finding: dipCut(12),
  s6_hear_fixed: dipCut(12),
  s7_melody: dipCut(12),
  s8_fix_all: dipCut(12),
  s9_text_lists: dipCut(12),
  s10_fair: dipCut(14),
  s11_upload: dipCut(12),
  s12_no_reference: slideCut("from-right", 18),
  s13_how: wipeCut(16),
  s14_evidence: slideCut("from-bottom", 18),
  s15_open: dipCut(18),
};

export const cutFrames = (id: SceneId): number => {
  const cut = CUT_AFTER[id];
  return cut === undefined ? 0 : cut.timing.getDurationInFrames({ fps: FPS });
};
