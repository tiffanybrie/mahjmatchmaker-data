"""The Beige Felt mat, a recurring joke character ("the beige boring mat"), Tiffany Oct 21.
ONE asset for every appearance (hotline reel Exhibit A polaroid, the swipe deck card, future skits).
Made-up mat: plain beige felt, a dashed stitch border and a thin inner line. Transparent outside the rounded corners.
Usage: python3 scripts/social/characters/beige_felt.py  -> assets/social/characters/beige-felt-mat.png (1200x1200)"""
import asyncio
from playwright.async_api import async_playwright
R = '/home/claude/mahjmatchmaker-data'
OUT = R + '/assets/social/characters/beige-felt-mat.png'
S = 1200; k = S / 640   # drawn on the Oct 19 Exhibit A geometry (640 box), scaled up
SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 640 640">
<defs><filter id="felt" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="{1.6 / k:.3f}" numOctaves="2" seed="4"/>
<feColorMatrix values="0 0 0 0 .78  0 0 0 0 .70  0 0 0 0 .58  0 0 0 .55 0"/><feComposite in2="SourceGraphic" operator="in"/></filter></defs>
<rect width="640" height="640" rx="34" fill="#cdbca3"/><rect width="640" height="640" rx="34" fill="#cdbca3" filter="url(#felt)"/>
<rect x="26" y="26" width="588" height="588" rx="20" fill="none" stroke="#a8957b" stroke-width="5" stroke-dasharray="16 11"/>
<rect x="58" y="58" width="524" height="524" rx="8" fill="none" stroke="#b9a68b" stroke-width="2"/></svg>"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': S, 'height': S})
        await pg.set_content(f'<html><body style="margin:0;background:transparent">{SVG}</body></html>')
        await pg.screenshot(path=OUT, omit_background=True); await b.close()
asyncio.run(main()); print(OUT)
