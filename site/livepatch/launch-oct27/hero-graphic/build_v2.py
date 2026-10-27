"""Homepage hero v2 (Tiffany Oct 27 2:29pm): the match-card fan is OLD direction (match cards = albums). The hero now shows the
Find Your Mat-ch APP on white phones (same trio as /links + launch reel: home, swipe deck, match card), with ✕ / ♥ under it.
Same two files / same slots as build.py, so swapping is: upload new desktop image to the section + new mobile URL in the Custom CSS.
Usage: python3 build_v2.py [bg|preview]"""
import os, sys, asyncio, pathlib
HERE = pathlib.Path(__file__).resolve().parent; REPO = HERE.parents[3]
TRIO = REPO / 'assets/social/mockups-oct26/fym-phones-trio-malachite-white.png'
PINK, HEART, BLUSH, PCREAM, CREAM = '#f56b8b', '#f56c8c', '#f7b6c8', '#fbe3ea', '#faf3ea'
def html(kind):
    if kind == 'desktop':
        W, H, tw, cx, top = 2400, 1500, 960, 1690, 230
        blobs = f'<i style="left:1000px;top:90px;width:1500px;height:1500px;background:{PCREAM}"></i><i style="left:-260px;top:1080px;width:700px;height:700px;background:{PCREAM};opacity:.75"></i><i style="left:900px;top:-330px;width:420px;height:420px;background:#fdeef2"></i>'
        hearts = [(1120, 300, 54, -14, BLUSH), (2280, 230, 70, 12, BLUSH), (2290, 1200, 48, 18, HEART), (1180, 1240, 40, -8, BLUSH)]
    else:
        W, H, tw, cx, top = 1170, 3900, 1110, 585, 2640
        blobs = f'<i style="left:-420px;top:2380px;width:2000px;height:2000px;background:{PCREAM}"></i><i style="left:780px;top:300px;width:620px;height:620px;background:#fdeef2"></i><i style="left:-260px;top:1300px;width:520px;height:520px;background:#fdeef2"></i>'
        hearts = [(70, 2560, 60, -14, BLUSH), (1030, 2540, 74, 12, BLUSH), (1050, 3700, 50, 18, HEART), (60, 3720, 40, -8, HEART)]
    th = tw * 2000 / 2160; bs = tw * .12
    hs = ''.join(f'<b style="left:{x}px;top:{y}px;font-size:{s}px;transform:rotate({r}deg);color:{c}">&#9829;</b>' for x, y, s, r, c in hearts)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0}}body{{width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{CREAM}}}
i{{position:absolute;border-radius:50%;display:block}}b{{position:absolute;font-weight:400;line-height:1;opacity:.9}}
.t{{position:absolute;left:{cx-tw/2}px;top:{top}px;width:{tw}px}}
.sw{{position:absolute;left:{cx}px;top:{top+th-bs*.35:.0f}px;transform:translateX(-50%);display:flex;gap:{bs*.55:.0f}px}}
.sw span{{width:{bs:.0f}px;height:{bs:.0f}px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 34px rgba(6,42,85,.24);font-family:Arial,sans-serif}}
.sw .no{{color:#8d97ad;font-size:{bs*.48:.0f}px}}.sw .yes{{color:#fff;background:{HEART};font-size:{bs*.52:.0f}px}}
</style></head><body>{blobs}{hs}<img class="t" src="{TRIO.as_uri()}"><div class="sw"><span class="no">&#10005;</span><span class="yes">&#9829;</span></div></body></html>''', W, H
async def bg():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for kind in ('desktop', 'mobile'):
            h, W, H = html(kind); f = pathlib.Path('/tmp') / f'hero2-{kind}.html'; f.write_text(h)
            pg = await b.new_page(viewport={'width': W, 'height': H}); await pg.goto(f.as_uri()); await pg.wait_for_timeout(600)
            out = HERE / f'fym-app-mahjong-hero-{kind}.jpg'; await pg.screenshot(path=str(out), type='jpeg', quality=88); print(out, os.path.getsize(out) // 1024, 'KB'); await pg.close()
        await b.close()
SEC = '69b1d01489d0f8016ee3d59f'
async def preview():
    from playwright.async_api import async_playwright
    out = HERE / 'previews'; out.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h in ((390, 844), (1280, 800)):
            pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2 if w < 500 else 1)
            await pg.route('https://hero.local/*', lambda r: r.fulfill(path=str(HERE / r.request.url.rsplit('/', 1)[1]), content_type='image/jpeg'))
            await pg.goto('https://www.mahjmatchmaker.com/?v=hero2', wait_until='networkidle', timeout=90000); await pg.wait_for_timeout(1200)
            sec = await pg.evaluate('''([sec]) => { const img = document.querySelector(`[data-section-id="${sec}"] .section-background img`);
              img.removeAttribute('srcset'); img.src = 'https://hero.local/fym-app-mahjong-hero-desktop.jpg';
              const s = document.createElement('style'); s.textContent = `@media (max-width:1199px){[data-section-id="${sec}"] .section-background{background:#faf3ea url(https://hero.local/fym-app-mahjong-hero-mobile.jpg) center bottom/cover no-repeat!important}}`; document.head.appendChild(s);
              const b = document.querySelector(`[data-section-id="${sec}"]`).getBoundingClientRect(); return b.y + b.height + scrollY }''', [SEC])
            await pg.wait_for_timeout(1500)
            await pg.screenshot(path=str(out / f'hero-app-{w}.png'), full_page=True, clip={'x': 0, 'y': 0, 'width': w, 'height': max(h, sec)}); await pg.close()
        await b.close()
if __name__ == '__main__':
    w = sys.argv[1] if len(sys.argv) > 1 else 'bg'
    asyncio.run(bg() if w == 'bg' else preview())
