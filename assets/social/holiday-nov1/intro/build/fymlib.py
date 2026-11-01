import os
os.environ['TMPDIR']='/dev/shm/holiday-intro/tmp'; os.makedirs('/dev/shm/holiday-intro/tmp',exist_ok=True)
from playwright.sync_api import sync_playwright
PX=os.environ['HTTPS_PROXY']
HTML=open('/dev/shm/holiday-intro/fym/index.html','rb').read()
LOGO=open('/dev/shm/holiday-intro/logo.txt').read()
def fixlogo(pg): pg.evaluate('(s)=>{const l=document.getElementById("logo");if(l&&!l.naturalWidth)l.src=s}',LOGO)
def start(p,scale=3,ctx_only=False):
    b=p.chromium.launch(proxy={'server':PX})
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=scale)
    BASE='https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@ad0675e42242c3abad40cac9f539a265220e26eb/site-app/fym-v72/'
    def h(r):
        u=r.request.url
        if u.split('?')[0].endswith('/index.html'): r.fulfill(status=200,body=HTML,headers={'content-type':'text/html; charset=utf-8'})
        else:
            resp=r.fetch(url=BASE+u.split('fym.test/',1)[1]); r.fulfill(response=resp)
    ctx.route('https://fym.test/**',h)
    pg=ctx.new_page()
    pg.goto('https://fym.test/index.html?tour=off'); pg.wait_for_timeout(7000)
    pg.add_style_tag(content='.swh{display:none!important}')
    fixlogo(pg)
    return b,ctx,pg
