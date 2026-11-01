// /christmas-mahjong-mats stock labels (Nov 1 2026). Same function runs in node (repo) and in the Squarespace editor (CodeMirror doc).
// Retired (product gone: 404 + not in the brand's products.json): grey "Retired" pill, no shop links, match count kept.
// Sold out (store says unavailable; may restock): grey "Sold out" pill, shop link kept ("Sold out · see the mat").
function stockLabels(code){
  var RETIRED=['https://www.ohmymahjong.com/products/sugarplum-mat'];
  var SOLD=['mahjsquadshop.com/products/candy-cane-pink-wonderland-mahjong-mat','brittmillsdesign.com/products/merrywood-neoprene-mahjong-mat','brittmillsdesign.com/products/winter-berry-neoprene-mahjong-mat','brittmillsdesign.com/products/nutcracker-neoprene-mahjong-mat','mahjmood.com/products/sleigh-all-day-mat','viroramahjong.com/products/hiverelle'];
  var CSS='<style id="mmg-stock-css">.mmg-img{position:relative}.mmg-pill{position:absolute;top:8px;left:8px;z-index:2;background:#9a8f86;color:#fff;font-style:normal;font-weight:700;font-size:10px;line-height:1;letter-spacing:.12em;text-transform:uppercase;padding:5px 9px;border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,.18);pointer-events:none}.mmg-card.is-retired .mmg-img img,.mmg-card.is-sold .mmg-img img{opacity:.82}.mmg-gone{margin-top:auto;padding-top:8px;font-weight:700;font-size:.85em;color:#9a8f86}</style>';
  var n={retired:0,sold:0};
  code=code.replace(/<li class="mmg-card"( data-tags="[^"]*")><a class="mmg-img" href="([^"]+)"([^>]*)>([\s\S]*?)<\/li>/g,function(all,tags,href,attrs,rest){
    if(RETIRED.some(function(u){return href.split('?')[0]===u})){
      n.retired++;
      var img=rest.slice(0,rest.indexOf('</a>'));
      var body=rest.slice(rest.indexOf('</a>')+4).replace(/<a class="mmg-shop"[^>]*>[^<]*<\/a>/,'<span class="mmg-gone">Retired · no longer sold</span>');
      return '<li class="mmg-card is-retired"'+tags+'><span class="mmg-img"><em class="mmg-pill">Retired</em>'+img+'</span>'+body+'</li>';
    }
    if(SOLD.some(function(u){return href.indexOf(u)>-1})){
      n.sold++;
      return '<li class="mmg-card is-sold"'+tags+'><a class="mmg-img" href="'+href+'"'+attrs+'><em class="mmg-pill">Sold out</em>'+rest.replace(/(<a class="mmg-shop"[^>]*>)Shop the mat(<\/a>)/,'$1Sold out · see the mat$2')+'</li>';
    }
    return all;
  });
  if(code.indexOf('mmg-stock-css')<0 && (n.retired||n.sold)) code=CSS+code;
  return {code:code,n:n};
}
if(typeof module!=='undefined') module.exports=stockLabels;
