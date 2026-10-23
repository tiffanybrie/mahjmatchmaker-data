import json, os, random, subprocess
from playwright.sync_api import sync_playwright
D = '/home/claude/reel1'
covers = [l.strip() for l in open(D + '/covers.txt') if l.strip()]
random.seed(4); random.shuffle(covers)
html = open(D + '/tpl.html').read().replace('__COV__', json.dumps(['file://' + c for c in covers]))
open(D + '/r.html', 'w').write(html)
os.makedirs(D + '/f', exist_ok=True)
FPS, DUR = 24, 18.8
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + D + '/r.html'); pg.wait_for_timeout(1500)
    # preload covers
    pg.evaluate("Promise.all(COV.map(s=>new Promise(r=>{const i=new Image();i.onload=r;i.onerror=r;i.src=s})))")
    for n in range(int(FPS * DUR)):
        pg.evaluate(f"render({n / FPS})")
        pg.wait_for_timeout(15)
        pg.screenshot(path=f'{D}/f/{n:04d}.jpg', type='jpeg', quality=90)
    b.close()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', D + '/f/%04d.jpg', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', D + '/reel1-hype.mp4'], check=True)
print('done')
