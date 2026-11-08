import sys
from playwright.sync_api import sync_playwright
url=sys.argv[1]
with sync_playwright() as p:
    dev=dict(p.devices['iPhone 14']); dev.pop('default_browser_type')
    b=p.chromium.launch(); ctx=b.new_context(**dev); pg=ctx.new_page()
    pg.goto(url,wait_until='domcontentloaded',timeout=90000); pg.wait_for_timeout(2500)
    pg.evaluate('document.querySelectorAll(".mm3-c img[data-lb]")[0].click()')
    cap=lambda: pg.evaluate('document.querySelector(".mm3-lb .c").textContent.slice(0,8)')
    cdp=ctx.new_cdp_session(pg)
    def T(t,pts): cdp.send('Input.dispatchTouchEvent',{'type':t,'touchPoints':[{'x':x,'y':y} for x,y in pts]})
    r=[cap()]
    for k in range(5):
        T('touchStart',[(150,400),(240,400)])
        for s in range(1,8): T('touchMove',[(150-s*12,400),(240+s*12,400)])
        T('touchEnd',[]); pg.wait_for_timeout(150); r.append(cap())
    print('pinches:',r)
    # one-finger swipe still works
    T('touchStart',[(300,400)]); 
    for s in range(1,6): T('touchMove',[(300-s*30,400)])
    T('touchEnd',[]); pg.wait_for_timeout(150); print('swipe left ->',cap())
    b.close()
