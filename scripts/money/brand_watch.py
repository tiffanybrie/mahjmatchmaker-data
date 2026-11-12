#!/usr/bin/env python3
"""Brand revenue watch (Tiffany Nov 4 2026: "you've got to look at brands' sales performance
as well - that CANNOT be ignored"). Reads HQ money docs exported with
ArtifactData list collection=money out_dir=<dir>, prints per-brand and total flags.
Usage: python3 scripts/money/brand_watch.py <dir-with-money/*.json> [--date YYYY-MM-DD] [--json out.json]
Rules live in docs/REVENUE-WATCH.md."""
import json, glob, os, sys, collections, datetime as dt, argparse

ALIAS = {  # one name per brand (money docs use several spellings)
    'middle and main mahjong': 'Middle & Main', 'middle & main': 'Middle & Main', 'middle and main': 'Middle & Main',
    'middle & main mahjong': 'Middle & Main',
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
        k = norm(b['brand']); agg[k][0] += b.get('orders') or 0; c_ = b.get('commission'); agg[k][1] += c_ if isinstance(c_, (int, float)) else 0  # '?' = amount unknown (Nov 8 rule): counts as an order, $0 until her screenshot
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
# DAY ALARM (added Nov 12 2026: Mon Nov 9 closed at $94 / 7 orders vs $224 / 12 the Monday before and nothing fired,
# because REVENUE-WATCH.md promised a "<60% of the same weekday last week" alarm that was never coded, and the day
# sat 'partial' with '?' amounts). Checks the end day by ORDERS as well as dollars, so unknown amounts can't hide it.
HOL = {'2026-10-31', '2026-11-26', '2026-12-24', '2026-12-25', '2026-12-31', '2027-01-01'}
unk = {}
for f in files:
    d = os.path.basename(f)[:-5]
    if d in day: unk[d] = sum(1 for b in json.load(open(f)).get('brands', []) if not isinstance(b.get('commission'), (int, float)))
def dayflags(e):
    fl = []
    if e.isoformat() in HOL: return fl
    ref = e - dt.timedelta(7)
    if ref.isoformat() in HOL: ref = e - dt.timedelta(14)
    o, c = sumd([e.isoformat()]); ro, rc = sumd([ref.isoformat()])
    if ro >= 5 and o < 0.6 * ro: fl.append(f'{e.strftime("%a %b %-d")}: {o} orders vs {ro} on {ref.strftime("%a %b %-d")} ({round(100*o/ro)}%)')
    if rc >= 100 and c < 0.6 * rc and not unk.get(e.isoformat()): fl.append(f'{e.strftime("%a %b %-d")}: ${c:.0f} vs ${rc:.0f} on {ref.strftime("%a %b %-d")} ({round(100*c/rc)}%)')
    elif rc >= 100 and c < 0.6 * rc: fl.append(f'{e.strftime("%a %b %-d")}: ${c:.0f} known so far (+{unk[e.isoformat()]} orders with no amount yet) vs ${rc:.0f} on {ref.strftime("%a %b %-d")}: likely a low day, check now')
    return fl
day_flags = dayflags(end)
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
for t in day_flags: print('DAY ALARM:', t)
for f in sorted(out['flags'], key=lambda f: -next(x['base28_weekly'][1] for x in out['brands'] if x['brand'] == f['brand'])):
    print('BRAND ALARM:', f['brand'], '·', '; '.join(f['why']))
out['totalFlags'] = tot_flags; out['dayFlags'] = day_flags
if a.json: json.dump(out, open(a.json, 'w'), indent=1)
