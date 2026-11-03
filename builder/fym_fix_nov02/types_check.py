"""Gates [151] rack types + [152] Tiffany's picks default off + price dropdown (Tiffany Nov 3 2:48pm). Runs the page's own code in
WebKit (iPhone 13). [151]: every visible rack has exactly one valid type; config/rack-types-nov03.json covers every visible rack;
no painted rack (Bird & Bamboo colour, Bam Bird / Virora / My Fair Mahjong colour wood) is Wood tone; the row says 'Type' and has no
Walnut. [152]: picking tiles, the mat door and the rack step all start with picks OFF; her picks still lead the mat deck; the rack
deck is the full colour-theory deck; price is ONE dropdown (no chip block). Usage: python3 types_check.py <build dir>"""
import sys, time, subprocess, socket, json, re, os
from playwright.sync_api import sync_playwright
B = sys.argv[1]; R0 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
CFG = json.load(open(os.path.join(R0, 'config', 'rack-types-nov03.json'))); F = []
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', B], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
PAINTED = re.compile(r'^(Bird & Bamboo (?!(White Wood Stain|Clear Wood Stain|Weathered Oak|Provincial|Dark Walnut|Red Mahogany)$))|^Bam Bird Boutique (?!Walnut).*Wood$|^Virora .*Magnetic Wood$|^My Fair Mahjong (Macaron|Bright White)')
def synth(pg, a, v): pg.evaluate("([a,v])=>{const x=document.createElement('button');x.setAttribute(a,v);x.style.display='none';document.body.appendChild(x);x.click();x.remove()}", [a, str(v)])
try:
    with sync_playwright() as p:
        br = p.webkit.launch(); pg = br.new_context(**p.devices['iPhone 13']).new_page(); pg.goto(f'http://127.0.0.1:{port}/index.html#notour'); pg.wait_for_function('window.__imgsReady===true', timeout=90000)
        r = pg.evaluate("()=>{const v=Object.keys(R).filter(k=>!R[k].hid);return {v,bad:v.filter(k=>RFIN(k).length!==1||!FINS.includes(RFIN(k)[0])).map(k=>R[k].n),types:Object.fromEntries(v.map(k=>[k,RFIN(k)[0]])),names:Object.fromEntries(v.map(k=>[k,R[k].n])),fins:FINS}}")
        for n in r['bad'][:6]: F.append(f"[151] {n}: not exactly one rack type")
        miss = [r['names'][k] for k in r['v'] if k not in CFG['racks']]
        if miss: F.append(f"[151] {len(miss)} visible racks not in config/rack-types-nov03.json: {miss[:4]}")
        for k, t in r['types'].items():
            if t == 'wood' and PAINTED.search(r['names'][k]): F.append(f"[151] {r['names'][k]}: a painted rack is in Wood tone")
        if 'walnut' in r['fins'] or 'wood' not in r['fins'] or 'painted' not in r['fins']: F.append(f"[151] rack types must have Wood tone + Painted and no Walnut: {r['fins']}")
        # [152] picks default off
        i = pg.evaluate("D.sets.findIndex(s=>s.slug==='oh-my-mahjong-papaya-spritz')")
        try: pg.locator('[data-tour-skip]').first.click(timeout=2500)
        except Exception: pass
        synth(pg, 'data-tile', i); time.sleep(1)
        q = pg.evaluate("()=>({her:S.f.m.her,first:matDeck()[0],hm:set().m.map(x=>x[0]).filter(id=>M[id]&&!M[id].hid),sel:document.querySelectorAll('#s-mats select[data-prsel]').length,chips:document.querySelectorAll('#s-mats .prc').length})")
        if q['her']: F.append("[152] picking a tile set turns Tiffany's picks ON (default must be off)")
        if q['hm'] and q['first'] not in q['hm']: F.append("[152] with picks off, Tiffany's own matches no longer lead the mat deck")
        if q['sel'] != 1 or q['chips']: F.append(f"[152] price on the mat deck is not one dropdown (select {q['sel']}, chips {q['chips']})")
        m = q['first']; pg.evaluate("m=>{S.liked=[m];S.fav=m;S._rdef=null;renderRacks()}", m); time.sleep(.8)
        q = pg.evaluate("()=>({her:S.f.r.her,n:rackDeck().length,h:herRacks().length,type:(document.querySelector('#s-racks .finrow .fl')||{}).textContent})")
        if q['her']: F.append("[152] the rack step starts with Tiffany's picks ON (default must be off)")
        if q['h'] and q['n'] <= q['h']: F.append("[152] the rack deck is limited to Tiffany's picks by default")
        if q['type'] != 'Type': F.append(f"[151] rack filter row label is {q['type']!r} (want 'Type')")
        pg.goto(f'http://127.0.0.1:{port}/index.html#notour'); pg.wait_for_function('window.__imgsReady===true', timeout=90000)
        mm = pg.evaluate("Object.keys(M).find(k=>M[k].n==='Larkspur'&&!M[k].hid)")
        synth(pg, 'data-door', 'mat'); time.sleep(.4); synth(pg, 'data-dmat', mm); time.sleep(1)
        ds = pg.evaluate("setsForMat(S.dmat)"); si = (ds.get('her') or ds.get('alb') or ds.get('cat') or [{}])[0].get('i')
        if si is not None:
            synth(pg, 'data-dset', si); time.sleep(.8)
            if pg.evaluate("S.f.m.her"): F.append("[152] the mat door turns Tiffany's picks ON (default must be off)")
        br.close()
finally: srv.kill()
for f in F: print(f)
print('types check', 'FAIL' if F else 'ok'); sys.exit(1 if F else 0)
