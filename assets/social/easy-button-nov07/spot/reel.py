# FYM promo reel: spotlight house style (FYM-REEL-RULES #39), same render pattern as holiday-nov1/intro/build/v2_reel.py
import json, os, sys, shutil
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__)); R='/home/claude/mahjmatchmaker-data'
FONTS=f'file://{R}/scripts/social/tileprofile/fonts'
M=json.load(open(D+'/rec/marks.json')); TF=[round(x-M['frames'][0],3) for x in M['frames']]
CFG=dict(RA=f'file://{D}/rec/f/',TA=TF,T0=M['frames'][0],TILES=f'file://{D}/../up/a-crown-jewels-tiles.jpg')
HTML=r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Cap;src:url(__F__/Caprasimo.ttf)}
@font-face{font-family:Bit;src:url(__F__/bitter-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:PF;src:url(__F__/playfair-display-latin-600-italic.woff2);font-style:italic}
:root{--navy:#062a55;--rose:#d6336c;--pink:#f56c8c}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;position:relative;font-family:Bit}
.sc{position:absolute;inset:0;display:none;overflow:hidden}
.bgn{background:radial-gradient(ellipse at 50% 42%,#ffffff 0%,#eef6fc 38%,#d9eaf6 75%,#c6ddef 100%)}
.plate{position:absolute;left:0;right:0;text-align:center;z-index:40}
.plate span{display:inline-block;font:400 78px/1.06 Cap;color:var(--navy);background:#fff;padding:24px 50px 32px;border-radius:32px;box-shadow:0 14px 36px rgba(30,70,120,.28);white-space:nowrap}
.cam{position:absolute;left:0;top:0;transform-origin:0 0}
.bez{position:absolute;left:-30px;top:-30px;width:840px;height:1748px;border-radius:118px;background:#f6f6f8;box-shadow:0 34px 80px rgba(30,70,120,.40),inset 0 0 0 4px #d8d8de}
.scr{position:absolute;left:0;top:0;width:780px;height:1688px;border-radius:92px;overflow:hidden;background:#fff}
.scr img.f{position:absolute;left:0;top:0;width:780px;height:1688px}
.ring{position:absolute;border-radius:50%;border:10px solid var(--pink)}
.card{position:absolute;border-radius:28px;overflow:hidden;background:#fff;box-shadow:0 24px 50px rgba(30,70,120,.32);border:10px solid #fff}
.card img{width:100%;height:100%;object-fit:cover;display:block;border-radius:16px}
.pill{display:inline-block;font:700 44px/1.1 Bit;padding:20px 44px;border-radius:60px;white-space:nowrap;background:var(--rose);color:#fff}
</style></head><body>
<div id="open" class="sc bgn"><div class="card" id="tc" style="left:190px;top:520px;width:700px;height:700px"><img src="__TILES__"></div>
 <div style="position:absolute;left:0;right:0;top:1290px;text-align:center"><span class="pill" id="op">Find their mat in Find <i style="font:italic 600 46px PF">Your</i> Mat-ch™</span></div></div>
<div id="app" class="sc bgn"><div class="cam" id="cam"><div class="bez"></div><div class="scr"><img class="f" id="fr"><svg id="spot" width="780" height="1688" style="position:absolute;left:0;top:0"></svg><div id="ov" style="position:absolute;inset:0"></div></div></div></div>
<div class="plate" id="plate"><span id="plt"></span></div>
<script>
const C=__CFG__;const $=id=>document.getElementById(id);
const cl=x=>Math.min(Math.max(x,0),1),eo=x=>1-Math.pow(1-cl(x),3),eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2},eb=x=>{x=cl(x);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
function plate(txt,k,y){const p=$('plate');if(!txt){p.style.display='none';return;}p.style.display='block';p.style.top=(y||270)+'px';if($('plt').innerHTML!==txt)$('plt').innerHTML=txt;$('plt').style.transform=`scale(${0.86+0.14*eb(k/0.3)})`;p.style.opacity=cl(k/0.12);}
function fidx(T,t){let lo=0,hi=T.length-1;if(t<=T[0])return 0;while(lo<hi){const m=(lo+hi+1)>>1;if(T[m]<=t)lo=m;else hi=m-1;}return lo;}
function pw(P,L){if(L<=P[0][0])return P[0][1];for(let i=1;i<P.length;i++){if(L<=P[i][0]){const [a,x]=P[i-1],[b,y]=P[i];return x+(y-x)*(L-a)/(b-a);}}return P[P.length-1][1];}
function frame(rt){const i=fidx(C.TA,rt);const u=C.RA+String(i).padStart(5,'0')+'.jpg';const f=$('fr');if(f.dataset.u!==u){f.src=u;f.dataset.u=u;}}
const SC0=1.1436;
function cam(s,fy,py){const k=SC0*s;$('cam').style.transform=`translate(${540-390*k}px,${py-fy*k}px) scale(${k})`;}
function spot(holes,a){$('spot').innerHTML=`<defs><filter id="bl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="16"/></filter><mask id="mk"><rect width="780" height="1688" fill="#fff"/>${holes.map(([x,y,w,h,r])=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r||22}" fill="#000" filter="url(#bl)"/>`).join('')}</mask></defs><rect width="780" height="1688" fill="rgb(6,16,38)" fill-opacity="${0.58*a}" mask="url(#mk)"/>`;}
function ring(x,y,k){if(k<0||k>1)return '';const r=40+60*eo(k);return `<div class="ring" style="left:${x-r}px;top:${y-r}px;width:${2*r}px;height:${2*r}px;opacity:${1-k}"></div>`;}
const SC=[['open',0,2.0],['tap',2.0,3.8],['swipe',3.8,12.2],['tray',12.2,14.6]];
window.render=function(t){let cur=SC[SC.length-1];for(const s of SC)if(t>=s[1]&&t<s[2]){cur=s;break;}
 const [id,a]=cur,L=t-a;$('open').style.display=id==='open'?'block':'none';$('app').style.display=id==='open'?'none':'block';plate('',0);$('ov').innerHTML='';
 if(id==='open'){$('tc').style.transform=`scale(${0.7+0.3*eb(L/0.45)}) rotate(${-3+3*eo(L/0.6)}deg)`;$('tc').style.opacity=cl(L/0.15);
   $('op').style.transform=`scale(${eb((L-0.5)/0.4)})`;plate('Own Crown Jewels?',L,300);}
 if(id==='tap'){frame(pw([[0,0.2],[1.4,1.30]],L));const s=1.0+0.5*eio(L/0.7);cam(s,843,980);
   spot([[268,652,244,384,28]],cl(L/0.3));$('ov').innerHTML=ring(390,843,(L-1.0)/0.45)+ring(390,843,(L-1.15)/0.45);plate('Pick your tiles',L,270);}
 if(id==='swipe'){frame(pw([[0,4.9],[8.4,14.3]],L));const s=0.92+0.05*Math.sin(Math.PI*cl(L/8.4));cam(s,960,1110);
   spot([[16,305,748,1260,30]],1);plate('Swipe mats  ✕  ♥',L,250);}
 if(id==='tray'){frame(pw([[0,14.6],[1.3,16.0],[2.4,18.0]],L));const s=1.0+0.18*eio(L/0.8);cam(s,1000,1060);
   spot([[16,760,748,170,26],[16,1190,748,440,26]],cl(L/0.3));plate('Your favorites, saved',L,250);}
};
</script></body></html>"""
open(D+'/reel.html','w').write(HTML.replace('__F__',FONTS).replace('__TILES__',CFG['TILES']).replace('__CFG__',json.dumps(CFG)))
mode=sys.argv[1] if len(sys.argv)>1 else 'frames'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920}); pg.goto('file://'+D+'/reel.html'); pg.wait_for_timeout(2000)
    wait="()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})))"
    if mode=='frames':
        fd=D+'/frames'; shutil.rmtree(fd,ignore_errors=True); os.makedirs(fd)
        for n in range(int(30*14.6)):
            pg.evaluate(f"render({n/30})"); pg.evaluate(wait); pg.screenshot(path=f'{fd}/{n:04d}.jpg',type='jpeg',quality=90)
    else:
        for tt in [float(x) for x in sys.argv[2:]]:
            pg.evaluate(f"render({tt})"); pg.evaluate(wait); pg.wait_for_timeout(100); pg.screenshot(path=f'{D}/t{tt:05.2f}.jpg',type='jpeg',quality=85)
    b.close()
