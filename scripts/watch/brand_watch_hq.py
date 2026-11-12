#!/usr/bin/env python3
"""Build hq/brandWatch for the HQ 'Brand Watch' tab.
Curated lines (config/brand-watch-curated.json) lead; new deduped events from the
store watcher (docs/status/partner-launches.json) and the IG watcher
(docs/status/mahj-watch.json) that the curated file doesn't cover go under
'auto' (one line per real event). Writes docs/status/brand-watch-hq.json; the
caller writes it to HQ with ArtifactData set hq/brandWatch.
Usage: python3 scripts/watch/brand_watch_hq.py
"""
import json, re, datetime, pathlib
R = pathlib.Path(__file__).resolve().parents[2]
cur = json.load(open(R/'config/brand-watch-curated.json'))
watch = json.load(open(R/'docs/status/mahj-watch.json'))
launch = json.load(open(R/'docs/status/partner-launches.json'))
MAHJ = re.compile(r'mahj|tile|mat\b|mats\b|rack|bam|dragon|joker', re.I)
EXCL = re.compile(r'mahjong row|yellow mountain', re.I)
covered = set()
for sec in ('this_week','coming_soon','just_dropped','sales','nonpartners'):
    for x in cur.get(sec, []):
        if x.get('url'): covered.add(x['url'].split('?')[0].rstrip('/'))
def norm(s): return re.sub(r'[^a-z0-9 ]','',(s or '').lower())[:70]
seen = set(); auto = []
today = datetime.date.today()
for x in watch.get('instagram', []) + watch.get('store', []):
    if EXCL.search(x.get('brand','')): continue
    u = (x.get('url') or '').split('?')[0].rstrip('/')
    if u in covered: continue
    if not x.get('partner') and not MAHJ.search(x.get('caption','')): continue
    key = (x.get('brand'), u) if u else (x.get('brand'), norm(x.get('caption')))
    k2 = (x.get('brand'), norm(x.get('caption')))
    if key in seen or k2 in seen: continue
    seen.add(key); seen.add(k2)
    try:
        if (today - datetime.date.fromisoformat(x.get('posted','')[:10])).days > 7: continue
    except Exception: pass
    auto.append({'date': x.get('posted',''), 'brand': x.get('brand'), 'partner': bool(x.get('partner')),
                 'kind': x.get('kind',''), 'what': (x.get('caption') or '')[:160], 'url': x.get('url',''),
                 'src': x.get('src','')})
# curated brand+date pairs (±1 day) already told: skip their IG duplicates
cb = set()
for sec in ('this_week','just_dropped'):
    for x in cur.get(sec, []):
        b = re.sub(r' \(.*','',x.get('brand','')).lower()
        try: d = datetime.date.fromisoformat(x.get('date',''))
        except Exception: continue
        for k in (-1,0,1): cb.add((b[:12], (d+datetime.timedelta(days=k)).isoformat()))
auto = [a for a in auto if (a['brand'].lower()[:12], a['date'][:10]) not in cb]
# one line per brand+day for store listings
grp = {}; rest = []
for a in auto:
    if a['src'] == 'store':
        g = grp.setdefault((a['brand'], a['date'][:10]), dict(a, items=[]))
        g['items'].append(a['what'])
    else: rest.append(a)
for g in grp.values():
    n = len(g['items']); g['what'] = (f"{n} new listings: " if n > 1 else '') + '; '.join(g['items'][:4]) + (' …' if n > 4 else '')
    g.pop('items')
auto = rest + list(grp.values())
auto.sort(key=lambda a: a['date'], reverse=True); auto.sort(key=lambda a: not a['partner'])
out = dict(cur); out.pop('_note', None)
# Tiffany Nov 12 10:26am: the Brand Watch tab is a CATALOG, not a to-do list. No "Do:" lines, no "I did it" boxes,
# no group-post drafts waiting on her yes (the HQ page shows "Do:" + "I did it" for any item with an 'action').
# Past dated drops leave "this week" (they stay in just_dropped for 7 days).
# Tiffany Nov 12 10:27am: Mahjong Studios + Splash of Color updates ALWAYS rank last, never up front:
# they leave every top list and go to the very end of 'auto' (the last list on the tab).
BURY = re.compile(r'mahjong studios|splash of color', re.I)
buried = []
for sec in ('this_week','coming_soon','just_dropped','sales'):
    keep = []
    for x in out.get(sec, []) or []:
        x = {k: v for k, v in x.items() if k != 'action'}
        if sec == 'this_week':
            try:
                if datetime.date.fromisoformat(str(x.get('date'))[:10]) < today: continue
            except Exception: pass
        if sec == 'just_dropped':
            try:
                if (today - datetime.date.fromisoformat(str(x.get('date'))[:10])).days > 7: continue
            except Exception: pass
        (buried if BURY.search(x.get('brand','') or '') else keep).append(x)
    out[sec] = keep
out['nonpartners'] = [{k: v for k, v in x.items() if k != 'action'} for x in out.get('nonpartners', []) or []]
auto = [a for a in auto if not BURY.search(a.get('brand','') or '')] + [a for a in auto if BURY.search(a.get('brand','') or '')]
out['auto'] = [a for a in auto if not BURY.search(a.get('brand','') or '')][:25] + [dict(b, kind=b.get('tag','')) for b in buried] + [a for a in auto if BURY.search(a.get('brand','') or '')]
out['updatedAt'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
out['sources'] = {'store_run': launch.get('run_at'), 'ig_run': watch.get('run_at')}
p = R/'docs/status/brand-watch-hq.json'
json.dump(out, open(p,'w'), indent=1, ensure_ascii=False)
print(f"wrote {p} · this_week {len(out['this_week'])} · coming {len(out['coming_soon'])} · dropped {len(out['just_dropped'])} · auto {len(out['auto'])}")
