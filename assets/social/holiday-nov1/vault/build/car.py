import os
from playwright.sync_api import sync_playwright
O='/home/claude/mahjmatchmaker-data/assets/social/holiday-nov1/vault/carousel/'
os.makedirs(O+'story',exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(args=['--allow-file-access-from-files']); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file:///dev/shm/vault-tour/build/carousel.html'); pg.wait_for_timeout(500)
    n=pg.evaluate('N')
    for i in range(n):
        for story in (0,1):
            pg.evaluate(f'show({i},{story})'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(700)
            f=(O+'story/' if story else O)+f'{i+1:02d}-'+('story' if story else 'slide')+'.jpg'
            pg.locator('#fr').screenshot(path=f,type='jpeg',quality=92)
    b.close()
print(n)
