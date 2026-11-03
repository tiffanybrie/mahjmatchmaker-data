"""Holiday intro reel v2 (Nov 2 2026), per Tiffany's Nov 1 6:09pm + Nov 2 9:23am notes (docs/ANSWERS.md):
slow only the tutorial (app) parts, one short centred text plate at a time, spotlight (dim the rest) on app moments,
9:16 layouts with real margins, Color Me Merry (Soiree All Day) as the hero, centred counters, no dating language,
end line says ACROSS BRANDS. Music: she adds Mariah "All I Want for Christmas Is You" in Edits (150 BPM, beat = 0.4s);
scene cuts sit on the 0.4s grid, 75 beats = 30.0s.
Inputs (rebuild with v2_stock.py + v2_capture.py): /dev/shm/introv2/{mats/map.json, recA, recB, recB/storycard.png}
Usage: python3 v2_reel.py frames | stills t1 t2 ...   -> /dev/shm/introv2/{frames,out}"""
import json, os, sys, shutil
W = '/dev/shm/introv2'
os.environ['TMPDIR'] = W + '/tmp'
from playwright.sync_api import sync_playwright
R = '/home/claude/mahjmatchmaker-data'
FONTS = f'file://{R}/scripts/social/tileprofile/fonts'
MAP = json.load(open(f'{W}/mats/map.json'))
BYN = {}
for k, (fn, n, bn, *_) in MAP.items(): BYN.setdefault(n, []).append((fn, bn))
def mat(n, bn=None):
    c = [f for f, b in BYN[n] if bn is None or b == bn]
    return 'file://' + c[0]
CMM = f'file://{W}/cmm-trim.jpg'  # assets/mats/soiree-all-day/color-me-merry-mahjong-mat.jpg, white margin trimmed (convert -fuzz 6% -trim)
# hook grid 3 x 4 (Color Me Merry at row 2, col 2 so it can fly to the hero spot); her holiday picks (also_year_round) mixed in
HOOK = [mat('Candy Cane Lane', 'Anders Ruff'), mat('Very Merry Wreath Premium'), mat('Tartan Tidings'),
        mat('Merry Mix'), CMM, mat('Festive Plaid Premium'),
        mat('Snowflake Lodge Premium'), mat('Peppermint Patty Premium'), mat('Merriment'),
        mat('The Ornamental'), mat('Merry & Striped'), mat('Christmas Ribbon Rhapsody')]
QUILT = [mat(n, b) for n, b in [('Santa\'s Mahjong Mail', None), ('Winterberry', None), ('Hip Hip Hanukkah', None), ('Clara\'s Dream Christmas', None),
         ('Plaid Tidings', None), ('Candy Cane Lane', 'Peace Love Mahjong'), ('Peppermint Wishes', None), ('Yuletide', None),
         ('Love & Light', None), ('Holly Jolly Christmas', 'Mahjong Register'), ('Evergreen & Tartan', None), ('Alpine Snowflakes', None),
         ('Merry & Bright, Holiday Prism', None), ('Candy Cane Christmas Village', None), ('Buffalo Plaid Snow Day', None), ('Festive Frost', None),
         ('Classic Very Merry Mahj', None), ('Holly Jolly Gingham', None), ('Vintage Noel', 'Peace Love Mahjong'), ('Holiday Neoprene', None)]]
T = f'file://{R}/assets/tiles/holiday/'
CV = f'file://{R}/assets/covers/holiday/'
COUNTS = [  # canonical, ../../COUNTS.md + ANSWERS Nov 1 6:00pm (14 holiday tile sets)
    dict(n=140, plus=True, lab='holiday mats', th=[mat('Very Merry Mahj'), mat("Santa's Mahjong Mail"), mat('Merry & Striped')]),
    dict(n=14, plus=False, lab='holiday tile sets', th=[T + 'dear-santa.jpg', T + 'holly-jolly-pink-pile.jpg', T + 'nivalee-blue.jpg']),
    dict(n=40, plus=True, lab='holiday albums', th=[CV + 'dear-santa.jpg', CV + 'nutcracker-ballet.jpg', CV + 'cmc-apres-ski.jpg']),
]
def rect_times(r):
    d = json.load(open(f'{W}/{r}/marks.json')); F = d['frames']; return [round(x - F[0], 3) for x in F]
CFG = dict(HOOK=HOOK, QUILT=QUILT, COUNTS=COUNTS, CMM=CMM, CARD=f'file://{W}/recB/storycard.png',
           RA=f'file://{W}/recA/f/', RB=f'file://{W}/recB/f/', TA=rect_times('recA'), TB=rect_times('recB'),
           FH=f'file://{R}/assets/brand/flame-heart-holiday.png')

HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Cap;src:url(__F__/Caprasimo.ttf)}
@font-face{font-family:Bit;src:url(__F__/bitter-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:Bit;src:url(__F__/bitter-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:PF;src:url(__F__/playfair-display-latin-600-italic.woff2);font-style:italic}
:root{--navy:#062a55;--deep:#041d3d;--red:#b3202a;--gold:#e9c77b;--pink:#f56c8c;--rose:#d6336c;--cream:#faf3ea}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;position:relative;background:#e4f0f9;font-family:Bit}
.sc{position:absolute;inset:0;display:none;overflow:hidden}
/* Nov 3 (Tiffany): not navy for holiday; a very light snowy blue */
.bgn{background:radial-gradient(ellipse at 50% 42%,#ffffff 0%,#eef6fc 38%,#d9eaf6 75%,#c6ddef 100%)}
.snow{position:absolute;inset:0;pointer-events:none}.snow i{position:absolute;border-radius:50%;background:#fff;box-shadow:0 0 0 1.5px rgba(120,165,205,.55),0 2px 6px rgba(70,120,170,.35)}
.plate{position:absolute;left:0;right:0;text-align:center;z-index:40}
.plate span{display:inline-block;font:400 78px/1.06 Cap;color:var(--navy);background:#fff;padding:24px 50px 32px;border-radius:32px;box-shadow:0 14px 36px rgba(30,70,120,.28);white-space:nowrap}
.card{position:absolute;border-radius:22px;overflow:hidden;background:#fff;box-shadow:0 14px 34px rgba(30,70,120,.30);border:8px solid #fff}
.card img{width:100%;height:100%;object-fit:cover;display:block;border-radius:12px}
.pill{display:inline-block;font:700 40px/1.1 Bit;padding:18px 40px;border-radius:60px;white-space:nowrap}
.pill small{font:600 34px Bit;opacity:.9}
/* odometer: digits centred as a group; the + hangs outside the group so it never shifts the number */
.odo{position:absolute;left:0;right:0;top:470px;height:330px;display:flex;justify-content:center}
.grp{position:relative;display:flex;gap:10px}
.dg{width:210px;height:320px;overflow:hidden;position:relative;background:rgba(4,29,61,.9);border-radius:28px;border:6px solid var(--gold);box-shadow:0 18px 40px rgba(30,70,120,.35)}
.dg .st{position:absolute;left:0;right:0;top:0}
.dg .st div{height:308px;font:400 262px/308px Cap;color:var(--cream);text-align:center}
.dg:after{content:"";position:absolute;inset:0;background:linear-gradient(rgba(0,0,0,.35),transparent 22%,transparent 78%,rgba(0,0,0,.35))}
.plus{position:absolute;left:100%;top:-10px;margin-left:14px;font:400 190px/1 Cap;color:var(--red)}
.olab{position:absolute;left:0;right:0;top:850px;text-align:center;font:400 104px/1.05 Cap;color:var(--navy)}
/* phone */
.cam{position:absolute;left:0;top:0;transform-origin:0 0}
.bez{position:absolute;left:-30px;top:-30px;width:840px;height:1748px;border-radius:118px;background:#14121a;box-shadow:0 34px 80px rgba(30,70,120,.40)}
.scr{position:absolute;left:0;top:0;width:780px;height:1688px;border-radius:92px;overflow:hidden;background:#fff}
.scr img.f{position:absolute;left:0;top:0;width:780px;height:1688px}
.ring{position:absolute;border-radius:50%;border:10px solid var(--pink)}
</style></head><body>
<div class="snow" id="snow" style="z-index:30"></div>
<div id="hook" class="sc bgn"><div id="grid"></div></div>
<div id="cnt" class="sc bgn"><div class="odo"><div class="grp" id="grp"></div></div><div class="olab" id="olab"></div><div id="thumbs"></div></div>
<div id="app" class="sc bgn"><div class="cam" id="cam"><div class="bez"></div><div class="scr"><img class="f" id="fr"><svg id="spot" width="780" height="1688" style="position:absolute;left:0;top:0"></svg><div id="ov" style="position:absolute;inset:0"></div></div></div></div>
<div id="cardsc" class="sc bgn"><img id="mcard" style="position:absolute;border-radius:28px;box-shadow:0 34px 80px rgba(30,70,120,.40)"></div>
<div id="quilt" class="sc bgn"><div id="qg"></div></div>
<div id="end" class="sc bgn">
 <img src="__FH__" id="fh" style="position:absolute;left:470px;top:470px;width:140px">
 <div style="position:absolute;left:0;right:0;top:650px;text-align:center"><span id="lock" style="display:inline-block;font:400 112px/1 Cap;color:var(--navy);white-space:nowrap">Find <span style="font:italic 600 116px/1 PF;color:var(--rose)">Your</span> Mat-ch<span style="position:absolute;font:400 40px Bit;margin-left:4px;margin-top:6px">™</span></span></div>
 <div style="position:absolute;left:0;right:0;top:840px;text-align:center;font:italic 600 56px/1.28 PF;color:var(--navy)">Holiday tiles, mats &amp; racks<br>across brands, together.</div>
 <div style="position:absolute;left:0;right:0;top:1060px;text-align:center"><span class="pill" id="shop" style="background:var(--pink);color:#fff;font-size:46px">Shop now · use code MAHJMATCH</span></div>
 <div style="position:absolute;left:0;right:0;top:1220px;text-align:center"><span class="pill" style="background:transparent;border:4px solid var(--red);color:var(--red);font-size:34px;letter-spacing:4px;text-transform:uppercase;padding:14px 36px">Link in bio</span></div>
</div>
<div class="plate" id="plate"><span id="plt"></span></div>
<div id="lbl" style="position:absolute;left:0;right:0;text-align:center;z-index:40"></div>
<script>
const C=__CFG__;
const cl=x=>Math.min(Math.max(x,0),1), eo=x=>1-Math.pow(1-cl(x),3), eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}, eb=x=>{x=cl(x);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const $=id=>document.getElementById(id);
// snow
const SN=[];let sd=3;const rnd=()=>{sd=(sd*16807)%2147483647;return sd/2147483647};
for(let i=0;i<70;i++){const e=document.createElement('i');const s=4+rnd()*10;e.style.width=e.style.height=s+'px';e.style.opacity=.25+rnd()*.45;$('snow').appendChild(e);SN.push([e,rnd()*1080,rnd()*1920,40+rnd()*80,rnd()*6]);}
function snow(t,on){$('snow').style.display=on?'block':'none';if(!on)return;for(const [e,x,y,v,p] of SN){e.style.left=(x+Math.sin(t*1.3+p)*30)+'px';e.style.top=((y+t*v)%1960-20)+'px';}}
// plate: one centred text at a time
function plate(txt,k,y){const p=$('plate');if(!txt){p.style.display='none';return;}p.style.display='block';p.style.top=(y||270)+'px';
 if($('plt').innerHTML!==txt)$('plt').innerHTML=txt;$('plt').style.transform=`scale(${0.86+0.14*eb(k/0.3)})`;p.style.opacity=cl(k/0.12);}
function label(html,k,y){const l=$('lbl');if(!html){l.innerHTML='';return;}l.style.top=y+'px';l.innerHTML=`<span class="pill" style="background:var(--rose);color:#fff;transform:translateY(${(1-eo(k/0.35))*30}px);opacity:${cl(k/0.2)}">${html}</span>`;}
// hook grid: 3 cols x 4 rows, 80px side margins, 30px gutters
const GX=80,GY=420,CW=287,GUT=30;
C.HOOK.forEach((u,i)=>{const d=document.createElement('div');d.className='card';d.innerHTML=`<img src="${u}">`;$('grid').appendChild(d);});
function hook(L){ // L = seconds into the hook+hero span (0..4.0)
 [...$('grid').children].forEach((d,i)=>{const c=i%3,r=Math.floor(i/3);let x=GX+c*(CW+GUT),y=GY+r*(CW+GUT),w=CW,o=1,s=eb((L+0.3-i*0.075)/0.32);
  d.style.left=x+'px';d.style.top=y+'px';d.style.width=d.style.height=w+'px';d.style.opacity=L+0.3<i*0.075?0:o;d.style.transform=`scale(${s})`;d.style.zIndex=1;});
 /* Nov 3 (Tiffany): no 'Our holiday favorite.' hero, it's an overview. The full grid holds with a slow push-in. */
 $('grid').style.transformOrigin='540px 1000px';$('grid').style.transform=`scale(${1+0.07*eio((L-1.2)/3.2)})`;
 plate('It&rsquo;s holiday time.',L+0.3);label('',0);
}
// counters
function buildOdo(D){const g=$('grp');if(g.dataset.n==String(D.n))return;g.dataset.n=String(D.n);g.innerHTML='';for(const ch of String(D.n)){const d=document.createElement('div');d.className='dg';const st=document.createElement('div');st.className='st';for(let r=0;r<4;r++)for(let k=0;k<10;k++){const x=document.createElement('div');x.textContent=k;st.appendChild(x);}d.appendChild(st);g.appendChild(d);}
 if(D.plus){const p=document.createElement('div');p.className='plus';p.id='pl';p.textContent='+';g.appendChild(p);}
 $('olab').textContent=D.lab;$('thumbs').innerHTML=D.th.map((u,i)=>`<div class="card th" style="left:${90+i*310}px;top:1110px;width:280px;height:280px"><img src="${u}"></div>`).join('');}
function counter(i,L){const D=C.COUNTS[i];buildOdo(D);const s=String(D.n);const p=eo(L/0.75);
 [...$('grp').querySelectorAll('.dg')].forEach((d,j)=>{const tot=(2+j)*10+(+s[j]);d.firstChild.style.transform=`translateY(${-((tot*p)%40)*308+6}px)`;});
 const pl=$('pl');if(pl){pl.style.opacity=cl((L-0.75)/0.12);pl.style.transform=`scale(${0.6+0.4*eb((L-0.75)/0.3)})`;}
 $('grp').style.transform=`scale(${1+0.06*Math.sin(Math.PI*cl((L-0.72)/0.3))})`;
 $('olab').style.opacity=cl((L-0.35)/0.2);$('olab').style.transform=`translateY(${(1-eo((L-0.35)/0.35))*36}px)`;
 [...$('thumbs').children].forEach((d,j)=>{const k=(L-0.5-j*0.1)/0.35;d.style.opacity=cl(k*3);d.style.transform=`scale(${0.7+0.3*eb(k)}) rotate(${[-3,0,3][j]*cl(k)}deg)`;});}
// app recordings
function fidx(T,t){let lo=0,hi=T.length-1;if(t<=T[0])return 0;while(lo<hi){const m=(lo+hi+1)>>1;if(T[m]<=t)lo=m;else hi=m-1;}return lo;}
function pw(P,L){if(L<=P[0][0])return P[0][1];for(let i=1;i<P.length;i++){if(L<=P[i][0]){const [a,x]=P[i-1],[b,y]=P[i];return x+(y-x)*(L-a)/(b-a);}}return P[P.length-1][1];}
function frame(base,T,rt){const i=fidx(T,rt);const u=base+String(i).padStart(5,'0')+'.jpg';const f=$('fr');if(f.dataset.u!==u){f.src=u;f.dataset.u=u;}}
const SC0=1.1436; // frame px -> page px at camera scale 1 (screen 892px wide)
function cam(s,fy,py){const k=SC0*s;$('cam').style.transform=`translate(${540-390*k}px,${py-fy*k}px) scale(${k})`;}
function spot(holes,a){ // dim the screen ~58% except soft-edged cut-outs (frame px)
 $('spot').innerHTML=`<defs><filter id="bl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="16"/></filter><mask id="mk"><rect width="780" height="1688" fill="#fff"/>${holes.map(([x,y,w,h,r])=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r||22}" fill="#000" filter="url(#bl)"/>`).join('')}</mask></defs><rect width="780" height="1688" fill="rgb(6,16,38)" fill-opacity="${0.58*a}" mask="url(#mk)"/>`;}
function ring(x,y,k){if(k<0||k>1)return '';const r=40+60*eo(k);return `<div class="ring" style="left:${x-r}px;top:${y-r}px;width:${2*r}px;height:${2*r}px;opacity:${1-k}"></div>`;}
// quilt: 4 cols x 5 rows, 90px margins, 20px gutters, centred on the frame
C.QUILT.forEach((u,i)=>{const d=document.createElement('div');d.className='card';d.style.borderWidth='6px';d.style.borderRadius='16px';const c=i%4,r=Math.floor(i/4);d.style.left=(90+c*230)+'px';d.style.top=(395+r*230)+'px';d.style.width=d.style.height='210px';d.innerHTML=`<img src="${u}">`;$('qg').appendChild(d);});
const QO=[9,10,5,6,13,14,1,2,17,18,0,3,4,7,8,11,12,15,16,19];

// scene list (seconds; cuts on the 150 BPM 0.4s grid)
const SC=[['hook',0,4.4],['c0',4.4,6.4],['c1',6.4,8.4],['c2',8.4,10.4],['tap',10.4,12.4],['swipe',12.4,16.8],['saved',16.8,18.0],['zoom',18.0,20.0],['racks',20.0,23.2],['card',23.2,25.6],['quilt',25.6,26.8],['end',26.8,30.0]];
const DIV={hook:'hook',c0:'cnt',c1:'cnt',c2:'cnt',tap:'app',swipe:'app',saved:'app',zoom:'app',racks:'app',card:'cardsc',quilt:'quilt',end:'end'};
window.render=function(t){let cur=SC[SC.length-1];for(const s of SC)if(t>=s[1]&&t<s[2]){cur=s;break;}
 const [id,a]=cur,L=t-a;for(const d of ['hook','cnt','app','cardsc','quilt','end'])$(d).style.display=DIV[id]===d?'block':'none';
 snow(t,['hook','c0','c1','c2','end'].includes(id)); plate('',0); label('',0); $('ov').innerHTML='';
 if(id==='hook')hook(L);
 if(id[0]==='c'&&id.length===2)counter(+id[1],L);
 if(id==='tap'){ // Dear Santa picked; tap the Holiday chip, hold the tapped state ~1.2s
  frame(C.RA,C.TA,pw([[0,0.3],[0.8,1.24],[0.82,1.3],[2,2.4]],L)); const s=1.0+0.55*eio(L/0.55); cam(s,1071,1010);
  spot([[236,1022,183,98,40]],cl(L/0.3)); $('ov').innerHTML=ring(327,1071,(L-0.8)/0.5)+ring(327,1071,(L-0.95)/0.5);
  plate('Pick tiles. Tap Holiday.',L-0.05);}
 if(id==='swipe'){ // phone fixed for every swipe; flights slowed ~1.5x, ~0.8s holds between
  frame(C.RA,C.TA,pw([[0,4.84],[0.7,4.87],[1.4,5.36],[2.2,6.36],[2.25,6.43],[2.95,6.93],[3.6,7.93],[3.65,7.99],[4.4,8.5]],L)); cam(0.92,825,1092);
  spot([[18,200,744,1252,30]],1); plate('Swipe holiday mats.',L-0.05);}
 if(id==='saved'){ frame(C.RA,C.TA,10.2); cam(1.0+0.1*eio(L/0.5),1117,1010);
  spot([[16,1030,748,174,26]],cl(L/0.25)); plate('Your favorites, saved.',L-0.05);}
 if(id==='zoom'){ frame(C.RB,C.TB,pw([[0,0.95],[1.55,3.0],[2,3.4]],L)); cam(1.0+0.22*eio(L/0.45),528,960);
  spot([[16,360,748,336,26]],cl(L/0.25)); $('ov').innerHTML=[0.08,0.84,1.6].map(t0=>ring(706,416,(L-t0)/0.45)).join('');
  plate('Zoom in on your mat.',L-0.05);}
 if(id==='racks'){ frame(C.RB,C.TB,pw([[0,4.45],[0.5,4.88],[1.15,5.4],[1.15,6.95],[1.55,7.36],[2.2,7.88],[2.2,9.4],[2.7,9.85],[3.2,9.85]],L)); cam(0.8,1124,1092);
  spot([[16,360,748,336,26],[16,1032,748,856,30]],1); plate('Swipe racks to match.',L-0.05);}
 if(id==='card'){ const im=$('mcard');if(!im.src)im.src=C.CARD;const k=eo(L/0.6);const w=630;im.style.width=w+'px';im.style.left=(540-w/2)+'px';im.style.top=(440+(1-k)*120)+'px';im.style.opacity=cl(L/0.2);im.style.transform=`scale(${0.92+0.08*k})`;
  plate('See it together. Shop it.',L-0.25);}
 if(id==='quilt'){ const n=Math.min(20,Math.pow(2,Math.floor(L/0.15)));const ch=[...$('qg').children];
  QO.forEach((qi,j)=>{const d=ch[qi];const on=j<n;d.style.display=on?'block':'none';if(on){const born=j===0?0:(Math.floor(Math.log2(j))+1)*0.15;d.style.transform=`scale(${eb((L-born)/0.25)})`;}});}
 if(id==='end'){ $('fh').style.transform=`scale(${eb(L/0.45)})`;$('shop').style.transform=`scale(${L<1?eb((L-0.35)/0.45):1+0.04*Math.sin(Math.PI*2*((L-1)/0.8))})`;}
};
</script></body></html>"""

def page():
    return HTML.replace('__F__', FONTS).replace('__FH__', CFG['FH']).replace('__CFG__', json.dumps(CFG))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'frames'
    out = f'{W}/out'; os.makedirs(out, exist_ok=True)
    open(f'{W}/reel.html', 'w').write(page())
    FPS, DUR = 30, 30.0
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(f'file://{W}/reel.html'); pg.wait_for_timeout(2500)
        wait = "()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r})))"
        if mode == 'frames':
            fd = f'{W}/frames'
            rng = range(int(FPS * DUR))
            if len(sys.argv) > 2:  # re-render only frames a-b (inclusive), e.g. frames 0-20 504-540
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
