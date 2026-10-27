"""'Here's how we're matching <set>' story (Oct 27, Tiffany 12:07): real FYM app screens, push-ins, swipes that fly RIGHT
with the heart on the card, suitors, real zoom on the mat while picking racks, clean match card, FYM CTA. Follows docs/FYM-REEL-RULES.md.
Usage: python3 how_story.py <capdir> "<Set name>" "<short name>" <N matches> '<json swipe labels>' <out.mp4>"""
import os, sys, json, asyncio, subprocess
SRC = open(os.path.join(os.path.dirname(__file__), 'launch_reel_v5.py')).read().split('\nS = []')[0]
CAPDIR, SETN, SHORT, NM, LABELS, OUT = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), json.loads(sys.argv[5]), sys.argv[6]
SRC = SRC.replace("CAP = f'{R}/assets/social/fym-launch/sunday-flow'", f"CAP = '{CAPDIR}'").replace("'/tmp/reelv5'", "'/tmp/howstory-" + SHORT.lower() + "'")
exec(SRC)
_full=open(os.path.join(os.path.dirname(__file__), 'launch_reel_v5.py')).read()
exec(_full[_full.index('async def shoot('):_full.index('async def main(')])
TILE = f'{CAPDIR}/tile.jpg'
def lab(t, x, y, rot=-3, delay=.25, bg=PINK): return f'<div class="call a" style="left:{x}px;top:{y}px;transform:rotate({rot}deg);background:{bg};animation:fade .25s {delay}s forwards">{t}</div>'
S = []
S.append(('h1', page(NAVY, f'<div class="a it" style="color:{BLUSH};font-size:64px;animation:up .45s .05s forwards">Here&rsquo;s how we&rsquo;re matching</div><div class="a cap" style="font-size:118px;color:#fff;margin:24px 0 50px;animation:up .5s .25s forwards">{SETN}</div>' + f'<img class="a" src="file://{TILE}" style="width:640px;height:430px;object-fit:cover;border-radius:28px;border:12px solid #fff;box-shadow:0 26px 60px rgba(0,0,0,.4);animation:pop .55s .45s forwards">', '#fff'), 2.2))
S.append(('h2', page(CREAM, step(1, 'Search her name') + '<div style="position:absolute;left:0;right:0;top:440px;bottom:0;overflow:hidden"><div style="position:absolute;inset:0;--z:1.25;transform-origin:30% 35%;animation:zoomin 1.2s .45s ease-in-out forwards">' + phone('01-search.png', 720, None, 30, 250, 0, .05) + '</div></div>' + lab(f'{SHORT} tiles &rarr; tap', 470, 1080, 3, .8)), 1.8))
def zscene():
    PW, PX, PY, CR = 1000, 40, 400, 215
    k = (PW - 2 * 0.034 * PW) / 390; dz = json.load(open(f'{CAPDIR}/dz.json'))[0] or [352, 355]
    tx = PX + PW * .034 + dz[0] * k; ty = PY + PW * .034 + PW * .13 + (dz[1] - CR) * k
    layers = ''.join(f'<div class="a" style="position:absolute;inset:0;animation:fade .12s {0.15 + j * .5:.2f}s forwards">' + phone(f'07-dz{j}.png', PW, PX, PY, CR, 0, 0) + '</div>' for j in range(4))
    taps = ''.join(f'<div class="a" style="position:absolute;left:{tx-45:.0f}px;top:{ty-45:.0f}px;width:90px;height:90px;border-radius:50%;border:8px solid {PINK};z-index:30;animation:ring .45s {0.05 + j * .5:.2f}s forwards"></div>' for j in range(3))
    return page(CREAM, step(2, 'Tap + to zoom in') + layers + taps + lab('her mat fills the frame', 90, 1740, -3, 1.4, NAVY))
for i, t in enumerate(LABELS):
    if i == len(LABELS) - 1: S.append(('zm', zscene(), 2.4))
    S.append((f'sw{i}', page(CREAM, step(2, 'Swipe her mats' if i == 0 else ('&hearts; &hearts; &hearts;' if i < len(LABELS) - 1 else 'Ooh, that one. &hearts;')) + f'<div style="position:absolute;inset:0;animation:flyR .35s .62s ease-in both">' + phone(f'02-swipe{i}.png', 720, None, 470, 230, 0, .03) + stamp('yes', .3, 640, 900) + lab('&hearts; ' + t, 90, 1560, -3, .15) + '</div>'), 1.0))
S.append(('su', page(CREAM, step(3, 'Hearts fall to your suitors') + '<div style="position:absolute;left:0;right:0;top:440px;bottom:0;overflow:hidden"><div style="position:absolute;inset:0;--z:1.35;transform-origin:50% 45%;animation:zoomin 1.6s .3s ease-in-out forwards">' + phone('03-suitors.png', 720, None, 30, 250, 0, .05) + '</div></div>' + lab(f'{len(LABELS)} suitors, pick the one', 520, 1520, 3, .9, NAVY)), 2.3))
S.append(('rk', page(CREAM, step(4, 'Add racks') + phone('05-racks-zoom.png', 720, None, 470, 40, 0, .05) + lab('&uarr; her mat stays up top', 330, 1640, -2, .6, NAVY)), 2.0))
S.append(('cd', page(NAVY, step(5, '<span style="color:#fff">It&rsquo;s a match!</span>') + f'<div style="position:absolute;left:0;right:0;top:450px"><div class="a" style="animation:pop .5s .1s forwards"><img src="file://{CAPDIR}/card.png" style="width:820px;display:block;margin:0 auto;border-radius:30px;box-shadow:0 30px 70px rgba(0,0,0,.4)"></div></div>' + sparks(.3, 540, 1100, 12), '#fff'), 2.4))
S.append(('cta', page(NAVY, f'<img class="a" src="{u(R+"/assets/brand/flame-heart.png")}" style="width:140px;animation:pop .45s .05s forwards"><div class="a cap" style="font-size:96px;color:#fff;margin-top:36px;animation:up .5s .2s forwards">Mock up {SHORT}</div><div class="a it" style="color:{BLUSH};font-size:56px;margin-top:18px;animation:up .5s .45s forwards">with all {NM} of her matches</div><div class="a" style="margin-top:60px;animation:pop .5s .8s forwards"><div style="background:{PINK};color:#fff;border-radius:999px;padding:30px 54px;font-family:Cap;font-size:72px;white-space:nowrap">{FYM}</div></div><div class="a" style="font:700 38px Bit;color:#fff;margin-top:50px;letter-spacing:.04em;white-space:nowrap;animation:up .5s 1.1s forwards">mahjmatchmaker.com &middot; code MAHJMATCH</div>', '#fff'), 3.4))
async def main():
    from playwright.async_api import async_playwright
    clips = []
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for n, h, s in S: clips.append(await shoot(pg, n, h, s))
        await b.close()
    with open(f'{FR}/all.txt', 'w') as f:
        for c in clips: f.write(f"file '{c}'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{FR}/all.txt', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', OUT], check=True)
asyncio.run(main()); print('ok')
