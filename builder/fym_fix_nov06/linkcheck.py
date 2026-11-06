"""FYM shop-link check (Nov 6 2026, FYM 1.16; standing authority: broken link fixes). 11 shop links were found dead on Nov 6
(config/mat-gallery-link-fixes.json) only because the Mat Gallery build happened to check them. Gate [162] now curl-checks EVERY visible
FYM shop link (D.mats / D.racks / D.tiles `u`) and FAILS on 404 / 410.

- An auto-apply link (/discount/<CODE>?redirect=<path>) is checked at its landing page (host + redirect path), i.e. the product page.
- Query strings are dropped (a ?variant= never 404s by itself), so each product page is fetched once.
- Skipped: ShopMy (go.shopmy.us) and Etsy (both block bots), Amazon (amzn.to / amazon.com, same).
- Results are cached in config/fym-link-check-cache.json: a 2xx/3xx answer is trusted for 7 days, a 404/410 for 12 hours, anything else
  (403, 429, 5xx, timeout) is re-tried on the next run and only WARNED about.
Fix for a dead link: builder/fym_fix_nov06/deadlinks116.py (config/mat-gallery-link-fixes.json): no shop button, NOT 'Retired'.
Usage: python3 builder/fym_fix_nov06/linkcheck.py <build dir or index.html>   (prints dead + unknown; exit 1 on dead)"""
import json, os, sys, time, subprocess
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlsplit, urlunsplit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import autoapply_links as AA

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
CACHE = REPO + 'config/fym-link-check-cache.json'
SKIP = ('go.shopmy.us', 'etsy.com', 'amzn.to', 'amazon.com')
OK_TTL, BAD_TTL = 7 * 86400, 12 * 3600
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'


def target(u):
    """The page a shop link lands on, without its query; None = not checked (empty or skipped host)."""
    u = (u or '').strip()
    if not u.startswith('http'):
        return None
    h = AA.host_of(u)
    if any(h == s or h.endswith('.' + s) for s in SKIP):
        return None
    p = urlsplit(u)
    path = p.path
    if path.startswith('/discount/'):
        path = urlsplit(AA.redirect_target(u) or '/').path or '/'
    return urlunsplit((p.scheme or 'https', p.netloc, path, '', ''))


def fetch(url):
    try:
        r = subprocess.run(['curl', '-s', '-o', '/dev/null', '-L', '--max-redirs', '6', '-m', '25', '-A', UA, '-w', '%{http_code}', url],
                           capture_output=True, text=True, timeout=40)
        return int(r.stdout.strip() or 0)
    except Exception:
        return 0


def check(D, workers=16, now=None):
    """-> (dead, unknown, n_checked). dead/unknown = [(group, key, name, brand, url, status)]."""
    now = now or time.time()
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    items = []
    for g in ('mats', 'racks', 'tiles'):
        for k, o in (D.get(g) or {}).items():
            if o.get('hid'):
                continue
            t = target(o.get('u'))
            if t:
                items.append((g, k, o.get('n'), o.get('bn'), o.get('u'), t))
    def fresh(t):
        c = cache.get(t)
        if not c:
            return False
        s, age = c['s'], now - c['t']
        if 200 <= s < 400:
            return age < OK_TTL
        if s in (404, 410):
            return age < BAD_TTL
        return False
    todo = sorted({t for *_, t in items if not fresh(t)})
    if todo:
        with ThreadPoolExecutor(workers) as ex:
            for t, s in zip(todo, ex.map(fetch, todo)):
                cache[t] = {'s': s, 't': int(now)}
        json.dump(dict(sorted(cache.items())), open(CACHE, 'w'), indent=0)
    dead, unk = [], []
    for g, k, n, b, u, t in items:
        s = cache[t]['s']
        if s in (404, 410):
            dead.append((g, k, n, b, u, s))
        elif not (200 <= s < 400):
            unk.append((g, k, n, b, u, s))
    return dead, unk, len({t for *_, t in items})


if __name__ == '__main__':
    P = sys.argv[1]
    P = P if P.endswith('.html') else os.path.join(P, 'index.html')
    h = open(P).read()
    i = h.index('const D=') + 8
    D, _ = json.JSONDecoder().raw_decode(h, i)
    dead, unk, n = check(D)
    print(f'checked {n} pages: dead {len(dead)}, unknown {len(unk)}')
    for x in dead:
        print('  DEAD', x[5], x[0], x[3], '|', x[2], '|', x[1])
    for x in unk:
        print('  ?', x[5], x[0], x[3], '|', x[2], '|', x[4])
    sys.exit(1 if dead else 0)
