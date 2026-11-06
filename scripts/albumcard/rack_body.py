"""Rack BODY extent in a card rack PNG (Nov 6, true relative rack size): the trough's bottom edge runs along the
image bottom, the pusher foot/arm does not. Returns (x0, x1) as fractions of the image width: the columns whose
lowest opaque pixel sits in the bottom 12% of the image. Checked by eye on OMM Hot Pink, Agate, Pink Quartz,
White Acrylic and PLM Pink (yellow-line sheet, Nov 6)."""
import numpy as np
from PIL import Image
def body(im):
    a = np.asarray(im.convert('RGBA'))[..., 3] > 100; H, W = a.shape
    has = a.any(0); low = np.where(has, H - 1 - np.argmax(a[::-1], 0), -1)
    ok = np.nonzero(low >= H * .88)[0]
    if not len(ok): return 0.0, 1.0
    return ok.min() / W, (ok.max() + 1) / W
