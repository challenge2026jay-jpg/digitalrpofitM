#!/usr/bin/env python3
"""Cale une voix enregistrée (note vocale, MP3, WAV, M4A…) sur le script du montage.

    python3 caler_voix.py chemin/vers/ma_voix.m4a

1. Convertit l'audio en audio/voix_samantha_claude.mp3 (mono 48 kHz, volume normalisé).
2. Transcrit localement avec faster-whisper (mots horodatés), sans service payant.
3. Aligne les mots reconnus sur les mots exacts du script (plan.py) et écrit audio/voix_mots.json.
Ensuite : python3 build.py  → plans, sous-titres et sons suivent la vraie voix.
"""
import sys, os, json, difflib, re, subprocess
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT); sys.path.insert(0, ROOT)
import plan as P

src = sys.argv[1]
out_mp3 = "audio/voix_samantha_claude.mp3"
subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "48000",
                       "-af", "highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11", "-b:a", "192k", out_mp3])

from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")
import numpy as np
pcm = subprocess.check_output(["ffmpeg", "-v", "error", "-i", out_mp3, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"])
segs, _ = model.transcribe(np.frombuffer(pcm, np.float32), language="fr", word_timestamps=True, vad_filter=True)
rec = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words if w.word.strip()]

def norm(w): return re.sub(r"[^\w]", "", w.lower().replace("’", "'"))
script = [w for p in P.PASSAGES for w in p[0].split()]
a = [norm(w) for w in script]; b = [norm(w[0]) for w in rec]
times = [None] * len(script)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1): times[i1 + k] = (rec[j1 + k][1], rec[j1 + k][2])
    elif tag == "replace" and j2 > j1:          # mots reconnus différemment : on répartit le passage
        t0, t1 = rec[j1][1], rec[j2 - 1][2]; n = i2 - i1
        for k in range(n): times[i1 + k] = (t0 + (t1 - t0) * k / n, t0 + (t1 - t0) * (k + 1) / n)
# trous restants : interpolation entre voisins
for i in range(len(times)):
    if times[i] is None:
        prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0.0)
        nxt = next((times[j][0] for j in range(i + 1, len(times)) if times[j]), prev + 0.4)
        times[i] = (prev, max(prev + 0.05, (prev + nxt) / 2))
ok = sum(1 for t in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks() for _ in range(t.size))
words = [{"text": w, "type": "word", "start": round(t[0], 3), "end": round(t[1], 3)} for w, t in zip(script, times)]
json.dump({"words": words, "source": os.path.basename(src)}, open("audio/voix_mots.json", "w"), ensure_ascii=False, indent=1)
print(f"{ok}/{len(script)} mots reconnus exactement ; audio/voix_mots.json écrit. Lance maintenant : python3 build.py")
