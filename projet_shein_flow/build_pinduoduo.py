#!/usr/bin/env python3
"""Vidéo 2 — « Pinduoduo en français avec WeChat » (≈ 22 s, 9:16, texte animé + musique).

Stratégie tirée de vidéos virales du même sujet (analyse dans STRATEGIE_PINDUODUO.md) :
  accroche-problème → étapes concrètes très lisibles → preuve → appel à écrire (DM) → formations.
Le chemin WeChat est celui montré publiquement par @yayoservices (TikTok) ; aucune fausse capture
d'appli n'est fabriquée : les étapes sont présentées en cartes typographiques.

    python3 build_pinduoduo.py            -> export/pinduoduo_wechat_9x16.mp4
    python3 build_pinduoduo.py --preview 1,5,9
"""
import sys, subprocess, math
import build as B
from build import (W, H, FPS, Image, ImageDraw, clamp, ease_out, ease_io, cover, card, paste_c, text_img, fit_text,
                   kin, bg_gradient, bg_cream, liquid_mask, phone_page, tap, badge, img, rmask,
                   NAVY, ORANGE, CREAM, INK, YELLOW, WHITE)

TOTAL = 22.5
RED = (230, 56, 44)

def persona(name, t, t0, cx=0.5, cy=0.4, z=1.0, w=W, h=H):
    return cover(img(name), w, h, cx, cy, z * (1 + 0.035 * max(0, t - t0)))

def ai_tag(base):
    paste_c(base, text_img("Personnage généré par IA", "SemiBold", 26, WHITE), W - 200, 92, 0.75)

# ---------------------------------------------------------------- scènes
def s_hook(t):            # 0 – 2.6
    base = Image.new("RGBA", (W, H)); base.paste(persona("perso_etonnee_tailleur.png", t, 0, 0.5, 0.42, 1.05), (0, 0))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle((0, 1050, W, H), fill=(6, 12, 30, 170)); base.alpha_composite(ov)
    kin(base, "Pinduoduo est en chinois ?", t, 0.15, W // 2, 1220, "play", 96, WHITE, 3)
    kin(base, "Mets-le en FRANÇAIS", t, 0.9, W // 2, 1370, "anton", 120, YELLOW, 2)
    kin(base, "en 6 étapes, avec WeChat", t, 1.5, W // 2, 1500, "SemiBold", 52, CREAM)
    ai_tag(base); return base

def s_problem(t):         # 2.6 – 4.6
    base = bg_gradient(t)
    paste_c(base, fit_text("拼多多", "cjk", 400, WHITE, 0, 1000), W // 2, 1500, 0.08)
    k = ease_out((t - 2.6) / 0.35)
    paste_c(base, card(cover(img("exasperation_assise_ordinateur.png"), 820, 980, 0.5, 0.42), 40), W // 2, 1150 + (1 - k) * 80, k)
    kin(base, "Tout est en chinois…", t, 2.7, W // 2, 330, "anton", 104, WHITE)
    kin(base, "et tu bloques.", t, 3.4, W // 2, 470, "anton", 104, YELLOW)
    return base

STEPS = [("1", "Ouvre WeChat", "onglet « Moi »"),
         ("2", "« Paramètres »", "puis « Généralités »"),
         ("3", "« Gérer la page Découvrir »", ""),
         ("4", "Active « Mini-programmes »", ""),
         ("5", "Découvrir › Mini-programmes", "cherche 拼多多 (Pinduoduo)"),
         ("6", "Appuie sur « Traduction »", "→ Pinduoduo en français")]
T_STEPS, DT = 4.6, 1.25

def step_card(num, title, sub, active):
    w, h = 900, 150 if not sub else 196
    im = Image.new("RGB", (w, h), WHITE); d = ImageDraw.Draw(im)
    col = ORANGE if active else (200, 200, 205)
    d.ellipse((30, h // 2 - 46, 122, h // 2 + 46), fill=col)
    fn = B.f_anton(64); d.text((76 - B.tw(fn, num) // 2, h // 2 - 46), num, font=fn, fill=WHITE)
    ft = B.f_inter("Bold", 50); fs = B.f_inter("Medium", 38)
    title_im = fit_text(title, "Bold", 50, INK, 0, 720)
    im.paste(title_im, (150, (24 if sub else h // 2 - 38)), title_im)
    if sub:
        sub_im = fit_text(sub, "cjk" if any(ord(c) > 0x2E80 for c in sub) else "Medium", 38, (90, 90, 100), 0, 720); im.paste(sub_im, (150, 112), sub_im)
    return card(im, 30)

def s_steps(t):           # 4.6 – 12.1
    base = bg_cream(t)
    kin(base, "WeChat → Pinduoduo en français", t, 4.6, W // 2, 190, "play", 70, NAVY)
    n = int((t - T_STEPS) / DT) + 1
    y0, gap = 330, 225
    for i, (num, ti, sub) in enumerate(STEPS[:max(0, n)]):
        t0 = T_STEPS + i * DT
        k = ease_out((t - t0) / 0.35)
        paste_c(base, step_card(num, ti, sub, i == n - 1), W // 2, y0 + i * gap + 110 + (1 - k) * 60, k)
    return base

def s_proof(t):           # 12.1 – 14.6
    base = Image.new("RGBA", (W, H)); base.paste(persona("perso_jubilante_robe_orange.png", t, 12.1, 0.5, 0.4, 1.1), (0, 0))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle((0, 1080, W, H), fill=(6, 12, 30, 165)); base.alpha_composite(ov)
    kin(base, "Et voilà : en français.", t, 12.2, W // 2, 1250, "play", 98, WHITE, 3)
    kin(base, "Commander, payer, faire livrer au Congo ?", t, 12.9, W // 2, 1400, "SemiBold", 48, YELLOW, 2)
    ai_tag(base); return base

def s_dm(t):              # 14.6 – 18.6 : appel à écrire
    base = bg_gradient(t, warm=True)
    kin(base, "Écris « PDD »", t, 14.7, W // 2, 300, "anton", 150, YELLOW)
    kin(base, "sur WhatsApp, je réponds à tes questions", t, 15.1, W // 2, 440, "SemiBold", 50, WHITE)
    ph, s = phone_page("capture_chaine_whatsapp.jpg", 1050)
    k = ease_out((t - 15.3) / 0.4)
    if t >= 15.3: paste_c(base, ph, W // 2, 1150 + (1 - k) * 200, k)
    return base

PAGES2 = [("capture_formation_ia_motion_design.jpg", 18.6, (20, 1066, 630, 1134), "335+ apprenants"),
          ("capture_formation_claude_transform.jpg", 20.4, (26, 938, 624, 1003), "128+ apprenants")]

def s_formations(t):      # 18.6 – fin
    base = bg_gradient(t)
    kin(base, "Et pour aller plus loin :", t, 18.6, W // 2, 120, "play", 76, WHITE)
    for i, (name, t0, btn, lab) in enumerate(PAGES2):
        t1 = PAGES2[i + 1][1] if i + 1 < len(PAGES2) else 99
        if not (t0 <= t < t1 + 0.35): continue
        ph, s = phone_page(name)
        ki = ease_out((t - t0) / 0.35); out = ease_io((t - t1) / 0.35) if t >= t1 else 0
        cx = W // 2 + (1 - ki) * 700 - out * 900; cy = 1060
        ox = cx - ph.width / 2 + 84; oy = cy - ph.height / 2 + 84
        paste_c(base, ph, cx, cy, 1.0)
        badge(base, t, t0 + 0.4, lab, W // 2, 245)
        tap(base, t, t0 + 1.0, ox + (btn[0] + btn[2]) / 2 * s + 120, oy + (btn[1] + btn[3]) / 2 * s)
    return base

SCENES = [(0, s_hook), (2.6, s_problem), (4.6, s_steps), (12.1, s_proof), (14.6, s_dm), (18.6, s_formations)]

def frame(t):
    fn = [f for t0, f in SCENES if t >= t0][-1]
    im = fn(t)
    for tc in (2.6, 4.6, 12.1, 14.6):          # transitions liquides aux changements de partie
        if tc - 0.01 <= t < tc + 0.45:
            prev = [f for t0, f in SCENES if t0 < tc][-1](tc - 0.02)
            m = liquid_mask(clamp((t - tc) / 0.45), (0.5, 1.0))
            prev.paste(im, (0, 0), m); im = prev
    if t > TOTAL - 0.5:
        im = Image.blend(im, Image.new("RGBA", (W, H), B.NAVY2 + (255,)), clamp((t - (TOTAL - 0.5)) / 0.5) * 0.6)
    return im.convert("RGB")

SFX = [(2.58, "audio/sfx_souffle.mp3", -8), (4.58, "audio/sfx_souffle.mp3", -10), (12.08, "audio/sfx_souffle.mp3", -10),
       (14.58, "audio/sfx_souffle.mp3", -8), (19.6, "audio/sfx_clic.mp3", -9), (21.4, "audio/sfx_clic.mp3", -9)]

def build_audio(out="cache/mix_pdd.wav"):
    inp = ["-i", "audio/musique_tech_house.mp3"]
    fc = [f"[0:a]aresample=48000,atrim=0:{TOTAL},volume=-6dB,afade=t=in:d=0.2,afade=t=out:st={TOTAL - 1.5}:d=1.5[m]"]
    lab = ["[m]"]
    for i, (t, f, g) in enumerate(SFX):
        inp += ["-i", f]
        fc.append(f"[{i + 1}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:1.4,afade=t=out:st=1.0:d=0.4,volume={g}dB,adelay={int(t * 1000)}|{int(t * 1000)}[s{i}]")
        lab.append(f"[s{i}]")
    fc.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0:duration=first,alimiter=limit=0.8:level=false[o]")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", ";".join(fc), "-map", "[o]", "-t", str(TOTAL), "-ac", "2", out])
    return out

def render(out="export/pinduoduo_wechat_9x16.mp4"):
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
            g.save(f"cache/pdd_preview_{j // 5}.jpg", quality=86)
        print("ok")
    else:
        render()
