import json,sys
from PIL import Image,ImageDraw,ImageFont
S='/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/deco/'
G='/home/claude/mahjmatchmaker-data/assets/mats/gallery/'
D=json.load(open(S+'D117.json'));M=D['mats'];gm=json.load(open(S+'galmap.json'));mi=json.load(open(S+'mi.json'))
keys=json.load(open(S+'sheetkeys.json'))
idx=[int(x) for x in sys.argv[2].split(',')]; out=sys.argv[1]
def path(k): return G+gm[k] if k in gm else mi[k]
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
lp=Image.open(S+'lagoon-pile.jpg').resize((120,120));mp=Image.open(S+'mulberry-pile.jpg').resize((120,120))
C=5;T=320
sh=Image.new('RGB',(C*T,((len(idx)+C-1)//C)*(T+24)),'white');d=ImageDraw.Draw(sh)
for j,n in enumerate(idx):
    k=keys[n];x=(j%C)*T;y=(j//C)*(T+24)
    im=Image.open(path(k)).convert('RGB');im.thumbnail((T-6,T-6));sh.paste(im,(x+3,y+3))
    sh.paste(lp,(x+T-128,y+T-250));sh.paste(mp,(x+T-128,y+T-126))
    d.text((x+4,y+T),f"{n} {M[k]['n'][:30]}",fill='black',font=F)
sh.save(S+out,quality=85)
