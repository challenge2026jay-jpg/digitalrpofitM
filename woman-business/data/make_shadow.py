"""Génère l'ombre de fenêtre (store / croisillons) posée sur toute la vidéo, comme dans la référence.
Image en niveaux de gris : blanc = lumière, gris = ombre. Utilisée en mode « multiply »."""
from PIL import Image, ImageDraw, ImageFilter

W, H = 1800, 2800
img = Image.new("L", (W, H), 255)
d = ImageDraw.Draw(img)
# Lames de store diagonales.
for y in range(-H, 2 * H, 210):
    d.polygon([(0, y), (W, y - 700), (W, y - 700 + 95), (0, y + 95)], fill=150)
# Montant vertical de la fenêtre.
d.rectangle([1180, 0, 1290, H], fill=140)
img = img.filter(ImageFilter.GaussianBlur(26))
img.save("public/img/ombre_fenetre.png", optimize=True)
print("ok")
