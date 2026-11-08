import sys, time, subprocess, json
from playwright.sync_api import sync_playwright
url=sys.argv[1]; eng=sys.argv[2] if len(sys.argv)>2 else 'webkit'
def rss(name):
    out=subprocess.run("ps -eo rss,comm,args | grep -iE '%s' | grep -v grep"%name,shell=True,capture_output=True,text=True).stdout
    return sum(int(l.split()[0]) for l in out.splitlines() if l.strip())//1024
with sync_playwright() as p:
    dev=p.devices['iPhone 14']
    b=getattr(p,eng).launch()
    if eng=='chromium': dev={k:v for k,v in dev.items() if k!='default_browser_type'}
    else: dev={k:v for k,v in dev.items() if k!='default_browser_type'}
    ctx=b.new_context(**dev); pg=ctx.new_page()
    errs=[]; pg.on('console',lambda m: m.type in('error','warning') and errs.append(m.text[:150])); pg.on('pageerror',lambda e: errs.append('PAGEERR '+str(e)[:150]))
    crashed=[]; pg.on('crash',lambda: crashed.append(1))
    pg.goto(url,wait_until='load',timeout=90000)
    H=pg.evaluate('document.body.scrollHeight')
    for y in range(0,H,600):
        pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(120)
    pg.wait_for_timeout(3000)
    st=lambda: pg.evaluate('({n:document.getElementsByTagName("*").length, imgs:[...document.images].filter(i=>i.complete&&i.naturalWidth).length, h:document.body.scrollHeight, lb:document.querySelectorAll(".mm3-lb").length, st:document.querySelectorAll("style").length})')
    print('after scroll',st(),'rss',rss('WebKit|chrom'))
    for k in range(30):
        w=390 if k%2 else 1200; hh=664 if k%2 else 2000
        pg.set_viewport_size({'width':w,'height':hh})
        pg.evaluate('window.dispatchEvent(new Event("resize")); window.visualViewport&&window.visualViewport.dispatchEvent(new Event("resize")); window.dispatchEvent(new Event("scroll"))')
        pg.wait_for_timeout(150)
    print('after zoom',st(),'rss',rss('WebKit|chrom'),'crash',crashed)
    # lightbox: open and swipe through all
    n=pg.evaluate('document.querySelectorAll("img[data-lb]").length')
    pg.evaluate('document.querySelector(".mm3-c img[data-lb]").click()')
    for k in range(n): pg.evaluate('document.querySelector(".mm3-lb .n").click()'); pg.wait_for_timeout(80)
    print('after lightbox',st(),'rss',rss('WebKit|chrom'))
    print('errors',len(errs),errs[:10])
    b.close()
