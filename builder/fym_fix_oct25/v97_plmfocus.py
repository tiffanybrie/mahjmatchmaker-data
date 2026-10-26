"""FYM v97: Peace Love Mahjong tile band framing (config/fym-plm-band-oct26.json): OG Desert Dreams showed the BLANK row on the
match card. Sets t.bf. Idempotent. Gate [86]. Usage: v97_plmfocus.py <build>"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); e += i
n = 0
for k, bf in json.load(open(REPO + 'config/fym-plm-band-oct26.json'))['tiles'].items():
    if D['tiles'][k].get('bf') != bf: D['tiles'][k]['bf'] = bf; n += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:]; open(P, 'w').write(h); print('plm band', n)
