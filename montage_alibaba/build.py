#!/usr/bin/env python3
"""Rendu du TikTok « Commander sur Alibaba » à partir de plan.py.

Usage :  python3 build.py [--preview t1,t2,...] [--from T --to T]
  - sans option : rend export/alibaba_tiktok.mp4 (1080x1920, 30 fps)
  - --preview  : écrit des PNG de contrôle dans cache/preview_<t>.png

Dépendances : Python 3 + Pillow + numpy, ffmpeg (avec libass).
Les vidéos sources du Drive doivent être dans media/ sous leur nom d'origine.
"""
import json, math, os, subprocess, sys, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import plan

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
W, H, FPS = 1080, 1920, 30
CACHE = "cache"; os.makedirs(CACHE, exist_ok=True)

FONT_DIR = "/usr/share/fonts/opentype/inter/"
def font(weight, size):
    return ImageFont.truetype(FONT_DIR + {"black": "InterDisplay-Black.otf", "xbold": "InterDisplay-ExtraBold.otf",
                                          "bold": "InterDisplay-Bold.otf", "semi": "InterDisplay-SemiBold.otf",
                                          "med": "InterDisplay-Medium.otf"}[weight], size)

YELLOW = (255, 214, 10)
CREAM = (246, 238, 228)
INK = (24, 24, 27)

# ---------------------------------------------------------------- helpers
def smooth(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)

def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3

def lerp(a, b, k):
    return a + (b - a) * k

def lerp_t(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))

def rounded_mask(size, r):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255)
    return m

def shadow(size, r, blur=28, alpha=110, pad=60):
    s = Image.new("RGBA", (size[0] + 2 * pad, size[1] + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle((pad, pad + 14, pad + size[0], pad + size[1] + 14), r, fill=(0, 0, 0, alpha))
    return s.filter(ImageFilter.GaussianBlur(blur)), pad

@functools.lru_cache(maxsize=None)
def load_image(path):
    return Image.open(path).convert("RGB")

def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height", "-of", "csv=p=0", path]).decode().split(",")
    return int(out[0]), int(out[1])

def video_frames(path, ss, speed, n):
    """Décode n images à 30 fps depuis ss (vitesse `speed`), réduites pour le cadrage."""
    w, h = probe(path)
    scale = "scale=-2:1920" if (w > h and h > 1300) else "null"
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", path, "-vf",
           f"setpts=(PTS-STARTPTS)/{speed},fps={FPS},{scale}", "-frames:v", str(n + 2),
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    ow, oh = (round(w * 1920 / h / 2) * 2, 1920) if scale != "null" else (w, h)
    last = None
    for _ in range(n):
        buf = p.stdout.read(ow * oh * 3)
        if len(buf) == ow * oh * 3:
            last = Image.frombuffer("RGB", (ow, oh), buf, "raw", "RGB", 0, 1)
        yield last
    p.stdout.close(); p.wait()

# ---------------------------------------------------------------- framing
def fill_frame(img, c, z):
    sw, sh = img.size
    if sw / sh > W / H:
        bh, bw = sh, sh * W / H
    else:
        bw, bh = sw, sw * H / W
    rw, rh = bw / z, bh / z
    left = min(max(c[0] * sw - rw / 2, 0), sw - rw)
    top = min(max(c[1] * sh - rh / 2, 0), sh - rh)
    return img.transform((W, H), Image.AFFINE, (rw / W, 0, left, 0, rh / H, top), Image.BICUBIC)

def blur_bg(img, dark=0.55):
    small = fill_frame(img, (0.5, 0.5), 1.0).resize((W // 6, H // 6), Image.BILINEAR)
    small = small.filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BICUBIC)
    return Image.eval(small, lambda v: int(v * dark))

def fit_frame(img, box, fw=1000, fy=None, hl=None, k=0.0):
    sw, sh = img.size
    frame = blur_bg(img, 0.45)
    x0, y0, x1, y1 = box[0] * sw, box[1] * sh, box[2] * sw, box[3] * sh
    bw, bh = x1 - x0, y1 - y0
    fh = int(fw * bh / bw)
    if fh > 1250:  # garde la carte dans la zone utile
        fh = 1250; fw2 = int(fh * bw / bh)
    else:
        fw2 = fw
    fg = img.transform((fw2, fh), Image.AFFINE, (bw / fw2, 0, x0, 0, bh / fh, y0), Image.BICUBIC)
    if hl:
        d = ImageDraw.Draw(fg)
        hx0 = (hl[0] - x0) * fw2 / bw; hy0 = (hl[1] - y0) * fh / bh
        hx1 = (hl[2] - x0) * fw2 / bw; hy1 = (hl[3] - y0) * fh / bh
        a = smooth(k * 4)
        pad = 8
        d.rounded_rectangle((hx0 - pad, hy0 - pad, hx1 + pad, hy1 + pad), 14, outline=YELLOW + (255,), width=max(1, int(7 * a)))
    r = 34
    sh_img, pad = shadow((fw2, fh), r)
    cx, cy = W // 2, fy if fy else 830
    frame.paste(sh_img, (cx - fw2 // 2 - pad, cy - fh // 2 - pad), sh_img)
    frame.paste(fg, (cx - fw2 // 2, cy - fh // 2), rounded_mask((fw2, fh), r))
    return frame

def logo_frame(img, z, green=False):
    bg = Image.new("RGB", (W, H), CREAM)
    # léger dégradé radial
    grad = Image.radial_gradient("L").resize((W * 2, H * 2)).crop((W // 2, H // 2 - 200, W // 2 + W, H // 2 - 200 + H))
    bg = Image.composite(bg, Image.new("RGB", (W, H), (232, 220, 206)), Image.eval(grad, lambda v: 255 - v // 2))
    size = int(560 * z)
    lg = img.resize((size, size), Image.LANCZOS)
    r = int(size * 0.2)
    sh_img, pad = shadow((size, size), r, blur=36, alpha=90)
    cy = 820
    bg.paste(sh_img, (W // 2 - size // 2 - pad, cy - size // 2 - pad), sh_img)
    bg.paste(lg, (W // 2 - size // 2, cy - size // 2), rounded_mask((size, size), r))
    return bg

# ---------------------------------------------------------------- overlays
def text_w(f, s):
    return f.getbbox(s)[2] - f.getbbox(s)[0]

def card(w, h, r=36, fill=(255, 255, 255, 242)):
    sh_img, pad = shadow((w, h), r, blur=24, alpha=90)
    c = Image.new("RGBA", sh_img.size, (0, 0, 0, 0))
    c.alpha_composite(sh_img)
    body = Image.new("RGBA", (w, h), fill)
    c.paste(body, (pad, pad), rounded_mask((w, h), r))
    return c, pad

def draw_check(d, x, y, s, on):
    if on:
        d.ellipse((x, y, x + s, y + s), fill=YELLOW + (255,))
        d.line((x + s * .27, y + s * .52, x + s * .44, y + s * .69, x + s * .75, y + s * .33), fill=INK + (255,), width=max(3, s // 9), joint="curve")
    else:
        d.ellipse((x, y, x + s, y + s), outline=(200, 200, 205, 255), width=4)

@functools.lru_cache(maxsize=None)
def checklist_img(title, items, n_on, yellow_words):
    fT, fI = font("black", 46), font("xbold", 46)
    w = 900
    h = 120 + 92 * len(items)
    c, pad = card(w, h)
    d = ImageDraw.Draw(c)
    d.text((pad + 44, pad + 34), title, font=fT, fill=INK)
    for i, it in enumerate(items):
        y = pad + 118 + i * 92
        on = i < n_on
        draw_check(d, pad + 44, y, 54, on)
        x = pad + 124
        for word in it.split(" "):
            col = YELLOW_DARK if word.strip(",./").lower() in yellow_words else (INK if on else (150, 150, 158))
            d.text((x, y + 2), word, font=fI, fill=col)
            x += text_w(fI, word + " ")
    return c, pad

YELLOW_DARK = (222, 160, 0)

def checklist(t, t0, t1, title, items, times, yellow_words):
    if not (t0 <= t < t1):
        return None
    n_on = sum(1 for x in times if t >= x)
    img, pad = checklist_img(title, tuple(items), n_on, tuple(yellow_words))
    a = min(1, (t - t0) / 0.18, (t1 - t) / 0.15)
    pop = 0.92 + 0.08 * ease_out((t - t0) / 0.25)
    return img, W // 2, 150 + img.size[1] // 2 - pad, a, pop

@functools.lru_cache(maxsize=None)
def big_text(lines, size=118, color=YELLOW, sub=None):
    f = font("black", size)
    fs = font("xbold", 44)
    lh = int(size * 1.08)
    w = max(text_w(f, l) for l in lines) + 40
    h = lh * len(lines) + (80 if sub else 0) + 30
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        x = (im.size[0] - text_w(f, l)) // 2
        d.text((x, 20 + i * lh), l, font=f, fill=color + (255,), stroke_width=6, stroke_fill=(0, 0, 0, 255))
    if sub:
        x = (im.size[0] - text_w(fs, sub)) // 2
        d.text((x, 30 + lh * len(lines)), sub, font=fs, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    return im

@functools.lru_cache(maxsize=None)
def shield_card():
    w, h = 820, 560
    c, pad = card(w, h)
    d = ImageDraw.Draw(c)
    cx, cy = pad + w // 2, pad + 200
    s = 150  # bouclier
    pts = [(cx, cy - s), (cx + s * .85, cy - s * .62), (cx + s * .75, cy + s * .35), (cx, cy + s), (cx - s * .75, cy + s * .35), (cx - s * .85, cy - s * .62)]
    d.polygon(pts, fill=(255, 112, 30, 255))
    d.line((cx - 55, cy + 2, cx - 12, cy + 48, cx + 62, cy - 45), fill=(255, 255, 255, 255), width=22, joint="curve")
    f, fs = font("black", 64), font("semi", 36)
    t = "Trade Assurance"
    d.text((cx - text_w(f, t) // 2, pad + 390), t, font=f, fill=YELLOW_DARK)
    t2 = "Protection d'achat Alibaba"
    d.text((cx - text_w(fs, t2) // 2, pad + 478), t2, font=fs, fill=(90, 90, 98))
    return c

@functools.lru_cache(maxsize=None)
def note_pill(text):
    f = font("semi", 32)
    w = text_w(f, text) + 60
    c, pad = card(w, 70, r=35, fill=(20, 20, 24, 215))
    ImageDraw.Draw(c).text((pad + 30, pad + 15), text, font=f, fill=(255, 255, 255))
    return c, pad

@functools.lru_cache(maxsize=None)
def million_card():
    w, h = 900, 470
    c, pad = card(w, h)
    d = ImageDraw.Draw(c)
    f1, f2, f3 = font("black", 128), font("xbold", 50), font("xbold", 50)
    t = "1 000 000 $"
    d.text((pad + (w - text_w(f1, t)) // 2, pad + 50), t, font=f1, fill=INK)
    t = "de transactions"
    d.text((pad + (w - text_w(f2, t)) // 2, pad + 215), t, font=f2, fill=(90, 90, 98))
    t = "= bon signe"
    tw = text_w(f3, t) + 80
    x0 = pad + (w - tw) // 2
    d.rounded_rectangle((x0, pad + 320, x0 + tw, pad + 410), 45, fill=YELLOW)
    d.text((x0 + 40, pad + 334), t, font=f3, fill=INK)
    return c, pad

@functools.lru_cache(maxsize=None)
def contact_button(pressed):
    f = font("xbold", 50)
    t = "Contact Supplier"
    w, h = text_w(f, t) + 120, 116
    c, pad = card(w, h, r=58, fill=(255, 106, 0, 255) if not pressed else (225, 88, 0, 255))
    ImageDraw.Draw(c).text((pad + 60, pad + 28), t, font=f, fill=(255, 255, 255))
    return c, pad

@functools.lru_cache(maxsize=None)
def cursor_img():
    s = 3
    im = Image.new("RGBA", (40 * s, 56 * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(2, 2), (2, 44), (12, 34), (20, 52), (28, 48), (20, 31), (34, 31)]
    d.polygon([(x * s, y * s) for x, y in pts], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2 * s)
    return im.resize((40 * 2, 56 * 2), Image.LANCZOS)

def wrap(words, f, maxw):
    lines, cur = [], ""
    for w_ in words:
        test = (cur + " " + w_).strip()
        if text_w(f, test) <= maxw:
            cur = test
        else:
            lines.append(cur); cur = w_
    if cur:
        lines.append(cur)
    return lines

MSG_WORDS = None
def message_bubble(t):
    global MSG_WORDS
    if MSG_WORDS is None:
        ws = [w for w in WORDS if 91.7 <= w["start"] <= 101.6 and w["text"] not in ("«", "»")]
        MSG_WORDS = ws
    shown = [w["text"] for w in MSG_WORDS if t >= w["start"] - 0.05]
    return _bubble(tuple(shown))

@functools.lru_cache(maxsize=None)
def _bubble(shown):
    f, fh = font("semi", 46), font("xbold", 34)
    all_words = [w["text"] for w in MSG_WORDS]
    lines_all = wrap(all_words, f, 800)
    w, h = 900, 150 + 64 * len(lines_all) + 40
    c, pad = card(w, h, r=40)
    d = ImageDraw.Draw(c)
    d.text((pad + 48, pad + 38), "Message au fournisseur", font=fh, fill=(255, 106, 0))
    lines = wrap(list(shown), f, 800)
    for i, l in enumerate(lines):
        d.text((pad + 48, pad + 110 + i * 64), l, font=f, fill=INK)
    if shown and len(shown) < len(all_words):  # curseur de saisie
        lx = pad + 48 + text_w(f, lines[-1]) + 10
        ly = pad + 110 + (len(lines) - 1) * 64
        d.rectangle((lx, ly + 6, lx + 5, ly + 54), fill=(255, 106, 0))
    return c, pad

def cta(t):
    out = []
    f1, f2 = font("black", 72), font("xbold", 58)
    specs = [(137.64, "Pour plus d'astuces,", (255, 255, 255), 1180, f2),
             (138.82, "rejoins ma chaîne", (255, 255, 255), 1270, f1),
             (139.52, "WhatsApp", (37, 211, 102), 1360, font("black", 96)),
             (140.30, "Le lien est dans ma bio", YELLOW, 1500, f2)]
    for ts, txt, col, y, ff in specs:
        if t >= ts:
            im = _txt(txt, col, ff.size, ff.path)
            out.append((im, W // 2, y, min(1, (t - ts) / 0.12), 0.85 + 0.15 * ease_out((t - ts) / 0.2)))
    return out

@functools.lru_cache(maxsize=None)
def _txt(txt, col, size, path):
    ff = ImageFont.truetype(path, size)
    words = txt.split(" ")
    gap = int(size * 0.32)
    w = sum(text_w(ff, x) for x in words) + gap * (len(words) - 1) + 40
    im = Image.new("RGBA", (w, int(size * 1.4)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 20
    for word in words:
        d.text((x, 4), word, font=ff, fill=col + (255,), stroke_width=7, stroke_fill=(0, 0, 0, 255))
        x += text_w(ff, word) + gap
    return im

def overlays(t):
    """Retourne une liste (img RGBA, cx, cy, alpha, scale)."""
    out = []
    o = checklist(t, 33.65, 46.30, "Les points à demander au transitaire",
                  ["Prix du kilo / CBM", "Durée d'envoi", "Adresse en Chine", "Shipping mark"],
                  [33.76, 39.66, 42.60, 45.42], ["prix", "cbm", "shipping", "mark"])
    if o: out.append(o)
    o = checklist(t, 58.00, 64.60, "Les critères du fournisseur",
                  ["2 ans minimum", "Statut vérifié", "Avis positifs", "Trade Assurance"],
                  [59.52, 61.82, 63.26, 64.70], ["trade", "assurance"])
    if o: out.append(o)
    if 48.85 <= t < 50.05:
        k = (t - 48.85)
        out.append((big_text(("C'EST NON", "NÉGOCIABLE")), W // 2, 900, min(1, k / 0.1), 1.25 - 0.25 * ease_out(k / 0.18)))
    if 64.60 <= t < 66.00:
        k = t - 64.60
        out.append((shield_card(), W // 2, 860, min(1, k / 0.12), 0.85 + 0.15 * ease_out(k / 0.22)))
    if 66.00 <= t < 71.10:
        im, pad = note_pill("Protection d'achat Alibaba · selon conditions")
        out.append((im, W // 2, 240, min(1, (t - 66.0) / 0.2, (71.1 - t) / 0.15), 1.0))
    if 78.55 <= t < 82.40:
        im, pad = million_card(); k = t - 78.55
        out.append((im, W // 2, 820, min(1, k / 0.12), 0.85 + 0.15 * ease_out(k / 0.22)))
    if 85.50 <= t < 89.60:
        pressed = 87.86 <= t < 88.10
        im, pad = contact_button(pressed)
        k = t - 85.5
        sc = 0.94 if pressed else 1.0
        out.append((im, W // 2, 1180, min(1, k / 0.15), sc * (0.9 + 0.1 * ease_out(k / 0.2))))
        cx = lerp(W // 2 + 330, W // 2 + 120, smooth((t - 86.6) / 1.1))
        cy = lerp(1420, 1215, smooth((t - 86.6) / 1.1))
        if t > 86.4:
            out.append((cursor_img(), int(cx) + 40, int(cy) + 56, min(1, (t - 86.4) / 0.2), 1.0))
    if 91.60 <= t < 102.10:
        im, pad = message_bubble(t)
        k = t - 91.6
        out.append((im, W // 2, 240 + im.size[1] // 2 - pad, min(1, k / 0.15, (102.1 - t) / 0.12), 0.92 + 0.08 * ease_out(k / 0.25)))
    if t >= 137.60:
        out += cta(t)
    return out

def composite(frame, ovs):
    base = frame.convert("RGBA")
    for im, cx, cy, a, sc in ovs:
        if a <= 0:
            continue
        if abs(sc - 1) > 1e-3:
            im = im.resize((max(1, int(im.size[0] * sc)), max(1, int(im.size[1] * sc))), Image.BICUBIC)
        if a < 1:
            im = im.copy(); im.putalpha(Image.eval(im.getchannel("A"), lambda v: int(v * a)))
        base.alpha_composite(im, (int(cx - im.size[0] / 2), int(cy - im.size[1] / 2)))
    return base.convert("RGB")

# ---------------------------------------------------------------- shots
def shot_bounds():
    out = []
    for i, s in enumerate(plan.SHOTS):
        t1 = plan.SHOTS[i + 1]["t"] if i + 1 < len(plan.SHOTS) else plan.TOTAL
        out.append((s, s["t"], t1))
    return out

def render_shot(s, t0, t1):
    n = round(t1 * FPS) - round(t0 * FPS)
    is_vid = s["src"].lower().endswith(".mp4")
    src_iter = video_frames(s["src"], s.get("ss", 0), s.get("speed", 1.0), n) if is_vid else None
    still = None if is_vid else load_image(s["src"])
    for i in range(n):
        k = i / max(1, n - 1)
        img = next(src_iter) if is_vid else still
        m = s["mode"]
        if m == "fill":
            e = smooth(k)
            fr = fill_frame(img, lerp_t(s["c0"], s["c1"], e), lerp(s["z0"], s["z1"], k))
        elif m == "fit":
            box = lerp_t(s["box0"], s.get("box1", s["box0"]), smooth(k))
            fr = fit_frame(img, box, fw=s.get("fw", 1000), fy=s.get("fy"), hl=s.get("hl"), k=k)
        elif m == "logo":
            fr = logo_frame(img, lerp(s["z0"], s["z1"], ease_out(k * 2.5)))
        elif m == "card":
            fr = blur_bg(img, 0.35)
        yield fr

WORDS = json.load(open("audio/voix_off_words.json"))["words"]

def all_frames(t_from=0.0, t_to=None):
    t_to = t_to or plan.TOTAL
    for s, t0, t1 in shot_bounds():
        if t1 <= t_from or t0 >= t_to:
            continue
        f0 = round(t0 * FPS)
        for j, fr in enumerate(render_shot(s, t0, t1)):
            t = (f0 + j) / FPS
            if t < t_from or t >= t_to:
                continue
            ovs = overlays(t)
            if 121.10 <= t < 121.30:  # flash appareil photo
                a = 1 - (t - 121.10) / 0.2
                fr = Image.blend(fr, Image.new("RGB", (W, H), (255, 255, 255)), 0.85 * a)
            yield t, composite(fr, ovs)

# ---------------------------------------------------------------- subtitles (ASS)
def norm(w):
    return w.lower().strip(".,;:!?«» ")

def ass_time(x):
    x = max(0, x)
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"

DISPLAY_FIX = {"trade": "Trade", "assurance.": "Assurance.", "assurance": "Assurance"}

def build_subs():
    ws = []
    for w in WORDS:
        tx = w["text"]
        if tx in ("«", "»", "»."):
            continue
        ws.append(dict(text=DISPLAY_FIX.get(tx, tx), start=w["start"], end=w["end"]))
    def hidden(t):
        return any(a - 0.01 <= t < b for a, b in plan.SUB_HIDE)
    ws = [w for w in ws if not hidden(w["start"])]
    # groupes de 1 à 3 mots, coupure après ponctuation ou pause
    groups, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        nxt = ws[i + 1] if i + 1 < len(ws) else None
        chars = sum(len(x["text"]) + 1 for x in cur)
        brk = (w["text"][-1] in ".,?!:;" or len(cur) >= 3 or chars >= 17 or
               (nxt and nxt["start"] - w["end"] > 0.35) or nxt is None)
        if nxt and not brk and chars + len(nxt["text"]) > 20:
            brk = True
        if brk:
            groups.append(cur); cur = []
    kw = set(plan.KEYWORDS)
    lines = []
    for i, g in enumerate(groups):
        st = g[0]["start"] - 0.04
        en = min(g[-1]["end"] + 0.45, groups[i + 1][0]["start"] - 0.04) if i + 1 < len(groups) else g[-1]["end"] + 0.6
        for a, b in plan.SUB_HIDE:
            if st < a < en:
                en = a
        parts = []
        for w in g:
            tx = w["text"].replace("{", "").replace("}", "")
            if norm(tx) in kw:
                parts.append(r"{\c&H0AD6FF&}" + tx + r"{\c&HFFFFFF&}")
            else:
                parts.append(tx)
        txt = r"\h ".join(parts)
        lines.append(f"Dialogue: 0,{ass_time(st)},{ass_time(en)},Sub,,0,0,0,,{{\\fscx86\\fscy86\\t(0,90,\\fscx100\\fscy100)}}{txt}")
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter Display Black,82,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,6,2,2,90,90,470,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    open("sous_titres.ass", "w", encoding="utf8").write(head + "\n".join(lines) + "\n")
    # SRT simple pour réutilisation (CapCut, Premiere, etc.)
    def srt_t(x):
        x = max(0, x); ms = int(round(x * 1000))
        return f"{ms // 3600000:02d}:{ms % 3600000 // 60000:02d}:{ms % 60000 // 1000:02d},{ms % 1000:03d}"
    srt = []
    for i, g in enumerate(groups):
        st = g[0]["start"] - 0.04
        en = min(g[-1]["end"] + 0.45, groups[i + 1][0]["start"] - 0.04) if i + 1 < len(groups) else g[-1]["end"] + 0.6
        srt.append(f"{i + 1}\n{srt_t(st)} --> {srt_t(en)}\n{' '.join(w['text'] for w in g)}\n")
    open("sous_titres.srt", "w", encoding="utf8").write("\n".join(srt))
    return len(groups)

# ---------------------------------------------------------------- audio
def build_audio(out="cache/mix.wav"):
    inputs = ["-i", "audio/voix_off_samantha_claude.mp3", "-stream_loop", "1", "-i", "audio/music/music_motivating_mornings.mp3"]
    fc = ["[0:a]aresample=48000,volume=-1.5dB,apad=whole_dur=%.2f[v]" % plan.TOTAL]
    a, b, g = plan.MUSIC_DUCK
    fc.append(f"[1:a]aresample=48000,atrim=0:{plan.TOTAL},volume={plan.MUSIC_GAIN_DB}dB,"
              f"volume='if(between(t,{a},{b}),{g},1)':eval=frame,afade=t=in:d=0.6,afade=t=out:st={plan.TOTAL - 2.2}:d=2.2[m]")
    labels = ["[v]", "[m]"]
    for i, (t, name, gain, dur, fade) in enumerate(plan.SFX):
        inputs += ["-i", f"audio/sfx/{name}.mp3"]
        idx = i + 2
        chain = f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo"
        if dur:
            chain += f",atrim=0:{dur}"
            if fade:
                chain += f",afade=t=out:st={max(0, dur - fade)}:d={fade}"
        chain += f",volume={gain}dB,adelay={int(t * 1000)}|{int(t * 1000)}[s{i}]"
        fc.append(chain); labels.append(f"[s{i}]")
    fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,alimiter=limit=0.95[out]")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(fc),
                           "-map", "[out]", "-t", str(plan.TOTAL), "-ac", "2", out])
    return out

# ---------------------------------------------------------------- main
def render(out="export/alibaba_tiktok.mp4"):
    n = build_subs()
    print("sous-titres :", n, "blocs")
    mix = build_audio()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", mix, "-vf", "ass=sous_titres.ass", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
           "-shortest", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    total = round(plan.TOTAL * FPS)
    for i, (t, fr) in enumerate(all_frames()):
        p.stdin.write(fr.tobytes())
        if i % 300 == 0:
            print(f"  {t:6.1f}s / {plan.TOTAL}s", flush=True)
    p.stdin.close(); p.wait()
    print("OK ->", out)

def preview(times):
    build_subs()
    times = sorted(times)
    for t in times:
        got = None
        for tt, fr in all_frames(t, t + 1.0 / FPS + 1e-6):
            got = fr
        path = f"{CACHE}/preview_{t:06.2f}.png"
        got.save(path)
        # sous-titres via ffmpeg pour l'aperçu
        subprocess.call(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", path, "-vf",
                         f"setpts=PTS+{t}/TB,ass=sous_titres.ass", "-frames:v", "1", "-update", "1", path.replace(".png", "_s.png")],
                        stdin=subprocess.DEVNULL)
        print(path)

if __name__ == "__main__":
    if "--preview" in sys.argv:
        preview([float(x) for x in sys.argv[sys.argv.index("--preview") + 1].split(",")])
    elif "--audio" in sys.argv:
        print(build_audio())
    else:
        render()
