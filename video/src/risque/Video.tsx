// Composition « SansStockRisque » : le dropshipping sans stock n'est pas sans risque.
import React from "react";
import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Captions } from "../Captions";
import { LEAD, f, norm } from "../timing";
import { C } from "../ui";
import { Avatar, Chrome } from "../Video";
import { OV } from "../scenes12";
import { SCENE_COMPONENTS } from "./scenes";
import { REVEAL, SCENES, SceneName, TOTAL_FRAMES, VOICE_END, WORDS, at, endOf } from "./timing";

const KEYWORDS = new Set(["sans", "stock", "risque", "livraison", "refus", "rdc", "réel"].map(norm));

// Effets sonores courts (synthétisés, public/sfx), chacun sur une action visuelle.
const SFX: { file: string; t: number; vol: number }[] = [
  { file: "whoosh", t: 0.05, vol: 0.25 },
  { file: "impact", t: at("stock") + 0.33, vol: 0.35 },
  { file: "bassdrop", t: at("risque"), vol: 0.3 },
  // Le risque se déplace
  { file: "whoosh_rev", t: at("déplaces"), vol: 0.25 },
  ...[0, 1, 2, 3].map((i) => ({ file: "tick", t: at("déplaces") + 0.1 + i * 0.167, vol: 0.3 })),
  { file: "pop", t: at("déplaces") + 0.75, vol: 0.22 },
  // Parcours de commande
  ...["Facebook", "Instagram", "WhatsApp"].map((w) => ({ file: "click", t: at(w), vol: 0.28 })),
  { file: "notif", t: at("commande"), vol: 0.3 },
  { file: "whoosh", t: at("commande") + 0.15, vol: 0.18 },
  { file: "cash", t: at("paie"), vol: 0.25 },
  // Problèmes réels
  { file: "error", t: at("fournisseur", "problèmes"), vol: 0.25 },
  { file: "glitch", t: at("produit", "rupture"), vol: 0.22 },
  { file: "clock", t: at("délai"), vol: 0.25 },
  { file: "vibration", t: at("client", "délai"), vol: 0.3 },
  { file: "negative", t: at("refuser"), vol: 0.28 },
  // Retour vers toi
  { file: "notif", t: at("cas"), vol: 0.28 },
  { file: "vibration", t: at("cas") + 0.05, vol: 0.25 },
  { file: "notif", t: at("Il va revenir"), vol: 0.28 },
  { file: "impact", t: at("toi"), vol: 0.28 },
  // Calcul de marge
  { file: "cash", t: at("25"), vol: 0.28 },
  ...[at("9"), at("4"), at("4", "publicité"), at("1"), at("2")].map((t) => ({ file: "calc", t, vol: 0.35 })),
  ...[at("9"), at("4"), at("4", "publicité"), at("1"), at("2")].map((t) => ({ file: "tick", t: t + 0.12, vol: 0.22 })),
  { file: "impact", t: REVEAL, vol: 0.4 },
  // Critères
  ...[at("fournisseur", "Vérifie"), at("paiement"), at("livraison", "zone"), at("taux"), at("coût réel")].map((t) => ({ file: "tick", t, vol: 0.3 })),
  // Appel à l'action
  { file: "whoosh", t: at("Rejoins") - 0.1, vol: 0.2 },
  { file: "chime", t: endOf("bio") + 0.1, vol: 0.3 },
  // Changements de séquence
  ...(["deplace", "parcours", "problemes", "retour", "marge", "criteres", "cta"] as SceneName[]).map((s) => ({ file: "whoosh", t: SCENES[s][0], vol: 0.16 })),
];

const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const drift = (frame * 0.6) % 72;
  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, #D3EEFE 0%, ${C.sky} 45%, ${C.skyDeep} 100%)` }}>
      <AbsoluteFill style={{
        backgroundImage: "linear-gradient(rgba(255,255,255,0.45) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,0.45) 2px, transparent 2px)",
        backgroundSize: "72px 72px", backgroundPosition: `0 ${drift}px`, opacity: 0.55,
      }} />
    </AbsoluteFill>
  );
};

const MUSIC_FROM = 1.0; // la fin naturelle du morceau tombe ainsi sur le dernier plan

export const SansStockRisque: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: C.sky }}>
      <Background />
      {(Object.keys(SCENES) as SceneName[]).map((name) => {
        const [s, e] = SCENES[name];
        const Comp = SCENE_COMPONENTS[name];
        const from = f(s);
        return (
          <Sequence key={name} from={from} durationInFrames={f(e) - from + (name === "cta" ? 0 : OV)} layout="none">
            <Comp start={s} dur={e - s} />
          </Sequence>
        );
      })}
      <Captions words={WORDS} keywords={KEYWORDS} />
      <Chrome />
      {/* Le hook et l'appel à l'action montrent déjà la photo en grand. */}
      <Avatar showAt={SCENES.deplace[0] + 0.2} hideAt={SCENES.cta[0] + 0.2} />

      <Sequence from={f(LEAD)} layout="none">
        <Audio src={staticFile("audio/risque/voix_off_finale.wav")} volume={1} />
      </Sequence>
      <Audio
        src={staticFile("audio/risque/musique.mp3")}
        startFrom={f(MUSIC_FROM)}
        volume={(fr) => {
          const t = fr / fps;
          const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
          // Discrète au départ, environ 10 % sous la voix, un peu plus présente sur l'appel à l'action et après la voix.
          const fadeIn = interpolate(t, [0, 2.5], [0.35, 1], clamp);
          const level = interpolate(t, [SCENES.cta[0], SCENES.cta[0] + 1, VOICE_END, VOICE_END + 0.5], [0.1, 0.13, 0.13, 0.16], clamp);
          // Silence musical juste avant le résultat « 5 $ ».
          const gap = interpolate(t, [REVEAL - 0.4, REVEAL - 0.3, REVEAL, REVEAL + 0.15], [1, 0, 0, 1], clamp);
          const fadeOut = interpolate(fr, [TOTAL_FRAMES - 24, TOTAL_FRAMES], [1, 0], clamp);
          return fadeIn * level * gap * fadeOut;
        }}
      />
      {SFX.map((s, i) => (
        <Sequence key={i} from={Math.max(0, f(s.t))} durationInFrames={40} layout="none">
          <Audio src={staticFile(`sfx/${s.file}.wav`)} volume={s.vol} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
