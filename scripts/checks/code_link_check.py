#!/usr/bin/env python3
"""CODE LINK CHECK (Tiffany Nov 11 4:15pm: products added before a brand is fully onboarded can end up with generic links,
"a huge miss for us, and one that would be hard for us to discover after the fact").

For every VISIBLE item in Find Your Mat-ch (mats, tiles, racks) whose brand is a code partner (config/link-routes.json route
code-site) on a store where the code CAN be put in the cart by link (config/autoapply-hosts.json `hosts`), the shop link
must carry the code: /discount/<CODE> (or the brand's affiliate ref, e.g. sca_ref / ref=). A plain product link means the
shopper lands with no code in the cart; they only get it if they type it in from our card.
Stores in autoapply `skip` (the code can't be applied by link) are allowed plain links.
Brands whose code is not confirmed yet (scripts/checks/partner_coverage.py code_ok) must have NO visible items at all.

Usage: code_link_check.py <FYM index.html | D.js> [--json out]   exit 1 on any miss (fym_gate [172b] calls it).
"""
import json, re, os, sys, subprocess
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
src = sys.argv[1]
if src.endswith('.js'):
    D = json.loads(subprocess.run(['node', '-e', f'process.stdout.write(JSON.stringify(require({json.dumps(os.path.abspath(src))})))'], capture_output=True, text=True).stdout)
else:
    h = open(src).read(); i = h.index('const D={') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
routes = json.load(open(R + 'config/link-routes.json'))['brands']
auto = json.load(open(R + 'config/autoapply-hosts.json'))
ok_hosts = {h.replace('www.', '') for h in auto.get('hosts', [])}
ct = json.load(open(R + 'config/code-truth.json'))
norm = lambda t: re.sub(r'[^a-z0-9]', '', t.lower()).replace('the', '')
confirmed = {norm(k) for k in ct.get('pct', {})} | {norm(k) for k, v in (ct.get('terms') or {}).items() if isinstance(v, dict) and str(v.get('status', '')).lower().startswith('confirmed')}
miss, held = {}, {}
for g in ('mats', 'tiles', 'racks'):
    for k, v in (D.get(g) or {}).items():
        if v.get('hid'): continue
        b = v.get('bn') or ''; rt = routes.get(b, {})
        if rt.get('route') != 'code-site': continue
        u = v.get('u') or ''
        if not u: continue
        host = re.sub(r'^https?://(www\.)?', '', u).split('/')[0]
        if not any(norm(b) == c or (len(c) > 5 and (c in norm(b) or norm(b) in c)) for c in confirmed):
            held.setdefault(b, []).append(v.get('n')); continue
        if host in ok_hosts and not re.search(r'/discount/|sca_ref|[?&]ref=|ref%3D|aff', u, re.I):
            miss.setdefault(b, []).append(v.get('n'))
if '--json' in sys.argv: json.dump({'plain': miss, 'held_visible': held}, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
n = sum(map(len, miss.values())); nh = sum(map(len, held.values()))
print(f"CODE LINK CHECK: {'PASS' if not n and not nh else 'FAIL'}: {n} visible items with a plain link where the code could be in the cart; {nh} visible items from brands with no confirmed code")
for b, xs in sorted(miss.items(), key=lambda x: -len(x[1])): print(f'  PLAIN {b}: {len(xs)} (e.g. {", ".join(map(str, xs[:3]))})')
for b, xs in held.items(): print(f'  NO CODE YET {b}: {len(xs)} visible (e.g. {", ".join(map(str, xs[:3]))})')
sys.exit(1 if n or nh else 0)
