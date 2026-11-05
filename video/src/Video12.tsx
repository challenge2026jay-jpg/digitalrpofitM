// Composition « DropshippingRDC12 » : storyboard en 12 scènes (images du dossier Drive « Identité Claude »).
import React from "react";
import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Captions } from "./Captions";
import { LEAD, at, f } from "./timing";
import { C } from "./ui";
import { Avatar, Chrome } from "./Video";
import { OV, SCENE12_COMPONENTS, SCENES12, TOTAL12_FRAMES, VOICE_END } from "./scenes12";

const start = (i: number) => SCENES12[i][0];

// Effets sonores : chacun accompagne une action visuelle précise.
const SFX: { file: string; t: number; vol: number }[] = [
  ...[1, 3, 4, 5, 8, 9, 11].map((i) => ({ file: "whoosh", t: start(i), vol: 0.2 })),
  { file: "pop", t: at("Grâce"), vol: 0.28 },
  { file: "pop", t: at("dropshipping"), vol: 0.25 },
  { file: "thud", t: at("bloque"), vol: 0.42 },
  { file: "pop", t: at("erreur"), vol: 0.26 },
  { file: "pop", t: at("condition"), vol: 0.26 },
  { file: "pop", t: at("RDC"), vol: 0.24 },
  { file: "ding", t: at("qui bloque"), vol: 0.3 },
  { file: "click", t: at("pays", "documentation"), vol: 0.3 },
  { file: "click", t: at("activité"), vol: 0.3 },
  { file: "click", t: at("compte", "documentation"), vol: 0.3 },
  { file: "pop", t: at("acceptés"), vol: 0.28 },
  { file: "pop", t: at("demande"), vol: 0.26 },
  { file: "thud", t: at("avant de payer"), vol: 0.38 },
  { file: "ding", t: at("capable"), vol: 0.3 },
  { file: "pop", t: at("clique"), vol: 0.28 },
  { file: "ding", t: start(11) + 0.4, vol: 0.28 },
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

export const DropshippingRDC12: React.FC = () => {
  const { fps } = useVideoConfig();
  const s8 = SCENES12[7];
  return (
    <AbsoluteFill style={{ backgroundColor: C.sky }}>
      <Background />
      {SCENE12_COMPONENTS.map((Comp, i) => {
        const [s, e] = SCENES12[i];
        const from = f(s);
        const last = i === SCENE12_COMPONENTS.length - 1;
        return (
          <Sequence key={i} from={from} durationInFrames={f(e) - from + (last ? 0 : OV)} layout="none">
            <Comp start={s} dur={e - s} />
          </Sequence>
        );
      })}
      {/* La phrase centrale (scène 8) et l'écran final portent déjà le texte à l'écran. */}
      <Captions hide={(t) => (t >= s8[0] + 0.05 && t < s8[1]) || t >= SCENES12[11][0]} />
      <Chrome />
      <Avatar hideAt={SCENES12[11][0] + 0.3} />

      <Sequence from={f(LEAD)} layout="none">
        <Audio src={staticFile("audio/voix_off_finale.wav")} volume={1} />
      </Sequence>
      <Audio
        src={staticFile("audio/musique_longue.mp3")}
        volume={(fr) => {
          const t = fr / fps;
          const fadeIn = interpolate(t, [0, 1], [0, 1], { extrapolateRight: "clamp" });
          // Discrète sous la voix, plus présente sur l'écran final.
          const bed = interpolate(t, [VOICE_END - 0.1, VOICE_END + 0.6], [0.09, 0.2], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const fadeOut = interpolate(fr, [TOTAL12_FRAMES - 36, TOTAL12_FRAMES], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return fadeIn * bed * fadeOut;
        }}
      />
      {SFX.map((s, i) => (
        <Sequence key={i} from={Math.max(0, f(s.t))} durationInFrames={30} layout="none">
          <Audio src={staticFile(`sfx/${s.file}.wav`)} volume={s.vol} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
