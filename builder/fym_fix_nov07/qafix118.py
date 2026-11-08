"""FYM 1.18 independent-QA fixes in the BUILD (Nov 8, docs/reports/fym/qa-v118-2026-11-08.md F1/F3). Runs in build118.sh after
albumlive118.py and before fym_apply_locks.py / tilerank_v118.py (so D.tso ranks the mat it makes visible). Idempotent.
 1. LBB Paint Feathers (Juniper's final 42, her yes Nov 7 11:21pm; Questionable since Nov 1 for an angled floor shot). Every Let's Be
    Besties product image was checked Nov 8 (letsbebesties.com/products/paint-feathers-neoprene-mahjong-mat.json: IMG-3212, IMG-3213,
    Paint_Feathers_33_small_file.png, IMG-3341). IMG-3212 is a straight-down shot of the WHOLE mat on the floor: perspective-corrected
    and cropped to the mat (rule 3b: room/floor shots get cropped to the mat), saved as assets/mats/qafix-nov08/lbb-paint-feathers-flat.jpg
    (whole mat, colours clear, no floor). The mat gets that photo (new packed chunk + inline thumb), re-measured swatches, mf green+pink
    (it visibly has both; old mf ['pink'] / sh [0] came from the floor shot), is made visible, leaves the Questionable list, the
    mat_photo_flags entry becomes ok, its locks 'hid' and its m_hidden_ok line go.
 2. YMI Outlaws of the Marsh Mahjong Treasure Set showed 'PHOTO COMING SOON': the SET is hidden (s.hid) and flagged no_tiles in
    builder/fym_flags/tile_photo_flags.json until a real photo exists (the tile stays selectable data, gate [28]).
 3. builder/fym_flags/watermark_flags.json lists photos with a brand watermark; gate [171] fails on a visible one unless accepted.
Usage: python3 builder/fym_fix_nov07/qafix118.py <build dir>"""
import sys, os, io, json, base64, re, struct, tempfile
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M = D['mats']
src = open(REPO + 'builder/fym_fix_oct25/v92_splash.py').read()
exec(src[src.index('def kmeans_sw'):src.index('tmpl = ')])
sys.path.insert(0, REPO + 'scripts/colors'); from families import read_image
PF = 'letsbebesties.com/paint-feathers-neoprene-mahjong-mat'
PF_IMG = 'assets/mats/qafix-nov08/lbb-paint-feathers-flat.jpg'
PF_TH = 'mq08pf'
YMI = 'yellow-mountain-imports-outlaws-of-the-marsh-mahjong-treasure-set'
log = []
# 1. Paint Feathers
o = M[PF]
if o.get('src') != 'qafix-nov08':
    im = Image.open(REPO + PF_IMG).convert('RGB'); im.thumbnail((640, 640)); b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6)
    mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); chunk = max(int(v) for v in mcb.group(1).split(',')) + 1
    maxN = max(int(x['f'].split('/')[1].split('.')[0]) for x in M.values() if str(x.get('f', '')).startswith('m/'))
    chunk = max(chunk, maxN // 12 + 1); f = f'm/{chunk * 12}.webp'
    raw = b.getvalue(); hj = json.dumps({f: [0, len(raw)]}, separators=(',', ':')).encode()
    open(f'{B}/mc/{chunk}.webp', 'wb').write(raw + hj + struct.pack('<I', len(hj)))
    h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + f', {chunk}]);', 1)
    t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'JPEG', quality=72)
    TH = {PF_TH: 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()}
    fw, tone, _ = read_image(REPO + PF_IMG)
    pink, green = round(100 * (fw.get('pink', 0) + fw.get('red', 0)), 1), round(100 * fw.get('green', 0), 1)
    o.update(f=f, th=PF_TH, w=im.width, h=im.height, ms=kmeans_sw(im), mf=['pink', 'green'], mt=[0, 1], sh=[pink, green], src='qafix-nov08')
    o.pop('hid', None)
    log.append(f'Paint Feathers: visible, photo {f} (chunk {chunk}) from {PF_IMG}, mf pink {pink} / green {green}')
    # the colour record the ranking reads (like partner_adds118)
    C = json.load(open(REPO + 'config/fym-colour-oct25.json'))
    C['mats'][PF] = {'sw': o['ms'], 'tone': tone}
    json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
    a = '<script src="b24v1.js"></script>'
    if h.count(a) != 1: a = re.search(r'<script src="b\d+v\d+\.js"></script>', h).group(0)
    h = h.replace(a, a + '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(TH, separators=(',', ':')) + ');</script>', 1)
    i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i; M = D['mats']
else:
    log.append('Paint Feathers: already done')
# repo records (idempotent)
QL = json.load(open(REPO + 'builder/fym_flags/fym_questionable.json'))
lst = QL['items'] if isinstance(QL, dict) and 'items' in QL else QL
keep = [x for x in lst if x.get('key') != PF]
if len(keep) != len(lst):
    if isinstance(QL, dict) and 'items' in QL: QL['items'] = keep
    else: QL = keep
    json.dump(QL, open(REPO + 'builder/fym_flags/fym_questionable.json', 'w'), indent=1, ensure_ascii=False); log.append('Paint Feathers: off the Questionable list')
FL = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
if FL.get(PF, {}).get('flag') != 'ok' or FL[PF].get('photo') != M[PF]['f']:
    FL[PF] = {'name': 'Paint Feathers', 'brand': "Let's Be Besties", 'flag': 'ok', 'photo': M[PF]['f'], 'src': PF_IMG,
              'note': ("Nov 8 (FYM 1.18 QA F1): brand photo IMG-3212 (straight-down shot of the whole mat) perspective-corrected + cropped to "
                       "the mat; whole mat, colours clear (LOOKED at). Was questionable (angled floor shot, Nov 1).")}
    json.dump(FL, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
LK = json.load(open(REPO + 'builder/fym_flags/locks.json'))
if LK['mats'].get(PF, {}).get('hid'):
    LK['mats'][PF].pop('hid')
    if not LK['mats'][PF]: LK['mats'].pop(PF)
    LK.setdefault('_changes', [])
    if isinstance(LK['_changes'], list):
        LK['_changes'].append(f"2026-11-08 FYM 1.18 QA F1: {PF} hid lock removed: clean photo found (brand IMG-3212 cropped to the mat, "
                              "builder/fym_fix_nov07/qafix118.py); Tiffany's Juniper final 42 (her yes Nov 7 11:21pm)")
    json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
HO = json.load(open(REPO + 'builder/fym_flags/m_hidden_ok.json'))
n0 = len(HO['allowed']); HO['allowed'] = [x for x in HO['allowed'] if not (x.get('set') == 'juniper' and x.get('key') == PF)]
if len(HO['allowed']) != n0: json.dump(HO, open(REPO + 'builder/fym_flags/m_hidden_ok.json', 'w'), indent=1, ensure_ascii=False)
# 2. YMI Outlaws of the Marsh: set hidden + no_tiles flag
TF = json.load(open(REPO + 'builder/fym_flags/tile_photo_flags.json'))
if TF.get(YMI, {}).get('flag') != 'no_tiles':
    TF[YMI] = {'name': 'Outlaws of the Marsh Mahjong Treasure Set', 'maker': 'Yellow Mountain Imports', 'flag': 'no_tiles', 'photo': 't15/177.jpg',
               'note': ("Nov 8 (FYM 1.18 QA F3): showed the 'PHOTO COMING SOON' placeholder; set stays hidden until a real photo exists. "
                        "Brand images checked Nov 8 (ymimports.com/products/hb-at002-a.json): a single-tile face/side/back shot and a full-set "
                        "layout strip.")}
    json.dump(TF, open(REPO + 'builder/fym_flags/tile_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
for s in D['sets']:
    if s['slug'] in TF and TF[s['slug']].get('flag') == 'no_tiles' and s['slug'] == YMI and not s.get('hid'):
        s['hid'] = True; log.append(f"{s['name']}: set hidden (no_tiles)")
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
open(P, 'w').write(h)
for l in log: print('qafix118:', l)
