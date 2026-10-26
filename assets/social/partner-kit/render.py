"""Partner launch kit samples (Tiffany Oct 25 8:28pm: show 3 first). One story per brand showing ONLY that brand's products,
captured from the current Find Your Mat-ch (artifact v91, local copy /home/claude/fymlive). Flat JPG 1080x1920."""
import os, sys
from playwright.sync_api import sync_playwright
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(D + '/../../..')
F = 'file://' + R + '/scripts/social/tileprofile/fonts/'
BRANDS = [('Charleston Mahjong Club', 'n_charlestonmahjongclub.png', 'samples/cap-cmc.png', 'mats'),
          ('Mahjong Row & Co.', 'n_mahjongrowco.png', 'samples/cap-mrc-tiles.png', 'tiles'),
          ('Bam Bird Boutique', 'n_bambirdboutique.png', 'samples/cap-bam-mats.png', 'mats')]
T = '''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Cap;src:url(%(F)sCaprasimo.ttf)}
@font-face{font-family:Bit;src:url(%(F)sbitter-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:PF;src:url(%(F)splayfair-display-latin-400-italic.woff2);font-style:italic}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1920px;background:#faf3ea;position:relative;overflow:hidden;font-family:Bit}
.c{position:absolute;left:0;right:0;text-align:center}
.blob{position:absolute;border-radius:50%%;background:#fbe3ea;width:980px;height:980px;left:50px;top:700px}
.logo{position:absolute;left:240px;top:230px;width:600px;height:200px;display:flex;align-items:center;justify-content:center}
.logo img{width:100%%;height:100%%;object-fit:contain}
.pill{display:inline-block;background:#062a55;color:#fff;font:700 34px Bit;letter-spacing:6px;padding:14px 36px;border-radius:50px}
.t{font-family:Cap;color:#062a55;font-size:96px;line-height:1}
.sub{font:italic 46px/1.25 PF;color:#c8325f}
.phone{position:absolute;left:225px;top:820px;width:630px;border-radius:72px;background:#151a22;padding:17px;box-shadow:0 30px 70px rgba(6,42,85,.3);transform:rotate(-2deg)}
.phone .scr{border-radius:56px;overflow:hidden;background:#fff;height:860px}.phone img{width:100%%;display:block}
.foot{position:absolute;left:0;right:0;top:1770px;text-align:center;font:700 38px Bit;color:#062a55}
.h{position:absolute;color:#f56c8c}
</style></head><body><div class="blob"></div>
<div class="logo"><img src="file://%(LOGO)s"></div>
<div class="c" style="top:455px"><span class="pill">NOW IN</span></div>
<div class="c t" style="top:520px">Find Your Mat-ch&trade;</div>
<div class="c sub" style="top:650px">Find the perfect match for your<br>%(BRAND)s %(WHAT)s</div>
<div class="phone"><div class="scr"><img src="file://%(CAP)s"></div></div>
<div class="h" style="left:90px;top:1100px;font-size:80px">&hearts;</div><div class="h" style="right:80px;top:1500px;font-size:64px;color:#c8325f">&hearts;</div>
<div class="foot">mahjmatchmaker.com/find-your-match</div>
</body></html>'''
os.makedirs(D + '/samples/out', exist_ok=True)
from PIL import ImageChops
def trim(path):
    im = Image.open(path).convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 0))
    a = im.split()[3].point(lambda v: 255 if v > 10 else 0)
    w = Image.new('RGBA', im.size, (255, 255, 255, 255)); flat = Image.alpha_composite(w, im).convert('RGB')
    nonwhite = ImageChops.difference(flat, Image.new('RGB', im.size, (255, 255, 255))).convert('L').point(lambda v: 255 if v > 18 else 0)
    box = ImageChops.multiply(a, nonwhite).getbbox() or im.getbbox()
    out = D + '/_logo_' + os.path.basename(path); im.crop(box).save(out); return out
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for brand, logo, cap, what in BRANDS:
        html = T % {'F': F, 'LOGO': trim(R + '/builder/logos/' + logo), 'CAP': D + '/' + cap, 'BRAND': brand, 'WHAT': what}
        open(D + '/_r.html', 'w').write(html); pg.goto('file://' + D + '/_r.html'); pg.wait_for_timeout(900)
        pg.screenshot(path=D + '/_r.png')
        out = D + '/samples/out/' + brand.lower().replace(' & ', '-').replace(' ', '-').replace('.', '') + '-story.jpg'
        Image.open(D + '/_r.png').convert('RGB').save(out, quality=92); print(out)
    b.close()
import glob
for f in ['_r.html', '_r.png'] + [os.path.basename(x) for x in glob.glob(D + '/_logo_*')]: os.remove(D + '/' + f)
