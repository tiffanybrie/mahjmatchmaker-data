"""FYM v89 tile photo framing (Tiffany Oct 24 9:45pm form + Oct 25 16:36: "The boots and bubbles blue tile is out of frame ...
all those get adjusted"). The card draws the tile photo as a wide band (Mood board, ~3.9:1), a portrait box (Showcase) and a circle
(Love triangle); tall photos with pouches / boxes / white space showed empty white, a pouch or one row of faces.
1. config/fym-tile-focus-oct25.json (90 sets, boxes picked by eye + verified on contact sheets): each photo is cropped to its box
   -> t89/<name>.jpg; t.full points at it (swipe screens and the card use the same photo, gate [44]). Grid thumbnails (pile) are
   re-cut from the cropped photo, except locked album piles. t.fo keeps the original path; locks and the album-photo gate checks compare against t.fo.
2. Every set gets the best band / portrait anchor for its photo (t.bf=[fx,fy] band, t.pf=[fx,fy] portrait) by maximising how much of
   the crop is tiles (not white background), so two-tray photos land on the tiles instead of the gap. Card cover() calls use them.
Usage: python3 v89_tilefocus.py <build_dir>"""
import sys, os, io, json, base64, hashlib, re
import numpy as np
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
T = D['tiles']; FOC = json.load(open(REPO + 'config/fym-tile-focus-oct25.json'))
LP = REPO + 'builder/fym_flags/locks.json'; L = json.load(open(LP))
os.makedirs(B + '/t89', exist_ok=True); IMG = {}; nc = 0
for k, t in T.items():
    f = t.get('full'); fo = FOC.get(f)
    if not fo or not os.path.exists(B + '/' + f): continue
    im = Image.open(B + '/' + f).convert('RGB'); W, H = im.size; x0, y0, x1, y1 = fo['box']
    c = im.crop((round(x0 * W), round(y0 * H), round(x1 * W), round(y1 * H))); c.thumbnail((1000, 1000))
    nf = 't89/' + re.sub(r'[^a-z0-9]+', '-', os.path.splitext(f)[0].lower()).strip('-') + '.jpg'; c.save(B + '/' + nf, quality=88)
    lk = L['tiles'].get(k)
    if lk and lk.get('full') == f: pass   # locked album photo: lock stays on the original (t.fo); locked pile kept
    else:
        q = min(c.size); sq = c.crop(((c.width - q) // 2, (c.height - q) // 2, (c.width - q) // 2 + q, (c.height - q) // 2 + q)).resize((360, 360), Image.LANCZOS)
        b = io.BytesIO(); sq.save(b, 'JPEG', quality=84); pk = 'p89' + hashlib.md5(nf.encode()).hexdigest()[:10]
        IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode(); t['pile'] = pk
    t['fo'] = f; t['full'] = nf; nc += 1
    if fo.get('band'): t['bf'] = fo['band']   # Close up band anchor picked by eye (QA v90: two-tray photos)   # fo = original photo (gate [1]/[3c]/[30] + locks compare against it)
def score(a):  # share of the crop that is tiles: not near-white background, saturated colour counts extra
    bg = (a.min(2) > 225) & ((a.max(2) - a.min(2)) < 18); sat = (a.max(2) - a.min(2)) > 60
    return float((~bg).mean() + .5 * sat.mean())
def best(im, ar, zoom):
    W, H = im.size; k = max(ar / W, 1 / H) * zoom; cw, ch = ar / k, 1 / k   # crop size in image px
    a = np.asarray(im.resize((240, max(1, round(240 * H / W))))).astype(int); s = 240 / W
    cands = [(fx, fy) for fx in (0, .15, .3, .5, .7, .85, 1) for fy in (0, .15, .3, .45, .6, .75, .9, 1)]
    def sc(fx, fy):
        x0 = (W - cw) * fx; y0 = (H - ch) * fy
        return score(a[int(y0 * s):int((y0 + ch) * s) + 1, int(x0 * s):int((x0 + cw) * s) + 1])
    base = sc(.5, .45); top = max(cands, key=lambda p: sc(*p) - (0.02 if p != (.5, .45) else 0))
    return (list(top) if sc(*top) > base + .06 else None), base, sc(*top)
nb = npf = 0
AUTO_ANCHORS = False   # QA v89: automatic band/portrait anchors made ~30 sets worse (corner anchors on background); off
for s in (D['sets'] if AUTO_ANCHORS else []):
    t = T.get(s['tile']) or {}; f = t.get('full')
    if not f or not os.path.exists(B + '/' + f): continue
    im = Image.open(B + '/' + f).convert('RGB')
    bf, _, _ = best(im, 3.87, 1.05); pf, _, _ = best(im, .78, 1.12)
    t.pop('bf', None); t.pop('pf', None)
    if bf: t['bf'] = bf; nb += 1
    if pf: t['pf'] = pf; npf += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
def rep(a, b):
    global h
    assert h.count(a) == 1, a; h = h.replace(a, b)

rep("cover(tile,x,top,w,hT,22,1.05,.5,.45);", "cover(tile,x,top,w,hT,22,1.05,...(T[s.tile].bf||[.5,.45]));")
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
print('reframed', nc, '| band anchors', nb, '| portrait anchors', npf)
