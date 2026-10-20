"""Oct 20: Talulah's original title had a drop shadow. Repaint the logo+title area from its own (smooth) panel texture,
then set white OMM logo + 'Talulah Tiles' at the standard size, no shadow. Usage: python3 talulah_fix.py <in.jpg> <out.jpg>"""
import sys, os, subprocess, tempfile, numpy as np, cv2
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'; C = R + 'scripts/covers/'
a = np.asarray(Image.open(sys.argv[1]).convert('RGB')).copy()
m = np.zeros(a.shape[:2], np.uint8); m[318:905, 175:905] = 1
small = cv2.resize(a, (270, 338), interpolation=cv2.INTER_AREA); ms = cv2.resize(m, (270, 338), interpolation=cv2.INTER_NEAREST)
fill = cv2.resize(cv2.inpaint(small, ms, 9, cv2.INPAINT_TELEA), (1080, 1350), interpolation=cv2.INTER_CUBIC)
fill = cv2.GaussianBlur(fill, (0, 0), 6)
w = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 12)[..., None]
out = (a * (1 - w) + fill * w).clip(0, 255).astype(np.uint8)
d = tempfile.mkdtemp(); Image.fromarray(out).save(d + '/bg.png')
html = f'''<html><head><link href="https://fonts.googleapis.com/css2?family=Caprasimo&display=block" rel="stylesheet"><style>
body{{margin:0;width:1080px;height:1350px;overflow:hidden;position:relative;background:url("{d}/bg.png")}}
.c{{position:absolute;left:87px;top:300px;height:600px;width:906px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:#fbf6ee;text-align:center}}
h1{{font:400 132px/1.0 Caprasimo;margin:14px 0 0;text-shadow:none}}</style></head>
<body><div class="c"><img src="{C}holiday/omm_white.png" style="display:block;height:160px"><h1>Talulah<br>Tiles</h1></div></body></html>'''
open(d + '/c.html', 'w').write(html)
NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
subprocess.run(['node', R + 'scripts/albumcard/shot.js', d + '/c.html', sys.argv[2]], check=True, env={**os.environ, 'NODE_PATH': NP}, stdout=subprocess.DEVNULL)
im = Image.open(sys.argv[2]).convert('RGBA'); im.alpha_composite(Image.open(C + 'holiday/frame3.png').convert('RGBA').resize((906, 788)), (87, 281)); im.convert('RGB').save(sys.argv[2], quality=94)
