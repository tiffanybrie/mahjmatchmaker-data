"""Textured-back patch sheets (Tiffany Nov 20 2026 8:53am: Bam Bird Tortoise walls 'just look brown'; they are amber with black blotches).
The Table view wall draws each wall tile from a random 60% window of the set's patch (D.tv.backs[slug].p). A patch cut from ONE small
back (24x56 px for Tortoise) turns to a brown blur. This builds the patch as a 2x2 SHEET of four different REAL backs from the brand's
own photo, feather-blended so no seam shows: a 60% window is then about 1.2 real tiles wide, so the pattern keeps its real scale and
every wall tile looks different. Real photo pixels only; nothing drawn or recoloured.
usage: python3 builder/table_view/patch_sheet_nov20.py <slug> <photo> x0,y0,x1,y1[,r] x4  (r = rotate 90 for a landscape crop)"""
import sys, numpy as np
from PIL import Image, ImageFilter
R = __file__.rsplit('/builder/', 1)[0] + '/'
def sheet(photo, boxes, tw=150, th=200, ov=50, inset=7):
    im = Image.open(photo).convert('RGB'); tiles = []
    for b in boxes:
        c = im.crop((b[0] + inset, b[1] + inset, b[2] - inset, b[3] - inset))
        if len(b) > 4 and b[4]: c = c.rotate(90, expand=True)
        tiles.append(c.resize((tw + ov, th + ov), Image.LANCZOS))
    W, H = 2 * tw, 2 * th
    acc = np.zeros((H, W, 3)); wsum = np.zeros((H, W, 1))
    m = Image.new('L', (tw + ov, th + ov), 0); m.paste(255, (ov // 2, ov // 2, tw + ov // 2, th + ov // 2)); m = np.asarray(m.filter(ImageFilter.GaussianBlur(ov / 4.0)), float)[..., None] / 255 + 1e-4
    for i, t in enumerate(tiles):
        ox, oy = (i % 2) * tw - ov // 2, (i // 2) * th - ov // 2
        for dx in (-W, 0, W):
            for dy in (-H, 0, H):   # wrap so the sheet edges blend too
                x0, y0 = ox + dx, oy + dy; a0, b0 = max(0, x0), max(0, y0); a1, b1 = min(W, x0 + tw + ov), min(H, y0 + th + ov)
                if a1 <= a0 or b1 <= b0: continue
                sl = (slice(b0 - y0, b1 - y0), slice(a0 - x0, a1 - x0))
                acc[b0:b1, a0:a1] += np.asarray(t, float)[sl] * m[sl]; wsum[b0:b1, a0:a1] += m[sl]
    return Image.fromarray((acc / wsum).clip(0, 255).astype(np.uint8))
if __name__ == '__main__':
    slug, photo = sys.argv[1:3]; boxes = [[int(float(x)) for x in a.split(',')] for a in sys.argv[3:7]]
    s = sheet(R + photo if not photo.startswith('/') else photo, boxes); out = R + f'assets/table-view/backs/{slug}.webp'; s.save(out, 'WEBP', quality=84)
    import os; print(slug, s.size, os.path.getsize(out), 'bytes')
