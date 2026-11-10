#!/usr/bin/env python3
"""Reel end frame "get hooked up" (Lagoon reel layout, Tiffany Nov 10 5:59pm), per set, 1080x1920.
Our real logo: blue mahjmatchmaker wordmark + MATCHING MAHJONG TILES, MATS & RACKS (not 'Mahjong Social Club').
Usage: hooked_up.py <set name> <hex accent> <mat png> <tile png> <out.png> [--transparent]"""
import sys, os, asyncio
from playwright.async_api import async_playwright
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + '/'
name, acc, mat, tile, out = sys.argv[1:6]; tr = '--transparent' in sys.argv
F = R + 'scripts/social/tileprofile/fonts/'
u = lambda p: 'file://' + (p if p.startswith('/') else R + p)
corner = lambda: f'''<svg width="210" height="210" viewBox="0 0 210 210"><g fill="none" stroke="{acc}" stroke-width="7" stroke-linecap="square">
<path d="M8 202 V8 H202"/><path d="M30 202 V30 H202"/><path d="M52 120 V52 H120 V88 H88 V70 H70 V120"/></g></svg>'''
heart = lambda fill, stroke='none', sw=0: f'<svg width="96" height="86" viewBox="0 0 24 21.5"><path d="M12 21C5.5 16.1 1.8 12.7 1.8 8.4 1.8 5.4 4.2 3 7.1 3c1.9 0 3.7 1 4.9 2.5C13.2 4 15 3 16.9 3c2.9 0 5.3 2.4 5.3 5.4 0 4.3-3.7 7.7-10.2 12.6z" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/></svg>'
bubble = lambda bg, x, y, flip, inner: (f'<div style="position:absolute;left:{x}px;top:{y}px;width:250px;height:170px">'
   f'<div style="position:absolute;inset:0 0 34px 0;background:{bg};border-radius:30px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 24px rgba(0,0,0,.12)">{inner}</div>'
   f'<div style="position:absolute;bottom:0;{"right" if flip else "left"}:36px;width:0;height:0;border-left:{0 if flip else 46}px solid transparent;border-right:{46 if flip else 0}px solid transparent;border-top:44px solid {bg}"></div></div>')
html = f'''<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Capra;src:url('{u(F+"Caprasimo.ttf")}')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:{"transparent" if tr else "#fff"}}}
.pill{{position:absolute;left:50%;transform:translateX(-50%);background:#f8efe4;border-radius:14px;white-space:nowrap}}
</style></head><body>
<div style="position:absolute;left:30px;top:30px">{corner()}</div>
<div style="position:absolute;right:30px;top:30px;transform:scaleX(-1)">{corner()}</div>
<div style="position:absolute;left:30px;bottom:30px;transform:scaleY(-1)">{corner()}</div>
<div style="position:absolute;right:30px;bottom:30px;transform:scale(-1,-1)">{corner()}</div>
<img src="{u("assets/brand/mahjmatchmaker-wordmark-notag.png")}" style="position:absolute;left:90px;top:330px;width:900px">
<div style="position:absolute;left:0;right:0;top:478px;text-align:center;font:600 30px Poppins;letter-spacing:.17em;color:#054689">MATCHING MAHJONG TILES, MATS &amp; RACKS</div>
<img src="{u(mat)}" style="position:absolute;left:-40px;top:690px;width:440px;transform:rotate(-12deg);filter:drop-shadow(0 18px 26px rgba(0,0,0,.28))">
{bubble("#f2789c", 380, 700, False, heart("#fff"))}
{bubble(acc, 500, 820, True, heart("none", "#fff", 2.2))}
<img src="{u(tile)}" style="position:absolute;right:30px;top:780px;width:250px;transform:rotate(10deg);filter:drop-shadow(0 14px 20px rgba(0,0,0,.25))">
<div class="pill" style="top:1010px;padding:10px 34px 18px;font:400 92px/1 Capra;color:{acc}">get hooked up</div>
<div class="pill" style="top:1420px;padding:14px 26px;font:700 44px Poppins;letter-spacing:.02em;color:{acc}">SEE ALL OF {name.upper()}&rsquo;S MATCHES</div>
</body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        hp = '/tmp/hooked.html'; open(hp, 'w').write(html); await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle')
        await pg.evaluate('document.fonts.ready'); await pg.screenshot(path=out, omit_background=tr); await b.close()
asyncio.run(main()); print(out)
