"""v2 (Nov 2): load the live FYM site copy (app v113 @3c0b8ceb) in headless Chromium for the intro reel v2 captures."""
import os, re
W = '/dev/shm/introv2'
os.environ['TMPDIR'] = W + '/tmp'; os.makedirs(W + '/tmp', exist_ok=True)
from playwright.sync_api import sync_playwright
PX = os.environ.get('HTTPS_PROXY')
HTML = open(W + '/fym/index.html', 'rb').read()   # git show 3c0b8ceb:site-app/fym-v113/index.html
BASE = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@3c0b8ceb/site-app/fym-v113/'
BASE72 = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@ad0675e42242c3abad40cac9f539a265220e26eb/site-app/fym-v72/'  # every other relative file (b*v1.js bundles, t10/ tiles...) lives here
import re
LOGO = re.search(rb'id="logo"[^>]*?src="(data:image/png;base64,[^"]+)"', HTML).group(1).decode()
def fixlogo(pg): pg.evaluate('(s)=>{for(const l of document.querySelectorAll("#logo,img[alt=\'Mahj Matchmaker\']"))if(!l.naturalWidth)l.src=s}', LOGO)
RECT = """(sel)=>{const e=[...document.querySelectorAll(sel)].find(x=>x.offsetParent);if(!e)return null;const r=e.getBoundingClientRect();return [r.left,r.top,r.width,r.height]}"""
def start(p, scale=2):
    b = p.chromium.launch(proxy={'server': PX} if PX else None, args=[f'--force-device-scale-factor={scale}'])  # Nov 3: without this the CDP screencast came back at 390px (1x) -> soft app footage
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=scale)
    def h(r):
        u = r.request.url
        if u.split('?')[0].endswith('/index.html'):
            r.fulfill(status=200, body=HTML, headers={'content-type': 'text/html; charset=utf-8'})
        else:
            f = u.split('fym.test/', 1)[1]
            r.fulfill(response=r.fetch(url=(BASE if f.startswith(('mc/', 'thumbs113')) else BASE72) + f))
    ctx.route('https://fym.test/**', h)
    pg = ctx.new_page()
    pg.goto('https://fym.test/index.html?tour=off'); pg.wait_for_timeout(7000)
    pg.add_style_tag(content='.swh{display:none!important}')
    fixlogo(pg)
    return b, ctx, pg
