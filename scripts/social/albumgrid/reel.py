#!/usr/bin/env python3
"""Album teaser REEL (Tiffany Nov 9 2026: reels for reach; show the depth of each album).
9:16, 10s: title, tile set pops in centre, her top 8 mats pop in around it in album order, CTA.
Text stays in y 270-1440 (safe zone; story link lane 1450-1640 empty). Reuses build.py's trimmed assets.
Usage: reel.py <spec.json> <grids_dir> [slug ...]"""
import json,sys,os,subprocess,shutil
from playwright.sync_api import sync_playwright
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
F=R+'/scripts/social/tileprofile/fonts'
FPS=24; DUR=10.0
def page(sp,d,n):
    cells=['m0','m1','m2','m3','tiles','m4','m5','m6','m7'] if n>=8 else ['m0','m1','tiles','m2']
    cols,cell=(3,290) if n>=8 else (2,420)
    order=['tiles']+[c for c in cells if c!='tiles']
    fs=110 if len(sp['name'])<=14 else 80 if len(sp['name'])<=22 else 62
    g=''.join(f'<div class="cell {"t" if c=="tiles" else ""}" id="{c}" style="width:{cell}px;height:{cell}px"><img src="{d}/{c}.jpg"></div>' for c in cells)
    code=f'Code MAHJMATCH at {sp["brand"]}' if sp.get('code') else f'Shop {sp["brand"]}'
    return f'''<html><head><style>
@font-face{{font-family:Cap;src:url({F}/Caprasimo.ttf)}}@font-face{{font-family:PF;font-style:italic;src:url({F}/playfair-display-latin-400-italic.woff2)}}
@font-face{{font-family:Bit;font-weight:700;src:url({F}/bitter-latin-700-normal.woff2)}}@font-face{{font-family:Bit;font-weight:600;src:url({F}/bitter-latin-600-normal.woff2)}}
body{{margin:0;background:#f6e9df}}.c{{width:1080px;height:1920px;position:relative;overflow:hidden}}
.hd{{position:absolute;top:280px;width:100%;text-align:center}}h1{{font:{fs}px/1 Cap;color:#054689;margin:0}}
.k{{font:700 30px Bit;letter-spacing:5px;color:#c8325f;margin-top:12px}}.s{{font:italic 36px PF;color:#062a55;margin-top:8px}}
.g{{position:absolute;top:{'540' if n>=8 else '560'}px;left:50%;transform:translateX(-50%);display:grid;grid-template-columns:repeat({cols},{cell}px);gap:14px}}
.cell img{{width:100%;height:100%;object-fit:cover;border-radius:16px;display:block;box-shadow:0 8px 22px rgba(6,42,85,.18)}}
.t img{{outline:8px solid #054689;outline-offset:-8px}}
.ft{{position:absolute;top:1495px;width:100%;text-align:center}}
.p{{display:inline-block;background:#c8325f;color:#fff;font:700 34px Bit;padding:16px 36px;border-radius:50px}}
.code{{font:600 30px Bit;color:#062a55;margin-top:14px}}
</style></head><body><div class="c"><div class="hd" id="hd"><h1>{sp["name"]}</h1><div class="k">BY {sp["brand"].upper()}</div>
<div class="s">{"Her top "+str(n)+" holiday matches" if n>1 else ""}</div></div>
<div class="g" id="g">{g}</div><div class="ft" id="ft"><div class="p">See all {sp["count"]} in the album · link in bio</div><div class="code">{code}</div></div></div>
<script>
const order={json.dumps(order)};
function ease(x){{x=Math.min(1,Math.max(0,x));return 1-Math.pow(1-x,3)}}
function back(x){{x=Math.min(1,Math.max(0,x));const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}}
window.step=function(t){{
 const hd=document.getElementById('hd');let a=ease(t/0.6);hd.style.opacity=a;hd.style.transform=`translateY(${{(1-a)*30}}px)`;
 order.forEach((id,i)=>{{const st=0.5+i*0.38;const e=document.getElementById(id);const x=(t-st)/0.45;e.style.opacity=ease(x);e.style.transform=`scale(${{0.6+0.4*back(x)}})`;}});
 const ce=0.5+order.length*0.38+0.3;const f=document.getElementById('ft');const y=ease((t-ce)/0.5);f.style.opacity=y;f.style.transform=`translateY(${{(1-y)*40}}px)`;
 const z=1+0.035*Math.max(0,(t-ce)/({DUR}-ce));document.getElementById('g').style.transform=`translateX(-50%) scale(${{z}})`;
}};</script></body></html>'''
spec={s['slug']:s for s in json.load(open(sys.argv[1]))}; gd=sys.argv[2]
slugs=sys.argv[3:] or list(spec)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    for slug in slugs:
        sp=spec[slug]; d=f'{gd}/{slug}'; n=min(8,len(sp['mats'])); n=8 if n>=8 else 3
        hp=f'{d}/reel.html'; open(hp,'w').write(page(sp,d,n)); pg.goto('file://'+hp); pg.wait_for_timeout(600)
        fr=f'{d}/frames'; shutil.rmtree(fr,ignore_errors=True); os.makedirs(fr)
        for i in range(int(DUR*FPS)):
            pg.evaluate(f'step({i/FPS})'); pg.screenshot(path=f'{fr}/{i:04d}.jpg',type='jpeg',quality=88)
        out=f'{gd}/{slug}-reel.mp4'
        subprocess.run(['ffmpeg','-v','error','-y','-framerate',str(FPS),'-i',f'{fr}/%04d.jpg','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',out],check=True)
        shutil.rmtree(fr); print('ok',out)
    b.close()
