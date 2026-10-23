import subprocess, numpy as np
raw = subprocess.run(["ffmpeg","-v","error","-i","public/audio/musique.mp3","-ac","1","-ar","11025","-f","f32le","-"],capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.float32)[11025*5:11025*45]
hop=256; frames=len(x)//hop
env=np.array([np.sum(x[i*hop:(i+1)*hop]**2) for i in range(frames)])
onset=np.maximum(0,np.diff(np.log(env+1e-9)))
onset-=onset.mean()
ac=np.correlate(onset,onset,'full')[len(onset)-1:]
fr=11025/hop
lo,hi=int(fr*60/160),int(fr*60/70)
lag=lo+np.argmax(ac[lo:hi])
print("BPM ~", round(60*fr/lag,1), "beat", round(lag/fr,4))
