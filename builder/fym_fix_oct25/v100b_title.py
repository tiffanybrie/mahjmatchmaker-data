"""FYM v100b card title (Tiffany Oct 27 12:47am: "Solara was supposed to be peachy... look at the colors of the albums that are
already approved"; "why is Papaya Spritz green?"). Title = the colour on her APPROVED album cards (config/fym-title-colours-oct27.json,
else the set's stored tc), EXACTLY: solid fill + soft white offset shadow, NO outline, NO darkening. Only near-white/grey colours
that vanish on the cream (contrast < 1.5) get a fallback, chosen by her (FB below; window.TCFB lets a preview switch it).
Usage: v100b_title.py <build> [dark|navy]"""
import sys, json, os
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; FB = sys.argv[2] if len(sys.argv) > 2 else 'dark'; P = B + '/index.html'; h = open(P).read()
TCO = json.load(open(REPO + 'config/fym-title-colours-oct27.json'))['colours']
a = h.index("const tc=/*v100 title*/"); b = h.index("const mName=", a)
new = ("const tc=/*v100 title*//*v100b album colour*/(()=>{const h=(" + json.dumps(TCO, separators=(',', ':')) + ")[s.name]||s.tc||'#d6247f';"
 "const L_=x=>{const c=parseInt(h.slice(x,x+2),16)/255;return c<=.03928?c/12.92:Math.pow((c+.055)/1.055,2.4);};"
 "if(!/^#[0-9a-f]{6}$/i.test(h)||(.8534+.05)/(.2126*L_(1)+.7152*L_(3)+.0722*L_(5)+.05)>=1.5)return h;"
 "if((window.TCFB||'" + FB + "')==='navy')return '#1f3a6b';"
 "let r=parseInt(h.slice(1,3),16)/255,gg=parseInt(h.slice(3,5),16)/255,b=parseInt(h.slice(5,7),16)/255;const mx=Math.max(r,gg,b),mn=Math.min(r,gg,b);let H2=0,S2=0,L=(mx+mn)/2;"
 "if(mx!==mn){const d=mx-mn;S2=L>.5?d/(2-mx-mn):d/(mx+mn);H2=mx===r?(gg-b)/d+(gg<b?6:0):mx===gg?(b-r)/d+2:(r-gg)/d+4;H2/=6;}"
 "return `hsl(${Math.round(H2*360)},${Math.round(Math.min(1,Math.max(S2,.3))*100)}%,55%)`;})();\n ")
h = h[:a] + new + h[b:]
open(P, 'w').write(h); print('v100b: album colours', len(TCO), 'fallback', FB)
