"""Thu Nov 5 carousel finals: hook slide (1) + 7 Dear Santa x Anders Ruff album cards (her live-page order) + Find Your Mat-ch CTA (9),
story frames come from build_stories.py. Fonts: scripts/social/tileprofile/fonts. Run from the repo root."""
import os, shutil
from playwright.sync_api import sync_playwright
R = '/home/claude/mahjmatchmaker-data'; O = f'{R}/assets/social/week-2026-11-02/final/thu-ds'
F = f'file://{R}/scripts/social/tileprofile/fonts'
CARDS = [f'{R}/assets/cards/holiday-v4/dear-santa-mahjong-tiles-anders-ruff-{m}-mat.jpg' for m in
         ['candy-cane-lane', 'classic-very-merry-mahj', 'evergreen-tartan', 'santa-s-mahjong-mail', 'tartan-tidings', 'tartan-toile-no-l', 'watercolor-christmas-tree']]
FYM = '/dev/shm/weekdrafts/fym-ds-ccl.jpg'
CSS = f"""@font-face{{font-family:Cap;src:url({F}/Caprasimo.ttf)}}@font-face{{font-family:Bit;src:url({F}/bitter-latin-600-normal.woff2);font-weight:600}}
@font-face{{font-family:Bit;src:url({F}/bitter-latin-700-normal.woff2);font-weight:700}}@font-face{{font-family:PF;src:url({F}/playfair-display-latin-600-italic.woff2);font-style:italic}}
*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1350px;background:#faf3ea;font-family:Bit;color:#062a55;position:relative;overflow:hidden}}
.c{{position:absolute;left:0;right:0;text-align:center}}"""
HOOK = f"""<style>{CSS}</style>
<div class=c style="top:170px;font:400 150px/1 Cap;color:#a3192e">Dear Santa,</div>
<div class=c style="top:350px;font:400 84px/1.15 Cap">all I want is…<br>all of them</div>
<div class=c style="top:620px"><span style="display:inline-block;background:#1f5a3c;color:#fff;font:700 40px/1 Bit;letter-spacing:5px;padding:20px 40px;border-radius:60px">ANDERS RUFF</span></div>
<div class=c style="top:740px;font:600 50px/1.35 Bit">Dear Santa tiles on 7 of their<br>Christmas mats, in my order</div>
<div class=c style="top:960px;font:700 44px/1 Bit;color:#a3192e">Swipe ›</div>
<div class=c style="top:1150px;font:600 34px/1 Bit;color:#5d6f88">mahjmatchmaker.com</div>"""
CTA = f"""<style>{CSS}.ph{{position:absolute;left:330px;top:300px;width:420px;height:909px;border-radius:56px;background:#062a55;padding:16px}}
.ph img{{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:42px;display:block}}</style>
<div class=c style="top:70px;font:400 92px/1 Cap">Find <span style="font:italic 600 96px/1 PF;color:#d6336c">Your</span> Mat-ch<span style="font:400 40px Bit;vertical-align:top">™</span></div>
<div class=c style="top:190px;font:600 44px/1 Bit">Swipe them all yourself</div>
<div class=ph><img src="file://{FYM}"></div>
<div class=c style="top:1245px;font:700 40px/1 Bit;color:#a3192e">Code MAHJMATCH · mahjmatchmaker.com</div>"""
def story(pg, src, out):
    pg.set_viewport_size({'width': 1080, 'height': 1920})
    open('/dev/shm/weekdrafts/_s.html','w').write(f'<style>*{{margin:0}}body{{width:1080px;height:1920px;background:#faf3ea;display:flex;align-items:center;justify-content:center}}img{{width:1080px;height:1350px;display:block}}</style><img src="file://{src}">'); pg.goto('file:///dev/shm/weekdrafts/_s.html')
    pg.wait_for_timeout(400); pg.screenshot(path=out, type='jpeg', quality=92)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for n, html in [(1, HOOK), (9, CTA)]:
        pg.set_viewport_size({'width': 1080, 'height': 1350}); open('/dev/shm/weekdrafts/_p.html','w').write('<meta charset=utf-8>'+html); pg.goto('file:///dev/shm/weekdrafts/_p.html'); pg.wait_for_timeout(1200)
        pg.screenshot(path=f'{O}/slide{n}.jpg', type='jpeg', quality=93)
    for i, c in enumerate(CARDS, 2): shutil.copy(c, f'{O}/slide{i}.jpg')
    b.close()
print('ok')
