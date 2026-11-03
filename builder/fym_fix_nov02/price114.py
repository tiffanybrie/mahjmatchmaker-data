"""v114 price filter on the app's own decks (see price114.js). Run AFTER builder/table_view/preview_nov01.py --release (needs TVD).
Card meta shows the price while a chip is on; the mat-door tile deck gets its row in the controls under the deck.
Idempotent. Usage: python3 price114.py <build dir or index.html>"""
import sys, os, pathlib
P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html'); h = open(P).read()
if '/*v114 price*/' in h: print('price114 already'); sys.exit()
assert 'const TVD=' in h, 'run the Table view step first'
def rep(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:100]); h = h.replace(a, b)
rep("${!mat&&UNI.includes(id)?' · goes with everything':''}</span>", "${!mat&&UNI.includes(id)?' · goes with everything':''}</span>${typeof PRC==='function'?PRC(mat?'m':'r',id):''}")
rep("""${(T[s.tile]||{}).oos?' <b class="sob">Sold out</b>':''}</span></div>${peek?'':STB('t',s.slug)}""",
    """${(T[s.tile]||{}).oos?' <b class="sob">Sold out</b>':''}</span>${typeof PRC==='function'?PRC('t',r.i):''}</div>${peek?'':STB('t',s.slug)}""")
rep("""<div class="s2ctl">${VROW()}<div class="msearch s2"><input id="tdq\"""", """<div class="s2ctl">${VROW()}${typeof PRB==='function'?PRB('t'):''}<div class="msearch s2"><input id="tdq\"""")
css = ("/*v114 price*/.prw{display:flex;flex-wrap:wrap;gap:4px 8px;justify-content:center;align-items:center;margin:4px 0 2px}.prsel{display:inline-flex;align-items:center;gap:6px;font:700 12px/1 var(--body);color:var(--navy,#054689)}.prsel select{font:600 13px/1.2 var(--body);color:var(--navy,#054689);border:1px solid #ecd5df;border-radius:999px;padding:6px 26px 6px 12px;background:#fff;-webkit-appearance:none;appearance:none;background-image:linear-gradient(45deg,transparent 50%,currentColor 50%),linear-gradient(135deg,currentColor 50%,transparent 50%);background-position:calc(100% - 13px) 50%,calc(100% - 9px) 50%;background-size:4px 4px;background-repeat:no-repeat}.prw .prn{flex-basis:100%;text-align:center}.prw .chip.prc{font-size:12px;padding:6px 10px}"
       ".prw .chip.prc[aria-pressed=true]{background:var(--navy,#054689);color:#fff;border-color:var(--navy,#054689)}"
       ".prn{display:block;text-align:center;font-size:11.5px;color:var(--mute);margin:2px 6px 4px}"
       ".prc1{display:block;font:700 12px/1.25 var(--body);color:var(--ink)}.prc1 em{font:italic 400 11px var(--body);color:#c8325f}")
i = h.index('</style>'); h = h[:i] + css + h[i:]
js = (pathlib.Path(__file__).parent / 'price114.js').read_text()
j = h.rindex('</body>') if '</body>' in h else len(h)
h = h[:j] + '<script>' + js + '</script>' + h[j:]
open(P, 'w').write(h); print('price114 ok', len(h.encode()))
