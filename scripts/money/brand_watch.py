#!/usr/bin/env python3
"""Brand revenue watch (Tiffany Nov 4 2026: "you've got to look at brands' sales performance
as well - that CANNOT be ignored"). Reads HQ money docs exported with
ArtifactData list collection=money out_dir=<dir>, prints per-brand and total flags.
Usage: python3 scripts/money/brand_watch.py <dir-with-money/*.json> [--date YYYY-MM-DD] [--json out.json]
Rules live in docs/REVENUE-WATCH.md."""
import json, glob, os, sys, collections, datetime as dt, argparse

ALIAS = {  # one name per brand (money docs use several spellings)
    'middle and main mahjong': 'Middle & Main', 'middle & main': 'Middle & Main',
    'anders ruff design co.': 'Anders Ruff', 'anders ruff': 'Anders Ruff',
    'mac + miller': 'Mac + Miller', 'mac+miller mahjong': 'Mac + Miller',
    'amanda toppe': 'Amanda Toppe Living', 'amanda toppe living': 'Amanda Toppe Living',
    'virora': 'Virora Mahjong', 'virora mahjong': 'Virora Mahjong',
    'amahj line': 'Amahj', 'lets be besties': "Let's Be Besties",
}
def norm(n):
    n = n.split(' (')[0].strip()
    return ALIAS.get(n.lower(), n)

ap = argparse.ArgumentParser(); ap.add_argument('dir'); ap.add_argument('--date'); ap.add_argument('--json')
a = ap.parse_args()
files = glob.glob(os.path.join(a.dir, '**', '*.json'), recursive=True)
day = {}
for f in files:
    d = os.path.basename(f)[:-5]
    try: dt.date.fromisoformat(d)
    except ValueError: continue
    agg = collections.defaultdict(lambda: [0, 0.0])
    for b in json.load(open(f)).get('brands', []):
        if b['brand'].startswith('ShopMy: Ambassador'): continue
        k = norm(b['brand']); agg[k][0] += b.get('orders') or 0; agg[k][1] += b.get('commission') or 0
    day[d] = agg
end = dt.date.fromisoformat(a.date) if a.date else max(dt.date.fromisoformat(d) for d in day)  # last COMPLETE day
def rng(e, n): return [(e - dt.timedelta(i)).isoformat() for i in range(n)]
def sumd(ds, brand=None):
    o = c = 0
    for d in ds:
        for k, v in day.get(d, {}).items():
            if brand is None or k == brand: o += v[0]; c += v[1]
    return o, round(c, 2)
last7 = rng(end, 7); prev7 = rng(end - dt.timedelta(7), 7); base28 = rng(end - dt.timedelta(7), 28)
T7, P7, B28 = sumd(last7), sumd(prev7), sumd(base28)
peak = max((sumd(rng(dt.date.fromisoformat(d), 7))[1], d) for d in day if dt.date.fromisoformat(d) <= end)
out = {'end': end.isoformat(), 'total': {'last7': T7, 'prev7': P7, 'base28_weekly': (round(B28[0]/4, 1), round(B28[1]/4, 2)),
       'peak7': {'commission': peak[0], 'ending': peak[1]}}, 'flags': [], 'brands': []}
tot_flags = []
if P7[1] and T7[1] < 0.8 * P7[1]: tot_flags.append(f'7-day commission ${T7[1]} is {round(100*T7[1]/P7[1])}% of the week before (${P7[1]})')
if B28[1] and T7[1] < 0.8 * B28[1] / 4: tot_flags.append(f'7-day commission ${T7[1]} is {round(100*T7[1]/(B28[1]/4))}% of the 4-week weekly average (${round(B28[1]/4,2)})')
if peak[0] and T7[1] < 0.6 * peak[0]: tot_flags.append(f'7-day commission is {round(100*T7[1]/peak[0])}% of the best week (${peak[0]}, week ending {peak[1]})')
brands = sorted({k for d in day.values() for k in d})
for b in brands:
    o7, c7 = sumd(last7, b); op, cp = sumd(prev7, b); o28, c28 = sumd(base28, b)
    wk = o28 / 4
    lastd = max((d for d in day if day[d].get(b, [0])[0] > 0 and dt.date.fromisoformat(d) <= end), default=None)
    gap = (end - dt.date.fromisoformat(lastd)).days if lastd else None
    rate = o28 / 28  # orders/day baseline
    fl = []
    if wk >= 2 and o7 < 0.5 * wk: fl.append(f'orders {o7} this week vs {wk:.1f}/week baseline ({round(100*o7/wk)}%)')
    if op >= 3 and o7 < 0.5 * op: fl.append(f'orders {o7} vs {op} the week before')
    if rate >= 0.3 and gap is not None and gap >= max(3, round(2.5 / rate)): fl.append(f'no order for {gap} days (usually ~{1/rate:.1f} days apart)')
    if c28/4 >= 40 and c7 < 0.5 * c28/4: fl.append(f'commission ${c7:.0f} this week vs ${c28/4:.0f}/week baseline ({round(100*c7/(c28/4))}%)')
    if cp >= 60 and c7 < 0.5 * cp: fl.append(f'commission ${c7:.0f} vs ${cp:.0f} the week before')
    if fl: out['flags'].append({'brand': b, 'why': fl})
    out['brands'].append({'brand': b, 'last7': [o7, c7], 'prev7': [op, cp], 'base28_weekly': [round(wk, 1), round(c28/4, 2)], 'lastOrder': lastd, 'daysSince': gap})
print(f"BRAND WATCH through {out['end']}: last 7 days {T7[0]} orders / ${T7[1]} · week before {P7[0]} / ${P7[1]} · 4-week weekly avg {out['total']['base28_weekly'][0]} / ${out['total']['base28_weekly'][1]} · best week ${peak[0]} (ending {peak[1]})")
for t in tot_flags: print('TOTAL ALARM:', t)
for f in sorted(out['flags'], key=lambda f: -next(x['base28_weekly'][1] for x in out['brands'] if x['brand'] == f['brand'])):
    print('BRAND ALARM:', f['brand'], '·', '; '.join(f['why']))
out['totalFlags'] = tot_flags
if a.json: json.dump(out, open(a.json, 'w'), indent=1)
