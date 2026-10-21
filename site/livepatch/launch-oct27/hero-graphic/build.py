"""Launch-day homepage hero (Tue Oct 27): the nav-plan "It's a mat-ch!" match-card fan, brought up to date (Oct 21).

Design source: site/livepatch/nav-plan (mock/gen.py FAN, README steps 4-5, rts/01 + 02), shown to Tiffany in Ready to Ship.
Changes vs that draft: cream/blush brand background instead of the LoveShackFancy Coquette photo; bigger fan (it is the
star); live Papaya card (Press for Mahjong, Beechwood racks, fbf7ec9) in front; live Heritage 2.0 + Isla card (photo
check OK, "10% OFF" line cut off) and live Coquette + Fleur card behind; stamp "It's a mat-ch!"; no % anywhere.

The headline, line, button and code line stay LIVE Squarespace text; only the fan + background are an image.
  bg-desktop.jpg  2400x1500, used >=1100px wide (fan on the right, text column on the left kept clear)
  bg-mobile.jpg   1170x3900, used <1100px (fan at the bottom, text stacks above it)

Usage: PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR=/dev/shm python3 build.py [bg|preview|all]
"""
import os, sys, asyncio, pathlib
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
IMG = REPO / 'site/livepatch/nav-plan/mock/img'
FONTS = REPO / 'assets/fonts'

NAVY, NAVY2, PINK, HEART, BLUSH, PCREAM, CREAM = '#054689', '#062a55', '#f56b8b', '#f56c8c', '#f7b6c8', '#fbe3ea', '#faf3ea'

def bg_html(kind):
    if kind == 'desktop':
        W, H = 2400, 1500
        fan_cx, fan_top, cw, dx, side_scale = 1690, 370, 640, 300, .86
        blobs = f'''<i style="left:1000px;top:90px;width:1500px;height:1500px;background:{PCREAM}"></i>
<i style="left:-260px;top:1080px;width:700px;height:700px;background:{PCREAM};opacity:.75"></i>
<i style="left:900px;top:-330px;width:420px;height:420px;background:#fdeef2"></i>'''
    else:
        W, H = 1170, 3900
        fan_cx, fan_top, cw, dx, side_scale = 585, 2780, 600, 240, .84
        blobs = f'''<i style="left:-420px;top:2380px;width:2000px;height:2000px;background:{PCREAM}"></i>
<i style="left:780px;top:300px;width:620px;height:620px;background:#fdeef2"></i>
<i style="left:-260px;top:1300px;width:520px;height:520px;background:#fdeef2"></i>'''
    ch = cw * 1350 / 1080
    hearts = ''.join(f'<b style="left:{x}px;top:{y}px;font-size:{s}px;transform:rotate({r}deg);color:{c}">&#9829;</b>'
                     for x, y, s, r, c in (HEARTS_D if kind == 'desktop' else HEARTS_M))
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Shrikhand;src:url({FONTS.as_uri()}/shrikhand-latin-400-normal.woff2)}}
html,body{{margin:0}}body{{width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{CREAM}}}
i{{position:absolute;border-radius:50%;display:block}}
b{{position:absolute;font-weight:400;line-height:1;opacity:.9}}
.c{{position:absolute;top:{fan_top}px;left:{fan_cx - cw / 2}px;width:{cw}px;border-radius:26px;overflow:hidden;border:11px solid #fff;background:#fff;
   box-shadow:0 30px 70px rgba(6,42,85,.26),0 6px 16px rgba(6,42,85,.12)}}
.c img{{display:block;width:100%}}
.c1{{transform:translateX(-{dx}px) translateY(70px) rotate(-11deg) scale({side_scale})}}
.c2{{transform:translateX({dx}px) translateY(70px) rotate(10deg) scale({side_scale})}}
.c3{{transform:rotate(-1.5deg);z-index:2}}
.tag{{position:absolute;z-index:4;left:{fan_cx}px;top:{fan_top - 38}px;transform:translate(-50%,-50%) rotate(-5deg);font-family:Shrikhand;font-size:{cw * .1:.0f}px;
   color:#fff;background:{PINK};padding:{cw * .018:.0f}px {cw * .065:.0f}px {cw * .03:.0f}px;border-radius:22px;white-space:nowrap;box-shadow:0 14px 34px rgba(214,83,122,.42)}}
.sw{{position:absolute;z-index:4;left:{fan_cx}px;top:{fan_top + ch + 28}px;transform:translateX(-50%);display:flex;gap:{cw * .085:.0f}px}}
.sw span{{width:{cw * .21:.0f}px;height:{cw * .21:.0f}px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;
   box-shadow:0 14px 34px rgba(6,42,85,.24);font-family:Arial,sans-serif}}
.sw .no{{color:#8d97ad;font-size:{cw * .1:.0f}px}}.sw .yes{{color:{HEART};font-size:{cw * .11:.0f}px}}
</style></head><body>{blobs}{hearts}
<div class="c c1"><img src="{(IMG / 'card-coquette.jpg').as_uri()}"></div>
<div class="c c2"><img src="{(IMG / 'card-heritage2.jpg').as_uri()}"></div>
<div class="c c3"><img src="{(IMG / 'card-papaya.jpg').as_uri()}"></div>
<div class="tag">It&rsquo;s a mat-ch!</div>
<div class="sw"><span class="no">&#10005;</span><span class="yes">&#9829;</span></div>
</body></html>''', W, H

# a few soft hearts around the fan (never over the text column)
HEARTS_D = [(1180, 300, 54, -14, BLUSH), (2230, 230, 70, 12, BLUSH), (2290, 1180, 48, 18, HEART), (1250, 1270, 40, -8, BLUSH), (1990, 140, 36, 6, HEART)]
HEARTS_M = [(90, 2620, 60, -14, BLUSH), (1010, 2560, 74, 12, BLUSH), (1030, 3600, 50, 18, HEART), (80, 3660, 40, -8, HEART)]


async def render_bg():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for kind in ('desktop', 'mobile'):
            html, W, H = bg_html(kind)
            f = pathlib.Path('/dev/shm') / f'hero-bg-{kind}.html'; f.write_text(html)
            pg = await b.new_page(viewport={'width': W, 'height': H})
            await pg.goto(f.as_uri(), wait_until='load'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
            out = HERE / f'bg-{kind}.jpg'
            await pg.screenshot(path=str(out), type='jpeg', quality=88)
            print('bg', out, os.path.getsize(out) // 1024, 'KB')
            await pg.close()
        await b.close()


# ---------- preview on the LIVE homepage: real header, real fonts, real blocks; image + text + CSS swapped in ----------
SEC = '69b1d01489d0f8016ee3d59f'
TEXT_HTML = (HERE / 'text-block.html').read_text().strip() if (HERE / 'text-block.html').exists() else ''
LINKS_HTML = (HERE / 'links-block.html').read_text().strip() if (HERE / 'links-block.html').exists() else ''
CSS = (HERE / 'launch-hero.css').read_text() if (HERE / 'launch-hero.css').exists() else ''
JS = '''([text, links, css, desk, mob]) => {
  const t = document.querySelector('#block-b79726a6f150a9dd219f .sqs-html-content'); t.innerHTML = text;
  const a = document.querySelector('#block-yui_3_17_2_1_1773260945246_2648 a'); a.textContent = 'Start swiping'; a.setAttribute('href', '/find-your-match');
  const bar = document.querySelector('.sqs-announcement-bar-dropzone'); if (bar) bar.style.display = 'none';
  // the extra text block Tiffany's editor adds on launch day (Add Block > Text); appended like Squarespace does
  const fe = document.querySelector('[data-section-id="SEC"] .fluid-engine');
  const blk = document.createElement('div'); blk.className = 'fe-block fe-block-newlinks';
  blk.innerHTML = '<div class="sqs-block html-block sqs-block-html"><div class="sqs-block-content"><div class="sqs-html-content">' + links + '</div></div></div>';
  fe.appendChild(blk);
  const img = document.querySelector('[data-section-id="SEC"] .section-background img');
  img.removeAttribute('srcset'); img.src = desk; img.setAttribute('data-src', desk);
  const s = document.createElement('style'); s.textContent = css.split('MOBILE_URL').join(mob); document.head.appendChild(s);
  return new Promise(r => setTimeout(() => { const r_ = e => { const b = e.getBoundingClientRect(); return [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)] };
    r({sec: r_(document.querySelector('[data-section-id="SEC"]')), text: r_(document.querySelector('#block-b79726a6f150a9dd219f h1')),
       btn: r_(a), links: r_(blk), sw: document.documentElement.scrollWidth}) }, 900));
}'''.replace('SEC', SEC)


async def preview(widths=((1280, 800), (390, 844), (1440, 900), (1024, 768), (1920, 1080), (768, 1024))):
    from playwright.async_api import async_playwright
    out = HERE / 'previews'; out.mkdir(exist_ok=True)
    desk_url, mob_url = 'https://hero.local/bg-desktop.jpg', 'https://hero.local/bg-mobile.jpg'
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h in widths:
            pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2 if w <= 430 else 1)
            await pg.route('https://hero.local/*', lambda r: r.fulfill(path=str(HERE / r.request.url.rsplit('/', 1)[1]), content_type='image/jpeg'))
            await pg.goto('https://www.mahjmatchmaker.com/?preview=launchhero', wait_until='networkidle', timeout=90000)
            await pg.wait_for_timeout(1200)
            info = await pg.evaluate(JS, [TEXT_HTML, LINKS_HTML, CSS, desk_url, mob_url])
            await pg.wait_for_timeout(800)
            print(w, info)
            sec_h = info['sec'][1] + info['sec'][3]
            await pg.screenshot(path=str(out / f'hero-launch-{w}.png'), full_page=True, clip={'x': 0, 'y': 0, 'width': w, 'height': max(h, sec_h)})
            await pg.close()
        await b.close()


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('bg', 'all'): asyncio.run(render_bg())
    if what in ('preview', 'all'): asyncio.run(preview())
