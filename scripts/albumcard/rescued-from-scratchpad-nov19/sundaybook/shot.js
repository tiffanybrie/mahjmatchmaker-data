const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});
await p.goto('file://'+process.cwd()+'/index.html');await p.waitForTimeout(2500);
const imgs=await p.$$eval('img',a=>a.filter(i=>i.src.length>1e5||/Humm/.test(i.alt||'')).map(i=>[i.alt,i.width,i.height]).slice(0,10));console.log(JSON.stringify(imgs));
await p.screenshot({path:'home.png'});
const el=await p.$('text=Hummingbird');if(el){await el.scrollIntoViewIfNeeded();await p.screenshot({path:'hb.png'});}
await b.close();})();
