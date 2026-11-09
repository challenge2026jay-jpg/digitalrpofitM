#!/usr/bin/env python3
"""Prépare les vrais écrans de l'appli tirés de vidéos virales (analyse) :
retire le visage du créateur, ses sous-titres et ses annotations, floute les données personnelles.

    python3 prep_ecrans.py <dossier_images_yayo> <dossier_images_cc>

Sources (images de l'interface WeChat / Pinduoduo, une par étape) :
  - TikTok @yayoservices 7538518611388943621 (WeChat en français, 2 images/s)
  - TikTok @connectchineafrique 7546282348308958469 (achat Pinduoduo, 1 image/s ; visage coupé)
"""
import sys
from PIL import Image, ImageFilter

YAYO, CC = sys.argv[1], sys.argv[2]
OUT = "assets/ecrans/"

def blur(im, boxes):
    for x0, y0, x1, y1 in boxes:
        b = (int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(18)), b[:2])
    return im

# nom -> (source, numéro d'image, zones à flouter (x0,y0,x1,y1 en 0–1), recadrage vertical (y0,y1))
SRC = {
    "wx_decouvrir.png":  (YAYO, 36,  [(0.81, 0.098, 0.93, 0.142), (0.45, 0.172, 0.57, 0.215)], None),            # miniatures Moments / Chaîne
    "wx_moi.png":        (YAYO, 47,  [(0.0, 0.03, 1.0, 0.175)], None),              # profil du créateur
    "wx_parametres.png": (YAYO, 51,  [], None),
    "wx_generalites.png": (YAYO, 59, [], None),
    "wx_gerer.png":      (YAYO, 100, [], None),
    "wx_activer.png":    (YAYO, 113, [], None),
    "wx_active_ok.png":  (YAYO, 120, [], None),
    "wx_decouvrir2.png": (YAYO, 135, [(0.81, 0.098, 0.93, 0.142), (0.45, 0.172, 0.57, 0.215)], None),
    "wx_miniprog.png":   (YAYO, 142, [], None),
    "pdd_chinois.png":   (YAYO, 163, [], None),
    "pdd_menu.png":      (YAYO, 167, [(0.0, 0.46, 1.0, 0.62)], None),              # contacts « Transférer à »
    "pdd_francais.png":  (YAYO, 175, [], None),
    "cc_produit.png":    (CC, 100, [(0.0, 0.80, 1.0, 0.88)], (0.15, 1.0)),         # pseudo des acheteurs ; visage coupé
    "cc_taille.png":     (CC, 130, [(0.0, 0.0, 1.0, 0.13)], (0.15, 1.0)),          # adresse (après recadrage)
    "cc_paye.png":       (CC, 160, [], (0.15, 0.70)),                              # sous-titres du créateur coupés
}

for name, (d, i, boxes, crop) in SRC.items():
    im = Image.open(f"{d}/f_{i:03d}.png").convert("RGB")
    if crop: im = im.crop((0, int(crop[0] * im.height), im.width, int(crop[1] * im.height)))
    blur(im, boxes).save(OUT + name)
    print(name, im.size)
