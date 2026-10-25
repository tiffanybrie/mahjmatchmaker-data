"""FYM v90 (Tiffany Oct 25 16:58, Cypress showed Splash of Color 'Preppy Animal Print' as a far-away AI living-room render:
"If that's our best photo, it can't be that far away. We're mostly showing a room."). An agent audited all 793 visible mat photos;
4 had the mat too small in the frame (config/fym-mat-focus-oct25.json, boxes verified by eye). Each is cropped to the mat and packed
into a new image chunk (ids 2100+), its thumbnail re-cut, and its colours re-measured from the crop (config/fym-colour-oct25.json),
so the colour ranking no longer reads the room. Gate [50] keeps them cropped.
Usage: python3 v90_matfocus.py <build_dir>"""
import sys, os, io, json, struct, re, base64, hashlib
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i; M = D['mats']
FOC = json.load(open(REPO + 'config/fym-mat-focus-oct25.json'))
imgs = {}
for fn in os.listdir(B + '/mc'):
    if fn.endswith('.webp'):
        raw = open(B + '/mc/' + fn, 'rb').read(); n = struct.unpack('<I', raw[-4:])[0]
        for f, (a, l) in json.loads(raw[-4 - n:-4]).items(): imgs[f] = raw[a:a + l]
def kmeans_sw(im, k=8, minw=.03):
    a = np.asarray(im.convert('RGB').resize((72, 72))).astype(float).reshape(-1, 3) / 255; a = a[~(a.min(1) > .94)]
    L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3); km = KMeans(n_clusters=k, n_init=3, random_state=0).fit(L)
    cnt = np.bincount(km.labels_, minlength=k) / len(L); out = []
    for j in np.argsort(-cnt):
        if cnt[j] < minw: continue
        rgb = np.clip(lab2rgb(km.cluster_centers_[j].reshape(1, 1, 3)).reshape(3), 0, 1)
        out.append(['#%02x%02x%02x' % tuple(int(round(x * 255)) for x in rgb), round(float(cnt[j]), 3)])
    return out
C = json.load(open(REPO + 'config/fym-colour-oct25.json'))
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); MCN = int(re.search(r'MCN=(\d+)', h).group(1))
chunk = max(int(v) for v in mcb.group(1).split(',')) + 1; nid = chunk * MCN
body, hdr, IMG = b'', {}, {}
for k, fo in FOC.items():
    if fo.get('action') != 'crop' or k not in M: continue
    m = M[k]; im = Image.open(io.BytesIO(imgs[m['f']])).convert('RGB'); W, H = im.size; x0, y0, x1, y1 = fo['box']
    c = im.crop((round(x0 * W), round(y0 * H), round(x1 * W), round(y1 * H)))
    b = io.BytesIO(); c.save(b, 'WEBP', quality=88); raw = b.getvalue(); f = f'm/{nid}.webp'; nid += 1
    hdr[f] = [len(body), len(raw)]; body += raw
    t = c.copy(); t.thumbnail((300, 300)); tb = io.BytesIO(); t.save(tb, 'WEBP', quality=80); th = 'mt90' + hashlib.md5(f.encode()).hexdigest()[:8]
    IMG[th] = 'data:image/webp;base64,' + base64.b64encode(tb.getvalue()).decode()
    m['f0'] = m['f']; m['th0'] = m.get('th'); m['f'] = f; m['th'] = th; m['w'], m['h'] = c.size
    sw = kmeans_sw(c); C['mats'][k] = {'sw': sw, 'tone': C['mats'].get(k, {}).get('tone')}; m['ms'] = sw
    print('cropped', m['bn'], '|', m['n'], '->', f, c.size)
hj = json.dumps(hdr, separators=(',', ':')).encode(); open(f'{B}/mc/{chunk}.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + f', {chunk}]);', 1)
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h); json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
print('chunk', chunk)
