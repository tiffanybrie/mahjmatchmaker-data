"""FYM v77 (built from v76). Usage: python3 builder/fym_fix_oct23/v77_offer.py <build_dir>
Tiffany Oct 23 2:54pm (phone screenshots): on first open the tour jumped the screen down to the tile grid before she could
take in the "Find Your Mat-ch / I have tiles / I have a mat" screen. Her rule:
 - Opening the app never moves the screen.
 - The tour OFFER pops up right where "Take the 30-second tour" sits (under the two doors): "Want a 30-second tour?"
   Show me / No thanks. No thanks closes it and she uses the tool.
 - Step 1 is the doors themselves ("tiles or mat"), not the tile grid. No scrolling for step 1.
 - Any tip whose target scrolls off screen hides until it is back (it never sits over another part of the tool).
Gate [35] (builder/fym_tour_place_check.py) checks: no scroll on open, offer next to the tour link, step 1 = doors."""
import sys
B = sys.argv[1]; P = B + '/index.html'
h = open(P).read()

def rep(old, new, n=1):
    global h
    c = h.count(old)
    assert c == n, f'expected {n} x {old[:90]!r}, found {c}'
    h = h.replace(old, new)

rep("""{k:'tiles',t:'Step 1 · Your tiles',p:'Pick your tile set to start. Have a mat instead? Tap \\u201cI have a mat\\u201d.',b:'#s-tiles .tgrid button,#s-tiles .dsets button,#s-tiles .door',done:()=>S.set!=null},""",
    """{k:'tiles',t:'Step 1 · Tiles or mat',p:'Start with what you have: tap \\u201cI have tiles\\u201d or \\u201cI have a mat\\u201d, then pick yours just below.',b:'#s-tiles .door',still:true,done:()=>S.set!=null},""")
# the tour starts where she is: no reset scroll, no jump
rep("""function tourStart(){const d=$('tourq');if(d)d.remove();TOUR.prompt=false;doStartOver();TOUR.on=true;TOUR.step=0;TOUR.log=[];TOUR.shown=-1;window.scrollTo({top:0,behavior:'instant'});setTimeout(tourSync,350);}""",
    """function tourStart(){const d=$('tourq');if(d)d.remove();tourOfferClose();TOUR.prompt=false;const fresh=S.set==null&&!S.dmat;if(!fresh){doStartOver();window.scrollTo({top:0,behavior:'instant'});}TOUR.on=true;TOUR.step=0;TOUR.log=[];TOUR.shown=-1;setTimeout(tourSync,fresh?60:350);}
/* v77: first open = a small offer bubble right under the two doors, where "Take the 30-second tour" sits; the screen never moves */
function tourOfferClose(){const o=$('coach');if(o&&o.dataset.step==='offer')o.remove();TOUR.offer=false;}
function tourOfferShow(){if(TOUR.on||TOUR.offer)return;const l=document.querySelector('#s-tiles [data-tour]');if(!l)return;const r=l.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)return;TOUR.offer=true;
 const c=document.createElement('div');c.id='coach';c.className='coach';c.dataset.step='offer';c.setAttribute('role','dialog');c.setAttribute('aria-live','polite');
 c.innerHTML='<b>Want a 30-second tour?</b>I\\u2019ll walk you through it: pick your tiles or mat, swipe, add racks, get your match card.<div class="cr"><span><button type="button" class="sk" data-tour-skip>No thanks</button></span><span><button type="button" data-tour-go>Show me \\u2665</button></span></div>';
 document.body.appendChild(c);tourOfferPlace();}
function tourOfferPlace(){const c=$('coach');if(!c||c.dataset.step!=='offer')return;const l=document.querySelector('#s-tiles [data-tour]');if(!l){c.remove();TOUR.offer=false;return;}
 const vw=document.documentElement.clientWidth||innerWidth,w=Math.min(420,vw-24),r=l.getBoundingClientRect();c.style.width=w+'px';c.style.right='auto';c.style.margin='0';c.style.bottom='';
 c.style.left=Math.round(Math.max(12,Math.min(vw-w-12,r.left+r.width/2-w/2)))+'px';c.style.top=Math.round(r.bottom+8)+'px';c.style.visibility=(r.bottom<56||r.top>innerHeight)?'hidden':'';}""")
rep("""setTimeout(()=>{if(S.set==null&&!NOTOUR&&!LS.get('fym_tour')&&!TOUR.on)tourStart();},1200);""",
    """setTimeout(()=>{if(S.set==null&&!NOTOUR&&!LS.get('fym_tour')&&!TOUR.on)tourOfferShow();},1200);""")
rep("""if(q('[data-tour-skip]')){tourEnd(true);return;}""", """if(q('[data-tour-skip]')){if(TOUR.offer){tourOfferClose();LS.set('fym_tour','skipped');return;}tourEnd(true);return;}
 if(q('[data-tour-go]')){tourStart();return;}""")
# steps marked still never scroll the page; every tip hides while its target is off screen (no tip over another part of the tool)
rep("""if(fresh&&b){/* every new step brings its own area into view */""", """if(fresh&&b&&!s.still){/* every new step brings its own area into view */""")
rep("""let tsc=0;addEventListener('scroll',()=>{if(!TOUR.on||!TSTEPS[TOUR.step].hand)return;""",
    """let tso=0;addEventListener('scroll',()=>{if(TOUR.offer){cancelAnimationFrame(tso);tso=requestAnimationFrame(tourOfferPlace);return;}if(!TOUR.on||TSTEPS[TOUR.step].hand)return;cancelAnimationFrame(tso);tso=requestAnimationFrame(()=>{const c=$('coach'),b=tourTarget(TSTEPS[TOUR.step]);if(!c||!b)return;const r=b.getBoundingClientRect(),seen=r.bottom>56&&r.top<innerHeight;c.style.visibility=seen?'':'hidden';if(seen&&TSTEPS[TOUR.step].still){const h=c.offsetHeight;c.style.top=Math.round(r.bottom+10+h<=innerHeight-10?r.bottom+10:Math.max(64,r.top-10-h))+'px';}});},{passive:true});
let tsc=0;addEventListener('scroll',()=>{if(!TOUR.on||!TSTEPS[TOUR.step].hand)return;""")
# step 1 tip sits right under the doors (where the tour link is), never above them over the title, never scrolling
rep(""" coachPlace(c,b);const st=TOUR.step;clearTimeout(TOUR.rp);TOUR.rp=setTimeout(()=>{/* the card preview draws late and moves the page: re-place once */if(TOUR.on&&TOUR.step===st&&!s.hand){""",
    """ if(s.still&&b){const vw=document.documentElement.clientWidth||innerWidth,w=Math.min(420,vw-24),r=b.getBoundingClientRect(),hh=c.offsetHeight;c.style.width=w+'px';c.style.right='auto';c.style.margin='0';c.style.bottom='';c.style.left=Math.round(Math.max(12,Math.min(vw-w-12,r.left+r.width/2-w/2)))+'px';c.style.top=Math.round(r.bottom+10+hh<=innerHeight-10?r.bottom+10:Math.max(64,r.top-10-hh))+'px';c.style.visibility=(r.bottom<56||r.top>innerHeight)?'hidden':'';return;}
 coachPlace(c,b);const st=TOUR.step;clearTimeout(TOUR.rp);TOUR.rp=setTimeout(()=>{/* the card preview draws late and moves the page: re-place once */if(TOUR.on&&TOUR.step===st&&!s.hand){""")
open(P, 'w').write(h)
print('v77 patched')
