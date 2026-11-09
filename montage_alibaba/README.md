# TikTok faceless — « Commander sur Alibaba »

Vidéo verticale 9:16 (1080×1920, 30 fps, 2 min 23 s) montée d'après le style du « Final edit » de la vidéo de référence :
images réalistes plein cadre, coupes franches avec légers zooms, sous-titres blancs synchronisés mot à mot avec mots clés en jaune.
Pas de visage, d'avatar ni d'éléments de démonstration (« original », « Final edit », timeline).

## Fichiers

| Fichier | Rôle |
|---|---|
| `export/alibaba_tiktok.mp4` | **Vidéo finale** (H.264 + AAC), non publiée |
| `PLAN_DE_MONTAGE.md` | Tableau phrase / fichier / moment / texte écran / son |
| `projet_editable/alibaba_tiktok.fcpxml` | Timeline éditable : plans, voix, musique, SFX sur pistes séparées (DaVinci Resolve : *Fichier → Importer → Timeline*, Final Cut Pro, Premiere via conversion XML). Reliez les médias au dossier `media/` si demandé. Les zooms, cartes et checklist sont « cuits » dans le rendu Python, pas dans la timeline. |
| `sous_titres.srt` / `sous_titres.ass` | Sous-titres mot à mot (SRT pour CapCut/Premiere, ASS = style exact) |
| `plan.py` | Plan de montage source : plans, cadrages, timings, effets sonores, volumes |
| `build.py` | Rendu complet (`python3 build.py`), aperçus (`--preview 12.5,40`) |
| `export_projet.py` | Régénère `PLAN_DE_MONTAGE.md` et le FCPXML |
| `audio/` | Voix off ElevenLabs + transcription horodatée, musique et SFX Mixkit |
| `media/` | Images du Drive (noms d'origine). Les vidéos du Drive (88 Mo) ne sont pas versionnées : téléchargez-les depuis le dossier Drive dans `media/` sans les renommer. |

## Sources

- **Visuels** : uniquement le dossier Drive fourni (15 fichiers, tous examinés un par un). Pinterest n'a pas été utilisé : la recherche exige une connexion, et le Chrome de l'ordinateur n'était pas joignable depuis la session.
- **Voix** : ElevenLabs, voix clonée « voix de samantha claude » (seule voix clonée du compte correspondant à « Samantha Claude »), modèle `eleven_multilingual_v2`.
- **Musique** : Mixkit « Motivating Mornings » (#33), licence *Mixkit Stock Music Free License*.
- **Effets** : Mixkit (licence *Sound Effects Free License* : usage libre, commercial ou non, dans des vidéos sur les réseaux sociaux) — détails dans `export_projet.py` (`SFX_LABEL`).

## Photo de couverture

- `export/couverture_tiktok.png` (version A, camion rouge devant l'entrepôt) et `export/couverture_tiktok_b.png` (version B, chargement du conteneur), 1080×1920, générées par `python3 cover.py`.
- Texte dans la zone centrale 3:4 (visible sur la grille du profil TikTok). Pas de logo Alibaba : le nom est écrit en texte neutre pour ne pas suggérer de partenariat.
- Police : Anton (`fonts/Anton.woff2`, SIL Open Font License 1.1, Google Fonts) + Inter Display (OFL).
- Fond : photos du Drive (`896708975821689274.jpg`, `Custom Canvas Totes – Ready for Your Brand.jpg`).
- Références Pinterest, utilisées uniquement pour l'inspiration (REFERENCE_ONLY, aucune image intégrée) : principes retenus = titre très gras condensé, contraste jaune/noir, hiérarchie empilée, mot clé dans un bloc de couleur.
  - https://www.pinterest.com/ideas/black-and-yellow-text-design/947134288399/
  - https://www.pinterest.com/quotes-pin/digital-products-poster-design--13792342604789441/
  - https://za.pinterest.com/ideas/bold-yellow-text-design/921386179117/
  - https://www.pinterest.com/ideas/bold-red-and-yellow-text/952960177119/
