"""Dead shop link that is LIVE AGAIN gets its shop button back (FYM 1.18, Nov 7 2026; gap audit A7: OMM Pearlescent came back on
Nov 7 at $475, 40 of Tiffany's matches, but FYM v117 kept it `u_dead` with no shop button: deadlinks116.py only ever blanks links).

RULE: an item listed in config/fym-dead-links.json whose store product answers 200 with at least one AVAILABLE variant
(Shopify /products/<handle>.json) is revived:
  build:  u = u_dead (the old auto-apply link), u_dead dropped, Sold out flag (oos) dropped;
  repo:   the item moves from config/fym-dead-links.json 'items' to 'revived' (date + price), so deadlinks116.py no longer blanks it;
          config/fym-stock.json '<g>:<key>' = in stock + store price (the price filter / Table view read it).
Items whose store page is not Shopify, or answers 200 with every variant sold out, are only reported (never guessed).
The link check (builder/fym_fix_nov06/linkcheck.py `revivable()`, gate [162b]) reports any dead-link item that is live again.

Usage: python3 builder/fym_fix_nov07/revive_links.py <build dir>            (revive in the build + update the repo files)
       python3 builder/fym_fix_nov07/revive_links.py <build dir> --check    (report only; exit 1 if something should be revived)"""
import sys, os, json, re, subprocess, datetime
from urllib.parse import urlsplit, unquote
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
STK_KEY = {'mats': 'm:', 'tiles': 't:', 'racks': 'r:'}


def product_url(u):
    """Store product page behind a shop link (auto-apply /discount/CODE?redirect=/products/x -> https://host/products/x)."""
    u = (u or '').strip()
    if not u.startswith('http'): return None
    p = urlsplit(u)
    path = p.path
    if path.startswith('/discount/') and 'redirect=' in u:
        path = unquote(u.split('redirect=', 1)[1].split('&')[0]).split('?')[0]
    return f'https://{p.netloc}{path}'.rstrip('/')


def store_state(url):
    """-> (status, available, price) from Shopify <url>.json; status 0 = no answer."""
    try:
        r = subprocess.run(['curl', '-s', '-L', '-m', '25', '-A', UA, '-w', '\n%{http_code}', url + '.json'], capture_output=True, text=True, timeout=40)
        body, code = r.stdout.rsplit('\n', 1); code = int(code or 0)
    except Exception:
        return 0, None, None
    if code != 200: return code, None, None
    try: p = json.loads(body)['product']
    except Exception: return code, None, None  # not Shopify
    vs = p.get('variants') or []
    av = [v for v in vs if v.get('available', True) is not False]
    # products.json-style variants carry 'available'; <handle>.json may not: fall back to the .js endpoint for availability
    if vs and 'available' not in vs[0]:
        try:
            j = subprocess.run(['curl', '-s', '-L', '-m', '25', '-A', UA, url + '.js'], capture_output=True, text=True, timeout=40).stdout
            ids = {v['id'] for v in json.loads(j).get('variants', []) if v.get('available')}; av = [v for v in vs if v.get('id') in ids]
        except Exception: pass
    price = min((float(v['price']) for v in (av or vs) if v.get('price') not in (None, '')), default=None)  # .json prices are dollars
    return code, bool(av), price


def revivable(D, items):
    """-> list of (key, group, name, url, price) for dead-link items whose store product is live and available."""
    out, report = [], []
    for k, x in items.items():
        o = (D.get(x['g']) or {}).get(k)
        if not o: report.append((k, 'not in build')); continue
        url = product_url(o.get('u_dead') or o.get('u0') or o.get('u'))
        if not url: report.append((k, 'no store url')); continue
        code, av, price = store_state(url)
        if code == 200 and av: out.append((k, x['g'], o.get('n'), url, price))
        else: report.append((k, f'{code} available={av}'))
    return out, report


if __name__ == '__main__':
    B = sys.argv[1]; P = B if B.endswith('.html') else os.path.join(B, 'index.html')
    h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
    CFG = json.load(open(R + 'config/fym-dead-links.json'))
    live, rep = revivable(D, CFG['items'])
    for k, why in rep: print('  still dead/unknown:', k, why)
    if '--check' in sys.argv:
        for k, g, n, url, pr in live: print('  LIVE AGAIN (revive):', g, n, url, pr)
        sys.exit(1 if live else 0)
    STK = json.load(open(R + 'config/fym-stock.json')); today = datetime.date.today().isoformat()
    for k, g, n, url, pr in live:
        o = D[g][k]
        if o.get('u_dead'): o['u'] = o.pop('u_dead')
        elif not o.get('u'): o['u'] = o.get('u0') or url
        o.pop('oos', None)
        STK['items'][STK_KEY[g] + k] = {'in': True, 'how': f'shopify product (revive_links {today})', **({'price': pr} if pr else {})}
        x = CFG['items'].pop(k); CFG.setdefault('revived', {})[k] = dict(x, revived=today, url=url, price=pr)
        print('revived', g, n, url, pr)
    for k, x in (CFG.get('revived') or {}).items():  # revived on an earlier run (repo already updated): apply to this build too (idempotent)
        o = (D.get(x['g']) or {}).get(k)
        if o and o.get('u_dead'): o['u'] = o.pop('u_dead'); o.pop('oos', None); print('revived (earlier run)', x['g'], o.get('n'))
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]; open(P, 'w').write(h)
    if live:
        json.dump(CFG, open(R + 'config/fym-dead-links.json', 'w'), indent=1, ensure_ascii=False)
        json.dump(STK, open(R + 'config/fym-stock.json', 'w'), indent=0, ensure_ascii=False)
    print('revive_links: revived', len(live), 'of', len(live) + len(rep))
