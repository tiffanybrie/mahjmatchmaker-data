"""'It's a mat-ch!' carousel: the middle post of every tile set's launch row (Tiffany, Oct 21).

Three 1080x1350 slides on one cream paper background, plus a 1080x1920 story version of slide 1:
  slide1.jpg  It's a mat-ch! card: tile circle + heart + mat square, "Set ♥ Mat", brand caps line, navy pill
              "Swipe all N of <Short>'s matches / mahjmatchmaker.com", wordmark, "Hooking up tiles, / mats & racks".
              Stands on its own (brands reshare it), so it carries the site URL. Content inside y 120-1230 (grid crop).
  slide2.jpg  The real album match card (assets/cards/<set>/, via manifest.json) big in a soft white frame,
              header "From <Short>'s album", labels: mat · brand, then the racks named exactly as on the card.
  slide3.jpg  Find Your Mat-ch™ preview: phone mockup of the real FYM swipe view (fym_shot.py screenshot) with
              "Swipe your own matches · mahjmatchmaker.com". No dates: these run after the Oct 27 launch (Tiffany).
  story.jpg   slide 1 at 1080x1920, key content inside the safe band (top 14% = 269px, bottom 20% = 384px clear).
  preview.jpg side-by-side contact sheet of all four.

Settled rules (BRAND-GUIDE changelog 2026-10-21): headline "It's a mat-ch!" (FINAL, no ™); no pronouns on short
pieces (use the set's short name: "Papaya's matches"); always say where the albums live (mahjmatchmaker.com);
no @handle line; navy + pink, never brown; X and heart only on the FYM screen.

Usage (one set):
  python3 scripts/social/its_a_match/render.py --set-slug papaya-spritz --tile "Papaya Spritz" --short Papaya \
     --mat Heiress --mat-brand "Britt Mills" --count 50 \
     --current-racks "Bird & Bamboo Lavender" "Peace Love Mahjong Chartreuse" "Middle & Main Scalloped Beechwood" \
     --fym-img assets/social/its-a-match/papaya-heiress/fym-screen.jpg \
     --out-dir assets/social/its-a-match/papaya-heiress
  python3 scripts/social/its_a_match/render.py --json carousels.json     (list of dicts with the same keys)

Defaults read from the repo: tile_img = assets/tiles/album/<slug>.*, mat_img = assets/colorcards/<slug>/mats/
<mat>-<brand>.jpg, card_img + tile_racks + mat_racks = the manifest.json card for that mat. Make the FYM screen
first with fym_shot.py. The script prints OVERFLOW / WARN lines; fix every one before showing Tiffany.
"""
import asyncio, glob, json, os, re, tempfile, html as H

R = '/home/claude/mahjmatchmaker-data'
F = f'file://{R}/scripts/social/tileprofile/fonts'
G = 'file:///usr/share/fonts/truetype/google-fonts'
u = lambda p: p if p.startswith(('http', 'file:')) else f'file://{p if p.startswith("/") else R + "/" + p}'
e = H.escape
HEART = '<svg viewBox="0 0 48 48" width="{w}" height="{w}"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="{c}"/></svg>'
NAVY, WNAVY, PINK, PINK2, BLUSH = '#062a55', '#054689', '#d6336c', '#f56c8c', '#f7b6c8'
PAPER = '#faf3ea'   # paper cream (brand guide §6); same background on every slide
SITE = 'mahjmatchmaker.com'
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
poss = lambda n: f'{H.escape(n)}&rsquo;s'   # already escaped; never e(poss(..))


def headline():
    # Caveat's own hyphen, nudged off the t's crossbar so it reads as a deliberate "mat-ch" (tested Oct 21)
    return 'It&rsquo;s a mat<span class=hy style="margin:0 .06em">-</span>ch!'


def shell(W, Ht, body):
    return f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Hand;src:url('{F}/Caveat-Bold.ttf')}}
@font-face{{font-family:Lo;src:url('{G}/Lora-Variable.ttf')}}
@font-face{{font-family:Lo;font-style:italic;src:url('{G}/Lora-Italic-Variable.ttf')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{F}/bitter-latin-600-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:700;src:url('{F}/bitter-latin-700-normal.woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:{W}px;height:{Ht}px;overflow:hidden}}
.c{{position:relative;text-align:center}}
</style></head><body><div style="position:relative;width:{W}px;height:{Ht}px;background:{PAPER};overflow:hidden">
<div style="position:absolute;right:-210px;top:-230px;width:700px;height:700px;border-radius:50%;background:#fbe3ea"></div>
<div style="position:absolute;left:-230px;bottom:-250px;width:660px;height:660px;border-radius:50%;background:#fbe3ea;opacity:.75"></div>
{body}</div></body></html>"""


def slide1(c, kind):
    W, Ht = 1080, (1350 if kind == 'feed' else 1920)
    feed = kind == 'feed'
    g = lambda f, s: f if feed else s
    img = g(330, 412)
    hl = g(124, 150)
    names = f'{e(c["tile"])} <span style="color:{PINK2}">&hearts;</span> <i>{e(c["mat"])}</i>'
    nlen = len(c['tile']) + len(c['mat'])
    nsize = 70 if nlen <= 20 else 62 if nlen <= 26 else 54 if nlen <= 32 else 46
    if not feed: nsize += 6
    brands = f'{e(c["tile_brand"])} &middot; {e(c["mat_brand"])}'
    top, bot = (120, 1230) if feed else (269, 1536)
    body = f"""<div id=blk style="position:absolute;left:0;right:0;top:{top}px;height:{bot-top}px;display:flex;flex-direction:column;align-items:center;justify-content:center">
<div class=c style="font-family:Hand;font-size:{hl}px;color:{PINK};line-height:1;white-space:nowrap">{headline()}</div>
<div class=c style="display:flex;align-items:center;margin-top:{g(30,52)}px">
  <div style="width:{img}px;height:{img + 14}px;border-radius:50%;background:url('{u(c['tile_img'])}') center/cover;box-shadow:0 0 0 12px #fff,0 22px 46px rgba(200,80,90,.20)"></div>
  <div style="position:relative;z-index:2;margin:0 -38px;width:118px;height:118px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 26px rgba(0,0,0,.13)">{HEART.format(w=76, c=PINK2)}</div>
  <div style="width:{img}px;height:{img}px;border-radius:36px;background:url('{u(c['mat_img'])}') center/cover;box-shadow:0 0 0 12px #fff,0 22px 46px rgba(200,80,90,.20)"></div>
</div>
<div class=c id=nm style="font-family:Lo;font-weight:700;font-size:{nsize}px;color:{NAVY};margin-top:{g(42,64)}px;line-height:1.08;padding:0 50px">{names}</div>
<div class=c style="font:600 {g(28,32)}px Bit;letter-spacing:.16em;text-transform:uppercase;color:{PINK};margin-top:{g(12,16)}px;padding:0 40px">{brands}</div>
<div class=c id=pill style="margin-top:{g(28,44)}px;background:{NAVY};color:#fff;border-radius:{g(44,52)}px;padding:{g(16,20)}px 46px {g(18,22)}px;line-height:1.15">
  <div style="font:600 {g(36,40)}px Bit;white-space:nowrap">Swipe all {c['count']} of {poss(c['short'])} matches</div>
  <div style="font:700 {g(32,36)}px Bit;color:{BLUSH};margin-top:{g(4,6)}px;letter-spacing:.02em;white-space:nowrap">{SITE}</div>
</div>
<img src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="position:relative;width:{g(600,660)}px;margin-top:{g(32,48)}px">
<div class=c style="font-family:Lo;font-style:italic;font-weight:500;font-size:{g(38,42)}px;color:{NAVY};margin-top:{g(6,10)}px;line-height:1.18">Hooking up tiles,<br>mats &amp; racks</div>
</div>"""
    return W, Ht, shell(W, Ht, body)


def slide2(c):
    W, Ht = 1080, 1350
    col = lambda label, racks: (f'<div style="flex:{max(len(r) for r in racks + [label])} 1 0;min-width:0"><div style="font:700 26px Bit;letter-spacing:.16em;color:{PINK};text-transform:uppercase">{label}</div>'
                                + ''.join(f'<div style="font:600 31px Bit;color:{NAVY};margin-top:6px;line-height:1.15">{e(r)}</div>' for r in racks) + '</div>')
    cols = col('Match the tiles', c['tile_racks'])
    if c.get('mat_racks'): cols += '<div style="width:2px;background:#f2c9d5;margin:0 26px;align-self:stretch"></div>' + col('Match the mat', c['mat_racks'])
    body = f"""<div id=blk style="position:absolute;left:0;right:0;top:52px;bottom:48px;display:flex;flex-direction:column;align-items:center">
<div class=c style="font:700 30px Bit;letter-spacing:.2em;color:{NAVY};text-transform:uppercase">Top match card</div>
<div class=c style="font-family:Hand;font-size:96px;color:{PINK};line-height:1;margin-top:4px;white-space:nowrap">From {poss(c['short'])} album</div>
<div id=frame style="flex:1;min-height:0;margin-top:22px;background:#fff;border-radius:30px;padding:20px;box-shadow:0 18px 44px rgba(200,80,90,.16),0 0 0 1px #f3dfe3;display:flex">
  <img id=card src="{u(c['card_img'])}" style="height:100%;width:auto;border-radius:14px;display:block">
</div>
<div class=c id=nm style="font-family:Lo;font-weight:700;font-size:46px;color:{NAVY};margin-top:24px;line-height:1.1"><i>{e(c['mat'])}</i> <span style="color:{PINK2}">&middot;</span> {e(c['mat_brand'])}</div>
<div id=racks style="display:flex;margin-top:16px;width:1010px;text-align:center">{cols}</div>
</div>"""
    return W, Ht, shell(W, Ht, body)


def slide3(c):
    W, Ht = 1080, 1350
    body = f"""<div id=blk style="position:absolute;left:0;right:0;top:60px;bottom:56px;display:flex;flex-direction:column;align-items:center">
<div class=c style="font-family:Lo;font-weight:700;font-size:84px;color:{NAVY};line-height:1;white-space:nowrap">Find <i>Your</i> Mat-ch<span style="font-size:.34em;vertical-align:1.3em;margin-left:3px">&trade;</span></div>
<div class=c style="font:600 38px Bit;color:{NAVY};margin-top:18px">Swipe your own matches</div>
<div class=c style="font:700 32px Bit;letter-spacing:.12em;color:{PINK};text-transform:uppercase;margin-top:10px">{SITE}</div>
<div id=phone style="flex:1;min-height:0;margin-top:36px;aspect-ratio:{390+2*16}/{844+34+2*16};background:{NAVY};border-radius:74px;padding:16px;box-shadow:0 26px 60px rgba(6,42,85,.22),inset 0 0 0 3px #1d4573;position:relative">
  <div style="width:100%;height:100%;border-radius:58px;overflow:hidden;background:#fff;position:relative">
    <img id=scr src="{u(c['fym_img'])}" style="width:100%;height:auto;display:block;margin-top:0">
    <div style="position:absolute;left:50%;bottom:12px;width:34%;height:7px;margin-left:-17%;border-radius:4px;background:#1b1f2a;opacity:.85"></div>
  </div>
</div>
</div>"""
    return W, Ht, shell(W, Ht, body)


def fill_defaults(c):
    s = c.get('set_slug') or slug(c['tile'])
    c.setdefault('short', c['tile']); c.setdefault('tile_brand', 'Oh My Mahjong')
    if not c.get('tile_img'):
        hits = sorted(glob.glob(f'{R}/assets/tiles/album/{s}.*'))
        if not hits: raise SystemExit(f'no album tile photo assets/tiles/album/{s}.*')
        c['tile_img'] = hits[0]
    if not c.get('mat_img'):
        p = f'{R}/assets/colorcards/{s}/mats/{slug(c["mat"])}-{slug(c["mat_brand"])}.jpg'
        if not os.path.exists(p): raise SystemExit(f'no mat-only image {p}; pass --mat-img (FYM photo)')
        c['mat_img'] = p
    if not c.get('card_img') or 'tile_racks' not in c:
        man = json.load(open(f'{R}/assets/cards/{s}/manifest.json'))
        cards = [k for k in man['cards'] if k['mat'].lower() == c['mat'].lower() and k['brand'].lower() == c['mat_brand'].lower()]
        if not cards: raise SystemExit(f'{c["mat"]} ({c["mat_brand"]}) not in assets/cards/{s}/manifest.json')
        k = cards[0]
        c.setdefault('card_img', f'{R}/assets/cards/{s}/{k["file"]}')
        c.setdefault('tile_racks', k.get('racks') or []); c.setdefault('mat_racks', k.get('mat_racks') or [])
        c.setdefault('_album_order', k.get('order'))
    cur = c.get('current_racks')
    if cur:
        stale = [r for r in c['tile_racks'] if r not in cur]
        if stale:
            print(f'WARN {c["tile"]} + {c["mat"]}: the album card still shows {stale}, which are not '
                  f'{c["short"]}\'s current racks {cur}. Slide 2 labels follow the card; re-render when the card is fixed.')
    c.setdefault('out_dir', f'assets/social/its-a-match/{slug(c["short"])}-{slug(c["mat"])}')
    return c


async def render(cards):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for c in cards:
            od = c['out_dir'] if c['out_dir'].startswith('/') else f'{R}/{c["out_dir"]}'
            os.makedirs(od, exist_ok=True)
            jobs = [('slide1', *slide1(c, 'feed')), ('slide2', *slide2(c)), ('slide3', *slide3(c)), ('story', *slide1(c, 'story'))]
            c['_check'] = {}
            for name, W, Ht, html in jobs:
                pg = await b.new_page(viewport={'width': W, 'height': Ht})
                tmp = os.path.join(tempfile.gettempdir(), f'its_a_match_{name}.html')
                open(tmp, 'w').write(html)
                await pg.goto('file://' + tmp, wait_until='load')
                await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
                chk = await pg.evaluate("""()=>{const b=document.getElementById('blk');const r=b.getBoundingClientRect();
                  const out=[];b.querySelectorAll('*').forEach(el=>{const q=el.getBoundingClientRect();if(q.width&&!el.classList.contains('hy')&&(q.bottom>r.bottom+1||q.top<r.top-14||q.left<-1||q.right>innerWidth+1))out.push((el.id||el.tagName)+':'+el.textContent.slice(0,20)+'@'+[q.top,q.bottom,q.left,q.right].map(Math.round))});
                  const broken=[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src.slice(-60));
                  return {overflow:b.scrollHeight-b.clientHeight,outside:out.slice(0,6),broken}}""")
                if chk['overflow'] > 1 or chk['outside'] or chk['broken']: print('OVERFLOW/BROKEN', name, chk)
                c['_check'][name] = chk
                await pg.screenshot(path=f'{od}/{name}.jpg', type='jpeg', quality=92)
                await pg.close()
            preview(od)
        await b.close()


def preview(od):
    from PIL import Image, ImageDraw, ImageFont
    names = ['slide1', 'slide2', 'slide3', 'story']
    H0 = 900
    ims = [Image.open(f'{od}/{n}.jpg') for n in names]
    ims = [i.resize((round(i.width * H0 / i.height), H0), Image.LANCZOS) for i in ims]
    W = sum(i.width for i in ims) + 40 * (len(ims) + 1)
    sheet = Image.new('RGB', (W, H0 + 120), '#e9e4ea')
    d = ImageDraw.Draw(sheet)
    try: fnt = ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf', 34)
    except Exception: fnt = ImageFont.load_default()
    x = 40
    for n, i in zip(['1 · It\'s a mat-ch!', '2 · Match card', '3 · Find Your Mat-ch', 'Story (slide 1)'], ims):
        sheet.paste(i, (x, 40)); d.text((x, H0 + 60), n, fill='#062a55', font=fnt); x += i.width + 40
    sheet.save(f'{od}/preview.jpg', quality=90)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description="Render the It's a mat-ch! carousel (3 slides + story) for one set, or a JSON list")
    ap.add_argument('--json', help='JSON list of carousel dicts (keys = the long option names with _)')
    ap.add_argument('--tile', help='tile set name as the brand writes it'); ap.add_argument('--set-slug', help='album slug, e.g. papaya-spritz')
    ap.add_argument('--short', help="short name for the pill/header, e.g. Papaya (no pronouns on short pieces)")
    ap.add_argument('--mat'); ap.add_argument('--mat-brand'); ap.add_argument('--tile-brand', default='Oh My Mahjong')
    ap.add_argument('--tile-img'); ap.add_argument('--mat-img'); ap.add_argument('--card-img')
    ap.add_argument('--tile-racks', nargs='*', help='override; default = racks on the album card'); ap.add_argument('--mat-racks', nargs='*')
    ap.add_argument('--current-racks', nargs='*', help="the set's current racks; WARN if the card shows others")
    ap.add_argument('--count', type=int, help='cards on the live album page, never rounded')
    ap.add_argument('--fym-img', help='FYM phone screenshot from fym_shot.py')
    ap.add_argument('--out-dir')
    a = ap.parse_args()
    if a.json:
        cards = json.load(open(a.json))
    else:
        need = ['tile', 'mat', 'mat_brand', 'count', 'fym_img']
        miss = [n for n in need if getattr(a, n) in (None, '')]
        if miss: ap.error('missing: ' + ', '.join('--' + m.replace('_', '-') for m in miss))
        cards = [{k: v for k, v in vars(a).items() if v not in (None, []) and k != 'json'}]
    cards = [fill_defaults(c) for c in cards]
    asyncio.run(render(cards))
    for c in cards: print(c['out_dir'], json.dumps(c.get('_check')))
