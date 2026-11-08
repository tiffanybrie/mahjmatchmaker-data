import sys,re
from playwright.sync_api import sync_playwright
MARK='<!-- Album lightbox pinch fix'
def run(p,url,strip):
    dev=dict(p.devices['iPhone 14']); dev.pop('default_browser_type')
    b=p.chromium.launch(); ctx=b.new_context(**dev); pg=ctx.new_page()
    errs=[]; pg.on('console',lambda m: m.type=='error' and errs.append(m.text[:140])); pg.on('pageerror',lambda e: errs.append('PAGEERR '+str(e)[:140]))
    if strip:
        def h(route):
            r=route.fetch(); body=r.text()
            body=re.sub(r'<!-- Album lightbox pinch fix.*?</script>','',body,flags=re.S)
            route.fulfill(response=r,body=body)
        pg.route(url,h)
    pg.goto(url,wait_until='domcontentloaded',timeout=90000); pg.wait_for_timeout(3000)
    has=pg.evaluate('document.documentElement.innerHTML.includes("Album lightbox pinch fix")')
    pg.evaluate('document.querySelectorAll(".mm3-c img[data-lb]")[0].click()')
    cap=lambda: pg.evaluate('document.querySelector(".mm3-lb .c").textContent.slice(0,8)')
    cdp=ctx.new_cdp_session(pg)
    def T(t,pts): cdp.send('Input.dispatchTouchEvent',{'type':t,'touchPoints':[{'x':x,'y':y} for x,y in pts]})
    r=[cap()]
    for k in range(5):
        T('touchStart',[(150,400),(240,400)])
        for s in range(1,8): T('touchMove',[(150-s*12,400),(240+s*12,400)])
        T('touchEnd',[]); pg.wait_for_timeout(150); r.append(cap())
    sw=[]
    T('touchStart',[(300,400)])
    for s in range(1,6): T('touchMove',[(300-s*30,400)])
    T('touchEnd',[]); pg.wait_for_timeout(200); sw.append(cap())
    T('touchStart',[(100,400)])
    for s in range(1,6): T('touchMove',[(100+s*30,400)])
    T('touchEnd',[]); pg.wait_for_timeout(200); sw.append(cap())
    b.close(); return has,r,sw,errs
url=sys.argv[1]
with sync_playwright() as p:
    a=run(p,url,False); base=run(p,url,True)
print(url); print(' live snippet present:',a[0],'| pinches:',a[1],'| swipe L,R:',a[2])
print(' baseline (snippet stripped) present:',base[0],'| pinches:',base[1])
new=[e for e in a[3] if e not in base[3]]
print(' console errors live:',len(a[3]),'baseline:',len(base[3]),'NEW:',new)
