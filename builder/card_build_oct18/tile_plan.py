"""Decide per tile set where the card's HD tile comes from, to keep the artifact under its size budget:
 'full'  = the set's own full photo (T.full, already published) shows the same framing as the approved pile and is >= 900px -> no new bytes
 'chunk' = our HD crop (hd_tiles) is needed (embedded in hd/t*.json, capped)
 'pile'  = nothing better than the bundled pile."""
import json,sys,os
import numpy as np
from PIL import Image
sys.argv=['x','__none__']
import hd_tiles as H
s=open(H.BUILD+'/index.html').read();i=s.index('const D=')+8;j=s.index('\n',i);D=json.loads(s[i:j].rstrip()[:-1])
# bundles may have changed (b14): reload IMG from the build too
import re,glob
for f in [H.BUILD+'/b13v1.js',H.BUILD+'/b14v1.js']:
    t=open(f).read()
    for m in re.finditer(r'"([A-Za-z0-9_:.-]{6,60})"\s*:\s*"(data:image/[^"]+)"',t):H.IMG[m.group(1)]=m.group(2)
rep=json.load(open(H.SP+'/hd_tiles/report.json'))
plan={};c={'full':0,'chunk':0,'pile':0}
for k,t in D['tiles'].items():
    q=H.dec(H.IMG[t['pile']]) if t.get('pile') in H.IMG else None
    fp=H.fullpath(t['full']) if t.get('full') else None
    choice='pile'
    if q is not None and fp:
        f=Image.open(fp).convert('RGB')
        if min(f.size)>=900 and abs(f.size[0]/f.size[1]-q.size[0]/q.size[1])<0.03 and H.sim(f.resize(q.size),q)>0.97:choice='full'
    if choice=='pile' and rep.get(k,{}).get('hd'):
        hs=rep[k]['size']
        fs=Image.open(fp).size if fp else (0,0)
        choice='chunk' if min(hs)>max(min(q.size) if q else 0,0)*1.25 else 'pile'
    plan[k]={'c':choice,'full':t.get('full')};c[choice]+=1
json.dump(plan,open(H.SP+'/hd_tiles/plan.json','w'),indent=1);print(c)
