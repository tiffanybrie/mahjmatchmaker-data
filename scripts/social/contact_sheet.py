"""Contact sheet for the social content scrub (Oct 21): every image (and N frames per video) in a grid with its name,
so a person or agent can actually LOOK at all drafts at once.
Usage: python3 scripts/social/contact_sheet.py OUT.jpg FILE_OR_DIR [...] [--cols 6] [--w 300] [--frames 6]
Videos (.mp4/.mov) contribute --frames evenly spaced frames each (ffmpeg)."""
import sys, os, glob, subprocess, tempfile, argparse
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('src', nargs='+')
ap.add_argument('--cols', type=int, default=6); ap.add_argument('--w', type=int, default=300)
ap.add_argument('--frames', type=int, default=6)
a = ap.parse_args()
IMG = ('.jpg', '.jpeg', '.png', '.webp'); VID = ('.mp4', '.mov')
files = []
for s in a.src:
    files += sorted(f for f in glob.glob(s + '/**/*', recursive=True) if f.lower().endswith(IMG + VID)) if os.path.isdir(s) else [s]
tiles = []; tmp = tempfile.mkdtemp()
for f in files:
    if f.lower().endswith(VID):
        d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))
        for i in range(a.frames):
            t = d * (i + .5) / a.frames; o = f'{tmp}/{len(tiles)}.jpg'
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{t:.2f}', '-i', f, '-frames:v', '1', o])
            if os.path.exists(o): tiles.append((o, f'{os.path.basename(f)} @{t:.1f}s'))
    else:
        tiles.append((f, os.path.basename(f)))
W = a.w; ims = []
for p, lab in tiles:
    try: im = Image.open(p).convert('RGB')
    except Exception: continue
    im = im.resize((W, max(1, int(im.height * W / im.width))))
    ims.append((im, lab))
H = max((im.height for im, _ in ims), default=W) + 34
rows = (len(ims) + a.cols - 1) // a.cols
sheet = Image.new('RGB', (a.cols * (W + 8) + 8, max(1, rows) * (H + 8) + 8), '#222')
dr = ImageDraw.Draw(sheet)
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
except Exception: font = ImageFont.load_default()
for i, (im, lab) in enumerate(ims):
    x = 8 + (i % a.cols) * (W + 8); y = 8 + (i // a.cols) * (H + 8)
    sheet.paste(im, (x, y)); dr.text((x + 2, y + im.height + 4), lab[:44], fill='#fff', font=font)
sheet.save(a.out, quality=85); print(a.out, len(ims), 'tiles')
