// Holiday fix Nov 9: swap card images (and Dec 1994 rack captions) inside one holiday-page code block.
// usage in the Squarespace code editor: const r=swapFix(v.state.doc.toString(), SWAP.sections['<sid>']); r.note; then dispatch r.src
window.swapFix=function(src,pairs){let n=0,miss=[],multi=[];for(const [o,nw] of pairs){const c=src.split(o).length-1;if(c===0){miss.push(o.slice(-80));continue}if(c>1)multi.push(o.slice(-60)+' x'+c);src=src.split(o).join(nw);n++}return {src,note:`swapped ${n}/${pairs.length}; missing ${miss.length}; multi ${multi.length}`,miss,multi}};
