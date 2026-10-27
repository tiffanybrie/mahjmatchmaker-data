"""Centering check for any graphic or reel (Tiffany Oct 27: things keep landing left/right of center).
Usage: python3 scripts/social/center_check.py <image-or-mp4> [more...]   (mp4: 1 frame/sec)
Splits each frame into horizontal bands of content (text lines, images) and reports bands whose
left/right margins differ by more than TOL px (default 16, env TOL). Exit 1 if any band is off.
Callout stickers that are meant to sit to one side will show up: judge those by eye, everything else must pass."""
import sys, os, subprocess, tempfile, glob
from PIL import Image, ImageChops
TOL = int(os.environ.get('TOL', 16))
def frames(p):
    if p.lower().endswith(('.mp4', '.mov')):
        d = tempfile.mkdtemp(); subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', 'fps=1', f'{d}/f%03d.png'], check=True)
        return sorted(glob.glob(f'{d}/*.png'))
    return [p]
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
