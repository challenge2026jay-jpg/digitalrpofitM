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

const VOICE_END = WORDS[WORDS.length - 1].end;
export const TOTAL_SECONDS = VOICE_END + 1.2;
export const TOTAL_FRAMES = Math.ceil(TOTAL_SECONDS * FPS);

export const norm = (s: string) =>
  s.toLowerCase().replace(/[.,!?;:«»"…]/g, "").replace(/’/g, "'");

// Recherche d'expressions dans une narration alignée : `at` donne le début (s) de `phrase`,
// cherchée après l'expression `after` si fournie ; `endOf` donne sa fin.
export const makeAligner = (words: Word[]) => {
  const find = (phrase: string, from = 0): number => {
    const p = phrase.split(" ").map(norm);
    for (let i = from; i <= words.length - p.length; i++) {
      if (p.every((x, j) => norm(words[i + j].text) === x)) return i;
    }
    throw new Error(`Expression introuvable dans la narration : « ${phrase} »`);
  };
  const at = (phrase: string, after?: string): number => words[find(phrase, after ? find(after) : 0)].start;
  const endOf = (phrase: string, after?: string): number => {
    const i = find(phrase, after ? find(after) : 0);
    return words[i + phrase.split(" ").length - 1].end;
  };
  return { find, at, endOf };
};

// Narration à partir d'un alignement brut, décalée de LEAD.
export const withLead = (raw: Word[]): Word[] => raw.map((w) => ({ text: w.text, start: w.start + LEAD, end: w.end + LEAD }));

export const { find, at, endOf } = makeAligner(WORDS);

export const f = (seconds: number) => Math.round(seconds * FPS);

// Découpage en séquences selon les phrases réellement prononcées.
const pre = 0.12;
const b = {
  intro: 0,
  blocage: at("Elle suit") - pre,
  doute: at("Elle recommence") - pre,
  cause: at("Le doute") - pre,
  rdc: at("Depuis la RDC") - pre,
  verif: at("Avant de tout") - pre,
  payer: at("Si ce n'est") - pre,
  confiance: at("Un blocage") - pre,
  cta: at("Si tu veux explorer") - pre,
  fin: TOTAL_SECONDS,
};

export const SCENES = {
  intro: [b.intro, b.blocage],
  blocage: [b.blocage, b.doute],
  doute: [b.doute, b.cause],
  cause: [b.cause, b.rdc],
  rdc: [b.rdc, b.verif],
  verif: [b.verif, b.payer],
  payer: [b.payer, b.confiance],
  confiance: [b.confiance, b.cta],
  cta: [b.cta, b.fin],
} as const;

export type SceneName = keyof typeof SCENES;
