import sys,json,base64,re,os
from playwright.sync_api import sync_playwright
JS=open(os.path.dirname(os.path.abspath(__file__))+'/gen.js').read()
brands=sys.argv[1:]; out=os.environ.get('OUT','cards')
os.makedirs(out,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844})
    pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(5000)
    for B in brands:
        res=pg.evaluate(JS,[B,3,json.loads(os.environ.get('EX','[]'))]); slug=re.sub(r'[^a-z0-9]+','-',B.lower()).strip('-')
        for k,r in enumerate(res):
            if r['url']: open(f'{out}/{slug}-{k+1}.jpg','wb').write(base64.b64decode(r['url'].split(',')[1]))
            r.pop('url'); print(B,k+1,json.dumps(r))
    b.close()
