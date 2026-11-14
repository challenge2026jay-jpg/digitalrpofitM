# Règles permanentes pour ce dépôt

## Modèle de toutes les vidéos (décision de la propriétaire)
**Toute nouvelle vidéo (faceless ou facecam, peu importe le sujet ou le format) part du modèle `modele_video/`**, tiré de la vidéo YouTube « Les obstacles des commandes en Chine ».

- Lire `modele_video/MODELE_VIDEO.md` AVANT de commencer toute vidéo.
- **Ne JAMAIS changer le thème ni le style** : fonds vert émeraude (sombre, grille, crème, noir), couleurs, polices (Inter + Playfair Display Italic + IBM Plex Mono), cartes, tampons, curseur, suivi de progression, sous-titres, règles de rythme et de son.
- **On change seulement le concept des animations**, selon ce que dit la voix.
- Réutiliser `modele_video/engine.py` tel quel ; copier `exemple_long_16x9.py` (YouTube) ou `exemple_court_9x16.py` (vertical) pour écrire le nouveau storyboard.
- Si une consigne est ambiguë, poser les questions AVANT de faire quoi que ce soit.

## Règles qui s'appliquent toujours
- Voix : n'utiliser que la voix d'origine fournie (jamais de TTS ni de voix de remplacement sauf demande). Retirer doublons, hésitations et sons parasites.
- Une image n'apparaît que si le mot prononcé lui correspond, avec un son. Jamais de succession aléatoire d'images. Équilibrer texte et images.
- Effets sonores seulement sur un événement visible, jamais plus d'un par seconde. Musique discrète.
- Aucun chiffre, revenu ou résultat inventé. Étiqueter le contenu IA. Faceless : aucun visage identifiable. Flouter les données personnelles.
- Ne jamais publier sans demande explicite. Toujours signaler les problèmes (licences, voix, ressources manquantes).
- Fichiers de moins de 100 Mo (limite GitHub). Grain fixe, pas animé.
- Écrire en français, en tutoyant.
