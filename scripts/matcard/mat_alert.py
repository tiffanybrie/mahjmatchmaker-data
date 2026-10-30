"""NEW MAT ALERT + Mat Edit social set (Tiffany, Oct 30 9:05am: "those would be great little pieces of like new
Mat alert... and then like the Mat edit... easy for you to build without me"). Runbook: docs/MAT-EDIT-ALERT.md.

Reuses the Larkspur Mat Edit colour card look (scripts/matcard/matcard.py, Oct 12-13: warm cream, mat-colour title,
flame-heart eyebrows, palette dots, album tile shots with names) and brings it up to the brand guide's newer rules:
Caprasimo headlines with no text shadow (BRAND-GUIDE 6 + Oct 21 14:12), story safe band y 269-1536, feed band
y 120-1230, flat JPG on a solid background, code on the card but no hard-coded %, Find *Your* Mat-ch(TM) with
"Your" in Playfair Display italic (Oct 26 13:29). Fonts come from the repo (scripts/social/tileprofile/fonts), so a
scheduled run needs nothing from /tmp.

Four frames, each at story size (1080x1920) and feed carousel size (1080x1350):
  1 alert   NEW MAT ALERT, mat name, "by <brand>", @handle (visible mention), big mat hero, "N tile matches" cue
  2 edit    THE MAT EDIT: mat + its palette (the Larkspur colour card)
  3 tiles   TIFFANY'S TILE MATCHES: every one of her real yeses, album tile photos with names (+ "retired")
  4 cta     match-card style mat with one cross-brand pick inset, "See all N matches in Find Your Mat-ch(TM)",
            www.mahjmatchmaker.com, code pill (link sticker goes on this frame)

Usage:
  python3 scripts/matcard/mat_alert.py poppins --matches "Lola,Moonlight,Osler,..."
  python3 scripts/matcard/mat_alert.py poppins                    # matches from config/matcard/poppins.json tiles_all
  options: --handle ohmymahjong (default: config/social/ig-handles.json for the spec's brand)
           --cta-pick "Petalee" (default: first match from a different brand that isn't retired, else first live one)
           --out assets/social/mat-edit/<key>   --frames alert,edit,tiles,cta   --no-render (HTML only)
Spec = config/matcard/<key>.json (name, brand, tag, color, mat_path, palette [[name,hex]...]). A brand-new mat with no
spec: run with --mat-photo <flat mat photo> --name "Poppins" --brand "Oh My Mahjong" [--color "#d94784"] and the
script crops the mat (palette.py crop_mat), measures the palette (palette.py palette) and names the colours from the
table below, then writes the spec (palette names are a best guess; hex is measured). Matches must be Tiffany's REAL
yeses (swipe book / album), never Claude picks (CLAUDE.md rule 4).
Checks (exit 1 on any): a tile name with no album photo, text or image outside the safe band, text clipped or
overflowing its box. Then run scripts/social/center_check.py and LOOK at contact.jpg before anything goes out.
"""
import argparse, asyncio, base64, io, json, os, re, sys, unicodedata, html as H
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'scripts', 'swipe'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
FONTS = f'file://{ROOT}/scripts/social/tileprofile/fonts'
NAVY, DNAVY, CREAM, INK, MUTED, CARD = '#054689', '#062a55', '#f6e9df', '#2a2036', '#6b5a77', '#fff8f2'
BANDS = {'story': (1080, 1920, 269, 1536), 'feed': (1080, 1350, 120, 1230)}   # W, H, top, bottom of the safe band
e = H.escape


def norm(s):
    s = re.sub(r'\(retired\)', '', s or '', flags=re.I)
    return re.sub(r'[^a-z0-9]+', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower())


def b64(p, size=None, fmt='JPEG'):
    im = Image.open(p)
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[3]); im = bg
    else:
        im = im.convert('RGB')
    if size: im.thumbnail((size, size), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, fmt, quality=90)
    return f'data:image/{fmt.lower()};base64,' + base64.b64encode(b.getvalue()).decode()


def png64(p, size=None):
    im = Image.open(p).convert('RGBA')
    if size: im.thumbnail((size, size), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


# ---------- tile lookup: album photo (assets/tiles/album/index.json) with canon_tiles overrides, names + brands ----------
IDX = json.load(open(f'{ROOT}/assets/tiles/album/index.json'))
RET = json.load(open(f'{ROOT}/config/tile-retired.json'))['sets']
RET_BY = {norm(s['name']): s for s in RET}


def tile_info(name):
    k = norm(name)
    key = next((x for x in IDX if norm(x) == k), None)
    if not key:
        return None
    meta = IDX[key]; r = RET_BY.get(k, {})
    path = f"{ROOT}/{meta['file']}"
    try:
        import canon_tiles   # Bam Bird Boutique + Virora sets use the exact Find Your Mat-ch photo (Tiffany Oct 28 2:28pm)
        c = canon_tiles.canon_for(re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', key.replace('(retired)', '')).encode('ascii', 'ignore').decode().lower()).strip('-'))
        if c: path = c
    except Exception:
        pass
    retired = bool(meta.get('retired')) or str(r.get('status', '')).startswith('retired')
    disp = r.get('name') or key.replace(' (retired)', '')
    brand = r.get('brand') or meta.get('brand') or ''
    return {'name': disp, 'img': path, 'retired': retired, 'brand': brand}


# ---------- palette naming for a brand-new spec ----------
NAMED = [('Hot Pink', '#e3528f'), ('Blush', '#e8b9cf'), ('Watermelon', '#ed5c76'), ('Crimson', '#b8142c'), ('Coral', '#f27d6b'),
         ('Peach', '#f6c3a5'), ('Orange', '#ee8a2f'), ('Butter Yellow', '#f3dc7a'), ('Mustard', '#c9a227'), ('Lime', '#a8c24b'),
         ('Olive', '#868229'), ('Sage', '#a7b89a'), ('Kelly Green', '#3c9a4f'), ('Emerald', '#1f7a55'), ('Forest', '#2f4f3a'),
         ('Mint', '#bfe3cf'), ('Teal', '#2a9a9a'), ('Aqua', '#7fd3d6'), ('Sky Blue', '#4fade3'), ('Powder Blue', '#cfe0ee'),
         ('Cornflower', '#6f8fd8'), ('Periwinkle', '#788ccb'), ('Royal Blue', '#2b4fb3'), ('Navy', '#1a2a5e'), ('Indigo', '#1a2371'),
         ('Lavender', '#9f9fd6'), ('Lilac', '#c8b3e0'), ('Plum', '#6b2d5c'), ('Berry', '#9c2a5b'), ('Cream', '#f3ead8'),
         ('Ivory', '#fbf7ef'), ('Tan', '#c9a882'), ('Caramel', '#a8672f'), ('Chocolate', '#5a3a29'), ('Charcoal', '#3a3a3a'),
         ('Black', '#141414'), ('Gray', '#9a9a9a'), ('Gold', '#c8a24a'), ('White', '#ffffff')]


def name_palette(hexes):
    import numpy as np, palette as P
    def L(h): return P.lab(np.array([[int(h[i:i + 2], 16) for i in (1, 3, 5)]], float))[0]
    out, used = [], set()
    for h in hexes:
        c = L(h); best = min((x for x in NAMED if x[0] not in used), key=lambda x: float(((L(x[1]) - c) ** 2).sum()))
        used.add(best[0]); out.append([best[0], h])
    return out


def make_spec(a, key):
    import palette as P
    os.makedirs(f'{ROOT}/config/matcard', exist_ok=True)
    mat_out = f'config/matcard/{key}_mat.jpg'
    P.crop_mat(a.mat_photo, f'{ROOT}/{mat_out}')
    pal = [h for h, s, _ in P.palette(f'{ROOT}/{mat_out}', 7) if s >= 0.03][:6]
    named = name_palette(pal)
    spec = {'name': a.name, 'brand': a.brand, 'tag': a.tag or '', 'color': a.color or named[0][1], 'mat_path': mat_out,
            'palette': named, 'tiles_all': [], '_made_by': 'mat_alert.py --mat-photo (palette names are a best guess; check them)'}
    json.dump(spec, open(f'{ROOT}/config/matcard/{key}.json', 'w'), indent=1, ensure_ascii=False)
    print('wrote spec', f'config/matcard/{key}.json')
    return spec


# ---------- HTML ----------
def head(W, Ht, top, bot):
    return f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Cap;src:url('{FONTS}/Caprasimo.ttf')}}
@font-face{{font-family:PlayI;font-style:italic;font-weight:400;src:url('{FONTS}/playfair-display-latin-400-italic.woff2')}}
@font-face{{font-family:PlayI;font-style:italic;font-weight:600;src:url('{FONTS}/playfair-display-latin-600-italic.woff2')}}
@font-face{{font-family:Bit;font-weight:400;src:url('{FONTS}/bitter-latin-400-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{FONTS}/bitter-latin-600-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:700;src:url('{FONTS}/bitter-latin-700-normal.woff2')}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{W}px;height:{Ht}px;background:{CREAM};font-family:Bit;color:{INK};overflow:hidden;position:relative}}
.wrap{{position:absolute;left:0;right:0;top:{top}px;bottom:{Ht - bot}px;padding:0 48px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;text-align:center}}
.k{{text-wrap:balance}}
.logo{{display:block}}
.eb{{font-family:Bit;font-weight:700;color:{NAVY};display:flex;align-items:center;justify-content:center;gap:14px;letter-spacing:.24em;white-space:nowrap}}
.eb img{{display:block}}
.t{{font-family:Cap;line-height:.95;text-transform:uppercase;letter-spacing:.01em}}
.by{{font-family:PlayI;font-style:italic}}
.hdl{{font-family:Bit;font-weight:700;color:{NAVY};letter-spacing:.04em}}
.tag{{font-family:PlayI;font-style:italic;color:{MUTED}}}
.mat{{border-radius:24px;background:center/cover;box-shadow:0 12px 34px rgba(42,32,54,.18);position:relative;flex:none}}
.pile{{position:absolute;border-radius:20px;background:center/cover;border:8px solid #fff;box-shadow:0 12px 30px rgba(42,32,54,.28)}}
.pal{{display:grid;background:{CARD};border-radius:20px}}
.sw{{display:flex;align-items:center;gap:14px;font-family:Bit;font-weight:700;text-transform:uppercase;letter-spacing:.04em;text-align:left}}
.sw i{{border-radius:50%;flex:none;box-shadow:inset 0 0 0 2px rgba(255,255,255,.6)}}
.grid{{display:flex;flex-wrap:wrap;justify-content:center}}
figure{{text-align:center}}
.tp{{border-radius:16px;background-size:cover;background-position:center;background-color:#efe2d6;box-shadow:0 4px 12px rgba(42,32,54,.15)}}
figcaption{{font-family:Bit;font-weight:700;line-height:1.1;white-space:nowrap}}
figcaption small{{display:block;font-weight:400;color:{MUTED};margin-top:2px}}
.cue{{font-family:Bit;font-weight:700;color:{NAVY};background:{CARD};border-radius:999px}}
.pill{{background:{DNAVY};color:#fff;font-family:Bit;font-weight:700;border-radius:999px;white-space:nowrap}}
.web{{font-family:Bit;font-weight:700;color:{NAVY};white-space:nowrap}}
.cta{{font-family:Cap;color:{DNAVY};line-height:1.08}}
.cta em{{font-family:PlayI;font-style:italic;font-weight:600}}
.cta sup{{font-family:Bit;font-size:.38em;vertical-align:.95em;margin-left:2px}}
.code{{font-family:Bit;font-weight:600;color:{INK}}}
.code b{{color:{NAVY}}}
</style></head><body><div class=wrap>"""


def build(spec, tiles, cta, handle, size):
    W, Ht, top, bot = BANDS[size]; story = size == 'story'
    s = lambda st, fe: st if story else fe
    col = spec['color']; n = len(tiles)
    mat = b64(f"{ROOT}/{spec['mat_path']}", 1400)
    logo = png64(f'{ROOT}/assets/brand/mahjmatchmaker-wordmark-notag.png')
    flame = png64(f'{ROOT}/assets/brand/flame-heart.png', 120)
    fl = lambda h: f"<img src='{flame}' style='height:{h}px'>"
    eb = lambda t, fs: f"<div class='eb k' style='font-size:{fs}px'>{fl(int(fs * 1.25))}{e(t)}{fl(int(fs * 1.25))}</div>"
    LOGO = f"<img class=logo src='{logo}' style='height:{s(70, 60)}px'>"
    title = lambda fs: f"<div class='t k' style='font-size:{fs}px;color:{col}'>{e(spec['name'])}</div>"
    by = lambda fs: f"<div class='by k' style='font-size:{fs}px'>by {e(spec['brand'])}</div>"
    code_line = lambda fs: f"<div class='code k' style='font-size:{fs}px'>www.mahjmatchmaker.com &nbsp;·&nbsp; Code <b>MAHJMATCH</b></div>"
    frames = {}

    # 1 NEW MAT ALERT
    ms = s(800, 640)
    frames['alert'] = f"""{LOGO}{eb('NEW MAT ALERT', s(38, 32))}
<div>{title(s(150, 124))}<div style='margin-top:{s(10, 6)}px'>{by(s(50, 42))}</div>
<div class='hdl k' style='font-size:{s(34, 28)}px;margin-top:{s(4, 2)}px'>@{e(handle)}</div></div>
<div class=mat style="width:{ms}px;height:{ms}px;background-image:url({mat})"></div>
<div class='cue k' style='font-size:{s(32, 28)}px;padding:{s(16, 12)}px {s(40, 34)}px'>Tiffany&rsquo;s {n} tile matches &rarr;</div>"""

    # 2 THE MAT EDIT (colour card)
    pal = spec['palette'][:6]
    if story:
        ms = 640
        body = f"""<div class=mat style="width:{ms}px;height:{ms}px;background-image:url({mat})"></div>
<div style='width:100%'><div class='hdl' style='font-size:26px;letter-spacing:.24em;margin-bottom:14px'>THE PALETTE</div>
<div class=pal style='grid-template-columns:repeat(3,1fr);gap:22px 18px;padding:24px 28px'>{''.join(f"<div class=sw style='font-size:23px'><i style='width:58px;height:58px;background:{h}'></i><span>{e(nm)}</span></div>" for nm, h in pal)}</div></div>"""
    else:
        ms = 560
        body = f"""<div style='display:flex;gap:30px;align-items:center;justify-content:center;width:100%'>
<div class=mat style="width:{ms}px;height:{ms}px;background-image:url({mat})"></div>
<div style='flex:0 0 360px'><div class='hdl' style='font-size:22px;letter-spacing:.24em;margin-bottom:12px'>THE PALETTE</div>
<div class=pal style='grid-template-columns:1fr;gap:16px;padding:22px 24px'>{''.join(f"<div class=sw style='font-size:22px'><i style='width:52px;height:52px;background:{h}'></i><span>{e(nm)}</span></div>" for nm, h in pal)}</div></div></div>"""
    frames['edit'] = f"""{LOGO}{eb('THE MAT EDIT', s(36, 30))}
<div>{title(s(130, 112))}<div style='margin-top:8px'>{by(s(46, 40))}</div>
{f"<div class='tag k' style='font-size:{s(32, 28)}px;margin-top:6px'>{e(spec['tag'])}</div>" if spec.get('tag') else ''}</div>
{body}{code_line(s(30, 26))}"""

    # 3 TIFFANY'S TILE MATCHES (all of her yeses)
    cols = 5 if n > 12 else 4 if n > 6 else 3
    rows = -(-n // cols)
    avail_h = (bot - top) - s(330, 290)            # room left after the header + footer
    tsz = min(s(184, 168), int((W - 96 - (cols - 1) * 18) / cols), int(avail_h / rows) - s(64, 58))
    fs = 23 if tsz >= 170 else 21
    figs = ''.join(f"<figure style='width:{tsz + 14}px'><div class=tp style=\"width:{tsz}px;height:{tsz}px;margin:0 auto;background-image:url({b64(t['img'], 420)})\"></div>"
                   f"<figcaption style='font-size:{fs}px;margin-top:8px'>{e(t['name'])}{'<small style=font-size:' + str(fs - 5) + 'px>retired</small>' if t['retired'] else ''}</figcaption></figure>" for t in tiles)
    frames['tiles'] = f"""{eb("TIFFANY'S TILE MATCHES", s(32, 28))}
<div><div class='t k' style='font-size:{s(96, 84)}px;color:{col}'>{e(spec['name'])} + {n}</div>
<div class='by k' style='font-size:{s(36, 32)}px;margin-top:6px'>tile sets she matched with this {e(spec['brand'])} mat</div></div>
<div class=grid style='gap:{s(22, 16)}px 4px'>{figs}</div>{code_line(s(30, 26))}"""

    # 4 CTA: match-card style (mat full, tiles inset bottom-right), Find Your Mat-ch
    ms = s(660, 500); ps = int(ms * .46)
    frames['cta'] = f"""{LOGO}
<div class='cta k' style='font-size:{s(76, 62)}px;max-width:{s(940, 960)}px'>See all {n} matches in Find <em>Your</em> Mat-ch<sup>&trade;</sup></div>
<div style='display:flex;flex-direction:column;align-items:center'><div class=mat style="width:{ms}px;height:{ms}px;margin-right:{s(34, 28)}px;background-image:url({mat})">
<div class=pile style="width:{ps}px;height:{ps}px;right:-{s(34, 28)}px;bottom:-{s(30, 24)}px;background-image:url({b64(cta['img'], 700)})"></div></div>
<div class='hdl k' style='font-size:{s(30, 26)}px;margin-top:{s(48, 40)}px'>{e(spec['name'])} + {e(cta['name'])}{(' · ' + e(cta['brand'])) if cta.get('brand') and cta['brand'] != spec['brand'] else ''}</div></div>
<div style='display:flex;flex-direction:column;align-items:center;gap:{s(18, 14)}px'><div class='web k' style='font-size:{s(40, 34)}px'>www.mahjmatchmaker.com</div>
<div class=pill style='font-size:{s(30, 26)}px;padding:{s(16, 13)}px {s(40, 34)}px'>Use code MAHJMATCH to save</div></div>"""
    return {k: head(W, Ht, top, bot) + v + '</div></body></html>' for k, v in frames.items()}


CHECK_JS = """([top,bot,W])=>{const out=[];const els=[...document.querySelectorAll('.wrap *')];
for(const el of els){const r=el.getBoundingClientRect(); if(!r.width||!r.height) continue;
 const label=(el.className||el.tagName)+': '+(el.innerText||'').slice(0,40).replace(/\\n/g,' ');
 if(r.top<top-1||r.bottom>bot+1) out.push('OVERFLOW band '+label+' y='+Math.round(r.top)+'-'+Math.round(r.bottom));
 if(r.left<-1||r.right>W+1) out.push('OVERFLOW width '+label+' x='+Math.round(r.left)+'-'+Math.round(r.right));
 if(el.children.length===0&&el.innerText&&(el.scrollWidth>el.clientWidth+2)) out.push('CLIPPED '+label);}
return out;}"""


async def render(pages, out_dir):
    from playwright.async_api import async_playwright
    problems, files = [], []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for (size, name), html in pages.items():
            W, Ht, top, bot = BANDS[size]
            hp = f'{out_dir}/html/{size}-{name}.html'; open(hp, 'w').write(html)
            pg = await b.new_page(viewport={'width': W, 'height': Ht})
            await pg.goto('file://' + hp); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            for pr in await pg.evaluate(CHECK_JS, [top, bot, W]): problems.append(f'{size}-{name}: {pr}')
            num = ['alert', 'edit', 'tiles', 'cta'].index(name) + 1
            f = f'{out_dir}/{size}-{num}-{name}.jpg'
            await pg.screenshot(path=f, type='jpeg', quality=92); files.append(f); await pg.close()
        await b.close()
    return problems, files


def contact(files, out):
    ims = [Image.open(f) for f in files]; h = 900
    th = [im.resize((int(im.width * h / im.height), h)) for im in ims]
    sheet = Image.new('RGB', (sum(t.width for t in th) + 24 * (len(th) + 1), h + 48), '#ffffff'); x = 24
    for t in th: sheet.paste(t, (x, 24)); x += t.width + 24
    sheet.save(out, quality=88)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('key'); ap.add_argument('--matches'); ap.add_argument('--handle'); ap.add_argument('--cta-pick')
    ap.add_argument('--out'); ap.add_argument('--frames', default='alert,edit,tiles,cta'); ap.add_argument('--no-render', action='store_true')
    ap.add_argument('--mat-photo'); ap.add_argument('--name'); ap.add_argument('--brand'); ap.add_argument('--color'); ap.add_argument('--tag')
    a = ap.parse_args()
    sp = f'{ROOT}/config/matcard/{a.key}.json'
    spec = json.load(open(sp)) if os.path.exists(sp) else (make_spec(a, a.key) if a.mat_photo and a.name and a.brand else sys.exit(f'no spec {sp}: pass --mat-photo --name --brand'))
    names = [x.strip() for x in (a.matches.split(',') if a.matches else spec.get('tiles_all', [])) if x.strip()]
    if not names: sys.exit('no matches: pass --matches (Tiffany\'s real yeses) or fill tiles_all in the spec')
    tiles, missing = [], []
    for nm in names:
        t = tile_info(nm); (tiles.append(t) if t else missing.append(nm))
    if missing: sys.exit('FAIL no album tile photo for: ' + ', '.join(missing) + ' (add it to assets/tiles/album/index.json first)')
    handles = json.load(open(f'{ROOT}/config/social/ig-handles.json'))
    handle = a.handle or handles.get(spec['brand'])
    if not handle: sys.exit(f"FAIL no verified IG handle for {spec['brand']} in config/social/ig-handles.json (brand guide 3: never guess)")
    if a.cta_pick:
        cta = tile_info(a.cta_pick)
    else:   # cross-brand, never the obvious same-brand pair (BRAND-GUIDE Oct 23 14:34); live sets before retired ones
        cta = next((t for t in tiles if t['brand'] and t['brand'] != spec['brand'] and not t['retired'] and 'LoveShackFancy' not in t['brand']), None) \
            or next((t for t in tiles if not t['retired']), tiles[0])
    out = os.path.abspath(a.out or f'{ROOT}/assets/social/mat-edit/{a.key}'); os.makedirs(f'{out}/html', exist_ok=True)
    want = a.frames.split(',')
    pages = {}
    for size in ('story', 'feed'):
        for k, v in build(spec, tiles, cta, handle, size).items():
            if k in want: pages[(size, k)] = v
    meta = {'mat': spec['name'], 'brand': spec['brand'], 'handle': handle, 'count': len(tiles), 'cta_pick': cta['name'],
            'matches': [{'name': t['name'], 'brand': t['brand'], 'retired': t['retired']} for t in tiles],
            'brands_shown': sorted({spec['brand']} | {t['brand'] for t in tiles if t['brand']}),
            'handles': {b: handles.get(b) for b in sorted({spec['brand']} | {t['brand'] for t in tiles if t['brand']})}}
    json.dump(meta, open(f'{out}/meta.json', 'w'), indent=1, ensure_ascii=False)
    if a.no_render:
        for (size, k), v in pages.items(): open(f'{out}/html/{size}-{k}.html', 'w').write(v)
        print('HTML only:', out); return
    problems, files = asyncio.run(render(pages, out))
    contact([f for f in files if '/story-' in f], f'{out}/contact-story.jpg')
    contact([f for f in files if '/feed-' in f], f'{out}/contact-feed.jpg')
    import shutil; shutil.rmtree(f'{out}/html', ignore_errors=True)
    for f in files: print(f)
    print('contact sheets:', f'{out}/contact-story.jpg', f'{out}/contact-feed.jpg')
    print('brands to tag:', meta['handles'])
    if problems:
        print('\n'.join(problems)); sys.exit(1)
    print('OK: every element inside the safe band, nothing clipped. Next: center_check.py + LOOK at the contact sheets.')


if __name__ == '__main__':
    main()
