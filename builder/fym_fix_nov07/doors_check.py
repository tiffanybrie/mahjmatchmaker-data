#!/usr/bin/env python3
"""FYM gate [167] (Nov 7 2026, FYM 1.18; Tiffany 10:24pm "make sure everything is mirrored up so that everybody can get to whatever
they want to get to, however they want to get to it"): STATIC door-parity check.

For every item type (tile sets, mats, racks) it reads, from the build's own source, which filter controls each place that item is
chosen renders (tiles door / mat door, step 1 / step 2 / racks step, Table view swap sheet) and fails when they differ:
  * every place gets the item type's BASE set: search, brand, colour, holiday (tiles + mats), in stock, price
    (+ multi-colour for mats in the app; + rack type for racks);
  * every place that comes AFTER another pick (2nd step, racks step, Table view) also gets Tiffany's picks + 'same brand as my ...'.
KNOWN (allowed, listed in the report): the Table view sheet is single-colour for mats (no '+ Add a colour').
Usage: python3 builder/fym_fix_nov07/doors_check.py <build_dir | index.html> [--json]   -> prints the matrix; exit 1 on a gap.
"""
import json, os, sys


def region(h, a, b):
    i = h.find(a)
    if i < 0: return ''
    j = h.find(b, i + len(a))
    return h[i:j if j > 0 else i + 20000]


def matrix(h):
    fn = lambda name, nxt: region(h, 'function ' + name + '(', nxt)
    rTiles = fn('renderTiles', 'function addSB(')
    rMats = fn('renderMats', 'const rBackBtn=')
    rRacks = fn('renderRacks', 'function matBand(')
    rFilt = fn('filters', 'function card(')
    rIns = region(h, 'const _ib=INSB;INSB=', ';\ndocument')
    rDoor = fn('renderMatDoor', "document.addEventListener('click'")
    rDchips = fn('doorChips', 'function setsForMat(')
    rTsw = fn('tswipe', 'function tdecide(')
    rTfil = region(h, 'window.TFIL=function', 'window.SAMEB=')
    rSame = region(h, 'window.SAMEB=function', 'window.TGON=')
    rTorder = fn('tileOrder', 'function tileChips(')
    rTv = region(h, 'function panel(){', 'function pass(force)')
    rCk = fn('colorKeys', 'function dots(')
    rBp = fn('brandPop', 'function synth(')
    rPool = fn('pool', 'function list(')
    has = lambda r, *t: bool(r) and all(x in r for x in t)
    tv = lambda tab_colour: {  # Table view swap sheet: one sheet, tabbed; shared controls + per-tab colour keys
        'search': has(rTv, 'id="tvq"'), 'brand': has(rTv, 'id="tvbrand"', 'data-tvb'), 'colour': has(rTv, 'id="tvdots"', 'data-tvc'),
        'instock': has(rTv, 'id="tvins"'), 'price': has(rTv, 'id="tvprices"', 'tvprsel'), 'picks': has(rTv, 'id="tvpk"'),
        'samebrand': has(rBp, 'Same brand as my'), **tab_colour}
    M = {
        'tiles': {
            'tiles door, step 1 (tile grid)': {
                'search': has(rTiles, 'id="tsq"'), 'brand': has(rTiles, 'brandMenu()'), 'colour': has(rTiles, 'tileChips()'),
                'holiday': has(rTorder, "unshift('Holiday')") or has(rTorder, "push('Holiday')"), 'instock': has(rTiles, 'TINS()'),
                'price': has(rTiles, "GPRB('t')")},
            'mat door, step 2 (tile swipe)': {
                'search': has(rTsw, 'id="tdq"'), 'brand': has(rTsw, 'TFIL()') and has(rTfil, 'data-tbrands'),
                'colour': has(rTfil, 'data-tfam="${esc(G)}"'), 'holiday': has(rTfil, 'data-tfam="Holiday"'),
                'instock': has(rTfil, 'chipIns(ie)') and has(h, 'const chipIns=e=>`<div class="insw"><button type="button" class="chip insb" data-ins'), 'price': has(rTfil, "PRB('t')") or has(rTsw, "PRB('t')"), 'picks': has(rTfil, 'data-ther'),
                'samebrand': has(rTfil, "sameChip('t','mat'")},
            "mat door, step 2 ('See all' grid)": {
                'search': has(rTsw, 'id="tdq"'),  # the grid is the same step: its search is the swipe view's (one tap, 'Swipe instead')
                'brand': has(rDoor, 'TFIL()'), 'colour': has(rDoor, 'TFIL()'), 'holiday': has(rDoor, 'TFIL()'), 'instock': has(rDoor, 'TFIL()'),
                'price': has(rDoor, 'TFIL()'), 'picks': has(rDoor, 'TFIL()'), 'samebrand': has(rDoor, 'TFIL()')},
            'Table view swap sheet (Tiles tab)': tv({'holiday': has(rCk, 'BACKG')}),
        },
        'mats': {
            'mat door, step 1 (mat grid)': {
                'search': has(rDoor, 'id="mdq"'), 'brand': has(rDoor, 'matBrandMenu()'), 'colour': has(rDchips, 'data-dfam="${f}"'),
                'multicolour': has(rDchips, 'data-dmulti'), 'holiday': has(rDchips, 'data-dfam="holiday"'), 'instock': has(rDchips, "INSB('d')"),
                'price': has(rDoor, "GPRB('m')")},
            'tiles door, step 2 (mat deck)': {
                'search': has(rMats, 'id="msq"'), 'brand': has(rMats, "filters('m')") and has(rFilt, 'data-brands="${k}"'),
                'colour': has(rFilt, 'data-fam="${x}"'), 'multicolour': has(rFilt, 'data-fmulti'), 'holiday': has(rFilt, 'data-fam="holiday"'),
                'instock': has(rFilt, 'INSB(k)'), 'price': has(rIns, "k==='m'", 'PRB(k)'), 'picks': has(rFilt, 'herBtn(k)'),
                'samebrand': has(rFilt, 'SAMEB(k)') and has(rSame, "['tiles',tb]")},
            'Table view swap sheet (Mat tab)': tv({'holiday': has(rCk, "SW.tab==='mat')return ['holiday'") and has(rPool, "isHolM(k)?['holiday']")}),
        },
        'racks': {
            'racks step (both doors)': {
                'search': has(rRacks, 'data-rsheet'), 'brand': has(rRacks, "filters('r')") and has(rFilt, 'data-brands="${k}"'),
                'colour': has(rFilt, 'data-fam="${x}"'), 'type': has(rFilt, 'FINROW('), 'instock': has(rFilt, 'INSB(k)'),
                'price': has(rIns, "k==='r'", 'PRB(k)'), 'picks': has(rFilt, 'herBtn(k)'),
                'samebrand': has(rFilt, 'SAMEB(k)') and has(rSame, "k==='r'&&S.fav")},
            'Table view swap sheet (Racks tab)': tv({'type': has(rTv, 'id="tvfins"', 'data-tvfin')}),
        },
    }
    return M


BASE = {'tiles': ['search', 'brand', 'colour', 'holiday', 'instock', 'price'],
        'mats': ['search', 'brand', 'colour', 'multicolour', 'holiday', 'instock', 'price'],
        'racks': ['search', 'brand', 'colour', 'type', 'instock', 'price']}
SECOND = ['picks', 'samebrand']
FIRST_STEP = {'tiles door, step 1 (tile grid)', 'mat door, step 1 (mat grid)'}
KNOWN = {('mats', 'Table view swap sheet (Mat tab)', 'multicolour'): 'the swap sheet picks one colour at a time (v114 singles)'}


def check(h):
    M = matrix(h); fails = []
    for it, places in M.items():
        for pl, c in places.items():
            need = BASE[it] + ([] if pl in FIRST_STEP else SECOND)
            for k in need:
                if c.get(k): continue
                if (it, pl, k) in KNOWN: continue
                fails.append(f"{it}: '{pl}' has no {k} filter (every place {it} are chosen must have it; run builder/fym_fix_nov07/doors_v118.py)")
    return fails, M


def main():
    p = sys.argv[1]; p = p if p.endswith('.html') else os.path.join(p, 'index.html')
    h = open(p).read(); fails, M = check(h)
    if '--json' in sys.argv:
        print(json.dumps({'fails': fails, 'matrix': M})); return 1 if fails else 0
    cols = ['search', 'brand', 'samebrand', 'colour', 'multicolour', 'holiday', 'type', 'instock', 'price', 'picks']
    for it, places in M.items():
        print(f'\n{it.upper()}')
        for pl, c in places.items():
            print(f'  {pl:44s} ' + ' '.join(f"{k}={'Y' if c.get(k) else ('known' if (it, pl, k) in KNOWN else '-')}" for k in cols if k in c or k in BASE[it] or k in SECOND))
    print('\nDOOR PARITY: ' + ('PASS' if not fails else f'FAIL ({len(fails)})'))
    for f in fails: print('  ' + f)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
