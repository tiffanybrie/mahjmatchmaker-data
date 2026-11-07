# FYM v116 r2 ARTIFACT copy (independent QA agent, Nov 6). Usage: python3 artifact116_r2.py <r1 site index> <r2 site index> <live r1 artifact index> <out index> --slim
# r2 artifact copy = live r1 artifact (fymb116) + (r2 website D - r1 website D) field deltas + Mahj Pit rack IMG script.
import json,sys,re
r1s,r2s,art,out=sys.argv[1:5]
def LD(h):
    i=h.index('const D=')+8; D,e=json.JSONDecoder().raw_decode(h[i:]); return D,i,i+e
A=open(r1s).read();B=open(r2s).read();F=open(art).read()
DA,_,_=LD(A);DB,_,_=LD(B);DF,fi,fe=LD(F)
assert DA['order']==DB['order']==DF['order']
AH={k for k,o in DF['mats'].items() if o.get('ahid')}
LINK={'u','u0','u_dead','u_plain','dc','pa','oos','alt','altu'}
n=0
for top in DA:
  a,b=DA[top],DB[top]
  if a==b: continue
  if isinstance(a,dict):
    for k in set(a)|set(b):
      if a.get(k)==b.get(k): continue
      if k not in a: DF[top][k]=b[k]; n+=1; continue
      if k not in b: DF[top].pop(k,None); n+=1; continue
      if isinstance(a[k],dict) and isinstance(b[k],dict):
        for f in set(a[k])|set(b[k]):
          if a[k].get(f)==b[k].get(f): continue
          if top=='mats' and k in AH and f not in LINK: continue
          if f in b[k]: DF[top][k][f]=b[k][f]
          else: DF[top][k].pop(f,None)
          n+=1
      else: DF[top][k]=b[k]; n+=1
  elif top=='sets':
    assert len(a)==len(b)==len(DF['sets'])
    for x,y,z in zip(a,b,DF['sets']):
      assert x.get('slug')==z.get('slug')
      for f in set(x)|set(y):
        if x.get(f)!=y.get(f):
          if f in y: z[f]=y[f]
          else: z.pop(f,None)
          n+=1
  else: DF[top]=b; n+=1
DS={DF['order'].index(k) for k in AH}
for s in DF['sets']:
  for fld in ('rank','cr'):
    if fld in s: s[fld]=[j for j in s[fld] if j not in DS]
h=F[:fi]+json.dumps(DF,ensure_ascii=False,separators=(',',':'))+F[fe:]
img=re.search(r'<script>window\.IMG=Object\.assign\(window\.IMG\|\|\{\},\{"rk116mpwhitebeech":[^<]*</script>',B).group(0)
tag='<script src="b24v1.js">'; assert h.count(tag)==1; h=h.replace(tag,img+tag)
open(out,'w').write(h); print('changes',n,'size',len(h.encode()))
# --- size cap (artifact version total <= 256 MiB): drop build-only link metadata (u_plain/u_dead: 0 refs in app code)
#     and the shop links of the 325 artifact-hidden slim mats (ahid: hid=true, never rendered in the artifact)
if len(sys.argv)>5 and sys.argv[5]=='--slim':
  h=open(out).read(); D,i0,i1=LD(h); n1=n2=0
  for g in ('mats','racks','tiles'):
    for o in D[g].values():
      for f in ('u_plain','u_dead'):
        if f in o: o.pop(f); n1+=1
  for k,o in D['mats'].items():
    if o.get('ahid') and o.get('hid'):
      for f in ('u','u0'):
        if f in o: o.pop(f); n2+=1
  h=h[:i0]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[i1:]
  open(out,'w').write(h); print('slim: dropped',n1,'u_plain/u_dead,',n2,'ahid links; size',len(h.encode()))
