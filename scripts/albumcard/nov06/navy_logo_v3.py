"""Nov 6 (Tiffany, Juniper round-3 note 13: "wrong Mahj Matchmaker logo used multiple times"): the navy logo box on album
match cards (assets/brand/card_navy_logo_v2.png) carries the OLD wordmark (flame on the j, no heart). The current logo
(brand guide 'Logo use': assets/brand/mahjmatchmaker-wordmark-notag.png, the flame-heart j) is used everywhere else
(covers, profile, carousel, colour wheel). This builds the same navy box with the current wordmark in white, pink heart kept,
and the same 'MATCHING MAHJONG TILES, MATS & RACKS' line lifted from v2 -> assets/brand/card_navy_logo_v3.png."""
import numpy as np
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
old = Image.open(R + 'assets/brand/card_navy_logo_v2.png').convert('RGB'); a = np.asarray(old)
NAVY = tuple(int(v) for v in a[10, 10]); W, H = old.size
wm = (a[:150].sum(2) > 600); ys, xs = np.nonzero(wm); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
out = Image.new('RGB', (W, H), NAVY)
out.paste(old.crop((0, 170, W, H)), (0, 170))                         # tagline, untouched
logo = Image.open(R + 'scripts/covers/holiday/ourlogo.png').convert('RGBA')  # current wordmark, light version (pink heart)
L = np.asarray(logo).astype(int).copy(); light = (L[..., :3].min(2) > 200)
L[light, 0:3] = 255                                                     # cream -> white, heart stays pink
logo = Image.fromarray(L.astype(np.uint8), 'RGBA'); logo = logo.crop(logo.getbbox())
w = int((x1 - x0) * 1.04); h = round(logo.height * w / logo.width); logo = logo.resize((w, h), Image.LANCZOS)
out.paste(logo, ((W - w) // 2, y1 - h + 6), logo)
out.save(R + 'assets/brand/card_navy_logo_v3.png'); print(out.size, NAVY, (w, h))
