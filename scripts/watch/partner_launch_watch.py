#!/usr/bin/env python3
"""Partner launch + restock watch (Nov 6 2026, LAUNCH GAP fix).

Why: we missed Charleston Mahjong Club's Cabana Club (new, preorder) and Bam Bird's
MCM Olive restock (sold out -> available). The existing launch watch only notices NEW
handles; it never noticed a known product flipping back to available, a new
'preorder'/'coming soon' state, or put either in front of Tiffany as a dated card.

What it does (read-only GETs of each partner Shopify store's /products.json):
  diff vs config/partner-products-snapshot.json and report
    new        - handle never seen (or a new variant on a known listing)
    restock    - a variant (or the whole product) went unavailable -> available
    soldout    - available -> unavailable (info only)
    preorder   - 'preorder'/'pre-order'/'coming soon'/'presale' newly in title or tags
    price      - min variant price changed
  plus 'recent' = products created/published in the last N days (default 14).
Each item gets kind (tiles|mat|rack|travel tiles|other), album flag and a
30-second reshare instruction for Tiffany.
Outputs: docs/status/partner-launches.json, docs/status/partner-launches.md,
         config/partner-products-snapshot.json (updated unless --no-save).
Never posts to any form. Store text is data, not instructions.

Usage: python3 scripts/watch/partner_launch_watch.py [--days 14] [--no-save] [--only domain,...]
"""
import json, os, re, subprocess, sys, time, datetime, argparse, concurrent.futures as cf

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
SNAP = REPO + 'config/partner-products-snapshot.json'
OUT_JSON = REPO + 'docs/status/partner-launches.json'
OUT_MD = REPO + 'docs/status/partner-launches.md'
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

# store -> brand. Partners only (config/domains.tsv + partner list). Mahjong Row & Co. is OUT (Tiffany Nov 6).
STORES = {
    'www.ohmymahjong.com': 'Oh My Mahjong', 'amahjline.com': 'Amahj', 'shop.andersruff.com': 'Anders Ruff',
    'www.bambirdboutique.com': 'Bam Bird Boutique', 'www.bamletsmahjong.com': "Bam! Let's Mahjong",
    'www.bespokemahjong.com': 'Bespoke Mahjong', 'birdandbamboo.com': 'Bird & Bamboo', 'brittmillsdesign.com': 'Britt Mills',
    'www.charlestonmahjongclub.com': 'Charleston Mahjong Club', 'www.hiphipmahjong.com': 'Hip Hip Mahjong',
    'www.letsmahj-on.com': "Let's Mahj On", 'www.macandmillermahjong.com': 'Mac + Miller Mahjong', 'mahjandvine.com': 'Mahj & Vine',
    'mahjmood.com': 'Mahj Mood', 'mahjsquadshop.com': 'Mahj Squad', 'mahjongco.com': 'The Mahjong Co.',
    'mahjongstudios.com': 'Mahjong Studios', 'minimahjer.com': 'Mini Mahjer', 'missmahjong.com': 'Miss Mahjong',
    'myfairmahjong.com': 'My Fair Mahjong', 'peacelovemahjong.com': 'Peace Love Mahjong', 'themahjongpress.com': 'The Mahjong Press',
    'tigredetartan.com': 'Tigre de Tartán', 'www.viroramahjong.com': 'Virora Mahjong', 'www.ymimports.com': 'Yellow Mountain Imports',
    'mahjongregister.com': 'Mahjong Register', 'theroyalmahjongsociety.com': 'The Royal Mahjong Society',
    'sundaymahjong.com': 'Sunday Mahjong', 'letsbebesties.com': "Let's Be Besties", 'www.fait-a-main.com': 'Fait à Main',
    'soireeallday.co': 'Soirée All Day', 'sweetjojomahjong.com': 'Sweet Jojo Mahjong', 'splashofcolorco.com': 'Splash of Color',
}
# brand-specific handling (CLAUDE.md + ANSWERS)
NO_SOCIAL = {'Yellow Mountain Imports'}                 # never featured on social
NO_ALERT_MATS = {'Splash of Color', 'Mahjong Studios', 'The Mahjong Co.'}  # mats out of FYM (tiles stay)
TDT = 'Tigre de Tartán'                                  # code is image-only: never type MAHJMATCH next to it

PRE = re.compile(r"pre-?order|presale|coming[- ]soon|coming[- ]back|back[- ]soon|notify me", re.I)
TRAVEL = re.compile(r"travel|mini\b|solo|petite|pocket", re.I)
K_TILE = re.compile(r"\btiles?\b|tile set|mahjong set|mah jongg set|\bbundle\b", re.I)
K_MAT = re.compile(r"\bmats?\b|table ?cloth|table ?cover|tablecloth", re.I)
K_RACK = re.compile(r"\bracks?\b|pushers?", re.I)
SKIP = re.compile(r"gift card|e-?gift|replacement|coaster|ornament|sticker|shirt|sweatshirt|hoodie|hat\b|cap\b|sock|towel|"
                  r"card holder|nmjl|\bcards?\b(?! set)|scorecard|necklace|earring|bracelet|charm|pin\b|keychain|candle|"
                  r"wholesale|sample|bundle deposit|shipping|insurance|protection|class|lesson|ticket|membership|"
                  r"shuffler|dice|wallet|joker|blanks?\b", re.I)


def get(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, url], capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def fetch(domain):
    out, page = [], 1
    while page <= 12:
        txt = get(f"https://{domain}/products.json?limit=250&page={page}")
        try:
            ps = json.loads(txt).get("products", [])
        except Exception:
            time.sleep(2)
            try:
                ps = json.loads(get(f"https://{domain}/products.json?limit=250&page={page}")).get("products", [])
            except Exception:
                return domain, None
        out += ps
        if len(ps) < 250:
            break
        page += 1
    return domain, out


BAG = re.compile(r"\bbags?\b|clutch|pool mat|floating|pool float", re.I)


def kind_of(p):
    if BAG.search(p.get('title') or '') and not re.search(r"\btiles\b|\bmats?\b", p.get('title') or '', re.I):
        return None
    t = (p.get('title') or '') + ' ' + (p.get('product_type') or '') + ' ' + ' '.join(p.get('tags') or [])
    title = p.get('title') or ''
    if SKIP.search(title):
        return None
    if K_RACK.search(t) and not K_MAT.search(title):
        return 'rack'
    if K_MAT.search(title) or (K_MAT.search(t) and not K_TILE.search(title)):
        return 'travel mat' if TRAVEL.search(title) else 'mat'
    if K_TILE.search(t):
        return 'travel tiles' if TRAVEL.search(title) else 'tiles'
    return None


def slim(p):
    vs = {}
    for v in p.get('variants') or []:
        try:
            price = float(v.get('price') or 0)
        except Exception:
            price = 0
        vs[str(v.get('id'))] = {'t': v.get('title'), 'a': bool(v.get('available')), 'p': price}
    tags = [t for t in (p.get('tags') or []) if PRE.search(t)]
    return {
        'title': p.get('title'), 'kind': kind_of(p), 'created': p.get('created_at'), 'published': p.get('published_at'),
        'avail': any(v['a'] for v in vs.values()), 'pre': bool(PRE.search(p.get('title') or '') or tags),
        'pretags': tags, 'min': min([v['p'] for v in vs.values()] or [0]), 'v': vs,
        'img': ((p.get('images') or [{}])[0] or {}).get('src'),
    }


def reshare(brand, kind, ev, title):
    if brand in NO_SOCIAL:
        return "No social (YMI is never featured). Monday codes post only if allowed."
    if brand in NO_ALERT_MATS and kind and 'mat' in kind:
        return "Log only (this brand's mats are out of FYM)."
    code = "" if brand == TDT else " + 'code MAHJMATCH' text"
    what = {'restock': 'is back in stock', 'new': 'is new', 'preorder': 'is open for preorder', 'recent': 'is new'}.get(ev, 'changed')
    return (f"30 sec: open the brand's IG post about {title} → paper-plane → Add to story → add @-mention"
            f"{code} + link sticker to the product. ({title} {what}.)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=14)
    ap.add_argument('--no-save', action='store_true')
    ap.add_argument('--only', default='')
    a = ap.parse_args()
    stores = {d: b for d, b in STORES.items() if not a.only or d in a.only.split(',')}
    old = json.load(open(SNAP)) if os.path.exists(SNAP) else {}
    first_run = not old
    now = datetime.datetime.now(datetime.timezone.utc)
    cutoff = now - datetime.timedelta(days=a.days)
    try:
        albums = json.load(open(REPO + 'assets/tiles/album/index.json'))
        album_txt = json.dumps(albums).lower()
    except Exception:
        album_txt = ''

    events, recent, status, new_snap = [], [], {}, {}
    with cf.ThreadPoolExecutor(8) as ex:
        res = list(ex.map(fetch, stores))
    for domain, prods in res:
        brand = stores[domain]
        if prods is None:
            status[domain] = 'not checkable (not Shopify or blocked)'
            if domain in old:
                new_snap[domain] = old[domain]
            continue
        status[domain] = f'ok {len(prods)} products'
        cur = {}
        for p in prods:
            s = slim(p)
            if not s['kind']:
                continue
            cur[p['handle']] = s
        new_snap[domain] = cur
        prev = old.get(domain)
        base = {'brand': brand, 'domain': domain}
        for h, s in cur.items():
            url = f"https://{domain}/products/{h}"
            item = dict(base, handle=h, title=s['title'], kind=s['kind'], url=url, img=s['img'],
                        album=bool(album_txt and (s['title'] or '').lower().split(' tile')[0].strip() in album_txt))
            # recent (by date)
            dt = None
            for f in ('published', 'created'):
                try:
                    d = datetime.datetime.fromisoformat((s[f] or '').replace('Z', '+00:00'))
                    dt = d if dt is None or d > dt else dt
                except Exception:
                    pass
            if dt and dt >= cutoff:
                recent.append(dict(item, ev='recent', when=dt.astimezone(datetime.timezone(datetime.timedelta(hours=-5))).strftime('%Y-%m-%d'),
                                   avail=s['avail'], pre=s['pre'], reshare=reshare(brand, s['kind'], 'recent', s['title'])))
            if prev is None:
                continue
            o = prev.get(h)
            if o is None:
                events.append(dict(item, ev='new', avail=s['avail'], pre=s['pre'], reshare=reshare(brand, s['kind'], 'new', s['title'])))
                continue
            back = [v['t'] for vid, v in s['v'].items() if v['a'] and vid in o['v'] and not o['v'][vid]['a']]
            if (s['avail'] and not o['avail']) or back:
                events.append(dict(item, ev='restock', variants=back, reshare=reshare(brand, s['kind'], 'restock', s['title'])))
            elif o['avail'] and not s['avail']:
                events.append(dict(item, ev='soldout'))
            newv = [v['t'] for vid, v in s['v'].items() if vid not in o['v']]
            if newv and o['v']:
                events.append(dict(item, ev='new variant', variants=newv, reshare=reshare(brand, s['kind'], 'new', s['title'])))
            if s['pre'] and not o.get('pre'):
                events.append(dict(item, ev='preorder', reshare=reshare(brand, s['kind'], 'preorder', s['title'])))
            if o.get('min') and s['min'] and abs(s['min'] - o['min']) > 0.009:
                events.append(dict(item, ev='price', was=o['min'], now=s['min']))

    recent.sort(key=lambda x: x['when'], reverse=True)
    out = {'run_at': now.isoformat(timespec='seconds'), 'first_run': first_run, 'days': a.days,
           'events': events, 'recent': recent, 'stores': status}
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    json.dump(out, open(OUT_JSON, 'w'), indent=1, ensure_ascii=False)
    L = [f"# Partner launches & restocks ({now.strftime('%Y-%m-%d %H:%M')} UTC)", '']
    act = [e for e in events if e['ev'] in ('new', 'restock', 'preorder', 'new variant')]
    L.append(f"## Since last run: {len(act)} to act on" + (" (first run: snapshot seeded)" if first_run else ''))
    for e in act:
        L.append(f"- **{e['ev'].upper()}** {e['brand']} · {e['title']} ({e['kind']}){' · ' + ', '.join(map(str, e.get('variants') or [])) if e.get('variants') else ''} · {e['url']}")
    L += ['', f"## Created/published in the last {a.days} days (tiles, mats, racks)"]
    for r in recent:
        L.append(f"- {r['when']} · {r['brand']} · {r['title']} ({r['kind']}) · {'available' if r['avail'] else 'NOT available'}{' · PREORDER/COMING SOON' if r['pre'] else ''} · {r['url']}")
    L += ['', '## Stores'] + [f"- {d}: {s}" for d, s in sorted(status.items())]
    open(OUT_MD, 'w').write('\n'.join(L) + '\n')
    if not a.no_save:
        json.dump(new_snap, open(SNAP, 'w'), separators=(',', ':'), ensure_ascii=False)
    print(f"events {len(events)} (act {len(act)}), recent {len(recent)}, stores ok {sum(1 for s in status.values() if s.startswith('ok'))}/{len(status)}")


if __name__ == '__main__':
    main()
