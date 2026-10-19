import json,sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/fymfix2/ascripts')
import h
h.URL='http://127.0.0.1:8955/index.html'
from h import launch,page,sync_playwright
O='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/qa19/fym/'
SETS=['Papaya Spritz','Sunday','Coquette','Lagoon','Amara','Sierra','Drake','Heritage 2.0']
MATS=['Vivienne','Goldie','Larkspur','Greenly']
R={}
def sw(pg): return pg.evaluate('[document.documentElement.scrollWidth,innerWidth]')
with sync_playwright() as p:
    b=launch(p)
    for w,hh in ((390,844),(1280,900)):
        for name in SETS:
            pg=page(b,w,hh); r={}
            try:
                i=pg.evaluate('n=>D.sets.findIndex(s=>s.name===n)',name); r['idx']=i
                if i<0: R[f'{w}:{name}']={'missing':True}; pg.close(); continue
                pg.evaluate('i=>{S.set=i;S.tilesOpen=false;renderAll();jump&&jump("s-mats")}',i); pg.wait_for_timeout(2500)
                r['top_mat']=pg.evaluate('(()=>{const c=document.querySelector("#top-m");return c?M[c.dataset.id].n:null})()')
                r['top_img_ok']=pg.evaluate('(()=>{const im=document.querySelector("#top-m .ph img");return im?[im.naturalWidth,im.src.slice(0,30)]:null})()')
                pg.click('[data-yes="m"]'); pg.wait_for_timeout(600)
                if pg.query_selector('[data-mock]'):
                    pg.locator('[data-mock]').first.click(); pg.wait_for_timeout(1500)
                r['fav']=pg.evaluate('S.fav?M[S.fav].n:null')
                # racks: yes twice
                for k in range(2):
                    if pg.query_selector('[data-yes="r"]'): pg.locator('[data-yes="r"]').first.click(); pg.wait_for_timeout(500)
                r['rpick']=pg.evaluate('(S.rpick||[]).map(x=>R[x]?R[x].n:x)')
                # make card
                mk=pg.query_selector('[data-make]') or pg.query_selector('button:has-text("Make my match card")')
                if mk: mk.click(); pg.wait_for_timeout(2500)
                else: pg.evaluate('()=>{S.made=true;renderAll();jump("s-card")}'); pg.wait_for_timeout(2500)
                views=pg.eval_on_selector_all('[data-view]','e=>e.map(x=>x.dataset.view)')
                r['views']=views; r['cards']={}
                for v in views:
                    pg.click(f'[data-view="{v}"]'); pg.wait_for_timeout(4000)
                    el=pg.query_selector('#s-card')
                    if el:
                        el.scroll_into_view_if_needed()
                        info=pg.evaluate('(()=>{const c=document.querySelector("#s-card canvas")||document.querySelector("#s-card img");if(!c)return null;let blank=null;if(c.tagName==="CANVAS"){try{const x=c.getContext("2d").getImageData(c.width/2,c.height/2,1,1).data;blank=(x[3]===0)}catch(e){blank="taint"}}return [c.tagName,c.width||c.naturalWidth,c.height||c.naturalHeight,blank]})()')
                        r['cards'][v]=info
                        if name in ('Papaya Spritz','Sunday','Coquette') : el.screenshot(path=O+f'card_{name.replace(" ","_")}_{v}_{w}.jpg',type='jpeg',quality=60)
                r['shop']=pg.eval_on_selector_all('#s-card a[href], #s-shop a[href], .shop a[href]','e=>e.map(x=>x.href)')[:30]
                r['broken_imgs']=pg.evaluate('[...document.images].filter(i=>i.complete&&i.naturalWidth===0&&i.getAttribute("src")).map(i=>i.src.slice(0,80))')[:10]
                r['sw']=sw(pg)
            except Exception as e:
                r['exc']=str(e)[:200]
            r['errs']=pg.errs[:10]; r['fails']=pg.fails[:10]
            R[f'{w}:{name}']=r; pg.close()
        # mat door
        for q in MATS:
            pg=page(b,w,hh); r={}
            try:
                pg.click('[data-door="mat"]'); pg.wait_for_timeout(400)
                pg.fill('#mdq',q); pg.wait_for_timeout(600)
                hits=pg.eval_on_selector_all('#mdgrid button','e=>e.map(x=>[x.dataset.dmat,x.innerText.slice(0,40)])')
                r['hits']=hits[:5]
                if hits:
                    pg.click(f'#mdgrid button[data-dmat="{hits[0][0]}"]'); pg.wait_for_timeout(3000)
                    r['sets']=pg.eval_on_selector_all('.dsets button','e=>e.length'); r['her']=pg.eval_on_selector_all('.dsets button:has(b.her)','e=>e.length')
                    r['first_sets']=pg.eval_on_selector_all('.dsets button','e=>e.slice(0,4).map(x=>x.innerText.slice(0,30))')
                    pg.screenshot(path=O+f'door_{q}_{w}.jpg',type='jpeg',quality=55)
                    if r['sets']:
                        pg.locator('.dsets button').first.click(); pg.wait_for_timeout(2500)
                        r['after_pick_fav']=pg.evaluate('S.fav?M[S.fav].n:null'); r['after_pick_set']=pg.evaluate('S.set>=0?D.sets[S.set].name:null')
                        for k in range(2):
                            if pg.query_selector('[data-yes="r"]'): pg.locator('[data-yes="r"]').first.click(); pg.wait_for_timeout(500)
                        mk=pg.query_selector('[data-make]')
                        if mk: mk.click(); pg.wait_for_timeout(2500)
                        r['card']=pg.evaluate('(()=>{const c=document.querySelector("#s-card canvas")||document.querySelector("#s-card img");return c?[c.tagName,c.width||c.naturalWidth]:null})()')
                r['broken_imgs']=pg.evaluate('[...document.images].filter(i=>i.complete&&i.naturalWidth===0&&i.getAttribute("src")).map(i=>i.src.slice(0,80))')[:10]
                r['sw']=sw(pg)
            except Exception as e: r['exc']=str(e)[:200]
            r['errs']=pg.errs[:10]; r['fails']=pg.fails[:10]
            R[f'{w}:door:{q}']=r; pg.close()
    b.close()
json.dump(R,open(O+'res.json','w'),indent=1)
print(json.dumps(R,indent=1)[:9000])
