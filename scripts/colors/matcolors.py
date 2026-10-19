"""One place to read a mat's colors (Tiffany's color model, Oct 19, 2026).

Order of truth for every mat (catalog key, e.g. "www.ohmymahjong.com/larkspur-mat-in-tube"):
  1. config/mat-color-overrides.json  -> Tiffany's taps in the Mat Color Tagger (always wins)
  2. config/mat-color-guesses.json    -> the computer's photo read (scripts/colors/families.py)
Each record: {primary, secondary:[], tone, holiday, skip}.

Readers:
  - Swipe-book color pulls: pull_score() (primary weighted 2x over accents, tone must match: clean/bright and
    muted/earthy are never mixed; pastel sits between them). Skipped mats are never pulled.
  - FYM catalog build (builder/fym_build.py): fym_families() -> the FYM filter families (primary first).
  - Gallery and color pages group by PRIMARY only.
  - Mat Edit cards (scripts/matcard): the mat's own palette stays the photo swatches; order_palette() puts the primary's
    swatch first so the card leads with the color she named.
"""
import json, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
_O = _G = None
FYM_MAP = {'teal': 'blue', 'gold': 'yellow', 'brown': 'orange', 'bw': 'neutral'}  # FYM filter chips predate the new codes
TONE_NEAR = {('bright', 'pastel'): 0.5, ('pastel', 'bright'): 0.5, ('muted', 'pastel'): 0.4, ('pastel', 'muted'): 0.4}


def _load():
    global _O, _G
    if _O is None:
        p = os.path.join(R, 'config/mat-color-overrides.json'); _O = json.load(open(p)).get('mats', {}) if os.path.exists(p) else {}
        g = os.path.join(R, 'config/mat-color-guesses.json'); _G = json.load(open(g)).get('mats', {}) if os.path.exists(g) else {}
    return _O, _G


def get(key):
    """-> record dict with 'src' ('tiffany'|'computer') or None."""
    o, g = _load()
    if key in o: return dict(o[key], src='tiffany')
    if key in g: return dict(g[key], src='computer')
    return None


def fym_families(key, fallback=None):
    r = get(key)
    if not r: return fallback
    fams = [] if r['primary'] == 'multi' else [r['primary']]
    fams += [c for c in r.get('secondary', []) if c not in fams]
    out = []
    for c in fams:
        c = FYM_MAP.get(c, c)
        if c in ('multi', 'dark') and c == 'multi': continue
        if c not in out: out.append(c)
    return out[:3] or fallback


def pull_score(key, set_colors, set_tone=None):
    """How well a mat fits a tile set for a swipe-book color pull.
    set_colors: the set's accent colors (back + layers, never the white face), new codes, most important first.
    Returns 0..~3; 0 = leave it out (skipped, or a clash of tones)."""
    r = get(key)
    if not r or r.get('skip'): return 0
    t = 1.0
    if set_tone and r.get('tone') and r['tone'] != set_tone:
        t = TONE_NEAR.get((r['tone'], set_tone), 0.0)  # bright vs muted -> 0, never mixed
        if t == 0: return 0
    s = 0.0
    for i, c in enumerate(set_colors):
        w = 1.0 / (1 + i)
        if r['primary'] == c: s += 2.0 * w
        elif c in r.get('secondary', []): s += 1.0 * w
    if r['primary'] == 'multi': s += 0.3 * sum(1 for c in set_colors if c in r.get('secondary', []))
    return round(s * t, 3)


def order_palette(key, palette):
    """palette: [[name, hex], ...] from the photo. Moves the swatch closest to the primary family first."""
    r = get(key)
    if not r: return palette
    try:
        import families as F
    except ImportError:
        import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import families as F
    import numpy as np
    def fam(h):
        rgb = np.array([[int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]]); return str(F.fam_arr(rgb)[0][0])
    hit = [p for p in palette if fam(p[1]) == r['primary']]
    return hit[:1] + [p for p in palette if p not in hit[:1]] if hit else palette
