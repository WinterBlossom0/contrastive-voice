import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Same tokens as the dashboard (src/cvoice/static/style.css), so the video and the product look like one thing.
export const color = {
  base: "#121212",
  surface: "#1a1a1d",
  panel: "#1f1f23",
  panel2: "#26262b",
  panel3: "#2d2d33",
  border: "rgba(255, 255, 255, 0.08)",
  line: "rgba(255, 255, 255, 0.1)",
  ink: "#e6e6e6",
  ink2: "#a3a3ab",
  muted: "#77777f",
  accent: "#8784e2",
  accentText: "#adaaf0",
  accentWash: "rgba(135, 132, 226, 0.12)",
  flag: "#d26c8b",
  flagText: "#e39ab0",
  flagWash: "rgba(210, 108, 139, 0.14)",
  reference: "#8a8a93",
} as const;

export const font = {
  display: "Sora, 'Atkinson Hyperlegible Next', sans-serif",
  text: "'Atkinson Hyperlegible Next', sans-serif",
} as const;

export const fontsReady = Promise.all([
  loadFont({ family: "Sora", url: staticFile("fonts/Sora-SemiBold.woff2"), weight: "600" }),
  loadFont({ family: "Sora", url: staticFile("fonts/Sora-Bold.woff2"), weight: "700" }),
  loadFont({ family: "Atkinson Hyperlegible Next", url: staticFile("fonts/AtkinsonHyperlegibleNext-Regular.woff2"), weight: "400" }),
  loadFont({ family: "Atkinson Hyperlegible Next", url: staticFile("fonts/AtkinsonHyperlegibleNext-Bold.woff2"), weight: "700" }),
]);

// Key content stays above this line; the subtitle band sits below it.
export const SUBTITLE_TOP = 930;
