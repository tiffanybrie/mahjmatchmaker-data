import asyncio,base64,subprocess,time,sys,json,os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(HERE,'out');os.makedirs(OUT,exist_ok=True)
COMBOS=[('sunday','Sunday','alb2:ozark-mah-jongg-carson-vintage'),('papaya','Papaya Spritz','brittmillsdesign.com/regency-scalloped-neoprene-mahjong-mat'),('pippa','Pippa','www.ohmymahjong.com/hampton-mat-in-tube')]
DIRS=sys.argv[1].split(',') if len(sys.argv)>1 else ['bands','spread','split']
FMTS=sys.argv[2].split(',') if len(sys.argv)>2 else ['fb','pin']
BEFORE='before' in sys.argv
def save(url,name):
    open(os.path.join(OUT,name),'wb').write(base64.b64decode(url.split(',',1)[1]))
async def main():
    srv=subprocess.Popen(['python3','-m','http.server','8766'],cwd=os.path.join(HERE,'serve'),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
    try:
        async with async_playwright() as p:
            b=await p.chromium.launch();pg=await b.new_page()
            pg.on('pageerror',lambda e:print('PAGEERR',e))
            await pg.goto('http://localhost:8766/index.html',wait_until='domcontentloaded',timeout=90000)
            await pg.wait_for_function('typeof D!=="undefined"&&D.sets&&typeof drawCard==="function"',timeout=90000)
            await pg.add_style_tag(content='@font-face{font-family:Caprasimo;src:url(Caprasimo.ttf)}')
            await pg.add_script_tag(path=os.path.join(HERE,'mock.js'))
            for key,sn,mid in COMBOS:
                for d in DIRS:
                    for f in FMTS:
                        r=await pg.evaluate('([d,s,m,f])=>MOCK.render(d,s,m,null,f)',[d,sn,mid,f])
                        save(r['url'],f'{d}_{key}_{f}.jpg');print(d,key,f,r['racks'],r['code'],r['tc'])
                if BEFORE:
                    for v in ['tri','stack','shop']:
                        u=await pg.evaluate('([s,m,f,v])=>MOCK.before(s,m,null,f,v)',[sn,mid,'fb',v])
                        if u: save(u,f'before_{v}_{key}_fb.jpg')
            await b.close()
    finally: srv.kill()
asyncio.run(main())
