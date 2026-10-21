"""Turn 1080x1350 feed slides into 1080x1920 story frames (Tiffany, Oct 21 12:56/1:05: "This carousel's good. It deserves
to be out there."). Each slide is lifted off its paper (paper + blush blobs keyed out) onto a 1080x1920 paper with full
blobs, inside the story safe band (top 262px, bottom 352px clear). --room N on frame 1 shrinks it so an N-px empty band is
left above the bottom safe zone for a VISIBLE sticker (e.g. the @ohmymahjong mention OMM should reshare).

Usage:
  python3 scripts/social/its_a_match/story_frames.py its-a-match DIR          (Papaya x Heiress: story.jpg + slide2/3)
  python3 scripts/social/its_a_match/story_frames.py slides OUT_DIR a.jpg b.jpg c.jpg [--room 200] [--last-room 160] [--blur]
  --blur: for slides whose background can't be keyed (photos/gradients): whole slide as a rounded card on plain paper.
  --fit (Tiffany, Oct 21 1:47pm, the default for new stories): each slide's CONTENT (paper keyed out, bounding box) is
  scaled as big as it can go and centred in the story safe band (top 250 / bottom 340 clear, 35px sides). No empty band
  for stickers: stickers sit over the cream margin. Render sources at 2x so upscaled text stays sharp.
  python3 story_frames.py slides OUT_DIR a.png b.png --fit [--paper intro]"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw

BG = np.array([(250, 243, 233), (250, 227, 233), (251, 231, 233), (249, 242, 232), (251, 227, 234), (247, 239, 228), (246, 233, 223)], float)
SAFE_T, SAFE_B, SIDE = 250, 1920 - 340, 35
TOP, BOT = 262, 1920 - 352


def frame_blur(src, out, room=0):
    """Slides with a photo/gradient background that can't be keyed: the slide sits whole (rounded, soft shadow) in the
    safe band on plain paper with the blush blobs."""
    from PIL import ImageFilter
    sl = Image.open(src).convert('RGB')
    bg = Image.new('RGB', (1080, 1920), (250, 243, 233)); dr = ImageDraw.Draw(bg)
    dr.ellipse((620, -260, 1400, 520), fill=(250, 227, 233)); dr.ellipse((-380, 1380, 420, 2180), fill=(251, 231, 233))
    h = BOT - TOP - room; w = round(1080 * h / 1350); x = (1080 - w) // 2
    sh = Image.new('L', (1080, 1920), 0); ImageDraw.Draw(sh).rounded_rectangle((x + 4, TOP + 14, x + w + 4, TOP + h + 14), 36, fill=90)
    bg.paste((60, 40, 30), (0, 0), sh.filter(ImageFilter.GaussianBlur(18)))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 32, fill=255)
    bg.paste(sl.resize((w, h), Image.LANCZOS), (x, TOP), m)
    bg.save(out, quality=93)


def paper(kind='pink'):
    """Story paper. 'pink' = the It's a mat-ch / OMM paper; 'intro' = the profile-carousel paper (#f6e9df, peach blobs)."""
    if kind == 'intro':
        c = Image.new('RGB', (1080, 1920), (246, 233, 223)); dr = ImageDraw.Draw(c)
        dr.ellipse((590, -250, 1310, 470), fill=(249, 220, 207)); dr.ellipse((-220, 1540, 420, 2180), fill=(239, 220, 205))   # = intro_framed STORY blobs
        return c
    c = Image.new('RGB', (1080, 1920), (250, 243, 233)); dr = ImageDraw.Draw(c)
    dr.ellipse((700, -260, 1400, 440), fill=(251, 227, 234)); dr.ellipse((-330, 1500, 330, 2160), fill=(251, 231, 233))
    return c


def fit(src, out, kind='pink'):
    """Key the slide's paper out, crop to its content, scale it as big as the safe band allows, centre it there."""
    im = Image.open(src).convert('RGB'); s = np.asarray(im).astype(float)
    dist = np.min(np.linalg.norm(s[:, :, None, :] - BG[None, None], axis=3), axis=2)
    a = np.clip((dist - 3) * 255 / 25, 0, 255).astype('uint8')
    ys, xs = np.where(a > 60)
    # ignore lone specks: bbox from rows/cols with real content
    rows = np.where((a > 60).sum(1) > 3)[0]; cols = np.where((a > 60).sum(0) > 3)[0]
    pad = round(im.width / 1080 * 6)
    x0, x1 = max(cols[0] - pad, 0), min(cols[-1] + pad, im.width); y0, y1 = max(rows[0] - pad, 0), min(rows[-1] + pad, im.height)
    crop = im.crop((x0, y0, x1, y1)); m = Image.fromarray(a).crop((x0, y0, x1, y1))
    k = min((1080 - 2 * SIDE) / crop.width, (SAFE_B - SAFE_T) / crop.height)
    w, h = round(crop.width * k), round(crop.height * k)
    c = paper(kind); x = (1080 - w) // 2; y = SAFE_T + (SAFE_B - SAFE_T - h) // 2
    c.paste(crop.resize((w, h), Image.LANCZOS), (x, y), m.resize((w, h), Image.LANCZOS))
    c.save(out, quality=93)
    print(f'fit {os.path.basename(out)}: content {w}x{h} at y {y}-{y + h}')


def frame(src, out, room=0):
    s = np.asarray(Image.open(src).convert('RGB')).astype(float)
    dist = np.min(np.linalg.norm(s[:, :, None, :] - BG[None, None], axis=3), axis=2)
    mask = Image.fromarray(np.clip((dist - 3) * 255 / 25, 0, 255).astype('uint8'))
    c = Image.new('RGB', (1080, 1920), (250, 243, 233)); dr = ImageDraw.Draw(c)
    dr.ellipse((620, -260, 1400, 520), fill=(250, 227, 233)); dr.ellipse((-380, 1380, 420, 2180), fill=(251, 231, 233))
    h = BOT - TOP - room; w = round(1080 * h / 1350)
    c.paste(Image.fromarray(s.astype('uint8')).resize((w, h), Image.LANCZOS), ((1080 - w) // 2, TOP), mask.resize((w, h), Image.LANCZOS))
    c.save(out, quality=93)


if __name__ == '__main__':
    a = sys.argv[1:]
    room = 0; last_room = 0; fn = frame
    if '--room' in a:
        i = a.index('--room'); room = int(a[i + 1]); del a[i:i + 2]
    if '--last-room' in a:
        i = a.index('--last-room'); last_room = int(a[i + 1]); del a[i:i + 2]
    if '--blur' in a:
        a.remove('--blur'); fn = frame_blur
    kind = 'pink'
    if '--paper' in a:
        i = a.index('--paper'); kind = a[i + 1]; del a[i:i + 2]
    if '--fit' in a:
        a.remove('--fit'); fn = lambda src, out, r=0: fit(src, out, kind)
    if a[0] == 'its-a-match':
        d = a[1].rstrip('/') + '/'; o = d + 'story-frames/'; os.makedirs(o, exist_ok=True)
        Image.open(d + 'story.jpg').convert('RGB').save(o + 'story-1.jpg', quality=93)
        for i, n in ((2, 'slide2'), (3, 'slide3')):
            frame(d + n + '.jpg', o + f'story-{i}.jpg')
    else:
        o = a[1]; os.makedirs(o, exist_ok=True)
        srcs = a[2:]
        for i, src in enumerate(srcs, 1):
            fn(src, f'{o}/story-{i}.jpg', room if i == 1 else (last_room if i == len(srcs) else 0))
    print('ok', o)
