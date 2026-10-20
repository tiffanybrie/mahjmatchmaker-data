"""Oct 20 (Tiffany): ONE album cover style for the new era (the grid + site).
Every cover: white brand logo, ONE measured title size (names that don't fit wrap instead of shrinking),
flame-heart wordmark (holiday/ourlogo.png) + white letter-spaced FIND YOUR MATCH tagline (doc 52, no pink bar) in the same spot. Built from the existing cover:
its panel content is painted out, then logo + title + wordmark are redrawn through one template.
Non-OMM brand logos (Miss Mahjong, Mahjong Row & Co., Bam Bird, LoveShackFancy x OMM) are lifted from the
cover itself (they're already white). Writes to <outdir>; does NOT touch the live site covers.
Usage: python3 uniform_covers.py <outdir> key1 key2 ..."""
import sys, os, glob, json, subprocess, tempfile, numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import tagline_v2 as T
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'; C = R + 'scripts/covers/'; OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TITLE_PX = int(os.environ.get('TITLE_PX', 0)) or None
NAMES = {'sunday-tile-set': 'Sunday', 'glow-wild': 'Glow Wild', 'heritage-2-0': 'Heritage', 'la-fete': 'La Fête', 'lilac-soiree': 'Lilac Soirée', 'preppy-soiree': 'Preppy Soirée',
         'shangri-la': 'Shangri-La', 'palm-royale': 'Palm Royale', 'papaya-spritz': 'Papaya Spritz', 'spring-love': 'Spring Love', 'cypress-forest': 'Cypress'}
LIFT = {'malachite', 'jade', 'cypress-forest', 'tortoise', 'coquette'}   # keep their own (white) logo + subline
def src(k):
    if k == 'sunday-tile-set': return R + 'assets/cards/sunday-tile-set/00-sunday-tile-set-mahjong-tiles-cover.jpg'
    return [f for f in glob.glob(R + 'assets/covers/albums/*.jpg') if os.path.basename(f).split('-', 1)[1].startswith(k + '-mahjong-tiles')][0]
def title(k):
    n = NAMES.get(k, k.replace('-', ' ').title()); return (n, 'Tiles 2.0') if k == 'heritage-2-0' else ((n, 'Tile Set') if k == 'sunday-tile-set' else (n, 'Tiles'))
X0, X1, Y0, Y1 = 190, 890, 300, 1075
def masks(a):
    reg = a[Y0:Y1, X0:X1].astype(int); med = np.median(reg.reshape(-1, 3), axis=0)
    d = np.abs(reg - med).sum(axis=2); return med, d
def lift_logo(a):
    """white brand logo (+ its subline) above the title, lifted with a whiteness alpha"""
    xa, xb = 230, 850; reg = a[Y0:900, xa:xb].astype(int)
    wh = (reg.min(axis=2) > 185) & ((reg.max(axis=2) - reg.min(axis=2)) < 60)
    rows = wh.sum(axis=1) > 3; bl, s0 = [], None
    for i, r in enumerate(list(rows) + [False]):
        if r and s0 is None: s0 = i
        if not r and s0 is not None:
            if bl and s0 - bl[-1][1] < 10: bl[-1] = (bl[-1][0], i)
            else: bl.append((s0, i))
            s0 = None
    bl = [b for b in bl if b[1] - b[0] >= 10]
    logo = bl[:-2]                                   # last two blocks = "<Name>" / "Tiles"
    t, bt = logo[0][0] + Y0 - 4, logo[-1][1] + Y0 + 4
    sub = a[t:bt, xa:xb].astype(int); cols = np.nonzero(((sub.min(axis=2) > 185)).sum(axis=0) > 0)[0]
    l, r = cols.min() + xa - 4, cols.max() + xa + 4; sub = a[t:bt, l:r].astype(int)
    al = (np.clip((sub.min(axis=2) - 140) / 90, 0, 1) * 255).astype(np.uint8)
    im = Image.new('RGBA', (al.shape[1], al.shape[0]), (251, 246, 238, 255)); im.putalpha(Image.fromarray(al)); return im
VAULT = {'lilac-soiree', 'preppy-soiree', 'shangri-la', 'spring-love', 'sunday-tile-set'}
def wipe(a, d, k):
    mm = (d > 60).astype(np.uint8) * 255
    if k not in VAULT:
        for (xa, xb) in ((0, 352 - X0), (728 - X0, X1 - X0)): mm[990 - Y0:1040 - Y0, xa:xb] = 0
    m = np.zeros(a.shape[:2], np.uint8); m[Y0:Y1, X0:X1] = cv2.dilate(mm, np.ones((9, 9), np.uint8))
    # wide band in the middle (long old titles ran past the narrow box); frame corners are outside these rows
    reg = a[430:900, 105:975].astype(int); med = np.median(reg.reshape(-1, 3), axis=0)
    m2 = ((np.abs(reg - med).sum(axis=2) > 60).astype(np.uint8) * 255)
    m[430:900, 105:975] |= cv2.dilate(m2, np.ones((9, 9), np.uint8))
    if k == 'coquette':   # faint old logo tag behind the OMM logo
        reg = a[330:560, 300:780].astype(int); med = np.median(reg.reshape(-1, 3), axis=0)
        m[330:560, 300:780] |= cv2.dilate(((np.abs(reg - med).sum(axis=2) > 22).astype(np.uint8) * 255), np.ones((9, 9), np.uint8))
    out = cv2.inpaint(a, m, 13, cv2.INPAINT_TELEA)
    if k in VAULT:   # old vault wordmark crossed the frame lines: redraw the template frame on top
        im = Image.fromarray(out).convert('RGBA'); fr = Image.open(C + 'holiday/frame2.png').convert('RGBA').resize((906, 788)); im.alpha_composite(fr, (87, 281)); out = np.asarray(im.convert('RGB'))
    return out
NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
def shot(html, out):
    d = tempfile.mkdtemp(); hf = d + '/c.html'; open(hf, 'w').write(html)
    subprocess.run(['node', R + 'scripts/albumcard/shot.js', hf, out], check=True, env={**os.environ, 'NODE_PATH': NP}, stdout=subprocess.DEVNULL)
FONT = '<link href="https://fonts.googleapis.com/css2?family=Caprasimo&display=block" rel="stylesheet">'
MAXW = 720
if not TITLE_PX:   # measure: the biggest size where every single word fits the panel opening
    words = sorted({w for k in sys.argv[2:] for part in title(k) for w in part.split()}, key=len)
    hf = tempfile.mkdtemp() + '/m.html'
    open(hf, 'w').write(FONT + '<body>' + ''.join(f'<span style="font:400 100px Caprasimo;white-space:nowrap" class="w">{w}</span><br>' for w in words) +
        '<script>document.fonts.ready.then(()=>{document.title=Math.max(...[...document.querySelectorAll(".w")].map(e=>e.getBoundingClientRect().width))})</script>')
    js = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://%s');await p.waitForTimeout(1500);console.log(await p.title());await b.close()})()" % hf
    w = float(subprocess.run(['node', '-e', js], capture_output=True, text=True, env={**os.environ, 'NODE_PATH': NP}).stdout.strip())
    TITLE_PX = min(112, int(MAXW / w * 100)); print('title px', TITLE_PX)
WM, BAR = C + 'holiday/ourlogo.png', C + 'tagbar.png'
def whiten(img):   # pink OMM logo -> white, in place (textured panels we can't repaint)
    a = np.asarray(img.convert('RGB').resize((1080, 1350), Image.LANCZOS)).astype(float); hsv = cv2.cvtColor(a.astype(np.uint8), cv2.COLOR_RGB2HSV)
    t, b, l, r = 300, 560, 300, 780; reg = hsv[t:b, l:r]
    col = (reg[..., 1] > 90) & (((reg[..., 0] > 145) | (reg[..., 0] < 6)) | ((reg[..., 0] > 95) & (reg[..., 0] < 130)))
    if col.sum() < 500: return Image.fromarray(a.astype(np.uint8))
    ys, xs = np.nonzero(col); y0, y1, x0, x1 = ys.min() + t - 4, ys.max() + t + 5, xs.min() + l - 4, xs.max() + l + 5
    sub = hsv[y0:y1, x0:x1].astype(float); h = sub[..., 0]
    hue_ok = (((h > 140) & (sub[..., 2] > 140)) | ((h > 95) & (h < 130) & (sub[..., 2] > 110)))  # OMM pink + blue only (not the burl)
    al = (np.clip((sub[..., 1] - 50) / 70, 0, 1) * hue_ok)
    al = cv2.GaussianBlur(cv2.dilate(al.astype(np.float32), np.ones((3, 3), np.uint8)), (3, 3), 0)[..., None]
    a[y0:y1, x0:x1] = a[y0:y1, x0:x1] * (1 - al) + np.array([251, 246, 238]) * al
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
KEEP = {'cypress-forest', 'emerald', 'glow-wild', 'talulah', 'heritage', 'heritage-2-0'}   # photographic wood panel: inpainting smears it, so only the wordmark + tagline are swapped
for k in sys.argv[2:]:
    if k in KEEP:
        im0 = Image.open(src(k)); img = T.clean(whiten(im0) if k == 'heritage-2-0' else im0.convert('RGB').resize((1080, 1350), Image.LANCZOS)).convert('RGBA')
        wm = Image.open(WM).convert('RGBA'); w = 540; wm = wm.resize((w, int(wm.height * w / wm.width)), Image.LANCZOS)
        img.alpha_composite(wm, ((1080 - w) // 2, 942 - wm.height // 2)); t = T.tagline('FIND YOUR MATCH'); img.alpha_composite(t, ((1080 - t.width) // 2, 1012 - t.height // 2))
        img.convert('RGB').save(f'{OUT}/{k}.jpg', quality=94); print(k); continue
    a = np.asarray(Image.open(src(k)).convert('RGB').resize((1080, 1350), Image.LANCZOS)).copy()
    med, d = masks(a)
    tmp = tempfile.mkdtemp()
    if k == 'sunday-tile-set': logo = f'<img src="{C}holiday/sunday_white.png" style="display:block;height:120px">'
    elif k in LIFT: lift_logo(a).save(tmp + '/logo.png'); logo = f'<img src="{tmp}/logo.png" style="display:block;max-width:600px">'
    else: logo = f'<img src="{C}holiday/omm_white.png" style="display:block;height:160px">'
    Image.fromarray(wipe(a, d, k)).save(tmp + '/bg.png')
    n, t2 = title(k)
    html = f'''<html><head>{FONT}<style>
body{{margin:0;width:1080px;height:1350px;overflow:hidden;position:relative;background:url("{tmp}/bg.png")}}
.c{{position:absolute;left:87px;top:300px;height:600px;width:906px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:#fbf6ee;text-align:center}}
h1{{font:400 {TITLE_PX}px/1.0 Caprasimo;margin:14px 0 0;text-shadow:0 2px 8px rgba(0,0,0,.18);max-width:{MAXW}px}}
.wm{{position:absolute;left:50%;transform:translateX(-50%);top:915px;width:560px}} .bar{{position:absolute;left:50%;transform:translateX(-50%);top:1010px;width:380px}}
</style></head><body><div class="c">{logo}<h1 id="t">{n} {t2}</h1></div>
<script>/* wrap: "Name" on its own line(s), then "Tiles" */ const h=document.getElementById('t');h.innerHTML={json.dumps(n)}+'<br>'+{json.dumps(t2)};</script></body></html>'''
    o = f'{OUT}/{k}.jpg'; shot(html, o)
    img = Image.open(o).convert('RGBA'); wm = Image.open(WM).convert('RGBA'); w = 540; wm = wm.resize((w, int(wm.height * w / wm.width)), Image.LANCZOS)
    img.alpha_composite(wm, ((1080 - w) // 2, 942 - wm.height // 2)); t = T.tagline('FIND YOUR MATCH'); img.alpha_composite(t, ((1080 - t.width) // 2, 1012 - t.height // 2))
    img.convert('RGB').save(o, quality=94); print(k)
