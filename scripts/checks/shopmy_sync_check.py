#!/usr/bin/env python3
"""ShopMy -> Mat Gallery / FYM sync check (Nov 7, after Tiffany: "It doesn't appear that all of my Luna EK studio mats were
brought in ... This needs a cross check").

Reads EVERY collection on her ShopMy (public + private, via the public API, no browser):
  https://api.shopmy.us/api/Users/username/mahjmatchmaker      -> collection list
  https://apiv3.shopmy.us/api/Collections/<id>                 -> pins
picks the MAT pins, and checks each one against
  (a) the Mat Gallery rows the live gallery page loads (site/livepatch/matgallery/matgallery-v7.html data-src -> local data file)
      + config/mat-gallery-dedupe-v6.json merges + config/mat-gallery-photo-holds.json (held = known, not missing)
  (b) the WEBSITE FYM build (newest site-app/fym-vNN/index.html on origin/fym-site-preview). NOT the claude.ai artifact copy and NOT
      config/fym-mats-snapshot.json: the artifact hides adds that don't fit its byte budget ('ahid'), so the snapshot shows
      e.g. all 28 Luna EK Studio mats as hidden although the website app shows them (the Nov 7 false alarm).
  (c) the staged queue: config/fym-*shopmy*.json specs (mats waiting for the next FYM build / gallery sync).
Match order: go.shopmy.us/p-<pin id>, Etsy listing id, Amazon ASIN, store domain + product handle, normalized brand + name.
Not-a-mat pins and decided skips live in config/shopmy-sync-skips.json (pin id -> reason). Everything else that is a mat and is in
neither place FAILS the check.

Usage: python3 scripts/checks/shopmy_sync_check.py [--cache DIR] [--out config/shopmy-crosscheck-<date>.json] [--fym path/index.html]
Exit 0 = PASS (every ShopMy mat is in the gallery and FYM, staged, held or skipped), 1 = FAIL (lists the mats to add).
Runs in the Monday checks (docs/HQ-CLEANUP.md)."""
import sys, os, re, json, subprocess, unicodedata, datetime, time, urllib.request

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
args = sys.argv[1:]
def opt(name, default=None):
    if name in args:
        v = args[args.index(name) + 1]; return v
    return default
CACHE = opt('--cache'); OUT = opt('--out'); FYM = opt('--fym')
USER = 'mahjmatchmaker'

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
    for a in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)
        except Exception as e:  # noqa
            err = e; time.sleep(2 + 3 * a)
    raise err

def load_shopmy():
    if CACHE and os.path.exists(os.path.join(CACHE, 'user.json')):
        u = json.load(open(os.path.join(CACHE, 'user.json')))
    else:
        u = get(f'https://api.shopmy.us/api/Users/username/{USER}')
        if CACHE: os.makedirs(CACHE, exist_ok=True); json.dump(u, open(os.path.join(CACHE, 'user.json'), 'w'))
    cols = []
    for c in u['user']['collections']:
        p = os.path.join(CACHE, 'cols', f"{c['id']}.json") if CACHE else None
        if p and os.path.exists(p): d = json.load(open(p))
        else:
            d = get(f"https://apiv3.shopmy.us/api/Collections/{c['id']}")
            if p: os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(d, open(p, 'w'))
        cols.append((c, d))
    return cols

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'\b(the|mahjong|mahjongg|mahj|mat|mats|game|play|neoprene|non-?slip|tabletop|table|top|with|and|in|of|a)\b', ' ', s)
    return re.sub(r'[^a-z0-9]+', '', s)

def ids(*urls):
    """Identifiers of a product from any of its urls / keys."""
    out = set()
    for u in urls:
        if not u: continue
        u = urllib.request.unquote(urllib.request.unquote(u))
        for m in re.finditer(r'go\.shopmy\.us/p-(\d+)', u): out.add('pin:' + m.group(1))
        for m in re.finditer(r'etsy\.com/(?:[a-z-]+/)?listing/(\d+)', u): out.add('etsy:' + m.group(1))
        for m in re.finditer(r'(?:/dp/|/gp/product/)([A-Z0-9]{10})', u): out.add('asin:' + m.group(1))
        hm = re.match(r'(?:https?://)?(?:www\.)?([a-z0-9.-]+\.[a-z]{2,})/', u)
        if hm:
            for m in re.finditer(r'/products/([a-z0-9-]+)', u): out.add(f'h:{hm.group(1)}/{m.group(1)}')
        m = re.match(r'(?:www\.)?([a-z0-9.-]+\.[a-z]{2,})/([a-z0-9-]+)$', u)  # FYM keys: domain/handle
        if m: out.add(f'h:{m.group(1)}/{m.group(2)}')
    return out

# ---------- mat classification ----------
MAT_COLS = {'Luna EK Studio Mats (Etsy)', 'Rebecca Illustrated Mats', 'Amazon Mahjong Mats', 'Etsy & Amazon Holiday Mats', 'More Mahjong Mats',
            'Collab Mats', 'Retired Mats', 'Mahj & Moon (Etsy)', 'Betty June Jeannette (Etsy)', 'Etsy Mahjong Mats'}
NOT_MAT = re.compile(r'\b(tiles?|racks?|pushers?|shufflers?|tablecloths?|table ?cloth|table cover|bag|tote|pouch|box|case|candle|lamp|coasters?|dish|tray|'
                     r'ornament|sweater|pillow|cups?|print|painting|bundle|edition|set of|holder|folio|trinkets?)\b', re.I)
IS_MAT = re.compile(r'\b(mats?|playmat|play mat|game mat|game surface)\b', re.I)
def is_mat(col, title):
    if NOT_MAT.search(title) and not IS_MAT.search(title): return False
    if re.search(r'tablecloth|table cover|tablemat', title, re.I) and not re.search(r'mahjong mat\b', title, re.I): return False
    return bool(IS_MAT.search(title)) or col in MAT_COLS

def brand_of(pin):
    t = pin['title']; d = (pin.get('domain') or '').lower()
    m = re.match(r'^([A-Z0-9&!\'’ .-]{3,})\s+[|\-–]\s+', t)
    if m and m.group(1).strip().upper() == m.group(1).strip(): return m.group(1).strip().title()
    return {'etsy.com': 'Etsy', 'amazon.com': 'Amazon'}.get(d, d)

def main():
    today = datetime.date.today().isoformat()
    cols = load_shopmy()
    SK = json.load(open(REPO + 'config/shopmy-sync-skips.json')) if os.path.exists(REPO + 'config/shopmy-sync-skips.json') else {}
    skips, same = SK.get('pins', {}), SK.get('same_as', {})
    # ---- gallery rows ----
    html = open(REPO + 'site/livepatch/matgallery/matgallery-v7.html').read()
    src = re.search(r'data-src="[^"]*/(site/livepatch/matgallery/data/matgallery-v\d+\.json)"', html).group(1)
    gver = re.search(r'data-fym="(v\d+)"', html).group(1)
    G = json.load(open(REPO + src))
    dd = json.load(open(REPO + 'config/mat-gallery-dedupe-v6.json')).get('merge', {})
    holds = json.load(open(REPO + 'config/mat-gallery-photo-holds.json')).get('mats', {})
    extra = {r['img']: r for r in json.load(open(REPO + 'config/mat-gallery-extra-rows.json'))['rows']}
    gidx, gname = {}, {}
    for r in G:
        ek = extra.get(r[0], {}).get('key')
        rid = ids(r[3], ek) | {'img:' + r[0]} | ({'key:' + ek} if ek else set())
        for x in rid: gidx[x] = r
        gname[norm(r[2]) + '|' + norm(r[1])] = r; gname.setdefault('*|' + norm(r[1]), r)
    for k, v in dd.items():  # merged twin -> kept row
        if v.get('keep') in {r[0] for r in G}:
            row = next(r for r in G if r[0] == v['keep']); gidx['img:' + k] = row
            if k in extra:
                for x in ids(extra[k].get('url'), extra[k].get('key')): gidx.setdefault(x, row)
    hidx = {}
    for k, v in holds.items():
        for x in ids(k) | {'key:' + k}: hidx[x] = v
    # ---- FYM website build ----
    if FYM: fh = open(FYM).read(); fver = re.search(r'fym-(v\d+)', FYM); fver = fver.group(1) if fver else '?'
    else:
        ls = subprocess.run(['git', '-C', REPO, 'ls-tree', '--name-only', 'origin/fym-site-preview', 'site-app/'], capture_output=True, text=True).stdout.split()
        vs = sorted((int(re.search(r'fym-v(\d+)', x).group(1)), x) for x in ls if re.search(r'fym-v\d+$', x))
        fver = 'v%d' % vs[-1][0]
        fh = subprocess.run(['git', '-C', REPO, 'show', f'origin/fym-site-preview:{vs[-1][1]}/index.html'], capture_output=True, text=True).stdout
    i = fh.index('const D={') + 8; D, _ = json.JSONDecoder().raw_decode(fh[i:]); FM = D['mats']
    fidx, fname = {}, {}
    for k, m in FM.items():
        for x in ids(k, m.get('u'), m.get('u0')) | {'key:' + k}: fidx[x] = (k, m)
        fname[norm(m.get('bn')) + '|' + norm(m.get('n'))] = (k, m); fname.setdefault('*|' + norm(m.get('n')), (k, m))
    flags = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
    # ---- ShopMy link maps kept elsewhere (Mahj & Moon, Tala, ...): pin id -> FYM key / gallery img ----
    alias = {}
    def walk(o, k=None):
        if isinstance(o, dict):
            for kk, vv in o.items(): walk(vv, kk)
        elif isinstance(o, list):
            for vv in o: walk(vv, k)
        elif isinstance(o, str) and k and not k.startswith('_'):
            for m in re.finditer(r'go\.shopmy\.us/p-(\d+)', o): alias.setdefault('pin:' + m.group(1), set()).update({'key:' + k, 'img:' + k})
    for f in sorted(os.listdir(REPO + 'config')):
        if f.endswith('.json') and 'shopmy' in f and not f.startswith('shopmy-crosscheck'):
            d = json.load(open(REPO + 'config/' + f))
            if isinstance(d, dict):
                for k, v in d.items():
                    if isinstance(v, dict) and (v.get('shopmy_url') or v.get('etsy_url')) and not k.startswith('_'):
                        for x in ids(v.get('shopmy_url'), v.get('etsy_url')): alias.setdefault(x, set()).update({'key:' + k, 'img:' + k})
                walk({k: v for k, v in d.items() if k in ('links', 'tiles', 'racks')})
    for r in extra.values():
        for x in ids(r.get('url')):
            alias.setdefault(x, set()).update({'key:' + r.get('key', ''), 'img:' + r['img']})
    # ---- staged queue ----
    staged = {}
    for f in sorted(os.listdir(REPO + 'config')):
        if re.match(r'fym-.*(shopmy|amazon).*\.json$', f):
            for x in json.load(open(REPO + 'config/' + f)).get('mats', []):
                for y in ids(x.get('key'), x.get('u')) | {'key:' + x.get('key', '')}: staged[y] = (f, x)
    rows, seen = [], set()
    for c, d in cols:
        for p in d.get('pins') or []:
            if not is_mat(c['name'], p['title']): continue
            pid = str(p['id']); link = p.get('link') or ''
            my = ids(link) | {'pin:' + pid}
            for x in list(my): my |= alias.get(x, set())
            if pid in same: my |= {'key:' + same[pid]['fym']} | ({'img:' + same[pid]['gallery']} if same[pid].get('gallery') else set())
            skip = skips.get(pid)
            g = next((gidx[x] for x in my if x in gidx), None)
            f = next((fidx[x] for x in my if x in fidx), None)
            st = next((staged[x] for x in my if x in staged), None)
            if st and not g: g = gidx.get('img:' + (st[1].get('img_gallery') or ''), None)
            how = 'id'
            if f and not g:  # FYM key -> gallery row of the same product
                fk_, fm_ = f
                g = next((gidx[x] for x in ids(fk_, fm_.get('u'), fm_.get('u0')) | {'key:' + fk_} if x in gidx), None) or gname.get(norm(fm_.get('bn')) + '|' + norm(fm_.get('n')))
                if g: how = 'fym->gallery'
            if (not g or not f):
                nm = st[1]['name'] if st else re.sub(r'^.*?\s[|]\s', '', p['title']); bn = st[1]['brand'] if st else brand_of(p)
                g2 = gname.get(norm(bn) + '|' + norm(nm)); f2 = fname.get(norm(bn) + '|' + norm(nm))
                if (g2 and not g) or (f2 and not f): how = 'name'
                g = g or g2; f = f or f2
            held = next((hidx[x] for x in my | ({'key:' + st[1]['key']} if st else set()) if x in hidx), None)
            fk, fm = f if f else (None, None)
            hid_reason = ''
            if fm and fm.get('hid'):
                fl = flags.get(fk, {})
                hid_reason = (fl.get('flag', 'hidden') + ': ' + fl.get('note', '')).strip(': ') if fl else 'hidden in build (no photo flag entry)'
            r = dict(collection=c['name'], collection_id=c['id'], private=bool(c.get('private')), pin_id=p['id'],
                     name=(fm or {}).get('n') or (g[1] if g else None) or (st[1]['name'] if st else p['title']),
                     brand=(fm or {}).get('bn') or (g[2] if g else None) or (st[1]['brand'] if st else brand_of(p)),
                     shopmy_title=p['title'], shopmy_link=f"https://go.shopmy.us/p-{p['id']}", product_url=link.split('?')[0],
                     in_gallery=bool(g), gallery_img=g[0] if g else None, gallery_held=(held or {}).get('reason') if (held and not g) else None,
                     in_fym=bool(f), fym_key=fk, fym_hidden=bool(fm and fm.get('hid')), fym_hidden_reason=hid_reason,
                     staged=st[0] if st else None, skip=skip, match=how if (g or f) else None)
            amazon = (p.get('domain') or '').endswith('amazon.com')
            qst = bool(fm and fm.get('hid') and flags.get(fk, {}).get('flag') in ('questionable', 'too_far', 'covered'))
            r['amazon'] = amazon
            r['status'] = ('skip' if skip else
                           'ok' if (g and f and not (fm or {}).get('hid')) else
                           'fym-questionable' if (qst and not g) else          # photo failed the FYM bar: hidden + on her Questionable list
                           'ok-hidden' if (g and f) else
                           'staged' if (st and not f) else                    # in a pending spec, waiting for the next FYM build
                           'held-gallery' if (f and held and not g) else       # gallery photo hold (config/mat-gallery-photo-holds.json)
                           'gallery-next-sync' if (f and not g and not fm.get('hid')) else  # visible in FYM; gallery_sync.py adds it at the next release
                           # (Amazon pins are no longer 'her pick': Tiffany Nov 8 2:08pm "if it's in ShopMy, bring it in")
                           'missing')
            rows.append(r)
    from collections import Counter, defaultdict
    per = defaultdict(Counter)
    for r in rows:
        per[r['collection']]['mats'] += 1
        per[r['collection']]['in_gallery'] += r['in_gallery']; per[r['collection']]['in_fym'] += r['in_fym']
        per[r['collection']]['fym_hidden'] += r['fym_hidden']; per[r['collection']][r['status']] += 1
    missing = [r for r in rows if r['status'] == 'missing']
    amz = sorted({(r['pin_id'], r['collection'], r['shopmy_title'][:70]) for r in rows if r['status'] == 'amazon-her-pick'})
    nxt = [r for r in rows if r['status'] == 'gallery-next-sync']
    rep = dict(_about='ShopMy mat cross-check (scripts/checks/shopmy_sync_check.py). One row per ShopMy mat pin (a mat pinned in 2 collections shows twice).',
               run=today, gallery=src, gallery_fym=gver, fym_build=fver,
               counts=dict(collections=len(cols), pins=sum(len(d.get('pins') or []) for _, d in cols), mat_pins=len(rows),
                           unique_mats=len({r['pin_id'] for r in rows})),
               per_collection={k: dict(v) for k, v in sorted(per.items())},
               missing=[{k: r[k] for k in ('collection', 'brand', 'name', 'shopmy_link', 'in_gallery', 'in_fym', 'staged')} for r in missing],
               amazon_her_pick=[{'pin_id': a, 'collection': b, 'title': c, 'shopmy_link': f'https://go.shopmy.us/p-{a}'} for a, b, c in amz],
               gallery_next_sync=[{k: r[k] for k in ('collection', 'brand', 'name', 'fym_key')} for r in nxt],
               mats=rows)
    if OUT: json.dump(rep, open(OUT, 'w'), indent=1, ensure_ascii=False)
    print(f"ShopMy: {rep['counts']['collections']} collections, {rep['counts']['pins']} pins, {len(rows)} mat pins; gallery {src.split('/')[-1]} (fym {gver}), FYM website {fver}")
    for k, v in sorted(per.items()): print(f'  {k}: ' + ', '.join(f'{a} {b}' for a, b in v.items()))
    for r in missing: print(f"  MISSING ({'gallery' if not r['in_gallery'] else ''}{'+' if not r['in_gallery'] and not r['in_fym'] else ''}{'FYM' if not r['in_fym'] else ''}): {r['collection']} | {r['brand']} | {r['name']} | {r['shopmy_link']}")
    if nxt: print(f"  gallery-next-sync: {len(nxt)} visible FYM mats not in the staged gallery yet (gallery_sync.py adds them at the next FYM release; gate [159b])")
    if amz: print(f"  AMAZON, her pick ({len(amz)} pins not in FYM; Amazon never auto-enters FYM): list in the report's amazon_her_pick")
    print('PASS' if not missing else f'FAIL: {len(missing)} ShopMy mat pins missing from the gallery and/or FYM (add them, or put the pin in config/shopmy-sync-skips.json with a reason)')
    return 0 if not missing else 1

if __name__ == '__main__':
    sys.exit(main())
