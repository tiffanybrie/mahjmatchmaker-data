// Called by holiday_numbering.py: node holiday_dom_check.js <slug...>; prints FAIL <slug>: ... when #holiday-matches sits inside .mm3-faq
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();let bad=0;
for(const s of process.argv.slice(2)){try{await p.goto('https://www.mahjmatchmaker.com/'+s+'?nc='+Date.now(),{waitUntil:'domcontentloaded',timeout:60000});
 const r=await p.evaluate(()=>{const h=document.getElementById('holiday-matches');return h?!!h.closest('.mm3-faq'):null});
 if(r){console.log('FAIL '+s+': holiday section sits inside the .mm3-faq wrapper');bad++}}catch(e){console.log('FAIL '+s+': load error '+e.message.slice(0,80));bad++}}
await b.close();process.exit(bad?1:0);})();
