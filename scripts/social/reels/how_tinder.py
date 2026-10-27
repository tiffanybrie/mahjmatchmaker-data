"""'Here's how we're matching <set>' reel, Tinder cut (Tiffany Oct 27 2:05pm + 2:07pm, docs/FYM-REEL-RULES.md 14-17).
Real FYM screens; every swipe cuts the top card out of the screen and throws it LEFT (✕) or RIGHT (♥) with a dating-app tilt and stamp,
revealing the real next card underneath. Flow: pick a colour -> swipe everyday mats -> tap Holiday -> swipe holiday mats -> suitors ->
racks step: + + + zoom on the mat and pan -> rack-type chip (Wood) -> swipe racks ✕/♥ with the mat zoomed -> "It's a match!" -> CTA.
Capture: /tmp/sun/how/cap3.py (copy in assets/social/restock-oct27/how/cap3.py). Config: JSON file (argv[1]); output argv[2]."""
import os, sys, json, asyncio, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(sys.argv[1])); OUT = sys.argv[2]; CAPDIR = CFG['capdir']
SRC = open(os.path.join(HERE, 'launch_reel_v5.py')).read().split('\nS = []')[0]
SRC = SRC.replace("CAP = f'{R}/assets/social/fym-launch/sunday-flow'", f"CAP = '{CAPDIR}'").replace("'/tmp/reelv5'", "'/tmp/howtinder'")
exec(SRC)
_full = open(os.path.join(HERE, 'launch_reel_v5.py')).read(); exec(_full[_full.index('async def shoot('):_full.index('async def main(')])
META = json.load(open(f'{CAPDIR}/meta.json')); SL = float(os.environ.get('SLOW', '1.0'))
SLATE = '#6f6280'
CSS2 = """<style>@keyframes swR{0%{transform:none}40%{transform:translateX(70px) rotate(6deg)}100%{transform:translateX(1250px) rotate(28deg)}}
@keyframes swL{0%{transform:none}40%{transform:translateX(-70px) rotate(-6deg)}100%{transform:translateX(-1250px) rotate(-28deg)}}
@keyframes stmp{0%{opacity:0;transform:scale(1.8) rotate(var(--r))}100%{opacity:1;transform:scale(1) rotate(var(--r))}}
@keyframes btn{0%,100%{transform:scale(1)}50%{transform:scale(1.28)}}</style>"""
def pg_(bg, body, fg=NAVY): return page(bg, body, fg).replace('</head>', CSS2 + '</head>')
def lab(t, x, y, rot=-3, delay=.25, bg=PINK): return f'<div class="call a" style="left:{x}px;top:{y}px;transform:rotate({rot}deg);background:{bg};animation:fade .25s {delay}s forwards">{t}</div>'
def geo(PW, PX, PY, CR):
    p = PW * .034; k = (PW - 2 * p) / 390; return PX + p, PY + p + PW * .13 - CR * k, k
def ring(x, y, t, c=PINK): return f'<div class="a" style="position:absolute;left:{x-50:.0f}px;top:{y-50:.0f}px;width:100px;height:100px;border-radius:50%;border:9px solid {c};z-index:30;animation:ring .5s {t:.2f}s forwards"></div>'
def tstamp(kind, t):
    if kind == 'yes':
        return f'<div style="position:absolute;left:40px;top:60px;--r:-14deg;opacity:0;animation:stmp .22s {t:.2f}s forwards;border:12px solid {PINK};color:{PINK};border-radius:28px;padding:6px 34px;font:400 130px/1 Cap;background:rgba(255,255,255,.88)">&hearts;</div>'
    return f'<div style="position:absolute;right:40px;top:60px;--r:14deg;opacity:0;animation:stmp .22s {t:.2f}s forwards;border:12px solid {SLATE};color:{SLATE};border-radius:28px;padding:6px 38px;font:400 120px/1 Cap;background:rgba(255,255,255,.88)">&#10005;</div>'
def bigbtns(kind, t):
    on = lambda k: f'animation:btn .35s {t:.2f}s;' if k == kind else ''
    return (f'<div style="position:absolute;left:0;right:0;bottom:70px;display:flex;justify-content:center;gap:120px;z-index:40">'
            f'<div style="{on("no")}width:150px;height:150px;border-radius:50%;background:#fff;box-shadow:0 12px 30px rgba(0,0,0,.25);display:grid;place-items:center;font:400 80px Cap;color:{SLATE}">&#10005;</div>'
            f'<div style="{on("yes")}width:150px;height:150px;border-radius:50%;background:{PINK};box-shadow:0 12px 30px rgba(0,0,0,.25);display:grid;place-items:center;font:400 84px Cap;color:#fff">&hearts;</div></div>')
def still(html): return html.replace('animation:rise .5s 0.00s cubic-bezier(.2,.9,.25,1.05) forwards', 'opacity:1')
def swipe(name, title, bg_img, card_id, kind, label, PW, PX, PY, CR, secs, extra='', LT=430, btns=False, pbtn=None):
    sx, sy, k = geo(PW, PX, PY, CR); bx, by, bw, bh = META[card_id]
    t_stamp, t_go = .35 * SL, .55 * SL
    fly = (f'<div style="position:absolute;left:{sx+bx*k:.0f}px;top:{sy+by*k:.0f}px;width:{bw*k:.0f}px;z-index:20;transform-origin:50% 120%;'
           f'animation:{"swR" if kind=="yes" else "swL"} {.6*SL:.2f}s {t_go:.2f}s cubic-bezier(.5,0,.8,.6) both">'
           f'<img src="file://{CAPDIR}/{card_id}-card.png" style="width:100%;display:block;border-radius:{14*k:.0f}px;box-shadow:0 30px 70px rgba(0,0,0,.35)">'
           + tstamp(kind, t_stamp) + (f'<div class="call" style="left:30px;top:{LT}px;transform:rotate(-3deg);background:{PINK if kind=="yes" else SLATE}">{label}</div>' if label else '') + '</div>')
    return (name, pg_(CREAM, title + f'<div style="position:absolute;inset:0;overflow:hidden">' + still(phone(bg_img, PW, PX, PY, CR, 0, 0)) + fly + '</div>' + (bigbtns(kind, t_stamp) if btns else '') + (ring(*pbtn[kind], t_stamp) if pbtn else '') + extra), secs)

C = CFG; S = []
PB = {'no': (460, 1813), 'yes': (616, 1813)}  # the phone's own ✕ / ♥ buttons in the mats frame
MPW, MPX, MPY, MCR = 860, 110, 400, 200          # mats: deck card big in frame
RPW, RPX, RPY, RCR = 800, 140, 300, 20           # racks: zoomed mat preview + rack card
S.append(('h1', pg_(NAVY, f'<div class="a it" style="color:{BLUSH};font-size:64px;animation:up .45s .05s forwards">Here&rsquo;s how we&rsquo;re matching</div><div class="a cap" style="font-size:118px;color:#fff;margin:24px 0 50px;animation:up .5s .25s forwards">{C["set"]}</div><img class="a" src="file://{CAPDIR}/tile.jpg" style="width:640px;height:430px;object-fit:cover;border-radius:28px;border:12px solid #fff;box-shadow:0 26px 60px rgba(0,0,0,.4);animation:pop .55s .45s forwards">', '#fff'), 2.2 * SL))
# colour filter
sx, sy, k = geo(MPW, MPX, MPY, MCR); cx, cy = META['colchip']
S.append(('col', pg_(CREAM, step(1, 'Pick a color') + '<div style="position:absolute;inset:0;overflow:hidden">' + phone('10-col-before.png', MPW, MPX, MPY, MCR, 0, 0) + '</div>' + ring(sx + cx * k, sy + cy * k, .5 * SL) + ring(sx + cx * k, sy + cy * k, .75 * SL) + lab(C['col_label'], 300, sy + cy * k + 80, 3, .7 * SL, NAVY)), 1.7 * SL))
EV, HO = C['every'], C['hol']
for i, (lbl, kind) in enumerate(EV):
    S.append(swipe(f's{i}', step(2, 'Swipe right &hearts; or left &#10005;' if i == 0 else ('Love her? &hearts;' if kind == 'yes' else 'Not the one? &#10005;')), f's{i}-a.png', f's{i}', kind, lbl, MPW, MPX, MPY, MCR, 1.35 * SL, pbtn=PB))
# holiday button
hx, hy = META['holchip']
S.append(('hol', pg_(NAVY, f'<div class="a cap" style="position:absolute;top:120px;left:60px;right:60px;font-size:84px;color:#fff;animation:up .45s .05s forwards">{C["hol_title"]}</div>' + '<div style="position:absolute;inset:0;overflow:hidden">' + phone('20-hol-before.png', MPW, MPX, MPY + 40, MCR, 0, 0) + '</div>' + ring(sx + hx * k, sy + 40 + hy * k, .6 * SL) + ring(sx + hx * k, sy + 40 + hy * k, .85 * SL) + lab(f'tap Holiday &middot; {META["holn"]} holiday mats for her', 170, sy + 40 + hy * k + 90, -2, .8 * SL), '#fff'), 2.2 * SL))
for j, (lbl, kind) in enumerate(HO):
    i = len(EV) + j
    S.append(swipe(f's{i}', step(3, 'Try her on for the holidays' if j == 0 else ('Love her? &hearts;' if kind == 'yes' else 'Not the one? &#10005;')), f's{i}-a.png', f's{i}', kind, lbl, MPW, MPX, MPY, MCR, 1.35 * SL, pbtn=PB))
S.append(('su', pg_(CREAM, step(4, 'Your &hearts;s line up') + '<div style="position:absolute;left:0;right:0;top:440px;bottom:0;overflow:hidden"><div style="position:absolute;inset:0;--z:1.3;transform-origin:50% 45%;animation:zoomin 1.6s .3s ease-in-out forwards">' + phone('30-suitors.png', 760, None, 30, 250, 0, .05) + '</div></div>' + lab(C['pick_label'], 300, 1540, 3, .9 * SL, NAVY)), 2.2 * SL))
# racks step: + + + zoom on the mat, then pan
rsx, rsy, rk = geo(RPW, RPX, RPY, RCR); zx, zy = META['rz']
layers = ''.join(f'<div class="a" style="position:absolute;inset:0;animation:fade .12s {(0 if j == 0 else 0.3 + j * .55) * SL:.2f}s forwards">' + phone(f'40-rz{j}.png', RPW, RPX, RPY, RCR, 0, 0) + '</div>' for j in range(5))
taps = ''.join(ring(rsx + zx * rk, rsy + zy * rk, (0.15 + j * .55) * SL) for j in range(3))
ZO = f'{rsx + 195 * rk:.0f}px {rsy + 190 * rk:.0f}px'
S.append(('rz', pg_(CREAM, step(5, 'Tap + to zoom in') + f'<div style="position:absolute;inset:0;overflow:hidden"><div style="position:absolute;inset:0;--z:1.45;transform-origin:{ZO};animation:zoomin {1.2*SL:.2f}s {1.9*SL:.2f}s ease-in-out forwards">' + still(layers) + '</div></div>' + taps + lab('+ + + then drag to the pattern', 140, 1180, -3, 2.3 * SL, NAVY)), 3.3 * SL))
wx, wy = META['woodchip']
S.append(('chip', pg_(CREAM, step(5, 'Pick a rack type') + '<div style="position:absolute;inset:0;overflow:hidden">' + still(phone('45-chips.png', RPW, RPX, RPY, RCR, 0, 0)) + '</div>' + ring(rsx + wx * rk, rsy + wy * rk, .5 * SL) + lab('wood, tortoise, metallic, clear', 330, rsy + wy * rk + 80, 2, .7 * SL)), 1.6 * SL))
RK = C['racks']; RBG = ['r1-b.png', 'r1-a.png', 'r2-a.png']
for j, (lbl, kind) in enumerate(RK):
    S.append(swipe(f'r{j}', step(5, 'Swipe racks' if j == 0 else ('Love it? &hearts;' if kind == 'yes' else 'Not the one? &#10005;')), RBG[j], f'r{j}', kind, lbl, RPW, RPX, RPY, RCR, 1.35 * SL, LT=110, btns=True))
# dating-app match moment
mat_img = f'{CAPDIR}/{C["match_card_id"]}-card.png'
circ = lambda src, x, d: f'<div class="a" style="position:absolute;top:470px;left:{x}px;width:380px;height:380px;border-radius:50%;border:14px solid #fff;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.4);animation:pop .5s {d}s forwards"><img src="file://{src}" style="width:100%;height:100%;object-fit:cover;object-position:50% 30%"></div>'
S.append(('match', pg_(NAVY, f'<div class="a it" style="position:absolute;top:200px;left:0;right:0;font-size:150px;color:#fff;animation:slam .5s .05s forwards">It&rsquo;s a match!</div>' + circ(f'{CAPDIR}/tile.jpg', 106, .35) + circ(mat_img, 566, .5) + f'<div class="a" style="position:absolute;top:590px;left:480px;width:120px;height:120px;z-index:5;animation:pop .45s .8s forwards">{HEART.format(c=PINK)}</div>' + f'<div class="a" style="position:absolute;left:0;right:0;top:960px;font:700 50px Bit;color:{BLUSH};animation:up .45s 1.0s forwards">{C["match_line"]}</div>' + sparks(.9, 540, 660, 14), '#fff'), 2.2 * SL))
S.append(('cd', pg_(NAVY, f'<div style="position:absolute;left:0;right:0;top:250px"><div class="a" style="animation:pop .5s .1s forwards"><img src="file://{CAPDIR}/card.png" style="width:860px;display:block;margin:0 auto;border-radius:30px;box-shadow:0 30px 70px rgba(0,0,0,.4)"></div></div>', '#fff'), 2.6 * SL))
S.append(('cta', pg_(NAVY, f'<img class="a" src="{u(R+"/assets/brand/flame-heart.png")}" style="width:140px;animation:pop .45s .05s forwards"><div class="a cap" style="font-size:96px;color:#fff;margin-top:36px;animation:up .5s .2s forwards">Mock up {C["short"]}</div><div class="a it" style="color:{BLUSH};font-size:56px;margin-top:18px;animation:up .5s .45s forwards">{C["cta_line"]}</div><div class="a" style="margin-top:60px;animation:pop .5s .8s forwards"><div style="background:{PINK};color:#fff;border-radius:999px;padding:30px 54px;font-family:Cap;font-size:72px;white-space:nowrap">{FYM}</div></div><div class="a" style="font:700 38px Bit;color:#fff;margin-top:50px;letter-spacing:.04em;white-space:nowrap;animation:up .5s 1.1s forwards">mahjmatchmaker.com &middot; code MAHJMATCH</div>', '#fff'), 3.4 * SL))
ONLY = os.environ.get('ONLY')
async def main():
    from playwright.async_api import async_playwright
    clips = []
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for n, h, s in S:
            if ONLY and n not in ONLY.split(','):
                if os.environ.get('REUSE') and os.path.exists(f'{FR}/{n}.mp4'): clips.append(f'{FR}/{n}.mp4')
                continue
            clips.append(await shoot(pg, n, h, s))
        await b.close()
    with open(f'{FR}/all.txt', 'w') as f:
        for c in clips: f.write(f"file '{c}'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{FR}/all.txt', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', OUT], check=True)
    print('secs', round(sum(s for _, _, s in S), 1))
asyncio.run(main()); print('ok')
