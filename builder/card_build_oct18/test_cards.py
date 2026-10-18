"""Render every match-card view x size for 6 combos through the real FYM drawCard(); save exports + check console errors."""
import asyncio,base64,subprocess,time,os,sys,json
from playwright.async_api import async_playwright
SERVE='/home/claude/mahjmatchmaker-data/builder/card_redesign_oct18/serve'
OUT='/home/claude/mahjmatchmaker-data/builder/card_build_oct18/out';os.makedirs(OUT,exist_ok=True)
COMBOS=[('sunday','Sunday','alb2:ozark-mah-jongg-carson-vintage'),('papaya','Papaya Spritz','brittmillsdesign.com/regency-scalloped-neoprene-mahjong-mat'),('pippa','Pippa','www.ohmymahjong.com/hampton-mat-in-tube'),
 ('amara','Amara',None),('heritage2','Heritage 2.0',None),('coquette','Coquette',None)]
ONLY=sys.argv[1].split(',') if len(sys.argv)>1 else None
JS='''async ([sn,mid,view,fmt])=>{const si=D.sets.findIndex(x=>x.name===sn);S.set=si;S.fav=mid||D.sets[si].m[0][0];
 const hr=herRacks();S.rpick=(hr.length?hr:rackPool()).slice(0,2);S.view=view;S.fmt=fmt;S.step='card';
 if(!document.getElementById('prev')){const d=document.createElement('div');d.id='prev';document.body.appendChild(d);}
 await drawCard();return {url:cardURL,racks:S.rpick.map(r=>[r,rackLabel(r)]),mat:M[S.fav].n};}'''
async def main():
    srv=subprocess.Popen(['python3','-m','http.server','8768'],cwd=SERVE,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1);errs=[]
    try:
        async with async_playwright() as p:
            b=await p.chromium.launch();pg=await b.new_page()
            pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
            await pg.goto('http://localhost:8768/index.html',wait_until='domcontentloaded',timeout=90000)
            await pg.wait_for_function('typeof D!=="undefined"&&D.sets&&typeof drawCard==="function"',timeout=90000)
            await pg.add_style_tag(content='@font-face{font-family:Caprasimo;src:url(Caprasimo.ttf)}')
            for key,sn,mid in COMBOS:
                if ONLY and key not in ONLY:continue
                for v in ['tri','stack','shop']:
                    for f in ['fb','pin']:
                        r=await pg.evaluate(JS,[sn,mid,v,f])
                        open(f'{OUT}/{key}_{v}_{f}.jpg','wb').write(base64.b64decode(r['url'].split(',',1)[1]))
                print(key,r['mat'],r['racks'])
            await b.close()
    finally:srv.kill()
    print('errors',[e for e in errs if 'favicon' not in e][:10])
asyncio.run(main())
