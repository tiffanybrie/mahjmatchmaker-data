"""Add a 'Done' button + finish sheet to a swipe book (Tiffany, Oct 13).
At the end of the book (or any time via the top ✓ button) she sees her yes/no counts,
can leave a note, tap 'Mark done', and jump back to HQ. Saves to collection <col>_status, doc 'done'.
Usage: python3 finish_patch.py in.html out.html"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def _canon(p):
    # Tiffany Oct 15: canonical Heritage 1.0 / 2.0, Sunday and Spring Fling photos, every build
    from canon_tiles import fix_book
    fix_book(p)
HQ='https://claude.ai/artifact/Cor6pKtesou4mFRQ41P6Ye'
t=open(sys.argv[1]).read()
if 'id="fsheet"' in t:
    open(sys.argv[2],'w').write(t);print('already patched')
    _canon(sys.argv[2]);sys.exit()
a='<button class="nav" id="nextGroup" title="Next">⏭</button>'
assert a in t
t=t.replace(a,a+'<button class="nav" id="finBtn" title="I\'m done" style="background:#2e9d5e">✓</button>',1)
sheet=('<div class="sheet" id="fsheet"><div class="hd"><span style="flex:1">All done?</span><button class="nav" id="fX">✕</button></div>'
 '<div style="padding:16px;display:flex;flex-direction:column;gap:12px;max-width:520px;margin:0 auto;width:100%">'
 '<div id="fsum" style="font-size:16px;line-height:1.5"></div>'
 '<textarea id="fnote" rows="3" placeholder="Anything for Claude? (optional)" style="width:100%;box-sizing:border-box;border-radius:12px;border:1px solid #ccc;padding:10px;font:inherit;font-size:16px"></textarea>'
 '<button id="fDone" class="zoom" style="position:static;background:#2e9d5e;color:#fff;padding:14px 18px;font-size:16px;font-weight:700">✓ Mark this done</button>'
 '<a id="fHQ" href="'+HQ+'" target="_top" class="zoom" style="position:static;display:block;text-align:center;text-decoration:none;background:rgba(255,255,255,.16);color:#fff;padding:12px 18px;font-size:15px">← Back to my HQ list</a>'
 '<button id="fKeep" class="zoom" style="position:static;background:transparent;color:#cfc8d6;padding:8px">Keep swiping</button>'
 '<div id="fst" style="font-size:13px;color:#9fd9b4;text-align:center;min-height:18px"></div></div></div>')
b='<div class="sheet" id="nsheet">'
assert b in t
t=t.replace(b,sheet+b,1)
js=r'''
<script>
(function(){const SC=COL+'_status';let FD=null;
function fsum(){let y=0,n=0;Object.values(V).forEach(o=>Object.values(o||{}).forEach(v=>{if(v==='y')y++;else if(v==='n')n++}));
 const tot=(D.items||[]).length*((D.groups||[]).length||1);
 $('fsum').innerHTML='<b>'+y+'</b> yes · <b>'+n+'</b> no'+(tot?' · '+(y+n)+' of '+tot+' seen':'')+(FD&&FD.done?'<br><span style="color:#9fd9b4">Marked done '+new Date(FD.at).toLocaleString()+'</span>':'');
 $('fDone').textContent=FD&&FD.done?'✓ Done (tap to update note)':'✓ Mark this done'}
window.openFin=function(){fsum();if(FD&&FD.note)$('fnote').value=FD.note;$('fsheet').classList.add('on')};
$('finBtn').onclick=openFin;$('fX').onclick=$('fKeep').onclick=()=>$('fsheet').classList.remove('on');
$('fDone').onclick=async()=>{if(!db){$('fst').textContent='Sign in to claude.ai so this saves.';return}
 let y=0,n=0;Object.values(V).forEach(o=>Object.values(o||{}).forEach(v=>{if(v==='y')y++;else if(v==='n')n++}));
 const x={done:true,note:$('fnote').value.trim(),yes:y,no:n,at:new Date().toISOString()};
 for(let k=0;k<4;k++){try{await db.collection(SC).doc('done').set(x);FD=x;fsum();$('fst').textContent='Saved ✓ Claude will pick this up. Tap "Back to my HQ list" when you\'re ready.';return}catch(e){await new Promise(r=>setTimeout(r,700))}}
 $('fst').textContent='Couldn’t save. Tap again.'};
const ft=$('foot');new MutationObserver(()=>{if(/All done/.test(ft.textContent))openFin()}).observe(ft,{childList:true,characterData:true,subtree:true});
(async function w(){for(let k=0;k<40&&!db;k++)await new Promise(r=>setTimeout(r,250));if(!db)return;try{const q=await db.collection(SC).limit(10).get();q.docs.forEach(d=>{if(d.id==='done')FD=d.data()})}catch(e){}})();
})();
</script>'''
i=t.rfind('</body>')
t=(t[:i]+js+t[i:]) if i>=0 else t+js
open(sys.argv[2],'w').write(t);print('patched')
_canon(sys.argv[2])
# Oct 18 (Tiffany): yes-only swiping. Arrows/swipes = next, only the check records a yes; not-yes = no.
import subprocess as _sp, os as _os
_sp.run(['python3', _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'yes_only_patch.py'), sys.argv[2], sys.argv[2]], check=True)
