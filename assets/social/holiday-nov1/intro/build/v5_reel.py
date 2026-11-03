"""Holiday intro reel v4 (Nov 3 2026), per Tiffany's v3 notes Nov 3 1:58pm (docs/ANSWERS.md) on top of v3.
42.0s = 105 beats @150 BPM. Opener + mat wall kept; tile wall swaps to the sets' holiday album covers; "50+ brands"
partner-logo tickers replace the album wall; white iPhone frame; step text sits in the white space ABOVE the phone
(y 330, phone top 470) and never over the app; mats screen in context ("Pick your mat") before the Holiday push-in;
4 hearts; the "Which suitor is the one?" pick screen; match card camera push-in until it leaves the frame; end card with
two partner-logo tickers (code partners only; no Sunday, no Tigre de Tartan next to "use code").
Inputs: /dev/shm/introv2/{rec0,recA,recP,recB} (v4_capture.py) + /dev/shm/introv3/{wall,tiles,brand} + /dev/shm/introv4/logos.
Usage: python3 v4_reel.py frames [a-b ...] | stills t1 t2 ...   -> /dev/shm/introv4/{frames,out}"""
import json, os, sys, shutil, glob
W2 = '/dev/shm/introv2'; W = '/dev/shm/introv3'; W4 = '/dev/shm/introv4'; W5 = '/dev/shm/introv5'
os.environ['TMPDIR'] = W2 + '/tmp'
from playwright.sync_api import sync_playwright
R = '/home/claude/mahjmatchmaker-data'
FONTS = f'file://{R}/scripts/social/tileprofile/fonts'
F = lambda p: 'file://' + p
WALL = [F(r['f']) for r in json.load(open(f'{W}/wall_sel.json'))]
# v5 (Tiffany 2:32pm): the 3 sets with NO holiday album sit in row 3 (cells 6-8) under the centred counter box; every album set shows
TORD = ['dear-santa', 'rackin-rudolph', 'hj-red', 'hj-green', 'hj-pink', 'tin-ruby', 'niv-emerald', 'merry-nutcracker', 'spirit',
        'tin-emerald', 'niv-blue', 'nutcracker', 'apres', 'dec1994', 'dear-santa']
TWALL = [F(f'{W}/tiles/{n}.jpg') for n in TORD]
CV = f'{R}/assets/covers/holiday/'
CMAP = {'dear-santa': 'dear-santa', 'rackin-rudolph': 'rackin-rudolph', 'hj-red': 'holly-jolly-red', 'hj-green': 'holly-jolly-green', 'hj-pink': 'holly-jolly-pink',
        'tin-ruby': 'tinselle-ruby', 'tin-emerald': 'tinselle-emerald', 'niv-blue': 'nivalee-blue', 'nutcracker': 'nutcracker-ballet', 'apres': 'cmc-apres-ski',
        'dec1994': 'december-1994'}   # Nivalee Emerald, Merry Nutcracker, Spirit of Christmas have no holiday album cover: their tile photo stays
TC = [CMAP.get(n) for n in TORD]
TCOV = [F(CV + c + '.jpg') if c else '' for c in TC]
LG = '/dev/shm/introv4/logos/'
ALLP = ['omm','mrc','missm','myfair','middlemain','bb','bambird','squad','tdt','britt','plm','cmc','bespoke','virora','ar','mood','minimahjer','macmiller','toppe','amahj','mahjon','vine','hiphip','bam','ymi','mahjongco','studios','ilovemahj','splash','wren','press','royal','soiree','register','lbb','yolo','maison','noli']
PLOGOS = [F(LG + n + '.png') for n in ALLP]                       # 38 code partners (assets/hub/partner-brands-2026-10-30.jpg)
ELOGOS = [F(LG + n + '.png') for n in ALLP if n != 'tdt']         # end card sits next to "use code": no Tigre de Tartan (affiliate policy)
def rt(r):
    d = json.load(open(f'{W2}/{r}/marks.json')); Fr = d['frames']; return [round(x - Fr[0], 3) for x in Fr]
XC = [F(f) for f in sorted(glob.glob(f'{W4}/xcards/*.png'))]   # v5_cards.py: 15 cross-brand FYM match cards (Amara x Very Merry Wreath first), full-frame wall
CFG = dict(XC=XC, WALL=WALL, TWALL=TWALL, TCOV=TCOV, PLOGOS=PLOGOS, ELOGOS=ELOGOS, CARD=F(f'{W2}/recB/storycard.png'),
           R0=F(f'{W2}/rec0/f/'), RA=F(f'{W2}/recA/f/'), RP=F(f'{W2}/recP/f/'), RB=F(f'{W2}/recB/f/'),
           T0=rt('rec0'), TA=rt('recA'), TP=rt('recP'), TB=rt('recB'),
           FL=F(f'{W}/brand/fl.png'), FLH=F(f'{W}/brand/flh.png'), WM=F(f'{R}/assets/brand/mahjmatchmaker-wordmark-notag.png'), WMH=F(f'{R}/assets/brand/mahjmatchmaker-wordmark-holiday-notag.png'))

HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Cap;src:url(__F__/Caprasimo.ttf)}
@font-face{font-family:Bit;src:url(__F__/bitter-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:Bit;src:url(__F__/bitter-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:PF;src:url(__F__/playfair-display-latin-600-italic.woff2);font-style:italic}
:root{--navy:#062a55;--red:#b3202a;--green:#1f5a3c;--gold:#e9c77b;--cream:#faf3ea}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;position:relative;background:radial-gradient(ellipse at 50% 42%,#ffffff 0%,#eef6fc 38%,#d9eaf6 75%,#c6ddef 100%);font-family:Bit}
#app{z-index:10}
.sc{position:absolute;inset:0;display:none;overflow:hidden}
.bgn{background:radial-gradient(ellipse at 50% 42%,#ffffff 0%,#eef6fc 38%,#d9eaf6 75%,#c6ddef 100%)}
.snow{position:absolute;inset:0;pointer-events:none;z-index:45}
.snow i{position:absolute;border-radius:50%;background:#fff;box-shadow:0 0 0 2px rgba(120,165,205,.55),0 3px 8px rgba(60,110,160,.35)}
.plate{position:absolute;left:0;right:0;text-align:center;z-index:50}
.plate span{display:inline-block;font:400 76px/1.08 Cap;color:var(--navy);background:#fff;padding:22px 48px 30px;border-radius:32px;box-shadow:0 14px 36px rgba(30,70,120,.28);white-space:nowrap;text-align:center}
.cell{position:absolute;overflow:hidden;background:#fff}
.cell img{width:100%;height:100%;object-fit:cover;display:block}
.cnt{position:absolute;left:110px;right:110px;top:560px;padding:40px 0 46px;background:rgba(255,255,255,.94);border-radius:40px;box-shadow:0 30px 70px rgba(20,50,90,.38);text-align:center;z-index:20}
.odo{display:flex;justify-content:center;height:300px}
.grp{position:relative;display:flex;gap:10px}
.dg{width:190px;height:290px;overflow:hidden;position:relative;background:var(--navy);border-radius:26px;border:6px solid var(--gold);box-shadow:0 16px 36px rgba(20,50,90,.35)}
.dg .st{position:absolute;left:0;right:0;top:0}
.dg .st div{height:278px;font:400 236px/278px Cap;color:var(--cream);text-align:center}
.plus{position:absolute;left:100%;top:-6px;margin-left:12px;font:400 176px/1 Cap;color:var(--red)}
.olab{margin-top:22px;font:400 92px/1.05 Cap;color:var(--navy)}
.word{position:absolute;left:0;right:0;text-align:center;z-index:21}
.word span{display:inline-block;font:400 104px/1 Cap;color:#fff;padding:20px 50px 30px;border-radius:30px;box-shadow:0 18px 44px rgba(0,0,0,.35)}
.cam{position:absolute;left:0;top:0;transform-origin:0 0}
.bez{position:absolute;left:-28px;top:-28px;width:836px;height:1834px;border-radius:120px;background:#f7f7f5;box-shadow:0 34px 80px rgba(30,70,120,.30),inset 0 0 0 5px #d6d6d3}
.bez i{position:absolute;width:11px;background:#e2e2df;border-radius:4px}
.sb{position:absolute;left:0;top:0;width:780px;height:90px;background:#fff;font:600 34px -apple-system,Helvetica,Arial;color:#111}
.isl{position:absolute;left:276px;top:20px;width:228px;height:62px;background:#000;border-radius:40px}
.tick{position:absolute;left:0;width:1080px;height:150px;overflow:hidden}
.tick .row{position:absolute;top:0;left:0;display:flex;gap:22px;white-space:nowrap}
.chip{flex:none;width:230px;height:150px;background:#fff;border-radius:24px;box-shadow:0 10px 26px rgba(30,70,120,.18);display:flex;align-items:center;justify-content:center}
.chip img{max-width:212px;max-height:132px;object-fit:contain}
.scr{position:absolute;left:0;top:0;width:780px;height:1778px;border-radius:92px;overflow:hidden;background:#fff}
.apz{position:absolute;left:0;top:90px;width:780px;height:1688px}
.scr img.f{position:absolute;left:0;top:0;width:780px;height:1688px}
.ring{position:absolute;border-radius:50%;border:10px solid var(--red)}
.pill{display:inline-block;font:700 46px/1.1 Bit;padding:18px 42px;border-radius:60px;white-space:nowrap}
.spk{position:absolute;width:26px;height:26px;background:var(--gold);clip-path:polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%)}
.mc{position:absolute;border-radius:26px;box-shadow:0 34px 80px rgba(30,70,120,.40)}
</style></head><body>
<div class="snow" id="snow"></div>
<div id="open" class="sc bgn">
 <div id="wmw" style="position:absolute;left:260px;top:405px;width:560px;height:80px"><img id="wm" src="__WM__" style="position:absolute;left:0;top:0;width:560px"><img id="wmh" src="__WMH__" style="position:absolute;left:0;top:0;width:560px;opacity:0"></div>
 <div id="flw" style="position:absolute;left:420px;top:535px;width:240px;height:260px"><img id="fl" src="__FL__" style="position:absolute;inset:0;width:240px"><img id="flh" src="__FLH__" style="position:absolute;inset:0;width:240px;opacity:0"><div id="spks"></div></div>
 <div id="olk" style="position:absolute;left:0;right:0;top:845px;text-align:center"><span style="display:inline-block;font:400 104px/1 Cap;color:var(--navy);white-space:nowrap;position:relative">Find <span style="font:italic 600 108px/1 PF;color:var(--red)">Your</span> Mat-ch<span style="position:absolute;font:400 38px Bit;margin-left:4px;margin-top:4px">™</span></span></div>
 <div id="hed" style="position:absolute;left:0;right:0;top:1035px;text-align:center"><span class="pill" style="background:var(--red);color:#fff;letter-spacing:8px;font-size:44px;border:5px solid var(--gold);padding:16px 46px">HOLIDAY EDITION</span></div>
 <div id="iht" style="position:absolute;left:0;right:0;top:1200px;text-align:center"><span style="display:inline-block;font:400 76px/1.05 Cap;color:var(--green);background:#fff;padding:26px 56px 38px;border-radius:40px;box-shadow:0 18px 44px rgba(30,70,120,.25);white-space:nowrap">It&rsquo;s holiday time!</span></div>
</div>
<div id="wall" class="sc bgn"><div id="wg" style="position:absolute;left:0;top:0;width:1080px"></div><div id="veil" style="position:absolute;inset:0;background:#eef6fc;opacity:0"></div>
 <div id="ticks"></div><div class="cnt" id="cnt"><div class="odo"><div class="grp" id="grp"></div></div><div class="olab" id="olab"></div></div><div id="words"></div></div>
<div id="app" class="sc"><div class="cam" id="cam"><div class="bez"><i style="left:-9px;top:300px;height:80px"></i><i style="left:-9px;top:430px;height:140px"></i><i style="left:-9px;top:600px;height:140px"></i><i style="right:-9px;top:470px;height:210px"></i></div><div class="scr"><div class="sb"><span style="position:absolute;left:96px;top:24px">9:41</span><span style="position:absolute;right:86px;top:26px;font-size:26px;letter-spacing:3px">▂▄▆ ◔ ▭</span><div class="isl"></div></div><div class="apz"><img class="f" id="fr"><svg id="spot" width="780" height="1688" style="position:absolute;left:0;top:0"></svg><div id="ov" style="position:absolute;inset:0"></div></div></div></div>
 <div id="intro" style="position:absolute;left:0;right:0;top:250px;text-align:center;z-index:50"></div></div>
<div id="cardsc" class="sc bgn"><img id="mcard" class="mc"><div id="boom"></div></div>
<div id="end" class="sc bgn">
 <img src="__FLH__" id="fh" style="position:absolute;left:465px;top:250px;width:150px">
 <img src="__WMH__" style="position:absolute;left:290px;top:420px;width:500px">
 <div style="position:absolute;left:0;right:0;top:530px;text-align:center"><span style="display:inline-block;font:400 104px/1 Cap;color:var(--navy);white-space:nowrap;position:relative">Find <span style="font:italic 600 108px/1 PF;color:var(--red)">Your</span> Mat-ch<span style="position:absolute;font:400 38px Bit;margin-left:4px;margin-top:4px">™</span></span></div>
 <div style="position:absolute;left:0;right:0;top:675px;text-align:center;font:italic 600 58px/1.28 PF;color:var(--navy)">Match holiday tiles, mats<br>&amp; racks across brands</div>
 <div style="position:absolute;left:0;right:0;top:860px;text-align:center"><span class="pill" id="shop" style="background:var(--red);color:#fff;font-size:48px">Shop now · use code MAHJMATCH</span></div>
 <div style="position:absolute;left:0;right:0;top:985px;text-align:center"><span class="pill" style="background:#fff;border:4px solid var(--green);color:var(--green);font-size:34px;letter-spacing:4px;text-transform:uppercase;padding:14px 36px">Link in bio</span></div>
 <div id="eticks"></div>
</div>
<div class="plate" id="plate"><span id="plt"></span></div>
<script>
const C=__CFG__;
const cl=x=>Math.min(Math.max(x,0),1), eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}, eb=x=>{x=cl(x);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const $=id=>document.getElementById(id);
let sd=3;const rnd=()=>{sd=(sd*16807)%2147483647;return sd/2147483647};
const SN=[];for(let i=0;i<120;i++){const e=document.createElement('i');const s=6+rnd()*12;e.style.width=e.style.height=s+'px';e.style.opacity=.55+rnd()*.45;$('snow').appendChild(e);SN.push([e,rnd()*1080,rnd()*1960,50+rnd()*90,rnd()*6]);}
function snow(t,a,z){$('snow').style.opacity=a;$('snow').style.zIndex=z||45;for(const [e,x,y,v,p] of SN){e.style.left=(x+Math.sin(t*1.3+p)*30)+'px';e.style.top=((y+t*v)%1980-30)+'px';}}
function plate(txt,k,y){const p=$('plate');if(!txt){p.style.display='none';return;}p.style.display='block';p.style.top=(y||250)+'px';
 if($('plt').innerHTML!==txt)$('plt').innerHTML=txt;$('plt').style.transform=`scale(${0.86+0.14*eb(k/0.3)})`;p.style.opacity=cl(k/0.12);}
// ---------- opener ----------
for(let i=0;i<10;i++){const s=document.createElement('div');s.className='spk';$('spks').appendChild(s);}
function opener(L){L+=0.25; /* first frame already shows the lockup (cover/thumbnail) */
 const a=eb(L/0.4); $('wmw').style.opacity=cl(L/0.25); $('wmw').style.transform=`translateY(${(1-eo(L/0.4))*-30}px)`;
 $('olk').style.opacity=cl(L/0.2); $('olk').style.transform=`scale(${0.7+0.3*a})`;
 const k=(L-0.8)/0.35; // flame puts on its holiday look
 $('fl').style.opacity=1-cl(k); $('flh').style.opacity=cl(k); $('wm').style.opacity=1-cl(k); $('wmh').style.opacity=cl(k);
 $('flw').style.transform=`scale(${(L<0.8?eb(L/0.45):1)*(1+0.22*Math.sin(Math.PI*cl(k)))}) rotate(${-8*Math.sin(Math.PI*cl(k))}deg)`;
 [...$('spks').children].forEach((s,i)=>{const q=(L-0.8-i*0.02)/0.6;const ang=i/10*Math.PI*2;const r=60+170*eo(q);s.style.left=(107+Math.cos(ang)*r)+'px';s.style.top=(117+Math.sin(ang)*r)+'px';s.style.opacity=q>0&&q<1?1-q*q:0;s.style.transform=`scale(${1.4-0.8*cl(q)}) rotate(${q*180}deg)`;});
 const h=(L-1.15)/0.35; $('hed').style.opacity=cl(h*3); $('hed').style.transform=`translateY(${(1-eb(h))*-120}px)`;
 const t=(L-1.6)/0.35; $('iht').style.opacity=cl(t*3); $('iht').style.transform=`scale(${0.6+0.4*eb(t)}) rotate(${-3*cl(t)}deg)`;}
// ---------- walls (tile out from the centre, doubling every 0.2s, edge to edge) ----------
const WL={};
function mkwall(key,imgs,cols,cw,ch,top){const g=document.createElement('div');g.style.position='absolute';g.style.left='0';g.style.top=top+'px';g.dataset.k=key;g.style.display='none';
 const n=imgs.length,rows=Math.ceil(n/cols);const cells=[];
 imgs.forEach((u,i)=>{const c=i%cols,r=Math.floor(i/cols);const d=document.createElement('div');d.className='cell';d.style.left=(c*cw)+'px';d.style.top=(r*ch)+'px';d.style.width=cw+'px';d.style.height=ch+'px';d.style.boxShadow='inset 0 0 0 3px #fff';d.innerHTML=`<img src="${u}">`;g.appendChild(d);
  const dx=(c+.5)/cols-.5,dy=((r+.5)*ch+top-960)/1920;cells.push([Math.hypot(dx,dy*0.6)+rnd()*0.08,i]);});
 cells.sort((a,b)=>a[0]-b[0]);$('wg').appendChild(g);WL[key]={g,ord:cells.map(x=>x[1]),n};}
mkwall('m',C.WALL,6,180,180,-30);
mkwall('t',C.TWALL,3,360,360,60);
mkwall('x',C.XC,3,360,450,-165);
function wall(key,L){for(const k in WL)WL[k].g.style.display=k===key?'block':'none';const W=WL[key];const ch=W.g.children;
 const n=Math.min(W.n,Math.pow(2,Math.floor(L/0.2)+2));
 W.ord.forEach((ci,j)=>{const d=ch[ci];const on=j<n;d.style.visibility=on?'visible':'hidden';if(on){const born=j<4?0:(Math.floor(Math.log2(j))-1)*0.2;d.style.transform=`scale(${eb((L-born+0.1)/0.3)})`;}});}
function buildOdo(n,plus,lab){const g=$('grp');if(g.dataset.n===lab)return;g.dataset.n=lab;g.innerHTML='';for(const ch of String(n)){const d=document.createElement('div');d.className='dg';const st=document.createElement('div');st.className='st';for(let r=0;r<4;r++)for(let k=0;k<10;k++){const x=document.createElement('div');x.textContent=k;st.appendChild(x);}d.appendChild(st);g.appendChild(d);}
 if(plus){const p=document.createElement('div');p.className='plus';p.id='pl';p.textContent='+';g.appendChild(p);} $('olab').textContent=lab;}
function counter(n,plus,lab,L,out){buildOdo(n,plus,lab);const s=String(n);const p=eo(L/0.8);
 [...$('grp').querySelectorAll('.dg')].forEach((d,j)=>{const tot=(2+j)*10+(+s[j]);d.firstChild.style.transform=`translateY(${-((tot*p)%40)*278+6}px)`;});
 const pl=$('pl');if(pl){pl.style.opacity=cl((L-0.8)/0.12);pl.style.transform=`scale(${0.6+0.4*eb((L-0.8)/0.3)})`;}
 const c=$('cnt');const k=eb(L/0.35);let ty=0,sc=0.6+0.4*k,op=cl(L/0.15);
 if(out!=null&&L>out){const q=eio((L-out)/0.4);ty=-330*q;sc=1-0.32*q;}
 c.style.opacity=op;c.style.transform=`translateY(${ty}px) scale(${sc})`;}
const WD=[['Christmas','#b3202a',-4],['Hanukkah','#1d4f9a',3],['Snow days','#1f5a3c',-2]];
function words(L){let h='';WD.forEach(([w,c,r],i)=>{const k=(L-i*0.6)/0.3;if(k<0)return;h+=`<div class="word" style="top:${[860,1050,1240][i]}px"><span style="background:${c};transform:rotate(${r}deg) scale(${0.7+0.3*eb(k)})">${w}</span></div>`;});$('words').innerHTML=h;}
// ---------- app ----------
function fidx(T,t){let lo=0,hi=T.length-1;if(t<=T[0])return 0;while(lo<hi){const m=(lo+hi+1)>>1;if(T[m]<=t)lo=m;else hi=m-1;}return lo;}
function pw(P,L){if(L<=P[0][0])return P[0][1];for(let i=1;i<P.length;i++){if(L<=P[i][0]){const [a,x]=P[i-1],[b,y]=P[i];return x+(y-x)*(L-a)/(b-a);}}return P[P.length-1][1];}
function frame(base,T,t){const i=fidx(T,t);const u=base+String(i).padStart(5,'0')+'.jpg';const f=$('fr');if(f.dataset.u!==u){f.src=u;f.dataset.u=u;}}
/* Nov 3 1:42pm safe zones: whole phone 0.88x and 110px lower so plates sit at y>=250 and the phone clears the right-side buttons */
/* v4: no extra global scale; scenes pass the screen scale k. Full-phone shots: phoneTop(k) puts the phone top at y 470 (text plate sits at y 330 above it). */
function camK(k,fy,py,x){$('cam').style.transform=`translate(${(x==null?540:x)-390*k}px,${py-(fy+90)*k}px) scale(${k})`;}
const PK=0.74; function phone(k){camK(k||PK,-90,470);}
/* v5 (Tiffany 2:32pm): the camera never parks. CK keys = [L, k, fx, fy]: app point (fx,fy) sits at screen (540,960) at zoom k; full phone = [.74,390,572] */
function camF(k,fx,fy){$('cam').style.transform=`translate(${540-fx*k}px,${960-(fy+90)*k}px) scale(${k})`;}
function cam(keys,L,t){let a=keys[0],b=keys[keys.length-1];for(let i=1;i<keys.length;i++){if(L<=keys[i][0]){a=keys[i-1];b=keys[i];break;}}
 const q=b[0]>a[0]?eio((L-a[0])/(b[0]-a[0])):1; const dr=Math.sin(t*1.7)*0.012; // gentle drift so it is never still
 camF((a[1]+(b[1]-a[1])*q)*(1+dr),a[2]+(b[2]-a[2])*q+Math.sin(t*1.1)*6,a[3]+(b[3]-a[3])*q+Math.cos(t*0.9)*6);}
const FULL=[.74,390,572];
function spot(holes,a){$('spot').innerHTML=a<=0?'':`<defs><filter id="bl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="16"/></filter><mask id="mk"><rect width="780" height="1688" fill="#fff"/>${holes.map(([x,y,w,h,r])=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r||22}" fill="#000" filter="url(#bl)"/>`).join('')}</mask></defs><rect width="780" height="1688" fill="rgb(6,16,38)" fill-opacity="${0.55*a}" mask="url(#mk)"/>`;}
function ring(x,y,k){if(k<0||k>1)return '';const r=40+60*eo(k);return `<div class="ring" style="left:${x-r}px;top:${y-r}px;width:${2*r}px;height:${2*r}px;opacity:${1-k}"></div>`;}
// ---------- logo tickers ----------
function mkTick(host,logos,rows,y0,dy,off){for(let r=0;r<rows;r++){const t=document.createElement('div');t.className='tick';t.style.top=(y0+r*dy)+'px';const row=document.createElement('div');row.className='row';
  const n=Math.ceil(logos.length/rows);let L=logos.filter((u,i)=>(i+off)%rows===r);while(L.length<7)L=L.concat(L);const seq=L.concat(L).concat(L);seq.forEach(u=>{const c=document.createElement('div');c.className='chip';c.innerHTML=`<img src="${u}">`;row.appendChild(c);});
  t.appendChild(row);t.dataset.dir=r%2?1:-1;host.appendChild(t);}}
mkTick($('ticks'),C.PLOGOS,11,-20,178,0); mkTick($('eticks'),C.ELOGOS,6,1090,138,1); [...$('eticks').querySelectorAll('.chip')].forEach(c=>{c.style.width='190px';c.style.height='120px';}); [...$('eticks').querySelectorAll('.chip img')].forEach(i=>{i.style.maxWidth='172px';i.style.maxHeight='104px';}); [...$('eticks').children].forEach(t=>t.style.height='120px');
function ticks(host,t,a,sp){[...host.children].forEach((e,i)=>{const d=+e.dataset.dir;const w=e.firstChild.scrollWidth/3;const x=((t*sp*(1+0.15*i))%w);e.firstChild.style.transform=`translateX(${d<0?-x-w*0.2:x-w}px)`;e.style.opacity=a;});}
// ---------- cards ----------
const SC=[['open',0,2.8],['wm',2.8,8.0],['wt',8.0,11.2],['wb',11.2,14.8],['intro',14.8,17.2],['tiles',17.2,20.0],['ctx',20.0,21.6],['tap',21.6,23.6],['swipe',23.6,30.0],['fav',30.0,32.4],['racks',32.4,36.4],['card',36.4,38.4],['xw',38.4,40.0],['end',40.0,42.8]];
const DIV={open:'open',wm:'wall',wt:'wall',wb:'wall',intro:'app',tiles:'app',ctx:'app',tap:'app',swipe:'app',fav:'app',racks:'app',card:'cardsc',xw:'wall',end:'end'};
window.render=function(t){let cur=SC[SC.length-1];for(const s of SC)if(t>=s[1]&&t<s[2]){cur=s;break;}
 const [id,a]=cur,L=t-a;for(const d of ['open','wall','app','cardsc','end'])$(d).style.display=DIV[id]===d?'block':'none';
 snow(t,1,DIV[id]==='app'?5:45); plate('',0); $('ov').innerHTML=''; $('intro').innerHTML=''; spot([],0); $('words').innerHTML='';
 if(id==='open')opener(L);
 if(id==='wm'){wall('m',L);counter(140,true,'holiday mats',L-0.5,2.6);if(L<0.5)$('cnt').style.opacity=0;words(L-3.0);$('veil').style.opacity=0;}
 if(id==='wt'){wall('t',L);counter(14,false,'holiday tile sets',L-0.4);if(L<0.4)$('cnt').style.opacity=0;$('veil').style.opacity=0;
  const ch=WL.t.g.children;WL.t.ord.forEach((ci,j)=>{const d=ch[ci];const im=d.firstChild;const cv=C.TCOV[ci];const q=(L-1.7-j*0.05)/0.24; // flip each tile photo to its holiday album cover
   if(!cv){return;} if(q<0.5){if(im.dataset.c==='1'){im.src=C.TWALL[ci];im.dataset.c='0';}}else{if(im.dataset.c!=='1'){im.src=cv;im.dataset.c='1';}}
   if(q>0&&q<1)d.style.transform=`scaleX(${Math.abs(Math.cos(Math.PI*q))})`;});}
 $('ticks').style.display=id==='wb'?'block':'none';
 if(id==='xw'){wall('x',L);$('cnt').style.opacity=0;$('veil').style.opacity=0;} // cross-brand Find Your Mat-ch match cards tile out
 if(id==='wb'){for(const k in WL)WL[k].g.style.display='none';ticks($('ticks'),L,cl(L/0.3),210);$('cnt').style.top='708px';counter(50,true,'brands',L-0.1);}else if(id==='wt'){$('cnt').style.top='708px';}else{$('cnt').style.top='';}
 if(id==='intro'){ // phone flies in; app home screen
  frame(C.R0,C.T0,0.6); camK(PK,-90,470+(1-eo(L/0.6))*1400,540);
  const q=cl((L-0.15)/0.3);
  $('intro').style.top='250px';$('intro').innerHTML=`<div style="display:inline-block;background:#fff;border-radius:34px;box-shadow:0 14px 36px rgba(30,70,120,.28);padding:18px 40px 22px;transform:scale(${0.86+0.14*eb(q)});opacity:${cl(q*4)}"><div style="font:400 60px/1.12 Cap;color:var(--navy)">Mix and match them all,<br>plus the tiles you own, in</div><div style="margin-top:8px;font:400 78px/1.05 Cap;color:var(--navy);white-space:nowrap">Find <span style="font:italic 600 82px/1 PF;color:var(--red)">Your</span> Mat-ch&trade;</div></div>`;}
 if(id==='tiles'){ // tiles step: tap Holiday (tile colours) -> holiday sets -> tap Dear Santa
  frame(C.R0,C.T0,pw([[0,1.2],[0.4,1.9],[0.8,3.1],[1.1,3.7],[1.5,4.6],[1.9,6.9],[2.3,7.82],[2.8,8.35]],L));
  cam([[0,...FULL],[0.5,...FULL],[0.95,1.3,250,860],[1.6,1.3,240,860],[2.05,1.2,200,800],[2.8,1.05,300,760]],L,t);
  if(L>0.7&&L<1.9){spot([[97,830,187,89,40]],cl((L-0.7)/0.2));$('ov').innerHTML=ring(190,874,(L-1.05)/0.45);}
  if(L>=1.9){spot([[14,650,253,336,26]],cl((L-1.9)/0.2));$('ov').innerHTML=ring(140,818,(L-2.25)/0.45);}
  if(L<0.6)plate('Start with your tiles',L-0.05,330);}
 if(id==='ctx'){frame(C.RA,C.TA,pw([[0,0.3],[1.6,1.5]],L)); cam([[0,1.0,390,700],[0.3,...FULL],[1.6,.78,390,560]],L,t); spot([[14,100,752,1290,30]],cl(L/0.25)); if(L>0.2)plate('Pick your mat',L-0.25,330);}
 if(id==='tap'){frame(C.RA,C.TA,pw([[0,1.5],[0.7,2.7],[1.05,3.26],[1.1,3.3],[2.0,4.0]],L)); const q=eio((L-0.55)/0.5); // phone in context, then push in on the Holiday chip as it's tapped
  cam([[0,.78,390,560],[0.45,.78,390,560],[1.0,1.45,330,1060],[2.0,1.38,360,1020]],L,t);
  spot([[236,1022,183,98,40]],cl((L-0.6)/0.3)); $('ov').innerHTML=ring(327,1071,(L-1.05)/0.5)+ring(327,1071,(L-1.2)/0.5);
  if(L<0.5)plate('Tap Holiday',L-0.05,330);}
 if(id==='swipe'){frame(C.RA,C.TA,pw([[0,5.0],[0.6,5.66],[1.4,6.87],[2.0,7.35],[2.8,8.4],[3.3,8.9],[4.0,9.95],[4.5,10.45],[5.1,11.6],[5.6,12.1],[6.0,13.13],[6.4,13.6]],L));
  cam([[0,1.2,390,900],[0.25,...FULL],[0.75,...FULL],[1.25,1.02,390,780],[2.2,1.08,300,800],[3.2,1.02,470,760],[4.2,1.1,330,820],[5.2,1.03,450,770],[6.4,0.96,390,760]],L,t);
  spot([[16,200,748,1252,30]],cl(L/0.2)); if(L>0.15&&L<0.8)plate('Swipe holiday mats',L-0.2,330);}
 if(id==='fav'){
  frame(C.RP,C.TP,pw([[0,0.5],[1.3,1.0],[1.5,1.66],[2.4,1.665]],L));
  cam([[0,...FULL],[0.55,...FULL],[1.05,1.08,390,900],[1.45,1.25,540,960],[2.4,1.18,500,940]],L,t); /* 'Which suitor is the one?' with all 4 hearted mats; stop before the racks screen */
  spot([[18,560,744,700,28]],cl(L/0.2)); $('ov').innerHTML=ring(598,987,(L-1.45)/0.45);
  if(L<0.6)plate('Pick your favorite',L-0.05,330);}
 if(id==='racks'){frame(C.RB,C.TB,pw([[0,2.4],[0.4,3.3],[1.0,3.85],[1.4,5.35],[2.0,5.8],[2.5,6.3],[3.1,7.8],[3.6,8.26],[4.0,8.27]],L));
  cam([[0,...FULL],[0.55,...FULL],[1.0,1.15,390,560],[1.4,1.15,390,600],[1.9,1.02,390,1150],[2.8,1.08,330,1200],[3.4,1.02,450,1180],[4.0,0.98,390,1100]],L,t);
  spot([[16,360,748,336,26],[16,1032,748,500,30]],1); if(L<0.6)plate('Add racks',L-0.05,330);}
 if(id==='card'){const im=$('mcard');if(im.dataset.u!=='c'){im.src=C.CARD;im.dataset.u='c';} $('boom').innerHTML='';
  const k=eo(L/0.5);const w=540;im.style.width=w+'px';im.style.left=(540-w/2)+'px';im.style.top=(500+(1-k)*120)+'px';im.style.opacity=cl(L/0.2);
  const z=1+0.09*eio((L-0.3)/1.7); im.style.transformOrigin='50% 50%'; im.style.transform=`scale(${(0.94+0.06*k)*z}) translateY(${-6*eio(L/2)}px)`; // v5: gentle push only, every word of the card stays in frame
  plate('See it together,<br>share it or shop it',L-0.25,250);}
  if(id==='end'){$('fh').style.transform=`scale(${eb(L/0.45)})`;$('shop').style.transform=`scale(${L<1?eb((L-0.35)/0.45):1+0.04*Math.sin(Math.PI*2*((L-1)/0.8))})`;
  ticks($('eticks'),t,cl((L-0.5)/0.3),150);}
};
</script></body></html>"""

def page():
    return (HTML.replace('__F__', FONTS).replace('__FLH__', CFG['FLH']).replace('__FL__', CFG['FL']).replace('__WMH__', CFG['WMH']).replace('__WM__', CFG['WM'])
            .replace('__CFG__', json.dumps(CFG)))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'frames'
    out = f'{W5}/out'; os.makedirs(out, exist_ok=True)
    os.makedirs(W5, exist_ok=True); open(f'{W5}/reel.html', 'w').write(page())
    FPS, DUR = 30, 42.8
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(f'file://{W5}/reel.html'); pg.wait_for_timeout(3000)
        wait = "()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})))"
        if mode == 'frames':
            fd = f'{W5}/frames'
            rng = range(int(FPS * DUR))
            if len(sys.argv) > 2:
                rng = [n for a in sys.argv[2:] for n in range(int(a.split('-')[0]), int(a.split('-')[1]) + 1)]
            else:
                if os.path.isdir(fd): shutil.rmtree(fd)
                os.makedirs(fd)
            for n in rng:
                pg.evaluate(f"render({n / FPS})"); pg.evaluate(wait)
                pg.screenshot(path=f'{fd}/{n:04d}.jpg', type='jpeg', quality=92)
        else:
            for tt in [float(x) for x in sys.argv[2:]]:
                pg.evaluate(f"render({tt})"); pg.evaluate(wait); pg.wait_for_timeout(150)
                pg.screenshot(path=f'{out}/t{tt:05.2f}.jpg', type='jpeg', quality=88)
        b.close()
