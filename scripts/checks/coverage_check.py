#!/usr/bin/env python3
"""COVERAGE CHECK: one "X of N" line per feature, so nothing is declared done on a sample again.
Tiffany Nov 7 2026 ("It makes me worry about where we have other gaps"): table-view walls were "done" at 30 of 336, ShopMy
mats and approved Amazon picks were "in" while half were missing, and nothing counted coverage.
Spec: docs/audits/gap-audit-2026-11-07.md ("Suggested single guard").

Reads what is LIVE, never a config file standing in for it:
  - the website FYM build pinned in the live /find-your-match page block (site-app/fym-vNNN/index.html @sha, read with
    `git show` from this repo; jsDelivr only if the commit is missing locally),
  - the Mat Gallery data pinned in the live /mahjong-mats page, and the search index pinned by search.js there,
  - sitemap.xml, the codes hub, every *-discount-code page, every album page, the holiday page (live curls),
  - config/code-truth.json, the latest config/shopmy-crosscheck-*.json, docs/OVERDUE.md, docs/DESK.md,
    docs/status/tasks-off.json.
Network results are cached in docs/status/coverage.json (`net`), refreshed when older than 6 hours or with --refresh.
A cached run takes a few seconds; --refresh ~15-30s (parallel curls).

Each line: OK / GAP / UNKNOWN, have of total, the target, and a few examples of what is missing.
front_door.py prints the GAP lines (top 8) at the top of every chat from docs/status/coverage.json (no network there).
Morning HQ cleanup runs `python3 scripts/checks/coverage_check.py --refresh`; GAP lines go to HQ Today (docs/HQ-CLEANUP.md).

Usage: python3 scripts/checks/coverage_check.py [--refresh] [--json]   (exit 1 when any GAP)
docs/status/tasks-off.json (written by any attended chat that can run list_triggers):
  {"at": "<ISO>", "off": [{"name": "...", "reason": "device_absent", "since": "YYYY-MM-DD"}]}"""
import os, re, sys, json, html, time, datetime, subprocess, unicodedata, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(R)
OUT = 'docs/status/coverage.json'
SITE = 'https://www.mahjmatchmaker.com'
CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
FYM_WORKTREE = '/home/claude/fym-site'
MAX_NET_AGE_H = 6
REFRESH = '--refresh' in sys.argv
T0 = time.time()
NOW = datetime.datetime.now()
TODAY = NOW.date()

# ---------------------------------------------------------------- helpers
def nz(x):
    x = ''.join(c for c in unicodedata.normalize('NFD', html.unescape(str(x or ''))) if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]', '', x.replace('&', 'and').replace('+', 'and'))

def nu(u):
    u = str(u or '')
    if '/discount/' in u and 'redirect=' in u:
        u = re.sub(r'^(https?://[^/]+).*$', r'\1', u) + urllib.parse.unquote(u.split('redirect=', 1)[1].split('&')[0])
    return re.sub(r'^https?://(www\.)?', '', u.split('?')[0].split('#')[0]).rstrip('/').replace('/products/', '/')

def get(u, timeout=25):
    """(status, final_url, text). Follows redirects."""
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 mm-coverage'}), timeout=timeout)
        return r.status, r.geturl(), r.read().decode('utf8', 'ignore')
    except urllib.error.HTTPError as e:
        return e.code, u, ''
    except Exception as e:
        return 0, u, ''

def visible(h):
    h = re.sub(r'<!--.*?-->', ' ', h, flags=re.S)
    h = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I)
    alts = ' '.join(re.findall(r'\balt="([^"]*)"', h))
    return html.unescape(re.sub(r'<[^>]+>', ' ', h) + ' ' + alts)

def git_show(sha, path):
    for attempt in (0, 1):
        try:
            return subprocess.run(['git', 'show', f'{sha}:{path}'], capture_output=True, check=True, timeout=30).stdout.decode('utf8')
        except Exception:
            if attempt == 0:
                subprocess.run(['git', 'fetch', '-q', 'origin'], capture_output=True, timeout=60)
    st, _, t = get(CDN + sha + '/' + path, 60)
    return t if st == 200 else None

MON = {m: i + 1 for i, m in enumerate(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])}
def verified_dates(t):
    out = []
    for m in re.finditer(r'verified[^0-9A-Za-z]{0,40}?(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.? (\d{1,2}),? (20\d\d)', t, flags=re.I):
        try: out.append(datetime.date(int(m.group(3)), MON[m.group(1)[:3].lower()], int(m.group(2))))
        except ValueError: pass
    return out

# ---------------------------------------------------------------- network part (cached)
def refresh_net():
    net = {'at': NOW.isoformat(timespec='seconds'), 'errors': []}
    with ThreadPoolExecutor(4) as ex:
        f_fym, f_gal, f_sm, f_hub, f_hol = [ex.submit(get, SITE + p) for p in
            ('/find-your-match', '/mahjong-mats', '/sitemap.xml', '/mahjong-discount-codes', '/holiday-mahjong-matches')]
        (s1, _, fym), (s2, _, gal), (s3, _, sm), (s4, _, hub), (s5, _, hol) = [f.result() for f in (f_fym, f_gal, f_sm, f_hub, f_hol)]
    m = re.search(r'mahjmatchmaker-data@([0-9a-f]{7,40})/(site-app/fym-v\d+)/index\.html', fym)
    net['fym_pin'] = {'sha': m.group(1), 'path': m.group(2) + '/index.html'} if m else None
    if not m: net['errors'].append(f'/find-your-match ({s1}): no fym-vNNN pin found')
    m = re.search(r'mahjmatchmaker-data@([0-9a-f]{7,40})/(site/livepatch/matgallery/data/matgallery-v\d+\.json)', gal)
    net['gallery_pin'] = {'sha': m.group(1), 'path': m.group(2)} if m else None
    if not m: net['errors'].append(f'/mahjong-mats ({s2}): no matgallery pin found')
    net['gallery_data_fym'] = (re.search(r'data-fym="(v\d+)"', gal) or [None, None])[1]
    m = re.search(r'mahjmatchmaker-data@([0-9a-f]{7,40})/assets/search/search\.js', gal + fym)
    net['search_pin'] = {'sha': m.group(1), 'path': 'assets/search/search-index.json'} if m else None
    urls = [u.replace(SITE, '') or '/' for u in re.findall(r'<loc>([^<]+)</loc>', sm)]
    net['sitemap'] = urls
    if not urls: net['errors'].append(f'sitemap ({s3}) empty')
    # codes hub: every <li><a href><strong>Brand</strong></a>
    hb = []
    for href, name in re.findall(r'<li[^>]*>\s*<a href="([^"]+)"[^>]*>\s*<strong>(.*?)</strong>', hub, flags=re.S):
        hb.append([html.unescape(re.sub(r'<[^>]+>', '', name)).strip(), href])
    net['hub_brands'] = hb
    if not hb: net['errors'].append(f'codes hub ({s4}): no brands parsed')
    # holiday page: section ids and which are hidden
    net['holiday_ids'] = {i: bool(re.search(r'display:\s*none', st or '')) for i, st in
                          re.findall(r'<section[^>]*\bid="([^"]+)"(?:[^>]*\bstyle="([^"]*)")?', hol)}
    # brand pages + album pages + removed pages
    truth = json.load(open('config/code-truth.json'))
    removed = [p for o in truth.get('removed_brands', {}).values() for p in o.get('removed_pages', [])]
    brand_pages = sorted({u for u in urls if u.endswith('-discount-code') or re.search(r'-discount-code-\d+$', u)} |
                         {h for _, h in hb if h.startswith('/')} | set(removed))
    album_pages = sorted(u for u in urls if re.fullmatch(r'/[a-z0-9-]+-mahjong-tile-matches', u))
    with ThreadPoolExecutor(16) as ex:
        got = dict(zip(brand_pages + album_pages, ex.map(lambda p: get(SITE + p), brand_pages + album_pages)))
    net['brand_pages'] = {}
    for p in brand_pages:
        st, fin, h = got[p]
        ds = verified_dates(visible(h)) if st == 200 else []
        net['brand_pages'][p] = {'status': st, 'redirected': nu(fin) != nu(SITE + p), 'verified': str(max(ds)) if ds else None,
                                 'verified_min': str(min(ds)) if ds else None}
    # album pages: keep a normalized name blob per page (for "her picks named on the page"), dropped after use
    net['album_pages'] = {}
    blobs = {}
    for p in album_pages:
        st, fin, h = got[p]
        net['album_pages'][p] = {'status': st, 'redirected': nu(fin) != nu(SITE + p)}
        blobs[p] = nz(visible(h)) if st == 200 else ''
    blobs['/holiday-mahjong-matches'] = nz(visible(hol)) if s5 == 200 else ''
    return net, blobs

old = {}
try: old = json.load(open(OUT))
except Exception: pass
net = old.get('net') or {}
try: age_h = (NOW - datetime.datetime.fromisoformat(net['at'])).total_seconds() / 3600
except Exception: age_h = 99
blobs = None
if REFRESH or age_h > MAX_NET_AGE_H or not net.get('fym_pin'):
    net, blobs = refresh_net()
    age_h = 0

# ---------------------------------------------------------------- load live builds
src = {}
pin = net.get('fym_pin')
fym_html = git_show(pin['sha'], pin['path']) if pin else None
if fym_html:
    src['fym'] = f"{pin['path']} @{pin['sha'][:8]} (live /find-your-match)"
else:  # fall back to the newest preview build in the website worktree
    vs = sorted((int(d[5:]), d) for d in os.listdir(FYM_WORKTREE + '/site-app') if re.fullmatch(r'fym-v\d+', d))
    p = f'{FYM_WORKTREE}/site-app/{vs[-1][1]}/index.html'
    fym_html = open(p).read(); src['fym'] = f'{p} (NEWEST PREVIEW, live pin unreadable)'
i = fym_html.index('const D=') + 8
D, _ = json.JSONDecoder().raw_decode(fym_html, i)
try:
    j = fym_html.index('BACKG=') + 6; BACKG, _ = json.JSONDecoder().raw_decode(fym_html, j)
except Exception: BACKG = {}
FYM_VER = (re.search(r'fym-(v\d+)', src['fym']) or [None, '?'])[1]
del fym_html

M, T, RK, S, TV = D['mats'], D['tiles'], D['racks'], D['sets'], D['tv']
vis_sets = [s for s in S if not s.get('hid') and not T.get(s['tile'], {}).get('hid')]
vis_mats = [k for k, v in M.items() if not v.get('hid')]
vis_racks = [k for k, v in RK.items() if not v.get('hid')]

G = None
gp = net.get('gallery_pin')
if gp:
    t = git_show(gp['sha'], gp['path'])
    if t: G = json.loads(t); src['gallery'] = f"{gp['path'].split('/')[-1]} @{gp['sha'][:8]} (live /mahjong-mats, data-fym={net.get('gallery_data_fym')})"
SIDX = None
sp = net.get('search_pin')
if sp:
    t = git_show(sp['sha'], sp['path'])
    if t: SIDX = json.loads(t); src['search'] = f"search-index.json @{sp['sha'][:8]} (live search.js pin)"

truth = json.load(open('config/code-truth.json'))
P = truth['pct']; MAXAGE = truth.get('verified_max_age_days', 9)
REMOVED_BRANDS = truth.get('removed_brands', {})
REMOVED_PAGES = {p for o in REMOVED_BRANDS.values() for p in o.get('removed_pages', [])}

# ---------------------------------------------------------------- lines
L = []
def line(id_, area, label, have, total, target=None, unit='', missing=None, note='', zero=False, status=None):
    """zero=True: `have` is a count that should be 0 (target 0)."""
    if status is None:
        if zero: status = 'OK' if have == 0 else 'GAP'
        else: status = 'OK' if total and have >= (total if target is None else target) else 'GAP'
    tgt = '0' if zero else ('all' if target is None else str(target))
    txt = f'{label}: {have}' + ('' if zero else f' of {total}') + (f' {unit}' if unit else '') + f' (target {tgt})'
    if note: txt += f'; {note}'
    if missing:
        ms = list(missing)
        txt += ' | missing: ' + ', '.join(map(str, ms[:6])) + (f' +{len(ms) - 6} more' if len(ms) > 6 else '')
    L.append({'id': id_, 'area': area, 'status': status, 'have': have, 'total': total, 'target': tgt, 'text': txt})

vn = lambda k, D_=M: (D_.get(k) or {}).get('n', k)

# --- FYM tile sets
N = len(vis_sets)
backs = TV.get('backs', {})
line('walls', 'FYM', 'Table view walls (back colour confirmed)', sum(1 for s in vis_sets if s['slug'] in backs), N, unit='visible tile sets',
     missing=[s['name'] for s in vis_sets if s['slug'] not in backs])
line('tile_photo', 'FYM', 'Tile sets with a tile photo', sum(1 for s in vis_sets if T.get(s['tile'], {}).get('full') or T.get(s['tile'], {}).get('src')), N,
     missing=[s['name'] for s in vis_sets if not (T.get(s['tile'], {}).get('full') or T.get(s['tile'], {}).get('src'))])
line('pile', 'FYM', 'Tile sets with a pile image', sum(1 for s in vis_sets if T.get(s['tile'], {}).get('pile')), N,
     missing=[s['name'] for s in vis_sets if not T.get(s['tile'], {}).get('pile')])
in_col = {n for g, names in BACKG.items() for n in names}
line('tile_colours', 'FYM', 'Tile sets in a colour group (tile colour filter)', sum(1 for s in vis_sets if s['name'] in in_col), N,
     missing=[s['name'] for s in vis_sets if s['name'] not in in_col])
line('tagline', 'FYM', 'Tile sets with a tagline ("dating profile" line)', sum(1 for s in vis_sets if s.get('tag')), N,
     missing=[s['name'] for s in vis_sets if s.get('album') and not s.get('tag')])

# --- albums wired to FYM
COLOUR_PAGES = {a[0] for a in (SIDX or {}).get('a', []) if a[5] == 1} or {'/mahjong-tile-matches'}
ap = net.get('album_pages', {})
live_albums = [p for p, v in ap.items() if v['status'] == 200 and not v['redirected'] and p not in COLOUR_PAGES and p not in REMOVED_PAGES]
fym_album_paths = {s['album'].replace(SITE, '').replace('https://mahjmatchmaker.com', '').split('#')[0] for s in vis_sets if s.get('album')}
line('albums_in_fym', 'Albums', 'Live album pages wired to an FYM tile set', sum(1 for p in live_albums if p in fym_album_paths), len(live_albums),
     missing=[p.strip('/').replace('-mahjong-tile-matches', '') for p in live_albums if p not in fym_album_paths])
picks = [s for s in vis_sets if s['m']]
line('fym_album_link', 'Albums', 'FYM sets with her picks that link to their album', sum(1 for s in picks if s.get('album')), len(picks),
     missing=[s['name'] for s in picks if not s.get('album')])
hol_sets = [s for s in vis_sets if '/holiday-mahjong-matches' in (s.get('album') or '')]
if hol_sets:
    line('holiday_anchor', 'Albums', 'Holiday sets linking to their own holiday-page section', sum(1 for s in hol_sets if '#' in s['album']), len(hol_sets),
         missing=[s['name'] for s in hol_sets if '#' not in s['album']])
# her picks named on the live album page (computed at refresh, cached)
if blobs is not None:
    tot = named = 0; miss = {}
    for s in picks:
        p = (s.get('album') or '').replace(SITE, '').split('#')[0]
        b = blobs.get(p)
        if not b: continue
        for k, _r in s['m']:
            n = vn(k)
            n = re.sub(r'^.*:', '', n) if n == k else n
            cands = {nz(n), nz(re.sub(r'\s*\(.*?\)', '', n)), nz(re.sub(r'\b(mahjong|mahj|mat|neoprene|leatherette|vegan leather)\b', '', n, flags=re.I))}
            cands = {c for c in cands if len(c) >= 4}
            tot += 1
            if any(c in b for c in cands): named += 1
            else: miss[n] = miss.get(n, 0) + 1
    net['album_picks'] = {'fym': FYM_VER, 'named': named, 'total': tot,
                          'top_missing': [f'{n} ({c})' for n, c in sorted(miss.items(), key=lambda x: -x[1])[:10]]}
apk = net.get('album_picks')
if apk:
    line('album_picks', 'Albums', 'Her FYM picks named on the live album page', apk['named'], apk['total'],
         note='name match, a little noise' + ('' if apk['fym'] == FYM_VER else f"; measured on {apk['fym']}"), missing=apk['top_missing'])

# --- table view mats / racks
cls = TV.get('cls', {})
line('tv_mats_checked', 'FYM', 'Mats checked for Table view (have a class)', sum(1 for k in vis_mats if k in cls), len(vis_mats), unit='visible mats',
     missing=[f"{M[k]['bn']}: {M[k]['n']}" for k in vis_mats if k not in cls])
line('tv_mats_usable', 'FYM', 'Mats usable in Table view (class A/B)', sum(1 for k in vis_mats if cls.get(k) in ('A', 'B')), len(vis_mats),
     note=f"{sum(1 for k in vis_mats if cls.get(k) == 'C')} class C (need a flat photo)")
rk = TV.get('rk', {})
line('tv_racks', 'FYM', 'Racks usable in Table view', sum(1 for k in vis_racks if k in rk), len(vis_racks), unit='visible racks',
     missing=[RK[k]['n'] for k in vis_racks if k not in rk])

# --- prices
pm, pt, pr = TV.get('pm', {}), TV.get('pt', {}), TV.get('price', {})
from collections import Counter
mb = Counter(M[k]['bn'] for k in vis_mats if k not in pm)
line('price_mats', 'FYM', 'Mats with a price (price filter hides the rest)', sum(1 for k in vis_mats if k in pm), len(vis_mats),
     missing=[f'{b} {c}' for b, c in mb.most_common()])
line('price_tiles', 'FYM', 'Tile sets with a price', sum(1 for s in vis_sets if s['tile'] in pt), N, missing=[s['name'] for s in vis_sets if s['tile'] not in pt])
line('price_racks', 'FYM', 'Racks with a price', sum(1 for k in vis_racks if k in pr), len(vis_racks), missing=[RK[k]['n'] for k in vis_racks if k not in pr])

# --- gallery vs FYM (both directions; matched like gate [90]: FYM key via gallery manifests, product URL, or name + brand)
if G is not None:
    GALD = 'site/livepatch/matgallery/'
    def lj(p, d=None):
        try: return json.load(open(p))
        except Exception: return d
    MAN = lj(GALD + 'manifest.json', {}); N53 = (lj(GALD + 'new53_rows.json', {}) or {}).get('manifest', {})
    RA = {a['gallery_id']: a['fym_key'] for a in lj(GALD + 'retired_additions_oct20.json', [])}
    XR = lj('config/mat-gallery-extra-rows.json', {'rows': []})['rows']
    RA.update({a['img']: a['key'] for a in XR})
    GK = lambda im: MAN.get(im) or N53.get(im) or RA.get(im)
    nameb = lambda n, b: nz(re.sub(r'\b(neoprene|leatherette|vegan leather|mahjong|mat)\b', '', n or '', flags=re.I)) + '|' + nz(b)
    GKS = {GK(r[0]) for r in G}; GU = {nu(r[3]) for r in G if r[3]}; GN = {nameb(r[1], r[2]) for r in G}
    XT = lj('config/mat-gallery-crosstags.json', {}).get('remove_mats', {})
    RMB = set(XT.get('brands', [])); RMK = {MAN.get(i) for i in XT.get('imgs', [])}
    SKIPB = {'House of Hearts Studio'}  # Tiffany Oct 25 11:06: FYM only for now
    def in_gal(k):
        v = M[k]
        return k in GKS or nu(v.get('u')) in GU or nu(v.get('u0')) in GU or nameb(v['n'], v['bn']) in GN
    elig = [k for k in vis_mats if M[k]['bn'] not in SKIPB | RMB and k not in RMK and '#side-b' not in k and not M[k].get('twin')]
    miss = [k for k in elig if not in_gal(k)]
    line('gallery_has_fym', 'Gallery', 'Visible FYM mats that are in the live Mat Gallery', len(elig) - len(miss), len(elig),
         note='House of Hearts (FYM only), Mahjong Studios, side-B twins left out', missing=[f"{M[k]['bn']}: {M[k]['n']}" for k in miss])
    # reverse: gallery rows whose FYM mat is hidden
    UK = {}
    for k, v in M.items():
        for u in (v.get('u'), v.get('u0')):
            if u: UK.setdefault(nu(u), k)
    NK = {nameb(v['n'], v['bn']): k for k, v in M.items()}
    hid_rows = []; unmapped = 0
    for r in G:
        k = GK(r[0]); k = k if k in M else (UK.get(nu(r[3])) or NK.get(nameb(r[1], r[2])))
        if not k: unmapped += 1
        elif M[k].get('hid'): hid_rows.append(f'{r[2]}: {r[1]}')
    line('gallery_shows_hidden', 'Gallery', 'Gallery mats that FYM hides', len(hid_rows), len(G), zero=True,
         note=f'{unmapped} gallery rows not found in FYM at all', missing=hid_rows)
    gv = net.get('gallery_data_fym')
    line('gallery_version', 'Gallery', f'Live gallery built from the live FYM ({FYM_VER})', int(gv == FYM_VER), 1,
         note=f'gallery data-fym={gv}', status='OK' if gv == FYM_VER else 'GAP')
if SIDX is not None:
    sa = {a[0] for a in SIDX.get('a', [])}
    line('search_albums', 'Search', 'Live album pages in the site search', sum(1 for p in live_albums if p in sa), len(live_albums),
         missing=[p for p in live_albums if p not in sa])
    hid_ids = net.get('holiday_ids', {})
    bad = [a for a in sa if a.startswith('/holiday-mahjong-matches#') and hid_ids.get(a.split('#')[1], True)]
    line('search_hidden', 'Search', 'Search entries pointing at hidden/missing holiday sections', len(bad), len(sa), zero=True,
         missing=[a.split('#')[1] for a in sorted(bad)])
    if G is not None:
        gi = {r[0] for r in G}; si = {m[0] for m in SIDX.get('m', [])}
        line('search_mats', 'Search', 'Gallery mats findable in site search', len(gi & si), len(gi), missing=sorted(gi - si))

# --- partner brands / code pages
hb = net.get('hub_brands', [])
removed_names = {nz(b) for b in REMOVED_BRANDS}
hb = [(n, h) for n, h in hb if nz(n) not in removed_names]
PN = {nz(b) for b in P}
line('truth_brands', 'Codes', 'Hub brands with a code-truth % entry (live_codes_check can catch a wrong %)',
     sum(1 for n, _ in hb if nz(n) in PN), len(hb), missing=[n for n, _ in hb if nz(n) not in PN])
line('hub_pages', 'Codes', 'Hub brands with their own brand page', sum(1 for _, h in hb if h.startswith('/')), len(hb),
     missing=[n for n, h in hb if not h.startswith('/')])
bp = net.get('brand_pages', {})
hub_paths = {h for _, h in hb}
live_bp = {p: v for p, v in bp.items() if v['status'] == 200 and not v['redirected'] and p not in REMOVED_PAGES}
fresh = [p for p, v in live_bp.items() if v['verified_min'] and (TODAY - datetime.date.fromisoformat(v['verified_min'])).days <= MAXAGE]
line('verified', 'Codes', f'Live brand pages with a verified line within {MAXAGE} days', len(fresh), len(live_bp),
     note=f"as of {net.get('at', '?')[:16]}",
     missing=[p.strip('/') + (f" ({v['verified_min']})" if v['verified_min'] else ' (no line)') for p, v in sorted(live_bp.items()) if p not in fresh])
orphan = [p for p in live_bp if p not in hub_paths]
line('orphan_brand_pages', 'Codes', 'Live brand pages in the sitemap but not on the codes hub', len(orphan), len(live_bp), zero=True, missing=sorted(orphan))
sm = set(net.get('sitemap', []))
still = [p for p in sorted(REMOVED_PAGES) if (bp.get(p, {}).get('status') == 200 and not bp.get(p, {}).get('redirected')) or p in sm]
line('removed_live', 'Codes', 'Removed pages still live or in the sitemap', len(still), len(REMOVED_PAGES), zero=True,
     missing=[p + (' (200)' if bp.get(p, {}).get('status') == 200 and not bp.get(p, {}).get('redirected') else '') + (' (sitemap)' if p in sm else '') for p in still])

# --- ShopMy sync (reuse the latest cross-check file; never refetch here)
import glob
cc = sorted(glob.glob('config/shopmy-crosscheck-*.json'), key=os.path.getmtime)
if cc:
    j = json.load(open(cc[-1])); tv_ = j.get('summary', {}).get('totals_v117') or next((v for k, v in j.get('summary', {}).items() if k.startswith('totals')), {})
    pins = tv_.get('mat_pins', 0); amz = tv_.get('amazon_her_pick', 0); skip = tv_.get('decided_skip', 0); hidn = tv_.get('fym_hidden', 0)
    infym = tv_.get('in_fym_v117', next((v for k, v in tv_.items() if k.startswith('in_fym')), 0))
    target = pins - amz - skip - hidn
    stale = '' if j.get('fym_build') == FYM_VER else f"; checked against {j.get('fym_build')}, live is {FYM_VER}"
    line('shopmy_fym', 'ShopMy', 'ShopMy mats live in FYM', infym, target,
         note=f"{os.path.basename(cc[-1])}: {tv_.get('staged_for_118', '?')} staged, {amz} Amazon (her pick), {skip} skipped, {hidn} photo-held" + stale)
    line('shopmy_unaccounted', 'ShopMy', 'ShopMy mats not in FYM, staged or decided', len(j.get('missing', [])), pins, zero=True,
         missing=[f"{x.get('brand')}: {x.get('name')}" for x in j.get('missing', [])])
else:
    L.append({'id': 'shopmy_fym', 'area': 'ShopMy', 'status': 'UNKNOWN', 'have': None, 'total': None, 'target': 'all',
              'text': 'ShopMy mats live in FYM: unknown (no config/shopmy-crosscheck-*.json; run scripts/checks/shopmy_sync_check.py)'})

# --- approved but not done (OVERDUE.md + DESK "Blocked, approved")
def first_date(s):
    m = re.search(r'since (20\d\d-\d\d-\d\d)', s)
    if m: return datetime.date.fromisoformat(m.group(1))
    m = re.search(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? (\d{1,2})\b', s)
    if m:
        d = datetime.date(TODAY.year, MON[m.group(1).lower()], int(m.group(2)))
        return d if d <= TODAY else d.replace(year=TODAY.year - 1)
    return None
items = []
try: items += [('OVERDUE', l.strip()) for l in open('docs/OVERDUE.md') if l.startswith('- ')]
except Exception: pass
try:
    d = open('docs/DESK.md').read(); m = re.search(r'## Blocked, approved[^\n]*\n(.*?)\n## ', d, re.S)
    items += [('DESK', l.strip()) for l in (m.group(1).splitlines() if m else []) if l.strip().startswith('-')]
except Exception: pass
old_items, undated = [], []
for where, s in items:
    dt = first_date(s); short = re.sub(r'[*`]', '', s[2:])[:70]
    if dt is None: undated.append(f'{where}: {short}')
    elif (TODAY - dt).days > 3: old_items.append(f'{where} {dt:%b %-d}: {short}')
line('approved_old', 'Ops', 'Approved/overdue items older than 3 days (OVERDUE + DESK Blocked)', len(old_items), len(items), zero=True,
     note=f'{len(undated)} more carry no date, so they cannot age (give each a date)', missing=old_items)
if undated:
    L[-1]['status'] = 'GAP'

# --- scheduled tasks off
try:
    tj = json.load(open('docs/status/tasks-off.json'))
    tage = (NOW - datetime.datetime.fromisoformat(tj['at'])).total_seconds() / 3600
    off = tj.get('off', [])
    if tage > 48: raise ValueError('stale')
    line('tasks_off', 'Ops', 'Scheduled tasks switched off', len(off), None, zero=True, note=f"listed {tj['at'][:16]}",
         missing=[f"{o.get('name')} ({o.get('reason', '?')})" for o in off])
except Exception as e:
    L.append({'id': 'tasks_off', 'area': 'Ops', 'status': 'UNKNOWN', 'have': None, 'total': None, 'target': '0',
              'text': 'Scheduled tasks switched off: unknown (' + ('docs/status/tasks-off.json older than 48h' if str(e) == 'stale' else 'no docs/status/tasks-off.json')
                      + '; an attended chat runs list_triggers and writes it)'})

# ---------------------------------------------------------------- output
for e in net.get('errors', []):
    L.append({'id': 'net_error', 'area': 'Ops', 'status': 'UNKNOWN', 'have': None, 'total': None, 'target': '', 'text': 'network: ' + e})
# front-door order (HQ-CLEANUP section 4: Google/codes first, then money, then FYM usefulness, then albums/search)
PRIO = ['removed_live', 'tasks_off', 'truth_brands', 'verified', 'hub_pages', 'orphan_brand_pages', 'approved_old', 'shopmy_unaccounted',
        'shopmy_fym', 'price_mats', 'gallery_has_fym', 'gallery_shows_hidden', 'gallery_version', 'albums_in_fym', 'fym_album_link',
        'walls', 'tv_mats_checked', 'tv_racks', 'tv_mats_usable', 'price_tiles', 'price_racks', 'album_picks', 'search_hidden',
        'holiday_anchor', 'search_albums', 'search_mats', 'tile_colours', 'tile_photo', 'pile', 'tagline']
L.sort(key=lambda x: PRIO.index(x['id']) if x['id'] in PRIO else len(PRIO))
gaps = [x for x in L if x['status'] == 'GAP']
unk = [x for x in L if x['status'] == 'UNKNOWN']
res = {'at': NOW.isoformat(timespec='seconds'), 'fym': FYM_VER, 'sources': src, 'net_at': net.get('at'),
       'summary': f'{len(L) - len(gaps) - len(unk)} OK, {len(gaps)} GAP, {len(unk)} UNKNOWN',
       'gaps': [x['text'] for x in gaps], 'unknown': [x['text'] for x in unk], 'lines': L,
       'net': {k: v for k, v in net.items()}}
os.makedirs('docs/status', exist_ok=True)
json.dump(res, open(OUT, 'w'), indent=1, ensure_ascii=False)
print(f"COVERAGE CHECK {res['at'][:16]} · FYM {FYM_VER} · {res['summary']} · network data {net.get('at', '?')[:16]} · {time.time() - T0:.1f}s")
for k, v in src.items(): print(f'  source {k}: {v}')
for x in L: print(f"{x['status']:<7} [{x['area']}] {x['text']}")
sys.exit(1 if gaps else 0)
