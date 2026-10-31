"""v109 spec (Oct 31 eve): Etsy non-partner brands Tiffany chose 'Bring in now': Betty June & Jeannette (new listings beyond the 23 in
FYM) + Piper Chase Studios (whole mat line). Listings + ShopMy links from config/etsy-brands-oct31.json (Chrome pass Oct 31).
By-eye decisions: etsy109_decisions.py. Photos: Etsy brand images cropped to the mat (boxes picked on a 10% grid; auto box where the
listing shot is already mat-only), 1600px max. Writes config/fym-nonpartner-adds-oct31b.json + assets/mats/v109/*.jpg.
Usage: python3 spec109.py <image dir (img/<pre>__<listing>__<n>.jpg)> <auto boxes json>"""
import sys, json, os, re, importlib.util
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
IMG, AUTO = sys.argv[1], json.load(open(sys.argv[2]))
sp = importlib.util.spec_from_file_location('dec', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etsy109_decisions.py'))
dec = importlib.util.module_from_spec(sp); sp.loader.exec_module(dec)
NB = {  # normalized crop boxes (x0,y0,x1,y1) picked by eye on the 10% grid (scratchpad/feeds109/grid_*.jpg)
 'bjj0': (.05,.12,.80,.86), 'bjj1': (.05,.11,.79,.86), 'bjj2': (0,.10,.82,.92), 'bjj6': (.06,.13,.78,.86), 'bjj10': (0,.10,.78,.87),
 'bjj13': (.05,.14,.75,.87), 'bjj16': (0,.18,.73,.88), 'bjj22': (.05,.18,.73,.88), 'bjj23': (.04,.06,.89,.96), 'bjj32': (0,.15,.74,.88),
 'bjj33': (.04,.14,.71,.88), 'bjj36': (.04,.19,.70,.83), 'bjj44': (0,.20,.80,.87), 'bjj45': (.05,0,.79,1), 'bjj46': (.03,.06,.86,.92),
 'pcs0': (.19,.24,.75,.81), 'pcs2': (.18,.24,.75,.81), 'pcs3': (.18,.24,.75,.81), 'pcs14': (.27,.25,.72,.70), 'pcs16': (.19,.23,.75,.79),
 'pcs17': (.19,.23,.75,.81), 'pcs18': (.19,.23,.76,.81), 'pcs27': (.19,.24,.75,.80), 'pcs28': (.19,.24,.75,.80), 'pcs21': (.23,.20,.77,.76),
 'pcs22': (.23,.21,.77,.77), 'pcs23': (.22,.20,.78,.78), 'pcs24': (.20,.20,.80,.79), 'pcs29': (.18,.18,.82,.83), 'pcs31': (.23,.22,.77,.78),
 'pcs19': (.08,.10,.90,.92), 'pcs20': (.16,.17,.83,.84), 'pcs25': (.21,.22,.79,.78), 'pcs7': (.08,.08,.92,.92)}
NB.update({  # v109 QA re-crops (Oct 31 eve): hands / person / room / table / bag out of frame (scratchpad fix109/g_*.jpg)
 'bjj37': (.02,.03,.82,.94), 'bjj61': (.09,.21,.97,.96), 'bjj17': (.155,.135,.825,.875), 'bjj34': (0,.09,1,1), 'bjj11': (0,.13,.81,.97),
 'bjj9': (.06,.18,.76,.97), 'pcs30': (.22,.27,.84,.79), 'pcs32': (.25,.27,.75,.73), 'pcs33': (.25,.27,.75,.73), 'pcs25': (.24,.25,.77,.735),
 **{t: (.205,.275,.735,.785) for t in ('pcs0','pcs2','pcs3','pcs17','pcs18','pcs27','pcs28')}})
XCUT = {'bjj5': .75, 'bjj18': .85, 'bjj35': .79, 'bjj50': .785, 'bjj53': .80, 'bjj44': .64, 'bjj45': .80, 'bjj55': .78, 'bjj58': .78, 'bjj59': .78}  # v109 QA: bag/tube beside the mat -> cut the auto box's right edge at this fraction of the image width
HIDE = {'bjj61': 'angled shot on a kitchen counter with tiles; no flat image (other listing image is a table mockup) (v109 QA)', 'bjj51': 'brand watermark ("Betty June and Jeannette" script) runs across the only mat images', 'bjj56': 'brand watermark runs across the only mat images; mostly blank design',
        **{f'pcs{k}': v for k, v in dec.PCS_HIDE.items()}}
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:60]
E = json.load(open(REPO + 'config/etsy-brands-oct31.json'))
os.makedirs(REPO + 'assets/mats/v109', exist_ok=True)
mats, skipped = [], []
for bi, br in enumerate(E['brands']):
    pre = 'bjj' if bi == 0 else 'pcs'; bn = 'Betty June & Jeannette' if bi == 0 else 'Piper Chase Studios'
    for k, L in enumerate(br['listings']):
        tag = f'{pre}{k}'
        if pre == 'bjj':
            name, hol, ii, skip, _ = dec.BJJ[k]
            if skip: skipped.append((bn, L['name'], skip)); continue
        else:
            name, hol, ii = L['name'], k in dec.PCS_HOL, 0
        if not L.get('shopmy_url'): skipped.append((bn, name, 'no ShopMy link')); continue
        src = f'{IMG}/{pre}__{L["listing_id"]}__{ii}.jpg'
        im = Image.open(src).convert('RGB'); W, H = im.size
        if tag in NB: x0, y0, x1, y1 = NB[tag]; box = (round(x0*W), round(y0*H), round(x1*W), round(y1*H))
        else: box = tuple(AUTO[tag]['box'])
        if tag in XCUT: box = (box[0], box[1], min(box[2], round(XCUT[tag] * W)), box[3])
        im = im.crop(box); im.thumbnail((1600, 1600)); dst = f'assets/mats/v109/{pre}-{L["listing_id"]}-{slug(name)}.jpg'; im.save(REPO + dst, quality=90)
        hid = tag in HIDE
        mats.append(dict(key=f'www.etsy.com/listing/{L["listing_id"]}/{slug(name)}', name=name, bn=bn, b=bn, u=L['shopmy_url'], u0=L['etsy_url'],
                         dc='', pa=False, img=dst, hol=bool(hol), hid=hid, reason=HIDE.get(tag, ''),
                         photo_note=f'Etsy listing image {ii}, cropped to the mat' + (' (grid box)' if tag in NB else ' (auto box)')))
json.dump(dict(_about=__doc__, made='2026-10-31', mats=mats, skipped=[dict(brand=a, name=b, why=c) for a, b, c in skipped]),
          open(REPO + 'config/fym-nonpartner-adds-oct31b.json', 'w'), indent=1, ensure_ascii=False)
from collections import Counter
print(len(mats), Counter(m['bn'] for m in mats), 'hol', sum(m['hol'] for m in mats), 'hidden', sum(m['hid'] for m in mats), 'skipped', len(skipped))
