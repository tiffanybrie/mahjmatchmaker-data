"""Mat door holiday demo: Tartan Tidings (Anders Ruff) -> swipe tile sets -> card."""
import sys,json; sys.path.insert(0,'/home/claude/mahjmatchmaker-data/assets/social/fym-bank-oct31')
from lib import *
with sync_playwright() as p:
    b,pg=start(p); ev=pg.evaluate
    ev("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Start with a mat')).click()"); pg.wait_for_timeout(2500)
    pg.locator('input[placeholder*=Search]:visible').first.click(); pg.keyboard.type('Tartan Tidings'); pg.wait_for_timeout(1500)
    ev("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/Tartan Tidings/.test(b.innerText));b.click()}"); pg.wait_for_timeout(3000)
    print(ev("()=>JSON.stringify({dset:S.dset,tseen:Object.keys(S.tseen||{}).length})"))
    print(ev("()=>[...document.querySelectorAll('[class*=deck]')].map(d=>d.className)"))
    def td(): ev("()=>{const d=document.querySelector('.deck.t')||[...document.querySelectorAll('[class*=deck]')][0];window.scrollTo(0,d.getBoundingClientRect().top+scrollY-330)}"); pg.wait_for_timeout(1000)
    for _ in range(3): ev("()=>{const b=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&e.innerText.trim()==='−')[0];b&&b.click()}"); pg.wait_for_timeout(500)
    names=[]
    for i in range(5):
        td(); shot(pg,f'td{i}'); n=ev("()=>{const y=[...document.querySelectorAll('button.sb.yes, button.yes')].filter(b=>b.offsetParent)[0].getBoundingClientRect().top;const bs=[...document.querySelectorAll('b')].filter(e=>e.offsetParent&&e.getBoundingClientRect().top>y);return bs.length?bs[0].innerText:''}"); names.append(n)
        ev("()=>[...document.querySelectorAll('button.no')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1300)
    print(names)
    b.close()
