"""Nov 6 (Tiffany, Juniper round-3 note 5: the OMM White Acrylic card rack was a "photoshop hack job"):
the Oct 15 rembg cut of OMM's white-on-white product photo (assets/racks/omm/white.jpg) dropped big parts of the
white rack body to transparent, so the card background showed through as dark smears.
Clean cut: rembg mask -> holes filled + small gaps closed (the white body becomes solid), the open gap between
the pusher arm and the rack stays transparent, a 1px feathered edge, then the same level + rack_band as real_racks.py.
Writes assets/racks/card/oh-my-mahjong-white-acrylic.png + updates its index.json rack_frac.
Check sheet: on white AND navy (CLAUDE.md 6b) -> argv[1] if given."""
import sys, os, json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'scripts/albumcard')
import real_racks as RR
from rembg import new_session, remove
src = Image.open(R + 'assets/racks/omm/white.jpg').convert('RGB'); src.thumbnail((1800, 1800))
im = remove(src, session=new_session('isnet-general-use')).convert('RGBA')
a = np.asarray(im)[..., 3] > 40
lab, n = ndi.label(a); sz = ndi.sum(a, lab, range(1, n + 1)); a = np.isin(lab, [i + 1 for i, s in enumerate(sz) if s > 0.05 * sz.max()])
a = ndi.binary_closing(a, structure=np.ones((5, 5)), iterations=2)
a = ndi.binary_fill_holes(a)
a = ndi.binary_opening(a, structure=np.ones((3, 3)))
alpha = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
out = src.convert('RGBA'); out.putalpha(alpha)
out = RR.level(out); out, _ = RR.rack_band(out)
# rembg also dropped the white top of the trough's back wall on the left (white on white): rebuild the trough as one solid
# band between its straight top edge (fitted where the cut is good, right 40%) and its bottom edge, from its left end.
A = np.asarray(out).copy(); al = A[..., 3] > 100; Hh, Ww = al.shape
def run(x):
    col = al[::-1, x]
    if not col.any(): return None
    b = int(np.argmax(col)); L = int(np.argmax(~col[b:])) if (~col[b:]).any() else Hh - b
    return Hh - 1 - b, L  # (bottom y, run length)
xs = np.arange(int(Ww * .6), int(Ww * .95)); tops = []
for x in xs:
    r = run(x); tops.append(r[0] - r[1] + 1)
m, b0 = np.polyfit(xs, tops, 1); med = np.median([run(x)[1] for x in xs])
xl = next(x for x in range(Ww) if run(x) and run(x)[1] >= .6 * med)
for x in range(xl, int(Ww * .6)):
    r = run(x)
    if not r: continue
    y0 = int(round(m * x + b0)); x2 = int(Ww * .7); dy = int(round(m * (x2 - x)))
    for y in range(y0, r[0] + 1):
        if A[y, x, 3] < 200: A[y, x, :3] = A[min(Hh - 1, y + dy), x2, :3]  # same spot further along the (uniform) trough
        A[y, x, 3] = 255
out = Image.fromarray(A, 'RGBA')
a2 = np.asarray(out)[..., 3] > 100; frac = float(med) / Hh
if out.width > 1400: out = out.resize((1400, round(out.height * 1400 / out.width)), Image.LANCZOS)
f = R + 'assets/racks/card/oh-my-mahjong-white-acrylic.png'; out.save(f, optimize=True)
idx = json.load(open(R + 'assets/racks/card/index.json'))
idx['racks']['Oh My Mahjong White Acrylic'].update({'rack_frac': round(frac, 3), 'built_by': 'scripts/albumcard/nov06/omm_white_recut.py',
    'note': 'Nov 6: clean recut (holes filled) after Tiffany called the Oct 15 cut a photoshop hack job; looked at on white + navy'})
json.dump(idx, open(R + 'assets/racks/card/index.json', 'w'), indent=1, ensure_ascii=False)
print(f, out.size, 'frac', round(frac, 3))
if len(sys.argv) > 1:
    W = out.width + 80; sh = Image.new('RGB', (W, out.height * 2 + 120), 'white')
    sh.paste((5, 40, 90), (0, out.height + 60, W, out.height * 2 + 120))
    sh.paste(out, (40, 30), out); sh.paste(out, (40, out.height + 90), out); sh.save(sys.argv[1])
