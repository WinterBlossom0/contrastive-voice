import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Same tokens as the dashboard (src/cvoice/static/style.css), so the video and the product look like one thing.
// One job per hue: clay is a primary action, lavender this recording, lake the reference, bramble a flag.
export const color = {
  base: "#1f1e1d",
  surface: "#262624",
  panel: "#2a2927",
  panel2: "#302f2c",
  panel3: "#3a3835",
  border: "rgba(237, 230, 218, 0.09)",
  line: "rgba(237, 230, 218, 0.12)",
  ink: "#ede6da",
  ink2: "#b3aca1",
  muted: "#968f85",
  action: "#d97757",
  actionWash: "rgba(217, 119, 87, 0.14)",
  onAction: "#1f1e1d",
  you: "#957fd0",
  youText: "#bcaef0",
  youWash: "rgba(149, 127, 208, 0.13)",
  ref: "#219ba1",
  refText: "#6cc4c8",
  flag: "#b24981",
  flagText: "#ee98bf",
  flagWash: "rgba(178, 73, 129, 0.16)",
  // The dusk sky of the dashboard hero, from the top of the frame down to the ground.
  night: "#1c1d2b",
  dusk: "#2b2a43",
  ember: "#a87468",
} as const;

export const font = {
  display: "Newsreader, Georgia, serif",
  text: "'Atkinson Hyperlegible Next', sans-serif",
} as const;

export const fontsReady = Promise.all([
  // A variable font: one file serves every weight from 200 to 800.
  loadFont({ family: "Newsreader", url: staticFile("fonts/Newsreader-latin.woff2"), weight: "200 800" }),
  loadFont({ family: "Atkinson Hyperlegible Next", url: staticFile("fonts/AtkinsonHyperlegibleNext-Regular.woff2"), weight: "400" }),
  loadFont({ family: "Atkinson Hyperlegible Next", url: staticFile("fonts/AtkinsonHyperlegibleNext-Bold.woff2"), weight: "700" }),
]);

// Key content stays above this line; the subtitle band sits below it.
export const SUBTITLE_TOP = 930;
