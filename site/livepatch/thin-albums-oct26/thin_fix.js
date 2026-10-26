// thinFix(src, setName, CARDS) -> {src, note}. src = the album's main code block source (the one containing "Every <Set> match").
// CARDS = the raw <set>-cards.html (one or more <figure class="mm3-c"> cards, Tiffany's thin-album hearts Oct 23-24).
// Appends the new cards at the END of the main grid (after the last card, before </section>, so holiday sections are untouched),
// renumbers the main grid (2-digit), and bumps "all N <Set> mat matches from M brands" (FAQ text + JSON-LD) by
// +cards added and +brands not already on the page (counts include the holiday sections, so we bump rather than recount).
// Idempotent: a card whose image file is already on the page is skipped.
function thinFix(src, setName, CARDS){
  const h = src.indexOf('Every ' + setName + ' match'); if (h < 0) throw 'no main heading for ' + setName;
  const g0 = src.indexOf('<div class="mm3-grid">', h); const gEnd = src.indexOf('</section>', g0);
  if (g0 < 0 || gEnd < 0) throw 'no main grid for ' + setName;
  const grid = src.slice(g0, gEnd);
  const figs = grid.match(/<figure class="mm3-c[ "][\s\S]*?<\/figure>/g);
  if (!figs || figs.length < 3) throw 'grid too short';
  const fileOf = f => (f.match(/\/assets\/cards\/[^"]*\/([^"\/]+\.jpg)"/) || [])[1];
  const brandOf = f => { const m = f.match(/<span class="mm3-by">Mat by (?:<a[^>]*>)?([^<]+)/); return m ? m[1].trim() : ''; };
  const onPage = new Set(figs.map(brandOf));
  const add = (CARDS.match(/<figure class="mm3-c[ "][\s\S]*?<\/figure>/g) || []).filter(f => !src.includes(fileOf(f)));
  if (!add.length) return {src, note: 'already'};
  const newBrands = [...new Set(add.map(brandOf))].filter(b => !onPage.has(b));
  const lastEnd = grid.lastIndexOf(figs[figs.length-1]) + figs[figs.length-1].length;
  let ng = grid.slice(0, lastEnd) + add.join('') + grid.slice(lastEnd);
  let n = 0; ng = ng.replace(/<span class="mm3-n">[^<]*<\/span>/g, () => '<span class="mm3-n">' + String(++n).padStart(2,'0') + '</span>');
  let res = src.slice(0, g0) + ng + src.slice(gEnd);
  const esc = setName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  let cnt = '', hits = 0;
  res = res.replace(new RegExp('all (\\d+) ' + esc + ' mat matches from (\\d+) brands', 'g'),
    (m, a, b) => { hits++; return (cnt = `all ${+a + add.length} ${setName} mat matches from ${+b + newBrands.length} brands`); });
  return {src: res, note: `added ${add.length} (new brands: ${newBrands.join(', ') || 'none'}); grid ${n}; ${cnt} x${hits}`};
}
if (typeof module !== 'undefined') module.exports = thinFix; else window.thinFix = thinFix;
