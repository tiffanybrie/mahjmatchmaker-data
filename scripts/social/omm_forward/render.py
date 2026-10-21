"""OMM-forward launch carousel (Tiffany, Oct 21 12:55pm): one post per OMM launch built on OMM's own photography,
so OMM has something to reshare, and it still points to the album / Find Your Mat-ch.

Papaya Spritz x Vivienne (Oct 21 launch). Three 1080x1350 slides, content inside y 190-1230 (Oct 21 2:12pm, Tiffany: clear of the
Planoly/IG profile header at the top; grid crop at the bottom). Headlines in Caprasimo navy (the dating-profile headline
font, never the script); logo = wordmark + 'Matching mahjong tiles, mats & racks' ribbon:
  slide1  OMM's styled pair shot (Vivienne with Papaya Spritz tiles + racks), "Made for each other",
          "Papaya Spritz tiles · Vivienne mat", OH MY MAHJONG.
  slide2  "My favorite faces": OMM photo crops of her favourite Papaya faces with short warm labels.
  slide3  Her OMM match cards from the Papaya album fanned behind "50 matches and counting", navy pill
          "Swipe all 50 of Papaya's matches / mahjmatchmaker.com", wordmark + brand line.
          Match cards are cropped above their code band (never a hard-coded % on social).
Usage: python3 scripts/social/omm_forward/render.py [out_dir]
Story (Oct 21 1:47pm): DSF=2 python3 render.py /tmp/x, then
  python3 scripts/social/its_a_match/story_frames.py slides <story-frames dir> /tmp/x/*-1-*.jpg /tmp/x/*-2-*.jpg /tmp/x/*-3-*.jpg --fit
"""
import asyncio, os, sys, html as H

R = '/home/claude/mahjmatchmaker-data'
F = f'file://{R}/scripts/social/tileprofile/fonts'
G = 'file:///usr/share/fonts/truetype/google-fonts'
u = lambda p: f'file://{R}/{p}'
NAVY, WNAVY, PINK, PINK2, PAPER, BLUSHBG = '#062a55', '#054689', '#d6336c', '#f56c8c', '#faf3ea', '#fbe3ea'
OUT = sys.argv[1] if len(sys.argv) > 1 else f'{R}/assets/social/papaya-spritz-launch/omm-forward'

PAIR = 'assets/launches/omm-papaya-spritz-tiles/site-oct19/papaya-spritz-ultimate-starter-kit-3527310.jpg'
FACES = 'assets/tiles/faces/papaya-spritz/clean'
CARDS = 'assets/cards/papaya-spritz/papaya-spritz-mahjong-tiles-oh-my-mahjong-{}-mat.jpg'
COUNT, SHORT = 50, 'Papaya'


def shell(body, H=1350):
    return f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Hand;src:url('{F}/Caveat-Bold.ttf')}}
@font-face{{font-family:Capra;src:url('{F}/Caprasimo.ttf')}}
@font-face{{font-family:Lo;src:url('{G}/Lora-Variable.ttf')}}
@font-face{{font-family:Lo;font-style:italic;src:url('{G}/Lora-Italic-Variable.ttf')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{F}/bitter-latin-600-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:700;src:url('{F}/bitter-latin-700-normal.woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:{H}px;overflow:hidden}}
.k{{font-family:Bit;font-weight:700;letter-spacing:.2em;color:{WNAVY}}}
.hd{{font-family:Capra;font-weight:400;line-height:1;color:{WNAVY};text-align:center;white-space:nowrap}}
.lk{{display:inline-flex;flex-direction:column;align-items:stretch}} .lk img{{display:block;width:100%}}
.lk b{{display:block;margin-top:.5em;background:#f56c8c;color:#fff;font-family:Bit;font-weight:700;letter-spacing:.14em;text-align:center;white-space:nowrap;padding:.5em 0 .44em;border-radius:3px}}
</style></head><body><div id=pg style="position:relative;width:1080px;height:{H}px;background:{PAPER};overflow:hidden">
<div style="position:absolute;right:-210px;top:-230px;width:700px;height:700px;border-radius:50%;background:{BLUSHBG}"></div>
<div style="position:absolute;left:-230px;bottom:-250px;width:660px;height:660px;border-radius:50%;background:{BLUSHBG};opacity:.75"></div>
{body}</div></body></html>"""


def lockup(w):
    """Wordmark WITH the tagline ribbon (Tiffany Oct 21 2:12pm; = assets/brand/mahjmatchmaker-wordmark.png, rebuilt in HTML
    so it stays sharp at any size: that PNG is only 420px wide). Never pair it with "Hooking up..." (one tagline per piece)."""
    return (f'<div class=lk style="width:{w}px"><img src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}">'
            f'<b style="font-size:{round(w*0.0315)}px">MATCHING MAHJONG TILES, MATS &amp; RACKS</b></div>')


def slide1():
    return shell(f"""
<div class=hd style="position:absolute;left:0;right:0;top:190px;font-size:88px">Made for each other</div>
<div style="position:absolute;left:150px;top:316px;width:780px;height:780px;border-radius:26px;background:#fff url('{u(PAIR)}') center/104% no-repeat;box-shadow:0 22px 50px rgba(200,80,90,.18)"></div>
<div style="position:absolute;left:0;right:0;top:1122px;text-align:center;font-family:Lo;font-weight:700;font-size:46px;color:{NAVY};line-height:1">Papaya Spritz tiles <span style="color:{PINK2}">&middot;</span> <i style="font-weight:600">Vivienne mat</i></div>
<div class=k style="position:absolute;left:0;right:0;top:1182px;text-align:center;font-size:27px">OH MY MAHJONG</div>
""")


def face(img, w):
    return (f'<div style="width:{w}px;height:{round(w*556/426)}px;border-radius:16px;background:#fff url(\'{u(FACES + "/" + img)}\') center/cover;'
            f'box-shadow:0 0 0 3px #fff,0 14px 30px rgba(6,42,85,.16)"></div>')


def group(imgs, name, sub, w=220, gap=20):
    tiles = ''.join(face(i, w) for i in imgs)
    return (f'<div style="display:flex;flex-direction:column;align-items:center">'
            f'<div style="display:flex;gap:{gap}px">{tiles}</div>'
            f'<div style="margin-top:22px;font-family:Lo;font-weight:700;font-size:38px;color:{NAVY};line-height:1.1;text-align:center">{name}</div>'
            f'<div style="margin-top:6px;font-family:Lo;font-style:italic;font-size:30px;color:{PINK};line-height:1.15;text-align:center">{sub}</div></div>')


def slide2():
    row1 = group(['dragon-coral.png', 'dragon-green.png'], 'The dancing dragons', 'always mid-dance') + \
        group(['lola-ginger.png'], 'Ginger Lola', 'the redheaded matriarch')
    row2 = group(['crane.png'], 'The crowned crane', 'the prettiest bird bam') + \
        group(['dot3.png', 'dot7.png'], 'The parasol dots', 'spritz weather, always')
    return shell(f"""
<div class=hd style="position:absolute;left:0;right:0;top:190px;font-size:96px">My favorite faces</div>
<div class=k style="position:absolute;left:0;right:0;top:304px;text-align:center;font-size:27px">PAPAYA SPRITZ &middot; OH MY MAHJONG</div>
<div style="position:absolute;left:0;right:0;top:372px;display:flex;justify-content:center;gap:64px">{row1}</div>
<div style="position:absolute;left:0;right:0;top:800px;display:flex;justify-content:center;gap:64px">{row2}</div>
""")


def card(mat, x, y, w, rot, z):
    # Oct 21 QA: box-sizing is border-box, so the image area is w-20 wide; size the image to that and crop right at the
    # code band (logo strip ends ~1242 of 1350). Before, the image was drawn w wide and the logo strip got cut mid-logo.
    iw = w - 20; h = round(iw * 1242 / 1080) + 20
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z};'
            f'background:url(\'{u(CARDS.format(mat))}\') top/{iw}px auto no-repeat;border:10px solid #fff;border-radius:14px;'
            f'box-shadow:0 18px 40px rgba(6,42,85,.22)"></div>')


def slide3():
    cards = (card('goldie', 40, 270, 380, -8, 1) + card('larkspur', 660, 270, 380, 8, 1) +
             card('vivienne', 315, 196, 450, 0, 3))
    return shell(f"""{cards}
<div style="position:absolute;left:60px;right:60px;top:744px;z-index:5;background:{PAPER};border-radius:34px;padding:34px 30px 34px;text-align:center;box-shadow:0 20px 50px rgba(6,42,85,.22)">
  <div class=hd style="font-size:66px">50 matches and counting</div>
  <div style="display:inline-block;margin-top:26px;background:{NAVY};color:#fff;border-radius:44px;padding:16px 44px 18px;line-height:1.15">
    <div style="font-family:Lo;font-weight:700;font-size:40px">Swipe all {COUNT} of {SHORT}&rsquo;s matches</div>
    <div style="font-family:Bit;font-weight:600;font-size:28px;letter-spacing:.06em;color:#f7b6c8;margin-top:4px">mahjmatchmaker.com</div>
  </div>
  <div style="margin-top:28px">{lockup(420)}</div>
</div>
""")


def slide3_story():
    """Story version of slide 3 (Oct 21 1:47pm): taller layout, bigger cards and box, so the fitted story frame fills the
    safe band instead of sitting in the middle with empty bands. Rendered on plain paper (story_frames --fit keys it)."""
    cards = (card('goldie', 20, 120, 420, -8, 1) + card('larkspur', 640, 120, 420, 8, 1) +
             card('vivienne', 250, 40, 580, 0, 3))
    return shell(f"""{cards}
<div style="position:absolute;left:30px;right:30px;top:780px;z-index:5;background:{PAPER};border-radius:40px;padding:40px 30px 40px;text-align:center;box-shadow:0 20px 50px rgba(6,42,85,.22)">
  <div class=hd style="font-size:74px">50 matches and counting</div>
  <div style="display:inline-block;margin-top:30px;background:{NAVY};color:#fff;border-radius:54px;padding:20px 52px 22px;line-height:1.15">
    <div style="font-family:Lo;font-weight:700;font-size:50px;white-space:nowrap">Swipe all {COUNT} of {SHORT}&rsquo;s matches</div>
    <div style="font-family:Bit;font-weight:600;font-size:36px;letter-spacing:.06em;color:#f7b6c8;margin-top:6px">mahjmatchmaker.com</div>
  </div>
  <div style="margin-top:34px">{lockup(540)}</div>
</div>
""", 1500)


async def main():
    if os.environ.get('STORY3') == '1':   # just the story version of slide 3 -> OUT/papaya-vivienne-omm-forward-3-story.jpg
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1500}, device_scale_factor=2)
            f = f'{OUT}/.s3story.html'; open(f, 'w').write(slide3_story())
            await pg.goto('file://' + f); await pg.wait_for_timeout(600)
            await pg.screenshot(path=f'{OUT}/papaya-vivienne-omm-forward-3-story.jpg', type='jpeg', quality=95); os.remove(f); await b.close()
        print('wrote story 3'); return
    from playwright.async_api import async_playwright
    os.makedirs(OUT, exist_ok=True)
    names = ['papaya-vivienne-omm-forward-1-made-for-each-other', 'papaya-vivienne-omm-forward-2-favorite-faces',
             'papaya-vivienne-omm-forward-3-all-matches']
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=int(os.environ.get('DSF', '1')))
        for n, html in zip(names, [slide1(), slide2(), slide3()]):
            f = f'{OUT}/.{n}.html'
            open(f, 'w').write(html)
            await pg.goto('file://' + f); await pg.wait_for_timeout(600)
            bad = await pg.evaluate("""()=>{const o=[];for(const el of document.querySelectorAll('#pg div,#pg img')){
              if(el.closest('[style*="z-index"]')&&el.style.transform)continue;
              const r=el.getBoundingClientRect(); if(!r.width||el.innerText===undefined)continue;
              if(el.children.length===0&&el.innerText.trim()&&(r.top<112||r.bottom>1232))o.push(el.innerText.trim()+' '+Math.round(r.top)+'-'+Math.round(r.bottom));
              if(el.tagName==='IMG'&&!el.naturalWidth)o.push('BROKEN '+el.src);}return o}""")
            if bad: print('OVERFLOW', n, bad)
            await pg.screenshot(path=f'{OUT}/{n}.jpg', type='jpeg', quality=93)
            os.remove(f)
            print('wrote', f'{OUT}/{n}.jpg')
        await b.close()

asyncio.run(main())
