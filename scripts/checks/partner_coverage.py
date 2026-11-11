#!/usr/bin/env python3
"""PARTNER COVERAGE (Tiffany Nov 11 2:19-2:21pm: "There needs to be no gap between the things that we say are going to
happen and the things that actually happen").

Why it exists: Fait à Main (approved Oct 19) and Maison Mahj (code partner Oct 29) were each half set up. Every earlier
check looked at ONE list: the codes-page checklist only knew brands already on the codes page; FYM gate [114] only failed
a partner with ZERO items (Maison had 1 mat, so it passed with 0 of 6 tile sets); gate [100] only looked for missing MATS,
never tile sets. Nothing compared the lists against each other, so a brand could sit in one and be missing from the rest.

This script is the comparison. A brand is a PARTNER if it is in ANY of: config/code-truth.json, config/link-routes.json
(route code-site), config/fym-partner-coverage.json, config/partners-pipeline.json. For each one:
  codes_page  on the live /mahjong-discount-codes page (or excused in config/partner-coverage-excuse.json, reason + review date)
  fym_tiles   every full-size tile set in its store (config/partner-products-snapshot.json, kind tiles, >= $150) is in FYM
              (config/fym-items-index.json), or in config/fym-pending-queue.json (allowed 2 days), or on the sweep ignore list
  fym_mats    same for mats (kind mat)
Excuses expire: past review_by, the excuse stops counting and the gap shows again.
Usage: partner_coverage.py [--html codes.html] [--json out.json] [--front]
--front: one line per partner with a gap, for scripts/hooks/front_door.py (every message, every chat)."""
import json, re, os, sys, html, subprocess, unicodedata, datetime
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
a = sys.argv; arg = lambda k: a[a.index(k) + 1] if k in a else None
J = lambda p, d=None: json.load(open(R + p)) if os.path.exists(R + p) else d
norm = lambda t: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower().replace('&', 'and').replace('mahjong', 'mj').replace('the', ''))
today = datetime.date.today()

partners = {}  # norm -> {name, hosts, sources}
def add(name, src, hosts=()):
    k = norm(name); p = partners.setdefault(k, {'brand': name, 'hosts': set(), 'sources': []})
    p['sources'].append(src); p['hosts'] |= {h.replace('www.', '') for h in hosts if h}
ct = J('config/code-truth.json', {})
for b in ct.get('pct', {}):
    add(b, 'code-truth')
for b, v in J('config/link-routes.json')['brands'].items():
    if v.get('route') == 'code-site': add(b, 'link-routes', v.get('store_hosts', []))
for v in J('config/fym-partner-coverage.json', {'brands': []})['brands']:
    add(v['brand'], 'fym-coverage')
for v in J('config/partners-pipeline.json', {'brands': []})['brands']:
    add(v['brand'], 'pipeline', [v.get('store', '')])
for b, v in J('config/link-routes.json')['brands'].items():  # store hosts for partners whatever their link route
    if norm(b) in partners: partners[norm(b)]['hosts'] |= {h.replace('www.', '') for h in v.get('store_hosts', [])}

src = open(arg('--html')).read() if arg('--html') else subprocess.run(['curl', '-s', '--max-time', '20', 'https://www.mahjmatchmaker.com/mahjong-discount-codes'], capture_output=True, text=True).stdout
m = re.search(r'"@type": "ItemList".*?"itemListElement": (\[.*?\])\}', src, re.S)
live = set() if not m else {norm(x['name'].split(':')[0]) for x in json.loads(html.unescape(m.group(1)))}
page_txt = norm(re.sub(r'<[^>]+>', ' ', html.unescape(src)))

exc = {norm(k): v for k, v in J('config/partner-coverage-excuse.json', {'brands': {}})['brands'].items()}
def excused(k, row):
    e = exc.get(k, {}).get(row)
    if not e: return None
    if e.get('review_by') and datetime.date.fromisoformat(e['review_by']) < today: return None
    return e['reason']

snap = J('config/partner-products-snapshot.json', {})
idx = J('config/fym-items-index.json', {'mats': [], 'tiles': [], 'racks': []})
have = set(idx['mats']) | set(idx['tiles']) | set(idx['racks'])
tnorm = lambda t: norm(re.sub(r'^(in stock|odd lots[^-]*|pre-?order[^-]*)\s*-\s*', '', t, flags=re.I).split('|')[0].split(' - ')[0])
names = {}
for x in idx.get('names', []):
    b, n = x.split('|', 1); names.setdefault(norm(b), set()).add(tnorm(n))
pend = {}
for it in J('config/fym-pending-queue.json', {'items': []})['items']:
    mm = re.search(r'/products/([^/?#]+)', it.get('url', ''))
    if mm: pend[mm.group(1)] = it.get('added', '')
ign = {k.split('/')[-1] for k in J('config/partner-mat-sweep-ignore.json', {'items': {}})['items']}
ign |= {k.split('/')[-1] for k in J('config/partner-coverage-excuse.json', {'products': {}}).get('products', {})}
BAD = re.compile(r'travel|mini|solo|sample|gift card|e-?gift|bundle|replacement|single tile|blank|bag|case|pouch|sticker|preorder deposit|table ?cloth|table cover|tote|wall art|framed|kids|little mahj|odd lots|less than perfect|seconds|imperfect|rummi|rummy|special order - the \w+ table', re.I)

rows = []
for k, p in sorted(partners.items(), key=lambda x: x[1]['brand'].lower()):
    r = {'brand': p['brand'], 'sources': sorted(set(p['sources'])), 'gaps': []}
    on_page = k in live or any(k == x or (len(k) > 4 and (x.startswith(k) or k.startswith(x))) for x in live)
    r['codes_page'] = 'ok' if on_page else (('excused: ' + excused(k, 'codes_page')) if excused(k, 'codes_page') else 'MISSING')
    if r['codes_page'] == 'MISSING': r['gaps'].append('not on the codes page')
    hosts = [h for h in snap if h.replace('www.', '') in p['hosts']]
    for kind, label, floor in (('tiles', 'tile sets', 150), ('mat', 'mats', 40)):
        miss = []
        for h in hosts:
            for handle, it in snap[h].items():
                if it.get('kind') != kind or (it.get('min') or 0) < floor or BAD.search(it.get('title', '')): continue
                if handle in have or handle in ign: continue
                tn = tnorm(it.get('title', '')); bn = names.get(k, set())
                if tn and any(tn == x or (len(x) > 5 and (tn.startswith(x) or x.startswith(tn))) for x in bn): continue
                if handle in pend and (today - datetime.date.fromisoformat(pend[handle][:10])).days <= 2: continue
                miss.append(it['title'] + (' (queued since ' + pend[handle][:10] + ')' if handle in pend else ''))
        ex = excused(k, 'fym_' + kind)
        r['fym_' + kind] = ('excused: ' + ex) if (miss and ex) else (miss or 'ok')
        r['shop_' + kind] = r.get('shop_' + kind, 0) + sum(1 for h in hosts for it in snap[h].values() if it.get('kind') == kind and (it.get('min') or 0) >= floor and not BAD.search(it.get('title', '')))
        r['miss_' + kind] = miss
        if miss and not ex: r['gaps'].append(f'{len(miss)} {label} not in FYM: ' + '; '.join(miss[:6]) + (' …' if len(miss) > 6 else ''))
    if not hosts:
        r['store'] = 'store not read automatically (not Shopify, and no reader in config/non-shopify-partners.json yet)'
        if not excused(k, 'store'): r['gaps'].append('store not read automatically yet (not Shopify): check it in Chrome + its Instagram/emails today, and give it a reader in config/non-shopify-partners.json')
    rows.append(r)

if arg('--json'): json.dump(rows, open(arg('--json'), 'w'), indent=1, ensure_ascii=False)
if arg('--hq'):  # HQ 'Find Your Match' tab catalog card (hq/catalog): whole inventory, mats AND tile sets, every partner
    cnt = {}
    for x in idx.get('names', []): cnt[norm(x.split('|', 1)[0])] = cnt.get(norm(x.split('|', 1)[0]), 0) + 1
    hr = []
    for r in rows:
        mm, mt = r.get('miss_mat') or [], r.get('miss_tiles') or []
        mm = mm if isinstance(mm, list) else []; mt = mt if isinstance(mt, list) else []
        hr.append({'brand': r['brand'], 'app_mats': cnt.get(norm(r['brand'])), 'shop_mats': (r.get('shop_mat', 0) + r.get('shop_tiles', 0)) if r.get('store') is None else None,
                   'missing_mats': len(mm) + len(mt), 'missing_racks': 0, 'done': not r['gaps'] and not any(str(r.get(k, '')).startswith('excused') for k in ('codes_page', 'fym_tiles', 'fym_mat')),
                   'top': ['tile set: ' + t for t in mt] + mm + [g for g in r['gaps'] if not g[0].isdigit()]})
    hr.sort(key=lambda x: (x['done'], -x['missing_mats'], x['brand']))
    tot_t = sum(len(r.get('miss_tiles') or []) if isinstance(r.get('miss_tiles'), list) else 0 for r in rows)
    tot_m = sum(len(r.get('miss_mat') or []) if isinstance(r.get('miss_mat'), list) else 0 for r in rows)
    import datetime as _d
    json.dump({'headline': f"{sum(x['done'] for x in hr)} of {len(hr)} partners complete: whole store in the app + on the codes page",
               'sub': f"Missing right now: {tot_t} tile sets and {tot_m} mats across partner shops (counts are tile sets + mats; racks not counted yet). 'In app' = items in Find Your Mat-ch for that brand; 'In shop' = full-size tile sets + mats in their store snapshot.",
               'note': f"Checked {_d.datetime.now().strftime('%b %-d %-I:%M %p')} by scripts/checks/partner_coverage.py (live codes page + store snapshot vs the live app). A brand is complete only when nothing is missing; one mat in the app does not count. Stores we can't read automatically (not Shopify) show 'store not watched' and need a manual check.",
               'rows': hr, 'at': _d.datetime.now(_d.timezone.utc).isoformat()}, open(arg('--hq'), 'w'), ensure_ascii=False, indent=1)
g = [r for r in rows if r['gaps']]
if not live:
    print('PARTNER COVERAGE: could not read the live codes page'); sys.exit(1)
if '--front' in a:
    for r in g: print(f"PARTNER HALF SET UP: {r['brand']}: {' | '.join(r['gaps'])}. Fix now, or excuse it with a reason + review date in config/partner-coverage-excuse.json.")
    sys.exit(0)
print(f'PARTNER COVERAGE: {len(rows)} partners, {len(g)} half set up')
for r in g: print(f"  {r['brand']} ({', '.join(r['sources'])}): {' | '.join(r['gaps'])}")
sys.exit(1 if g else 0)
