#!/usr/bin/env python3
"""Render page-block.html inside the LIVE /find-your-mat-ch-preview page (swapped in the browser only; nothing on the
site changes).  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR=/dev/shm python3 preview.py [outdir] [url]
Saves fym-page-<w>.png (full page, downscaled sheet) + fym-app-<w>.png (the app section) and prints checks."""
import os, sys, json
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'qa')
URL = sys.argv[2] if len(sys.argv) > 2 else 'https://www.mahjmatchmaker.com/find-your-mat-ch-preview'
SWAP_IN = '--live' not in sys.argv
os.makedirs(OUT, exist_ok=True)
BLOCK = open(os.path.join(HERE, 'page-block.html')).read()
SWAP = """(html)=>{const m=document.querySelector('#fymp,#fymx');const box=m.closest('.sqs-block-content');box.innerHTML=html;
box.querySelectorAll('script').forEach(o=>{const n=document.createElement('script');n.textContent=o.textContent;o.replaceWith(n)});
return !!document.getElementById('fymx')}"""
CHECK = """(()=>{const R=document.getElementById('fymx');const im=[...R.querySelectorAll('img')];const f=document.getElementById('fx-f');
 let app='';try{app=f.contentDocument.body.innerText.slice(0,80)}catch(e){app='ERR '+e}
 const st=document.getElementById('fx-stage').getBoundingClientRect();
 return {sw:[document.documentElement.scrollWidth,document.documentElement.clientWidth],rootW:R.getBoundingClientRect().width,
  h1:getComputedStyle(R.querySelector('h1')).fontFamily.slice(0,30),h1px:getComputedStyle(R.querySelector('h1')).fontSize,
  imgs:im.length,loaded:im.filter(i=>i.complete&&i.naturalWidth>0).length,stage:[Math.round(st.width),Math.round(st.height)],
  inner:window.innerHeight,app:app,ld:getComputedStyle(document.getElementById('fx-ld')).display}})()"""
with sync_playwright() as p:
    b = p.chromium.launch(proxy={'server': os.environ['HTTPS_PROXY']} if os.environ.get('HTTPS_PROXY') else None,
                          args=['--disable-dev-shm-usage'])
    res = {}
    for w, h in ((390, 844), (1280, 800), (1440, 900)):
        ctx = b.new_context(viewport={'width': w, 'height': h}, is_mobile=w < 500, has_touch=w < 500, device_scale_factor=1)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
        pg.goto(URL + ('&' if '?' in URL else '?') + 'nocache=%d' % os.getpid(), wait_until='load', timeout=90000)
        ok = pg.evaluate(SWAP, BLOCK) if SWAP_IN else True
        pg.evaluate("document.querySelectorAll('#fymx img').forEach(i=>i.loading='eager')")
        pg.wait_for_timeout(9000)
        r = pg.evaluate(CHECK); r['swap'] = ok; r['errs'] = errs
        # stitched viewport shots (Chromium full_page drops some lazy images on this site)
        from PIL import Image; import io
        H = pg.evaluate("document.documentElement.scrollHeight"); shots = []; y = 0
        while y < H:
            pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(700)
            sy = pg.evaluate("window.scrollY"); shots.append((sy, Image.open(io.BytesIO(pg.screenshot()))))
            if sy + h >= H: break
            y += h
        sheet = Image.new('RGB', (w, H), 'white')
        for sy, im in shots: sheet.paste(im, (0, sy))
        sheet.save(os.path.join(OUT, f'fym-page-{w}.png'))
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500)
        pg.query_selector('#fymx [data-fx-go]').click(); pg.wait_for_timeout(1500)
        pg.screenshot(path=os.path.join(OUT, f'fym-app-{w}.png'))
        r['afterStart'] = pg.evaluate("Math.round(document.getElementById('fx-stage').getBoundingClientRect().top)")
        btn = [x for x in pg.query_selector_all('#fymx [data-fx-fs]') if x.is_visible()]
        if btn:
            btn[0].click(); pg.wait_for_timeout(800)
            pg.screenshot(path=os.path.join(OUT, f'fym-fullscreen-{w}.png'))
            r['fs'] = pg.evaluate("(()=>{const s=document.getElementById('fx-stage').getBoundingClientRect();return [s.left,s.top,s.width,s.height]})()")
            pg.click('#fx-x'); pg.wait_for_timeout(500)
            r['fsClosed'] = pg.evaluate("!document.getElementById('fx-stage').classList.contains('fs')")
        res[w] = r; ctx.close()
    b.close()
print(json.dumps(res, indent=1))
