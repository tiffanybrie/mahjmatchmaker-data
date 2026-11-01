"""v113 (Nov 1, Tiffany 4:50am): Sunday Vegan Leather Ruby + Forrest (own cards) and the Let's Be Besties full mat catalog.
Runs builder/fym_fix_oct31/partneradds109.py UNCHANGED in logic with spec config/fym-adds-nov01b.json, ADD 'nov01-v113'
(photos looked at on contact sheets: angled/room shots hidden + Questionable; custom/personalized + non-mahjong game mats skipped;
material / instruction twins merged into one card with 'Also available in ...'). Post: alt + ncn from the spec.
Idempotent. Usage: python3 adds113.py <build_dir>"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
SRC = REPO + 'builder/fym_fix_oct31/partneradds109.py'
src = open(SRC).read()
for a, b in [("config/fym-nonpartner-adds-oct31b.json", "config/fym-adds-nov01b.json"),
             ("ADD = 'oct31-v109'", "ADD = 'nov01-v113'"),
             ("src='nonpartner-adds-oct31b'", "src='adds-nov01b'"),
             ("'Oct 31 non-partner Etsy brand add (v109, Tiffany Brands to Bring In = now): '", "'Nov 1 v113 add (Tiffany 4:50am): '")]:
    assert a in src, 'partneradds109 changed, re-check anchor: ' + a
    src = src.replace(a, b)
g = {'__name__': '__main__', '__file__': SRC}
exec(compile(src, SRC, 'exec'), g)
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
SPEC = json.load(open(REPO + 'config/fym-adds-nov01b.json')); n = 0
for x in SPEC['mats']:
    o = D['mats'].get(x['key'])
    if not o: continue
    if x.get('alt') and o.get('alt') != x['alt']: o['alt'] = x['alt']; n += 1
    if x.get('ncn') and not o.get('ncn'): o['ncn'] = 1; n += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h)
# QA Nov 1: spec mats that are visible now (flat brand image found) leave the Questionable list; merged twins leave FYM records
QP = REPO + 'builder/fym_flags/fym_questionable.json'; Q = json.load(open(QP)); vis = {x['key'] for x in SPEC['mats'] if not x['hid']}
skipk = {'letsbebesties.com/' + k for k, _ in SPEC.get('skipped', []) if 'merged' in _}
q0 = len(Q['items']); Q['items'] = [it for it in Q['items'] if it['key'] not in vis and it['key'] not in skipk]
if len(Q['items']) != q0: json.dump(Q, open(QP, 'w'), indent=1, ensure_ascii=False)
print('adds113 post steps:', n, '| questionable removed', q0 - len(Q['items']))
