"""Holiday intro reel v3 (Nov 3 2026), per Tiffany's Nov 3 12:54pm, 1:06pm and 1:09pm notes (docs/ANSWERS.md) +
../STORYBOARD-v3.md. 42.0s = 105 beats at 150 BPM (she adds "All I Want for Christmas Is You" in Edits; 40-43s so the song
ends right). Snowy light-blue holiday look (no navy), snow the whole time, red accents. No trailing periods on step text.
Scenes: opener (flame puts on its holiday look, HOLIDAY EDITION, "It's holiday time!") -> mat wall 140+ (v1's tile-out
shot, edge to edge) + Christmas / Hanukkah / Snow days -> tile-set wall 14 -> album wall 40+ -> tool intro (phone flies in)
-> Start with your tiles -> Tap Holiday -> Swipe holiday mats -> Pick your favorite -> Add racks (opens zoomed) ->
match card "See it together, share it or shop it" -> boom of 3 more holiday match cards -> end card.
Inputs: /dev/shm/introv2/{rec0,recA,recP,recB} (v3_capture.py) + /dev/shm/introv3/{wall,tiles,alb,brand} + wall_sel.json.
Usage: python3 v3_reel.py frames [a-b ...] | stills t1 t2 ...   -> /dev/shm/introv3/{frames,out}"""
import json, os, sys, shutil, glob
W2 = '/dev/shm/introv2'; W = '/dev/shm/introv3'
os.environ['TMPDIR'] = W2 + '/tmp'
from playwright.sync_api import sync_playwright
R = '/home/claude/mahjmatchmaker-data'
FONTS = f'file://{R}/scripts/social/tileprofile/fonts'
F = lambda p: 'file://' + p
WALL = [F(r['f']) for r in json.load(open(f'{W}/wall_sel.json'))]
TORD = ['dear-santa', 'rackin-rudolph', 'hj-red', 'hj-green', 'hj-pink', 'tin-ruby', 'tin-emerald', 'niv-blue', 'nutcracker',
        'apres', 'niv-emerald', 'merry-nutcracker', 'spirit', 'dec1994']
TWALL = [F(f'{W}/tiles/{n}.jpg') for n in TORD]
TWALL = TWALL[:7] + [TWALL[0]] + TWALL[7:]          # 15 cells (3 x 5): Dear Santa shows twice, far apart
AWALL = [F(p) for p in sorted(glob.glob(f'{W}/alb/*.jpg'))]
CD = f'{R}/assets/cards/holiday-v4/'
BOOM = [F(CD + n) for n in ['nutcracker-ballet-mahjong-tiles-mahj-squad-clara-s-dream-christmas-mat.jpg',
                            'nivalee-blue-mahjong-tiles-charleston-mahjong-club-ski-club-red-sweater-mat.jpg',
                            'holly-jolly-pink-mahjong-tiles-mahjong-register-very-merry-wreath-mat.jpg']]
LOGOS = [F(f'{R}/assets/brand/partner-logos/{n}.png') for n in ['ar', 'sunday', 'virora', 'squad', 'bam', 'cmc', 'hiphip', 'lets-be-besties']]
def rt(r):
    d = json.load(open(f'{W2}/{r}/marks.json')); Fr = d['frames']; return [round(x - Fr[0], 3) for x in Fr]
CFG = dict(WALL=WALL, TWALL=TWALL, AWALL=AWALL, BOOM=BOOM, LOGOS=LOGOS, CARD=F(f'{W2}/recB/storycard.png'),
           R0=F(f'{W2}/rec0/f/'), RA=F(f'{W2}/recA/f/'), RP=F(f'{W2}/recP/f/'), RB=F(f'{W2}/recB/f/'),
           T0=rt('rec0'), TA=rt('recA'), TP=rt('recP'), TB=rt('recB'),
           FL=F(f'{W}/brand/fl.png'), FLH=F(f'{W}/brand/flh.png'), WM=F(f'{R}/assets/brand/mahjmatchmaker-wordmark-notag.png'))

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
.bez{position:absolute;left:-30px;top:-30px;width:840px;height:1748px;border-radius:118px;background:#14121a;box-shadow:0 34px 80px rgba(30,70,120,.40)}
.scr{position:absolute;left:0;top:0;width:780px;height:1688px;border-radius:92px;overflow:hidden;background:#fff}
.scr img.f{position:absolute;left:0;top:0;width:780px;height:1688px}
.ring{position:absolute;border-radius:50%;border:10px solid var(--red)}
.pill{display:inline-block;font:700 46px/1.1 Bit;padding:18px 42px;border-radius:60px;white-space:nowrap}
.spk{position:absolute;width:26px;height:26px;background:var(--gold);clip-path:polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%)}
.mc{position:absolute;border-radius:26px;box-shadow:0 34px 80px rgba(30,70,120,.40)}
</style></head><body>
<div class="snow" id="snow"></div>
<div id="open" class="sc bgn">
 <img id="wm" src="__WM__" style="position:absolute;left:260px;top:250px;width:560px">
 <div id="flw" style="position:absolute;left:420px;top:380px;width:240px;height:260px"><img id="fl" src="__FL__" style="position:absolute;inset:0;width:240px"><img id="flh" src="__FLH__" style="position:absolute;inset:0;width:240px;opacity:0"><div id="spks"></div></div>
 <div id="olk" style="position:absolute;left:0;right:0;top:690px;text-align:center"><span style="display:inline-block;font:400 104px/1 Cap;color:var(--navy);white-space:nowrap;position:relative">Find <span style="font:italic 600 108px/1 PF;color:var(--red)">Your</span> Mat-ch<span style="position:absolute;font:400 38px Bit;margin-left:4px;margin-top:4px">™</span></span></div>
 <div id="hed" style="position:absolute;left:0;right:0;top:880px;text-align:center"><span class="pill" style="background:var(--red);color:#fff;letter-spacing:8px;font-size:44px;border:5px solid var(--gold);padding:16px 46px">HOLIDAY EDITION</span></div>
 <div id="iht" style="position:absolute;left:0;right:0;top:1050px;text-align:center"><span style="display:inline-block;font:400 82px/1.05 Cap;color:var(--green);background:#fff;padding:26px 56px 38px;border-radius:40px;box-shadow:0 18px 44px rgba(30,70,120,.25);white-space:nowrap">It&rsquo;s holiday time!</span></div>
</div>
<div id="wall" class="sc bgn"><div id="wg" style="position:absolute;left:0;top:0;width:1080px"></div><div id="veil" style="position:absolute;inset:0;background:#eef6fc;opacity:0"></div>
 <div class="cnt" id="cnt"><div class="odo"><div class="grp" id="grp"></div></div><div class="olab" id="olab"></div></div><div id="words"></div></div>
<div id="app" class="sc"><div class="cam" id="cam"><div class="bez"></div><div class="scr"><img class="f" id="fr"><svg id="spot" width="780" height="1688" style="position:absolute;left:0;top:0"></svg><div id="ov" style="position:absolute;inset:0"></div></div></div>
 <div id="intro" style="position:absolute;left:0;right:0;top:250px;text-align:center;z-index:50"></div></div>
<div id="cardsc" class="sc bgn"><img id="mcard" class="mc"><div id="boom"></div></div>
<div id="end" class="sc bgn">
 <img src="__FLH__" id="fh" style="position:absolute;left:465px;top:260px;width:150px">
 <img src="__WM__" style="position:absolute;left:300px;top:440px;width:480px">
 <div style="position:absolute;left:0;right:0;top:550px;text-align:center"><span style="display:inline-block;font:400 104px/1 Cap;color:var(--navy);white-space:nowrap;position:relative">Find <span style="font:italic 600 108px/1 PF;color:var(--red)">Your</span> Mat-ch<span style="position:absolute;font:400 38px Bit;margin-left:4px;margin-top:4px">™</span></span></div>
 <div style="position:absolute;left:0;right:0;top:720px;text-align:center;font:italic 600 58px/1.28 PF;color:var(--navy)">Holiday tiles, mats &amp; racks<br>across brands, together</div>
 <div style="position:absolute;left:0;right:0;top:930px;text-align:center"><span class="pill" id="shop" style="background:var(--red);color:#fff;font-size:48px">Shop now · use code MAHJMATCH</span></div>
 <div style="position:absolute;left:0;right:0;top:1080px;text-align:center"><span class="pill" style="background:#fff;border:4px solid var(--green);color:var(--green);font-size:34px;letter-spacing:4px;text-transform:uppercase;padding:14px 36px">Link in bio</span></div>
 <div id="logos" style="position:absolute;left:80px;right:80px;top:1210px;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:26px 40px"></div>
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
 const a=eb(L/0.4); $('wm').style.opacity=cl(L/0.25); $('wm').style.transform=`translateY(${(1-eo(L/0.4))*-30}px)`;
 $('olk').style.opacity=cl(L/0.2); $('olk').style.transform=`scale(${0.7+0.3*a})`;
 const k=(L-0.8)/0.35; // flame puts on its holiday look
 $('fl').style.opacity=1-cl(k); $('flh').style.opacity=cl(k);
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
mkwall('a',C.AWALL,5,216,270,0);
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
function camK(k,fy,py,x){$('cam').style.transform=`translate(${540*0.12}px,110px) scale(0.88) translate(${(x==null?540:x)-390*k}px,${py-fy*k}px) scale(${k})`;}
function spot(holes,a){$('spot').innerHTML=a<=0?'':`<defs><filter id="bl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="16"/></filter><mask id="mk"><rect width="780" height="1688" fill="#fff"/>${holes.map(([x,y,w,h,r])=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r||22}" fill="#000" filter="url(#bl)"/>`).join('')}</mask></defs><rect width="780" height="1688" fill="rgb(6,16,38)" fill-opacity="${0.55*a}" mask="url(#mk)"/>`;}
function ring(x,y,k){if(k<0||k>1)return '';const r=40+60*eo(k);return `<div class="ring" style="left:${x-r}px;top:${y-r}px;width:${2*r}px;height:${2*r}px;opacity:${1-k}"></div>`;}
// ---------- cards ----------
C.LOGOS.forEach(u=>{const i=document.createElement('img');i.src=u;i.style.height='110px';i.style.maxWidth='230px';i.style.objectFit='contain';$('logos').appendChild(i);});
const SC=[['open',0,2.8],['wm',2.8,8.0],['wt',8.0,11.6],['wa',11.6,15.2],['intro',15.2,17.6],['tiles',17.6,20.4],['tap',20.4,22.8],['swipe',22.8,28.4],['fav',28.4,31.2],['racks',31.2,35.6],['card',35.6,38.0],['boom',38.0,39.2],['end',39.2,42.0]];
const DIV={open:'open',wm:'wall',wt:'wall',wa:'wall',intro:'app',tiles:'app',tap:'app',swipe:'app',fav:'app',racks:'app',card:'cardsc',boom:'cardsc',end:'end'};
window.render=function(t){let cur=SC[SC.length-1];for(const s of SC)if(t>=s[1]&&t<s[2]){cur=s;break;}
 const [id,a]=cur,L=t-a;for(const d of ['open','wall','app','cardsc','end'])$(d).style.display=DIV[id]===d?'block':'none';
 snow(t,1,DIV[id]==='app'?5:45); plate('',0); $('ov').innerHTML=''; $('intro').innerHTML=''; spot([],0); $('words').innerHTML='';
 if(id==='open')opener(L);
 if(id==='wm'){wall('m',L);counter(140,true,'holiday mats',L-0.5,2.6);if(L<0.5)$('cnt').style.opacity=0;words(L-3.0);$('veil').style.opacity=0;}
 if(id==='wt'){wall('t',L);counter(14,false,'holiday tile sets',L-0.4);if(L<0.4)$('cnt').style.opacity=0;$('veil').style.opacity=0;}
 if(id==='wa'){wall('a',L);$('wg').style.transform=`translateY(${-510*eio((L-0.6)/2.8)}px)`;counter(40,true,'holiday albums',L-0.4);if(L<0.4)$('cnt').style.opacity=0;$('veil').style.opacity=0;}
 if(id!=='wa')$('wg').style.transform='';
 if(id==='intro'){ // phone flies in; app home screen
  frame(C.R0,C.T0,0.6); const k=0.8*(0.9+0.1*eo(L/0.6)); camK(k,0,560+(1-eo(L/0.6))*1300,540);
  const q=cl((L-0.15)/0.3);
  $('intro').innerHTML=`<div style="display:inline-block;background:#fff;border-radius:34px;box-shadow:0 14px 36px rgba(30,70,120,.28);padding:22px 46px 28px;transform:scale(${0.86+0.14*eb(q)});opacity:${cl(q*4)}"><div style="font:400 60px/1.12 Cap;color:var(--navy)">Mix and match them all,<br>plus the tiles you own, in</div><div style="margin-top:8px;font:400 78px/1.05 Cap;color:var(--navy);white-space:nowrap">Find <span style="font:italic 600 82px/1 PF;color:var(--red)">Your</span> Mat-ch&trade;</div></div>`;}
 if(id==='tiles'){ // tiles step: tap Holiday (tile colours) -> holiday sets -> tap Dear Santa
  frame(C.R0,C.T0,pw([[0,1.2],[0.4,1.9],[0.8,3.1],[1.1,3.7],[1.5,4.6],[1.9,6.9],[2.3,7.82],[2.8,8.35]],L));
  camK(0.82+0.1*eio((L-0.2)/0.6),900,1060);
  if(L>0.7&&L<1.9){spot([[97,830,187,89,40]],cl((L-0.7)/0.2));$('ov').innerHTML=ring(190,874,(L-1.05)/0.45);}
  if(L>=1.9){spot([[14,650,253,336,26]],cl((L-1.9)/0.2));$('ov').innerHTML=ring(140,818,(L-2.25)/0.45);}
  plate('Start with your tiles',L-0.05);}
 if(id==='tap'){frame(C.RA,C.TA,pw([[0,0.3],[0.8,1.24],[0.85,1.3],[2.4,2.6]],L)); const s=1.0+0.55*eio(L/0.55); camK(1.1436*s,1071,1010);
  spot([[236,1022,183,98,40]],cl(L/0.3)); $('ov').innerHTML=ring(327,1071,(L-0.8)/0.5)+ring(327,1071,(L-0.95)/0.5);
  plate('Tap Holiday',L-0.05);}
 if(id==='swipe'){frame(C.RA,C.TA,pw([[0,4.84],[0.9,4.87],[1.6,5.36],[2.6,6.36],[2.65,6.43],[3.35,6.93],[4.4,7.93],[4.45,7.99],[5.2,8.5],[5.6,8.6]],L)); camK(1.052,0,350);
  spot([[18,200,744,1252,30]],1); plate('Swipe holiday mats',L-0.05);}
 if(id==='fav'){
  if(L<1.0){frame(C.RA,C.TA,10.25); camK(1.0,1030,1010); spot([[16,1030,748,174,26]],cl(L/0.2));}
  else{const u=L-1.0; frame(C.RP,C.TP,pw([[0,0.9],[0.75,1.62],[1.0,1.665],[1.8,1.665]],u));  /* stop before the racks screen (its default first rack is Persimmon) */ camK(1.05,1180,1010);
   spot([[30,960,720,440,26]],1); $('ov').innerHTML=ring(286,1238,(u-0.72)/0.45);}
  plate('Pick your favorite',L-0.05);}
 if(id==='racks'){frame(C.RB,C.TB,pw([[0,2.4],[0.5,3.3],[1.1,3.85],[1.5,5.4],[2.1,5.82],[2.6,6.3],[3.3,7.85],[3.8,8.3],[4.4,8.32]],L)); camK(0.82,0,340);
  spot([[16,360,748,336,26],[16,1032,748,856,30]],1); plate('Add racks',L-0.05);}
 if(id==='card'){const im=$('mcard');if(im.dataset.u!=='c'){im.src=C.CARD;im.dataset.u='c';} $('boom').innerHTML='';
  const k=eo(L/0.6);const w=560;im.style.width=w+'px';im.style.left=(540-w/2)+'px';im.style.top=(450+(1-k)*120)+'px';im.style.opacity=cl(L/0.2);im.style.transform=`scale(${0.92+0.08*k})`;
  plate('See it together,<br>share it or shop it',L-0.25,250);}
 if(id==='boom'){const im=$('mcard');const i=Math.min(2,Math.floor(L/0.4));const u='b'+i;if(im.dataset.u!==u){im.src=C.BOOM[i];im.dataset.u=u;}
  const q=(L-i*0.4)/0.25;const w=700;im.style.width=w+'px';im.style.left=(540-w/2)+'px';im.style.top='420px';im.style.opacity=1;im.style.transform=`scale(${0.8+0.2*eb(q)}) rotate(${[-3,2,-2][i]*(1-cl(q))}deg)`;
  plate('Holiday match cards',0.4);}
 if(id==='end'){$('fh').style.transform=`scale(${eb(L/0.45)})`;$('shop').style.transform=`scale(${L<1?eb((L-0.35)/0.45):1+0.04*Math.sin(Math.PI*2*((L-1)/0.8))})`;
  [...$('logos').children].forEach((e,i)=>{e.style.opacity=cl((L-0.6-i*0.06)/0.2);});}
};
</script></body></html>"""

def page():
    return (HTML.replace('__F__', FONTS).replace('__FLH__', CFG['FLH']).replace('__FL__', CFG['FL']).replace('__WM__', CFG['WM'])
            .replace('__CFG__', json.dumps(CFG)))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'frames'
    out = f'{W}/out'; os.makedirs(out, exist_ok=True)
    open(f'{W}/reel.html', 'w').write(page())
    FPS, DUR = 30, 42.0
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(f'file://{W}/reel.html'); pg.wait_for_timeout(3000)
        wait = "()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})))"
        if mode == 'frames':
            fd = f'{W}/frames'
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
