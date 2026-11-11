#!/usr/bin/env python3
"""Rendu du TikTok faceless « Dropshipping local avec 50 dollars » (1080x1920, 30 i/s).

    python3 build.py                    -> export/dropshipping_local_9x16.mp4
    python3 build.py --preview 1,5,9    -> cache/preview_*.jpg (planches de contrôle)
    python3 build.py --plan             -> PLAN_DE_MONTAGE.md (tableau phrase | fichier | passage | texte | son)

Minutage : audio/voix_mots.json (mots horodatés de la voix ElevenLabs « Samantha Claude »).
S'il est absent, un minutage estimé est calculé (audio/voix_mots_estime.json) et la vidéo sort sans voix.
Voix : audio/voix_samantha_claude.mp3 (mixée automatiquement si présente).
"""
import os, sys, json, math, re, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
sys.path.insert(0, ROOT)
import plan as P

W, H, FPS = 1080, 1920, 30
os.makedirs("cache", exist_ok=True); os.makedirs("export", exist_ok=True)

YELLOW, WHITE, INK, CREAM = (255, 205, 40), (255, 255, 255), (20, 20, 24), (248, 242, 232)
GREEN = (37, 211, 102)
FD = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(FD + f"InterDisplay-{w}.otf", s)
ANTON = "/home/user/digitalrpofitM/projet_shein_flow/fonts/Anton.woff2"
def anton(s): return ImageFont.truetype(ANTON, s)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3

# ------------------------------------------------------------------ minutage des mots
def tokens(s): return s.split()

ALL_WORDS = [w for p in P.PASSAGES for w in tokens(p[0])]

def estimate_words():
    t, out = 0.25, []
    for w in ALL_WORDS:
        d = 0.06 * len(w.strip(",.?!:")) + 0.1
        out.append({"text": w, "type": "word", "start": round(t, 3), "end": round(t + d, 3)})
        t += d + 0.04
        if w.endswith((".", "?", "!")): t += 0.42
        elif w.endswith((",", ":")): t += 0.2
    return {"words": out, "estime": True}

def load_words():
    if os.path.exists("audio/voix_mots.json"):
        d = json.load(open("audio/voix_mots.json")); ws = [w for w in d["words"] if w.get("type", "word") == "word"]
        if len(ws) != len(ALL_WORDS):
            sys.exit(f"Voix : {len(ws)} mots horodatés pour {len(ALL_WORDS)} mots dans le plan — vérifier le découpage.")
        return ws, False
    d = estimate_words(); json.dump(d, open("audio/voix_mots_estime.json", "w"), ensure_ascii=False, indent=1)
    return d["words"], True

WORDS, ESTIMATED = load_words()
VOICE_END = WORDS[-1]["end"]
TOTAL = round(VOICE_END + P.CTA_HOLD, 2)

# début / fin de chaque passage
PASS_T = []
i = 0
for k, p in enumerate(P.PASSAGES):
    n = len(tokens(p[0]))
    PASS_T.append([WORDS[i]["start"] if k else 0.0, None, i, i + n]); i += n
for k in range(len(PASS_T)):
    PASS_T[k][1] = PASS_T[k + 1][0] if k + 1 < len(PASS_T) else TOTAL

def anchor_time(k, a, lead=0.0):
    """Temps d'un ancrage dans le passage k : None = début, nombre = fraction, texte = mot prononcé."""
    t0, t1, i0, i1 = PASS_T[k]
    if a is None: return t0
    if isinstance(a, (int, float)): return t0 + (t1 - t0) * a
    toks = tokens(P.PASSAGES[k][0])
    j = toks.index(a)                      # le mot doit exister tel quel dans le passage
    return max(t0, WORDS[i0 + j]["start"] - lead)

# plans à l'échelle de la vidéo : chaque image arrive sur son mot
SHOTS = []
vid_offset = {}
for k, (txt, shots, sfx, label) in enumerate(P.PASSAGES):
    starts = [anchor_time(k, sh[1], lead=0.08) for sh in shots]
    for n, (f, anc, crop, mv, tr) in enumerate(shots):
        t = starts[n]; t_end = starts[n + 1] if n + 1 < len(shots) else PASS_T[k][1]
        off = vid_offset.get(f, 0.0)
        if f in P.F and P.F[f].endswith(".mp4"): vid_offset[f] = off + (t_end - t) + 1.0
        SHOTS.append(dict(f=f, t0=t, t1=t_end, crop=crop, mv=mv, tr=tr, off=off, k=k))
# le premier plan d'un passage commence là où finit le précédent (pas de trou)
for n in range(1, len(SHOTS)): SHOTS[n - 1]["t1"] = SHOTS[n]["t0"]

# ------------------------------------------------------------------ sources
@functools.lru_cache(maxsize=None)
def src_image(f):
    im = Image.open(P.M + P.F[f]).convert("RGB")
    for x0, y0, x1, y1 in getattr(P, "BLUR", {}).get(f, []):
        bx = (int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height))
        im.paste(im.crop(bx).filter(ImageFilter.GaussianBlur(14)), bx[:2])
    return im

def vid_meta(path):
    o = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                                 "-show_entries", "format=duration", "-of", "json", path])
    j = json.loads(o); s = j["streams"][0]; return s["width"], s["height"], float(j["format"]["duration"])

class VideoShot:
    """Lit les images d'une vidéo source, dans l'ordre, au format source (pipe ffmpeg)."""
    def __init__(self, f, off):
        self.path = P.M + P.F[f]; self.w, self.h, self.dur = vid_meta(self.path)
        sc = min(1.0, 1400 / max(self.w, self.h)); self.ow, self.oh = int(self.w * sc) // 2 * 2, int(self.h * sc) // 2 * 2
        off = off % max(0.1, self.dur - 3)
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(off), "-stream_loop", "-1", "-i", self.path, "-vf",
                                   f"fps={FPS},scale={self.ow}:{self.oh}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE)
        self.n = -1; self.last = None
    def frame(self, n):
        while self.n < n:
            b = self.p.stdout.read(self.ow * self.oh * 3)
            if len(b) < self.ow * self.oh * 3: break
            self.last = Image.frombytes("RGB", (self.ow, self.oh), b); self.n += 1
        return self.last
    def close(self): self.p.kill()

_open = {}
def shot_source(i, t):
    s = SHOTS[i]
    if P.F.get(s["f"], "").endswith(".mp4"):
        if i not in _open: _open[i] = VideoShot(s["f"], s["off"])
        return _open[i].frame(int((t - s["t0"]) * FPS))
    return src_image(s["f"])

def cover(im, cx, cy, z):
    sw, sh = im.size
    if sw / sh > W / H: rh = sh / z; rw = rh * W / H
    else: rw = sw / z; rh = rw * H / W
    l = clamp(cx * sw - rw / 2, 0, sw - rw); t = clamp(cy * sh - rh / 2, 0, sh - rh)
    return im.transform((W, H), Image.AFFINE, (rw / W, 0, l, 0, rh / H, t), Image.BICUBIC)

def render_shot(i, t):
    s = SHOTS[i]; k = clamp((t - s["t0"]) / max(0.1, s["t1"] - s["t0"]))
    cx, cy, z = s["crop"]; mv = s["mv"]
    if mv == "in": z *= 1 + 0.07 * ease(k)
    elif mv == "out": z *= 1.07 - 0.07 * ease(k)
    elif mv == "gauche": cx -= 0.05 * ease(k); z *= 1.04
    elif mv == "droite": cx += 0.05 * ease(k); z *= 1.04
    im = cover(shot_source(i, t), cx, cy, z)
    return grade(im)

_vig = None
def grade(im):
    """Étalonnage commun : un peu de contraste, légère chaleur, vignette douce."""
    global _vig
    im = ImageEnhance.Contrast(im).enhance(1.06); im = ImageEnhance.Color(im).enhance(1.05)
    if _vig is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2)
        _vig = Image.fromarray((np.clip(1 - 0.32 * d ** 2.2, 0, 1) * 255).astype(np.uint8))
    black = Image.new("RGB", (W, H), (8, 6, 4))
    return Image.composite(im, black, _vig)

# ------------------------------------------------------------------ carton final (CTA)
@functools.lru_cache(maxsize=None)
def cta_bg():
    im = cover(src_image("16"), 0.5, 0.5, 1.0).filter(ImageFilter.GaussianBlur(26))
    return Image.blend(im, Image.new("RGB", (W, H), (14, 12, 10)), 0.55)

def text_c(d, xy, s, f, fill, stroke=0, sfill=INK):
    w = d.textlength(s, font=f); d.text((xy[0] - w / 2, xy[1]), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)

def render_cta(t):
    k0 = SHOTS[-1]["t0"]; im = cta_bg().copy().convert("RGBA"); d = ImageDraw.Draw(im)
    a = ease_out((t - k0) / 0.4)
    # titre
    ft = anton(118)
    text_c(d, (W // 2, 250 - (1 - a) * 30), "ÉCRIS « LOCAL »", ft, YELLOW + (int(255 * a),))
    text_c(d, (W // 2, 390 - (1 - a) * 30), "EN COMMENTAIRE", anton(96), WHITE + (int(255 * a),))
    # zone de commentaires stylisée
    pw, ph = 820, 620; px, py = (W - pw) // 2, 600
    card = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, pw - 1, ph - 1), 44, fill=(250, 250, 250, 255))
    text_c(cd, (pw // 2, 34), "Commentaires", font("Bold", 40), INK)
    cd.line((40, 104, pw - 40, 104), fill=(225, 225, 228), width=3)
    # moment où « LOCAL » est prononcé
    li = next(j for j in range(PASS_T[-1][2], PASS_T[-1][3]) if "LOCAL" in WORDS[j]["text"])
    tl = WORDS[li]["start"]; typed = int(clamp((t - tl) / 0.5) * 5)
    sent = t >= tl + 0.75
    if sent:
        ks = ease_out((t - tl - 0.75) / 0.3)
        cd.ellipse((44, 150, 124, 230), fill=(205, 205, 212))
        cd.text((146, 148), "toi", font=font("SemiBold", 32), fill=(120, 120, 128))
        cd.text((146, 190), "LOCAL", font=font("Black", 64), fill=INK + (int(255 * ks),))
        cd.text((pw - 120, 200), "♥", font=font("Bold", 46), fill=(235, 70, 90, int(255 * ks)))
    # champ de saisie
    cd.rounded_rectangle((36, ph - 140, pw - 36, ph - 40), 50, fill=(238, 238, 241))
    s = "LOCAL"[:typed] if not sent else ""
    cd.text((78, ph - 120), s if s else ("Ajoute un commentaire…" if not sent else "Ajoute un commentaire…"),
            font=font("Bold" if s else "Medium", 50), fill=INK if s else (150, 150, 158))
    if s and int(t * 3) % 2 == 0:
        x = 78 + cd.textlength(s, font=font("Bold", 50)) + 6; cd.rectangle((x, ph - 116, x + 5, ph - 64), fill=(255, 60, 90))
    cd.ellipse((pw - 132, ph - 128, pw - 52, ph - 52), fill=(255, 60, 90) if typed else (220, 220, 225))
    cd.polygon([(pw - 104, ph - 108), (pw - 104, ph - 72), (pw - 72, ph - 90)], fill=WHITE)
    sh = Image.new("RGBA", (pw + 120, ph + 120), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((60, 80, pw + 60, ph + 80), 44, fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(24)), (px - 60, py - 60))
    card.putalpha(card.getchannel("A").point(lambda v: int(v * a)))
    im.alpha_composite(card, (px, py))
    # « Je t'envoie le lien de la chaîne »
    ji = next(j for j in range(PASS_T[-1][2], PASS_T[-1][3]) if WORDS[j]["text"].lower().startswith("je"))
    b = ease_out((t - WORDS[ji]["start"]) / 0.35)
    if b > 0:
        f2 = font("Bold", 50); s2 = "Je t'envoie le lien de la chaîne"
        w2 = d.textlength(s2, font=f2) + 70; y2 = 1300 + (1 - b) * 30
        d.rounded_rectangle(((W - w2) / 2, y2, (W + w2) / 2, y2 + 96), 48, fill=GREEN + (int(255 * b),))
        text_c(d, (W // 2, y2 + 18), s2, f2, WHITE + (int(255 * b),))
    return im.convert("RGB")

# ------------------------------------------------------------------ sous-titres
def norm(w): return re.sub(r"[^\w$]", "", w.lower().replace("’", "'"))

def keyword_marks():
    n = [norm(w["text"]) for w in WORDS]; marks = set()
    for kw in P.KEYWORDS:
        kt = [norm(x) for x in kw.split()]
        for j in range(len(n) - len(kt) + 1):
            if n[j:j + len(kt)] == kt and (kw != "LOCAL" or WORDS[j]["text"].strip(",.") == "LOCAL"):
                marks.update(range(j, j + len(kt)))
    return marks
MARKS = keyword_marks()

def chunks():
    out, cur = [], []
    for j, w in enumerate(WORDS):
        cur.append(j)
        txt = " ".join(WORDS[x]["text"] for x in cur)
        end_p = w["text"].endswith((",", ".", "?", "!", ":"))
        nxt_kw = j + 1 < len(WORDS) and (j + 1) in MARKS and j in MARKS
        if (len(cur) >= 3 or len(txt) >= 17 or end_p) and not nxt_kw:
            out.append(cur); cur = []
    if cur: out.append(cur)
    res = []
    for c, ids in enumerate(out):
        t0 = WORDS[ids[0]]["start"]; t1 = WORDS[out[c + 1][0]]["start"] if c + 1 < len(out) else WORDS[ids[-1]]["end"] + 0.4
        t1 = min(t1, WORDS[ids[-1]]["end"] + 0.6)
        res.append((t0, t1, ids))
    return res
CHUNKS = chunks()

SUB_Y = 1250          # zone centrale basse, au-dessus de la légende TikTok (bas ~20 %)
SUB_CX = 520          # légèrement à gauche : la colonne de boutons TikTok est à droite
def draw_subs(im, t):
    c = next((c for c in CHUNKS if c[0] <= t < c[1]), None)
    if not c or t >= VOICE_END + 0.5: return
    t0, t1, ids = c
    f = font("Black", 76); gap = 20
    words = [WORDS[j]["text"] for j in ids]
    ws = [ImageDraw.Draw(im).textlength(w, font=f) for w in words]
    tot = sum(ws) + gap * (len(ws) - 1)
    if tot > 860:
        f = font("Black", int(76 * 860 / tot)); ws = [ImageDraw.Draw(im).textlength(w, font=f) for w in words]; tot = sum(ws) + gap * (len(ws) - 1)
    k = ease_out((t - t0) / 0.12); sc = 0.9 + 0.1 * k
    layer = Image.new("RGBA", (int(tot) + 60, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(layer); x = 30
    for j, w, wd in zip(ids, words, ws):
        col = YELLOW if j in MARKS else WHITE
        d.text((x, 20), w, font=f, fill=col, stroke_width=7, stroke_fill=(10, 10, 12))
        x += wd + gap
    if sc != 1: layer = layer.resize((int(layer.width * sc), int(layer.height * sc)), Image.BICUBIC)
    im.paste(layer, (int(SUB_CX - layer.width / 2), int(SUB_Y - layer.height / 2)), layer)

# ------------------------------------------------------------------ textes à l'écran
def label_at(t):
    for k, p in enumerate(P.PASSAGES):
        if p[3]:
            t1 = PASS_T[k][1]; s = anchor_time(k, p[3][1])
            if s <= t < t1: return p[3][0], s, t1
    return None

def draw_label(im, t):
    L = label_at(t)
    if not L: return
    s, t0, t1 = L; a = ease_out((t - t0) / 0.25) * clamp((t1 - t) / 0.2)
    if a <= 0: return
    d = ImageDraw.Draw(im, "RGBA")
    if s == "CALCUL": return draw_budget(im, t, t0, a)
    big = s in ("2023-2024", "2026", "50 $")
    sz = 190 if big else 92
    while d.textlength(s, font=anton(sz)) > 900: sz -= 4
    f = anton(sz)
    w = d.textlength(s, font=f); y = 420 - (1 - a) * 24
    if big:
        col = (210, 205, 195) if s == "2023-2024" else YELLOW
        d.text(((W - w) / 2, y), s, font=f, fill=col + (int(255 * a),), stroke_width=8, stroke_fill=(10, 10, 12, int(230 * a)))
    else:
        pad = 40; d.rounded_rectangle(((W - w) / 2 - pad, y - 8, (W + w) / 2 + pad, y + 132), 30, fill=CREAM + (int(240 * a),))
        d.text(((W - w) / 2, y + 2), s, font=f, fill=INK + (int(255 * a),))

def draw_budget(im, t, t0, a):
    """Carnet de budget : les postes cités dans la phrase, sans chiffres inventés."""
    d = ImageDraw.Draw(im, "RGBA"); x0, y0, w, h = 150, 300, 640, 560
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 28, fill=CREAM + (int(244 * a),))
    for yy in range(y0 + 120, y0 + h - 20, 92): d.line((x0 + 40, yy, x0 + w - 40, yy), fill=(200, 190, 175, int(255 * a)), width=2)
    d.text((x0 + 44, y0 + 34), "Ma marge", font=anton(70), fill=INK + (int(255 * a),))
    rows = ["Prix d'achat", "Livraison", "Communication", "Prix de vente"]
    for r, s in enumerate(rows):
        b = clamp((t - t0 - 0.35 - 0.45 * r) / 0.25) * a
        if b <= 0: continue
        y = y0 + 140 + r * 92
        d.text((x0 + 60, y), ("✓ " if r < 3 else "→ ") + s, font=font("Bold", 46), fill=(INK if r < 3 else (190, 120, 0)) + (int(255 * b),))

# ------------------------------------------------------------------ image finale
def shot_index(t):
    for i, s in enumerate(SHOTS):
        if s["t0"] <= t < s["t1"]: return i
    return len(SHOTS) - 1

# ------------------------------------------------------------------ tableau de bord Chariow (capture réelle)
DASH_CROP = (0, 226, 2000, 900)            # sans la barre du navigateur ni le bandeau jaune
DASH_TARGET = (352, 384, 1000, 674)        # zone du « Revenu total » (dans la capture recadrée)
DASH_HL = (455, 500, 728, 575)             # « 1088000 CDF » à encadrer

@functools.lru_cache(maxsize=None)
def dash_src(): return Image.open(P.M + P.F["35"]).convert("RGB").crop(DASH_CROP)

@functools.lru_cache(maxsize=None)
def dash_bg():
    im = cover(Image.open(P.M + P.F["35"]).convert("RGB"), 0.5, 0.55, 1.0).filter(ImageFilter.GaussianBlur(30))
    return Image.blend(im, Image.new("RGB", (W, H), (12, 12, 16)), 0.62)

def render_dash(i, t):
    s = SHOTS[i]; src = dash_src(); sw, sh = src.size
    k = ease((t - s["t0"] - 0.35) / 1.1)                          # plan large, puis rapprochement
    full = (0, 0, sw, sh); tg = DASH_TARGET
    v = [full[j] + (tg[j] - full[j]) * k for j in range(4)]
    dw = 1000; dh = int(dw * (v[3] - v[1]) / (v[2] - v[0]))
    view = src.crop(tuple(int(x) for x in v)).resize((dw, dh), Image.LANCZOS)
    im = dash_bg().copy(); x0 = (W - dw) // 2; y0 = 760 - dh // 2
    sh_ = Image.new("RGBA", (dw + 120, dh + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh_).rounded_rectangle((60, 76, dw + 60, dh + 76), 28, fill=(0, 0, 0, 140))
    im.paste(sh_.filter(ImageFilter.GaussianBlur(22)), (x0 - 60, y0 - 60), sh_.filter(ImageFilter.GaussianBlur(22)))
    m = Image.new("L", (dw, dh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, dw - 1, dh - 1), 28, fill=255)
    im.paste(view, (x0, y0), m)
    if k > 0.95:                                                  # cadre jaune qui clignote sur le revenu
        sx = dw / (v[2] - v[0]); sy = dh / (v[3] - v[1])
        hx0 = x0 + (DASH_HL[0] - v[0]) * sx; hy0 = y0 + (DASH_HL[1] - v[1]) * sy
        hx1 = x0 + (DASH_HL[2] - v[0]) * sx; hy1 = y0 + (DASH_HL[3] - v[1]) * sy
        a = 0.6 + 0.4 * abs(math.sin((t - s["t0"]) * 6))
        ImageDraw.Draw(im, "RGBA").rounded_rectangle((hx0 - 14, hy0 - 12, hx1 + 14, hy1 + 12), 18, outline=YELLOW + (int(255 * a),), width=9)
    return im

def base_frame(i, t):
    f = SHOTS[i]["f"]
    if f == "CTA": return render_cta(t)
    if f == "DASH": return render_dash(i, t)
    return render_shot(i, t)

def frame(t):
    i = shot_index(t); s = SHOTS[i]; im = base_frame(i, t)
    dt = t - s["t0"]
    if i > 0 and s["tr"] == "fondu" and dt < 0.22:
        im = Image.blend(base_frame(i - 1, s["t0"] - 0.01), im, ease(dt / 0.22))
    elif i > 0 and s["tr"] == "balayage" and dt < 0.26:
        k = ease_out(dt / 0.26); prev = base_frame(i - 1, s["t0"] - 0.01)
        c = Image.new("RGB", (W, H)); c.paste(prev, (int(-W * k), 0)); c.paste(im, (int(W * (1 - k)), 0))
        im = c.filter(ImageFilter.BoxBlur(6 * (1 - abs(2 * k - 1))))
    for j in list(_open):
        if j < i - 1: _open.pop(j).close()
    if s["f"] != "CTA":
        draw_label(im, t); draw_subs(im, t)
    if t > TOTAL - 0.4: im = Image.blend(im, Image.new("RGB", (W, H)), 0.0)
    return im

# ------------------------------------------------------------------ son
MUSIC = "audio/music/music_motivating_mornings.mp3"
VOICE = "audio/voix_samantha_claude.mp3"

def sfx_events():
    ev = []
    for k, p in enumerate(P.PASSAGES):
        for (r, f, g) in p[2]: ev.append((anchor_time(k, r), f, g))
    return ev

def music_volume_expr():
    """Musique calme au début, plus présente pendant les étapes pratiques, puis baisse avant le CTA."""
    a = PASS_T[25][0]; b = PASS_T[30][0]; c = PASS_T[-1][0]
    base = 0.16 if os.path.exists(VOICE) else 0.42
    return (f"{base}*(1+0.35*between(t,{a},{b})-0.45*gte(t,{c - 1.0})*min(1,(t-{c - 1.0})/1.0))")

def build_audio(out="cache/mix.wav"):
    inp = ["-stream_loop", "1", "-i", MUSIC]
    fc = [f"[0:a]aresample=48000,atrim=0:{TOTAL},volume='{music_volume_expr()}':eval=frame,afade=t=in:d=0.4,afade=t=out:st={TOTAL - 1.2}:d=1.2[m]"]
    lab = ["[m]"]
    for n, (t, f, g) in enumerate(sfx_events()):
        rev = f.endswith("_inverse"); f = f.replace("_inverse", "")
        inp += ["-i", f"audio/sfx/{f}.mp3"]
        fx = "areverse," if rev else ""
        fc.append(f"[{n + 1}:a]aresample=48000,aformat=channel_layouts=stereo,{fx}atrim=0:1.6,afade=t=out:st=1.1:d=0.5,volume={g}dB,adelay={int(t * 1000)}|{int(t * 1000)}[s{n}]")
        lab.append(f"[s{n}]")
    if os.path.exists(VOICE):
        j = len(sfx_events()) + 1; inp += ["-i", VOICE]
        fc.append(f"[{j}:a]aresample=48000,aformat=channel_layouts=stereo,volume=1.0[v]"); lab.append("[v]")
    fc.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0:duration=first,alimiter=limit=0.85:level=false[o]")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", ";".join(fc), "-map", "[o]", "-t", str(TOTAL), "-ac", "2", out])
    return out

def render(out="export/dropshipping_local_9x16.mp4"):
    mix = build_audio()
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", mix, "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
    for n in range(round(TOTAL * FPS)):
        p.stdin.write(frame(n / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK ->", out, f"({TOTAL:.1f} s{', minutage estimé, sans voix' if ESTIMATED else ''})")

# ------------------------------------------------------------------ plan de montage (tableau)
SFX_FR = {"papier_froisse_billets": "froissement de papier (billets)", "notification_message_pop": "notification", "page_tournee": "page tournée",
          "frappe_clavier_lente": "frappe clavier", "fermeture_objectif": "fermeture légère", "mise_au_point": "mise au point",
          "appareil_photo": "déclic d'appareil photo", "papier_tranche_ruban": "papier tranché (ruban)", "grande_page_carton": "fermeture carton (papier)",
          "touches_calculatrice": "touches de calculatrice", "crayon_ecriture": "stylo", "bulle_message_envoye": "message envoyé",
          "validation_douce": "validation douce", "clics_souris": "petit clic", "clavier_telephone": "frappe sur téléphone",
          "whoosh_air": "whoosh doux", "whoosh_fast": "whoosh court", "whoosh_fast_inverse": "whoosh inversé (rembobinage)"}
TR_FR = {"cut": "coupe franche", "fondu": "fondu court", "balayage": "balayage"}

def write_plan():
    rows = ["| Phrase prononcée | Fichier exact (Drive) | Passage | Texte à l'écran | Son et transition |", "|---|---|---|---|---|"]
    for k, (txt, shots, sfx, label) in enumerate(P.PASSAGES):
        t0, t1 = PASS_T[k][:2]
        files = " → ".join(("capture du tableau de bord Chariow (`" + P.F["35"] + "`), rapprochement sur le revenu total") if s[0] == "DASH" else ("carton final (zone de commentaires stylisée, fond flou de « " + P.F["16"] + " »)") if s[0] == "CTA" else f"`{P.F[s[0]]}`" for s in shots)
        lab = {"CALCUL": "Carnet « Ma marge » : prix d'achat, livraison, communication, prix de vente"}.get(label[0], label[0]) if label else "—"
        if k == len(P.PASSAGES) - 1: lab = "ÉCRIS « LOCAL » EN COMMENTAIRE / Je t'envoie le lien de la chaîne"
        snd = ", ".join(SFX_FR.get(f, f) for _, f, _ in sfx) or "musique seule"
        trs = ", ".join(TR_FR[s[4]] for s in shots)
        rows.append(f"| {txt} | {files} | {t0:.1f}–{t1:.1f} s | {lab} | {snd} ; {trs} |")
    hdr = ("# Plan de montage — Dropshipping local\n\n"
           + ("> Minutage **estimé** (la voix ElevenLabs n'a pas encore pu être générée) : il sera recalculé automatiquement "
              "sur la vraie voix.\n\n" if ESTIMATED else "") + f"Durée : {TOTAL:.1f} s.\n\n")
    open("PLAN_DE_MONTAGE.md", "w").write(hdr + "\n".join(rows) + "\n")
    print("PLAN_DE_MONTAGE.md écrit")

if __name__ == "__main__":
    if "--plan" in sys.argv: write_plan()
    elif "--preview" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1].split(",")]
        ims = [frame(t).resize((360, 640)) for t in ts]
        for j in range(0, len(ims), 6):
            g = Image.new("RGB", (360 * 6, 640), "white")
            for i, im in enumerate(ims[j:j + 6]): g.paste(im, (i * 360, 0))
            g.save(f"cache/preview_{j // 6}.jpg", quality=85)
        print("ok", TOTAL)
    else: render()
