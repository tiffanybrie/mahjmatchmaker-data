"""Post 1 of every tile set row: "Meet <set>", her INTRODUCTION carousel (Tiffany, Oct 19 evening).
Slides (Oct 19 night): 1 dating profile (cover) / 2 her colors (layer diagram + small color wheel) /
3 her faces (brand photo of the faces + main & supporting color cards) / 4 her best features (favorite tiles) /
5 racks she's into / 6 made for each other (favorite match) / 7 she's been matched.
No baked-in dots (Instagram shows its own). Needs carousel.py html first (s2 colors, s3 racks, s4 pair).
Usage: python3 intro.py papaya-spritz"""
import sys, os, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from PIL import Image

key = sys.argv[1]; P, S = load(key)
OUT = R + f'assets/social/{key}-launch/intro'; H = R + f'assets/social/{key}-launch/html'; os.makedirs(OUT, exist_ok=True)
subprocess.run(['python3', R + 'scripts/social/tileprofile/carousel.py', key, H], check=True, capture_output=True)
nodots = lambda s: re.sub(r'<div class="dots">.*?</div>', '', s, flags=re.S)

# slide 1: dating profile story cropped to 4:5 on cream
st = Image.open(R + f'assets/colorcards/{key}/00-{key}-mahjong-tiles-profile-d-story.jpg').convert('RGB')
crop = st.crop((0, 140, 1080, 1760)); h = 1350; w = round(1080 * h / crop.height)
cv = Image.new('RGB', (1080, 1350), st.getpixel((10, 1000))); cv.paste(crop.resize((w, h), Image.LANCZOS), ((1080 - w) // 2, 0))
cv.save(f'{OUT}/1.jpg', quality=93)
Image.open(R + f'assets/social/{key}-launch/{key}-favorite-tiles.jpg').convert('RGB').save(f'{OUT}/4.jpg', quality=93)

e = __import__('html').escape
# end slide (Tiffany, Oct 19 night): album cover with her real match cards peeking out behind (homepage holiday style)
import glob as _g
def _card(slug): 
    f = _g.glob(R + f'assets/cards/{key}/{key}-mahjong-tiles-*{slug}-mat.jpg'); return url(f[0]) if f else None
_peek = [c for c in (_card(x) for x in P.get('album_peek', [])) if c][:4]
_pos = [(-268, 40, -11, 1), (268, 40, 11, 1), (-150, 0, -5, 2), (150, 0, 5, 2)]
fan = ''
for (dx, dy, rot, z), c in sorted(zip(_pos, _peek), key=lambda t: t[0][3]):
    fan += (f'<div class="ph" style="position:absolute;left:{450 - 180 + dx}px;top:{dy + 50}px;width:360px;height:450px;border-radius:18px;'
            f'background-image:url({c});box-shadow:0 0 0 8px #fff,0 12px 28px rgba(6,40,90,.18);transform:rotate({rot}deg);z-index:{z}"></div>')
fan += (f'<div class="ph" style="position:absolute;left:{450 - 220}px;top:10px;width:440px;height:550px;border-radius:22px;z-index:5;'
        f"background-image:url({url(f'assets/covers/albums/w800/00-{key}-mahjong-tiles-cover.jpg')});box-shadow:0 0 0 10px #fff,0 18px 40px rgba(6,40,90,.24)\"></div>")
end = f"""<!doctype html><html><head><meta charset=utf8><style>{css(1080, 1350, S['col'])}</style></head><body>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;padding:96px 80px 0">
 <div class="caps" style="font-size:20px;color:#5a6b85">{e(P['name'])} · {e(P['brand'])}</div>
 <div class="cap" style="font-size:108px;margin-top:22px;line-height:.95">She&rsquo;s been<br><span style="color:var(--acc)">matched</span></div>
 <div style="position:relative;margin-top:34px;width:900px;height:590px">{fan}</div>
 <div class="pf" style="font-size:46px;margin-top:46px">See all <b style="font-weight:600;color:var(--pink)">{P['matches']}</b> of her match cards</div>
 <div class="pill" style="margin-top:22px;background:var(--pink)">link in bio &rarr;</div>
 <div style="margin-top:28px;font:700 30px Bit">Code <span style="color:var(--pink)">MAHJMATCH</span> at {e(P['brand'])}</div>
 <img src="{url('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="width:420px;margin-top:34px">
</div></body></html>"""
# merged "Her colors" slide (Tiffany, Oct 19 night): layer diagram from the brand's back + side photo, small color wheel, face dots
BACK = P.get('back_photo', 'assets/tiles/backs/' + key + '-back-and-side-omm.jpg')
BACK_CUT = BACK.rsplit('.', 1)[0] + '-cutout.png'
bk = {b[0].lower(): b[1] for b in P['her_colors']['backs']}
cpap, clav, clime = bk.get('papaya', '#de7e30'), bk.get('lavender', '#a8a3e1'), bk.get('light lime', '#c8d7a5')
faces = ''.join(f'<span style="display:inline-flex;align-items:center;gap:10px"><i style="width:26px;height:26px;border-radius:50%;background:{h};box-shadow:0 0 0 3px #fff,0 1px 4px rgba(5,40,90,.2)"></i>{e(n.title())}</span>' for n, h in P['her_colors']['faces'])
WHEEL = url(f'assets/colorwheels/{key}-color-wheel-mini.png')
def lab(y, txt, col, x2):
    return (f'<div style="position:absolute;left:806px;top:{y-22}px;display:flex;align-items:center;gap:10px;font:700 27px Bit;color:var(--navy);white-space:nowrap">'
            f'<i style="width:26px;height:26px;border-radius:50%;background:{col};box-shadow:0 0 0 3px #fff,0 1px 4px rgba(5,40,90,.25)"></i>{txt}</div>'
            f'<svg style="position:absolute;left:0;top:0" width="1080" height="1350"><line x1="{x2}" y1="{y}" x2="798" y2="{y}" stroke="#054689" stroke-width="3"/><circle cx="{x2}" cy="{y}" r="7" fill="#fff" stroke="#054689" stroke-width="3"/></svg>')
colors = f"""<!doctype html><html><head><meta charset=utf8><style>{css(1080, 1350, S['col'])}</style></head><body>
<div style="position:relative;width:1080px;height:1350px">
<div style="position:absolute;top:58px;left:72px;right:72px;display:flex;justify-content:space-between"><span class="caps" style="font-size:19px;color:#5a6b85">{e(P['name'])} · her profile</span><span class="caps" style="font-size:19px;color:#5a6b85">1 · her colors</span></div>
<div class="cap" style="position:absolute;top:118px;left:72px;font-size:96px">Her colors</div>
<div style="position:absolute;left:60px;top:268px;width:740px;height:478px;filter:drop-shadow(0 12px 16px rgba(80,40,20,.16))"><div style="position:absolute;inset:0;background:url({url(BACK_CUT)}) no-repeat;background-size:858px auto;background-position:-95px -114px"></div></div>
{lab(390, 'Papaya', cpap, 601)}{lab(490, 'Lavender layer', clav, 650)}{lab(590, 'Light lime layer', clime, 703)}
<div style="position:absolute;left:79px;width:294px;top:760px;text-align:center;font:700 21px Bit;letter-spacing:.2em;text-transform:uppercase;color:#5a6b85">the back</div><div style="position:absolute;left:560px;width:200px;top:760px;text-align:center;font:700 21px Bit;letter-spacing:.2em;text-transform:uppercase;color:#5a6b85">the side</div>
<img src="{WHEEL}" style="position:absolute;left:44px;top:800px;width:510px;height:510px">
<div style="position:absolute;left:584px;top:880px;right:56px">
 <div class="caps" style="font-size:21px;color:var(--pink)">On the color wheel</div>
 <div style="font:400 30px/1.35 Bit;color:#2c3e63;margin-top:22px"><b style="font-weight:700;color:var(--navy)">1 &nbsp;Papaya</b><br>warm orange<div style="height:22px"></div><b style="font-weight:700;color:var(--navy)">2 &nbsp;Lavender</b><br>cool, blue-leaning<div style="height:22px"></div><b style="font-weight:700;color:var(--navy)">3 &nbsp;Light lime</b><br>soft yellow-green</div>
</div>
</div></body></html>"""
# slide 3 "Her faces" (Tiffany, Oct 19 night): the brand's photo of the faces + ALL the color cards in one place
# (main colors = the back layers, supporting colors = measured from the faces). No color cards anywhere else.
hc = P['her_colors']
fx = hc['faces_crop']; fc = Image.open(R + hc['faces_photo']).convert('RGB').crop(tuple(fx))
for box in hc.get('faces_blank', []):  # paint out stray bits (Papaya: corner of the loose back tile)
    fc.paste(fc.getpixel((fc.width - 3, 3)), tuple(box))
fc.save(f'{H}/faces-crop.jpg', quality=94)
def chip(n, h, w, sw):
    return (f'<div style="width:{w}px;background:#fff;border-radius:14px;box-shadow:0 2px 10px rgba(5,40,90,.13);overflow:hidden">'
            f'<div style="height:{sw}px;background:{h}"></div><div style="padding:10px 6px 11px;text-align:center">'
            f'<div style="font:700 {19 if w < 130 else 23}px/1.1 Bit;color:var(--navy)">{e(n)}</div>'
            f'<div style="font:500 14px Bit;letter-spacing:.06em;color:#7a879c;margin-top:4px">{h.upper()}</div></div></div>')
mains = ''.join(chip(n, h, 170, 88) for n, h in [('Papaya', cpap), ('Lavender', clav), ('Light lime', clime)])
sups = ''.join(chip(n, h, 106, 70) for n, h in hc['supporting'])
facesl = f"""<!doctype html><html><head><meta charset=utf8><style>{css(1080, 1350, S['col'])}</style></head><body>
<div style="position:relative;width:1080px;height:1350px">
<div style="position:absolute;top:58px;left:72px;right:72px;display:flex;justify-content:space-between"><span class="caps" style="font-size:19px;color:#5a6b85">{e(P['name'])} · her profile</span><span class="caps" style="font-size:19px;color:#5a6b85">2 · her faces</span></div>
<div class="cap" style="position:absolute;top:118px;left:72px;font-size:96px">Her faces</div>
<div style="position:absolute;left:72px;top:250px;width:936px;height:629px;border-radius:22px;background:#fff url({url(H + '/faces-crop.jpg')}) center/cover;box-shadow:0 0 0 10px #fff,0 14px 30px rgba(6,40,90,.16)"></div>
<div style="position:absolute;left:72px;top:922px;right:72px">
 <div style="display:flex;align-items:flex-end;gap:22px">
  <div style="width:186px;padding-bottom:6px"><div class="caps" style="font-size:19px;color:var(--pink)">Main colors</div><div style="font:400 22px/1.3 Bit;color:#5a6b85;margin-top:6px">her back<br>+ layers</div></div>
  <div style="display:flex;gap:16px">{mains}</div>
 </div>
 <div class="caps" style="font-size:19px;color:var(--pink);margin-top:26px">Supporting colors <span style="color:#5a6b85;letter-spacing:.1em">· from her faces</span></div>
 <div style="display:flex;justify-content:space-between;margin-top:12px">{sups}</div>
</div>
</div></body></html>"""
pages = {2: colors, 3: facesl, 4: None, 5: nodots(open(f'{H}/s3.html').read()).replace('2 · racks', '3 · racks'), 6: nodots(open(f'{H}/s4.html').read()).replace('3 · made', '4 · made'), 7: end}
args = ['node', R + 'scripts/social/tileprofile/shot.js', '1080', '1350']
for n, s in pages.items():
    if s is None: continue
    p = f'{H}/intro-{n}.html'; open(p, 'w').write(s); args += [p, f'{OUT}/{n}.jpg']
subprocess.run(args, check=True, cwd=R + 'scripts/social/tileprofile', env={**os.environ, 'NODE_PATH': subprocess.check_output(['npm', 'root', '-g']).decode().strip()})
print(OUT)
