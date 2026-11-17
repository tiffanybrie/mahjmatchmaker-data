// missedFix(src, PAGE, opt) -> {src, note}
// src  = the album page's code block source (the block holding the "Every <Set> match" / "My <Set> matches" grid),
//        or, on /holiday-mahjong-matches, the block holding id="<sid>".
// PAGE = pages/<page>.json from this folder: {main:[figure html], holiday:[figure html]} (cards numbered 00).
// opt  = {sid: 'dear-santa'} on the holiday page; {} on album pages. opt.css = holiday CSS for pages without a holiday section.
// Album pages: main cards go at the END of the main grid (after the last card), the grid is renumbered 01..NN, and the
// count strings ("all N <Set> mat matches from M brands" or "N <Set> mat matches") are bumped by the cards added and by
// brands new to the page. Holiday cards go at the end of the page's holiday section (#holiday-matches), numbering continues
// the section's own numbers and its "N mat matches," line is bumped; a page with no holiday section gets one right after the
// main grid section (same markup as the Nov 4 late-holiday sections). Idempotent: a card whose image file is already on the
// page is skipped.
function missedFix(src, PAGE, opt) {
  opt = opt || {};
  const FIG = /<figure class="mm3-c[ "][\s\S]*?<\/figure>/g;
  const fileOf = f => (f.match(/\/assets\/cards\/[^"]*\/([^"\/]+\.jpg)"/) || [])[1];
  const brandOf = f => { const m = f.match(/<span class="mm3-by">Mat by (?:<a[^>]*>)?([^<]+)/); return m ? m[1].trim().replace(/&#x27;|&#39;|&rsquo;|’/g, "'").replace(/&amp;/g, '&') : ''; };
  const fresh = arr => (arr || []).filter(f => !src.includes(fileOf(f)));
  const num = (f, n) => f.replace(/<span class="mm3-n">\d*<\/span>/, '<span class="mm3-n">' + String(n).padStart(2, '0') + '</span>');
  const notes = [];
  const holAppend = (s, sid, figs) => {
    const i = s.indexOf('id="' + sid + '"'); if (i < 0) return null;
    const end = s.indexOf('</section>', i); const seg = s.slice(i, end);
    const nums = [...seg.matchAll(/<span class="mm3-n">(\d+)<\/span>/g)].map(m => +m[1]); const n = nums.length ? Math.max(...nums) : 0;
    const gEnd = seg.lastIndexOf('</div>'); if (gEnd < 0) throw new Error('no grid end in #' + sid);
    let nseg = seg.slice(0, gEnd) + figs.map((f, k) => num(f, n + 1 + k)).join('') + seg.slice(gEnd);
    nseg = nseg.replace(/<p class="mm3-sub">(\d+) mat match(es)?,/, (m, a) => { const k = +a + figs.length; return '<p class="mm3-sub">' + k + ' mat match' + (k == 1 ? '' : 'es') + ','; });
    notes.push(`#${sid}: +${figs.length} (numbers ${n + 1}-${n + figs.length})`);
    return s.slice(0, i) + nseg + s.slice(end);
  };
  if (opt.sid) {  // holiday page section
    const figs = fresh(PAGE.holiday);
    if (!figs.length) return {src, note: 'already'};
    const out = holAppend(src, opt.sid, figs); if (out == null) throw new Error('no section #' + opt.sid + ' in this block');
    return {src: out, note: notes.join('; ')};
  }
  const hm = src.match(/<h2>(?:Every (.+?) match|My (.+?) matches)<\/h2>/);
  if (!hm) throw new Error('no main heading ("Every X match" / "My X matches") in this block');
  const setName = (hm[1] || hm[2]).replace(/&amp;/g, '&');
  const before = new Set((src.match(FIG) || []).map(brandOf));
  const main = fresh(PAGE.main), hol = fresh(PAGE.holiday);
  if (!main.length && !hol.length) return {src, note: 'already'};
  let res = src;
  const g0 = res.indexOf('<div class="mm3-grid"', hm.index); const sEnd = res.indexOf('</section>', g0);
  if (g0 < 0 || sEnd < 0) throw new Error('no main grid');
  if (main.length) {
    const grid = res.slice(g0, sEnd); const figs = grid.match(FIG) || [];
    if (figs.length < 3) throw new Error('main grid too short (' + figs.length + ')');
    const last = figs[figs.length - 1]; const lastEnd = grid.lastIndexOf(last) + last.length;
    let ng = grid.slice(0, lastEnd) + main.join('') + grid.slice(lastEnd);
    let n = 0; ng = ng.replace(/<span class="mm3-n">[^<]*<\/span>/g, () => '<span class="mm3-n">' + String(++n).padStart(2, '0') + '</span>');
    res = res.slice(0, g0) + ng + res.slice(sEnd);
    notes.push(`main: +${main.length} (grid now ${n})`);
  }
  if (hol.length) {
    let out = holAppend(res, 'holiday-matches', hol);
    if (out == null) {  // no holiday section yet: add one right after the main grid section
      const at = res.indexOf('</section>', res.indexOf('<div class="mm3-grid"', hm.index)) + 10;
      const css = res.includes('.mm3-hol{') ? '' : (opt.css || '');
      const sec = css + '<section class="mm3-hol" id="holiday-matches"><h2>Holiday matches for ' + setName + '</h2><p class="mm3-sub">' + hol.length +
        ' mat match' + (hol.length == 1 ? '' : 'es') + ', Christmas, Hanukkah and winter mats for ' + setName +
        ', with rack picks. See more holiday matches on the <a href="/holiday-mahjong-matches">Holiday Matches</a> page.</p><div class="mm3-grid">' +
        hol.map((f, k) => num(f, k + 1)).join('') + '</div></section>';
      out = res.slice(0, at) + sec + res.slice(at);
      notes.push(`new holiday section: ${hol.length}` + (css ? ' (+css)' : ''));
    }
    res = out;
  }
  const added = main.length + hol.length;
  const newBrands = [...new Set([...main, ...hol].map(brandOf))].filter(b => !before.has(b));
  const esc = setName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/&/g, '(?:&|&amp;)');
  let hits = 0, cnt = '';
  res = res.replace(new RegExp('all (\\d+) (' + esc + ') mat matches from (\\d+) brands', 'g'),
    (m, a, nm, b) => { hits++; return (cnt = `all ${+a + added} ${nm} mat matches from ${+b + newBrands.length} brands`); });
  if (!hits) res = res.replace(new RegExp('\\b(\\d+) (' + esc + ') mat matches', 'g'), (m, a, nm) => { hits++; return (cnt = `${+a + added} ${nm} mat matches`); });
  notes.push(`counts: ${cnt || 'none found'} x${hits}; new brands: ${newBrands.join(', ') || 'none'}`);
  return {src: res, note: notes.join('; ')};
}
if (typeof module !== 'undefined') module.exports = missedFix; else window.missedFix = missedFix;
