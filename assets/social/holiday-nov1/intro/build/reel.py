"""Holiday intro hero reel (Merry Mahjong, Mon Nov 2 2026). Music-first: cut to Mariah Carey "All I Want for Christmas Is You" @150 BPM
(beat = 0.4s, bar = 1.6s). 72 beats = 28.8s, 30fps (12 frames per beat), 1080x1920, rendered from HTML with Playwright.
Inputs live in /dev/shm/holiday-intro (rebuild them with the scripts in this folder: stock.py, mats.py, rec.py, rec2.py):
  mats/*.webp      real in-stock holiday mat photos pulled from Find Your Mat-ch v1.10 (stock checked Nov 1 ~12:10am ET)
  rec/f, rec2/f    real FYM v1.10 screen recording frames (Dear Santa -> Holiday chip -> swipes; racks step zoom + swipes -> card)
  rec2/storycard.png  the Story 9:16 match card the app made at the end of the recording
Usage: python3 reel.py [frames|cover]  -> /dev/shm/holiday-intro/out/"""
import json, os, sys, subprocess, shutil, random
os.environ['TMPDIR'] = '/dev/shm/holiday-intro/tmp'
from playwright.sync_api import sync_playwright
R = '/home/claude/mahjmatchmaker-data'
W = '/dev/shm/holiday-intro'
FONTS = f'file://{R}/scripts/social/tileprofile/fonts'
Q = json.load(open(f'{W}/quilt.json'))['quilt']
random.seed(7)
QU = Q[:54]; random.shuffle(QU)
MATS = {n: f for f, n, b in Q}
def mat(n): return 'file://' + MATS[n]
T = f'file://{R}/assets/tiles/holiday/'
DUMP1 = [  # one per beat b16-b19: tiles, mat, tiles, mat
    (T + 'dear-santa.jpg', 'Dear Santa tiles', 'Anders Ruff', 'tile'),
    (mat('Tartan Tidings'), 'Tartan Tidings mat', 'Anders Ruff', 'mat'),
    (T + 'rackin-rudolph.jpg', "Rackin' Rudolph tiles", 'Hip Hip Mahjong', 'tile'),
    (mat('Very Merry Wreath Premium'), 'Very Merry Wreath mat', 'Mahjong Register', 'mat'),
]
DUMP2 = [  # eighth notes b52-b56 then hold
    (T + 'holly-jolly-pink-pile.jpg', 'Holly Jolly (Sugarplum Pink) tiles', "Bam! Let's Mahjong", 'tile'),
    (mat('Merriment'), 'Merriment mat', 'Oh My Mahjong', 'mat'),
    (f'file://{R}/assets/racks/v99/mm-milk-glass.webp', 'Milk Glass racks', 'Middle & Main', 'rack'),
    (T + 'nutcracker-ballet.jpg', 'Nutcracker Ballet tiles', 'Mahj Squad', 'tile'),
    (mat("Clara's Dream Christmas"), "Clara's Dream Christmas mat", 'Mahj Squad', 'mat'),
    (T + 'cmc-apres-ski.jpg', 'Après Ski Club tiles', 'Charleston Mahjong Club', 'tile'),
    (mat('Snowflake Lodge Premium'), 'Snowflake Lodge mat', 'Mahjong Register', 'mat'),
    (T + 'nivalee-blue.jpg', 'Nivalee (Glacier Blue) tiles', 'Virora Mahjong', 'tile'),
    (mat('Holly Jolly Christmas'), 'Holly Jolly Christmas mat', "Bam! Let's Mahjong", 'mat'),
]
BURST = [mat(n) for n in ['Candy Cane Lane', 'Winterberry', 'Yuletide', 'Peppermint Patty Premium', 'Merry Mix', 'Snowflake Lodge Premium',
                          'Santa\'s Mahjong Mail', 'Hip Hip Hanukkah', 'Clara', 'Perfectly Wrapped', 'Christmas Botanical Bow', 'Plaid Tidings'] if n in MATS]
TILES13 = [T + f for f in ['dear-santa.jpg', 'rackin-rudolph.jpg', 'holly-jolly-red-pile.jpg', 'holly-jolly-green.jpg', 'holly-jolly-pink-pile.jpg',
                           'tinselle-emerald-3x3.jpg', 'nivalee-blue.jpg', 'nutcracker-ballet.jpg', 'cmc-apres-ski.jpg']]  # Nov 1 polish: PLM Spirit of Christmas (sold out) dropped
COV = [f'file://{R}/assets/covers/holiday/{f}' for f in ['dear-santa.jpg', 'rackin-rudolph.jpg', 'holly-jolly-red.jpg', 'holly-jolly-pink.jpg', 'nutcracker-ballet.jpg',
       'cmc-apres-ski.jpg', 'nivalee-blue.jpg', 'tinselle-emerald.jpg', 'december-1994.jpg']] + \
      [f'file://{R}/assets/covers/albums/uniform-v3/{f}.jpg' for f in ['amara', 'birdie', 'coquette', 'gatsby', 'moonlight', 'heritage-2-0', 'osler', 'smith', 'pearlescent', 'lola', 'la-fete', 'glitterville']]
CFG = dict(QU=['file://' + f for f, n, b in QU], DUMP1=DUMP1, DUMP2=DUMP2, BURST=BURST, TILES13=TILES13, COV=COV,
           REC=f'file://{W}/rec/f/', REC2=f'file://{W}/rec2/f/', CARD=f'file://{W}/rec2/storycard.png',
           FH=f'file://{R}/assets/brand/flame-heart-holiday.png', WM=f'file://{R}/assets/brand/mahjmatchmaker-wordmark-notag.png')

HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Cap;src:url(__F__/Caprasimo.ttf)}
@font-face{font-family:Bit;src:url(__F__/bitter-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:Bit;src:url(__F__/bitter-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:PF;src:url(__F__/playfair-display-latin-600-italic.woff2);font-style:italic}
@font-face{font-family:Cav;src:url(__F__/Caveat-Bold.ttf)}
:root{--navy:#062a55;--red:#b3202a;--pine:#1f5a3a;--gold:#e9c77b;--pink:#f56c8c;--rose:#d6336c;--cream:#faf3ea}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:__H__px;overflow:hidden;position:relative;background:var(--navy);font-family:Bit}
.sc{position:absolute;inset:0;display:none;overflow:hidden}
.abs{position:absolute}
.cap{font-family:Cap;line-height:1.02}
.c{position:absolute;left:0;right:0;text-align:center}
.pill{display:inline-block;font:700 38px Bit;letter-spacing:5px;padding:16px 38px;border-radius:60px;text-transform:uppercase}
.lab{position:absolute;font:700 34px/1.15 Bit;color:#fff;background:var(--rose);padding:12px 22px;border-radius:18px;white-space:nowrap;box-shadow:0 10px 26px rgba(0,0,0,.28)}
.lab small{display:block;font:600 24px Bit;opacity:.92;letter-spacing:.5px}
.lab.x{background:#5e5368}.lab.n{background:var(--navy)}
.snow i{position:absolute;border-radius:50%;background:#fff}
.plaid{background-color:#9e1b25;background-image:
 repeating-linear-gradient(90deg,rgba(14,64,40,.55) 0 70px,transparent 70px 150px,rgba(255,255,255,.07) 150px 158px,transparent 158px 230px),
 repeating-linear-gradient(0deg,rgba(14,64,40,.55) 0 70px,transparent 70px 150px,rgba(255,255,255,.07) 150px 158px,transparent 158px 230px)}
/* gift box */
#box{position:absolute;left:290px;top:820px;width:500px;height:420px}
#box .b{position:absolute;left:0;top:120px;width:500px;height:300px;background:#b3202a;border-radius:10px;box-shadow:0 30px 60px rgba(0,0,0,.4)}
#box .l{position:absolute;left:-25px;top:40px;width:550px;height:100px;background:#c8283a;border-radius:10px;box-shadow:0 10px 20px rgba(0,0,0,.25)}
#box .rv{position:absolute;left:220px;top:120px;width:60px;height:300px;background:var(--gold)}
#box .rh{position:absolute;left:245px;top:0;width:60px;height:100px;background:var(--gold)}
#box .bow{position:absolute;left:150px;top:-60px;width:250px;height:110px}
#box .bow:before,#box .bow:after{content:"";position:absolute;top:0;width:120px;height:100px;border:26px solid var(--gold);border-radius:60px 60px 10px 60px}
#box .bow:before{left:0;transform:rotate(-20deg)}#box .bow:after{right:0;transform:rotate(20deg) scaleX(-1)}
.burst{position:absolute;width:300px;height:300px;border-radius:14px;box-shadow:0 18px 40px rgba(0,0,0,.4);object-fit:cover}
/* odometer */
.odo{display:flex;justify-content:center;gap:6px}
.dg{width:200px;height:300px;overflow:hidden;position:relative;background:rgba(6,42,85,.86);border-radius:26px;border:6px solid var(--gold);box-shadow:0 20px 50px rgba(0,0,0,.45)}
.dg .st{position:absolute;left:0;right:0;top:0}
.dg .st div{height:288px;font:400 250px/288px Cap;color:var(--cream);text-align:center}
.dg:after{content:"";position:absolute;inset:0;background:linear-gradient(rgba(0,0,0,.35),transparent 22%,transparent 78%,rgba(0,0,0,.35))}
.plus{font:400 250px/300px Cap;color:var(--gold)}
.mos{position:absolute;inset:-40px;display:grid;gap:8px;opacity:.55}
.mos img{width:100%;height:100%;object-fit:cover;border-radius:8px}
.big{position:absolute;inset:0;object-fit:cover}
.photo{position:absolute;inset:0;overflow:hidden}
/* phone */
.cam{position:absolute;inset:0;transform-origin:540px 960px}
.phone{position:absolute;left:62px;top:300px;width:956px;height:2060px;background:#14121a;border-radius:110px;padding:28px;box-shadow:0 40px 90px rgba(0,0,0,.5)}
.phone .scr{position:relative;width:900px;height:1948px;border-radius:84px;overflow:hidden;background:#fff}
.phone .scr img.f{position:absolute;left:0;top:0;width:900px;height:1948px}
.ring{position:absolute;width:120px;height:120px;border-radius:50%;border:12px solid var(--pink);margin:-60px 0 0 -60px}
.stamp{position:absolute;font:400 150px/1 Cap;color:var(--pink);border:14px solid var(--pink);border-radius:34px;padding:0 34px 14px;background:rgba(255,255,255,.92)}
.head{position:absolute;left:0;right:0;top:250px;text-align:center;z-index:20}
.head span{display:inline-block;font:400 74px/1.05 Cap;color:#fff;background:var(--navy);padding:18px 36px 24px;border-radius:30px;box-shadow:0 14px 34px rgba(0,0,0,.35)}
.quilt img{position:absolute;width:180px;height:180px;object-fit:cover;box-shadow:0 0 0 3px #fff}
.word{position:absolute;left:0;right:0;text-align:center}
.word span{display:inline-block;font:400 120px/1 Cap;color:#fff;background:var(--red);padding:18px 44px 30px;border-radius:34px;box-shadow:0 20px 50px rgba(0,0,0,.45)}
</style></head><body>
<div class="snow" id="snow" style="position:absolute;inset:0;z-index:50;pointer-events:none"></div>
<!-- S1 hook -->
<div id="s1" class="sc">
 <div class="c cap" id="h1" style="top:330px;font-size:118px;color:#fff"></div>
 <div id="bursts"></div>
 <div id="box"><div class="b"></div><div class="rv"></div><div class="l" id="lid"><div class="rh"></div></div></div>
</div>
<!-- S2 counts -->
<div id="s2" class="sc">
 <div class="mos" id="mos"></div><div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 48%,rgba(6,42,85,.55),rgba(6,42,85,.92) 70%)"></div>
 <div class="c" style="top:420px"><span class="pill" style="background:var(--red);color:#fff" id="kick">Holiday at Mahj Matchmaker</span></div>
 <div class="c" style="top:600px"><div class="odo" id="odo"></div></div>
 <div class="c cap" id="olab" style="top:960px;font-size:92px;color:#fff;padding:0 60px"></div>
 <div class="c" id="osub" style="top:1230px;font:italic 600 54px PF;color:var(--gold)"></div>
</div>
<!-- S3 / S7 photo dump -->
<div id="s3" class="sc"><div class="photo" id="ph"></div></div>
<!-- S4 / S6 app -->
<div id="s4" class="sc plaid">
 <div class="cam" id="cam"><div class="phone"><div class="scr"><img class="f" id="fr"><div id="ov" style="position:absolute;inset:0"></div></div></div></div>
 <div class="head" id="head"><span id="headt"></span></div>
 <div id="labs" style="position:absolute;inset:0;z-index:25"></div>
</div>
<!-- S5 quilt -->
<div id="s5" class="sc" style="background:var(--navy)"><div class="quilt" id="quilt"></div><div id="qw" style="position:absolute;inset:0"></div></div>
<!-- S6b card -->
<div id="s6" class="sc plaid"><img id="card" style="position:absolute;left:90px;top:160px;width:900px;border-radius:30px;box-shadow:0 40px 90px rgba(0,0,0,.5)"><div id="cardt" style="position:absolute;inset:0"></div></div>
<!-- S9 end -->
<div id="s9" class="sc" style="background:var(--navy)">
 <img src="__FH__" class="abs" id="fh" style="left:465px;top:300px;width:150px">
 <div class="c" style="top:490px;font:700 40px Bit;letter-spacing:10px;color:var(--gold)">MERRY MAHJONG</div>
 <div class="c cap" style="top:580px;font-size:104px;color:#fff;white-space:nowrap">Find <span style="font:italic 600 106px/1 PF;color:var(--pink)">Your</span> Mat-ch<sup style="font-size:38px;vertical-align:top;position:relative;top:14px">™</sup></div>
 <div class="c" style="top:760px;font:italic 600 50px/1.3 PF;color:var(--cream);padding:0 90px">The only place to see holiday tiles, mats &amp; racks together, then shop them.</div>
 <div class="c" style="top:1010px" id="shop"><span class="pill" style="background:var(--pink);color:#fff;font-size:44px;letter-spacing:3px;padding:22px 46px;text-transform:none">Shop now · use code MAHJMATCH</span></div>
 <div class="c" style="top:1190px"><span class="pill" style="background:transparent;border:4px solid var(--gold);color:var(--gold);font-size:32px">Link in bio</span></div>
</div>
<script>
const C=__CFG__; const H=__H__;
const BEAT=0.4, b=t=>t/BEAT;
const cl=x=>Math.min(Math.max(x,0),1), eo=x=>1-Math.pow(1-cl(x),3), eb=x=>{x=cl(x);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const $=id=>document.getElementById(id);
// snow
const SN=[];let sd=3;const rnd=()=>{sd=(sd*16807)%2147483647;return sd/2147483647};
for(let i=0;i<90;i++){const e=document.createElement('i');const s=4+rnd()*12;e.style.width=e.style.height=s+'px';e.style.opacity=.35+rnd()*.55;$('snow').appendChild(e);SN.push([e,rnd()*1080,rnd()*H,40+rnd()*90,rnd()*6]);}
function snow(t,on){if(window.NOSNOW)on=false;$('snow').style.display=on?'block':'none';if(!on)return;for(const [e,x,y,v,p] of SN){e.style.left=(x+Math.sin(t*1.3+p)*30)+'px';e.style.top=((y+t*v)%(H+40)-20)+'px';}}
// burst mats
C.BURST.forEach((u,i)=>{const im=document.createElement('img');im.src=u;im.className='burst';im.style.display='none';$('bursts').appendChild(im);});
// odometer
function buildOdo(n){const o=$('odo');o.innerHTML='';const s=String(n);for(const ch of s){const d=document.createElement('div');d.className='dg';const st=document.createElement('div');st.className='st';for(let r=0;r<4;r++)for(let k=0;k<10;k++){const x=document.createElement('div');x.textContent=k;st.appendChild(x);}d.appendChild(st);o.appendChild(d);}o.dataset.n=s;}
function setOdo(n,p,plus){if($('odo').dataset.n!==String(n)+(plus?'+':''))
 {buildOdo(n);if(plus){const s=document.createElement('div');s.className='plus';s.textContent='+';s.id='pl';$('odo').appendChild(s);}$('odo').dataset.n=String(n)+(plus?'+':'');}
 const s=String(n);[...$('odo').querySelectorAll('.dg')].forEach((d,i)=>{const tgt=+s[i];const turns=2+i;const total=(turns*10+tgt);const q=eo(p);const pos=total*q;d.firstChild.style.transform=`translateY(${-(pos%40)*288+6}px)`;});
 const pl=$('pl');if(pl){pl.style.opacity=p>=1?1:0;}}
function mosaic(list,cols){const m=$('mos');if(m.dataset.k===list[0]+cols)return;m.dataset.k=list[0]+cols;m.innerHTML='';m.style.gridTemplateColumns=`repeat(${cols},1fr)`;const rows=Math.ceil((H+80)/(1160/cols))+1;m.style.gridAutoRows=(1160/cols)+'px';for(let i=0;i<cols*rows;i++){const im=document.createElement('img');im.src=list[(i*7)%list.length];m.appendChild(im);}}
// photo dump
function photo(item,k,zoomIn){const [u,name,brand,kind]=item;const ph=$('ph');if(ph.dataset.u!==u){ph.dataset.u=u;
  const bg=kind==='rack'?'#b3202a':kind==='tile'?'#f3ece2':'#062a55';
  ph.innerHTML=`<div style="position:absolute;inset:0;background:${bg}"></div>`+(kind==='rack'?`<img src="${u}" style="position:absolute;left:40px;top:640px;width:1000px;transform:rotate(-8deg)">`:`<img src="${u}" style="position:absolute;left:-200px;top:-200px;width:1480px;height:2320px;object-fit:cover;filter:blur(40px) brightness(.75)"><img class="fg" src="${u}" style="position:absolute;left:0;top:${kind==='mat'?330:300}px;width:1080px;height:${kind==='mat'?1080:1080}px;object-fit:${kind==='mat'?'contain':'cover'};box-shadow:0 30px 70px rgba(0,0,0,.45)">`)+
   `<div class="lab ${kind==='mat'?'n':''}" style="left:60px;top:${kind==='rack'?1060:1310}px">${name}<small>${brand}</small></div>`;}
  const im=ph.querySelector('img.fg')||ph.querySelector('img');im.style.transform=(kind==='rack'?'rotate(-8deg) ':'')+`scale(${1.12-0.08*eo(k)})`;
  const lb=ph.querySelector('.lab');lb.style.transform=`translateY(${(1-eb(Math.min(1,k*3)))*60}px)`;lb.style.opacity=cl(k*4);}
// app frames
const F1=[[0,0],[1.0,0],[1.02,1],[1.9,1],[1.95,3],[2.35,40],[2.9,42],[2.95,43],[3.45,49],[3.5,50],[3.95,59],[4.0,60],[5.45,100],[5.5,101],[5.95,113],[6.4,113],[6.45,115],[7.4,119],[7.45,120],[7.95,125],[8.4,126],[9.4,150],[12,157]];
const F2=[[0,0],[0.15,2],[1.6,27],[2.0,36],[2.2,36],[2.21,39],[2.75,47],[3.15,48],[3.25,48],[3.26,50],[3.4,51],[3.41,53],[3.9,59],[4.4,60],[4.6,61],[4.61,64],[5.15,72],[5.6,75],[5.61,77],[5.74,77],[5.75,113],[8,125]];
function fidx(K,t){if(t<=K[0][0])return K[0][1];for(let i=1;i<K.length;i++){if(t<=K[i][0]){const [a,x]=K[i-1],[c,y]=K[i];return Math.round(x+(y-x)*(t-a)/(c-a));}}return K[K.length-1][1];}
function frame(base,i){const u=base+String(i).padStart(5,'0')+'.jpg';const f=$('fr');if(f.dataset.u!==u){f.src=u;f.dataset.u=u;}}
const SC=900/780; // frame px -> screen px
function scr2page(x,y){return [62+28+x*SC, 300+28+y*SC];}
function cam(s,fx,fy,dy){ // zoom s around frame point (fx,fy), shift so that point lands at page y=dy
 const [px,py]=scr2page(fx,fy);const tx=540-px*s, ty=dy-py*s;$('cam').style.transform=`translate(${tx}px,${ty}px) scale(${s})`;$('cam').style.transformOrigin='0 0';return [tx,ty,s];}
function lab(html,x,y,cls,k,rot){return `<div class="lab ${cls||''}" style="left:${x}px;top:${y}px;transform:rotate(${rot||-3}deg) scale(${0.6+0.4*eb(k)});opacity:${cl(k*3)}">${html}</div>`;}
function ring(x,y,k){return `<div class="ring" style="left:${x}px;top:${y}px;transform:scale(${0.5+eo(k)*1.1});opacity:${1-cl(k)}"></div>`;}
// quilt
(function(){const q=$('quilt');C.QU.forEach((u,i)=>{const im=document.createElement('img');im.src=u;const c=i%6,r=Math.floor(i/6);im.style.left=(c*180)+'px';im.style.top=(r*180+(H-1620)/2)+'px';im.style.display='none';q.appendChild(im);});})();
const QORD=(()=>{const a=[...Array(54).keys()];let s=17;const r=()=>{s=(s*16807)%2147483647;return s/2147483647};const c=[26,27,20,21];const rest=a.filter(x=>!c.includes(x)).sort(()=>r()-.5);return [26,27,20,21,...rest];})();

const SCN=[['s1',0,4],['s2',4,16],['s3',16,20],['s4',20,32],['s5',32,40],['s4',40,50],['s6',50,52],['s3',52,60],['s6',60,64],['s9',64,72]];
window.render=function(t){const B=b(t);
 let cur=null;for(const [id,a,z] of SCN){if(B>=a&&B<z){cur=[id,a,z];}}
 for(const id of ['s1','s2','s3','s4','s5','s6','s9'])$(id).style.display=(cur&&cur[0]===id)?'block':'none';
 if(!cur)return; const [id,a]=cur; const L=B-a;
 snow(t,['s1','s2','s9','s5'].includes(id)&&!(id==='s5'&&L<6));
 if(a===0){ // hook
  $('h1').innerHTML=L<2?'We made a<br>holiday list.':'And checked<br>it twice.';
  $('h1').style.transform=`scale(${0.85+0.15*eb((L%2)/0.5)})`;
  const shake=L<3?Math.sin(L*Math.PI*2)*6*(1-(L%1)):0;$('box').style.transform=`rotate(${shake}deg) translateY(${L>=3?-40*eo(L-3):0}px)`;
  const pop=eo((L-3)/0.6);$('lid').style.transform=`translate(${pop*-60}px,${-pop*420}px) rotate(${-pop*28}deg)`;$('lid').style.opacity=1-cl((L-3.3)/0.5);
  [...$('bursts').children].forEach((im,i)=>{const on=L>=3;im.style.display=on?'block':'none';if(!on)return;const k=eo((L-3)/0.9);const ang=Math.PI*(-0.08+1.16*i/(C.BURST.length-1));const r=200+620*k*(0.7+0.3*((i*37)%10)/10);
    im.style.left=(540-150+Math.cos(ang)*r)+'px';im.style.top=(1000-150+Math.sin(ang)*r*0.75)+'px';im.style.transform=`scale(${0.3+0.45*k}) rotate(${(i%2?1:-1)*k*30}deg)`;});
 }
 if(a===4){ const i=Math.floor(L/4), k=L-i*4;
  const D=[[140,'holiday mats','in Find Your Mat-ch™',C.QU,5,true],[10,'holiday tile sets','ready to swipe',C.TILES13,4,true],[40,'holiday albums','full of match cards',C.COV,4,true]][i]; /* canonical counts: ../../COUNTS.md */
  mosaic(D[3],D[4]); $('mos').style.display=window.NOSNOW?'none':'grid'; $('mos').style.transform=`scale(${1.08-0.06*L/12}) translateY(${-k*12}px)`;
  setOdo(D[0],k/2,D[5]); const land=cl((k-2)/0.4); $('odo').style.transform=`scale(${1+0.08*Math.sin(Math.PI*land)})`;
  $('olab').textContent=D[1]; $('olab').style.opacity=cl((k-1.6)/0.4); $('olab').style.transform=`translateY(${(1-eo((k-1.6)/0.5))*40}px)`;
  $('osub').textContent=D[2]; $('osub').style.opacity=cl((k-2.2)/0.4);
  $('kick').style.opacity=i===0?1:0.0+1;
 }
 if(id==='s3'){ if(a===16){const i=Math.min(3,Math.floor(L));photo(C.DUMP1[i],L-i);}
  else { if(L<4.5){const i=Math.min(8,Math.floor(L*2));photo(C.DUMP2[i],(L*2-i));}
   else{photo(C.DUMP2[8],1);}
   // 400+ counter over photo dump from 4.5
   const ph=$('ph');let cc=ph.querySelector('#c400');if(L>=4.5){if(!cc){cc=document.createElement('div');cc.id='c400';cc.style.cssText='position:absolute;inset:0;background:rgba(6,42,85,.9)';cc.innerHTML=`<div class="c cap" style="top:470px;font-size:300px;color:var(--cream)"><span id="n400">0</span><span style="color:var(--gold)">+</span></div><div class="c cap" style="top:800px;font-size:96px;color:#fff">holiday matches</div><div class="c" style="top:930px;font:italic 600 60px PF;color:var(--gold)">and counting</div>`;ph.appendChild(cc);}
     const k=eo((L-4.5)/1.4);cc.style.opacity=cl((L-4.5)/0.25);$('n400').textContent=Math.round(400*k);} else if(cc)cc.remove();
  }}
 if(id==='s4'){
  const ov=$('ov'), lb=$('labs'); let o='',l='';
  if(a===20){ const fi=fidx(F1,L); frame(C.REC,fi);
   $('headt').innerHTML=L<3?'Pick your tiles. Tap Holiday.':(L<8.4?'Swipe holiday mats.':'Your holiday suitors');
   if(L<2){ // chips push-in on Holiday chip (frame px 327,1071)
     const s=1+0.9*eo(L/1.0); cam(s,327,1071,1000);
     if(L>=1.0) o+=ring(327*SC,1071*SC,(L-1.0)/0.5);
     if(L>=1.0) l+=lab('Holiday',330,1180,'',(L-1.0)/0.3,-4);
   } else if(L<8.4){ const s=1.12; cam(s,390,900,1080);
     // labels on tiles band + mat
     l+=lab('Dear Santa tiles<small>Anders Ruff</small>',40,560,'n',(L-2.4)/0.3,-3);
     if(L>=2.95&&L<3.95) l+=lab('✕ The Polo Club<small>Luxe Mahjong</small>',70,1240,'x',(L-3.0)/0.3,-3);
     if(L>=4.0&&L<5.95) l+=lab('♥ Candy Cane Lane<small>Anders Ruff</small>',70,1240,'',(L-4.0)/0.3,-3);
     if(L>=6.45&&L<7.95) l+=lab('♥ Festive Plaid Premium<small>Sunday Mahjong</small>',70,1240,'',(L-6.45)/0.3,-3);
     if(L>=5.95&&L<6.45) l+=lab('Classic Very Merry Mahj<small>Anders Ruff</small>',70,1240,'n',(L-5.95)/0.3,-3);
     for(const [t0,kind] of [[3.5,'x'],[5.5,'h'],[7.45,'h']]) if(L>=t0&&L<t0+0.45){const k=(L-t0)/0.25;o+=`<div class="stamp" style="left:${kind==='x'?470:90}px;top:700px;color:${kind==='x'?'#5e5368':''};border-color:${kind==='x'?'#5e5368':''};transform:rotate(${kind==='x'?14:-14}deg) scale(${1.8-0.8*eo(k)});opacity:${cl(k*2)*(1-cl((L-t0-0.3)/0.15))}">${kind==='x'?'✕':'♥'}</div>`;}
   } else { // suitors push-in
     const s=1+0.6*eo((L-8.6)/1.2); cam(s,330,1110,1000);
     if(L>=9.4) l+=lab('2 suitors<small>Candy Cane Lane · Festive Plaid Premium</small>',60,760,'',(L-9.4)/0.3,-3);
   }
  } else { // racks a=40
   const fi=fidx(F2,L); frame(C.REC2,fi);
   $('headt').innerHTML=L<1.9?'Zoom in on the mat.':(L<5.75?'Swipe racks to match.':'It&rsquo;s a match!');
   if(L<5.7){ if(L<1.6){cam(1.0+0.3*eo(L/0.8),390,700,760);} else {const k=eo((L-1.6)/0.4); cam(1.3-0.38*k,390,700+363*k,760+170*k);}
     for(const t0 of [0.1,0.55,1.0]) if(L>=t0&&L<t0+0.5) o+=ring(706*SC,592*SC,(L-t0)/0.45);
     if(L>=0.2) l+=lab('Festive Plaid Premium<small>Sunday Mahjong · zoomed in</small>',40,880,'n',(L-0.2)/0.3,-3);
     if(L>=2.0&&L<3.1) l+=lab('♥ Persimmon<small>Bird & Bamboo</small>',80,1180,'',(L-2.0)/0.3,-3);
     if(L>=3.25&&L<4.4) l+=lab('✕ Basil<small>Bird & Bamboo</small>',80,1180,'x',(L-3.25)/0.3,-3);
     if(L>=4.4&&L<5.6) l+=lab('♥ Walnut<small>Bam Bird Boutique</small>',80,1180,'',(L-4.4)/0.3,-3);
   } else { const s=1.0+0.25*eo((L-6.2)/1.2); cam(s,390,1200,1060); }
  }
  ov.innerHTML=o; lb.innerHTML=l; $('head').style.opacity=1;
 }
 if(id==='s5'){ // quilt doubles per beat
  const n=L<6?Math.min(54,Math.pow(2,Math.floor(L))):54; const imgs=[...$('quilt').children];
  QORD.forEach((qi,j)=>{const im=imgs[qi];const on=j<n;im.style.display=on?'block':'none';if(on){const born=j===0?0:Math.floor(Math.log2(j))+1;const k=(L-born)/0.35;im.style.transform=`scale(${eb(Math.min(1,Math.max(k,0)))})`;}});
  $('quilt').style.transform=`scale(${1+0.04*L/8})`;$('quilt').style.transformOrigin='540px 960px';
  const W=['Christmas.','Hanukkah.','Snow days.'];let w='';
  if(L>=5&&L<8){const i=Math.min(2,Math.floor(L-5));const k=L-5-i;w=`<div class="word" style="top:${[700,880,1060][i]}px"><span style="background:${['#b3202a','#054689','#1f5a3a'][i]};transform:rotate(${[-4,3,-2][i]}deg) scale(${0.7+0.3*eb(k/0.4)})">${W[i]}</span></div>`;
   for(let j=0;j<i;j++) w+=`<div class="word" style="top:${[700,880,1060][j]}px"><span style="background:${['#b3202a','#054689','#1f5a3a'][j]};transform:rotate(${[-4,3,-2][j]}deg)">${W[j]}</span></div>`;}
  $('qw').innerHTML=w;
 }
 if(id==='s6'){ const cd=$('card'); if(!cd.src)cd.src=C.CARD;
  if(a===50){ const k=eo(L/0.8); cd.style.left=(90)+'px';cd.style.top=(300+(1-k)*300)+'px';cd.style.width='900px';cd.style.transform=`rotate(${(1-k)*-6}deg) scale(${0.85+0.15*k})`;
    $('cardt').innerHTML=`<div class="c" style="top:200px"><span class="pill" style="background:var(--pink);color:#fff;transform:scale(${eb(cl(L/0.4))});display:inline-block">It&rsquo;s a match!</span></div>`;}
  else { const k=eo(L/0.6); cd.style.width=(900-260*k)+'px';cd.style.left=(90+130*k)+'px';cd.style.top=(300+210*k)+'px';cd.style.transform=`rotate(${-3*k}deg)`;
    const words=['Holiday tiles','+ mats','+ racks','together.'];let h='';for(let i=0;i<4;i++){if(L>=i*0.9){const kk=(L-i*0.9)/0.35;h+=`<div class="word" style="top:${[270,410,1290,1430][i]}px"><span style="font-size:96px;padding:12px 36px 22px;background:${['#062a55','#b3202a','#1f5a3a','#d6336c'][i]};transform:rotate(${[-3,2,-2,3][i]}deg) scale(${0.6+0.4*eb(cl(kk))})">${words[i]}</span></div>`;}}
    $('cardt').innerHTML=h;}
 }
 if(id==='s9'){ $('fh').style.transform=`scale(${eb(cl(L/0.5))})`; $('shop').style.transform=`scale(${L<1?eb(cl((L-0.3)/0.5)):1+0.05*Math.sin(Math.PI*2*((L)%1))})`; }
};
</script></body></html>"""

def page(H=1920):
    return HTML.replace('__F__', FONTS).replace('__H__', str(H)).replace('__FH__', CFG['FH']).replace('__CFG__', json.dumps(CFG))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'frames'
    out = f'{W}/out'; os.makedirs(out, exist_ok=True)
    open(f'{W}/reel.html', 'w').write(page())
    FPS, DUR = 30, 28.8
    fd = f'{W}/frames'
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(f'file://{W}/reel.html'); pg.wait_for_timeout(2500)
        if mode == 'frames':
            if os.path.isdir(fd): shutil.rmtree(fd)
            os.makedirs(fd)
            # preload all rec frames
            for n in range(int(FPS * DUR)):
                pg.evaluate(f"render({n / FPS})")
                pg.evaluate("()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})))")
                pg.screenshot(path=f'{fd}/{n:04d}.jpg', type='jpeg', quality=92)
        else:
            if mode == 'nosnow': pg.evaluate("window.NOSNOW=1")
            for tt in [float(x) for x in sys.argv[2:]]:
                pg.evaluate(f"render({tt})"); pg.wait_for_timeout(400)
                pg.screenshot(path=f'{out}/t{tt:05.2f}.jpg', type='jpeg', quality=88)
        b.close()
