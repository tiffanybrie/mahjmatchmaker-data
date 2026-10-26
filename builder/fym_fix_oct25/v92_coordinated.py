"""FYM v92: coordinated collections first (Tiffany Oct 25 20:24: "Their Deco match should populate first", own colourway first).
config/fym-coordinated.json: set slug -> mat keys in order. They go to the front of s.cr (picks off / colour ranking) and
s.rank. Run AFTER any colour-rank rebuild. Usage: v92_coordinated.py <build>"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
cfg = {k: v for k, v in json.load(open(REPO + 'config/fym-coordinated.json')).items() if not k.startswith('_')}
OI = {m: j for j, m in enumerate(D['order'])}
for s in D['sets']:
    if s['slug'] not in cfg: continue
    front = [OI[m] for m in cfg[s['slug']] if m in OI and not D['mats'][m].get('hid')]
    for f in ('cr', 'rank'):
        s[f] = front + [x for x in s.get(f, []) if x not in front]
    print(s['name'], '->', [D['mats'][D['order'][x]]['n'] for x in front])
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h)
