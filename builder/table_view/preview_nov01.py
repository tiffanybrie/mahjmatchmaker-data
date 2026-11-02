"""Find Your Mat-ch PREVIEW with Table view (Nov 1, Tiffany 5:47pm: a FULL app her husband can run start to finish; NOT the
website, NOT the live artifact). Takes the live artifact copy's index.html (pub112 = Version 1.12) and:
  1. adds 'Table' as the third option of the View switch (Up close / Aerial / Table); table mode reuses the Aerial layout,
  2. injects builder/table_view/preview_tv.js (rebuilt Nov 1 8pm to the SAMPLE's UX): every swipe card is a top-down
     table (walls from config/tableview-back-colors.json ONLY, never the title color; coverage classes from
     config/tableview-photo-class-nov01.json; sizes from config/tableview-sizecheck-nov01.json), one Adjust button by the
     View switch -> bottom sheet (Swap tiles/mat/racks, Walls, Tile faces) -> swap sheet (tabs, per-tab search, brand,
     color, finish, in stock, Tiffany's picks, price), always 4 players; small app patches (zoom on Table cards, ⤢ = whole
     table full screen, land on the table after each step, a swapped pick goes on top of the app's own deck),
  3. labels the build 'Version 1.12 + Table view preview'.
All other files are copied server-side from the live artifact at publish. Usage: python3 preview_nov01.py <pub index.html> <out dir>"""
import sys, json, re, io, base64, pathlib, os
from PIL import Image
R = pathlib.Path(__file__).resolve().parents[2]
SRC, OUT = sys.argv[1], pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
h = open(SRC).read()
i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
COV = json.load(open(R / 'config/tableview-photo-class-nov01.json'))
BACK = json.load(open(R / 'config/tableview-back-colors.json'))
STK = json.load(open(R / 'config/fym-stock.json'))['items']
PCT = json.load(open(R / 'config/fym-code-pct.json'))['pct']
def durl(p, px=320, alpha=False):
    im = Image.open(R / p).convert('RGBA' if alpha else 'RGB'); im.thumbnail((px, px)); b = io.BytesIO(); im.save(b, 'WEBP', quality=82)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
cls, why = {}, {}
for k in D['mats']:
    c = COV.get(k)
    if not c: continue
    cl = 'C' if c.get('racks') == 'colored' else c['class']; cls[k] = cl
    if cl == 'C': why[k] = 'its photo has its own colored racks on it.' if c.get('racks') == 'colored' else 'no flat, top-down photo of this mat yet.'
rk = {k: 1 for k, v in COV['_racks'].items() if v['class'] == 'S'}
rkw = {k: ('Only a group or lifestyle photo of these racks.' if v['class'] == 'G' else 'Only an angled photo of these racks.') for k, v in COV['_racks'].items() if v['class'] != 'S'}
FIN = [('walnut', r'walnut'), ('wood', r'wood|walnut|oak|beech|acacia|maple|cherry|mahogany'), ('tortoise', r'tortoise|hawksbill|burl'),
       ('pearl', r'pearl|iridescent|opal|mother.of|shell|nacre'), ('clear', r'clear|acrylic|transparent|crystal'), ('lucite', r'lucite'),
       ('metallic', r'metallic|gold|silver|chrome|bronze|copper'), ('white', r'\bwhite\b'), ('glitter', r'glitter|sparkle|confetti')]
fin, price, so = {}, {}, {}
for k, r in D['racks'].items():
    t = (r['n'].replace(r.get('bn', ''), '') + ' ' + ' '.join(r.get('rf', []))).lower()
    f = [a for a, rx in FIN if re.search(rx, t)]
    if f: fin[k] = f
    s = STK.get('r:' + k, {})
    if s.get('in') is False: so[k] = 1
    if s.get('price') is not None:
        pc = PCT.get(r['bn']) if r.get('pa') else None; v = s['price']
        price[k] = [v, round(v * (1 - pc / 100), 2) if pc else v, int(bool(pc))]
backs = {}
for slug, v in BACK.items():
    if slug.startswith('_'): continue
    e = {'b': v['back']}
    if v.get('patch'): e['p'] = durl(v['patch'])
    if v.get('sprite'):
        bp = Image.open(R / v['sprite']).convert('RGBA'); bp = bp.crop(bp.split()[3].point(lambda x: 255 if x > 128 else 0).getbbox()); bp.thumbnail((320, 320))
        b = io.BytesIO(); bp.save(b, 'WEBP', quality=82); e['s'] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    backs[slug] = e
def pz(key, bn, pa):
    v = STK.get(key, {}).get('price')
    if v is None or not v: return None
    pc = PCT.get(bn) if pa else None
    return [v, round(v * (1 - pc / 100), 2) if pc else v, int(bool(pc))]
pm = {k: x for k, m in D['mats'].items() if not m.get('hid') and (x := pz('m:' + k, m['bn'], m.get('pa')))}
pt = {}
for sl in D['sets']:
    t = D['tiles'].get(sl['tile'], {}); x = pz('t:' + sl['tile'], t.get('bn', sl['maker']), t.get('pa'))
    if x: pt[sl['tile']] = x
fr = lambda x: int(round(x / 5) * 5) if x < 100 else (int(round(x / 25) * 25) if x < 300 else int(round(x / 50) * 50))
def ranges(vals):
    v = sorted(vals); return sorted(set(fr(v[int(len(v) * f)]) for f in (.2, .4, .6, .8))) if len(v) >= 8 else []
pr = {'mat': ranges([x[1] for x in pm.values()]), 'tiles': ranges([x[1] for x in pt.values()]), 'racks': ranges([x[1] for x in price.values()])}
SC = json.load(open(R / 'config/tableview-sizecheck-nov01.json'))
sz = {'mat': SC.get('mat_listed_in', 33.0), 'edge': 1.0, 'wallDepth': SC['wall_depth_in'] / SC['tile_width_in'], 'gap': SC['wall_to_rack_gap_in']}
TVD = dict(cls=cls, why=why, rk=rk, rkw=rkw, fin=fin, price=price, pm=pm, pt=pt, so=so, backs=backs, pr=pr, sz=sz)
css = """<style>/* Table view preview (Nov 1 rebuild: sample UX) */
/* WebKit iPhone: the step nav (.stp, 289px) would not shrink and pushed the stars/account icons 10px off-screen (also in live 1.12) */
html{overflow-x:hidden;overscroll-behavior-x:none}body{overflow-x:clip;max-width:100%}/* not overflow on body: WebKit would make body the scroller and window.scrollTo would stop working */.top .stp{min-width:0;flex:1 1 auto;overflow:hidden}
body.tvmode .scard .onmat{display:none}
.scard .ph img.tvimg{object-fit:contain;border-radius:10px}
.scard.tvoff .ph img{filter:grayscale(1) opacity(.5)}
.tvna{position:absolute;left:8px;right:8px;bottom:8px;z-index:3;background:rgba(255,255,255,.95);border-radius:10px;padding:6px 9px;font:600 12px/1.3 var(--body);color:#2a2036;pointer-events:none}
@media (max-width:460px){.vrow>span{display:none}.vrow{gap:6px}.vrow .seg.mode button{padding-left:10px;padding-right:10px}}/* 3 views + Adjust fit a phone */
.tvadj{border:1px solid #ecd5df;background:#fff;border-radius:999px;padding:7px 11px;font:700 12.5px/1 var(--body);color:var(--navy,#054689);cursor:pointer;flex:none}
.vrow.tvctl{margin:2px 0 6px}
.tvp{position:fixed;left:0;right:0;bottom:0;z-index:250;background:#fff;border-radius:18px 18px 0 0;max-height:46vh;max-height:46dvh;overflow-y:auto;overflow-x:hidden;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;
 transform:translateY(105%);transition:transform .25s ease;padding:0 max(14px,env(safe-area-inset-left,0px)) calc(14px + env(safe-area-inset-bottom,0px));box-shadow:0 -10px 30px rgba(0,0,0,.18);font:14px/1.4 var(--body);color:#2a2036;display:flex;flex-direction:column;gap:10px;visibility:hidden}
.tvp.open{transform:none;visibility:visible}.tvp.drag{transition:none}
@media (min-width:700px){.tvp{left:50%;right:auto;width:560px;margin-left:-280px}}
.tvp[data-mode="adjust"] .tvswapsec,.tvp[data-mode="swap"] .tvadjsec,.tvp[data-mode="adjust"] .tvback{display:none}
.tvp section{display:flex;flex-direction:column;gap:10px;min-width:0}
.tvp h3{margin:0;font:400 18px/1.15 var(--display,serif);color:var(--navy,#054689)}
.tvgrab{position:sticky;top:0;z-index:3;background:#fff;display:flex;align-items:center;justify-content:space-between;padding:8px 0 4px;touch-action:none;cursor:grab;-webkit-user-select:none;user-select:none}
.tvgrab span{position:absolute;left:50%;top:6px;width:44px;height:5px;margin-left:-22px;border-radius:9px;background:#d8ccd6}
.tvx{margin-left:auto;border:0;background:none;font-size:24px;line-height:1;color:#76687f;padding:4px 8px;cursor:pointer}
.tvback{border:0;background:none;font:700 13px var(--body);color:var(--navy,#054689);padding:4px 0;cursor:pointer}
.tvswaps{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.tvswaps button{border:0;background:#c8325f;color:#fff;border-radius:999px;padding:11px 4px;font:700 13px/1 var(--body);cursor:pointer}
.tvc{display:flex;align-items:center;justify-content:space-between;gap:10px;font-weight:600}
.tvsw{position:relative;width:44px;height:26px;border-radius:999px;border:0;background:#d9cfdc;flex:none;cursor:pointer;padding:0}.tvsw::after{content:"";position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:#fff;transition:left .15s}
.tvsw[aria-checked="true"]{background:#c8325f}.tvsw[aria-checked="true"]::after{left:21px}
.tvseg{display:inline-flex;border:1px solid #ecd5df;border-radius:999px;overflow:hidden}.tvseg button{border:0;background:#fff;padding:8px 12px;font:600 13px/1 var(--body);color:#76687f;cursor:pointer}.tvseg button.on{background:var(--navy,#054689);color:#fff}
.tvhint{margin:0;font-size:12.5px;color:#76687f}.tvlink{border:0;background:none;color:#c8325f;font:700 12.5px var(--body);padding:0;cursor:pointer;text-decoration:underline}
.tvtabs{display:flex;border-bottom:1px solid #ecd5df}.tvtabs button{flex:1;border:0;background:none;padding:9px 4px;font:700 14px/1 var(--body);color:#76687f;border-bottom:3px solid transparent;cursor:pointer}.tvtabs button.on{color:var(--navy,#054689);border-bottom-color:var(--navy,#054689)}
.tvsearch{display:flex;align-items:center;gap:8px;border:1px solid #ecd5df;border-radius:999px;padding:6px 6px 6px 12px;background:#fff}.tvsearch input{border:0;outline:0;flex:1;min-width:0;font:16px var(--body);background:none;color:#2a2036}
.tvsearch button{border:0;background:#c8325f;color:#fff;border-radius:999px;padding:5px 11px;font:700 12px/1.2 var(--body);cursor:pointer}
.tvbw{position:relative}.tvbtn{border:1px solid #ecd5df;background:#fff;border-radius:999px;padding:8px 14px;font:600 13px/1 var(--body);color:var(--navy,#054689);cursor:pointer}
.tvpop{position:absolute;z-index:5;top:calc(100% + 6px);left:0;width:min(340px,calc(100vw - 48px));max-height:260px;overflow:auto;background:#fff;border:1px solid #ecd5df;border-radius:12px;box-shadow:0 12px 30px rgba(0,0,0,.18);padding:6px}
.tvpop button{display:block;width:100%;border:0;background:none;text-align:left;padding:8px 6px;border-radius:8px;font:14px var(--body);cursor:pointer}.tvpop .tvh{color:#c8325f}
.tvchips{display:flex;gap:7px;flex-wrap:wrap;align-items:center}.tvchips[hidden]{display:none}
.tvchip{border:1px solid #ecd5df;background:#fff;border-radius:999px;padding:5px 10px;font:600 12px/1 var(--body);cursor:pointer;text-transform:capitalize}.tvchip.on{background:var(--navy,#054689);border-color:var(--navy,#054689);color:#fff}
.tvdot{width:24px;height:24px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 1px #ecd5df;padding:0;cursor:pointer}.tvdot.on{box-shadow:0 0 0 2px var(--navy,#054689)}
.tvdot.all{width:auto;padding:0 10px;border-radius:999px;font:700 12px/20px var(--body);background:#fff;color:var(--navy,#054689)}
.tvtg{display:flex;gap:16px;flex-wrap:wrap}.tvtg label{display:flex;align-items:center;gap:7px;font:600 13px var(--body)}
.tvact{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:13px;background:#fbe3ec;border-radius:10px;padding:7px 10px}.tvact[hidden]{display:none}.tvact button{border:0;background:#c8325f;color:#fff;border-radius:999px;padding:4px 11px;font:700 12px/1.3 var(--body);cursor:pointer}
.tvgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(92px,1fr));gap:10px}
.tvit{position:relative;border:0;background:none;padding:0;text-align:left;display:flex;flex-direction:column;gap:3px;cursor:pointer;min-width:0;color:#2a2036}
.tvit .ph{position:relative;aspect-ratio:1;border-radius:10px;overflow:hidden;background:#f2ecf1;border:2px solid transparent}
.tvgrid.rk .tvit .ph{aspect-ratio:2/1;display:flex;align-items:center;justify-content:center;background:#f6f1f4}
.tvit .ph img{width:100%;height:100%;object-fit:cover;display:block}.tvgrid.rk .tvit .ph img{object-fit:contain;padding:4px}
.tvit.on .ph{border-color:var(--navy,#054689)}
.tvpk{position:absolute;top:5px;right:5px;width:20px;height:20px;border-radius:50%;background:#fff;color:#c8325f;font-size:12px;display:grid;place-items:center;box-shadow:0 1px 3px rgba(0,0,0,.2)}
.tvtag{position:absolute;left:5px;bottom:5px;right:5px;background:rgba(255,255,255,.94);border-radius:6px;font:700 9.5px/1.2 var(--body);padding:3px 5px}
.tvit.off .ph img{filter:grayscale(1) opacity(.45)}.tvit.off .nm,.tvit.off .bn{color:#b8adbf}
.tvit .nm{font:600 11.5px/1.2 var(--body);overflow-wrap:anywhere}.tvit .nm small{color:#c8325f;font-weight:700}.tvit .bn{font-size:10.5px;color:#76687f;line-height:1.2}
.tvit .pr{font:700 11.5px/1.2 var(--body)}.tvit .pr em{display:block;font:italic 400 10px/1.2 var(--body);color:#c8325f}
.tvempty{font-size:13px;color:#76687f;padding:8px 0;grid-column:1/-1}
#tvtoast{position:fixed;left:50%;bottom:calc(24px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:#2a2036;color:#fff;border-radius:16px;padding:9px 15px;font:13px/1.35 var(--body);z-index:400;max-width:calc(100vw - 32px);text-align:center}
#tvtoast[hidden]{display:none}
</style>"""
js = (R / 'builder/table_view/preview_tv.js').read_text()
inj = css + '<script>const TVD=' + json.dumps(TVD, separators=(',', ':')) + ';</script><script>' + js + '</script>'
a = """<button type="button" data-mode="aerial" aria-pressed="${S.mode==='aerial'}">Aerial</button>"""
assert h.count(a) == 1, h.count(a)
h = h.replace(a, a + """<button type="button" data-mode="table" aria-pressed="${S.mode==='table'}">Table <b style="color:#c8325f;font-size:9px;letter-spacing:.06em">NEW</b></button>""")
n = h.count("S.mode==='aerial'"); h = h.replace("S.mode==='aerial'", "(S.mode==='aerial'||S.mode==='table')")
h = h.replace("""aria-pressed="${(S.mode==='aerial'||S.mode==='table')}">Aerial""", """aria-pressed="${S.mode==='aerial'}">Aerial""")
for v in re.findall(r'Version 1\.\d+(?:\.\d+)?', h)[:1]:
    h = h.replace(v + '<', v + ' + Table view preview<')
h = re.sub(r'<title>[^<]*</title>', '<title>Find Your Mat-ch Preview</title>', h, count=1)
def sub1(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:80]); h = h.replace(a, b)
# Table cards zoom like Up close (pinch, double-tap, + / -), one shared key so zoom persists across swipes and swaps
sub1("zoomer(c,img,ph,{key:k==='m'&&S.mode==='close'?'mz':null,zoom:k==='m'&&S.mode==='close',",
     "zoomer(c,img,ph,{key:S.mode==='table'?'tvz':(k==='m'&&S.mode==='close'?'mz':null),zoom:(k==='m'&&S.mode==='close')||S.mode==='table',")
sub1("zoomer(c,img,c.querySelector('.ph'),{zoom:false,", "zoomer(c,img,c.querySelector('.ph'),{zoom:S.mode==='table',key:S.mode==='table'?'tvz':null,")
ZB = """<div class="zb"><button type="button" data-z="-1" aria-label="Zoom out">−</button><button type="button" data-z="1" aria-label="Zoom in">+</button></div>"""
sub1("${back||!mat?''" + ":`<button type=" + '"button" class="xz"', "${back||(!mat&&S.mode!=='table')?''" + ":`<button type=" + '"button" class="xz"')
sub1("${mat&&!aer?'" + ZB + "':''}", "${(mat&&!aer)||S.mode==='table'?'" + ZB + "':''}")
sub1("""${peek?'':'<span class="stamp yes" aria-hidden="true">♥</span><span class="stamp no" aria-hidden="true">✕</span>'}</div>${r.her?""",
     """${peek||S.mode!=='table'?'':'<button type="button" class="xz" data-lbx="tv" aria-label="See the whole table full screen">⤢</button>""" + ZB + """'}${peek?'':'<span class="stamp yes" aria-hidden="true">♥</span><span class="stamp no" aria-hidden="true">✕</span>'}</div>${r.her?""")
# ⤢ in Table view = the whole table full screen
sub1("function openLbx(id){closeLbx();", "function openLbx(id){closeLbx();if(S.mode==='table'&&window.TVLBX&&TVLBX(id))return;")
# land on the table (not the controls) after each step
sub1("function jump(id){requestAnimationFrame(()=>{", "function jump(id){if(S.mode==='table'&&window.TVLAND&&TVLAND(id))return;requestAnimationFrame(()=>{")
# zoom survives a new tile set in Table view
sub1("dset:null,zs:{}});", "dset:null,zs:S.zs&&S.zs.tvz?{tvz:S.zs.tvz}:{}});")
# a mat / rack swapped in from the Table sheet becomes the current card, whatever the deck filters
sub1("function matDeck(){return INSF('m',matDeck0());}", "function matDeck(){const d=INSF('m',matDeck0());const f=S.tvforce;return f&&f===S.mfront&&S.mfset===S.set&&M[f]&&!S.seen[f]?[f,...d.filter(x=>x!==f)]:d;}")
sub1("function rackDeck(){return INSF('r',rackDeck0());}", "function rackDeck(){const d=INSF('r',rackDeck0());const f=S.tvrf;return f&&R[f]&&!R[f].hid&&!S.rseen[f]?[f,...d.filter(x=>x!==f)]:d;}")

j = h.rindex('</body>') if '</body>' in h else len(h)
h = h[:j] + inj + h[j:]
(OUT / 'index.html').write_text(h)
print('aerial refs', n, 'price ranges', pr, 'priced', {'mat': len(pm), 'tiles': len(pt), 'racks': len(price)}, 'cls', len(cls), 'usable racks', len(rk), 'backs', len(backs), 'priced racks', len(price), 'price chips', pr, 'index MB', round(len(h.encode()) / 1e6, 2))
