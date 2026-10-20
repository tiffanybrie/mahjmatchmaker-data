"""Find a higher-resolution copy of each mat photo on the brand's Shopify product page (products/<handle>.js), matched
to the photo Tiffany swiped (grayscale correlation at 64px). Usage: hd_fetch.py list.json srcdir outdir
list.json: [{vote_id, mat, url}]; writes outdir/<vote_id>.jpg + outdir/report.json"""
import json, sys, re, io, os, subprocess
import numpy as np
from PIL import Image
L = json.load(open(sys.argv[1])); SRC = sys.argv[2]; OUT = sys.argv[3]; os.makedirs(OUT, exist_ok=True)
def get(u, binary=False):
    r = subprocess.run(['curl', '-sSL', '--max-time', '40', '-A', 'Mozilla/5.0', u], capture_output=True)
    return r.stdout if binary else r.stdout.decode('utf8', 'ignore')
def trim(im):
    g = im.convert('L').point(lambda p: 255 if p < 238 else 0); b = g.getbbox(); return im.crop(b) if b else im
def sig(im):
    im = trim(im); g = np.asarray(im.convert('L').resize((64, 64))).astype(float); g -= g.mean(); return g / (np.linalg.norm(g) + 1e-9)
rep = {}
for it in L:
    k = it['vote_id']; u = it.get('url') or ''
    m = re.match(r'(https?://[^/]+)/products/([^/?#]+)', u)
    if not m: rep[k] = {'mat': it['mat'], 'status': 'no product url'}; continue
    try: p = json.loads(get(f'{m.group(1)}/products/{m.group(2)}.js'))
    except Exception as e: rep[k] = {'mat': it['mat'], 'status': 'no product json'}; print(k, rep[k]); continue
    cur = trim(Image.open(f'{SRC}/{k}.jpg').convert('RGB')); cs = sig(cur); best = None
    for src in p.get('images', [])[:12]:
        s = ('https:' + src) if src.startswith('//') else src
        try: im = Image.open(io.BytesIO(get(s, True))).convert('RGB')
        except Exception: continue
        c = float((sig(im) * cs).sum())
        if best is None or c > best[0]: best = (c, trim(im), s)
    if best and best[0] > .9 and best[1].width > cur.width * 1.08:
        best[1].save(f'{OUT}/{k}.jpg', quality=95); rep[k] = {'mat': it['mat'], 'status': 'upgraded', 'corr': round(best[0], 3), 'from': list(cur.size), 'to': list(best[1].size), 'src': best[2]}
    else:
        rep[k] = {'mat': it['mat'], 'status': 'kept', 'corr': round(best[0], 3) if best else None, 'best_size': list(best[1].size) if best else None, 'cur': list(cur.size)}
    print(k, rep[k])
json.dump(rep, open(f'{OUT}/report.json', 'w'), indent=1)
