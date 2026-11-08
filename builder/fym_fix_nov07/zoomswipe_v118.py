#!/usr/bin/env python3
"""FYM 1.18: swipe while zoomed (Tiffany Nov 7 8:24pm: "when mat is zoomed in you can't swipe right or left. Can this be changed?").

Before: in the shared zoomer(), once a card was zoomed (z.s>1) every drag only panned the photo, so the card could not be swiped.
After (one change in zoomer(), so it covers the mat deck in both doors, the tiles-door/mat-door decks and the table view, S.zs.tvz):
  * a drag pans the zoomed photo exactly as before (vertical / diagonal included);
  * once the photo's left/right EDGE is reached, the extra horizontal drag (past a 16px dead zone, drag at <=45deg) moves the CARD
    like a normal swipe (stamps fade in); let go past 75px and it flies (right = heart, left = X); short of that it springs back;
  * a fast horizontal flick (>0.65 px/ms over the last 100ms up to the lift, >50px, mostly horizontal) swipes from anywhere (a pan
    that stops before the finger lifts never counts as a flick); the flick's own pan is
    undone first so the zoom spot that carries to the next card is where she left it;
  * a pan no longer arms double-tap (a quick tap right after panning used to zoom out);
  * zoom level + spot still persist to the next card (S.zs key, unchanged); X / heart buttons untouched; cards that cannot be swiped
    (sw.ok() false: chosen mat / locked mat / tile peek) only pan, as before.
Gate [164] checks the marker + runs builder/fym_fix_nov07/zoomswipe_check.js (the page's own zoomer in node with fake pointer events).

Usage: python3 builder/fym_fix_nov07/zoomswipe_v118.py <build_dir>   (idempotent; run after the 1.18 data patches)
"""
import os, sys

MARK = '/*v118 zoom swipe*/'
REPL = [
    # 1. state: zsw = card is being swiped out of a zoomed pan, vs = recent pointer samples for flick speed
    ("const pts=new Map();let st=null,pinch=null,last=0,dx=0,lock=null;const sw=opt.swipe;",
     "const pts=new Map();let st=null,pinch=null,last=0,dx=0,lock=null,zsw=false,vs=[];const sw=opt.swipe;" + MARK +
     "const ZSW={dead:16,fly:75,v:0.65};"),
    # 2. pointerdown: reset
    ("st={x:e.clientX,y:e.clientY,zx:z.x,zy:z.y,py:e.clientY};dx=0;lock=null;host.style.transition='none';",
     "st={x:e.clientX,y:e.clientY,zx:z.x,zy:z.y,py:e.clientY};dx=0;lock=null;zsw=false;vs=[{x:e.clientX,t:performance.now()}];host.style.transition='none';"),
    # 3. pointermove while zoomed: pan, and swipe with whatever the edge stops
    ("if(z.s>1){z.x=st.zx+ddx;z.y=st.zy+ddy;clamp();apply(false);return;}",
     "if(z.s>1){const tn=performance.now();vs.push({x:e.clientX,t:tn});while(vs.length>2&&tn-vs[0].t>100)vs.shift();"
     "if(lock===null&&Math.hypot(ddx,ddy)>10)lock='z';const wx=st.zx+ddx;z.x=wx;z.y=st.zy+ddy;clamp();apply(false);"
     "const ov=wx-z.x;"
     "if(sw&&sw.ok()&&Math.abs(ov)>ZSW.dead&&Math.abs(ddx)>=Math.abs(ddy)){zsw=true;dx=ov-Math.sign(ov)*ZSW.dead;"
     "host.style.transform=`translateX(${dx}px)`;sw.yes.style.opacity=Math.max(0,Math.min(1,dx/80));sw.no.style.opacity=Math.max(0,Math.min(1,-dx/80));}"
     "else if(zsw){zsw=false;dx=0;host.style.transform='';sw.yes.style.opacity=0;sw.no.style.opacity=0;}"
     "return;}"),
    # 4. pointerup while zoomed: fly past the edge or on a flick, else spring back
    ("if(sw&&st&&z.s===1&&lock==='x'){",
     "if(sw&&st&&z.s>1&&!pinch){let v=0;const tu=performance.now();vs.push({x:e.clientX,t:tu});while(vs.length>2&&tu-vs[0].t>100)vs.shift();"
     "{const a=vs[0],b=vs[vs.length-1];v=(b.x-a.x)/Math.max(1,b.t-a.t);}"
     "const tdx=e.clientX-st.x,tdy=e.clientY-st.y,far=zsw&&Math.abs(dx)>ZSW.fly,"
     "flick=Math.abs(v)>ZSW.v&&Math.abs(tdx)>50&&Math.abs(tdx)>Math.abs(tdy)*1.5&&Math.sign(v)===Math.sign(tdx);"
     "if(sw.ok()&&(far||flick)){const yes=far?dx>0:v>0;if(!zsw){z.x=st.zx;z.y=st.zy;clamp();apply(false);}zsw=false;dx=0;sw.fly(yes);st=null;return;}"
     "if(zsw){host.style.transition='transform .2s';host.style.transform='';sw.yes.style.opacity=0;sw.no.style.opacity=0;}zsw=false;dx=0;}"
     "if(sw&&st&&z.s===1&&lock==='x'){"),
]


def patch(b):
    p = os.path.join(b, 'index.html')
    h = open(p).read()
    if MARK in h:
        print('zoomswipe_v118: already applied'); return 0
    for old, new in REPL:
        n = h.count(old)
        if n != 1:
            print(f'zoomswipe_v118: anchor found {n}x (need 1): {old[:70]}'); return 1
        h = h.replace(old, new)
    open(p, 'w').write(h)
    print('zoomswipe_v118: applied (4 edits in zoomer())'); return 0


if __name__ == '__main__':
    sys.exit(patch(sys.argv[1]))
