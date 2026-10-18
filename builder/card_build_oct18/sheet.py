import sys,glob
from PIL import Image
fs=sys.argv[2:];out=sys.argv[1];cols=min(3,len(fs));w=600
ims=[Image.open(f) for f in fs];ims=[i.resize((w,int(w*i.height/i.width))) for i in ims];h=max(i.height for i in ims)
rows=(len(ims)+cols-1)//cols;S=Image.new('RGB',(cols*w+(cols-1)*10,rows*h+(rows-1)*10),'white')
for k,i in enumerate(ims):S.paste(i,((k%cols)*(w+10),(k//cols)*(h+10)))
S.save(out,quality=85)
