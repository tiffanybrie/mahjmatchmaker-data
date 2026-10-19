"""Title-card skit reels ("silent movie" dialogue cards, Tinder-site style), Oct 19.
Big serif line on a full-bleed solid color, text in a brighter shade of the same color, one italic word for emphasis,
small speaker label under it. Navy = the Matchmaker. The tile set talks in its own color. Photos cut in between.
Usage: python3 scripts/social/titlecards/build.py   -> assets/social/titlecards/counseling-ep1-papaya/
"""
import os, asyncio, subprocess
from PIL import Image
from playwright.async_api import async_playwright

R = '/home/claude/mahjmatchmaker-data'
F = f'file://{R}/scripts/social/tileprofile/fonts'
G = 'file:///usr/share/fonts/truetype/google-fonts'
u = lambda p: f'file://{R}/{p}'
OUT = f'{R}/assets/social/titlecards/counseling-ep1-papaya'
os.makedirs(OUT + '/frames', exist_ok=True)

MM = ('#062a55', '#f7b6c8', 'The Matchmaker')            # navy, blush text
PS = ('#ec7a32', '#fff3e6', 'Papaya Spritz')              # papaya, cream text (Tiffany: papaya, not brown)
PAUSE = ('#141414', '#f2ece6', '')
END = ('#fbe3ea', '#d6336c', '')

HEAD = f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Lo;src:url('{G}/Lora-Variable.ttf')}}
@font-face{{font-family:Lo;font-style:italic;src:url('{G}/Lora-Italic-Variable.ttf')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{F}/bitter-latin-600-normal.woff2')}}
@font-face{{font-family:Hand;src:url('{F}/Caveat-Bold.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden}}
.wrap{{position:relative;width:1080px;height:1920px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px}}
.line{{font-family:Lo;font-weight:700;line-height:1.02;letter-spacing:-.015em}}
.line i{{font-style:italic;font-weight:600}}
.who{{font:600 40px Bit;margin-top:56px;opacity:.85}}
.mark{{position:absolute;bottom:90px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:14px;font:600 26px Bit;letter-spacing:.2em;text-transform:uppercase;opacity:.55}}
</style></head><body>"""

def card(pal, html, size=150, who=None, mark=True, q=True, pre=''):
    bg, fg, name = pal
    w = who if who is not None else name
    if q: html = f'&ldquo;{html}&rdquo;'
    pre = f'<div style="font-family:Lo;font-style:italic;font-size:64px;opacity:.8;margin-bottom:34px">{pre}</div>' if pre else ''
    return (HEAD + f'<div class="wrap" style="background:{bg};color:{fg}">{pre}<div class="line" style="font-size:{size}px">{html}</div>'
            + (f'<div class="who">{w}</div>' if w else '')
            + (f'<div class="mark">mahj matchmaker</div>' if mark else '') + '</div></body></html>')

def photo(img, label, note=None, pos='center'):
    return (HEAD + f'<div class="wrap" style="background:url({u(img)}) {pos}/cover;justify-content:flex-end;padding-bottom:150px">'
            + f'<div style="background:rgba(6,42,85,.88);color:#fff;font:600 38px Bit;padding:18px 34px;border-radius:999px">{label}</div>'
            + (f'<div style="margin-top:22px;background:#fff8;color:#062a55;font:600 28px Bit;padding:10px 24px;border-radius:14px">{note}</div>' if note else '')
            + '</div></body></html>')

TILE = 'assets/tiles/album/papaya-spritz.jpg'
EVID = HEAD + f"""<div class="wrap" style="background:#efe4d6">
 <div style="font-family:Hand;font-size:110px;color:#062a55;margin-bottom:40px">Exhibit A</div>
 <div style="background:#fff;padding:30px 30px 120px;box-shadow:0 30px 60px rgba(0,0,0,.18);transform:rotate(-3deg)">
  <div style="width:720px;height:720px;background:#5d4a3a;display:flex;align-items:center;justify-content:center">
   <svg width="640" height="640" viewBox="0 0 640 640" style="position:absolute;filter:drop-shadow(0 14px 18px rgba(0,0,0,.35))">
    <defs><filter id="felt"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 .78  0 0 0 0 .70  0 0 0 0 .58  0 0 0 .55 0"/><feComposite in2="SourceGraphic" operator="in"/></filter></defs>
    <rect x="0" y="0" width="640" height="640" rx="34" fill="#cdbca3"/>
    <rect x="0" y="0" width="640" height="640" rx="34" fill="#cdbca3" filter="url(#felt)"/>
    <rect x="26" y="26" width="588" height="588" rx="20" fill="none" stroke="#a8957b" stroke-width="5" stroke-dasharray="16 11"/>
    <rect x="58" y="58" width="524" height="524" rx="8" fill="none" stroke="#b9a68b" stroke-width="2"/>
   </svg>
   <div style="position:relative;width:420px;height:420px;border-radius:50%;background:url({u(TILE)}) center/cover;-webkit-mask-image:radial-gradient(circle,#000 58%,transparent 72%)"></div></div>
  <div style="font-family:Hand;font-size:62px;color:#333;margin-top:22px">her + the beige felt mat</div></div>
 <div style="font:600 30px Bit;color:#062a55;opacity:.6;margin-top:70px;letter-spacing:.06em">(a made-up mat. no real mats were harmed.)</div>
</div></body></html>"""

SHOTS = [
    (HEAD + f"""<div class="wrap" style="background:{MM[0]};color:{MM[1]}">
      <div style="width:210px;height:210px;border-radius:50%;background:#f7b6c8;display:flex;align-items:center;justify-content:center;margin-bottom:60px"><img src="{u('assets/brand/flame-heart.png')}" style="width:120px"></div>
      <div style="font:600 40px Bit;letter-spacing:.24em;text-transform:uppercase;opacity:.8">The Mahj Matchmaker</div>
      <div class="line" style="font-size:170px;margin-top:30px">Counseling <i>Sessions</i></div>
      <div class="who">Session 1 · Papaya Spritz</div></div></body></html>""", 2.6),
    (photo(TILE, 'Papaya Spritz', 'your 3-sec clip: her tiles in a jar, alone on the couch'), 2.4),
    (card(PS, 'I just don&rsquo;t know what <i>went wrong.</i>'), 2.6),
    (card(MM, 'Tell me <i>what happened.</i>'), 2.0),
    (EVID, 2.6),
    (card(MM, 'Mm&#8209;hmm.', 140), 1.2),
    (card(MM, '<i>Wow.</i>', 220), 1.2),
    (card(MM, '<span style="font-size:96px;font-weight:500">&ldquo;It&rsquo;s not you&hellip;</span><br><span style="display:inline-block;margin-top:40px">it&rsquo;s your <i>mat.</i>&rdquo;</span>', 190, pre='(whispering)', q=False), 4.0),
    (photo('assets/launches/omm-vivienne-mat/02.jpg', 'Papaya Spritz + Vivienne · Oh My Mahjong'), 2.6),
    (card(MM, 'You deserve someone who brings out your <i>best colors.</i>', 128), 3.0),
    (card(PS, 'Hook me <i>up.</i>', 190), 2.2),
    (HEAD + f"""<div class="wrap" style="background:{END[0]};color:{END[1]}">
      <img src="{u('assets/brand/flame-heart.png')}" style="width:170px;margin-bottom:50px">
      <div class="line" style="font-size:200px">It&rsquo;s a <i>match!</i></div>
      <div style="font:600 44px Bit;color:#062a55;margin-top:60px">Consider yourself hooked up.</div>
      <div style="font:600 34px Bit;color:#062a55;opacity:.7;margin-top:16px">Find Your Match · 10.27 · mahjmatchmaker.com</div>
      <img src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="position:absolute;bottom:110px;width:440px"></div></body></html>""", 3.2),
]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for i, (h, _) in enumerate(SHOTS, 1):
            hp = f'{OUT}/frames/f{i:02d}.html'; open(hp, 'w').write(h)
            await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle'); await pg.evaluate('document.fonts.ready')
            await pg.screenshot(path=f'{OUT}/frames/f{i:02d}.png')
        await b.close()
    lst = f'{OUT}/frames/list.txt'
    with open(lst, 'w') as f:
        for i, (_, d) in enumerate(SHOTS, 1): f.write(f"file 'f{i:02d}.png'\nduration {d}\n")
        f.write(f"file 'f{len(SHOTS):02d}.png'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', 'fps=30,format=yuv420p',
                    '-c:v', 'libx264', '-crf', '18', f'{OUT}/counseling-session-1-papaya-spritz.mp4'], check=True)
    ims = [Image.open(f'{OUT}/frames/f{i:02d}.png').convert('RGB').resize((270, 480)) for i in range(1, len(SHOTS) + 1)]
    cols = 7; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 280 + 10, rows * 490 + 10), (240, 236, 230))
    for k, im in enumerate(ims): sheet.paste(im, (10 + (k % cols) * 280, 10 + (k // cols) * 490))
    sheet.save(f'{OUT}/contact-sheet.jpg', quality=90)

if __name__ == '__main__':
    asyncio.run(main()); print(OUT)
