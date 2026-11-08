"""Gap audit B4 (Nov 7): fetch store prices for every VISIBLE FYM mat / tile set / rack that has no price in D.tv (pm / pt / price).
Read-only against the build; writes config/fym-prices-nov07.json, applied by builder/fym_fix_nov07/prices_v118.py.

Sources, in order:
  1. Shopify (/products/<handle> anywhere in u0 / u / the key, incl. /discount/...?redirect=): the store's full catalog
     (/products.json pages, one pass per domain) by handle, else /products/<handle>.js (catches unlisted / sold-out products),
     else an exact normalized-title match in that store's catalog (src notes 'title match').
     Price = the key's ?variant= / ?v= variant if given, else the lowest AVAILABLE variant (lowest of all if none available).
     'was' = compare_at when higher (on sale).
  2. Squarespace (/p/<slug>): ?format=json, lowest variant (sale price when on sale).
  3. Wix (/product-page/): product:price:amount meta.
  4. ShopMy pin (go.shopmy.us/p-<id> in any link, or the same product URL pinned in her collections): product.fallbackPrice (USD).
     Used for Etsy / Amazon (curl gets 403) and as the fallback for anything above.
  5. Etsy (DataDome blocks curl): prices read with WebFetch from the shop pages / listings, passed as --etsy <json>
     {listing_id: {p, was?, so?, how}}; Etsy entries already in config/fym-prices-nov07.json are KEPT on a re-run.
Polite: 6 workers, retries with backoff on 429 / 5xx.
Usage: python3 builder/fym_fix_nov07/prices_fetch_nov07.py <build dir or index.html> [--pins <shopmy pins cache json>] [--etsy <json>]"""
import sys, os, re, json, time, html, unicodedata, urllib.request, urllib.parse, concurrent.futures as cf, pathlib, threading
R = pathlib.Path(__file__).resolve().parents[2]
P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html')
OUT = R / 'config/fym-prices-nov07.json'; AT = '2026-11-07'
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36',
      'Accept': 'application/json,text/html;q=0.9,*/*;q=0.8'}
_lock = threading.Lock()

def fetch(u, tries=5):
    d = 2
    for a in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30) as r:
                return r.status, r.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and a < tries - 1:
                time.sleep(int(e.headers.get('Retry-After') or 0) or d); d *= 2; continue
            return e.code, ''
        except Exception:
            if a < tries - 1: time.sleep(d); d *= 2; continue
            return 0, ''
    return 0, ''

def getj(u):
    s, b = fetch(u)
    try: return json.loads(b) if s == 200 else None
    except Exception: return None

h = open(P).read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:]); TV = D['tv']
items = []
for k, m in D['mats'].items():
    if not m.get('hid') and k not in TV['pm']: items.append(('m', k, m))
seen = set()
for s in D['sets']:
    t = D['tiles'].get(s['tile'], {})
    if s.get('hid') or t.get('hid') or s['tile'] in TV['pt'] or s['tile'] in seen: continue
    seen.add(s['tile']); items.append(('t', s['tile'], t))
for k, r in D['racks'].items():
    if not r.get('hid') and k not in TV['price']: items.append(('r', k, r))
print('missing:', {c: sum(1 for x in items if x[0] == c) for c in 'mtr'})

# ShopMy pins (all her collections)
PINS = {}
pc = sys.argv[sys.argv.index('--pins') + 1] if '--pins' in sys.argv else None
if pc and os.path.exists(pc): PINS = {int(a): b for a, b in json.load(open(pc)).items()}
else:
    u = getj('https://api.shopmy.us/api/Users/username/mahjmatchmaker')
    cols = {c['id']: c['name'] for c in u['user']['collections']}
    with cf.ThreadPoolExecutor(6) as ex:
        for cid, d in zip(cols, ex.map(lambda c: getj(f'https://apiv3.shopmy.us/api/Collections/{c}'), cols)):
            for p in (d or {}).get('pins', []):
                pr = p.get('product') or {}
                PINS[p['id']] = dict(link=p.get('link'), title=p.get('title'), price=pr.get('fallbackPrice'), cur=pr.get('fallbackPriceCurrency'))
    if pc: json.dump(PINS, open(pc, 'w'))
def ukey(u):
    u = urllib.parse.unquote(urllib.parse.unquote(u or '')).split('?')[0].rstrip('/').lower()
    u = re.sub(r'^https?://(www\.)?', '', u); m = re.search(r'etsy\.com/(?:[a-z-]+/)?listing/(\d+)', u)
    return 'etsy:' + m.group(1) if m else u
PIN_BY_URL = {ukey(p['link']): (pid, p) for pid, p in PINS.items() if p.get('link') and p.get('price')}

# Items whose FYM link is only a homepage / code page: the store product checked by hand Nov 7 (same mat name in that store).
MANUAL = {
    'alb2:charleston-mahjong-club-club-mat': 'https://www.charlestonmahjongclub.com/products/the-club-mat-2-color-options-copy',  # both Club Mat colourways $75
    'alb2:my-fair-mahjong-confetti-lemon-lime': 'https://myfairmahjong.com/products/mahjong-mat-confetti-33-x-33?v=Green',
    'alb2:mahjong-moxie-duck-camp': 'https://www.mahjong-moxie.com/products/untitled-jul14_11-27',  # 'Duck Camp Mat'
    'alb2:wren-mats-bright-orangey': 'https://www.wrenmats.com/mats/p/bright-orangey-red-and-blue-art',
    'alb2:wren-mats-palm-beach': 'https://www.wrenmats.com/mats/p/0kam5qvgncmooixxnmb05lcuhaqp68',
}
def urls(o, k):
    out = [MANUAL[k]] if k in MANUAL else []
    for u in (o.get('u0'), o.get('u'), o.get('u1')):
        if not u: continue
        u = urllib.parse.unquote(urllib.parse.unquote(u)); out.append(u)
        m = re.search(r'^(https?://[^/]+)/discount/[^?]*\?.*?redirect=(/[^&]+)', u)
        if m: out.append(m.group(1) + m.group(2))
    if re.match(r'^[a-z0-9.-]+\.[a-z]{2,}/', k):
        out.append('https://' + k)
        if 'etsy.com' not in k and '/' in k and k.count('/') == 1: out.append('https://' + k.replace('/', '/products/', 1))
    return out

def norm(s):
    s = unicodedata.normalize('NFKD', html.unescape(s or '')).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'\b(the|mahjong|mahjongg|mahj|mat|mats|neoprene|leatherette|vegan|leather|tile|tiles|set|with|and|of|a|pre-?order|preorder)\b', ' ', s)
    return re.sub(r'[^a-z0-9]+', '', s)

CAT = {}; CAT_LOCK = {}
def catalog(dom):
    with _lock: lk = CAT_LOCK.setdefault(dom, threading.Lock())
    with lk:
        if dom in CAT: return CAT[dom]
        prods, pg = [], 1
        while pg <= 40:
            d = getj(f'https://{dom}/products.json?limit=250&page={pg}')
            if not d or not d.get('products'): break
            prods += d['products']; pg += 1
            if len(d['products']) < 250: break
        CAT[dom] = {p['handle']: p for p in prods} if prods else None
        return CAT[dom]

def pick_variant(vars_, vid, cents):
    f = (lambda x: x / 100) if cents else (lambda x: float(x))
    vs = [v for v in vars_ if v.get('price') not in (None, '')]
    if vid:
        vv = [v for v in vs if str(v.get('id')) == str(vid) or (v.get('title') or '').lower() == str(vid).lower()
              or str(vid).lower() in [str(v.get(o) or '').lower() for o in ('option1', 'option2', 'option3')]]
        if vv: vs = vv
    av = [v for v in vs if v.get('available', True)] or vs
    if not av: return None
    v = min(av, key=lambda v: f(v['price'])); p = f(v['price'])
    ca = v.get('compare_at_price'); ca = f(ca) if ca not in (None, '', 0, '0.00') else None
    return p, (ca if ca and ca > p else None), all(not x.get('available', True) for x in vs)

def shopify(u, name):
    m = re.match(r'https?://([^/]+)/(?:collections/[^/]+/)?products/([^/?#]+)(?:\?(.*))?', u)
    if not m: return None
    dom, hd, q = m.group(1).lower(), m.group(2), urllib.parse.parse_qs(m.group(3) or '')
    vid = (q.get('variant') or q.get('v') or [None])[0]
    cat = catalog(dom); p = cat.get(hd) if cat else None; how = 'products.json'
    if p:
        r = pick_variant(p['variants'], vid, False)
    else:
        j = getj(f'https://{dom}/products/{hd}.js'); how = '.js'
        r = pick_variant(j['variants'], vid, True) if j and j.get('variants') else None
        if not r and cat:  # renamed handle: exact normalized title match, unique
            n = norm(name); c = [x for x in cat.values() if norm(x['title']) == n]
            if len(c) == 1:
                r = pick_variant(c[0]['variants'], vid, False); hd = c[0]['handle']; how = 'title match'
    if not r: return None
    return dict(p=r[0], was=r[1], src=f'https://{dom}/products/{hd}', how='shopify ' + how, so=r[2] or None)

def squarespace(u):
    if '/p/' not in u: return None
    j = getj(u.split('?')[0] + '?format=json')
    it = (j or {}).get('item') or {}; vs = it.get('variants') or []
    if not vs: return None
    def pr(v):
        a = float(v['priceMoney']['value']); s = float((v.get('salePriceMoney') or {}).get('value') or 0)
        return (s, a) if v.get('onSale') and s else (a, None)
    av = [v for v in vs if v.get('unlimited') or v.get('qtyInStock', 1) > 0] or vs
    p, was = min((pr(v) for v in av), key=lambda x: x[0])
    return dict(p=p, was=was, src=u.split('?')[0], how='squarespace format=json', so=(len(av) == len(vs) and not any(v.get('unlimited') or v.get('qtyInStock', 0) > 0 for v in vs)) or None)

def wix(u):
    if '/product-page/' not in u: return None
    s, b = fetch(u.split('?')[0])
    m = re.search(r'product:price:amount" content="([\d.]+)"', b)
    return dict(p=float(m.group(1)), src=u.split('?')[0], how='wix meta') if m else None

def pin(us):
    for u in us:
        m = re.search(r'go\.shopmy\.us/p-(\d+)', u)
        if m and PINS.get(int(m.group(1)), {}).get('price'):
            p = PINS[int(m.group(1))]; return dict(p=float(p['price']), src=f'https://go.shopmy.us/p-{m.group(1)}', how='shopmy pin', cur=p.get('cur'))
    for u in us:
        x = PIN_BY_URL.get(ukey(u))
        if x: return dict(p=float(x[1]['price']), src=f'https://go.shopmy.us/p-{x[0]}', how='shopmy pin (same product url)', cur=x[1].get('cur'))
    return None

def resolve(it):
    c, k, o = it; us = urls(o, k)
    # follow a go.shopmy pin to its product link
    for u in list(us):
        m = re.search(r'go\.shopmy\.us/p-(\d+)', u)
        if m and PINS.get(int(m.group(1)), {}).get('link'): us.append(PINS[int(m.group(1))]['link'])
    name = o.get('n') or ''
    for f in (lambda: next((r for u in us if (r := shopify(u, name))), None),
              lambda: next((r for u in us if (r := squarespace(u))), None),
              lambda: next((r for u in us if (r := wix(u))), None),
              lambda: pin(us)):
        try: r = f()
        except Exception as e: r = None
        if r and r.get('p') and r['p'] > 0 and (r.get('cur') in (None, 'USD')): return c, k, o, r, us
    return c, k, o, None, us

ETSY = json.load(open(sys.argv[sys.argv.index('--etsy') + 1])) if '--etsy' in sys.argv else {}
OLD = {k: v for k, v in json.load(open(OUT)).items() if not k.startswith('_') and str(v.get('how', '')).startswith('etsy')} if OUT.exists() else {}
def etsy(it, us):
    c, k, o = it
    if k in OLD: return OLD[k]
    for u in us:
        m = re.search(r'etsy\.com/(?:[a-z-]+/)?listing/(\d+)', u)
        if m and m.group(1) in ETSY:
            e = dict(ETSY[m.group(1)]); return dict(c=c, src=f'https://www.etsy.com/listing/{m.group(1)}', at=AT, **e)
    return None

res, left = {}, []
with cf.ThreadPoolExecutor(6) as ex:
    for c, k, o, r, us in ex.map(resolve, items):
        if not r and (x := etsy((c, k, o), us)):
            res[k] = {'c': c, 'p': x['p'], 'src': x['src'], 'at': x.get('at', AT), 'how': x['how'], **{a: x[a] for a in ('was', 'so') if a in x}}; continue
        if r:
            e = {'c': c, 'p': round(r['p'], 2), 'src': r['src'], 'at': AT, 'how': r['how']}
            if r.get('was'): e['was'] = round(r['was'], 2)
            if r.get('so'): e['so'] = 1
            res[k] = e
        else:
            left.append({'c': c, 'k': k, 'n': o.get('n'), 'bn': o.get('bn'), 'urls': sorted(set(us))[:3]})
json.dump({'_about': 'Store prices for visible FYM items with no price in D.tv (gap audit B4, Nov 7). c = m mat / t tile set / r rack; '
           'p = current store price USD (lowest available variant, or the variant the key names; sale price when on sale, was = compare_at); '
           'src = where it was read; so = every variant sold out (last listed price). Built by builder/fym_fix_nov07/prices_fetch_nov07.py, '
           'applied by builder/fym_fix_nov07/prices_v118.py. _left = items still without a price.',
           **dict(sorted(res.items())), '_left': left}, open(OUT, 'w'), indent=1, ensure_ascii=False)
print('filled', {c: sum(1 for v in res.values() if v['c'] == c) for c in 'mtr'}, 'left', len(left), '->', OUT)
