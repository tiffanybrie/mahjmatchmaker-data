"""Post 1 of every tile set row: "Meet <set>", her INTRODUCTION carousel (Tiffany, Oct 19 evening).
Slides (Oct 19 night): 1 dating profile (cover) / 2 her colors (layer diagram + small color wheel + faces) /
3 her best features (favorite tiles) / 4 racks she's into / 5 made for each other (favorite match) / 6 her album is ready.
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
st = Image.open(R + f'assets/colorcards/{key}/00-{key}-mahjong-tiles-profile-c-story.jpg').convert('RGB')
crop = st.crop((0, 140, 1080, 1760)); h = 1350; w = round(1080 * h / crop.height)
cv = Image.new('RGB', (1080, 1350), st.getpixel((10, 1000))); cv.paste(crop.resize((w, h), Image.LANCZOS), ((1080 - w) // 2, 0))
cv.save(f'{OUT}/1.jpg', quality=93)
Image.open(R + f'assets/social/{key}-launch/{key}-favorite-tiles.jpg').convert('RGB').save(f'{OUT}/3.jpg', quality=93)

e = __import__('html').escape
end = f"""<!doctype html><html><head><meta charset=utf8><style>{css(1080, 1350, S['col'])}</style></head><body>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;padding:96px 80px 0">
 <div class="caps" style="font-size:20px;color:#5a6b85">{e(P['name'])} · {e(P['brand'])}</div>
 <div class="cap" style="font-size:108px;margin-top:22px;line-height:.95">Her album<br><span style="color:var(--acc)">is ready</span></div>
 <div class="ph" style="margin-top:40px;width:440px;height:550px;border-radius:22px;background-image:url({url(f'assets/covers/albums/w800/00-{key}-mahjong-tiles-cover.jpg')});box-shadow:0 0 0 10px #fff,0 16px 36px rgba(6,40,90,.20);transform:rotate(-2deg)"></div>
 <div class="pf" style="font-size:46px;margin-top:46px">See all <b style="font-weight:600;color:var(--pink)">{P['matches']}</b> of her matches</div>
 <div class="pill" style="margin-top:22px;background:var(--pink)">link in bio &rarr;</div>
 <div style="margin-top:28px;font:700 30px Bit">Code <span style="color:var(--pink)">MAHJMATCH</span> at {e(P['brand'])}</div>
 <img src="{url('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="width:420px;margin-top:34px">
</div></body></html>"""
# merged "Her colors" slide (Tiffany, Oct 19 night): layer diagram from the brand's back + side photo, small color wheel, face dots
BACK = P.get('back_photo', 'assets/tiles/backs/' + key + '-back-and-side-omm.jpg')
bk = {b[0].lower(): b[1] for b in P['her_colors']['backs']}
cpap, clav, clime = bk.get('papaya', '#de7e30'), bk.get('lavender', '#a8a3e1'), bk.get('light lime', '#c8d7a5')
faces = ''.join(f'<span style="display:inline-flex;align-items:center;gap:8px;margin-right:18px"><i style="width:26px;height:26px;border-radius:50%;background:{h};box-shadow:0 0 0 3px #fff,0 1px 4px rgba(5,40,90,.2)"></i>{e(n.title())}</span>' for n, h in P['her_colors']['faces'])
WHEEL = url(f'assets/colorwheels/{key}-color-wheel-mini.png')
def lab(y, txt, col, x2):
    return (f'<div style="position:absolute;left:806px;top:{y-22}px;display:flex;align-items:center;gap:10px;font:700 27px Bit;color:var(--navy);white-space:nowrap">'
            f'<i style="width:26px;height:26px;border-radius:50%;background:{col};box-shadow:0 0 0 3px #fff,0 1px 4px rgba(5,40,90,.25)"></i>{txt}</div>'
            f'<svg style="position:absolute;left:0;top:0" width="1080" height="1350"><line x1="{x2}" y1="{y}" x2="798" y2="{y}" stroke="#054689" stroke-width="3"/><circle cx="{x2}" cy="{y}" r="7" fill="#fff" stroke="#054689" stroke-width="3"/></svg>')
colors = f"""<!doctype html><html><head><meta charset=utf8><style>{css(1080, 1350, S['col'])}</style></head><body>
<div style="position:relative;width:1080px;height:1350px">
<div style="position:absolute;top:58px;left:72px;right:72px;display:flex;justify-content:space-between"><span class="caps" style="font-size:19px;color:#5a6b85">{e(P['name'])} · her profile</span><span class="caps" style="font-size:19px;color:#5a6b85">1 · her colors</span></div>
<div class="cap" style="position:absolute;top:118px;left:72px;font-size:96px">Her colors</div>
<div style="position:absolute;left:60px;top:268px;width:740px;height:478px;background:#fff;border-radius:28px;box-shadow:0 10px 26px rgba(5,40,90,.10);overflow:hidden">
 <div style="position:absolute;inset:0;background:url({url(BACK)}) no-repeat;background-size:858px auto;background-position:-95px -114px"></div></div>
{lab(390, 'Papaya', cpap, 601)}{lab(490, 'Lavender layer', clav, 650)}{lab(590, 'Light lime layer', clime, 703)}
<div style="position:absolute;left:79px;width:294px;top:760px;text-align:center;font:700 21px Bit;letter-spacing:.2em;text-transform:uppercase;color:#5a6b85">the back</div><div style="position:absolute;left:560px;width:200px;top:760px;text-align:center;font:700 21px Bit;letter-spacing:.2em;text-transform:uppercase;color:#5a6b85">the side</div>
<img src="{WHEEL}" style="position:absolute;left:60px;top:830px;width:440px;height:440px">
<div style="position:absolute;left:540px;top:850px;right:60px">
 <div class="caps" style="font-size:19px;color:var(--pink)">On the color wheel</div>
 <div style="font:400 26px/1.5 Bit;color:#2c3e63;margin-top:14px">1 &nbsp;Papaya · warm orange<br>2 &nbsp;Lavender · cool, blue-leaning<br>3 &nbsp;Light lime · soft yellow-green</div>
 <div class="caps" style="font-size:19px;color:var(--pink);margin-top:34px">Her faces</div>
 <div style="font:600 24px Bit;color:var(--navy);margin-top:14px;line-height:2.1">{faces}</div>
</div>
</div></body></html>"""
pages = {2: colors, 3: None, 4: nodots(open(f'{H}/s3.html').read()), 5: nodots(open(f'{H}/s4.html').read()), 6: end}
args = ['node', R + 'scripts/social/tileprofile/shot.js', '1080', '1350']
for n, s in pages.items():
    if s is None: continue
    p = f'{H}/intro-{n}.html'; open(p, 'w').write(s); args += [p, f'{OUT}/{n}.jpg']
subprocess.run(args, check=True, cwd=R + 'scripts/social/tileprofile', env={**os.environ, 'NODE_PATH': subprocess.check_output(['npm', 'root', '-g']).decode().strip()})
print(OUT)
