"""Find Your Mat-ch LAUNCH REEL REDO (Nov 3 2026), to swap into the Oct 27 launch post (Dancing On My Own, 58.0s).
Tiffany Nov 3 4:33-4:37pm: keep the original calm cut's cuts, length and song sync; fix its errors (every card on screen
acknowledged; the phone never moves on a swipe, only the card flies); latest app (v113); holiday-intro-v5 standard.
0.00-24.06s = the ORIGINAL calm cut unchanged (ever-burning question, catalog wall, Find Your Mat-ch is HERE, Today you're the
matchmaker) -> 24.06s on = rebuilt on real 2x screen recordings with a moving camera (cap.py):
24.06 Start with your tiles | 26.76 Swipe the mats (♥ Brownstone Bloom lands 27.71 = 'watching you kiss her', same as before)
29.46 ✕ Chinoiserie Songbird (30.31) | 31.62 ♥ Carson Vintage + ♥ Midnight Garden | 33.40 Pick your favorite
36.06 Add racks (zoom, Wood, ✕ Teal Wood, ♥ Walnut, ♥ Oak) | 40.03 match card | 43.73 cross-brand match-card wall
47.00 Shop it with code MAHJMATCH (Discount code under every partner piece) | 51.50-58.00 end card.
19.20-20.68 = NEW depth wall of everyday partner mats (dwall.py) over the tail of the original 'is HERE' hold.
Usage: python3 reel.py frames [a-b ...] | stills t1 t2 ...  -> /dev/shm/lr/{frames,out}"""
import json, os, sys, shutil, glob
O = '/dev/shm/lr'; os.environ['TMPDIR'] = '/dev/shm/introv2/tmp'
from playwright.sync_api import sync_playwright
R = '/home/claude/mahjmatchmaker-data'
FONTS = f'file://{R}/scripts/social/tileprofile/fonts'
F = lambda p: 'file://' + p
def rt(r): d = json.load(open(f'{O}/{r}/marks.json')); Fr = d['frames']; return [round(x - Fr[0], 3) for x in Fr]
LG = '/dev/shm/introv4/logos/'
ALLP = ['omm','missm','myfair','middlemain','bb','bambird','squad','britt','plm','cmc','bespoke','virora','ar','mood','minimahjer','macmiller','toppe','amahj','mahjon','vine','hiphip','bam','mahjongco','studios','ilovemahj','splash','wren','press','royal','soiree','register','lbb','yolo','maison','noli']  # code partners; no Tigre de Tartan (affiliate policy), no Sunday; Nov 6: no Mahjong Row (out), no YMI (never on social)
CFG = dict(DW=[F(f) for f in sorted(glob.glob(f'{O}/dwall/*.jpg'))], XC=[F(f) for f in sorted(glob.glob(f'{O}/xcards/*.png'))], LOGOS=[F(LG + n + '.png') for n in ALLP], CARD=F(f'{O}/recB/storycard.png'),
           R0=F(f'{O}/rec0/f/'), RA=F(f'{O}/recA/f/'), RP=F(f'{O}/recP/f/'), RB=F(f'{O}/recB/f/'), T0=rt('rec0'), TA=rt('recA'), TP=rt('recP'), TB=rt('recB'),
           FL=F(f'{R}/assets/brand/flame-heart.png'), WM=F(f'{R}/assets/brand/mahjmatchmaker-wordmark-notag.png'))
T_START, T_END = 24.06, 58.0
DW_A, DW_B = 576, 620   # frames 19.20-20.67s: depth wall replaces the tail of the original 'is HERE' hold
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
.plate span{display:inline-block;font:400 76px/1.08 Cap;color:var(--navy);background:#fff;padding:22px 48px 30px;border-radius:32px;box-shadow:0 14px 36px rgba(60,30,40,.20);white-space:nowrap;text-align:center}
.cell{position:absolute;overflow:hidden;background:#fff}.cell img{width:100%;height:100%;object-fit:cover;display:block}
.cam{position:absolute;left:0;top:0;transform-origin:0 0}
.bez{position:absolute;left:-28px;top:-28px;width:836px;height:1834px;border-radius:120px;background:#ffffff;box-shadow:0 34px 80px rgba(90,50,60,.22),inset 0 0 0 5px #e4e1de}
.bez i{position:absolute;width:11px;background:#e9e6e3;border-radius:4px}
.sb{position:absolute;left:0;top:0;width:780px;height:90px;background:#fff;font:600 34px -apple-system,Helvetica,Arial;color:#111}
.isl{position:absolute;left:276px;top:20px;width:228px;height:62px;background:#000;border-radius:40px}
.scr{position:absolute;left:0;top:0;width:780px;height:1778px;border-radius:92px;overflow:hidden;background:#fff}
.apz{position:absolute;left:0;top:90px;width:780px;height:1688px}.scr img.f{position:absolute;left:0;top:0;width:780px;height:1688px}
.ring{position:absolute;border-radius:50%;border:10px solid var(--pink)}
.stamp{position:absolute;width:220px;height:220px;margin:-110px 0 0 -110px;border-radius:50%;display:flex;align-items:center;justify-content:center;font:400 150px/1 Arial;color:#fff;box-shadow:0 20px 50px rgba(0,0,0,.30);border:10px solid #fff}
.tick{position:absolute;left:0;width:1080px;overflow:hidden}.tick .row{position:absolute;top:0;left:0;display:flex;gap:22px;white-space:nowrap}
.chip{flex:none;width:190px;height:120px;background:#fff;border-radius:22px;box-shadow:0 10px 26px rgba(0,0,0,.18);display:flex;align-items:center;justify-content:center}.chip img{max-width:172px;max-height:104px;object-fit:contain}
.mc{position:absolute;border-radius:26px;box-shadow:0 34px 80px rgba(60,30,40,.30)}
.pill{display:inline-block;font:700 46px/1.1 Bit;padding:18px 42px;border-radius:60px;white-space:nowrap}
</style></head><body>
<div id="app" class="sc cr"><div class="cam" id="cam"><div class="bez"><i style="left:-9px;top:300px;height:80px"></i><i style="left:-9px;top:430px;height:140px"></i><i style="left:-9px;top:600px;height:140px"></i><i style="right:-9px;top:470px;height:210px"></i></div><div class="scr"><div class="sb"><span style="position:absolute;left:96px;top:24px">9:41</span><span style="position:absolute;right:86px;top:26px;font-size:26px;letter-spacing:3px">▂▄▆ ◔ ▭</span><div class="isl"></div></div><div class="apz"><img class="f" id="fr"><svg id="spot" width="780" height="1688" style="position:absolute;left:0;top:0"></svg><div id="ov" style="position:absolute;inset:0"></div></div></div></div></div>
<div id="cardsc" class="sc cr"><img id="mcard" class="mc"></div>
<div id="dw" class="sc nv" style="perspective:1500px;perspective-origin:50% 30%"><div id="dwg" style="position:absolute;left:-660px;top:-760px;width:2400px;height:3300px;transform-style:preserve-3d"></div></div>
<div id="wall" class="sc nv"><div id="wg" style="position:absolute;left:0;top:0;width:1080px"></div></div>
<div id="end" class="sc nv">
 <div id="eg" style="position:absolute;left:0;right:0;top:0">
 <img src="__FL__" id="fh" style="position:absolute;left:470px;top:250px;width:140px">
 <div style="position:absolute;left:0;right:0;top:420px;text-align:center;font:400 150px/1.02 Cap;color:#fff" id="nag">Never ask<br>again</div>
 <div style="position:absolute;left:0;right:0;top:760px;text-align:center"><span style="display:inline-block;font:400 92px/1 Cap;color:#fff;white-space:nowrap;position:relative">Find <span style="font:italic 600 96px/1 PF;color:var(--blush)">Your</span> Mat-ch<span style="position:absolute;font:400 34px Bit;margin-left:4px;margin-top:4px">™</span></span></div>
 <div style="position:absolute;left:0;right:0;top:885px;text-align:center;font:italic 600 54px/1.25 PF;color:var(--blush)">Match tiles, mats &amp; racks<br>across brands</div>
 <div style="position:absolute;left:0;right:0;top:1055px;text-align:center"><span class="pill" id="shop" style="background:var(--pink);color:#fff">Shop now · use code MAHJMATCH</span></div>
 <div style="position:absolute;left:0;right:0;top:1180px;text-align:center"><span class="pill" style="background:transparent;border:4px solid #fff;color:#fff;font-size:32px;letter-spacing:4px;padding:12px 34px">LINK IN BIO</span></div>
 </div><div id="eticks"></div>
</div>
<div class="plate" id="plate"><span id="plt"></span></div>
<script>
const C=__CFG__;
const cl=x=>Math.min(Math.max(x,0),1), eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}, eb=x=>{x=cl(x);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const $=id=>document.getElementById(id);
function plate(txt,k,y){const p=$('plate');if(!txt){p.style.display='none';return;}p.style.display='block';p.style.top=(y||330)+'px';
 if($('plt').innerHTML!==txt)$('plt').innerHTML=txt;$('plt').style.transform=`scale(${0.86+0.14*eb(k/0.3)})`;p.style.opacity=cl(k/0.12);}
function spot(holes,a){ // FYM-REEL-RULES #39: dim the app ~58% except soft-edged cut-outs (frame px), holiday intro v2 style
 if(!holes.length||a<=0.001){$('spot').innerHTML='';return;}
 $('spot').innerHTML=`<defs><filter id="bl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="16"/></filter><mask id="mk"><rect width="780" height="1688" fill="#fff"/>${holes.map(([x,y,w,h,r])=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r||22}" fill="#000" filter="url(#bl)"/>`).join('')}</mask></defs><rect width="780" height="1688" fill="rgb(6,16,38)" fill-opacity="${0.58*a}" mask="url(#mk)"/>`;}
function sp(L,a,b,holes){const k=cl((L-a)/0.22)*cl((b-L)/0.22);if(L>=a&&L<=b){spot(holes,k);return true;}return false;}
function fidx(T,t){let lo=0,hi=T.length-1;if(t<=T[0])return 0;while(lo<hi){const m=(lo+hi+1)>>1;if(T[m]<=t)lo=m;else hi=m-1;}return lo;}
function pw(P,L){if(L<=P[0][0])return P[0][1];for(let i=1;i<P.length;i++){if(L<=P[i][0]){const [a,x]=P[i-1],[b,y]=P[i];return x+(y-x)*(L-a)/(b-a);}}return P[P.length-1][1];}
function frame(base,T,t){const i=fidx(T,t);const u=base+String(i).padStart(5,'0')+'.jpg';const f=$('fr');if(f.dataset.u!==u){f.src=u;f.dataset.u=u;}}
function camF(k,fx,fy){$('cam').style.transform=`translate(${540-fx*k}px,${960-(fy+90)*k}px) scale(${k})`;}
function cam(keys,L,t){let a=keys[0],b=keys[keys.length-1];for(let i=1;i<keys.length;i++){if(L<=keys[i][0]){a=keys[i-1];b=keys[i];break;}}
 const q=b[0]>a[0]?eio((L-a[0])/(b[0]-a[0])):1; const dr=Math.sin(t*1.7)*0.012;
 camF((a[1]+(b[1]-a[1])*q)*(1+dr),a[2]+(b[2]-a[2])*q+Math.sin(t*1.1)*6,a[3]+(b[3]-a[3])*q+Math.cos(t*0.9)*6);}
const FULL=[.74,390,572];
function ring(x,y,k){if(k<0||k>1)return '';const r=40+60*eo(k);return `<div class="ring" style="left:${x-r}px;top:${y-r}px;width:${2*r}px;height:${2*r}px;opacity:${1-k}"></div>`;}
function stamp(x,y,k,yes){if(k<0||k>0.48)return '';const s=k<0.25?2.2-1.2*eb(k/0.25):1;const o=k>0.38?1-(k-0.38)/0.1:cl(k/0.08); /* lands 0.075s before the tap, gone 0.13s after it: never sits on the next card */return `<div class="stamp" style="left:${x}px;top:${y}px;background:${yes?'#e0547f':'#7a6a85'};transform:scale(${s}) rotate(${yes?12:-12}deg);opacity:${o}">${yes?'&hearts;':'&#10005;'}</div>`;}
// walls
const WL={};
function mkwall(key,imgs,cols,cw,ch,top){const g=document.createElement('div');g.style.position='absolute';g.style.left='0';g.style.top=top+'px';g.style.display='none';
 const cells=[];let sd=5;const rnd=()=>{sd=(sd*16807)%2147483647;return sd/2147483647};
 imgs.forEach((u,i)=>{const c=i%cols,r=Math.floor(i/cols);const d=document.createElement('div');d.className='cell';d.style.left=(c*cw)+'px';d.style.top=(r*ch)+'px';d.style.width=cw+'px';d.style.height=ch+'px';d.style.boxShadow='inset 0 0 0 3px #fff';d.innerHTML=`<img src="${u}">`;g.appendChild(d);
  const dx=(c+.5)/cols-.5,dy=((r+.5)*ch+top-960)/1920;cells.push([Math.hypot(dx,dy*0.6)+rnd()*0.08,i]);});
 cells.sort((a,b)=>a[0]-b[0]);$('wg').appendChild(g);WL[key]={g,ord:cells.map(x=>x[1]),n:imgs.length};}
mkwall('x',C.XC,3,360,450,-165);
function wall(key,L){for(const k in WL)WL[k].g.style.display=k===key?'block':'none';const W=WL[key];const ch=W.g.children;const n=Math.min(W.n,Math.pow(2,Math.floor(L/0.2)+2));
 W.ord.forEach((ci,j)=>{const d=ch[ci];const on=j<n;d.style.visibility=on?'visible':'hidden';if(on){const born=j<4?0:(Math.floor(Math.log2(j))-1)*0.2;d.style.transform=`scale(${eb((L-born+0.1)/0.3)})`;}});
 W.g.style.transform=`scale(${1+0.05*eio(L/3.27)})`;W.g.style.transformOrigin='540px 960px';}
// logo tickers
function mkTick(host,logos,rows,y0,dy,off){for(let r=0;r<rows;r++){const t=document.createElement('div');t.className='tick';t.style.top=(y0+r*dy)+'px';t.style.height='120px';const row=document.createElement('div');row.className='row';
  let L=logos.filter((u,i)=>(i+off)%rows===r);while(L.length<8)L=L.concat(L);L.concat(L).concat(L).forEach(u=>{const c=document.createElement('div');c.className='chip';c.innerHTML=`<img src="${u}">`;row.appendChild(c);});
  t.appendChild(row);t.dataset.dir=r%2?1:-1;host.appendChild(t);}}
mkTick($('eticks'),C.LOGOS,4,1330,140,1);
function ticks(host,t,a,sp){[...host.children].forEach((e,i)=>{const d=+e.dataset.dir;const w=e.firstChild.scrollWidth/3;const x=((t*sp*(1+0.15*i))%w);e.firstChild.style.transform=`translateX(${d<0?-x-w*0.2:x-w}px)`;e.style.opacity=a;});}
// depth wall: everyday partner mats laid out as a tilted floor the camera glides over (full frame, edge to edge)
(()=>{const g=$('dwg');let sd=9;const rnd=()=>{sd=(sd*16807)%2147483647;return sd/2147483647};for(let r=0;r<11;r++)for(let c=0;c<8;c++){const i=(r*8+c+(r>5?3:0))%C.DW.length;const d=document.createElement('div');d.className='cell';
 d.style.cssText=`left:${c*300}px;top:${r*300}px;width:300px;height:300px;box-shadow:inset 0 0 0 5px #062a55`;d.dataset.b=(rnd()*0.28-0.12).toFixed(2);d.innerHTML=`<img src="${C.DW[i]}">`;g.appendChild(d);}})();
function dwall(L){const g=$('dwg');const q=L/1.48;g.style.transform=`rotateX(${34-6*q}deg) rotateZ(${-9+4*q}deg) translateZ(${-260+440*(0.35*q+0.65*eo(q))}px) translateY(${-160*q}px)`;
 [...g.children].forEach(d=>{const k=eb((L-(+d.dataset.b))/0.35);d.style.transform=`scale(${0.55+0.45*k})`;d.style.opacity=cl((L-(+d.dataset.b))/0.12);});}
const SC=[['dw',19.20,20.68],['tiles',24.06,26.76],['sw1',26.76,29.46],['sw2',29.46,31.62],['sw3',31.62,33.40],['fav',33.40,36.06],['racks',36.06,40.03],['card',40.03,43.73],['xw',43.73,47.0],['shop',47.0,51.5],['end',51.5,58.05]];
const DIV={dw:'dw',tiles:'app',sw1:'app',sw2:'app',sw3:'app',fav:'app',racks:'app',shop:'app',card:'cardsc',xw:'wall',end:'end'};
window.render=function(t){let cur=SC[SC.length-1];for(const s of SC)if(t>=s[1]&&t<s[2]){cur=s;break;}
 const [id,a]=cur,L=t-a;for(const d of ['dw','app','cardsc','wall','end'])$(d).style.display=DIV[id]===d?'block':'none';
 plate('',0); $('ov').innerHTML=''; spot([],0);
 if(id==='dw'){dwall(L);}
 if(id==='tiles'){frame(C.R0,C.T0,pw([[0,0.5],[0.42,1.03],[0.62,2.11],[1.3,3.74],[1.75,4.4],[1.8,4.47],[2.3,5.7],[2.7,7.76]],L));
  cam([[0,...FULL],[0.5,...FULL],[0.95,1.05,390,1150],[1.6,1.18,240,1330],[2.3,0.95,390,850],[2.7,0.85,390,700]],L,t);
  sp(L,0.12,0.66,[[8,636,412,200,90]])||sp(L,0.66,1.18,[[14,790,752,770,30]])||sp(L,1.18,1.82,[[16,1212,252,346,28]]); $('ov').innerHTML=ring(208,736,(L-0.3)/0.45)+ring(141,1380,(L-1.3)/0.45); if(L<0.5)plate('Start with your tiles',L-0.02);}
 if(id==='sw1'){frame(C.RA,C.TA,pw([[0,1.0],[1.0,1.93],[1.025,1.95],[1.3,2.08],[2.7,3.85]],L));
  cam([[0,...FULL],[0.45,...FULL],[0.85,1.0,390,780],[2.7,1.06,330,800]],L,t);
  sp(L,0.1,2.8,[[14,250,752,1250,30]]); $('ov').innerHTML=stamp(390,980,(L-0.725)/0.9,true); if(L<0.5)plate('Swipe the mats',L-0.02);}
 if(id==='sw2'){frame(C.RA,C.TA,pw([[0,3.86],[0.83,3.89],[0.85,3.91],[1.1,4.16],[1.6,5.04],[2.16,5.6]],L));
  cam([[0,1.06,330,800],[1.0,1.1,450,790],[2.16,1.03,390,770]],L,t); sp(L,-0.3,2.3,[[14,250,752,1250,30]]); $('ov').innerHTML=stamp(390,980,(L-0.55)/0.9,false);}
 if(id==='sw3'){frame(C.RA,C.TA,pw([[0,5.6],[0.43,5.87],[0.45,5.89],[0.7,6.14],[1.18,7.86],[1.2,7.88],[1.45,8.07],[1.78,9.75]],L));
  cam([[0,1.03,390,770],[0.9,1.09,330,800],[1.45,1.02,420,800],[1.78,0.95,390,950]],L,t); sp(L,-0.3,1.42,[[14,250,752,1250,30]]); $('ov').innerHTML=stamp(390,980,(L-0.15)/0.9,true)+stamp(390,980,(L-0.9)/0.9,true);}
 if(id==='fav'){if(L<1.75)frame(C.RP,C.TP,0.3); else frame(C.RB,C.TB,pw([[1.75,0],[2.66,0.8]],L));  // tap -> the racks screen (opens on Teal Wood, picks off)
  cam([[0,...FULL],[0.55,...FULL],[1.1,1.1,480,1150],[1.6,1.2,480,1238],[2.2,1.0,390,800],[2.66,...FULL]],L,t);
  sp(L,0.35,1.8,[[18,958,744,424,28]]); $('ov').innerHTML=ring(598,1238,(L-1.3)/0.45); if(L<0.55)plate('Pick your favorite',L-0.02);}
 if(id==='racks'){frame(C.RB,C.TB,pw([[0,0.8],[0.4,0.95],[0.75,1.7],[1.13,2.89],[1.15,2.91],[1.63,4.96],[1.65,4.98],[2.05,5.6],[2.53,7.27],[2.55,7.29],[2.95,7.9],[3.43,9.62],[3.45,9.64],[3.7,9.82],[3.97,11.0]],L));
  cam([[0,...FULL],[0.4,...FULL],[0.75,1.12,450,560],[1.15,1.14,300,900],[1.6,1.02,390,1230],[2.55,1.08,330,1250],[3.45,1.02,450,1230],[3.97,0.98,390,1150]],L,t);
  sp(L,0.25,0.86,[[16,356,752,404,26]])||sp(L,0.86,1.2,[[60,816,250,160,70]])||sp(L,1.2,4.2,[[16,356,752,404,26],[16,1040,752,660,30]]); $('ov').innerHTML=ring(182,895,(L-1.05)/0.45)+stamp(390,1260,(L-1.29)/0.9,false)+stamp(390,1260,(L-2.19)/0.9,true)+stamp(390,1260,(L-3.09)/0.9,true); if(L<0.4)plate('Add racks',L-0.02);}
 if(id==='card'){const im=$('mcard');if(im.dataset.u!=='c'){im.src=C.CARD;im.dataset.u='c';}
  const k=eo(L/0.5);const w=580;im.style.width=w+'px';im.style.left=(540-w/2)+'px';im.style.top=(455+(1-k)*120)+'px';im.style.opacity=cl(L/0.2);
  const z=1+0.09*eio((L-0.3)/3.2); im.style.transformOrigin='50% 50%'; im.style.transform=`scale(${(0.94+0.06*k)*z})`;
  plate('See it together,<br>share it or shop it',L-0.25,250);}
 if(id==='xw'){wall('x',L);}
 if(id==='shop'){frame(C.RB,C.TB,pw([[0,17.49],[0.8,17.55],[1.6,18.26]],L));
  cam([[0,...FULL],[0.8,...FULL],[1.7,1.15,420,760],[2.7,1.3,420,900],[3.7,1.3,420,1060],[4.5,1.12,400,950]],L,t); sp(L,0.05,0.85,[[80,1462,620,116,56]])||sp(L,1.55,4.7,[[8,1272,764,416,26]]); if(L<0.8)plate('Shop it with<br>code MAHJMATCH',L-0.02,250);}
 if(id==='end'){$('fh').style.transform=`scale(${eb(L/0.45)})`;$('nag').style.opacity=cl((L-0.15)/0.2);$('nag').style.transform=`scale(${0.8+0.2*eb((L-0.15)/0.4)})`;
  $('shop').style.transform=`scale(${L<1?eb((L-0.35)/0.45):1+0.04*Math.sin(Math.PI*2*((L-1)/0.8))})`; ticks($('eticks'),t,cl((L-0.5)/0.3),150);}
};
</script></body></html>"""
def page():
    return HTML.replace('__F__', FONTS).replace('__FL__', CFG['FL']).replace('__CFG__', json.dumps(CFG))
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'frames'
    out = f'{O}/out'; os.makedirs(out, exist_ok=True); open(f'{O}/reel.html', 'w').write(page()); FPS = 30
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(f'file://{O}/reel.html'); pg.wait_for_timeout(3000)
        wait = "()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})))"
        if mode == 'frames':
            fd = f'{O}/frames'; os.makedirs(fd, exist_ok=True)
            rng = list(range(DW_A, DW_B + 1)) + list(range(round(T_START * FPS), round(T_END * FPS)))
            if len(sys.argv) > 2: rng = [n for a in sys.argv[2:] for n in range(int(a.split('-')[0]), int(a.split('-')[1]) + 1)]
            for n in rng:
                pg.evaluate(f"render({n / FPS})"); pg.evaluate(wait); pg.screenshot(path=f'{fd}/{n:04d}.jpg', type='jpeg', quality=92)
        else:
            for tt in [float(x) for x in sys.argv[2:]]:
                pg.evaluate(f"render({tt})"); pg.evaluate(wait); pg.wait_for_timeout(150); pg.screenshot(path=f'{out}/t{tt:05.2f}.jpg', type='jpeg', quality=88)
        b.close()
