#!/usr/bin/env python3
"""Spot TikTok 9:16 — « Ta photo… ou ta vidéo ? » (Woman Business × Google Flow).

Rendu 100 % code (Pillow + numpy + ffmpeg) : fond dégradé animé, masques liquides
générés (formes organiques originales), typographie animée, cartes produit.
Timings calés sur les 13 phrases de la voix off (pauses détectées dans audio/voix_off.mp3).

    python3 build.py               -> export/woman_business_flow_9x16.mp4
    python3 build.py --preview 1.0,9.5
"""
import os, sys, math, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
W, H, FPS = 1080, 1920, 30
VO = 0.25                       # décalage de la voix dans la vidéo
TOTAL = 21.6

NAVY, NAVY2 = (14, 27, 61), (6, 12, 30)
ORANGE, CREAM, INK = (242, 140, 40), (246, 238, 228), (16, 18, 28)
YELLOW, WHITE = (255, 214, 10), (255, 255, 255)

# phrases de la voix (début, fin) en secondes dans la piste voix
SEG = [(0.00, 1.13), (1.38, 2.12), (2.72, 3.40), (3.72, 4.45), (4.85, 5.88), (6.33, 6.88), (7.14, 8.67),
       (9.03, 10.18), (10.55, 11.51), (11.85, 12.87), (13.17, 16.70), (16.99, 18.19), (18.39, 19.55)]
def S(i):  # début de la phrase i dans la vidéo
    return SEG[i][0] + VO

# ------------------------------------------------------------------ outils
FD = "fonts/"
def f_play(s): return ImageFont.truetype(FD + "PlayfairDisplay-Italic-900.ttf", s)
def f_play7(s): return ImageFont.truetype(FD + "PlayfairDisplay-Italic-700.ttf", s)
def f_anton(s): return ImageFont.truetype(FD + "Anton.woff2", s)
def f_inter(w, s): return ImageFont.truetype(f"/usr/share/fonts/opentype/inter/InterDisplay-{w}.otf", s)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_io(x): x = clamp(x); return x * x * (3 - 2 * x)
def lerp(a, b, k): return a + (b - a) * k

@functools.lru_cache(maxsize=None)
def img(path): return Image.open("assets/" + path).convert("RGB")

def cover(im, w, h, cx=0.5, cy=0.5, z=1.0):
    sw, sh = im.size
    if sw / sh > w / h: rh = sh / z; rw = rh * w / h
    else: rw = sw / z; rh = rw * h / w
    l = clamp(cx * sw - rw / 2, 0, sw - rw); t = clamp(cy * sh - rh / 2, 0, sh - rh)
    return im.transform((w, h), Image.AFFINE, (rw / w, 0, l, 0, rh / h, t), Image.BICUBIC)

def rmask(size, r):
    m = Image.new("L", size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255); return m

def card(im, r=36, shadow=True, border=None):
    w, h = im.size; pad = 70
    out = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 22, pad + w, pad + h + 22), r, fill=(0, 0, 0, 120))
        out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26)))
    out.paste(im.convert("RGB"), (pad, pad), rmask((w, h), r))
    if border:
        ImageDraw.Draw(out).rounded_rectangle((pad, pad, pad + w - 1, pad + h - 1), r, outline=border, width=4)
    return out

def paste_c(base, im, cx, cy, alpha=1.0, scale=1.0, rot=0.0):
    if scale != 1.0: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BICUBIC)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1.0:
        im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    if alpha > 0: base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def tw(f, s): b = f.getbbox(s); return b[2] - b[0]

@functools.lru_cache(maxsize=None)
def text_img(s, font_key, size, color, stroke=0, scolor=INK, spacing_word=None):
    f = {"play": f_play, "play7": f_play7, "anton": f_anton}.get(font_key)
    f = f(size) if f else f_inter(font_key, size)
    words = s.split(" "); gap = spacing_word if spacing_word is not None else int(size * 0.28)
    w = sum(tw(f, x) for x in words) + gap * (len(words) - 1) + 2 * stroke + 20
    im = Image.new("RGBA", (w, int(size * 1.45)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 10 + stroke
    for word in words:
        d.text((x, int(size * 0.1)), word, font=f, fill=color + (255,), stroke_width=stroke, stroke_fill=scolor + (255,))
        x += tw(f, word) + gap
    return im

def fit_text(s, font, size, color, stroke=0, maxw=960):
    im = text_img(s, font, size, color, stroke)
    while im.width > maxw and size > 20:
        size -= 4; im = text_img(s, font, size, color, stroke)
    return im

def kin(base, s, t, t0, cx, cy, font="play", size=96, color=WHITE, stroke=0, dur=0.28, t1=None, rise=40, maxw=960):
    """Texte qui monte et apparaît (et disparaît avant t1)."""
    if t < t0 or (t1 is not None and t >= t1): return
    k = ease_out((t - t0) / dur); a = k
    if t1 is not None: a = min(a, clamp((t1 - t) / 0.15))
    paste_c(base, fit_text(s, font, size, color, stroke, maxw), cx, cy + (1 - k) * rise, a)

# ------------------------------------------------------------------ fonds et masques
_yy, _xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
def bg_gradient(t, warm=False):
    """Dégradé bleu nuit avec une nappe orange qui dérive lentement (original, généré)."""
    h, w = _yy.shape
    gx = w * (0.75 + 0.18 * math.sin(t * 0.35)); gy = h * (0.25 + 0.12 * math.cos(t * 0.27))
    d = np.sqrt((_xx - gx) ** 2 + (_yy - gy) ** 2) / (w * 0.9)
    glow = np.clip(1 - d, 0, 1) ** 2.2
    base = np.stack([np.full_like(_yy, c) for c in (NAVY2 if not warm else NAVY)], -1)
    top = np.stack([np.full_like(_yy, c) for c in NAVY], -1)
    v = _yy / h
    col = base * v[..., None] + top * (1 - v[..., None])
    col = col * (1 - glow[..., None] * 0.85) + np.array(ORANGE, np.float32) * glow[..., None] * 0.85
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    return im.convert("RGBA")

def bg_cream(t):
    h, w = _yy.shape
    gx = w * (0.2 + 0.1 * math.sin(t * 0.4)); gy = h * (0.78 + 0.05 * math.cos(t * 0.3))
    d = np.sqrt(((_xx - gx) / 1.3) ** 2 + (_yy - gy) ** 2) / (w * 0.8)
    blob = np.clip(1 - d, 0, 1) ** 1.6
    g2x = w * (0.9 - 0.08 * math.sin(t * 0.33)); g2y = h * 0.1
    d2 = np.sqrt((_xx - g2x) ** 2 + (_yy - g2y) ** 2) / (w * 0.7); blob2 = np.clip(1 - d2, 0, 1) ** 1.8
    col = np.ones((h, w, 3), np.float32) * np.array(CREAM, np.float32)
    col = col * (1 - blob[..., None] * 0.9) + np.array(NAVY, np.float32) * blob[..., None] * 0.9
    col = col * (1 - blob2[..., None] * 0.6) + np.array(ORANGE, np.float32) * blob2[..., None] * 0.6
    return Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).convert("RGBA")

_rng = np.random.default_rng(7)
_BLOBS = _rng.uniform(0, 1, (9, 4))
def liquid_mask(p, origin=(1.0, 0.5), w=W, h=H):
    """Masque organique (metaballs) qui envahit l'écran depuis `origin`. p : 0 -> 1."""
    sw, sh = w // 6, h // 6
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    field = np.zeros((sh, sw), np.float32)
    ox, oy = origin[0] * sw, origin[1] * sh
    grow = ease_io(p)
    for (a, b, c, d) in _BLOBS:
        ang = a * 2 * math.pi; dist = (0.1 + 0.9 * b) * grow * max(sw, sh) * 1.1
        bx, by = ox + math.cos(ang) * dist * 0.7, oy + math.sin(ang) * dist
        r = (0.12 + 0.25 * c) * max(sw, sh) * (0.2 + 1.4 * grow)
        field += r * r / ((xx - bx) ** 2 + (yy - by) ** 2 + 1)
    m = np.clip((field - 1.0) * 4 + 0.5, 0, 1) if p < 0.999 else np.ones_like(field)
    return Image.fromarray((m * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).point(lambda v: 255 if v > 127 else 0).filter(ImageFilter.GaussianBlur(1.5))

def ai_tag(base):
    paste_c(base, text_img("Images générées par IA", "SemiBold", 26, WHITE), W - 190, 92, 0.75)

# ------------------------------------------------------------------ éléments préparés
@functools.lru_cache(maxsize=None)
def before_photo():   # photo amateur, mise à la verticale (prise du dessus)
    im = img("robe_photo_avant.png").rotate(-90, expand=True)
    return ImageOps.autocontrast(im, cutoff=0).point(lambda v: int(v * 0.92))

@functools.lru_cache(maxsize=None)
def cards():
    c = {}
    c["avant"] = card(cover(before_photo(), 430, 640), 30)
    c["perso"] = card(cover(img("personnage_planche.png"), 430, 540, 0.5, 0.5), 30)
    c["prompt"] = None
    c["vignette"] = card(cover(before_photo(), 260, 360, 0.5, 0.48, 1.25), 24, border=WHITE + (255,))
    f = img("capture_formation_ia_motion_design.jpg")
    ban = f.crop((26, 385, 618, 603)).resize((960, int(218 * 960 / 592)), Image.LANCZOS)
    c["formation"] = card(ban, 34)
    wa = img("capture_chaine_whatsapp.jpg").crop((40, 110, 1040, 700))
    c["whatsapp"] = card(wa.resize((900, int(590 * 900 / 1000)), Image.LANCZOS), 40)
    c["exasp"] = card(cover(img("exasperation_assise_ordinateur.png"), 820, 1000, 0.5, 0.42), 40)
    jub = cover(img("jubilation_portrait_face.png"), 520, 520, 0.5, 0.36)
    m = Image.new("L", (520, 520), 0); ImageDraw.Draw(m).ellipse((0, 0, 519, 519), fill=255)
    circ = Image.new("RGBA", (520, 520), (0, 0, 0, 0)); circ.paste(jub, (0, 0), m)
    ring = Image.new("RGBA", (560, 560), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((0, 0, 559, 559), fill=ORANGE + (255,))
    ring.alpha_composite(circ, (20, 20)); c["jub"] = ring
    return c

@functools.lru_cache(maxsize=None)
def flow_ui_base():
    """Vraie image de l'interface Google Flow (démo officielle, 3,0 s), dont on remplace les
    ingrédients et le prompt par les nôtres. Présenté à l'écran comme un montage."""
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", "3.0", "-i", "assets/google_flow_demo_ingredients_to_video.mp4",
                                   "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    im = Image.frombuffer("RGB", (1920, 1080), raw, "raw", "RGB", 0, 1).copy()
    a = np.asarray(im).astype(np.float32).copy()
    a[395:525, 200:1910] = a[548:552, 200:1910].mean(axis=0, keepdims=True)   # efface le prompt d'origine
    im = Image.fromarray(a.astype(np.uint8))
    chips = [(180, 603, 545, 828, cover(before_photo(), 365, 225, 0.5, 0.45, 1.6)),
             (568, 603, 930, 828, cover(img("personnage_planche.png"), 362, 225, 0.5, 0.48, 2.6)),
             (953, 603, 1317, 828, cover(img("personnage_planche.png"), 364, 225, 0.5, 0.2, 1.0))]
    for x0, y0, x1, y1, ph in chips:
        im.paste(ph, (x0, y0), rmask((x1 - x0, y1 - y0), 56))
    return im

def flow_ui_card(t, t0):
    base = flow_ui_base().copy(); d = ImageDraw.Draw(base)
    full = "Elle porte cette robe dans un salon lumineux"
    f = f_inter("Regular", 68)
    n = int(len(full) * clamp((t - t0) / 0.85))
    d.text((228, 410), full[:n], font=f, fill=(236, 238, 240))
    if n < len(full) and int(t * 4) % 2 == 0:
        x = 228 + tw(f, full[:n]) + 8; d.rectangle((x, 420, x + 5, 505), fill=(236, 238, 240))
    k = clamp((t - t0 - 0.9) / 0.25)                       # bouton « générer » qui s'active
    r = int(62 * (1 + 0.12 * math.sin(k * math.pi)))
    cx, cy = 1815, 455
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255) if k > 0 else (60, 64, 70))
    col = (20, 22, 26) if k > 0 else (160, 165, 170)
    d.line((cx - 30, cy, cx + 28, cy), fill=col, width=9); d.line((cx + 4, cy - 26, cx + 30, cy, cx + 4, cy + 26), fill=col, width=9)
    crop = base.crop((110, 110, 1920, 880)).resize((960, int(770 * 960 / 1810)), Image.LANCZOS)
    return card(crop, 30, border=WHITE + (255,))

def prompt_card(t, t0):
    full = "« Elle porte cette robe dans un salon lumineux. »"
    n = int(len(full) * clamp((t - t0) / 0.9))
    w, h = 900, 250
    im = Image.new("RGB", (w, h), WHITE); d = ImageDraw.Draw(im)
    d.text((40, 30), "Prompt", font=f_inter("Bold", 30), fill=(120, 120, 130))
    txt = full[:n]; f = f_inter("SemiBold", 44)
    cut = full.index("dans") if "dans" in full else 27
    line1, line2 = (txt[:cut].rstrip(), txt[cut:]) if len(txt) > cut else (txt, "")
    d.text((40, 85), line1, font=f, fill=INK); d.text((40, 145), line2, font=f, fill=INK)
    if n < len(full):
        lx = 40 + tw(f, line2 if line2 else line1) + 6; ly = 145 if line2 else 85
        d.rectangle((lx, ly + 6, lx + 5, ly + 52), fill=ORANGE)
    return card(im, 30)

# ------------------------------------------------------------------ scènes
def scene_A(t):   # 0 – 2.75 : avant / après en écran partagé + masque liquide
    base = Image.new("RGBA", (W, H), INK + (255,))
    left = cover(before_photo(), W // 2, H, 0.5, 0.5, 1.05 + 0.03 * t)
    base.paste(left, (0, 0))
    tr = S(1) - 0.05
    hint = cover(img("personnage_robe_salon.png"), W // 2, H, 0.5, 0.45, 1.06).filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.35))
    base.paste(hint, (W // 2, 0))
    if t >= tr:
        p = clamp((t - tr) / 0.55)
        right = cover(img("personnage_robe_salon.png"), W // 2, H, 0.5, 0.45, 1.06 + 0.04 * (t - tr))
        m = liquid_mask(p, (1.0, 0.45), W // 2, H)
        base.paste(right, (W // 2, 0), m)
        ai_tag(base)
    ImageDraw.Draw(base).line((W // 2, 0, W // 2, H), fill=WHITE + (255,), width=6)
    kin(base, "Ta photo…", t, S(0), W // 4, 1240, "play", 92, WHITE, 3, maxw=500)
    kin(base, "…ta vidéo ?", t, S(1) + 0.15, 3 * W // 4, 1240, "play", 92, YELLOW, 3, maxw=500)
    return base

def scene_B(t):   # 2.75 – 5.0 : le problème
    base = bg_gradient(t)
    paste_c(base, fit_text("STUDIO", "anton", 430, WHITE, 0, 1040), W // 2, 1560, 0.08)
    k = ease_out((t - 2.75) / 0.4)
    paste_c(base, cards()["exasp"], W // 2, 1130 + (1 - k) * 80, k, 0.98 + 0.02 * (t - 2.75))
    kin(base, "PAS DE MANNEQUIN ?", t, S(2), W // 2, 330, "anton", 112, WHITE)
    kin(base, "PAS DE STUDIO ?", t, S(3), W // 2, 470, "anton", 112, YELLOW)
    return base

def scene_C(t):   # 5.0 – 6.5 : Google Flow
    base = bg_gradient(t, warm=True)
    k = ease_out((t - 5.0) / 0.35)
    paste_c(base, cards()["jub"], W // 2, 1250, k, 0.85 + 0.15 * k)
    ti = text_img("Google Flow", "play", 168, WHITE)
    wipe = clamp((t - S(4) - 0.1) / 0.45)
    if wipe > 0:
        crop = ti.crop((0, 0, max(1, int(ti.width * ease_io(wipe))), ti.height))
        tmp = Image.new("RGBA", ti.size, (0, 0, 0, 0)); tmp.paste(crop, (0, 0)); paste_c(base, tmp, W // 2, 620)
        ImageDraw.Draw(base).rectangle((W // 2 - ti.width // 2 + 10, 740, W // 2 - ti.width // 2 + 10 + int((ti.width - 20) * ease_io(wipe)), 748), fill=ORANGE + (255,))
    kin(base, "l'outil vidéo IA de Google", t, S(4) + 0.4, W // 2, 820, "SemiBold", 52, CREAM)
    return base

def scene_D(t):   # 6.5 – 10.75 : photo + personnage + phrase = vidéo
    tr = S(7) - 0.05
    base = bg_cream(t)
    c = cards()
    def pop(name_or_img, t0, cx, cy, rot):
        if t < t0: return
        k = ease_out((t - t0) / 0.35); fl = 8 * math.sin((t - t0) * 2.2)
        im = c[name_or_img] if isinstance(name_or_img, str) else name_or_img
        paste_c(base, im, cx, cy + fl + (1 - k) * 60, k, 0.9 + 0.1 * k, rot)
    pop("avant", S(5), 310, 600, 4)
    kin(base, "1. Ta photo", t, S(5), 310, 960, "play", 64, NAVY, maxw=480)
    pop("perso", S(6), 770, 660, -4)
    kin(base, "2. Ton personnage", t, S(6), 770, 970, "play", 64, NAVY, maxw=520)
    t3 = S(6) + 0.55
    if t >= t3:
        pop(flow_ui_card(t, t3), t3, W // 2, 1310, 0)
        kin(base, "3. Une phrase dans Google Flow", t, t3, W // 2, 1640, "play", 60, NAVY)
        paste_c(base, text_img("Montage sur l’interface Google Flow", "Medium", 26, NAVY), W // 2, 1710, 0.75)
    if t >= tr:   # résultat : masque liquide vers la vidéo
        p = clamp((t - tr) / 0.6)
        full = Image.new("RGBA", (W, H))
        z = 1.0 + 0.06 * clamp((t - tr) / 1.6)
        full.paste(cover(img("personnage_robe_salon.png"), W, H, 0.5, 0.48, z), (0, 0))
        k = ease_out((t - tr - 0.35) / 0.4)
        if k > 0: paste_c(full, c["vignette"], 860, 560 + 6 * math.sin(t * 2), k, 1.0, -3)
        kin(full, "= ta vidéo", t, tr + 0.3, W // 2, 1380, "play", 110, WHITE, 3)
        ai_tag(full)
        base.paste(full, (0, 0), liquid_mask(p, (0.5, 1.0)))
    return base

def scene_E(t):   # 10.75 – 13.35 : lookbook en match-cuts
    shots = [(10.75, (0.5, 0.45, 1.0)), (S(9) - 0.05, (0.53, 0.40, 2.6)), (S(9) + 0.65, (0.5, 0.20, 2.3))]
    cx, cy, z = shots[0][1]
    for t0, v in shots:
        if t >= t0: cx, cy, z = v; tt = t - t0
    base = Image.new("RGBA", (W, H))
    base.paste(cover(img("personnage_robe_salon.png"), W, H, cx, cy, z * (1 + 0.025 * tt)), (0, 0))
    d = ImageDraw.Draw(base)
    for (x0, y0, x1, y1) in [(60, 60, 200, 64), (60, 60, 64, 200), (W - 200, H - 64, W - 60, H - 60), (W - 64, H - 200, W - 60, H - 60)]:
        d.rectangle((x0, y0, x1, y1), fill=WHITE + (230,))
    kin(base, "Montre le style.", t, S(8), W // 2, 1300, "play", 104, WHITE, 3)
    kin(base, "Montre les détails.", t, S(9), W // 2, 1440, "play", 104, YELLOW, 3)
    paste_c(base, text_img("Robe portefeuille · satin terracotta", "SemiBold", 34, WHITE, 2), W // 2, 1650, 0.9)
    ai_tag(base)
    return base

@functools.lru_cache(maxsize=None)
def formation_cards():
    ia = img("capture_formation_ia_motion_design.jpg").crop((26, 385, 618, 603))
    ct = img("capture_formation_claude_transform.jpg").crop((26, 247, 624, 500))
    ia_btn = img("capture_formation_ia_motion_design_2.jpg").crop((20, 935, 630, 1002))
    ct_btn = img("capture_formation_claude_transform.jpg").crop((26, 938, 624, 1003))
    def sized(im, w): return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    return {"ia": card(sized(ia, 880), 30), "ct": card(sized(ct, 880), 30),
            "ia_btn": card(sized(ia_btn, 820), 34, shadow=False), "ct_btn": card(sized(ct_btn, 820), 34, shadow=False)}

TAP_IA, TAP_CT = S(10) + 1.25, S(10) + 2.85

def tap(base, t, t0, cx, cy):
    """Indicateur de toucher (cercle qui s'élargit) sur le bouton."""
    k = (t - t0) / 0.45
    if 0 <= k <= 1:
        r = int(30 + 70 * ease_out(k)); a = int(200 * (1 - k))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ov).ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, a // 2), outline=(255, 255, 255, a), width=6)
        base.alpha_composite(ov)

def scene_F(t):   # 13.35 – 17.12 : rejoindre les formations
    base = bg_gradient(t)
    c = formation_cards()
    kin(base, "Rejoins mes formations", t, S(10), W // 2, 300, "play", 96, WHITE)
    def show(name, t0, cy, press=None):
        if t < t0: return
        k = ease_out((t - t0) / 0.35)
        sc = 1.0
        if press is not None and press <= t < press + 0.18: sc = 0.95
        paste_c(base, c[name], W // 2, cy + (1 - k) * 70, k, sc)
    show("ia", S(10) + 0.3, 600)
    show("ia_btn", S(10) + 0.7, 870, TAP_IA); tap(base, t, TAP_IA, W // 2 + 250, 870)
    show("ct", S(10) + 1.9, 1180)
    show("ct_btn", S(10) + 2.3, 1450, TAP_CT); tap(base, t, TAP_CT, W // 2 + 250, 1450)
    kin(base, "IA Motion Design · Claude Transform — 20,5 $US chacune", t, S(10) + 2.5, W // 2, 1600, "Medium", 40, CREAM)
    return base

def scene_G(t):   # 17.2 – fin : appel à l'action
    base = bg_gradient(t, warm=True)
    kin(base, "Rejoins la chaîne WhatsApp", t, 17.12, W // 2, 470, "play", 86, WHITE)
    t0 = 17.2; k = ease_out((t - t0) / 0.32)
    if t >= t0: paste_c(base, cards()["whatsapp"], W // 2, 1000 + (1 - k) * 260, k)
    if t >= S(12):
        pill = text_img("Le lien est dans ma bio", "Black", 60, INK)
        bg = Image.new("RGBA", (pill.width + 60, pill.height + 24), (0, 0, 0, 0))
        ImageDraw.Draw(bg).rounded_rectangle((0, 0, bg.width - 1, bg.height - 1), 40, fill=YELLOW + (255,))
        bg.alpha_composite(pill, (30, 8))
        kk = ease_out((t - S(12)) / 0.3); paste_c(base, bg, W // 2, 1500, kk, 0.9 + 0.1 * kk)
    paste_c(base, text_img("Woman Business", "play7", 54, CREAM), W // 2, 1700, 0.85)
    return base

SCENES = [(0.0, scene_A), (2.75, scene_B), (5.0, scene_C), (6.5, scene_D), (10.75, scene_E), (13.35, scene_F), (17.12, scene_G)]

def frame(t):
    fn = [f for t0, f in SCENES if t >= t0][-1]
    im = fn(t)
    if t > TOTAL - 0.5:   # fondu final
        im = Image.blend(im, Image.new("RGBA", (W, H), NAVY2 + (255,)), clamp((t - (TOTAL - 0.5)) / 0.5) * 0.6)
    return im.convert("RGB")

# ------------------------------------------------------------------ audio
SFX = [(S(1) - 0.08, "audio/sfx_souffle.mp3", -6),   # 1. ouverture du masque liquide
       (S(7) - 0.02, "audio/sfx_tissu.mp3", -4),     # 2. la robe apparaît portée
       (TAP_IA - 0.02, "audio/sfx_clic.mp3", -9),     # toucher « Rejoindre la formation » (IA Motion Design)
       (TAP_CT - 0.02, "audio/sfx_clic.mp3", -9),     # toucher « Rejoindre la formation » (Claude Transform)
       (17.2 + 0.30, "audio/sfx_clic.mp3", -8)]     # 3. la carte WhatsApp se pose

def build_audio(out="cache/mix.wav"):
    os.makedirs("cache", exist_ok=True)
    inp = ["-i", "audio/voix_off.mp3", "-i", "audio/musique_cat_walk.mp3"]
    fc = [f"[0:a]aresample=48000,adelay={int(VO*1000)}|{int(VO*1000)},volume=1.0[v]",
          f"[1:a]aresample=48000,atrim=0:{TOTAL},volume=-17dB,afade=t=in:d=0.3,afade=t=out:st={TOTAL-1.4}:d=1.4[m]"]
    lab = ["[v]", "[m]"]
    for i, (t, f, g) in enumerate(SFX):
        inp += ["-i", f]
        fc.append(f"[{i+2}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:1.6,afade=t=out:st=1.2:d=0.4,volume={g}dB,adelay={int(t*1000)}|{int(t*1000)}[s{i}]")
        lab.append(f"[s{i}]")
    fc.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0:duration=longest,alimiter=limit=0.8:level=false[o]")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", ";".join(fc), "-map", "[o]", "-t", str(TOTAL), "-ac", "2", out])
    return out

def render(out="export/woman_business_flow_9x16.mp4"):
    mix = build_audio(); os.makedirs("export", exist_ok=True)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", mix, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
    n = round(TOTAL * FPS)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
        if i % 90 == 0: print(f"  {i/FPS:5.1f}s / {TOTAL}s", flush=True)
    p.stdin.close(); p.wait(); print("OK ->", out)

if __name__ == "__main__":
    if "--preview" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1].split(",")]
        os.makedirs("cache", exist_ok=True)
        ims = [frame(t).resize((270, 480)) for t in ts]
        sh = Image.new("RGB", (270 * len(ims), 480))
        for i, im in enumerate(ims): sh.paste(im, (i * 270, 0))
        sh.save("cache/preview.jpg", quality=88); print("cache/preview.jpg")
        big = [frame(t).resize((432, 768)) for t in ts]
        for j in range(0, len(big), 5):
            g = Image.new("RGB", (432 * 5, 768), "white")
            for i, im in enumerate(big[j:j + 5]): g.paste(im, (i * 432, 0))
            g.save(f"cache/preview_big_{j // 5}.jpg", quality=86)
    else:
        render()
