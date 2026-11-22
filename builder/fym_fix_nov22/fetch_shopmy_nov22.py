"""Nov 22 daily ShopMy check: fetch brand product JSON + all image URLs for the 54 'missing' pins (config/shopmy-crosscheck-2026-11-22.json).
Writes assets/qa/shopmy-nov22/products.json (title, type, status, image urls) and downloads image #0..#2 per product as raw sources.
404 on the product JSON = dead pin. Usage: python3 builder/fym_fix_nov22/fetch_shopmy_nov22.py"""
import os, re, json, urllib.request, urllib.error
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
QA = REPO + 'assets/qa/shopmy-nov22/'; RAW = QA + 'raw/'; os.makedirs(RAW, exist_ok=True)
rep = json.load(open(REPO + 'config/shopmy-crosscheck-2026-11-22.json'))
out = {}
for m in rep['mats']:
    if m['status'] != 'missing': continue
    u = m['product_url']; mm = re.match(r'https?://([^/]+)/products/([^/?#]+)', u)
    r = {'pin': m['pin_id'], 'name': m['name'], 'url': u}
    try:
        req = urllib.request.Request(f'https://{mm.group(1)}/products/{mm.group(2)}.json', headers={'User-Agent': 'Mozilla/5.0'})
        p = json.load(urllib.request.urlopen(req, timeout=60))['product']
        r.update(title=p['title'], ptype=p.get('product_type'), tags=p.get('tags'), imgs=[i['src'] for i in p['images']], alts=[i.get('alt') for i in p['images']])
        for k, s in enumerate(r['imgs'][:3]):
            fn = f"{m['pin_id']}_{k}.jpg"
            if not os.path.exists(RAW + fn):
                open(RAW + fn, 'wb').write(urllib.request.urlopen(urllib.request.Request(s + ('&' if '?' in s else '?') + 'width=1400', headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read())
    except urllib.error.HTTPError as e: r['err'] = e.code
    except Exception as e: r['err'] = str(e)[:80]
    out[str(m['pin_id'])] = r
json.dump(out, open(QA + 'products.json', 'w'), indent=1)
print(len(out), 'fetched;', sum(1 for r in out.values() if 'err' in r), 'errors')
for k, r in out.items():
    if 'err' in r: print('ERR', k, r['name'], r['err'])
