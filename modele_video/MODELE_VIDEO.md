# MODÈLE DE TOUTES LES VIDÉOS : « Les obstacles des commandes en Chine »

Décision de la propriétaire de la chaîne : **toutes les vidéos futures, faceless ou facecam, partent de ce modèle.**
On ne change NI le thème NI le style. On change seulement le **concept des animations** selon ce que dit la voix.

Références réalisées :
- `exemple_long_16x9.py` : YouTube 16:9, 1920 × 1080, 30 i/s, 58 scènes (9 min 09 s).
- `exemple_court_9x16.py` : version courte verticale 1080 × 1920 (1 min), mêmes éléments remis en page.
- `engine.py` : tout le style (fonds, polices, cartes, tampons, curseur, animations). À réutiliser tel quel.
- `apercus/apercu_style.jpg` : planche de captures du rendu.

Les deux exemples sont des copies de référence : ils lisent `audio/` et `drive/` du dossier où ils tournent. Pour une nouvelle vidéo, créer `projet_xxx/`, y copier `engine.py`, `fonts/`, un exemple et `transcrire.py`, puis ajouter `audio/` (voix, `sfx/`, `music/`) et `drive/`.

## 1. Ce qui est FIXE (ne jamais changer)

### Couleurs
| Rôle | Valeur |
|---|---|
| Accent (mots-clés, coches, boutons) | vert menthe `#2FD08A` |
| Danger, piège, erreur | rouge brique `#E05A4F`, avec parcimonie |
| Texte | blanc, ou encre `#181E1B` sur fond clair |
| Cartes sombres | `#1A2420`, coins 18 px, bordure fine, ombre douce |
| Gris secondaire | `#96AAA0` (sur sombre), `#787C7C` (sur clair) |

### Fonds (3 + 1)
1. **sombre** : dégradé radial vert émeraude `#0E3B2C` au centre vers `#050D0A`, vignettage, grain fixe. Fond par défaut.
2. **grille** : vert moyen `#0F5A40` avec grille fine type plan d'architecte. Pour les chiffres et calculs.
3. **crème** : `#F1EFEA` avec grande courbe grise douce. Pour les comparaisons et les questions.
4. **noir** : presque noir avec vignettage. Pour les phrases-chocs, l'ouverture « rupture » et la phrase finale.

### Typographie (jamais d'autres polices)
- **Inter ExtraBold / Bold / SemiBold** : titres et texte.
- **Playfair Display Italic** : le mot fort d'un titre, les grands chiffres, les accroches. Elle se mêle au gras dans le même titre (« un parcours *du combattant.* »).
- **IBM Plex Mono** : petits labels en capitales dans les cartes (« PRIX AFFICHÉ »).
- Petite accroche en serif italique au-dessus du titre (« mais dans la réalité… »).

### Composants (dans `engine.py`)
- `label_card` : carte d'interface, petit label mono + grande valeur.
- `checklist_card` : checklist avec cases qui se cochent, une par mot prononcé. Marques « ok » vert ou « x » rouge.
- `pill` : pastille blanche ou sombre avec icône optionnelle.
- `stamp` : tampon incliné de −6°, cadre vert ou rouge, avec rebond. Exemples : VÉRIFIE, ARNAQUE, ÉCHANTILLON.
- `Cursor` : flèche de souris blanche qui se déplace et « clique » (petit cercle au clic).
- `framed` + `shadowed` : image posée dans un cadre arrondi, jamais collée brute. Zoom lent de 100 à 105-110 % (`kb`).
- Animations d'entrée : `pop`, `up`, `down`, `left`, `right`, `fade`, `stamp`. **Pas de transitions entre plans** : coupes franches, le mouvement vient des éléments qui entrent. Seuls effets autorisés : glitch (rupture, danger) et fondu au noir avant la phrase finale.
- Suivi de progression permanent en haut à droite (comme le C-O-M-P-A-S de la référence) : N petits carrés numérotés, le courant en blanc, les terminés en vert avec coche. Pastille « Obstacle N · Nom » en haut à gauche. Le nombre de carrés suit le nombre de parties de la vidéo.
- Numéros de partie : grand « 01 » en serif très estompé + titre gras/italique + tampon incliné.
- **Sous-titres** : 3 à 5 mots, Inter Bold, centrés en bas, mot-clé en vert menthe ; sur fond clair ou grille, dans une pastille sombre. Ils suivent la voix mot à mot. En vertical : pastille sombre, zone centrale, hors des boutons TikTok/Instagram.

### Rythme
- Un nouvel élément à l'écran toutes les 2 secondes environ. Jamais d'image immobile.
- Plans de 6 à 8 s. Calculs et chiffres : lents, un élément à la fois au rythme de la voix. Conclusion : accélère puis s'arrête net sur la phrase finale (1 s de noir).
- **Chaque élément apparaît exactement sur le mot prononcé**, jamais avant (transcription mot à mot, `transcrire.py`).
- Images : jamais en succession aléatoire. Une image n'apparaît que si le mot correspond, avec un son.

### Son
- Voix à 0 dB, **uniquement la voix d'origine fournie** (jamais de TTS, ElevenLabs ou voix de remplacement sauf demande explicite). On retire les doublons, hésitations et sons parasites.
- Effets Mixkit entre −15 et −20 dB, **jamais plus d'un par seconde**, uniquement sur un événement visible (apparition, coche, tampon, erreur). Pas de « ting » décoratif.
- Impact fort (S5) 3 fois maximum par vidéo, carton d'ouverture (S6) une seule fois.
- Musique de fond continue, discrète (−22 à −26 dB sous la voix), coupée 1 s avant la phrase finale.
- Sons utilisés : `projet_obstacles_chine/audio/sfx/` (S1 à S20, identifiants dans `ids.json`), musique dans `audio/music/`.
- Niveau final : −16 LUFS en 16:9, −14 LUFS en vertical.

### Technique
- Rendu Python (Pillow + NumPy) envoyé à ffmpeg (libx264, AAC 192 k, faststart), 4 processus en parallèle. Grain **fixe** (un grain animé fait exploser le poids du fichier).
- Garder chaque fichier sous 100 Mo (limite GitHub).
- 16:9 YouTube = 1920 × 1080, 30 i/s. Vertical = 1080 × 1920.

## 2. Ce qui CHANGE à chaque vidéo : le concept des animations

À partir du texte de la voix off, on invente pour chaque scène la métaphore visuelle qui illustre ce qui est dit, avec les composants ci-dessus. Exemples déjà faits :
- « un fournisseur sérieux, un intermédiaire, de fausses images » → 3 cartes.
- « le coût réel = produit + transport + douane… » → la formule se construit terme par terme.
- « 3 $ + 2 $ = 5 $ » → compteurs qui s'additionnent, le « 3 $ » se barre.
- « la marge réelle devient faible » → barre de marge qui fond à chaque frais.
- « avance par étapes » → escalier de 4 marches.
- « rejoins ma chaîne » → bouton S'abonner cliqué par le curseur.

Règles pour inventer une animation :
1. Un concept par phrase-clé, pas plus.
2. Le visuel doit correspondre exactement au mot dit.
3. Équilibrer texte et images (ni tout écrit, ni succession d'images).
4. Aucun chiffre, résultat ou revenu inventé. Les exemples chiffrés viennent de la voix off, ou sont présentés comme exemples.
5. Visages : faceless = aucun visage identifiable. Logos réels autorisés. Données personnelles floutées. Contenu IA étiqueté.

## 3. Variantes

### Faceless (cas de la vidéo de référence)
Tout est carte, texte, tampon, icône animée et image posée dans un cadre. Les vidéos extérieures ne sont pas utilisées sauf demande.

### Facecam (à construire au premier besoin, même style)
Comme la vidéo de référence de départ (« Claude vient de changer Google Ads ») :
- La personne à l'écran en plan fixe, étalonnage vert-froid légèrement désaturé, vignettage.
- Sous-titres 3 à 5 mots en bas, mot-clé en vert ; suivi de progression en haut à droite et pastille « Étape N · Nom » en haut à gauche.
- Alternance avec les cartes d'interface en plein écran (même style que ci-dessus) sur chaque idée forte : un nouvel élément toutes les 2 s, jamais plus de ~15 s de face caméra sans carte.
- Même fonds, mêmes polices, mêmes tampons, même règles de son.

## 4. Méthode de travail pour une nouvelle vidéo

1. Recevoir la voix (et le dossier Drive). Examiner chaque fichier avant de l'utiliser.
2. Nettoyer la voix (doublons, hésitations, sons parasites) : inspirer de `projet_obstacles_chine/nettoyer_voix.py`. Garder l'original intact.
3. Transcrire mot à mot : `transcrire.py` (faster-whisper medium, audio décodé par ffmpeg en f32 16 kHz).
4. Écrire le storyboard (une fonction `@scene("phrase d'ancrage")` par scène dans une copie de `exemple_long_16x9.py`), avec le concept d'animation propre à cette vidéo.
5. Aperçus : `python3 build_xxx.py --frames t1 t2 …`, vérifier chevauchements et textes coupés avant le rendu complet.
6. Rendu, vérification (durée, niveau sonore, quelques images), export dans le projet.
7. Rédiger le plan de montage, signaler les problèmes (licences, voix, ressources manquantes).
8. **Ne jamais publier** sans demande. Proposer titre, description, hashtags quand elle le demande.
9. Commit et push sur la branche de la session, fichiers < 100 Mo.

## 5. Points d'attention rappelés à chaque fois
- Licence de la voix : une voix clonée avec XTTS est non commerciale. Prévenir, et rappeler la case « contenu synthétique » sur YouTube.
- Les clips vidéo Mixkit étiquetés « Restricted » sont interdits en usage commercial.
- Les animations de 150 px du Drive ne s'affichent qu'en petite icône dans une carte, jamais en plein cadre.
