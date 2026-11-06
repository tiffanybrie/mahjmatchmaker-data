"""OMM Agate card rack (Nov 6, Tiffany 2:11am: Juniper racks = OMM Hot Pink + OMM Agate, same OMM shape, lying the same way).
Step 1 = the exact pipeline that made oh-my-mahjong-hot-pink.png (real_racks.build 'omm': rembg cut of OMM's product photo
assets/racks/omm/agate.jpg, levelled on the rack's bottom edge; re-running it on hot-pink.jpg reproduces the committed card
pixel for pixel). OMM shot Agate with the pusher opened wider (9.5 deg vs 5.9) and from a little higher (taller rack body), so
step 2 rotates ONLY the pusher down about its hinge to the hot-pink angle, and step 3 scales the height so the rack body has the
hot-pink card's proportions. Edges: alpha below 24 dropped, edge pixels de-whitened (no halo on navy).
Usage: python3 scripts/albumcard/omm_agate_card.py  -> assets/racks/card/oh-my-mahjong-agate.png + index.json entry"""
import json, sys, os
import numpy as np
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'scripts/albumcard')
import real_racks as RR

def lines(im):
    a = np.asarray(im)[..., 3] > 100; H, W = a.shape; xs = np.arange(int(W * .25), int(W * .75)); top, rt = [], []
    for x in xs:
        c = a[:, x]; t = np.argmax(c); g = t + np.argmax(~c[t:]); top.append(t); rt.append(g + np.argmax(c[g:]))
    return np.polyfit(xs, top, 1), np.polyfit(xs, rt, 1), a

hp = Image.open(R + 'assets/racks/card/oh-my-mahjong-hot-pink.png').convert('RGBA')
HP_TOP, _, _ = lines(hp)
HP_FRAC = json.load(open(R + 'assets/racks/card/index.json'))['racks']['Oh My Mahjong Hot Pink']['rack_frac']
im, frac = RR.build('Oh My Mahjong Agate', 'omm', R + 'assets/racks/omm/agate.jpg')
top, rtop, a = lines(im)
H, W = a.shape
delta = np.degrees(np.arctan(top[0])) - np.degrees(np.arctan(HP_TOP[0]))   # slopes are negative (rising right): delta < 0 = agate steeper
arr = np.asarray(im).copy()
yy, xx = np.mgrid[0:H, 0:W]
rack_top = np.polyval(rtop, xx)
push = (arr[..., 3] > 0) & (yy < rack_top - 1)
# hinge = left end of the pusher where it meets the rack top
px = int(np.nonzero(push.any(0))[0][0]) + 40; py = float(np.polyval(rtop, px))
push &= xx > px + 30   # the hinge block stays put (rotating it with the arm left a seam)
pus = arr.copy(); pus[..., 3] = np.where(push, arr[..., 3], 0)
rack = arr.copy(); rack[..., 3] = np.where(push, 0, arr[..., 3])
pad = 200
canvas = lambda x: Image.fromarray(np.pad(x, ((pad, pad), (0, 0), (0, 0))), 'RGBA')
def compose(d):
    P = canvas(pus).rotate(d, resample=Image.BICUBIC, center=(px, py + pad))   # PIL: positive = counter-clockwise; d < 0 lowers the pusher
    o = Image.new('RGBA', P.size, (0, 0, 0, 0)); o.alpha_composite(P); o.alpha_composite(canvas(rack)); o = o.crop(o.getbbox())
    rb = frac * im.height; trb = HP_FRAC * hp.height / hp.width * o.width; k = trb / rb
    return o.resize((o.width, round(o.height * k)), Image.LANCZOS), k, trb
# the slope fit alone lowers it too far (235px tall vs hot pink 259), so pick the rotation that gives the hot-pink card's
# overall proportions (height/width) once the rack body matches
best = min((abs(compose(d)[0].height / compose(d)[0].width - hp.height / hp.width), d) for d in np.arange(delta, 0.01, 0.1))
delta = best[1]; out, sy, target_rb = compose(delta)
new_frac = target_rb / out.height
# clean edges: drop faint alpha, pull edge colour away from white
o = np.asarray(out).astype(float); al = o[..., 3]
al[al < 24] = 0
edge = (al > 0) & (al < 230)
lum = o[..., :3].mean(2)
o[..., :3] = np.where((edge & (lum > 200))[..., None], o[..., :3] * 0.75, o[..., :3])
o[..., 3] = al
out = Image.fromarray(o.clip(0, 255).astype(np.uint8), 'RGBA'); out = out.crop(out.getbbox())
if out.width != hp.width: out = out.resize((hp.width, round(out.height * hp.width / out.width)), Image.LANCZOS)
f = R + 'assets/racks/card/oh-my-mahjong-agate.png'; out.save(f, optimize=True)
idx = json.load(open(R + 'assets/racks/card/index.json'))
idx['racks']['Oh My Mahjong Agate'] = {'file': 'assets/racks/card/oh-my-mahjong-agate.png', 'source': 'assets/racks/omm/agate.jpg', 'kind': 'omm',
                                       'rack_frac': round(new_frac, 3), 'built_by': 'scripts/albumcard/omm_agate_card.py', 'note': 'Nov 6: pusher rotated %.1f deg to the hot-pink angle, height x%.3f (scripts/albumcard/omm_agate_card.py)' % (delta, sy)}
json.dump(idx, open(R + 'assets/racks/card/index.json', 'w'), indent=1, ensure_ascii=False)
print(f, out.size, 'delta %.2f' % delta, 'sy %.3f' % sy, 'frac %.3f' % new_frac, 'hp', hp.size, HP_FRAC)
