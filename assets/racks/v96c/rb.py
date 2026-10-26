import sys,os,numpy as np
from rembg import new_session, remove
from PIL import Image
from scipy import ndimage
exec(open('/home/claude/mahjmatchmaker-data/assets/racks/v96c/make.py').read().split("if __name__")[0])
s=new_session('isnet-general-use')
os.makedirs('out3',exist_ok=True)
for name,(src,how,opt) in JOBS.items():
    im=Image.open(src).convert('RGB')
    if im.width>1400: im=im.resize((1400,round(im.height*1400/im.width)),Image.LANCZOS)
    mask=np.asarray(remove(im,session=s,only_mask=True)).astype(float)/255
    a=np.asarray(im).astype(float)/255
    m,v=pick(mask>.5,opt.get('mode','len'))
    al=np.where(ndimage.binary_dilation(m,iterations=2),mask,0)
    if opt.get('clear'): al=np.maximum(al*np.where(m,1,0), 0)  # keep model alpha
    o=Image.fromarray(np.dstack([(a*255).astype(np.uint8),(al*255).astype(np.uint8)]),'RGBA')
    if opt.get('level',True):
        ang=np.degrees(np.arctan2(v[1],v[0])); ang=ang-180 if ang>90 else ang+180 if ang<-90 else ang
        if abs(ang)>.4: o=o.rotate(ang,resample=Image.BICUBIC,expand=True)
    o=o.crop(o.getbbox())
    if o.width>1000:o=o.resize((1000,round(o.height*1000/o.width)),Image.LANCZOS)
    o.save(f'out3/{name}.webp',quality=90);print(name,o.size)
