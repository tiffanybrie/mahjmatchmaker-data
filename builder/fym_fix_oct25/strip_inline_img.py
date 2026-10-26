import re,json,sys
P=sys.argv[1];h=open(P).read()
pat=re.compile(r'<script>window\.IMG=Object\.assign\(window\.IMG\|\|\{\},(\{.*?\})\);</script>',re.S)
blocks=[(m.start(),m.end(),json.loads(m.group(1))) for m in pat.finditer(h)]
rest=pat.sub('',h)
last={}
for i,(a,b,d) in enumerate(blocks):
  for k in d: last[k]=i
keep=[]; dead=dup=0
for i,(a,b,d) in enumerate(blocks):
  nd={}
  for k,v in d.items():
    if last[k]!=i: dup+=1; continue
    if k not in rest: dead+=1; continue
    nd[k]=v
  keep.append(nd)
out=[];pos=0
for (a,b,d),nd in zip(blocks,keep):
  out.append(h[pos:a])
  if nd: out.append('<script>window.IMG=Object.assign(window.IMG||{},'+json.dumps(nd,separators=(',',':'))+');</script>')
  pos=b
out.append(h[pos:]);h2=''.join(out)
print('blocks',len(blocks),'dup',dup,'dead',dead,len(h),'->',len(h2))
if len(sys.argv)>2: open(P,'w').write(h2)
