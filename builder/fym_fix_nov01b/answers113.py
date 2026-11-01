"""v113: Tiffany Nov 1 3:27pm answers (docs/ANSWERS.md):
 (1) TdT Estate Sale -> works_for_holiday (wfh): stays year-round in its colour sections, also offered for holiday tile sets
     (late-calls works_for_holiday.fym_keys + FYM flag wfh).
 (2) Mahj & Moon Festive Citrus Chinoiserie stays Holiday (no change; checked: hol).
 (3) Holy Mahj stays hidden until she sends the full image.
 (4) TdT Queen Bee (retired) VISIBLE on the corner crop we have (her call, overrides the photo bar): replaces the 'Photo coming soon'
     placeholder; tvc=1 = Table view shows it Corner-only (no full top-down photo). Off the placeholder/no_mat flag.
Image -> new chunk mc/<n>.webp (never written through a hardlink), thumb inline. Idempotent. Usage: python3 answers113.py <build_dir>"""
import sys, os, io, json, base64, hashlib, re, struct
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i; M = D['mats']
QB, ES, FC = 'alb2:tigre-de-tartan-queen-bee', 'tigredetartan.com/mahjong-mat-estate-sale', 'mahjandmoon.com/festive-chinoiserie-mahjong-mat'
assert M[FC].get('hol'), 'Festive Citrus Chinoiserie should be holiday'
assert M['alb2:tigre-de-tartan-holy-mahj'].get('hid'), 'Holy Mahj must stay hidden'
M[ES]['wfh'] = True
o = M[QB]; IMGK = None
if not o.get('tvc'):
    mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); chunk = max(int(v) for v in mcb.group(1).split(',')) + 1
    maxN = max(int(x['f'].split('/')[1].split('.')[0]) for x in M.values() if str(x.get('f', '')).startswith('m/'))
    chunk = max(chunk, maxN // 12 + 1); f = f'm/{chunk * 12}.webp'
    im = Image.open(REPO + 'assets/mats/gallery-retired-new/tigre-de-tartan--queen-bee.jpg').convert('RGB'); im.thumbnail((640, 640))
    b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6); raw = b.getvalue()
    hj = json.dumps({f: [0, len(raw)]}, separators=(',', ':')).encode(); p_ = f'{B}/mc/{chunk}.webp'
    if os.path.exists(p_): os.remove(p_)
    open(p_, 'wb').write(raw + hj + struct.pack('<I', len(hj)))
    t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'JPEG', quality=72)
    th = 'm113' + hashlib.md5(QB.encode()).hexdigest()[:8]; IMGK = (th, 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode())
    o.update(f=f, th=th, w=im.width, h=im.height, tvc=1); o.pop('hid', None)
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
    h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + f', {chunk}]);', 1)
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps({IMGK[0]: IMGK[1]}, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
else:
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
open(P, 'w').write(h)
# repo records
FL = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
FL[QB] = {'name': 'Queen Bee (retired)', 'brand': 'Tigre de Tartan', 'flag': 'ok', 'note': "Tiffany Nov 1 3:27pm: no full view exists; show the corner crop we have (her call, overrides the photo bar). Table view: Corner only (tvc)."}
json.dump(FL, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
LK = json.load(open(REPO + 'builder/fym_flags/locks.json'))
LK['mats'][QB].update(hid=False, f=o['f'], th=o['th'])
json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
LC = REPO + 'config/tiffany-color-notes/2026-10-20-late-calls.json'; lc = json.load(open(LC)); w = lc['works_for_holiday']
if ES not in w.setdefault('fym_keys', []): w['fym_keys'].append(ES); w.setdefault('names', {})[ES] = "TdT Estate Sale (Tiffany Nov 1 3:27pm)"
json.dump(lc, open(LC, 'w'), indent=1, ensure_ascii=False)
print('answers113: Estate Sale wfh; Queen Bee visible', o['f'], o['th'], 'tvc', o.get('tvc'))
