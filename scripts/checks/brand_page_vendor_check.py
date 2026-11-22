#!/usr/bin/env python3
"""Brand pages must never show another brand's product as the page brand's own (Tiffany Nov 21 9:55pm: Mahj Pit page showed
Tigre de Tartan mats as Mahj Pit products; cause: the page was built from the store's products.json, which includes
Shopify Collective items from other vendors). For every live *-discount-code page: each product link on a Shopify store is
fetched as <product>.json; FAIL when it is tagged 'Shopify Collective' (another brand's product); a different vendor name alone is listed under 'review' (often a factory or artist name).
usage: python3 scripts/checks/brand_page_vendor_check.py [--quiet]   (writes docs/status/brand-page-vendor-check.json)"""
import re, sys, json, time, urllib.request, collections, os
UA = {'User-Agent': 'Mozilla/5.0'}
def get(u):
    try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20).read().decode('utf8', 'ignore')
    except Exception as e: return None
sm = get('https://www.mahjmatchmaker.com/sitemap.xml') or ''
pages = sorted(set(re.findall(r'https://www\.mahjmatchmaker\.com/[a-z0-9-]*discount-code[a-z0-9-]*', sm)))
out = {'checked': time.strftime('%Y-%m-%d %H:%M'), 'fail': [], 'unread': [], 'pages': len(pages), 'products': 0}
for pg in pages:
    h = get(pg) or ''; b = h[h.find('<main'):h.find('</main>')]
    links = sorted(set(re.findall(r'href="(https://[^"/]+/products/[^"?#]+)', b)))
    rows = []
    for u in links:
        j = get(u + '.json'); time.sleep(0.3)
        if not j or not j.lstrip().startswith('{'): out['unread'].append([pg.rsplit('/', 1)[1], u]); continue
        try: p = json.loads(j)['product']
        except Exception: out['unread'].append([pg.rsplit('/', 1)[1], u]); continue
        rows.append((u, p.get('vendor') or '', p.get('tags') or '', p.get('title') or ''))
    out['products'] += len(rows)
    byhost = collections.defaultdict(list)
    for r in rows: byhost[r[0].split('/')[2]].append(r)
    for host, rs in byhost.items():
        main = collections.Counter(r[1] for r in rs).most_common(1)[0][0]
        for u, v, t, ti in rs:
            row = {'page': pg.rsplit('/', 1)[1], 'url': u, 'title': ti, 'vendor': v, 'store_vendor': main}
            if 'shopify collective' in str(t).lower(): out['fail'].append(row)   # another brand's product resold through Shopify Collective
            elif v != main and len(rs) > 2: out.setdefault('review', []).append(row)   # vendor differs (often a factory name or an artist collab): look once, not a fail
os.makedirs('docs/status', exist_ok=True); json.dump(out, open('docs/status/brand-page-vendor-check.json', 'w'), indent=1)
print('BRAND PAGE VENDOR CHECK: %s (%d pages, %d products read, %d other-vendor products, %d unread)' % ('FAIL' if out['fail'] else 'PASS', out['pages'], out['products'], len(out['fail']), len(out['unread'])))
if '--quiet' not in sys.argv:
    for f in out['fail']: print('  ', f['page'], '|', f['title'], '| vendor', f['vendor'], '|', f['url'])
sys.exit(1 if out['fail'] else 0)
