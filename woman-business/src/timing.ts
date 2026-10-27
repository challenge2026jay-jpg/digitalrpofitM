// Toute la synchronisation dérive de l'alignement mot par mot de la voix off
// (ElevenLabs Scribe sur la voix clonée, décalé par data/build_voice.py).
import raw from "./words.json";

export type Word = { text: string; start: number; end: number };

export const FPS = 30;
// Petite respiration avant la première syllabe.
export const LEAD = 0.25;

export const WORDS: Word[] = (raw as Word[]).map((w) => ({
  text: w.text,
  start: w.start + LEAD,
  end: w.end + LEAD,
}));

export const VOICE_END = WORDS[WORDS.length - 1].end;
// Le dernier écran (appel à l'action) reste lisible 1,6 s après la dernière syllabe.
export const TOTAL_SECONDS = VOICE_END + 1.6;
export const TOTAL_FRAMES = Math.ceil(TOTAL_SECONDS * FPS);

export const norm = (s: string) =>
  s.toLowerCase().replace(/[.,!?;:«»"…]/g, "").replace(/’/g, "'");

// Index du premier mot de `phrase` à partir de l'index `from`.
export const find = (phrase: string, from = 0): number => {
  const p = phrase.split(" ").map(norm);
  for (let i = from; i <= WORDS.length - p.length; i++) {
    if (p.every((x, j) => norm(WORDS[i + j].text) === x)) return i;
  }
  throw new Error(`Expression introuvable dans la narration : « ${phrase} »`);
};

// Début (s) de `phrase`, cherchée après l'expression `after` si fournie.
export const at = (phrase: string, after?: string): number =>
  WORDS[find(phrase, after ? find(after) : 0)].start;

export const endOf = (phrase: string, after?: string): number => {
  const i = find(phrase, after ? find(after) : 0);
  return WORDS[i + phrase.split(" ").length - 1].end;
};

export const f = (seconds: number) => Math.round(seconds * FPS);

// Découpage en scènes selon les phrases réellement prononcées.
const pre = 0.15;
const b = {
  accroche: 0,
  obstacles: at("Trouver") - pre,
  samantha: at("Je suis") - pre,
  whatsapp: at("Tu peux aussi") - pre,
  ia: at("Sur ma chaîne") - pre,
  commandes: at("mieux comprendre") - pre,
  trafic: at("Je t'apprends") - pre,
  cta: at("Tu veux apprendre") - pre,
  fin: TOTAL_SECONDS,
};

export const SCENES = {
  accroche: [b.accroche, b.obstacles],
  obstacles: [b.obstacles, b.samantha],
  samantha: [b.samantha, b.whatsapp],
  whatsapp: [b.whatsapp, b.ia],
  ia: [b.ia, b.commandes],
  commandes: [b.commandes, b.trafic],
  trafic: [b.trafic, b.cta],
  cta: [b.cta, b.fin],
} as const;

export type SceneName = keyof typeof SCENES;
