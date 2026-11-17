"""Holiday album reel, Dear Santa v3 format (Tiffany Nov 9: dynamic, several scenes, album cover; a reel that promotes
Find Your Mat-ch MUST show the tool in use). Scenes: brand hook photo -> tiles -> photo-dump of the album's holiday match
cards with a running count -> LIVE Find Your Mat-ch recording in a phone (search the set, swipe) -> album cover -> end card.
Usage: build.py <config.json> <out.mp4>   config = reel_dump.py keys + search, button, label (e.g. "December 1994")."""
import json, sys, os, subprocess, shutil, bisect
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
R = '/home/claude/mahjmatchmaker-data'; H = R + '/scripts/social/holidayreel'; F = R + '/scripts/social/tileprofile/fonts'
cfg_p, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]); cfg = json.load(open(cfg_p))
W = os.path.splitext(out)[0] + '_work'; shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
FPS = 24
# 1 dump reel (hook, tiles, dump, cover, end)
subprocess.run(['python3', R + '/scripts/social/albumgrid/reel_dump.py', cfg_p, W + '/dump.mp4'], check=True)
# 2 live recording
subprocess.run(['python3', H + '/rec.py', cfg['search'], cfg['button'], W + '/rec'], check=True)
meta = json.load(open(W + '/rec/meta.json')); ts = [t - meta['ts'][0] for t in meta['ts']]; mk = dict(meta['marks'])
# 3 phone scene background with header
bgp = W + '/bg.png'
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    open(W + '/bg.html', 'w').write(f'''<html><head><style>@font-face{{font-family:Cap;src:url(file://{F}/Caprasimo.ttf)}}
@font-face{{font-family:PF;font-style:italic;src:url(file://{F}/playfair-display-latin-400-italic.woff2)}}
@font-face{{font-family:Bit;font-weight:700;src:url(file://{F}/bitter-latin-700-normal.woff2)}}
body{{margin:0;width:1080px;height:1920px;background:#f6e9df;text-align:center}}
h1{{font:92px/1 Cap;color:#0d4a2d;margin:0;padding-top:250px}}h1 i{{font:italic 92px PF}}h1 sup{{font-size:40px}}
p{{font:700 40px Bit;color:#b3152b;margin:22px 0 0}}</style></head><body>
<h1>Find <i>Your</i> Mat-ch<sup>™</sup></h1><p>Pick {cfg["label"]}. Swipe the mats.</p></body></html>''')
    pg.goto('file://' + W + '/bg.html'); pg.wait_for_timeout(1200); pg.screenshot(path=bgp); b.close()
bg = Image.open(bgp).convert('RGB')
PW, PH, PX, PY = 700, 1380, 190, 470
mask = Image.new('L', (PW, PH), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, PW - 1, PH - 1), 58, fill=255)
frame = Image.new('RGBA', (PW + 36, PH + 36), (0, 0, 0, 0)); ImageDraw.Draw(frame).rounded_rectangle((0, 0, PW + 35, PH + 35), 74, fill=(24, 24, 28, 255))
t_a, t_b = mk['home'] + 0.6, mk['swiped'] + 1.0; SPEED = (t_b - t_a) / 8.0 if (t_b - t_a) > 8 else 1.0
os.makedirs(W + '/ph')
n = int((t_b - t_a) / SPEED * FPS)
for i in range(n):
    t = t_a + i / FPS * SPEED; j = max(0, bisect.bisect_right(ts, t) - 1)
    sc = Image.open(f'{W}/rec/f/{j:05d}.jpg').convert('RGB').resize((PW, int(PW * 1688 / 780)))
    sc = sc.crop((0, 0, PW, PH))
    im = bg.copy(); im.paste(frame, (PX - 18, PY - 18), frame); im.paste(sc, (PX, PY), mask)
    im.save(f'{W}/ph/{i:04d}.jpg', quality=88)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{W}/ph/%04d.jpg', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', W + '/phone.mp4'], check=True)
# 4 splice: dump[0,10.6] + phone + dump[10.6,end]
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', W + '/dump.mp4', '-i', W + '/phone.mp4', '-filter_complex',
                '[0:v]trim=0:10.6,setpts=PTS-STARTPTS[a];[0:v]trim=start=10.6,setpts=PTS-STARTPTS[c];[1:v]setpts=PTS-STARTPTS[b];[a][b][c]concat=n=3:v=1[v]',
                '-map', '[v]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-movflags', '+faststart', out], check=True)
base = os.path.splitext(out)[0]
for f in os.listdir(os.path.dirname(out) or '.'):
    pass
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout)
ims = []
for t in [1.3, 3.8, 8.0, 11.5, 14.5, 17.5, dur - 3.4, dur - 1.0]:
    fp = f'{W}/chk{t}.jpg'; subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', out, '-frames:v', '1', '-vf', 'scale=270:-1', fp]); ims.append(Image.open(fp))
S = Image.new('RGB', (270 * len(ims), 480), 'white'); [S.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; S.save(base + '-check.jpg')
shutil.rmtree(W); print('ok', out, round(dur, 1))
