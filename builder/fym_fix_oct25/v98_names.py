"""FYM v98 (Version 1.2): mat name clean-up + visible brand logos (config/fym-names-logos-v98.json). Peppi name without the
leading quote; Wren Mats logo badge = tight bolder wordmark (thumbnail inline IMG['lg98<brand>'] + HD file r98/<file>.webp).
Idempotent. Gate [96]. Usage: v98_names.py <build>"""
import sys, os, io, json, base64
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
C = json.load(open(REPO + 'config/fym-names-logos-v98.json')); n = 0; IMG = {}
for k, nm in C['mat_names'].items():
    if k in D['mats'] and D['mats'][k]['n'] != nm: D['mats'][k]['n'] = nm; n += 1
hd = json.load(open(B + '/hd/index.json')); os.makedirs(B + '/r98', exist_ok=True)
for brand, src in C['logos'].items():
    key = 'lg98' + ''.join(ch for ch in brand.lower() if ch.isalnum())
    if D['logos'].get(brand) == key: continue
    im = Image.open(REPO + src).convert('RGBA'); base = os.path.splitext(os.path.basename(src))[0]
    im.save(f'{B}/r98/{base}.webp', 'WEBP', quality=92, method=6)
    t = im.copy(); t.thumbnail((240, 240), Image.LANCZOS); b = io.BytesIO(); t.save(b, 'WEBP', quality=88, method=6)
    IMG[key] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode(); D['logos'][brand] = key; hd['l'][brand] = f'file:r98/{base}.webp'; n += 1
json.dump(hd, open(B + '/hd/index.json', 'w'), separators=(',', ':'))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a_ = '<script src="b24v1.js"></script>'; assert h.count(a_) == 1; h = h.replace(a_, a_ + inl, 1)
open(P, 'w').write(h); print('v98 names/logos', n)
