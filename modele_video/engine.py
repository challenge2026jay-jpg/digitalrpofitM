"""Moteur de rendu motion design (style « interface émeraude » de la vidéo de référence).
Tout est dessiné en Python (Pillow + NumPy) puis encodé par ffmpeg.
"""
import os, math, subprocess, json, re, unicodedata
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1920, 1080, 30

# ---------------------------------------------------------------- couleurs
MINT = (47, 208, 138)
RED = (224, 90, 79)
WHITE = (255, 255, 255)
CREAM = (241, 239, 234)
INK = (24, 30, 27)
CARD = (26, 36, 32)
CARD2 = (32, 46, 40)
MUTED = (150, 170, 160)
GREY = (120, 128, 124)

def rgba(c, a=255):
    return (c[0], c[1], c[2], a)

# ---------------------------------------------------------------- polices
FONTS = {
    "bold": "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    "xbold": "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
    "semi": "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
    "med": "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
    "serif_i": os.path.join(HERE, "fonts/PlayfairDisplay-Italic.ttf"),
    "serif": os.path.join(HERE, "fonts/PlayfairDisplay.ttf"),
    "mono": os.path.join(HERE, "fonts/IBMPlexMono-Medium.ttf"),
}

@lru_cache(None)
def F(name, size):
    f = ImageFont.truetype(FONTS[name], int(size))
    if name == "serif_i":
        try: f.set_variation_by_name("Medium Italic")
        except Exception: pass
    return f

# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(p): return 1 - (1 - p) ** 3
def ease_in_out(p): return 3 * p * p - 2 * p * p * p
def ease_back(p, s=1.7):
    p -= 1
    return p * p * ((s + 1) * p + s) + 1

# ---------------------------------------------------------------- fonds
def _radial(cx, cy, rx, ry):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    return np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)

@lru_cache(None)
def background(kind):
    rng = np.random.default_rng(7)
    if kind == "dark":
        d = np.clip(_radial(W / 2, H * 0.42, W * 0.62, H * 0.75), 0, 1.4)
        c0, c1 = np.array([14, 59, 44], np.float32), np.array([5, 13, 10], np.float32)
        k = np.clip(d, 0, 1)[..., None] ** 1.2
        img = c0 * (1 - k) + c1 * k
        img *= (1 - 0.35 * np.clip(d - 0.9, 0, 1))[..., None]
    elif kind == "grid":
        base = np.array([15, 90, 64], np.float32)
        img = np.ones((H, W, 3), np.float32) * base
        g = np.zeros((H, W), np.float32)
        step = 60
        g[:, ::step] = 1; g[::step, :] = 1
        g[:, ::step * 4] = 1.8; g[::step * 4, :] = 1.8
        img += g[..., None] * 0.10 * (255 - base)
        d = np.clip(_radial(W / 2, H / 2, W * 0.75, H * 0.85), 0, 1.3)
        img *= (1 - 0.40 * np.clip(d - 0.55, 0, 1))[..., None]
    elif kind == "cream":
        img = np.ones((H, W, 3), np.float32) * np.array(CREAM, np.float32)
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        curve = H * 0.80 - H * 0.55 * np.exp(-((x - W * 0.62) / (W * 0.22)) ** 2)
        band = np.exp(-((y - curve) / 120) ** 2)
        below = (y > curve).astype(np.float32) * 0.5
        img -= (band * 10 + below * 5)[..., None]
        d = np.clip(_radial(W / 2, H / 2, W * 0.8, H * 0.9), 0, 1.3)
        img *= (1 - 0.10 * np.clip(d - 0.6, 0, 1))[..., None]
    elif kind == "black":
        d = np.clip(_radial(W / 2, H / 2, W * 0.7, H * 0.8), 0, 1.3)
        img = np.ones((H, W, 3), np.float32) * np.array([9, 14, 12], np.float32)
        img *= (1 - 0.6 * np.clip(d - 0.4, 0, 1))[..., None]
    else:
        raise ValueError(kind)
    img += rng.normal(0, 2.2, (H, W, 1)).astype(np.float32)   # grain fixe
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")

# ---------------------------------------------------------------- primitives
def text_size(txt, font):
    b = font.getbbox(txt)
    return b[2] - b[0], b[3] - b[1]

def rich(runs, gap=0, align_base=True):
    """runs = [(texte, police, taille, couleur)] sur une ligne, alignés sur la ligne de base."""
    parts = []
    for txt, fn, sz, col in runs:
        f = F(fn, sz)
        asc, desc = f.getmetrics()
        wid = int(f.getlength(txt))
        parts.append((txt, f, col, asc, desc, wid))
    A = max(p[3] for p in parts); D = max(p[4] for p in parts)
    total = sum(p[5] for p in parts) + gap * (len(parts) - 1) + 8
    im = Image.new("RGBA", (max(1, total), A + D + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 4
    for txt, f, col, asc, desc, wid in parts:
        d.text((x, 4 + A - asc), txt, font=f, fill=rgba(col) if len(col) == 3 else col)
        x += wid + gap
    return im

def stack(images, spacing=10, align="center"):
    w = max(i.width for i in images); h = sum(i.height for i in images) + spacing * (len(images) - 1)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0)); y = 0
    for i in images:
        x = (w - i.width) // 2 if align == "center" else (0 if align == "left" else w - i.width)
        out.alpha_composite(i, (x, y)); y += i.height + spacing
    return out

def hstack(images, spacing=10):
    h = max(i.height for i in images); w = sum(i.width for i in images) + spacing * (len(images) - 1)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0)); x = 0
    for i in images:
        out.alpha_composite(i, (x, (h - i.height) // 2)); x += i.width + spacing
    return out

def shadowed(im, radius=28, offset=(0, 14), opacity=110):
    pad = radius * 2
    out = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    a = im.getchannel("A").point(lambda v: v * opacity // 255)
    blk = Image.new("RGBA", im.size, (0, 0, 0, 255)); blk.putalpha(a)
    sh.alpha_composite(blk, (pad + offset[0], pad + offset[1]))
    sh = sh.filter(ImageFilter.GaussianBlur(radius / 2))
    out.alpha_composite(sh); out.alpha_composite(im, (pad, pad))
    return out

def rounded(w, h, fill, r=18, outline=None, width=2):
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill, outline=outline, width=width)
    return im

def card(w, h, light=False, r=18):
    if light:
        c = rounded(w, h, rgba(WHITE), r, outline=(225, 225, 220, 255), width=2)
    else:
        c = rounded(w, h, (26, 36, 32, 240), r, outline=(60, 80, 70, 255), width=2)
    return c

def pill(txt, bg=(255, 255, 255, 255), fg=INK, size=30, fn="semi", pad=(22, 12), icon=None, r=None):
    t = rich([(txt, fn, size, fg)])
    iw = 0
    if icon is not None: iw = icon.width + 10
    w = t.width + pad[0] * 2 + iw; h = t.height + pad[1] * 2
    im = rounded(w, h, bg, r if r is not None else h // 2)
    x = pad[0]
    if icon is not None:
        im.alpha_composite(icon, (x, (h - icon.height) // 2)); x += iw
    im.alpha_composite(t, (x, pad[1]))
    return im

def check_box(size=34, on=True, col=MINT):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if on:
        d.rounded_rectangle((0, 0, size - 1, size - 1), size // 4, fill=rgba(col))
        s = size
        d.line([(s * .25, s * .52), (s * .43, s * .70), (s * .76, s * .32)], fill=WHITE, width=max(3, s // 9), joint="curve")
    else:
        d.rounded_rectangle((1, 1, size - 2, size - 2), size // 4, outline=(170, 180, 175, 255), width=3)
    return im

def cross_mark(size=34, col=RED):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, size - 1, size - 1), size // 4, fill=rgba(col))
    s = size; w = max(3, s // 9)
    d.line([(s * .3, s * .3), (s * .7, s * .7)], fill=WHITE, width=w); d.line([(s * .7, s * .3), (s * .3, s * .7)], fill=WHITE, width=w)
    return im

def stamp(txt, col=MINT, size=64, angle=-6):
    t = rich([(txt, "xbold", size, col)])
    pad = 22
    im = Image.new("RGBA", (t.width + pad * 2, t.height + pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((3, 3, im.width - 4, im.height - 4), 10, outline=rgba(col), width=6, fill=(col[0], col[1], col[2], 28))
    im.alpha_composite(t, (pad, pad // 2 - 2))
    # texture « encre »
    rng = np.random.default_rng(len(txt))
    a = np.array(im.getchannel("A"), np.float32)
    a *= (rng.random(a.shape) > 0.06)
    im.putalpha(Image.fromarray(a.astype(np.uint8)))
    return im.rotate(angle, resample=Image.BICUBIC, expand=True)

def label_card(label, value_runs, w=760, h=None, sub=None, light=False, extra=None):
    """Carte d'interface : petit label mono en capitales + grande valeur (comme « TON BUDGET / 95 % »)."""
    lab = rich([(label.upper(), "mono", 26, MINT if not light else (60, 140, 100))], gap=0)
    val = rich(value_runs)
    parts_h = 40 + lab.height + 18 + val.height + 40
    if sub is not None: parts_h += sub.height + 20
    if extra is not None: parts_h += extra.height + 20
    h = h or parts_h
    c = card(w, h, light)
    y = 40
    c.alpha_composite(lab, (44, y)); y += lab.height + 18
    c.alpha_composite(val, (40, y)); y += val.height + 20
    if sub is not None: c.alpha_composite(sub, (44, y)); y += sub.height + 20
    if extra is not None: c.alpha_composite(extra, (44, y))
    return shadowed(c)

def checklist_card(title, items, checked, w=760, light=True, title_col=None, size=34, marks=None):
    """items : textes ; checked : nombre de cases cochées (peut être float pour l'animation) ;
    marks : liste optionnelle de 'ok' / 'x' / None."""
    lab = rich([(title.upper(), "mono", 24, title_col or ((40, 130, 90) if light else MINT))])
    rows = []
    for i, it in enumerate(items):
        m = (marks[i] if marks else "ok")
        on = i < checked
        box = (check_box(size + 4, True) if m == "ok" else cross_mark(size + 4)) if on else check_box(size + 4, False)
        tx = rich([(it, "semi", size, INK if light else WHITE)])
        rows.append(hstack([box, tx], 18))
    lst = stack(rows, 18, "left")
    h = 44 + lab.height + 26 + lst.height + 44
    c = card(w, h, light)
    c.alpha_composite(lab, (44, 44)); c.alpha_composite(lst, (44, 44 + lab.height + 26))
    return shadowed(c)

def icon_tile(img, size=220, light=True, r=36, pad=24):
    """Carte blanche arrondie avec une icône du Drive à l'intérieur (taille modeste, jamais plein cadre)."""
    c = rounded(size, size, rgba(WHITE) if light else (26, 36, 32, 255), r, outline=(225, 225, 220, 255) if light else (60, 80, 70, 255), width=2)
    im = img.copy(); im.thumbnail((size - pad * 2, size - pad * 2), Image.LANCZOS)
    c.alpha_composite(im.convert("RGBA"), ((size - im.width) // 2, (size - im.height) // 2))
    return c

def framed(img, w, r=26, border=(60, 80, 70, 255)):
    im = img.convert("RGBA").copy()
    h = int(im.height * w / im.width)
    im = im.resize((int(w), h), Image.LANCZOS)
    mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    im.putalpha(ImageChops.multiply(im.getchannel("A"), mask))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, outline=border, width=3)
    return im

# ---------------------------------------------------------------- médias du Drive
DRIVE = os.path.join(HERE, "drive")
def drive_path(code):
    for f in os.listdir(DRIVE):
        if f.startswith(code + " - "): return os.path.join(DRIVE, f)
    raise FileNotFoundError(code)

@lru_cache(None)
def drive_image(code):
    return Image.open(drive_path(code)).convert("RGBA")

@lru_cache(None)
def drive_video(code, maxw, maxh, t0=0.0, t1=None, fps=30):
    """Décode une animation du Drive en liste d'images RGBA (redimensionnées, jamais agrandies au-delà de 2x)."""
    p = drive_path(code)
    pr = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", p]))
    sw, sh = pr["streams"][0]["width"], pr["streams"][0]["height"]
    sc = min(maxw / sw, maxh / sh, 2.0)
    w, h = int(sw * sc) // 2 * 2, int(sh * sc) // 2 * 2
    cmd = ["ffmpeg", "-v", "error", "-ss", str(t0), "-i", p]
    if t1: cmd += ["-t", str(t1 - t0)]
    cmd += ["-vf", f"fps={fps},scale={w}:{h}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "rgba", "-"]
    raw = subprocess.check_output(cmd)
    n = len(raw) // (w * h * 4)
    arr = np.frombuffer(raw, np.uint8)[: n * w * h * 4].reshape(n, h, w, 4)
    return [Image.fromarray(a.copy()) for a in arr]

# ---------------------------------------------------------------- éléments animés
class El:
    """Un élément posé sur l'écran. img : Image ou fonction(t_local)->Image.
    anim : pop | up | down | left | right | fade | stamp | none | zoom (ken burns)."""
    def __init__(self, img, x, y, t0, t1=None, anim="pop", dur=0.35, sfx=None, gain=0, out=False, kb=None, anchor="c", z=0):
        self.img, self.x, self.y, self.t0, self.t1 = img, x, y, t0, t1
        self.anim, self.dur, self.sfx, self.gain, self.out, self.kb, self.anchor, self.z = anim, dur, sfx, gain, out, kb, anchor, z

    def get(self, t):
        return self.img(t - self.t0) if callable(self.img) else self.img

def _apply_alpha(im, a):
    if a >= 0.999: return im
    im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    return im

def paste(frame, im, x, y):
    """alpha_composite avec rognage (x, y = coin haut gauche, peut être négatif)."""
    x, y = int(round(x)), int(round(y))
    if x >= W or y >= H or x + im.width <= 0 or y + im.height <= 0: return
    cx0, cy0 = max(0, -x), max(0, -y)
    cx1, cy1 = min(im.width, W - x), min(im.height, H - y)
    if (cx0, cy0, cx1, cy1) != (0, 0, im.width, im.height):
        im = im.crop((cx0, cy0, cx1, cy1))
    frame.alpha_composite(im, (x + cx0, y + cy0))

def draw_el(frame, el, t):
    if t < el.t0 or (el.t1 is not None and t >= el.t1): return
    im = el.get(t)
    if im is None: return
    p = clamp((t - el.t0) / el.dur) if el.dur > 0 else 1.0
    s, dx, dy, a = 1.0, 0, 0, 1.0
    A = el.anim
    if A == "pop":
        s = 0.82 + 0.18 * ease_back(p); a = clamp(p * 2.2)
    elif A == "up":
        dy = 50 * (1 - ease_out(p)); a = clamp(p * 1.8)
    elif A == "down":
        dy = -50 * (1 - ease_out(p)); a = clamp(p * 1.8)
    elif A == "left":
        dx = -140 * (1 - ease_out(p)); a = clamp(p * 1.8)
    elif A == "right":
        dx = 140 * (1 - ease_out(p)); a = clamp(p * 1.8)
    elif A == "fade":
        a = ease_in_out(p)
    elif A == "stamp":
        s = 1.0 + 0.9 * (1 - ease_back(p, 2.2)) if p < 1 else 1.0; a = clamp(p * 3)
    if el.kb:                       # zoom lent continu (ken burns) 100 -> kb
        life = (el.t1 - el.t0) if el.t1 else 8.0
        s *= 1.0 + (el.kb - 1.0) * clamp((t - el.t0) / life)
    if el.out and el.t1 is not None:
        q = clamp((el.t1 - t) / 0.25); a *= q
    if abs(s - 1.0) > 1e-3:
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
    im = _apply_alpha(im, a)
    if el.anchor == "c":
        x, y = el.x - im.width / 2 + dx, el.y - im.height / 2 + dy
    elif el.anchor == "l":
        x, y = el.x + dx, el.y - im.height / 2 + dy
    elif el.anchor == "r":
        x, y = el.x - im.width + dx, el.y - im.height / 2 + dy
    else:
        x, y = el.x + dx, el.y + dy
    paste(frame, im, x, y)

# ---------------------------------------------------------------- curseur
@lru_cache(None)
def cursor_img():
    s = 3
    im = Image.new("RGBA", (40 * s, 56 * s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(2, 2), (2, 42), (12, 32), (19, 49), (26, 46), (19, 30), (33, 30)]
    pts = [(x * s, y * s) for x, y in pts]
    d.polygon(pts, fill=WHITE, outline=(20, 20, 20, 255)); d.line(pts + [pts[0]], fill=(20, 20, 20, 255), width=2 * s)
    im = im.resize((40, 56), Image.LANCZOS)
    return shadowed(im, 8, (2, 4), 120)

class Cursor:
    """Curseur de souris : keys = [(t, x, y)], clicks = [t]."""
    def __init__(self, keys, clicks, t1):
        self.keys, self.clicks, self.t0, self.t1 = keys, clicks, keys[0][0], t1
        self.z = 10; self.sfx = None

    def pos(self, t):
        k = self.keys
        if t <= k[0][0]: return k[0][1:]
        for (ta, xa, ya), (tb, xb, yb) in zip(k, k[1:]):
            if ta <= t <= tb:
                p = ease_in_out((t - ta) / max(1e-3, tb - ta)); return xa + (xb - xa) * p, ya + (yb - ya) * p
        return k[-1][1:]

def draw_cursor(frame, c, t):
    if t < c.t0 or t >= c.t1: return
    x, y = c.pos(t)
    for tc in c.clicks:
        if 0 <= t - tc < 0.45:
            p = (t - tc) / 0.45; r = 12 + 34 * ease_out(p)
            ov = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
            ImageDraw.Draw(ov).ellipse((60 - r, 60 - r, 60 + r, 60 + r), outline=(255, 255, 255, int(220 * (1 - p))), width=4)
            paste(frame, ov, x - 60, y - 60)
    im = cursor_img()
    pressed = any(0 <= t - tc < 0.12 for tc in c.clicks)
    if pressed: im = im.resize((int(im.width * .9), int(im.height * .9)))
    paste(frame, im, x - 18, y - 16)

# ---------------------------------------------------------------- texte normalisé (recherche des mots)
def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9$ ]+", " ", s.replace("’", "'").replace("'", " ")).split()
