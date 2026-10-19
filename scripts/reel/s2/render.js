const {chromium}=require('playwright');const fs=require('fs');const {execSync}=require('child_process');
(async()=>{const eps=JSON.parse(fs.readFileSync('eps.json'));const tpl=fs.readFileSync('tpl.html','utf8');const b=await chromium.launch();
for(const [ep,name,tile] of eps){const n=String(parseInt(ep));const h=tpl.replace('__EP__',n).replace('__NAME__',name).replace('__TILE__',"'file://"+tile+"'");fs.writeFileSync(`op${ep}.html`,h);
const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+process.cwd()+`/op${ep}.html`);await p.evaluate(()=>document.fonts.ready);
await p.evaluate(()=>{const c=document.getElementById('c');let fs=150;while(c.scrollWidth>1000&&fs>70){fs-=4;c.style.fontSize=fs+'px'}});
fs.mkdirSync(`fr${ep}`,{recursive:true});for(let i=0;i<90;i++){await p.evaluate(t=>render(t),i/30);await p.screenshot({path:`fr${ep}/${String(i).padStart(3,'0')}.jpg`,type:'jpeg',quality:92});}
await p.close();execSync(`ffmpeg -v error -y -framerate 30 -i fr${ep}/%03d.jpg -c:v libx264 -pix_fmt yuv420p -crf 18 op${ep}.mp4 && rm -rf fr${ep}`);console.log('done',ep,name);}
await b.close()})();
