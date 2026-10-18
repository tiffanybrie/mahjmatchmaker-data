// Apply to the live Pearlescent code block source (string -> string). Inserts the 3 approved Oct 18 cards:
// Rainbow Row + Pink Floral Chinoiserie as TOP (#7, #8, right after Rally in Pink #6); Secret Garden at the end of the main grid.
// Renumbers the main grid (2-digit) and updates the "all N Pearlescent mat matches from M brands" line. Idempotent (no-op if already inserted).
function pearlFix(src, TOP, END){
  if (src.includes('pearlescent-mahjong-tiles-rebecca-illustrated-rainbow-row-mat')) return {src, note:'already'};
  const h = src.indexOf('Every Pearlescent match'); if (h < 0) throw 'no main heading';
  const g0 = src.indexOf('<div class="mm3-grid">', h); const gEnd = src.indexOf('</section>', g0);
  const grid = src.slice(g0, gEnd);
  const figs = grid.match(/<figure class="mm3-c"[\s\S]*?<\/figure>/g);
  const sixth = figs.findIndex(f => f.includes('Rally in Pink'));
  if (sixth < 0) throw 'no rally';
  const out = figs.slice(0, sixth+1).concat([TOP], figs.slice(sixth+1), [END]).join('');
  const firstFig = grid.indexOf(figs[0]); const lastEnd = grid.lastIndexOf(figs[figs.length-1]) + figs[figs.length-1].length;
  let ng = grid.slice(0, firstFig) + out + grid.slice(lastEnd);
  let n = 0; ng = ng.replace(/<span class="mm3-n">[^<]*<\/span>/g, () => '<span class="mm3-n">' + String(++n).padStart(2,'0') + '</span>');
  const brands = new Set([...ng.matchAll(/Mat by (?:<a[^>]*>)?([^<]+)/g)].map(m => m[1].trim()));
  let res = src.slice(0, g0) + ng + src.slice(gEnd);
  res = res.replace(/all \d+ Pearlescent mat matches from \d+ brands/g, `all ${n} Pearlescent mat matches from ${brands.size} brands`);
  return {src: res, note: `figs ${n}, brands ${brands.size}`};
}
if (typeof module !== 'undefined') module.exports = pearlFix; else window.pearlFix = pearlFix;
