"""Tiffany Oct 25 15:02: Sierra + Anders Ruff Tartan Toile Noël is NOT a match (mis-swipe). Remove it everywhere.
Live Sierra album page: card removed by the Matches chat (Chrome) Oct 25 15:15. This script removes it from the repo sources
(locks, holiday sections push, holiday manifest, search index) and, given a build dir, from FYM (Sierra's m list).
Usage: python3 v87_sierra.py [<build_dir>]"""
import sys, os, json, re
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
MAT = 'shop.andersruff.com/tartan-toile-noel-mahjong-mat'; SLUG = 'sierra'
L = json.load(open(REPO + 'builder/fym_flags/locks.json'))
s = L['sets'].get(SLUG)
if s and any(x[0] == MAT for x in s.get('m', [])):
    s['m'] = [x for x in s['m'] if x[0] != MAT]
    L.setdefault('_changes', []).append('2026-10-25: sierra m: removed Tartan Toile Noël (Tiffany: mis-swipe, not a match)')
    json.dump(L, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False); print('locks: removed')
# holiday sections push: drop the figure
p = REPO + 'pushes/holiday_sections.json'; H = json.load(open(p)); sec = H['sections'].get('sierra-mahjong-tile-matches', '')
m = sec.find('tartan-toile-no-l-mat.jpg')
if m >= 0:
    a = sec.rfind('<figure', 0, m); b = sec.find('</figure>', m) + 9
    H['sections']['sierra-mahjong-tile-matches'] = sec[:a] + sec[b:]; json.dump(H, open(p, 'w'), ensure_ascii=False); print('holiday_sections: removed')
# holiday manifest
p = REPO + 'scripts/albumcard/holiday_manifest.json'; HM = json.load(open(p))
def drop(o):
    if isinstance(o, list): return [drop(x) for x in o if not (isinstance(x, dict) and 'sierra' in json.dumps(x).lower() and 'tartan-toile' in json.dumps(x).lower())]
    if isinstance(o, dict): return {k: drop(v) for k, v in o.items() if not (('sierra' in k.lower()) and ('tartan-toile' in k.lower() or 'tartan-toile' in json.dumps(v).lower()))}
    return o
n0 = json.dumps(HM).count('tartan-toile'); HM = drop(HM); json.dump(HM, open(p, 'w'), indent=1, ensure_ascii=False)
print('holiday_manifest tartan-toile mentions', n0, '->', json.dumps(HM).count('tartan-toile'))
# search index
p = REPO + 'assets/search/search-index.json'; SI = json.load(open(p))
def dsi(o):
    if isinstance(o, list): return [dsi(x) for x in o if not (isinstance(x, (dict, list)) and 'sierra' in json.dumps(x).lower() and 'tartan toile' in json.dumps(x, ensure_ascii=False).lower())]
    if isinstance(o, dict): return {k: dsi(v) for k, v in o.items()}
    return o
a0 = json.dumps(SI, ensure_ascii=False).count('Tartan Toile'); SI = dsi(SI); json.dump(SI, open(p, 'w'), ensure_ascii=False, separators=(',', ':'))
print('search index Tartan Toile mentions', a0, '->', json.dumps(SI, ensure_ascii=False).count('Tartan Toile'))
if len(sys.argv) > 1:
    P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
    for st in D['sets']:
        if st['slug'] == SLUG: st['m'] = [x for x in st['m'] if x[0] != MAT]
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h); print('FYM build: removed from Sierra')
