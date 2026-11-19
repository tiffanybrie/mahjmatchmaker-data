import json,re,numpy as np,cv2
from PIL import Image,ImageDraw,ImageFont
S='/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/deco/'
R='/home/claude/mahjmatchmaker-data/'
D=json.load(open(S+'D117.json'));M=D['mats'];p=json.load(open(S+'picks.json'));hd=json.load(open(S+'hd.json'));gm=json.load(open(S+'galmap.json'));mi=json.load(open(S+'mi.json'));mi.update(json.load(open(S+'mi2.json')))
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower().replace('&','and').replace("'",'').replace('–','-')).strip('-')
USE_GAL={'Evergreen'}
out={}
old=json.load(open(S+'matfiles.json'))
for k in sorted({c['key'] for c in p['deco-indigo']}):
    if k in old: out[k]=old[k]; continue
    m=M[k];nm=re.sub(r'\s*\(retired\)','',m['n'])
    src=hd.get(k,'')
    if not src.startswith('/') or nm in USE_GAL: src=R+'assets/mats/gallery/'+gm[k] if k in gm else mi[k]
    im=Image.open(src).convert('RGBA');bg=Image.new('RGBA',im.size,(255,255,255,255));bg.alpha_composite(im);im=bg.convert('RGB')
    a=np.asarray(im).astype(int);H,W=a.shape[:2]
    corners=np.array([a[3,3],a[3,W-4],a[H-4,3],a[H-4,W-4]]);c=np.median(corners,0)
    if corners.std(0).max()<12 and corners.mean()>150:  # plain light background -> crop to largest object
        dif=np.abs(a-c).max(2)>28
        mk=cv2.morphologyEx(dif.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
        n,lab,st,_=cv2.connectedComponentsWithStats(mk);i=1+np.argmax(st[1:,4]);x,y,w,h=st[i,:4]
        im=im.crop((x,y,x+w,y+h))
    im.thumbnail((1400,1400),Image.LANCZOS)
    f=f"assets/colorcards/deco/mats/{slug(m['bn'])}-{slug(nm)}.jpg"
    im.save(R+f,quality=90);out[k]=dict(file=f,size=im.size,src=src.split('/')[-1])
old.update(out);json.dump(old,open(S+'matfiles.json','w'),indent=1)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
ks=list(out);C=8;T=200;sh=Image.new('RGB',(C*T,((len(ks)+C-1)//C)*(T+18)),(200,200,200));d=ImageDraw.Draw(sh)
for j,k in enumerate(ks):
    im=Image.open(R+out[k]['file']);sz=im.size;im.thumbnail((T-6,T-6));x=(j%C)*T;y=(j//C)*(T+18);sh.paste(im,(x+3,y+3));d.text((x+3,y+T-2),f"{M[k]['n'][:16]} {sz[0]}",fill='black',font=F)
sh.save(S+'cropsheet-ind.jpg',quality=82)
