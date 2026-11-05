# Vidéo TikTok — Dropshipping en RDC (Samantha Mwange)

Vidéo verticale 1080 × 1920, 30 i/s, 56,9 s, montée avec [Remotion](https://www.remotion.dev/).

**Fichier final :** `out/dropshipping-rdc.mp4`

## Contenu

| Élément | Fichier | Origine |
|---|---|---|
| Voix off (export ElevenLabs brut) | `public/audio/voix_elevenlabs_originale.mp3` | ElevenLabs, voix clonée « voix de samantha claude » (`zKdf6MIRGXwlngiJP357`), modèle `eleven_v4`, script officiel lu sans modification |
| Voix off montée (pauses de direction) | `public/audio/voix_off_finale.wav` | Générée par `data/build_voice.py` |
| Alignement mot par mot | `data/words_raw.json` → `src/words.json` | ElevenLabs Scribe sur la voix générée, décalé des pauses ajoutées |
| Musique de fond | `public/audio/musique.mp3` | Composition originale ElevenLabs Music (`eleven_music_v2_5`), sans paroles (vérifié par transcription) |
| Illustrations de Grâce | `public/img/grace_*.png` (originaux dans `data/candidats/`) | Générées pour ce projet avec ElevenLabs (`gpt-image-2.5-sunburst`) |
| Photo de Samantha Mwange | `public/img/samantha.jpg` | Fournie par Samantha Mwange |
| Effets sonores | `public/sfx/*.wav` | Synthétisés avec ffmpeg (aucune source tierce) |
| Police Poppins | `public/fonts/` | SIL Open Font License 1.1 (`public/fonts/OFL.txt`) |

Les sorties ElevenLabs sont utilisables selon les conditions de l'abonnement ElevenLabs du compte qui les a générées. Aucun élément de la vidéo de référence (images, sons, logo, nom) n'est réutilisé. Seuls ses principes de montage ont été repris : sous-titres mot par mot, mots-clés surlignés, cartes animées, coches, tampon, appel « lien dans ma bio ».

## Version storyboard en 12 scènes (`DropshippingRDC12`)

**Fichier final :** `out/dropshipping-rdc-12-scenes.mp4` (1080 × 1920, 30 i/s, 60,2 s)

| Élément | Fichier | Origine |
|---|---|---|
| Images des 12 scènes | `public/img/scenes/01.jpg` … `12.jpg` | Dossier Google Drive « Identité Claude » de Samantha Mwange (originaux PNG 1632 × 2176, redimensionnés en JPEG 1224 × 1632) |
| Musique allongée | `public/audio/musique_longue.mp3` | Même musique ElevenLabs, allongée de 2 mesures (92 BPM) par un fondu enchaîné aligné sur le rythme, pour que sa fin tombe sur l'écran final |
| Voix off et alignement | `public/audio/voix_off_finale.wav`, `src/words.json` | Réutilisés : même script mot pour mot, même voix clonée |

- **Code :** `src/scenes12.tsx` (une scène par passage de narration, incrustations calées sur les mots) et `src/Video12.tsx`.
- **Interfaces affichées :** l'écran d'erreur (scène 2) et la page « Documentation officielle » (scène 5) sont des interfaces génériques présentes dans les images fournies. Elles ne sont attribuées à aucune plateforme réelle.
- **Scène 6 :** le message est présenté comme un exemple.
- **Scène 9 :** aucune ville n'est nommée.

## « Sans stock ≠ sans risque » (`SansStockRisque`)

**Fichier final :** `out/sans-stock-sans-risque.mp4` (1080 × 1920, 30 i/s, 60,8 s). Elle suit le plan sonore et d'animation en 8 séquences : hook, risque déplacé, parcours de commande, problèmes réels, retour vers toi, calcul de marge, critères, appel WhatsApp.

| Élément | Fichier | Origine |
|---|---|---|
| Voix off | `public/audio/risque/voix_elevenlabs_originale.mp3` → `voix_off_finale.wav` | ElevenLabs, voix clonée « voix de samantha claude », `eleven_v4`. Pauses ajoutées via `data/risque_voice.json` : arrêt après le hook, silence avant « 5 $ de marge réelle » |
| Alignement | `data/risque_words_raw.json` → `src/risque/words.json` | ElevenLabs Scribe |
| Musique | `public/audio/risque/musique.mp3` | Composition originale ElevenLabs Music (minimal tech, légèrement tendue), sans paroles (vérifié par transcription). Lue à partir de 1 s pour que sa fin tombe sur le dernier plan |
| Effets sonores | `public/sfx/` (impact, bassdrop, whoosh_rev, tick, notif, cash, calc, error, glitch, clock, vibration, negative, chime) | Synthétisés avec ffmpeg |
| Photo | `public/img/samantha.jpg` | Fournie par Samantha Mwange (utilisée à la place d'un plan face caméra, non fourni) |

- **Interfaces affichées :** les notifications de messages et la notification « Nouvelle commande » sont génériques, sans logo ni interface d'une application réelle.
- **Calcul :** 25 − 9 − 4 − 4 − 1 − 2 = 5 $.

## « Choisir un produit et vendre sans stock avec le dropshipping local en RDC » (`DropshippingLocal`)

- **Fichier final :** `out/dropshipping-local-rdc.mp4` (1080 × 1920, 30 i/s, 2 min 33).
- **Plan de production complet** (concept, texte, timeline seconde par seconde, plans à tourner, animations, transitions, sons Mixkit avec liens et licences, réglages audio, textes, instructions CapCut, écran final) : `docs/plan-dropshipping-local-rdc.md`.

| Élément | Fichier | Origine |
|---|---|---|
| Voix off | `public/audio/local/voix_elevenlabs_originale.mp3` → `voix_off_finale.wav` | ElevenLabs, voix clonée « voix de samantha claude », texte exact ; pauses via `data/local_voice.json` |
| Alignement | `data/local_words_raw.json` → `src/local/words.json` | ElevenLabs Scribe |
| Musique et effets sonores | `public/mixkit/` (**non versionné**) | Mixkit : « Focus on Yourself » (Eugenio Mininni, Mixkit Stock Music Free License) et 12 effets sous Mixkit Sound Effects Free License. À télécharger avec `bash data/mixkit_fetch.sh` avant le rendu : les licences interdisent de redistribuer les fichiers seuls ou avec des fichiers sources. |
| Photos d'illustration | `public/img/scenes/06.jpg`, `07.jpg`, `10.jpg` | Dossier Drive « Identité Claude » |
| Photo | `public/img/samantha.jpg` | Fournie par Samantha Mwange |

## Synchronisation

Aucun timecode n'est écrit à la main. `src/timing.ts` charge l'alignement mot par mot. Les séquences, textes, icônes et effets sonores sont déclenchés en cherchant un mot ou une expression de la narration, par exemple `at("bloque")` ou `endOf("officielle")`. Si la voix est régénérée, il suffit de :

1. remplacer `public/audio/voix_elevenlabs_originale.mp3` et `data/words_raw.json` ;
2. ajuster les points de coupe des pauses dans `data/build_voice.py` (milieux des silences mesurés avec `ffmpeg -af silencedetect`), puis lancer `python3 data/build_voice.py` ;
3. refaire le rendu.

## Commandes

```bash
npm install
npm run studio   # prévisualisation et retouches
npm run render   # rendu dans out/dropshipping-rdc.mp4
```

`remotion.config.ts` pointe vers le Chromium « headless shell » de l'environnement cloud. Sur une autre machine, retirez la ligne `setBrowserExecutable`.
