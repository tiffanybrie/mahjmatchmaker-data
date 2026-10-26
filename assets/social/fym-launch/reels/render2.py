import json, os, subprocess, shutil
from playwright.sync_api import sync_playwright
D = '/home/claude/reel1'
order = json.load(open(D + '/order.json'))
covers = ['file:///home/claude/mahjmatchmaker-data/assets/covers/albums/uniform-v3/' + f for f in order]
open(D + '/r2.html', 'w').write(open(D + '/tpl2.html').read().replace('__COV__', json.dumps(covers)))
fd = D + '/f2'
if os.path.isdir(fd): shutil.rmtree(fd)
os.makedirs(fd)
FPS, DUR = 24, 26.5
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + D + '/r2.html'); pg.wait_for_timeout(2500)
    for n in range(int(FPS * DUR)):
        pg.evaluate(f"render({n / FPS})"); pg.wait_for_timeout(12)
        pg.screenshot(path=f'{fd}/{n:04d}.jpg', type='jpeg', quality=90)
    b.close()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', fd + '/%04d.jpg', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', D + '/reel1-hype-v2.mp4'], check=True)
print('done')
