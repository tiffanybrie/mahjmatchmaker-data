"""[144] (Nov 1, live bug found by the Table-preview build): on WebKit iPhone the page must never be wider than the screen
(document scrollWidth <= innerWidth) and the top bar must fit, at every step: open, tile grid, mats deck, mat picked, racks, rack
picked, match card, mat door. Widths: 390 (iPhone 13), 375 (iPhone mini / SE class), 340 (the app inside the website's page block).
The step nav (.stp, 266-289px) used not to shrink and pushed the stars/account icons and the page sideways.
Usage: python3 fym_webkit_width.py <build dir>  -> prints FAIL lines, exit 1 on failure."""
import sys, time, subprocess, socket
from playwright.sync_api import sync_playwright
B = sys.argv[1]; s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', B], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
F = []
W = """()=>({sw:document.documentElement.scrollWidth,bw:document.body.scrollWidth,iw:innerWidth,
  top:Math.max(0,...[...document.querySelectorAll('.top, .top > *')].map(e=>Math.round(e.getBoundingClientRect().right)))})"""
def chk(pg, label):
    r = pg.evaluate(W)
    if max(r['sw'], r['bw']) > r['iw'] + 1: F.append(f"[144] WebKit iPhone {label}: page {max(r['sw'], r['bw'])}px wide on a {r['iw']}px screen")
    if r['top'] > r['iw'] + 1: F.append(f"[144] WebKit iPhone {label}: the top bar reaches {r['top']}px on a {r['iw']}px screen")
def flow(pg, L):
    pg.goto(f'http://127.0.0.1:{port}/index.html#notour'); pg.wait_for_function('window.__imgsReady===true', timeout=90000); time.sleep(1.5); chk(pg, L + ' open')
    if not pg.locator('#s-tiles .tgrid [data-tile]').count(): pg.locator('#s-tiles .blg').first.click(); time.sleep(.8)
    chk(pg, L + ' tile grid'); pg.locator('#s-tiles .tgrid [data-tile]').first.click(); time.sleep(1); chk(pg, L + ' mats step')
    pg.locator('[data-yes="m"]').first.click(); time.sleep(.8); pg.locator('.tray .th button').first.click(); time.sleep(.8); chk(pg, L + ' mat picked')
    pg.locator('.tray .go[data-mock]').first.click(); time.sleep(1); chk(pg, L + ' racks step')
    pg.locator('[data-yes="r"]').first.click(); time.sleep(.8); pg.locator('#rtray .th button').first.click(); time.sleep(.6); chk(pg, L + ' rack picked')
    pg.locator('#rtray [data-make]').first.click(); time.sleep(2); chk(pg, L + ' match card')
    pg.evaluate("S.door='mat';S.dmat=null;renderAll()"); time.sleep(1); chk(pg, L + ' mat door')
try:
    with sync_playwright() as p:
        br = p.webkit.launch()
        for vw in (390, 375, 340):
            ctx = br.new_context(**dict(p.devices['iPhone 13'], viewport={'width': vw, 'height': 664})); pg = ctx.new_page()
            try: flow(pg, f'{vw}px')
            except Exception as e: F.append(f'[144] WebKit width check stopped at {vw}px: {str(e)[:160]}')
            ctx.close()
        br.close()
except Exception as e: F.append(f'[144] WebKit width check did not run: {str(e)[:200]}')
srv.kill()
for f in F: print(f)
sys.exit(1 if F else 0)
