"""Animated ending for title-card skits (Oct 19): 'Hook me up!' card with a heart burst + animated end card
(logo pops, line slides, big Find Your Match button bounces in, code MAHJMATCH). Renders ending.mp4 (30fps, silent)."""
import os, asyncio, subprocess, importlib.util
R = '/home/claude/mahjmatchmaker-data'
spec = importlib.util.spec_from_file_location('b', R + '/scripts/social/titlecards/build.py'); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
u, HEAD, PS, OUT = b.u, b.HEAD, b.PS, b.OUT
FPS = 30
HEART = '<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="{c}"/></svg>'
import random; random.seed(3)
burst = ''.join(f'<div class="h" style="--x:{random.randint(-420,420)}px;--y:{random.randint(-760,-120)}px;--r:{random.randint(-30,30)}deg;--d:{random.random()*0.5:.2f}s;width:{random.randint(50,110)}px;height:{random.randint(50,110)}px">{HEART.format(c=random.choice(["#fff3e6","#f7b6c8","#f56c8c","#c4dc8c","#a99bd0"]))}</div>' for _ in range(16))
STYLE = """<style>
@keyframes pop{0%{transform:scale(.2);opacity:0}60%{transform:scale(1.12);opacity:1}100%{transform:scale(1);opacity:1}}
@keyframes up{0%{transform:translateY(60px);opacity:0}100%{transform:none;opacity:1}}
@keyframes fly{0%{transform:translate(0,0) rotate(0) scale(.3);opacity:0}15%{opacity:1}100%{transform:translate(var(--x),var(--y)) rotate(var(--r)) scale(1);opacity:0}}
@keyframes bounce{0%{transform:scale(.3);opacity:0}55%{transform:scale(1.1);opacity:1}75%{transform:scale(.96)}100%{transform:scale(1);opacity:1}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
.a{opacity:0;animation-fill-mode:forwards;animation-timing-function:cubic-bezier(.2,.8,.2,1)}
.h{position:absolute;left:50%;top:58%;margin:-40px;opacity:0;animation:fly 1.6s var(--d) ease-out forwards}
</style>"""
HOOK = HEAD + STYLE + f"""<div class="wrap" style="background:{PS[0]};color:{PS[1]}">{burst}
  <div class="line a" style="font-size:150px;white-space:nowrap;animation:pop .6s .05s forwards">&ldquo;Hook me <i>up!</i>&rdquo;</div>
  <div class="a" style="display:flex;align-items:center;gap:22px;margin-top:60px;animation:up .5s .35s forwards"><div style="width:120px;height:120px;border-radius:50%;{b.AV['Papaya Spritz']};box-shadow:0 0 0 6px {PS[1]}"></div><div class="who" style="margin-top:0">Papaya Spritz</div></div>
</div></body></html>"""
END = HEAD + STYLE + f"""<div class="wrap" style="background:#fbe3ea;color:#d6336c">
  <div style="position:absolute;right:-200px;top:-180px;width:700px;height:700px;border-radius:50%;background:#f9d3df"></div>
  <div style="position:absolute;left:-220px;bottom:-200px;width:640px;height:640px;border-radius:50%;background:#f6e9df"></div>
  <img class="a" src="{u('assets/brand/flame-heart.png')}" style="position:relative;width:170px;animation:pop .6s .1s forwards">
  <img class="a" src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="position:relative;width:740px;margin-top:36px;animation:up .55s .45s forwards">
  <div class="line a" style="position:relative;font-size:84px;margin-top:30px;animation:up .55s .8s forwards">Hooking up <i>tiles, mats</i> &amp; <i>racks.</i></div>
  <div class="a" style="position:relative;margin-top:80px;animation:bounce .7s 1.35s forwards"><div style="background:#062a55;color:#fff;border-radius:999px;padding:36px 70px;font:700 70px Lo;animation:pulse 1.2s 2.1s ease-in-out infinite">Find Your <i>Match</i></div></div>
  <div class="a" style="position:relative;font:600 50px Bit;color:#062a55;margin-top:30px;letter-spacing:.06em;animation:up .5s 1.9s forwards">10.27 &middot; mahjmatchmaker.com</div>
  <div class="a" style="position:relative;margin-top:56px;background:#fff;border-radius:22px;padding:20px 36px;font:700 40px Bit;color:#062a55;box-shadow:0 8px 20px rgba(6,42,85,.1);animation:up .5s 2.35s forwards">Code <span style="color:#d6336c">MAHJMATCH</span> at Oh My Mahjong</div>
</div></body></html>"""

async def shoot(page, html, name, secs):
    hp = f'{OUT}/frames/{name}.html'; open(hp, 'w').write(html)
    await page.goto('file://' + hp); await page.wait_for_load_state('networkidle'); await page.evaluate('document.fonts.ready')
    d = f'{OUT}/frames/{name}'; os.makedirs(d, exist_ok=True)
    await page.evaluate('document.getAnimations().forEach(a=>a.pause())')
    for i in range(int(secs * FPS)):
        t = i * 1000 / FPS
        await page.evaluate(f'document.getAnimations().forEach(a=>{{a.currentTime={t}}})')
        await page.screenshot(path=f'{d}/{i:04d}.png')
    return d

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page(viewport={'width': 1080, 'height': 1920})
        d1 = await shoot(pg, HOOK, 'end_hook', 2.6); d2 = await shoot(pg, END, 'end_card', 4.6)
        await br.close()
    for d in (d1, d2):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{d}/%04d.png', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', f'{d}.mp4'], check=True)
    with open(f'{OUT}/frames/end_list.txt', 'w') as f: f.write(f"file '{d1}.mp4'\nfile '{d2}.mp4'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/frames/end_list.txt', '-c', 'copy', f'{OUT}/ending-hook-me-up-animated.mp4'], check=True)
asyncio.run(main()); print('ok')
