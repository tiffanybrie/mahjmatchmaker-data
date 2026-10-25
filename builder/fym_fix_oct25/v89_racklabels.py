"""FYM v89 (Tiffany Oct 25 16:37): on the Mood board match card the racks sat too high and their white RACKS label pills
overlapped the bottom of the rack photo. Mood board (the app's 'tri' view; 'stack' is labelled Close up) only: labels sit just BELOW each rack (whole rack visible) and the racks
come down. Close up keeps the overlap she's fine with.
Usage: python3 v89_racklabels.py <build_dir>  (in place)"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (a[:90], h.count(a)); h = h.replace(a, b)
# label band height: full pill + gap when below
rep("const fs=o.fs||21,fk=Math.round(fs*.6),ph=fs+fk+22,lh=Math.round(ph*.55)+6;",
    "const fs=o.fs||21,fk=Math.round(fs*.6),ph=fs+fk+22,lh=o.below?ph+10:Math.round(ph*.55)+6;")
# rows layout
rep("rkt.forEach((im,i)=>{const b=draw(im,i,x,yy,w,rowH);lab(labels[i],x,b.y+b.h-Math.round(ph*.45),w,i);yy+=rowH+lh+rg;});}",
    "rkt.forEach((im,i)=>{const b=draw(im,i,x,yy,w,rowH);lab(labels[i],x,o.below?b.y+b.h+10:b.y+b.h-Math.round(ph*.45),w,i);yy+=rowH+lh+rg;});}")
# columns layout
rep("else{const cg=22,cw=(w-cg*(n-1))/n,ih=h-lh;rkt.forEach((im,i)=>{draw(im,i,x+i*(cw+cg),y,cw,ih);lab(labels[i],x+i*(cw+cg),y+ih-Math.round(ph*.45),cw,i);});}",
    "else{const cg=22,cw=(w-cg*(n-1))/n,ih=h-lh;"
    "if(o.below){/* v89: racks share one height box, labels in a row under them, the group centred in the band */"
    "const DH=Math.max(...rkt.map(im=>im?im.height*Math.min(cw/im.width,ih/im.height):0),1),y0=y+(h-DH-lh)/2;"
    "rkt.forEach((im,i)=>{draw(im,i,x+i*(cw+cg),y0,cw,DH);lab(labels[i],x+i*(cw+cg),y0+DH+10,cw,i);});}"
    "else rkt.forEach((im,i)=>{draw(im,i,x+i*(cw+cg),y,cw,ih);lab(labels[i],x+i*(cw+cg),y+ih-Math.round(ph*.45),cw,i);});}")
# mood board call
# Mood board = the 'tri' view (VIEWS: tri='Mood board', stack='Close up'): labels below + racks lower. Close up keeps its overlap.
rep("rx=30,ry=Math.max(top+70,Math.min(cy-rh/2,bot-rh-lch-10));\n  racks(rx,ry,rw,rh,{fs:STORY?23:19,maxRow:rh,rows:true,back:true});",
    "rx=30,ry=Math.max(top+110,Math.min(cy-rh/2+48,bot-rh-lch-10));\n  racks(rx,ry,rw,rh,{fs:STORY?23:19,maxRow:rh,rows:true,back:true,below:true});")
open(P, 'w').write(h); print('ok')
