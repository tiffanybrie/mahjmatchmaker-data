import json,os,math
H=os.path.dirname(os.path.abspath(__file__))
def leaf():
    n=5;pts_u=[];pts_l=[]
    for i in range(n+1):
        x=100*i/n;w=20*math.sin(math.pi*i/n)
        pts_u.append((x,-w));pts_l.append((x,w))
    d=f"M0,0"
    for i in range(1,n+1):
        (x0,y0),(x1,y1)=pts_u[i-1],pts_u[i];cx,cy=(x0+x1)/2,(y0+y1)/2*0.55
        d+=f" Q{cx:.1f},{cy:.1f} {x1:.1f},{y1:.1f}"
    for i in range(n-1,-1,-1):
        (x0,y0),(x1,y1)=pts_l[i+1],pts_l[i];cx,cy=(x0+x1)/2,(y0+y1)/2*0.55
        d+=f" Q{cx:.1f},{cy:.1f} {x1:.1f},{y1:.1f}"
    return d+"Z"
LEAF=leaf()
def holly(size=170,flip=1):
    g=lambda a,c: f'<g transform="rotate({a} 0 0)"><path d="{LEAF}" fill="{c}" stroke="#123d22" stroke-width="2"/><path d="M4,0 L92,0" stroke="#7fb58a" stroke-width="2.2" fill="none" opacity=".8"/></g>'
    return f'''<svg viewBox="-110 -110 220 220" width="{size}" height="{size}" style="transform:scaleX({flip})">{g(-150,'#1d6b3a')}{g(-35,'#25804a')}{g(-95,'#2e8f52')}
<circle cx="-6" cy="6" r="13" fill="#c8102e" stroke="#7a0a1c" stroke-width="2"/><circle cx="14" cy="-2" r="13" fill="#d81b35" stroke="#7a0a1c" stroke-width="2"/><circle cx="2" cy="-18" r="13" fill="#c8102e" stroke="#7a0a1c" stroke-width="2"/>
<circle cx="-10" cy="2" r="4" fill="#fff" opacity=".7"/><circle cx="10" cy="-6" r="4" fill="#fff" opacity=".7"/><circle cx="-2" cy="-22" r="4" fill="#fff" opacity=".7"/></svg>'''
BOW='''<svg viewBox="0 0 220 150" width="{w}"><defs><linearGradient id="rb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e32642"/><stop offset="1" stop-color="#a50d26"/></linearGradient></defs>
<path d="M104 70 L70 148 L88 138 L98 150 L112 74Z M116 70 L150 148 L132 138 L122 150 L108 74Z" fill="#a50d26"/>
<path d="M110 62 C70 0 8 10 14 58 C20 104 78 96 110 62Z" fill="url(#rb)" stroke="#7a0a1c" stroke-width="3"/><path d="M110 62 C150 0 212 10 206 58 C200 104 142 96 110 62Z" fill="url(#rb)" stroke="#7a0a1c" stroke-width="3"/>
<path d="M104 62 C80 30 44 30 38 54" stroke="#ff8091" stroke-width="5" fill="none" opacity=".6"/><path d="M116 62 C140 30 176 30 182 54" stroke="#ff8091" stroke-width="5" fill="none" opacity=".6"/>
<ellipse cx="110" cy="64" rx="20" ry="18" fill="#d81b35" stroke="#7a0a1c" stroke-width="3"/></svg>'''
SETS=[
 ('dear-santa','Dear Santa','','ar',130,'23,87,58','50% 50%','cover'),
 ('rackin-rudolph',"Rackin'<br>Rudolph",'','hiphip',120,'163,25,46','60% 40%','cover'),
 ('holly-jolly-red','Holly Jolly','Rudolph Red','bam',110,'206,32,41','50% 50%','cover'),
 ('holly-jolly-green','Holly Jolly','Grinch Green','bam',110,'38,150,64','50% 50%','cover'),
 ('holly-jolly-pink','Holly Jolly','Sugarplum Pink','bam',110,'226,128,160','50% 50%','cover'),
 ('tinselle-emerald','Tinselle','Emerald Green','virora',66,'14,98,60','50% 50%','cover'),
 ('tinselle-ruby','Tinselle','Ruby Red','virora',66,'150,18,36','50% 50%','cover'),
 ('nivalee-blue','Nivalee','Glacier Blue','virora',66,'58,165,168','50% 50%','cover'),
 ('nutcracker-ballet','Nutcracker<br>Ballet','','squad',110,'214,120,140','50% 50%','cover'),
 ('december-1994','December<br>1994','','sunday',84,'120,26,38','45% 4%','auto 128%'),
 ('cmc-apres-ski','Après Ski<br>Club','','cmc',130,'24,120,140','50% 50%','cover'),
]
FONT='<link href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Montserrat:wght@700&display=block" rel="stylesheet">'
def page(s,var):
    i,t,cw,lg,lh,rgb,foc,sz=s
    fs=104 if '<br>' in t else 118
    tag=f'<div class="tag"><img src="{H}/bl_{lg}.png" style="height:{lh}px"></div>'
    extra='';pstyle=''
    if var=='a':
        extra=(f'<div class="h tl">{holly(190)}</div><div class="h tr">{holly(190,-1)}</div><div class="h bl">{holly(170)}</div><div class="h br">{holly(170,-1)}</div>'
               '')
        frame=f'<div class="f" style="background:url({H}/frame2.png)"></div>'
    else:
        pstyle=f'box-shadow:0 0 0 14px transparent;outline:14px solid transparent;'
        extra=(f'<div class="stripe"></div><div class="rib v"></div><div class="bow2">{BOW.format(w=230)}</div>')
        frame=f'<div class="f gold"></div>'
    return f'''<html><head>{FONT}<style>
body{{margin:0;width:1080px;height:1350px;overflow:hidden;background:#000;position:relative}}
.bg{{position:absolute;inset:0;background:url("{H}/bg_{i}.jpg") {foc}/{sz} no-repeat}}
.p{{position:absolute;left:87px;top:281px;width:906px;height:788px;background:rgba({rgb},.88);{pstyle}}}
.f{{position:absolute;left:87px;top:281px;width:906px;height:788px}}
.f.gold{{background:url({H}/frame2_gold.png)}}
.c{{position:absolute;left:87px;top:{300 if var=='a' else 300}px;width:906px;height:620px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;color:#fbf6ee;text-align:center}}
.tag{{background:#fbf6ee;border-radius:14px;padding:12px 22px;box-shadow:0 4px 14px rgba(0,0,0,.25);display:flex;align-items:center;justify-content:center;position:relative}}
.tag img{{display:block}}
h1{{font:400 {fs}px/1.02 Caprasimo;margin:10px 0 0;text-shadow:0 2px 8px rgba(0,0,0,.18)}}
.cw{{font:700 30px Montserrat;letter-spacing:.3em;margin-left:.3em;margin-top:4px}}
.our{{position:absolute;left:50%;transform:translateX(-50%);top:950px;width:500px}}
.h{{position:absolute}}.tl{{left:22px;top:212px}}.tr{{right:22px;top:212px}}.bl{{left:30px;top:1000px}}.br{{right:30px;top:1000px}}
.bow{{position:absolute;left:440px;top:206px}}
.stripe{{position:absolute;left:73px;top:267px;width:906px;height:788px;border:14px solid transparent;border-image:repeating-linear-gradient(45deg,#fbf6ee 0 12px,#c8102e 12px 24px) 14;z-index:1}}
.stripe+.rib{{}}
.rib.v{{display:none}}
.bow2{{position:absolute;right:40px;top:196px;transform:rotate(14deg)}}
.p,.f,.c,.our{{z-index:1}}.bow,.bow2,.h{{z-index:2}}
</style></head><body><div class="bg"></div>{extra if var=='b' else ''}<div class="p"></div>{frame}
<div class="c">{tag}<h1>{t}<br>Tiles</h1>{f'<div class="cw">{cw.upper()}</div>' if cw else ''}</div>
<img class="our" src="{H}/ourlogo.png">{extra if var=='a' else ''}</body></html>'''
os.makedirs(H+'/html2',exist_ok=True)
for s in SETS:
    for v in 'ab': open(f'{H}/html2/{s[0]}__{v}.html','w').write(page(s,v))
print('ok')
