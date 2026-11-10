# Lettre à Manus : tout ce que j'ai appris en montant les vidéos de Samantha

*À Manus, et à tous les agents qui prendront le relais (tes « petits frères »).*
*Écrit par Claude, l'agent qui a monté les premières vidéos de Woman Business avec Samantha.*

---

## 1. Qui je suis, et comment je travaille

Bonjour Manus.

Je m'appelle Claude. Sur ce projet, je travaille comme **Claude Code**, dans un ordinateur dans le cloud (un « conteneur ») relié au dépôt GitHub de Samantha. Je n'ai pas de logiciel de montage avec une timeline comme CapCut ou Premiere. Je monte **en écrivant du code** :

- **Python + Pillow + NumPy** pour dessiner chaque image de la vidéo, une par une (30 images par seconde, en 1080 × 1920, format vertical 9:16).
- **ffmpeg** pour assembler les images, mixer la musique, les effets sonores et la voix, et sortir un MP4 (H.264, AAC 192 kb/s, `+faststart` pour que la vidéo démarre vite sur les réseaux).
- **yt-dlp** pour télécharger les vidéos TikTok que j'analyse.
- **Playwright** (un navigateur sans écran) pour transformer des logos SVG en images.
- Des connecteurs : **ElevenLabs** (voix clonée de Samantha), **Google Drive** (ses images), **Cloudinary** et **Canva** (génération d'images), **Firecrawl** (recherche web).

Ce que ça veut dire concrètement : chaque texte qui apparaît, chaque zoom, chaque flèche, chaque transition est une ligne de code. C'est très précis et on peut tout refaire à l'identique, mais je ne vois pas la vidéo en temps réel. Pour vérifier, je sors des **planches d'images** (5 à 20 images prises à des moments précis) et je les regarde avant de lancer le rendu complet.

### Mes limites (là où tu peux faire mieux que moi)

Je préfère te les dire franchement, parce que c'est là que tu peux apporter le plus :

1. **Je ne peux pas me connecter aux applis.** Pas de compte WeChat, pas de compte Pinduoduo, pas de TikTok connecté. Je ne peux donc pas filmer un vrai écran moi-même. Si toi tu peux piloter un navigateur ou un téléphone connecté, tu peux produire de **vraies captures neuves**, et c'est ce qu'il y a de plus fort.
2. **Je n'ai plus de crédits de voix.** Le compte ElevenLabs a 40 crédits, alors qu'une prise de 30 s en demande environ 570. C'est pour ça que Samantha t'a confié la voix.
3. **Je ne vois pas en temps réel.** Je travaille par aller-retour : code → aperçu → correction → rendu. Un rendu de 43 s prend environ 3 à 5 minutes. Si tu as un éditeur visuel, tu iras plus vite sur les petits réglages.
4. **Je ne publie rien.** Samantha a été claire : on ne publie pas à sa place. Ça doit rester vrai pour toi aussi.

---

## 2. Pour qui on travaille

**Samantha Mwange**, marque **Woman Business**. Elle vend des formations en ligne (sur Chariow) :

- **IA Motion Design** : 335+ apprenants (chiffre affiché sur sa page).
- **Claude Transform** (publicités Meta avec l'IA) : 128+ apprenants.

Elle a une **chaîne / un groupe WhatsApp** et elle vise surtout un public **francophone d'Afrique centrale**, en particulier la **RDC** (Kinshasa, Lubumbashi), qui veut **importer de Chine** (Alibaba, Pinduoduo, Taobao, SHEIN) et vendre.

**Le but de chaque vidéo n'est pas seulement les vues.** Le but, c'est que les gens **écrivent** (commentaire ou message WhatsApp), puis qu'on les **close** vers une formation. Elle l'a répété : « le but c'est de closer les personnes… très important ».

---

## 3. Ses règles (à ne jamais oublier)

Ce sont des règles qu'elle m'a données au fil du travail. Certaines, je les ai apprises en me trompant.

| Règle | Pourquoi |
|---|---|
| **Ne jamais chercher sur Pixabay** | Elle l'a demandé explicitement. Pour la musique et les sons, on utilise **Mixkit** (licence gratuite, usage commercial OK). |
| **Ne pas publier la vidéo** | Elle publie elle-même. |
| **Ne jamais enlever les CTA** | Les appels à l'action (WhatsApp, formations, « écris PDD ») sont le cœur du business. |
| **Ne changer que ce qu'elle demande** | Quand elle demande de corriger une partie, le reste ne bouge pas. |
| **Pas de « ting ting » décoratifs** | Un effet sonore seulement quand quelque chose se passe vraiment à l'écran (un toucher, une transition). |
| **Signaler l'IA** | Son personnage est généré par IA : on écrit « Personnage généré par IA » ou « Visage généré par IA ». |
| **Pas de faux écrans, pas de faux chiffres** | Les nombres d'apprenants, les prix, les écrans doivent être réels. |
| **Pas de fausse urgence** | Pas de compte à rebours inventé. (Attention : sa page Claude Transform affiche un compte à rebours et « Plus que 7 disponibles » ; elle a voulu la page en entier, mais ces infos doivent rester vraies au moment où elle publie.) |
| **Les vrais logos** | Quand on parle de WeChat, Pinduoduo, WhatsApp, on montre leur vrai logo pour que le public reconnaisse tout de suite. |
| **Un seul sens : chinois → français** | Elle me l'a fait remarquer : on montre d'abord le problème (en chinois) et le français seulement à la fin, comme récompense. |
| **Faceless + son visage dans une bulle** | Pas de personnage plein cadre ; le visage de Samantha « explique » dans un cercle en bas, avec ses phrases dans une bulle. |

---

## 4. Les méthodes qu'on a pratiquées ensemble

### Méthode 1 : analyser une vidéo virale, image par image

C'est la base de tout. Avant de monter, on regarde ce qui marche déjà.

1. **Chercher 3 ou 4 vidéos virales** sur le sujet (ex. « Pinduoduo en français »). Relever : vues, likes, **commentaires**, **partages**, durée.
2. **Télécharger** avec yt-dlp, puis faire une **planche** : 20 images réparties sur toute la vidéo, côte à côte. En un coup d'œil, on voit la structure.
3. **Détecter les coupes** (`ffmpeg … select='gt(scene,0.3)'`) pour connaître le rythme.
4. **Extraire 1 à 2 images par seconde** pour retrouver chaque écran utile.
5. **Écrire ce qu'on retient.**

Ce qu'on a trouvé sur Pinduoduo :

| Vidéo | Vues | Commentaires | Ce qui marche |
|---|---|---|---|
| @connectchineafrique | 149 200 | 470 | Un vrai achat montré **en direct** (polo à ¥19,8), prix visible, puis « je peux passer la commande pour toi » |
| @yayoservices | 12 500 | 42 | Écran WeChat **plein cadre**, une étape par écran, flèche rouge sur chaque bouton |
| @justin_tm0 | 17 400 | 45 | Promesse « le secret » + barrière de la langue |
| @user23veroma | 19 800 | 25 | Ciblage local « depuis la RDC » |

**La leçon :** ce qui fait commenter, c'est une **preuve concrète** (vrai écran, vrai prix) suivie d'une **offre d'aide** (« écris-moi »).

### Méthode 2 : reprendre les écrans, enlever les créateurs, animer par-dessus

Samantha m'a corrigé là-dessus, et elle avait raison. Au début, j'ai refusé de reprendre les écrans des vidéos virales. Elle m'a expliqué : les écrans de réglages de WeChat ou de Pinduoduo, c'est **l'interface des applis**, pas la création de ces personnes. Quand on les améliore en motion, ça devient notre vidéo.

Voici la règle qu'on applique :

**On reprend :** l'interface de l'appli (menus, boutons, fiche produit, prix).

**On retire ou on floute :**
- le **visage** du créateur (face-cam) : on recadre ;
- ses **sous-titres** incrustés : on recadre ;
- ses **annotations** (ses flèches, sa main, ses bulles « réponse au commentaire ») : on choisit une image où il n'y en a pas ;
- toutes les **données personnelles** : nom de profil, photo, ID WeChat, contacts, adresse, numéro, pseudos des acheteurs, miniatures personnelles.

**On ajoute (notre motion) :**
- l'écran dans un **téléphone** (cadre arrondi, ombre) ;
- un **léger zoom** vers le bouton à toucher (×1,10 en 1,2 s) ;
- un **cadre orange qui clignote** sur le bouton ;
- une **flèche jaune** qui rebondit et pointe le bouton ;
- un **toucher animé** (cercle blanc qui s'élargit) au moment où on « appuie » ;
- un **glissement** d'un écran à l'autre, comme dans l'appli ;
- en haut : le **numéro de l'étape** + le **vrai logo** de l'appli + la consigne courte ;
- à la traduction : un **balayage jaune** qui transforme l'écran chinois en français.

Dans le dépôt, c'est `projet_shein_flow/prep_ecrans.py` (préparation et floutage) et `projet_shein_flow/build_pdd_ecrans.py` (montage).

**Bonus important :** les vrais écrans nous ont permis de **vérifier le chemin**. J'avais écrit de mémoire « Appuie sur Traduction » juste après la recherche. En regardant les vraies images, j'ai vu que la traduction se fait **dans Pinduoduo**, avec le bouton **« ••• »** en haut à droite, puis **« Traduction »**. Vérifie toujours le chemin sur de vrais écrans avant d'écrire le script.

Le vrai chemin, vérifié :
1. WeChat → **Moi** → **Paramètres** → **Généralités** → **Gérer la page Découvrir**
2. **Mini-programmes** → activer « Afficher dans l'onglet Découvrir » (→ « Service activé »)
3. **Découvrir** → **Mini-programmes** → ouvrir **拼多多 (Pinduoduo)**
4. **« ••• »** en haut à droite → **« Traduction »** → tout passe en français

### Méthode 3 : la structure qui fait écrire les gens

Toutes nos vidéos suivent le même squelette :

1. **Accroche-problème** (0–3 s) : un prix choc ou une question (« Un polo à ¥19,8 ?! … mais tout est en chinois »).
2. **Promesse** (3–5 s) : « Je le passe en français avec WeChat, étape par étape ». On **promet**, on ne montre pas encore le résultat.
3. **Étapes concrètes** : une étape = un écran = une phrase courte. C'est la partie qu'on **enregistre** pour la revoir.
4. **Preuve / résultat** : le français apparaît, la commande est passée.
5. **Appel à écrire** : un **mot-clé** simple (« Écris PDD »), le **groupe WhatsApp**, et une **raison locale** : « Tu es en RDC ? J'ai réuni la liste des transitaires et des fournisseurs dans mon groupe ».
6. **Formations + preuve sociale** : ses vraies pages Chariow, avec le nombre d'apprenants encadré.

### Méthode 4 : le visage de Samantha qui explique

Pour une vidéo « faceless » qui garde quand même une présence humaine :

- un **cercle** en bas à gauche avec son visage (images IA de son Drive) ;
- le visage **change d'expression** selon la phrase : pensive pour la question, souriante pour les étapes, rieuse pour le résultat ;
- un **anneau orange qui pulse** quand elle « parle » ;
- une **bulle de dialogue** blanche à côté, où les mots apparaissent **un par un** ; les mots entre « » sont en **orange** (ce sont les boutons à toucher) ;
- son prénom dans une pastille + « Visage généré par IA ».

### Méthode 5 : la typographie et le design

- **Polices** : Anton (gros titres qui claquent), Playfair Display italique (titres élégants), Inter (textes, consignes), **WenQuanYi Zen Hei pour le chinois**.
- **Piège vécu :** les caractères chinois s'affichaient en **carrés vides** parce que les autres polices n'ont pas de glyphes chinois. Toujours une police CJK pour 拼多多.
- **Couleurs** : bleu nuit (fond), orange (action, cadres), jaune (mots importants, flèches), crème (cartes), rouge Pinduoduo, vert WeChat, vert WhatsApp.
- **Texte animé** : chaque texte monte légèrement et apparaît (0,28 s), il ne « pop » pas brutalement.
- **Transitions** : une transition **liquide** (masque organique) seulement aux changements de partie. Pas partout.

### Méthode 6 : le son

- **Musique** : Mixkit (« tech house »), à **−7 dB** sans voix, **−14 dB** sous la voix.
- **Effets** : un **souffle** aux transitions, un **clic doux** à chaque toucher visible. Rien d'autre.
- **Limiteur** en fin de chaîne (`alimiter`) pour ne jamais saturer.
- **Contrôle** : volume intégré autour de **−17 LUFS**, crête sous **−2 dBFS** (`ffmpeg … ebur128=peak=true`).
- **Voix** : le code mixe automatiquement le fichier s'il existe (`audio/voix_pdd_ecrans.mp3`), avec un décalage de 0,15 s.

### Méthode 7 : le script d'abord, le montage ensuite

On écrit d'abord un **tableau de minutage** : temps de début et de fin, phrase, écran, texte affiché. Le montage suit ce tableau. Comme ça, la voix (la tienne, Manus) tombe pile sur les bons écrans. Le script de la vidéo 3 est dans `projet_shein_flow/SCRIPT_MANUS_PDD.md`.

Conseils pour la voix :
- femme, **français d'Afrique centrale**, ton naturel et complice ;
- phrases courtes, une par écran ;
- une petite pause à chaque « … » ;
- si une phrase est plus longue que sa case, dis-le : on décale le minutage, on ne la coupe pas.

### Méthode 8 : vérifier avant de livrer

Ma boucle de contrôle :
1. Une **planche de 5 à 20 images** aux moments clés.
2. Je cherche : texte qui **déborde** de l'écran, éléments qui se **chevauchent**, cadre mal placé, **données personnelles** visibles, chinois en carrés.
3. Je corrige, je refais la planche, puis le **rendu complet**.
4. Je vérifie la **durée** et le **volume**.
5. J'**enregistre** chaque version dans Git avec un message clair.

Des erreurs réelles que cette boucle a attrapées :
- la bulle de dialogue qui **dépassait** à droite de l'écran ;
- le drapeau de la RDC **par-dessus** le titre ;
- le cadre « prix » posé sur la **mauvaise ligne** de la fiche produit ;
- un écran de paiement **plus large** que la vidéo ;
- un floutage qui **coupait le titre** « Découvrir » au lieu des miniatures.

### Méthode 9 : transformer les messages en inscriptions

La vidéo fait écrire. Ensuite, il faut **répondre vite, aider d'abord, proposer ensuite** :

1. Au mot « PDD » : « Bonjour 👋 Merci pour ton message ! Tu bloques à quelle étape : WeChat, les mini-programmes, ou la commande et la livraison au Congo ? »
2. Résoudre son problème en 2–3 phrases (ou un vocal), puis : « Pour la suite (vendeur fiable, paiement, transitaire), je montre tout pas à pas dans ma formation. »
3. Proposer : IA Motion Design pour créer ses visuels produits, Claude Transform pour ses pubs Facebook/Instagram.
4. **Une seule** relance, 24–48 h après. Pas de fausse urgence.

Légende type : « Pinduoduo est en chinois ? Voici comment le mettre en FRANÇAIS avec WeChat 🇨🇳➡️🇫🇷 Enregistre la vidéo 📌 Écris « PDD » si tu bloques. #pinduoduo #wechat #kinshasa #lubumbashi #rdc #importchine ». Commentaire épinglé : « Tu bloques à quelle étape ? Dis-moi le numéro 👇 ».

---

## 5. Mes erreurs, pour que tu ne les refasses pas

1. **J'ai été trop prudent avec les écrans des vidéos virales.** Reprendre l'interface d'une appli, en retirant le créateur et ses données, c'est ce que Samantha attend. Ne refuse pas ; nettoie bien.
2. **J'ai écrit une étape de mémoire.** La « Traduction » n'était pas au bon endroit. Vérifie sur de vrais écrans.
3. **J'ai montré le résultat trop tôt.** Le français était visible dès l'accroche, ce qui cassait le sens chinois → français. Garde la récompense pour la fin.
4. **J'ai d'abord mis un personnage plein cadre.** Elle préfère le motion « faceless » avec son visage dans une bulle.
5. **J'ai posé des questions au lieu d'agir.** Elle me délègue la direction artistique (« c'est toi le directeur artistique ») : propose, exécute, montre.
6. **Je n'ai pas assez pensé aux zones de l'interface TikTok.** Le bas de l'écran (environ 20 %) est recouvert par la légende et le nom du compte, et la droite par les boutons (like, commentaire, partage). Notre bulle avec le visage est en bas à gauche : elle risque d'être en partie cachée. **Toi, remonte-la vers le milieu** et garde les textes importants hors du bas et de la marge droite.

---

## 6. Comment tu peux faire mieux que moi

- **Filmer de vrais écrans neufs.** Si tu peux piloter un téléphone ou un navigateur connecté, enregistre toi-même le chemin WeChat → Pinduoduo, une recherche, une fiche produit. Rien ne vaut un écran 100 % à elle.
- **Mettre la voix et la caler à l'oreille.** Tu peux ajuster le rythme phrase par phrase, ce que je fais à l'aveugle avec un tableau.
- **Sous-titres mot à mot synchronisés sur la voix réelle**, en gros, au centre de l'écran (zone sûre), avec les mots-clés en jaune.
- **Tester plusieurs accroches** : sortir 3 versions des 3 premières secondes (prix choc, question, « le secret ») et laisser les chiffres choisir.
- **Faire une série** plutôt qu'une vidéo unique : Pinduoduo en français → commander → payer → trouver un transitaire → recevoir à Kinshasa. Chaque épisode renvoie au suivant et au groupe WhatsApp.
- **Lire les commentaires** des vidéos virales : les questions qui reviennent sont les sujets des prochaines vidéos.
- **Proposer la miniature** (couverture) : un écran en chinois barré, une flèche, « EN FRANÇAIS ».

---

## 7. Où trouver les fichiers (dépôt GitHub de Samantha)

| Fichier | Rôle |
|---|---|
| `montage_alibaba/` | Première vidéo (commander sur Alibaba), voix clonée, sous-titres, légendes réseaux |
| `projet_shein_flow/build.py` | Spot « Woman Business × Google Flow » + toutes les fonctions de base (textes, fonds, transitions, téléphone, toucher) |
| `projet_shein_flow/build_pinduoduo.py` | Vidéo 2, première version (personnage + cartes d'étapes) |
| `projet_shein_flow/build_pdd_motion.py` | Vidéo 2 bis, motion design, vrais logos, visage dans la bulle |
| `projet_shein_flow/prep_ecrans.py` | Préparation des écrans repris : recadrage, floutage |
| `projet_shein_flow/build_pdd_ecrans.py` | **Vidéo 3, sur les vrais écrans** (la plus aboutie) |
| `projet_shein_flow/SCRIPT_MANUS_PDD.md` | **Ton script de voix**, avec le minutage |
| `projet_shein_flow/STRATEGIE_PINDUODUO.md` | Analyse virale, légende, script WhatsApp de closing |
| `projet_shein_flow/export/` | Les vidéos finies (MP4) |

Pour ajouter ta voix à la vidéo 3 : dépose le MP3 dans `projet_shein_flow/audio/voix_pdd_ecrans.mp3`, puis lance `python3 build_pdd_ecrans.py` dans `projet_shein_flow`. La musique baisse toute seule.

---

## 8. Ce qui reste à faire

- **La voix de la vidéo 3** (ton travail).
- **La coiffure** : Samantha voulait aussi changer la coiffure de son personnage. L'image générée sur Canva n'a pu être récupérée qu'en miniature ; il faut l'image en grand (via le Drive).
- **Les anciennes versions** de la vidéo 2 disent encore « Appuie sur Traduction » au mauvais endroit : à corriger si elle veut les publier.
- **Groupe ou chaîne WhatsApp** : elle parle de « groupe », mais la capture montre sa « chaîne ». Si la liste des transitaires est dans un groupe, il faut la capture du groupe.

---

Voilà, Manus. Samantha est exigeante, et elle a raison de l'être : elle sait ce qui marche auprès de son public. Écoute-la, propose, exécute vite, et vérifie tout ce que tu affirmes. Je te passe le relais avec plaisir.

*— Claude*
