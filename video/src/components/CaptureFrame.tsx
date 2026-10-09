import { Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { color, font } from "../theme";
import type { TimedCameraKey, TimedCapture } from "../timeline";
import { fadeOut, rise } from "./anim";

// The frame ends above the subtitle band (theme.ts SUBTITLE_TOP 930).
export const FRAME = { left: 80, top: 116, width: 1760, height: 800, chrome: 36 } as const;
const VIEW = { width: FRAME.width, height: FRAME.height - FRAME.chrome };
// A new capture fades in over the previous one, which stays visible underneath for these frames.
export const CAPTURE_FADE_FRAMES = 10;
// A held camera keeps a slow push-in, so a still shot does not look frozen; the unit is zoom gained per second.
const DRIFT_PER_SEC = 0.006;
const cameraEase = Easing.bezier(0.45, 0, 0.55, 1);

type Camera = { x: number; y: number; zoom: number };

const drifted = (camera: Camera, frames: number, fps: number): Camera => ({ ...camera, zoom: camera.zoom * (1 + (DRIFT_PER_SEC * Math.max(0, frames)) / fps) });

// Each key starts a move from wherever the camera is at that frame, so a key that comes early never makes the camera jump.
const cameraAt = (keys: TimedCameraKey[], frame: number, fps: number): Camera => {
  const first = keys[0];
  let camera: Camera = { x: first.x, y: first.y, zoom: first.zoom };
  let settledAt = first.frame;
  for (const key of keys.slice(1)) {
    if (frame < key.frame) {
      break;
    }
    const start = drifted(camera, key.frame - settledAt, fps);
    const progress = interpolate(frame, [key.frame, key.frame + key.moveFrames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: cameraEase });
    camera = {
      x: start.x + (key.x - start.x) * progress,
      y: start.y + (key.y - start.y) * progress,
      zoom: start.zoom + (key.zoom - start.zoom) * progress,
    };
    settledAt = key.frame + key.moveFrames;
    if (progress < 1) {
      return camera;
    }
  }
  return drifted(camera, frame - settledAt, fps);
};

// The view never leaves the media; a media edge smaller than the view is centred.
const clampCentre = (centre: number, mediaSize: number, viewSize: number): number => {
  const half = viewSize / 2;
  if (mediaSize <= viewSize) {
    return mediaSize / 2;
  }
  return Math.min(mediaSize - half, Math.max(half, centre));
};

const Placeholder: React.FC<{ capture: TimedCapture }> = ({ capture }) => (
  <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", backgroundColor: color.panel, gap: 18, padding: 80 }}>
    <div style={{ fontFamily: font.display, fontWeight: 600, fontSize: 40, color: color.ink2 }}>Capture pending: {capture.id}</div>
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

const CameraView: React.FC<{ capture: TimedCapture; fadeIn: boolean }> = ({ capture, fadeIn }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const [mediaWidth, mediaHeight] = capture.size;
  const keys = capture.cameraKeys.length > 0 ? capture.cameraKeys : [{ frame: 0, x: mediaWidth / 2, y: mediaHeight / 2, zoom: VIEW.width / mediaWidth, moveFrames: 0 }];
  const camera = cameraAt(keys, capture.from + frame, fps);
  const x = clampCentre(camera.x, mediaWidth, VIEW.width / camera.zoom);
  const y = clampCentre(camera.y, mediaHeight, VIEW.height / camera.zoom);
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        width: mediaWidth,
        height: mediaHeight,
        transformOrigin: "0 0",
        transform: `translate(${VIEW.width / 2 - x * camera.zoom}px, ${VIEW.height / 2 - y * camera.zoom}px) scale(${camera.zoom})`,
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
  return (
    <div
      style={{
        position: "absolute",
        left: FRAME.left,
        top: FRAME.top,
        width: FRAME.width,
        height: FRAME.height,
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
      <div style={{ position: "relative", width: VIEW.width, height: VIEW.height, overflow: "hidden", backgroundColor: color.base }}>
        {captures.map((capture, index) => (
          <Sequence
            key={capture.id}
            name={`Capture ${capture.id}`}
            from={capture.from}
            durationInFrames={index < captures.length - 1 ? capture.durationInFrames + CAPTURE_FADE_FRAMES : capture.durationInFrames}
            premountFor={fps}
          >
            <CameraView capture={capture} fadeIn={index > 0} />
          </Sequence>
        ))}
      </div>
    </div>
  );
};
