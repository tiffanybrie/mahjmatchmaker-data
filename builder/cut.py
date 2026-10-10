import json,os
from rembg import remove,new_session
from PIL import Image
s=new_session('u2netp')
F=json.load(open('fetched.json'));
for pid,r in F.items():
    if 'file' not in r or 'cut' in r: continue
    out='/tmp/mb/cut/'+pid.replace('/','__')+'.png'
    im=Image.open(r['file']).convert('RGB'); im.thumbnail((700,700))
    o=remove(im,session=s)
    bb=o.getbbox()
    if bb: o=o.crop(bb)
    o.save(out); r['cut']=out
json.dump(F,open('fetched.json','w'),indent=1)
print('ok',sum(1 for r in F.values() if 'cut' in r))
