#!/usr/bin/env python3
"""Brand Watch auto-add (Tiffany Nov 23 11:11pm: "figure out why they weren't added already and then fix the misses step").
WHY THEY WERE MISSED: partner_launch_watch.py reads every partner store 3x a day, but only products that are NEW SINCE THE LAST RUN
(`events`) were acted on, and acting was a judgement step in the scheduled run. Anything that slipped once (a run that wrote only some
finds, a run that stopped, a store whose first read silently seeded the snapshot, like Spools + Brewtifully on Nov 18-19) became
'known' in the snapshot and was never offered again; it only sat in the ignored `recent` list. Nov 23: 6 brands' new mats/tiles
were in `recent` and not on the page.
THE FIX: this script runs at the end of every partner_launch_watch.py run and writes EVERY tile set / mat / rack published in the
last 10 days by a code partner into config/brand-watch-curated.json if the page doesn't already have it. No judgement step.
One item per brand per run (up to 4 names + "and N more"). Splash of Color stays out (big catalog, least-favorite weight).
The run can then polish wording; it can no longer forget. scripts/checks/brand_watch_gate.py --stores proves it on publish."""
import json, os, re, datetime, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
F = R + 'config/brand-watch-curated.json'
d = json.load(open(F)); L = json.load(open(R + 'docs/status/partner-launches.json'))
ct = json.load(open(R + 'config/code-truth.json')); pipe = json.load(open(R + 'config/partners-pipeline.json'))
n = lambda s: re.sub(r'[^a-z0-9]', '', (s or '').lower().replace('&', 'and').replace('tartán', 'tartan'))
partners = {n(k) for k in ct['pct']} | {n(k) for k in (ct.get('terms') or {}) if not k.startswith('_')}
partners |= {n(p.get('brand')) for p in (pipe if isinstance(pipe, list) else pipe.get('partners', [])) if isinstance(p, dict)}
SKIPB = {n('Splash of Color'), n('Yellow Mountain Imports'), n('Mahjong Row & Co.')}
def is_partner(b):
    k = n(b)
    return k not in SKIPB and any(p and (p == k or p.startswith(k) or k.startswith(p)) for p in partners)
txt = ' '.join((x.get('what', '') + ' ' + str(x.get('buy', '')) + ' ' + str(x.get('url', '')) + ' ' + ' '.join(x.get('handles') or [])).lower() for s in ('this_week', 'coming_soon', 'just_dropped', 'sales') for x in d[s])
STOP = set('mahjong mahj tiles tile set mat mats the and of with a in rack racks bundle pre order preorder full size travel new edition collection sleek surface american double sided made usa sleeksurface'.split())
def on_page(r):
    if r['handle'] in txt: return True
    w = [x for x in re.findall(r"[a-z0-9']+", r['title'].lower()) if x not in STOP and len(x) > 2]
    if bool(w) and sum(x in txt for x in w) >= max(1, (len(w) + 1) // 2): return True
    return any(f'{a} {b}' in txt or f'{a} to {b}' in txt for a, b in zip(w, w[1:]))   # 'Summit to Sea' = two name words together
cut = (datetime.date.today() - datetime.timedelta(days=10)).isoformat()
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5)))
by = {}
for r in L.get('recent', []) + [e for e in L.get('events', []) if e.get('ev') == 'new']:
    if r.get('kind') not in ('tiles', 'mat', 'rack', 'travel tiles'): continue
    if re.search(r'tablecloth|printable|pillow|placemat|napkin|runner|sweatshirt|tee\b|bag|pouch|tray|coaster|ornament|sticker|candle|scarf|notepad|mouse|cutting board|apron|oven|toaster', r['title'], re.I): continue   # the watcher's kind guess calls a tablecloth a 'mat'
    if (r.get('when') or now.date().isoformat()) < cut or not is_partner(r['brand']) or on_page(r): continue
    if any(x['handle'] == r['handle'] for x in by.get(r['brand'], [])): continue
    by.setdefault(r['brand'], []).append(r)
added = []
for b, rs in by.items():
    rs.sort(key=lambda r: r.get('when') or '', reverse=True)
    names = [re.sub(r'(?i)^.*?™\s*|\s*-\s*$', '', re.sub(r'(?i)\bMahjong\b|\bMat in Tube\b', '', r['title'])).strip(' -') or r['title'] for r in rs]
    names = [re.sub(r'\s{2,}', ' ', x) for x in names]
    kinds = {r['kind'] for r in rs}; kw = 'tile sets' if kinds <= {'tiles', 'travel tiles'} else 'mats' if kinds == {'mat'} else 'pieces'
    what = (f'New {kw} on their site: ' if len(rs) > 1 else 'New on their site: ') + ', '.join(names[:4]) + (f', and {len(names) - 4} more' if len(names) > 4 else '') + '.'
    pre = any(r.get('pre') for r in rs) and not any(r.get('avail') for r in rs)
    date = rs[0].get('when') or now.date().isoformat()
    item = {'partner': True, 'urgency': 'NOW', 'found': now.strftime('%Y-%m-%dT%H:%M'), 'date': date, 'day': datetime.date.fromisoformat(date).strftime('%a %-m/%-d'),
            'time': 'Preorder' if pre else 'LIVE now', 'brand': b, 'what': what, 'tag': {'tiles': 'tiles', 'travel tiles': 'tiles', 'mat': 'mat', 'rack': 'racks'}[rs[0]['kind']],
            'new': True, 'buy': rs[0]['url'], 'url': rs[0]['url'], 'img': rs[0].get('img'), 'source': 'store', 'source_kind': 'store',
            'added_by': 'brand_watch_autoadd (store read, no judgement step)', 'handles': [r['handle'] for r in rs]}
    d['just_dropped'].insert(0, item); added.append(f'{b}: {what}')
if added and '--dry' not in sys.argv:
    d['updated'] = now.strftime('%Y-%m-%dT%H:%M')
    json.dump(d, open(F, 'w'), ensure_ascii=False, indent=1)
print(f'BRAND WATCH AUTO-ADD: {len(added)} brand item(s) added' + ''.join('\n  + ' + a for a in added))
