"""Measured color analysis (Oct 19). Report only: reads mat photos + tile photos, writes
config/mat-color-measured.json, config/tile-color-measured.json and prints a summary used by docs/87.
Method: resize, strip flat border background + near-white/near-black, k-means in Lab, map clusters to our families."""
import os, json, colorsys, collections
import numpy as np
from PIL import Image
from skimage.color import rgb2lab, lab2rgb
from sklearn.cluster import KMeans

R = '/home/claude/mahjmatchmaker-data/'
GAL = R + 'assets/mats/gallery/'
G = json.load(open(R + 'config/mat-color-guesses.json'))['mats']

def family(rgb):
    r, g, b = rgb
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    H = h * 360
    lab = rgb2lab(np.array([[rgb]]))[0, 0]
    C = float(np.hypot(lab[1], lab[2]))
    L = lab[0]
    if L < 16: return 'dark'
    if C < 9:
        if L > 92: return 'bw'
        if L < 30: return 'dark'
        return 'neutral'
    if L < 26 and C < 30: return 'dark'
    if L > 78 and C < 22 and 30 <= H < 100: return 'neutral'   # cream / ivory grounds
    if (H < 20 or H >= 350) and L < 42 and C < 55: return 'brown'   # cognac, chestnut
    if 20 <= H < 50 and L < 48 and C < 45: return 'brown'
    if 38 <= H < 58 and 45 <= L < 75 and C < 45: return 'gold'
    if H < 12 or H >= 345:
        return 'pink' if L > 62 else 'red'
    if H < 40: return 'orange' if L > 45 else ('red' if C > 45 else 'brown')
    if H < 65: return 'yellow'
    if H < 160: return 'green'
    if H < 195: return 'teal'
    if H < 255: return 'blue'
    if H < 290: return 'purple'
    return 'pink'

COMPAT = {  # families close enough that a tag is not "wrong"
    'pink': {'red', 'purple'}, 'red': {'pink', 'orange'}, 'orange': {'red', 'yellow', 'gold', 'brown'},
    'yellow': {'gold', 'orange', 'green'}, 'gold': {'yellow', 'brown', 'orange', 'neutral'},
    'green': {'teal', 'yellow'}, 'teal': {'green', 'blue'}, 'blue': {'teal', 'purple'},
    'purple': {'blue', 'pink'}, 'brown': {'neutral', 'gold', 'orange', 'dark'},
    'neutral': {'bw', 'brown', 'gold'}, 'bw': {'neutral', 'dark'}, 'dark': {'bw', 'brown', 'blue'},
    'multi': set(),
}

def load(path, size=160):
    im = Image.open(path).convert('RGB'); im.thumbnail((size, size))
    return np.asarray(im).astype(float) / 255

def bg_mask(a):
    """True = keep. Strip flat border color (product-shot background) + near white/black."""
    h, w, _ = a.shape
    border = np.concatenate([a[:3].reshape(-1, 3), a[-3:].reshape(-1, 3), a[:, :3].reshape(-1, 3), a[:, -3:].reshape(-1, 3)])
    keep = np.ones((h, w), bool)
    flat = border.std(0).max() < 0.06
    if flat:
        bc = np.median(border, 0)
        keep &= np.linalg.norm(a - bc, axis=2) > 0.09
    lum = a.mean(2); sat = a.max(2) - a.min(2)
    keep &= ~((lum > 0.94) & (sat < 0.08))
    keep &= lum > 0.04
    return keep, flat

def clusters(a, keep, k=6):
    px = a[keep]
    if len(px) < 200: px = a.reshape(-1, 3)
    lab = rgb2lab(px[None])[0]
    km = KMeans(n_clusters=k, n_init=3, random_state=0).fit(lab)
    out = []
    for i in range(k):
        m = km.labels_ == i
        if not m.any(): continue
        c = lab2rgb(km.cluster_centers_[i][None, None])[0, 0].clip(0, 1)
        h, l, s = colorsys.rgb_to_hls(*c)
        out.append({'hex': '#%02x%02x%02x' % tuple((c * 255).round().astype(int)), 'hue': round(h * 360), 'sat': round(s, 2),
                    'light': round(l, 2), 'pct': round(100 * m.mean(), 1), 'family': family(tuple(c))})
    out.sort(key=lambda x: -x['pct'])
    return out

FAMS = ['dark','bw','neutral','brown','gold','pink','red','orange','yellow','green','teal','blue','purple']
def family_vec(px):
    lab = rgb2lab(px[None])[0]; L = lab[:, 0]; C = np.hypot(lab[:, 1], lab[:, 2])
    mx = px.max(1); mn = px.min(1); d = mx - mn + 1e-9
    r, g, b = px[:, 0], px[:, 1], px[:, 2]
    H = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    out = np.full(len(px), 'pink', dtype=object)
    conds = [
        (L < 16, 'dark'), ((C < 9) & (L > 92), 'bw'), ((C < 9) & (L < 30), 'dark'), (C < 9, 'neutral'),
        ((L < 26) & (C < 30), 'dark'), ((L > 78) & (C < 22) & (H >= 30) & (H < 100), 'neutral'),
        (((H < 20) | (H >= 350)) & (L < 42) & (C < 55), 'brown'),
        ((H >= 20) & (H < 50) & (L < 48) & (C < 45), 'brown'), ((H >= 38) & (H < 58) & (L >= 45) & (L < 75) & (C < 45), 'gold'),
        (((H < 12) | (H >= 345)) & (L > 62), 'pink'), ((H < 12) | (H >= 345), 'red'),
        ((H < 40) & (L > 45), 'orange'), ((H < 40) & (C > 45), 'red'), (H < 40, 'brown'),
        (H < 65, 'yellow'), (H < 160, 'green'), (H < 195, 'teal'), (H < 255, 'blue'), (H < 290, 'purple')]
    done = np.zeros(len(px), bool)
    for c, f in conds:
        m = c & ~done; out[m] = f; done |= m
    return out

def pixel_area(a, keep):
    px = a[keep]
    if len(px) < 200: px = a.reshape(-1, 3)
    f = family_vec(px); n = len(f)
    return collections.Counter({k: 100 * v / n for k, v in collections.Counter(f).items()})

def fam_area(cl):
    d = collections.Counter()
    for c in cl: d[c['family']] += c['pct']
    return d

def compat(f, tags):
    return f in tags or bool(COMPAT.get(f, set()) & set(tags)) or 'multi' in tags

def run_mats():
    res = {}
    for key, v in G.items():
        p = None
        for ext in ('.webp', '.jpg', '.png', '.jpeg'):
            if os.path.exists(GAL + v['image'] + ext): p = GAL + v['image'] + ext; break
        if not p: continue
        a = load(p); keep, flat = bg_mask(a)
        cl = clusters(a, keep)
        area = pixel_area(a, keep)
        # dominant chromatic family: largest family by area, ignoring tiny
        fams = area.most_common()
        chrom = [(f, x) for f, x in fams if f not in ('neutral', 'bw', 'dark')]
        ground = fams[0]
        if chrom and sum(x for f, x in chrom) >= 15: dom, dom_pct = chrom[0]
        else: dom, dom_pct = ground
        tags = [v['primary']] + list(v.get('secondary', []))
        flags = []
        if not compat(dom, tags): flags.append('dominant-not-tagged')
        if v['primary'] != 'multi' and area.get(v['primary'], 0) + sum(area.get(x, 0) for x in COMPAT.get(v['primary'], ())) * 0.5 < 5:
            flags.append('primary-under-5pct')
        weak_sec = [t for t in v.get('secondary', []) if area.get(t, 0) < 5 and not any(area.get(x, 0) >= 5 for x in COMPAT.get(t, ()))]
        if weak_sec: flags.append('secondary-under-5pct:' + ','.join(weak_sec))
        # grade
        wood = area.get('brown', 0) + area.get('orange', 0) * 0.3
        unreliable = (not flat and wood > 25 and v['primary'] not in ('brown', 'orange', 'gold', 'neutral')) or keep.mean() < 0.25
        busy = dom_pct < 34 or len([f for f, x in fams if x >= 12]) >= 4
        if not flags: grade = None
        elif unreliable: grade = 'measurement-unreliable'
        elif busy or (flags == ['secondary-under-5pct:' + ','.join(weak_sec)] if weak_sec else False):
            grade = 'ambiguous'
        else: grade = 'likely-wrong-tag'
        score = 0
        if 'dominant-not-tagged' in flags: score += dom_pct
        if 'primary-under-5pct' in flags: score += 30
        score += {'low': 10, 'medium': 5, 'high': 0}.get(v.get('conf'), 0)
        res[key] = {'image': v['image'], 'flat_bg': bool(flat), 'clusters': cl[:3], 'all_clusters': cl,
                    'family_area': {k2: round(x, 1) for k2, x in fams}, 'cluster_family_area': {k2: round(x, 1) for k2, x in fam_area(cl).most_common()}, 'measured_ground': ground[0], 'measured_dominant': dom, 'dominant_pct': round(dom_pct, 1),
                    'measured_families': [f for f, x in fams if x >= 8][:4], 'tags': tags, 'conf': v.get('conf'),
                    'flags': flags, 'grade': grade, 'score': round(score, 1)}
    return res

def run_tiles():
    cc = json.load(open(R + 'config/colorcards.json'))['sets']
    tb = json.load(open(R + 'config/tile-back-colors.json'))
    inv = {}
    for famname, names in tb.items():
        for n in names: inv.setdefault(n.lower(), []).append(famname)
    out = {}
    for f in sorted(os.listdir(R + 'assets/tiles/album')):
        if not f.endswith('.jpg'): continue
        key = f[:-4]
        a = load(R + 'assets/tiles/album/' + f, 200)
        lum = a.mean(2); sat = a.max(2) - a.min(2)
        keep = ~((lum > 0.78) & (sat < 0.18)) & (lum > 0.05)   # mask white faces
        cl = clusters(a, keep, k=5)
        rec = {'clusters': cl, 'family_area': dict(fam_area(cl).most_common())}
        name = key.replace('-', ' ').title()
        rec['site_back_family'] = inv.get(name.lower()) or inv.get(key.replace('-', ' ').lower())
        if key in cc:
            card = []
            for nm, hx, kind in cc[key].get('backs', []):
                c = np.array([int(hx[i:i + 2], 16) for i in (1, 3, 5)]) / 255
                labc = rgb2lab(c[None, None])[0, 0]
                best = min(cl, key=lambda x: np.linalg.norm(rgb2lab((np.array([int(x['hex'][i:i + 2], 16) for i in (1, 3, 5)]) / 255)[None, None])[0, 0] - labc))
                dE = float(np.linalg.norm(rgb2lab((np.array([int(best['hex'][i:i + 2], 16) for i in (1, 3, 5)]) / 255)[None, None])[0, 0] - labc))
                card.append({'name': nm, 'card_hex': hx, 'closest_measured': best['hex'], 'deltaE': round(dE, 1), 'card_family': family(tuple(c)), 'measured_family': best['family']})
            rec['colorcard_backs'] = card
        out[key] = rec
    return out

if __name__ == '__main__':
    mats = run_mats()
    json.dump({'about': 'Measured mat colors (Oct 19): k-means in Lab on gallery photos, flat background + near white/black removed. Report only; tags unchanged. See docs/87.',
               'mats': mats}, open(R + 'config/mat-color-measured.json', 'w'), indent=1)
    tiles = run_tiles()
    json.dump({'about': 'Measured tile back/layer colors from assets/tiles/album (white faces masked). See docs/87.', 'tiles': tiles},
              open(R + 'config/tile-color-measured.json', 'w'), indent=1)
    print(len(mats), len(tiles))
