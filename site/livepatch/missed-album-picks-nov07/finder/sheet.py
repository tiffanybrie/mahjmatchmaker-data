import sys,json
from PIL import Image,ImageDraw,ImageFont
def sheet(items,out,cols=8,w=260,h=300):
    rows=(len(items)+cols-1)//cols; S=Image.new('RGB',(cols*w,rows*h),'white'); d=ImageDraw.Draw(S)
    try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
    except: f=None
    for i,(p,lab) in enumerate(items):
        x,y=(i%cols)*w,(i//cols)*h
        try:
            im=Image.open(p).convert('RGB'); im.thumbnail((w-8,h-40)); S.paste(im,(x+4,y+4))
        except Exception as e: d.text((x+4,y+4),'ERR',fill='red')
        d.text((x+4,y+h-34),lab[:38],fill='black',font=f); d.text((x+4,y+h-18),lab[38:76],fill='black',font=f)
    S.save(out,quality=80)
if __name__=='__main__':
    M=json.load(open('matimg.json')); D8=json.load(open('D118.json'))['mats']
    it=[(v['file'],f"{i} {D8.get(k,{}).get('n',k)} | {D8.get(k,{}).get('bn','')}") for i,(k,v) in enumerate(sorted(M.items()))]
    for j in range(0,len(it),48): sheet(it[j:j+48],f'mats_{j//48}.jpg')
