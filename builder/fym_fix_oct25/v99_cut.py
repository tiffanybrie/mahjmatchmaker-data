"""FYM v99 rack singles cutter (Tiffany Oct 26 10:07pm: "Have all of the vertical racks been rotated to horizontal? Have
backgrounds been removed from racks where possible? Have we isolated a single horizontal rack from every set where it's
possible?"). Makes assets/racks/v99/<name>.webp from config/fym-rack-singles-oct26.json:
  src  : brand product image URL (Shopify CDN, fetched at width=1400) or "cur" (the rack's current card image in <build>)
  mask : "rembg" (isnet-general-use on the brand photo) | "alpha" (image is already a cut-out) | "light" (object on a light,
         plain background: distance from the border colour) | "dark" (light object on a dark plain background)
  pick : [fx, fy] point (fractions of the pre-crop) -> the connected component nearest it = the ONE rack kept
  pre  : optional [x0,y0,x1,y1] fractions, crop before masking (keeps neighbouring racks out)
  split: erosion iterations used only to separate touching racks when picking (default 0)
  rot  : "auto" (long side of the picked rack -> horizontal) or degrees; flip: true adds 180
  white: true for white/clear racks (stricter defringe)
Never redraws or recolours: pixels are the brand's own photo, only alpha + rotation + crop change.
Usage: v99_cut.py <build_dir> [name ...]   (build_dir only needed for src "cur")"""
import sys, os, io, json, hashlib, urllib.request
import numpy as np, cv2
from PIL import Image
from scipy import ndimage
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(H + '/../..') + '/'
sys.path.insert(0, REPO + 'builder'); from fym_defringe import defringe
CFG = REPO + 'config/fym-rack-singles-oct26.json'; OUT = REPO + 'assets/racks/v99/'
CACHE = os.environ.get('V99_CACHE', '/tmp/v99cache'); os.makedirs(CACHE, exist_ok=True)
_S = None
def rembg_alpha(im):
    global _S
    from rembg import remove, new_session
    if _S is None: _S = new_session('isnet-general-use')
    return np.asarray(remove(im.convert('RGB'), session=_S, post_process_mask=True).getchannel('A')).astype(float)
def fetch(u):
    u = ('https:' + u) if u.startswith('//') else u; u += ('&' if '?' in u else '?') + 'width=1400'
    f = CACHE + '/' + hashlib.sha1(u.encode()).hexdigest()[:16]
    if not os.path.exists(f): open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read())
    return Image.open(f)
def cur(B, key):
    from fym_rack_images import shown
    best = None
    for k, n, t, h, b in shown(B):
        if k == key and b:
            im = Image.open(io.BytesIO(b));
            if best is None or im.width * im.height > best.width * best.height: best = im
    return best
def cut(im, c):
    im = im.convert('RGBA')
    if c.get('pre'):
        x0, y0, x1, y1 = c['pre']; W, Hh = im.size; im = im.crop((int(x0 * W), int(y0 * Hh), int(x1 * W), int(y1 * Hh)))
    a = np.asarray(im).astype(float); rgb = a[..., :3]; m = c.get('mask', 'rembg')
    if m == 'box':  # keep the brand photo on its own white background (clear/white racks that can't be cut cleanly): crop + quarter turn only
        o = im.convert('RGB').rotate(float(c.get('rot', 0)), expand=True, resample=Image.BICUBIC, fillcolor=(255, 255, 255))
        if c.get('post') == 'auto':  # tight to the photographed object (anything darker than the white backdrop) + small margin
            g = np.asarray(o).min(2) < 236; ys, xs = np.nonzero(g); p_ = 12
            o = o.crop((max(0, xs.min() - p_), max(0, ys.min() - p_), min(o.width, xs.max() + p_), min(o.height, ys.max() + p_)))
        elif c.get('post'): W, Hh = o.size; x0, y0, x1, y1 = c['post']; o = o.crop((int(x0 * W), int(y0 * Hh), int(x1 * W), int(y1 * Hh)))
        return o.convert('RGBA'), 1, [], c.get('rot', 0)
    if m == 'alpha': al = a[..., 3]
    elif m == 'rembg': al = rembg_alpha(im)
    else:
        bd = np.concatenate([rgb[:4].reshape(-1, 3), rgb[-4:].reshape(-1, 3), rgb[:, :4].reshape(-1, 3), rgb[:, -4:].reshape(-1, 3)])
        bg = np.array(c['bg'], float) if c.get('bg') else np.median(bd, 0); d = np.sqrt(((rgb - bg) ** 2).sum(2)); t = c.get('t', 28)
        al = np.clip((d - t * 0.5) / (t * 0.5), 0, 1) * 255
        al = np.minimum(al, a[..., 3])
    mb = al > 128
    if c.get('solid'):  # opaque rack: holes the matting punched into bright highlights are filled back in
        al = np.maximum(al, ndimage.binary_erosion(ndimage.binary_fill_holes(ndimage.binary_closing(mb, iterations=3)), iterations=2) * 255.0)
    mb = ndimage.binary_fill_holes(ndimage.binary_closing(mb, iterations=2)) if c.get('fill', True) else mb
    sp = c.get('split', 0); probe = ndimage.binary_erosion(mb, iterations=sp) if sp else mb
    lab, n = ndimage.label(probe)
    if not n: raise SystemExit('empty mask')
    W, Hh = im.size; pk = c.get('pick'); px, py = pk if isinstance(pk, list) else [0.5, 0.5]; px *= W; py *= Hh
    if c.get('pick') in ('largest', 'all') or 'pick' not in c:
        j = np.argmax(ndimage.sum(probe, lab, range(1, n + 1))) + 1
    else:
        ys, xs = np.nonzero(probe); q = np.argmin((xs - px) ** 2 + (ys - py) ** 2); j = lab[ys[q], xs[q]]
    keep = lab == j
    if c.get('pick') == 'all':  # a multi-colour / stacked set kept whole (only background removed + leveled)
        big = [i + 1 for i, s_ in enumerate(ndimage.sum(probe, lab, range(1, n + 1))) if s_ > 0.02 * probe.sum()]; keep = np.isin(lab, big)
    if sp: keep = ndimage.binary_dilation(keep, iterations=sp + 1) & mb
    sizes = ndimage.sum(probe, lab, range(1, n + 1))
    keep = ndimage.binary_dilation(keep, iterations=2)
    al = np.where(keep, al, 0)
    o = Image.fromarray(np.dstack([rgb, al]).astype(np.uint8), 'RGBA')
    ys, xs = np.nonzero(keep); r = cv2.minAreaRect(np.column_stack([xs, ys]).astype(np.float32)); (w_, h_), ang = r[1], r[2]
    rot = c.get('rot', 'auto')
    if rot == 'edge':  # level the longest straight outline edge (the rack's base), not the rack+pusher bounding box
        e = cv2.Canny((keep * 255).astype(np.uint8), 50, 150)
        L = cv2.HoughLinesP(e, 1, np.pi / 720, 60, minLineLength=int(max(keep.shape) * 0.3), maxLineGap=8)
        x1, y1, x2, y2 = [float(v) for v in max(np.asarray(L).reshape(-1, 4).astype(float), key=lambda l: (l[2] - l[0]) ** 2 + (l[3] - l[1]) ** 2)]
        t = np.degrees(np.arctan2(y2 - y1, x2 - x1)); t = (t + 90) % 180 - 90; deg = t + c.get('adj', 0)
    elif rot == 'auto': deg = ang if w_ >= h_ else ang - 90   # cv2 angle: rotate image by +deg (PIL ccw) to level the long side
    else: deg = float(rot)
    if c.get('flip'): deg += 180
    o = o.rotate(deg, resample=Image.BICUBIC, expand=True)
    o = o.crop(o.getchannel('A').point(lambda v: 255 if v > 24 else 0).getbbox())
    if o.height > o.width: o = o.rotate(90, expand=True)
    if c.get('defringe', True): o = defringe(o, whiteish_rack=c.get('white', False))
    o = o.crop(o.getchannel('A').point(lambda v: 255 if v > 24 else 0).getbbox())
    if c.get('trim'):  # [left, right] fractions trimmed off the ends (a stray bit of a neighbouring object at the end)
        l_, r_ = c['trim']; o = o.crop((int(l_ * o.width), 0, int(o.width * (1 - r_)), o.height)); o = o.crop(o.getchannel('A').point(lambda v: 255 if v > 24 else 0).getbbox())
    return o, int(n), [int(s) for s in sorted(sizes, reverse=True)[:6]], round(deg, 1)
if __name__ == '__main__':
    B = sys.argv[1]; only = set(sys.argv[2:]); C = json.load(open(CFG))['cuts']; os.makedirs(OUT, exist_ok=True)
    for name, c in C.items():
        if only and name not in only: continue
        im = cur(B, c['key']) if c['src'] == 'cur' else fetch(c['src'])
        o, n, sz, deg = cut(im, c)
        if o.width > 1200: o = o.resize((1200, round(o.height * 1200 / o.width)), Image.LANCZOS)
        o.save(OUT + name + '.webp', 'WEBP', quality=95, method=6); print(name, o.size, 'comps', n, sz, 'rot', deg)
