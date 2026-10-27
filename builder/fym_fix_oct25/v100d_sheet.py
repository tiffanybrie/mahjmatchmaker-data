"""FYM v100d (Version 1.4): framed pop-ups are placed inside the part of the website frame that is ON SCREEN (QA of v100c:
Brand tapped low on an iPhone left most of the box below the screen). An IntersectionObserver on a full-height sentinel gives the
visible slice of the iframe even across origins; the box is shrunk to fit that slice and moved into it. Gate [99].
Usage: v100d_sheet.py <build>"""
import sys
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
if '/*v100d visible*/' in h: print('v100d: already'); sys.exit()
o = "const f=b.querySelector('button');if(f)try{f.focus({preventScroll:true});}catch(e){}}function startOver(){"
assert h.count(o) == 1, h.count(o)
n = ("/*v100d visible*/try{if('IntersectionObserver' in window){const sen=document.createElement('div');sen.style.cssText='position:absolute;left:0;top:0;width:1px;height:'+H+'px;pointer-events:none;visibility:hidden';d.appendChild(sen);"
     "b.style.visibility='hidden';const show=()=>{b.style.visibility='';};const tmo=setTimeout(show,400);"
     "new IntersectionObserver((es,ob)=>{ob.disconnect();clearTimeout(tmo);const e=es[0],r=e.intersectionRect,br=e.boundingClientRect;"
     "if(r.height>80){const vt=r.top-br.top,vb=r.bottom-br.top,mh=Math.max(200,Math.round(r.height-24));if(b.offsetHeight>mh)b.style.maxHeight=mh+'px';"
     "const bh=Math.min(b.offsetHeight,mh);b.style.top=Math.round(Math.max(vt+12,Math.min(vb-bh-12,t-Math.min(bh/2,110))))+'px';}show();sen.remove();}).observe(sen);}}catch(e){b.style.visibility='';}")
h = h.replace(o, "const f=b.querySelector('button');if(f)try{f.focus({preventScroll:true});}catch(e){}" + n + "}function startOver(){")
open(P, 'w').write(h); print('v100d: framed pop-ups fit the on-screen part of the frame')
