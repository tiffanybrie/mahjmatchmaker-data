"""Pull Tiffany's per-mat rack picks from every live album page and map them to FYM keys.
Each album card is <figure class="mm3-c"> with <h3>Set + Mat</h3> and a <div class="mm3-rk"> line:
  "Rack matches: a · b"  (her picks for that mat)        -> kind 'mat'
  "Racks shown: a · b"   (racks in her photo of that pairing) -> kind 'mat'
  "Match the tiles: ... Match the mat: ..." (holiday cards) -> 'tiles' list + 'mat' list
Racks are mapped by their link (product handle + variant) to FYM rack keys, then by name.
Output config/album-rack-picks.json {set slug: {mat key: {"mat": [rack keys], "tiles": [rack keys]}}} + report.
Why (Tiffany Oct 25 17:10): FYM showed Birdie's tile racks (Hot Pink) first for Luna, whose album pick is PLM Oak + OMM White Acrylic.
Usage: python3 scripts/album_rack_picks.py <build_dir> [cache_dir] [--fresh]"""
import sys, os, re, json, html, subprocess, unicodedata
from urllib.parse import urlparse, parse_qs, unquote
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
B = sys.argv[1]; CACHE = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else '/tmp/album_cache'; os.makedirs(CACHE, exist_ok=True)
h = open(B + '/index.html').read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:]); M, R = D['mats'], D['racks']
def nm(x): x = unicodedata.normalize('NFKD', html.unescape(x or '')).encode('ascii', 'ignore').decode().lower(); return re.sub(r'[^a-z0-9]+', ' ', x).strip()
def ukey(u):
    u = html.unescape(u or '')
    if 'redirect=' in u: u = 'https://x' + unquote(parse_qs(urlparse(u).query).get('redirect', [''])[0])
    p = urlparse(u); q = parse_qs(p.query); hnd = p.path.rstrip('/').split('/')[-1]
    return (urlparse(u).netloc.replace('www.', '').split('.')[0] if p.netloc != 'x' else '') , hnd, (q.get('variant') or [''])[0]
RU = {}
for k, r in R.items():
    for u in (r.get('u'), r.get('u0')):
        if u: _, hnd, v = ukey(u); RU.setdefault((hnd, v), []).append(k)
RN = {}
for k, r in R.items(): RN.setdefault(nm(r['n']), []).append(k)
def pick(c): vis = [k for k in c if not R[k].get('hid')]; return (vis or c or [None])[0]
def rack_key(name, href):
    _, hnd, v = ukey(href)
    c = RU.get((hnd, v)) or ([] if v else RU.get((hnd, ''), []))
    if len(c) > 1: c = [k for k in c if nm(R[k]['n']) == nm(name)] or c
    if c: return pick(c)
    n = nm(name); c = RN.get(n) or [k for kk, vv in RN.items() if sorted(kk.split()) == sorted(n.split()) for k in vv]
    return pick(c)
def page(url):
    p = CACHE + '/' + re.sub(r'[^a-z0-9]+', '_', url.lower())[-80:] + '.html'
    if not os.path.exists(p) or '--fresh' in sys.argv: subprocess.run(['curl', '-s', '-L', '-o', p, url], check=False)
    return open(p, errors='ignore').read()
def links(seg): return [(html.unescape(re.sub(r'<[^>]+>', '', t)).strip(), hr) for hr, t in re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', seg, re.S)]
out, report = {}, {}
for s in D['sets']:
    if not s.get('album') or not s['m'] or s['slug'] in out: continue
    t = page(s['album']); mats = {nm(M[k]['n']): k for k, _ in s['m'] if k in M}
    res, miss, cards = {}, [], 0
    for fig in re.findall(r'<figure class="mm3-c[^"]*">(.*?)</figure>', t, re.S):
        hm = re.search(r'<h3>(.*?)</h3>', fig, re.S); rk = re.search(r'<div class="mm3-rk"[^>]*>(.*?)</div>', fig, re.S)
        if not hm or not rk: continue
        cards += 1; title = html.unescape(re.sub(r'<[^>]+>', '', hm.group(1))).strip()
        if ' + ' in title and nm(title.split(' + ', 1)[0]) != nm(s['name']) and nm(title.split(' + ', 1)[0]) not in nm(s['name']): cards -= 1; continue   # shared holiday page: other sets' cards
        mname = title.split(' + ', 1)[1] if ' + ' in title else title
        mk = mats.get(nm(mname)) or next((k for n_, k in mats.items() if nm(mname) and (nm(mname) in n_ or n_ in nm(mname))), None)
        if not mk: miss.append(f'mat? {mname}'); continue
        body = rk.group(1); parts = {'mat': [], 'tiles': []}
        if 'Match the tiles' in body or 'Match the mat' in body:
            mt = body.split('Match the mat', 1); parts['tiles'] = links(mt[0]); parts['mat'] = links(mt[1]) if len(mt) > 1 else []
        else: parts['mat'] = links(body)
        e = {}
        for kind, lst in parts.items():
            keys = []
            for name, href in lst:
                k = rack_key(name, href)
                if k: keys.append(k)
                else: miss.append(f'rack? {name} (on {mname})')
            e[kind] = keys
        if re.sub(r'<[^>]+>', '', body).strip().startswith('Racks shown'): e['shown'] = True   # racks in her photo (tile racks listed first)
        res[mk] = e
    out[s['slug']] = res; report[s['slug']] = {'name': s['name'], 'cards': cards, 'mapped': len(res), 'app_mats': len(s['m']), 'missing': miss}
json.dump(out, open(REPO + 'config/album-rack-picks.json', 'w'), indent=1, ensure_ascii=False)
json.dump(report, open(REPO + 'config/album-rack-picks-report.json', 'w'), indent=1, ensure_ascii=False)
for sl, r in report.items(): print(f"{r['name']}: cards {r['cards']} mapped {r['mapped']}/{r['app_mats']}" + (f" MISSING {r['missing'][:5]}" if r['missing'] else ''))
