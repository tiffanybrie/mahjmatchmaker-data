"""FYM 1.22.15 (copy of rank12212.py; add tag nov22-v12216). FYM 1.23: colour-rank ONLY the 1.23 adds (add == 'nov17-v123') with builder/fym_fix_oct30/v104rank.py. v104rank's own STUCK test
(TAIL=130 positions from the end) would miss part of a 225-mat append and would also move older tail mats; this runs the same code with
STUCK = the new mats and nothing else, so every existing position stays as it is. Usage: python3 rank123.py <build_dir>"""
import sys, os
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
path = R + '/builder/fym_fix_oct30/v104rank.py'; src = open(path).read()
a = "STUCK = {OI[k] for k, m in M.items() if not m.get('hid') and seen[k] and tail[k] <= TAIL}"; assert src.count(a) == 1
src = src.replace(a, "STUCK = {OI[k] for k, m in M.items() if not m.get('hid') and m.get('add') == 'nov22-v12216'}")
b = 'STUCK |= _blk'; assert src.count(b) == 1; src = src.replace(b, '_blk = set()')
exec(compile(src, path, 'exec'), {'__file__': path, '__name__': '__main__'})
# 1.22.15: faces|backs split sets added in this release (YMI) get the back-weighted ranking + s.bsw (gate [76]); only those sets.
import json, subprocess
_h = open(sys.argv[1] + '/index.html').read(); _i = _h.index('const D=') + 8; _D, _ = json.JSONDecoder().raw_decode(_h[_i:])
_sl = [s['slug'] for s in _D['sets'] if (_D['tiles'].get(s['tile']) or {}).get('add') == 'nov22-v12216' and _D['tiles'][s['tile']].get('split')]
if _sl: subprocess.run([sys.executable, R + '/builder/fym_fix_oct25/v95_matrank.py', sys.argv[1], '--only', ','.join(_sl)], check=True); print('v95 back ranking for', _sl)
