#!/usr/bin/env python3
"""Génère le plan de montage (Markdown) et une timeline FCPXML éditable à partir de plan.py.

  python3 export_projet.py
    -> PLAN_DE_MONTAGE.md
    -> projet_editable/alibaba_tiktok.fcpxml  (DaVinci Resolve / Final Cut Pro / Premiere via import XML)
"""
import os, json, subprocess, urllib.parse
from fractions import Fraction
import plan

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
FPS = 30

SFX_LABEL = {
    "whoosh_fast": "Mixkit « Fast whoosh transition » (#1490)",
    "whoosh_air": "Mixkit « Air woosh » (#1489)",
    "impact_deep_whoosh": "Mixkit « Cinematic whoosh deep impact » (#1143), coupé court",
    "check_box": "Mixkit « Modern click box check » (#1120)",
    "mouse_double": "Mixkit « Fast double click on mouse » (#275)",
    "mouse_clicks": "Mixkit « Clear mouse clicks » (#2997)",
    "typing_laptop": "Mixkit « Typing on a laptop keyboard » (#2531)",
    "confirmation_tone": "Mixkit « Confirmation tone » (#2867)",
    "camera_shutter": "Mixkit « Camera shutter click » (#1133)",
    "scanner_beeps": "Mixkit « Shop scanner beeps » (#1073), 0,7 s",
    "truck_steady": "Mixkit « Truck driving steady » (#1621)",
    "long_pop": "Mixkit « Long pop » (#2358)",
}

ON_SCREEN = [  # (début, fin, texte écran hors sous-titres)
    (33.65, 46.30, "Checklist « Les points à demander au transitaire » : Prix du kilo / CBM · Durée d'envoi · Adresse en Chine · Shipping mark (cochés au fil de la voix)"),
    (48.85, 50.05, "Grand texte jaune « C'EST NON NÉGOCIABLE »"),
    (58.00, 64.60, "Checklist « Les critères du fournisseur » : 2 ans minimum · Statut vérifié · Avis positifs · Trade Assurance"),
    (58.00, 64.60, "Cadre jaune sur « 10 ans », « Verified », « 5/5 » dans la fiche fournisseur"),
    (64.60, 66.00, "Carte neutre « Trade Assurance — Protection d'achat Alibaba » (bouclier)"),
    (66.00, 71.10, "Mention « Protection d'achat Alibaba · selon conditions »"),
    (75.10, 78.55, "Cadre jaune sur le chiffre d'affaires du fournisseur"),
    (78.55, 82.40, "Carte « 1 000 000 $ de transactions = bon signe »"),
    (85.50, 89.60, "Bouton « Contact Supplier » + curseur qui clique (87,9 s)"),
    (91.60, 102.10, "Bulle « Message au fournisseur » : le message anglais s'écrit mot à mot avec la voix"),
    (121.10, 121.30, "Flash blanc (photo du colis)"),
    (137.60, plan.TOTAL, "« Pour plus d'astuces, rejoins ma chaîne WhatsApp — Le lien est dans ma bio »"),
]

def fmt(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"

def bounds():
    for i, s in enumerate(plan.SHOTS):
        yield s, s["t"], (plan.SHOTS[i + 1]["t"] if i + 1 < len(plan.SHOTS) else plan.TOTAL)

def write_plan_md():
    rows = []
    for s, t0, t1 in bounds():
        f = os.path.basename(s["src"])
        extra = ""
        if s["src"].endswith(".mp4"):
            sp = s.get("speed", 1.0)
            extra = f" (extrait {s.get('ss', 0):.1f} s → {s.get('ss', 0) + (t1 - t0) * sp:.1f} s" + (f", vitesse ×{sp}" if sp != 1 else "") + ")"
        txt = "; ".join(x for a, b, x in ON_SCREEN if a < t1 and b > t0) or "Sous-titres synchronisés"
        snd = "; ".join(f"{SFX_LABEL[n].split(' (')[0]} à {t:.2f} s" for t, n, *_ in plan.SFX if t0 - 0.06 <= t < t1)
        rows.append(f"| {s['phrase']} | `{f}`{extra} | {fmt(t0)} → {fmt(t1)} | {txt} | {snd or '—'} |")
    md = ["# Plan de montage — « Commander sur Alibaba » (TikTok 9:16)", "",
          "Voix off : ElevenLabs, voix clonée « voix de samantha claude » (eleven_multilingual_v2), prise 1, 141,8 s.",
          "Timings : transcription horodatée mot à mot (ElevenLabs Scribe), fichier `audio/voix_off_words.json`.",
          "Musique : Mixkit « Motivating Mornings » (#33), −23 dB sous la voix, baissée sur « non négociable ».", "",
          "| Phrase prononcée | Fichier exact | Moment d'apparition | Texte à l'écran | Son ou effet |",
          "|---|---|---|---|---|"] + rows
    md += ["", "Sous-titres : blocs de 1 à 3 mots synchronisés mot à mot, blancs avec contour noir, mots clés en jaune "
           "(Alibaba, transitaire, prix, CBM, Trade Assurance, shipping mark, tracking code), centrés vers 73 % de la hauteur "
           "(au-dessus de la zone légende/boutons TikTok). Masqués quand le même texte est déjà affiché à l'écran "
           "(« non négociable », message au fournisseur, CTA)."]
    open("PLAN_DE_MONTAGE.md", "w", encoding="utf8").write("\n".join(md) + "\n")

# ---------------------------------------------------------------- FCPXML
def rt(sec):
    fr = round(sec * FPS)
    return f"{fr}/{FPS}s" if fr else "0s"

def dur_of(path):
    try:
        return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode().strip())
    except Exception:
        return 0.0

def esc(x):
    return x.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")

def write_fcpxml():
    os.makedirs("projet_editable", exist_ok=True)
    assets, aid = {}, [0]
    def asset(path, kind):
        if path in assets:
            return assets[path][0]
        aid[0] += 1
        assets[path] = (f"a{aid[0]}", kind, dur_of(path) if kind != "image" else 0)
        return assets[path][0]
    clips = []
    for s, t0, t1 in bounds():
        kind = "video" if s["src"].endswith(".mp4") else "image"
        a = asset(s["src"], kind)
        name = esc(os.path.basename(s["src"]))
        if kind == "video":
            clips.append(f'<asset-clip ref="{a}" lane="1" offset="{rt(t0)}" start="{rt(s.get("ss", 0))}" duration="{rt(t1 - t0)}" name="{name}" audioRole="dialogue" />')
        else:
            clips.append(f'<video ref="{a}" lane="1" offset="{rt(t0)}" start="0s" duration="{rt(t1 - t0)}" name="{name}" />')
    vo = asset("audio/voix_off_samantha_claude.mp3", "audio")
    clips.append(f'<asset-clip ref="{vo}" lane="-1" offset="0s" start="0s" duration="{rt(assets["audio/voix_off_samantha_claude.mp3"][2])}" name="Voix off" audioRole="dialogue" />')
    mu = asset("audio/music/music_motivating_mornings.mp3", "audio")
    md = assets["audio/music/music_motivating_mornings.mp3"][2]
    t = 0.0
    while t < plan.TOTAL:
        d = min(md, plan.TOTAL - t)
        clips.append(f'<asset-clip ref="{mu}" lane="-2" offset="{rt(t)}" start="0s" duration="{rt(d)}" name="Musique" audioRole="music"><adjust-volume amount="{plan.MUSIC_GAIN_DB}dB"/></asset-clip>')
        t += d
    for i, (ts, n, gain, dur, fade) in enumerate(plan.SFX):
        p = f"audio/sfx/{n}.mp3"
        a = asset(p, "audio")
        d = dur or assets[p][2]
        clips.append(f'<asset-clip ref="{a}" lane="{-3 - (i % 3)}" offset="{rt(ts)}" start="0s" duration="{rt(d)}" name="SFX {n}" audioRole="effects"><adjust-volume amount="{gain}dB"/></asset-clip>')
    res = ['<format id="r0" name="FFVideoFormat1080x1920p30" frameDuration="1/30s" width="1080" height="1920"/>']
    for path, (i, kind, d) in assets.items():
        url = "file://" + urllib.parse.quote(os.path.abspath(path))
        hv = 'hasVideo="1" format="r0"' if kind in ("video", "image") else ""
        ha = 'hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000"' if kind in ("video", "audio") else ""
        res.append(f'<asset id="{i}" name="{esc(os.path.basename(path))}" start="0s" duration="{rt(d)}" {hv} {ha}><media-rep kind="original-media" src="{url}"/></asset>')
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.10">
  <resources>
    {chr(10).join("    " + r for r in res).strip()}
  </resources>
  <library>
    <event name="Alibaba TikTok">
      <project name="Commander sur Alibaba - TikTok">
        <sequence format="r0" duration="{rt(plan.TOTAL)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">
          <spine>
            <gap name="Base" offset="0s" start="0s" duration="{rt(plan.TOTAL)}">
              {chr(10).join("              " + c for c in clips).strip()}
            </gap>
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
'''
    open("projet_editable/alibaba_tiktok.fcpxml", "w", encoding="utf8").write(xml)

if __name__ == "__main__":
    write_plan_md()
    write_fcpxml()
    print("OK : PLAN_DE_MONTAGE.md, projet_editable/alibaba_tiktok.fcpxml")
