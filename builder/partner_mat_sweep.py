"""Partner store mat sweep (Tiffany Oct 27 2:21am: "This is going to get very old, me chasing down mats").
Scans every PARTNER Shopify store in config/launch-watch-seen.json (+ EXTRA_STORES) via /products.json, keeps the FULL-SIZE
mahjong mats (no travel / mini / solo / practice / floating / pool mats, no bags / tubes / straps / sleeves / caddies / totes,
no art prints / calendars / needlepoint, no wholesale lots) and writes config/partner-mat-sweep.json:
  swept_at, fym_ref (the FYM build compared against), stores{domain: {brand, status, products, mats:[[published, title, handle]],
  missing:[...]}}.  'missing' = mats not found in that FYM build (key, u or u0 -> domain/handle).
Run by the twice-daily LAUNCH WATCH scheduled task after it checks new products (Tiffany Oct 27 2:26am: no scanning per build,
no new scheduled task). The FYM gate [100] only READS this file (no network): it FAILS on a full-size partner mat published
> 2 days ago that is neither in the build being gated nor in config/partner-mat-sweep-ignore.json (with a reason), and WARNS
when this file is older than 3 days.
Usage: python3 builder/partner_mat_sweep.py [--fym <index.html>]   (default FYM = newest site-app/fym-vNN on origin/fym-site-preview)"""
import json, os, re, sys, subprocess, time, urllib.request, urllib.parse, datetime
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
BRAND = {  # store domain -> brand name used in FYM / the partner list (builder/fym_flags/nonpartner_allow.json 'partners')
    'amahjline.com': 'Amahj', 'bambirdboutique.com': 'Bam Bird Boutique', 'bamletsmahjong.com': "Bam! Let's Mahjong",
    'bespokemahjong.com': 'Bespoke Mahjong', 'birdandbamboo.com': 'Bird & Bamboo', 'brittmillsdesign.com': 'Britt Mills',
    'charlestonmahjongclub.com': 'Charleston Mahjong Club', 'hiphipmahjong.com': 'Hip Hip Mahjong', 'letsmahj-on.com': "Let's Mahj On",
    'macandmillermahjong.com': 'Mac + Miller Mahjong', 'mahjandvine.com': 'Mahj & Vine', 'mahjmood.com': 'Mahj Mood',
    'mahjongco.com': 'Mahjong Co.', 'mahjongregister.com': 'Mahjong Register', 'mahjongrowandco.com': 'Mahjong Row & Co.',
    'mahjongstudios.com': 'Mahjong Studios', 'mahjsquadshop.com': 'Mahj Squad', 'middleandmainmahjong.com': 'Middle & Main Mahjong',
    'minimahjer.com': 'Mini Mahjer', 'missmahjong.com': 'Miss Mahjong', 'myfairmahjong.com': 'My Fair Mahjong',
    'ohmymahjong.com': 'Oh My Mahjong', 'peacelovemahjong.com': 'Peace Love Mahjong', 'shop.andersruff.com': 'Anders Ruff',
    'soireeallday.co': 'Soirée All Day', 'splashofcolorco.com': 'Splash of Color', 'sundaymahjong.com': 'Sunday Mahjong',
    'themahjongpress.com': 'The Mahjong Press', 'theroyalmahjongsociety.com': 'The Royal Mahjong Society', 'tigredetartan.com': 'Tigre de Tartan',
    'viroramahjong.com': 'Virora Mahjong', 'wrenmats.com': 'Wren Mats', 'ymimports.com': 'Yellow Mountain Imports',
    'amandatoppeart.com': 'Amanda Toppe', 'ilovemahj.com': 'I Love Mahj', 'letsbebesties.com': "Let's Be Besties", 'faitamainstudio.com': 'Fait à Main'}
EXTRA_STORES = ['letsbebesties.com', 'faitamainstudio.com']  # partner stores not (yet) in the launch watch list
# partners whose mats are OUT of FYM by Tiffany's own decision: not swept (Coordinator relay of Tiffany, Oct 27 2:25am)
EXCLUDED = {'splashofcolorco.com': "partner, pulled from FYM by her Oct 26 decision (too many mats); only her album-match Splash mats stay",
            'mahjongstudios.com': "partner, every Mahjong Studios mat is out of FYM + the Mat Gallery by her Oct 20 22:31 decision (tiles/racks stay)"}
MAT = re.compile(r'\bmats?\b|\bplaymat\b', re.I)
NOT_FULL = re.compile(r'\b(travel|mini|solo|practice|floating|pool|poolside|umbrella|sample|wholesale|odd lots|less than perfect)\b', re.I)
ACCESSORY = re.compile(r'\bmats?\s*(bag|bags|tube|tubes|storage|strap|straps|sleeve|sleeves|caddy|band|holder|tote|case|carrier)\b|'
                       r'^(the\s+)?(clear\s+)?(mahj(ong)?\s+)?(game\s+)?(mat\s+)?(storage\s+)?(tube|bag|strap|sleeve|caddy|tote)\b|'
                       r'\b(storage tube|mat caddy|rack bag|crossbody|art print|calendar|calendars|needlepoint|coaster|placemat|gift card|bundle only|'
                       r'desk mat|bath mat|pet food mat|mouse ?pad|mat art|yoga|door ?mat|bar mat)\b|'
                       r'\bfor tdt mat bag\b', re.I)
OUT = REPO + 'config/partner-mat-sweep.json'


def get(url, tries=3):
    for k in range(tries):
        try:
            rq = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (mahjmatchmaker partner sweep)'})
            return json.load(urllib.request.urlopen(rq, timeout=40))
        except Exception as e:
            err = e; time.sleep(2 + 3 * k)
    raise err


def products(dom):
    out, page = [], 1
    try: get(f'https://{dom}/products.json?limit=1', tries=1)
    except Exception:
        if not dom.startswith('www.'): dom = 'www.' + dom  # e.g. middleandmainmahjong.com only answers on www.
    while page < 30:
        d = get(f'https://{dom}/products.json?limit=250&page={page}')
        ps = d.get('products', [])
        out += ps
        if len(ps) < 250: break
        page += 1
    return out


def is_full_mat(p):
    t = p.get('title', ''); pt = p.get('product_type', '') or ''
    if not MAT.search(t): return False  # title only (a 'Mats' product_type also covers bags/tubes)
    if re.search(r'\b(tile|tiles|rack|racks|pushers?)\b', t, re.I) and not MAT.search(t): return False
    if NOT_FULL.search(t) or ACCESSORY.search(t): return False
    return True


def nu(u):  # same normaliser as gate [90]/[100]: /discount/CODE?redirect=/products/x -> domain/x
    u = str(u or '')
    if '/discount/' in u and 'redirect=' in u:
        u = re.sub(r'^(https?://[^/]+).*$', r'\1', u) + urllib.parse.unquote(u.split('redirect=', 1)[1].split('&')[0])
    u = re.sub(r'^https?://', '', u.split('?')[0].split('#')[0]).rstrip('/').replace('/products/', '/')
    return re.sub(r'^(www\.|shop\.)', '', u)


def fym_index(D):
    s = set()
    for k, m in D['mats'].items():
        for u in (k, m.get('u'), m.get('u0')):
            if u: s.add(nu(u))
    return s


def load_fym(path):
    if path: h = open(path).read(); ref = path
    else:
        subprocess.run(['git', '-C', REPO, 'fetch', '-q', 'origin', 'fym-site-preview'], check=False)
        ls = subprocess.run(['git', '-C', REPO, 'ls-tree', '--name-only', 'origin/fym-site-preview', 'site-app/'], capture_output=True, text=True).stdout.split()
        v = max((x for x in ls if re.search(r'fym-v\d+$', x)), key=lambda x: int(re.search(r'(\d+)$', x).group(1)))
        h = subprocess.run(['git', '-C', REPO, 'show', f'origin/fym-site-preview:{v}/index.html'], capture_output=True, text=True).stdout; ref = 'origin/fym-site-preview:' + v
    i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:]); return D, ref


def main():
    fym = sys.argv[sys.argv.index('--fym') + 1] if '--fym' in sys.argv else None
    D, ref = load_fym(fym); have = fym_index(D)
    partners = set(json.load(open(REPO + 'builder/fym_flags/nonpartner_allow.json'))['partners'])
    stores = list(json.load(open(REPO + 'config/launch-watch-seen.json')).keys()) + [s for s in EXTRA_STORES]
    res = {}
    for dom in dict.fromkeys(stores):
        brand = BRAND.get(dom, dom)
        if dom in EXCLUDED: res[dom] = {'brand': brand, 'status': 'excluded: ' + EXCLUDED[dom]}; continue
        if brand not in partners: res[dom] = {'brand': brand, 'status': 'skipped: not a partner (builder/fym_flags/nonpartner_allow.json partners)'}; continue
        try: ps = products(dom)
        except Exception as e: res[dom] = {'brand': brand, 'status': f'error (not a Shopify store / no products.json?): {e}'[:200]}; continue
        mats = sorted([[p.get('published_at') or p.get('created_at') or '', p['title'], p['handle']] for p in ps if is_full_mat(p)], reverse=True)
        miss = [m for m in mats if nu(f'{dom}/{m[2]}') not in have]
        res[dom] = {'brand': brand, 'status': 'ok', 'products': len(ps), 'mats': mats, 'missing': miss}
        time.sleep(.5)
    out = {'_about': __doc__.split('\n')[0] + ' Written by builder/partner_mat_sweep.py; read by builder/fym_gate.py [100].',
           'swept_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), 'fym_ref': ref, 'stores': res}
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    n = sum(len(v.get('missing', [])) for v in res.values())
    print(f"partner mat sweep: {sum(1 for v in res.values() if v['status'] == 'ok')} stores ok, {n} full-size mats not in {ref}")
    for dom, v in res.items():
        if v['status'] != 'ok': print(f'  {dom}: {v["status"]}')
        for m in v.get('missing', []): print(f'  MISSING {dom} {m[0][:10]} {m[1]} ({m[2]})')


if __name__ == '__main__':
    main()
