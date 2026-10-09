import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { rise } from "../components/anim";
import { Heading, SceneShell } from "../components/SceneShell";
import { color, font } from "../theme";
import { beatFrame, type SceneTiming } from "../timeline";

// The two commands of the README section "Run with Docker", joined into the one command that the narration names.
const COMMAND = "docker build -t cvoice . && docker run --rm -p 7860:7860 cvoice";
const CHARS_PER_FRAME = 1.1;

const LINKS = [
  { place: "Model", address: "huggingface.co/WinterBlossom/contrastive-voice" },
  { place: "Code", address: "github.com/WinterBlossom0/contrastive-voice" },
];

export const S9Open: React.FC<{ scene: SceneTiming }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const typingStart = 14;
  const openPage = beatFrame(scene, 1);
  const links = beatFrame(scene, 2);
  const typed = Math.min(COMMAND.length, Math.max(0, Math.floor((frame - typingStart) * CHARS_PER_FRAME)));
  return (
    <SceneShell>
      <Heading style={{ position: "absolute", left: 260, top: 110, fontSize: 72, opacity: rise(frame, 0, 18) }}>Open, and runs on your machine</Heading>
      <div
        style={{
          position: "absolute",
          left: 260,
          top: 250,
          width: 1400,
          borderRadius: 18,
          overflow: "hidden",
          backgroundColor: color.surface,
          border: `1px solid ${color.border}`,
          boxShadow: "0 30px 80px rgba(0, 0, 0, 0.5)",
          opacity: rise(frame, 4, 18),
        }}
      >
        <div style={{ height: 40, display: "flex", alignItems: "center", gap: 9, paddingLeft: 18, backgroundColor: color.panel2 }}>
          {[0, 1, 2].map((dot) => (
            <div key={dot} style={{ width: 12, height: 12, borderRadius: 6, backgroundColor: color.panel3 }} />
          ))}
        </div>
        <div style={{ padding: "30px 36px", fontFamily: "ui-monospace, 'DejaVu Sans Mono', monospace", fontSize: 34, lineHeight: 1.9 }}>
          <div style={{ whiteSpace: "nowrap" }}>
            <span style={{ color: color.accentText }}>$ </span>
            {COMMAND.slice(0, typed)}
            {typed < COMMAND.length && Math.floor(frame / 8) % 2 === 0 ? <span style={{ color: color.accentText }}>▍</span> : null}
          </div>
          <div style={{ color: color.ink2, opacity: rise(frame, openPage, 16) }}>Then open localhost:7860 in your browser</div>
        </div>
      </div>
      <div style={{ position: "absolute", left: 260, top: 640, display: "flex", flexDirection: "column", gap: 26 }}>
        {LINKS.map((link, index) => {
          const shown = rise(frame, links + index * 10, 20);
          return (
            <div key={link.place} style={{ display: "flex", alignItems: "baseline", gap: 30, opacity: shown, translate: `${interpolate(shown, [0, 1], [-16, 0])}px 0px` }}>
              <div style={{ width: 130, fontSize: 32, color: color.ink2 }}>{link.place}</div>
              <div style={{ fontFamily: font.display, fontWeight: 600, fontSize: 48 }}>{link.address}</div>
            </div>
          );
        })}
      </div>
    </SceneShell>
  );
};
