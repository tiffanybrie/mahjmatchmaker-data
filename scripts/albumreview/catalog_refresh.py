"""Album Playbook step 4a: CATALOG UP TO DATE BEFORE THE PULL (Tiffany Nov 8 1:33pm: "If I just added new mats to ShopMy there
is a good chance they won't be browsed for matching").

Usage: python3 scripts/albumreview/catalog_refresh.py <set> [--no-network]
 1. ShopMy: scripts/checks/shopmy_sync_check.py over EVERY collection (public + private) -> config/shopmy-crosscheck-<date>.json.
    New = mat pins in neither the Mat Gallery nor the website FYM build nor a staged queue ('missing'), plus her Amazon pins
    ('amazon-her-pick': for albums her own Amazon pins count as her picks).
 2. Partner stores: builder/partner_mat_sweep.py (products.json on every partner Shopify store vs the newest website FYM build)
    -> config/partner-mat-sweep.json. New = 'missing' mats not in config/partner-mat-sweep-ignore.json and not already staged.
 3. Every new mat gets its photo (assets/albums/catalog-new/<slug>.jpg) and measured colour shares (scripts/colors/families.py
    rules), goes straight into the album's candidate pool (record pool.new_candidates; pool.pulled_at = now), and is staged
    for the next FYM release: config/fym-shopmy-catalog-refresh-<date>.json (ShopMy + Amazon; shopmy_sync_check reads it as
    staged) and config/fym-partner-adds-<date>.json (partner stores). Staged rows are hid:false; the FYM photo flags still
    decide visibility at build time.
 4. Writes record catalog_checked {at, shopmy_new, partner_new, added:[...]}. album_gate [4a] fails unless catalog_checked is
    from the same day as pool.pulled_at and not after it.
The by-sight check then judges the new candidates for this album (cards or Left out with a reason)."""
import json, os, re, sys, subprocess, datetime, urllib.request, io
import numpy as np
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'scripts/colors')
from families import fam_arr
SET = sys.argv[1]
NOW = datetime.datetime.now().astimezone()
D8 = NOW.strftime('%b%d').lower()  # nov08
HOL = re.compile(r'christmas|hanukkah|chanukah|menorah|dreidel|snow|ski\b|apres|winter|holiday|noel|merry|santa|reindeer|nutcracker|holly|wreath|jingle|yule|gingerbread|candy cane|ornament|mistletoe|tartan', re.I)


def slug(s): return re.sub(r'[^a-z0-9]+', '-', (s or '').lower().replace('&', 'and').replace("'", '')).strip('-')[:80]


def get(url, js=True):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json' if js else '*/*'})
    with urllib.request.urlopen(req, timeout=40) as r:
        b = r.read()
    return json.loads(b) if js else b


def measure(im, N=96):
    a = np.asarray(im.convert('RGB').resize((N, N))).astype(float) / 255
    f, h, l, s = fam_arr(a)
    low = ((f == 'orange') & (s < 0.45)) | (np.isin(f, ['yellow', 'gold']) & (s < 0.5))
    f = np.where(low, np.where(l >= 0.75, 'neutral', 'earthy'), f)
    f = np.where(f == 'gold', np.where(l < 0.45, 'earthy', 'yellow'), f)
    f = np.where((f == 'teal') & (h < 180), 'green', f).ravel()
    keep = ~np.isin(f, ['white', 'black']); vals, cnt = np.unique(f[keep], return_counts=True); t = cnt.sum() or 1
    sh = {str(v): round(100.0 * c / t, 1) for v, c in zip(vals, cnt)}
    return dict(sorted(sh.items(), key=lambda x: -x[1]))


def photo(url, name):
    os.makedirs(R + 'assets/albums/catalog-new', exist_ok=True)
    p = f'assets/albums/catalog-new/{name}.jpg'
    m = re.match(r'https://production-shopmyshelf-pins\.s3[^/]*/(.+)$', url or '')
    if m: url = 'https://static.shopmy.us/pins/' + m.group(1)  # the raw S3 bucket answers 403; the CDN serves the same file
    if not os.path.exists(R + p):
        im = Image.open(io.BytesIO(get(url, js=False))).convert('RGB'); im.thumbnail((1600, 1600)); im.save(R + p, quality=90)
    im = Image.open(R + p)
    return p, measure(im), im.size


def shopmy_new():
    cache = f'/tmp/shopmy-cache-{D8}'
    out = f'config/shopmy-crosscheck-{D8}.json'
    r = subprocess.run(['python3', R + 'scripts/checks/shopmy_sync_check.py', '--cache', cache, '--out', R + out], capture_output=True, text=True, cwd=R)
    print(r.stdout.strip().splitlines()[0] if r.stdout.strip() else r.stderr[-400:])
    rep = json.load(open(R + out))
    pins = {}
    u = json.load(open(f'{cache}/user.json'))
    for c in u['user']['collections']:
        d = json.load(open(f"{cache}/cols/{c['id']}.json"))
        for p in d.get('pins') or []: pins[p['id']] = p
    new = []
    for m in rep['mats']:
        if m['status'] not in ('missing', 'amazon-her-pick'): continue
        p = pins.get(m['pin_id'], {})
        img = p.get('image') or p.get('image_url') or p.get('imageUrl')
        new.append({'source': 'ShopMy · ' + m['collection'], 'name': m['name'], 'brand': m['brand'], 'link': m['shopmy_link'],
                    'product_url': m.get('product_url'), 'shopmy_id': m['pin_id'], 'img_url': img, 'amazon_her_pick': bool(m.get('amazon')),
                    'status': m['status']})
    return new, out


def partner_new():
    r = subprocess.run(['python3', R + 'builder/partner_mat_sweep.py'], capture_output=True, text=True, cwd=R)
    print((r.stdout.strip().splitlines() or [r.stderr[-300:]])[0])
    sw = json.load(open(R + 'config/partner-mat-sweep.json'))
    ign = set(json.load(open(R + 'config/partner-mat-sweep-ignore.json')).get('items', {}))
    staged = set()
    for f in os.listdir(R + 'config'):
        if re.match(r'fym-partner-adds-.*\.json$', f):
            d = json.load(open(R + 'config/' + f))
            for x in (d.get('mats', []) if isinstance(d, dict) else d):
                if isinstance(x, dict) and not str(x.get('added_by', '')).startswith('catalog_refresh'): staged |= {x.get('key', ''), x.get('handle', '')}
    new = []
    for dom, v in sw['stores'].items():
        base = re.sub(r'^(www\.|shop\.)', '', dom)
        for pub, title, handle in v.get('missing', []):
            key = f'{base}/{handle}'
            if key in ign or key in staged or handle in staged: continue
            new.append({'source': 'Partner store · ' + v.get('brand', dom), 'name': title, 'brand': v.get('brand', dom), 'link': f'https://{dom}/products/{handle}',
                        'product_url': f'https://{dom}/products/{handle}', 'key': key, 'published': pub, 'dom': dom, 'handle': handle})
    return new, sw.get('swept_at')


def main():
    rec_p = R + f'config/album-records/{SET}.json'; rec = json.load(open(rec_p))
    sm, smfile = shopmy_new()
    pn, swept = partner_new()
    added, stage_sm, stage_pa, problems, amz = [], [], [], [], []
    for m in sm + pn:
        try:
            url = m.get('img_url')
            if not url and m.get('dom'):
                pj = get(f"https://{m['dom']}/products/{m['handle']}.json")['product']; url = (pj.get('images') or [{}])[0].get('src')
                m['name'] = pj.get('title', m['name'])
            if not url: problems.append(f"{m['brand']} | {m['name']}: no photo"); continue
            nm = slug(m['brand']) + '--' + slug(m['name'])
            p, sh, size = photo(url, nm)
        except Exception as e:
            problems.append(f"{m['brand']} | {m['name']}: {str(e)[:80]}"); continue
        hol = bool(HOL.search(m['name']))
        row = {'name': m['name'], 'brand': m['brand'], 'img': p, 'colours': sh, 'holiday_guess': hol, 'source': m['source'],
               'link': m['link'], 'product_url': m.get('product_url'), 'lowres': max(size) < 800}
        if m.get('amazon_her_pick'): row['amazon_her_pick'] = True
        added.append(row)
        st = {'key': m.get('key') or (m.get('product_url') or m['link']).split('://')[-1].replace('www.', ''), 'name': m['name'], 'brand': m['brand'],
              'u': m['link'], 'product_url': m.get('product_url'), 'img': p, 'src': url, 'hol': hol, 'hid': False, 'reason': '',
              'colours': sh, 'added_by': f'catalog_refresh {SET} {NOW.isoformat(timespec="minutes")}'}
        if m.get('shopmy_id'): st['shopmy_id'] = m['shopmy_id']
        if m.get('amazon_her_pick'): st['b'] = 'Amazon'; st['note'] = "Her own Amazon ShopMy pin: staged for FYM on her Nov 8 2:08pm yes; counts as her pick for albums"
        (stage_sm if m.get('shopmy_id') else stage_pa).append(st)  # Tiffany Nov 8 2:08pm: "if it's in ShopMy, bring it in" (Amazon pins too)
    if stage_sm:
        json.dump({'_note': f'Catalog refresh {NOW:%b %d %H:%M}: ShopMy mat pins not yet in the gallery/FYM (incl. her Amazon pins), staged for the next FYM release by scripts/albumreview/catalog_refresh.py. Photo flags decide visibility at build time.',
                   'mats': stage_sm}, open(R + f'config/fym-shopmy-catalog-refresh-{D8}.json', 'w'), indent=1, ensure_ascii=False)
    if stage_pa:
        json.dump({'_note': f'Catalog refresh {NOW:%b %d %H:%M}: partner-store mats not in the website FYM build (builder/partner_mat_sweep.py), staged for the next FYM release.',
                   'mats': stage_pa}, open(R + f'config/fym-partner-adds-{D8}.json', 'w'), indent=1, ensure_ascii=False)
    pool = rec.setdefault('pool', {})
    old = {(x['brand'], x['name']) for x in pool.get('new_candidates', [])}
    pool['new_candidates'] = pool.get('new_candidates', []) + [a for a in added if (a['brand'], a['name']) not in old]
    pool['pulled_at'] = NOW.isoformat(timespec='seconds')
    base = pool.get('size_fym', pool.get('size', 0)); pool['size_fym'] = base; pool['size'] = base + len(pool['new_candidates'])
    src = 'New since the last FYM build: ShopMy (every collection, incl. her Amazon pins) + partner-store sweep'
    if src not in pool.get('sources', []): pool.setdefault('sources', []).append(src)
    rec['catalog_checked'] = {'at': NOW.isoformat(timespec='seconds'), 'shopmy_new': len(sm), 'partner_new': len(pn),
                              'added': [f"{a['brand']} · {a['name']}" for a in pool['new_candidates']], 'problems': problems,
                              'reports': [smfile, 'config/partner-mat-sweep.json'], 'partner_swept_at': swept}
    json.dump(rec, open(rec_p, 'w'), indent=1, ensure_ascii=False)
    print(f"CATALOG CHECKED {SET}: ShopMy new {len(sm)}, partner new {len(pn)}, added to the pool {len(added)}; problems {len(problems)}")
    for x in problems: print('  ' + x)


if __name__ == '__main__':
    main()
