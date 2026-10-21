"""Frame-level review for the S2 v2 reels (Oct 21 process rule): contact sheets at full fps around every cut
(+-0.5 s) and over the whole ending, plus frame-diff checks for one-frame flashes and blank frames.
Usage: python3 scripts/reel/s2/v2/review.py REEL.mp4 OUTDIR [--cuts f1,f2,...] [--end-from FRAME]
Prints: detected cuts, flash suspects (a frame that differs from BOTH neighbours while they match each other),
blank/flat frames, and the sheet paths."""
import sys, os, subprocess, argparse
import numpy as np
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser(); ap.add_argument('mp4'); ap.add_argument('out')
ap.add_argument('--cuts', default=''); ap.add_argument('--end-from', type=int, default=None)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
W, H = 108, 192
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', a.mp4, '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                     capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.float32); n = len(fr)
d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2, 3))            # d[i] = |f[i+1]-f[i]|
print(f'{a.mp4}: {n} frames ({n / 30:.2f}s)')
med = float(np.median(d)) + .05
cuts = [i + 1 for i in range(len(d)) if d[i] > max(12, 8 * med)]
print('detected cuts (frame, s, diff):', [(c, round(c / 30, 2), round(float(d[c - 1]), 1)) for c in cuts])
flash = []
for i in range(1, n - 1):
    nb = np.abs(fr[i + 1] - fr[i - 1]).mean()
    if d[i - 1] > 10 and d[i] > 10 and nb < .35 * min(d[i - 1], d[i]):
        flash.append((i, round(i / 30, 2), round(float(d[i - 1]), 1), round(float(nb), 1)))
print('one-frame flash suspects:', flash or 'none')
std = fr.reshape(n, -1, 3).std(axis=1).mean(axis=1)
blank = [(i, round(i / 30, 2), round(float(std[i]), 1)) for i in range(n) if std[i] < 4]
print('blank/flat frames:', blank or 'none')
np.save(f'{a.out}/diff.npy', d)


def sheet(frames, name, cols=8, w=240):
    h = int(w * 16 / 9)
    fs = [f for f in frames if 0 <= f < n]
    rows = (len(fs) + cols - 1) // cols
    im = Image.new('RGB', (cols * w, rows * (h + 22)), 'black'); dr = ImageDraw.Draw(im)
    tmp = f'{a.out}/_f'; os.makedirs(tmp, exist_ok=True)
    sel = '+'.join(f'eq(n,{f})' for f in fs)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', a.mp4, '-vf', f"select='{sel}',scale={w}:{h}", '-vsync', '0', f'{tmp}/%04d.png'], check=True)
    for k, f in enumerate(fs):
        x, y = (k % cols) * w, (k // cols) * (h + 22)
        im.paste(Image.open(f'{tmp}/{k + 1:04d}.png'), (x, y + 22)); dr.text((x + 4, y + 4), f'{f} ({f / 30:.2f}s)', fill='white')
        os.remove(f'{tmp}/{k + 1:04d}.png')
    p = f'{a.out}/{name}.jpg'; im.save(p, quality=85); return p


cl = sorted(set(cuts + [int(x) for x in a.cuts.split(',') if x]))
for c in cl:
    print('sheet', sheet(range(c - 15, c + 16), f'cut-{c:04d}'))
ef = a.end_from if a.end_from is not None else n - 216
for k, s in enumerate(range(ef, n, 48)):
    print('sheet', sheet(range(s, min(n, s + 48)), f'end-{k}'))
