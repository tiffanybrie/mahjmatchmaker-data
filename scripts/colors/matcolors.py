"""One place to read a mat's colors (Tiffany's color model, Oct 19, 2026).

Order of truth for every mat (catalog key, e.g. "www.ohmymahjong.com/larkspur-mat-in-tube"):
  1. config/mat-color-overrides.json  -> Tiffany's taps in the Mat Color Tagger (always wins)
  2. config/mat-color-guesses.json    -> the computer's photo read (scripts/colors/families.py)
Each record: {primary, secondary:[], tone (bright|pastel|muted|blend), holiday, skip}.

Readers:
  - Swipe-book color pulls: pull_score() with set_colors=tile_colors(name) (TIGHT, Oct 19 3:03am: mat primary must be one of the
    set's own colors; accents only rank; tile tone gates mat tone per doc 76:
    clean tile -> clean/pastel/blend, earthy tile -> earthy/blend, transitional -> all with blend first; a solid clean
    tile on a solid earthy mat or the reverse scores 0). Skipped mats are never pulled.
  - FYM catalog build (builder/fym_build.py): fym_families() -> the FYM filter families (primary first).
  - Gallery and color pages group by PRIMARY only.
  - Mat Edit cards (scripts/matcard): the mat's own palette stays the photo swatches; order_palette() puts the primary's
    swatch first so the card leads with the color she named.
"""
import json, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
_O = _G = None
FYM_MAP = {'teal': 'blue', 'gold': 'yellow', 'brown': 'orange', 'bw': 'neutral'}  # FYM filter chips predate the new codes


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


# Tiffany's color theory (doc 76): which mat tones each tile tone may be pulled onto, and their weight.
# Clean tile -> clean/bright, pastel, blend. Earthy tile -> earthy, blend. Transitional (berries etc.) -> everything, blend first.
# A solid clean tile on a solid earthy mat (or the reverse) is a hard no (0), never just a lower score.
TONE_FIT = {
    'clean': {'bright': 1.0, 'pastel': 1.0, 'blend': 0.9, 'muted': 0.0},
    'earthy': {'muted': 1.0, 'blend': 0.9, 'bright': 0.0, 'pastel': 0.0},
    'transitional': {'blend': 1.2, 'bright': 1.0, 'pastel': 1.0, 'muted': 1.0},
}
OLD_TILE_TONE = {'bright': 'clean', 'pastel': 'clean', 'muted': 'earthy'}  # older callers passed mat-style tones


def tile_tone(name_or_key):
    """Tile set tone from config/tile-tones.json (her corrections win via the tagger export). -> (tone, dominant) or (None, None)."""
    import re
    p = os.path.join(R, 'config/tile-tones.json')
    if not os.path.exists(p): return None, None
    T = json.load(open(p)).get('sets', {})
    k = re.sub(r'[^a-z0-9]', '', str(name_or_key).lower().replace('(retired)', '').replace('\u00e9', 'e').replace('é', 'e'))
    r = T.get(k)
    return (r.get('tone'), r.get('dominant')) if r else (None, None)


def tile_colors(name_or_key):
    """The tile set's OWN color families for pulls (config/tile-tones.json 'colors'): the dominant color first, plus its
    analogous neighbor only when the set really is an in-between (e.g. Lagoon blue-green -> blue, teal, green)."""
    import re
    p = os.path.join(R, 'config/tile-tones.json')
    if not os.path.exists(p): return []
    T = json.load(open(p)).get('sets', {})
    k = re.sub(r'[^a-z0-9]', '', str(name_or_key).lower().replace('(retired)', '').replace('\u00e9', 'e').replace('é', 'e'))
    r = T.get(k) or {}
    return r.get('colors') or ([r['dominant']] if r.get('dominant') else [])


def pull_score(key, set_colors, set_tone=None, past_yes=False):
    """How well a mat fits a tile set for a swipe-book color pull. Tight rule (Tiffany, Oct 19 3:03am; doc 76):
    1. TONE gate: clean tile -> clean/pastel/blend mats; earthy tile -> earthy/blend; transitional -> any tone (blend first).
       Transitional relaxes ONLY the tone gate, never the color gate.
    2. COLOR gate: the mat's PRIMARY color must be one of the set's own colors (set_colors = tile_colors(name): dominant
       first, plus its analogous neighbor only for true in-betweens). A blend or multicolor mat qualifies only if one of the
       set's colors is among its accents in real amounts. Accents never qualify a mat on their own.
    3. Ranking among qualified mats: dominant-color primary > neighbor primary; accents that echo the set's colors add a
       little; her past yes for a same-color, similar-tone set adds a small boost (past_yes). What earlier swipe books merely
       SHOWED is never a signal.
    Returns 0 (leave it out) or a positive score."""
    r = get(key)
    if not r or r.get('skip') or not set_colors: return 0
    t = 1.0
    if set_tone:
        tt = OLD_TILE_TONE.get(set_tone, set_tone)
        if tt in TONE_FIT and r.get('tone'):
            t = TONE_FIT[tt].get(r['tone'], 1.0)
            if t == 0: return 0
    prim, sec = r['primary'], r.get('secondary', [])
    if prim in set_colors:
        s = 2.0 if prim == set_colors[0] else 1.4
    elif (r.get('tone') == 'blend' or prim == 'multi') and any(c in sec for c in set_colors):
        s = 1.0
    else:
        return 0
    s += 0.25 * sum(1 for c in sec if c in set_colors and c != prim)
    if past_yes: s += 0.3
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

def pull(set_name, keys, limit=60, past_yes=()):
    """Ranked color pull for a tile set's swipe book: tone gate + color gate (pull_score), best first, capped at `limit`
    (doc 51: 40-60 mats). keys = match-pool mat keys only (brand gates and her skip list already applied).
    past_yes = mat keys she said yes to for same-color, similar-tone sets (small boost only)."""
    tone, _ = tile_tone(set_name); cols = tile_colors(set_name)
    py = set(past_yes)
    sc = [(pull_score(k, cols, tone, k in py), k) for k in keys]
    return [k for s, k in sorted([x for x in sc if x[0] > 0], key=lambda x: -x[0])][:limit]
