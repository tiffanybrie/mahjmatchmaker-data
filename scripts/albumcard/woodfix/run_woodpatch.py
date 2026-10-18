import json, glob, sys, numpy as np
S = '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/qafix'
sys.path.insert(0, S)
import woodpatch as W
from PIL import Image, ImageDraw
d = json.load(open(S + '/woods2.json'))
fs = sorted(glob.glob('assets/cards/logofix-v2/*.jpg'))
SL = {1: (781, 245, 120, 24), 2: (785, 321, 105, 23), 3: (785, 391, 108, 19)}
manual = {51: [('Almond', 1)], 56: [('Almond', 2)], 93: [('Almond', 2)], 117: [('Almond', 1), ('Provincial', 2)],
          165: [('Almond', 1), ('Provincial', 2)], 177: [('Almond', 2)], 199: [('Almond', 2)], 203: [('Tudor', 1)], 164: [('Dark Walnut', 1)], 113: [('Provincial', 1), ('Almond', 2)]}
for i, hs in manual.items():
    d[fs[i]] = [[k, *SL[s], 'A'] for k, s in hs]
for f in d:
    if 'willow-mahjong-tiles-tigre-de-tartan-caned-trompe' in f:
        for h in d[f]: h[5] = 'B'
ONLY = set(sys.argv[1:])
if ONLY: d = {f: v for f, v in d.items() if f in ONLY}
tmpl = np.load(S + '/tmplcol.npy')[:, :1]
CORN = (0x6A, 0x8C, 0xBC)
def repl(f, wood):
    if wood == 'Almond': return {'kind': 'paint', 'rgb': W.CREAM, 'label': 'Cream', 'label_full': 'Bird & Bamboo Cream'}
    if wood == 'Tudor' and 'blue-christmas' in f: return {'kind': 'paint', 'rgb': CORN, 'label': 'Cornflower Blue', 'label_full': 'Bird & Bamboo Cornflower Blue'}
    return {'kind': 'photo', 'label': 'Bam Bird Walnut', 'label_full': 'Bam Bird Boutique Walnut'}
done, bad = {}, []
for f, hits in d.items():
    im = Image.open(f).convert('RGBA'); a = np.asarray(im.convert('RGB')).copy()
    holiday = '/holiday' in f or 'codefooter-v1' in f
    seen = set(); out = []
    for h in sorted(hits, key=lambda h: h[2]):
        key = round(h[2] / 25)
        if key in seen: continue
        seen.add(key)
        r = repl(f, h[0])
        fn = W.patch_C if holiday else (W.patch_B if h[5] == 'B' else W.patch_A)
        res = fn(im, a, h, r, tmpl)
        if res is None or (isinstance(res, tuple) and isinstance(res[0], str)):
            bad.append((f, h, res)); continue
        out.append([h[0], r['label_full'], list(map(int, res))])
    if out:
        im.convert('RGB').save(f, quality=93); done[f] = out
import os
if ONLY and os.path.exists(S + '/woodpatched.json'):
    prev = json.load(open(S + '/woodpatched.json')); prev.update(done); done_all = prev
else: done_all = done
json.dump(done_all, open(S + '/woodpatched.json', 'w'), indent=1)
json.dump(bad, open(S + '/woodbad.json', 'w'), indent=1, default=str)
print(len(done), sum(len(v) for v in done.values()), 'bad', len(bad))
for b in bad: print(b)
# contact sheet
items = list(done)
Wd, Hd, cols = 330, 300, 6
sh = Image.new('RGB', (Wd * cols, (Hd + 14) * ((len(items) + cols - 1) // cols)), 'white'); dr = ImageDraw.Draw(sh)
for i, f in enumerate(items):
    im = Image.open(f).convert('RGB').crop((660, 60, 1080, 480)).resize((Wd, Hd))
    x = (i % cols) * Wd; y = (i // cols) * (Hd + 14); sh.paste(im, (x, y + 14)); dr.text((x + 2, y + 1), f'{i} ' + f.split('/')[-1][:44], fill='red')
sh.save(S + '/woodsheet.jpg')
