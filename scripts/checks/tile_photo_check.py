"""Tile photo approval gate (Album Playbook step 0, Tiffany Nov 8 1:37pm): before ANY album card is built, she approves the
set's tile pile / matching shot in chat.

Record: config/album-records/<set>.json "tile_photo": {file, inset, source, asked_at, approved_at|null}
  file = the tile photo shown on the review page (the FYM photo), inset = the shot on the cards (what she approves),
  source = listing image + variant_ids, asked_at = when Claude sent it to her, approved_at = her yes (null until then).
Live albums (docs/status/live-albums.json) are exempt: their photo went live with her yes.

Used by:
- scripts/albumcard/gen2.py: missing_for_outdir(outdir) -> REFUSES to render album cards for a set whose photo is not approved.
- scripts/checks/album_gate.py: step [0].
- scripts/hooks/front_door.py: asks_pending() -> "ASK TIFFANY NOW (tile photo for <set>)" at the top of every chat.
CLI: python3 scripts/checks/tile_photo_check.py  -> PASS, or the sets waiting on her yes (exit 1)."""
import json, os, sys
R = '/home/claude/mahjmatchmaker-data/'


def _j(p, d=None):
    try: return json.load(open(R + p))
    except Exception: return d


def album_sets():
    d = _j('config/colorcards.json', {})
    return [k for k in d.get('sets', d) if not k.startswith('_')]


def live():
    return set(_j('docs/status/live-albums.json', {}).get('live', []))


def tile_photo(s):
    tp = (_j(f'config/album-records/{s}.json', {}) or {}).get('tile_photo')
    return tp if isinstance(tp, dict) else None


def approved(s):
    if s in live(): return True
    tp = tile_photo(s)
    return bool(tp and tp.get('approved_at'))


def problem(s):
    if approved(s): return None
    tp = tile_photo(s)
    if not tp: return f'no tile photo on record for {s} (config/album-records/{s}.json tile_photo): send it to Tiffany for a yes first'
    if not tp.get('asked_at'): return f'tile photo for {s} not sent to Tiffany yet (tile_photo.asked_at)'
    return f'tile photo for {s} waiting on her yes (asked {tp["asked_at"]})'


def missing_for_outdir(outdir):
    """The album set an output folder (assets/cards/<set>[-suffix]) belongs to, if its tile photo isn't approved."""
    base = os.path.basename(os.path.normpath(outdir))
    for s in sorted(album_sets(), key=len, reverse=True):
        if base == s or base.startswith(s + '-'):
            return None if approved(s) else s
    return None


def asks_pending():
    out = []
    for f in sorted(os.listdir(R + 'config/album-records')) if os.path.isdir(R + 'config/album-records') else []:
        s = f[:-5]; tp = tile_photo(s)
        if tp and tp.get('asked_at') and not tp.get('approved_at') and s not in live():
            out.append((s, tp))
    return out


if __name__ == '__main__':
    p = asks_pending()
    for s, tp in p: print(f"ASK TIFFANY NOW (tile photo for {s}): send the photo in chat for a yes ({tp.get('inset') or tp.get('file')}; asked {tp['asked_at']})")
    if p: sys.exit(1)
    print('TILE PHOTO CHECK PASS: no album tile photo waiting on her')
