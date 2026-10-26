"""FYM v95 rack photos (Tiffany Oct 26 11:35 + 11:39; QA v95 rack list).
1. config/fym-rack-recut-oct26.json: rack key -> single-rack recut (assets/racks/v95q/make.py: the LONGEST rack, levelled,
   background removed; Iridescent Opal = Miss Mahjong's own single-rack cutout, no white box). New card image, HD copy dropped.
2. config/fym-rack-pq-oct26.json: photo-quality score (pq 1-5) re-judged by eye on the v95 card image; overrides
   config/rack-photo-quality.json so angled/standing shots (e.g. Anders Ruff clear acrylic) lose ties to clean ones.
Idempotent (new IMG key = old + 'q95'). Run after v95_racksize. Gate [75]. Usage: v95_rackphotos.py <build>"""
import sys, os, json, base64
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
cut = json.load(open(REPO + 'config/fym-rack-recut-oct26.json'))['racks']
pq = json.load(open(REPO + 'config/fym-rack-pq-oct26.json'))['racks']
hd = json.load(open(B + '/hd/index.json')); IMG = {}; nq = 0
for k, path in cut.items():
    r = D['racks'].get(k)
    if not r: print('missing rack', k); continue
    if r['im'].endswith('q95'): continue
    nk = r['im'] + 'q95'; IMG[nk] = 'data:image/webp;base64,' + base64.b64encode(open(REPO + path, 'rb').read()).decode()
    r['im'] = nk; hd['r'].pop(k, None)
for k, v in pq.items():
    if k in D['racks']: D['racks'][k]['pq'] = v['pq']; nq += 1
json.dump(hd, open(B + '/hd/index.json', 'w'), separators=(',', ':'))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h); print('rack recuts:', len(IMG), '| pq re-judged:', nq)
