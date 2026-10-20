"""Oct 20 noon (Tiffany: no Photoshop remnants). Uniform album covers, rebuilt CLEAN instead of erased:
the panel is repainted fresh (estimated panel colour at the template's .88 over a soft underlay), so nothing old shows through.
Kept from the original: the photo outside the panel, the white frame (incl. Coquette's bows) and the white non-OMM brand logos,
lifted with a whiteness alpha. Redrawn: white OMM logo, title at one size, flame-heart wordmark, FIND YOUR MATCH tagline.
Usage: python3 uniform_v2.py <outdir> key ..."""
import sys, os, glob, json, subprocess, tempfile, numpy as np, cv2
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import tagline_v2 as T
R = '/home/claude/mahjmatchmaker-data/'; C = R + 'scripts/covers/'; OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TITLE_PX = int(os.environ.get("TITLE_PX", 132)); A = .88   # measured: her originals "Tiles" line = 99px ink tall
PX0, PY0, PX1, PY1 = 87, 281, 993, 1069
NAMES = {'sunday-tile-set': 'Sunday', 'glow-wild': 'Glow Wild', 'heritage-2-0': 'Heritage', 'la-fete': 'La Fête', 'lilac-soiree': 'Lilac Soirée', 'preppy-soiree': 'Preppy Soirée',
         'shangri-la': 'Shangri-La', 'palm-royale': 'Palm Royale', 'papaya-spritz': 'Papaya Spritz', 'spring-love': 'Spring Love', 'cypress-forest': 'Cypress'}
LIFT = {'malachite', 'jade', 'tortoise', 'coquette'}
TEX = {'coquette', 'emerald', 'glow-wild', 'talulah', 'heritage', 'heritage-2-0', 'cypress-forest'}   # photo-textured panels: template frame, no lifting
PANEL = {'emerald': (18, 112, 78)}   # panel colour overrides (Emerald's old panel was a gem photo)
def src(k):
    if k == 'sunday-tile-set': return R + 'assets/cards/sunday-tile-set/00-sunday-tile-set-mahjong-tiles-cover.jpg'
    return [f for f in glob.glob(R + 'assets/covers/albums/*.jpg') if os.path.basename(f).split('-', 1)[1].startswith(k + '-mahjong-tiles')][0]
def title(k):
    n = NAMES.get(k, k.replace('-', ' ').title())
    return (n, 'Tiles 2.0') if k == 'heritage-2-0' else ((n, 'Tile Set') if k == 'sunday-tile-set' else (n, 'Tiles'))
REF = {'lum': 120}
def white_alpha(a):  # white ink -> alpha, relative to the panel colour (works on light panels too)
    a = a.astype(int); mn = a.min(axis=2); sat = a.max(axis=2) - mn
    base = REF['lum']; lo = min(base + 28, 215); hi = max(min(base + 85, 245), lo + 20)
    return (np.clip((mn - lo) / (hi - lo), 0, 1) * (sat < 70)).astype(float)
def panel_obs(a):  # median panel colour from the ring between the frame and the content
    a = a.astype(float); m = np.zeros((1350, 1080), bool); m[440:880, PX0 + 22:180] = True; m[440:880, 900:PX1 - 22] = True
    px = a[m]; lum = px.min(axis=1)
    keep = lum < np.percentile(lum, 70)       # drop frame lines / bows
    return np.median(px[keep], axis=0)
VAULT = {'lilac-soiree', 'preppy-soiree', 'shangri-la', 'spring-love', 'sunday-tile-set'}
def content_mask(k=''):
    if False:   # (bows dropped Oct 20) + swoosh lines whole; only the text area is repainted
        m = np.zeros((1350, 1080), bool); m[380:1000, 262:818] = True; m[905:985, 252:845] = True; m[990:1060, 345:735] = True; return m
    m = np.zeros((1350, 1080), bool); m[330:1000, 185:895] = True; m[990:1060, 345:735] = True
    if k != 'coquette': m[540:800, 140:945] = True   # Coquette's ribbon tails run down the sides
    if k in VAULT: m[960:1062, 150:930] = True
    return m
def lift_logo(a, y0=300):
    xa, xb = 230, 850; wh = white_alpha(a[y0:900, xa:xb]) > .5
    rows = wh.sum(axis=1) > 3; bl, s0 = [], None
    for i, r in enumerate(list(rows) + [False]):
        if r and s0 is None: s0 = i
        if not r and s0 is not None:
            if bl and s0 - bl[-1][1] < 10: bl[-1] = (bl[-1][0], i)
            else: bl.append((s0, i))
            s0 = None
    bl = [b for b in bl if b[1] - b[0] >= 10]; logo = bl[:-2]
    t, bt = logo[0][0] + y0 - 4, logo[-1][1] + y0 + 4
    al = white_alpha(a[t:bt, xa:xb]); cols = np.nonzero((al > .3).sum(axis=0))[0]; l, r = cols.min() - 4, cols.max() + 5
    al = al[:, max(l, 0):r]
    n, lab, st, _ = cv2.connectedComponentsWithStats((al > .2).astype(np.uint8))
    for i in range(1, n):   # drop thin decorative rules beside the logo (they read as leftover lines)
        x, y, w, h, area = st[i]
        if h <= 9 and w >= 35: al[lab == i] = 0
    im = Image.new('RGBA', (al.shape[1], al.shape[0]), (251, 246, 238, 255)); im.putalpha(Image.fromarray((al * 255).astype(np.uint8))); return im
def rebuild_panel(a, k):
    obs = panel_obs(a); a = a.astype(float); pan = a[PY0:PY1, PX0:PX1]
    wa = white_alpha(pan)
    # soft underlay: the photo around the panel, blurred into the panel area
    top = a[0:PY0, PX0:PX1]; bot = a[PY1:1350, PX0:PX1]
    stack = np.concatenate([top, top[::-1], top, top[::-1]], axis=0)[:PY1 - PY0]   # mirrored joins = no seams
    st = stack.astype(np.float32); bl = cv2.GaussianBlur(st, (0, 0), 14)
    wgt = np.zeros(st.shape[0], np.float32)
    for j in range(PY0 - 0, st.shape[0] + 1, PY0):     # soften every mirror join
        d = np.abs(np.arange(st.shape[0]) - j); wgt = np.maximum(wgt, np.clip(1 - d / 70, 0, 1))
    st = st * (1 - wgt[:, None, None]) + bl * wgt[:, None, None]
    under = a.copy(); under[PY0:PY1, PX0:PX1] = st
    um = np.median(under[PY0:PY1, PX0:PX1].reshape(-1, 3), axis=0)
    P = np.array(PANEL[k], float) if k in PANEL else np.clip((obs - (1 - A) * um) / A, 0, 255)
    out = a.copy(); out[PY0:PY1, PX0:PX1] = A * P + (1 - A) * under[PY0:PY1, PX0:PX1]
    # frame layer: white ink of the original panel OUTSIDE the content area (corners, border lines, bows)
    fr = wa.copy(); fr[content_mask(k)[PY0:PY1, PX0:PX1]] = 0
    fr[:] = 0   # Oct 20: never reuse the old frame pixels; the template frame is always drawn fresh
    out[PY0:PY1, PX0:PX1] = out[PY0:PY1, PX0:PX1] * (1 - fr[..., None]) + pan * fr[..., None]
    out = out.clip(0, 255).astype(np.uint8)
    if True:   # template frame drawn fresh on every cover crossed the frame lines: draw the template frame instead
        im = Image.fromarray(out).convert('RGBA'); im.alpha_composite(Image.open(C + 'holiday/frame3.png').convert('RGBA').resize((906, 788)), (87, 281)); out = np.asarray(im.convert('RGB'))
    return out
NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
FONT = '<link href="https://fonts.googleapis.com/css2?family=Caprasimo&display=block" rel="stylesheet">'
WM = C + 'holiday/ourlogo.png'
for k in sys.argv[2:]:
    a = np.asarray(Image.open(src(k)).convert('RGB').resize((1080, 1350), Image.LANCZOS)).copy(); tmp = tempfile.mkdtemp()
    REF['lum'] = float(panel_obs(a).min())
    if k == 'sunday-tile-set': logo = f'<img src="{C}holiday/sunday_white.png" style="display:block;height:150px">'
    elif k == 'cypress-forest': logo = f'<img src="{R}builder/logos/mahjongrowco_0.png" style="display:block;height:250px;margin:-30px 0 -20px">'
    elif k in LIFT: lift_logo(a, 395 if k == 'coquette' else 300).save(tmp + '/logo.png'); logo = f'<img src="{tmp}/logo.png" style="display:block;max-width:600px">'
    else: logo = f'<img src="{C}holiday/omm_white.png" style="display:block;height:160px">'
    Image.fromarray(rebuild_panel(a, k)).save(tmp + '/bg.png')
    n, t2 = title(k)
    from PIL import ImageFont
    three = ImageFont.truetype(R + 'scripts/social/tileprofile/fonts/Caprasimo.ttf', TITLE_PX).getlength(n) > 800
    if three: logo = logo.replace('height:160px', 'height:112px').replace('height:150px', 'height:110px')
    light = False   # Tiffany Oct 20: never drop shadows on cover text
    sh = '0 2px 3px rgba(40,30,30,.30),0 3px 14px rgba(40,30,30,.28)' if light else '0 2px 8px rgba(0,0,0,.18)'
    html = f'''<html><head>{FONT}<style>body{{margin:0;width:1080px;height:1350px;overflow:hidden;position:relative;background:url("{tmp}/bg.png")}}
.c{{position:absolute;left:87px;top:300px;height:600px;width:906px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:#fbf6ee;text-align:center}}
h1{{font:400 {TITLE_PX}px/1.0 Caprasimo;margin:14px 0 0;text-shadow:none;max-width:800px}} img{{filter:{'drop-shadow(0 2px 4px rgba(40,30,30,.30))' if light else 'none'}}}</style></head>
<body><div class="c">{logo}<h1>{n}<br>{t2}</h1></div></body></html>'''
    hf = tmp + '/c.html'; open(hf, 'w').write(html); o = f'{OUT}/{k}.jpg'
    subprocess.run(['node', R + 'scripts/albumcard/shot.js', hf, o], check=True, env={**os.environ, 'NODE_PATH': NP}, stdout=subprocess.DEVNULL)
    img = Image.open(o).convert('RGBA'); wm = Image.open(WM).convert('RGBA'); w = 540; wm = wm.resize((w, int(wm.height * w / wm.width)), Image.LANCZOS)
    t = T.tagline('FIND YOUR MATCH'); pos_w = ((1080 - w) // 2, 942 - wm.height // 2); pos_t = ((1080 - t.width) // 2, 1012 - t.height // 2)
    if light:   # soft dark shadow under the white wordmark + tagline
        from PIL import ImageFilter
        for lay, pos in ((wm, pos_w), (t, pos_t)):
            shd = Image.new('RGBA', lay.size, (40, 30, 30, 0)); shd.putalpha(lay.getchannel('A').point(lambda v: int(v * .45)))
            big = Image.new('RGBA', img.size, (0, 0, 0, 0)); big.alpha_composite(shd, (pos[0], pos[1] + 2)); img.alpha_composite(big.filter(ImageFilter.GaussianBlur(4)))
    img.alpha_composite(wm, pos_w); img.alpha_composite(t, pos_t)
    img.convert('RGB').save(o, quality=94); print(k)
