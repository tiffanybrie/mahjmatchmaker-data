import asyncio,json,subprocess,time,os
from playwright.async_api import async_playwright
B='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/fymfix2/build'
async def main():
    srv=subprocess.Popen(['python3','-m','http.server','8765'],cwd=B,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page()
        await pg.goto('http://localhost:8765/index.html');await pg.wait_for_timeout(3000)
        r=await pg.evaluate('''()=>{
         const fs=n=>D.sets.findIndex(s=>s.name===n);
         const fm=n=>Object.keys(M).filter(k=>M[k].n.toLowerCase().includes(n.toLowerCase())).map(k=>[k,M[k].n,M[k].bn,M[k].pa,M[k].nc]);
         const out={logos:Object.keys(D.logos),sets:{}};
         for(const n of ['Sunday','Papaya Spritz','Pippa']){const i=fs(n);const s=D.sets[i];out.sets[n]={i,tc:s.tc,tile:s.tile,bn:T[s.tile].bn,maker:s.maker,tag:s.tag,top:s.m.slice(0,3)};}
         out.mats={carson:fm('Carson'),regency:fm('Regency'),hampton:fm('Hampton')};
         return out;}''')
        print(json.dumps(r,indent=1)[:5000])
        await b.close()
    srv.kill()
asyncio.run(main())
