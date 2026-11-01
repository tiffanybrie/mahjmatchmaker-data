"""v113 QA round 2 (Nov 1): Let's Be Besties mats that were ALREADY in FYM (Oct 16 add):
 - Sky Blue Florals: the FYM photo was a 602x296 strip -> the brand's flat render (assets/mats/v113/lbb/sky-blue-florals-mahjong-mat.jpg),
   new chunk, colours kept.
 - Tobacco Leaves Blue, Paint Feathers, Tobacco Leaves (leatherette; gone from the LBB store): only angled floor shots, no flat brand
   image -> HIDDEN + Questionable list (when in doubt, pull it).
Idempotent. Usage: python3 photos113.py <build_dir>"""
import sys, os, io, json, base64, hashlib, re, struct
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i; M = D['mats']
SB = 'letsbebesties.com/sky-blue-florals-mahjong-mat'
HIDE = {'letsbebesties.com/tobacco-leaves-blue-neoprene-mahjong-mat': 'angled floor shot, no flat brand image (QA round 2 Nov 1)',
        'letsbebesties.com/paint-feathers-neoprene-mahjong-mat': 'angled floor shot; the only other image is a close-up crop (QA round 2 Nov 1)',
        'letsbebesties.com/leatherette-tobacco-leaves': 'angled floor shot; product no longer in the LBB store (QA round 2 Nov 1)'}
for k in HIDE: M[k]['hid'] = True
o = M[SB]; inl = ''
if not o.get('p113'):
    mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); chunk = max(int(v) for v in mcb.group(1).split(',')) + 1
    maxN = max(int(x['f'].split('/')[1].split('.')[0]) for x in M.values() if str(x.get('f', '')).startswith('m/'))
    chunk = max(chunk, maxN // 12 + 1); f = f'm/{chunk * 12}.webp'
    im = Image.open(REPO + 'assets/mats/v113/lbb/sky-blue-florals-mahjong-mat.jpg').convert('RGB'); im.thumbnail((640, 640))
    b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6); raw = b.getvalue()
    hj = json.dumps({f: [0, len(raw)]}, separators=(',', ':')).encode(); p_ = f'{B}/mc/{chunk}.webp'
    if os.path.exists(p_): os.remove(p_)
    open(p_, 'wb').write(raw + hj + struct.pack('<I', len(hj)))
    t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'JPEG', quality=72)
    th = 'm113' + hashlib.md5(SB.encode()).hexdigest()[:8]
    o.update(f=f, th=th, w=im.width, h=im.height, p113=1)
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps({th: 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()}, separators=(',', ':')) + ');</script>'
    h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + f', {chunk}]);', 1)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if inl:
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
FL = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json')); Q = json.load(open(REPO + 'builder/fym_flags/fym_questionable.json'))
LK = json.load(open(REPO + 'builder/fym_flags/locks.json')); qk = {it['key'] for it in Q['items']}
for k, why in HIDE.items():
    FL[k] = {'name': M[k]['n'], 'brand': M[k]['bn'], 'flag': 'questionable', 'note': why}
    if k not in qk: Q['items'].append({'key': k, 'img': M[k]['f'], 'name': M[k]['n'], 'brand': M[k]['bn'], 'reason': why, 'added': '2026-11-01'})
    LK['mats'].setdefault(k, {})['hid'] = True
FL[SB] = {'name': o['n'], 'brand': o['bn'], 'flag': 'ok', 'note': "QA round 2 Nov 1: the FYM photo was a 602x296 strip; replaced by the brand's flat render"}
LK['mats'].setdefault(SB, {}).update(f=o['f'], th=o['th'])
for fp, d in (('mat_photo_flags.json', FL), ('fym_questionable.json', Q), ('locks.json', LK)):
    json.dump(d, open(REPO + 'builder/fym_flags/' + fp, 'w'), indent=1, ensure_ascii=False)
print('photos113: Sky Blue Florals', o['f'], '| hidden', list(HIDE))
