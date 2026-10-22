"""FYM v73 (built from live v72 + rack_picks.py). Usage: python3 builder/fym_fix_oct22/v73_ui.py <build_dir>
Tiffany's desktop test notes (Oct 22 4:44am, DESK "FYM Sunday build" items 1-3; she moved them to NOW at 1:39pm):
 1. Rack screen laid out like the mat screen: the picker ("Your racks" slots with the empty "♥ a rack" slots + Make it
    official) sits up top, right under the chosen mat; filters, then the swipe deck; the RACK SUITORS (hearted racks waiting
    to be swapped in) go to the BOTTOM, the way the mat suitors tray sits at the bottom of the mat screen.
 2. ONE "Tiffany's picks" toggle on the rack screen: the one in the filter row. The second toggle bar under the deck is gone,
    and the pill over the rack photo is a plain label again ("Tiffany's match"), not a switch. Mat screen unchanged.
 3. Back on racks: "← Back" above the rack deck (same spot as the mat screen) brings back the last rack swiped, either way
    (uses the existing undo('r')).
Gate [37] checks all three."""
import sys
B = sys.argv[1]; P = B + '/index.html'
h = open(P).read()

def rep(old, new, n=1):
    global h
    c = h.count(old)
    assert c == n, f'expected {n} x {old[:80]!r}, found {c}'
    h = h.replace(old, new)

# 1 + 3: rack screen order = mat view -> picker -> filters -> Back -> deck -> X/heart -> rack suitors (bottom)
rep("""`<div class="cmp">${tileView('r')}<div class="matv"><img src="${matSrc(S.fav)}" alt="${esc(m.n)}" class="${m.c?'':'photo'}" data-lbx="${esc(S.fav)}"><button type="button" class="chip mini" data-back-mats>Change mat</button><button type="button" class="xz" data-lbx="${esc(S.fav)}" aria-label="See this mat full screen">⤢</button></div></div>`+tray('r')+filters('r')+`<div class="cmp">${deck('r')}</div>`+herBar('r')+acts('r');""",
    """`<div class="cmp">${tileView('r')}<div class="matv"><img src="${matSrc(S.fav)}" alt="${esc(m.n)}" class="${m.c?'':'photo'}" data-lbx="${esc(S.fav)}"><button type="button" class="chip mini" data-back-mats>Change mat</button><button type="button" class="xz" data-lbx="${esc(S.fav)}" aria-label="See this mat full screen">⤢</button></div></div>`+tray('r')+filters('r')+`<div class="backrow">${rBackBtn()}</div><div class="cmp">${deck('r')}</div>`+acts('r')+rSuitors();""")
rep("""const backBtn=()=>""", """const rBackBtn=()=>`<button type="button" class="backb" data-back="r" ${S.rhist.length?'':'disabled'} aria-label="Bring back the last rack">\\u2190 Back</button>`;
const backBtn=()=>""")
# picker keeps slots + Make it official; suitors move out of it into their own bottom tray
rep("""${SG.length?`<div class="rsug"><small>Rack suitors: ${P.length===2?'tap \\u00d7 above, then tap one to swap it in':'tap one to add it'}</small><div class="th">${SG.map(id=>`<button type="button" data-rp="${esc(id)}" aria-label="${esc(R[id].n)}"><img src="${rackSrc(id)}" alt=""></button>`).join('')}</div></div>`:(P.length?'':`<div class="none">${queue('r').length>1?'Swipe right':'Tap \\u2665'} on racks you like. Your first 2 fill these slots.</div>`)}""",
    """${P.length?'':`<div class="none">${queue('r').length>1?'Swipe right':'Tap \\u2665'} on racks you like below. Your first 2 fill these slots.</div>`}""")
rep("""function tileView(cls){""", """function rSuitors(){const P=S.rpick,SG=S.rliked.filter(id=>!P.includes(id)).reverse();if(!SG.length)return '';return `<div class="tray rsug rsb" id="rsuit"><div class="tl"><b>${SG.length}</b>${SG.length===1?'suitor':'suitors'}</div><div class="rsw"><small>Rack suitors: ${P.length===2?'tap \\u00d7 on a rack above, then tap one here to swap it in':'tap one to add it'}</small><div class="th">${SG.map(id=>`<button type="button" data-rp="${esc(id)}" aria-label="${esc(R[id].n)}"><img src="${rackSrc(id)}" alt=""></button>`).join('')}</div></div></div>`;}
function tileView(cls){""")
# 2: the pill over the rack photo is a label, not a second toggle
rep("""return herUseful(kk)?`<button type="button" class="hb" data-her="${kk}\"""", """return kk==='m'&&herUseful(kk)?`<button type="button" class="hb" data-her="${kk}\"""")
# styles for the bottom suitors tray
_c = """.coach button.sk{background:transparent;color:#fbe3ec;text-decoration:underline;padding:6px 0}"""
rep(_c, _c + """
.tray.rsb{align-items:center}.tray.rsb .rsw{flex:1;min-width:0}.tray.rsb .rsw small{display:block;font:600 12px var(--body);color:var(--mute);margin:0 0 4px}
.tray.rsb .th button{width:84px;height:54px}""")
open(P, 'w').write(h)
print('v73 rack screen patched')
