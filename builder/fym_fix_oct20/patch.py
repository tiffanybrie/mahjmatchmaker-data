"""FYM Oct 20 fixes (P1 bugs + album tile photos + Tiffany's-match guard + hide no-tile photos).
Usage: python3 patch.py <site_dir> <out_dir>
  site_dir: local copy of the live FYM artifact files (index.html + b*.js + t1x/ + hd/ + mc/)
  out_dir : staged copy for publishing (site_dir is copied there first; new files: t16/*, b15v1.js, hd/index.json)
Every string replace asserts its match count. Data is edited via json raw_decode of `const D=`.
"""
import sys, os, json, re, io, base64, shutil, glob
from PIL import Image, ImageOps
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tilemap import TILEMAP
REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
SITE, OUT = sys.argv[1], sys.argv[2]
shutil.copytree(SITE, OUT, dirs_exist_ok=True)
h = open(os.path.join(SITE, 'index.html')).read()

# ---------- 0. strip the hosting wrapper from the downloaded page
k = h.find('<!doctype html>\n<html lang="en">')
assert k > 0, 'real doctype not found'
h = h[k:]
e = h.rfind('</script>')
tail = h[e:]
assert tail.count('</body></html>') == 3, tail
h = h[:e] + '</script>\n</body></html>\n'

def R(old, new, cnt=1):
    global h
    n = h.count(old)
    assert n == cnt, (n, old[:100])
    h = h.replace(old, new)

# ---------- 1. data
i = h.find('const D=') + 8
D, end = json.JSONDecoder().raw_decode(h, i)
T = D['tiles']
by = {}
for ix, s in enumerate(D['sets']):
    if s['name'] in by:   # e.g. Seabreeze (OMM album set #6) vs Seabreeze (Yellow Mountain catalog #262): keep the album one
        assert s.get('cat') and not s.get('album'), s['name']; continue
    by[s['name']] = (ix, s)
report = {'tile_photos': [], 'hidden': [], 'm_cleared': [], 'fp': [], 'partner': []}

def flat(p):
    im = Image.open(p).convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
def sig(im): return np.asarray(ImageOps.fit(im, (48, 48)).convert('L'), dtype=float)
def jpg(im, side, q=86):
    im = im.copy(); im.thumbnail((side, side), Image.LANCZOS); b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True); return b.getvalue()

# 1a. album / swipe-book tile photos: FYM must show exactly the album photo
os.makedirs(os.path.join(OUT, 't16'), exist_ok=True)
hdix_p = os.path.join(SITE, 'hd', 'index.json'); HDIX = json.load(open(hdix_p))
newimg = {}
for name, rel in TILEMAP.items():
    ix, s = by[name]; t = T[s['tile']]
    src = REPO + rel; assert os.path.exists(src), src
    old = t['full']; a = flat(src); o = flat(os.path.join(SITE, old))
    diff = float(np.abs(sig(o) - sig(a)).mean())
    ar_same = abs(o.size[0] / o.size[1] - a.size[0] / a.size[1]) < 0.02
    replaced = not (diff < 1.0 and ar_same)
    if replaced:
        fn = 't16/%s.jpg' % s['slug']
        open(os.path.join(OUT, fn), 'wb').write(jpg(a, 1000))
        t['full'] = fn
        HDIX['t'][s['tile']] = 'file:' + fn          # match card uses the album photo too
    t['src'] = rel
    report['tile_photos'].append([name, rel, old, t['full'], 'yes' if replaced else 'no (already identical)', round(diff, 1)])
# pile thumbnails (tile grid / tray) that were not tile photos
PILEFIX = ['December 1994']
for name in PILEFIX:
    ix, s = by[name]; t = T[s['tile']]
    a = ImageOps.fit(flat(REPO + TILEMAP[name]), (360, 360), Image.LANCZOS, centering=(.5, .5))
    b = io.BytesIO(); a.save(b, 'JPEG', quality=84); key = 'p16' + s['slug'][:20].replace('-', '')
    newimg[key] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    t['pile'] = key
open(os.path.join(OUT, 'b15v1.js'), 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(newimg) + ');\n')
os.makedirs(os.path.join(OUT, 'hd'), exist_ok=True)
json.dump(HDIX, open(os.path.join(OUT, 'hd', 'index.json'), 'w'))

# 1b. Tiffany's-match guard: lists only from real albums (s.album) or recorded swipe books (s.sb)
SWIPEBOOK = ['Brownstone Bloom', 'December 1994', 'Hummingbird', 'Sunday', 'Papaya Spritz']
for n in SWIPEBOOK: by[n][1]['sb'] = True
CLEAR = ['Sunshine', 'Florielle', 'Mahj in Bloom', 'Bams & Bubbly', 'Plum Panda', 'Little Bird', 'Nature Walk', 'Sunday Blues']
for n in CLEAR:
    s = by[n][1]; report['m_cleared'].append([n, len(s['m'])]); s['m'] = []
for s in D['sets']:
    if s['m'] and not (s.get('album') or s.get('sb')):
        report['m_cleared'].append([s['name'], len(s['m'])]); s['m'] = []

# 1c. hide catalog sets whose photo shows no tiles (bags, boxes, trays, scenes, graphics) until real photos are sourced
HIDE = {64: '90s Taffy (Pink)', 89: 'Yellow Lilac Ocean Blue', 114: 'The Jubilee Series', 115: 'The Lumera Series', 116: 'Crystal Confetti',
        117: 'The Play Series', 119: 'Crystal Prism', 194: 'Peach & Pine', 195: 'Barrier Island', 196: 'Sunshine', 197: 'Palmetto',
        198: 'Charleston', 200: 'Sunburst Debutante', 201: 'Poppy Debutante', 202: 'Cadet Debutante', 203: 'Jardin Debutante',
        238: 'Classic Mahjong Tile Set', 258: 'Mojave', 174: 'Nativity', 143: 'Classic Beechwood', 147: 'Mcm', 148: 'Boots & Bubbles',
        149: 'Deco', 167: 'Bespoke X Gray Malin Beach Club', 168: 'Bespoke X Gray Malin Getaway Dogs XL Mega',
        169: 'Grateful Dead x Bespoke Mahjong XL Mega', 170: 'Bespoke X Corey Paige Color Crush XL Mega'}
WHY = {64: 'colour-swatch graphic, no tiles', 89: 'bags and boxes, tiles tiny', 194: 'zip bag + rule card', 195: 'zip bag + rule card',
       196: 'tiles in a purple zip bag', 197: 'zip bag + rule card', 198: 'zip bag + rule card', 200: 'bag + racks, tiles tiny',
       201: 'bag + racks, tiles tiny', 202: 'bag + racks, tiles tiny', 203: 'bag + racks, tiles tiny', 238: 'acrylic trays only',
       258: 'single blank tile next to a quarter', 174: 'hand in frame, few tiny tiles', 143: 'trays of wood backs, no faces',
       147: 'acrylic trays', 148: 'acrylic trays', 149: 'acrylic trays'}
for ix, nm in HIDE.items():
    s = D['sets'][ix]; assert s['name'] == nm, (ix, s['name'], nm)
    assert not s.get('album') and not s.get('sb'), nm
    s['hid'] = True; report['hidden'].append([ix, nm, s['maker'], T[s['tile']]['full'],
        WHY.get(ix, 'product/bag/box scene, tiles not the subject' if ix < 170 or ix > 199 else 'product scene')])

# 1d. framing: per-set focal point (fraction of image) + initial zoom for the tile view
for s in D['sets']:
    if s.get('cat') and s['maker'] == 'Virora Mahjong': s['fp'] = [0.5, 0.68]      # layout shot: back tile sits bottom-right
    elif s.get('cat') and s['maker'] == 'Mahjong Studios': s['fp'] = [0.5, 0.72]   # title banner on top, back of tile bottom-right
    elif s.get('cat') and s['maker'] == 'Mahjong Row & Co.': s['fp'] = [0.5, 0.7]
by['Florielle'][1]['fp'] = [0.6, 0.7]; by['Florielle'][1]['fz'] = 1.15             # bottom rows + the pink/green back
report['fp'] = [[s['name'], s['fp'], s.get('fz', 1)] for s in D['sets'] if 'fp' in s]

# 1e. partner flags / codes
def each(brand):
    for kind in ('tiles', 'mats', 'racks'):
        for kk, o in D[kind].items():
            if o.get('bn') == brand: yield kind, kk, o
for _, _, o in each('Mahjong Studios'): o['nc'] = True                      # shop-through-link brand, no code
for _, _, o in each('Sunday Mahjong'): o['pa'] = False; o['nc'] = False
for _, _, o in each('Yellow Mountain Imports'): o['code'] = 'MAHJMATCH10-YMI-2025'
for _, _, o in each('Amanda Toppe'):
    o['pa'] = True; o['nc'] = False; o['dc'] = 'https://mahjmatchmaker.com/amanda-toppe-discount-code'
for kind in ('tiles', 'mats', 'racks'):
    for kk, o in D[kind].items():
        if o.get('u', '').startswith('/'):
            o['u'] = 'https://www.mahjmatchmaker.com' + o['u']
            report['partner'].append(['abs-url', kk, o['u']])
m = D['mats'].get('alb2:charleston-mahjong-club-club-mat')
assert m and m['u'] == 'https://www.mahjmatchmaker.com/charleston-mahjong-club-discount-code', m

# 1g. mat audit (scratchpad/mat-audit/report.csv, copied to mat_audit_report.csv): hide placeholders / wrong images / no-mat photos,
#     hide raw Mahjong Studios "...Ships Rolled" duplicates (keep clean listings), clean raw names, brand spellings
import csv
MA = list(csv.DictReader(open(os.path.join(HERE, 'mat_audit_report.csv'))))
MM = D['mats']; report['mats'] = {'hidden': [], 'image_from_twin': [], 'renamed': [], 'brand': [], 'her_list_remap': [], 'color': []}
def hide_mat(mid, why):
    if mid in MM and not MM[mid].get('hid'):
        MM[mid]['hid'] = True; report['mats']['hidden'].append([mid, MM[mid]['n'], MM[mid]['bn'], why])
# Mahjong Studios twins
def core(n): return re.sub(r'\s+', ' ', re.split(r'\s+(?:-\s+)?Mahjong Mat', n)[0].replace('The ', '')).strip(' -')
SPECIAL = {'Jade Peacock': 'Green Jade Peacock', 'Blue Songbird': 'Blue Birdsong'}
clean = {o['n']: k for k, o in MM.items() if o['bn'] == 'Mahjong Studios' and '?v=' in k}
twin = {}
for k, o in MM.items():
    if o['bn'] == 'Mahjong Studios' and 'ships rolled' in o['n'].lower():
        c = SPECIAL.get(core(o['n']), core(o['n'])); assert c in clean, (k, o['n'], c); twin[k] = clean[c]
for raw, cl in twin.items():
    if MM[cl]['n'] in ('Ivory Coast', 'Pastel Luxe'):        # clean listing showed the Looking Glass image; the raw listing has the right one
        for f in ('f', 'th', 'w', 'h', 'ms', 'mf', 'c'): MM[cl][f] = MM[raw][f]
        report['mats']['image_from_twin'].append([cl, MM[cl]['n'], raw])
    hide_mat(raw, 'duplicate Mahjong Studios "Ships Rolled" listing (kept %s)' % cl)
raw_lf = 'mahjongstudios.com/lunaflor-mahjong-mat'
if raw_lf in MM: MM[raw_lf]['n'] = 'Lunaflor'
for s in D['sets']:                                           # her lists keep pointing at a visible listing
    for x in s['m']:
        if x[0] in twin: report['mats']['her_list_remap'].append([s['name'], x[0], twin[x[0]]]); x[0] = twin[x[0]]
for r in MA:
    pt, mid = r['problem_type'], r['mat_id']
    if mid not in MM: continue
    if pt == 'placeholder image': hide_mat(mid, 'placeholder "Photo coming soon" image')
    elif pt == 'wrong image (shows another mat)' and MM[mid]['n'] not in ('Ivory Coast', 'Pastel Luxe'): hide_mat(mid, 'wrong image: ' + r['detail'][:120])
    elif 'no mat' in r['detail'].lower() and pt != 'partial crop (full mat not shown)': hide_mat(mid, 'photo shows no mat: ' + r['detail'][:120])
    elif pt == 'raw store title':
        mm = re.match(r'rename to "(.+)"$', r['suggested_fix'])
        if mm and mm.group(1).strip() and MM[mid]['n'] == r['name']:
            report['mats']['renamed'].append([mid, MM[mid]['n'], mm.group(1)]); MM[mid]['n'] = mm.group(1)
for k, o in MM.items():
    if o['bn'] == 'Mahj and Moon': o['bn'] = 'Mahj & Moon'; report['mats']['brand'].append([k, 'Mahj and Moon -> Mahj & Moon'])
    if o['bn'] == 'Ozark Mah Jongg': o['bn'] = 'Ozark Mahjongg'; report['mats']['brand'].append([k, 'Ozark Mah Jongg -> Ozark Mahjongg'])
# Tiffany's colour calls (config/mat-color-overrides.json, by tiffany-chat-2026-10-20) -> FYM colour families
FAMMAP = {'teal': 'blue', 'aqua': 'blue', 'navy': 'blue', 'brown': 'dark', 'black': 'dark', 'white': 'neutral', 'ivory': 'neutral', 'cream': 'neutral', 'gold': 'yellow', 'coral': 'orange', 'lavender': 'purple'}
FAMS = ['pink', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'neutral', 'dark']
CO = json.load(open(REPO + 'config/mat-color-overrides.json'))['mats']
for mid, c in CO.items():
    if c.get('by') != 'tiffany-chat-2026-10-20' or mid not in MM or c.get('skip'): continue
    fam = []
    for x in [c.get('primary')] + list(c.get('secondary') or []):
        x = FAMMAP.get(x, x)
        if x in FAMS and x not in fam: fam.append(x)
    if fam and fam != MM[mid]['mf']:
        report['mats']['color'].append([mid, MM[mid]['n'], MM[mid]['mf'], fam]); MM[mid]['mf'] = fam

# 1f. mats named "(retired)" but not flagged: flag them so they only appear through her real albums
report['retired_flagged'] = []
for kk, o in D['mats'].items():
    if '(retired)' in o['n'].lower() and not o['rt']:
        o['rt'] = True; report['retired_flagged'].append(o['n'])

h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]

# ---------- 2. static first paint + bundle order (tile grid bundles first, the rest after first render)
icon_key = D['logos']['icon']; ICON = ''
for f in glob.glob(os.path.join(SITE, 'b*.js')):
    mm = re.search('"' + icon_key + r'"\s*:\s*"(data:image/[^"]+)"', open(f).read())
    if mm: ICON = mm.group(1); break
assert ICON and len(ICON) < 60000, len(ICON)
R('<div id="app"><header class="top"><img id="logo" alt="Mahj Matchmaker">',
  '<div id="app"><header class="top"><img id="logo" alt="Mahj Matchmaker" src="' + ICON + '">')
R('<section id="s-tiles" class="sec"></section>',
  '<section id="s-tiles" class="sec"><div class="boot" id="boot"><img src="' + ICON + '" alt=""><p>Loading your matches…</p></div></section>')
OLD_TAGS = ('<script src="b0v10.js"></script>\n<script src="b1v10.js"></script>\n<script src="b2v10.js"></script>\n<script src="b3v10.js"></script>\n'
            '<script src="b4v11.js"></script><script src="b5v1.js"></script><script src="b6v1.js"></script><script src="b8v1.js"></script>'
            '<script src="b7v1.js"></script><script src="b9v1.js"></script><script src="b10v1.js"></script><script src="b11v1.js"></script>'
            '<script src="b12v1.js"></script><script src="b13v1.js"></script><script src="b14v1.js"></script>')
FIRST = ['b2v10.js', 'b3v10.js', 'b6v1.js', 'b7v1.js', 'b9v1.js', 'b10v1.js', 'b13v1.js', 'b15v1.js']   # tile piles + logos
LAZY = ['b14v1.js', 'b0v10.js', 'b8v1.js', 'b12v1.js', 'b4v11.js', 'b11v1.js', 'b1v10.js', 'b5v1.js']   # mats + racks
assert sorted(FIRST[:-1] + LAZY) == sorted(re.findall(r'src="(b\d+v\d+\.js)"', OLD_TAGS))
R(OLD_TAGS, '<script>window.IMG=window.IMG||{};window.__LAZY=' + json.dumps(LAZY) + ';</script>\n' +
  ''.join('<script src="%s"></script>' % f for f in FIRST))
R('.mgrid img{border-radius:14px}\n</style>', '''.mgrid img{border-radius:14px}
/* Oct 20 */
.boot{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;min-height:46vh;color:var(--navy);font:700 16px var(--body)}
.boot img{width:64px;height:64px;object-fit:contain;animation:bootp 1.2s ease-in-out infinite}
.boot p{margin:0}
@keyframes bootp{50%{transform:scale(.9);opacity:.75}}
.scard .ph img:not(.onmat){width:100%;height:100%}
.matv img{width:100%;height:100%}
.si span.go{opacity:.6}
</style>''')

# ---------- 3. app script
# guard + hidden sets
R("const set=()=>D.sets[S.set];",
  "D.sets.forEach(s=>{if(!(s.album||s.sb))s.m=[];});/* Oct 20: Tiffany's match = album or recorded swipe book only */\n"
  "const VIS=s=>!(s.hid||(T[s.tile]&&T[s.tile].hid));\nconst set=()=>D.sets[S.set];")
R("function tileGrid(){const all=D.sets.map((s,i)=>[s,i]);", "function tileGrid(){const all=D.sets.map((s,i)=>[s,i]).filter(x=>VIS(x[0]));")
R("const hits=D.sets.map((s,i)=>[s,i]).filter(([s])=>{const h=", "const hits=D.sets.map((s,i)=>[s,i]).filter(([s])=>VIS(s)).filter(([s])=>{const h=")
R("function setsForMat(id){const ix=D.order.indexOf(id);const rows=D.sets.map((s,i)=>{",
  "function setsForMat(id){const ix=D.order.indexOf(id);const rows=D.sets.map((s,i)=>[s,i]).filter(x=>VIS(x[0])).map(([s,i])=>{")
R("function matCounts(){if(DOOR.cnt)return DOOR.cnt;const c={};D.sets.forEach(s=>s.m.forEach(",
  "function matCounts(){if(DOOR.cnt)return DOOR.cnt;const c={};D.sets.filter(VIS).forEach(s=>s.m.forEach(")
R("function matPool(){const h=set().m.map(x=>x[0]).filter(id=>M[id]);", "function matPool(){const h=set().m.map(x=>x[0]).filter(id=>M[id]&&!M[id].hid);")
# fix 1: colour dots
R("if(b=q('.dots [data-fam]')){", "if(b=q('.frow [data-fam]')){")
# fix 2/3: zoom state kept across swipes + per-set focal point
R("function zoomer(host,img,box,opt){opt=opt||{};let z={s:1,x:0,y:0};\n const apply=a=>{img.style.transition=a?'transform .2s':'none';img.style.transform=`translate(${z.x}px,${z.y}px) scale(${z.s})`;host.style.touchAction=(z.s>1||opt.swipe)?'none':'pan-y';};",
  "function zoomer(host,img,box,opt){opt=opt||{};let z={s:1,x:0,y:0};\n const apply=a=>{img.style.transition=a?'transform .2s':'none';img.style.transform=`translate(${z.x}px,${z.y}px) scale(${z.s})`;host.style.touchAction=(z.s>1||opt.swipe)?'none':'pan-y';if(opt.key)S.zs[opt.key]={s:z.s,x:z.x,y:z.y};};")
R("const init=()=>{if(opt.cover){clamp();}apply(false);};",
  "const init=()=>{const st=opt.key&&S.zs[opt.key];if(st){z={s:st.s,x:st.x,y:st.y};clamp();}"
  "else if(opt.fp){const r=box.getBoundingClientRect(),w=img.offsetWidth,hh=img.offsetHeight;z.s=Math.max(1,Math.min(4,opt.fz||1));z.x=r.width/2-img.offsetLeft-opt.fp[0]*w*z.s;z.y=r.height/2-img.offsetTop-opt.fp[1]*hh*z.s;clamp();}"
  "else if(opt.cover){clamp();}apply(false);};")
R("S.f={m:{fam:'',brand:'',her:false},r:{fam:'',brand:'',her:false}};", "S.f={m:{fam:'',brand:'',her:false},r:{fam:'',brand:'',her:false}};S.zs={};")
R("function resetFrom(level){if(level<=1){Object.assign(S,{seen:{},liked:[],hist:[],peek:null,dset:null});",
  "function resetFrom(level){if(level<=1){Object.assign(S,{seen:{},liked:[],hist:[],peek:null,dset:null,zs:{}});")
R("zoomer(c,img,ph,{zoom:k==='m'&&S.mode==='close',swipe:",
  "zoomer(c,img,ph,{key:k==='m'&&S.mode==='close'?'mz':null,zoom:k==='m'&&S.mode==='close',swipe:")
R("function bindTile(id){const t=$(id);if(!t)return;zoomer(t,t.querySelector('img'),t,{cover:true});}",
  "function bindTile(id){const t=$(id);if(!t)return;const s=set();zoomer(t,t.querySelector('img'),t,{cover:true,key:'tz_'+id,fp:s.fp||[.5,.5],fz:s.fz||1});}")
# fix 5: "Your mat" note only while peeking the door mat
R("(S.dmat&&S.dset===S.set&&M[S.dmat]?", "(S.dmat&&S.dset===S.set&&S.peek&&S.peek===S.dmat&&M[S.dmat]?")
R("if(q('[data-unpeek]')){S.peek=null;", "if(q('[data-unpeek]')){S.peek=null;S.dset=null;")
R("if(k==='m'){S.seen[id]=1;S.hist.push(id);", "if(k==='m'){S.dset=null;S.seen[id]=1;S.hist.push(id);")
# fix 6: wording
R('<span class="stamp yes">CRUSH</span><span class="stamp no">NEXT</span>', '<span class="stamp yes" aria-hidden="true">♥</span><span class="stamp no" aria-hidden="true">✕</span>')
R('aria-label="Pass" ${q.length', 'aria-label="No thanks" ${q.length')
R('aria-label="Crush" ${q.length', 'aria-label="Love" ${q.length')
R("set().m.length?'Right = crush, left = pass':'Tiffany hasn\\u2019t matched '+esc(set().name)+' yet. Match away! Right = crush, left = pass'",
  "set().m.length?'Tap \\u2665 if you love it, \\u2715 if it\\u2019s not the one':'Tiffany hasn\\u2019t matched '+esc(set().name)+' yet. Match away! Tap \\u2665 if you love it, \\u2715 if it\\u2019s not the one'")
R('<div><b>2</b>Pick your crush</div>', '<div><b>2</b>Pick your favorite</div>')
# fix 10: wait for the mat/rack bundles before drawing mats; first paint comes from the tile bundles
R("function renderMats(){const el=$('s-mats');if(S.set==null){el.innerHTML='';return;}",
  "const BOOT=t=>`<div class=\"boot\"><img src=\"${LG('icon')}\" alt=\"\"><p>${t}</p></div>`;\n"
  "function renderMats(){const el=$('s-mats');if(S.set==null){el.innerHTML='';return;}if(!window.__imgsReady){el.innerHTML=BOOT('Loading the mats\\u2026');return;}")
R("function renderRacks(){const el=$('s-racks');if(S.set==null){el.innerHTML='';return;}",
  "function renderRacks(){const el=$('s-racks');if(S.set==null){el.innerHTML='';return;}if(!window.__imgsReady){el.innerHTML='';return;}")
R("function renderMatDoor(el){const lock=", "function renderMatDoor(el){if(!window.__imgsReady){el.innerHTML=BOOT('Loading the mats\\u2026');return;}const lock=")
R("renderAll();\n\n</script>",
  "renderAll();\n"
  "(function(){const L=window.__LAZY||[];let n=L.length;const done=()=>{if(window.__imgsReady)return;window.__imgsReady=true;"
  "if(S.door==='mat'&&(S.set==null||S.tilesOpen))renderTiles();if(S.set!=null){renderMats();renderRacks();steps();}};"
  "if(!n){done();return;}const go=()=>L.forEach(f=>{const s=document.createElement('script');s.src=f;s.async=false;s.onload=s.onerror=()=>{if(--n===0)done();};document.body.appendChild(s);});"
  "requestAnimationFrame(()=>setTimeout(go,0));})();\n\n</script>")
R("<span>${esc(o.bn)}${o.rt?' · retired':''}", "<span>${esc(o.bn)}${o.rt&&!/retired/i.test(o.n)?' · retired':''}")
# fix 9: prototype email box
R("if(q('[data-mail]')){mail();return;}\n", "")
R(''' <div class="mailbox"><h3>Email me my match card</h3><p>We’ll email you the view you picked in both sizes: a post size and a tall pin size.</p><div class="row"><input type="email" id="em" placeholder="you@email.com" autocomplete="email" aria-label="Email"><button type="button" data-mail>Send</button></div><div id="mailok" hidden></div></div>\n''', '')
mi = h.find('function mail(){'); mj = h.find('</script>', mi); assert mi > 0 and h.count('function mail(){') == 1
h = h[:mi] + h[mj:]
# fix 8: no Shop link without a URL
R('''<a class="go" href="${esc(o.u)}" target="_blank" rel="noopener">${o.rt?'Retired':'Shop ›'}</a>''',
  '''${o.u?`<a class="go" href="${esc(o.u)}" target="_blank" rel="noopener">${o.rt?'Retired':'Shop ›'}</a>`:(o.rt?'<span class="go">Retired</span>':'')}''')
# fix 7: card footer code line
R("function allPartner(){return T[set().tile].pa&&!T[set().tile].nc&&M[S.fav].pa&&!M[S.fav].nc&&S.rpick.every(r=>R[r].pa&&!R[r].nc);}",
  "function codeLine(){const ps=[T[set().tile],M[S.fav],...S.rpick.map(r=>R[r])].filter(o=>o&&o.pa&&!o.nc);if(!ps.length)return '';"
  "if(ps.some(o=>!o.code))return 'Use code MAHJMATCH';return 'Use code '+ps[0].code;}")
R("const t=allPartner()?'Use code MAHJMATCH to save 10%':'Swipe for your own match'", "const t=codeLine()||'Swipe for your own match'")

open(os.path.join(OUT, 'index.html'), 'w').write(h)
json.dump(report, open(os.path.join(OUT, 'patch_report.json'), 'w'), indent=1, ensure_ascii=False)
print('ok', len(h), 'replaced photos:', sum(1 for r in report['tile_photos'] if r[4] == 'yes'), 'hidden:', len(report['hidden']), 'm cleared:', len(report['m_cleared']))
