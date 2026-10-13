# Synthesize a soft UI click at each decision time (wav), then mux with the video.
import json,sys,wave,struct,math,random
meta=json.load(open(sys.argv[1]));out=sys.argv[2];sr=44100;n=int(meta['dur']*sr)
buf=[0.0]*n;random.seed(3)
def click(t0,pitch):
    s=int(t0*sr)
    for i in range(int(0.06*sr)):
        if s+i>=n:break
        e=math.exp(-i/(0.008*sr))
        buf[s+i]+=0.55*e*math.sin(2*math.pi*pitch*i/sr)+0.15*e*(random.random()*2-1)
def whoosh(t0):
    s=int(t0*sr);L=int(0.35*sr)
    for i in range(L):
        if s+i>=n:break
        e=math.sin(math.pi*i/L)**2*0.10
        buf[s+i]+=e*(random.random()*2-1)
for (s,d,o) in meta['T']:
    click(d,1800);click(d+0.05,1200);whoosh(o)
end=meta['T'][-1][2]+0.55
for k in range(3):click(end+0.6+k*0.12,2200+k*300)
with wave.open(out,'w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
    w.writeframes(b''.join(struct.pack('<h',int(max(-1,min(1,x))*30000)) for x in buf))
