import os,json
os.environ['TMPDIR']='/dev/shm/fym-holiday'
from playwright.sync_api import sync_playwright
O='/dev/shm/fym-holiday/caps/'; os.makedirs(O,exist_ok=True)
def start(p,scale=3):
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=scale)
    pg.goto('http://127.0.0.1:8791/index.html?tour=off'); pg.wait_for_timeout(8000)
    pg.add_style_tag(content='.swh{display:none!important}')
    return b,pg
def shot(pg,n): pg.screenshot(path=O+n+'.png'); print('shot',n)
def ev(pg,js,*a): return pg.evaluate(js,*a)
def pick(pg,q,name):
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type(q); pg.wait_for_timeout(1300)
    ev(pg,"(t)=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.includes(t)).click()",name); pg.wait_for_timeout(3000)
def to(pg,sel,off):
    ev(pg,f"()=>{{const d=document.querySelector('{sel}');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-{off})}}"); pg.wait_for_timeout(900)
def front(pg,name):
    k=ev(pg,"(n)=>Object.keys(M).find(k=>M[k].n===n&&!M[k].hid&&matDeck().includes(k))",name); assert k,name
    ev(pg,"(k)=>{S.mfront=k;S.mfset=S.set;renderAll()}",k); pg.wait_for_timeout(1300); return k
def bbox(pg,sel_js):
    return ev(pg,f"()=>{{const e=({sel_js});if(!e)return null;const q=e.getBoundingClientRect();return [q.left,q.top,q.width,q.height]}}")
