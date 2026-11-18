from PIL import Image, ImageDraw
import numpy as np, json
R='/home/claude/mahjmatchmaker-data'; D='dl/'
SRC=[ # brand, file, weight (top earners bigger), opts
("Oh My Mahjong",D+"ohmymahjong_svg.png",1.45,{}),
("Bam Bird Boutique",D+"bambirdboutique_svg.png",1.45,{}),
("Miss Mahjong","/home/claude/mahjmatchmaker-data/assets/brand/fym-logo-src/miss-mahjong-stacked.png",1.45,{}),
("My Fair Mahjong",D+"myfairmahjong.png",1.45,{}),
("Middle & Main Mahjong",R+"/builder/logos/middlemainmahjong_0.png",1.45,{}),
("Peace Love Mahjong",D+"peacelovemahjong.png",1.0,{}),
("Mahjong Co.",R+"/builder/logos/mahjongco_0.png",1.0,{}),
("Bird & Bamboo",D+"birdbamboo.png",1.0,{}),
("Mahj Mood",D+"mahjmood.png",1.0,{"bgkey":True}),
("Virora Mahjong",R+"/assets/brand/partner-logos/virora.png",1.0,{}),
("Anders Ruff",R+"/assets/brand/partner-logos/ar.png",1.0,{}),
("Mini Mahjer",D+"minimahjer.png",1.0,{}),
("Britt Mills",D+"brittmills.png",1.0,{"recolor":(40,60,90),"clipbr":True}),
("Mahj Squad",R+"/assets/brand/partner-logos/squad.png",1.0,{}),
("Mac + Miller Mahjong",D+"macmillermahjong.png",1.0,{}),
("Hip Hip Mahjong",R+"/assets/brand/partner-logos/hiphip.png",1.0,{}),
("Charleston Mahjong Club",R+"/assets/brand/partner-logos/cmc.png",1.0,{}),
("Amanda Toppe",D+"amandatoppe.png",1.0,{}),
("Let's Be Besties",D+"letsbebesties.png",1.0,{}),
("Bam! Let's Mahjong",R+"/assets/brand/partner-logos/bam.png",1.0,{}),
("The Royal Mahjong Society",D+"theroyalmahjongsociety.png",1.0,{}),
("Mahjong Register",D+"mahjongregister.png",1.0,{}),
("Mahj & Vine",D+"mahjvine.png",1.0,{}),
("Amahj",D+"amahj.png",1.0,{"bgkey":True}),
("Splash of Color",R+"/builder/logos/splashofcolor_0.png",1.0,{}),
("The Mahjong Press",D+"themahjongpress.png",1.0,{}),
("Bespoke Mahjong",D+"bespokemahjong.png",1.0,{}),
("I Love Mahj",D+"ilovemahj.png",1.0,{}),
("Let's Mahj On",D+"letsmahjon_svg.png",1.0,{}),
("Mahj Pit",R+"/assets/brand/partner-logos/mahj-pit-stacked.png",1.0,{}),
("Maison Mahj",R+"/assets/brand/partner-logos/maison-mahj.png",1.0,{}),
("Noli June",R+"/assets/brand/partner-logos/noli-june.png",1.0,{}),
("Soirée All Day",D+"soireallday.png",1.0,{"bgkey":True}),
("YOLO Mahjong",R+"/assets/brand/partner-logos/yolo-mahjong.png",1.0,{}),
("Wren Mats",D+"wren.jpg",1.0,{"bgkey":True}),
("Mahjong Studios",R+"/builder/logos/mahjongstudios_0.png",1.0,{}),
("Tigre de Tartán",D+"tigredetartn.png",1.0,{}),
]
out=[]
for i,(b,f,w,o) in enumerate(SRC):
    im=Image.open(f).convert('RGBA')
    a=np.array(im).astype(int)
    if o.get('bgkey'):
        # key out the colour found at the corners (flat background box)
        c=a[2,2,:3]; d=np.abs(a[:,:,:3]-c).sum(2)
        a[:,:,3]=np.where(d<40,0,a[:,:,3])
    # ink = not transparent and not near-white
    ink=(a[:,:,3]>25)&(a[:,:,:3].min(2)<238)
    ys,xs=np.where(ink)
    if len(xs)==0: print('EMPTY',b); continue
    x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
    a=a[y0:y1,x0:x1]
    # make near-white fully transparent only if image had no alpha bg (opaque white bg)
    if (a[:,:,3]>250).mean()>0.98:
        wh=a[:,:,:3].min(2)>245; a[:,:,3]=np.where(wh,0,a[:,:,3])
    if o.get('recolor'):
        r,g,bb=o['recolor']
        a[:,:,0]=r;a[:,:,1]=g;a[:,:,2]=bb
    if o.get('clipbr'):
        H_,W_=a.shape[:2]; a[int(H_*0.8):,int(W_*0.82):,3]=0
        ys2,xs2=np.where(a[:,:,3]>25); a=a[ys2.min():ys2.max()+1,xs2.min():xs2.max()+1]
    t=Image.fromarray(a.astype('uint8'),'RGBA')
    fn=f'trim/{i:02d}.png'; t.save(fn)
    out.append({'brand':b,'file':fn,'w':t.size[0],'h':t.size[1],'weight':w})
    print(i,b,t.size)
json.dump(out,open('trim/list.json','w'),indent=1)
