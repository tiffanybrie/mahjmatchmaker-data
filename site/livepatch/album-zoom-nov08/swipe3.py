import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    dev=dict(p.devices['iPhone 14']); dev.pop('default_browser_type')
    b=p.chromium.launch(); ctx=b.new_context(**dev); pg=ctx.new_page()
    if len(sys.argv)>2: pg.add_init_script(open(sys.argv[2]).read())
    pg.goto(sys.argv[1],wait_until='domcontentloaded',timeout=90000); pg.wait_for_timeout(2000)
    print(pg.evaluate('''()=>{document.querySelectorAll(".mm3-c img[data-lb]")[0].click();var r=document.querySelector(".mm3-lb"),c=()=>r.querySelector(".c").textContent.slice(0,8),o=[c()];
    function tc(x){return new Touch({identifier:1,target:r,clientX:x,clientY:400})}
    r.dispatchEvent(new TouchEvent("touchstart",{touches:[tc(300)],changedTouches:[tc(300)],bubbles:true}));
    r.dispatchEvent(new TouchEvent("touchend",{touches:[],changedTouches:[tc(150)],bubbles:true}));o.push(c());
    r.dispatchEvent(new TouchEvent("touchstart",{touches:[tc(100)],changedTouches:[tc(100)],bubbles:true}));
    r.dispatchEvent(new TouchEvent("touchend",{touches:[],changedTouches:[tc(300)],bubbles:true}));o.push(c());return o}'''))
    b.close()
