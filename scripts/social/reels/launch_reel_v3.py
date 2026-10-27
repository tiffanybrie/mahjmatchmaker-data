"""Timing: "is HERE" slams at exactly 0:16 (song drop goes there); card burst on a 120 bpm grid (0.5s).
Launch-day reel v3 (Oct 27, Tiffany 2:11-2:13am): the ever-burning question -> 3-2-1 countdown -> "Find Your
Mat-ch is HERE." -> burst of match cards -> her own screen recording (1.5x max, never faster) framed in navy with a
running stopwatch -> "Matched." -> end card. Navy/cream with pink as the accent (v2 was "so pink"), every line held
long enough to read, title on one line, everything centred. Silent: her song goes on in Instagram.
Usage: python3 launch_reel_v3.py <body.mp4 cut+cropped 1080x1920 real speed> <cards_dir> <out.mp4>"""
import os, sys, asyncio, subprocess, glob, random
R = '/home/claude/mahjmatchmaker-data'
F = f'file://{R}/scripts/social/tileprofile/fonts/'
u = lambda p: f'file://{R}/{p}'
FPS = 30
FR = os.environ.get('FR', '/tmp/launchv3'); os.makedirs(FR, exist_ok=True)
NAVY, PINK, CREAM, BLUSH = '#062a55', '#e0547f', '#fdf6ee', '#f7b6c8'
FYM = ('Find <span class="pf">Your</span> Mat&#8209;ch<sup style="font-size:.32em;vertical-align:super">&trade;</sup>')
CSS = f"""<style>@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:Bit;font-weight:700;src:url({F}bitter-latin-700-normal.woff2)}}
@font-face{{font-family:Bit;font-weight:600;src:url({F}bitter-latin-600-normal.woff2)}}@font-face{{font-family:PF;font-style:italic;src:url({F}playfair-display-latin-600-italic.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
.w{{position:relative;width:1080px;height:1920px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px;overflow:hidden}}
.cap{{font-family:Cap;line-height:1.04}}.pf{{font-family:PF;font-style:italic;font-weight:600}}.it{{font:italic 600 60px/1.3 PF}}
.a{{opacity:0;animation-fill-mode:forwards;animation-timing-function:cubic-bezier(.2,.8,.2,1)}}
@keyframes up{{0%{{transform:translateY(70px);opacity:0}}100%{{transform:none;opacity:1}}}}
@keyframes pop{{0%{{transform:scale(.3);opacity:0}}60%{{transform:scale(1.1);opacity:1}}100%{{transform:scale(1);opacity:1}}}}
@keyframes slam{{0%{{transform:scale(2.4);opacity:0}}45%{{transform:scale(.94);opacity:1}}70%{{transform:scale(1.03)}}100%{{transform:scale(1);opacity:1}}}}
@keyframes num{{0%{{transform:scale(2.2);opacity:0}}25%{{transform:scale(1);opacity:1}}80%{{transform:scale(.92);opacity:1}}100%{{transform:scale(.6);opacity:0}}}}
@keyframes ring{{0%{{transform:scale(.4);opacity:.9}}100%{{transform:scale(2.6);opacity:0}}}}
@keyframes land{{0%{{transform:translateY(900px) rotate(var(--r0));opacity:1}}100%{{transform:translateY(0) rotate(var(--r));opacity:1}}}}
@keyframes pulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.05)}}}}
@keyframes spark{{0%{{transform:translate(0,0) scale(.2);opacity:0}}20%{{opacity:1}}100%{{transform:translate(var(--x),var(--y)) scale(1);opacity:0}}}}
</style>"""
HEART = '<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="{c}"/></svg>'
def page(bg, body): return f'<!doctype html><html><head><meta charset=utf8>{CSS}</head><body><div class="w" style="background:{bg}">{body}</div></body></html>'
random.seed(7)
def sparks(t0, cx=540, cy=960, n=18):
    out = []
    for k in range(n):
        import math
        ang = k / n * 6.283 + random.random() * .3; dist = random.randint(380, 620); w = random.randint(44, 90)
        out.append(f'<div class="a" style="position:absolute;left:{cx-w//2}px;top:{cy-w//2}px;width:{w}px;height:{w}px;--x:{int(math.cos(ang)*dist)}px;--y:{int(math.sin(ang)*dist)}px;animation:spark 1.3s {t0+random.random()*.15:.2f}s ease-out forwards">'
                   f'{HEART.format(c=random.choice([PINK, BLUSH, "#fff", "#f6c66b"]))}</div>')
    return ''.join(out)
TILE = u('assets/tiles/album/cypress.jpg'); MAT = u('assets/mats/gallery/britt-mills--knox.webp')

SCENES = []   # (name, html, secs)
SCENES.append(('q1', page(NAVY, f'<div class="a it" style="color:{BLUSH};font-size:70px;margin-bottom:40px;animation:up .5s .1s forwards">Presenting&hellip;</div>'
                           f'<div class="a cap" style="font-size:132px;color:#fff;animation:up .6s .5s forwards">The ever&#8209;burning question.</div>'), 3.4))
SCENES.append(('q2', page(CREAM, f'<img class="a" src="{TILE}" style="width:440px;height:440px;object-fit:cover;border-radius:50%;border:14px solid #fff;box-shadow:0 22px 50px rgba(6,42,85,.25);margin-bottom:70px;animation:pop .6s .05s forwards">'
                            f'<div class="a cap" style="font-size:116px;color:{NAVY};animation:up .6s .45s forwards">What mat goes with <span style="color:{PINK}">these</span> tiles?</div>'), 3.6))
SCENES.append(('q3', page(NAVY, f'<div class="a cap" style="font-size:104px;color:#fff;animation:up .55s .1s forwards">Asked in every mahj group.</div>'
                            f'<div class="a cap" style="font-size:104px;color:{BLUSH};margin-top:50px;animation:up .55s .9s forwards">Every. Single. Day.</div>'), 3.8))
SCENES.append(('q4', page(CREAM, f'<div class="a cap" style="font-size:150px;color:{NAVY};animation:slam .6s .1s forwards">Not anymore.</div>'), 1.8))
cd = ''.join(f'<div class="a cap" style="position:absolute;font-size:520px;color:#fff;animation:num .8s {i*.8:.1f}s forwards">{n}</div>'
             f'<div class="a" style="position:absolute;width:520px;height:520px;border-radius:50%;border:16px solid {PINK};animation:ring .8s {i*.8:.1f}s forwards"></div>' for i, n in enumerate('321'))
SCENES.append(('cd', page(NAVY, cd), 2.4))
SCENES.append(('here', page(NAVY, sparks(.15) + f'<img class="a" src="{u("assets/brand/flame-heart.png")}" style="width:170px;margin-bottom:50px;animation:pop .5s 0s forwards">'
                              f'<div class="a cap" style="font-size:96px;color:#fff;white-space:nowrap;animation:slam .6s .05s forwards">{FYM}</div>'
                              f'<div class="a cap" style="font-size:210px;color:{PINK};margin-top:30px;animation:slam .6s 1.0s forwards">is HERE.</div>'
                              f'<div class="a" style="font:700 40px Bit;color:{BLUSH};letter-spacing:.12em;margin-top:60px;animation:up .5s 1.6s forwards">10.27 &middot; MAHJMATCHMAKER.COM</div>'), 3.8))

async def shoot(pg, name, html, secs):
    hp = f'{FR}/{name}.html'; open(hp, 'w').write(html)
    await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
    d = f'{FR}/{name}'; os.makedirs(d, exist_ok=True)
    await pg.evaluate('document.getAnimations().forEach(a=>a.pause())')
    for i in range(int(secs * FPS)):
        await pg.evaluate(f'document.getAnimations().forEach(a=>{{a.currentTime={i * 1000 / FPS}}})')
        await pg.screenshot(path=f'{d}/{i:04d}.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{d}/%04d.png', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', f'{d}.mp4'], check=True)
    return f'{d}.mp4'

def run(c): subprocess.run(c, check=True)
def dur(p): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).decode())

async def main(body, cards_dir, out):
    cards = sorted(glob.glob(f'{cards_dir}/*'))
    deck = ''.join(f'<img class="a" src="file://{c}" style="position:absolute;width:900px;border-radius:36px;box-shadow:0 30px 70px rgba(0,0,0,.45);'
                   f'--r0:{random.randint(-25,25)}deg;--r:{random.choice([-7,-5,-3,3,5,7])}deg;animation:land .38s {i*.5:.2f}s cubic-bezier(.2,.9,.25,1.05) forwards">' for i, c in enumerate(cards))
    burst = page(NAVY, deck + f'<div class="a cap" style="position:absolute;left:0;right:0;bottom:120px;font-size:80px;color:#fff;text-shadow:0 6px 24px rgba(0,0,0,.5);animation:up .5s {len(cards)*.5:.2f}s forwards">Matched across brands.</div>')
    watch = page(CREAM, f'<div class="a it" style="color:{PINK};font-size:66px;margin-bottom:40px;animation:up .5s .1s forwards">Watch me match</div>'
                        f'<img class="a" src="{TILE}" style="width:380px;height:380px;object-fit:cover;border-radius:50%;border:14px solid #fff;box-shadow:0 22px 50px rgba(6,42,85,.25);animation:pop .6s .35s forwards">'
                        f'<div class="a cap" style="font-size:120px;color:{NAVY};margin-top:50px;animation:up .55s .6s forwards">my Cypress tiles.</div>'
                        f'<div class="a" style="font:700 42px Bit;color:{NAVY};opacity:.75;margin-top:44px;letter-spacing:.06em;animation:up .5s 1.2s forwards">Stopwatch on.</div>'), 3.0
    secs_real = int(dur(body))
    done = page(NAVY, sparks(.2) + f'<div class="a cap" style="font-size:180px;color:#fff;animation:slam .6s .05s forwards">Matched.</div>'
                               f'<div style="display:flex;gap:40px;align-items:center;margin-top:60px">'
                               f'<div class="a" style="width:300px;height:300px;border-radius:50%;background:url({TILE}) center/cover;box-shadow:0 0 0 12px #fff;animation:pop .5s .5s forwards"></div>'
                               f'<div class="a" style="width:110px;height:110px;animation:pop .5s .75s forwards">{HEART.format(c=PINK)}</div>'
                               f'<div class="a" style="width:300px;height:300px;border-radius:50%;background:url({MAT}) center/cover;box-shadow:0 0 0 12px #fff;animation:pop .5s 1s forwards"></div></div>'
                               f'<div class="a" style="font:700 52px/1.35 Bit;color:{BLUSH};margin-top:70px;animation:up .5s 1.4s forwards">Tiles, mat &amp; racks in under 2 minutes.<br>Tutorial and all.</div>'), 3.6
    end = page(CREAM, f'<img class="a" src="{u("assets/brand/mahjmatchmaker-wordmark-notag.png")}" style="width:720px;animation:up .55s .1s forwards">'
                      f'<div class="a cap" style="font-size:150px;color:{NAVY};margin-top:80px;animation:slam .6s .45s forwards">Never ask again.</div>'
                      f'<div class="a" style="margin-top:80px;animation:pop .6s 1.0s forwards"><div style="background:{NAVY};color:#fff;border-radius:999px;padding:34px 60px;font-family:Cap;font-size:76px;white-space:nowrap;animation:pulse 1.2s 1.8s ease-in-out infinite">{FYM}</div></div>'
                      f'<div class="a" style="font:700 50px Bit;color:{PINK};margin-top:56px;letter-spacing:.06em;animation:up .5s 1.5s forwards">LINK IN BIO</div>'
                      f'<div class="a" style="font:600 40px Bit;color:{NAVY};margin-top:24px;animation:up .5s 1.8s forwards">mahjmatchmaker.com &middot; code MAHJMATCH</div>'), 4.6
    from playwright.async_api import async_playwright
    clips = []
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page(viewport={'width': 1080, 'height': 1920})
        for n, h, s in SCENES: clips.append(await shoot(pg, n, h, s))
        clips.append(await shoot(pg, 'burst', burst, len(cards) * .5 + 2.0))
        clips.append(await shoot(pg, 'watch', *watch))
        rec_slot = len(clips); clips.append(None)
        clips.append(await shoot(pg, 'done', *done)); clips.append(await shoot(pg, 'end', *end))
        await br.close()
    # recording: 1.5x, framed on navy with a stopwatch band (real elapsed time of the recording)
    from PIL import Image, ImageDraw, ImageFont
    sw = f'{FR}/sw'; os.makedirs(sw, exist_ok=True)
    fnt = ImageFont.truetype(f'{R}/scripts/social/tileprofile/fonts/Caprasimo.ttf', 78)
    lst = open(f'{FR}/sw.txt', 'w')
    for s in range(secs_real + 1):
        im = Image.new('RGBA', (1080, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((330, 30, 750, 150), 60, fill=(224, 84, 127, 255))
        d.ellipse((372, 58, 432, 118), outline='white', width=7); d.rectangle((394, 44, 410, 54), fill='white'); d.line((402, 88, 402, 70), fill='white', width=6); d.line((402, 88, 416, 96), fill='white', width=6)
        d.text((585, 92), f'{s // 60}:{s % 60:02d}', font=fnt, fill='white', anchor='mm')
        im.save(f'{sw}/{s:04d}.png'); lst.write(f"file '{sw}/{s:04d}.png'\nduration {1/1.5:.4f}\n")
    lst.close()
    rec = f'{FR}/rec.mp4'
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', body, '-f', 'concat', '-safe', '0', '-i', f'{FR}/sw.txt', '-filter_complex',
         f'[0:v]setpts=PTS/1.5,fps=30,scale=960:1707[v];color=c={NAVY}:s=1080x1920:r=30[bg];[bg][v]overlay=60:185:shortest=1[b];[1:v]fps=30,format=rgba[s];[b][s]overlay=0:5:eof_action=repeat[o]',
         '-map', '[o]', '-an', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', rec])
    clips[rec_slot] = rec
    with open(f'{FR}/all.txt', 'w') as f:
        for c in clips: f.write(f"file '{c}'\n")
    run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{FR}/all.txt', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', out])
asyncio.run(main(*sys.argv[1:4])); print('ok')
