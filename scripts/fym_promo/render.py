"""Find Your Mat-ch promo visuals (Tiffany, Oct 21 3:13pm + 3:14pm): anything that unveils or promotes the tool SHOWS
THE TOOL. Real app screens from capture.py, in a true-proportion iPhone frame (as in papaya_heiress_story_v2.py frame 3),
plus brand headline images in Caprasimo for the emails.

  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 scripts/fym_promo/render.py [/dev/shm/fymh]

Writes
  site/email/assets/fym/hero.jpg                 launch email hero: swipe phone (Papaya Spritz + Heiress, her #1) + doors phone
  site/email/assets/fym/step1..6.jpg             launch email tutorial phones
  site/email/assets/fym/hl-*.png                 headline / step title / section head images (2x, Caprasimo, brand colours)
  assets/site/fym-page-v2/hero-phones.webp       FYM page hero (transparent)
  assets/site/fym-page-v2/step1..6.webp          FYM page how-it-works phones (transparent)
Screens: undo hidden, X and heart only, no %."""
import asyncio, os, sys, json
from PIL import Image

R = '/home/claude/mahjmatchmaker-data'
SRC = sys.argv[1] if len(sys.argv) > 1 else '/dev/shm/fymh'
EM = f'{R}/site/email/assets/fym'
PG = f'{R}/assets/site/fym-page-v2'
TMP = '/dev/shm/fymh/render'
NAVY, DEEP, PINK, ROSE, HEART, PAPER = '#054689', '#062a55', '#d6336c', '#c8325f', '#f56c8c', '#fffdfa'

# step screen, page/email title, alt text
STEPS = [
    ('doors.jpg', 'Pick your door', 'The Find Your Mat-ch start screen with two doors: I have tiles, or I have a mat, plus Shop by color'),
    ('swipe.jpg', 'Swipe ✕ or ♥', 'Swiping mats for Papaya Spritz tiles: the Heiress mat by Britt Mills, marked Tiffany’s match, with the X and heart buttons'),
    ('picks-off.jpg', 'My picks, on or off', 'The Tiffany’s picks button switched to Showing: all mats, so every mat in the catalog is in the swipe'),
    ('color.jpg', 'Shop by color', 'The color dots above the swipe, with Pink selected to narrow the mats to pink'),
    ('racks.jpg', 'Choose your racks', 'The racks step: Papaya Spritz tiles on the Heiress mat with Tiffany’s rack match, Middle & Main Scalloped Beechwood'),
    ('card.jpg', 'Save your match card', 'The finished match card: Papaya Spritz tiles on the Heiress mat with Beechwood racks, ready to save or share'),
]
HEADS = {  # file stem: (text html, kind)
    'hl-launch-h1': ('It&rsquo;s here!', 'h1'),
    'hl-launch-how': ('Here&rsquo;s how it works', 'h2'),
    'hl-welcome-h1': ('Hi, I&rsquo;m Tiffany!', 'h1'),
    'hl-welcome-start': ('Three fun places to start', 'h2'),
    'hl-welcome-reads': ('A few of my favorite reads', 'h2'),
    'hl-request-h1': ('Thank you for your request!', 'h1'),
    'hl-exists-h1': ('Great taste!', 'h1'),
    'hl-live-h1': ('You asked, I matched!', 'h1'),
}
FONT = f"@font-face{{font-family:Cap;src:url('file://{R}/assets/fonts/Caprasimo.ttf')}}"


def phone(src, ph):
    """True-proportion iPhone 14/15 (71.5 x 147 mm body, 19.5:9 screen) around a 390x844 app screen."""
    pw = round(ph * 71.5 / 147); bez = round(ph * 22 / 940); sw = pw - 2 * bez; sh = ph - 2 * bez; rad = round(pw * 0.17)
    return f"""<div class=ph style="box-sizing:border-box;position:relative;width:{pw}px;height:{ph}px;border-radius:{rad}px;background:linear-gradient(145deg,#2b2f38,#0d0f14 45%,#2a2d35);padding:{bez}px;box-shadow:0 {round(ph*.03)}px {round(ph*.07)}px rgba(6,42,85,.26),inset 0 0 0 2px #4a4f5a,inset 0 0 0 {max(3,round(ph*.0064))}px #111">
 <div style="position:absolute;left:-4px;top:{round(ph*.2)}px;width:4px;height:{round(ph*.07)}px;border-radius:2px;background:#22252c"></div>
 <div style="position:absolute;left:-4px;top:{round(ph*.29)}px;width:4px;height:{round(ph*.07)}px;border-radius:2px;background:#22252c"></div>
 <div style="position:absolute;right:-4px;top:{round(ph*.25)}px;width:4px;height:{round(ph*.11)}px;border-radius:2px;background:#22252c"></div>
 <div style="width:{sw}px;height:{sh}px;border-radius:{rad-bez+4}px;overflow:hidden;background:#fff;position:relative">
  <div style="height:{round(sw*47/390)}px;display:flex;align-items:center;justify-content:space-between;padding:0 {round(sw*.09)}px 0 {round(sw*.1)}px;font:600 {round(sw*.042)}px -apple-system,Helvetica,Arial,sans-serif;color:#000">
   <span>9:41</span><span style="display:flex;gap:{round(sw*.012)}px;align-items:center"><svg width="{round(sw*.045)}" height="{round(sw*.03)}" viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx=".7"/><rect x="5" y="5.5" width="3" height="6.5" rx=".7"/><rect x="10" y="3" width="3" height="9" rx=".7"/><rect x="15" y="0" width="3" height="12" rx=".7"/></svg><svg width="{round(sw*.065)}" height="{round(sw*.03)}" viewBox="0 0 27 12"><rect x=".5" y=".5" width="22" height="11" rx="3" fill="none" stroke="#000" opacity=".4"/><rect x="2" y="2" width="19" height="8" rx="1.8"/><rect x="24" y="4" width="2" height="4" rx="1" opacity=".4"/></svg></span></div>
  <img src="file://{SRC}/{src}" style="width:100%;height:{sh - round(sw*81/390)}px;object-fit:contain;object-position:top center;display:block">
  <div style="position:absolute;left:50%;bottom:{round(sw*8/390)}px;width:{round(sw*.35)}px;height:{max(4, round(sw*5/390))}px;margin-left:-{round(sw*.175)}px;border-radius:99px;background:#000"></div>
  <div style="position:absolute;left:50%;top:{round(ph*11/940)}px;width:{round(sw*.31)}px;height:{round(sw*.09)}px;margin-left:-{round(sw*.155)}px;border-radius:99px;background:#000"></div>
 </div></div>"""


def page(body, bg='transparent', w=1200, h=1200):
    return f"""<!doctype html><meta charset=utf-8><style>{FONT}html,body{{margin:0;background:{bg}}}#c{{position:relative;width:{w}px;height:{h}px}}</style><div id=c>{body}</div>"""


def head(text, kind):
    if kind == 'h1':
        st = f'font:400 80px/1.08 Cap;color:{PINK}'
    else:
        st = f'font:400 52px/1.1 Cap;color:{NAVY}'
    return f"""<!doctype html><meta charset=utf-8><style>{FONT}html,body{{margin:0;background:transparent}}#c{{display:inline-block;padding:6px 4px 10px;max-width:1060px;text-align:center;text-wrap:balance;{st}}}</style><div id=c>{text}</div>"""


def step_head(n, text):
    return f"""<!doctype html><meta charset=utf-8><style>{FONT}html,body{{margin:0;background:transparent}}#c{{display:inline-flex;align-items:center;gap:20px;padding:6px 4px 10px;white-space:nowrap}}
#c b{{width:68px;height:68px;border-radius:50%;background:{ROSE};color:#fff;font:400 40px/68px Cap;text-align:center;flex:none}}#c span{{font:400 52px/1.1 Cap;color:{NAVY}}}#c i{{font-style:normal;font-family:Arial,sans-serif}}#c .x{{color:#8d97ad}}#c .h{{color:{HEART}}}</style>
<div id=c><b>{n}</b><span>{text}</span></div>"""


def q8(path):
    im = Image.open(path).convert('RGBA')
    im.quantize(colors=64, method=Image.FASTOCTREE).save(path, optimize=True)


async def go():
    from playwright.async_api import async_playwright
    for d in (EM, PG, TMP):
        os.makedirs(d, exist_ok=True)
    alts = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()

        async def shot(html, out, sel='#c', omit=True, scale=1):
            pg = await b.new_page(viewport={'width': 1400, 'height': 1600}, device_scale_factor=scale)
            f = f'{TMP}/t.html'; open(f, 'w').write(html)
            await pg.goto('file://' + f, wait_until='load'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.locator(sel).screenshot(path=out, omit_background=omit)
            await pg.close()

        # 0. pre-launch homepage (Tiffany 3:58pm): ONE phone, the v70 START screen only (Find Your Mat-ch), nothing else teased
        await shot(page(f'<div style="position:absolute;left:40px;top:30px">{phone("doors.jpg", 1040)}</div>', w=590, h=1140), f'{TMP}/start.png')
        im = Image.open(f'{TMP}/start.png'); os.makedirs(f'{R}/assets/site/home-prelaunch', exist_ok=True)
        im.resize((560, round(im.height * 560 / im.width)), Image.LANCZOS).save(f'{R}/assets/site/home-prelaunch/start-phone.webp', quality=84, method=6)
        # 1. hero: big swipe phone + smaller doors phone, overlapping (email = paper bg jpg, page = transparent)
        hero = f"""<div style="position:absolute;left:150px;top:150px;transform:rotate(-4deg)">{phone('doors.jpg', 760)}</div>
<div style="position:absolute;left:560px;top:30px;z-index:2">{phone('swipe.jpg', 1000)}</div>"""
        await shot(page(hero, w=1120, h=1080), f'{TMP}/hero.png')
        im = Image.open(f'{TMP}/hero.png')
        # email hero dropped (QA Oct 21: email weight); page keeps the transparent hero
        if 0: bg.convert('RGB').resize((960, round(im.height * 960 / im.width)), Image.LANCZOS).save(f'{EM}/hero.jpg', quality=76, optimize=True, progressive=True)
        im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS).save(f'{PG}/hero-phones.webp', quality=82, method=6)

        # 2. step phones
        for i, (src, title, alt) in enumerate(STEPS, 1):
            await shot(page(f'<div style="position:absolute;left:40px;top:30px">{phone(src, 900)}</div>', w=518, h=1010), f'{TMP}/s{i}.png')
            im = Image.open(f'{TMP}/s{i}.png')
            bg = Image.new('RGBA', im.size, PAPER); bg.alpha_composite(im)
            if 0: bg.convert('RGB').resize((240, round(im.height * 240 / im.width)), Image.LANCZOS).save(f'{EM}/step{i}.jpg', quality=62, optimize=True, progressive=True)  # QA: ~15-20 KB each
            im.resize((480, round(im.height * 480 / im.width)), Image.LANCZOS).save(f'{PG}/step{i}.webp', quality=80, method=6)
            th = title.replace('✕', '<i class=x>✕</i>').replace('♥', '<i class=h>♥</i>')
            # email step titles now come from render2.py (hl-tut*)

        # 3. headline images
        for stem, (text, kind) in HEADS.items():
            await shot(head(text, kind), f'{EM}/{stem}.png'); q8(f'{EM}/{stem}.png')
            alts[stem] = text.replace('&rsquo;', '’')
        await b.close()
    alts['hero'] = ('Find Your Mat-ch on a phone: Papaya Spritz tiles swiping on the Heiress mat by Britt Mills with the X and heart '
                    'buttons, next to the start screen where you pick I have tiles or I have a mat')
    sizes = {f: [*Image.open(f'{EM}/{f}').size, os.path.getsize(f'{EM}/{f}')] for f in sorted(os.listdir(EM)) if not f.endswith('.json')}
    json.dump({'alt': alts, 'sizes': sizes}, open(f'{EM}/manifest.json', 'w'), indent=1, ensure_ascii=False)
    tot = sum(v[2] for v in sizes.values())
    print('email assets', len(sizes), 'files', round(tot / 1024), 'KB')
    for f, v in sizes.items():
        print(f, v)
    for f in sorted(os.listdir(PG)):
        print('page', f, Image.open(f'{PG}/{f}').size, os.path.getsize(f'{PG}/{f}'))


asyncio.run(go())
