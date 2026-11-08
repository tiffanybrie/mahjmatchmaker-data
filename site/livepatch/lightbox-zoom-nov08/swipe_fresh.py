import sys
from playwright.sync_api import sync_playwright
url=sys.argv[1]
with sync_playwright() as p:
    dev=dict(p.devices['iPhone 14']); dev.pop('default_browser_type')
    b=p.chromium.launch(); ctx=b.new_context(**dev); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)[:120]))
    pg.goto(url,wait_until='domcontentloaded',timeout=90000); pg.wait_for_timeout(3000)
    pg.evaluate('document.querySelectorAll(".mm3-c img[data-lb]")[0].click()')
    cap=lambda: pg.evaluate('document.querySelector(".mm3-lb .c").textContent.slice(0,8)+" scale="+visualViewport.scale.toFixed(2)')
    cdp=ctx.new_cdp_session(pg)
    def T(t,pts): cdp.send('Input.dispatchTouchEvent',{'type':t,'touchPoints':[{'x':x,'y':y} for x,y in pts]})
    o=[cap()]
    def swipe(a,bx):
        T('touchStart',[(a,400)])
        for s in range(1,6): T('touchMove',[(a+(bx-a)*s/5,400)])
        T('touchEnd',[]); pg.wait_for_timeout(250); o.append(cap())
    swipe(300,100); swipe(300,100); swipe(100,300)
    # pinch then check scale
    T('touchStart',[(150,400),(240,400)])
    for s in range(1,8): T('touchMove',[(150-s*12,400),(240+s*12,400)])
    T('touchEnd',[]); pg.wait_for_timeout(300); o.append('after pinch '+cap())
    print(url.split('/')[-1],o,errs); b.close()
