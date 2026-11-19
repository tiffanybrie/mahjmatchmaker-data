const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});
await p.goto('file://'+process.cwd()+'/index.html');await p.waitForTimeout(2000);
await p.mouse.click(33,29);await p.waitForTimeout(800);await p.screenshot({path:'menu.png'});
const l=p.locator('text=Hummingbird').first();await l.click();await p.waitForTimeout(1500);await p.screenshot({path:'hb.png'});await b.close();})();
