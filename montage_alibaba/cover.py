#!/usr/bin/env python3
"""Photo de couverture TikTok (1080x1920) — « Commander sur Alibaba ».

Composition originale. Principes généraux tirés de références Pinterest (voir
README) : titre très gras condensé, contraste jaune/noir, hiérarchie empilée,
mot clé dans un bloc de couleur. Fond : photo du Drive de l'utilisatrice.
Tout le texte reste dans la zone 3:4 centrale (y 240–1680) visible sur la
grille du profil TikTok.

  python3 cover.py  -> export/couverture_tiktok.png (+ variante _b)
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
W, H = 1080, 1920
YELLOW = (255, 214, 10)
INK = (14, 14, 16)
ANTON = "fonts/Anton.woff2"          # Anton, SIL Open Font License 1.1 (Google Fonts)
INTER = "/usr/share/fonts/opentype/inter/"

def f_anton(s): return ImageFont.truetype(ANTON, s)
def f_inter(w, s): return ImageFont.truetype(INTER + f"InterDisplay-{w}.otf", s)

def tw(f, s):
    b = f.getbbox(s); return b[2] - b[0]

def cover_bg(path, cx=0.5, cy=0.5, zoom=1.0):
    im = Image.open(path).convert("RGB")
    sw, sh = im.size
    if sw / sh > W / H:
        rh = sh / zoom; rw = rh * W / H
    else:
        rw = sw / zoom; rh = rw * H / W
    l = min(max(cx * sw - rw / 2, 0), sw - rw); t = min(max(cy * sh - rh / 2, 0), sh - rh)
    return im.transform((W, H), Image.AFFINE, (rw / W, 0, l, 0, rh / H, t), Image.BICUBIC)

def gradient_overlay():
    """Assombrit fortement le haut/centre (zone titre), laisse respirer le bas."""
    g = Image.new("L", (1, H))
    for y in range(H):
        k = y / H
        a = 165 if k < 0.62 else int(165 - (k - 0.62) / 0.38 * 125)
        g.putpixel((0, y), a)
    return Image.merge("RGBA", [Image.new("L", (W, H), 0)] * 3 + [g.resize((W, H))])

def centered(d, y, text, font, fill, stroke=0, sfill=None):
    x = (W - tw(font, text)) // 2
    d.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=sfill)

def render(bg_path, out, cx=0.5, cy=0.5, zoom=1.0):
    bg = cover_bg(bg_path, cx, cy, zoom).filter(ImageFilter.GaussianBlur(1.2))
    im = bg.convert("RGBA")
    im.alpha_composite(gradient_overlay())
    d = ImageDraw.Draw(im)

    # 1. accroche (pilule)
    fk = f_inter("Black", 40)
    k = "TUTO 2026  ·  DE A À Z"
    pw = tw(fk, k) + 64
    x0 = (W - pw) // 2
    d.rounded_rectangle((x0, 300, x0 + pw, 300 + 74), 37, outline=YELLOW, width=4)
    d.text((x0 + 32, 312), k, font=fk, fill=YELLOW)

    # 2. titre — « COMMANDER » blanc
    size = 260
    while tw(f_anton(size), "COMMANDER") > 940:
        size -= 2
    f1 = f_anton(size)
    centered(d, 420, "COMMANDER", f1, (255, 255, 255), 4, INK)

    # 3. mot clé dans un bloc jaune légèrement incliné
    t2 = "SUR ALIBABA"
    size = 220
    while tw(f_anton(size), t2) > 880:
        size -= 2
    f2 = f_anton(size)
    bw, bh = tw(f2, t2) + 90, int(size * 1.3)
    block = Image.new("RGBA", (bw + 40, bh + 40), (0, 0, 0, 0))
    bd = ImageDraw.Draw(block)
    bd.rectangle((20, 20, 20 + bw, 20 + bh), fill=YELLOW)
    bd.text((20 + 45, 20 + 4), t2, font=f2, fill=INK)
    block = block.rotate(-2.2, resample=Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", block.size, (0, 0, 0, 0))
    sh.putalpha(block.getchannel("A").point(lambda v: int(v * 0.55)))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    bx = (W - block.size[0]) // 2
    im.alpha_composite(sh, (bx + 10, 726))
    im.alpha_composite(block, (bx, 706))

    # 4. promesse
    d = ImageDraw.Draw(im)
    f3 = f_inter("Black", 66)
    centered(d, 1070, "sans payer de formation", f3, (255, 255, 255), 3, INK)

    # 5. ligne d'étapes façon marge d'affiche
    f4 = f_inter("ExtraBold", 34)
    steps = ["TRANSITAIRE", "FOURNISSEUR", "PAIEMENT", "COLIS"]
    y = 1500
    total = sum(tw(f4, s) for s in steps) + 3 * 62
    x = (W - total) // 2
    d.line((x, y - 26, x + total, y - 26), fill=(255, 255, 255, 140), width=2)
    for i, s in enumerate(steps):
        d.text((x, y), s, font=f4, fill=(255, 255, 255), stroke_width=2, stroke_fill=INK)
        x += tw(f4, s)
        if i < 3:
            d.text((x + 16, y - 2), "→", font=f4, fill=YELLOW, stroke_width=2, stroke_fill=INK)
            x += 62
    f5 = f_inter("Bold", 30)
    centered(d, y + 62, "4 ÉTAPES · EN MOINS DE 2 MINUTES", f5, YELLOW, 2, INK)

    im.convert("RGB").save(out, quality=95)
    print(out)

if __name__ == "__main__":
    os.makedirs("export", exist_ok=True)
    # A : camion rouge chargé de cartons devant l'entrepôt (Chine)
    render("media/896708975821689274.jpg", "export/couverture_tiktok.png", cx=0.5, cy=0.5, zoom=1.0)
    # B : chargement d'un conteneur, palettes de cartons
    render("media/Custom Canvas Totes – Ready for Your Brand.jpg", "export/couverture_tiktok_b.png", cx=0.5, cy=0.6, zoom=1.0)
