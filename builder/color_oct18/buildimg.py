import json,base64,io,hashlib,os
from PIL import Image,ImageOps
SP='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
rows=json.load(open('rows_album.json'))
SWAP=["Rackin' Rudolph",'Holly Jolly (Rudolph Red)','Nivalee (Glacier Blue)','Tinselle (Emerald Green)','Tinselle (Ruby Red)','Après Ski Club','Brownstone Bloom','Plum Panda','Hummingbird','Sunday','Papaya Spritz','Petalée']
src={r[0]:r[2] for r in rows}
os.makedirs(SP+'fymaudit/t13',exist_ok=True)
imgs={};out={}
for k,n in enumerate(SWAP):
    im0=ImageOps.exif_transpose(Image.open(src[n])).convert('RGBA');im=Image.new('RGB',im0.size,'white');im.paste(im0,mask=im0.split()[3])
    w,h=im.size;m=min(w,h);sq=im.crop(((w-m)//2,(h-m)//2,(w-m)//2+m,(h-m)//2+m))
    p=sq.resize((360,360),Image.LANCZOS);b=io.BytesIO();p.save(b,'WEBP',quality=80)
    d='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
    hsh=hashlib.md5(d.encode()).hexdigest()[:10];imgs[hsh]=d
    f=im.copy();f.thumbnail((900,900),Image.LANCZOS);f.save(SP+f'fymaudit/t13/{k}.jpg','JPEG',quality=85)
    out[n]={'pile':hsh,'full':f't13/{k}.jpg','src':src[n]}
open(SP+'fymaudit/b10v1.js','w').write('window.IMG=Object.assign(window.IMG||{},'+json.dumps(imgs)+');')
json.dump(out,open('swap.json','w'),indent=1,ensure_ascii=False)
print(len(imgs),os.path.getsize(SP+'fymaudit/b10v1.js'))
