"""Album review page self-test (Tiffany Nov 8 3:06pm: Scarlett vanished from Lagoon's list while she compared it with Reba;
grid view looked gone; Done must never lock). build_review.py runs this on the finished page BEFORE it writes index.html.

Usage: python3 scripts/albumreview/selftest.py <page.html> [saved-doc.json]
  The page must sit in its build folder (images under c/). With no saved doc, a hard one is made up: the main order
  reversed, every NEW card placed near the top (#2, #3...), done:true. With a saved doc (e.g. her real review/<set> doc),
  that doc is used as-is. The db is stubbed (window.claude.use('db')), viewport 390x844.
Fails (exit 1) when: any ordered card is missing from the list (cards view or grid view), a card shows twice, the order on
screen differs from the saved order, the Cards/Grid toggle is missing, Move to # does not move a NEW card, a control
stops working after Done, or the page logs a console error."""
import json, os, sys, re

STUB = """window.__DOC=%s;window.__W=[];window.claude={use:async n=>({doc:p=>({get:async()=>({exists:!!window.__DOC,data:()=>JSON.parse(JSON.stringify(window.__DOC))}),set:async d=>{window.__W.push(JSON.parse(JSON.stringify(d)))}})})};"""


def page_data(path):
    m = re.search(r'const D=(\{.*?\});\nconst \$', open(path, encoding='utf-8').read(), re.S)
    return json.loads(m.group(1).replace('<\\/', '</'))


def synth_doc(D):
    main = [c['id'] for c in D['cards'] if not c['hol']][::-1]
    hol = [c['id'] for c in D['cards'] if c['hol']]
    new = [i for i in main if next(c for c in D['cards'] if c['id'] == i)['new']]
    rest = [i for i in main if i not in new]
    main = rest[:1] + new + rest[1:]
    return {'set': D['set'], 'round': D['round'], 'v': {}, 'notes': {}, 'order': {'main': main, 'hol': hol}, 'ordering_off': False,
            'faces': D['picks'], 'cover': 0, 'putin': [], 'adds': [], 'finds': {}, 'anything': '', 'done': True}


def keep_place(pg, ids, order, doc):
    """Tiffany Nov 8 6:06pm: she types a number in a card's Move to # box, then taps the NEXT card's box. That alone must apply and
    save the move, the next box keeps focus, and the page must not jump (the next card stays within ~1 card, we require half).
    Same in grid view (pick up, tap a later spot): the cell after the spot she left stays put."""
    bad, L = [], len(order)
    if doc.get('ordering_off') or L < 8: return bad
    k = 2; A, B = order[k], order[k + 1]; to = min(L, k + 7)
    pg.locator(f'#mv-{A}').fill(str(to))
    pg.evaluate(f"window.scrollBy(0, document.getElementById('mv-{B}').getBoundingClientRect().top - 600)")
    y0 = pg.evaluate(f"document.getElementById('mv-{B}').getBoundingClientRect().top")
    card = pg.evaluate(f"document.querySelector('.mc[data-id=\"{B}\"]').getBoundingClientRect().height")
    n0 = len(pg.evaluate('window.__W'))
    pg.locator(f'#mv-{B}').click()
    pg.wait_for_timeout(800)
    now = ids('#main .mc', 'id')
    if A not in now or now.index(A) != to - 1: bad.append(f'blur (tapping the next box) did not apply Move to # for {A} (want #{to}, now #{now.index(A) + 1 if A in now else "gone"})')
    W = pg.evaluate('window.__W')
    if len(W) <= n0 or W[-1]['order']['main'].index(A) != to - 1: bad.append('blur (tapping the next box) did not SAVE the Move to #')
    y1 = pg.evaluate(f"document.getElementById('mv-{B}').getBoundingClientRect().top")
    if abs(y1 - y0) > card / 2: bad.append(f'page jumped after Move to #: the next box moved {y1 - y0:+.0f}px (card is {card:.0f}px)')
    if pg.evaluate('document.activeElement && document.activeElement.id') != f'mv-{B}': bad.append('the next card\'s Move to # box lost focus after the move')
    if 'Moved to #' not in (pg.evaluate("[...document.querySelectorAll('.mvnote')].map(x=>x.textContent).join(' ')") or ''): bad.append('no "Moved to #N" note on the spot she left')
    pg.locator(f'#mv-{A}').fill(str(k + 1)); pg.locator(f'#mv-{A}').press('Enter')
    if ids('#main .mc', 'id') != order: bad.append('Enter did not move the card back (order not restored)')
    if L >= 12:  # grid: pick up #4, tap #10; the cell that was #5 stays on screen where it was
        pg.locator('.topview .vt button[data-view="grid"]').click()
        P, N, T = order[3], order[4], order[9]
        pg.evaluate(f"window.scrollBy(0, document.querySelector('.gc[data-gid=\"{N}\"]').getBoundingClientRect().top - 300)")
        y0 = pg.evaluate(f"document.querySelector('.gc[data-gid=\"{N}\"]').getBoundingClientRect().top")
        row = pg.evaluate(f"document.querySelector('.gc[data-gid=\"{N}\"]').getBoundingClientRect().height")
        pg.locator(f'.gc[data-gid="{P}"]').click(); pg.locator(f'.gc[data-gid="{T}"]').click()
        g = ids('#main .gc', 'gid')
        if g.index(P) != 9: bad.append(f'grid tap-to-place failed (#4 went to #{g.index(P) + 1}, want #10)')
        y1 = pg.evaluate(f"document.querySelector('.gc[data-gid=\"{N}\"]').getBoundingClientRect().top")
        if abs(y1 - y0) > row / 2: bad.append(f'grid jumped after a move: {y1 - y0:+.0f}px (row is {row:.0f}px)')
        nums = pg.eval_on_selector_all('#main .gc .gn', 'els=>els.map(e=>e.textContent)')
        if nums != [f'#{n + 1}' for n in range(len(nums))]: bad.append('grid numbers not redone after a move')
        pg.locator(f'.gc[data-gid="{P}"]').click(); pg.locator(f'.gc[data-gid="{N}"]').click()
        pg.locator('.topview .vt button[data-view="cards"]').click()
        if ids('#main .mc', 'id') != order: bad.append('grid round trip did not restore the order')
    return bad


def run(path, doc=None):
    from playwright.sync_api import sync_playwright
    D = page_data(path)
    doc = doc or synth_doc(D)
    bad = []
    want = {s: [i for i in (doc.get('order') or {}).get(s, []) if any(c['id'] == i for c in D['cards'])] for s in ('main', 'hol')}
    allids = {s: [c['id'] for c in D['cards'] if c['hol'] == (s == 'hol')] for s in ('main', 'hol')}
    expect = {s: want[s] + [i for i in allids[s] if i not in want[s]] for s in ('main', 'hol')}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 390, 'height': 844})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.add_init_script(STUB % json.dumps(doc))
        pg.goto('file://' + os.path.abspath(path))
        pg.wait_for_function("document.querySelector('#st').textContent.includes('loaded')", timeout=8000)
        ids = lambda sel, attr: pg.eval_on_selector_all(sel, f'els=>els.map(e=>e.dataset.{attr})')
        if doc.get('done') and pg.locator('#donebar').is_hidden(): bad.append('Done state not shown (Still ordering bar missing)')
        for s in ('main', 'hol'):
            got = ids(f'#{s} .mc', 'id')
            if got != expect[s]:
                miss = [i for i in expect[s] if i not in got]
                bad.append(f'cards view {s}: shows {len(got)} of {len(expect[s])}; missing {miss[:5]}; order matches: {got == expect[s]}')
        if pg.locator('.vt[data-sec="main"] button[data-view="grid"]').count() < 2:
            bad.append('Cards/Grid toggle missing (need the one at the top and the one on the matches bar)')
        else:
            pg.locator('.topview .vt button[data-view="grid"]').click()
            got = ids('#main .gc', 'gid')
            if got != expect['main']:
                bad.append(f'grid view main: shows {len(got)} of {len(expect["main"])}')
            pg.locator('.topview .vt button[data-view="cards"]').click()
        newids = [i for i in expect['main'] if next(c for c in D['cards'] if c['id'] == i)['new']]
        targets = newids or expect['main'][-1:]
        for i in targets:  # Move to # on every NEW card (and the last card when there are none): to #2 and back
            orig = expect['main'].index(i) + 1
            for to in (2, orig):
                inp = pg.locator(f'#mv-{i}')
                inp.fill(str(to)); pg.locator(f'[data-go="mv-{i}"]').click()
                now = ids('#main .mc', 'id')
                if len(now) != len(expect['main']) or now.index(i) != to - 1:
                    bad.append(f'Move to # failed for {i} (to #{to}; now #{now.index(i) + 1 if i in now else "gone"}, {len(now)} cards shown)')
                    break
        if newids:  # the New box Move to # too
            i = newids[0]; orig = expect['main'].index(i) + 1
            pg.locator(f'#nmv-{i}').fill('1'); pg.locator(f'[data-go="nmv-{i}"]').click()
            now = ids('#main .mc', 'id')
            if now[:1] != [i] or len(now) != len(expect['main']): bad.append(f'New box Move to # failed for {i}')
            pg.locator(f'#mv-{i}').fill(str(orig)); pg.locator(f'[data-go="mv-{i}"]').click()
        if ids('#main .mc', 'id') != expect['main']: bad.append('order not restored after the Move to # round trip')
        bad += keep_place(pg, ids, expect['main'], doc)
        # Done never locks: with done set, hearts, arrows and grid still work
        first = expect['main'][0]
        pg.locator(f'.mc[data-id="{first}"] [data-act="keep"]').click()
        if pg.locator(f'.mc[data-id="{first}"] [data-act="keep"]').get_attribute('aria-pressed') != 'true': bad.append('heart does not work after Done')
        pg.locator(f'.mc[data-id="{first}"] [data-act="keep"]').click()
        if len(ids('#main .mc', 'id')) != len(expect['main']): bad.append('cards lost after tapping a heart')
        pg.wait_for_timeout(700)
        if errs: bad.append('console errors: ' + ' | '.join(errs[:3]))
        b.close()
    return bad


if __name__ == '__main__':
    doc = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else None
    bad = run(sys.argv[1], doc)
    print('REVIEW PAGE SELF-TEST ' + ('FAIL:\n  ' + '\n  '.join(bad) if bad else 'PASS'))
    sys.exit(1 if bad else 0)
