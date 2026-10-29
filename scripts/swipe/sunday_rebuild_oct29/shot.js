const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(1500);await p.screenshot({path:process.argv[3]});
console.log(await p.evaluate(()=>document.getElementById('tb').textContent+' | '+document.getElementById('foot').textContent));console.log('errs',errs);await b.close()})();
