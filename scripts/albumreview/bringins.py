"""Bring-in tracker (Album Playbook step 10b, Tiffany Nov 8 6:02pm: album bring-ins must close the loop).

When she taps "Bring it in" on a New find, read_review.py adds an entry to config/album-records/<set>.json "bringins":
  {id, mat, brand, store, store_url, route, shopmy_link, shopmy_collection, amazon_saved, ops_imported, catalog_staged, round, at, notes}
  - route comes from config/link-routes.json (by brand, else by store host: etsy.com -> shopmy-etsy, amazon -> shopmy-amazon,
    anything else -> shopmy-site); docs/LINK-ROUTES.md
  - every step field is null until done, then a short proof string ("go.shopmy.us/p-..", "config/fym-....json", "2026-11-08 Ops")
  - amazon_saved / ops_imported only matter for shopmy-amazon (Associates portal save, then Ops imports it into ShopMy)
album_gate.py --golive FAILS while any bring-in lacks its paid link or catalog staging (missing()).
"""
import json, os, re, datetime, urllib.parse

R = '/home/claude/mahjmatchmaker-data/'


def _routes():
    try:
        return json.load(open(R + 'config/link-routes.json')).get('brands', {})
    except Exception:
        return {}


def store_host(u):
    h = urllib.parse.urlsplit(u or '').netloc.lower()
    return h[4:] if h.startswith('www.') else h


def route_for(brand, store_url):
    h = store_host(store_url)
    if h.endswith('etsy.com'):
        return 'shopmy-etsy'
    if h.endswith('amazon.com') or h in ('amzn.to', 'a.co'):
        return 'shopmy-amazon'
    row = _routes().get(brand)
    if row:
        return row['route']
    return 'shopmy-site'


def clean_brand(seller):
    return re.sub(r'\s*\(.*$', '', seller or '').split(',')[0].strip()


def add(rec, find, rnd):
    """Adds (or keeps) the tracker entry for a New find she brought in. Returns (entry, is_new)."""
    bi = rec.setdefault('bringins', [])
    for e in bi:
        if e.get('id') == find.get('id') or e.get('store_url') == find.get('url'):
            return e, False
    brand = clean_brand(find.get('seller'))
    e = {'id': find.get('id'), 'mat': find.get('name'), 'brand': brand, 'store': store_host(find.get('url')), 'store_url': find.get('url'),
         'route': route_for(brand, find.get('url')), 'shopmy_link': None, 'shopmy_collection': None, 'amazon_saved': None, 'ops_imported': None,
         'catalog_staged': None, 'round': rnd, 'at': datetime.datetime.now().astimezone().isoformat(timespec='seconds')}
    if e['route'] == 'code-site':
        e['shopmy_link'] = 'n/a (code partner: own store link)'
    bi.append(e)
    return e, True


def missing(e):
    """The steps still open for one bring-in (empty = loop closed)."""
    out = []
    r = e.get('route')
    if r == 'shopmy-amazon':
        if not e.get('amazon_saved'): out.append('saved in the Amazon Associates portal')
        if not e.get('ops_imported'): out.append('Ops imported it into ShopMy')
    if r in ('shopmy-site', 'shopmy-etsy', 'shopmy-amazon') and not e.get('shopmy_link'):
        out.append('ShopMy link (paid link)')
    if not e.get('catalog_staged'):
        out.append('catalog / FYM staging')
    return out


def status(e):
    m = missing(e)
    return 'Brought in: all set (paid link + catalog)' if not m else 'Brought in: waiting on ' + ', '.join(m)


def desk_lines(rec, e):
    d = f"{datetime.date.today():%b %d}"
    lines = [f"- {d} · {rec['name']} album · BRING-IN {e['mat']} ({e['brand']}, {e['store']}, route {e['route']}): close the loop in "
             f"config/album-records/{rec['set']}.json bringins[{e['id']}] (paid link + catalog staging; album_gate --golive fails until done). Owner: Matches & Catalog\n"]
    if e['route'] == 'shopmy-amazon':
        lines.append(f"- {d} · OPS: Amazon mat {e['mat']} saved in the Associates portal? then import to ShopMy ({e['store_url']}); "
                     f"record amazon_saved + ops_imported + shopmy_link in config/album-records/{rec['set']}.json bringins. If the save needs Tiffany "
                     f"(signed out), put ONE HQ needs card: 'Save {e['mat']} in Amazon Associates' (needs-amazon-{e['id']}).\n")
    return lines
