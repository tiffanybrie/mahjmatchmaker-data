"""Yes-only swipe books (Tiffany, Oct 18 2:50pm): "If you don't get a yes from me, then it's a no."
Arrows / swipes just advance; only the green check records a yes (tap again to undo). Advancing past an
unvoted mat records 's' (seen) so she resumes at the furthest mat. Readers: anything not 'y' = no.
Usage: python3 yes_only_patch.py in.html out.html   (run after build_book.py + finish_patch.py)"""
import sys
t = open(sys.argv[1]).read()
R = [
 # mark(): 'y' toggles; 's' = seen; advance without a stamp for 's'
 ("function mark(val){const k=vk(),id=item().id;V[k]=V[k]||{};V[k][id]=val;save(k,id,val);",
  "function mark(val){const k=vk(),id=item().id;V[k]=V[k]||{};if(val==='y'&&V[k][id]==='y'){V[k][id]='s';save(k,id,'s');paint();return}if(val==='s'){if(!V[k][id]){V[k][id]='s';save(k,id,'s')}step(1);return}V[k][id]=val;save(k,id,val);"),
 # swipe either way = next (yes only via the check)
 ("if(dx>80)mark('y');else if(dx<-80)mark('n');", "if(dx>80||dx<-80){c.style.transform='';mark('s')}"),
 # keys: right = next, left = back
 ("if(e.key==='ArrowRight')mark('y');if(e.key==='ArrowLeft')mark('n');", "if(e.key==='ArrowRight')mark('s');if(e.key==='ArrowLeft')step(-1);if(e.key==='Enter'||e.key===' ')mark('y');"),
 # buttons: no X; skip records seen
 ("$('no').onclick=()=>mark('n');$('skip').onclick=()=>step(1);", "$('no').style.display='none';$('skip').onclick=()=>mark('s');"),
 ('<button class="big s" id="skip" title="Skip">→</button>', '<button class="big s" id="skip" title="Next" style="width:72px;height:72px;font-size:30px">→</button>'),
 # foot text
 ("Swipe right = yes · left = no · pinch or double-tap to zoom", "Tap ✓ for a yes · arrow or swipe = next (not a yes) · pinch or double-tap to zoom"),
 # summary counts: yeses of seen
 ("$('fsum').innerHTML='<b>'+y+'</b> yes · <b>'+n+'</b> no'+(tot?' · '+(y+n)+' of '+tot+' seen':'')",
  "$('fsum').innerHTML='<b>'+y+'</b> yeses of <b>'+(y+n)+'</b> seen'+(tot?' (of '+tot+' mats)':'')"),
]
for a, b in R:
    c = t.count(a)
    assert c >= 1, 'missing: ' + a[:70]
    t = t.replace(a, b)
# count 's' and 'n' as seen-not-yes in both counters
t = t.replace("if(v==='y')y++;else if(v==='n')n++", "if(v==='y')y++;else if(v==='n'||v==='s')n++")
# stamp: 's' shows nothing
t = t.replace("s.className='stamp'+(v==='y'?' y':v==='n'?' n':'');s.textContent=v==='y'?'✓ Yes':v==='n'?'✕ No':'';",
              "s.className='stamp'+(v==='y'?' y':'');s.textContent=v==='y'?'✓ Yes':'';")
open(sys.argv[2], 'w').write(t)
print('ok')
