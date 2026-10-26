"""FYM v95: Mahj & Moon mats -> her ShopMy links (Tiffany Oct 26 11:04am, docs/ANSWERS.md: Mahj & Moon sells on Etsy
(MahjandMoonCo); ShopMy collection 'Mahj & Moon' holds her matched mats; FYM uses those go.shopmy.us links with no code).
Spec: config/mahj-moon-shopmy-links.json {fym_key: {etsy_url, shopmy_url, name, site_url}} ('_' keys = metadata).
For every mapped mat with a go.shopmy.us shopmy_url: u (and u0 if present) = the ShopMy link; no code claim, same as the
other ShopMy-linked mats (v95_etsy.py, Tala): dc '', pa False, nc False. Gate [9] then allows it as ShopMy-affiliated and
gate [10] checks it claims no code. Mats with shopmy_url null (not made yet / not on Etsy) are left as they are.
Idempotent. Usage: python3 v95_mahjmoon.py <build_dir>"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
SHOPMY = 'https://go.shopmy.us/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M = D['mats']
SPEC = {k: v for k, v in json.load(open(REPO + 'config/mahj-moon-shopmy-links.json')).items() if not k.startswith('_')}
changed, done, pending, missing = [], [], [], []
for key, x in SPEC.items():
    if key not in M: missing.append(key); continue
    o = M[key]
    if o.get('bn') != 'Mahj & Moon': raise SystemExit(f'{key}: brand is {o.get("bn")!r}, not Mahj & Moon')
    url = x.get('shopmy_url')
    if not url: pending.append(o['n'] + ' (' + key + ')'); continue
    assert url.startswith(SHOPMY), (key, url)
    new = dict(u=url, dc='', pa=False, nc=False)
    if 'u0' in o: new['u0'] = url
    if any(o.get(f) != v for f, v in new.items()):
        o.update(new); changed.append(key)
    done.append(key)
if changed:
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
    open(P, 'w').write(h)
print('linked', len(done), 'changed now', len(changed), 'pending (no ShopMy link yet)', len(pending), 'missing from build', len(missing))
for p in pending: print('  pending:', p)
for m in missing: print('  missing:', m)
