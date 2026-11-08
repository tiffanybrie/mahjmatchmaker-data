"""Pinned Find Your Mat-ch reel v3 (Nov 8 2026), app half, TWO versions (FEEDBACK-nov08-v3.md).
A = v2 style with every fix; B = same, but the swipes and the RACK step happen in Table view (racks on the mat).
Recordings: cap3.py (live site app v118). Local t=0 == 19.6s in the final reel (0-19.6 = v2 teaser, unchanged).
Fixes vs v2: slow readable typing (zoomed), NO dimming over the tiles/mat comparison, view switcher (Up close / Aerial / Table)
shown, only YES racks, zoom on mat + rack, rack filters (colour dot, Wood tone), 'Save + share your match card' showing the graphic
change (Story close up -> Story mood board), live stock 1-2-3 kept, all text/callouts inside y 270-1440 (IG reel safe area) and NOTHING
in the story link-sticker lane y 1450-1640, end title with breathing room + Title Case tagline.
Usage: python3 reel3.py A|B frames | A|B stills t1 t2 ... | A|B safe t1 ...  -> /dev/shm/pin3/{framesA,framesB,out}"""
import json, os, sys, bisect
O = '/dev/shm/pin3'; os.environ['TMPDIR'] = f'{O}/tmp'; os.makedirs(f'{O}/tmp', exist_ok=True)
from playwright.sync_api import sync_playwright
R = '/home/claude/mahjmatchmaker-data'
FONTS = f'file://{R}/scripts/social/tileprofile/fonts'
F = lambda p: 'file://' + p
NOLOGO = {'Tigre de Tartán', 'Tigre de Tartan', 'Sunday Mahjong', 'YMI', 'Mahjong Row'}  # image-only/never-on-social brands stay off the strip
ALLP_V2 = ['omm','missm','myfair','middlemain','bb','bambird','squad','britt','plm','cmc','bespoke','virora','ar','mood','minimahjer','macmiller','toppe','amahj','mahjon','vine','hiphip','bam','mahjongco','studios','ilovemahj','splash','wren','press','royal','soiree','register','lbb','yolo','maison','noli']  # code partners; no Tigre de Tartan, no Sunday, no Mahjong Row, no YMI
V = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ('A', 'B') else 'A'
def rec(n):
    d = json.load(open(f'{O}/{n}/marks.json')); f0 = d['frames'][0]
    ts = sorted((x - f0 + 0.05, i) for i, x in enumerate(d['frames']))
    return dict(u=F(f'{O}/{n}/f/'), t=[round(a, 3) for a, _ in ts], i=[b for _, b in ts])
CFG = dict(V=V, LOGOS=[F(f'{R}/assets/hub/build-2026-11-07/' + x['file']) for x in json.load(open(f'{R}/assets/hub/build-2026-11-07/trim/list.json')) if x['brand'] not in NOLOGO], FL=F(f'{R}/assets/brand/flame-heart.png'),
           R0=rec('rec0'), S=rec('S' + V), P=rec('P' + V), K=rec('K' + V))
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
.plate span{display:inline-block;font:400 72px/1.08 Cap;color:var(--navy);background:#fff;padding:20px 46px 28px;border-radius:34px;box-shadow:0 14px 40px rgba(60,30,40,.28);white-space:nowrap;text-align:center}
.cam{position:absolute;left:0;top:0;transform-origin:0 0}
.bez{position:absolute;left:-28px;top:-28px;width:836px;height:1834px;border-radius:120px;background:#ffffff;box-shadow:0 34px 80px rgba(90,50,60,.22),inset 0 0 0 5px #e4e1de}
.bez i{position:absolute;width:11px;background:#e9e6e3;border-radius:4px}
.sb{position:absolute;left:0;top:0;width:780px;height:90px;background:#fff;font:600 34px -apple-system,Helvetica,Arial;color:#111}
.isl{position:absolute;left:276px;top:20px;width:228px;height:62px;background:#000;border-radius:40px}
.scr{position:absolute;left:0;top:0;width:780px;height:1778px;border-radius:92px;overflow:hidden;background:#fff}
.apz{position:absolute;left:0;top:90px;width:780px;height:1688px}.scr img.f{position:absolute;left:0;top:0;width:780px;height:1688px}
.ring{position:absolute;border-radius:50%;border:9px solid var(--pink)}
.stamp{position:absolute;width:180px;height:180px;margin:-90px 0 0 -90px;border-radius:50%;display:flex;align-items:center;justify-content:center;font:400 118px/1 Arial;color:#fff;box-shadow:0 20px 50px rgba(0,0,0,.30);border:10px solid #fff}
.tick{position:absolute;left:0;width:1080px;overflow:hidden}.tick .row{position:absolute;top:0;left:0;display:flex;gap:22px;white-space:nowrap}
.chip{flex:none;width:180px;height:108px;background:#fff;border-radius:22px;box-shadow:0 10px 26px rgba(0,0,0,.18);display:flex;align-items:center;justify-content:center}.chip img{max-width:162px;max-height:92px;object-fit:contain}
.pill{display:inline-block;font:700 46px/1.1 Bit;padding:18px 42px;border-radius:60px;white-space:nowrap}
.code{position:absolute;left:0;right:0;text-align:center;z-index:60}
.code span{display:inline-block;background:var(--pink);color:#fff;font:700 54px/1 Bit;letter-spacing:2px;padding:22px 48px;border-radius:80px;box-shadow:0 16px 40px rgba(120,20,60,.35);border:6px solid #fff}
.ln{position:absolute;left:0;right:0;text-align:center;font:400 110px/1 Cap;color:#fff;white-space:nowrap}
#safe{position:absolute;inset:0;z-index:999;display:none;pointer-events:none}
</style></head><body>
<div id="app" class="sc cr"><div class="cam" id="cam"><div class="bez"><i style="left:-9px;top:300px;height:80px"></i><i style="left:-9px;top:430px;height:140px"></i><i style="left:-9px;top:600px;height:140px"></i><i style="right:-9px;top:470px;height:210px"></i></div><div class="scr"><div class="sb"><span style="position:absolute;left:96px;top:24px">9:41</span><span style="position:absolute;right:86px;top:26px;font-size:26px;letter-spacing:3px">▂▄▆ ◔ ▭</span><div class="isl"></div></div><div class="apz"><img class="f" id="fr"><svg id="spot" width="780" height="1688" style="position:absolute;left:0;top:0"></svg><div id="ov" style="position:absolute;inset:0"></div></div></div></div></div>
<div id="see" class="sc nv">
 <div class="ln" id="l1" style="top:400px">See it together.</div>
 <div class="ln" id="l2" style="top:600px;color:var(--blush)">Save it.</div>
 <div class="ln" id="l3" style="top:800px">Share it.</div>
 <div class="ln" id="l4" style="top:1000px;color:var(--blush)">Shop it.</div>
 <div style="position:absolute;left:0;right:0;top:1170px;text-align:center" id="l4c"><span class="pill" style="background:#fff;color:var(--navy);font-size:40px;padding:14px 36px">code MAHJMATCH</span></div>
</div>
<div id="end" class="sc nv">
 <img src="__FL__" id="fh" style="position:absolute;left:475px;top:290px;width:130px">
 <div style="position:absolute;left:0;right:0;top:470px;text-align:center" id="en"><span style="display:inline-block;font:400 96px/1 Cap;color:#fff;white-space:nowrap">Find <span style="font:italic 600 102px/1 PF;color:var(--blush)">Your</span> Mat-ch</span></div>
 <div style="position:absolute;left:0;right:0;top:620px;text-align:center;font:400 66px/1.18 Cap;color:var(--blush)" id="es">Match Tiles, Mats &amp; Racks<br>Across Brands</div>
 <div style="position:absolute;left:0;right:0;top:820px;text-align:center" id="eb"><span class="pill" style="background:var(--pink);color:#fff;font-size:46px;letter-spacing:5px;padding:18px 50px">LINK IN BIO</span></div>
 <div style="position:absolute;left:0;right:0;top:935px;text-align:center;font:700 38px Bit;color:#fff;opacity:.9" id="eu">free at mahjmatchmaker.com</div>
 <div id="eticks"></div>
</div>
<div class="plate" id="plate"><span id="plt"></span></div>
<div class="code" id="code"><span>Use code MAHJMATCH</span></div>
<svg id="safe" width="1080" height="1920"><defs><pattern id="hp" width="24" height="24" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="12" height="24" fill="rgba(0,160,255,.30)"/></pattern></defs>
 <rect x="0" y="0" width="1080" height="269" fill="rgba(255,0,0,.16)"/><text x="20" y="250" font-size="30" fill="#c00" font-family="Arial">TOP 14% (IG header)</text>
 <rect x="0" y="1248" width="1080" height="672" fill="rgba(255,140,0,.10)"/><rect x="0" y="1536" width="1080" height="384" fill="rgba(255,0,0,.16)"/>
 <rect x="0" y="1450" width="1080" height="190" fill="url(#hp)" stroke="#08f" stroke-width="4"/><text x="20" y="1560" font-size="34" fill="#035" font-family="Arial" font-weight="bold">STORY LINK-STICKER LANE 1450-1640</text>
 <rect x="950" y="1000" width="130" height="700" fill="rgba(255,0,0,.16)"/><text x="20" y="1290" font-size="28" fill="#a50" font-family="Arial">bottom 35% (caption when expanded)</text>
 <text x="20" y="1880" font-size="30" fill="#c00" font-family="Arial">bottom 20% (caption, buttons)</text>
 <rect x="0" y="269" width="1080" height="1171" fill="none" stroke="#0a0" stroke-width="5" stroke-dasharray="20 12"/></svg>
<script>
const C=__CFG__;
const cl=x=>Math.min(Math.max(x,0),1), eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}, eb=x=>{x=cl(x);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const $=id=>document.getElementById(id);
function plate(txt,k,y){const p=$('plate');if(!txt){p.style.display='none';return;}p.style.display='block';p.style.top=(y||290)+'px';
 if($('plt').innerHTML!==txt)$('plt').innerHTML=txt;$('plt').style.transform=`scale(${0.86+0.14*eb(k/0.3)})`;p.style.opacity=cl(k/0.12);}
function code(k,y){const c=$('code');if(k<=0){c.style.display='none';return;}c.style.display='block';c.style.top=(y||440)+'px';c.style.opacity=cl(k/0.15);c.firstChild.style.transform=`scale(${0.7+0.3*eb(k/0.35)})`;}
function spot(holes,a){ // spotlight on BUTTONS only (never over the tiles/mat comparison)
 if(!holes.length||a<=0.001){$('spot').innerHTML='';return;}
 $('spot').innerHTML=`<defs><filter id="bl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter><mask id="mk"><rect width="780" height="1688" fill="#fff"/>${holes.map(([x,y,w,h,r])=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r||22}" fill="#000" filter="url(#bl)"/>`).join('')}</mask></defs><rect width="780" height="1688" fill="rgb(6,16,38)" fill-opacity="${0.5*a}" mask="url(#mk)"/>`;}
function sp(L,a,b,holes){const k=cl((L-a)/0.2)*cl((b-L)/0.2);if(L>=a&&L<=b){spot(holes,k);return true;}return false;}
function pw(P,L){if(L<=P[0][0])return P[0][1];for(let i=1;i<P.length;i++){if(L<=P[i][0]){const [a,x]=P[i-1],[b,y]=P[i];return b>a?x+(y-x)*(L-a)/(b-a):y;}}return P[P.length-1][1];}
function frame(R,t){let lo=0,hi=R.t.length-1,k=0;while(lo<=hi){const m=(lo+hi)>>1;if(R.t[m]<=t){k=m;lo=m+1}else hi=m-1}
 const u=R.u+String(R.i[k]).padStart(5,'0')+'.jpg';const f=$('fr');if(f.dataset.u!==u){f.src=u;f.dataset.u=u;}}
// CAMERA keyed in RECORDING time: [t, k, cx, cy]; frame point (cx,cy) sits at screen centre, zoom k. Equal neighbouring keys = hold.
function camAt(keys,t){let a=keys[0],b=keys[0];if(t<=keys[0][0]){a=b=keys[0];}else{a=b=keys[keys.length-1];for(let i=1;i<keys.length;i++){if(t<=keys[i][0]){a=keys[i-1];b=keys[i];break;}}}
 const q=b[0]>a[0]?eio((t-a[0])/(b[0]-a[0])):1;const m=i=>a[i]+(b[i]-a[i])*q;const k=m(1),cx=m(2),cy=m(3);
 $('cam').style.transform=`translate(${540-cx*k}px,${960-(cy+90)*k}px) scale(${k})`;}
function ring(x,y,k){if(k<0||k>1)return '';const r=40+60*eo(k);return `<div class="ring" style="left:${x-r}px;top:${y-r}px;width:${2*r}px;height:${2*r}px;opacity:${1-k}"></div>`;}
function stamp(x,y,k,yes){if(k<0||k>0.5)return '';const s=k<0.25?2.2-1.2*eb(k/0.25):1;const o=k>0.4?1-(k-0.4)/0.1:cl(k/0.08);return `<div class="stamp" style="left:${x}px;top:${y}px;background:${yes?'#e0547f':'#7a6a85'};transform:scale(${s}) rotate(${yes?12:-12}deg);opacity:${o}">${yes?'&hearts;':'&#10005;'}</div>`;}
function mkTick(host,logos,rows,y0,dy,off){for(let r=0;r<rows;r++){const t=document.createElement('div');t.className='tick';t.style.top=(y0+r*dy)+'px';t.style.height='112px';const row=document.createElement('div');row.className='row';
  let L=logos.filter((u,i)=>(i+off)%rows===r);while(L.length<8)L=L.concat(L);L.concat(L).concat(L).forEach(u=>{const c=document.createElement('div');c.className='chip';c.innerHTML=`<img src="${u}">`;row.appendChild(c);});
  t.appendChild(row);t.dataset.dir=r%2?1:-1;host.appendChild(t);}}
mkTick($('eticks'),C.LOGOS,3,1060,126,1);  // logo strip ends at 1060+2*126+112 = 1424 (above the link lane)
function ticks(host,t,a,sp){[...host.children].forEach((e,i)=>{const d=+e.dataset.dir;const w=e.firstChild.scrollWidth/3;const x=((t*sp*(1+0.15*i))%w);e.firstChild.style.transform=`translateX(${d<0?-x-w*0.2:x-w}px)`;e.style.opacity=a;});}
const B=C.V==='B';
const SC=B?[['tiles',0,4.4],['sw',4.4,11.45],['pick',11.45,13.25],['racks',13.25,20.0],['off',20.0,21.6],['card',21.6,26.0],['shop',26.0,30.6],['see',30.6,33.2],['end',33.2,39.35]]
          :[['tiles',0,4.4],['sw',4.4,11.8],['pick',11.8,13.6],['racks',13.6,20.0],['off',20.0,21.6],['card',21.6,26.0],['shop',26.0,30.6],['see',30.6,33.2],['end',33.2,39.35]];
const DIV={tiles:'app',sw:'app',pick:'app',racks:'app',off:'app',card:'app',shop:'app',see:'see',end:'end'};
window.render=function(t){let cur=SC[SC.length-1];for(const s of SC)if(t>=s[1]&&t<s[2]){cur=s;break;}
 const [id,a]=cur,L=t-a;for(const d of ['app','see','end'])$(d).style.display=DIV[id]===d?'block':'none';
 plate('',0); code(0); $('ov').innerHTML=''; spot([],0);
 if(id==='tiles'){ // home -> Start with tiles -> type "Sunday" (real speed, zoomed) -> tap Sunday -> Mat-ching
  const T=pw([[0,0.3],[0.55,0.97],[0.56,2.1],[0.8,2.45],[2.85,4.5],[3.4,5.3],[3.75,5.98],[3.76,7.0],[4.4,9.97]],L); frame(C.R0,T);
  camAt([[0,1.0,390,844],[1.0,1.0,390,844],[1.01,1.4,300,810],[4.45,1.4,300,810],[5.25,1.4,300,1150],[6.5,1.4,300,1150],[6.51,1.0,390,775]],T);
  sp(L,0.05,0.62,[[24,656,350,150,70]]);
  $('ov').innerHTML=ring(208,736,(L-0.3)/0.35)+ring(141,1330,(L-3.4)/0.4);
  if(L<0.56)plate('Start with your tiles',L); else if(L<2.85)plate('Search your set',L-0.56); else if(L<3.76)plate('Tap your tiles',L-2.85);}
 if(id==='sw'){
  if(!B){ // A: Up close -> Aerial -> Table (the view switcher), back to Up close, then swipe with tiles AND mat both in view (no dimming)
   const T=pw([[0,0.3],[1.2,1.75],[2.2,3.1],[2.5,3.3],[3.5,4.9],[3.51,5.45],[4.3,6.85],[5.3,8.62],[6.3,10.39],[7.2,12.17],[7.4,12.42]],L); frame(C.S,T);
   camAt([[0,0.95,390,1148],[1.84,0.95,390,1148],[1.85,1.0,390,904],[3.42,1.0,390,904],[3.6,1.0,390,792],[4.95,1.0,390,792],[5.4,1.0,390,775]],T);
   $('ov').innerHTML=ring(419,1453,(L-0.85)/0.4)+ring(560,1144,(L-2.05)/0.4)+stamp(390,855,(L-4.15)/0.7,true)+stamp(390,855,(L-5.15)/0.7,false)+stamp(390,855,(L-6.15)/0.7,true)+stamp(390,855,(L-7.05)/0.7,true);
   if(L<1.2)plate('View it up close',L); else if(L<2.5)plate('From above',L-1.2); else if(L<3.5)plate('Or at the table',L-2.5); else if(L<4.2)plate('Swipe the mats',L-3.5);}
  else { // B: Up close -> Aerial -> Table, then every swipe happens AT THE TABLE (tiles + racks on the mat)
   const T=pw([[0,0.3],[1.2,1.72],[2.2,3.0],[2.5,3.25],[3.4,4.6],[3.9,5.46],[4.9,7.23],[5.9,9.0],[6.85,10.77],[7.05,10.86]],L); frame(C.S,T);
   camAt([[0,0.95,390,1148],[1.81,0.95,390,1148],[1.82,1.0,390,904],[3.36,1.0,390,904],[3.52,1.0,390,792],[4.6,1.0,390,792],[5.25,1.25,390,600]],T);
   $('ov').innerHTML=ring(419,1453,(L-0.85)/0.4)+ring(560,1144,(L-2.05)/0.4)+stamp(390,453,(L-3.75)/0.7,true)+stamp(390,453,(L-4.75)/0.7,false)+stamp(390,453,(L-5.75)/0.7,true)+stamp(390,453,(L-6.7)/0.7,true);
   if(L<1.2)plate('View it up close',L); else if(L<2.5)plate('From above',L-1.2); else if(L<3.4)plate('Or at the table',L-2.5); else if(L<4.0)plate('Swipe the mats',L-3.4);}}
 if(id==='pick'){ // which suitor is the one? straight zoom in on Brownstone Bloom, tap
  const T=pw([[0,0.3],[1.8,1.0]],L); frame(C.P,T);
  camAt([[0.3,1.0,390,1150],[0.48,1.0,390,1150],[0.85,2.0,570,1200],[1.0,2.0,570,1200]],T);
  sp(L,0.15,1.8,[[480,1080,180,250,26]]); $('ov').innerHTML=ring(570,1200,(L-1.2)/0.45); if(L<0.9)plate('Pick your favorite',L);}
 if(id==='racks'){ // YES racks only, seen against the mat; the rack filters: colour dot, then Wood tone
  const e=B?0.35:0;
  const T=pw([[0,0.4],[1.2,1.6],[1.7,3.1],[2.3,3.82],[2.6,4.3],[3.0,5.01],[3.5,5.9],[3.51,6.5],[4.0,7.3],[4.6+e*0.5,8.99],[5.3+e*0.5,9.8],[5.31+e*0.5,10.6],[5.8+e,11.2],[6.4+e,11.42]],L); frame(C.K,T);
  const deck=B?[1.35,390,600]:[1.15,390,1060], fil=[1.5,390,900];
  camAt([[0,...deck],[2.4,...deck],[3.1,...fil],[6.5,...fil],[7.3,...deck]],T);
  const sy=B?580:1050;
  $('ov').innerHTML=ring(314,1090,(L-1.95)/0.4)+ring(280,631,(L-2.65)/0.4)+stamp(390,sy,(L-(4.45+e*0.5))/0.9,true)+stamp(390,sy,(L-(5.65+e))/0.9,true);
  if(L<1.2)plate(B?'Add racks, at the table':'Add racks',L); else if(L<2.3)plate('Find racks by color',L-1.2); else if(L<3.6)plate('Or by wood tone',L-2.3); else if(L<4.4+e*0.5)plate('Love it',L-3.6);}
 if(id==='off'){ // the tray -> 'Make it official ♥' big
  const T=pw([[0,13.95],[0.8,14.66],[1.6,14.72]],L); frame(C.K,T);
  camAt([[13.95,1.0,390,1100],[14.2,1.0,390,1100],[14.6,2.4,630,1296],[15.4,2.4,630,1296]],T);
  sp(L,0.15,1.6,[[495,1220,270,160,44]]); $('ov').innerHTML=ring(630,1296,(L-0.7)/0.45); if(L<1.0)plate('Make it official',L);}
 if(id==='card'){ // Save + share: the GRAPHIC changes, Story close up -> Story mood board
  const T=pw([[0,21.6],[1.9,23.1],[1.91,23.97],[4.4,25.7]],L); frame(C.K,T); camAt([[0,0.83,390,1110]],T);
  plate('Save + share<br>your match card',L);}
 if(id==='shop'){ // shop list: live stock (Sunday sold out), the 1-2-3 of what you can shop, code MAHJMATCH
  const T=pw([[0,26.0],[0.9,26.96],[4.6,29.49]],L); frame(C.K,T); camAt([[0,1.36,390,740]],T);
  sp(L,1.0,2.0,[[20,490,740,130,22]])||sp(L,2.0,4.8,[[20,630,740,430,22]]);
  $('ov').innerHTML=ring(670,550,(L-1.15)/0.45)+ring(690,696,(L-2.1)/0.45)+ring(690,840,(L-2.3)/0.45)+ring(690,984,(L-2.5)/0.45);
  if(L<1.0)plate('Shop your match',L); else if(L<2.0)plate('Live stock check',L-1.0); else plate('Shop each piece',L-2.0);
  code(L-2.6,440);}
 if(id==='see'){const ln=(e,s)=>{const k=eb((L-s)/0.35);$(e).style.opacity=cl((L-s)/0.12);$(e).style.transform=`scale(${0.75+0.25*k})`;};
  ln('l1',0.1);ln('l2',0.6);ln('l3',1.1);ln('l4',1.6);ln('l4c',2.0);}
 if(id==='end'){$('fh').style.transform=`scale(${eb(L/0.45)})`;
  const ap=(e,s)=>{$(e).style.opacity=cl((L-s)/0.2);$(e).style.transform=`scale(${0.82+0.18*eb((L-s)/0.4)})`;};
  ap('en',0.15);ap('es',0.55);ap('eb',1.0);ap('eu',1.2);
  $('eb').firstChild.style.transform=`scale(${L<1.6?1:1+0.04*Math.sin(Math.PI*2*((L-1.6)/0.8))})`; ticks($('eticks'),t,cl((L-1.0)/0.3),150);}
};
</script></body></html>"""
def page():
    return HTML.replace('__F__', FONTS).replace('__FL__', CFG['FL']).replace('__CFG__', json.dumps(CFG))
if __name__ == '__main__':
    mode = sys.argv[2] if len(sys.argv) > 2 else 'frames'
    out = f'{O}/out'; os.makedirs(out, exist_ok=True); hp = f'{O}/reel3{V}.html'; open(hp, 'w').write(page()); FPS = 30
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(f'file://{hp}'); pg.wait_for_timeout(3000)
        wait = "()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})))"
        if mode == 'frames':
            fd = f'{O}/frames{V}'; os.makedirs(fd, exist_ok=True)
            for n in range(0, round(DUR * FPS)):
                pg.evaluate(f"render({n / FPS})"); pg.evaluate(wait); pg.screenshot(path=f'{fd}/{n:04d}.jpg', type='jpeg', quality=92)
        else:
            if mode == 'safe': pg.evaluate("document.getElementById('safe').style.display='block'")
            for tt in [float(x) for x in sys.argv[3:]]:
                pg.evaluate(f"render({tt})"); pg.evaluate(wait); pg.wait_for_timeout(150); pg.screenshot(path=f'{out}/{V}{mode[0]}{tt:05.2f}.jpg', type='jpeg', quality=85)
        b.close()
