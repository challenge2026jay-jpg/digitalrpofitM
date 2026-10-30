import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { at, f } from "./timing";
import { Body, Burst, C, Card, Echo, Icon, IconDot, Kicker, Letters, Reveal, Words, ease, sans, serif, useProgress } from "./ui";

// Les scènes se chevauchent de quelques frames pour un fondu flou continu, sans écran vide.
export const OVERLAP = 8;

type SceneProps = { start: number; dur: number };
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Frame locale d'un mot de la narration.
const cueOf = (start: number) => (phrase: string, after?: string) => f(at(phrase, after) - start);

// Entrée floue / sortie floue de chaque scène, avec une poussée de caméra très lente.
const Stage: React.FC<{ dur: number; children: React.ReactNode; push?: number }> = ({ dur, children, push = 0.035 }) => {
  const frame = useCurrentFrame();
  const total = f(dur) + OVERLAP;
  const enter = interpolate(frame, [0, 14], [0, 1], { ...clamp, easing: ease });
  const exit = interpolate(frame, [total - OVERLAP - 4, total], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  const cam = interpolate(frame, [0, total], [1, 1 + push]);
  return (
    <AbsoluteFill
      style={{
        opacity: enter * (1 - exit),
        filter: `blur(${(1 - enter) * 18 + exit * 16}px)`,
        transform: `scale(${cam * (1.04 - 0.04 * enter) * (1 - 0.02 * exit)})`,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

// Bloc qui sort en flou à `out` (changement d'idée à l'intérieur d'une scène).
const Phase: React.FC<{ out?: number; children: React.ReactNode }> = ({ out, children }) => {
  const frame = useCurrentFrame();
  const e = out === undefined ? 0 : interpolate(frame, [out, out + 10], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  if (e >= 1) return null;
  return <AbsoluteFill style={{ opacity: 1 - e, filter: `blur(${e * 14}px)`, transform: `scale(${1 + e * 0.03})` }}>{children}</AbsoluteFill>;
};

const PAD = 92;
const big = (size: number, color = C.cacao): React.CSSProperties => ({
  fontFamily: serif,
  fontStyle: "italic",
  fontWeight: 700,
  fontSize: size,
  lineHeight: 0.98,
  color,
  letterSpacing: -1,
});

// Photo dans une carte arrondie qui entre en zoom flou.
const PhotoCard: React.FC<{ src: string; cue: number; x: number; y: number; w: number; h: number; pos?: string; radius?: number }> = ({ src, cue, x, y, w, h, pos = "50% 30%", radius = 44 }) => {
  const frame = useCurrentFrame();
  const p = useProgress(cue, 24);
  const drift = interpolate(frame, [cue, cue + 400], [1.12, 1.02], clamp);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: w,
        height: h,
        borderRadius: radius,
        overflow: "hidden",
        opacity: p,
        filter: `blur(${(1 - p) * 16}px)`,
        transform: `translateY(${(1 - p) * 60}px) scale(${0.94 + 0.06 * p})`,
        boxShadow: "0 40px 80px rgba(60,35,20,0.22), 0 8px 18px rgba(60,35,20,0.1)",
      }}
    >
      <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: pos, transform: `scale(${drift})` }} />
    </div>
  );
};

// 1. ACCROCHE — le commerce en ligne depuis la RDC.
export const SceneAccroche: React.FC<SceneProps> = ({ start, dur }) => {
  const c = cueOf(start);
  const frame = useCurrentFrame();
  // « RDC » arrive en gros plan puis se pose.
  const punch = interpolate(frame, [c("RDC"), c("RDC") + 20], [0, 1], { ...clamp, easing: ease });
  const photo = useProgress(c("commerce") - 4, 30);
  return (
    <Stage dur={dur}>
      <Phase out={c("lancer") - 6}>
        <Reveal cue={c("Tu")} style={{ left: PAD, top: 560 }}>
          <Kicker size={64}>Tu es en</Kicker>
        </Reveal>
        <div
          style={{
            position: "absolute",
            left: PAD - 10,
            top: 640,
            ...big(380),
            opacity: punch,
            filter: `blur(${(1 - punch) * 24}px)`,
            transform: `scale(${1.7 - 0.7 * punch})`,
            transformOrigin: "20% 50%",
          }}
        >
          RDC
        </div>
        {[1, 2].map((k) => (
          <div
            key={k}
            style={{
              position: "absolute",
              left: PAD - 10,
              top: 640 + 250 * k * punch,
              ...big(380),
              color: "transparent",
              WebkitTextStroke: `2px ${C.cacao}`,
              opacity: punch * (0.3 - k * 0.1),
            }}
          >
            RDC
          </div>
        ))}
      </Phase>

      <Reveal cue={c("lancer")} style={{ left: PAD, top: 250 }}>
        <Kicker size={52}>et tu veux te lancer dans le</Kicker>
      </Reveal>
      <div style={{ position: "absolute", left: PAD, top: 320, ...big(150) }}>
        <Words text="Commerce" cue={c("commerce")} />
        <br />
        <Words text="en ligne" cue={c("en ligne") + 2} />
      </div>
      <Reveal cue={c("mais")} style={{ left: PAD, top: 660, width: 900 }}>
        <Body size={40} style={{ color: C.mute }}>mais comment commander tes produits</Body>
      </Reveal>
      <Reveal cue={c("l'étranger")} style={{ left: PAD, top: 720 }}>
        <div style={big(110, C.ink)}>à l'étranger ?</div>
      </Reveal>
      {/* Nature morte générée pour ce projet : colis sur piédestal, ombres de fenêtre. */}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 900,
          width: 1080,
          height: 1020,
          opacity: photo,
          transform: `translateY(${(1 - photo) * 140}px)`,
          WebkitMaskImage: "linear-gradient(180deg, transparent 0%, black 22%)",
        }}
      >
        <Img src={staticFile("img/colis_piedestal.jpg")} style={{ width: 1080, height: 1152, objectFit: "cover", objectPosition: "50% 70%" }} />
      </div>
    </Stage>
  );
};

// 2. LES OBSTACLES — fournisseur, paiements, transport, douane.
const OBSTACLES = [
  { icon: "supplier", title: "Fournisseur fiable", sub: "Trouver le bon partenaire", word: "fournisseur" },
  { icon: "payment", title: "Paiements internationaux", sub: "Régler à l'étranger", word: "paiements" },
  { icon: "transport", title: "Transport", sub: "Acheminer jusqu'en RDC", word: "transport" },
  { icon: "customs", title: "Frais de douane", sub: "Anticiper les coûts", word: "frais" },
];

export const SceneObstacles: React.FC<SceneProps> = ({ start, dur }) => {
  const c = cueOf(start);
  const frame = useCurrentFrame();
  const dim = interpolate(frame, [c("Tous"), c("Tous") + 14], [0, 1], { ...clamp, easing: ease });
  return (
    <Stage dur={dur}>
      <div style={{ opacity: 1 - dim * 0.72, filter: `blur(${dim * 5}px)`, position: "absolute", inset: 0 }}>
        <Reveal cue={0} style={{ left: PAD, top: 250 }}>
          <Kicker size={56}>Commander à l'étranger,</Kicker>
        </Reveal>
        <Reveal cue={4} style={{ left: PAD, top: 322 }}>
          <div style={big(96, C.ink)}>c'est aussi…</div>
        </Reveal>
        {OBSTACLES.map((o, i) => {
          const cue = c(o.word);
          return (
            <Reveal key={o.title} cue={cue} dx={120} dy={0} blur={18} dur={20} style={{ left: PAD, top: 520 + i * 232, width: 1080 - PAD * 2 }}>
              <Card style={{ display: "flex", alignItems: "center", gap: 34, padding: "34px 40px", transform: `rotate(${i % 2 ? 0.6 : -0.6}deg)` }}>
                <IconDot name={o.icon} />
                <div>
                  <div style={{ ...big(58, C.cacao), fontWeight: 600, lineHeight: 1.05 }}>{o.title}</div>
                  <div style={{ fontFamily: sans, fontWeight: 500, fontSize: 30, color: C.mute, marginTop: 8 }}>{o.sub}</div>
                </div>
                <div style={{ marginLeft: "auto", fontFamily: serif, fontStyle: "italic", fontSize: 44, color: C.sand }}>0{i + 1}</div>
              </Card>
            </Reveal>
          );
        })}
      </div>
      <Reveal cue={c("Tous")} style={{ left: PAD, top: 640 }}>
        <Kicker size={60}>Tous ces</Kicker>
      </Reveal>
      <div style={{ position: "absolute", left: PAD - 6, top: 720 }}>
        <Echo text="obstacles" cue={c("obstacles")} size={190} copies={2} />
      </div>
      <Reveal cue={c("freiner")} style={{ left: PAD, top: 1220, width: 900 }}>
        <Body size={46} style={{ fontWeight: 600 }}>
          peuvent <span style={{ fontFamily: serif, fontStyle: "italic", fontWeight: 700, color: C.cacao, fontSize: 64 }}>freiner</span> ton projet.
        </Body>
      </Reveal>
    </Stage>
  );
};

// 3. PRÉSENTATION — vraie photo de Samantha (dossier « Personal Identity Kit Samantha »).
const Chip: React.FC<{ cue: number; icon: string; label: string; y: number; x?: number }> = ({ cue, icon, label, y, x = PAD }) => (
  <Reveal cue={cue} dx={-80} dy={0} style={{ left: x, top: y }}>
    <div style={{ display: "flex", alignItems: "center", gap: 22, background: C.white, borderRadius: 999, padding: "18px 36px 18px 18px", boxShadow: "0 18px 40px rgba(60,35,20,0.12)" }}>
      <IconDot name={icon} size={76} />
      <div style={{ ...big(50, C.ink), fontWeight: 600, whiteSpace: "nowrap" }}>{label}</div>
    </div>
  </Reveal>
);

export const SceneSamantha: React.FC<SceneProps> = ({ start, dur }) => {
  const c = cueOf(start);
  const frame = useCurrentFrame();
  const burst = useProgress(4, 30);
  const out = c("Depuis") - 6;
  return (
    <Stage dur={dur} push={0.02}>
      <Phase out={out}>
        <div style={{ position: "absolute", left: 660, top: 700, opacity: burst, transform: `scale(${0.6 + 0.4 * burst}) rotate(${frame * 0.15}deg)` }}>
          <Burst size={480} />
        </div>
        <PhotoCard src="img/samantha_presentation.jpg" cue={0} x={190} y={190} w={700} h={980} pos="50% 30%" />
        <Reveal cue={c("Je suis")} style={{ left: PAD, top: 1230 }}>
          <Kicker size={54}>Je suis</Kicker>
        </Reveal>
        <div style={{ position: "absolute", left: PAD, top: 1296, ...big(112) }}>
          <Letters text="Samantha Mwange" cue={c("Samantha")} />
        </div>
        <Reveal cue={c("entrepreneure")} style={{ left: PAD, top: 1446 }}>
          <Body size={38} style={{ color: C.mute }}>Entrepreneure & créatrice de</Body>
        </Reveal>
        <Reveal cue={c("Woman")} style={{ left: PAD, top: 1500 }}>
          <div style={{ fontFamily: serif, fontWeight: 700, fontSize: 84, letterSpacing: 6, color: C.ink }}>WOMAN BUSINESS</div>
        </Reveal>
      </Phase>

      <Reveal cue={out + 6} style={{ left: PAD, top: 210 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 26 }}>
          <div style={{ width: 150, height: 150, borderRadius: 999, overflow: "hidden", border: `5px solid ${C.white}`, boxShadow: "0 14px 30px rgba(60,35,20,0.18)" }}>
            <Img src={staticFile("img/samantha_presentation.jpg")} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 20%", transform: "scale(1.7)", transformOrigin: "50% 26%" }} />
          </div>
          <div>
            <div style={{ ...big(46, C.ink), fontWeight: 600 }}>Samantha Mwange</div>
            <Body size={28} style={{ color: C.mute, letterSpacing: 3 }}>FONDATRICE · WOMAN BUSINESS</Body>
          </div>
        </div>
      </Reveal>
      <Reveal cue={c("Depuis")} style={{ left: PAD, top: 470 }}>
        <Kicker size={60}>Depuis plus de</Kicker>
      </Reveal>
      <div style={{ position: "absolute", left: PAD - 8, top: 540 }}>
        <Echo text="3 ans" cue={c("trois")} size={250} copies={1} gap={0.62} />
      </div>
      <Chip cue={c("dropshipping")} icon="box" label="Dropshipping" y={1010} />
      <Chip cue={c("l'intelligence")} icon="ai" label="Intelligence artificielle" y={1160} />
      <Chip cue={c("commerce", "faciliter")} icon="shop" label="Commerce en ligne · RDC" y={1310} />
    </Stage>
  );
};

// 4. WHATSAPP, OUTIL COMMERCIAL — maquette d'illustration (pas une capture réelle).
const Bubble: React.FC<{ cue: number; me?: boolean; children: React.ReactNode }> = ({ cue, me, children }) => {
  const p = useProgress(cue, 14);
  return (
    <div
      style={{
        alignSelf: me ? "flex-end" : "flex-start",
        maxWidth: "82%",
        background: me ? "#E7D8C4" : C.white,
        borderRadius: 26,
        borderBottomRightRadius: me ? 8 : 26,
        borderBottomLeftRadius: me ? 26 : 8,
        padding: "16px 22px",
        fontFamily: sans,
        fontWeight: 500,
        fontSize: 26,
        color: C.ink,
        boxShadow: "0 4px 10px rgba(60,35,20,0.08)",
        opacity: p,
        transform: `translateY(${(1 - p) * 24}px) scale(${0.9 + 0.1 * p})`,
        transformOrigin: me ? "100% 100%" : "0% 100%",
      }}
    >
      {children}
    </div>
  );
};

const Phone: React.FC<{ children: React.ReactNode; title: string }> = ({ children, title }) => (
  <div style={{ width: 500, height: 960, borderRadius: 70, background: C.ink, padding: 16, boxShadow: "0 50px 90px rgba(40,22,12,0.3)" }}>
    <div style={{ width: "100%", height: "100%", borderRadius: 56, overflow: "hidden", background: "#F3ECE2", display: "flex", flexDirection: "column" }}>
      <div style={{ height: 150, background: C.cacao, display: "flex", alignItems: "flex-end", padding: "0 26px 22px", gap: 16 }}>
        <div style={{ width: 62, height: 62, borderRadius: 999, background: C.beige, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: serif, fontWeight: 700, fontStyle: "italic", fontSize: 28, color: C.cacao }}>
          WB
        </div>
        <div>
          <div style={{ fontFamily: sans, fontWeight: 600, fontSize: 28, color: C.ivory }}>{title}</div>
          <div style={{ fontFamily: sans, fontWeight: 500, fontSize: 20, color: "rgba(247,242,234,0.7)" }}>en ligne</div>
        </div>
      </div>
      <div style={{ flex: 1, padding: 24, display: "flex", flexDirection: "column", gap: 16, justifyContent: "flex-end" }}>{children}</div>
    </div>
  </div>
);

// Un écran du téléphone, qui laisse la place au suivant en flou.
const Screen: React.FC<{ cue: number; out?: number; children: React.ReactNode }> = ({ cue, out, children }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [cue, cue + 10], [0, 1], clamp);
  const e = out === undefined ? 0 : interpolate(frame, [out, out + 8], [0, 1], clamp);
  if (p <= 0 || e >= 1) return null;
  return <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", gap: 16, justifyContent: "flex-end", opacity: p * (1 - e), filter: `blur(${e * 8}px)` }}>{children}</div>;
};

const Step: React.FC<{ cue: number; out?: number; n: string; kicker: string; title: string }> = ({ cue, out, n, kicker, title }) => (
  <>
    <Reveal cue={cue} out={out} style={{ left: PAD, top: 250 }}>
      <Kicker size={50}>{kicker}</Kicker>
    </Reveal>
    <Reveal cue={cue + 3} out={out} style={{ left: PAD, top: 316 }}>
      <div style={big(112)}>{title}</div>
    </Reveal>
    <Reveal cue={cue} out={out} style={{ right: PAD, top: 262 }}>
      <div style={{ fontFamily: serif, fontStyle: "italic", fontSize: 40, color: C.sand }}>{n}</div>
    </Reveal>
  </>
);

export const SceneWhatsApp: React.FC<SceneProps> = ({ start, dur }) => {
  const c = cueOf(start);
  const frame = useCurrentFrame();
  const phoneIn = c("Au lieu") - 4;
  const phoneOut = c("L'objectif") - 6;
  const ph = interpolate(frame, [phoneIn, phoneIn + 24], [0, 1], { ...clamp, easing: ease });
  const s1 = c("Au lieu");
  const s2 = c("apprends");
  const s3 = c("présenter");
  const s4 = c("transformer");
  const cards = useProgress(s3, 18);
  return (
    <Stage dur={dur} push={0.02}>
      {/* A. Samantha, téléphone en main. */}
      <Phase out={phoneIn - 4}>
        <Reveal cue={0} style={{ left: PAD, top: 220 }}>
          <Kicker size={54}>Apprends à mieux utiliser</Kicker>
        </Reveal>
        <Reveal cue={c("WhatsApp")} blur={20} style={{ left: PAD - 6, top: 290 }}>
          <div style={big(170)}>WhatsApp</div>
        </Reveal>
        <Reveal cue={c("vendre")} style={{ left: PAD, top: 480 }}>
          <Body size={42}>pour vendre tes produits.</Body>
        </Reveal>
        <PhotoCard src="img/samantha_telephone.jpg" cue={6} x={PAD} y={610} w={1080 - PAD * 2} h={1060} pos="50% 35%" />
      </Phase>

      {/* B. De la discussion à l'outil commercial, étape par étape. */}
      <Phase out={phoneOut}>
        <Step cue={s1} out={s2 - 6} n="01" kicker="Au lieu de seulement" title="discuter…" />
        <Step cue={s2} out={s3 - 6} n="02" kicker="apprends à" title="publier" />
        <Step cue={s3} out={s4 - 6} n="03" kicker="à mieux" title="présenter" />
        <Step cue={s4} n="04" kicker="et à" title="transformer" />
        <Reveal cue={s2 + 8} out={s3 - 6} style={{ left: PAD, top: 450 }}>
          <Body size={36} style={{ color: C.mute }}>des contenus qui suscitent l'intérêt</Body>
        </Reveal>
        <Reveal cue={s3 + 8} out={s4 - 6} style={{ left: PAD, top: 450 }}>
          <Body size={36} style={{ color: C.mute }}>tes offres, clairement</Body>
        </Reveal>
        <Reveal cue={c("l'intérêt", "transformer")} style={{ left: PAD, top: 450 }}>
          <Body size={36} style={{ color: C.mute }}>
            l'intérêt de tes contacts <span style={{ color: C.cacao, fontWeight: 700 }}>en achats</span>
          </Body>
        </Reveal>

        <div style={{ position: "absolute", left: 290, top: 600, opacity: ph, filter: `blur(${(1 - ph) * 16}px)`, transform: `translateY(${(1 - ph) * 120}px) rotate(${(1 - ph) * 4}deg)` }}>
          <Phone title="Ma boutique">
            <div style={{ position: "relative", flex: 1 }}>
              <Screen cue={s1} out={s2}>
                <Bubble cue={s1 + 6}>Coucou, ça va ?</Bubble>
                <Bubble cue={s1 + 22} me>Oui et toi ?</Bubble>
                <Bubble cue={c("proches")}>On se voit ce week-end ?</Bubble>
              </Screen>
              <Screen cue={s2} out={s3}>
                <div style={{ borderRadius: 26, overflow: "hidden", background: C.white, boxShadow: "0 8px 20px rgba(60,35,20,0.12)" }}>
                  <Img src={staticFile("img/colis_piedestal.jpg")} style={{ width: "100%", height: 330, objectFit: "cover", objectPosition: "50% 72%" }} />
                  <div style={{ padding: "16px 22px", fontFamily: sans, fontSize: 26, fontWeight: 600, color: C.ink }}>Nouveautés de la semaine</div>
                  <div style={{ padding: "0 22px 18px", fontFamily: sans, fontSize: 22, fontWeight: 500, color: C.mute }}>Découvre la sélection en photos</div>
                </div>
                <Bubble cue={c("l'intérêt")}>Ça m'intéresse !</Bubble>
              </Screen>
              <Screen cue={s3} out={s4}>
                <div style={{ background: C.white, borderRadius: 26, padding: 24, boxShadow: "0 8px 20px rgba(60,35,20,0.12)", opacity: cards, transform: `translateY(${(1 - cards) * 30}px)` }}>
                  <div style={{ fontFamily: serif, fontStyle: "italic", fontWeight: 700, fontSize: 38, color: C.cacao }}>Mon offre</div>
                  {["Description du produit", "Photos et détails", "Livraison et délais", "Comment commander"].map((l, i) => (
                    <div key={l} style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 14, opacity: useProgressLocal(frame, s3 + 8 + i * 5) }}>
                      <Icon name="check" size={30} color={C.cacao} stroke={2.4} />
                      <span style={{ fontFamily: sans, fontWeight: 500, fontSize: 25, color: C.ink }}>{l}</span>
                    </div>
                  ))}
                </div>
              </Screen>
              <Screen cue={s4}>
                <Bubble cue={s4 + 4}>Je suis intéressée. Comment commander ?</Bubble>
                <Bubble cue={c("contacts")} me>Avec plaisir ! Voici les étapes.</Bubble>
                <Reveal cue={c("achats")} dy={20} style={{ position: "relative", alignSelf: "center" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 12, background: C.cacao, color: C.ivory, borderRadius: 999, padding: "14px 26px", fontFamily: sans, fontWeight: 600, fontSize: 26 }}>
                    <Icon name="check" size={30} color={C.ivory} stroke={2.6} /> Commande confirmée
                  </div>
                </Reveal>
              </Screen>
            </div>
          </Phone>
          <div style={{ textAlign: "center", marginTop: 18, fontFamily: sans, fontSize: 22, letterSpacing: 4, color: C.mute }}>ILLUSTRATION</div>
        </div>
      </Phase>

      {/* C. L'objectif. */}
      <Reveal cue={c("L'objectif")} style={{ left: PAD, top: 520 }}>
        <Kicker size={60}>L'objectif : faire de WhatsApp</Kicker>
      </Reveal>
      <div style={{ position: "absolute", left: PAD - 6, top: 620 }}>
        <div style={big(150, C.ink)}>
          <Words text="un véritable" cue={c("véritable") - 4} />
        </div>
        <Echo text="outil commercial" cue={c("outil")} size={136} copies={2} gap={0.8} />
      </div>
      <Reveal cue={c("commercial") + 6} style={{ left: PAD, top: 1230 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 26 }}>
          <IconDot name="chat" />
          <div style={{ width: 120, height: 3, background: C.sand }} />
          <IconDot name="shop" bg={C.cacao} color={C.ivory} />
        </div>
      </Reveal>
    </Stage>
  );
};

const useProgressLocal = (frame: number, cue: number) => interpolate(frame, [cue, cue + 10], [0, 1], clamp);

// 5. INTELLIGENCE ARTIFICIELLE — chaque usage apparaît quand il est prononcé.
const USES = [
  { icon: "ai", title: "Outils d'IA utiles", word: ["outils", "découvrir"] },
  { icon: "search", title: "Produits & fournisseurs", word: ["rechercher"] },
  { icon: "video", title: "Publicités vidéo avec l'IA", word: ["créer"] },
  { icon: "shop", title: "Boutique en ligne", word: ["développer", "vidéo"] },
] as const;

export const SceneIA: React.FC<SceneProps> = ({ start, dur }) => {
  const c = cueOf(start);
  const frame = useCurrentFrame();
  const cues = USES.map((u) => c(u.word[0], u.word[1]));
  return (
    <Stage dur={dur} push={0.02}>
      <Reveal cue={c("Sur ma")} style={{ left: PAD, top: 230 }}>
        <Kicker size={54}>Sur ma chaîne WhatsApp</Kicker>
      </Reveal>
      <div style={{ position: "absolute", left: PAD - 6, top: 300, ...big(124, C.ink) }}>
        <Words text="Démonstrations" cue={c("démonstrations")} />
      </div>
      <div style={{ position: "absolute", left: PAD - 6, top: 428, ...big(124) }}>
        <Words text="pratiques" cue={c("pratiques")} />
      </div>
      {USES.map((u, i) => {
        const cue = cues[i];
        const next = cues[i + 1] ?? 9999;
        const active = interpolate(frame, [cue, cue + 10, next, next + 10], [0, 1, 1, 0], clamp);
        return (
          <Reveal key={u.title} cue={cue} dx={100} dy={0} blur={16} style={{ left: PAD, top: 680 + i * 210, width: 1080 - PAD * 2 }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 30,
                padding: "26px 34px",
                borderRadius: 34,
                background: active > 0.5 ? C.cacao : C.white,
                boxShadow: `0 ${20 + 14 * active}px ${44 + 20 * active}px rgba(60,35,20,${0.12 + 0.08 * active})`,
                transform: `scale(${1 + 0.03 * active})`,
              }}
            >
              <IconDot name={u.icon} size={100} bg={active > 0.5 ? "rgba(247,242,234,0.16)" : C.beige} color={active > 0.5 ? C.ivory : C.cacao} />
              <div style={{ ...big(52, active > 0.5 ? C.ivory : C.ink), fontWeight: 600 }}>{u.title}</div>
              <div style={{ marginLeft: "auto", fontFamily: serif, fontStyle: "italic", fontSize: 40, color: active > 0.5 ? C.sand : C.beige }}>0{i + 1}</div>
            </div>
          </Reveal>
        );
      })}
    </Stage>
  );
};

// 6. RÉALITÉS DES COMMANDES À L'ÉTRANGER — fournisseurs, paiements, transport, douane.
const ETAPES = [
  { icon: "supplier", label: "Fournisseur" },
  { icon: "payment", label: "Paiement" },
  { icon: "transport", label: "Transport" },
  { icon: "customs", label: "Douane" },
];

export const SceneCommandes: React.FC<SceneProps> = ({ start, dur }) => {
  const c = cueOf(start);
  const frame = useCurrentFrame();
  const t0 = c("étapes");
  const line = interpolate(frame, [t0, t0 + 40], [0, 1], { ...clamp, easing: ease });
  return (
    <Stage dur={dur} push={0.03}>
      <Reveal cue={0} style={{ left: PAD, top: 230 }}>
        <Kicker size={54}>Mieux comprendre les</Kicker>
      </Reveal>
      <div style={{ position: "absolute", left: PAD - 6, top: 300, ...big(128) }}>
        <Words text="étapes" cue={c("étapes")} /> <Words text="& défis" cue={c("défis")} wordStyle={() => ({ color: C.ink })} />
      </div>
      <Reveal cue={c("commandes", "défis")} style={{ left: PAD, top: 450 }}>
        <Body size={40}>des commandes à l'étranger</Body>
      </Reveal>
      <div style={{ position: "absolute", left: PAD + 54, top: 640, width: 1080 - (PAD + 54) * 2, height: 4, background: C.beige }}>
        <div style={{ width: `${line * 100}%`, height: "100%", background: C.cacao }} />
      </div>
      {ETAPES.map((e, i) => (
        <Reveal key={e.label} cue={t0 + i * 8} dy={30} scale={0.7} style={{ left: PAD + i * ((1080 - PAD * 2 - 108) / 3), top: 588, width: 108 }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
            <IconDot name={e.icon} size={108} bg={C.white} />
            <div style={{ fontFamily: sans, fontWeight: 600, fontSize: 27, color: C.ink, whiteSpace: "nowrap" }}>{e.label}</div>
          </div>
        </Reveal>
      ))}
      <PhotoCard src="img/colis_ombres.jpg" cue={6} x={PAD} y={860} w={1080 - PAD * 2} h={820} pos="50% 62%" />
    </Stage>
  );
};

// 7. TRAFIC & MONÉTISATION — TikTok, YouTube, Instagram, sans promesse de revenus.
const PLATFORMS = [
  { icon: "note", label: "TikTok", word: "TikTok" },
  { icon: "play", label: "YouTube", word: "YouTube" },
  { icon: "camera", label: "Instagram", word: "Instagram" },
];

export const SceneTrafic: React.FC<SceneProps> = ({ start, dur }) => {
  const c = cueOf(start);
  const frame = useCurrentFrame();
  const out = c("explorer") - 6;
  const draw = interpolate(frame, [c("trafic"), c("trafic") + 45], [0, 1], { ...clamp, easing: ease });
  const dot = interpolate(draw, [0.9, 1], [0, 1], clamp);
  const path = "M40 420 C 220 400, 260 300, 400 310 S 600 180, 720 170 S 860 60, 880 40";
  return (
    <Stage dur={dur} push={0.025}>
      <Phase out={out}>
        <Reveal cue={c("attirer")} style={{ left: PAD, top: 260 }}>
          <Kicker size={60}>Attirer du</Kicker>
        </Reveal>
        <div style={{ position: "absolute", left: PAD - 8, top: 330 }}>
          <Echo text="trafic" cue={c("trafic")} size={250} copies={2} gap={0.6} />
        </div>
        <Reveal cue={c("réseaux")} style={{ left: PAD, top: 780 }}>
          <Body size={44}>vers tes réseaux sociaux</Body>
        </Reveal>
        <svg width={960} height={480} viewBox="0 0 960 480" style={{ position: "absolute", left: 60, top: 930 }}>
          {[120, 240, 360].map((y) => (
            <line key={y} x1={40} x2={900} y1={y} y2={y} stroke={C.line} strokeWidth={2} />
          ))}
          <path d={path} fill="none" stroke={C.cacao} strokeWidth={10} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
          <circle cx={880} cy={40} r={22 * dot} fill={C.cacao} />
          <circle cx={880} cy={40} r={40 * dot} fill="none" stroke={C.cacao} strokeOpacity={0.3} strokeWidth={4} />
        </svg>
      </Phase>

      <Reveal cue={out + 6} style={{ left: PAD, top: 260 }}>
        <Kicker size={56}>et explorer les possibilités de</Kicker>
      </Reveal>
      <div style={{ position: "absolute", left: PAD - 6, top: 330, ...big(150) }}>
        <Words text="monétisation" cue={c("monétisation")} />
      </div>
      <Reveal cue={c("plateformes")} style={{ left: PAD, top: 530 }}>
        <Body size={40} style={{ color: C.mute }}>de plateformes comme</Body>
      </Reveal>
      {PLATFORMS.map((p, i) => (
        <Reveal key={p.label} cue={c(p.word)} dy={60} blur={16} style={{ left: PAD + i * 306, top: 700 }}>
          <Card style={{ width: 284, height: 340, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 30 }}>
            <IconDot name={p.icon} size={130} bg={i === 1 ? C.cacao : C.beige} color={i === 1 ? C.ivory : C.cacao} />
            <div style={{ ...big(48, C.ink), fontWeight: 600 }}>{p.label}</div>
          </Card>
        </Reveal>
      ))}
      <Reveal cue={c("Instagram") + 14} style={{ left: PAD, top: 1130, width: 1080 - PAD * 2 }}>
        <Body size={30} style={{ color: C.mute, textAlign: "center" }}>Des possibilités à explorer, sans revenus garantis.</Body>
      </Reveal>
    </Stage>
  );
};

// 8. APPEL À L'ACTION — la chaîne WhatsApp WOMAN BUSINESS, gratuite.
// Lien réel de la chaîne : à renseigner quand il sera fourni (aucun lien inventé).
export const LIEN_WHATSAPP: string | null = null;

export const SceneCTA: React.FC<SceneProps> = ({ start, dur }) => {
  const c = cueOf(start);
  const frame = useCurrentFrame();
  const out = c("Rejoins") - 6;
  const bounce = Math.max(0, Math.sin((frame - c("lien")) / 6)) * 14 * (frame > c("lien") ? 1 : 0);
  return (
    <Stage dur={dur} push={0.015}>
      <Phase out={out}>
        <Reveal cue={c("Tu veux apprendre")} style={{ left: PAD, top: 420 }}>
          <Kicker size={58}>Tu veux apprendre à utiliser</Kicker>
        </Reveal>
        <div style={{ position: "absolute", left: PAD - 8, top: 500 }}>
          <Echo text="l'IA" cue={c("l'IA", "Tu veux apprendre")} size={300} copies={1} gap={0.55} />
        </div>
        <Reveal cue={c("développer", "Tu veux apprendre")} style={{ left: PAD, top: 900, width: 900 }}>
          <Body size={46}>pour développer ton activité commerciale,</Body>
        </Reveal>
        <Reveal cue={c("même")} style={{ left: PAD, top: 1040 }}>
          <div style={big(110)}>même depuis<br />la RDC ?</div>
        </Reveal>
      </Phase>

      {/* Écran final : il reste affiché jusqu'à la fin pour laisser le temps de lire. */}
      <Reveal cue={out + 4} scale={0.8} style={{ left: (1080 - 260) / 2, top: 150 }}>
        <div style={{ position: "relative", width: 260, height: 260 }}>
          <Burst size={330} color={C.beige} rotate={frame * 0.2} style={{ position: "absolute", left: -35, top: -35 }} />
          <div style={{ position: "absolute", inset: 0, borderRadius: 999, overflow: "hidden", border: `6px solid ${C.white}`, boxShadow: "0 20px 40px rgba(60,35,20,0.2)" }}>
            <Img src={staticFile("img/samantha_portrait.jpg")} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 22%" }} />
          </div>
        </div>
      </Reveal>
      <Reveal cue={c("Rejoins")} style={{ left: 0, top: 460, width: 1080 }}>
        <Kicker size={58} style={{ textAlign: "center" }}>
          Rejoins <span style={{ fontWeight: 700, color: C.cacao }}>gratuitement</span> la chaîne
        </Kicker>
      </Reveal>
      <Reveal cue={c("WhatsApp", "Rejoins")} style={{ left: 0, top: 545, width: 1080, display: "flex", justifyContent: "center" }}>
        <div style={{ fontFamily: sans, fontWeight: 600, fontSize: 30, letterSpacing: 6, color: C.ink, border: `2px solid ${C.ink}`, borderRadius: 999, padding: "10px 30px" }}>WHATSAPP</div>
      </Reveal>
      <div style={{ position: "absolute", left: 0, top: 640, width: 1080, textAlign: "center", fontFamily: serif, fontWeight: 700, fontSize: 132, lineHeight: 1, letterSpacing: 4, color: C.ink }}>
        <Letters text="WOMAN" cue={c("Woman", "Rejoins")} stagger={2} />
        <br />
        <Letters text="BUSINESS" cue={c("Business", "Rejoins") - 2} stagger={2} style={{ color: C.cacao }} />
      </div>
      <Reveal cue={c("cliquant")} scale={0.85} style={{ left: 0, top: 960, width: 1080, display: "flex", justifyContent: "center" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, background: C.cacao, color: C.ivory, borderRadius: 999, padding: "30px 56px", fontFamily: sans, fontWeight: 600, fontSize: 44, boxShadow: "0 24px 50px rgba(107,54,34,0.35)" }}>
          Rejoindre la chaîne
          <span style={{ display: "inline-flex", transform: `translateY(${bounce}px)` }}>
            <Icon name="arrowDown" size={48} color={C.ivory} stroke={2.4} />
          </span>
        </div>
      </Reveal>
      {/* Emplacement réservé au lien ou au QR code. */}
      <Reveal cue={c("lien")} style={{ left: PAD + 60, top: 1140, width: 1080 - (PAD + 60) * 2 }}>
        <div style={{ border: `3px dashed ${C.sand}`, borderRadius: 30, padding: "26px 20px", textAlign: "center", background: "rgba(255,255,255,0.55)" }}>
          <div style={{ fontFamily: sans, fontWeight: 600, fontSize: 40, color: C.ink }}>{LIEN_WHATSAPP ?? "Lien ci-dessous"}</div>
          <div style={{ fontFamily: sans, fontWeight: 500, fontSize: 26, color: C.mute, marginTop: 6 }}>Accès gratuit à la chaîne</div>
        </div>
      </Reveal>
      <div style={{ position: "absolute", left: 0, top: 1380, width: 1080, display: "flex", justifyContent: "center", gap: 14 }}>
        {[
          { t: "des outils", w: "outils" },
          { t: "des démonstrations", w: "démonstrations" },
          { t: "des opportunités", w: "opportunités" },
        ].map((x, i) => (
          <Reveal key={x.t} cue={c(x.w, "ci-dessous")} dy={24} style={{ position: "relative" }}>
            <div style={{ fontFamily: serif, fontStyle: "italic", fontWeight: 600, fontSize: 35, color: i === 1 ? C.cacao : C.ink, background: C.white, borderRadius: 999, padding: "12px 24px", boxShadow: "0 10px 24px rgba(60,35,20,0.1)", whiteSpace: "nowrap" }}>
              {x.t}
            </div>
          </Reveal>
        ))}
      </div>
      <Reveal cue={c("entreprendre")} style={{ left: 0, top: 1490, width: 1080 }}>
        <Kicker size={50} style={{ textAlign: "center" }}>
          pour entreprendre autrement grâce à l'IA
        </Kicker>
      </Reveal>
    </Stage>
  );
};
