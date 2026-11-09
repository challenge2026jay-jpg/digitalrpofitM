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
