"""Mahjong Row & Co. OUT of Find Your Mat-ch (Tiffany Nov 6 1:19pm: "Remove them from the site completely ... park somewhere else
so that if we want to turn it back on, we can"). Hides (never deletes) every Mahjong Row & Co. mat, tile set and rack in a build's
D, takes the brand out of the logo order (BLORD) and the tiles-door brand list, and writes what it hid to
archive/mahjong-row-parked-2026-11-06/fym-hidden.json so it can be undone (set hid back to false / remove 'parked').
Usage: python3 builder/fym_fix_nov06/mr_out.py <build dir>   (edits <build dir>/index.html in place). Gate [160] checks the result."""
import sys, os, json, re
B = sys.argv[1]; R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
BRAND = 'Mahjong Row & Co.'; DOM = 'mahjongrowandco.com/'
p = B + '/index.html'; h = open(p).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
hid = {'mats': [], 'tiles': [], 'racks': [], 'sets': []}
for sec in ('mats', 'tiles', 'racks'):
    for k, v in D[sec].items():
        if v.get('bn') == BRAND or k.startswith(DOM):
            if not v.get('hid'): hid[sec].append(k)
            v['hid'] = True; v['parked'] = 'mahjong-row-nov06'
for s in D['sets']:
    if s.get('maker') == BRAND:
        if not s.get('hid'): hid['sets'].append(s['slug'])
        s['hid'] = True; s['parked'] = 'mahjong-row-nov06'
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]
n0 = h.count('"Mahjong Row & Co.", ') + h.count(', "Mahjong Row & Co."')
h = re.sub(r'(const BLORD=\[[^\]]*?)"Mahjong Row & Co\.", ', r'\1', h, count=1)
h = re.sub(r"('Mahjong Row & Co\.',)(?=[^;]*'My Fair Mahjong')", '', h, count=1)
open(p, 'w').write(h)
# Locks (FYM 1.16 build): her Nov 6 1:33pm scope says Find Your Mat-ch loses ALL of Mahjong Row, so the locked 'hid' of their items
# follows her call (otherwise fym_apply_locks.py would un-hide 9 locked mats). Only hid / parked change; everything else stays locked.
LKP = R + 'builder/fym_flags/locks.json'; LK = json.load(open(LKP)); nl = 0
for sec in ('mats', 'tiles', 'racks', 'sets'):
    for k, v in LK.get(sec, {}).items():
        mine = (v.get('bn') == BRAND or k.startswith(DOM)) if sec != 'sets' else any(s.get('slug') == k and s.get('maker') == BRAND for s in D['sets'])
        if mine and 'hid' in v and not v['hid']: v['hid'] = True; nl += 1
if nl:
    LK['_changes'].append('2026-11-06 v116 Mahjong Row & Co. OUT of FYM (Tiffany Nov 6 1:19pm + 1:33pm scope, docs/ANSWERS.md): locked hid -> true for %d items (builder/fym_fix_nov06/mr_out.py)' % nl)
    json.dump(LK, open(LKP, 'w'), indent=1, ensure_ascii=False)
A = R + 'archive/mahjong-row-parked-2026-11-06/'; os.makedirs(A, exist_ok=True)
json.dump(hid, open(A + 'fym-hidden.json', 'w'), indent=1)
print('Mahjong Row OUT of FYM:', {k: len(v) for k, v in hid.items()})
