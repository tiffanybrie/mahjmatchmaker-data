// FYM gate [60] (Tiffany Oct 26 8:29am): best-photographed rack leads among equals. Runs the page code in node (stub DOM copied from fym_matdoor_check.js).
// Usage: node builder/fym_rackquality_check.js <build_dir>   -> prints JSON {fails:[...], notes:[...]} ; exit 0 always (gate reads fails)
const fs = require('fs'), vm = require('vm'), path = require('path');
const B = process.argv[2];
const html = fs.readFileSync(path.join(B, 'index.html'), 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const F = [], N = [];
const fail = m => F.push(m);
const els = {}, appended = [];
function El(id) { return { id, innerHTML: '', style: {}, value: '', title: '', classList: { add() {}, remove() {}, contains() { return false; } }, dataset: {}, setAttribute() {}, getAttribute() { return null; }, addEventListener() {}, appendChild(c) { appended.push(c); }, remove() {}, querySelector() { return null; }, querySelectorAll() { return []; }, getBoundingClientRect() { return { top: 0, left: 0, width: 390, height: 600 }; }, focus() {} }; }
const KNOWN = ['s-tiles', 's-mats', 's-racks', 's-card', 'stp', 'logo'];
const listeners = { click: [], input: [], keydown: [] };
const document = {
  getElementById: id => KNOWN.includes(id) ? (els[id] = els[id] || El(id)) : null,
  addEventListener: (t, f) => { (listeners[t] = listeners[t] || []).push(f); },
  createElement: () => El(''), body: El('body'), head: El('head'), querySelectorAll: () => [], fonts: { load: () => Promise.resolve() }, visibilityState: 'visible'
};
document.body.appendChild = c => appended.push(c);
const ctx = { document, console, URL, Blob, TextDecoder, Math, JSON, Promise, Date, Map, Set, Object, Array, String, Number, parseInt, parseFloat, isNaN,
  setTimeout: () => 0, clearTimeout() {}, setInterval: () => 0, requestAnimationFrame: () => 0, innerWidth: 390, innerHeight: 800, scrollY: 0,
  scrollTo() {}, scrollBy() {}, fetch: () => Promise.reject(new Error('no fetch')), Image: function () { return {}; }, navigator: {}, addEventListener() {} };
ctx.window = ctx; ctx.window.IMG = {};
vm.createContext(ctx);
try { vm.runInContext(scripts.join('\n;\n') + '\n;globalThis.__T={S,M,D,set,rackDeck,herRacks,R,uni};for(const n of ["matLocked","herUseful","codeLine","doStartOver"]){try{globalThis.__T[n]=eval(n);}catch(e){globalThis.__T[n]=null;}}', ctx, { timeout: 20000 }); }
catch (e) { console.log(JSON.stringify({ fails: ['page script failed to run in node: ' + e.message], notes: [] })); process.exit(0); }
const X = ctx.__T, S = X.S, D = X.D, R = X.R;
const vis = r => R[r] && !R[r].hid;
for (const r of Object.keys(R)) if (vis(r) && !(R[r].pq >= 1 && R[r].pq <= 5)) fail(`rack ${R[r].n} has no photo score (config/rack-photo-quality.json)`);
const pairs = [];
D.sets.forEach((s, si) => (s.m || []).forEach(e => { if (M0(e[0])) pairs.push([si, e[0]]); }));
function M0(k) { return X.M[k] && !X.M[k].hid; }
const ex = D.sets.findIndex(s => s.slug === 'mahjong-studios-american');
if (ex >= 0) pairs.unshift([ex, 'www.etsy.com/listing/4504460459/preppy-mahjong-mat-whimsical-chinoiserie']);
let n = 0;
for (const [si, mk] of pairs) {
  if (!X.M[mk]) continue;
  S.set = si; S.fav = mk; S.f.r.brand = ''; S.f.r.her = false; S.rseen = {};
  const hr = X.herRacks(), U = X.uni(), mine = r => hr.includes(r) || U.includes(r);
  const nm = `${D.sets[si].name} + ${X.M[mk].n}`;
  // default suggestions, picks off: first non-pick rack vs racks whose colour distance is within 2 dE of it (same penalty tier)
  S.f.r.fam = [];
  const sw = (X.M[mk].ms || []).filter(s => s[1] >= .06);
  let deck = X.rackDeck(); const first = deck[0];
  if (first && !mine(first)) {
    const lab = h => { const c = [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16) / 255).map(v => v > .04045 ? ((v + .055) / 1.055) ** 2.4 : v / 12.92);
      let [x, y, z] = [c[0] * .4124 + c[1] * .3576 + c[2] * .1805, c[0] * .2126 + c[1] * .7152 + c[2] * .0722, c[0] * .0193 + c[1] * .1192 + c[2] * .9505];
      [x, y, z] = [x / .95047, y, z / 1.08883].map(v => v > .008856 ? Math.cbrt(v) : 7.787 * v + 16 / 116); return [116 * y - 16, 500 * (x - y), 200 * (y - z)]; };
    const SW = sw.map(s => lab(s[0]));
    const sc = r => { const h = R[r].hx; if (!h || !SW.length) return 99; const L = lab(h); return Math.min(...SW.map(s => Math.hypot(L[0] - s[0], L[1] - s[1], L[2] - s[2]))); };
    const pen = r => (R[r].pa ? 0 : 1e5) + (R[r].lo ? 1e4 : 0);
    const best = Math.min(...deck.filter(r => !mine(r)).map(r => sc(r) + pen(r)));
    const band = deck.filter(r => !mine(r) && sc(r) + pen(r) <= best + 2);
    if (R[first].pq < 4 && band.some(r => R[r].pq >= 4)) fail(`default racks for ${nm}: leads with ${R[first].n} (photo ${R[first].pq}) although ${R[band.find(r => R[r].pq >= 4)].n} (photo ${R[band.find(r => R[r].pq >= 4)].pq}) is as close in colour`);
  }
  n++;
}
// white / clear / wood chips (picks off), on the example pairing and every 10th album pairing
for (const [si, mk] of pairs.filter((_, i) => i % 10 === 0)) {
  S.set = si; S.fav = mk; S.f.r.her = false; S.f.r.brand = '';
  const hr = X.herRacks();
  for (const c of ['neutral', 'clear', 'wood']) {
    S.f.r.fam = [c]; const d = X.rackDeck(); if (!d.length || hr.includes(d[0])) continue;
    const rs = r => (R[r].rs || {})[c] || 0, top = Math.max(...d.filter(r => !hr.includes(r)).map(rs));
    const band = d.filter(r => !hr.includes(r) && rs(r) >= top - .05);
    if (R[d[0]].pq < 4 && band.some(r => R[r].pq >= 4)) fail(`${c} chip (${D.sets[si].name} + ${X.M[mk].n}): leads with ${R[d[0]].n} (photo ${R[d[0]].pq}) although a photo-4+ rack has the same ${c} share`);
  }
}
N.push(`pairings checked: ${n}`);
console.log(JSON.stringify({ fails: F.slice(0, 20), nfail: F.length, notes: N }));
