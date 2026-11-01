"""Find Your Mat-ch PREVIEW with Table view (Nov 1, Tiffany 5:47pm: a FULL app her husband can run start to finish; NOT the
website, NOT the live artifact). Takes the live artifact copy's index.html (pub112 = Version 1.12) and:
  1. adds 'Table' as the third option of the View switch (Up close / Aerial / Table); table mode reuses the Aerial layout,
  2. injects builder/table_view/preview_tv.js: every swipe card (mat deck, mat-door tile deck, rack deck) is redrawn as a
     top-down table (walls from config/tableview-back-colors.json ONLY, never the title color; coverage classes from
     config/tableview-photo-class-nov01.json; gray + reason when not usable), a Table bar (walls, players, tile faces, racks)
     and a whole-catalog rack picker (search name/brand/color/finish, brand, color, finish, price, in stock, fit by tile width),
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
def durl(p, px=160, alpha=False):
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
        bp = Image.open(R / v['sprite']).convert('RGBA'); bp = bp.crop(bp.split()[3].point(lambda x: 255 if x > 128 else 0).getbbox()); bp.thumbnail((160, 160))
        b = io.BytesIO(); bp.save(b, 'WEBP', quality=82); e['s'] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    backs[slug] = e
pcs = sorted(v[1] for v in price.values())
fr = lambda x: int(round(x / 5) * 5) if x < 100 else (int(round(x / 25) * 25) if x < 300 else int(round(x / 50) * 50))
pr = sorted(set(fr(pcs[int(len(pcs) * f)]) for f in (.2, .4, .6, .8))) if len(pcs) > 8 else []
TVD = dict(cls=cls, why=why, rk=rk, rkw=rkw, fin=fin, price=price, so=so, backs=backs, pr=pr)
css = """<style>/* Table view preview */
/* WebKit iPhone: the step nav (.stp, 289px) would not shrink and pushed the stars/account icons 10px off-screen (also in live 1.12) */
html,body{overflow-x:hidden}.top .stp{min-width:0;flex:1 1 auto;overflow:hidden}
.tvbar{margin:10px 0 4px;background:#fff;border:2px solid #f3e1e8;border-radius:16px;padding:10px 12px;display:flex;flex-direction:column;gap:8px;font:14px var(--body)}
.tvrow{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.tvrow b{color:var(--navy,#054689)}.tvl{color:var(--mute);font-size:13px}
.tvrn{font-weight:600;min-width:0;overflow-wrap:anywhere}
.tvseg{display:inline-flex;border:1px solid #ecd5df;border-radius:999px;overflow:hidden}.tvseg button{border:0;background:#fff;padding:6px 11px;font:600 13px var(--body);color:var(--mute);cursor:pointer}.tvseg button.on{background:var(--navy,#054689);color:#fff}
.tvchg,.tvauto{border:0;border-radius:999px;background:#c8325f;color:#fff;font:700 13px var(--body);padding:7px 12px;cursor:pointer}.tvauto{background:#fff;color:var(--navy,#054689);border:1px solid #ecd5df}
.tvhint{margin:0;font-size:12px;color:var(--mute)}
body.tvmode .scard .onmat{display:none}
.scard .ph img.tvimg{object-fit:contain}
.scard.tvoff .ph img{filter:grayscale(1) opacity(.5)}
.tvna{position:absolute;left:8px;right:8px;bottom:8px;z-index:3;background:rgba(255,255,255,.95);border-radius:10px;padding:6px 9px;font:600 12px/1.3 var(--body);color:#2a2036;pointer-events:none}
#tvsheet{position:fixed;inset:0;z-index:300;background:rgba(30,20,40,.4);display:flex;align-items:flex-end;justify-content:center}
#tvsheet[hidden]{display:none}
.tvs-in{background:#fff;width:min(560px,100%);max-height:86dvh;overflow:auto;overscroll-behavior:contain;border-radius:18px 18px 0 0;padding:12px max(14px,env(safe-area-inset-left,0px)) calc(16px + env(safe-area-inset-bottom,0px));display:flex;flex-direction:column;gap:9px;font:14px var(--body)}
.tvs-h{display:flex;justify-content:space-between;align-items:center}.tvs-h b{font:400 20px var(--display,serif);color:var(--navy,#054689)}.tvx{border:0;background:none;font-size:26px;color:var(--mute);cursor:pointer}
#tvq,#tvbrand{border:1px solid #ecd5df;border-radius:999px;padding:9px 13px;font:15px var(--body);background:#fff;width:100%}
.tvchips{display:flex;gap:6px;flex-wrap:wrap;align-items:center}.tvchips button{border:1px solid #ecd5df;background:#fff;border-radius:999px;padding:5px 10px;font:600 12px var(--body);cursor:pointer;text-transform:capitalize}.tvchips button.on{background:var(--navy,#054689);color:#fff;border-color:var(--navy,#054689)}
.tvst{font:600 12.5px var(--body);display:flex;gap:5px;align-items:center}
.tvact{background:#fbe3ec;border-radius:10px;padding:7px 10px;font-size:13px}.tvact button{border:0;background:#c8325f;color:#fff;border-radius:999px;padding:3px 10px;font:700 12px var(--body);margin-left:6px}
.tvgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:10px}
.tvit{border:0;background:none;padding:0;text-align:left;display:flex;flex-direction:column;gap:3px;cursor:pointer;min-width:0}
.tvit .ph{position:relative;aspect-ratio:2/1;border-radius:10px;background:#f6f1f4;display:flex;align-items:center;justify-content:center;border:2px solid transparent;overflow:hidden}
.tvit.on .ph{border-color:var(--navy,#054689)}.tvit .ph img{max-width:92%;max-height:86%;object-fit:contain}
.tvit .ph i{position:absolute;top:4px;right:6px;color:#c8325f;font-style:normal}.tvit .ph em{position:absolute;left:4px;right:4px;bottom:4px;background:rgba(255,255,255,.94);border-radius:6px;font:700 9.5px/1.2 var(--body);padding:2px 4px;font-style:normal}
.tvit.off .ph img{filter:grayscale(1) opacity(.45)}.tvit.off .nm,.tvit.off .bn{color:#b8adbf}
.tvit .nm{font:600 11.5px/1.2 var(--body);overflow-wrap:anywhere}.tvit .nm small{color:#c8325f;font-weight:700}.tvit .bn{font-size:10.5px;color:var(--mute)}
.tvit .pr{font:700 11.5px var(--body)}.tvit .pr em{display:block;font:italic 400 10px var(--body);color:#c8325f}
#tvtoast{position:fixed;left:50%;bottom:calc(24px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:#2a2036;color:#fff;border-radius:999px;padding:9px 15px;font:13px var(--body);z-index:400;max-width:calc(100vw - 32px)}
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
j = h.rindex('</body>') if '</body>' in h else len(h)
h = h[:j] + inj + h[j:]
(OUT / 'index.html').write_text(h)
print('aerial refs', n, 'cls', len(cls), 'usable racks', len(rk), 'backs', len(backs), 'priced racks', len(price), 'price chips', pr, 'index MB', round(len(h.encode()) / 1e6, 2))
