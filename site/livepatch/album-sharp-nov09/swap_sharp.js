// album-sharp-nov09: swap card image srcs inside the album page's code block (pairs from swap.json). Each old src must occur exactly once.
window.sharpSwap=function(src,pairs){let n=0,bad=[];let out=src;for(const [o,nw] of pairs){const c=out.split(o).length-1;if(c!==1){bad.push(o.slice(-70)+' x'+c);continue}out=out.split(o).join(nw);n++}
const dl=pairs.reduce((a,[o,nw])=>a+nw.length-o.length,0);return {src:out,ok:n===pairs.length&&bad.length===0&&out.length-src.length===dl,note:`swapped ${n}/${pairs.length}; bad ${bad.length}; lenΔ ${out.length-src.length} (expect ${dl})`,bad}};
