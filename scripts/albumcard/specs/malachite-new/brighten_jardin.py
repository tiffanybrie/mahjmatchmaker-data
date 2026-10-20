"""Brighten the muted Jardin needlepoint canvas photo: neutralise the blue-grey cast using the light
canvas background, stretch levels, lift saturation. Usage: brighten.py in out"""
import sys, numpy as np
from PIL import Image, ImageEnhance
im = Image.open(sys.argv[1]).convert('RGB'); a = np.asarray(im).astype(np.float32)
mx = a.max(2); mn = a.min(2)
bg = (mx > np.percentile(mx, 70)) & ((mx - mn) < 25)       # light, low-chroma canvas pixels
ref = a[bg].mean(0); target = np.array([246., 243., 236.])  # warm white like the printed mat
a = a * (target / ref)
lo = np.percentile(a, 1.0); hi = 255.
a = np.clip((a - lo) / (hi - lo) * 255, 0, 255)
a = 255 * (a / 255) ** 1.08                                   # keep mids from washing out
out = Image.fromarray(a.astype(np.uint8))
out = ImageEnhance.Color(out).enhance(1.25); out = ImageEnhance.Contrast(out).enhance(1.08)
out.save(sys.argv[2], quality=94) if sys.argv[2].endswith('jpg') else out.save(sys.argv[2], quality=92)
print('bg ref', ref.round(1))
