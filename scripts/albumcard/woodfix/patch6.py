"""Oct 18: patch the 6 live holiday/album cards the first woodpatch missed."""
import json, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import woodpatch as W
from PIL import Image
D = os.path.dirname(__file__)
W.BITTER = os.path.join(D, 'Bitter-Bold.ttf')
HITS = json.load(open(sys.argv[1])); FS = list(HITS)
tmpl = np.load(os.path.join(D, 'tmplcol.npy'))[:, :1]
CORN = (0x6A, 0x8C, 0xBC)
def repl(f, wood):
    if wood == 'Almond': return {'kind': 'paint', 'rgb': W.CREAM, 'label': 'Cream', 'label_full': 'Bird & Bamboo Cream'}
    if wood == 'Tudor' and 'blue-christmas' in f: return {'kind': 'paint', 'rgb': CORN, 'label': 'Cornflower Blue', 'label_full': 'Bird & Bamboo Cornflower Blue'}
    return {'kind': 'photo', 'label': 'Bam Bird Walnut', 'label_full': 'Bam Bird Boutique Walnut'}
wp = os.path.join(D, 'woodpatched.json'); prev = json.load(open(wp))
for f in FS:
    hits = HITS[f]
    print(f, hits)
    im = Image.open(f).convert('RGBA'); a = np.asarray(im.convert('RGB')).copy()
    holiday = '/holiday' in f
    out, seen = [], set()
    for h in sorted(hits, key=lambda h: h[2]):
        if round(h[2] / 25) in seen: continue
        seen.add(round(h[2] / 25))
        r = repl(f, h[0])
        fn = {'C': W.patch_C, 'B': W.patch_B, 'A': W.patch_A}[h[5]]
        res = fn(im, a, h, r, tmpl)
        print('  ->', h[0], res)
        if res is None or isinstance(res[0], str): continue
        out.append([h[0], r['label_full'], list(map(int, res))])
    if out:
        im.convert('RGB').save(f, quality=93); prev[f] = out
json.dump(prev, open(wp, 'w'), indent=1)
