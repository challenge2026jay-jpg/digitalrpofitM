#!/usr/bin/env python3
"""Montage complet « Les obstacles des commandes en Chine » (16:9, 1080p, 30 i/s).

    python3 nettoyer_voix.py          # voix sans sons parasites + mots horodatés
    python3 build_chine.py            # rendu complet -> export/obstacles_chine_16x9.mp4
    python3 build_chine.py --frames 12.5 300 410   # aperçus PNG à ces secondes (cache/apercus)

Style : celui de la vidéo de référence (fond émeraude, cartes d'interface, titres gras + serif italique,
tampons, suivi de progression, sous-titres 3-5 mots). Aucune vidéo extérieure : seulement textes animés
et fichiers du Drive (D1-D15). Chaque élément apparaît sur le mot prononcé.
"""
import os, sys, json, subprocess, math
from multiprocessing import Process
import numpy as np
from PIL import Image, ImageDraw
from engine import *

os.chdir(HERE)
VOICE = "audio/voix_montage.wav"
WORDS = json.load(open("audio/mots_montage.json"))["words"]
VOICE_DUR = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VOICE]))
END_HOLD = 1.3
TOTAL = VOICE_DUR + END_HOLD

# ------------------------------------------------------------------ corrections du texte (sous-titres)
WORDS = [w for w in WORDS if w["text"].strip() not in ("«", "»", "?")]
FIX = [
    ("au cas ici", "« Ça ici,"), ("moi y eux", "moi. »"), ("tout parait sain", "tout paraît simple."),
    ("photos a noter", "photos annotées"), ("defini les criteres", "Définis les critères"),
    ("dire au gars", "Dire « "), ("qualite ee et trop vague", "qualité » est trop vague."),
    ("fournisseur point ils", "fournisseur. Ils"), ("etre fait", "être vrai."), ("si il", "s'il"),
    ("dont aussi", "demande aussi"), ("prevoit", "prévois"), ("evite de", "Évite de"),
    ("avance par etape", "Avance par étapes :"), ("mais ne verifie pas", "mais ne vérifient pas"),
    ("doit apporter", "doit porter"), ("pays c est", "pays ? C'est"), ("tous les frais", "tous les frais ?"),
    ("se vendre est ce que je", "se vendre ? Est-ce que je"), ("seulement est ce que", "seulement : est-ce que"),
    ("demande donc combien", "demande-toi : combien"), ("chaque unite", "chaque unité ?"), ("puis je la vendre", "puis-je la vendre ?"),
    ("la publicite et la livraison", "la publicité et la livraison ?"), ("se vend pas", "se vend pas ?"),
]
def apply_fix(words, old, new):
    tgt = norm(old); out = []; i = 0
    while i < len(words):
        acc = []; j = i
        while j < len(words) and len(acc) < len(tgt):
            acc += norm(words[j]["text"]); j += 1
        if acc == tgt:
            a, b = words[i]["start"], words[j - 1]["end"]; parts = new.split(" ")
            for k, p in enumerate(parts):
                out.append({"text": p, "start": a + (b - a) * k / len(parts), "end": a + (b - a) * (k + 1) / len(parts)})
            i = j
        else:
            out.append(words[i]); i += 1
    return out
for o, n in FIX: WORDS = apply_fix(WORDS, o, n)

TOK = []          # (token normalisé, index du mot)
for i, w in enumerate(WORDS):
    for t in norm(w["text"]): TOK.append((t, i))

def find(phrase, after=0.0, which="start"):
    tgt = norm(phrase)
    for k in range(len(TOK) - len(tgt) + 1):
        if WORDS[TOK[k][1]]["start"] < after - 0.05: continue
        if [TOK[k + m][0] for m in range(len(tgt))] == tgt:
            w = WORDS[TOK[k + len(tgt) - 1][1]] if which == "end" else WORDS[TOK[k][1]]
            return w[which]
    raise KeyError(f"introuvable après {after:.1f}s : {phrase}")

# ------------------------------------------------------------------ scènes
OBST = ["Fournisseur", "Langue", "Qualité", "Frais cachés", "Délais", "Arnaques", "Rentabilité"]
class Scene:
    def __init__(self, n, phrase, bg, ob, build, chrome=True, subs=True, glitch=False):
        self.n, self.phrase, self.bg, self.ob, self.build = n, phrase, bg, ob, build
        self.chrome, self.subs, self.glitch = chrome, subs, glitch
        self.els = []; self.cursors = []
    def w(self, phrase, which="start"): return find(phrase, self.t0, which)
    def add(self, *a, **k):
        k.setdefault("t1", self.t1); e = El(*a, **k); self.els.append(e); return e
    def cursor(self, keys, clicks):
        self.cursors.append(Cursor(keys, clicks, self.t1))

SC = []
def scene(phrase, bg="dark", ob=None, chrome=True, subs=True, glitch=False):
    def deco(fn):
        SC.append(Scene(len(SC) + 1, phrase, bg, ob, fn, chrome, subs, glitch)); return fn
    return deco

# ------------------------------------------------------------------ petits constructeurs
CX, CY = 960, 480
def hook(txt, col=MUTED, size=40): return rich([(txt, "serif_i", size, col)])
def title(h, runs, hcol=MUTED, spacing=6):
    return stack([hook(h, hcol)] + [rich(r) for r in runs], spacing) if h else stack([rich(r) for r in runs], spacing)
def B(t, s=110, c=WHITE): return (t, "xbold", s, c)
def I(t, s=110, c=MINT): return (t, "serif_i", s, c)
def big_num(t, s=230, c=WHITE): return rich([(t, "serif_i", s, c)])

def vid(code, maxw, maxh, mode="tile", t0=0.0, t1=None, size=None, w=None, crop=None):
    """Animation du Drive : mode tile (carte blanche carrée), frame (cadre arrondi), raw."""
    if mode == "tile":
        S = size or 240
        if crop:
            src = drive_video(code, 600, 600, t0, t1); fw, fh = src[0].size
            frames = []
            for fr in src:
                c = fr.crop((int(crop[0] * fw), int(crop[1] * fh), int(crop[2] * fw), int(crop[3] * fh)))
                c.thumbnail((S - 50, S - 50), Image.LANCZOS) if c.width > S - 50 else None
                sc = (S - 60) / max(c.size); frames.append(c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS))
        else:
            frames = drive_video(code, S - 50, S - 50, t0, t1)
    else:
        frames = drive_video(code, maxw, maxh, t0, t1)
    cache = {}
    def f(tl):
        i = int(tl * 30) % len(frames)
        if i not in cache:
            fr = frames[i]
            if mode == "tile":
                c = rounded(S, S, rgba(WHITE), 40, outline=(225, 225, 220, 255), width=2)
                c.alpha_composite(fr, ((S - fr.width) // 2, (S - fr.height) // 2)); cache[i] = shadowed(c, 24, (0, 10), 90)
            elif mode == "frame":
                cache[i] = shadowed(framed(fr, w or fr.width), 28, (0, 14), 110)
            else:
                cache[i] = fr
        return cache[i]
    return f

def img_frame(code, w, r=26): return shadowed(framed(drive_image(code), w, r))

def obstacle_card(S, k, l1, l2, st, red=False, sub=None, sub_t=None):
    col = RED if red else MINT
    num = rich([(f"{k:02d}", "serif", 260, (255, 255, 255, 60) if not red else (255, 200, 195, 70))])
    ttl = stack([rich([B(l1, 96)]), rich([I(l2, 104, col)])], 0, "left")
    S.add(num, 520, CY - 10, S.t0, anim="fade", dur=0.4)
    S.add(ttl, 720, CY - 20, S.t0 + 0.08, anim="left", anchor="l", sfx="S9" if red else "S1")
    S.add(stamp(st, col, 52), 1460, CY + 150, S.t0 + 0.7, anim="stamp", dur=0.3)
    if sub: S.add(hook(sub, MUTED, 44), CX, CY + 290, sub_t, anim="up")

def chips_row(items, size=34, bg=(255, 255, 255, 235), fg=INK):
    return [pill(t, bg, fg, size) for t in items]

def strike(w, col=RED, thick=8):
    def f(tl):
        p = ease_out(clamp(tl / 0.35)); im = Image.new("RGBA", (w, thick + 4), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle((0, 2, max(thick, int(w * p)), thick + 2), thick // 2, fill=rgba(col))
        return im
    return f

def bubble(txt_lines, mine=True, w=620):
    col = (32, 120, 86, 255) if mine else (255, 255, 255, 255); fg = WHITE if mine else INK
    t = stack([rich([(l, "semi", 32, fg)]) for l in txt_lines], 4, "left")
    c = rounded(min(w, t.width + 56), t.height + 40, col, 26)
    c.alpha_composite(t, (28, 20)); return shadowed(c, 20, (0, 8), 80)

def calendar_card(highlight=(), red=(), title_txt="NOVEMBRE", w=520):
    c = card(w, 470, light=True); d = ImageDraw.Draw(c)
    c.alpha_composite(rich([(title_txt, "mono", 26, (40, 130, 90))]), (40, 34))
    cell = (w - 80) // 7
    for i, dn in enumerate("LMMJVSD"):
        c.alpha_composite(rich([(dn, "semi", 24, GREY)]), (40 + i * cell + cell // 2 - 10, 90))
    for k in range(30):
        r, q = divmod(k, 7); x = 40 + q * cell; y = 140 + r * 62
        fill = None; fg = INK
        if k + 1 in highlight: fill = rgba(MINT); fg = WHITE
        if k + 1 in red: fill = rgba(RED); fg = WHITE
        if fill: d.rounded_rectangle((x + 4, y, x + cell - 4, y + 52), 12, fill=fill)
        t = rich([(str(k + 1), "semi", 26, fg)]); c.alpha_composite(t, (x + (cell - t.width) // 2, y + 8))
    return shadowed(c)

def phone(content, h=720):
    w = int(h * 0.5)
    body = rounded(w, h, (16, 20, 18, 255), 56, outline=(90, 100, 95, 255), width=4)
    scr = content.copy(); scr = scr.resize((w - 28, int(scr.height * (w - 28) / scr.width)))
    inner = Image.new("RGBA", (w - 28, h - 28), (10, 14, 12, 255))
    inner.alpha_composite(scr, (0, (inner.height - scr.height) // 2))
    m = Image.new("L", inner.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, inner.width - 1, inner.height - 1), 44, fill=255)
    inner.putalpha(m); body.alpha_composite(inner, (14, 14))
    ImageDraw.Draw(body).rounded_rectangle((w // 2 - 60, 26, w // 2 + 60, 50), 12, fill=(0, 0, 0, 255))
    return shadowed(body)

def icon_warn(s=120, col=RED):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(s / 2, 6), (s - 6, s - 10), (6, s - 10)], fill=rgba(col))
    t = rich([("!", "xbold", int(s * .55), WHITE)]); im.alpha_composite(t, ((s - t.width) // 2, int(s * .25)))
    return im

def bar_dyn(w, h, frac_fn, col_fn):
    cache = {}
    def f(tl):
        fr = round(frac_fn(tl), 3)
        if fr not in cache:
            im = rounded(w, h, (255, 255, 255, 40), h // 2)
            ww = max(h, int(w * fr)); ImageDraw.Draw(im).rounded_rectangle((0, 0, ww - 1, h - 1), h // 2, fill=rgba(col_fn(fr)))
            cache[fr] = im
        return cache[fr]
    return f

def counter(fn_val, fmt, size=200, col=WHITE, font="serif_i"):
    cache = {}
    def f(tl):
        v = fmt(fn_val(tl))
        if v not in cache: cache[v] = rich([(v, font, size, col)])
        return cache[v]
    return f

# ================================================================== STORYBOARD (58 scènes)
# ---- Partie 1 : introduction
@scene("Tu as déjà regardé", chrome=False)
def s1(S):
    t2 = S.w("Ça ici"); t3 = S.w("et le revendre")
    S.add(title("sur une plateforme chinoise…", [[B("Tu as déjà regardé", 100)], [I("un produit", 120)]]), CX, CY, 0.0, t1=t2, anim="up", sfx="S6", gain=-3)
    S.add(label_card("Prix fournisseur", [("3 $", "serif_i", 200, WHITE), ("/unité", "serif_i", 60, MUTED)], w=700), CX, CY, t2, t1=t3, anim="pop")
    S.add(pill("prix affiché", (47, 208, 138, 255), INK, 30), CX + 250, CY - 190, S.w("3 dollars"), t1=t3, anim="stamp", sfx="S10")
    S.add(vid("D8", 760, 430, "frame", w=760), 560, CY, t3, anim="left")
    S.add(title("", [[B("revendre", 100)], [I("chez moi.", 110)]]), 1380, CY - 30, S.w("revendre"), anim="up")
    S.add(stamp("FACILE ?", MINT, 56), 1380, CY + 160, S.w("facilement"), anim="stamp", sfx="S10")

@scene("Sur le papier", chrome=False)
def s2(S):
    t2 = S.w("Tu trouves")
    S.add(title("sur le papier,", [[B("tout paraît ", 120), I("simple.", 130)]]), CX, CY, S.t0, t1=t2, anim="up")
    items = [("Fournisseur", "D4", "trouves"), ("Produit", "D5", "choisis"), ("Paiement", "D3", "paies"), ("Colis", "D6", "colis")]
    xs = [360, 760, 1160, 1560]
    for (lab, code, wd), x in zip(items, xs):
        t = S.w(wd)
        S.add(vid(code, 0, 0, "tile", size=250), x, CY - 40, t, anim="pop", sfx="S10")
        S.add(rich([(lab, "bold", 40, WHITE)]), x, CY + 140, t + 0.05, anim="up")
    tv = S.w("tu commences")
    for k, x in enumerate(xs):
        S.add(check_box(56), x + 105, CY - 145, tv + 0.12 * k, anim="pop", dur=0.25, sfx="S13" if k == 0 else None, gain=-4)
    S.add(strike(1400, RED, 12), CX, CY - 40, S.t1 - 0.45, anim="none", sfx="S14", gain=-4)

@scene("Mais dans la réalité", bg="black", chrome=False, glitch=True)
def s3(S):
    S.add(hook("mais dans la réalité…", MUTED, 48), CX, CY - 150, S.t0, anim="fade", sfx="S2")
    S.add(rich([B("commander en Chine", 96)]), CX, CY - 40, S.w("commander en Chine"), anim="up")
    tp = S.w("parcours")
    S.add(rich([B("un parcours ", 120), I("du combattant.", 130, RED)]), CX, CY + 110, tp, anim="stamp", dur=0.3, sfx="S5", gain=-2)

@scene("Le produit reçu", chrome=False)
def s4(S):
    shots = [("différent", "D13", "DIFFÉRENT", "S14"), ("décevante", "D12", "DÉCEVANT", None), ("cesser de répondre", None, "SILENCE", "S15"),
             ("frais de transport", None, "FRAIS", "S16"), ("le colis", "D6", "RETARD", "S14")]
    times = [S.w("différent") - 0.6, S.w("la qualité"), S.w("le fournisseur"), S.w("les frais"), S.w("et le colis"), S.t1]
    for k, (wd, code, word, sx) in enumerate(shots):
        a, b = times[k], times[k + 1]
        if code in ("D13", "D12"):
            S.add(img_frame(code, 900 if code == "D13" else 760), 640, CY, a, t1=b, anim="pop", kb=1.05)
        elif word == "SILENCE":
            S.add(bubble(["Bonjour, des nouvelles", "de ma commande ?"], True), 640, CY - 120, a, t1=b, anim="up", sfx="S15")
            S.add(bubble(["Bonjour ?"], True), 760, CY + 60, a + 1.0, t1=b, anim="up")
            S.add(rich([("Vu · pas de réponse", "med", 30, MUTED)]), 760, CY + 170, a + 1.6, t1=b, anim="fade")
        elif word == "FRAIS":
            S.add(vid("D3", 0, 0, "tile", size=260), 460, CY, a, t1=b, anim="pop")
            S.add(label_card("Ton coût", [("+ transport", "serif_i", 110, WHITE)], w=560), 900, CY, a + 0.3, t1=b, anim="left")
        else:
            S.add(vid("D6", 700, 700, "tile", size=520), 640, CY, a, t1=b, anim="pop")
        S.add(rich([B(word, 120, RED if word in ("RETARD", "SILENCE") else WHITE)]), 1440, CY, S.w(wd), t1=b, anim="stamp", dur=0.3, sfx=sx)

@scene("Quand on débute", bg="grid", chrome=False)
def s5(S):
    t2 = S.w("Tu peux avoir")
    S.add(title("quand on débute avec un petit budget,", [[B("1 erreur", 130), I(" = capital bloqué.", 110)]], hcol=(220, 240, 230)), CX, CY - 40, S.w("une seule erreur"), t1=t2, anim="up", sfx="S10")
    S.add(stamp("BLOQUÉ", RED, 60), 1420, CY + 150, S.w("bloquer"), t1=t2, anim="stamp", sfx="S14")
    S.add(vid("D3", 0, 0, "tile", size=230), 380, CY, t2, anim="pop")
    lst = ["fournisseur vérifié", "échantillon demandé", "frais réels calculés"]
    ts = [S.w("vérifié"), S.w("demandé un échantillon"), S.w("calculé")]
    for k in range(4):
        tt = t2 if k == 0 else ts[k - 1]
        tn = ts[k] if k < 3 else S.t1
        S.add(checklist_card("Avant d'acheter", lst, k, w=820, marks=["x"] * 3), 1080, CY, tt, t1=tn, anim="up" if k == 0 else "none",
              sfx=None if k == 0 else ("S14" if k == 1 else "S20"), gain=-4)

@scene("Dans cette vidéo", chrome=False)
def s6(S):
    t2 = S.w("Nous parlerons")
    S.add(title("dans cette vidéo :", [[B("les obstacles", 110)], [I("et les solutions.", 110)]]), CX, CY, S.t0, t1=t2, anim="up")
    names = [("01", "Fournisseurs", "fournisseurs"), ("02", "Communication", "communication"), ("03", "Qualité", "qualité"),
             ("04", "Frais cachés", "frais cachés"), ("05", "Délais", "délais"), ("06", "Arnaques", None), ("07", "Rentabilité", None)]
    pos = [(420, 330), (800, 330), (1180, 330), (1560, 330), (610, 630), (990, 630), (1370, 630)]
    tl = S.w("délais")
    for k, ((n, nm, wd), (x, y)) in enumerate(zip(names, pos)):
        t = S.w(wd) if wd else t2 + 0.3 + 0.2 * (k - 5)
        c = card(340, 210); c.alpha_composite(rich([(n, "serif_i", 64, MINT)]), (30, 22)); c.alpha_composite(rich([(nm, "bold", 38, WHITE)]), (32, 130))
        S.add(shadowed(c), x, y, t, anim="pop", sfx="S10" if wd and k % 2 == 0 else None, gain=-4)

@scene("Avant de commander ton prochain stock", bg="cream", chrome=False)
def s7(S):
    tv = S.w("le vrai défi")
    S.add(title("retiens déjà ceci :", [[B("trouver un produit", 96, INK)], [I("bon marché ?", 110, (40, 130, 90))]], hcol=GREY), CX, CY, S.t0, t1=tv, anim="up")
    S.add(strike(820, RED, 10), CX, CY + 70, S.w("n'est pas seulement") + 0.3, t1=tv, anim="none")
    S.add(img_frame("D11", 980), 620, CY, tv, anim="fade", kb=1.06)
    S.add(hook("le vrai défi :", GREY, 46), 1500, CY - 200, tv, anim="up")
    for k, (lab, wd) in enumerate([("bon produit", "le bon produit"), ("bon prix", "au bon prix"), ("bons délais", "dans les bons délais")]):
        S.add(pill(lab, (24, 30, 27, 255), WHITE, 44, icon=check_box(40)), 1500, CY - 90 + k * 120, S.w(wd), anim="left", sfx="S13", gain=-6)

# ---- Partie 2 : fournisseur
@scene("Trouver un fournisseur réellement fiable", ob=1)
def s8(S): obstacle_card(S, 1, "Un fournisseur", "fiable.", "VÉRIFIE", sub="à qui peux-tu faire confiance ?", sub_t=S.w("à qui"))

@scene("Sur internet beaucoup", ob=1)
def s9(S):
    S.add(img_frame("D10", 900), 560, CY, S.t0, anim="fade", kb=1.10)
    for k, (lab, wd) in enumerate([("belles photos", "belles photos"), ("prix attractifs", "prix attractifs"), ("descriptions pro", "descriptions")]):
        S.add(pill(lab, (255, 255, 255, 240), INK, 40), 1430, CY - 200 + k * 110, S.w(wd), anim="left", sfx="S10" if k != 1 else None, gain=-5)
    S.add(stamp("BELLE PAGE ≠ FIABLE", RED, 50), 1400, CY + 200, S.w("ne garantit"), anim="stamp", sfx="S14", gain=-3)

@scene("Certains fournisseurs sont sérieux", ob=1)
def s10(S):
    cols = [("Sérieux", check_box(90), "sérieux", "S13"), ("Intermédiaire", None, "intermédiaires", "S20"), ("Fausses images", cross_mark(90), "fausses images", "S14")]
    for k, (lab, ic, wd, sx) in enumerate(cols):
        c = card(460, 420)
        if ic is None:
            ic = Image.new("RGBA", (180, 90), (0, 0, 0, 0)); d = ImageDraw.Draw(ic)
            for j in range(3): d.ellipse((j * 70, 25, j * 70 + 40, 65), fill=rgba(MINT if j != 1 else (240, 180, 80)))
            d.line([(40, 45), (70, 45)], fill=WHITE, width=5); d.line([(110, 45), (140, 45)], fill=WHITE, width=5)
        c.alpha_composite(ic, ((460 - ic.width) // 2, 90))
        t = rich([(lab, "bold", 46, WHITE)]); c.alpha_composite(t, ((460 - t.width) // 2, 260))
        S.add(shadowed(c), 450 + k * 510, CY, S.w(wd), anim="up", sfx=sx, gain=-4)

@scene("Le prix le plus bas", bg="grid", ob=1)
def s11(S):
    t2 = S.w("Un tarif")
    S.add(title("", [[B("le prix le plus bas", 110)], [I("≠ la meilleure affaire.", 110, WHITE)]]), CX, CY, S.t0, t1=t2, anim="up", sfx="S12", gain=-4)
    hs = [300, 280, 320, 70]
    for k, hh in enumerate(hs):
        col = RED if k == 3 else (255, 255, 255)
        bar = rounded(150, hh, rgba(col, 230), 14)
        S.add(bar, 560 + k * 220, 740 - hh // 2, t2 + 0.15 * k, anim="up", dur=0.4)
        S.add(rich([(f"fournisseur {'ABCD'[k]}", "mono", 22, (230, 245, 238))]), 560 + k * 220, 780, t2 + 0.15 * k, anim="fade")
    S.add(rich([("?", "serif_i", 160, RED)]), 1220, 560, S.w("beaucoup plus bas"), anim="pop", sfx="S14", gain=-6)
    S.add(pill("prix trop bas = questions", (20, 30, 26, 255), WHITE, 40), 1440, 300, S.w("questions"), anim="stamp")

@scene("Avant de commander vérifie", ob=1)
def s12(S):
    items = ["Ancienneté du fournisseur", "Photos et vidéos réelles", "Quantités minimales", "Délais de production", "Conditions de paiement"]
    wds = ["ancienneté", "des photos", "quantités minimales", "délais de production", "conditions de paiement"]
    ts = [S.w(w) for w in wds]
    for k in range(6):
        a = S.t0 if k == 0 else ts[k - 1] + 0.25
        b = ts[k] + 0.25 if k < 5 else S.t1
        S.add(checklist_card("Checklist fournisseur", items, k, w=860), CX, CY, a, t1=b, anim="up" if k == 0 else "none",
              sfx=None if k == 0 else "S20", gain=-5)
    keys = [(S.t0, 1500, 900)]
    for k, t in enumerate(ts): keys += [(t - 0.05, 625, 268 + k * 70), (t + 0.25, 625, 268 + k * 70)]
    S.cursor(keys, [t + 0.2 for t in ts])

@scene("demande également une vidéo récente", ob=1)
def s13(S):
    scr = drive_image("D12").crop((190, 0, 560, 493)); dd = ImageDraw.Draw(scr)
    dd.ellipse((scr.width - 130, 20, scr.width - 100, 50), fill=rgba(RED))
    ph = phone(scr, 700)
    S.add(ph, 520, CY, S.t0, anim="up", sfx="S4", gain=-5)
    S.add(title("", [[B("demande une", 80)], [I("vidéo récente.", 96)]]), 1280, CY - 250, S.t0 + 0.2, anim="up")
    for k, (lab, wd) in enumerate([("plusieurs pièces", "plusieurs pièces"), ("l'emballage", "emballage"), ("les détails", "détails")]):
        S.add(pill(lab, (255, 255, 255, 240), INK, 40, icon=check_box(38)), 1280, CY - 40 + k * 110, S.w(wd), anim="left", sfx="S13" if k == 0 else None, gain=-6)
    S.add(stamp("LE PRODUIT EXISTE", MINT, 46), 1290, CY + 320, S.w("existe réellement"), anim="stamp", sfx="S10")

@scene("Et surtout ne commence pas", bg="cream", ob=1)
def s14(S):
    tg = S.w("grosse commande"); tt = S.w("Fais d'abord")
    c = card(560, 600, light=True)
    c.alpha_composite(rich([("GROSSE COMMANDE", "mono", 26, RED)]), (40, 34))
    S.add(shadowed(c), 1340, CY, tg, anim="pop")
    S.add(vid("D9", 300, 440, "frame", 0, 7.5, w=300), 1340, CY + 40, tg + 0.05, anim="fade")
    S.add(cross_mark(90), 1560, CY - 260, tg + 0.5, anim="stamp", sfx="S14", gain=-4)
    c2 = card(560, 600, light=True); c2.alpha_composite(rich([("PETITE COMMANDE", "mono", 26, (40, 130, 90))]), (40, 34))
    S.add(shadowed(c2), 580, CY, tt, anim="pop")
    S.add(vid("D4", 0, 0, "tile", size=260), 580, CY - 40, tt + 0.05, anim="pop")
    S.add(stamp("TEST", MINT, 70), 580, CY + 190, tt + 0.3, anim="stamp", sfx="S13", gain=-4)
    pl = [(pill(lab, (24, 30, 27, 255), WHITE, 32, icon=check_box(32)), S.w(wd)) for lab, wd in [("communication", "la communication"), ("qualité", "la qualité"), ("ponctualité", "ponctualité")]]
    x = 580 - (sum(p.width for p, _ in pl) + 20 * 2) / 2
    for p, t in pl:
        S.add(p, x, CY + 360, t, anim="up", anchor="l"); x += p.width + 20

@scene("Règle simple", bg="black", chrome=False)
def s15(S):
    S.add(hook("règle simple :", MUTED, 50), CX, CY - 170, S.t0, anim="fade")
    S.add(rich([B("Teste le fournisseur", 110)]), CX, CY - 40, S.w("teste le fournisseur"), anim="up")
    S.add(rich([B("avant de tester ", 110), I("ton capital.", 120)]), CX, CY + 110, S.w("avant de tester"), anim="up", sfx="S5", gain=-3)

# ---- Partie 3 : langue
@scene("La barrière linguistique", ob=2)
def s16(S): obstacle_card(S, 2, "La barrière", "de la langue.", "ÉCRIS TOUT", sub="le deuxième obstacle : la communication", sub_t=S.w("Le deuxième"))

@scene("Une mauvaise traduction", ob=2)
def s17(S):
    S.add(img_frame("D14", 860), CX, CY + 20, S.t0, anim="fade", kb=1.06)
    words = [("couleur", 380, 230), ("taille", 1540, 230), ("matière", 300, 520), ("modèle", 1620, 520), ("quantité", 420, 800), ("emballage", 1500, 800)]
    for k, (wd, x, y) in enumerate(words):
        S.add(pill(wd.upper(), (20, 30, 26, 245), WHITE, 40, fn="bold"), x, y, S.w(wd), anim="pop", sfx="S10" if k % 2 == 0 else None, gain=-6)

@scene("Tu peux penser avoir commandé", bg="cream", ob=2)
def s18(S):
    S.add(img_frame("D13", 860), 520, CY, S.t0, anim="fade", kb=1.05)
    S.add(pill("100 pièces noires", (24, 30, 27, 255), WHITE, 42, icon=check_box(40)), 1490, CY - 200, S.w("100 pièces"), anim="left")
    S.add(pill("emballage individuel", (24, 30, 27, 255), WHITE, 42), 1490, CY - 90, S.w("emballage individuel"), anim="left")
    S.add(stamp("ERREUR", RED, 70), 1490, CY + 60, S.w("compris autre chose"), anim="stamp", sfx="S14", gain=-3)
    S.add(rich([("petite confusion → ", "semi", 40, GREY), ("grosse perte.", "serif_i", 50, RED)]), 1440, CY + 230, S.w("Une petite confusion"), anim="up")

@scene("Pour éviter cela", ob=2)
def s19(S):
    S.add(title("pas de conversation vague :", [[B("écris", 120)], [I("tout.", 130)]]), 480, CY, S.t0, anim="up")
    rows = [("Quantité", "100 pièces", "la quantité"), ("Couleur", "noir", "la couleur"), ("Dimensions", "20 × 12 cm", "les dimensions"),
            ("Matériau", "coton", "le matériau"), ("Logo", "1 couleur", "le logo"), ("Emballage", "individuel", "type d'emballage"), ("Délai", "à confirmer", "le délai")]
    ts = [S.w(r[2]) for r in rows]
    def sheet(tl):
        t = S._t0c + tl
        c = card(860, 640, light=True)
        c.alpha_composite(rich([("FICHE PRODUIT · À ENVOYER", "mono", 24, (40, 130, 90))]), (44, 36))
        for k, (lab, val, _) in enumerate(rows):
            if t < ts[k]: break
            n = int(clamp((t - ts[k]) / 0.5) * len(val))
            y = 100 + k * 74
            c.alpha_composite(rich([(lab, "semi", 32, GREY)]), (44, y)); c.alpha_composite(rich([(val[:n], "bold", 32, INK)]), (330, y))
            ImageDraw.Draw(c).line([(44, y + 60), (816, y + 60)], fill=(230, 230, 225, 255), width=2)
        return shadowed(c)
    S._t0c = S.w("Écris toutes")
    S.add(sheet, 1300, CY, S._t0c, anim="up", sfx="S19", gain=-8)

@scene("Ajoute des photos", ob=2)
def s20(S):
    S.add(img_frame("D15", 560), 560, CY, S.t0, anim="up", sfx="S4", gain=-6, kb=1.04)
    for k, (lab, wd) in enumerate([("photos annotées", "photos annotées"), ("mesures précises", "mesures"), ("maquette du logo", "maquette")]):
        S.add(pill(lab, (255, 255, 255, 240), INK, 44, icon=check_box(40)), 1300, CY - 150 + k * 140, S.w(wd), anim="left", sfx="S13" if k == 2 else None, gain=-6)

@scene("Ensuite reformule", ob=2)
def s21(S):
    tr = S.w("reformule"); tc = S.w("confirmer chaque"); tl = S.w("Cette étape")
    S.add(bubble(["Récapitulatif de ma commande :", "100 pièces · noir · 20 × 12 cm", "logo 1 couleur · emballage individuel"], True, 760), 1140, 330, tr, t1=tl, anim="up", sfx="S15", gain=-5)
    S.add(bubble(["Confirmé ✓ pour chaque point"], False), 660, 560, tc + 0.4, t1=tl, anim="up", sfx="S13", gain=-5)
    btn = pill("Envoyer", (47, 208, 138, 255), INK, 34, fn="bold")
    S.add(btn, 1400, 520, tr + 0.2, t1=tl, anim="pop")
    S.cursor([(tr - 0.2, 1700, 900), (tr + 1.4, 1405, 525), (tc, 1405, 525), (tc + 0.6, 1600, 820)], [tr + 1.55])
    S.add(title("", [[B("5 minutes", 100)], [I("de vérification…", 90)]]), 520, CY, tl, anim="up")
    S.add(vid("D9", 360, 520, "frame", 0, 7.5, w=360), 1360, CY, S.w("plusieurs cartons"), anim="pop")
    S.add(stamp("DÉJÀ EXPÉDIÉ", RED, 48), 1360, CY + 330, S.w("expédiés"), anim="stamp", sfx="S14", gain=-4)

# ---- Partie 4 : qualité
@scene("Recevoir une qualité différente", ob=3)
def s22(S): obstacle_card(S, 3, "La qualité", "du produit.", "ÉCHANTILLON", sub="ce que tu vois ≠ ce que tu reçois", sub_t=S.w("Troisième obstacle"))

@scene("Les photos publiées en ligne", bg="cream", ob=3)
def s23(S):
    tr = S.w("Le produit réel")
    for x, lab, col in [(560, "EN LIGNE", (40, 130, 90)), (1360, "EN VRAI", RED)]:
        c = card(640, 620, light=True); c.alpha_composite(rich([(lab, "mono", 30, col)]), (44, 36))
        S.add(shadowed(c), x, CY, S.t0 if x == 560 else tr, anim="pop")
    for k, (lab, wd) in enumerate([("bonne lumière", "bonne lumière"), ("angle avantageux", "angle avantageux"), ("retouche", "retouche")]):
        S.add(pill(lab, (47, 208, 138, 255), INK, 40, icon=check_box(38, col=(24, 30, 27))), 560, CY - 130 + k * 110, S.w(wd), anim="left", sfx="S10" if k == 0 else None, gain=-6)
    for k, (lab, wd) in enumerate([("plus petit", "plus petit"), ("plus fragile", "plus fragile"), ("moins bien fini", "moins bien"), ("autre matière", "matière différente")]):
        S.add(pill(lab, (255, 235, 232, 255), RED, 40), 1360, CY - 170 + k * 100, S.w(wd), anim="right", sfx="S14" if k == 0 else None, gain=-6)
    S.add(rich([B("≠", 140, INK)]), CX, CY, tr, anim="pop")

@scene("C'est pourquoi il ne faut pas commander", ob=3)
def s24(S):
    te = S.w("un échantillon")
    S.add(img_frame("D13", 760), 620, CY, S.t0, t1=te, anim="fade")
    S.add(title("", [[B("une grande quantité", 80)], [I("sur une photo ?", 90, RED)]]), 1390, CY, S.w("une grande quantité"), t1=te, anim="up")
    S.add(hook("la meilleure solution :", MUTED, 50), CX, CY - 180, S.w("La meilleure solution"), anim="fade")
    S.add(stamp("ÉCHANTILLON", MINT, 120, -4), CX, CY + 20, te, anim="stamp", dur=0.35, sfx="S12", gain=-3)

@scene("Il te permettra de vérifier", ob=3)
def s25(S):
    items = ["Taille", "Matière", "Solidité", "Finition", "Couleur", "Emballage"]
    wds = ["la taille", "la matière", "la solidité", "la finition", "la couleur", "emballage"]
    ts = [S.w(w) for w in wds]; tcl = S.w("montrer")
    for k in range(7):
        a = S.t0 if k == 0 else ts[k - 1] + 0.2
        b = ts[k] + 0.2 if k < 6 else tcl
        S.add(checklist_card("Contrôle de l'échantillon", items, k, w=640), 560, CY, a, t1=b, anim="up" if k == 0 else "none",
              sfx="S13" if k in (1, 6) else None, gain=-7)
    keys = [(S.t0, 1200, 900)]
    for k, t in enumerate(ts): keys += [(t - 0.05, 302, 268 + k * 70), (t + 0.2, 302, 268 + k * 70)]
    keys.append((tcl - 0.01, 302, 650))
    S.cursors.append(Cursor(keys, [t + 0.15 for t in ts], tcl))
    S.add(vid("D8", 820, 460, "frame", w=820), 1360, CY - 60, S.t0 + 0.3, t1=tcl, anim="fade")
    S.add(vid("D8", 760, 430, "frame", w=760), 1380, CY - 40, tcl, anim="none")
    S.add(pill("avis de clients potentiels", (255, 255, 255, 240), INK, 40), 1380, CY + 230, tcl + 0.2, anim="up", sfx="S10", gain=-6)
    S.add(rich([I("avant d'acheter davantage", 54, WHITE)]), 500, CY, tcl + 0.4, anim="up")

@scene("doit porter ton logo", ob=3)
def s26(S):
    tm = S.w("maquette")
    prod = rounded(420, 420, (232, 228, 220, 255), 40)
    c = card(620, 640, light=True); c.alpha_composite(rich([("MAQUETTE AVANT PRODUCTION", "mono", 24, (40, 130, 90))]), (40, 34)); c.alpha_composite(prod, (100, 130))
    S.add(shadowed(c), 640, CY, S.t0, anim="pop")
    logo = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); d = ImageDraw.Draw(logo)
    d.ellipse((0, 0, 179, 179), fill=rgba((24, 30, 27))); t = rich([("TON", "xbold", 40, WHITE)]); logo.alpha_composite(t, ((180 - t.width) // 2, 40))
    t = rich([("logo", "serif_i", 44, MINT)]); logo.alpha_composite(t, ((180 - t.width) // 2, 88))
    S.add(logo, 640, CY + 50, tm, anim="stamp", sfx="S4", gain=-5)
    S.add(pill("échantillon personnalisé", (255, 255, 255, 240), INK, 42, icon=check_box(40)), 1380, CY - 60, S.w("personnalisé"), anim="left", sfx="S13", gain=-6)
    S.add(rich([I("avant de lancer la production", 56, WHITE)]), 1380, CY + 80, S.w("avant de lancer"), anim="up")

@scene("Pour une commande importante", ob=3)
def s27(S):
    S.add(img_frame("D12", 780), 540, CY, S.t0, anim="fade", kb=1.07)
    S.add(title("", [[B("inspection", 80)], [I("avant expédition.", 84)]]), 1320, CY - 230, S.w("inspection"), anim="up", sfx="S3", gain=-6)
    items = ["Quantité", "État des produits", "Conformité à la commande"]; wds = ["la quantité", "l'état", "conformité"]
    ts = [S.w(w) for w in wds]
    for k in range(4):
        a = S.w("Elle permet") if k == 0 else ts[k - 1] + 0.2
        b = ts[k] + 0.2 if k < 3 else S.t1
        S.add(checklist_card("Inspection", items, k, w=700), 1320, CY + 110, a, t1=b, anim="up" if k == 0 else "none", sfx="S13" if k == 3 else None, gain=-7)

@scene("Définis les critères", bg="cream", ob=3)
def s28(S):
    tq = S.w("Dire"); ta = S.w("acceptes")
    S.add(title("avant de payer,", [[B("définis tes ", 96, INK), I("critères.", 104, (40, 130, 90))]], hcol=GREY), CX, CY, S.t0, t1=tq, anim="up")
    S.add(rich([("« je veux une bonne qualité »", "serif_i", 90, INK)]), CX, CY - 60, tq, t1=ta, anim="up")
    S.add(strike(1150, RED, 10), CX, CY - 40, S.w("trop vague"), t1=ta, anim="none", sfx="S14", gain=-5)
    S.add(rich([B("trop vague.", 60, RED)]), CX, CY + 80, S.w("trop vague") + 0.2, t1=ta, anim="up")
    for x, lab, col, items, wd, sx in [(600, "ACCEPTÉ", (40, 130, 90), ["conforme à l'échantillon", "dimensions respectées"], "acceptes", "S13"),
                                        (1320, "REFUSÉ", RED, ["défaut visible", "couleur différente"], "refuses", "S14")]:
        S.add(checklist_card(lab, items, 2, w=620, title_col=col, marks=["ok", "ok"] if col != RED else ["x", "x"]), x, CY, S.w(wd), anim="up", sfx=sx, gain=-6)

@scene("Un échantillon coûte quelques dollars", ob=3)
def s29(S):
    S.add(label_card("Un échantillon", [("quelques $", "serif_i", 100, MINT)], w=560), 520, CY, S.t0, anim="pop", sfx="S16", gain=-7)
    tb = S.w("Un stock entier")
    S.add(label_card("Un stock entier raté", [("ton activité.", "serif_i", 110, RED)], w=820), 1320, CY, tb, anim="pop")
    S.add(icon_warn(110), 1660, CY - 170, S.w("activité"), anim="stamp", sfx="S5", gain=-3)

# ---- Partie 5 : frais cachés
@scene("Les frais cachés qui changent", ob=4)
def s30(S): obstacle_card(S, 4, "Les frais", "cachés.", "FRAIS CACHÉS")

@scene("Beaucoup de débutants regardent", bg="grid", ob=4)
def s31(S):
    S.add(vid("D2", 0, 0, "tile", size=240), 360, CY, S.t0, anim="pop")
    S.add(label_card("Prix affiché", [("3 $", "serif_i", 220, WHITE)], w=620), 960, CY, S.w("3 dollars"), anim="pop", sfx="S16", gain=-6)
    S.add(pill("« grande marge ! »", (255, 255, 255, 240), INK, 40), 1500, CY - 170, S.w("grande marge"), anim="left")
    S.add(stamp("≠ COÛT RÉEL", RED, 64), 1440, CY + 120, S.w("pas toujours le coût réel"), anim="stamp", sfx="S12", gain=-4)

@scene("Il faut parfois ajouter", ob=4)
def s32(S):
    S.add(img_frame("D11", 1000), CX, CY - 110, S.t0, anim="fade", kb=1.05)
    fees = [("+ usine → entrepôt", "le transport entre"), ("+ regroupement", "regroupement"), ("+ transport international", "transport international"),
            ("+ douane", "douane"), ("+ livraison locale", "livraison locale"), ("+ agent", "agent"), ("+ change", "change")]
    pos = [(330, 820), (760, 820), (1260, 820), (1680, 820), (480, 930), (960, 930), (1380, 930)]
    pos = [(250, 200), (250, 340), (250, 480), (250, 620), (1670, 200), (1670, 340), (1670, 480)]
    for k, ((lab, wd), (x, y)) in enumerate(zip(fees, pos)):
        S.add(pill(lab, (224, 90, 79, 255), WHITE, 32, fn="bold"), x, y, S.w(wd), anim="left" if x < CX else "right", sfx="S11" if k % 2 == 0 else None, gain=-7)

@scene("Utilise cette formule", bg="grid", ob=4)
def s33(S):
    S.add(hook("la formule simple :", (220, 240, 230), 50), CX, 230, S.t0, anim="fade")
    terms = [("COÛT RÉEL =", "coût réel", MINT), ("prix du produit", "prix du produit", WHITE), ("+ transport", "plus transport", WHITE),
             ("+ frais de service", "frais de service", WHITE), ("+ douane", "douane", WHITE), ("+ livraison locale", "livraison locale", WHITE)]
    pos = [(560, 400), (1240, 400), (560, 560), (1240, 560), (560, 720), (1240, 720)]
    for k, ((lab, wd, col), (x, y)) in enumerate(zip(terms, pos)):
        im = rich([(lab, "xbold" if k == 0 else "serif_i", 80 if k == 0 else 76, col)])
        S.add(im, x, y, S.w(wd), anim="up", sfx="S17" if k % 2 == 0 else None, gain=-6)

@scene("Prenons un exemple", bg="grid", ob=4)
def s34(S):
    S.add(hook("prenons un exemple :", (220, 240, 230), 50), CX, 230, S.t0, anim="fade")
    t3, t2, t5, tn = S.w("3 dollars"), S.w("2 dollars"), S.w("5 dollars"), S.w("non de 3")
    S.add(big_num("3 $"), 420, CY, t3, anim="pop", sfx="S17", gain=-6)
    S.add(big_num("+ 2 $"), 900, CY, t2, anim="pop", sfx="S17", gain=-6)
    S.add(big_num("= 5 $", c=MINT), 1440, CY, t5, anim="stamp", sfx="S12", gain=-3)
    S.add(strike(240, RED, 12), 420, CY + 10, tn, anim="none")
    S.add(stamp("+2 $", RED, 60), 900, CY + 200, tn + 0.3, anim="stamp")

@scene("Si tu le revends 7 dollars", ob=4)
def s35(S):
    tp = S.w("la publicité"); tl = S.w("la livraison"); td = S.w("défectueux"); tf = S.w("très faible")
    S.add(label_card("Prix de vente", [("7 $", "serif_i", 150, WHITE)], w=480), 440, CY - 100, S.t0, anim="pop", sfx="S16", gain=-7)
    S.add(vid("D3", 0, 0, "tile", size=200), 440, CY + 230, S.t0 + 0.2, anim="pop")
    def frac(tl_):
        t = S.t0 + tl_
        f = 1.0
        for tt, v in [(tp, 0.72), (tl, 0.5), (td, 0.3), (tf, 0.12)]:
            if t >= tt: f = v if t >= tt + 0.4 else f - (f - v) * ease_out((t - tt) / 0.4)
        return f
    S.add(rich([("MARGE · 2 $ AU DÉPART", "mono", 26, MINT)]), 820, CY - 170, S.w("marge apparente"), anim="fade", anchor="l")
    S.add(bar_dyn(900, 70, frac, lambda f: MINT if f > 0.35 else RED), 820, CY - 90, S.w("marge apparente"), anim="left", anchor="l")
    x = 820
    for k, (lab, t) in enumerate([("− publicité", tp), ("− livraison client", tl), ("− produits défectueux", td)]):
        p = pill(lab, (255, 235, 232, 255), RED, 34)
        S.add(p, x, CY + 40, t, anim="up", anchor="l", sfx="S16" if k == 0 else None, gain=-7); x += p.width + 18
    S.add(rich([B("marge réelle ", 70), I("très faible.", 80, RED)]), 820, CY + 190, tf, anim="up", anchor="l")

@scene("Avant de commander demande-toi", ob=4)
def s36(S):
    S.add(vid("D7", 560, 560, "tile", size=560), 520, CY, S.t0, anim="fade")
    q = stack([rich([("« Combien me coûtera", "serif_i", 72, MINT)]), rich([("ce produit une fois arrivé", "serif_i", 72, MINT)]), rich([("dans mon pays ? »", "serif_i", 72, MINT)])], 6, "left")
    S.add(q, 1000, CY - 60, S.w("combien me coûtera"), anim="up", anchor="l", sfx="S3", gain=-6)
    S.add(pill("la question qui protège ta rentabilité", (255, 255, 255, 240), INK, 34), 1000, CY + 170, S.w("cette question"), anim="up", anchor="l")

# ---- Partie 6 : délais
@scene("Les retards de production", ob=5)
def s37(S): obstacle_card(S, 5, "Les délais", "de livraison.", "MARGE DE SÉCURITÉ", sub="le cinquième obstacle", sub_t=S.w("Le cinquième"))

@scene("Un fournisseur peut annoncer", ob=5)
def s38(S):
    S.add(calendar_card(highlight=range(1, 8)), 600, CY, S.t0, anim="pop")
    S.add(rich([I("7 jours ?", 200, WHITE)]), 1340, CY, S.w("7 jours"), anim="stamp", sfx="S10")

@scene("Mais il faut distinguer", ob=5)
def s39(S):
    steps = [("Production", "D4", "délai de production"), ("Préparation", "D5", "délai de préparation"), ("Transport", "D7", "délai de transport"), ("Livraison", "D6", "délai de livraison")]
    for k, (lab, code, wd) in enumerate(steps):
        t = S.w(wd); x = 330 + k * 420
        S.add(vid(code, 0, 0, "tile", size=250), x, CY - 40, t, anim="pop", sfx="S11", gain=-7)
        S.add(rich([(f"{k + 1}. {lab}", "bold", 40, WHITE)]), x, CY + 140, t + 0.05, anim="up")
        if k: S.add(rich([("→", "bold", 70, MINT)]), x - 210, CY - 40, t, anim="left")

@scene("Si tu confonds ces étapes", ob=5)
def s40(S):
    ts = S.w("saisonnier")
    S.add(calendar_card(highlight=(12,), red=(20,)), 560, CY, S.t0, t1=ts, anim="pop")
    S.add(pill("date promise", (47, 208, 138, 255), INK, 40), 1300, CY - 100, S.w("promettre"), t1=ts, anim="left")
    S.add(pill("date réelle", (224, 90, 79, 255), WHITE, 40), 1300, CY + 20, S.w("respecter"), t1=ts, anim="left", sfx="S14", gain=-5)
    S.add(vid("D8", 820, 460, "frame", w=820), 600, CY, ts, anim="fade")
    for k, (lab, wd) in enumerate([("produit saisonnier", "saisonnier"), ("promotion", "promotion"), ("commandes encaissées", "encaissé")]):
        S.add(pill(lab, (255, 235, 232, 255), RED, 40), 1420, CY - 140 + k * 120, S.w(wd), anim="left")

@scene("demande donc un calendrier clair", ob=5)
def s41(S):
    items = ["Calendrier clair", "Stock disponible ou à fabriquer ?", "Délai pour chaque étape"]; wds = ["calendrier clair", "disponible", "pour chaque étape"]
    ts = [S.w(w) for w in wds]
    for k in range(4):
        a = S.t0 if k == 0 else ts[k - 1] + 0.25
        b = ts[k] + 0.25 if k < 3 else S.t1
        S.add(checklist_card("À demander au fournisseur", items, k, w=880), CX, CY, a, t1=b, anim="up" if k == 0 else "none", sfx=None if k == 0 else "S13", gain=-7)
    keys = [(S.t0, 1500, 900)]
    for k, t in enumerate(ts): keys += [(t - 0.05, 595, 410 + k * 70), (t + 0.25, 595, 410 + k * 70)]
    S.cursor(keys, [t + 0.2 for t in ts])

@scene("Commande suffisamment tôt", ob=5)
def s42(S):
    t30 = S.w("30 jours"); tm = S.w("marge de sécurité")
    S.add(title("", [[B("commande ", 90), I("tôt.", 100)]]), CX, 250, S.t0, anim="up")
    for k in range(30):
        S.add(rounded(36, 90, rgba(WHITE, 220), 8), 330 + k * 42, CY + 20, S.t0 + 0.3 + k * 0.03, anim="up", dur=0.25)
    S.add(rounded(260, 90, rgba(MINT, 255), 8), 330 + 30 * 42 + 112, CY + 20, tm, anim="left", sfx="S13", gain=-6)
    S.add(rich([("+ marge de sécurité", "bold", 34, MINT)]), 1640, CY - 60, tm + 0.1, anim="up")
    S.add(rich([I("30 jours", 120, WHITE)]), 950, CY - 120, t30, anim="pop", sfx="S10", gain=-5)
    S.add(pill("pas de date promise sans confirmation", (224, 90, 79, 255), WHITE, 36), CX, CY + 220, S.w("ne promets jamais"), anim="up")
    S.add(pill("transporteur ou agent ✓", (255, 255, 255, 240), INK, 36, icon=check_box(34)), CX, CY + 330, S.w("transporteur"), anim="up", sfx="S13", gain=-6)

# ---- Partie 7 : arnaques
@scene("Les arnaques et les paiements risqués", ob=6, glitch=True)
def s43(S): obstacle_card(S, 6, "Les arnaques", "et paiements risqués.", "ARNAQUE", red=True)

@scene("Méfie-toi d'un fournisseur", ob=6)
def s44(S):
    items = ["Pression pour payer vite", "Refuse de répondre", "Change de compte bancaire", "Bénéficiaire ≠ entreprise", "Refuse l'échantillon", "Prix trop beau pour être vrai"]
    wds = ["pression excessive", "refuse de répondre", "compte bancaire", "nom du bénéficiaire", "refuse d'envoyer", "trop beau"]
    ts = [S.w(w) for w in wds]
    S.add(icon_warn(150), 380, CY - 40, S.t0, anim="pop", sfx="S8", gain=-10)
    S.add(rich([("SIGNAUX", "xbold", 60, RED)]), 380, CY + 110, S.t0 + 0.1, anim="up")
    S.add(rich([("D'ALERTE", "serif_i", 64, WHITE)]), 380, CY + 180, S.t0 + 0.15, anim="up")
    for k in range(7):
        a = S.t0 if k == 0 else ts[k - 1]
        b = ts[k] if k < 6 else S.t1
        S.add(checklist_card("Méfie-toi si le fournisseur…", items, k, w=900, light=False, title_col=RED, marks=["x"] * 6), 1200, CY, a, t1=b,
              anim="up" if k == 0 else "none", sfx=None if k in (0, 6) else "S14", gain=-9)
    S.add(stamp("ARNAQUE", RED, 80), 1450, CY + 300, ts[5] + 0.6, anim="stamp", sfx="S12", gain=-5)

@scene("Avant de payer vérifie", ob=6)
def s45(S):
    S.add(img_frame("D10", 820), 520, CY, S.t0, anim="fade", kb=1.10)
    items = ["Vérifie l'entreprise", "Garde factures et captures", "Paiement protégé"]; wds = ["vérifie les informations", "conserve les factures", "moyen de paiement"]
    ts = [S.w(w) for w in wds]
    for k in range(4):
        a = S.t0 if k == 0 else ts[k - 1] + 0.25
        b = ts[k] + 0.25 if k < 3 else S.t1
        S.add(checklist_card("Protège ton argent", items, k, w=760), 1340, CY - 40, a, t1=b, anim="up" if k == 0 else "none",
              sfx=None if k == 0 else ("S18" if k == 3 else "S13"), gain=-7)
    keys = [(S.t0, 1800, 950)]
    for k, t in enumerate(ts): keys += [(t - 0.05, 1027, 384 + k * 70), (t + 0.25, 1027, 384 + k * 70)]
    S.cursor(keys, [t + 0.2 for t in ts])
    S.add(stamp("VÉRIFIÉ", MINT, 70), 1380, CY + 260, S.w("protection"), anim="stamp", sfx="S10", gain=-4)

@scene("Évite de transférer", ob=6)
def s46(S):
    ta = S.w("Avance par étapes")
    S.add(title("", [[B("tout ton capital", 96)], [I("à un fournisseur jamais testé ?", 80, RED)]]), CX, CY, S.t0, t1=ta, anim="up", sfx="S14", gain=-6)
    steps = [("Vérification", "vérification"), ("Échantillon", "échantillon"), ("Petite commande", "petite commande"), ("Grande commande", "commande plus importante")]
    for k, (lab, wd) in enumerate(steps):
        x = 300 + k * 440; y = 780 - k * 130
        st = rounded(400, 110, rgba(MINT if k < 3 else WHITE, 255 if k < 3 else 230), 18)
        t = rich([(f"{k + 1}. {lab}", "bold", 36, INK)]); st.alpha_composite(t, ((400 - t.width) // 2, (110 - t.height) // 2))
        S.add(shadowed(st), x, y, S.w(wd), anim="up", sfx="S11", gain=-7)
    S.add(hook("avance par étapes :", MUTED, 50), 520, 300, ta, anim="fade")

@scene("La confiance se construit", ob=6)
def s47(S):
    S.add(title("", [[B("la confiance", 110)], [I("se construit.", 120)]]), CX, 330, S.t0, anim="up", sfx="S3", gain=-6)
    tp = S.w("trois belles photos")
    for k, code in enumerate(["D13", "D10", "D12"]):
        S.add(img_frame(code, 420, 20), 520 + k * 440, 720, tp - 0.9 + 0.3 * k, anim="up", out=False)
    S.add(rich([B("≠ 3 belles photos", 60, RED)]), CX, 920, tp + 0.2, anim="up")

# ---- Partie 8 : rentabilité
@scene("Ne pas calculer la rentabilité", ob=7)
def s48(S): obstacle_card(S, 7, "La rentabilité", "calculée avant.", "CALCULE", sub="commander sans connaître sa marge réelle", sub_t=S.w("Le dernier obstacle"))

@scene("Certaines personnes choisissent", ob=7)
def s49(S):
    S.add(vid("D8", 820, 460, "frame", w=820), 560, CY, S.t0, anim="fade")
    tb = S.w("prêts à payer")
    def arrow(tl):
        t = S.t0 + tl; im = Image.new("RGBA", (620, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        pts = [(20, 380), (180, 300), (300, 240), (440, 120), (580, 40)]
        if t >= tb: pts = pts[:4] + [(560, 330)]
        p = clamp(tl / 1.2); n = max(2, int(2 + p * (len(pts) - 2)))
        d.line(pts[:n], fill=rgba(MINT if t < tb else RED), width=14, joint="curve")
        return im
    S.add(arrow, 1400, CY - 60, S.w("tendance"), anim="fade", sfx="S2", gain=-6)
    S.add(rich([B("tendance ", 70), I("≠ rentable.", 80, RED)]), 1400, CY + 230, tb, anim="up", sfx="S14", gain=-6)

@scene("pose-toi quatre questions", ob=7)
def s50(S):
    qs = [("Coût réel par unité ?", "coûte réellement"), ("Prix de vente ?", "à quel prix"), ("Pub + livraison ?", "la publicité et la livraison"), ("Et les invendus ?", "partie du stock")]
    for k, (lab, wd) in enumerate(qs):
        c = card(400, 400); c.alpha_composite(rich([(f"0{k + 1}", "serif_i", 90, MINT)]), (34, 30))
        t = stack([rich([(l, "bold", 40, WHITE)]) for l in lab.replace(" ?", " ?").split(" ", 1)], 4, "left")
        c.alpha_composite(t, (36, 200))
        S.add(shadowed(c), 330 + k * 420, CY, S.w(wd), anim="up", sfx="S10", gain=-6)

@scene("Exemple le produit coûte trois", bg="grid", ob=7)
def s51(S):
    t3, t2, t1_, t6, t8, tr = S.w("trois dollars"), S.w("deux dollars"), S.w("un dollar"), S.w("six dollars"), S.w("huit dollars"), S.w("il ne te reste")
    S.add(vid("D2", 0, 0, "tile", size=200), 1720, 220, S.t0, anim="pop")
    for x, txt, t, sx in [(300, "3 $", t3, "S17"), (680, "+ 2 $", t2, "S17"), (1080, "+ 1 $", t1_, "S17")]:
        S.add(big_num(txt, 160), x, 400, t, anim="pop", sfx=sx, gain=-6)
    S.add(rich([("produit", "mono", 24, (220, 240, 230))]), 300, 520, t3, anim="fade")
    S.add(rich([("frais", "mono", 24, (220, 240, 230))]), 700, 520, t2, anim="fade")
    S.add(rich([("pub / vente", "mono", 24, (220, 240, 230))]), 1100, 520, t1_, anim="fade")
    S.add(big_num("= 6 $", 180, MINT), 1500, 400, t6, anim="stamp", sfx="S12", gain=-3)
    S.add(label_card("Vendu", [("8 $", "serif_i", 120, WHITE)], w=380), 560, 760, t8, anim="up")
    S.add(rich([B("8 − 6 = ", 100), I("2 $", 120)]), 1220, 760, tr, anim="up", sfx="S16", gain=-7)
    S.add(pill("avant retours et défauts", (20, 30, 26, 255), WHITE, 34), 1220, 900, S.w("avant même"), anim="up")

@scene("Un produit peut donc être populaire", bg="cream", ob=7)
def s52(S):
    S.add(title("", [[B("populaire ", 100, INK), I("≠ rentable.", 110, RED)]]), CX, 270, S.t0, anim="up")
    q1 = pill("Ce produit peut-il se vendre ?", (255, 255, 255, 255), GREY, 48, pad=(36, 22))
    q2 = pill("Puis-je le vendre avec une marge suffisante ?", (24, 30, 27, 255), WHITE, 48, pad=(36, 22), icon=check_box(46))
    ts = S.w("est-ce que ce produit"); tm = S.w("Est-ce que je peux")
    S.add(q1, CX, 520, ts, anim="up")
    S.add(strike(760, GREY, 6), CX, 524, tm, anim="none")
    S.add(q2, CX, 680, tm, anim="up", sfx="S13", gain=-6)

# ---- Partie 9 : conclusion
@scene("Commander en Chine peut offrir", ob=7)
def s53(S):
    tr = S.w("trois règles")
    S.add(vid("D7", 560, 560, "tile", size=560), 520, CY, S.t0, anim="fade")
    S.add(title("de belles opportunités…", [[B("mais de la ", 90), I("méthode.", 100)]]), 1340, CY - 120, S.t0 + 0.3, t1=tr, anim="up")
    S.add(pill("réduire les erreurs évitables", (255, 255, 255, 240), INK, 40), 1340, CY + 80, S.w("réduire"), t1=tr, anim="up")
    S.add(rich([B("les ", 110), I("3 règles.", 120)]), 1340, CY, tr, anim="pop", sfx="S1", gain=-5)

def rule(S, n, verb, rest, code, chips=()):
    S.add(rich([(str(n), "serif_i", 420, MINT)]), 400, CY - 20, S.t0, anim="stamp", dur=0.3, sfx="S13", gain=-5)
    S.add(rich([B(verb, 120)]), 720, CY - 120, S.t0 + 0.15, anim="left", anchor="l")
    S.add(rich([I(rest, 76, WHITE)]), 724, CY + 10, S.t0 + 0.3, anim="left", anchor="l")
    if code: S.add(vid(code, 0, 0, "tile", size=220), 1640, CY - 160, S.t0 + 0.3, anim="pop")
    for k, (lab, t) in enumerate(chips):
        S.add(pill(lab, (255, 255, 255, 235), INK, 32), 724 + (k % 4) * 270, CY + 150 + (k // 4) * 80, t, anim="up", anchor="l")

@scene("Premièrement teste toujours")
def s54(S): rule(S, 1, "Teste", "avant de commander gros.", "D4", [("échantillon", S.w("Un échantillon")), ("petite commande", S.w("petite commande"))])

@scene("Deuxièmement calcule")
def s55(S): rule(S, 2, "Calcule", "le coût réel.", "D2", [("prix affiché = une partie", S.w("Le prix affiché"))])

@scene("Troisièmement confirme")
def s56(S):
    ch = [(w, S.w(w)) for w in ["quantité", "qualité", "dimensions", "couleur", "emballage", "délai", "livraison"]]
    rule(S, 3, "Confirme", "tout par écrit.", None, ch)
    S.add(vid("D1", 0, 0, "tile", size=220, crop=(0.3, 0.12, 0.7, 0.88)), 1640, CY - 160, S.t0 + 0.3, anim="pop")

@scene("Si tu veux continuer à apprendre", chrome=False)
def s57(S):
    tj = S.w("rejoins ma chaîne")
    S.add(title("pour apprendre à commander en Chine", [[B("rejoins ", 120), I("ma chaîne.", 130)]]), CX, 330, S.t0, anim="up")
    btn = pill("S'abonner", (47, 208, 138, 255), INK, 52, fn="xbold", pad=(56, 26))
    S.add(btn, CX, 580, S.t0 + 0.6, anim="pop")
    S.add(pill("Abonné ✓", (24, 30, 27, 255), WHITE, 52, fn="xbold", pad=(56, 26)), CX, 580, tj + 0.75, anim="none")
    S.cursor([(S.t0 + 0.6, 1500, 900), (tj + 0.4, 990, 590), (tj + 1.3, 990, 590), (tj + 2.2, 1300, 820)], [tj + 0.7])
    S.els[-1].sfx = "S20"
    S.add(pill("le lien est dans ma bio", (255, 255, 255, 240), INK, 40), CX, 740, S.w("Le lien"), anim="up", sfx="S10", gain=-6)
    S.add(rich([I("même avec un petit budget", 54, MUTED)]), CX, 860, S.w("même si tu commences"), anim="up")

@scene("Et n'oublie pas", bg="black", chrome=False, subs=False)
def s58(S):
    S.add(hook("en importation,", MUTED, 54), CX, 300, S.w("en importation"), anim="fade")
    S.add(rich([B("ce n'est pas celui qui ", 84), I("commande le plus", 92, WHITE)]), CX, 450, S.w("ce n'est pas celui"), anim="up")
    S.add(rich([B("qui réussit,", 84)]), CX, 560, S.w("qui réussit"), anim="up")
    S.add(rich([B("c'est celui qui ", 96), I("vérifie le mieux.", 110)]), CX, 720, S.w("c'est celui qui"), anim="up")

# ------------------------------------------------------------------ calcul des temps des scènes
cur = 0.0
for i, s in enumerate(SC):
    s.t0 = 0.0 if i == 0 else find(s.phrase, cur - 0.5)
    cur = s.t0 + 0.1
for i, s in enumerate(SC):
    s.t1 = SC[i + 1].t0 if i + 1 < len(SC) else TOTAL
for s in SC: s.build(s)
OB_TIMES = [(s.t0, s.ob) for s in SC if s.ob]

# ------------------------------------------------------------------ habillage permanent
@lru_cache(None)
def tracker_img(cur, done, light=False):
    sz, gap = 40, 8; im = Image.new("RGBA", (7 * sz + 6 * gap + 8, sz + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(7):
        x = 4 + k * (sz + gap); n = k + 1
        if n < cur or (done and n <= cur):
            d.rounded_rectangle((x, 4, x + sz, 4 + sz), 9, fill=rgba(MINT))
            d.line([(x + 11, 24), (x + 18, 31), (x + 30, 15)], fill=WHITE, width=4)
        elif n == cur:
            d.rounded_rectangle((x, 4, x + sz, 4 + sz), 9, fill=(24, 30, 27, 255) if light else (255, 255, 255, 255))
            t = rich([(str(n), "bold", 24, WHITE if light else (24, 30, 27))]); im.alpha_composite(t, (x + (sz - t.width) // 2 + 1, 4 + (sz - t.height) // 2))
        else:
            fg = (24, 30, 27, 150) if light else (255, 255, 255, 150)
            d.rounded_rectangle((x, 4, x + sz, 4 + sz), 9, fill=(24, 30, 27, 25) if light else (255, 255, 255, 40), outline=(24, 30, 27, 90) if light else (255, 255, 255, 90), width=2)
            t = rich([(str(n), "bold", 22, fg)]); im.alpha_composite(t, (x + (sz - t.width) // 2 + 1, 4 + (sz - t.height) // 2))
    return im

@lru_cache(None)
def step_pill(n):
    sq = rounded(40, 40, rgba(MINT), 9); t = rich([(str(n), "bold", 24, WHITE)]); sq.alpha_composite(t, ((40 - t.width) // 2 + 1, (40 - t.height) // 2))
    return pill(f"Obstacle {n} · {OBST[n - 1]}", (255, 255, 255, 240), INK, 26, icon=sq, pad=(10, 8), r=14)

# ------------------------------------------------------------------ sous-titres
KEY = set(norm("fournisseur fournisseurs échantillon qualité prix capital frais délai délais marge coût réel arnaques commande commandes "
               "Chine dollars vidéo photo photos test teste confiance rentabilité rentable budget erreur perte logo maquette inspection "
               "douane transport calendrier sécurité paiement chaîne bio vérifie stock communication traduction critères écrit "
               "calcule confirme règles méthode obstacle problème défi"))
def build_subs():
    chunks, cur = [], []
    for w in WORDS:
        txt = w["text"].strip()
        if not txt: continue
        if cur and not (txt.startswith("'") or txt.startswith("-")):
            gap = w["start"] - cur[-1]["end"]; prev = cur[-1]["text"].strip()
            n_chars = sum(len(x["text"]) for x in cur)
            if len(cur) >= 5 or n_chars > 30 or gap > 0.35 or (prev[-1:] in ".?!,:;" and len(cur) >= 2) or prev[-1:] in ".?!":
                chunks.append(cur); cur = []
        cur.append(w)
    if cur: chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        a = c[0]["start"]; b = min(c[-1]["end"] + 0.5, chunks[i + 1][0]["start"] if i + 1 < len(chunks) else c[-1]["end"] + 0.5)
        txt = ""
        for w in c:
            t = w["text"].strip()
            txt += t if (t.startswith("'") or t.startswith("-")) else (" " + t)
        txt = txt.strip().rstrip(",")
        out.append((a, b, txt))
    return out
SUBS = build_subs()

@lru_cache(None)
def sub_img(txt, pillbg):
    words = txt.split(" "); hl = None
    for k, wd in enumerate(words):
        if any(t in KEY for t in norm(wd)): hl = k; break
    runs = []
    for k, wd in enumerate(words):
        runs.append((wd + (" " if k < len(words) - 1 else ""), "bold", 38, MINT if k == hl else WHITE))
    t = rich(runs)
    if pillbg:
        c = rounded(t.width + 40, t.height + 16, (38, 44, 41, 235), 14); c.alpha_composite(t, (20, 8)); return c
    sh = Image.new("RGBA", (t.width + 20, t.height + 20), (0, 0, 0, 0))
    blk = Image.new("RGBA", t.size, (0, 0, 0, 255)); blk.putalpha(t.getchannel("A").point(lambda v: v * 0.6))
    sh.alpha_composite(blk, (10, 13)); sh = sh.filter(ImageFilter.GaussianBlur(5)); sh.alpha_composite(t, (10, 10))
    return sh

# ------------------------------------------------------------------ rendu d'une image
def scene_at(t):
    for s in SC:
        if s.t0 <= t < s.t1: return s
    return SC[-1]

def glitch(frame, amt):
    a = np.array(frame); rng = np.random.default_rng(int(amt * 1000))
    sh = int(18 * amt)
    a[..., 0] = np.roll(a[..., 0], sh, axis=1); a[..., 2] = np.roll(a[..., 2], -sh, axis=1)
    for _ in range(int(8 * amt)):
        y = rng.integers(0, H - 40); h = rng.integers(8, 40); a[y:y + h] = np.roll(a[y:y + h], rng.integers(-60, 60), axis=1)
    return Image.fromarray(a)

def render_frame(t):
    s = scene_at(t)
    fr = background(s.bg).copy()
    items = sorted(s.els, key=lambda e: e.z)
    for e in items: draw_el(fr, e, t)
    for c in s.cursors: draw_cursor(fr, c, t)
    if s.chrome:
        ob = [o for tt, o in OB_TIMES if tt <= t]
        if ob:
            n = ob[-1]; ti = tracker_img(n, False, s.bg == "cream"); paste(fr, ti, W - 60 - ti.width, 44)
            sp = step_pill(n); paste(fr, sp, 60, 42)
    if s.subs:
        for a, b, txt in SUBS:
            if a <= t < b:
                im = sub_img(txt, s.bg in ("cream", "grid")); paste(fr, im, (W - im.width) / 2, 1012 - im.height / 2); break
    out = fr.convert("RGB")
    if s.glitch and t - s.t0 < 0.22: out = glitch(out, 1 - (t - s.t0) / 0.22)
    nxt = SC.index(s) + 1
    if nxt < len(SC) and SC[nxt].n == 58 and s.t1 - t < 0.4:          # fondu au noir avant la phrase finale
        out = Image.blend(out, Image.new("RGB", (W, H), (0, 0, 0)), clamp(1 - (s.t1 - t) / 0.4))
    if s.n == 58 and t - s.t0 < 0.3:
        out = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), out, clamp((t - s.t0) / 0.3))
    if t > VOICE_DUR + 0.6:
        out = Image.blend(out, Image.new("RGB", (W, H), (0, 0, 0)), clamp((t - VOICE_DUR - 0.6) / 0.6))
    return out

# ------------------------------------------------------------------ audio
def load_audio(path, sr=48000):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"])
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

SFX_FILES = {f.split("_")[0]: os.path.join("audio/sfx", f) for f in os.listdir("audio/sfx") if f.endswith(".mp3")}
def sfx_events():
    ev = []
    for s in SC:
        for e in s.els:
            if e.sfx: ev.append((e.t0, e.sfx, e.gain))
    ev.sort(); kept = []; last = -9
    for t, code, g in ev:
        if t - last < 0.8: continue                       # jamais plus d'un effet par seconde environ
        kept.append((t, code, g)); last = t
    return kept

def build_audio(out_wav):
    sr = 48000; n = int(TOTAL * sr) + sr
    voice = load_audio(VOICE)
    mix = np.zeros((n, 2), np.float32); mix[:len(voice)] += voice
    # effets : crête ramenée à -17 dBFS puis gain propre à l'effet
    cache = {}
    for t, code, g in sfx_events():
        if code not in cache:
            a = load_audio(SFX_FILES[code]); a = a[: int(sr * (2.0 if code in ("S19", "S8") else 3.0))]
            fl = int(0.15 * sr)
            if len(a) > fl: a[-fl:] *= np.linspace(1, 0, fl)[:, None]
            cache[code] = a / (np.abs(a).max() + 1e-9) * 10 ** (-17 / 20)
        a = cache[code] * 10 ** (g / 20); i = int(t * sr); j = min(n, i + len(a)); mix[i:j] += a[: j - i]
    # musique : 4 pistes Mixkit enchaînées en fondu, -25 dB sous la voix, coupée 1 s avant la phrase finale
    if not os.path.exists("cache/musique.wav"):
        tr = ["audio/music/deep_urban.mp3", "audio/music/hazy_after_hours.mp3", "audio/music/deep_techno_ambience.mp3", "audio/music/digital_clouds.mp3"]
        fc = "[0][1]acrossfade=d=4[a];[a][2]acrossfade=d=4[b];[b][3]acrossfade=d=4,loudnorm=I=-16:TP=-2[m]"
        cmd = ["ffmpeg", "-v", "error", "-y"]
        for p in tr: cmd += ["-i", p]
        subprocess.check_call(cmd + ["-filter_complex", fc, "-map", "[m]", "-ar", "48000", "-ac", "2", "cache/musique.wav"])
    mus = load_audio("cache/musique.wav")
    t_cut = SC[-1].t0 - 1.0
    m = np.zeros((n, 2), np.float32); L = min(n, len(mus)); m[:L] = mus[:L]
    env = np.ones(n, np.float32) * 10 ** (-25 / 20)
    i0 = int(t_cut * sr); env[i0:] = 0; env[i0 - sr:i0] *= np.linspace(1, 0, sr)
    env[: int(1.5 * sr)] *= np.linspace(0, 1, int(1.5 * sr))
    mix += m * env[:, None]
    mix = mix[: int(TOTAL * sr)]
    peak = np.abs(mix).max()
    if peak > 0.97: mix *= 0.97 / peak
    mix.astype(np.float32).tofile("cache/mix.f32")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "cache/mix.f32", out_wav])

# ------------------------------------------------------------------ rendu vidéo (4 processus)
def render_range(i0, i1, path):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for i in range(i0, i1):
        p.stdin.write(render_frame(i / FPS).tobytes())
        if (i - i0) % 600 == 0: print(f"  {path}: {i - i0}/{i1 - i0}", flush=True)
    p.stdin.close(); p.wait()

def write_plan():
    rows = ["| # | Début | Fin | Fond | Phrase d'ancrage |", "|---|---|---|---|---|"]
    for s in SC:
        rows.append(f"| {s.n} | {int(s.t0 // 60)}:{s.t0 % 60:05.2f} | {int(s.t1 // 60)}:{s.t1 % 60:05.2f} | {s.bg} | « {s.phrase} » |")
    open("cache/scenes.md", "w").write("\n".join(rows) + "\n")
    json.dump([{"t": round(t, 2), "son": c, "gain_db": g} for t, c, g in sfx_events()], open("cache/sons.json", "w"), indent=0)

if __name__ == "__main__":
    os.makedirs("cache/apercus", exist_ok=True); os.makedirs("export", exist_ok=True)
    write_plan()
    if "--frames" in sys.argv:
        for a in sys.argv[sys.argv.index("--frames") + 1:]:
            t = float(a); render_frame(t).save(f"cache/apercus/f_{t:07.2f}.png"); print("ok", t, scene_at(t).n)
        sys.exit()
    if "--audio" in sys.argv:
        build_audio("cache/mix.wav"); sys.exit()
    N = int(TOTAL * FPS); K = 4; bounds = [N * k // K for k in range(K + 1)]
    procs = [Process(target=render_range, args=(bounds[k], bounds[k + 1], f"cache/part{k}.mp4")) for k in range(K)]
    for p in procs: p.start()
    build_audio("cache/mix.wav")
    for p in procs: p.join()
    open("cache/parts.txt", "w").write("".join(f"file 'part{k}.mp4'\n" for k in range(K)))
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "cache/parts.txt", "-i", "cache/mix.wav",
                           "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
                           "export/obstacles_chine_16x9.mp4"])
    print("export/obstacles_chine_16x9.mp4")
