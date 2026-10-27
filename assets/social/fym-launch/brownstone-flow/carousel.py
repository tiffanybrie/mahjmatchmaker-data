"""Launch carousel (Oct 27, Tiffany 3:29am brief): ONE match all the way through (Brownstone Bloom tiles, Anders Ruff),
every step of the tool on its own real screen: question hook -> it's here -> pick tiles -> swipe mats -> suitors fall
to the bottom -> pick your suitor -> add racks (mat zoomed on top) -> make it official -> match card -> shop + MAHJMATCH
-> you're the matchmaker. 4:5 posts (grid, pinned) + 9:16 story versions. Usage: python3 carousel.py post|story"""
import os, sys
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); R = '/home/claude/mahjmatchmaker-data'
F = f'file://{R}/scripts/social/tileprofile/fonts/'
u = lambda p: 'file://' + (p if p.startswith('/') else f'{D}/{p}')
NAVY, PINK, CREAM, BLUSH, INK = '#062a55', '#e0547f', '#fdf6ee', '#f7b6c8', '#4a3d58'
CSS = f"""@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:PF;font-style:italic;src:url({F}playfair-display-latin-600-italic.woff2)}}
@font-face{{font-family:Bit;font-weight:700;src:url({F}bitter-latin-700-normal.woff2)}}@font-face{{font-family:Bit;font-weight:600;src:url({F}bitter-latin-600-normal.woff2)}}
*{{margin:0;box-sizing:border-box}}body{{position:relative;overflow:hidden;font-family:Bit;color:{NAVY};background:{CREAM}}}
.c{{position:absolute;left:0;right:0;text-align:center}}.pf{{font-family:PF;font-style:italic;font-weight:600}}
.num{{display:inline-grid;place-items:center;width:84px;height:84px;border-radius:50%;background:{PINK};color:#fff;font:400 46px Cap;vertical-align:middle;margin-right:18px}}
.h{{font:400 76px/1.02 Cap}}.sub{{font:italic 600 38px/1.3 PF;color:{INK};margin-top:14px}}
.pill{{display:inline-block;background:{NAVY};color:#fff;font:700 26px Bit;letter-spacing:5px;padding:12px 28px;border-radius:40px}}
.call{{position:absolute;z-index:10;background:{PINK};color:#fff;font:700 30px/1.2 Bit;padding:14px 22px;border-radius:22px;box-shadow:0 10px 24px rgba(214,36,127,.3);max-width:420px;text-align:left}}
.dots{{position:absolute;left:0;right:0;display:flex;gap:10px;justify-content:center}}.dots i{{width:12px;height:12px;border-radius:50%;background:#e8cdd6}}.dots i.on{{background:{PINK};width:34px;border-radius:8px}}
"""
FYM = lambda s: f'Find <span class="pf" style="font-size:{s*1.02:.0f}px">Your</span> Mat-ch<sup style="font-size:{s*.36:.0f}px">&trade;</sup>'
def phone(img, w, x, y, rot=0, z=2, crop_top=0):
    h = w * 2.06; p = w * 0.034
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z}">'
            f'<div style="position:absolute;inset:0;border-radius:{w*.16}px;background:#f7f7f5;box-shadow:0 30px 70px rgba(6,42,85,.22),inset 0 0 0 {w*.006}px #d6d6d3;padding:{p}px">'
            f'<div style="position:relative;width:100%;height:100%;border-radius:{w*.13}px;overflow:hidden;background:#fff">'
            f'<div style="height:{w*.13:.0f}px;background:#fff"></div><div style="overflow:hidden;height:100%"><img src="{u(img)}" style="width:100%;display:block;margin-top:-{crop_top*(w-2*p)/390:.0f}px"></div></div>'
            f'<div style="position:absolute;left:50%;top:{w*.045}px;transform:translateX(-50%);width:{w*.28}px;height:{w*.08}px;background:#000;border-radius:{w*.05}px"></div></div></div>')
N = 10
def dots(k, y): return f'<div class="dots" style="top:{y}px">' + ''.join(f'<i class="{"on" if i == k else ""}"></i>' for i in range(N)) + '</div>'
def step(n, t, sub, T): return f'<div class="c" style="top:{T}px"><div class="h"><span class="num">{n}</span>{t}</div><div class="sub">{sub}</div></div>'

def slides(H):
    st = H > 1500; T = 230 if st else 70; Y = (T + 330) if st else 290; PW = 470 if st else 420; DY = H - (330 if st else 70)
    cx = (1080 - PW) // 2; o = {}
    o['01-question'] = (NAVY, f'''<div class="c" style="top:{T+20}px;color:#fff"><div class="pf" style="font-size:52px;color:{BLUSH}">The ever&#8209;burning question&hellip;</div>
<div style="font:400 104px/1.02 Cap;margin-top:26px">What mat goes with<br><span style="color:{BLUSH}">these</span> tiles?</div></div>
<img src="{u(R+'/assets/tiles/album/brownstone-bloom.jpg')}" style="position:absolute;left:290px;top:{T+(470 if st else 420)}px;width:500px;height:500px;object-fit:cover;border-radius:50%;border:14px solid #fff;box-shadow:0 30px 70px rgba(0,0,0,.35)">
<div class="c" style="top:{T+(1010 if st else 960)}px;color:#fff;font:700 34px Bit;letter-spacing:.04em">Asked in every mahj group. Every. Single. Day.</div>
<div class="c" style="top:{DY-60}px;color:{BLUSH};font:700 30px Bit;letter-spacing:.2em">SWIPE FOR THE ANSWER &rarr;</div>''')
    o['02-here'] = (CREAM, f'''<div class="c" style="top:{T}px"><span class="pill">NOW LIVE &middot; FREE</span><div style="font:400 112px/1.0 Cap;margin-top:26px">{FYM(112)}<br><span style="color:{PINK}">is HERE.</span></div>
<div class="sub">Today, <b>you</b> are the matchmaker.</div></div>''' + phone('01-home.png', 470, 305, Y + (170 if st else 150), 0, 3) +
        f'<div class="call" style="left:30px;top:{Y+(400 if st else 380)}px;transform:rotate(-4deg)">Start with your tiles&hellip;</div><div class="call" style="right:30px;top:{Y+(480 if st else 460)}px;transform:rotate(4deg);background:{NAVY}">&hellip;or with the mat you own</div>')
    o['03-tiles'] = (CREAM, step(1, 'Pick your tiles', 'Search, or shop by color or brand.', T) + phone('02-search.png', 600, 240, Y-20, 0, 2, 150) +
        f'<div class="call" style="left:40px;top:{Y+820}px;transform:rotate(-4deg)">Brownstone Bloom<br>by Anders Ruff</div>')
    o['04-swipe'] = (CREAM, step(2, 'Swipe the mats', '&hearts; the ones you love, &#10005; the rest.', T) + phone('04-swipe-marigold.png', 470, 70, Y+60, -7, 1, 120) + phone('03-swipe-scarlett.png', 520, 500, Y-10, 4, 3, 120) +
        f'<div class="call" style="left:40px;top:{Y-20}px;transform:rotate(-4deg)">My picks are baked in,<br>so you never swipe alone</div><div class="call" style="left:150px;top:{Y+520}px;transform:rotate(3deg);background:{NAVY}">&#10005; Marigold</div><div class="call" style="right:60px;top:{Y+700}px;transform:rotate(-3deg)">&hearts; Scarlett</div>')
    o['05-suitors'] = (CREAM, step(3, 'Meet your suitors', 'Every &hearts; falls to the bottom. Pick the one.', T) + phone('07-suitors.png', 600, 240, Y-20, 0, 2, 150) +
        f'<div class="call" style="left:30px;top:{Y+120}px;transform:rotate(-4deg)">Your hearted mats<br>wait down here</div>')
    o['06-racks'] = (CREAM, step(4, 'Add racks', 'Your mat stays up top while you swipe racks.', T) + phone('08-racks.png', 470, 560, Y+60, 7, 1, 40) + phone('09-racks2.png', 520, 80, Y-10, -3, 3, 40) +
        f'<div class="call" style="right:30px;top:{Y-30}px;transform:rotate(4deg);background:{NAVY}">Racks from brands<br>across the table</div><div class="call" style="left:30px;top:{Y+560}px;transform:rotate(-4deg)">&uarr; Your mat, zoomed in</div>')
    o['07-official'] = (CREAM, step(5, 'Make it official', 'Pick 1 or 2 racks. Tap &hearts; Make it official.', T) + phone('09-racks2.png', 470, 50, Y+50, -6, 1, 40) + phone('10-rack-slots.png', 520, 510, Y-10, 4, 3, 440) +
        f'<div class="call" style="right:40px;top:{Y+520}px;transform:rotate(3deg)">Walnut + Olive Green<br>by Bam Bird Boutique</div>')
    o['08-card'] = (CREAM, step(6, 'Your match card', 'Save it. Share it. Tag #mahjmatch.', T) + phone('11-card.png', 600, 240, Y-20, 0, 2, 120))
    o['09-shop'] = (CREAM, step(7, 'Shop your picks', 'Every piece links straight to its shop.', T) + phone('12-shop.png', 600, 240, Y-20, 0, 2, 185) +
        f'<div class="call" style="left:30px;top:{Y-60}px;transform:rotate(-4deg)">Code MAHJMATCH<br>saves at partner brands</div>')
    o['10-cta'] = (NAVY, f'''<div class="c" style="top:{T+(150 if st else 90)}px;color:#fff"><div class="pf" style="font-size:46px;color:{BLUSH}">Mahj Matchmaker 2.0</div>
<div style="font:400 108px/1.02 Cap;margin-top:22px">Today, <span style="color:{BLUSH}">you</span><br>are the<br>matchmaker.</div>
<div style="margin-top:50px"><span style="display:inline-block;background:{PINK};color:#fff;border-radius:999px;padding:26px 50px;font:400 64px Cap">{FYM(64)}</div>
<div style="font:700 44px Bit;margin-top:46px">mahjmatchmaker.com &middot; link in bio</div>
<div style="font:700 30px Bit;letter-spacing:.14em;color:{BLUSH};margin-top:26px">SAVE THIS POST &middot; SEND IT TO YOUR MAHJ GROUP</div></div>''')
    out = {}
    for i, (k, (bg, body)) in enumerate(o.items()):
        out[k] = (bg, body)
    return out

mode = sys.argv[1]; H = 1350 if mode == 'post' else 1920
os.makedirs(f'{D}/out', exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': H})
    for k, (bg, body) in slides(H).items():
        open(f'{D}/_c.html', 'w').write(f'<html><head><meta charset=utf8><style>{CSS}body{{width:1080px;height:{H}px;background:{bg}}}</style></head><body>{body}</body></html>')
        pg.goto('file://' + D + '/_c.html'); pg.wait_for_timeout(900); pg.screenshot(path=f'{D}/out/{mode}-{k}.jpg', type='jpeg', quality=92)
    b.close()
os.remove(f'{D}/_c.html'); print('ok')
