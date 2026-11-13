# Les obstacles des commandes en Chine : montage réalisé

Vidéo YouTube 16:9, 1920 × 1080, 30 i/s, 9 min 09 s, 58 scènes, 100 % faceless.
Fichier : `export/obstacles_chine_16x9.mp4`. Rien n'a été publié.

## Ce qui a été fait

- **Style de la vidéo de référence** : fond vert émeraude en dégradé, fond grille pour les chiffres, fond crème pour les comparaisons, cartes d'interface, titres qui mêlent sans-serif gras et serif italique, tampons inclinés, curseur qui clique, suivi des 7 obstacles en haut à droite, sous-titres de 3 à 5 mots avec le mot-clé en vert menthe.
- **Aucune vidéo extérieure**, comme demandé : les scènes prévues avec des vidéos réelles (ports, usines, entrepôts) sont devenues des scènes de textes animés et de cartes, avec les fichiers du Drive.
- **Les 15 fichiers du Drive sont utilisés** (D1 à D15). Les petites animations (150 px) restent en icônes dans des cartes blanches, jamais en plein écran. D9 n'est utilisée que sur ses 7,5 premières secondes : le logo FasterFreight et la statistique Covid n'apparaissent jamais.
- **Synchronisation au mot** : la voix a été transcrite mot par mot, et chaque carte, coche, chiffre et tampon apparaît sur le mot prononcé.
- **Sons Mixkit S1 à S20** : 133 effets, jamais plus d'un par seconde environ, l'impact S5 trois fois seulement (« combattant », « ton capital », « ton activité »), S6 une fois à l'ouverture.
- **Musique** : 4 pistes Mixkit enchaînées en fondu, environ 25 dB sous la voix, coupée 1 s avant la phrase finale.

## Problèmes trouvés dans la voix off (corrigés)

La voix `voixoff_chine_complete_v2.wav` contient des sons qui ne font pas partie du texte, typiques d'une voix clonée qui « déraille ». Ils ont été retirés (script `nettoyer_voix.py`, l'original reste intact) :

| Moment dans l'original | Son parasite retiré |
|---|---|
| 5:03 – 5:12 | 8 secondes de sons inintelligibles après « Prenons un exemple. » |
| 5:34 | « Eggy » avant « combien me coûtera ce produit… » |
| 5:38 | « Au-dessus » avant « c'est cette question… » |
| 8:18 | « Oh bah » avant « est-ce que ce produit peut se vendre ? » |
| 8:21 – 8:23 | « Yo, c'est… Ah… » |
| 8:27 – 8:30 | « Euh… Yo ? » |

La vidéo passe donc de 9:23 à 9:09. Restent quelques mots un peu déformés que je n'ai pas coupés, parce qu'ils sont au milieu des phrases : « Ça, ici » au tout début (0:02), « y'eux » juste après « chez moi » (0:06), et « Point » après « le fournisseur » (4:33). Les sous-titres affichent le texte correct.

## À savoir avant de publier

- **Licence de la voix** : d'après le plan, la voix a été clonée avec XTTS, dont la licence est non commerciale. Pour une vidéo monétisée ou qui sert à vendre, il faut une autre voix (ta propre voix enregistrée, ou une voix avec licence commerciale).
- **Mention IA** : si tu gardes cette voix synthétique, coche la mention « contenu modifié ou synthétique » sur YouTube.
- **« Mikkit »** : c'est bien Mixkit (mixkit.co) qui a été utilisé pour les sons et la musique.
- **Vidéos Mixkit** : toutes celles que j'ai vérifiées (ports, cargos, entrepôts, usines) sont en licence « Restricted ». De toute façon, aucune vidéo extérieure n'est utilisée.
- **LottieFiles (R8 à R13)** : remplacés par des icônes et des cartes dessinées dans le style de la vidéo (alerte, calendrier, checklist, loupe…).
- Les chiffres affichés sont seulement ceux de la voix off (3 $, 2 $, 5 $, 7 $, 6 $, 8 $, 30 jours, 7 jours). Les valeurs de la fiche produit (100 pièces, noir, 20 × 12 cm…) sont des exemples, présentés comme tels.

## Storyboard réalisé (timecodes de la vidéo finale)

| # | Timecode | Fond | Ce qu'on voit |
|---|---|---|---|
| 1 | 0:00–0:06 | sombre | Accroche : titre, carte « Prix fournisseur 3 $ », boutique D8, tampon FACILE ? |
| 2 | 0:06–0:14 | sombre | « tout paraît simple » puis 4 tuiles (D4, D5, D3, D6) cochées, puis barrées en rouge |
| 3 | 0:14–0:18 | noir | Glitch, « un parcours du combattant » en rouge (impact S5) |
| 4 | 0:18–0:31 | sombre | 5 problèmes, un par plan : D13 DIFFÉRENT, D12 DÉCEVANT, bulles SILENCE, D3 FRAIS, D6 RETARD |
| 5 | 0:31–0:45 | grille | Fond grille : « 1 erreur = capital bloqué », tampon BLOQUÉ, checklist de 3 croix + D3 |
| 6 | 0:45–0:57 | sombre | Sommaire : 7 tuiles numérotées, apparition sur chaque thème cité |
| 7 | 0:57–1:10 | crème | Fond crème : « produit bon marché ? » barré, D11 + BON PRODUIT · BON PRIX · BONS DÉLAIS |
| 8 | 1:10–1:15 | sombre | Numéro 01 « Un fournisseur fiable » + tampon VÉRIFIE ; le suivi 1/7 s'allume |
| 9 | 1:15–1:24 | sombre | D10 (loupe) en zoom lent + 3 pastilles, tampon BELLE PAGE ≠ FIABLE |
| 10 | 1:24–1:31 | sombre | 3 cartes : Sérieux, Intermédiaire, Fausses images |
| 11 | 1:31–1:41 | grille | Fond grille : « le prix le plus bas ≠ la meilleure affaire », barres de prix, PRIX TROP BAS = QUESTIONS |
| 12 | 1:41–1:51 | sombre | Checklist fournisseur 5 lignes, curseur qui coche chaque ligne |
| 13 | 1:51–2:01 | sombre | Téléphone (D12 recadré) « demande une vidéo récente » + 3 pastilles + LE PRODUIT EXISTE |
| 14 | 2:01–2:12 | crème | Fond crème : GROSSE COMMANDE (D9 0-7,5 s) ✗ / PETITE COMMANDE (D4) TEST ✓ |
| 15 | 2:12–2:18 | noir | Fond noir : « Teste le fournisseur avant de tester ton capital » (impact S5) |
| 16 | 2:18–2:24 | sombre | Numéro 02 « La barrière de la langue » + tampon ÉCRIS TOUT |
| 17 | 2:24–2:31 | sombre | D14 + COULEUR, TAILLE, MATIÈRE, MODÈLE, QUANTITÉ, EMBALLAGE sur chaque mot |
| 18 | 2:31–2:40 | crème | Fond crème : D13 + « 100 pièces noires », tampon ERREUR, petite confusion → grosse perte |
| 19 | 2:40–2:54 | sombre | « écris tout » + fiche produit qui se remplit en machine à écrire (S19) |
| 20 | 2:54–3:02 | sombre | D15 (appli de traduction) + photos annotées, mesures, maquette du logo |
| 21 | 3:02–3:16 | sombre | Bulles : récapitulatif envoyé (clic), « Confirmé ✓ », puis D9 + DÉJÀ EXPÉDIÉ |
| 22 | 3:16–3:22 | sombre | Numéro 03 « La qualité du produit » + tampon ÉCHANTILLON |
| 23 | 3:22–3:36 | crème | Fond crème : EN LIGNE (lumière, angle, retouche) ≠ EN VRAI (petit, fragile, fini, matière) |
| 24 | 3:36–3:42 | sombre | D13 « une grande quantité sur une photo ? » puis grand tampon ÉCHANTILLON |
| 25 | 3:42–3:54 | sombre | Checklist échantillon 6 lignes (curseur), puis D8 « avis de clients potentiels » |
| 26 | 3:54–4:01 | sombre | Maquette avant production : le logo tamponne le produit, échantillon personnalisé |
| 27 | 4:01–4:11 | sombre | D12 + « inspection avant expédition » + checklist quantité, état, conformité |
| 28 | 4:11–4:20 | crème | Fond crème : « je veux une bonne qualité » barré, colonnes ACCEPTÉ / REFUSÉ |
| 29 | 4:20–4:27 | sombre | Cartes « Un échantillon : quelques $ » / « Un stock entier raté : ton activité » (impact S5) |
| 30 | 4:27–4:29 | sombre | Numéro 04 « Les frais cachés » + tampon FRAIS CACHÉS |
| 31 | 4:29–4:39 | grille | Fond grille : D2 + carte « Prix affiché 3 $ » + tampon ≠ COÛT RÉEL |
| 32 | 4:39–4:52 | sombre | D11 + 7 étiquettes de frais rouges sur chaque mot |
| 33 | 4:52–5:02 | grille | Fond grille : la formule du coût réel se construit terme par terme |
| 34 | 5:02–5:12 | grille | Fond grille : 3 $ + 2 $ = 5 $, le « 3 $ » se barre, tampon +2 $ |
| 35 | 5:12–5:24 | sombre | Prix de vente 7 $, barre de marge qui fond à chaque frais, « marge réelle très faible » |
| 36 | 5:24–5:32 | sombre | D7 + la question « Combien me coûtera ce produit… ? » |
| 37 | 5:32–5:38 | sombre | Numéro 05 « Les délais de livraison » + tampon MARGE DE SÉCURITÉ |
| 38 | 5:38–5:42 | sombre | Calendrier, 7 jours surlignés, « 7 jours ? » |
| 39 | 5:42–5:49 | sombre | Frise en 4 étapes : D4 production, D5 préparation, D7 transport, D6 livraison |
| 40 | 5:49–6:02 | sombre | Calendrier date promise / date réelle, puis D8 + saisonnier, promotion, commandes encaissées |
| 41 | 6:02–6:11 | sombre | Checklist à demander au fournisseur (curseur) |
| 42 | 6:11–6:28 | sombre | « commande tôt », 30 cases + zone marge de sécurité, pas de date sans confirmation |
| 43 | 6:28–6:30 | sombre | Glitch, numéro 06 rouge « Les arnaques et paiements risqués » + tampon ARNAQUE |
| 44 | 6:30–6:48 | sombre | Signaux d'alerte : 6 lignes rouges sur chaque mot + tampon ARNAQUE |
| 45 | 6:48–7:03 | sombre | D10 + checklist « Protège ton argent » (curseur) + tampon VÉRIFIÉ |
| 46 | 7:03–7:14 | sombre | « tout ton capital à un fournisseur jamais testé ? » puis escalier en 4 marches |
| 47 | 7:14–7:21 | sombre | « la confiance se construit » + 3 belles photos (D13, D10, D12) |
| 48 | 7:21–7:29 | sombre | Numéro 07 « La rentabilité calculée avant » + tampon CALCULE |
| 49 | 7:29–7:38 | sombre | D8 + courbe de tendance qui casse, « tendance ≠ rentable » |
| 50 | 7:38–7:49 | sombre | 4 cartes de questions numérotées |
| 51 | 7:49–8:03 | grille | Fond grille : 3 $ + 2 $ + 1 $ = 6 $, vendu 8 $, 8 − 6 = 2 $ + D2 |
| 52 | 8:03–8:14 | crème | Fond crème : « populaire ≠ rentable », la 1re question se barre, la 2e s'allume |
| 53 | 8:14–8:25 | sombre | D7 + « mais de la méthode », puis « les 3 règles » |
| 54 | 8:25–8:31 | sombre | Règle 1 « Teste » + D4 |
| 55 | 8:31–8:37 | sombre | Règle 2 « Calcule » + D2 |
| 56 | 8:37–8:46 | sombre | Règle 3 « Confirme tout par écrit » + D1 + les 7 éléments |
| 57 | 8:46–9:00 | sombre | Écran de fin : « rejoins ma chaîne », bouton S'abonner cliqué, lien dans la bio |
| 58 | 9:00–9:08 | noir | Fondu au noir, phrase finale mot à mot, musique coupée |

## Refaire ou modifier le montage

```bash
python3 nettoyer_voix.py      # voix sans sons parasites + mots horodatés
python3 build_chine.py        # rendu complet (environ 25 min) -> export/obstacles_chine_16x9.mp4
python3 build_chine.py --frames 75 300   # aperçus PNG à ces secondes, dans cache/apercus
```

- Chaque scène est une petite fonction dans `build_chine.py` (`@scene("phrase d'ancrage")`). Pour changer un texte, une couleur ou le moment d'apparition, on modifie la fonction et on relance le rendu.
- `engine.py` contient le style : couleurs, polices (Inter, Playfair Display, IBM Plex Mono), cartes, tampons, curseur.
- Sons : `audio/sfx/` (S1 à S20, identifiants Mixkit dans `ids.json`). Musique : `audio/music/`.
