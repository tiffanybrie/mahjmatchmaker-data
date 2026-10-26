"""FYM v98 (Version 1.2): Peace Love Mahjong OG Desert Dreams 'Up close' tile strip (above the mat deck) showed ~5 blank tiles
right of the S and W winds; v97 only re-framed the match card (t.bf). Sets the set's strip focus s.fp/s.fz from
config/fym-plm-band-oct26.json 'strip'. Also 'card_bf_v98': match card Close up band anchors (Jubilee Midnight Blue showed
the standing winds cut in half). Idempotent. Gate [93]. Usage: v98_plmstrip.py <build>"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); e += i
n = 0
for name, (fx, fy, fz) in json.load(open(REPO + 'config/fym-plm-band-oct26.json'))['strip'].items():
    for s in D['sets']:
        if s['name'] == name and (s.get('fp') != [fx, fy] or s.get('fz') != fz): s['fp'] = [fx, fy]; s['fz'] = fz; n += 1
C_ = json.load(open(REPO + 'config/fym-plm-band-oct26.json'))
for k, bf in C_.get('card_bf_v98', {}).items():
    if D['tiles'][k].get('bf') != bf: D['tiles'][k]['bf'] = bf; n += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:]; open(P, 'w').write(h); print('plm strip', n)
