#!/usr/bin/env python3
"""White phone check (Tiffany Nov 23 11:24pm: "So why do I keep having to give this correction?").
WHY IT KEPT HAPPENING: the white-iPhone rule (brand guide, Oct 26 13:59) lived only in a doc. Every new piece that shows a phone
(reels, showcase, FYM Phone view, promo, title cards) drew its own phone from scratch, and the FYM Phone view drew a black bezel.
THE FIX: there is ONE white phone builder (scripts/social/phone/iphone_white.py). Any file that draws a phone must import it, or
carry the line WHITE-PHONE-OK (added only after its output was rendered and LOOKED at: white body, white bezel). This check lists
every file that draws a phone ('9:41' status bar or 'dynamic island') without either; front door shows them every message.
usage: python3 scripts/checks/phone_white_check.py [--front]"""
import os, re, sys, glob
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
files = [f for p in ('scripts/**/*.py', 'builder/*.html', 'site-app/fym-r2-preview/index.html', 'site/livepatch/**/*.py') for f in glob.glob(R + p, recursive=True)]
bad = []
for f in files:
    if f.endswith('phone_white_check.py') or 'iphone_white.py' in f: continue
    try: t = open(f, errors='ignore').read()
    except Exception: continue
    if not re.search(r"['\">]9:41['\"<]|dynamic island", t, re.I): continue
    if 'iphone_white' in t or 'WHITE-PHONE-OK' in t: continue
    bad.append(f[len(R):])
if '--front' in sys.argv:
    if bad: print(f"WHITE PHONE NOT VERIFIED ({len(bad)}): before using any of these, render it, LOOK (white body + white bezel), then add WHITE-PHONE-OK or switch it to scripts/social/phone/iphone_white.py: " + ', '.join(bad))
    sys.exit(0)
print('\n'.join('FAIL ' + b for b in bad) or 'PASS'); sys.exit(1 if bad else 0)
