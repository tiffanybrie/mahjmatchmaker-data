"""FYM v91 (Tiffany Oct 25 20:03): on the mat step the filter row (Tiffany's picks / Brand / colours / + Add colour / Holiday) sat ABOVE
the tile photo, but it filters the MATS. Same principle as the racks (v85): it now sits between the tile photo and the mat deck
(Up close), or right above the deck (Aerial). The 'Already own a mat?' search stays at the top. The 30-second tour targets the deck
card (#top-m) and the tray, so gate [35] (tour placement at 390x664 / 390x844 / 1280x800) re-checks every step lands.
Usage: python3 v91_matfilters.py <build_dir>"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
def rep(a, b):
    global h
    assert h.count(a) == 1, a[:100]; h = h.replace(a, b)
rep("aria-label=\"Search mats\"><div id=\"msr\" class=\"msr\" role=\"listbox\"></div></div>`+filters('m')+(S.door==='mat'",
    "aria-label=\"Search mats\"><div id=\"msr\" class=\"msr\" role=\"listbox\"></div></div>`+(S.door==='mat'")
rep("(S.mode==='close'?`<div class=\"cmp\">${tileView('m')}<div class=\"tcap\"><span>${esc(s.name)} tiles</span>${backBtn()}</div>${deck('m')}</div>`:`<div class=\"backrow\">${backBtn()}</div><div class=\"cmp aer\">${deck('m')}</div>`)+acts('m')",
    "(S.mode==='close'?`<div class=\"cmp\">${tileView('m')}<div class=\"tcap\"><span>${esc(s.name)} tiles</span>${backBtn()}</div><div class=\"rfil mfil\">${filters('m')}</div>${deck('m')}</div>`:`<div class=\"backrow\">${backBtn()}</div><div class=\"rfil mfil\">${filters('m')}</div><div class=\"cmp aer\">${deck('m')}</div>`)+acts('m')")
open(P, 'w').write(h); print('ok')
