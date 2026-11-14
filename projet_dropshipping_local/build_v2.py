#!/usr/bin/env python3
"""Rendu V2 — « Dropshipping local » sur la voix originale de Samantha (audio WhatsApp nettoyé).

    python3 nettoyer_voix.py            # doublons, hésitations et longs silences retirés
    python3 build_v2.py --plan          # PLAN_DE_MONTAGE_V2.md
    python3 build_v2.py --preview 2,10  # cache/v2_preview_*.jpg
    python3 build_v2.py                 # export/dropshipping_local_voix_originale_9x16.mp4

Style repris de la vidéo de référence : plans courts, gros titres (lettres bâton + italique jaune),
petits sous-titres avec mots-clés en jaune, arrivées par zoom flou, coupes franches.
"""
import os, sys, json, math, re, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT); sys.path.insert(0, ROOT)
import plan_v2 as P

W, H, FPS = 1080, 1920, 30
YELLOW, WHITE, INK, CREAM, GREEN = (255, 205, 40), (255, 255, 255), (18, 18, 22), (248, 242, 232), (37, 211, 102)
FD = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(FD + f"InterDisplay-{w}.otf", s)
FONTS = "/home/user/digitalrpofitM/projet_shein_flow/fonts/"
def anton(s): return ImageFont.truetype(FONTS + "Anton.woff2", s)
def script(s): return ImageFont.truetype(FONTS + "PlayfairDisplay-Italic-900.ttf", s)
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x):  # léger dépassement, comme les titres de la référence
    x = clamp(x); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

WORDS = json.load(open("audio/voix_mots.json"))["words"]
VOICE = "audio/voix_nettoyee.wav"
VOICE_END = WORDS[-1]["end"]
TOTAL = round(VOICE_END + P.CTA_HOLD, 2)
def wt(i): return WORDS[i]["start"]

# ------------------------------------------------------------------ plans
SHOTS = []
for n, (wi, f, crop, mv, tr, off) in enumerate(P.SHOTS):
    t0 = 0.0 if n == 0 else max(0.0, wt(wi) - 0.06)
    SHOTS.append(dict(w=wi, f=f, crop=crop, mv=mv, tr=tr, off=off, t0=t0))
for n in range(len(SHOTS)): SHOTS[n]["t1"] = SHOTS[n + 1]["t0"] if n + 1 < len(SHOTS) else TOTAL

def is_video(f): return P.F.get(f, "").endswith(".mp4")

@functools.lru_cache(maxsize=None)
def src_image(f):
    im = Image.open(P.M + P.F[f]).convert("RGB")
    for x0, y0, x1, y1 in P.BLUR.get(f, []):
        bx = (int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height))
        im.paste(im.crop(bx).filter(ImageFilter.GaussianBlur(14)), bx[:2])
    return im

class VideoShot:
    def __init__(self, f, off):
        self.path = P.M + P.F[f]
        j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                                                "-show_entries", "format=duration", "-of", "json", self.path]))
        w, h = j["streams"][0]["width"], j["streams"][0]["height"]; dur = float(j["format"]["duration"])
        sc = min(1.0, 2000 / max(w, h)); self.ow, self.oh = int(w * sc) // 2 * 2, int(h * sc) // 2 * 2
        off = off % max(0.1, dur - 1.5)
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(off), "-stream_loop", "-1", "-i", self.path, "-vf",
                                   f"fps={FPS},scale={self.ow}:{self.oh}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.n = -1; self.last = None
    def frame(self, n):
        sz = self.ow * self.oh * 3
        while self.n < n:
            b = self.p.stdout.read(sz)
            if len(b) < sz: break
            self.last = Image.frombytes("RGB", (self.ow, self.oh), b); self.n += 1
        return self.last
    def close(self): self.p.kill()

_open = {}
def source(i, t):
    s = SHOTS[i]
    if is_video(s["f"]):
        if i not in _open: _open[i] = VideoShot(s["f"], s["off"])
        return _open[i].frame(int((t - s["t0"]) * FPS))
    return src_image(s["f"])

def cover(im, cx, cy, z):
    sw, sh = im.size
    if sw / sh > W / H: rh = sh / z; rw = rh * W / H
    else: rw = sw / z; rh = rw * H / W
    l = clamp(cx * sw - rw / 2, 0, sw - rw); t = clamp(cy * sh - rh / 2, 0, sh - rh)
    return im.transform((W, H), Image.AFFINE, (rw / W, 0, l, 0, rh / H, t), Image.BICUBIC)

_vig = None
def grade(im, grey=False):
    global _vig
    if grey: im = ImageEnhance.Color(im).enhance(0.25); im = ImageEnhance.Contrast(im).enhance(0.92)
    else: im = ImageEnhance.Contrast(im).enhance(1.06); im = ImageEnhance.Color(im).enhance(1.06)
    if _vig is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2)
        _vig = Image.fromarray((np.clip(1 - 0.30 * d ** 2.2, 0, 1) * 255).astype(np.uint8))
    return Image.composite(im, Image.new("RGB", (W, H), (8, 6, 4)), _vig)

def render_shot(i, t):
    s = SHOTS[i]; k = clamp((t - s["t0"]) / max(0.1, s["t1"] - s["t0"]))
    cx, cy, z = s["crop"]
    mv = s["mv"]
    if mv == "in": z *= 1 + 0.07 * ease(k)
    elif mv == "out": z *= 1.07 - 0.07 * ease(k)
    elif mv == "gauche": cx -= 0.05 * ease(k); z *= 1.04
    elif mv == "droite": cx += 0.05 * ease(k); z *= 1.04
    return grade(cover(source(i, t), cx, cy, z), s["f"] in P.GRISE)

# ------------------------------------------------------------------ tableau de bord Chariow (capture réelle de Samantha)
DASH_CROP = (0, 226, 2000, 900); DASH_TARGET = (352, 384, 1000, 674); DASH_HL = (455, 500, 728, 575)
@functools.lru_cache(maxsize=None)
def dash_src(): return Image.open(P.M + P.F["35"]).convert("RGB").crop(DASH_CROP)
@functools.lru_cache(maxsize=None)
def dash_bg():
    im = cover(Image.open(P.M + P.F["35"]).convert("RGB"), 0.5, 0.55, 1.0).filter(ImageFilter.GaussianBlur(30))
    return Image.blend(im, Image.new("RGB", (W, H), (12, 12, 16)), 0.62)
def render_dash(i, t):
    s = SHOTS[i]; src = dash_src(); sw, sh = src.size
    k = ease((t - s["t0"] - 0.3) / 1.0)
    v = [(0, 0, sw, sh)[j] + (DASH_TARGET[j] - (0, 0, sw, sh)[j]) * k for j in range(4)]
    dw = 1000; dh = int(dw * (v[3] - v[1]) / (v[2] - v[0]))
    view = src.crop(tuple(int(x) for x in v)).resize((dw, dh), Image.LANCZOS)
    im = dash_bg().copy(); x0 = (W - dw) // 2; y0 = 760 - dh // 2
    sh_ = Image.new("RGBA", (dw + 120, dh + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh_).rounded_rectangle((60, 76, dw + 60, dh + 76), 28, fill=(0, 0, 0, 140)); sh_ = sh_.filter(ImageFilter.GaussianBlur(22))
    im.paste(sh_, (x0 - 60, y0 - 60), sh_)
    m = Image.new("L", (dw, dh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, dw - 1, dh - 1), 28, fill=255)
    im.paste(view, (x0, y0), m)
    if k > 0.95:
        sx = dw / (v[2] - v[0]); sy = dh / (v[3] - v[1]); a = 0.6 + 0.4 * abs(math.sin((t - s["t0"]) * 6))
        ImageDraw.Draw(im, "RGBA").rounded_rectangle((x0 + (DASH_HL[0] - v[0]) * sx - 14, y0 + (DASH_HL[1] - v[1]) * sy - 12,
                                                      x0 + (DASH_HL[2] - v[0]) * sx + 14, y0 + (DASH_HL[3] - v[1]) * sy + 12),
                                                     18, outline=YELLOW + (int(255 * a),), width=9)
    return im

# ------------------------------------------------------------------ carton final (CTA)
@functools.lru_cache(maxsize=None)
def cta_bg():
    im = cover(src_image("16"), 0.5, 0.5, 1.0).filter(ImageFilter.GaussianBlur(26))
    return Image.blend(im, Image.new("RGB", (W, H), (14, 12, 10)), 0.58)
def text_c(d, xy, s, f, fill): w = d.textlength(s, font=f); d.text((xy[0] - w / 2, xy[1]), s, font=f, fill=fill)
def render_cta(i, t):
    t0 = SHOTS[i]["t0"]; im = cta_bg().copy().convert("RGBA"); d = ImageDraw.Draw(im)
    a = ease_out((t - t0) / 0.4)
    text_c(d, (W // 2, 240 - (1 - a) * 30), "ÉCRIS « LOCAL »", anton(118), YELLOW + (int(255 * a),))
    text_c(d, (W // 2, 380 - (1 - a) * 30), "EN COMMENTAIRE", anton(96), WHITE + (int(255 * a),))
    pw, ph = 820, 600; px, py = (W - pw) // 2, 590
    card = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, pw - 1, ph - 1), 44, fill=(250, 250, 250, 255))
    text_c(cd, (pw // 2, 34), "Commentaires", font("Bold", 40), INK)
    cd.line((40, 104, pw - 40, 104), fill=(225, 225, 228), width=3)
    li = next(j for j in range(len(WORDS)) if WORDS[j]["text"].startswith("LOCAL"))
    tl = wt(li); typed = int(clamp((t - tl) / 0.5) * 5); sent = t >= tl + 0.8
    if sent:
        ks = ease_out((t - tl - 0.8) / 0.3)
        cd.ellipse((44, 150, 124, 230), fill=(205, 205, 212))
        cd.text((146, 148), "toi", font=font("SemiBold", 32), fill=(120, 120, 128))
        cd.text((146, 190), "LOCAL", font=font("Black", 64), fill=INK + (int(255 * ks),))
        cd.text((pw - 120, 200), "♥", font=font("Bold", 46), fill=(235, 70, 90, int(255 * ks)))
    cd.rounded_rectangle((36, ph - 140, pw - 36, ph - 40), 50, fill=(238, 238, 241))
    s = "LOCAL"[:typed] if not sent else ""
    cd.text((78, ph - 120), s if s else "Ajoute un commentaire…", font=font("Bold" if s else "Medium", 50), fill=INK if s else (150, 150, 158))
    if s and int(t * 3) % 2 == 0:
        x = 78 + cd.textlength(s, font=font("Bold", 50)) + 6; cd.rectangle((x, ph - 116, x + 5, ph - 64), fill=(255, 60, 90))
    cd.ellipse((pw - 132, ph - 128, pw - 52, ph - 52), fill=(255, 60, 90) if typed else (220, 220, 225))
    cd.polygon([(pw - 104, ph - 108), (pw - 104, ph - 72), (pw - 72, ph - 90)], fill=WHITE)
    shd = Image.new("RGBA", (pw + 120, ph + 120), (0, 0, 0, 0)); ImageDraw.Draw(shd).rounded_rectangle((60, 80, pw + 60, ph + 80), 44, fill=(0, 0, 0, 120))
    im.alpha_composite(shd.filter(ImageFilter.GaussianBlur(24)), (px - 60, py - 60))
    card.putalpha(card.getchannel("A").point(lambda v: int(v * a))); im.alpha_composite(card, (px, py))
    ji = next(j for j in range(li, len(WORDS)) if WORDS[j]["text"].lower().startswith("je"))
    b = ease_out((t - wt(ji)) / 0.35)
    if b > 0:
        f2 = font("Bold", 46); s2 = "Je t'envoie le lien de ma chaîne WhatsApp"
        w2 = d.textlength(s2, font=f2) + 70; y2 = 1270 + (1 - b) * 30
        d.rounded_rectangle(((W - w2) / 2, y2, (W + w2) / 2, y2 + 92), 46, fill=GREEN + (int(255 * b),))
        text_c(d, (W // 2, y2 + 18), s2, f2, WHITE + (int(255 * b),))
    return im.convert("RGB")

# ------------------------------------------------------------------ textes animés
def shadow_text(layer, xy, s, f, fill, sh=10):
    d = ImageDraw.Draw(layer)
    d.text((xy[0] + sh * 0.5, xy[1] + sh), s, font=f, fill=(0, 0, 0, 120))
    d.text(xy, s, font=f, fill=fill)

def draw_titre(im, t, t0, t1, l1, l2):
    """Gros titre : ligne en lettres bâton blanches + ligne en italique jaune (style de la référence)."""
    k = back((t - t0) / 0.35); fo = clamp((t1 - t) / 0.18); a = clamp((t - t0) / 0.15) * fo
    if a <= 0: return
    layer = Image.new("RGBA", (W, 560), (0, 0, 0, 0))
    f1 = anton(210); w1 = ImageDraw.Draw(layer).textlength(l1, font=f1)
    while w1 > 940: f1 = anton(f1.size - 10); w1 = ImageDraw.Draw(layer).textlength(l1, font=f1)
    f2 = script(112); w2 = ImageDraw.Draw(layer).textlength(l2, font=f2)
    while w2 > 960: f2 = script(f2.size - 6); w2 = ImageDraw.Draw(layer).textlength(l2, font=f2)
    shadow_text(layer, ((W - w1) / 2, 40), l1, f1, WHITE + (255,))
    shadow_text(layer, ((W - w2) / 2, 40 + f1.size * 1.45), l2, f2, YELLOW + (255,), 6)
    sc = 0.85 + 0.15 * k; lw, lh = int(W * sc), int(560 * sc)
    layer = layer.resize((lw, lh), Image.BICUBIC); layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    im.paste(layer, ((W - lw) // 2, 300 - (lh - 560) // 2), layer)

def pill(im, s, cx, cy, a, bg=CREAM, fg=INK, size=72, f=None):
    f = f or anton(size); d = ImageDraw.Draw(im, "RGBA"); w = d.textlength(s, font=f)
    while w > 900: size -= 4; f = anton(size); w = d.textlength(s, font=f)
    pad = 38; h = size * 1.45
    d.rounded_rectangle((cx - w / 2 - pad, cy - h / 2, cx + w / 2 + pad, cy + h / 2), h / 2.6, fill=bg + (int(240 * a),))
    d.text((cx - w / 2, cy - h / 2 + size * 0.12), s, font=f, fill=fg + (int(255 * a),))

def draw_overlays(im, t):
    for (w0, w1, kind, data) in P.OVERLAYS:
        t0 = wt(w0) - 0.05; t1 = wt(w1) - 0.08 if w1 < len(WORDS) else TOTAL
        if not (t0 <= t < t1): continue
        a = ease_out((t - t0) / 0.22) * clamp((t1 - t) / 0.15)
        if kind == "titre": draw_titre(im, t, t0, t1, *data)
        elif kind == "pastille": pill(im, data, W // 2, 470 - (1 - a) * 20, a)
        elif kind == "annee":
            d = ImageDraw.Draw(im, "RGBA"); f = anton(250); w = d.textlength(data, font=f)
            col = (215, 208, 196) if "2023" in data else YELLOW
            k = back((t - t0) / 0.35); y = 360 + (1 - k) * 40
            d.text(((W - w) / 2 + 6, y + 12), data, font=f, fill=(0, 0, 0, int(110 * a)))
            d.text(((W - w) / 2, y), data, font=f, fill=col + (int(255 * a),))
        elif kind == "etapes": draw_etapes(im, t, a)
        elif kind == "reseaux": draw_liste(im, t, a, P.RESEAUX, numbered=False)
        elif kind == "trois": draw_liste(im, t, a, P.TROIS, numbered=True)
        elif kind == "marge": draw_marge(im, t, a)

def draw_etapes(im, t, a):
    """Fournisseur → Présentation → Commande → Livraison : l'étape en cours s'allume."""
    d = ImageDraw.Draw(im, "RGBA"); sz = 40
    names = [n for n, _ in P.ETAPES]
    while True:
        f = font("Black", sz); ws = [d.textlength(n, font=f) + 36 for n in names]; gap = 26
        tot = sum(ws) + gap * (len(ws) - 1)
        if tot <= 1010 or sz <= 26: break
        sz -= 2
    x = (W - tot) / 2; y = 270
    cur = max([i for i, (_, w) in enumerate(P.ETAPES) if t >= wt(w) - 0.05] or [-1])
    for i, (n, w) in enumerate(zip(names, ws)):
        on = i <= cur; act = i == cur
        bg = YELLOW if act else ((250, 250, 250) if on else (40, 40, 44))
        fg = INK if on else (170, 170, 176)
        k = back((t - wt(P.ETAPES[i][1])) / 0.3) if act else 1
        hh = 74 * (0.92 + 0.08 * k)
        d.rounded_rectangle((x, y - hh / 2, x + w, y + hh / 2), 30, fill=bg + (int(235 * a),))
        d.text((x + 18, y - sz * 0.62), n, font=f, fill=fg + (int(255 * a),))
        if i < len(names) - 1: d.text((x + w + 5, y - sz * 0.62), "›", font=font("Black", 40), fill=WHITE + (int(220 * a),))
        x += w + gap

def draw_liste(im, t, a, items, numbered):
    d = ImageDraw.Draw(im, "RGBA"); f = font("Black", 54); y = 330
    for i, (s, w) in enumerate(items):
        k = ease_out((t - wt(w) + 0.05) / 0.25) * a
        if k <= 0: continue
        label = (f"{i + 1}  " if numbered else "") + s
        tw = d.textlength(label, font=f); x = 90 - (1 - k) * 40
        last = i == max(j for j, (_, ww) in enumerate(items) if t >= wt(ww) - 0.05)
        d.rounded_rectangle((x, y, x + tw + 60, y + 96), 26, fill=(YELLOW if last else CREAM) + (int(240 * k),))
        d.text((x + 30, y + 14), label, font=f, fill=INK + (int(255 * k),))
        y += 116

def draw_marge(im, t, a):
    d = ImageDraw.Draw(im, "RGBA"); x0, y0, w, h = 150, 290, 640, 520
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 28, fill=CREAM + (int(244 * a),))
    for yy in range(y0 + 116, y0 + h - 20, 92): d.line((x0 + 40, yy, x0 + w - 40, yy), fill=(200, 190, 175, int(255 * a)), width=2)
    d.text((x0 + 44, y0 + 30), "Je calcule", font=anton(70), fill=INK + (int(255 * a),))
    rows = [m for m in P.MARGE if m[0] != "Marge"]; tm = [m for m in P.MARGE if m[0] == "Marge"][0][1]
    for r, (s, wi) in enumerate(rows):
        b = clamp((t - wt(wi)) / 0.25) * a
        if b > 0: d.text((x0 + 60, y0 + 134 + r * 92), "+ " + s, font=font("Bold", 46), fill=INK + (int(255 * b),))
    b = clamp((t - WORDS[tm]["start"] - 0.3) / 0.3) * a        # « marge » arrive en dernier
    if b > 0:
        yb = y0 + 134 + len(rows) * 92 - 8
        d.rounded_rectangle((x0 + 40, yb, x0 + w - 40, yb + 84), 22, fill=YELLOW + (int(255 * b),))
        d.text((x0 + 62, yb + 6), "= MA MARGE", font=anton(62), fill=INK + (int(255 * b),))

# ------------------------------------------------------------------ sous-titres (voix réelle)
def norm(w): return re.sub(r"[^\w$]", "", w.lower().replace("’", "'"))
def keyword_marks():
    n = [norm(w["text"]) for w in WORDS]; marks = set()
    for kw in P.KEYWORDS:
        kt = [norm(x) for x in kw.split()]
        for j in range(len(n) - len(kt) + 1):
            if n[j:j + len(kt)] == kt and (kw != "LOCAL" or WORDS[j]["text"].startswith("LOCAL")):
                marks.update(range(j, j + len(kt)))
    return marks
MARKS = keyword_marks()
def chunks():
    out, cur = [], []
    for j, w in enumerate(WORDS):
        cur.append(j); txt = " ".join(WORDS[x]["text"] for x in cur)
        stop = len(cur) >= 4 or len(txt) >= 22 or w["text"].endswith((",", ".", "?", "!"))
        if stop and not (j in MARKS and j + 1 in MARKS): out.append(cur); cur = []
    if cur: out.append(cur)
    res = []
    for c, ids in enumerate(out):
        t0 = wt(ids[0]); t1 = wt(out[c + 1][0]) if c + 1 < len(out) else WORDS[ids[-1]]["end"] + 0.4
        res.append((t0, min(t1, WORDS[ids[-1]]["end"] + 0.5), ids))
    return res
CHUNKS = chunks()
SUB_Y, SUB_CX = 1300, 520
def draw_subs(im, t):
    c = next((c for c in CHUNKS if c[0] <= t < c[1]), None)
    if not c or t >= wt(360) - 0.05: return       # le carton final porte ses propres textes
    t0, t1, ids = c; f = font("Black", 62); gap = 16; d = ImageDraw.Draw(im)
    words = [WORDS[j]["text"] for j in ids]; ws = [d.textlength(w, font=f) for w in words]
    tot = sum(ws) + gap * (len(ws) - 1)
    if tot > 860:
        f = font("Black", int(62 * 860 / tot)); ws = [d.textlength(w, font=f) for w in words]; tot = sum(ws) + gap * (len(ws) - 1)
    layer = Image.new("RGBA", (int(tot) + 60, 120), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer); x = 30
    for j, w, wd in zip(ids, words, ws):
        said = t >= wt(j) - 0.03
        col = (YELLOW if j in MARKS else WHITE) if said else (WHITE if j not in MARKS else YELLOW)
        alpha = 255 if said else 150
        ld.text((x, 18), w, font=f, fill=col + (alpha,), stroke_width=6, stroke_fill=(10, 10, 12, 255))
        x += wd + gap
    k = ease_out((t - t0) / 0.1); sc = 0.92 + 0.08 * k
    layer = layer.resize((int(layer.width * sc), int(layer.height * sc)), Image.BICUBIC)
    im.paste(layer, (int(SUB_CX - layer.width / 2), int(SUB_Y - layer.height / 2)), layer)

# ------------------------------------------------------------------ image finale
def shot_index(t):
    for i, s in enumerate(SHOTS):
        if s["t0"] <= t < s["t1"]: return i
    return len(SHOTS) - 1
def base(i, t):
    f = SHOTS[i]["f"]
    return render_cta(i, t) if f == "CTA" else render_dash(i, t) if f == "DASH" else render_shot(i, t)
def frame(t):
    i = shot_index(t); s = SHOTS[i]; im = base(i, t); dt = t - s["t0"]
    if i > 0 and s["tr"] == "zoom" and dt < 0.22:
        k = ease_out(dt / 0.22); z = 1.14 - 0.14 * k
        big = im.resize((int(W * z), int(H * z)), Image.BILINEAR)
        im = big.crop(((big.width - W) // 2, (big.height - H) // 2, (big.width - W) // 2 + W, (big.height - H) // 2 + H))
        im = im.filter(ImageFilter.GaussianBlur(14 * (1 - k)))
    elif i > 0 and s["tr"] == "fondu" and dt < 0.22:
        im = Image.blend(base(i - 1, s["t0"] - 0.01), im, ease(dt / 0.22))
    for j in list(_open):
        if j < i - 1: _open.pop(j).close()
    im = im.convert("RGBA")
    if s["f"] != "CTA": draw_overlays(im, t); draw_subs(im, t)
    return im.convert("RGB")

# ------------------------------------------------------------------ son
MUSIC = "audio/music/music_motivating_mornings.mp3"
def music_expr():
    a = wt(258); b = wt(305); c = wt(360)
    return (f"0.11*(1+0.35*between(t,{a},{b})-0.55*gte(t,{c - 1.0})*min(1,(t-{c - 1.0})/1.0))")
def build_audio(out="cache/mix_v2.wav"):
    inp = ["-i", MUSIC, "-i", MUSIC, "-i", VOICE]
    fc = [f"[0:a][1:a]acrossfade=d=3[mm]",
          f"[mm]aresample=48000,atrim=0:{TOTAL},volume='{music_expr()}':eval=frame,afade=t=in:d=0.3,afade=t=out:st={TOTAL - 1.5}:d=1.5[m]",
          "[2:a]aresample=48000,aformat=channel_layouts=stereo[v]"]
    lab = ["[m]", "[v]"]
    for n, (wi, f, g, off) in enumerate(P.SFX):
        t = max(0.0, wt(wi) + off); rev = f.endswith("_inverse"); f = f.replace("_inverse", "")
        inp += ["-i", f"audio/sfx/{f}.mp3"]
        fc.append(f"[{n + 3}:a]aresample=48000,aformat=channel_layouts=stereo,{'areverse,' if rev else ''}atrim=0:1.4,afade=t=out:st=1.0:d=0.4,volume={g}dB,adelay={int(t * 1000)}|{int(t * 1000)}[s{n}]")
        lab.append(f"[s{n}]")
    fc.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0:duration=longest,atrim=0:{TOTAL},alimiter=limit=0.89:level=false[o]")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", ";".join(fc), "-map", "[o]", "-ac", "2", out])
    return out
def render(out="export/dropshipping_local_voix_originale_9x16.mp4"):
    mix = build_audio()
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", mix, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
    for n in range(round(TOTAL * FPS)): p.stdin.write(frame(n / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK ->", out, f"({TOTAL:.1f} s)")

# ------------------------------------------------------------------ plan de montage
TR = {"cut": "coupe franche", "zoom": "arrivée par zoom flou", "fondu": "fondu court"}
def write_plan():
    ov = {}
    for (w0, w1, kind, data) in P.OVERLAYS:
        txt = {"titre": lambda d: f"{d[0]} — {d[1]}", "pastille": lambda d: d, "annee": lambda d: d,
               "etapes": lambda d: "Fournisseur → Présentation → Commande → Livraison (l'étape s'allume au mot)",
               "reseaux": lambda d: "WhatsApp · Instagram · TikTok · Facebook (au fil des mots)",
               "trois": lambda d: "1 Choisir · 2 Vérifier le prix · 3 Présenter",
               "marge": lambda d: "Carnet « Ma marge » : achat + livraison + communication = MARGE"}[kind](data)
        ov.setdefault(w0, []).append(txt)
    sfx = {wi: f for wi, f, g, o in P.SFX}
    names = {"DASH": f"`{P.F['35']}` (tableau de bord Chariow, rapprochement sur le revenu total)",
             "CTA": "carton final : zone de commentaires stylisée"}
    rows = ["| Phrase prononcée | Fichier exact | Passage | Texte à l'écran | Son et transition |", "|---|---|---|---|---|"]
    for n, s in enumerate(SHOTS):
        w1 = SHOTS[n + 1]["w"] if n + 1 < len(SHOTS) else len(WORDS)
        phrase = " ".join(WORDS[j]["text"] for j in range(s["w"], w1))
        f = names[s["f"]] if s["f"] in names else f"`{P.F[s['f']]}`" + (" (désaturé)" if s["f"] in P.GRISE else "")
        txts = "; ".join(t for j in range(s["w"], w1) for t in ov.get(j, [])) or "—"
        snd = ", ".join(sfx[j] for j in range(s["w"], w1) if j in sfx)
        rows.append(f"| {phrase} | {f} | {s['t0']:.1f}–{s['t1']:.1f} s | {txts} | {TR[s['tr']]}{(' ; ' + snd) if snd else ''} |")
    hdr = (f"# Plan de montage V2 — voix originale (audio WhatsApp)\n\nDurée : {TOTAL:.1f} s. Voix : `{VOICE}` "
           "(doublons, hésitations et longs silences retirés par `nettoyer_voix.py`).\n"
           "Musique : Mixkit « Motivating Mornings », plus calme au début, plus présente sur les étapes pratiques, baissée avant le CTA.\n\n")
    open("PLAN_DE_MONTAGE_V2.md", "w").write(hdr + "\n".join(rows) + "\n"); print("PLAN_DE_MONTAGE_V2.md écrit")

if __name__ == "__main__":
    if "--plan" in sys.argv: write_plan()
    elif "--preview" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1].split(",")]
        ims = [frame(t).resize((360, 640)) for t in ts]
        for j in range(0, len(ims), 6):
            g = Image.new("RGB", (360 * 6, 640), "white")
            for i, im in enumerate(ims[j:j + 6]): g.paste(im, (i * 360, 0))
            g.save(f"cache/v2_preview_{j // 6}.jpg", quality=85)
        print("ok", TOTAL)
    else: render()
