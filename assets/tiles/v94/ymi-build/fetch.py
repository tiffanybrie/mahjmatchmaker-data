import json,urllib.request,io,os,concurrent.futures as cf
from PIL import Image,ImageDraw
H="tc-at001-a tc-at002-a us-at402-b tc-at007-a us-at028-a us-at020-b hb-at002-a us-at031-a fx-at002-a tc-at005-a tc-at006-a fx-at001-a fx-at003-a tc-at003-a tc-at004-a us-at024-a us-at021-c us-at007-a us-at022-a tc-af010-a tc-af009-a fx-am021-a us-af033-a us-af032-a us-am001-h us-am008-a fx-am010-a fx-am018-a fx-am009-a us-am011-a fx-am027-a fx-am012-a fx-am022-a fx-am019-a fx-am014-a fx-am016-a us-am009-a us-af035-a fx-am015-a fx-am020-a fx-am011-a fx-am024-a".split()
meta={}
def get(h):
    d=json.load(urllib.request.urlopen(f'https://www.ymimports.com/products/{h}.json'))['product']
    os.makedirs(f'img/{h}',exist_ok=True);ims=[]
    for n,i in enumerate(d['images']):
        p=f'img/{h}/{n:02d}.jpg'
        if not os.path.exists(p):
            Image.open(io.BytesIO(urllib.request.urlopen(i['src']).read())).convert('RGB').save(p,quality=93)
        ims.append(p)
    return h,d['title'],ims
with cf.ThreadPoolExecutor(8) as ex:
    for h,t,ims in ex.map(get,H):
        meta[h]={'title':t,'imgs':ims}
        th=[Image.open(p) for p in ims];
        S=Image.new('RGB',(250*min(8,len(th)),250*((len(th)+7)//8)),'white');dr=ImageDraw.Draw(S)
        for n,im in enumerate(th):
            im=im.copy();im.thumbnail((245,245));S.paste(im,((n%8)*250,(n//8)*250));dr.text(((n%8)*250+3,(n//8)*250+3),f'{n} {Image.open(ims[n]).size}',fill='red')
        S.save(f'sheet_{h}.jpg',quality=80)
json.dump(meta,open('meta.json','w'),indent=1)
print({h:len(m['imgs']) for h,m in meta.items()})
