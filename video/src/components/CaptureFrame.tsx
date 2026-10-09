import { Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Img, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { color, font } from "../theme";
import type { TimedCapture } from "../timeline";
import { fadeOut, rise } from "./anim";

export const FRAME = { left: 320, top: 150, width: 1280, chrome: 40 } as const;
const INNER_HEIGHT = Math.round((FRAME.width * 9) / 16);
// The dashboard page is a centred column at x 280 to 1639 of the 1920 px capture; the frame shows that column only, so its text stays legible.
const CROP = { left: 264, width: 1392 };
const CROP_SCALE = FRAME.width / CROP.width;

const Placeholder: React.FC<{ capture: TimedCapture }> = ({ capture }) => (
  <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", backgroundColor: color.panel, gap: 18, padding: 80 }}>
    <div style={{ fontFamily: font.display, fontWeight: 600, fontSize: 40, color: color.ink2 }}>Capture pending: {capture.id}</div>
    <div style={{ fontSize: 30, color: color.muted, textAlign: "center" }}>{capture.description}</div>
    <div style={{ fontSize: 24, color: color.muted }}>public/{capture.file}</div>
  </AbsoluteFill>
);

const Still: React.FC<{ file: string }> = ({ file }) => (
  <Img src={staticFile(file)} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "top" }} />
);

// A screen recording plays once and then holds on its still, so the pointer never jumps back to the start.
const CaptureMedia: React.FC<{ capture: TimedCapture }> = ({ capture }) => {
  const { fps } = useVideoConfig();
  const isVideo = capture.file.endsWith(".webm") || capture.file.endsWith(".mp4");
  if (!capture.fileExists) {
    return capture.still === null ? <Placeholder capture={capture} /> : <Still file={capture.still} />;
  }
  if (!isVideo) {
    return <Still file={capture.file} />;
  }
  const lead = capture.leadFrames;
  const rate = capture.playbackRate ?? 1;
  const playFrames = Math.min(capture.durationInFrames - lead, Math.round((capture.durationSec * fps) / rate));
  return (
    <>
      {lead > 0 && capture.firstStill !== undefined ? (
        <Sequence name={`First frame ${capture.id}`} durationInFrames={lead}>
          <Still file={capture.firstStill} />
        </Sequence>
      ) : null}
      <Sequence name={`Recording ${capture.id}`} from={lead} durationInFrames={playFrames} premountFor={fps}>
        <Video src={staticFile(capture.file)} muted playbackRate={rate} objectFit="cover" style={{ width: "100%", height: "100%" }} />
      </Sequence>
      {capture.still !== null && lead + playFrames < capture.durationInFrames ? (
        <Sequence name={`Still ${capture.id}`} from={lead + playFrames} premountFor={fps}>
          <Still file={capture.still} />
        </Sequence>
      ) : null}
    </>
  );
};

const CroppedCapture: React.FC<{ capture: TimedCapture }> = ({ capture }) => (
  <div
    style={{
      position: "absolute",
      left: -CROP.left * CROP_SCALE,
      top: -(capture.top ?? 0) * CROP_SCALE,
      width: 1920 * CROP_SCALE,
      height: 1080 * CROP_SCALE,
    }}
  >
    <CaptureMedia capture={capture} />
  </div>
);

export const CaptureFrame: React.FC<{ captures: TimedCapture[]; sceneDuration: number }> = ({ captures, sceneDuration }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div
      style={{
        position: "absolute",
        left: FRAME.left,
        top: FRAME.top,
        width: FRAME.width,
        height: INNER_HEIGHT + FRAME.chrome,
        borderRadius: 18,
        overflow: "hidden",
        backgroundColor: color.surface,
        border: `1px solid ${color.border}`,
        boxShadow: "0 30px 80px rgba(0, 0, 0, 0.55)",
        opacity: rise(frame, 0, 20) * fadeOut(frame, sceneDuration, 10),
        translate: `0px ${interpolate(rise(frame, 0, 24), [0, 1], [26, 0])}px`,
      }}
    >
      <div style={{ height: FRAME.chrome, display: "flex", alignItems: "center", gap: 9, paddingLeft: 18, backgroundColor: color.panel2 }}>
        {[0, 1, 2].map((dot) => (
          <div key={dot} style={{ width: 12, height: 12, borderRadius: 6, backgroundColor: color.panel3 }} />
        ))}
        <div
          style={{
            marginLeft: 22,
            padding: "3px 16px",
            borderRadius: 8,
            backgroundColor: color.base,
            color: color.ink2,
            fontSize: 22,
          }}
        >
          localhost:7860
        </div>
      </div>
      <div style={{ position: "relative", width: FRAME.width, height: INNER_HEIGHT, overflow: "hidden", backgroundColor: color.base }}>
        {captures.map((capture) => (
          <Sequence
            key={capture.id}
            name={`Capture ${capture.id}`}
            from={capture.from}
            durationInFrames={capture.durationInFrames}
            premountFor={fps}
          >
            <CroppedCapture capture={capture} />
          </Sequence>
        ))}
      </div>
    </div>
  );
};
