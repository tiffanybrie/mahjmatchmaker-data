"""Holiday Find Your Mat-ch reel (Nov 1 2026): Nutcracker Ballet (Mahj Squad) x Clara (Oh My Mahjong), real FYM v110 screens.
Sugar-plum night stage (navy -> berry, falling snow, gold twinkles, red velvet curtains), cut on a 160 BPM grid
(Kelly Clarkson "Underneath the Tree", 1 beat = 0.375 s). Phone never moves on a swipe (FYM-REEL-RULES 20); the camera
pushes in / pulls back between swipes. Captures: cap.py (+ cap_tail.py) -> /dev/shm/fym-holiday/caps.
Usage: python3 build.py full|hook   (env ONLY=scene,scene to re-render some scenes; frames in /dev/shm, deleted after)."""
import os, sys, json, asyncio, subprocess, random, math, shutil
R = '/home/claude/mahjmatchmaker-data'; HERE = f'{R}/assets/social/holiday-nov1/fym'
CAP = '/dev/shm/fym-holiday/caps'; F = f'file://{R}/scripts/social/tileprofile/fonts/'
MODE = sys.argv[1] if len(sys.argv) > 1 else 'full'
FR = f'/dev/shm/fym-holiday/fr-{MODE}' + ('-nobg' if os.environ.get('NOBG') == '1' else ''); os.makedirs(FR, exist_ok=True)
FPS = 30; BPM = 160; B = 60 / BPM
META = json.load(open(f'{CAP}/meta.json'))
NAVY, PINK, BLUSH, GOLD, RED, PINE, SLATE = '#062a55', '#e0547f', '#f7b6c8', '#f2c46d', '#b3202a', '#1f5a3a', '#6f6280'
FYM = 'Find <span class="pf">Your</span> Mat&#8209;ch<sup style="font-size:.34em;vertical-align:super">&trade;</sup>'
u = lambda p: 'file://' + (p if p.startswith('/') else f'{CAP}/{p}')
HEART = '<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="{c}"/></svg>'
STAR = '<svg viewBox="0 0 40 40" width="100%" height="100%"><path d="M20 0 L23 17 L40 20 L23 23 L20 40 L17 23 L0 20 L17 17 Z" fill="{c}"/></svg>'

CSS = f"""<style>@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:Bit;font-weight:700;src:url({F}bitter-latin-700-normal.woff2)}}
@font-face{{font-family:PF;font-style:italic;font-weight:600;src:url({F}playfair-display-latin-600-italic.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;background:{NAVY}}}
.w{{position:relative;width:1080px;height:1920px;overflow:hidden;color:#fff;
 background:radial-gradient(ellipse 120% 70% at 50% 18%,#123d7a 0%,{NAVY} 45%,#2a1450 75%,#5b1745 100%)}}
.cap{{font-family:Cap;line-height:1.02}}.pf{{font-family:PF;font-style:italic;font-weight:600}}
.a{{opacity:0;animation-fill-mode:forwards;animation-timing-function:cubic-bezier(.2,.8,.2,1)}}
.snow{{position:absolute;border-radius:50%;background:#fff;animation:fall linear infinite}}
.tw{{position:absolute;animation:tw ease-in-out infinite}}
@keyframes fall{{0%{{transform:translate(0,-60px)}}100%{{transform:translate(var(--dx),2000px)}}}}
@keyframes tw{{0%,100%{{opacity:.15;transform:scale(.5) rotate(0)}}50%{{opacity:1;transform:scale(1) rotate(45deg)}}}}
@keyframes up{{0%{{transform:translateY(70px);opacity:0}}100%{{transform:none;opacity:1}}}}
@keyframes fade{{0%{{opacity:0}}100%{{opacity:1}}}}
@keyframes out{{0%{{opacity:1}}100%{{opacity:0}}}}
@keyframes pop{{0%{{transform:scale(.3);opacity:0}}60%{{transform:scale(1.08);opacity:1}}100%{{transform:scale(1);opacity:1}}}}
@keyframes slam{{0%{{transform:scale(2.6);opacity:0}}45%{{transform:scale(.94);opacity:1}}70%{{transform:scale(1.03)}}100%{{transform:scale(1);opacity:1}}}}
@keyframes ring{{0%{{transform:scale(.4);opacity:1}}100%{{transform:scale(2.4);opacity:0}}}}
@keyframes cam{{0%{{transform:translate(var(--x0),var(--y0)) scale(var(--s0))}}100%{{transform:translate(var(--x1),var(--y1)) scale(var(--s1))}}}}
@keyframes swR{{0%{{transform:none}}35%{{transform:translateX(60px) rotate(6deg)}}100%{{transform:translateX(1150px) rotate(26deg)}}}}
@keyframes swL{{0%{{transform:none}}35%{{transform:translateX(-60px) rotate(-6deg)}}100%{{transform:translateX(-1150px) rotate(-26deg)}}}}
@keyframes stmp{{0%{{opacity:0;transform:scale(2.2) rotate(var(--r))}}60%{{opacity:1;transform:scale(.92) rotate(var(--r))}}100%{{opacity:1;transform:scale(1) rotate(var(--r))}}}}
@keyframes land{{0%{{transform:translate(var(--fx),var(--fy)) scale(var(--fs)) rotate(14deg)}}100%{{transform:none}}}}
@keyframes curL{{0%{{transform:translateX(0)}}100%{{transform:translateX(-102%)}}}}
@keyframes curR{{0%{{transform:translateX(0)}}100%{{transform:translateX(102%)}}}}
@keyframes spark{{0%{{transform:translate(0,0) scale(.2);opacity:0}}20%{{opacity:1}}100%{{transform:translate(var(--x),var(--y)) scale(1);opacity:0}}}}
@keyframes bump{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.25)}}}}
.ttl{{position:absolute;left:40px;right:40px;top:262px;text-align:center;z-index:30;font-family:Cap;font-size:84px;line-height:1.02;color:#fff;text-shadow:0 6px 0 rgba(0,0,0,.18),0 0 40px rgba(242,196,109,.35)}}
.ttl em{{font-style:normal;color:{GOLD}}}
.call{{position:absolute;z-index:40;background:{PINK};color:#fff;font:700 42px/1.15 Bit;padding:18px 30px;border-radius:28px;box-shadow:0 14px 34px rgba(0,0,0,.35);white-space:nowrap;border:4px solid #fff}}
</style>"""

random.seed(11)
FLAKES = [(random.uniform(0, 1080), random.uniform(4, 13), random.uniform(5, 11), random.uniform(0, 12), random.uniform(-80, 80), random.uniform(.45, .95)) for _ in range(90)]
TWS = [(random.uniform(20, 1060), random.uniform(20, 1900), random.uniform(18, 46), random.uniform(1.2, 2.6), random.uniform(0, 3)) for _ in range(26)]
def bg(t0):
    """Snow + gold twinkles, driven by the global clock so they never jump at a cut."""
    s = ''.join(f'<div class="snow" style="left:{x:.0f}px;top:0;width:{d:.1f}px;height:{d:.1f}px;opacity:{o:.2f};--dx:{dx:.0f}px;animation-duration:{dur:.2f}s;animation-delay:-{(t0 + ph) % dur:.2f}s;filter:blur({.6 if d < 7 else 0}px)"></div>' for x, d, dur, ph, dx, o in FLAKES)
    s += ''.join(f'<div class="tw" style="left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{w:.0f}px;animation-duration:{d:.2f}s;animation-delay:-{(t0 + ph) % d:.2f}s">{STAR.format(c=GOLD)}</div>' for x, y, w, d, ph in TWS)
    # garland of warm bokeh lights along the top edge
    s += ''.join(f'<div style="position:absolute;left:{40 + i * 84}px;top:{22 + (i % 2) * 26}px;width:34px;height:34px;border-radius:50%;background:{["#f2c46d", "#e0547f", "#7fd3a6", "#f7b6c8"][i % 4]};box-shadow:0 0 26px 8px {["#f2c46d", "#e0547f", "#7fd3a6", "#f7b6c8"][i % 4]}88;opacity:.85"></div>' for i in range(13))
    return f'<div style="position:absolute;inset:0;z-index:1;pointer-events:none">{s}</div>'
def snow_front(t0):
    s = ''.join(f'<div class="snow" style="left:{(x * 1.7) % 1080:.0f}px;top:0;width:{d * .8:.1f}px;height:{d * .8:.1f}px;opacity:{o * .7:.2f};--dx:{-dx:.0f}px;animation-duration:{dur * .8:.2f}s;animation-delay:-{(t0 + ph * 1.3) % (dur * .8):.2f}s"></div>' for x, d, dur, ph, dx, o in FLAKES[:28])
    return f'<div style="position:absolute;inset:0;z-index:60;pointer-events:none">{s}</div>'
NOBG = os.environ.get("NOBG") == "1"
def page(body, t0, front=True):
    if NOBG: return f'<!doctype html><html><head><meta charset=utf8>{CSS}</head><body><div class="w" style="background:{NAVY}">{body}</div></body></html>'
    return f'<!doctype html><html><head><meta charset=utf8>{CSS}</head><body><div class="w">{bg(t0)}{body}{snow_front(t0) if front else ""}</div></body></html>'

# ---- phone geometry (static frame; screenshots are 390-css-wide viewports at 3x)
PW, PX, PY = 720, 180, 410
P = PW * .034; K = (PW - 2 * P) / 390; TOP = PY + P + PW * .10
def sx(x): return PX + P + x * K
def sy(y, crop): return TOP + (y - crop) * K
def phone(img, crop, extra=''):
    return (f'<div style="position:absolute;left:{PX}px;top:{PY}px;width:{PW}px;height:{PW * 2.06:.0f}px;z-index:5">'
            f'<div style="position:absolute;inset:0;border-radius:{PW * .15:.0f}px;background:linear-gradient(145deg,#fdf6ee,#e9dccf);box-shadow:0 0 0 6px {GOLD}55,0 40px 90px rgba(0,0,0,.55);padding:{P:.0f}px">'
            f'<div style="position:relative;width:100%;height:100%;border-radius:{PW * .12:.0f}px;overflow:hidden;background:#fff">'
            f'<div style="height:{PW * .10:.0f}px;background:#fff"></div><div style="margin-top:-{crop * K:.0f}px"><img src="{u(img)}" style="width:100%;display:block"></div>{extra}</div>'
            f'<div style="position:absolute;left:50%;top:{PW * .04:.0f}px;transform:translateX(-50%);width:{PW * .27:.0f}px;height:{PW * .075:.0f}px;background:#111;border-radius:{PW * .05:.0f}px"></div></div></div>')
def layer(img, crop, t_in, dur=.08):
    """A later screenshot of the same phone screen, faded in on top (taps / zoom steps)."""
    return f'<div class="a" style="position:absolute;inset:0;z-index:6;animation:fade {dur}s {t_in:.3f}s forwards">{phone(img, crop)}</div>'
def ring(x, y, t, c=GOLD, n=2):
    return ''.join(f'<div class="a" style="position:absolute;left:{x - 52:.0f}px;top:{y - 52:.0f}px;width:104px;height:104px;border-radius:50%;border:10px solid {c};z-index:45;animation:ring .5s {t + k * .16:.3f}s forwards"></div>' for k in range(n))
def lab(t, x, y, d, rot=-3, bgc=PINK, size=42):
    return f'<div class="call a" style="left:{x}px;top:{y}px;transform:rotate({rot}deg);background:{bgc};font-size:{size}px;animation:pop .3s {d:.3f}s forwards">{t}</div>'
def ttl(t, d=0.0, top=250, size=76): return f'<div class="ttl a" style="top:{top}px;font-size:{size}px;animation:slam .4s {d:.3f}s forwards"><span style="display:inline-block;background:rgba(6,42,85,.92);border:5px solid {GOLD};border-radius:34px;padding:16px 34px 20px;box-shadow:0 14px 40px rgba(0,0,0,.45)">{t}</span></div>'
Z = 1.337; FY = 400   # base framing: every app moment is shown zoomed in (Tiffany Nov 1 12:22am), css crop+15 lands at y=400
def zcam(inner, crop, focus=None, s1=None, fy=960, d=0.0, dur=.5):
    y0 = TOP + 15 * K; tx0, ty0 = 540 - 540 * Z, FY - y0 * Z
    if focus is None: tx1, ty1, s1 = tx0, ty0, Z
    else: tx1, ty1 = 540 - s1 * focus[0], fy - s1 * focus[1]
    return (f'<div style="position:absolute;inset:0;z-index:5;transform-origin:0 0;--x0:{tx0:.1f}px;--y0:{ty0:.1f}px;--s0:{Z};--x1:{tx1:.1f}px;--y1:{ty1:.1f}px;--s1:{s1};'
            f'transform:translate({tx0:.1f}px,{ty0:.1f}px) scale({Z});animation:cam {dur:.3f}s {d:.3f}s cubic-bezier(.45,0,.2,1) forwards">{inner}</div>')
def cam(inner, x0=0, y0=0, s0=1, x1=0, y1=0, s1=1, d=0, dur=.5, ox=540, oy=960):
    return (f'<div style="position:absolute;inset:0;z-index:5;transform-origin:{ox}px {oy}px;--x0:{x0}px;--y0:{y0}px;--s0:{s0};--x1:{x1}px;--y1:{y1}px;--s1:{s1};'
            f'transform:translate({x0}px,{y0}px) scale({s0});animation:cam {dur:.3f}s {d:.3f}s cubic-bezier(.45,0,.2,1) forwards">{inner}</div>')
def stamp_on(kind, t):
    if kind == 'yes':
        return f'<div style="position:absolute;left:34px;top:46px;--r:-14deg;opacity:0;animation:stmp .22s {t:.3f}s forwards;border:12px solid {PINK};color:{PINK};border-radius:30px;padding:2px 34px;font:400 150px/1.1 Cap;background:rgba(255,255,255,.92);z-index:3">&hearts;</div>'
    return f'<div style="position:absolute;right:34px;top:46px;--r:14deg;opacity:0;animation:stmp .22s {t:.3f}s forwards;border:12px solid {SLATE};color:{SLATE};border-radius:30px;padding:2px 40px;font:400 140px/1.1 Cap;background:rgba(255,255,255,.92);z-index:3">&#10005;</div>'
def big_stamp(kind, t):
    c = PINK if kind == 'yes' else SLATE; g = '&hearts;' if kind == 'yes' else '&#10005;'
    return f'<div class="a" style="position:absolute;left:390px;top:820px;width:300px;height:300px;border-radius:50%;background:{c};border:10px solid #fff;color:#fff;display:grid;place-items:center;font:400 190px/1 Cap;z-index:50;--r:{-10 if kind == "yes" else 10}deg;animation:stmp .25s {t:.3f}s forwards;box-shadow:0 20px 60px rgba(0,0,0,.4)">{g}</div>'
def sparks(t0, cx=540, cy=960, n=18):
    rr = random.Random(int(t0 * 100) + cx); out = []
    for k in range(n):
        ang = k / n * 6.283 + rr.random() * .3; d = rr.randint(360, 600); w = rr.randint(44, 92)
        sym = HEART.format(c=rr.choice([PINK, BLUSH, '#fff'])) if k % 3 else STAR.format(c=GOLD)
        out.append(f'<div class="a" style="position:absolute;left:{cx - w // 2}px;top:{cy - w // 2}px;width:{w}px;height:{w}px;z-index:55;--x:{int(math.cos(ang) * d)}px;--y:{int(math.sin(ang) * d)}px;animation:spark 1.2s {t0 + rr.random() * .12:.2f}s ease-out forwards">{sym}</div>')
    return ''.join(out)
def curtains(t_open, dur=.75, closed_only=False):
    fold = f'repeating-linear-gradient(90deg,#6d0c18 0px,#a3182a 34px,#c8283a 52px,#a3182a 70px,#6d0c18 104px)'
    trim = f'linear-gradient(90deg,transparent,transparent)'
    an = lambda k: '' if closed_only else f'animation:{k} {dur:.2f}s {t_open:.3f}s cubic-bezier(.6,0,.3,1) forwards;'
    panel = lambda side, k: (f'<div style="position:absolute;top:0;bottom:0;{side}:0;width:50%;z-index:70;background:{fold};box-shadow:inset 0 -60px 80px rgba(0,0,0,.35),0 0 40px rgba(0,0,0,.6);{an(k)}">'
                              f'<div style="position:absolute;{"right" if side == "left" else "left"}:0;top:0;bottom:0;width:18px;background:linear-gradient(90deg,{GOLD},#b8862f,{GOLD})"></div></div>')
    valance = f'<div style="position:absolute;left:0;right:0;top:0;height:120px;z-index:72;background:{fold};border-bottom:12px solid {GOLD};border-radius:0 0 50% 50%/0 0 40px 40px;box-shadow:0 10px 30px rgba(0,0,0,.5)"></div>'
    return panel('left', 'curL') + panel('right', 'curR') + valance

# ---- scenes
CROP = 105               # deck screens: tiles strip + mat card (rule 22: tiles big, not a sliver)
CARD = META['s0']        # deck card box (viewport css)
def swipe(i, kind, title, label, t0, beats, bgimg=None, crop=CROP, deck='m', card_key=None, rot_lab=-3):
    secs = beats * B; key = card_key or f's{i}'; bx, by, bw, bh = META[key]
    t_st, t_go = B * .9, B * 1.5
    btn = META.get(f'{key}-btn')
    fly = (f'<div style="position:absolute;left:{sx(bx):.0f}px;top:{sy(by, crop):.0f}px;width:{bw * K:.0f}px;z-index:20;transform-origin:50% 120%;'
           f'animation:{"swR" if kind == "yes" else "swL"} {B * 1.4:.3f}s {t_go:.3f}s cubic-bezier(.5,0,.8,.6) both">'
           f'<img src="{u(key + "-card.png")}" style="width:100%;display:block;border-radius:{14 * K:.0f}px;box-shadow:0 30px 70px rgba(0,0,0,.45)">'
           + stamp_on(kind, t_st) + '</div>')
    taps = ring(sx(btn[0] + btn[2] / 2), sy(btn[1] + btn[3] / 2, crop), t_st - .12, PINK if kind == 'yes' else '#fff', 1) if btn else ''
    clip = f'<div style="position:absolute;left:{PX + P:.0f}px;top:{TOP:.0f}px;width:{PW - 2 * P:.0f}px;height:1600px;overflow:hidden;z-index:19;pointer-events:none"></div>'
    body = ttl(title) + zcam(phone(bgimg or f'{key}-a.png', crop) + fly + taps, crop) + lab(label, 110, 1300, t_st, rot_lab, PINK if kind == 'yes' else SLATE)
    return body, secs

def scene_list(mode):
    S = []
    def add(name, fn, beats):
        S.append((name, fn, beats))
    # 0 HOOK: curtains part on the beat, Nutcracker Ballet tiles in a gold frame, the dating question
    def hook(t0, beats=6):
        tile = f'{CAP}/tile_full.jpg'
        body = (f'<div class="a" style="position:absolute;left:190px;top:700px;width:700px;height:700px;z-index:10;animation:pop .45s {B * 1.6:.3f}s forwards">'
                f'<div style="position:absolute;inset:0;border-radius:40px;border:14px solid {GOLD};box-shadow:0 0 0 8px #fff,0 30px 80px rgba(0,0,0,.55);overflow:hidden"><img src="file://{tile}" style="width:100%;height:100%;object-fit:cover"></div></div>'
                + f'<div class="a cap" style="position:absolute;left:40px;right:40px;top:300px;text-align:center;z-index:80;font-size:90px;animation:slam .4s 0s forwards;text-shadow:0 8px 0 rgba(0,0,0,.25)">Nutcracker Ballet</div>'
                + f'<div class="a" style="position:absolute;left:40px;right:40px;top:430px;text-align:center;z-index:80;font:italic 600 62px/1.15 PF;color:{GOLD};animation:slam .4s {B * 2:.3f}s forwards;text-shadow:0 6px 18px rgba(0,0,0,.5)">needs a date for the holidays</div>'
                + lab('Mahj Squad tiles', 343, 1420, B * 3, -3, PINK)
                + curtains(B * 1.0, B * 2) + sparks(B * 1.7, 540, 1050, 14))
        return body, beats * B
    def search(t0, beats=3):
        sb = META['search_btn']; crop = 330
        body = ttl('Pick her tiles') + phone('01-search.png', crop) + ring(sx(sb[0] + sb[2] / 2), sy(sb[1] + sb[3] / 2, crop), B * 1.2) + lab('Nutcracker &rarr; tap', 560, sy(sb[1] + sb[3] * .3, crop), B * 1.4, 4, NAVY)
        return body, beats * B
    def chip(before, after, bb, title, label, beats, front_after=None, lab_y=None):
        def f(t0):
            crop = 85; cx, cy = sx(bb[0] + bb[2] / 2), sy(bb[1] + bb[3] / 2, crop)
            s1 = 1.75; ox, oy = cx, cy
            inner = phone(before, crop) + layer(after, crop, B * 2) + ring(cx, cy, B * 1.3, GOLD, 2)
            body = ttl(title) + zcam(inner, crop, (cx, cy), 2.4, 980, B * .1, B * 1.0) + lab(label, 150, 1360 if lab_y is None else lab_y, B * 2.1, -2, PINK)
            return body, beats * B
        return f
    def landing(sukey, img, cardkey, title, label, beats, slot=0):
        def f(t0):
            su = META[sukey]; th = su['th'][slot]; box = su['box']; crop = box[1] - 260
            tx, ty, tw = sx(th[0]), sy(th[1], crop), th[2] * K
            cx, cy = sx(box[0] + box[2] / 2), sy(box[1] + box[3] / 2, crop)
            cover = f'<div style="position:absolute;left:{tx - 4:.0f}px;top:{ty - 4:.0f}px;width:{tw + 8:.0f}px;height:{tw + 8:.0f}px;background:#fbefe9;z-index:7"></div>'
            flyin = (f'<div style="position:absolute;left:{tx:.0f}px;top:{ty:.0f}px;width:{tw:.0f}px;height:{tw:.0f}px;z-index:8;transform-origin:0 0;--fx:{700 - tx:.0f}px;--fy:{-600:.0f}px;--fs:9;'
                     f'animation:land {B * 1.3:.3f}s {B * .2:.3f}s cubic-bezier(.3,.1,.2,1) both"><img src="file://{CAP}/dump/{cardkey}.png" style="width:100%;height:100%;object-fit:cover;border-radius:6px;box-shadow:0 6px 16px rgba(0,0,0,.35)"></div>')
            inner = phone(img, crop) + cover + flyin + ring(tx + tw / 2, ty + tw / 2, B * 1.5, PINK, 1)
            body = ttl(title) + zcam(inner, crop, (cx, cy), 2.05, 1000, B * 1.5, B * .9) + lab(label, 640, 1180, B * 2.4, 3, NAVY)
            return body, beats * B
        return f
    def pick(t0, beats=3):
        su = META['su_final']; pb = META['pickbtn']; crop = 300
        cx, cy = sx(pb[0] + pb[2] / 2), sy(pb[1] + pb[3] / 2, crop)
        inner = phone('30-suitors.png', crop)
        inner += ring(cx, cy, B * 1.3, PINK, 2)
        body = ttl('Which suitor<br>is <em>the one</em>?') + zcam(inner, crop, (cx, cy), 2.3, 1000, B * .1, B * .9) + lab('Clara, it&rsquo;s you &hearts;', 300, 1270, B * 1.5, -3, PINK)
        return body, beats * B
    def rzoom(t0, beats=6):
        crop = 85; z = META['rz']; zx, zy = sx(z[0] + z[2] / 2), sy(z[1] + z[3] / 2, crop)
        steps = ''.join(layer(f'40-rz{j}.png', crop, B * (j + .9)) for j in range(1, 4)) + layer('40-rz4.png', crop, B * 4.2, .3)
        taps = ''.join(ring(zx, zy, B * (j + .7), GOLD, 1) for j in range(3))
        pls = ''.join(f'<div class="a cap" style="position:absolute;left:{zx - 40 + j * 0:.0f}px;top:{zy - 150 - j * 20:.0f}px;font-size:90px;color:{GOLD};z-index:46;text-shadow:0 4px 12px rgba(0,0,0,.6);animation:pop .25s {B * (j + .7):.3f}s forwards,out .2s {B * (j + 1.5):.3f}s forwards">+</div>' for j in range(3))
        mx, my = sx(195), sy(210, crop)
        inner = phone('40-rz0.png', crop) + steps
        inner += taps + pls
        body = (ttl('Racks: + + + zoom<br>on her mat') + zcam(inner, crop, (mx, my), 2.2, 1000, B * 3.6, B * 1.4)
                + lab('see her blues &amp; magentas up close', 110, 1380, B * 4.4, -2, NAVY, 38))
        return body, beats * B
    def rchips(t0, beats=3):
        crop = 85; w = META['woodchip']; cx, cy = sx(w[0] + w[2] / 2), sy(w[1] + w[3] / 2, crop)
        inner = phone('45-chips.png', crop) + layer('46-wood.png', crop, B * 1.6)
        inner += ring(cx, cy, B * 1.0, GOLD, 2)
        body = ttl('Pick a rack type') + zcam(inner, crop, (cx, cy), 2.0, 900, B * .1, B * .8) + lab('Wood &middot; Tortoise &middot; Metallic &middot; Clear', 120, 1080, B * 1.2, 2, NAVY, 38)
        return body, beats * B
    def rswipe(j, kind, title, label, beats):
        def f(t0):
            crop = 85; key = f'r{j}'; bx, by, bw, bh = META[key]
            t_st, t_go = B * .9, B * 1.5
            fly = (f'<div style="position:absolute;left:{sx(bx):.0f}px;top:{sy(by, crop):.0f}px;width:{bw * K:.0f}px;z-index:20;transform-origin:50% 120%;'
                   f'animation:{"swR" if kind == "yes" else "swL"} {B * 1.4:.3f}s {t_go:.3f}s cubic-bezier(.5,0,.8,.6) both">'
                   f'<img src="{u(key + "-card.png")}" style="width:100%;display:block;border-radius:{14 * K:.0f}px;box-shadow:0 30px 70px rgba(0,0,0,.45)">' + stamp_on(kind, t_st) + '</div>')
            body = ttl(title) + zcam(phone(f'{key}-a.png', crop) + fly, crop) + lab(label, 110, 1420, t_st, -3, PINK if kind == 'yes' else SLATE)
            return body, beats * B
        return f
    def match(t0, beats=4):
        tile = f'{CAP}/tile_full.jpg'; mat = f'{CAP}/dump/clara.png'
        circ = lambda src, x, d, pos: f'<div class="a" style="position:absolute;top:640px;left:{x}px;width:400px;height:400px;border-radius:50%;border:14px solid {GOLD};overflow:hidden;box-shadow:0 0 0 8px #fff,0 24px 60px rgba(0,0,0,.5);z-index:10;animation:pop .4s {d:.3f}s forwards"><img src="file://{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos}"></div>'
        body = (f'<div class="a" style="position:absolute;top:300px;left:0;right:0;text-align:center;z-index:30;font:italic 600 150px/1 PF;color:#fff;text-shadow:0 0 50px {PINK};animation:slam .45s 0s forwards">It&rsquo;s a match!</div>'
                + circ(tile, 90, B * .6, '50% 50%') + circ(mat, 590, B * .9, '50% 35%')
                + f'<div class="a" style="position:absolute;top:770px;left:470px;width:140px;height:140px;z-index:12;animation:pop .4s {B * 1.3:.3f}s forwards">{HEART.format(c=PINK)}</div>'
                + f'<div class="a" style="position:absolute;left:0;right:0;top:1110px;text-align:center;z-index:30;animation:up .4s {B * 1.6:.3f}s forwards"><div class="cap" style="font-size:70px">Nutcracker Ballet &times; Clara</div><div style="font:700 40px Bit;color:{BLUSH};margin-top:18px">Mahj Squad tiles &middot; Oh My Mahjong mat</div><div style="font:700 40px Bit;color:{BLUSH};margin-top:8px">Bird &amp; Bamboo Magenta + Light Blue racks</div></div>'
                + sparks(B * 1.3, 540, 840, 20))
        return body, beats * B
    def card(t0, beats=5):
        body = (f'<div class="a" style="position:absolute;left:0;right:0;top:120px;z-index:10;animation:pop .45s 0s forwards"><img src="file://{CAP}/storycard.jpg" style="height:1660px;width:auto;display:block;margin:0 auto;border-radius:30px;border:10px solid {GOLD};box-shadow:0 30px 80px rgba(0,0,0,.55)"></div>'
                + lab('your match card, ready to share', 230, 1640, B * 1.5, -2, PINK, 40))
        return body, beats * B
    def shop(t0, beats=4):
        crop = 140
        inner = phone('70-shop.png', crop)
        mx, my = sx(195), sy(330, crop)
        body = ttl('Then shop it all') + zcam(inner, crop, (mx, my), 1.75, 1000, B * .3, B * 1.2) + lab('code MAHJMATCH saves at our partners', 90, 1420, B * 1.4, -2, PINK, 40)
        return body, beats * B
    def cta(t0, beats=6):
        body = (f'<img class="a" src="file://{R}/assets/brand/flame-heart.png" style="position:absolute;left:470px;top:300px;width:140px;z-index:10;animation:pop .4s 0s forwards">'
                + f'<div class="a cap" style="position:absolute;left:30px;right:30px;top:500px;text-align:center;font-size:104px;white-space:nowrap;z-index:10;animation:slam .45s {B * .5:.3f}s forwards">{FYM}</div>'
                + f'<div class="a" style="position:absolute;left:60px;right:60px;top:700px;text-align:center;font:italic 600 60px/1.25 PF;color:{GOLD};z-index:10;animation:up .4s {B * 1.5:.3f}s forwards">150+ holiday mats. Your tiles.<br>Racks to match.</div>'
                + f'<div class="a" style="position:absolute;left:0;right:0;top:960px;text-align:center;z-index:10;animation:pop .4s {B * 2.5:.3f}s forwards"><span style="display:inline-block;background:{PINK};border:5px solid #fff;color:#fff;border-radius:999px;padding:24px 40px;font:400 54px Cap;box-shadow:0 20px 50px rgba(0,0,0,.4);white-space:nowrap">Shop now &middot; use code MAHJMATCH</span></div>'
                + f'<div class="a" style="position:absolute;left:0;right:0;top:1150px;text-align:center;font:700 44px Bit;letter-spacing:.03em;z-index:10;animation:up .4s {B * 2.8:.3f}s forwards">Link in bio &middot; mahjmatchmaker.com</div>'
                + sparks(B * .6, 540, 620, 16))
        return body, beats * B
    DUMP = f'{CAP}/dump'
    def tagp(t, x, y, d, rot=-3, c=NAVY, size=40): return lab(t, x, y, d, rot, c, size)
    def dumpA(t0, beats=4):
        mats = [('claras-dream', 'Clara&rsquo;s Dream Christmas &middot; Mahj Squad'), ('pretty-little', 'Pretty Little Christmas &middot; Peace Love Mahjong'),
                ('tied-bow', 'Tied With A Bow &middot; Peace Love Mahjong'), ('clara', 'Clara &middot; Oh My Mahjong')]
        top = (f'<div style="position:absolute;left:0;right:0;top:0;height:900px;z-index:8;overflow:hidden;border-bottom:14px solid {GOLD}">'
               f'<img src="file://{CAP}/tile_full.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 45%"></div>'
               + tagp('Nutcracker Ballet &middot; Mahj Squad', 180, 690, 0, -2, PINK))
        bot = ''.join(f'<div class="a" style="position:absolute;left:0;right:0;top:914px;bottom:0;z-index:{9 + j};overflow:hidden;animation:fade .06s {j * B:.3f}s forwards">'
                      f'<img src="file://{DUMP}/{m}.png" style="width:100%;height:100%;object-fit:cover;object-position:50% 30%;transform:scale(1.04)">' + tagp(t, 90, 426, .02, [-3, 2, -2, 3][j], NAVY, 38) + '</div>' for j, (m, t) in enumerate(mats))
        hdr = f'<div class="a cap" style="position:absolute;left:0;right:0;top:300px;text-align:center;z-index:30;font-size:96px;text-shadow:0 6px 24px rgba(0,0,0,.6);animation:slam .35s 0s forwards">Try her on.</div>'
        return top + bot + hdr + ''.join(f'<div class="a" style="position:absolute;left:0;right:0;top:914px;height:20px;z-index:20;background:#fff;animation:out .15s {j * B:.3f}s forwards;opacity:1"></div>' for j in range(1, 4)), beats * B
    def dumpB(t0, beats=4):
        racks = [('bb-magenta', 'Bird &amp; Bamboo Magenta'), ('bb-lightblue', 'Bird &amp; Bamboo Light Blue'), ('bb-balletpink', 'Bird &amp; Bamboo Ballet Pink'), ('bb-mulberry', 'Bird &amp; Bamboo Mulberry')]
        base = (f'<div style="position:absolute;inset:0;z-index:8;overflow:hidden"><img src="file://{DUMP}/clara.png" style="position:absolute;left:-200px;top:300px;width:1480px;height:1480px;object-fit:cover;--x0:0px;--y0:0px;--s0:1;--x1:-60px;--y1:-40px;--s1:1.12;animation:cam {beats * B:.2f}s 0s linear forwards"></div>'
                + f'<div style="position:absolute;left:0;right:0;top:0;height:300px;z-index:9;background:linear-gradient({NAVY},{NAVY}ee 70%,transparent)"></div>')
        rk = ''.join(f'<div class="a" style="position:absolute;left:60px;right:60px;top:{620 + j * 190}px;z-index:{12 + j};--r:{[-4, 3, -2, 4][j]}deg;animation:stmp .22s {j * B:.3f}s forwards">'
                     f'<img src="file://{DUMP}/{r}.png" style="width:100%;display:block;filter:drop-shadow(0 14px 22px rgba(0,0,0,.55))"></div>'
                     + tagp(t, 120 + (j % 2) * 360, 760 + j * 190, j * B + .05, [-3, 3, -2, 2][j], NAVY, 34) for j, (r, t) in enumerate(racks))
        hdr = f'<div class="a cap" style="position:absolute;left:0;right:0;top:300px;text-align:center;z-index:30;font-size:88px;text-shadow:0 6px 24px rgba(0,0,0,.6);animation:slam .35s 0s forwards">Now, <span class="pf" style="color:{GOLD}">racks</span>.</div>'
        return base + rk + hdr + tagp('Clara &middot; Oh My Mahjong', 300, 1440, B * .5, 2, PINK, 38), beats * B
    def dumpC(t0, beats=4):
        mats = [('very-merry', 'Very Merry Mahj &middot; Anders Ruff'), ('holly-jolly', 'Holly Jolly Christmas &middot; Bam! Let&rsquo;s Mahjong'),
                ('candy-cane-ar', 'Candy Cane Lane &middot; Anders Ruff'), ('nutcracker-noel', 'Nutcracker Noel &middot; Peace Love Mahjong')]
        fl = ''.join(f'<div class="a" style="position:absolute;inset:0;z-index:{8 + j};overflow:hidden;animation:fade .05s {j * B:.3f}s forwards">'
                     f'<img src="file://{DUMP}/{m}.png" style="width:100%;height:100%;object-fit:cover;--x0:0px;--y0:0px;--s0:1.18;--x1:0px;--y1:0px;--s1:1.02;animation:cam {B * 1.2:.3f}s {j * B:.3f}s ease-out both">' + tagp(t, 80, 1330, .02, [-3, 2, -2, 3][j], NAVY, 36) + '</div>' for j, (m, t) in enumerate(mats))
        hdr = (f'<div style="position:absolute;left:0;right:0;top:250px;z-index:30;text-align:center"><div class="a" style="display:inline-block;background:{NAVY}e6;border:6px solid {GOLD};border-radius:36px;padding:22px 44px;animation:slam .35s 0s forwards">'
               f'<div class="cap" style="font-size:96px;color:#fff">150+ holiday mats</div><div style="font:italic 600 52px PF;color:{GOLD};margin-top:6px">all in Find <span>Your</span> Mat&#8209;ch</div></div></div>')
        return fl + hdr, beats * B
    if mode == 'full':
        add('hook', lambda t0: hook(t0, 5), 5); add('dumpA', dumpA, 4)
        add('hol', chip('10-hol-before.png', '11-hol-after.png', META['holc'], 'Tap <em>Holiday</em>', 'only her holiday matches now', 4), 4)
        add('s0', lambda t0: swipe(0, 'yes', 'Swipe &hearts; or &#10005;', '&hearts; Clara&rsquo;s Dream Christmas &middot; Mahj Squad', t0, 3), 3)
        add('l0', landing('su0', 'su0.png', 'claras-dream', 'Hearts land in<br>your <em>suitors</em>', '1 suitor', 3), 3)
        add('s1', lambda t0: swipe(1, 'no', 'Not the one? &#10005;', '&#10005; Yuletide &middot; Oh My Mahjong', t0, 3), 3)
        add('blue', chip('20-blue-before.png', '21b-blue-after.png', META['blue'], 'Add a color: <em>blue</em>', 'the deck changes', 4), 4)
        add('s2', lambda t0: swipe(2, 'yes', 'Love her? &hearts;', '&hearts; Pretty Little Christmas &middot; Peace Love Mahjong', t0, 3, rot_lab=-2), 3)
        add('s3', lambda t0: swipe(3, 'yes', '<em>Clara</em>, for a Nutcracker?', '&hearts; Clara &middot; Oh My Mahjong', t0, 3), 3)
        add('l3', landing('su3', 'su3.png', 'clara', '3 suitors.<br>One <em>holiday date</em>.', '3 suitors', 3), 3)
        add('pick', pick, 3); add('dumpB', dumpB, 4); add('rz', rzoom, 6); add('chips', rchips, 3)
        add('r0', rswipe(0, 'no', 'Wood? &#10005;', '&#10005; Peace Love Mahjong Oak', 3), 3)
        add('r1', rswipe(1, 'yes', 'Her magenta &hearts;', '&hearts; Bird &amp; Bamboo Magenta', 3), 3)
        add('r2', rswipe(2, 'yes', 'Her sky blue &hearts;', '&hearts; Bird &amp; Bamboo Light Blue', 3), 3)
        add('dumpC', dumpC, 4); add('match', match, 4); add('card', lambda t0: card(t0, 4), 4); add('shop', shop, 4); add('cta', lambda t0: cta(t0, 4), 4)
    else:
        add('hook', lambda t0: hook(t0, 4), 4)
        add('s1', lambda t0: swipe(1, 'no', 'Not the one? &#10005;', '&#10005; Yuletide &middot; Oh My Mahjong', t0, 3), 3)
        add('s3', lambda t0: swipe(3, 'yes', 'Love her? &hearts;', '&hearts; Clara &middot; Oh My Mahjong', t0, 3), 3)
        add('l3', landing('su3', 'su3.png', 'clara', 'Hearts land in<br>your <em>suitors</em>', '3 suitors', 3), 3)
        add('match', match, 4); add('cta', lambda t0: cta(t0, 4), 4)
    return S

async def shoot(pg, name, html, secs):
    hp = f'{FR}/{name}.html'; open(hp, 'w').write(html)
    await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(250)
    d = f'{FR}/{name}'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    await pg.evaluate('document.getAnimations().forEach(a=>a.pause())')
    n = int(round(secs * FPS))
    for i in range(n):
        await pg.evaluate(f'document.getAnimations().forEach(a=>{{a.currentTime={i * 1000 / FPS}}})')
        await pg.screenshot(path=f'{d}/{i:04d}.jpg', type='jpeg', quality=93)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{d}/%04d.jpg', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', f'{d}.mp4'], check=True)
    shutil.rmtree(d)
    return f'{d}.mp4'

async def main():
    from playwright.async_api import async_playwright
    S = scene_list(MODE); ONLY = os.environ.get('ONLY'); clips = []; t = 0.0; marks = []
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for name, fn, beats in S:
            body, secs = fn(t); marks.append((name, round(t, 3), beats))
            if ONLY and name not in ONLY.split(',') and os.path.exists(f'{FR}/{name}.mp4'): clips.append(f'{FR}/{name}.mp4')
            else: clips.append(await shoot(pg, name, page(body, t, name not in ('card',)), secs))
            t += beats * B
        await b.close()
    with open(f'{FR}/all.txt', 'w') as f:
        for c in clips: f.write(f"file '{c}'\n")
    out = f'{HERE}/fym-holiday-{"reel" if MODE == "full" else "hook"}-nutcracker.mp4' if not NOBG else f'/dev/shm/fym-holiday/nobg-{MODE}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{FR}/all.txt', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', out], check=True)
    if not NOBG: json.dump({'bpm': BPM, 'beat_s': B, 'scenes': marks, 'total_s': round(t, 3)}, open(f'{HERE}/beats-{MODE}.json', 'w'), indent=1)
    print('out', out, 'secs', round(t, 2))
asyncio.run(main())
