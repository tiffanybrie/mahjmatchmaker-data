"""FYM 1.23 search: the mat search box ('Search any mat by name or brand') also finds a Let's Be Besties artist mat by its artist
(Lillian Claire Designs, Wanda Viola, BeachyMahj, OHBoN Studios, STM, AC Studios, Charmaine J.W., Andy Albert). The artist is dropped
from the card name (live LBB style) and kept in M[id].ak, which the search reads. Tiffany Nov 17: people type the mat's name or the
brand into Find Your Mat-ch search and it has to show up. Idempotent. Usage: python3 search123.py <build_dir> <prev dir>"""
import sys, os, json, re
B = sys.argv[1]; PV = sys.argv[2]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
items = json.load(open(PV + '/items.json'))
ART = [('Lillian Claire Designs', 'Lillian Claire Designs'), ('Wanda Viola', 'Wanda Viola'), ('BeachyMahj', 'BeachyMahj'), ('BeachMahj', 'BeachyMahj'),
       ('OHBoN Studios', 'OHBoN Studios'), ('STM', 'STM'), ('AC Studios', 'AC Studios'), ('Charmaine J.W.', 'Charmaine J.W.'), ('Andy Albert', 'Andy Albert')]
n = 0
for it in items:
    k = it['key']
    if k not in D['mats'] or D['mats'][k].get('add') != 'nov17-v123': continue
    for pat, name in ART:
        if re.search(r'(?<![A-Za-z])' + re.escape(pat) + r'(?![A-Za-z])', it['name']): D['mats'][k]['ak'] = name; n += 1; break
# a new artist mat whose short name matches another visible mat of the same brand keeps its artist in the name (e.g. two Besties Speakeasy mats)
def nk(s): s = re.sub(r'[^a-z0-9 ]', ' ', s.lower()); s = re.sub(r'\b(the|mahjong|mahj|mat)\b', ' ', s); return ' '.join(s.split())
for k, m in D['mats'].items():
    if m.get('add') != 'nov17-v123' or not m.get('ak') or m.get('hid') or m['n'].endswith(')'): continue
    if any(k2 != k and not o.get('hid') and o.get('bn') == m.get('bn') and nk(o['n']) == nk(m['n']) for k2, o in D['mats'].items()):
        m['n'] += ' (' + m['ak'] + ')'; print('kept artist in name:', m['n'])
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
a = "const s=NRM(M[id].n+' '+(M[id].bn||''));"
if a in h: assert h.count(a) == 2; h = h.replace(a, "const s=NRM(M[id].n+' '+(M[id].bn||'')+' '+(M[id].ak||''));")
else: assert "(M[id].ak||'')" in h
open(P, 'w').write(h); print('artist names on', n, 'mats')
