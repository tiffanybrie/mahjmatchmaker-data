"""Color wheel seal, full-wheel versions (Oct 19). Real flame-heart (assets/brand/flame-heart.png) upscaled via
smoothed masks, placed on a fully filled color wheel. Variants: pastel / true wheel x white flame / navy flame."""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
R='/home/claude/mahjmatchmaker-data/'
src=Image.open(R+'assets/brand/flame-heart.png').convert('RGBA'); a=np.asarray(src).astype(int)
alpha=a[...,3]; r,g,b=a[...,0],a[...,1],a[...,2]
pinkm=((r>180)&(g<160)&(alpha>40)); flamem=(alpha>40)  # flame = whole silhouette; heart drawn on top
def up(mask,S):
    m=Image.fromarray((mask*255).astype('uint8')).resize((S,int(S*src.height/src.width)),Image.LANCZOS).filter(ImageFilter.GaussianBlur(S/400))
    return m.point(lambda v:255 if v>127 else 0).filter(ImageFilter.GaussianBlur(1))
def logo(S,flame_col,heart_col):
    fm,hm=up(flamem,S),up(pinkm,S); im=Image.new('RGBA',fm.size,(0,0,0,0))
    im.paste(Image.new('RGBA',fm.size,flame_col),(0,0),fm); im.paste(Image.new('RGBA',fm.size,heart_col),(0,0),hm); return im
def wheel(S,kind):
    y,x=np.mgrid[0:S,0:S]; cx=cy=(S-1)/2; dx,dy=x-cx,y-cy; rr=np.hypot(dx,dy)/(S/2)
    ang=(np.degrees(np.arctan2(dx,-dy))%360)/360  # 0 at top, clockwise
    import colorsys
    if kind=='true':
        h=ang; sat=np.clip(rr,0,1)**0.9*0.95+0.05; val=np.ones_like(rr)*0.98
    else:
        h=ang; sat=np.clip(0.16+0.26*rr,0,1); val=np.ones_like(rr)*0.98
    hsv=np.stack([h,sat,val],-1); rgb=np.zeros_like(hsv)
    i=(h*6).astype(int)%6; f=h*6-np.floor(h*6); p=val*(1-sat); q=val*(1-f*sat); t=val*(1-(1-f)*sat)
    for k,(R_,G_,B_) in enumerate([(val,t,p),(q,val,p),(p,val,t),(p,q,val),(t,p,val),(val,p,q)]):
        m=i==k; rgb[...,0][m]=R_[m]; rgb[...,1][m]=G_[m]; rgb[...,2][m]=B_[m]
    im=Image.fromarray((rgb*255).astype('uint8')).convert('RGBA')
    mask=Image.new('L',(S*4,S*4),0); ImageDraw.Draw(mask).ellipse((0,0,S*4-1,S*4-1),fill=255); im.putalpha(mask.resize((S,S),Image.LANCZOS)); return im
def seal(kind,flame,S=900):
    w=wheel(S,kind); col={'white':(255,255,255,255),'navy':(5,70,137,255)}[flame]
    lg=logo(int(S*0.50),col,(245,108,140,255))
    P=40; sh=Image.new('RGBA',(lg.width+2*P,lg.height+2*P),(0,0,0,0)); m=Image.new('L',sh.size,0); m.paste(lg.getchannel('A'),(P,P))
    sh.paste(Image.new('RGBA',sh.size,(20,30,60,70)),(0,0),m); sh=sh.filter(ImageFilter.GaussianBlur(12))
    x=(S-lg.width)//2; y=(S-lg.height)//2+int(S*0.01)
    w.alpha_composite(sh,(x+4-P,y+10-P)); w.alpha_composite(lg,(x,y)); return w
if __name__=='__main__':
    out=R+'assets/brand/seal/'; import os; os.makedirs(out,exist_ok=True)
    combos=[('pastel','white'),('pastel','navy'),('true','white'),('true','navy')]
    tiles=[]
    for k,f in combos:
        s=seal(k,f); s.save(out+f'seal-full-{k}-{f}-flame.png'); tiles.append(s)
    T=420; sheet=Image.new('RGB',(4*T+5*40,T+150),(246,233,223)); d=ImageDraw.Draw(sheet)
    ft=ImageFont.truetype(R+'scripts/social/tileprofile/fonts/Caprasimo.ttf',30)
    names=['1 - Pastel wheel, white flame','2 - Pastel wheel, navy flame','3 - Bright wheel, white flame','4 - Bright wheel, navy flame']
    for i,(s,n) in enumerate(zip(tiles,names)):
        x=40+i*(T+40); sheet.paste(s.resize((T,T),Image.LANCZOS),(x,40),s.resize((T,T),Image.LANCZOS))
        d.text((x+T/2,T+80),n,font=ft,fill=(5,70,137),anchor='mm')
    sheet.save(R+'assets/brand/seal/seal-full-wheel-options.png'); print('ok')
