"""FYM: Tiffany's photo calls on the 8 un-hidden mats (Oct 21, 8:03am). STAGED ONLY; the main session publishes.
Usage: python3 builder/fym_fix_oct21/photocalls.py <staged_build_dir> <brand_img_dir>
  staged_build_dir: copy of the live build (fym-oct21c, copied from fym-oct21b = published v66); edited in place
  brand_img_dir   : brand images downloaded with curl from /products/<handle>.json (all images, checked by eye on contact sheets)
Her calls:
  HIDE  Green Malachite (too far away)  -> re-checked all 7 Mahj Squad images: image 2/7 is a close, whole-mat view with no racks,
        colours clear -> photo swapped in, stays visible (her rule: use a better photo instead of hiding). Not locked (unapproved).
  HIDE  Pastel Chinoiserie (covered)    -> all 8 images re-checked: only 2/8 has nothing on it, but it is a corner close-up
        (rule 6: out). Hidden + locked hid; the 2/8 crop is staged on the Questionable list as an alternate she can approve.
  HIDE  Hip Hip Celebration (too little mat showing, judgment call) -> hidden + locked hid + Questionable list.
  KEEP  Regency, Jade Green Chinoiserie, El Ultimo Refresco, Vegan Leather Premium (solid: lower bar), Paige Spearin Apres Mahj.
  El Ultimo Refresco: the Miss Mahjong entry is the SAME mat as the locked TdT x Miss Mahjong entry (same art, both $175, both
        in stock). TdT image 1/12 (whole mat top-down, colours clear) is already the locked TdT entry's photo; it is clearly better
        than all 4 Miss Mahjong images (tilted close-ups), so it goes on the Miss Mahjong entry too, and that entry is hidden as a
        duplicate (one card per mat; the locked TdT entry stays). Questionable list asks her which store link to keep.
"""
import sys, os, io, json, re, base64, hashlib, struct
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
OUT, IMG = sys.argv[1], sys.argv[2]
FL = REPO + 'builder/fym_flags/'
CLEAN_M = REPO + 'assets/mats/clean/'
TODAY = '2026-10-21'

GM = 'mahjsquadshop.com/green-malachite-mahjong-mat-emerald-green-and-jewel-neoprene-mahjongg-mat-jewel-tone-mahj-mat-malachite-stone-mahj-ongg-mat-1'
PC = 'mahjsquadshop.com/blue-chinoiserie-mahjong-mat-copy'
HH = 'www.hiphipmahjong.com/celebration-mahjong-mat'
MM = 'missmahjong.com/el-ultimo-refresco-mahjong-playing-mat'
TDT = 'tigredetartan.com/tigre-de-tartan-x-miss-mahjong-el-ultimo-refresco-mahjong-mat'
KEEP = {
    'mahjsquadshop.com/regency-mahjong-mat': 'KEPT by Tiffany Oct 21 8:03am (props photo OK for FYM).',
    'mahjsquadshop.com/jade-green-chinoiserie-mahjong-mat': 'KEPT by Tiffany Oct 21 8:03am (props photo OK for FYM).',
    'sundaymahjong.com/vegan-leather-premium-mahjong-mat': 'KEPT by Tiffany Oct 21 8:03am. Solid / vegan leather mat: lower bar (uniform colour shows even in an angled shot).',
    'tigredetartan.com/paige-spearin-mahjong-mat-apres-mahj': 'KEPT by Tiffany Oct 21 8:03am. Paige Spearin x TdT collab: NO commission (TdT excluded them); stays in the library, do not promote. Already holiday-tagged before Oct 21 (ski scene); not moved.',
    TDT: 'El Ultimo Refresco KEPT by Tiffany Oct 21 8:03am; this locked TdT entry (photo = TdT image 1/12, whole mat) is the one card for the mat.',
}

h = open(os.path.join(OUT, 'index.html')).read()
i = h.find('const D=') + 8
D, end = json.JSONDecoder().raw_decode(h, i)
M = D['mats']
LOCKS = json.load(open(FL + 'locks.json'))
FLAGS = json.load(open(FL + 'mat_photo_flags.json'))
SRC = json.load(open(CLEAN_M + 'oct21_sources.json'))
for k in (GM, PC, HH, MM):
    assert k in M and k not in LOCKS['mats'], k
assert TDT in LOCKS['mats'] and M[TDT]['f'] == 'm/1851.webp'
JS = {os.path.basename(f)[:-5]: json.load(open(os.path.join(IMG, '..', 'json', f)))['product']
      for f in os.listdir(os.path.join(IMG, '..', 'json'))}


def src_of(prefix, n):
    tag = [t for t in JS if t.startswith(prefix)][0]; p = JS[tag]
    dom = tag.split('_')[0]
    return {'url': p['images'][n - 1]['src'], 'product_json': f"https://{dom}/products/{p['handle']}.json", 'title': p['title'],
            'image_index': n, 'fetched': TODAY}


def webp(im, q=86):
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q, method=6); return b.getvalue()


B = {}


def thumb(im):   # same as photofix.py / round 3
    t = im.copy(); t.thumbnail((150, 150)); b = io.BytesIO(); t.convert('RGB').save(b, 'JPEG', quality=70)
    v = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    k = 'mt' + hashlib.md5(v.encode()).hexdigest()[:8]; B[k] = v; return k


def palette(im):
    q = im.convert('RGB').resize((96, 96)).quantize(6, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette(); hist = q.histogram()[:6]; tot = sum(hist)
    sw = sorted(((hist[j] / tot, '#%02x%02x%02x' % tuple(pal[j * 3:j * 3 + 3])) for j in range(6) if hist[j]), reverse=True)[:5]
    return [[hx, round(s, 2)] for s, hx in sw]


rep = {'photo_swapped': [], 'hidden': [], 'kept': [], 'questionable': []}

# ---- Green Malachite: brand image 2/7 (close, whole mat, no racks) -> new chunk
fn = 'green-malachite-mahj-squad-2.jpg'
orig = Image.open(os.path.join(IMG, 'mahjsquadshop.com_green-malach_02.jpg')).convert('RGB')
orig.save(CLEAN_M + fn, quality=92); SRC[fn] = src_of('mahjsquadshop.com_green-malach', 2)
im = orig.crop((0, 60, 1000, 640))   # mat edge to edge (bottom corners run just off the brand frame), a sliver of table
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values())
N = (maxN // 12 + 1) * 12; C = N // 12
assert not os.path.exists(os.path.join(OUT, 'mc', f'{C}.webp'))
f = f'm/{N}.webp'; raw = webp(im)
hj = json.dumps({f: [0, len(raw)]}, separators=(',', ':')).encode()
open(os.path.join(OUT, 'mc', f'{C}.webp'), 'wb').write(raw + hj + struct.pack('<I', len(hj)))
o = M[GM]; old = o['f']
o.update(f=f, th=thumb(im), w=im.width, h=im.height, ms=palette(im), src='clean-oct21')
o['hid'] = None
FLAGS[GM] = {'name': o['n'], 'brand': o['bn'], 'flag': 'ok', 'photo': f, 'source': SRC[fn], 'original': 'assets/mats/clean/' + fn,
             'was': 'ok_fym_props', 'note': 'Oct 21 8:03am: Tiffany said HIDE (old photo shot from too far away) unless a closer brand photo exists. '
             'Brand image 2/7 shows the whole mat up close, no racks, colours clear -> swapped in instead of hiding. Not locked until she OKs it.'}
rep['photo_swapped'].append([GM, o['n'], o['bn'], old, f, 'assets/mats/clean/' + fn])

# ---- Miss Mahjong El Ultimo Refresco: same mat as the locked TdT entry -> better photo + hidden duplicate
o = M[MM]; t = M[TDT]; old = o['f']
o.update(f=t['f'], th=t['th'], w=t['w'], h=t['h'], ms=t.get('ms'), hid=True)
FLAGS[MM] = {'name': o['n'], 'brand': o['bn'], 'flag': 'duplicate', 'photo': t['f'], 'source': src_of('tigredetartan.com_tigre-de-tar', 1),
             'was': 'ok_fym_props',
             'note': 'Oct 21: same mat as the locked TdT x Miss Mahjong "El Ultimo Refresco" entry (' + TDT + '). Both stores list it '
             '($175, in stock). All 4 Miss Mahjong images are tilted close-ups with tiles; TdT image 1/12 (whole mat, top-down, colours clear) '
             'is clearly better and now on both entries. This entry is hidden as the duplicate; Tiffany picks which store link to keep '
             '(fym_questionable.json). Note: the TdT listing says "Not eligible for promotions".'}
rep['photo_swapped'].append([MM, o['n'], o['bn'], old, t['f'], 'TdT image 1/12 (already the locked TdT entry photo)'])
rep['hidden'].append([MM, o['n'], o['bn'], 'duplicate'])

# ---- Pastel Chinoiserie: hidden (covered); alternate corner shot staged
os.makedirs(CLEAN_M + 'review_oct21', exist_ok=True)
fn = 'pastel-chinoiserie-mahj-squad-2.jpg'
orig = Image.open(os.path.join(IMG, 'mahjsquadshop.com_blue-chinois_02.jpg')).convert('RGB')
orig.save(CLEAN_M + fn, quality=92); SRC[fn] = src_of('mahjsquadshop.com_blue-chinois', 2)
alt = 'assets/mats/clean/review_oct21/pastel-chinoiserie-alt-corner.webp'
open(REPO + alt, 'wb').write(webp(orig))
HIDE = {
    PC: ('covered', 'Oct 21 8:03am Tiffany: HIDE, pattern hard to see, tiles and racks cover it. Re-checked all 8 Mahj Squad images: '
         '7 have racks/tiles on the mat; 2/8 has nothing on it but is a corner close-up (rule 6: out). Staged as an alternate on the '
         'Questionable list: ' + alt, alt),
    HH: ('questionable', 'Oct 21 8:03am Tiffany: too little mat showing (racks, tiles, gold tray and props cover most of it). Judgment call: '
         'pulled and listed on the Questionable list. Only 1 brand image exists.', None),
}
for k, (flag, note, cand) in HIDE.items():
    o = M[k]; o['hid'] = True
    FLAGS[k] = {'name': o['n'], 'brand': o['bn'], 'flag': flag, 'was': 'ok_fym_props', 'note': note}
    if cand: FLAGS[k]['candidate'] = cand
    LOCKS['mats'][k] = {'n': o['n'], 'bn': o['bn'], 'f': o['f'], 'th': o['th'], 'rt': o.get('rt', False), 'hid': True,
                        'mf': o.get('mf'), 'mt': o.get('mt')}
    rep['hidden'].append([k, o['n'], o['bn'], flag])

for k, note in KEEP.items():
    FLAGS[k]['note'] = note + ' ' + FLAGS[k].get('note', '')
    rep['kept'].append([k, M[k]['n'], M[k]['bn']])

# ---- Questionable for FYM list
QP = FL + 'fym_questionable.json'
Q = json.load(open(QP)) if os.path.exists(QP) else {
    '_about': "Tiffany's 'Questionable for FYM' review list (CLAUDE.md rule 6: when in doubt, PULL IT). Every item here stays hidden in FYM "
              "(gate [3d]) until Tiffany says keep (then drop it from this list and un-hide; update locks.json in the same commit). "
              "Fields: key (FYM mat id), img (FYM photo), name, brand, reason, photo (repo path or FYM path to look at), candidate (alternate photo, if any).",
    'items': []}
have = {x['key'] for x in Q['items']}
def q(k, reason, photo, cand=None):
    if k in have: return
    o = M[k]; it = {'key': k, 'img': o['f'], 'name': o['n'], 'brand': o['bn'], 'reason': reason, 'photo': photo, 'added': TODAY}
    if cand: it['candidate'] = cand
    Q['items'].append(it); rep['questionable'].append([k, o['n'], o['bn']])
q(HH, 'Too little mat showing (her call Oct 21: judgment call). Only 1 brand image exists.', 'FYM ' + M[HH]['f'])
q(PC, 'You said hide (tiles and racks cover the pattern). The only clear brand image (2/8) is a corner close-up: say yes to use it.',
  'FYM ' + M[PC]['f'], alt)
q(MM, 'Duplicate: same mat as Tigre de Tartan x Miss Mahjong "El Ultimo Refresco" (kept, locked). Which store link do you want on the card? '
      'Miss Mahjong has your ref link; the TdT listing says "Not eligible for promotions".', 'FYM ' + M[MM]['f'])
json.dump(Q, open(QP, 'w'), indent=1, ensure_ascii=False)

# ---- write
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h)
assert max(int(x) for x in mcb.group(1).split(',')) < C
h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + f', {C}]);', 1)
assert h.count('<script src="b17v1.js"></script>') == 1 and 'b18v1.js' not in h
h = h.replace('<script src="b17v1.js"></script>', '<script src="b17v1.js"></script><script src="b18v1.js"></script>', 1)
open(os.path.join(OUT, 'b18v1.js'), 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(B, separators=(',', ':')) + ');')
open(os.path.join(OUT, 'index.html'), 'w').write(h)
json.dump(FLAGS, open(FL + 'mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
json.dump(LOCKS, open(FL + 'locks.json', 'w'), indent=1, ensure_ascii=False)
json.dump(SRC, open(CLEAN_M + 'oct21_sources.json', 'w'), indent=1, ensure_ascii=False)
rep['new_chunk'] = C
json.dump(rep, open(HERE + '/photocalls_report.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(rep, ensure_ascii=False, indent=1))
