"""Post 1 of every tile set row: "Meet <set>", her INTRODUCTION carousel (Tiffany, Oct 19 evening).
Slides: 1 dating profile (cover) / 2 color wheel / 3 her colors / 4 her best features (favorite tiles) /
5 racks she's into / 6 made for each other (favorite match) / 7 her album is ready.
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
Image.open(R + f'assets/colorwheels/{key}-color-wheel.jpg').convert('RGB').save(f'{OUT}/2.jpg', quality=93)
Image.open(R + f'assets/social/{key}-launch/{key}-favorite-tiles.jpg').convert('RGB').save(f'{OUT}/4.jpg', quality=93)

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
pages = {3: nodots(open(f'{H}/s2.html').read()), 5: nodots(open(f'{H}/s3.html').read()), 6: nodots(open(f'{H}/s4.html').read()), 7: end}
args = ['node', R + 'scripts/social/tileprofile/shot.js', '1080', '1350']
for n, s in pages.items():
    p = f'{H}/intro-{n}.html'; open(p, 'w').write(s); args += [p, f'{OUT}/{n}.jpg']
subprocess.run(args, check=True, cwd=R + 'scripts/social/tileprofile', env={**os.environ, 'NODE_PATH': subprocess.check_output(['npm', 'root', '-g']).decode().strip()})
print(OUT)
