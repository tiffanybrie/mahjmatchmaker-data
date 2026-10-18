import asyncio,subprocess,time,json,os,sys
from playwright.async_api import async_playwright
SERVE='/home/claude/mahjmatchmaker-data/builder/card_redesign_oct18/serve'
COMBOS=[('Sunday','alb2:ozark-mah-jongg-carson-vintage'),('Papaya Spritz','brittmillsdesign.com/regency-scalloped-neoprene-mahjong-mat'),('Pippa','www.ohmymahjong.com/hampton-mat-in-tube')]
JS='''async ([sn,mid])=>{const si=D.sets.findIndex(x=>x.name===sn);S.set=si;S.fav=mid;const s=D.sets[si];
const hr=herRacks();const rp=(hr.length?hr:rackPool()).slice(0,3);
const dim=src=>new Promise(r=>{if(!src)return r(null);const i=new Image();i.onload=()=>r([i.naturalWidth,i.naturalHeight,String(src).slice(0,40)]);i.onerror=()=>r('err');i.src=src;});
const mf=await matFull(mid);
return {tile:await dim(pile(s)),tileKey:T[s.tile].pile,mat:await dim(mf),matTh:await dim(matTh(mid)),racks:await Promise.all(rp.map(async r=>[r,R[r].n,await dim(rackSrc(r))])),
logos:await Promise.all([T[s.tile].bn,M[mid].bn,...rp.map(r=>R[r].bn),'ours','icon'].map(async b=>[b,await dim(LG(b))]))};}'''
async def main():
    srv=subprocess.Popen(['python3','-m','http.server','8767'],cwd=SERVE,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
    try:
        async with async_playwright() as p:
            b=await p.chromium.launch();pg=await b.new_page()
            await pg.goto('http://localhost:8767/index.html',wait_until='domcontentloaded',timeout=90000)
            await pg.wait_for_function('typeof D!=="undefined"&&D.sets&&typeof drawCard==="function"',timeout=90000)
            for sn,mid in COMBOS:
                print(sn,json.dumps(await pg.evaluate(JS,[sn,mid])))
            await b.close()
    finally: srv.kill()
asyncio.run(main())
