#!/usr/bin/env python3
"""Render the staged teaser inside the LIVE /find-your-match page (swapped in the browser only; nothing on
the site changes). Usage: python3 preview.py [outdir]  ->  teaser-390.png, teaser-1280.png
Needs PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers and the agent proxy in HTTPS_PROXY."""
import os, sys, json
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'qa')
os.makedirs(OUT, exist_ok=True)
BLOCK = open(os.path.join(HERE, 'teaser-block.html')).read()
SWAP = """(html)=>{const m=document.querySelector('.mmab');const box=m.closest('.sqs-block-content');box.innerHTML=html;
box.querySelectorAll('script').forEach(o=>{const n=document.createElement('script');n.textContent=o.textContent;o.replaceWith(n)});
return !!document.getElementById('mmtz')}"""
with sync_playwright() as p:
    b = p.chromium.launch(proxy={'server': os.environ['HTTPS_PROXY']} if os.environ.get('HTTPS_PROXY') else None,
                          args=['--disable-dev-shm-usage'])
    res = {}
    for w, h in ((390, 844), (1280, 900)):
        ctx = b.new_context(viewport={'width': w, 'height': h}, is_mobile=w < 500, has_touch=w < 500, device_scale_factor=1)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
        pg.goto('https://www.mahjmatchmaker.com/find-your-match', wait_until='load', timeout=90000)
        ok = pg.evaluate(SWAP, BLOCK)
        pg.wait_for_timeout(5000)
        r = pg.evaluate("""(()=>{const R=document.getElementById('mmtz');const im=[...R.querySelectorAll('img')];
          const tk=[...R.querySelectorAll('.mmtz-tk a')].slice(0,6).map(a=>getComputedStyle(a).backgroundImage.slice(5,60));
          return {sw:[document.documentElement.scrollWidth,document.documentElement.clientWidth],
            cd:R.querySelector('.mmtz-cd').innerText.replace(/\\n/g,' '),live:R.className,
            imgs:im.length,loaded:im.filter(i=>i.complete&&i.naturalWidth>0).length,
            h1:getComputedStyle(R.querySelector('h1')).fontFamily,h1px:getComputedStyle(R.querySelector('h1')).fontSize,
            body_px:getComputedStyle(R.querySelector('.mmtz-n p')).fontSize,tk:tk.length,box:R.getBoundingClientRect().width}})()""")
        r['swap'] = ok; r['errs'] = errs
        # make every card image load for the check (lazy ones off-screen)
        pg.evaluate("document.querySelectorAll('#mmtz img').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(2500)
        r['loaded_all'] = pg.evaluate("[...document.querySelectorAll('#mmtz img')].filter(i=>i.complete&&i.naturalWidth>0).length")
        el = pg.query_selector('#mmtz')
        el.screenshot(path=os.path.join(OUT, f'teaser-{w}.png'))
        # a mid-animation frame of the card stack (heart / X)
        pg.query_selector('#mmtz .mmtz-st').scroll_into_view_if_needed()
        for k in range(3):
            pg.wait_for_timeout(1150)
            pg.query_selector('#mmtz .mmtz-st').screenshot(path=os.path.join(OUT, f'teaser-stack-{w}-{k}.png'))
        res[w] = r; ctx.close()
    b.close()
print(json.dumps(res, indent=1))
