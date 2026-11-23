"""Nov 23 2026 (Tiffany 11:46am: Tortoise + Jade reel covers show bars in the Reels grid; Juniper/Lagoon are right).
True 9:16 reel cover for the covers whose background is a WALL OF TILE BACKS and whose source photo we don't have
(tortoise, jade): the 4:5 cover sits untouched in the middle (so the post-grid crop is identical) and the wall is
continued to the top and bottom with the cover's own real tile backs (bottom strip continues the top, top strip
continues the bottom, soft join). No blur bands, no mirroring. Covers with a tile PHOTO use TALL=1 album_cover_omm.py.
Usage: python3 scripts/social/covers/reel_tall_wall.py <slug> [join px]"""
import sys, numpy as np
from PIL import Image
slug=sys.argv[1]; J=int(sys.argv[2]) if len(sys.argv)>2 else 16
c=np.asarray(Image.open(f'assets/covers/albums/uniform-v3/{slug}.jpg').convert('RGB').resize((1080,1350),Image.LANCZOS)).astype(float)
E_=285; out=np.zeros((1920,1080,3)); out[E_:E_+1350]=c
# v3 (Tiffany 11:52am: 'those tile backs don't line up'): no stretch, no cross-fade. The seam IS a row edge: the
# continued row ends at the seam and a real-looking gap (shadow + lit edge, measured from the cover's own gaps) is drawn there.
C=270
out[E_-C:E_]=c[1350-C:1350]; out[0:E_-C]=c[1350-C:1350-C+(E_-C)][::1]*0+c[1350-C]   # above: the cover's real bottom rows
out[E_+1350:E_+1350+C]=c[0:C]; out[E_+1350+C:]=c[C-1]  # below: the cover's real top rows
def shift(a,dx):   # slide a strip sideways so its column gaps sit exactly over the cover's (edge pixels repeat)
    if dx==0: return a
    b=np.roll(a,dx,axis=1)
    if dx>0: b[:,:dx]=a[:,:1]
    else: b[:,dx:]=a[:,-1:]
    return b
DX=9 if slug=='tortoise' else 0   # measured: bottom-strip column gaps minus top-strip column gaps
out[0:E_]=shift(out[0:E_],-DX); out[E_+1350:]=shift(out[E_+1350:],DX)
def gap(y, soft):   # horizontal gap between two rows of backs, centred on y
    if soft:        # jade-style: thin dark line
        for k in range(-5,6): out[y+k]*=1-0.45*max(0,1-abs(k)/5)
        return
    for k in range(-26,0): out[y+k]*=max(0.04,1-((k+26)/20)**1.3) if k<-6 else 0.04
    for k in range(0,7): out[y+k]=out[y+k]*0.35+np.array([205,150,95])*0.65*(1-abs(k-3)/4)+out[y+k]*0.65*(abs(k-3)/4)
    for k in range(7,16): out[y+k]*=0.75+0.25*(k-7)/9
if slug=='jade':
    # Jade's wall has clean real row edges (rows start at cover y=26, 469, 912; period 443), so the continued rows are laid on
    # that true grid: every piece below comes from the same height inside a real tile, and the row edges are the real ones.
    out[34:E_]=c[1078:1329]; out[0:34]=c[153:187]
    for k in range(21): out[E_+k]=c[1329+k]*(1-k/20)+c[k]*(k/20)   # ease the continued tile into the cover's own row 0                       # above: row offsets 132..417, then the cover's row 0 (offset 417)
    out[E_+1350:E_+1350+254]=c[20:274]; out[E_+1350+254:]=c[1160:1191]  # below: real row edge (y=26) + the row under it
else:
    gap(E_,False); gap(E_+1350,False)
    import cv2
    for y in (E_,E_+1350):   # the cover's own gaps are soft-focus: match them
        out[y-34:y+24]=cv2.GaussianBlur(out[y-34:y+24],(0,0),2.2)
Image.fromarray(out.clip(0,255).astype('uint8')).save(f'assets/covers/albums/reel-tall/{slug}.jpg',quality=95); print(slug)
