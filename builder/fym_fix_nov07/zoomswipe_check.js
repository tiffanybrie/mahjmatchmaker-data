// FYM gate [164] behavioural test (Nov 7 2026, FYM 1.18 "zoom swipe"): runs the build's own zoomer() in node with fake pointer
// events and checks that a ZOOMED card can still be swiped. Usage: node builder/fym_fix_nov07/zoomswipe_check.js <build_dir>
// Prints JSON {ok:bool, fails:[...], cases:{...}}.
const fs = require('fs'), path = require('path');
const h = fs.readFileSync(path.join(process.argv[2], 'index.html'), 'utf8');
const a = h.indexOf('function zoomer('), b = h.indexOf('\nfunction bindCard(', a);
if (a < 0 || b < 0) { console.log(JSON.stringify({ ok: false, fails: ['zoomer() not found in build'] })); process.exit(0); }
const src = h.slice(a, b);
let T = 1000;
Object.defineProperty(globalThis, 'performance', { value: { now: () => T }, configurable: true });
const realNow = Date.now; Date.now = () => T;
globalThis.window = { scrollBy() {} };
globalThis.S = { zs: {} };
const zoomer = new Function('S', 'window', src + '\nreturn zoomer;')(globalThis.S, globalThis.window);

function el(extra) {
  const L = {};
  return Object.assign({ style: {}, addEventListener(t, f) { (L[t] = L[t] || []).push(f); }, fire(t, e) { (L[t] || []).forEach(f => f(e)); },
    setPointerCapture() {}, querySelectorAll() { return []; } }, extra);
}
function mk(zs, ok) {
  const host = el(), img = el({ offsetWidth: 300, offsetHeight: 300, offsetLeft: 0, offsetTop: 0, complete: true });
  const box = el({ getBoundingClientRect: () => ({ left: 0, top: 0, width: 300, height: 300 }) });
  const flew = [];
  S.zs = zs ? { k: Object.assign({}, zs) } : {};
  zoomer(host, img, box, { key: 'k', zoom: true, swipe: { yes: { style: {} }, no: { style: {} }, ok: () => ok !== false, fly: y => flew.push(y) } });
  return { host, flew };
}
const ZC = { s: 2.4, x: -210, y: -210 };  // zoomed 2.4x, centred (image 720px in a 300px box: 210px of pan room each side)
function drag(c, pts, ms) {  // pts: [[x,y],...] from the first point; ms between moves
  T += 1000; const id = 1;
  c.host.fire('pointerdown', { pointerId: id, clientX: pts[0][0], clientY: pts[0][1] });
  let p = pts[0];
  for (const q of pts.slice(1)) { T += ms; p = q; c.host.fire('pointermove', { pointerId: id, clientX: q[0], clientY: q[1] }); }
  c.host.fire('pointerup', { pointerId: id, clientX: p[0], clientY: p[1] });
}
const line = (x0, y0, x1, y1, n) => Array.from({ length: n + 1 }, (_, i) => [x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n]);
const fails = [], cases = {};
function t(name, cond, info) { cases[name] = { pass: !!cond, info }; if (!cond) fails.push(name + ': ' + JSON.stringify(info)); }

let c;
c = mk(ZC); drag(c, line(150, 150, 90, 150, 6), 40);  // small slow drag: pans only
t('small drag pans, no swipe', !c.flew.length && S.zs.k.x === -270 && !c.host.style.transform, { flew: c.flew, x: S.zs.k.x });

c = mk(ZC); drag(c, line(350, 150, -10, 150, 36), 40);  // slow drag left: 210 pan + 150 past the edge
t('drag left past edge = X', c.flew.length === 1 && c.flew[0] === false && S.zs.k.s === 2.4, { flew: c.flew, zs: S.zs.k });

c = mk(ZC); drag(c, line(-10, 150, 350, 150, 36), 40);
t('drag right past edge = heart', c.flew.length === 1 && c.flew[0] === true, { flew: c.flew });

c = mk({ s: 2.4, x: -420, y: -210 }); drag(c, line(200, 150, 160, 150, 8), 40);  // at right edge, 40px more (<16+75): springs back
t('short drag past edge springs back', !c.flew.length && c.host.style.transform === '', { flew: c.flew, tf: c.host.style.transform });

c = mk(ZC); drag(c, line(250, 150, 150, 150, 4), 10);  // fast flick left from the middle (2.5 px/ms)
t('flick while zoomed = X, pan restored', c.flew.length === 1 && c.flew[0] === false && S.zs.k.x === -210 && S.zs.k.s === 2.4, { flew: c.flew, zs: S.zs.k });

c = mk(ZC); { T += 1000; c.host.fire('pointerdown', { pointerId: 1, clientX: 250, clientY: 150 }); for (let i = 1; i <= 4; i++) { T += 10; c.host.fire('pointermove', { pointerId: 1, clientX: 250 - 25 * i, clientY: 150 }); }
  T += 400; c.host.fire('pointerup', { pointerId: 1, clientX: 150, clientY: 150 }); }  // fast pan, then holds still 0.4s before lifting
t('fast pan that stops before lifting = no swipe', !c.flew.length && S.zs.k.x === -310, { flew: c.flew, zs: S.zs.k });

c = mk(ZC); drag(c, line(150, 150, 270, 150, 4), 33);  // 60Hz-paced flick right (0.9 px/ms, as a phone sends it)
t('60Hz flick right = heart', c.flew.length === 1 && c.flew[0] === true, { flew: c.flew });

c = mk(ZC); drag(c, line(150, 300, 150, 0, 10), 10);  // fast vertical drag: pans, never swipes
t('vertical drag pans', !c.flew.length && S.zs.k.y === -420, { flew: c.flew, zs: S.zs.k });

c = mk(ZC); drag(c, line(300, 300, 0, 0, 30), 40);  // diagonal drag to the corner: pans
t('diagonal drag pans', !c.flew.length && S.zs.k.x === -420 && S.zs.k.y === -420, { flew: c.flew, zs: S.zs.k });

c = mk(ZC, false); drag(c, line(350, 150, -10, 150, 36), 40);  // card that cannot be swiped (chosen / locked mat)
t('locked card only pans', !c.flew.length && !c.host.style.transform, { flew: c.flew });

c = mk(null); drag(c, line(150, 150, 30, 150, 12), 40);  // not zoomed: normal swipe still works
t('unzoomed swipe still works', c.flew.length === 1 && c.flew[0] === false, { flew: c.flew });

Date.now = realNow;
console.log(JSON.stringify({ ok: !fails.length, fails, cases }));
