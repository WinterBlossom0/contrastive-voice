import { Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { color, font } from "../theme";
import { CAPTURE_VIEW, cameraFromRect, type CameraRect, type TimedCameraKey, type TimedCapture } from "../timeline";
import { fadeOut, rise } from "./anim";

// The area that holds the browser window; the window ends above the subtitle band (theme.ts SUBTITLE_TOP 930).
export const FRAME = { left: 80, top: 116, width: 1760, height: 800, chrome: 36 } as const;
// A new capture fades in over the previous one, which stays visible underneath for these frames.
export const CAPTURE_FADE_FRAMES = 10;
const cameraEase = Easing.bezier(0.45, 0, 0.55, 1);
const CAPTURE_VIEW_FULL = { viewWidth: CAPTURE_VIEW.width, viewHeight: CAPTURE_VIEW.height };

const mix = (from: CameraRect, to: CameraRect, progress: number): CameraRect =>
  from.map((edge, index) => edge + (to[index] - edge) * progress) as CameraRect;

// Each key starts a move from wherever the camera is at that frame, so a key that comes early never makes the camera jump.
const rectAt = (keys: TimedCameraKey[], frame: number): CameraRect => {
  let rect = keys[0].rect;
  for (const key of keys.slice(1)) {
    if (frame < key.frame) {
      break;
    }
    const progress = interpolate(frame, [key.frame, key.frame + key.moveFrames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: cameraEase });
    rect = mix(rect, key.rect, progress);
  }
  return rect;
};

const captureRect = (capture: TimedCapture, sceneFrame: number): CameraRect =>
  capture.cameraKeys.length > 0 ? rectAt(capture.cameraKeys, sceneFrame) : [0, 0, capture.size[0], capture.size[1]];

const Placeholder: React.FC<{ capture: TimedCapture }> = ({ capture }) => (
  <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", backgroundColor: color.panel, gap: 18, padding: 80 }}>
    <div style={{ fontFamily: font.display, fontWeight: 500, fontSize: 40, color: color.ink2 }}>Capture pending: {capture.id}</div>
    <div style={{ fontSize: 30, color: color.muted, textAlign: "center" }}>{capture.description}</div>
    <div style={{ fontSize: 24, color: color.muted }}>public/{capture.file}</div>
  </AbsoluteFill>
);

const Still: React.FC<{ file: string }> = ({ file }) => <Img src={staticFile(file)} style={{ display: "block", width: "100%", height: "auto" }} />;

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
        <Video src={staticFile(capture.file)} muted playbackRate={rate} style={{ display: "block", width: "100%", height: "auto" }} />
      </Sequence>
      {capture.still !== null && lead + playFrames < capture.durationInFrames ? (
        <Sequence name={`Still ${capture.id}`} from={lead + playFrames} premountFor={fps}>
          <Still file={capture.still} />
        </Sequence>
      ) : null}
    </>
  );
};

// The capture's rect fills the window; a capture that fades out keeps its own rect inside the window of the next one.
const CameraView: React.FC<{ capture: TimedCapture; fadeIn: boolean; view: { width: number; height: number } }> = ({ capture, fadeIn, view }) => {
  const frame = useCurrentFrame();
  const [left, top, right, bottom] = captureRect(capture, capture.from + frame);
  const zoom = Math.min(view.width / (right - left), view.height / (bottom - top));
  const x = (left + right) / 2;
  const y = (top + bottom) / 2;
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        width: capture.size[0],
        height: capture.size[1],
        transformOrigin: "0 0",
        transform: `translate(${view.width / 2 - x * zoom}px, ${view.height / 2 - y * zoom}px) scale(${zoom})`,
        opacity: fadeIn ? rise(frame, 0, CAPTURE_FADE_FRAMES) : 1,
      }}
    >
      <CaptureMedia capture={capture} />
    </div>
  );
};

export const CaptureFrame: React.FC<{ captures: TimedCapture[]; sceneDuration: number }> = ({ captures, sceneDuration }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  // The window takes the shape of the rect of the capture on screen.
  const active = captures.filter((capture) => capture.from <= frame).pop() ?? captures[0];
  const { viewWidth, viewHeight } = active === undefined ? CAPTURE_VIEW_FULL : cameraFromRect(captureRect(active, frame));
  const view = { width: viewWidth, height: viewHeight };
  return (
    <div
      style={{
        position: "absolute",
        left: FRAME.left + (FRAME.width - viewWidth) / 2,
        top: FRAME.top + (FRAME.height - FRAME.chrome - viewHeight) / 2,
        width: viewWidth,
        height: viewHeight + FRAME.chrome,
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
        <div style={{ marginLeft: 22, padding: "2px 16px", borderRadius: 8, backgroundColor: color.base, color: color.ink2, fontSize: 20 }}>localhost:7860</div>
      </div>
      <div style={{ position: "relative", width: viewWidth, height: viewHeight, overflow: "hidden", backgroundColor: color.base }}>
        {captures.map((capture, index) => (
          <Sequence
            key={capture.id}
            name={`Capture ${capture.id}`}
            from={capture.from}
            durationInFrames={index < captures.length - 1 ? capture.durationInFrames + CAPTURE_FADE_FRAMES : capture.durationInFrames}
            premountFor={fps}
          >
            <CameraView capture={capture} fadeIn={index > 0} view={view} />
          </Sequence>
        ))}
      </div>
    </div>
  );
};
