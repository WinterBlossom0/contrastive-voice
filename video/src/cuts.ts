import { linearTiming, springTiming, type TransitionPresentation, type TransitionTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { FPS, type SceneId } from "./timeline";

// moves: true for a slide or a wipe, which gets a fuller whoosh than a fade.
export type Cut = { presentation: TransitionPresentation<Record<string, unknown>>; timing: TransitionTiming; moves: boolean };

const fadeCut = (frames: number): Cut => ({ presentation: fade() as TransitionPresentation<Record<string, unknown>>, timing: linearTiming({ durationInFrames: frames }), moves: false });
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
  s1_hook: fadeCut(18),
  s2_what: fadeCut(15),
  s3_open_example: fadeCut(12),
  s4_listen: fadeCut(12),
  s5_finding: fadeCut(12),
  s6_hear_fixed: fadeCut(12),
  s7_melody: fadeCut(12),
  s8_fix_all: fadeCut(12),
  s9_text_lists: fadeCut(12),
  s10_fair: slideCut("from-right", 18),
  s11_upload: fadeCut(12),
  s12_no_reference: slideCut("from-right", 18),
  s13_how: wipeCut(16),
  s14_evidence: slideCut("from-bottom", 18),
  s15_open: fadeCut(18),
};

export const cutFrames = (id: SceneId): number => {
  const cut = CUT_AFTER[id];
  return cut === undefined ? 0 : cut.timing.getDurationInFrames({ fps: FPS });
};
