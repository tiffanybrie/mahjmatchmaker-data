"""Week of Oct 22-27 social pieces for Planoly (built Oct 21 for the Planoly-only review, content-strategy-oct-dec.md).
Same look as the approved countdown stories (scripts/reel/countdown-oct20/cd.html): pink dotted paper, navy pill,
Shrikhand headline, Playfair italic line, no-tag wordmark. Our own assets only (album covers, album tile photos,
gallery mat photo, brand marks); no brand product photos on their own, no app UI.
Stories 1080x1920 (safe: top 269px, bottom 384px). Feed 1080x1350 (content inside y 120-1230). Pins 1000x1500.
Run: python3 scripts/social/week_oct22/build.py  -> assets/social/week-oct22/*.jpg"""
import os, sys
from playwright.sync_api import sync_playwright
from PIL import Image

R = '/home/claude/mahjmatchmaker-data'
O = R + '/assets/social/week-oct22/'
TMP = '/dev/shm/wk22/'
os.makedirs(O, exist_ok=True); os.makedirs(TMP, exist_ok=True)
u = lambda p: f'file://{R}/{p}'
FA = f'file://{R}/assets/fonts'; FT = f'file://{R}/scripts/social/tileprofile/fonts'

HEART = ('<svg viewBox="0 0 230 210" style="width:{w}px;vertical-align:middle"><path d="M115 200S12 140 12 72C12 36 38 12 70 12c22 0 37 12 45 '
         '28 8-16 23-28 45-28 32 0 58 24 58 60 0 68-103 128-103 128z" fill="{c}" stroke="#fff" stroke-width="{s}"/></svg>')
heart = lambda w=44, c='#d6608c', s=0: HEART.format(w=w, c=c, s=s)
TM = '<sup style="font-size:.42em;vertical-align:super;letter-spacing:0;font-style:normal">&trade;</sup>'
FYM = f'Find <i>Your</i> Mat-ch{TM}'
FYM2 = f'Find <i>Your</i><br>Mat-ch{TM}'

CSS = f"""
@font-face{{font-family:Shrikhand;src:url({FA}/shrikhand-latin-400-normal.woff2)}}
@font-face{{font-family:Bitter;font-weight:700;src:url({FA}/bitter-latin-700-normal.woff2)}}
@font-face{{font-family:Bitter;font-weight:400;src:url({FA}/bitter-latin-400-normal.woff2)}}
@font-face{{font-family:Playfair;font-style:italic;src:url({FA}/playfair-display-latin-400-italic.woff2)}}
@font-face{{font-family:Capra;src:url({FT}/Caprasimo.ttf)}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:linear-gradient(170deg,#fff7f4,#fde3ec);font-family:Bitter,Georgia,serif;color:#064587;position:relative;overflow:hidden}}
.bgdots{{position:absolute;inset:0;background-image:radial-gradient(#f6c9d6 2.2px,transparent 2.6px);background-size:46px 46px;opacity:.55}}
.abs{{position:absolute;left:0;right:0;text-align:center}}
.pill{{display:inline-block;background:#064587;color:#fff;font:700 38px Bitter;letter-spacing:.14em;padding:12px 40px;border-radius:99px}}
.sh{{font-family:Shrikhand;font-weight:400}}
.pink{{color:#d6608c}}
.big{{font:120px/1.02 Shrikhand;color:#d6608c;text-shadow:0 8px 0 #fff}}
.mid{{font:84px/1.05 Shrikhand;color:#064587;text-shadow:0 5px 0 #fff}}
.line{{font:italic 54px/1.2 Playfair;color:#064587}}
.line b{{font-style:normal;font-family:Shrikhand;font-weight:400;color:#d6608c}}
.card{{background:#fff;border-radius:40px;box-shadow:0 18px 50px rgba(6,40,90,.16)}}
.code{{display:inline-flex;align-items:center;gap:18px;background:#d6608c;color:#fff;font:700 44px Bitter;padding:22px 46px;border-radius:99px;box-shadow:0 10px 30px rgba(214,96,140,.35)}}
.code b{{letter-spacing:.06em}}
.chip{{display:inline-block;background:#fde3ec;border:3px solid #f3b4c8;color:#064587;font:700 30px Bitter;padding:9px 20px;border-radius:99px;margin:8px 6px}}
.c{{position:absolute;border-radius:50%;border:13px solid #fff;box-shadow:0 18px 50px rgba(6,40,90,.22);background-size:cover;background-position:center}}
.wm{{position:absolute;left:50%;transform:translateX(-50%)}}
"""

def page(w, h, inner, bg=None):
    style = f'width:{w}px;height:{h}px' + (f';background:{bg}' if bg else '')
    return f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body style='{style}'><div class=bgdots></div>{inner}</body></html>"

CODE = f"<span class=code>Use code <b>MAHJMATCH</b> to save {heart(46, '#fff')}</span>"
WM_STORY = f"<img class=wm src='{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}' style='bottom:440px;width:560px'>"

P = {}

# ---- Oct 22, 12pm CT: Mahj Mood restock tomorrow (plain story, auto) ----
DETAILS = """<div class='abs' style='top:{top}px'><div class='card' style='display:inline-block;width:900px;padding:44px 40px 36px'>
<div style='font:700 30px Bitter;letter-spacing:.2em;color:#d6608c'>MAHJ MOOD</div>
<div class='mid' style='font-size:64px;margin-top:10px'>20&rdquo; Clear Racks</div>
<div style='font:italic 44px Playfair;color:#064587;margin:6px 0 18px'>+ 8 new pushers</div>
<div><span class=chip>Pearl pink</span><span class=chip>Pearl purple</span><span class=chip>Pearl light blue</span><span class=chip>Pearl light green</span></div>
<div><span class=chip>Scalloped Malachite</span><span class=chip>Scalloped Blue Agate</span><span class=chip>Scalloped Tortoise</span><span class=chip>Scalloped White</span></div>
</div></div>"""
P['mahj-mood-restock-tomorrow-story'] = (1080, 1920, f"""
<div class='abs' style='top:285px'><span class=pill>RESTOCK · FRI 10/23 · 10AM CT</span></div>
<div class='abs big' style='top:390px'>Nice racks</div>
<div class='abs mid' style='top:525px'>are back tomorrow.</div>
{DETAILS.format(top=680)}
<div class='abs line' style='top:1290px;left:70px;right:70px'>Malachite owners: there's a<br><b>Scalloped Malachite</b> pusher.</div>
<div class='abs' style='top:1440px'>{CODE}</div>""")

# ---- Oct 23, 10am CT: Mahj Mood restocked today (plain story, auto) ----
P['mahj-mood-restocked-today-story'] = (1080, 1920, f"""
<div class='abs' style='top:285px'><span class=pill>RESTOCKED TODAY</span></div>
<div class='abs big' style='top:390px'>Nice racks</div>
<div class='abs mid' style='top:525px'>are back.</div>
{DETAILS.format(top=680)}
<div class='abs line' style='top:1290px;left:70px;right:70px'>Live now at <b>Mahj Mood.</b><br>Go get your pushers.</div>
<div class='abs' style='top:1440px'>{CODE}</div>""")

# ---- Oct 23, 12pm CT: Papaya Spritz still in stock (plain story, auto) ----
P['papaya-still-in-stock-story'] = (1080, 1920, f"""
<div class='abs' style='top:285px'><span class=pill>OH MY MAHJONG · IN STOCK</span></div>
<div class='abs big' style='top:390px;color:#de7e30'>Still available.</div>
<div class='abs line' style='top:540px'>Papaya Spritz is <b>still in stock.</b></div>
<div style='position:absolute;top:660px;left:0;right:0;height:430px'>
 <div class=c style='left:120px;top:20px;width:400px;height:400px;background-image:url({u('assets/tiles/album/papaya-spritz.jpg')})'></div>
 <div class=c style='right:120px;top:20px;width:400px;height:400px;border-radius:44px;background-image:url({u('assets/mats/gallery/britt-mills--heiress.webp')})'></div>
 <div style='position:absolute;left:50%;top:220px;transform:translate(-50%,-50%)'>{heart(170, '#d6608c', 12)}</div></div>
<div class='abs' style='top:1100px;font:700 34px Bitter;letter-spacing:.14em;color:#064587'>PAPAYA SPRITZ <span class=pink>&hearts;</span> HEIRESS</div>
<div class='abs line' style='top:1170px;left:60px;right:60px'>Swipe all 50 of Papaya's matches<br><b>mahjmatchmaker.com</b></div>
<div class='abs' style='top:1360px'>{CODE}</div>""")

# ---- Oct 24, 12pm CT: Petalée album story (plain story, auto) ----
P['petalee-album-story'] = (1080, 1920, f"""
<div class='abs' style='top:285px'><span class=pill>VIRORA · IN STOCK NOW</span></div>
<div class='abs mid' style='top:380px;font-size:92px'>Petalée's album<br><span class=pink>is ready.</span></div>
<div class='abs' style='top:620px'><img src='{u('assets/covers/albums/00-petalee-mahjong-tiles-cover.jpg')}' style='width:600px;border-radius:36px;border:12px solid #fff;box-shadow:0 18px 50px rgba(6,40,90,.22)'></div>
<div class='abs line' style='top:1390px'>See all of Petalée's matches</div>
<div class='abs' style='top:1460px;font:700 40px Bitter;color:#d6608c;letter-spacing:.06em'>mahjmatchmaker.com</div>""")

# ---- Oct 26, 12pm CT: Miss Classic tease 1 (2 plain story frames, auto) ----
for slug, name, color in (('malachite', 'Malachite', '#1f7a5a'), ('jade', 'Jade', '#2f8f7a')):
    P[f'miss-classic-tease-{slug}-story'] = (1080, 1920, f"""
<div class='abs' style='top:285px'><span class=pill>MISS MAHJONG · WEEK OF NOV 3</span></div>
<div class='abs big' style='top:380px;color:{color};font-size:116px'>{name}</div>
<div class='abs mid' style='top:510px;font-size:76px'>is coming back.</div>
<div class='abs' style='top:640px'><img src='{u(f'assets/covers/albums/uniform-v3/{slug}.jpg')}' style='width:480px;border-radius:36px;border:12px solid #fff;box-shadow:0 18px 50px rgba(6,40,90,.22)'></div>
<div class='abs line' style='top:1300px'><b>Pick your mat now.</b><br>See all of {name}'s matches</div>
<div class='abs' style='top:1450px;font:700 38px Bitter;color:#d6608c;letter-spacing:.06em'>mahjmatchmaker.com</div>""")

# ---- Oct 27 launch carousel (feed, 1080x1350, auto) ----
SWIPE = f"""<div style='position:absolute;left:{{x}}px;top:{{y}}px;width:{{w}}px;transform:rotate({{r}}deg)' class=card>
<div style='padding:18px 18px 26px'><div style='position:relative;width:100%;aspect-ratio:1/1;border-radius:26px;background:url({u('assets/mats/gallery/britt-mills--heiress.webp')}) center/cover'>
<div style='position:absolute;right:-8px;bottom:-34px;width:{{t}}px;height:{{t}}px;border-radius:50%;background:url({u('assets/tiles/album/papaya-spritz.jpg')}) center/cover;box-shadow:0 0 0 9px #fff,0 12px 26px rgba(6,40,90,.25)'></div></div>
<div style='font:700 20px Bitter;letter-spacing:.22em;color:#d6608c;margin:30px 0 0 6px'>BRITT MILLS</div>
<div style='font:52px/1.05 Capra;color:#064587;margin:6px 0 0 6px'>Heiress</div>
<div style='font:italic 26px Playfair;color:#3c4f73;margin:6px 0 0 6px'>for your Papaya Spritz tiles</div></div></div>"""
BTNS = f"""<div style='position:absolute;left:{{x}}px;top:{{y}}px;width:{{w}}px;display:flex;justify-content:space-between'>
<div style='width:130px;height:130px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 30px rgba(6,40,90,.2)'><svg width=54 height=54 viewBox='0 0 24 24'><path d='M5 5L19 19M19 5L5 19' stroke='#064587' stroke-width='3.2' stroke-linecap='round'/></svg></div>
<div style='width:130px;height:130px;border-radius:50%;background:#f2708f;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 30px rgba(6,40,90,.2)'>{heart(70, '#fff')}</div></div>"""
WM_FEED = f"<img class=wm src='{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}' style='top:1120px;width:440px'>"
P['launch-1-live'] = (1080, 1350, f"""
<div class='abs' style='top:130px'><span class=pill style='background:#d6608c'>LIVE NOW</span></div>
<div class='abs' style='top:205px;font:112px/1 Capra;color:#064587'>{FYM2}</div>
<div class='abs line' style='top:445px;font-size:44px'>Pick your tiles. Swipe the mats.<br>Heart the ones you love.</div>
{SWIPE.format(x=330, y=590, w=420, r=-3, t=140)}
{BTNS.format(x=95, y=840, w=890)}
""" + f"<div class='abs' style='top:1185px;font:700 30px Bitter;letter-spacing:.2em;color:#d6608c'>MAHJMATCHMAKER.COM · LINK IN BIO</div>")

DOOR = """<div class=card style='position:absolute;left:{x}px;top:{y}px;width:450px;height:700px;padding:34px 30px;text-align:center'>
<div style='font:700 26px Bitter;letter-spacing:.2em;color:#d6608c'>{k}</div>
<div style='font:60px/1.05 Capra;color:#064587;margin:14px 0 26px'>{h}</div>
<div style='margin:0 auto;width:270px;height:270px;{shape};border:10px solid #fde3ec;background:url({img}) center/cover'></div>
<div style='font:italic 36px/1.25 Playfair;color:#064587;margin-top:28px'>{p}</div></div>"""
P['launch-3-two-doors'] = (1080, 1350, f"""
<div class='abs' style='top:140px;font:96px/1 Capra;color:#064587'>Two ways in.</div>
<div class='abs line' style='top:262px;font-size:44px'>Start wherever your collection starts.</div>
{DOOR.format(x=70, y=380, k='DOOR 1', h='Start with<br>your tiles', shape='border-radius:50%', img=u('assets/tiles/album/papaya-spritz.jpg'), p='Swipe the mats that bring out <b>their best colors.</b>')}
{DOOR.format(x=560, y=380, k='DOOR 2', h='Start with<br>your mat', shape='border-radius:36px', img=u('assets/mats/gallery/britt-mills--heiress.webp'), p='Already own a mat? See the <b>tile sets it matches.</b>')}
{WM_FEED}""")

P['launch-4-code'] = (1080, 1350, f"""
<div class='abs' style='top:170px'>{heart(170, '#d6608c', 12)}</div>
<div class='abs' style='top:380px;font:100px/1.02 Capra;color:#064587'>Found your<br>match?</div>
<div class='abs line' style='top:620px;font-size:50px'>Save at our partner brands.</div>
<div class='abs' style='top:740px'><span class=code style='font-size:52px;padding:30px 60px'>Use code <b>MAHJMATCH</b> to save {heart(54, '#fff')}</span></div>
<div class='abs line' style='top:900px;font-size:44px'>{FYM.replace('<i>', '<i style="font-style:normal">')} · <b>mahjmatchmaker.com</b></div>
{WM_FEED}""")

# ---- Oct 27 launch link story (REMINDER: she adds the link sticker in the empty band) ----
P['launch-link-story'] = (1080, 1920, f"""
<div class='abs' style='top:285px'><span class=pill style='background:#d6608c'>LIVE NOW</span></div>
<div class='abs' style='top:370px;font:118px/1 Capra;color:#064587'>{FYM2}</div>
<div class='abs line' style='top:620px;font-size:46px'>Pick your tiles. Swipe the mats.<br>Heart the ones you love.</div>
{SWIPE.format(x=315, y=770, w=450, r=-3, t=150)}
{BTNS.format(x=80, y=1010, w=920)}
<div class='abs' style='top:1420px;font:700 30px Bitter;letter-spacing:.2em;color:#c8325f;opacity:.55'>&darr; TAP THE LINK &darr;</div>""")

# ---- Pins (1000x1500, auto) ----
P['petalee-album-pin'] = (1000, 1500, f"""
<div class='abs' style='top:70px;font:700 28px Bitter;letter-spacing:.24em;color:#d6608c'>VIRORA MAHJONG</div>
<div class='abs' style='top:120px;font:92px/1.02 Capra;color:#064587'>Petalée<br>Mahjong Tiles</div>
<div class='abs line' style='top:340px;font-size:46px'>Mat &amp; rack matches</div>
<div class='abs' style='top:440px'><img src='{u('assets/covers/albums/00-petalee-mahjong-tiles-cover.jpg')}' style='width:620px;border-radius:34px;border:12px solid #fff;box-shadow:0 18px 50px rgba(6,40,90,.22)'></div>
<div class='abs' style='top:1390px;font:700 28px Bitter;letter-spacing:.2em;color:#064587'>SHOP THE LOOK · MAHJMATCHMAKER.COM</div>""")
P['find-your-match-pin'] = (1000, 1500, f"""
<div class='abs' style='top:80px;font:700 28px Bitter;letter-spacing:.24em;color:#d6608c'>WHAT MAT GOES WITH MY TILES?</div>
<div class='abs' style='top:135px;font:112px/1 Capra;color:#064587'>{FYM2}</div>
<div class='abs line' style='top:375px;font-size:42px'>Pick your mahjong tiles.<br>Swipe the mats. Heart the ones you love.</div>
{SWIPE.format(x=290, y=520, w=420, r=-3, t=140)}
{BTNS.format(x=70, y=760, w=860)}
<div class='abs' style='top:1185px'><span class=code style='font-size:40px'>Use code <b>MAHJMATCH</b> to save {heart(40, '#fff')}</span></div>
<div class='abs' style='top:1390px;font:700 28px Bitter;letter-spacing:.2em;color:#064587'>SHOP THE LOOK · MAHJMATCHMAKER.COM</div>""")

# story wordmark on every plain story except the link story (needs the sticker band)
for k, (w, h, inner) in list(P.items()):
    if h == 1920 and k != 'launch-link-story':
        P[k] = (w, h, inner + WM_STORY.replace('bottom:440px', 'top:1560px').replace('width:560px', 'width:440px'))
    if k == 'launch-link-story':
        P[k] = (w, h, inner + WM_STORY.replace('bottom:440px', 'top:1500px').replace('width:560px', 'width:380px'))
    if h == 1500:
        P[k] = (w, h, inner + f"<img class=wm src='{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}' style='top:1300px;width:380px'>")

only = sys.argv[1:]
with sync_playwright() as p:
    b = p.chromium.launch()
    for k, (w, h, inner) in P.items():
        if only and k not in only:
            continue
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        hp = TMP + k + '.html'; open(hp, 'w').write(page(w, h, inner))
        pg.goto('file://' + hp); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(700)
        # overflow check: anything poking outside the canvas
        ov = pg.evaluate("""()=>[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width&&(r.right>innerWidth+2||r.left<-2||r.bottom>innerHeight+2)}).length""")
        if ov: print('OVERFLOW', k, ov)
        pg.screenshot(path=TMP + k + '.png'); pg.close()
        Image.open(TMP + k + '.png').convert('RGB').save(O + k + '.jpg', quality=92)
        print('ok', k)
    b.close()
# launch slide 2 = the approved "It's a mat-ch!" phone slide (Find Your Mat-ch preview), reused as-is
import shutil; shutil.copy(R + '/assets/social/its-a-match/papaya-heiress/slide3.jpg', O + 'launch-2-phone.jpg')
