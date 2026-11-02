"""[145] (v114 Table view + price filter, Nov 2). Runs the page's own code in WebKit iPhone at 390 / 375 / 340px:
 - tiles door: Papaya -> Table: the swipe card lands fully on screen; Adjust -> Swap mat 'Festive Plaid Premium' -> it is the current
   card; ♥ -> suitor -> Add racks -> Racks step with that mat, the rack card on screen
 - mat door: Larkspur -> Table -> Swap tiles to Dear Santa (not in Larkspur's deck) -> ♥ -> it is a suitor -> Add racks works
 - the sheet never carries data-mode (the app would read it as a View) and a tap on its heading leaves the app on Table
 - price chips never empty a deck silently (every chip: deck non-empty, or the 'so showing all' note)
 - no sideways slide at any step (scrollWidth <= innerWidth)
Usage: python3 fym_tableview_check.py <build dir>  -> prints FAIL lines ([145] ...), exit 1 on failure."""
import sys, time, subprocess, socket
from playwright.sync_api import sync_playwright
B = sys.argv[1]; s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', B], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
F = []
GEO = """sec=>{const c=document.querySelector('#'+sec+' .scard[id^="top-"]');const hd=document.querySelector('header.top');const H=hd?hd.getBoundingClientRect().bottom:0;
 const o={sw:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth),iw:innerWidth};if(c){const q=c.getBoundingClientRect();o.in=q.top>=H-4&&q.bottom<=innerHeight+2}return o}"""
def tap(pg, sel, text=None):
    l = pg.locator(sel, has_text=text) if text else pg.locator(sel)
    l = l.locator('visible=true').first; l.scroll_into_view_if_needed(); l.tap()
def chk(pg, L, sec, want_in=True):
    time.sleep(1.4); r = pg.evaluate(GEO, sec)
    if r['sw'] > r['iw'] + 1: F.append(f"[145] {L}: page {r['sw']}px wide on a {r['iw']}px screen")
    if want_in and r.get('in') is False: F.append(f"[145] {L}: the table card is not fully on screen after landing")
def boot(pg):
    pg.goto(f'http://127.0.0.1:{port}/index.html#notour'); pg.wait_for_function('window.__imgsReady===true', timeout=90000); time.sleep(1.2)
    try: pg.locator('[data-tour-skip]').first.click(timeout=3000)
    except Exception: pass
def synth(pg, a, v): pg.evaluate("([a,v])=>{const x=document.createElement('button');x.setAttribute(a,v);x.style.display='none';document.body.appendChild(x);x.click();x.remove()}", [a, str(v)])
def flow(pg, L):
    boot(pg)
    pi = pg.evaluate("D.sets.findIndex(s=>s.slug==='oh-my-mahjong-papaya-spritz')"); fest = pg.evaluate("Object.keys(M).find(k=>M[k].n==='Festive Plaid Premium'&&!M[k].hid)")
    synth(pg, 'data-tile', pi); time.sleep(1)
    tap(pg, '#s-mats [data-mode="table"]'); chk(pg, L + ' tiles door: Table', 's-mats')
    # price chips never empty the mat deck silently
    for v in pg.evaluate("TVD.pr.mat"):
        pg.evaluate(f"S.pr.m={v};renderMats()"); time.sleep(.2)
        r = pg.evaluate("({n:matDeck().length,e:S.prE.m,note:!!document.querySelector('#s-mats .prn')})")
        if not r['n']: F.append(f"[145] {L}: price chip under ${v} empties the mat deck")
        if r['e'] and 'so showing all' not in (pg.evaluate("(document.querySelector('#s-mats .prn')||{}).innerText||''")): F.append(f"[145] {L}: price chip under ${v} fell back without the note")
    pg.evaluate("S.pr.m='';renderMats()"); time.sleep(.3)
    tap(pg, '#s-mats [data-tvadj]'); time.sleep(.5)
    if pg.locator('#tvpanel[data-mode]').count(): F.append(f"[145] {L}: the Table sheet carries data-mode")
    tap(pg, '#tvpanel h3'); time.sleep(.3)
    if pg.evaluate("S.mode") != 'table': F.append(f"[145] {L}: a tap on the sheet heading changed the view to {pg.evaluate('S.mode')!r}")
    if fest:
        tap(pg, '#tvpanel [data-tvopen="mat"]'); pg.locator('#tvq').fill('festive plaid'); time.sleep(.5); tap(pg, '#tvgrid .tvit', 'Festive Plaid'); chk(pg, L + ' swap mat', 's-mats')
        if pg.evaluate("(document.querySelector('#top-m')||{dataset:{}}).dataset.id") != fest: F.append(f"[145] {L}: the swapped mat is not the current card")
        tap(pg, '#tvpanel [data-tvclose]'); tap(pg, '#s-mats .sbx [data-yes="m"]'); time.sleep(.8)
        tap(pg, f'#s-mats .tray [data-peek="{fest}"]'); time.sleep(.6); tap(pg, '#s-mats .acts.pk [data-mock]'); chk(pg, L + ' Racks after a swapped mat', 's-racks')
        if pg.evaluate("S.fav") != fest: F.append(f"[145] {L}: hearting the swapped mat did not carry it to Racks")
        # [146] rack filter = SINGLES (Tiffany Nov 1 11:33pm): one pick at a time across finish + colour, rows never shrink
        if pg.evaluate("document.body.innerHTML.includes('v114 singles')"):
            st = lambda: pg.evaluate("()=>({fin:S.f.r.fin||'',fam:S.f.r.fam.slice(),nf:document.querySelectorAll('#s-racks [data-fin]').length,nd:document.querySelectorAll('#s-racks [data-fam][data-k=\"r\"]').length})")
            c0 = st(); fins = pg.evaluate("[...document.querySelectorAll('#s-racks [data-fin]')].map(b=>b.dataset.fin)"); dots = pg.evaluate("[...document.querySelectorAll('#s-racks [data-fam][data-k=\"r\"]')].map(b=>b.dataset.fam).filter(Boolean)")
            if fins and len(dots) >= 2:
                cl = lambda sel: pg.locator(sel).first.evaluate('e=>e.click()')
                cl(f'#s-racks [data-fin="{fins[0]}"]'); time.sleep(.3); a1 = st()
                cl(f'#s-racks [data-fam="{dots[0]}"][data-k="r"]'); time.sleep(.3); a2 = st()
                cl(f'#s-racks [data-fam="{dots[1]}"][data-k="r"]'); time.sleep(.3); a3 = st()
                cl(f'#s-racks [data-fin="{fins[-1]}"]'); time.sleep(.3); a4 = st()
                cl('#s-racks [data-fam=""][data-k="r"]'); time.sleep(.3); a5 = st()
                if a1['fin'] != fins[0] or a1['fam']: F.append(f"[146] {L}: finish chip did not select alone: {a1}")
                if a2['fin'] or a2['fam'] != [dots[0]]: F.append(f"[146] {L}: a colour did not replace the finish: {a2}")
                if a3['fam'] != [dots[1]]: F.append(f"[146] {L}: a second colour did not replace the first: {a3}")
                if a4['fam'] or a4['fin'] != fins[-1]: F.append(f"[146] {L}: a finish did not replace the colour: {a4}")
                if a5['fin'] or a5['fam']: F.append(f"[146] {L}: the rainbow did not clear finish + colour: {a5}")
                if any((x['nf'], x['nd']) != (c0['nf'], c0['nd']) for x in (a1, a2, a3, a4, a5)): F.append(f"[146] {L}: a rack filter row changed length after a pick")
    # mat door
    boot(pg); lark = pg.evaluate("Object.keys(M).find(k=>M[k].n==='Larkspur'&&!M[k].hid)"); ds = pg.evaluate("D.sets.findIndex(s=>/dear santa/i.test(s.name))")
    if not lark or ds < 0: F.append(f"[145] {L}: test items Larkspur / Dear Santa missing"); return
    tap(pg, '[data-door="mat"]'); time.sleep(.6); synth(pg, 'data-dmat', lark); time.sleep(1.2)
    tap(pg, '#s-tiles [data-mode="table"]'); chk(pg, L + ' mat door: Table', 's-tiles')
    tap(pg, '#s-tiles [data-tvadj]'); tap(pg, '#tvpanel [data-tvopen="tiles"]'); pg.locator('#tvq').fill('dear santa'); time.sleep(.5); tap(pg, '#tvgrid .tvit', 'Dear Santa'); chk(pg, L + ' swap tiles', 's-tiles')
    tap(pg, '#tvpanel [data-tvclose]'); tap(pg, '#s-tiles .sbx [data-tyes]'); time.sleep(1)
    if not pg.locator(f'#s-tiles [data-tpk="{ds}"]').count(): F.append(f"[145] {L}: a swapped-in tile set (Dear Santa) did not become a suitor"); return
    tap(pg, f'#s-tiles [data-tpk="{ds}"]'); time.sleep(.6); tap(pg, '#s-tiles [data-tadd]'); chk(pg, L + ' Racks after swapped tiles', 's-racks')
    if pg.evaluate("S.set") != ds: F.append(f"[145] {L}: Add racks did not take the swapped tile set")
try:
    with sync_playwright() as p:
        br = p.webkit.launch()
        for vw in (390, 375, 340):
            ctx = br.new_context(**dict(p.devices['iPhone 13'], viewport={'width': vw, 'height': 664})); pg = ctx.new_page()
            errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
            pg.route('**/*', lambda r: r.abort() if ('supabase.co' in r.request.url or 'fonts.g' in r.request.url) else r.continue_())
            try: flow(pg, f'{vw}px')
            except Exception as e: F.append(f'[145] Table view check stopped at {vw}px: {str(e)[:200]}')
            for e in errs[:3]: F.append(f'[145] {vw}px page error: {e}')
            ctx.close()
        br.close()
except Exception as e: F.append(f'[145] Table view check did not run: {str(e)[:200]}')
srv.kill()
for f in F: print(f)
sys.exit(1 if F else 0)
