import React from "react";
import { continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

// Poppins (SIL OFL 1.1) embarquée dans public/fonts pour un rendu sans dépendance réseau.
export const fontFamily = "Poppins";
const fontHandle = delayRender("Chargement de Poppins");
Promise.all(
  [500, 600, 700, 800, 900].map((w) =>
    new FontFace(fontFamily, `url(${staticFile(`fonts/Poppins-${w}.ttf`)})`, { weight: String(w) })
      .load()
      .then((face) => document.fonts.add(face)),
  ),
).then(() => continueRender(fontHandle));

export const C = {
  sky: "#BFE5FB",
  skyDeep: "#8FD0F5",
  navy: "#0B2545",
  ink: "#13315C",
  mute: "rgba(11,37,69,0.28)",
  orange: "#FF8A1F",
  yellow: "#FFC93C",
  green: "#1FB45A",
  whatsapp: "#25D366",
  red: "#E5484D",
  white: "#FFFFFF",
};

// Progression d'apparition (0 → 1) déclenchée à `cue` (frame locale).
export const usePop = (cue: number, damping = 14, mass = 0.7) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - cue, fps, config: { damping, mass, stiffness: 160 } });
};

export const Pop: React.FC<{
  cue: number;
  children: React.ReactNode;
  from?: "up" | "down" | "left" | "right" | "scale";
  damping?: number;
  style?: React.CSSProperties;
}> = ({ cue, children, from = "up", damping, style }) => {
  const p = usePop(cue, damping);
  const d = 60 * (1 - p);
  const tr =
    from === "up" ? `translateY(${d}px)` :
    from === "down" ? `translateY(${-d}px)` :
    from === "left" ? `translateX(${-d * 1.5}px)` :
    from === "right" ? `translateX(${d * 1.5}px)` : "";
  const scale = from === "scale" ? 0.6 + 0.4 * p : 0.92 + 0.08 * p;
  return (
    <div style={{ opacity: Math.min(1, p * 1.4), transform: `${tr} scale(${scale})`, ...style }}>
      {children}
    </div>
  );
};

export const Card: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => (
  <div
    style={{
      background: C.white,
      borderRadius: 36,
      boxShadow: "0 18px 40px rgba(11,37,69,0.14), 0 2px 0 rgba(11,37,69,0.05)",
      padding: 32,
      ...style,
    }}
  >
    {children}
  </div>
);

export const Pill: React.FC<{ children: React.ReactNode; bg?: string; color?: string; style?: React.CSSProperties }> = ({
  children, bg = C.navy, color = C.white, style,
}) => (
  <div
    style={{
      display: "inline-flex", alignItems: "center", gap: 12, background: bg, color,
      borderRadius: 999, padding: "12px 28px", fontWeight: 800, fontSize: 34, letterSpacing: 1,
      ...style,
    }}
  >
    {children}
  </div>
);

// Coche animée : le tracé se dessine à partir de `cue`.
export const Check: React.FC<{ cue: number; size?: number; color?: string }> = ({ cue, size = 64, color = C.green }) => {
  const p = usePop(cue, 12);
  const draw = interpolate(p, [0, 1], [30, 0], { extrapolateRight: "clamp" });
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" style={{ transform: `scale(${0.5 + 0.5 * p})`, opacity: p > 0.01 ? 1 : 0.15 }}>
      <circle cx="32" cy="32" r="30" fill={p > 0.01 ? color : "#D9E6F2"} />
      <path d="M19 33 l9 9 l17 -19" fill="none" stroke="#fff" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round"
        strokeDasharray="30" strokeDashoffset={draw} />
    </svg>
  );
};

type IconProps = { size?: number; color?: string };
const S: React.FC<IconProps & { children: React.ReactNode }> = ({ size = 72, children }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none" strokeLinecap="round" strokeLinejoin="round">{children}</svg>
);

export const Icon = {
  play: ({ size, color = C.white }: IconProps) => (
    <S size={size}><path d="M17 12 L36 24 L17 36 Z" fill={color} /></S>
  ),
  warning: ({ size, color = C.orange }: IconProps) => (
    <S size={size}>
      <path d="M24 6 L44 40 H4 Z" fill={color} />
      <path d="M24 18 V28" stroke="#fff" strokeWidth="4.5" />
      <circle cx="24" cy="34" r="2.6" fill="#fff" />
    </S>
  ),
  loop: ({ size, color = C.navy }: IconProps) => (
    <S size={size}>
      <path d="M38 18 A15 15 0 0 0 11 15" stroke={color} strokeWidth="4.5" />
      <path d="M10 30 A15 15 0 0 0 37 33" stroke={color} strokeWidth="4.5" />
      <path d="M11 7 V15 H19" stroke={color} strokeWidth="4.5" />
      <path d="M37 41 V33 H29" stroke={color} strokeWidth="4.5" />
    </S>
  ),
  cursor: ({ size, color = C.navy }: IconProps) => (
    <S size={size}>
      <path d="M12 6 L36 26 L25 27 L31 40 L26 42 L20 29 L12 36 Z" fill={color} />
    </S>
  ),
  globe: ({ size, color = C.navy }: IconProps) => (
    <S size={size}>
      <circle cx="24" cy="24" r="17" stroke={color} strokeWidth="4" />
      <path d="M7 24 H41 M24 7 C15 16 15 32 24 41 C33 32 33 16 24 7" stroke={color} strokeWidth="3.5" />
    </S>
  ),
  pin: ({ size, color = C.red }: IconProps) => (
    <S size={size}>
      <path d="M24 44 C24 44 9 29 9 19 A15 15 0 0 1 39 19 C39 29 24 44 24 44 Z" fill={color} />
      <circle cx="24" cy="19" r="6" fill="#fff" />
    </S>
  ),
  copy: ({ size, color = C.navy }: IconProps) => (
    <S size={size}>
      <rect x="15" y="14" width="22" height="27" rx="4" stroke={color} strokeWidth="4" />
      <path d="M11 33 V10 A3 3 0 0 1 14 7 H30" stroke={color} strokeWidth="4" />
    </S>
  ),
  shield: ({ size, color = C.green }: IconProps) => (
    <S size={size}>
      <path d="M24 5 L40 11 V23 C40 33 33 40 24 43 C15 40 8 33 8 23 V11 Z" fill={color} />
      <path d="M16 24 l6 6 l11 -12" stroke="#fff" strokeWidth="4.5" />
    </S>
  ),
  note: ({ size, color = C.navy }: IconProps) => (
    <S size={size}>
      <rect x="9" y="6" width="30" height="36" rx="5" stroke={color} strokeWidth="4" />
      <path d="M16 17 H32 M16 25 H32 M16 33 H25" stroke={color} strokeWidth="4" />
    </S>
  ),
  doc: ({ size, color = C.navy }: IconProps) => (
    <S size={size}>
      <path d="M12 5 H29 L37 13 V43 H12 Z" stroke={color} strokeWidth="4" />
      <path d="M29 5 V13 H37" stroke={color} strokeWidth="4" />
      <path d="M18 23 H31 M18 30 H31 M18 37 H26" stroke={color} strokeWidth="3.5" />
    </S>
  ),
  flag: ({ size, color = C.navy }: IconProps) => (
    <S size={size}>
      <path d="M11 43 V6" stroke={color} strokeWidth="4" />
      <path d="M11 8 H37 L31 16 L37 24 H11" fill={C.skyDeep} stroke={color} strokeWidth="3.5" />
    </S>
  ),
  user: ({ size, color = C.navy }: IconProps) => (
    <S size={size}>
      <circle cx="24" cy="16" r="8" stroke={color} strokeWidth="4" />
      <path d="M9 42 C9 32 16 28 24 28 C32 28 39 32 39 42" stroke={color} strokeWidth="4" />
    </S>
  ),
  briefcase: ({ size, color = C.navy }: IconProps) => (
    <S size={size}>
      <rect x="6" y="15" width="36" height="25" rx="5" stroke={color} strokeWidth="4" />
      <path d="M17 15 V10 H31 V15 M6 26 H42" stroke={color} strokeWidth="4" />
    </S>
  ),
  question: ({ size, color = C.orange }: IconProps) => (
    <S size={size}>
      <circle cx="24" cy="24" r="20" fill={color} />
      <path d="M18 19 A6 6 0 1 1 26 24.5 C24.5 25.3 24 26.5 24 28.5" stroke="#fff" strokeWidth="4.5" />
      <circle cx="24" cy="35" r="2.6" fill="#fff" />
    </S>
  ),
  lockClosed: ({ size, color = C.navy }: IconProps) => (
    <S size={size}>
      <rect x="9" y="21" width="30" height="22" rx="5" fill={color} />
      <path d="M15 21 V15 A9 9 0 0 1 33 15 V21" stroke={color} strokeWidth="4.5" />
    </S>
  ),
  lockOpen: ({ size, color = C.green }: IconProps) => (
    <S size={size}>
      <rect x="9" y="21" width="30" height="22" rx="5" fill={color} />
      <path d="M15 21 V15 A9 9 0 0 1 32 11" stroke={color} strokeWidth="4.5" />
    </S>
  ),
  chat: ({ size, color = C.white }: IconProps) => (
    <S size={size}>
      <path d="M24 6 A18 18 0 0 0 8.5 33 L6 42 L15.5 39.5 A18 18 0 1 0 24 6 Z" stroke={color} strokeWidth="3.8" />
      <path d="M17 17 C17 26 22 31 31 31 L33 27 L28 25 L26 27 C23 26 22 25 21 22 L23 20 L21 15 Z" fill={color} />
    </S>
  ),
  arrowDown: ({ size, color = C.navy }: IconProps) => (
    <S size={size}><path d="M24 8 V38 M12 27 L24 39 L36 27" stroke={color} strokeWidth="5" /></S>
  ),
};
