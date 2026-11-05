// Vidéo « Choisir un produit et vendre sans stock avec le dropshipping local en RDC ».
import raw from "./words.json";
import { Word, makeAligner, withLead } from "../timing";

export const WORDS: Word[] = withLead(raw as Word[]);
export const { at, endOf } = makeAligner(WORDS);

export const VOICE_END = WORDS[WORDS.length - 1].end;
export const END_HOLD = 3.0; // écran final lisible après la dernière phrase
export const TOTAL_SECONDS = VOICE_END + END_HOLD;
export const TOTAL_FRAMES = Math.ceil(TOTAL_SECONDS * 30);

const pre = 0.1;
const S = (phrase: string, after?: string) => at(phrase, after) - pre;

// Une séquence par passage de narration ; chaque séquence change encore de visuel toutes les 2 à 4 s.
const cuts: [string, number][] = [
  ["sansStock", 0],
  ["pasNimporte", S("Mais tu ne")],
  ["methode", S("La vraie méthode")],
  ["commentTitre", S("Voici comment")],
  ["schema", S("Tu identifies")],
  ["quatreChoses", S("Pour choisir")],
  ["viral", S("Un produit viral")],
  ["calcul", S("Prenons")],
  ["risquesMarge", S("Mais si le client")],
  ["livrees", S("Tu dois donc calculer")],
  ["erreurs", S("Évite")],
  ["bonneBase", S("Commence avec")],
  ["gagnant", S("Tu ne cherches")],
  ["utile", S("Tu cherches un produit utile")],
  ["cta", S("Tu veux apprendre")],
];

export type SceneName =
  | "sansStock" | "pasNimporte" | "methode" | "commentTitre" | "schema" | "quatreChoses" | "viral" | "calcul"
  | "risquesMarge" | "livrees" | "erreurs" | "bonneBase" | "gagnant" | "utile" | "cta";

export const SCENES = Object.fromEntries(
  cuts.map(([name, start], i) => [name, [start, i + 1 < cuts.length ? cuts[i + 1][1] : TOTAL_SECONDS] as const]),
) as Record<SceneName, readonly [number, number]>;

export const ORDER = cuts.map(([n]) => n as SceneName);
