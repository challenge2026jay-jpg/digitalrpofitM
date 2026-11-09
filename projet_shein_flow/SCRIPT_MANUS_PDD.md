# Vidéo 3 — « Pinduoduo en français avec WeChat » sur les vrais écrans : script pour Manus

Vidéo : `export/pinduoduo_vrais_ecrans_9x16.mp4` (43 s, 9:16).

## D'où viennent les écrans

On a analysé 3 vidéos virales sur le sujet et repris les **écrans de l'appli** (pas les créateurs) :

| Vidéo analysée | Écrans repris | Retiré / flouté |
|---|---|---|
| @yayoservices — « Pinduoduo en français sur WeChat » | Les 12 écrans du chemin WeChat → Pinduoduo → Traduction | Bulle « réponse au commentaire », ses flèches et sa main, son profil (nom, photo, ID), miniatures, contacts |
| @connectchineafrique — « Comment passer commande sur Pinduoduo » (149 200 vues) | Fiche du polo à ¥19,8, choix de la taille, paiement réussi de ¥19,80 | Son visage (face-cam), ses sous-titres, l'adresse, le pseudo des acheteurs |
| @justin_tm0 / @user23veroma | Accroche (prix + « le secret »), ciblage RDC | — |

Notre motion par-dessus : écran dans un téléphone, léger zoom vers le bouton, cadre orange qui clignote, flèche jaune, toucher animé, numéro d'étape, vrais logos WeChat / Pinduoduo / WhatsApp, visage de Samantha qui « explique » dans la bulle.

## Le vrai chemin (vérifié sur les écrans)

1. WeChat → onglet **Moi**
2. **Paramètres**
3. **Généralités**
4. **Gérer la page Découvrir**
5. **Mini-programmes** → active « Afficher dans l'onglet Découvrir » (→ « Service activé »)
6. Onglet **Découvrir** → **Mini-programmes**
7. Ouvre **拼多多 (Pinduoduo)**
8. Dans Pinduoduo, appuie sur **« ••• »** en haut à droite
9. Appuie sur **« Traduction »** → l'appli passe en français

## Script pour Manus (à copier tel quel)

Consigne de voix : femme, français d'Afrique centrale, ton naturel et complice, rythme vif. Petite pause à chaque « … ».

> Un polo à moins de 20 yuans sur Pinduoduo… mais l'appli est en chinois ?
> Je te la mets en français avec WeChat. Suis-moi !
> Dans WeChat, appuie sur « Moi »,
> puis « Paramètres »,
> « Généralités »,
> et « Gérer la page Découvrir ».
> Touche « Mini-programmes »…
> et active « Afficher dans l'onglet Découvrir ».
> Retourne dans « Découvrir », « Mini-programmes »,
> et ouvre Pinduoduo.
> Appuie sur les trois petits points…
> puis « Traduction »… et voilà : en français !
> Tu choisis ta taille, tu paies… commande passée !
> Tu es en RDC ? J'ai réuni la liste des transitaires et des fournisseurs dans mon groupe WhatsApp.
> Le lien est dans ma bio. Si tu bloques, écris-moi « PDD ».
> Et pour aller plus loin : mes formations.

## Minutage (pour caler la voix)

| Temps | Phrase | À l'écran |
|---|---|---|
| 0,0 – 3,2 s | Un polo à moins de 20 yuans sur Pinduoduo… mais l'appli est en chinois ? | Fiche produit, prix ¥19,8 qui clignote |
| 3,2 – 5,6 s | Je te la mets en français avec WeChat. Suis-moi ! | Avant / après (chinois → français) + logo WeChat |
| 5,6 – 8,0 s | Dans WeChat, appuie sur « Moi », | Étape 1 |
| 8,0 – 10,2 s | puis « Paramètres », | Étape 2 |
| 10,2 – 12,4 s | « Généralités », | Étape 3 |
| 12,4 – 14,8 s | et « Gérer la page Découvrir ». | Étape 4 |
| 14,8 – 17,2 s | Touche « Mini-programmes »… | Étape 5 |
| 17,2 – 20,0 s | et active « Afficher dans l'onglet Découvrir ». | Étape 6 + « Service activé » |
| 20,0 – 22,4 s | Retourne dans « Découvrir », « Mini-programmes », | Étape 7 |
| 22,4 – 24,6 s | et ouvre Pinduoduo. | Étape 8 |
| 24,6 – 27,0 s | Appuie sur les trois petits points… | Étape 9 |
| 27,0 – 29,4 s | puis « Traduction »… et voilà : en français ! | Étape 10 + badge FR |
| 29,4 – 32,4 s | Tu choisis ta taille, tu paies… commande passée ! | Taille L, paiement ¥19,80 |
| 32,4 – 35,6 s | Tu es en RDC ? J'ai réuni la liste des transitaires et des fournisseurs dans mon groupe WhatsApp. | Drapeau RDC, TRANSITAIRES / FOURNISSEURS |
| 35,6 – 38,4 s | Le lien est dans ma bio. Si tu bloques, écris-moi « PDD ». | Capture WhatsApp |
| 38,4 – 43,0 s | Et pour aller plus loin : mes formations. | Pages IA Motion Design et Claude Transform |

Quand l'audio de Manus est prêt : le mettre dans `audio/voix_pdd_ecrans.mp3` et relancer `python3 build_pdd_ecrans.py`.
La musique baisse automatiquement sous la voix. Si une phrase dure plus longtemps que prévu, j'ajuste le minutage.
