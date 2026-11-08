"""FYM 1.18: an album that went LIVE (Juniper, Nov 8 ~12:45am) is now an album set in the gate's eyes:
  [1]  its album photo is locked (builder/fym_flags/locks.json tiles.<tile key> = the build's current album src / full / pile);
  [36] every Tiffany's-match pairing leads with her rack picks for that mat (config/mat-racks-picks.json via rack_picks.expected),
       then the racks the pairing already had. Applies to every set's m (only missing picks are added). Run after juniper_m118.py.
Idempotent. Usage: python3 builder/fym_fix_nov07/albumlive118.py <build dir>"""
import sys, os, json
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, R + 'builder/fym_fix_oct22'); from rack_picks import expected
P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); e += i
L = json.load(open(R + 'builder/fym_flags/locks.json')); nl = 0
for slug in ('juniper',):
    s = next(x for x in D['sets'] if x['slug'] == slug); t = D['tiles'][s['tile']]
    if s['tile'] not in L['tiles'] and t.get('src'):
        L['tiles'][s['tile']] = {'set': s['name'], 'src': t['src'], 'full': t['full'], 'pile': t.get('pile')}; nl += 1
# rule 3 (album tile photos are canonical): the FYM tile photo becomes the album photo (Juniper: the OMM pile shot, round 3 Nov 6)
from PIL import Image
nt = 0
for slug in ('juniper',):
    s = next(x for x in D['sets'] if x['slug'] == slug); t = D['tiles'][s['tile']]; src = R + t['src']
    rel = f't118/{slug}.jpg'; out = os.path.join(sys.argv[1], rel)
    if t.get('full') != rel or not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True); im = Image.open(src).convert('RGB'); im.thumbnail((1200, 1200)); im.save(out, 'JPEG', quality=88)
        t['full'] = rel; t.pop('fo', None); nt += 1
        if s['tile'] in L['tiles']: L['tiles'][s['tile']]['full'] = rel
lm, _, _ = expected(json.loads(json.dumps(D))); nr = 0
for s in D['sets']:
    for x in s.get('m', []):
        want = (lm or {}).get(x[0]) or []
        cur = x[1] if len(x) > 1 else []
        if not all(r in cur for r in want):
            new = list(dict.fromkeys(list(want) + list(cur)))
            if len(x) > 1: x[1] = new
            else: x.append(new)
            nr += 1
            if s['slug'] in L['sets'] and 'm' in L['sets'][s['slug']]: L['sets'][s['slug']]['m'] = s['m']
open(P, 'w').write(h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:])
json.dump(L, open(R + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
print('albumlive118: album photos locked', nl, '| tile photo = album photo', nt, '| pairings given her rack picks', nr)
