"""Whole-domain link failures (Nov 7 2026, Tiffany 10:45pm, after Ozark Mahjongg was marked 'parked/dead' when the real store
https://www.ozarkmahjongg.com was live all along: our links had used ozarkmahjong.com, one g, a parked domain).

RULE: a failure of a WHOLE DOMAIN (parked page, JS redirect to /lander, 'domain for sale', every page of a host redirecting to one
other host, DNS gone) is never a reason to mark that brand's items dead. It almost always means WE have the wrong domain.
Before any item goes into config/fym-dead-links.json / config/mat-gallery-link-fixes.json for a domain-level failure:
  1. find the brand's REAL store (its Instagram bio / site footer link, config/social/ig-handles.json, a Google search of the brand);
  2. record it in config/brand-domains.json (brand -> real host + the wrong hosts seen);
  3. re-point the links to the real product pages; only items whose product is missing ON THE REAL STORE are dead.

Used by builder/fym_fix_nov06/linkcheck.py (gate [162]: a link on a parked/wrong host now counts as DEAD with status 'parked',
which a plain curl missed: the parked page answers 200 and redirects in JavaScript) and builder/fym_fix_nov06/deadlinks116.py
(refuses a dead-links entry on a parked host, or whose brand has a different real domain).
CLI: python3 scripts/checks/domain_check.py <url> [<url> ...]   -> prints host, parked?, why, the brand's real domain if known."""
import json, os, re, subprocess, sys
from urllib.parse import urlsplit

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
MARKERS = re.compile(r'window\.location(?:\.href)?\s*=\s*["\']/lander|/lander["\']|domain (?:is|may be) for sale|buy this domain|'
                     r'parkingcrew|sedoparking|bodis\.com|afternic|dan\.com/|hugedomains|this domain has expired|domain parking', re.I)
_CACHE = {}


def host(u):
    h = urlsplit(u if '://' in u else 'https://' + u).netloc.lower()
    return h[4:] if h.startswith('www.') else h


def domains():
    p = R + 'config/brand-domains.json'
    return json.load(open(p))['brands'] if os.path.exists(p) else {}


def real_domain(brand=None, h=None):
    """-> (brand, real_host) when the brand (or a known WRONG host) is in config/brand-domains.json, else (None, None)."""
    for b, x in domains().items():
        if (brand and b.lower() == brand.lower()) or (h and (host(h) in [host(w) for w in x.get('wrong', [])] or host(h) == host(x['real']))):
            return b, x['real']
    return None, None


def parked(h, timeout=20):
    """Is the host ROOT a parked / dead / off-host page? -> (bool, why). Cached per run."""
    h = host(h)
    if h in _CACHE: return _CACHE[h]
    try:
        r = subprocess.run(['curl', '-s', '-L', '--max-redirs', '6', '-m', str(timeout), '-A', UA, '-w', '\n%{http_code} %{url_effective}',
                            f'https://{h}/'], capture_output=True, text=True, timeout=timeout + 10)
        body, _, tail = r.stdout.rpartition('\n'); code, _, eff = tail.partition(' ')
    except Exception as e:
        _CACHE[h] = (True, f'no answer ({e.__class__.__name__})'); return _CACHE[h]
    if not code or code == '000': out = (True, 'no answer (DNS/connection)')
    elif MARKERS.search(body[:20000]): out = (True, 'parked-domain page (/lander redirect or for-sale marker)')
    elif host(eff) != h and not host(eff).endswith('.' + h) and not h.endswith('.' + host(eff)): out = (True, f'root redirects off-host to {host(eff)}')
    elif len(body) < 400 and 'location' in body.lower(): out = (True, 'tiny JS-redirect page')
    else: out = (False, f'{code} ok')
    _CACHE[h] = out; return out


def verdict(url, brand=None):
    """-> None when the domain is fine and the brand has no different real domain; else a message saying what to do."""
    h = host(url); b, real = real_domain(brand, h)
    if real and host(real) != h:
        return f'{h} is NOT {b}\'s store; the real domain is {real}: re-point the link (config/brand-domains.json)'
    p, why = parked(h)
    if p:
        return (f'{h}: {why}. Whole-domain failure: find {brand or "the brand"}\'s REAL store (IG bio / site footer / Google), add it to '
                f'config/brand-domains.json and re-point; do NOT mark items dead')
    return None


if __name__ == '__main__':
    for u in sys.argv[1:]:
        print(u, '->', verdict(u) or 'ok')
