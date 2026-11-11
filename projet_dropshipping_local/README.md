# Dropshipping local avec 50 dollars — projet de montage TikTok (faceless, 9:16)

Projet éditable : tout le montage est décrit dans `plan.py` et rendu par `build.py`.

## Contenu

| Fichier / dossier | Rôle |
|---|---|
| `media/` | Les fichiers du Drive, sous leur nom exact (préfixés par leur numéro d'ordre) |
| `plan.py` | Plan de montage : chaque passage du script → plans (fichier, cadrage, mouvement, transition), sons, texte à l'écran |
| `build.py` | Rendu de la vidéo (Python + Pillow + ffmpeg) |
| `PLAN_DE_MONTAGE.md` | Tableau phrase / fichier / passage / texte / son et transition (généré par `python3 build.py --plan`) |
| `caler_voix.py` | Cale une voix enregistrée sur le script (transcription locale, mots horodatés) |
| `audio/music/` | Musique Mixkit « Motivating Mornings » |
| `audio/sfx/` | Effets Mixkit (licence Mixkit gratuite : utilisables dans un montage, pas redistribuables seuls) |
| `export/dropshipping_local_9x16.mp4` | Vidéo exportée |

## Ajouter la voix

**Avec la voix clonée ElevenLabs « Samantha Claude »** : générer le script complet (≈ 2 220 crédits par prise),
télécharger le MP3, puis :

```bash
python3 caler_voix.py chemin/voix.mp3
python3 build.py --plan
python3 build.py
```

**Avec ta propre voix** (note vocale WhatsApp, enregistrement téléphone) : même commande. L'audio est normalisé,
transcrit localement, et chaque mot du script reçoit son temps exact : les plans, les sous-titres et les sons suivent.

Sans voix, `build.py` utilise un minutage estimé (`audio/voix_mots_estime.json`) et monte la musique un peu plus fort.

## Modifier le montage

- Changer une image d'un passage : modifier la ligne correspondante dans `PASSAGES` (`plan.py`).
- Recadrer : `(cx, cy, zoom)` — centre du cadre dans l'image (0–1) et resserrement (> 1).
- Flouter une zone (prénom, numéro) : ajouter le fichier dans `BLUR`.
- Contrôler sans tout rendre : `python3 build.py --preview 2,10,30` → `cache/preview_0.jpg`.

## Règles respectées

- Faceless : visages recadrés hors champ (plans de mains, produits, colis).
- Aucune image présentée comme filmée à Kinshasa (aucun fichier du Drive n'est identifié comme tel).
- Pas de chiffres de revenus à l'écran ; seuls « 50 $ » et les années prononcées apparaissent.
- Sous-titres dans la zone centrale basse, décalés à gauche des boutons TikTok, mots-clés en jaune.
