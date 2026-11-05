// Composition « DropshippingLocal » : choisir un produit et vendre sans stock avec le dropshipping local en RDC.
// Musique et effets sonores : Mixkit (licences vérifiées, voir README) ; fichiers récupérés par data/mixkit_fetch.sh.
import React from "react";
import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Captions, CaptionTheme } from "../Captions";
import { LEAD, f, norm } from "../timing";
import { C, fontFamily } from "../ui";
import { Avatar } from "../Video";
import { OV } from "../scenes12";
import { RED } from "../pictos";
import { INK, NAVY, SCENE_COMPONENTS } from "./scenes";
import { ORDER, SCENES, SceneName, TOTAL_FRAMES, VOICE_END, WORDS, at, endOf } from "./timing";

const DARK_THEME: CaptionTheme = { text: C.white, mute: "rgba(255,255,255,0.32)", hlBg: C.whatsapp, hlText: INK, hlShadow: "#128C4A", riskBg: RED };
const KEYWORDS = new Set(["local", "localement", "fournisseur", "confirme", "confirmes", "confirmation", "rdc", "marge", "livrée", "livrées", "testé", "tester", "whatsapp", "utile", "réel", "réelle"].map(norm));
const RISKS = new Set(["refus", "refuse", "erreur", "erreurs", "diminue", "problème"].map(norm));

// Effets sonores Mixkit (public/mixkit/sfx-<id>.wav), chacun calé sur un mot ; volumes 20 à 30 %.
const S = (id: number, t: number, vol = 0.25, len = 45) => ({ id, t, vol, len });
const SFX = [
  // Transitions : 1490 « Fast whoosh transition » entre parties, 3120 « Technology transition slide » à l'intérieur
  ...(["methode", "schema", "quatreChoses", "calcul", "erreurs", "gagnant"] as SceneName[]).map((n) => S(1490, SCENES[n][0], 0.22)),
  ...(["pasNimporte", "commentTitre", "viral", "risquesMarge", "livrees", "bonneBase", "utile", "cta"] as SceneName[]).map((n) => S(3120, SCENES[n][0], 0.2)),
  // Colis : 1530 « Paper slide »
  ...[at("remplir"), at("maison"), at("produits")].map((t) => S(1530, t, 0.22)),
  S(1530, at("achètes"), 0.25), S(1530, at("l'envoies"), 0.25),
  // Clics : 2568 « Cool interface click tone »
  ...[at("problème", "identifies"), at("fournisseur", "Ensuite"), at("photos"), at("WhatsApp"), at("Facebook"), at("Instagram"), at("TikTok")].map((t) => S(2568, t, 0.25)),
  ...[at("Premièrement"), at("Deuxièmement"), at("Troisièmement"), at("Quatrièmement")].map((t) => S(2568, t, 0.25)),
  // Notification et message : 2354 « Message pop alert », 1393 « Smartphone typing »
  S(2354, at("Quand un client", "TikTok"), 0.25), S(1393, at("confirmes") + 0.1, 0.18, 75), S(2354, at("simples"), 0.22),
  // Validations : 1112 « Positive interface click », 2867 « Confirmation tone »
  S(2867, at("confirme"), 0.22), S(2867, at("Ce n'est"), 0.22),
  ...[endOf("audience"), at("vérifies"), at("seul produit"), at("zone précise"), at("fournisseur fiable"), at("commandes confirmées")].map((t) => S(1112, t, 0.25)),
  ...[at("utile", "cherches un"), at("localement"), at("gros stock"), at("marge réelle")].map((t) => S(1112, t, 0.25)),
  // Calcul : 2841 « Atm cash machine key press »
  ...[at("8"), at("15"), at("3"), at("1")].map((t) => S(2841, t, 0.3)),
  S(2867, at("Il te reste"), 0.25),
  // Erreurs et risques : 2569 « Negative tone interface tap », 2868 « Double beep tone alert »
  ...[at("Première erreur"), at("Deuxième erreur"), at("Troisième erreur"), at("Quatrième erreur")].map((t) => S(2569, t, 0.25)),
  ...[at("refuse"), at("augmente"), at("plus cher")].map((t) => S(2569, t, 0.22)),
  S(2868, at("problème en attente"), 0.2), S(2868, at("diminue"), 0.2),
  // Appel à l'action : 2865 « Success software tone »
  S(2865, at("Rejoins"), 0.25),
];

const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const drift = (frame * 0.5) % 72;
  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${NAVY} 0%, ${INK} 70%, #000000 100%)` }}>
      <AbsoluteFill style={{
        backgroundImage: "linear-gradient(rgba(255,255,255,0.05) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,0.05) 2px, transparent 2px)",
        backgroundSize: "72px 72px", backgroundPosition: `0 ${drift}px`,
      }} />
    </AbsoluteFill>
  );
};

const Chrome: React.FC = () => (
  <>
    <div style={{ position: "absolute", top: 92, left: 56, fontFamily }}>
      <div style={{ background: C.white, color: INK, fontWeight: 900, fontSize: 32, padding: "12px 24px", borderRadius: 999 }}>
        DROPSHIPPING <span style={{ color: "#128C4A" }}>LOCAL</span> · RDC
      </div>
    </div>
    <div style={{ position: "absolute", bottom: 64, left: 0, right: 0, display: "flex", justifyContent: "center", fontFamily }}>
      <div style={{ background: "rgba(255,255,255,0.1)", color: C.white, fontWeight: 800, fontSize: 26, letterSpacing: 2, padding: "12px 28px", borderRadius: 999 }}>
        TESTER AVANT D'ACHETER · SANS GROS STOCK
      </div>
    </div>
  </>
);

export const DropshippingLocal: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: INK }}>
      <Background />
      {ORDER.map((name) => {
        const [s, e] = SCENES[name];
        const Comp = SCENE_COMPONENTS[name];
        const from = f(s);
        return (
          <Sequence key={name} from={from} durationInFrames={f(e) - from + (name === "cta" ? 0 : OV)} layout="none">
            <Comp start={s} dur={e - s} />
          </Sequence>
        );
      })}
      <Captions words={WORDS} keywords={KEYWORDS} risks={RISKS} theme={DARK_THEME} />
      <Chrome />
      <Avatar showAt={0.4} hideAt={SCENES.cta[0] + 0.2} pill={C.white} pillText={INK} />

      <Sequence from={f(LEAD)} layout="none">
        <Audio src={staticFile("audio/local/voix_off_finale.wav")} volume={1} />
      </Sequence>
      {/* Mixkit « Focus on Yourself » (Eugenio Mininni) : environ 10 % sous la voix, fondu d'entrée et de sortie. */}
      <Audio
        src={staticFile("mixkit/music-568.mp3")}
        volume={(fr) => {
          const t = fr / fps;
          const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
          const fadeIn = interpolate(t, [0, 2], [0.4, 1], clamp);
          const level = interpolate(t, [VOICE_END - 0.2, VOICE_END + 0.6], [0.1, 0.12], clamp);
          const fadeOut = interpolate(fr, [TOTAL_FRAMES - 75, TOTAL_FRAMES], [1, 0], clamp);
          return fadeIn * level * fadeOut;
        }}
      />
      {SFX.map((s, i) => (
        <Sequence key={i} from={Math.max(0, f(s.t))} durationInFrames={s.len} layout="none">
          <Audio src={staticFile(`mixkit/sfx-${s.id}.wav`)} volume={s.vol} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
