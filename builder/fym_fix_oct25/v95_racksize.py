"""FYM v95: racks that drew TINY on match cards (photo = a stack of racks) get ONE real rack cropped from the brand's
listing photo; a rack with no usable single-rack photo is hidden. config/fym-rack-size-oct26.json. Run AFTER
v95_rackrotate.py. Idempotent (new IMG key = old + 's95'). Gate [73]. Usage: v95_racksize.py <build>"""
import sys, os, json, base64
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
C = json.load(open(REPO + 'config/fym-rack-size-oct26.json')); IMG = {}
hd = json.load(open(B + '/hd/index.json'))
for k, v in C['racks'].items():
    r = D['racks'].get(k)
    if not r: print('missing rack', k); continue
    if r['im'].endswith('s95'): continue
    nk = r['im'] + 's95'; IMG[nk] = 'data:image/webp;base64,' + base64.b64encode(open(REPO + v['img'], 'rb').read()).decode()
    r['im'] = nk; hd['r'].pop(k, None)
for k in C.get('hide', {}):
    if k in D['racks'] and not D['racks'][k].get('hid'): D['racks'][k]['hid'] = True; print('hidden', D['racks'][k]['n'])
json.dump(hd, open(B + '/hd/index.json', 'w'), separators=(',', ':'))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h); print('single-rack photos:', len(IMG))
