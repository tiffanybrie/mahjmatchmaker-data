import json
from PIL import Image
R='/home/claude/mahjmatchmaker-data/'
src=Image.open(R+'assets/hub/partner-brands-2026-11-05.jpg').convert('RGB')
bg=src.getpixel((540,700))
out=src.copy()
# clear the frame interior
from PIL import ImageDraw
d=ImageDraw.Draw(out); d.rectangle((44,211,1036,1224),fill=bg)
for p in json.load(open('placed.json')):
    im=Image.open(p['file']).convert('RGBA')
    w,h=round(p['w']),round(p['h'])
    if w>im.size[0]: print('UPSCALE',p['brand'],im.size,w)
    im=im.resize((w,h),Image.LANCZOS)
    out.paste(im,(round(p['x']),round(p['y'])),im)
out.save('wall.jpg',quality=93)
t=out.resize((390,488),Image.LANCZOS); t.save('wall_390.png')
print('ok')
