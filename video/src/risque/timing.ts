// Vidéo « Sans stock ≠ sans risque » : alignement mot par mot de sa propre voix off.
import raw from "./words.json";
import { Word, makeAligner, withLead } from "../timing";

export const WORDS: Word[] = withLead(raw as Word[]);
export const { at, endOf } = makeAligner(WORDS);

export const VOICE_END = WORDS[WORDS.length - 1].end;
export const TOTAL_SECONDS = VOICE_END + 1.0;
export const TOTAL_FRAMES = Math.ceil(TOTAL_SECONDS * 30);

// Révélation de la marge : pendant la pause ajoutée après « refus. »
export const REVEAL = endOf("refus") + 0.25;

const pre = 0.1;
export const SCENES = {
  hook: [0, at("En réalité") - pre],
  deplace: [at("En réalité") - pre, at("Le client voit") - pre],
  parcours: [at("Le client voit") - pre, at("Mais voici") - pre],
  problemes: [at("Mais voici") - pre, at("Et dans tous") - pre],
  retour: [at("Et dans tous") - pre, at("Tu vends") - pre],
  marge: [at("Tu vends") - pre, at("Donc") - pre],
  criteres: [at("Donc") - pre, at("Tu veux apprendre") - pre],
  cta: [at("Tu veux apprendre") - pre, TOTAL_SECONDS],
} as const;
export type SceneName = keyof typeof SCENES;
