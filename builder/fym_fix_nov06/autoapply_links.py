"""Auto-apply discount links (Nov 6 2026; standing authority: discount codes + links checks).

A Shopify link https://<store>/discount/<CODE>?redirect=<url-encoded path+query> sets the discount_code cookie, so the code is
already applied at checkout. A plain /products/<handle> link applies nothing (Tiffany asked Nov 6 1:21am; verified in a fresh
browser, docs/ANSWERS.md). This module turns every link of a Shopify CODE PARTNER (config/autoapply-hosts.json "hosts") into that
form, keeping the whole path + query (sca_ref, variant, ...) inside redirect=, exactly like the existing Bespoke / My Fair Mahjong
links. Hosts in "skip" (Tigre de Tartan: Oct 30 visible-only decision; Squarespace stores; Maison Mahj; ShopMy; Amazon) and every
other host are returned unchanged. Idempotent: a /discount/ link is left as it is.

Used by:
  - site/livepatch/matgallery/build_v6.py (Mat Gallery shop links)
  - the next FYM build (1.16): python3 builder/fym_fix_nov06/autoapply_links.py <build_dir> [--write]
    rewrites D.mats / D.racks / D.tiles `u` in <build_dir>/index.html (dry run without --write: prints counts per brand)
  - builder/fym_gate.py [159]: FAILS on any plain link of a Shopify code partner (plain_partner_links()).
"""
import json, os, re, sys
from urllib.parse import urlsplit, quote

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
CFG = json.load(open(REPO + 'config/autoapply-hosts.json'))
HOSTS, SKIP = CFG['hosts'], CFG['skip']


def host_of(u):
    try:
        return (urlsplit(u).netloc or '').lower().removeprefix('www.')
    except Exception:
        return ''


def classify(u):
    """-> 'empty' | 'discount' (already auto-applies) | 'skip' (host on the skip list) | 'other' (not a code partner) |
    'odd' (code-partner host, but not a product / collection / home link: e.g. a referral path; left alone) | 'plain' (convert)"""
    u = (u or '').strip()
    if not u:
        return 'empty'
    h = host_of(u)
    if h in SKIP:
        return 'skip'
    if h not in HOSTS:
        return 'other'
    p = urlsplit(u)
    if p.path.startswith('/discount/'):
        return 'discount'
    if p.path in ('', '/') or p.path.startswith(('/products/', '/collections/')):
        return 'plain'
    return 'odd'


def autoapply(u):
    """Returns (url, status). status = classify(u); only 'plain' links change."""
    st = classify(u)
    if st != 'plain':
        return u, st
    p = urlsplit(u.strip())
    cfg = HOSTS[host_of(u)]
    path = p.path or '/'
    target = path + ('?' + p.query if p.query else '')
    pre = (cfg['pre'] + '&') if cfg.get('pre') else ''
    return f"{p.scheme or 'https'}://{p.netloc}/discount/{cfg['code']}?{pre}redirect={quote(target, safe='')}", 'converted'


def redirect_target(u):
    """The product path a /discount/ link lands on (for checks)."""
    from urllib.parse import parse_qs, unquote
    q = parse_qs(urlsplit(u).query)
    return unquote(q.get('redirect', [''])[0])


def plain_partner_links(D):
    """[(group, key, name, brand, url)] for every FYM item whose link is a plain link of a Shopify code partner (gate [159])."""
    out = []
    for g in ('mats', 'racks', 'tiles'):
        for k, o in (D.get(g) or {}).items():
            if classify(o.get('u')) == 'plain':
                out.append((g, k, o.get('n'), o.get('bn'), o.get('u')))
    return out


def convert_D(D):
    """Rewrites u in D.mats / D.racks / D.tiles in place. Returns {brand: {status: count}}."""
    log = {}
    for g in ('mats', 'racks', 'tiles'):
        for k, o in (D.get(g) or {}).items():
            nu, st = autoapply(o.get('u'))
            log.setdefault(o.get('bn') or '?', {}).setdefault(f'{g}:{st}', 0)
            log[o.get('bn') or '?'][f'{g}:{st}'] += 1
            if st == 'converted':
                o.setdefault('u_plain', o.get('u'))  # keep the old link for audits (u0 already holds the scraped product URL)
                o['u'] = nu
    return log


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    B = sys.argv[1]
    P = os.path.join(B, 'index.html')
    h = open(P).read()
    i = h.index('const D=') + 8
    D, end = json.JSONDecoder().raw_decode(h, i)
    log = convert_D(D)
    tot = {}
    for b, d in sorted(log.items()):
        conv = {k: v for k, v in d.items() if k.endswith(':converted')}
        if conv:
            print(f'  {b}: ' + ', '.join(f'{k} {v}' for k, v in conv.items()))
        for k, v in d.items():
            tot[k.split(':')[1]] = tot.get(k.split(':')[1], 0) + v
    print('totals', tot)
    left = plain_partner_links(D)
    print('plain code-partner links left:', len(left))
    if '--write' in sys.argv:
        open(P, 'w').write(h[:i] + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + h[end:])
        print('written', P)
    else:
        print('(dry run: add --write to rewrite index.html)')
