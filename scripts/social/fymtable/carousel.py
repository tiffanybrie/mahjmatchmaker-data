#!/usr/bin/env python3
"""FYM Table-view carousel (Tiffany Nov 23 7:09-7:19pm): one brand's mats under a tile set in Find Your Mat-ch Table view,
all that brand's own products (brand-share play), pair mat first, last slide = Find Your Mat-ch + album CTA. 1080x1350.
Usage: carousel.py <spec.json> <outdir>"""
import json,sys,os
from playwright.sync_api import sync_playwright
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
F=R+'/scripts/social/tileprofile/fonts'
sp=json.load(open(sys.argv[1]));OUT=sys.argv[2];os.makedirs(OUT,exist_ok=True)
CSS=f'''@font-face{{font-family:Cap;src:url({F}/Caprasimo.ttf)}}@font-face{{font-family:PF;font-style:italic;src:url({F}/playfair-display-latin-400-italic.woff2)}}
@font-face{{font-family:Bit;font-weight:700;src:url({F}/bitter-latin-700-normal.woff2)}}@font-face{{font-family:Bit;font-weight:600;src:url({F}/bitter-latin-600-normal.woff2)}}
body{{margin:0}}.c{{width:1080px;height:1350px;background:#f6e9df;position:relative;overflow:hidden;font-family:Bit}}
.k{{position:absolute;top:56px;width:100%;text-align:center;font:700 26px Bit;letter-spacing:5px;color:#c8325f}}
h1{{position:absolute;top:94px;width:100%;margin:0;text-align:center;font:62px/1.04 Cap;color:#054689}}h1 i{{font:italic 400 66px PF}}
.t{{position:absolute;left:100px;top:262px;width:880px;height:880px;border-radius:22px;overflow:hidden;box-shadow:0 14px 34px rgba(6,42,85,.22)}}.t img{{width:100%;height:100%;display:block}}
.cap{{position:absolute;top:1178px;width:100%;text-align:center;font:italic 38px PF;color:#062a55}}.cap b{{font:700 30px Bit;color:#c8325f;font-style:normal;letter-spacing:1px}}
.n{{position:absolute;right:44px;top:56px;font:600 24px Bit;color:#5a6b85}}'''
def page(body): return f'<html><head><style>{CSS}</style></head><body><div class="c">{body}</div></body></html>'
S=sp['slides'];N=len(S)+1
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox']);pg=b.new_page(viewport={'width':1080,'height':1350})
    for i,s in enumerate(S):
        head=sp['head'] if i==0 else sp.get('head2',sp['head'])
        body=(f'<div class="k">{sp["kicker"]}</div><h1>{head}</h1><div class="n">{i+1}/{N}</div>'
              + (f'<img src="file://{R}/{s["phone"]}" style="position:absolute;left:50%;top:238px;height:1010px;transform:translateX(-50%);filter:drop-shadow(0 18px 30px rgba(6,42,85,.28))"><div class="cap" style="top:1268px">{s["cap"]}</div>' if s.get('phone') else f'<div class="t"><img src="file://{R}/{s["img"]}"></div><div class="cap">{s["cap"]}</div>'))
        h=f'{OUT}/s{i+1}.html';open(h,'w').write(page(body));pg.goto('file://'+h);pg.wait_for_timeout(700)
        pg.screenshot(path=f'{OUT}/{i+1}.jpg',type='jpeg',quality=92)
    e=sp['end'];body=(f'<div class="k">{sp["kicker"]}</div><div class="n">{N}/{N}</div>'
       f'<div style="position:absolute;top:210px;width:100%;text-align:center"><div style="font:86px/1.02 Cap;color:#054689">{e["h"]}</div>'
       f'<div style="font:italic 42px/1.3 PF;color:#062a55;margin:34px 90px 0">{e["p"]}</div>'
       f'<div style="display:inline-block;margin-top:56px;background:#c8325f;color:#fff;font:700 36px Bit;padding:22px 46px;border-radius:60px">{e["btn"]}</div>'
       f'<div style="font:600 32px Bit;color:#062a55;margin-top:40px">{e["code"]}</div>'
       f'<img src="file://{R}/assets/brand/mahjmatchmaker-wordmark-notag.png" style="width:420px;margin-top:120px"></div>')
    h=f'{OUT}/s{N}.html';open(h,'w').write(page(body));pg.goto('file://'+h);pg.wait_for_timeout(700);pg.screenshot(path=f'{OUT}/{N}.jpg',type='jpeg',quality=92)
    b.close()
print('ok',N)
