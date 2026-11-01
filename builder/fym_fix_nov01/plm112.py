"""v112: PLM Chartreuse racks -> Tiffany's approved shade "A" (186,212,96) (Oct 26 8:53pm, ANSWERS line 462).
b111 still showed the neon (200,238,80) on BOTH plm:Chartreuse and the wavy chartreuse rack.
New recoloured cut-outs (looked at on white + navy, sheets beside them in assets/racks/v112/):
  plm:Chartreuse  <- assets/racks/v112/plm-chartreuse-A.png      (im rk98plmchartreuseA = gate [94] locked name)
  wavy chartreuse <- assets/racks/v112/plm-wavy-chartreuse-A.webp (im rk112plmwavychartreuseA)
Thumbs (360px webp) go into window.IMG in b24v1.js; HD (900px webp) goes inline into hd/index.json as 'file:data:...'
(no new files: the claude.ai artifact is at its 512-file limit). Copy-on-write (build dirs are hardlinked).
Usage: python3 plm112.py <build dir>"""
import sys, os, io, json, re, base64
from PIL import Image
B = sys.argv[1]; R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
WAVY = 'peacelovemahjong.com/wavy-mahjong-rack-pusher-set-chartrusse'
SPEC = {'plm:Chartreuse': ('assets/racks/v112/plm-chartreuse-A.png', 'rk98plmchartreuseA'),
        WAVY: ('assets/racks/v112/plm-wavy-chartreuse-A.webp', 'rk112plmwavychartreuseA')}
def webp(p, w):
    im = Image.open(os.path.join(R, p)).convert('RGBA'); im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=88, method=6); return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
def cow_write(p, s):
    os.remove(p); open(p, 'w').write(s)
h = open(B + '/index.html').read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
th = {}
for k, (src, im) in SPEC.items():
    r = D['racks'][k]; r['im'] = im; r['hx'] = '#bad460'; th[im] = webp(src, 360)
cow_write(B + '/index.html', h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:])
b24 = open(B + '/b24v1.js').read(); a = 'window.IMG=Object.assign(window.IMG||{},{'; assert b24.startswith(a)
b24 = a + ','.join(json.dumps(k) + ':' + json.dumps(v) for k, v in th.items()) + ',' + b24[len(a):]
cow_write(B + '/b24v1.js', b24)
hd = json.load(open(B + '/hd/index.json'))
for k, (src, im) in SPEC.items(): hd['r'][k] = 'file:' + webp(src, 900)
cow_write(B + '/hd/index.json', json.dumps(hd, separators=(',', ':')))
# gate [94] reference: the locked straight rack + the wavy rack both measure against shade A
cp = os.path.join(R, 'config/fym-rack-split-oct26.json'); c = json.load(open(cp))
c['plm_ref']['plm:Chartreuse'] = [186, 212, 96]; c['plm_ref'][WAVY] = [186, 212, 96]
c['replace']['plm:Chartreuse']['img'] = SPEC['plm:Chartreuse'][0]
if 'Nov 1 (v112)' not in c['replace']['plm:Chartreuse']['why']: c['replace']['plm:Chartreuse']['why'] += " | Nov 1 (v112): Tiffany's Oct 26 8:53pm pick 'Chartreuse A is right (186,212,96)' applied to both PLM chartreuse racks (b111 still showed 200,238,80); gate [94] holds the median within 12 of A."
json.dump(c, open(cp, 'w'), indent=1, ensure_ascii=False)
print('plm112: b24v1.js', os.path.getsize(B + '/b24v1.js'), 'hd/index.json', os.path.getsize(B + '/hd/index.json'))
