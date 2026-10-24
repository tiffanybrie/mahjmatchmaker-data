// FYM gate [22]: runs the page's OWN code in node (tiny DOM stub) over the paths Tiffany tested on Oct 21 (6:20-6:37pm).
// Usage: node builder/fym_matdoor_check.js <build_dir>   -> prints JSON {fails:[...], notes:[...]} ; exit 0 always (gate reads fails)
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
try { vm.runInContext(scripts.join('\n;\n') + '\n;globalThis.__T={S,M,D,set,queue,matDeck,rackDeck,decide,undo,setsForMat,herRacks};for(const n of ["matLocked","herUseful","codeLine","doStartOver"]){try{globalThis.__T[n]=eval(n);}catch(e){globalThis.__T[n]=null;}}', ctx, { timeout: 20000 }); }
catch (e) { console.log(JSON.stringify({ fails: ['page script failed to run in node: ' + e.message], notes: [] })); process.exit(0); }
ctx.window.__imgsReady = true;
const X = ctx.__T, S = X.S, M = X.M, D = X.D;
if (!X.matLocked) { X.matLocked = () => false; fail('matLocked() missing (no locked mat-door state)'); }
if (!X.herUseful) fail('herUseful() missing (picks toggle shown even when it changes nothing)');
if (!X.doStartOver) { X.doStartOver = () => { Object.assign(S, { set: null, dmat: null, door: 'tiles', tilesOpen: true, liked: [], seen: {}, hist: [], peek: null, fav: null }); }; fail('no Start over function'); }
const H = id => (els[id] || El(id)).innerHTML;
const attrsOf = tag => { const a = {}; for (const m of tag.matchAll(/([a-zA-Z-]+)(?:="([^"]*)")?/g)) { if (m[1] !== 'button') a[m[1]] = m[2] === undefined ? '' : m[2].replace(/&quot;/g, '"').replace(/&amp;/g, '&'); } return a; };
const buttons = h => [...h.matchAll(/<button\b([^>]*)>([\s\S]*?)<\/button>/g)].map(m => ({ a: attrsOf(m[1]), text: m[2].replace(/<[^>]+>/g, '').trim() }));
const camel = s => s.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
function tgt(a) {
  const ds = {}; for (const k in a) if (k.startsWith('data-')) ds[camel(k.slice(5))] = a[k];
  const simple = sel => { let m; if ((m = sel.match(/^\[([a-z-]+)(?:="([^"]*)")?\]$/))) return m[1] in a && (m[2] === undefined || a[m[1]] === m[2]); if (sel === '#logo') return a.id === 'logo'; return false; };
  const t = { dataset: ds, tagName: 'BUTTON', getAttribute: k => (k in a ? a[k] : null), hasAttribute: k => k in a, classList: { contains: c => (a.class || '').split(/\s+/).includes(c) },
    closest(sel) { for (const p of sel.split(',')) { const tk = p.trim().split(/\s+/); if (tk.length > 1 && !(tk[0] === '.frow' && a.__frow)) continue; if (simple(tk[tk.length - 1])) return t; } return null; } };
  return t;
}
const click = a => { const e = { target: tgt(a), preventDefault() {}, stopPropagation() {} }; for (const f of listeners.click) f(e); };
function press(sec, pred, label) { const b = buttons(H(sec)).find(pred); if (!b) { fail(`${label}: button not found in ${sec}`); return false; } click(b.a); return true; }
const setIx = (name, maker) => D.sets.findIndex(s => s.name === name && (!maker || s.maker === maker) && !s.hid);
const matKey = (n, bn) => Object.keys(M).find(k => M[k].n === n && (!bn || M[k].bn === bn) && !M[k].hid);
const deckIds = () => X.queue('m');
const SW = /swip/i;
function lockedChecks(label) {
  const t = H('s-tiles'), m = H('s-mats');
  const bt = buttons(t);
  if (!bt.some(b => 'data-dswap' in b.a && /Change mat/.test(b.text))) fail(`${label}: no working "Change mat" in the pairing summary`);
  if (!bt.some(b => 'data-opentiles' in b.a && /Change tiles/.test(b.text))) fail(`${label}: no "Change tiles" in the pairing summary`);
  if (!/Your mat/.test(t) || !/Your tiles/.test(t)) fail(`${label}: pairing summary missing "Your mat" / "Your tiles"`);
  if (!X.matLocked()) fail(`${label}: mat door after tiles is not the single-card view`);
  if (SW.test(m.replace(/<[^>]+>/g, ' '))) fail(`${label}: "swipe" copy on the locked single card`);
  if (/data-her=/.test(m)) fail(`${label}: Tiffany's picks toggle shown on a locked single card (it changes nothing)`);
  if (!/data-ddeck/.test(m) || !/See other mats for/.test(m)) fail(`${label}: no "See other mats for <set>" button`);
  if (/Make it official|Mock up/i.test(m)) fail(`${label}: mock-up CTA shown in the mats step (must follow racks)`);
  if (!/Mat ✓/.test(t) || !/Tiles ✓/.test(t) || !/Racks/.test(t) || !/Mock up/.test(t)) fail(`${label}: step indicator Mat ✓ > Tiles ✓ > Racks > Mock up missing`);
  if (!/data-startover/.test(t)) fail(`${label}: no Start over link near the top`);
}
function toggleChecks(label) {
  for (const k of ['m', 'r']) {
    const sec = k === 'm' ? 's-mats' : 's-racks', h = H(sec);
    if (!h || !/data-her="/.test(h)) continue;
    if (!new RegExp(`data-her="${k}"`).test(h)) continue;
    const f = S.f[k], o = f.her, dk = () => (k === 'm' ? X.matDeck() : X.rackDeck()).filter(id => !(k === 'm' ? S.seen : S.rseen)[id]).join('|');
    f.her = true; const a = dk(); f.her = false; const b = dk(); f.her = o;
    if (a === b) fail(`${label}: picks toggle (${k}) shown but turning it on/off changes nothing`);
  }
}
const run = (label, fn) => { try { fn(); } catch (e) { fail(`${label}: threw ${e.message}`); } };

// ---------- scenario 1: Rattan -> December 1994 -> change tiles to Cypress -> See other mats -> swipe -> picks -> Back
run('Rattan path', () => {
  X.doStartOver(); click({ 'data-door': 'mat' });
  const rat = matKey('Rattan', 'Sunday Mahjong'), dec = setIx('December 1994'), cyp = setIx('Cypress');
  if (!rat || dec < 0 || cyp < 0) { fail('Rattan path: Rattan / December 1994 / Cypress not found'); return; }
  click({ 'data-dmat': rat });
  click({ 'data-dset': String(dec) });
  lockedChecks('Rattan + December 1994');
  press('s-tiles', b => 'data-opentiles' in b.a, 'Rattan: Change tiles');
  const t = H('s-tiles');
  if (!/data-dkeept/.test(t)) fail('Rattan: Change tiles view has no "Keep <set>" way back');
  if (!/data-dset=/.test(t)) fail('Rattan: Change tiles view shows no tile sets');
  click({ 'data-dset': String(cyp) });
  if (S.dmat !== rat || S.set !== cyp) fail(`Rattan: after changing tiles the pairing is not Rattan + Cypress (mat ${S.dmat}, set ${S.set})`);
  lockedChecks('Rattan + Cypress');
  press('s-mats', b => 'data-ddeck' in b.a, 'Rattan: See other mats');
  if (X.matLocked() || S.peek) fail('Rattan: "See other mats" still shows a locked card');
  if (!S.liked.includes(rat)) fail('Rattan: her mat is not kept in the shortlist when the deck opens');
  const q0 = deckIds();
  if (q0.length < 2) fail(`Rattan: "See other mats" deck has ${q0.length} cards`);
  if (!SW.test(H('s-mats').replace(/<[^>]+>/g, ' ')) && q0.length > 1) N.push('Rattan deck: no swipe hint text (ok)');
  toggleChecks('Rattan deck');
  if (/data-her="m"/.test(H('s-mats'))) { const o = S.f.m.her; press('s-mats', b => b.a['data-her'] === 'm', 'Rattan: picks toggle'); if (S.f.m.her === o) fail('Rattan: picks toggle click did not switch'); click({ 'data-her': 'm' }); }
  const h0 = S.hist.length; X.decide('m', true); X.decide('m', false);
  if (S.hist.length !== h0 + 2) fail('Rattan: swiping in the "See other mats" deck did nothing');
  click({ 'data-back': 'm' }); click({ 'data-back': 'm' });
  if (S.hist.length !== h0 || S.liked.length !== 1) fail('Rattan: Back did not restore the deck / shortlist');
  if (deckIds().join() !== q0.join()) fail('Rattan: after Back x2 the deck order differs');
  click({ 'data-dundeck': '' });
  if (!X.matLocked()) fail('Rattan: "Back to Rattan" did not return to her mat');
});
// ---------- scenario 2: change mat after tiles keeps the tiles
run('Change mat', () => {
  const cyp = S.set, jade = matKey('Jade', 'Oh My Mahjong');
  press('s-tiles', b => 'data-dswap' in b.a, 'Change mat');
  if (!/data-dkeep/.test(H('s-tiles'))) fail('Change mat: picker has no "Keep <mat>" way back');
  if (!/data-dmat=/.test(H('s-tiles'))) fail('Change mat: picker shows no mats');
  click({ 'data-dmat': jade });
  if (S.set !== cyp || S.dmat !== jade) fail('Change mat: picking a new mat did not keep the tiles');
  lockedChecks('Jade + Cypress (after Change mat)');
  press('s-tiles', b => 'data-dswap' in b.a, 'Change mat 2'); click({ 'data-dkeep': '' });
  if (S.dmat !== jade || !X.matLocked()) fail('Change mat: "Keep" did not restore the pairing');
});
// ---------- scenario 3: Jade -> Birdie (one suitor, picks toggle on by default)
run('Jade + Birdie', () => {
  X.doStartOver(); click({ 'data-door': 'mat' });
  const jade = matKey('Jade', 'Oh My Mahjong'), bir = setIx('Birdie');
  click({ 'data-dmat': jade }); click({ 'data-dset': String(bir) });
  lockedChecks('Jade + Birdie');
  click({ 'data-ddeck': '' });
  const q = deckIds();
  if (!q.length) fail('Jade + Birdie: "See other mats" deck is empty');
  if (q.length < 2 && SW.test(H('s-mats').replace(/<[^>]+>/g, ' '))) fail('Jade + Birdie: swipe copy with fewer than 2 cards');
  toggleChecks('Jade + Birdie deck');
  const o = S.f.m.her; click({ 'data-her': 'm' });
  if (/data-her="m"/.test(H('s-mats')) && deckIds().join() === q.join() && S.f.m.her !== o) fail('Jade + Birdie: picks toggle changed state but not the deck');
});
// ---------- scenario 4: tiles door, 5 fast swipes, Back x5, mock-up from HER pick, racks tray
run('Tiles door', () => {
  X.doStartOver();
  const os = setIx('Osler'); click({ 'data-tile': String(os) });
  toggleChecks('Osler');
  if (/Make it official|Mock up this/i.test(H('s-mats'))) fail('Osler: mock-up CTA in the mats step');
  const q0 = deckIds().slice(0, 6), pat = [true, false, true, true, false];
  pat.forEach(y => X.decide('m', y));
  if (S.liked.length !== 3) fail(`Osler: 3 hearts expected in the shortlist, got ${S.liked.length}`);
  if (!/data-back="m"/.test(H('s-mats')) || /data-back="m" disabled/.test(H('s-mats'))) fail('Osler: no enabled Back button above the card after swiping');
  for (let k = 0; k < 5; k++) click({ 'data-back': 'm' });
  if (S.hist.length || S.liked.length) fail('Osler: Back x5 did not undo all 5 swipes (hearts / X)');
  if (deckIds().slice(0, 6).join() !== q0.join()) fail('Osler: after Back x5 the cards are not back in order');
  pat.forEach(y => X.decide('m', y));
  const r = H('s-racks');
  if (S.fav) fail('Osler: a mat was chosen for the mock-up without her tapping one');
  if (!/Which suitor is the one/.test(r)) fail('Osler: with several suitors the racks step does not ask her to pick one');
  const nb = buttons(H('s-mats')).filter(b => /Add racks|Next/.test(b.text));
  if (nb.some(b => 'data-mock' in b.a)) fail('Osler: Add racks offered before she picked a mat suitor (Oct 23: pick first, then Add racks)');
  const mine = S.liked[0]; click({ 'data-mock': mine });
  if (S.fav !== mine) fail('Osler: picking her suitor did not set the mock-up mat');
  if (!S.liked.includes(S.fav)) fail('Osler: mock-up mat is not one of HER hearts');
  if (!/data-make disabled/.test(H('s-racks'))) fail('Osler: Make it official enabled before any racks');
  X.decide('r', true); X.decide('r', true); X.decide('r', true);
  // v79 (Tiffany Oct 23 8:35pm): hearting never picks a rack; she taps suitors to see them on her mat (max 2)
  if (S.rpick.length !== 0) fail(`Osler: hearting racks preselected ${S.rpick.length} (nothing is picked until she taps)`);
  if (!/Pick 1 or 2 racks/.test(H('s-racks'))) fail('Osler: no "Pick 1 or 2 racks" note before a pick');
  { const s0 = buttons(H('s-racks')).filter(b => 'data-rp' in b.a); click(s0[0].a);
    if (!/id="rpv"/.test(H('s-racks')) || /id="top-r"/.test(H('s-racks'))) fail('Osler: tapping a rack suitor did not show it on the deck (or the deck still swipes)');
    click(buttons(H('s-racks')).filter(b => 'data-rp' in b.a)[0].a);
    if (!/rpv n2/.test(H('s-racks'))) fail('Osler: two picked racks are not both shown on the deck'); }
  const rt = H('s-racks');
  if (S.rpick.length !== 2) fail(`Osler: racks tray holds ${S.rpick.length} (max 2)`);
  if (!/2 of 2/.test(rt) || (rt.match(/data-rx=/g) || []).length !== 2) fail('Osler: full racks tray lacks "2 of 2" / two x buttons');
  const sug = buttons(rt).find(b => 'data-rp' in b.a);
  if (!sug) fail('Osler: third hearted rack not in Rack suitors');
  else { click(sug.a); if (S.rpick.includes(sug.a['data-rp'])) fail('Osler: tapping a suitor with 2 of 2 replaced a rack without x'); click({ 'data-rx': S.rpick[0] }); click(sug.a); if (!S.rpick.includes(sug.a['data-rp']) || S.rpick.length !== 2) fail('Osler: x then tap did not swap the rack in'); }
  // Oct 22: Back on racks (Tiffany: "a missed rack is gone for good")
  const rh0 = S.rhist.length, rb = H('s-racks');
  if (!/data-back="r"/.test(rb) || /data-back="r" disabled/.test(rb)) fail('Osler: no enabled Back button above the rack deck after swiping');
  else { click({ 'data-back': 'r' }); if (S.rhist.length !== rh0 - 1) fail('Osler: rack Back did not bring the last rack back'); }
  if (X.codeLine) { const c = X.codeLine(); if (c && !/ to save$/.test(c)) fail(`card code line "${c}" does not end "to save"`); }
  // start over from the top logo (confirm sheet because there is a shortlist)
  const n0 = appended.length; click({ id: 'logo' });
  if (appended.length === n0 || !/Start over\?/.test(appended[appended.length - 1].innerHTML)) fail('logo: no confirm sheet when there is a shortlist');
  click({ 'data-so-yes': '' });
  if (S.set != null || S.liked.length || S.door !== 'tiles') fail('logo Start over did not reset to the doors');
  if (!/data-door="mat"/.test(H('s-tiles'))) fail('Start over did not show the two doors');
});
console.log(JSON.stringify({ fails: F, notes: N }));
