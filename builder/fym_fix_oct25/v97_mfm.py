"""FYM v97 (Version 1.1): My Fair Mahjong tile sets (docs/MATCH-INBOX.md, Tiffany Oct 26 5:45pm).
1. Five MFM sets were still HIDDEN by the old bag/box photo's no_tiles flag (The Jubilee Series, The Lumera Series, The Play Series,
   Crystal Confetti, Crystal Prism). Jubilee/Lumera/Play already show the Oct 21 audit's close pile (faces + backs). Crystal
   Confetti + Crystal Prism still showed the box + pouch shot with small tiles, so they get a close brand photo (faces + layered
   backs; listing images CO35FF_1 / COLLEC_2, looked at Oct 26 evening). All 5 are unhidden (+ YMI Mojave: same stale flag, its
   v94 faces|backs split was meant to bring it back per config/fym-ymi-splits-oct26.json 'unsoon'); locks.json (set hid), the tile
   photo flags and the upgrades list are updated to match (Tiffany's request = approval). Gate [85].
2. NEW: The Jubilee Series (Midnight Blue) (myfairmahjong.com/products/jubilee-midnight-blue, live since Aug 7 2026, $395):
   catalog set, m=[] (her Jubilee x Parquet Petal + MFM wood racks idea is logged for her album/swipe book, never put in m),
   brand photo JubileeSeries-MidnightBlue_6 (winds faces + navy marble backs), colours measured like v85 (back 50% + photo).
Colour ranking (s.cr) for these 7 sets is recomputed with v95_matrank on a scratch copy (+ v92_coordinated) and copied back,
so no other set's order moves. Idempotent. Usage: v97_mfm.py <build>"""
import sys, os, io, json, base64, hashlib, re, shutil, subprocess, tempfile, datetime
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
T, sets = D['tiles'], D['sets']
CB = 'assets/tiles/catalog-better/'
UNHIDE = ['my-fair-mahjong-the-jubilee-series', 'my-fair-mahjong-the-lumera-series', 'my-fair-mahjong-the-play-series',
          'my-fair-mahjong-crystal-confetti', 'my-fair-mahjong-crystal-prism',
          'yellow-mountain-imports-mojave']   # same stale-flag bug: flagged on its old lone-tile photo, already on its v94 faces|backs split (YMI 'unsoon')
NEWPHOTO = {'my-fair-mahjong-crystal-confetti': ('https://cdn.shopify.com/s/files/1/0703/3369/4263/files/CO35FF_1.png', 'close pile: faces + layered blue backs'),
            'my-fair-mahjong-crystal-prism': ('https://cdn.shopify.com/s/files/1/0703/3369/4263/files/COLLEC_2.jpg', 'close pile: faces + patterned backs')}
MID = dict(slug='my-fair-mahjong-the-jubilee-series-midnight-blue', key='myfairmahjong.com/jubilee-midnight-blue',
           name='The Jubilee Series (Midnight Blue)', handle='jubilee-midnight-blue',
           src='https://cdn.shopify.com/s/files/1/0703/3369/4263/files/JubileeSeries-MidnightBlue_6.png')
os.makedirs(B + '/t97', exist_ok=True); IMG = {}; log = []

def kmeans_sw(a, k=6, minw=.05):
    L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3); km = KMeans(n_clusters=k, n_init=3, random_state=0).fit(L)
    cnt = np.bincount(km.labels_, minlength=k) / len(L); out = []
    for j in np.argsort(-cnt):
        if cnt[j] < minw: continue
        rgb = np.clip(lab2rgb(km.cluster_centers_[j].reshape(1, 1, 3)).reshape(3), 0, 1)
        out.append(['#%02x%02x%02x' % tuple(int(round(x * 255)) for x in rgb), round(float(cnt[j]), 3)])
    return out
def photo_sw(im, back):  # same as v85_measure: back 50% + k-means of the photo with ivory/white faces dropped
    a = np.asarray(im.convert('RGB').resize((72, 72))).astype(float).reshape(-1, 3) / 255
    a = a[~((a.min(1) > .82) & (a.max(1) - a.min(1) < .12))]
    return [[back, 0.5]] + [[hx, round(w * .5, 3)] for hx, w in kmeans_sw(a)]
def use_photo(t, slug):
    """t.full -> t97/<slug>.jpg from the committed asset, pile = centred 360px square"""
    im = Image.open(REPO + CB + slug + '.jpg').convert('RGB'); fn = f't97/{slug}.jpg'; im.save(f'{B}/{fn}', quality=88)
    q = min(im.size); sq = im.crop(((im.width - q) // 2, (im.height - q) // 2, (im.width - q) // 2 + q, (im.height - q) // 2 + q)).resize((360, 360), Image.LANCZOS)
    b = io.BytesIO(); sq.save(b, 'JPEG', quality=84); pk = 'p97' + hashlib.md5(slug.encode()).hexdigest()[:10]
    IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    t.pop('fo', None)   # not a reframe of a locked photo: the new photo IS the photo (gate [3c]/[30] read t.src + flags)
    t.update(full=fn, pile=pk, src=CB + slug + '.jpg', bf=[.5, .5]); t.pop('cf', None); return im

# 1. new close photos for Confetti + Prism, unhide all 5
for s in sets:
    if s['slug'] in NEWPHOTO: use_photo(T[s['tile']], s['slug']); s['fp'] = [.5, .5]; s['fz'] = 1
    if s['slug'] in UNHIDE and s.get('hid'): s.pop('hid'); log.append('unhid ' + s['name'])
    if s['slug'] in UNHIDE: T[s['tile']].pop('hid', None)

# 2. Jubilee Midnight Blue
if MID['key'] not in T:
    base = T['myfairmahjong.com/jubilee-pearl-white']
    T[MID['key']] = dict(n=MID['name'], bn='My Fair Mahjong', u='https://myfairmahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2F' + MID['handle'],
                         dc=base['dc'], pa=True, nc=False, rt=False, cat=True, u0='https://myfairmahjong.com/products/' + MID['handle'], add='oct26-v97')
im_mid = use_photo(T[MID['key']], MID['slug'])
a = np.asarray(im_mid.resize((200, 200))).astype(float).reshape(-1, 3) / 255; L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3)
navy = a[(L[:, 0] < 45) & (L[:, 2] < -12)]   # navy marble backs
BACK = '#%02x%02x%02x' % tuple(int(round(x * 255)) for x in np.median(navy, 0))
s_mid = next((s for s in sets if s['slug'] == MID['slug']), None)
if s_mid is None:
    tmpl = next(s for s in sets if s['slug'] == 'my-fair-mahjong-the-jubilee-series')
    s_mid = {k: v for k, v in tmpl.items() if k not in ('cr', 'hid', 'bsw', 'sb')}; s_mid['rank'] = list(tmpl['rank']); sets.append(s_mid); log.append('added ' + MID['name'])
s_mid.update(slug=MID['slug'], name=MID['name'], maker='My Fair Mahjong', tile=MID['key'], tc=BACK, m=[], album='', tag='', cat=True, fp=[.5, .5], fz=1)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
j = h.index('const BACKG=') + len('const BACKG='); BG, bend = json.JSONDecoder().raw_decode(h[j:]); bend += j
if MID['name'] not in BG['Blue']: BG['Blue'].append(MID['name'])
h = h[:j] + json.dumps(BG, ensure_ascii=False) + h[bend:]
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a_ = '<script src="b24v1.js"></script>'; assert h.count(a_) == 1; h = h.replace(a_, a_ + inl, 1)
open(P, 'w').write(h)

# colours (config/fym-colour-oct25.json, v85 format) for the 3 new photos
C = json.load(open(REPO + 'config/fym-colour-oct25.json'))
for slug in list(NEWPHOTO) + [MID['slug']]:
    back = BACK if slug == MID['slug'] else C['sets'][slug]['back']
    C['sets'][slug] = {'sw': photo_sw(Image.open(REPO + CB + slug + '.jpg'), back), 'tone': 'clean', 'src': 'back+photo', 'back': back}
json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)

# s.cr for the 7 sets: v95_matrank (--only) + v92_coordinated on a scratch copy, copy back just these sets
ONLY = UNHIDE + [MID['slug']]
tmp = tempfile.mkdtemp(); shutil.copytree(B, tmp + '/b', symlinks=True)
for sc in (['v95_matrank.py', tmp + '/b', '--only', ','.join(ONLY)], ['v92_coordinated.py', tmp + '/b']):
    subprocess.run([sys.executable, REPO + 'builder/fym_fix_oct25/' + sc[0]] + sc[1:], check=True, capture_output=True)
h2 = open(tmp + '/b/index.html').read(); i2 = h2.index('const D=') + 8; D2, _ = json.JSONDecoder().raw_decode(h2[i2:]); shutil.rmtree(tmp)
CR = {s['slug']: (s.get('cr'), s.get('bsw')) for s in D2['sets'] if s['slug'] in ONLY}
h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
for s in D['sets']:
    if s['slug'] in CR and CR[s['slug']][0]:
        s['cr'] = CR[s['slug']][0]
        if CR[s['slug']][1]: s['bsw'] = CR[s['slug']][1]
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h)

# repo state: locks, tile photo flags, upgrades (idempotent)
today = '2026-10-26'
LP = REPO + 'builder/fym_flags/locks.json'; Lk = json.load(open(LP)); ch = False
for slug in UNHIDE:
    if Lk['sets'].get(slug, {}).get('hid'): Lk['sets'][slug]['hid'] = False; ch = True
note = f'{today}: 5 My Fair Mahjong sets + YMI Mojave unhidden (stale no_tiles flag from the old photo; Tiffany 5:45pm), Crystal Confetti + Prism on close brand photos (v97_mfm.py)'
if ch and note not in Lk['_changes']: Lk['_changes'].append(note)
json.dump(Lk, open(LP, 'w'), indent=1, ensure_ascii=False)
FP = REPO + 'builder/fym_flags/tile_photo_flags.json'; Fl = json.load(open(FP))
for s in D['sets']:
    if s['slug'] in UNHIDE:
        Fl[s['slug']] = {'name': s['name'], 'maker': s['maker'], 'flag': 'ok', 'photo': T[s['tile']].get('fo') or T[s['tile']]['full'], 'shown': T[s['tile']]['full'],
                         'note': f'{today} v97: current photo shows faces + backs (looked at); the no_tiles flag was for the old photo ' + str((Fl.get(s['slug']) or {}).get('photo'))}
json.dump(Fl, open(FP, 'w'), indent=1, ensure_ascii=False)
UP = REPO + 'builder/fym_flags/tile_photo_upgrades.json'; U = json.load(open(UP))
for slug in UNHIDE:
    u = U['sets'].get(slug)
    if not u: continue
    u['hidden_now'] = False
    if slug in NEWPHOTO: u.update(status='upgrade', proposed=CB + slug + '.jpg', source_url=NEWPHOTO[slug][0], reason=NEWPHOTO[slug][1], kind='pile', applied='v97')
json.dump(U, open(UP, 'w'), indent=1, ensure_ascii=False)
print('\n'.join(log)); print('v97 mfm: midnight back', BACK, 'cr copied', len(CR))
