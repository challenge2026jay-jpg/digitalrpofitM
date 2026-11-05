// Les 8 séquences de « Sans stock ≠ sans risque », calées sur les mots de la narration.
import React from "react";
import { Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { f } from "../timing";
import { C, Card, Check, Icon, Pill, Pop, fontFamily, usePop } from "../ui";
import { Flat, PhotoScene, WordReveal } from "../scenes12";
import { REVEAL, at, endOf } from "./timing";
import { DARK, Pic, RED, useShake } from "../pictos";

type SP = { start: number; dur: number };
const useLocal = (start: number) => (abs: number) => f(abs - start);

const PHOTO = { path: "img/samantha.jpg", img: { w: 1280, h: 1280 } };

// ---------- 1. Hook : face caméra, « SANS STOCK ≠ SANS RISQUE » ----------
export const SHook: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  // Scribe prolonge la fin de « stock » sur le silence : on cale le « ≠ » sur le début du mot.
  const neq = L(at("stock")) + 10;
  const shake = useShake(neq, 16, 12);
  return (
    <>
      {/* Zoom rapide vers le visage dès l'ouverture, puis image fixe : l'arrêt net tombe sur le « ≠ ». */}
      <PhotoScene {...PHOTO} dur={dur} enter="zoom" kb={{ from: 1, to: 1, ox: 50, oy: 28 }}
        punch={{ at: 0, scale: 1.22, ox: 50, oy: 26 }} />
      <Flat>
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 560, background: "linear-gradient(180deg, rgba(8,26,51,0) 0%, rgba(8,26,51,0.85) 65%)" }} />
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 150, display: "flex", flexDirection: "column", alignItems: "center", gap: 6 }}>
          <Pop cue={L(at("sans stock"))} from="up" damping={12}>
            <div style={{ fontSize: 112, fontWeight: 900, color: C.white, letterSpacing: 2, lineHeight: 1 }}>SANS STOCK</div>
          </Pop>
          <Pop cue={neq} from="scale" damping={10}>
            <div style={{ display: "flex", alignItems: "center", gap: 22 }}>
              <span style={{ display: "inline-block", fontSize: 120, fontWeight: 900, color: C.orange, lineHeight: 1, transform: `translateX(${shake}px) rotate(${shake / 2}deg)` }}>≠</span>
              <span style={{ fontSize: 104, fontWeight: 900, color: C.orange, letterSpacing: 2, lineHeight: 1 }}>SANS RISQUE</span>
            </div>
          </Pop>
        </div>
        <Pop cue={8} from="left" style={{ position: "absolute", left: 34, bottom: 46 }}>
          <Pill bg={C.white} color={C.navy} style={{ fontSize: 38 }}>Samantha Mwange</Pill>
        </Pop>
      </Flat>
    </>
  );
};

// ---------- 2. Le risque se déplace ----------
export const SDeplace: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const move = L(at("déplaces"));
  const gone = interpolate(frame, [move - 4, move + 4], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const targets = [
    { t: "Fournisseur", icon: Pic.factory(C.white, 64), x: 80, y: 560 },
    { t: "Livreur", icon: Pic.truck(C.white, 64), x: 540, y: 560 },
    { t: "Client", icon: Pic.user(C.white, 64), x: 80, y: 800 },
    { t: "Réputation", icon: Pic.star(C.white, 64), x: 540, y: 800 },
  ];
  return (
    <PhotoScene panel={DARK} dur={dur} enter="slideLeft" kb={{ from: 1, to: 1.04 }}>
      <div style={{ position: "absolute", inset: 0, fontFamily, color: C.white }}>
        <Pop cue={2} from="up" style={{ position: "absolute", left: 0, right: 0, top: 60, textAlign: "center" }}>
          <div style={{ fontSize: 64, fontWeight: 900 }}>Le stock disparaît.</div>
        </Pop>
        {/* La chambre et sa boîte de stock */}
        <div style={{ position: "absolute", left: 360, top: 190, width: 280, height: 280, display: "flex", alignItems: "center", justifyContent: "center", opacity: 0.35 + 0.65 * gone }}>
          {Pic.home(C.white, 260)}
          <div style={{ position: "absolute", top: 130, opacity: gone, transform: `scale(${0.4 + 0.6 * gone})` }}>{Pic.box(C.yellow, 110)}</div>
        </div>
        {targets.map((tg, i) => (
          <Pop key={tg.t} cue={move + 3 + i * 5} from="scale" damping={11} style={{ position: "absolute", left: tg.x, top: tg.y }}>
            <div style={{ width: 380, height: 190, borderRadius: 30, background: "rgba(255,255,255,0.08)", border: "3px solid rgba(255,255,255,0.25)", display: "flex", alignItems: "center", gap: 20, padding: "0 26px" }}>
              <div style={{ position: "relative" }}>{tg.icon}<div style={{ position: "absolute", left: -22, top: -30 }}>{Pic.box(C.yellow, 44)}</div></div>
              <div>
                <div style={{ fontSize: 40, fontWeight: 800 }}>{tg.t}</div>
                <div style={{ fontSize: 30, fontWeight: 800, color: C.orange }}>risque</div>
              </div>
            </div>
          </Pop>
        ))}
        <Pop cue={move + 22} from="up" style={{ position: "absolute", left: 0, right: 0, bottom: 70, textAlign: "center" }}>
          <div style={{ fontSize: 56, fontWeight: 900 }}>Le <span style={{ color: C.orange }}>risque</span> change d'endroit.</div>
        </Pop>
      </div>
    </PhotoScene>
  );
};

// ---------- 3. Le parcours de commande ----------
export const SParcours: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const nodes = [
    { t: "Client", icon: Pic.user(C.navy, 66), cue: L(at("client")) },
    { t: "Boutique", icon: Pic.store(C.navy, 66), cue: L(at("ton produit")) },
    { t: "Fournisseur", icon: Pic.factory(C.navy, 66), cue: L(at("commande")) },
    { t: "Client", icon: Pic.user(C.navy, 66), cue: L(at("système")) },
  ];
  const platforms = [["Facebook", L(at("Facebook"))], ["Instagram", L(at("Instagram"))], ["WhatsApp", L(at("WhatsApp"))]] as const;
  const pays = [["Mobile Money", L(at("paie"))], ["Avance", L(at("selon"))], ["Paiement à la livraison", L(at("système"))]] as const;
  // Le colis avance d'une étape à l'autre à partir de la commande.
  const colis = interpolate(frame, [L(at("commande")), L(endOf("place"))], [0, 3], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const order = usePop(L(at("commande")), 12);
  const X0 = 50, STEP = 236, Y = 330;
  return (
    <PhotoScene panel={C.white} dur={dur} enter="slideUp" kb={{ from: 1, to: 1.03 }}>
      <div style={{ position: "absolute", inset: 0, fontFamily, color: C.navy }}>
        <Pop cue={2} from="up" style={{ position: "absolute", left: 0, right: 0, top: 50, textAlign: "center" }}>
          <Pill bg={C.navy} style={{ fontSize: 36 }}>LE PARCOURS D'UNE COMMANDE</Pill>
        </Pop>
        {/* Ligne du parcours */}
        <div style={{ position: "absolute", left: X0 + 90, top: Y + 70, width: STEP * 3, height: 8, borderRadius: 4, background: "#DCE8F3" }}>
          <div style={{ width: `${(colis / 3) * 100}%`, height: "100%", borderRadius: 4, background: C.orange }} />
        </div>
        {nodes.map((n, i) => (
          <Pop key={i} cue={n.cue} from="scale" damping={11} style={{ position: "absolute", left: X0 + i * STEP, top: Y }}>
            <div style={{ width: 180, display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
              <div style={{ width: 150, height: 150, borderRadius: 999, background: "#EEF5FB", border: `5px solid ${i === 2 ? C.orange : C.skyDeep}`, display: "flex", alignItems: "center", justifyContent: "center" }}>{n.icon}</div>
              <div style={{ fontSize: 32, fontWeight: 800 }}>{n.t}</div>
            </div>
          </Pop>
        ))}
        {frame >= L(at("commande")) && (
          <div style={{ position: "absolute", left: X0 + 90 + colis * STEP - 38, top: Y + 30 }}>{Pic.box(C.yellow, 76)}</div>
        )}
        <div style={{ position: "absolute", left: 40, top: 640, display: "flex", flexDirection: "column", gap: 14 }}>
          <div style={{ fontSize: 30, fontWeight: 700, opacity: 0.6 }}>Le client voit ton produit sur</div>
          {platforms.map(([p, c]) => (
            <Pop key={p} cue={c} from="left"><Pill bg={C.navy} style={{ fontSize: 34, padding: "10px 26px" }}>{p}</Pill></Pop>
          ))}
        </div>
        <div style={{ position: "absolute", right: 40, top: 640, display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 14 }}>
          <div style={{ fontSize: 30, fontWeight: 700, opacity: 0.6 }}>Il paie par</div>
          {pays.map(([p, c]) => (
            <Pop key={p} cue={c} from="right"><Pill bg={C.green} style={{ fontSize: 32, padding: "10px 24px" }}>{Pic.money(C.white, 40)}{p}</Pill></Pop>
          ))}
        </div>
        {/* Notification de commande (illustrative) */}
        <div style={{ position: "absolute", left: 210, top: 1000, width: 580, opacity: order, transform: `translateY(${(1 - order) * -60}px)` }}>
          <Card style={{ padding: "18px 26px", display: "flex", alignItems: "center", gap: 18, borderRadius: 26, border: `3px solid ${C.orange}` }}>
            {Pic.box(C.orange, 56)}
            <div style={{ fontSize: 36, fontWeight: 800 }}>Nouvelle commande</div>
          </Card>
        </div>
      </div>
    </PhotoScene>
  );
};

// ---------- 4. Les problèmes réels ----------
const Alert: React.FC<{ cue: number; icon: React.ReactNode; a: string; b: string; dim: boolean }> = ({ cue, icon, a, b, dim }) => {
  const shake = useShake(cue + 4, 10, 10);
  return (
    <Pop cue={cue} from="left">
      <div style={{
        width: 900, display: "flex", alignItems: "center", gap: 24, padding: "20px 28px", borderRadius: 26,
        background: "rgba(255,77,79,0.12)", border: `3px solid ${RED}`, transform: `translateX(${shake}px)`, opacity: dim ? 0.55 : 1,
      }}>
        <div style={{ width: 84, height: 84, borderRadius: 22, background: RED, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>{icon}</div>
        <div style={{ fontSize: 48, fontWeight: 900, color: C.white }}>{a} <span style={{ color: RED }}>{b}</span></div>
      </div>
    </Pop>
  );
};

export const SProblemes: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const items = [
    { a: "Rupture", b: "fournisseur", cue: L(at("fournisseur", "problèmes")), icon: Pic.factory(C.white, 56) },
    { a: "Produit", b: "différent", cue: L(at("produit", "rupture")), icon: Pic.box(C.white, 56) },
    { a: "Livraison", b: "retardée", cue: L(at("délai")), icon: Pic.clock(C.white, 56) },
    { a: "Client", b: "absent", cue: L(at("client", "délai")), icon: Pic.phone(C.white, 56) },
    { a: "Commande", b: "refusée", cue: L(at("refuser")), icon: Pic.ban(C.white, 56) },
  ];
  return (
    <PhotoScene panel={DARK} dur={dur} enter="zoom" kb={{ from: 1, to: 1.04 }}>
      <div style={{ position: "absolute", inset: 0, fontFamily, display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 60, gap: 26 }}>
        <Pop cue={2} from="scale">
          <Pill bg={RED} style={{ fontSize: 40 }}><Icon.warning size={44} color={C.white} /> LES VRAIS PROBLÈMES</Pill>
        </Pop>
        {items.map((it, i) => (
          <Alert key={it.a} cue={it.cue} icon={it.icon} a={it.a} b={it.b} dim={i < items.length - 1 && frame > (items[i + 1]?.cue ?? 1e9) + 6} />
        ))}
      </div>
    </PhotoScene>
  );
};

// ---------- 5. La responsabilité revient vers toi ----------
const Notif: React.FC<{ cue: number; text: string }> = ({ cue, text }) => {
  const p = usePop(cue, 13);
  return (
    <div style={{ opacity: p, transform: `translateY(${(1 - p) * -80}px)` }}>
      <div style={{ width: 610, background: C.white, borderRadius: 26, padding: "16px 22px", boxShadow: "0 10px 26px rgba(0,0,0,0.25)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 24, fontWeight: 800, color: C.green }}>
          <Icon.chat size={30} color={C.green} /> MESSAGE · CLIENT
        </div>
        <div style={{ fontSize: 31, fontWeight: 700, color: C.navy, marginTop: 6, lineHeight: 1.25 }}>{text}</div>
      </div>
    </div>
  );
};

export const SRetour: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const n1 = L(at("cas")), n2 = L(at("Il va revenir"));
  const buzz = (cue: number) => (frame - cue >= 0 && frame - cue < 14 ? Math.sin((frame - cue) * 3) * 6 : 0);
  const back = L(at("revenir"));
  const arrow = interpolate(frame, [back, back + 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ring = usePop(L(at("toi")), 10);
  return (
    <PhotoScene panel={DARK} dur={dur} enter="slideUp" kb={{ from: 1, to: 1.03 }}>
      <div style={{ position: "absolute", inset: 0, fontFamily, color: C.white }}>
        {/* Téléphone générique */}
        <div style={{ position: "absolute", left: 160, top: 50, width: 680, height: 560, borderRadius: 50, border: "8px solid rgba(255,255,255,0.3)", background: "rgba(255,255,255,0.06)", transform: `translateX(${buzz(n1) + buzz(n2)}px)`, display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 50, gap: 22 }}>
          <Notif cue={n1} text="Bonjour, où est ma commande ?" />
          <Notif cue={n2} text="Le produit ne ressemble pas à la photo." />
        </div>
        {/* Fournisseur : le client ne lui écrit pas */}
        <Pop cue={L(at("fournisseur", "écrire"))} from="left" style={{ position: "absolute", left: 60, top: 700 }}>
          <div style={{ width: 300, height: 260, borderRadius: 30, border: "3px solid rgba(255,255,255,0.25)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 12, position: "relative" }}>
            {Pic.factory(C.white, 90)}
            <div style={{ fontSize: 36, fontWeight: 800 }}>Fournisseur</div>
            <div style={{ position: "absolute", top: 10, right: 10 }}>{Pic.ban(RED, 60)}</div>
          </div>
        </Pop>
        {/* Flèche qui revient vers Samantha */}
        <svg style={{ position: "absolute", left: 360, top: 790, overflow: "visible" }} width={260} height={80}>
          <path d="M10 40 H230 M200 12 L236 40 L200 68" stroke={C.orange} strokeWidth={10} fill="none" strokeLinecap="round" strokeLinejoin="round"
            strokeDasharray={320} strokeDashoffset={320 * (1 - arrow)} />
        </svg>
        <Pop cue={back} from="right" style={{ position: "absolute", left: 640, top: 680 }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12 }}>
            <div style={{ width: 230, height: 230, borderRadius: 999, padding: 8, background: ring > 0.05 ? RED : "rgba(255,255,255,0.3)", boxShadow: `0 0 0 ${16 * ring}px rgba(255,77,79,${0.35 * ring})` }}>
              <Img src={staticFile("img/samantha.jpg")} style={{ width: "100%", height: "100%", borderRadius: 999, objectFit: "cover", objectPosition: "50% 25%", border: "6px solid white" }} />
            </div>
            <Pill bg={RED} style={{ fontSize: 40 }}>TOI</Pill>
          </div>
        </Pop>
      </div>
    </PhotoScene>
  );
};

// ---------- 6. Le calcul de marge ----------
export const SMarge: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const rows = [
    { t: "VENTE", v: 25, cue: L(at("25")) },
    { t: "PRODUIT", v: -9, cue: L(at("9")) },
    { t: "PUBLICITÉ", v: -4, cue: L(at("4")) },
    { t: "LIVRAISON", v: -4, cue: L(at("4", "publicité")) },
    { t: "COMMUNICATION", v: -1, cue: L(at("1")) },
    { t: "RETOURS / REFUS", v: -2, cue: L(at("2")) },
  ];
  const reveal = L(REVEAL);
  // Valeur restante, qui descend à chaque dépense annoncée.
  let remaining = 0;
  rows.forEach((r) => { if (frame >= r.cue) remaining += r.v; });
  const prev = rows.reduce((acc, r) => (frame >= r.cue + 8 ? acc + r.v : acc), 0);
  const last = [...rows].reverse().find((r) => frame >= r.cue);
  const k = last ? interpolate(frame, [last.cue, last.cue + 8], [0, 1], { extrapolateRight: "clamp" }) : 0;
  const shown = last ? prev + (remaining - prev) * k : 0;
  const final = usePop(reveal, 9, 0.5);
  return (
    <PhotoScene panel={C.white} dur={dur} enter="zoom" kb={{ from: 1, to: 1.03 }}>
      <div style={{ position: "absolute", inset: 0, fontFamily, color: C.navy, padding: "40px 60px" }}>
        <Pop cue={3} from="scale" style={{ display: "flex", justifyContent: "center", marginBottom: 18 }}>
          <Pill bg={C.navy} style={{ fontSize: 36 }}>LE VRAI CALCUL D'UNE COMMANDE</Pill>
        </Pop>
        <div style={{ display: "flex", flexDirection: "column", gap: 10, opacity: 1 - 0.55 * final }}>
          {rows.map((r) => (
            <Pop key={r.t} cue={r.cue} from={r.v > 0 ? "scale" : "right"} damping={13}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", fontSize: 50, fontWeight: 800, borderBottom: "2px dashed #D5E2EE", padding: "6px 0" }}>
                <span>{r.t}</span>
                <span style={{ color: r.v > 0 ? C.green : RED, fontWeight: 900 }}>{r.v > 0 ? `+${r.v}` : `−${-r.v}`} $</span>
              </div>
            </Pop>
          ))}
        </div>
        {/* Barre de marge : 25 → 16 → 12 → 8 → 7 → 5 */}
        <div style={{ marginTop: 34 }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 34, fontWeight: 800 }}>
            <span>Il te reste</span><span style={{ color: shown <= 8 ? RED : C.green }}>{Math.round(shown)} $</span>
          </div>
          <div style={{ height: 40, borderRadius: 22, background: "#E3EEF8", marginTop: 10 }}>
            <div style={{ width: `${(shown / 25) * 100}%`, height: "100%", borderRadius: 22, background: shown <= 8 ? RED : C.green }} />
          </div>
        </div>
        {/* Résultat final */}
        <div style={{ position: "absolute", left: 40, right: 40, bottom: 50, opacity: final, transform: `scale(${1.6 - 0.6 * final})` }}>
          <div style={{ background: C.navy, color: C.white, borderRadius: 34, padding: "26px 20px", textAlign: "center", boxShadow: "0 18px 40px rgba(11,37,69,0.35)" }}>
            <div style={{ fontSize: 120, fontWeight: 900, color: C.yellow, lineHeight: 1 }}>5 $</div>
            <div style={{ fontSize: 50, fontWeight: 900, letterSpacing: 2 }}>DE MARGE RÉELLE</div>
          </div>
        </div>
      </div>
    </PhotoScene>
  );
};

// ---------- 7. La leçon stratégique ----------
export const SCriteres: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const crit = [
    { t: "Fournisseur", cue: L(at("fournisseur", "Vérifie")), x: 50, y: 120 },
    { t: "Paiement", cue: L(at("paiement")), x: 620, y: 120 },
    { t: "Livraison", cue: L(at("livraison", "zone")), x: 40, y: 600 },
    { t: "Taux de refus", cue: L(at("taux")), x: 545, y: 600 },
    { t: "Marge réelle", cue: L(at("coût réel")), x: 320, y: 745 },
  ];
  const lesson = L(at("et le coût"));
  return (
    <PhotoScene panel={DARK} dur={dur} enter="slideLeft" kb={{ from: 1, to: 1.04 }}>
      <div style={{ position: "absolute", inset: 0, fontFamily, color: C.white }}>
        <Pop cue={4} from="scale" style={{ position: "absolute", left: 0, right: 0, top: 30, display: "flex", justifyContent: "center" }}>
          <Pill bg={C.white} color={C.navy} style={{ fontSize: 36 }}><Icon.pin size={42} /> EN RDC, VÉRIFIE AUSSI</Pill>
        </Pop>
        <Pop cue={L(at("seulement"))} from="scale" style={{ position: "absolute", left: 360, top: 230 }}>
          <div style={{ width: 280, height: 280, borderRadius: 999, padding: 8, background: `conic-gradient(${C.orange}, ${C.yellow}, ${C.orange})` }}>
            <Img src={staticFile("img/samantha.jpg")} style={{ width: "100%", height: "100%", borderRadius: 999, objectFit: "cover", objectPosition: "50% 25%", border: "6px solid white" }} />
          </div>
        </Pop>
        {crit.map((c) => (
          <Pop key={c.t} cue={c.cue} from="scale" damping={12} style={{ position: "absolute", left: c.x, top: c.y }}>
            <div style={{ display: "flex", alignItems: "center", gap: 14, background: "rgba(255,255,255,0.1)", border: `3px solid ${C.green}`, borderRadius: 999, padding: "14px 28px 14px 16px" }}>
              <Check cue={c.cue + 3} size={50} />
              <span style={{ fontSize: 40, fontWeight: 800 }}>{c.t}</span>
            </div>
          </Pop>
        ))}
        <Pop cue={lesson} from="up" style={{ position: "absolute", left: 40, right: 40, bottom: 50 }}>
          <div style={{ background: C.yellow, color: C.navy, borderRadius: 30, padding: "26px 30px", textAlign: "center", fontSize: 48, fontWeight: 900, lineHeight: 1.2 }}>
            Une commande reçue n'est pas encore une commande rentable.
          </div>
        </Pop>
      </div>
    </PhotoScene>
  );
};

// ---------- 8. Appel à l'action ----------
export const SCta: React.FC<SP> = ({ start, dur }) => {
  const L = useLocal(start);
  const frame = useCurrentFrame();
  const join = L(at("Rejoins"));
  const bounce = usePop(join, 7, 0.6);
  const lien = L(at("lien"));
  const arrowY = frame > lien ? Math.abs(Math.sin((frame - lien) / 6)) * 16 : 0;
  const zoom = interpolate(frame, [0, f(dur)], [1, 1.05]);
  return (
    <PhotoScene panel={C.white} dur={dur} enter="zoom" kb={{ from: 1, to: 1 }}>
      <div style={{ position: "absolute", inset: 0, fontFamily, color: C.navy, display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 60, transform: `scale(${zoom})` }}>
        <Pop cue={2} from="scale">
          <div style={{ width: 300, height: 300, borderRadius: 999, padding: 8, background: `conic-gradient(${C.orange}, ${C.yellow}, ${C.whatsapp}, ${C.orange})`, boxShadow: "0 16px 36px rgba(11,37,69,0.25)" }}>
            <Img src={staticFile("img/samantha.jpg")} style={{ width: "100%", height: "100%", borderRadius: 999, objectFit: "cover", objectPosition: "50% 25%", border: "8px solid white" }} />
          </div>
        </Pop>
        <Pop cue={6} from="up"><div style={{ fontSize: 46, fontWeight: 900, marginTop: 16 }}>Samantha Mwange</div></Pop>
        <div style={{ marginTop: 30 }}>
          <WordReveal size={66} color={C.navy} words={[
            { t: "VENDS", cue: L(at("vendre")) },
            { t: "PLUS", cue: L(at("plus")) },
            { t: "INTELLIGEMMENT", cue: L(at("intelligemment")), hl: true },
            { t: "EN", cue: L(at("RDC", "intelligemment")) },
            { t: "RDC", cue: L(at("RDC", "intelligemment")), hl: true },
          ]} />
        </div>
        <div style={{
          marginTop: 40, display: "inline-flex", alignItems: "center", gap: 16, background: C.whatsapp, color: C.white, borderRadius: 999,
          padding: "20px 40px", fontSize: 48, fontWeight: 900, opacity: bounce, transform: `scale(${0.5 + 0.5 * bounce})`,
        }}>
          <Icon.chat size={58} /> Rejoins ma chaîne WhatsApp
        </div>
        <Pop cue={lien} from="up" style={{ marginTop: 34, display: "flex", alignItems: "center", gap: 14 }}>
          <div style={{ transform: `translateY(${-arrowY}px) rotate(180deg)` }}><Icon.arrowDown size={64} color={C.orange} /></div>
          <span style={{ fontSize: 48, fontWeight: 900 }}>Lien dans la bio</span>
        </Pop>
      </div>
    </PhotoScene>
  );
};

export const SCENE_COMPONENTS = { hook: SHook, deplace: SDeplace, parcours: SParcours, problemes: SProblemes, retour: SRetour, marge: SMarge, criteres: SCriteres, cta: SCta };
