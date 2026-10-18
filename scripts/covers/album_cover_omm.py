"""OMM-style album cover (the live Sorbet/Willow look), 1080x1350: photo full-bleed, translucent panel in the
set's colour, chinoiserie frame, brand logo straight on the panel (or on a cream tag with --tag), Caprasimo
"X Tiles" title, white mahjmatchmaker wordmark + pink tagline bar.
Usage: python3 album_cover_omm.py <bg> <logo png> <logo h px> "<Title<br>Tiles>" "<r,g,b>" <out.jpg> [bg pos] [--tag]"""
import sys, os, subprocess, tempfile
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'holiday')
args=[a for a in sys.argv[1:] if a!='--tag']; tag='--tag' in sys.argv
bg, logo, lh, title, rgb, out = args[:6]
pos = args[6] if len(args) > 6 else '50% 50%'
BAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tagbar.png')
fs = (96 if max(len(x) for x in title.split('<br>'))>10 else 112) if '<br>' in title else 124
logo_html = f'<div class="tag"><img src="{os.path.abspath(logo)}"></div>' if tag else f'<img class="lg" src="{os.path.abspath(logo)}">'
html = f'''<html><head><link href="https://fonts.googleapis.com/css2?family=Caprasimo&display=block" rel="stylesheet"><style>
body{{margin:0;width:1080px;height:1350px;overflow:hidden;background:#000;position:relative}}
.bg{{position:absolute;inset:0;background:url("{os.path.abspath(bg)}") {pos}/cover no-repeat}}
.p{{position:absolute;left:87px;top:281px;width:906px;height:788px;background:rgba({rgb},.88)}}
.f{{position:absolute;left:87px;top:281px;width:906px;height:788px;background:url({H}/frame2.png)}}
.c{{position:absolute;left:87px;top:360px;width:906px;display:flex;flex-direction:column;align-items:center;gap:6px;color:#fbf6ee;text-align:center}}
.lg{{display:block;height:{lh}px}}
.tag{{background:#fbf6ee;border-radius:14px;padding:12px 22px;box-shadow:0 4px 14px rgba(0,0,0,.25);display:flex}}
.tag img{{display:block;height:{lh}px}}
h1{{font:400 {fs}px/1.0 Caprasimo;margin:14px 0 0;text-shadow:0 2px 8px rgba(0,0,0,.18)}}
.our{{position:absolute;left:50%;transform:translateX(-50%);top:915px;width:560px}}
.bar{{position:absolute;left:50%;transform:translateX(-50%);top:1010px;width:380px}}
.p,.f,.c,.our,.bar{{z-index:1}}
</style></head><body><div class="bg"></div><div class="p"></div><div class="f"></div>
<div class="c">{logo_html}<h1>{title}</h1></div>
<img class="our" src="{H}/ourlogo.png"><img class="bar" src="{BAR}"></body></html>'''
d = tempfile.mkdtemp(); hf = os.path.join(d, 'cover.html'); open(hf, 'w').write(html)
NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
js = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'albumcard', 'shot.js')
subprocess.run(['node', js, hf, os.path.abspath(out)], check=True, env={**os.environ, 'NODE_PATH': NP}, stdout=subprocess.DEVNULL)
print(out)
