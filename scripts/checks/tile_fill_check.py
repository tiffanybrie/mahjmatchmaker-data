"""Tile-inset fill check (Tiffany Nov 9 1:43am: Virora tile insets showed the tiles shrunk inside a white box with about a
tile-width of white margin on every side; "when I matched these the tiles FILLED the inset rectangle").
The card inset (card2.html #tile, 422x526, object-fit: cover) must show tiles edge to edge: after the cover crop to the
inset aspect, no side may carry a white/near-white band thicker than 3% of that side.
  band(im)            -> {'top','bottom','left','right'} band fractions of the cover-cropped inset
  problem(path)       -> None or a reason string (used by gen2.py, which REFUSES a card whose tile file fails)
  fill_crop(im)       -> trims the white border and cover-crops to the inset aspect (used to make *-fill tile files)
CREAM margin (Nov 9 QA, Apres Ski #01-#08): a photo shot on an off-white/cream backdrop (232-237, below the pure-white
cut) left a ~9% left / ~12% top margin that the white test missed. The visible TOP and LEFT edges of the inset (right =
card edge, bottom = navy box) are also tested with a cream definition (all channels >= 215, chroma <= 18, >= 95% of the
row) and may carry at most CREAM_MAX (5%); scattered piles on white (Dear Santa fill 4.3%) pass.
Loose tile modes (tile_mode 'loose', transparent cut-outs) are exempt: they are drawn without a box.
CLI: python3 scripts/checks/tile_fill_check.py [files...]  (default: every tile file the live/staged card builds use)
Exit 1 on any failure."""
import sys, os, glob, json
import numpy as np
from PIL import Image, ImageFilter
R = '/home/claude/mahjmatchmaker-data/'
AR = 422 / 526          # card2.html #tile box
MAXBAND = 0.03
CREAM_MAX = 0.05
def _cover(im):
    w, h = im.size
    if w / h > AR: nw = int(h * AR); return im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    nh = int(w / AR); return im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
def _white_rows(a):  # a: HxWx3 float; a row is "white" when >=97% of its pixels are near-white (all channels >= 232, low chroma)
    wht = (a.min(axis=2) >= 232) & ((a.max(axis=2) - a.min(axis=2)) <= 14)
    return wht.mean(axis=1) >= 0.97
def _run(flags):
    n = 0
    for f in flags:
        if not f: break
        n += 1
    return n
def band(im):
    im = im.convert('RGB'); im = _cover(im); im.thumbnail((400, 400))
    a = np.asarray(im.filter(ImageFilter.MedianFilter(3)), dtype=np.int16)
    rows = _white_rows(a); cols = _white_rows(a.transpose(1, 0, 2))
    h, w = rows.size, cols.size
    return {'top': _run(rows) / h, 'bottom': _run(rows[::-1]) / h, 'left': _run(cols) / w, 'right': _run(cols[::-1]) / w}
def _cream_rows(a):
    c = (a.min(axis=2) >= 215) & ((a.max(axis=2) - a.min(axis=2)) <= 18)
    return c.mean(axis=1) >= 0.95
def cream(im):
    im = im.convert('RGB'); im = _cover(im); im.thumbnail((400, 400))
    a = np.asarray(im.filter(ImageFilter.MedianFilter(3)), dtype=np.int16)
    rows = _cream_rows(a); cols = _cream_rows(a.transpose(1, 0, 2))
    return {'top': _run(rows) / rows.size, 'left': _run(cols) / cols.size}
def problem(path):
    p = path if os.path.isabs(path) else R + path
    im = Image.open(p)
    if im.mode in ('RGBA', 'LA') and np.asarray(im.split()[-1]).min() < 250: return None  # transparent cut-out (loose mode)
    b = band(im)
    bad = {k: round(v * 100, 1) for k, v in b.items() if v > MAXBAND}
    bad.update({f'{k} (cream)': round(v * 100, 1) for k, v in cream(im).items() if v > CREAM_MAX})
    return f'tile inset has a white border band ({", ".join(f"{k} {v}%" for k, v in bad.items())}; max {MAXBAND*100:.0f}%): use a filled crop (tile_fill_check.fill_crop)' if bad else None
def fill_crop(im, grow=0.0, box=None):
    """Bounding box of the tile ART (coloured or dark pixels: faces, engraving, coloured backs), grown by `grow` x its size
    (to take in the ivory tile edges), then the cover crop to the inset aspect. Soft grey shadows and the white/ivory
    backdrop are not content. box=(x0,y0,x1,y1) skips detection (a hand-picked close-up, e.g. Petalee's grid)."""
    im = im.convert('RGB')
    if box is None:
        a = np.asarray(im.filter(ImageFilter.MedianFilter(5)), dtype=np.int16)
        art = ((a.max(axis=2) - a.min(axis=2)) > 45) | (a.min(axis=2) < 150)
        ys = np.where(art.mean(axis=1) > 0.01)[0]; xs = np.where(art.mean(axis=0) > 0.01)[0]
        x0, y0, x1, y1 = xs[0], ys[0], xs[-1] + 1, ys[-1] + 1
        gx, gy = (x1 - x0) * grow, (y1 - y0) * grow
        box = (max(0, int(x0 - gx)), max(0, int(y0 - gy)), min(im.width, int(x1 + gx)), min(im.height, int(y1 + gy)))
    return _cover(im.crop(box))
def default_files():
    fs = set()
    idx = json.load(open(R + 'assets/tiles/album/index.json'))
    for v in idx.values():
        if isinstance(v, dict) and v.get('file') and v.get('tile_mode') != 'loose': fs.add(v['file'])
    fs |= {f[len(R):] for f in glob.glob(R + 'assets/tiles/holiday/*') if f.endswith(('.jpg', '.png'))}
    lk = R + 'config/tile-fill-locks.json'
    if os.path.exists(lk): fs |= {v for v in json.load(open(lk))['files'].values()}
    return sorted(f for f in fs if os.path.exists(R + f))
if __name__ == '__main__':
    fs = sys.argv[1:] or default_files()
    lk = json.load(open(R + 'config/tile-fill-locks.json'))['files'] if os.path.exists(R + 'config/tile-fill-locks.json') else {}
    bad = []
    for f in fs:
        if f in lk: continue  # replaced by its locked filled crop (gen2 swaps it in)
        try: p = problem(f)
        except Exception as e: p = f'unreadable: {e}'
        if p: bad.append((f, p))
    print(f'TILE FILL CHECK {"FAIL" if bad else "PASS"}: {len(fs)} tile files, {len(bad)} with a white border band')
    for f, p in bad: print('  FAIL', f, '-', p)
    sys.exit(1 if bad else 0)
