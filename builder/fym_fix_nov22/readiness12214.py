"""FYM 1.22.14 (Nov 22 2026, spare-usage run): close ALL-OR-NOTHING gaps without adding items.
 - mat prices from config/fym-prep-nov22/prices/prices.json (status priced): D.tv.pm[key] = [price, price after code, has %]
   brands that already carry a 10% pair in pm keep it; every other brand gets [p, p, 0] (no discount claimed).
 - tile-set walls from config/fym-prep-nov22/walls/walls.json: D.tv.backs[slug] = {'b': hex} (26 sets; back seen and checked by eye).
Usage: python3 readiness12214.py <build_dir>"""
import sys, json, os, collections
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
B = sys.argv[1]; p = os.path.join(B, 'index.html'); h = open(p).read()
i = h.index('const D=') + 8; D, n = json.JSONDecoder().raw_decode(h[i:]); end = i + n
TV = D['tv']; M = D['mats']
pct = collections.defaultdict(set)
for k, v in TV['pm'].items():
    if k in M and v[0]: pct[M[k]['bn']].add((round(v[1] / v[0], 2), v[2]))
P = json.load(open(REPO + '/config/fym-prep-nov22/prices/prices.json')); np_ = 0
for k, v in P.items():
    if v['status'] != 'priced' or not v.get('price') or k not in M or k in TV['pm']: continue
    r = pct.get(M[k]['bn'])
    ratio, flag = (list(r)[0] if r and len(r) == 1 else (1.0, 0))
    TV['pm'][k] = [float(v['price']), round(float(v['price']) * ratio, 2), flag]; np_ += 1
W = json.load(open(REPO + '/config/fym-prep-nov22/walls/walls.json')); slugs = {s['slug'] for s in D['sets']}; nw = 0
for s, v in W.items():
    if s in slugs and s not in TV['backs']: TV['backs'][s] = {'b': v['back']}; nw += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
assert h.count('1.22.13') == 2; h = h.replace('1.22.13', '1.22.14'); open(p, 'w').write(h)
print('prices added', np_, '| walls added', nw)
