"""Table rack fixes round 2 (independent QA Nov 2, coordinator relay): racks still not clean on the table.
 - Bam Bird Boutique wood racks: the photo includes the diagonal pusher stick -> keep the rack only (row/column coverage trim).
 - Mahjong Black Acrylic (Bamlet's): solid black box -> re-cut from the brand's top-down photo (bam_0, black on white).
 - Bam Bird Boutique White Acrylic: ragged left end -> re-cut from the brand's top-down photo (bbw_0, white on lavender).
 - My Fair Mahjong Clear, The Ultimate Rack Crystal Clear: white slab -> see-through acrylic cut (alpha from how much darker than white).
 - Virora White Magnetic Wood: blurry white halo -> hard edge + 1px choke.
Never grays a rack out. Writes assets/table-view/racks/<safe>.webp + config/tableview-rack-audit-nov02.json 'fixed'.
Usage: python3 rack_fix_nov02b.py <build dir> <dir with black.png bbwhite.png (brand re-cuts)>"""
import sys, json
sys.path.insert(0, __import__('os').path.dirname(__file__))
from rack_audit_nov02 import *
from PIL import ImageFilter
B, CUT = sys.argv[1], sys.argv[2]; D, IMG = load_build(B); aud = json.load(open(AUD)); done = {}
def app(k): return decode(IMG[D['racks'][k]['im']])
def finish(a, m, blur=.6):
    al = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))) if blur else (m * 255).astype(np.uint8)
    a = a.copy(); a[..., 3] = np.minimum(a[..., 3], al) if a[..., 3].max() else al
    o = Image.fromarray(a, 'RGBA'); ys, xs = np.where(a[..., 3] > 20); return o.crop((max(xs.min() - 2, 0), max(ys.min() - 2, 0), xs.max() + 3, ys.max() + 3))
def regular(im, frac=.85, fill=True, rect=False):
    a = np.asarray(im.convert('RGBA')).copy(); m = a[..., 3] > 128
    r = m.sum(1); rs = np.where(r >= frac * r.max())[0]; m[:rs.min()] = False; m[rs.max() + 1:] = False
    c = m.sum(0); cs = np.where(c >= frac * c.max())[0]; m[:, :cs.min()] = False; m[:, cs.max() + 1:] = False
    if rect:  # clean rectangle: the rows / columns the rack really fills
        rs = np.where(m.sum(1) >= frac * m.sum(1).max())[0]; cs = np.where(m.sum(0) >= frac * m.sum(0).max())[0]
        m[:] = False; m[rs.min():rs.max() + 1, cs.min():cs.max() + 1] = True
    if fill:  # fill notches along rows and along columns (e.g. where the pusher stick met the rack)
        for y in range(m.shape[0]):
            x = np.where(m[y])[0]
            if len(x): m[y, x.min():x.max() + 1] = True
        for x in range(m.shape[1]):
            y = np.where(m[:, x])[0]
            if len(y): m[y.min():y.max() + 1, x] = True
    a[..., 3] = 255; return a, m
def save(k, o, method):
    p = OVD / (safe(k) + '.webp'); o.save(p, 'WEBP', lossless=True)
    done[k] = {'file': str(p.relative_to(R0)), 'was': ['QA Nov 2: ' + method.split(':')[0]], 'now': metrics(shave(o), whiteish(D['racks'][k]))['why'], 'method': method}
    print(D['racks'][k]['n'], o.size, done[k]['now'])
byname = {D['racks'][k]['n']: k for k in table_racks(D)}
for n in ['Dusty Lilac', 'Indigo', 'Lagoon', 'Mulberry', 'Periwinkle', 'Pink', 'Slate Blue', 'Teal', 'Olive Green']:
    k = byname['Bam Bird Boutique ' + n + ' Wood']; a0 = np.asarray(app(k)); a, m = regular(app(k), .8)
    hole = m & (a0[..., 3] < 128)  # holes in the brand cut (where the stick met the rack, magnet dots): colour from the nearest real pixel
    if hole.any(): _, idx = ndimage.distance_transform_edt(hole, return_indices=True); a[..., :3] = a0[..., :3][idx[0], idx[1]]
    a[..., 3] = 0; save(k, finish(a, m), 'pusher stick removed: rack-only crop (row/column coverage), holes filled + soft 0.6px edge')
for n, f, meth in (('Mahjong Black Acrylic Racks and Scallop Pushers', 'black.png', 're-cut from the brand top-down photo (black on white, dark-pixel mask)'),
                   ('Bam Bird Boutique White Acrylic', 'bbwhite.png', 're-cut from the brand top-down photo (white on lavender) + squared ends')):
    save(byname[n], Image.open(os.path.join(CUT, f)).convert('RGBA'), meth)
for n in ('My Fair Mahjong Clear', 'The Ultimate Rack - CRYSTAL CLEAR'):
    k = byname[n]; im = app(k); a0 = np.asarray(im); a, m = regular(im, .9, rect=True)
    rgb = a0[..., :3].astype(float); hole = m & (a0[..., 3] < 128)
    if hole.any():  # corner bite: fill colour from the nearest real pixel
        _, idx = ndimage.distance_transform_edt(hole, return_indices=True); rgb = rgb[idx[0], idx[1]]
    L = rgb.mean(2); al = np.clip(60 + 2.2 * (245 - L), 60, 235)
    edge = m & ~ndimage.binary_erosion(m, iterations=2); al = np.where(edge, np.maximum(al, 200), al)
    out = np.dstack([rgb, al * m]).astype(np.uint8); o = finish(out, m, 0); o = Image.fromarray(np.asarray(o), 'RGBA')
    save(k, o, 'see-through acrylic cut: alpha from darkness (white slab -> clear), squared outline, solid 2px edge')
k = byname['Virora White Magnetic Wood']; a = np.asarray(app(k)).copy(); m = a[..., 3] > 235; m = ndimage.binary_erosion(m, iterations=1)
lab, nn = ndimage.label(m); sz = ndimage.sum(m, lab, range(1, nn + 1)); m = lab == (np.argmax(sz) + 1); a[..., 3] = 255
Lr = np.array([a[y, m[y], :3].mean() if m[y].any() else 255 for y in range(m.shape[0])]); yb = m.shape[0] - 14 + int(np.argmin(Lr[-14:])); m[yb + 2:] = False  # cut the shadow below the dark bottom edge
c = m.sum(0); cs = np.where(c >= .9 * np.median(c[c > 0]))[0]; m[:, :cs.min()] = False; m[:, cs.max() + 1:] = False  # soft white end blobs
save(k, finish(a, m, .5), 'halo removed: hard alpha (>235) + 1px choke')
aud['fixed'].update(done); json.dump(aud, open(AUD, 'w'), indent=1); print('fixed', len(done))
