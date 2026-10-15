"""Holiday album covers, round 3 (Tiffany, Oct 15 review of gen2.py round 2).
Her notes: use style B (candy-stripe border + gold chinoiserie corners) but REMOVE the bow; the "J" in "Jolly" is
warped on all three Holly Jolly covers; backgrounds must be tile PILE shots with the tiles clearly visible
(Sugarplum Pink is the model); Grinch Green: tiles couldn't be seen and the translucent rectangle muddied it;
Tinselle Emerald: remove the background and fill the frame with tiles. All 11 covers back so she can pick a top 3.

- J fix: Caprasimo's J has a pinched, lumpy hook that reads as warped at 110px. Every "J" in a title is set in
  Bagel Fat One (same soft heavy weight, clean hook); the rest of the title stays Caprasimo.
- Backgrounds: built by bg() below from assets/covers/holiday/bg_src/ (brand photos):
  * Bam! has no pile shot of Rudolph Red or Grinch Green (product page checked Oct 15: 16 images; only Sugarplum Pink
    has a pile). Red = Bam!'s scattered-tiles shot (default) + an alt built like Green. Green = Bam!'s grid photo,
    zoomed so the tile rows fill the bands above and below the panel ("wall" fill), and a more opaque panel.
  * Virora 3x3 photos: white studio background trimmed off so the tiles fill the frame.
Usage: python3 gen3.py <outdir> [set ...]   -> <outdir>/<set>.jpg (1080x1350); also writes assets/covers/holiday/."""
import os, sys, subprocess, re, shutil
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(H + '/../../..') + '/'
SRC = R + 'assets/covers/holiday/bg_src/'; BG = R + 'assets/covers/holiday/bg/'; LOGO = R + 'assets/brand/partner-logos/'
W, HH = 1080, 1350
# id, title, colourway, logo, logo height, panel rgb, bg position, bg size, panel alpha, bg recipe
SETS = [
 ('dear-santa', 'Dear Santa', '', 'ar', 130, '23,87,58', '50% 50%', 'cover', .88, ('copy', 'dear-santa')),
 ('rackin-rudolph', "Rackin'<br>Rudolph", '', 'hiphip', 120, '163,25,46', '60% 40%', 'cover', .88, ('copy', 'rackin-rudolph')),
 ('holly-jolly-red', 'Holly Jolly', 'Rudolph Red', 'bam', 110, '206,32,41', '50% 50%', 'cover', .88, ('copy', 'holly-jolly-red')),
 ('holly-jolly-red-alt', 'Holly Jolly', 'Rudolph Red', 'bam', 110, '206,32,41', '50% 50%', 'cover', .94, ('wall', 'holly-jolly-red-grid', (84, 246, 846, 842))),
 ('holly-jolly-green', 'Holly Jolly', 'Grinch Green', 'bam', 110, '30,128,52', '50% 50%', 'cover', .94, ('wall', 'holly-jolly-green', (64, 244, 862, 880))),
 ('holly-jolly-pink', 'Holly Jolly', 'Sugarplum Pink', 'bam', 110, '226,128,160', '50% 50%', 'cover', .88, ('copy', 'holly-jolly-pink')),
 ('tinselle-emerald', 'Tinselle', 'Emerald Green', 'virora', 66, '14,98,60', '50% 50%', 'cover', .88, ('crop', 'tinselle-emerald', (0, 0, 1118, 1555))),
 ('tinselle-ruby', 'Tinselle', 'Ruby Red', 'virora', 66, '150,18,36', '50% 50%', 'cover', .88, ('crop', 'tinselle-ruby', (0, 0, 1104, 1540))),
 ('nivalee-blue', 'Nivalee', 'Glacier Blue', 'virora', 66, '58,165,168', '50% 50%', 'cover', .88, ('crop', 'nivalee-blue', (0, 0, 1104, 1530))),
 ('nutcracker-ballet', 'Nutcracker<br>Ballet', '', 'squad', 110, '214,120,140', '50% 50%', 'cover', .88, ('copy', 'nutcracker-ballet')),
 ('december-1994', 'December<br>1994', '', 'sunday', 84, '120,26,38', '45% 4%', 'auto 128%', .88, ('copy', 'december-1994')),
 ('cmc-apres-ski', 'Après Ski<br>Club', '', 'cmc', 130, '24,120,140', '50% 50%', 'cover', .88, ('copy', 'cmc-apres-ski')),
]
def bg(recipe, out):
    kind, name = recipe[0], recipe[1]; im = Image.open(SRC + name + '.jpg').convert('RGB')
    if kind == 'crop': im = im.crop(recipe[2])
    elif kind == 'wall':
        # Bam! grid photo (900x1200): recipe[2] = the tile block incl. the wall of backs. Zoom it to the card width;
        # the top band shows the top rows, the bottom band the bottom rows (the panel covers the middle).
        blk = im.crop(recipe[2]); blk = blk.resize((W, round(W * blk.height / blk.width)), Image.LANCZOS)
        off = HH - blk.height; a = Image.new('RGB', (W, HH)); a.paste(blk, (0, 0)); b = Image.new('RGB', (W, HH)); b.paste(blk, (0, off))
        seam, fz = HH // 2, 40  # the join sits under the panel; only the 73px side strips cross it, so feather it there
        m = Image.linear_gradient('L').resize((W, 2 * fz)); mask = Image.new('L', (W, HH), 0); mask.paste(255, (0, seam + fz, W, HH)); mask.paste(m, (0, seam - fz))
        im = Image.composite(b, a, mask)
    im.save(out, quality=92)
FONT = '<link href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Bagel+Fat+One&family=Montserrat:wght@700&display=block" rel="stylesheet">'
def page(s):
    i, t, cw, lg, lh, rgb, foc, sz, alpha = s[:9]
    fs = 104 if '<br>' in t else 118
    t = re.sub(r'J', '<span class="j">J</span>', t)
    return f'''<html><head>{FONT}<style>
body{{margin:0;width:{W}px;height:{HH}px;overflow:hidden;background:#000;position:relative}}
.bg{{position:absolute;inset:0;background:url("{BG}{i}.jpg") {foc}/{sz} no-repeat}}
.p{{position:absolute;left:87px;top:281px;width:906px;height:788px;background:rgba({rgb},{alpha})}}
.f{{position:absolute;left:87px;top:281px;width:906px;height:788px;background:url({H}/frame2_gold.png)}}
.c{{position:absolute;left:87px;top:300px;width:906px;height:620px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;color:#fbf6ee;text-align:center}}
.tag{{background:#fbf6ee;border-radius:14px;padding:12px 22px;box-shadow:0 4px 14px rgba(0,0,0,.25);display:flex;align-items:center;justify-content:center}}
.tag img{{display:block}}
h1{{font:400 {fs}px/1.02 Caprasimo;margin:10px 0 0;text-shadow:0 2px 8px rgba(0,0,0,.18)}}
h1 .j{{font-family:'Bagel Fat One';font-size:1.0em;margin-right:.02em}}
.cw{{font:700 30px Montserrat;letter-spacing:.3em;margin-left:.3em;margin-top:4px}}
.our{{position:absolute;left:50%;transform:translateX(-50%);top:950px;width:500px}}
.stripe{{position:absolute;left:73px;top:267px;width:906px;height:788px;border:14px solid transparent;border-image:repeating-linear-gradient(45deg,#fbf6ee 0 12px,#c8102e 12px 24px) 14}}
.p,.f,.c,.our,.stripe{{z-index:1}}
</style></head><body><div class="bg"></div><div class="stripe"></div><div class="p"></div><div class="f"></div>
<div class="c"><div class="tag"><img src="{LOGO}{lg}.png" style="height:{lh}px"></div><h1>{t}<br>Tiles</h1>{f'<div class="cw">{cw.upper()}</div>' if cw else ''}</div>
<img class="our" src="{H}/ourlogo.png"></body></html>'''
if __name__ == '__main__':
    out = sys.argv[1]; only = set(sys.argv[2:]); os.makedirs(out + '/html', exist_ok=True); os.makedirs(BG, exist_ok=True)
    jobs = []
    for s in SETS:
        if only and s[0] not in only: continue
        bg(s[9], BG + s[0] + '.jpg')
        hf = f'{out}/html/{s[0]}.html'; open(hf, 'w').write(page(s)); jobs += [hf, f'{out}/{s[0]}.png']
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:%d,height:%d}});"
          "const a=process.argv.slice(2);for(let k=0;k<a.length;k+=2){await p.goto('file://'+a[k]);await p.evaluate(()=>document.fonts.ready);"
          "await p.waitForTimeout(700);await p.screenshot({path:a[k+1]});}await b.close()})();") % (W, HH)
    open(out + '/html/shot.js', 'w').write(js)
    NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
    subprocess.run(['node', out + '/html/shot.js'] + jobs, check=True, env={**os.environ, 'NODE_PATH': NP})
    os.makedirs(R + 'assets/covers/holiday', exist_ok=True)
    for k in range(1, len(jobs), 2):
        p = jobs[k]; j = p[:-4] + '.jpg'; Image.open(p).convert('RGB').save(j, quality=90); os.remove(p)
        shutil.copy(j, R + 'assets/covers/holiday/' + os.path.basename(j))
    print(len(jobs) // 2, 'covers ->', out)
