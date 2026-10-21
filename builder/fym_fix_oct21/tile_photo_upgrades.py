"""Apply the tile-photo audit (builder/fym_flags/tile_photo_upgrades.json) to an FYM build. Usage: python3 builder/fym_fix_oct21/tile_photo_upgrades.py <build_dir>
Expected file (written by the audit): {"default": {"fp": [x, y], "fz": z}?, "items": {<set slug or tile key>: {"status": "upgrade"|"ok"|"coming_soon",
  "photo": "<repo path of the new full photo>"?, "pile": "<repo path of a square picker photo>"?, "fp": [x, y]?, "fz": z?, "faces_only": bool?, "reason": "..."}}}
 - coming_soon: T[tile].soon = true (the app draws the brand "Photo coming soon" card; the set stays selectable)
 - upgrade: new full photo copied into the build (t71/<slug>.jpg), optional square pile (b21v1.js), optional fp/fz framing on the set(s)
 - ok: framing only (fp/fz), photo unchanged; faces_only items get the file's global "default" back + faces crop when no fp/fz is given
Locked tiles (builder/fym_flags/locks.json tiles) change only when the item carries a "reason"; their lock is updated with that reason."""
import sys, os, json, io, base64, shutil
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
B = sys.argv[1]; F = REPO + 'builder/fym_flags/tile_photo_upgrades.json'
if not os.path.exists(F): print('no tile_photo_upgrades.json yet: nothing applied'); sys.exit(0)
U = json.load(open(F)); DEF = U.get('default') or {}
P = os.path.join(B, 'index.html'); h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
T = D['tiles']; L = json.load(open(REPO + 'builder/fym_flags/locks.json'))
by_slug = {s['slug']: s for s in D['sets']}
IMGS, done, refused = {}, [], []
os.makedirs(os.path.join(B, 't71'), exist_ok=True)
for key, it in U.get('items', {}).items():
    s = by_slug.get(key); tk = s['tile'] if s else key
    if tk not in T: refused.append((key, 'unknown')); continue
    locked = tk in L['tiles']
    if locked and it.get('status') in ('upgrade', 'coming_soon') and not it.get('reason'): refused.append((key, 'locked, no reason')); continue
    sets = [x for x in D['sets'] if x['tile'] == tk]
    st = it.get('status')
    if st == 'coming_soon': T[tk]['soon'] = True
    elif st == 'upgrade' and it.get('photo'):
        T[tk].pop('soon', None)
        slug = (s or sets[0])['slug'] if (s or sets) else tk.replace('/', '_')
        im = Image.open(REPO + it['photo']).convert('RGB'); im.thumbnail((1000, 1000)); fn = f't71/{slug}.jpg'; im.save(os.path.join(B, fn), quality=86)
        T[tk]['full'] = fn; T[tk]['src'] = it['photo']
        pp = Image.open(REPO + it['pile']).convert('RGB') if it.get('pile') else None
        if pp is None:
            w, hh = im.size; q = min(w, hh); pp = im.crop(((w - q) // 2, (hh - q) // 2, (w - q) // 2 + q, (hh - q) // 2 + q))
        pp = pp.resize((360, 360)); b = io.BytesIO(); pp.save(b, 'JPEG', quality=82); pk = 'p71' + slug[:20]
        IMGS[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode(); T[tk]['pile'] = pk
        if locked: L['tiles'][tk].update(src=it['photo'], full=fn, pile=pk)
    fr = {k: it[k] for k in ('fp', 'fz') if k in it} or ({k: DEF[k] for k in ('fp', 'fz') if k in DEF} if it.get('faces_only') else {})
    for x in sets: x.update(fr)
    if locked and it.get('reason'): L['_changes'].append({'date': it.get('date', ''), 'tile': tk, 'field': 'photo', 'change': st, 'approval': it['reason']})
    done.append((key, st))
if IMGS:
    open(os.path.join(B, 'b21v1.js'), 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMGS) + ');')
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if IMGS and 'b21v1.js' not in h: h = h.replace('<script src="b20v1.js"></script>', '<script src="b20v1.js"></script><script src="b21v1.js"></script>', 1)
open(P, 'w').write(h); json.dump(L, open(REPO + 'builder/fym_flags/locks.json', 'w'), ensure_ascii=False, indent=1)
print('applied', len(done), 'refused', refused)
