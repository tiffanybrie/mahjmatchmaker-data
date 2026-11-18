"""Origami Timber album cover, full layout (Mulberry Deco cover style: translucent set-colour panel, chinoiserie frame,
white Bam Bird logo, Caprasimo title, flame-heart wordmark). Usage: layout.py <bg.jpg> <out.jpg> [r,g,b] [alpha]"""
import sys, os, subprocess, tempfile
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); H = C + '/holiday'
bg, out = sys.argv[1:3]; rgb = sys.argv[3] if len(sys.argv) > 3 else '140,67,41'; al = sys.argv[4] if len(sys.argv) > 4 else '.88'
title = os.environ.get('TITLE', 'Origami<br>Timber Tiles'); lh = os.environ.get('LOGO_H', '160')  # Tiffany Nov 17 1:06am: SET name first, then colourway; Bam Bird logo bigger (delicate)
html = f'''<html><head><link href="https://fonts.googleapis.com/css2?family=Caprasimo&display=block" rel="stylesheet"><style>
body{{margin:0;width:1080px;height:1350px;overflow:hidden;position:relative}}
.bg{{position:absolute;inset:0;background:url("{os.path.abspath(bg)}") center/cover}}
.p{{position:absolute;left:87px;top:281px;width:906px;height:788px;background:rgba({rgb},{al})}}
.f{{position:absolute;left:87px;top:281px;width:906px;height:788px;background:url({H}/frame3.png)}}
.c{{position:absolute;left:87px;top:385px;width:906px;display:flex;flex-direction:column;align-items:center;gap:22px;color:#fbf6ee;text-align:center}}
.c img{{height:{lh}px}}
h1{{font:400 110px/0.95 Caprasimo;margin:18px 0 0;text-shadow:0 2px 8px rgba(0,0,0,.18)}}
.our{{position:absolute;left:50%;transform:translateX(-50%);top:922px;width:552px}}
.tb{{position:absolute;left:50%;transform:translateX(-50%);top:1006px;width:378px}}
</style></head><body><div class="bg"></div><div class="p"></div><div class="f"></div>
<div class="c"><img src="{H}/bambird_white.png"><h1>{title}</h1></div>
<img class="our" src="{H}/ourlogo.png"><img class="tb" src="{C}/tagbar.png"></body></html>'''
d = tempfile.mkdtemp(); hf = os.path.join(d, 'c.html'); open(hf, 'w').write(html)
NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
subprocess.run(['node', C + '/../albumcard/shot.js', hf, os.path.abspath(out)], check=True, env={**os.environ, 'NODE_PATH': NP}, stdout=subprocess.DEVNULL)
print(out)
