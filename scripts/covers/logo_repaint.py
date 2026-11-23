"""Nov 23 2026 (Tiffany 11:50am: 'you've messed up their logo... you cannot mess up their logos').
Repaint a brand logo on a uniform cover from the CLEAN brand logo file (the Oct 20 'lifted' logos are ragged).
Usage: python3 scripts/covers/logo_repaint.py <cover.jpg> <clean white logo png> <logo width px> <centre y in a 1350 cover> [region y0 y1 x0 x1]
Works on 1080x1350 covers and 1080x1920 reel covers (same design, 285px lower)."""
import sys, numpy as np, cv2
from PIL import Image
f, logo, w, cy = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
r = [int(x) for x in sys.argv[5:9]] if len(sys.argv) > 8 else [335, 500, 300, 770]
c = Image.open(f).convert('RGB'); dy = 285 if c.size[1] == 1920 else 0; a = np.asarray(c).copy()
y0, y1, x0, x1 = r[0]+dy, r[1]+dy, r[2], r[3]; reg = a[y0:y1, x0:x1]
mask = cv2.dilate(((reg.min(axis=2).astype(int) > 150)*255).astype('uint8'), np.ones((9, 9), np.uint8))
a[y0:y1, x0:x1] = cv2.cvtColor(cv2.inpaint(cv2.cvtColor(reg, cv2.COLOR_RGB2BGR), mask, 7, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB)
out = Image.fromarray(a); lg = Image.open(logo).convert('RGBA'); lg = lg.crop(lg.getbbox()); h = round(lg.height*w/lg.width); lg = lg.resize((w, h), Image.LANCZOS)
out.paste(lg, (540-w//2, cy+dy-h//2), lg); out.save(f, quality=94); print(f)
