"""FYM v85 (Tiffany Oct 25 14:36): on the racks step the Brand + colour row sat ABOVE the mat picture, so her husband never found it
and kept swiping racks he didn't want. Move it between the mat picture and the rack cards (right above the swiping).
Usage: python3 v85_rackfilters.py <build_dir>  (in place)"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
a = ("'Pick your racks. Tap \\u2665 if you love it, \\u2715 if it\\u2019s not the one.')}</div>`+filters('r')+\n"
     " `<div class=\"cmp\">${matBand()}<div class=\"tcap\"><span>${esc(MN(S.fav))} mat</span><span class=\"tcr\"><button type=\"button\" class=\"backb\" data-back-mats>Change mat</button>${rBackBtn()}</span></div>${deck('r')}</div>`")
assert h.count(a) == 1, h.count(a)
b = ("'Pick your racks. Tap \\u2665 if you love it, \\u2715 if it\\u2019s not the one.')}</div>`+\n"
     " `<div class=\"cmp\">${matBand()}<div class=\"tcap\"><span>${esc(MN(S.fav))} mat</span><span class=\"tcr\"><button type=\"button\" class=\"backb\" data-back-mats>Change mat</button>${rBackBtn()}</span></div><div class=\"rfil\">${filters('r')}</div>${deck('r')}</div>`")
h = h.replace(a, b)
css = '.swh .swx{color:#7a6a85}'
assert h.count(css) == 1
h = h.replace(css, '.rfil{padding:8px 0 10px} ' + css)
open(P, 'w').write(h); print('ok')
