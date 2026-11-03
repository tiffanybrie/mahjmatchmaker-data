"""v114: 'Text or email me this list' must never end silently (Tiffany Nov 3 2:27pm; repro scratchpad sharebug/NOTES.txt: inside the
site iframe navigator.share is undefined -> window.open(mailto) with no mail handler = nothing; on iPhone a NotAllowedError fell to
window.open AFTER the await, popup blocked = nothing; no clipboard fallback anywhere).
New handler: FIRST (no await before it) copy the list (navigator.clipboard.writeText, textarea + execCommand fallback) and show a
toast 'Copied! Paste it into a text or email'; THEN try navigator.share; if share is missing or throws anything but AbortError,
open a small sheet: Email (mailto:?subject&body) and Text (sms:&body=) links + the list in a read-only textarea. Gate [149].
Idempotent. Usage: python3 share114.py <build dir or index.html>"""
import sys, os
P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html'); h = open(P).read()
if '/*v114 shoplist*/' in h: print('share114 already'); sys.exit()
a = """document.addEventListener('click',async e=>{if(!(e.target.closest&&e.target.closest('[data-shoplist]')))return;const t=shopText();trk('shoplist',{mat:S.fav});if(navigator.share){try{await navigator.share({title:'My mahjong match',text:t});return;}catch(x){if(x&&x.name==='AbortError')return;}}const u='mailto:?subject='+encodeURIComponent('My mahjong match')+'&body='+encodeURIComponent(t);try{window.open(u,'_blank')||(location.href=u);}catch(x){location.href=u;}});"""
assert h.count(a) == 1, h.count(a)
b = r"""/*v114 shoplist*/function SLexec(t){try{const a=document.createElement('textarea');a.value=t;a.setAttribute('readonly','');a.style.cssText='position:fixed;top:-1000px;left:0;opacity:0';document.body.appendChild(a);a.focus();a.select();try{a.setSelectionRange(0,t.length)}catch(_){}const r=document.execCommand('copy');a.remove();return !!r}catch(x){return false}}
function SLcopy(t){let ok=false;try{if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).catch(()=>SLexec(t));ok=true}}catch(x){}return ok||SLexec(t)}
function SLtoast(m){let el=document.getElementById('sltoast');if(!el){el=document.createElement('div');el.id='sltoast';el.setAttribute('role','status');el.setAttribute('aria-live','polite');document.body.appendChild(el)}el.textContent=m;el.hidden=false;clearTimeout(SLtoast.t);SLtoast.t=setTimeout(()=>{el.hidden=true},4000)}
function SLsheet(t){let el=document.getElementById('slsheet');if(el)el.remove();el=document.createElement('div');el.id='slsheet';el.setAttribute('role','dialog');el.setAttribute('aria-label','Send yourself this list');
 const sub=encodeURIComponent('My mahjong match'),body=encodeURIComponent(t);
 el.innerHTML=`<div class="slbox"><button type="button" class="slx" aria-label="Close">×</button><h3>Send yourself this list</h3><p>It’s copied, so you can paste it anywhere. Or tap:</p><div class="slbtns"><a class="big" href="mailto:?subject=${sub}&body=${body}" target="_blank" rel="noopener">Email</a><a class="big gh" href="sms:&body=${body}">Text</a></div><textarea readonly rows="7" aria-label="Your list"></textarea></div>`;
 el.querySelector('textarea').value=t;el.addEventListener('click',x=>{if(x.target===el||x.target.closest('.slx'))el.remove()});document.body.appendChild(el);return el}
document.addEventListener('click',e=>{if(!(e.target.closest&&e.target.closest('[data-shoplist]')))return;const t=shopText();try{trk('shoplist',{mat:S.fav})}catch(_){}
 const ok=SLcopy(t);SLtoast(ok?'Copied! Paste it into a text or email':'Tap Email or Text to send this list');
 let sh=null;try{sh=navigator.share?navigator.share({title:'My mahjong match',text:t}):null}catch(x){sh=Promise.reject(x)}
 if(!sh){SLsheet(t);return}Promise.resolve(sh).catch(x=>{if(!(x&&x.name==='AbortError'))SLsheet(t)});});"""
h = h.replace(a, b)
css = """#sltoast{position:fixed;left:50%;bottom:calc(24px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);z-index:450;background:#2a2036;color:#fff;border-radius:16px;padding:10px 16px;font:600 14px/1.35 var(--body);max-width:calc(100vw - 32px);text-align:center;box-shadow:0 8px 24px rgba(0,0,0,.25)}#sltoast[hidden]{display:none}
#slsheet{position:fixed;inset:0;z-index:440;background:rgba(20,10,30,.45);display:flex;align-items:flex-end;justify-content:center}
#slsheet .slbox{position:relative;background:#fff;border-radius:18px 18px 0 0;width:min(560px,100%);padding:16px 16px calc(18px + env(safe-area-inset-bottom,0px));display:flex;flex-direction:column;gap:10px;font:14px/1.4 var(--body);color:#2a2036}
#slsheet h3{margin:0;font:400 20px/1.15 var(--display,serif);color:var(--navy,#054689)}#slsheet p{margin:0;color:#76687f}
#slsheet .slbtns{display:flex;gap:10px}#slsheet .slbtns a{flex:1;text-align:center;text-decoration:none}
#slsheet textarea{width:100%;box-sizing:border-box;border:1px solid #ecd5df;border-radius:10px;padding:8px;font:13px/1.4 var(--body);resize:none}
#slsheet .slx{position:absolute;top:8px;right:10px;border:0;background:none;font-size:26px;line-height:1;color:#76687f;cursor:pointer}
@media (min-width:700px){#slsheet{align-items:center}#slsheet .slbox{border-radius:18px}}"""
h = h.replace('</style>', css + '</style>', 1)
open(P, 'w').write(h); print('share114 ok')
