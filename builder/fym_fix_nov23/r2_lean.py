"""FYM round 2 LEAN design preview (Tiffany Nov 23 5:52pm). DRAFT, NOT LIVE: never point live.json at it.
Applies to a copy of the ux123 build (v123r2). Data + UI:
 data: Lily + Starling OMM mats (flat renders), Dapper 1 clean Table view photo (tv.mo, class A; her OK 5:22pm),
       Lotus Cove clean photo in EVERY view, Sadie Jane album picks as Tiffany's matches (m list), single racks (rackSrc).
 UI:   Table view first (default + first button), tiles chip "Sadie Jane v" and racks chip on the Table card
       (open the existing swap sheet on that tab), tap the top/bottom edge of the Table picture = rack sheet,
       slim X / heart on the card (the big button row + hint text hidden), version label 'Round 2 design preview (draft)'.
Usage: python3 r2_lean.py <index.html>"""
import sys, io, json, base64, re, tempfile, os
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'scripts/colors'); sys.path.insert(0, REPO + 'builder/fym_fix_oct25')
from build_accents import measure
P = sys.argv[1]; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M, TV, R = D['mats'], D['tv'], D['racks']
src = open(REPO + 'builder/fym_fix_oct25/v92_splash.py').read()
exec(src[src.index('def kmeans_sw'):src.index('tmpl = ')])
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}

def durl(im, q=82, mx=1200):
    im = im.copy(); im.thumbnail((mx, mx)); b = io.BytesIO(); im.save(b, 'WEBP', quality=q, method=5)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()

def autocrop(im, thr=242):
    import numpy as np
    a = np.asarray(im.convert('L')); m = a < thr; ys, xs = np.where(m)
    pad = 6; return im.crop((max(xs.min() - pad, 0), max(ys.min() - pad, 0), min(xs.max() + pad, im.width), min(ys.max() + pad, im.height)))

SEED = {}
# --- new OMM mats ---
ser = M['www.ohmymahjong.com/serendipity-mat-in-tube']
for key, name, img in [('www.ohmymahjong.com/lily-mat-in-tube', 'Lily', 'assets/launches/lily-mat/01-Matt_Lily_a.jpg'),
                       ('www.ohmymahjong.com/starling-mat-in-tube', 'Starling', 'assets/launches/starling-mat/01-Matt_Starling_a.jpg')]:
    if key in M: continue
    im = autocrop(Image.open(REPO + img).convert('RGB')); im.thumbnail((900, 900))
    f = 'm/9' + str(len(SEED) + 90001) + '.webp'; SEED[f] = durl(im, 84, 900)
    th = 'r2th' + name.lower(); t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'WEBP', quality=70)
    SEED['IMG:' + th] = 'data:image/webp;base64,' + base64.b64encode(bb.getvalue()).decode()
    path = tempfile.mktemp(suffix='.png'); im.save(path); sh = {}
    for fam, p in measure(path): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
    fams = [c for c, p in sorted(sh.items(), key=lambda kv: -kv[1]) if p >= 8][:4] or [max(sh, key=sh.get)]
    handle = key.split('/')[-1]
    o = dict(ser); o.update(n=name, f=f, th=th, w=im.width, h=im.height, ms=kmeans_sw(im), src='r2-nov23', add='r2-nov23',
                            u='https://ohmymahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2F' + handle,
                            u0='https://www.ohmymahjong.com/products/' + handle,
                            mf=fams, mt=list(range(len(fams))), sh=[round(sh.get(c, 0), 1) for c in fams], hol=False)
    o.pop('pre', None)
    M[key] = o; D['order'].append(key); D['tso'].append(D['tso'][D['order'].index('www.ohmymahjong.com/serendipity-mat-in-tube')])
    n = len(D['order']) - 1
    for s in D['sets']: s['rank'].append(n)
    TV['cls'][key] = 'A'; TV['pm'][key] = TV['pm'].get('www.ohmymahjong.com/serendipity-mat-in-tube')
    print('added', name, fams)

# --- Dapper 1 clean photo for Table view only ---
d1 = 'alb:cypress-forest:Dapper 1'
TV['mo'][d1] = durl(Image.open(REPO + 'assets/mats/omm-retired/tableview/dapper-1-clean.png').convert('RGB'), 84, 800)
TV['cls'][d1] = 'A'; TV['why'].pop(d1, None)

# --- Sadie Jane: her album picks become Tiffany's matches ---
spec = json.load(open(REPO + 'scripts/albumcard/specs/sadie-jane_nov21.json'))
byname = {}
for k, r in R.items(): byname.setdefault(r['n'], k)
sj = next(s for s in D['sets'] if s['slug'] == 'sadie-jane'); ml = []
for x in spec['mats']:
    k = x.get('fym')
    if k in M and not M[k].get('hid') and k not in [m[0] for m in ml]:
        ml.append([k, [byname[n] for n in x.get('mat_racks', []) if n in byname]])
sj['m'] = ml; sj['album'] = 'sadie-jane'; sj['cat'] = False; D.setdefault('ao', {})['sadie-jane'] = [k for k, _ in ml]; print('sadie jane matches', len(ml))

h = h[:i] + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + h[end:]

def rep(old, new, count=1):
    global h
    n = h.count(old); assert n == count, (n, old[:100]); h = h.replace(old, new)

# seed images (after IMG / MC exist)
seed_js = ''.join(f"IMG[{json.dumps(k[4:])}]={json.dumps(v)};" if k.startswith('IMG:') else f"MC[{json.dumps(k)}]={json.dumps(v)};" for k, v in SEED.items())
rep("const matFull=id=>", seed_js + "\nconst matFull=id=>")
# Lotus Cove clean photo everywhere
rep("const matSrc=id=>{const f=M[id].f;", "const R2MO=new Set(['www.ohmymahjong.com/lotus-cove-mat-in-tube']);const matSrc=id=>{if(R2MO.has(id)&&D.tv.mo[id])return D.tv.mo[id];const f=M[id].f;")
rep('function openP(mode,tab){', "window.R2OPEN=function(tab,sec){if(sec)CTX=sec;openP('swap',tab)};window.R2CTX=c=>ctx(c);window.R2TAB=()=>SW.tab;window.R2FACES=v=>{TV.faces=v;save();try{syncAdj()}catch(e){}pass(true)};window.R2GETFACES=()=>TV.faces;function openP(mode,tab){")
# Table view first
rep("S.mode='close';S.tilesOpen=true;", "S.mode='table';S.tilesOpen=true;")
rep('''<div class="seg mode" role="group" aria-label="View"><button type="button" data-mode="close" aria-pressed="${S.mode==='close'}">Up close</button><button type="button" data-mode="table" aria-pressed="${S.mode==='table'}">Table <b style="color:#c8325f;font-size:9px;letter-spacing:.06em">NEW</b></button>''',
    '''<div class="seg mode" role="group" aria-label="View"><button type="button" data-mode="table" aria-pressed="${S.mode==='table'}">Table</button><button type="button" data-mode="close" aria-pressed="${S.mode==='close'}">Up close</button>''')
# preview runs outside the site page: relative mc/ chunks resolve against the live base
BASE = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@ad0675e42242c3abad40cac9f539a265220e26eb/site-app/fym-v72/'
if '<base ' not in h: h = h.replace('<head>', '<head><base href="' + BASE + '">', 1)
# version label
h = re.sub(r'>Version 1\.23 layout preview[^<]*</small>', '>Round 2 design preview (draft, not live)</small>', h, count=1)
# CSS + JS
css = """<style id="r2css">
body .deck .sbx{display:flex!important;top:auto!important;bottom:10px;padding:0 10px;z-index:7}
body .deck .sbx .sb{width:40px;height:40px;font-size:18px;box-shadow:0 2px 8px rgba(0,0,0,.25)}
#s-mats>.acts:not(.pk),#s-racks>.acts:not(.pk),#s-tiles>.acts:not(.pk),.cmp~.acts:not(.pk),.swhint{display:none!important}
.r2chip{position:absolute;z-index:8;border:0;border-radius:999px;background:rgba(255,255,255,.95);box-shadow:0 2px 8px rgba(0,0,0,.22);font:700 12.5px/1 var(--body);color:#2a2036;padding:8px 12px;cursor:pointer;max-width:62%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.r2chip.t{left:10px;top:54px}
.r2yn{position:absolute;z-index:8;bottom:12px;width:40px;height:40px;border-radius:50%;border:0;background:rgba(255,255,255,.96);box-shadow:0 2px 8px rgba(0,0,0,.25);font:700 18px/1 var(--body);display:flex;align-items:center;justify-content:center;cursor:pointer}
.r2yn.no{left:10px;color:#5e5368}.r2yn.yes{right:10px;color:#c8325f}.r2chip.r{left:50%;transform:translateX(-50%);bottom:12px}

/* r2b (Tiffany 6:34pm): sheet results right under the search; filters behind one button */
.tvswapsec{display:flex;flex-direction:column}
.tvswapsec .tvtabs{order:1}.tvswapsec .tvsearch{order:2}.tvswapsec .r2fbtn{order:3}
.tvswapsec .tvact{order:4}.tvswapsec .tvgrid{order:5}.tvswapsec #tvsh{order:6}
.tvswapsec .tvbw,.tvswapsec #tvdots,.tvswapsec #tvfins,.tvswapsec #tvprices,.tvswapsec .tvtg{order:7}
.r2fbtn{align-self:flex-start;border:1px solid #ecd5df;background:#fff;border-radius:999px;padding:7px 13px;font:700 12.5px/1 var(--body);color:var(--navy,#054689);cursor:pointer}
.r2chip.f{left:10px;top:98px;font-size:11.5px;padding:7px 10px}
.r2swh{position:absolute;z-index:7;left:50%;top:50%;transform:translate(-50%,-50%);background:rgba(5,70,137,.92);color:#fff;font:700 13px/1.35 var(--body);padding:9px 14px;border-radius:12px;text-align:center;pointer-events:none;transition:opacity .4s}

/* r2c (Tiffany 6:53pm): nothing written over the table; small tap dots on the racks + tiles; one control bar under the table */
body.tvmode .r2chip,body.tvmode .scard .hb,body .tvadj{display:none!important}
.r2dot{position:absolute;z-index:8;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;border:0;padding:0;background:rgba(255,255,255,.88);box-shadow:0 0 0 2px rgba(200,50,95,.55),0 2px 8px rgba(0,0,0,.25);cursor:pointer;display:flex;align-items:center;justify-content:center}
.r2dot svg{width:15px;height:15px}
.r2dot.pulse{animation:r2p 1.6s ease-out 3}
@keyframes r2p{0%{box-shadow:0 0 0 2px rgba(200,50,95,.55),0 0 0 0 rgba(200,50,95,.45)}100%{box-shadow:0 0 0 2px rgba(200,50,95,.55),0 0 0 16px rgba(200,50,95,0)}}
body:not(.tvmode) .r2dot,body:not(.tvmode) .r2bar{display:none!important}
.r2bar{display:flex;align-items:stretch;gap:8px;margin:10px 0 4px;flex-wrap:wrap}
.r2bar .r2b{flex:1 1 0;min-width:0;display:flex;flex-direction:column;align-items:center;gap:4px;border:1.5px solid #ecd5df;background:#fff;border-radius:14px;padding:6px 4px 7px;cursor:pointer;font:700 12.5px/1 var(--body);color:var(--navy,#054689)}
.r2bar .r2b img{width:100%;height:42px;object-fit:contain;border-radius:8px}
.r2bar .r2b.on{border-color:#c8325f;box-shadow:0 0 0 2px rgba(200,50,95,.15)}
.r2fc{flex:1 0 100%;display:flex;align-items:center;justify-content:center;gap:6px;font:600 12px var(--body);color:#5a6b85}
.r2fc button{border:1px solid #ecd5df;background:#fff;border-radius:999px;padding:5px 10px;font:700 12px var(--body);color:var(--navy,#054689);cursor:pointer}
.r2fc button.on{background:#054689;color:#fff;border-color:#054689}
/* compact sheet: search + brands on one row, colours one row, price + toggles one row, pictures right after */
.tvp .tvback,.tvp .r2fbtn,.tvp #tvsh{display:none!important}
.tvp .tvswapsec{display:grid!important;grid-template-columns:repeat(12,minmax(0,1fr));gap:8px 6px;align-items:center}
.tvp .tvswapsec .tvsearch{grid-column:1/9}.tvp .tvswapsec .tvbw{grid-column:9/-1}.tvp .tvswapsec .tvbw .tvbtn{width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.tvp .tvswapsec #tvprices{grid-column:1/6}.tvp .tvswapsec .tvtg{grid-column:6/-1}
.tvp .tvswapsec .tvtabs,.tvp .tvswapsec #tvdots,.tvp .tvswapsec #tvfins,.tvp .tvswapsec .tvact,.tvp .tvswapsec .tvgrid{grid-column:1/-1}
.tvp .tvswapsec .tvbw,.tvp .tvswapsec #tvdots,.tvp .tvswapsec #tvfins,.tvp .tvswapsec #tvprices,.tvp .tvswapsec .tvtg{display:flex!important;order:0!important}
.tvp .tvswapsec>*{order:0!important;min-width:0}
.tvp .tvswapsec #tvdots,.tvp .tvswapsec #tvfins{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;padding:2px 2px 4px}
.tvp .tvswapsec #tvdots>*,.tvp .tvswapsec #tvfins>*{flex:none}
.tvp .tvswapsec .tvtg{gap:10px;font-size:12px;justify-content:flex-end;flex-wrap:nowrap}
.tvp .tvswapsec .tvsearch{width:100%!important;max-width:none!important;justify-self:stretch;box-sizing:border-box;margin:0!important;display:flex!important}.tvp .tvswapsec .tvsearch input{width:100%;min-width:0}
.tvp .tvswapsec #tvprices{gap:6px;flex-wrap:nowrap;align-items:center}.tvp .tvswapsec #tvprices select,.tvp .tvswapsec #tvprices button{max-width:118px;font-size:12px}
.tvp .tvswapsec .tvtg label{font-size:11.5px;gap:4px;white-space:nowrap;display:flex;align-items:center}.tvp .tvswapsec .tvtg .tvsw{transform:scale(.78);transform-origin:right center;margin:0 -4px 0 0}
.tvp{padding-left:max(14px,env(safe-area-inset-left));padding-right:max(14px,env(safe-area-inset-right));box-sizing:border-box;overflow-x:hidden}
body:not(.tvmode) .r2chip{display:none}
.scard.back .r2yn,.scard.tvoff .r2chip{display:none}
</style>"""
js = r"""<script id="r2js">
(function(){
 function chips(){if(!document.body.classList.contains('tvmode'))return;
  document.querySelectorAll('.scard[id^="top-"] .ph').forEach(ph=>{const card=ph.closest('.scard');if(card.classList.contains('tvoff'))return;
   const s=(typeof curSet==='function'&&curSet())||(S.set!=null?D.sets[S.set]:null);const nm=s?s.name:'Tiles';
   let t=ph.querySelector('.r2chip.t');if(!t){t=document.createElement('button');t.type='button';t.className='r2chip t';t.dataset.r2open='tiles';ph.appendChild(t)}
   if(card.classList.contains('tk'))t.remove();else t.textContent=nm+' ▾';
   let r=ph.querySelector('.r2chip.r');if(!r){r=document.createElement('button');r.type='button';r.className='r2chip r';r.dataset.r2open='racks';ph.appendChild(r)}
   let rk=null;try{const x=window.R2CTX(card);rk=x&&x.rack}catch(e){}r.textContent=(rk&&R[rk]?shortR(rk)+' racks':'Racks')+' ▾';});}
 function yn(){document.querySelectorAll('.deck .scard[id^="top-"] .ph').forEach(ph=>{const card=ph.closest('.scard');const k=card.id.slice(4);if(!['m','r','t'].includes(k))return;if(k==='m'&&(S.peek||(typeof matLocked==='function'&&matLocked())))return;
   if(!ph.querySelector('.r2yn.no'))ph.insertAdjacentHTML('beforeend','<button type="button" class="r2yn no" data-r2yn="0" aria-label="Not the one">✕</button><button type="button" class="r2yn yes" data-r2yn="1" aria-label="Love it">♥</button>')})}
 window.addEventListener('pointerdown',e=>{const b=e.target.closest&&e.target.closest('[data-r2yn]');if(!b)return;e.preventDefault();e.stopPropagation();const card=b.closest('.scard'),k=card.id.slice(4),yes=b.dataset.r2yn==='1';
   setTimeout(()=>{if(k==='m'||k==='r'){fly(k,yes)}else{const sec=card.closest('[id^="s-"]');const x=sec&&sec.querySelector(yes?'[data-tyes]':'[data-tno]');if(x)x.click()}},30)},true);
 window.addEventListener('click',e=>{if(e.target.closest&&e.target.closest('[data-r2yn]')){e.preventDefault();e.stopPropagation()}},true);

 function sheet(){const p=document.getElementById('tvpanel');if(!p||p.querySelector('.r2fbtn'))return;const sec=p.querySelector('.tvswapsec');if(!sec)return;
   const b=document.createElement('button');b.type='button';b.className='r2fbtn';b.textContent='Filters ▾';
   b.addEventListener('click',e=>{e.stopPropagation();p.classList.toggle('r2f');b.textContent=p.classList.contains('r2f')?'Hide filters ▴':'Filters ▾'});sec.appendChild(b);
   const q=p.querySelector('#tvq');if(q)q.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();q.blur();const g=p.querySelector('#tvgrid');if(g)g.scrollIntoView({block:'nearest'})}});}
 const FL={center:'Tiles: center',corner:'Tiles: corner',off:'Tiles: hidden'},NX={center:'corner',corner:'off',off:'center'};
 function faces(){if(!document.body.classList.contains('tvmode')||typeof window.R2GETFACES!=='function')return;
   document.querySelectorAll('.scard[id^="top-"] .ph').forEach(ph=>{const card=ph.closest('.scard');if(card.classList.contains('tvoff'))return;let f=ph.querySelector('.r2chip.f');
    if(!f){f=document.createElement('button');f.type='button';f.className='r2chip f';f.dataset.r2faces='1';ph.appendChild(f)}const v=window.R2GETFACES()||'center';f.textContent=(FL[v]||FL.center)+' ▾';});}
 window.addEventListener('pointerdown',e=>{const b=e.target.closest&&e.target.closest('[data-r2faces]');if(!b)return;e.preventDefault();e.stopPropagation();const v=window.R2GETFACES()||'center';setTimeout(()=>window.R2FACES(NX[v]||'center'),30)},true);
 window.addEventListener('click',e=>{if(e.target.closest&&e.target.closest('[data-r2faces]')){e.preventDefault();e.stopPropagation()}},true);
 let hinted=false;try{hinted=!!sessionStorage.getItem('r2swh')}catch(e){}
 function swh(){if(hinted||!document.body.classList.contains('tvmode'))return;const ph=document.querySelector('#s-mats .scard[id^="top-"] .ph img.tvimg');if(!ph)return;hinted=true;try{sessionStorage.setItem('r2swh','1')}catch(e){}
   const h=document.createElement('div');h.className='r2swh';h.innerHTML='Swipe right ♥ if you love it<br>Swipe left ✕ if it’s not the one';ph.parentElement.appendChild(h);setTimeout(()=>{h.style.opacity='0';setTimeout(()=>h.remove(),500)},3200);}

 const PEN='<svg viewBox="0 0 24 24"><path d="M4 20l4-1 11-11-3-3L5 16l-1 4z" fill="none" stroke="#c8325f" stroke-width="2.4" stroke-linejoin="round"/></svg>';
 let pulsed=false;
 function dots(){if(!document.body.classList.contains('tvmode'))return;document.querySelectorAll('.scard[id^="top-"] .ph').forEach(ph=>{const card=ph.closest('.scard');const img=ph.querySelector('img.tvimg');
   if(card.classList.contains('tvoff')||!img){ph.querySelectorAll('.r2dot').forEach(d=>d.remove());return}
   const pr=ph.getBoundingClientRect(),ir=img.getBoundingClientRect();if(!ir.width)return;const fx=x=>((ir.left-pr.left)+ir.width*x)/pr.width*100+'%',fy=y=>((ir.top-pr.top)+ir.height*y)/pr.height*100+'%';
   const fv=(window.R2GETFACES&&window.R2GETFACES())||'center';const pos={racks:[0.5,0.93]};if(fv==='center')pos.tiles=[0.62,0.40];else if(fv==='corner')pos.tiles=[0.86,0.70];
   for(const k of ['racks','tiles']){let d=ph.querySelector('.r2dot[data-r2open="'+k+'"]');if(!pos[k]){if(d)d.remove();continue}
    if(!d){d=document.createElement('button');d.type='button';d.className='r2dot'+(pulsed?'':' pulse');d.dataset.r2open=k;d.setAttribute('aria-label',k==='racks'?'Change the racks':'Change the tiles');d.innerHTML=PEN;ph.appendChild(d)}
    d.style.left=fx(pos[k][0]);d.style.top=fy(pos[k][1]);}
   });pulsed=true;}
 function bar(){if(!document.body.classList.contains('tvmode'))return;for(const id of ['s-mats','s-tiles','s-racks']){const sec=document.getElementById(id);if(!sec)continue;const card=sec.querySelector('.deck .scard[id^="top-"]');if(!card){continue}
   let b=sec.querySelector('.r2bar');const deck=card.closest('.deck');if(!b){b=document.createElement('div');b.className='r2bar';
    b.innerHTML='<button type="button" class="r2b" data-r2open="tiles"><img alt="">Tiles</button><button type="button" class="r2b" data-r2open="mat"><img alt="">Mat</button><button type="button" class="r2b" data-r2open="racks"><img alt="">Racks</button><div class="r2fc">Tile photo:<button type="button" data-r2f="center">Center</button><button type="button" data-r2f="corner">Corner</button><button type="button" data-r2f="off">Off</button></div>';
    deck.insertAdjacentElement('afterend',b)}
   let x=null;try{x=window.R2CTX(card)}catch(e){}if(x){const im=b.querySelectorAll('.r2b img');try{im[0].src=pile(x.s);im[1].src=matTh(x.mat);if(x.rack)im[2].src=rackSrc(x.rack)}catch(e){}}
   const fv=(window.R2GETFACES&&window.R2GETFACES())||'center';b.querySelectorAll('[data-r2f]').forEach(z=>z.classList.toggle('on',z.dataset.r2f===fv));
   const tab=window.R2TAB&&window.R2TAB(),open=document.getElementById('tvpanel')&&document.getElementById('tvpanel').classList.contains('open');b.querySelectorAll('.r2b').forEach(z=>z.classList.toggle('on',!!open&&z.dataset.r2open===tab));}}
 window.addEventListener('pointerdown',e=>{const b=e.target.closest&&e.target.closest('[data-r2f]');if(!b)return;e.preventDefault();e.stopPropagation();const v=b.dataset.r2f;setTimeout(()=>window.R2FACES(v),30)},true);
 window.addEventListener('click',e=>{if(e.target.closest&&e.target.closest('[data-r2f]')){e.preventDefault();e.stopPropagation()}},true);
 function open(card,tab){if(!card){const bb=document.activeElement;}const sec=card?card.closest('[id^="s-"]'):null;window.R2OPEN(tab,sec&&sec.id)}
 window.addEventListener('pointerdown',e=>{const b=e.target.closest&&e.target.closest('[data-r2open]');if(!b)return;e.preventDefault();e.stopPropagation();const c=b.closest('.scard')||b.closest('[id^="s-"]'),t=b.dataset.r2open;setTimeout(()=>open(c,t),30)},true);window.addEventListener('click',e=>{if(e.target.closest&&e.target.closest('[data-r2open]')){e.preventDefault();e.stopPropagation()}},true);
 let dn=null;
 window.addEventListener('pointerdown',e=>{const ph=e.target.closest&&e.target.closest('.scard[id^="top-"] .ph');dn=(ph&&document.body.classList.contains('tvmode')&&!e.target.closest('button'))?{x:e.clientX,y:e.clientY,t:Date.now(),ph}:null},true);
 window.addEventListener('pointerup',e=>{if(!dn)return;const d=dn;dn=null;if(Math.hypot(e.clientX-d.x,e.clientY-d.y)>8||Date.now()-d.t>350)return;
  const zz=S.zs&&S.zs.tvz;if(zz&&zz.s>1.05)return;const img=d.ph.querySelector('img.tvimg');if(!img)return;const r=img.getBoundingClientRect();
  const y=(e.clientY-r.top)/r.height,x=(e.clientX-r.left)/r.width;if(x<0||x>1||y<0||y>1)return;
  if(y<0.2||y>0.8||x<0.14||x>0.86)setTimeout(()=>open(d.ph.closest('.scard'),'racks'),60)},true);
 setInterval(()=>{yn();sheet();swh();dots();bar()},400);
})();
</script>"""
k = h.rindex('</body>'); h = h[:k] + css + js + h[k:]
open(P, 'w').write(h); print('ok', len(h))
