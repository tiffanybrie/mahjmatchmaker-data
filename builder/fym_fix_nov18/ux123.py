"""FYM 1.23 LAYOUT PREVIEW (Tiffany Nov 18 feedback). NOT LIVE: never point site-app/live.json at this build.

Takes the live website build (site-app/fym-v122/index.html @89b4dc07, Version 1.22) and changes ONLY the experience
(layout / UI / JS / CSS / wording). const D (all data) is untouched; the script asserts that.

Her changes (Nov 18):
 1  X / heart buttons move BELOW the photo (no more side buttons over it); Table and Aerial photos fill the card width
    (no 100dvh cap on a phone, no inner padding). Swipe right = a big heart pops over the photo, left = an X.
 2  Up close stays as it is (tiles next to the mat); only its buttons move under the photo.
 3  View order: Up close, Table, Aerial.
 4  The view buttons pulse for ~8s the first time the pairing step shows (once per session; a tap stops it).
 5  Shortlist ("Pick your mat"): big cards, 2 per row on a phone; a tap shows THAT mat in the big view in the current
    mode, marks it, and scrolls the big view into sight. Swiping more mats still works.
 6  Racks in the SAME frame: picking a mat keeps the big view (current mode) with suggested racks on it; a pulsing
    "Choose your racks" button opens large rack choices right under it; a tap puts the rack on the mat live
    (Table view draws your 1st rack N/S and 2nd rack E/W). No separate small-mat rack screen.
 7  Finish button says what is missing ("Pick your racks to finish") until a rack is picked, then "Make it official".
    Guided pulse: view modes -> pick your mat -> choose your racks -> finish.

Usage: python3 builder/fym_fix_nov18/ux123.py <v122 index.html> <out index.html>
       python3 builder/fym_fix_nov18/ux123.py <live artifact index.html> <out index.html> --artifact   (claude.ai preview copy)
"""
import sys, re, hashlib

SRC, OUT = sys.argv[1:3]
h = open(SRC, encoding='utf-8').read()


def data_block(x):
    i = x.index('const D={')
    j = x.index('\nconst IMG=window.IMG||{};', i)
    return x[i:j]


D0 = hashlib.sha256(data_block(h).encode()).hexdigest()


def rep(old, new, count=1):
    global h
    n = h.count(old)
    assert n == count, (n, old[:120])
    h = h.replace(old, new)


# ---- version label (footer + title) ----
# label: the website copy (base 1.22) is 'Version 1.23 layout preview'; the artifact copy (base = live artifact 1.18 index,
# --artifact) says which catalog it carries
ART = '--artifact' in sys.argv
m = re.search(r'<title>Find Your Mat-ch \(Version (1\.\d+(?:\.\d+)?)\)</title>', h); BASEV = m.group(1)
LAB = f'Version 1.23 layout preview (catalog of {BASEV})' if ART else 'Version 1.23 layout preview'
rep(f'<title>Find Your Mat-ch (Version {BASEV})</title>', '<title>Find Your Mat-ch 1.23 layout preview</title>' if ART else '<title>Find Your Mat-ch (Version 1.23 layout preview)</title>')
rep(f'>Version {BASEV}</small>', f'>{LAB}</small>')

# ---- 3. view order: Up close, Table, Aerial ----
rep('''<button type="button" data-mode="aerial" aria-pressed="${S.mode==='aerial'}">Aerial</button><button type="button" data-mode="table" aria-pressed="${S.mode==='table'}">Table <b style="color:#c8325f;font-size:9px;letter-spacing:.06em">NEW</b></button>''',
    '''<button type="button" data-mode="table" aria-pressed="${S.mode==='table'}">Table <b style="color:#c8325f;font-size:9px;letter-spacing:.06em">NEW</b></button><button type="button" data-mode="aerial" aria-pressed="${S.mode==='aerial'}">Aerial</button>''')

# ---- peek wording: the mat being shown from the shortlist ----
rep('''if(k==='m'&&S.peek)return `<div class="deck m"><div class="peekbar"><span>Your suitor</span>''',
    '''if(k==='m'&&S.peek)return `<div class="deck m"><div class="peekbar"><span>${S.rstage?'Your mat':'From your shortlist'}</span>''')
# no swipe-away of the chosen mat while racks are being picked
rep("ok:()=>!(k==='m'&&(S.peek||matLocked()))", "ok:()=>!(k==='m'&&(S.peek||S.rstage||matLocked()))")

# ---- tour steps follow the new layout ----
rep("p:'Up close, Aerial or Table: tap one, or Next to stay.'", "p:'Up close, Table or Aerial: tap one, or Next to stay.'")
rep("{k:'pick',t:'Pick your mat',p:'Tap your favorite in Suitors to add racks.',b:'.tray .th button',",
    "{k:'pick',t:'Pick your mat',p:'Tap a mat in your shortlist to see it with your tiles.',b:'.sgrid button',")
rep("{k:'add',t:'Add racks',p:'Tap Add racks once to go to the racks.',b:'.acts.pk [data-mock],.tray .go[data-mock],.dacts [data-mock],.tray .th button',done:()=>!!S.fav},",
    "{k:'add',t:'Choose your racks',p:'Tap Choose your racks.',b:'.acts.pk [data-mock],.dacts [data-mock],.sgrid button',done:()=>!!S.fav&&!!S.rstage},")
rep("{k:'racks',t:'Swipe the racks',p:'Same as the mats: ♥ if you love it, ✕ if it’s not the one.',b:'#top-r',hand:'r',done:()=>S.rliked.length>0||S.rpick.length>0},",
    "{k:'racks',t:'Choose your racks',p:'Tap Choose your racks to see the rack choices.',b:'[data-rchoose]',done:()=>!!S.rch||S.rpick.length>0},")
rep("{k:'rmenu',t:'Narrow the racks',p:'The menu below the racks shows one color or one type at a time.',b:'#s-racks .rctl',ring:true,next:'Next'},",
    "{k:'rmenu',t:'Narrow the racks',p:'The menu below the racks shows one color or one type at a time.',b:'#rch .rfil',ring:true,next:'Next',skip:()=>!S.rch},")
rep("{k:'rpick',t:'Pick 1 or 2 racks',p:'Tap a rack suitor to pick it (✓).',b:'#rtray .th button',done:()=>S.rpick.length>0},",
    "{k:'rpick',t:'Pick 1 or 2 racks',p:'Tap a rack to put it on your mat (✓).',b:'#rch .rgc',done:()=>S.rpick.length>0},")
rep("b:'#rtray [data-make]',done:()=>!!S.made}", "b:'#s-mats [data-make]',done:()=>!!S.made}")

# ---- Table view: the racks you picked go on the table (1st rack N/S, 2nd rack E/W) ----
rep("function pickRack(s,mat){if(TV.rack&&rackOK(TV.rack,s))return TV.rack;",
    "function pickRack(s,mat){if(S.rstage&&mat===S.fav){const p=(S.rpick||[]).find(k=>rackOK(k,s));if(p)return p}if(TV.rack&&rackOK(TV.rack,s))return TV.rack;")
rep("window.TVPICK=(slug,mat)=>{const s=D.sets.find(x=>x.slug===slug);return s?pickRack(s,mat):null};",
    "window.TVPICK=(slug,mat)=>{const s=D.sets.find(x=>x.slug===slug);return s?pickRack(s,mat):null};window.TVROK=(k,slug)=>{const s=D.sets.find(x=>x.slug===slug);return !!(s&&rackOK(k,s))};window.TVRWHY=(k,slug)=>{const s=D.sets.find(x=>x.slug===slug);return s?rackWhy(k,s):''};")
rep("async function render(mat,s,rack,corner,N){", "async function render(mat,s,rack,corner,N,rack2){")
rep("const [mi,ri,fi]=await Promise.all([(TVD.mo&&TVD.mo[mat]?Promise.resolve(TVD.mo[mat]):matFull(mat)).then(load),rackImg(rack),load(tileFull(s)||pile(s))]);",
    "const [mi,ri,fi,ri2]=await Promise.all([(TVD.mo&&TVD.mo[mat]?Promise.resolve(TVD.mo[mat]):matFull(mat)).then(load),rackImg(rack),load(tileFull(s)||pile(s)),rack2?rackImg(rack2):Promise.resolve(null)]);")
rep("const drawRacks=()=>{for(const p of place){c.save();c.translate(p.x+p.w/2,p.y+p.h/2);c.rotate(p.a);c.drawImage(ri,-L/2,-Dp/2,L,Dp);c.restore()}};",
    "const drawRacks=()=>{for(const p of place){c.save();c.translate(p.x+p.w/2,p.y+p.h/2);c.rotate(p.a);c.drawImage(ri2&&(p.sd==='E'||p.sd==='W')?ri2:ri,-L/2,-Dp/2,L,Dp);c.restore()}};")
rep("function tableURL(x,N){const key=[x.mat,x.s.slug,x.rack,x.corner?1:0,TV.walls,TV.faces,N].join('|');",
    "function tableURL(x,N){const key=[x.mat,x.s.slug,x.rack,x.rack2||'',x.corner?1:0,TV.walls,TV.faces,N].join('|');")
rep("const p=render(x.mat,x.s,x.rack,x.corner,N);cput(key,p,N>2000?3:36);return p}",
    "const p=render(x.mat,x.s,x.rack,x.corner,N,x.rack2);cput(key,p,N>2000?3:36);return p}")
rep("return {mat,s,cls,fixed:!!rack,rack:rack||pickRack(s,mat),corner:cls==='B'}}",
    "const r1=rack||pickRack(s,mat);const r2=!rack&&S.rstage&&mat===S.fav?((S.rpick||[]).filter(k=>rackOK(k,s)&&k!==r1)[0]||null):null;return {mat,s,cls,fixed:!!rack,rack:r1,rack2:r2,corner:cls==='B'}}")
rep("const N=cardN(card);const key=[x.mat,x.s.slug,x.rack,TV.walls,TV.faces].join('|');",
    "const N=cardN(card);const key=[x.mat,x.s.slug,x.rack,x.rack2||'',TV.walls,TV.faces].join('|');")

CSS = r'''<style>/* v123 layout preview (Tiffany Nov 18) */
.sbx{display:none!important}
.cmp+.acts,.cmp+.swhint+.acts,.cmp~.acts.uxmv{margin:10px 0 2px}
.acts.uxmv{padding-left:0;gap:28px}.acts.uxmv .no{width:58px;height:58px}.acts.uxmv .yes{width:66px;height:66px}
.swhint.uxmv{margin:4px 0 6px}
/* Table + Aerial: the photo fills the card width */
.cmp.aer .scard .ph{padding:0}.cmp.aer .scard .ph img.photo,.cmp.aer .scard .ph img.tvimg,.cmp.aer .scard .ph img.tkm{border-radius:0}
@media (max-width:560px){.deck.m,.cmp.aer .deck.m{min-height:200px}.cmp.aer .deck.m,.cmp.aer .deck.t.aer,.deck.t.aer{height:min(calc(100vw - 24px + 56px),560px)!important}}
/* swipe pop */
.uxpop{position:absolute;left:50%;top:42%;z-index:30;width:104px;height:104px;margin:-52px 0 0 -52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font:700 56px/1 var(--body);pointer-events:none;animation:uxpop .7s ease-out forwards;box-shadow:0 10px 28px rgba(0,0,0,.28)}
.uxpop.y{background:#c8325f;color:#fff}.uxpop.n{background:#fff;color:#5e5368}
@keyframes uxpop{0%{transform:scale(.4);opacity:0}22%{transform:scale(1.12);opacity:1}62%{transform:scale(1);opacity:1}100%{transform:scale(1.2);opacity:0}}
/* guided pulse */
@keyframes uxpl{0%,100%{box-shadow:0 0 0 0 rgba(200,50,95,.6)}55%{box-shadow:0 0 0 10px rgba(200,50,95,0)}}
.uxpl{animation:uxpl 1.5s ease-in-out infinite}
.seg.mode.uxpl{border-radius:999px;outline:2px solid #c8325f;outline-offset:2px}
.uxmh{flex-basis:100%;text-align:center;margin:2px 0 0;font:600 12.5px/1.3 var(--body);color:#c8325f}
@media (prefers-reduced-motion:reduce){.uxpl{animation:none;box-shadow:0 0 0 3px rgba(200,50,95,.5)}.uxpop{animation-duration:.01s}}
/* shortlist */
.sgw{margin:14px 0 6px;padding:14px 12px 12px;border-radius:18px;background:#fff5f8;border:1px solid #f3d3df}
.sgh{margin:0;font:400 24px/1.1 var(--display,Georgia,serif);color:var(--navy,#054689)}
.sgp{margin:4px 0 10px;font:600 14px/1.35 var(--body);color:#5b4e66}
.sgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
@media (min-width:700px){.sgrid{grid-template-columns:repeat(auto-fill,minmax(200px,1fr))}}
.sgc{border:2px solid #f0dbe4;background:#fff;border-radius:16px;padding:6px 6px 8px;text-align:left;cursor:pointer;display:flex;flex-direction:column;gap:3px;color:#2a2036;min-width:0}
.sgc .sgi{position:relative;display:block;aspect-ratio:1;border-radius:11px;overflow:hidden;background:#f6eff2}
.sgc .sgi img{width:100%;height:100%;object-fit:cover;display:block}
.sgc b{font:700 14px/1.2 var(--body);overflow-wrap:anywhere}.sgc small{font:12px/1.2 var(--body);color:#76687f}
.sgc.on{border-color:#c8325f;box-shadow:0 0 0 3px rgba(200,50,95,.22)}
.sgon{position:absolute;left:6px;top:6px;background:#c8325f;color:#fff;border-radius:999px;padding:3px 9px;font:700 11.5px/1.3 var(--body)}
.uxsl{display:block;margin:6px auto 2px;border:0;background:none;color:#c8325f;font:700 14px/1.3 var(--body);text-decoration:underline;cursor:pointer}
.acts.pk .pkr{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;width:100%}
/* racks in the same frame */
.rkov{position:absolute;left:8px;bottom:8px;z-index:4;display:flex;flex-direction:column;gap:6px;max-width:62%;pointer-events:none}
.cmp.aer .rkov{max-width:52%}
.rkov span{display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.93);border-radius:10px;padding:5px 7px;box-shadow:0 4px 12px rgba(0,0,0,.2)}
.rkov img{display:block;max-width:100%;max-height:54px;width:auto!important;height:auto!important;object-fit:contain;transform:none!important}
.rkln{margin:8px 2px 4px;text-align:center;font:600 13.5px/1.35 var(--body);color:#2a2036}.rkln em{color:#76687f;font-style:normal;font-weight:500}
.uxrk{display:flex;flex-direction:column;gap:10px;margin:8px 0 6px}
.uxrk .big{width:100%}
.big.uxwait{background:#efe5ea;color:#5b4e66;box-shadow:none}
.uxfn{margin:-2px 0 4px;text-align:center;font:600 13px/1.35 var(--body);color:#5b4e66}
.rch{padding:12px 10px;border-radius:18px;background:#fff5f8;border:1px solid #f3d3df;display:flex;flex-direction:column;gap:8px}
.rchh{display:flex;align-items:baseline;justify-content:space-between;gap:8px}.rchh b{font:400 21px/1.1 var(--display,Georgia,serif);color:var(--navy,#054689)}.rchh span{font:700 13px var(--body);color:#c8325f}
.rchp{margin:0;font:600 13px/1.35 var(--body);color:#5b4e66}
.rgrid{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x proximity;padding:2px 2px 8px;-webkit-overflow-scrolling:touch}
.rgc{flex:0 0 46%;scroll-snap-align:start;border:2px solid #f0dbe4;background:#fff;border-radius:14px;padding:6px 6px 8px;text-align:left;cursor:pointer;display:flex;flex-direction:column;gap:3px;color:#2a2036;min-width:0}
@media (min-width:700px){.rgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));overflow:visible}.rgc{flex:none}}
.rgc .rgi{position:relative;display:flex;align-items:center;justify-content:center;aspect-ratio:3/2;border-radius:10px;background:#fff;overflow:hidden}
.rgc .rgi img{max-width:100%;max-height:100%;object-fit:contain}
.rgc b{font:700 13px/1.2 var(--body);overflow-wrap:anywhere}.rgc small{font:11.5px/1.2 var(--body);color:#76687f}
.rgc.on{border-color:#c8325f;box-shadow:0 0 0 3px rgba(200,50,95,.22)}
.rgc .ck{position:absolute;right:6px;top:6px;width:26px;height:26px;border-radius:50%;background:#c8325f;color:#fff;display:grid;place-items:center;font:700 15px/1 var(--body)}
.rgc .rgh{position:absolute;left:6px;top:6px;background:rgba(255,255,255,.94);color:#c8325f;border-radius:999px;padding:2px 7px;font:700 10.5px/1.3 var(--body)}
.rgc .rgt{position:absolute;left:6px;bottom:6px;right:6px;background:rgba(255,255,255,.94);border-radius:6px;padding:2px 5px;font:700 10px/1.25 var(--body);color:#76687f}
.rgc.rgoff .rgi img{opacity:.55}
.rch .rfil .frow{flex-wrap:wrap;justify-content:center;row-gap:6px}
.uxlinks{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 14px;margin:4px 0}
.uxlinks button{border:0;background:none;color:var(--navy,#054689);font:700 14px/1.3 var(--body);text-decoration:underline;cursor:pointer;padding:6px 2px}
#s-racks:empty{display:none}
</style>'''

JS = r'''<script>/* v123 layout preview (Tiffany Nov 18): see builder/fym_fix_nov18/ux123.py */
(function(){
S.rstage=false;S.rch=false;window.__fymUx123=1;
const stop=e=>{try{e.preventDefault&&e.preventDefault();e.stopImmediatePropagation&&e.stopImmediatePropagation();}catch(x){}};
const qs=sel=>{try{return typeof document.querySelector==='function'?document.querySelector(sel):null}catch(e){return null}};
const SS={get:k=>{try{return sessionStorage.getItem(k)}catch(e){return null}},set:(k,v)=>{try{sessionStorage.setItem(k,v)}catch(e){}}};
const hdrH=()=>{const hd=qs('header.top');return (hd?hd.getBoundingClientRect().height:56)+6};
function scrollToEl(el,smooth){if(!el)return;const y=el.getBoundingClientRect().top+window.scrollY-hdrH();window.scrollTo({top:Math.max(0,y),behavior:smooth===false?'instant':'smooth'})}
function bigView(){const el=$('s-mats');if(!el)return null;const c=el.querySelector('.cmp');if(!c)return null;return c}
/* ---------- 4 + 7. guided pulse ---------- */
const PULSE={until:0,stopped:SS.get('fym_ux_modes')==='1'};
function modePulse(root){if(PULSE.stopped||!root)return;const seg=root.querySelector('.vrow .seg.mode');if(!seg)return;
 const now=Date.now();if(!PULSE.until){if(S.mode!=='close')return;PULSE.until=now+8000;SS.set('fym_ux_modes','1');setTimeout(stopPulse,8100);}
 if(now>=PULSE.until)return;seg.classList.add('uxpl');const vr=seg.closest('.vrow');if(vr&&!vr.querySelector('.uxmh'))vr.insertAdjacentHTML('beforeend','<p class="uxmh">Tap to flip between Up close, Table and Aerial</p>');}
function stopPulse(){PULSE.stopped=true;SS.set('fym_ux_modes','1');document.querySelectorAll('.seg.mode.uxpl').forEach(x=>x.classList.remove('uxpl'));document.querySelectorAll('.uxmh').forEach(x=>x.remove());}
document.addEventListener('click',e=>{if(e.target.closest&&e.target.closest('[data-mode]'))stopPulse();},true);
/* ---------- 1. X / heart under the photo ---------- */
function relayout(el){if(!el)return;el.querySelectorAll('.sbx').forEach(x=>x.remove());const cmp=el.querySelector(':scope > .cmp');if(!cmp)return;
 const acts=el.querySelector(':scope > .acts'),hint=el.querySelector(':scope > .swhint');let at=cmp;
 if(acts){acts.classList.add('uxmv');at.after(acts);at=acts;}if(hint){hint.classList.add('uxmv');at.after(hint);at=hint;}
 if(el.id==='s-mats'&&!S.rstage&&!S.peek&&!matLocked()&&S.liked.length&&el.querySelector('#sgw')){at.insertAdjacentHTML('afterend',`<button type="button" class="uxsl" data-uxsl>♥ ${S.liked.length} on your shortlist: pick your mat ↓</button>`);}}
/* swipe pop: a big heart (right) or X (left) over the photo */
function pop(sec,yes){const d=qs(sec+' .deck');if(!d)return;const p=document.createElement('div');p.className='uxpop '+(yes?'y':'n');p.setAttribute('aria-hidden','true');p.textContent=yes?'♥':'✕';d.appendChild(p);setTimeout(()=>p.remove(),760);}
const _fly=fly;fly=function(k,yes){if(k==='r')return;if(k==='m'&&S.rstage)return;const ok=!!$('top-'+k)&&queue(k).length&&!(k==='m'&&(S.peek||matLocked()));const r=_fly(k,yes);if(ok)pop('#s-mats',yes);return r;};
const _tfly=tfly;tfly=function(yes){const ok=!!$('top-t')&&tq().length&&S.tpeek==null;const r=_tfly(yes);if(ok)pop('#s-tiles',yes);return r;};
/* ---------- 5. shortlist ---------- */
const shownMat=()=>S.rstage?S.fav:S.peek;
const _tray=tray;tray=function(k){if(k!=='m')return _tray(k);const L=S.liked.filter(id=>M[id]);
 if(!L.length)return `<div class="sgw" id="sgw"><h3 class="sgh">Your shortlist</h3><p class="sgp">Tap ♥ on mats you like. They’ll wait here so you can see each one with your tiles.</p></div>`;
 const cur=shownMat(),guide=!cur&&!S.rstage;
 return `<div class="sgw${guide?' uxpl':''}" id="sgw"><h3 class="sgh">Pick your mat</h3><p class="sgp">Your shortlist (${L.length}): tap one to see it with your tiles.</p><div class="sgrid">${L.slice().reverse().map(id=>`<button type="button" class="sgc${cur===id?' on':''}" data-spk="${esc(id)}" aria-pressed="${cur===id}"><span class="sgi"><img src="${matSrc(id)}" alt="" loading="lazy">${cur===id?'<span class="sgon">Showing ✓</span>':''}</span><b>${esc(MN(id))}</b><small>${esc(BDN(M[id].bn||''))}</small></button>`).join('')}</div></div>`;};
const _acts=acts;acts=function(k){if(k==='m'&&S.peek&&!S.rstage)return `<div class="acts pk"><button type="button" class="go pkgo uxpl" data-mock="${esc(S.peek)}">Choose your racks ›</button><div class="pkr"><button type="button" class="pill" data-unpeek>‹ Keep swiping mats</button><button type="button" class="pill gh" data-unlike="${esc(S.peek)}">✕ Remove from shortlist</button></div></div>`;return _acts(k);};
/* ---------- 6. racks in the same frame ---------- */
function defRacks(){if(S.mode==='table'&&window.TVPICK){const r=TVPICK(set().slug,S.fav);return r?[r]:[];}let a=[];try{a=herRacks().filter(r=>R[r]&&!R[r].hid);}catch(e){}if(!a.length){try{a=rackDeck().slice(0,2);}catch(e){}}return a.slice(0,2);}
function shownRacks(){const P=S.rpick.filter(r=>R[r]);return P.length?P:defRacks();}
function rackName(r){try{return rackLabel(r);}catch(e){return shortR(r);}}
function rackCard(id,on,herSet){const tbl=S.mode==='table'&&window.TVROK&&!TVROK(id,set().slug);const her=herSet.has(id);
 return `<button type="button" class="rgc${on?' on':''}${tbl?' rgoff':''}" ${on?'data-rx':'data-rp'}="${esc(id)}" aria-pressed="${on}" aria-label="${on?'Take off':'Put on'} ${esc(R[id].n)}"><span class="rgi"><img src="${rackSrc(id)}" alt="" loading="lazy">${on?'<span class="ck">✓</span>':''}${her?'<span class="rgh">♥ Tiffany’s pick</span>':''}${tbl?'<span class="rgt">Not in Table view</span>':''}</span><b>${esc(shortR(id))}</b><small>${esc(BDN(R[id].bn||''))}</small>${typeof PRC==='function'?PRC('r',id):''}</button>`;}
function chooser(){const P=S.rpick.filter(r=>R[r]);let L=[];try{L=rackDeck();}catch(e){}L=[...P,...L.filter(r=>!P.includes(r))].slice(0,innerWidth>=700?36:40);let hs=new Set();try{hs=new Set(herRacks());}catch(e){}
 return `<div class="rch" id="rch"><div class="rchh"><b>Choose your racks</b><span>${P.length} of 2 picked</span></div><p class="rchp">Tap a rack to put it on your mat (✓). Tap it again to take it off. ${innerWidth<700?'Scroll sideways for more ›':''}</p><div class="rgrid">${L.length?L.map(id=>rackCard(id,P.includes(id),hs)).join(''):'<p class="rchp">No racks fit these filters. Tap the rainbow dot to see all colors.</p>'}</div><div class="rfil">${filters('r')}</div><button type="button" class="ownr" data-rsheet>+ Search any rack by name or brand</button></div>`;}
function rackFrame(){const el=$('s-mats'),s=set(),id=S.fav,P=S.rpick.filter(r=>R[r]),sh=shownRacks();
 const deckH=`<div class="deck m"><div class="peekbar"><span>Your mat</span></div>${card(id,'m')}</div>`;
 const big=S.mode==='close'?`<div class="cmp">${tileView('m')}<div class="tcap"><span>${esc(s.name)} tiles</span><span>Pinch either photo to zoom</span></div>${deckH}</div>`:`<div class="cmp aer">${deckH}</div>`;
 const tvNo=S.mode==='table'&&typeof TVD==='object'&&TVD.cls&&(TVD.cls[id]||'C')==='C';
 const line=tvNo?`<p class="rkln"><em>This mat has no top-down photo for Table view yet. Tap Up close or Aerial to see racks on it.</em></p>`:sh.length?`<p class="rkln">${P.length?'Your racks: <b>'+P.map(r=>esc(rackName(r))).join(' + ')+'</b>':'Suggested racks shown: <b>'+sh.map(r=>esc(rackName(r))).join(' + ')+'</b> <em>(pick your own below)</em>'}${S.mode==='table'&&P.length&&window.TVROK&&P.some(r=>!TVROK(r,s.slug))?'<br><em>'+P.filter(r=>!TVROK(r,s.slug)).map(r=>esc(rackName(r))+': '+esc(TVRWHY(r,s.slug))).join(' ')+' Try Up close or Aerial to see it.</em>':''}</p>`:'';
 const fin=`<button type="button" class="big go uxfin${P.length?' uxpl':' uxwait'}" data-make${P.length?'':' aria-disabled="true"'}>${P.length?'Make it official ♥':'Pick your racks to finish'}</button><p class="uxfn">${P.length===2?'2 of 2 racks picked.':P.length===1?'1 of 2 racks picked: add a second rack or finish now.':'Pick 1 or 2 racks, then finish.'}</p>`;
 el.innerHTML=`<div class="shrow">${head(3,'Choose your racks',esc(MN(id))+' + '+esc(s.name)+' tiles')}</div>`+big+line+`<div class="vrow-wrap">${VROW()}</div>`+
  `<div class="uxrk">${S.rch?chooser():`<button type="button" class="big${P.length?' gh':' uxpl'}" data-rchoose>${P.length?'Change your racks':'Choose your racks'}</button>`}${fin}</div>`+
  `<div class="uxlinks"><button type="button" data-uxback>‹ Back to the mats</button>${S.door==='mat'&&S.dmat?'':`<button type="button" data-uxswipe>Keep swiping mats</button>`}</div>`+(S.door==='mat'&&matLocked()?'':tray('m'));
 const ph=el.querySelector('#top-m .ph');if(ph&&S.mode!=='table'&&sh.length)ph.insertAdjacentHTML('beforeend',`<div class="rkov" aria-hidden="true">${sh.map(r=>`<span><img src="${rackSrc(r)}" alt=""></span>`).join('')}</div>`);
 bindCard('m');if(S.mode==='close')bindTile('tv-m');}
const _rm=renderMats;renderMats=function(){if(S._toR){S._toR=false;if(S.fav)S.rstage=true;}
 if(S.set!=null&&S.fav&&S.rstage&&M[S.fav]&&window.__imgsReady){rackFrame();try{updFlow();}catch(e){}if(TOUR.on)setTimeout(tourSync,40);}else _rm();
 const el=$('s-mats');relayout(el);modePulse(el);};
const _rt=renderTiles;renderTiles=function(){_rt();const el=$('s-tiles');relayout(el);modePulse(el);};
renderRacks=function(){const el=$('s-racks');if(S.fav&&S._rdef!==S.fav+'|'+S.set){S._rdef=S.fav+'|'+S.set;S.f.r.her=false;}if(el)el.innerHTML='';if(S.rstage&&S.fav)renderMats();try{updFlow();}catch(e){}if(TOUR.on)setTimeout(tourSync,40);};
const _rf=resetFrom;resetFrom=function(l){if(l<=2){S.rstage=false;S.rch=false;}return _rf(l);};
const _jump=jump;jump=function(id){if(id==='s-racks'){if(S.fav&&!S.rstage){S.rstage=true;S.peek=null;renderMats();}id='s-mats';}return _jump(id);};
document.addEventListener('click',e=>{const q=s=>e.target.closest&&e.target.closest(s);let b;
 if(b=q('[data-spk]')){stop(e);const id=b.dataset.spk;if(!M[id])return;
  if(S.rstage&&id===S.fav){scrollToEl(bigView());return;}S.rstage=false;S.rch=false;S.peek=id;S.dset=null;try{trk('peek',{mat:id});}catch(x){}renderMats();steps();requestAnimationFrame(()=>scrollToEl(bigView()));return;}
 if(q('[data-uxsl]')){stop(e);scrollToEl($('sgw'));return;}
 if(q('[data-mock]')){S._toR=true;S.rch=false;return;}/* the app's own handler picks the mat; renderMats then shows the rack frame */
 if(q('[data-rchoose]')){stop(e);S.rch=true;renderMats();requestAnimationFrame(()=>{const c=bigView();if(c){const r=c.getBoundingClientRect();const y=r.top+window.scrollY-hdrH()+Math.max(0,r.height-(innerHeight-hdrH())*.62);window.scrollTo({top:Math.max(0,y),behavior:'smooth'});}});try{trk('rchoose',{mat:S.fav});}catch(x){}return;}
 if(q('[data-make]')&&!S.rpick.length){stop(e);S.rch=true;renderMats();requestAnimationFrame(()=>{const r=$('rch');if(r){r.classList.add('uxpl');setTimeout(()=>r.classList.remove('uxpl'),3000);r.scrollIntoView({block:'nearest',behavior:'smooth'});}});return;}
 if(q('[data-uxback]')){stop(e);S.rstage=false;S.rch=false;S.peek=S.liked.includes(S.fav)?S.fav:null;renderMats();steps();requestAnimationFrame(()=>scrollToEl(bigView()));return;}
 if(q('[data-uxswipe]')||q('[data-unpeek]')||q('[data-ddeck]')||q('[data-back-mats]')){S.rstage=false;S.rch=false;if(q('[data-uxswipe]')){stop(e);S.peek=null;S.dset=null;renderMats();steps();requestAnimationFrame(()=>scrollToEl(bigView()));}return;}
 if(q('[data-rp]')||q('[data-rx]')){const y=window.scrollY;setTimeout(()=>{if(Math.abs(window.scrollY-y)>2)window.scrollTo({top:y,behavior:'instant'});},0);}
},true);
/* the mat door's locked pairing: the next step says what it is */
const _rm2=renderMats;renderMats=function(){_rm2();const g=qs('#s-mats .dacts [data-mock]');if(g){g.textContent='Choose your racks ›';g.classList.add('uxpl');}};
try{if(S.set!=null){renderMats();renderRacks();}else renderTiles();}catch(e){}
})();
</script>'''

k = h.rindex('</body></html>')
assert h.endswith('</body></html>') or h[k:].strip() == '</body></html>'
h = h[:k] + CSS + JS + h[k:]

assert hashlib.sha256(data_block(h).encode()).hexdigest() == D0, 'const D changed'
open(OUT, 'w', encoding='utf-8').write(h)
print('ux123 ok', OUT, len(h.encode()), 'bytes; const D unchanged', D0[:12])
