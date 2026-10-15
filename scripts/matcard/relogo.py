"""Swap the top logo on finished Mat Edit cards for the big no-tagline wordmark (Tiffany, Oct 15 6:50pm, Vivienne:
"the logo tagline text is too small to read"). The cards are the reviewed set (rack box re-drawn by rackpanel.py),
so this patches the PNGs in place instead of re-rendering: the old wordmark + tiny tagline block is found as the first
non-background band at the top, painted over with the card background, and assets/brand/mahjmatchmaker-wordmark-notag.png
is pasted centred in that band at full band height (about 2x the old letter size). matcard.py now uses the same logo.
Usage: python3 scripts/matcard/relogo.py card.png [...]   (writes in place)"""
import sys
import numpy as np
from PIL import Image
LOGO = Image.open(__file__.rsplit('/scripts/', 1)[0] + '/assets/brand/mahjmatchmaker-wordmark-notag.png').convert('RGBA')
def runs(rows):
    out = []; s = p = rows[0]
    for r in rows[1:]:
        if r != p + 1: out.append((s, p)); s = r
        p = r
    return out + [(s, p)]
for f in sys.argv[1:]:
    im = Image.open(f).convert('RGB'); a = np.asarray(im).astype(int); bg = tuple(a[5, 5])
    d = np.abs(a - np.array(bg)).sum(2) > 40
    rr = runs(list(np.nonzero(d.any(1))[0]))
    y0, y1 = rr[0][0], rr[1][1]  # wordmark + tagline bar
    cols = np.nonzero(d[y0:y1 + 1].any(0))[0]; x0, x1 = cols[0], cols[-1]
    nxt = rr[2][0]  # next element (THE MAT EDIT line): keep a gap above it
    im.paste(bg, (x0 - 4, y0 - 4, x1 + 5, y1 + 5))
    h = min(nxt - 14, y1 + 8) - (y0 - 6); lg = LOGO.copy(); lg = lg.resize((round(lg.width * h / lg.height), h), Image.LANCZOS)
    im.paste(lg, ((im.width - lg.width) // 2, y0 - 6), lg)
    im.save(f, optimize=True); print(f, 'logo', lg.size)
