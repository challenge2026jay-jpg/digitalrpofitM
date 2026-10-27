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

// Effets sonores extraits de la vidéo de référence (public/sfx_ref, voir README),
// chacun calé sur une transition ou une animation, elle-même calée sur un mot de la narration.
const WHOOSHES = ["whoosh_a", "whoosh_b", "whoosh_c"];
const POPS = ["pop_1", "pop_2", "pop_3"];
const pop = (t: number, i: number, vol = 0.32) => ({ file: POPS[i % POPS.length], t, vol });

const SFX: { file: string; t: number; vol: number }[] = [
  // Transitions entre scènes : souffle de la référence, juste avant le fondu.
  ...(["obstacles", "whatsapp", "ia", "commandes", "trafic"] as SceneName[]).map((s, i) => ({ file: WHOOSHES[i % WHOOSHES.length], t: SCENES[s][0] - 0.12, vol: 0.4 })),
  // Balayages en bandes cacao : longue transition de la référence.
  ...STRIPES_AT.map((t) => ({ file: "transition_longue", t: t - 0.45, vol: 0.38 })),
  // Accroche : « RDC » arrive en gros plan.
  { file: "impact", t: at("RDC") - 0.03, vol: 0.4 },
  { file: "whoosh_b", t: at("commerce") - 0.15, vol: 0.3 },
  { file: "blip", t: at("l'étranger"), vol: 0.22 },
  // Cartes des obstacles.
  ...["fournisseur", "paiements", "transport", "frais"].map((w, i) => pop(at(w), i)),
  { file: "impact", t: at("obstacles"), vol: 0.3 },
  // Présentation de Samantha.
  { file: "riser", t: at("Samantha") - 0.1, vol: 0.22 },
  { file: "blip", t: at("Woman"), vol: 0.22 },
  { file: "tictac", t: at("Depuis"), vol: 0.22 },
  ...["dropshipping", "l'intelligence"].map((w, i) => pop(at(w), i)),
  pop(at("commerce", "faciliter"), 2),
  // WhatsApp, étape par étape.
  { file: "blip", t: at("WhatsApp"), vol: 0.22 },
  { file: "riser", t: at("Au lieu") - 0.2, vol: 0.2 },
  ...["apprends", "présenter", "transformer"].map((w, i) => ({ file: WHOOSHES[(i + 1) % 3], t: at(w) - 0.1, vol: 0.26 })),
  pop(at("achats"), 0, 0.34),
  { file: "impact", t: at("outil"), vol: 0.26 },
  // Usages de l'IA : une carte par usage.
  { file: "blip", t: at("démonstrations"), vol: 0.2 },
  pop(at("outils", "découvrir"), 0),
  pop(at("rechercher"), 1),
  pop(at("créer"), 2),
  pop(at("développer", "vidéo"), 0),
  // Étapes d'une commande internationale.
  ...[0, 1, 2, 3].map((i) => pop(at("étapes") + (i * 8) / 30, i + 1, 0.26)),
  // Trafic et plateformes.
  { file: "riser", t: at("trafic") - 0.15, vol: 0.22 },
  { file: "blip", t: at("monétisation"), vol: 0.2 },
  ...["TikTok", "YouTube", "Instagram"].map((w, i) => pop(at(w), i)),
  // Appel à l'action.
  { file: "impact", t: at("l'IA", "Tu veux apprendre"), vol: 0.3 },
  { file: "blip", t: at("gratuitement"), vol: 0.22 },
  { file: "riser", t: at("Woman", "Rejoins") - 0.1, vol: 0.22 },
  pop(at("cliquant"), 1, 0.36),
  { file: "blip", t: at("lien"), vol: 0.24 },
  ...["outils", "démonstrations", "opportunités"].map((w, i) => pop(at(w, "ci-dessous"), i, 0.24)),
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
        <Sequence key={i} from={Math.max(0, f(s.t))} durationInFrames={50} layout="none">
          <Audio src={staticFile(`sfx_ref/${s.file}.wav`)} volume={s.vol} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
