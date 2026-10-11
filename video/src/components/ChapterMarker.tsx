import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { color, font } from "../theme";
import { pop, rise } from "./anim";

// The feature that the demo shows now, over the top left of the browser window. It wipes in at the start of its scene.
export const ChapterMarker: React.FC<{ index: number; title: string; left: number; top: number; start?: number }> = ({ index, title, left, top, start = 6 }) => {
  const frame = useCurrentFrame();
  const badge = pop(frame, start, true);
  const wipe = rise(frame, start + 4, 22);
  const rule = rise(frame, start + 10, 26);
  return (
    <div style={{ position: "absolute", left, top, display: "flex", alignItems: "center", gap: 20 }}>
      <div
        style={{
          width: 54,
          height: 54,
          borderRadius: 14,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: color.actionWash,
          border: `1.5px solid ${color.action}`,
          color: color.action,
          fontFamily: font.mono,
          fontWeight: 500,
          fontSize: 22,
          opacity: Math.min(1, badge * 1.4),
          scale: String(interpolate(badge, [0, 1], [0.6, 1])),
        }}
      >
        {String(index).padStart(2, "0")}
      </div>
      <div style={{ position: "relative", paddingBottom: 8 }}>
        <div
          style={{
            fontFamily: font.display,
            fontWeight: 450,
            fontSize: 46,
            lineHeight: 1.05,
            letterSpacing: "-0.01em",
            color: color.ink,
            whiteSpace: "nowrap",
            clipPath: `inset(-10% ${100 - 100 * wipe}% -20% 0)`,
            translate: `${interpolate(wipe, [0, 1], [-18, 0])}px 0px`,
          }}
        >
          {title}
        </div>
        <div style={{ position: "absolute", left: 0, bottom: 0, height: 2, width: `${100 * rule}%`, borderRadius: 1, background: `linear-gradient(90deg, ${color.action}, rgba(217, 119, 87, 0))` }} />
      </div>
    </div>
  );
};
