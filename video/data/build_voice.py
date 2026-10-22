"""Insère les pauses de direction dans la voix off ElevenLabs et décale l'alignement mot par mot.
Points de coupe = milieu des silences réels mesurés (ffmpeg silencedetect)."""
import json, subprocess

SRC = "public/audio/voix_elevenlabs_originale.mp3"
OUT = "public/audio/voix_off_finale.wav"
# (point de coupe en s, pause ajoutée en s)
PAUSES = [
    (4.21, 0.15),   # après « dropshipping. »
    (9.12, 0.35),   # après le blocage du compte : légère pause
    (11.40, 0.90),  # après « se sent nulle. » : pause marquée
    (17.35, 0.30),  # après le doute lié au pays
    (24.07, 0.30),  # après « notre situation. »
    (33.25, 0.20),  # après « sont acceptés. »
    (36.67, 0.20),  # après « avant de payer. »
    (38.66, 0.50),  # avant la phrase clé
    (41.40, 0.90),  # après « tu n'es pas capable. » : pause avant la suite
    (49.13, 0.30),  # avant la conclusion
]

parts, inputs, t0 = [], [], 0.0
fc = []
for i, (cut, pad) in enumerate(PAUSES):
    fc.append(f"[0:a]atrim={t0}:{cut},asetpts=PTS-STARTPTS[s{i}]")
    fc.append(f"anullsrc=r=44100:cl=mono,atrim=0:{pad}[p{i}]")
    parts += [f"[s{i}]", f"[p{i}]"]
    t0 = cut
n = len(PAUSES)
fc.append(f"[0:a]atrim={t0},asetpts=PTS-STARTPTS[s{n}]")
parts.append(f"[s{n}]")
fc.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1,aresample=48000[out]")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", SRC,
                "-filter_complex", ";".join(fc), "-map", "[out]", "-ac", "1", OUT], check=True)

words = json.load(open("data/words_raw.json"))["words"]
out = []
for w in words:
    if w.get("type") != "word":
        continue
    shift = sum(pad for cut, pad in PAUSES if w["start"] > cut)
    out.append({"text": w["text"], "start": round(w["start"] + shift, 3), "end": round(w["end"] + shift, 3)})
json.dump(out, open("src/words.json", "w"), ensure_ascii=False, indent=1)
print(len(out), "mots ; fin", out[-1]["end"])
