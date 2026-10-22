#!/usr/bin/env python3
"""Build assets/search/search-index.json for the site-wide search (curl-based).

Reads the LIVE site only (curl -s): sitemap.xml, the album hub, the live Mat Gallery
(/mahjong-mats code block JSON, same rows as site/livepatch/matgallery/matgallery-v5.html),
every album page, the holiday matches page, brand/code pages, blog posts and main pages.
Writes a compact index plus small webp thumbnails (assets/search/thumbs/), regenerating a
thumb only when its source URL changed (assets/search/thumbs.json).

Usage:  python3 scripts/search/build_index.py            (from anywhere)
        python3 scripts/search/build_index.py --no-thumbs
        python3 scripts/search/build_index.py --debug     (lists album captions not found in the gallery)
Then commit + push, and re-pin site/livepatch/search/header-injection.html to the new commit
(python3 site/livepatch/search/pin.py <commit>), warm, and replace the Code Injection snippet.

Index layout (all arrays, to keep it small):
  m  gallery mats   [img key, name, brand, shop url, retired 0/1, colour sections, brand guide path,
                     album idxs, one-to-watch 0/1, silent keywords]
  x  album-only mats (in an album caption but not in the gallery)
                    [name, brand, album idxs, shop url, retired 0/1, card thumb ('@rel' under thumbs/ or url), keywords,
                     full card image url]
  a  albums         [path, set name, brand, cover url, hub colours, kind 0 album/1 colour hub/2 holiday,
                     n mats, description, mats in caption order (m idx, or -(x idx + 1) for album-only mats)]
  p  pages          [path, title, kind brand|blog|page, description, image, code, pct, brand]
"""
import html, io, json, os, re, subprocess, sys, time, unicodedata
from concurrent.futures import ThreadPoolExecutor

SITE = 'https://www.mahjmatchmaker.com'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'assets', 'search')
THUMBS = os.path.join(OUT, 'thumbs')
MAIN_PAGES = ['', 'mahjong-tile-matches', 'mahjong-mats', 'christmas-mahjong-mats', 'holiday-mahjong-matches',
              'find-your-match', 'mahjong-discount-codes', 'blog', 'about', 'mahj-matchmaker-community',
              'request-an-album', 'first-mahjong-racks-to-buy', 'bird-and-bamboo-rack-colors', 'share-your-table',
              'private-mahjong-lessons', 'events', 'rentals', 'links']
SKIP = {'home', 'mahj-matchmaker-community-old'}
GENERIC_OG = 'share-wide-1200x630'
# colour hub album pages (/<x>-mahjong-tile-matches). Coquette is a real album (LoveShackFancy x OMM), not a hub.
COLOR_HUBS = {'pink', 'blue', 'green', 'yellow-orange', 'orange', 'purple', 'neutral', 'masculine', 'red',
              'brown', 'ivory', 'teal'}

# ---------------------------------------------------------------- silent theme keywords
# (regex on the normalised mat name, keywords added). Name words only, word-bounded, so brand
# names (Peace LOVE Mahjong, Tigre de TARTAN, Bird & BAMBOO) never trigger a theme.
THEMES = [
    (r'\b(halloween|spooky|spook\w*|witch\w*|ghost\w*|haunt\w*|raven|bats?|boo|hocus|pocus|skull\w*|creep\w*|cauldron)\b',
     'halloween spooky october fall'),
    (r'\bpumpkins?\b', 'pumpkin halloween fall autumn harvest'),
    (r'\b(fall|autumn|harvest|thanksgiving|maple|acorn\w*)\b', 'fall autumn harvest'),
    (r'\b(valentines?|cupid|hearts?|sweetheart|xoxo|amour)\b|❤', 'valentine valentines hearts love'),
    (r'\b(freedom|patriot\w*|americana|usa|july|fourth|stars and stripes|uncle sam)\b',
     'patriotic 4th of july fourth of july stars and stripes americana usa'),
    (r'\b(st patrick\w*|clovers?|shamrocks?|irish|leprechaun)\b', 'st patricks day clover shamrock lucky irish'),
    (r'\b(easter|bunny|bunnies|eggs? hunt|chicks?)\b', 'easter bunny spring'),
    (r'\b(derby|kentucky|equestrian|jockey)\b|(?<!year of the )\bhorses?\b', 'kentucky derby horse equestrian'),
    (r'\b(leopards?|cheetahs?|tigers?|zebras?|giraffe|safari|jaguar|animal print|snake ?skin|python)\b',
     'animal print leopard cheetah'),
    (r'\b(gingham|plaid|tartan|check|checks|checkered|checkerboard|checkers|buffalo check|houndstooth)\b',
     'plaid gingham tartan check checkered'),
    (r'\b(stripes?|striped|cabana|ticking|seersucker)\b', 'stripe stripes striped'),
    (r'\b(chinoiserie|toile|pagoda|ginger jar)\b', 'chinoiserie toile grandmillennial'),
    (r'\b(floral|flowers?|blooms?|bloom\w*|rose|roses|peony|peonies|garden|botanical|blossoms?|poppies|poppy|lily|lilies|tulips?|daisy|daisies|hydrangea\w*|lotus|magnolia)\b',
     'floral flowers'),
    (r'\b(palm|palms|tropical|beach|coastal|seaside|shell|shells|ocean|nautical|sea|island|cabana|lagoon|coral)\b',
     'coastal beach tropical summer'),
    (r'\b(lemons?|citrus|limoncello|oranges?|cherr(y|ies)|strawberr(y|ies)|fruit\w*|peach\w*)\b', 'fruit summer'),
    (r'\b(year of the (dragon|horse|snake|rabbit|tiger)|yotd|lunar)\b', 'lunar new year year of the'),
    (r'\b(ski|skis|apres|alpine|snow|snowy|snowflakes?|snowman|winter|wintry|chalet|ski sweater|icicles?|glacier|lodge)\b', 'winter ski snow'),
    (r'\b(christmas|xmas|noel|santa|merry|jolly|yule\w*|mistletoe|poinsettia|nutcracker|sugarplum|candy cane|ornament\w*|wreath|evergreen|reindeer|rudolph|tinsel\w*|sleigh|elf|elves|holly)\b',
     'christmas holiday'),
    (r'\b(hanukkah|chanukah|menorah|dreidel|hanukah)\b', 'hanukkah holiday'),
    (r'\b(velvet|vegan leather|leatherette|neoprene|solid)\b', 'solid'),
]
# themes read off the mat PHOTO by Claude (Oct 21 contact-sheet pass) where the name does not say it.
# img key -> extra keywords. Only obvious ones.
PHOTO_THEMES_FILE = os.path.join(ROOT, 'config', 'search-photo-themes.json')
COLOR_WORDS = {
    'pink': 'pink blush rose', 'red': 'red', 'orange': 'orange peach coral', 'yellow': 'yellow mustard gold',
    'green': 'green sage emerald', 'teal': 'teal aqua turquoise', 'blue': 'blue navy cobalt periwinkle',
    'purple': 'purple lilac lavender violet', 'neutral': 'neutral ivory cream beige', 'earthy': 'earthy brown tan',
    'dark': 'dark moody', 'bw': 'black white black and white', 'pastel': 'pastel pastels', 'brights': 'bright brights',
    'florals': 'floral flowers', 'animal': 'animal print leopard cheetah', 'simple': 'simple solid',
}


def curl(url, binary=False):
    for i in range(3):
        r = subprocess.run(['curl', '-s', '-L', '--max-time', '40', url], capture_output=True)
        if r.returncode == 0 and r.stdout:
            return r.stdout if binary else r.stdout.decode('utf-8', 'replace')
        time.sleep(1 + i)
    return b'' if binary else ''


def strip(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s or ''))).strip()


def text_lines(h):
    m = h.find('<main')
    t = h[m if m > -1 else 0:]
    t = re.sub(r'<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>', '', t, flags=re.S)
    t = html.unescape(re.sub(r'<[^>]+>', '\n', t))
    return [re.sub(r'\s+', ' ', l).strip() for l in t.split('\n') if l.strip()]


def meta(h, prop):
    m = re.search(r'<meta (?:property|name)="%s" content="([^"]*)"' % re.escape(prop), h)
    return html.unescape(m.group(1)).strip() if m else ''


def clean_title(t):
    return re.sub(r'\s*[—–-]\s*Mahj Matchmaker\s*$', '', t).strip()


def first_img(h):
    m = h.find('<main')
    for src in re.findall(r'<img[^>]+?(?:data-src|src)="([^"]+)"', h[m if m > -1 else 0:]):
        s = html.unescape(src)
        if not s.startswith(('http', '//')) or 'logo' in s.lower() or 'Headshot' in s or GENERIC_OG in s:
            continue
        return 'https:' + s if s.startswith('//') else s
    return ''


def small_img(u):
    """Return a small version of an image URL when the host supports it."""
    if not u:
        return ''
    if 'squarespace' in u:
        return re.sub(r'\?.*$', '', u) + '?format=300w'
    if 'cdn.shopify.com' in u:
        u = re.sub(r'([?&])width=\d+', r'\1width=300', u)
        return u if 'width=' in u else u + ('&' if '?' in u else '?') + 'width=300'
    return u


def norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r'\(retired\)|mahjong mat|game mat|\bmat\b', ' ', s)
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def kw_norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower().replace('❤️', ' ❤ ')
    return re.sub(r'[^a-z0-9❤]+', ' ', s).strip()


STOP = {'the', 'a', 'and', 'of', 'mat', 'mats', 'x', 'in'}


def toks(s):
    s = norm(s).replace('yotd', 'year of the dragon')
    t = [w for w in s.split() if w not in STOP]
    if t and t[-1].isdigit():
        t = t[:-1]
    return t


def brand_key(b):
    b = norm(b).replace('mahjongg', 'mahjong')
    return ' '.join(w for w in b.split() if w not in ('co', 'company', 'the', 'mahjong'))


def fuzzy_mat(R, name, brand):
    """Album caption -> gallery row: same brand, every caption word equal to (or a prefix of) a word in
    the gallery name; unique hit only."""
    a, b = toks(name), brand_key(brand)
    if not a:
        return None

    def ok(x):
        g = toks(x[1])
        return all(any(w == v or (len(w) >= 1 and v.startswith(w) and (len(w) == 1 or len(w) >= 4)) for v in g) for w in a)
    hits = [i for i, x in enumerate(R) if brand_key(x[2]) == b and ok(x)]
    return hits if 1 <= len(hits) <= 3 else None  # 2-3 hits = variants of one design (Premium / Double-Sided)


def themes(name, secs=(), holiday=False):
    n = kw_norm(name)
    out = []
    for rx, words in THEMES:
        if re.search(rx, n):
            out += words.split()
    if holiday:
        out.append('holiday')
        if not re.search(r'hanukkah|chanukah|menorah|dreidel|pumpkin|halloween|fall|autumn|harvest', n) and \
                not re.search(r'\b(ski|apres|alpine|snow|snowflakes?|winter|chalet|glacier)\b', n):
            out += ['christmas']
        if re.search(r'\b(ski|apres|alpine|snow|snowy|snowflakes?|winter|chalet|glacier)\b', n):
            out += ['winter', 'ski', 'snow']
    for s in secs:
        out += COLOR_WORDS.get(s, '').split()
    seen, res = set(), []
    for w in out:
        if w not in seen and w not in n.split():
            seen.add(w)
            res.append(w)
    return ' '.join(res)


FIG = re.compile(r'<figure class="mm3-c[^"]*">(.*?)</figure>', re.S)


def album_cards(h):
    """Every match card on an album page: (mat name, brand, card img, shop url, retired, pick)."""
    out = []
    for f in FIG.findall(h):
        t = re.search(r'<h3>(.*?)</h3>', f, re.S)
        if not t:
            continue
        cap = strip(t.group(1))
        mm = re.match(r'^(.{1,60}?) \+ (.{2,90})$', cap)
        if not mm:
            continue
        by = re.search(r'class="mm3-by">(.*?)</span>', f, re.S)
        brand = re.sub(r'^Mat by\s*', '', strip(by.group(1))) if by else ''
        tag = re.search(r'\s+(Retired|Holiday|New)$', brand)
        brand = brand[:tag.start()] if tag else brand
        img = re.search(r'<img[^>]+src="([^"]+)"', f)
        shop = re.search(r'<a class="mm3-btn" href="([^"]+)"', f)
        out.append((mm.group(2).strip(), brand, html.unescape(img.group(1)) if img else '',
                    html.unescape(shop.group(1)) if shop else '', 1 if (re.search(r'>\s*Retired\s*<', f) or (tag and tag.group(1) == 'Retired')) else 0,
                    1 if 'mm3-hstar' in f else 0))
    return out


def main():
    do_thumbs = '--no-thumbs' not in sys.argv
    os.makedirs(OUT, exist_ok=True)
    sm = curl(SITE + '/sitemap.xml')
    urls = [u.replace(SITE, '').strip('/') for u in re.findall(r'<loc>([^<]+)</loc>', sm)]
    if len(urls) < 50:
        sys.exit('sitemap fetch failed (%d urls)' % len(urls))
    slugs = [u for u in urls if u not in SKIP]
    pages = sorted(set(slugs) | set(MAIN_PAGES))
    with ThreadPoolExecutor(8) as ex:
        H = dict(zip(pages, ex.map(lambda s: curl(SITE + '/' + s), pages)))
    bad = [s for s in pages if len(H[s]) < 2000]
    if bad:
        print('WARN short/failed pages:', bad, file=sys.stderr)

    # ---- Mat Gallery (live code block JSON) ----
    g = H['mahjong-mats']
    R = json.loads(re.search(r'<script type="application/json"[^>]*>(.*?)</script>', g, re.S).group(1))
    mb = re.search(r"B='(https://cdn\.jsdelivr\.net/[^']+)'", g).group(1)
    ibm = re.search(r'IB=(\{[^}]*\})', g)
    ib = json.loads(ibm.group(1)) if ibm else {}
    sec_lab = dict(re.findall(r'data-f="([a-z]+)"[^>]*>([^<]+)<', g))
    sec_lab.pop('all', None)
    sec_lab = {k: html.unescape(v).strip() for k, v in sec_lab.items()}

    # ---- Album hub: slug -> cover, brand, set, colour ----
    hub = H['mahjong-tile-matches']
    covers, colors = {}, {}
    cur = None
    for m in re.finditer(r'<h3 class="mmalb-ch" id="color-([a-z-]+)"|<a class="mmalb-c" href="/([a-z0-9-]+)"><img src="([^"]+)"[^>]*><span><small>([^<]*)</small>([^<]*)</span>', hub):
        if m.group(1):
            cur = m.group(1)
            continue
        s = m.group(2)
        covers.setdefault(s, (m.group(3), html.unescape(m.group(4)), html.unescape(m.group(5))))
        if cur:
            colors.setdefault(s, [])
            if cur not in colors[s]:
                colors[s].append(cur)

    # ---- Albums ----
    albums, album_mats = [], {}
    for s in [u for u in slugs if u.endswith('tile-matches')]:
        h = H.get(s, '')
        if not h:
            continue
        hubish = s == 'mahjong-tile-matches' or s.replace('-mahjong-tile-matches', '') in COLOR_HUBS
        title = clean_title(meta(h, 'og:title') or s)
        cov, brand, setname = covers.get(s, ('', '', ''))
        if not setname:
            setname = re.split(r' Mahjong| Tile Matches| Matches', title)[0].strip()
        if not brand:
            parts = [p.strip() for p in title.split('|')]
            brand = parts[-1] if len(parts) > 2 and 'Pairing' not in parts[-1] else ''
        if not cov:
            cov = first_img(h)
        cards = album_cards(h)
        if s == 'mahjong-tile-matches':
            setname, brand = 'All tile match albums', ''
        elif hubish:
            setname, brand = re.sub(r' Mahjong.*$', '', title) + ' tile matches', ''
            cards = []
        album_mats[len(albums)] = cards
        albums.append(['/' + s, setname, brand, small_img(cov), colors.get(s, []), 1 if hubish else 0,
                       len({(c[0], c[1]) for c in cards}), meta(h, 'description')[:160]])
    # holiday page: the page itself + one entry per holiday tile set section (anchors)
    hh = H.get('holiday-mahjong-matches', '')
    if hh:
        albums.append(['/holiday-mahjong-matches', 'Holiday tile matches', 'Christmas, Hanukkah & Winter',
                       small_img(meta(hh, 'og:image')), [], 2, 0, meta(hh, 'description')[:160]])
        album_mats[len(albums) - 1] = []
        secs = list(re.finditer(r'<section class="mm3-hol" id="([a-z0-9-]+)"[^>]*><h2>(.*?)</h2>', hh))
        for k, m in enumerate(secs):
            chunk = hh[m.start(): secs[k + 1].start() if k + 1 < len(secs) else len(hh)]
            name = strip(m.group(2))
            cv = re.search(r'<img class="mmhol-cv" src="([^"]+)"', chunk)
            cards = album_cards(chunk)
            setn = re.sub(r'\s*holiday matches$', '', name)
            album_mats[len(albums)] = cards
            albums.append(['/holiday-mahjong-matches#' + m.group(1), setn + ' (holiday)', 'Holiday matches',
                           cv.group(1) if cv else small_img(cards[0][2] if cards else ''), [], 2, len({(c[0], c[1]) for c in cards}),
                           strip(re.search(r'<p class="mm3-sub">(.*?)</p>', chunk).group(1)) if 'mm3-sub' in chunk else ''])

    # ---- Mats ----
    key = {}
    for i, x in enumerate(R):
        key.setdefault((norm(x[1]), brand_key(x[2])), i)
    mat_albums, extra, unmatched = {}, {}, 0
    order = {}  # album idx -> mats in her caption order (her top picks first)
    for ai, cards in album_mats.items():
        od = order.setdefault(ai, [])
        for name, brand, img, shop, ret, pick in cards:
            i = key.get((norm(name), brand_key(brand)))
            hits = [i] if i is not None else fuzzy_mat(R, name, brand)
            if not hits and re.search(r'mahjong studios|four winds', brand or '', re.I):
                continue  # removed brands (Tiffany Oct 20): no mat cards/shop links in search either
            if not hits:
                unmatched += 1
                e = extra.setdefault((name, brand), {'a': [], 'shop': '', 'ret': ret, 'img': ''})
                if ai not in e['a']:
                    e['a'].append(ai)
                e['shop'] = e['shop'] or shop
                e['img'] = e['img'] or img
                e['ret'] = min(e['ret'], ret) if e['shop'] else ret
                if '--debug' in sys.argv:
                    print('  unmatched:', albums[ai][0], '|', name, '|', brand, file=sys.stderr)
                if ('x', name, brand) not in od:
                    od.append(('x', name, brand))
                continue
            for i in hits:
                if i not in od:
                    od.append(i)
                mat_albums.setdefault(i, [])
                if ai not in mat_albums[i]:
                    mat_albums[i].append(ai)
    photo_kw = {}
    if os.path.exists(PHOTO_THEMES_FILE):
        photo_kw = {k: v for k, v in json.load(open(PHOTO_THEMES_FILE)).get('mats', {}).items()}
    mats = []
    for i, x in enumerate(R):
        secs = [c for c in x[5] if c in sec_lab]
        also = [c for c in (x[8] or []) if c in sec_lab and c not in secs]
        kw = themes(x[1], secs + also, 'holiday' in x[5])
        if len(x) > 12 and x[12]:  # year-round mat that also works for the holidays (row field 12)
            kw = (kw + ' holiday christmas').strip()
        if x[0] in photo_kw:
            kw = (kw + ' ' + photo_kw[x[0]]).strip()
        # also-colours are searchable (silent) but chips show the sections
        mats.append([x[0], x[1], x[2], x[3] or '', 1 if x[4] else 0, secs, x[6] or '', mat_albums.get(i, []),
                     1 if x[7] else 0, kw])
    xs = []
    for (n, b), e in sorted(extra.items()):
        hol = any(albums[a][5] == 2 for a in e['a'])
        xs.append([n, b, e['a'], e['shop'], e['ret'] if not e['shop'] else 0, e['img'], themes(n, (), hol),
                   re.sub(r'\?format=\d+w$', '?format=750w', e['img'])])
    xpos = {(x[0], x[1]): k for k, x in enumerate(xs)}
    for ai, a in enumerate(albums):
        a.append([v if isinstance(v, int) else -(xpos[(v[1], v[2])] + 1) for v in order.get(ai, [])])

    # ---- Pages: brands/codes, blog, main ----
    hubcodes = {}
    for l in text_lines(H.get('mahjong-discount-codes', '')):
        mm = re.match(r'^(.+?) [—-] (\d+)% off with ([A-Z0-9]{4,20})', l)
        if mm:
            hubcodes[norm(mm.group(1))] = (mm.group(3), mm.group(2))
    pages_out = []
    for s in pages:
        if s.endswith('tile-matches') or s == 'holiday-mahjong-matches':
            continue
        h = H.get(s, '')
        if len(h) < 2000 or (re.search(r'-\d$', s) and re.sub(r'-\d$', '', s) in H):
            continue
        title = clean_title(meta(h, 'og:title') or s)
        desc = meta(h, 'description') or meta(h, 'og:description')
        img = meta(h, 'og:image')
        if GENERIC_OG in img or not img:
            img = first_img(h)
        img = small_img(img.replace('http://', 'https://'))
        code, pct, kind, brand = '', '', 'page', ''
        if s.endswith('discount-code') or s.endswith('discount-code-2'):
            kind = 'brand'
            brand = re.split(r' Discount Code| Code\b', title)[0].strip()
            t = ' '.join(text_lines(h)[:80])
            mm = re.search(r'\b[Cc]ode\s*:?\s*([A-Z][A-Z0-9-]{4,24})\b', t)
            if mm:
                code = mm.group(1)
                pm = re.search(r'(\d{1,2})% off|[Ss]ave (\d{1,2})%', t)
                pct = (pm.group(1) or pm.group(2)) if pm else ''
            elif norm(brand) in hubcodes:
                code, pct = hubcodes[norm(brand)]
        elif s.startswith('blog/'):
            kind = 'blog'
        pages_out.append(['/' + s, title, kind, desc[:180], img, code, pct, brand])

    # ---- Thumbnails ----
    man_path = os.path.join(OUT, 'thumbs.json')
    try:
        man = json.load(open(man_path))
    except Exception:
        man = {}
    jobs = []
    for x in R:
        src = (mb.replace(re.search(r'@[0-9a-f]+/', mb).group(0), '@' + ib[x[0]] + '/') if x[0] in ib else mb) + x[0] + '.webp'
        jobs.append(('m/' + x[0] + '.webp', src, 200))
    for a in albums:
        if a[3] and 'jsdelivr' in a[3]:
            jobs.append(('a/' + a[0].strip('/').replace('#', '--') + '.webp', a[3], 240))
    for k, x in enumerate(xs):
        if x[5] and 'jsdelivr' in x[5]:
            rel = 'x/' + re.sub(r'[^a-z0-9]+', '-', norm(x[1] + ' ' + x[0])).strip('-') + '.webp'
            jobs.append((rel, x[5], 200))
    if do_thumbs:
        from PIL import Image

        def mk(job):
            rel, src, w = job
            dst = os.path.join(THUMBS, rel)
            if man.get(rel) == src and os.path.exists(dst):
                return rel, src, 'cached'
            b = curl(src, binary=True)
            try:
                im = Image.open(io.BytesIO(b)).convert('RGB')
            except Exception as e:
                print('  thumb error', rel, len(b), str(e)[:80], file=sys.stderr)
                return rel, src, 'FAIL'
            im.thumbnail((w, w * 2))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            im.save(dst, 'WEBP', quality=72, method=6)
            return rel, src, 'new'
        with ThreadPoolExecutor(8) as ex:
            res = list(ex.map(mk, jobs))
        fails = [r for r in res if r[2] == 'FAIL']
        for rel, src, st in res:
            if st != 'FAIL':
                man[rel] = src
        # drop thumbs that are no longer used
        used = {j[0] for j in jobs}
        for rel in list(man):
            if rel not in used:
                try:
                    os.remove(os.path.join(THUMBS, rel))
                except OSError:
                    pass
                man.pop(rel)
        json.dump(man, open(man_path, 'w'), separators=(',', ':'), sort_keys=True)
        print('thumbs: %d new, %d cached, %d failed' % (sum(r[2] == 'new' for r in res),
                                                         sum(r[2] == 'cached' for r in res), len(fails)))
        for f in fails:
            print('  thumb FAIL', f[1], file=sys.stderr)
    have = set(k for k in man if os.path.exists(os.path.join(THUMBS, k)))
    # point album covers / album-only card images at their local thumb when we have one
    for a in albums:
        rel = 'a/' + a[0].strip('/').replace('#', '--') + '.webp'
        if rel in have:
            a[3] = '@' + rel
    for x in xs:
        rel = 'x/' + re.sub(r'[^a-z0-9]+', '-', norm(x[1] + ' ' + x[0])).strip('-') + '.webp'
        if rel in have:
            x[5] = '@' + rel
        elif x[5]:
            x[5] = small_img(x[5])

    idx = {
        'v': 2,
        'built': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'mb': mb, 'ib': ib,
        'sec': sec_lab,
        # mats WITHOUT a local thumb (fall back to the gallery image); '@rel' = local thumb under thumbs/
        'nt': [x[0] for x in R if 'm/' + x[0] + '.webp' not in have],
        'm': mats, 'x': xs, 'a': albums, 'p': pages_out,
    }
    with open(os.path.join(OUT, 'search-index.json'), 'w') as f:
        json.dump(idx, f, ensure_ascii=False, separators=(',', ':'))
    stats = {
        'mats': len(mats), 'albums': sum(1 for a in albums if a[5] == 0), 'colour_hubs': sum(1 for a in albums if a[5] == 1),
        'holiday_entries': sum(1 for a in albums if a[5] == 2),
        'brand_pages': sum(1 for p in pages_out if p[2] == 'brand'), 'blog_posts': sum(1 for p in pages_out if p[2] == 'blog'),
        'main_pages': sum(1 for p in pages_out if p[2] == 'page'), 'gallery_mats_in_albums': len(mat_albums),
        'album_only_mats': len(xs), 'mats_with_theme_kw': sum(1 for m in mats if any(
            w in m[9].split() for w in ('halloween', 'valentine', 'patriotic', 'shamrock', 'easter', 'derby', 'christmas', 'hanukkah', 'winter', 'fall'))),
        'bytes': os.path.getsize(os.path.join(OUT, 'search-index.json')),
    }
    print('index:', json.dumps(stats))


if __name__ == '__main__':
    main()
