"""FYM v94: fix Mahjong Studios rack colour tags (Tiffany Oct 26 9:18am). config/fym-mstudios-rack-colours-oct26.json.
Idempotent. Usage: v94_msrackcolours.py <build>"""
import sys, os, json
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
C = json.load(open(R + 'config/fym-mstudios-rack-colours-oct26.json'))
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i; n = 0
for k, r in D['racks'].items():
    if r.get('bn') != 'Mahjong Studios': continue
    for pre, fix in C['by_name'].items():
        if r['n'].startswith(pre): r['rf'] = fix['rf']; r['hx'] = fix['hx']; n += 1
    if 'clear' in (r.get('rf') or []) and not any(w in r['n'] for w in C['drop_clear_unless_name']):
        r['rf'] = [x for x in r['rf'] if x != 'clear']; n += 1
print('Mahjong Studios rack colour fixes:', n)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h)
