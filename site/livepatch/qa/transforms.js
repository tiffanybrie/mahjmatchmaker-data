// Oct 18 approved live fixes, applied as string transforms on a code block's source.
(function(root){
const MF_OLD='https://myfairmahjong.com/tiffany817';
const MF_NEW='https://myfairmahjong.com/products/acrylic-mahjong-racks?sca_ref=10090290.TW8PinT201';
const LINKS=[[MF_OLD,MF_NEW],
 ['https://www.ohmymahjong.com/products/lagoon-ultimate-starter-kit','https://www.ohmymahjong.com/products/lagoon-ultimate-starter'],
 ['https://www.ohmymahjong.com/products/nantucket-ultimate-starter-kit','https://www.ohmymahjong.com/products/nantucket-tiles'],
 ['https://www.ohmymahjong.com/products/nantucket-starter-kit','https://www.ohmymahjong.com/products/nantucket-tiles']];
function links(s){let n=0; for(const [o,w] of LINKS){const re=new RegExp('href="'+o.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'"','g'); s=s.replace(re,()=>{n++;return 'href="'+w+'"'});} return [s,n];}
const RET_URLS=['liberty-mat-w-tube','holly-jolly-mat-in-tube','anthro-goldie-mat-w-tube'];
const PILL='<span class="mm3-btn" style="background:#9a8f86!important;border-color:#9a8f86!important;color:#fff!important;cursor:default;pointer-events:none">Retired</span>';
function retire(s,handles){handles=handles||RET_URLS; let n=0;
 const hre='https?://(?:www\\.)?ohmymahjong\\.com/products/(?:'+handles.join('|')+')[^"]*';
 // 1) shop buttons in match cards -> grey non-link "Retired" pill
 s=s.replace(new RegExp('<a class="mm3-btn" href="'+hre+'"[^>]*>[^<]*</a>(<span class="mm3-code">[^<]*</span>)?','g'),()=>{n++;return PILL});
 // 2) any other link to these mats -> plain text + " (retired)" (unless already says retired)
 s=s.replace(new RegExp('<a [^>]*href="'+hre+'"[^>]*>([\\s\\S]*?)</a>(\\s*\\(retired\\))?','g'),(m,txt,already)=>{n++; return txt+(already||/retired/i.test(txt)?(already||''):' (retired)')});
 return [s,n];}
root.MMFIX={links,retire,PILL};
})(typeof window!=='undefined'?window:globalThis);
