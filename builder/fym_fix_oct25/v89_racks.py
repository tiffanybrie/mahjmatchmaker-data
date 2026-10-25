"""FYM v89 rack fixes (Tiffany Oct 25 16:36-16:38):
1. Peace Love Mahjong Chartreuse racks looked highlighter-neon ("Their rack is a lime green ... way too bright"). Both Chartreuse
   cutouts (straight plm:Chartreuse, wavy) are recoloured so their median colour matches PLM's own variant photo
   (chartreuse1, median ~ rgb(194,217,106)); hx updated. The straight one's HD copy is dropped so the card uses the corrected image.
2. Tigre de Tartan Clear Acrylic Logo: clear acrylic on a busy blue print, you can barely see the racks, and all 8 brand photos are
   the same kind of shot. Pulled (hid) and put on the 'Questionable / needs a better photo' list (fym_questionable.json, kind rack).
Usage: python3 v89_racks.py <build_dir>"""
import sys, os, io, re, json, base64, glob
import numpy as np
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
R = D['racks']; TARGET = np.array([194, 217, 106], float)
def find_img(key):
    for fn in sorted(glob.glob(B + '/b*.js')) + [P]:
        m = re.search(r'"%s"\s*:\s*"(data:image/\w+;base64,[^"]+)"' % key, open(fn, errors='ignore').read())
        if m: return m.group(1)
def recolor(data_url):
    im = Image.open(io.BytesIO(base64.b64decode(data_url.split(',', 1)[1]))).convert('RGBA'); a = np.asarray(im).astype(float)
    rgb = a[..., :3]; m = (a[..., 3] > 200) & (rgb.min(-1) < 235) & (rgb[..., 1] > rgb[..., 2] + 40)
    gain = TARGET / np.median(rgb[m], 0)
    body = (a[..., 3] > 0) & (rgb[..., 1] > rgb[..., 2] + 20)   # the green body only (holes/magnets/edges keep their colour)
    rgb[body] = np.clip(rgb[body] * gain, 0, 255); a[..., :3] = rgb
    out = Image.fromarray(a.astype(np.uint8), 'RGBA'); b = io.BytesIO(); out.save(b, 'WEBP', quality=90, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode(), gain
IMG = {}
# straight: our old cutout had a neon glow that recolouring can't remove -> PLM's own Chartreuse variant photo, background removed
r = R['plm:Chartreuse']; nk = r['im'] + 'v89'
IMG[nk] = 'data:image/webp;base64,' + base64.b64encode(open(REPO + 'assets/racks/v89/plm-chartreuse-straight.webp', 'rb').read()).decode()
r['im'] = nk; r['hx'] = '#c2d96a'; print('replaced', r['n'], 'with the brand variant photo')
# wavy: same photo as the brand's, nudged to the same lime
r = R['peacelovemahjong.com/wavy-mahjong-rack-pusher-set-chartrusse']; nk = r['im'] + 'v89'; IMG[nk], g = recolor(find_img(r['im'])); r['im'] = nk; r['hx'] = '#c2d96a'
print('recoloured', r['n'], 'gain', np.round(g, 2))
hd = json.load(open(B + '/hd/index.json')); hd['r'].pop('plm:Chartreuse', None); json.dump(hd, open(B + '/hd/index.json', 'w'), separators=(',', ':'))
TK = 'tigredetartan.com/clear-acrylic-logo-straight-mahjong-racks-with-pushers-custom-storage-bag'
R[TK]['hid'] = 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
qp = REPO + 'builder/fym_flags/fym_questionable.json'; q = json.load(open(qp))
if not any(it.get('key') == TK for it in q['items']):
    q['items'].append({'key': TK, 'kind': 'rack', 'name': 'Clear Acrylic Logo racks', 'brand': 'Tigre de Tartan',
        'reason': "Needs a better photo: clear acrylic on a busy blue print, you can barely see the racks (Tiffany Oct 25). All 8 brand photos are the same kind of shot; ask TdT for a clean one.",
        'photo': 'FYM rack image b1709f1590', 'added': '2026-10-25'})
    json.dump(q, open(qp, 'w'), indent=1, ensure_ascii=False)
print('TdT clear acrylic hidden + on the questionable list')
