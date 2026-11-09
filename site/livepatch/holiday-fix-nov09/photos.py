import json, re, os, io, subprocess, urllib.parse, hashlib
import numpy as np
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)) + '/photos/'; os.makedirs(D, exist_ok=True)
def curl(u, binary=False):
    r = subprocess.run(['curl', '-sL', '--max-time', '60', '-A', 'Mozilla/5.0', u], capture_output=True)
    return r.stdout if binary else r.stdout.decode('utf8', 'ignore')
def parse(shop):
    u = urllib.parse.urlparse(shop); q = urllib.parse.parse_qs(u.query)
    path = u.path; dom = u.netloc
    if 'redirect' in q:
        r = urllib.parse.urlparse(q['redirect'][0]); path = r.path; q = urllib.parse.parse_qs(r.query)
    m = re.search(r'/products/([^/?#]+)', path)
    return dom, (m.group(1) if m else None), (q.get('variant') or [None])[0]
def hist(im):
    a = np.asarray(im.convert('RGB').resize((96, 96)), dtype=np.int32) // 32
    h = np.bincount((a[..., 0] * 64 + a[..., 1] * 8 + a[..., 2]).ravel(), minlength=512).astype(float)
    return h / h.sum()
def sim(a, b): return float(np.minimum(hist(a), hist(b)).sum())
def shopify_images(dom, handle):
    for d in (dom, 'www.' + dom if not dom.startswith('www.') else dom[4:]):
        t = curl(f'https://{d}/products/{handle}.json')
        try: return json.loads(t)['product']
        except Exception: pass
    return None
def best(shop, ref=None, name=None):
    """-> (local path, info) of the largest matching brand photo, or (None, why)"""
    dom, handle, variant = parse(shop)
    if not handle: return None, 'no product handle in ' + shop
    p = shopify_images(dom, handle)
    if not p: return None, f'no Shopify product json for {dom}/{handle}'
    imgs = p['images']
    cands = imgs
    if variant:
        v = next((v for v in p['variants'] if str(v['id']) == str(variant)), None)
        if v and v.get('image_id'): cands = [i for i in imgs if i['id'] == v['image_id']]
    elif name:
        v = next((v for v in p['variants'] if name.lower() in v['title'].lower()), None)
        if v and v.get('image_id'): cands = [i for i in imgs if i['id'] == v['image_id']]
    out = []
    for i in cands[:10]:
        f = D + hashlib.md5(i['src'].encode()).hexdigest() + '.jpg'
        if not os.path.exists(f): open(f, 'wb').write(curl(i['src'], True))
        try: im = Image.open(f); im.load()
        except Exception: continue
        s = sim(im, ref) if ref is not None and len(cands) > 1 else 1.0
        out.append((s, im.width * im.height, f, i['src']))
    if not out: return None, 'no images'
    out.sort(key=lambda x: (-round(x[0], 2), -x[1]))
    return out[0][2], {'src': out[0][3], 'sim': round(out[0][0], 3), 'n': len(cands), 'size': Image.open(out[0][2]).size}
