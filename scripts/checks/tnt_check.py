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
# TABLED (Tiffany Nov 8 1:11pm): albums already live before the TNT gate; no backward-looking TNT search this week
# ("we got to make sure we're at least on track for this week before we start looking backwards"). Rainy-day item on DESK.
SKIP |= {'shangri-la', 'lilac-soiree', 'preppy-soiree', 'spring-love', 'papaya-spritz', 'sunday-tile-set', 'brownstone-bloom', 'juniper'}


def album_sets():
    d = json.load(open(R + 'config/colorcards.json'))
    return [k for k in d.get('sets', d) if not k.startswith('_') and k not in SKIP]


def complete(v):
    """Tiffany Nov 8 6:20pm ("you didn't even make it thru the Deco tiles list on just Tiles & tablescapes"): a TNT record only
    counts when it proves the search was exhaustive: posts_read > 0, the terms searched, and scrolled_to_end true (every search
    scrolled to Facebook's 'End of results', every Deco post opened and read to the last comment)."""
    return (isinstance(v, dict) and v.get('scanned') and (v.get('posts_read') or 0) > 0
            and isinstance(v.get('terms'), list) and len(v['terms']) > 0 and v.get('scrolled_to_end') is True)


def why_incomplete(v):
    if not isinstance(v, dict) or not v.get('scanned'): return 'never searched'
    out = []
    if not (v.get('posts_read') or 0) > 0: out.append('posts_read missing/0')
    if not (isinstance(v.get('terms'), list) and v['terms']): out.append('terms list missing')
    if v.get('scrolled_to_end') is not True: out.append('scrolled_to_end not true')
    return ', '.join(out)


def tnt_sets():
    d = json.load(open(R + 'config/tnt-recs.json'))
    return {k: v for k, v in d.get('sets', {}).items() if complete(v)}


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
        allr = json.load(open(R + 'config/tnt-recs.json')).get('sets', {})
        print(f'TNT CHECK FAIL: {len(m)} album set(s) with no complete Tiles & Tablescapes search: ' + ', '.join(f'{s} ({why_incomplete(allr.get(s))})' for s in m))
        print('  Search the TNT group (read the WHOLE post), save to config/tnt-recs.json sets.<set> {scanned, source, recs[], posts_read, terms[], scrolled_to_end: true}, '
              'and put allowed recs FIRST in the album ("TNT rec · mat · brand").')
        sys.exit(1)
    print('TNT CHECK PASS: every album set has a Tiles & Tablescapes search on record')
