"""FYM v98 (Version 1.2) match card rack layout (docs/MATCH-INBOX.md, Tiffany Oct 26 6:19pm + 7:20pm, Main's partner-graphics
rule, ANSWERS 7:22pm): on the Mood board ('tri') card the racks sat too high on the mat (covered the Heirloom Fire + Fortune
horse), far apart, and every rack was drawn at a different size (Bespoke's 4-rack stack photos came out as small lumps).
Now, in every format (Story / Post / Pin):
- racks sit LOW: the block ends just above the brand line (bottom = bot+8), rows tight (12px + label);
- EQUAL LENGTH: every rack is drawn at the same width rw = W*.40;
- stack-photo racks (Bespoke) are drawn BIG (up to W*.26 tall) instead of shrinking into the row height;
- x = max(48, mat left - 8.5% W): hanging a little off the LEFT of the mat with breathing room (Main 7:22pm correction).
The Close up ('stack') card keeps racks in their own band below the mat. Idempotent. Gate [91]. Usage: v98_card.py <build>"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read(); n = 0
old = ("const lch=56,n=Math.max(1,rkt.length),rw=Math.max(W*.34,Math.min(W*.5,mbx.x+mbx.w*.6-30)),rh=Math.min(bot-top-lch-30,Math.max(2*r+40,n*170)),rx=30,ry=Math.max(top+110,Math.min(cy-rh/2+48,bot-rh-lch-10));\n"
       "  racks(rx,ry,rw,rh,{fs:STORY?23:19,maxRow:rh,rows:true,back:true,below:true});")
new = ("const lch=56,rw=W*.40,rx=Math.max(48,mbx.x-W*.085);/*v98 racks low equal*/\n"
       "  racks(rx,top+110,rw,bot-top-110,{fs:STORY?23:19,rows:true,back:true,below:true,eq:true,stk:W*.26,bottom:bot+8});")
if '/*v98 racks low equal*/' not in h:
    assert h.count(old) == 1, h.count(old); h = h.replace(old, new); n += 1
o2 = "  if(rows){const rg=12,rowH=Math.min(o.maxRow||110,(h-n*lh-rg*(n-1))/n),tot=n*(rowH+lh)+rg*(n-1);let yy=y+(h-tot)/2;"
n2 = ("  if(rows&&o.eq){/*v98 equal-length racks*/const rg=12,a=rkt.map(im=>im?im.height/im.width:.15);let hs=a.map(v=>Math.min(w*v,o.stk||w*.6));"
      "const room=h-n*lh-rg*(n-1),sum=hs.reduce((s,v)=>s+v,0);if(sum>room)hs=hs.map(v=>v*room/sum);const tot=hs.reduce((s,v)=>s+v,0)+n*lh+rg*(n-1);"
      "let yy=o.bottom!=null?Math.max(y,o.bottom-tot):y+(h-tot)/2;rkt.forEach((im,i)=>{const bw=Math.min(w,hs[i]/a[i]);const b=draw(im,i,x,yy,bw,hs[i]);"
      "lab(labels[i],x,b.y+b.h+10,w,i);yy+=hs[i]+lh+rg;});}\n  else " + o2.lstrip())
if '/*v98 equal-length racks*/' not in h:
    assert h.count(o2) == 1, h.count(o2); h = h.replace(o2, n2); n += 1
open(P, 'w').write(h); print('v98 card rack layout', n)
