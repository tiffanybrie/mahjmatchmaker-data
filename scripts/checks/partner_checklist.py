#!/usr/bin/env python3
"""PARTNER CHECKLIST (Tiffany Nov 10 10:33pm): every partner brand, every loop closed, and no new affiliate falls off.
"we add a new affiliate... forgot that we added them, and they're left out of everything. And they're probably the people
paying attention the most because they're brand new to us."

THE PARTNER LIST = the live /mahjong-discount-codes page (what we tell the world) + config/partners-pipeline.json
(approved / onboarding brands not on the page yet). A brand in either list gets every row checked:
  page      brand guide page on the site (schema ItemList url)
  routes    config/link-routes.json entry (how its links get paid)
  newsl     docs/PARTNER-NEWSLETTERS.md status (seen / confirmed / signed up = ok; FAILED / missing = gap)
  ig        verified handle in config/social/ig-handles.json
  fav       handle listed as favorited in docs/IG-FAVORITES.md
  store     store in the partner watch's store snapshot (config/partner-products-snapshot.json) = new products get caught
Usage: partner_checklist.py [--html codes.html] [--csv out.csv] [--json out.json] [--quiet]
Exit 1 = gaps (front door prints them). Fetches the live codes page with curl unless --html is given."""
import json, re, sys, os, html, subprocess, unicodedata, csv
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
a = sys.argv; arg = lambda k: a[a.index(k) + 1] if k in a else None
norm = lambda t: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower().replace('&', 'and').replace('mahjong', 'mj').replace('the', ''))
src = open(arg('--html')).read() if arg('--html') else subprocess.run(['curl', '-s', '--max-time', '20', 'https://www.mahjmatchmaker.com/mahjong-discount-codes'], capture_output=True, text=True).stdout
m = re.search(r'"@type": "ItemList".*?"itemListElement": (\[.*?\])\}', src, re.S)
live = [] if not m else [(x['name'].split(':')[0].strip(), x['url']) for x in json.loads(html.unescape(m.group(1)))]
pipe_p = R + 'config/partners-pipeline.json'
pipe = json.load(open(pipe_p))['brands'] if os.path.exists(pipe_p) else []
routes = json.load(open(R + 'config/link-routes.json'))['brands']
ig = {k: v for k, v in json.load(open(R + 'config/social/ig-handles.json')).items() if not k.startswith('_')}
favtxt = open(R + 'docs/IG-FAVORITES.md').read()
nl = {}
for line in open(R + 'docs/PARTNER-NEWSLETTERS.md'):
    c = [x.strip() for x in line.strip().strip('|').split('|')]
    if len(c) == 3 and c[0] not in ('Brand', '---'): nl[norm(c[0])] = (c[0], c[1], c[2])
snap = json.load(open(R + 'config/partner-products-snapshot.json'))
snaphosts = {h.replace('www.', '') for h in snap}
ALIAS = {norm('Mah Jongg Maven'): norm('MahjjMaven')}
def find(d, b):
    k = norm(b)
    if d is routes: k = ALIAS.get(k, k)
    for kk in d:
        n = norm(kk) if not isinstance(d, dict) or kk not in nl else kk
        if n and (n == k or n.startswith(k) or k.startswith(n)): return kk
    return None
rows = []
names = [(b, u, 'live', '') for b, u in live] + [(p['brand'], p.get('page', ''), p.get('stage', 'pipeline'), p.get('store', '')) for p in pipe if not any(norm(p['brand']) == norm(b) for b, _ in live)]
for b, url, stage, pstore in names:
    r = {'brand': b, 'stage': stage}
    rk = find(routes, b); rt = routes.get(rk, {}) if rk else {}
    r['page'] = 'ok' if 'mahjmatchmaker.com/' in (url or '') else ('n/a (no page by design)' if b == 'Maison Mahj' else 'MISSING')
    r['routes'] = rt.get('route', 'MISSING')
    nk = next((k for k in nl if k == norm(b) or (len(k) > 3 and (k.startswith(norm(b)) or norm(b).startswith(k)))), None)
    st = nl[nk][2] if nk else 'MISSING (not in list)'
    r['newsletter'] = st
    r['newsletter_ok'] = bool(re.match(r'(seen|confirmed|signed up)', st, re.I))
    ik = find(ig, b); h = ig.get(ik) if ik else None
    r['ig'] = '@' + h if h else 'MISSING'
    r['favorited'] = 'yes' if h and re.search(r'\b' + re.escape(h) + r'\b', favtxt.split('## Handle verified')[0]) else ('no handle' if not h else 'NO')
    hosts = {x.replace('www.', '') for x in rt.get('store_hosts', [])} | ({pstore.replace('www.', '')} if pstore else set())
    r['store_watched'] = 'yes' if hosts & snaphosts else ('MISSING' if hosts - {''} else 'no store host')
    gaps = [k for k in ('page', 'routes', 'ig', 'store_watched') if str(r[k]).startswith('MISSING')]
    if not r['newsletter_ok']: gaps.append('newsletter')
    if r['favorited'] == 'NO': gaps.append('favorite')
    r['gaps'] = gaps; rows.append(r)
if arg('--json'): json.dump(rows, open(arg('--json'), 'w'), indent=1, ensure_ascii=False)
if arg('--csv'):
    with open(arg('--csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['Brand', 'Stage', 'Brand page', 'Link route', 'Newsletter', 'Instagram', 'Favorited', 'New products watched', 'Gaps'])
        for r in rows: w.writerow([r['brand'], r['stage'], r['page'], r['routes'], r['newsletter'], r['ig'], r['favorited'], r['store_watched'], ', '.join(r['gaps']) or 'none'])
g = [r for r in rows if r['gaps']]
if not live: print('PARTNER CHECKLIST: could not read the live codes page'); sys.exit(1)
if '--front' not in a and ('--quiet' not in a or g):
    print(f'PARTNER CHECKLIST: {len(rows)} partners ({len(live)} live, {len(rows) - len(live)} onboarding), {len(g)} with gaps')
    if '--quiet' not in a:
        for r in g: print(f"  {r['brand']}: {', '.join(r['gaps'])}")
if '--front' in a:  # front door: only brand-NEW partners (pipeline) with gaps, so a new affiliate can't fall off
    for r in rows:
        if r['stage'] != 'live' and r['gaps']: print(f"NEW PARTNER NOT FULLY ONBOARDED: {r['brand']} ({r['stage']}): missing {', '.join(r['gaps'])}. Do the missing steps now (CLAUDE.md partner onboarding; checklist sheet).")
    sys.exit(0)
sys.exit(1 if g else 0)
