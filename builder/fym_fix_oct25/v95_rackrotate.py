"""FYM v95: vertical rack photos lie horizontal (Tiffany Oct 26 10:46am: portrait rack photos mock up tiny and in the
wrong proportions on the match card). config/fym-rack-rotate-oct26.json: rack key -> rotated real photo (rotate 90 +
trim; a few with a white-point lift or background lifted to white). The new image is the card image; HD copies dropped.
Idempotent (new IMG key = old + 'r95'). Gate [70]. Usage: v95_rackrotate.py <build>"""
import sys, os, json, base64
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
cfg = json.load(open(REPO + 'config/fym-rack-rotate-oct26.json'))['racks']; IMG = {}
hd = json.load(open(B + '/hd/index.json'))
for k, v in cfg.items():
    r = D['racks'].get(k)
    if not r: print('missing rack', k); continue
    if r['im'].endswith('r95'): continue
    nk = r['im'] + 'r95'; IMG[nk] = 'data:image/webp;base64,' + base64.b64encode(open(REPO + v['img'], 'rb').read()).decode()
    r['im'] = nk; hd['r'].pop(k, None)
json.dump(hd, open(B + '/hd/index.json', 'w'), separators=(',', ':'))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h); print('rotated rack photos:', len(IMG))
