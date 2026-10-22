import React from "react";
import { AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Captions } from "./Captions";
import { OVERLAP, SceneBlocage, SceneCause, SceneConfiance, SceneCTA, SceneDoute, SceneIntro, ScenePayer, SceneRDC, SceneVerif } from "./scenes";
import { LEAD, SCENES, SceneName, TOTAL_FRAMES, WORDS, at, endOf, f } from "./timing";
import { C, fontFamily } from "./ui";

const SCENE_COMPONENTS: Record<SceneName, React.FC<{ start: number; dur: number }>> = {
  intro: SceneIntro, blocage: SceneBlocage, doute: SceneDoute, cause: SceneCause, rdc: SceneRDC,
  verif: SceneVerif, payer: ScenePayer, confiance: SceneConfiance, cta: SceneCTA,
};

// Effets sonores, chacun calé sur un mot de la narration.
const SFX: { file: string; t: number; vol: number }[] = [
  ...(["blocage", "doute", "cause", "rdc", "verif", "payer", "cta"] as SceneName[]).map((s) => ({ file: "whoosh", t: SCENES[s][0], vol: 0.22 })),
  { file: "pop", t: at("Grâce"), vol: 0.3 },
  { file: "pop", t: at("dropshipping"), vol: 0.25 },
  { file: "thud", t: at("bloque"), vol: 0.45 },
  { file: "click", t: at("bloque") + 0.15, vol: 0.3 },
  { file: "pop", t: at("erreur"), vol: 0.28 },
  { file: "pop", t: at("condition"), vol: 0.28 },
  { file: "pop", t: at("RDC"), vol: 0.25 },
  { file: "ding", t: endOf("qui bloque"), vol: 0.3 },
  { file: "ding", t: endOf("officielle"), vol: 0.3 },
  { file: "pop", t: at("pays", "documentation"), vol: 0.3 },
  { file: "pop", t: at("compte", "documentation"), vol: 0.3 },
  { file: "pop", t: at("acceptés"), vol: 0.3 },
  { file: "thud", t: endOf("payer") - 0.1, vol: 0.4 },
  { file: "ding", t: at("capable"), vol: 0.32 },
  { file: "pop", t: at("clique"), vol: 0.3 },
];

const VOICE_END = WORDS[WORDS.length - 1].end;
const MUSIC_DELAY = 1.4;

const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  // Moment de doute : le bleu se densifie légèrement ; moment de confiance : il s'éclaircit.
  const doubt = interpolate(t, [SCENES.doute[0], SCENES.doute[0] + 0.6, SCENES.doute[1] - 0.3, SCENES.doute[1] + 0.3], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const calm = interpolate(t, [SCENES.confiance[0], SCENES.confiance[0] + 0.8, SCENES.confiance[1], SCENES.confiance[1] + 0.4], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const drift = (frame * 0.6) % 72;
  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, #D3EEFE 0%, ${C.sky} 45%, ${C.skyDeep} 100%)` }}>
      <AbsoluteFill style={{
        backgroundImage: "linear-gradient(rgba(255,255,255,0.45) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,0.45) 2px, transparent 2px)",
        backgroundSize: "72px 72px", backgroundPosition: `0 ${drift}px`, opacity: 0.55,
      }} />
      <div style={{ position: "absolute", width: 520, height: 520, borderRadius: 999, left: -180, top: 1180 + Math.sin(t / 2) * 30, background: "rgba(255,255,255,0.35)" }} />
      <div style={{ position: "absolute", width: 380, height: 380, borderRadius: 999, right: -140, top: 620 + Math.cos(t / 2.5) * 30, background: "rgba(255,201,60,0.18)" }} />
      <AbsoluteFill style={{ background: `rgba(19,49,92,${0.16 * doubt})` }} />
      <AbsoluteFill style={{ background: `rgba(255,255,255,${0.22 * calm})` }} />
    </AbsoluteFill>
  );
};

// Bulle photo en haut à droite, nom au-dessus ; elle s'efface quand la grande photo de fin apparaît.
const Avatar: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame: frame - 6, fps, config: { damping: 13 } });
  const hide = interpolate(frame, [f(at("clique")) - 8, f(at("clique")) + 4], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const breathe = 1 + 0.015 * Math.sin(frame / 18);
  return (
    <div style={{ position: "absolute", top: 50, right: 46, display: "flex", flexDirection: "column", alignItems: "center", opacity: enter * hide, transform: `scale(${(0.6 + 0.4 * enter) * breathe})`, transformOrigin: "top right", fontFamily }}>
      <div style={{ background: C.navy, color: C.white, fontWeight: 800, fontSize: 28, padding: "8px 20px", borderRadius: 999, marginBottom: 12, whiteSpace: "nowrap" }}>
        Samantha Mwange
      </div>
      <div style={{ width: 196, height: 196, borderRadius: 999, padding: 7, background: `conic-gradient(${C.orange}, ${C.yellow}, ${C.orange})`, boxShadow: "0 12px 28px rgba(11,37,69,0.25)" }}>
        <Img src={staticFile("img/samantha.jpg")} style={{ width: "100%", height: "100%", borderRadius: 999, objectFit: "cover", objectPosition: "50% 25%", border: "6px solid white" }} />
      </div>
    </div>
  );
};

const Chrome: React.FC = () => (
  <>
    <div style={{ position: "absolute", top: 92, left: 56, fontFamily, display: "flex", flexDirection: "column", gap: 10 }}>
      <div style={{ background: C.white, color: C.navy, fontWeight: 900, fontSize: 34, padding: "12px 26px", borderRadius: 999, boxShadow: "0 8px 20px rgba(11,37,69,0.12)" }}>
        DROPSHIPPING <span style={{ color: C.orange }}>RDC</span>
      </div>
    </div>
    <div style={{ position: "absolute", bottom: 64, left: 0, right: 0, display: "flex", justifyContent: "center", fontFamily }}>
      <div style={{ background: C.navy, color: C.white, fontWeight: 800, fontSize: 28, letterSpacing: 2, padding: "12px 30px", borderRadius: 999 }}>
        E-COMMERCE · RÉALITÉS DE LA RDC
      </div>
    </div>
  </>
);

export const DropshippingRDC: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: C.sky }}>
      <Background />
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
      <Captions />
      <Chrome />
      <Avatar />

      <Sequence from={f(LEAD)} layout="none">
        <Audio src={staticFile("audio/voix_off_finale.wav")} volume={1} />
      </Sequence>
      {/* Décalée pour que la fin naturelle du morceau tombe sur le dernier plan. */}
      <Sequence from={f(MUSIC_DELAY)} layout="none">
      <Audio
        src={staticFile("audio/musique.mp3")}
        volume={(fr) => {
          const t = fr / fps + MUSIC_DELAY;
          const fadeIn = interpolate(fr / fps, [0, 1.2], [0, 1], { extrapolateRight: "clamp" });
          // Musique discrète sous la voix, remonte légèrement après la dernière phrase, puis fondu.
          const bed = interpolate(t, [VOICE_END - 0.1, VOICE_END + 0.5], [0.09, 0.17], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const fadeOut = interpolate(fr + f(MUSIC_DELAY), [TOTAL_FRAMES - 24, TOTAL_FRAMES], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return fadeIn * bed * fadeOut;
        }}
      />
      </Sequence>
      {SFX.map((s, i) => (
        <Sequence key={i} from={Math.max(0, f(s.t))} durationInFrames={30} layout="none">
          <Audio src={staticFile(`sfx/${s.file}.wav`)} volume={s.vol} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
