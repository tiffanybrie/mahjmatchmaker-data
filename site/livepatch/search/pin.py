#!/usr/bin/env python3
"""Pin the site search snippet to a commit and warm every jsDelivr URL it uses (doc 73).

Usage (repo root):  python3 site/livepatch/search/pin.py <commit sha>          pin + warm
                    python3 site/livepatch/search/pin.py <commit sha> --no-warm
Rewrites the @<sha> in header-injection.html, writes urls.txt (css, js, index, every thumb)
and warm_result.json. The commit must already be pushed and contain assets/search/.
"""
import json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@%s/assets/search/'


def main():
    if len(sys.argv) < 2 or not re.fullmatch(r'[0-9a-f]{7,40}', sys.argv[1]):
        sys.exit(__doc__)
    sha = subprocess.run(['git', '-C', ROOT, 'rev-parse', sys.argv[1]], capture_output=True, text=True).stdout.strip()
    if not sha:
        sys.exit('unknown commit')
    base = CDN % sha
    p = os.path.join(HERE, 'header-injection.html')
    h = open(p).read()
    h = re.sub(r'https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]+/assets/search/', base, h)
    open(p, 'w').write(h)
    # every file the snippet can load at that commit
    ls = subprocess.run(['git', '-C', ROOT, 'ls-tree', '-r', '--name-only', sha, 'assets/search/'],
                        capture_output=True, text=True).stdout.split()
    files = [f for f in ls if f.endswith(('.css', '.js', 'search-index.json', '.webp'))]
    urls = [base + f[len('assets/search/'):] for f in files]
    urls.sort(key=lambda u: (not u.endswith(('.css', '.js', '.json')), u))
    open(os.path.join(HERE, 'urls.txt'), 'w').write('\n'.join(urls) + '\n')
    print('pinned to', sha, '|', len(urls), 'urls')
    if '--no-warm' in sys.argv:
        return

    def warm(u):
        last = None
        for i in range(8):
            r = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '40', u],
                               capture_output=True, text=True)
            last = r.stdout.strip()
            if last == '200':
                return u, 200, i
            time.sleep(2 + 2 * i)
        return u, last, 8
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(warm, urls))
    bad = {u: c for u, c, n in res if c != 200}
    out = {'commit': sha, 'total': len(res), 'ok_first_try': sum(1 for u, c, n in res if c == 200 and n == 0),
           'ok_after_retry': sum(1 for u, c, n in res if c == 200 and n > 0), 'still_failing': bad}
    json.dump(out, open(os.path.join(HERE, 'warm_result.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'still_failing'}), '| still failing:', len(bad))


if __name__ == '__main__':
    main()
