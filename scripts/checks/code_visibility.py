#!/usr/bin/env python3
"""Honest code-visibility scorecard (Tiffany Nov 6 2026: "we show for all 34" was false; no glossed answers).

One row per CHECK in docs/status/code-visibility-checks.jsonl:
  {"date": "YYYY-MM-DD", "brand": "<brand>", "surface": "<surface>", "hit": true|false,
   "detail": "...", "source": "..."}
Surfaces: claude_search (WebSearch tool, Claude-side index), google_ai_overview (signed-out/desktop or mobile,
say which in detail), google_ai_mode, google_organic_top3, chatgpt, gemini.
A brand/surface with no row in the window is 'not checked' - NEVER assumed yes.

Usage:
  python3 scripts/checks/code_visibility.py ingest-seo <dir with seo/*.json from ArtifactData export>
  python3 scripts/checks/code_visibility.py add <date> <surface> <brand> <yes|no> [detail]
  python3 scripts/checks/code_visibility.py report --money <dir with money/*.json> [--date YYYY-MM-DD] [--days 7]
        [--md out.md] [--json out.json]
Report: per brand x surface 'hits/checks (last date)'; per surface 'X of N brands hit on latest check'
plus 'X of N checks hit in window'; joined with each brand's orders/commission last 7 days vs prior 7."""
import json, os, re, sys, glob, argparse, collections, datetime as dt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG = os.path.join(ROOT, 'docs/status/code-visibility-checks.jsonl')
SURFACES = ['google_organic_top3', 'google_ai_overview', 'google_ai_mode', 'chatgpt', 'gemini', 'claude_search']
LABEL = {'google_organic_top3': 'Google top 3', 'google_ai_overview': 'AI Overview', 'google_ai_mode': 'AI Mode',
         'chatgpt': 'ChatGPT', 'gemini': 'Gemini', 'claude_search': 'Claude search'}
EXCLUDE = {'Mahjong Row & Co.'}  # out Nov 6 2026
ALIAS = {'tigre de tartán': 'Tigre de Tartán', 'tigre de tartan': 'Tigre de Tartán', 'mahjong co.': 'The Mahjong Co.',
         'the mahjong co.': 'The Mahjong Co.', 'soiree all day': 'Soirée All Day', 'anders ruff design co.': 'Anders Ruff',
         'middle and main mahjong': 'Middle & Main Mahjong', 'middle & main': 'Middle & Main Mahjong',
         'mac+miller mahjong': 'Mac + Miller Mahjong', 'mac + miller': 'Mac + Miller Mahjong',
         'amanda toppe living': 'Amanda Toppe', 'virora': 'Virora Mahjong', 'amahj line': 'Amahj',
         'lets be besties': "Let's Be Besties", 'bird and bamboo': 'Bird & Bamboo', 'britt mills (bmd)': 'Britt Mills',
         'britt mills design': 'Britt Mills', 'royal mahjong society': 'The Royal Mahjong Society', 'middle and main': 'Middle & Main Mahjong'}

def norm(b):
    b = b.split(' (')[0].strip()
    return ALIAS.get(b.lower(), b)

def load():
    rows = []
    if os.path.exists(LOG):
        for line in open(LOG):
            line = line.strip()
            if line: rows.append(json.loads(line))
    return rows

def save(rows):
    seen, out = set(), []
    for r in rows:
        k = (r['date'], norm(r['brand']), r['surface'], r.get('source', ''))
        if k in seen: continue
        seen.add(k); out.append(r)
    out.sort(key=lambda r: (r['date'], r['surface'], r['brand']))
    with open(LOG, 'w') as f:
        for r in out: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    return len(out)

def ingest_seo(d):
    rows = load(); n0 = len(rows)
    for f in sorted(glob.glob(os.path.join(d, '**', '*.json'), recursive=True)):
        day = os.path.basename(f)[:-5]
        try: dt.date.fromisoformat(day)
        except ValueError: continue
        j = json.load(open(f)); j = j.get('data', j)
        for b in j.get('aiBrands') or []:
            if not b.get('checked'): continue
            brand = norm(b['brand'])
            rows.append({'date': day, 'brand': brand, 'surface': 'google_ai_overview', 'hit': bool(b.get('namesUs')),
                         'detail': ('cites us' if b.get('cites') else '') + ('' if b.get('overview', True) else ' no overview shown'),
                         'source': 'morning report (Chrome, ' + ('desktop' if 'desktop' in str(b.get('position', '')) else 'device n/a') + ')'})
            m = re.match(r'#(\d+)', str(b.get('position') or ''))
            if m:
                rows.append({'date': day, 'brand': brand, 'surface': 'google_organic_top3', 'hit': int(m.group(1)) <= 3,
                             'detail': str(b.get('position')), 'source': 'morning report'})
    print('ingested', save(rows) - n0, 'new rows')

def money(d):
    day = {}
    for f in glob.glob(os.path.join(d, '**', '*.json'), recursive=True):
        k = os.path.basename(f)[:-5]
        try: dt.date.fromisoformat(k)
        except ValueError: continue
        j = json.load(open(f)); j = j.get('data', j)
        agg = collections.defaultdict(lambda: [0, 0.0, False])
        for b in j.get('brands', []):
            if b['brand'].startswith('ShopMy'): continue
            a = agg[norm(b['brand'])]; a[0] += b.get('orders') or 0; a[1] += b.get('commission') or 0
            if b.get('commission') is None: a[2] = True
        day[k] = (agg, bool(j.get('partial')))
    return day

def report(a):
    rows = [r for r in load() if norm(r['brand']) not in EXCLUDE]
    end = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
    start = end - dt.timedelta(a.days - 1)
    win = [r for r in rows if start.isoformat() <= r['date'] <= end.isoformat()]
    brands = sorted({norm(r['brand']) for r in rows})
    cell = collections.defaultdict(lambda: {'hits': 0, 'n': 0, 'last': None, 'lasthit': None})
    for r in sorted(win, key=lambda r: r['date']):
        c = cell[(norm(r['brand']), r['surface'])]; c['n'] += 1; c['hits'] += 1 if r['hit'] else 0
        c['last'] = r['date']; c['lasthit'] = r['hit']
    surf = {}
    for s in SURFACES:
        latest = max((r['date'] for r in win if r['surface'] == s), default=None)
        lat = [r for r in win if r['surface'] == s and r['date'] == latest]
        allc = [r for r in win if r['surface'] == s]
        surf[s] = {'latest': latest, 'latest_hits': sum(r['hit'] for r in lat), 'latest_n': len({norm(r['brand']) for r in lat}),
                   'window_hits': sum(r['hit'] for r in allc), 'window_n': len(allc),
                   'brands_checked': len({norm(r['brand']) for r in allc}), 'brands_total': len(brands),
                   'always': sum(1 for b in brands if (c := cell.get((b, s))) and c['n'] >= 2 and c['hits'] == c['n'])}
    sales = {}
    if a.money:
        md = money(a.money)
        def rng(e, n): return [(e - dt.timedelta(i)).isoformat() for i in range(n)]
        l7, p7 = rng(end, 7), rng(end - dt.timedelta(7), 7)
        for b in brands:
            def s(ds):
                o = c = 0; unk = False
                for d in ds:
                    if d in md and b in md[d][0]:
                        v = md[d][0][b]; o += v[0]; c += v[1]; unk = unk or v[2]
                return o, round(c, 2), unk
            sales[b] = {'last7': s(l7), 'prev7': s(p7)}
    out = {'date': end.isoformat(), 'window_days': a.days, 'surfaces': surf, 'brands': []}
    for b in brands:
        e = {'brand': b}
        for s in SURFACES:
            c = cell.get((b, s))
            e[s] = None if not c else {'hits': c['hits'], 'n': c['n'], 'last': c['last'], 'lasthit': c['lasthit']}
        if b in sales: e['sales'] = sales[b]
        out['brands'].append(e)
    if a.json: json.dump(out, open(a.json, 'w'), indent=1, ensure_ascii=False)
    L = [f"# Code visibility scorecard, {end.isoformat()} (last {a.days} days)", '',
         'Rule: a cell is hits/checks in the window and the date of the last check; "not checked" means nobody looked, never "yes".', '',
         '## By surface', '', '| Surface | Latest check | Brands hit on latest check | Checks hit in window | Brands hit on EVERY check (2+ checks) | Brands never checked |', '|---|---|---|---|---|---|']
    for s in SURFACES:
        v = surf[s]
        L.append(f"| {LABEL[s]} | {v['latest'] or 'never'} | {v['latest_hits']} of {v['latest_n']} checked | {v['window_hits']} of {v['window_n']} ({round(100*v['window_hits']/v['window_n']) if v['window_n'] else 0}%) | {v['always']} | {v['brands_total'] - v['brands_checked']} of {v['brands_total']} |")
    L += ['', '## By brand (sales = orders / commission, last 7 vs prior 7; * = some amounts unknown)', '',
          '| Brand | ' + ' | '.join(LABEL[s] for s in SURFACES) + ' | Sales 7d | Prior 7d |', '|' + '---|' * (len(SURFACES) + 3)]
    for e in out['brands']:
        cells = []
        for s in SURFACES:
            c = e[s]
            cells.append('not checked' if not c else f"{c['hits']}/{c['n']} ({c['last'][5:]}{' ✓' if c['lasthit'] else ' ✗'})")
        sl = e.get('sales', {}); f = lambda t: f"{t[0]} / ${t[1]}{'*' if t[2] else ''}" if t else ''
        L.append(f"| {e['brand']} | " + ' | '.join(cells) + f" | {f(sl.get('last7'))} | {f(sl.get('prev7'))} |")
    txt = '\n'.join(L) + '\n'
    if a.md: open(a.md, 'w').write(txt)
    print(txt)

ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd')
p = sp.add_parser('ingest-seo'); p.add_argument('dir')
p = sp.add_parser('add'); p.add_argument('date'); p.add_argument('surface'); p.add_argument('brand'); p.add_argument('hit'); p.add_argument('detail', nargs='?', default=''); p.add_argument('--source', default='manual')
p = sp.add_parser('report'); p.add_argument('--money'); p.add_argument('--date'); p.add_argument('--days', type=int, default=7); p.add_argument('--md'); p.add_argument('--json')
a = ap.parse_args()
if a.cmd == 'ingest-seo': ingest_seo(a.dir)
elif a.cmd == 'add':
    assert a.surface in SURFACES, SURFACES
    r = load(); r.append({'date': a.date, 'brand': norm(a.brand), 'surface': a.surface, 'hit': a.hit.lower() in ('y', 'yes', 'true', '1'), 'detail': a.detail, 'source': a.source}); save(r)
elif a.cmd == 'report': report(a)
else: ap.print_help()
