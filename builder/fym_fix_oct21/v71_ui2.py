"""FYM v71 UI, part 2 (Tiffany's live tests Oct 21 6:30-6:37pm). Run after v71_ui.py. Usage: python3 builder/fym_fix_oct21/v71_ui2.py <build_dir>
 1 headlines never italic: plain "Find Your Mat-ch(TM)" in display type
 2 the "Tiffany's match" pill on a card is a working picks toggle (same state as the bar toggle)
 3 zoom: after pinching back out, the remaining finger swipes immediately (pinch end snaps ~1x to 1x and re-seeds the drag)
 4 the mock-up always uses HER pick: with several suitors and none chosen she is asked to tap one; never auto-picks
 5 racks: "Your racks" tray with 2 slots (thumb + x), extra hearts go to "Rack suitors" (tap to fill an empty slot);
   Make it official uses exactly the 2 slots; own-rack search stays
 6 card footer: "Use code MAHJMATCH to save"
 7 Save / Share button: Claude downloads capability inside claude.ai (iOS app = share sheet), navigator.share (PNG) elsewhere,
   then download, then open in a new tab; press-and-hold copy removed
 8 one card design (Love triangle, plus the Mood board view) in 3 sizes: Story 9:16, Post 4:5, Pin 2:3
11 Start over: tapping the top logo (confirm sheet if there is a shortlist) + a small Start over link near the top past the doors
12 "<- Back" just above the card brings back the previous mat (undoes its heart or X), repeatable through history"""
import sys, json, re
B = sys.argv[1]; P = B + '/index.html'
h = open(P).read()
i = h.index('const D=') + 8
_, end = json.JSONDecoder().raw_decode(h[i:]); end += i
H, data, t = h[:i], h[i:end], h[end:]

def rep(s, a, b, n=1):
    c = s.count(a)
    assert c == n, (c, a[:100])
    return s.replace(a, b)

# ---- CSS
H = rep(H, ".lock .ttl i{font-style:italic}", ".lock .ttl i{font-style:normal}")
H = rep(H, ".herbar small{flex:1;min-width:0;text-align:right;line-height:1.3}\n</style>", """.herbar small{flex:1;min-width:0;text-align:right;line-height:1.3}
/* v71 part 2 */
.scard button.hb{pointer-events:auto;border:0;cursor:pointer;font:700 11px var(--body)}
.scard button.hb[aria-pressed="false"]{background:rgba(255,255,255,.95);color:var(--mute);box-shadow:0 0 0 1.5px #f2c2d4 inset}
.frow2{display:flex;align-items:center;justify-content:space-between;gap:8px}
.solink{flex:none;border:0;background:none;color:var(--pink);font:700 12.5px var(--body);text-decoration:underline;text-underline-offset:3px;cursor:pointer;padding:4px 2px}
#logo{cursor:pointer}
.tcap .backb,.backrow .backb{border:0;border-radius:999px;background:#fff;color:var(--navy);font:700 12px var(--body);padding:3px 10px;cursor:pointer;line-height:1.3}
.tcap{align-items:center}
.tcap .backb:disabled,.backrow .backb:disabled{opacity:.4;cursor:default}
.backrow{display:flex;justify-content:flex-start;margin:0 0 6px}
.backrow .backb{background:var(--navy);color:#fff}
.tray.rk{flex-direction:column;align-items:stretch;gap:8px;flex-wrap:nowrap}
.rkh{display:flex;align-items:baseline;justify-content:space-between;gap:8px}
.rkh b{font:400 18px 'Alfa Slab One',Georgia,serif;color:var(--navy)}
.rkh span{font:700 12.5px var(--body);color:var(--mute)}
.rkh span.full{color:var(--pink)}
.slots{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.slot{position:relative;height:64px;border-radius:14px;background:#fff;border:2px solid var(--pink);display:flex;align-items:center;justify-content:center;padding:4px}
.slot img{max-width:100%;max-height:100%;object-fit:contain}
.slot.empty{border:2px dashed #e3c9d4;color:var(--mute);font:600 12.5px var(--body)}
.slot .rx{position:absolute;right:-7px;top:-7px;width:26px;height:26px;border-radius:50%;border:0;background:var(--pink);color:#fff;font:700 16px/26px var(--body);cursor:pointer;padding:0}
.rsug small{display:block;font:600 12px var(--body);color:var(--mute);margin:0 0 4px}
.rsug .th{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding:2px}
.rsug .th button{flex:none;width:84px;height:54px;border-radius:12px;border:2px solid #fff;background:#fff;padding:2px;cursor:pointer}
.rsug .th button img{width:100%;height:100%;object-fit:contain}
.rkb{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.rkb .ownr{flex:1 1 auto;margin:0}
.rkb .go{flex:1 1 auto;max-width:none;padding:11px 14px;font-size:14px}
.r3p .pick1{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:6px}
.r3p .pick1 button{width:96px;border:2px solid var(--line);background:#fff;border-radius:14px;padding:6px;cursor:pointer;font:700 11.5px/1.2 var(--body);color:var(--ink)}
.r3p .pick1 img{width:80px;height:80px;margin:0 auto 4px}
.sheet .box p{margin:0 0 12px;color:var(--mute);font-size:14px;line-height:1.4}
</style>""")

# ---- 1. headlines without italics
t = rep(t, '<h1 class="ttl">Find <i>Your</i> Mat-ch™</h1>', '<h1 class="ttl">Find Your Mat-ch™</h1>')
t = rep(t, '<h1 class="ttl">Find <i>Your</i> Mat-ch</h1>', '<h1 class="ttl">Find Your Mat-ch</h1>')

# ---- 2. picks pill on the card toggles picks
t = rep(t, "${her?`<span class=\"hb\">${icon()} ${!mat&&UNI.includes(id)&&!herRacks().includes(id)?'Goes with everything':'Tiffany’s match'}</span>`:''}",
        "${her?(()=>{const lab=!mat&&UNI.includes(id)&&!herRacks().includes(id)?'Goes with everything':'Tiffany’s match',kk=mat?'m':'r';return herUseful(kk)?`<button type=\"button\" class=\"hb\" data-her=\"${kk}\" aria-pressed=\"${S.f[kk].her}\" aria-label=\"Tiffany’s picks ${S.f[kk].her?'on':'off'}: tap to switch\">${icon()} ${lab} · ${S.f[kk].her?'picks on':'picks off'}</button>`:`<span class=\"hb\">${icon()} ${lab}</span>`;})():''}")
t = rep(t, "function bindCard(k){const c=$('top-'+k);if(!c)return;const img=c.querySelector('.ph img'),ph=c.querySelector('.ph');\n",
        "function bindCard(k){const c=$('top-'+k);if(!c)return;const img=c.querySelector('.ph img'),ph=c.querySelector('.ph');c.querySelectorAll('button.hb').forEach(b=>b.addEventListener('pointerdown',e=>e.stopPropagation()));\n")

# ---- 3. zoom: pinch end snaps near-1x to 1x and the remaining finger keeps swiping
t = rep(t, " const up=e=>{if(!pts.has(e.pointerId))return;pts.delete(e.pointerId);if(pts.size<2)pinch=null;\n",
        " const up=e=>{if(!pts.has(e.pointerId))return;pts.delete(e.pointerId);if(pinch&&pts.size<2){pinch=null;if(z.s<1.15){const r=box.getBoundingClientRect();zoomAt(1,r.left+r.width/2,r.top+r.height/2,true);}const rest=[...pts.values()][0];st=rest?{x:rest.x,y:rest.y,zx:z.x,zy:z.y,py:rest.y}:null;dx=0;lock=null;last=0;host.style.transform='';return;}if(pts.size<2)pinch=null;\n")

# ---- 4. her own pick for the mock-up
t = rep(t, "function selSuitor(){return S.peek||(S.fav&&S.liked.includes(S.fav)?S.fav:null)||S.liked[S.liked.length-1]||null;}",
        "function selSuitor(){return (S.peek&&S.liked.includes(S.peek)?S.peek:null)||(S.fav&&S.liked.includes(S.fav)?S.fav:null)||(S.liked.length===1?S.liked[0]:null);}/* v71: never auto-pick from several suitors (Tiffany 6:30pm: the prompt used the wrong mat) */")
t = rep(t, "el.innerHTML=head(3,'Love triangle','All couples need a wingman.')+`<div class=\"r3p\">${sel?`<img src=\"${matTh(sel)}\" alt=\"\"><p>Pick your favorite suitor and tap <b>Next: add racks</b>.</p><button type=\"button\" class=\"big\" style=\"width:auto;padding:10px 18px\" data-mock=\"${esc(sel)}\">Add racks with ${esc(M[sel].n)} ›</button>`:`<p>Heart a mat in step 2 and it’ll show up here.</p>`}</div>`;return;}",
        "el.innerHTML=head(3,'Love triangle','All couples need a wingman.')+`<div class=\"r3p\">${sel?`<img src=\"${matTh(sel)}\" alt=\"\"><p>Ready to add racks to <b>${esc(M[sel].n)}</b>?</p><button type=\"button\" class=\"big\" style=\"width:auto;padding:10px 18px\" data-mock=\"${esc(sel)}\">Add racks with ${esc(M[sel].n)} ›</button>`:(S.liked.length?`<p>Which suitor is the one? Tap your favorite.</p><div class=\"pick1\">${S.liked.slice().reverse().map(id=>`<button type=\"button\" data-mock=\"${esc(id)}\"><img src=\"${matTh(id)}\" alt=\"\">${esc(M[id].n)}</button>`).join('')}</div>`:`<p>Heart a mat you love in step 2 first. Then you’ll pick racks for it here.</p>`)}</div>`;return;}")

# tray (mats): Next goes straight on only when the choice is unambiguous
t = rep(t, "<button type=\"button\" class=\"go\" data-mock=\"${esc(S.peek||L[L.length-1])}\">Next: add racks ›</button>",
        "${S.peek||L.length===1?`<button type=\"button\" class=\"go\" data-mock=\"${esc(S.peek||L[0])}\">Next: add racks ›</button>`:`<button type=\"button\" class=\"go\" data-choose>Next: add racks ›</button>`}")

# ---- 5. racks tray with 2 slots
a = t.index(" const L=S.rliked;return `<div class=\"tray rk\">"); b = t.index("\n", a)
t = t[:a] + """ const P=S.rpick,SG=S.rliked.filter(id=>!P.includes(id)).reverse();return `<div class="tray rk" id="rtray"><div class="rkh"><b>Your racks</b><span class="${P.length===2?'full':''}">${P.length===2?'2 of 2 \\u2014 tap \\u00d7 to swap':P.length+' of 2 picked'}</span></div><div class="slots">${[0,1].map(i=>P[i]?`<div class="slot"><img src="${rackSrc(P[i])}" alt="${esc(R[P[i]].n)}"><button type="button" class="rx" data-rx="${esc(P[i])}" aria-label="Remove ${esc(shortR(P[i]))}">\\u00d7</button></div>`:`<div class="slot empty">\\u2665 a rack</div>`).join('')}</div>${SG.length?`<div class="rsug"><small>Rack suitors: ${P.length===2?'tap \\u00d7 above, then tap one to swap it in':'tap one to add it'}</small><div class="th">${SG.map(id=>`<button type="button" data-rp="${esc(id)}" aria-label="${esc(R[id].n)}"><img src="${rackSrc(id)}" alt=""></button>`).join('')}</div></div>`:(P.length?'':`<div class="none">${queue('r').length>1?'Swipe right':'Tap \\u2665'} on racks you like. Your first 2 fill these slots.</div>`)}<div class="rkb"><button type="button" class="ownr" data-rsheet>+ Own racks? Search yours</button><button type="button" class="go" data-make ${P.length?'':'disabled'}>Make it official \\u2665</button></div></div>`;}""" + t[b:]
t = rep(t, " else{S.rseen[id]=1;S.rhist.push(id);if(yes&&!S.rliked.includes(id)){S.rliked.push(id);if(S.rpick.length<2)S.rpick.push(id);}renderRacks();}}",
        " else{S.rseen[id]=1;S.rhist.push(id);if(yes&&!S.rliked.includes(id)){S.rliked.push(id);if(S.rpick.length<2)S.rpick.push(id);else toast('Saved to your rack suitors');}renderRacks();}}")
t = rep(t, " if(b=q('[data-rp]')){const id=b.dataset.rp,i=S.rpick.indexOf(id);if(i>=0)S.rpick.splice(i,1);else{S.rpick.push(id);if(S.rpick.length>2)S.rpick.shift();}S.made=false;renderRacks();$('s-card').innerHTML='';steps();return;}",
        " if(b=q('[data-rp]')){const id=b.dataset.rp;if(S.rpick.includes(id))return;if(S.rpick.length>=2){toast('2 of 2 \\u2014 tap \\u00d7 on one to swap');return;}S.rpick.push(id);S.made=false;renderRacks();$('s-card').innerHTML='';steps();return;}\n if(b=q('[data-rx]')){S.rpick=S.rpick.filter(x=>x!==b.dataset.rx);S.made=false;renderRacks();$('s-card').innerHTML='';steps();return;}\n if(q('[data-choose]')){renderRacks();steps();jump('s-racks');return;}\n if(b=q('[data-back]')){undo(b.dataset.back);steps();return;}\n if(q('#logo')||q('[data-startover]')){startOver();return;}\n if(q('[data-so-yes]')){const d=$('sosheet');if(d)d.remove();doStartOver();return;}\n if(q('[data-so-no]')){const d=$('sosheet');if(d)d.remove();return;}")
t = rep(t, " S.rseen[id]=1;if(!S.rliked.includes(id))S.rliked.push(id);if(!S.rpick.includes(id)){if(S.rpick.length>=2)S.rpick.shift();S.rpick.push(id);}\n renderRacks();const t=document.createElement('div');t.className='toast';t.textContent=shortR(id)+' added to your racks';",
        " S.rseen[id]=1;if(!S.rliked.includes(id))S.rliked.push(id);const full=!S.rpick.includes(id)&&S.rpick.length>=2;if(!S.rpick.includes(id)&&!full)S.rpick.push(id);\n renderRacks();const t=document.createElement('div');t.className='toast';t.textContent=shortR(id)+(full?' saved to your rack suitors':' added to your racks');")

# ---- 6. code line
t = rep(t, "if(ps.some(o=>!o.code))return 'Use code MAHJMATCH';return 'Use code '+ps[0].code;}", "if(ps.some(o=>!o.code))return 'Use code MAHJMATCH to save';return 'Use code '+ps[0].code+' to save';}")

# ---- 8. one design, 3 sizes
t = rep(t, "const VIEWS=[['tri','Love triangle'],['stack','Mood board'],['shop','Shop']];", "const VIEWS=[['tri','Love triangle'],['stack','Mood board']];\nconst CARD_SIZES={story:{w:1080,h:1920,l:'Story',s:'9:16'},post:{w:1080,h:1350,l:'Post',s:'4:5'},pin:{w:1000,h:1500,l:'Pin',s:'2:3'}};if(!CARD_SIZES[S.fmt])S.fmt='post';if(!VIEWS.some(v=>v[0]===S.view))S.view='tri';")
t = rep(t, "<div class=\"seg nv\" role=\"group\" aria-label=\"Size\"><button type=\"button\" data-fmt=\"fb\" aria-pressed=\"${S.fmt==='fb'}\">Facebook post</button><button type=\"button\" data-fmt=\"pin\" aria-pressed=\"${S.fmt==='pin'}\">Pinterest pin</button></div>",
        "<div class=\"seg nv\" role=\"group\" aria-label=\"Size\">${Object.entries(CARD_SIZES).map(([k,v])=>`<button type=\"button\" data-fmt=\"${k}\" aria-pressed=\"${S.fmt===k}\">${v.l} ${v.s}</button>`).join('')}</div>")
t = rep(t, " <p class=\"hint\">On your phone, press and hold the picture to save it.</p>\n <button type=\"button\" class=\"big\" data-share>Save or share my match card</button>",
        " <button type=\"button\" class=\"big\" data-share>Save / Share my match card</button>")
t = rep(t, "const s=set(),fb=S.fmt==='fb',W=fb?1080:1000,H=fb?1350:1500,SC=2;", "const s=set(),FM=CARD_SIZES[S.fmt]||CARD_SIZES.post,W=FM.w,H=FM.h,fb=H/W<1.3,SC=2;")
t = rep(t, "if(b=q('[data-view]')){S.view=b.dataset.view;renderCard();return;}", "if(b=q('[data-view]')){S.view=b.dataset.view;renderCard();return;}")
# ---- 7. save / share
t = rep(t, " try{cardURL=cv.toDataURL('image/jpeg',.92);}catch(e){cardURL='';}\n", " try{cardURL=cv.toDataURL('image/jpeg',.92);}catch(e){cardURL='';}\n cardBlob=null;try{cv.toBlob(b=>{if(job===cardJob)cardBlob=b;},'image/png');}catch(e){}\n")
t = rep(t, "let cardURL='',cardJob=0;", "let cardURL='',cardJob=0,cardBlob=null;\nconst DLP=(window.claude&&typeof claude.use==='function')?Promise.resolve(claude.use('downloads')).catch(()=>null):Promise.resolve(null);let DL=null;DLP.then(d=>{DL=d;});")
a = t.index("async function share(){"); b = t.index("\n</script>", a)
t = t[:a] + """async function share(){if(!cardURL)return;trk('save',{mat:S.fav,rack:S.rpick.join(' + '),x:S.fmt});const name=`${set().slug}-match-${S.fmt}.png`;
 let blob=cardBlob;if(!blob){try{blob=await (await fetch(cardURL)).blob();}catch(e){blob=null;}}if(!blob){toast('Still drawing your card. Try again in a second.');return;}
 const inFrame=(()=>{try{return window.top!==window;}catch(e){return true;}})();
 const viaDL=async()=>{const dl=DL||await Promise.race([DLP,new Promise(r=>setTimeout(()=>r(null),1500))]);if(!dl)return false;try{await dl.save({filename:name,data:blob});toast('Match card saved');return true;}catch(e){return !!(e&&e.code==='declined');}};
 const viaShare=async()=>{let f;try{f=new File([blob],name,{type:blob.type||'image/png'});}catch(e){return false;}if(!(navigator.canShare&&navigator.canShare({files:[f]})))return false;try{await navigator.share({files:[f],title:'My Find Your Mat-ch card',text:'Matched on www.mahjmatchmaker.com'});return true;}catch(e){return !!(e&&e.name==='AbortError');}};
 if(inFrame?(await viaDL()||await viaShare()):(await viaShare()||await viaDL()))return;
 try{const u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();toast('Match card downloaded');return;}catch(e){}
 try{window.open(URL.createObjectURL(blob),'_blank');toast('Your card opened in a new tab');}catch(e){toast('Saving is blocked here. Open mahjmatchmaker.com to save it.');}}""" + t[b:]

# ---- 11. start over
t = rep(t, "function updFlow(){", """function startOver(){const n=S.liked.length,r=S.rliked.length;if(!n&&!r&&!S.made){doStartOver();return;}const d=document.createElement('div');d.className='sheet';d.id='sosheet';d.innerHTML=`<div class="box"><h3>Start over?</h3><p>This clears your shortlist${n?` (${n} mat${n>1?'s':''}${r?`, ${r} rack${r>1?'s':''}`:''})`:''} and takes you back to the start.</p><div class="dacts"><button type="button" class="big" data-so-yes>Start over</button><button type="button" class="big gh" data-so-no>Keep my picks</button></div></div>`;d.addEventListener('click',e=>{if(e.target===d)d.remove();});document.body.appendChild(d);}
function doStartOver(){Object.assign(S,{set:null,dmat:null,dkeep:null,ddeck:false,dset:null,door:'tiles',tilesOpen:true,dfams:[],dshow:0,dcat:false});resetFrom(1);closeLbx();renderAll();window.scrollTo({top:0,behavior:'smooth'});}
const flowRow=()=>`<div class="frow2"><ol class="flow" id="flow" aria-label="Your steps">${flowHTML()}</ol><button type="button" class="solink" data-startover>Start over</button></div>`;
function updFlow(){""")
t = rep(t, "<div class=\"pair\"><ol class=\"flow\" id=\"flow\" aria-label=\"Your steps\">${flowHTML()}</ol>", "<div class=\"pair\">${flowRow()}")
t = rep(t, "el.innerHTML=`<ol class=\"flow\" id=\"flow\" aria-label=\"Your steps\">${flowHTML()}</ol><div class=\"picked\"><span class=\"num\">1</span>", "el.innerHTML=`${flowRow()}<div class=\"picked\"><span class=\"num\">1</span>")
t = rep(t, "$('logo').src=LG('icon')||LG('ours');", "$('logo').src=LG('icon')||LG('ours');$('logo').setAttribute('role','button');$('logo').setAttribute('tabindex','0');$('logo').setAttribute('aria-label','Start over');$('logo').title='Start over';$('logo').addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();startOver();}});")

# ---- 12. Back above the card (mats deck)
t = rep(t, "(S.mode==='close'?`<div class=\"cmp\">${tileView('m')}<div class=\"tcap\"><span>${esc(s.name)} tiles</span><span>Pinch either photo to zoom</span></div>${deck('m')}</div>`:`<div class=\"cmp aer\">${deck('m')}</div>`)+herBar('m')",
        "(S.mode==='close'?`<div class=\"cmp\">${tileView('m')}<div class=\"tcap\"><span>${esc(s.name)} tiles</span>${backBtn()}</div>${deck('m')}</div>`:`<div class=\"backrow\">${backBtn()}</div><div class=\"cmp aer\">${deck('m')}</div>`)+herBar('m')")
t = rep(t, "function selSuitor(){", "const backBtn=()=>`<button type=\"button\" class=\"backb\" data-back=\"m\" ${S.hist.length&&!S.peek?'':'disabled'} aria-label=\"Bring back the last mat\">\\u2190 Back</button>`;\nfunction selSuitor(){")
open(P, 'w').write(H + data + t)
print('v71 ui2 patched')
