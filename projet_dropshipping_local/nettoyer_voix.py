#!/usr/bin/env python3
"""Nettoie la voix originale (audio WhatsApp de Samantha) sans la transformer :
retire les doublons, les hésitations et les silences trop longs, puis remonte le niveau.

    python3 nettoyer_voix.py   -> audio/voix_nettoyee.wav + audio/coupes_voix.json

Aucune voix de synthèse : seuls des morceaux de l'enregistrement original sont gardés.
"""
import json, subprocess, numpy as np, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SRC = "audio/WhatsApp Audio 2026-11-11 at 09.16.36.mp4"
SR = 48000

# Coupes repérées à la transcription (secondes dans l'audio original)
CUTS = [
    (0.00, 2.70, "silence de début"),
    (79.64, 81.58, "doublon : « ou avant d'acheter un gros produit »"),
    (84.82, 88.36, "faux départs : « qui ne risque pas, qui risque de ne pas être… »"),
    (90.46, 91.22, "hésitation : « euh »"),
    (93.34, 96.60, "hésitation : « les… » + longue pause"),
    (102.60, 103.84, "doublon : « Tu peux… »"),
]
MAX_PAUSE = 0.38          # les silences plus longs sont ramenés à cette durée
THR = -44                 # seuil de silence (dBFS, fenêtres de 20 ms)

pcm = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", SRC, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]), np.float32)
dur = len(pcm) / SR

# 1) intervalles gardés après les coupes manuelles
keep = []; t = 0.0
for a, b, _ in sorted(CUTS):
    if a > t: keep.append([t, a])
    t = max(t, b)
if t < dur: keep.append([t, dur])

# 2) raccourcir les silences longs à l'intérieur des intervalles gardés
win = int(0.02 * SR)
def silent_runs(a, b):
    i0, i1 = int(a * SR), int(b * SR); seg = pcm[i0:i1]; n = len(seg) // win
    if n == 0: return []
    e = 20 * np.log10(np.sqrt((seg[:n * win].reshape(n, win) ** 2).mean(1)) + 1e-9)
    runs = []; st = None
    for k, s in enumerate(e < THR):
        if s and st is None: st = k
        if not s and st is not None: runs.append((a + st * 0.02, a + k * 0.02)); st = None
    if st is not None: runs.append((a + st * 0.02, a + n * 0.02))
    return runs
final = []
for a, b in keep:
    cur = a
    for s0, s1 in silent_runs(a, b):
        if s1 - s0 > MAX_PAUSE:
            mid = (s0 + s1) / 2; h = MAX_PAUSE / 2
            final.append([cur, mid - h]); cur = mid + h
    final.append([cur, b])
final = [[round(x, 3), round(y, 3)] for x, y in final if y - x > 0.02]

# 3) assemblage avec fondus de 12 ms à chaque raccord, niveau remonté (-16 LUFS), voix d'origine préservée
fade = int(0.012 * SR); parts = []
for a, b in final:
    seg = pcm[int(a * SR):int(b * SR)].copy()
    if len(seg) > 2 * fade:
        ramp = np.linspace(0, 1, fade, dtype=np.float32); seg[:fade] *= ramp; seg[-fade:] *= ramp[::-1]
    parts.append(seg)
out = np.concatenate(parts)
raw = "cache/voix_coupee.f32"; out.tofile(raw)
subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw,
                       "-af", "highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "audio/voix_nettoyee.wav"])
json.dump({"source": SRC, "coupes": CUTS, "gardes": final}, open("audio/coupes_voix.json", "w"), ensure_ascii=False, indent=1)
print(f"original {dur:.1f} s -> nettoyé {len(out) / SR:.1f} s ({len(final)} morceaux)")
