"""Build the holiday-section payload for live album pages.
Usage: python3 hol_payload.py <picker data5.json> <cards manifest.json> <git sha> <out.json>
Output: {album_slug: {"tile": name, "figs": [figure html, ...]}, "_new": {tile_slug: {...}}}"""
import json, sys, html, re
R = '/home/claude/mahjmatchmaker-data/'
D = json.load(open(sys.argv[1])); man = json.load(open(sys.argv[2])); sha = sys.argv[3]
DD = json.load(open(R + 'data.json'))
RL = {n: u for n, u in DD['R']}
MM = json.load(open('/tmp/hol/mats.json'))
albums = {a['slug'] for a in json.load(open(R + 'work/albums.json'))}
e = lambda s: html.escape(s, quote=True)

def base(u): return re.sub(r'([?&])variant=\d+&?', r'\1', u).replace('?&', '?').rstrip('?&')
BB_BASE = base(next(u for n, u in RL.items() if n.startswith('Bird & Bamboo')))
PLM_BASE = base(RL['Peace Love Mahjong Pink'])
def rack_link(k):
    if k.startswith('bb:'):
        n = 'Bird & Bamboo ' + k[3:]; return n, RL.get(n, BB_BASE)
    if k.startswith('plm:'):
        n = 'Peace Love Mahjong ' + k[4:]; return n, RL.get(n, PLM_BASE)
    nm = D['RK'][k][0]
    for n, u in RL.items():
        if k.split('/')[-1] in u or n == nm: return n, u
    if '/' in k:
        d, h = k.split('/', 1); return nm, f'https://{d}/products/{h}'
    return nm, None

def mat_link(m, name):
    for v in MM.values():
        h = v.get('handle', '')
        if h and (h == m or h.startswith(m) or m.startswith(h)):
            u = v['url']; return u + ('?' + v['ref'] if v.get('ref') else '')
    for x in DD['M']:
        if x[0].lower() in name.lower() or name.lower().startswith(x[0].lower()): return x[2]
    return None

BRANDPAGE = {}
for l in open(R + 'work/domains.tsv'):
    p = l.strip().split('\t')
    if len(p) == 2: BRANDPAGE[p[0]] = p[1]
def brand_href(b):
    slug = '/' + re.sub(r'[^a-z0-9]+', '-', b.lower().replace('&', 'and').replace('!', '')).strip('-') + '-discount-code'
    return slug if slug in BRANDPAGE else None

NOCODE = {'Sunday Mahjong', 'Luxe Mahjong', 'Maison Mahj', 'Lucky Daughters', 'Mahjong Studios', ''}
out = {}; missing = []
for c in man:
    slug = c['tile'] + '-mahjong-tile-matches'
    mname = re.sub(r'\s*\(.*?\)', '', c['matName']).strip()
    url = mat_link(c['mat'], c['matName'])
    if not url: missing.append(c['matName'])
    bh = brand_href(c['brand'])
    by = f'<a href="{bh}">{e(c["brand"])}</a>' if bh else e(c['brand'])
    alt = f"{c['tileName']} mahjong tiles with {c['brand']} {mname} holiday mahjong mat"
    img = f"https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{sha}/assets/cards/holiday/{c['file']}"
    code = '' if (c['brand'] in NOCODE or c['tile'] == 'coquette' or c['brand'] == 'Maison Mahj') else '<span class="mm3-code">code MAHJMATCH</span>'
    btn = f'<a class="mm3-btn" href="{e(url)}" target="_blank" rel="sponsored noopener">Shop the {e(mname)}</a>' if url else ''
    rk = []
    for k in c['racks']:
        n, u = rack_link(k)
        rk.append(f'<a href="{e(u)}" target="_blank" rel="sponsored noopener">{e(n)}</a>' if u else e(n))
    star = '<span class="mm3-hstar">Matchmaker&#x27;s pick</span>' if c['star'] else ''
    fig = (f'<figure class="mm3-c mm3-hc"><div class="mm3-im"><img src="{img}" data-lb="" alt="{e(alt)}" loading="lazy" width="750" height="938">'
           f'<a class="mm3-pin" href="#" target="_blank" rel="noopener" aria-label="Save to Pinterest">Save</a></div>'
           f'<figcaption><span class="mm3-n">00</span><h3>{e(c["title"])}</h3>{star}<span class="mm3-by">Mat by {by}</span>'
           f'<div class="mm3-l">{btn}{code}</div>'
           f'<div class="mm3-rk" style="margin-top:8px;font-size:.82em;line-height:1.55">Rack matches: {" · ".join(rk)}</div></figcaption></figure>')
    key = slug if slug in albums else '_new:' + c['tile']
    o = out.setdefault(key, {'tile': c['tileName'], 'hol': c['hol'], 'cards': []})
    o['cards'].append((not c['star'], c['order'], fig))
res = {}
for k, v in out.items():
    v['cards'].sort(key=lambda x: (x[0], x[1]))
    res[k] = {'tile': v['tile'], 'hol': v['hol'], 'figs': [f for _, _, f in v['cards']]}
json.dump(res, open(sys.argv[4], 'w'))
print(len(res), 'albums;', sum(len(v['figs']) for v in res.values()), 'cards; existing albums:',
      sum(1 for k in res if not k.startswith('_new')), '; mats without link:', sorted(set(missing)))
