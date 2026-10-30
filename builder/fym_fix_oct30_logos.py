"""FYM v104 (Version 1.8): tiles-door opening view = PARTNER BRAND LOGOS (Tiffany Oct 29 3:29/3:31/3:33pm, Oct 30 2:49am).

- No colour picked, no brand, no search -> brand logo tiles instead of the alphabetical tile-set grid
  (it opened on Mahj Mood "90s Pool Party" + YMI "Aloha"). Partners first (OMM, then by 30-day commission,
  config/fym-brand-logo-order.json), each with a pink "Save with MAHJMATCH" tag; non-partners last in their own
  smaller group ("More brands · no discount").
- Tap a logo = that brand's sets (same state as the Shop by brand dropdown, so they stay in sync) + "All brands" back.
- Tap a colour = that colour's sets, partners first, non-partners last. Clear the colour = logos again.
- "Pick your tiles: tap a brand, a colour, or search your set" line; the search box stays right above the logos.
- Logos: the brand logos already in the app, trimmed + fitted to the same box so small ones (Britt Mills, YMI) read;
  missing ones added from the brands' own sites / our partner-logo files (Virora, Sunday, Royal Mahjong Society,
  Tala: its pale-yellow logo is darkened to a deeper gold so it shows on white).

usage: python3 builder/fym_fix_oct30_logos.py <src build dir (b103)> <out build dir (b104)>
Out dir = hardlinks of every src file + a patched index.html.
"""
import sys, os, re, io, json, base64, glob, shutil
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(SRC):
    if f == 'index.html': continue
    d, sf = os.path.join(OUT, f), os.path.join(SRC, f)
    if os.path.exists(d): continue
    if os.path.isdir(sf): shutil.copytree(sf, d, copy_function=os.link)
    else: os.link(sf, d)
h = open(os.path.join(SRC, 'index.html')).read()

def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c == n, (c, a[:90])
    h = h.replace(a, b)

# ---------- 1. version
rep('<title>Find Your Mat-ch (Version 1.7)</title>', '<title>Find Your Mat-ch (Version 1.8)</title>')
rep('color:var(--mute)">Version 1.7</small>', 'color:var(--mute)">Version 1.8</small>')

# ---------- 2. logo images (trimmed + fitted)
i = h.find('const D=') + 8
D, _ = json.JSONDecoder().raw_decode(h, i)
srcs = {}
for f in [os.path.join(SRC, 'index.html')] + sorted(glob.glob(os.path.join(SRC, '*.js'))):
    t = h if f.endswith('index.html') else open(f).read()
    for k in set(D['logos'].values()):
        if k in srcs: continue
        m = re.search('"' + re.escape(k) + r'":"(data:image/[a-z]+;base64,[A-Za-z0-9+/=]+)"', t)
        if m: srcs[k] = m.group(1)
FILES = {  # brands with no logo in the app yet
    'Virora Mahjong': 'assets/brand/partner-logos/virora.png',
    'Sunday Mahjong': 'assets/brand/partner-logos/sunday.png',
    'Royal Mahjong Society': 'assets/brand/fym-logo-src/royal-mahjong-society.png',   # theroyalmahjongsociety.com header logo
    'Tala Mahj': 'assets/brand/fym-logo-src/tala-mahj.png',                           # talamahj.com header logo
}
RECOLOR = {'Tala Mahj': (176, 140, 40)}  # pale #fbe98f on white is invisible -> deeper gold, same shape
BOX = (360, 150)

def tile(im, rgb=None):
    im = im.convert('RGBA')
    if rgb:
        a = im.getchannel('A'); im = Image.new('RGBA', im.size, rgb + (255,)); im.putalpha(a)
    px = im.load(); W, H = im.size
    # content = visible and not near-white
    xs, ys = [], []
    for y in range(0, H):
        for x in range(0, W):
            r, g, b, a = px[x, y]
            if a > 24 and not (r > 240 and g > 240 and b > 240):
                xs.append(x); ys.append(y)
    if xs: im = im.crop((min(xs), min(ys), max(xs) + 1, max(ys) + 1))
    s = min(BOX[0] / im.width, BOX[1] / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    o = io.BytesIO(); im.save(o, 'WEBP', quality=88, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(o.getvalue()).decode(), im

makers = sorted({s['maker'] for s in D['sets']})
BL, prev = {}, {}
for mk in makers:
    if mk in FILES:
        im = Image.open(REPO + FILES[mk])
    elif mk in D['logos'] and D['logos'][mk] in srcs:
        im = Image.open(io.BytesIO(base64.b64decode(srcs[D['logos'][mk]].split(',', 1)[1])))
    else:
        continue
    uri, pim = tile(im, RECOLOR.get(mk))
    BL[mk] = uri; prev[mk] = pim
# contact sheet for eyes (scratch, not shipped)
sheet = os.environ.get('LOGO_SHEET')
if sheet:
    cols = 4; cw, ch = 400, 210
    rows = (len(prev) + cols - 1) // cols
    S = Image.new('RGB', (cols * cw, rows * ch), 'white')
    from PIL import ImageDraw
    dr = ImageDraw.Draw(S)
    for n, (mk, im) in enumerate(sorted(prev.items())):
        x, y = (n % cols) * cw, (n // cols) * ch
        dr.rectangle([x + 8, y + 8, x + cw - 8, y + ch - 30], outline=(230, 200, 210))
        S.paste(im, (x + (cw - im.width) // 2, y + 12 + (BOX[1] - im.height) // 2), im)
        dr.text((x + 12, y + ch - 24), mk, fill=(40, 40, 60))
    S.save(sheet)
order = json.load(open(REPO + 'config/fym-brand-logo-order.json'))['order']
JS_BL = 'const BLOGO=' + json.dumps(BL, ensure_ascii=False) + ';const BLORD=' + json.dumps(order, ensure_ascii=False) + ';\n'

# ---------- 3. CSS
CSS = '''.blv{grid-column:1/-1;margin:2px 0 6px}.blv .blq{text-align:center;font:600 13.5px/1.35 var(--body);color:var(--navy);margin:2px 4px 10px}
.blh{font:800 11.5px var(--body);letter-spacing:.1em;text-transform:uppercase;color:#c8325f;margin:4px 2px 8px;text-align:center}.blh.np{color:var(--mute);margin-top:18px}
.blgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}@media (min-width:700px){.blgrid{grid-template-columns:repeat(4,minmax(0,1fr))}}@media (min-width:1000px){.blgrid{grid-template-columns:repeat(5,minmax(0,1fr))}}
.blg{background:#fff;border:1.5px solid #f2d3de;border-radius:16px;padding:10px 7px 9px;display:flex;flex-direction:column;align-items:center;gap:3px;cursor:pointer;font:inherit;color:inherit;box-shadow:0 2px 8px rgba(163,40,90,.06);transition:transform .12s,border-color .12s}.blg:hover{border-color:#c8325f;transform:translateY(-1px)}
.blg .bli{width:100%;aspect-ratio:12/5;display:flex;align-items:center;justify-content:center}.blg .bli img{max-width:100%;max-height:100%;object-fit:contain}
.blg .blt{font:700 italic 14px/1.15 'Playfair Display',Georgia,serif;color:var(--navy);text-align:center}
.blg b{font:700 12px/1.2 var(--body);color:var(--navy);text-align:center}.blg small{font:500 11px var(--body);color:var(--mute)}
.blg em{font:800 9.5px var(--body);font-style:normal;letter-spacing:.03em;color:#fff;background:#c8325f;border-radius:999px;padding:2px 7px;margin-top:2px;white-space:nowrap}
.blgrid.np .blg{border-color:#ece6ea;box-shadow:none;padding:7px 6px}.blgrid.np .blg .bli{aspect-ratio:3/1;opacity:.92}
.tgrid .blg .bli{height:62px;aspect-ratio:auto;width:100%}.tgrid .blgrid.np .blg .bli{height:44px}@media (min-width:700px){.tgrid .blg .bli{height:72px}}
.tgrid .blg .bli img{width:auto;height:auto;max-width:100%;max-height:100%;aspect-ratio:auto;border-radius:0;object-fit:contain}
.tgrid .blg{border:1.5px solid #f2d3de;padding:10px 7px 9px;justify-content:flex-start}.tgrid .blgrid.np .blg{border-color:#ece6ea;padding:7px 6px}
.tgrid .blg b{font:700 12px/1.2 var(--body)}.tgrid .blg small{font:500 10.5px var(--body)}
.tgrid .blg em{font:800 9px/1.25 var(--body);font-style:normal;letter-spacing:0;white-space:normal;text-align:center;max-width:100%;margin-top:auto;padding:3px 9px;align-self:center}
.blback{grid-column:1/-1;justify-self:start;border:1.5px solid #c8325f;border-radius:999px;background:#fff;color:#c8325f;font:700 12.5px var(--body);padding:4px 12px;cursor:pointer;margin:0 0 4px}
'''
k = h.rindex('</style></head>'); h = h[:k] + CSS + h[k:]

# ---------- 4. JS: logo view, default = logos, colour results partners first, logo tap = brand
rep('function brandMenu(){', JS_BL + '''const BPA=m=>!!BCODE[m];
function blogoView(){const all=D.sets.filter(VIS),n={};all.forEach(s=>{n[s.maker]=(n[s.maker]||0)+1;});const ix=m=>{const k=BLORD.indexOf(m);return k<0?1e3-n[m]:k;};
 const B=Object.keys(n).sort((a,b)=>ix(a)-ix(b)||a.localeCompare(b)),P=B.filter(BPA),NP=B.filter(m=>!BPA(m));
 const one=m=>`<button type="button" class="blg" data-blogo="${esc(m)}" aria-label="${esc(m)}: ${n[m]} tile sets"><span class="bli">${BLOGO[m]?`<img src="${BLOGO[m]}" alt="" loading="lazy">`:`<span class="blt">${esc(m)}</span>`}</span><b>${esc(m)}</b><small>${n[m]} tile set${n[m]>1?'s':''}</small>${BPA(m)?'<em>Save with MAHJMATCH</em>':''}</button>`;
 return `<div class="blv" id="blv"><p class="blq">Pick your tiles: tap a brand, a colour, or search your set</p><h4 class="blh">Partner brands \\u00b7 save 10% or more with code MAHJMATCH</h4><div class="blgrid">${P.map(one).join('')}</div>${NP.length?`<h4 class="blh np">More brands \\u00b7 no discount</h4><div class="blgrid np">${NP.map(one).join('')}</div>`:''}</div>`;}
function brandMenu(){''')
rep("if(S.tbrand)return all.filter(x=>x[0].maker===S.tbrand)",
    "if(S.tbrand)return '<button type=\"button\" class=\"blback\" data-blogo=\"\">\\u2039 All brands</button>'+all.filter(x=>x[0].maker===S.tbrand)")
rep(" if(S.tcol==='az'||S.tcol==='')return all.sort(",
    " if(S.tcol==='')return blogoView();/* v104: no colour picked = partner brand logos (Tiffany Oct 29 3:31pm) */\n if(S.tcol==='az')return all.sort(")
rep("return (BACKG[S.tcol]||[]).flatMap(n=>all.filter(x=>x[0].name===n)).sort((a,b)=>!!T[a[0].tile].soon-!!T[b[0].tile].soon)",
    "return (BACKG[S.tcol]||[]).flatMap(n=>all.filter(x=>x[0].name===n)).sort((a,b)=>(BPA(a[0].maker)?0:1)-(BPA(b[0].maker)?0:1)||!!T[a[0].tile].soon-!!T[b[0].tile].soon)/* v104: partners first, non-partners last */")
rep("if(b=q('[data-tcol]')){",
    "if(b=q('[data-blogo]')){S.tbrand=b.dataset.blogo;S.tcol='';renderTiles();const g=$(S.tbrand?'tgrid':'tbr');if(g)g.scrollIntoView({block:'start',behavior:'smooth'});trk('brand',{x:S.tbrand||'all',via:'logo'});return;}\n  if(b=q('[data-tcol]')){")

open(os.path.join(OUT, 'index.html'), 'w').write(h)
print('ok', len(h), 'logos', len(BL), 'missing', [m for m in makers if m not in BL])
