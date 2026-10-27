"""FYM v98 (Version 1.2) match card title colour (MATCH-INBOX, Tiffany Oct 26 6:25pm): the v95 contrast loop re-invented the set
colour (OMM Solara #e26959 came out burnt orange). The title now uses the ASSIGNED colour-card colour s.tc exactly; when it is
light against the cream card (contrast < 3), it only gets a white outline + soft shadow, never a different colour.
Idempotent. Gate [95] (and [72] accepts the v98 marker). Usage: v98_title.py <build>"""
import sys, re
P = sys.argv[1] + '/index.html'; h = open(P).read(); n = 0
if '/*v98 assigned title colour*/' not in h:
    i = h.index(' const tc=(()=>{const h=s.tc||'); j = h.index('})();', i) + 5
    assert '/* v95 contrast */' in h[i:j]
    new = (" const tc=s.tc||'#d6247f'/*v98 assigned title colour*/;const tcLow=(()=>{const L_=x=>{const c=parseInt(tc.slice(x,x+2),16)/255;"
           "return c<=.03928?c/12.92:Math.pow((c+.055)/1.055,2.4);};const l=.2126*L_(1)+.7152*L_(3)+.0722*L_(5);return /^#[0-9a-f]{6}$/i.test(tc)&&(.8534+.05)/(l+.05)<3;})();")
    h = h[:i] + new + h[j:]; n += 1
o = "g.fillStyle='rgba(255,255,255,.9)';g.fillText(l,W/2+4,y+4);g.fillStyle=tc;g.fillText(l,W/2,y);"
nw = ("g.fillStyle='rgba(255,255,255,.9)';g.fillText(l,W/2+4,y+4);if(tcLow){/*v98 white outline for light colours*/g.save();g.lineJoin='round';"
      "g.strokeStyle='#fff';g.lineWidth=10;g.shadowColor='rgba(40,20,30,.35)';g.shadowBlur=10;g.strokeText(l,W/2,y);g.restore();}g.fillStyle=tc;g.fillText(l,W/2,y);")
if '/*v98 white outline for light colours*/' not in h:
    assert h.count(o) == 1, h.count(o); h = h.replace(o, nw); n += 1
open(P, 'w').write(h); print('v98 title', n)
