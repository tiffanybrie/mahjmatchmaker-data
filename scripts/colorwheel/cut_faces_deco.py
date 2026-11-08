"""Bam Bird Boutique Deco clean face cutouts (Nov 7). All Deco colourways share the same faces (Tiffany Oct 25 9:41pm), so
one set serves Lagoon, Mulberry and Indigo. Source: Bam Bird's Deco listing image 16 (BamBird_Deco-15-2.jpg, 4000x6000):
the faces in the lucite box, 4 rows x 10, shot from straight above (assets/launches/bambird-deco-tile-set/16-src-FULL.jpg
is not kept in the repo; pass the downloaded file). Grid lines are found from the dark seams between tiles, then each tile
gets a rounded-corner alpha mask. Output: assets/tiles/faces/deco/clean/<name>.png
Usage: python3 scripts/colorwheel/cut_faces_deco.py <BamBird_Deco-15-2.jpg>"""
import numpy as np, os, sys
from PIL import Image, ImageDraw
R = '/home/claude/mahjmatchmaker-data/'
im = Image.open(sys.argv[1]).convert('RGB'); a = np.asarray(im.convert('L')).astype(float)
OUT = R + 'assets/tiles/faces/deco/clean/'; os.makedirs(OUT, exist_ok=True)
X0, PX, Y0, PY = 300 + 2 * 103, 2 * 141.6, 2250 + 2 * 38, 2 * 197.2
def refine(prof, g, win=26):
    lo, hi = int(g - win), int(g + win); return lo + int(np.argmin(prof[lo:hi]))
# seam guesses read off the photo (display x 0.5 + offset), refined in a small window, per row for the columns
GX = [506, 790, 1074, 1356, 1640, 1924, 2206, 2490, 2774, 3056, 3340]
GY = [2330, 2722, 3114, 3510, 3906]
rowprof = np.median(a[:, 560:3000], axis=1)
ys = [GY[0]] + [refine(rowprof, g, 12) for g in GY[1:-1]] + [GY[-1]]
XS = []
for j in range(4):
    cp = np.median(a[ys[j] + 40:ys[j + 1] - 40, :], axis=0)
    XS.append([refine(cp, g, 12) for g in GX])
print('y', ys); [print('x', r) for r in XS]
NAMES = [[f'dot-{i}' for i in range(1, 10)] + ['dragon-white'],
         ['bam-1-crane'] + [f'bam-{i}' for i in range(2, 10)] + ['dragon-green'],
         [f'crak-{i}' for i in range(1, 10)] + ['dragon-red'],
         ['flower-iris-navy', 'flower-iris-gold', 'flower-poppy', 'flower-lily', 'wind-north', 'wind-east', 'wind-west', 'wind-south', 'joker-teal-lion', 'joker-rose-lion']]
INSET, RAD = 7, 26
def mask(w, h):
    s = 4; m = Image.new('L', (w * s, h * s), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * s - 1, h * s - 1], RAD * s, fill=255); return m.resize((w, h), Image.LANCZOS)
n = 0
for j, row in enumerate(NAMES):
    for i, nm in enumerate(row):
        xs = XS[j]; box = (xs[i] + INSET, ys[j] + INSET, xs[i + 1] - INSET + 1, ys[j + 1] - INSET + 1)
        t = im.crop(box).convert('RGBA'); t.putalpha(mask(*t.size)); t.save(OUT + nm + '.png'); n += 1
print(n, 'tiles ->', OUT)
