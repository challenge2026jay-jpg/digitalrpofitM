import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { WORDS, Word, norm } from "./timing";
import { C, fontFamily } from "./ui";

// Mots mis en avant (surlignage), repris tels quels de la narration.
const DEFAULT_KEYWORDS = new Set(
  ["grâce", "dropshipping", "bloque", "nulle", "doute", "pays", "rdc", "vérifier", "note",
   "documentation", "officielle", "compte", "confirmation", "payer", "capable", "whatsapp", "bio"].map(norm),
);

type Chunk = { words: Word[]; start: number; end: number };

// Découpe la narration en lignes courtes, lisibles sur téléphone.
const buildChunks = (words: Word[]): Chunk[] => {
  const chunks: Chunk[] = [];
  let cur: Word[] = [];
  const push = () => {
    if (cur.length) chunks.push({ words: cur, start: cur[0].start, end: cur[cur.length - 1].end });
    cur = [];
  };
  for (const w of words) {
    cur.push(w);
    const endsSentence = /[.!?…]$/.test(w.text);
    const comma = /,$/.test(w.text);
    if (endsSentence || cur.length >= 6 || (comma && cur.length >= 3)) push();
  }
  push();
  return chunks;
};

const chunkCache = new WeakMap<Word[], Chunk[]>();
const chunksOf = (words: Word[]) => {
  if (!chunkCache.has(words)) chunkCache.set(words, buildChunks(words));
  return chunkCache.get(words)!;
};

export type CaptionTheme = { text: string; mute: string; hlBg: string; hlText: string; hlShadow: string; riskBg: string };
const LIGHT: CaptionTheme = { text: C.navy, mute: C.mute, hlBg: C.yellow, hlText: C.navy, hlShadow: C.orange, riskBg: "#E5484D" };

// `words` / `keywords` : narration et mots surlignés (par défaut, la vidéo « Dropshipping en RDC »).
// `risks` : mots surlignés en rouge (risques, erreurs). `theme` : couleurs (par défaut, fond clair).
// `hide(t)` masque les sous-titres quand un autre élément porte déjà la phrase.
export const Captions: React.FC<{
  hide?: (t: number) => boolean; words?: Word[]; keywords?: Set<string>; risks?: Set<string>; theme?: CaptionTheme;
}> = ({ hide, words = WORDS, keywords = DEFAULT_KEYWORDS, risks, theme = LIGHT }) => {
  const CHUNKS = chunksOf(words);
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // Ligne active : la dernière dont le premier mot a commencé (légère anticipation).
  let idx = -1;
  for (let i = 0; i < CHUNKS.length; i++) if (t >= CHUNKS[i].start - 0.08) idx = i;
  if (idx < 0 || hide?.(t)) return null;
  const chunk = CHUNKS[idx];
  const enter = spring({ frame: frame - Math.round((chunk.start - 0.08) * fps), fps, config: { damping: 16, stiffness: 180 } });

  return (
    <div
      style={{
        position: "absolute", top: 330, left: 70, right: 70, minHeight: 240,
        display: "flex", flexWrap: "wrap", justifyContent: "center", alignContent: "flex-start",
        gap: "6px 18px", fontFamily, fontWeight: 800, fontSize: 66, lineHeight: 1.18,
        textAlign: "center",
        opacity: enter, transform: `translateY(${(1 - enter) * 24}px)`,
      }}
    >
      {chunk.words.map((w, i) => {
        const spoken = t >= w.start - 0.03;
        const p = spring({ frame: frame - Math.round((w.start - 0.03) * fps), fps, config: { damping: 12, stiffness: 220 } });
        const risk = risks?.has(norm(w.text)) ?? false;
        const key = risk || keywords.has(norm(w.text));
        const scale = spoken ? 1 + 0.08 * Math.sin(Math.min(1, p) * Math.PI) : 1;
        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              color: spoken ? (risk ? C.white : key ? theme.hlText : theme.text) : theme.mute,
              background: spoken && key ? (risk ? theme.riskBg : theme.hlBg) : "transparent",
              borderRadius: 14,
              padding: key ? "0 12px" : 0,
              transform: `scale(${scale})`,
              boxShadow: spoken && key && !risk ? `0 6px 0 ${theme.hlShadow}` : "none",
              transition: "none",
              opacity: interpolate(p, [0, 1], [0.85, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
            }}
          >
            {w.text}
          </span>
        );
      })}
    </div>
  );
};
