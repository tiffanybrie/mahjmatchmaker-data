"""Oct 17: anonymous event counting hooks for Find Your Match (Ready to Ship d-tracking = ok).
Events are batched and sent with navigator.sendBeacon to Tiffany's Google Apps Script web app (TRK_URL).
While TRK_URL is empty, nothing leaves the page. No names, emails or IPs; a random per-visit id only.
Usage: python3 fym_track_oct17.py <in index.html> <out index.html> [TRK_URL]"""
import sys
src, out = sys.argv[1:3]
url = sys.argv[3] if len(sys.argv) > 3 else ''
t = open(src).read()
if 'const TRK_URL=' in t:
    import re
    t = re.sub(r"const TRK_URL='[^']*';", f"const TRK_URL='{url}';", t, count=1)
    open(out, 'w').write(t); print('url updated'); sys.exit()
JS = r"""
const TRK_URL='__URL__';const TRK={q:[],sid:Math.random().toString(36).slice(2,10)};
function trk(t,o){if(!TRK_URL)return;o=o||{};TRK.q.push({t,set:o.set!=null?o.set:(S.set!=null?set().slug:''),mat:o.mat||'',rack:o.rack||'',x:o.x||'',sid:TRK.sid});if(TRK.q.length>=15)trkFlush();}
function trkFlush(){if(!TRK_URL||!TRK.q.length)return;const b=JSON.stringify({events:TRK.q.splice(0,50)});try{navigator.sendBeacon(TRK_URL,new Blob([b],{type:'text/plain'}));}catch(e){}}
document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')trkFlush();});setInterval(trkFlush,20000);
document.addEventListener('click',e=>{const a=e.target.closest&&e.target.closest('a.go,a.dc,.si a');if(!a)return;const si=a.closest('.si');trk(a.classList.contains('dc')?'code':'shop',{x:(si&&si.querySelector('b')?si.querySelector('b').textContent:'')+' | '+(a.getAttribute('href')||'').split('?')[0].slice(0,90)});},true);
let trkSearchT=null;document.addEventListener('input',e=>{if(!/^(tsq|msq|rsq|mdq)$/.test(e.target.id))return;clearTimeout(trkSearchT);const v=e.target.value.trim();trkSearchT=setTimeout(()=>{if(v.length>2)trk('search',{x:e.target.id+':'+v.slice(0,60)});},1500);});
"""
JS = JS.replace('__URL__', url)
anchor = "function decide(k,yes){const q=queue(k);if(!q.length)return;const id=q[0];"
assert anchor in t
t = t.replace(anchor, JS + anchor + "\n trk(yes?'right':'left',k==='m'?{mat:id}:{mat:S.fav,rack:id});", 1)
a2 = "async function share(){if(!cardURL)return;"
assert a2 in t
t = t.replace(a2, a2 + "trk('save',{mat:S.fav,rack:S.rpick.join(' + '),x:S.fmt});", 1)
a3 = "if(b=q('[data-tile]')){const i=+b.dataset.tile;"
assert a3 in t
t = t.replace(a3, a3 + "trk('tiles',{set:D.sets[i].slug});", 1)
a4 = "if(b=q('[data-dmat]')){S.dmat=b.dataset.dmat;"
if a4 in t: t = t.replace(a4, a4 + "trk('matdoor',{set:'',mat:S.dmat});", 1)
a5 = "if(q('[data-make]')){if(!S.rpick.length)return;"
assert a5 in t
t = t.replace(a5, a5 + "trk('card',{mat:S.fav,rack:S.rpick.join(' + ')});", 1)
open(out, 'w').write(t)
print('patched', len(t))
