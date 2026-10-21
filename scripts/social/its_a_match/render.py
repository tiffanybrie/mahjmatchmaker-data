"""'It's a match!' cards for brand reshares (Tiffany, Oct 21).

One card = one of her real album picks: tile set (canonical album photo) + a partner mat (mat-only card image).
Sizes: feed 1080x1350 (content inside y 120-1230 so the 3:4 grid crop keeps it) and story 1080x1920
(key content inside the safe zone: top 14% = 269px and bottom 20% = 384px stay clear).
Branding: wordmark (2x the Oct 21 Papaya card), tagline "Hooking up tiles, / mats & racks". No @handle line (Instagram already shows @mahjmatchmaker under a reshare; Tiffany Oct 21).
Headline variants: A = "It's a mat-ch!", B = "It's a match!".

Usage:
  python3 scripts/social/its_a_match/render.py --tile "Papaya Spritz" --mat Heiress --mat-brand "Britt Mills" \
     --tile-img assets/tiles/album/papaya-spritz.jpg --mat-img assets/colorcards/papaya-spritz/mats/heiress-britt-mills.jpg \
     --count 50 --pron her --variant B --out assets/social/<set>-launch/grid/<set>-its-a-match-<mat>
  python3 scripts/social/its_a_match/render.py --json cards.json
Each card: tile, mat, tile_brand, mat_brand, tile_img, mat_img, count, pron ('her'|'his'), out (path stem), variant.
"""
import asyncio, json, sys, os, tempfile, html as H
R = '/home/claude/mahjmatchmaker-data'
F = f'file://{R}/scripts/social/tileprofile/fonts'
G = 'file:///usr/share/fonts/truetype/google-fonts'
u = lambda p: p if p.startswith(('http', 'file:')) else f'file://{R}/{p}'
HEART = '<svg viewBox="0 0 48 48" width="{w}" height="{w}"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="{c}"/></svg>'
NAVY, PINK, PINK2 = '#062a55', '#d6336c', '#f56c8c'


def headline(variant, size):
    if variant == 'A':
        # Caveat's own hyphen, nudged off the t's crossbar so it reads as a deliberate "mat-ch" (tested Oct 21:
        # unspaced it touches the t; a drawn bar looked pasted on)
        return 'It&rsquo;s a mat<span style="margin:0 .06em">-</span>ch!'
    return 'It&rsquo;s a match!'


def page(c, kind):
    W, Ht = 1080, (1350 if kind == 'feed' else 1920)
    feed = kind == 'feed'
    img = 330 if feed else 456            # tile circle / mat square size (story: fill the safe band, Oct 21)
    hl = 128 if feed else 150
    names = f'{H.escape(c["tile"])} <span style="color:{PINK2}">&hearts;</span> <i>{H.escape(c["mat"])}</i>'
    nlen = len(c['tile']) + len(c['mat'])
    nsize = 70 if nlen <= 20 else 62 if nlen <= 26 else 54 if nlen <= 32 else 46
    if not feed: nsize += 6
    brands = f'{H.escape(c["tile_brand"])} &middot; {H.escape(c["mat_brand"])}'
    pill = f'All {c["count"]} of {c["pron"]} matches are live'
    # content block is centred in the safe band: feed 120-1230, story 269-1536
    top, bot = (120, 1230) if feed else (269, 1536)
    gap = (lambda f, s: f if feed else s)
    return f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Hand;src:url('{F}/Caveat-Bold.ttf')}}
@font-face{{font-family:Lo;src:url('{G}/Lora-Variable.ttf')}}
@font-face{{font-family:Lo;font-style:italic;src:url('{G}/Lora-Italic-Variable.ttf')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{F}/bitter-latin-600-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:700;src:url('{F}/bitter-latin-700-normal.woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{Ht}px;overflow:hidden}}
.c{{position:relative;text-align:center}}
</style></head><body><div style="position:relative;width:{W}px;height:{Ht}px;background:#fdece4;overflow:hidden">
<div style="position:absolute;right:-200px;top:-220px;width:700px;height:700px;border-radius:50%;background:#fbd9c9"></div>
<div style="position:absolute;left:-220px;bottom:-240px;width:640px;height:640px;border-radius:50%;background:#fbe3ea"></div>
<div id=blk style="position:absolute;left:0;right:0;top:{top}px;height:{bot-top}px;display:flex;flex-direction:column;align-items:center;justify-content:center">
<div class=c style="font-family:Hand;font-size:{hl}px;color:{PINK};line-height:1;white-space:nowrap">{headline(c['variant'], hl)}</div>
<div class=c style="display:flex;align-items:center;margin-top:{gap(34,56)}px">
  <div style="width:{img}px;height:{img + 14}px;border-radius:50%;background:url('{u(c['tile_img'])}') center/cover;box-shadow:0 0 0 12px #fff,0 22px 46px rgba(200,80,90,.22)"></div>
  <div style="position:relative;z-index:2;margin:0 -38px;width:118px;height:118px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 26px rgba(0,0,0,.15)">{HEART.format(w=76, c=PINK2)}</div>
  <div style="width:{img}px;height:{img}px;border-radius:36px;background:url('{u(c['mat_img'])}') center/cover;box-shadow:0 0 0 12px #fff,0 22px 46px rgba(200,80,90,.22)"></div>
</div>
<div class=c id=nm style="font-family:Lo;font-weight:700;font-size:{nsize}px;color:{NAVY};margin-top:{gap(46,70)}px;line-height:1.08;padding:0 50px">{names}</div>
<div class=c style="font:600 {gap(28,32)}px Bit;letter-spacing:.16em;text-transform:uppercase;color:{PINK};margin-top:{gap(14,18)}px;padding:0 40px">{brands}</div>
<div class=c style="margin-top:{gap(30,46)}px;background:{NAVY};color:#fff;border-radius:999px;padding:{gap(16,20)}px 42px;font:600 {gap(34,38)}px Bit">{pill}</div>
<img src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="position:relative;width:{gap(560,620)}px;margin-top:{gap(36,48)}px">
<div class=c style="font-family:Lo;font-style:italic;font-weight:500;font-size:{gap(36,40)}px;color:{NAVY};margin-top:{gap(8,12)}px;line-height:1.2">Hooking up tiles, mats &amp; racks</div>
</div></div></body></html>"""


async def render(cards):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for c in cards:
            for kind in ('feed', 'story'):
                Ht = 1350 if kind == 'feed' else 1920
                pg = await b.new_page(viewport={'width': 1080, 'height': Ht})
                tmp = os.path.join(tempfile.gettempdir(), 'its_a_match_tmp.html')
                open(tmp, 'w').write(page(c, kind))
                await pg.goto('file://' + tmp, wait_until='load')
                await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(250)
                # overflow guard: the content block must fit its safe band
                over = await pg.evaluate("(()=>{const b=document.getElementById('blk');return b.scrollHeight-b.clientHeight})()")
                nmw = await pg.evaluate("document.getElementById('nm').getBoundingClientRect().height")
                if over > 0: print('OVERFLOW', c['out'], kind, over)
                c.setdefault('_check', {})[kind] = {'overflow': over, 'names_h': nmw}
                await pg.screenshot(path=f"{R}/{c['out']}-{kind}.jpg", type='jpeg', quality=92)
                await pg.close()
        await b.close()


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description="Render one It's a match card (feed + story), or a JSON list with --json")
    ap.add_argument('--json', help='JSON list of card dicts (keys as below)')
    ap.add_argument('--tile'); ap.add_argument('--mat')
    ap.add_argument('--tile-brand', default='Oh My Mahjong'); ap.add_argument('--mat-brand')
    ap.add_argument('--tile-img', help='canonical album photo, assets/tiles/album/<set>.*')
    ap.add_argument('--mat-img', help='mat-only card image (assets/colorcards/<set>/mats/... or the FYM photo)')
    ap.add_argument('--count', type=int, help='cards on the live album page, never rounded')
    ap.add_argument('--pron', choices=['her', 'his'], default='her')
    ap.add_argument('--variant', choices=['A', 'B'], default='B', help="A = It's a mat-ch!, B = It's a match!")
    ap.add_argument('--out', help='path stem; writes <out>-feed.jpg and <out>-story.jpg')
    a = ap.parse_args()
    if a.json:
        cards = json.load(open(a.json))
    else:
        need = ['tile', 'mat', 'mat_brand', 'tile_img', 'mat_img', 'count', 'out']
        miss = [n for n in need if getattr(a, n) in (None, '')]
        if miss: ap.error('missing: ' + ', '.join('--' + m.replace('_', '-') for m in miss))
        cards = [dict(tile=a.tile, mat=a.mat, tile_brand=a.tile_brand, mat_brand=a.mat_brand, tile_img=a.tile_img,
                      mat_img=a.mat_img, count=a.count, pron=a.pron, variant=a.variant, out=a.out)]
    asyncio.run(render(cards))
    for c in cards: print(c['out'], c.get('_check'))
