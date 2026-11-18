# Replace the typed "Find Your Mat-ch" header in the reels' phone segment with the real lockup image.
# Fades are handled linearly: fixed = frame + a*(fixed_ref - ref), a = how much of the phone scene is in the frame.
import sys, glob, os, shutil
import numpy as np
from PIL import Image
LOCK='/home/claude/tiffanybrie/mahjmatchmaker-data/assets/brand/fym-lockup/find-your-mat-ch-lockup.png'
BG=(245,233,223)
def run(src_dir, dst_dir, box, lw, ref_idx):
    fs=sorted(glob.glob(src_dir+'/f*.png')); os.makedirs(dst_dir,exist_ok=True)
    x0,y0,x1,y1=box
    ref=np.asarray(Image.open(fs[ref_idx]).convert('RGB')).astype(float)
    fixed=Image.fromarray(ref.astype(np.uint8)); fixed.paste(BG,(x0,y0,x1,y1))
    lk=Image.open(LOCK); lh=round(lk.height*lw/lk.width); lk=lk.resize((lw,lh),Image.LANCZOS)
    cy=(y0+y1)//2; fixed=fixed.convert('RGBA'); fixed.alpha_composite(lk,((1080-lw)//2,cy-lh//2)); fixed=np.asarray(fixed.convert('RGB')).astype(float)
    delta=(fixed-ref)[y0:y1,x0:x1]; R=ref[y0:y1,x0:x1]
    ds=[]
    for f in fs: ds.append(np.abs(np.asarray(Image.open(f).convert('RGB')).astype(float)[y0:y1,x0:x1]-R).mean())
    full=[i for i,d in enumerate(ds) if d<3]; lo,hi=full[0],full[-1]
    # Fade-in: in the header box a frame is BG + c*(A-BG) + h*(T-BG), with A the last steady frame
    # before the fade and T the typed-header reference. Solve c and h per frame by least squares, then
    # swap the typed header for the lockup at that same strength h: frame + h*(fixed - ref).
    # Frames after the segment get h=0 (a hard cut leaves no header behind).
    def box(i): return np.asarray(Image.open(fs[i]).convert('RGB')).astype(float)[y0:y1,x0:x1]
    def moving(i): return np.abs(box(i)-box(i-1)).mean()>0.3
    j=lo
    while j>1 and moving(j): j-=1
    bg=np.array(BG,float); Av=(box(j-1)-bg).ravel(); Tv=(R-bg).ravel(); M=np.stack([Av,Tv],1)
    alphas={i:(1.0 if lo<=i<=hi else 0.0) for i in range(len(fs))}
    for i in range(j,lo):
        (c,h),res,_,_=np.linalg.lstsq(M,(box(i)-bg).ravel(),rcond=None)
        alphas[i]=min(1.0,max(0.0,float(h)))
    for i,f in enumerate(fs):
        a=alphas[i]; out=os.path.join(dst_dir,os.path.basename(f))
        if a==0:
            shutil.copyfile(f,out); continue  # a real copy, never a hard link (a later save would write into the source)
        im=np.asarray(Image.open(f).convert('RGB')).astype(float); im[y0:y1,x0:x1]+=a*delta
        Image.fromarray(np.clip(im,0,255).astype(np.uint8)).save(out)
    print('segment',lo+1,hi+1,'fades',{k+1:round(v,2) for k,v in alphas.items() if 0<v<1})
if __name__=='__main__':
    which=sys.argv[1]; S=sys.argv[2]
    if which=='ds': run(S+'/src_ds',S+'/fix_ds',(95,176,990,276),860,300)
    else: run(S+'/src_tin',S+'/fix_tin',(130,276,960,368),800,275)
