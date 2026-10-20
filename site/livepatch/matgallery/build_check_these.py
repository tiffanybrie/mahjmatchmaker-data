"""v5 'check these' list for Tiffany (Oct 20): mats where Claude's measured dominant color disagrees with the current primary tag,
or where blue/teal/green or pink/purple is borderline. Skips anything she has already called. Worst first, capped at 40.
Usage: python3 build_check_these.py   (reads matgallery-v5.html, config/mat-accent-colors.json, overrides) -> v5_check_these.json"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); P = lambda *a: os.path.join(HERE, '..', '..', '..', *a)
t = open(os.path.join(HERE, 'matgallery-v5.html')).read()
R = json.loads(re.search(r'<script type="application/json">(.*?)</script>', t, re.S).group(1).replace('<\\/', '</'))
ACC = json.load(open(P('config/mat-accent-colors.json')))['mats']
man = json.load(open(os.path.join(HERE, 'manifest.json')))
OV = json.load(open(P('config/mat-color-overrides.json')))['mats']
V5 = json.load(open(P('config/tiffany-color-notes/2026-10-20-v5-calls.json')))
called = set(V5['final_sections']) | {m['img'] for m in V5['mood_calls']}
called |= {img for img, k in man.items() if str((OV.get(k) or {}).get('by', '')).startswith('tiffany')}
COLORS = ['pink', 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple']
LAB = {'pink': 'Pink', 'red': 'Red', 'orange': 'Orange & Peach', 'yellow': 'Yellow & Mustard', 'green': 'Green', 'teal': 'Teal & Aqua', 'blue': 'Blue', 'purple': 'Purple & Lilac'}
GROUPS = [{'blue', 'teal', 'green'}, {'pink', 'purple'}]
out = []
for x in R:
    img, name, brand, secs = x[0], x[1], x[2], x[5]
    if img in called or x[4] or secs == ['holiday']: continue
    prim = secs[0]
    if prim not in COLORS: continue
    sh = ACC.get(img, {}).get('shares', {})
    col = {c: sh.get(c, 0) for c in COLORS}
    dom = max(col, key=col.get)
    if col[dom] < 12: continue  # too little measured color to argue with
    p = col[prim]
    if dom != prim and col[dom] >= 1.6 * max(p, 1) and col[dom] - p >= 15:
        score = col[dom] - p + 100
        reason = f'measured {LAB[dom]} {col[dom]:.0f}% vs {LAB[prim]} {p:.0f}%: does the primary read right?'
    else:
        g = next((g for g in GROUPS if prim in g), None)
        if not g: continue
        rival = max((c for c in g if c != prim), key=lambda c: col[c])
        if col[rival] >= 12 and col[rival] >= 0.75 * max(p, 1) and rival not in secs:
            score = 50 - abs(col[rival] - p)
            reason = f'borderline {LAB[prim]} vs {LAB[rival]} (measured {p:.0f}% vs {col[rival]:.0f}%)'
            dom = rival if col[rival] > p else prim
        else:
            continue
    out.append(dict(img=img, name=name, brand=brand, current_primary=LAB[prim], current_tags=secs, measured_dominant=LAB[dom],
                    measured_pct={c: round(v) for c, v in col.items() if v >= 5}, reason=reason, _s=score))
out.sort(key=lambda d: -d['_s'])
for d in out: d.pop('_s')
json.dump({'by': 'claude-measured', 'date': '2026-10-20', 'about': __doc__.split('\n')[0] + ' Image: https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@<commit>/assets/mats/gallery/<img>.webp',
           'total_candidates': len(out), 'mats': out[:40]}, open(os.path.join(HERE, 'v5_check_these.json'), 'w'), indent=1, ensure_ascii=False)
print(len(out), 'candidates; saved', min(40, len(out)))
for d in out[:40]: print(d['brand'][:16], '|', d['name'][:30], '|', d['reason'])
