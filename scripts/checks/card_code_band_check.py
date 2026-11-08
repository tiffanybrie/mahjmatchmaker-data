"""Code band gate for album match cards (Tiffany Nov 8 10:11am, HARD RULE, docs/ANSWERS.md):
never put "NOT A PARTNER : NO CODE" / "NO CODE AT THIS TIME" (or any no-code band) on a match card when ANY piece on the card
(tiles, mat or a rack) is a partner brand. The band "SAVE WITH CODE : MAHJMATCH" (or "10% OFF  USE CODE : MAHJMATCH") is always
there; "no code" notes belong in captions only.

Used two ways:
- gen2.py imports check_cards() and refuses to render a spec that breaks the rule (every album card build goes through gen2.py).
- CLI: python3 scripts/checks/card_code_band_check.py [spec.json|manifest.json ...]
  With no args it scans scripts/albumcard/specs/*.json and assets/cards/*/manifest.json. Prints PASS or the bad cards; exit 1 on FAIL.
Partners = config/code-truth.json 'pct' + builder/fym_flags/nonpartner_allow.json 'partners' (the no-% partners are in there)."""
import json, os, re, sys, glob
R = '/home/claude/mahjmatchmaker-data/'
NOCODE = re.compile(r'NO\s*CODE|NOT\s*A\s*PARTNER', re.I)


def partners():
    p = set(json.load(open(R + 'config/code-truth.json'))['pct'])
    try: p |= set(json.load(open(R + 'builder/fym_flags/nonpartner_allow.json'))['partners'])
    except Exception: pass
    return p


def _brand_of(label, P):
    for b in sorted(P, key=len, reverse=True):
        if label == b or label.startswith(b + ' '): return b
    return None


def partner_pieces(tile_brand=None, mat_brand=None, racks=(), P=None):
    P = P or partners(); hits = []
    if tile_brand and tile_brand in P: hits.append('tiles: ' + tile_brand)
    if mat_brand and mat_brand in P: hits.append('mat: ' + mat_brand)
    for l in racks or ():
        b = _brand_of(l, P)
        if b: hits.append('rack: ' + l)
    return hits


def bad_band(code, tile_brand=None, mat_brand=None, racks=(), P=None):
    """Return a problem string, or None when the band is fine."""
    code = code or ''
    if not NOCODE.search(code) and 'MAHJMATCH' in code.upper(): return None
    hits = partner_pieces(tile_brand, mat_brand, racks, P)
    if NOCODE.search(code) and hits: return f'no-code band "{code}" on a card with a partner piece ({", ".join(hits[:3])})'
    if 'MAHJMATCH' not in code.upper() and hits: return f'band "{code}" has no MAHJMATCH code on a card with a partner piece ({", ".join(hits[:3])})'
    return None


def check_cards(spec):
    """gen2.py spec ({cards:[...], tile_brand?, code?}). Returns a list of problems."""
    P = partners(); bad = []
    for c in spec.get('cards', []):
        code = c.get('code', spec.get('code', '10% OFF  USE CODE : MAHJMATCH'))
        tb = c.get('tile_brand', spec.get('tile_brand', 'Oh My Mahjong'))
        racks = list(c.get('racks', [])) + list(c.get('mat_racks', spec.get('mat_racks', [])) or []) + list(c.get('bb', []))
        why = bad_band(code, tb, c.get('brand') or c.get('mat_brand'), racks, P)
        if why: bad.append(f"{c.get('file') or c.get('slug') or c.get('title')}: {why}")
    return bad


def check_file(path, P=None):
    P = P or partners(); d = json.load(open(path)); bad = []
    if not isinstance(d, dict): return bad
    if 'cards' in d and isinstance(d['cards'], list):  # gen2 spec or album manifest
        tb = d.get('tile_brand')
        for c in d['cards']:
            if not isinstance(c, dict) or 'code' not in c: continue
            racks = list(c.get('racks', []) or []) + list(c.get('mat_racks', []) or [])
            why = bad_band(c['code'], c.get('tile_brand', tb), c.get('brand'), racks, P)
            if why: bad.append(f"{os.path.relpath(path, R)} :: {c.get('file') or c.get('mat') or c.get('title')}: {why}")
    if 'mats' in d and isinstance(d['mats'], list):  # album spec rows (juniper_final_nov07.json, deco specs ...)
        tb = d.get('tile_brand')
        for m in d['mats']:
            if not isinstance(m, dict) or 'code' not in m: continue
            why = bad_band(m['code'], m.get('tile_brand', tb), m.get('brand'), m.get('racks', []), P)
            if why: bad.append(f"{os.path.relpath(path, R)} :: {m.get('name')} ({m.get('brand')}): {why}")
    return bad


def main(paths):
    P = partners()
    if not paths: paths = sorted(glob.glob(R + 'scripts/albumcard/specs/*.json') + glob.glob(R + 'assets/cards/*/manifest.json'))
    bad = []
    for p in paths:
        try: bad += check_file(p, P)
        except (ValueError, OSError): continue
    if bad:
        print('FAIL card_code_band_check:', len(bad), 'card(s) with a no-code band and a partner piece')
        for b in bad: print('  ' + b)
        return 1
    print('PASS card_code_band_check:', len(paths), 'files')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
