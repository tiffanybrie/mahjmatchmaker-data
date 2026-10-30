// TdT visible-code fix for album match cards (Tiffany Oct 30 12:04-12:10am, ANSWERS; TdT affiliate policy).
// On Tigre de Tartan mat cards only: "code MAHJMATCH" -> "save 10% with my link", and the Shop button
// goes to the auto-apply link (code rides inside the URL, not visible text). Alt text / other cards untouched.
// Same function runs in node (preview/check) and in the Squarespace code-block editor. Idempotent.
var TDT_REF = 'sca_ref=11798386.tvil8GTGTp6s2';
// any tigredetartan.com URL -> auto-apply form; same output as scripts/albumcard/tdt_policy.py tdt_link()
function tdtLink(path, query){
  if (path.replace(/\/$/, '') === '/mahjmatchmaker' || path === '') path = '/';
  var q = (query || '').replace(/^\?/, '').replace(/&amp;/g, '&').split('&').filter(function(x){ return x && x.indexOf('sca_ref=') !== 0; });
  q.push(TDT_REF);
  return 'https://tigredetartan.com/discount/MAHJMATCH?redirect=' + encodeURIComponent(path + '?' + q.join('&'));
}
function tdtFix(code){
  var n = 0, links = 0;
  code = code.replace(/<figure class="mm3-c[^"]*">[\s\S]*?<\/figure>/g, function(fg){
    if (!/Mat by (<a [^>]*>)?Tigre de Tart/.test(fg)) return fg;
    if (fg.indexOf('<span class="mm3-code">code MAHJMATCH</span>') < 0) return fg;
    n++;
    fg = fg.replace('<span class="mm3-code">code MAHJMATCH</span>', '<span class="mm3-code">save 10% with my link</span>');
    fg = fg.replace(/(<a class="mm3-btn" href=")https:\/\/tigredetartan\.com(?!\/discount\/)(\/[^"?#]*)?(\?[^"#]*)?"/,
      function(m, a, p, q){ links++; return a + tdtLink(p || '/', q) + '"'; });
    return fg;
  });
  return {code: code, cards: n, links: links};
}
if (typeof module !== 'undefined') module.exports = {tdtFix: tdtFix, tdtLink: tdtLink};
