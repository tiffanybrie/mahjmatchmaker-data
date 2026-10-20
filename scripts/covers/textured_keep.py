"""Oct 20 (Tiffany): the textured panels (Glow Wild, Heritage, Heritage 2.0, Talulah, Emerald, Cypress) keep her ORIGINAL cover
untouched (texture, title, logo). Only the old wordmark + pink bar are removed (texture-aware FSR inpaint) and the
flame-heart wordmark + FIND YOUR MATCH go on. Usage: python3 textured_keep.py <outdir> key ..."""
import sys, os, glob, numpy as np, cv2
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import tagline_v2 as T
R = '/home/claude/mahjmatchmaker-data/'; OUT = sys.argv[1]
def src(k): return [f for f in glob.glob(R + 'assets/covers/albums/*.jpg') if os.path.basename(f).split('-', 1)[1].startswith(k + '-mahjong-tiles')][0]
for k in sys.argv[2:]:
    a = np.asarray(Image.open(src(k)).convert('RGB').resize((1080, 1350), Image.LANCZOS)).copy()
    logo_box = None
    if k == 'heritage-2-0':   # her original has the pink OMM logo: remove it (texture fill) and place the white logo
        h = cv2.cvtColor(a, cv2.COLOR_RGB2HSV); t, l = 300, 300; sub = h[300:560, 300:780]
        ok = (sub[..., 1] > 80) & (((sub[..., 0] > 140) & (sub[..., 2] > 140)) | ((sub[..., 0] > 95) & (sub[..., 0] < 130) & (sub[..., 2] > 110)))
        ys, xs = np.nonzero(ok); y0_, y1_, x0_, x1_ = ys.min() + t, ys.max() + t, xs.min() + l, xs.max() + l
        lm = np.zeros(a.shape[:2], np.uint8); lm[y0_ - 6:y1_ + 7, x0_ - 6:x1_ + 7] = 1
        bg_ = cv2.cvtColor(a, cv2.COLOR_RGB2BGR); o_ = np.zeros_like(bg_)
        cv2.xphoto.inpaint(bg_, (1 - lm).astype(np.uint8), o_, cv2.xphoto.INPAINT_FSR_FAST); a = cv2.cvtColor(o_, cv2.COLOR_BGR2RGB)
        logo_box = (x0_, y0_, x1_ - x0_ + 1, y1_ - y0_ + 1)
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV); y0, y1 = 895, 1052; band = a[y0:y1].astype(int)
    white = (band.min(axis=2) > 190) & (hsv[y0:y1, :, 1] < 70)
    pink = (np.abs(band[..., 0] - 245) < 35) & (np.abs(band[..., 1] - 108) < 45) & (np.abs(band[..., 2] - 140) < 45)
    mm = (white | pink).astype(np.uint8); mm[:, :190] = 0; mm[:, 890:] = 0
    for xa, xb in ((0, 352), (728, 1080)): mm[990 - y0:1035 - y0, xa:xb] = 0
    m = np.zeros(a.shape[:2], np.uint8); m[y0:y1] = mm
    m[996:1030, 345:735] = 1   # whole old pink bar incl. its end caps
    m = cv2.dilate(m, np.ones((9, 9), np.uint8))
    bgr = cv2.cvtColor(a, cv2.COLOR_RGB2BGR); outb = np.zeros_like(bgr)
    cv2.xphoto.inpaint(bgr, (1 - m).astype(np.uint8), outb, cv2.xphoto.INPAINT_FSR_FAST)
    img = Image.fromarray(cv2.cvtColor(outb, cv2.COLOR_BGR2RGB)).convert('RGBA')
    img.alpha_composite(Image.open(R + 'scripts/covers/holiday/frame3.png').convert('RGBA').resize((906, 788)), (87, 281))
    if logo_box:
        lg = Image.open(R + 'scripts/covers/holiday/omm_white.png').convert('RGBA'); x, y, w_, h_ = logo_box
        lg = lg.resize((w_, int(lg.height * w_ / lg.width)), Image.LANCZOS); img.alpha_composite(lg, (x, y + (h_ - lg.height) // 2))
    wm = Image.open(R + 'scripts/covers/holiday/ourlogo.png').convert('RGBA'); w = 540; wm = wm.resize((w, int(wm.height * w / wm.width)), Image.LANCZOS)
    img.alpha_composite(wm, ((1080 - w) // 2, 942 - wm.height // 2)); t = T.tagline('FIND YOUR MATCH'); img.alpha_composite(t, ((1080 - t.width) // 2, 1012 - t.height // 2))
    img.convert('RGB').save(f'{OUT}/{k}.jpg', quality=94); print(k)
