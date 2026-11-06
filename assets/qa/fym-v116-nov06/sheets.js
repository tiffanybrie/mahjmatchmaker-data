const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1500,height:1500}});
await p.goto('http://localhost:8116/index.html',{waitUntil:'load',timeout:120000});await p.waitForTimeout(2500);
const items=await p.evaluate(()=>{
 const tiles=D.sets.map((s,i)=>[s,i]).filter(([s])=>VIS(s)).map(([s,i])=>({k:'t',n:s.name,b:s.maker,src:(typeof pile==='function'?pile(s):'')}));
 const mats=Object.keys(M).filter(id=>!M[id].hid).map(id=>({k:'m',n:M[id].n,b:M[id].bn,src:matSrc(id)}));
 const racks=Object.keys(R).filter(id=>!R[id].hid&&!R[id].rt).map(id=>({k:'r',n:R[id].n,b:R[id].bn,src:(typeof rackSrc==='function'?rackSrc(id):'')}));
 return {tiles,mats,racks};});
console.log(items.tiles.length,items.mats.length,items.racks.length, items.tiles.filter(x=>!x.src).length, items.mats.filter(x=>!x.src).length, items.racks.filter(x=>!x.src).length);
const bad=[...items.tiles,...items.mats,...items.racks].filter(x=>/Mahjong Row|Mahjong by SI/.test(x.b)||(x.k==='m'&&/Mahjong Co\./.test(x.b)));console.log('BAD',bad.map(x=>x.n+'/'+x.b));
const out={};
for(const [kind,arr] of Object.entries(items)){const per=96;for(let pg=0;pg*per<arr.length;pg++){const chunk=arr.slice(pg*per,pg*per+per);
 await p.evaluate(({chunk,kind,pg})=>{let d=document.getElementById('__cs');if(d)d.remove();d=document.createElement('div');d.id='__cs';d.style.cssText='position:fixed;inset:0;z-index:99999;background:'+(kind==='r'||kind==='racks'?'#1d2b4a':'#fff')+';display:grid;grid-template-columns:repeat(12,1fr);gap:4px;padding:6px;overflow:hidden;font:9px sans-serif';
  d.innerHTML=chunk.map(x=>`<div style="text-align:center;background:#fff;overflow:hidden"><img src="${x.src}" style="width:100%;height:118px;object-fit:cover;display:block"><div style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${x.n}</div><div style="color:#888;white-space:nowrap;overflow:hidden">${x.b}</div></div>`).join('');document.body.appendChild(d);},{chunk,kind,pg});
 await p.waitForTimeout(1500);const f=`qa/sheets/${kind}-${String(pg+1).padStart(2,'0')}.jpg`;require('fs').mkdirSync('qa/sheets',{recursive:true});
 await p.evaluate(()=>Promise.all([...document.querySelectorAll('#__cs img')].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))));
 const broken=await p.evaluate(()=>[...document.querySelectorAll('#__cs img')].filter(i=>!i.naturalWidth).map(i=>i.parentElement.innerText.replace(/\n/g,' / ')));
 await p.screenshot({path:f,type:'jpeg',quality:80});out[f]=broken;}}
console.log(JSON.stringify(out,null,1));await b.close()})();
