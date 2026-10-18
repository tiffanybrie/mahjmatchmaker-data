import json,sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/fymfix2/ascripts')
import h
h.URL='http://127.0.0.1:8765/index.html'
from h import launch,page,sync_playwright
O='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/fymfix2/f3/test/'
res={}
with sync_playwright() as p:
    b=launch(p)
    for w,hh in ((390,844),(1280,900)):
        pg=page(b,w,hh)
        r={}
        r['sw']=pg.evaluate('[document.documentElement.scrollWidth,innerWidth]')
        # tile door: Papaya Spritz first mats
        pg.click('[data-tcol="az"]') if pg.query_selector('[data-tcol="az"]') else None
        pg.wait_for_timeout(300)
        btn=pg.query_selector('#tgrid button:has-text("Papaya Spritz")')
        if btn:
            btn.click(); pg.wait_for_timeout(1500)
            r['papaya_top']=pg.evaluate('(()=>{const c=document.querySelector("#top-m");return c?M[c.dataset.id].n:null})()')
            pg.wait_for_timeout(2500); pg.screenshot(path=O+f'papaya_{w}.png')
        r['glitter_glow_sets']=pg.evaluate('D.sets.filter(s=>/Glitter Glow/.test(s.name)).length')
        r['mat_imgs_broken']=pg.evaluate('[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src.slice(0,60))')
        # mat door: Knox, Chinoiserie Songbird, Goldie, Caroline
        pg.goto(h.URL); pg.wait_for_timeout(800)
        pg.click('[data-door="mat"]'); pg.wait_for_timeout(300)
        for q,id in (('Knox','brittmillsdesign.com/knox-neoprene-mahjong-mat'),('Chinoiserie Songbird','mahjandvine.com/chinoiserie-song-bird'),('Goldie','alb:amara:Goldie'),('Caroline','mahjandvine.com/caroline-in-peacock'),('Savannah Leatherette','brittmillsdesign.com/savannah-leatherette-mahjong-mat')):
            pg.fill('#mdq',q); pg.wait_for_timeout(300)
            hits=pg.eval_on_selector_all('#mdgrid button','e=>e.map(x=>x.dataset.dmat)')
            r['door_'+q]=id in hits
            if id in hits:
                pg.click(f'#mdgrid button[data-dmat="{id}"]'); pg.wait_for_timeout(2500)
                r['door_'+q+'_her']=pg.eval_on_selector_all('.dsets button:has(b.her)','e=>e.length')
                pg.screenshot(path=O+f'door_{q.replace(" ","_")}_{w}.png')
                pg.click('[data-dchange]'); pg.wait_for_timeout(200)
        r['errs']=pg.errs[:8]; r['fails']=[f for f in pg.fails if 'favicon' not in f][:8]
        res[w]=r
    b.close()
json.dump(res,open(O+'res.json','w'),indent=1); print(json.dumps(res,indent=1))
