"""Oct 20 (Tiffany): the intro carousel as a dating profile you swipe through.
Slides 1-6 sit inside the SAME profile card (phone-shaped, ~1:1.56 like a Tinder card); slides 2-6 are laid out
natively for the card (big, legible text, no shrunken 1080 slides). Slide 7 is NOT in the card: you've reached the
back of her profile, so it's the plain "She's been MAT-ched" graphic (intro.py's 7.jpg as-is).
Footer on every card: Mahj Matchmaker wordmark + "Dating profile". Buttons: X + heart only (Tinder's look).
Usage: python3 intro_framed.py papaya-spritz   (run intro.py + swipe_profile.py first)"""
import sys, os, asyncio, shutil, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.async_api import async_playwright
from PIL import Image
import swipe_profile as SP
from common import css, url, load, R
key = sys.argv[1]; P, S = load(key); e = html.escape
SRC = f'{R}assets/social/{key}-launch/intro'; OUT = f'{R}assets/social/{key}-launch/intro-framed' + ('-open' if os.environ.get('OPEN') == '1' else ''); H = f'{R}assets/social/{key}-launch/html'
CARD = f'{R}assets/colorcards/{key}/00-{key}-mahjong-tiles-profile-d-card@2x.png'
os.makedirs(OUT, exist_ok=True); TMP = os.path.dirname(os.path.abspath(__file__)) + '/html'
OPEN = os.environ.get('OPEN') == '1'   # Option B (Tiffany Oct 20): same slides, not in the card from slide 2 on
CX, CY, CW, CH = 130, 22, 820, 1281
VER = lambda n: f'<svg width="{n}" height="{n}" viewBox="0 0 24 24"><path d="M12 21.5C5.5 16.6 2 13.2 2 8.9 2 5.9 4.4 3.5 7.3 3.5c1.9 0 3.6 1 4.7 2.5 1.1-1.5 2.8-2.5 4.7-2.5 2.9 0 5.3 2.4 5.3 5.4 0 4.3-3.5 7.7-10 12.6z" fill="#d6608c" stroke="#fff" stroke-width="1.2"/><path d="M7.6 11.3l3 3 5.8-5.8" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
HT = lambda n: f'<svg width="{n}" height="{n}" viewBox="0 0 24 24"><path d="M12 21.5C5.5 16.6 2 13.2 2 8.9 2 5.9 4.4 3.5 7.3 3.5c1.9 0 3.6 1 4.7 2.5 1.1-1.5 2.8-2.5 4.7-2.5 2.9 0 5.3 2.4 5.3 5.4 0 4.3-3.5 7.7-10 12.6z" fill="#c8325f"/></svg>'
L = 36; W = CW - 2 * L                                  # content margins inside the card
hdr = lambda t: (f'<div class="caps" style="position:absolute;left:{L}px;top:48px;font-size:17px;color:#5a6b85">{e(P["name"])} · her profile</div>'
                 f'<div class="cap" style="position:absolute;left:{L}px;top:82px;font-size:{t[1]}px;white-space:nowrap">{t[0]}</div>')
ab = lambda x, y, s, w='': f'<div style="position:absolute;left:{x}px;top:{y}px;{("width:%spx;" % w) if w else ""}{s}">'
cl = lambda t, y, extra='': f'{ab(L, y, "")}<span class="caps" style="font-size:19px;color:var(--pink)">{t}</span>{extra}</div>'

# ---- slide 2: her colors
hc = P['her_colors']; bk = {b[0].lower(): b[1] for b in hc['backs']}
cpap, clav, clime = bk.get('papaya', '#de7e30'), bk.get('lavender', '#a8a3e1'), bk.get('light lime', '#c8d7a5')
BACK_CUT = P.get('back_photo', 'assets/tiles/backs/' + key + '-back-and-side-omm.jpg').rsplit('.', 1)[0] + '-cutout.png'
k = .78; tx, ty = 36 - 134 * k, 196 - 268 * k; M = lambda x, y: (tx + x * k, ty + y * k)
diag = (f'<div style="position:absolute;left:0;top:0;width:1080px;height:1350px;transform:translate({tx}px,{ty}px) scale({k});transform-origin:0 0">'
        f'<div style="position:absolute;left:134px;top:268px;width:740px;height:478px;filter:drop-shadow(0 12px 16px rgba(80,40,20,.16))"><div style="position:absolute;inset:0;clip-path:inset(0 380px 0 0);background:url({url(BACK_CUT)}) no-repeat;background-size:858px auto;background-position:-95px -114px"></div></div>'
        f'<div style="position:absolute;left:60px;top:268px;width:740px;height:478px;filter:drop-shadow(0 12px 16px rgba(80,40,20,.16))"><div style="position:absolute;inset:0;clip-path:inset(0 0 0 440px);background:url({url(BACK_CUT)}) no-repeat;background-size:858px auto;background-position:-95px -114px"></div></div>'
        '<svg style="position:absolute;left:0;top:0" width="1080" height="1350">' +
        ''.join(f'<line x1="{x2}" y1="{y}" x2="798" y2="{y}" stroke="#054689" stroke-width="3.5"/><circle cx="{x2}" cy="{y}" r="8" fill="#fff" stroke="#054689" stroke-width="3.5"/>' for y, x2 in ((390, 601), (490, 650), (590, 703))) +
        '</svg></div>')
labs = ''.join(f'{ab(M(798, 0)[0] + 12, M(0, y)[1] - 17, "display:flex;align-items:center;gap:10px;font:700 26px/1.05 Bit;color:var(--navy)", 236)}<i style="flex:0 0 24px;height:24px;border-radius:50%;background:{c};box-shadow:0 0 0 3px #fff,0 1px 4px rgba(5,40,90,.25)"></i><span>{t}</span></div>'
               for y, t, c in ((390, 'Papaya', cpap), (490, 'Lavender layer', clav), (590, 'Light lime layer', clime)))
capy = M(0, 760)[1]
s2 = (hdr(('Her colors', 84)) + diag + labs +
      f'{ab(M(153,0)[0], capy, "text-align:center;font:700 19px Bit;letter-spacing:.2em;text-transform:uppercase;color:#5a6b85", 294*k)}the back</div>'
      f'{ab(M(560,0)[0], capy, "text-align:center;font:700 19px Bit;letter-spacing:.2em;text-transform:uppercase;color:#5a6b85", 200*k)}the side</div>'
      f'<img src="{url(f"assets/colorwheels/{key}-color-wheel-mini.png")}" style="position:absolute;left:14px;top:640px;width:430px;height:430px">'
      f'{ab(458, 690, "", 330)}<div class="caps" style="font-size:19px;color:var(--pink)">On the color wheel</div>'
      f'<div style="font:400 30px/1.3 Bit;color:#2c3e63;margin-top:18px"><b style="font-weight:700;color:var(--navy)">1 &nbsp;Papaya</b><br>bright, warm orange<div style="height:18px"></div><b style="font-weight:700;color:var(--navy)">2 &nbsp;Lavender</b><br>soft, cool, blue-leaning<div style="height:18px"></div><b style="font-weight:700;color:var(--navy)">3 &nbsp;Light lime</b><br>soft yellow-green</div>'
      f'<div style="margin-top:20px;font:italic 400 25px/1.3 PF;color:#5a6b85">Outer edge = bright.<br>Toward the center = soft.</div></div>')

# ---- slide 3: her faces
def chip(n, h, w, sw, fs, hs):
    return (f'<div style="width:{w}px;background:#fff;border-radius:14px;box-shadow:0 2px 10px rgba(5,40,90,.13);overflow:hidden"><div style="height:{sw}px;background:{h}"></div>'
            f'<div style="padding:9px 6px 10px;text-align:center"><div style="font:700 {fs}px/1.1 Bit;color:var(--navy)">{e(n)}</div><div style="font:500 {hs}px Bit;letter-spacing:.06em;color:#7a879c;margin-top:4px">{h.upper()}</div></div></div>')
mains = ''.join(chip(n, h, 236, 66, 27, 16) for n, h in [('Papaya', cpap), ('Lavender', clav), ('Light lime', clime)])
sw = (W - 3 * 16) // 4; sups = [chip(n, h, sw, 40, 23, 14) for n, h in hc['supporting']]
s3 = (hdr(('Her faces', 84)) +
      f'<div style="position:absolute;left:{L}px;top:192px;width:{W}px;height:470px;border-radius:20px;background:#fff url({url(H + "/faces-crop.jpg")}) center/cover;box-shadow:0 0 0 8px #fff,0 12px 26px rgba(6,40,90,.16)"></div>'
      + cl('Main colors', 700, '<span style="font:400 21px Bit;color:#5a6b85;margin-left:12px">her back + layers</span>') +
      f'{ab(L, 736, "display:flex;gap:20px", W)}{mains}</div>'
      + cl('Supporting colors', 900, '<span style="font:400 21px Bit;color:#5a6b85;margin-left:12px">from her faces</span>') +
      f'{ab(L, 936, "display:flex;gap:16px", W)}{"".join(sups[:4])}</div>{ab(L, 1046, "display:flex;gap:16px", W)}{"".join(sups[4:8])}</div>')

# ---- slide 4: her best features
FT = R + f'assets/tiles/faces/{key}/clean/'
FAV = P.get('best_features', {'top': ['The dancing dragons', ['dragon-coral', 'dragon-green'], 'My favorite dragons, and they come as a pair'],
       'singles': [['The crane', 'crane', 'Her gray-crowned<br>crane bird bam'], ['Ginger Lola', 'lola-ginger', 'The redheaded<br>matriarch'], ['The parasols', 'dot3', 'Little umbrellas']]})
ft = lambda kk, w: f'<img src="file://{FT}{kk}.png" style="width:{w}px;display:block">'
fl = lambda t: f'<div class="caps" style="font-size:21px;color:var(--pink);text-align:center;white-space:nowrap">{t}</div>'
fc = lambda t, s: f'<div class="pf" style="font-size:{s}px;line-height:1.22;color:#3c4f73;text-align:center">{t}</div>'
t0 = FAV['top']
sing = ''.join(f'<div style="display:flex;flex-direction:column;align-items:center;width:{W//3}px">{fl(n)}<div style="margin-top:14px">{ft(kk, 212)}</div><div style="margin-top:14px">{fc(c, 27)}</div></div>' for n, kk, c in FAV['singles'])
s4 = (hdr(('Her best features', 72)) +
      f'{ab(0, 196, "", CW)}{fl(t0[0])}<div style="display:flex;justify-content:center;gap:44px;margin-top:16px">{"".join(ft(kk, 250) for kk in t0[1])}</div><div style="margin-top:14px">{fc(t0[2], 31)}</div></div>'
      f'{ab(L, 676, "display:flex;justify-content:space-between", W)}{sing}</div>')

# ---- slide 5: racks she's into
RACK = {'Bird & Bamboo Lavender': 'assets/colorcards/papaya-spritz/racks/bird-and-bamboo-lavender.png', 'Peace Love Mahjong Chartreuse': 'assets/racks/card/peace-love-mahjong-chartreuse.png',
        'Peace Love Mahjong Oak': 'assets/racks/card/peace-love-mahjong-oak.png', 'Middle & Main Scalloped Beechwood': 'assets/racks/card/middle--main-scalloped-beechwood.png',
        'Mahjong Row & Co. Scalloped Tortoise': 'assets/racks/card/mahjong-row--co-scalloped-tortoise.png'}
BRANDS = ('Bird & Bamboo', 'Peace Love Mahjong', 'Middle & Main', 'Miss Mahjong', 'Mahjong Row & Co.', 'Bam Bird Boutique')
def rrow(r):
    b = next((x for x in BRANDS if r['name'].startswith(x)), r['name'].split()[0]); c = r['name'][len(b) + 1:]
    return (f'<div style="margin-top:24px"><div class="caps" style="font-size:17px;color:#8a6a80">{e(b)}</div><div class="pf" style="font-size:40px;font-weight:600;line-height:1.1;margin-top:2px">{e(c)}</div>'
            f'<img src="{url(RACK[r["name"]])}" style="display:block;width:{W}px;height:84px;object-fit:fill;margin-top:8px;filter:drop-shadow(0 8px 10px rgba(6,40,90,.18))"></div>')
grp = lambda g: ''.join(rrow(r) for r in P['racks'] if r.get('group', 'color') == g)
s5 = (hdr(("Racks she's into", 80)) +
      f'{ab(L, 180, "", W)}<div class="pf" style="font-size:29px;line-height:1.25;color:#3c4f73">A color from her layers, or a rack that goes with everything.</div>'
      f'<div class="caps" style="font-size:19px;color:var(--pink);margin-top:30px">Match her layers</div>{grp("color")}'
      f'<div style="margin-top:34px;display:flex;align-items:center;gap:14px"><span class="hand" style="font-size:52px;color:var(--navy);line-height:1">super versatile</span>'
      f'<svg width="62" height="40" viewBox="0 0 70 44"><path d="M4 8 C 28 4, 46 14, 58 34" fill="none" stroke="#c8325f" stroke-width="4" stroke-linecap="round"/><path d="M46 30 L 59 37 L 62 22" fill="none" stroke="#c8325f" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
      f'<span class="pf" style="font-size:27px;color:#3c4f73">my go-tos</span></div>{grp("versatile")}'
      f'<div class="hand" style="font-size:46px;margin-top:30px;color:var(--pink)">now, who she&rsquo;s dating &rarr;</div></div>')

# ---- slide 6: made for each other (text UNDER the photo row, Tiffany Oct 20)
pr = P['omm_launch']['pair']
cap = pr.get('together_caption') or f"{P['name']} on {pr['mat']}, in {pr['brand']}’s own photo"
s6 = (hdr(('Made for each other', 70)) +
      f'{ab(L, 166, "", W)}<div class="pf" style="font-size:31px;color:#3c4f73">Her official {e(pr["brand"])} pair: <b style="font-weight:600;color:var(--navy)">{e(pr["mat"])}</b></div></div>'
      f'<div style="position:absolute;left:{L}px;top:226px;width:{W}px;height:470px;border-radius:22px;background:url({url(pr["together"])}) 52% 42%/150%;box-shadow:0 10px 26px rgba(6,40,90,.16)">'
      f'<div style="position:absolute;left:16px;bottom:16px;background:rgba(255,255,255,.93);border-radius:99px;padding:8px 18px;font:600 20px Bit;color:var(--navy)">{e(cap)}</div></div>'
      f'{ab(0, 730, "display:flex;justify-content:center;align-items:center;gap:26px", CW)}'
      f'<div style="width:190px;height:190px;border-radius:50%;background:#fff url({url(pr["circle"])}) center/112% no-repeat;box-shadow:0 0 0 6px #fff,0 8px 20px rgba(6,40,90,.16)"></div>{HT(60)}'
      f'<div style="width:212px;height:212px;border-radius:18px;background:url({url(pr["img"])}) center/114%;box-shadow:0 8px 22px rgba(6,40,90,.16)"></div></div>'
      f'{ab(L, 984, "", W)}<div style="display:flex;align-items:center;gap:10px">{VER(34)}<span class="caps" style="font-size:20px;color:var(--pink)">Official pair</span></div>'
      f'<div style="font:400 29px/1.35 Bit;margin-top:10px;color:#2c3e63">{e(pr["why"])}</div></div>')
NATIVE = {2: s2, 3: s3, 4: s4, 5: s5, 6: s6}

def page(n):
    bars = ''.join(f'<i style="background:{"#054689" if j == n else "rgba(5,70,137,.16)"}"></i>' for j in range(1, 8))
    if n == 1:
        inner = f'<img src="file://{CARD}" style="position:absolute;inset:0;width:100%;height:100%"><div style="position:absolute;left:0;right:0;bottom:0;height:60px;background:#fff"></div>'
    else:
        inner = f'<div style="position:absolute;inset:0;background:var(--cream)"></div>{NATIVE[n]}<div class="bars">{bars}</div>'
    return f"""<!doctype html><html><head><meta charset=utf8><style>{css(1080, 1350, S['col'])}
html,body{{background:{'var(--cream)' if OPEN else '#f6e9df'}}}
.card{{position:absolute;left:{CX}px;top:{CY}px;width:{CW}px;height:{CH}px;background:{'var(--cream)' if OPEN else '#fff'};border-radius:{0 if OPEN else 38}px;overflow:{'visible' if OPEN else 'hidden'};
  box-shadow:{'none' if OPEN else '0 26px 60px rgba(5,40,90,.18),0 4px 12px rgba(5,40,90,.09)'}}}
.bars{{position:absolute;left:24px;right:24px;top:20px;display:flex;gap:9px;z-index:3}}
.bars i{{flex:1;height:7px;border-radius:4px}}
.sign{{position:absolute;left:0;right:0;bottom:78px;display:flex;justify-content:center;align-items:center;gap:12px}}
.sign img{{width:200px}}
.sign span{{font:700 16px Bit;letter-spacing:.22em;text-transform:uppercase;color:#c8325f;padding-top:4px}}
.btns{{position:absolute;left:0;right:0;top:{CY + CH - 56}px;display:flex;justify-content:center;align-items:center;gap:120px}}
</style></head><body>
{'' if OPEN else '''<div style="position:absolute;right:-190px;top:-170px;width:650px;height:650px;border-radius:50%;background:#f9dccf"></div>
<div style="position:absolute;left:-170px;bottom:-200px;width:530px;height:530px;border-radius:50%;background:#efdccd"></div>'''}
<div class="card">{inner}
 <div class="sign"><img src="{url('assets/brand/mahjmatchmaker-wordmark-notag.png')}"><span>Dating profile</span></div>
</div>
<div class="btns">{SP.buttons(112, 50, 54)}</div>
</body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=2)
        for n in range(2 if OPEN else 1, 7):
            hp = f'{TMP}/framed-{n}.html'; open(hp, 'w').write(page(n))
            await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle'); await pg.evaluate('document.fonts.ready')
            png = f'{TMP}/framed-{n}@2x.png'; await pg.screenshot(path=png)
            Image.open(png).convert('RGB').resize((1080, 1350), Image.LANCZOS).save(f'{OUT}/{n}.jpg', quality=93)
        await b.close()
    shutil.copy(f'{SRC}/7.jpg', f'{OUT}/7.jpg')
    if OPEN: shutil.copy(OUT.replace('-open', '') + '/1.jpg', f'{OUT}/1.jpg')   # slide 1 = the same profile card   # slide 7 = plain graphic, not in the card
asyncio.run(main()); print(OUT)
