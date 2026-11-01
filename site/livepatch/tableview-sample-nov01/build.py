"""Table View Sample (Nov 1, Tiffany 5:06am: build the storyboard v3 as a working sample she can play with).
Pulls a light subset of the LIVE v112 FYM build data (sets, mats, racks, tiles, logos) + coverage classes
(config/tableview-photo-class-nov01.json) + stock (config/fym-stock.json), shrinks every photo to webp data URLs,
and writes index.html = app.html with /*DATA*/ replaced. Usage: python3 build.py <b112 build dir>"""
import sys, json, io, base64, struct, glob, os, re, colorsys, pathlib
from PIL import Image
HERE = pathlib.Path(__file__).parent; R = HERE.parents[2]
B = sys.argv[1]
h = open(B + '/index.html').read()
IMG = {}; pat = 'Object.assign(window.IMG||{},'
for t in [h] + [open(f).read() for f in glob.glob(B + '/b*.js')]:
    p = 0
    while (j := t.find(pat, p)) >= 0:
        o, e = json.JSONDecoder().raw_decode(t[j + len(pat):]); IMG.update(o); p = j + len(pat) + e
i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
MC = {}
for f in glob.glob(B + '/mc/*.webp'):
    ab = open(f, 'rb').read(); n = struct.unpack('<I', ab[-4:])[0]
    try: hh = json.loads(ab[-4 - n:-4])
    except Exception: continue
    for k, (a, l) in hh.items(): MC[k] = (f, a, l)
COV = json.load(open(R / 'config/tableview-photo-class-nov01.json'))
STK = json.load(open(R / 'config/fym-stock.json'))['items']
LINKONLY = {'Tigre de Tartan'}

def from_img(key):
    d = IMG.get(key)
    return Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))) if d else None
def from_path(p):
    if p in MC:
        f, a, l = MC[p]; return Image.open(io.BytesIO(open(f, 'rb').read()[a:a + l]))
    return Image.open(B + '/' + p) if os.path.exists(B + '/' + p) else None
def url(im, px, q=68, square=False, keep_alpha=False):
    if im is None: return None
    im = im.convert('RGBA' if keep_alpha else 'RGB')
    if square:
        s = min(im.size); im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2))
    im.thumbnail((px, px), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
def fam(hx):
    r, g, b = (int(hx[k:k + 2], 16) / 255 for k in (1, 3, 5)); hh, l, s = colorsys.rgb_to_hls(r, g, b); hh *= 360
    if s < .18 or l > .9: return 'neutral' if l > .35 else 'black'
    if l < .18: return 'black'
    for lim, name in ((15, 'red'), (40, 'orange'), (68, 'yellow'), (165, 'green'), (255, 'blue'), (290, 'purple'), (340, 'pink'), (361, 'red')):
        if hh < lim: return name
SLUGS = ['oh-my-mahjong-papaya-spritz', 'solara', 'limoncello', 'pippa', 'sunset', 'amara', 'tortoise', 'jade', 'la-fete', 'glow-wild',
         'drake', 'lagoon', 'coquette', 'heritage', 'gatsby', 'willow', 'moonlight', 'nantucket', 'palm-royale', 'talulah', 'birdie',
         'sorbet', 'anders-ruff-brownstone-bloom', 'sunday-mahjong-hummingbird', 'sunday-mahjong-sunday', 'malachite', 'emerald',
         'seabreeze', 'dear-santa', 'nutcracker-ballet', 'sunday-mahjong-nature-walk']
SB = {s['slug']: s for s in D['sets']}
# one pattern-back set with no back photo (walls greyed demo)
for sl, v in COV['_sets'].items():
    if v['back_type'] == 'pattern' and v['back_photo'] != 'Y' and sl in SB and not SB[sl].get('hid'):
        SLUGS.append(sl); break
FRUIT = 'www.middleandmainmahjong.com/fruit-stand-citrus-mat'
mats, racks, tiles, sets = {}, {}, {}, []
def add_mat(k):
    if k in mats or k not in D['mats'] or D['mats'][k].get('hid'): return k in mats
    if len(mats) >= 78 and k != FRUIT: return False
    m = D['mats'][k]; c = COV.get(k, {'class': 'C', 'racks': 'none'})
    cls = c['class'] if c.get('racks') != 'colored' else 'C'
    full = from_path(m['f']) if m.get('f') else None
    if k == FRUIT: full = Image.open(R / 'assets/table-view/src/mm-fruit-stand-overhead-photo.jpg')
    mats[k] = dict(n=m['n'], bn=m['bn'], pa=bool(m.get('pa')), nc=bool(m.get('nc')), u=m.get('u'), rt=bool(m.get('rt')),
                   mf=m.get('mf', []), hol=bool(m.get('hol')), cls=cls, rk=c.get('racks', 'none'),
                   why={'B': 'Only a close-up or corner photo of this mat, so Corner view only.',
                        'C': ('This mat’s photo has its own colored racks on it.' if c.get('racks') == 'colored' else 'No flat, top-down photo of this mat yet.')}.get(cls, ''),
                   so=bool(STK.get('m:' + k, {}).get('in') is False),
                   th=url(from_img(m.get('th')) or full, 120, 62, square=True), im=url(full, 560, 58) if cls != 'C' else None)
    return True
def add_rack(k):
    if k in racks or k not in D['racks']: return k in racks
    if len(racks) >= 48: return False
    r = D['racks'][k]; c = COV['_racks'].get(k, {'class': 'G'})
    im = from_img(r.get('im'))
    if k in ('bb:Lilac', 'bb:Lavender'):
        im = Image.open(R / ('assets/table-view/src/bb-real/' + ('bb-p51-lilac-rack-overhead.png' if k == 'bb:Lilac' else 'bb-p51-rack-overhead-lavender.png'))); c = {'class': 'S'}
    ok = c['class'] == 'S' and im is not None and im.mode == 'RGBA' and im.width > im.height * 3
    racks[k] = dict(n=r['n'], bn=r['bn'], pa=bool(r.get('pa')), nc=bool(r.get('nc')), u=r.get('u'), hx=r.get('hx', '#ccc'), rf=r.get('rf', []),
                    len=float(r.get('len') or 20), ok=ok, why='' if ok else ('Only a group or lifestyle photo of these racks.' if c['class'] == 'G' else 'Only an angled photo of these racks.'),
                    so=bool(STK.get('r:' + k, {}).get('in') is False),
                    th=url(im, 260, 72, keep_alpha=True), im=url(im, 640, 74, keep_alpha=True) if ok else None)
    return True
for sl in SLUGS:
    s = SB.get(sl)
    if not s or s.get('hid'): continue
    t = D['tiles'].get(s['tile'])
    if not t: continue
    cv = COV['_sets'].get(sl, {'back_photo': 'N', 'back_type': 'unknown'})
    walls = not (cv['back_type'] == 'pattern' and cv['back_photo'] != 'Y')
    face = from_path(t['full']) if t.get('full') else from_img(t.get('pile'))
    picks, recs = [], {}
    for mk, rl in s['m'][:5]:
        if add_mat(mk): picks.append(mk); recs[mk] = [x for x in rl if add_rack(x)][:5]
    color = []
    for idx in s['rank'][:12]:
        mk = D['order'][idx]
        if mk not in picks and add_mat(mk): color.append(mk)
        if len(color) >= 3: break
    if sl == 'oh-my-mahjong-papaya-spritz':
        add_mat(FRUIT); picks.insert(0, FRUIT); recs[FRUIT] = [x for x in ['bb:Lilac', 'bb:Lavender', 'plm:Chartreuse', 'www.middleandmainmahjong.com/golden-grain-beechwood-mahjong-rack-and-pusher-set-of-4'] if add_rack(x)]
    rk = [x for x in D['lt'].get(sl, []) if add_rack(x)]
    for idx in s['cr'][:6]:
        x = D['uni'][idx] if idx < len(D['uni']) else None
        if x and add_rack(x) and x not in rk: rk.append(x)
    tiles[sl] = dict(n=s['name'], bn=t['bn'], pa=bool(t.get('pa')), nc=bool(t.get('nc')), u=t.get('u'), tc=s.get('tc', '#888'), fam=fam(s.get('tc', '#888888')),
                     tw=float(t.get('tw') or .9), walls=walls, pat=cv['back_type'] == 'pattern', so=bool(t.get('oos') or t.get('so')),
                     face=url(face, 320, 64, square=True), th=url(face, 120, 64, square=True), back=None)
    sets.append(dict(slug=sl, picks=picks, color=color, recs=recs, racks=rk))
bp = Image.open(R / 'assets/table-view/src/omm-papaya-back-photo.png').convert('RGBA')
bp = bp.crop(bp.split()[3].point(lambda v: 255 if v > 128 else 0).getbbox())
tiles['oh-my-mahjong-papaya-spritz']['back'] = url(bp, 160, 80, keep_alpha=True)
brands = sorted({x['bn'] for x in list(mats.values()) + list(racks.values()) + list(tiles.values())})
logos = {b: url(from_img(D['logos'][b]), 200, 80, keep_alpha=True) for b in brands if b in D['logos'] and from_img(D['logos'][b])}
DATA = dict(sets=sets, mats=mats, racks=racks, tiles=tiles, logos=logos, linkonly=sorted(LINKONLY), checked=json.load(open(R / 'config/fym-stock.json')).get('checked', ''))
js = json.dumps(DATA, separators=(',', ':'), ensure_ascii=False)
app = (HERE / 'app.html').read_text()
out = app.replace('/*DATA*/null', js)
(HERE / 'index.html').write_text(out)
print('sets', len(sets), 'mats', len(mats), 'racks', len(racks), 'usable racks', sum(r['ok'] for r in racks.values()),
      'mat classes', {c: sum(m['cls'] == c for m in mats.values()) for c in 'ABC'}, 'logos', len(logos), 'index KB', len(out) // 1024)
