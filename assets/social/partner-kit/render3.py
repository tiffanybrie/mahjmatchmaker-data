"""Partner kit round 3 (Tiffany Oct 25 9:54pm): no MAHJMATCH code anywhere (cards say "Swipe for your own match"),
full brand names, phones only, 3 cards = 3 different tile sets + mats + racks from the brand's own line (FYM colour ranking, gen.js).
Three layout options for her pick: A 3-card fan, B phone swipe screen -> match card, C phone in front of 2 cards."""
import os, glob
from playwright.sync_api import sync_playwright
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
exec(open(D + '/render.py').read().split('with sync_playwright')[0])
HEAD = T.split('<div class="phone">')[0].replace('Find the perfect match for your<br>%(BRAND)s %(WHAT)s', '%(SUB)s')
CSS = '''<style>.card{position:absolute;border-radius:24px;box-shadow:0 26px 60px rgba(6,42,85,.28)}
.ph{position:absolute;width:430px;border-radius:64px;background:#151a22;padding:14px;box-shadow:0 30px 70px rgba(6,42,85,.35)}
.ph .scr{border-radius:52px;overflow:hidden;background:#fff}.ph img{width:100%;display:block}
.lab{position:absolute;font:700 30px Bit;color:#062a55;background:#fff;border-radius:40px;padding:10px 22px;box-shadow:0 10px 24px rgba(6,42,85,.18)}
.arr{position:absolute;font:400 90px Cap;color:#c8325f}</style>'''
TAIL = '<div class="foot">mahjmatchmaker.com/find-your-match</div></body></html>'
def page(brand, logo, sub, body):
    return HEAD % {'F': F, 'LOGO': trim(R + '/builder/logos/' + logo), 'SUB': sub} + CSS + body + TAIL
def build(slug, brand, logo):
    c = sorted(glob.glob(D + f'/samples/r3/{slug}-[0-9].jpg')); sw = D + f'/samples/r3/swipe-{slug}.png'
    sub = f'Mix and match {brand}<br>tiles, mats &amp; racks'
    A = ''.join(f'<img class="card" src="file://{f}" style="width:470px;left:{x}px;top:{y}px;transform:rotate({r}deg);z-index:{z}">'
                for f, (x, y, r, z) in zip(c, [(40, 860, -7, 1), (305, 800, 0, 2), (570, 860, 7, 1)]))
    B = (f'<div class="ph" style="left:70px;top:800px;transform:rotate(-3deg)"><div class="scr"><img src="file://{sw}"></div></div>'
         f'<img class="card" src="file://{c[0]}" style="width:440px;left:575px;top:900px;transform:rotate(4deg)">'
         '<div class="lab" style="left:380px;top:770px;z-index:3">Swipe &hearts;</div><div class="arr" style="left:500px;top:1180px;z-index:3">&rarr;</div>'
         '<div class="lab" style="left:640px;top:1700px;z-index:3">Your match card</div>')
    C = ''.join(f'<img class="card" src="file://{f}" style="width:430px;left:{x}px;top:{y}px;transform:rotate({r}deg)">' for f, (x, y, r) in zip(c[1:], [(40, 880, -8), (610, 880, 8)])) + \
        f'<div class="ph" style="left:310px;top:790px;z-index:2"><div class="scr"><img src="file://{sw}"></div></div>'
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for k, body in (('A-fan', A), ('B-phone-to-card', B), ('C-phone-front', C)):
            open(D + '/_r.html', 'w').write(page(brand, logo, sub, body)); pg.goto('file://' + D + '/_r.html'); pg.wait_for_timeout(1200); pg.screenshot(path=D + '/_r.png')
            o = D + f'/samples/out/{slug}-{k}.jpg'; Image.open(D + '/_r.png').convert('RGB').save(o, quality=92); out.append(o)
        b.close()
    for f in ['_r.html', '_r.png'] + [os.path.basename(x) for x in glob.glob(D + '/_logo_*')]: os.remove(D + '/' + f)
    return out
if __name__ == '__main__':
    o = build('mahjong-row-co', 'Mahjong Row &amp; Co.', 'n_mahjongrowco.png')
    ims = [Image.open(f).resize((540, 960)) for f in o]; s = Image.new('RGB', (1660, 980), 'white')
    [s.paste(im, (10 + i * 550, 10)) for i, im in enumerate(ims)]; s.save(D + '/samples/out/layouts-mahjong-row-co.jpg', quality=88); print(o)
