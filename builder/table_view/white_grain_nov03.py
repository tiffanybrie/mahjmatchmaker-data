"""QA r9 (Nov 3): Bird & Bamboo White Wood Stain's real-grain band (from B&B's own WOOD STAINS photo) is so pale that on a phone it
reads as a painted white rack. A white stain is a thin whitewash over real grain, so lift ONLY the photo's own fine grain (local
contrast: + 1.8 x (image - its 3px blur)), same colour, same outline; nothing painted on. Run once on the asset (idempotent via the
audit 'grain_lift' note). Usage: python3 white_grain_nov03.py"""
import json, numpy as np
from pathlib import Path
from PIL import Image, ImageFilter
R0 = Path(__file__).resolve().parents[2]; AUD = R0 / 'config/tableview-rack-audit-nov02.json'; aud = json.load(open(AUD))
k = 'bb:White Wood Stain'; f = R0 / aud['fixed'][k]['file']
if 'grain_lift' in aud['fixed'][k]: print('already'); raise SystemExit
im = Image.open(f).convert('RGBA'); a = np.asarray(im).astype(float); bl = np.asarray(im.filter(ImageFilter.GaussianBlur(3))).astype(float)
o = a.copy(); o[..., :3] = np.clip(a[..., :3] + 1.8 * (a[..., :3] - bl[..., :3]), 0, 255)
Image.fromarray(o.astype(np.uint8), 'RGBA').save(f, 'WEBP', quality=92, method=6)
aud['fixed'][k]['grain_lift'] = 'Nov 3 QA r9: the real grain lifted 1.8x (local contrast only) so the whitewash reads as wood, not paint'
json.dump(aud, open(AUD, 'w'), indent=1); print('ok', f)
