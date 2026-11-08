import json, os, subprocess, shutil, sys
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__))
OUT = '/tmp/claude-0/-home-claude/f4da3022-6ec8-595a-90aa-668aea191899/scratchpad/pin'
covers = ['file://' + f for f in json.load(open(D + '/order2.json'))]  # v2: REAL album covers (uniform-v3 had the old tagline + squashed Bam Bird logo)
open(OUT + '/r.html', 'w').write(open(D + '/tpl_pin2.html').read().replace('__COV__', json.dumps(covers)))
fd = OUT + '/f'
if os.path.isdir(fd): shutil.rmtree(fd)
os.makedirs(fd)
FPS, DUR = 30, 19.6
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + OUT + '/r.html'); pg.wait_for_timeout(2500)
    for n in range(int(round(FPS * DUR))):
        pg.evaluate(f"render({n / FPS})"); pg.wait_for_timeout(10)
        pg.screenshot(path=f'{fd}/{n:04d}.jpg', type='jpeg', quality=92)
    b.close()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', fd + '/%04d.jpg', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', OUT + '/teaser.mp4'], check=True)
print('done')
