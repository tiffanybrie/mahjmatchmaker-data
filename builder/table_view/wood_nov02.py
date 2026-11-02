"""Real wood grain for wood racks in Table view (Tiffany Nov 2 10:11am: Bird & Bamboo wood racks 'look like painted brown racks').
Why: the app's B&B images are the brand's flat colour RENDERS (420x54), no grain at all (not our trim); Yellow Mountain pine /
chestnut / camphor images are 360px and go soft at Table zoom. Fix (sources in assets/table-view/racks-src/wood-nov02/):
 - B&B wood stains (White Wood Stain, Clear, Weathered Oak, Provincial, Dark Walnut): each stain's own band from the brand's
   'WOOD STAINS' photo (real racks, real grain); the label rows are rebuilt from the label-free rest of the same rows, stretched lengthwise (no tiling); shaped like
   the app's B&B rack (its outline). Red Mahogany has no brand photo: Provincial's real grain in Red Mahogany's brand colour.
 - Cherry Red is a B&B PAINT colour, not a stain: not a wood rack (finish tag fixed in preview_nov01.py).
 - Yellow Mountain Natural Pine, Dark Pine, Classic Chestnut, Dark Camphor: the front rack cut from the brand's 2048px
   4-rack photo, straightened, edges squared.
Writes assets/table-view/racks/<safe>.webp + config/tableview-rack-audit-nov02.json 'fixed'. Usage: python3 wood_nov02.py <build dir>"""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
from rack_audit_nov02 import *
from PIL import ImageFilter
B = sys.argv[1]; D, IMG = load_build(B); aud = json.load(open(AUD)); SRC = R0 / 'assets/table-view/racks-src/wood-nov02'; done = {}
byname = {D['racks'][k]['n']: k for k in table_racks(D)}
def save(k, im, method):
    p = OVD / (safe(k) + '.webp'); im.save(p, 'WEBP', quality=90, method=6)
    done[k] = {'file': str(p.relative_to(R0)), 'was': ['flat render / low-res: no visible wood grain (Tiffany Nov 2 10:11am)'], 'now': metrics(shave(im), whiteish(D['racks'][k]))['why'], 'method': method}
    print(D['racks'][k]['n'], im.size, done[k]['now'])
# --- Bird & Bamboo stains from the brand's WOOD STAINS photo (1080x1080): band rows, label box (x0, x1, y0, y1)
BANDS = {'White Wood Stain': (144, 323, (70, 300, 250, 322)), 'Clear Wood Stain': (335, 498, (66, 272, 436, 498)),
         'Weathered Oak': (514, 695, (80, 652, 604, 680)), 'Provincial': (707, 860, (80, 462, 784, 860)), 'Dark Walnut': (872, 1046, (80, 545, 968, 1040))}
X0, X1 = 66, 1027
ph = np.asarray(Image.open(SRC / 'birdandbamboo_wood_stains.jpg').convert('RGB')).copy()
def band(name):
    y0, y1, (tx0, tx1, ty0, ty1) = BANDS[name]; b = ph[y0:y1, X0:X1].copy(); w = b.shape[1]; tx0 -= X0; tx1 = min(w, tx1 - X0 + 10)
    srcw = w - tx1; r0, r1 = max(0, ty0 - y0 - 6), min(b.shape[0], ty1 - y0 + 4)
    seg = Image.fromarray(b[r0:r1, tx1:]).resize((w, r1 - r0), Image.LANCZOS)  # label rows <- the label-free rest of the same rows, stretched lengthwise (no tiling, no mirror)
    b[r0:r1] = np.asarray(seg)
    return b
def shaped(tex, k, H=128):
    al = decode(IMG[D['racks'][k]['im']]).split()[3]; Wt = int(round(al.width * H / al.height)); al = al.resize((Wt, H), Image.LANCZOS)
    t = Image.fromarray(tex).resize((Wt, H), Image.LANCZOS)  # the whole band stretched to the rack's length (grain runs lengthwise)
    t = t.crop((0, 0, Wt, H)).convert('RGBA'); t.putalpha(al); return t
for nm, key in (('White Wood Stain', 'Bird & Bamboo White Wood Stain'), ('Clear Wood Stain', 'Bird & Bamboo Clear Wood Stain'), ('Weathered Oak', 'Bird & Bamboo Weathered Oak'),
                ('Provincial', 'Bird & Bamboo Provincial'), ('Dark Walnut', 'Bird & Bamboo Dark Walnut')):
    k = byname[key]; save(k, shaped(band(nm), k), "real grain: this stain's band from Bird & Bamboo's WOOD STAINS photo, label rows from the rest of the same rows, B&B rack outline")
k = byname['Bird & Bamboo Red Mahogany']; pv = band('Provincial').astype(float); L = pv.mean(2, keepdims=True)
rm = np.asarray(decode(IMG[D['racks'][k]['im']]).convert('RGBA')).astype(float); col = np.median(rm[rm[..., 3] > 200][:, :3], 0)
tex = np.clip(L / L.mean() * col, 0, 255).astype(np.uint8)
save(k, shaped(tex, k), "no brand photo of Red Mahogany: Provincial's real grain in Red Mahogany's brand colour (flagged)")
# --- Yellow Mountain: front rack from the brand 4-rack photo
for f, key in (('ymnat', '18" Natural Pine Wooden Mahjong Racks with Pushers - Set of 4 (Racks with Pushers Only)'), ('ymdark', '18-Inch Dark Pine Wooden Mahjong Game Racks with Built-in Pushers - Set of 4'),
               ('ymchest', 'Yellow Mountain Classic Chestnut Wood'), ('ymcamph', 'Dark Camphor Wooden Mahjong Game Racks with Pushers, 18" - Set of 4')):
    im = Image.open(SRC / (f + '_cut.png')).convert('RGBA'); a = np.asarray(im).copy(); m = a[..., 3] > 128
    r = m.sum(1); rs = np.where(r >= .9 * r.max())[0]; m[:rs.min()] = False; m[rs.max() + 1:] = False  # squared top / bottom (no ragged shadow)
    c = m.sum(0); cs = np.where(c >= .92 * c.max())[0]; m[:, :cs.min()] = False; m[:, cs.max() + 1:] = False  # squared ends (no white sliver / slanted end face)
    Lr = a[..., :3].mean(2); rows = [y for y in range(m.shape[0]) if m[y].any()]; yb = rows[-1]
    while yb > rows[0] and Lr[yb, m[yb]].mean() > Lr[rows[len(rows) // 2], m[rows[len(rows) // 2]]].mean() + 40: m[yb] = False; yb -= 1  # pale shadow rows at the bottom
    m = ndimage.binary_erosion(m, iterations=2); a[..., 3] = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.6)))
    o = Image.fromarray(a, 'RGBA'); ys, xs = np.where(a[..., 3] > 20); o = o.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)); o.thumbnail((1000, 1000))
    save(byname[key], o, 'real grain: front rack cut from the brand 2048px 4-rack photo, straightened, squared edges')
aud['fixed'].update(done); json.dump(aud, open(AUD, 'w'), indent=1); print('wood racks', len(done))
