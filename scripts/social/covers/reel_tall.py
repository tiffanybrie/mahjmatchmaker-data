"""Tall (9:16) reel-cover versions of the uniform-v3 album covers.
The grid tile (3:4 middle) is cut only from the real cover, same size as the photo-post tile;
the band above/below (only seen when the full reel cover opens) is a soft blur of the cover.
Usage: python3 scripts/social/covers/reel_tall.py [slug ...]   (no args = all)"""
import sys, os, glob
from PIL import Image, ImageFilter, ImageEnhance
SRC='assets/covers/albums/uniform-v3'; OUT='assets/covers/albums/reel-tall'
slugs=sys.argv[1:] or [os.path.splitext(os.path.basename(p))[0] for p in glob.glob(SRC+'/*.jpg')]
for s in slugs:
    c=Image.open(f'{SRC}/{s}.jpg').convert('RGB').resize((1080,1350),Image.LANCZOS)
    W,H=1080,1920
    bg=c.resize((1536,1920),Image.LANCZOS).crop((228,0,228+W,H)).filter(ImageFilter.GaussianBlur(40))
    bg=ImageEnhance.Brightness(bg).enhance(0.92)
    bg.paste(c.resize((1152,1440),Image.LANCZOS).crop((36,0,1116,1440)),(0,240))
    bg.save(f'{OUT}/{s}.jpg',quality=93); print(s)
