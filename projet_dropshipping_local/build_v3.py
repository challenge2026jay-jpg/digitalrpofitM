#!/usr/bin/env python3
"""Rendu V3 — « Dropshipping local » sur la voix originale de Samantha.

Principe (demande de Samantha) : PAS de succession d'images.
  - La base est un fond animé sobre + les mots prononcés en grand au centre (texte cinétique).
  - Une image n'apparaît QUE quand la voix nomme ce qu'elle montre (50 dollars, ebook, tableau de bord,
    boutique, fournisseur, livraison, colis, étranger, accessoires…), dans une carte qui arrive avec un son.
  - WhatsApp, Instagram, TikTok, Facebook : leurs logos sortent pile sur le mot, avec un « pop ».

    python3 build_v3.py --preview 3,46,48   # cache/v3_preview_*.jpg
    python3 build_v3.py --plan              # PLAN_DE_MONTAGE_V3.md
    python3 build_v3.py                     # export/dropshipping_local_v3_9x16.mp4
"""
import os, sys, math, json, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT); sys.path.insert(0, ROOT)
import build_v2 as V                       # voix, mots, sous-titres, polices, lecture vidéo, carton CTA
from build_v2 import W, H, FPS, WORDS, wt, font, anton, script, clamp, ease, ease_out, back, YELLOW, WHITE, INK, CREAM, GREEN

TOTAL = V.TOTAL
MEDIA = "media/"
LOGO_WA = "/home/user/digitalrpofitM/projet_shein_flow/assets/logos/whatsapp_app.png"

def wend(i): return WORDS[i]["end"]

# ------------------------------------------------------------------ ce qui apparaît, et quand (numéros de mots)
# carte : (mot d'arrivée, mot de départ, source, cadrage (cx, cy, zoom), taille (l, h), son d'arrivée)
CARDS = [
    (7,   13,  "17 - AMERICAN DOLLAR.jpg", (0.5, 0.5, 1.0), (760, 860), "papier_froisse_billets"),          # 50 dollars
    (13,  18,  "08 - 233382_medium.mp4", (0.48, 0.6, 1.0), (760, 860), "whoosh_air"),                         # te lancer dans un business
    (25,  39,  "14 - Buisness Ebook _ Buisness Guide.jpg", (0.5, 0.42, 1.0), (760, 860), "page_tournee"),     # produits digitaux
    (39,  47,  "15 - Crush Ebook Sales on Instagram_ Story Strategies for Faceless Accounts.jpg", (0.5, 0.42, 1.0), (760, 860), "page_tournee"),  # ça peut très bien marcher
    (47,  55,  "DASH", None, (940, 520), "whoosh_air"),                                                     # j'ai gagné beaucoup d'argent
    (75,  79,  "18 - 298645019062415060.jpg", (0.5, 0.5, 1.0), (820, 720), "whoosh_air"),                    # commerce physique
    (79,  81,  "32 - WhatsApp Business Marketing Tips for Indian SMEs.jpg", (0.5, 0.5, 1.15), (820, 720), "whoosh_fast"),  # commerce online
    (105, 112, "21 - HIPAA Patient Intake & Forms Blog _ MedForward.jpg", (0.55, 0.45, 1.0), (820, 720), "notification_message_pop"),  # les commerces en ligne
    (112, 121, "20 - Premium Poly Mailer Bags for Ecommerce Shipping _ Tilak Polypack.jpg", (0.55, 0.7, 1.4), (820, 720), "whoosh_air"),  # prennent de plus en plus de place
    (127, 131, "34 - Mobile shop #mobile accessories.jpg", (0.5, 0.45, 1.05), (820, 760), "whoosh_air"),     # produits disponibles
    (131, 135, "02 - 441775044713248418.jpg", (0.5, 0.5, 1.05), (820, 760), "whoosh_fast"),                  # chez un fournisseur
    (135, 140, "13 - 100 Phone Accessories on Amazon_ Cases, Chargers and Earbuds.jpg", (0.5, 0.5, 1.0), (820, 760), "whoosh_air"),  # sans gros stock au départ
    (141, 146, "33 - Traveling light_ This UBeesize tripod is a….jpg", (0.45, 0.45, 1.0), (820, 720), "appareil_photo"),  # tu présentes tes produits
    (152, 163, "pixabay/px_message_telephone.mp4", (0.5, 0.5, 1.0), (820, 640), "clavier_telephone"),        # les clients commandent
    (169, 174, "31 - Quality Packing And Shipping Solutions In Madera.jpg", (0.4, 0.6, 1.55), (820, 720), "whoosh_air"),   # livraison aux clients
    (184, 189, "01 - Young entrepreneur packing order in warehouse.jpg", (0.48, 0.74, 1.8), (820, 720), "papier_tranche_ruban"),  # préparer le colis
    (199, 203, "pixabay/px_billets_mains.mp4", (0.5, 0.5, 1.0), (820, 640), "papier_froisse_billets"),       # peu d'argent
    (203, 211, "pixabay/px_telephone_main_fond_blanc.mp4", (0.5, 0.5, 1.0), (820, 640), "notification_message_pop"),  # tester la demande
    (218, 228, "28 - Amazon Liquidation Pallets.jpg", (0.5, 0.5, 1.0), (820, 720), "whoosh_air"),            # un stock qui risque de ne pas être vendu
    (235, 242, "27 - 878413102300172217.jpg", (0.5, 0.55, 1.0), (820, 720), "whoosh_air"),                  # livraison plus rapide
    (242, 245, "26 - China’s logistics sector grows 6_2% in Q1 2026.jpg", (0.35, 0.5, 1.0), (820, 720), "whoosh_fast"),  # commande à l'étranger
    (249, 252, "13 - 100 Phone Accessories on Amazon_ Cases, Chargers and Earbuds.jpg", (0.35, 0.75, 1.8), (820, 720), "clics_souris"),  # vérifier la qualité
    (252, 258, "32 - WhatsApp Business Marketing Tips for Indian SMEs.jpg", (0.5, 0.42, 1.3), (820, 720), "bulle_message_envoye"),  # échanger avec ton fournisseur
    (259, 266, "17 - AMERICAN DOLLAR.jpg", (0.5, 0.55, 1.15), (760, 860), "papier_froisse_billets"),       # avec 50 dollars
    (268, 271, "13 - 100 Phone Accessories on Amazon_ Cases, Chargers and Earbuds.jpg", (0.5, 0.5, 1.0), (820, 760), "whoosh_air"),  # accessoires
    (291, 296, "19 - 286930_medium.mp4", (0.62, 0.5, 1.0), (820, 600), "touches_calculatrice"),            # calcule ta marge
    (316, 319, "18 - 298645019062415060.jpg", (0.5, 0.5, 1.0), (820, 720), "whoosh_air"),                    # le commerce physique
    (319, 330, "pixabay/px_telephone_manteau.mp4", (0.42, 0.5, 1.0), (820, 720), "whoosh_fast"),             # ou le commerce en ligne
    (332, 339, "03 - Commandes Wholesale de Noël 🎄 _ Coulisses d'une Petite Entreprise Artisanale.jpg", (0.5, 0.5, 1.0), (820, 720), "whoosh_air"),  # commencer progressivement
    (343, 351, "21 - HIPAA Patient Intake & Forms Blog _ MedForward.jpg", (0.55, 0.45, 1.05), (820, 720), "notification_message_pop"),  # ce que tes clients recherchent
    (351, 360, "13 - 100 Phone Accessories on Amazon_ Cases, Chargers and Earbuds.jpg", (0.5, 0.5, 1.0), (820, 720), "whoosh_air"),  # sans gros stock
]
CALC = next(c for c in CARDS if "286930" in c[2])
LOGOS = [("WhatsApp", 146, LOGO_WA), ("Instagram", 147, MEDIA + "38 - 733312751865693445.jpg"),
         ("TikTok", 148, MEDIA + "36 - Logo do tik tok _ Vetor Premium.jpg"), ("Facebook", 151, MEDIA + "37 - Facebook logo.jpg")]
LOGO_END = 152
TITRES = [(84, 87, "Dropshipping", "local")]
ANNEES = [(87, 95, "2023-2024"), (95, 104, "2026")]
ETAPES = (121, 174)                            # barre Fournisseur › Présentation › Commande › Livraison
TROIS = (271, 291)                             # 1 Choisir · 2 Vérifier le prix · 3 Présenter
MARGE = (291, 309)                             # Achat + Livraison + Communication = Ma marge
EMPHASE = [(199, 203, "Commencer petit"), (203, 211, "Tester la demande"), (330, 339, "Étape par étape"),
           (351, 360, "Teste. Apprends. Réinvestis.")]
CTA_W = 360

def card_window(c):
    w0, w1 = c[0], c[1]
    t0 = wt(w0) - 0.12; t1 = wt(w1) - 0.05 if w1 < len(WORDS) else TOTAL
    return t0, max(t1, t0 + 1.0)

# ------------------------------------------------------------------ fond animé (sobre)
_yy, _xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
_rng = np.random.default_rng(7); _grain = [(_rng.normal(0, 1, (H // 2, W // 2)) * 6).astype(np.float32) for _ in range(4)]
def background(t):
    h, w = _yy.shape
    top = np.array((14, 20, 36), np.float32); bot = np.array((24, 14, 40), np.float32)
    v = (_yy / h)[..., None]; col = top * (1 - v) + bot * v
    for (cx, cy, r, c, sp) in ((0.75, 0.22, 0.75, (255, 170, 40), 0.21), (0.18, 0.78, 0.8, (40, 160, 170), 0.17)):
        gx = w * (cx + 0.10 * math.sin(t * sp)); gy = h * (cy + 0.07 * math.cos(t * sp * 1.3))
        d = np.sqrt((_xx - gx) ** 2 + (_yy - gy) ** 2) / (w * r)
        g = (np.clip(1 - d, 0, 1) ** 2.4)[..., None] * 0.38
        col = col * (1 - g) + np.array(c, np.float32) * g
    big = np.asarray(Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)).resize((W // 2, H // 2), Image.BICUBIC), np.float32)
    big = np.clip(big + _grain[0][..., None] * 0.6, 0, 255).astype(np.uint8)   # grain fixe : léger et compressible
    return Image.fromarray(big).resize((W, H), Image.BICUBIC).convert("RGBA")

# ------------------------------------------------------------------ cartes images
_video = {}
@functools.lru_cache(maxsize=None)
def still(path):
    im = Image.open(MEDIA + path).convert("RGB")
    if path.startswith("32 - WhatsApp"):                       # prénom de l'exemple flouté
        x0, y0, x1, y1 = 0.27, 0.215, 0.9, 0.305
        bx = (int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height))
        im.paste(im.crop(bx).filter(ImageFilter.GaussianBlur(14)), bx[:2])
    return im
def card_source(n, c, t):
    path = c[2]
    if path.endswith(".mp4"):
        if n not in _video:
            sh = V.VideoShot.__new__(V.VideoShot)
            full = os.path.normpath(MEDIA + path)
            j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "json", full]))
            w, h = j["streams"][0]["width"], j["streams"][0]["height"]; sc = min(1.0, 1600 / max(w, h))
            sh.ow, sh.oh = int(w * sc) // 2 * 2, int(h * sc) // 2 * 2
            sh.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", "1", "-stream_loop", "-1", "-i", full, "-vf", f"fps={FPS},scale={sh.ow}:{sh.oh}",
                                     "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            sh.n = -1; sh.last = None; _video[n] = sh
        return _video[n].frame(int((t - card_window(c)[0]) * FPS))
    return still(path)

def fit(im, w, h, cx, cy, z):
    sw, sh = im.size
    if sw / sh > w / h: rh = sh / z; rw = rh * w / h
    else: rw = sw / z; rh = rw * h / w
    l = clamp(cx * sw - rw / 2, 0, sw - rw); tp = clamp(cy * sh - rh / 2, 0, sh - rh)
    return im.transform((w, h), Image.AFFINE, (rw / w, 0, l, 0, rh / h, tp), Image.BICUBIC)

DASH = dict(crop=(0, 226, 2000, 900), target=(352, 384, 1000, 674), hl=(455, 500, 728, 575))
def dash_view(t, t0, w, h):
    src = Image.open(MEDIA + "35 - capture_tableau_de_bord_chariow.png").convert("RGB").crop(DASH["crop"]); sw, sh = src.size
    k = ease((t - t0 - 0.45) / 1.0); full = (0, 0, sw, sh); tg = DASH["target"]
    v = [full[j] + (tg[j] - full[j]) * k for j in range(4)]
    vh = (v[2] - v[0]) * h / w; cyv = (v[1] + v[3]) / 2; v[1], v[3] = cyv - vh / 2, cyv + vh / 2
    view = src.crop(tuple(int(x) for x in v)).resize((w, h), Image.LANCZOS)
    if k > 0.95:
        sx = w / (v[2] - v[0]); sy = h / (v[3] - v[1]); a = 0.6 + 0.4 * abs(math.sin((t - t0) * 6)); hl = DASH["hl"]
        ImageDraw.Draw(view).rounded_rectangle(((hl[0] - v[0]) * sx - 14, (hl[1] - v[1]) * sy - 12, (hl[2] - v[0]) * sx + 14, (hl[3] - v[1]) * sy + 12),
                                               18, outline=YELLOW if a > 0.8 else (230, 185, 30), width=9)
    return view

def paste_card(base, img, cx, cy, k_in, k_out, rot0=-4):
    """Carte arrondie avec ombre : arrive en grossissant (léger dépassement), repart en s'effaçant."""
    w, h = img.size; r = 38
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    pad = 60; c = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    shd = Image.new("RGBA", c.size, (0, 0, 0, 0)); ImageDraw.Draw(shd).rounded_rectangle((pad, pad + 24, pad + w, pad + h + 24), r, fill=(0, 0, 0, 150))
    c.alpha_composite(shd.filter(ImageFilter.GaussianBlur(26)))
    c.paste(img, (pad, pad), m)
    ImageDraw.Draw(c).rounded_rectangle((pad, pad, pad + w - 1, pad + h - 1), r, outline=(255, 255, 255, 70), width=3)
    s = (0.72 + 0.28 * back(k_in)) * (1 - 0.08 * k_out); a = clamp(k_in * 3) * (1 - k_out)
    rot = rot0 * (1 - ease_out(k_in))
    c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.BICUBIC)
    if rot: c = c.rotate(rot, Image.BICUBIC, expand=True)
    if a < 1: c.putalpha(c.getchannel("A").point(lambda v: int(v * a)))
    base.alpha_composite(c, (int(cx - c.width / 2), int(cy - c.height / 2 + (1 - ease_out(k_in)) * 70)))

CARD_CY = 690
def draw_cards(base, t):
    shown = 0.0
    for n, c in enumerate(CARDS):
        t0, t1 = card_window(c)
        if not (t0 <= t < t1 + 0.25): continue
        k_in = clamp((t - t0) / 0.38); k_out = clamp((t - t1) / 0.25)
        w, h = c[4]
        if c[2] == "DASH": img = dash_view(t, t0, w, h)
        else:
            cx, cy, z = c[3]; z *= 1 + 0.05 * clamp((t - t0) / max(1, t1 - t0))
            img = ImageEnhance.Contrast(fit(card_source(n, c, t), w, h, cx, cy, z)).enhance(1.05)
        paste_card(base, img, W // 2, CARD_CY, k_in, k_out)
        shown = max(shown, ease_out(k_in) * (1 - k_out))
    return shown

@functools.lru_cache(maxsize=None)
def logo_img(path, size=250):
    im = Image.open(path).convert("RGBA")
    if path.endswith("Facebook logo.jpg"):                     # garder le carré bleu, sans le blanc autour
        a = np.asarray(im.convert("RGB")).astype(int); mask = (a.sum(2) < 600)
        ys, xs = np.where(mask); im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    im = im.resize((size, size), Image.LANCZOS)
    m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), int(size * 0.22), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0)); out.paste(im, (0, 0), m); return out

def draw_logos(base, t):
    if not (wt(LOGOS[0][1]) - 0.1 <= t < wt(LOGO_END) + 0.2): return 0
    k_out = clamp((t - wt(LOGO_END)) / 0.2); shown = 0
    pos = [(W // 2 - 165, 560), (W // 2 + 165, 560), (W // 2 - 165, 890), (W // 2 + 165, 890)]
    for (name, wi, path), (x, y) in zip(LOGOS, pos):
        k = (t - wt(wi) + 0.06) / 0.32
        if k <= 0: continue
        s = back(k); a = clamp(k * 3) * (1 - k_out)
        lg = logo_img(path); sh = Image.new("RGBA", (lg.width + 80, lg.height + 80), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((40, 58, 40 + lg.width, 58 + lg.height), 55, fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(18)); sh.alpha_composite(lg, (40, 40))
        sh = sh.resize((max(1, int(sh.width * s)), max(1, int(sh.height * s))), Image.BICUBIC)
        if a < 1: sh.putalpha(sh.getchannel("A").point(lambda v: int(v * a)))
        base.alpha_composite(sh, (int(x - sh.width / 2), int(y - sh.height / 2)))
        shown = 1
    return shown * (1 - k_out)

# ------------------------------------------------------------------ éléments graphiques (texte)
def in_words(t, w0, w1):
    t0 = wt(w0) - 0.05; t1 = wt(w1) - 0.08 if w1 < len(WORDS) else TOTAL
    return t0, t1, (t0 <= t < t1)

def draw_graphics(base, t, busy_cards=0.0):
    present = 0.0
    for w0, w1, l1, l2 in TITRES:
        t0, t1, on = in_words(t, w0, w1)
        if on: V.draw_titre(base, t, t0, t1, l1, l2); present = 1
    for w0, w1, y in ANNEES:
        t0, t1, on = in_words(t, w0, w1)
        if on:
            d = ImageDraw.Draw(base, "RGBA"); sz = 280
            while d.textlength(y, font=anton(sz)) > 960: sz -= 10
            f = anton(sz); w = d.textlength(y, font=f)
            a = ease_out((t - t0) / 0.2) * clamp((t1 - t) / 0.15); k = back((t - t0) / 0.35)
            col = (205, 198, 186) if "2023" in y else YELLOW; yy = 470 + (1 - k) * 50
            d.text(((W - w) / 2 + 8, yy + 14), y, font=f, fill=(0, 0, 0, int(120 * a)))
            d.text(((W - w) / 2, yy), y, font=f, fill=col + (int(255 * a),)); present = 1
    t0, t1, on = in_words(t, *ETAPES)
    if on: V.draw_etapes(base, t, ease_out((t - t0) / 0.25) * clamp((t1 - t) / 0.2))
    t0, t1, on = in_words(t, *TROIS)
    if on:
        a = ease_out((t - t0) / 0.25) * clamp((t1 - t) / 0.2); d = ImageDraw.Draw(base, "RGBA"); f = font("Black", 72); y = 420
        for i, (s, wi) in enumerate([("Choisir", 271), ("Vérifier le prix", 274), ("Présenter", 285)]):
            k = ease_out((t - wt(wi) + 0.05) / 0.3) * a
            if k <= 0: continue
            cur = i == max(j for j, ww in enumerate((271, 274, 285)) if t >= wt(ww) - 0.05)
            lab = f"{i + 1}   {s}"; tw = d.textlength(lab, font=f); x = (W - tw) / 2 - 40 + (1 - k) * 60
            d.rounded_rectangle((x, y, x + tw + 80, y + 124), 34, fill=(YELLOW if cur else CREAM) + (int(240 * k),))
            d.text((x + 40, y + 18), lab, font=f, fill=INK + (int(255 * k),)); y += 150
        present = 1
    t0, t1, on = in_words(t, *MARGE)
    if on and t > card_window(CALC)[1]:                  # après la calculatrice : le carnet de marge
        a = ease_out((t - card_window(CALC)[1]) / 0.3) * clamp((t1 - t) / 0.2); draw_marge(base, t, a); present = 1
    for w0, w1, s in EMPHASE:
        t0, t1, on = in_words(t, w0, w1)
        if on:
            y = 205 if busy_cards > 0.05 else 560
            V.pill(base, s, W // 2, y - (1 - ease_out((t - t0) / 0.25)) * 20, ease_out((t - t0) / 0.25) * clamp((t1 - t) / 0.15), size=80 if busy_cards > 0.05 else 92); present = 1
    return present

def draw_marge(base, t, a):
    d = ImageDraw.Draw(base, "RGBA"); x0, y0, w, h = 170, 360, 740, 560
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 34, fill=CREAM + (int(246 * a),))
    d.text((x0 + 48, y0 + 34), "Je calcule", font=anton(84), fill=INK + (int(255 * a),))
    rows = [("Achat", 291), ("Livraison", 299), ("Communication", 302)]
    for r, (s, wi) in enumerate(rows):
        b = clamp((t - wt(wi)) / 0.25) * a
        if b > 0: d.text((x0 + 60, y0 + 160 + r * 96), "+ " + s, font=font("Bold", 58), fill=INK + (int(255 * b),))
    b = clamp((t - wt(304) - 0.3) / 0.3) * a
    if b > 0:
        yb = y0 + 160 + 3 * 96
        d.rounded_rectangle((x0 + 40, yb - 6, x0 + w - 40, yb + 88), 24, fill=YELLOW + (int(255 * b),))
        d.text((x0 + 64, yb), "= MA MARGE", font=anton(72), fill=INK + (int(255 * b),))

# ------------------------------------------------------------------ texte cinétique (la voix, en grand)
def chunks():
    out, cur = [], []
    for j, w in enumerate(WORDS):
        cur.append(j); txt = " ".join(WORDS[x]["text"] for x in cur)
        if (len(cur) >= 3 or len(txt) >= 16 or w["text"].endswith((",", ".", "?", "!"))) and not (j in V.MARKS and j + 1 in V.MARKS):
            out.append(cur); cur = []
    if cur: out.append(cur)
    return [(wt(ids[0]) - 0.04, (wt(out[c + 1][0]) - 0.04) if c + 1 < len(out) else wend(ids[-1]) + 0.4, ids) for c, ids in enumerate(out)]
CH = chunks()
_ypos = {"y": 960.0}
def draw_kinetic(base, t, busy):
    if t >= wt(CTA_W) - 0.05: return
    c = next((c for c in CH if c[0] <= t < c[1]), None)
    target = 1290 if busy > 0.05 else 960                       # le texte descend quand une image est à l'écran
    _ypos["y"] += (target - _ypos["y"]) * 0.28
    if not c: return
    t0, t1, ids = c; size = 104 if busy < 0.05 else 78
    f = font("Black", size); gap = int(size * 0.26); d = ImageDraw.Draw(base)
    words = [WORDS[j]["text"] for j in ids]; ws = [d.textlength(w, font=f) for w in words]
    tot = sum(ws) + gap * (len(ws) - 1)
    if tot > 920:
        size = int(size * 920 / tot); f = font("Black", size); gap = int(size * 0.26)
        ws = [d.textlength(w, font=f) for w in words]; tot = sum(ws) + gap * (len(ws) - 1)
    layer = Image.new("RGBA", (int(tot) + 80, int(size * 1.7)), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer); x = 40
    for j, w, wd in zip(ids, words, ws):
        k = (t - wt(j) + 0.03) / 0.16
        if k <= 0: x += wd + gap; continue
        col = YELLOW if j in V.MARKS else WHITE
        wl = Image.new("RGBA", (int(wd) + 40, int(size * 1.7)), (0, 0, 0, 0)); wdd = ImageDraw.Draw(wl)
        wdd.text((20 + size * 0.04, int(size * 0.2) + size * 0.06), w, font=f, fill=(0, 0, 0, 120))
        wdd.text((20, int(size * 0.2)), w, font=f, fill=col + (255,))
        s = 1.18 - 0.18 * ease_out(k)
        if s != 1: wl = wl.resize((int(wl.width * s), int(wl.height * s)), Image.BICUBIC)
        a = clamp(k * 1.6)
        if a < 1: wl.putalpha(wl.getchannel("A").point(lambda v: int(v * a)))
        layer.alpha_composite(wl, (int(x - 20 - (wl.width - wd - 40) / 2), int((layer.height - wl.height) / 2)))
        x += wd + gap
    base.alpha_composite(layer, (int(V.SUB_CX + 20 - layer.width / 2), int(_ypos["y"] - layer.height / 2)))

# ------------------------------------------------------------------ carton final
CTA_IDX = len(V.SHOTS) - 1
def render_cta(t):
    V.cta_bg = lambda: background(t).convert("RGB")
    im = V.render_cta(CTA_IDX, t).convert("RGBA")
    li = 364; k = back((t - wt(li) - 0.8) / 0.35)
    if k > 0:
        lg = logo_img(LOGO_WA, 150); lg = lg.resize((max(1, int(150 * k)), max(1, int(150 * k))))
        im.alpha_composite(lg, (W // 2 - lg.width // 2, 1490 - lg.height // 2))
    return im.convert("RGB")

def frame(t):
    if t >= wt(CTA_W) - 0.05:
        im = render_cta(t)
        dt = t - (wt(CTA_W) - 0.05)
        if dt < 0.25:
            prev = background(t).convert("RGB"); im = Image.blend(prev, im, ease(dt / 0.25))
        return im
    base = background(t)
    bc = draw_cards(base, t)
    busy = max(bc, draw_logos(base, t), draw_graphics(base, t, bc))
    draw_kinetic(base, t, busy)
    for n in list(_video):
        if t > card_window(CARDS[n])[1] + 0.5: _video.pop(n).p.kill()
    return base.convert("RGB")

# ------------------------------------------------------------------ son
def sfx_events():
    ev = [(card_window(c)[0] - 0.02, c[5], -15 if c[5].startswith("whoosh") else -16) for c in CARDS]
    ev += [(wt(wi) - 0.02, "bulle_message_envoye", -12) for _, wi, _ in LOGOS]
    ev += [(wt(87) - 0.1, "whoosh_fast_inverse", -16), (wt(95) - 0.1, "whoosh_air", -16), (wt(84) - 0.1, "whoosh_air", -17),
           (wt(271) - 0.05, "whoosh_air", -19), (wt(363), "clavier_telephone", -22), (wend(374) + 0.3, "validation_douce", -14)]
    return ev
def build_audio(out="cache/mix_v3.wav"):
    inp = ["-i", V.MUSIC, "-i", V.MUSIC, "-i", V.VOICE]
    fc = ["[0:a][1:a]acrossfade=d=3[mm]",
          f"[mm]aresample=48000,atrim=0:{TOTAL},volume='{V.music_expr().replace("0.11*", "0.073*")}':eval=frame,afade=t=in:d=0.3,afade=t=out:st={TOTAL - 1.5}:d=1.5[m]",
          "[2:a]aresample=48000,aformat=channel_layouts=stereo[v]"]
    lab = ["[m]", "[v]"]
    for n, (t, f, g) in enumerate(sfx_events()):
        rev = f.endswith("_inverse"); f = f.replace("_inverse", ""); t = max(0.0, t)
        inp += ["-i", f"audio/sfx/{f}.mp3"]
        fc.append(f"[{n + 3}:a]aresample=48000,aformat=channel_layouts=stereo,{'areverse,' if rev else ''}atrim=0:1.3,afade=t=out:st=0.9:d=0.4,volume={g}dB,adelay={int(t * 1000)}|{int(t * 1000)}[s{n}]")
        lab.append(f"[s{n}]")
    fc.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0:duration=longest,atrim=0:{TOTAL},alimiter=limit=0.89:level=false[o]")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", ";".join(fc), "-map", "[o]", "-ac", "2", out])
    return out

def render(out="export/dropshipping_local_v3_9x16.mp4"):
    mix = build_audio()
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", mix, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
    for n in range(round(TOTAL * FPS)): p.stdin.write(frame(n / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK ->", out, f"({TOTAL:.1f} s)")

def write_plan():
    rows = ["| Phrase prononcée | Visuel | Passage | Son |", "|---|---|---|---|"]
    items = []
    for c in CARDS:
        t0, t1 = card_window(c)
        items.append((t0, " ".join(WORDS[j]["text"] for j in range(c[0], c[1])),
                      "tableau de bord Chariow (capture de Samantha), rapprochement sur le revenu" if c[2] == "DASH" else f"`{os.path.basename(c[2])}` en carte", t1, c[5]))
    for name, wi, path in LOGOS:
        items.append((wt(wi), WORDS[wi]["text"], f"logo {name} (`{os.path.basename(path)}`)", wt(LOGO_END), "pop"))
    for w0, w1, l1, l2 in TITRES: items.append((wt(w0), " ".join(WORDS[j]["text"] for j in range(w0, w1)), f"titre « {l1} {l2} »", wt(w1), "whoosh"))
    for w0, w1, y in ANNEES: items.append((wt(w0), " ".join(WORDS[j]["text"] for j in range(w0, w1)), f"année « {y} » en grand", wt(w1), "whoosh"))
    items.append((wt(ETAPES[0]), "Le dropshipping local … livraison aux clients", "barre Fournisseur › Présentation › Commande › Livraison (l'étape s'allume au mot)", wt(ETAPES[1]), "—"))
    items.append((wt(TROIS[0]), "choisis le produit … premiers clients", "1 Choisir · 2 Vérifier le prix · 3 Présenter", wt(TROIS[1]), "whoosh"))
    items.append((card_window(CALC)[1], "et prévois aussi les frais …", "carnet : Achat + Livraison + Communication = MA MARGE", wt(MARGE[1]), "—"))
    for w0, w1, s in EMPHASE: items.append((wt(w0), " ".join(WORDS[j]["text"] for j in range(w0, w1)), f"pastille « {s} »", wt(w1), "—"))
    items.append((wt(CTA_W), " ".join(WORDS[j]["text"] for j in range(CTA_W, len(WORDS))), "ÉCRIS « LOCAL » EN COMMENTAIRE, zone de commentaire, « Je t'envoie le lien de ma chaîne WhatsApp », logo WhatsApp", TOTAL, "clavier, validation douce"))
    for t0, ph, vis, t1, snd in sorted(items): rows.append(f"| {ph} | {vis} | {t0:.1f}–{t1:.1f} s | {snd} |")
    hdr = (f"# Plan de montage V3 — voix originale\n\nDurée : {TOTAL:.1f} s. Le reste du temps : fond animé sobre et mots prononcés en grand au centre "
           "(mots-clés en jaune). Une image n'apparaît que lorsque la voix nomme ce qu'elle montre.\n\n")
    open("PLAN_DE_MONTAGE_V3.md", "w").write(hdr + "\n".join(rows) + "\n"); print("PLAN_DE_MONTAGE_V3.md écrit")

if __name__ == "__main__":
    if "--plan" in sys.argv: write_plan()
    elif "--preview" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1].split(",")]
        ims = []
        for t in ts:
            _ypos["y"] = 1290 if True else 960
            for k in range(8): frame(max(0, t - (8 - k) / FPS))     # laisse le texte se placer
            ims.append(frame(t).resize((360, 640)))
        for j in range(0, len(ims), 6):
            g = Image.new("RGB", (360 * 6, 640), "white")
            for i, im in enumerate(ims[j:j + 6]): g.paste(im, (i * 360, 0))
            g.save(f"cache/v3_preview_{j // 6}.jpg", quality=85)
        print("ok", TOTAL)
    else: render()
