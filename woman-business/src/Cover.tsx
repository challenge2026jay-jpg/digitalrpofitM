import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Backdrop, Burst, C, WindowShadow, sans, serif } from "./ui";

// Couverture TikTok 1080 × 1920. Tout le contenu utile reste dans le cadre central 3:4
// (y 240 → 1680) que TikTok garde sur la grille du profil, et hors de la colonne d'icônes à droite.
const big = (size: number, color: string): React.CSSProperties => ({
  fontFamily: serif,
  fontStyle: "italic",
  fontWeight: 700,
  fontSize: size,
  lineHeight: 0.98,
  color,
  letterSpacing: -1,
  whiteSpace: "nowrap",
});

export const Cover: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: C.ivory }}>
    <Backdrop />

    <div style={{ position: "absolute", top: 268, left: 0, width: 1080, textAlign: "center", fontFamily: sans, fontWeight: 600, fontSize: 30, letterSpacing: 10, color: C.ink }}>
      WOMAN BUSINESS
    </div>
    <div style={{ position: "absolute", top: 330, left: 0, width: 1080, textAlign: "center" }}>
      <div style={big(114, C.ink)}>Vendre en ligne</div>
      <div style={{ fontFamily: serif, fontStyle: "italic", fontSize: 62, color: C.ink, margin: "14px 0 6px" }}>depuis la RDC,</div>
      <div style={big(146, C.cacao)}>grâce à l'IA</div>
    </div>

    <div style={{ position: "absolute", left: 620, top: 1130 }}>
      <Burst size={340} rotate={12} />
    </div>
    <div
      style={{
        position: "absolute",
        left: (1080 - 560) / 2,
        top: 760,
        width: 560,
        height: 660,
        borderRadius: 44,
        overflow: "hidden",
        boxShadow: "0 40px 80px rgba(60,35,20,0.25), 0 8px 18px rgba(60,35,20,0.1)",
      }}
    >
      <Img src={staticFile("img/samantha_presentation.jpg")} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 28%" }} />
    </div>

    <div style={{ position: "absolute", top: 1474, left: 0, width: 1080, display: "flex", justifyContent: "center" }}>
      <div style={{ background: C.cacao, color: C.ivory, borderRadius: 999, padding: "24px 48px", fontFamily: sans, fontWeight: 600, fontSize: 40, boxShadow: "0 20px 44px rgba(107,54,34,0.35)", whiteSpace: "nowrap" }}>
        Chaîne WhatsApp gratuite
      </div>
    </div>
    <div style={{ position: "absolute", top: 1590, left: 0, width: 1080, textAlign: "center", fontFamily: serif, fontStyle: "italic", fontSize: 44, color: C.ink }}>
      avec Samantha Mwange
    </div>

    <WindowShadow opacity={0.36} />
  </AbsoluteFill>
);
