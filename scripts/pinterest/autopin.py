#!/usr/bin/env python3
"""Mahj Matchmaker Pinterest autopin queue (Oct 21, 2026).

Tiffany (Oct 21): every album cover / color card, blog post image and mood board we make
must reach Pinterest for evergreen mahjong searches, without her monitoring it.

Queue: config/pinterest/queue.json  (one item per pin; status pending|scheduled|published|failed|hold|todo)
Pins render to assets/social/pinterest/pins/auto/<id>.jpg (1000x1500).

  python3 scripts/pinterest/autopin.py refresh        # add new album / blog pages from the live sitemap
  python3 scripts/pinterest/autopin.py render <id>..  # render pin images (or 'pending' for all pending)
  python3 scripts/pinterest/autopin.py next [N]       # print the next N pending items (respects notBefore)
  python3 scripts/pinterest/autopin.py mark <id> <status> [postGroupId] [scheduledFor ISO]
  python3 scripts/pinterest/autopin.py check          # curl-verify every pending/scheduled link (must be 200)

Rules baked in: our own work only (album covers, our mood boards/graphics, grids of our covers);
real mahjmatchmaker.com links (curl 200); no "coupon"/"promo" wording; holiday mood boards are
'hold' until the rebuilt files exist (assets/blog/holiday-boards-oct21/); Paige Spearin x TdT
never promoted; holiday items never before notBefore.
"""
import json, os, re, sys, subprocess, datetime, io, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUEUE = os.path.join(REPO, 'config/pinterest/queue.json')
OUT = os.path.join(REPO, 'assets/social/pinterest/pins/auto')
COVERS = os.path.join(REPO, 'assets/covers/albums/uniform-v3')
HCOVERS = os.path.join(REPO, 'assets/covers/holiday')
SITE = 'https://www.mahjmatchmaker.com'
UA = 'Mozilla/5.0 (MahjMatchmaker autopin)'

BOARDS = {
    'Pink Mahjong Tiles and Mat Matches': '908319887286213298',
    'Blue Mahjong Tiles and Mat Matches': '908319887286213299',
    'Green Mahjong Tiles and Mat Matches': '908319887286213300',
    'Neutral Mahjong Tiles and Mat Matches': '908319887286213301',
    'Oh My Mahjong Tile and Mat Matches': '908319887286213303',
    'Christmas Mahjong Mats': '908319887286213304',
    'Holiday Mahjong Table Ideas': '908319887286213305',
    'Mahjong Racks and Rack Colors': '908319887286213306',
    'Amazon Mahjong Finds': '908319887286213307',
    'Mahjong Tile Matches': '908319887286202745',
    'Mahjong Table Inspiration': '908319887286202746',
    'Mahjong Gift Ideas': '908319887286202747',
    'Mahjong Mats & Racks': '908319887286202750',
    'Learn to Play Mahjong': '908319887286202751',
    'Mahjong Discount Codes': '908319887286202752',
}
COLOR_BOARD = {'pink': 'Pink Mahjong Tiles and Mat Matches', 'blue': 'Blue Mahjong Tiles and Mat Matches',
               'green': 'Green Mahjong Tiles and Mat Matches', 'neutral': 'Neutral Mahjong Tiles and Mat Matches'}
HUBS = ['pink', 'blue', 'green', 'yellow-orange', 'purple', 'red', 'neutral', 'brown', 'ivory', 'masculine']
COLOR_WORDS = {'pink': 'pink', 'blue': 'blue', 'green': 'green', 'yellow-orange': 'yellow and orange', 'purple': 'purple',
               'red': 'red', 'neutral': 'neutral', 'brown': 'brown', 'ivory': 'ivory', 'masculine': 'classic'}
UTM = '?utm_source=pinterest&utm_medium=social&utm_campaign=evergreen'

NAVY = (5, 70, 137); PINK = (245, 108, 140); CREAM = (251, 243, 230); WHITE = (255, 255, 255); RED = (150, 24, 40)
W, H = 1000, 1500
CAPRA = os.path.join(REPO, 'assets/fonts/Caprasimo.ttf')
_inter = '/usr/share/fonts/opentype/inter/'
BOLD = _inter + 'Inter-Bold.otf' if os.path.exists(_inter + 'Inter-Bold.otf') else os.path.join(REPO, 'assets/fonts/poppins-latin-700-normal.woff2')
SEMI = _inter + 'Inter-SemiBold.otf' if os.path.exists(_inter + 'Inter-SemiBold.otf') else os.path.join(REPO, 'assets/fonts/poppins-latin-600-normal.woff2')
LOGO = os.path.join(REPO, 'assets/brand/mahjmatchmaker-wordmark.png')


def load():
    return json.load(open(QUEUE)) if os.path.exists(QUEUE) else {'items': []}


def save(q):
    os.makedirs(os.path.dirname(QUEUE), exist_ok=True)
    q['updated'] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    json.dump(q, open(QUEUE, 'w'), indent=1, ensure_ascii=False)


def get(url):
    return subprocess.run(['curl', '-s', '-L', '-A', UA, url], capture_output=True, text=True).stdout


def status(url):
    return subprocess.run(['curl', '-s', '-o', '/dev/null', '-L', '-w', '%{http_code}', '-A', UA, url],
                          capture_output=True, text=True).stdout


def clean_title(t):
    import html
    t = html.unescape(t).split(' — ')[0].strip()
    return t


# ---------------------------------------------------------------- refresh
def refresh():
    q = load(); have = {i['url'] for i in q['items']}
    locs = re.findall(r'<loc>(.*?)</loc>', get(SITE + '/sitemap.xml'))
    hub = {}
    for h in HUBS:
        for s in set(re.findall(r'href="/([a-z0-9-]+)-mahjong-tile-matches"', get(f'{SITE}/{h}-mahjong-tile-matches'))):
            if s not in HUBS: hub.setdefault(s, []).append(h)
    added = 0
    for u in locs:
        u = u.replace('http://', 'https://')
        if u in have: continue
        m = re.match(SITE + r'/([a-z0-9-]+)-mahjong-tile-matches$', u)
        if m and m.group(1) not in HUBS and m.group(1) != '':
            slug = m.group(1); cov = os.path.join(COVERS, slug + '.jpg')
            page = get(u); t = re.search(r'<title>(.*?)</title>', page, re.S)
            title = clean_title(t.group(1)) if t else slug
            brand = 'Oh My Mahjong'
            for b in ['Oh My Mahjong', 'Miss Mahjong', 'Bam Bird', 'Sunday Mahjong', 'LoveShackFancy', 'Mahjong Row']:
                if b in title or b in page[:20000]: brand = b; break
            name = slug.replace('-', ' ').title().replace('2 0', '2.0').replace('Cypress Forest', 'Cypress')
            colors = hub.get(slug, [])
            item = dict(id='album-' + slug, kind='album', url=u, slug=slug, name=name, brand=brand, colors=colors,
                        image=os.path.relpath(cov, REPO) if os.path.exists(cov) else None, status='pending')
            if not item['image']:
                item['status'] = 'todo'; item['note'] = 'No uniform-v3 cover yet: make the cover (doc 86), then render.'
            q['items'].append(item); added += 1
        elif '/blog/' in u and not u.endswith('/blog'):
            q['items'].append(dict(id='blog-' + u.rsplit('/', 1)[1], kind='blog', url=u, status='todo',
                                   note='New blog post: pick our own image (mood board / our graphic / grid of our covers), set title+desc, then pending.'))
            added += 1
    save(q); print(f'refresh: {added} new items')


# ---------------------------------------------------------------- copy
def album_copy(it):
    n, b = it['name'], it['brand']
    cw = [COLOR_WORDS[c] for c in it.get('colors', []) if c not in ('masculine', 'ivory', 'brown')][:2]
    color = (' and '.join(cw) + ' ') if cw else ''
    title = f'{n} Mahjong Tiles: Mat & Rack Matches'
    if len(title) < 60 and b not in title: title = f'{n} Mahjong Tiles by {b}: Mat & Rack Matches'
    desc = (f'Which mahjong mat goes with {b} {n} mahjong tiles? See every mat and rack match I styled for {n}, '
            f'from {color}mahjong mats to racks that pull the tile colors. Ideas for mahjong table decor, '
            f'gifts and your next mahjong set. Save with code MAHJMATCH (affiliate) at participating partner shops. '
            f'#mahjong #mahjongtiles #mahjongmat #mahjongtable #mahjmatchmaker')
    col = next((c for c in it.get('colors', []) if c in COLOR_BOARD), None)
    board = COLOR_BOARD[col] if col else ('Oh My Mahjong Tile and Mat Matches' if b == 'Oh My Mahjong' else 'Mahjong Tile Matches')
    return title[:100], desc, board


# ---------------------------------------------------------------- render
def font(p, s): return ImageFont.truetype(p, s)


def wrap(d, text, path, size, maxw, maxlines=2, minsize=50):
    while size >= minsize:
        f = font(path, size); lines = []; cur = ''
        for w in text.split():
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=f) <= maxw: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
        if len(lines) <= maxlines: return f, lines
        size -= 4
    return f, lines


def fit(d, text, path, size, maxw, minsize=22):
    while size > minsize and d.textlength(text, font=font(path, size)) > maxw: size -= 2
    return font(path, size)


def header(cv, title, sub, accent=NAVY):
    d = ImageDraw.Draw(cv)
    lg = Image.open(LOGO).convert('RGBA'); lg.thumbnail((330, 80)); cv.paste(lg, ((W - lg.width) // 2, 34), lg)
    f, lines = wrap(d, title, CAPRA, 84, W - 90)
    y = 140
    for ln in lines:
        d.text((W // 2, y), ln, font=f, fill=accent, anchor='ma'); y += int(f.size * 1.12)
    fs = fit(d, sub, SEMI, 36, W - 100)
    d.text((W // 2, y + 8), sub, font=fs, fill=(60, 60, 70), anchor='ma')
    return y + 8 + fs.size + 26


def footer(cv, l1, l2='mahjmatchmaker.com  ·  Save with code MAHJMATCH', bg=NAVY):
    l2 = l2 or 'mahjmatchmaker.com'
    d = ImageDraw.Draw(cv); d.rectangle([0, H - 150, W, H], fill=bg)
    d.text((W // 2, H - 122), l1, font=fit(d, l1, BOLD, 46, W - 80, 30), fill=WHITE, anchor='ma')
    d.text((W // 2, H - 62), l2, font=fit(d, l2, SEMI, 32, W - 80), fill=(255, 205, 216), anchor='ma')


def place(cv, im, top, bottom, margin=40, radius=22):
    im = im.convert('RGB'); maxw, maxh = W - 2 * margin, bottom - top
    s = min(maxw / im.width, maxh / im.height); im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x = (W - im.width) // 2; y = top + (maxh - im.height) // 2
    sh = Image.new('RGBA', (im.width + 40, im.height + 40), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([20, 24, im.width + 20, im.height + 24], radius, fill=(0, 0, 0, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(10)); cv.paste(sh, (x - 20, y - 20), sh)
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius, fill=255)
    cv.paste(im, (x, y), m)


def grid(paths, cols=2, cell_ratio=1350 / 1080, gap=18, width=W - 80):
    cw = (width - gap * (cols - 1)) // cols; ch = int(cw * cell_ratio); rows = (len(paths) + cols - 1) // cols
    g = Image.new('RGB', (width, rows * ch + (rows - 1) * gap), CREAM)
    for i, p in enumerate(paths):
        im = Image.open(os.path.join(REPO, p)).convert('RGB')
        s = max(cw / im.width, ch / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
        l = (im.width - cw) // 2; t = (im.height - ch) // 2; im = im.crop((l, t, l + cw, t + ch))
        mk = Image.new('L', im.size, 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, cw - 1, ch - 1], 16, fill=255)
        g.paste(im, ((i % cols) * (cw + gap), (i // cols) * (ch + gap)), mk)
    return g


def fetch_img(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read()))


def render(it):
    os.makedirs(OUT, exist_ok=True)
    cv = Image.new('RGB', (W, H), CREAM)
    accent = RED if it.get('holiday') else NAVY
    if it['kind'] == 'album':
        top = header(cv, it.get('head') or f"{it['name']} mahjong tiles", it.get('sub') or 'Every mat & rack I matched to them')
        place(cv, Image.open(os.path.join(REPO, it['image'])), top, H - 180)
        footer(cv, it.get('cta') or f"See all of {it['name']}'s matches →")
    else:
        top = header(cv, it['head'], it['sub'], accent=accent)
        if it.get('grid'): im = grid(it['grid'], cols=it.get('cols', 2))
        elif it.get('src_url') and it.get('kind') in ('card', 'guide'):
            im = fetch_img(it['src_url'] + ('?format=1500w' if 'squarespace-cdn' in it['src_url'] else ''))
        elif it.get('src_url'): im = fetch_img(it['src_url'])
        else: im = Image.open(os.path.join(REPO, it['image']))
        if it.get('crop_top') or it.get('crop_bottom'):
            im = im.convert('RGB'); im = im.crop((0, it.get('crop_top', 0), im.width, im.height - it.get('crop_bottom', 0)))
        place(cv, im, top, H - 180)
        footer(cv, it['cta'], it.get('cta2', 'mahjmatchmaker.com  \u00b7  Save with code MAHJMATCH'), bg=accent)
    fn = os.path.join(OUT, it['id'] + '.jpg'); cv.convert('RGB').save(fn, quality=88)
    it['pin'] = os.path.relpath(fn, REPO); return fn


# ---------------------------------------------------------------- expand (Oct 21, Tiffany: "spam it and get it filled up")
# Every live album yields many unique pins: its cover (on each of its boards), its colour guide, and its
# match cards (tiles + mat + racks, our own images) in her ranked order. `expand N` adds up to N NEW card
# pins per album per run, plus any missing cover/guide pins. Re-run weekly to keep circulating.
HOLD_SETS = {'jade', 'malachite'}  # Miss Mahjong restock: save for the buying window (Tiffany, Oct 21)
BLOCK_BRANDS = ('paige spearin', 'mahjong studios', 'four winds', 'the mahjong line', 'mahj house rules', 'maison mahj')
SET_NAMES = {'tortoise': 'Classic Tortoise', 'cypress-forest': 'Cypress Forest', 'heritage-2-0': 'Heritage 2.0',
             'sunday-tile-set': 'Sunday', 'shangri-la': 'Shangri La', 'la-fete': 'La Fete', 'glow-wild': 'Glow Wild',
             'lilac-soiree': 'Lilac Soiree', 'preppy-soiree': 'Preppy Soiree', 'spring-love': 'Spring Love',
             'palm-royale': 'Palm Royale', 'papaya-spritz': 'Papaya Spritz'}
SET_BRAND = {'jade': 'Miss Mahjong', 'malachite': 'Miss Mahjong', 'tortoise': 'Bam Bird Boutique',
             'sunday-tile-set': 'Sunday Mahjong', 'cypress-forest': 'Mahjong Row & Co.', 'coquette': 'LoveShackFancy x Oh My Mahjong'}
HUB_BOARD = {'pink': 'Pink Mahjong Tiles and Mat Matches', 'blue': 'Blue Mahjong Tiles and Mat Matches',
             'green': 'Green Mahjong Tiles and Mat Matches', 'neutral': 'Neutral Mahjong Tiles and Mat Matches',
             'ivory': 'Neutral Mahjong Tiles and Mat Matches', 'brown': 'Neutral Mahjong Tiles and Mat Matches'}
TAGS = ['#mahjong #mahjongtiles #mahjongmat #mahjmatchmaker', '#mahjongmat #mahjongtable #mahjongdecor #mahjmatchmaker',
        '#americanmahjong #mahjongtiles #mahjongset #mahjmatchmaker', '#mahjongracks #mahjongmat #mahjongtiles #mahjmatchmaker']
CODE = 'Save with code MAHJMATCH (affiliate) at participating partner shops.'


def scrape_album(slug):
    import html as H
    p = get(f'{SITE}/{slug}-mahjong-tile-matches'); cards = []; seen = set()
    for m in re.finditer(r'<img src="(https://(?:images\.squarespace-cdn\.com|cdn\.jsdelivr\.net)/[^"?]+)[^"]*"[^>]*alt="([^"]*mahjong tiles with[^"]*)"', p):
        url, alt = m.group(1), H.unescape(m.group(2))
        if url in seen: continue
        seen.add(url)
        txt = re.sub(r'\s+', ' ', H.unescape(re.sub('<[^>]+>', ' ', p[m.end():m.end() + 5000])))
        mm = re.search(r'^\s*(?:\S+\s+){0,6}?(\d{1,2}) (.+?) \+ (.+?) (?:Mat )?by ', txt)
        after = re.sub(r' (holiday )?mahjong mat$', '', alt.split(' mahjong tiles with ', 1)[1]).strip()
        base = re.sub(r' Mat$', '', (mm.group(3) if mm else '').strip()).strip()
        brand = after[:after.lower().rfind(base.lower())].strip() if base and base.lower() in after.lower() else ''
        nx = re.search(r' Save \d{1,2} ', txt[5:]); seg = txt[:nx.start() + 5] if nx else txt[:1500]
        rk = re.search(r'Rack (?:matches|shown): (.+?)(?: Save|$)', seg)
        cards.append(dict(img=url, n=int(mm.group(1)) if mm else 99, mat=base or after, brand=brand,
                          retired='Retired' in seg[:300] or 'is retired' in seg,
                          holiday='holiday' in (url + alt).lower(),
                          racks=[r.strip() for r in rk.group(1).split('·') if r.strip()][:3] if rk else []))
    cards.sort(key=lambda c: c['n'])
    g = re.findall(r'https://(?:images\.squarespace-cdn\.com|cdn\.jsdelivr\.net)/[^"?]+(?:color-guide|tile-edit-moodboard)[^"?]*\.jpg', p)
    return cards, (g[0] if g else None)


def boards_for(slug, hubs, brand):
    b = []
    for h in hubs:
        if h in HUB_BOARD and HUB_BOARD[h] not in b: b.append(HUB_BOARD[h])
    if 'Oh My Mahjong' in (brand or ''): b.append('Oh My Mahjong Tile and Mat Matches')
    if 'masculine' in hubs: b.append('Mahjong Gift Ideas')
    if not b: b.append('Mahjong Tile Matches')
    return b


def expand(per_album=3):
    q = load(); items = q['items']; have = {i['id'] for i in items}
    used_img = {i.get('src_url') for i in items}
    hub = {}
    for h in HUBS:
        for s in set(re.findall(r'href="/([a-z0-9-]+)-mahjong-tile-matches"', get(f'{SITE}/{h}-mahjong-tile-matches'))):
            if s not in HUBS: hub.setdefault(s, []).append(h)
    locs = re.findall(r'<loc>(.*?)</loc>', get(SITE + '/sitemap.xml'))
    slugs = [m.group(1) for u in locs for m in [re.match(r'https?://www\.mahjmatchmaker\.com/([a-z0-9-]+)-mahjong-tile-matches$', u)] if m and m.group(1) not in HUBS]
    added = 0
    for slug in slugs:
        if slug in HOLD_SETS: continue
        name = SET_NAMES.get(slug, slug.replace('-', ' ').title())
        brand = SET_BRAND.get(slug, 'Oh My Mahjong')
        hubs = hub.get(slug, []); bl = boards_for(slug, hubs, brand)
        url = f'{SITE}/{slug}-mahjong-tile-matches'; link = url + UTM
        cards, guide = scrape_album(slug); N = len(cards)
        cw = ' and '.join(COLOR_WORDS[c] for c in hubs if c not in ('masculine', 'ivory', 'brown'))[:30]
        # cover on every board it belongs to
        cov = os.path.join(COVERS, slug + '.jpg')
        on = {i.get('board') for i in items if i.get('url') == url and i['kind'] in ('album', 'cover2', 'oct19')}
        for k, b in enumerate(bl):
            iid = f'cover2-{slug}-{BOARDS[b][-3:]}'
            if b in on or iid in have or not os.path.exists(cov): continue
            heads = [f'What mat goes with {name} tiles?', f'{name} mahjong tiles', f'Mats that match {name}']
            items.append(dict(id=iid, kind='cover2', url=url, link=link, status='pending', prio=25, image=os.path.relpath(cov, REPO),
                              board=b, head=heads[k % 3], sub=f'{N} mat & rack matches, styled' if N else 'Every mat & rack I matched',
                              cta=f"See all of {name}'s matches →", cta2='mahjmatchmaker.com',
                              title=(f'What Mahjong Mat Goes With {name} Tiles? {N} Mat and Rack Matches' if N else f'What Mahjong Mat Goes With {name} Tiles?')[:100],
                              desc=f'Wondering what mahjong mat goes with {brand} {name} tiles? I styled {name} with {N or "every"} mahjong mats and racks, {("from " + cw + " mats ") if cw else ""}to classic neutrals, so you can see the whole table before you buy. {CODE} {TAGS[k % 4]}'))
            have.add(iid); added += 1
        if guide and f'guide-{slug}' not in have and guide not in used_img:
            items.append(dict(id=f'guide-{slug}', kind='guide', url=url, link=link, status='pending', prio=30, src_url=guide, board=bl[0],
                              head=f'{name} tiles color guide', sub='The colors, racks & mats that pull them out', cta=f"See all of {name}'s matches →", cta2='mahjmatchmaker.com',
                              title=f'{name} Mahjong Tiles Color Guide: Matching Mahjong Mats and Racks'[:100],
                              desc=f'The {brand} {name} mahjong tiles color guide: every color in the set, the mahjong racks that match, and mats that bring those colors out. Pin it before you shop for a mahjong mat. {CODE} {TAGS[2]}'))
            have.add(f'guide-{slug}'); added += 1
        k = 0
        for c in cards:
            if k >= per_album: break
            iid = f'card-{slug}-{c["n"]:02d}'
            if iid in have or c['img'] in used_img or c['retired'] or c['holiday'] or c['n'] == 99: continue
            if any(x in (c['brand'] + ' ' + c['mat']).lower() for x in BLOCK_BRANDS): continue
            if slug in ('amara', 'birdie', 'cypress-forest', 'emerald', 'gatsby', 'glow-wild', 'heritage-2-0', 'heritage', 'la-fete', 'lagoon',
                        'moonlight', 'nantucket', 'osler', 'palm-royale', 'pearlescent', 'pippa', 'seabreeze', 'talulah') and c['n'] == 1: continue  # #1 pinned Oct 19
            mat, mb = c['mat'], c['brand'] or 'a partner brand'
            cnt = sum(1 for i in items if i['kind'] == 'card'); j = cnt % 4
            rot = [bl[0], 'Mahjong Mats & Racks', 'Mahjong Racks and Rack Colors' if c['racks'] else 'Mahjong Tile Matches',
                   bl[0], 'Mahjong Table Inspiration', bl[-1] if len(bl) > 1 else 'Mahjong Tile Matches', 'Mahjong Tile Matches']
            rb = rot[(cnt + k) % len(rot)]
            r1 = c['racks'][0] if c['racks'] else ''
            titles = [f'{name} Mahjong Tiles With the {mat} Mahjong Mat by {mb}',
                      f'What Mat Goes With {name} Mahjong Tiles? Try {mb} {mat}',
                      f'Mahjong Racks for {name} Tiles: {r1} With the {mat} Mat' if r1 else f'{name} Mahjong Table: {mat} Mat and Matching Racks',
                      f'{mat} Mahjong Mat by {mb}: A Pretty Match for {name} Tiles']
            racks = ', '.join(c['racks'][:2])
            descs = [f'{brand} {name} mahjong tiles on the {mat} mahjong mat by {mb}{", with " + racks + " racks" if racks else ""}. It is one of {N} mat and rack matches in the {name} album, so see them all before you pick your mat. {CODE} {TAGS[0]}',
                     f'What mahjong mat goes with {name} tiles? The {mb} {mat} mat is one of my {N} {name} matches{" (racks: " + racks + ")" if racks else ""}. Browse the whole album for more mahjong mat and rack ideas. {CODE} {TAGS[1]}',
                     f'Racks that pull the colors out of {name} mahjong tiles: {racks or "see the album"}, styled on the {mat} mahjong mat by {mb}. Mahjong table decor ideas from all {N} {name} matches. {CODE} {TAGS[3]}',
                     f'The {mat} mahjong mat by {mb} with {brand} {name} tiles{" and " + racks + " racks" if racks else ""}. Love it? There are {N} more mat and rack matches for {name} on mahjmatchmaker.com. {CODE} {TAGS[2]}']
            items.append(dict(id=iid, kind='card', url=url, link=link, status='pending', prio=35 + c['n'], src_url=c['img'], board=rb,
                              head=f'{name} tiles + the {mat} mat', sub=f'{mat} mat by {mb}', cta=f"See all {N} of {name}'s matches →",
                              title=titles[j][:100], desc=descs[j][:500]))
            have.add(iid); used_img.add(c['img']); k += 1; added += 1
    save(q); print(f'expand: {added} new items')


# ---------------------------------------------------------------- cli
def main():
    a = sys.argv[1:] or ['help']; q = load(); byid = {i['id']: i for i in q['items']}
    if a[0] == 'refresh': refresh()
    elif a[0] == 'expand':  # Oct 21: card / guide / 2nd-cover pins from live album pages
        n = int(a[1]) if len(a) > 1 else 3
        expand(n)
    elif a[0] == 'render':
        ids = [i['id'] for i in q['items'] if i['status'] == 'pending'] if a[1:] == ['pending'] else a[1:]
        for i in ids:
            it = byid[i]
            if it['kind'] == 'album' and not it.get('title'):
                it['title'], it['desc'], it['board'] = album_copy(it)
            it['boardId'] = BOARDS[it['board']]
            print(render(it))
        save(q)
    elif a[0] == 'next':
        n = int(a[1]) if len(a) > 1 else 3; now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
        out = [i for i in q['items'] if i['status'] == 'pending' and i.get('notBefore', '0') <= now]
        out.sort(key=lambda i: i.get('prio', 50))
        print(json.dumps(out[:n], indent=1, ensure_ascii=False))
    elif a[0] == 'mark':
        it = byid[a[1]]; it['status'] = a[2]
        if len(a) > 3: it['postGroupId'] = a[3]
        if len(a) > 4: it['scheduledFor'] = a[4]
        save(q); print(it['id'], it['status'])
    elif a[0] == 'check':
        bad = 0
        for it in q['items']:
            if it['status'] in ('pending', 'scheduled') and it.get('link'):
                c = status(it['link'])
                if c != '200': bad += 1; print('BAD', c, it['id'], it['link'])
        print('check done, bad =', bad)
    else: print(__doc__)


if __name__ == '__main__':
    main()
