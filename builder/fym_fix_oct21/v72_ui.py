"""FYM v72 (built from live v71). Usage: python3 builder/fym_fix_oct21/v72_ui.py <build_dir>
v71 QA follow-ups:
 - mat-door headline carries (TM) (each door's title is that screen's most prominent use)
 - fast swipes are queued (no swipe lost when two land < 300ms apart); a swipe never counts as half of a double-tap zoom
 - Yellow Mountain Ivory Pinstripe / Ridge / Stripes: each gets its own brand image (they shared one photo)
 - tile photo in "Take them home" fills its square (Heritage 1.0 showed white bars: object-fit contain on a portrait photo)
 - "Blue Editon" -> "Blue Edition"
 - deck tab ("Browsing racks" / "Your mat") no longer sits on the card's pill (pills move below the tab)
Optional first-run tour (Tiffany 6:37/6:38pm): "Want a quick tour of Find Your Mat-ch? (30 sec)" Yes / Skip on first open; coach
marks make her do each motion (swipe right, swipe left, Back, picks toggle, a colour, shortlist + Next); Mac-dock bounce on the next
thing to touch (soft glow with prefers-reduced-motion); "Take the tour" link near the top; done flag stored so it never repeats.
One-time hints outside the tour (2 hops, once each, remembered): Back after the first left swipe, the picks toggle on the first card,
the colour chips after ~5 swipes, Next: add racks when the shortlist gets its first heart."""
import sys, os, io, json, base64, hashlib
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'
h = open(P).read()
h = h.replace('Blue Editon', 'Blue Edition')
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
# ---- Ivory sets: own brand image each (full + pile)
IV = {'www.ymimports.com/fx-am022-a': 'ivory-pinstripe', 'www.ymimports.com/fx-am019-a': 'ivory-ridge', 'www.ymimports.com/fx-am014-a': 'ivory-stripes'}
IMGS = {}
os.makedirs(os.path.join(B, 't72'), exist_ok=True)
for tk, n in IV.items():
    if tk not in D['tiles']: continue
    src = f'assets/tiles/catalog-better/yellow-mountain-imports-{n}.jpg'
    im = Image.open(REPO + src).convert('RGB'); full = im.copy(); full.thumbnail((1000, 1000)); fn = f't72/{n}.jpg'; full.save(os.path.join(B, fn), quality=88)
    w, hh = im.size; q = min(w, hh); pp = im.crop(((w - q) // 2, (hh - q) // 2, (w - q) // 2 + q, (hh - q) // 2 + q)).resize((360, 360), Image.LANCZOS)
    b = io.BytesIO(); pp.save(b, 'JPEG', quality=84); pk = 'p72' + hashlib.md5(n.encode()).hexdigest()[:10]
    IMGS[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    D['tiles'][tk].update(full=fn, pile=pk, src=src)
open(os.path.join(B, 'b22v1.js'), 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMGS) + ');')
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if 'b22v1.js' not in h: h = h.replace('<script src="b21v1.js"></script>', '<script src="b21v1.js"></script><script src="b22v1.js"></script>', 1)
i = h.index('const D=') + 8; _, end = json.JSONDecoder().raw_decode(h[i:]); end += i
H, data, t = h[:i], h[i:end], h[end:]
def rep(s, a, b):
    assert s.count(a) == 1, (s.count(a), a[:90]); return s.replace(a, b)

H = rep(H, ".nw{white-space:nowrap}\n</style>", """.nw{white-space:nowrap}
/* v72: tab never covers the card pills; tile photo fills its square in Take them home */
.deck:has(.peekbar) .scard .hb,.deck:has(.peekbar) .scard .zb{top:34px}.deck:has(.peekbar) .scard .aw{top:64px}
.si img.tcv{object-fit:cover;border-radius:10px}
/* v72: tour + one-time hints. Mac-dock bounce; soft glow when reduced motion is on */
@keyframes dock{0%,100%{transform:translateY(0)}18%{transform:translateY(-16px)}36%{transform:translateY(0)}54%{transform:translateY(-8px)}72%{transform:translateY(0)}}
@keyframes glow{0%,100%{box-shadow:0 0 0 0 rgba(200,50,95,0)}50%{box-shadow:0 0 0 5px rgba(200,50,95,.35),0 0 18px rgba(200,50,95,.45)}}
.bnc{animation:dock 1.15s ease-in-out infinite;position:relative;z-index:61}
.bnc1{animation:dock 1.15s ease-in-out 1}
@media (prefers-reduced-motion:reduce){.bnc{animation:glow 1.6s ease-in-out infinite}.bnc1{animation:glow 1.6s ease-in-out 1}}
.tourq .box{text-align:center}.tourq .box p{margin:0 0 14px}
.coach{position:fixed;left:12px;right:12px;max-width:420px;margin:0 auto;z-index:70;pointer-events:none;background:var(--navy);color:#fff;border-radius:16px;padding:12px 14px;box-shadow:0 12px 30px rgba(5,70,137,.35);font:600 14.5px/1.35 var(--body)}
.coach b{font:400 18px 'Alfa Slab One',Georgia,serif;display:block;margin-bottom:2px}
.coach .cr{display:flex;justify-content:space-between;align-items:center;margin-top:8px;font-size:12px;opacity:.9}
.coach button{pointer-events:auto;border:0;border-radius:999px;background:#fff;color:var(--navy);font:700 12.5px var(--body);padding:6px 12px;cursor:pointer}
.coach button.sk{background:transparent;color:#fbe3ec;text-decoration:underline;padding:6px 0}
</style>""")
# (TM) on the mat-door headline too
t = rep(t, '<h1 class="ttl">Find Your Mat-ch</h1>', '<h1 class="ttl">Find Your Mat-ch™</h1>')
# fast swipes: the flying card is a detached copy and the next card is live at once (no lock, nothing dropped)
_fa = t.index("function fly(k,yes){"); _fb = t.index("\n", _fa)
t = t[:_fa] + "/* v72: the flying card is a detached copy; the next card is live at once, so fast swipes and taps are never dropped */\nfunction fly(k,yes){const c=$('top-'+k);if(!c||!queue(k).length||(k==='m'&&(S.peek||matLocked())))return;const r=c.getBoundingClientRect(),g=c.cloneNode(true);g.removeAttribute('id');Object.assign(g.style,{position:'fixed',left:r.left+'px',top:r.top+'px',width:r.width+'px',height:r.height+'px',margin:'0',zIndex:'55',pointerEvents:'none',transition:'none',transform:c.style.transform||''});document.body.appendChild(g);const s=g.querySelector('.stamp.'+(yes?'yes':'no'));if(s)s.style.opacity=1;decide(k,yes);requestAnimationFrame(()=>{g.style.transition='transform .22s ease-in, opacity .22s';g.style.transform=`translateX(${yes?150:-150}%) rotate(${yes?18:-18}deg)`;g.style.opacity='.5';});setTimeout(()=>g.remove(),280);}" + t[_fb:]
# double-tap zoom only from two TAPS (a fast second swipe is not a double tap)
t = rep(t, "const n=Date.now();if(opt.zoom!==false&&n-last<280){zoomAt(z.s>1?1:2.4,e.clientX,e.clientY,true);st=null;last=0;}else last=n;",
        "const n=Date.now();if(opt.zoom!==false&&n-last<280){zoomAt(z.s>1?1:2.4,e.clientX,e.clientY,true);st=null;last=0;}")
t = rep(t, "const up=e=>{if(!pts.has(e.pointerId))return;pts.delete(e.pointerId);",
        "const up=e=>{if(!pts.has(e.pointerId))return;pts.delete(e.pointerId);last=(st&&lock===null&&!pinch)?Date.now():0;")
# Take them home: tile photo fills the square
t = rep(t, "return `<div class=\"si\"><img src=\"${im}\" alt=\"\">", "return `<div class=\"si\"><img src=\"${im}\" alt=\"\" class=\"${T[id]?'tcv':''}\">")
# Take the tour links
t = rep(t, "const flowRow=()=>`<div class=\"frow2\"><ol class=\"flow\" id=\"flow\" aria-label=\"Your steps\">${flowHTML()}</ol><button type=\"button\" class=\"solink\" data-startover>Start over</button></div>`;",
        "const flowRow=()=>`<div class=\"frow2\"><ol class=\"flow\" id=\"flow\" aria-label=\"Your steps\">${flowHTML()}</ol><span><button type=\"button\" class=\"solink\" data-tour>Take the tour</button> <button type=\"button\" class=\"solink\" data-startover>Start over</button></span></div>`;")
t = rep(t, "<div class=\"how\"><div><b>1</b>Swipe on mats</div>", "<button type=\"button\" class=\"solink\" data-tour style=\"display:block;margin:-4px auto 2px\">Take the 30-second tour</button><div class=\"how\"><div><b>1</b>Swipe on mats</div>")
# event hooks for the tour + hints
t = rep(t, "function undo(k){", "function undo(k){tourEv('back');")
t = rep(t, "if(b=q('[data-her]')){const f=S.f[b.dataset.her];f.her=!f.her;rerender(b.dataset.her);return;}",
        "if(b=q('[data-her]')){const f=S.f[b.dataset.her];f.her=!f.her;rerender(b.dataset.her);tourEv('her');return;}")
t = rep(t, "if((b=q('.frow [data-fam]'))||(b=q('[data-fam=\"holiday\"]'))){const f=S.f[b.dataset.k];f.fam=TOG(f.fam,b.dataset.fam);rerender(b.dataset.k);return;}",
        "if((b=q('.frow [data-fam]'))||(b=q('[data-fam=\"holiday\"]'))){const f=S.f[b.dataset.k];f.fam=TOG(f.fam,b.dataset.fam);rerender(b.dataset.k);tourEv('fam');return;}\n if(q('[data-tour]')){tourStart();return;}\n if(q('[data-tq-yes]')){const d=$('tourq');if(d)d.remove();tourStart();return;}\n if(q('[data-tq-no]')){const d=$('tourq');if(d)d.remove();TOUR.prompt=false;LS.set('fym_tour','skipped');return;}\n if(q('[data-tour-next]')){tourNext();return;}\n if(q('[data-tour-skip]')){tourEnd(true);return;}")
t = rep(t, "renderAll();\n(function(){const L=window.__LAZY", r"""/* ---------- v72: optional first-run tour + one-time hints ---------- */
const LS={get(k){try{return localStorage.getItem(k);}catch(e){return null;}},set(k,v){try{localStorage.setItem(k,v);}catch(e){}}};
const TOUR={on:false,step:0,prompt:false};
const TSTEPS=[
 {ev:'yes',t:'Swipe right to love it ♥',p:'Or tap the heart. Loved mats wait in your shortlist.',b:'[data-yes="m"]',a:'#top-m'},
 {ev:'no',t:'Swipe left: not the one',p:'Or tap ✕ and the next mat steps up.',b:'[data-no="m"]',a:'#top-m'},
 {ev:'back',t:'Tap ← Back to bring one back',p:'Swiped too fast? Back brings the last mat back.',b:'[data-back="m"]',a:'[data-back="m"]'},
 {ev:'her',t:'Tiffany’s matches or all mats',p:'Tap to switch between my picks and every mat. Watch the deck change.',b:'.frow [data-her="m"]',a:'.frow',skip:()=>!document.querySelector('.frow [data-her="m"]')},
 {ev:'fam',t:'Pick a color',p:'Tap a color to see mats with it. Tap it again to clear it.',b:'.frow .dot[data-fam]:not([data-fam=""])',a:'.frow',skip:()=>!document.querySelector('.frow .dot[data-fam]:not([data-fam=""])')},
 {ev:'next',t:'Your shortlist & Mock up',p:'Every mat you ♥ waits here. When you’re ready, tap Next: add racks to mock up your match.',b:'.tray .go,.tray',a:'.tray'}];
function tourDemo(){if(S.set!=null)return true;const i=D.sets.findIndex(s=>s.slug==='oh-my-mahjong-papaya-spritz'&&VIS(s));const j=i>=0?i:D.sets.findIndex(s=>VIS(s)&&s.m.length);if(j<0)return false;S.door='tiles';resetFrom(1);S.set=j;S.f.m.her=set().m.length>0;S.tilesOpen=false;renderAll();return true;}
function tourStart(){const d=$('tourq');if(d)d.remove();TOUR.prompt=false;if(S.door==='mat'&&matLocked()){S.ddeck=true;S.peek=null;}if(!tourDemo())return;S.peek=null;TOUR.on=true;TOUR.step=0;renderMats();jump('s-mats');setTimeout(tourPaint,450);}
function tourEnd(skipped){TOUR.on=false;LS.set('fym_tour',skipped?'skipped':'done');document.querySelectorAll('.bnc').forEach(e=>e.classList.remove('bnc'));const c=$('coach');if(c)c.remove();}
function tourNext(){TOUR.step++;while(TOUR.step<TSTEPS.length&&TSTEPS[TOUR.step].skip&&TSTEPS[TOUR.step].skip())TOUR.step++;if(TOUR.step>=TSTEPS.length){tourEnd(false);toast('That’s it. Happy matching ♥');return;}tourPaint();}
function tourEv(ev){if(!TOUR.on)return;const s=TSTEPS[TOUR.step];if(s&&s.ev===ev)setTimeout(tourNext,260);}
function tourPaint(){document.querySelectorAll('.bnc').forEach(e=>e.classList.remove('bnc'));let c=$('coach');if(!TOUR.on){if(c)c.remove();return;}const s=TSTEPS[TOUR.step];if(s.skip&&s.skip()){tourNext();return;}
 const b=s.b.split(',').map(x=>document.querySelector(x)).find(Boolean);if(b)b.classList.add('bnc');
 if(!c){c=document.createElement('div');c.id='coach';c.className='coach';c.setAttribute('role','dialog');c.setAttribute('aria-live','polite');document.body.appendChild(c);}
 c.innerHTML=`<b>${s.t}</b>${s.p}<div class="cr"><span>${TOUR.step+1} of ${TSTEPS.length}</span><span><button type="button" class="sk" data-tour-skip>Skip tour</button> ${s.ev==='next'?'<button type="button" data-tour-next>Done ♥</button>':''}</span></div>`;
 coachPlace(c,b);}
/* v72b: the bubble never covers its target. Scroll a chip row so the target is fully visible, bring the target on screen
   leaving room for the bubble, then put the bubble right above it (or below if there is no room) and next to it horizontally. */
function coachRect(){const c=$('coach'),b=TOUR.on&&TSTEPS[TOUR.step]&&TSTEPS[TOUR.step].b.split(',').map(x=>document.querySelector(x)).find(Boolean);if(!c||!b)return null;const r=c.getBoundingClientRect(),q=b.getBoundingClientRect();return {c:[r.left,r.top,r.right,r.bottom],b:[q.left,q.top,q.right,q.bottom]};}
function coachPlace(c,b){const vw=document.documentElement.clientWidth||innerWidth||390,vh=innerHeight||800,G=10,TOPS=64;
 const w=Math.min(420,vw-24);c.style.width=w+'px';c.style.right='auto';c.style.margin='0';c.style.top='0px';c.style.bottom='';
 if(!b){c.style.left=Math.round((vw-w)/2)+'px';c.style.top=TOPS+'px';return;}
 let p=b.parentElement;while(p&&p!==document.body&&!(p.scrollWidth>p.clientWidth+1&&/(auto|scroll)/.test(getComputedStyle(p).overflowX)))p=p.parentElement;
 if(p&&p!==document.body){const pr=p.getBoundingClientRect(),br=b.getBoundingClientRect();if(br.left<pr.left+4||br.right>pr.right-4)p.scrollLeft+=(br.left+br.width/2)-(pr.left+pr.width/2);}
 const h=c.offsetHeight;let r=b.getBoundingClientRect();
 const fitsAbove=r.top-G-h>=TOPS,fitsBelow=r.bottom+G+h<=vh-G;
 if(!fitsAbove&&!fitsBelow){/* scroll so the target sits low enough to have the bubble above it */const want=TOPS+h+G+8;window.scrollBy({top:r.top-want,left:0,behavior:'instant'});r=b.getBoundingClientRect();}
 else if(r.top<TOPS||r.bottom>vh){b.scrollIntoView({block:'center',behavior:'instant'});r=b.getBoundingClientRect();}
 let top=(r.top-G-h>=TOPS)?r.top-G-h:(r.bottom+G+h<=vh-G?r.bottom+G:Math.max(TOPS,r.top-G-h));
 const cx=r.left+r.width/2;let left=Math.max(12,Math.min(vw-w-12,cx-w/2));
 c.style.top=Math.round(top)+'px';c.style.left=Math.round(left)+'px';}
addEventListener('resize',()=>{if(TOUR.on)tourPaint();});
const HS=(()=>{try{return JSON.parse(LS.get('fym_hints')||'{}')||{};}catch(e){return {};}})();
function hint(id,sel){if(TOUR.on||TOUR.prompt||HS[id])return;requestAnimationFrame(()=>{const e=document.querySelector(sel);if(!e)return;HS[id]=1;LS.set('fym_hints',JSON.stringify(HS));e.classList.add('bnc1');setTimeout(()=>e.classList.remove('bnc1'),1700);});}
{const _rm=renderMats;renderMats=function(){_rm();if(TOUR.on)setTimeout(tourPaint,30);else if(S.set!=null&&!matLocked()&&queue('m').length)hint('picks','.frow [data-her="m"]');};
 const _dc=decide;decide=function(k,yes){_dc(k,yes);if(k!=='m')return;tourEv(yes?'yes':'no');if(!yes)hint('back','[data-back="m"]');if(yes&&S.liked.length===1)hint('mock','.tray .go');if(S.hist.length>=5)hint('colors','.frow .dot[data-fam]:not([data-fam=""])');};}
function tourOffer(){if(LS.get('fym_tour')||TOUR.on||$('tourq'))return;TOUR.prompt=true;const d=document.createElement('div');d.className='sheet tourq';d.id='tourq';d.innerHTML=`<div class="box"><h3>Want a quick tour?</h3><p>See how Find Your Mat-ch works in about 30 seconds. You’ll try each move yourself.</p><div class="dacts"><button type="button" class="big" data-tq-yes>Yes, show me ♥</button><button type="button" class="big gh" data-tq-no>Skip</button></div></div>`;d.addEventListener('click',e=>{if(e.target===d){d.remove();TOUR.prompt=false;LS.set('fym_tour','skipped');}});document.body.appendChild(d);}
setTimeout(()=>{if(S.set==null)tourOffer();},1200);
renderAll();
(function(){const L=window.__LAZY""")
open(P, 'w').write(H + data + t)
print('v72 patched; ivory piles', list(IMGS))
