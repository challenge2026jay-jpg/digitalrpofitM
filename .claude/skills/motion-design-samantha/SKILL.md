---
name: motion-design-samantha
description: Produire une vidéo courte verticale (TikTok, Reels, Shorts) en motion design pour Samantha Mwange, à partir d'un script, de sa voix clonée ElevenLabs et d'une vidéo de référence : voix off, alignement mot par mot, montage Remotion synchronisé, rendu MP4 1080×1920 et contrôle qualité. À utiliser pour toute demande de vidéo, de montage, de voix off ou de contenu animé pour Samantha Mwange ou ses thèmes (dropshipping, e-commerce, RDC).
---

# Motion Design Samantha

Chaîne de production complète, éprouvée sur la vidéo « Dropshipping en RDC » (`video/`). Le projet `video/` sert de **gabarit** : on le duplique ou on l'adapte au lieu de repartir de zéro.

## 0. Règles fixes

- **Script :** lire le texte fourni tel quel, sans réécrire, résumer ni ajouter de phrase. Les indications d'interprétation (pauses, ton) ne sont jamais lues à voix haute.
- **Voix :** uniquement la voix clonée **« voix de samantha claude »**, `voice_id` **`zKdf6MIRGXwlngiJP357`** (français, catégorie *cloned*). Avant de générer, vérifier qu'elle existe avec `creative_list_voices` (search « samantha »). Ne jamais prendre une autre « Samantha » de la bibliothèque publique.
- **Identité visuelle :**
  - format vertical 1080 × 1920, fond bleu ciel avec grille légère ;
  - photo de Samantha en **bulle ronde en haut à droite**, avec « Samantha Mwange » au-dessus ;
  - grande photo, nom et appel à l'action en fin de vidéo ;
  - police Poppins, très lisible sur téléphone.
- **Photo :** utiliser le fichier réellement fourni (`video/public/img/samantha.jpg`). Ne jamais générer de portrait qui lui ressemble.
- **Vidéo de référence :** reprendre les principes de montage, jamais le nom, le logo, les images ou les sons d'autrui.
- **Liens :** ne pas inventer de lien WhatsApp. L'appel renvoie au « lien dans ma bio ».
- **Honnêteté :** ne jamais prétendre avoir généré, écouté ou exporté quelque chose sans l'avoir fait. Signaler le blocage précis.
- **Crédits :** chaque génération ElevenLabs coûte des crédits. Ne jamais relancer un appel pour « réessayer ». Annoncer le coût approximatif à la fin.

## 1. Inventaire

1. Inspecter le dépôt (`git ls-files`, branches) et réutiliser `video/` (composants, effets sonores, polices, configuration).
2. Vidéo de référence : TikTok bloque yt-dlp, Firecrawl et l'oEmbed (aucune image exploitable). Demander directement le **fichier vidéo**, puis l'analyser :
   ```bash
   ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of compact REF.mp4
   ffmpeg -i REF.mp4 -vf "select='gt(scene,0.25)',showinfo" -vsync vfr -f null - 2>&1 | grep -o "pts_time:[0-9.]*"
   ffmpeg -i REF.mp4 -vf "fps=1/3,scale=192:-1,tile=6x3" sheet_%02d.png   # puis lire les planches
   ```
   Noter : rythme, sous-titres mot par mot, mots-clés surlignés, cartes et icônes, coches, tampons, transitions, appel final.

3. **Dossier Drive « Identité Claude »** (`1KMWBxS078lwEnvu_HktsQeb66NsVK7NU`) :
   - Lister avec `search_files` (`parentId = '…'`, avec pagination).
   - Le connecteur Drive ne transmet les fichiers qu'en base64 dans la conversation, ce qui est inutilisable pour des images ou des vidéos.
   - Si les fichiers sont partagés par lien, les télécharger directement : `curl -sSfL "https://drive.usercontent.google.com/download?id=<ID>&export=download"`.
   - Le même blocage empêche de **déposer** une vidéo sur Drive : le dire à Samantha au lieu de le prétendre fait.
4. **Storyboard en images numérotées** (`01_…png` à `12_…png`) : une image par scène, à placer dans un cadre photo (composition `DropshippingRDC12`, `src/scenes12.tsx`). Relever les coordonnées des zones à surligner sur une copie quadrillée (`drawgrid`), puis les convertir avec `P(x, y, focusY)`.

Si le script est identique à une vidéo précédente, **réutiliser** la voix, l'alignement et les pauses déjà produits (environ 1 900 crédits économisés) et le signaler.

## 2. Voix off (ElevenLabs, connecteur complet `Eleven_labs`)

1. `creative_create_flow` pour regrouper toutes les générations du projet.
2. `creative_generate_speech` : `model_id: eleven_v4`, `voice_id: zKdf6MIRGXwlngiJP357`, le script exact avec une ligne vide entre les phrases. Garder le nombre de prises par défaut (2). Une « prise » est une version de **la même voix** ; l'expliquer à Samantha si besoin.
3. Interroger `creative_get_flow_run_status` jusqu'à `all_completed`, puis télécharger **immédiatement** les MP3 (les URL signées expirent en 2 h).
4. Retenir une prise, garder son export brut (`public/audio/voix_elevenlabs_originale.mp3`) et supprimer l'autre pour éviter toute confusion.

## 3. Alignement mot par mot (obligatoire)

1. `creative_add_flow_asset_node` (modality `audio`, `generation_id` de la prise retenue), puis `creative_transcribe_audio` (`eleven_scribe_v1`, `connect_from` = ce nœud).
2. Le résultat contient `words` (start/end par mot) et `words_download_url`. Télécharger le JSON dans `data/words_raw.json`.
3. Comparer le texte transcrit au script : il doit être identique mot pour mot.

## 4. Pauses de direction

ElevenLabs enchaîne les phrases presque sans pause. On insère les pauses demandées **au milieu des silences réels**, puis on décale l'alignement :

```bash
ffmpeg -i public/audio/voix_elevenlabs_originale.mp3 -af silencedetect=noise=-38dB:d=0.12 -f null - 2>&1 | grep silence_
```

Reporter les milieux de silence dans `PAUSES` de `data/build_voice.py` (point de coupe, durée ajoutée), puis lancer `python3 data/build_voice.py`. Le script produit `public/audio/voix_off_finale.wav` et `src/words.json`. Repères utilisés :
- 0,15 à 0,5 s entre les phrases ordinaires ;
- environ 0,9 s après une phrase émotionnelle (« se sent nulle ») et après la phrase clé (« tu n'es pas capable »).

Les fins de mot données par Scribe débordent légèrement sur le silence : se fier à `silencedetect` pour les coupes.

## 5. Ressources visuelles et sonores

- **Illustrations :** `creative_generate_image` (`gpt-image-2.5-sunburst`, 2 variations). Demander un style vectoriel plat, un fond blanc uni, sans texte et une palette bleu ciel / marine / moutarde / orange. Un seul prompt de personnage donne deux variantes cohérentes (ex. une expression concentrée et une expression de doute). Recadrer avec `ffmpeg -vf crop=...` et les poser sur une carte blanche arrondie : pas besoin de détourage.
- **Musique :** `creative_generate_in_flow` (`node_type: music`, `eleven_music_v2_5`), en décrivant un morceau instrumental doux et discret, avec la durée voulue.
  - Le nœud n'impose pas l'instrumental. **Vérifier l'absence de chant** en transcrivant la musique : une transcription vide signifie pas de paroles.
  - Par défaut, 4 variations sont générées, d'environ 900 crédits chacune.
  - Mesurer la fin du morceau (`volumedetect` seconde par seconde). Si elle s'éteint trop tôt, décaler la musique (`MUSIC_DELAY`) pour que sa fin naturelle tombe sur le dernier plan.
  - Si le morceau est trop court, mesurer le tempo (`data/tempo.py`) et l'allonger d'un nombre entier de mesures, sans nouvelle génération. Exemple : `atrim=0:36.70` + `atrim=30` avec `acrossfade=d=1.5:c1=qsin:c2=qsin`. Le point de jonction doit être décalé d'un multiple de la mesure, et les courbes `qsin` évitent le creux de volume.
- **Fin d'un élément ou d'un tampon :** caler l'apparition sur le **début** du mot (`at`) plutôt que sur sa fin (`endOf`) quand la scène se termine juste après le mot. Sinon l'élément n'apparaît qu'en sortie de scène.
- **Effets sonores :** synthétisés avec ffmpeg (aucun droit tiers), déjà présents dans `public/sfx/` (pop, whoosh, ding, thud, click).
- **Police :** Poppins TTF (OFL) dans `public/fonts/`, chargée en local avec `FontFace`. Google Fonts échoue derrière le proxy (`ERR_CERT_AUTHORITY_INVALID`).
- **Droits :** rien venant de Pinterest ou d'ailleurs sans source et licence vérifiées. Tout tracer dans `video/README.md`.

## 6. Montage Remotion (`video/`)

Architecture :
- `src/timing.ts` : charge `words.json` et ajoute `LEAD` (0,25 s). Fournit les fonctions `find`, `at(expression, après?)` et `endOf(expression)`, et calcule `SCENES` à partir des phrases réellement prononcées. **Aucun timecode écrit à la main** : chaque élément se déclenche sur un mot.
- `src/Captions.tsx` : sous-titres en haut (y ≈ 330), découpés en lignes de 6 mots maximum. Le mot prononcé s'allume, les mots à venir restent gris, les mots-clés sont surlignés en jaune avec une ombre orange.
- `src/scenes.tsx` : une scène par étape de l'histoire, dans un `Stage` qui gère l'entrée en ressort, la caméra simulée (léger zoom) et la sortie en fondu.
  - Les scènes se chevauchent de `OVERLAP` = 7 frames pour un fondu enchaîné, sinon l'écran se vide 0,3 s.
  - Une scène émotionnelle utilise `calm` (ressort plus lent) et une teinte de fond.
- `src/ui.tsx` : palette `C`, `Pop`, `Card`, `Pill`, `Check` animé, icônes SVG maison. Pas d'emoji : le rendu headless n'a pas de police emoji.
- `src/Video.tsx` : fond, bandeau en haut à gauche, bulle photo en haut à droite (masquée quand la grande photo de fin arrive), bandeau du bas, séquences, sous-titres, voix, musique et effets sonores calés sur les mots.
  - Volume musique : environ 0,09 sous la voix, 0,17 après la dernière phrase, avec fondu d'entrée et de sortie.

Structure narrative type (à adapter au script) :
1. personnage et sujet ;
2. le blocage, avec le texte principal ;
3. le doute (rythme ralenti, image assombrie) ;
4. les causes possibles, aucune présentée comme certaine ;
5. le contexte RDC ;
6. la liste de vérifications et les mots-clés successifs ;
7. confirmer avant de payer (tampon) ;
8. reprendre confiance (composition dégagée) ;
9. appel à l'action, avec photo, nom et bouton WhatsApp générique.

Ne jamais afficher de faux site officiel ni de fausse erreur attribuée à une vraie plateforme.

## 7. Rendu

Commandes :

```bash
cd video && npm install
npx tsc -p .                                                   # typage
npx remotion still DropshippingRDC out/s.png --frame=NNN       # images de contrôle
npx remotion render DropshippingRDC out/<nom>.mp4 --codec=h264 --crf=18 --audio-codec=aac
```

Points à respecter :
- **Navigateur :** `remotion.config.ts` doit pointer vers `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`. Le Chromium normal échoue (« Old Headless mode has been removed »).
- **Images de contrôle :** rendre une dizaine d'images fixes aux moments clés, les assembler (`hstack`) et les **regarder** avant le rendu complet. On y repère chevauchements, retours à la ligne et scènes vides.
- **Durée :** compter environ 4 min 30 de rendu pour 57 s de vidéo.

## 8. Contrôle qualité (avant de dire « terminé »)

```bash
ffprobe -v error -show_entries stream=width,height,r_frame_rate:format=duration -of compact OUT.mp4
ffmpeg -i OUT.mp4 -vf blackdetect=d=0.1:pix_th=0.1 -an -f null - 2>&1 | grep -c black_start   # attendu : 0
ffmpeg -i OUT.mp4 -af silencedetect=noise=-45dB:d=0.6 -vn -f null - 2>&1 | grep silence_start  # attendu : rien
ffmpeg -i OUT.mp4 -af ebur128 -vn -f null - 2>&1 | grep -E "^\s+I:"                            # voix ≈ -15 LUFS
ffmpeg -ss T -t 1.5 -i OUT.mp4 -vf "fps=4,scale=180:-1,tile=6x1" -frames:v 1 transition.png     # transitions
```

Vérifier aussi :
- la narration est complète et fidèle (transcription identique au script) ;
- la voix est bien la voix clonée (le résultat de génération indique `voice.name`) ;
- l'orthographe est correcte ;
- la musique reste au moins 20 dB sous la voix ;
- le format est 9:16 ;
- aucune image ne manque.

Dire clairement que Claude ne peut pas écouter l'audio et demander à Samantha une écoute finale.

## 9. Livraison

- **Fichiers :** vidéo dans `video/out/`, envoyée avec `SendUserFile` (display `render`).
- **Dépôt :** commit et push sur la branche de travail, PR en brouillon, abonnement à la PR.
- **Bilan court en français :**
  - ce qui a été fait ;
  - les ressources et leurs licences ;
  - le coût en crédits ElevenLabs ;
  - les blocages éventuels ;
  - les chemins des fichiers.
