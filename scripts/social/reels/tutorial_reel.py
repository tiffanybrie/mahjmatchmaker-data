"""Tutorial reel (Oct 27, Tiffany): her own phone screen recording of the FYM tour, at 1.5x (never faster; 5x was
rejected), Marigold + Rattan left-swipes cut, browser bars cropped, with a branded intro ("Introducing Find Your
Mat-ch") and the brand end card. Silent: she adds her song by hand in Instagram.
Usage: python3 tutorial_reel.py <body.mp4 (already cut+cropped, 1080x1920)> <out.mp4>"""
import os, sys, asyncio, subprocess, importlib.util
R = '/home/claude/mahjmatchmaker-data'
spec = importlib.util.spec_from_file_location('b', R + '/scripts/social/titlecards/build.py'); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
u, HEAD = b.u, b.HEAD
FPS = 30
FR = os.environ.get('FR', '/tmp/tutreel'); os.makedirs(FR, exist_ok=True)
HEART = '<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="{c}"/></svg>'
STYLE = """<style>
@keyframes pop{0%{transform:scale(.2);opacity:0}60%{transform:scale(1.12);opacity:1}100%{transform:scale(1);opacity:1}}
@keyframes up{0%{transform:translateY(60px);opacity:0}100%{transform:none;opacity:1}}
@keyframes bounce{0%{transform:scale(.3);opacity:0}55%{transform:scale(1.1);opacity:1}75%{transform:scale(.96)}100%{transform:scale(1);opacity:1}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
.a{opacity:0;animation-fill-mode:forwards;animation-timing-function:cubic-bezier(.2,.8,.2,1)}
</style>"""
FYM = 'Find <i>Your</i> Mat-ch<sup style="font-size:.35em;vertical-align:super;font-style:normal">&trade;</sup>'
FYM_NOTM = 'Find <i>Your</i> Mat-ch'
COL_L, COL_W = 90, 770
TILE = u('assets/tiles/album/cypress.jpg'); MAT = u('assets/mats/gallery/britt-mills--knox.webp')
def pair(top, delay):
    return (f'<div class="a" style="position:absolute;left:{COL_L}px;width:{COL_W}px;top:{top}px;display:flex;justify-content:center;align-items:center;gap:34px;animation:up .6s {delay}s forwards">'
            f'<div style="width:240px;height:240px;border-radius:50%;background:url({TILE}) center/cover;box-shadow:0 0 0 10px #fff,0 14px 30px rgba(6,42,85,.16)"></div>'
            f'<div style="width:100px;height:100px">{HEART.format(c="#f56c8c")}</div>'
            f'<div style="width:240px;height:240px;border-radius:50%;background:url({MAT}) center/cover;box-shadow:0 0 0 10px #fff,0 14px 30px rgba(6,42,85,.16)"></div></div>')
BG = """<div style="position:absolute;right:-200px;top:-180px;width:700px;height:700px;border-radius:50%;background:#f9d3df"></div>
  <div style="position:absolute;left:-220px;bottom:-200px;width:760px;height:760px;border-radius:50%;background:#f6e9df"></div>"""
INTRO = HEAD + STYLE + f"""<div class="wrap" style="background:#fbe3ea;color:#d6336c;justify-content:flex-start;padding:0">{BG}
  <div style="position:absolute;left:{COL_L}px;top:230px;width:{COL_W}px;display:flex;flex-direction:column;align-items:center">
  <img class="a" src="{u('assets/brand/flame-heart.png')}" style="width:150px;animation:pop .6s .05s forwards">
  <div class="a" style="font:italic 600 72px Lo;color:#062a55;margin-top:50px;animation:up .5s .3s forwards">Introducing</div>
  <div class="line a" style="font-size:118px;margin-top:24px;line-height:1.05;animation:up .55s .6s forwards">{FYM}</div>
  <div class="a" style="font:600 50px Bit;color:#062a55;margin-top:56px;line-height:1.3;animation:up .5s 1.1s forwards">Pick your tiles. Swipe the mats.<br>Add racks. It&rsquo;s a match.</div>
  <div class="a" style="font:600 40px Bit;color:#d6336c;margin-top:48px;letter-spacing:.04em;animation:up .5s 1.6s forwards">Watch me match my Cypress tiles &darr;</div>
  </div>{pair(1236, 2.0)}
</div></body></html>"""
END = HEAD + STYLE + f"""<div class="wrap" style="background:#fbe3ea;color:#d6336c;justify-content:flex-start;padding:0">{BG}
  <div style="position:absolute;left:{COL_L}px;top:190px;width:{COL_W}px;display:flex;flex-direction:column;align-items:center">
  <img class="a" src="{u('assets/brand/flame-heart.png')}" style="width:150px;animation:pop .6s .1s forwards">
  <img class="a" src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="width:700px;margin-top:40px;animation:up .55s .45s forwards">
  <div class="line a" style="font-size:86px;margin-top:48px;line-height:1.1;animation:up .55s .8s forwards">Hooking up <i>tiles,</i><br><i>mats</i> &amp; <i>racks.</i></div>
  <div class="a" style="margin-top:78px;animation:bounce .7s 1.35s forwards"><div style="background:#062a55;color:#fff;border-radius:999px;padding:32px 56px;font:700 68px Lo;white-space:nowrap;animation:pulse 1.2s 2.1s ease-in-out infinite">{FYM}</div></div>
  <div class="a" style="font:600 46px Bit;color:#062a55;margin-top:42px;letter-spacing:.04em;white-space:nowrap;animation:up .5s 1.9s forwards">Link in bio &middot; mahjmatchmaker.com</div>
  <div class="a" style="margin-top:44px;background:#fff;border-radius:22px;padding:18px 32px;font:700 38px Bit;color:#062a55;white-space:nowrap;box-shadow:0 8px 20px rgba(6,42,85,.1);animation:up .5s 2.35s forwards">Code <span style="color:#d6336c">MAHJMATCH</span> at our partner brands</div>
  </div>{pair(1300, 2.6)}
</div></body></html>"""

async def shoot(page, html, name, secs, t0=0):
    hp = f'{FR}/{name}.html'; open(hp, 'w').write(html)
    await page.goto('file://' + hp); await page.wait_for_load_state('networkidle'); await page.evaluate('document.fonts.ready')
    d = f'{FR}/{name}'; os.makedirs(d, exist_ok=True)
    await page.evaluate('document.getAnimations().forEach(a=>a.pause())')
    for i in range(int(secs * FPS)):
        await page.evaluate(f'document.getAnimations().forEach(a=>{{a.currentTime={t0 + i * 1000 / FPS}}})')
        await page.screenshot(path=f'{d}/{i:04d}.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{d}/%04d.png', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', f'{d}.mp4'], check=True)
    return f'{d}.mp4'

async def main(body, out):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page(viewport={'width': 1080, 'height': 1920})
        i = await shoot(pg, INTRO, 'intro', 3.6, t0=150); e = await shoot(pg, END, 'end', 4.8, t0=300)
        await br.close()
    fast = f'{FR}/body15.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', body, '-an', '-vf', 'setpts=PTS/1.5,fps=30', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', fast], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', i, '-i', fast, '-i', e, '-filter_complex',
                    '[0:v]setsar=1[a];[1:v]setsar=1[b];[2:v]setsar=1[c];[a][b]xfade=transition=fade:duration=0.4:offset=3.2[ab];[ab][c]xfade=transition=fade:duration=0.4:offset=PLACEHOLDER[v]'
                    .replace('PLACEHOLDER', str(round(3.2 + float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', fast]).decode()) - 0.4, 2))),
                    '-map', '[v]', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], check=True)
    for nm in ('intro', 'end'):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-sseof', '-0.1', '-i', f'{FR}/{nm}.mp4', '-frames:v', '1', f'{FR}/{nm}-last.png'])
asyncio.run(main(sys.argv[1], sys.argv[2])); print('ok')
