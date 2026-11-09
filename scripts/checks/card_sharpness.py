"""Card mat sharpness (Tiffany Nov 9 1:39am: the December 1994 + Festive Plaid card on /holiday-mahjong-matches showed a
pixelated, blurry mat; she had flagged blurry Festive Plaid before, Nov 3 reels. "Agents must catch this.")
Two measures, calibrated by looking at every live card (Nov 9 contact sheets, 627 mats):
  upscale(w, h)   source crop -> the 1080x1110 mat area (card2.html #mat, background-size: cover). > MAX_UPSCALE = the source
                  is too small for the crop (Festive Plaid ~5x, the 425-500px PLM holiday photos ~2.3x). gen2.py REFUSES.
  measure(card)   on the rendered card, mat area x20-620 / y150-560 (above the racks, left of the rack chart, clear of the
                  tile box): e1 = pixel-scale detail (|img - blur1|), e2 = mid-scale structure (|blur1 - blur3|),
                  r = e1/e2. A mat with real pattern (e2 >= MIN_STRUCT) and r < MIN_RATIO is soft/pixelated (Festive Plaid
                  r .09, Polo Club .13, Candy Cane Lane .19; sharp cards .25-.9). Solid and very soft-art mats (e2 < MIN_STRUCT)
                  are not judged by r. gen2.py REFUSES (deletes the card) on a fail.
                  TIGHTENED Nov 9 (QA of /holiday-mahjong-matches): soft PLM plaid cards from the ~500px photo sat just above
                  0.2 (Peace Love Holiday r .203, Sugarplum Plaid .237, Bespoke Holiday Love .233; the 1512px brand photo
                  renders .253-.29). New rule: r < MIN_RATIO (0.21) for any patterned mat, or r < MIN_RATIO_STRONG (0.24) when
                  the mat has strong structure (e2 >= STRONG_STRUCT 5.0: plaids, busy prints, where softness shows most).
                  Calibration (live scan Nov 9, 2178 cards): 3 -> 54 cards / 9 mats, all the same soft photos (PLM Peace Love
                  Holiday + Sugarplum Plaid, Bespoke Holiday Love R&G + Blue, Britt Mills Chinoiserie, B&B Boots & Bubbles
                  Periwinkle + the 3 old ones); flat-vector PLM mats rendered from 1512px (Merry & Striped .223 e2 4.8, Candy
                  Cane Lane .227 e2 1.9) stay PASS. Known blind spot: a JPEG-blocky upscale can read SHARP (Anders Ruff Candy
                  Cane Lane zoomed card r .40, fixed by eye Nov 9): the source-size gate (MAX_UPSCALE) in gen2.py is the guard.
Exceptions only with a reason in config/card-sharpness-ok.json {"<card file name>": "why (e.g. no larger photo exists, checked <date>)"}.
CLI: scripts/checks/card_sharpness_check.py scans the live album + holiday pages."""
import os, json
import numpy as np
from PIL import Image, ImageFilter
R = '/home/claude/mahjmatchmaker-data/'
MAX_UPSCALE = 2.0
MIN_STRUCT = 0.6
MIN_RATIO = 0.21
MIN_RATIO_STRONG = 0.24
STRONG_STRUCT = 5.0
BOX = (20, 150, 620, 560)
def upscale(w, h): return max(1080 / w, 1110 / h)
def measure(im):
    g = im.convert('L')
    if g.size != (1080, 1350): g = g.resize((1080, 1350), Image.LANCZOS)
    g = g.crop(BOX); a = np.asarray(g, dtype=np.float32)
    b1 = np.asarray(g.filter(ImageFilter.GaussianBlur(1)), dtype=np.float32)
    b3 = np.asarray(g.filter(ImageFilter.GaussianBlur(3)), dtype=np.float32)
    e1 = float(np.abs(a - b1).mean()); e2 = float(np.abs(b1 - b3).mean())
    return {'e1': round(e1, 3), 'e2': round(e2, 3), 'r': round(e1 / (e2 + 1e-6), 3)}
def blurry(m): return (m['e2'] >= MIN_STRUCT and m['r'] < MIN_RATIO) or (m['e2'] >= STRONG_STRUCT and m['r'] < MIN_RATIO_STRONG)
def ok_list():
    p = R + 'config/card-sharpness-ok.json'
    return json.load(open(p)).get('ok', {}) if os.path.exists(p) else {}
