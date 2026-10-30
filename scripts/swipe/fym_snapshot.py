#!/usr/bin/env python3
"""Export a slim snapshot of the live Find Your Mat-ch mats for book_gate.py.
Usage: python3 scripts/swipe/fym_snapshot.py <FYM index.html (published artifact copy)> [out=config/fym-mats-snapshot.json] [--version vNN]
--version: the internal FYM build (e.g. v103). Auto-detected from a site-app/fym-vNN path. book_gate [f] compares it with the
newest site-app/fym-vNN on the fym-site-preview branch (rules audit GA2, Oct 30).
Run after every FYM publish (the gate refuses books against a snapshot older than the FYM version they were built from)."""
import sys, json, os, datetime
import re
VER = sys.argv[sys.argv.index('--version') + 1] if '--version' in sys.argv else None
args = [a for a in sys.argv[1:] if a != '--version' and a != VER]
src = args[0]; out = args[1] if len(args) > 1 else os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'fym-mats-snapshot.json')
if not VER:
    _m = re.search(r'fym-(v\d+)', os.path.abspath(src)); VER = _m.group(1) if _m else None
h = open(src).read(); i = h.index('const D={') + 8
D, _ = json.JSONDecoder().raw_decode(h[i:])
M = {k: {'n': m.get('n'), 'bn': m.get('bn'), 'hol': bool(m.get('hol')), 'hid': bool(m.get('hid')), 'pa': bool(m.get('pa')),
         'nc': bool(m.get('nc')), 'f': m.get('f'), 'mf': m.get('mf') or []} for k, m in D['mats'].items()}
json.dump({'_about': 'Slim FYM mats snapshot for scripts/swipe/book_gate.py (fym_snapshot.py).', 'built': datetime.date.today().isoformat(),
           'source': os.path.basename(src), 'fym_version': VER, 'mats': M}, open(out, 'w'), ensure_ascii=False, separators=(',', ':'))
print('mats', len(M), 'fym_version', VER, '->', out)
