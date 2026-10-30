"""FYM v106 = public "Version 1.9.1" (Oct 30 eve), on top of v105 + partneradds106 (YOLO + Noli June mats).
1. Racks step brand filter shows ALL of a brand's racks (Tiffany 5:14pm: "when I filter by brand I'm only seeing the clear wood").
   Cause: with "Tiffany's picks: on" (the default when she has rack picks) rackDeck() kept only her picks + universal racks,
   then the brand filter ran on that short list -> Bird & Bamboo showed only the 1-4 B&B racks she picked. Same for matDeck().
   Fix: when a brand is picked, her picks of that brand lead, then every other visible rack/mat of that brand in rank order.
2. Bird & Bamboo wood stains: Weathered Oak / Provincial / Red Mahogany / Dark Walnut were rf ['brown'] only, so the Wood
   finish chip showed only Clear. They are stained wood: rf += 'wood' (colour family kept). + White Wood Stain (MATCH-INBOX
   Oct 27; in stock on birdandbamboo.com Oct 30): the same blank as every B&B rack recoloured to the White band of B&B's
   own 'WOOD STAINS' swatch photo (#e4d9cd), like the other 93 B&B colours (builder/bbrack.py).
3. YOLO Mahjong (MATCH-INBOX Oct 28 NEW PARTNER): 2 racks (cut from the brand's product photos, checked on white + navy),
   Journey to the West tile set (catalog set, m=[]), Pink Tiger (her pick, yolo:pink-tiger) relinked with code + ref, YOLO logo.
4. Noli June: brand-menu note says "10% off $100+" (never a plain 10%; MATCH-INBOX Oct 30 10:30am).
5. Version 1.9.1.  Usage: python3 v106extra.py <build dir>"""
import sys, os, io, json, base64, hashlib, re, tempfile, shutil, subprocess
import numpy as np
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'builder')
import bbrack
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()

def rep(a, b, n=1):
    global h
    c = h.count(a); assert c == n, (c, a[:90]); h = h.replace(a, b)

# ---------- code
rep("if(f.her){const U=uni();ids=ids.filter(r=>hr.includes(r)||U.includes(r));}",
    "if(f.her){const U=uni(),hu=r=>hr.includes(r)||U.includes(r);ids=f.brand?[...ids.filter(hu),...ids.filter(r=>!hu(r))]:ids.filter(hu);}/*v106: a picked brand shows ALL its racks, her picks first (Tiffany Oct 30 5:14pm)*/")
rep("if(f.her)ids=ids.filter(herMat);",
    "if(f.her&&f.brand){const hs=new Set(ids.filter(herMat));ids=[...hs,...MSL(colorPool()).filter(x=>!hs.has(x))];}else if(f.her)ids=ids.filter(herMat);/*v106: brand = all its mats, her picks first*/")
rep("function bnote(b){", "const BMIN={'Noli June':'10% off $100+'};/*v106: Noli June code has a $100 minimum*/\nfunction bnote(b){")
rep("return BCODE[b]?`<p class=\"bnote ok\"><span>✦ Save 10% or more at ${esc(b)} with code <b>MAHJMATCH</b></span></p>`",
    "return BCODE[b]?(BMIN[b]?`<p class=\"bnote ok\"><span>✦ ${BMIN[b]} at ${esc(b)} with code <b>MAHJMATCH</b></span></p>`:`<p class=\"bnote ok\"><span>✦ Save 10% or more at ${esc(b)} with code <b>MAHJMATCH</b></span></p>`)")
rep("o=b=>`<option value=\"${esc(b)}\"${cur===b?' selected':''}>${esc(b)} (${n[b]})</option>`",
    "o=b=>`<option value=\"${esc(b)}\"${cur===b?' selected':''}>${esc(b)} (${n[b]})${BMIN[b]?' \\u00b7 '+BMIN[b]:''}</option>`")
h = h.replace('Version 1.9<', 'Version 1.9.1<').replace('(Version 1.9)', '(Version 1.9.1)')
assert h.count('Version 1.9.1') == 2, h.count('Version 1.9.1')

# ---------- data
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M, R, T, sets = D['mats'], D['racks'], D['tiles'], D['sets']
IMG = {}; added = []
for k in ('bb:Weathered Oak', 'bb:Provincial', 'bb:Red Mahogany', 'bb:Dark Walnut'):
    r = R[k]
    if 'wood' not in r['rf']: r['rf'] = r['rf'] + ['wood']
    r.setdefault('rs', {})['wood'] = max(r['rs'].get('wood', 0), 1.5); added.append(('rack rf+wood', r['n']))
# White Wood Stain: Clear's HD image (the shared B&B blank) recoloured
hdi = json.load(open(B + '/hd/index.json')); base = None
v = hdi['r']['bb:Clear']; du = json.load(open(B + '/hd/' + v))['bb:Clear']
base = Image.open(io.BytesIO(base64.b64decode(du.split(',', 1)[1]))).convert('RGBA')
WH = '#e4d9cd'; rc = bbrack.recolor(base, WH)
os.makedirs(REPO + 'assets/racks/v106', exist_ok=True); rc.save(REPO + 'assets/racks/v106/bird-and-bamboo-white-wood-stain.png')
def img_uri(im, w=700, fmt='WEBP'):
    t = im.copy(); t.thumbnail((w, w)); b = io.BytesIO(); t.save(b, fmt, quality=84, method=6) if fmt == 'WEBP' else t.save(b, fmt, quality=84)
    return f'data:image/{fmt.lower()};base64,' + base64.b64encode(b.getvalue()).decode()
c = R['bb:Clear']
k = 'bb:White Wood Stain'
if k not in R:
    vid = '47160204460184'
    R[k] = dict(n='Bird & Bamboo White Wood Stain', bn='Bird & Bamboo', b='Bird & Bamboo',
                u=re.sub(r'variant%3D\d+', f'variant%3D{vid}', c['u']),
                u0=re.sub(r'variant=\d+', f'variant={vid}', c['u0']), dc=c['dc'], pa=True, nc=False, rt=False, c=True, ml=False, sk=True,
                hx=WH, rf=['neutral', 'wood'], rs={'neutral': 1.2, 'wood': 1.6}, pq=5, im='rk106bbwhitewood', add='oct30-v106')
    IMG['rk106bbwhitewood'] = img_uri(rc, 420)
    added.append(('rack', 'Bird & Bamboo White Wood Stain', R[k]['u0']))
# YOLO racks + tile set
YREF = '12572562.5IBLjBHZ1vuX4J'; YDC = 'https://mahjmatchmaker.com/yolo-mahjong-discount-code'
yl = lambda hd: (f'https://www.yolomahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2F{hd}%3Fsca_ref%3D{YREF}', f'https://www.yolomahjong.com/products/{hd}?sca_ref={YREF}')
YR = [('journey-to-the-west-golden-wooden-rack-20', 'YOLO Mahjong Metallic Gold Wooden', 'assets/racks/v106/yolo-metallic-gold-wooden.png', '#d9b84f', ['yellow', 'metallic'], {'yellow': 1.5, 'metallic': 1.3}),
      ('journey-to-the-west-tortoiseshell-acrylic-rack-20', 'YOLO Mahjong Tortoiseshell Acrylic', 'assets/racks/v106/yolo-tortoiseshell-acrylic.png', '#6b3a1c', ['tortoise'], {'tortoise': 1.6})]
for hd, name, f, hx, rf, rs in YR:
    key = f'www.yolomahjong.com/{hd}'
    if key in R: continue
    u, u0 = yl(hd); th = 'rk106' + hashlib.md5(key.encode()).hexdigest()[:8]
    IMG[th] = img_uri(Image.open(REPO + f).convert('RGBA'), 700)
    R[key] = dict(n=name, bn='YOLO Mahjong', b='yolomahjong.com', u=u, u0=u0, dc=YDC, pa=True, nc=False, rt=False, c=False, ml=False, sk=False,
                  hx=hx, rf=rf, rs=rs, pq=4, im=th, add='oct30-v106')
    added.append(('rack', name))
o = M.get('yolo:pink-tiger')
if o:
    hd = 'pink-tiger-mahjong-mat-floral-chinese-mahjong-table-mat-for-mahjong-set-31-5-x-31-5-inch'; u, u0 = yl(hd)
    o.update(u=u, u0=u0, dc=YDC, pa=True, b='yolomahjong.com'); added.append(('relink', 'YOLO Pink Tiger (her pick)'))
tk = 'www.yolomahjong.com/journey-to-the-west-collection-mahjong-tiles'; slug = 'yolo-journey-to-the-west'
if tk not in T:
    os.makedirs(B + '/t106', exist_ok=True)
    im = Image.open(REPO + 'assets/tiles/v106/yolo-journey-to-the-west.jpg').convert('RGB')
    fn = 't106/yolo-journey-to-the-west.jpg'
    if os.path.exists(B + '/' + fn): os.remove(B + '/' + fn)
    t_ = im.copy(); t_.thumbnail((1000, 1000)); t_.save(B + '/' + fn, quality=80, optimize=True, progressive=True)
    S_ = min(im.size); sq = im.crop(((im.width - S_) // 2, (im.height - S_) // 2, (im.width + S_) // 2, (im.height + S_) // 2)).resize((360, 360), Image.LANCZOS)
    pk = 'p106yolojttw'; b = io.BytesIO(); sq.save(b, 'JPEG', quality=84); IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    u, u0 = yl('journey-to-the-west-collection-mahjong-tiles')
    T[tk] = dict(full=fn, n='Journey to the West', bn='YOLO Mahjong', u=u, dc=YDC, pa=True, nc=False, rt=False, pile=pk,
                 src='assets/tiles/v106/yolo-journey-to-the-west.jpg', u0=u0, add='oct30-v106')
    tmpl = next((s for s in sets if s['name'].startswith('Heritage')), sets[0])
    sets.append(dict(slug=slug, name='Journey to the West', maker='YOLO Mahjong', tile=tk, tc='#8a1f2d', tag='', album='', rank=list(tmpl['rank']), m=[], cr=[]))
    added.append(('tiles', 'YOLO Journey to the West', 'catalog set m=[]'))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
# tile colour group (Ivory backs, red + gold faces)
j = h.index('const BACKG=') + len('const BACKG='); BG, bend = json.JSONDecoder().raw_decode(h[j:]); bend += j
for g in ('Ivory', 'Red'):
    if 'Journey to the West' not in BG[g]: BG[g].append('Journey to the West')
h = h[:j] + json.dumps(BG, ensure_ascii=False) + h[bend:]
# YOLO logo on the tiles-door logo grid (same trim + fit as fym_fix_oct30_logos.py)
j = h.index('const BLOGO=') + len('const BLOGO='); BL, bend = json.JSONDecoder().raw_decode(h[j:]); bend += j
if 'YOLO Mahjong' not in BL:
    lg = Image.open(REPO + 'assets/brand/partner-logos/yolo-mahjong.png').convert('RGBA')
    a = np.asarray(lg); vis = (a[..., 3] > 24) & ~((a[..., 0] > 240) & (a[..., 1] > 240) & (a[..., 2] > 240))
    ys, xs = np.where(vis); lg = lg.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    s = min(360 / lg.width, 150 / lg.height); lg = lg.resize((max(1, round(lg.width * s)), max(1, round(lg.height * s))), Image.LANCZOS)
    b = io.BytesIO(); lg.save(b, 'WEBP', quality=88, method=6); BL['YOLO Mahjong'] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    h = h[:j] + json.dumps(BL, ensure_ascii=False) + h[bend:]
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'
    if h.count(a) == 1: h = h.replace(a, a + inl, 1)
    else:
        a = '<script>window.IMG=Object.assign(window.IMG||{},'; assert a in h; h = h.replace(a, inl + a, 1)
open(P, 'w').write(h)
# colour ranking (cr) for the new tile set (as partneradds: v85_colorrank on a scratch copy, copy back only this set's cr)
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
im = Image.open(REPO + 'assets/tiles/v106/yolo-journey-to-the-west.jpg').convert('RGB')
a = np.asarray(im.resize((120, 100))).astype(float).reshape(-1, 3) / 255; a = a[~(a.min(1) > .82)]
L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3); km = KMeans(n_clusters=6, n_init=3, random_state=0).fit(L)
cnt = np.bincount(km.labels_, minlength=6) / len(L); sw = []
for jj in np.argsort(-cnt):
    if cnt[jj] < .05: continue
    rgb = np.clip(lab2rgb(km.cluster_centers_[jj].reshape(1, 1, 3)).reshape(3), 0, 1)
    sw.append(['#%02x%02x%02x' % tuple(int(round(v * 255)) for v in rgb), round(float(cnt[jj]), 3)])
C = json.load(open(REPO + 'config/fym-colour-oct25.json')); C['sets'][slug] = {'sw': sw, 'tone': 'clean', 'src': 'photo', 'back': '#f4ecd8'}
json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
tmp = tempfile.mkdtemp(); shutil.copy(P, tmp + '/index.html')
subprocess.run([sys.executable, REPO + 'builder/fym_fix_oct25/v85_colorrank.py', tmp], check=True, capture_output=True)
h2 = open(tmp + '/index.html').read(); i2 = h2.index('const D=') + 8; D2, _ = json.JSONDecoder().raw_decode(h2[i2:])
cr = next((s.get('cr') for s in D2['sets'] if s['slug'] == slug), None); shutil.rmtree(tmp)
h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
for s in D['sets']:
    if s['slug'] == slug and cr: s['cr'] = cr
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h)
# repo records
LK = json.load(open(REPO + 'builder/fym_flags/locks.json'))
LK['tiles'][tk] = {'set': 'Journey to the West', 'src': 'assets/tiles/v106/yolo-journey-to-the-west.jpg', 'full': 't106/yolo-journey-to-the-west.jpg', 'pile': 'p106yolojttw'}
LK['sets'][slug] = {'m': [], 'name': 'Journey to the West'}
json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
TF = json.load(open(REPO + 'builder/fym_flags/tile_photo_flags.json'))
TF[slug] = {'flag': 'ok', 'note': 'Oct 30 v106: YOLO listing image 0 (joker tiles on their Journey mat), tiles fill the frame'}
json.dump(TF, open(REPO + 'builder/fym_flags/tile_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
for a_ in added: print(*a_)
