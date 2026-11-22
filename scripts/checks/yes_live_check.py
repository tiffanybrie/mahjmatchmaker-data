#!/usr/bin/env python3
"""YES-vs-LIVE CHECK (docs/OVERDUE.md, since Nov 9): every "yes" Tiffany has given vs the LIVE album pages.

A YES IS A YES (CLAUDE.md, Nov 4): a yes in a swipe book, picks page or review page goes into the album. This check
proves it did: it reads every recorded yes, reads every live album page, and lists each yes that has no live card.

Usage:
  python3 scripts/checks/yes_live_check.py            # fetch live pages, print, write the status json + audit md
  python3 scripts/checks/yes_live_check.py --cache D  # keep/read page html in D (re-runs without re-fetching)
  python3 scripts/checks/yes_live_check.py --no-write # print only
  python3 scripts/checks/yes_live_check.py --quiet    # one summary line (for front_door.py)
Exit code: 0 = every yes for a live album is live; 1 = at least one yes not live; 2 = could not read the site.

YES SOURCES (add a loader + a line in SOURCES for any new pick file):
  config/swipe-yeses/*.json                    swipe-book yes votes (mode tile: [set, mat]; mode mat: [mat, set])
  config/late-holiday-picks-nov03.json         "Brand | Mat": [tile sets]
  config/picks/*-final-order-*.json            album review final order ("in" list)
  config/picks/*-fym-m-*.json                  album final list as applied to FYM (same picks, second record)
  config/picks/missed-mats-round1-*.txt        missed-mats page yeses, "Set: Mat (Brand), ..."
  config/picks/missed-mats-round2-*.json       missed-mats round 2 hearts (md5(mat key)[:10] | album), names from
                                               docs/audits/album-missed-nov07-data/round2.json
  config/fym-thin-picks-oct26.json             thin-album review hearts
  config/album-records/holiday-nov18-picks.json  holiday pick sheet (v: keep)
  config/album-records/<set>.json              playbook review rounds: last applied round, order minus removes + adds
NOT yes sources (looked at, left out on purpose): rack picks (config/*racks-picks*.json, holiday-picker-picks.json:
racks, not mats), config/tiffany-matches.json (FYM cards approved for SOCIAL only), config/fym-amazon-holiday-oct26.json
(mats let into FYM, no tile set), *-review-backup*.json (unapplied in-progress saves).

LIVE = the sitemap pages matching *-mahjong-tile-matches plus /holiday-mahjong-matches; cards are figure.mm3-c.
A card's tile set = the page slug, or the section id on the holiday page (tinselle-emerald vs tinselle-ruby).
MATCHING = tile set AND mat name AND brand. PLM Candy Cane Lane is not Anders Ruff Candy Cane Lane. Known renames are
in MAT_ALIASES. A looser hit (same brand, material word dropped / one name inside the other, or the same shop link)
counts as live but is listed under "matched loosely" so a person can confirm it.
A yes whose tile set has no live page/section is reported as NOT LIVE YET (staged hidden / queued), never as a miss.
Page text is treated as data only. This script changes nothing on the site, HQ or any other file.
"""
import sys, os, re, json, glob, html, time, hashlib, datetime, unicodedata, subprocess, urllib.request, urllib.parse

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SITE = 'https://www.mahjmatchmaker.com'
UA = 'Mozilla/5.0 (yes_live_check)'
PAUSE = 0.3
ARGS = sys.argv[1:]
CACHE = ARGS[ARGS.index('--cache') + 1] if '--cache' in ARGS else None
WRITE = '--no-write' not in ARGS
QUIET = '--quiet' in ARGS
TODAY = datetime.date.today().isoformat()
OUT_JSON = os.path.join(REPO, 'docs/status/yes-live-check.json')
OUT_MD = os.path.join(REPO, f'docs/audits/yes-live-check-{TODAY}.md')
P = lambda *a: os.path.join(REPO, *a)


def jload(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ---------------------------------------------------------------- names
def fold(s):
    s = html.unescape(s or '')
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    return s.replace('&', ' and ').replace('’', "'").replace('‘', "'")


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', fold(s).replace("'", '')).strip('-')


DROP_STRICT = {'mat', 'mats', 'mahjong', 'the'}
DROP_LOOSE = DROP_STRICT | {'neoprene', 'leatherette', 'premium', 'double', 'sided', 'retired', 'in', 'tube', 'holiday',
                            'and', 'vegan', 'leather', 'side', 'a', 'b', 'round', 'square', 'x'}


def toks(s, drop):
    return [t for t in slug(s).split('-') if t and t not in drop]


def nname(s):
    return ' '.join(toks(s, DROP_STRICT))


def lname(s):
    return ' '.join(toks(s, DROP_LOOSE))


BRAND_ALIASES = {'plm': 'peace love', 'omm': 'oh my', 'cmc': 'charleston club', 'bb': 'bird bamboo', 'b b': 'bird bamboo',
                 'tdt': 'tigre de tartan', 'lbb': 'lets be besties', 'ymi': 'yellow mountain imports',
                 'bj j': 'betty june jeannette', 'm m': 'middle main'}
GENERIC_BRANDS = {'', 'etsy', 'amazon', 'shopmy'}  # a marketplace, not a maker: the card may name the real shop
BRAND_DROP = {'mahjong', 'the', 'and', 'co', 'company', 'studio', 'studios', 'design', 'designs', 'shop', 'boutique'}


def nbrand(s):
    b = ' '.join(t for t in slug(s).split('-') if t and t not in BRAND_DROP)
    return BRAND_ALIASES.get(b, b)


def brand_ok(yes_b, card_b):
    a, c = nbrand(yes_b), nbrand(card_b)
    if a in GENERIC_BRANDS:
        return True
    return a == c or (len(a) > 3 and len(c) > 3 and (a in c or c in a))


# (brand, mat name in the yes file) -> (brand, mat name as the live card calls it). Known renames only.
MAT_ALIASES = {
    ('peace love', nname('Sugarplum Plaid')): ('Peace Love Mahjong', 'Peace Love Holiday'),
    ('peace love', nname('Peace Love Holiday')): ('Peace Love Mahjong', 'Sugarplum Plaid'),
}

# ---------------------------------------------------------------- tile sets
SET_ALIASES = {  # yes-file token -> live set keys (album page slug or holiday section id)
    'sunday': ['sunday-tile-set', 'sunday'], 'sunday-tile-set': ['sunday-tile-set', 'sunday'],
    'sunday-mahjong-sunday': ['sunday-tile-set', 'sunday'],
    'tinselle-emerald-green': ['tinselle-emerald'], 'tinselle-ruby-red': ['tinselle-ruby'],
    'holly-jolly-sugarplum-pink': ['holly-jolly-pink'], 'holly-jolly-rudolph-red': ['holly-jolly-red'],
    'holly-jolly-grinch-green': ['holly-jolly-green'],
    'miss-classic-malachite': ['malachite'], 'miss-classic-jade': ['jade'], 'classic-tortoise': ['tortoise'],
    'plm-spirit': ['spirit-of-christmas'], 'bam-bird-boutique-deco': ['deco-lagoon'],
    'apres-ski-club': ['cmc-apres-ski'], 'shangri-la': ['shangri-la'],
}
SET_NAMES = {'spirit-of-christmas': 'Spirit of Christmas (Peace Love Mahjong)', 'plm-nutcracker': 'Nutcracker (Peace Love Mahjong)',
             'cmc-apres-ski': 'Après Ski Club', 'sunday-tile-set': 'Sunday Tile Set'}


def set_keys(token):
    t = slug(re.sub(r'\((retired|holiday)\)', '', token, flags=re.I))
    t = re.sub(r'^(hol|vault)-', '', t)
    t = re.sub(r'^sunday-mahjong-(?!sunday$)', '', t)
    return SET_ALIASES.get(t, [t])


# ---------------------------------------------------------------- live site
def fetch(url):
    name = url.rstrip('/').rsplit('/', 1)[-1] + '.html'
    if CACHE and os.path.exists(os.path.join(CACHE, name)):
        return open(os.path.join(CACHE, name), encoding='utf-8', errors='replace').read()
    body = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                if r.status == 200 and r.geturl().rstrip('/') == url.rstrip('/'):
                    body = r.read().decode('utf-8', 'replace')
            break
        except Exception:
            try:  # same request with curl (proxy / CA setups where urllib fails)
                out = subprocess.run(['curl', '-s', '-A', UA, '-w', '\n%{http_code}', url], capture_output=True, timeout=60)
                txt = out.stdout.decode('utf-8', 'replace')
                if txt.rstrip().endswith('200'):
                    body = txt.rsplit('\n', 1)[0]
                    break
            except Exception:
                pass
            time.sleep(1.5)
    time.sleep(PAUSE)
    if body and CACHE:
        os.makedirs(CACHE, exist_ok=True)
        open(os.path.join(CACHE, name), 'w', encoding='utf-8').write(body)
    return body


def live_pages():
    sm = fetch(SITE + '/sitemap.xml')
    if not sm:
        return None
    urls = [u for u in re.findall(r'<loc>([^<]+)</loc>', sm)
            if re.search(r'-mahjong-tile-matches$|/holiday-mahjong-matches$', u.rstrip('/'))]
    return sorted(set(urls))


TAG = re.compile(r'<[^>]+>')
WALK = re.compile(r'<(?:section|div|h2|h3|a|span)\b[^>]*\bid="([a-z0-9-]+)"|<figure class="mm3-c[ "].*?</figure>', re.S)


def parse_cards(url, page):
    """-> [card dict]; set key = page slug, or the nearest section id above the card on the holiday page."""
    pslug = url.rstrip('/').rsplit('/', 1)[-1]
    is_hol = pslug == 'holiday-mahjong-matches'
    base = re.sub(r'-mahjong-tile-matches$', '', pslug)
    cards, sec = [], ''
    for m in WALK.finditer(page):
        if m.group(1):
            sec = m.group(1)
            continue
        f = m.group(0)
        retired = 'class="mm3-ret"' in f
        f = re.sub(r'<span class="mm3-ret">.*?</span>', '', f, flags=re.S)
        h3 = re.search(r'<h3>(.*?)</h3>', f, re.S)
        by = re.search(r'class="mm3-by">(.*?)</span>', f, re.S)
        if not h3:
            continue
        title = html.unescape(TAG.sub('', h3.group(1))).strip()
        tile, _, mat = title.partition(' + ')
        brand = re.sub(r'^\s*Mat by\s*', '', html.unescape(TAG.sub('', by.group(1) if by else ''))).strip()
        img = (re.search(r'<img[^>]+src="([^"]+)"', f) or [None, ''])[1].rsplit('/', 1)[-1]
        btn = re.search(r'class="mm3-btn" href="([^"]+)"', f)
        href = urllib.parse.unquote(urllib.parse.unquote(html.unescape(btn.group(1)))) if btn else ''
        skey = sec if is_hol else base
        if is_hol and '-mahjong-tiles-' in img and sec in ('', 'holiday-matches', 'your-tiles', 'new-holiday-sets'):
            skey = img.split('-mahjong-tiles-')[0]
        cards.append({'set': skey, 'tile': tile.strip(), 'mat': mat.strip(), 'brand': brand, 'page': '/' + pslug,
                      'img': img, 'href': href.lower(), 'holiday_card': 'mm3-hc' in f[:40], 'retired': retired})
    return cards


# ---------------------------------------------------------------- yes loaders
YESES = []  # {set_token, mat, brand, key, src, detail}
NOTES = []
SHARED_HANDLES = set()  # one store listing that sells several different mats (PLM "mahjong-mats-holiday"): its link proves nothing


def add(set_token, mat, brand, src, key=None, detail=None, holiday=None, any_variant=False):
    YESES.append({'set_token': set_token, 'mat': (mat or '').strip(), 'brand': (brand or '').strip(), 'key': key or '',
                  'src': src, 'detail': detail or '', 'holiday': holiday, 'any_variant': any_variant})


def split_name_brand(s):
    """'Garden Glow – Emerald Green (Bespoke Mahjong)' -> (name, brand): the LAST parenthesis is the brand."""
    m = re.match(r'^(.*)\(([^()]*)\)\s*$', s.strip())
    return (m.group(1).strip(), m.group(2).strip()) if m else (s.strip(), '')


def snapshot():
    try:
        return jload(P('config/fym-mats-snapshot.json'))['mats']
    except Exception:
        return {}


def handle_of(key):
    return key.split('?')[0].rstrip('/').rsplit('/', 1)[-1].lower() if key else ''


SWIPE_HANDLE_FIX = {  # swipe-book ids that are not store handles (same table as builder/fym_fix_oct21/swipe_yeses.py)
    'omm-merry-mahjong': ('Merry Mahjong', 'Oh My Mahjong'), 'polo-club': ('The Polo Club', 'Luxe'),
    'festive-plaid': ('Festive Plaid', 'Sunday Mahjong'),
    'cmc-ski-club-red-sweater': ('Ski Club Red Sweater Border', 'Charleston Mahjong Club'),
    'holidayloveredgreen': ('Holiday Love Red & Green', ''),
}


def load_swipe_yeses():
    snap = snapshot()
    by_handle = {}
    for k, o in snap.items():
        by_handle.setdefault(handle_of(k), []).append((k, o))
    for f in sorted(glob.glob(P('config/swipe-yeses/*.json'))):
        rel = os.path.relpath(f, REPO)
        for bk, b in jload(f).get('books', {}).items():
            names = dict(b.get('items') or {})
            names.update(b.get('groups') or {})
            for g, it in b.get('yes', []):
                st, mid = (g, it) if b.get('mode') == 'tile' else (it, g)
                key = ''
                if mid in names:
                    n, bn = names[mid][0], names[mid][1] or ''
                elif mid in SWIPE_HANDLE_FIX and mid not in by_handle:
                    n, bn = SWIPE_HANDLE_FIX[mid]
                else:
                    c = by_handle.get(mid) or [x for h, v in by_handle.items() if h.startswith(mid) for x in v]
                    c.sort(key=lambda x: (bool(x[1].get('hid')), len(x[0])))
                    variants = sorted({x[1]['n'] for x in c if not x[1].get('hid') and handle_of(x[0]) == mid})
                    if len(variants) > 1:  # the book recorded the listing, not which mat on it
                        bn = c[0][1].get('bn') or ''
                        add(st, f'{bn} holiday mat, variant not recorded (listing {mid})', bn, rel, key='/' + mid, any_variant=True,
                            detail=f'swipe book "{bk}" yes [{g}, {it}]: one listing, {len(variants)} mats ({", ".join(variants)})')
                        msg = f'{rel} book {bk}: mat id "{mid}" is one store listing for {len(variants)} different mats; the yes cannot say which, so any live card from that listing counts (loose)'
                        if msg not in NOTES:
                            NOTES.append(msg)
                        continue
                    if c:
                        key, n, bn = c[0][0], c[0][1]['n'], c[0][1].get('bn') or ''
                    else:
                        n, bn = mid.replace('-', ' ').title(), ''
                        NOTES.append(f'{rel} book {bk}: mat id "{mid}" is not in config/fym-mats-snapshot.json; matched by its id words / shop link only')
                    if not key:
                        key = '/' + mid
                add(st, n, bn, rel, key=key, detail=f'swipe book "{bk}" yes [{g}, {it}]')


def load_late_holiday():
    f = P('config/late-holiday-picks-nov03.json')
    if not os.path.exists(f):
        return
    for mk, sets in jload(f).get('picks', {}).items():
        brand, _, mat = mk.partition(' | ')
        for s in sets:
            add(s, mat, brand, 'config/late-holiday-picks-nov03.json', detail=f'"{mk}": {s}', holiday=True)


def load_final_orders():
    for f in sorted(glob.glob(P('config/picks/*-final-order-*.json'))):
        rel = os.path.relpath(f, REPO)
        st = os.path.basename(f).split('-final-order-')[0]
        for s in jload(f).get('in', []):
            n, b = split_name_brand(s)
            add(st, n, b, rel, detail='final album order ("in")')
    for f in sorted(glob.glob(P('config/picks/*-fym-m-*.json'))):
        rel = os.path.relpath(f, REPO)
        d = jload(f)
        st = os.path.basename(f).split('-fym-m-')[0]
        for e in d.get('m', []):
            n, b = split_name_brand(e.get('pick', ''))
            add(st, n, b, rel, key=e.get('key'), detail=f"final list #{e.get('order')}", holiday=e.get('holiday'))


def load_missed_round1():
    for f in sorted(glob.glob(P('config/picks/missed-mats-round1-*.txt'))):
        rel = os.path.relpath(f, REPO)
        for line in open(f, encoding='utf-8').read().splitlines()[1:]:
            if ':' not in line:
                continue
            st, _, rest = line.partition(':')
            hol = '(holiday)' in st.lower()
            for item in re.split(r'(?<=\))\s*,\s*', rest.strip()):
                if item.strip():
                    n, b = split_name_brand(item)
                    add(st, n, b, rel, detail=line.partition(':')[0].strip(), holiday=hol)


def load_missed_round2():
    mp = P('docs/audits/album-missed-nov07-data/round2.json')
    mats = {}
    if os.path.exists(mp):
        for m in jload(mp).get('mats', []):
            mats[hashlib.md5(m['key'].encode()).hexdigest()[:10]] = m
    for f in sorted(glob.glob(P('config/picks/missed-mats-round2-*.json'))):
        rel = os.path.relpath(f, REPO)
        for h in jload(f).get('hearts', []):
            mid, _, alb = h.partition('|')
            m = mats.get(mid)
            if not m:
                NOTES.append(f'{rel}: heart "{h}" has no mat in docs/audits/album-missed-nov07-data/round2.json (cannot name it)')
                continue
            add(alb, m['name'], m['brand'], rel, key=m['key'], detail=f'round 2 heart {h}', holiday=m.get('holiday'))


def load_thin_picks():
    f = P('config/fym-thin-picks-oct26.json')
    if os.path.exists(f):
        for p in jload(f).get('picks', []):
            add(p['set'], p['name'], p['brand'], 'config/fym-thin-picks-oct26.json', key=p.get('key'), detail='thin-album review heart')


def load_holiday_nov18():
    f = P('config/album-records/holiday-nov18-picks.json')
    if not os.path.exists(f):
        return
    d = jload(f)
    snap = snapshot()
    new = {}
    bp = P('scripts/albumreview/holiday_nov18/build_picks.py')
    if os.path.exists(bp):
        for k, n, b in re.findall(r"'([a-z]+:[a-z0-9-]+)':\s*\('([^']+)',\s*'([^']+)',", open(bp, encoding='utf-8').read()):
            new[k] = (n, b)
    for st, votes in d.get('v', {}).items():
        for k, v in votes.items():
            if v != 'keep':
                continue
            if k in snap:
                n, b = snap[k]['n'], snap[k].get('bn') or ''
            elif k in new:
                n, b = new[k]
            else:
                n, b = handle_of(k).replace('-', ' ').title(), ''
                NOTES.append(f'config/album-records/holiday-nov18-picks.json: key "{k}" has no name in the FYM snapshot; matched by shop link / id words')
            add(st, n, b, 'config/album-records/holiday-nov18-picks.json', key=k if '/' in k else '',
                detail=f"holiday pick sheet keep (answered {d.get('at', '')[:10]}, done={d.get('done')})", holiday=True)


def load_album_records():
    for f in sorted(glob.glob(P('config/album-records/*.json'))):
        rel = os.path.relpath(f, REPO)
        if 'backup' in f or f.endswith('holiday-nov18-picks.json'):
            continue
        d = jload(f)
        rounds = [r for r in (d.get('rounds') or []) if isinstance(r, dict) and r.get('applied_at') and (r.get('answers') or {}).get('order')]
        if not rounds:
            continue
        r = rounds[-1]
        a = r['answers']
        spec = {}
        try:
            for m in jload(P(d['spec'])).get('mats', []):
                for nm in filter(None, (m['name'], m.get('short'))):
                    full = m['brand'] + ' ' + nm
                    for cid in (slug(full), re.sub(r'[^a-z0-9]+', '-', full.lower().replace('&', 'and').replace("'", '').replace('’', '')).strip('-')):
                        spec[cid] = (m['name'], m['brand'], m.get('fym') or '')  # 2nd form: accents become '-' (card ids were built that way)
        except Exception:
            pass
        removed = {k for k, v in (a.get('v') or {}).items() if v == 'remove'}
        st = d.get('set') or os.path.basename(f)[:-5]
        det = f"review round {r.get('round')} applied {str(r.get('applied_at'))[:10]} (done={a.get('done')})"
        for grp in ('main', 'hol'):
            for cid in a['order'].get(grp, []):
                if cid in removed:
                    continue
                n, b, k = spec.get(cid) or spec.get(re.sub(r'^lo-', '', cid)) or (cid.replace('-', ' ').title(), '', '')
                add(st, n, b, rel, key=k, detail=det + f', card id {cid}', holiday=(grp == 'hol'))
        for x in a.get('adds') or []:
            add(st, re.sub(r'\s*\(retired\)\s*$', '', x.get('n', '')), x.get('b', ''), rel,
                key=x.get('k') if '/' in (x.get('k') or '') else '', detail=det + ', her add')


SOURCES = [load_swipe_yeses, load_late_holiday, load_final_orders, load_missed_round1, load_missed_round2,
           load_thin_picks, load_holiday_nov18, load_album_records]


# ---------------------------------------------------------------- not-live-yet context
def staged_info():
    info = {}
    try:
        for k, v in jload(P('config/album-launch-slots.json')).get('slots', {}).items():
            info.setdefault(k, f'go-live slot {v} (config/album-launch-slots.json)')
            if k == 'cmc-cabana-apres-ski':
                info['cabana-club'] = f'go-live slot {v} (config/album-launch-slots.json {k})'
    except Exception:
        pass
    try:
        for a in jload(P('config/album-queue.json')).get('albums', []):
            wk = a.get('week')
            info.setdefault(a['slug'], f"album queue, week of {wk}{' (proposed)' if a.get('proposed') else ''}" if wk else 'album queue, no week yet')
    except Exception:
        pass
    for f in glob.glob(P('config/album-records/*.json')):
        s = os.path.basename(f)[:-5]
        if 'backup' not in s:
            info.setdefault(s, 'album record exists, no go-live slot yet (config/album-records)')
            try:
                d = jload(f)
                if d.get('name'):
                    SET_NAMES.setdefault(s, d['name'] + (f" ({d['brand']})" if d.get('brand') else ''))
            except Exception:
                pass
    try:
        for it in jload(P('config/release-calendar.json')).get('upcomingAlbums', {}).get('items', []):
            info.setdefault(slug(it.get('set', '')), 'upcoming album (config/release-calendar.json upcomingAlbums)')
    except Exception:
        pass
    return info


# ---------------------------------------------------------------- match
def match(y, cards_by_set):
    """-> (status, card or None, how). status: live | loose | not_live_yet | not_live"""
    keys = [k for k in set_keys(y['set_token']) if k in cards_by_set]
    if not keys:
        return 'not_live_yet', None, ''
    cards = [c for k in keys for c in cards_by_set[k]]
    yn, yl = nname(y['mat']), lname(y['mat'])
    alias = MAT_ALIASES.get((nbrand(y['brand']), yn))
    wanted = [(y['mat'], y['brand'])] + ([(alias[1], alias[0])] if alias else [])
    for n, b in wanted:
        for c in cards:
            if nname(c['mat']) == nname(n) and brand_ok(b, c['brand']):
                return 'live', c, 'name + brand' if (n, b) == wanted[0] else f'known rename: live card is "{c["mat"]}"'
    h = handle_of(y['key'])
    if len(h) >= 8 and (h not in SHARED_HANDLES or y.get('any_variant')):
        for c in cards:
            if re.search(r'(?<![a-z0-9-])' + re.escape(h) + r'(?![a-z0-9-])', c['href']):
                if brand_ok(y['brand'], c['brand']) or not y['brand']:
                    return 'loose', c, f'same shop link ({h}); live card is "{c["mat"]}" by {c["brand"]}'
    if y.get('any_variant'):
        return 'not_live', None, 'no live card from that listing for this tile set'
    yt = yl.split()
    for c in cards:
        if not brand_ok(y['brand'], c['brand']) or nbrand(y['brand']) in GENERIC_BRANDS:
            continue
        cl = lname(c['mat'])
        ct = cl.split()
        if not yt or not ct:
            continue
        short, long_ = (ct, yt) if len(ct) <= len(yt) else (yt, ct)
        if yl == cl or (len(short) >= 2 and set(short) <= set(long_)) or long_[:len(short)] == short:
            why = 'same brand, close name' if len(short) >= 2 or yl == cl else 'same brand, the live card has the short name (colour / side / variant not on the card)'
            return 'loose', c, f'{why}; live card is "{c["mat"]}"'
    other = [c for c in cards if nname(c['mat']) == yn or (yl and lname(c['mat']) == yl)]
    if other:
        return 'not_live', other[0], f'same mat name on the page from another brand: {other[0]["brand"]} "{other[0]["mat"]}"'
    return 'not_live', None, ''


def main():
    urls = live_pages()
    if not urls:
        print('YES-vs-LIVE CHECK: could not read the sitemap; nothing checked.')
        return 2
    cards, pages, failed = [], [], []
    for u in urls:
        body = fetch(u)
        if body is None:
            failed.append(u)
            continue
        pc = parse_cards(u, body)
        pages.append({'url': u, 'cards': len(pc)})
        cards += pc
    if failed and len(failed) > len(urls) // 4:
        print(f'YES-vs-LIVE CHECK: {len(failed)} of {len(urls)} album pages did not load; not trusted, nothing written.')
        return 2
    cards_by_set, by_link = {}, {}
    for c in cards:
        cards_by_set.setdefault(c['set'], []).append(c)
        m = re.search(r'/(?:products|listing/\d+|dp)/([a-z0-9-]+)', c['href'])
        if m:
            by_link.setdefault(m.group(1), set()).add((nname(c['mat']), nbrand(c['brand'])))
    SHARED_HANDLES.update(h for h, names in by_link.items() if len(names) > 1)
    by_h = {}
    for k, o in snapshot().items():
        if not o.get('hid'):
            by_h.setdefault(handle_of(k), set()).add(nname(o['n']))
    SHARED_HANDLES.update(h for h, names in by_h.items() if len(names) > 1)
    set_title = {}
    for c in cards:
        set_title.setdefault(c['set'], c['tile'])

    for fn in SOURCES:
        try:
            fn()
        except Exception as e:  # a broken source file must not hide the others
            NOTES.append(f'{fn.__name__} failed: {type(e).__name__}: {e}')

    # one row per (tile set, mat, brand); every source that recorded it is kept
    rows = {}
    for y in YESES:
        sk = '+'.join(set_keys(y['set_token']))
        k = (sk, lname(y['mat']) or nname(y['mat']), nbrand(y['brand']))
        r = rows.setdefault(k, dict(y, set=([x for x in set_keys(y['set_token']) if x in cards_by_set] or set_keys(y['set_token']))[0], sources=[], details=[]))
        if y['src'] not in r['sources']:
            r['sources'].append(y['src'])
            r['details'].append(y['detail'])
        if y['key'] and not r['key']:
            r['key'] = y['key']
        if y['brand'] and not r['brand']:
            r['brand'] = y['brand']
    staged = staged_info()
    SET_NAMES.setdefault('cypress-forest', 'Cypress Forest')
    SET_NAMES.setdefault('plum-panda', 'Plum Panda (Sunday Mahjong)')
    res = {'live': [], 'loose': [], 'not_live': [], 'not_live_yet': []}
    for r in rows.values():
        st, card, how = match(r, cards_by_set)
        item = {'set': r['set'], 'set_name': set_title.get(r['set']) or SET_NAMES.get(r['set']) or r['set_token'].strip(),
                'mat': r['mat'], 'brand': r['brand'], 'holiday': bool(r.get('holiday')), 'sources': r['sources'],
                'details': r['details'], 'how': how}
        if card:
            item['live_card'] = {'page': card['page'], 'mat': card['mat'], 'brand': card['brand']}
        if st == 'not_live_yet':
            item['why'] = staged.get(r['set']) or 'no live album page or holiday section for this tile set'
        res[st].append(item)
    for v in res.values():
        v.sort(key=lambda i: (i['set'], i['brand'], i['mat']))

    n_all = len(rows)
    n_scope = n_all - len(res['not_live_yet'])
    miss = res['not_live']
    by_album = {}
    for i in miss:
        by_album.setdefault(i['set'], []).append(i)
    by_src = {}
    for i in miss:
        for s in i['sources']:
            by_src[s] = by_src.get(s, 0) + 1
    nly_sets = {}
    for i in res['not_live_yet']:
        nly_sets.setdefault(i['set'], []).append(i)
    src_counts = {}
    for y in YESES:
        src_counts[y['src']] = src_counts.get(y['src'], 0) + 1

    summary = (f"YES-vs-LIVE CHECK: {len(miss)} yes(es) NOT LIVE of {n_scope} checked against live albums "
               f"({len(res['live'])} live, {len(res['loose'])} live by a loose match); "
               f"{len(res['not_live_yet'])} more are for {len(nly_sets)} album(s) not live yet. "
               f"{len(YESES)} yes records read, {n_all} unique tile set + mat pairs, {len(pages)} live pages, {len(cards)} cards.")
    if QUIET:
        print(summary)
    else:
        print(summary)
        if failed:
            print('  PAGES THAT DID NOT LOAD (their yeses may show as not live):', ', '.join(failed))
        for alb in sorted(by_album, key=lambda a: -len(by_album[a])):
            its = by_album[alb]
            print(f"\n  {its[0]['set_name']} ({alb}): {len(its)} not live")
            for i in its:
                print(f"    - {i['mat']} ({i['brand'] or 'brand not recorded'}){' [holiday]' if i['holiday'] else ''}  <- {'; '.join(i['sources'])}"
                      + (f"  ! {i['how']}" if i['how'] else ''))
        if res['not_live_yet']:
            print('\n  NOT LIVE YET (not misses):')
            for alb in sorted(nly_sets, key=lambda a: -len(nly_sets[a])):
                print(f"    {nly_sets[alb][0]['set_name']} ({alb}): {len(nly_sets[alb])} yeses - {nly_sets[alb][0]['why']}")
        if res['loose']:
            print(f"\n  MATCHED LOOSELY, counted live ({len(res['loose'])}): see {os.path.relpath(OUT_MD, REPO)}")
        for n in NOTES:
            print('  note:', n)

    if WRITE:
        out = {'at': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'summary': summary,
               'pass': not miss, 'counts': {'yes_records': len(YESES), 'unique_pairs': n_all, 'checked_against_live': n_scope,
                                            'live': len(res['live']), 'live_loose': len(res['loose']),
                                            'not_live': len(miss), 'not_live_yet': len(res['not_live_yet'])},
               'records_by_source': src_counts, 'not_live_by_source': by_src,
               'not_live_by_album': {a: len(v) for a, v in sorted(by_album.items(), key=lambda kv: -len(kv[1]))},
               'pages': pages, 'pages_failed': failed, 'notes': NOTES,
               'not_live': miss, 'not_live_yet': res['not_live_yet'], 'live_loose': res['loose']}
        os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
        json.dump(out, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        L = [f'# Yes vs live check, {TODAY}', '',
             'Every yes Tiffany has given (swipe books, picks pages, late picks, review rounds) compared with the cards on the live album pages. '
             'Built by `python3 scripts/checks/yes_live_check.py`; data in `docs/status/yes-live-check.json`.', '',
             f'- Yes records read: **{len(YESES)}** ({n_all} unique tile set + mat pairs; the same yes is often recorded in two files)',
             f'- Checked against live albums: **{n_scope}**',
             f'- Live: **{len(res["live"]) + len(res["loose"])}** ({len(res["loose"])} of them by a loose match, listed at the bottom)',
             f'- **Not live: {len(miss)}**',
             f'- For albums that are not live yet (not misses): {len(res["not_live_yet"])}',
             f'- Live pages read: {len(pages)} ({len(cards)} cards)' + (f'; {len(failed)} did not load' if failed else ''), '',
             'Matching is by tile set, mat name and brand together.', '',
             '## Yes records by source', '', '| Source file | Yes records | Not live |', '|---|---|---|']
        for s in sorted(src_counts):
            L.append(f'| `{s}` | {src_counts[s]} | {by_src.get(s, 0)} |')
        L += ['', '## Yes, not live (per album)', '']
        if not miss:
            L.append('None. Every yes for a live album has a live card.')
        for alb in sorted(by_album, key=lambda a: (-len(by_album[a]), a)):
            its = by_album[alb]
            L += [f"### {its[0]['set_name']} (`{alb}`): {len(its)}", '', '| Mat | Brand | Holiday | Source | Note |', '|---|---|---|---|---|']
            for i in its:
                src = '<br>'.join(f'`{s}` ({d})' for s, d in zip(i['sources'], i['details']))
                L.append(f"| {i['mat']} | {i['brand'] or 'not recorded'} | {'yes' if i['holiday'] else ''} | {src} | {i['how']} |".replace('\n', ' '))
            L.append('')
        L += ['## Not live yet (staged hidden or queued, not misses)', '']
        if not nly_sets:
            L.append('None.')
        for alb in sorted(nly_sets, key=lambda a: (-len(nly_sets[a]), a)):
            its = nly_sets[alb]
            L += [f"### {its[0]['set_name']} (`{alb}`): {len(its)} yeses", '', f"Status: {its[0]['why']}. Sources: {', '.join(sorted({'`' + s + '`' for i in its for s in i['sources']}))}", '',
                  ', '.join(f"{i['mat']} ({i['brand']})" if i['brand'] else i['mat'] for i in its), '']
        L += ['## Matched loosely (counted live, worth a look)', '']
        if res['loose']:
            L += ['| Album | Yes | Live card | Why it counted | Source |', '|---|---|---|---|---|']
            for i in res['loose']:
                c = i['live_card']
                L.append(f"| {i['set_name']} (`{i['set']}`) | {i['mat']} ({i['brand']}) | {c['mat']} ({c['brand']}) on {c['page']} | {i['how']} | {'; '.join('`' + s + '`' for s in i['sources'])} |")
        else:
            L.append('None.')
        if NOTES or failed:
            L += ['', '## Notes', ''] + [f'- {n}' for n in NOTES] + [f'- Page did not load: {u}' for u in failed]
        L.append('')
        os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
        open(OUT_MD, 'w', encoding='utf-8').write('\n'.join(L))
    return 1 if miss else 0


if __name__ == '__main__':
    sys.exit(main())
