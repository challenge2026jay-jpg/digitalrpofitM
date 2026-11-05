// Les séquences de « Dropshipping local en RDC », chacune calée sur les mots de la narration.
// Palette : bleu foncé, noir, blanc, vert WhatsApp ; le rouge est réservé aux erreurs et aux risques.
import React from "react";
import { Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { f } from "../timing";
import { C, Check, Icon, Pill, Pop, fontFamily, usePop } from "../ui";
import { PhotoScene } from "../scenes12";
import { Pic, RED, useShake } from "../pictos";
import { at, endOf } from "./timing";

type SP = { start: number; dur: number };
const useLocal = (start: number) => (abs: number) => f(abs - start);

export const NAVY = "#0F2747";
export const INK = "#06101F";
const GREEN = C.whatsapp;
const LINE = "rgba(255,255,255,0.14)";

// Panneau sombre aux dimensions du cadre (même entrée/sortie que les autres vidéos).
const Panel: React.FC<SP & { enter?: "zoom" | "slideLeft" | "slideUp" | "dissolve"; children: React.ReactNode; bg?: string }> = ({
  dur, enter = "slideUp", children, bg = NAVY,
}) => (
  <PhotoScene panel={bg} dur={dur} enter={enter} kb={{ from: 1, to: 1.03 }}>
    <div style={{ position: "absolute", inset: 0, fontFamily, color: C.white }}>{children}</div>
  </PhotoScene>
);

const Title: React.FC<{ cue: number; children: React.ReactNode; color?: string; bg?: string; top?: number }> = ({
  cue, children, color = INK, bg = C.white, top = 50,
}) => (
  <Pop cue={cue} from="scale" style={{ position: "absolute", left: 0, right: 0, top, display: "flex", justifyContent: "center" }}>
    <Pill bg={bg} color={color} style={{ fontSize: 40, padding: "14px 34px" }}>{children}</Pill>
  </Pop>
);

// Photo (images du dossier Drive « Identité Claude ») dans un cadre arrondi.
const Photo: React.FC<{ src: string; x: number; y: number; w: number; h: number; focus?: string; cue?: number }> = ({
  src, x, y, w, h, focus = "50% 40%", cue = 0,
}) => {
  const frame = useCurrentFrame();
  const z = interpolate(frame, [cue, cue + 120], [1.04, 1.12], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Pop cue={cue} from="up" style={{ position: "absolute", left: x, top: y }}>
      <div style={{ width: w, height: h, borderRadius: 30, overflow: "hidden", border: `3px solid ${LINE}` }}>
        <Img src={staticFile(`img/scenes/${src}`)} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: focus, transform: `scale(${z})` }} />
      </div>
    </Pop>
  );
};

const Row: React.FC<{ cue: number; icon: React.ReactNode; text: React.ReactNode; tone?: "neutral" | "ok" | "risk"; check?: number; w?: number }> = ({
  cue, icon, text, tone = "neutral", check, w = 900,
}) => {
  const shake = useShake(tone === "risk" ? cue + 3 : -999, 10, 10);
  const border = tone === "ok" ? GREEN : tone === "risk" ? RED : LINE;
  const bg = tone === "ok" ? "rgba(37,211,102,0.12)" : tone === "risk" ? "rgba(255,77,79,0.14)" : "rgba(255,255,255,0.06)";
  return (
    <Pop cue={cue} from="left">
      <div style={{ width: w, display: "flex", alignItems: "center", gap: 22, padding: "18px 26px", borderRadius: 26, background: bg, border: `3px solid ${border}`, transform: `translateX(${shake}px)` }}>
        <div style={{ width: 78, height: 78, borderRadius: 20, background: tone === "risk" ? RED : tone === "ok" ? GREEN : "rgba(255,255,255,0.12)", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>{icon}</div>
        <div style={{ fontSize: 44, fontWeight: 800, flex: 1, lineHeight: 1.15 }}>{text}</div>
        {check !== undefined && <Check cue={check} size={58} color={GREEN} />}
      </div>
    </Pop>
  );
};

// ---------- 0:00 Hook : pas besoin de remplir sa maison de produits ----------
export const SSansStock: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const drops = [L(at("remplir")), L(at("maison")), L(at("produits"))];
  const away = interpolate(frame, [L(at("vendre")) - 2, L(at("vendre")) + 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Panel start={start} dur={dur} enter="zoom" bg={INK}>
      <Title cue={2}>PAS BESOIN D'UN GROS STOCK</Title>
      <div style={{ position: "absolute", left: 300, top: 220, width: 400, height: 400, opacity: 1 - 0.6 * away }}>
        {Pic.home(C.white, 400)}
        {drops.map((c, i) => {
          const p = usePop(c, 12);
          return (
            <div key={i} style={{ position: "absolute", left: 105 + i * 70, top: 330 - 40 * p - i * 8, opacity: p * (1 - away), transform: `translate(${away * (i - 1) * 260}px, ${-away * 300}px) rotate(${away * (i - 1) * 40}deg)` }}>
              {Pic.box(C.yellow, 90)}
            </div>
          );
        })}
      </div>
      <Pop cue={L(at("vendre"))} from="up" style={{ position: "absolute", left: 0, right: 0, top: 700, display: "flex", flexDirection: "column", alignItems: "center", gap: 22 }}>
        {Pic.phone(GREEN, 150)}
        <div style={{ fontSize: 58, fontWeight: 900 }}>Vendre en ligne <span style={{ color: GREEN }}>en RDC</span></div>
      </Pop>
    </Panel>
  );
};

// Mais pas n'importe quel produit.
export const SPasNimporte: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const pick = usePop(L(at("quel")), 12);
  const items = [Pic.fan, Pic.box, Pic.phone, Pic.camera, Pic.cart, Pic.star];
  return (
    <Panel start={start} dur={dur} enter="slideLeft">
      <Title cue={2}>PAS N'IMPORTE QUEL PRODUIT</Title>
      <div style={{ position: "absolute", left: 95, top: 220, width: 810, display: "flex", flexWrap: "wrap", gap: 30 }}>
        {items.map((ic, i) => {
          const chosen = i === 0;
          return (
            <Pop key={i} cue={L(at("n'importe")) + i * 3} from="scale">
              <div style={{
                width: 250, height: 250, borderRadius: 34, display: "flex", alignItems: "center", justifyContent: "center", position: "relative",
                background: "rgba(255,255,255,0.06)", border: `4px solid ${chosen && pick > 0.5 ? GREEN : LINE}`, opacity: chosen ? 1 : 1 - 0.55 * pick,
              }}>
                {ic(C.white, 120)}
                {!chosen && <div style={{ position: "absolute", top: 14, right: 14 }}><Icon.question size={52} color="#8AA0BF" /></div>}
                {chosen && <div style={{ position: "absolute", top: 14, right: 14, opacity: pick }}><Check cue={L(at("quel"))} size={56} color={GREEN} /></div>}
              </div>
            </Pop>
          );
        })}
      </div>
    </Panel>
  );
};

// La vraie méthode en trois étapes.
export const SMethode: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const confirm = usePop(L(at("confirme")), 12);
  return (
    <Panel start={start} dur={dur} enter="slideUp">
      <Title cue={2}>LA VRAIE MÉTHODE</Title>
      <div style={{ position: "absolute", left: 50, top: 200, display: "flex", flexDirection: "column", gap: 30 }}>
        <Row cue={L(at("produit utile"))} icon={Pic.factory(C.white, 54)} text={<>Un produit utile, chez un <span style={{ color: GREEN }}>fournisseur local</span></>} check={L(at("local", "fournisseur"))} />
        <Row cue={L(at("tester"))} icon={Pic.chats(C.white, 54)} text="Le tester avec ton audience" check={L(endOf("audience"))} />
        <Row cue={L(at("acheter"))} icon={Pic.cart(C.white, 54)} text="Acheter seulement quand le client confirme" tone={confirm > 0.5 ? "ok" : "neutral"} check={L(at("confirme"))} />
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 70, display: "flex", justifyContent: "center", opacity: confirm, transform: `scale(${0.8 + 0.2 * confirm})` }}>
        <Pill bg={GREEN} color={INK} style={{ fontSize: 46, padding: "18px 40px" }}><Icon.chat size={54} color={INK} /> Commande confirmée</Pill>
      </div>
    </Panel>
  );
};

export const SCommentTitre: React.FC<SP> = ({ start, dur }) => (
  <Panel start={start} dur={dur} enter="zoom" bg={INK}>
    <Pop cue={1} from="scale" style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ fontSize: 96, fontWeight: 900, textAlign: "center", lineHeight: 1.05 }}>Comment<br /><span style={{ color: GREEN }}>ça marche</span></div>
    </Pop>
  </Panel>
);

// ---------- 0:15 Le schéma : problème → fournisseur → contenu → commande → achat → livraison ----------
export const SSchema: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const steps = [
    { t: "Problème\nréel", icon: Pic.search, cue: L(at("problème", "identifies")) },
    { t: "Fournisseur\nlocal", icon: Pic.factory, cue: L(at("fournisseur", "Ensuite")) },
    { t: "Contenu", icon: Pic.camera, cue: L(at("photos")) },
    { t: "Commande\nconfirmée", icon: Pic.chats, cue: L(at("confirmes")) },
    { t: "Achat", icon: Pic.cart, cue: L(at("achètes")) },
    { t: "Livraison", icon: Pic.truck, cue: L(at("l'envoies")) },
  ];
  const X0 = 30, STEP = 160;
  // Le colis avance d'une étape à l'autre à chaque étape annoncée.
  const reached = steps.filter((s) => frame >= s.cue).length;
  const pos = steps.reduce((acc, s, i) => acc + interpolate(frame, [s.cue, s.cue + 12], [0, i === 0 ? 0 : 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }), 0);
  const panel = (from: number, to: number) => {
    const a = interpolate(frame, [from, from + 8, to - 4, to + 4], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    return { opacity: a, transform: `translateY(${(1 - a) * 30}px)` };
  };
  const pPub = L(at("publies")), pCmd = L(at("Quand un client", "TikTok")), pAchat = L(at("Ce n'est")), end = f(dur) + 10;
  const platforms = ["WhatsApp", "Facebook", "Instagram", "TikTok"];
  const checks = [["Numéro", L(at("numéro"))], ["Commune", L(at("commune"))], ["Prix total", L(at("prix total"))], ["Frais de livraison", L(at("frais"))]] as const;
  return (
    <Panel start={start} dur={dur} enter="slideLeft">
      {/* Schéma permanent en haut du cadre */}
      <div style={{ position: "absolute", left: X0 + 50, top: 92, width: STEP * 5, height: 8, borderRadius: 4, background: LINE }}>
        <div style={{ width: `${(pos / 5) * 100}%`, height: "100%", borderRadius: 4, background: GREEN }} />
      </div>
      {steps.map((s, i) => {
        const on = frame >= s.cue;
        return (
          <div key={i} style={{ position: "absolute", left: X0 + i * STEP, top: 40, width: 120, display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
            <div style={{ width: 110, height: 110, borderRadius: 999, background: on ? GREEN : INK, border: `4px solid ${on ? GREEN : LINE}`, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${on ? 1 : 0.9})` }}>
              {s.icon(on ? INK : "#8AA0BF", 58)}
            </div>
            <div style={{ fontSize: 22, fontWeight: 800, textAlign: "center", whiteSpace: "pre-line", lineHeight: 1.1, opacity: on ? 1 : 0.5 }}>{s.t}</div>
          </div>
        );
      })}
      {reached > 0 && <div style={{ position: "absolute", left: X0 + 30 + pos * STEP, top: 4 }}>{Pic.box(C.yellow, 60)}</div>}

      {/* Détail de l'étape en cours */}
      <div style={{ position: "absolute", left: 30, top: 270, width: 940, height: 880, ...panel(steps[0].cue - 4, steps[1].cue) }}>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 30, paddingTop: 120 }}>
          {Pic.search(GREEN, 220)}
          <div style={{ fontSize: 64, fontWeight: 900 }}>Un problème <span style={{ color: GREEN }}>réel</span></div>
        </div>
      </div>
      <div style={{ position: "absolute", left: 30, top: 270, width: 940, height: 880, ...panel(steps[1].cue, pPub - 6) }}>
        <Photo src="07.jpg" x={0} y={0} w={940} h={620} focus="50% 35%" cue={steps[1].cue} />
        <div style={{ position: "absolute", left: 0, right: 0, top: 660, display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
          <Pill bg={C.white} color={INK} style={{ fontSize: 40 }}>{Pic.factory(INK, 44)} Fournisseur local</Pill>
          <Pop cue={L(at("vérifies"))} from="up"><Pill bg={GREEN} color={INK} style={{ fontSize: 40 }}><Icon.shield size={44} color={INK} /> Produit vérifié toi-même</Pill></Pop>
        </div>
      </div>
      <div style={{ position: "absolute", left: 30, top: 270, width: 940, height: 880, ...panel(pPub - 6, pCmd) }}>
        <Photo src="10.jpg" x={0} y={0} w={940} h={600} focus="50% 30%" cue={pPub - 6} />
        <div style={{ position: "absolute", left: 0, right: 0, top: 640, display: "flex", flexWrap: "wrap", justifyContent: "center", gap: 16 }}>
          <Pill bg={C.white} color={INK} style={{ fontSize: 34 }}>{Pic.camera(INK, 40)} Tes propres photos et vidéos</Pill>
          {platforms.map((p) => (
            <Pop key={p} cue={L(at(p.replace("WhatsApp", "WhatsApp")))} from="up">
              <Pill bg={p === "WhatsApp" ? GREEN : "rgba(255,255,255,0.14)"} color={p === "WhatsApp" ? INK : C.white} style={{ fontSize: 36 }}>{p}</Pill>
            </Pop>
          ))}
        </div>
      </div>
      <div style={{ position: "absolute", left: 30, top: 270, width: 940, height: 880, ...panel(pCmd, pAchat) }}>
        <Photo src="06.jpg" x={0} y={0} w={940} h={520} focus="50% 30%" cue={pCmd} />
        <div style={{ position: "absolute", left: 0, top: 550, width: 940, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          {checks.map(([t, c]) => (
            <Pop key={t} cue={c} from="up">
              <div style={{ display: "flex", alignItems: "center", gap: 14, padding: "16px 20px", borderRadius: 22, background: "rgba(255,255,255,0.06)", border: `3px solid ${GREEN}` }}>
                <Check cue={c + 3} size={50} color={GREEN} />
                <span style={{ fontSize: 36, fontWeight: 800 }}>{t}</span>
              </div>
            </Pop>
          ))}
        </div>
      </div>
      <div style={{ position: "absolute", left: 30, top: 270, width: 940, height: 880, ...panel(pAchat, end) }}>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 34, paddingTop: 70 }}>
          <Pop cue={pAchat} from="scale"><Pill bg={GREEN} color={INK} style={{ fontSize: 44, padding: "16px 36px" }}><Icon.chat size={50} color={INK} /> Confirmation reçue</Pill></Pop>
          <Row cue={steps[4].cue} icon={Pic.cart(C.white, 54)} text="Tu achètes chez le fournisseur" w={860} />
          <Row cue={steps[5].cue} icon={Pic.truck(C.white, 54)} text="Tu livres le client" w={860} tone="ok" check={steps[5].cue + 8} />
        </div>
      </div>
    </Panel>
  );
};

// ---------- 0:40 Choisir le bon produit : quatre cartes ----------
export const SQuatreChoses: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const cards = [
    { t: "Problème réel", icon: Pic.search, cue: L(at("Premièrement")), done: L(at("Deuxièmement")) },
    { t: "Démonstration facile", icon: Pic.camera, cue: L(at("Deuxièmement")), done: L(at("Troisièmement")) },
    { t: "Disponibilité locale", icon: Pic.factory, cue: L(at("Troisièmement")), done: L(at("Quatrièmement")) },
    { t: "Marge après livraison", icon: Pic.truck, cue: L(at("Quatrièmement")), done: f(dur) - 6 },
  ];
  return (
    <Panel start={start} dur={dur} enter="zoom">
      <Title cue={L(at("vérifie"))}>VÉRIFIE 4 CHOSES</Title>
      <div style={{ position: "absolute", left: 40, top: 190, width: 920, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 26 }}>
        {cards.map((c, i) => {
          const active = frame >= c.cue && frame < c.done;
          return (
            <Pop key={c.t} cue={c.cue} from="scale" damping={12}>
              <div style={{
                height: 430, borderRadius: 36, padding: 28, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 22, position: "relative",
                background: active ? C.white : "rgba(255,255,255,0.06)", color: active ? INK : C.white,
                border: `4px solid ${frame >= c.done ? GREEN : active ? C.white : LINE}`, transform: `scale(${active ? 1.03 : 1})`,
              }}>
                <div style={{ position: "absolute", top: 18, left: 24, fontSize: 40, fontWeight: 900, color: active ? INK : GREEN }}>{i + 1}</div>
                {c.icon(active ? INK : C.white, 120)}
                <div style={{ fontSize: 42, fontWeight: 900, textAlign: "center", lineHeight: 1.1 }}>{c.t}</div>
                <div style={{ position: "absolute", top: 16, right: 16 }}><Check cue={c.done} size={56} color={GREEN} /></div>
              </div>
            </Pop>
          );
        })}
      </div>
    </Panel>
  );
};

// Un produit viral mal livré : un problème en attente (risque, en rouge).
export const SViral: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const ban = usePop(L(at("livrer")), 10);
  return (
    <Panel start={start} dur={dur} enter="slideLeft" bg={INK}>
      <Title cue={2}>PRODUIT VIRAL ?</Title>
      <div style={{ position: "absolute", left: 340, top: 230, width: 320, height: 320, borderRadius: 999, background: "rgba(255,255,255,0.06)", border: `4px solid ${LINE}`, display: "flex", alignItems: "center", justifyContent: "center" }}>
        {Pic.truck(C.white, 190)}
        <div style={{ position: "absolute", opacity: ban, transform: `scale(${1.6 - 0.6 * ban})` }}>{Pic.ban(RED, 300)}</div>
      </div>
      <Pop cue={L(at("opportunité"))} from="up" style={{ position: "absolute", left: 0, right: 0, top: 620, textAlign: "center" }}>
        <div style={{ fontSize: 60, fontWeight: 900 }}>Pas livrable <span style={{ color: RED }}>≠</span> opportunité</div>
      </Pop>
      <Pop cue={L(at("problème en attente"))} from="scale" style={{ position: "absolute", left: 60, right: 60, top: 770 }}>
        <div style={{ background: RED, borderRadius: 30, padding: "26px 20px", textAlign: "center", fontSize: 54, fontWeight: 900 }}>UN PROBLÈME EN ATTENTE</div>
      </Pop>
    </Panel>
  );
};

// ---------- 1:05 Exemple chiffré : le mini-ventilateur ----------
// `note` remplace le montant quand le texte ne donne pas de chiffre (aucun montant inventé).
const MarginBar: React.FC<{ value: number; max: number; color: string; label: string; note?: string }> = ({ value, max, color, label, note }) => (
  <div>
    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 36, fontWeight: 800 }}>
      <span>{label}</span><span style={{ color }}>{note ?? (value > 0 ? `${Math.round(value * 10) / 10} $` : "—")}</span>
    </div>
    <div style={{ height: 40, borderRadius: 22, background: "rgba(255,255,255,0.12)", marginTop: 10 }}>
      <div style={{ width: `${Math.max(0, value / max) * 100}%`, height: "100%", borderRadius: 22, background: color }} />
    </div>
  </div>
);

export const SCalcul: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const c8 = L(at("8")), c15 = L(at("15")), c3 = L(at("3")), c1 = L(at("1")), cRes = L(at("Il te reste"));
  const rows = [
    { t: "Prix de vente", v: "+15 $", cue: c15, good: true },
    { t: "Produit", v: "−8 $", cue: c8, good: false },
    { t: "Livraison", v: "−3 $", cue: c3, good: false },
    { t: "Suivi / emballage", v: "−1 $", cue: c1, good: false },
  ];
  // La barre part de 15 $ et descend à chaque coût : 15 → 7 → 4 → 3.
  const step = (cue: number, from: number, to: number) => interpolate(frame, [cue, cue + 10], [from, to], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const v = frame < c15 ? 0 : frame < c15 + 10 ? step(c15, 15, 15) : frame < c3 ? step(c15 + 10, 15, 7) : frame < c1 ? step(c3, 7, 4) : step(c1, 4, 3);
  const res = usePop(cRes, 10);
  return (
    <Panel start={start} dur={dur} enter="zoom">
      <Pop cue={L(at("mini-ventilateur"))} from="scale" style={{ position: "absolute", left: 0, right: 0, top: 36, display: "flex", justifyContent: "center" }}>
        <Pill bg={C.white} color={INK} style={{ fontSize: 42, padding: "14px 34px" }}>{Pic.fan(INK, 52)} Exemple : mini-ventilateur</Pill>
      </Pop>
      <div style={{ position: "absolute", left: 60, right: 60, top: 160, display: "flex", flexDirection: "column", gap: 8, opacity: 1 - 0.4 * res }}>
        {rows.map((r) => (
          <Pop key={r.t} cue={r.cue} from="right" damping={13}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", fontSize: 50, fontWeight: 800, borderBottom: `2px dashed ${LINE}`, padding: "10px 0" }}>
              <span>{r.t}</span><span style={{ color: r.good ? GREEN : C.white, fontWeight: 900 }}>{r.v}</span>
            </div>
          </Pop>
        ))}
      </div>
      <div style={{ position: "absolute", left: 60, right: 60, top: 600, opacity: frame >= c15 ? 1 : 0 }}>
        <MarginBar value={v} max={15} color={GREEN} label="Marge" />
      </div>
      <div style={{ position: "absolute", left: 60, right: 60, top: 790, opacity: res, transform: `scale(${1.4 - 0.4 * res})` }}>
        <div style={{ background: GREEN, color: INK, borderRadius: 34, padding: "22px 20px", textAlign: "center" }}>
          <div style={{ fontSize: 44, fontWeight: 900 }}>MARGE ESTIMÉE</div>
          <div style={{ fontSize: 110, fontWeight: 900, lineHeight: 1 }}>≈ 3 $</div>
          <div style={{ fontSize: 34, fontWeight: 800 }}>par commande livrée</div>
        </div>
      </div>
    </Panel>
  );
};

// Les risques qui font baisser la marge (rouge) — illustratif, sans chiffre inventé.
export const SRisquesMarge: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const risks = [
    { t: "Colis refusé", cue: L(at("refuse")), icon: Pic.ban(C.white, 50) },
    { t: "Prix fournisseur en hausse", cue: L(at("augmente")), icon: Pic.factory(C.white, 50) },
    { t: "Livraison plus chère que prévu", cue: L(at("plus cher")), icon: Pic.truck(C.white, 50) },
  ];
  const hit = risks.filter((r) => frame >= r.cue).length;
  const v = interpolate(hit, [0, 1, 2, 3], [3, 2.2, 1.5, 0.9]);
  const down = usePop(L(at("diminue")), 10);
  return (
    <Panel start={start} dur={dur} enter="slideUp">
      <div style={{ position: "absolute", left: 60, right: 60, top: 60 }}>
        <MarginBar value={v} max={3} color={hit ? RED : GREEN} label="Marge réelle" note={hit ? "en baisse" : "≈ 3 $"} />
      </div>
      <div style={{ position: "absolute", left: 50, top: 260, display: "flex", flexDirection: "column", gap: 22 }}>
        {risks.map((r) => <Row key={r.t} cue={r.cue} icon={r.icon} text={r.t} tone="risk" />)}
      </div>
      <Pop cue={L(at("diminue"))} from="scale" style={{ position: "absolute", left: 60, right: 60, bottom: 70, opacity: down }}>
        <div style={{ border: `4px solid ${RED}`, borderRadius: 30, padding: "22px 20px", textAlign: "center", fontSize: 54, fontWeight: 900, color: RED }}>TA MARGE DIMINUE</div>
      </Pop>
    </Panel>
  );
};

// Calculer sur les commandes livrées, pas sur les messages.
export const SLivrees: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const cross = usePop(L(at("pas sur les")), 10);
  return (
    <Panel start={start} dur={dur} enter="slideLeft" bg={INK}>
      <Title cue={2}>CALCULE SUR LES COMMANDES LIVRÉES</Title>
      <Pop cue={L(at("réellement"))} from="left" style={{ position: "absolute", left: 50, top: 220 }}>
        <div style={{ width: 430, height: 600, borderRadius: 34, border: `4px solid ${GREEN}`, background: "rgba(37,211,102,0.1)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 26 }}>
          {Pic.truck(GREEN, 170)}
          <div style={{ fontSize: 46, fontWeight: 900, textAlign: "center" }}>Commandes<br />livrées</div>
          <Check cue={L(at("livrées", "réellement")) + 2} size={80} color={GREEN} />
        </div>
      </Pop>
      <Pop cue={L(at("simples"))} from="right" style={{ position: "absolute", left: 520, top: 220 }}>
        <div style={{ width: 430, height: 600, borderRadius: 34, border: `4px solid ${LINE}`, background: "rgba(255,255,255,0.05)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 26, position: "relative", opacity: 1 - 0.35 * cross }}>
          {Pic.chats(C.white, 170)}
          <div style={{ fontSize: 46, fontWeight: 900, textAlign: "center" }}>Simples<br />messages</div>
          <div style={{ position: "absolute", left: 30, right: 30, top: "50%", height: 10, borderRadius: 6, background: RED, transform: `rotate(-18deg) scaleX(${cross})` }} />
        </div>
      </Pop>
    </Panel>
  );
};

// ---------- 1:35 Quatre erreurs (rouge) ----------
export const SErreurs: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const errs = [
    { t: "Produit non testé", cue: L(at("Première erreur")), icon: Pic.camera(C.white, 50) },
    { t: "Fournisseur unique", cue: L(at("Deuxième erreur")), icon: Pic.factory(C.white, 50) },
    { t: "Adresse non confirmée", cue: L(at("Troisième erreur")), icon: Icon.pin({ size: 50, color: C.white }) },
    { t: "Zone non maîtrisée", cue: L(at("Quatrième erreur")), icon: Pic.map(C.white, 50) },
  ];
  return (
    <Panel start={start} dur={dur} enter="zoom" bg={INK}>
      <Title cue={2} bg={RED} color={C.white}>ÉVITE 4 ERREURS</Title>
      <div style={{ position: "absolute", left: 50, top: 210, display: "flex", flexDirection: "column", gap: 28 }}>
        {errs.map((e) => <Row key={e.t} cue={e.cue} icon={e.icon} text={e.t} tone="risk" />)}
      </div>
    </Panel>
  );
};

// La bonne base : validations vertes, observation, puis décision.
export const SBonneBase: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const ok = [
    { t: "Produit testé", cue: L(at("seul produit")), icon: Pic.camera(INK, 50) },
    { t: "Livraison possible", cue: L(at("zone précise")), icon: Pic.truck(INK, 50) },
    { t: "Fournisseur vérifié", cue: L(at("fournisseur fiable")), icon: Pic.factory(INK, 50) },
    { t: "Commande confirmée", cue: L(at("commandes confirmées")), icon: Pic.chats(INK, 50) },
  ];
  const decide = L(at("décide"));
  const phaseA = interpolate(frame, [decide - 6, decide + 4], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const watch = [["Commandes confirmées", L(at("commandes confirmées")), GREEN], ["Livraisons réussies", L(at("réussies")), GREEN], ["Refus", L(at("refus", "réussies")), RED]] as const;
  return (
    <Panel start={start} dur={dur} enter="slideUp">
      <div style={{ opacity: phaseA }}>
        <Title cue={2} bg={GREEN} color={INK}>COMMENCE PETIT ET PRÉCIS</Title>
        <div style={{ position: "absolute", left: 50, top: 190, display: "flex", flexDirection: "column", gap: 18 }}>
          {ok.map((o) => (
            <Pop key={o.t} cue={o.cue} from="left">
              <div style={{ width: 900, display: "flex", alignItems: "center", gap: 20, padding: "14px 24px", borderRadius: 24, background: "rgba(37,211,102,0.12)", border: `3px solid ${GREEN}` }}>
                <div style={{ width: 70, height: 70, borderRadius: 18, background: GREEN, display: "flex", alignItems: "center", justifyContent: "center" }}>{o.icon}</div>
                <span style={{ fontSize: 42, fontWeight: 800, flex: 1 }}>{o.t}</span>
                <Check cue={o.cue + 3} size={54} color={GREEN} />
              </div>
            </Pop>
          ))}
        </div>
        <div style={{ position: "absolute", left: 50, right: 50, top: 760, display: "flex", gap: 16 }}>
          {watch.map(([t, c, col]) => (
            <Pop key={t} cue={c} from="up">
              <div style={{ width: 290, height: 150, borderRadius: 24, border: `3px solid ${col}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 6 }}>
                <div style={{ fontSize: 24, fontWeight: 700, opacity: 0.7 }}>À OBSERVER</div>
                <div style={{ fontSize: 32, fontWeight: 900, color: col, textAlign: "center", lineHeight: 1.1 }}>{t}</div>
              </div>
            </Pop>
          ))}
        </div>
      </div>
      {/* Décision, seulement après observation */}
      <div style={{ position: "absolute", inset: 0, opacity: 1 - phaseA }}>
        <Title cue={decide} top={60}>ENSUITE SEULEMENT, DÉCIDE</Title>
        <Pop cue={L(at("augmenter"))} from="left" style={{ position: "absolute", left: 50, top: 300 }}>
          <div style={{ width: 410, height: 420, borderRadius: 34, border: `4px solid ${LINE}`, background: "rgba(255,255,255,0.06)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 20 }}>
            {Pic.box(C.yellow, 150)}
            <div style={{ fontSize: 44, fontWeight: 900, textAlign: "center" }}>Augmenter<br />le stock</div>
          </div>
        </Pop>
        <div style={{ position: "absolute", left: 460, width: 80, top: 480, textAlign: "center", fontSize: 44, fontWeight: 900, opacity: 0.7 }}>ou</div>
        <Pop cue={L(at("continuer"))} from="right" style={{ position: "absolute", left: 540, top: 300 }}>
          <div style={{ width: 410, height: 420, borderRadius: 34, border: `4px solid ${GREEN}`, background: "rgba(37,211,102,0.1)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 20 }}>
            {Pic.chats(GREEN, 150)}
            <div style={{ fontSize: 44, fontWeight: 900, textAlign: "center" }}>Continuer<br />en précommande</div>
          </div>
        </Pop>
      </div>
    </Panel>
  );
};

// ---------- 1:55 Conclusion ----------
export const SGagnant: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const strike = usePop(L(at("gagnant")), 12);
  return (
    <Panel start={start} dur={dur} enter="zoom" bg={INK}>
      <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
        <Pop cue={L(at("simplement"))} from="scale">
          <div style={{ position: "relative", fontSize: 92, fontWeight: 900, textAlign: "center", lineHeight: 1.05, opacity: 1 - 0.4 * strike }}>
            « Produit<br />gagnant »
            <div style={{ position: "absolute", left: -20, right: -20, top: "50%", height: 12, borderRadius: 6, background: RED, transform: `rotate(-10deg) scaleX(${strike})` }} />
          </div>
        </Pop>
      </div>
    </Panel>
  );
};

export const SUtile: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const items = [
    { t: "Utile", cue: L(at("utile", "cherches un")), icon: Pic.search(INK, 48) },
    { t: "Acheté localement", cue: L(at("localement")), icon: Pic.factory(INK, 48) },
    { t: "Sans gros stock", cue: L(at("gros stock")), icon: Pic.box(INK, 48) },
    { t: "Livré avec une marge réelle", cue: L(at("marge réelle")), icon: Pic.truck(INK, 48) },
  ];
  return (
    <Panel start={start} dur={dur} enter="slideUp">
      <Title cue={2} bg={GREEN} color={INK}>LE BON PRODUIT</Title>
      <div style={{ position: "absolute", left: 50, top: 220, display: "flex", flexDirection: "column", gap: 26 }}>
        {items.map((o) => (
          <Pop key={o.t} cue={o.cue} from="left">
            <div style={{ width: 900, display: "flex", alignItems: "center", gap: 22, padding: "20px 26px", borderRadius: 26, background: C.white, color: INK }}>
              <div style={{ width: 76, height: 76, borderRadius: 20, background: GREEN, display: "flex", alignItems: "center", justifyContent: "center" }}>{o.icon}</div>
              <span style={{ fontSize: 46, fontWeight: 900, flex: 1 }}>{o.t}</span>
              <Check cue={o.cue + 3} size={56} color={GREEN} />
            </div>
          </Pop>
        ))}
      </div>
    </Panel>
  );
};

// ---------- 2:00 Écran final et appel WhatsApp ----------
export const SCta: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const join = usePop(L(at("Rejoins")), 8, 0.6);
  const lien = L(at("lien"));
  const arrowY = frame > lien ? Math.abs(Math.sin((frame - lien) / 6)) * 14 : 0;
  return (
    <Panel start={start} dur={dur} enter="zoom" bg={INK}>
      <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 50 }}>
        <Pop cue={2} from="scale">
          <div style={{ width: 300, height: 300, borderRadius: 999, padding: 8, background: GREEN, boxShadow: "0 0 0 10px rgba(37,211,102,0.2)" }}>
            <Img src={staticFile("img/samantha.jpg")} style={{ width: "100%", height: "100%", borderRadius: 999, objectFit: "cover", objectPosition: "50% 25%", border: "8px solid white" }} />
          </div>
        </Pop>
        <Pop cue={6} from="up"><div style={{ fontSize: 48, fontWeight: 900, marginTop: 18 }}>Samantha Mwange</div></Pop>
        <Pop cue={L(at("dropshipping", "tester"))} from="up" style={{ marginTop: 18 }}>
          <Pill bg="rgba(255,255,255,0.12)" color={C.white} style={{ fontSize: 36 }}>Dropshipping local en RDC</Pill>
        </Pop>
        <div style={{
          marginTop: 50, display: "inline-flex", alignItems: "center", gap: 16, background: GREEN, color: INK, borderRadius: 999,
          padding: "22px 42px", fontSize: 50, fontWeight: 900, opacity: join, transform: `scale(${0.5 + 0.5 * join})`, whiteSpace: "nowrap",
        }}>
          <Icon.chat size={60} color={INK} /> Rejoins ma chaîne WhatsApp
        </div>
        <Pop cue={lien} from="up" style={{ marginTop: 34, display: "flex", alignItems: "center", gap: 14 }}>
          <div style={{ transform: `translateY(${-arrowY}px) rotate(180deg)` }}><Icon.arrowDown size={64} color={GREEN} /></div>
          <span style={{ fontSize: 50, fontWeight: 900 }}>— lien dans la bio</span>
        </Pop>
      </div>
    </Panel>
  );
};

export const SCENE_COMPONENTS = {
  sansStock: SSansStock, pasNimporte: SPasNimporte, methode: SMethode, commentTitre: SCommentTitre, schema: SSchema,
  quatreChoses: SQuatreChoses, viral: SViral, calcul: SCalcul, risquesMarge: SRisquesMarge, livrees: SLivrees,
  erreurs: SErreurs, bonneBase: SBonneBase, gagnant: SGagnant, utile: SUtile, cta: SCta,
};
