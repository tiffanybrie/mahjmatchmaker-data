"""FYM 1.18: fill missing prices (gap audit B4) from config/fym-prices-nov07.json into D.tv of a build.
Only ADDS: an item that already has a price keeps it; hidden items and keys not in D are skipped.
Format is exactly preview_nov01.py's pz(): [store price, price after code, 1 if a partner code % applies else 0]
  mats -> D.tv.pm[mat key], tile sets -> D.tv.pt[tile key], racks -> D.tv.price[rack key];
  code % = config/fym-code-pct.json pct[brand name] for partner items (pa), as in the Table view build.
Then D.tv.pr (the price dropdown steps) is recomputed with preview_nov01.py's ranges() so the steps fit the fuller data.
RUN AFTER tv118.py (tv118 rebuilds pm / pt / price from config/fym-stock.json and would drop these). Idempotent.
Usage: python3 builder/fym_fix_nov07/prices_v118.py <build dir or index.html> [more ...]"""
import sys, os, json, pathlib
R = pathlib.Path(__file__).resolve().parents[2]
PR = {k: v for k, v in json.load(open(R / 'config/fym-prices-nov07.json')).items() if not k.startswith('_')}
PCT = json.load(open(R / 'config/fym-code-pct.json'))['pct']
fr = lambda x: int(round(x / 5) * 5) if x < 100 else (int(round(x / 25) * 25) if x < 300 else int(round(x / 50) * 50))
def ranges(vals):
    v = sorted(vals); return sorted(set(fr(v[int(len(v) * f)]) for f in (.2, .4, .6, .8))) if len(v) >= 8 else []
def triple(p, bn, pa):
    pc = PCT.get(bn) if pa else None; p = float(p)
    return [p, round(p * (1 - pc / 100), 2) if pc else p, int(bool(pc))]
for P in sys.argv[1:]:
    P = P if P.endswith('.html') else os.path.join(P, 'index.html')
    h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); TV = D['tv']
    tiles_vis = {s['tile'] for s in D['sets'] if not s.get('hid') and not D['tiles'].get(s['tile'], {}).get('hid')}
    add = {'m': 0, 't': 0, 'r': 0}
    for k, v in PR.items():
        c = v['c']
        if c == 'm':
            o = D['mats'].get(k)
            if o and not o.get('hid') and k not in TV['pm']: TV['pm'][k] = triple(v['p'], o.get('bn'), o.get('pa')); add['m'] += 1
        elif c == 't':
            o = D['tiles'].get(k)
            if o and k in tiles_vis and k not in TV['pt']:
                bn = o.get('bn') or next((s['maker'] for s in D['sets'] if s['tile'] == k), None)
                TV['pt'][k] = triple(v['p'], bn, o.get('pa')); add['t'] += 1
        elif c == 'r':
            o = D['racks'].get(k)
            if o and not o.get('hid') and k not in TV['price']: TV['price'][k] = triple(v['p'], o.get('bn'), o.get('pa')); add['r'] += 1
    old = TV.get('pr')
    TV['pr'] = {'mat': ranges([x[1] for x in TV['pm'].values()]), 'tiles': ranges([x[1] for x in TV['pt'].values()]),
                'racks': ranges([x[1] for x in TV['price'].values()])}
    if any(add.values()) or old != TV['pr']:
        h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]; open(P, 'w').write(h)
    vm = [k for k, m in D['mats'].items() if not m.get('hid')]; vr = [k for k, r in D['racks'].items() if not r.get('hid')]
    vs = [s for s in D['sets'] if not s.get('hid') and not D['tiles'].get(s['tile'], {}).get('hid')]
    print(f"prices_v118 {P}: added {add}; price steps {old} -> {TV['pr']}; coverage mats {sum(1 for k in vm if k in TV['pm'])}/{len(vm)}, "
          f"tile sets {sum(1 for s in vs if s['tile'] in TV['pt'])}/{len(vs)}, racks {sum(1 for k in vr if k in TV['price'])}/{len(vr)}")
