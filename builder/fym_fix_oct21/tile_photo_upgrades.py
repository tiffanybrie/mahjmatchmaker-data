"""Apply the tile-photo audit (builder/fym_flags/tile_photo_upgrades.json, commit 9450473) to an FYM build.
Usage: python3 builder/fym_fix_oct21/tile_photo_upgrades.py <build_dir>
 - status upgrade: the proposed photo (assets/tiles/catalog-better/...) becomes the tile's full photo (t71/<slug>.jpg) and its square
   picker pile (b21v1.js); the set's frame (fp/fz) is applied (mostly a reset to centre: old chart-photo crops no longer apply).
   Locked tiles change only with the recorded reason (Classic Tortoise: Tiffany 6:57pm); their lock is updated.
 - status ok with a frame: framing only (Mahjong Studios chart crops: faces + tile-back swatch).
 - status coming_soon: HELD (coordinator, Oct 21 7pm: asking Tiffany whether to lower the bar). The build marks the tile `cs` (candidate)
   and shows the "Photo coming soon" card ONLY for sets listed in builder/fym_flags/tile_coming_soon_on.json ({"on": [slugs]} or
   {"all": true}). One switch: edit that file, re-run this script, gate, QA.
Entries are matched by tile_key (the audit's slugs can differ from build slugs, e.g. classic-tortoise = build 'tortoise')."""
import sys, os, io, json, base64, shutil
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
B = sys.argv[1]
U = json.load(open(REPO + 'builder/fym_flags/tile_photo_upgrades.json'))['sets']
SW = REPO + 'builder/fym_flags/tile_coming_soon_on.json'
if not os.path.exists(SW):
    json.dump({'_note': "coming_soon switch (Oct 21): sets listed in 'on' (or all: true) show the Photo coming soon card. Empty = held, current photos stay.", 'all': False, 'on': []}, open(SW, 'w'), indent=1)
SWJ = json.load(open(SW)); ON_ALL, ON = bool(SWJ.get('all')), set(SWJ.get('on') or [])
P = os.path.join(B, 'index.html'); h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
T = D['tiles']; L = json.load(open(REPO + 'builder/fym_flags/locks.json')); TF = json.load(open(REPO + 'builder/fym_flags/tile_photo_flags.json'))
sets_by_tile = {}
for s in D['sets']: sets_by_tile.setdefault(s['tile'], []).append(s)
os.makedirs(os.path.join(B, 't71'), exist_ok=True)
IMGS, rep = {}, {'upgrade': [], 'frame': [], 'cs_held': [], 'cs_on': [], 'skipped': []}
TORT = 'www.bambirdboutique.com/east-meets-west-tortoise-shell-tile-set-copy'
for key, it in U.items():
    tk = it.get('tile_key'); ss = sets_by_tile.get(tk, [])
    if tk not in T or not ss: rep['skipped'].append((key, 'not in build')); continue
    st = it['status']
    if st == 'upgrade':
        locked = tk in L['tiles']
        if locked and not it.get('reason'): rep['skipped'].append((key, 'locked without reason')); continue
        src = it['proposed']
        if tk == TORT:  # canonical album photo: lives in assets/tiles/album (canon map + album/index.json + identity check)
            dst = 'assets/tiles/album/classic-tortoise-cream.jpg'
            if not os.path.exists(REPO + dst): shutil.copyfile(REPO + src, REPO + dst)
            src = dst
        im = Image.open(REPO + src).convert('RGB'); slug = ss[0]['slug']
        full = im.copy(); full.thumbnail((1000, 1000)); fn = f't71/{slug}.jpg'; full.save(os.path.join(B, fn), quality=88)
        w, hh = im.size; q = min(w, hh); pp = im.crop(((w - q) // 2, (hh - q) // 2, (w - q) // 2 + q, (hh - q) // 2 + q)).resize((360, 360), Image.LANCZOS)
        b = io.BytesIO(); pp.save(b, 'JPEG', quality=84); pk = 'p71' + slug.replace('-', '')[:24]
        IMGS[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
        T[tk].update(full=fn, pile=pk, src=src); T[tk].pop('cs', None); T[tk].pop('soon', None)
        if locked:
            L['tiles'][tk].update(src=src, full=fn, pile=pk)
            L['_changes'].append({'date': '2026-10-21', 'tile': tk, 'field': 'src/full/pile', 'change': f'{src} (tile photo audit upgrade)', 'approval': it['reason']})
        for s in ss:
            if s['slug'] in TF and TF[s['slug']].get('photo'):
                TF[s['slug']].update(photo=fn, note=TF[s['slug']].get('note', '') + ' | Oct 21 tile photo audit upgrade: ' + it.get('reason', ''))
        rep['upgrade'].append(slug)
    elif st == 'coming_soon':
        T[tk]['cs'] = 1
        if ON_ALL or any(s['slug'] in ON or key in ON for s in ss): T[tk]['soon'] = True; rep['cs_on'].append(key)
        else: T[tk].pop('soon', None); rep['cs_held'].append(key)
    fr = it.get('frame')
    if fr and st in ('upgrade', 'ok'):
        for s in ss:
            s['fp'] = fr['fp']; s['fz'] = fr.get('fz', 1)
            if s['slug'] in L['sets'] and ('fp' in L['sets'][s['slug']] or 'fz' in L['sets'][s['slug']]):
                L['sets'][s['slug']].update(fp=s['fp'], fz=s['fz'])
        rep['frame'].append(key)
# canon map + album index for Classic Tortoise
AI = REPO + 'assets/tiles/album/index.json'; ai = json.load(open(AI))
if 'Classic Tortoise' in ai and ai['Classic Tortoise']['file'] != 'assets/tiles/album/classic-tortoise-cream.jpg' and 'tortoise' in [s['slug'] for s in D['sets'] if s['tile'] == TORT]:
    ai['Classic Tortoise'].update(prev_file=ai['Classic Tortoise']['file'], file='assets/tiles/album/classic-tortoise-cream.jpg',
                                  note=ai['Classic Tortoise'].get('note', '') + " | Oct 21 6:57pm Tiffany: her isolated tortoise PNG composited on cream (#faf7f0) replaces the confetti-mat zoom, everywhere; she will shoot a real pile later")
    json.dump(ai, open(AI, 'w'), ensure_ascii=False, indent=1)
if IMGS:
    open(os.path.join(B, 'b21v1.js'), 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMGS) + ');')
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if IMGS and 'b21v1.js' not in h: h = h.replace('<script src="b20v1.js"></script>', '<script src="b20v1.js"></script><script src="b21v1.js"></script>', 1)
json.dump(TF, open(REPO + 'builder/fym_flags/tile_photo_flags.json', 'w'), ensure_ascii=False, indent=1)
open(P, 'w').write(h); json.dump(L, open(REPO + 'builder/fym_flags/locks.json', 'w'), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in rep.items()}, 'skipped:', rep['skipped'])
