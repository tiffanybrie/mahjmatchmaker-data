// FYM gate [166b] (Nov 8, FYM 1.18 QA F2 + QA2 Q2: across every See all section): runs the page's OWN code in node (tiny DOM stub, same harness as fym_matdoor_check.js)
// for the mat door -> tile deck with a price chosen. For Lotus Cove (OMM) + 'Under $175' (and 4 more mats x every price option):
//   deck  = tAll() (what the swipe deck deals): no priced set after an unpriced one; no priced set over the limit; tile-rank order (p)
//           holds inside the priced album+catalog group and inside the unpriced one, apart from the brand cap (BCAP) moves.
//   grid  = setsForMat() sections her / alb / cat ('See all'): inside each section no priced set after an unpriced one.
// Usage: node builder/fym_fix_nov07/tiledeckprice_check.js <build_dir | index.html>  -> JSON {fails:[...], notes:[...]}; exit 0 always
const fs = require('fs'), vm = require('vm'), path = require('path');
const A = process.argv[2]; const P = A.endsWith('.html') ? A : path.join(A, 'index.html');
const html = fs.readFileSync(P, 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const F = [], N = [];
const els = {}, appended = [];
function El(id) { return { id, innerHTML: '', style: {}, value: '', title: '', classList: { add() {}, remove() {}, contains() { return false; } }, dataset: {}, setAttribute() {}, getAttribute() { return null; }, addEventListener() {}, appendChild(c) { appended.push(c); }, remove() {}, querySelector() { return null; }, querySelectorAll() { return []; }, getBoundingClientRect() { return { top: 0, left: 0, width: 390, height: 600 }; }, focus() {} }; }
const KNOWN = ['s-tiles', 's-mats', 's-racks', 's-card', 'stp', 'logo'];
const document = {
  getElementById: id => KNOWN.includes(id) ? (els[id] = els[id] || El(id)) : null,
  addEventListener() {}, createElement: () => El(''), body: El('body'), head: El('head'), querySelectorAll: () => [], querySelector: () => null,
  fonts: { load: () => Promise.resolve() }, visibilityState: 'visible'
};
const ctx = { document, console: { log() {}, warn() {}, error() {} }, URL, Blob, TextDecoder, Math, JSON, Promise, Date, Map, Set, Object, Array, String, Number, parseInt, parseFloat, isNaN,
  setTimeout: () => 0, clearTimeout() {}, setInterval: () => 0, requestAnimationFrame: () => 0, innerWidth: 390, innerHeight: 800, scrollY: 0,
  scrollTo() {}, scrollBy() {}, fetch: () => Promise.reject(new Error('no fetch')), Image: function () { return {}; }, navigator: {}, addEventListener() {},
  localStorage: { getItem: () => null, setItem() {}, removeItem() {} }, sessionStorage: { getItem: () => null, setItem() {}, removeItem() {} }, location: { search: '', hash: '', href: '' }, history: { replaceState() {} } };
ctx.window = ctx; ctx.window.IMG = {};
vm.createContext(ctx);
try { vm.runInContext(scripts.join('\n;\n') + '\n;globalThis.__T={S,M,D,setsForMat,tAll,renderMatDoor:(typeof renderMatDoor==="function"?renderMatDoor:null)};', ctx, { timeout: 30000 }); }
catch (e) { console.log(JSON.stringify({ fails: ['page script failed to run in node: ' + e.message], notes: [] })); process.exit(0); }
ctx.window.__imgsReady = true;
const X = ctx.__T, S = X.S, M = X.M, D = X.D, TVD = D.tv || {};
if (!html.includes('/*v118 no-price last*/')) F.push('price118 not applied');
if (!html.includes('/*v118b tile-deck price groups*/')) F.push('tile-deck price groups not applied (builder/fym_fix_nov07/tiledeckprice118.py)');
// = price118's PRP('t', i) (inside its IIFE): TVD.pt[tile], [.., price, ..]
const price = i => { const s = D.sets[i]; const x = s && (TVD.pt || {})[s.tile]; return x ? x[1] : null; };
const opts = (TVD.pr || {}).tiles || [];  // price118 CAT.t = 'tiles'
const matKey = (n, bn) => Object.keys(M).find(k => M[k].n === n && (!bn || M[k].bn === bn) && !M[k].hid);
const lotus = matKey('Lotus Cove', 'Oh My Mahjong');
if (!lotus) F.push('Lotus Cove (Oh My Mahjong) mat not found / hidden');
// 4 more mats: the 4 visible mats with the most Tiffany's-match sets (so the her group is exercised)
const cnt = {}; for (const s of D.sets) for (const x of (s.m || [])) cnt[x[0]] = (cnt[x[0]] || 0) + 1;
const more = Object.keys(cnt).filter(k => M[k] && !M[k].hid && k !== lotus).sort((a, b) => cnt[b] - cnt[a]).slice(0, 4);
function run(mk, v, label) {
  S.dmat = mk; S.set = null; S.door = 'mat'; S.tfront = null; S.pr = Object.assign({}, S.pr || {}, { t: v }); S.prE = S.prE || {}; S.prN = S.prN || {};
  let deck;
  try { deck = X.tAll(); } catch (e) { F.push(`${label}: tAll() threw ${e.message}`); return; }
  const pr = deck.map(r => price(r.i));
  const firstNo = pr.findIndex(p => p == null);
  if (!S.prE.t && firstNo >= 0) {
    const late = pr.slice(firstNo).filter(p => p != null).length;
    if (late) F.push(`${label}: tile deck has ${late} priced set(s) after the first unpriced one (card ${firstNo + 1}: ${deck[firstNo].s.name})`);
  }
  if (!S.prE.t) { const over = deck.filter((r, j) => pr[j] != null && pr[j] > v); if (over.length) F.push(`${label}: ${over.length} priced set(s) over $${v} in the deck (${over[0].s.name})`); }
  // tile-rank order inside each price group (album + catalog part; BCAP may move a capped brand later, so compare only sets of one brand)
  for (const grp of [true, false]) {
    const rows = deck.filter((r, j) => !r.her && ((pr[j] != null) === grp));
    const byB = {}; for (const r of rows) { const b = (D.tiles[r.s.tile] || {}).bn || r.s.maker; (byB[b] = byB[b] || []).push(r.p); }
    for (const b in byB) { const a = byB[b]; for (let j = 1; j < a.length; j++) if (a[j] < a[j - 1]) { F.push(`${label}: ${grp ? 'priced' : 'unpriced'} group out of tile-rank order for ${b}`); break; } }
  }
  // See all grid (QA2 Nov 8): the RENDERED grid, across every section, first as it opens, then with Show more / partner sets opened
  if (!X.renderMatDoor) F.push('renderMatDoor() missing');
  else for (const open of [false, true]) {
    S.dgrid = true; S.dshow = open ? 9999 : 0; S.dcat = open; const el = El('s-tiles');
    try { X.renderMatDoor(el); } catch (e) { F.push(`${label}: See all render threw ${e.message}`); break; }
    if (!/data-dset=/.test(el.innerHTML)) { F.push(`${label}: See all grid rendered no tile sets`); break; }
    const ids = [...el.innerHTML.matchAll(/data-dset="(\d+)"/g)].map(m => +m[1]);
    const a = ids.map(price); const fn = a.findIndex(p => p == null);
    if (!S.prE.t && fn >= 0 && a.slice(fn).some(p => p != null)) F.push(`${label}: See all grid${open ? ' (all opened)' : ''} shows a priced set after an unpriced one (card ${fn + 1} has no price)`);
    if (!S.prE.t && !open) {  // an unpriced card may only show once every priced set the grid has is on screen
      const g = X.setsForMat(mk); const allPriced = [...g.her, ...g.alb, ...g.cat].filter(r => price(r.i) != null).length;
      if (fn >= 0 && a.filter(p => p != null).length < allPriced) F.push(`${label}: See all grid shows unpriced sets while ${allPriced - a.filter(p => p != null).length} priced set(s) are still behind a button`);
    }
    if (!S.prE.t && /without a listed price shown last/.test(el.innerHTML) && fn >= 0 && fn < a.filter(p => p != null).length) F.push(`${label}: note says shown last but they are not`);
    if (open && label.startsWith('Lotus Cove, Under')) N.push(`grid ${label}: ${a.map(p => p == null ? '-' : '$').join('')}`);
    S.dgrid = false; S.dshow = 0; S.dcat = false;
  }
  return { n: deck.length, priced: pr.filter(p => p != null).length, firstUnpriced: firstNo + 1, top: deck.slice(0, 8).map((r, j) => `${r.s.name}${pr[j] == null ? ' (no price)' : ' $' + pr[j]}`) };
}
if (lotus) {
  if (!opts.includes(175)) N.push(`price options for tile sets: ${JSON.stringify(opts)} (175 not offered; tested anyway)`);
  const r = run(lotus, 175, 'Lotus Cove, Under $175'); if (r) N.push('Lotus Cove Under $175: ' + JSON.stringify(r));
  if (r && r.priced === 0) F.push('Lotus Cove, Under $175: no priced set in the deck (test would pass vacuously)');
}
for (const mk of [lotus, ...more].filter(Boolean)) for (const v of opts) run(mk, v, `${M[mk].n} (${M[mk].bn}), Under $${v}`);
S.pr.t = '';
console.log(JSON.stringify({ fails: F, notes: N }));
