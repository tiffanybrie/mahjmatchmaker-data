"""FYM v71 tile-set removals (Tiffany Oct 21 6:55pm). Usage: python3 builder/fym_fix_oct21/tile_removals.py <build_dir>
1. Only full-size sets are matched: every add-on / partial tile product (numbered flower packs, flower/joker/blank add-ons, sample,
   mini, travel) is hidden and locked hidden. Found Oct 21: Miss Mahjong Numbered Flower packs x4.
2. Simply (Wren Mats): bad photo + out of stock -> hidden + locked.
Gate [29] fails if a visible tile entry looks like a partial set."""
import sys, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
B = sys.argv[1]; P = os.path.join(B, 'index.html'); h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
PARTIAL = re.compile(r'(?i)numbered[- ]flower|flower[- ](pack|tiles? pack|add)|add[- ]?on\b|\bsample\b|\bmini\b|\btravel\b|joker[- ](pack|set)|blank[- ]tiles?')
EXTRA = {'wren-mats-simply': 'Tiffany Oct 21 6:55pm: bad photo and out of stock'}
L = json.load(open(REPO + 'builder/fym_flags/locks.json')); hid = []
for s in D['sets']:
    t = D['tiles'][s['tile']]
    why = EXTRA.get(s['slug']) or ('Tiffany Oct 21 6:55pm: partial / add-on tile product, "we\'re only matching full size sets"' if PARTIAL.search(s['name'] + ' ' + t.get('n', '') + ' ' + (t.get('u0') or t.get('u', ''))) else None)
    if not why or s.get('hid'): continue
    s['hid'] = True; s['m'] = []; hid.append((s['slug'], why))
    L['sets'].setdefault(s['slug'], {'name': s['name']}); L['sets'][s['slug']].update(hid=True, m=[])
if hid:
    L['_changes'].append({'date': '2026-10-21', 'set': ','.join(x[0] for x in hid), 'field': 'hid', 'change': 'hidden + locked hidden', 'approval': '; '.join(sorted({x[1] for x in hid}))})
    json.dump(L, open(REPO + 'builder/fym_flags/locks.json', 'w'), ensure_ascii=False, indent=1)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h)
print('hidden', hid)
