"""Phone screenshot of Find Your Mat-ch (tiles door) with one set + one mat on screen, for slide 3 of the
"It's a mat-ch!" carousel (Tiffany, Oct 21).

Serves a local FYM build folder (the published artifact's index.html + its b*.js / m/ / mc/ files), opens the
tiles door at 390x844 (@3x), searches the set, then taps X until the wanted mat is the top card.
Taps X only (never heart), so nothing is saved. The undo arrow is hidden in the shot: social shows X and heart only.

  python3 scripts/social/its_a_match/fym_shot.py --build-dir <fym build dir> --set "Papaya Spritz" --mat Heiress \
      --out assets/social/its-a-match/papaya-heiress/fym-screen.jpg
"""
import argparse, asyncio, functools, http.server, socketserver, threading, sys

TOP = """()=>{const ns=[...document.querySelectorAll('b')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.y>450&&r.y<780});
for(const e of ns){const r=e.getBoundingClientRect();const h=document.elementFromPoint(r.x+3,r.y+r.height/2);if(h&&(h===e||e.contains(h)))return e.textContent}
return ''}"""


def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
    s = socketserver.TCPServer(('127.0.0.1', 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


async def shot(build, tset, mat, out, max_swipes=150):
    from playwright.async_api import async_playwright
    srv = serve(build)
    url = f'http://127.0.0.1:{srv.server_address[1]}/index.html'
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
        await pg.goto(url, wait_until='load'); await pg.wait_for_timeout(1500)
        await pg.click('text=I have tiles'); await pg.wait_for_timeout(600)
        await pg.fill('#tsq', tset); await pg.wait_for_timeout(600)
        await pg.locator(f"button:has-text({tset!r})").first.click(); await pg.wait_for_timeout(2000)
        seen = []
        for _ in range(max_swipes):
            t = (await pg.evaluate(TOP)).strip()
            seen.append(t)
            if t.lower().startswith(mat.lower()): break
            await pg.click('button.no'); await pg.wait_for_timeout(650)
        else:
            sys.exit(f'{mat} never reached the top card; seen: {seen}')
        await pg.add_style_tag(content='button.undo{display:none!important}')
        await pg.wait_for_timeout(1500)   # let the mat photo finish loading
        ok = await pg.evaluate("[...document.images].filter(i=>i.getBoundingClientRect().width>200).every(i=>i.complete&&i.naturalWidth>0)")
        await pg.screenshot(path=out, type='jpeg', quality=93)
        await b.close()
    srv.shutdown()
    print('FYM screen', out, 'swipes:', seen, 'images loaded:', ok)
    return seen


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--build-dir', required=True); ap.add_argument('--set', required=True)
    ap.add_argument('--mat', required=True); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    asyncio.run(shot(a.build_dir, a.set, a.mat, a.out))
