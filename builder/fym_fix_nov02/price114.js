/* v114 PRICE FILTER on the app's own decks (Tiffany Nov 1 5:45pm, coordinator Nov 1 overnight): mat deck (tiles door),
   tile deck (mat door), rack deck. Same chips and rules as the Table view swap sheet: ranges from the 20/40/60/80th
   percentiles per category (TVD.pr), the price after code MAHJMATCH only where the code % is verified in our repo
   (config/fym-code-pct.json), otherwise the store price; items with no listed price drop out and the count is shown;
   a chip that would empty the deck shows everything with a note instead (never empties silently); cards show the store
   price + 'less with code MAHJMATCH' while a price chip is on. A Table-view swap (S.tvforce / S.tvrf / S.tfront) is
   never filtered out. Default: Any price. Uses TVD (prices) from the Table view block. */
(function(){
S.pr=S.pr||{m:'',t:'',r:''};S.prE={m:0,t:0,r:0};S.prN={m:0,t:0,r:0};
const CAT={m:'mat',t:'tiles',r:'racks'};
function PRP(k,id){if(typeof TVD!=='object')return null;if(k==='m')return TVD.pm[id]||null;if(k==='r')return TVD.price[id]||null;const s=D.sets[id];return s?(TVD.pt[s.tile]||null):null}
const forced=(k,id)=>(k==='m'&&id===S.tvforce&&id===S.mfront)||(k==='r'&&id===S.tvrf);
function PRF(k,ids){S.prE[k]=0;S.prN[k]=0;const v=S.pr[k];if(v==='')return ids;S.prN[k]=ids.filter(id=>!PRP(k,id)).length;
  const f=ids.filter(id=>forced(k,id)||((x=>x&&x[1]<=v)(PRP(k,id))));if(!f.filter(id=>!forced(k,id)).length&&ids.length){S.prE[k]=1;return ids}return f}
window.PRF=PRF;
const _md=matDeck;matDeck=function(){return PRF('m',_md())};
const _rd=rackDeck;rackDeck=function(){return PRF('r',_rd())};
const _sf=setsForMat;setsForMat=function(id){const g=_sf(id);if(S.pr.t==='')return g;const all=[...(g.her||[]),...(g.alb||[]),...(g.cat||[])];
  const keep=new Set(PRF('t',all.map(r=>r.i)));if(S.prE.t)return g;const f=a=>(a||[]).filter(r=>keep.has(r.i));return Object.assign({},g,{her:f(g.her),alb:f(g.alb),cat:f(g.cat)})};
const money=v=>'$'+(Math.round(v)===v?v:v.toFixed(2));
window.PRB=function(k){const r=((typeof TVD==='object'&&TVD.pr)||{})[CAT[k]]||[];if(!r.length)return '';
  try{if(k==='m')matDeck();else if(k==='r')rackDeck();else if(S.dmat)setsForMat(S.dmat)}catch(x){}const v=S.pr[k];
  return `<div class="prw" role="group" aria-label="Price"><button type="button" class="chip prc" data-prc="${k}" data-v="" aria-pressed="${v===''}">Any price</button>${r.map(x=>`<button type="button" class="chip prc" data-prc="${k}" data-v="${x}" aria-pressed="${v===x}">Under $${x}</button>`).join('')}</div>`+
   (v!==''?`<small class="prn">${S.prE[k]?`Nothing under $${v} here, so showing all. `:''}${S.prN[k]?`${S.prN[k]} without a listed price not shown. `:''}Prices: store price, or less with code MAHJMATCH where it applies.</small>`:'')};
/* QA Nov 2: a card that is under the chip only after the code says so: 'Under $65 with code MAHJMATCH' (no % printed) */
window.PRC=function(k,id){const v=S.pr[k];if(v==='')return '';const x=PRP(k,id);if(!x)return '';const viaCode=x[2]&&x[0]>v&&x[1]<=v;
  return `<b class="prc1">${money(x[0])}${viaCode?` <em class="prcv">Under $${v} with code MAHJMATCH</em>`:(x[2]?' <em>less with code MAHJMATCH</em>':'')}</b>`};
/* the in-stock chip row of the mat and rack decks carries the price row right after it */
const _ib=INSB;INSB=function(k){return _ib(k)+(k==='m'||k==='r'?PRB(k):'')};
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-prc]');if(!b)return;e.preventDefault();e.stopPropagation();
  const k=b.dataset.prc,v=b.dataset.v===''?'':+b.dataset.v;S.pr[k]=S.pr[k]===v?'':v;
  if(k==='m'){S.peek=null;renderMats()}else if(k==='r')renderRacks();else renderTiles();if(typeof steps==='function')steps()},true);
})();
