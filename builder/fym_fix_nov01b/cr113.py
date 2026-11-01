"""v113: same as builder/fym_fix_oct31/v109cr.py for the v113 adds (add == 'nov01-v113'): new mats never push a set's established
top-5 colour-deck mats out (gate [76]). Usage: python3 cr113.py <source index.html> <out build dir>"""
import os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fym_fix_oct31', 'v109cr.py')
src = open(P).read(); a = "== 'oct31-v109'"; assert a in src; src = src.replace(a, "== 'nov01-v113'")
exec(compile(src, P, 'exec'), {'__name__': '__main__', '__file__': P})
