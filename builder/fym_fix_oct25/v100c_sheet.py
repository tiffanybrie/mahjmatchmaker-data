"""FYM v100c (Version 1.4): pop-up sheets inside the website frame on iPhone (Tiffany Oct 27 2:06am: "Shop by brand ... the last
two brands you can't select, they fall below ... it finally let go ... pushes you down the page and the brands are floating in the
middle"). In a frame, the sheet box was up to 600px tall with its own scroll, so on a phone its bottom sat under Safari's bar and
the inner scroll chained into the page scroll. Now: box height <= 55% of the phone's screen (never taller than what is visible),
centred on the tap but kept inside that window, overscroll-behavior:contain (no scroll chaining), extra bottom padding so the last
row is never under the bar. Gate [99]. Usage: v100c_sheet.py <build>"""
import sys
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
if '/*v100c sheet*/' in h: print('v100c: already'); sys.exit()
css_o = ".sheet.at .box{position:absolute;left:50%;transform:translateX(-50%);border-radius:22px;width:calc(100% - 24px);max-height:600px;box-shadow:0 18px 50px rgba(30,16,30,.35)}"
assert h.count(css_o) == 1, h.count(css_o)
h = h.replace(css_o, css_o + "/*v100c sheet*/.sheet.at .box{max-height:var(--sbh,600px);overflow-y:auto;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;padding-bottom:36px}")
js_o = "d.classList.add('at');d.style.height=H+'px';const b=d.querySelector('.box');"
assert h.count(js_o) == 1
h = h.replace(js_o, js_o + "/*v100c*/const sh=Math.min(window.screen&&screen.height||800,window.top===window?innerHeight:9e9);b.style.setProperty('--sbh',Math.round(Math.min(600,Math.max(320,sh*.55)))+'px');")
open(P, 'w').write(h); print('v100c: frame sheets fit the phone screen, no scroll chaining')
