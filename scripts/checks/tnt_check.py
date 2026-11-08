"""Tiles & Tablescapes (TNT) gate for ALBUMS (Tiffany Nov 8 12:57pm: "I don't want to have to ask for the tiles and
tablescape stuff. We went over this with the previous album. Why does that stuff get missed every single time?").

Why it kept slipping: the TNT rule was only enforced by scripts/swipe/book_gate.py, i.e. only when a SWIPE BOOK was built.
Juniper, Papaya Spritz and the Deco albums went straight to album cards / review pages, so nothing ever asked for TNT.

Rule now: every album tile set (each key in config/colorcards.json 'sets' = every album, since the colour card is step one)
must have a record in config/tnt-recs.json 'sets' with a 'scanned' date and a 'source' saying what was searched
(finds may be empty). Allowed/visible recs LEAD the album, labelled "TNT rec · <mat> · <brand>".

Used two ways:
- scripts/albumcard/gen2.py imports missing_for_outdir() and REFUSES to render album cards for a set with no TNT record.
- CLI: python3 scripts/checks/tnt_check.py  -> PASS, or FAIL listing the album sets with no TNT search (exit 1).
  scripts/hooks/front_door.py shows the FAIL lines at the top of every chat.
SKIP: sets Tiffany dropped (no album)."""
import json, os, sys
R = '/home/claude/mahjmatchmaker-data/'
SKIP = {'style-of-your-life'}  # dropped Nov 7 11:47pm (Dillard's exclusive)


def album_sets():
    d = json.load(open(R + 'config/colorcards.json'))
    return [k for k in d.get('sets', d) if not k.startswith('_') and k not in SKIP]


def tnt_sets():
    d = json.load(open(R + 'config/tnt-recs.json'))
    return {k: v for k, v in d.get('sets', {}).items() if isinstance(v, dict) and v.get('scanned')}


def missing():
    t = tnt_sets()
    return [s for s in album_sets() if s not in t]


def missing_for_outdir(outdir):
    """The album set an output folder (assets/cards/<set>[-suffix]) belongs to, if it has no TNT record."""
    base = os.path.basename(os.path.normpath(outdir))
    t = tnt_sets()
    for s in sorted(album_sets(), key=len, reverse=True):
        if base == s or base.startswith(s + '-'):
            return None if s in t else s
    return None


if __name__ == '__main__':
    m = missing()
    if m:
        print(f'TNT CHECK FAIL: {len(m)} album set(s) never searched in Tiles & Tablescapes: ' + ', '.join(m))
        print('  Search the TNT group (read the WHOLE post), save to config/tnt-recs.json sets.<set> {scanned, source, recs[]}, '
              'and put allowed recs FIRST in the album ("TNT rec · mat · brand").')
        sys.exit(1)
    print('TNT CHECK PASS: every album set has a Tiles & Tablescapes search on record')
