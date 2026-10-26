import json,sys
from PIL import Image,ImageDraw
M={'tc-at001-a':(3,4),'tc-at002-a':(3,4),'us-at402-b':(3,4),'tc-at007-a':(3,4),'us-at028-a':(3,4),'us-at020-b':(4,5),
'us-at031-a':(4,5),'fx-at002-a':(4,5),'tc-at005-a':(3,4),'tc-at006-a':(3,4),'fx-at001-a':(4,5),'fx-at003-a':(4,5),'tc-at003-a':(3,4),
'tc-at004-a':(3,4),'us-at024-a':(3,4),'us-at021-c':(4,5),'us-at007-a':(4,5),'us-at022-a':(4,5),'tc-af010-a':(5,6),
'tc-af009-a':(6,7),'us-af033-a':(6,7),'us-af032-a':(6,7),'us-am001-h':(6,7),'us-am008-a':(6,7),'fx-am010-a':(6,7),'fx-am018-a':(6,7),
'fx-am009-a':(6,7),'us-am011-a':(6,7),'fx-am027-a':(6,7),'fx-am012-a':(6,7),'fx-am022-a':(6,7),'fx-am019-a':(6,7),'fx-am016-a':(6,7),
'us-am009-a':(6,7),'us-af035-a':(6,7),'fx-am015-a':(6,7),'fx-am020-a':(6,7),'fx-am011-a':(6,7),'fx-am024-a':(6,7)}
FC=(880,1240,1790,2036);BC=(300,280,1215,1080)
OV=json.load(open('ov.json')) if __import__('os').path.exists('ov.json') else {}
def make(h):
    f,b=M[h];o=OV.get(h,{})
    fa=Image.open(f'img/{h}/{f:02d}.jpg').convert('RGB').crop(tuple(o.get('fc',FC))).resize((796,700),Image.LANCZOS)
    ba=Image.open(f'img/{h}/{b:02d}.jpg').convert('RGB').crop(tuple(o.get('bc',BC))).resize((796,700),Image.LANCZOS)
    c=Image.new('RGB',(1600,700),'white');c.paste(fa,(0,0));c.paste(ba,(804,0));return c
if __name__=='__main__':
    meta=json.load(open('meta.json'));hs=sys.argv[1:] or list(M)
    rows=[]
    for h in hs:
        c=make(h);c.save(f'out/{h}.jpg',quality=90)
        r=Image.new('RGB',(1000,300),'white');s=c.resize((640,280));r.paste(s,(0,18))
        cc=c.crop((450,0,1150,700)).resize((280,280));m=Image.new('L',(280,280),0);ImageDraw.Draw(m).ellipse((0,0,279,279),fill=255)
        r.paste(cc,(680,18),m);ImageDraw.Draw(r).text((2,2),h+' '+meta[h]['title'][:60],fill='black');rows.append(r)
    for k in range(0,len(rows),8):
        S=Image.new('RGB',(1000,300*len(rows[k:k+8])),'white')
        for i,r in enumerate(rows[k:k+8]):S.paste(r,(0,i*300))
        S.save(f'cs{k//8}.jpg',quality=85)
