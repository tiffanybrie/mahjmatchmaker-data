// Retired tile-set labels (Tiffany yes Oct 19, RTS l-retired-tiles / l-retired-tiles2).
// List = config/tile-retired.json recommend:"retired" with an album. Sunday Mahjong never retired.
// Each function takes a code block's text and returns the new text. Idempotent.
var RET = {"birdie":"Birdie","dandy":"Dandy","glitterville":"Glitterville","heritage":"Heritage",
  "lilac-soiree":"Lilac Soiree","limoncello":"Limoncello","lola":"Lola","preppy-soiree":"Preppy Soiree",
  "shangri-la":"Shangri La","sorbet":"Sorbet","spring-love":"Spring Love","sunset":"Sunset","taylor":"Taylor"};
var PILL_CSS = '<style id="mm-retpill-css">.mmalb-c,.mmcol-card{position:relative}.mm-retpill{position:absolute;top:8px;left:8px;z-index:2;background:#9a8f86;color:#fff!important;font-style:normal;font-weight:700;font-size:10px;line-height:1;letter-spacing:.12em;text-transform:uppercase;padding:5px 9px;border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,.18);pointer-events:none}</style>';
function coverPills(code){
  var n = 0;
  Object.keys(RET).forEach(function(s){
    var re = new RegExp('(<a class="(?:mmalb-c|mmcol-card)" href="/' + s + '-mahjong-tile-matches"[^>]*>)(?!<em class="mm-retpill">)', 'g');
    code = code.replace(re, function(m, a){ n++; return a + '<em class="mm-retpill">Retired</em>'; });
  });
  if (code.indexOf('mm-retpill-css') < 0 && code.indexOf('mm-retpill') >= 0) code = PILL_CSS + code;
  coverPills.count = n;
  return code;
}
var RETP = function(name){ return '<p><strong>' + name + ' is retired</strong>, so Oh My Mahjong no longer sells it, but lots of players still own it and look for mats to go with it. Mats with a Shop button are available now, and mats marked Retired can often be found secondhand in buy/sell groups.</p>'; };
var HERP = '<p><strong>Heritage (the original Heritage 1.0) is retired</strong>, so Oh My Mahjong no longer sells it, but lots of players still own it and look for mats to go with it. Oh My Mahjong now sells <a href="/heritage-2-0-mahjong-tile-matches">Heritage 2.0</a>, which has its own album. Mats with a Shop button are available now, and mats marked Retired can often be found secondhand in buy/sell groups.</p>';
function albumHeader(code, slug){
  var name = RET[slug]; if (!name) throw new Error('not retired: ' + slug);
  if (code.indexOf('mm3-tret') >= 0) return code;  // already labelled
  var k = code.indexOf('<p class="mm3-kicker">Oh My Mahjong</p>');
  if (k < 0) throw new Error('kicker not found');
  code = code.replace('<p class="mm3-kicker">Oh My Mahjong</p>', '<p class="mm3-kicker">Oh My Mahjong <span class="mm3-ret mm3-tret">Retired tile set</span></p>');
  var i = code.indexOf('<div class="mm3-intro">'); var j = code.indexOf('</div><p class="mm3-cta">', i);
  if (i < 0 || j < 0) throw new Error('intro not found');
  code = code.slice(0, j) + (slug === 'heritage' ? HERP : RETP(name)) + code.slice(j);
  if (slug === 'heritage') {
    var old = '<a class="mm3-btn mm3-btn-l" href="https://www.ohmymahjong.com/products/heritage-tiles" target="_blank" rel="sponsored noopener">Shop Heritage at Oh My Mahjong</a>';
    if (code.indexOf(old) < 0) throw new Error('heritage button not found');
    code = code.replace(old, '<a class="mm3-btn mm3-btn-l" href="https://www.ohmymahjong.com/collections/mahjong-mats" target="_blank" rel="sponsored noopener">Shop Current Oh My Mahjong Mats</a>');
  }
  return code;
}
if (typeof module !== 'undefined') module.exports = {RET: RET, coverPills: coverPills, albumHeader: albumHeader};
