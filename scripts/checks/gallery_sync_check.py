#!/usr/bin/env python3
"""Mat Gallery vs Find Your Mat-ch sync check (Tiffany Nov 6 2026, 5:24pm: "set it up that way").

DAILY (morning HQ cleanup, seconds):   python3 scripts/checks/gallery_sync_check.py
WEEKLY (Mondays, ~3 min, adds links):   python3 scripts/checks/gallery_sync_check.py --links

Daily: the live /mahjong-mats gallery must be stamped data-fym="vNNN" with the SAME version
as the live /find-your-match app (page block loads site-app/fym-vNNN/index.html).
Weekly: every non-ShopMy shop link in the live gallery data is loaded; 404/410 = dead. --links also runs the LINK-ROUTE check
(scripts/checks/link_route_check.py, config/link-routes.json, Nov 8): every live gallery link + the newest website FYM build must be
paid the way its brand's route says (ShopMy redirects resolved); unstaged mismatches FAIL, staged ones are listed.
Prints one line: PASS ... or FAIL ... (exit 1). FAIL = fix the same day (rebuild/paste the
gallery per site/livepatch/matgallery/README.md "v6", or drop/replace dead links via
config/mat-gallery-link-fixes.json). No Claude usage beyond reading the one line.
"""
import re, sys, json, urllib.request, concurrent.futures as cf, time

SITE = 'https://www.mahjmatchmaker.com'
UA = {'User-Agent': 'Mozilla/5.0 (MahjMatchmaker link check)'}


def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', 'replace')


def status(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=UA, method='GET')
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(5 * (attempt + 1)); continue
            return e.code
        except Exception:
            time.sleep(2)
    return 0  # unreachable: warn only


def main():
    links = '--links' in sys.argv
    problems, notes = [], []
    _, app = get(f'{SITE}/find-your-match?x={int(time.time())}')
    m = re.search(r'site-app/fym-v(\d+)/index\.html', app)
    app_v = int(m.group(1)) if m else None
    _, gal = get(f'{SITE}/mahjong-mats?x={int(time.time())}')
    g = re.search(r'data-fym="v(\d+)"', gal)
    gal_v = int(g.group(1)) if g else None
    if app_v is None:
        problems.append('could not read the live app version')
    if gal_v is None:
        problems.append('live gallery has no data-fym stamp (still the old v5 block)')
    elif app_v and gal_v < app_v:
        problems.append(f'gallery built from v{gal_v}, app is v{app_v}: rebuild + paste the gallery')
    if links:
        d = re.search(r'data-src="([^"]+matgallery-v\d+\.json)"', gal)
        if '--data' in sys.argv:  # test a candidate data file before it is live
            d = re.match(r'(.*)', sys.argv[sys.argv.index('--data') + 1])
        if not d:
            problems.append('no gallery data file found for the link check')
        else:
            _, raw = get(d.group(1))
            rows = json.loads(raw)
            urls = {}
            def walk(x):
                if isinstance(x, str):
                    if x.startswith('http'): yield x
                elif isinstance(x, list):
                    for y in x: yield from walk(y)
            for r in rows:
                for u in walk(r):
                    if 'shopmy' not in u and 'etsy.com' not in u and 'jsdelivr' not in u:
                        urls.setdefault(u, r[1] + ' · ' + r[2])
            with cf.ThreadPoolExecutor(8) as ex:
                res = dict(zip(urls, ex.map(status, urls)))
            dead = [f'{urls[u]} ({c})' for u, c in res.items() if c in (404, 410)]
            unk = sum(1 for c in res.values() if c == 0)
            notes.append(f'{len(res)} links checked')
            if unk: notes.append(f'{unk} unreachable (not counted)')
            if dead:
                problems.append(f'{len(dead)} dead shop links: ' + '; '.join(dead[:15]))
            try:  # link routes (Nov 8 2026, Tiffany 6:02pm): live gallery rows + newest website FYM build
                sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
                import link_route_check as LR
                try:
                    _html, _src = LR.website_build(); _D = LR.load_D(_html)
                except BaseException:
                    _D = None
                lr = LR.check(_D, rows)
                notes.append(f"link routes: {len(lr['fails'])} mismatches, {len(lr['staged'])} staged")
                if lr['fails']:
                    problems.append(f"{len(lr['fails'])} links not paid the way config/link-routes.json says: " + '; '.join(lr['fails'][:10]))
            except Exception as e:
                notes.append(f'link-route check did not run: {e}')
    head = f'app v{app_v}, gallery v{gal_v}'
    if problems:
        print('FAIL gallery_sync_check: ' + head + ' | ' + ' | '.join(problems + notes)); sys.exit(1)
    print('PASS gallery_sync_check: ' + head + (' | ' + ', '.join(notes) if notes else ''))


if __name__ == '__main__':
    main()
