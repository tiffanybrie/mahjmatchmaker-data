"""FYM v80 match card (Tiffany Oct 23 3:59pm, 8:46pm, 8:48pm).
 - Top, two versions to compare: A (default) = flame heart over the big no-tagline wordmark; B (#ctop=b) = no top logo,
   our seal at the right end of the tile-set title line.
 - Bottom: brand line "flame heart  Matched with Find Your Mat-ch(TM) . mahjmatchmaker.com" above the navy code bar
   ("Use code MAHJMATCH to save" alone in the bar). Nothing else touches the bar.
 - Mood board: no white rack box. Racks sit on the mat at left, stacked, as big as the space allows (about the tile
   circle's height); a rack photo that isn't a clean cutout keeps its own small white backing. Brand logos on each piece
   (opposite corner from its label); the old bottom logo row is gone.
 - Every rack image is trimmed to its content first, so small product shots (Anders Ruff tortoise) aren't tiny.
 - Rack labels = the same left-aligned pills as MAT / TILES ("RACKS" + colour), on both views.
 - Close up: bigger brand logos; logo chips never let a logo spill out of its pill.
Needs b24v1.js (IMG.wmn = no-tagline wordmark, IMG.seal = seal). Usage: python3 v80_card.py <build_dir> <repo>"""
import sys, io, base64, json
from PIL import Image
B, REPO = sys.argv[1], sys.argv[2]; P = B + '/index.html'; h = open(P).read()
def rep(old, new, n=1):
    global h
    c = h.count(old); assert c == n, f'expected {n} x {old[:90]!r}, found {c}'; h = h.replace(old, new)
def between(a, b, new):
    global h
    i = h.index(a); j = h.index(b, i); assert h.count(a) == 1; h = h[:i] + new + h[j:]

# brand images for the card
def du(path, maxw):
    im = Image.open(path).convert('RGBA'); im.thumbnail((maxw, maxw)); b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
imgs = {'wmn': du(REPO + '/assets/brand/mahjmatchmaker-wordmark-notag.png', 900),
        'seal': du(REPO + '/assets/brand/seal/seal-full-pastel-navy-flame.png', 320)}
open(B + '/b24v1.js', 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(imgs) + ');')
if 'b24v1.js' not in h:
    rep('<script src="b23v1.js"></script>', '<script src="b23v1.js"></script><script src="b24v1.js"></script>')

rep("const cv=document.createElement('canvas');",
    "const [wmn,seal]=await Promise.all([lk(IMG.wmn),lk(IMG.seal)]);if(job!==cardJob)return;\n const cv=document.createElement('canvas');")

# logo chip: centred inside its pill, never spilling out
rep("const sq=im&&im.width/im.height<1.6,padX=sq?10:14,ih=sq?h-4:h-16;", "const sq=im&&im.width/im.height<1.6,padX=sq?12:16,ih=sq?h-12:h-18;")
rep("if(im)fit(im,X+padX,y+8,w-2*padX,ih);", "if(im)fit(im,X+padX,y+(h-ih)/2,w-2*padX,ih);")

# racks: trimmed images, left pills
between('/* racks with a short colour label', 'const tc=(()=>', r'''/* v80: racks trimmed to their content, labelled with the same left pills as MAT / TILES */
 const labels=rp.map(rackLabel);
 const trim=(im,norot)=>{if(!im)return im;try{const k=Math.min(1,400/Math.max(im.width,im.height)),w=Math.max(1,Math.round(im.width*k)),hh=Math.max(1,Math.round(im.height*k)),c=document.createElement('canvas');c.width=w;c.height=hh;const x=c.getContext('2d');x.drawImage(im,0,0,w,hh);const d=x.getImageData(0,0,w,hh).data;let x0=w,y0=hh,x1=-1,y1=-1;
  if(!norot){/* a rack shot on the diagonal (e.g. Anders Ruff tortoise) is turned flat so it fills the space */let n=0,mx=0,my=0;const on=i=>d[i+3]>24&&Math.min(d[i],d[i+1],d[i+2])<232;for(let yy=0;yy<hh;yy+=2)for(let xx=0;xx<w;xx+=2){if(on((yy*w+xx)*4)){n++;mx+=xx;my+=yy;}}
   if(n>50){mx/=n;my/=n;let sxx=0,syy=0,sxy=0;for(let yy=0;yy<hh;yy+=2)for(let xx=0;xx<w;xx+=2){if(on((yy*w+xx)*4)){const a=xx-mx,b=yy-my;sxx+=a*a;syy+=b*b;sxy+=a*b;}}const ang=.5*Math.atan2(2*sxy,sxx-syy),tr=sxx+syy,dt=Math.sqrt(Math.max(0,tr*tr/4-(sxx*syy-sxy*sxy))),el=(tr/2+dt)/Math.max(1e-6,tr/2-dt);
    if(el>4&&Math.abs(ang)>.2&&Math.abs(ang)<1.37){const cs=Math.abs(Math.cos(ang)),sn=Math.abs(Math.sin(ang)),c2=document.createElement('canvas');c2.width=Math.round(im.width*cs+im.height*sn);c2.height=Math.round(im.width*sn+im.height*cs);const x2=c2.getContext('2d');x2.fillStyle='rgba(0,0,0,0)';x2.translate(c2.width/2,c2.height/2);x2.rotate(-ang);x2.drawImage(im,-im.width/2,-im.height/2);return trim(c2,true);}}}
  for(let yy=0;yy<hh;yy++)for(let xx=0;xx<w;xx++){const i=(yy*w+xx)*4;if(d[i+3]>24&&Math.min(d[i],d[i+1],d[i+2])<232){if(xx<x0)x0=xx;if(xx>x1)x1=xx;if(yy<y0)y0=yy;if(yy>y1)y1=yy;}}
  if(x1<0)return im;const p=Math.round(Math.max(x1-x0,y1-y0)*.04);x0=Math.max(0,x0-p);y0=Math.max(0,y0-p);x1=Math.min(w-1,x1+p);y1=Math.min(hh-1,y1+p);if((x1-x0+1)*(y1-y0+1)>w*hh*.92)return im;
  const o=document.createElement('canvas');o.width=Math.max(1,Math.round((x1-x0+1)/k));o.height=Math.max(1,Math.round((y1-y0+1)/k));o.getContext('2d').drawImage(im,x0/k,y0/k,o.width,o.height,0,0,o.width,o.height);return o;}catch(e){return im;}};
 const rkt=rks.map(trim);
 const racks=(x,y,w,h,o={})=>{const n=rkt.length;if(!n)return;const fs=o.fs||21,fk=Math.round(fs*.6),ph=fs+fk+22,lh=Math.round(ph*.55)+6;g.save();
  const draw=(im,i,bx,by,bw,bh)=>{if(!im)return {x:bx,y:by,w:bw,h:bh};const cut=R[rp[i]]&&R[rp[i]].c;
   if(!cut&&o.back){const k=Math.min((bw-16)/im.width,(bh-16)/im.height),dw=im.width*k,dh=im.height*k,dx=bx+(bw-dw)/2,dy=by+(bh-dh)/2;g.save();shadow('rgba(50,25,35,.18)',10,4);g.fillStyle='#fff';g.beginPath();g.roundRect(dx-8,dy-8,dw+16,dh+16,14);g.fill();g.restore();g.drawImage(im,dx,dy,dw,dh);return {x:dx-8,y:dy-8,w:dw+16,h:dh+16};}
   g.save();shadow('rgba(50,25,35,.2)',8,4);const b=fit(im,bx,by,bw,bh)||{x:bx,y:by,w:bw,h:bh};g.restore();return b;};
  const lab=(t,lx,ty,mw)=>pill(lx,ty,'RACKS',t,{maxW:mw,fsN:fs,fsK:fk});
  const rows=o.rows||n===1||rkt.every(r=>r&&r.width/r.height>=2.4);
  if(rows){const rg=12,rowH=Math.min(o.maxRow||110,(h-n*lh-rg*(n-1))/n),tot=n*(rowH+lh)+rg*(n-1);let yy=y+(h-tot)/2;
   rkt.forEach((im,i)=>{const b=draw(im,i,x,yy,w,rowH);lab(labels[i],x,b.y+b.h-Math.round(ph*.45),w);yy+=rowH+lh+rg;});}
  else{const cg=22,cw=(w-cg*(n-1))/n,ih=h-lh;rkt.forEach((im,i)=>{draw(im,i,x+i*(cw+cg),y,cw,ih);lab(labels[i],x+i*(cw+cg),y+ih-Math.round(ph*.45),cw);});}
  g.restore();};
 ''')

# header: version A (flame heart over the big wordmark) or B (seal at the end of the title line)
between('const STORY=H/W>1.6;', '// footer: slim navy bar', r'''const STORY=H/W>1.6,CT=S.ctop||(/ctop=b/i.test(location.hash)?'B':'A');
let y=STORY?200:40;
 if(CT==='A'){const ih=STORY?96:72,wh=STORY?56:46;if(icon){const w=icon.width*ih/icon.height;g.drawImage(icon,(W-w)/2,y,w,ih);}y+=ih+10;const wm=wmn||ours;if(wm){const w=Math.min(wm.width*wh/wm.height,W*.7);g.drawImage(wm,(W-w)/2,y,w,w*wm.height/wm.width);}y+=wh+14;}
 else y+=12;
 {const nm=s.name.toUpperCase(),SW=CT==='B'?150:0;let fs=W>1040?104:98;g.textAlign='center';g.font=`${fs}px Caprasimo, Georgia, serif`;while(g.measureText(nm).width>W-120-2*SW&&fs>48){fs-=4;g.font=`${fs}px Caprasimo, Georgia, serif`;}
  y+=fs*.82;g.fillStyle='rgba(255,255,255,.9)';g.fillText(nm,W/2+4,y+4);g.fillStyle=tc;g.fillText(nm,W/2,y);
  if(CT==='B'&&(seal||icon)){const sm=seal||icon,sh=Math.min(136,fs*1.3),sw=sm.width*sh/sm.height;g.drawImage(sm,W-44-sw,y-fs*.36-sh/2,sw,sh);}
  y+=44;g.fillStyle='#4a3d58';g.font='italic 500 32px "Playfair Display", Georgia, serif';g.fillText(clip(`tiles on the ${mName} mat`,W-120),W/2,y);}
 ''')

# footer: brand line + code bar
between('// footer: slim navy bar', 'const pin=!fb;', r'''// footer (v80): brand line, then the navy bar with the code only
 const fh=60,fy=H-fh-(STORY?210:30),fby=fy-64;
 {const x=40,w=W-80;g.fillStyle=NAVY;g.beginPath();g.roundRect(x,fy,w,fh,fh/2);g.fill();const t=codeLine()||'Swipe for your own match';g.textAlign='center';g.fillStyle='#fff';g.font='700 30px Bitter, Georgia, serif';g.fillText(clip(t,w-40),W/2,fy+fh/2+10);
  const a='Matched with Find Your Mat-ch™',b='mahjmatchmaker.com',ih=42,cy=fby+30;g.font='700 27px Bitter, Georgia, serif';const wa=g.measureText(a).width;g.font='600 25px Bitter, Georgia, serif';const wb=g.measureText(b).width;
  const iw=icon?icon.width*ih/icon.height:0,tot=iw+14+wa+34+wb;let sx=(W-tot)/2;if(icon)g.drawImage(icon,sx,cy-ih/2-4,iw,ih);sx+=iw+14;
  g.textAlign='left';g.fillStyle=NAVY;g.font='700 27px Bitter, Georgia, serif';g.fillText(a,sx,cy+9);sx+=wa+12;g.fillStyle=PINK;g.fillText('·',sx,cy+9);sx+=22;g.font='600 25px Bitter, Georgia, serif';g.fillText(b,sx,cy+8);}
 ''')
rep('bot=fy-22', 'bot=fby-10', 2)

# close up: bigger logos + bigger racks
rep('racks(x+28,ry+16,w-56,hR-32-lch-6,{fs:20,maxRow:96});','racks(x+28,ry+16,w-56,hR-32,{fs:20,maxRow:230});{let lx2=x+w-16;rl.forEach((im,i)=>{lx2-=logoChip(im,rb[i],lx2,ry+hR-14-lch,lch,{right:true,maxW:210})+10;});}')
rep("logoChip(tl,tb,x+w-16,top+16,52,{right:true});", "logoChip(tl,tb,x+w-16,top+16,66,{right:true,maxW:240});")
rep("logoChip(ml,mb,x+w-16,my+16,52,{right:true});", "logoChip(ml,mb,x+w-16,my+16,66,{right:true,maxW:240});")
rep('const lch=46;', 'const lch=60;', 2)
rep('lch,{right:true,maxW:150}', 'lch,{right:true,maxW:210}', 2)

# mood board
rep("  const logoH=44,ly=fy-22-logoH/2,top=y+28,bot=ly-logoH/2-22,availH=bot-top;\n  const ms=STORY?Math.min(W*.86,availH*.7):Math.min(W*(pin?.8:.74),availH*.86)",
    "  const top=y+24,bot=fby-12,availH=bot-top;\n  const ms=STORY?Math.min(W*.86,availH*.72):Math.min(W*(pin?.8:.76),availH*.9)")
i = h.index('// racks card: each rack a row'); j = h.index(' }\n ', i)
h = h[:i] + r'''// v80: racks on the mat at left, stacked, no white box; brand logos on each piece
  const lch=56,n=Math.max(1,rkt.length),rw=Math.max(W*.34,Math.min(W*.5,mbx.x+mbx.w*.6-30)),rh=Math.min(bot-top-lch-30,Math.max(2*r+40,n*170)),rx=30,ry=Math.max(top+70,Math.min(cy-rh/2,bot-rh-lch-10));
  racks(rx,ry,rw,rh,{fs:19,maxRow:rh,rows:true,back:true});
  {let lx=rx;rl.forEach((im,i)=>{lx+=logoChip(im,rb[i],lx,ry+rh+8,lch,{maxW:210})+10;});}
  pill(mbx.x+14,mbx.y+14,'MAT',mName,{maxW:mbx.w*.6,fsN:20,fsK:12});logoChip(ml,mb,mbx.x+mbx.w-14,mbx.y+14,60,{right:true,maxW:230});
  pill(cx+r*.15,cy-r-6,'TILES',s.name,{up:true,right:true,maxW:r*2,fsN:20,fsK:12});logoChip(tl,tb,cx-r*.8,Math.min(cy+r-30,fby-66),58,{maxW:220});
''' + h[j:]
open(P, 'w').write(h); print('v80 card applied')
