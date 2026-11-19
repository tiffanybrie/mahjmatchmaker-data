const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});
await p.goto('file://'+process.cwd()+'/holiday-picks.html');await p.waitForTimeout(800);
await p.evaluate(()=>window.scrollTo(0,380));await p.waitForTimeout(400);await p.screenshot({path:'m1.png'});
await p.click('.combo');await p.waitForTimeout(400);await p.screenshot({path:'m2.png'});
await p.click('#lbtog');await p.waitForTimeout(300);await p.screenshot({path:'m3.png'});await b.close()})();
