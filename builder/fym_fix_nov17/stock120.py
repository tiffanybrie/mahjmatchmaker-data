"""FYM 1.20 stock refresh (Nov 17). Shop lookups can't run from the cloud container (the proxy refuses shop hosts), so the
Shopify /products/<handle>.js calls run in Tiffany's Chrome (same handles as builder/fym_fix_nov17/stock-jobs.json, made by
the same target() rule as scripts/fym_stock_check.py) and the raw answers are saved to a JSON file:
  {"<host>|<handle>": {"a": 0|1, "p": cents, "v": [[variant_id, 0|1, cents], ...]} | {"e": "<error>"}}
This script turns those answers into config/fym-stock.json (same format as scripts/fym_stock_check.py) and the sold-out
flags in the build: mats/racks .oos=1, tiles .so=1 + .oos=1; a flag is cleared when the store now says available.
Items the store can't answer for (ShopMy / Etsy / Amazon / non-Shopify / lookup error) stay as they were: an existing
sold-out flag is kept (written to the stock file as out, how='kept earlier sold-out flag') so gate [138] still matches.
Prices in D are NOT touched (tv118.py price lesson). The Nov 17 answers carry no prices, so the stock file keeps each item's Nov 1 price.
Usage: python3 stock120.py <build dir> <answers.json> [--date YYYY-MM-DD]"""
import sys, os, json, re, datetime, urllib.parse, collections
B, A = sys.argv[1], json.load(open(sys.argv[2]))
DAY = sys.argv[sys.argv.index('--date') + 1] if '--date' in sys.argv else datetime.date.today().isoformat()
R0 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
p = B + '/index.html'; h = open(p).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
def target(u):
    if not u or re.search(r'shopmy|etsy\.com|amazon\.|amzn\.', u, re.I): return None
    q0 = urllib.parse.urlparse(u); q = urllib.parse.parse_qs(q0.query); path = q0.path
    if 'redirect' in q: r = urllib.parse.urlparse(q['redirect'][0]); path = r.path; q = urllib.parse.parse_qs(r.query)
    m = re.search(r'/products/([^/?#]+)', path)
    return (q0.netloc, m.group(1), (q.get('variant') or [None])[0]) if m else None
items = {}
for kind, coll in (('m', D['mats']), ('r', D['racks'])):
    for k, o in coll.items():
        if not o.get('hid'): items[f'{kind}:{k}'] = o
vis = {s['tile'] for s in D['sets']}
for k, o in D['tiles'].items():
    if k in vis: items[f't:{k}'] = o
OLD = json.load(open(os.path.join(R0, 'config/fym-stock.json')))['items']
res, log = {}, collections.Counter(); changes = []
for key, o in items.items():
    was = bool(o.get('oos'))
    if o.get('rt'): res[key] = {'in': False, 'how': 'retired'}; continue
    t = target(o.get('u') or o.get('u0') or '')
    j = A.get(f'{t[0]}|{t[1]}') if t else None
    if not t or j is None or 'e' in j:
        why = 'not a Shopify product link' if not t else ('not checked' if j is None else j['e'])
        res[key] = {'in': not was, 'how': ('kept earlier sold-out flag' if was else 'unknown') + f' ({why})'}; log['unknown' + (' kept out' if was else '')] += 1; continue
    r = None
    if t[2]:
        v = [x for x in j.get('v', []) if str(x[0]) == str(t[2])]
        if v: r = {'in': bool(v[0][1]), 'how': 'shopify variant'}; pr = v[0][2]
    if r is None: r = {'in': bool(j.get('a')), 'how': 'shopify product'}; pr = j.get('p')
    if isinstance(pr, (int, float)): r['price'] = round(pr / 100, 2)
    elif 'price' in OLD.get(key, {}): r['price'] = OLD[key]['price']  # answers carried no price: keep the Nov 1 one
    if not r['in'] and re.search(r'arriving|pre-?order|coming-soon', t[1] + ' ' + (j.get('t') or ''), re.I): r = {'in': True, 'how': 'preorder (store says unavailable, link says arriving / pre-order)'}
    res[key] = r; kd = key[0]
    if not r['in'] and not was:
        o['oos'] = 1
        if kd == 't': o['so'] = 1
        changes.append(('now sold out', key, o.get('n'), o.get('bn') or o.get('b'))); log['set sold out'] += 1
    elif r['in'] and (was or (kd == 't' and o.get('so') == 1)):
        o.pop('oos', None)
        if kd == 't' and o.get('so') == 1: o.pop('so', None)
        changes.append(('back in stock', key, o.get('n'), o.get('bn') or o.get('b'))); log['cleared'] += 1
    else: log['same'] += 1
d = datetime.date.fromisoformat(DAY); D['stk'] = d.strftime('%b ') + str(d.day)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]; open(p, 'w').write(h)
out = {'_about': 'FYM stock check (In stock only filter). Nov 17: answers fetched in her Chrome, applied by builder/fym_fix_nov17/stock120.py.',
       'checked': DAY, 'items': dict(sorted(res.items()))}
json.dump(out, open(os.path.join(R0, 'config/fym-stock.json'), 'w'), indent=0, ensure_ascii=False)
print('stock120', DAY, dict(log), 'D.stk =', D['stk'])
for c in sorted(changes): print(' ', c[0], '|', c[3], '|', c[2], '|', c[1])
