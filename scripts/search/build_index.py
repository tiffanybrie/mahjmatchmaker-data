#!/usr/bin/env python3
"""Build assets/search/search-index.json for the site-wide search (curl-based).

Reads the LIVE site only (curl -s): sitemap.xml, the album hub, the live Mat Gallery
(/mahjong-mats code block JSON), every album page, brand/code pages, blog posts and
main pages. Writes a compact index plus small webp thumbnails (assets/search/thumbs/),
regenerating a thumb only when its source URL changed (assets/search/thumbs.json).

Usage:  python3 scripts/search/build_index.py            (from the repo root)
        python3 scripts/search/build_index.py --no-thumbs
Then commit, push, and re-pin site/livepatch/search/header-injection.html to the new commit.
"""
import html, io, json, os, re, subprocess, sys, tempfile, time, unicodedata
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
COLOR_HUBS = {'pink', 'blue', 'green', 'yellow-orange', 'purple', 'neutral', 'masculine', 'coquette', 'red',
              'brown', 'ivory'}


def curl(url, binary=False):
    for i in range(3):
        r = subprocess.run(['curl', '-s', '-L', '--max-time', '40', url], capture_output=True)
        if r.returncode == 0 and r.stdout:
            return r.stdout if binary else r.stdout.decode('utf-8', 'replace')
        time.sleep(1 + i)
    return b'' if binary else ''


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
    t = re.sub(r'\s*[—–-]\s*Mahj Matchmaker\s*$', '', t)
    return t.strip()


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


STOP = {'the', 'a', 'and', 'of', 'mat', 'mats', 'x'}


def toks(s):
    s = norm(s).replace('yotd', 'year of the dragon')
    t = [w for w in s.split() if w not in STOP]
    if t and t[-1].isdigit():
        t = t[:-1]
    return set(t)


def fuzzy_mat(R, name, brand):
    """Album caption -> gallery row: same brand, every caption word in the gallery name; unique hit only."""
    a, b = toks(name), norm(brand)
    if not a:
        return None
    hits = [i for i, x in enumerate(R) if norm(x[2]) == b and a <= toks(x[1])]
    return hits[0] if len(hits) == 1 else None


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
    sec_lab = {k: html.unescape(v) for k, v in sec_lab.items()}

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
    albums = []
    album_mats = {}  # album index -> [(name, brand)]
    for s in [u for u in slugs if u.endswith('tile-matches')] + ['holiday-mahjong-matches']:
        h = H.get(s, '')
        if not h:
            continue
        hubish = s == 'mahjong-tile-matches' or s.replace('-mahjong-tile-matches', '') in COLOR_HUBS
        title = clean_title(meta(h, 'og:title') or s)
        cov, brand, setname = covers.get(s, ('', '', ''))
        if not setname:
            setname = re.split(r' Mahjong| Tile Matches| Matches', title)[0].strip()
        if not brand:
            mm = re.search(r'\|\s*([^|]+?)\s*$', title)
            brand = mm.group(1) if mm and 'Pairing' not in mm.group(1) else ''
        if not cov:
            cov = first_img(h)
        L = text_lines(h)
        mats = []
        pre = re.escape(setname) if setname else r'[^+]+'
        for i, l in enumerate(L[:-3]):
            mm = re.match(r'^(.{2,60}?) \+ (.{2,80})$', l)
            if mm and L[i + 1] == 'Mat by':
                mats.append((mm.group(2).strip(), L[i + 2].strip()))
        seen = set()
        mats = [x for x in mats if not (x in seen or seen.add(x))]
        idx = len(albums)
        album_mats[idx] = mats
        hb = 1 if hubish else (2 if s == 'holiday-mahjong-matches' else 0)
        if s == 'mahjong-tile-matches':
            setname, brand = 'All tile match albums', ''
        elif hubish:
            setname, brand = re.sub(r' Mahjong.*$', '', title) + ' tile matches', ''
        elif s == 'holiday-mahjong-matches':
            setname = 'Holiday tile matches'
        albums.append([s, setname, brand, small_img(cov),
                       colors.get(s, []), hb, len(mats), meta(h, 'description')[:160]])

    # ---- Mats ----
    key = {}
    for i, x in enumerate(R):
        key.setdefault((norm(x[1]), norm(x[2])), i)
        key.setdefault((norm(x[1]), ''), i)
    mat_albums = {}
    extra = {}  # album mats not in the gallery: (name, brand) -> [album idxs]
    unmatched = 0
    for ai, ms in album_mats.items():
        for name, brand in ms:
            i = key.get((norm(name), norm(brand)), key.get((norm(name), '')))
            if i is None:
                i = fuzzy_mat(R, name, brand)
            if i is None:
                unmatched += 1
                e = extra.setdefault((name, brand), [])
                if ai not in e:
                    e.append(ai)
                if '--debug' in sys.argv:
                    print('  unmatched:', albums[ai][0], '|', name, '|', brand, file=sys.stderr)
                continue
            mat_albums.setdefault(i, [])
            if ai not in mat_albums[i]:
                mat_albums[i].append(ai)
    mats = []
    for i, x in enumerate(R):
        secs = [c for c in x[5] if c in sec_lab]
        mats.append([x[0], x[1], x[2], x[3] or '', 1 if x[4] else 0, secs, x[6] or '', mat_albums.get(i, []),
                     1 if x[7] else 0])

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
            mm = re.search(r'\b[Cc]ode\s*:?\s*([A-Z][A-Z0-9]{4,19})\b', t)
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
            jobs.append(('a/' + a[0] + '.webp', a[3], 240))
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
            except Exception:
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
        json.dump(man, open(man_path, 'w'), separators=(',', ':'), sort_keys=True)
        print('thumbs: %d new, %d cached, %d failed' % (sum(r[2] == 'new' for r in res),
                                                         sum(r[2] == 'cached' for r in res), len(fails)))
        for f in fails:
            print('  thumb FAIL', f[1], file=sys.stderr)
    have = set(k for k in man if os.path.exists(os.path.join(THUMBS, k)))

    idx = {
        'v': 1,
        'built': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'mb': mb, 'ib': ib,
        'sec': sec_lab,
        'th': {'m': sum(1 for x in R if 'm/' + x[0] + '.webp' in have),
               'a': [a[0] for a in albums if 'a/' + a[0] + '.webp' in have]},
        # mats: [img, name, brand, shop url, retired, colour sections, brand guide page, album idxs, one-to-watch]
        'm': mats,
        # album-only mats (in an album caption, not in the gallery): [name, brand, album idxs]
        'x': [[n, b, a] for (n, b), a in sorted(extra.items())],
        # albums: [slug, set name, brand, cover, hub colour sections, kind 0 album/1 colour hub/2 holiday, n mats, desc]
        'a': albums,
        # pages: [path, title, kind brand|blog|page, desc, img, code, pct, brand]
        'p': pages_out,
    }
    with open(os.path.join(OUT, 'search-index.json'), 'w') as f:
        json.dump(idx, f, ensure_ascii=False, separators=(',', ':'))
    n_al = sum(1 for a in albums if a[5] == 0)
    print('index: %d mats, %d albums (+%d colour hubs, %d holiday), %d brand pages, %d blog posts, %d main pages; '
          'album mats linked to gallery: %d mats, %d album captions unmatched; %d bytes' % (
              len(mats), n_al, sum(1 for a in albums if a[5] == 1), sum(1 for a in albums if a[5] == 2),
              sum(1 for p in pages_out if p[2] == 'brand'), sum(1 for p in pages_out if p[2] == 'blog'),
              sum(1 for p in pages_out if p[2] == 'page'), len(mat_albums), unmatched,
              os.path.getsize(os.path.join(OUT, 'search-index.json'))))


if __name__ == '__main__':
    main()
