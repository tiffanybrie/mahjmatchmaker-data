"""FYM v89 (Tiffany Oct 25 16:55, desktop): tapping Start over at the top of the page greyed the screen but the "Start over? ...
Keep my picks" prompt appeared at the very bottom of the page. Inside the artifact / website the app is one tall frame, so a
position:fixed bottom sheet sits at the bottom of the whole page. Now every pop-up sheet (Start over, Shop by brand) opens where
the person tapped when the app is inside a frame; standalone it stays a bottom sheet.
Usage: python3 v89_sheetpos.py <build_dir>"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (a[:80], h.count(a)); h = h.replace(a, b)
css = ".sheet{position:fixed;inset:0;z-index:40;background:rgba(30,16,30,.45);display:flex;align-items:flex-end;justify-content:center}"
rep(css, css + ".sheet.at{position:absolute;inset:auto;left:0;right:0;top:0;display:block}.sheet.at .box{position:absolute;left:50%;transform:translateX(-50%);border-radius:22px;width:calc(100% - 24px);max-height:600px;box-shadow:0 18px 50px rgba(30,16,30,.35)}")
JS = ("/* v89: pop-ups open where you tapped when the app is inside a frame (artifact / website), not at the bottom of the page */"
      "let lastTap=null;document.addEventListener('pointerdown',e=>{lastTap=e.target;},true);"
      "function openSheet(d){document.body.appendChild(d);let inFrame=true;try{inFrame=window.top!==window;}catch(e){}if(!inFrame)return;"
      "const de=document.documentElement||{},H=Math.max(de.scrollHeight||0,(document.body||{}).scrollHeight||0);if(!H)return;d.classList.add('at');d.style.height=H+'px';const b=d.querySelector('.box');"
      "const t=lastTap&&lastTap.isConnected?lastTap.getBoundingClientRect().top+window.scrollY:window.scrollY+80;"
      "b.style.top=Math.max(12,Math.min(H-b.offsetHeight-12,t-Math.min(b.offsetHeight/2,110)))+'px';const f=b.querySelector('button');if(f)try{f.focus({preventScroll:true});}catch(e){}}")
rep("function startOver(){", JS + "function startOver(){")
rep("d.addEventListener('click',e=>{if(e.target===d)d.remove();});document.body.appendChild(d);}",
    "d.addEventListener('click',e=>{if(e.target===d)d.remove();});openSheet(d);}")
import re
# brand sheet: find its append
i = h.index("el.className='sheet';el.innerHTML=`<div class=\"box\"><button type=\"button\" class=\"x\" aria-label=\"Close\">✕</button><h3>Shop by brand</h3>")
j = h.index("document.body.appendChild(el)", i); assert j - i < 3000
h = h[:j] + "openSheet(el)" + h[j + len("document.body.appendChild(el)"):]
open(P, 'w').write(h); print('ok')
