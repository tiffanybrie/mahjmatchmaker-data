"""FYM v89 (Tiffany Oct 25 16:56): the on-card swipe cue shows once per VISIT (sessionStorage: a new browser session / reopened app
shows it again on the first card), not once ever (localStorage). "someone might use it once, but then they want to show their friend".
Usage: python3 v89_cueonce.py <build_dir>"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
SS = "const SSW={get(){try{return sessionStorage.getItem('fym_swiped');}catch(e){return null;}},set(){try{sessionStorage.setItem('fym_swiped','1');}catch(e){}}};"
for a, b in (("function swLearned(){LS.set('fym_swiped','1');", SS + "function swLearned(){SSW.set();"), ("LS.get('fym_swiped')", "SSW.get()")):
    assert h.count(a) == 1, a; h = h.replace(a, b)
open(P, 'w').write(h); print('ok')
