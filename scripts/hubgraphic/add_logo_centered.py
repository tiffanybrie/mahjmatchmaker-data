"""Like add_logo.py, but lays the logos on a COLS-wide grid with the last row centred (Oct 29, 2026: Maison Mahj, 37 logos).
Usage: python3 add_logo_centered.py <current.jpg> <old cols> <old rows> <n old logos> <new cols> <out.jpg> <new_logo.png> [...]"""
import sys, math
from PIL import Image
sys.argv = sys.argv[:]
SRC, OC, OR, NOLD, NC, OUT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
NEW = sys.argv[7:]
import importlib.util, os
spec = importlib.util.spec_from_file_location('al', os.path.join(os.path.dirname(__file__), 'add_logo.py'))
# reuse helpers without running add_logo's main: copy them here
from PIL import ImageChops
import numpy as np
base = Image.open(SRC).convert('RGB').resize((1080, 1350)); CREAM = base.getpixel((540, 190))
x0, y0, x1, y1 = 78, 222, 1002, 1222
def trim_cream(im):
    diff = ImageChops.difference(im, Image.new('RGB', im.size, CREAM)).convert('L').point(lambda v: 255 if v > 28 else 0)
    bb = diff.getbbox(); im = im.crop(bb) if bb else im
    a = np.array(im).astype(int); dist = np.abs(a - np.array(CREAM)).sum(-1)
    alpha = np.clip((dist - 12) * 6, 0, 255).astype('uint8')
    return Image.fromarray(np.dstack([a.astype('uint8'), alpha]), 'RGBA')
def knock(im):
    im = im.convert('RGBA'); a = np.array(im).astype(int)
    if a[..., 3].min() < 250: return im.crop(im.getbbox())
    a[..., 3] = np.where(a[..., :3].min(-1) > 238, 0, 255); im = Image.fromarray(a.astype('uint8'), 'RGBA'); return im.crop(im.getbbox())
cw, ch = (x1 - x0) / OC, (y1 - y0) / OR; logos = []
for i in range(NOLD):
    cx, cy = x0 + (i % OC) * cw, y0 + (i // OC) * ch
    logos.append(trim_cream(base.crop((int(cx + 4), int(cy + 4), int(cx + cw - 4), int(cy + ch - 4)))))
logos += [knock(Image.open(p)) for p in NEW]
n = len(logos); cols = NC; rows = math.ceil(n / cols)
c = base.copy(); c.paste(Image.new('RGB', (x1 - x0, y1 - y0), CREAM), (x0, y0))
cw, ch = (x1 - x0) / cols, (y1 - y0) / rows
for i, im in enumerate(logos):
    r, k = divmod(i, cols); inrow = min(cols, n - r * cols); off = (cols - inrow) * cw / 2
    bw, bh = cw - 18, ch - 26; s = min(bw / im.width, bh / im.height, 1.6)
    im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    cx = x0 + off + k * cw + cw / 2; cy = y0 + r * ch + ch / 2
    c.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)
c.save(OUT, quality=92); print('ok', n, 'logos', cols, 'x', rows)
