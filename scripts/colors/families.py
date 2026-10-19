"""Mat color model (Tiffany, Oct 19, 2026).
Each mat: ONE primary color (what you'd name at first glance) + 0-3 secondary accents + a TONE + a holiday flag.
Primaries: pink red orange yellow gold green teal blue purple brown neutral bw dark multi.
Tones: bright (clean/bright), muted (muted/earthy), pastel. Clean bright and muted earthy colors must never be mixed in matching.
The computer's read comes from the mat photo itself: the pattern/border counts fully; a plain or dotted center panel counts
very little (Hamptons Hydrangea's peach dotted center must not make it an orange mat)."""
import numpy as np
from PIL import Image

CODES = ['pink', 'red', 'orange', 'yellow', 'gold', 'green', 'teal', 'blue', 'purple', 'brown', 'neutral', 'bw', 'dark', 'multi']
LABEL = {'pink': 'Pink', 'red': 'Red', 'orange': 'Orange', 'yellow': 'Yellow', 'gold': 'Gold/Mustard', 'green': 'Green',
         'teal': 'Teal/Aqua', 'blue': 'Blue', 'purple': 'Purple', 'brown': 'Brown & Tan', 'neutral': 'Neutral & Ivory',
         'bw': 'Black & White', 'dark': 'Dark & Moody', 'multi': 'Multicolor'}
TONES = ['bright', 'muted', 'pastel']
TONE_LABEL = {'bright': 'Clean/Bright', 'muted': 'Muted/Earthy', 'pastel': 'Pastel'}
COLORFAM = set(CODES) - {'neutral', 'bw', 'dark', 'multi'}


def _hls(rgb):
    mx = rgb.max(-1); mn = rgb.min(-1); l = (mx + mn) / 2; d = mx - mn
    s = np.where(d == 0, 0, d / np.where(l < 0.5, mx + mn + 1e-9, 2 - mx - mn + 1e-9))
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    dd = np.where(d == 0, 1, d)
    h = np.zeros_like(l)
    h = np.where(mx == r, ((g - b) / dd) % 6, h); h = np.where(mx == g, (b - r) / dd + 2, h); h = np.where(mx == b, (r - g) / dd + 4, h)
    return h * 60, l, s


def fam_arr(rgb):
    """rgb float array (...,3) in 0-1 -> family array (white/black/neutral are split out for the primary logic)."""
    h, l, s = _hls(rgb)
    out = np.full(l.shape, 'neutral', dtype=object)
    low = (s < 0.14) | ((l > 0.86) & (s < 0.45))
    out[low & (l > 0.72)] = 'white'; out[low & (l < 0.3)] = 'black'
    col = ~low
    dk = col & ((l < 0.17) | ((l < 0.26) & (s < 0.35)))
    out[dk] = 'dark'
    br = col & ~dk & (h >= 12) & (h < 48) & ((l < 0.42) | ((s < 0.58) & (l < 0.74)))
    out[br] = 'brown'
    rest = col & ~dk & ~br

    def put(m, v): out[rest & m] = v
    put(((h < 10) | (h >= 345)) & (l > 0.68), 'pink'); put(((h < 10) | (h >= 345)) & (l <= 0.68), 'red')
    put((h >= 10) & (h < 22) & (l > 0.76), 'pink')
    put((h >= 10) & (h < 40) & ~((h < 22) & (l > 0.76)), 'orange')
    put((h >= 40) & (h < 52) & (l < 0.58) & (s < 0.78), 'gold')
    put((h >= 40) & (h < 52) & ~((l < 0.58) & (s < 0.78)), 'yellow')
    put((h >= 52) & (h < 70), 'yellow'); put((h >= 70) & (h < 172), 'green')
    put((h >= 172) & (h < 192) & (s > 0.3), 'teal'); put((h >= 172) & (h < 192) & (s <= 0.3), 'blue')
    put((h >= 192) & (h < 255), 'blue'); put((h >= 255) & (h < 290), 'purple')
    put((h >= 290) & (h < 345) & (l > 0.45), 'pink'); put((h >= 290) & (h < 345) & (l <= 0.45), 'purple')
    return out, h, l, s


def read_image(path, N=96):
    """-> (family weights, tone guess, downweighted center family or None)"""
    a = np.asarray(Image.open(path).convert('RGB').resize((N, N))).astype(float) / 255
    f, h, l, s = fam_arr(a)
    w = np.ones((N, N))
    c0, c1 = int(N * .25), int(N * .75)
    cen = (slice(c0, c1), slice(c0, c1))
    uniform = a[cen].reshape(-1, 3).std(0).mean() < 0.07
    w[cen] = 0.1 if uniform else 0.45
    cf = f[cen].ravel(); vals, cnt = np.unique(cf, return_counts=True)
    ctop = str(vals[cnt.argmax()]); cshare = cnt.max() / cf.size
    panel = None
    if cshare > 0.55:  # big solid or dotted center field
        sub = w[cen]; sub[f[cen] == ctop] = 0.08; w[cen] = sub; panel = ctop
    fw = {}
    for k in np.unique(f): fw[str(k)] = float(w[f == k].sum())
    t = sum(fw.values()) or 1; fw = {k: v / t for k, v in fw.items()}
    # tone: weighted saturation/lightness over colored pixels
    colm = np.isin(f, list(COLORFAM))
    if colm.sum() > 30:
        ww = w[colm]; S = float((s[colm] * ww).sum() / ww.sum()); L = float((l[colm] * ww).sum() / ww.sum())
        brownish = fw.get('brown', 0) + fw.get('gold', 0)
        if L > 0.7 and S < 0.75: tone = 'pastel'
        elif S >= 0.5 and brownish < 0.25 and L >= 0.3: tone = 'bright'
        else: tone = 'muted'
    else:
        tone = 'muted'
    return fw, tone, panel


def guess_from_weights(w, panel=None):
    w = dict(w)
    white = w.pop('white', 0); black = w.pop('black', 0); neu = w.pop('neutral', 0)
    col = sorted(w.items(), key=lambda x: -x[1]); colored = sum(v for _, v in col)
    if white >= 0.28 and black >= 0.18 and colored < 0.35: prim = 'bw'
    elif white + neu + black >= 0.66 or not col: prim = 'dark' if black > white + neu else 'neutral'
    else:
        big = [k for k, v in col if v >= 0.12]
        prim = 'multi' if (len(big) >= 4 and col[0][1] < 0.28) else col[0][0]
    sec = [k for k, v in col if v >= 0.07 and k != prim][:3]
    if panel and panel in COLORFAM and panel != prim and panel not in sec: sec.insert(0, panel)
    if prim not in ('neutral', 'bw') and white + neu >= 0.25 and len(sec) < 3: sec.append('neutral')
    if prim != 'dark' and black >= 0.2 and len(sec) < 3: sec.append('dark')
    vals = sorted([v for _, v in col] + [white + neu], reverse=True)
    amb = 1 - (vals[0] - vals[1]) if len(vals) > 1 else 0
    return prim, sec[:3], round(amb, 3)


def guess_img(path):
    """-> (primary, secondary[], tone, ambiguity)"""
    w, tone, panel = read_image(path)
    p, s, a = guess_from_weights(w, panel)
    if p in ('neutral', 'bw') and tone == 'bright': tone = 'muted'
    return p, s, tone, a


def from_mf(mf):
    """Old catalog color families -> new codes (orange stays orange now)."""
    return list(mf or [])
