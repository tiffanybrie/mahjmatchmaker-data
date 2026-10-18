"""Real rack photos for album cards and mat cards (Tiffany, Oct 15: "Still has rendered OMM ...").
Builds assets/racks/card/<key>.png: one REAL rack photo per approved rack name, background removed,
levelled (long axis horizontal; the card template does the angling) and trimmed. index.json maps the
approved rack name (config/tile-racks-picks.json final_lists spelling) -> file + source.

Sources (doc 48 Rack Rules):
- Oh My Mahjong: OMM's own single-rack + pusher product photo, assets/racks/omm/<rack>.jpg (rembg cut-out).
- Peace Love Mahjong: the real per-colour rack cut-outs from PLM's colour photo (Oct 9, /tmp/mb/plm/r_<Color>.png).
- Bam Bird Boutique Walnut: Bam Bird's product photo, single rack cut out (/tmp/mb/rkalt/walnut.png).
- Middle & Main / Miss Mahjong / Mahjong Row & Co.: Tiffany's rack cut-outs, assets/racks/cutouts/<key>-1.png
  (horizontal); Chestnut Cream only has the angled -2.
- Mahjong Row & Co. Scalloped Tortoise: the front rack of MR&C's product photo (assets/racks/mrc-scalloped-tortoise.png).
- Bird & Bamboo is NOT here: per doc 48 it is the one rack we generate (builder/bbrack.py recolor of the real
  B&B blank, saved as assets/racks/card/bb-blank.png).
Usage: python3 scripts/albumcard/real_racks.py   (re-run only to add racks; outputs are committed)"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
R = '/home/claude/mahjmatchmaker-data/'
OUT = R + 'assets/racks/card/'
CUT = R + 'assets/racks/cutouts/'
OMM = R + 'assets/racks/omm/'
SRC = {
 # approved name: (kind, path)
 'Oh My Mahjong White Acrylic': ('omm', OMM + 'white.jpg'),
 'Oh My Mahjong Tortoise Shell': ('omm', OMM + 'tortoise-shell.jpg'),
 'Oh My Mahjong Pink Quartz': ('omm', OMM + 'pink-quartz.jpg'),
 'Oh My Mahjong Hot Pink': ('omm', OMM + 'hot-pink.jpg'),
 'Oh My Mahjong Burl': ('omm', OMM + 'burl.jpg'),
 'Peace Love Mahjong Pink': ('flat', '/tmp/mb/plm/r_Pink.png'),
 'Peace Love Mahjong Oak': ('flat', '/tmp/mb/plm/r_Oak.png'),
 'Peace Love Mahjong Chartreuse': ('flat', '/tmp/mb/plm/r_Chartreuse.png'),
 'Peace Love Mahjong Dark Green': ('flat', '/tmp/mb/plm/r_Dark_Green.png'),
 'Peace Love Mahjong Light Pink': ('flat', '/tmp/mb/plm/r_Light_Pink.png'),
 'Peace Love Mahjong Red': ('flat', '/tmp/mb/plm/r_Red.png'),
 'Peace Love Mahjong Navy': ('flat', '/tmp/mb/plm/r_Navy.png'),
 'Peace Love Mahjong White': ('flat', '/tmp/mb/plm/r_White.png'),
 'Peace Love Mahjong Acrylic Burl': ('flat', CUT + 'peace-love-mahjong-acrylic-burl.png'),  # Oct 18: PLM shop photo, white bg removed
 'Middle & Main Milk Glass Scalloped Acrylic': ('cut', CUT + 'middle-and-main-milk-glass-2.png'),
 'Bam Bird Boutique Walnut': ('flat', '/tmp/mb/rkalt/walnut.png'),
 'Middle & Main Hawksbill Heritage Tortoise': ('cut', CUT + 'middle-and-main-hawksbill-tortoise-1.png'),
 'Middle & Main Hawksbill Tortoise': ('same', 'Middle & Main Hawksbill Heritage Tortoise'),
 'Middle & Main Scalloped Beechwood': ('cut', CUT + 'middle-and-main-scalloped-beechwood-1.png'),
 'Miss Mahjong Scalloped Iridescent Opal': ('cut', CUT + 'miss-mahjong-iridescent-opal-scalloped-1.png'),
 'Miss Mahjong Iridescent Opal Scalloped': ('same', 'Miss Mahjong Scalloped Iridescent Opal'),
 'Miss Mahjong Peach Sorbet Scalloped': ('cut', CUT + 'miss-mahjong-peach-sorbet-scalloped-1.png'),
 'Miss Mahjong Cornflower Blue Scalloped': ('cut', CUT + 'miss-mahjong-cornflower-blue-scalloped-1.png'),
 'Miss Mahjong Opal & Brass': ('cut', CUT + 'miss-mahjong-opal-and-brass-1.png'),
 'Miss Mahjong Jade & Brass': ('cut', CUT + 'miss-mahjong-jade-and-brass-1.png'),
 'Miss Mahjong Brass & Tortoise': ('cut', CUT + 'miss-mahjong-brass-and-tortoise-1.png'),
 'Mahjong Row & Co. Matcha Green': ('cut', CUT + 'mahjong-row-and-co-matcha-green-1.png'),
 'Mahjong Row & Co. Chestnut Cream': ('cut', CUT + 'mahjong-row-and-co-chestnut-cream-2.png'),
 'Mahjong Row & Co. Scalloped Tortoise': ('front', R + 'assets/racks/mrc-scalloped-tortoise.png'),
}
MISSING = {
 "Tigre de Tartán Oxblood Scallop": "not listed in Tigre's shop (checked Oct 18), so no product photo. Oxblood cards use B&B Wine + PLM Acrylic Burl for now. oxblood: swap to her own photo when she sends it.",
 "Sunday Mahjong Candy Blue / Tortoise / Blonde Tortoise / Clear": "same problem as Cola: no clean single-rack shot in Sunday's listings. Mat side only once photographed."
}  # Oct 18: kept in sync with index.json "missing"

def slug(n): return ''.join(c if c.isalnum() else '-' for c in n.lower()).replace('--', '-').strip('-')

def level(im):
    """rotate so the rack's long axis is horizontal (no skew/stretch), then trim"""
    a = np.asarray(im)[..., 3] > 60
    ys, xs = np.nonzero(a); p = np.stack([xs, ys], 1).astype(float); p -= p.mean(0)
    ev, evec = np.linalg.eigh(np.cov(p.T)); v = evec[:, ev.argmax()]
    ang = np.degrees(np.arctan2(v[1], v[0]))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    if abs(ang) > 0.4: im = im.rotate(ang, resample=Image.BICUBIC, expand=True)
    return im.crop(im.getbbox())

def rack_band(im):
    """OMM photo = rack + its pusher (doc 48). Level on the rack's straight bottom edge; return (img, rack band
    height as a fraction of the image height) so cards size the RACK like the others and let the pusher overhang."""
    for _ in range(3):
        a = np.asarray(im)[..., 3] > 100; cols = np.nonzero(a.any(0))[0]; c0, c1 = cols[0], cols[-1]; w = c1 - c0
        xs = np.arange(int(c0 + w * .2), int(c0 + w * .8)); bot = np.array([a.shape[0] - 1 - np.argmax(a[::-1, x]) for x in xs])
        d = np.degrees(np.arctan(np.polyfit(xs, bot, 1)[0]))
        if abs(d) < 0.2: break
        im = im.rotate(d, resample=Image.BICUBIC, expand=True); im = im.crop(im.getbbox())
    a = np.asarray(im)[..., 3] > 100; H = a.shape[0]; runs = []
    for x in range(int(a.shape[1] * .3), int(a.shape[1] * .7)):
        col = a[::-1, x]; b = np.argmax(col)
        if not col.any(): continue
        L = np.argmax(~col[b:]) if (~col[b:]).any() else H - b; runs.append(L)
    return im, float(np.median(runs)) / H

def build(name, kind, path):
    if kind == 'omm':
        from rembg import new_session, remove
        global _S
        if '_S' not in globals(): _S = new_session('isnet-general-use')
        src = Image.open(path).convert('RGB'); src.thumbnail((1800, 1800))
        im = remove(src, session=_S).convert('RGBA')
        a = np.asarray(im)[..., 3] > 60; lab, n = ndi.label(a)
        if n > 1:  # keep rack + pusher, drop specks
            sz = ndi.sum(a, lab, range(1, n + 1)); keep = np.isin(lab, [i + 1 for i, s in enumerate(sz) if s > 0.05 * sz.max()])
            arr = np.asarray(im).copy(); arr[..., 3] = np.where(keep, arr[..., 3], 0); im = Image.fromarray(arr, 'RGBA')
        im, frac = rack_band(level(im))
        if im.width > 1400: im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        return im, frac
    elif kind == 'front':
        im = Image.open(path).convert('RGBA'); a = np.asarray(im)[..., 3] > 40; lab, n = ndi.label(a)
        sz = ndi.sum(a, lab, range(1, n + 1)); k = 1 + int(np.argmax(sz))  # largest = front rack, fully visible
        arr = np.asarray(im).copy(); arr[..., 3] = np.where(lab == k, arr[..., 3], 0)
        im = level(Image.fromarray(arr, 'RGBA'))
    elif kind == 'cut':
        im = level(Image.open(path).convert('RGBA'))
    else:  # flat: already a level single-rack cut-out
        im = Image.open(path).convert('RGBA'); im = im.crop(im.getbbox())
    if im.width > 1400: im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    return im, 1.0

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    idx = {'_note': __doc__.split('\n')[0] + ' Real photos only; B&B = generated (doc 48). Missing racks listed under "missing".', 'racks': {}, 'missing': MISSING}
    old = json.load(open(OUT + 'index.json')) if os.path.exists(OUT + 'index.json') else {'racks': {}}
    for name, (kind, path) in SRC.items():
        if kind == 'same': continue
        f = slug(name) + '.png'
        frac = old['racks'].get(name, {}).get('rack_frac', 1.0)
        if os.path.exists(path):
            im, frac = build(name, kind, path); im.save(OUT + f, optimize=True)
        elif not os.path.exists(OUT + f):
            print('SKIP (no source):', name); continue
        idx['racks'][name] = {'file': 'assets/racks/card/' + f, 'source': path.replace(R, ''), 'kind': kind, 'rack_frac': round(frac, 3)}
    for name, (kind, path) in SRC.items():
        if kind == 'same' and path in idx['racks']: idx['racks'][name] = dict(idx['racks'][path], alias_of=path)
    for name, v in old['racks'].items():  # Oct 18: keep approved renders (Sunday Mahjong Cola) that have no source photo
        if v.get('kind') == 'render' and name not in idx['racks']: idx['racks'][name] = v
    if os.path.exists('/tmp/mb/bb_blank.png'): Image.open('/tmp/mb/bb_blank.png').save(OUT + 'bb-blank.png', optimize=True)
    json.dump(idx, open(OUT + 'index.json', 'w'), indent=1, ensure_ascii=False)
    print(len(idx['racks']), 'racks ->', OUT)
