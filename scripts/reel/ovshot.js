const { chromium } = require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();
for(const f of fs.readdirSync('/tmp/cc/reel').filter(x=>x.startsWith('ov-')&&x.endsWith('.html'))){const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file:///tmp/cc/reel/'+f);await p.waitForTimeout(400);await p.screenshot({path:'/tmp/cc/reel/'+f.replace('.html','.png'),omitBackground:true});await p.close();}
await b.close();})();
