"""FYM 1.16: Mahj Pit racks (DESK 'FYM 1.15 leftovers: Mahj Pit racks (6b)'; Mahj Pit = partner since Nov 4, code MAHJMATCH).
Mahj Pit sells 6 rack listings (assets/launches/mahjpit-*rack*). Every brand photo is a lifestyle shot: racks lying at an angle on a
busy painted mat, overlapping each other and covered with tiles; no product shot on white or black exists. Rule 6b cut-out review
(Nov 6, white + navy):
  ADDED   White Beech Wood (19", $145): photo 04 is ONE rack alone on a plain magenta/purple ground. Cut by low saturation, the mask
          replaced by its convex hull (straight clean edges, no jagged fringe), rotated level, defringed toward the rack's own
          off-white, the dark notch at the far end trimmed -> assets/racks/v116/mahj-pit-white-beech-wood.png. Looked at on white +
          navy (racks116 sheet), approved with builder/fym_rack_images.py --approve.
  LEFT OUT (cannot be cut cleanly; need a clean product shot from Mahj Pit):
          Blonde Tortoise Pusher House + Tag-A-Long (translucent tortoise over a busy mat / blurred close-ups, racks overlap),
          Double Trouble Tortoise Siamese (translucent, tiles + other racks on top), Rainbow Acrylic Wave (clear acrylic, see-through
          to the mat), Solid Scallop Acrylic (clear body + coloured scallop, several racks stacked over a busy mat).
Idempotent. Usage: python3 racks116.py <build dir>"""
import sys, os, io, json, base64
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
R = D['racks']; REF = '12703261.srer4OxWkeRwwDVs'; DC = 'https://www.mahjmatchmaker.com/mahj-pit-discount-code'
LEFT_OUT = ['blonde-tortoise-pusher-house-racks-set-of-4-copy', 'blonde-tortoise-pusher-tag-a-long-racks-set-of-4',
            'double-trouble-tortoise-siamese-racks', 'rainbow-acrylic-wave-racks-with-pushers-17-5-inch-stackable',
            'solid-scallop-acrylic-racks-pushers-18-inches']
hd = 'white-beech-wood-mahjong-racks-with-magnetic-pushers-custom-storage-bag-1'; key = f'mahjpit.co/{hd}'; IMG = {}
if key not in R:
    im = Image.open(REPO + 'assets/racks/v116/mahj-pit-white-beech-wood.png').convert('RGBA'); im.thumbnail((700, 700))
    b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6); th = 'rk116mpwhitebeech'
    IMG[th] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    R[key] = dict(n='Mahj Pit White Beech Wood', bn='Mahj Pit', b='mahjpit.co',
                  u=f'https://mahjpit.co/discount/MAHJMATCH?redirect=%2Fproducts%2F{hd}%3Fsca_ref%3D{REF}',
                  u0=f'https://mahjpit.co/products/{hd}?sca_ref={REF}', dc=DC, pa=True, nc=False, rt=False, c=True, ml=False, sk=False,
                  hx='#f1e8dc', rf=['neutral'], rs={'neutral': 1.9}, pq=4, wh=1, len=19.0, im=th, add='nov06-v116')
    TV = D['tv']  # rack type (gate [151], one type: Painted) + White colour dot; no price row (Mahj Pit has no price data in FYM yet)
    TV['rt'][key] = 'painted'; TV['fin'][key] = ['painted']
    if key not in TV['rw']: TV['rw'].append(key)
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'
    assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
    open(P, 'w').write(h)
RT = REPO + 'config/rack-types-nov03.json'; RTC = json.load(open(RT))  # gate [151]: exactly one type; painted white wood
if key not in RTC['racks']:
    RTC['racks'][key] = {'n': 'Mahj Pit White Beech Wood', 'type': 'painted', 'by_eye': True}
    if key not in RTC['white']: RTC['white'].append(key)
    json.dump(RTC, open(RT, 'w'), indent=1, ensure_ascii=False)
STP = REPO + 'config/fym-stock.json'; ST = json.load(open(STP))
ST['items'][f'r:{key}'] = {'in': True, 'how': 'v116 add (mahjpit.co products.json Nov 6)', 'price': 145.0}
json.dump(ST, open(STP, 'w'), indent=0, ensure_ascii=False)
print('racks116: Mahj Pit White Beech Wood', 'added' if IMG else 'already in', '| left out (no clean cut):', len(LEFT_OUT))
