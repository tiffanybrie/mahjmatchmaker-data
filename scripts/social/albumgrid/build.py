#!/usr/bin/env python3
"""Album grid post (Tiffany Nov 9 2026): tile set centre, her TOP matches in album order around it,
full mats centred (auto-trimmed, never a corner crop, no props), title = set name + 'by <brand>'.
Usage: build.py <spec.json> <outdir>   spec: [{slug,name,brand,code,count,tiles,mats:[img,...]}]"""
import json,sys,os,numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
F=R+'/scripts/social/tileprofile/fonts'
def trim(src,out,size=640):
    im=Image.open(src).convert('RGB'); a=np.asarray(im).astype(int)
    bg=np.median(np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]),axis=0)
    diff=np.abs(a-bg).sum(2)>45
    rows=np.where(diff.mean(1)>0.08)[0]; cols=np.where(diff.mean(0)>0.08)[0]
    if len(rows)>10 and len(cols)>10: im=im.crop((cols.min(),rows.min(),cols.max()+1,rows.max()+1))
    w,h=im.size; s=max(w,h); pad=int(s*0.03); c=Image.new('RGB',(s+2*pad,s+2*pad),(255,253,250))
    c.paste(im,((s-w)//2+pad,(s-h)//2+pad)); c.resize((size,size),Image.LANCZOS).save(out,quality=92)
def sq(src,out,size=640):
    im=Image.open(src).convert('RGB'); w,h=im.size; s=min(w,h)
    im.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s)).resize((size,size),Image.LANCZOS).save(out,quality=92)
CSS=f'''@font-face{{font-family:Cap;src:url({F}/Caprasimo.ttf)}}
@font-face{{font-family:PF;font-style:italic;src:url({F}/playfair-display-latin-400-italic.woff2)}}
@font-face{{font-family:Bit;font-weight:700;src:url({F}/bitter-latin-700-normal.woff2)}}
@font-face{{font-family:Bit;font-weight:600;src:url({F}/bitter-latin-600-normal.woff2)}}
body{{margin:0}}.c{{width:1080px;height:1350px;background:#f6e9df;display:flex;flex-direction:column;align-items:center;box-sizing:border-box;padding:50px 48px 40px}}
h1{{font:{{fs}}px/1.02 Cap;color:#054689;margin:0 0 10px;text-align:center}}
.k{{font:700 27px Bit;letter-spacing:5px;color:#c8325f}}.s{{font:italic 32px PF;color:#062a55;margin:8px 0 30px}}
.g{{display:grid;gap:14px}}.g img{{width:100%;height:100%;object-fit:cover;border-radius:14px;display:block}}
.t img{{outline:7px solid #054689;outline-offset:-7px}}
.f{{margin-top:auto;text-align:center}}.p{{display:inline-block;background:#c8325f;color:#fff;font:700 27px Bit;padding:13px 30px;border-radius:40px}}
.code{{font:600 25px Bit;color:#062a55;margin-top:14px}}.wm{{height:44px;margin-top:16px}}'''
def html(sp,cells,n):
    cols,cell=(3,288) if n>=8 else (2,420) if n>=3 else (2,420)
    fs=104 if len(sp['name'])<=14 else 76 if len(sp['name'])<=22 else 58
    g=''.join(f'<div class="{"t" if c=="tiles" else ""}" style="width:{cell}px;height:{cell}px"><img src="{c}.jpg"></div>' for c in cells)
    code=f'<div class="code">Code MAHJMATCH at {sp["brand"]}</div>' if sp.get('code') else f'<div class="code">Shop {sp["brand"]}</div>'
    return f'''<html><head><style>{CSS.replace("{fs}",str(fs))}</style></head><body><div class="c">
<h1>{sp["name"]}</h1><div class="k">BY {sp["brand"].upper()}</div><div class="s">{"Her top "+str(n)+" holiday matches" if n>1 else "Her holiday match"}</div>
<div class="g" style="grid-template-columns:repeat({cols},{cell}px)">{g}</div>
<div class="f"><div class="p">See all {sp["count"]} in the album · link in bio</div>{code}<img class="wm" src="{R}/assets/brand/mahjmatchmaker-wordmark-notag.png"></div></div></body></html>'''
spec=json.load(open(sys.argv[1])); out=sys.argv[2]; os.makedirs(out,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=2)
    for sp in spec:
        d=f'{out}/{sp["slug"]}'; os.makedirs(d,exist_ok=True)
        sq(R+'/'+sp['tiles'],f'{d}/tiles.jpg')
        mats=sp['mats'][:8]
        for i,m in enumerate(mats): trim(R+'/'+m,f'{d}/m{i}.jpg')
        n=len(mats)
        if n>=8: cells=['m0','m1','m2','m3','tiles','m4','m5','m6','m7']
        elif n>=3: cells=(['tiles']+[f'm{i}' for i in range(3)]) if n==3 else ['m0','m1','tiles','m2']+([] if n==3 else [])
        else: cells=['tiles']+[f'm{i}' for i in range(n)]
        if n in (4,5,6,7): n=3; cells=['m0','m1','tiles','m2']
        open(f'{d}/p.html','w').write(html(sp,cells,n))
        pg.goto('file://'+f'{d}/p.html'); pg.wait_for_timeout(500)
        assert pg.evaluate("document.querySelector('.c').scrollHeight")<=1350, sp['slug']+' overflows'
        pg.screenshot(path=f'{out}/{sp["slug"]}-grid.jpg',type='jpeg',quality=90)
    b.close()
