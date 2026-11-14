#!/usr/bin/env python3
"""Retire de la voix off les sons parasites qui ne font pas partie du texte (« Eggy », « Au-dessus »,
« Oh bah », « Yo… Ah… », « Euh… Yo ? »), sans rien changer d'autre.
    python3 nettoyer_voix.py -> audio/voix_montage.wav + audio/mots_montage.json
"""
import json, subprocess, os, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SRC, SR = "audio/voixoff_chine_complete_v2.wav", 48000
CUTS = [
    (303.45, 311.75, "8 s de sons inintelligibles après « Prenons un exemple. »"),
    (334.48, 335.22, "« Eggy » avant « combien me coûtera… »"),
    (338.42, 339.12, "« Au-dessus » avant « c'est cette question… »"),
    (498.00, 499.20, "« Oh bah » avant « est-ce que ce produit peut se vendre ? »"),
    (501.10, 503.62, "« Yo, c'est… Ah… »"),
    (507.75, 510.25, "« Euh… Yo ? » après « après tous les frais ? »"),
]
x = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", SRC, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]), np.float32).copy()
fade = int(0.015 * SR); parts = []; t = 0.0
for a, b, _ in CUTS:
    parts.append((t, a)); t = b
parts.append((t, len(x) / SR))
out = []
for a, b in parts:
    seg = x[int(a * SR):int(b * SR)].copy()
    r = np.linspace(0, 1, fade, dtype=np.float32)
    if a > 0: seg[:fade] *= r
    if b < len(x) / SR: seg[-fade:] *= r[::-1]
    out.append(seg)
y = np.concatenate(out)
y.tofile("cache/voix.f32")
subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "cache/voix.f32", "audio/voix_montage.wav"])

def remap(tt):
    shift = 0.0
    for a, b, _ in CUTS:
        if tt >= b: shift += b - a
        elif tt > a: return None
    return tt - shift
words = json.load(open("audio/transcription.json"))["words"]
# mots oubliés par la transcription automatique (vérifiés par une 2e transcription du passage)
AJOUTS = [("Trouver", 70.50, 70.84), ("un", 70.84, 70.98), ("fournisseur", 70.98, 71.52), ("réellement", 71.52, 71.94), ("fiable.", 71.94, 72.10)]
words = sorted(words + [{"text": a, "start": b, "end": c} for a, b, c in AJOUTS], key=lambda w: w["start"])
kept = []
for w in words:
    s, e = remap(w["start"]), remap(w["end"])
    if s is None or e is None: continue
    kept.append({"text": w["text"], "start": round(s, 3), "end": round(e, 3)})
json.dump({"coupes": CUTS, "words": kept}, open("audio/mots_montage.json", "w"), ensure_ascii=False, indent=0)
print(f"{len(x)/SR:.2f} s -> {len(y)/SR:.2f} s, {len(words)} -> {len(kept)} mots")
