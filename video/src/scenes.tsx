import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { at, endOf, f } from "./timing";
import { C, Card, Check, Icon, Pill, Pop, fontFamily, usePop } from "./ui";

type SceneProps = { start: number; dur: number };

// Convertit un instant absolu de la narration en frame locale de la séquence.
export const OVERLAP = 7;

const useLocal = (start: number) => (abs: number) => f(abs - start);

// Conteneur de scène : entrée, sortie propre et léger mouvement de caméra simulé.
const Stage: React.FC<{ dur: number; children: React.ReactNode; zoom?: number; calm?: boolean }> = ({
  dur, children, zoom = 0.05, calm,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: calm ? 22 : 15, stiffness: calm ? 90 : 150 } });
  const total = f(dur);
  // La séquence dure OVERLAP frames de plus : la sortie se fond dans l'entrée de la suivante.
  const exit = interpolate(frame, [total - 1, total + OVERLAP], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const cam = interpolate(frame, [0, total], [1, 1 + zoom]);
  return (
    <div
      style={{
        position: "absolute", left: 0, right: 0, top: 660, height: 1130,
        display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
        fontFamily, color: C.navy,
        opacity: Math.min(enter * 1.3, exit),
        transform: `translateY(${(1 - enter) * 80}px) scale(${cam * (0.94 + 0.06 * enter) * (0.97 + 0.03 * exit)})`,
      }}
    >
      {children}
    </div>
  );
};

const Illustration: React.FC<{ src: string; size?: number; tint?: number }> = ({ src, size = 560, tint = 0 }) => (
  <Card style={{ padding: 18, width: size, height: size * 1.16, overflow: "hidden", position: "relative" }}>
    <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: "cover", borderRadius: 24 }} />
    {tint > 0 && (
      <div style={{ position: "absolute", inset: 18, borderRadius: 24, background: `rgba(19,49,92,${tint})` }} />
    )}
  </Card>
);

// 1. Introduction : Grâce, jeune Congolaise, veut se lancer.
export const SceneIntro: React.FC<SceneProps> = ({ start, dur }) => {
  const L = useLocal(start);
  return (
    <Stage dur={dur}>
      <div style={{ position: "relative" }}>
        <Pop cue={L(at("Grâce")) - 4} from="scale">
          <Illustration src="img/grace_concentree.png" size={540} />
        </Pop>
        <Pop cue={L(at("Grâce"))} from="left" style={{ position: "absolute", left: -70, top: 40 }}>
          <Pill bg={C.navy} style={{ fontSize: 48, padding: "14px 34px" }}>GRÂCE</Pill>
        </Pop>
        <Pop cue={L(at("Congolaise"))} from="right" style={{ position: "absolute", right: -80, top: 230 }}>
          <Pill bg={C.white} color={C.navy} style={{ boxShadow: "0 10px 24px rgba(11,37,69,0.15)" }}>
            <Icon.pin size={44} /> RDC
          </Pill>
        </Pop>
        <Pop cue={L(at("dropshipping"))} from="up" style={{ position: "absolute", left: -40, bottom: 40 }}>
          <Pill bg={C.orange} style={{ fontSize: 40 }}>DROPSHIPPING</Pill>
        </Pop>
      </div>
    </Stage>
  );
};

// 2. Le blocage : un tutoriel générique, une étape qui ne passe pas.
export const SceneBlocage: React.FC<SceneProps> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const bloque = L(at("bloque"));
  const isBlocked = frame >= bloque;
  const progress = interpolate(frame, [0, bloque], [0.08, 0.62], { extrapolateRight: "clamp" });
  const shake = isBlocked ? Math.sin((frame - bloque) * 1.6) * interpolate(frame - bloque, [0, 12], [10, 0], { extrapolateRight: "clamp" }) : 0;
  const steps = ["Étape 1", "Étape 2", "Ouvrir le compte"];
  const question = ["Tu", "bloques", "toujours", "au", "même", "endroit", "?"];
  return (
    <Stage dur={dur} zoom={0.04}>
      <Card style={{ width: 860, padding: 26 }}>
        <div style={{ background: C.navy, borderRadius: 24, height: 250, position: "relative", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <div style={{ position: "absolute", top: 20, left: 26, color: "rgba(255,255,255,0.75)", fontSize: 28, fontWeight: 700 }}>TUTORIEL</div>
          <div style={{ width: 110, height: 110, borderRadius: 999, background: "rgba(255,255,255,0.18)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Icon.play size={64} />
          </div>
          <div style={{ position: "absolute", left: 26, right: 26, bottom: 22, height: 10, borderRadius: 9, background: "rgba(255,255,255,0.25)" }}>
            <div style={{ width: `${progress * 100}%`, height: "100%", borderRadius: 9, background: C.orange }} />
          </div>
        </div>
        <div style={{ marginTop: 22, display: "flex", flexDirection: "column", gap: 14 }}>
          {steps.map((s, i) => {
            const last = i === steps.length - 1;
            return (
              <Pop key={s} cue={L(at("tutoriel")) + i * 5} from="left">
                <div style={{
                  display: "flex", alignItems: "center", gap: 20, padding: "16px 22px", borderRadius: 20,
                  background: last && isBlocked ? "#FFF1E3" : "#F2F7FC", fontSize: 38, fontWeight: 700,
                  border: last && isBlocked ? `3px solid ${C.orange}` : "3px solid transparent",
                  transform: last ? `translateX(${shake}px)` : undefined,
                }}>
                  {!last ? <Check cue={L(at("tutoriel")) + i * 5 + 6} size={52} /> :
                    isBlocked ? <Icon.warning size={52} /> :
                    <div style={{ width: 52, height: 52, borderRadius: 999, border: `6px solid ${C.skyDeep}`, borderTopColor: C.navy, transform: `rotate(${frame * 14}deg)` }} />}
                  <span>{s}</span>
                  {last && isBlocked && <span style={{ marginLeft: "auto", color: C.orange, fontWeight: 800 }}>bloqué</span>}
                </div>
              </Pop>
            );
          })}
        </div>
      </Card>
      {/* Texte principal 1, révélé mot par mot à partir de « bloque » */}
      <div style={{ marginTop: 44, width: 920, display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "0 20px" }}>
        {question.map((w, i) => {
          const hl = i >= 3 && i <= 5;
          return (
            <Pop key={i} cue={bloque + 4 + i * 3} from="up" damping={11}>
              <span style={{
                display: "inline-block", fontSize: 78, fontWeight: 900, lineHeight: 1.12,
                color: hl ? C.white : C.navy, background: hl ? C.navy : "transparent",
                padding: hl ? "0 14px" : 0, borderRadius: 16,
              }}>{w}</span>
            </Pop>
          );
        })}
      </div>
    </Stage>
  );
};

// 3. Le doute : elle recommence, elle se sent nulle. Rythme ralenti, image assombrie.
export const SceneDoute: React.FC<SceneProps> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const tries = frame < L(at("recommence")) + 8 ? 1 : frame < L(at("sent")) ? 2 : 3;
  const tint = interpolate(frame, [L(at("sent")), L(endOf("nulle")) + 10], [0, 0.18], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const spin = interpolate(frame, [0, f(dur)], [0, -540]);
  return (
    <Stage dur={dur} zoom={0.09} calm>
      <div style={{ position: "relative" }}>
        <Illustration src="img/grace_doute.png" size={560} tint={tint} />
        <Pop cue={L(at("recommence"))} from="scale" style={{ position: "absolute", right: -70, top: -40 }}>
          <Card style={{ padding: 22, display: "flex", alignItems: "center", gap: 16, borderRadius: 30 }}>
            <div style={{ transform: `rotate(${spin}deg)` }}><Icon.loop size={70} /></div>
            <span style={{ fontSize: 56, fontWeight: 900 }}>×{tries}</span>
          </Card>
        </Pop>
      </div>
    </Stage>
  );
};

// 4. Comprendre la cause possible : deux pistes, aucune présentée comme certaine.
export const SceneCause: React.FC<SceneProps> = ({ start, dur }) => {
  const L = useLocal(start);
  const Option: React.FC<{ cue: number; icon: React.ReactNode; title: string; color: string }> = ({ cue, icon, title, color }) => (
    <Pop cue={cue} from="up">
      <Card style={{ width: 800, display: "flex", alignItems: "center", gap: 28, borderTop: `12px solid ${color}`, padding: "30px 34px" }}>
        <div style={{ width: 110, height: 110, borderRadius: 28, background: "#EEF5FB", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
          {icon}
        </div>
        <div style={{ fontSize: 46, fontWeight: 800, lineHeight: 1.15, flex: 1 }}>{title}</div>
        <Icon.question size={64} />
      </Card>
    </Pop>
  );
  return (
    <Stage dur={dur} zoom={0.04}>
      <Pop cue={L(at("Le doute"))} from="scale">
        <Pill bg={C.navy} style={{ fontSize: 40, marginBottom: 40 }}>LE DOUTE</Pill>
      </Pop>
      <Option cue={L(at("erreur"))} icon={<Icon.cursor size={70} />} title="Erreur de manipulation" color={C.skyDeep} />
      <Pop cue={L(at("ou une condition"))} from="scale">
        <div style={{ margin: "26px 0", width: 110, height: 110, borderRadius: 999, background: C.orange, color: C.white, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 44, fontWeight: 900 }}>OU</div>
      </Pop>
      <Option cue={L(at("condition"))} icon={<Icon.globe size={70} />} title="Condition d'accès liée au pays" color={C.orange} />
    </Stage>
  );
};

// 5. Depuis la RDC : ne pas copier un tutoriel sans vérifier.
export const SceneRDC: React.FC<SceneProps> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const strike = interpolate(frame, [L(at("sans vérifier")), L(at("sans vérifier")) + 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Stage dur={dur} zoom={0.04}>
      <Pop cue={L(at("RDC"))} from="scale">
        <Card style={{ display: "flex", alignItems: "center", gap: 20, padding: "22px 40px", borderRadius: 999, marginBottom: 54 }}>
          <Icon.pin size={64} />
          <span style={{ fontSize: 52, fontWeight: 900 }}>Depuis la RDC</span>
        </Card>
      </Pop>
      <Pop cue={L(at("copier"))} from="left">
        <Card style={{ width: 820, display: "flex", alignItems: "center", gap: 26, position: "relative" }}>
          <Icon.copy size={80} />
          <span style={{ fontSize: 48, fontWeight: 800, opacity: 1 - 0.45 * strike }}>Copier un tutoriel</span>
          <div style={{ position: "absolute", left: 130, top: "50%", height: 8, borderRadius: 6, background: C.red, width: `${strike * 560}px` }} />
        </Card>
      </Pop>
      <Pop cue={L(at("sans vérifier")) + 4} from="scale">
        <div style={{ margin: "18px 0" }}><Icon.arrowDown size={80} /></div>
      </Pop>
      <Pop cue={L(at("vérifier"))} from="right">
        <Card style={{ width: 820, display: "flex", alignItems: "center", gap: 26, border: `4px solid ${C.green}` }}>
          <Icon.shield size={84} />
          <span style={{ fontSize: 46, fontWeight: 800, lineHeight: 1.15 }}>Vérifier si l'outil accepte ta situation</span>
        </Card>
      </Pop>
    </Stage>
  );
};

// 6. Les vérifications : noter, documentation officielle, puis « Pays, compte, conditions ».
export const SceneVerif: React.FC<SceneProps> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const after = "documentation";
  const tiles = [
    { label: "Pays", cue: L(at("pays", after)), icon: <Icon.flag size={70} /> },
    { label: "Compte", cue: L(at("compte", after)), icon: <Icon.user size={70} /> },
    { label: "Conditions", cue: L(at("acceptés")), icon: <Icon.doc size={70} /> },
  ];
  // La liste remonte et se compacte quand les trois mots-clés arrivent.
  const lift = spring({ frame: frame - tiles[0].cue + 6, fps: 30, config: { damping: 18 } });
  const Row: React.FC<{ cue: number; check: number; icon: React.ReactNode; text: string }> = ({ cue, check, icon, text }) => (
    <Pop cue={cue} from="left">
      <Card style={{ width: 840, display: "flex", alignItems: "center", gap: 24, padding: "24px 30px", borderRadius: 28 }}>
        {icon}
        <span style={{ fontSize: 44, fontWeight: 800, flex: 1 }}>{text}</span>
        <Check cue={check} size={62} />
      </Card>
    </Pop>
  );
  return (
    <Stage dur={dur} zoom={0.03}>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 22, transform: `translateY(${-lift * 40}px) scale(${1 - 0.1 * lift})` }}>
        <Pop cue={L(at("Avant de tout"))} from="scale">
          <Pill bg={C.navy} style={{ fontSize: 38, marginBottom: 8 }}>AVANT DE TOUT RECOMMENCER</Pill>
        </Pop>
        <Row cue={L(at("note"))} check={L(endOf("qui bloque"))} icon={<Icon.note size={66} />} text="Note l'étape qui bloque" />
        <Row cue={L(at("consulte"))} check={L(endOf("officielle"))} icon={<Icon.doc size={66} />} text="Documentation officielle" />
      </div>
      {/* Texte principal 2 : les trois mots apparaissent successivement */}
      <div style={{ display: "flex", gap: 26, marginTop: 40 }}>
        {tiles.map((t) => (
          <Pop key={t.label} cue={t.cue} from="up" damping={11}>
            <Card style={{ width: 270, height: 250, padding: 20, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16, borderBottom: `12px solid ${C.orange}` }}>
              {t.icon}
              <span style={{ fontSize: 48, fontWeight: 900 }}>{t.label}</span>
            </Card>
          </Pop>
        ))}
      </div>
    </Stage>
  );
};

// 7. Demander confirmation avant de payer, et apprendre le reste en parallèle.
export const ScenePayer: React.FC<SceneProps> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const stamp = usePop(L(endOf("payer")) - 6, 9, 0.5);
  const par = L(at("Tu peux apprendre"));
  const fill = (delay: number, speed: number) =>
    interpolate(frame, [par + delay, par + delay + f(speed)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const Bar: React.FC<{ label: string; v: number; color: string }> = ({ label, v, color }) => (
    <div style={{ width: 760 }}>
      <div style={{ fontSize: 36, fontWeight: 700, marginBottom: 10 }}>{label}</div>
      <div style={{ height: 30, borderRadius: 20, background: "#E3EEF8" }}>
        <div style={{ width: `${8 + v * 80}%`, height: "100%", borderRadius: 20, background: color }} />
      </div>
    </div>
  );
  return (
    <Stage dur={dur} zoom={0.04}>
      <Pop cue={L(at("Si ce n'est"))} from="scale">
        <Card style={{ display: "flex", alignItems: "center", gap: 22, padding: "26px 44px", borderRadius: 999 }}>
          <Icon.question size={66} />
          <span style={{ fontSize: 50, fontWeight: 900 }}>Pas clair ?</span>
        </Card>
      </Pop>
      <Pop cue={L(at("demande"))} from="up" style={{ marginTop: 34 }}>
        <Card style={{ width: 860, padding: "34px 36px", position: "relative", textAlign: "center" }}>
          <div style={{ fontSize: 50, fontWeight: 900 }}>Demande confirmation</div>
          <div style={{ fontSize: 40, fontWeight: 600, marginTop: 6, opacity: 0.75 }}>avant de payer</div>
          <div style={{
            position: "absolute", right: -26, bottom: -58, transform: `rotate(-8deg) scale(${2.2 - 1.2 * stamp})`, opacity: stamp,
            border: `6px solid ${C.green}`, color: C.green, borderRadius: 16, padding: "8px 18px", fontSize: 34, fontWeight: 900, background: "rgba(255,255,255,0.95)",
          }}>VÉRIFIE AVANT DE PAYER</div>
        </Card>
      </Pop>
      <Pop cue={par} from="up" style={{ marginTop: 100 }}>
        <Card style={{ padding: "30px 40px", display: "flex", flexDirection: "column", gap: 22, alignItems: "center" }}>
          <Bar label="Vérifications" v={fill(0, 1.6)} color={C.green} />
          <Bar label="Apprentissage" v={fill(3, 1.6)} color={C.orange} />
          <Pop cue={L(at("parallèle"))} from="scale">
            <Pill bg={C.navy} style={{ fontSize: 34 }}>EN PARALLÈLE</Pill>
          </Pop>
        </Card>
      </Pop>
    </Stage>
  );
};

// 8. Reprendre confiance : composition dégagée, mouvement lent, cadenas qui s'ouvre.
export const SceneConfiance: React.FC<SceneProps> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const open = frame >= L(at("capable")) - 2;
  const glow = usePop(L(at("capable")) - 2, 20);
  return (
    <Stage dur={dur} zoom={0.035} calm>
      <div style={{ position: "relative", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ position: "absolute", width: 760, height: 760, borderRadius: 999, background: `radial-gradient(circle, rgba(255,255,255,${0.75 * glow}) 0%, rgba(255,255,255,0) 70%)` }} />
        <Pop cue={4} from="scale" damping={22}>
          <Illustration src="img/grace_concentree.png" size={500} />
        </Pop>
        <Pop cue={L(at("blocage"))} from="scale" damping={18} style={{ position: "absolute", right: -90, top: -50 }}>
          <div style={{ width: 170, height: 170, borderRadius: 999, background: C.white, boxShadow: "0 16px 36px rgba(11,37,69,0.18)", display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${1 + 0.12 * Math.sin(glow * Math.PI)})` }}>
            {open ? <Icon.lockOpen size={100} /> : <Icon.lockClosed size={100} />}
          </div>
        </Pop>
      </div>
    </Stage>
  );
};

// 9. Appel à l'action : explorer le dropshipping en RDC, puis WhatsApp avec la photo de Samantha.
export const SceneCTA: React.FC<SceneProps> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const cta = L(at("clique"));
  const swap = spring({ frame: frame - cta + 4, fps: 30, config: { damping: 18 } });
  const bounce = Math.abs(Math.sin((frame - cta) / 7)) * 18;
  const steps = L(at("étape par étape"));
  const chips = [
    { t: "Dropshipping", c: L(at("explorer")), bg: C.orange },
    { t: "E-commerce", c: L(at("l'e-commerce")), bg: C.navy },
    { t: "Réalités de la RDC", c: L(at("réalités")), bg: C.white },
  ];
  return (
    <Stage dur={dur} zoom={0.02}>
      {/* Thèmes, puis remplacés par l'appel à l'action */}
      <div style={{ position: "absolute", top: 120, display: "flex", flexDirection: "column", alignItems: "center", gap: 26, opacity: Math.max(0, 1 - swap * 2.5), transform: `translateY(${-swap * 260}px) scale(${1 - 0.2 * swap})` }}>
        {chips.map((c) => (
          <Pop key={c.t} cue={c.c} from="up">
            <Pill bg={c.bg} color={c.bg === C.white ? C.navy : C.white} style={{ fontSize: 54, padding: "20px 44px", boxShadow: "0 12px 28px rgba(11,37,69,0.15)" }}>
              {c.t === "Réalités de la RDC" && <Icon.pin size={54} />}{c.t}
            </Pill>
          </Pop>
        ))}
      </div>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", opacity: swap, transform: `translateY(${(1 - swap) * 140}px)` }}>
        <div style={{ fontSize: 50, fontWeight: 900, marginBottom: 18 }}>Samantha Mwange</div>
        <div style={{ width: 330, height: 330, borderRadius: 999, padding: 10, background: `conic-gradient(${C.orange}, ${C.yellow}, ${C.whatsapp}, ${C.orange})`, boxShadow: "0 18px 40px rgba(11,37,69,0.25)" }}>
          <Img src={staticFile("img/samantha.jpg")} style={{ width: "100%", height: "100%", borderRadius: 999, objectFit: "cover", objectPosition: "50% 25%", border: "8px solid white" }} />
        </div>
        <Card style={{ marginTop: 44, width: 900, padding: "36px 40px", textAlign: "center" }}>
          <div style={{ display: "inline-flex", alignItems: "center", gap: 18, background: C.whatsapp, color: C.white, borderRadius: 999, padding: "18px 36px", fontSize: 44, fontWeight: 900, whiteSpace: "nowrap", transform: `translateY(${-bounce * 0.3}px)` }}>
            <Icon.chat size={58} /> Rejoins ma chaîne WhatsApp
          </div>
          <div style={{ fontSize: 42, fontWeight: 700, marginTop: 22 }}>– clique sur le lien dans ma bio.</div>
        </Card>
        <div style={{ display: "flex", gap: 22, marginTop: 40 }}>
          {[0, 1, 2, 3].map((i) => {
            const p = usePop(steps + i * 5, 12);
            return <div key={i} style={{ width: 60, height: 18, borderRadius: 9, background: p > 0.5 ? C.navy : "rgba(11,37,69,0.18)", transform: `scaleX(${0.6 + 0.4 * p})` }} />;
          })}
        </div>
      </div>
    </Stage>
  );
};
