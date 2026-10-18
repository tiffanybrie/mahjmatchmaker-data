import json,random,os
here=os.path.abspath('.')
pool=[]
F='file:///home/claude/mahjmatchmaker-data/assets/fonts/'
WM='file:///home/claude/mahjmatchmaker-data/assets/brand/mahjmatchmaker-wordmark-notag.png'
FH='file:///home/claude/mahjmatchmaker-data/assets/brand/flame-heart.png'
W,H=1640,856
PW,PH=640,330  # center panel
px,py=(W-PW)//2,(H-PH)//2
panel=f'''<div class="panel" style="left:{px}px;top:{py}px;width:{PW}px;height:{PH}px">
<img class="wm" src="{WM}"><div class="tag">MATCHING MAHJONG TILES, MATS &amp; RACKS</div>
<div class="sub">40+ tile set albums and counting</div><div class="url">mahjmatchmaker.com</div></div>'''
css=f'''@font-face{{font-family:Bitter;font-weight:700;src:url({F}bitter-latin-700-normal.woff2)}}
@font-face{{font-family:Bitter;font-weight:900;src:url({F}bitter-latin-900-normal.woff2)}}
*{{margin:0;box-sizing:border-box}}html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{background:#fff7f4;position:relative;font-family:Bitter,Georgia,serif}}
.c{{position:absolute;border:5px solid #fff;border-radius:10px;box-shadow:0 8px 18px rgba(6,40,90,.28);background-size:cover;background-position:center}}
.panel{{position:absolute;background:#fff;border-radius:28px;border:7px solid #064587;box-shadow:0 0 0 7px #fff,0 0 0 11px #d6608c,0 24px 60px rgba(6,40,90,.35);display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:500}}
.panel .wm{{width:540px}}
.panel .tag{{margin-top:16px;background:#d6608c;color:#fff;font:700 20px Bitter;letter-spacing:.16em;padding:9px 22px;border-radius:6px}}
.panel .sub{{margin-top:20px;font:900 28px Bitter;color:#d6608c}}
.panel .url{{margin-top:8px;font:700 26px Bitter;color:#064587;letter-spacing:.02em}}'''
def page(cards):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{cards}{panel}</body></html>'

D='/home/claude/mahjmatchmaker-data/assets/covers/albums/w800/'
import glob
F={os.path.basename(f)[3:].split('-mahjong')[0]:f for f in glob.glob(D+'*.jpg')}
F['jade']=[f for f in glob.glob(D+'*jade*')][0]

F['sunday']='/home/claude/mahjmatchmaker-data/assets/cards/sunday-tile-set/00-sunday-tile-set-mahjong-tiles-cover.jpg'
F['brownstone']='/home/claude/mahjmatchmaker-data/assets/cards/brownstone-bloom/00-brownstone-bloom-mahjong-tiles-cover.jpg'
F['lilac-soiree']='/home/claude/mahjmatchmaker-data/assets/cards/from-the-vault/lilac-soiree/00-lilac-soiree-mahjong-tiles-cover.jpg'
F['preppy-soiree']='/home/claude/mahjmatchmaker-data/assets/cards/from-the-vault/preppy-soiree/00-preppy-soiree-mahjong-tiles-cover.jpg'
F['shangri-la']='/home/claude/mahjmatchmaker-data/assets/cards/from-the-vault/shangri-la/00-shangri-la-mahjong-tiles-cover.jpg'
F['spring-love']='/home/claude/mahjmatchmaker-data/assets/cards/from-the-vault/spring-love/00-spring-love-mahjong-tiles-cover.jpg'
colors=['petalee','coquette','spring-love','la-fete','amara','glitterville','dandy','nantucket','brownstone','solara','cypress-forest','sierra','papaya-spritz','tortoise','sunset','sorbet','pippa','sunday','limoncello','palm-royale','willow','jade','jasmine','shangri-la','emerald','malachite','gatsby','seabreeze','lagoon','birdie','lola','osler','preppy-soiree','moonlight','lilac-soiree','gemma','luminaire','taylor']
neutral={4:('talulah',0),6:('smith',3),9:('heritage-2-0',0),11:('pearlescent',3)}
random.seed(21)
cw,ch=188,235
xs=[64+i*137 for i in range(12)]
evenR=[40,265,490,715];oddR=[150,375,600,825]
slots=[]
for b,x in enumerate(xs):
    rows=evenR if b%2==0 else oddR
    for r,y in enumerate(rows):
        if 500<x<1140 and 263<y<593: continue
        slots.append((b,r,x,y))
# assign
assign={}
for b,(name,ri) in neutral.items():
    bs=[s for s in slots if s[0]==b]
    assign[bs[min(ri,len(bs)-1)]]=name
ci=0
for s in slots:
    if s in assign: continue
    assign[s]=colors[ci%len(colors)];ci+=1
def swap(a,b):
    ka=[k for k,v in assign.items() if v==a][0];kb=[k for k,v in assign.items() if v==b][0]
    assign[ka],assign[kb]=b,a
swap('shangri-la','jasmine')
swap('petalee','glitterville')
swap('tortoise','solara')
swap('tortoise','sorbet')
swap('brownstone','nantucket')
print('slots',len(slots),'colors used',ci)
html=''
# underlay: tight grid so there is no background showing; each cell takes the cover of the nearest slot
uw,uh=150,188
for gy in range(-40,H+40,uh-6):
    for gx in range(-30,W+30,uw-6):
        cx,cy=gx+uw/2,gy+uh/2
        near=min(slots,key=lambda s:(s[2]-cx)**2+((s[3]-cy)*0.6)**2)
        html+=f'<div style="position:absolute;left:{gx}px;top:{gy}px;width:{uw}px;height:{uh}px;background:url(file://{F[assign[near]]}) center/cover;filter:brightness(.82) saturate(1.05);z-index:0"></div>'
z=list(range(1,len(slots)+1));random.shuffle(z)
NEW={'jade','tortoise','sunday','papaya-spritz','petalee','brownstone','lilac-soiree','preppy-soiree','shangri-la','spring-love'}
z=[zz+(400 if assign[slots[k]] in NEW else 0)+(40 if assign[slots[k]] in ('papaya-spritz','petalee','jade') else 0)+(20 if assign[slots[k]]=='malachite' else 0)+(600 if assign[slots[k]]=='pearlescent' else 0)-(30 if assign[slots[k]]=='lilac-soiree' else 0) for k,zz in enumerate(z)]
# Oct 18 (Tiffany): tuck Petalee's bottom-right corner behind Cypress -> nearest Cypress card to Petalee's lower right sits above it
_pk=[k for k,s in enumerate(slots) if assign[s]=='petalee'][0]; _ps=slots[_pk]
_ck=min([k for k,s in enumerate(slots) if assign[s]=='cypress-forest'],key=lambda k:(slots[k][2]-(_ps[2]+cw*0.6))**2+(slots[k][3]-(_ps[3]+ch*0.6))**2)
z[_ck]=z[_pk]+1
print('petalee',_ps,'z',z[_pk],'cypress',slots[_ck],'z',z[_ck])
for k,s in enumerate(slots):
    b,r,x,y=s;name=assign[s]
    lean=1 if (b+r)%2 else -1
    a=lean*random.uniform(6,13)
    x+=random.uniform(-14,14);y+=random.uniform(-26,26)
    sc=random.uniform(1.0,1.1)*(1.16 if name=='petalee' else 1.14 if name=='pearlescent' else 1.0)
    html+=f'<div class="c" style="left:{x-cw*sc/2:.0f}px;top:{y-ch*sc/2:.0f}px;width:{cw*sc:.0f}px;height:{ch*sc:.0f}px;transform:rotate({a:.1f}deg);background-image:url(file://{F[name]});z-index:{z[k]}"></div>'
open('RF6.html','w').write(page(html))
