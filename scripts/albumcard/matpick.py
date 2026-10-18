"""Claude's mat-match picks (upper-right MATCH THE MAT group) when Tiffany asks Claude to pick them
(Oct 15 evening: "You will pick the mat matches for me" for Sunday Tile Set; vault Lilac Soiree).
Picks 1-2 Bird & Bamboo colours (work/bbracks.json palette) nearest (CIEDE2000) to the mat's main colours:
k-means on the mat photo (white background dropped), clusters by size; the 1st pick = nearest B&B to the
strongest coloured cluster (size x chroma; neutrals only for an all-neutral mat), a 2nd pick only if another
coloured cluster maps to a clearly different B&B colour. Metallics, Clear and anything already used as a tile rack are skipped.
Usage: from matpick import pick; pick(PIL image, exclude=[B&B names]) -> ['Bird & Bamboo X', ...]"""
import json
import numpy as np
from skimage.color import rgb2lab, deltaE_ciede2000
from scipy.cluster.vq import kmeans2
R = '/home/claude/mahjmatchmaker-data/'
BB = {x['name']: x['hex'] for x in json.load(open(R + 'work/bbracks.json'))}
def _lab(h): return rgb2lab(np.array([[[int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)]]]) / 255.)[0, 0]
# B&B wood finishes are BANNED (Tiffany, Oct 15 11:57pm): not sold now, and our renders look painted, not wood. Doc 57.
BB_WOODS = {'Weathered Oak', 'Provincial', 'Red Mahogany', 'Dark Walnut', 'Almond', 'Tudor'}  # Oct 18: Almond + Tudor added (wood-look; Tiffany 01:44)
BBL = {k: _lab(v) for k, v in BB.items() if 'Metallic' not in k and k != 'Clear' and k not in BB_WOODS}

def pick(im, exclude=(), k=6, maxn=2):
    im = im.convert('RGB').copy(); im.thumbnail((220, 220))
    a = np.asarray(im).reshape(-1, 3) / 255.
    a = a[a.min(1) < .95]
    lab = rgb2lab(a[None])[0]
    np.random.seed(0); c, l = kmeans2(lab, k, minit='++', seed=0)
    cnt = np.bincount(l, minlength=k) / len(l)
    ex = {e.replace('Bird & Bamboo ', '') for e in exclude}
    cand = {n: v for n, v in BBL.items() if n not in ex}
    out = []
    ch = np.hypot(c[:, 1], c[:, 2])
    # her picks pull the mat's COLOURS (accents), not its background neutrals: coloured clusters (chroma >= 12, >= 6% of the
    # mat) first, by size x chroma; neutrals only when the mat has no colour
    col = [i for i in range(k) if ch[i] >= 12 and cnt[i] >= .06]
    order = sorted(col, key=lambda i: -cnt[i] * min(ch[i], 40)) or list(np.argsort(-cnt))
    for i in order:
        n = min(cand, key=lambda n: deltaE_ciede2000(c[i], cand[n]))
        if n in out: continue
        if out and deltaE_ciede2000(cand[n], cand[out[0]]) < 15: continue
        out.append(n)
        if len(out) >= maxn: break
    return ['Bird & Bamboo ' + n for n in out]
