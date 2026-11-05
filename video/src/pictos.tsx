// Pictogrammes et petits utilitaires partagés par les vidéos (mêmes conventions que ui.tsx).
import React from "react";
import { useCurrentFrame } from "remotion";
import { C } from "./ui";

export const RED = "#FF4D4F";
export const DARK = "#081A33";

// Pictogrammes vectoriels, couleur et taille paramétrables.
const G: React.FC<{ size?: number; children: React.ReactNode }> = ({ size = 72, children }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none" strokeLinecap="round" strokeLinejoin="round">{children}</svg>
);
export const Pic = {
  box: (c = C.yellow, s?: number) => (
    <G size={s}><path d="M24 5 L42 14 V34 L24 43 L6 34 V14 Z" fill={c} /><path d="M6 14 L24 23 L42 14 M24 23 V43" stroke={DARK} strokeWidth="3" /></G>
  ),
  home: (c = C.white, s?: number) => (
    <G size={s}><path d="M6 22 L24 7 L42 22" stroke={c} strokeWidth="4" /><path d="M11 19 V41 H37 V19" stroke={c} strokeWidth="4" /></G>
  ),
  factory: (c = C.white, s?: number) => (
    <G size={s}><path d="M5 42 V20 L16 27 V20 L27 27 V10 H37 V42 Z" stroke={c} strokeWidth="3.5" /><path d="M13 35 H17 M23 35 H27 M32 35 H34" stroke={c} strokeWidth="3.5" /></G>
  ),
  truck: (c = C.white, s?: number) => (
    <G size={s}><path d="M4 12 H29 V34 H4 Z M29 20 H38 L44 27 V34 H29" stroke={c} strokeWidth="3.5" /><circle cx="13" cy="36" r="4" fill={c} /><circle cx="36" cy="36" r="4" fill={c} /></G>
  ),
  user: (c = C.white, s?: number) => (
    <G size={s}><circle cx="24" cy="15" r="8" stroke={c} strokeWidth="4" /><path d="M8 42 C8 31 15 27 24 27 C33 27 40 31 40 42" stroke={c} strokeWidth="4" /></G>
  ),
  star: (c = C.white, s?: number) => (
    <G size={s}><path d="M24 5 L29.5 17.5 L43 18.6 L32.8 27.4 L35.9 40.6 L24 33.6 L12.1 40.6 L15.2 27.4 L5 18.6 L18.5 17.5 Z" stroke={c} strokeWidth="3.5" /></G>
  ),
  store: (c = C.white, s?: number) => (
    <G size={s}><path d="M6 18 L10 7 H38 L42 18 Z" stroke={c} strokeWidth="3.5" /><path d="M9 18 V41 H39 V18 M19 41 V29 H29 V41" stroke={c} strokeWidth="3.5" /></G>
  ),
  clock: (c = C.white, s?: number) => (
    <G size={s}><circle cx="24" cy="24" r="18" stroke={c} strokeWidth="4" /><path d="M24 13 V24 L31 29" stroke={c} strokeWidth="4" /></G>
  ),
  phone: (c = C.white, s?: number) => (
    <G size={s}><rect x="14" y="5" width="20" height="38" rx="4" stroke={c} strokeWidth="3.5" /><path d="M21 37 H27" stroke={c} strokeWidth="3.5" /></G>
  ),
  ban: (c = RED, s?: number) => (
    <G size={s}><circle cx="24" cy="24" r="18" stroke={c} strokeWidth="4.5" /><path d="M11.5 11.5 L36.5 36.5" stroke={c} strokeWidth="4.5" /></G>
  ),
  swap: (c = C.white, s?: number) => (
    <G size={s}><path d="M8 16 H38 L31 9 M40 32 H10 L17 39" stroke={c} strokeWidth="4" /></G>
  ),
  money: (c = C.white, s?: number) => (
    <G size={s}><rect x="4" y="13" width="40" height="22" rx="4" stroke={c} strokeWidth="3.5" /><circle cx="24" cy="24" r="5" stroke={c} strokeWidth="3.5" /></G>
  ),
  fan: (c = C.white, s?: number) => (
    <G size={s}><circle cx="24" cy="19" r="14" stroke={c} strokeWidth="3.5" /><path d="M24 19 C24 11 30 9 31 13 C32 17 26 19 24 19 Z M24 19 C30 23 29 29 25 28 C21 27 22 21 24 19 Z M24 19 C17 22 13 18 16 15 C19 12 23 16 24 19 Z" fill={c} /><path d="M24 33 V41 M16 43 H32" stroke={c} strokeWidth="3.5" /></G>
  ),
  camera: (c = C.white, s?: number) => (
    <G size={s}><path d="M6 16 H14 L18 10 H30 L34 16 H42 V38 H6 Z" stroke={c} strokeWidth="3.5" /><circle cx="24" cy="26" r="7" stroke={c} strokeWidth="3.5" /></G>
  ),
  search: (c = C.white, s?: number) => (
    <G size={s}><circle cx="21" cy="21" r="12" stroke={c} strokeWidth="4" /><path d="M30 30 L41 41" stroke={c} strokeWidth="4.5" /></G>
  ),
  cart: (c = C.white, s?: number) => (
    <G size={s}><path d="M4 8 H10 L15 32 H38 L42 15 H12" stroke={c} strokeWidth="3.5" /><circle cx="18" cy="39" r="3" fill={c} /><circle cx="35" cy="39" r="3" fill={c} /></G>
  ),
  map: (c = C.white, s?: number) => (
    <G size={s}><path d="M5 11 L17 6 L31 11 L43 6 V37 L31 42 L17 37 L5 42 Z M17 6 V37 M31 11 V42" stroke={c} strokeWidth="3.2" /></G>
  ),
  chats: (c = C.white, s?: number) => (
    <G size={s}><path d="M5 8 H31 V26 H15 L8 32 V26 H5 Z" stroke={c} strokeWidth="3.2" /><path d="M35 16 H43 V34 H40 V40 L33 34 H19 V30" stroke={c} strokeWidth="3.2" /></G>
  ),
  plus: (c = C.white, s?: number) => (
    <G size={s}><path d="M24 8 V40 M8 24 H40" stroke={c} strokeWidth="5" /></G>
  ),
};

// Tremblement bref à l'apparition d'un élément.
export const useShake = (cue: number, amp = 12, len = 10) => {
  const frame = useCurrentFrame();
  const d = frame - cue;
  return d >= 0 && d < len ? Math.sin(d * 2.2) * amp * (1 - d / len) : 0;
};

