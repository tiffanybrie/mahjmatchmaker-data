"""FYM v84 (Tiffany Oct 25 14:13-14:14, approved; buttons moved up = picks row under them): (1) intro line above the two door buttons on both start screens:
"Pick your tiles and we'll find the mat. Pick a mat and we'll find the tiles. Then add racks."  (2) swipe hints for people who skip the tour
(her husband): a line "Swipe right ♥ to keep · swipe left ✕ to pass" over the ✕/♥ buttons, and 'Pass' / 'Keep' labels under them.
Usage: python3 v84_hints.py <build_dir>  (in place, after v84_doors.py)"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
INTRO = '<p class="intro">Pick your tiles and we’ll find the mat. Pick a mat and we’ll find the tiles. Then add racks.</p>'
a = 'bringing to the table.</div></div>${doorBtns()}<button type="button" class="solink" data-tour'
assert h.count(a) == 1; h = h.replace(a, a.replace('${doorBtns()}', INTRO + '${doorBtns()}'))
b = "el.innerHTML=lock+doorBtns()+'<button type=\"button\" class=\"solink\" data-tour"
assert h.count(b) == 1; h = h.replace(b, b.replace("lock+doorBtns()", "lock+'" + INTRO + "'+doorBtns()"))
c = ("return `<div class=\"acts\"><button type=\"button\" class=\"no\" data-no=\"${k}\" aria-label=\"No thanks\" ${q.length?'':'disabled'}>✕</button>"
     "<button type=\"button\" class=\"yes\" data-yes=\"${k}\" aria-label=\"Love\" ${q.length?'':'disabled'}>♥</button></div>`;")
assert h.count(c) == 1, h.count(c)
h = h.replace(c, "return `${q.length?'<p class=\"swhint\">Swipe right ♥ to keep · swipe left ✕ to pass</p>':''}<div class=\"acts\">"
              "<span class=\"ab\"><button type=\"button\" class=\"no\" data-no=\"${k}\" aria-label=\"No thanks\" ${q.length?'':'disabled'}>✕</button><small>Pass</small></span>"
              "<span class=\"ab\"><button type=\"button\" class=\"yes\" data-yes=\"${k}\" aria-label=\"Love\" ${q.length?'':'disabled'}>♥</button><small>Keep</small></span></div>`;")
css = '.acts .no{width:54px;'
assert h.count(css) == 1
h = h.replace(css, '.intro{margin:2px 6px 8px;text-align:center;font:600 14px/1.4 var(--body);color:var(--navy)} '
              '.swhint{margin:2px 0 0;text-align:center;font:600 12.5px/1.3 var(--body);color:var(--mute)} '
              '.acts .ab{display:flex;flex-direction:column;align-items:center;gap:3px} .acts .ab small{font:700 11px var(--body);color:var(--mute);letter-spacing:.02em} ' + css)
# (3) buttons up: Tiffany's-picks row moves under the buttons on the mat deck
d = "herBar('m')+acts('m')+tray('m')"
assert h.count(d) == 1; h = h.replace(d, "acts('m')+herBar('m')+tray('m')")
# (4) 'Start with a mat' fits on one line on a phone
e = "font:400 clamp(15px,4.4vw,19px)/1.05 'Alfa Slab One'"
assert h.count(e) == 1; h = h.replace(e, "font:400 clamp(14px,3.9vw,19px)/1.05 'Alfa Slab One'")
open(P, 'w').write(h); print('ok')
