"""Re-sort the FYM opening-screen brand logos (Tiffany Oct 29 3:29pm / 3:31pm, Oct 30 2:49am).

Order = Oh My Mahjong first (category leader), then partner brands by commission over the last 30 days
(HQ artifact Cor6pKtesou4mFRQ41P6Ye, db collection `money`, one doc per day with brands[].commission),
then partners with no recent sales by number of visible tile sets. Non-partners are always last (the page
splits them out by BCODE, so their place in this list does not matter).

Usage:  export the money collection with ArtifactData list (out_dir) and run
    python3 builder/fym_brand_logo_order.py <dir with YYYY-MM-DD.json>
It rewrites config/fym-brand-logo-order.json. Re-run weekly (Monday desk cleanup) and rebuild FYM.
"""
import sys, os, json, glob, datetime, collections
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
OUT = REPO + 'config/fym-brand-logo-order.json'
# money-ledger brand names -> FYM tile maker names (s.maker)
ALIAS = {
    'Mahjong Row & Co. (11:44pm order)': 'Mahjong Row & Co.', 'Middle & Main': 'Middle & Main Mahjong',
    'Virora': 'Virora Mahjong', 'Tigre de Tartán': 'Tigre de Tartan', 'Mac + Miller': 'Mac + Miller Mahjong',
    'Mac+Miller Mahjong': 'Mac + Miller Mahjong', 'The Mahjong Co.': 'Mahjong Co.',
    'The Royal Mahjong Society': 'Royal Mahjong Society', 'Amahj Line': 'Amahj', 'Lets Be Besties': "Let's Be Besties",
}
FIRST = ['Oh My Mahjong']

def main(d):
    files = sorted(glob.glob(os.path.join(d, '*.json')))
    last = max(os.path.basename(f)[:10] for f in files)
    cut = (datetime.date.fromisoformat(last) - datetime.timedelta(days=29)).isoformat()
    c = collections.Counter()
    for f in files:
        if os.path.basename(f)[:10] < cut: continue
        for b in json.load(open(f)).get('brands', []):
            n = ALIAS.get(b.get('brand', ''), b.get('brand', ''))
            if n.startswith('ShopMy'): continue
            c[n] += float(b.get('commission') or 0)
    order = FIRST + [b for b, _ in c.most_common() if b not in FIRST]
    json.dump({
        '_note': 'FYM tiles-door opening logos. OMM first, then partners by commission over the 30 days ending ' + last +
                 ' (HQ money). Partners not listed here follow by visible tile-set count; non-partners always last. '
                 'Rebuild with builder/fym_brand_logo_order.py <money export dir>. Hand edits are fine: just move a name.',
        'window': [cut, last], 'order': order,
        'commission_30d': {k: round(v, 2) for k, v in c.most_common()},
    }, open(OUT, 'w'), indent=1, ensure_ascii=False)
    print('wrote', OUT, order[:12])

if __name__ == '__main__':
    main(sys.argv[1])
