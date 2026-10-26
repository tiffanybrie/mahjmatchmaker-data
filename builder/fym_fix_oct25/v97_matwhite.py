"""FYM v97 (Version 1.1): mat photos fill the frame (Tiffany Oct 26 5:49pm: white bands on the match card + swipe, e.g. Amahj
Blue, Citron + Lilac). config/fym-mat-white-oct26.json: 'trim' cuts flat white margins (rows/cols > 97% near-white), 'replace'
uses a flattened photo (Main's perspective warp for the Amahj angled shot). New images go in a new chunk (like v90_matfocus),
thumbnails re-cut, colours re-measured from the new photo (config/fym-colour-oct25.json + M.ms). M.f0/th0 keep the originals
for locks. Idempotent (skips mats already carrying w97). Gate [89]. Usage: v97_matwhite.py <build>"""
import sys, os, io, json, struct, re, base64, hashlib
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i; M = D['mats']
CFG = json.load(open(REPO + 'config/fym-mat-white-oct26.json'))['mats']
imgs = {}
for fn in os.listdir(B + '/mc'):
    if fn.endswith('.webp'):
        raw = open(B + '/mc/' + fn, 'rb').read(); n = struct.unpack('<I', raw[-4:])[0]
        for f, (a, l) in json.loads(raw[-4 - n:-4]).items(): imgs[f] = raw[a:a + l]
def kmeans_sw(im, k=8, minw=.03):   # same as v90_matfocus
    a = np.asarray(im.convert('RGB').resize((72, 72))).astype(float).reshape(-1, 3) / 255; a = a[~(a.min(1) > .94)]
    L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3); km = KMeans(n_clusters=k, n_init=3, random_state=0).fit(L)
    cnt = np.bincount(km.labels_, minlength=k) / len(L); out = []
    for j in np.argsort(-cnt):
        if cnt[j] < minw: continue
        rgb = np.clip(lab2rgb(km.cluster_centers_[j].reshape(1, 1, 3)).reshape(3), 0, 1)
        out.append(['#%02x%02x%02x' % tuple(int(round(x * 255)) for x in rgb), round(float(cnt[j]), 3)])
    return out
def trim(im):
    a = np.asarray(im).astype(int); wh = (a.min(2) > 235) & ((a.max(2) - a.min(2)) < 16)
    cols = np.where(wh.mean(0) <= .97)[0]; rows = np.where(wh.mean(1) <= .97)[0]
    return im.crop((int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1))
C = json.load(open(REPO + 'config/fym-colour-oct25.json'))
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); MCN = int(re.search(r'MCN=(\d+)', h).group(1))
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values() if str(o.get('f', '')).startswith('m/'))
chunk = max(max(int(v) for v in mcb.group(1).split(',')) + 1, maxN // MCN + 1); nid = chunk * MCN
CH, IMG, done = {}, {}, []   # chunk id -> [body, hdr]
for k, fo in CFG.items():
    m = M.get(k)
    if not m or m.get('w97') or m.get('hid'): continue
    im = Image.open(REPO + fo['img']).convert('RGB') if fo['action'] == 'replace' else trim(Image.open(io.BytesIO(imgs[m['f']])).convert('RGB'))
    if max(im.size) > 1200: im.thumbnail((1200, 1200), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=88); raw = b.getvalue(); f = f'm/{nid}.webp'; c_ = nid // MCN; nid += 1
    bh = CH.setdefault(c_, [b'', {}]); bh[1][f] = [len(bh[0]), len(raw)]; bh[0] += raw
    t = im.copy(); t.thumbnail((220, 220)); tb = io.BytesIO(); t.save(tb, 'WEBP', quality=72); th = 'mt97' + hashlib.md5(f.encode()).hexdigest()[:8]
    IMG[th] = 'data:image/webp;base64,' + base64.b64encode(tb.getvalue()).decode()
    if not m.get('f0'): m['f0'] = m['f']; m['th0'] = m.get('th')
    m['f'] = f; m['th'] = th; m['w'], m['h'] = im.size; m['w97'] = fo['action']
    sw = kmeans_sw(im); C['mats'][k] = {'sw': sw, 'tone': C['mats'].get(k, {}).get('tone')}; m['ms'] = sw; done.append(f"{m.get('bn')} | {m['n']} ({fo['action']})")
if done:
    for c_, (body, hdr) in CH.items():
        hj = json.dumps(hdr, separators=(',', ':')).encode(); open(f'{B}/mc/{c_}.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
    h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + ''.join(f', {c_}' for c_ in CH) + ']);', 1)
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
    open(P, 'w').write(h); json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
print('\n'.join(done)); print('v97 matwhite', len(done), 'chunks', list(CH))
