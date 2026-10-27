import React from "react";
import { AbsoluteFill, Easing, Img, continueRender, delayRender, interpolate, staticFile, useCurrentFrame } from "remotion";

// Polices embarquées dans public/fonts (SIL OFL 1.1) pour un rendu sans dépendance réseau.
export const serif = "Playfair";
export const sans = "Poppins";
const fontHandle = delayRender("Chargement des polices");
Promise.all([
  ...[500, 600, 700].map((w) => new FontFace(sans, `url(${staticFile(`fonts/Poppins-${w}.ttf`)})`, { weight: String(w) })),
  ...[400, 600, 700].flatMap((w) =>
    (["normal", "italic"] as const).map(
      (s) => new FontFace(serif, `url(${staticFile(`fonts/playfair-display-latin-${w}-${s}.woff2`)})`, { weight: String(w), style: s }),
    ),
  ),
].map((face) => face.load().then((loaded) => document.fonts.add(loaded)))).then(() => continueRender(fontHandle));

// Palette WOMAN BUSINESS : ivoire, beige, brun cacao, noir doux.
export const C = {
  ivory: "#F7F2EA",
  paper: "#FBF8F3",
  beige: "#E9DCCA",
  sand: "#D6C2A8",
  cacao: "#6B3622",
  rust: "#8C4126",
  ink: "#231B17",
  mute: "#857769",
  line: "rgba(35,27,23,0.12)",
  white: "#FFFFFF",
};

export const ease = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Progression 0 → 1 à partir de la frame locale `cue`.
export const useProgress = (cue: number, dur = 18) => {
  const frame = useCurrentFrame();
  return interpolate(frame, [cue, cue + dur], [0, 1], { ...clamp, easing: ease });
};

// Apparition floue → nette, avec léger glissement (langage de la vidéo de référence).
export const Reveal: React.FC<{
  cue: number;
  out?: number;
  dur?: number;
  dx?: number;
  dy?: number;
  blur?: number;
  scale?: number;
  style?: React.CSSProperties;
  children: React.ReactNode;
}> = ({ cue, out, dur = 18, dx = 0, dy = 34, blur = 14, scale = 1, style, children }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [cue, cue + dur], [0, 1], { ...clamp, easing: ease });
  const e = out === undefined ? 0 : interpolate(frame, [out, out + 12], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  const s = scale + (1 - scale) * p;
  return (
    <div
      style={{
        position: "absolute",
        opacity: p * (1 - e),
        filter: `blur(${(1 - p) * blur + e * 12}px)`,
        transform: `translate(${dx * (1 - p)}px, ${dy * (1 - p) - e * 24}px) scale(${s})`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

// Mots qui apparaissent l'un après l'autre.
export const Words: React.FC<{ text: string; cue: number; stagger?: number; style?: React.CSSProperties; wordStyle?: (i: number) => React.CSSProperties }> = ({
  text,
  cue,
  stagger = 3,
  style,
  wordStyle,
}) => {
  const frame = useCurrentFrame();
  return (
    <span style={style}>
      {text.split(" ").map((w, i) => {
        const p = interpolate(frame, [cue + i * stagger, cue + i * stagger + 16], [0, 1], { ...clamp, easing: ease });
        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              opacity: p,
              filter: `blur(${(1 - p) * 10}px)`,
              transform: `translateY(${(1 - p) * 26}px)`,
              marginRight: "0.26em",
              ...(wordStyle ? wordStyle(i) : {}),
            }}
          >
            {w}
          </span>
        );
      })}
    </span>
  );
};

// Lettres posées une à une avec une légère rotation (comme « Cup » dans la référence).
export const Letters: React.FC<{ text: string; cue: number; stagger?: number; style?: React.CSSProperties }> = ({ text, cue, stagger = 1.6, style }) => {
  const frame = useCurrentFrame();
  return (
    <span style={{ whiteSpace: "pre", ...style }}>
      {text.split("").map((ch, i) => {
        const c = cue + i * stagger;
        const p = interpolate(frame, [c, c + 14], [0, 1], { ...clamp, easing: ease });
        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              opacity: p,
              transform: `translateY(${(1 - p) * 40}px) rotate(${(1 - p) * -14}deg)`,
              filter: `blur(${(1 - p) * 6}px)`,
            }}
          >
            {ch}
          </span>
        );
      })}
    </span>
  );
};

// Titre serif avec ses échos en contour, décalés vers le bas (« Emotions / Emotions / Emotions »).
export const Echo: React.FC<{ text: string; cue: number; size: number; color?: string; copies?: number; gap?: number; style?: React.CSSProperties }> = ({
  text,
  cue,
  size,
  color = C.cacao,
  copies = 2,
  gap = 0.78,
  style,
}) => {
  const frame = useCurrentFrame();
  const base: React.CSSProperties = { fontFamily: serif, fontStyle: "italic", fontWeight: 700, fontSize: size, lineHeight: 1, whiteSpace: "nowrap" };
  return (
    <div style={{ position: "relative", ...style }}>
      {Array.from({ length: copies }).map((_, k) => {
        const c = cue + 6 + k * 5;
        const p = interpolate(frame, [c, c + 22], [0, 1], { ...clamp, easing: ease });
        return (
          <div
            key={k}
            style={{
              ...base,
              position: "absolute",
              left: 0,
              top: size * gap * (k + 1) * p,
              color: "transparent",
              WebkitTextStroke: `2px ${color}`,
              opacity: p * (0.32 - k * 0.12),
            }}
          >
            {text}
          </div>
        );
      })}
      <div style={{ ...base, position: "relative", color }}>
        <Words text={text} cue={cue} stagger={4} />
      </div>
    </div>
  );
};

export const Kicker: React.FC<{ children: React.ReactNode; size?: number; style?: React.CSSProperties }> = ({ children, size = 50, style }) => (
  <div style={{ fontFamily: serif, fontStyle: "italic", fontWeight: 400, fontSize: size, color: C.ink, lineHeight: 1.15, ...style }}>{children}</div>
);

export const Body: React.FC<{ children: React.ReactNode; size?: number; style?: React.CSSProperties }> = ({ children, size = 38, style }) => (
  <div style={{ fontFamily: sans, fontWeight: 500, fontSize: size, color: C.ink, lineHeight: 1.3, ...style }}>{children}</div>
);

// Fond ivoire, grille très légère et ombre de fenêtre qui dérive lentement.
export const Backdrop: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: `radial-gradient(120% 80% at 30% 20%, ${C.paper} 0%, ${C.ivory} 55%, #EFE6DA 100%)` }}>
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(${C.line} 1px, transparent 1px), linear-gradient(90deg, ${C.line} 1px, transparent 1px)`,
          backgroundSize: "120px 120px",
          opacity: 0.35,
        }}
      />
    </AbsoluteFill>
  );
};

export const WindowShadow: React.FC<{ opacity?: number }> = ({ opacity = 0.5 }) => {
  const frame = useCurrentFrame();
  const drift = Math.sin(frame / 160) * 40 + frame * 0.08;
  return (
    <AbsoluteFill style={{ mixBlendMode: "multiply", opacity, pointerEvents: "none" }}>
      <Img
        src={staticFile("img/ombre_fenetre.png")}
        style={{ position: "absolute", left: -360 + drift, top: -440 - drift * 0.4, width: 1800, height: 2800 }}
      />
    </AbsoluteFill>
  );
};

// Carte blanche arrondie, ombre douce.
export const Card: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => (
  <div
    style={{
      background: C.white,
      borderRadius: 36,
      boxShadow: "0 30px 60px rgba(60,35,20,0.16), 0 6px 14px rgba(60,35,20,0.08)",
      ...style,
    }}
  >
    {children}
  </div>
);

// Éclat cacao derrière les photos (forme de la référence, redessinée).
export const Burst: React.FC<{ size: number; color?: string; rotate?: number; style?: React.CSSProperties }> = ({ size, color = C.cacao, rotate = 0, style }) => {
  const pts: string[] = [];
  const n = 7;
  for (let i = 0; i < n * 2; i++) {
    const r = i % 2 === 0 ? 50 : 14;
    const a = (Math.PI * i) / n;
    pts.push(`${50 + r * Math.cos(a)},${50 + r * Math.sin(a)}`);
  }
  return (
    <svg viewBox="0 0 100 100" width={size} height={size} style={{ transform: `rotate(${rotate}deg)`, ...style }}>
      <polygon points={pts.join(" ")} fill={color} />
    </svg>
  );
};

// Pictogrammes au trait (dessinés pour ce projet).
const P: Record<string, React.ReactNode> = {
  supplier: (
    <>
      <path d="M3 10l2-6h14l2 6" />
      <path d="M3 10h18v2a3 3 0 01-6 0 3 3 0 01-6 0 3 3 0 01-6 0z" />
      <path d="M5 13v7h14v-7M10 20v-4h4v4" />
    </>
  ),
  payment: (
    <>
      <rect x="2.5" y="5" width="19" height="14" rx="2.5" />
      <path d="M2.5 10h19M6.5 15h4" />
    </>
  ),
  transport: (
    <>
      <path d="M2 13l20-8-6 15-4-5-5 3 1-5z" />
      <path d="M12 15l10-10" />
    </>
  ),
  customs: (
    <>
      <path d="M6 2.5h9l4 4V21.5H6z" />
      <path d="M15 2.5v4h4M9 11h7M9 15h7M9 18.5h4" />
    </>
  ),
  ai: (
    <>
      <path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z" />
      <path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z" />
    </>
  ),
  search: (
    <>
      <circle cx="10.5" cy="10.5" r="6.5" />
      <path d="M15.5 15.5L21 21" />
    </>
  ),
  video: (
    <>
      <rect x="2.5" y="5.5" width="13" height="13" rx="2.5" />
      <path d="M15.5 10l6-3.5v11l-6-3.5" />
    </>
  ),
  shop: (
    <>
      <path d="M5 7h14l-1.2 13.5H6.2z" />
      <path d="M9 9V6a3 3 0 016 0v3" />
    </>
  ),
  chat: (
    <>
      <path d="M4 5h16v11H9l-5 4z" />
    </>
  ),
  play: (
    <>
      <rect x="2.5" y="5" width="19" height="14" rx="4" />
      <path d="M10 9v6l5-3z" />
    </>
  ),
  note: (
    <>
      <path d="M14 3v11.5a3.5 3.5 0 11-2-3.2V3h2z" />
      <path d="M14 3c0 3 2.5 5 5.5 5" />
    </>
  ),
  camera: (
    <>
      <rect x="3" y="3" width="18" height="18" rx="5" />
      <circle cx="12" cy="12" r="4.2" />
      <circle cx="17.3" cy="6.7" r="0.6" />
    </>
  ),
  check: <path d="M4.5 12.5l5 5 10-11" />,
  arrowDown: <path d="M12 4v15M6 13l6 6 6-6" />,
  box: (
    <>
      <path d="M3 7.5L12 3l9 4.5v9L12 21l-9-4.5z" />
      <path d="M3 7.5L12 12l9-4.5M12 12v9" />
    </>
  ),
};

export const Icon: React.FC<{ name: keyof typeof P | string; size?: number; color?: string; stroke?: number }> = ({ name, size = 56, color = C.cacao, stroke = 1.6 }) => (
  <svg viewBox="0 0 24 24" width={size} height={size} fill="none" stroke={color} strokeWidth={stroke} strokeLinecap="round" strokeLinejoin="round">
    {P[name]}
  </svg>
);

// Pastille ronde beige qui porte une icône.
export const IconDot: React.FC<{ name: string; size?: number; bg?: string; color?: string }> = ({ name, size = 108, bg = C.beige, color = C.cacao }) => (
  <div style={{ width: size, height: size, borderRadius: 999, background: bg, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
    <Icon name={name} size={size * 0.5} color={color} />
  </div>
);
