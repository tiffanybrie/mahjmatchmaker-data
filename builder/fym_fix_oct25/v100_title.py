"""FYM v100 (Version 1.4) card title (Tiffany Oct 27 12:37am: "these cards are hideous now... I hate it", OG Desert Dreams
with the v98b navy outline). Back to the pre-Oct-26 title look (v97: white offset shadow + solid fill, NO outline), keeping only
her 6:25pm ask: the ASSIGNED colour-card colour s.tc exactly when it reads on the cream card (contrast >= 2.5, e.g. Solara coral).
Paler colours get the v97 same-hue darkening (what every card showed before Oct 26). Gate [98]. Usage: v100_title.py <build>"""
import sys
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
if '/*v100 title*/' in h: print('v100 title: already'); sys.exit()
a = h.index("const tc=s.tc||'#d6247f'/*v98 assigned title colour*/;"); b = h.index("const mName=", a)
new = ("const tc=/*v100 title*/(()=>{const h=s.tc||'#d6247f';const L_=x=>{const c=parseInt(h.slice(x,x+2),16)/255;return c<=.03928?c/12.92:Math.pow((c+.055)/1.055,2.4);};"
 "if(/^#[0-9a-f]{6}$/i.test(h)&&(.8534+.05)/(.2126*L_(1)+.7152*L_(3)+.0722*L_(5)+.05)>=2.5)return h;"
 "let r=parseInt(h.slice(1,3),16)/255,gg=parseInt(h.slice(3,5),16)/255,b=parseInt(h.slice(5,7),16)/255;const mx=Math.max(r,gg,b),mn=Math.min(r,gg,b);let H2=0,S2=0,L=(mx+mn)/2;"
 "if(mx!==mn){const d=mx-mn;S2=L>.5?d/(2-mx-mn):d/(mx+mn);H2=mx===r?(gg-b)/d+(gg<b?6:0):mx===gg?(b-r)/d+2:(r-gg)/d+4;H2/=6;}const Hh=H2*360,Ss=Math.min(1,Math.max(S2,.38));let Ll=Math.min(L,.5);"
 "const lum=(hh,ss,ll)=>{const a=ss*Math.min(ll,1-ll),f=n=>{const k=(n+hh/30)%12;const c=ll-a*Math.max(-1,Math.min(k-3,9-k,1));return c<=.03928?c/12.92:Math.pow((c+.055)/1.055,2.4);};return .2126*f(0)+.7152*f(8)+.0722*f(4);};"
 "const LC=.8534;while((LC+.05)/(lum(Hh,Ss,Ll)+.05)<3.5&&Ll>.12)Ll-=.02;return `hsl(${Math.round(Hh)},${Math.round(Ss*100)}%,${Math.round(Ll*100)}%)`;})();\n ")
h = h[:a] + new + h[b:]
o = ("if(!tcVL){g.fillStyle='rgba(255,255,255,.9)';g.fillText(l,W/2+4,y+4);}if(tcLow){/*v98 white outline for light colours*//*v98b navy outline when very light*/g.save();g.lineJoin='round';"
     "g.strokeStyle=tcVL?'#062a55':'#fff';g.lineWidth=tcVL?7:10;g.shadowColor='rgba(40,20,30,.35)';g.shadowBlur=10;g.strokeText(l,W/2,y);g.restore();}g.fillStyle=tc;g.fillText(l,W/2,y);")
assert h.count(o) == 1, h.count(o)
h = h.replace(o, "g.fillStyle='rgba(255,255,255,.9)';g.fillText(l,W/2+4,y+4);g.fillStyle=tc;g.fillText(l,W/2,y);")
assert 'tcVL' not in h and 'tcLow' not in h, 'leftover'
open(P, 'w').write(h); print('v100 title: v97 look, exact s.tc when contrast >= 2.5')
