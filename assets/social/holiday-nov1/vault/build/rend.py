import sys,os,subprocess,shutil
from playwright.sync_api import sync_playwright
html,out=sys.argv[1],sys.argv[2]; mode=sys.argv[3]  # 'stills' t1,t2.. or 'video' dur fps
with sync_playwright() as p:
    b=p.chromium.launch(args=['--allow-file-access-from-files'])
    pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file://'+html); pg.evaluate('window.ready'); pg.wait_for_timeout(800)
    if mode=='stills':
        for t in sys.argv[4].split(','):
            pg.evaluate(f'render({t})'); pg.wait_for_timeout(60)
            pg.screenshot(path=f'{out}/s_{float(t):05.2f}.jpg',type='jpeg',quality=80)
    else:
        dur,fps=float(sys.argv[4]),int(sys.argv[5]); fd=out+'/frames'
        if os.path.isdir(fd): shutil.rmtree(fd)
        os.makedirs(fd)
        for n in range(int(round(dur*fps))):
            pg.evaluate(f'render({n/fps})'); pg.wait_for_timeout(8)
            pg.screenshot(path=f'{fd}/{n:04d}.jpg',type='jpeg',quality=92)
    b.close()
