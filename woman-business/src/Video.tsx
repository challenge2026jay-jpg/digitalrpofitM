import React from "react";
import { AbsoluteFill, Audio, Easing, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { OVERLAP, SceneAccroche, SceneCTA, SceneCommandes, SceneIA, SceneObstacles, SceneSamantha, SceneTrafic, SceneWhatsApp } from "./scenes";
import { LEAD, SCENES, SceneName, TOTAL_FRAMES, VOICE_END, at, f } from "./timing";
import { Backdrop, C, WindowShadow, sans } from "./ui";

const SCENE_COMPONENTS: Record<SceneName, React.FC<{ start: number; dur: number }>> = {
  accroche: SceneAccroche,
  obstacles: SceneObstacles,
  samantha: SceneSamantha,
  whatsapp: SceneWhatsApp,
  ia: SceneIA,
  commandes: SceneCommandes,
  trafic: SceneTrafic,
  cta: SceneCTA,
};

// Balayage en bandes cacao (transition reprise de la référence) avant les deux moments forts.
const STRIPES_AT = [SCENES.samantha[0], SCENES.cta[0]];
const STRIPE_COLORS = ["#3A1D12", "#5A2C1B", C.cacao, "#7E3F25", C.rust];

const Stripes: React.FC = () => {
  const frame = useCurrentFrame();
  const { width } = useVideoConfig();
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {STRIPE_COLORS.map((col, i) => {
        const d = i * 2;
        // Entrée de gauche à droite, couverture brève, sortie vers la droite.
        const inP = interpolate(frame, [d, d + 9], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
        const outP = interpolate(frame, [14 + d, 23 + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
        const w = width / STRIPE_COLORS.length;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              top: 0,
              bottom: 0,
              left: i * w,
              width: w + 2,
              background: col,
              transform: `scaleX(${inP * (1 - outP)})`,
              transformOrigin: outP > 0 ? "right" : "left",
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

// Petite signature en haut à gauche, masquée sur l'écran final.
const Signature: React.FC = () => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [10, 30, f(SCENES.cta[0]) - 10, f(SCENES.cta[0])], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", top: 120, left: 92, opacity: o * 0.8, fontFamily: sans, fontWeight: 600, fontSize: 24, letterSpacing: 7, color: C.ink }}>
      WOMAN BUSINESS
    </div>
  );
};

// Effets sonores discrets, chacun calé sur un mot de la narration.
const SFX: { file: string; t: number; vol: number }[] = [
  ...(["obstacles", "whatsapp", "ia", "commandes", "trafic"] as SceneName[]).map((s) => ({ file: "whoosh", t: SCENES[s][0] - 0.05, vol: 0.14 })),
  ...STRIPES_AT.map((t) => ({ file: "whoosh", t: t - 0.15, vol: 0.22 })),
  { file: "thud", t: at("RDC"), vol: 0.22 },
  ...["fournisseur", "paiements", "transport", "frais"].map((w) => ({ file: "pop", t: at(w), vol: 0.16 })),
  { file: "click", t: at("Samantha"), vol: 0.16 },
  ...["dropshipping", "l'intelligence"].map((w) => ({ file: "pop", t: at(w), vol: 0.15 })),
  { file: "pop", t: at("commerce", "faciliter"), vol: 0.15 },
  ...["apprends", "présenter", "transformer"].map((w) => ({ file: "click", t: at(w), vol: 0.14 })),
  { file: "ding", t: at("achats"), vol: 0.16 },
  ...["rechercher", "créer"].map((w) => ({ file: "pop", t: at(w), vol: 0.15 })),
  { file: "pop", t: at("outils", "découvrir"), vol: 0.15 },
  { file: "pop", t: at("développer", "vidéo"), vol: 0.15 },
  ...["TikTok", "YouTube", "Instagram"].map((w) => ({ file: "pop", t: at(w), vol: 0.15 })),
  { file: "click", t: at("cliquant"), vol: 0.18 },
  { file: "ding", t: at("lien"), vol: 0.2 },
];

export const WomanBusiness: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: C.ivory }}>
      <Backdrop />
      {(Object.keys(SCENES) as SceneName[]).map((name) => {
        const [s, e] = SCENES[name];
        const Comp = SCENE_COMPONENTS[name];
        const from = f(s);
        return (
          <Sequence key={name} from={from} durationInFrames={Math.max(1, f(e) - from) + (name === "cta" ? 0 : OVERLAP)} layout="none">
            <Comp start={s} dur={e - s} />
          </Sequence>
        );
      })}
      <WindowShadow opacity={0.42} />
      <Signature />
      {STRIPES_AT.map((t, i) => (
        <Sequence key={i} from={f(t) - 12} durationInFrames={36} layout="none">
          <Stripes />
        </Sequence>
      ))}

      <Sequence from={f(LEAD)} layout="none">
        <Audio src={staticFile("audio/voix_off_finale.wav")} volume={1} />
      </Sequence>
      <Audio
        src={staticFile("audio/musique.mp3")}
        volume={(fr) => {
          const t = fr / fps;
          const fadeIn = interpolate(t, [0, 0.8], [0.4, 1], { extrapolateRight: "clamp" });
          // Discrète sous la voix (≈ -21 dB), remonte légèrement après la dernière phrase, puis fondu.
          const bed = interpolate(t, [VOICE_END - 0.1, VOICE_END + 0.6], [0.09, 0.16], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const fadeOut = interpolate(fr, [TOTAL_FRAMES - 30, TOTAL_FRAMES], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return fadeIn * bed * fadeOut;
        }}
      />
      {SFX.map((s, i) => (
        <Sequence key={i} from={Math.max(0, f(s.t))} durationInFrames={20} layout="none">
          <Audio src={staticFile(`sfx/${s.file}.wav`)} volume={s.vol} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
