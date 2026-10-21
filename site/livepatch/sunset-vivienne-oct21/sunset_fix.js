// vivFix(src, setName, FIG) -> {src, note}. src = the album's main code block source (the one containing "Every <Set> match").
// Inserts the Vivienne match card as #4 (right after her top 3 picks, which the FAQ names), renumbers the main grid (2-digit),
// and bumps "all N <Set> mat matches from M brands" (FAQ text + JSON-LD) by +1 match; brands unchanged (Vivienne is Oh My Mahjong, already counted).
function vivFix(src, setName, FIG){
  if (src.includes('oh-my-mahjong-vivienne-mat')) return {src, note:'already'};
  const h = src.indexOf('Every ' + setName + ' match'); if (h < 0) throw 'no main heading for ' + setName;
  const g0 = src.indexOf('<div class="mm3-grid">', h); const gEnd = src.indexOf('</section>', g0);
  const grid = src.slice(g0, gEnd);
  const figs = grid.match(/<figure class="mm3-c[ "][\s\S]*?<\/figure>/g);
  if (!figs || figs.length < 3) throw 'grid too short';
  const out = figs.slice(0, 3).concat([FIG], figs.slice(3)).join('');
  const firstFig = grid.indexOf(figs[0]); const lastEnd = grid.lastIndexOf(figs[figs.length-1]) + figs[figs.length-1].length;
  let ng = grid.slice(0, firstFig) + out + grid.slice(lastEnd);
  let n = 0; ng = ng.replace(/<span class="mm3-n">[^<]*<\/span>/g, () => '<span class="mm3-n">' + String(++n).padStart(2,'0') + '</span>');
  let res = src.slice(0, g0) + ng + src.slice(gEnd);
  const esc = setName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  let cnt = '';
  res = res.replace(new RegExp('all (\\d+) ' + esc + ' mat matches from (\\d+) brands', 'g'), (m, a, b) => (cnt = `all ${+a + 1} ${setName} mat matches from ${b} brands`));
  return {src: res, note: `grid ${n}; ${cnt}`};
}
if (typeof module !== 'undefined') module.exports = vivFix; else window.vivFix = vivFix;
