"""Find Your Mat-ch TUTORIAL images v2 (Tiffany Oct 21 3:56pm: "not idiot-proof enough"): one step per block, big real
v72 screens, callout pills (Caprasimo, brand colours) with pink arrows pointing at the real UI. Captions stay live text.

  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 scripts/fym_promo/render2.py [/dev/shm/fymh/v2]
Input: capture2.py full-page @3x shots. Output:
  assets/site/fym-tutorial/tut1..6.webp   page (1000 wide)
  site/email/assets/fym/tut1..6.jpg       email (560 wide, light)
  site/email/assets/fym/hl-tut1..6.png    email step-title images
  scripts/fym_promo/tutorial.json         titles, captions, alt text (one source for page + email)"""
import asyncio, os, sys, json
from PIL import Image

R = '/home/claude/mahjmatchmaker-data'
SRC = sys.argv[1] if len(sys.argv) > 1 else '/dev/shm/fymh/v3'
TMP = '/dev/shm/fymh/r2'
PG = f'{R}/assets/site/fym-tutorial'
EM = f'{R}/site/email/assets/fym'
NAVY, ROSE, HEART, CREAM = '#054689', '#c8325f', '#f56c8c', '#faf3ea'
FONT = f"@font-face{{font-family:Cap;src:url('file://{R}/assets/fonts/Caprasimo.ttf')}}"

# v72 (Oct 21 night): 6 steps from capture2.py (live v72 flow). Each step = one or more PARTS stacked into one image:
# (crop y0..y1 in page CSS px, labels: (text, colour, band, target x, target y)). Top-band arrows land on the control's top edge,
# bottom-band arrows on its bottom edge (targets read from /dev/shm/fymh/v3/rects.json; check each image by eye).
STEPS = [
    dict(title='Pick your door', screen='doors',
         caption='Start with the tiles you own, or start with the mat you already&nbsp;love.',
         alt='The Find Your Mat-ch start screen. Arrows point to the two doors: I have tiles, and I have a mat.',
         parts=[((0, 360), [('Start with your tiles', NAVY, 'bottom', 104, 345), ('Or start with your mat', ROSE, 'bottom', 286, 345)])]),
    dict(title='Here&rsquo;s what these buttons do', screen='swipe',
         caption='Tap &hearts; to love a mat and &#10005; when it&rsquo;s not the one. Swiped too fast? &larr;&nbsp;Back brings it back. My picks show first; tap Tiffany&rsquo;s picks to see every mat. Tap a color or Holiday to narrow the mats, and tap it again to clear&nbsp;it.',
         alt='Swiping mats for Papaya Spritz tiles, with the Haven mat by Britt Mills on screen. Arrows point to the Tiffany’s picks button (my picks on or off), the Holiday and color buttons, the Back button (brings the last mat back), the X button (not the one) and the heart button (love it).',
         parts=[((365, 425), [('My picks on or off', ROSE, 'top', 90, 380), ('Holiday + colors', NAVY, 'top', 332, 381)]),
                ((515, 1174), [('&larr; Back brings one back', NAVY, 'top', 335, 596),
                               ('&#10005; Not the one', NAVY, 'bottom', 156, 1150), ('&hearts; Love it', ROSE, 'bottom', 230, 1152)])],
         email=[((365, 425), [('My picks on or off', ROSE, 'top', 90, 380), ('Holiday + colors', NAVY, 'top', 332, 381)]),
                ((562, 618), [('&larr; Back brings one back', NAVY, 'top', 335, 596)]),
                ((1095, 1174), [('&#10005; Not the one', NAVY, 'bottom', 156, 1150), ('&hearts; Love it', ROSE, 'bottom', 230, 1152)])]),
    dict(title='Your shortlist', screen='swipe',
         caption='Every mat you &hearts; waits at the bottom, so you can compare. When you&rsquo;re ready, tap Next: add&nbsp;racks.',
         alt='The shortlist bar under the swipe buttons, holding two loved mats. Arrows point to the shortlist and to the Next: add racks button.',
         parts=[((1095, 1258), [('Your shortlist', ROSE, 'bottom', 109, 1235), ('Next: add racks', NAVY, 'bottom', 322, 1236)])]),
    dict(title='Pick 2 racks', screen='racks',
         caption='Tap the suitor you love most, then swipe racks the same way, with my rack picks first. Your first two &hearts; fill your rack slots; tap &times; to swap one. Then tap Make it&nbsp;official.',
         alt='The racks step for Papaya Spritz on Heiress. Arrows point to the heart button for swiping racks, to Your racks holding Beechwood and Coral (tap × to swap), and to the Make it official button.',
         parts=[((2350, 2448), [('Swipe racks the same way', ROSE, 'bottom', 230, 2420)]),
                ((1830, 2050), [('Your 2 racks: tap &times; to swap', NAVY, 'top', 115, 1893), ('Make it official &hearts;', ROSE, 'bottom', 195, 2035)])]),
    dict(title='Make it official', screen='card',
         caption='Pick your view and your size: Story, Post or Pin. Then save your match card or share it with your mahj&nbsp;group.',
         alt='The finished match card: Papaya Spritz tiles on the Heiress mat with Beechwood and Coral racks. Arrows point to the view buttons (Love triangle or Mood board), the size buttons (Story, Post or Pin) and Save / Share my match card.',
         parts=[((2570, 2680), [('Pick your view', NAVY, 'top', 104, 2600), ('Story, Post or Pin size', ROSE, 'bottom', 195, 2671)]),
                ((2684, 3205), [('Save or share it', ROSE, 'bottom', 195, 3186)])]),
    dict(title='Use code MAHJMATCH to save', screen='card',
         caption='Every piece on your card is linked, with each partner brand&rsquo;s code one tap&nbsp;away.',
         alt='The bottom of the match card, with the line Use code MAHJMATCH to save, and the Take them home list. Arrows point to the code line and to a Shop button.',
         parts=[((3070, 3318), [('Use code MAHJMATCH to save', NAVY, 'top', 195, 3121), ('Shop every piece', ROSE, 'bottom', 345, 3282)])]),
]

W = 1000


def html(tag, crop, labels):
    y0, y1 = crop
    k = W / 390
    top = [l for l in labels if l[2] == 'top']
    bot = [l for l in labels if l[2] == 'bottom']

    def band(ls, cls):
        if not ls:
            return f'<div class="band {cls} empty"></div>'
        ls = sorted(ls, key=lambda l: l[3])
        return f'<div class="band {cls}">' + ''.join(
            f'<b class=pill data-tx="{l[3] * k:.1f}" data-ty="{(l[4] - y0) * k:.1f}" style="background:{l[1]}">{l[0]}</b>' for l in ls) + '</div>'
    return f"""<!doctype html><meta charset=utf-8><style>{FONT}
html,body{{margin:0;background:{CREAM}}}#c{{position:relative;width:{W}px;background:{CREAM};padding:0 0 4px}}
.band{{display:flex;justify-content:space-around;align-items:center;gap:24px;padding:30px 26px}}.band.empty{{padding:14px}}
.pill{{font:400 46px/1.08 Cap;color:#fff;padding:18px 30px 22px;border-radius:30px;max-width:470px;text-align:center;box-shadow:0 8px 20px rgba(6,42,85,.18);position:relative;z-index:3;text-wrap:balance}}
#scr{{position:relative;margin:0 22px;border-radius:30px;overflow:hidden;box-shadow:0 14px 34px rgba(6,42,85,.16);border:5px solid #fff}}
#scr img{{display:block;width:100%}}
svg{{position:absolute;inset:0;z-index:2;pointer-events:none}}</style>
<div id=c>{band(top, 'top')}<div id=scr><img src="file://{TMP}/crop{tag}.png"></div>{band(bot, 'bot')}<svg id=sv></svg></div>
<script>
const c=document.getElementById('c'),scr=document.getElementById('scr'),sv=document.getElementById('sv');
function go(){{const cr=c.getBoundingClientRect(),sr=scr.getBoundingClientRect(),sc=(sr.width)/{W};
sv.setAttribute('width',cr.width);sv.setAttribute('height',cr.height);sv.setAttribute('viewBox','0 0 '+cr.width+' '+cr.height);
let h='<defs><marker id=a markerWidth=5 markerHeight=5 refX=3.2 refY=2.5 orient=auto markerUnits=strokeWidth><path d="M0,0 L5,2.5 L0,5 z" fill="{HEART}"/></marker></defs>';
for(const p of document.querySelectorAll('.pill')){{const r=p.getBoundingClientRect();const top=p.parentElement.classList.contains('top');
 const tx=sr.left-cr.left+(+p.dataset.tx)*sc, ty=sr.top-cr.top+(+p.dataset.ty)*sc;
 const sx=r.left-cr.left+r.width/2, sy=top?r.bottom-cr.top:r.top-cr.top;
 const ex=tx, ey=top?ty-18:ty+24; const mx=(sx+ex)/2, my=(sy+ey)/2;
 const d='M'+sx+','+sy+' Q'+sx+','+my+' '+ex+','+ey;
 h+='<path d="'+d+'" stroke="#fff" stroke-width="16" fill="none" stroke-linecap="round"></path>';
 h+='<path d="'+d+'" stroke="{HEART}" stroke-width="8" fill="none" stroke-linecap="round" marker-end="url(#a)"></path>';
 h+='<circle cx="'+tx+'" cy="'+ty+'" r=10 fill="{HEART}" stroke="#fff" stroke-width="4" opacity="0"></circle>';}}
sv.innerHTML=h;}}
window.go=go;document.fonts.ready.then(go);</script>"""


def step_head(n, text):
    return f"""<!doctype html><meta charset=utf-8><style>{FONT}html,body{{margin:0;background:transparent}}#c{{display:inline-flex;align-items:center;gap:20px;padding:6px 4px 10px;max-width:1060px}}
#c b{{width:68px;height:68px;border-radius:50%;background:{ROSE};color:#fff;font:400 40px/68px Cap;text-align:center;flex:none}}#c span{{font:400 52px/1.1 Cap;color:{NAVY}}}</style>
<div id=c><b>{n}</b><span>{text}</span></div>"""


async def go():
    from playwright.async_api import async_playwright
    for d in (TMP, PG, EM):
        os.makedirs(d, exist_ok=True)
    out = []
    async with async_playwright() as p:
        b = await p.chromium.launch()

        async def part(tag, screen, crop, labels):
            y0, y1 = crop
            Image.open(f"{SRC}/{screen}.png").crop((0, y0 * 3, 1170, y1 * 3)).save(f'{TMP}/crop{tag}.png')
            pg = await b.new_page(viewport={'width': W, 'height': 1200}, device_scale_factor=1)
            f = f'{TMP}/t{tag}.html'; open(f, 'w').write(html(tag, crop, labels))
            await pg.goto('file://' + f, wait_until='load'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
            await pg.evaluate('go()'); await pg.wait_for_timeout(150)
            await pg.locator('#c').screenshot(path=f'{TMP}/tut{tag}.png'); await pg.close()
            return Image.open(f'{TMP}/tut{tag}.png').convert('RGB')

        async def stack(i, s, parts, sfx):
            ps = [await part(f'{i}{sfx}{j}', s['screen'], c, l) for j, (c, l) in enumerate(parts)]
            im = Image.new('RGB', (W, sum(x.height for x in ps)), CREAM); y = 0
            for x in ps:
                im.paste(x, (0, y)); y += x.height
            return im

        for i, s in enumerate(STEPS, 1):
            im = await stack(i, s, s['parts'], 'p')
            im.save(f'{PG}/tut{i}.webp', quality=80, method=6)
            em = await stack(i, s, s['email'], 'e') if s.get('email') else im
            ew = 560
            e = em.resize((ew, round(em.height * ew / em.width)), Image.LANCZOS)
            e.save(f'{EM}/tut{i}.jpg', quality=52, optimize=True, progressive=True)
            pg = await b.new_page(viewport={'width': 1200, 'height': 400})
            f = f'{TMP}/h{i}.html'; open(f, 'w').write(step_head(i, s['title']))
            await pg.goto('file://' + f, wait_until='load'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(200)
            await pg.locator('#c').screenshot(path=f'{EM}/hl-tut{i}.png', omit_background=True); await pg.close()
            h = Image.open(f'{EM}/hl-tut{i}.png').convert('RGBA'); h.quantize(colors=64, method=Image.FASTOCTREE).save(f'{EM}/hl-tut{i}.png', optimize=True)
            out.append({'n': i, 'title': s['title'], 'caption': s['caption'], 'alt': s['alt'], **({'email_alt': s['email_alt']} if s.get('email_alt') else {}),
                        'page': [im.width, im.height, os.path.getsize(f'{PG}/tut{i}.webp')],
                        'email': [e.width, e.height, os.path.getsize(f'{EM}/tut{i}.jpg')],
                        'hl': [*Image.open(f'{EM}/hl-tut{i}.png').size, os.path.getsize(f'{EM}/hl-tut{i}.png')]})
        await b.close()
    # Squarespace email editor = one image section per step: title baked in above the screen (Oct 21)
    PAPER = (255, 253, 250)
    for o in out:
        i = o['n']; W2 = 560
        parts = []
        if i == 1:
            hw = Image.open(f'{EM}/hl-launch-how.png').convert('RGBA'); k = min(0.85, (W2 - 40) / hw.width); parts.append(hw.resize((round(hw.width * k), round(hw.height * k)), Image.LANCZOS))
        h = Image.open(f'{EM}/hl-tut{i}.png').convert('RGBA')
        sc = min(0.8, (W2 - 40) / h.width)
        parts.append(h.resize((round(h.width * sc), round(h.height * sc)), Image.LANCZOS))
        sh = Image.open(f'{EM}/tut{i}.jpg').convert('RGBA')
        H = sum(p.height for p in parts) + 18 * len(parts) + 10 + sh.height
        c = Image.new('RGBA', (W2, H), PAPER + (255,)); y = 12
        for p in parts:
            c.alpha_composite(p, ((W2 - p.width) // 2, y)); y += p.height + 14
        c.alpha_composite(sh, ((W2 - sh.width) // 2, y))
        c.convert('RGB').save(f'{EM}/step-sq{i}.jpg', quality=56, optimize=True, progressive=True)
        o['sq'] = [c.width, c.height, os.path.getsize(f'{EM}/step-sq{i}.jpg')]
    json.dump(out, open(f'{R}/scripts/fym_promo/tutorial.json', 'w'), indent=1, ensure_ascii=False)
    for o in out:
        print(o['n'], o['page'], o['email'], o['hl'])
    print('email KB', round(sum(o['email'][2] + o['hl'][2] for o in out) / 1024))


asyncio.run(go())
