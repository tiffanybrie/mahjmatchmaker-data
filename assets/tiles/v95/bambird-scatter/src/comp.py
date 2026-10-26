import glob, random, sys
from PIL import Image, ImageFilter
TW=104
def load(k):
    F=[Image.open(p) for p in sorted(glob.glob(f'u_{k}_f*.png'))]
    Bk=[Image.open(p) for p in sorted(glob.glob(f'u_{k}_b*.png'))]
    if k=='classic': F=[f for i,f in enumerate(F) if i!=13]; Bk=[b for i,b in enumerate(Bk) if i!=5]
    Bk=[b for b in Bk if b.width>100 and b.height>100]
    norm=lambda t:t.resize((TW,int(t.height*TW/t.width)),Image.LANCZOS)
    return [norm(f) for f in F],[norm(b) for b in Bk]
def build(k,seed):
    F,Bk=load(k);rnd=random.Random(seed)
    W,H=1600,700;c=Image.new('RGBA',(W,H),(255,255,255,255))
    pts=[]
    tries=0
    while tries<20000 and len(pts)<80:
        tries+=1;x=rnd.uniform(20,W-20);y=rnd.uniform(30,H-30)
        if all((x-a)**2+(y-b)**2>140**2 for a,b in pts): pts.append((x,y))
    rnd.shuffle(pts)
    order=sorted(range(len(pts)),key=lambda i:(pts[i][0]-800)**2+(pts[i][1]-330)**2)
    faceset=set(order[0:len(F)*2:2])
    fi=bi=0;fs=F[:];rnd.shuffle(fs);bs=Bk[:]
    for n,(x,y) in enumerate(pts):
        if (n not in faceset) or fi>=len(fs): t=bs[bi%len(bs)];bi+=1;t=t.transpose(Image.ROTATE_180) if bi%2 else t
        else: t=fs[fi];fi+=1
        t=t.rotate(rnd.uniform(-40,40),expand=True,resample=Image.BICUBIC)
        sh=Image.new('RGBA',t.size,(0,0,0,0));al=t.getchannel('A').point(lambda v:int(v*.28));sh.putalpha(al);sh=sh.filter(ImageFilter.GaussianBlur(7))
        px,py=int(x-t.width/2),int(y-t.height/2);c.alpha_composite(sh,(px+5,py+8));c.alpha_composite(t,(px,py))
    return c.convert('RGB')
for k in ('classic','emw'):
    im=build(k,7 if k=='classic' else 11);im.save(f'scatter_{k}.jpg',quality=90)
    im.crop((450,0,1150,700)).save(f'scatter_{k}_circle.jpg')
