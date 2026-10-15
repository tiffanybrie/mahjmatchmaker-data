"""Regular album cover (the Sunday Tile Set cover style, no holiday twist), 1080x1350.
Photo full-bleed, translucent rectangle in the tile set's colour, chinoiserie corner frame,
brand logo on a cream tag, Caprasimo title, our flame-heart wordmark (doc 52).
Usage: python3 album_cover.py <bg photo> <brand logo png> <logo height px> "<Title<br>Line 2>" "<r,g,b>" <out.jpg> [bg position]"""
import sys, os, subprocess, tempfile
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'holiday')
bg, logo, lh, title, rgb, out = sys.argv[1:7]
pos = sys.argv[7] if len(sys.argv) > 7 else '50% 50%'
fs = 104 if '<br>' in title else 118
html = f'''<html><head><link href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Montserrat:wght@700&display=block" rel="stylesheet"><style>
body{{margin:0;width:1080px;height:1350px;overflow:hidden;background:#000;position:relative}}
.bg{{position:absolute;inset:0;background:url("{os.path.abspath(bg)}") {pos}/cover no-repeat}}
.p{{position:absolute;left:87px;top:281px;width:906px;height:788px;background:rgba({rgb},.88)}}
.f{{position:absolute;left:87px;top:281px;width:906px;height:788px;background:url({H}/frame2.png)}}
.c{{position:absolute;left:87px;top:300px;width:906px;height:620px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;color:#fbf6ee;text-align:center}}
.tag{{background:#fbf6ee;border-radius:14px;padding:12px 22px;box-shadow:0 4px 14px rgba(0,0,0,.25);display:flex}}
.tag img{{display:block;height:{lh}px}}
h1{{font:400 {fs}px/1.02 Caprasimo;margin:10px 0 0;text-shadow:0 2px 8px rgba(0,0,0,.18)}}
.our{{position:absolute;left:50%;transform:translateX(-50%);top:950px;width:500px}}
.p,.f,.c,.our{{z-index:1}}
</style></head><body><div class="bg"></div><div class="p"></div><div class="f"></div>
<div class="c"><div class="tag"><img src="{os.path.abspath(logo)}"></div><h1>{title}</h1></div>
<img class="our" src="{H}/ourlogo.png"></body></html>'''
d = tempfile.mkdtemp(); hf = os.path.join(d, 'cover.html'); open(hf, 'w').write(html)
NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
js = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'albumcard', 'shot.js')
subprocess.run(['node', js, hf, os.path.abspath(out)], check=True, env={**os.environ, 'NODE_PATH': NP}, stdout=subprocess.DEVNULL)
print(out)
