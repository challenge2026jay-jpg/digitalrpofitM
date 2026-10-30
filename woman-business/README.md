# Publicité WOMAN BUSINESS — chaîne WhatsApp (Samantha Mwange)

Vidéo verticale 1080 × 1920, 30 i/s, montée avec [Remotion](https://www.remotion.dev/).

**Fichier final :** `out/woman-business.mp4`

## Script de narration utilisé

Le script fourni est lu en entier. Seules trois retouches ont été faites pour l'oral :

- « 3 ans » est écrit « trois ans » pour la synthèse vocale ;
- « WOMAN BUSINESS » est écrit « Woman Business » pour que le nom ne soit pas épelé ;
- le repère « [Lien de la chaîne WhatsApp à insérer] » n'est pas lu.

> Tu es en RDC et tu veux te lancer dans le commerce en ligne, mais tu ne sais pas comment commander tes produits à l'étranger ?
>
> Trouver un fournisseur fiable, effectuer des paiements internationaux, gérer le transport et les frais de douane… Tous ces obstacles peuvent freiner ton projet.
>
> Je suis Samantha Mwange, entrepreneure et créatrice de Woman Business.
>
> Depuis plus de trois ans, j'évolue dans le dropshipping et j'explore les possibilités qu'offre l'intelligence artificielle pour faciliter le commerce en ligne en RDC.
>
> Tu peux aussi apprendre à mieux utiliser WhatsApp pour vendre tes produits.
>
> Au lieu d'utiliser WhatsApp uniquement pour discuter avec tes proches, apprends à publier des contenus qui suscitent l'intérêt, à mieux présenter tes offres et à transformer l'intérêt de tes contacts en achats.
>
> L'objectif est de faire de WhatsApp un véritable outil commercial.
>
> Sur ma chaîne WhatsApp, je partage des démonstrations pratiques pour t'aider à découvrir des outils d'intelligence artificielle utiles pour ton business, rechercher des produits et des fournisseurs, créer des publicités vidéo avec l'IA, développer une boutique en ligne et mieux comprendre les étapes et les défis des commandes à l'étranger.
>
> Je t'apprends également à attirer du trafic vers tes réseaux sociaux et à explorer les possibilités de monétisation de plateformes comme TikTok, YouTube et Instagram.
>
> Tu veux apprendre à utiliser l'IA pour développer ton activité commerciale, même depuis la RDC ?
>
> Rejoins gratuitement la chaîne WhatsApp Woman Business en cliquant sur le lien ci-dessous.
>
> Woman Business : des outils, des démonstrations et des opportunités pour entreprendre autrement grâce à l'IA.

La transcription ElevenLabs Scribe de la voix générée correspond mot pour mot à ce texte.

## Ressources

| Élément | Fichier | Origine |
|---|---|---|
| Voix off (export brut) | `public/audio/voix_elevenlabs_originale.mp3` | ElevenLabs, voix clonée « voix de samantha claude » (`zKdf6MIRGXwlngiJP357`), modèle `eleven_v4`. La voix « Voix Samantha Claude Direct » demandée n'existe pas dans le compte ; ce remplacement a été validé par Samantha. |
| Voix off montée | `public/audio/voix_off_finale.wav` | `data/build_voice.py` : respirations ajoutées entre les parties, au milieu des silences réels |
| Alignement mot par mot | `data/words_raw.json` → `src/words.json` | ElevenLabs Scribe |
| Musique | `public/audio/musique.mp3` (original : `data/generations/musique_originale.mp3`) | Composition originale ElevenLabs Music (`eleven_music_v2_5`), sans chant (transcription vide). Allongée de 2 mesures (96 BPM) par un fondu enchaîné aligné sur le tempo. |
| Photos de Samantha | `public/img/samantha_presentation.jpg`, `samantha_telephone.jpg`, `samantha_portrait.jpg` | Présentation : portrait en blazer marine, main au menton, fond brun, fourni directement par Samantha (remplace `fierte_debout_endroit_chic.png`). WhatsApp et appel à l'action : dossier Google Drive « Personal Identity Kit Samantha » (`samantha_assise_jambes_croisees_telephone_en_main.png`, `sourire_portrait_face.png`). Toutes redimensionnées seulement, sans autre retouche. |
| Natures mortes (colis) | `public/img/colis_piedestal.jpg`, `colis_ombres.jpg` | Générées pour ce projet avec ElevenLabs (`bytedance-seedream-5-pro`). Aucune personne, aucun texte, aucun logo. |
| Ombre de fenêtre | `public/img/ombre_fenetre.png` | Générée par `data/make_shadow.py` |
| Effets sonores | `public/sfx_ref/*.wav` | Extraits de la vidéo de référence fournie par Samantha, à sa demande : séparation de sources (Demucs `htdemucs`, pistes « batterie » et « autres », pour écarter la chanson et sa voix), puis découpe aux instants des transitions. Voir « Sons de transition » ci-dessous. |
| Polices | `public/fonts/` | Playfair Display et Poppins, SIL Open Font License 1.1 |
| Pictogrammes, maquette de téléphone | `src/ui.tsx`, `src/scenes.tsx` | Dessinés en code pour ce projet. La maquette porte la mention « ILLUSTRATION » ; elle ne reproduit pas l'interface de WhatsApp. |

## Sons de transition (repris de la vidéo de référence)

Samantha a demandé que les sons de la vidéo de référence soient réutilisés. Ils ont été isolés avec Demucs, puis découpés aux moments où ils apparaissent dans la référence :

| Fichier | Extrait de la référence | Utilisation dans la publicité |
|---|---|---|
| `whoosh_a/b/c.wav` | souffles à 0,40 s, 5,80 s, 9,42 s | changements de scène, étapes WhatsApp |
| `transition_longue.wav` | 1,72 → 3,18 s | balayages en bandes cacao (présentation, appel à l'action) |
| `impact.wav` | 7,95 s (batterie + basse de la piste « autres ») | « RDC », « obstacles », « outil commercial », « l'IA » |
| `pop_1/2/3.wav` | 15,05 / 15,36 / 15,66 s (apparition des cartes) | cartes, pastilles, plateformes, étapes |
| `blip.wav` | 5,22 s (piste « autres ») | mots-clés (WhatsApp, Woman Business, monétisation, lien) |
| `riser.wav` | 1,30 s (piste « autres ») | entrée du nom, du téléphone, du trafic |
| `tictac.wav` | 12,78 → 14,30 s (horloge) | « Depuis plus de 3 ans » |

**Droits :** ces sons viennent d'une vidéo tierce (gabarit publicitaire). Leurs conditions d'utilisation commerciale n'ont pas pu être vérifiées. Avant une diffusion payante, confirmer que la licence du gabarit ou de la banque de sons d'origine le permet ; sinon, revenir aux effets synthétisés (commit précédent).

## Ressources demandées mais introuvables

- **« Kalosanga » :** absent du dépôt `challenge2026jay-jpg/digitalrpofitM` (recherche dans les noms et contenus de toutes les branches et de tous les commits) et absent du Google Drive. Aucun autre dépôt n'est accessible depuis cette session.
- **Voix « Voix Samantha Claude Direct » :** absente des deux connexions ElevenLabs disponibles. La seule voix clonée de Samantha est « voix de samantha claude » (`zKdf6MIRGXwlngiJP357`), utilisée ici.

Les générations ElevenLabs sont utilisables selon les conditions de l'abonnement ElevenLabs du compte qui les a produites. Rien n'est repris de la vidéo de référence : ni ses images, ni ses sons, ni sa marque. Seul son langage de montage a été réinterprété : ombres de fenêtre, accroche en italique et mot-clé en serif cacao, apparitions floues, échos de texte en contour, cartes arrondies, balayage en bandes cacao.

## Lien WhatsApp

Aucun lien n'a été inventé. L'écran final affiche « Lien ci-dessous » dans un cadre réservé. Pour afficher le vrai lien, il suffit de renseigner `LIEN_WHATSAPP` dans `src/scenes.tsx`, puis de refaire le rendu.

## Synchronisation

Aucun timecode n'est écrit à la main. `src/timing.ts` charge l'alignement mot par mot, et chaque scène, texte, carte et effet sonore se déclenche sur un mot de la narration, par exemple `at("Instagram")`.

## Couverture TikTok

`out/couverture-tiktok.jpg` (et `.png`) : 1080 × 1920, composition `CouvertureTikTok` (`src/Cover.tsx`). Le texte et la photo restent dans le cadre central 3:4 (y 240 → 1680) que TikTok garde sur la grille du profil, hors de la colonne d'icônes à droite et de la zone de légende en bas. Rendu : `npx remotion still CouvertureTikTok out/couverture-tiktok.png`.

## Commandes

```bash
npm install
npx tsc -p .
node data/stills.mjs 1.5 16 45   # images de contrôle (s)
npm run render                    # out/woman-business.mp4
```

`remotion.config.ts` et `data/stills.mjs` pointent vers le Chromium « headless shell » de l'environnement cloud. Sur une autre machine, retirez ces chemins.
