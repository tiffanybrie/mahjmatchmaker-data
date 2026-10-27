"""Launch reel v5 (Oct 27 9am: cross-brand Sunday tiles x Brownstone Bloom mat, Walnut + Oak racks). Based on v4 (Oct 27, Tiffany's 3:29am brief). ONE match all the way through: Brownstone Bloom tiles (Anders Ruff).
Hype: ever-burning question -> catalog wall in motion (800+ mats, 300+ tile sets, 50+ brands) -> 3-2-1 -> "Find Your Mat-ch
is HERE." (slam lands at exactly 0:16 = the song's drop) -> "Today, YOU are the matchmaker." -> every step of the tool on
real app screens (pick tiles, swipe mats, suitors, pick one, racks with the mat zoomed on top, make it official, match
card, shop + code MAHJMATCH) -> end card. Cuts on a 120 bpm grid (0.5s). CALM=1 renders the calmer-but-cool cut (slower,
no countdown, soft fades). Silent: her song goes on in Instagram.
Usage: python3 launch_reel_v4.py <wall.mp4> <out.mp4>"""
import os, sys, asyncio, subprocess
R = '/home/claude/mahjmatchmaker-data'; F = f'file://{R}/scripts/social/tileprofile/fonts/'
CAP = f'{R}/assets/social/fym-launch/sunday-flow'
u = lambda p: 'file://' + (p if p.startswith('/') else f'{CAP}/{p}')
CALM = os.environ.get('CALM') == '1'; K = 1.35 if CALM else 1.0
FPS = 30; FR = os.environ.get('FR', '/tmp/reelv5' + ('c' if CALM else '')); os.makedirs(FR, exist_ok=True)
NAVY, PINK, CREAM, BLUSH, INK = '#062a55', '#e0547f', '#fdf6ee', '#f7b6c8', '#4a3d58'
FYM = 'Find <span class="pf">Your</span> Mat&#8209;ch<sup style="font-size:.32em;vertical-align:super">&trade;</sup>'
CSS = f"""<style>@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:Bit;font-weight:700;src:url({F}bitter-latin-700-normal.woff2)}}
@font-face{{font-family:PF;font-style:italic;src:url({F}playfair-display-latin-600-italic.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
.w{{position:relative;width:1080px;height:1920px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px;overflow:hidden}}
.cap{{font-family:Cap;line-height:1.04}}.pf{{font-family:PF;font-style:italic;font-weight:600}}.it{{font:italic 600 60px/1.3 PF}}
.a{{opacity:0;animation-fill-mode:forwards;animation-timing-function:cubic-bezier(.2,.8,.2,1)}}
@keyframes up{{0%{{transform:translateY(70px);opacity:0}}100%{{transform:none;opacity:1}}}}
@keyframes fade{{0%{{opacity:0}}100%{{opacity:1}}}}
@keyframes pop{{0%{{transform:scale(.3);opacity:0}}60%{{transform:scale(1.1);opacity:1}}100%{{transform:scale(1);opacity:1}}}}
@keyframes slam{{0%{{transform:scale(2.4);opacity:0}}45%{{transform:scale(.94);opacity:1}}70%{{transform:scale(1.03)}}100%{{transform:scale(1);opacity:1}}}}
@keyframes num{{0%{{transform:scale(2.2);opacity:0}}25%{{transform:scale(1);opacity:1}}80%{{transform:scale(.92);opacity:1}}100%{{transform:scale(.6);opacity:0}}}}
@keyframes ring{{0%{{transform:scale(.4);opacity:.9}}100%{{transform:scale(2.6);opacity:0}}}}
@keyframes rise{{0%{{transform:translateY(500px) rotate(var(--r,0deg));opacity:0}}100%{{transform:translateY(0) rotate(var(--r,0deg));opacity:1}}}}
@keyframes scroll{{0%{{transform:translateY(0)}}100%{{transform:translateY(var(--dy))}}}}
@keyframes zoomin{{0%{{transform:scale(1)}}100%{{transform:scale(var(--z,1.18))}}}}
@keyframes stamp{{0%{{transform:scale(2.6) rotate(var(--r));opacity:0}}40%{{transform:scale(.9) rotate(var(--r));opacity:1}}60%{{transform:scale(1.05) rotate(var(--r))}}100%{{transform:scale(1) rotate(var(--r));opacity:1}}}}
@keyframes flyR{{0%{{transform:none}}100%{{transform:translateX(900px) rotate(18deg);opacity:0}}}}
@keyframes flyL{{0%{{transform:none}}100%{{transform:translateX(-900px) rotate(-18deg);opacity:0}}}}
@keyframes pulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.05)}}}}
@keyframes spark{{0%{{transform:translate(0,0) scale(.2);opacity:0}}20%{{opacity:1}}100%{{transform:translate(var(--x),var(--y)) scale(1);opacity:0}}}}
.step{{position:absolute;top:150px;left:0;right:0;text-align:center;z-index:9}}
.step b{{display:inline-block;background:{PINK};color:#fff;font:700 34px Bit;letter-spacing:.14em;padding:12px 26px;border-radius:40px}}
.step div{{font-family:Cap;font-size:92px;line-height:1.02;margin-top:22px}}
.call{{position:absolute;z-index:12;background:{PINK};color:#fff;font:700 40px/1.2 Bit;padding:18px 28px;border-radius:26px;box-shadow:0 14px 30px rgba(0,0,0,.25);text-align:left}}
</style>"""
HEART = '<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="{c}"/></svg>'
def page(bg, body, fg=NAVY): return f'<!doctype html><html><head><meta charset=utf8>{CSS}</head><body><div class="w" style="background:{bg};color:{fg}">{body}</div></body></html>'
import random, math; random.seed(5)
def sparks(t0, cx=540, cy=960, n=18):
    out = []
    for k in range(n):
        ang = k / n * 6.283 + random.random() * .3; d = random.randint(380, 620); w = random.randint(44, 90)
        out.append(f'<div class="a" style="position:absolute;left:{cx-w//2}px;top:{cy-w//2}px;width:{w}px;height:{w}px;--x:{int(math.cos(ang)*d)}px;--y:{int(math.sin(ang)*d)}px;animation:spark 1.3s {t0+random.random()*.15:.2f}s ease-out forwards">{HEART.format(c=random.choice([PINK, BLUSH, "#fff", "#f6c66b"]))}</div>')
    return ''.join(out)
def phone(img, w=700, x=None, top=520, crop=0, dy=0, delay=0.0, dur=1.0, extra='', z=2, rot=0):
    x = (1080 - w) // 2 if x is None else x; h = w * 2.06; p = w * .034; sw = w - 2 * p; k = sw / 390
    scr = f'--dy:{-dy*k:.0f}px;animation:scroll {dur:.2f}s {delay+0.45:.2f}s ease-in-out forwards' if dy else ''
    return (f'<div class="a" style="position:absolute;left:{x}px;top:{top}px;width:{w}px;height:{h}px;z-index:{z};--r:{rot}deg;animation:rise .5s {delay:.2f}s cubic-bezier(.2,.9,.25,1.05) forwards">'
            f'<div style="position:absolute;inset:0;border-radius:{w*.16}px;background:#f7f7f5;box-shadow:0 40px 90px rgba(0,0,0,.35),inset 0 0 0 {w*.006}px #d6d6d3;padding:{p}px">'
            f'<div style="position:relative;width:100%;height:100%;border-radius:{w*.13}px;overflow:hidden;background:#fff">'
            f'<div style="height:{w*.13:.0f}px;background:#fff"></div><div style="margin-top:-{crop*k:.0f}px;{scr}"><img src="{u(img)}" style="width:100%;display:block"></div>{extra}</div>'
            f'<div style="position:absolute;left:50%;top:{w*.045}px;transform:translateX(-50%);width:{w*.28}px;height:{w*.08}px;background:#000;border-radius:{w*.05}px"></div></div></div>')
def stamp(kind, t, x, y):
    if kind == 'yes': return f'<div class="a" style="position:absolute;left:{x}px;top:{y}px;width:200px;height:200px;z-index:20;--r:-12deg;animation:stamp .45s {t:.2f}s forwards">{HEART.format(c=PINK)}</div>'
    return f'<div class="a" style="position:absolute;left:{x}px;top:{y}px;z-index:20;--r:12deg;font:400 170px Cap;color:#fff;background:#7a6a85;width:200px;height:200px;border-radius:50%;display:grid;place-items:center;animation:stamp .45s {t:.2f}s forwards">&#10005;</div>'
def step(n, t): return f'<div class="step"><b>STEP {n}</b><div class="a" style="animation:up .45s .05s forwards">{t}</div></div>'
TILE = f'{R}/assets/tiles/album/sunday-tile-set-hd.jpg'; MAT = f'{R}/assets/mats/gallery/anders-ruff--brownstone-bloom-mahjong-mat.webp'
def rect(src, t, w, h, rot=0, fit='cover'): return f'<img class="a" src="{u(src)}" style="width:{w}px;height:{h}px;object-fit:{fit};border-radius:24px;border:12px solid #fff;background:#fff;box-shadow:0 26px 60px rgba(0,0,0,.3);margin-bottom:60px;--r:{rot}deg;animation:rise .6s {t:.2f}s cubic-bezier(.2,.9,.25,1.05) forwards">'
def circle(src, t, size=480): return f'<img class="a" src="{u(src)}" style="width:{size}px;height:{size}px;object-fit:cover;border-radius:50%;border:14px solid #fff;box-shadow:0 22px 50px rgba(0,0,0,.3);margin-bottom:60px;animation:pop .6s {t:.2f}s forwards">'

S = []  # (name, html, secs)
S.append(('q1', page(NAVY, f'<div class="a cap" style="font-size:150px;color:#fff;animation:up .55s .1s forwards">The ever&#8209;burning question.</div>', '#fff'), 2.0*K))
S.append(('q2', page(CREAM, rect(TILE, .05, 640, 560, -3) + f'<div class="a cap" style="font-size:118px;animation:up .5s .3s forwards">What mat goes with <span style="color:{PINK}">these</span> tiles?</div>'), 2.5*K))
S.append(('q3', page(CREAM, rect(MAT, .05, 660, 660, 3, 'contain') + f'<div class="a cap" style="font-size:118px;animation:up .5s .3s forwards">What tiles go with <span style="color:{PINK}">this</span> mat?</div>'), 2.0*K))
S.append(('q4', page(NAVY, f'<div class="a cap" style="font-size:100px;color:#fff;animation:up .5s .05s forwards">Asked in every mahj Facebook group.</div><div class="a cap" style="font-size:112px;color:{BLUSH};margin-top:50px;animation:slam .5s .9s forwards">Every. Single. Day.</div>', '#fff'), 2.5*K))
WALL_AT = len(S)
if not CALM:
    cd = ''.join(f'<div class="a cap" style="position:absolute;font-size:520px;color:#fff;animation:num .5s {i*.5:.1f}s forwards">{n}</div><div class="a" style="position:absolute;width:520px;height:520px;border-radius:50%;border:16px solid {PINK};animation:ring .5s {i*.5:.1f}s forwards"></div>' for i, n in enumerate('321'))
    S.append(('cd', page(NAVY, cd), 1.5))
here_d = 1.0 if not CALM else 0.6
S.append(('here', page(NAVY, sparks(here_d - .05) + f'<img class="a" src="{u(R+"/assets/brand/flame-heart.png")}" style="width:170px;margin-bottom:50px;animation:pop .5s 0s forwards"><div class="a cap" style="font-size:96px;color:#fff;white-space:nowrap;animation:{"slam .6s .05s" if not CALM else "up .6s .05s"} forwards">{FYM}</div><div class="a cap" style="font-size:210px;color:{PINK};margin-top:30px;animation:{"slam" if not CALM else "pop"} .6s {here_d}s forwards">is HERE.</div><div class="a" style="font:700 40px Bit;color:{BLUSH};letter-spacing:.12em;margin-top:60px;animation:up .5s {here_d+.6:.1f}s forwards">10.27 &middot; MAHJMATCHMAKER.COM</div>', '#fff'), 3.0*K))
S.append(('you', page(CREAM, f'<div class="a it" style="color:{PINK};font-size:62px;animation:up .5s .05s forwards">Mahj Matchmaker 2.0</div><div class="a cap" style="font-size:118px;margin-top:30px;animation:up .55s .3s forwards">Today,<br><span style="color:{PINK}">you&rsquo;re</span> the<br>matchmaker.</div><div class="a" style="font:700 42px Bit;margin-top:60px;animation:up .5s .9s forwards">One match. Four brands. Watch &darr;</div>'), 2.5*K))
# walkthrough on real screens (one match, start to finish)
S.append(('w1', page(CREAM, step(1, 'Pick your tiles') + phone('02-search.png', 720, None, 470, 160, 0, .1) + f'<div class="call a" style="left:60px;top:1350px;transform:rotate(-4deg);animation:fade .3s .8s forwards">Sunday tiles<br>by Sunday Mahjong</div>'), 2.0*K))
S.append(('w2', page(CREAM, step(2, 'Swipe the mats') + f'<div style="position:absolute;inset:0;animation:flyR .4s {2.0*K-0.45:.2f}s ease-in both">' + phone('05-swipe-brownstone.png', 720, None, 470, 120, 0, .05) + '</div>' + stamp('yes', .95, 760, 760) + f'<div class="call a" style="left:60px;top:1450px;transform:rotate(-4deg);animation:fade .3s .5s forwards">&hearts; Brownstone Bloom<br>by Anders Ruff</div>'), 2.0*K))
S.append(('w3', page(CREAM, step(2, 'Not the one?') + f'<div style="position:absolute;inset:0;animation:flyL .4s {1.6*K-0.45:.2f}s ease-in both">' + phone('04-swipe-songbird.png', 720, None, 470, 120, 0, .05) + '</div>' + stamp('no', .85, 120, 760) + f'<div class="call a" style="right:60px;top:1450px;transform:rotate(4deg);background:#7a6a85;animation:fade .3s .45s forwards">&#10005; Swipe left</div>'), 1.6*K))
# (Oct 27 9:24) w4 dropped: Tiffany synced her song to the calm cut; first heart (w2) must stay at 27.7s, nothing before 31s moves
S.append(('w5', page(CREAM, step(3, 'Meet your suitors') + phone('07-suitors.png', 720, None, 470, 200, 160, .05, 1.0) + f'<div class="call a" style="left:50px;top:1700px;transform:rotate(-4deg);animation:fade .3s 1.0s forwards">Every &hearts; falls to<br>the bottom. Pick one.</div>'), 2.4*K))
S.append(('w6', page(CREAM, step(4, 'Add racks') + phone('08-racks.png', 720, None, 470, 40, 0, .05) + f'<div class="call a" style="right:50px;top:760px;transform:rotate(4deg);animation:fade .3s .6s forwards">Your mat stays<br>zoomed up top</div>' + stamp('yes', 1.3, 760, 1300)), 2.2*K))
S.append(('w7', page(CREAM, step(5, 'Make it official') + phone('10-rack-slots.png', 720, None, 470, 120, 0, .05) + f'<div class="call a" style="left:50px;top:1690px;transform:rotate(-4deg);animation:fade .3s .6s forwards">Walnut + Oak<br>&rarr; Make it official &hearts;</div>'), 2.0*K))
S.append(('w8', page(NAVY, step(6, '<span style="color:#fff">It&rsquo;s a match!</span>') + f'<div style="position:absolute;left:0;right:0;top:470px;height:1240px;overflow:hidden"><div class="a" style="animation:pop .55s .1s forwards"><div><img src="{u("11-card-crop.png")}" style="width:800px;display:block;margin:60px auto 0;border-radius:30px;box-shadow:0 30px 70px rgba(0,0,0,.4)"></div></div></div>' + sparks(.3, 540, 1100, 14) + f'<div class="call a" style="left:60px;top:1600px;transform:rotate(-4deg);animation:fade .3s 1.2s forwards">4 brands. 1 match.</div>', '#fff'), 2.6*K))
S.append(('w9', page(CREAM, step(7, 'Shop your picks') + phone('12-shop.png', 720, None, 470, 175, 0, .05) + f'<div class="call a" style="right:40px;top:400px;transform:rotate(4deg);animation:fade .3s .6s forwards">Code MAHJMATCH<br>saves at partner brands</div>'), 2.4*K))
S.append(('end', page(NAVY, f'<img class="a" src="{u(R+"/assets/brand/flame-heart.png")}" style="width:150px;animation:pop .5s .05s forwards"><div class="a cap" style="font-size:150px;color:#fff;margin-top:40px;animation:slam .55s .3s forwards">Never ask<br>again.</div><div class="a" style="margin-top:70px;animation:pop .6s .8s forwards"><div style="background:{PINK};color:#fff;border-radius:999px;padding:34px 60px;font-family:Cap;font-size:78px;white-space:nowrap;animation:pulse 1.2s 1.6s ease-in-out infinite">{FYM}</div></div><div class="a" style="font:700 54px Bit;color:#fff;margin-top:60px;letter-spacing:.06em;animation:up .5s 1.2s forwards">LINK IN BIO</div><div class="a" style="font:700 40px Bit;color:{BLUSH};margin-top:24px;animation:up .5s 1.5s forwards">mahjmatchmaker.com &middot; code MAHJMATCH</div>', '#fff'), 4.0))

EXT = {'w5':1.2,'w6':1.0,'w7':1.0,'w8':1.5,'w9':1.0,'end':1.05} if CALM else {}  # calm = 58s (her song length)
S = [(n, h, s + EXT.get(n, 0)) for n, h, s in S]
async def shoot(pg, name, html, secs):
    hp = f'{FR}/{name}.html'; open(hp, 'w').write(html)
    await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
    d = f'{FR}/{name}'; os.makedirs(d, exist_ok=True)
    await pg.evaluate('document.getAnimations().forEach(a=>a.pause())')
    for i in range(int(round(secs * FPS))):
        await pg.evaluate(f'document.getAnimations().forEach(a=>{{a.currentTime={i * 1000 / FPS}}})')
        await pg.screenshot(path=f'{d}/{i:04d}.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{d}/%04d.png', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', f'{d}.mp4'], check=True)
    return f'{d}.mp4'

async def main(wall, out):
    from playwright.async_api import async_playwright
    clips = []
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for n, h, s in S: clips.append(await shoot(pg, n, h, s))
        await b.close()
    clips.insert(WALL_AT, wall)
    t = 0; mark = {}
    for (n, _, s) in S[:WALL_AT]: t += s
    print('wall at', round(t, 2))
    with open(f'{FR}/all.txt', 'w') as f:
        for c in clips: f.write(f"file '{c}'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{FR}/all.txt', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', out], check=True)
asyncio.run(main(sys.argv[1], sys.argv[2])); print('ok')
