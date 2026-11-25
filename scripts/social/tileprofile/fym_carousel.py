"""FYM Table-view carousel (1080x1350), the Sadie Jane template (Nov 23, approved): slide 1 = the pair mat ("her <brand> pair
mat"), slides 2-6 = more of the brand's own mats, slide 7 = CTA. Phones come from assets/social/<key>-launch/fym-phones
(Find Your Mat-ch round 2, one rack style per table). Usage: python3 fym_carousel.py <key> '<SET NAME>' '<Brand>' <count> pair:Label mat:Label ..."""
import sys, os, asyncio
from playwright.async_api import async_playwright
R = '/home/claude/mahjmatchmaker-data/'
key, SET, BR, N = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
items = [a.split(':', 1) for a in sys.argv[5:]]
OUT = f'{R}assets/social/{key}-launch/fym-carousel/'; os.makedirs(OUT, exist_ok=True)
head = open(f'{R}assets/social/sadie-jane-launch/fym-carousel/s1.html').read(); head = head[:head.find('<body>')]
tot = len(items) + 1
def slide(i, slug, label, first):
    cap = f'on <b>{label.upper()}</b> · her {BR} pair mat' if first else f'on <b>{label.upper()}</b> · {BR}'
    tm = '™' if first else ''
    return (head + f'<body><div class="c"><div class="k">{SET.upper()} · {BR.upper()}</div><h1>Match her up in<br>Find <i>Your</i> Mat-ch{tm}</h1>'
            f'<div class="n">{i}/{tot}</div><img src="file://{R}assets/social/{key}-launch/fym-phones/{key}-fym-phone-table-{slug}.png" '
            f'style="position:absolute;left:50%;top:238px;height:1010px;transform:translateX(-50%);filter:drop-shadow(0 18px 30px rgba(6,42,85,.28))">'
            f'<div class="cap" style="top:1268px">{cap}</div></div></body></html>')
end = (head + f'<body><div class="c"><div class="k">{SET.upper()} · {BR.upper()}</div><div class="n">{tot}/{tot}</div><div style="position:absolute;top:210px;width:100%;text-align:center">'
       f'<div style="font:86px/1.02 Cap;color:#054689">Try every mat<br>on {SET}</div><div style="font:italic 42px/1.3 PF;color:#062a55;margin:34px 90px 0">'
       f'Swap mats, tiles and racks on the table in Find <i>Your</i> Mat-ch. Then see all {N} of her matches in the album.</div>'
       f'<div style="display:inline-block;margin-top:56px;background:#c8325f;color:#fff;font:700 36px Bit;padding:22px 46px;border-radius:60px">Comment ALBUM</div>'
       f'<div style="font:600 32px Bit;color:#062a55;margin-top:40px">Code MAHJMATCH at {BR}</div>'
       f'<img src="file://{R}assets/brand/mahjmatchmaker-wordmark-notag.png" style="width:420px;margin-top:120px"></div></div></body></html>')
pages = [slide(i + 1, s, l, i == 0) for i, (s, l) in enumerate(items)] + [end]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for i, h in enumerate(pages, 1):
            f = OUT + f's{i}.html'; open(f, 'w').write(h); await pg.goto('file://' + f); await pg.wait_for_timeout(900)
            await pg.screenshot(path=OUT + f'{i}.jpg', type='jpeg', quality=92)
        await b.close()
asyncio.run(main()); print(OUT, len(pages))
