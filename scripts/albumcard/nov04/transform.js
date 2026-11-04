function mmTransform(src, figs, opt){
  // opt: {sid: section id ('holiday-matches' for albums), newSection: tileName|null, css: holcss}
  const renum=(arr,start)=>arr.map((f,i)=>f.replace('<span class="mm3-n">00</span>','<span class="mm3-n">'+String(start+i).padStart(2,'0')+'</span>'));
  let i=src.indexOf('id="'+opt.sid+'"');
  if(i<0){
    if(!opt.newSection) throw new Error('no section '+opt.sid);
    const foot=src.indexOf('<p class="mm3-foot">'); if(foot<0) throw new Error('no foot');
    const at=src.lastIndexOf('</section>',foot); if(at<0) throw new Error('no main section end');
    const t=opt.newSection;
    const sec=(src.includes('.mm3-hol{')?'':opt.css)+'<section class="mm3-hol" id="holiday-matches"><h2>Holiday matches for '+t+'</h2><p class="mm3-sub">Christmas, Hanukkah and winter mats for '+t+', with rack picks. See more holiday matches on the <a href="/holiday-mahjong-matches">Holiday Matches</a> page.</p><div class="mm3-grid">'+renum(figs,1).join('')+'</div></section>';
    return {out: src.slice(0,at+10)+sec+src.slice(at+10), before:0, after:figs.length};
  }
  const end=src.indexOf('</section>',i);
  const seg=src.slice(i,end);
  const nums=[...seg.matchAll(/<span class="mm3-n">(\d+)<\/span>/g)].map(m=>+m[1]); const n=nums.length?Math.max(...nums):0; // continue the section's own numbering (QA Nov 4: Spring Love/Shangri-La sections continue from the main grid)
  const gEnd=seg.lastIndexOf('</div>'); // closes mm3-grid
  if(gEnd<0) throw new Error('no grid end');
  let nseg=seg.slice(0,gEnd)+renum(figs,n+1).join('')+seg.slice(gEnd);
  nseg=nseg.replace(/<p class="mm3-sub">(\d+) mat match(es)?,/,(m,a)=>{const k=+a+figs.length;return '<p class="mm3-sub">'+k+' mat match'+(k==1?'':'es')+',';});
  return {out: src.slice(0,i)+nseg+src.slice(end), before:n, after:n+figs.length};
}
if(typeof module!=='undefined') module.exports=mmTransform;
