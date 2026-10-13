// Render brand-font text boxes as transparent PNGs (2x) so they can replace Canva text boxes.
// Usage: NODE_PATH=$(npm root -g) node textpng.js spec.json outdir
// spec: [{name, text, font: shrikhand|alfa|bitter|bitterb|playi, size, color, w, h, align?, upper?, shadow?, lh?, ls?}]
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
const F = process.env.MATCARD_FONTS || '/tmp/cc/f/';
const fonts = {
  shrikhand: F + 'fontsource-shrikhand/files/shrikhand-latin-400-normal.woff2',
  alfa: F + 'fontsource-alfa-slab-one-5.3.0/package/files/alfa-slab-one-latin-400-normal.woff2',
  bitter: F + 'fontsource-bitter-5.3.0/package/files/bitter-latin-400-normal.woff2',
  bitterb: F + 'fontsource-bitter-5.3.0/package/files/bitter-latin-700-normal.woff2',
  playi: F + 'fontsource-playfair-display-5.3.0/package/files/playfair-display-latin-400-italic.woff2',
};
(async () => {
  const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const out = process.argv[3]; fs.mkdirSync(out, {recursive: true});
  const b = await chromium.launch();
  const p = await b.newPage({deviceScaleFactor: 2});
  for (const s of spec) {
    const ff = Object.entries(fonts).map(([k, v]) => `@font-face{font-family:${k};src:url(file://${v})}`).join('');
    const esc = t => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/\n/g, '<br>');
    const html = `<html><head><style>${ff}html,body{margin:0;background:transparent}
      .b{width:${s.w}px;height:${s.h}px;display:flex;align-items:center;justify-content:${s.align === 'left' ? 'flex-start' : 'center'};text-align:${s.align || 'center'}}
      .t{font-family:${s.font};font-size:${s.size}px;color:${s.color};line-height:${s.lh || 1.15};letter-spacing:${s.ls || 0}em;${s.upper ? 'text-transform:uppercase;' : ''}${s.shadow ? `text-shadow:${s.shadow};` : ''}}
      </style></head><body><div class="b"><div class="t">${esc(s.text)}</div></div></body></html>`;
    await p.setViewportSize({width: Math.ceil(s.w), height: Math.ceil(s.h)});
    const hf=path.join(require('os').tmpdir(),'textpng_'+process.pid+'.html'); fs.writeFileSync(hf,html); await p.goto('file://'+hf); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150);
    const over = await p.evaluate(() => { const t = document.querySelector('.t'); const b = document.querySelector('.b'); return t.scrollWidth > b.clientWidth + 1 || t.scrollHeight > b.clientHeight + 1; });
    await p.screenshot({path: path.join(out, s.name + '.png'), omitBackground: true, clip: {x: 0, y: 0, width: Math.ceil(s.w), height: Math.ceil(s.h)}});
    console.log(s.name, over ? 'OVERFLOW' : 'ok');
  }
  await b.close();
})();
