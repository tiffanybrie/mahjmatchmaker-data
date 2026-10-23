"""FYM tour walk (Tiffany Oct 23 9:33-9:38am; replaces the v72 6-step placement check). Gate [35] runs it.
At 390x664, 390x844 (Chromium + WebKit) and 1280x800 (Chromium), from a fresh first open:
 - the tour starts by itself and walks her 8-step script by DOING each step (pick tiles, heart a mat, pick the suitor,
   Add racks ONCE, heart a rack, Make it official, Next, Done);
 - the steps arrive exactly in order (tiles, mats, pick, add, racks, make, share, shop); a step never repeats or goes back;
 - Add racks moves to the racks with ONE tap;
 - each tip box names its own step (coach data-step == current step, text starts with that step's title);
 - each step's target is on screen when the step starts (auto-scroll) and the tip box does not cover it;
 - no page errors; #notour keeps the tour off; "Take the tour" replays it from step 1.
Usage: python3 builder/fym_tour_place_check.py <build_dir> [shots_dir]. Exit 1 on any fail."""
import sys, time, os, socket, subprocess
from playwright.sync_api import sync_playwright
B = os.path.abspath(sys.argv[1]); OUT = sys.argv[2] if len(sys.argv) > 2 else None
so = socket.socket(); so.bind(('127.0.0.1', 0)); port = so.getsockname()[1]; so.close()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', B], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
URL = f'http://localhost:{port}/index.html'
ORDER = ['tiles', 'mats', 'pick', 'add', 'racks', 'make', 'share', 'shop']
ACT = {'tiles': '#s-tiles .tgrid button', 'mats': '[data-yes="m"]', 'pick': '.tray .th button', 'add': 'TARGET',
       'racks': '[data-yes="r"]', 'make': 'TARGET', 'share': '[data-tour-next]', 'shop': '[data-tour-next]'}
STATE = """()=>{if(!TOUR.on)return {on:false};const s=TSTEPS[TOUR.step],c=document.getElementById('coach'),t=tourTarget(s);
 const cr=c&&c.getBoundingClientRect(),tr=t&&t.getBoundingClientRect(),vh=innerHeight,vw=document.documentElement.clientWidth;
 const inter=!!(cr&&tr)&&!(cr.right<=tr.left||tr.right<=cr.left||cr.bottom<=tr.top||tr.bottom<=cr.top);
 const vis=tr?Math.max(0,Math.min(tr.bottom,vh)-Math.max(tr.top,56))/Math.max(1,Math.min(tr.height,vh-56)):0;
 return {on:true,k:s.k,title:s.t,cstep:c&&c.dataset.step,ctext:c?c.textContent:'',target:!!t,vis:Math.round(vis*100)/100,inter,
   offX:tr?(tr.left<-1||tr.right>vw+1):false,log:TOUR.log.slice()};}"""
fails = []
def F(tag, msg): print(tag, 'FAIL', msg); fails.append(f'{tag}: {msg}')
with sync_playwright() as p:
    for bt in ('chromium', 'webkit'):
        for (w, h) in ((390, 664), (390, 844), (1280, 800)):
            if bt == 'webkit' and w > 400: continue
            tag = f'{bt}-{w}x{h}'
            try: br = getattr(p, bt).launch()
            except Exception as e_: print(tag, 'SKIP: browser not installed here'); continue
            pg = br.new_page(viewport={'width': w, 'height': h}); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(URL); pg.wait_for_function('window.__imgsReady===true', timeout=90000)
            try: pg.wait_for_function('TOUR.on===true', timeout=6000)
            except Exception: F(tag, 'tour did not start by itself on first open'); br.close(); continue
            seen = []
            for n in range(12):
                time.sleep(.9)
                st = pg.evaluate(STATE)
                if not st['on']: break
                k = st['k']
                if seen and seen[-1] == k: F(tag, f'step {k} did not move forward after its action'); break
                if k in seen: F(tag, f'step {k} came back (loop)'); break
                seen.append(k)
                if OUT: pg.screenshot(path=f'{OUT}/{tag}-{len(seen)}-{k}.png')
                if st['cstep'] != k or not st['ctext'].startswith(st['title']): F(tag, f'tip box does not match step {k}: {st["ctext"][:60]!r}')
                if not st['target']: F(tag, f'step {k}: target missing'); break
                if st['vis'] < .6 or st['offX']: F(tag, f'step {k}: target not in view when the step starts (visible {st["vis"]})')
                if st['inter']: F(tag, f'step {k}: tip box covers its target')
                sel = ACT[k]
                if sel == 'TARGET':
                    sel = pg.evaluate("(()=>{const s=TSTEPS[TOUR.step];return s.b.split(',').find(x=>document.querySelector(x));})()")
                pg.locator(sel).first.click()
                if k == 'add':
                    time.sleep(.5)
                    if not pg.evaluate('!!S.fav'): F(tag, 'Add racks needed more than one tap')
            print(tag, 'steps', seen)
            if seen != ORDER: F(tag, f'step order {seen} != {ORDER}')
            if pg.evaluate('TOUR.on'): F(tag, 'tour still on after Done')
            if errs: F(tag, f'page errors {errs[:2]}')
            # replay from the start
            pg.locator('[data-tour]').first.click(); time.sleep(.8)
            if not pg.evaluate("TOUR.on&&TSTEPS[TOUR.step].k==='tiles'"): F(tag, '"Take the tour" did not replay from step 1')
            br.close()
    # off-script (QA v75): picks toggle on the swipe steps, Back to the deck on step 4, Change mat on the racks step
    for (w, h) in ((390, 844), (390, 664)):
        tag = f'offscript-{w}x{h}'; br = p.chromium.launch(); pg = br.new_page(viewport={'width': w, 'height': h})
        pg.goto(URL); pg.wait_for_function('window.__imgsReady===true', timeout=90000); pg.wait_for_function('TOUR.on===true', timeout=6000); time.sleep(.8)
        def chk(label):
            time.sleep(.7); st = pg.evaluate(STATE)
            if st['inter'] or st['vis'] < .6: F(tag, f'{label}: tip box covers the target or target not in view (visible {st["vis"]})')
            return st
        pg.locator('#s-tiles .tgrid button').first.click(); time.sleep(.9)
        if pg.locator('.frow [data-her="m"]').count(): pg.locator('.frow [data-her="m"]').first.click(); chk('picks toggle on step 2')
        pg.locator('[data-yes="m"]').click(); time.sleep(.8); pg.locator('.tray .th button').first.click(); time.sleep(.8)
        pg.locator('[data-unpeek]').click(); st = chk('Back to the deck on step 4')
        if 'Tap Add racks once' in st['ctext']: F(tag, 'step 4 still says "Tap Add racks once" with no suitor picked')
        pg.locator('.tray .th button').first.click(); time.sleep(.7); pg.locator('.tray .go[data-mock]').click(); time.sleep(1)
        if pg.locator('.frow [data-her="r"]').count(): pg.locator('.frow [data-her="r"]').first.click(); chk('picks toggle on step 5')
        pg.locator('[data-back-mats]').click(); time.sleep(1)
        if pg.evaluate("document.getElementById('s-mats').getBoundingClientRect().bottom<0||document.getElementById('s-mats').getBoundingClientRect().top>innerHeight"): F(tag, 'Change mat during the tour did not scroll to the mats')
        if pg.evaluate("TOUR.log.length!==new Set(TOUR.log).size"): F(tag, f'tour step repeated: {pg.evaluate("TOUR.log")}')
        print(tag, 'log', pg.evaluate('TOUR.log')); br.close()
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 390, 'height': 844})
    pg.goto(URL + '#notour'); pg.wait_for_function('window.__imgsReady===true', timeout=90000); time.sleep(2.5)
    if pg.evaluate('TOUR.on'): F('notour', '#notour did not keep the tour off')
    br.close()
srv.terminate()
print('FAILS', fails)
sys.exit(1 if fails else 0)
