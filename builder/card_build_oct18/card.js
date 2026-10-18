/* ---------- match card (Oct 18 redesign, approved): Love triangle = spread, Mood board = close-up bands, Shop = showcase.
   Drawn at 2x for crisp exports; tiles, racks and logos come from HD chunks (hd/*.json) with the bundled thumbnails as fallback. ---------- */
const VIEWS=[['tri','Love triangle'],['stack','Mood board'],['shop','Shop']];
let cardURL='',cardJob=0;
function pieces(){return [set().tile,S.fav,...S.rpick];}
function allPartner(){return T[set().tile].pa&&!T[set().tile].nc&&M[S.fav].pa&&!M[S.fav].nc&&S.rpick.every(r=>R[r].pa&&!R[r].nc);}
function renderCard(){const st=$('s-card');const s=set();
 st.innerHTML=`<div class="sh"><span class="num">4</span><div><h2>Your match card</h2></div></div><div class="hello" style="padding-top:0"><h1 style="font-size:clamp(26px,7.4vw,34px)">It’s a match!</h1><p>${esc(s.name)} + ${esc(M[S.fav].n)}. Pick your view, then save it or send it to your mahj group.</p></div>
 <div class="seg" role="group" aria-label="View">${VIEWS.map(v=>`<button type="button" data-view="${v[0]}" aria-pressed="${S.view===v[0]}">${v[1]}</button>`).join('')}</div>
 <div class="seg nv" role="group" aria-label="Size"><button type="button" data-fmt="fb" aria-pressed="${S.fmt==='fb'}">Facebook post</button><button type="button" data-fmt="pin" aria-pressed="${S.fmt==='pin'}">Pinterest pin</button></div>
 <div class="prev" id="prev"><div class="ld">Dressing up your match…</div></div>
 <p class="hint">On your phone, press and hold the picture to save it.</p>
 <button type="button" class="big" data-share>Save or share my match card</button>
 <div class="mailbox"><h3>Email me my match card</h3><p>We’ll email you the view you picked in both sizes: a post size and a tall pin size.</p><div class="row"><input type="email" id="em" placeholder="you@email.com" autocomplete="email" aria-label="Email"><button type="button" data-mail>Send</button></div><div id="mailok" hidden></div></div>
 <div class="shop"><h3>Take them home</h3>${pieces().map(id=>{const o=M[id]||R[id]||T[id];const im=M[id]?matTh(id):R[id]?rackSrc(id):pile(set());const nm=T[id]?set().name:R[id]?o.n:o.n;
  return `<div class="si"><img src="${im}" alt=""><div class="tx"><b>${esc(nm)}</b><small>${esc(o.bn)}</small>${M[id]&&o.alt?`<em class="alt">${esc(o.alt)}</em>`:''}${o.dc?`<a class="dc" href="${esc(o.dc)}" target="_blank" rel="noopener">Discount code ›</a>`:''}</div><a class="go" href="${esc(o.u)}" target="_blank" rel="noopener">${o.rt?'Retired':'Shop ›'}</a></div>`;}).join('')}</div>
 <button type="button" class="lnk" data-restart>Start over with new tiles</button>`;
 drawCard();}
const lk=src=>new Promise(r=>{if(!src)return r(null);const i=new Image();i.onload=()=>r(i);i.onerror=()=>r(null);i.src=src;});
/* HD images: hd/index.json maps tile key / rack id / brand -> chunk file; chunks map key -> data URI. */
const HDC={};let HDI=null;
const hdIndex=()=>HDI||(HDI=fetch('hd/index.json').then(r=>r.ok?r.json():{}).catch(()=>({})));
async function hd(kind,key){try{const ix=await hdIndex();const c=(ix[kind]||{})[key];if(!c)return '';if(c.startsWith('file:'))return c.slice(5);if(!HDC[c])HDC[c]=fetch('hd/'+c).then(r=>r.json()).catch(()=>({}));return (await HDC[c])[key]||'';}catch(e){return '';}}
const hdOr=async(kind,key,fb)=>(await hd(kind,key))||fb||'';
/* Short rack label: colour name only (brand and product words dropped). "Middle & Main Hawksbill Heritage (tortoise)" -> "Tortoise". */
const RL_JUNK=/\b(mahjong|mah jongg|racks?|pushers?|pusher set|set|sets|of|pieces?|acrylic|premium|signature|luxury|luxe|handmade|wooden|wood|classic|heritage|hawksbill|scalloped|scallop|with|built-in|attached|game|bag|the|magnetic|hinged|logo|collection|accessory|preorder|matte|finish|straight|double|two player|modern|new|shelf|angle|options?|color options|tile|only|included|no|patent|pending|american|solid|colors|multiple|inch|in|and|w)\b/gi;
const RL_COL=/\b(white|black|clear|ivory|cream|pink|red|green|blue|navy|purple|lilac|yellow|orange|teal|aqua|mint|jade|tortoise|tortoiseshell|walnut|oak|burl|agate|marble|quartz|pearl|opal|brass|gold|silver|chartreuse|coral|peach|plum|lavender|mauve|magenta|cobalt|emerald|sapphire|turquoise|sand|sandstone|carrara|camphor|pine|mahogany|chestnut|cola|beechwood|lucite)\b/i;
function rackLabel(id){const r=R[id];let t=shortR(id);const par=t.match(/\(([^)]+)\)/);if(par&&RL_COL.test(par[1]))return par[1].replace(/\b\w/g,c=>c.toUpperCase());
 const core=(r.bn||'').replace(/\s*(Mahjong|Mahj Jongg|Imports|Boutique)\s*$/i,'').trim();if(core&&t.toLowerCase().startsWith(core.toLowerCase()))t=t.slice(core.length).trim();
 t=t.replace(/\([^)]*\)/g,' ').replace(/\s+and\s+/gi,' & ');
 const clean=x=>x.replace(/\d+(\.\d+)?\s*(-?inch|in|["”″])?/gi,' ').replace(RL_JUNK,' ').replace(/[“”"″,|+()!]/g,' ').replace(/\s&\s*$/,'').replace(/^\s*&\s/,'').replace(/\s+/g,' ').replace(/^(&|-)\s*|\s*(&|-)$/g,'').trim();
 const segs=t.split(/\s+[–—|-]\s+|\s*\|\s*/).map(clean).filter(x=>x&&x.length>1);
 let pick=segs.find(x=>RL_COL.test(x))||segs[segs.length-1]||'';
 pick=pick.split(' ').map(w=>w===w.toUpperCase()&&w.length>2?w[0]+w.slice(1).toLowerCase():w).join(' ');
 pick=clean(pick.replace(/\s-\s*$/,''));if(!/[A-Za-z]{3}/.test(pick)||/^(of|pusher|pushers|set|racks?|mahjong)\b/i.test(pick)){const cs=(r.n.match(new RegExp(RL_COL.source,'gi'))||[]).slice(0,2);pick=cs.length?cs.map(c=>c[0].toUpperCase()+c.slice(1).toLowerCase()).join(' '):'';}
 if(!pick)pick=/luxe/i.test(r.n)?'Luxe':/acrylic|lucite/i.test(r.n)?'Acrylic':/wood/i.test(r.n)?'Wood':'Racks';
 const w=pick.split(' ').filter(Boolean);if(!w.length)return shortR(id).split(' ').slice(-2).join(' ');
 if(w.length>3){const k=w.indexOf('&');return (k>0?w.slice(Math.max(0,k-1),k+2):w.slice(-2)).join(' ');}return w.join(' ');}
async function drawCard(){const job=++cardJob;
 try{await Promise.all(['400 100px Caprasimo','italic 500 40px "Playfair Display"','700 30px Bitter','600 26px Bitter'].map(f=>document.fonts.load(f)));}catch(e){}
 const s=set(),fb=S.fmt==='fb',W=fb?1080:1000,H=fb?1350:1500,SC=2;
 const PINK='#c8325f',NAVY='#054689',INK='#2a2036',MUTE='#7a6a85',CREAM='#f7ece3';
 const tb=T[s.tile].bn,mb=M[S.fav].bn,rp=S.rpick,rb=[...new Set(rp.map(r=>R[r].bn))];
 const [mat,tile,ours,icon,rks,tl,ml,rl]=await Promise.all([matFull(S.fav).then(lk),hdOr('t',s.tile,pile(s)).then(lk),hdOr('l','ours',LG('ours')).then(lk),hdOr('l','icon',LG('icon')).then(lk),
  Promise.all(rp.map(r=>hdOr('r',r,rackSrc(r)).then(lk))),hdOr('l',tb,LG(tb)).then(lk),hdOr('l',mb,LG(mb)).then(lk),Promise.all(rb.map(b=>hdOr('l',b,LG(b)).then(lk)))]);
 if(job!==cardJob)return;
 const cv=document.createElement('canvas');cv.width=W*SC;cv.height=H*SC;const g=cv.getContext('2d');g.scale(SC,SC);g.imageSmoothingEnabled=true;g.imageSmoothingQuality='high';
 const ls=px=>{try{g.letterSpacing=px+'px';}catch(e){}};
 const fit=(im,x,y,w,h)=>{if(!im)return null;const k=Math.min(w/im.width,h/im.height);const dw=im.width*k,dh=im.height*k;const dx=x+(w-dw)/2,dy=y+(h-dh)/2;g.drawImage(im,dx,dy,dw,dh);return {x:dx,y:dy,w:dw,h:dh};};
 const cover=(im,x,y,w,h,r,zoom=1,fx=.5,fy=.5)=>{if(!im)return;g.save();g.beginPath();g.roundRect(x,y,w,h,r);g.clip();const k=Math.max(w/im.width,h/im.height)*zoom;const dw=im.width*k,dh=im.height*k;g.drawImage(im,x+(w-dw)*fx,y+(h-dh)*fy,dw,dh);g.restore();};
 const shadow=(c,b,oy)=>{g.shadowColor=c;g.shadowBlur=b;g.shadowOffsetY=oy;};
 const noShadow=()=>{g.shadowColor='transparent';g.shadowBlur=0;g.shadowOffsetY=0;};
 const card=(x,y,w,h,r)=>{g.save();shadow('rgba(50,25,35,.16)',14,5);g.fillStyle='#fff';g.beginPath();g.roundRect(x,y,w,h,r);g.fill();g.restore();};
 const clip=(t,mw)=>{let n=t;while(g.measureText(n).width>mw&&n.length>4)n=n.slice(0,-2).trim()+'…';return n;};
 const pill=(x,y,kicker,name,o={})=>{const fsK=o.fsK||13,fsN=o.fsN||21,padX=15,h=fsN+fsK+22;
  g.font=`700 ${fsK}px Bitter, Georgia, serif`;ls(3);const wk=g.measureText(kicker).width;ls(0);g.font=`600 ${fsN}px Bitter, Georgia, serif`;const nm=clip(name,(o.maxW||600)-2*padX);const wn=g.measureText(nm).width;
  const w=Math.max(wk,wn)+2*padX,X=o.right?x-w:x,Y=o.up?y-h:y;g.save();shadow('rgba(40,20,30,.18)',10,3);g.fillStyle='rgba(255,255,255,.95)';g.beginPath();g.roundRect(X,Y,w,h,14);g.fill();g.restore();
  g.textAlign='left';g.fillStyle=MUTE;g.font=`700 ${fsK}px Bitter, Georgia, serif`;ls(3);g.fillText(kicker,X+padX,Y+9+fsK);ls(0);g.fillStyle=INK;g.font=`600 ${fsN}px Bitter, Georgia, serif`;g.fillText(nm,X+padX,Y+h-11);return {x:X,y:Y,w,h};};
 const logoChip=(im,brand,x,y,h,o={})=>{g.save();const sq=im&&im.width/im.height<1.6,padX=sq?10:14,ih=sq?h-4:h-16;let w;
  if(im){w=Math.min(im.width*ih/im.height,o.maxW||200)+2*padX;}else{g.font=`700 ${Math.round(ih*.5)}px "Playfair Display", Georgia, serif`;w=Math.min(g.measureText(brand).width,(o.maxW||200))+2*padX;}
  const X=o.right?x-w:x;shadow('rgba(40,20,30,.15)',8,2);g.fillStyle='rgba(255,255,255,.95)';g.beginPath();g.roundRect(X,y,w,h,h/2);g.fill();noShadow();
  if(im)fit(im,X+padX,y+8,w-2*padX,ih);else{g.fillStyle=INK;g.textAlign='center';g.fillText(clip(brand,w-2*padX),X+w/2,y+h/2+ih*.18);}g.restore();return w;};
 const logoRow=(ims,brands,cy,h,maxTot)=>{const items=ims.map((im,i)=>{if(im){const hh=im.width/im.height<1.6?h*1.45:h;return {im,hh,w:Math.min(im.width*hh/im.height,210)};}g.font=`700 ${Math.round(h*.42)}px "Playfair Display", Georgia, serif`;return {t:brands[i],w:g.measureText(brands[i]).width};});
  const gap=36;const tot=items.reduce((a,b)=>a+b.w,0)+gap*(items.length-1);const k=Math.min(1,maxTot/tot);let x=(W-tot*k)/2;
  items.forEach(it=>{if(it.im){const w=it.w*k,hh=Math.min(it.hh,w*it.im.height/it.im.width);g.drawImage(it.im,x,cy-hh/2,w,hh);}else{g.fillStyle='#5b4e66';g.textAlign='left';g.font=`700 ${Math.round(h*.42*k)}px "Playfair Display", Georgia, serif`;g.fillText(it.t,x,cy+h*.15);}x+=(it.w+gap)*k;});};
 /* racks with a short colour label under each one; labels get their own line so they never sit on a rack */
 const labels=rp.map(rackLabel);
 const racks=(x,y,w,h,o={})=>{const n=rks.length;if(!n)return;const fs=o.fs||21,lh=fs+12;g.save();
  const wide=rks.every(r=>r&&r.width/r.height>=2.4);
  const lab=(t,cx,ly,mw)=>{g.save();noShadow();g.textAlign='center';g.fillStyle=INK;g.font=`600 ${fs}px Bitter, Georgia, serif`;g.fillText(clip(t,mw),cx,ly);g.restore();};
  if(wide&&!o.cols){const rg=10,rowH=Math.min(o.maxRow||110,(h-n*lh-rg*(n-1))/n),tot=n*(rowH+lh)+rg*(n-1);let yy=y+(h-tot)/2;
   rks.forEach((im,i)=>{shadow('rgba(50,25,35,.2)',8,4);const b=fit(im,x,yy,w,rowH)||{x,y:yy,w,h:rowH};lab(labels[i],x+w/2,yy+rowH+fs+4,w);yy+=rowH+lh+rg;});}
  else{const cg=22,cw=(w-cg*(n-1))/n,ih=h-lh;rks.forEach((im,i)=>{shadow('rgba(50,25,35,.2)',8,4);fit(im,x+i*(cw+cg),y,cw,ih);lab(labels[i],x+i*(cw+cg)+cw/2,y+ih+fs+6,cw);});}
  g.restore();};
 const tc=(()=>{const h=s.tc||'#d6247f';let r=parseInt(h.slice(1,3),16)/255,gg=parseInt(h.slice(3,5),16)/255,b=parseInt(h.slice(5,7),16)/255;const mx=Math.max(r,gg,b),mn=Math.min(r,gg,b);let H2=0,S2=0,L=(mx+mn)/2;
  if(mx!==mn){const d=mx-mn;S2=L>.5?d/(2-mx-mn):d/(mx+mn);H2=mx===r?(gg-b)/d+(gg<b?6:0):mx===gg?(b-r)/d+2:(r-gg)/d+4;H2/=6;}return `hsl(${Math.round(H2*360)},${Math.round(Math.min(1,Math.max(S2,.38))*100)}%,${Math.round(Math.min(L,.5)*100)}%)`;})();
 const mName=M[S.fav].n.replace(/\s*(Neoprene|Leatherette)?\s*Mahjong Mat$/i,'').trim();
 // frame
 g.fillStyle=CREAM;g.fillRect(0,0,W,H);g.strokeStyle='#ebcdd8';g.lineWidth=3;g.beginPath();g.roundRect(16,16,W-32,H-32,28);g.stroke();
 // header: our wordmark, set name in the set's colour, mat line
 let y=40;if(ours){const wm=48,w=Math.min(ours.width*wm/ours.height,W*.5);g.drawImage(ours,(W-w)/2,y,w,wm);}y+=48+22;
 {const nm=s.name.toUpperCase();let fs=W>1040?104:98;g.textAlign='center';g.font=`${fs}px Caprasimo, Georgia, serif`;while(g.measureText(nm).width>W-120&&fs>48){fs-=4;g.font=`${fs}px Caprasimo, Georgia, serif`;}
  y+=fs*.82;g.fillStyle='rgba(255,255,255,.9)';g.fillText(nm,W/2+4,y+4);g.fillStyle=tc;g.fillText(nm,W/2,y);y+=44;g.fillStyle='#4a3d58';g.font='italic 500 32px "Playfair Display", Georgia, serif';g.fillText(clip(`tiles on the ${mName} mat`,W-120),W/2,y);}
 // footer: slim navy bar, code for partner pieces, website
 const fh=62,fy=H-fh-30;{const x=40,w=W-80;g.fillStyle=NAVY;g.beginPath();g.roundRect(x,fy,w,fh,fh/2);g.fill();const t=allPartner()?'Use code MAHJMATCH to save 10%':'Swipe for your own match',t2='mahjmatchmaker.com';
  g.font='700 27px Bitter, Georgia, serif';const w1=g.measureText(t).width;g.font='600 22px Bitter, Georgia, serif';const w2=g.measureText(t2).width;const gap=34;let sx=W/2-(w1+gap+w2)/2;
  g.textAlign='left';g.fillStyle='#fff';g.font='700 27px Bitter, Georgia, serif';g.fillText(t,sx,fy+fh/2+9);g.fillStyle='rgba(255,255,255,.45)';g.fillRect(sx+w1+gap/2-1,fy+fh*.28,2,fh*.44);g.fillStyle='#ffd3e1';g.font='600 22px Bitter, Georgia, serif';g.fillText(t2,sx+w1+gap,fy+fh/2+8);}
 const pin=!fb;
 if(S.view==='stack'){ // Mood board: stacked close-ups (tiles / mat / racks)
  const top=y+26,bot=fy-22,x=36,w=W-72,gap=14,avail=bot-top-2*gap;const hT=avail*.3,hM=avail*.4,hR=avail-hT-hM;
  card(x,top,w,hT,22);cover(tile,x,top,w,hT,22,1.05,.5,.45);pill(x+16,top+hT-14,'TILES',s.name,{up:true,maxW:w*.55});logoChip(tl,tb,x+w-16,top+16,52,{right:true});
  const my=top+hT+gap;card(x,my,w,hM,22);if(mat){g.save();g.beginPath();g.roundRect(x,my,w,hM,22);g.clip();const k=w*1.06/mat.width;const dw=mat.width*k,dh=mat.height*k;g.drawImage(mat,x+(w-dw)/2,my+(hM-dh)*.3,dw,dh);g.restore();}
  pill(x+16,my+hM-14,'MAT',mName,{up:true,maxW:w*.6});logoChip(ml,mb,x+w-16,my+16,52,{right:true});
  const ry=my+hM+gap;card(x,ry,w,hR,22);
  // logos for the rack brands sit along the bottom-right; racks take the rest of the band
  let lx=x+w-16,lwTot=0;const lch=46;rl.forEach((im,i)=>{const ww=logoChip(im,rb[i],lx,ry+hR-14-lch,lch,{right:true,maxW:150});lx-=ww+10;lwTot+=ww+10;});
  racks(x+28,ry+16,w-56,hR-32-lch-6,{fs:20,maxRow:96});
 }else if(S.view==='shop'){ // Showcase: full mat + tile close-up, racks laid out wide underneath
  const top=y+28,bot=fy-22,x=36,w=W-72,gap=14;const lw=Math.round(w*.6),rw=w-lw-gap,sq=pin?(bot-top)*.6:Math.min(lw,(bot-top)*.64);
  card(x,top,lw,sq,24);g.save();shadow('rgba(60,30,40,.22)',16,8);fit(mat,x+16,top+16,lw-32,sq-32);g.restore();
  pill(x+14,top+sq-14,'MAT',mName,{up:true,maxW:lw-170,fsN:21,fsK:12});logoChip(ml,mb,x+lw-14,top+14,50,{right:true,maxW:140});
  const rx=x+lw+gap;cover(tile,rx,top,rw,sq,24,1.12,.5,.45);pill(rx+14,top+sq-14,'TILES',s.name,{up:true,maxW:rw-28,fsN:21,fsK:12});logoChip(tl,tb,rx+rw-14,top+14,50,{right:true,maxW:150});
  const ry=top+sq+gap,rh=bot-ry;card(x,ry,w,rh,24);const lch=46;let lx=x+w-14;rl.forEach((im,i)=>{lx-=logoChip(im,rb[i],lx,ry+rh-14-lch,lch,{right:true,maxW:150})+10;});
  racks(x+30,ry+16,w-60,rh-32-lch-6,{fs:20,maxRow:110});
 }else{ // Love triangle: hero mat, big tile pile out right, racks out left
  const logoH=44,ly=fy-22-logoH/2,top=y+28,bot=ly-logoH/2-22,availH=bot-top;
  const ms=Math.min(W*(pin?.8:.74),availH*.86),r0=Math.min(W*.2,ms*.3),mx=(W-ms)/2,my=top+Math.max(0,(availH-(ms+r0*.8))/2);
  g.save();shadow('rgba(60,30,40,.25)',26,12);const mbx=fit(mat,mx,my,ms,ms)||{x:mx,y:my,w:ms,h:ms};g.restore();
  const r=Math.min(W*.2,ms*.3),cx=Math.min(W-34-r,mbx.x+mbx.w+r*.28),cy=Math.min(mbx.y+mbx.h-r*.25,bot-r-6);
  if(tile){g.save();shadow('rgba(40,20,30,.32)',24,10);g.fillStyle=CREAM;g.beginPath();g.arc(cx,cy,r+10,0,Math.PI*2);g.fill();g.restore();g.save();g.beginPath();g.arc(cx,cy,r,0,Math.PI*2);g.clip();const k=Math.max(2*r/tile.width,2*r/tile.height)*1.08;g.drawImage(tile,cx-tile.width*k/2,cy-tile.height*k/2,tile.width*k,tile.height*k);g.restore();}
  // racks card: each rack a row with its colour name under it
  const n=Math.max(1,rks.length),rw=W*.33,rowH=Math.min(64,rw*.19),lfs=19,lh=lfs+10,rg=8,pad=14,tot=n*(rowH+lh)+(n-1)*rg,cw=rw+2*pad,ch=tot+2*pad;
  const rx=34,ry=Math.min(mbx.y+mbx.h-ch*.55,bot-ch-6);g.save();shadow('rgba(40,20,30,.22)',18,7);g.fillStyle='rgba(255,255,255,.97)';g.beginPath();g.roundRect(rx,ry,cw,ch,20);g.fill();g.restore();
  racks(rx+pad,ry+pad,rw,tot,{fs:lfs,maxRow:rowH});
  pill(mbx.x+14,mbx.y+14,'MAT',mName,{maxW:mbx.w*.6,fsN:20,fsK:12});pill(cx+r*.15,cy-r-6,'TILES',s.name,{up:true,right:true,maxW:r*2,fsN:20,fsK:12});
  const B=[...new Set([tb,mb,...rb])],IM={};IM[tb]=tl;IM[mb]=ml;rb.forEach((b,i)=>IM[b]=rl[i]);
  const ly2=pin?Math.min(ly,Math.max(cy+r,ry+ch)+70):ly;logoRow(B.map(b=>IM[b]),B,ly2,logoH,W-180);
 }
 try{cardURL=cv.toDataURL('image/jpeg',.92);}catch(e){cardURL='';}
 const p=$('prev');if(p&&job===cardJob)p.innerHTML=cardURL?`<img src="${cardURL}" alt="Your ${esc(s.name)} match card">`:'<div class="ld">Couldn’t draw the card here.</div>';}
