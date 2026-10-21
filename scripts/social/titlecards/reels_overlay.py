"""Reels UI safe-area check (Oct 21, from Tiffany's screenshot of the live reel). Draws Instagram's Reels chrome as
semi-transparent boxes over a 1080x1920 frame: top header band (y < 190), right icon column (x 880-1080 from y 1150),
bottom username/caption band (y > 1500), plus the text-safe box (x 90-860). Text must not touch the red/blue boxes.
Usage: python3 scripts/social/titlecards/reels_overlay.py frame.png out.jpg"""
import sys
from PIL import Image, ImageDraw, ImageFont
im = Image.open(sys.argv[1]).convert('RGB').resize((1080, 1920)); d = ImageDraw.Draw(im, 'RGBA')
d.rectangle((0, 0, 1080, 190), fill=(0, 0, 0, 70))
d.rectangle((880, 1150, 1080, 1920), fill=(220, 0, 0, 80))
for i, y in enumerate(range(1190, 1760, 115)):  # heart, comment, repost, share, save
    d.ellipse((935, y, 1025, y + 90), outline=(255, 255, 255, 230), width=6)
d.rectangle((0, 1500, 880, 1920), fill=(0, 60, 200, 70))
d.rectangle((90, 0, 860, 1920), outline=(0, 160, 0, 200), width=3)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
except Exception: f = ImageFont.load_default()
d.text((30, 1530), '@mahjmatchmaker  caption...', fill=(255, 255, 255, 255), font=f)
d.text((100, 10), 'text-safe x 90-860', fill=(0, 120, 0, 255), font=f)
im.save(sys.argv[2], quality=90); print(sys.argv[2])
