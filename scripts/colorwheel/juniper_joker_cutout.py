"""Nov 6 (Tiffany, Juniper round-3 note 9): keep the layer arrows on the Her colors slide, but on the JOKER tile photo
(ohmymahjong.com/cdn/shop/files/juniper-mahjong-tiles-9588574.jpg, saved as
assets/launches/omm-juniper-mahjong-tiles/11-juniper-joker-ohmymahjong-cdn.jpg). rembg cut, holes filled (white tile on white),
trimmed -> assets/tiles/backs/juniper-layers-joker-cutout.png. Prints the layer centres sampled down the tile's front edge."""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
from rembg import new_session, remove
R = '/home/claude/mahjmatchmaker-data/'
src = Image.open(R + 'assets/launches/omm-juniper-mahjong-tiles/11-juniper-joker-ohmymahjong-cdn.jpg').convert('RGB')
im = remove(src, session=new_session('isnet-general-use')).convert('RGBA')
a = np.asarray(im)[..., 3] > 60
lab, n = ndi.label(a); sz = ndi.sum(a, lab, range(1, n + 1)); a = lab == (1 + int(np.argmax(sz)))
a = ndi.binary_fill_holes(ndi.binary_closing(a, np.ones((5, 5)), 2))
out = src.convert('RGBA'); out.putalpha(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1)))
out = out.crop(out.getbbox()); out.save(R + 'assets/tiles/backs/juniper-layers-joker-cutout.png', optimize=True)
print(out.size)
