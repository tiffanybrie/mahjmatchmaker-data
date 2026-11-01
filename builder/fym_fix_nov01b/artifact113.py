"""v113 claude.ai artifact copy. The artifact is at its 512-file limit and ~0.75 MiB under the 253.14 MiB safety line (256 MiB cap
- 3 MB margin) after v112 (live: 252.39 MiB). So the v113 adds do NOT all fit:
 - Sunday Ruby + Forrest always go in;
 - Let's Be Besties new mats go in best-ranked first, round-robin over their primary colours (rank = how high the mat sits in the
   sets' colour decks: sum over sets of max(0, 40 - position)), until the byte budget is used;
 - every other v113 add is hidden in THIS copy only (hid + ahid=1, photo/thumb dropped); the website copy has all of them.
Pack: chunks 190..241 -> ONE mc/190.webp at q66 (only images the index references), as artifact112. b24v1.js stays the published
v111 one; thumbnails it lacks go inline. Writes <out>/index.html, <out>/mc/190.webp, <out>/files.json (only changed files).
Usage: python3 artifact113.py <b113 dir> <published b24v1.js> <pub112 dir> <out dir> [budget bytes, default 786432-65536]"""
import sys, os, json, re, struct, io, base64, mimetypes
from PIL import Image
B, PB24, P112, O = sys.argv[1:5]; BUDGET = int(sys.argv[5]) if len(sys.argv) > 5 else 786432 - 65536
os.makedirs(O + '/mc', exist_ok=True)
h = open(B + '/index.html').read()
i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); M = D['mats']
NEWC = [c for c in range(190, 260) if os.path.exists(f'{B}/mc/{c}.webp')]
IMGS = {}
for c in NEWC:
    ab = open(f'{B}/mc/{c}.webp', 'rb').read(); n = struct.unpack('<I', ab[-4:])[0]
    for f, (a, l) in json.loads(ab[-4 - n:-4]).items(): IMGS[f] = ab[a:a + l]
def q66(raw):
    im = Image.open(io.BytesIO(raw)); b = io.BytesIO(); im.save(b, 'WEBP', quality=66, method=6); return b.getvalue()
def inl(s):
    out = {}
    for m in re.finditer(r'window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', s):
        o, _ = json.JSONDecoder().raw_decode(s[m.end():]); out.update(o)
    return out
TH = inl(h)
pos = {}
for s in D['sets']:
    L = [D['order'][j] for j in (s.get('cr') or []) + s.get('rank', []) if j < len(D['order'])]
    seen = []
    for k in L:
        if k in seen or k not in M or M[k].get('hid') or M[k].get('rt'): continue
        seen.append(k)
    for p, k in enumerate(seen[:40]): pos[k] = pos.get(k, 0) + (40 - p)
adds = [k for k, m in M.items() if m.get('add') == 'nov01-v113' and not m.get('hid')]
must = [k for k in adds if M[k].get('bn') == 'Sunday Mahjong']
lbb = [k for k in adds if k not in must]
byc = {}
for k in sorted(lbb, key=lambda k: -pos.get(k, 0)):
    c = (M[k].get('mf') or M[k].get('ha') or ['other'])[0]; byc.setdefault(c, []).append(k)
order, cols = [], sorted(byc, key=lambda c: -pos.get(byc[c][0], 0))
while any(byc.values()):
    for c in cols:
        if byc[c]: order.append(byc[c].pop(0))
cost = lambda k: len(q66(IMGS[M[k]['f']])) + len(TH.get(M[k].get('th'), '')) + 120 + 4 * 328
used, keep = 0, []
for k in must + order:
    cst = cost(k)
    if k in must or used + cst <= BUDGET: keep.append(k); used += cst
drop = [k for k in adds if k not in keep]
for k in drop:
    o = M[k]; TH.pop(o.get('th'), None); o.update(hid=True, ahid=1, f='', th='')
DS = {D['order'].index(k) for k in drop}
for s_ in D['sets']:
    for fld in ('rank', 'cr'):
        if fld in s_: s_[fld] = [j for j in s_[fld] if j not in DS]
for k in drop:  # slim the hidden entries (never shown here)
    o = M[k]; M[k] = {x: o[x] for x in ('n', 'bn', 'b', 'hid', 'ahid', 'f', 'th', 'add', 'mf', 'mt', 'hol', 'u', 'pa') if x in o}
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]
# rewrite inline IMG blocks without the dropped thumbnails
first = None
while True:
    m = re.search(r'<script>window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', h)
    if not m: break
    o, e2 = json.JSONDecoder().raw_decode(h[m.end():]); end = h.index('</script>', m.end() + e2) + len('</script>')
    if first is None: first = m.start()
    h = h[:m.start()] + h[end:]
pub, mine = inl(open(PB24).read()), inl(open(B + '/b24v1.js').read())
assert all(mine[k] == pub[k] for k in pub if k in mine), 'a published thumbnail changed value'
need = {k: v for k, v in {**mine, **TH}.items() if k not in pub}
need = {k: v for k, v in need.items() if k in h}
tag = '<script src="b24v1.js">'; assert h.count(tag) == 1
h = h.replace(tag, '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(need, separators=(',', ':')) + ');</script>' + tag, 1)
# pack
body, hdr = b'', {}
for f, raw in IMGS.items():
    if f not in h: continue
    q = q66(raw); hdr[f] = [len(body), len(q)]; body += q
hj = json.dumps(hdr, separators=(',', ':')).encode()
open(O + '/mc/190.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
a = "fetch('mc/'+c+'.webp')"; assert h.count(a) == 1, h.count(a)
h = h.replace(a, f"fetch('mc/'+(c>=190&&c<={NEWC[-1]}?190:c)+'.webp')/*v113 artifact: chunks 190-{NEWC[-1]} packed in one file (512-file limit)*/", 1)
i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); ninl = 0
for t in D['tiles'].values():
    p = t.get('full', '')
    if isinstance(p, str) and p.startswith(('t106/', 't112/')):
        t['full'] = f'data:{mimetypes.guess_type(p)[0] or "image/jpeg"};base64,' + base64.b64encode(open(B + '/' + p, 'rb').read()).decode(); ninl += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]
open(O + '/index.html', 'w').write(h)
sz = len(h.encode()); assert sz < 16 * 10**6 - 30000, sz
d_idx = sz - os.path.getsize(P112 + '/index.html'); d_pack = os.path.getsize(O + '/mc/190.webp') - os.path.getsize(P112 + '/mc/190.webp')
json.dump({'mc/190.webp': os.path.basename(O) + '/mc/190.webp'}, open(O + '/files.json', 'w'), indent=1)
print('artifact113: v113 adds', len(adds), 'in artifact', len(keep), f'(Sunday {len(must)}, LBB {len(keep) - len(must)})', 'hidden here', len(drop),
      '| index', sz, 'delta', d_idx, '| pack', os.path.getsize(O + '/mc/190.webp'), 'delta', d_pack, '| total delta', d_idx + d_pack, 'budget', BUDGET)
json.dump({'kept': keep, 'dropped': drop}, open(O + '/kept.json', 'w'))
