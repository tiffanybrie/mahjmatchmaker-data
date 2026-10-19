// node shot.js W H in1.html out1.jpg [in2 out2 ...]
const {chromium}=require('playwright');(async()=>{const a=process.argv.slice(2);const W=+a[0],H=+a[1];const b=await chromium.launch();const p=await b.newPage({viewport:{width:W,height:H}});
for(let i=2;i<a.length;i+=2){await p.goto('file://'+a[i]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:a[i+1],type:'jpeg',quality:92});console.log(a[i+1])}await b.close()})();
