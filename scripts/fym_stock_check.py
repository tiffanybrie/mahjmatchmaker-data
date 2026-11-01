"""FYM stock check (Tiffany Nov 1 12:04am: 'In stock only' filter). Checks every visible FYM mat / rack / tile product on its
brand's Shopify store (/products/<handle>.js -> available; a ?variant= in the link checks that variant) and writes
config/fym-stock.json {"checked": "YYYY-MM-DD", "items": {"m:<id>"|"r:<id>"|"t:<tile>": {"in": true|false, "how": ...}}}.
ShopMy / Etsy / Amazon / non-Shopify links and any lookup error = unknown -> treated as IN stock (never hide on a guess).
Retired items (rt) are always out of stock. Polite: one request at a time per store, 0.4 s apart, 8 stores in parallel.
Usage: python3 scripts/fym_stock_check.py <build dir> [--out config/fym-stock.json]"""
import sys, os, json, re, time, datetime, threading, urllib.request, urllib.parse, collections
from concurrent.futures import ThreadPoolExecutor
B = sys.argv[1]; OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'fym-stock.json')
h = open(B + '/index.html').read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
UA = {'User-Agent': 'Mozilla/5.0 (compatible; MahjMatchmakerStockCheck/1.0; +https://www.mahjmatchmaker.com)'}
def target(u):
    """-> (host, handle, variant) for a Shopify product link (direct or via /discount/CODE?redirect=), else None"""
    if not u or re.search(r'shopmy|etsy\.com|amazon\.|amzn\.', u, re.I): return None
    p = urllib.parse.urlparse(u); q = urllib.parse.parse_qs(p.query); path = p.path
    if 'redirect' in q: r = urllib.parse.urlparse(q['redirect'][0]); path = r.path; q = urllib.parse.parse_qs(r.query)
    m = re.search(r'/products/([^/?#]+)', path)
    if not m: return None
    return p.netloc, m.group(1), (q.get('variant') or [None])[0]
items = {}
for kind, coll in (('m', D['mats']), ('r', D['racks'])):
    for k, o in coll.items():
        if o.get('hid'): continue
        items[f'{kind}:{k}'] = o
vis_tiles = {s['tile'] for s in D['sets']}
for k, o in D['tiles'].items():
    if k in vis_tiles: items[f't:{k}'] = o
res, jobs = {}, collections.defaultdict(list)
for key, o in items.items():
    if o.get('rt'): res[key] = {'in': False, 'how': 'retired'}; continue
    t = target(o.get('u') or o.get('u0') or '')
    if not t: res[key] = {'in': True, 'how': 'unknown (not a Shopify product link)'}; continue
    jobs[t[0]].append((key, t))
cache = {}
def run_host(host):
    for key, (hst, handle, variant) in jobs[host]:
        j = cache.get((hst, handle))
        if j is None:
            try:
                rq = urllib.request.Request(f'https://{hst}/products/{handle}.js', headers=UA)
                j = json.loads(urllib.request.urlopen(rq, timeout=20).read())
            except Exception as e:
                j = {'_err': str(e)[:80]}
            cache[(hst, handle)] = j; time.sleep(0.4)
        if '_err' in j: res[key] = {'in': True, 'how': 'unknown (' + j['_err'] + ')'}; continue
        if variant:
            v = [x for x in j.get('variants', []) if str(x.get('id')) == str(variant)]
            if v: res[key] = {'in': bool(v[0].get('available')), 'how': 'shopify variant'}; continue
        res[key] = {'in': bool(j.get('available')), 'how': 'shopify product'}
        if not res[key]['in'] and re.search(r'arriving|pre-?order|coming-soon', handle + ' ' + j.get('title', ''), re.I): res[key] = {'in': True, 'how': 'preorder (store says unavailable, link says arriving / pre-order)'}
with ThreadPoolExecutor(8) as ex: list(ex.map(run_host, list(jobs)))
out = {'_about': __doc__.split('\n')[0], 'checked': datetime.date.today().isoformat(), 'items': dict(sorted(res.items()))}
json.dump(out, open(OUT, 'w'), indent=0, ensure_ascii=False)
c = collections.Counter(('in' if v['in'] else 'OUT') + ' / ' + v['how'].split(' (')[0] for v in res.values())
print('stock check', out['checked'], len(res), 'items:', dict(c))
