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
rep('function openP(mode,tab){', "window.R2OPEN=function(tab,sec){if(sec)CTX=sec;openP('swap',tab)};window.R2CTX=c=>ctx(c);window.R2TAB=()=>SW.tab;function openP(mode,tab){")
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
 function open(card,tab){const sec=card&&card.closest('[id^="s-"]');window.R2OPEN(tab,sec&&sec.id)}
 window.addEventListener('pointerdown',e=>{const b=e.target.closest&&e.target.closest('[data-r2open]');if(!b)return;e.preventDefault();e.stopPropagation();const c=b.closest('.scard'),t=b.dataset.r2open;setTimeout(()=>open(c,t),30)},true);window.addEventListener('click',e=>{if(e.target.closest&&e.target.closest('[data-r2open]')){e.preventDefault();e.stopPropagation()}},true);
 let dn=null;
 window.addEventListener('pointerdown',e=>{const ph=e.target.closest&&e.target.closest('.scard[id^="top-"] .ph');dn=(ph&&document.body.classList.contains('tvmode')&&!e.target.closest('button'))?{x:e.clientX,y:e.clientY,t:Date.now(),ph}:null},true);
 window.addEventListener('pointerup',e=>{if(!dn)return;const d=dn;dn=null;if(Math.hypot(e.clientX-d.x,e.clientY-d.y)>8||Date.now()-d.t>350)return;
  const zz=S.zs&&S.zs.tvz;if(zz&&zz.s>1.05)return;const img=d.ph.querySelector('img.tvimg');if(!img)return;const r=img.getBoundingClientRect();
  const y=(e.clientY-r.top)/r.height,x=(e.clientX-r.left)/r.width;if(x<0||x>1||y<0||y>1)return;
  if(y<0.2||y>0.8||x<0.14||x>0.86)setTimeout(()=>open(d.ph.closest('.scard'),'racks'),60)},true);
 setInterval(()=>{chips();yn()},500);
})();
</script>"""
k = h.rindex('</body>'); h = h[:k] + css + js + h[k:]
open(P, 'w').write(h); print('ok', len(h))
