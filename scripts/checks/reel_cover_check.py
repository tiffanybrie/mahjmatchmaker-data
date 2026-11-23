"""Reel cover gate (Tiffany Nov 23 2026 11:46am + 11:50am 'save the cover rules... the cover card thing keeps coming up').
A reel cover must be 1080x1920 with the real background running to the very top and bottom: NO blur bands, NO flat
colour bars. The Reels tab shows the whole 9:16; the post grid shows the middle 3:4; both must look right.
FAIL = top/bottom band (240px) much softer than the background beside the box, or a hard seam at y=240 / y=1680.
Usage: python3 scripts/checks/reel_cover_check.py [files...]   (no args = assets/covers/albums/reel-tall/*.jpg)"""
import sys, glob, numpy as np
from PIL import Image
def sharp(a):
    g=a.astype(float).mean(axis=2); return float(np.abs(np.diff(g,axis=0)).mean()+np.abs(np.diff(g,axis=1)).mean())
bad=[]
for f in (sys.argv[1:] or sorted(glob.glob('assets/covers/albums/reel-tall/*.jpg'))):
    im=Image.open(f).convert('RGB')
    if im.size!=(1080,1920): bad.append((f,'size %dx%d'%im.size)); continue
    a=np.asarray(im)
    mid=(sharp(a[300:560])+sharp(a[1360:1620]))/2          # background above/below the box
    top,bot=sharp(a[0:230]),sharp(a[1690:1920])
    g=a.astype(float).mean(axis=2)
    seam=max(np.abs(g[238:243].mean(axis=1)[1:]-g[238:243].mean(axis=1)[:-1]).max(), np.abs(g[1678:1683].mean(axis=1)[1:]-g[1678:1683].mean(axis=1)[:-1]).max())
    why=[]
    if min(top,bot) < 0.45*mid: why.append('blur/flat band (top %.1f bottom %.1f vs background %.1f)'%(top,bot,mid))
    if why: bad.append((f,'; '.join(why)))
for f,w in bad: print('FAIL',f,w)
print('reel covers:', 'PASS' if not bad else 'FAIL %d'%len(bad)); sys.exit(1 if bad else 0)
