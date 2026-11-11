#!/usr/bin/env python3
"""FIND YOUR MAT-CH IS ALL OR NOTHING (Tiffany Nov 11 5:53pm).

"If anything comes into Find Your Match at all, it has to clear everything. It can't just clear the photo check."
Table view (Nov 1-7) was added on top of the original bring-everything-in process, so FYM risked splitting into two worlds:
items cleared "before Table view" and items cleared "after". She was once told "everything is ready for Table view" when only
~30 tile sets were. This check is the single list of what EVERY visible item must have, in EVERY view and filter:

  tile set : photo (src/full) | Table view walls (D.tv.backs[slug]) | price (D.tv.pt, price filter) | card colour (set.tc)
  mat      : Table view class (D.tv.cls; A/B shown, C grayed with a reason in D.tv.why) | price (D.tv.pm)
  rack     : Table view decision (D.tv.rt / D.tv.rk usable, or a reason in D.tv.rkw) | price (D.tv.price)
(Photo flags, colours, link routes and codes are already gated: [3] [45] [50] [56] [169] [172] [172b].)

A new dimension added to FYM later MUST be added here the same day, with a backfill for every item already in the app.

Writes config/fym-readiness.json (per-brand gaps, read by the front door and partner_coverage: a brand is not COVERED while any of
its visible items has a gap). Gaps that existed on Nov 11 are in config/fym-readiness-baseline.json and are OVERDUE work (the
front door shows the count until 0). The gate (fym_gate [173]) FAILS on any gap NOT in the baseline: a new item can't go
visible half-ready, and the baseline can only shrink.

Usage: fym_all_or_nothing.py <build dir | index.html> [--write-baseline]
"""
import sys, os, json, collections, pathlib
R = pathlib.Path(__file__).resolve().parents[2]
A = sys.argv[1]; P = A if A.endswith('.html') else os.path.join(A, 'index.html')
h = open(P).read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
TV = D.get('tv', {}); T = D['tiles']
gaps = []  # (kind, key, brand, name, missing)
for s in D['sets']:
    t = T.get(s['tile'], {})
    if s.get('hid') or t.get('hid'): continue
    miss = [m for m, ok in (('table-view walls', s['slug'] in TV.get('backs', {})), ('price', s['tile'] in TV.get('pt', {})),
                            ('card colour', bool(s.get('tc'))), ('photo', bool(t.get('src') or t.get('full'))))
            if not ok]
    if miss: gaps.append(('tile set', s['tile'], s.get('maker'), s.get('name'), miss))
for k, m in D['mats'].items():
    if m.get('hid'): continue
    miss = [x for x, ok in (('table-view class', k in TV.get('cls', {})), ('price', k in TV.get('pm', {}))) if not ok]
    if miss: gaps.append(('mat', k, m.get('bn'), m.get('n'), miss))
for k, r in D['racks'].items():
    if r.get('hid'): continue
    miss = [x for x, ok in (('table-view decision', k in TV.get('rt', {}) or k in TV.get('rk', {}) or k in TV.get('rkw', {})),
                            ('price', k in TV.get('price', {}))) if not ok]
    if miss: gaps.append(('rack', k, r.get('bn'), r.get('n'), miss))

key = lambda g: f"{g[0]}|{g[1]}|{','.join(g[4])}"
BP = R / 'config/fym-readiness-baseline.json'
if '--write-baseline' in sys.argv:
    json.dump({'_about': 'Gaps already live on Nov 11 2026 when the all-or-nothing rule started (Tiffany 5:53pm). OVERDUE work: clear them; this list may only shrink. scripts/checks/fym_all_or_nothing.py', 'gaps': sorted(key(g) for g in gaps)}, open(BP, 'w'), indent=1)
base = set(json.load(open(BP))['gaps']) if BP.exists() else set()
new = [g for g in gaps if key(g) not in base]
by = collections.defaultdict(lambda: collections.Counter())
for g in gaps:
    for m in g[4]: by[g[2] or '?'][f'{g[0]} {m}'] += 1
json.dump({'_about': 'Written by scripts/checks/fym_all_or_nothing.py on every FYM build. Per brand: visible items missing a view/filter.',
           'fym_version': D.get('ver') or '', 'total_gaps': len(gaps), 'new_gaps': len(new),
           'brands': {b: dict(c) for b, c in sorted(by.items())},
           'items': [{'kind': g[0], 'key': g[1], 'brand': g[2], 'name': g[3], 'missing': g[4]} for g in gaps]},
          open(R / 'config/fym-readiness.json', 'w'), indent=1, ensure_ascii=False)
tot = collections.Counter(f'{g[0]} {m}' for g in gaps for m in g[4])
print(f"FYM ALL-OR-NOTHING: {len(gaps)} visible items not ready in every view/filter ({', '.join(f'{v} {k}' for k, v in tot.most_common())}); {len(new)} NEW (not in the Nov 11 baseline)")
for b, c in sorted(by.items(), key=lambda x: -sum(x[1].values()))[:15]: print(f"  {b}: " + ', '.join(f'{v} {k}' for k, v in c.items()))
for g in new[:20]: print(f"  NEW {g[0]} {g[2]} | {g[3]}: missing {', '.join(g[4])}")
sys.exit(1 if new else 0)
