from PIL import Image, ImageDraw
def split(fimg, fbox, bimg, bbox, out):
    f = Image.open(fimg).convert('RGB').crop(fbox); s = 700 / f.height; f = f.resize((round(f.width * s), 700), Image.LANCZOS)
    f = f.crop((f.width - 800, 0, f.width, 700))
    b = Image.open(bimg).convert('RGB').crop(bbox); b = b.resize((800, 700), Image.LANCZOS)
    c = Image.new('RGB', (1600, 700), 'white'); c.paste(f, (0, 0)); c.paste(b, (800, 0))
    ImageDraw.Draw(c).rectangle((796, 0, 803, 700), fill='white'); c.save(out, quality=90); return c
A = 'east-meets-west-tortoise-shell-tile-set-copy'; E = 'east-meets-west-tortoise-shell-tile-set'
split(f'{A}_00.jpg', (645, 1875, 2970, 3270), f'{A}_01.jpg', (2933, 1333, 3733, 2033), 'bam-bird-classic-tortoise-split.jpg')
split(f'{E}_00.jpg', (1058, 2171, 3336, 3440), f'{E}_00.jpg', (194, 3159, 944, 3815), 'bam-bird-emw-tortoise-split.jpg')
rows = []
for n in ['bam-bird-classic-tortoise-split.jpg', 'bam-bird-emw-tortoise-split.jpg']:
    c = Image.open(n); sq = c.crop((450, 0, 1150, 700)).resize((300, 300)); m = Image.new('L', (300, 300), 0); ImageDraw.Draw(m).ellipse((0, 0, 299, 299), fill=255)
    r = Image.new('RGB', (1000, 310), 'white'); r.paste(c.resize((686, 300)), (0, 5)); r.paste(sq, (695, 5), m); rows.append(r)
S = Image.new('RGB', (1000, 620), 'white'); [S.paste(r, (0, i * 310)) for i, r in enumerate(rows)]; S.save('after.jpg', quality=88)
