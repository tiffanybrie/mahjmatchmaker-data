import json
from PIL import Image,ImageDraw,ImageFont
S='/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/deco/'
G='/home/claude/mahjmatchmaker-data/assets/mats/gallery/'
D=json.load(open(S+'D117.json'));M=D['mats'];P=json.load(open(S+'pool.json'));gm=json.load(open(S+'galmap.json'));mi=json.load(open(S+'mi.json'))
sc=json.load(open(S+'scores.json'))
keys=sorted(set(P['lag'])|set(P['mul']),key=lambda k:(M[k]['bn'],M[k]['n']))
def path(k):
    if k in gm: return G+gm[k]
    v=mi.get(k); return v if v and v.startswith('/') else None
keys=[k for k in keys if path(k)]
json.dump(keys,open(S+'sheetkeys.json','w'))
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
C,Rw,T=8,6,200
lp=Image.open(S+'lagoon-pile.jpg').resize((150,150));mp=Image.open(S+'mulberry-pile.jpg').resize((150,150))
for si in range(0,len(keys),C*Rw):
    sh=Image.new('RGB',(C*T,170+Rw*(T+34)),'white');d=ImageDraw.Draw(sh)
    sh.paste(lp,(10,10));sh.paste(mp,(170,10))
    for j,k in enumerate(keys[si:si+C*Rw]):
        n=si+j;x=(j%C)*T;y=170+(j//C)*(T+34)
        try:
            im=Image.open(path(k)).convert('RGB');im.thumbnail((T-8,T-8));sh.paste(im,(x+4+(T-8-im.width)//2,y+4))
        except Exception as e: d.text((x+5,y+50),'ERR',fill='red',font=F)
        d.text((x+4,y+T-2),f"{n} {M[k]['n'][:24]}",fill='black',font=F);d.text((x+4,y+T+14),M[k]['bn'][:26],fill='gray',font=F)
    sh.save(S+f'sh{si//(C*Rw):02d}.jpg',quality=82)
print(len(keys))
