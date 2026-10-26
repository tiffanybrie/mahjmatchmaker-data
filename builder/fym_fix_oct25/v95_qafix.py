"""FYM v95 QA fixes (QA v95 report, Oct 26):
 (1) Close up (stack) card: 'Photo coming soon' sets get their own band drawn to fit (name + PHOTO COMING SOON + maker all
     inside the tiles band, no TILES pill on top of the name).
 (2) Every card pill (TILES / MAT / RACKS): long names shrink the font first, then wrap to 2 lines, before any '…'.
     Mood board TILES label is narrower (r*1.5) so a long set name wraps instead of running across the mat.
 (3) Etsy mat photos: done in config/fym-etsy-shopmy-oct26.json (v95_etsy.py reads it): Savannah Soiree hidden ->
     Questionable; Kristen, Julia, Gigi, Green Christmas Watercolor, Lemon Lime Floral use the flat mat-only listing photo.
Gate [77]. Idempotent. Usage: python3 v95_qafix.py <build_dir>"""
import sys, os, io, json, base64, hashlib
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()

# ---- (2) pill: shrink then wrap -------------------------------------------------------------------------------
OLD_PILL = """const pill=(x,y,kicker,name,o={})=>{const fsK=o.fsK||13,fsN=o.fsN||21,padX=15,h=fsN+fsK+22;
  g.font=`700 ${fsK}px Bitter, Georgia, serif`;ls(3);const wk=g.measureText(kicker).width;ls(0);g.font=`600 ${fsN}px Bitter, Georgia, serif`;const nm=clip(name,(o.maxW||600)-2*padX);const wn=g.measureText(nm).width;
  const w=Math.max(wk,wn)+2*padX,X=o.right?x-w:x,Y=o.up?y-h:y;g.save();shadow('rgba(40,20,30,.18)',10,3);g.fillStyle='rgba(255,255,255,.95)';g.beginPath();g.roundRect(X,Y,w,h,14);g.fill();g.restore();
  g.textAlign='left';g.fillStyle=MUTE;g.font=`700 ${fsK}px Bitter, Georgia, serif`;ls(3);g.fillText(kicker,X+padX,Y+9+fsK);ls(0);g.fillStyle=INK;g.font=`600 ${fsN}px Bitter, Georgia, serif`;g.fillText(nm,X+padX,Y+h-11);return {x:X,y:Y,w,h};};"""
NEW_PILL = """const pill=(x,y,kicker,name,o={})=>{/*v95 pill fit*/const fsK=o.fsK||13,padX=15,mw=(o.maxW||600)-2*padX;let fsN=o.fsN||21;const FN=n=>{g.font=`600 ${n}px Bitter, Georgia, serif`;};
  g.font=`700 ${fsK}px Bitter, Georgia, serif`;ls(3);const wk=g.measureText(kicker).width;ls(0);FN(fsN);const f0=fsN;while(g.measureText(name).width>mw&&fsN>Math.max(14,f0*.78)){fsN-=1;FN(fsN);}
  let L=[name];if(g.measureText(name).width>mw){const ws=String(name).split(' ');if(ws.length>1){let bi=1,bs=1e9;for(let k=1;k<ws.length;k++){const sc=Math.max(g.measureText(ws.slice(0,k).join(' ')).width,g.measureText(ws.slice(k).join(' ')).width);if(sc<bs){bs=sc;bi=k;}}L=[ws.slice(0,bi).join(' '),ws.slice(bi).join(' ')];}L=L.map(l=>clip(l,mw));}
  const lh=fsN*1.18,h=fsK+22+fsN+(L.length-1)*lh,wn=Math.max(...L.map(l=>g.measureText(l).width));
  const w=Math.max(wk,wn)+2*padX,X=o.right?x-w:x,Y=o.up?y-h:y;g.save();shadow('rgba(40,20,30,.18)',10,3);g.fillStyle='rgba(255,255,255,.95)';g.beginPath();g.roundRect(X,Y,w,h,14);g.fill();g.restore();
  g.textAlign='left';g.fillStyle=MUTE;g.font=`700 ${fsK}px Bitter, Georgia, serif`;ls(3);g.fillText(kicker,X+padX,Y+9+fsK);ls(0);g.fillStyle=INK;FN(fsN);L.forEach((l,i)=>g.fillText(l,X+padX,Y+h-11-(L.length-1-i)*lh));return {x:X,y:Y,w,h};};"""

# ---- (1) Close up soon band ----------------------------------------------------------------------------------
OLD_STACK = "card(x,top,w,hT,22);cover(tile,x,top,w,hT,22,1.05,...(T[s.tile].bf||[.5,.45]));pill(x+16,top+hT-14,'TILES',s.name,{up:true,maxW:w*.55});logoChip(tl,tb,x+w-16,top+16,66,{right:true,maxW:240});"
NEW_STACK = ("card(x,top,w,hT,22);if(T[s.tile].soon){/*v95 soon band*/soonBand(x,top,w,hT);}else{cover(tile,x,top,w,hT,22,1.05,...(T[s.tile].bf||[.5,.45]));"
             "pill(x+16,top+hT-14,'TILES',s.name,{up:true,maxW:w*.55});}logoChip(tl,tb,x+w-16,top+16,66,{right:true,maxW:240});")
SOONBAND = """ const soonBand=(x,y,w,hh)=>{g.save();g.fillStyle='#f6e9df';g.beginPath();g.roundRect(x,y,w,hh,22);g.fill();g.strokeStyle='#ecd5df';g.lineWidth=3;g.setLineDash([10,8]);g.beginPath();g.roundRect(x+10,y+10,w-20,hh-20,18);g.stroke();g.setLineDash([]);
  const tw=w-2*Math.min(270,w*.27),nm=String(s.name),F=n=>{g.font=`${n}px Caprasimo, Georgia, serif`;};const lfs=Math.max(15,Math.min(24,hh*.075)),mfs=Math.max(15,Math.min(24,hh*.075));
  let fs=Math.min(64,hh*.3),L=[nm];F(fs);const bal=()=>{const ws=nm.split(' ');let bi=1,bs=1e9;for(let k=1;k<ws.length;k++){const sc=Math.max(g.measureText(ws.slice(0,k).join(' ')).width,g.measureText(ws.slice(k).join(' ')).width);if(sc<bs){bs=sc;bi=k;}}return ws.length>1?[ws.slice(0,bi).join(' '),ws.slice(bi).join(' ')]:[nm];};
  const room=()=>hh-28-lfs*1.9-mfs*1.7;while(g.measureText(nm).width>tw&&fs>40){fs-=2;F(fs);}if(g.measureText(nm).width>tw){L=bal();}
  while((Math.max(...L.map(l=>g.measureText(l).width))>tw||L.length*fs*1.06>room())&&fs>18){fs-=2;F(fs);}
  const tot=L.length*fs*1.06+lfs*1.9+mfs*1.7;let yy=y+(hh-tot)/2+fs*.86;g.textAlign='center';g.fillStyle='#c8325f';L.forEach((l,i)=>{F(fs);g.fillText(l,x+w/2,yy+i*fs*1.06);});yy+=(L.length-1)*fs*1.06+lfs*1.75;
  g.fillStyle='#7a6a85';g.font=`700 ${lfs}px Bitter, Georgia, serif`;ls(2);g.fillText('PHOTO COMING SOON',x+w/2,yy);ls(0);yy+=mfs*1.55;g.fillStyle='#054689';g.font=`${mfs}px Bitter, Georgia, serif`;g.fillText(clip(String(s.maker||''),tw),x+w/2,yy);g.restore();};
"""
ANCH_SOON = " const logoChip=(im,brand,x,y,h,o={})=>{"
OLD_TRI = "pill(cx+r*.15,cy-r-6,'TILES',s.name,{up:true,right:true,maxW:r*2,fsN:20,fsK:12});"
NEW_TRI = "pill(cx+r*.15,cy-r-6,'TILES',s.name,{up:true,right:true,maxW:r*1.5,fsN:20,fsK:12});"

if '/*v95 pill fit*/' not in h:
    for a, b in ((OLD_PILL, NEW_PILL), (OLD_STACK, NEW_STACK), (OLD_TRI, NEW_TRI)):
        assert h.count(a) == 1, a[:70]; h = h.replace(a, b)
    assert h.count(ANCH_SOON) == 1; h = h.replace(ANCH_SOON, SOONBAND + ANCH_SOON)
    print('qafix: soon band + pill fit')
else:
    print('qafix: card already')

open(P, 'w').write(h)
