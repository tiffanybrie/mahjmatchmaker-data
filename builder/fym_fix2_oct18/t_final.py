from h import *
res={}
with sync_playwright() as p:
    b=launch(p)
    for w in (390,1280):
        pg=page(b,w,844 if w<500 else 900)
        # Jade: her list includes Watercolor Floral, not Butterfly
        r=pg.evaluate("""()=>{const i=D.sets.findIndex(s=>s.name==='Miss Classic Jade');S.set=i;return D.sets[i].m.map(x=>M[x[0]].n)}""")
        res[f'jade_{w}']=[n for n in r if n in ('Watercolor Floral','Butterfly')]
        # pick Jade via UI, mock Watercolor Floral, screenshot step 3
        pg.evaluate("""()=>{const i=D.sets.findIndex(s=>s.name==='Miss Classic Jade');resetFrom(1);S.set=i;S.f.m.her=true;resetFrom(2);S.tilesOpen=false;const id='www.wrenmats.com/watercolor-floral';S.liked=[id];S.seen[id]=1;S.fav=id;renderAll();}""")
        pg.wait_for_timeout(1200); pg.evaluate("document.getElementById('s-racks').scrollIntoView()"); pg.wait_for_timeout(500)
        pg.screenshot(path=f'{A}/shots/final_jade_wf_{w}.png')
        res[f'jade_racks_{w}']=pg.evaluate("rackPool().slice(0,6).map(r=>R[r].n)")
        # make the card
        btn=pg.locator('[data-make], .big').first
        res[f'scrollW_{w}']=pg.evaluate('document.documentElement.scrollWidth')
        # Après first mats
        res[f'apres_{w}']=pg.evaluate("D.sets.find(s=>s.name==='Après Ski Club').m.slice(0,4).map(x=>M[x[0]].n)")
        res[f'pippa_{w}']=pg.evaluate("D.sets.find(s=>s.name==='Pippa').m.slice(0,3).map(x=>M[x[0]].n)")
        res[f'woods_{w}']=pg.evaluate("Object.keys(R).filter(r=>/^bb:(Tudor|Almond|Weathered Oak|Provincial|Red Mahogany|Dark Walnut)$/.test(r)&&!R[r].hid)")
        res[f'uni_{w}']=pg.evaluate("UNI.map(r=>R[r].n)")
        # door search hunt club
        pg.evaluate("()=>{S.door='mat';S.dmat=null;renderAll&&renderAll();}"); pg.wait_for_timeout(600)
        if pg.locator('#mdq').count():
            pg.fill('#mdq','hunt club'); pg.wait_for_timeout(500)
            res[f'hunt_{w}']=pg.evaluate("[...document.querySelectorAll('#mdgrid button span')].map(e=>e.textContent)")
            pg.screenshot(path=f'{A}/shots/final_door_hunt_{w}.png')
        res[f'errs_{w}']=[e for e in pg.errs if 'favicon' not in e and '404' not in e]
        res[f'fails_{w}']=pg.fails
    b.close()
import json; print(json.dumps(res,indent=1,ensure_ascii=False))
