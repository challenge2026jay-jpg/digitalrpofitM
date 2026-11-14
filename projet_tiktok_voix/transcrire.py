import subprocess, numpy as np, json
from faster_whisper import WhisperModel
pcm = subprocess.check_output(["ffmpeg","-v","error","-i","audio/voix_off_tik_tok.wav","-ac","1","-ar","16000","-f","f32le","-"])
m = WhisperModel("medium", device="cpu", compute_type="int8")
segs,_ = m.transcribe(np.frombuffer(pcm,np.float32), language="fr", word_timestamps=True, beam_size=5,
     initial_prompt="TikTok, Instagram, Facebook, WhatsApp, YouTube, Alibaba, AliExpress, Temu, Shein, Chariow, produits digitaux, business en ligne, vendre en ligne.")
words=[]
for s in segs:
    print(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text}", flush=True)
    for w in s.words: words.append({"text":w.word.strip(),"start":round(w.start,3),"end":round(w.end,3),"p":round(w.probability,3)})
json.dump({"words":words}, open("audio/transcription.json","w"), ensure_ascii=False, indent=1)
print(len(words),"mots", flush=True)
