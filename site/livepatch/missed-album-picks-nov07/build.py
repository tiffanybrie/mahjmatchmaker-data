"""Missed album picks (Nov 7 2026): every (album, mat) pair that is one of Tiffany's real picks but is NOT a match card on the
live album page becomes a match card appended to that page.

Why: Tiffany hearted mats in MAT swipe books (Larkspur Oct 25 onto 28 tile sets, Poppins, Vivienne, holiday mat books) and
in the Nov 7 missed-mats page. The yeses reached Find Your Mat-ch m-lists but never the album pages ("So much time spent on
that single mat... and then you guys just let it fall on the floor"). A YES IS A YES: they go on the album pages.

Inputs (pairs.json, written by find_pairs.py):
  - FYM website copy site-app/fym-v117 (fym-site-preview) set m-lists  +  config/picks/missed-mats-round1-2026-11-07.txt
  - minus every pair whose mat is already a card on the live page (card-level match: mat name tokens + "Mat by" brand)
Card (Juniper/Deco pipeline, scripts/albumcard/gen2.py + card2.html): tile PILE photo assets/tiles/album/<set> (holiday sets:
assets/tiles/holiday), current navy wordmark (card_navy_logo_v3.png), racks at TRUE relative length.
  Year-round card: tile racks = the album's approved list (config/tile-racks-picks.json final_lists, else colorcards racks);
    mat racks = config/mat-racks-picks.json registry when the mat is listed, else the mat's saved card racks
    (config/matcard/<mat>.json, e.g. Poppins), else matpick (2 nearest B&B colours, not already tile racks).
  Holiday card (mat is a holiday mat, or a holiday-page section): late-holiday rules (Tiffany Nov 3 STANDING): tile side
    trimmed to its first painted colour, mat side = one B&B colour (never orange) + one neutral real rack; registry wins.
  Code band: 10% floor; 'SAVE WITH CODE' for Anders Ruff / Mahjong Register / The Mahjong Press mats (Juniper rule).
Usage: python3 build.py cards [only_prefix...]     render cards -> assets/cards/missed-nov07/
       python3 build.py html <sha>                 write pages/<page>.html figure payloads + manifest.json"""
import json, os, re, sys, io, base64, html, subprocess
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, R + 'scripts/albumcard')
from matpick import pick as MATPICK
from tdt_policy import card_code, shop_url
OUT = 'assets/cards/missed-nov07'
P = json.load(open(HERE + 'pairs.json'))
# Short names the live album pages already use for these mats (live h3s, e.g. 'Dear Santa + Holiday Love Red & Green'), so titles fit the card
SHORT = {'Bespoke x Corey Paige - Holiday Love Mat - Red/Green (Side A: All-Over Hearts)': 'Holiday Love Red & Green',
         'Bespoke x Corey Paige - Holiday Love Mat - Blue (Side A: All-Over Hearts)': 'Holiday Love Blue',
         'Ski Club Mat- Red Sweater Border': 'Ski Club Red Sweater', 'Ski Club Mat - Periwinkle Center': 'Ski Club Periwinkle',
         'Betty (Floral Monogram Game Surface)': 'Betty Floral', 'Holly Jolly Double-Sided Leatherette': 'Holly Jolly Leatherette'}
CARDTITLE = {'Lena Took Seven Months to Needlepoint a Pillow': 'Lena Took Seven Months'}  # card title band only; the caption keeps the full name
for _p in P: _p['mat'] = SHORT.get(_p['mat'], _p['mat'])
# Held out of the paste: the only photo we have (FYM's) carries the brand's MAHJ SQUAD watermark all over it
HOLD = {'Green Malachite'}
SITE = 'https://www.mahjmatchmaker.com'
F = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']
CC = json.load(open(R + 'config/colorcards.json'))['sets']
REG = {k: v for k, v in json.load(open(R + 'config/mat-racks-picks.json')).items() if isinstance(v, dict)}
HOLMAN = json.load(open(R + 'scripts/albumcard/holiday_manifest.json'))
SIB = {}
for x in HOLMAN: SIB.setdefault(x['tile'], x['racks'])
COLS = json.load(open(R + 'scripts/albumcard/holiday_title_colors.json'))
RL = {n: u for n, u in json.load(open(R + 'data.json'))['R']}
IDX = json.load(open(R + 'assets/racks/card/index.json'))['racks']
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
ORANGE = {x['name'] for x in json.load(open(R + 'builder/bbracks.json')) if x['fam'] == 'orange' or any(w in x['name'] for w in ('Coral', 'Orange', 'Peach', 'Tangerine', 'Rust'))}
FLAME = 'data:image/png;base64,' + base64.b64encode(open(R + 'assets/brand/flame-heart-holiday.png', 'rb').read()).decode()
nz = lambda x: re.sub(r'[^a-z0-9]', '', str(x or '').lower().replace('&', 'and'))
e = lambda s: html.escape(str(s), quote=True)

# ---- tile side ------------------------------------------------------------------------------------------------
HOLTILE = {'dear-santa': 'assets/tiles/holiday/dear-santa.jpg', 'nutcracker-ballet': 'assets/tiles/holiday/nutcracker-ballet.jpg',
           'holly-jolly-pink': 'assets/tiles/holiday/holly-jolly-pink-pile.jpg', 'holly-jolly-red': 'assets/tiles/holiday/holly-jolly-red-pile.jpg',
           'holly-jolly-green': 'assets/tiles/holiday/holly-jolly-green.jpg', 'tinselle-emerald': 'assets/tiles/holiday/tinselle-emerald-3x3.jpg',
           'tinselle-ruby': 'assets/tiles/holiday/tinselle-ruby-3x3.jpg', 'rackin-rudolph': 'assets/tiles/holiday/rackin-rudolph.jpg',
           'nivalee-blue': 'assets/tiles/holiday/nivalee-blue.jpg', 'cmc-apres-ski': 'assets/tiles/holiday/cmc-apres-ski.jpg',
           'december-1994': 'assets/tiles/sunday_mahjong_december_1994_tilebox_CARD-ONLY-edited.jpg'}
TILEFILE = {'tortoise': 'assets/tiles/album/classic-tortoise-cream.jpg', 'sunday-tile-set': 'assets/tiles/album/sunday-tile-set.png'}
def page_key(u):  # 'lola' / 'holiday#dear-santa'
    p = u.replace(SITE, '').strip('/').split('#')
    return ('holiday#' + p[1]) if len(p) > 1 else p[0].replace('-mahjong-tile-matches', '')
def tile_slug(pk): return pk.split('#')[1] if '#' in pk else pk
def tile_file(t):
    if t in HOLTILE: return HOLTILE[t]
    if t in TILEFILE: return TILEFILE[t]
    for x in ('jpg', 'png'):
        if os.path.exists(R + f'assets/tiles/album/{t}.{x}'): return f'assets/tiles/album/{t}.{x}'
    raise SystemExit('no tile photo for ' + t)
NOREMOVED = lambda ls: [l for l in ls if not l.startswith('Mahjong Row')]  # Mahjong Row & Co. is out of the site (Nov 6): never on a new card
def full(k): return 'Bird & Bamboo ' + k[3:] if k.startswith('bb:') else ('Peace Love Mahjong ' + k[4:] if k.startswith('plm:') else k)
def tile_racks_year(t):
    src = F.get(t) or (CC.get(t) or {}).get('racks') or SIB.get(t) or []
    return NOREMOVED([full(x) for x in src])
NEUTRAL_WORDS = ('Oak', 'Walnut', 'Tortoise', 'Opal', 'Milk Glass', 'Beechwood', 'White Acrylic', 'Burl', 'Clear', 'Pearl', 'Lace', 'Brass')
def neutral(l):
    if l.startswith('Bird & Bamboo '): return False
    return any(w in l for w in NEUTRAL_WORDS) and not any(w in l for w in ('Jade', 'Cornflower', 'Peach', 'Oxblood'))
def tile_racks_hol(t):  # late_holiday_build.tile_racks: one painted colour, real photos only, max 3
    src = F.get(t) or SIB.get(t) or (CC.get(t) or {}).get('racks') or []
    out, painted = [], 0
    for l in NOREMOVED(map(full, src)):
        if not l.startswith('Bird & Bamboo ') and l not in IDX: continue
        if not neutral(l):
            if painted: continue
            painted += 1
        out.append(l)
    return out[:3]

# ---- mat side ------------------------------------------------------------------------------------------------
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')
def trim(im):
    g = im.convert('L').point(lambda p: 255 if p < 235 else 0); bb = g.getbbox(); return im.crop(bb) if bb else im
def curled(im):  # Etsy/YOLO/Amazon photos with the black backing curled up at the top right (white cut-off corner, dark backing
    # just inside it) -> turn 90 deg so the corner sits under the tile photo (thin-albums Oct 26 rule)
    g = im.convert('L'); w, h = g.size
    px = lambda t: g.getpixel((min(w - 1, int(w * (1 - t))), int(h * t)))
    big = all(px(t) > 240 for t in (.02, .05, .08, .11)) and sum(px(t) < 70 for t in (.17, .2, .23, .26, .3)) >= 2
    small = all(px(t) > 240 for t in (.01, .03)) and sum(px(t) < 70 for t in (.07, .09, .11, .13, .15)) >= 2
    return big or small
def crop_year(im):  # Juniper/Papaya default framing: whole mat for small photos, a 72% bottom-left zoom for big ones
    Wd, H = im.size; z = .72 if Wd >= 900 else 1.0
    cw = int(Wd * z); ch = int(cw / .973)
    if ch > H: ch = H; cw = int(ch * .973)
    return im.crop((0, H - ch, cw, H))
def crop_hol(im):  # late holiday: whole mat
    W_, H = im.size; cw = W_; ch = int(cw / .973)
    if ch > H: ch = H; cw = int(ch * .973)
    return im.crop((0, H - ch, cw, H))
# better local photos / approved crops for the mat-book mats
LOCAL = {'www.ohmymahjong.com/larkspur-mat-w-tube': ('assets/launches/omm-larkspur-mat/01.jpg', [150, 1000, 1650, 2541]),
         'www.ohmymahjong.com/vivienne-mat-w-tube': ('assets/launches/omm-vivienne-mat/01.jpg', [0, 0, 2195, 2195]),
         'www.ohmymahjong.com/poppins-mat-w-tube': ('config/matcard/poppins_mat.jpg', None),
         'mahjandmoon.com/scalloped-bow-mahjong-mat': ('assets/mats/v108/mm-scalloped-bow-mahjong-mat.jpg', None)}
MATCARD = {}
for f in os.listdir(R + 'config/matcard'):
    if f.endswith('.json'):
        j = json.load(open(R + 'config/matcard/' + f)); MATCARD[nz(j.get('brand', '') + j['name'])] = j
def mat_image(p):
    k = p['key']
    for kk, (f, c) in LOCAL.items():
        if kk in k or k.endswith(kk.split('/')[-1]):
            im = flat(Image.open(R + f)); return (im.crop(tuple(c)) if c else im), f, True
    f = HERE + 'matphotos/' + p['photo']
    im = trim(flat(Image.open(f)))
    if curled(im): im = im.rotate(-90, expand=True)
    return im, 'site/livepatch/missed-album-picks-nov07/matphotos/' + p['photo'], False
def reg_racks(p):
    t = nz(p['brand'] + p['mat_name'])
    for v in REG.values():
        if nz(v.get('mat')) == t or nz(v.get('mat')) == nz(p['brand'] + p['mat']): return list(v['racks'])
    mc = MATCARD.get(nz(p['brand'] + p['mat_name']))
    if mc and mc.get('racks'):
        return ['Bird & Bamboo ' + r[0] for r in mc['racks'] if r[2]][:3]
    return None
def mat_racks_year(im, tr):
    return [l for l in MATPICK(im, exclude=[x for x in tr if x.startswith('Bird & Bamboo ')]) if l not in tr][:2]
def mat_racks_hol(im, tr):
    ex = [l for l in tr if l.startswith('Bird & Bamboo ')] + ['Bird & Bamboo ' + o for o in ORANGE]
    p = [x for x in MATPICK(im, exclude=ex, maxn=2) if x.startswith('Bird & Bamboo ') and x[14:] not in ORANGE][:1]
    import numpy as _n
    light = _n.asarray(im.convert('L').resize((64, 64))).mean() > 150
    for n in (['Middle & Main Milk Glass Scalloped Acrylic', 'Miss Mahjong Scalloped Iridescent Opal', 'Bam Bird Boutique Walnut'] if light
              else ['Bam Bird Boutique Walnut', 'Middle & Main Hawksbill Heritage Tortoise', 'Miss Mahjong Scalloped Iridescent Opal']):
        if n not in tr: return p + [n]
    return p
def footer(brand): return 'SAVE WITH CODE : MAHJMATCH' if brand in NOPCT else '10% OFF  USE CODE : MAHJMATCH'
def uri(im, maxs=1500):
    im = im.copy(); im.thumbnail((maxs, maxs), Image.LANCZOS); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=91)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and').replace("'", '').replace('é', 'e').replace('á', 'a')).strip('-')

def flush(cards):
    if not cards: return
    spec = {'_note': 'missed album picks Nov 7', 'cards': cards, 'max_racks': 4, 'navy': 'assets/brand/card_navy_logo_v3.png', 'true_len': True}
    sp = '/tmp/missed_spec.json'; json.dump(spec, open(sp, 'w'))
    subprocess.run(['python3', R + 'scripts/albumcard/gen2.py', sp, R + OUT], check=True)
    os.remove(sp)
    for c in cards:
        f = f"/tmp/cards2/{c['slug']}.html"
        if os.path.exists(f): os.remove(f)

def build_cards(only=()):
    cards, man = [], []
    cache = {}
    for p in P:
        pk = p['page']; t = tile_slug(pk)
        if only and not any(pk.startswith(o) or nz(p['mat']).startswith(nz(o)) for o in only): continue
        if p['key'] not in cache: cache[p['key']] = mat_image(p)
        im, src, local = cache[p['key']]
        hol = p['section'] == 'holiday'
        if hol:
            m = crop_hol(im) if not local else im
            tr = tile_racks_hol(t); mr = reg_racks(p) or mat_racks_hol(m, tr)
        else:
            m = im if local else crop_year(im)
            tr = tile_racks_year(t); mr = reg_racks(p) or mat_racks_year(m, tr)
        mr = [x for x in mr if x not in tr]
        col = COLS.get(t) or (CC.get(t) or {}).get('col') or p.get('tc') or '#1f3a6b'
        c = {'slug': p['file'][:-4], 'set': t, 'title': f"{p['tile_name']} + {CARDTITLE.get(p['mat'], p['mat'])}", 'col': col, 'tile_file': tile_file(t), 'tilefit': 'cover',
             'racks': tr, 'mat_racks': mr, 'file': p['file'], 'code': footer(p['brand']), 'mat': uri(m), 'tile_brand': p['tile_brand']}
        if hol: c.update(hol=True, flame=FLAME)
        if not (os.environ.get('SKIP_DONE') and os.path.exists(R + OUT + '/' + p['file'])): cards.append(c)
        if os.environ.get('META_ONLY'): cards.clear()
        if len(cards) >= 24: flush(cards); cards.clear()
        man.append({k: p[k] for k in ('page', 'section', 'tile_name', 'mat', 'brand', 'key', 'file')} | {'tile_racks': tr, 'mat_racks': mr, 'mat_src': src})
    flush(cards)
    old = {}
    if os.path.exists(HERE + 'cards.json'): old = {x['file']: x for x in json.load(open(HERE + 'cards.json'))}
    for x in man: old[x['file']] = x
    json.dump(list(old.values()), open(HERE + 'cards.json', 'w'), indent=1, ensure_ascii=False)
    print(len(cards), 'cards')

def rack_links(labels):
    out = []
    for r in labels:
        u = RL.get(r)
        out.append(f'<a href="{e(u)}" target="_blank" rel="sponsored noopener">{e(r)}</a>' if u else e(r))
    return ' · '.join(out)

def figures(sha):
    C = {x['file']: x for x in json.load(open(HERE + 'cards.json'))}
    import racks as RK
    def drawn(l): return l.startswith('Bird & Bamboo ') or RK.by_label(l) is not None or RK.photo(l) is not None  # caption = racks on the card
    pages = {}
    for p in P:
        c = C.get(p['file'])
        if not c or p['mat_name'] in HOLD: continue
        c = dict(c, tile_racks=[l for l in c['tile_racks'] if drawn(l)][:4], mat_racks=[l for l in c['mat_racks'] if drawn(l)])
        b = p['brand']; dc = p.get('dc') or ''
        dcp = re.sub(r'^https?://(www\.)?mahjmatchmaker\.com', '', dc)
        by = f'<a href="{e(dcp)}">{e(b)}</a>' if dcp else e(b)
        if p.get('retired'): by += '<span class="mm3-ret">Retired</span>'
        url = shop_url(p.get('url') or '', b)
        if p.get('retired'):
            ret = '<p class="mm3-retn">This mat is retired. Look for it secondhand in mahjong buy/sell groups.</p>'
            btn = (f'<a class="mm3-btn" href="https://www.ohmymahjong.com/collections/mahjong-mats" target="_blank" rel="sponsored noopener">Shop Current OMM Mats</a>'
                   if b == 'Oh My Mahjong' else '')
        else:
            ret = ''
            btn = f'<a class="mm3-btn" href="{e(url)}" target="_blank" rel="sponsored noopener">Shop the {e(p["mat"])} Mat</a>' if url else ''
        code = card_code(b) if p.get('code') else ''
        hol = p['section'] == 'holiday'
        alt = f"{p['tile_brand']} {p['tile_name']} mahjong tiles with {b} {p['mat']} {'holiday ' if hol else ''}mahjong mat"
        fig = (f'<figure class="mm3-c{" mm3-hc" if hol else ""}"><div class="mm3-im"><img src="https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{sha}/{OUT}/{p["file"]}" data-lb="" '
               f'alt="{e(alt)}" loading="lazy" width="750" height="938"><a class="mm3-pin" href="#" target="_blank" rel="noopener" aria-label="Save to Pinterest">Save</a></div>'
               f'<figcaption><span class="mm3-n">00</span><h3>{e(p["tile_name"])} + {e(p["mat"])}</h3><span class="mm3-by">Mat by {by}</span>{ret}'
               f'<div class="mm3-l">{btn}{code}</div>'
               f'<div class="mm3-rk" style="margin-top:8px;font-size:.82em;line-height:1.55">Match the tiles: {rack_links(c["tile_racks"])}<br>Match the mat: {rack_links(c["mat_racks"])}</div></figcaption></figure>')
        pg = pages.setdefault(p['page'], {'url': p['album'], 'main': [], 'holiday': [], 'brands': set()})
        pg['holiday' if hol else 'main'].append(fig); pg['brands'].add(b)
    os.makedirs(HERE + 'pages', exist_ok=True)
    man = {}
    for pk, v in pages.items():
        fn = pk.replace('#', '--') + '.json'
        json.dump({'url': v['url'], 'main': v['main'], 'holiday': v['holiday']}, open(HERE + 'pages/' + fn, 'w'), ensure_ascii=False)
        man[pk] = {'url': v['url'], 'file': 'pages/' + fn, 'main': len(v['main']), 'holiday': len(v['holiday']), 'brands': sorted(v['brands'])}
    mats = {}
    for p in P: mats.setdefault(p['page'], set()).add(p['mat'])
    def rank(pk):
        s = mats.get(pk, set())
        return (0 if 'Larkspur' in s else 1 if s & {'Poppins', 'Vivienne'} else 2 if pk.startswith('holiday#') else 3, -len(s), pk)
    json.dump({'sha': sha, 'order': sorted(man, key=rank), 'pages': man}, open(HERE + 'manifest.json', 'w'), indent=1, ensure_ascii=False)
    print(len(man), 'pages', sum(x['main'] + x['holiday'] for x in man.values()), 'cards')

if __name__ == '__main__':
    if sys.argv[1] == 'cards': build_cards(sys.argv[2:])
    else: figures(sys.argv[2])
