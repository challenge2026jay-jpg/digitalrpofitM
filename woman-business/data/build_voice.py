"""Insère des respirations dans la voix off ElevenLabs et décale l'alignement mot par mot.
Points de coupe = milieu des silences réels mesurés (ffmpeg silencedetect, -38 dB)."""
import json, subprocess

SRC = "public/audio/voix_elevenlabs_originale.mp3"
OUT = "public/audio/voix_off_finale.wav"
# (point de coupe en s, pause ajoutée en s)
PAUSES = [
    (6.07, 0.20),   # après la question d'accroche
    (14.72, 0.40),  # après « freiner ton projet. » : avant la présentation
    (19.04, 0.15),  # après « Woman Business. »
    (27.77, 0.40),  # après « en RDC. » : passage à WhatsApp
    (41.64, 0.15),  # avant « L'objectif »
    (45.27, 0.40),  # après « outil commercial. » : passage à l'IA
    (62.10, 0.25),  # après « commandes à l'étranger. »
    (70.90, 0.50),  # après « Instagram. » : avant l'appel à l'action
    (75.99, 0.20),  # après la question finale
    (80.52, 0.35),  # avant la signature
]

parts, fc, t0 = [], [], 0.0
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
    if w.get("type") != "word" or w["text"] in ("?", ":"):
        continue
    shift = sum(pad for cut, pad in PAUSES if w["start"] > cut)
    out.append({"text": w["text"], "start": round(w["start"] + shift, 3), "end": round(w["end"] + shift, 3)})
json.dump(out, open("src/words.json", "w"), ensure_ascii=False, indent=1)
print(len(out), "mots ; fin", out[-1]["end"])
