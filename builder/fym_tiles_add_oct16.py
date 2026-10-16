"""Oct 16 (doc 65 + Tiffany 2:56pm): every partner tile set into Find Your Match on the LOW catalog bar.
No keep/skip list for her. One row per real tile set (colour variants with their own photo are split),
travel/mini/accessories out, best listing photo picked automatically; unsure ones are flagged for her.
Catalog sets carry cat=true and m=[] (no Tiffany matches): the mat step then shows the 'not matched yet' note.
Usage: python3 fym_tiles_add_oct16.py <index.html (after mats/racks fill)> <report.json> <feeds dir> <out dir>"""
import json, sys, re, io, os, base64, hashlib, subprocess
import numpy as np
from PIL import Image
sys.path.insert(0, '/tmp/cc')
from profile import prof
from skimage.color import rgb2lab, deltaE_ciede2000
idx_html, REP, FEEDS, OUT = sys.argv[1:5]
t = open(idx_html).read(); i0 = t.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(t[i0:])
rep = json.load(open(REP)); nd = lambda d: d.replace('www.', '')
SKIPDOM = {'splashofcolorco.com', 'themahjongpress.com'}
NOT = re.compile(r'floating|convertible|note ?cards?|stationery|personalized|notepad|cabana stripe|rummi|rummy|tile pack|chinese|riichi|japanese|yakitori|marker|game of ur|display box|acrylic display|acrylic box|travel|\bmini\b|petite|compact|needle minder|canvas|blank tile|single tile|replacement|extra tile|joker tile|tile bag|\bbag\b|\bcase only|tile box|lucite.*box|pusher|young players|\bkids?\b|scorecard|card holder|ornament|cookie|sticker|gift card|sample|shuffler|coaster|candle|charm|pin\b|keychain|mat\b|rack\b|racks\b|101/102|lesson|book\b', re.I)
BR = {}
for kind in ('mats', 'racks', 'tiles'):
    for k, v in D[kind].items():
        if '/' not in k or ':' in k.split('/')[0]: continue
        dom = nd(k.split('/')[0]); q = v['u'].split('?', 1)[1] if '?' in v.get('u', '') else ''
        q = '&'.join(p for p in q.split('&') if not p.startswith('variant='))
        BR.setdefault(dom, dict(bn=v['bn'], dc=v.get('dc', ''), q=q, host=k.split('/')[0]))
def feed(dom):
    for f in (f'{FEEDS}/{dom}.json', f'{FEEDS}/www.{dom}.json'):
        if os.path.exists(f): return json.load(open(f))
    return []
def clean(n):
    orig = n
    qm = re.search(r'["“]([^"”]{2,40})["”]', n)
    if qm: return qm.group(1).strip()
    n = re.sub(r'^(NEW|PRE-?ORDER|PRESALE|【[^】]*】|LIMITED|SALE)[:!\s-]*', '', n, flags=re.I)
    n = re.sub(r'\((pre-?order|preorder)[^)]*\)|\bPRE-?ORDER\b|\bPRESALE\b', '', n, flags=re.I)
    n = re.sub(r'^(Mahjong Studios|Christmas Mahjong Set)\s*[–-]\s*', '', n, flags=re.I)
    n = re.sub(r'^Tile Sets\s+', '', n, flags=re.I); n = re.sub(r'\s*(-\s*)?(Coming|Expected|Ships?)\b.*$', '', n, flags=re.I); n = re.sub(r'\s+Back$', '', n, flags=re.I)
    n = re.sub(r'^(Black\s+)?Mahjong Tiles\s*[–-]\s*', '', n, flags=re.I)
    n = re.sub(r'\(\d+\s*Tiles\)|\b\d{3}\s+(American\s+)?(Mahjong\s+)?Tiles\b', '', n, flags=re.I)
    n = re.sub(r'\s*[–-]?\s*American Mahjong (Game )?(Tile )?Set,?\s*', ' ', n, flags=re.I)
    n = re.sub(r'\s*[–\-|:,]\s*(Classic )?(American )?(Mah ?jongg?|Mahj)\s*(Tile)?\s*(Set|Tiles)\b.*$', '', n, flags=re.I)
    n = re.sub(r'\s*\b(Tile Set|Tiles|Mahjong Tiles)\b.*$', '', n, flags=re.I)
    n = re.sub(r'\s*with .*$|\s*[–-]\s*$', '', n, flags=re.I)
    n = re.sub(r'\s*\|.*$', '', n); n = re.sub(r'\s+(Mahjong|Mahj)$', '', n, flags=re.I); n = re.sub(r'\s+[–-]\s+', ' ', n)
    n = re.sub(r'\s+', ' ', n).strip(' -–|:,"“”')
    if n.lower() in ('green', 'blue', 'pink', 'red', 'white', 'black', 'purple', 'yellow', 'tile set', '') and ' - ' in orig: n = clean(orig.rsplit(' - ', 1)[1])
    n = ' '.join(w.title() if w.isupper() and len(w) > 2 else w for w in n.split())
    return n or 'Tile Set'
BUNDLE = re.compile(r'rack|\bmat\b|bag|tote|all in one|bundle|instruction|complete|presale|tiles ?\+|\+|no mat|choose|dice', re.I)
def flat_graphic(im):
    q = im.convert('RGB').resize((96, 96)).quantize(16); h = sorted(q.histogram()[:16], reverse=True)
    return sum(h[:3]) / max(1, sum(h)) > 0.86
BAD = re.compile(r'box|packag|case|bag|size|dimension|chart|guide|logo|rack|lifestyle', re.I)
def imgs_of(p):
    ims = p.get('images') or []
    if isinstance(ims, str):
        try: ims = eval(ims)
        except Exception: ims = []
    return ims
def get(url, fn):
    if not os.path.exists(fn): subprocess.run(['curl', '-s', '-m', '40', url, '-o', fn])
    return Image.open(fn).convert('RGB')
def lab(h): return rgb2lab(np.array([[[int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]]]))[0, 0]
os.makedirs(OUT + '/img', exist_ok=True); os.makedirs(OUT + '/t11', exist_ok=True)
B = {}
def uri(im, w, q=76):
    im = im.copy(); im.thumbnail((w, w)); b = io.BytesIO(); im.save(b, 'WEBP', quality=q)
    v = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode(); h = hashlib.md5(v.encode()).hexdigest()[:10]; B[h] = v; return h
STOP = {'the', 'christmas', 'collection', 'i', 'ii', 'tile', 'set', 'tiles', 'mahjong', 'edition', 'without', 'acrylic', 'box', 'with'}
def canon(n): return frozenset(w for w in re.findall(r'[a-z0-9]+', n.lower().replace('é', 'e').replace('è', 'e')) if w not in STOP)
def bkey(b): return re.sub(r'[^a-z]', '', b.lower().split(' x ')[-1])[:6]
have = [(bkey(s_['maker']), canon(s_['name'])) for s_ in D['sets']]
def dup(bn, name):
    c = canon(name); b = bkey(bn)
    return not c or any(b == hb and (hc <= c or c <= hc) and hc for hb, hc in have)
have_names = {(T['bn'], T['n'].lower()) for T in D['tiles'].values()}
rows = []; flagged = []; n = 0
for dom, rr in rep.items():
    if dom in SKIPDOM or dom not in BR: continue
    fd = {x['handle'].rstrip('/').split('/')[-1]: x for x in feed(dom)}; br = BR[dom]
    for r in rr:
        if r['inapp'] or r['cat'] != 'tiles' or r['rule']: continue
        p = fd.get(r['h'])
        if not p or NOT.search(p['title']): continue
        ims = imgs_of(p); vs = p.get('variants') or []
        if isinstance(vs, str):
            try: vs = eval(vs)
            except Exception: vs = []
        byid = {i.get('id'): i for i in ims}
        vimg = [(v, (v.get('featured_image') or {}).get('src') if isinstance(v.get('featured_image'), dict) else None) for v in vs]
        opts = p.get('options') or []
        split = br['bn'] != 'Mahjong Studios' and len(vs) > 1 and len(opts) == 1 and len({s for v, s in vimg if s}) == len(vs) and not any(BUNDLE.search(v['title']) for v in vs)
        pn = clean(p['title']); vn = lambda v: clean(v['title']) if any(w.lower() in clean(v['title']).lower() for w in pn.split() if len(w) > 3) else f"{pn} {clean(v['title'])}".strip()
        units = [(vn(v), s, v.get('id'), v.get('available')) for v, s in vimg] if split else \
                [(clean(p['title']), None, None, any(v.get('available') for v in vs) if vs else None)]
        for name, vsrc, vid, avail in units:
            if (br['bn'], name.lower()) in have_names or dup(br['bn'], name): continue
            have_names.add((br['bn'], name.lower())); have.append((bkey(br['bn']), canon(name)))
            if vsrc: src = vsrc
            else:
                good = [x for x in ims if not BAD.search((x.get('alt') or '') + ' ' + x.get('src', '').split('/')[-1].split('?')[0])]
                pick = (good or ims or [None])[0]
                if not pick: flagged.append((dom, name, 'no photo')); continue
                src = pick['src']
                if not good: flagged.append((dom, name, 'only box/lifestyle photos'))
            src = src.split('?')[0] + '?width=1200'
            try: im = get(src, OUT + '/img/' + hashlib.md5(src.encode()).hexdigest()[:12] + '.jpg')
            except Exception: flagged.append((dom, name, 'download failed')); continue
            if flat_graphic(im):  # colour swatch / graphic: try the next listing photos
                for alt in ims[1:5]:
                    a2 = alt['src'].split('?')[0] + '?width=1200'
                    try: im2 = get(a2, OUT + '/img/' + hashlib.md5(a2.encode()).hexdigest()[:12] + '.jpg')
                    except Exception: continue
                    if not flat_graphic(im2): im = im2; break
                else: flagged.append((dom, name, 'only graphic/swatch photos'))
            host = br['host']; key = f"{host}/{r['h']}" + (f"?v={vid}" if vid else '')
            u = 'https://' + host + '/products/' + r['h'] + ('?variant=' + str(vid) if vid else '')
            if br['q']: u += ('&' if '?' in u else '?') + br['q']
            full = im.copy(); full.thumbnail((900, 900)); fn = f't11/{n}.jpg'; full.save(OUT + '/' + fn, quality=80); n += 1
            pr = prof(im, name) or {'sw': []}
            sw = [[h, round(s, 2)] for nm, h, s in pr.get('sw', [])]
            colored = [h for h, s in sw if np.hypot(*lab(h)[1:]) > 18] or [h for h, s in sw] or ['#888888']
            D['tiles'][key] = dict(full=fn, n=name, bn=br['bn'], u=u, dc=br['dc'], pa=True, nc=False, rt=False, pile=uri(im, 360), cat=True)
            rows.append((key, name, br['bn'], colored[0], sw, avail))
# sets + ranks (same scoring as the album sets)
order = D['order']; ML = {m: [(lab(h), w) for h, w in D['mats'][m]['ms']] for m in order if D['mats'][m]['ms']}
def sim(A, Bv):
    la = np.array([a for a, _ in A]); wa = np.array([w for _, w in A]); lb = np.array([b for b, _ in Bv])
    Dm = deltaE_ciede2000(np.repeat(la, len(lb), 0), np.tile(lb, (len(la), 1))).reshape(len(la), len(lb))
    return float((Dm.min(1) * wa).sum() / wa.sum())
ix = {m: i for i, m in enumerate(order)}; slugs = {s['slug'] for s in D['sets']}
for key, name, bn, tc, sw, avail in rows:
    slug = re.sub(r'[^a-z0-9]+', '-', f'{bn}-{name}'.lower()).strip('-')[:80]
    while slug in slugs: slug += '-2'
    slugs.add(slug)
    T = [(lab(h), w) for h, w in sw] if sw else None
    if T: sc = sorted(((0.6 * sim(T, ML[m]) + 0.4 * sim(ML[m], T) + (25 if D['mats'][m].get('hol') else 0)) if m in ML else 999, m) for m in order); rank = [ix[m] for _, m in sc]
    else: rank = list(range(len(order)))
    D['sets'].append(dict(slug=slug, name=name, maker=bn, tile=key, tc=tc, tag='', album='', rank=rank, m=[], cat=True))
# template: tile search + 'not matched yet' note
t2 = t[:i0] + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + t[i0 + end:]
a = '<div class="tgrid">${tileGrid()}</div>`;}'
assert t2.count(a) == 1
t2 = t2.replace(a, '<div class="msearch"><input id="tsq" type="search" enterkeyhint="search" placeholder="Don\\u2019t see yours? Search every tile set by name or brand" autocomplete="off" aria-label="Search tile sets"></div><div class="tgrid" id="tgrid">${tileGrid()}</div>`;}', 1)
b = "document.addEventListener('input',e=>{if(e.target.id!=='msq')return;"
assert t2.count(b) == 1
t2 = t2.replace(b, "document.addEventListener('input',e=>{if(e.target.id!=='tsq')return;const v=e.target.value.trim().toLowerCase(),g=$('tgrid');if(!g)return;if(v.length<2){g.innerHTML=tileGrid();return;}const toks=v.split(/\\s+/);const hits=D.sets.map((s,i)=>[s,i]).filter(([s])=>{const h=(s.name+' '+s.maker).toLowerCase();return toks.every(k=>h.includes(k));}).sort((a,b)=>(a[0].cat?1:0)-(b[0].cat?1:0)||a[0].name.localeCompare(b[0].name));g.innerHTML=hits.length?hits.map(([s,i])=>tileBtn(s,i)).join(''):'<p class=\"hint\" style=\"grid-column:1/-1\">No tile sets match that yet.</p>';});\n" + b, 1)
c = "head(2,'Mat-ching','Right = crush, left = pass')"
assert t2.count(c) == 1
t2 = t2.replace(c, "head(2,'Mat-ching',set().m.length?'Right = crush, left = pass':'Tiffany hasn\\u2019t matched '+esc(set().name)+' yet. Match away! Right = crush, left = pass')", 1)
# az list: album sets first, catalog sets after (so the 47 albums stay easy to find)
d = "if(S.tcol==='az')return all.sort((a,b)=>a[0].name.localeCompare(b[0].name))"
assert t2.count(d) == 1
t2 = t2.replace(d, "if(S.tcol==='az')return all.sort((a,b)=>a[0].name.localeCompare(b[0].name))", 1)
t2 = t2.replace('<script src="b5v1.js"></script>', '<script src="b5v1.js"></script><script src="b6v1.js"></script>', 1)
assert 'b6v1.js' in t2
open(OUT + '/index.html', 'w').write(t2)
open(OUT + '/b6v1.js', 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(B, separators=(',', ':')) + ');')
json.dump(dict(added=[(k, nme, bn, av) for k, nme, bn, tc, sw, av in rows], flagged=flagged, files=n), open(OUT + '/tiles_added.json', 'w'), indent=1, ensure_ascii=False)
print('tile sets now', len(D['sets']), 'added', len(rows), 'flagged', len(flagged), 'files', n, 'bundle KB', len(json.dumps(B)) // 1024)
