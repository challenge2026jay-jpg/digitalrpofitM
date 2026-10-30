---
name: pub-premium-samantha
description: Produire une publicité vidéo verticale premium (9:16, 1080×1920) pour Samantha Mwange / WOMAN BUSINESS à partir d'un script, d'une vidéo de référence, de sa voix clonée ElevenLabs et de ses vraies photos Drive. Couvre l'analyse de la référence, l'extraction de ses sons de transition, la voix off, l'alignement mot par mot, la musique, le montage Remotion synchronisé, le contrôle qualité et la livraison. À utiliser pour toute nouvelle vidéo publicitaire, reel, TikTok ou motion design de Samantha.
---

# Publicité premium Samantha Mwange

Le projet `woman-business/` est le **gabarit** de référence : on le duplique (`cp -r woman-business <nouveau-projet>`, sans `node_modules/` ni `out/`) et on remplace le script, les scènes et les images. Ne jamais repartir de zéro.

## 0. Règles fixes (à respecter à chaque vidéo)

- **Script :** lire tout le texte fourni. Seules les retouches orales sont permises : chiffres en lettres (« trois ans »), « Woman Business » au lieu de « WOMAN BUSINESS » (sinon la voix épelle), repères comme « [lien à insérer] » non lus. Les signaler dans le livrable.
- **Durée :** fixée par la voix réelle. Ne jamais couper d'idée pour tenir un chrono.
- **Voix :** chercher d'abord le nom exact demandé avec `creative_list_voices` (plusieurs recherches : nom complet, mots isolés). S'il est absent, le dire et demander l'accord avant de remplacer. Voix clonée connue : « voix de samantha claude », `zKdf6MIRGXwlngiJP357` (français, accent africain). Ne jamais prendre une « Samantha » de la bibliothèque publique.
- **Photos :** uniquement les vraies photos du dossier Drive « Personal Identity Kit Samantha » (`19dSgrnpmTGnrlRa9BMfSIsx4hqlGs9IR`). Aucune personne générée, aucune retouche des traits.
- **Lien WhatsApp :** ne jamais l'inventer. Constante `LIEN_WHATSAPP` dans `src/scenes.tsx` ; tant qu'elle vaut `null`, l'écran final affiche « Lien ci-dessous ».
- **Honnêteté :** aucun prix, revenu, délai ni résultat inventé. Les maquettes d'interface portent « ILLUSTRATION ». Ne jamais dire qu'une ressource a été utilisée sans l'avoir vérifiée.
- **Crédits ElevenLabs :** chaque appel coûte (voix ≈ 1 700 / prise, musique ≈ 900 / variante, image ≈ 820 / variante, transcription d'une musique ≈ 500). Annoncer le coût **avant** les générations optionnelles. Ne jamais relancer un appel pour « réessayer ».

## 1. Inventaire des ressources

1. **Dépôt :** `git fetch --all`, puis chercher les ressources nommées dans le brief dans toutes les branches (`git ls-tree -r --name-only <branche>`, `git grep -i`). « Kalosanga » n'existe dans aucune branche au 27/10/2026 ; si on le redemande, revérifier, puis le dire précisément.
2. **Drive :** lister le dossier avec `search_files` (`parentId = '…'`, pagination). Télécharger les fichiers directement : `curl -sSfL "https://drive.usercontent.google.com/download?id=<ID>&export=download"`. Faire une planche (`ffmpeg … hstack`) et la regarder avant de choisir. Photos validées : pour la présentation, le portrait en blazer marine, main au menton, fond brun (fourni par Samantha ; copie dans `woman-business/public/img/samantha_presentation.jpg`), préféré par elle à `fierte_debout_endroit_chic.png` ; `samantha_assise_jambes_croisees_telephone_en_main.png` (scène WhatsApp), `sourire_portrait_face.png` (appel à l'action).
3. **Pinterest / « My Browser » :** non disponible dans les sessions cloud ; le signaler.

## 2. Analyser la vidéo de référence

```bash
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of compact REF.mp4
ffmpeg -i REF.mp4 -vf "fps=1,scale=184:-1,tile=6x4" -frames:v 1 planche.png            # vue d'ensemble
ffmpeg -ss 0 -t 4 -i REF.mp4 -vf "fps=6,scale=150:-1,tile=12x2" -frames:v 1 bande.png  # transitions image par image
ffmpeg -i REF.mp4 -vf "select='gt(scene,0.18)',showinfo" -an -f null - 2>&1 | grep -o "pts_time:[0-9.]*"   # coupes
```

Langage visuel relevé sur la référence WOMAN BUSINESS : fond ivoire, ombre de fenêtre en diagonale (`public/img/ombre_fenetre.png`, en mode `multiply`), petite accroche en serif italique au-dessus d'un grand mot-clé en Playfair gras italique couleur cacao, apparitions floues qui deviennent nettes, échos du titre en contour, cartes arrondies ombrées, photo dans une carte arrondie avec un éclat cacao, balayage en bandes cacao, écran final avec logo et formes rondes.

## 3. Récupérer les sons de transition de la référence (demandé par Samantha)

La bande-son de la référence mélange une chanson (avec voix) et des effets. On les sépare avec Demucs :

```bash
pip install -q torch torchaudio --index-url https://download.pytorch.org/whl/cpu && pip install -q demucs
ffmpeg -i REF.mp4 -vn -ac 2 -ar 48000 ref.wav
python3 -m demucs -n htdemucs -o sep ref.wav          # → sep/htdemucs/ref/{drums,other,bass,vocals}.wav
ffmpeg -i sep/htdemucs/ref/drums.wav -lavfi "showspectrumpic=s=1600x260:legend=1:scale=log:fscale=log" drums.png
```

- Les effets (souffles, impacts, pops, tic-tac) sont dans **drums** ; les blips et montées tonales sont dans **other**. **vocals** n'est jamais utilisé.
- Repérer les bouffées sur le spectrogramme, découper (`-ss/-t`), ajouter un fondu de 8 ms à l'entrée et de 80 ms à la sortie, puis **normaliser sur le pic** (−1 dBFS). Ne pas utiliser `loudnorm` sur des sons courts : il remonte le bruit.
- Sons déjà extraits pour la référence actuelle : `woman-business/public/sfx_ref/` (`whoosh_a/b/c`, `transition_longue`, `impact`, `pop_1/2/3`, `blip`, `riser`, `tictac`). Les réutiliser si la même référence est fournie. La table des instants d'origine est dans `woman-business/README.md`.
- Correspondance : changement de scène → whoosh ; balayage en bandes → transition_longue (0,45 s avant) ; gros mot-clé → impact ; carte ou pastille → pop (en alternant 1/2/3) ; mot-clé secondaire → blip ; entrée d'un nom, d'un téléphone ou d'une courbe → riser ; idée de durée → tictac. Volumes entre 0,2 et 0,4.
- **Droits :** ces sons viennent d'une vidéo tierce. Toujours le signaler dans le livrable et le README.

## 4. Voix off

1. `creative_create_flow`, puis `creative_generate_speech` (`eleven_v4`, voix clonée, paragraphes séparés par une ligne vide, 2 prises).
2. Télécharger **immédiatement** les MP3 (les liens expirent en 2 h). Choisir la prise dont les silences (`silencedetect=noise=-38dB:d=0.25`) tombent entre les paragraphes.
3. `creative_add_flow_asset_node` (prise retenue), puis `creative_transcribe_audio` (`eleven_scribe_v1`). Télécharger `words.json` dans `data/words_raw.json` et vérifier que la transcription correspond au script mot pour mot.
4. Ajouter des respirations au **milieu des silences mesurés** : `data/build_voice.py` (liste `PAUSES` : 0,15 à 0,5 s, jusqu'à 0,5 s avant l'appel à l'action). Le script produit `public/audio/voix_off_finale.wav` et `src/words.json`.

## 5. Musique et visuels

- **Musique :** `creative_generate_in_flow` (`music`, `eleven_music_v2_5`), en décrivant un morceau instrumental élégant, sobre, avec piano et cordes pincées vers 96 BPM, de la durée de la voix + 2 s. Le réglage « Instrumental » n'est pas garanti : transcrire la variante retenue (transcription vide = pas de chant). Mesurer l'enveloppe de volume (`volumedetect` seconde par seconde) ; si le morceau s'éteint trop tôt, l'allonger d'un nombre entier de mesures (`data/tempo.py`, puis `atrim` + `acrossfade=d=1.5:c1=qsin:c2=qsin`, point de reprise = fin − 1,5 s − k × mesure). Volume 0,09 sous la voix (≈ 19–20 dB en dessous), 0,16 après la dernière phrase.
- **Natures mortes :** `bytedance-seedream-5-pro`, sans personne, sans texte, sans logo, palette ivoire, beige et cacao, ombres de fenêtre. Le modèle sort du 16:9 : recadrer au centre de l'objet (`crop=1150:1152:X:0`) et vérifier que rien n'est coupé.
- **Polices :** Playfair Display (paquet npm `@fontsource/playfair-display`, fichiers woff2) et Poppins, toutes deux sous licence OFL, dans `public/fonts/`, chargées avec `FontFace`. Google Fonts échoue derrière le proxy.

## 6. Montage Remotion

- `src/timing.ts` : `at("mot", "après")` et `SCENES`, découpées sur les phrases prononcées. **Aucun timecode écrit à la main.** Attention aux mots répétés (« tu veux », « l'IA », « Woman », « développer ») : préciser l'expression qui précède avec `after`.
- `src/ui.tsx` : palette `C`, `Reveal` (apparition floue), `Words`, `Letters`, `Echo`, `Kicker`, `Card`, `Burst`, `Icon`, `IconDot`, `WindowShadow`. Pas d'emoji : le rendu headless n'a pas de police emoji.
- `src/scenes.tsx` : `Stage` (entrée et sortie floues, légère poussée de caméra), `Phase` (changement d'idée dans une scène), `PhotoCard`, `Phone`. Chevauchement de 8 frames entre scènes.
- `src/Video.tsx` : fond, scènes, ombre de fenêtre, signature, bandes cacao, voix, musique et `SFX` (chaque effet déclenché sur un mot).
- Marges : 92 px sur les côtés ; contenu utile entre y = 200 et y = 1600 (zones d'interface de TikTok et Reels).

## 7. Contrôle et rendu

```bash
cd <projet> && npm install && npx tsc -p .
node data/stills.mjs 1.5 6 9 15 20 31 45 58 63 70 80 90   # images de contrôle à ½ échelle → out/still_*.png
npx remotion render <Id> out/<nom>.mp4 --codec=h264 --crf=18 --audio-codec=aac --audio-bitrate=192k --concurrency=4
```

- Navigateur : `/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell` (le numéro de version peut changer : `ls /opt/pw-browsers`). À mettre dans `remotion.config.ts` et `data/stills.mjs`.
- **Regarder** les planches d'images de contrôle avant le rendu complet : textes qui débordent (« même depuis la RDC ? » → passer sur 2 lignes), échos qui chevauchent le texte (1 copie au lieu de 2), photos mal recadrées, points qui apparaissent avant leur courbe.
- Rendu d'environ 92 s : 8 à 10 min, à lancer en arrière-plan.

Contrôle qualité final :

```bash
ffprobe -v error -show_entries stream=width,height,r_frame_rate:format=duration -of compact OUT.mp4   # 1080x1920, 30/1
ffmpeg -i OUT.mp4 -vf blackdetect=d=0.1:pix_th=0.1 -an -f null - 2>&1 | grep -c black_start            # 0
ffmpeg -i OUT.mp4 -af silencedetect=noise=-45dB:d=0.8 -vn -f null - 2>&1 | grep silence_start           # rien
ffmpeg -i OUT.mp4 -af ebur128 -vn -f null - 2>&1 | grep -E "^\s+I:"                                      # ≈ -16,5 LUFS
ffmpeg -ss T -t 1.2 -i OUT.mp4 -vf "fps=8,scale=135:-1,tile=10x1" -frames:v 1 transition.png             # transitions
```

Pour vérifier que les effets sonores sont présents, comparer le niveau moyen (`volumedetect`) aux instants des effets avec une version sans effets. Claude ne peut pas écouter : demander une écoute finale à Samantha.

## 8. Livraison

- Vidéo dans `<projet>/out/`, envoyée avec `SendUserFile` (`display: render`).
- README du projet : script lu et retouches, tableau des ressources et licences, sons de la référence avec leurs instants d'origine, ressources introuvables.
- Commit, push sur la branche de travail, PR en brouillon, abonnement à la PR.
- Bilan court en français : vidéo, durée réelle, script, ressources utilisées, coût en crédits, éléments manquants (lien WhatsApp, ressources introuvables, droits des sons tiers).
