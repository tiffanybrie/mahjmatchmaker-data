"""FYM v94: Mahjong Studios tiles -> Photo coming soon; brands whose sets are all 'Photo coming soon' sort last
in the Shop-by-brand menu (Tiffany Oct 26 8:42am: "Mahjong Studio's tiles just aren't cutting it because they don't
have a tile back view. We change all of them to photo coming soon, and we move that brand to the bottom of the list").
Run after v94_soonlast.py (which already sorts soon items last in A-Z / brand / colour lists). Idempotent.
Usage: python3 v94_mstudios.py <build_dir>"""
import sys, json
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
n = 0
for k, t in D['tiles'].items():
    if k.startswith('mahjongstudios.com/'):
        if not t.get('soon'): n += 1
        t['soon'] = 1
print('Mahjong Studios tiles set to Photo coming soon:', n)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
old = "n[s.maker]=(n[s.maker]||0)+1;pa[s.maker]=pa[s.maker]||!!t.pa;});const B=Object.keys(n).sort((a,b)=>a.localeCompare(b))"
new = ("n[s.maker]=(n[s.maker]||0)+1;pa[s.maker]=pa[s.maker]||!!t.pa;so[s.maker]=(so[s.maker]??true)&&!!t.soon;});"
       "const B=Object.keys(n).sort((a,b)=>(so[a]-so[b])||a.localeCompare(b))")
if old in h:
    assert h.count(old) == 1
    h = h.replace(old, new).replace("function brandMenu(){const all=D.sets.filter(VIS),pa={},n={};",
                                    "function brandMenu(){const all=D.sets.filter(VIS),pa={},n={},so={};", 1)
    assert 'so={}' in h
    print('brand menu: all-soon brands last')
open(P, 'w').write(h)
