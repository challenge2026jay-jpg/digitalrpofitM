#!/usr/bin/env python3
"""Vidéo 3 — « Pinduoduo en français avec WeChat » sur les VRAIS écrans de l'appli (≈ 43 s, 9:16).

Écrans tirés de vidéos virales analysées (voir prep_ecrans.py) : visage, sous-titres et annotations
des créateurs retirés, données personnelles floutées. Notre motion par-dessus : téléphone, léger zoom,
cadre orange qui clignote sur le bouton, flèche, toucher, en-tête avec les vrais logos, visage de Samantha.

Voix : si audio/voix_pdd_ecrans.mp3 existe (voix Manus ou ElevenLabs), elle est mixée et la musique baisse.

    python3 build_pdd_ecrans.py               -> export/pinduoduo_vrais_ecrans_9x16.mp4
    python3 build_pdd_ecrans.py --preview 1,7,26
"""
import sys, os, subprocess, math, functools
import build as B
import build_pdd_motion as M
from build import (W, H, FPS, Image, ImageDraw, ImageFilter, clamp, ease_out, ease_io, card, paste_c,
                   text_img, fit_text, kin, bg_gradient, liquid_mask, tap, rmask, NAVY2, ORANGE, INK, YELLOW, WHITE)
from build_pdd_motion import pdd, wechat, shadowed, pop, chip

TOTAL = 43.0
GREEN = (7, 193, 96)

# ------------------------------------------------------------------ ce que dit Samantha (= script de la voix)
M.LINES = [
    (0.15, 3.2, "Un polo à moins de 20 yuans sur Pinduoduo… mais l'appli est en chinois ?", "pense"),
    (3.2, 5.6, "Je te la mets en français avec WeChat. Suis-moi !", "sourire"),
    (5.6, 8.0, "Dans WeChat, appuie sur « Moi »,", "neutre"),
    (8.0, 10.2, "puis « Paramètres »,", "neutre"),
    (10.2, 12.4, "« Généralités »,", "sourire"),
    (12.4, 14.8, "et « Gérer la page Découvrir ».", "neutre"),
    (14.8, 17.2, "Touche « Mini-programmes »…", "neutre"),
    (17.2, 20.0, "et active « Afficher dans l'onglet Découvrir ».", "sourire"),
    (20.0, 22.4, "Retourne dans « Découvrir », « Mini-programmes »,", "neutre"),
    (22.4, 24.6, "et ouvre Pinduoduo.", "sourire"),
    (24.6, 27.0, "Appuie sur les trois petits points…", "neutre"),
    (27.0, 29.4, "puis « Traduction »… et voilà : en français !", "rire"),
    (29.4, 32.4, "Tu choisis ta taille, tu paies… commande passée !", "sourire"),
    (32.4, 35.6, "Tu es en RDC ? J'ai réuni la liste des transitaires et des fournisseurs dans mon groupe WhatsApp.", "sourire"),
    (35.6, 38.4, "Le lien est dans ma bio. Si tu bloques, écris-moi « PDD ».", "rire"),
    (38.4, 42.6, "Et pour aller plus loin : mes formations.", "sourire"),
]

# ------------------------------------------------------------------ écrans
@functools.lru_cache(maxsize=None)
def screen(name): return Image.open("assets/ecrans/" + name).convert("RGB")

PH_H = 1180            # hauteur de l'écran dans le téléphone
PH_CX, PH_CY = W // 2, 840

# (début, écran, cadre cible (cx, cy, l, h) en 0–1 ou None, délai du toucher, numéro, consigne, logo)
STEPS = [
    (5.6,  "wx_decouvrir.png",  (0.87, 0.95, 0.17, 0.065), 1.3, "1", "Appuie sur « Moi »", "wx"),
    (8.0,  "wx_moi.png",        (0.5, 0.551, 0.95, 0.045), 1.2, "2", "« Paramètres »", "wx"),
    (10.2, "wx_parametres.png", (0.5, 0.511, 0.95, 0.045), 1.1, "3", "« Généralités »", "wx"),
    (12.4, "wx_generalites.png", (0.5, 0.777, 0.95, 0.045), 1.2, "4", "« Gérer la page Découvrir »", "wx"),
    (14.8, "wx_gerer.png",      (0.5, 0.697, 0.95, 0.045), 1.2, "5", "« Mini-programmes »", "wx"),
    (17.2, "wx_activer.png",    (0.82, 0.718, 0.16, 0.045), 1.0, "6", "Active l'interrupteur", "wx"),
    (18.6, "wx_active_ok.png",  (0.5, 0.745, 0.95, 0.09), None, "6", "Service activé", "wx"),
    (20.0, "wx_decouvrir2.png", (0.5, 0.477, 0.95, 0.045), 1.2, "7", "Découvrir › « Mini-programmes »", "wx"),
    (22.4, "wx_miniprog.png",   (0.165, 0.424, 0.2, 0.1), 1.1, "8", "Ouvre Pinduoduo", "pdd"),
    (24.6, "pdd_chinois.png",   (0.80, 0.062, 0.13, 0.045), 1.2, "9", "Appuie sur « ••• »", "pdd"),
    (27.0, "pdd_menu.png",      (0.925, 0.83, 0.13, 0.085), 0.75, "10", "« Traduction »", "pdd"),
    (28.0, "pdd_francais.png",  (0.5, 0.06, 0.98, 0.05), None, "", "En français !", "pdd"),
    (29.4, "cc_taille.png",     (0.25, 0.735, 0.1, 0.06), 0.9, "", "Choisis ta taille", "pdd"),
    (30.9, "cc_paye.png",       (0.5, 0.12, 0.6, 0.1), None, "", "Payé : ¥19,80", "pdd"),
]
T_END = 32.4

def phone_screen(sc, ph_h=PH_H):
    w = int(sc.width * ph_h / sc.height)
    if w > 820: w, ph_h = 820, int(sc.height * 820 / sc.width)
    return sc.resize((w, ph_h), Image.LANCZOS)

def phone_frame(inner):
    w, h = inner.size
    fr = Image.new("RGBA", (w + 28, h + 28), (0, 0, 0, 0))
    ImageDraw.Draw(fr).rounded_rectangle((0, 0, w + 27, h + 27), 54, fill=(20, 20, 24, 255))
    fr.paste(inner, (14, 14), rmask((w, h), 44))
    return card(fr.convert("RGB"), 58)

def zoomed(sc, box, z):
    """Recadrage qui se resserre doucement vers la cible (zoom caméra)."""
    if z <= 1.0 or box is None: return sc
    cx, cy = box[0] * sc.width, box[1] * sc.height
    w, h = sc.width / z, sc.height / z
    l = clamp(cx - w / 2, 0, sc.width - w); t = clamp(cy - h / 2, 0, sc.height - h)
    return sc.crop((int(l), int(t), int(l + w), int(t + h))).resize(sc.size, Image.BICUBIC), (l, t, w, h)

def step_at(t):
    cur = [s for s in STEPS if t >= s[0]]
    return cur[-1] if cur else STEPS[0]

def header(base, t, s):
    t0, _, _, _, num, txt, lg = s
    k = ease_out((t - t0) / 0.3)
    parts = []
    lgim = wechat(104) if lg == "wx" else pdd(110)
    tx = fit_text(txt, "Bold", 60, WHITE, 0, 760 if num else 840)
    wtot = lgim.width + 24 + (100 if num else 0) + tx.width
    im = Image.new("RGBA", (wtot, 120), (0, 0, 0, 0)); x = 0
    im.alpha_composite(lgim, (x, 60 - lgim.height // 2)); x += lgim.width + 24
    if num:
        d = ImageDraw.Draw(im); d.ellipse((x, 18, x + 84, 102), fill=ORANGE + (255,))
        fn = B.f_anton(56 if len(num) == 1 else 46); d.text((x + 42 - B.tw(fn, num) // 2, 22 if len(num) == 1 else 28), num, font=fn, fill=WHITE)
        x += 100
    im.alpha_composite(tx, (x, 60 - tx.height // 2))
    paste_c(base, im, W // 2, 150 + (1 - k) * 25, k)

def arrow(base, x, y, side, t):
    """Flèche jaune qui pointe la cible (depuis la gauche ou la droite, ou le haut)."""
    b = 12 * math.sin(t * 9)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    if side == "down":
        pts = [(x, y + b), (x - 34, y - 46 + b), (x - 13, y - 46 + b), (x - 13, y - 130 + b), (x + 13, y - 130 + b), (x + 13, y - 46 + b), (x + 34, y - 46 + b)]
    else:
        s = -1 if side == "left" else 1
        pts = [(x + s * b, y), (x + s * (46 + b), y - 34), (x + s * (46 + b), y - 13), (x + s * (130 + b), y - 13),
               (x + s * (130 + b), y + 13), (x + s * (46 + b), y + 13), (x + s * (46 + b), y + 34)]
    d.polygon(pts, fill=YELLOW + (255,), outline=INK + (255,), width=4)
    base.alpha_composite(ov)

def s_steps(t):
    base = bg_gradient(t)
    s = step_at(t); i = STEPS.index(s)
    t0, name, box, tap_dt, num, txt, lg = s
    sc = screen(name)
    z = 1 + 0.10 * ease_io((t - t0 - 0.3) / 1.2) if box and box[2] < 0.9 else 1 + 0.04 * ease_io((t - t0) / 1.5)
    inner_full = phone_screen(sc)
    zr = zoomed(inner_full, box, z)
    inner, view = (zr if isinstance(zr, tuple) else (zr, (0, 0, inner_full.width, inner_full.height)))
    # glissement depuis l'écran précédent (navigation dans l'appli)
    if i > 0 and t - t0 < 0.28:
        prev = phone_screen(screen(STEPS[i - 1][1]))
        if prev.size != inner.size: prev = prev.resize(inner.size)
        k = ease_out((t - t0) / 0.28); comp = prev.copy()
        comp.paste(inner, (int(inner.width * (1 - k)), 0)); inner = comp
    ph = phone_frame(inner)
    paste_c(base, ph, PH_CX, PH_CY, 1.0)
    ox = PH_CX - inner.width / 2; oy = PH_CY - inner.height / 2
    if box:
        l, tp, vw, vh = view; sx = inner.width / vw; sy = inner.height / vh
        cx = ox + (box[0] * inner_full.width - l) * sx; cy = oy + (box[1] * inner_full.height - tp) * sy
        bw = box[2] * inner_full.width * sx; bh = box[3] * inner_full.height * sy
        a = clamp((t - t0 - 0.3) / 0.2)
        if a > 0:
            blink = 0.55 + 0.45 * (0.5 + 0.5 * math.sin((t - t0) * 11))
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
            col = GREEN if not num else ORANGE
            d.rounded_rectangle((cx - bw / 2 - 8, cy - bh / 2 - 8, cx + bw / 2 + 8, cy + bh / 2 + 8), 18,
                                fill=col + (int(55 * a * blink),), outline=col + (int(255 * a * blink),), width=8)
            base.alpha_composite(ov)
            if num and tap_dt is not None and t < t0 + tap_dt + 0.1:
                if bw > inner.width * 0.6: arrow(base, cx + bw / 2 - 60, cy - bh / 2 - 14, "down", t)
                elif cx > PH_CX: arrow(base, cx - bw / 2 - 18, cy, "left", t)
                else: arrow(base, cx + bw / 2 + 18, cy, "right", t)
            if tap_dt is not None: tap(base, t, t0 + tap_dt, cx, cy)
    header(base, t, s)
    # badges de résultat
    if name == "pdd_francais.png":
        kf = pop(t, t0 + 0.15)
        if kf > 0:
            b = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); bd = ImageDraw.Draw(b)
            bd.ellipse((0, 0, 179, 179), fill=YELLOW + (255,), outline=WHITE + (255,), width=8); ft = B.f_anton(88)
            bd.text((90 - B.tw(ft, "FR") // 2, 24), "FR", font=ft, fill=INK)
            paste_c(base, b, PH_CX + inner.width / 2 - 10, PH_CY - inner.height / 2 + 110, 1.0, max(0.01, kf), -10)
    if name == "cc_paye.png":
        kc = pop(t, t0 + 0.2)
        if kc > 0: paste_c(base, chip("Commande passée", GREEN, WHITE, 70), W // 2, PH_CY + inner.height / 2 + 30, 1.0, max(0.01, kc), -3)
    return base

def s_hook(t):                        # 0 – 5.6
    base = bg_gradient(t)
    if t < 3.2:
        # le vrai prix sur la fiche produit
        sc = phone_screen(screen("cc_produit.png"), 1000)
        z = 1 + 0.35 * ease_io((t - 0.3) / 1.4)
        box = (0.27, 0.512, 0.32, 0.05)
        inner, view = zoomed(sc, box, z) if z > 1 else (sc, (0, 0, sc.width, sc.height))
        k = ease_out(t / 0.35)
        paste_c(base, phone_frame(inner), W // 2, 940 + (1 - k) * 120, k, 1.0, -3 * (1 - ease_io(t / 1.2)))
        l, tp, vw, vh = view; sx = inner.width / vw
        cx = W // 2 - inner.width / 2 + (box[0] * sc.width - l) * sx; cy = 940 - inner.height / 2 + (box[1] * sc.height - tp) * sx
        if t > 1.2:
            bl = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * 11))
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(ov).rounded_rectangle((cx - 150, cy - 50, cx + 150, cy + 50), 20, outline=YELLOW + (int(255 * bl),), width=9)
            base.alpha_composite(ov)
        kin(base, "Un polo à ¥19,8 ?!", t, 0.3, W // 2, 150, "anton", 120, YELLOW)
        kp = pop(t, 1.7)
        if kp > 0:
            paste_c(base, shadowed(pdd(130)), 150, 300, 1.0, max(0.01, kp), -8)
            kin(base, "…mais tout est en chinois", t, 1.8, W // 2 + 70, 300, "SemiBold", 56, WHITE)
    else:
        # avant / après : chinois → français
        for j, (nm, lab, cx) in enumerate((("pdd_chinois.png", "AVANT", 290), ("pdd_francais.png", "APRÈS", W - 290))):
            k = ease_out((t - 3.2 - 0.25 * j) / 0.4)
            if k <= 0: continue
            sc = phone_screen(screen(nm), 860)
            paste_c(base, phone_frame(sc), cx, 900 + (1 - k) * 100, k, 1.0, -4 if j == 0 else 4)
            paste_c(base, chip(lab, (90, 90, 100) if j == 0 else GREEN, WHITE, 52), cx, 420, k)
        kw = pop(t, 3.5)
        if kw > 0: paste_c(base, shadowed(wechat(170)), W // 2, 900, 1.0, max(0.01, kw))
        kin(base, "En FRANÇAIS avec WeChat", t, 3.3, W // 2, 190, "anton", 104, YELLOW)
    return base

def s_rdc(t): return M.s_rdc(t - 32.4 + 19.4)
def s_form(t): return M.s_formations(t - 38.4 + 25.4)

SCENES = [(0, s_hook), (5.6, s_steps), (32.4, s_rdc), (38.4, s_form)]
CUTS = (5.6, 32.4, 38.4)

def frame(t):
    im = [f for t0, f in SCENES if t >= t0][-1](t)
    for tc in CUTS:
        if tc - 0.01 <= t < tc + 0.45:
            prev = [f for t0, f in SCENES if t0 < tc][-1](tc - 0.02)
            m = liquid_mask(clamp((t - tc) / 0.45), (0.5, 1.0))
            prev.paste(im, (0, 0), m); im = prev
    M.bottom_shade(im); M.avatar(im, t); M.speech_bubble(im, t)
    if t > TOTAL - 0.5:
        im = Image.blend(im, Image.new("RGBA", (W, H), NAVY2 + (255,)), clamp((t - (TOTAL - 0.5)) / 0.5) * 0.6)
    return im.convert("RGB")

# ------------------------------------------------------------------ son
VOICE = "audio/voix_pdd_ecrans.mp3"
SFX = [(c - 0.02, "audio/sfx_souffle.mp3", -10) for c in CUTS] + \
      [(s[0] + s[3], "audio/sfx_clic.mp3", -14) for s in STEPS if s[3] is not None] + \
      [(t0 + 13.0 + 0.98, "audio/sfx_clic.mp3", -11) for t0 in (25.4, 27.5)]

def build_audio(out="cache/mix_pdd_ecrans.wav"):
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
        fc.append(f"[{j}:a]aresample=48000,aformat=channel_layouts=stereo,adelay=150|150[v]"); lab.append("[v]")
    fc.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0:duration=first,alimiter=limit=0.8:level=false[o]")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", ";".join(fc), "-map", "[o]", "-t", str(TOTAL), "-ac", "2", out])
    return out

def render(out="export/pinduoduo_vrais_ecrans_9x16.mp4"):
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
            g.save(f"cache/pdde_preview_{j // 5}.jpg", quality=86)
        print("ok")
    else:
        render()
