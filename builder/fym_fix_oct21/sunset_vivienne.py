"""FYM v71: Oh My Mahjong Vivienne into Sunset's match list (Tiffany Oct 21 7:15pm: 'if Vivienne matches Papaya Spritz it should
match Sunset too'; album card #4). Racks = Sunset tile racks (D.lt) + config/mat-racks-picks.json vivienne. Lock + live album snapshot + D.ao.
Usage: python3 builder/fym_fix_oct21/sunset_vivienne.py <build_dir>"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
K = 'www.ohmymahjong.com/vivienne-mat-in-tube'; R = D['racks']
byname = {r['n']: k for k, r in R.items()}
mr = [byname[n] for n in json.load(open(REPO + 'config/mat-racks-picks.json'))['vivienne']['racks'] if n in byname]
s = next(x for x in D['sets'] if x['slug'] == 'sunset'); L = json.load(open(REPO + 'builder/fym_flags/locks.json'))
if not any(e[0] == K for e in s['m']):
    s['m'].insert(min(3, len(s['m'])), [K, list(dict.fromkeys(list(D['lt'].get('sunset', [])) + mr))])
    L['sets']['sunset']['m'] = s['m']
    L['_changes'].append({'date': '2026-10-21', 'set': 'sunset', 'field': 'm', 'change': f'added Vivienne ({K}) at #4, racks Sunset tile racks + Vivienne mat racks',
                          'approval': "Tiffany Oct 21 7:15pm: if Vivienne matches Papaya Spritz it should match Sunset too (album card #4). Her real pick."})
    json.dump(L, open(REPO + 'builder/fym_flags/locks.json', 'w'), ensure_ascii=False, indent=1)
SNAP = REPO + 'scripts/social/its_a_match/albums-live-oct21.json'; A = json.load(open(SNAP))
for a in A:
    if a['slug'] == 'sunset' and not any(c['mat'] == 'Vivienne' for c in a['cards']):
        a['cards'].insert(3, {'n': '04', 'img': '', 'mat': 'Vivienne', 'brand': 'Oh My Mahjong', 'retired': False})
        for k, c in enumerate(a['cards']): c['n'] = '%02d' % (k + 1)
        if isinstance(a.get('n'), int): a['n'] += 1
json.dump(A, open(SNAP, 'w'), indent=0)
import album_order; D['ao'], _ = album_order.compute(D)
open(P, 'w').write(h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:])
print('sunset m', len(s['m']), 'racks', mr, 'ao sunset first 5', [D['mats'][k]['n'] for k in D['ao'].get('sunset', [])[:5]])
