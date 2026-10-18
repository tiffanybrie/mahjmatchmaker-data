"""HD mats for the match card: for mats Tiffany matched (on any album list) whose best FYM image is under 1000px,
locate that image in the brand's Shopify product photos (2000px) with SIFT and warp-crop it (cap 1800).
Usage: python3 hd_mats.py [name filter]. Writes scratchpad/hd_mats/."""
import json,os,sys,glob,re,base64,io,hashlib
from PIL import Image
flt=sys.argv[1].lower() if len(sys.argv)>1 else ''
sys.argv=['x','__none__']
import hd_tiles as H
O=H.SP+'/hd_mats';os.makedirs(O,exist_ok=True)
MC={}
for f in glob.glob(H.BUILD+'/mc/*.json')+glob.glob(H.REPO+'builder/card_redesign_oct18/serve/mc/*.json'):
    try:d=json.load(open(f))
    except Exception:continue
    for k,v in d.items():
        if k not in MC:MC[k]=v
used=set(m[0] for s in H.D['sets'] for m in s.get('m',[]))
rep=json.load(open(O+'/report.json')) if os.path.exists(O+'/report.json') else {}
for mid in sorted(used):
    m=H.D['mats'].get(mid)
    if not m:continue
    if flt and flt not in m['n'].lower():continue
    if mid in rep and not flt:continue
    src=MC.get(m.get('f')) or H.IMG.get(m.get('th'))
    if not src:rep[mid]={'n':m['n'],'err':'no img'};continue
    q=H.dec(src)
    if min(q.size)>=1000:rep[mid]={'n':m['n'],'ok':list(q.size)};continue
    best=None
    for s2,c in H.shopify(m.get('u','')):
        if max(c.size)<=max(q.size)*1.2:continue
        L=H.locate(q,c)
        if L and (not best or L[0]>best[0]):best=(*L,s2,c)
    if not best or best[0]<1.3:rep[mid]={'n':m['n'],'size':list(q.size),'hd':None,'best':round(best[0],2) if best else None};print(m['n'],'no upgrade',q.size);continue
    o=H.warp(best[4],best[1],q,best[0],cap=1800);sm=H.sim(o,q)
    if sm<0.85:rep[mid]={'n':m['n'],'size':list(q.size),'hd':None,'sim':round(sm,3)};print(m['n'],'low sim',sm);continue
    qa=Image.open(io.BytesIO(base64.b64decode(src.split(',',1)[1])))
    if qa.mode in('RGBA','LA','P'):
        al=qa.convert('RGBA').split()[3]
        if al.getextrema()[0]<250:o=o.convert('RGBA');o.putalpha(al.resize(o.size,Image.LANCZOS))
    fn=hashlib.md5(mid.encode()).hexdigest()[:12]+'.webp';o.save(O+'/'+fn,'WEBP',quality=88)
    rep[mid]={'n':m['n'],'size':list(q.size),'hd':fn,'hdsize':list(o.size),'src':best[3][:120],'sim':round(sm,3)};print(m['n'],q.size,'->',o.size,round(sm,3))
    json.dump(rep,open(O+'/report.json','w'),indent=1)
json.dump(rep,open(O+'/report.json','w'),indent=1)
