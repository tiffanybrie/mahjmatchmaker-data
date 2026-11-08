"""FYM 1.18 zoom-swipe QA in a real browser (Chromium): 390px phone with touch (CDP touch events) and 1440px desktop (mouse).
Tiles door (Up close mat deck, colour filter on/off), table view (S.zs.tvz), mat door (locked mat only pans; table-view tile deck swipes).
Usage: python3 builder/fym_fix_nov07/zoomswipe_pw.py <build_dir> <shot_dir>   (build_dir must hold the image bundles b*v*.js too)   -> prints PASS/FAIL lines, exit 1 on any FAIL."""
import sys, time, subprocess, socket, os, json
from playwright.sync_api import sync_playwright
B, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', B], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
R = []
def ok(L, cond, info=''):
    R.append((bool(cond), L)); print(('PASS ' if cond else 'FAIL ') + L + ('' if cond else f'  {info}'), flush=True)

class G:  # gestures: touch via CDP on the phone, mouse on desktop
    def __init__(s, pg, touch):
        s.pg, s.touch = pg, touch; s.cdp = pg.context.new_cdp_session(pg) if touch else None
    def down(s, x, y):
        if s.touch: s.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
        else: s.pg.mouse.move(x, y); s.pg.mouse.down()
    def move(s, x, y):
        if s.touch: s.cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y}]})
        else: s.pg.mouse.move(x, y)
    def up(s):
        if s.touch: s.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        else: s.pg.mouse.up()
    def drag(s, x0, y0, x1, y1, n=20, dt=0.03, hold=False):
        s.down(x0, y0)
        for i in range(1, n + 1): time.sleep(dt); s.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n)
        time.sleep(0.12 if dt >= 0.02 else 0)  # a slow drag ends still; a flick lifts while moving
        if not hold: s.up(); time.sleep(0.9)

ST = """k=>{const c=document.querySelector('#top-'+k);const im=c&&c.querySelector('.ph img');const key=S.mode==='table'?'tvz':(k==='m'?'mz':null);
 return {id:c?(c.dataset.id||c.dataset.i||''):null,zs:key&&S.zs[key]?S.zs[key]:null,tf:im?im.style.transform:'',liked:(k==='t'?S.tliked:S.liked).length,mode:S.mode}}"""
def st(pg, k='m'): return pg.evaluate(ST, k)
def box(pg, k='m'):
    pg.locator(f'#top-{k}').scroll_into_view_if_needed(); time.sleep(.3)
    return pg.evaluate("k=>{const r=document.querySelector('#top-'+k+' .ph').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}", k)
def boot(pg):
    pg.goto('about:blank'); pg.goto(f'http://127.0.0.1:{port}/index.html#notour'); pg.wait_for_function('window.__imgsReady===true', timeout=90000); time.sleep(1.2)
    try: pg.locator('[data-tour-skip]').first.click(timeout=2000)
    except Exception: pass
def synth(pg, a, v): pg.evaluate("([a,v])=>{const x=document.createElement('button');x.setAttribute(a,v);x.style.display='none';document.body.appendChild(x);x.click();x.remove()}", [a, str(v)])
def waitimg(pg, k):
    try: pg.wait_for_function("k=>{const i=document.querySelector('#top-'+k+' .ph img');return i&&i.complete&&i.naturalWidth>0}", arg=k, timeout=20000); time.sleep(.3)
    except Exception: print('  (image slow to load)')
def zoom_in(pg, k='m', times=2):
    for _ in range(times): pg.locator(f'#top-{k} [data-z="1"]').first.evaluate('e=>e.click()'); time.sleep(.35)

def deck_suite(pg, g, L, k='m'):
    """the zoomed swipe cases on deck k; returns nothing, appends to R"""
    s0 = st(pg, k); zs0 = s0['zs']; ok(f'{L}: zoomed in', zs0 and zs0['s'] > 1.5, s0)
    x, y, w, h = box(pg, k); cx, cy = x + w / 2, y + h / 2
    # small drag pans
    g.drag(cx + 20, cy, cx - 30, cy, n=10); s1 = st(pg, k)
    ok(f'{L}: small drag pans (same card, photo moved)', s1['id'] == s0['id'] and s1['zs']['x'] != zs0['x'], (s0, s1))
    # vertical drag pans
    g.drag(cx, cy + 60, cx, cy - 60, n=12); s2 = st(pg, k)
    ok(f'{L}: vertical drag pans (same card)', s2['id'] == s0['id'] and s2['zs']['y'] != s1['zs']['y'], (s1, s2))
    # diagonal drag pans
    g.drag(cx + 50, cy + 50, cx - 50, cy - 50, n=12); s3 = st(pg, k)
    ok(f'{L}: diagonal drag pans (same card)', s3['id'] == s0['id'], s3)
    # drag left: from the centre, a first drag pans to the edge, a further drag past the edge swipes (X)
    for zb in ('-1', '-1', '-1', '1', '1'): pg.locator(f'#top-{k} [data-z="{zb}"]').first.evaluate('e=>e.click()'); time.sleep(.3)
    s0 = st(pg, k); zs0 = s0['zs']
    g.drag(x + w - 20, cy, x + w - 320, cy, n=24); s4 = st(pg, k)
    ok(f'{L}: long drag pans to the right edge first', s4['id'] == s0['id'], s4)
    rem = max(0, s4['zs']['x'] + w * (s4['zs']['s'] - 1))  # pan room left before the right edge
    g.drag(x + w - 10, cy, x + w - 10 - rem - 130, cy, n=14 + int(rem / 25), hold=True); time.sleep(.15)
    pg.screenshot(path=f'{OUT}/{L.replace(" ", "_").replace(":", "")}_1_midswipe.png')
    g.up(); time.sleep(.9); waitimg(pg, k); s5 = st(pg, k)
    ok(f'{L}: drag past the edge swipes to the next card (X)', s5['id'] != s0['id'] and s5['liked'] == s0['liked'], (s0, s5))
    ok(f'{L}: zoom persists to the next card', s5['zs'] and abs(s5['zs']['s'] - zs0['s']) < .01 and (f"scale({s5['zs']['s']:.2f}" in s5['tf'] or 'scale(1)' not in s5['tf']), s5)
    if not s5['tf']: print('  (next photo still loading; S.zs carries the zoom, applied on load)')
    pg.screenshot(path=f'{OUT}/{L.replace(" ", "_").replace(":", "")}_2_nextcard.png')
    # flick right from wherever the photo is = heart
    x, y, w, h = box(pg, k); cx, cy = x + w / 2, y + h / 2
    g.drag(cx - 60, cy, cx + 60, cy, n=4, dt=0.012); s6 = st(pg, k)
    ok(f'{L}: flick right while zoomed = heart, next card', s6['id'] != s5['id'] and s6['liked'] == s5['liked'] + 1, (s5, s6))
    ok(f'{L}: flick keeps the zoom spot', s6['zs'] and abs(s6['zs']['x'] - s5['zs']['x']) < 1, (s5['zs'], s6['zs']))
    # short overflow springs back
    x, y, w, h = box(pg, k); cx, cy = x + w / 2, y + h / 2
    g.drag(x + w - 10, cy, x + 10, cy, n=24); s7 = st(pg, k)
    g.drag(cx, cy, cx - 40, cy, n=10); s8 = st(pg, k)
    tf = pg.evaluate("k=>document.querySelector('#top-'+k).style.transform", k)
    ok(f'{L}: short drag past the edge springs back', s8['id'] == s7['id'] and not tf, (s7, s8, tf))
    # buttons still work while zoomed
    btn = '[data-tno]' if k == 't' else f'[data-no="{k}"]'
    sec = '#s-tiles' if k == 't' else ('#s-mats' if k == 'm' else '#s-racks')
    b = pg.locator(f'{sec} {btn}').locator('visible=true')
    if b.count():
        b.first.click(); time.sleep(.9); s9 = st(pg, k)
        ok(f'{L}: X button works while zoomed', s9['id'] != s8['id'], (s8, s9))
    else: print(f'  (no visible X button for {L})')

def run(p, L, vp, touch):
    br = p.chromium.launch()
    ctx = br.new_context(viewport=vp, has_touch=touch, is_mobile=touch, device_scale_factor=2 if touch else 1)
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); g = G(pg, touch)
    # tiles door, Up close
    boot(pg); pi = pg.evaluate("D.sets.findIndex(s=>s.slug==='oh-my-mahjong-papaya-spritz')"); synth(pg, 'data-tile', pi); time.sleep(1.2)
    ok(f'{L} tiles door: Up close mode', st(pg)['mode'] == 'close')
    if touch:  # double-tap to zoom (the phone way)
        x, y, w, h = box(pg); g.down(x + w / 2, y + h / 2); g.up(); time.sleep(.08); g.down(x + w / 2, y + h / 2); g.up(); time.sleep(.5)
        ok(f'{L} tiles door: double-tap zooms', (st(pg)['zs'] or {}).get('s', 1) > 1.5, st(pg))
        if (st(pg)['zs'] or {}).get('s', 1) < 1.5: zoom_in(pg)
    else: zoom_in(pg)
    pg.screenshot(path=f'{OUT}/{L}_0_zoomed.png')
    deck_suite(pg, g, f'{L} tiles door')
    # colour filter on: zoomed swipe still works, then clear
    fams = pg.evaluate("[...document.querySelectorAll('#s-mats [data-fam][data-k=\"m\"]')].map(b=>b.dataset.fam).filter(Boolean)")
    if fams:
        fam = 'green' if 'green' in fams else fams[0]
        pg.locator(f'#s-mats [data-fam="{fam}"][data-k="m"]').first.evaluate('e=>e.click()'); time.sleep(.8)
        s0 = st(pg); x, y, w, h = box(pg); cx, cy = x + w / 2, y + h / 2
        g.drag(cx - 60, cy, cx + 60, cy, n=4, dt=0.012); s1 = st(pg)
        ok(f'{L} colour filter {fam}: zoomed flick swipes', s1['id'] != s0['id'], (s0, s1))
        pg.locator('#s-mats [data-fam=""][data-k="m"]').first.evaluate('e=>e.click()'); time.sleep(.6)
        ok(f'{L} colour filter: cleared', pg.evaluate("S.f.m.fam.length") == 0)
    # table view (S.zs.tvz)
    pg.locator('#s-mats [data-mode="table"]').locator('visible=true').first.click(); time.sleep(2.5)
    if (st(pg)['zs'] or {}).get('s', 1) < 1.5: zoom_in(pg)
    pg.screenshot(path=f'{OUT}/{L}_3_table_zoomed.png')
    s0 = st(pg); ok(f'{L} table view: zoom (tvz)', s0['zs'] and s0['zs']['s'] > 1.5, s0)
    x, y, w, h = box(pg); cy = y + h / 2
    g.drag(x + w - 10, cy, x + 10, cy, n=24); g.drag(x + w - 10, cy, x + w - 140, cy, n=14); time.sleep(1.5); s1 = st(pg)
    waitimg(pg, 'm'); s1 = st(pg)
    ok(f'{L} table view: drag past the edge swipes, tvz persists', s1['id'] != s0['id'] and s1['zs'] and abs(s1['zs']['s'] - s0['zs']['s']) < .01, (s0, s1))
    pg.screenshot(path=f'{OUT}/{L}_4_table_next.png')
    # mat door: the chosen (locked) mat only pans; table-view tile deck swipes while zoomed
    boot(pg); lark = pg.evaluate("Object.keys(M).find(k=>M[k].n==='Larkspur'&&!M[k].hid)")
    synth(pg, 'data-door', 'mat'); time.sleep(.6); synth(pg, 'data-dmat', lark); time.sleep(1.5)
    if pg.evaluate('S.mode') != 'table': pg.locator('#s-tiles [data-mode="table"]').first.evaluate('e=>e.click()'); time.sleep(2.5)
    if pg.locator('#top-t').count():
        if not (st(pg, 't')['zs'] or {}).get('s', 1) > 1.5: zoom_in(pg, 't')
        s0 = st(pg, 't'); ok(f'{L} mat door table: tiles zoomed', (s0['zs'] or {}).get('s', 1) > 1.5, s0)
        x, y, w, h = box(pg, 't'); cx, cy = x + w / 2, y + h / 2
        g.drag(cx - 60, cy, cx + 60, cy, n=4, dt=0.012); s1 = st(pg, 't')
        ok(f'{L} mat door table: zoomed flick swipes the tile card (heart)', s1['id'] != s0['id'] and s1['liked'] == s0['liked'] + 1, (s0, s1))
        pg.screenshot(path=f'{OUT}/{L}_5_matdoor_table.png')
    else: ok(f'{L} mat door: tile deck present', False, 'no #top-t')
    ok(f'{L}: no page errors', not errs, errs[:3])
    br.close()

with sync_playwright() as p:
    run(p, 'phone390', {'width': 390, 'height': 844}, True)
    run(p, 'desk1440', {'width': 1440, 'height': 900}, False)
srv.terminate()
n = sum(1 for r in R if not r[0]); print(f'ZOOMSWIPE QA: {"PASS" if not n else "FAIL"} ({len(R) - n}/{len(R)})'); sys.exit(1 if n else 0)
