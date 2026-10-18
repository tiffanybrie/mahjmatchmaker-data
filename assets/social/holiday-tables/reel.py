# Holiday table reels: cover -> item-by-item reveal -> full table + LINK IN BIO. No audio (she adds music in-app).
import sys, os, subprocess, shutil
S='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
exec(open(S+'holiday_social/build.py').read().split("if __name__=='__main__':")[0])
FPS=30

def sprite(im,rot=0):
    if rot: im=im.rotate(rot,expand=True,resample=Image.BICUBIC)
    sp,(dx,dy)=shadow(im); return sp,dx,dy

def mk(kind,p,**k):
    if kind=='mat': return matimg(p,k['w'],k.get('rad',0.045))
    if kind=='card': return card(load(p),k['w'],k.get('h',k['w']))
    im=load(p)
    return fit(im,w=k['w']) if 'w' in k else fit(im,h=k['h'])

def layout(k):
    L=LOOKS[k]; it=[]
    def add(img,x,y,rot=0,label=None,lx=0,ly=0,ls=32,anchor='la'):
        sp,dx,dy=sprite(img,rot); it.append(dict(sp=sp,x=x+dx,y=y+dy,label=label,lx=lx,ly=ly,ls=ls,anchor=anchor))
    if k=='polo':
        m=mk('mat',L['mat'],w=600); add(m,430,250,-2,'polo club mat',730,180,30,'ma')
        add(mk('cut',L['rack'],w=600),440,890,1,'walnut racks',740,960,30,'ma')
        add(mk('card',HER,w=300,h=300),50,280,-4,'heritage tiles',60,240,30)
        add(mk('card',TS+'raw/cloth60.jpg',w=300,h=300),50,700,3,'hunter green cloth',60,1030,28)
        add(mk('cut',TS+'cut/coaster1.png',w=170),480,1010,0,'cognac coaster',565,1200,26,'ma')
        add(mk('cut',TS+'cut/ringdish.png',w=210),760,990,4,'tree ring dish',865,1210,26,'ma')
        add(mk('cut',TS+'cut/tree.png',h=330),80,1350,0,'a little tree',180,1700,28,'ma')
        add(mk('cut',TS+'cut/wreath.png',w=300),390,1470,0,'a candle wreath',540,1700,28,'ma')
        add(mk('cut',TS+'cut/lamp_green.png',h=400),790,1290,0,'a ribboned lamp',900,1700,28,'ma')
        extra=('pick one for the center',W//2,1300)
    elif k=='rattan':
        add(mk('cut',L['mat'],w=600),430,250,-2,'rattan mat',730,180,30,'ma')
        add(mk('cut',L['rack'],w=600),440,890,1,'walnut racks',740,960,30,'ma')
        add(mk('card',HER,w=300,h=300),50,280,-4,'heritage tiles',60,240,30)
        add(mk('cut',T2+'cut/clothE.png',w=360),30,720,2,'red tartan cloth',60,655,28)
        add(mk('cut',T2+'cut/lamp_tree.png',h=560),90,1120,0,'ceramic tree lamp',240,1720,28,'ma')
        add(mk('cut',T2+'cut/dice_holly.png',w=290),470,1290,-4,'holly dice dish',615,1600,28,'ma')
        add(mk('cut',T2+'cut/coaster_amber.png',w=230),790,1330,0,'amber glass coaster',905,1600,26,'ma')
        extra=None
    else:
        m=mk('mat',L['mat'],w=600,rad=0.0425); add(m,430,250,0,"rackin' rudolph mat",730,180,30,'ma')
        mb=250+m.height
        add(mk('card',T3+'raw/t_31a3RZHWCgL.jpg',w=300,h=300),50,280,-3,'cherry red cloth',60,240,30)
        add(mk('cut',T3+'cut/tiles_fan2.png',w=380),20,700,-2,"rackin' rudolph tiles",40,660,28)
        add(mk('cut',L['rack'],w=460),500,mb-80,0,'middle & main scalloped milk glass racks',730,mb+110,24,'ma')
        add(mk('cut',T3+'cut/lamp_bow.png',h=560),110,1130,0,'the bow lamp',230,1720,28,'ma')
        add(mk('cut',T3+'cut/deer_box.png',h=380),440,1260,0,'reindeer dice box',620,1680,28,'ma')
        add(mk('cut',T3+'cut/coaster_marble.png',w=210),800,1360,0,'marble coaster',905,1610,26,'ma')
        extra=None
    return it,extra

def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
def back(t):
    t=max(0,min(1,t)); c1=1.70158; c3=c1+1; return 1+c3*(t-1)**3+c1*(t-1)**2

def render(k):
    L=LOOKS[k]; od=OUT+k+'/reel_frames/'
    shutil.rmtree(od,ignore_errors=True); os.makedirs(od)
    cover=f_cover(L).convert('RGB')
    items,extra=layout(k)
    T_COVER=1.8; STEP=0.75; POP=0.35
    t_build=T_COVER; t_end=t_build+STEP*len(items)+0.6; T_TOTAL=t_end+2.2
    n=int(T_TOTAL*FPS); bg=base()
    lf=lambda s: font('HomemadeApple.ttf',s)
    for f in range(n):
        t=f/FPS
        if t<T_COVER:
            z=1+0.04*(t/T_COVER)
            im=cover.resize((int(W*z),int(Hh*z)),Image.LANCZOS)
            x=(im.width-W)//2; y=(im.height-Hh)//2; fr=im.crop((x,y,x+W,y+Hh))
            if t>T_COVER-0.25:
                a=(t-(T_COVER-0.25))/0.25; fr=Image.blend(fr,bg.convert('RGB'),a)
            fr.save(od+f'{f:04d}.jpg',quality=90); continue
        c=bg.copy(); d=ImageDraw.Draw(c)
        for i,it in enumerate(items):
            t0=t_build+i*STEP; p=(t-t0)/POP
            if p<=0: continue
            sc=back(p); al=ease(p*1.5)
            sp=it['sp']
            if sc<0.999 or al<0.999:
                w_,h_=max(1,int(sp.width*sc)),max(1,int(sp.height*sc))
                s2=sp.resize((w_,h_),Image.BILINEAR)
                if al<1:
                    a=s2.split()[3].point(lambda v:int(v*al)); s2.putalpha(a)
                cx=it['x']+sp.width//2; cy=it['y']+sp.height//2
                c.alpha_composite(s2,(cx-w_//2,cy-h_//2))
            else:
                c.alpha_composite(sp,(it['x'],it['y']))
            if it['label'] and p>0.7:
                d.text((it['lx'],it['ly']),it['label'],font=lf(it['ls']),fill=INK,anchor=it['anchor'])
        if extra and t>t_build+STEP*6:
            d.text((extra[1],extra[2]),extra[0],font=font('Caprasimo.ttf',40),fill=L['pillc'],anchor='mm')
        if t>t_end:
            a=ease((t-t_end)/0.4)
            band=Image.new('RGBA',(W,Hh),(0,0,0,0)); bd=ImageDraw.Draw(band)
            y0=int(1790-40*(1-a))
            bd.rounded_rectangle((70,y0,1010,y0+110),55,fill=L['pillc']+(int(255*a),))
            fA=font('Caprasimo.ttf',44); t1='shop the whole table'; t2='LINK IN BIO'; g=50
            w1=bd.textlength(t1,font=fA); w2=bd.textlength(t2,font=fA); x0=W//2-(w1+w2+g)/2
            col=L['pillt']+(int(255*a),)
            bd.text((x0,y0+55),t1,font=fA,fill=col,anchor='lm'); bd.ellipse((x0+w1+g/2-6,y0+49,x0+w1+g/2+6,y0+61),fill=col)
            bd.text((x0+w1+g,y0+55),t2,font=fA,fill=col,anchor='lm')
            c.alpha_composite(band)
        c.convert('RGB').save(od+f'{f:04d}.jpg',quality=90)
    mp4=OUT+k+f'/{k}-holiday-table-reel.mp4'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',od+'%04d.jpg','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',mp4],check=True)
    print(k,n,'frames',round(T_TOTAL,1),'s ->',mp4)

if __name__=='__main__':
    for k in (sys.argv[1:] or ['polo','rattan','rudolph']): render(k)
