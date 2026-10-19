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


def _tile_rec(name_or_key):
    import re
    p = os.path.join(R, 'config/tile-tones.json')
    if not os.path.exists(p): return {}
    T = json.load(open(p)).get('sets', {})
    k = re.sub(r'[^a-z0-9]', '', str(name_or_key).lower().replace('(retired)', '').replace('\u00e9', 'e').replace('é', 'e'))
    return T.get(k) or {}


def tile_colors(name_or_key):
    """The tile set's BACK color families (Tiffany, Oct 19 3:11am: the back rules). These alone qualify mats and set the
    tone gate. Juxtaposed layers (Dandy's olive, La Fete's olive + teal) never qualify or change the gate."""
    r = _tile_rec(name_or_key)
    return r.get('back_colors') or r.get('colors') or ([r['dominant']] if r.get('dominant') else [])


def tile_profile(name_or_key):
    """-> dict(back, layers, faces, light, chroma) for ranking."""
    r = _tile_rec(name_or_key)
    return dict(back=tile_colors(name_or_key), layers=r.get('layer_colors') or [], faces=r.get('face_colors') or [],
                light=r.get('light'), chroma=r.get('chroma'), pastel=bool(r.get('pastel_family')),
                back_hex=r.get('back_hex'), layer_hex=r.get('layer_hex') or [], signature=r.get('signature') or [])


_COLORFAM = {'pink', 'red', 'orange', 'yellow', 'gold', 'green', 'teal', 'blue', 'purple', 'brown'}


def multi_count(key, sep=15):
    """How many different real colors (>= 11% each, CIEDE2000 > `sep` apart, chroma >= 15) the mat's pattern shows."""
    pal = (palettes().get(key) or {}).get('pal') or []
    if not pal: return 0
    P = _pal_mod(); import numpy as np
    big = []
    for h, w in pal:
        L = P.lab(h)
        if w >= 0.11 and float(np.hypot(L[1], L[2])) >= 15 and all(P.dE(h, b) > sep for b in big): big.append(h)
    return len(big)


def is_multi(r, key=None):
    """Multicolor (doc 76): tagged 'multi' by her or the photo read, OR the measured palette shows 3+ clearly different real
    colors (each >= 12% of the pattern, CIEDE2000 > 20 apart, none over 45%), like a watercolor floral or Spring Fling.
    Accent tags alone don't make a mat multicolor (most mats carry 2-3 accent tags)."""
    if not r: return False
    if r.get('primary') == 'multi': return True
    if r.get('src') == 'tiffany': return False
    k = key or r.get('_key')
    pal = (palettes().get(k) or {}).get('pal') if k else None
    if not pal: return False
    P = _pal_mod(); import numpy as np
    big = []
    for h, w in pal:
        L = P.lab(h); ch = float(np.hypot(L[1], L[2]))
        if w >= 0.12 and ch >= 15 and all(P.dE(h, b) > 20 for b in big): big.append(h)
    return len(big) >= 3 and max(w for _, w in pal) < 0.45


def pull_score(key, set_colors, set_tone=None, past_yes=False, profile=None):
    """How well a mat fits a tile set (doc 76; tight 3:03am + back/layers/faces 3:11am).
    QUALIFY: 1) tone gate (clean tile -> clean/pastel/blend; earthy -> earthy/blend; transitional -> any tone, never any
    color); 2) the mat's PRIMARY is one of the set's BACK colors (set_colors), or a clean/bright MULTICOLOR mat for a clean
    or transitional tile (Spring Fling rule: lots of bright/pastel colors -> match on brightness), or a Blend/multicolor mat
    whose accents hold a back color. Accents alone never qualify.
    RANK (coordination: the more of the tile the mat echoes, the better): back match (dominant > other back color >
    multicolor/blend) + layer-color bonus + face-color bonus + brightness similarity (same brightness level ranks higher:
    Greenly + Papaya) + small accent echo. Returns 0 (leave out) or a positive score."""
    r = get(key)
    if not r or r.get('skip') or r.get('holiday') or not set_colors: return 0  # no holiday mats in regular books (doc 36)
    tt = OLD_TILE_TONE.get(set_tone, set_tone) if set_tone else None
    t = 1.0
    if tt in TONE_FIT and r.get('tone'):
        t = TONE_FIT[tt].get(r['tone'], 1.0)
        if t == 0: return 0
    prim, sec = r['primary'], r.get('secondary', [])
    multi = is_multi(r, key)
    if prim in set_colors:
        s = 2.0 if prim == set_colors[0] else 1.5
    elif multi and (profile or {}).get('pastel') and r.get('tone') in ('pastel', 'bright'):
        # Pastel family (doc 76, 3:15am): pastel multis work on lightness alone, the "Easter egg" effect (Sorbet's butter back
        # is rare in mats, but her mint layers and pastel faces blend her in). Pastel multis rank above bright multis.
        s = (1.7 if r.get('tone') == 'pastel' else 1.2) + (0.2 if any(c in sec for c in set_colors) else 0)
    elif multi and r.get('tone') in ('bright', 'pastel') and tt in ('clean', 'transitional'):
        # Spring Fling rule (doc 76): a mat with MANY bright/pastel colors takes nearly any clean tile; match on brightness.
        # 4+ distinct real colors that include the back's family rank with the best solid matches.
        full = multi_count(key) >= 4
        s = (2.3 if full else 1.9) if any(c in sec for c in set_colors) else (1.6 if full else 1.3)
    elif (r.get('tone') == 'blend' or prim == 'multi') and any(c in sec for c in set_colors):
        s = 1.1
    else:
        return 0
    pr = profile or {}
    mat_cols = set([prim] + list(sec))
    s += 0.35 * len(mat_cols & set(pr.get('layers') or []))
    s += 0.25 * len(mat_cols & set(pr.get('faces') or []))
    if pr.get('light') is not None and r.get('light') is not None:
        d = abs(pr['light'] - r['light']) + 0.5 * abs((pr.get('chroma') or 0) - (r.get('chroma') or 0))
        s += max(0.0, 0.6 - 1.5 * d)
    s += 0.15 * sum(1 for c in sec if c in set_colors and c != prim)
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

_PAL = None


def palettes():
    """config/mat-palettes.json: measured pattern-area colors per mat key ([hex, weight]); doc 77."""
    global _PAL
    if _PAL is None:
        p = os.path.join(R, 'config/mat-palettes.json'); _PAL = json.load(open(p)).get('mats', {}) if os.path.exists(p) else {}
    return _PAL


def _pal_mod():
    try:
        import palette as P
    except ImportError:
        import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import palette as P
    return P


def exact_bonus(key, prof):
    """Coordination by EXACT measured shade (doc 77): back shade present in the mat (+), layer shades present (+).
    dE < 10 = the same shade, < 18 = close; anything farther earns nothing (a yellower olive is not a deeper olive)."""
    P = _pal_mod(); pal = (palettes().get(key) or {}).get('pal') or []
    if not pal: return 0.0
    b = 0.0
    if prof.get('back_hex'):
        d = P.nearest(prof['back_hex'], pal); b += 0.5 if d < 10 else (0.25 if d < 18 else 0)
    for h in prof.get('layer_hex') or []:
        d = P.nearest(h, pal); b += 0.3 if d < 10 else (0.15 if d < 18 else 0)
    return b


def pull(set_name, keys, limit=60, past_yes=(), fill_min=30):
    """Ranked color pull for a tile set's swipe book (doc 76 + 77), best first, capped at `limit` (doc 51: 40-60 mats).
    QUALIFY (pull_score): tone gate from the BACK + mat primary in the back colors, OR a same-tone multicolor mat (pastel multis for
    the pastel family, bright multis for clean sets), OR a Blend mat holding the back colors. Juxtaposed layers never qualify.
    RANK: back match > layer/face coordination > brightness/pastel similarity > accents, plus exact-shade coordination.
    FALLBACK (doc 76): if fewer than `fill_min` qualify, fill with same-tone multicolor mats (pastel or bright for clean sets,
    muted for earthy sets).
    keys = match-pool mat keys only (brand gates and her skip list already applied). past_yes = small boost only."""
    tone, _ = tile_tone(set_name); cols = tile_colors(set_name); prof = tile_profile(set_name)
    py = set(past_yes)
    sc = []
    for k in keys:
        s = pull_score(k, cols, tone, k in py, prof)
        if s > 0: s += exact_bonus(k, prof)
        sc.append((s, k))
    got = [k for s, k in sorted([x for x in sc if x[0] > 0], key=lambda x: -x[0])]
    if len(got) < fill_min:
        tt = OLD_TILE_TONE.get(tone, tone)
        ok = {'clean': ('pastel', 'bright'), 'earthy': ('muted', 'blend'), 'transitional': ('bright', 'pastel', 'blend', 'muted')}.get(tt, ())
        extra = []
        for k in keys:
            r = get(k)
            if k in got or not r or r.get('skip') or r.get('holiday') or not is_multi(r, k) or r.get('tone') not in ok: continue
            extra.append((0.5 + exact_bonus(k, prof), k))
        got += [k for s, k in sorted(extra, key=lambda x: -x[0])][:fill_min - len(got)]
    return got[:limit]


def layer_picks(set_name, keys, exclude=(), n=8, max_dE=14):
    """Hand-pick-style extras for a juxtaposed layer (doc 76/77): up to `n` mats whose palette holds a color closest to the layer's
    EXACT measured shade (CIEDE2000 <= max_dE), never every mat with the same color word. Dandy's olive layer -> a few olive mats.
    Tone still matters loosely: a solid clean tile never gets a solid earthy mat... except here, where the layer IS earthy; the
    swipe book labels these 'for her <shade> layer' at the end."""
    P = _pal_mod(); prof = tile_profile(set_name); ex = set(exclude); out = []
    for h in prof.get('layer_hex') or []:
        cand = []
        for k in keys:
            if k in ex: continue
            r = get(k)
            if not r or r.get('skip'): continue
            pal = (palettes().get(k) or {}).get('pal') or []
            d = P.nearest(h, pal)
            if d <= max_dE: cand.append((d, k))
        for d, k in sorted(cand)[:n]:
            out.append({'key': k, 'layer_hex': h, 'dE': round(d, 1)}); ex.add(k)
    return out[:n]


def suggest_sets(mat_key, top=8, max_dE=14):
    """New mat in -> which tile sets' SIGNATURE colorway (2-3 measured shades, e.g. Lagoon teal-blue + berry) shows up in it.
    A set needs its back shade AND at least one more signature shade present; the tone gate still applies. -> [(set, score)]."""
    P = _pal_mod(); pal = (palettes().get(mat_key) or {}).get('pal') or []
    r = get(mat_key)
    if not pal or not r: return []
    p = os.path.join(R, 'config/tile-tones.json'); T = json.load(open(p)).get('sets', {})
    out = []
    for k, t in T.items():
        sig = t.get('signature') or []
        if len(sig) < 2: continue
        tt = OLD_TILE_TONE.get(t.get('tone'), t.get('tone'))
        if tt in TONE_FIT and TONE_FIT[tt].get(r.get('tone'), 1.0) == 0: continue
        ds = [P.nearest(h, pal) for h in sig]
        if ds[0] > max_dE or sum(1 for d in ds[1:] if d <= max_dE) < 1: continue
        out.append((t.get('name', k), round(sum(max(0, max_dE - d) for d in ds), 1)))
    return sorted(out, key=lambda x: -x[1])[:top]
