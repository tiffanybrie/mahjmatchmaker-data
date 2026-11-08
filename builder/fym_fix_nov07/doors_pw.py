"""FYM 1.18 door-parity QA in a real browser (Chromium) at 390px (touch) and 1440px: mat door -> Lotus Cove -> tiles step ->
Brand = Oh My Mahjong -> only OMM tiles; 'Same brand as my mat' chip; Clear; colour group + Holiday; filters never empty the deck;
'See all' grid filters; tiles door grid (in stock + price) and its mat deck 'Same brand as my tiles'; racks step same-brand chips;
Table view swap sheet (same brand in the Brand menu, Holiday on the Mat tab). Screenshots to <shot_dir>.
Usage: python3 builder/fym_fix_nov07/doors_pw.py <build_dir> <shot_dir>   (build_dir holds index.html + the b*v*.js bundles)
Prints PASS/FAIL lines, exit 1 on any FAIL."""
import sys, time, subprocess, socket, os
from playwright.sync_api import sync_playwright
B, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', B], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
R = []
OMM = 'Oh My Mahjong'
def ok(L, cond, info=''):
    R.append((bool(cond), L)); print(('PASS ' if cond else 'FAIL ') + L + ('' if cond else f'  {info}'), flush=True)
def boot(pg):
    pg.goto('about:blank'); pg.goto(f'http://127.0.0.1:{port}/index.html#notour'); pg.wait_for_function('window.__imgsReady===true', timeout=90000); time.sleep(1.2)
    try: pg.locator('[data-tour-skip]').first.click(timeout=2000)
    except Exception: pass
def click(pg, sel, i=0):
    el = pg.locator(sel).locator('visible=true').nth(i); el.scroll_into_view_if_needed(); el.click(); time.sleep(.6)
def shot(pg, name, sel=None):
    if sel:
        try: pg.locator(sel).first.scroll_into_view_if_needed()
        except Exception: pass
        time.sleep(.4)
    pg.screenshot(path=f'{OUT}/{name}.png')
TS = "()=>{const A=tAll();return {n:A.length,omm:A.filter(r=>TBM(r.s,'Oh My Mahjong')).length,f:Object.assign({},S.f.t),e:S.tfE}}"
def overflow(pg): return pg.evaluate('()=>document.documentElement.scrollWidth-innerWidth')

def run(pg, W, touch):
    L = f'{W}px'; errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    boot(pg)
    # ---------- MAT DOOR ----------
    click(pg, '[data-door="mat"]')
    ok(f'{L} mat door step 1: price dropdown', pg.locator('#s-tiles [data-prsel="m"]').count() == 1)
    ok(f'{L} mat door step 1: in stock + brand dropdown + colours still there', pg.locator('#s-tiles [data-ins]').count() and pg.locator('#mbr').count() and pg.locator('#s-tiles [data-dfam="holiday"]').count())
    v = pg.evaluate("()=>{const s=document.querySelector('#s-tiles [data-prsel=\"m\"]');return s.options[2].value}")
    pg.select_option('#s-tiles [data-prsel="m"]', v); time.sleep(.8)
    ok(f'{L} mat door step 1: price filters the mat grid (price lines shown)', pg.locator('#mdgrid .prc1').count() > 0, pg.locator('#mdgrid .prc1').count())
    shot(pg, f'{W}_1_matdoor_grid_price', '#s-tiles .gprw')
    pg.select_option('#s-tiles [data-prsel="m"]', ''); time.sleep(.6)
    ok(f'{L} mat door step 1: Any price clears', pg.locator('#mdgrid .prc1').count() == 0)
    pg.fill('#mdq', 'lotus cove'); time.sleep(.6)
    click(pg, '#mdgrid [data-dmat="www.ohmymahjong.com/lotus-cove-mat-in-tube"]'); time.sleep(.8)
    t0 = pg.evaluate(TS)
    ok(f'{L} Lotus Cove: tiles step has the filter row (in stock, price, brand, same brand, holiday/colours)',
       all(pg.locator('#s-tiles .tfil ' + x).count() for x in ('[data-ins]', '[data-prsel="t"]', '[data-tbrands]', '[data-sameb="t"]', '[data-tfam=""]')), t0)
    ok(f'{L} Lotus Cove: unfiltered tiles deck has other brands too', t0['n'] > t0['omm'] > 0, t0)
    ok(f'{L} no horizontal page scroll on the tiles step', overflow(pg) <= 0, overflow(pg))
    shot(pg, f'{W}_2_lotus_tiles_step', '#s-tiles .tfil')
    # Brand sheet -> Oh My Mahjong
    click(pg, '#s-tiles [data-tbrands]'); time.sleep(.4)
    shot(pg, f'{W}_3_tile_brand_sheet')
    pg.locator('.sheet [data-b="Oh My Mahjong"]').click(); time.sleep(.8)
    t1 = pg.evaluate(TS)
    ok(f'{L} Brand = Oh My Mahjong -> only OMM tile sets', t1['n'] == t1['omm'] and t1['n'] > 0 and not t1['e'], t1)
    top = pg.evaluate("()=>{const c=document.querySelector('#top-t');return c?D.sets[+c.dataset.i].maker:null}")
    ok(f'{L} top tile card is OMM', top and OMM in top, top)
    shot(pg, f'{W}_4_brand_omm', '#s-tiles .tfil')
    click(pg, '#s-tiles [data-tbrands]')  # 'Oh My Mahjong ✕' clears
    t2 = pg.evaluate(TS); ok(f'{L} tapping the brand chip again clears it', t2['n'] == t0['n'] and not t2['f']['brand'], t2)
    # same brand chip
    click(pg, '#s-tiles [data-sameb="t"]')
    t3 = pg.evaluate(TS); ok(f'{L} "Same brand as my mat" -> only OMM tile sets', t3['n'] == t3['omm'] == t1['n'] and t3['f']['brand'] == OMM, t3)
    ok(f'{L} same-brand chip shows pressed', pg.locator('#s-tiles [data-sameb="t"][aria-pressed="true"]').count() == 1)
    shot(pg, f'{W}_5_same_brand_on', '#s-tiles .tfil')
    # swipe still works with the lock on
    li = pg.evaluate('()=>S.tliked.length'); click(pg, '#s-tiles .acts [data-tyes]'); time.sleep(.5)
    ok(f'{L} heart still works with the brand lock', pg.evaluate('()=>S.tliked.length') == li + 1)
    t3b = pg.evaluate(TS); ok(f'{L} next card still OMM after a swipe', t3b['n'] == t3b['omm'], t3b)
    click(pg, '#s-tiles [data-tclear]')
    t4 = pg.evaluate(TS); ok(f'{L} Clear clears every tile filter', t4['n'] == t0['n'] and not (t4['f']['brand'] or t4['f']['fam'] or t4['f']['her']), t4)
    # colour group
    g = pg.evaluate("()=>{const b=[...document.querySelectorAll('#s-tiles .tfil [data-tfam]')].map(x=>x.dataset.tfam).filter(x=>x&&x!=='Holiday');return b[0]}")
    click(pg, f'#s-tiles .tfil [data-tfam="{g}"]')
    t5 = pg.evaluate("g=>{const A=tAll();return {n:A.length,ing:A.filter(r=>TGR(r.s).includes(g)).length}}", g)
    ok(f'{L} colour group "{g}" -> only that group', t5['n'] == t5['ing'] > 0, t5)
    click(pg, f'#s-tiles .tfil [data-tfam="{g}"]')
    ok(f'{L} tapping the colour again clears it', pg.evaluate(TS)['n'] == t0['n'])
    # a combination with no sets never empties the deck
    G0 = pg.evaluate("()=>{const A=tAll();const gs=tileOrder();return gs.find(G=>A.some(r=>TGR(r.s).includes(G))&&!A.some(r=>TGR(r.s).includes(G)&&TBM(r.s,'Oh My Mahjong')))||null}")
    if G0:
        click(pg, '#s-tiles [data-sameb="t"]'); click(pg, f'#s-tiles .tfil [data-tfam="{G0}"]')
        t6 = pg.evaluate(TS); ok(f'{L} OMM + "{G0}" (no such set) shows all with a note + Clear', t6['e'] == 1 and t6['n'] == t0['n'] and pg.locator('#s-tiles .tfil [data-tclear]').count() == 1, t6)
        shot(pg, f'{W}_6_empty_combo_note', '#s-tiles .tfil')
        click(pg, '#s-tiles [data-tclear]')
    # See all grid
    click(pg, '#s-tiles [data-sameb="t"]'); click(pg, '#s-tiles [data-dgrid="1"]')
    mk = pg.evaluate("()=>[...document.querySelectorAll('#s-tiles .dsets [data-dset]')].map(b=>D.sets[+b.dataset.dset].maker)")
    ok(f'{L} See all grid: filter row + only OMM sets', pg.locator('#s-tiles .dgctl [data-sameb="t"][aria-pressed="true"]').count() == 1 and mk and all(OMM in m for m in mk), mk[:5])
    shot(pg, f'{W}_7_seeall_grid_omm', '#s-tiles .dgctl')
    click(pg, '#s-tiles [data-dgrid="0"]')
    # Table view swap sheet, tiles tab
    click(pg, '#s-tiles [data-mode="table"]'); time.sleep(1)
    try:
        pg.evaluate("()=>{const b=document.querySelector('[data-tvadj]');b&&b.click()}"); time.sleep(.6)
        pg.evaluate("()=>{const b=document.querySelector('[data-tvopen=\"tiles\"]');b&&b.click()}"); time.sleep(.6)
        pg.evaluate("()=>document.getElementById('tvbrand').click()"); time.sleep(.4)
        same = pg.locator('#tvpop .tvsame')
        ok(f'{L} Table view Tiles tab: Brand menu offers "Same brand as my mat · Oh My Mahjong"', same.count() == 1 and OMM in same.first.inner_text(), same.count())
        shot(pg, f'{W}_8_table_tiles_brandmenu')
        same.first.evaluate('e=>e.click()'); time.sleep(.5)
        bns = pg.evaluate("()=>[...document.querySelectorAll('#tvgrid .tvit .bn')].map(x=>x.textContent)")
        ok(f'{L} Table view: same brand -> only OMM tile sets', bns and all(b == OMM for b in bns), bns[:6])
        pg.evaluate("()=>document.querySelector('[data-tvtab=\"mat\"]').click()"); time.sleep(.5)
        ok(f'{L} Table view Mat tab: Holiday chip', pg.locator('#tvdots [data-tvc="holiday"]').count() == 1)
        pg.evaluate("()=>document.querySelector('#tvdots [data-tvc=\"holiday\"]').click()"); time.sleep(.5)
        hol = pg.evaluate("()=>{const r=[...document.querySelectorAll('#tvgrid .tvit')].length;return r}")
        ok(f'{L} Table view Holiday chip filters to holiday mats', hol > 0, hol)
        shot(pg, f'{W}_9_table_mat_holiday')
        pg.evaluate("()=>{const b=document.querySelector('[data-tvclose]');b&&b.click()}"); time.sleep(.4)
    finally:
        pg.evaluate("()=>{const b=document.querySelector('[data-mode=\"close\"]');b&&b.click()}"); time.sleep(.8)
    # pick tiles -> racks step same brand chips
    pg.evaluate("()=>{const i=tq()[0].i;const x=document.createElement('button');x.setAttribute('data-tadd',i);document.body.appendChild(x);x.click();x.remove()}"); time.sleep(1.2)
    rs = pg.locator('#s-racks [data-sameb="r"]')
    ok(f'{L} racks step: same-brand chip(s)', rs.count() >= 1, rs.count())
    if rs.count():
        b = rs.first.get_attribute('data-b'); rs.first.scroll_into_view_if_needed(); rs.first.click(); time.sleep(.6)
        rb = pg.evaluate("()=>[...new Set(rackDeck().map(r=>R[r].bn))]")
        ok(f'{L} racks "Same brand as my ..." -> only {b} racks', rb == [b], rb)
        shot(pg, f'{W}_10_racks_same_brand', '#s-racks .rfil')
        pg.locator('#s-racks [data-sameb="r"]').first.click(); time.sleep(.5)
        ok(f'{L} racks same brand clears on a 2nd tap', pg.evaluate("()=>S.f.r.brand") == '')
    # ---------- TILES DOOR ----------
    boot(pg); click(pg, '[data-door="tiles"]')
    ok(f'{L} tiles door step 1: brand logos by default (unchanged)', pg.locator('#blv').count() == 1)
    ok(f'{L} tiles door step 1: in stock + price added', pg.locator('#s-tiles .tchips [data-ins]').count() == 1 and pg.locator('#s-tiles [data-prsel="t"]').count() == 1)
    shot(pg, f'{W}_11_tilesdoor_step1', '#s-tiles .tfind')
    click(pg, '#s-tiles .tchips [data-ins]')
    ok(f'{L} tiles door: In stock only shows the (in-stock) A-Z list', pg.locator('#tgrid [data-tile]').count() > 0 and pg.locator('#blv').count() == 0)
    oos = pg.evaluate("()=>[...document.querySelectorAll('#tgrid [data-tile]')].filter(b=>OOS('t',D.sets[+b.dataset.tile].tile)).length")
    ok(f'{L} tiles door: no sold-out set with In stock only', oos == 0, oos)
    click(pg, '#s-tiles .tchips [data-ins]')
    ok(f'{L} tiles door: In stock off -> logos back', pg.locator('#blv').count() == 1)
    pg.select_option('#tbr', OMM); time.sleep(.6)
    n_omm = pg.locator('#tgrid [data-tile]').count(); ok(f'{L} tiles door brand dropdown still works ({n_omm} OMM sets)', n_omm > 5)
    i0 = pg.evaluate("()=>+document.querySelector('#tgrid [data-tile]').dataset.tile")
    click(pg, f'#tgrid [data-tile="{i0}"]'); time.sleep(1)
    ms = pg.locator('#s-mats [data-sameb="m"]')
    ok(f'{L} mat deck: "Same brand as my tiles" chip', ms.count() == 1, ms.count())
    if ms.count():
        ms.first.scroll_into_view_if_needed(); ms.first.click(); time.sleep(.7)
        mb = pg.evaluate("()=>[...new Set(queue('m').map(id=>M[id].bn))]")
        ok(f'{L} mat deck same brand -> only OMM mats', mb == [OMM], mb)
        shot(pg, f'{W}_12_matdeck_same_brand', '#s-mats .rfil')
        pg.locator('#s-mats [data-sameb="m"]').first.click(); time.sleep(.6)
        ok(f'{L} mat deck same brand clears', pg.evaluate("()=>S.f.m.brand") == '')
    ok(f'{L} mat deck controls unchanged (picks/brand/colours/holiday/add colour/price/in stock)', all(pg.locator('#s-mats ' + x).count() for x in ('[data-brands="m"]', '[data-fam=""]', '[data-fmulti="m"]', '[data-prsel="m"]', '[data-ins]')))
    ok(f'{L} no horizontal page scroll (tiles door)', overflow(pg) <= 0, overflow(pg))
    ok(f'{L} no page errors', not errs, errs[:3])

with sync_playwright() as p:
    br = p.chromium.launch()
    for W, H, touch in ((390, 844, True), (1440, 900, False)):
        ctx = br.new_context(viewport={'width': W, 'height': H}, has_touch=touch, is_mobile=touch, device_scale_factor=2 if touch else 1)
        pg = ctx.new_page()
        try: run(pg, W, touch)
        except Exception as e: ok(f'{W}px run finished', False, repr(e)[:400]); shot(pg, f'{W}_crash')
        ctx.close()
    br.close()
srv.terminate()
n = sum(1 for x in R if not x[0]); print(f'\nDOORS QA: {"PASS" if not n else "FAIL"} ({len(R) - n}/{len(R)})'); sys.exit(1 if n else 0)
