"""Pinned Find Your Mat-ch reel v2 (Nov 8 2026): the app half, rebuilt on fresh recordings of the LIVE site app (v118, cap2.py).
Tiffany Nov 8 2:53-3:02pm (FEEDBACK-nov08.md): phone CENTERED and BIG, camera only moves straight in/out (zoom about the action,
never a sideways pan), close zoom on Brownstone Bloom, latest racks UI (rack right under the mat), 'Make it official' big on the phone,
card big, shop list with live stock (Sunday sold out) + code MAHJMATCH, 'See it together. Save it. Share it. Shop it.', end card
'Find Your Mat-ch: tiles, mats and racks across brands' (no 'never ask again'). Local t=0 == 19.6s in the final reel.
Usage: python3 reel2.py frames [a-b ...] | stills t1 t2 ...   -> /dev/shm/pin2/{frames,out}"""
import json, os, sys, glob
O = '/dev/shm/pin2'; os.environ['TMPDIR'] = f'{O}/tmp'; os.makedirs(f'{O}/tmp', exist_ok=True)
from playwright.sync_api import sync_playwright
R = '/home/claude/mahjmatchmaker-data'
FONTS = f'file://{R}/scripts/social/tileprofile/fonts'
F = lambda p: 'file://' + p
LG = '/dev/shm/introv4/logos/'   # holiday-nov1/intro/build/v5_prep.py logos
ALLP = ['omm','missm','myfair','middlemain','bb','bambird','squad','britt','plm','cmc','bespoke','virora','ar','mood','minimahjer','macmiller','toppe','amahj','mahjon','vine','hiphip','bam','mahjongco','studios','ilovemahj','splash','wren','press','royal','soiree','register','lbb','yolo','maison','noli']  # code partners; no Tigre de Tartan, no Sunday, no Mahjong Row, no YMI
CFG = dict(LOGOS=[F(LG + n + '.png') for n in ALLP], R0=F(f'{O}/rec0/f/'), RA=F(f'{O}/recA/f/'), RP=F(f'{O}/recP/f/'), RB=F(f'{O}/recB/f/'),
           FL=F(f'{R}/assets/brand/flame-heart.png'))
DUR = 39.3
HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Cap;src:url(__F__/Caprasimo.ttf)}
@font-face{font-family:Bit;src:url(__F__/bitter-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:PF;src:url(__F__/playfair-display-latin-600-italic.woff2);font-style:italic}
:root{--navy:#062a55;--pink:#e0547f;--cream:#fdf6ee;--blush:#f7b6c8}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;position:relative;background:var(--cream);font-family:Bit}
.sc{position:absolute;inset:0;display:none;overflow:hidden}
.cr{background:radial-gradient(ellipse at 50% 42%,#fffaf4 0%,var(--cream) 60%,#f6e9dc 100%)}
.nv{background:var(--navy)}
.plate{position:absolute;left:0;right:0;text-align:center;z-index:50}
.plate span{display:inline-block;font:400 80px/1.08 Cap;color:var(--navy);background:#fff;padding:22px 50px 30px;border-radius:34px;box-shadow:0 14px 40px rgba(60,30,40,.28);white-space:nowrap;text-align:center}
.cam{position:absolute;left:0;top:0;transform-origin:0 0}
.bez{position:absolute;left:-28px;top:-28px;width:836px;height:1834px;border-radius:120px;background:#ffffff;box-shadow:0 34px 80px rgba(90,50,60,.22),inset 0 0 0 5px #e4e1de}
.bez i{position:absolute;width:11px;background:#e9e6e3;border-radius:4px}
.sb{position:absolute;left:0;top:0;width:780px;height:90px;background:#fff;font:600 34px -apple-system,Helvetica,Arial;color:#111}
.isl{position:absolute;left:276px;top:20px;width:228px;height:62px;background:#000;border-radius:40px}
.scr{position:absolute;left:0;top:0;width:780px;height:1778px;border-radius:92px;overflow:hidden;background:#fff}
.apz{position:absolute;left:0;top:90px;width:780px;height:1688px}.scr img.f{position:absolute;left:0;top:0;width:780px;height:1688px}
.ring{position:absolute;border-radius:50%;border:9px solid var(--pink)}
.stamp{position:absolute;width:200px;height:200px;margin:-100px 0 0 -100px;border-radius:50%;display:flex;align-items:center;justify-content:center;font:400 130px/1 Arial;color:#fff;box-shadow:0 20px 50px rgba(0,0,0,.30);border:10px solid #fff}
.tick{position:absolute;left:0;width:1080px;overflow:hidden}.tick .row{position:absolute;top:0;left:0;display:flex;gap:22px;white-space:nowrap}
.chip{flex:none;width:190px;height:120px;background:#fff;border-radius:22px;box-shadow:0 10px 26px rgba(0,0,0,.18);display:flex;align-items:center;justify-content:center}.chip img{max-width:172px;max-height:104px;object-fit:contain}
.pill{display:inline-block;font:700 46px/1.1 Bit;padding:18px 42px;border-radius:60px;white-space:nowrap}
.code{position:absolute;left:0;right:0;text-align:center;z-index:60}
.code span{display:inline-block;background:var(--pink);color:#fff;font:700 62px/1 Bit;letter-spacing:2px;padding:26px 56px;border-radius:80px;box-shadow:0 16px 40px rgba(120,20,60,.35);border:6px solid #fff}
.ln{position:absolute;left:0;right:0;text-align:center;font:400 118px/1 Cap;color:#fff;white-space:nowrap}
</style></head><body>
<div id="app" class="sc cr"><div class="cam" id="cam"><div class="bez"><i style="left:-9px;top:300px;height:80px"></i><i style="left:-9px;top:430px;height:140px"></i><i style="left:-9px;top:600px;height:140px"></i><i style="right:-9px;top:470px;height:210px"></i></div><div class="scr"><div class="sb"><span style="position:absolute;left:96px;top:24px">9:41</span><span style="position:absolute;right:86px;top:26px;font-size:26px;letter-spacing:3px">▂▄▆ ◔ ▭</span><div class="isl"></div></div><div class="apz"><img class="f" id="fr"><svg id="spot" width="780" height="1688" style="position:absolute;left:0;top:0"></svg><div id="ov" style="position:absolute;inset:0"></div></div></div></div></div>
<div id="see" class="sc nv">
 <div class="ln" id="l1" style="top:470px">See it together.</div>
 <div class="ln" id="l2" style="top:700px;color:var(--blush)">Save it.</div>
 <div class="ln" id="l3" style="top:930px">Share it.</div>
 <div class="ln" id="l4" style="top:1160px;color:var(--blush)">Shop it.</div>
 <div style="position:absolute;left:0;right:0;top:1330px;text-align:center" id="l4c"><span class="pill" style="background:#fff;color:var(--navy);font-size:40px;padding:14px 36px">code MAHJMATCH</span></div>
</div>
<div id="end" class="sc nv">
 <img src="__FL__" id="fh" style="position:absolute;left:465px;top:240px;width:150px">
 <div style="position:absolute;left:0;right:0;top:450px;text-align:center" id="en"><span style="display:inline-block;font:400 120px/1 Cap;color:#fff;white-space:nowrap">Find <span style="font:italic 600 126px/1 PF;color:var(--blush)">Your</span> Mat-ch</span></div>
 <div style="position:absolute;left:0;right:0;top:660px;text-align:center;font:400 96px/1.12 Cap;color:var(--blush)" id="es">tiles, mats and racks<br>across brands</div>
 <div style="position:absolute;left:0;right:0;top:960px;text-align:center" id="eb"><span class="pill" style="background:var(--pink);color:#fff;font-size:50px;letter-spacing:5px;padding:20px 54px">LINK IN BIO</span></div>
 <div style="position:absolute;left:0;right:0;top:1090px;text-align:center;font:700 40px Bit;color:#fff;opacity:.9" id="eu">free at mahjmatchmaker.com</div>
 <div id="eticks"></div>
</div>
<div class="plate" id="plate"><span id="plt"></span></div>
<div class="code" id="code"><span>Use code MAHJMATCH</span></div>
<script>
const C=__CFG__;
const cl=x=>Math.min(Math.max(x,0),1), eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}, eb=x=>{x=cl(x);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const $=id=>document.getElementById(id);
function plate(txt,k,y){const p=$('plate');if(!txt){p.style.display='none';return;}p.style.display='block';p.style.top=(y||170)+'px';
 if($('plt').innerHTML!==txt)$('plt').innerHTML=txt;$('plt').style.transform=`scale(${0.86+0.14*eb(k/0.3)})`;p.style.opacity=cl(k/0.12);}
function code(k,y){const c=$('code');if(k<=0){c.style.display='none';return;}c.style.display='block';c.style.top=(y||1700)+'px';c.style.opacity=cl(k/0.15);c.firstChild.style.transform=`scale(${0.7+0.3*eb(k/0.35)})`;}
function spot(holes,a){ // spotlight (#39): dim the app except soft cut-outs (frame px)
 if(!holes.length||a<=0.001){$('spot').innerHTML='';return;}
 $('spot').innerHTML=`<defs><filter id="bl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter><mask id="mk"><rect width="780" height="1688" fill="#fff"/>${holes.map(([x,y,w,h,r])=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r||22}" fill="#000" filter="url(#bl)"/>`).join('')}</mask></defs><rect width="780" height="1688" fill="rgb(6,16,38)" fill-opacity="${0.58*a}" mask="url(#mk)"/>`;}
function sp(L,a,b,holes){const k=cl((L-a)/0.2)*cl((b-L)/0.2);if(L>=a&&L<=b){spot(holes,k);return true;}return false;}
function pw(P,L){if(L<=P[0][0])return P[0][1];for(let i=1;i<P.length;i++){if(L<=P[i][0]){const [a,x]=P[i-1],[b,y]=P[i];return x+(y-x)*(L-a)/(b-a);}}return P[P.length-1][1];}
const BADB=new Set([1,3,10,12,22,24,35]); // recB screencast frames where the mat thumbnail sits shifted left (layout glitch): skip
function frame(base,i){i=Math.max(0,Math.round(i));while(base===C.RB&&BADB.has(i))i++;const u=base+String(i).padStart(5,'0')+'.jpg';const f=$('fr');if(f.dataset.u!==u){f.src=u;f.dataset.u=u;}}
// CAMERA: the phone is centered at base zoom K0; zooming happens ABOUT the action point (ax,ay) so the camera moves straight in, never sideways.
const K0=1.25;
function camF(k,ax,ay,fy){ // anchor (ax,ay) in frame px; fy = frame y shown at screen centre when k==K0. As the zoom goes in, the
 // action point travels in a straight line to the middle of the screen (a dolly toward it), so close-ups are centred and big.
 const c=cl((k-K0)/0.6), X=540+(ax-390)*K0*(1-c), Y=960+(ay-fy)*K0*(1-c); $('cam').style.transform=`translate(${X-ax*k}px,${Y-(ay+90)*k}px) scale(${k})`;}
function cam(keys,L){let a=keys[0],b=keys[keys.length-1];for(let i=1;i<keys.length;i++){if(L<=keys[i][0]){a=keys[i-1];b=keys[i];break;}}
 const q=b[0]>a[0]?eio((L-a[0])/(b[0]-a[0])):1; const m=(i)=>a[i]+(b[i]-a[i])*q; camF(m(1),m(2),m(3),m(4));}
function ring(x,y,k){if(k<0||k>1)return '';const r=40+60*eo(k);return `<div class="ring" style="left:${x-r}px;top:${y-r}px;width:${2*r}px;height:${2*r}px;opacity:${1-k}"></div>`;}
function stamp(x,y,k,yes){if(k<0||k>0.5)return '';const s=k<0.25?2.2-1.2*eb(k/0.25):1;const o=k>0.4?1-(k-0.4)/0.1:cl(k/0.08);return `<div class="stamp" style="left:${x}px;top:${y}px;background:${yes?'#e0547f':'#7a6a85'};transform:scale(${s}) rotate(${yes?12:-12}deg);opacity:${o}">${yes?'&hearts;':'&#10005;'}</div>`;}
function mkTick(host,logos,rows,y0,dy,off){for(let r=0;r<rows;r++){const t=document.createElement('div');t.className='tick';t.style.top=(y0+r*dy)+'px';t.style.height='120px';const row=document.createElement('div');row.className='row';
  let L=logos.filter((u,i)=>(i+off)%rows===r);while(L.length<8)L=L.concat(L);L.concat(L).concat(L).forEach(u=>{const c=document.createElement('div');c.className='chip';c.innerHTML=`<img src="${u}">`;row.appendChild(c);});
  t.appendChild(row);t.dataset.dir=r%2?1:-1;host.appendChild(t);}}
mkTick($('eticks'),C.LOGOS,4,1250,145,1);
function ticks(host,t,a,sp){[...host.children].forEach((e,i)=>{const d=+e.dataset.dir;const w=e.firstChild.scrollWidth/3;const x=((t*sp*(1+0.15*i))%w);e.firstChild.style.transform=`translateX(${d<0?-x-w*0.2:x-w}px)`;e.style.opacity=a;});}
// [k, anchorX, anchorY, fy]  (anchor x 390 == dead centre)
const SC=[['tiles',0,2.6],['sw',2.6,7.8],['pick',7.8,10.6],['racks',10.6,15.0],['off',15.0,17.2],['card',17.2,22.8],['shop',22.8,27.8],['see',27.8,32.2],['end',32.2,39.35]];
const DIV={tiles:'app',sw:'app',pick:'app',racks:'app',off:'app',card:'app',shop:'app',see:'see',end:'end'};
window.render=function(t){let cur=SC[SC.length-1];for(const s of SC)if(t>=s[1]&&t<s[2]){cur=s;break;}
 const [id,a]=cur,L=t-a;for(const d of ['app','see','end'])$(d).style.display=DIV[id]===d?'block':'none';
 plate('',0); code(0); $('ov').innerHTML=''; spot([],0);
 if(id==='tiles'){ // home -> type Sunday -> tap Sunday -> Mat-ching
  frame(C.R0,pw([[0,0],[0.55,0],[0.6,2],[1.25,10],[1.3,11],[1.8,11],[1.85,12],[2.3,30],[2.6,48]],L));
  cam([[0,K0,390,725,820],[0.5,1.55,205,725,820],[0.62,K0,390,840,1000],[1.25,K0,390,1380,1100],[1.6,1.7,140,1380,1100],[1.85,1.7,140,1380,1100],[2.3,K0,390,900,900]],L);
  sp(L,0.1,0.62,[[20,650,370,150,70]])||sp(L,1.25,1.95,[[18,1222,244,322,26]]);
  $('ov').innerHTML=ring(205,725,(L-0.35)/0.4)+ring(140,1380,(L-1.6)/0.4); if(L<0.6)plate('Start with your tiles',L);}
 if(id==='sw'){ // ♥ Brownstone Bloom, ✕ Chinoiserie Songbird, ♥ Carson Vintage, ♥ Knox
  frame(C.RA,pw([[0,0],[0.9,0],[1.3,5],[1.35,6],[2.15,6],[2.55,12],[2.6,13],[3.4,31],[3.7,32],[3.75,33],[4.45,39],[4.7,40],[5.2,40]],L));
  cam([[0,K0,390,1000,950],[0.7,1.38,390,1000,950],[5.2,1.42,390,1000,950]],L);
  sp(L,0.05,5.4,[[24,650,732,720,30]]); $('ov').innerHTML=stamp(390,1000,(L-0.75)/0.9,true)+stamp(390,1000,(L-2.0)/0.9,false)+stamp(390,1000,(L-3.3)/0.9,true)+stamp(390,1000,(L-4.45)/0.9,true);
  if(L<0.75)plate('Swipe the mats',L);}
 if(id==='pick'){ // which suitor is the one? -> zoom straight in on Brownstone Bloom, tap -> racks step opens on the mat (close)
  if(L<1.5){frame(C.RP,0); cam([[0,K0,598,1240,1150],[0.45,K0,598,1240,1150],[1.3,2.6,598,1240,1150]],L);
   sp(L,0.2,1.6,[[500,1120,196,256,26]]); $('ov').innerHTML=ring(598,1240,(L-1.0)/0.45); if(L<0.7)plate('Pick your favorite',L);}
  else {frame(C.RB,0); cam([[1.5,2.7,390,715,900],[2.8,2.45,390,715,900]],L);}}
 if(id==='racks'){ // mat on top, rack right under it: ✕ Teal Wood, ♥ Bam Bird Boutique Walnut, ♥ Peace Love Mahjong Oak
  frame(C.RB,pw([[0,0],[1.35,2],[1.6,9],[1.65,10],[2.45,11],[2.7,21],[2.75,22],[3.55,23],[3.8,25],[4.4,25]],L));
  cam([[0,2.45,390,715,900],[0.9,1.32,390,1000,1060],[4.4,1.36,390,1000,1060]],L);
  sp(L,0.9,4.6,[[200,530,380,380,26],[20,1010,740,640,30]]);
  $('ov').innerHTML=stamp(390,1300,(L-1.0)/0.9,false)+stamp(390,1300,(L-2.1)/0.9,true)+stamp(390,1300,(L-3.2)/0.9,true); if(L>0.75&&L<1.6)plate('Add racks',L-0.75);}
 if(id==='off'){ // the tray: 2 suitors -> 'Make it official ♥' big
  frame(C.RB,pw([[0,64],[0.3,70],[1.45,76],[1.5,77],[2.2,95]],L));
  cam([[0,K0,630,1250,1150],[0.25,K0,630,1250,1150],[1.0,2.9,630,1250,1150],[1.55,2.9,630,1250,1150],[2.2,K0,390,1250,1150]],L);
  sp(L,0.2,1.6,[[495,1170,270,160,44]]); $('ov').innerHTML=ring(630,1250,(L-1.15)/0.45); if(L<1.0)plate('Make it official',L,170);}
 if(id==='card'){ // card big on the phone; views: Post 4:5 mood board -> Story close up -> Story mood board -> Post
  frame(C.RB,L<1.7?112:L<3.2?153:L<4.4?155:158);
  const fy=L<1.7?1000:L<4.4?1080:1000; cam([[0,K0,390,1000,900],[0.6,1.42,390,fy,fy],[5.6,1.48,390,fy,fy]],L);
  if(L<1.7)plate('Your match card',L,150); else if(L<3.2)plate('Story · close up',L-1.7,150); else if(L<4.4)plate('Story · mood board',L-3.2,150); else plate('Post · save or share',L-4.4,150);}
 if(id==='shop'){ // shop list: live stock (Sunday sold out), mat + 2 racks shoppable, code MAHJMATCH
  frame(C.RB,pw([[0,158],[0.6,176],[1.0,195]],L));
  cam([[0,K0,390,740,760],[1.0,1.36,390,740,740],[5.0,1.4,390,740,740]],L);
  sp(L,1.0,2.0,[[20,490,740,130,22]])||sp(L,2.0,5.2,[[20,630,740,430,22]]);
  $('ov').innerHTML=ring(670,550,(L-1.15)/0.45)+ring(690,696,(L-2.1)/0.45)+ring(690,840,(L-2.3)/0.45)+ring(690,984,(L-2.5)/0.45);
  if(L<1.0)plate('Shop your match',L,150); else if(L<2.0)plate('Live stock check',L-1.0,150); else plate('Shop each piece',L-2.0,150);
  code(L-2.6,1640);}
 if(id==='see'){const ln=(e,s)=>{const k=eb((L-s)/0.35);$(e).style.opacity=cl((L-s)/0.12);$(e).style.transform=`scale(${0.75+0.25*k})`;};
  ln('l1',0.1);ln('l2',0.9);ln('l3',1.7);ln('l4',2.5);ln('l4c',2.95);}
 if(id==='end'){$('fh').style.transform=`scale(${eb(L/0.45)})`;
  const ap=(e,s)=>{$(e).style.opacity=cl((L-s)/0.2);$(e).style.transform=`scale(${0.82+0.18*eb((L-s)/0.4)})`;};
  ap('en',0.15);ap('es',0.55);ap('eb',1.0);ap('eu',1.2);
  $('eb').firstChild.style.transform=`scale(${L<1.6?1:1+0.04*Math.sin(Math.PI*2*((L-1.6)/0.8))})`; ticks($('eticks'),t,cl((L-1.0)/0.3),150);}
};
</script></body></html>"""
def page():
    return HTML.replace('__F__', FONTS).replace('__FL__', CFG['FL']).replace('__CFG__', json.dumps(CFG))
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'frames'
    out = f'{O}/out'; os.makedirs(out, exist_ok=True); open(f'{O}/reel2.html', 'w').write(page()); FPS = 30
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(f'file://{O}/reel2.html'); pg.wait_for_timeout(3000)
        wait = "()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})))"
        if mode == 'frames':
            fd = f'{O}/frames'; os.makedirs(fd, exist_ok=True)
            rng = list(range(0, round(DUR * FPS)))
            if len(sys.argv) > 2: rng = [n for a in sys.argv[2:] for n in range(int(a.split('-')[0]), int(a.split('-')[1]) + 1)]
            for n in rng:
                pg.evaluate(f"render({n / FPS})"); pg.evaluate(wait); pg.screenshot(path=f'{fd}/{n:04d}.jpg', type='jpeg', quality=92)
        else:
            for tt in [float(x) for x in sys.argv[2:]]:
                pg.evaluate(f"render({tt})"); pg.evaluate(wait); pg.wait_for_timeout(150); pg.screenshot(path=f'{out}/t{tt:05.2f}.jpg', type='jpeg', quality=85)
        b.close()
