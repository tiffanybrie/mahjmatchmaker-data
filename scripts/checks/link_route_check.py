#!/usr/bin/env python3
"""Link-route check (Tiffany Nov 8 2026 6:02pm: "close the ShopMy gap once and for all").

Every VISIBLE shop link in Find Your Mat-ch (D.mats / D.racks / D.tiles `u`) and in the Mat Gallery (row[3]) must be paid the way
config/link-routes.json says for its brand:
  code-site      -> the brand's own store host (store_hosts); never go.shopmy.us
  shopmy-site    -> go.shopmy.us, landing on the brand's store host (or an exception_hosts retailer)
  shopmy-etsy    -> go.shopmy.us, landing on etsy.com
  shopmy-amazon  -> go.shopmy.us landing on amazon.com, OR a direct amzn.to / amazon.com link carrying the Associates tag
  none           -> any plain link (no commission); a go.shopmy.us link here means the table is out of date
Also allowed for every route: an empty link (no shop button) and our own pages (internal_ok, e.g. retired sets -> album page).
Per-brand exception_hosts (e.g. Bam! Let's Mahjong products sold by Printfresh) are allowed alongside the main route.
A brand with no row in the table FAILS (add the row the day a brand comes in).

go.shopmy.us destinations: the 302 Location reveals the store (url= on apiv3 redirect_click, murl= on linksynergy (Etsy),
btn_url= on amzlink (Amazon)). Pin destinations never change, so they are cached for good in config/shopmy-redirect-cache.json.
By default a SAMPLE per brand is resolved (--sample N, default 4; --all resolves every uncached pin).

Staged fixes: config/link-route-fixes.json `items` ("<group>|<key>" -> {u, ...}) are the corrected links waiting for the next FYM
build (builder/fym_fix_nov08/apply_link_routes.py applies them). A mismatch with a staged fix is reported as STAGED, not FAIL, in the
daily/live run; in the gate (--gate) a staged-but-unapplied fix FAILS, because the build must carry it.

Usage:
  python3 scripts/checks/link_route_check.py [<build dir | index.html>] [--gallery <rows.json>] [--gate] [--all] [--sample N] [--json out]
  no build given = the newest WEBSITE copy (origin/fym-site-preview site-app/fym-vNN) + the staged Mat Gallery data.
Prints PASS/FAIL + every mismatch; exit 1 on FAIL. Imported by builder/fym_gate.py [172] and gallery_sync_check.py --links.
"""
import sys, os, re, json, glob, subprocess, time, urllib.request, urllib.parse, collections

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
ROUTES = REPO + 'config/link-routes.json'
FIXES = REPO + 'config/link-route-fixes.json'
CACHE = REPO + 'config/shopmy-redirect-cache.json'
UA = {'User-Agent': 'Mozilla/5.0 (MahjMatchmaker link-route check)'}
AMAZON = ('amazon.com', 'amzn.to', 'a.co')


def host(u):
    try:
        h = urllib.parse.urlsplit((u or '').strip()).netloc.lower()
    except Exception:
        return ''
    h = h.split('@')[-1].split(':')[0]
    return h[4:] if h.startswith('www.') else h


def same(h, hosts):
    return any(h == x or h.endswith('.' + x) for x in hosts if x)


def load_json(p, default):
    try:
        return json.load(open(p))
    except Exception:
        return default


def resolve(u, cache):
    """go.shopmy.us/p-<id> -> destination host ('' = unknown). Cached forever by pin URL."""
    k = u.split('?')[0].rstrip('/')
    if k in cache:
        return cache[k]
    loc = ''
    for a in range(3):
        try:
            req = urllib.request.Request(k, headers=UA, method='GET')
            opener = urllib.request.build_opener(NoRedirect)
            try:
                opener.open(req, timeout=20)
            except urllib.error.HTTPError as e:
                loc = e.headers.get('Location') or ''
            break
        except Exception:
            time.sleep(2 + 2 * a)
    if not loc:
        return ''
    q = urllib.parse.parse_qs(urllib.parse.urlsplit(loc).query)
    dest = (q.get('url') or q.get('murl') or q.get('btn_url') or [loc])[0]
    d = {'host': host(dest), 'dest': dest[:300], 'at': time.strftime('%Y-%m-%d')}
    if same(d['host'], AMAZON):
        m = re.search(r'[?&]tag=([\w-]+)', dest)
        d['tag'] = m.group(1) if m else None
    cache[k] = d
    return d


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def website_build():
    ls = subprocess.run(['git', '-C', REPO, 'ls-tree', '--name-only', 'origin/fym-site-preview', 'site-app/'], capture_output=True, text=True).stdout.split()
    vs = sorted((int(m.group(1)), x) for x in ls for m in [re.search(r'fym-v(\d+)$', x)] if m)
    if not vs:
        raise SystemExit('no site-app/fym-vNN on origin/fym-site-preview (git fetch first)')
    return subprocess.run(['git', '-C', REPO, 'show', f'origin/fym-site-preview:{vs[-1][1]}/index.html'], capture_output=True, text=True).stdout, vs[-1][1]


def load_D(html):
    i = html.find('const D=') + 8
    D, _ = json.JSONDecoder().raw_decode(html, i)
    return D


def staged_gallery_rows():
    gp = sorted(glob.glob(REPO + 'site/livepatch/matgallery/matgallery-v[0-9]*.html'), key=lambda p: int(re.search(r'-v(\d+)\.html$', p).group(1)))[-1]
    g = open(gp).read()
    gm = re.search(r'<script type="application/json"( data-src="[^"]*")?>(.*?)</script>', g, re.S)
    if gm.group(1):
        return json.load(open(REPO + re.search(r'@[0-9a-f]{7,40}/(.*?)"', gm.group(1)).group(1))), os.path.basename(gp)
    return json.loads(gm.group(2).replace('<\\/', '</')), os.path.basename(gp)


def items(D=None, G=None):
    """[(where, group, key, name, brand, url)] for every visible FYM item and every gallery row."""
    out = []
    if D:
        for g in ('mats', 'racks', 'tiles'):
            for k, o in (D.get(g) or {}).items():
                if o.get('hid'):
                    continue
                out.append(('fym', g, k, o.get('n'), o.get('bn'), (o.get('u') or '').strip()))
    for r in G or []:
        out.append(('gallery', 'gallery', r[0], r[1], r[2], (r[3] or '').strip() if len(r) > 3 and isinstance(r[3], str) else ''))
    return out


def verdict(row, u, cache, resolve_it, tables):
    """-> (ok, why). resolve_it=False skips the network for go.shopmy.us (host-only check)."""
    if not u:
        return True, 'no link'
    h = host(u)
    if same(h, tables['internal_ok']):
        return True, 'our page'
    route = row['route']; hosts = row.get('store_hosts') or []; exc = row.get('exception_hosts') or []
    tag = row.get('associates_tag') or tables.get('tag')
    if h == 'go.shopmy.us':
        if route in ('code-site', 'none') and not exc:
            return False, f'go.shopmy.us link but route is {route}'
        if not resolve_it:
            return True, 'shopmy (not resolved)'
        d = resolve(u, cache)
        if not d or not d.get('host'):
            return True, 'shopmy (redirect unreadable, warn)'
        dh = d['host']
        if route == 'shopmy-etsy':
            return (same(dh, ['etsy.com']), f'ShopMy lands on {dh}, expected etsy.com')
        if route == 'shopmy-amazon':
            return (same(dh, AMAZON), f'ShopMy lands on {dh}, expected amazon.com')
        if route == 'shopmy-site':
            return (same(dh, hosts + exc) and not same(dh, ['etsy.com']), f'ShopMy lands on {dh}, expected {"/".join(hosts + exc)}')
        if exc and same(dh, exc):
            return True, 'exception retailer via ShopMy'
        return False, f'ShopMy lands on {dh} but route is {route}'
    if exc and same(h, exc):
        return True, 'exception host'
    if route == 'code-site':
        return (same(h, hosts), f'{h} is not the store ({"/".join(hosts)})')
    if route == 'none':
        return True, 'no-commission brand'
    if route == 'shopmy-amazon' and same(h, AMAZON):
        if h == 'amzn.to':
            d = resolve_amzn(u, cache) if resolve_it else {'tag': tag}
            return (d.get('tag') == tag, f'amzn.to link without Associates tag {tag}')
        return (f'tag={tag}' in u, f'amazon.com link without Associates tag {tag}')
    return False, f'plain {h} link, route is {route} (needs a go.shopmy.us link)'


def resolve_amzn(u, cache):
    k = u.split('?')[0]
    if k in cache:
        return cache[k]
    try:
        urllib.request.build_opener(NoRedirect).open(urllib.request.Request(k, headers=UA), timeout=20)
        loc = ''
    except urllib.error.HTTPError as e:
        loc = e.headers.get('Location') or ''
    except Exception:
        return {}
    m = re.search(r'[?&]tag=([\w-]+)', loc)
    cache[k] = {'host': host(loc), 'tag': m.group(1) if m else None, 'at': time.strftime('%Y-%m-%d')}
    return cache[k]


def check(D=None, G=None, gate=False, sample=4, resolve_all=False, net=True):
    """-> dict(fails=[...], staged=[...], warns=[...], info=[...], rows=[...])"""
    T = load_json(ROUTES, {})
    B = T.get('brands', {})
    tables = {'internal_ok': T.get('internal_ok', ['mahjmatchmaker.com']), 'tag': 'heritagesig05-20'}
    fixes = load_json(FIXES, {}).get('items', {})
    by_old = {x['old_u']: x for x in fixes.values() if x.get('old_u')}  # gallery rows are keyed by image, so match them by the old link
    cache = load_json(CACHE, {})
    n0 = len(cache)
    fails, staged, warns, rows = [], [], [], []
    per_brand_sm = collections.Counter()
    seen_brand = collections.Counter()
    for where, g, k, n, b, u in items(D, G):
        row = B.get(b)
        seen_brand[b] += 1
        if row is None:
            fails.append(f'{where} {g} {n} ({b}): brand has no row in config/link-routes.json')
            continue
        rs = False
        if net and host(u) in ('go.shopmy.us', 'amzn.to'):
            key = u.split('?')[0].rstrip('/')
            if resolve_all or key in cache or per_brand_sm[b] < sample:
                rs = True
                if key not in cache:
                    per_brand_sm[b] += 1
        ok, why = verdict(row, u, cache, rs, tables)
        if 'warn' in why:
            warns.append(f'{where} {g} {n} ({b}): {why}')
        if ok:
            continue
        fk = f'{g}|{k}'
        fx = fixes.get(fk) or (by_old.get(u) if where == 'gallery' else None)
        line = f'{where} {g} {n} ({b}, route {row["route"]}): {why} | {u[:110]}'
        rows.append({'where': where, 'group': g, 'key': k, 'name': n, 'brand': b, 'route': row['route'], 'why': why, 'u': u, 'staged': bool(fx)})
        if fx and fx.get('u') != u:
            (fails if (gate and where == 'fym') else staged).append(line + f' -> STAGED {fx.get("u")} ({fx.get("for", "next FYM build")})')
        elif fx and fx.get('u') == u:
            continue
        elif row.get('pending_fix'):
            (fails if (gate and where == 'fym') else staged).append(line + f' -> {row["pending_fix"]}')
        else:
            fails.append(line)
    if len(cache) != n0:
        json.dump(cache, open(CACHE, 'w'), indent=0, sort_keys=True)
    unused = [b for b in B if not seen_brand.get(b) and B[b]['route'] != 'none']
    info = [f'{sum(seen_brand.values())} links, {len(seen_brand)} brands, {len(cache)} ShopMy/Amazon redirects known']
    if unused:
        info.append('table rows with no visible item: ' + ', '.join(sorted(unused)))
    return {'fails': fails, 'staged': staged, 'warns': warns, 'info': info, 'rows': rows}


def main():
    a = sys.argv[1:]
    opt = lambda n, d=None: a[a.index(n) + 1] if n in a else d
    pos = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] not in ('--gallery', '--sample', '--json'))]
    if pos:
        p = pos[0]
        html = open(p if p.endswith('.html') else os.path.join(p, 'index.html')).read(); src = p
    else:
        html, src = website_build()
    D = load_D(html)
    if opt('--gallery'):
        G = json.load(open(opt('--gallery'))); gsrc = opt('--gallery')
    elif '--no-gallery' in a:
        G, gsrc = [], '-'
    else:
        G, gsrc = staged_gallery_rows()
    r = check(D, G, gate='--gate' in a, sample=int(opt('--sample', 4)), resolve_all='--all' in a)
    if opt('--json'):
        json.dump(r, open(opt('--json'), 'w'), indent=1, ensure_ascii=False)
    head = f'FYM {src} + gallery {gsrc} | ' + '; '.join(r['info'])
    for s in r['staged']:
        print('  STAGED ' + s)
    for w in r['warns'][:20]:
        print('  WARN ' + w)
    if r['fails']:
        print(f'FAIL link_route_check: {len(r["fails"])} mismatches ({len(r["staged"])} staged) | {head}')
        for f in r['fails']:
            print('  ' + f)
        sys.exit(1)
    print(f'PASS link_route_check: 0 unstaged mismatches ({len(r["staged"])} staged) | {head}')


if __name__ == '__main__':
    main()
