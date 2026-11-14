#!/usr/bin/env python3
"""TikTok 9:16 « Quelle plateforme chinoise choisir ? » — modèle « Les 7 obstacles » (modele_video/).

    python3 transcrire.py                  # audio/transcription.json (mots horodatés)
    python3 build_tiktok.py --frames 3 20  # aperçus PNG (cache/apercus)
    python3 build_tiktok.py                # -> export/plateformes_chine_tiktok_9x16.mp4

Voix : audio/voix_off_tik_tok.wav, utilisée entière, sans coupe. Images et animations : dossier Drive
« Dossier plateformes » uniquement. Sons : kit Mixkit S1-S20 (audio/sfx), musique Mixkit (audio/music).
"""
import os, sys, json, subprocess
from multiprocessing import Process
import numpy as np
import engine as E
E.W, E.H = 1080, 1920
from engine import *
from PIL import Image, ImageDraw, ImageFilter

os.chdir(HERE)
SR = 48000
VOICE = "audio/voix_off_tik_tok.wav"
VOICE_DUR = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VOICE]))
TOTAL = VOICE_DUR + 1.0
CX = 540

# ------------------------------------------------------------------ mots + corrections des sous-titres
WORDS = json.load(open("audio/transcription.json"))["words"]
FIX = [
    ("le commander en chine", "Tu veux commander en Chine"), ("plateforme me choisir", "plateforme choisir ?"),
    ("alibaba 1688", "Alibaba, 1688,"), ("propre bruit", "propre produit."), ("madeinchina com", "Made-in-China.com"),
    ("global source", "Global Sources."), ("trait d assurance", "Trade Assurance."), ("des ashgate", "DHgate."),
    ("16 88", "1688,"), ("tamal", "Tmall"), ("panduoduo", "Pinduoduo."), ("yuan", "yuans,"),
    ("yougo lie au grand marche de gros de yougo", "Yiwugo, lié au grand marché de gros de Yiwu."),
    ("l evaluation de ton produit", "Ton produit"), ("un exemple concretement", "Un exemple concret."),
]
def apply_fix(words, old, new):
    tgt = norm(old); out = []; i = 0
    while i < len(words):
        acc = []; j = i
        if not norm(words[i]["text"]):
            out.append(words[i]); i += 1; continue
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
TOK = [(t, i) for i, w in enumerate(WORDS) for t in norm(w["text"])]
def find(phrase, after=0.0, which="start"):
    tgt = norm(phrase)
    for k in range(len(TOK) - len(tgt) + 1):
        if WORDS[TOK[k][1]]["start"] < after - 0.05: continue
        if [TOK[k + m][0] for m in range(len(tgt))] == tgt:
            w = WORDS[TOK[k + len(tgt) - 1][1]] if which == "end" else WORDS[TOK[k][1]]
            return w[which]
    raise KeyError(f"introuvable après {after:.1f}s : {phrase}")

# ------------------------------------------------------------------ constructeurs (style du modèle)
def hook(txt, col=MUTED, size=54): return rich([(txt, "serif_i", size, col)])
def B(t, s=110, c=WHITE): return (t, "xbold", s, c)
def I(t, s=110, c=MINT): return (t, "serif_i", s, c)
def img_frame(name, w, r=30): return shadowed(framed(Image.open(f"drive/{name}").convert("RGBA"), w, r))

@lru_cache(None)
def dv(name, w, t0=0.0, t1=None):
    p = f"drive/{name}"
    sw, sh = map(int, subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", p]).decode().split(","))
    sc = w / sw; ww, hh = int(sw * sc) // 2 * 2, int(sh * sc) // 2 * 2
    cmd = ["ffmpeg", "-v", "error", "-ss", str(t0), "-i", p] + (["-t", str(t1 - t0)] if t1 else []) + ["-vf", f"fps=30,scale={ww}:{hh}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "rgba", "-"]
    raw = subprocess.check_output(cmd); n = len(raw) // (ww * hh * 4)
    return [Image.fromarray(a.copy()) for a in np.frombuffer(raw, np.uint8)[: n * ww * hh * 4].reshape(n, hh, ww, 4)]

def vid(name, w, t0=0.0, t1=None, tile=False, size=None, loop=True):
    """Animation du Drive : posée dans un cadre arrondi (ou une carte blanche carrée)."""
    frames = dv(name, (size - 60) if tile else w, t0, t1); cache = {}
    def f(tl):
        i = int(tl * 30); i = i % len(frames) if loop else min(i, len(frames) - 1)
        if i not in cache:
            fr = frames[i]
            if tile:
                c = rounded(size, size, rgba(WHITE), 44, outline=(225, 225, 220, 255), width=2)
                c.alpha_composite(fr, ((size - fr.width) // 2, (size - fr.height) // 2)); cache[i] = shadowed(c, 24, (0, 10), 90)
            else:
                cache[i] = shadowed(framed(fr, w), 28, (0, 14), 110)
        return cache[i]
    return f

LOGOS = {"alibaba": ("img_54d0df78.jpg", "Alibaba.com"), "1688": ("img_1794622197816.jpg", "1688"), "aliexpress": ("img_1794622191621.jpg", "AliExpress"),
         "taobao": ("img_1794622200636.jpg", "Taobao"), "madeinchina": ("img_d58ebf05.jpg", "Made-in-China"), "globalsources": ("img_1794622186868.jpg", "Global Sources"),
         "dhgate": ("img_1794622193747.jpg", "DHgate"), "tmall": ("img_1794622203420.jpg", "Tmall"), "pinduoduo": ("img_1794622206459.jpg", "Pinduoduo"),
         "yiwugo": ("img_1794622212474.jpg", "Yiwugo")}
@lru_cache(None)
def logo_card(key, w=420, h=250, label=True):
    fn, name = LOGOS[key]
    im = Image.open(f"drive/{fn}").convert("RGBA")
    # recadrage : on retire les bandes unies autour du logo
    a = np.array(im.convert("RGB")).astype(int); bg = a[2, 2]
    mask = np.abs(a - bg).sum(2) > 40
    ys, xs = np.where(mask)
    if len(xs): im = im.crop((max(0, xs.min() - 10), max(0, ys.min() - 10), min(im.width, xs.max() + 10), min(im.height, ys.max() + 10)))
    fill = tuple(int(v) for v in bg) + (255,)
    c = rounded(w, h, fill, 36, outline=(225, 225, 220, 255), width=2)
    im.thumbnail((w - 70, h - 60), Image.LANCZOS)
    c.alpha_composite(im, ((w - im.width) // 2, (h - im.height) // 2))
    c = shadowed(c, 24, (0, 10), 100)
    if not label: return c
    t = rich([(name, "bold", 40, WHITE)])
    out = Image.new("RGBA", (max(c.width, t.width), c.height + t.height - 20), (0, 0, 0, 0))
    out.alpha_composite(c, ((out.width - c.width) // 2, 0)); out.alpha_composite(t, ((out.width - t.width) // 2, c.height - 30))
    return out

def strike(w, col=RED, thick=10):
    def f(tl):
        p = ease_out(clamp(tl / 0.35)); im = Image.new("RGBA", (w, thick + 4), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle((0, 2, max(thick, int(w * p)), thick + 2), thick // 2, fill=rgba(col)); return im
    return f

def icon_warn(s=170, col=RED):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(s / 2, 6), (s - 6, s - 10), (6, s - 10)], fill=rgba(col))
    t = rich([("!", "xbold", int(s * .55), WHITE)]); im.alpha_composite(t, ((s - t.width) // 2, int(s * .25))); return im

def big_num(t, s=200, c=WHITE): return rich([(t, "serif_i", s, c)])

# ------------------------------------------------------------------ scènes
class Scene:
    def __init__(s, phrase, bg, part, fn, subs=True, glitch=False):
        s.phrase, s.bg, s.part, s.build, s.subs, s.glitch = phrase, bg, part, fn, subs, glitch
        s.els, s.cursors = [], []
    def w(s, phrase, which="start"): return find(phrase, s.t0, which)
    def add(s, *a, **k):
        k.setdefault("t1", s.t1); e = El(*a, **k); s.els.append(e); return e
    def cursor(s, keys, clicks): s.cursors.append(Cursor(keys, clicks, s.t1))

SC = []
def scene(phrase, bg="dark", part=None, subs=True, glitch=False):
    def deco(fn): SC.append(Scene(phrase, bg, part, fn, subs, glitch)); return fn
    return deco

CAS = [("Acheter en gros", "ou faire fabriquer.", "B2B"), ("Tester un produit", "petit budget.", "TEST"),
       ("Les prix", "les plus bas.", "AGENT"), ("Accessoires,", "maison, cadeaux.", "YIWU")]
def cas_headline(S, k, t_end):
    l1, l2, st = CAS[k - 1]
    S.add(rich([(f"0{k}", "serif", 380, (255, 255, 255, 55))]), CX, 620, S.t0, t1=t_end, anim="fade", dur=0.3)
    S.add(hook(f"cas n°{k}", MUTED, 54), CX, 470, S.t0, t1=t_end, anim="fade")
    S.add(rich([B(l1, 100)]), CX, 840, S.t0 + 0.05, t1=t_end, anim="up", sfx="S1", gain=-4)
    S.add(rich([I(l2, 104)]), CX, 970, S.t0 + 0.15, t1=t_end, anim="up")
    S.add(stamp(st, MINT, 64), CX, 1160, S.t0 + 0.5, t1=t_end, anim="stamp", dur=0.3)
def header(S, k, t):
    l1, l2, _ = CAS[k - 1]
    S.add(rich([(f"0{k} · ", "serif_i", 52, MINT), (l1 + " " + l2.rstrip("."), "bold", 42, WHITE)]), CX, 340, t, anim="fade")

def logos_grid(S, keys_words, y0=640, dy=330, cols=2, sfx="S10"):
    for k, (key, wd) in enumerate(keys_words):
        x = [300, 780][k % 2] if cols == 2 else CX
        y = y0 + (k // cols) * dy
        S.add(logo_card(key), x, y, S.w(wd), anim="pop", sfx=sfx if k % 2 == 0 else None, gain=-5)

# ---- Accroche
@scene("Tu veux commander en Chine")
def s_hook(S):
    S.add(vid("motion_cuts_703.mp4", 900, 5.0, 9.8, loop=False), CX, 1000, S.t0, anim="fade")
    S.add(rich([B("commander", 110)]), CX, 470, S.t0 + 0.1, anim="up", sfx="S6", gain=-6)
    S.add(rich([B("en Chine ", 88), I("pour la RDC ?", 82)]), CX, 600, S.w("revendre"), anim="up")
    S.add(pill("quelle plateforme choisir ?", (47, 208, 138, 255), INK, 50, fn="bold", pad=(34, 18)), CX, 1325, S.w("plateforme"), anim="stamp", sfx="S10", gain=-6)

@scene("Alibaba, 1688,")
def s_noms(S):
    logos_grid(S, [("alibaba", "Alibaba"), ("1688", "1688"), ("aliexpress", "AliExpress"), ("taobao", "Taobao")], y0=560, dy=360)
    S.add(stamp("PAS LA MÊME CHOSE", RED, 58), CX, 1290, S.w("même chose"), anim="stamp", sfx="S14", gain=-5)

@scene("Et si tu te trompes", bg="black", glitch=True)
def s_perte(S):
    S.add(icon_warn(170), CX, 520, S.t0, anim="pop", sfx="S2", gain=-5)
    S.add(rich([B("mauvaise plateforme", 92)]), CX, 720, S.w("trompes"), anim="up")
    S.add(rich([I("= beaucoup", 110, RED)]), CX, 870, S.w("perdre"), anim="stamp", dur=0.3, sfx="S5", gain=-3)
    S.add(rich([I("d'argent perdu.", 110, RED)]), CX, 1000, S.w("perdre") + 0.2, anim="stamp", dur=0.3)

@scene("Reste jusqu'à la fin")
def s_promesse(S):
    S.add(vid("floating_ecommerce_mockup.mp4", 430), CX, 680, S.t0, anim="fade")
    S.add(rich([B("laquelle choisir", 96)]), CX, 1160, S.w("laquelle"), anim="up")
    S.add(rich([I("selon ton objectif.", 92)]), CX, 1280, S.w("objectif"), anim="up", sfx="S10", gain=-6)

# ---- Cas 1 : gros / fabrication
@scene("Premier cas", part=1)
def s_cas1(S):
    tl = S.w("Alibaba.com") - 0.1
    cas_headline(S, 1, tl); header(S, 1, tl)
    logos_grid(S, [("alibaba", "Alibaba.com"), ("madeinchina", "Made-in-China"), ("globalsources", "Global Sources")], y0=620, dy=360)

@scene("Ce sont des plateformes B2B", part=1)
def s_b2b(S):
    header(S, 1, S.t0)
    S.add(stamp("B2B", MINT, 100, -4), CX, 480, S.t0, anim="stamp", sfx="S12", gain=-5)
    S.add(vid("chemyo_quality_control.mp4", 700, 0.0, 3.0), CX, 850, S.w("fabricants"), anim="fade")
    for k, (lab, wd) in enumerate([("fabricants", "fabricants"), ("grossistes", "grossistes"), ("acheteurs étrangers", "acheteurs étrangers")]):
        S.add(pill(lab, (255, 255, 255, 240), INK, 40, icon=check_box(38)), CX, 1170 + k * 90, S.w(wd), anim="up", sfx="S13" if k == 0 else None, gain=-6)

@scene("Tu peux demander des devis", part=1)
def s_devis(S):
    header(S, 1, S.t0)
    items = ["Demander des devis", "Recevoir des échantillons", "Négocier la quantité minimale"]
    ts = [S.w("devis"), S.w("échantillons"), S.w("négocier")]
    for k in range(4):
        a = S.t0 if k == 0 else ts[k - 1] + 0.2
        b = ts[k] + 0.2 if k < 3 else S.t1
        S.add(checklist_card("Sur ces plateformes, tu peux", items, k, w=940, size=40), CX, 820, a, t1=b, anim="up" if k == 0 else "none", sfx=None if k == 0 else "S20", gain=-6)
    keys = [(S.t0, 900, 1400)] + sum([[(t - 0.05, 112, 761 + k * 78), (t + 0.25, 112, 761 + k * 78)] for k, t in enumerate(ts)], [])
    S.cursor(keys, [t + 0.2 for t in ts])

@scene("Mais attention un badge", part=1)
def s_badge(S):
    header(S, 1, S.t0)
    S.add(pill("Fournisseur vérifié", (47, 208, 138, 255), INK, 60, fn="bold", pad=(40, 24), icon=check_box(56, col=(24, 30, 27))), CX, 700, S.w("badge"), anim="pop", sfx="S10", gain=-6)
    S.add(rich([B("≠ ", 120, RED), I("garantie.", 120, RED)]), CX, 930, S.w("garantie"), anim="stamp", dur=0.3, sfx="S14", gain=-4)

@scene("Compare toujours", part=1)
def s_compare(S):
    header(S, 1, S.t0)
    tt = S.w("sur Alibaba")
    S.add(img_frame("img_25dc22e3.jpg", 440), CX, 750, S.t0, t1=tt, anim="fade", kb=1.05)
    for k, lab in enumerate(["Fournisseur A", "Fournisseur B", "Fournisseur C"]):
        S.add(pill(lab, (255, 255, 255, 240), INK, 38, fn="bold"), CX, 1150 + k * 88, S.w("trois") + 0.25 * k, t1=tt, anim="up", sfx="S10" if k == 0 else None, gain=-6)
    S.add(img_frame("img_78b779af.jpg", 600), CX, 760, tt, anim="fade")
    S.add(pill("Trade Assurance", (47, 208, 138, 255), INK, 54, fn="bold", pad=(36, 20), icon=check_box(50, col=(24, 30, 27))), CX, 1130, S.w("Trade"), anim="stamp", sfx="S13", gain=-5)
    S.add(rich([I("commande officielle uniquement", 56, WHITE)]), CX, 1250, S.w("commande officielle"), anim="up")

# ---- Cas 2 : tester
@scene("Deuxième cas", part=2)
def s_cas2(S):
    tl = S.w("AliExpress") - 0.1
    cas_headline(S, 2, tl); header(S, 2, tl)
    logos_grid(S, [("aliexpress", "AliExpress"), ("dhgate", "DHgate")], y0=760, dy=420, cols=1)

@scene("Tu peux acheter à l'unité", part=2)
def s_unite(S):
    header(S, 2, S.t0)
    S.add(vid("ecommerce_ui_animation.mp4", 820, 0.0, 12.0), CX, 760, S.t0, anim="fade")
    for k, (lab, wd) in enumerate([("à l'unité", "unité"), ("un échantillon", "échantillon"), ("le produit plaît ?", "plaît")]):
        S.add(pill(lab, (255, 255, 255, 240), INK, 44, icon=check_box(40)), CX, 1160 + k * 100, S.w(wd), anim="up", sfx="S13" if k == 0 else None, gain=-6)

@scene("Mais le prix affiché", bg="grid", part=2)
def s_prix(S):
    header(S, 2, S.t0)
    S.add(label_card("Prix affiché", [("≠ prix final", "serif_i", 110, WHITE)], w=900), CX, 600, S.t0, anim="pop", sfx="S16", gain=-7)
    for k, (lab, wd) in enumerate([("+ livraison", "la livraison"), ("+ douane", "douane"), ("+ taxes", "taxes"), ("+ livraison locale", "livraison locale")]):
        S.add(pill(lab, (224, 90, 79, 255), WHITE, 48, fn="bold", pad=(32, 16)), 110, 860 + k * 110, S.w(wd), anim="left", anchor="l", sfx="S11" if k % 2 == 0 else None, gain=-7)
    S.add(vid("Delivery_3D_illustration.mp4", 0, tile=True, size=280), 830, 1100, S.w("jusqu'à ta ville"), anim="pop")

# ---- Cas 3 : prix les plus bas
@scene("Troisième cas", part=3)
def s_cas3(S):
    tl = S.w("1688") - 0.1
    cas_headline(S, 3, tl); header(S, 3, tl)
    logos_grid(S, [("1688", "1688"), ("taobao", "Taobao"), ("tmall", "Tmall"), ("pinduoduo", "Pinduoduo")], y0=600, dy=360)

@scene("Les prix sont très intéressants", part=3)
def s_chinois(S):
    header(S, 3, S.t0)
    S.add(pill("prix très intéressants", (47, 208, 138, 255), INK, 50, fn="bold", pad=(34, 18), icon=check_box(46, col=(24, 30, 27))), CX, 500, S.t0, anim="pop", sfx="S13", gain=-6)
    items = ["Faits pour les Chinois", "Interface en chinois", "Paiement en yuans", "Pas de livraison vers l'Afrique"]
    ts = [S.w("faits pour"), S.w("interface"), S.w("paiement"), S.w("livraison vers")]
    for k in range(5):
        a = S.w("mais ces sites") if k == 0 else ts[k - 1]
        b = ts[k] if k < 4 else S.t1
        S.add(checklist_card("Attention", items, k, w=940, light=False, title_col=RED, marks=["x"] * 4, size=40), CX, 900, a, t1=b,
              anim="up" if k == 0 else "none", sfx=None if k == 0 else ("S14" if k == 1 else None), gain=-8)
    S.add(vid("world_monuments.mp4", 0, 0.0, 6.0, tile=True, size=260), 860, 1260, S.w("Afrique"), anim="pop")

@scene("Il te faudra un agent", part=3)
def s_agent(S):
    header(S, 3, S.t0)
    td = S.w("Demande son nom")
    S.add(img_frame("img_ffc40de0.jpg", 560), CX, 720, S.t0, t1=td, anim="fade", kb=1.05)
    S.add(pill("agent d'achat", (255, 255, 255, 240), INK, 46), 330, 1110, S.w("agent d'achat"), t1=td, anim="up", sfx="S10", gain=-6)
    S.add(pill("transitaire", (255, 255, 255, 240), INK, 46), 770, 1110, S.w("transitaire"), t1=td, anim="up")
    S.add(stamp("PAS AUTOMATIQUEMENT FIABLE", RED, 44), CX, 1250, S.w("pas automatiquement"), t1=td, anim="stamp", sfx="S14", gain=-5)
    items = ["Son nom", "Ses références", "Un devis détaillé"]; ts = [S.w("son nom"), S.w("références"), S.w("devis détaillé")]
    for k in range(4):
        a = td if k == 0 else ts[k - 1] + 0.2
        b = ts[k] + 0.2 if k < 3 else S.t1
        S.add(checklist_card("Avant d'envoyer de l'argent", items, k, w=900, size=44), CX, 820, a, t1=b, anim="up" if k == 0 else "none", sfx=None if k == 0 else "S13", gain=-7)

# ---- Cas 4 : Yiwu
@scene("Enfin pour les petits accessoires", part=4)
def s_cas4(S):
    tl = S.w("Yiwugo") - 0.1
    cas_headline(S, 4, tl); header(S, 4, tl)
    S.add(logo_card("yiwugo", 600, 300), CX, 640, S.w("Yiwugo"), anim="pop", sfx="S10", gain=-5)
    S.add(vid("freu_mich_auf_dich.mp4", 860, 0.0, 6.0), CX, 1110, S.w("marché de gros"), anim="fade")

@scene("C'est pratique pour repérer", part=4)
def s_yiwu(S):
    header(S, 4, S.t0)
    S.add(img_frame("img_5aa9204c.jpg", 860), CX, 680, S.t0, anim="fade", kb=1.06)
    S.add(pill("repérer des produits", (255, 255, 255, 240), INK, 46, icon=check_box(42)), CX, 1010, S.w("repérer"), anim="up", sfx="S13", gain=-6)
    S.add(pill("demander des devis", (255, 255, 255, 240), INK, 46, icon=check_box(42)), CX, 1110, S.w("demander des devis"), anim="up")
    S.add(stamp("PAS FORCÉMENT UNE USINE", RED, 50), CX, 1260, S.w("pas forcément"), anim="stamp", sfx="S14", gain=-5)

# ---- Méthode en 5 points
@scene("Maintenant la méthode")
def s_methode(S):
    items = ["Produit simple, pas fragile", "Compare au moins 3 vendeurs", "Échantillon ou petite quantité", "Coût total jusqu'à ta ville", "Paiement officiel uniquement"]
    nums = []; t = S.w("en 5 points", "end")
    for n in "12345":
        t = find(n, t + 0.1); nums.append(t)
    S.add(rich([B("la méthode", 100)]), CX, 390, S.t0, anim="up", sfx="S1", gain=-5)
    S.add(rich([I("en 5 points.", 96)]), CX, 505, S.t0 + 0.2, anim="up")
    for k in range(6):
        a = S.t0 + 0.4 if k == 0 else nums[k - 1] + 0.15
        b = nums[k] + 0.15 if k < 5 else S.t1
        S.add(checklist_card("À faire avant de commander", items, k, w=960, size=40), CX, 830, a, t1=b, anim="up" if k == 0 else "none", sfx=None if k == 0 else "S13", gain=-7)
    tiles = [None, ("img", "img_25dc22e3.jpg"), ("vid", "Delivery_3D_illustration.mp4"), ("img", "img_a9ebc21a.jpg"), ("img", "img_78b779af.jpg")]
    for k, tl in enumerate(tiles):
        if not tl: continue
        b = nums[k + 1] if k < 4 else S.t1
        if tl[0] == "img":
            S.add(img_frame(tl[1], 300, 24), CX, 1250, nums[k] + 0.2, t1=b, anim="pop")
        else:
            S.add(vid(tl[1], 0, tile=True, size=280), CX, 1250, nums[k] + 0.2, t1=b, anim="pop")
    S.add(pill("pas réglementé", (255, 255, 255, 240), INK, 44, fn="bold"), CX, 1250, S.w("réglementé"), t1=nums[1] + 0.15, anim="up")
    for k, lab in enumerate(["transport", "douane", "taxes", "livraison"]):
        pass

# ---- Exemple chiffré
@scene("Un exemple concret", bg="grid")
def s_exemple(S):
    S.add(hook("un exemple concret :", (220, 240, 230), 56), CX, 380, S.t0, anim="fade")
    rows = [("produit", "3 $", S.w("3 dollars")), ("transport + frais", "+ 2 $", S.w("2 dollars")), ("pub + livraison locale", "+ 1 $", S.w("1 dollar"))]
    for k, (lab, val, t) in enumerate(rows):
        y = 520 + k * 135
        S.add(rich([(lab, "mono", 34, (220, 240, 230))]), 140, y, t, anim="fade", anchor="l")
        S.add(big_num(val, 130), 900, y, t, anim="pop", anchor="r", sfx="S17", gain=-6)
    S.add(strike(820, WHITE, 6), CX, 890, S.w("vrai coût"), anim="none")
    S.add(rich([B("vrai coût = ", 80), I("6 $", 130)]), CX, 980, S.w("6 dollars"), anim="stamp", sfx="S12", gain=-4)
    S.add(label_card("Revendu 8 $ → marge", [("2 $ seulement", "serif_i", 96, WHITE)], w=820), CX, 1200, S.w("8 dollars"), anim="up", sfx="S16", gain=-7)

@scene("Retiens ceci", bg="cream")
def s_retiens(S):
    tc = S.w("C'est celle")
    S.add(hook("retiens ceci :", GREY, 56), CX, 430, S.t0, anim="fade")
    S.add(rich([B("la meilleure", 100, INK)]), CX, 560, S.w("la meilleure"), anim="up")
    S.add(rich([I("plateforme", 110, (40, 130, 90))]), CX, 680, S.w("plateforme"), anim="up")
    S.add(pill("≠ le prix le plus bas", (255, 235, 232, 255), RED, 54, fn="bold", pad=(36, 20)), CX, 850, S.w("le prix"), anim="stamp", sfx="S14", gain=-6)
    for k, (lab, wd) in enumerate([("ton objectif", "objectif"), ("ton budget", "budget"), ("la logistique jusqu'à chez toi", "logistique")]):
        S.add(pill(lab, (24, 30, 27, 255), WHITE, 48, icon=check_box(44), pad=(30, 18)), CX, 1010 + k * 115, S.w(wd), anim="up", sfx="S13" if k == 0 else None, gain=-6)

@scene("Enregistre cette vidéo")
def s_cta(S):
    te, ta = S.w("Enregistre"), S.w("abonne")
    S.add(pill("Enregistre la vidéo", (255, 255, 255, 240), INK, 54, fn="xbold", pad=(40, 22)), CX, 330, te, anim="pop", sfx="S10", gain=-6)
    S.add(vid("canal_whatsapp_achadinhos.mp4", 440, 3.0, 8.2, loop=False), CX, 790, S.t0, anim="fade")
    S.add(pill("S'abonner", (47, 208, 138, 255), INK, 64, fn="xbold", pad=(66, 30)), CX, 1290, ta - 0.3, anim="pop")
    tc = ta + 0.5
    S.add(pill("Abonné ✓", (24, 30, 27, 255), WHITE, 64, fn="xbold", pad=(66, 30)), CX, 1290, tc, anim="none", sfx="S20", gain=-4)
    S.cursor([(ta - 0.3, 900, 1500), (tc - 0.15, 560, 1302), (tc + 0.6, 560, 1302), (tc + 1.2, 860, 1360)], [tc])

# ------------------------------------------------------------------ temps des scènes
cur = 0.0
for i, s in enumerate(SC):
    s.t0 = 0.0 if i == 0 else find(s.phrase, cur - 0.3) - 0.12
    cur = s.t0 + 0.3
for i, s in enumerate(SC): s.t1 = SC[i + 1].t0 if i + 1 < len(SC) else TOTAL
for s in SC: s.build(s)

# ------------------------------------------------------------------ suivi (4 cas) + sous-titres
@lru_cache(None)
def tracker_img(cur, n=4):
    sz, gap = 60, 14; im = Image.new("RGBA", (n * sz + (n - 1) * gap + 8, sz + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(n):
        x = 4 + k * (sz + gap); m = k + 1
        if m < cur:
            d.rounded_rectangle((x, 4, x + sz, 4 + sz), 12, fill=rgba(MINT)); d.line([(x + 16, 35), (x + 27, 46), (x + 45, 22)], fill=WHITE, width=5)
        elif m == cur:
            d.rounded_rectangle((x, 4, x + sz, 4 + sz), 12, fill=(255, 255, 255, 255))
            t = rich([(str(m), "bold", 34, (24, 30, 27))]); im.alpha_composite(t, (x + (sz - t.width) // 2 + 1, 4 + (sz - t.height) // 2))
        else:
            d.rounded_rectangle((x, 4, x + sz, 4 + sz), 12, fill=(255, 255, 255, 40), outline=(255, 255, 255, 90), width=2)
            t = rich([(str(m), "bold", 32, (255, 255, 255, 150))]); im.alpha_composite(t, (x + (sz - t.width) // 2 + 1, 4 + (sz - t.height) // 2))
    return im

KEY = set(norm("Chine RDC plateforme plateformes argent Alibaba 1688 AliExpress Taobao Made-in-China Global Sources DHgate Tmall Pinduoduo Yiwugo Yiwu "
               "B2B devis échantillon échantillons garantie fournisseurs Trade Assurance budget prix douane taxes agent transitaire usine méthode "
               "vendeurs coût dollars marge objectif logistique abonne enregistre fiable"))
def build_subs():
    chunks, cur = [], []
    for w in WORDS:
        txt = w["text"].strip()
        if not txt: continue
        if cur and not txt.startswith(("'", "-", ".")):
            gap = w["start"] - cur[-1]["end"]; prev = cur[-1]["text"].strip()
            if len(cur) >= 4 or sum(len(x["text"]) for x in cur) > 22 or gap > 0.3 or (prev[-1:] in ".?!,:;" and len(cur) >= 2) or prev[-1:] in ".?!":
                chunks.append(cur); cur = []
        cur.append(w)
    if cur: chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        a = c[0]["start"]; b = min(c[-1]["end"] + 0.4, chunks[i + 1][0]["start"] if i + 1 < len(chunks) else 1e9)
        txt = ""
        for w in c:
            t = w["text"].strip(); txt += t if t.startswith(("'", "-", ".")) else " " + t
        out.append((a, b, txt.strip().rstrip(",")))
    return out
SUBS = build_subs()

@lru_cache(None)
def sub_img(txt):
    words = txt.split(" "); hl = next((k for k, wd in enumerate(words) if any(t in KEY for t in norm(wd))), None)
    t = rich([(wd + (" " if k < len(words) - 1 else ""), "xbold", 54, MINT if k == hl else WHITE) for k, wd in enumerate(words)])
    c = rounded(t.width + 48, t.height + 22, (16, 22, 19, 225), 18); c.alpha_composite(t, (24, 11)); return c

def glitch(img, amt):
    a = np.array(img); rng = np.random.default_rng(int(amt * 1000)); sh = int(18 * amt)
    a[..., 0] = np.roll(a[..., 0], sh, axis=1); a[..., 2] = np.roll(a[..., 2], -sh, axis=1)
    for _ in range(int(8 * amt)):
        y = rng.integers(0, E.H - 40); h = rng.integers(8, 40); a[y:y + h] = np.roll(a[y:y + h], rng.integers(-60, 60), axis=1)
    return Image.fromarray(a)

def scene_at(t):
    for s in SC:
        if s.t0 <= t < s.t1: return s
    return SC[-1]

def render_frame(t):
    s = scene_at(t); fr = background(s.bg).copy()
    for e in s.els: draw_el(fr, e, t)
    for c in s.cursors: draw_cursor(fr, c, t)
    if s.part:
        ti = tracker_img(s.part); paste(fr, ti, (E.W - ti.width) / 2, 200)
    if s.subs:
        for a, b, txt in SUBS:
            if a <= t < b:
                im = sub_img(txt); paste(fr, im, (E.W - im.width) / 2, 1450 - im.height / 2); break
    out = fr.convert("RGB")
    if s.glitch and t - s.t0 < 0.22: out = glitch(out, 1 - (t - s.t0) / 0.22)
    if t > VOICE_DUR + 0.3: out = Image.blend(out, Image.new("RGB", out.size), clamp((t - VOICE_DUR - 0.3) / 0.6))
    return out

# ------------------------------------------------------------------ audio
def load_audio(path):
    return np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]), np.float32).reshape(-1, 2).copy()
SFX_FILES = {f.split("_")[0]: os.path.join("audio/sfx", f) for f in os.listdir("audio/sfx") if f.endswith(".mp3")}
def sfx_events():
    ev = sorted((e.t0, e.sfx, e.gain) for s in SC for e in s.els if e.sfx); kept = []; last = -9
    for t, c, g in ev:
        if t - last >= 0.8: kept.append((t, c, g)); last = t
    return kept

def build_audio(out):
    n = int(TOTAL * SR) + SR; mix = np.zeros((n, 2), np.float32)
    v = load_audio(VOICE); mix[:len(v)] += v
    for t, code, g in sfx_events():
        a = load_audio(SFX_FILES[code])[: int(SR * 3.0)]
        fl = int(0.15 * SR); a[-fl:] *= np.linspace(1, 0, fl)[:, None]
        a = a / (np.abs(a).max() + 1e-9) * 10 ** ((-17 + g) / 20); i = int(t * SR); j = min(n, i + len(a)); mix[i:j] += a[: j - i]
    if not os.path.exists("cache/musique.wav"):
        tr = ["audio/music/deep_urban.mp3", "audio/music/hazy_after_hours.mp3"]
        subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", tr[0], "-i", tr[1], "-filter_complex", "[0][1]acrossfade=d=4,loudnorm=I=-16:TP=-2[m]",
                               "-map", "[m]", "-ar", str(SR), "-ac", "2", "cache/musique.wav"])
    mus = load_audio("cache/musique.wav")
    m = np.zeros((n, 2), np.float32); L = min(n, len(mus)); m[:L] = mus[:L]
    env = np.ones(n, np.float32) * 10 ** (-24 / 20)
    i0 = int((VOICE_DUR - 0.2) * SR); env[i0:] *= np.linspace(1, 0, n - i0) ** 2
    env[: int(0.8 * SR)] *= np.linspace(0, 1, int(0.8 * SR))
    mix += m * env[:, None]; mix = mix[: int(TOTAL * SR)]
    mix *= 0.97 / max(0.97, np.abs(mix).max())
    mix.astype(np.float32).tofile("cache/mix.f32")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "cache/mix.f32",
                           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), out])

def render_range(i0, i1, path):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{E.W}x{E.H}", "-r", "30", "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for i in range(i0, i1): p.stdin.write(render_frame(i / 30).tobytes())
    p.stdin.close(); p.wait()

if __name__ == "__main__":
    os.makedirs("cache/apercus", exist_ok=True); os.makedirs("export", exist_ok=True)
    print(f"durée : {TOTAL:.1f} s")
    for s in SC: print(f"  {s.t0:6.2f} -> {s.t1:6.2f}  {s.phrase}")
    if "--frames" in sys.argv:
        for a in sys.argv[sys.argv.index("--frames") + 1:]:
            render_frame(float(a)).save(f"cache/apercus/f_{float(a):06.2f}.png")
        sys.exit()
    N = int(TOTAL * 30); K = 4; bd = [N * k // K for k in range(K + 1)]
    ps = [Process(target=render_range, args=(bd[k], bd[k + 1], f"cache/part{k}.mp4")) for k in range(K)]
    for p in ps: p.start()
    build_audio("cache/mix.wav")
    for p in ps: p.join()
    open("cache/parts.txt", "w").write("".join(f"file 'part{k}.mp4'\n" for k in range(K)))
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "cache/parts.txt", "-i", "cache/mix.wav",
                           "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
                           "export/plateformes_chine_tiktok_9x16.mp4"])
    print("export/plateformes_chine_tiktok_9x16.mp4")
