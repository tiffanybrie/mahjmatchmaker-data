"""Find Your Mat-ch TUTORIAL images v2 (Tiffany Oct 21 3:56pm: "not idiot-proof enough"): one step per block, big real
v70 screens, callout pills (Caprasimo, brand colours) with pink arrows pointing at the real UI. Captions stay live text.

  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 scripts/fym_promo/render2.py [/dev/shm/fymh/v2]
Input: capture2.py full-page @3x shots. Output:
  assets/site/fym-tutorial/tut1..5.webp   page (1000 wide)
  site/email/assets/fym/tut1..5.jpg       email (560 wide, light)
  site/email/assets/fym/hl-tut1..5.png    email step-title images
  scripts/fym_promo/tutorial.json         titles, captions, alt text (one source for page + email)"""
import asyncio, os, sys, json
from PIL import Image

R = '/home/claude/mahjmatchmaker-data'
SRC = sys.argv[1] if len(sys.argv) > 1 else '/dev/shm/fymh/v2'
TMP = '/dev/shm/fymh/r2'
PG = f'{R}/assets/site/fym-tutorial'
EM = f'{R}/site/email/assets/fym'
NAVY, ROSE, HEART, CREAM = '#054689', '#c8325f', '#f56c8c', '#faf3ea'
FONT = f"@font-face{{font-family:Cap;src:url('file://{R}/assets/fonts/Caprasimo.ttf')}}"

# (screen, crop y0..y1 in page CSS px, labels: (text, colour, band, target x, target y))
STEPS = [
    dict(title='Pick your door', screen='doors', crop=(0, 360),
         caption='Start with the tiles you own, or start with the mat you already love.',
         alt='The Find Your Mat-ch start screen. Arrows point to the two doors: I have tiles, and I have a mat.',
         labels=[('Start with your tiles', NAVY, 'bottom', 104, 346), ('Or start with your mat', ROSE, 'bottom', 286, 346)]),
    dict(title='Here&rsquo;s what these buttons do', screen='swipe', crop=(312, 1110),
         caption='Tap &hearts; to add a mat to your shortlist and &#10005; to skip it. My picks show first; tap the pink button to see every mat. Tap a color dot to shop by color, and tap it again to clear it.',
         alt='Swiping mats for Papaya Spritz tiles, with the Heiress mat on screen. Arrows point to the Tiffany’s picks button (turn my picks on or off), the color dots (shop by color), the X button (not for me) and the heart button (love it, add to my shortlist).',
         labels=[('Turn my picks on or off', ROSE, 'top', 123, 341), ('Shop by color', NAVY, 'top', 362, 341),
                 ('Not for me', NAVY, 'bottom', 156, 1071), ('Love it! Add to my shortlist', ROSE, 'bottom', 230, 1071)],
         email=[((312, 372), [('Turn my picks on or off', ROSE, 'top', 123, 341), ('Shop by color', NAVY, 'top', 362, 341)]),
                ((1034, 1110), [('Not for me', NAVY, 'bottom', 156, 1071), ('Love it! Add to my shortlist', ROSE, 'bottom', 230, 1071)])]),
    dict(title='Your shortlist', screen='shortlist', crop=(960, 1200),
         caption='Every mat you &hearts; collects at the bottom, so you can compare. When you&rsquo;re ready, tap Mock your&nbsp;match.',
         alt='The shortlist bar at the bottom of the swipe, holding two loved mats. Arrows point to the shortlist and to the Mock your match button.',
         labels=[('Your shortlist: every mat you ♥', ROSE, 'bottom', 135, 1148), ('Mock up your match', NAVY, 'bottom', 322, 1148)]),
    dict(title='Mock up your match', screen='racks', crop=(1320, 2120),
         caption='Swipe racks the same way, with my rack picks first. When you love one, tap Make it&nbsp;official.',
         alt='The mock-up step: Papaya Spritz tiles on the Heiress mat with Tiffany’s rack match, Middle & Main Scalloped Beechwood. Arrows point to the rack and to the X and heart buttons for swiping racks.',
         labels=[('Your tiles + mat, together', NAVY, 'top', 110, 1400), ('Swipe racks: ✕ or ♥', ROSE, 'bottom', 195, 2085)],
         email_alt='The racks step: Tiffany\u2019s rack match, Middle & Main Scalloped Beechwood, with arrows to the rack and to the X and heart buttons for swiping racks.',
         email=[((1792, 2120), [('My rack pick', NAVY, 'top', 230, 1860), ('Swipe racks: ✕ or ♥', ROSE, 'bottom', 195, 2085)])]),
    dict(title='Save and share', screen='card', crop=(2362, 3020),
         caption='Pick your view, then save your match card or send it to your mahj group. Every piece is linked, with code&nbsp;MAHJMATCH.',
         alt='The finished match card for Papaya Spritz on Heiress with Beechwood racks. Arrows point to the view buttons and to Save or share my match card.',
         labels=[('Pick your view', NAVY, 'top', 195, 2388), ('Save it or share it', ROSE, 'bottom', 195, 2986)],
         email=[((2362, 2800), [('Pick your view', NAVY, 'top', 195, 2388)]), ((2940, 3012), [('Save it or share it', ROSE, 'bottom', 195, 2986)])]),
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

        for i, s in enumerate(STEPS, 1):
            im = await part(str(i), s['screen'], s['crop'], s['labels'])
            im.save(f'{PG}/tut{i}.webp', quality=80, method=6)
            if s.get('email'):
                ps = [await part(f'{i}e{j}', s['screen'], c, l) for j, (c, l) in enumerate(s['email'])]
                em = Image.new('RGB', (W, sum(x.height for x in ps)), CREAM); y = 0
                for x in ps:
                    em.paste(x, (0, y)); y += x.height
            else:
                em = im
            ew = 480
            e = em.resize((ew, round(em.height * ew / em.width)), Image.LANCZOS)
            e.save(f'{EM}/tut{i}.jpg', quality=56, optimize=True, progressive=True)
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
    json.dump(out, open(f'{R}/scripts/fym_promo/tutorial.json', 'w'), indent=1, ensure_ascii=False)
    for o in out:
        print(o['n'], o['page'], o['email'], o['hl'])
    print('email KB', round(sum(o['email'][2] + o['hl'][2] for o in out) / 1024))


asyncio.run(go())
