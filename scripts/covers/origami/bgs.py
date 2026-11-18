"""Origami Timber cover backgrounds (Tiffany Nov 17 12:44am: covers must be FULL layouts, photo fills the frame, no white space).
Sources: Bam Bird listing images (origami-tile-set.json), Timber only. Writes 1080x1350 backgrounds to <out>/bg_*.jpg."""
import sys, os
from PIL import Image, ImageFilter
S = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
def fit(im, box):  # crop box then resize to W,H
    return im.crop(box).resize((W, H), Image.LANCZOS)
# A: pile in the velvet bag (img 7), zoomed into the pile
f07 = Image.open(f'{S}/f07.jpg'); k = f07.width / 667
cx, cy, w = 432 * k, 312 * k, 214 * k
fit(f07, (int(cx - w / 2), int(cy - w * 1.25 / 2), int(cx + w / 2), int(cy + w * 1.25 / 2))).save(f'{OUT}/bg_pile.jpg', quality=93)
# B: Timber backs wall (img 4 tray), straightened
f04 = Image.open(f'{S}/f04.jpg'); k = f04.width / 667
ANG = float(os.environ.get('ANG', '-40'))
r = f04.rotate(ANG, resample=Image.BICUBIC, center=(287 * k, 290 * k), expand=False, fillcolor='white')
r.save(f'{OUT}/rot04.jpg', quality=80)
# A (tightened): pile without bag corners
cx, cy, w = 452 * (f07.width / 667), 306 * (f07.width / 667), 166 * (f07.width / 667)
fit(f07, (int(cx - w / 2), int(cy - w * 1.25 / 2), int(cx + w / 2), int(cy + w * 1.25 / 2))).save(f'{OUT}/bg_pile.jpg', quality=93)
# B: backs wall from the straightened tray (backs block x 362-3001, y 925-2581 measured)
fit(r, (1100, 1080, 1100 + 1072, 1080 + 1340)).save(f'{OUT}/bg_wall.jpg', quality=93)
# C: backs over faces, like the FYM split turned on its side (img 5, both trays straight-on)
i05 = Image.open(f'{S}/i05.jpg')
c = Image.new('RGB', (W, H))
backs = i05.crop((486, 0, 1820, 737)).resize((W, 597), Image.LANCZOS)
faces = i05.crop((0, 1243, 1605, 2361)); faces = faces.resize((W, int(faces.height * W / faces.width)), Image.LANCZOS)
c.paste(faces, (0, H - faces.height)); c.paste(backs, (0, 0))
c.save(f'{OUT}/bg_split.jpg', quality=93)
