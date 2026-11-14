#!/usr/bin/env python3
"""Vidéo 2 bis — « Pinduoduo en français avec WeChat », version motion design sans personnage plein cadre.

Le visage de Samantha (images IA du Drive) parle dans une bulle en bas de l'écran ; ses phrases s'affichent
mot à mot dans une bulle de dialogue. Le haut de l'écran montre l'explication en motion design avec les
vrais logos (Pinduoduo, WeChat, WhatsApp) pour que le public reconnaisse tout de suite les applis.

La voix : si audio/voix_pdd.mp3 existe (voix clonée ElevenLabs ou enregistrement de Samantha),
elle est mixée automatiquement et la musique baisse sous la voix. Sinon, la vidéo sort en musique + texte.

    python3 build_pdd_motion.py              -> export/pinduoduo_wechat_motion_9x16.mp4
    python3 build_pdd_motion.py --preview 1,6,12
"""
import sys, os, subprocess, math, functools
import numpy as np
import build as B
from build import (W, H, FPS, Image, ImageDraw, ImageFilter, clamp, ease_out, ease_io, cover, card, paste_c,
                   text_img, fit_text, kin, bg_gradient, bg_cream, liquid_mask, phone_page, tap, badge, img, rmask,
                   NAVY, NAVY2, ORANGE, CREAM, INK, YELLOW, WHITE)

TOTAL = 30.0
RED = (225, 37, 27)          # rouge Pinduoduo
GREEN = (7, 193, 96)         # vert WeChat
WA = (37, 211, 102)          # vert WhatsApp

# ------------------------------------------------------------------ ce que dit Samantha (début, fin, phrase, visage)
LINES = [
    (0.15, 2.4, "Pinduoduo est en chinois ?", "pense"),
    (2.4, 4.6, "Regarde, je te le mets en français avec WeChat.", "sourire"),
    (4.6, 7.4, "Ouvre WeChat, va dans « Moi »,", "neutre"),
    (7.4, 9.6, "puis « Paramètres » et « Généralités ».", "neutre"),
    (9.6, 12.0, "Touche « Gérer la page Découvrir »", "sourire"),
    (12.0, 14.0, "et active les « Mini-programmes ».", "neutre"),
    (14.0, 16.8, "Dans « Découvrir », ouvre « Mini-programmes » et cherche Pinduoduo.", "sourire"),
    (16.8, 19.4, "Appuie sur « Traduction »… et voilà : c'est en français !", "rire"),
    (19.4, 22.6, "Tu es en RDC ? J'ai réuni la liste des transitaires et des fournisseurs dans mon groupe WhatsApp.", "sourire"),
    (22.6, 25.4, "Le lien est dans ma bio. Si tu bloques, écris-moi « PDD ».", "rire"),
    (25.4, 29.6, "Et pour aller plus loin : mes formations.", "sourire"),
]

# ------------------------------------------------------------------ logos
@functools.lru_cache(maxsize=None)
def logo(name, size):
    im = Image.open(f"assets/logos/{name}").convert("RGBA")
    im.thumbnail((size, size), Image.LANCZOS)
    return im

def pdd(size): return logo("pdd_app.png", size)
def wechat(size): return logo("wechat_app.png", size)
def whatsapp(size): return logo("whatsapp_app.png", size)

@functools.lru_cache(maxsize=None)
def pdd_word(w):
    im = Image.open("assets/logos/pdd_wordmark.png").convert("RGBA")
    return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)

def shadowed(im, blur=18, off=14, a=110):
    pad = blur * 2 + off
    out = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    m = im.getchannel("A").point(lambda v: v * a // 255)
    sh.paste((0, 0, 0, 255), (pad, pad + off), m)
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    out.alpha_composite(im, (pad, pad))
    return out

def pop(t, t0, d=0.45):
    """Apparition avec léger rebond (0 → 1, dépasse un peu)."""
    k = clamp((t - t0) / d)
    return 0 if k <= 0 else 1 + 0.12 * math.sin(k * math.pi) * (1 - k) * 2.2 - (1 - ease_out(k))

# ------------------------------------------------------------------ visage de Samantha + bulle de dialogue
FACE_SRC = {"neutre": ("personnage_planche.png", 0), "sourire": ("personnage_planche.png", 1),
            "pense": ("personnage_planche.png", 2), "rire": ("jubilation_portrait_face.png", None)}

@functools.lru_cache(maxsize=None)
def face(kind, d=250):
    f, i = FACE_SRC[kind]; p = img(f)
    if i is None:
        s = 980; cx, cy = 832, 720
    else:
        cw, ch = p.width / 3, p.height / 3; s = int(cw * 0.74); cx = i * cw + cw / 2; cy = ch + ch * 0.38
    im = p.crop((int(cx - s / 2), int(cy - s / 2), int(cx + s / 2), int(cy + s / 2))).resize((d, d), Image.LANCZOS)
    m = Image.new("L", (d, d), 0); ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), fill=255)
    out = Image.new("RGBA", (d, d), (0, 0, 0, 0)); out.paste(im, (0, 0), m)
    return out

def speaking(t):
    for t0, t1, s, f in LINES:
        if t0 <= t < t1: return t0, t1, s, f
    return None

FX, FY, FD = 175, 1700, 250      # centre et diamètre du visage

def avatar(base, t):
    k = ease_out((t - 0.05) / 0.4)
    if k <= 0: return
    ln = speaking(t)
    kind = ln[3] if ln else "sourire"
    talk = ln is not None and t < ln[1] - 0.25
    env = (0.55 + 0.45 * abs(math.sin(t * 9.1)) * abs(math.sin(t * 3.7 + 1))) if talk else 0.0
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    r0 = FD // 2 + 10
    for j, (extra, a) in enumerate(((10 + 26 * env, 70), (4 + 12 * env, 150))):
        r = r0 + extra
        d.ellipse((FX - r, FY - r, FX + r, FY + r), outline=ORANGE + (int(a * k),), width=6 if j else 4)
    d.ellipse((FX - r0, FY - r0, FX + r0, FY + r0), fill=WHITE + (255,))
    base.alpha_composite(ov)
    bob = 1 + 0.012 * math.sin(t * 2.3)
    paste_c(base, face(kind, FD), FX, FY - 4 * math.sin(t * 1.7), k, bob)
    # nom
    nm = text_img("Samantha", "Bold", 34, WHITE)
    tag = Image.new("RGBA", (nm.width + 26, nm.height + 6), (0, 0, 0, 0))
    ImageDraw.Draw(tag).rounded_rectangle((0, 0, tag.width - 1, tag.height - 1), 22, fill=ORANGE + (255,))
    tag.alpha_composite(nm, (13, 2)); paste_c(base, tag, FX, FY + FD // 2 + 26, k)
    paste_c(base, text_img("Visage généré par IA", "Medium", 22, (225, 228, 238)), FX, FY + FD // 2 + 76, 0.8 * k)

@functools.lru_cache(maxsize=None)
def bubble_layout(s, maxw=620, size=44):
    f = B.f_inter("Bold", size); sp = B.tw(f, " ")
    words = s.split(" "); lines = [[]]; x = 0; q = False; out = []
    for wd in words:
        w = B.tw(f, wd)
        if lines[-1] and x + w > maxw: lines.append([]); x = 0
        hl = q or "«" in wd or "»" in wd
        if "«" in wd: q = True
        if "»" in wd: q = False
        lines[-1].append((wd, x, hl)); x += w + sp
    return f, lines, size

def speech_bubble(base, t):
    ln = speaking(t)
    if not ln: return
    t0, t1, s, _ = ln
    f, lines, size = bubble_layout(s)
    n = sum(len(l) for l in lines)
    shown = int(clamp((t - t0) / max(0.4, (t1 - t0) * 0.8)) * n + 0.999)
    lh = int(size * 1.32); w = 690; h = len(lines) * lh + 44
    im = Image.new("RGBA", (w + 40, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 0, w + 39, h - 1), 34, fill=WHITE + (255,))
    d.polygon([(42, h // 2 - 22), (0, h // 2 + 4), (42, h // 2 + 22)], fill=WHITE + (255,))
    i = 0
    for li, row in enumerate(lines):
        for wd, x, hl in row:
            col = (ORANGE if hl else INK) if i < shown else (205, 205, 212)
            d.text((40 + 30 + x, 20 + li * lh), wd, font=f, fill=col + (255,)); i += 1
    k = ease_out((t - t0) / 0.18)
    sh = Image.new("RGBA", (im.width + 60, im.height + 60), (0, 0, 0, 0))
    m = im.getchannel("A").point(lambda v: v * 90 // 255); sh.paste((0, 0, 0, 255), (30, 42), m)
    sh = sh.filter(ImageFilter.GaussianBlur(16)); sh.alpha_composite(im, (30, 30))
    base.alpha_composite(sh.copy() if k >= 1 else _fade(sh, k), (FX + FD // 2 + 4 - 30, int(FY - im.height / 2 - 30 + (1 - k) * 18)))

def _fade(im, a):
    im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a))); return im

def bottom_shade(base):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for i in range(380):
        d.line((0, H - 380 + i, W, H - 380 + i), fill=(6, 12, 30, int(205 * (i / 380) ** 0.8)))
    base.alpha_composite(ov)

# ------------------------------------------------------------------ drapeau RDC (dessiné, proportions officielles 4:3)
@functools.lru_cache(maxsize=None)
def flag_rdc(w=240):
    h = int(w * 3 / 4); s = 4
    im = Image.new("RGBA", (w * s, h * s), (0, 127, 255, 255)); d = ImageDraw.Draw(im)
    W2, H2 = w * s, h * s
    def band(width, col):
        o = width * H2
        d.polygon([(0, H2 - o), (0, H2), (o * W2 / H2 * 0.75, H2), (W2, o), (W2, 0), (W2 - o * W2 / H2 * 0.75, 0)], fill=col)
    band(0.30, (247, 216, 23, 255)); band(0.22, (206, 16, 33, 255))
    cx, cy, R = W2 * 0.17, H2 * 0.22, H2 * 0.15
    pts = [(cx + (R if j % 2 == 0 else R * 0.4) * math.sin(j * math.pi / 5), cy - (R if j % 2 == 0 else R * 0.4) * math.cos(j * math.pi / 5)) for j in range(10)]
    d.polygon(pts, fill=(247, 216, 23, 255))
    im = im.resize((w, h), Image.LANCZOS)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0)); out.paste(im, (0, 0), rmask((w, h), 14)); return out

# ------------------------------------------------------------------ scènes
CHARS = "拼多多购物优惠特价包邮砍价"
def s_hook(t):                        # 0 – 4.6
    base = bg_gradient(t)
    rng = np.random.default_rng(3)
    for i in range(16):                # caractères chinois qui flottent : « tout est en chinois »
        x = rng.uniform(80, W - 80); y0 = rng.uniform(150, 1300); sp = rng.uniform(30, 70)
        a = 0.18 if t < 2.4 else 0.18 * clamp(1 - (t - 2.4) / 0.5)
        if a > 0:
            paste_c(base, text_img(CHARS[i % len(CHARS)], "cjk", int(rng.uniform(70, 140)), WHITE), x, (y0 - sp * t) % 1400 + 120, a)
    # logo Pinduoduo
    k = pop(t, 0.1)
    move = ease_io((t - 2.4) / 0.5)
    cx = W // 2 - move * 230; sz = 1 - 0.38 * move
    if k > 0:
        paste_c(base, shadowed(pdd(560)), cx, 560 + 10 * math.sin(t * 2), 1.0, max(0.01, k * sz), 4 * math.sin(t * 1.3) * (1 - move))
    kin(base, "Pinduoduo est en chinois ?", t, 0.5, W // 2, 1060, "anton", 104, WHITE, 0, t1=2.4)
    # WeChat arrive : PDD + WeChat = français
    if t >= 2.4:
        kw = pop(t, 2.55)
        paste_c(base, text_img("+", "anton", 140, YELLOW), W // 2, 560, clamp((t - 2.6) / 0.2))
        if kw > 0: paste_c(base, shadowed(wechat(330)), W // 2 + 230, 560, 1.0, max(0.01, kw))
        kin(base, "Mets-le en FRANÇAIS", t, 2.75, W // 2, 1000, "anton", 120, YELLOW)
        kin(base, "avec WeChat, en 6 étapes", t, 3.15, W // 2, 1135, "SemiBold", 58, WHITE)
    return base

STEPS = [("1", "Ouvre WeChat › « Moi »", "wechat"),
         ("2", "« Paramètres » puis « Généralités »", None),
         ("3", "« Gérer la page Découvrir »", None),
         ("4", "Active « Mini-programmes »", None),
         ("5", "Mini-programmes › 拼多多", "pdd"),
         ("6", "Appuie sur « Traduction »", "fr")]
STEP_T = [4.6, 7.4, 9.6, 12.0, 14.0, 16.8]

@functools.lru_cache(maxsize=None)
def step_card(i, active):
    num, title, ic = STEPS[i]
    w, h = 940, 158
    im = Image.new("RGBA", (w, h), WHITE + (255,)); d = ImageDraw.Draw(im)
    col = ORANGE if active else (205, 205, 212)
    d.ellipse((24, h // 2 - 44, 112, h // 2 + 44), fill=col)
    fn = B.f_anton(60); d.text((68 - B.tw(fn, num) // 2, h // 2 - 44), num, font=fn, fill=WHITE)
    maxw = 640 if ic else 770
    parts = title.split("拼多多")
    ti = fit_text(parts[0].strip(), "Bold", 46, INK, 0, maxw - (150 if len(parts) > 1 else 0))
    im.alpha_composite(ti, (128, h // 2 - ti.height // 2))
    if len(parts) > 1:
        cj = text_img("拼多多", "cjk", 46, RED); im.alpha_composite(cj, (128 + ti.width - 6, h // 2 - cj.height // 2 + 2))
    if ic == "wechat": im.alpha_composite(wechat(104), (w - 134, h // 2 - 52))
    elif ic == "pdd": im.alpha_composite(pdd(112), (w - 138, h // 2 - 56))
    elif ic == "fr":
        b = Image.new("RGBA", (112, 112), (0, 0, 0, 0)); bd = ImageDraw.Draw(b)
        bd.ellipse((0, 0, 111, 111), fill=YELLOW + (255,)); ft = B.f_anton(54)
        bd.text((56 - B.tw(ft, "FR") // 2, 14), "FR", font=ft, fill=INK)
        im.alpha_composite(b, (w - 138, h // 2 - 56))
    return card(im, 30, border=ORANGE + (255,) if active else None)

def s_steps(t):                       # 4.6 – 18.0
    base = bg_cream(t)
    # en-tête : logos réels
    k = ease_out((t - 4.65) / 0.35)
    hd = Image.new("RGBA", (900, 130), (0, 0, 0, 0))
    hd.alpha_composite(wechat(110), (0, 10))
    ar = text_img("→", "Bold", 80, NAVY); hd.alpha_composite(ar, (130, 8))
    hd.alpha_composite(pdd(120), (250, 5))
    tx = text_img("en français", "play", 74, NAVY); hd.alpha_composite(tx, (395, 18))
    paste_c(base, hd, W // 2 + 30, 175 + (1 - k) * 30, k)
    n = sum(1 for s in STEP_T if t >= s)
    y0, gap = 345, 188
    for i in range(n):
        ki = ease_out((t - STEP_T[i]) / 0.35)
        cy = y0 + i * gap
        paste_c(base, step_card(i, i == n - 1), W // 2, cy + (1 - ki) * 60, ki)
        if i == n - 1: tap(base, t, STEP_T[i] + 0.55, W // 2 + 360, cy)
    return base

def s_result(t):                      # 18.0 – 19.4
    base = bg_gradient(t, warm=True)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for j in range(14):                # rayons
        a = j * math.pi / 7 + t * 0.4
        d.polygon([(W // 2, 600), (W // 2 + 1400 * math.cos(a - 0.08), 600 + 1400 * math.sin(a - 0.08)),
                   (W // 2 + 1400 * math.cos(a + 0.08), 600 + 1400 * math.sin(a + 0.08))], fill=(255, 214, 10, 22))
    base.alpha_composite(ov)
    k = pop(t, 18.05)
    if k > 0: paste_c(base, shadowed(pdd(520)), W // 2, 600, 1.0, max(0.01, k))
    kf = pop(t, 18.35)
    if kf > 0:
        b = Image.new("RGBA", (190, 190), (0, 0, 0, 0)); bd = ImageDraw.Draw(b)
        bd.ellipse((0, 0, 189, 189), fill=YELLOW + (255,), outline=WHITE + (255,), width=8); ft = B.f_anton(92)
        bd.text((95 - B.tw(ft, "FR") // 2, 26), "FR", font=ft, fill=INK)
        paste_c(base, b, W // 2 + 230, 400, 1.0, max(0.01, kf), -10)
    kin(base, "Et voilà : en français !", t, 18.2, W // 2, 1010, "play", 96, WHITE, 3)
    kin(base, "Commander · Payer · Faire livrer en RDC", t, 18.55, W // 2, 1135, "SemiBold", 48, YELLOW)
    return base

def chip(txt, col, fg=WHITE, size=62):
    tx = text_img(txt, "anton", size, fg)
    im = Image.new("RGBA", (tx.width + 60, tx.height + 16), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, im.width - 1, im.height - 1), 26, fill=col + (255,))
    im.alpha_composite(tx, (30, 6)); return shadowed(im, 12, 8, 90)

def s_rdc(t):                         # 19.4 – 25.4 : la liste dans le groupe WhatsApp
    base = bg_gradient(t)
    if t < 22.6:
        kf = pop(t, 19.45)
        if kf > 0: paste_c(base, shadowed(flag_rdc(200), 14, 10, 120), 175, 230, 1.0, max(0.01, kf), 6)
        kin(base, "Tu es en RDC ?", t, 19.55, W // 2 + 125, 230, "anton", 104, WHITE)
        kin(base, "J'ai réuni la liste des", t, 19.9, W // 2, 420, "SemiBold", 56, CREAM)
        for j, (txt, col) in enumerate((("TRANSITAIRES", ORANGE), ("FOURNISSEURS", RED))):
            kc = pop(t, 20.25 + 0.35 * j)
            if kc > 0: paste_c(base, chip(txt, col, size=96), W // 2, 580 + j * 170, 1.0, max(0.01, kc), -3 + 6 * j)
        kin(base, "dans mon groupe", t, 21.1, W // 2, 960, "play", 92, WHITE)
        kw = pop(t, 21.3)
        if kw > 0:
            paste_c(base, shadowed(whatsapp(150)), W // 2 - 260, 1115, 1.0, max(0.01, kw))
        kin(base, "WhatsApp", t, 21.5, W // 2 + 80, 1110, "anton", 110, WA)
    else:
        ph, s = phone_page("capture_chaine_whatsapp.jpg", 920)
        k = ease_out((t - 22.6) / 0.4)
        paste_c(base, ph, W // 2 + 180, 760 + (1 - k) * 160, k)
        kw = pop(t, 22.75)
        if kw > 0: paste_c(base, shadowed(whatsapp(190)), 200, 330, 1.0, max(0.01, kw))
        kin(base, "Lien", t, 22.9, 200, 520, "anton", 92, WHITE)
        kin(base, "dans", t, 23.05, 200, 625, "anton", 92, WHITE)
        kin(base, "ma bio", t, 23.2, 200, 730, "anton", 92, YELLOW)
        kp = pop(t, 24.0)
        if kp > 0: paste_c(base, chip("Si tu bloques : écris « PDD »", YELLOW, INK, 60), W // 2, 1395, 1.0, max(0.01, kp), -3)
    return base

PAGES2 = [("capture_formation_ia_motion_design.jpg", 25.4, (20, 1066, 630, 1134), "335+ apprenants"),
          ("capture_formation_claude_transform.jpg", 27.5, (26, 938, 624, 1003), "128+ apprenants")]

def s_formations(t):                  # 25.4 – fin
    base = bg_gradient(t)
    kin(base, "Pour aller plus loin :", t, 25.4, W // 2, 110, "play", 74, WHITE)
    for i, (name, t0, btn, lab) in enumerate(PAGES2):
        t1 = PAGES2[i + 1][1] if i + 1 < len(PAGES2) else 99
        if not (t0 <= t < t1 + 0.35): continue
        ph, s = phone_page(name, 1180)
        ki = ease_out((t - t0) / 0.35); out = ease_io((t - t1) / 0.35) if t >= t1 else 0
        cx = W // 2 + (1 - ki) * 700 - out * 900; cy = 860
        ox = cx - ph.width / 2 + 84; oy = cy - ph.height / 2 + 84
        paste_c(base, ph, cx, cy, 1.0)
        badge(base, t, t0 + 0.4, lab, W // 2, 215)
        tap(base, t, t0 + 1.0, ox + (btn[0] + btn[2]) / 2 * s + 120, oy + (btn[1] + btn[3]) / 2 * s)
    return base

SCENES = [(0, s_hook), (4.6, s_steps), (18.0, s_result), (19.4, s_rdc), (25.4, s_formations)]
CUTS = (4.6, 18.0, 19.4, 25.4)

def scene_at(t): return [f for t0, f in SCENES if t >= t0][-1](t)

def frame(t):
    im = scene_at(t)
    for tc in CUTS:                    # transitions liquides
        if tc - 0.01 <= t < tc + 0.45:
            prev = [f for t0, f in SCENES if t0 < tc][-1](tc - 0.02)
            m = liquid_mask(clamp((t - tc) / 0.45), (0.5, 1.0))
            prev.paste(im, (0, 0), m); im = prev
    bottom_shade(im); avatar(im, t); speech_bubble(im, t)
    if t > TOTAL - 0.5:
        im = Image.blend(im, Image.new("RGBA", (W, H), NAVY2 + (255,)), clamp((t - (TOTAL - 0.5)) / 0.5) * 0.6)
    return im.convert("RGB")

# ------------------------------------------------------------------ son
VOICE = "audio/voix_pdd.mp3"
SFX = [(c - 0.02, "audio/sfx_souffle.mp3", -10) for c in CUTS] + \
      [(s + 0.53, "audio/sfx_clic.mp3", -14) for s in STEP_T] + \
      [(p[1] + 0.98, "audio/sfx_clic.mp3", -11) for p in PAGES2]

def build_audio(out="cache/mix_pdd_motion.wav"):
    has_voice = os.path.exists(VOICE)
    inp = ["-i", "audio/musique_tech_house.mp3"]
    fc = [f"[0:a]aresample=48000,atrim=0:{TOTAL},volume={-14 if has_voice else -7}dB,afade=t=in:d=0.2,afade=t=out:st={TOTAL - 1.5}:d=1.5[m]"]
    lab = ["[m]"]
    for i, (t, f, g) in enumerate(SFX):
        inp += ["-i", f]
        fc.append(f"[{i + 1}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:1.4,afade=t=out:st=1.0:d=0.4,volume={g}dB,adelay={int(t * 1000)}|{int(t * 1000)}[s{i}]")
        lab.append(f"[s{i}]")
    if has_voice:
        inp += ["-i", VOICE]; j = len(SFX) + 1
        fc.append(f"[{j}:a]aresample=48000,aformat=channel_layouts=stereo,adelay=150|150,volume=1.0[v]"); lab.append("[v]")
    fc.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0:duration=first,alimiter=limit=0.8:level=false[o]")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", ";".join(fc), "-map", "[o]", "-t", str(TOTAL), "-ac", "2", out])
    return out

def render(out="export/pinduoduo_wechat_motion_9x16.mp4"):
    mix = build_audio()
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", mix, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
    for i in range(round(TOTAL * FPS)):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK ->", out)

if __name__ == "__main__":
    if "--preview" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1].split(",")]
        big = [frame(t).resize((432, 768)) for t in ts]
        for j in range(0, len(big), 5):
            g = Image.new("RGB", (432 * 5, 768), "white")
            for i, im in enumerate(big[j:j + 5]): g.paste(im, (i * 432, 0))
            g.save(f"cache/pddm_preview_{j // 5}.jpg", quality=86)
        print("ok")
    else:
        render()
