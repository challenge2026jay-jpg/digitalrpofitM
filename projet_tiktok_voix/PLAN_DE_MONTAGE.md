# TikTok « Quelle plateforme chinoise choisir ? » : montage réalisé

Fichier : `export/plateformes_chine_tiktok_9x16.mp4` (1080 × 1920, 30 i/s, 2 min 50 s, son à −14 LUFS). Rien n'a été publié.

Modèle : `modele_video/` (« Les 7 obstacles »), sans changer le style. Seul le concept des animations est propre à cette vidéo.

## Ressources
- **Voix** : `audio/voix_off_tik_tok.wav`, le fichier envoyé, utilisé en entier, sans coupe. Aucun audio du Drive.
- **Drive « Dossier plateformes »** : logos de toutes les plateformes citées ; animations Motion Cuts (5 à 9,8 s), Floating e-commerce mockup, Quality Control, e-Commerce UI, Delivery 3D, World monuments, entrepôt 3D (« Freu mich auf dich »), WhatsApp (3 à 8,2 s, pour l'appel à l'action) ; images comparaison, paiement, poignée de main, entrepôt, livraison.
- **Non utilisés** : logo JD.com et animation LinkedIn (non cités dans la voix) ; animations usine de vaccins, voiture, interface « Parallax » et image « You have €50 » (sans lien avec le texte). Pour l'animation WhatsApp, j'ai retiré le début (cartons avec logos Amazon et Mercado Livre) et la fin (texte « Shopee, Amazon & Mercado Livre », en portugais).
- **Sons** : kit Mixkit S1 à S20 (`audio/sfx`), un seul effet par seconde au maximum, toujours sur un élément qui apparaît. Musique Mixkit discrète, 24 dB sous la voix.

## Storyboard
| # | Temps | Ce qu'on voit |
|---|---|---|
| 1 | 0:00.0 – 0:05.0 | Accroche : animation « Motion Cuts » (personnage qui hésite, « ??? »), titre « commander en Chine pour la RDC ? », pastille « quelle plateforme choisir ? » |
| 2 | 0:05.0 – 0:11.8 | Logos Alibaba.com, 1688, AliExpress, Taobao sur chaque nom + tampon rouge PAS LA MÊME CHOSE |
| 3 | 0:11.8 – 0:15.3 | Fond noir, glitch, alerte : « mauvaise plateforme = beaucoup d'argent perdu » (impact S5) |
| 4 | 0:15.3 – 0:21.5 | Animation « Floating e-commerce mockup » + « laquelle choisir selon ton objectif » |
| 5 | 0:21.5 – 0:30.5 | Cas 01 (suivi 1/4) + tampon B2B, puis logos Alibaba.com, Made-in-China, Global Sources |
| 6 | 0:30.5 – 0:36.7 | Tampon B2B + animation « Quality Control » (usine) + fabricants, grossistes, acheteurs étrangers |
| 7 | 0:36.7 – 0:41.2 | Checklist cochée au curseur : devis, échantillons, quantité minimale |
| 8 | 0:41.2 – 0:44.3 | Pastille « Fournisseur vérifié » + « ≠ garantie » en rouge |
| 9 | 0:44.3 – 0:51.1 | Image comparaison + Fournisseur A/B/C, puis image paiement + Trade Assurance (commande officielle) |
| 10 | 0:51.1 – 0:59.5 | Cas 02 + tampon TEST, puis logos AliExpress et DHgate |
| 11 | 0:59.5 – 1:04.7 | Animation « e-Commerce UI » (achat sur téléphone) + à l'unité, échantillon, le produit plaît ? |
| 12 | 1:04.7 – 1:12.7 | Fond grille : « prix affiché ≠ prix final » + livraison, douane, taxes, livraison locale + animation Delivery 3D |
| 13 | 1:12.7 – 1:21.3 | Cas 03 + tampon AGENT, puis logos 1688, Taobao, Tmall, Pinduoduo |
| 14 | 1:21.3 – 1:31.4 | Prix très intéressants ✓ puis checklist rouge : faits pour les Chinois, interface en chinois, yuans, pas de livraison vers l'Afrique + animation globe |
| 15 | 1:31.4 – 1:41.5 | Image poignée de main + agent d'achat / transitaire + tampon PAS AUTOMATIQUEMENT FIABLE, puis checklist nom, références, devis détaillé |
| 16 | 1:41.5 – 1:48.5 | Cas 04 + tampon YIWU, logo Yiwugo, animation entrepôt 3D sur « marché de gros » |
| 17 | 1:48.5 – 1:54.6 | Image entrepôt + repérer des produits, demander des devis + tampon PAS FORCÉMENT UNE USINE |
| 18 | 1:54.6 – 2:18.5 | « La méthode en 5 points » : checklist cochée sur chaque numéro, une image par étape |
| 19 | 2:18.5 – 2:35.9 | Fond grille : 3 $ + 2 $ + 1 $ = 6 $, revendu 8 $ → 2 $ seulement |
| 20 | 2:35.9 – 2:45.4 | Fond crème : la meilleure plateforme ≠ le prix le plus bas → ton objectif, ton budget, la logistique |
| 21 | 2:45.4 – 2:49.8 | Appel à l'action : « Enregistre la vidéo », animation WhatsApp du Drive, bouton S'abonner cliqué |

## Points à vérifier avant de publier
- La voix prononce mal quelques mots. Les sous-titres affichent le bon texte :
  - au début, on entend « Le commander en Chine » au lieu de « Tu veux commander » ;
  - « propre bruit » pour « propre produit » ;
  - « des Ashgate » pour « DHgate » ;
  - « Yougo » pour « Yiwugo » et « Yiwu » ;
  - « L'évaluation de ton produit » pour « Ton produit coûte 3 dollars ».

  Si ces passages te gênent, il faut réenregistrer ces phrases.
- Si la voix est générée par IA, active la mention « contenu généré par IA » sur TikTok.
- Les montants (3 $, 2 $, 1 $, 6 $, 8 $) sont ceux de la voix off, présentés comme un exemple.

## Refaire le rendu
```bash
python3 transcrire.py
python3 build_tiktok.py --frames 10 60   # aperçus
python3 build_tiktok.py                  # vidéo complète
```
