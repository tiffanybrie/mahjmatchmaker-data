"""v114 30-SECOND TOUR rebuild (Tiffany Nov 3 2:54pm, walked it on her phone; go-live condition). Her problems: step 1 kept
bouncing on the doors after she tapped; it never pointed at the finder and the grid sat off-screen; 'Try Table' had no Table tour;
a grayed 'not in Table view' note was jumped past; picks limited the racks (now off by default).
RULES: nothing preselected; each step waits for the person's REAL action, then the highlight moves to the next target; the target
is scrolled into view and the bubble docks right next to it; never skip a step they are on; one sentence per bubble.
 - every tap / typed search re-checks the tour (it used to re-check only on a few buttons);
 - the finder (colours + Brand + Search) is wrapped in .tfind so the tour can ring it;
 - big targets get a ring outline (.tring) instead of the bounce.
Steps (tiles door): door, find, grid, mats, view, [Table: tv1 what it shows, tv2 Adjust / swap, tv3 grayed-mat note, waits],
pick, add, racks, rmenu (menu below the racks, one colour OR one type), rpick, make, share (Save image), list (Text or email),
mine (My match cards). Mat door: door, mfind, mgrid, tswipe, tpk, tadd, view [Table], racks... Gate [35] walks both doors.
Idempotent. Usage: python3 tour114.py <build dir or index.html>"""
import sys, os
P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html'); h = open(P).read()
if '/*v114 tour*/' in h: print('tour114 already'); sys.exit()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)
# finder wrappers
rep('<div class="tchips" role="group" aria-label="Shop tiles by color">', '<div class="tfind"><div class="tchips" role="group" aria-label="Shop tiles by color">')
rep('aria-label="Search tile sets"></div><div class="tgrid" id="tgrid">', 'aria-label="Search tile sets"></div></div><div class="tgrid" id="tgrid">')
rep("+doorChips()+matBrandMenu()+`<div class=\"msearch\"><input id=\"mdq\"", "+'<div class=\"tfind\">'+doorChips()+matBrandMenu()+`<div class=\"msearch\"><input id=\"mdq\"")
rep('aria-label="Search mats"></div><div class="tgrid mgrid" id="mdgrid">', 'aria-label="Search mats"></div></div><div class="tgrid mgrid" id="mdgrid">')
# steps
i = h.index('const TSTEPS=['); j = h.index('];\nTOUR.log=[];', i) + 2
STEPS = r"""/* the finder is taller than a small phone can show with its bubble: ring the colours there (brand + search sit right below) */
const TFB=()=>(innerHeight||800)<760?'#s-tiles .tfind .tchips':'#s-tiles .tfind';
const TSTEPS=[/*v114 tour*/
 {k:'door',t:'Tiles or mat',p:'Start with your tiles, or with a mat you already love.',b:'#s-tiles .door',still:true,done:()=>!!TOUR.f.door||S.set!=null||!!S.dmat},
 {k:'find',t:'Find your tiles',p:'Shop by color, pick a brand, or search a set by name.',b:TFB,ring:true,next:'Next',done:()=>!!TOUR.f.find||S.set!=null,skip:()=>S.door==='mat'},
 {k:'grid',t:'Tap a tile set',p:'Tap the tiles you’re bringing to the table.',b:'#tgrid [data-tile],#tgrid .blg,#tgrid button',done:()=>S.set!=null,skip:()=>S.door==='mat'},
 {k:'mfind',t:'Find your mat',p:'Shop by color, pick a brand, or search your mat by name.',b:TFB,ring:true,next:'Next',done:()=>!!TOUR.f.find||!!S.dmat,skip:()=>S.door!=='mat'},
 {k:'mgrid',t:'Tap your mat',p:'Tap the mat you already have or love.',b:'#mdgrid button',done:()=>!!S.dmat,skip:()=>S.door!=='mat'},
 {k:'tswipe',t:'Swipe the tiles',p:'Tap ♥ if you love these tiles on your mat, ✕ if they’re not the one.',b:'#top-t',hand:'t',done:()=>S.tliked.length>0||S.set!=null,skip:()=>S.door!=='mat'},
 {k:'tpk',t:'Pick your tiles',p:'Tap your favorite in Suitors.',b:'#s-tiles .tray [data-tpk]',done:()=>S.tpeek!=null||S.set!=null,skip:()=>S.door!=='mat'},
 {k:'tadd',t:'Add racks',p:'Tap Add racks to move on to the racks.',b:'#s-tiles [data-tadd]',done:()=>S.set!=null&&!!S.fav,skip:()=>S.door!=='mat'},
 {k:'mats',t:'Swipe the mats',p:'Tap ♥ if you love it, ✕ if it’s not the one; Tiffany’s own matches come first.',b:'#top-m',hand:'m',done:()=>S.liked.length>0||!!S.fav,skip:()=>matLocked()},
 {k:'view',t:'Pick your view',p:'Up close, Aerial or Table: tap one, or Next to stay.',b:'#s-mats .vrow .seg',ring:true,next:'Next',done:()=>!!TOUR.f.view},
 {k:'tv1',t:'Table view',p:'Your tiles, mat and racks set at a table, seen from above.',b:'#s-mats .scard[id^="top-"] .ph',ring:true,next:'Next',skip:()=>S.mode!=='table'},
 {k:'tv2',t:'Swap anything',p:'Tap Adjust to swap the tiles, mat or racks right on the table.',b:'#s-mats [data-tvadj]',next:'Next',done:()=>!!TOUR.f.adj,skip:()=>S.mode!=='table'},
 {k:'tv3',t:'Not in Table view yet',p:'A grayed mat has no top-down photo yet; its note says why, so swipe on or try another view.',b:'#s-mats .scard.tvoff .tvna',ring:true,next:'Got it',skip:()=>S.mode!=='table'||!document.querySelector('#s-mats .scard.tvoff .tvna')},
 {k:'pick',t:'Pick your mat',p:'Tap your favorite in Suitors to add racks.',b:'.tray .th button',done:()=>!!S.peek||!!S.fav,skip:()=>matLocked()},
 {k:'add',t:'Add racks',p:'Tap Add racks once to go to the racks.',b:'.acts.pk [data-mock],.tray .go[data-mock],.dacts [data-mock],.tray .th button',done:()=>!!S.fav},
 {k:'racks',t:'Swipe the racks',p:'Same as the mats: ♥ if you love it, ✕ if it’s not the one.',b:'#top-r',hand:'r',done:()=>S.rliked.length>0||S.rpick.length>0},
 {k:'rmenu',t:'Narrow the racks',p:'The menu below the racks shows one color or one type at a time.',b:'#s-racks .rctl',ring:true,next:'Next'},
 {k:'rpick',t:'Pick 1 or 2 racks',p:'Tap a rack suitor to pick it (✓).',b:'#rtray .th button',done:()=>S.rpick.length>0},
 {k:'make',t:'Make it official',p:'Tap Make it official to build your match card.',b:'#rtray [data-make]',done:()=>!!S.made},
 {k:'share',wait:()=>{const p=$('prev');if(!p)return true;const i=p.querySelector('img');return !!(i&&i.complete&&i.naturalHeight&&p.offsetHeight>40)||/Couldn/.test(p.textContent);},t:'Your match card',p:'Save image downloads your card, or share it.',b:'[data-share]',next:'Next'},
 {k:'list',t:'Your shopping list',p:'Text or email yourself every piece with its link.',b:'[data-shoplist]',next:'Next'},
 {k:'mine',t:'My match cards',p:'Every card you make waits under ★ at the top, one per tile set.',b:'.tbx [data-mystars]',next:'Done ♥'}];"""
h = h[:i] + STEPS + h[j:]
rep("function tourTarget(s){return s.b.split(',')", "function tourTarget(s){return (typeof s.b==='function'?s.b():s.b).split(',')")
# a target in the fixed top bar (My match cards under the heart) is on screen even though it sits above the 56px line
rep("const r=b.getBoundingClientRect(),seen=r.bottom>56&&r.top<innerHeight;", "const r=b.getBoundingClientRect(),seen=(r.bottom>56||!!b.closest('.tbx'))&&r.top<innerHeight;")
# QA r9: the counter counted skipped steps ('3 of 22' then '9 of 22'): count only the steps this person actually sees
rep("<span>${TOUR.step+1} of ${TSTEPS.length}</span>", "<span>Step ${TOUR.log.length}</span>")
# the top-bar target (My match cards) is fixed: never scroll the page for it (the card stays on screen)
rep(" else if(r.top<TOPS||r.bottom>vh){b.scrollIntoView(", " else if((r.top<TOPS||r.bottom>vh)&&!b.closest('.tbx')){b.scrollIntoView(")
# re-check on every real action; remember the actions the steps wait for
rep("TOUR.log=[];\nconst NOTOUR=", """TOUR.log=[];TOUR.f={};
document.addEventListener('click',e=>{if(!TOUR.on)return;const q=s=>e.target.closest&&e.target.closest(s);if(q('#coach'))return;
 if(q('[data-door]'))TOUR.f.door=1;if(q('[data-tcol],[data-blogo],.blg,[data-dfam],[data-dmulti]'))TOUR.f.find=1;if(q('[data-mode]'))TOUR.f.view=1;if(q('[data-tvadj]'))TOUR.f.adj=1;
 setTimeout(tourSync,90);clearTimeout(TOUR.rpT);TOUR.rpT=setTimeout(()=>{if(TOUR.on){TOUR.repos=1;tourPaint();}},480);/* re-dock after the app's own scroll (land) settles */},true);
document.addEventListener('input',e=>{if(!TOUR.on)return;if(e.target&&/^(tsq|mdq)$/.test(e.target.id)&&e.target.value.trim().length>1)TOUR.f.find=1;setTimeout(tourSync,150);},true);
document.addEventListener('change',e=>{if(!TOUR.on)return;if(e.target&&e.target.closest&&e.target.closest('.tfind'))TOUR.f.find=1;setTimeout(tourSync,120);},true);
/* the bubble never sits on its target: for 3s after each paint, if a late image or the app's own scroll moved the target under
   the bubble, dock it again (only when the target and bubble fit on screen together) */
{const _tp=tourPaint;tourPaint=function(){_tp.apply(this,arguments);
 /* QA r9: a NEW step's bubble stays invisible until its target stops moving (late image, the app's own scroll), then docks and shows: no flash over the photo */
 {const c0=$('coach'),s0=TSTEPS[TOUR.step];if(c0&&s0&&!s0.hand&&TOUR.lastShown!==TOUR.step){TOUR.lastShown=TOUR.step;c0.style.opacity='0';let last='',k=0;clearInterval(TOUR.stI);
  TOUR.stI=setInterval(()=>{const cc=$('coach'),b=tourTarget(s0);if(!cc||!TOUR.on||TSTEPS[TOUR.step]!==s0){clearInterval(TOUR.stI);if(cc)cc.style.opacity='';return;}
   const r=b&&b.getBoundingClientRect(),key=r?[r.top,r.left,r.height].map(Math.round).join():'x';
   if(key===last||++k>22||!b){clearInterval(TOUR.stI);if(b){const q=cc.getBoundingClientRect();if(!(q.bottom<=r.top||q.top>=r.bottom||q.right<=r.left||q.left>=r.right)&&r.height+q.height+90<=innerHeight)coachPlace(cc,b);}cc.style.opacity='';}last=key;},70);}}
 let n=0;clearInterval(TOUR.wI);TOUR.wI=setInterval(()=>{if(!TOUR.on||++n>12){clearInterval(TOUR.wI);return;}
 const s=TSTEPS[TOUR.step];if(!s||s.hand)return;const b=tourTarget(s),c=$('coach');if(!b||!c||c.style.visibility==='hidden')return;const r=b.getBoundingClientRect(),q=c.getBoundingClientRect();
 const over=!(q.bottom<=r.top||q.top>=r.bottom||q.right<=r.left||q.left>=r.right);if(over&&r.height+q.height+90<=innerHeight)coachPlace(c,b);},250);};}
const NOTOUR=""")
rep("TOUR.on=true;TOUR.step=0;TOUR.log=[];", "TOUR.on=true;TOUR.step=0;TOUR.log=[];TOUR.f={};TOUR.lastShown=-1;")
rep("document.querySelectorAll('.bnc').forEach(e=>e.classList.remove('bnc'));", "document.querySelectorAll('.bnc,.tring').forEach(e=>e.classList.remove('bnc','tring'));", 2)
rep("if(b&&!s.hand)b.classList.add('bnc');", "if(b&&!s.hand)b.classList.add(s.ring?'tring':'bnc');")
h = h.replace('</style>', '.tring{outline:3px solid #c8325f;outline-offset:4px;border-radius:14px;box-shadow:0 0 0 8px rgba(200,50,95,.12)}</style>', 1)
open(P, 'w').write(h); print('tour114 ok')
