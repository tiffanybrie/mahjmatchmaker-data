#!/usr/bin/env python3
"""Tile-photo identity check: fails when a set's asset shows ANOTHER set's tile photo.

Why (Tiffany, Oct 21 12:10): the live Heritage 2.0 colour card ("The Tile Edit") showed the Heritage 1
tile pile + Heritage 1 burl swatch. "The whole point of that color card is to show the difference between
Heritage 1 and 2." Same mistake hit the swipe books on Oct 15 (scripts/swipe/canon_tiles.py). CLAUDE.md
rule 8: a reported bug gets an automated check the same day.

How it works
- Canonical tile photos = assets/tiles/album/* (one per set; aliases below). These are the ONLY photos that
  count as "set X's photo".
- Every asset image is matched against ALL canonical photos with SIFT features + one FLANN index (votes per
  canonical), then the top candidates are verified with a RANSAC homography. A real crop / resize of the same
  photo gives a large inlier count (typically 80-1000+). Sister sets with the same face artwork (Heritage 1 vs
  2.0) are different PHOTOS, so they only share a handful of inliers (one tile's artwork at most).
- An asset is attributed to a set from its filename (`<nn->?<set>-mahjong-tiles...`, `album/<set>.jpg`,
  `colorcards/<set>/`, FYM key) or an explicit expected set.
- FAIL  = the asset strongly matches a canonical photo of a DIFFERENT set (>= STRONG inliers and well above
          its own set's score). This is the Heritage-1-on-Heritage-2.0 bug.
- WARN  = no strong match at all (asset uses some non-canonical photo, e.g. a product shot); listed for a
          human look, never a failure.

Usage
  python3 builder/photo_identity_check.py --dirs assets/colorcards assets/covers/albums assets/social/pinterest/pins
  python3 builder/photo_identity_check.py --live-pages            # curl every *-tile-matches page on the live site
  python3 builder/photo_identity_check.py --fym <build_dir>       # FYM index.html (const D) tile photos
  python3 builder/photo_identity_check.py --files a.jpg=heritage-2-0 b.jpg=heritage
  Add --json out.json to save results; exit code 1 on any FAIL.
fym_gate.py can import check_fym(build_dir) -> list of failure strings.
"""
import os, re, sys, json, glob, io, hashlib, base64, subprocess
import numpy as np
import cv2

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CANON_DIR = os.path.join(REPO, 'assets/tiles/album')
CANON_DIRS = [CANON_DIR, os.path.join(REPO, 'assets/tiles/holiday')]  # holiday sets have no album photo: their pile shots count too
STRONG = 40          # RANSAC inliers that mean "this is that photo"
SIM_MIN = 0.85      # same-photo colour high-pass correlation after warping (true crops 0.87-1.0; Virora grid look-alikes <= 0.77)
COLOR_MAX = 14.0    # mean |RGB| difference in the matched area: true crops 0.3-8.5; Holly Jolly red vs green grid, Virora 13-50
HULL_MIN = 0.15     # matched area must cover >= 15% of the canonical photo (one shared tile artwork covers far less)
MARGIN = 2.0         # other-set score must beat own-set score by this factor to FAIL

# filename stem in assets/tiles/album -> set slug (only where they differ)
CANON_ALIAS = {
    'heritage-2-0-full': 'heritage-2-0', 'petalee-pile': 'petalee', 'sunday-tile-set-hd': 'sunday-tile-set',
    'classic-tortoise-zoom': 'classic-tortoise', 'cypress': 'cypress-forest',
    'holly-jolly-pink-pile': 'holly-jolly-pink', 'holly-jolly-red-pile': 'holly-jolly-red', 'tinselle-emerald-3x3': 'tinselle-emerald',
    'tinselle-ruby-3x3': 'tinselle-ruby', 'plm-spirit-of-christmas-faces-back': 'spirit-of-christmas',
}
# asset-side slug -> canonical set slug
SET_ALIAS = {
    'tortoise': 'classic-tortoise', 'cypress': 'cypress-forest', 'sunday': 'sunday-tile-set',
    'loveshackfancy-coquette': 'coquette', 'heritage-1': 'heritage', 'heritage-1-0': 'heritage',
    'heritage-2': 'heritage-2-0',
}
_SIFT = None
def sift():
    global _SIFT
    if _SIFT is None: _SIFT = cv2.SIFT_create(nfeatures=1000)
    return _SIFT

def load_rgb(src, max_side=1100):
    """RGB uint8 array, alpha composited on white (PNG tile photos), longest side <= max_side."""
    from PIL import Image
    try:
        im = Image.open(io.BytesIO(src) if isinstance(src, (bytes, bytearray)) else src)
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[3]); im = bg
        a = np.asarray(im.convert('RGB'))
    except Exception:
        return None
    h, w = a.shape[:2]; s = max_side / max(h, w)
    if s < 1: a = cv2.resize(a, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    return np.ascontiguousarray(a)

def load_gray(src, max_side=1100):
    a = load_rgb(src, max_side)
    return None if a is None else cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)

def norm_set(s):
    s = (s or '').lower()
    s = re.sub(r'^irl-', '', s)
    return SET_ALIAS.get(s, s)

class Canon:
    def __init__(self):
        self.labels, self.kps, self.descs, self.grays = [], [], [], []
        for p in sorted(f for d_ in CANON_DIRS for f in glob.glob(d_ + '/*')):
            if not re.search(r'\.(jpe?g|png|webp)$', p, re.I): continue
            stem = os.path.splitext(os.path.basename(p))[0]
            c = load_rgb(p, 1100); g = cv2.cvtColor(c, cv2.COLOR_RGB2GRAY)
            kp, d = sift().detectAndCompute(g, None)
            if d is None: continue
            self.labels.append(norm_set(CANON_ALIAS.get(stem, stem))); self.kps.append(kp); self.descs.append(d); self.grays.append(c)
        self.sets = sorted(set(self.labels))
        allD = np.vstack(self.descs).astype(np.float32)
        self.owner = np.concatenate([np.full(len(d), i) for i, d in enumerate(self.descs)])
        self.offset = np.cumsum([0] + [len(d) for d in self.descs])
        self.flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=64))
        self.flann.add([allD]); self.flann.train()

    def score(self, src, max_side=1100, detail=None):
        """-> {set_slug: inliers} for the top candidates (sets not listed scored ~0). A candidate counts only when the
        asset, warped onto the canonical photo, is the SAME PHOTO there (pixel NCC over the inlier hull >= SIM_MIN):
        brands that shoot every set in one identical grid layout (Virora) share geometry but not pixels."""
        rgb = load_rgb(src, max_side)
        if rgb is None: return None
        g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        kp, d = sift().detectAndCompute(g, None)
        if d is None or len(kp) < 10: return {}
        ms = self.flann.knnMatch(d.astype(np.float32), k=2)
        good = [m for m, n in (x for x in ms if len(x) == 2) if m.distance < 0.75 * n.distance]
        by = {}
        for m in good:
            ci = int(self.owner[m.trainIdx]); by.setdefault(ci, []).append(m)
        out = {}
        for ci, lst in sorted(by.items(), key=lambda x: -len(x[1]))[:6]:
            if len(lst) < 8: continue
            src_pts = np.float32([kp[m.queryIdx].pt for m in lst])
            dst_pts = np.float32([self.kps[ci][m.trainIdx - self.offset[ci]].pt for m in lst])
            H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 6.0)
            n = int(mask.sum()) if mask is not None else 0
            sim = self.same_photo(rgb, H, dst_pts[mask.ravel() == 1], ci) if n >= 12 else 0.0
            if detail is not None: detail[self.labels[ci]] = max(detail.get(self.labels[ci], (0, 0)), (n, round(sim, 3)))
            if sim < SIM_MIN: n = 0
            lab = self.labels[ci]; out[lab] = max(out.get(lab, 0), n)
        return out

    def same_photo(self, rgb, H, pts, ci):
        """Same-photo score in [0,1]: colour high-pass NCC between the canonical photo and the asset warped onto it,
        inside the hull of the RANSAC inliers. 0 when that hull covers < HULL_MIN of the canonical photo: sets that
        share face artwork (Virora Floréa vs Petalee, Heritage 1 vs 2.0) can match ONE identical tile, never a large area;
        and 0 when the colours differ (> COLOR_MAX): colourways shot in one identical grid (Holly Jolly red vs green)."""
        try:
            c = self.grays[ci]; h, w = c.shape[:2]
            hull = cv2.convexHull(pts.astype(np.int32))
            if cv2.contourArea(hull) < HULL_MIN * h * w: return 0.0
            wa = cv2.warpPerspective(rgb, H, (w, h), flags=cv2.INTER_AREA)
            m = np.zeros((h, w), np.uint8); cv2.fillConvexPoly(m, hull, 1)
            m &= (cv2.warpPerspective(np.ones(rgb.shape[:2], np.uint8), H, (w, h)) > 0).astype(np.uint8)
            m = cv2.erode(m, np.ones((5, 5), np.uint8)) > 0
            if m.sum() < 400: return 0.0
            hp = lambda z: z - cv2.GaussianBlur(z, (0, 0), 6)
            if float(np.abs(c[m].astype(float) - wa[m].astype(float)).mean()) > COLOR_MAX: return 0.0  # same layout, other colourway
            a = hp(c.astype(np.float32))[m].astype(float); b = hp(wa.astype(np.float32))[m].astype(float)
            a -= a.mean(); b -= b.mean(); den = np.sqrt((a * a).sum() * (b * b).sum())
            return float((a * b).sum() / den) if den else 0.0
        except Exception:
            return 0.0

def judge(scores, expected):
    """-> (status, best_set, best, own)"""
    if scores is None: return 'ERROR', None, 0, 0
    exp = norm_set(expected)
    own = scores.get(exp, 0)
    others = {k: v for k, v in scores.items() if k != exp}
    bset, best = (max(others.items(), key=lambda x: x[1]) if others else (None, 0))
    if best >= STRONG and best > MARGIN * max(own, 1): return 'FAIL', bset, best, own
    if own >= STRONG: return 'OK', exp, own, own
    return 'WARN', bset, best, own

SET_RX = re.compile(r'(?:^|/)(?:\d+-)?([a-z0-9]+(?:-[a-z0-9]+)*?)-mahjong-tiles')
def set_from_name(path):
    b = path.lower()
    fn = b.split('/')[-1]
    if fn.startswith('my-favorite-'):  # blog "my favorite <colour> tiles" collages show several sets: only a named set counts
        k = re.sub(r'-(mahjong-)?tiles.*$', '', fn[len('my-favorite-'):])
        return norm_set(k) if norm_set(k) in KNOWN_SETS else None
    m = re.search(r'colorcards/([a-z0-9-]+)/', b) or re.search(r'tiles/album/([a-z0-9-]+)\.', b)
    if m: return norm_set(CANON_ALIAS.get(m.group(1), m.group(1)))
    m = SET_RX.search(b.split('/')[-1])
    if m: return norm_set(m.group(1))
    m = re.search(r'covers/albums/uniform-v3/([a-z0-9-]+)\.', b)
    if m: return norm_set(m.group(1))
    # fallback: longest known set slug appearing as a whole token in the path (heritage-2-0 beats heritage)
    known = sorted(set(KNOWN_SETS) | set(SET_ALIAS), key=len, reverse=True)
    for k in known:
        if re.search(r'(^|[/_.-])' + re.escape(k) + r'($|[/_.-])', b) and not re.search(re.escape(k) + r'-(mat|rack)', b):
            return norm_set(k)
    return None

KNOWN_SETS = sorted({norm_set(CANON_ALIAS.get(os.path.splitext(f)[0], os.path.splitext(f)[0]))
                     for d_ in CANON_DIRS for f in os.listdir(d_) if re.search(r'\.(jpe?g|png|webp)$', f, re.I)})

def run(items, C=None, quiet=False):
    """items: list of (label/url, local path or bytes, expected set) -> results list"""
    C = C or Canon(); res = []
    for name, src, exp in items:
        if norm_set(exp) not in C.sets and not exp: continue
        sc = C.score(src)
        st, bset, best, own = judge(sc, exp)
        if norm_set(exp) not in C.sets and st != 'FAIL': st = 'NOCANON'
        r = dict(asset=name, expected=norm_set(exp), status=st, best_other=bset, best=best, own=own,
                 top=dict(sorted((sc or {}).items(), key=lambda x: -x[1])[:3]))
        res.append(r)
        if not quiet and st == 'FAIL': print('FAIL', name, 'expected', r['expected'], '-> looks like', bset, best, 'own', own)
    return res

def check_fym(build_dir, C=None):
    """FYM: no tile photo (full or pile) may be ANOTHER set's canonical album photo. -> list of failure strings."""
    items, F = fym_items(build_dir, guard=True)
    return F + [f"{r['asset']}: shows {r['best_other']}'s album photo ({r['best']} inliers vs own {r['own']})"
                for r in run(items, C, quiet=True) if r['status'] == 'FAIL']

def _name_slug(n):
    n = re.sub(r'\b1\.0\b', '', (n or '').lower())
    return re.sub(r'[^a-z0-9]+', '-', n).strip('-')

def fym_items(build_dir, guard=False):
    """(label, bytes|path, expected set) for every FYM tile photo: D.tiles[k].full (file) + .pile (window.IMG hash).
    Expected set (Oct 21 fix: D.sets slugs are brand-prefixed, e.g. 'sunday-mahjong-plum-panda', and OMM's key
    jubilee-mahjong-tiles IS Papaya Spritz) = the canonical album photo named in .src, else the tile's display name.
    guard=True also returns failures where the tile's NAME is a canonical set but .src points at another set's photo."""
    html = open(os.path.join(build_dir, 'index.html')).read()
    i = html.find('const D='); D, _ = json.JSONDecoder().raw_decode(html, i + 8)
    IMG = {}
    for js in glob.glob(os.path.join(build_dir, 'b*.js')):
        for k, v in re.findall(r'"([0-9a-f]{10})":"(data:image/[^"]+)"', open(js).read()): IMG[k] = v
    items, F = [], []
    for key, t in (D.get('tiles') or {}).items():
        src_set = None
        m = re.search(r'tiles/(?:album|holiday)/([a-z0-9-]+)\.', t.get('src') or '')
        if m: src_set = norm_set(CANON_ALIAS.get(m.group(1), m.group(1)))
        nm = norm_set(_name_slug(t.get('n') or key))
        if src_set and nm in KNOWN_SETS and nm != src_set:
            F.append(f"FYM {key} ({t.get('n')}): src is {src_set}'s album photo, but the tile is {nm}")
        exp = src_set or nm
        if t.get('full') and os.path.exists(os.path.join(build_dir, t['full'])):
            items.append((f"FYM {key} full", os.path.join(build_dir, t['full']), exp))
        if t.get('pile') in IMG:
            items.append((f"FYM {key} pile", base64.b64decode(IMG[t['pile']].split(',', 1)[1]), exp))
    return (items, F) if guard else items

def live_items(cache):
    os.makedirs(cache, exist_ok=True)
    sm = subprocess.run(['curl', '-sS', '-A', 'Mozilla/5.0', 'https://www.mahjmatchmaker.com/sitemap.xml'], capture_output=True, text=True).stdout
    pages = re.findall(r'<loc>([^<]+)</loc>', sm)
    urls = {}
    for u in pages:
        h = subprocess.run(['curl', '-sS', '-A', 'Mozilla/5.0', u], capture_output=True, text=True).stdout
        for x in re.findall(r'https://(?:cdn\.jsdelivr\.net|images\.squarespace-cdn\.com)[^"\'\s\)]+?\.(?:jpg|jpeg|png|webp)', h, re.I):
            urls.setdefault(x.split('?')[0], u)
    items = []
    for x in urls:
        s = set_from_name(x)
        if not s: continue
        f = os.path.join(cache, hashlib.md5(x.encode()).hexdigest()[:12])
        if not os.path.exists(f):
            subprocess.run(['curl', '-sS', '-m', '60', '-o', f, x + ('?format=1000w' if 'squarespace-cdn' in x else '')])
        items.append((x, f, s))
    return items

def main(a):
    js = None
    if '--json' in a: i = a.index('--json'); js = a[i + 1]; del a[i:i + 2]
    items = []
    if a and a[0] == '--dirs':
        for d in a[1:]:
            for p in sorted(glob.glob(os.path.join(REPO, d, '**/*'), recursive=True)):
                if re.search(r'\.(jpe?g|png|webp)$', p, re.I) and set_from_name(p):
                    items.append((os.path.relpath(p, REPO), p, set_from_name(p)))
    elif a and a[0] == '--live-pages':
        items = live_items(os.environ.get('PIC_CACHE', '/tmp/photo_identity_cache'))
    elif a and a[0] == '--fym':
        f = check_fym(a[1]); print('\n'.join(f) or 'FYM tile photos: OK'); sys.exit(1 if f else 0)
    elif a and a[0] == '--files':
        for x in a[1:]:
            p, s = x.rsplit('=', 1); items.append((p, p, s))
    else:
        print(__doc__); sys.exit(2)
    res = run(items)
    n = {k: sum(r['status'] == k for r in res) for k in ('OK', 'FAIL', 'WARN', 'NOCANON', 'ERROR')}
    print('photo identity:', n)
    if js: json.dump(res, open(js, 'w'), indent=1)
    sys.exit(1 if n['FAIL'] else 0)

if __name__ == '__main__':
    main(sys.argv[1:])
