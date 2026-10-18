"""HD brand logos for the FYM match card (Oct 18): largest clean file per brand from builder/logos and
assets/brand/partner-logos (the bundled ones are 63-90px tall and pixelate at 2x). Writes scratchpad/hd_logos/."""
import json,os,re,glob,unicodedata
import numpy as np
from PIL import Image
SP='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad';REPO='/home/claude/mahjmatchmaker-data/'
OUT=SP+'/hd_logos';os.makedirs(OUT,exist_ok=True)
s=open(SP+'/fymfix2/build/index.html').read();i=s.index('const D=')+8;j=s.index('\n',i);D=json.loads(s[i:j].rstrip()[:-1])
norm=lambda t:re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower())
brands=set(D['logos'])|{x['bn'] for k in ('tiles','mats','racks') for x in D[k].values() if x.get('bn')}
ALIAS={'Anders Ruff':['partner-logos/ar.png'],"Bam! Let's Mahjong":['partner-logos/bam.png'],'Charleston Mahjong Club':['partner-logos/cmc.png'],
 'Hip Hip Mahjong':['partner-logos/hiphip.png'],"Let's Be Besties":['partner-logos/lets-be-besties.png'],'Mahj Squad':['partner-logos/squad.png'],
 'Sunday Mahjong':['partner-logos/sunday.png'],'Virora Mahjong':['partner-logos/virora.png'],'Virora':['partner-logos/virora.png'],
 'ours':['../../builder/logos/ours.png'],'icon':['flame-heart.png']}
FILES=[f for f in glob.glob(REPO+'builder/logos/*.png') if not os.path.basename(f).startswith('n_')]
def trim(im):
    a=np.asarray(im.convert('RGBA'));m=(a[...,3]>16)&(a[...,:3].min(2)<246)
    ys,xs=np.where(m);return im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)) if len(xs) else im
rep={}
for b in sorted(brands|{'ours','icon'}):
    c=[REPO+'assets/brand/'+p for p in ALIAS.get(b,[])]
    nb=norm(b)
    if nb:c+=[f for f in FILES if norm(os.path.basename(f).rsplit('_',1)[0])==nb]
    c=[f for f in c if os.path.exists(f)]
    if not c:rep[b]=None;continue
    best=max(c,key=lambda f:Image.open(f).size[0]*Image.open(f).size[1])
    im=trim(Image.open(best).convert('RGBA'))
    if max(im.size)>900:im.thumbnail((900,900),Image.LANCZOS)
    fn=nb[:30] or 'x';fn=(fn if b not in('ours','icon') else b)+'.png';im.save(os.path.join(OUT,fn),optimize=True)
    rep[b]={'file':fn,'src':best[len(REPO):],'size':list(im.size)}
json.dump(rep,open(OUT+'/report.json','w'),indent=1)
for b,v in rep.items():print(b,v)
