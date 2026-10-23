// Version storyboard en 12 scènes, à partir des images du dossier Drive « Identité Claude ».
// Chaque scène place une image dans un cadre photo et y ajoute des incrustations calées sur les mots.
import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { WORDS, at, endOf, f } from "./timing";
import { C, Card, Check, Icon, Pill, Pop, fontFamily, usePop } from "./ui";

// ---------- Découpage : une scène par passage de narration ----------

const pre = 0.1;
export const VOICE_END = WORDS[WORDS.length - 1].end;
const END_HOLD = 4.2; // écran final lisible après la dernière phrase

const B = [
  0,
  at("Elle suit") - pre,
  at("Elle recommence") - pre,
  at("Depuis la RDC") - pre,
  at("puis consulte") - pre,
  at("Si ce n'est") - pre,
  at("Tu peux apprendre") - pre,
  at("Un blocage") - pre,
  at("Si tu veux explorer") - pre,
  at("clique") - pre,
  at("On avancera") - pre,
  VOICE_END + 0.3,
  VOICE_END + 0.3 + END_HOLD,
];

export const SCENES12 = B.slice(0, 12).map((s, i) => [s, B[i + 1]] as const);
export const TOTAL12_SECONDS = B[12];
export const TOTAL12_FRAMES = Math.ceil(TOTAL12_SECONDS * 30);
export const OV = 9; // chevauchement entre scènes (fondu enchaîné)

// ---------- Cadre photo ----------

const CARD = { left: 40, top: 590, w: 1000, h: 1180 };
const IMG = { w: 1224, h: 1632 };
const S = CARD.w / IMG.w; // échelle image → cadre
const OVERFLOW = IMG.h * S - CARD.h;

// Position d'un point de l'image source (pixels 1224×1632) dans le cadre.
const P = (x: number, y: number, focusY: number) => ({ x: x * S, y: y * S - OVERFLOW * focusY });

type Enter = "zoom" | "slideLeft" | "slideUp" | "dissolve";
type Punch = { at: number; scale: number; ox: number; oy: number };

type PhotoProps = {
  src: string;
  dur: number;
  enter: Enter;
  focusY?: number;
  kb?: { from: number; to: number; ox?: number; oy?: number; panX?: number };
  punch?: Punch;
  filter?: (frame: number) => string;
  children?: React.ReactNode;
};

export const PhotoScene: React.FC<PhotoProps> = ({ src, dur, enter, focusY = 0.5, kb = { from: 1, to: 1.06 }, punch, filter, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const total = f(dur);
  const slow = enter === "dissolve";
  const e = spring({ frame, fps, config: { damping: slow ? 26 : 16, stiffness: slow ? 70 : 140 } });
  const fadeIn = interpolate(frame, [0, slow ? 18 : 8], [0, 1], { extrapolateRight: "clamp" });
  const exit = interpolate(frame, [total, total + OV], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const enterTr =
    enter === "slideLeft" ? `translateX(${(1 - e) * 1100}px)` :
    enter === "slideUp" ? `translateY(${(1 - e) * 420}px)` :
    enter === "zoom" ? `scale(${1.1 - 0.1 * e})` : "";

  // Caméra simulée : zoom lent (Ken Burns) + éventuel « punch-in » sur un mot.
  const kbScale = interpolate(frame, [0, total + OV], [kb.from, kb.to]);
  const panX = interpolate(frame, [0, total + OV], [0, kb.panX ?? 0]);
  const pz = punch ? spring({ frame: frame - punch.at, fps, config: { damping: 18, stiffness: 120 } }) : 0;
  const scale = kbScale * (1 + (punch ? (punch.scale - 1) * pz : 0));
  const ox = punch ? interpolate(pz, [0, 1], [kb.ox ?? 50, punch.ox]) : kb.ox ?? 50;
  const oy = punch ? interpolate(pz, [0, 1], [kb.oy ?? 45, punch.oy]) : kb.oy ?? 45;

  return (
    <div style={{
      position: "absolute", left: CARD.left, top: CARD.top, width: CARD.w, height: CARD.h,
      borderRadius: 44, overflow: "hidden", background: C.navy,
      boxShadow: "0 24px 60px rgba(11,37,69,0.30)", border: "6px solid rgba(255,255,255,0.95)",
      opacity: Math.min(fadeIn, exit), transform: enterTr, fontFamily, color: C.navy,
    }}>
      <div style={{ position: "absolute", inset: 0, transform: `translateX(${panX}px) scale(${scale})`, transformOrigin: `${ox}% ${oy}%` }}>
        <Img
          src={staticFile(`img/scenes/${src}`)}
          style={{ position: "absolute", left: 0, top: -OVERFLOW * focusY, width: IMG.w * S, height: IMG.h * S, filter: filter?.(frame) }}
        />
        {children}
      </div>
    </div>
  );
};

// Les incrustations « à plat » (hors zoom) se posent dans ce calque, aux coordonnées du cadre.
const Flat: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div style={{ position: "absolute", left: CARD.left, top: CARD.top, width: CARD.w, height: CARD.h, fontFamily, color: C.navy, pointerEvents: "none" }}>
    {children}
  </div>
);

const useLocal = (start: number) => (abs: number) => f(abs - start);
type SP = { start: number; dur: number };

// Surligneur animé : un cadre arrondi qui se trace autour d'une zone de l'image.
const Ring: React.FC<{ cue: number; x: number; y: number; w: number; h: number; color?: string }> = ({ cue, x, y, w, h, color = C.orange }) => {
  const p = usePop(cue, 16);
  const per = 2 * (w + h);
  return (
    <svg style={{ position: "absolute", left: x - 8, top: y - 8, overflow: "visible" }} width={w + 16} height={h + 16}>
      <rect x={4} y={4} width={w + 8} height={h + 8} rx={18} fill={`rgba(255,201,60,${0.18 * p})`}
        stroke={color} strokeWidth={7} strokeDasharray={per} strokeDashoffset={per * (1 - p)} />
    </svg>
  );
};

const Bottom: React.FC<{ children: React.ReactNode; h?: number }> = ({ children, h = 420 }) => (
  <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: h, background: "linear-gradient(180deg, rgba(11,37,69,0) 0%, rgba(11,37,69,0.78) 60%)" }}>
    <div style={{ position: "absolute", left: 36, right: 36, bottom: 40, display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
      {children}
    </div>
  </div>
);

// Texte animé mot par mot, chaque mot apparaissant sur son propre instant.
const WordReveal: React.FC<{ words: { t: string; cue: number; hl?: boolean }[]; size?: number; color?: string }> = ({ words, size = 72, color = C.white }) => (
  <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "4px 18px" }}>
    {words.map((w, i) => (
      <Pop key={i} cue={w.cue} from="up" damping={12}>
        <span style={{
          display: "inline-block", fontSize: size, fontWeight: 900, lineHeight: 1.12, color: w.hl ? C.navy : color,
          background: w.hl ? C.yellow : "transparent", padding: w.hl ? "0 14px" : 0, borderRadius: 14,
          textShadow: w.hl ? "none" : "0 3px 14px rgba(0,0,0,0.35)",
        }}>{w.t}</span>
      </Pop>
    ))}
  </div>
);

// ---------- Les 12 scènes ----------

// 1. Grâce découvre le dropshipping.
export const S01: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  return (
    <>
      <PhotoScene src="01.jpg" dur={dur} enter="zoom" focusY={0.3} kb={{ from: 1.02, to: 1.1, ox: 40, oy: 35 }} />
      <Flat>
        <Pop cue={L(at("Grâce"))} from="left" style={{ position: "absolute", left: 34, top: 40 }}>
          <Pill bg={C.navy} style={{ fontSize: 50, padding: "14px 36px" }}>GRÂCE</Pill>
        </Pop>
        <Pop cue={L(at("Congolaise"))} from="right" style={{ position: "absolute", right: 34, top: 44 }}>
          <Pill bg={C.white} color={C.navy}><Icon.pin size={44} /> RDC</Pill>
        </Pop>
        <Pop cue={L(at("dropshipping"))} from="up" style={{ position: "absolute", left: 0, right: 0, bottom: 56, display: "flex", justifyContent: "center" }}>
          <Pill bg={C.orange} style={{ fontSize: 50, padding: "16px 44px" }}>DROPSHIPPING</Pill>
        </Pop>
      </Flat>
    </>
  );
};

// 2. Le compte ne s'ouvre pas : zoom sur l'écran d'erreur générique au mot « bloque ».
export const S02: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const bloque = L(at("bloque"));
  const words = ["Tu", "bloques", "toujours", "au", "même", "endroit", "?"];
  return (
    <>
      <PhotoScene src="02.jpg" dur={dur} enter="slideUp" focusY={0.55}
        kb={{ from: 1.0, to: 1.04, ox: 50, oy: 50 }} punch={{ at: bloque, scale: 1.16, ox: 55, oy: 64 }} />
      <Flat>
        <Bottom h={460}>
          <WordReveal size={74} words={words.map((t, i) => ({ t, cue: bloque + 3 + i * 3, hl: i >= 3 && i <= 5 }))} />
        </Bottom>
      </Flat>
    </>
  );
};

// 3. Le doute : image désaturée, rythme ralenti, deux causes possibles.
export const S03: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const nulle = L(endOf("nulle"));
  const Opt: React.FC<{ cue: number; icon: React.ReactNode; t: string }> = ({ cue, icon, t }) => (
    <Pop cue={cue} from="up">
      <Card style={{ width: 860, display: "flex", alignItems: "center", gap: 22, padding: "22px 28px", borderRadius: 28 }}>
        {icon}<span style={{ fontSize: 42, fontWeight: 800, flex: 1, lineHeight: 1.15 }}>{t}</span><Icon.question size={56} />
      </Card>
    </Pop>
  );
  return (
    <>
      <PhotoScene src="03.jpg" dur={dur} enter="dissolve" focusY={0.35} kb={{ from: 1.03, to: 1.14, ox: 45, oy: 30 }}
        filter={(fr) => {
          const d = interpolate(fr, [L(at("sent")), nulle + 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return `saturate(${1 - 0.45 * d}) brightness(${1 - 0.12 * d})`;
        }} />
      <Flat>
        <Pop cue={L(at("Le doute"))} from="scale" style={{ position: "absolute", left: 0, right: 0, top: 40, display: "flex", justifyContent: "center" }}>
          <Pill bg={C.navy} style={{ fontSize: 42 }}>LE DOUTE</Pill>
        </Pop>
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 44, display: "flex", flexDirection: "column", alignItems: "center", gap: 14 }}>
          <Opt cue={L(at("erreur"))} icon={<Icon.cursor size={60} />} t="Erreur de manipulation" />
          <Pop cue={L(at("ou une condition"))} from="scale">
            <div style={{ width: 92, height: 92, borderRadius: 999, background: C.orange, color: C.white, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 38, fontWeight: 900 }}>OU</div>
          </Pop>
          <Opt cue={L(at("condition"))} icon={<Icon.globe size={60} />} t="Condition d'accès liée au pays" />
        </div>
      </Flat>
    </>
  );
};

// 4. La checklist : on coche « Étape qui bloque » au mot « note ».
export const S04: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const fy = 0.5;
  const box = P(200, 640, fy);
  const line = P(250, 588, fy);
  return (
    <>
      <PhotoScene src="04.jpg" dur={dur} enter="slideLeft" focusY={fy} kb={{ from: 1.0, to: 1.07, ox: 30, oy: 35 }}>
        <Ring cue={L(at("note"))} x={line.x} y={line.y} w={410} h={78} />
        <div style={{ position: "absolute", left: box.x - 34, top: box.y - 34 }}><Check cue={L(at("qui bloque"))} size={68} /></div>
      </PhotoScene>
      <Flat>
        <Pop cue={L(at("RDC"))} from="right" style={{ position: "absolute", right: 30, top: 36 }}>
          <Pill bg={C.white} color={C.navy} style={{ fontSize: 40, boxShadow: "0 10px 24px rgba(11,37,69,0.2)" }}><Icon.pin size={48} /> Depuis la RDC</Pill>
        </Pop>
        <Pop cue={L(at("sans vérifier"))} from="left" style={{ position: "absolute", left: 30, top: 140 }}>
          <Pill bg={C.navy} style={{ fontSize: 34 }}><Icon.shield size={42} /> VÉRIFIER AVANT DE COPIER</Pill>
        </Pop>
      </Flat>
    </>
  );
};

// 5. La documentation officielle (interface illustrative) : « Pays, compte, conditions ».
export const S05: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const fy = 0.15;
  const after = "documentation";
  const rows = [
    { y: 440, cue: L(at("pays", after)) },
    { y: 570, cue: L(at("activité")) },
    { y: 680, cue: L(at("compte", after)) },
  ];
  const tiles = [
    { t: "Pays", cue: L(at("pays", after)), icon: <Icon.flag size={58} /> },
    { t: "Compte", cue: L(at("compte", after)), icon: <Icon.user size={58} /> },
    { t: "Conditions", cue: L(at("acceptés")), icon: <Icon.doc size={58} /> },
  ];
  return (
    <>
      <PhotoScene src="05.jpg" dur={dur} enter="zoom" focusY={fy} kb={{ from: 1.02, to: 1.12, ox: 60, oy: 25 }}>
        {rows.map((r, i) => {
          const p = P(230, r.y, fy);
          return <Ring key={i} cue={r.cue} x={p.x} y={p.y} w={720} h={70} color={C.green} />;
        })}
      </PhotoScene>
      <Flat>
        <Bottom h={440}>
          <div style={{ display: "flex", gap: 20 }}>
            {tiles.map((t) => (
              <Pop key={t.t} cue={t.cue} from="up" damping={11}>
                <Card style={{ width: 280, height: 200, padding: 16, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 10, borderBottom: `10px solid ${C.orange}` }}>
                  {t.icon}<span style={{ fontSize: 46, fontWeight: 900 }}>{t.t}</span>
                </Card>
              </Pop>
            ))}
          </div>
        </Bottom>
      </Flat>
    </>
  );
};

// 6. Demander confirmation : exemple de message, présenté comme tel.
export const S06: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const stamp = usePop(L(at("avant de payer")), 9, 0.5);
  return (
    <>
      <PhotoScene src="06.jpg" dur={dur} enter="slideUp" focusY={0.4} kb={{ from: 1.0, to: 1.06, ox: 35, oy: 45 }} />
      <Flat>
        <Pop cue={L(at("demande"))} from="up" style={{ position: "absolute", left: 30, bottom: 60 }}>
          <div style={{ width: 640, background: C.white, borderRadius: "34px 34px 34px 8px", padding: "24px 30px", boxShadow: "0 16px 36px rgba(11,37,69,0.3)" }}>
            <div style={{ fontSize: 26, fontWeight: 800, color: C.orange, letterSpacing: 1.5 }}>EXEMPLE DE MESSAGE</div>
            <div style={{ fontSize: 36, fontWeight: 600, lineHeight: 1.3, marginTop: 8 }}>
              Bonjour, votre service accepte-t-il les utilisateurs en RDC pour une activité de dropshipping ?
            </div>
          </div>
        </Pop>
        <div style={{
          position: "absolute", right: 30, top: 50, transform: `rotate(-7deg) scale(${2.2 - 1.2 * stamp})`, opacity: stamp,
          border: `7px solid ${C.green}`, color: C.green, borderRadius: 18, padding: "10px 22px", fontSize: 38, fontWeight: 900,
          background: "rgba(255,255,255,0.95)", fontFamily,
        }}>VÉRIFIE AVANT DE PAYER</div>
      </Flat>
    </>
  );
};

// 7. Continuer à apprendre : vérifications et apprentissage avancent en parallèle.
export const S07: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const par = L(at("Tu peux apprendre"));
  const fill = (d: number) => interpolate(frame, [par + d, par + d + 40], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const Bar: React.FC<{ label: string; v: number; color: string }> = ({ label, v, color }) => (
    <div style={{ width: 760 }}>
      <div style={{ fontSize: 34, fontWeight: 700, marginBottom: 8 }}>{label}</div>
      <div style={{ height: 26, borderRadius: 20, background: "#E3EEF8" }}>
        <div style={{ width: `${8 + v * 80}%`, height: "100%", borderRadius: 20, background: color }} />
      </div>
    </div>
  );
  return (
    <>
      <PhotoScene src="07.jpg" dur={dur} enter="zoom" focusY={0.35} kb={{ from: 1.08, to: 1.0, ox: 40, oy: 50 }} />
      <Flat>
        <Pop cue={par + 2} from="up" style={{ position: "absolute", left: 0, right: 0, bottom: 44, display: "flex", justifyContent: "center" }}>
          <Card style={{ padding: "26px 36px", display: "flex", flexDirection: "column", gap: 18, alignItems: "center" }}>
            <Bar label="Vérifications" v={fill(0)} color={C.green} />
            <Bar label="Apprentissage" v={fill(4)} color={C.orange} />
            <Pop cue={L(at("parallèle"))} from="scale"><Pill bg={C.navy} style={{ fontSize: 32 }}>EN PARALLÈLE</Pill></Pop>
          </Card>
        </Pop>
      </Flat>
    </>
  );
};

// 8. Reprendre confiance : la phrase centrale portée par une typographie animée.
export const S08: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const from = WORDS.findIndex((w) => w.start >= at("Un blocage") - 0.01);
  const to = WORDS.findIndex((w) => w.text.startsWith("capable"));
  const words = WORDS.slice(from, to + 1).map((w) => ({
    t: w.text, cue: L(w.start) - 1, hl: /blocage|capable/.test(w.text),
  }));
  const glow = usePop(L(at("capable")), 20);
  return (
    <>
      <PhotoScene src="08.jpg" dur={dur} enter="dissolve" focusY={0.25} kb={{ from: 1.1, to: 1.02, ox: 50, oy: 30 }}
        filter={() => `brightness(${1 + 0.06 * glow}) saturate(${1 + 0.1 * glow})`} />
      <Flat>
        <Bottom h={560}>
          <WordReveal size={78} words={words} />
        </Bottom>
      </Flat>
    </>
  );
};

// 9. Le contexte de la RDC (aucune ville nommée : le visuel ne permet pas de l'identifier).
export const S09: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const chips = [
    { t: "Dropshipping", cue: L(at("explorer")), bg: C.orange, fg: C.white },
    { t: "E-commerce", cue: L(at("l'e-commerce")), bg: C.navy, fg: C.white },
    { t: "Réalités de la RDC", cue: L(at("réalités")), bg: C.white, fg: C.navy },
  ];
  return (
    <>
      <PhotoScene src="09.jpg" dur={dur} enter="slideUp" focusY={0.45} kb={{ from: 1.06, to: 1.12, ox: 50, oy: 40, panX: -40 }} />
      <Flat>
        <div style={{ position: "absolute", left: 40, bottom: 60, display: "flex", flexDirection: "column", alignItems: "flex-start", gap: 18 }}>
          {chips.map((c) => (
            <Pop key={c.t} cue={c.cue} from="left">
              <Pill bg={c.bg} color={c.fg} style={{ fontSize: 50, padding: "18px 40px", boxShadow: "0 12px 28px rgba(0,0,0,0.25)" }}>
                {c.t === "Réalités de la RDC" && <Icon.pin size={50} />}{c.t}
              </Pill>
            </Pop>
          ))}
        </div>
      </Flat>
    </>
  );
};

// Carte d'appel à l'action (scènes 10 et 12), sans lien ni QR code inventés.
const CtaCard: React.FC<{ cue: number; joinCue: number; width?: number }> = ({ cue, joinCue, width = 900 }) => {
  const frame = useCurrentFrame();
  const join = usePop(joinCue, 10);
  const bounce = frame > joinCue ? Math.abs(Math.sin((frame - joinCue) / 7)) * 6 : 0;
  return (
    <Pop cue={cue} from="up">
      <Card style={{ width, padding: "30px 34px", textAlign: "center" }}>
        <div style={{
          display: "inline-flex", alignItems: "center", gap: 16, background: C.whatsapp, color: C.white, borderRadius: 999,
          padding: "16px 34px", fontSize: 44, fontWeight: 900, whiteSpace: "nowrap",
          transform: `scale(${1 + 0.08 * Math.sin(Math.min(1, join) * Math.PI)}) translateY(${-bounce}px)`,
        }}>
          <Icon.chat size={54} /> Rejoins ma chaîne WhatsApp
        </div>
        <div style={{ fontSize: 40, fontWeight: 700, marginTop: 18 }}>– clique sur le lien dans ma bio.</div>
      </Card>
    </Pop>
  );
};

// 10. Rejoindre WhatsApp.
export const S10: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  return (
    <>
      <PhotoScene src="10.jpg" dur={dur} enter="zoom" focusY={0.3} kb={{ from: 1.0, to: 1.08, ox: 50, oy: 35 }} />
      <Flat>
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 50, display: "flex", justifyContent: "center" }}>
          <CtaCard cue={L(at("clique")) + 2} joinCue={L(at("rejoins"))} />
        </div>
      </Flat>
    </>
  );
};

// 11. Avancer étape par étape.
export const S11: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const steps = L(at("étape par étape"));
  return (
    <>
      <PhotoScene src="11.jpg" dur={dur} enter="dissolve" focusY={0.4} kb={{ from: 1.04, to: 1.12, ox: 40, oy: 40, panX: 30 }} />
      <Flat>
        <Pop cue={steps - 4} from="up" style={{ position: "absolute", left: 0, right: 0, bottom: 70, display: "flex", flexDirection: "column", alignItems: "center", gap: 22 }}>
          <Pill bg={C.white} color={C.navy} style={{ fontSize: 48, padding: "16px 40px" }}>ÉTAPE PAR ÉTAPE</Pill>
          <div style={{ display: "flex", gap: 18 }}>
            {[0, 1, 2, 3].map((i) => <StepDot key={i} cue={steps + i * 6} />)}
          </div>
        </Pop>
      </Flat>
    </>
  );
};

const StepDot: React.FC<{ cue: number }> = ({ cue }) => {
  const p = usePop(cue, 12);
  return <div style={{ width: 70, height: 20, borderRadius: 10, background: p > 0.5 ? C.yellow : "rgba(255,255,255,0.45)", transform: `scaleX(${0.6 + 0.4 * p})` }} />;
};

// 12. Écran final : conclusion, photo réelle de Samantha, appel à l'action.
export const S12: React.FC<SP> = ({ start, dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const head = ["Le", "e-commerce,", "c'est", "possible", "aussi", "depuis", "la", "RDC\u00a0!"];
  const me = spring({ frame: frame - 16, fps, config: { damping: 14 } });
  return (
    <>
      <PhotoScene src="12.jpg" dur={dur + 1} enter="zoom" focusY={0.2} kb={{ from: 1.02, to: 1.08, ox: 55, oy: 30 }} />
      {/* Conclusion à la place des sous-titres */}
      <div style={{ position: "absolute", top: 300, left: 60, right: 60, fontFamily }}>
        <WordReveal size={66} color={C.navy} words={head.map((t, i) => ({ t, cue: 2 + i * 2, hl: t === "possible" || t.startsWith("RDC") }))} />
      </div>
      <Flat>
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 40, display: "flex", flexDirection: "column", alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 18, marginBottom: -30, zIndex: 2, opacity: me, transform: `translateY(${(1 - me) * 60}px)` }}>
            <div style={{ width: 170, height: 170, borderRadius: 999, padding: 6, background: `conic-gradient(${C.orange}, ${C.yellow}, ${C.whatsapp}, ${C.orange})`, boxShadow: "0 12px 28px rgba(0,0,0,0.3)" }}>
              <Img src={staticFile("img/samantha.jpg")} style={{ width: "100%", height: "100%", borderRadius: 999, objectFit: "cover", objectPosition: "50% 25%", border: "6px solid white" }} />
            </div>
            <Pill bg={C.navy} style={{ fontSize: 40, padding: "14px 32px" }}>Samantha Mwange</Pill>
          </div>
          <CtaCard cue={10} joinCue={24} width={920} />
        </div>
      </Flat>
    </>
  );
};

export const SCENE12_COMPONENTS = [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12];
