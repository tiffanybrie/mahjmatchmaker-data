import sys, os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
D = '/home/claude/fymapp'
tpl = open(D + '/story.html').read()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for name in sys.argv[1:]:
        h = tpl.replace('__SCR__', f'file://{D}/caps/{name}.png')
        open(D + '/_s.html', 'w').write(h)
        pg.goto('file://' + D + '/_s.html'); pg.wait_for_timeout(900)
        pg.screenshot(path=D + '/_s.png')
        im = Image.open(D + '/_s.png').convert('RGB')
        out = f'{D}/out/story-{name}.jpg'; os.makedirs(D + '/out', exist_ok=True)
        im.save(out, quality=92)
        g = im.copy(); d = ImageDraw.Draw(g)
        d.rectangle([0, 0, 1080, 269], outline='red', width=4); d.rectangle([0, 1690, 1080, 1920], outline='red', width=4)
        d.rectangle([40, 1240, 480, 1680], outline='blue', width=4)
        g.save(f'{D}/out/check-{name}.jpg', quality=70)
        print(out)
    b.close()
