import sys,os,numpy as np
from rembg import new_session, remove
from PIL import Image
from scipy import ndimage
exec(open('/home/claude/mahjmatchmaker-data/assets/racks/v96c/make.py').read().split("if __name__")[0])
s=new_session('isnet-general-use')
J={'bam-clear-scallop':'cur/15.png','bam-white-acrylic':'cur/14.png','mfm-clear':'cur/07.png','missmahjong-clear-scallop':'miss3.png','mahjongrow-white':'cur/11.png','mfm-bright-white':'cur/08.png','virora-white-magnetic':'cur/10.png','register-ivory-oyster':'cur/12.png','bespoke-crystal-clear':'cur/13.png','tdt-dove-white':'tdt_full.jpg'}
os.makedirs('out4',exist_ok=True)
for name,src in J.items():
    im=Image.open(src).convert('RGB')
    if im.width>1400: im=im.resize((1400,round(im.height*1400/im.width)),Image.LANCZOS)
    a0=np.asarray(im); edge=np.concatenate([a0[:4].reshape(-1,3),a0[-4:].reshape(-1,3)]); bg=tuple(int(x) for x in np.median(edge,0))
    S=max(im.size); sq=Image.new('RGB',(S,S),bg); ox,oy=(S-im.width)//2,(S-im.height)//2; sq.paste(im,(ox,oy))
    mk=np.asarray(remove(sq,session=s,only_mask=True)).astype(float)/255
    mask=mk[oy:oy+im.height,ox:ox+im.width]; a=a0.astype(float)/255
    fg=mask>.5
    if name=='tdt-dove-white': fg=ndimage.binary_erosion(fg,iterations=6)
    m,v=pick(fg,'len' if name in('missmahjong-clear-scallop','tdt-dove-white') else 'area')
    if name=='tdt-dove-white': m=ndimage.binary_dilation(m,iterations=8)&(mask>.5)
    al=np.where(ndimage.binary_dilation(m,iterations=2),mask,0)
    o=Image.fromarray(np.dstack([(a*255).astype(np.uint8),(al*255).astype(np.uint8)]),'RGBA')
    if name in('missmahjong-clear-scallop','tdt-dove-white'):
        ang=np.degrees(np.arctan2(v[1],v[0])); ang=ang-180 if ang>90 else ang+180 if ang<-90 else ang
        o=o.rotate(ang,resample=Image.BICUBIC,expand=True)
    o=o.crop(o.getbbox())
    if o.width>1000:o=o.resize((1000,round(o.height*1000/o.width)),Image.LANCZOS)
    o.save(f'out4/{name}.webp',quality=90);print(name,o.size)
