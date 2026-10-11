import React from "react";
import { AbsoluteFill } from "remotion";
import { CaptureFrame, FRAME } from "../components/CaptureFrame";
import { ChapterMarker } from "../components/ChapterMarker";
import { Backdrop, SceneShell } from "../components/SceneShell";
import { Subtitles } from "../components/Subtitles";
import type { SceneTiming, TimedCapture } from "../timeline";

// A visual check of the captures.json overlay contract (camera keys, clicks, callouts in capture px) on a real page shot.
// Render a still at frame 40 (click ripple), 140 (callout on the score) and 260 (callout on a finding chip).
// The subtitle line has word times with the numbers spoken as words, as a TTS gives them; frames 60 and 120 show the karaoke.
const CHECK_CAPTURE: TimedCapture = {
  id: "check_page",
  file: "captures/s3_page.png",
  durationSec: 10,
  scene: "s3_open_example",
  description: "The L3A page, for the overlay check.",
  size: [2240, 3901],
  from: 0,
  durationInFrames: 300,
  fileExists: true,
  still: null,
  leadFrames: 0,
  cameraKeys: [
    { frame: 0, rect: [0, 0, 2240, 1408], moveFrames: 30 },
    { frame: 90, rect: [0, 700, 1100, 1400], moveFrames: 36 },
    { frame: 190, rect: [700, 700, 2232, 1408], moveFrames: 36 },
  ],
  clickFrames: [{ frame: 30, x: 1720, y: 75 }],
  soundFrames: [],
  timedCallouts: [
    { from: 110, durationInFrames: 70, rect: [70, 760, 640, 990], text: "Delivery score 86.11" },
    { from: 230, durationInFrames: 60, rect: [1412, 948, 1636, 986], text: "Biggest cost: Rushed, −4.89" },
  ],
};

const CHECK_SCENE: SceneTiming = {
  id: "s5_finding",
  durationInFrames: 300,
  clip: null,
  captures: [],
  lines: [
    {
      text: "These five words took 0.87 seconds. The reference takes 1.62.",
      file: "",
      durationSec: 5,
      from: 30,
      durationInFrames: 150,
      fileExists: false,
      words: [
        ["These", 0, 0.2],
        ["five", 0.2, 0.45],
        ["words", 0.45, 0.8],
        ["took", 0.8, 1.05],
        ["zero", 1.1, 1.3],
        ["point", 1.3, 1.5],
        ["eight", 1.5, 1.7],
        ["seven", 1.7, 1.95],
        ["seconds", 1.95, 2.5],
        ["The", 2.7, 2.8],
        ["reference", 2.8, 3.3],
        ["takes", 3.3, 3.6],
        ["one", 3.6, 3.8],
        ["point", 3.8, 4.0],
        ["six", 4.0, 4.2],
        ["two", 4.2, 4.5],
      ],
    },
  ],
};

export const CaptureFrameCheck: React.FC = () => (
  <AbsoluteFill>
    <Backdrop />
    <SceneShell>
      <ChapterMarker index={1} title="Try an example" left={FRAME.left} top={30} />
      <CaptureFrame captures={[CHECK_CAPTURE]} enter pendingTitle="" pendingDetail="" />
    </SceneShell>
    <Subtitles scene={CHECK_SCENE} />
  </AbsoluteFill>
);
