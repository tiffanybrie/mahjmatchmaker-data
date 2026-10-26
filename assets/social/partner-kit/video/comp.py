"""Compose recorded FYM frames into a 1080x1920 explainer: intro card, floating-in, camera zooms on each tap, step labels, floating-out outro."""
import json,sys,subprocess,bisect,math
from PIL import Image,ImageFilter,ImageDraw
OUT=sys.argv[1]; FPS=30; W,H=1080,1920
R=json.load(open('rec.json')); FT=R['frames']; EV=R['events']
SW,SH=390,844
def ease(x): x=max(0,min(1,x)); return x*x*(3-2*x)
def clampcam(cx,cy,w):
    h=w*16/9; cx=max(w/2,min(SW-w/2,cx)); cy=max(h/2,min(SH-h/2,cy)); return cx,cy,w
FULLW=390; ZW=355
kf=[]
def add(t,cx,cy,w): kf.append((t,)+clampcam(cx,cy,w))
first=[e for e in EV if e['kind']=='pre'][0]
add(0,195,first['rect'][1]+first['rect'][3]/2,FULLW)
last=kf[-1]
evs=EV
for i,e in enumerate(evs):
    k=e['kind']; r=e['rect']
    if k=='full':
        add(e['t'],*kf[-1][1:]); add(e['t']+0.45,195,r[1]+r[3]/2+30,FULLW)
    elif k=='pre':
        tap=evs[i+1]; cy=r[1]+r[3]/2; zc=cy-120 if cy>500 else cy
        add(e['t']-0.05,*kf[-1][1:]); add(e['t']+0.5,195,zc,ZW); add(tap['t']+0.35,195,zc,ZW); add(tap['t']+0.95,195,kf[-4][2] if len(kf)>=4 else cy,FULLW)
    elif k=='card':
        add(e['t'],*kf[-1][1:]); add(e['t']+0.6,195,r[1]+r[3]/2,340)
END=[e for e in EV if e['kind']=='end'][0]['t']
kf.sort(key=lambda x:x[0])
def cam(t):
    if t<=kf[0][0]: return kf[0][1:]
    for a,b in zip(kf,kf[1:]):
        if a[0]<=t<=b[0]:
            u=ease((t-a[0])/max(1e-6,b[0]-a[0])); return tuple(a[j]+(b[j]-a[j])*u for j in (1,2,3))
    return kf[-1][1:]
steps=[(e['t'],e['label']) for e in EV if e['kind']=='step']
lt=[e['t'] for e in EV if e['kind']=='tap'][-1]; steps[-1]=(lt+0.6,steps[-1][1])
LABS=[Image.open(f'lab{i}.png').convert('RGBA') for i in range(len(steps))]
BAND=Image.new('RGBA',(W,240));
for yy in range(240): ImageDraw.Draw(BAND).line([(0,yy),(W,yy)],fill=(250,243,234,int(235*(1-yy/240)**1.3)))
INTRO=Image.open('intro.png').convert('RGB'); OUTRO=Image.open('outro.png').convert('RGBA')
cache={}
def src(t):
    i=max(0,bisect.bisect_right(FT,t)-1)
    if i not in cache:
        if len(cache)>4: cache.clear()
        cache[i]=Image.open('frames/%05d.jpg'%(i+1)).convert('RGB')
    return cache[i]
def view(t):
    cx,cy,w=cam(t); h=w*16/9; s=2
    box=(int((cx-w/2)*s),int((cy-h/2)*s),int((cx+w/2)*s),int((cy+h/2)*s))
    return src(t).crop(box).resize((W,H),Image.LANCZOS)
MASK=None
def floating(img,scale,t_label=None):
    bg=img.resize((W//8,H//8)).filter(ImageFilter.GaussianBlur(3)).resize((W,H),Image.BILINEAR)
    bg=Image.blend(bg,Image.new('RGB',(W,H),(250,243,234)),0.55)
    cw,ch=int(W*scale),int(H*scale); card=img.resize((cw,ch),Image.LANCZOS)
    m=Image.new('L',(cw,ch),0); ImageDraw.Draw(m).rounded_rectangle((0,0,cw-1,ch-1),radius=int(46*scale),fill=255)
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); x=(W-cw)//2; y=int((H-ch)/2 - (H*(1-scale))*0.32)
    d=ImageDraw.Draw(sh); d.rounded_rectangle((x,y+24,x+cw,y+ch+24),radius=int(46*scale),fill=(6,42,85,70)); sh=sh.filter(ImageFilter.GaussianBlur(28))
    out=bg.convert('RGBA'); out.alpha_composite(sh); out.paste(card,(x,y),m); return out
INTRO_T=1.8; FIN=0.7; TAIL=0.9; OUTRO_T=3.0
total=INTRO_T+END+OUTRO_T
p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-movflags','+faststart',OUT],stdin=subprocess.PIPE)
n=int(total*FPS)
for f in range(n):
    T=f/FPS
    if T<INTRO_T-0.35: fr=INTRO.convert('RGBA')
    else:
        t=max(0,T-INTRO_T)
        if t>END: t=END
        v=view(t)
        if T<INTRO_T+FIN:  # floating in
            u=ease((T-(INTRO_T-0.35))/(FIN+0.35)); fr=floating(v,0.80+0.20*u) if u<0.999 else v.convert('RGBA')
            if T<INTRO_T: fr=Image.blend(INTRO.convert('RGBA'),fr,ease((T-(INTRO_T-0.35))/0.35))
        elif T>INTRO_T+END-0.2:
            u=ease((T-(INTRO_T+END-0.2))/0.8); fr=floating(v,1-0.30*u); 
            if u>0: o=OUTRO.copy(); o.putalpha(o.split()[3].point(lambda a:int(a*u))); fr.alpha_composite(o)
        else: fr=v.convert('RGBA')
        # step label
        if INTRO_T+FIN<=T<=INTRO_T+END-0.2:
            si=max([i for i,(st,_) in enumerate(steps) if st<=t] or [0])
            a=min(1,(t-steps[si][0])/0.35) if si>0 else min(1,(T-INTRO_T-FIN)/0.35)
            bd=BAND.copy(); bd.putalpha(bd.split()[3].point(lambda x:int(x*a))); fr.alpha_composite(bd,(0,0)); l=LABS[si].copy(); l.putalpha(l.split()[3].point(lambda x:int(x*a))); fr.alpha_composite(l,(0,0))
    p.stdin.write(fr.convert('RGB').tobytes())
    if f%150==0: print(f,'/',n,flush=True)
p.stdin.close(); p.wait(); print('done',OUT,round(total,1))
