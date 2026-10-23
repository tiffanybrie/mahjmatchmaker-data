"""FYM v75 (built from live v74). Usage: python3 builder/fym_fix_oct23/v75_ui.py <build_dir>
Tiffany Oct 23 (DESK FOCUS 9:33am, rack spec 9:13am, tour script 9:37am, tour bugs 9:38am):

1. RACK SCREEN = MIRROR OF THE MAT SCREEN. Top: the chosen mat (where the tiles sit on the mat screen) with its caption bar
   (mat name, Change mat, Back). Directly under it: the rack swiper, same size, buttons and gestures as the mat swiper.
   Bottom: the rack suitors tray, styled like the mat suitors tray, with Make it official. The two empty rack slots are gone:
   hearted racks fall into the suitors tray; the first two are picked (✓); tap a ✓ rack to unpick, tap another to pick
   (max 2). One Tiffany's picks toggle (filter row). No "Browsing racks" tab on the rack deck (the mat deck has none).
2. PICK YOUR MAT BEFORE ADD RACKS. The mat suitors tray never offers Add racks until a suitor is picked (tap a suitor);
   then one "Add racks ›" button, one tap, straight to the racks. The peek view no longer repeats Add racks.
3. THE 30-SECOND TOUR, HER SCRIPT (8 steps): tiles → swipe mats (lingering swipe hand) → pick your mat → Add racks (once)
   → swipe racks (lingering hand) → Make it official → save or share (her prompt) → shop + code MAHJMATCH.
   The tour follows the app's STATE and only moves forward (a step is done when its state is reached; it never returns to
   an earlier step). Each tip box names its own step. Every new step scrolls its target into view. Auto-starts on first
   open; "Take the tour" replays it from the start. #notour (artifact) or ?tour=off (website page) skips it for testers.
4. Card section copy: "save it or share it" (never "your mahj group") + her share prompt line.
Gate [39] + builder/fym_tour_walk.py check all of this."""
import sys
B = sys.argv[1]; P = B + '/index.html'
h = open(P).read()

def rep(old, new, n=1):
    global h
    c = h.count(old)
    assert c == n, f'expected {n} x {old[:90]!r}, found {c}'
    h = h.replace(old, new)

# ---------- 1. rack screen mirror ----------
rep("""el.innerHTML=head(3,'Pick 2 racks','All couples need a wingman. '+(queue('r').length>1?'Swipe on racks below; your first 2 hearts fill these slots.':'Tap \\u2665 on the racks you like.'))+
 `<div class="cmp">${tileView('r')}<div class="matv"><img src="${matSrc(S.fav)}" alt="${esc(m.n)}" class="${m.c?'':'photo'}" data-lbx="${esc(S.fav)}"><button type="button" class="chip mini" data-back-mats>Change mat</button><button type="button" class="xz" data-lbx="${esc(S.fav)}" aria-label="See this mat full screen">⤢</button></div></div>`+tray('r')+filters('r')+`<div class="backrow">${rBackBtn()}</div><div class="cmp">${deck('r')}</div>`+acts('r')+rSuitors();
 bindCard('r');bindTile('tv-r');updFlow();}""",
"""el.innerHTML=`<div class="shrow">${head(3,'Rack-ing','All couples need a wingman. Tap \\u2665 if you love it, \\u2715 if it\\u2019s not the one')}</div>`+filters('r')+
 `<div class="cmp">${matBand()}<div class="tcap"><span>${esc(MN(S.fav))} mat</span><span class="tcr"><button type="button" class="backb" data-back-mats>Change mat</button>${rBackBtn()}</span></div>${deck('r')}</div>`+acts('r')+tray('r')+`<button type="button" class="ownr" data-rsheet>+ Own racks? Search yours</button>`;
 bindCard('r');bindMat();updFlow();}
function matBand(){const m=M[S.fav];return `<div class="tilev mband" id="tv-r"><img src="${matSrc(S.fav)}" alt="${esc(m.n)}" draggable="false"><div class="zb"><button type="button" data-tz="-1" aria-label="Zoom out">\\u2212</button><button type="button" data-tz="1" aria-label="Zoom in">+</button></div><button type="button" class="xz" data-lbx="${esc(S.fav)}" aria-label="See this mat full screen">\\u2922</button></div>`;}
function bindMat(){const t=$('tv-r');if(!t)return;zoomer(t,t.querySelector('img'),t,{key:'tz_r_'+S.fav,fp:[.5,.5],fz:1});}""")
# no "Browsing racks" tab: the rack deck looks like the mat deck
rep("""return `<div class="deck ${k}">${k==='r'?'<div class="peekbar"><span>Browsing racks</span></div>':''}""", """return `<div class="deck ${k}">""")
# rack suitors tray at the bottom (mirror of the mat suitors tray), no empty slots
_ta = h.index(""" const P=S.rpick,SG=S.rliked.filter(id=>!P.includes(id)).reverse();return `<div class="tray rk" id="rtray">""")
_tb = h.index("""function rSuitors(){""")
h = h[:_ta] + """ const L=S.rliked,P=S.rpick;return `<div class="tray rtr" id="rtray"><div class="tl"><b>${L.length}</b>${L.length===1?'suitor':'suitors'}</div>${L.length?`<div class="th">${L.slice().reverse().map(id=>{const on=P.includes(id);return `<button type="button" ${on?'data-rx':'data-rp'}="${esc(id)}" aria-pressed="${on}" aria-label="${on?'Unpick':'Pick'} ${esc(R[id].n)}"><img src="${rackSrc(id)}" alt="">${on?'<span class="ck">\\u2713</span>':''}</button>`;}).join('')}</div>`:`<div class="none">${queue('r').length>1?'Swipe right':'Tap \\u2665'} on racks you like. Pick up to 2 for each mat; they wait here.</div>`}<button type="button" class="go" data-make ${P.length?'':'disabled'}>Make it official \\u2665</button></div>${L.length?`<p class="rnote">${P.length===2?'2 of 2 picked: tap a \\u2713 rack to unpick it, then tap another to swap it in.':P.length+' of 2 picked: tap a rack suitor to pick it.'}</p>`:''}`;}
""" + h[_tb:]
# the old suitors-only tray is gone
_a = h.index("""function rSuitors(){"""); _b = h.index("""function tileView(cls){""")
h = h[:_a] + h[_b:]
# hearting a third rack goes quietly to the suitors tray (the toast covered the rack name, QA v73)
rep("""if(S.rpick.length<2)S.rpick.push(id);else toast('Saved to your rack suitors');}renderRacks();}}""", """if(S.rpick.length<2)S.rpick.push(id);}renderRacks();}}""")
rep("""if(S.rpick.length>=2){toast('2 of 2 \\u2014 tap \\u00d7 on one to swap');return;}""", """if(S.rpick.length>=2){toast('2 of 2 picked: tap a \\u2713 rack to unpick it first');return;}""")
# ---------- 2. pick a mat suitor before Add racks ----------
rep("""${S.peek||L.length===1?`<button type="button" class="go" data-mock="${esc(S.peek||L[0])}">Next: add racks ›</button>`:`<button type="button" class="go" data-choose>Next: add racks ›</button>`}""",
    """${S.peek?`<button type="button" class="go" data-mock="${esc(S.peek)}">Add racks ›</button>`:`<button type="button" class="go" disabled>Tap a suitor to pick your mat</button>`}""")
rep("""return `<div class="acts"><button type="button" class="pill" data-unpeek>‹ Back to the deck</button><button type="button" class="pill pk" data-mock="${esc(S.peek)}">Next: add racks ›</button></div>`;""",
    """return `<div class="acts"><button type="button" class="pill" data-unpeek>‹ Back to the deck</button></div>`;""")
rep("""el.innerHTML=head(3,'Love triangle','All couples need a wingman.')+`<div class="r3p">""", """el.innerHTML=head(3,'Pick your mat','All couples need a wingman.')+`<div class="r3p">""")
rep("""(S.liked.length?`<p>Which suitor is the one? Tap your favorite.</p>""", """(S.liked.length?`<p>Which suitor is the one? Pick which mat you\\u2019d like to mock up with racks.</p>""")
# Change mat during the tour: the tour must not pull her back to the racks (QA v75)
rep("""if(q('[data-back-mats]')){S.peek=S.fav;""", """if(q('[data-back-mats]')){TOUR.hold=Date.now();S.peek=S.fav;""")
# the racks section never offers a second Add racks (QA v75): it points back to the tray
rep("""${sel?`<img src="${matTh(sel)}" alt=""><p>Ready to add racks to <b>${esc(M[sel].n)}</b>?</p><button type="button" class="big" style="width:auto;padding:10px 18px" data-mock="${esc(sel)}">Add racks with ${esc(M[sel].n)} ›</button>`""",
    """${sel?`<img src="${matTh(sel)}" alt=""><p>You picked <b>${esc(M[sel].n)}</b>. Tap <b>Add racks</b> in your suitors above.</p>`""")
# the racks section never offers Add racks for a suitor she has not picked (Oct 23 bug b)
rep("""function selSuitor(){return (S.peek&&S.liked.includes(S.peek)?S.peek:null)||(S.fav&&S.liked.includes(S.fav)?S.fav:null)||(S.liked.length===1?S.liked[0]:null);}""",
    """function selSuitor(){return (S.peek&&S.liked.includes(S.peek)?S.peek:null)||(S.fav&&S.liked.includes(S.fav)?S.fav:null);}""")
# ---------- 4. card copy ----------
rep("""Pick your view, then save it or send it to your mahj group.</p>""", """Pick your view, then save it or share it.</p>""")
rep("""<button type="button" class="big" data-share>Save / Share my match card</button>""", """<button type="button" class="big" data-share>Save / Share my match card</button><p class="hint sharep">Share your match! Tag #mahjmatch, we love to see your matches!</p>""")
# ---------- 3. the tour ----------
_a = h.index("""const TSTEPS=[""")
_b = h.index("""/* v72b: the bubble never covers its target.""")
h = h[:_a] + r"""const TSTEPS=[
 {k:'tiles',t:'Step 1 · Your tiles',p:'Pick your tile set to start. Have a mat instead? Tap \u201cI have a mat\u201d.',b:'#s-tiles .tgrid button,#s-tiles .dsets button,#s-tiles .door',done:()=>S.set!=null},
 {k:'mats',t:'Step 2 · Swipe the mats',p:'\u2665 or swipe right if you love it, \u2715 or swipe left if it\u2019s not the one. Hearted mats fall below as your suitors.',b:'#top-m',hand:'m',done:()=>S.liked.length>0||!!S.fav,skip:()=>matLocked()},
 {k:'pick',t:'Step 3 · Pick your mat',p:'Pick which mat you\u2019d like to mock up with racks: tap it in your suitors.',b:'.tray .th button',done:()=>!!S.peek||!!S.fav,skip:()=>matLocked()},
 {k:'add',t:'Step 4 · Add racks',p:()=>S.peek||matLocked()?'Tap Add racks once. It takes you straight to the racks.':'Tap the suitor you\u2019d like to mock up, then tap Add racks once.',b:'.tray .go[data-mock],.dacts [data-mock],.tray .th button',done:()=>!!S.fav},
 {k:'racks',t:'Step 5 · Swipe the racks',p:'Same as the mats: \u2665 or swipe right, \u2715 or swipe left. Pick up to two rack suitors for each mat; they fall below.',b:'#top-r',hand:'r',done:()=>S.rpick.length>0},
 {k:'make',t:'Step 6 · Make it official',p:'Happy with your racks? Tap Make it official to build your match card.',b:'#rtray [data-make]',done:()=>!!S.made},
 {k:'share',t:'Step 7 · Save or share',p:'Save it or share it. Share your match! Tag #mahjmatch, we love to see your matches!',b:'[data-share]',next:'Next'},
 {k:'shop',t:'Step 8 · Shop the look',p:'Each piece links straight to its shop. Use code MAHJMATCH to save at our partner brands.',b:'.shop',next:'Done \u2665'}];
TOUR.log=[];
const NOTOUR=(()=>{const q=w=>{try{return /(^|[?&])tour=off\b/.test(w.location.search)||/notour/.test(w.location.hash);}catch(e){return false;}};return q(window)||q(window.parent);})();
function tourTarget(s){return s.b.split(',').map(x=>document.querySelector(x)).find(Boolean);}
function tourStart(){const d=$('tourq');if(d)d.remove();TOUR.prompt=false;doStartOver();TOUR.on=true;TOUR.step=0;TOUR.log=[];TOUR.shown=-1;window.scrollTo({top:0,behavior:'instant'});setTimeout(tourSync,350);}
function tourEnd(skipped){TOUR.on=false;LS.set('fym_tour',skipped?'skipped':'done');document.querySelectorAll('.bnc').forEach(e=>e.classList.remove('bnc'));document.querySelectorAll('.swh').forEach(e=>e.remove());const c=$('coach');if(c)c.remove();}
function tourNext(){if(!TOUR.on)return;TOUR.step++;tourSync();}
function tourEv(){if(TOUR.on)setTimeout(tourSync,60);}
/* the tour follows the app's state and only ever moves forward */
function tourSync(){if(!TOUR.on)return;while(TOUR.step<TSTEPS.length){const s=TSTEPS[TOUR.step];if((s.skip&&s.skip())||(s.done&&s.done()))TOUR.step++;else break;}
 if(TOUR.step>=TSTEPS.length){tourEnd(false);toast('That\u2019s it. Happy mat-ching \u2665');return;}tourPaint();}
function tourPaint(){document.querySelectorAll('.bnc').forEach(e=>e.classList.remove('bnc'));document.querySelectorAll('.swh').forEach(e=>e.remove());let c=$('coach');if(!TOUR.on){if(c)c.remove();return;}
 const s=TSTEPS[TOUR.step],fresh=TOUR.shown!==TOUR.step;if(fresh){TOUR.shown=TOUR.step;TOUR.log.push(s.k);}
 const b=tourTarget(s);if(b&&!s.hand)b.classList.add('bnc');
 if(b&&s.hand){const dk=b.parentElement;if(dk){const w=document.createElement('div');w.className='swh';w.setAttribute('aria-hidden','true');w.innerHTML='<span class="swx">\u2715</span><i></i><span class="swy">\u2665</span>';dk.appendChild(w);}}
 if(!c){c=document.createElement('div');c.id='coach';c.className='coach';c.setAttribute('role','dialog');c.setAttribute('aria-live','polite');document.body.appendChild(c);}
 c.dataset.step=s.k;c.innerHTML=`<b>${s.t}</b>${typeof s.p==='function'?s.p():s.p}<div class="cr"><span>${TOUR.step+1} of ${TSTEPS.length}</span><span><button type="button" class="sk" data-tour-skip>Skip tour</button> ${s.next?`<button type="button" data-tour-next>${s.next}</button>`:''}</span></div>`;
 if(fresh&&b){/* every new step brings its own area into view */const r=b.getBoundingClientRect();if(r.top<70||r.bottom>innerHeight-20)b.scrollIntoView({block:r.height>innerHeight*.6?'start':'center',behavior:'instant'});}
 {const app=$('app'),apr=app&&app.getBoundingClientRect(),vw=document.documentElement.clientWidth||innerWidth;
  if(b&&apr&&vw-apr.right>=292){/* desktop: the tip sits beside the app, level with its target, never on top of the app */const W2=Math.min(420,vw-apr.right-32);
   c.style.width=W2+'px';c.style.right='auto';c.style.margin='0';c.style.bottom='';c.style.left=Math.round(apr.right+16)+'px';
   if(fresh){const br=b.getBoundingClientRect();if(br.top<64||br.bottom>innerHeight-10)window.scrollBy({top:br.top-(br.height>innerHeight*.6?72:innerHeight*.3),left:0,behavior:'instant'});}
   c.style.top=Math.round(Math.min(Math.max(72,b.getBoundingClientRect().top),innerHeight-10-c.offsetHeight))+'px';return;}}
 if(b&&s.hand){/* swipe steps: the tip sits under the \u2715/\u2665 row so the tiles or mat on top, the card and the buttons all stay visible */
  const ac=b.closest('.sec')&&b.closest('.sec').querySelector('.acts');const vw=document.documentElement.clientWidth||innerWidth,w=Math.min(420,vw-24),G=10;
  c.style.width=w+'px';c.style.right='auto';c.style.margin='0';c.style.bottom='';c.style.left=Math.round((vw-w)/2)+'px';
  if(ac){const br=b.getBoundingClientRect(),seen=br.bottom>64&&br.top<innerHeight;if(!fresh&&!seen){c.style.visibility='hidden';return;}c.style.visibility='';
   {const ar=ac.getBoundingClientRect(),over=ar.bottom+G+c.offsetHeight-(innerHeight-G),room=br.top-64;const d=Math.min(over,room);if((fresh||Date.now()-(TOUR.hold||0)>1500)&&(d>0||(fresh&&br.top<64)))window.scrollBy({top:d>0?d:br.top-64,left:0,behavior:'instant'});}
   c.style.top=Math.round(Math.min(ac.getBoundingClientRect().bottom+G,innerHeight-G-c.offsetHeight))+'px';return;}}
 coachPlace(c,b);const st=TOUR.step;clearTimeout(TOUR.rp);TOUR.rp=setTimeout(()=>{/* the card preview draws late and moves the page: re-place once */if(TOUR.on&&TOUR.step===st&&!s.hand){const b2=tourTarget(s);if(b2)coachPlace(c,b2);}},700);}
""" + h[_b:]
# coachRect reads the new target helper
rep("""b=TOUR.on&&TSTEPS[TOUR.step]&&TSTEPS[TOUR.step].b.split(',').map(x=>document.querySelector(x)).find(Boolean);""", """b=TOUR.on&&TSTEPS[TOUR.step]&&tourTarget(TSTEPS[TOUR.step]);""")
# re-sync the tour after every render (instead of the v72 mats-only hooks)
rep("""{const _rm=renderMats;renderMats=function(){_rm();if(TOUR.on)setTimeout(tourPaint,30);else if(S.set!=null&&!matLocked()&&queue('m').length)hint('picks','.frow [data-her="m"]');};
 const _dc=decide;decide=function(k,yes){_dc(k,yes);if(k!=='m')return;tourEv(yes?'yes':'no');if(!yes)hint('back','[data-back="m"]');if(yes&&S.liked.length===1)hint('mock','.tray .go');if(S.hist.length>=5)hint('colors','.frow .dot[data-fam]:not([data-fam=""])');};}""",
"""{let tq=0;const sync=()=>{if(!TOUR.on)return;clearTimeout(tq);tq=setTimeout(tourSync,40);};
 const _rt=renderTiles;renderTiles=function(){_rt();sync();};const _rr=renderRacks;renderRacks=function(){_rr();sync();};const _st=steps;steps=function(){_st();sync();};
 const _rm=renderMats;renderMats=function(){_rm();sync();if(!TOUR.on&&S.set!=null&&!matLocked()&&queue('m').length)hint('picks','.frow [data-her="m"]');};
 const _dc=decide;decide=function(k,yes){_dc(k,yes);sync();if(k!=='m')return;if(!yes)hint('back','[data-back="m"]');if(yes&&S.liked.length===1)hint('mock','.tray .th button');if(S.hist.length>=5)hint('colors','.frow .dot[data-fam]:not([data-fam=""])');};}""")
# while the tour runs, it does the scrolling (jump()'s smooth scroll fought the tour's)
rep("""renderAll();jump('s-mats');return;}""", """renderAll();if(!TOUR.on)jump('s-mats');return;}""", 2)
rep("""S.peek=null;renderAll();jump('s-racks');""", """S.peek=null;renderAll();if(!TOUR.on)jump('s-racks');""")
# a scroll she makes re-places (never re-scrolls) the swipe-step tip
rep("""addEventListener('resize',()=>{if(TOUR.on)tourPaint();});""", """addEventListener('resize',()=>{if(TOUR.on)tourPaint();});
let tsc=0;addEventListener('scroll',()=>{if(!TOUR.on||!TSTEPS[TOUR.step].hand)return;cancelAnimationFrame(tsc);tsc=requestAnimationFrame(()=>{const c=$('coach'),b=tourTarget(TSTEPS[TOUR.step]);if(!c||!b)return;const br=b.getBoundingClientRect(),ac=b.closest('.sec')&&b.closest('.sec').querySelector('.acts');const seen=br.bottom>64&&br.top<innerHeight;c.style.visibility=seen?'':'hidden';if(seen&&ac&&!(innerWidth>=1100))c.style.top=Math.round(Math.min(ac.getBoundingClientRect().bottom+10,innerHeight-10-c.offsetHeight))+'px';});},{passive:true});""")
# first open: the tour starts by itself (no question sheet); testers can switch it off
rep("""setTimeout(()=>{if(S.set==null)tourOffer();},1200);""", """setTimeout(()=>{if(S.set==null&&!NOTOUR&&!LS.get('fym_tour')&&!TOUR.on)tourStart();},1200);""")
rep("""Take the 30-seco""", """Take the 30-seco""")
# styles
_c = """.tray.rsb{align-items:center}.tray.rsb .rsw{flex:1;min-width:0}.tray.rsb .rsw small{display:block;font:600 12px var(--body);color:var(--mute);margin:0 0 4px}
.tray.rsb .th button{width:84px;height:54px}"""
rep(_c, """/* v75: rack screen mirrors the mat screen; tour swipe hand */
.tilev.mband img{position:absolute;left:0;top:0;width:auto;height:100%;max-width:none}
.tilev.mband .xz{bottom:8px;right:8px}
.tcap .tcr{display:flex;gap:6px;align-items:center;opacity:1}
.tcap span.tcr{opacity:1}
.deck.r,.cmp .deck.r{height:min(calc(100vw - 24px + 54px),550px)}
@media (max-width:560px){.deck.r,.cmp .deck.r{height:min(calc(100vw - 24px + 54px),calc(100dvh - 372px),550px);min-height:200px}}
.tray.rtr .th button{width:84px;height:54px}
.tray.rtr .go{max-width:110px}
.rnote{margin:-2px 2px 0;font:600 12px var(--body);color:var(--mute)}
.ownr{align-self:flex-start}
.sharep{margin:2px 0 4px;font-weight:600;color:var(--pink)}
.swh{position:absolute;left:0;right:0;top:42%;z-index:5;pointer-events:none;display:flex;justify-content:space-between;align-items:center;padding:0 14px}
.swh span{font:700 22px var(--body);width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.92);box-shadow:0 4px 12px rgba(0,0,0,.18)}
.swh .swx{color:#7a6a85}.swh .swy{color:var(--pink)}
.swh i{position:absolute;left:50%;top:50%;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;background:rgba(255,255,255,.55);border:3px solid var(--navy);box-shadow:0 0 0 6px rgba(5,70,137,.18);animation:swipehint 2.6s ease-in-out infinite}
@keyframes swipehint{0%,8%{transform:translateX(0)}30%{transform:translateX(110px)}42%{transform:translateX(110px);opacity:.3}50%{transform:translateX(0);opacity:1}72%{transform:translateX(-110px)}84%{transform:translateX(-110px);opacity:.3}100%{transform:translateX(0);opacity:1}}
@media (prefers-reduced-motion:reduce){.swh i{animation:none}}""")
open(P, 'w').write(h)
print('v75 patched')
