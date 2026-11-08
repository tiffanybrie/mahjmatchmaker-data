"""Juniper clean face cutouts (Nov 6) from Oh My Mahjong's flat lay (product image 1 of
ohmymahjong.com/products/juniper-mahjong-tiles.json = assets/launches/omm-juniper-mahjong-tiles/01-Tile_Juniper_A.jpg).
The flat lay is a 10 x 5 grid of butted tiles separated by a 1-2px shadow line. We find each line exactly (column /
row median darkness inside a search window), crop just inside it, and give the tile a rounded-corner alpha mask:
no white frame, no shadow. Output: assets/tiles/faces/juniper/clean/<name>.png
Usage: python3 scripts/colorwheel/cut_faces_juniper.py [name ...]
Nov 7: checked every OMM Juniper image (tiles, starter kit, ultimate kit; retailers carry none). The flat lay is the
ONLY straight-on shot of all faces and its master is 3185x3982 (~266 px per tile); the 2048px corner close-up is angled
with depth-of-field blur, so these ~256x351 cutouts are the sharpest true source. No upscaling."""
import numpy as np, os
from PIL import Image, ImageDraw
R = '/home/claude/mahjmatchmaker-data/'
SRC = R + 'assets/launches/omm-juniper-mahjong-tiles/01-Tile_Juniper_A.jpg'
OUT = R + 'assets/tiles/faces/juniper/clean/'; os.makedirs(OUT, exist_ok=True)
im = Image.open(SRC).convert('RGB'); a = np.asarray(im.convert('L')).astype(float)
X0, Y0, PX, PY = 178, 1179, 266.6, 358.4
def refine(prof, guess, win=22):
    lo, hi = int(guess - win), int(guess + win); seg = prof[lo:hi]
    return lo + int(np.argmin(seg))
def outer(prof, guess, side, win=30):
    """outer edge against the pure-white background: first index where the tile (<249) starts"""
    lo, hi = int(guess - win), int(guess + win); seg = prof[lo:hi]
    idx = np.where(seg < 249)[0]
    return lo + (idx[0] if side == 'start' else idx[-1])
# vertical lines: median over the middle of rows 1-3 (all 10 columns full there)
colprof = np.median(a[int(Y0 + 40):int(Y0 + 3 * PY - 40), :], axis=0)
xs = [outer(colprof, X0, 'start')] + [refine(colprof, X0 + i * PX) for i in range(1, 10)] + [outer(colprof, X0 + 10 * PX, 'end')]
rowprof = np.median(a[:, int(X0 + 40):int(X0 + 9 * PX - 40)], axis=1)
ys = [outer(rowprof, Y0, 'start')] + [refine(rowprof, Y0 + j * PY) for j in range(1, 5)] + [outer(rowprof, Y0 + 5 * PY, 'end')]
print('x lines', xs); print('y lines', ys)
NAMES = [
 ['dot-1', 'dot-2', 'dot-3', 'dot-4', 'dot-5', 'dot-6', 'dot-7', 'dot-8', 'dot-9', 'dragon-white-pagoda'],
 ['bam-1-peacock', 'bam-2', 'bam-3', 'bam-4', 'bam-5', 'bam-6', 'bam-7', 'bam-8', 'bam-9', 'dragon-green'],
 ['crak-1', 'crak-2', 'crak-3', 'crak-4', 'crak-5', 'crak-6', 'crak-7', 'crak-8', 'crak-9', 'dragon-red'],
 ['flower-1a', 'flower-1b', 'flower-2a', 'flower-2b', 'flower-3a', 'flower-3b', 'flower-4a', 'flower-4b', None, None],
 ['wind-north', 'wind-east', 'wind-west', 'wind-south', 'joker-1', 'joker-2', 'joker-3', 'joker-4', 'joker-5', None],
]
INSET = 5; RAD = 22
# per-tile extra inset (left, top, right, bottom): Nov 7 bam-1-peacock top edge carried a sliver of the shadow line
EXTRA = {'bam-1-peacock': (0, 3, 0, 0)}
import sys
ONLY = set(sys.argv[1:])  # optional: cut only these names
def mask(w, h):
    s = 4; m = Image.new('L', (w * s, h * s), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * s - 1, h * s - 1], RAD * s, fill=255)
    return m.resize((w, h), Image.LANCZOS)
n = 0
for j, row in enumerate(NAMES):
    for i, nm in enumerate(row):
        if not nm or (ONLY and nm not in ONLY): continue
        el, et, er, eb = EXTRA.get(nm, (0, 0, 0, 0))
        bot = 12 if j == 4 else INSET  # bottom row: the outer edge shows a sliver of the green layers
        box = (xs[i] + INSET + el, ys[j] + INSET + et, xs[i + 1] - INSET + 1 - er, ys[j + 1] - bot + 1 - eb)
        t = im.crop(box).convert('RGBA'); t.putalpha(mask(*t.size)); t.save(OUT + nm + '.png'); n += 1
print(n, 'tiles ->', OUT)
