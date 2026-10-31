import sys
from playwright.sync_api import sync_playwright
SET,TAG,Q=sys.argv[1],sys.argv[2],sys.argv[3]
OUT='/tmp/claude-0/-home-claude/250610d9-5db2-5b77-a936-b63b33a20ff7/scratchpad/fr/'+TAG
import os; os.makedirs(OUT,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=3)
    pg.goto('https://www.mahjmatchmaker.com/find-your-match',timeout=60000); pg.wait_for_timeout(9000)
    f=pg.frames[1]
    el=pg.query_selector('iframe'); 
    f.add_style_tag(content='.swh{display:none!important}')
    f.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type(Q); pg.wait_for_timeout(1500)
    ok=f.evaluate("(t)=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(t));if(b){b.click();return true}return [...document.querySelectorAll('button')].filter(b=>b.offsetParent).map(b=>b.innerText.trim()).slice(0,30)}",SET); print('clicked',ok); pg.wait_for_timeout(3500)
    print(f.evaluate("()=>S.set+' '+S.step"))
    def deck(off=330):
        top=f.evaluate(f"()=>{{const d=document.querySelector('.deck.m');return d.getBoundingClientRect().top+scrollY-{off}}}")
        # scroll the outer page so the iframe region shows the deck
        ft=pg.evaluate("()=>document.querySelector('iframe').getBoundingClientRect().top+scrollY")
        pg.evaluate(f"window.scrollTo(0,{ft+top})"); f.evaluate(f"window.scrollTo(0,{top})"); pg.wait_for_timeout(1300)
    for i in range(3):
        deck(); pg.screenshot(path=f'{OUT}/swipe{i}.png'); print('shot',i)
        f.evaluate("()=>[...document.querySelectorAll('button.yes')].find(b=>b.offsetParent).click()"); pg.wait_for_timeout(1500)
    deck(250); pg.evaluate("window.scrollBy(0,360)"); f.evaluate("window.scrollBy(0,360)"); pg.wait_for_timeout(900); pg.screenshot(path=f'{OUT}/suitors.png')
    b.close()
