const { chromium } = require('playwright');
const fs = require('fs');
const OUT = process.argv[2];
const sets = ['malachite','jade','dandy','palm-royale','limoncello','la-fete','luminaire','osler','lola','moonlight','nantucket','amara','glitterville','emerald','sorbet','spring-love','shangri-la','heritage','pippa','sunday-tile-set'];
const pages = [['holiday','https://www.mahjmatchmaker.com/holiday-mahjong-matches']].concat(sets.map(s=>[s,`https://www.mahjmatchmaker.com/${s}-mahjong-tile-matches`]));
(async()=>{
  const b = await chromium.launch();
  const results = [];
  for (const w of [390,1280]) {
    const ctx = await b.newContext({viewport:{width:w,height:900}, deviceScaleFactor: w===390?2:1});
    for (const [name,url] of pages) {
      const p = await ctx.newPage();
      let r = {name,w,url};
      try {
        const resp = await p.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
        r.status = resp.status();
        // scroll to trigger lazy load
        await p.evaluate(async()=>{const H=()=>document.body.scrollHeight;for(let y=0;y<H();y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,120));}window.scrollTo(0,H());});
        await p.waitForTimeout(2500);
        // force lazy imgs
        await p.evaluate(()=>document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager'));
        await p.waitForTimeout(2500);
        Object.assign(r, await p.evaluate(()=>{
          const vis = el => !!(el.offsetWidth||el.offsetHeight||el.getClientRects().length);
          const imgs=[...document.images].filter(i=>vis(i) && i.complete && i.naturalWidth===0 && i.currentSrc).map(i=>i.currentSrc);
          const pending=[...document.images].filter(i=>vis(i) && !i.complete).map(i=>i.currentSrc||i.src);
          const hscroll = document.documentElement.scrollWidth > window.innerWidth+1;
          const secs=[...document.querySelectorAll('section.mm3-hol, .mm3-hol')].map(s=>{
            const figs=[...s.querySelectorAll('figure.mm3-c')].map(f=>{
              const img=f.querySelector('img');
              const n=(f.querySelector('.mm3-n')||{}).textContent;
              return {n:n&&n.trim(), title:(f.querySelector('h3')||{}).textContent, src:img&&img.getAttribute('src'), nw:img&&img.naturalWidth, isNew: !!(img&&/holiday-late-nov04/.test(img.getAttribute('src')||'')),
                links:[...f.querySelectorAll('a[href]')].map(a=>a.href).filter(h=>!h.endsWith('#')), code: /MAHJMATCH/i.test(f.textContent), text:f.innerText.slice(0,400), hidden: !vis(f)};
            });
            return {id:s.id, hidden: !vis(s), figs};
          });
          return {broken:imgs, pending, hscroll, sw:document.documentElement.scrollWidth, secs};
        }));
        // screenshots of new figs
        const figsH = await p.$$('figure.mm3-c');
        let k=0;
        for (const f of figsH) {
          const isNew = await f.evaluate(f=>{const i=f.querySelector('img');return !!(i&&/holiday-late-nov04/.test(i.getAttribute('src')||''))&&!!(f.offsetWidth||f.offsetHeight);});
          if (!isNew) continue;
          await f.scrollIntoViewIfNeeded(); await p.waitForTimeout(300);
          await f.screenshot({path:`${OUT}/shot-${w}-${name}-${k++}.png`});
        }
      } catch(e) { r.err=String(e); }
      results.push(r); await p.close();
      console.log(w,name,r.status,r.err||'', 'broken',(r.broken||[]).length,'h',r.hscroll);
    }
    await ctx.close();
  }
  fs.writeFileSync(`${OUT}/results.json`, JSON.stringify(results,null,1));
  await b.close();
})();
