"""Partner kit, round 2 (Tiffany Oct 25: "a version that shows tiles and mats ... their tiles matched up, and one with just their tiles").
A) MATCHED: the brand's own tiles on its own mat + racks, as real FYM v91 match cards (only pairings Tiffany already matched).
B) TILES ONLY: the brand's tile sets screen in FYM. Same frame as render.py."""
import os, glob
from playwright.sync_api import sync_playwright
from PIL import Image
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'render.py')).read().split('with sync_playwright')[0])
CARD_T = T.split('<div class="phone">')[0].replace('Find the perfect match for your<br>%(BRAND)s %(WHAT)s', '%(SUB)s') + '''%(CARDS)s
<div class="h" style="left:70px;top:1150px;font-size:80px">&hearts;</div><div class="h" style="right:60px;top:1560px;font-size:64px;color:#c8325f">&hearts;</div>
<div class="foot">mahjmatchmaker.com/find-your-match</div></body></html>'''
CARD_T = CARD_T.replace('.h{', '.card{position:absolute;width:480px;border-radius:26px;box-shadow:0 26px 60px rgba(6,42,85,.28)}.h{')
def cards(files):
    if len(files) == 1:
        return f'<img class="card" src="file://{files[0]}" style="left:270px;top:800px;width:540px;transform:rotate(-2deg)">'
    pos = [(70, 860, -7), (300, 800, 0), (530, 860, 7)]
    return ''.join(f'<img class="card" src="file://{f}" style="left:{x}px;top:{y}px;transform:rotate({r}deg);z-index:{2 if r == 0 else 1}">' for f, (x, y, r) in zip(files, pos))
JOBS = [('mahjong-row-co-matched', 'Mahjong Row & Co.', 'n_mahjongrowco.png', 'Mahjong Row tiles, matched with<br>Mahjong Row mats &amp; racks', ['card-mrc-own.png', 'card-mrc-own2.png', 'card-mrc-own3.png']),
        ('bam-bird-boutique-matched', 'Bam Bird Boutique', 'n_bambirdboutique.png', 'Bam Bird tiles, matched with<br>Bam Bird mats &amp; racks', ['card-bam-own.png'])]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for slug, brand, logo, sub, fs in JOBS:
        html = CARD_T % {'F': F, 'LOGO': trim(R + '/builder/logos/' + logo), 'SUB': sub, 'CARDS': cards([D + '/samples/' + f for f in fs])}
        open(D + '/_r.html', 'w').write(html); pg.goto('file://' + D + '/_r.html'); pg.wait_for_timeout(1200); pg.screenshot(path=D + '/_r.png')
        Image.open(D + '/_r.png').convert('RGB').save(D + f'/samples/out/{slug}-story.jpg', quality=92); print(slug)
    html = T % {'F': F, 'LOGO': trim(R + '/builder/logos/n_bambirdboutique.png'), 'CAP': D + '/samples/cap-bam-tiles.png', 'BRAND': 'Bam Bird Boutique', 'WHAT': 'tiles'}
    open(D + '/_r.html', 'w').write(html); pg.goto('file://' + D + '/_r.html'); pg.wait_for_timeout(1200); pg.screenshot(path=D + '/_r.png')
    Image.open(D + '/_r.png').convert('RGB').save(D + '/samples/out/bam-bird-boutique-tiles-story.jpg', quality=92); print('bam tiles')
    b.close()
for f in ['_r.html', '_r.png'] + [os.path.basename(x) for x in glob.glob(D + '/_logo_*')]: os.remove(D + '/' + f)
