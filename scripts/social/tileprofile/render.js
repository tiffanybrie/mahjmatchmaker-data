const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');
(async()=>{const [html,meta,mp4,fps]=[process.argv[2],JSON.parse(fs.readFileSync(process.argv[3])),process.argv[4],+(process.argv[5]||30)];
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+html);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',String(fps),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-r',String(fps),mp4]);
const n=Math.round(meta.dur*fps);for(let i=0;i<n;i++){await p.evaluate(t=>render(t),i/fps);const buf=await p.screenshot({type:'jpeg',quality:92});ff.stdin.write(buf)}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('frames',n)})();
