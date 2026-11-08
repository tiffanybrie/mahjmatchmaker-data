"""Nov 8: harness for the CURRENT live FYM (website copy v118 @7817f04d, the version on /find-your-match).
Serves index.html from the pinned commit; every other file tried from fym-v118 first, then fym-v72 (the page's base)."""
import os, re, subprocess
W = '/dev/shm/pin2'; os.environ['TMPDIR'] = W + '/tmp'; os.makedirs(W + '/tmp', exist_ok=True)
from playwright.sync_api import sync_playwright
PX = os.environ.get('HTTPS_PROXY')
SHA = '7817f04d2c907d1ea0d4fd01d857fa7a3cffb8bf'
R = '/home/claude/mahjmatchmaker-data'
HTML = subprocess.run(['git', '-C', R, 'show', f'{SHA}:site-app/fym-v118/index.html'], capture_output=True, check=True).stdout
B118 = f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{SHA}/site-app/fym-v118/'
B72 = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@ad0675e42242c3abad40cac9f539a265220e26eb/site-app/fym-v72/'
IN118 = set(subprocess.run(['git', '-C', R, 'ls-tree', '-r', '--name-only', SHA, 'site-app/fym-v118/'], capture_output=True, text=True).stdout.replace('site-app/fym-v118/', '').split())
m = re.search(rb'id="logo"[^>]*?src="(data:image/png;base64,[^"]+)"', HTML); LOGO = m.group(1).decode() if m else ''
def fixlogo(pg):
    if LOGO: pg.evaluate('(s)=>{for(const l of document.querySelectorAll("#logo,img[alt=\'Mahj Matchmaker\']"))if(!l.naturalWidth)l.src=s}', LOGO)
def start(p, scale=2):
    b = p.chromium.launch(proxy={'server': PX} if PX else None, args=[f'--force-device-scale-factor={scale}'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=scale)
    def h(r):
        u = r.request.url
        if u.split('?')[0].endswith('/index.html'):
            r.fulfill(status=200, body=HTML, headers={'content-type': 'text/html; charset=utf-8'}); return
        f = u.split('fym.test/', 1)[1].split('?')[0]
        r.fulfill(response=r.fetch(url=(B118 if f in IN118 else B72) + f))
    ctx.route('https://fym.test/**', h)
    pg = ctx.new_page(); pg.goto('https://fym.test/index.html?tour=off'); pg.wait_for_timeout(8000)
    pg.add_style_tag(content='.swh{display:none!important}'); fixlogo(pg)
    return b, ctx, pg
