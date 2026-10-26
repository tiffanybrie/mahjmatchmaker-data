"""FYM v92: rack cutouts with white halos / white background left inside (found on the Oct 25 night audit by
compositing every rack cutout on navy; on the mood board they sit on the mat). Config config/rack-defringe-oct25.json:
key -> repaired image made by builder/fym_defringe.py ('defringe'), or, where a white/clear product can't be cut
cleanly, the brand's photo flattened on white ('flat-white', Tiffany's Oct 23 rule). Usage: v92_rackdefringe.py <build>"""
import sys, os, json, base64
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
cfg = json.load(open(REPO + 'config/rack-defringe-oct25.json')); IMG = {}
for k, v in cfg.items():
    r = D['racks'].get(k)
    if not r: print('missing', k); continue
    nk = r['im'] + 'v92d'; IMG[nk] = 'data:image/webp;base64,' + base64.b64encode(open(REPO + v['path'], 'rb').read()).decode(); r['im'] = nk
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h); print('repaired', len(IMG), 'rack cutouts')
