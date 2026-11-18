#!/usr/bin/env python3
"""NON-SHOPIFY PARTNER STORE WATCH (Tiffany Nov 11 3:04pm). Reads config/non-shopify-partners.json and pulls each store's
products by its own method into config/partner-products-snapshot.json (same shape the Shopify watch writes: title, kind,
created, avail, min price, img), so partner_coverage.py and the partner watch see their inventory like any other partner.
Methods: woo (WooCommerce Store API), squarespace (<collection>?format=json), chrome (no automatic read: the run must open
the shop in Chrome). Prints NEW products (not in the snapshot before) and every store it could NOT read; a store it can't
read is a gap for that run to close in Chrome the same day, never "not watched".
Usage: nonshopify_watch.py [--no-save]"""
import json, os, re, subprocess, sys, html, datetime
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
CFG = json.load(open(R + 'config/non-shopify-partners.json'))['stores']
SNAP_P = R + 'config/partner-products-snapshot.json'; SNAP = json.load(open(SNAP_P))
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
get = lambda u: subprocess.run(['curl', '-sL', '--max-time', '25', '-A', UA, u], capture_output=True, text=True).stdout
def kind(t):
    t = t.lower()
    if re.search(r'tote|case|bag|carryall|cards|card\b|pouch|shirt|ornament|gift|dice|pusher only', t): return 'other'
    if re.search(r'\btile', t) or re.search(r'mah ?jongg? set\b', t): return 'tiles'
    if re.search(r'\bmat\b|table ?cover|tablecloth', t): return 'mat'
    if re.search(r'rack|pusher', t): return 'rack'
    return 'other'
new, failed = [], []
for host, c in CFG.items():
    items = {}
    try:
        if c['method'] == 'woo':
            for page in range(1, 20):
                d = json.loads(get(c['api'].format(page=page)) or '[]')
                if not d: break
                for p in d:
                    t = html.unescape(p['name']); pr = p.get('prices') or {}
                    mn = int(pr.get('price') or 0) / (10 ** int(pr.get('currency_minor_unit') or 2)) if pr.get('price') else None
                    items[p['slug']] = {'title': t, 'kind': kind(t), 'avail': bool(p.get('is_in_stock')), 'min': mn,
                                        'img': (p.get('images') or [{}])[0].get('src'), 'url': p.get('permalink')}
                if len(d) < 100: break
        elif c['method'] == 'squarespace':
            for col in c.get('collections', []):
                txt = get(f'https://www.{host}{col}?format=json')
                d = json.loads(txt)
                for p in d.get('items', []):
                    t = p.get('title', ''); v = (p.get('variants') or [{}])[0]
                    items[p.get('urlId')] = {'title': t, 'kind': kind(t), 'avail': (v.get('qtyInStock') or 0) > 0 or v.get('unlimited', False),
                                             'min': (v.get('priceMoney') or {}).get('value') and float(v['priceMoney']['value']), 'img': p.get('assetUrl'),
                                             'url': f"https://www.{host}{p.get('fullUrl', '')}"}
        else:
            raise RuntimeError('no automatic method: open the shop in Chrome')
        if not items: raise RuntimeError('read 0 products')
    except Exception as e:
        failed.append(f"{c['brand']} ({host}, {c['platform']}): {str(e)[:80]}"); continue
    old = SNAP.get(host, {})
    for h, it in items.items():
        if h not in old: new.append(f"{c['brand']}: {it['title']} ({it['kind']}) {it.get('url', '')}")
    SNAP[host] = items
if '--no-save' not in sys.argv: json.dump(SNAP, open(SNAP_P, 'w'), ensure_ascii=False, separators=(',', ':'))
print(f'NON-SHOPIFY WATCH {datetime.datetime.now():%b %d %H:%M}: {len(CFG) - len(failed)} of {len(CFG)} stores read; {len(new)} new products')
for n in new[:40]: print('  NEW', n)
for f in failed: print('  NOT READ (do it in Chrome today):', f)
