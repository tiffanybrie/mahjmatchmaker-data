"""Rack colour check (Tiffany Nov 23 2026, after a Peach Sorbet scallop sat on a blue snowflake mat: 'that color is not in
this at all... that's untrustworthy'). Cause: on Nov 22 the second mat rack was filled from a fixed list of scallop racks for
variety, with no check against the mat. RULE: every coloured mat rack must be a colour that is IN the mat photo. Neutrals
(white, milk glass, lace, opal, clear, wood, rattan, tortoise, metallic) pass. Her own picks pass (mat_racks_by starts 'Tiffany').
Usage: python3 scripts/checks/rack_colour_check.py <album spec json>   (exit 1 on any miss). The album build runs it."""
import sys, json, os, numpy as np
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + '/'
NEUTRAL = ('white', 'milk glass', 'lace', 'opal', 'clear', 'oak', 'burl', 'walnut', 'tortoise', 'cane', 'beechwood', 'metallic', 'cream', 'almond', 'pebble', 'agate', 'cola', 'chestnut')
def lab(c):
    c = np.asarray(c, float) / 255; c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    M = np.array([[.4124, .3576, .1805], [.2126, .7152, .0722], [.0193, .1192, .9505]]); x = M @ c / np.array([.9505, 1, 1.089])
    f = np.where(x > 0.008856, np.cbrt(x), 7.787 * x + 16 / 116); return np.array([116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])])
BB = {'Bird & Bamboo ' + x['name']: [int(x['hex'][i:i + 2], 16) for i in (1, 3, 5)] for x in json.load(open(R + 'work/bbracks.json'))}
IX = json.load(open(R + 'assets/racks/card/index.json'))['racks']
def rack_rgb(n):
    if n in BB: return BB[n]
    if n in IX:
        a = np.asarray(Image.open(R + IX[n]['file']).convert('RGBA').resize((120, 24))).reshape(-1, 4); a = a[a[:, 3] > 200]
        return np.median(a[:, :3], 0) if len(a) else None
def mat_pal(img, box=None):
    im = Image.open(R + img).convert('RGB')
    if box: im = im.crop(tuple(box))
    q = im.resize((120, 120)).quantize(12, kmeans=2); p = q.getpalette(); return [(n / 144, p[i * 3:i * 3 + 3]) for n, i in q.getcolors()]
def run(spec, tol=24, share=1.5):
    bad = []; never = {(x['brand'], x['name']) for x in json.load(open(R + 'config/album-never-show.json'))['mats']}
    for m in json.load(open(spec))['mats']:
        if (m.get('brand'), m.get('name')) in never: continue
        if not m.get('mat_racks') or (m.get('mat_racks_by') or '').startswith('Tiffany'): continue
        pal = [lab(c) for s, c in mat_pal(m['img'], m.get('box')) if s >= share]
        for r in m['mat_racks']:
            if any(w in r.lower() for w in NEUTRAL): continue
            c = rack_rgb(r)
            if c is None: bad.append(f"{m['name']}: {r} has no known colour"); continue
            d = min(np.linalg.norm(lab(c) - p) for p in pal)
            if d > tol: bad.append(f"{m['name']}: {r} is not in the mat (nearest mat colour is {d:.0f} away)")
    return bad
if __name__ == '__main__':
    b = run(sys.argv[1]); print('\n'.join(b) or 'rack colour check PASS'); sys.exit(1 if b else 0)
