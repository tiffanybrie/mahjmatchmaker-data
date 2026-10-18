"""Pick the final HD logo per brand (checked by eye on hd_logos/sheet.jpg) -> scratchpad/hd_logos/final/<brand>.png + map.json."""
import json,os,re
import numpy as np
from PIL import Image
SP='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad';L=SP+'/hd_logos';F=L+'/fetched';O=L+'/final';os.makedirs(O,exist_ok=True)
hd=json.load(open(L+'/report.json'))
SITE={'Bam Bird Boutique':'BamBirdBoutique.png','Amahj':'Amahj.png','Mahj & Vine':'MahjVine.png','Mac + Miller Mahjong':'MacMillerMahjong.png',
'My Fair Mahjong':'MyFairMahjong.png','Tigre de Tartan':'TigredeTartan.png','Peace Love Mahjong':'PeaceLoveMahjong.png','Miss Mahjong':'MissMahjong.png',
'Ozark Mah Jongg':'OzarkMahJongg.png','Ozark Mahjongg':'OzarkMahJongg.png','Mahj & Moon':'MahjMoon.png','Mahj and Moon':'MahjMoon.png','Mahjong Register':'MahjongRegister.png',
'Rebecca Illustrated':'RebeccaIllustrated.png','Royal Mahjong Society':'RoyalMahjongSociety.png','Wren Mats':'WrenMats.png'}
DEEPEN={'Britt Mills'}
SKIP_REPO={'Mahjong Row & Co.'}  # repo file is washed out; the bundled one is better
def trim(im):
    a=np.asarray(im.convert('RGBA'));m=(a[...,3]>16)&(a[...,:3].min(2)<246);ys,xs=np.where(m)
    return im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)) if len(xs) else im
mp={}
for b in sorted(set(hd)|set(SITE)):
    src=None
    if b in SITE and os.path.exists(F+'/'+SITE[b]):src=F+'/'+SITE[b]
    elif hd.get(b) and b not in SKIP_REPO:src=L+'/'+hd[b]['file']
    if not src:continue
    im=trim(Image.open(src).convert('RGBA'))
    if max(im.size)>900:im.thumbnail((900,900),Image.LANCZOS)
    # very pale logos (e.g. Britt Mills' light script) disappear on the card's white chips: deepen them, keeping the hue
    if b in DEEPEN:  # checked by eye: these pale scripts vanish on the white chips; deepen, keeping the hue
        a=np.asarray(im).astype(float);ink=a[...,3]>10;lum=(0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2])/255;Lm=lum[ink].mean();k=0.40/Lm
        a[ink,:3]=np.array([92,104,124]);im=Image.fromarray(a.astype('uint8'),'RGBA');print('deepened',b,round(Lm,2))
    fn=(re.sub(r'[^a-z0-9]','',b.lower()) or 'x')+'.png';im.save(O+'/'+fn,optimize=True);mp[b]={'f':fn,'size':list(im.size),'src':os.path.relpath(src,SP)}
json.dump(mp,open(O+'/map.json','w'),indent=1);print(len(mp));print({k:v['size'] for k,v in mp.items()})
