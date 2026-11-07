const pw=require('playwright');const fs=require('fs');const FILE=process.env.WEBFILE;
const orig=pw.chromium.launch.bind(pw.chromium);
pw.chromium.launch=async(o)=>{const b=await orig(o);const nc=b.newContext.bind(b);
 const hook=async c=>{await c.route('http://localhost:8117/index.html',r=>r.fulfill({status:200,contentType:'text/html; charset=utf-8',body:fs.readFileSync(FILE)}));return c};
 b.newContext=async(x)=>hook(await nc(x));
 b.newPage=async(x)=>{const c=await b.newContext(x);const p=await c.newPage();return p};return b};
