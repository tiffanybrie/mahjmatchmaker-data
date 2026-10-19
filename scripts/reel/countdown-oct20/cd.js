const {chromium}=require('playwright');
const C=[
['7','days','coquette.jpg','Your tiles are about to get<br>a <b>dating app.</b>'],
['6','days','malachite.jpg','His bio says “not into matching.”<br><b>We\'ll see.</b>'],
['5','days','pippa.jpg','Single tiles in your area<br>are looking for <b>a mat.</b>'],
['4','days','smith.jpg','Already own a mat?<br>It\'s been getting <b>matches too.</b>'],
['3','days','solara.jpg','Racks are invited.<br><b>Obviously.</b>'],
['2','days','talulah.jpg','Hundreds of mats are fixing<br>their hair <b>right now.</b>'],
['1','day','jade.jpg','Tomorrow, your tiles<br>meet <b>their match.</b>'],
['LIVE','today','coquette.jpg','Find Your Match is <b>here.</b><br>Link in bio.',1,'file:///home/claude/mahjmatchmaker-data/assets/mats/gallery/middle-main-mahjong--martha-mae-vintage-quilt.webp','MAHJ MATCHMAKER 2.0']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/cd.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
for(const [n,d,t,l,big,mat,pill] of C){await p.evaluate(o=>setCard(o),{n,d,t,l,big,mat,pill});await p.waitForTimeout(300);
await p.screenshot({path:`cd/countdown-${n==='LIVE'?'0-live':n}.jpg`,type:'jpeg',quality:90})}
await b.close()})();
