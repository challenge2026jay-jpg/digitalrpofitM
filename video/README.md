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
