const {chromium}=require('playwright');(async()=>{const [inp,out,w]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:844}});
const errs=[];p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});p.on('requestfailed',r=>errs.push('FAIL '+r.url()));
await p.goto('file://'+inp);await p.evaluate(async()=>{for(const i of document.images){i.loading='eager'}});await p.waitForTimeout(2500);
const sw=await p.evaluate(()=>document.documentElement.scrollWidth);console.log('scrollWidth',sw);
await p.screenshot({path:out,fullPage:true,type:'jpeg',quality:70});console.log(errs.slice(0,10).join('\n'));await b.close()})();
