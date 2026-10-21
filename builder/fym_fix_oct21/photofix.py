"""FYM Oct 21 photo fix (rule 6: mats show the mat flat, tiles show tiles). STAGED ONLY; the main session publishes.
Usage: python3 builder/fym_fix_oct21/photofix.py <site_dir> <out_dir>
  site_dir: live build (read only), e.g. scratchpad/fym-oct20e (artifact v64)
  out_dir : staged build, e.g. scratchpad/fym-oct21a (copied from site_dir if missing; index.html + hd/index.json re-derived from site_dir)
QA (Oct 20e) flagged 25 mats + 2 tile photos (room shots, tiles/racks/props on the mat, close or corner crops, logo / colour blocks).
Every product image on each brand's Shopify store (/products/<handle>.json) was checked by eye (contact sheets).
 FIX    : new photo from the brand's own images (originals kept in assets/mats/clean + assets/tiles/clean, sources in oct21_sources.json).
          Mats: perspective-corrected crop of the whole mat (corners below), no props. Packed like round 3: m/<n>.webp in a new mc chunk,
          150px thumbnail + tile pile thumbnails in b17v1.js, tile 'full' in t17/, match card hd -> file:t17/...
 HIDE   : unlocked mats with no acceptable photo -> hid=true + mat_photo_flags no_flat_photo (gate [3] keeps them hidden).
 REVIEW : locked mats (locks.json pins f/th/hid) are NOT changed. Flag locked_needs_approval; the prepared candidate (if any) is saved in
          assets/mats/clean/review_oct21/ and listed in builder/fym_fix_oct21/review_locked.json. Apply only after Tiffany's OK
          (then edit locks.json in the same commit).
"""
import sys, os, json, shutil, re, io, base64, hashlib, struct
import numpy as np, cv2
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
SITE, OUT = sys.argv[1], sys.argv[2]
if not os.path.exists(OUT):
    shutil.copytree(SITE, OUT)
CLEAN_M, CLEAN_T = REPO + 'assets/mats/clean/', REPO + 'assets/tiles/clean/'
SRC = json.load(open(CLEAN_M + 'oct21_sources.json'))

FIX_MATS = {   # key -> (original in assets/mats/clean, warp corners TL TR BR BL in original pixels, output side)
    'mahjsquadshop.com/vintage-rose-mahjong-mat-pink-mahj-mat-floral-neoprene-mahjongg-mat':
        ('vintage-rose-mahj-squad.webp', [(124, 26), (846, 18), (984, 726), (46, 726)], 1000,
         'brand photo 2/10: whole mat on a table seen from above, no tiles; perspective-corrected crop to the mat'),
}
REVIEW = {   # locked mats: candidate prepared, NOT applied
    'splashofcolorco.com/modern-nordic-scandinavian-folk-art-mahjong-mat-sleek-surface':
        ('modern-nordic-splash-of-color.jpg', [(4, 510), (606, 251), (1116, 607), (396, 1025)], 1100,
         'brand product render 2/7 (mat laid flat at an angle beside its bag, bag does not touch the mat); flattened, whole mat, no props. Strong candidate.'),
    'mahjsquadshop.com/palm-springs-mahjong-mat-neoprene-mahjong-mat-in-palm-springs-mid-century-mahjong-mat-pink-mahjong-tropical-mahj-mahjongg-mat-1':
        ('palm-springs-mahj-squad.webp', [(233, 99), (795, 89), (955, 567), (67, 557)], 1000,
         'brand photo 1/13: whole mat on a table, no tiles/racks; perspective-corrected crop to the mat. Strong candidate.'),
    'tigredetartan.com/katherine-hartman-x-tigre-de-tartan':
        ('birdsong-katherine-hartman-tigre-de-tartan.jpg', [(1137, 1297), (3378, 1557), (3425, 3802), (-9, 3028)], 1200,
         'brand photo 3/12: mat on a card table in a room, nothing on it; perspective-corrected crop. The left edge is a little cut off in the source.'),
}
REVIEW_NONE = {   # locked, no acceptable image on the brand store: recommend hiding once she OKs
    'mahjsquadshop.com/bejeweled-dream-mahjong-mat': 'all 18 brand images have tiles/racks on the mat or are partial close-ups',
    'mahjsquadshop.com/candy-cane-pink-wonderland-mahjong-mat': 'all 5 brand images are room shots or close-ups with racks',
    'tigredetartan.com/mahjong-mat-el-tigre-new-edition': '10 brand images: tiles/racks/people; the cleanest (current) shows the mat inside a wooden tray frame',
    'tigredetartan.com/tigre-de-tartan-x-miss-mahjong-el-ultimo-refresco-mahjong-mat': 'all 12 brand images have racks/tiles on the mat',
    'tigredetartan.com/mahjong-mat-mantel-mates': 'all 7 brand images have racks/tiles/a figurine on the mat',
    'tigredetartan.com/paige-spearin-shell-yeah-mahjong-mat': 'all 5 brand images are close-ups with tiles/racks',
    'tigredetartan.com/mahjong-mat-french-mural': 'all 6 brand images have racks/tiles/cards or a person',
    'tigredetartan.com/third-shipment-mahjong-mat-jardin-de-los-jefes': 'all 8 brand images have tiles/racks/a bag or are close-ups',
    'tigredetartan.com/mahjong-mat-caned-trompe-l-oeil-natural': 'all 5 brand images have racks/cards/tiles',
    'tigredetartan.com/mahjong-mat-hearts-horseshoes-2': 'all 6 brand images have racks/cards/a pouch',
    'tigredetartan.com/mahjong-mat-cannage-blonde-rules-edition': 'all 7 brand images have racks/tiles/dice or are a room shot',
    'alb:cypress-forest:Dapper 1': 'retired Oh My Mahjong mat, no product page left; album photo has racks/tiles/a bag on the mat',
    'www.bespokemahjong.com/graymalingamemat': '10 brand images: corner crops, tiles/racks, or a gift box sitting on the mat; no whole-mat photo',
}
HIDE = {   # unlocked, no acceptable photo -> hidden
    'mahjsquadshop.com/green-malachite-mahjong-mat-emerald-green-and-jewel-neoprene-mahjongg-mat-jewel-tone-mahj-mat-malachite-stone-mahj-ongg-mat-1':
        'all 7 brand images are AI room renders at a steep angle; the only whole-mat view flattens to a distorted, low-res image',
    'mahjsquadshop.com/regency-mahjong-mat': 'all 10 brand images are close-ups with tiles/dice/a tray',
    'mahjsquadshop.com/jade-green-chinoiserie-mahjong-mat': '17 brand images: tiles on the mat or partial close-ups, no whole-mat view',
    'mahjsquadshop.com/blue-chinoiserie-mahjong-mat-copy': '8 brand images: racks/tiles on the mat or a partial pattern close-up',
    'missmahjong.com/el-ultimo-refresco-mahjong-playing-mat': 'all 4 brand images are tilted close-ups with tiles',
    'sundaymahjong.com/vegan-leather-premium-mahjong-mat': 'all 4 brand images are patio shots with racks/tiles on the mat',
    'tigredetartan.com/paige-spearin-mahjong-mat-apres-mahj': 'only 1 brand image, tiles scattered on the mat',
    'www.hiphipmahjong.com/celebration-mahjong-mat': 'only 1 brand image, tiles/racks/props on the mat',
}
FIX_TILES = {   # tile key -> (set slug, original in assets/tiles/clean, note)
    'mahjmood.com/90s-tile-set?v=58077240361263': ('mahj-mood-90s-pool-party-blue', '90s-pool-party-blue-mahj-mood.jpg',
        'brand image 1/4: pile of tiles, blue backs + faces (old photo was colour blocks)'),
    'charlestonmahjongclub.com/the-country-club-edition': ('charleston-mahjong-club-the-country-club-edition', 'country-club-edition-charleston-mahjong-club.jpg',
        'brand image 5/14: tile faces + the green back (old photo was the logo card)'),
}

h = open(os.path.join(SITE, 'index.html')).read()
i = h.find('const D=') + 8
D, end = json.JSONDecoder().raw_decode(h, i)
M, T = D['mats'], D['tiles']
LOCKS = json.load(open(REPO + 'builder/fym_flags/locks.json'))
FLAGS_P, TFLAGS_P = REPO + 'builder/fym_flags/mat_photo_flags.json', REPO + 'builder/fym_flags/tile_photo_flags.json'
FLAGS, TFLAGS = json.load(open(FLAGS_P)), json.load(open(TFLAGS_P))
rep = {'fixed': [], 'hidden': [], 'review_candidate': [], 'review_no_candidate': [], 'tiles_fixed': []}
for k in list(FIX_MATS) + list(HIDE):
    assert k in M and k not in LOCKS['mats'], k
for k in list(REVIEW) + list(REVIEW_NONE):
    assert k in M and k in LOCKS['mats'], k
for k in FIX_TILES:
    assert k in T and k not in LOCKS['tiles'], k


def warp(path, pts, side):
    im = np.array(Image.open(path).convert('RGB'))[:, :, ::-1]
    mx = cv2.getPerspectiveTransform(np.float32(pts), np.float32([[0, 0], [side, 0], [side, side], [0, side]]))
    out = cv2.warpPerspective(im, mx, (side, side), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return Image.fromarray(out[:, :, ::-1])


def webp(im, q=86):
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q, method=6); return b.getvalue()


B = {}


def thumb(im):   # same as round 3
    t = im.copy(); t.thumbnail((150, 150)); b = io.BytesIO(); t.convert('RGB').save(b, 'JPEG', quality=70)
    v = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    k = 'mt' + hashlib.md5(v.encode()).hexdigest()[:8]
    B[k] = v; return k


def palette(im):   # same as round 3
    q = im.convert('RGB').resize((96, 96)).quantize(6, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette(); hist = q.histogram()[:6]; tot = sum(hist)
    sw = sorted(((hist[j] / tot, '#%02x%02x%02x' % tuple(pal[j * 3:j * 3 + 3])) for j in range(6) if hist[j]), reverse=True)[:5]
    return [[hx, round(s, 2)] for s, hx in sw]


# ---------- fixed mats -> new mc chunk(s)
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values())
N = (maxN // 12 + 1) * 12
CH = {}
for k, (fn, pts, side, note) in FIX_MATS.items():
    o = M[k]; im = warp(CLEAN_M + fn, pts, side); raw = webp(im)
    f = f'm/{N}.webp'; CH.setdefault(N // 12, []).append((f, raw)); N += 1
    old = o['f']
    o.update(f=f, th=thumb(im), w=im.width, h=im.height, ms=palette(im), src='clean-oct21')
    o.pop('hid', None)
    FLAGS[k] = {'name': o['n'], 'brand': o['bn'], 'flag': 'ok', 'photo': f, 'source': SRC[fn], 'original': 'assets/mats/clean/' + fn,
                'note': 'Oct 21 photo fix: ' + note}
    rep['fixed'].append([k, o['n'], o['bn'], old, f, note])
for c, items in CH.items():
    assert not os.path.exists(os.path.join(SITE, 'mc', f'{c}.webp')), c
    body, hdr = b'', {}
    for f, raw in items:
        hdr[f] = [len(body), len(raw)]; body += raw
    hj = json.dumps(hdr, separators=(',', ':')).encode()
    open(os.path.join(OUT, 'mc', f'{c}.webp'), 'wb').write(body + hj + struct.pack('<I', len(hj)))

# ---------- hidden
for k, why in HIDE.items():
    o = M[k]; o['hid'] = True
    FLAGS[k] = {'name': o['n'], 'brand': o['bn'], 'flag': 'no_flat_photo', 'note': 'Oct 21 QA: ' + why + '. Stays hidden until a flat photo exists.'}
    rep['hidden'].append([k, o['n'], o['bn'], why])

# ---------- locked: review only
os.makedirs(CLEAN_M + 'review_oct21', exist_ok=True)
review = {'_about': 'Locked FYM mats whose live photo breaks rule 6 (Oct 21 QA). Not changed: each needs Tiffany\'s OK. '
          'candidate = prepared flat photo (apply = new m/<n>.webp + thumb, then update locks.json f/th in the same commit); '
          'no candidate = recommend hid=true (locks.json hid) until the brand posts a flat photo.', 'items': {}}
for k, (fn, pts, side, note) in REVIEW.items():
    o = M[k]; im = warp(CLEAN_M + fn, pts, side)
    cand = 'assets/mats/clean/review_oct21/' + re.sub(r'[^a-z0-9]+', '-', o['n'].lower()).strip('-')[:50] + '.webp'
    open(REPO + cand, 'wb').write(webp(im))
    review['items'][k] = {'name': o['n'], 'brand': o['bn'], 'live_photo': o['f'], 'candidate': cand, 'original': 'assets/mats/clean/' + fn,
                          'source': SRC[fn], 'warp_corners': pts, 'note': note, 'recommend': 'swap to candidate'}
    FLAGS[k] = {'name': o['n'], 'brand': o['bn'], 'flag': 'locked_needs_approval', 'candidate': cand,
                'note': 'Oct 21 QA: live photo is a lifestyle/props shot; locked, flat candidate staged for Tiffany (review_locked.json)'}
    rep['review_candidate'].append([k, o['n'], o['bn'], cand])
for k, why in REVIEW_NONE.items():
    o = M[k]
    review['items'][k] = {'name': o['n'], 'brand': o['bn'], 'live_photo': o['f'], 'candidate': None, 'note': why, 'recommend': 'hide (no flat photo)'}
    FLAGS[k] = {'name': o['n'], 'brand': o['bn'], 'flag': 'locked_needs_approval', 'candidate': None,
                'note': 'Oct 21 QA: ' + why + '; locked, recommend hiding once Tiffany OKs (review_locked.json)'}
    rep['review_no_candidate'].append([k, o['n'], o['bn'], why])
json.dump(review, open(HERE + '/review_locked.json', 'w'), indent=1, ensure_ascii=False)

# ---------- tiles
os.makedirs(os.path.join(OUT, 't17'), exist_ok=True)
HDIX = json.load(open(os.path.join(SITE, 'hd', 'index.json')))
for key, (slug, fn, note) in FIX_TILES.items():
    t = T[key]; im = Image.open(CLEAN_T + fn); im = ImageOps.exif_transpose(im).convert('RGB')
    full = 't17/%s.jpg' % slug; a = im.copy(); a.thumbnail((1000, 1000), Image.LANCZOS)
    a.save(os.path.join(OUT, full), 'JPEG', quality=86, optimize=True)
    p = ImageOps.fit(im, (360, 360), Image.LANCZOS, centering=(.5, .5)); b = io.BytesIO(); p.save(b, 'JPEG', quality=84)
    pk = 'p17' + slug.replace('-', '')[:24]; B[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    old = t['full']; t['full'] = full; t['pile'] = pk; HDIX['t'][key] = 'file:' + full
    TFLAGS[slug] = {'name': t['n'], 'maker': t['bn'], 'flag': 'ok', 'photo': full, 'source': SRC[fn], 'original': 'assets/tiles/clean/' + fn,
                    'note': 'Oct 21 photo fix: ' + note}
    rep['tiles_fixed'].append([key, t['n'], old, full, note])
json.dump(HDIX, open(os.path.join(OUT, 'hd', 'index.json'), 'w'))

# ---------- write
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h)
assert max(int(x) for x in mcb.group(1).split(',')) < min(CH)
h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + ''.join(f', {c}' for c in sorted(CH)) + ']);', 1)
assert h.count('<script src="b15v1.js"></script>') == 1 and 'b17v1.js' not in h
h = h.replace('<script src="b15v1.js"></script>', '<script src="b15v1.js"></script><script src="b17v1.js"></script>', 1)
open(os.path.join(OUT, 'b17v1.js'), 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(B, separators=(',', ':')) + ');')
open(os.path.join(OUT, 'index.html'), 'w').write(h)
json.dump(FLAGS, open(FLAGS_P, 'w'), indent=1, ensure_ascii=False)
json.dump(TFLAGS, open(TFLAGS_P, 'w'), indent=1, ensure_ascii=False)
rep['new_chunks'] = sorted(CH)
json.dump(rep, open(HERE + '/photofix_report.json', 'w'), indent=1, ensure_ascii=False)
print('ok | fixed', len(rep['fixed']), '| hidden', len(rep['hidden']), '| locked review: candidate', len(rep['review_candidate']),
      'none', len(rep['review_no_candidate']), '| tiles fixed', len(rep['tiles_fixed']), '| chunks', sorted(CH))
