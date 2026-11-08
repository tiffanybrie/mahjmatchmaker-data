"""Vendor photo candidates for Table view (Nov 7). For each mat key: the store's product JSON (Shopify /products/<handle>.json;
the mat's u0/u link), EVERY product image analysed with matfit_nov07.analyze (studio backdrop -> mat quad), plus the app's own
FYM photo. Writes a small straightened preview per candidate and a JSON with the source URL + measures; a contact sheet per
mat row (FYM photo first) is made for the by-eye pick. Only vendor photos, never AI.
Usage: python3 vendor_cands_nov07.py <build dir> <keys.json> <out dir>"""
import sys, os, json, re, io, urllib.request, urllib.parse, concurrent.futures as cf
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from matimg import load_D, mat_full
from matfit_nov07 import analyze, warp_square
B, KJ, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True)
D = load_D(B); M = D['mats']; keys = json.load(open(KJ))
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36'}
def get(url, t=25):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=t).read()
def product_url(m):
    for u in (m.get('u0'), m.get('u')):
        if not u: continue
        q = urllib.parse.urlparse(u)
        if 'redirect=' in (q.query or ''):
            r = urllib.parse.parse_qs(q.query)['redirect'][0]; u = f'{q.scheme}://{q.netloc}{r}'; q = urllib.parse.urlparse(u)
        mm = re.search(r'/products/([^/?#]+)', q.path or '')
        if mm: return f'{q.scheme}://{q.netloc}/products/{mm.group(1)}'
    return None
def score(a):
    if a.get('kind') != 'studio': return 0
    s = 1.0
    s *= max(0, 1 - abs(a['fill'] - 1.01) * 6); s *= max(0, (a['aspect'] - .85) / .15); s *= min(1, a.get('mat_share', 0) / .35)
    return round(s, 3)
def one(idx_k):
    idx, k = idx_k; m = M[k]; rec = {'k': k, 'n': f"{m['bn']} | {m['n']}", 'c': []}
    try:
        im = mat_full(B, m['f']); a = analyze(im); a['src'] = 'fym'; a['score'] = score(a); rec['c'].append(a)
        warp_square(im, a['quad'], 260).save(f'{OUT}/{idx:03d}_0.jpg', quality=80) if a.get('quad') else im.resize((260, 260)).save(f'{OUT}/{idx:03d}_0.jpg')
    except Exception as e: rec['err_fym'] = str(e)
    pu = product_url(m); rec['pu'] = pu
    if pu:
        try:
            p = json.loads(get(pu + '.json'))['product']
            for j, imr in enumerate(p.get('images', [])[:10], 1):
                src = imr['src']; s2 = src + ('&' if '?' in src else '?') + 'width=900'
                try:
                    im = Image.open(io.BytesIO(get(s2))).convert('RGB'); a = analyze(im); a['src'] = src; a['score'] = score(a)
                    (warp_square(im, a['quad'], 260) if a.get('quad') else im.resize((260, 260))).save(f'{OUT}/{idx:03d}_{j}.jpg', quality=80)
                    rec['c'].append(a)
                except Exception as e: rec['c'].append({'src': src, 'err': str(e)[:80], 'score': 0})
        except Exception as e: rec['err_store'] = str(e)[:120]
    return idx, rec
recs = {}
with cf.ThreadPoolExecutor(10) as ex:
    for idx, rec in ex.map(one, list(enumerate(keys))): recs[idx] = rec
json.dump([recs[i] for i in range(len(keys))], open(f'{OUT}/cands.json', 'w'), indent=0)
# sheets: one row per mat, FYM photo + up to 7 vendor images (straightened previews), scores under each
PX = 200; COLS = 8; ROWS = 10
for si in range(0, len(keys), ROWS):
    o = Image.new('RGB', (COLS * PX + 230, ROWS * (PX + 14)), 'white'); d = ImageDraw.Draw(o)
    for r, i in enumerate(range(si, min(si + ROWS, len(keys)))):
        y = r * (PX + 14); rec = recs[i]; d.text((4, y + 4), f'#{i}', fill='black')
        for t in range(0, len(rec['n']), 30): d.text((4, y + 18 + t // 30 * 13), rec['n'][t:t + 30], fill='black')
        for j, a in enumerate(rec['c'][:COLS]):
            p = f'{OUT}/{i:03d}_{j}.jpg'; x = 230 + j * PX
            if os.path.exists(p): o.paste(Image.open(p).resize((PX - 4, PX - 4)), (x, y))
            d.text((x + 2, y + PX - 2), f"{j}{'F' if j == 0 else ''} s{a.get('score', 0)} {a.get('kind', '')[:3]} f{a.get('fill', '')} a{a.get('aspect', '')}", fill='red')
    o.save(f'{OUT}/sheet_{si // ROWS:03d}.jpg', quality=80)
print('mats', len(keys), 'with store', sum(1 for r in recs.values() if r.get('pu')), 'store errors', sum(1 for r in recs.values() if r.get('err_store')))
