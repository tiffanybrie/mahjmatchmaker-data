"""FYM v96 rack cleanup (QA v95 item 2c, Oct 26; Tiffany 11:35 'the best-photographed rack wins when equal').
config/fym-rack-clean-oct26.json: recut (clean cutouts from the brands' own photos, assets/racks/v96c), pq overrides,
data fixes (Bird & Bamboo 'Clear' = Clear Wood Stain -> Wood). Ranking: (1) a MAT-brand rack is only lifted early when its photo
scores pq>=3 (tile-brand lift unchanged); (2) a rack with pq<=2 never leads a list (top 3) unless it is her pick or the tile
brand's own rack. Idempotent (IMG key + 'c96'). Gate [81]. Usage: python3 v96_rackclean.py <build>"""
import sys, os, json, base64
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
cfg = json.load(open(REPO + 'config/fym-rack-clean-oct26.json'))
hd = json.load(open(B + '/hd/index.json')); IMG = {}
for k, path in cfg['recut'].items():
    r = D['racks'].get(k)
    if not r: print('missing rack', k); continue
    if r['im'].endswith('c96'): continue
    nk = r['im'] + 'c96'; IMG[nk] = 'data:image/webp;base64,' + base64.b64encode(open(REPO + path, 'rb').read()).decode()
    r['im'] = nk; hd['r'].pop(k, None)
for k, v in cfg['pq'].items():
    if k in D['racks']: D['racks'][k]['pq'] = v
for k, v in cfg['fix'].items():
    r = D['racks'].get(k)
    if r:
        for a, b in v.items():
            if not a.startswith('_'): r[a] = b
        r.pop('cl', None)
json.dump(hd, open(B + '/hd/index.json', 'w'), separators=(',', ':'))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if '/*v96 poor photo never leads*/' not in h:
    a = "const ow=L.filter(r=>!mine(r)&&B.includes(R[r].bn)&&(wc(r)||rackFits(r)&&sc(r)<=30));"
    assert h.count(a) == 1
    h = h.replace(a, "const ow=L.filter(r=>!mine(r)&&B.includes(R[r].bn)&&(ownW(r)===2||(R[r].pq||3)>=3)&&(wc(r)||rackFits(r)&&sc(r)<=30));", 1)
    a = "if(f.brand)ids=ids.filter(r=>R[r].bn===f.brand);return ids;}"
    assert h.count(a) == 1
    h = h.replace(a, "if(f.brand)ids=ids.filter(r=>R[r].bn===f.brand);/*v96 poor photo never leads*/{const U=uni(),poor=r=>(R[r].pq||3)<=2&&!hr.includes(r)&&!U.includes(r)&&ownW(r)!==2;const G=ids.filter(r=>!poor(r)).slice(0,3);if(G.length)ids=[...ids.filter(r=>!poor(r)&&ids.indexOf(r)<=ids.indexOf(G[G.length-1])),...ids.filter(r=>!(!poor(r)&&ids.indexOf(r)<=ids.indexOf(G[G.length-1])))];}return ids;}", 1)
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h); print('rackclean v96: recuts', len(IMG), '| pq', len(cfg['pq']), '| fixes', len(cfg['fix']))
