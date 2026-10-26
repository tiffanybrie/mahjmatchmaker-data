"""FYM v91 (Tiffany Oct 25 20:13: "The Grateful Dead photo being a product chart is a problem ... look for a better photo"):
only Sunshine Daydream used Bespoke's chart graphic (image 2/20); Rose Pink and Stealie Blue already use flat-lays. Swap in Bespoke's
own flat-lay of the Sunshine Daydream tiles (listing image 3/20, assets/tiles/v91/), same framing as the other two; pile thumb and
colour swatches re-cut from it.
Usage: python3 v91_gdphoto.py <build_dir>"""
import sys, os, io, json, base64, hashlib
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
K = 'www.bespokemahjong.com/bespoke-x-grateful-dead-mahjong-tiles-sunshine-daydream'; t = D['tiles'][K]
src = REPO + 'assets/tiles/v91/bespoke-grateful-dead-sunshine-daydream.jpg'
im = Image.open(src).convert('RGB'); os.makedirs(B + '/t91', exist_ok=True); fn = 't91/bespoke-grateful-dead-sunshine-daydream.jpg'
c = im.copy(); c.thumbnail((1000, 1000)); c.save(B + '/' + fn, quality=88)
q = min(im.size); sq = im.crop(((im.width - q) // 2, (im.height - q) // 2, (im.width - q) // 2 + q, (im.height - q) // 2 + q)).resize((360, 360), Image.LANCZOS)
b = io.BytesIO(); sq.save(b, 'JPEG', quality=84); pk = 'p91' + hashlib.md5(fn.encode()).hexdigest()[:10]
t['full'] = fn; t['pile'] = pk
a = np.asarray(im.resize((72, 72))).astype(float).reshape(-1, 3) / 255; a = a[~((a.min(1) > .82) & (a.max(1) - a.min(1) < .12))]
L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3); km = KMeans(n_clusters=6, n_init=3, random_state=0).fit(L); cnt = np.bincount(km.labels_, minlength=6) / len(L)
sw = [['#%02x%02x%02x' % tuple(int(round(x * 255)) for x in np.clip(lab2rgb(km.cluster_centers_[j].reshape(1, 1, 3)).reshape(3), 0, 1)), round(float(cnt[j]), 3)] for j in np.argsort(-cnt) if cnt[j] >= .05]
C = json.load(open(REPO + 'config/fym-colour-oct25.json'))
s = next(x for x in D['sets'] if x['tile'] == K); C['sets'][s['slug']] = {'sw': sw, 'tone': None, 'src': 'photo', 'back': None}
json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps({pk: 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()}, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h); print('Sunshine Daydream ->', fn)
