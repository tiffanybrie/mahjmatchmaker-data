#!/usr/bin/env python3
"""Reel end frame: Find Your Mat-ch + partner brand logo wall (holiday intro reel end card, year-round version,
Tiffany Nov 10 6:00pm). 1080x1920. Logos = assets/hub/build-2026-11-07/trim (37 code partners, no Mahjong Row / YMI);
Tigre de Tartan left out (sits next to 'use code', affiliate policy). Usage: fym_brands.py <set> <out.png>"""
import sys, os, json, asyncio
from playwright.async_api import async_playwright
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + '/'
name, out = sys.argv[1], sys.argv[2]
F = R + 'scripts/social/tileprofile/fonts/'; u = lambda p: 'file://' + (p if p.startswith('/') else R + p)
L = [x for x in json.load(open(R + 'assets/hub/build-2026-11-07/trim/list.json')) if 'Tigre' not in x['brand']]
m = json.load(open(R + 'config/fym-mats-snapshot.json'))['mats']; depth = f"{(sum(1 for v in m.values() if not v.get('hid')) // 100) * 100:,}"
chips = ''.join(f'<div class="chip"><img src="{u("assets/hub/build-2026-11-07/" + x["file"])}"></div>' for x in L)
html = f'''<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Cap;src:url('{u(F+"Caprasimo.ttf")}')}}
@font-face{{font-family:PF;font-style:italic;font-weight:600;src:url('{u(F+"playfair-display-latin-600-italic.woff2")}')}}
@font-face{{font-family:Bit;font-weight:400;src:url('{u(F+"bitter-latin-400-normal.woff2")}')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#fbf6ef}}
.pill{{display:inline-block;border-radius:999px;font:700 46px Poppins;padding:18px 40px}}
#g{{position:absolute;left:-60px;right:-60px;top:1080px;display:flex;flex-wrap:wrap;gap:18px;justify-content:center}}
.chip{{width:190px;height:120px;background:#fff;border-radius:22px;box-shadow:0 8px 22px rgba(30,70,120,.14);display:flex;align-items:center;justify-content:center}}
.chip img{{max-width:168px;max-height:96px;object-fit:contain}}
</style></head><body>
<img src="{u("assets/brand/flame-heart.png")}" style="position:absolute;left:470px;top:250px;width:140px">
<img src="{u("assets/brand/mahjmatchmaker-wordmark-notag.png")}" style="position:absolute;left:265px;top:420px;width:550px">
<div style="position:absolute;left:0;right:0;top:530px;text-align:center"><span style="display:inline-block;font:400 104px/1 Cap;color:#054689;white-space:nowrap;position:relative">Find <span style="font:italic 600 108px/1 PF;color:#c8325f">Your</span> Mat-ch<span style="position:absolute;font:400 38px Bit;margin-left:4px;margin-top:4px">™</span></span></div>
<div style="position:absolute;left:0;right:0;top:675px;text-align:center;font:italic 600 56px/1.28 PF;color:#054689">Match {name} with {depth}+ mats<br>&amp; racks across brands</div>
<div style="position:absolute;left:0;right:0;top:860px;text-align:center"><span class="pill" style="background:#c8325f;color:#fff">Shop now · use code MAHJMATCH</span></div>
<div style="position:absolute;left:0;right:0;top:985px;text-align:center"><span class="pill" style="background:#fff;border:4px solid #225d36;color:#225d36;font-size:34px;letter-spacing:4px;padding:12px 36px">LINK IN BIO</span></div>
<div id="g">{chips}</div>
</body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        open('/tmp/fymend.html', 'w').write(html); await pg.goto('file:///tmp/fymend.html'); await pg.wait_for_load_state('networkidle')
        await pg.evaluate('document.fonts.ready'); await pg.screenshot(path=out); await b.close()
asyncio.run(main()); print(out, len(L), 'logos')
