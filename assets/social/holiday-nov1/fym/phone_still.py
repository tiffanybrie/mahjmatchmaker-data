"""Rule 20 check for this reel: the phone bezel on the side the card is NOT flying to edge must not move during each swipe (the card's soft shadow passes over it, so edges are compared, not pixels)
(center_check --phone-still mistakes the white flying card for the phone). Usage: python3 phone_still.py <nobg.mp4>"""
import sys, subprocess, numpy as np
from PIL import Image
import tempfile, glob
SW = [('s0 heart', 4.9, 5.95, 'L'), ('s1 x', 7.15, 8.2, 'R'), ('s2 heart', 9.8, 10.85, 'L'), ('s3 heart', 10.9, 11.95, 'L'),
      ('r0 x', 19.2, 20.2, 'R'), ('r1 heart', 20.3, 21.3, 'L'), ('r2 heart', 21.4, 22.45, 'L')]
bad = 0
for name, a, b, side in SW:
    d = tempfile.mkdtemp(); subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-i', sys.argv[1], '-t', str(b - a), '-vf', 'fps=15', f'{d}/f%03d.png'], check=True)
    def edge(f):   # outer bezel edge (navy background -> light bezel), median over rows 700-1500, on the side the card is not flying to
        a = np.asarray(Image.open(f).convert('L'))[700:1500].astype(int)
        if side == 'R': a = a[:, ::-1]
        return float(np.median([np.argmax(r[:200] > 150) for r in a]))
    e = [edge(f) for f in sorted(glob.glob(f'{d}/*.png'))]
    diff = max(abs(x - e[0]) for x in e)
    print(f'{name:10s} {side} bezel edge at {e[0]:.0f}px from the {side} side, max move {diff:.1f}px over {len(e)} frames', 'OK' if diff <= 2 else 'MOVED'); bad += diff > 2
print('phone_still:', 'FAIL' if bad else 'PASS')
