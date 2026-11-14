#!/usr/bin/env python3
"""Version courte verticale (9:16, 1080x1920, ~1 min) de « Les obstacles des commandes en Chine ».
Même voix (extraits de audio/voix_montage.wav, rien de synthétique), mêmes images du Drive, même style.

    python3 build_short.py                 # -> export/obstacles_chine_1min_9x16.mp4
    python3 build_short.py --frames 3 20   # aperçus PNG (cache/apercus_short)
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
SRC_WORDS = json.load(open("audio/mots_montage.json"))["words"]
SRC_WORDS = [w for w in SRC_WORDS if w["text"].strip() not in ("«", "»", "?")]

TOK = []
for i, w in enumerate(SRC_WORDS):
    for t in norm(w["text"]): TOK.append((t, i))
def find(phrase, after, which="start"):
    tgt = norm(phrase)
    for k in range(len(TOK) - len(tgt) + 1):
        if SRC_WORDS[TOK[k][1]]["start"] < after - 0.05: continue
        if [TOK[k + m][0] for m in range(len(tgt))] == tgt:
            return SRC_WORDS[TOK[k + len(tgt) - 1][1]][which] if which == "end" else SRC_WORDS[TOK[k][1]]["start"]
    raise KeyError(phrase)

# ------------------------------------------------------------------ extraits de la voix (début, fin, vers)
CLIPS = [
    ("hook",  "Tu as déjà regardé", "plateforme chinoise", 0),
    ("real",  "Mais dans la réalité", "du combattant", 14),
    ("o1a",   "Trouver un fournisseur", "réellement fiable", 70),
    ("o1b",   "Règle simple", "ton capital", 132),
    ("o2a",   "La barrière linguistique", "de compréhension", 138),
    ("o2b",   "Écris toutes les caractéristiques", "du produit", 163),
    ("o3a",   "Recevoir une qualité différente", "celle attendue", 196),
    ("o3b",   "La meilleure solution", "un échantillon", 220),
    ("o4a",   "Les frais cachés qui changent", "le prix réel", 266),
    ("o4b",   "Mais le prix du produit", "le coût réel", 276),
    ("o5a",   "Les retards de production", "et de livraison", 332),
    ("o5b",   "Commande suffisamment tôt", "marge de sécurité", 371),
    ("o6a",   "Les arnaques et les paiements", "paiements risqués", 388),
    ("o6b",   "Évite de transférer", "jamais testé", 423),
    ("o7a",   "Ne pas calculer la rentabilité", "avant de commander", 441),
    ("o7b",   "Un produit peut donc être populaire", "pas être rentable", 483),
    ("cta",   "rejoins ma chaîne", "dans ma bio", 530),
    ("fin",   "en importation", "le mieux", 540),
]
GAP = {"real": 0.35, "o1a": 0.45, "o2a": 0.45, "o3a": 0.45, "o4a": 0.45, "o5a": 0.45, "o6a": 0.45, "o7a": 0.45, "cta": 0.45, "fin": 0.6}
voice = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", "audio/voix_montage.wav", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]), np.float32)
pieces, WORDS, T = [], [], {}
t_out = 0.25
for key, p0, p1, after in CLIPS:
    a = max(0.0, find(p0, after) - 0.06); b = find(p1, a, "end") + (0.02 if key == "hook" else 0.14)
    assert b - a > 0.5, (key, a, b)
    t_out += GAP.get(key, 0.2) if pieces else 0
    seg = voice[int(a * SR):int(b * SR)].copy(); f = int(0.012 * SR); r = np.linspace(0, 1, f, dtype=np.float32)
    seg[:f] *= r; seg[-f:] *= r[::-1]
    pieces.append((t_out, seg)); T[key] = (t_out, t_out + (b - a))
    for w in SRC_WORDS:
        if a <= w["start"] and w["end"] <= b:
            WORDS.append({"text": w["text"], "start": w["start"] - a + t_out, "end": w["end"] - a + t_out})
    t_out += b - a
VOICE_END = t_out
TOTAL = VOICE_END + 1.2
FIXW = {"Évite": "Évite", "etape": "étape"}
OUTWORDS = WORDS

def wt(phrase, key, which="start"):
    """temps (dans la vidéo courte) d'un mot de l'extrait key."""
    a, b = T[key]; tgt = norm(phrase)
    toks = [(t, i) for i, w in enumerate(WORDS) if a - 0.01 <= w["start"] <= b for t in norm(w["text"])]
    for k in range(len(toks) - len(tgt) + 1):
        if [toks[k + m][0] for m in range(len(tgt))] == tgt:
            return WORDS[toks[k + len(tgt) - 1][1]][which] if which == "end" else WORDS[toks[k][1]]["start"]
    raise KeyError(phrase)

# ------------------------------------------------------------------ helpers
CX = 540
def hook(txt, col=MUTED, size=50): return rich([(txt, "serif_i", size, col)])
def B(t, s=110, c=WHITE): return (t, "xbold", s, c)
def I(t, s=110, c=MINT): return (t, "serif_i", s, c)
def img_frame(code, w, r=30): return shadowed(framed(drive_image(code), w, r))

def vid(code, mode="tile", size=300, w=None, t1=None):
    frames = drive_video(code, size - 60, size - 60, 0.0, t1) if mode == "tile" else drive_video(code, w, w, 0.0, t1)
    cache = {}
    def f(tl):
        i = int(tl * 30) % len(frames)
        if i not in cache:
            fr = frames[i]
            if mode == "tile":
                c = rounded(size, size, rgba(WHITE), 44, outline=(225, 225, 220, 255), width=2)
                c.alpha_composite(fr, ((size - fr.width) // 2, (size - fr.height) // 2)); cache[i] = shadowed(c, 24, (0, 10), 90)
            else:
                cache[i] = shadowed(framed(fr, w), 28, (0, 14), 110)
        return cache[i]
    return f

def strike(w, col=RED, thick=10):
    def f(tl):
        p = ease_out(clamp(tl / 0.35)); im = Image.new("RGBA", (w, thick + 4), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle((0, 2, max(thick, int(w * p)), thick + 2), thick // 2, fill=rgba(col)); return im
    return f

def icon_warn(s=160, col=RED):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(s / 2, 6), (s - 6, s - 10), (6, s - 10)], fill=rgba(col))
    t = rich([("!", "xbold", int(s * .55), WHITE)]); im.alpha_composite(t, ((s - t.width) // 2, int(s * .25))); return im

def calendar_card(n_mint=30, extra=4, w=860):
    c = card(w, 560, light=True); d = ImageDraw.Draw(c)
    c.alpha_composite(rich([("TON PLANNING", "mono", 30, (40, 130, 90))]), (44, 38))
    cell = (w - 88) // 7
    for k in range(n_mint + extra):
        r, q = divmod(k, 7); x = 44 + q * cell; y = 110 + r * 82
        fill = rgba(MINT) if k < n_mint else rgba((24, 30, 27))
        d.rounded_rectangle((x + 5, y, x + cell - 5, y + 68), 14, fill=fill)
        t = rich([(str(k + 1), "semi", 30, WHITE)]); c.alpha_composite(t, (x + (cell - t.width) // 2, y + 12))
    return shadowed(c)

# ------------------------------------------------------------------ scènes
class Sc:
    def __init__(s, key0, key1, bg="dark", ob=None, subs=True, glitch=False, build=None):
        s.t0 = T[key0][0] - (0.25 if key0 == "hook" else GAP.get(key0, 0.2) * 0.5)
        s.k0, s.k1, s.bg, s.ob, s.subs, s.glitch, s.build = key0, key1, bg, ob, subs, glitch, build
        s.els, s.cursors = [], []
    def add(s, *a, **k):
        k.setdefault("t1", s.t1); e = El(*a, **k); s.els.append(e); return e

OB = [("Un fournisseur", "fiable.", "VÉRIFIE"), ("La barrière", "de la langue.", "ÉCRIS TOUT"), ("La qualité", "du produit.", "ÉCHANTILLON"),
      ("Les frais", "cachés.", "FRAIS CACHÉS"), ("Les délais", "de livraison.", "MARGE DE SÉCURITÉ"), ("Les arnaques", "et paiements risqués.", "ARNAQUE"),
      ("La rentabilité", "calculée avant.", "CALCULE")]

def headline(S, k, ka, kb):
    l1, l2, st = OB[k - 1]; red = k == 6; col = RED if red else MINT
    tb = T[kb][0] - 0.1
    S.add(rich([(f"{k:02d}", "serif", 380, (255, 255, 255, 55) if not red else (255, 200, 195, 70))]), CX, 640, S.t0, t1=tb, anim="fade", dur=0.3)
    S.add(rich([B(l1, 104)]), CX, 860, S.t0 + 0.05, t1=tb, anim="up", sfx="S9" if red else "S1", gain=-4)
    S.add(rich([I(l2, 112 if len(l2) < 16 else 84, col)]), CX, 990, S.t0 + 0.15, t1=tb, anim="up")
    S.add(stamp(st, col, 60), CX, 1180, S.t0 + 0.55, t1=tb, anim="stamp", dur=0.3)
    # bandeau de rappel pendant la solution
    S.add(rich([(f"{k:02d} · ", "serif_i", 52, col), (l1 + " " + l2.rstrip("."), "bold", 44, WHITE)]), CX, 360, tb, anim="fade")
    return tb

def s_hook(S):
    S.add(hook("sur une plateforme chinoise…", MUTED, 54), CX, 520, S.t0, anim="fade", sfx="S6", gain=-4)
    S.add(rich([B("Tu as déjà regardé", 96)]), CX, 650, 0.25, anim="up")
    S.add(rich([I("un produit", 130)]), CX, 790, wt("un produit", "hook"), anim="up")
    S.add(vid("D8", "frame", w=800), CX, 1090, wt("produit", "hook"), anim="pop", sfx="S10", gain=-5)

def s_real(S):
    S.add(hook("mais dans la réalité…", MUTED, 60), CX, 560, S.t0, anim="fade", sfx="S2", gain=-4)
    S.add(rich([B("commander", 110)]), CX, 720, wt("commander", "real"), anim="up")
    S.add(rich([B("en Chine", 110)]), CX, 840, wt("en Chine", "real"), anim="up")
    tp = wt("parcours", "real")
    S.add(rich([B("un parcours", 120)]), CX, 1020, tp, anim="stamp", dur=0.3, sfx="S5", gain=-2)
    S.add(rich([I("du combattant.", 130, RED)]), CX, 1160, tp + 0.25, anim="stamp", dur=0.3)

def s_o1(S):
    tb = headline(S, 1, "o1a", "o1b")
    S.add(img_frame("D10", 880), CX, 760, tb, anim="fade", kb=1.08)
    S.add(rich([B("Teste le fournisseur", 76)]), CX, 1170, wt("teste", "o1b"), anim="up")
    S.add(rich([B("avant de tester ", 70), I("ton capital.", 80)]), CX, 1270, wt("avant de tester", "o1b"), anim="up", sfx="S5", gain=-3)

def s_o2(S):
    tb = headline(S, 2, "o2a", "o2b")
    S.add(rich([B("écris ", 110), I("tout.", 120)]), CX, 520, tb, anim="up")
    rows = [("Quantité", "100 pièces"), ("Couleur", "noir"), ("Dimensions", "20 × 12 cm"), ("Logo", "1 couleur"), ("Emballage", "individuel")]
    t0 = wt("Écris", "o2b")
    def sheet(tl):
        c = card(900, 600, light=True); c.alpha_composite(rich([("FICHE PRODUIT · À ENVOYER", "mono", 28, (40, 130, 90))]), (48, 40))
        for k, (lab, val) in enumerate(rows):
            tk = tl - 0.1 - k * 0.42
            if tk < 0: break
            n = int(clamp(tk / 0.35) * len(val)); y = 110 + k * 94
            c.alpha_composite(rich([(lab, "semi", 40, GREY)]), (48, y)); c.alpha_composite(rich([(val[:n], "bold", 40, INK)]), (400, y))
            ImageDraw.Draw(c).line([(48, y + 74), (852, y + 74)], fill=(230, 230, 225, 255), width=2)
        return shadowed(c)
    S.add(sheet, CX, 960, t0, anim="up", sfx="S19", gain=-9)

def s_o3(S):
    tb = headline(S, 3, "o3a", "o3b")
    S.add(img_frame("D12", 820), CX, 740, tb, anim="fade", kb=1.06)
    S.add(hook("la meilleure solution :", MUTED, 54), CX, 1130, wt("La meilleure", "o3b"), anim="fade")
    S.add(stamp("ÉCHANTILLON", MINT, 100, -4), CX, 1270, wt("échantillon", "o3b"), anim="stamp", dur=0.35, sfx="S12", gain=-3)

def s_o4(S):
    tb = headline(S, 4, "o4a", "o4b")
    S.add(vid("D2", "tile", 220), CX, 560, tb, anim="pop")
    S.add(label_card("Prix affiché", [("3 $", "serif_i", 220, WHITE)], w=660), CX, 900, tb + 0.15, anim="pop", sfx="S16", gain=-7)
    S.add(stamp("≠ COÛT RÉEL", RED, 80), CX, 1250, wt("coût réel", "o4b"), anim="stamp", sfx="S12", gain=-4)

def s_o5(S):
    tb = headline(S, 5, "o5a", "o5b")
    S.add(rich([B("commande ", 100), I("tôt.", 110)]), CX, 520, wt("Commande", "o5b"), anim="up")
    S.add(calendar_card(30, 5), CX, 900, tb + 0.1, anim="pop")
    S.add(pill("+ marge de sécurité", (24, 30, 27, 255), MINT, 52, fn="bold", pad=(34, 18)), CX, 1250, wt("marge", "o5b"), anim="stamp", sfx="S13", gain=-5)

def s_o6(S):
    tb = headline(S, 6, "o6a", "o6b")
    S.add(icon_warn(170), CX, 560, tb, anim="pop", sfx="S14", gain=-6)
    S.add(rich([B("tout ton capital", 100)]), CX, 780, wt("tout ton capital", "o6b"), anim="up")
    S.add(rich([B("à un fournisseur", 76)]), CX, 900, wt("à un fournisseur", "o6b"), anim="up")
    S.add(rich([I("jamais testé ?", 110, RED)]), CX, 1030, wt("jamais testé", "o6b"), anim="up")
    S.add(stamp("ARNAQUE", RED, 90), CX, 1230, wt("jamais testé", "o6b") + 0.45, anim="stamp", sfx="S12", gain=-5)

def s_o7(S):
    tb = headline(S, 7, "o7a", "o7b")
    S.add(vid("D8", "frame", w=900), CX, 780, tb, anim="fade")
    S.add(rich([B("populaire", 110)]), CX, 1120, wt("populaire", "o7b"), anim="up")
    S.add(rich([I("≠ rentable.", 120, RED)]), CX, 1250, wt("rentable", "o7b"), anim="stamp", sfx="S14", gain=-5)

def s_cta(S):
    tj = wt("rejoins", "cta")
    S.add(rich([B("rejoins", 130)]), CX, 620, S.t0 + 0.1, anim="up")
    S.add(rich([I("ma chaîne.", 140)]), CX, 770, S.t0 + 0.25, anim="up")
    S.add(pill("S'abonner", (47, 208, 138, 255), INK, 64, fn="xbold", pad=(66, 30)), CX, 1000, S.t0 + 0.3, anim="pop")
    tc = wt("chaîne", "cta") + 0.1
    S.add(pill("Abonné ✓", (24, 30, 27, 255), WHITE, 64, fn="xbold", pad=(66, 30)), CX, 1000, tc, anim="none", sfx="S20", gain=-4)
    S.cursors.append(Cursor([(S.t0 + 0.3, 900, 1400), (tc - 0.15, 560, 1012), (tc + 0.6, 560, 1012), (tc + 1.2, 860, 1060)], [tc], S.t1))
    S.add(pill("le lien est dans ma bio", (255, 255, 255, 240), INK, 50, pad=(34, 18)), CX, 1200, wt("Le lien", "cta"), anim="up", sfx="S10", gain=-6)

def s_fin(S):
    S.add(hook("en importation,", MUTED, 60), CX, 520, wt("en importation", "fin"), anim="fade")
    S.add(rich([B("ce n'est pas celui qui", 76)]), CX, 660, wt("ce n'est pas", "fin"), anim="up")
    S.add(rich([I("commande le plus", 96, WHITE)]), CX, 770, wt("commande le plus", "fin"), anim="up")
    S.add(rich([B("qui réussit,", 76)]), CX, 880, wt("qui réussit", "fin"), anim="up")
    S.add(rich([B("c'est celui qui", 90)]), CX, 1060, wt("c'est celui", "fin"), anim="up")
    S.add(rich([I("vérifie le mieux.", 110)]), CX, 1190, wt("vérifie", "fin"), anim="up")

SCENES = [Sc("hook", "hook", build=s_hook), Sc("real", "real", "black", glitch=True, build=s_real),
          Sc("o1a", "o1b", ob=1, build=s_o1), Sc("o2a", "o2b", ob=2, build=s_o2), Sc("o3a", "o3b", ob=3, build=s_o3),
          Sc("o4a", "o4b", "grid", ob=4, build=s_o4), Sc("o5a", "o5b", ob=5, build=s_o5), Sc("o6a", "o6b", ob=6, glitch=True, build=s_o6),
          Sc("o7a", "o7b", ob=7, build=s_o7), Sc("cta", "cta", build=s_cta), Sc("fin", "fin", "black", subs=False, build=s_fin)]
SCENES[0].t0 = 0.0
for i, s in enumerate(SCENES): s.t1 = SCENES[i + 1].t0 if i + 1 < len(SCENES) else TOTAL
for s in SCENES: s.build(s)

# ------------------------------------------------------------------ suivi + sous-titres
@lru_cache(None)
def tracker_img(cur):
    sz, gap = 56, 12; im = Image.new("RGBA", (7 * sz + 6 * gap + 8, sz + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(7):
        x = 4 + k * (sz + gap); n = k + 1
        if n < cur:
            d.rounded_rectangle((x, 4, x + sz, 4 + sz), 12, fill=rgba(MINT)); d.line([(x + 15, 33), (x + 25, 43), (x + 42, 20)], fill=WHITE, width=5)
        elif n == cur:
            d.rounded_rectangle((x, 4, x + sz, 4 + sz), 12, fill=(255, 255, 255, 255))
            t = rich([(str(n), "bold", 32, (24, 30, 27))]); im.alpha_composite(t, (x + (sz - t.width) // 2 + 1, 4 + (sz - t.height) // 2))
        else:
            d.rounded_rectangle((x, 4, x + sz, 4 + sz), 12, fill=(255, 255, 255, 40), outline=(255, 255, 255, 90), width=2)
            t = rich([(str(n), "bold", 30, (255, 255, 255, 150))]); im.alpha_composite(t, (x + (sz - t.width) // 2 + 1, 4 + (sz - t.height) // 2))
    return im

KEY = set(norm("fournisseur échantillon qualité prix capital frais délais marge coût réel arnaques Chine produit rentabilité rentable "
               "testé teste caractéristiques langue combattant sécurité chaîne bio vérifie mieux paiements"))
def build_subs():
    chunks, cur = [], []
    for w in WORDS:
        txt = w["text"].strip()
        if cur and not (txt.startswith("'") or txt.startswith("-")):
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
            t = w["text"].strip(); txt += t if (t.startswith("'") or t.startswith("-")) else " " + t
        out.append((a, b, txt.strip().rstrip(",")))
    return out
SUBS = build_subs()

@lru_cache(None)
def sub_img(txt, pillbg):
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
    for s in SCENES:
        if s.t0 <= t < s.t1: return s
    return SCENES[-1]

def render_frame(t):
    s = scene_at(t); fr = background(s.bg).copy()
    for e in s.els: draw_el(fr, e, t)
    for c in s.cursors: draw_cursor(fr, c, t)
    if s.ob:
        ti = tracker_img(s.ob); paste(fr, ti, (E.W - ti.width) / 2, 200)
    if s.subs:
        for a, b, txt in SUBS:
            if a <= t < b:
                im = sub_img(txt, False); paste(fr, im, (E.W - im.width) / 2, 1430 - im.height / 2); break
    out = fr.convert("RGB")
    if s.glitch and t - s.t0 < 0.22: out = glitch(out, 1 - (t - s.t0) / 0.22)
    if t > VOICE_END + 0.5: out = Image.blend(out, Image.new("RGB", out.size), clamp((t - VOICE_END - 0.5) / 0.6))
    return out

# ------------------------------------------------------------------ audio
def load_audio(path):
    return np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]), np.float32).reshape(-1, 2).copy()
SFX_FILES = {f.split("_")[0]: os.path.join("audio/sfx", f) for f in os.listdir("audio/sfx") if f.endswith(".mp3")}
def sfx_events():
    ev = sorted((e.t0, e.sfx, e.gain) for s in SCENES for e in s.els if e.sfx); kept = []; last = -9
    for t, c, g in ev:
        if t - last >= 0.7: kept.append((t, c, g)); last = t
    return kept

def build_audio(out):
    n = int(TOTAL * SR) + SR; mix = np.zeros((n, 2), np.float32)
    for t0, seg in pieces:
        i = int(t0 * SR); mix[i:i + len(seg)] += seg[:, None]
    for t, code, g in sfx_events():
        a = load_audio(SFX_FILES[code])[: int(SR * (2.0 if code in ("S19",) else 3.0))]
        fl = int(0.15 * SR); a[-fl:] *= np.linspace(1, 0, fl)[:, None]
        a = a / (np.abs(a).max() + 1e-9) * 10 ** ((-17 + g) / 20); i = int(t * SR); j = min(n, i + len(a)); mix[i:j] += a[: j - i]
    if not os.path.exists("cache/musique.wav"):
        raise SystemExit("lance d'abord build_chine.py (cache/musique.wav)")
    mus = load_audio("cache/musique.wav")[int(20 * SR):]          # passage plus rythmé de la piste
    m = np.zeros((n, 2), np.float32); L = min(n, len(mus)); m[:L] = mus[:L]
    env = np.ones(n, np.float32) * 10 ** (-23 / 20)
    i0 = int((T["fin"][0] - 1.0) * SR); env[i0:] = 0; env[i0 - SR:i0] *= np.linspace(1, 0, SR)
    env[: int(0.8 * SR)] *= np.linspace(0, 1, int(0.8 * SR))
    mix += m * env[:, None]; mix = mix[: int(TOTAL * SR)]
    mix *= 0.97 / max(0.97, np.abs(mix).max())
    mix.astype(np.float32).tofile("cache/mix_short.f32")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "cache/mix_short.f32",
                           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), out])

def render_range(i0, i1, path):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{E.W}x{E.H}", "-r", "30", "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for i in range(i0, i1): p.stdin.write(render_frame(i / 30).tobytes())
    p.stdin.close(); p.wait()

if __name__ == "__main__":
    print(f"durée : {TOTAL:.1f} s")
    for s in SCENES: print(f"  {s.k0:5s} {s.t0:6.2f} -> {s.t1:6.2f}")
    if "--frames" in sys.argv:
        os.makedirs("cache/apercus_short", exist_ok=True)
        for a in sys.argv[sys.argv.index("--frames") + 1:]:
            render_frame(float(a)).save(f"cache/apercus_short/f_{float(a):06.2f}.png")
        sys.exit()
    N = int(TOTAL * 30); K = 4; bd = [N * k // K for k in range(K + 1)]
    ps = [Process(target=render_range, args=(bd[k], bd[k + 1], f"cache/short{k}.mp4")) for k in range(K)]
    for p in ps: p.start()
    build_audio("cache/mix_short.wav")
    for p in ps: p.join()
    open("cache/short_parts.txt", "w").write("".join(f"file 'short{k}.mp4'\n" for k in range(K)))
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "cache/short_parts.txt", "-i", "cache/mix_short.wav",
                           "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
                           "export/obstacles_chine_1min_9x16.mp4"])
    print("export/obstacles_chine_1min_9x16.mp4")
