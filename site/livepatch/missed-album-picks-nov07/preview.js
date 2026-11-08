// Dry run of missedFix on curls of the live pages: node preview.js <live_html_dir> <out_dir>
// <live_html_dir>/<page-slug>.html = curl of https://www.mahjmatchmaker.com/<page-slug> (holiday page: holiday-mahjong-matches.html).
// Writes <out_dir>/<page>.html (patched) and prints each page's note + checks (cards on page, grid numbering).
const fs = require('fs'), path = require('path');
const missedFix = require('./missed_fix.js');
const [, , LIVE, OUT] = process.argv; fs.mkdirSync(OUT, {recursive: true});
const man = JSON.parse(fs.readFileSync(path.join(__dirname, 'manifest.json'))).pages;
const css = fs.readFileSync(path.join(__dirname, 'holcss.html'), 'utf8');
let bad = 0; const hol = {};
for (const [pk, m] of Object.entries(man)) {
  const P = JSON.parse(fs.readFileSync(path.join(__dirname, m.file)));
  const isHol = pk.startsWith('holiday#');
  const file = isHol ? 'holiday-mahjong-matches.html' : pk + '-mahjong-tile-matches.html';
  let src = isHol && hol[file] ? hol[file] : fs.readFileSync(path.join(LIVE, file), 'utf8');
  try {
    const r = missedFix(src, P, isHol ? {sid: pk.split('#')[1]} : {css});
    const want = P.main.length + P.holiday.length;
    const got = (r.src.match(/assets\/cards\/missed-nov07\//g) || []).length - (src.match(/assets\/cards\/missed-nov07\//g) || []).length;
    const again = missedFix(r.src, P, isHol ? {sid: pk.split('#')[1]} : {css});
    const ok = got === want && again.note === 'already';
    if (!ok) bad++;
    console.log((ok ? 'OK  ' : 'BAD ') + pk + ' | +' + got + '/' + want + ' | ' + r.note);
    if (isHol) hol[file] = r.src; else fs.writeFileSync(path.join(OUT, file), r.src);
  } catch (e) { bad++; console.log('ERR ' + pk + ' | ' + e); }
}
for (const [f, s] of Object.entries(hol)) fs.writeFileSync(path.join(OUT, f), s);
console.log(bad ? bad + ' problems' : 'all pages OK');
process.exit(bad ? 1 : 0);
