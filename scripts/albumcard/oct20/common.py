"""Shared helpers for the Oct 20 owed-album builds (Malachite insert, Brownstone Bloom, Dec 1994, Spirit, Petalee).
Mat shop links: data.json M, then work/pub/catalog.json. Rack links: data.json R + links already used in live blocks.
Brand discount pages: the /<brand>-discount-code links already used in live/staged album blocks.
Footer rule (Oct 18, papaya_spritz_build.py): every card carries MAHJMATCH; partner % where known."""
import json, re, glob, html, unicodedata, sys
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'scripts/albumcard')
from tdt_policy import card_code, shop_url  # TdT: no visible code on their cards (Oct 30)
e = lambda s: html.escape(s, quote=True)
D = json.load(open(R + 'data.json'))
CAT = json.load(open(R + 'work/pub/catalog.json'))
PARTNERS = {b[0] for b in CAT['B']}
PCT = {}  # Oct 21 (Tiffany): card code bands ALWAYS say 10% (the safe floor: 'it might be more, but it's never less'). Real brand % lives on brand pages. Gate: scripts/albumcard/codeband_lint.py
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', s.replace('&', 'and')).strip()
def slug(s): return re.sub(r'[^a-z0-9]+', '-', norm(s)).strip('-')
MATS = {}
for m in D['M']: MATS.setdefault((norm(m[0]), norm(m[1])), m[2])
def _catmats():
    out = {}
    M = CAT.get('M') or []
    for m in M:
        if isinstance(m, list) and len(m) > 2 and isinstance(m[2], str): out.setdefault((norm(m[0]), norm(m[1])), m[2])
    return out
CMATS = _catmats()
def mat_url(name, brand):
    k = (norm(name), norm(brand))
    if k in MATS: return MATS[k]
    if k in CMATS: return CMATS[k]
    for (n, b), u in list(MATS.items()) + list(CMATS.items()):
        if b == k[1] and (n.startswith(k[0]) or k[0].startswith(n)): return u
    return None
# rack links
U = {n: u for n, u in D['R']}
BRANDPG = {}
for f in glob.glob(R + 'site/livepatch/**/*.html', recursive=True):
    s = open(f, errors='ignore').read()
    for u, n in re.findall(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', s):
        n = html.unescape(n).strip(); u = html.unescape(u)
        if n.startswith(('Bird & Bamboo', 'Peace Love', 'Middle & Main', 'Miss Mahjong', 'Mahjong Row', 'Sunday', 'Bam Bird', 'Tigre', 'Oh My', 'My Fair', 'Hip Hip')) and u.startswith('http'):
            U.setdefault(n, u)
    for u, n in re.findall(r'<a href="(/[a-z0-9-]+-discount-code)">([^<]+)</a>', s):
        BRANDPG.setdefault(html.unescape(n).strip(), u)
U.setdefault('Miss Mahjong Brass & Tortoise', 'https://missmahjong.com/products/dark-tortoise-and-brass-acrylic-racks?ref=mahjmatch')
BB = next(u for n, u in U.items() if n.startswith('Bird & Bamboo'))
BBBASE = re.sub(r'variant=\d+&?', '', BB).replace('?&', '?')
MISSING_LINKS = set()
def rack_link(n):
    u = U.get(n)
    if not u and n.startswith('Bird & Bamboo'): u = BBBASE
    if not u: MISSING_LINKS.add(n); return e(n)
    return f'<a href="{e(u)}" target="_blank" rel="sponsored noopener">{e(n)}</a>'
def footer(brand, retired=False):
    if retired or brand not in PARTNERS: return '10% OFF  USE CODE : MAHJMATCH'
    if brand in NOPCT: return 'SAVE WITH CODE : MAHJMATCH'
    return f"{PCT.get(brand, '10%')} OFF  USE CODE : MAHJMATCH"
def figure(n, img, tile_full, set_name, mat, brand, tile_racks, mat_racks, url=None, cls='mm3-c', retired=False):
    """One album card, same markup as the live/staged album blocks (Papaya + Malachite holiday captions)."""
    by = f'<a href="{BRANDPG[brand]}">{e(brand)}</a>' if brand in BRANDPG else e(brand)
    url = shop_url(url or mat_url(mat, brand), brand)
    btn = f'<a class="mm3-btn" href="{e(url)}" target="_blank" rel="sponsored noopener">Shop the {e(mat)} Mat</a>' if url else ''
    if not url: MISSING_LINKS.add(f'MAT {mat} ({brand})')
    code = card_code(brand) if brand in PARTNERS and not retired else ''
    cap = 'Match the tiles: ' + ' · '.join(rack_link(x) for x in tile_racks)
    if mat_racks: cap += '<br>Match the mat: ' + ' · '.join(rack_link(x) for x in mat_racks)
    alt = f'{tile_full} mahjong tiles with {brand} {mat} mahjong mat'
    return (f'<figure class="{cls}"><div class="mm3-im"><img src="{img}" data-lb="" alt="{e(alt)}" loading="lazy" width="750" height="938">'
            f'<a class="mm3-pin" href="#" target="_blank" rel="noopener" aria-label="Save to Pinterest">Save</a></div><figcaption>'
            f'<span class="mm3-n">{n:02d}</span><h3>{e(set_name)} + {e(mat)}</h3><span class="mm3-by">Mat by {by}</span>'
            f'<div class="mm3-l">{btn}{code}</div><div class="mm3-rk" style="margin-top:8px;font-size:.82em;line-height:1.55">{cap}</div></figcaption></figure>')
def contact(files, labels, out, cols=5, w=300):
    from PIL import Image, ImageDraw, ImageFont
    h = int(w * 1350 / 1080); lab = 34
    rows = (len(files) + cols - 1) // cols
    S = Image.new('RGB', (cols * w, rows * (h + lab)), 'white'); d = ImageDraw.Draw(S)
    try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    except Exception: F = ImageFont.load_default()
    for i, (f, l) in enumerate(zip(files, labels)):
        im = Image.open(f).convert('RGB'); im.thumbnail((w, h)); x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(im, (x, y)); d.text((x + 4, y + h + 4), l[:44], fill='black', font=F)
    S.save(out, quality=82)
