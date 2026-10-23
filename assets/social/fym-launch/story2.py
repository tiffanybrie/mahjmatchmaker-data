import os
from playwright.sync_api import sync_playwright
from PIL import Image
D = '/home/claude/fymapp'
tpl = open(D + '/story2.html').read()
V = {
 'cypress-huntclub': f'<div class="phone" id="p1"><div class="scr"><img src="file://{D}/caps/home.png"></div></div><div class="phone" id="p2"><div class="scr"><img src="file://{D}/caps/swipe-Cypress-The_Hunt_Club.png"></div></div>',
 'cypress-eltigre': f'<div class="phone" id="p1"><div class="scr"><img src="file://{D}/caps/home.png"></div></div><div class="phone" id="p2"><div class="scr"><img src="file://{D}/caps/swipe-Cypress-El_Tigre.png"></div></div>',
 'cypress-palomino': f'<div class="phone" id="p1"><div class="scr"><img src="file://{D}/caps/home.png"></div></div><div class="phone" id="p2"><div class="scr"><img src="file://{D}/caps/swipe-Cypress-Palomino.png"></div></div>',
 'tortoise': f'<div class="phone" id="p1"><div class="scr"><img src="file://{D}/caps/home.png"></div></div><div class="phone" id="p2"><div class="scr"><img src="file://{D}/caps/swipe-Classic_Tortoise-Elysium.png"></div></div>',
 'cypress-knox': f'<div class="phone" id="p1"><div class="scr"><img src="file://{D}/caps/home.png"></div></div><div class="phone" id="p2"><div class="scr"><img src="file://{D}/caps/swipe-Cypress-Knox.png"></div></div>',
 'papaya': '<img id="comp" src="file:///home/claude/mahjmatchmaker-data/assets/links/v2/fym-phones.webp">',
 'cypress': f'<div class="phone" id="p1"><div class="scr"><img src="file://{D}/caps/home.png"></div></div><div class="phone" id="p2"><div class="scr"><img src="file://{D}/caps/set-Cypress.png"></div></div>',
 'sunday': f'<div class="phone" id="p1"><div class="scr"><img src="file://{D}/caps/color-Yellow_and_Orange.png"></div></div><div class="phone" id="p2"><div class="scr"><img src="file://{D}/caps/set-Sunday.png"></div></div>',
}
os.makedirs(D + '/out', exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for k, v in [(k,V[k]) for k in [k for k in ('cypress-huntclub','cypress-eltigre','cypress-palomino') if os.path.exists(D+'/caps/swipe-Cypress-'+{'cypress-huntclub':'The_Hunt_Club','cypress-eltigre':'El_Tigre','cypress-palomino':'Palomino'}[k]+'.png')]]:
        open(D + '/_s2.html', 'w').write(tpl.replace('__PHONES__', v))
        pg.goto('file://' + D + '/_s2.html'); pg.wait_for_timeout(900); pg.screenshot(path=D + '/_s2.png')
        Image.open(D + '/_s2.png').convert('RGB').save(f'{D}/out/countdown-story-{k}.jpg', quality=92)
        print(k)
    b.close()
