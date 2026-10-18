import json,sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/fymfix2/ascripts')
import h
h.URL='http://127.0.0.1:8765/index.html'
from h import launch,page,sync_playwright
O='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/fympub_test/'
res={}
with sync_playwright() as p:
    b=launch(p)
    for w,hh in ((390,844),(1280,900)):
        pg=page(b,w,hh); r={}
        r['sw']=pg.evaluate('[document.documentElement.scrollWidth,innerWidth]')
        # tile door -> Papaya Spritz -> top mat full image (blob from .bin)
        if pg.query_selector('[data-tcol="az"]'): pg.click('[data-tcol="az"]')
        pg.wait_for_timeout(300)
        pg.click('#tgrid button:has-text("Papaya Spritz")'); pg.wait_for_timeout(4000)
        r['papaya_top']=pg.evaluate('(()=>{const c=document.querySelector("#top-m");return c?M[c.dataset.id].n:null})()')
        r['mc_bin_loaded']=pg.evaluate('Object.values(MC).filter(v=>String(v).startsWith("blob:")).length')
        r['mc_json_loaded']=pg.evaluate('Object.values(MC).filter(v=>String(v).startsWith("data:")).length')
        pg.screenshot(path=O+f'papaya_{w}.png')
        # card in all views (pick fav + racks like test_ui)
        views=pg.evaluate("""async()=>{const si=D.sets.findIndex(x=>x.name==='Papaya Spritz');S.set=si;S.fav=document.querySelector('#top-m').dataset.id;const hr=herRacks();S.rpick=(hr.length?hr:rackPool()).slice(0,2);S.made=true;renderAll();jump('s-card');return [...document.querySelectorAll('[data-view]')].map(b=>b.dataset.view+':'+b.textContent);}""")
        r['views']=views
        for v in [x.split(':')[0] for x in views]:
            pg.click(f'[data-view="{v}"]'); pg.wait_for_timeout(5000)
            el=pg.query_selector('#s-card'); el.scroll_into_view_if_needed()
            pg.screenshot(path=O+f'card_{v}_{w}.png')
            r['card_'+v]=pg.evaluate('(()=>{const c=document.querySelector("#s-card canvas, #s-card img");return c?(c.width||c.naturalWidth):0})()')
        r['broken']=pg.evaluate('[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src.slice(0,60))')
        # mat door
        pg.goto(h.URL); pg.wait_for_timeout(800)
        pg.click('[data-door="mat"]'); pg.wait_for_timeout(300)
        for q in ('Vivienne','Larkspur','Goldie'):
            pg.fill('#mdq',q); pg.wait_for_timeout(400)
            hits=pg.eval_on_selector_all('#mdgrid button','e=>e.map(x=>x.dataset.dmat)')
            r['door_'+q+'_hits']=len(hits)
            if hits:
                pg.click(f'#mdgrid button[data-dmat="{hits[0]}"]'); pg.wait_for_timeout(3000)
                r['door_'+q+'_sets']=pg.eval_on_selector_all('.dsets button','e=>e.length')
                r['door_'+q+'_her']=pg.eval_on_selector_all('.dsets button:has(b.her)','e=>e.length')
                r['door_'+q+'_broken']=pg.evaluate('[...document.images].filter(i=>i.complete&&i.naturalWidth===0).length')
                pg.screenshot(path=O+f'door_{q}_{w}.png')
                pg.click('[data-dchange]'); pg.wait_for_timeout(200)
        r['errs']=pg.errs[:8]; r['fails']=[f for f in pg.fails if 'favicon' not in f][:8]
        res[w]=r
    b.close()
json.dump(res,open(O+'res.json','w'),indent=1); print(json.dumps(res,indent=1))
