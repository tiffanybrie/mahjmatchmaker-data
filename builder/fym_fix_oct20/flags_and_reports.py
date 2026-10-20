"""Oct 20: write photo flags + locks (builder/fym_flags/) and the review lists in the staged folder.
Usage: python3 flags_and_reports.py <out_dir>   (out_dir = staged build written by patch.py)
Photo verdicts come from a visual pass over every catalog tile photo (contact sheets), Oct 20."""
import sys, os, json, csv
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
sys.path.insert(0, HERE)
from tilemap import TILEMAP
OUT = sys.argv[1]
h = open(os.path.join(OUT, 'index.html')).read(); i = h.find('const D=') + 8
D, _ = json.JSONDecoder().raw_decode(h, i); T = D['tiles']
rep = json.load(open(os.path.join(OUT, 'patch_report.json')))
key = lambda s: s['slug']
by = {}
for s in D['sets']: by.setdefault(s['name'], s)

# ---- visual verdicts (catalog sets, no album)
FACES_ONLY = {  # tiles visible, but only faces: no back / layers in the photo
 'Garden Stamped': 'Amahj layout, faces only', 'Teal Coastal Signature': 'Amahj layout, faces only', 'Round Top Stamped': 'Amahj, 8 faces only',
 'Pink Coastal Signature': 'Amahj layout, faces only', 'Foundation Beginner': 'Amahj layout, faces only', 'Original Stamped': 'Amahj layout, faces only',
 'White Signature': 'Amahj layout, faces only', 'Light Blue Signature': 'Amahj layout, faces only', 'Lilac Signature': 'Amahj layout, faces only',
 'Navy Signature': 'Amahj layout, faces only', 'White Edit': 'Mahjong Studios layout, no back tile shown', 'Neon Shadow': 'Mahjong Studios layout, no back tile shown',
 'Cowgirl Americana Numbered Flower': 'flower tiles only', 'Darling Numbered Flower': 'flower tiles only', 'Classic Jade Numbered Flower': 'flower tiles only',
 'Classic Malachite Numbered Flower': 'flower tiles only', 'The Texas Series': 'graphic: faces + big banner text', 'The New England Series': 'graphic: faces + banner',
 'The Scandinavian Folk Art Series': 'graphic: faces + banner', 'The Hawaii Series': 'graphic: faces + banner', 'The California Series': 'graphic: faces + banner',
 'The Southwest Series': 'graphic: faces + banner', 'Art Deco': 'faces only', 'Hocus Pocus Halloween': 'faces only',
 "Let's Wander!": 'pyramid of faces, no back', "Let's Be Iconic! Jeweled Purple": 'pyramid of faces, no back', "Let's Garden Party!": 'pyramid of faces, no back',
 "Let's Game. Set. Mahj!": 'pyramid of faces, no back', "Let's Be Iconic! Brilliant Pink": 'pyramid of faces, no back', "Let's Get Tropical!": 'pyramid of faces, no back',
 "Let's Be Iconic! Jeweled Green": 'pyramid of faces, no back', "Let's Get Nautical!": 'pyramid of faces, no back', "Let's Cocktail Party!": 'pyramid of faces, no back',
 'House Hearts Warm White': 'faces in acrylic trays', 'House Tigers Oyster': 'faces in trays', 'House Clovers': 'faces in tray',
 'Eau De Mahj': 'faces on a rack, blurred', 'Mahj in Bloom': 'faces on racks in a styled scene',
}
WATERMARK = ['Red White & Blues Collection', 'Heirloom Collection: Fire + Fortune Ember Fire (', 'Heirloom Collection: Fire + Fortune Verdant Fortune',
             'Laissez Les Bons Temps Rouler Collection', 'Sweet Dreams Collection']
BACK_IN_CORNER = 'layout shot; the back tile sits in a corner, tile view framing (fp) moved to show it'
for n in FACES_ONLY: assert n in by, n
for n in WATERMARK: assert n in by, n

# ---- flags files
os.makedirs(REPO + 'builder/fym_flags', exist_ok=True)
tf = {}
for ix, nm, mk, full, why in rep['hidden']:
    tf[D['sets'][ix]['slug']] = {'name': nm, 'maker': mk, 'flag': 'no_tiles', 'note': why, 'photo': full}
for n, why in FACES_ONLY.items():
    s = by[n]; tf[s['slug']] = {'name': n, 'maker': s['maker'], 'flag': 'faces_only', 'note': why, 'photo': T[s['tile']]['full']}
for n in WATERMARK:
    s = by[n]; tf[s['slug']] = {'name': n, 'maker': s['maker'], 'flag': 'watermark', 'note': 'brand watermark; every product photo on macandmillermahjong.com carries it (checked Oct 20), kept', 'photo': T[s['tile']]['full']}
json.dump(tf, open(REPO + 'builder/fym_flags/tile_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
mf = {}
for mid, n, bn, why in rep['mats']['hidden']:
    mf[mid] = {'name': n, 'brand': bn, 'flag': 'duplicate' if why.startswith('duplicate') else 'no_mat', 'note': why}
json.dump(mf, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)

# ---- locks: album tile photos, her match lists, fixed sets, mats in her lists
locks = {'_about': 'Approved values. fym_apply_locks.py re-applies them; fym_gate.py fails if the build differs. Edit only with Tiffany\'s approval.',
         'tiles': {}, 'sets': {}, 'mats': {}}
herm = set()
for s in D['sets']:
    t = T[s['tile']]
    if s['name'] in TILEMAP and by[s['name']] is s:
        locks['tiles'][s['tile']] = {'set': s['name'], 'src': t['src'], 'full': t['full'], 'pile': t['pile']}
    ent = {}
    if s.get('album') or s.get('sb'):
        ent['m'] = s['m']; ent['sb'] = bool(s.get('sb')); herm.update(x[0] for x in s['m'])
    elif s.get('cat') or s['name'] in [x[0] for x in rep['m_cleared']]:
        ent['m'] = []
    if s.get('hid'): ent['hid'] = True
    if 'fp' in s: ent['fp'] = s['fp']
    if 'fz' in s: ent['fz'] = s['fz']
    if ent: ent['name'] = s['name']; locks['sets'][s['slug']] = ent
touched = set(herm) | {x[0] for x in rep['mats']['hidden']} | {x[0] for x in rep['mats']['renamed']} | {x[0] for x in rep['mats']['image_from_twin']} \
    | {x[0] for x in rep['mats']['color']} | {x[0] for x in rep['mats']['brand']} | {k for k, m in D['mats'].items() if m['rt'] or m.get('hid')}
for mid in sorted(touched):
    m = D['mats'].get(mid)
    if m: locks['mats'][mid] = {'n': m['n'], 'bn': m['bn'], 'f': m['f'], 'th': m['th'], 'rt': m['rt'], 'hid': bool(m.get('hid')), 'mf': m['mf']}
json.dump(locks, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)

# ---- review lists in the staged folder
with open(os.path.join(OUT, 'tile_photo_audit.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['set', 'album photo', 'old FYM photo', 'new FYM photo', 'replaced', 'pixel diff old vs album (0=identical)'])
    for r in rep['tile_photos']: w.writerow(r)
with open(os.path.join(OUT, 'hidden_for_photo.txt'), 'w') as f:
    f.write('Catalog tile sets hidden (D.sets[i].hid=true) until a real tile photo is sourced. index | set | brand | FYM photo | what is wrong\n')
    for r in rep['hidden']: f.write(' | '.join(map(str, r)) + '\n')
with open(os.path.join(OUT, 'faces_only.txt'), 'w') as f:
    f.write('Visible catalog sets whose photo shows tile faces but no back/layers. Needs a better brand photo (none found in repo assets/tiles/**). set | brand | FYM photo | note\n')
    for n, why in FACES_ONLY.items(): f.write(f"{n} | {by[n]['maker']} | {T[by[n]['tile']]['full']} | {why}\n")
with open(os.path.join(OUT, 'no_back_photos.txt'), 'w') as f:
    f.write('Tile photos with no tile back (Oct 20 visual pass of every FYM tile photo).\n\n')
    f.write('A. Show NO tiles at all (bags, boxes, trays, scenes, graphics) -> hidden for launch:\n')
    for r in rep['hidden']: f.write(f"  {r[1]} ({r[2]}) {r[3]}: {r[4]}\n")
    f.write('  Middle & Main "Sunshine": the photo is tiles inside a purple zip bag -> hidden.\n')
    f.write('\nB. Faces only, no back or layers (still visible; listed in faces_only.txt):\n')
    for n, why in FACES_ONLY.items(): f.write(f"  {n} ({by[n]['maker']}): {why}\n")
    f.write('\nC. Back is in the photo but was cropped out by the old top-left framing (fixed with per-set focal point fp):\n')
    f.write('  Florielle (Virora): pink/green back bottom-right, fp [0.6,0.7] zoom 1.15. All Virora layouts fp [0.5,0.68]; Mahjong Studios [0.5,0.72]; Mahjong Row & Co. [0.5,0.7].\n')
    f.write('\nD. Album photo that is low-res / card-only: December 1994 uses assets/tiles/sunday_mahjong_december_1994_tilebox_CARD-ONLY-edited.jpg (360x432, reindeer tile edited in). README-tile-image-rules.md says CARD-ONLY = album-card tile box only. FYM tile view is the same tile-box role, but Tiffany should OK it or supply an unedited December 1994 pile photo.\n')
    f.write('\nE. Watermarked (Mac + Miller, 5 sets): every product image on their store is watermarked, no clean alternative; kept.\n')
with open(os.path.join(OUT, 'mat_fixes.txt'), 'w') as f:
    f.write('Mat fixes from the Oct 20 mat audit (scratchpad/mat-audit/report.csv)\n\nHIDDEN (hid=true):\n')
    herm2 = {x[0] for s in D['sets'] if s.get('album') or s.get('sb') for x in s['m']}
    for mid, n, bn, why in rep['mats']['hidden']: f.write(f"  {n} ({bn}) [{mid}]{'  ** in a Tiffany album list: needs a real photo **' if mid in herm2 else ''}: {why}\n")
    f.write('\nIMAGE TAKEN FROM DUPLICATE LISTING:\n'); [f.write(f"  {n} [{a}] <- {b}\n") for a, n, b in rep['mats']['image_from_twin']]
    f.write('\nBRAND SPELLING:\n'); [f.write(f"  {a}: {b}\n") for a, b in rep['mats']['brand']]
    f.write('\nRETIRED FLAG SET (name says retired):\n'); [f.write(f"  {n}\n") for n in rep['retired_flagged']]
    f.write("\nTIFFANY COLOUR CALLS APPLIED (mf old -> new):\n"); [f.write(f"  {n}: {a} -> {b}\n") for _, n, a, b in rep['mats']['color']]
    f.write('\nRENAMED (raw store titles):\n'); [f.write(f"  {a} -> {b}\n") for _, a, b in rep['mats']['renamed']]
print('flags', len(tf), 'locks tiles', len(locks['tiles']), 'sets', len(locks['sets']), 'mats', len(locks['mats']))
