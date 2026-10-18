// Match card redesign mocks (Oct 18). Runs inside the FYM build page (uses D, T, M, R, S, IMG, LG, pile, matFull, rackSrc, shortR, allPartner, herRacks, rackPool).
(function(){
const PINK='#c8325f',NAVY='#054689',INK='#2a2036',MUTE='#7a6a85',CREAM='#f7ece3';
const EXTRA_LOGOS={'Sunday Mahjong':'logo_sunday.png'};
const lk=src=>new Promise(r=>{if(!src)return r(null);const i=new Image();i.crossOrigin='anonymous';i.onload=()=>r(i);i.onerror=()=>r(null);i.src=src;});
function hexToHsl(h){let r=parseInt(h.slice(1,3),16)/255,g=parseInt(h.slice(3,5),16)/255,b=parseInt(h.slice(5,7),16)/255;const mx=Math.max(r,g,b),mn=Math.min(r,g,b);let H=0,S=0,L=(mx+mn)/2;if(mx!==mn){const d=mx-mn;S=L>.5?d/(2-mx-mn):d/(mx+mn);H=mx===r?(g-b)/d+(g<b?6:0):mx===g?(b-r)/d+2:(r-g)/d+4;H/=6;}return [H,S,L];}
function hsl(h,s,l){return `hsl(${Math.round(h*360)},${Math.round(s*100)}%,${Math.round(l*100)}%)`;}
// Title colour = the set's own colour, deepened until it reads on cream (Sunday's pale back -> mustard).
function titleColor(tc){const [h,s,l]=hexToHsl(tc||'#d6247f');return hsl(h,Math.min(1,Math.max(s,.38)),Math.min(l,.5));}
// Trim white/transparent margins off a product photo, and turn tall rack shots on their side.
function trimRack(im){if(!im)return null;const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const x=c.getContext('2d');x.drawImage(im,0,0);let px;try{px=x.getImageData(0,0,c.width,c.height).data;}catch(e){return im;}
  let x0=c.width,y0=c.height,x1=0,y1=0;for(let y=0;y<c.height;y+=2)for(let X=0;X<c.width;X+=2){const i=(y*c.width+X)*4;const a=px[i+3],m=Math.min(px[i],px[i+1],px[i+2]);if(a>40&&m<236){if(X<x0)x0=X;if(X>x1)x1=X;if(y<y0)y0=y;if(y>y1)y1=y;}}
  if(x1<=x0||y1<=y0)return im;const w=x1-x0+1,h=y1-y0+1;const o=document.createElement('canvas');const rot=h>w*1.2;o.width=rot?h:w;o.height=rot?w:h;const ox=o.getContext('2d');
  if(rot){ox.translate(o.width/2,o.height/2);ox.rotate(-Math.PI/2);ox.drawImage(c,x0,y0,w,h,-w/2,-h/2,w,h);}else ox.drawImage(c,x0,y0,w,h,0,0,w,h);return o;}
async function load(setName,matId,rackIds){
  const si=D.sets.findIndex(x=>x.name===setName);S.set=si;S.fav=matId;const s=D.sets[si];
  let rp=rackIds;if(!rp){const hr=herRacks();rp=(hr.length?hr:rackPool()).slice(0,2);}S.rpick=rp;
  const logoSrc=b=>LG(b)||EXTRA_LOGOS[b]||'';
  const [mat,tile,ours,icon,...rks]=await Promise.all([matFull(matId).then(lk),lk(pile(s)),lk(LG('ours')),lk(LG('icon')),...rp.map(r=>lk(rackSrc(r)))]);
  const tb=T[s.tile].bn,mb=M[matId].bn,rb=[...new Set(rp.map(r=>R[r].bn))];
  const [tl,ml,...rl]=await Promise.all([lk(logoSrc(tb)),lk(logoSrc(mb)),...rb.map(b=>lk(logoSrc(b)))]);
  return {s,mat,tile,ours,icon,rks:rks.map(trimRack),rp,tc:titleColor(s.tc),tb,mb,rb,tl,ml,rl,mName:M[matId].n.replace(/\s*(Neoprene|Leatherette)?\s*Mahjong Mat$/i,'').trim(),rName:rp.map(shortR).join(' + '),code:allPartner()};
}
function kit(g){
  const ls=px=>{try{g.letterSpacing=px+'px';}catch(e){}};
  const fit=(im,x,y,w,h,al)=>{if(!im)return null;const k=Math.min(w/im.width,h/im.height);const dw=im.width*k,dh=im.height*k;const dx=al==='left'?x:x+(w-dw)/2,dy=y+(h-dh)/2;g.drawImage(im,dx,dy,dw,dh);return {x:dx,y:dy,w:dw,h:dh};};
  const cover=(im,x,y,w,h,r,zoom=1,fx=.5,fy=.5)=>{if(!im)return;g.save();g.beginPath();g.roundRect(x,y,w,h,r);g.clip();const k=Math.max(w/im.width,h/im.height)*zoom;const dw=im.width*k,dh=im.height*k;g.drawImage(im,x+(w-dw)*fx,y+(h-dh)*fy,dw,dh);g.restore();};
  const shadow=(c,b,oy)=>{g.shadowColor=c;g.shadowBlur=b;g.shadowOffsetY=oy;};
  const pill=(x,y,kicker,name,opt={})=>{ // small tag on an image; returns width
    const fsK=opt.fsK||15,fsN=opt.fsN||24,padX=16,h=opt.h||(fsN+fsK+24);
    g.font=`700 ${fsK}px Bitter, Georgia, serif`;ls(3);const wk=g.measureText(kicker).width;ls(0);
    g.font=`600 ${fsN}px Bitter, Georgia, serif`;let nm=name;const maxW=opt.maxW||600;while(g.measureText(nm).width>maxW-2*padX&&nm.length>4)nm=nm.slice(0,-2).trim()+'…';const wn=g.measureText(nm).width;
    const w=Math.max(wk,wn)+2*padX;const X=opt.right?x-w:x,Y=opt.up?y-h:y;
    g.save();shadow('rgba(40,20,30,.18)',10,3);g.fillStyle='rgba(255,255,255,.95)';g.beginPath();g.roundRect(X,Y,w,h,14);g.fill();g.restore();
    g.textAlign='left';g.fillStyle=opt.kc||MUTE;g.font=`700 ${fsK}px Bitter, Georgia, serif`;ls(3);g.fillText(kicker,X+padX,Y+10+fsK);ls(0);
    g.fillStyle=INK;g.font=`600 ${fsN}px Bitter, Georgia, serif`;g.fillText(nm,X+padX,Y+h-12);return {x:X,y:Y,w,h};};
  const logoChip=(im,brand,x,y,h,opt={})=>{ // logo on a white chip; wordmark fallback
    g.save();let w;const padX=14,ih=h-16;
    if(im){w=Math.min(im.width*ih/im.height,opt.maxW||220)+2*padX;}else{g.font=`700 ${Math.round(ih*.5)}px "Playfair Display", Georgia, serif`;w=g.measureText(brand).width+2*padX;}
    const X=opt.right?x-w:x;shadow('rgba(40,20,30,.15)',8,2);g.fillStyle='rgba(255,255,255,.95)';g.beginPath();g.roundRect(X,y,w,h,h/2);g.fill();g.shadowColor='transparent';
    if(im){fit(im,X+padX,y+8,w-2*padX,ih);}else{g.fillStyle=INK;g.textAlign='center';g.fillText(brand,X+w/2,y+h/2+ih*.18);}
    g.restore();return w;};
  const logoRow=(ims,brands,cy,h,W,maxTot)=>{ // plain logos, no chips
    const items=ims.map((im,i)=>{if(im)return {im,w:Math.min(im.width*h/im.height,200)};g.font=`700 ${Math.round(h*.42)}px "Playfair Display", Georgia, serif`;return {t:brands[i],w:g.measureText(brands[i]).width};});
    const gap=36;let tot=items.reduce((a,b)=>a+b.w,0)+gap*(items.length-1);const k=Math.min(1,maxTot/tot);let x=(W-tot*k)/2;
    items.forEach(it=>{if(it.im){const w=it.w*k,hh=Math.min(h,w*it.im.height/it.im.width);g.drawImage(it.im,x,cy-hh/2,w,hh);}else{g.fillStyle='#5b4e66';g.textAlign='left';g.font=`700 ${Math.round(h*.42*k)}px "Playfair Display", Georgia, serif`;g.fillText(it.t,x,cy+h*.15);}x+=(it.w+gap)*k;});};
  return {ls,fit,cover,shadow,pill,logoChip,logoRow};
}
// Racks block: long rack shots stack as rows; if any photo isn't a long horizontal shot, use side-by-side columns so nothing shrinks to a thumbnail.
function racksBlock(g,K,rks,x,y,w,h){const n=rks.length||1;if(!rks.length)return;const wide=rks.every(r=>r&&r.width/r.height>=2.4);g.save();K.shadow('rgba(50,25,35,.2)',8,4);
  if(wide){const rg=14,rowH=Math.min(120,(h-rg*(n-1))/n),tot=rowH*n+rg*(n-1);rks.forEach((im,i)=>K.fit(im,x,y+(h-tot)/2+i*(rowH+rg),w,rowH));}
  else{const cg=24,cw=(w-cg*(n-1))/n;rks.forEach((im,i)=>K.fit(im,x+i*(cw+cg),y,cw,h));}
  g.restore();}
function header(g,K,d,W,y,o={}){
  const wm=o.wm||54;if(d.ours){const w=Math.min(d.ours.width*wm/d.ours.height,W*.5);g.drawImage(d.ours,(W-w)/2,y,w,wm);}y+=wm+(o.gap1||26);
  const nm=d.s.name.toUpperCase();let fs=o.fs||112;g.textAlign='center';g.font=`${fs}px Caprasimo, Georgia, serif`;while(g.measureText(nm).width>W-120&&fs>48){fs-=4;g.font=`${fs}px Caprasimo, Georgia, serif`;}
  y+=fs*.82;g.fillStyle='rgba(255,255,255,.9)';g.fillText(nm,W/2+4,y+4);g.fillStyle=d.tc;g.fillText(nm,W/2,y);
  y+=o.sub===false?0:44;if(o.sub!==false){g.fillStyle='#4a3d58';g.font='italic 500 32px "Playfair Display", Georgia, serif';g.fillText(`tiles on the ${d.mName} mat`,W/2,y);}
  return y;
}
function footer(g,K,d,W,H,h){ // slim navy bar: code (partners) + website
  const y=H-h-30,x=40,w=W-80;g.fillStyle=NAVY;g.beginPath();g.roundRect(x,y,w,h,h/2);g.fill();
  g.fillStyle='#fff';g.textAlign='center';
  const t=d.code?'Use code MAHJMATCH to save 10%':'Swipe for your own match';const t2='mahjmatchmaker.com';
  g.font='700 27px Bitter, Georgia, serif';const w1=g.measureText(t).width;g.font='600 22px Bitter, Georgia, serif';const w2=g.measureText(t2).width;
  const gap=34,tot=w1+gap+w2;let sx=W/2-tot/2;g.textAlign='left';g.font='700 27px Bitter, Georgia, serif';g.fillText(t,sx,y+h/2+9);
  g.fillStyle='rgba(255,255,255,.45)';g.fillRect(sx+w1+gap/2-1,y+h*.28,2,h*.44);g.fillStyle='#ffd3e1';g.font='600 22px Bitter, Georgia, serif';g.fillText(t2,sx+w1+gap,y+h/2+8);
  return y;
}
function bg(g,W,H){g.fillStyle=CREAM;g.fillRect(0,0,W,H);g.strokeStyle='#ebcdd8';g.lineWidth=3;g.beginPath();g.roundRect(16,16,W-32,H-32,28);g.stroke();}

// ---------- A: Bands (stacked close-ups: tiles / mat / racks) ----------
function drawBands(g,K,d,W,H){
  bg(g,W,H);let y=header(g,K,d,W,40,{wm:48,fs:W>1040?104:98,gap1:22});
  const fh=66,fy=footer(g,K,d,W,H,fh);
  const top=y+26,bot=fy-22,x=36,w=W-72,gap=14,avail=bot-top-2*gap;
  const n=d.rks.length||1;const hT=avail*.3,hM=avail*.4,hR=avail-hT-hM;
  // tiles
  g.save();K.shadow('rgba(50,25,35,.16)',14,5);g.fillStyle='#fff';g.beginPath();g.roundRect(x,top,w,hT,22);g.fill();g.restore();
  K.cover(d.tile,x,top,w,hT,22,1.05,.5,.45);
  K.pill(x+16,top+hT-14,'TILES',d.s.name,{up:true,maxW:w*.55});K.logoChip(d.tl,d.tb,x+w-16,top+16,52,{right:true});
  // mat close-up: middle strip of the flat mat, borders showing
  const my=top+hT+gap;g.save();K.shadow('rgba(50,25,35,.16)',14,5);g.fillStyle='#fff';g.beginPath();g.roundRect(x,my,w,hM,22);g.fill();g.restore();
  if(d.mat){g.save();g.beginPath();g.roundRect(x,my,w,hM,22);g.clip();const k=w*1.06/d.mat.width;const dw=d.mat.width*k,dh=d.mat.height*k;g.drawImage(d.mat,x+(w-dw)/2,my+(hM-dh)*.3,dw,dh);g.restore();}
  K.pill(x+16,my+hM-14,'MAT',d.mName,{up:true,maxW:w*.6});K.logoChip(d.ml,d.mb,x+w-16,my+16,52,{right:true});
  // racks: laid horizontally on a white band
  const ry=my+hM+gap;g.save();K.shadow('rgba(50,25,35,.16)',14,5);g.fillStyle='#fff';g.beginPath();g.roundRect(x,ry,w,hR,22);g.fill();g.restore();
  racksBlock(g,K,d.rks,x+28,ry+16,w-56,hR-94);
  K.pill(x+16,ry+hR-14,'RACKS',d.rName,{up:true,maxW:w*.6,fsN:22});let lx=x+w-16;d.rl.forEach((im,i)=>{lx-=K.logoChip(im,d.rb[i],lx,ry+hR-14-50,50,{right:true})+10;});
}
// ---------- B: Spread (hero mat, tiles out right, racks out left) ----------
function drawSpread(g,K,d,W,H){
  bg(g,W,H);let y=header(g,K,d,W,40,{wm:48,fs:W>1040?104:98,gap1:22});
  const fh=62,fy=footer(g,K,d,W,H,fh);const logoH=44,ly=fy-22-logoH/2;
  const top=y+28,bot=ly-logoH/2-22;const availH=bot-top;
  const pin=H/W>1.4;const ms=Math.min(W*(pin?.8:.74),availH*.86);const r0=Math.min(W*.2,ms*.3);const mx=(W-ms)/2,my=top+Math.max(0,(availH-(ms+r0*.8))/2);
  g.save();K.shadow('rgba(60,30,40,.25)',26,12);const mb=K.fit(d.mat,mx,my,ms,ms)||{x:mx,y:my,w:ms,h:ms};g.restore();
  // tiles circle: big, pushed out past the mat's lower-right corner
  const r=Math.min(W*.2,ms*.3);const cx=Math.min(W-34-r,mb.x+mb.w+r*.28),cy=Math.min(mb.y+mb.h-r*.25,bot-r-6);
  if(d.tile){g.save();K.shadow('rgba(40,20,30,.32)',24,10);g.fillStyle=CREAM;g.beginPath();g.arc(cx,cy,r+10,0,Math.PI*2);g.fill();g.restore();g.save();g.beginPath();g.arc(cx,cy,r,0,Math.PI*2);g.clip();const k=Math.max(2*r/d.tile.width,2*r/d.tile.height)*1.08;g.drawImage(d.tile,cx-d.tile.width*k/2,cy-d.tile.height*k/2,d.tile.width*k,d.tile.height*k);g.restore();}
  // racks card: out past the mat's lower-left corner
  const n=d.rks.length||1,rw=W*.34,rh=Math.min(78,rw*.2),rg=12,tot=n*rh+(n-1)*rg,pad=16,cw=rw+2*pad,ch=tot+2*pad;
  const rx=34,ry=Math.min(mb.y+mb.h-ch*.55,bot-ch-6);g.save();K.shadow('rgba(40,20,30,.22)',18,7);g.fillStyle='rgba(255,255,255,.97)';g.beginPath();g.roundRect(rx,ry,cw,ch,20);g.fill();g.restore();
  racksBlock(g,K,d.rks,rx+pad,ry+pad,rw,tot);
  // tags sit on the images
  K.pill(rx+8,ry-10,'RACKS',d.rName,{up:true,maxW:cw+30,fsN:20,fsK:12});
  K.pill(mb.x+14,mb.y+14,'MAT',d.mName,{maxW:mb.w*.6,fsN:20,fsK:12});
  K.pill(cx+r*.15,cy-r-6,'TILES',d.s.name,{up:true,right:true,maxW:r*2,fsN:20,fsK:12});
  const B=[...new Set([d.tb,d.mb,...d.rb])];const IM={};IM[d.tb]=d.tl;IM[d.mb]=d.ml;d.rb.forEach((b,i)=>IM[b]=d.rl[i]);
  const ly2=pin?Math.min(ly,Math.max(cy+r,ry+ch)+70):ly;K.logoRow(B.map(b=>IM[b]),B,ly2,logoH,W,W-180);
}
// ---------- C: Showcase (full mat + tile close-up on top, racks laid out wide below) ----------
function drawSplit(g,K,d,W,H){
  bg(g,W,H);let y=header(g,K,d,W,40,{wm:48,fs:W>1040?104:98,gap1:22});
  const fh=62,fy=footer(g,K,d,W,H,fh);const top=y+28,bot=fy-22,x=36,w=W-72,gap=14;
  const pin=H/W>1.4;const lw=Math.round(w*.6),rw=w-lw-gap,sq=pin?(bot-top)*.6:Math.min(lw,(bot-top)*.64);
  g.save();K.shadow('rgba(50,25,35,.16)',14,5);g.fillStyle='#fff';g.beginPath();g.roundRect(x,top,lw,sq,24);g.fill();g.restore();
  g.save();K.shadow('rgba(60,30,40,.22)',16,8);K.fit(d.mat,x+16,top+16,lw-32,sq-32);g.restore();
  K.pill(x+14,top+sq-14,'MAT',d.mName,{up:true,maxW:lw-170,fsN:21,fsK:12});K.logoChip(d.ml,d.mb,x+lw-14,top+14,50,{right:true,maxW:140});
  const rx=x+lw+gap;K.cover(d.tile,rx,top,rw,sq,24,1.12,.5,.45);
  K.pill(rx+14,top+sq-14,'TILES',d.s.name,{up:true,maxW:rw-28,fsN:21,fsK:12});K.logoChip(d.tl,d.tb,rx+rw-14,top+14,50,{right:true,maxW:150});
  const ry=top+sq+gap,rh=bot-ry;g.save();K.shadow('rgba(50,25,35,.16)',14,5);g.fillStyle='#fff';g.beginPath();g.roundRect(x,ry,w,rh,24);g.fill();g.restore();
  racksBlock(g,K,d.rks,x+30,ry+16,w-60,rh-94);
  K.pill(x+14,ry+rh-14,'RACKS',d.rName,{up:true,maxW:w*.6,fsN:21,fsK:12});let lx=x+w-14;d.rl.forEach((im,i)=>{lx-=K.logoChip(im,d.rb[i],lx,ry+rh-14-48,48,{right:true})+10;});
}
// ---------- Before: the current hero, for comparison ----------
window.MOCK={load,async render(dir,setName,matId,rackIds,fmt){
  try{await Promise.all(['400 100px Caprasimo','italic 500 40px "Playfair Display"','700 30px Bitter','600 26px Bitter'].map(f=>document.fonts.load(f)));}catch(e){}
  const d=await load(setName,matId,rackIds);const fb=fmt==='fb',W=fb?1080:1000,H=fb?1350:1500;
  const cv=document.createElement('canvas');cv.width=W;cv.height=H;const g=cv.getContext('2d');const K=kit(g);
  ({bands:drawBands,spread:drawSpread,split:drawSplit})[dir](g,K,d,W,H);
  return {url:cv.toDataURL('image/jpeg',.9),racks:d.rp,code:d.code,tc:d.tc};},
 async before(setName,matId,rackIds,fmt,view){await load(setName,matId,rackIds);S.fmt=fmt;S.view=view||'tri';
  let prev=document.getElementById('prev');if(!prev){prev=document.createElement('div');prev.id='prev';document.body.appendChild(prev);}
  await drawCard();return cardURL;}};
})();
