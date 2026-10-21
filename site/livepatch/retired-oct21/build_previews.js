const fs=require('fs'),T=require('./transforms.js');
const out={};
for (const f of fs.readdirSync('before')) {
  let h=fs.readFileSync('before/'+f,'utf8'), slug=f.replace('-mahjong-tile-matches.html','');
  let a;
  if (T.RET[slug]) a=T.albumHeader(h,slug); else { a=T.coverPills(h); out[f]=T.coverPills.count; }
  a=a.replace('<head>','<head><base href="https://www.mahjmatchmaker.com/">');
  fs.writeFileSync('after/'+f,a);
}
console.log(JSON.stringify(out));
