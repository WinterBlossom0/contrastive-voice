import { Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Freeze, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { color, font } from "../theme";
import { CAPTURE_VIEW, cameraFromRect, FPS, type CameraRect, type TimedCallout, type TimedCameraKey, type TimedCapture, type TimedClick } from "../timeline";
import { pop, rise } from "./anim";

// The area that holds the browser window; the window ends above the subtitle band (theme.ts SUBTITLE_TOP 930).
export const FRAME = { left: 80, top: 116, width: 1760, height: 800, chrome: 36 } as const;
// A new capture fades in over the previous one, which stays visible underneath for these frames.
export const CAPTURE_FADE_FRAMES = 10;
const CLICK_LEAD = 12;
const CLICK_TAIL = 22;
const CALLOUT_IN = 10;
const CALLOUT_OUT = 8;
const PILL_HEIGHT = 50;
const PILL_GAP = 22;

type View = { width: number; height: number };

const mix = (from: CameraRect, to: CameraRect, progress: number): CameraRect =>
  from.map((edge, index) => edge + (to[index] - edge) * progress) as CameraRect;

// Each key starts a move from wherever the camera is at that frame, so a key that comes early never makes the camera jump.
const rectAt = (keys: TimedCameraKey[], frame: number): CameraRect => {
  let rect = keys[0].rect;
  for (const key of keys.slice(1)) {
    if (frame < key.frame) {
      break;
    }
    const progress = spring({ frame: frame - key.frame, fps: FPS, config: { damping: 200 }, durationInFrames: key.moveFrames });
    rect = mix(rect, key.rect, progress);
  }
  return rect;
};

const captureRect = (capture: TimedCapture, sceneFrame: number): CameraRect =>
  capture.cameraKeys.length > 0 ? rectAt(capture.cameraKeys, sceneFrame) : [0, 0, capture.size[0], capture.size[1]];

// Capture px to page-area px of the window: the capture's rect at this frame fills the view.
const projector = (capture: TimedCapture, sceneFrame: number, view: View) => {
  const [left, top, right, bottom] = captureRect(capture, sceneFrame);
  const zoom = Math.min(view.width / (right - left), view.height / (bottom - top));
  const centreX = (left + right) / 2;
  const centreY = (top + bottom) / 2;
  return {
    zoom,
    centreX,
    centreY,
    x: (px: number) => view.width / 2 + (px - centreX) * zoom,
    y: (px: number) => view.height / 2 + (px - centreY) * zoom,
  };
};

const activeIndex = (captures: TimedCapture[], frame: number): number => {
  const started = captures.filter((capture) => capture.from <= frame).length;
  return Math.max(0, started - 1);
};

// The page area of the window: the active capture's rect shape; it morphs to the next shape while the next capture fades in.
const viewAt = (captures: TimedCapture[], frame: number): View => {
  if (captures.length === 0) {
    return { width: CAPTURE_VIEW.width, height: CAPTURE_VIEW.height };
  }
  const index = activeIndex(captures, frame);
  const current = cameraFromRect(captureRect(captures[index], frame));
  if (index === 0) {
    return { width: current.viewWidth, height: current.viewHeight };
  }
  const previous = cameraFromRect(captureRect(captures[index - 1], frame));
  const progress = rise(frame, captures[index].from, CAPTURE_FADE_FRAMES + 6);
  return {
    width: interpolate(progress, [0, 1], [previous.viewWidth, current.viewWidth]),
    height: interpolate(progress, [0, 1], [previous.viewHeight, current.viewHeight]),
  };
};

const windowBox = (view: View) => ({
  left: FRAME.left + (FRAME.width - view.width) / 2,
  top: FRAME.top + (FRAME.height - FRAME.chrome - view.height) / 2,
});

const Placeholder: React.FC<{ title: string; detail: string }> = ({ title, detail }) => (
  <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 16, padding: 80, background: `linear-gradient(160deg, ${color.panel} 0%, ${color.base} 100%)` }}>
    <div style={{ width: 64, height: 64, borderRadius: 32, border: `2px dashed ${color.line}` }} />
    <div style={{ fontFamily: font.display, fontWeight: 450, fontSize: 40, color: color.ink2 }}>{title}</div>
    <div style={{ fontSize: 26, color: color.muted, textAlign: "center", maxWidth: 1200 }}>{detail}</div>
  </AbsoluteFill>
);

const Still: React.FC<{ file: string }> = ({ file }) => <Img src={staticFile(file)} style={{ display: "block", width: "100%", height: "auto" }} />;

// A screen recording plays once and then holds on its still (or on its last frame), so the pointer never jumps back to the start.
const CaptureMedia: React.FC<{ capture: TimedCapture }> = ({ capture }) => {
  const { fps } = useVideoConfig();
  const isVideo = capture.file.endsWith(".webm") || capture.file.endsWith(".mp4");
  if (!capture.fileExists) {
    return capture.still === null ? <Placeholder title={`Capture pending: ${capture.id}`} detail={capture.description} /> : <Still file={capture.still} />;
  }
  if (!isVideo) {
    return <Still file={capture.file} />;
  }
  const lead = capture.leadFrames;
  const rate = capture.playbackRate ?? 1;
  const playFrames = Math.max(1, Math.round((capture.durationSec * fps) / rate));
  const video = <Video src={staticFile(capture.file)} muted playbackRate={rate} style={{ display: "block", width: "100%", height: "auto" }} />;
  return (
    <>
      {lead > 0 && capture.firstStill !== undefined ? (
        <Sequence name={`First frame ${capture.id}`} durationInFrames={lead}>
          <Still file={capture.firstStill} />
        </Sequence>
      ) : null}
      <Sequence name={`Recording ${capture.id}`} from={lead} durationInFrames={playFrames} premountFor={fps}>
        {video}
      </Sequence>
      <Sequence name={`Hold ${capture.id}`} from={lead + playFrames} premountFor={fps}>
        {capture.still === null ? <Freeze frame={playFrames - 1}>{video}</Freeze> : <Still file={capture.still} />}
      </Sequence>
    </>
  );
};

const CameraView: React.FC<{ capture: TimedCapture; fadeIn: boolean; view: View }> = ({ capture, fadeIn, view }) => {
  const frame = useCurrentFrame();
  const camera = projector(capture, capture.from + frame, view);
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        width: capture.size[0],
        height: capture.size[1],
        transformOrigin: "0 0",
        transform: `translate(${view.width / 2 - camera.centreX * camera.zoom}px, ${view.height / 2 - camera.centreY * camera.zoom}px) scale(${camera.zoom})`,
        opacity: fadeIn ? rise(frame, 0, CAPTURE_FADE_FRAMES) : 1,
      }}
    >
      <CaptureMedia capture={capture} />
    </div>
  );
};

// A soft ring closes in on the spot just before the click, then a ripple spreads from it. Sizes are in output px, at any zoom.
const ClickMark: React.FC<{ click: TimedClick; x: number; y: number; frame: number }> = ({ click, x, y, frame }) => {
  const since = frame - click.frame;
  const approach = rise(frame, click.frame - CLICK_LEAD, CLICK_LEAD);
  const ripple = interpolate(since, [0, 18], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const hold = interpolate(since, [6, CLICK_TAIL], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ring = interpolate(approach, [0, 1], [46, 24]) * (since >= 0 ? interpolate(since, [0, 4, 9], [1, 0.82, 1], { extrapolateRight: "clamp" }) : 1);
  return (
    <>
      <div
        style={{
          position: "absolute",
          left: x - ring,
          top: y - ring,
          width: ring * 2,
          height: ring * 2,
          borderRadius: "50%",
          border: `3px solid rgba(246, 220, 196, ${0.9 * approach * hold})`,
          backgroundColor: `rgba(217, 119, 87, ${0.22 * approach * hold})`,
          boxShadow: `0 0 24px rgba(217, 119, 87, ${0.45 * approach * hold})`,
        }}
      />
      {since >= 0 ? (
        <div
          style={{
            position: "absolute",
            left: x - (24 + 56 * ripple),
            top: y - (24 + 56 * ripple),
            width: 2 * (24 + 56 * ripple),
            height: 2 * (24 + 56 * ripple),
            borderRadius: "50%",
            border: `2px solid rgba(217, 119, 87, ${0.85 * (1 - ripple)})`,
          }}
        />
      ) : null}
    </>
  );
};

type ProjectedCallout = { callout: TimedCallout; box: { left: number; top: number; width: number; height: number }; shown: number };

const projectCallouts = (capture: TimedCapture, frame: number, view: View): ProjectedCallout[] => {
  const camera = projector(capture, frame, view);
  return capture.timedCallouts
    .filter((callout) => frame >= callout.from && frame < callout.from + callout.durationInFrames + CALLOUT_OUT)
    .map((callout) => {
      const [left, top, right, bottom] = callout.rect;
      const pad = 8;
      const box = { left: camera.x(left) - pad, top: camera.y(top) - pad, width: (right - left) * camera.zoom + 2 * pad, height: (bottom - top) * camera.zoom + 2 * pad };
      const shown = rise(frame, callout.from, CALLOUT_IN) * interpolate(frame, [callout.from + callout.durationInFrames, callout.from + callout.durationInFrames + CALLOUT_OUT], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
      return { callout, box, shown };
    });
};

// The rect of a callout, outlined in clay, with the rest of the page dimmed a little.
const CalloutBox: React.FC<{ item: ProjectedCallout }> = ({ item }) => (
  <div
    style={{
      position: "absolute",
      left: item.box.left,
      top: item.box.top,
      width: item.box.width,
      height: item.box.height,
      borderRadius: 12,
      border: `2.5px solid rgba(217, 119, 87, ${item.shown})`,
      boxShadow: `0 0 0 4000px rgba(12, 11, 16, ${0.32 * item.shown}), 0 0 28px rgba(217, 119, 87, ${0.35 * item.shown})`,
      scale: String(interpolate(item.shown, [0, 1], [1.04, 1])),
    }}
  />
);

// The label of a callout, above its rect when there is room in the window, else below it; kept inside the frame.
const CalloutPill: React.FC<{ item: ProjectedCallout; origin: { left: number; top: number }; view: View; frame: number }> = ({ item, origin, view, frame }) => {
  const { box, callout } = item;
  const spring = pop(frame, callout.from, true);
  const roomAbove = box.top - PILL_HEIGHT - PILL_GAP > 0;
  const roomBelow = box.top + box.height + PILL_HEIGHT + PILL_GAP < view.height;
  const placement = roomAbove || !roomBelow ? "above" : "below";
  const anchorX = origin.left + box.left + box.width / 2;
  const edgeY = origin.top + (placement === "above" ? Math.max(box.top, 0) : Math.min(box.top + box.height, view.height));
  const pillTop = placement === "above" ? Math.max(FRAME.top - 40, edgeY - PILL_GAP - PILL_HEIGHT) : edgeY + PILL_GAP;
  const estimatedWidth = 60 + callout.text.length * 14.5;
  const pillLeft = Math.min(Math.max(anchorX - estimatedWidth / 2, 40), 1880 - estimatedWidth);
  const lineTop = placement === "above" ? pillTop + PILL_HEIGHT : edgeY;
  const lineBottom = placement === "above" ? edgeY : pillTop;
  return (
    <>
      <div style={{ position: "absolute", left: anchorX - 1, top: lineTop, width: 2, height: Math.max(0, lineBottom - lineTop) * Math.min(1, spring), backgroundColor: color.action, opacity: item.shown }} />
      <div
        style={{
          position: "absolute",
          left: pillLeft,
          top: pillTop,
          height: PILL_HEIGHT,
          display: "flex",
          alignItems: "center",
          gap: 12,
          padding: "0 22px",
          borderRadius: PILL_HEIGHT / 2,
          backgroundColor: "rgba(38, 38, 36, 0.96)",
          border: `1.5px solid ${color.action}`,
          boxShadow: "0 12px 30px rgba(0, 0, 0, 0.45)",
          color: color.ink,
          fontFamily: font.text,
          fontWeight: 700,
          fontSize: 25,
          whiteSpace: "nowrap",
          opacity: item.shown,
          scale: String(interpolate(spring, [0, 1], [0.85, 1])),
          translate: `0px ${interpolate(spring, [0, 1], [placement === "above" ? 10 : -10, 0])}px`,
        }}
      >
        <div style={{ width: 10, height: 10, borderRadius: 5, backgroundColor: color.action }} />
        {callout.text}
      </div>
    </>
  );
};

type Props = {
  captures: TimedCapture[];
  // The window springs up with a 3D tilt once, when the demo starts.
  enter: boolean;
  pendingTitle: string;
  pendingDetail: string;
};

export const CaptureFrame: React.FC<Props> = ({ captures, enter, pendingTitle, pendingDetail }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const view = viewAt(captures, frame);
  const origin = windowBox(view);
  const page = { left: origin.left, top: origin.top + FRAME.chrome };
  const entry = enter ? spring({ frame, fps, config: { damping: 20, stiffness: 90, mass: 1 } }) : 1;
  // Overlays of a capture show while it is on screen, also during the fade into the next capture.
  const visible = captures.filter((capture, index) => frame >= capture.from && (index === captures.length - 1 || frame < capture.from + capture.durationInFrames + CAPTURE_FADE_FRAMES));
  const callouts = visible.flatMap((capture) => projectCallouts(capture, frame, view));
  const clicks = visible.flatMap((capture) => {
    const camera = projector(capture, frame, view);
    return capture.clickFrames
      .filter((click) => frame >= click.frame - CLICK_LEAD && frame <= click.frame + CLICK_TAIL)
      .map((click) => ({ click, x: camera.x(click.x), y: camera.y(click.y) }));
  });
  return (
    <AbsoluteFill
      style={{
        transformOrigin: "50% 90%",
        transform: `perspective(2400px) translateY(${interpolate(entry, [0, 1], [120, 0])}px) rotateX(${interpolate(entry, [0, 1], [24, 0])}deg) scale(${interpolate(entry, [0, 1], [0.88, 1])})`,
        opacity: Math.min(1, entry * 2),
      }}
    >
      <div
        style={{
          position: "absolute",
          left: origin.left,
          top: origin.top,
          width: view.width,
          height: view.height + FRAME.chrome,
          borderRadius: 18,
          overflow: "hidden",
          backgroundColor: color.surface,
          border: `1px solid rgba(237, 230, 218, 0.14)`,
          boxShadow: "0 40px 100px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(0, 0, 0, 0.3)",
        }}
      >
        <div style={{ height: FRAME.chrome, display: "flex", alignItems: "center", gap: 9, paddingLeft: 18, backgroundColor: color.panel2 }}>
          {[0, 1, 2].map((dot) => (
            <div key={dot} style={{ width: 12, height: 12, borderRadius: 6, backgroundColor: color.panel3 }} />
          ))}
          <div style={{ marginLeft: 22, padding: "2px 16px", borderRadius: 8, backgroundColor: color.base, color: color.ink2, fontSize: 18 }}>localhost:7860</div>
        </div>
        <div style={{ position: "relative", width: view.width, height: view.height, overflow: "hidden", backgroundColor: color.base }}>
          {captures.length === 0 ? <Placeholder title={pendingTitle} detail={pendingDetail} /> : null}
          {captures.map((capture, index) => (
            <Sequence
              key={capture.id}
              name={`Capture ${capture.id}`}
              from={capture.from}
              durationInFrames={index < captures.length - 1 ? capture.durationInFrames + CAPTURE_FADE_FRAMES : undefined}
              premountFor={fps}
            >
              <CameraView capture={capture} fadeIn={index > 0} view={view} />
            </Sequence>
          ))}
          {callouts.map((item, index) => (
            <CalloutBox key={`box-${index}`} item={item} />
          ))}
          {clicks.map(({ click, x, y }, index) => (
            <ClickMark key={`click-${index}`} click={click} x={x} y={y} frame={frame} />
          ))}
        </div>
      </div>
      {callouts.map((item, index) => (
        <CalloutPill key={`pill-${index}`} item={item} origin={page} view={view} frame={frame} />
      ))}
    </AbsoluteFill>
  );
};
