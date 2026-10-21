"""Story version of all 3 'It's a mat-ch!' slides (Tiffany, Oct 21 12:56: "This carousel's good. It deserves to be out there.").
Frame 1 = render.py story.jpg. Frames 2-3 = slide 2/3 lifted off their paper (bg + pink blobs keyed out) onto a 1080x1920
paper with full blobs, inside the story safe band (top 262px, bottom 352px clear).
Usage: python3 scripts/social/its_a_match/story_frames.py assets/social/its-a-match/papaya-heiress"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
d = sys.argv[1].rstrip('/') + '/'; o = d + 'story-frames/'; os.makedirs(o, exist_ok=True)
BG = np.array([(250, 243, 233), (250, 227, 233), (251, 231, 233), (249, 242, 232)], float)
Image.open(d + 'story.jpg').convert('RGB').save(o + 'story-1.jpg', quality=93)
for i, n in ((2, 'slide2'), (3, 'slide3')):
    s = np.asarray(Image.open(d + n + '.jpg').convert('RGB')).astype(float)
    dist = np.min(np.linalg.norm(s[:, :, None, :] - BG[None, None], axis=3), axis=2)
    mask = Image.fromarray(np.clip((dist - 3) * 255 / 25, 0, 255).astype('uint8'))
    c = Image.new('RGB', (1080, 1920), (250, 243, 233)); dr = ImageDraw.Draw(c)
    dr.ellipse((620, -260, 1400, 520), fill=(250, 227, 233)); dr.ellipse((-380, 1380, 420, 2180), fill=(251, 231, 233))
    top, bot = 262, 1920 - 352; h = bot - top; w = round(1080 * h / 1350)
    c.paste(Image.fromarray(s.astype('uint8')).resize((w, h), Image.LANCZOS), ((1080 - w) // 2, top), mask.resize((w, h), Image.LANCZOS))
    c.save(o + f'story-{i}.jpg', quality=93)
print('ok', o)
