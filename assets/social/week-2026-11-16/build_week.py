"""Week Nov 16-22 FINAL media for the Planoly drafts (Friday next-week prep task, Fri Nov 13).
Source = existing work only (SOCIAL-SYSTEM "never start from zero"):
  Mon  Deco (Lagoon) intro carousel = assets/social/deco-lagoon-launch/intro-framed/1-8 (the 8-slide profile set) + 8 stories
  Tue  It's a mat-ch! Deco (Lagoon) x Pretty in Plum (Mahjong Register) via scripts/social/its_a_match/render.py + story
  Wed  Deco (Lagoon) carousel reel (Juniper template: tall album cover, the 8 slides, slow zoom + cross-fades, animated end card)
  Thu  Deco (Lagoon) on Gilded Peacock in Find Your Mat-ch: the kit's 3 phones (Table view, Aerial, Up close) + stories
  Fri  It's a mat-ch! Deco (Lagoon) x Wren (Britt Mills) + story (Dear Santa reel v3 NOT used: it says 'every Christmas mat')
  Sat  story-only: Deco (Lagoon) in Table view on 4 in-stock mats (kit fym-table squares)
  Sun  story-only recap (frame 1 of Mon, Tue, Thu, Fri, Sat)
Usage: python3 build_week.py"""
import asyncio, os, shutil, subprocess, sys
from PIL import Image
R = '/home/claude/mahjmatchmaker-data'; K = f'{R}/assets/social/deco-lagoon-launch'; O = f'{R}/assets/social/week-2026-11-16/final'
F = f'file://{R}/scripts/social/tileprofile/fonts'
BB, BM, BG, RG = '@bambirdboutique', '@brittmillsdesign', '@bougiemahjong', 'Mahjong Register'
CREAM = (247, 238, 228)
INTRO = ['1', '2', '3', '4', '5', '6', '6b-play-the-field', '7']  # intro-framed order (6b = 'But she likes to play the field')
os.makedirs('/dev/shm/wk16', exist_ok=True)

def story_html(src, mentions, label=''):
    lab = f'<div class=l>{label}</div>' if label else ''
    return f"""<meta charset=utf-8><style>@font-face{{font-family:Bit;src:url({F}/bitter-latin-700-normal.woff2);font-weight:700}}
@font-face{{font-family:Capra;src:url({F}/Caprasimo.ttf)}}
*{{margin:0}}body{{width:1080px;height:1920px;background:#faf3ea;position:relative;font-family:Bit}}
img{{position:absolute;left:65px;top:270px;width:950px;height:1188px;object-fit:cover;border-radius:18px;box-shadow:0 10px 30px rgba(6,42,85,.18)}}
.l{{position:absolute;left:60px;right:60px;bottom:1668px;text-align:center;font:400 54px/1.08 Capra;color:#054689}}
.m{{position:absolute;left:40px;right:40px;top:1478px;text-align:center;font:700 34px/1.35 Bit;color:#062a55}}</style>
{lab}<img src="file://{src}"><div class=m>{' · '.join(mentions)}</div>"""

def feed_phone_html(phone, label, sub):
    return f"""<meta charset=utf-8><style>@font-face{{font-family:Bit;src:url({F}/bitter-latin-700-normal.woff2);font-weight:700}}
@font-face{{font-family:Capra;src:url({F}/Caprasimo.ttf)}}
*{{margin:0}}body{{width:1080px;height:1350px;background:#f7eee4;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Bit}}
.l{{font:400 76px Capra;color:#054689;text-align:center}}.s{{font:700 30px Bit;color:#c8325f;letter-spacing:.14em;text-transform:uppercase;margin:10px 0 34px;text-align:center}}
img{{height:1000px;filter:drop-shadow(0 18px 34px rgba(6,42,85,.22))}}</style>
<div class=l>{label}</div><div class=s>{sub}</div><img src="file://{phone}">"""

def shoot(pg, html, out, w, h):
    pg.set_viewport_size({'width': w, 'height': h})
    open('/dev/shm/wk16/p.html', 'w').write(html); pg.goto('file:///dev/shm/wk16/p.html'); pg.wait_for_timeout(450)
    pg.screenshot(path=out, type='jpeg', quality=92)

def build_stills():
    from playwright.sync_api import sync_playwright
    # Mon: the 8 intro slides as they are (approved graphics are never changed), stories with @mentions
    men = [(BB,), (BB,), (BB,), (BB,), (BB,), (BB,), (BM, BG, RG), (BB, BM)]
    d = f'{O}/mon-lagoon-intro'; os.makedirs(d, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for i, m in enumerate(men, 1):
            shutil.copy(f'{K}/intro-framed/{INTRO[i-1]}.jpg', f'{d}/slide{i}.jpg')
            shoot(pg, story_html(f'{d}/slide{i}.jpg', m), f'{d}/story-{i}.jpg', 1080, 1920)
        # Thu: 3 phones, 3 views (Gilded Peacock, Bougie Mahjong: in stock Nov 13)
        d = f'{O}/thu-lagoon-fym'; os.makedirs(d, exist_ok=True)
        ph = f'{K}/fym-phones/deco-lagoon-fym-phone-%s-gilded-peacock.png'
        views = [('1-table', 'Table view'), ('2-aerial', 'Aerial'), ('3-upclose', 'Up close')]
        for i, (k, lab) in enumerate(views, 1):
            shoot(pg, feed_phone_html(ph % k, lab, 'Deco (Lagoon) on Gilded Peacock'), f'{d}/slide{i}.jpg', 1080, 1350)
            shoot(pg, story_html(f'{d}/slide{i}.jpg', (BB, BG)), f'{d}/story-{i}.jpg', 1080, 1920)
        # Sat: story-only Table view on 4 in-stock mats (Bam Bird x2, Bougie, Mahjong Register)
        d = f'{O}/sat-lagoon-table'; os.makedirs(d, exist_ok=True)
        tv = [('deco-dragon-mulberry', 'Deco Dragon (Mulberry)', (BB,)), ('deco-neoprene', 'Deco Neoprene', (BB,)),
              ('gilded-peacock', 'Gilded Peacock', (BB, BG)), ('pretty-in-plum-premium', 'Pretty in Plum', (BB, RG))]
        for i, (k, name, m) in enumerate(tv, 1):
            shoot(pg, story_html(f'{K}/fym-table/deco-lagoon-table-{k}.jpg', m, f'Deco (Lagoon) on {name}'), f'{d}/story-{i}.jpg', 1080, 1920)
        b.close()

async def build_match(mat, mat_brand, mat_img, d):
    sys.path.insert(0, f'{R}/scripts/social/its_a_match'); import render as RR, tempfile
    c = dict(tile='Deco (Lagoon)', short='Deco (Lagoon)', tile_brand='Bam Bird Boutique', mat=mat, mat_brand=mat_brand,
             count=41, tile_img=f'{R}/assets/launches/bambird-deco-tile-set/backs-only-lagoon.jpg',
             mat_img=mat_img)
    os.makedirs(d, exist_ok=True)
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, (W, Ht, html) in [('slide1', RR.slide1(c, 'feed')), ('story-1', RR.slide1(c, 'story'))]:
            html = html.replace('class=c style="font-family:Hand;', 'class=c style="position:relative;left:%dpx;font-family:Hand;' % (-15 if Ht == 1350 else -18), 1)
            pg = await b.new_page(viewport={'width': W, 'height': Ht})
            t = os.path.join(tempfile.gettempdir(), f'lag_{name}.html'); open(t, 'w').write(html)
            await pg.goto('file://' + t, wait_until='load'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
            print(name, 'broken imgs', await pg.evaluate("[...document.images].filter(i=>!i.naturalWidth).length"),
                  'overflow', await pg.evaluate("(()=>{const b=document.getElementById('blk');return b.scrollHeight-b.clientHeight})()"))
            await pg.screenshot(path=f'{d}/{name}.jpg', type='jpeg', quality=92); await pg.close()
        await b.close()

def build_reel():
    """Juniper carousel-reel template: tall cover 2.4s, 8 slides x 2.4s (slow 4% push-in) on cream, 0.4s cross-fades, end card."""
    d = f'{O}/wed-lagoon-reel'; os.makedirs(d, exist_ok=True); fps = 30
    shutil.copy(f'{R}/assets/covers/albums/reel-tall/deco-lagoon.jpg', f'{d}/reel-cover.jpg')
    srcs = [f'{R}/assets/covers/albums/reel-tall/deco-lagoon.jpg'] + [f'{K}/intro-framed/{n}.jpg' for n in INTRO]
    seg, xf = 2.4, 0.4
    def frame(src, t):
        im = Image.open(src).convert('RGB'); z = 1 + 0.04 * (t / seg)
        if im.size == (1080, 1920):
            w, h = int(1080 * z), int(1920 * z); im = im.resize((w, h), Image.LANCZOS)
            return im.crop(((w - 1080) // 2, (h - 1920) // 2, (w - 1080) // 2 + 1080, (h - 1920) // 2 + 1920))
        bg = Image.new('RGB', (1080, 1920), CREAM); w, h = int(1000 * z), int(1250 * z)
        bg.paste(im.resize((w, h), Image.LANCZOS), ((1080 - w) // 2, 285 + (1250 - h) // 2)); return bg
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', str(fps), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '/dev/shm/wk16/body.mp4'], stdin=subprocess.PIPE)
    n = int(seg * fps)
    for k, s in enumerate(srcs):
        for f in range(n):
            t = f / fps; im = frame(s, t)
            if k + 1 < len(srcs) and t > seg - xf:
                im = Image.blend(im, frame(srcs[k + 1], 0), (t - (seg - xf)) / xf)
            p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    end = f'{K}/reel/deco-lagoon-end-find-your-match-animated.mp4'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', '/dev/shm/wk16/body.mp4', '-i', end, '-f', 'lavfi', '-t', '30', '-i', 'anullsrc=r=44100:cl=stereo',
                    '-filter_complex', '[0:v]fps=30,format=yuv420p,setsar=1[a];[1:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]',
                    '-map', '[v]', '-map', '2:a', '-shortest', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-movflags', '+faststart',
                    f'{d}/deco-lagoon-carousel-reel.mp4'], check=True)

def build_sun():
    d = f'{O}/sun-recap'; os.makedirs(d, exist_ok=True)
    for n, s in enumerate(['mon-lagoon-intro/story-1.jpg', 'tue-lagoon-match/story-1.jpg', 'thu-lagoon-fym/story-1.jpg', 'fri-lagoon-match/story-1.jpg', 'sat-lagoon-table/story-1.jpg'], 1):
        shutil.copy(f'{O}/{s}', f'{d}/story-{n}.jpg')

if __name__ == '__main__':
    build_stills()
    asyncio.run(build_match('Pretty in Plum', 'Mahjong Register', f'{K}/mats/06-pretty-in-plum-premium-mahjong-register.jpg', f'{O}/tue-lagoon-match'))
    # Fri: her #14 card, Wren (Britt Mills, in stock Nov 13; #2 Reba gone, #3 Viola sold out, #4 Splash, #5 no code, #6 used Tue, #7 Thu)
    asyncio.run(build_match('Wren', 'Britt Mills', f'{K}/mats/14-wren-britt-mills.jpg', f'{O}/fri-lagoon-match'))
    if not os.path.exists(f'{O}/wed-lagoon-reel/deco-lagoon-carousel-reel.mp4'): build_reel()
    build_sun(); print('ok')
