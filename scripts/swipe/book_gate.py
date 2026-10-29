#!/usr/bin/env python3
"""Swipe-book gate. A tile-set swipe book is NOT written or published unless this passes (exit 0).

Why (Tiffany, Oct 29 12:35pm): "you're only as good as the rules we create... if we created the rule and
you're just not following it, where do I go from there?" The Sunday Sets book went out without colour cards,
without the Tiles & Tablescapes recs and from the old narrow pool, although the rules existed. So the rules
live here, in code, and build_book.py + finish_patch.py refuse to write a book that fails.

Checks, for every tile-set group in a tile-mode book (D.mode == 'tile'):
  [a] colour card first: the set is in config/colorcards.json or has a card in assets/colorcards/<set>/ (doc 86 / 86b: colour card BEFORE the swipe).
  [b] TNT recs: the set has a record in config/tnt-recs.json, and every rec that is allowed (partner brand,
      or on builder/fym_flags/nonpartner_allow.json), visible in FYM, not holiday and has an fym_key is in the
      deck AHEAD of every non-TNT mat, labelled "TNT rec · <mat> · brand".
  [c] FYM photos: every mat item carries its FYM key (item.key, in config/fym-mats-snapshot.json) and
      item.ph in PH_OK (the FYM photo, its full-res twin matched by build_book, or a canonical override).
  [d] no holiday / hidden / skip-list (tiffany-skip-list.json) / Mahjong Studios / Splash of Color mats.
  [e] widest pool: D.pool = {src: 'fym-full-measured', n: <mats ranked>} (the full FYM catalog ranked by
      measured colour shares). Missing, or the old TIGHT pull (Oct 19 matcolors.pull, cap 60), fails.
Mat-mode books (groups are mats, items are tile sets) only get [e] skipped and a notice; [c]/[d] do not apply.

Usage: python3 scripts/swipe/book_gate.py <book index.html> [--snapshot config/fym-mats-snapshot.json]
Refresh the snapshot after every FYM publish: scripts/swipe/fym_snapshot.py <FYM index.html>.
"""
import sys, os, re, json

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
PH_OK = {'fym', 'fym-hires', 'canon-override'}
ALIAS = {'sunday': 'sunday-tile-set'}
BANNED_BRANDS = {'mahjong studios', 'splash of color'}
HOLIDAY = re.compile(r"christmas|xmas|holly|yuletide|merriment|winterberry|nutcracker|sugarplum|\bclara\b|santa|noel|jingle|"
                     r"candy cane|winter wonderland|mistletoe|reindeer|snowflake|halloween|spooky|valentine|easter|hanukkah", re.I)


def load_D(path):
    h = open(path).read()
    i = h.index('const D=') + 8
    return json.JSONDecoder().raw_decode(h[i:])[0]


def gate(path, snap_path=None):
    F, notes = [], []
    D = load_D(path)
    snap = json.load(open(snap_path or os.path.join(REPO, 'config', 'fym-mats-snapshot.json')))['mats']
    cards = json.load(open(os.path.join(REPO, 'config', 'colorcards.json')))['sets']
    tnt = json.load(open(os.path.join(REPO, 'config', 'tnt-recs.json')))['sets']
    na = json.load(open(os.path.join(REPO, 'builder', 'fym_flags', 'nonpartner_allow.json')))
    na_brands = {b.lower() for b in (na.get('brands') or {})}
    na_mats = set((na.get('mats') or {}).keys())
    skip = json.load(open(os.path.join(REPO, 'tiffany-skip-list.json')))['mats']
    skip_h = {(s.get('handle') or '').lower() for s in skip if s.get('handle')}
    mode = D.get('mode', 'tile')
    if mode != 'tile':
        notes.append(f"mode={mode}: tile-set checks [a][b][c][d] apply to tile-mode books only")
    else:
        pool = D.get('pool') or {}
        if pool.get('src') != 'fym-full-measured' or not isinstance(pool.get('n'), int) or pool.get('n', 0) < 200:
            F.append(f"[e] pool is not the widest one (D.pool={pool!r}); rank the FULL FYM catalog by measured colour shares and record D.pool={{src:'fym-full-measured',n:...}}")
    items = {x['id']: x for x in D.get('items', [])}
    order = D.get('order') or {}

    def allowed(m, key):
        bn = (m.get('bn') or '').lower()
        return m.get('pa') or bn in na_brands or key in na_mats

    for g in D.get('groups', []):
        gid = re.sub(r'^(hol-|vault-|ret-)', '', g['id'])
        gid = ALIAS.get(gid, gid)
        if mode != 'tile':
            continue
        _cd = os.path.join(REPO, 'assets', 'colorcards', gid)
        if gid not in cards and not (os.path.isdir(_cd) and any(f.endswith(('.jpg', '.png')) for f in os.listdir(_cd))):
            F.append(f"[a] {g.get('label', gid)}: no colour card in config/colorcards.json (doc 86b: colour card BEFORE the swipe)")
        rec = tnt.get(gid)
        ids = order.get(g['id']) or [x['id'] for x in D.get('items', [])]
        if not rec:
            F.append(f"[b] {g.get('label', gid)}: no TNT recs record in config/tnt-recs.json (search Tiles & Tablescapes first)")
        else:
            need = [r for r in rec.get('recs', []) if r.get('fym_key') in snap and not snap[r['fym_key']]['hid']
                    and not snap[r['fym_key']]['hol'] and not HOLIDAY.search(r.get('note', '')) and allowed(snap[r['fym_key']], r['fym_key'])]
            keyed = {items[i].get('key'): (n, items[i]) for n, i in enumerate(ids) if i in items and items[i].get('key')}
            pos = []
            for r in need:
                hit = keyed.get(r['fym_key'])
                if not hit:
                    F.append(f"[b] {g.get('label', gid)}: TNT rec {r['mat']} ({r['brand']}) is in FYM but not in the deck"); continue
                n, it = hit; pos.append(n)
                if not (it.get('label') or '').startswith('TNT rec · '):
                    F.append(f"[b] {g.get('label', gid)}: TNT rec {r['mat']} not labelled 'TNT rec · <mat> · brand' ({it.get('label')!r})")
            if pos and max(pos) >= len(pos):
                F.append(f"[b] {g.get('label', gid)}: TNT recs do not lead the deck (positions {sorted(pos)})")
        for i in ids:
            it = items.get(i)
            if not it:
                continue
            key = it.get('key')
            if not key or key not in snap:
                F.append(f"[c] {g.get('label', gid)} · {it.get('label', i)}: no FYM key (item.key) in the FYM snapshot"); continue
            if it.get('ph') not in PH_OK:
                F.append(f"[c] {g.get('label', gid)} · {it.get('label', i)}: photo is not the FYM photo (item.ph={it.get('ph')!r})")
            m = snap[key]
            why = ('holiday' if m['hol'] or HOLIDAY.search(m.get('n') or '') else 'hidden in FYM' if m['hid'] else
                   'banned brand' if (m.get('bn') or '').lower() in BANNED_BRANDS else
                   'skip list' if key.split('/')[-1].lower() in skip_h else '')
            if why:
                F.append(f"[d] {g.get('label', gid)} · {m.get('n')} ({m.get('bn')}): {why}")
    return F, notes


def main():
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    snap = sys.argv[sys.argv.index('--snapshot') + 1] if '--snapshot' in sys.argv else None
    if snap in a:
        a.remove(snap)
    if not a:
        print(__doc__); sys.exit(2)
    F, notes = gate(a[0], snap)
    for n in notes:
        print('BOOK GATE NOTE: ' + n)
    if F:
        print(f"BOOK GATE: FAIL ({len(F)} problems) — do not publish this book")
        for f in F[:80]:
            print('  ' + f)
        if len(F) > 80:
            print(f'  ... {len(F) - 80} more')
        sys.exit(1)
    print('BOOK GATE: PASS')


if __name__ == '__main__':
    main()
