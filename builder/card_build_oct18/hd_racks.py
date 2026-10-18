"""HD rack images for the FYM match card (Oct 18).
Priority: (1) the album-card rack cutout in assets/racks/card (1400px, matched by normalized name),
(2) Bird & Bamboo colours re-rendered from bb-blank.png with the colour hex (builder/bbrack.recolor),
(3) the brand's Shopify product image located by SIFT (same method as hd_tiles.py), else none.
Writes scratchpad/hd_racks/<hash>.webp + report.json."""
import json,re,os,sys,io,glob,hashlib,unicodedata
import numpy as np
from PIL import Image
sys.argv=[sys.argv[0],'__none__']  # reuse hd_tiles helpers without running its loop over tiles
import hd_tiles as H
sys.path.insert(0,'/home/claude/mahjmatchmaker-data/builder');from bbrack import recolor
REPO=H.REPO;OUT=H.SP+'/hd_racks';os.makedirs(OUT,exist_ok=True)
D=H.D;norm=H.norm
CARD={norm(os.path.splitext(os.path.basename(f))[0]):f for f in glob.glob(REPO+'assets/racks/card/*.png')}
BB={x['name']:x['hex'] for x in json.load(open(REPO+'builder/bbracks.json'))}
blank=Image.open(REPO+'assets/racks/card/bb-blank.png').convert('RGBA')
def trim(im):
    a=np.asarray(im.convert('RGBA'));al=a[...,3];m=(al>20)&(a[...,:3].min(2)<245)
    ys,xs=np.where(m)
    return im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)) if len(xs) else im
rep={}
for rid,r in D['racks'].items():
    src=None;out=None
    nn=norm(r['n']).replace('tortoise','tortoise')
    cands=[k for k in CARD if k==nn or k==norm(r['n'].replace('(','').replace(')',''))]
    if not cands:
        # tolerate small naming differences: card name contained in rack name or vice versa (same brand)
        cands=[k for k in CARD if len(k)>12 and (k in nn or nn in k) and norm(r['bn'])[:6] in k]
    if cands:
        src='card:'+os.path.basename(CARD[cands[0]]);out=Image.open(CARD[cands[0]]).convert('RGBA')
    elif rid.startswith('bb:') and rid[3:] in BB:
        src='bb-render:'+rid[3:];out=recolor(blank,BB[rid[3:]])
    else:
        q=H.dec(H.IMG[r['im']]) if r.get('im') in H.IMG else None
        if q is not None:
            best=None
            for s2,c in H.shopify(r.get('u','')):
                if max(c.size)<=max(q.size)*1.2:continue
                L=H.locate(q,c)
                if L and (not best or L[0]>best[0]):best=(*L,s2,c)
            if best and best[0]>=1.3:
                o=H.warp(best[4],best[1],q,best[0],cap=1400)
                if H.sim(o,q)>0.85:src=best[3];out=o
    if out is None:rep[rid]={'n':r['n'],'hd':None};continue
    out=trim(out)
    if max(out.size)>1400:out.thumbnail((1400,1400),Image.LANCZOS)
    fn=hashlib.md5(rid.encode()).hexdigest()[:12]+'.webp';out.save(os.path.join(OUT,fn),'WEBP',quality=90)
    rep[rid]={'n':r['n'],'hd':fn,'size':list(out.size),'src':src}
json.dump(rep,open(OUT+'/report.json','w'),indent=1)
c=sum(1 for v in rep.values() if v['hd']);print('racks',len(rep),'hd',c)
import collections;print(collections.Counter((v.get('src') or 'none').split(':')[0] for v in rep.values()))
