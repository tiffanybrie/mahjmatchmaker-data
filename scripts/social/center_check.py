"""Centering check for any graphic or reel (Tiffany Oct 27: things keep landing left/right of center).
Usage: python3 scripts/social/center_check.py <image-or-mp4> [more...]   (mp4: 1 frame/sec)
Splits each frame into horizontal bands of content (text lines, images) and reports bands whose
left/right margins differ by more than TOL px (default 16, env TOL). Exit 1 if any band is off.
Callout stickers that are meant to sit to one side will show up: judge those by eye, everything else must pass.

--phone-still (rules audit GA3, Oct 30; docs/FYM-REEL-RULES.md rule 20 "the phone frame never moves"):
  python3 scripts/social/center_check.py --phone-still <reel.mp4> [--from S] [--to S] [--fps N]
  Finds the phone/app frame in every sampled frame (the large near-white panel that differs from the background colour,
  or --phone-color RRGGBB) and reports the FIRST frame whose box moves more than PTOL px (default 4, env PTOL) from the
  first frame of the scene. Limit to the swipe scene with --from/--to (seconds). Exit 1 if it moves."""
import sys, os, subprocess, tempfile, glob
from PIL import Image, ImageChops
TOL = int(os.environ.get('TOL', 16))
def frames(p):
    if p.lower().endswith(('.mp4', '.mov')):
        d = tempfile.mkdtemp(); subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', 'fps=1', f'{d}/f%03d.png'], check=True)
        return sorted(glob.glob(f'{d}/*.png'))
    return [p]
def _arg(name, default=None):
    if name in sys.argv:
        i = sys.argv.index(name); v = sys.argv[i + 1]; del sys.argv[i:i + 2]; return v
    return default


def phone_box(path, color=None):
    import numpy as np
    a = np.asarray(Image.open(path).convert('RGB')).astype(int); H, W, _ = a.shape
    if color:
        c = np.array([int(color[i:i + 2], 16) for i in (0, 2, 4)])
        m = (np.abs(a - c).sum(2) < 30)
    else:
        corners = np.array([a[4, 4], a[4, W - 5], a[H - 5, 4], a[H - 5, W - 5]]).mean(0)
        m = (a.min(2) >= 246) & (np.abs(a - corners).sum(2) > 12)
    cols = np.where(m.mean(0) > 0.25)[0]; rows = np.where(m.mean(1) > 0.25)[0]
    if not len(cols) or not len(rows):
        return None
    return int(cols[0]), int(rows[0]), int(cols[-1]), int(rows[-1])


if '--phone-still' in sys.argv:
    sys.argv.remove('--phone-still')
    t0 = float(_arg('--from', 0)); t1 = _arg('--to'); fps = _arg('--fps', '2'); col = _arg('--phone-color')
    PTOL = int(os.environ.get('PTOL', 4)); moved = 0
    for p in sys.argv[1:]:
        d = tempfile.mkdtemp()
        cmd = ['ffmpeg', '-v', 'error', '-ss', str(t0)] + (['-to', str(t1)] if t1 else []) + ['-i', p, '-vf', f'fps={fps}', f'{d}/f%04d.png']
        if t1: cmd = ['ffmpeg', '-v', 'error', '-ss', str(t0), '-i', p, '-t', str(float(t1) - t0), '-vf', f'fps={fps}', f'{d}/f%04d.png']
        subprocess.run(cmd, check=True)
        fs = sorted(glob.glob(f'{d}/*.png')); ref = None
        for n, f in enumerate(fs):
            b = phone_box(f, col)
            if b is None:
                print(f'NOPHONE {os.path.basename(p)} t={t0 + n / float(fps):.1f}s: no phone frame found'); moved += 1; break
            if ref is None:
                ref = b; continue
            dmax = max(abs(x - y) for x, y in zip(b, ref))
            if dmax > PTOL:
                moved += 1
                print(f'MOVED {os.path.basename(p)} t={t0 + n / float(fps):.1f}s: phone box {b} vs {ref} (moved {dmax}px)'); break
        else:
            print(f'STILL {os.path.basename(p)}: phone box {ref} over {len(fs)} frames')
    print('phone_still:', 'FAIL' if moved else 'PASS'); sys.exit(1 if moved else 0)

bad = 0
for p in sys.argv[1:]:
    for f in frames(p):
        im = Image.open(f).convert('RGB'); W, H = im.size
        bg = Image.new('RGB', im.size, im.getpixel((6, H // 2)))
        m = ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > 40 else 0)
        rows = [m.crop((0, y, W, y + 1)).getbbox() is not None for y in range(H)]
        y = 0
        while y < H:
            if not rows[y]: y += 1; continue
            y0 = y
            while y < H and rows[y]: y += 1
            if y - y0 < 12: continue
            b = m.crop((0, y0, W, y)).getbbox(); l, r = b[0], W - b[2]
            if l == 0 and r == 0: continue
            if abs(l - r) > TOL:
                bad += 1; print(f'OFF  {os.path.basename(p)} {os.path.basename(f)} y{y0}-{y}: left {l}px vs right {r}px (shifted {"right" if l > r else "left"} by {abs(l-r)//2}px)')
print('center_check:', 'FAIL' if bad else 'PASS', bad, 'off-centre bands'); sys.exit(1 if bad else 0)
