"""Season 2 reels v2 (Oct 21, Tiffany's post-Papaya rules): shared kit for the trailer + Ep 6/8/13 rebuilds.
- HEAD: brand fonts (Caprasimo display, Lora lines, Bitter kickers, Playfair italic taglines, Caveat accents).
- shoot_js(): render a page whose window.render(t) draws time t (seconds) -> mp4 (frames piped to ffmpeg).
- shoot_css(): same for a page driven by CSS animations (seeked with currentTime), like titlecards/ending.py.
- ending(): the hotline v12 ending ("Hook me up!" card + end card), parametrised per set:
  brand line "Hooking up tiles, / mats & racks", Find *Your* Mat-ch(TM) button, "10.27 . mahjmatchmaker.com",
  Code MAHJMATCH bubble, LINK IN BIO, deco = tile circle + heart + a mat that is NOT the official pair.
  All end-card text sits inside x 90-860 and above y 1180 (Reels icon column + caption band); text_boxes() checks it.
Frames/intermediates go to WORK (scratchpad), never into the repo."""
import os, asyncio, subprocess, json, random
from playwright.async_api import async_playwright

R = '/home/claude/mahjmatchmaker-data'
WORK = os.environ.get('S2W', '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/s2w/render')
FPS = 30
u = lambda p: p if p.startswith('file://') else f'file://{p if p.startswith("/") else R + "/" + p}'
F1 = f'file://{R}/assets/fonts'
F2 = f'file://{R}/scripts/social/tileprofile/fonts'
G = 'file:///usr/share/fonts/truetype/google-fonts'
NAVY, DEEP, ROSE, HPINK, HEART, BLUSH, PCREAM = '#054689', '#062a55', '#c8325f', '#d6336c', '#f56c8c', '#f7b6c8', '#fbe3ea'

HEAD = f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Cap;src:url('{F1}/Caprasimo.ttf')}}
@font-face{{font-family:Lo;src:url('{G}/Lora-Variable.ttf')}}
@font-face{{font-family:Lo;font-style:italic;src:url('{G}/Lora-Italic-Variable.ttf')}}
@font-face{{font-family:Bit;font-weight:400;src:url('{F1}/bitter-latin-400-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{F2}/bitter-latin-600-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:700;src:url('{F1}/bitter-latin-700-normal.woff2')}}
@font-face{{font-family:Pf;font-style:italic;src:url('{F1}/playfair-display-latin-400-italic.woff2')}}
@font-face{{font-family:Hand;src:url('{F2}/Caveat-Bold.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden}}
.wrap{{position:relative;width:1080px;height:1920px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px}}
.line{{font-family:Lo;font-weight:700;line-height:1.02;letter-spacing:-.015em}}
.line i{{font-style:italic;font-weight:600}}
.who{{font:600 40px Bit;margin-top:56px;opacity:.85}}
</style></head><body>"""
HEART_SVG = '<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="{c}"/></svg>'
FYM = 'Find <i>Your</i> Mat-ch<sup style="font-size:.35em;vertical-align:super;font-style:normal">&trade;</sup>'


async def _page(p):
    b = await p.chromium.launch()
    return b, await b.new_page(viewport={'width': 1080, 'height': 1920})


class _Pipe:
    """Frames go straight into ffmpeg (PNG over a pipe): no frame folders on disk (the shared disk is nearly full)."""
    def __init__(self, out, crf=16):
        self.out = out
        self.p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'png', '-i', '-',
                                   '-c:v', 'libx264', '-preset', 'slow', '-crf', str(crf), '-pix_fmt', 'yuv420p', '-r', str(FPS), out], stdin=subprocess.PIPE)
    def put(self, b): self.p.stdin.write(b)
    def close(self):
        self.p.stdin.close(); assert self.p.wait() == 0, 'ffmpeg failed'


def _shoot(html, name, n, step):
    """step(pg, i) -> awaits the page state for frame i. Renders n frames into WORK/name.mp4 (retries on a crashed screenshot)."""
    hp = f'{WORK}/{name}.html'; open(hp, 'w').write(html); out = f'{WORK}/{name}.mp4'
    async def go():
        pipe = _Pipe(out)
        try:
            async with async_playwright() as p:
                b, pg = await _page(p)
                await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle'); await pg.evaluate('document.fonts.ready')
                await pg.wait_for_timeout(300)
                await step(pg, None)
                for i in range(n):
                    await step(pg, i); pipe.put(await pg.screenshot(type='png'))
                await b.close()
        finally:
            pipe.close()
    for attempt in range(4):
        try:
            asyncio.run(go()); break
        except Exception as e:
            print('render retry', name, attempt, str(e)[:100])
    else:
        raise RuntimeError('render failed: ' + name)
    return out


def shoot_js(html, name, secs, t_off=0.0, every=1):
    """window.render(t) pages -> WORK/name.mp4 (every>1: a quick-look clip at 30/every fps)."""
    n = len(range(0, int(round(secs * FPS)), every))
    async def step(pg, i):
        if i is not None: await pg.evaluate(f'render({t_off + i * every / FPS})')
    return _shoot(html, name, n, step)


def shoot_css(html, name, secs, t0=0):
    async def step(pg, i):
        if i is None: await pg.evaluate('document.getAnimations().forEach(a=>a.pause())'); return
        await pg.evaluate(f'document.getAnimations().forEach(a=>{{a.currentTime={t0 + i * 1000 / FPS}}})')
    return _shoot(html, name, int(round(secs * FPS)), step)


def text_boxes(html, t_ms=6000, sel='.txt'):
    """Bounding boxes of every element matching sel after all CSS animations finish (end-card safe-area check)."""
    hp = f'{WORK}/_tb.html'; open(hp, 'w').write(html)
    async def go():
        async with async_playwright() as p:
            b, pg = await _page(p)
            await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle'); await pg.evaluate('document.fonts.ready')
            await pg.evaluate(f'document.getAnimations().forEach(a=>{{a.pause();a.currentTime={t_ms}}})')
            r = await pg.evaluate(f"""[...document.querySelectorAll('{sel}')].map(e=>{{const b=e.getBoundingClientRect();return [e.textContent.trim().slice(0,40),Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)]}})""")
            await b.close(); return r
    return asyncio.run(go())


def encode(d, out, crf=16):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{d}/%04d.png', '-c:v', 'libx264', '-preset', 'slow',
                    '-crf', str(crf), '-pix_fmt', 'yuv420p', '-r', str(FPS), out], check=True)
    return out


def concat(parts, out):
    """Frame-exact concat by re-encoding (all parts 1080x1920 30fps, no audio): reels stay silent, her song goes on in Edits."""
    ins = sum([['-i', p] for p in parts], [])
    fc = ''.join(f'[{i}:v]fps={FPS},setpts=PTS-STARTPTS,format=yuv420p[v{i}];' for i in range(len(parts))) + \
         ''.join(f'[v{i}]' for i in range(len(parts))) + f'concat=n={len(parts)}:v=1:a=0[v]'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow',
                    '-crf', '16', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-movflags', '+faststart', out], check=True)
    return out


def xfade(a, b, out, offset, dur):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', a, '-i', b, '-filter_complex',
                    f'[0:v]fps={FPS},format=yuv420p[a];[1:v]fps={FPS},format=yuv420p[b];[a][b]xfade=transition=fade:duration={dur}:offset={offset}[v]',
                    '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', str(FPS), out], check=True)
    return out


def cut(src, out, start_frame, end_frame=None):
    """Frames [start_frame, end_frame) of src, re-encoded."""
    sel = f"select='between(n,{start_frame},{(end_frame or 10**7) - 1})',setpts=N/{FPS}/TB"
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf', sel, '-c:v', 'libx264', '-preset', 'slow', '-crf', '14',
                    '-pix_fmt', 'yuv420p', '-r', str(FPS), out], check=True)
    return out


# ---------------- ending (hotline v12 design, scripts/social/titlecards/ending.py) ----------------
STYLE = """<style>
@keyframes pop{0%{transform:scale(.2);opacity:0}60%{transform:scale(1.12);opacity:1}100%{transform:scale(1);opacity:1}}
@keyframes popsoft{0%{transform:scale(.6);opacity:0}60%{transform:scale(1.05);opacity:1}100%{transform:scale(1);opacity:1}}
@keyframes up{0%{transform:translateY(60px);opacity:0}100%{transform:none;opacity:1}}
@keyframes fly{0%{transform:translateY(0) rotate(0) scale(.3);opacity:0}20%{transform:translateY(calc(var(--y)*.2)) rotate(calc(var(--r)*.2)) scale(1);opacity:1}70%{opacity:1}100%{transform:translateY(var(--y)) rotate(var(--r)) scale(1);opacity:0}}
@keyframes bounce{0%{transform:scale(.3);opacity:0}55%{transform:scale(1.1);opacity:1}75%{transform:scale(.96)}100%{transform:scale(1);opacity:1}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
.a{opacity:0;animation-fill-mode:forwards;animation-timing-function:cubic-bezier(.2,.8,.2,1)}
.h{position:absolute;opacity:0;animation:fly 1.6s var(--d) ease-out forwards}
</style>"""


def _hearts(cols, seed=3):
    rnd = random.Random(seed); out = []
    for k in range(14):
        top_band = k % 2 == 0
        w = rnd.randint(56, 104)
        x = rnd.choice([rnd.randint(60, 380), rnd.randint(620, 1020 - w)])
        y = rnd.randint(170, 690 - w) if top_band else rnd.randint(1350, 1720 - w)
        out.append(f'<div class="h" style="left:{x}px;top:{y}px;--y:-{rnd.randint(60, 120)}px;--r:{rnd.randint(-20, 20)}deg;--d:{0.15 + rnd.random() * 0.6:.2f}s;'
                   f'width:{w}px;height:{w}px">{HEART_SVG.format(c=rnd.choice(cols))}</div>')
    return ''.join(out)


def hook_html(name, tile, bg, fg, heart_cols):
    """'Hook me up!' card in the set's colour, hearts in two bands that never cross the text (v11/v12 rule)."""
    return HEAD + STYLE + f"""<div class="wrap" style="background:{bg};color:{fg}">{_hearts(heart_cols)}
  <div class="line a" style="font-size:132px;white-space:nowrap;animation:popsoft .6s 0s forwards">&ldquo;Hook me <i>up!</i>&rdquo;</div>
  <div class="a" style="display:flex;align-items:center;gap:22px;margin-top:60px;animation:up .5s .35s forwards"><div style="width:120px;height:120px;border-radius:50%;background:url({u(tile)}) center/cover;box-shadow:0 0 0 6px {fg}"></div><div class="who" style="margin-top:0">{name}</div></div>
</div></body></html>"""


COL_L, COL_W = 90, 770


def end_html(tile, mat, code_line, heart_col=HEART, mat_bg='center/cover'):
    """v12 end card. Every text element carries class 'txt' for the safe-area check (x 90-860, bottom <= 1180)."""
    deco = (f'<div class="a" style="position:absolute;left:{COL_L}px;width:{COL_W}px;top:1236px;display:flex;justify-content:center;align-items:center;gap:34px;animation:up .6s 2.6s forwards">'
            f'<div style="width:240px;height:240px;border-radius:50%;background:url({u(tile)}) center/cover;box-shadow:0 0 0 10px #fff,0 14px 30px rgba(6,42,85,.16)"></div>'
            f'<div style="width:100px;height:100px">{HEART_SVG.format(c=heart_col)}</div>'
            f'<div style="width:240px;height:240px;border-radius:50%;background:url({u(mat)}) {mat_bg};box-shadow:0 0 0 10px #fff,0 14px 30px rgba(6,42,85,.16)"></div></div>')
    return HEAD + STYLE + f"""<div class="wrap" style="background:#fbe3ea;color:#d6336c;justify-content:flex-start;padding:0">
  <div style="position:absolute;right:-200px;top:-180px;width:700px;height:700px;border-radius:50%;background:#f9d3df"></div>
  <div style="position:absolute;left:-220px;bottom:-200px;width:760px;height:760px;border-radius:50%;background:#f6e9df"></div>
  <div style="position:absolute;left:{COL_L}px;top:170px;width:{COL_W}px;display:flex;flex-direction:column;align-items:center">
  <img class="a" src="{u('assets/brand/flame-heart.png')}" style="width:130px;animation:pop .6s .1s forwards">
  <img class="a" src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="width:700px;margin-top:30px;animation:up .55s .45s forwards">
  <div class="line a txt" style="font-size:84px;margin-top:38px;line-height:1.1;animation:up .55s .8s forwards">Hooking up <i>tiles,</i><br><i>mats</i> &amp; <i>racks.</i></div>
  <div class="a" style="margin-top:56px;animation:bounce .7s 1.35s forwards"><div id="fym" class="txt" style="background:#062a55;color:#fff;border-radius:999px;padding:28px 54px;font:700 66px Lo;white-space:nowrap;animation:pulse 1.2s 2.1s ease-in-out infinite">{FYM}</div></div>
  <div class="a txt" style="font:600 44px Bit;color:#062a55;margin-top:32px;letter-spacing:.04em;white-space:nowrap;animation:up .5s 1.9s forwards">10.27 &middot; mahjmatchmaker.com</div>
  <div class="a txt" style="margin-top:28px;background:#fff;border-radius:22px;padding:16px 30px;font:700 36px Bit;color:#062a55;white-space:nowrap;box-shadow:0 8px 20px rgba(6,42,85,.1);animation:up .5s 2.2s forwards">{code_line}</div>
  <div class="a txt" style="margin-top:24px;background:#d6336c;color:#fff;border-radius:999px;padding:12px 34px;font:700 34px Bit;letter-spacing:.16em;white-space:nowrap;animation:up .5s 2.45s forwards">LINK IN BIO</div>
  </div>{deco}
</div></body></html>"""


def check_end(html):
    bad = []
    for txt, l, t, r, b in text_boxes(html):
        ok = l >= 90 and r <= 860 and b <= 1180
        print(f'  end-card text {"ok " if ok else "BAD"} x {l}-{r} y {t}-{b}  {txt!r}')
        if not ok: bad.append(txt)
    assert not bad, f'end card text outside the Reels safe area: {bad}'


def ending(tag, name, tile, mat, code_line, hook_bg, hook_fg, heart_cols, with_hook=True, mat_bg='center/cover', deco_heart=HEART):
    """Renders (hook.mp4?, end.mp4) for one reel. Returns the list of mp4 parts."""
    eh = end_html(tile, mat, code_line, deco_heart, mat_bg)
    check_end(eh)
    parts = []
    if with_hook:
        parts.append(shoot_css(hook_html(name, tile, hook_bg, hook_fg, heart_cols), f'{tag}-hook', 2.6, t0=200))
    parts.append(shoot_css(eh, f'{tag}-end', 4.6, t0=300))
    return parts
