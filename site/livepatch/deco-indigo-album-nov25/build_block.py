"""Deco Indigo (Bam Bird Boutique) album page code block, built from the Sadie Jane builder (Nov 25).
Original notes: Sadie Jane (Oh My Mahjong) album page code block (Tiffany's review round 2 closed Nov 23 4:14pm, final order in
review db v437 -> scripts/albumcard/specs/deco-indigo_nov07.json order).
Layout (Tiffany Nov 23 4:14-4:24pm, first OMM album built this way):
  1. "Top Oh My Mahjong matches": the OMM mats from her order, same order.
  2. "Cross-brand matches": every other brand, her order, no repeats.
  3. Holiday section (#holiday-matches).
Template = the LIVE Juniper block (CSS, hero, FAQ + JSON-LD, guides, lightbox with the Nov 8 pinch fix), like Deco Lagoon.
Links: FYM 1.22.16 build for catalog mats; record new-finds urls for the 6 not in FYM (plain product links, no code: ShopMy
links owed, OVERDUE). Pre-launch copy: tiles + Serendipity drop Wed Nov 25 11am ET.
Usage: python3 build_block.py <image sha> <fym index.html>  -> deco-indigo-codeblock.html + urls.txt"""
import json, sys, re, html as H, urllib.parse as U
R = '/home/claude/mahjmatchmaker-data/'; HERE = R + 'site/livepatch/deco-indigo-album-nov25/'
SHA, FYM = sys.argv[1], sys.argv[2]
h = open(FYM, encoding='utf-8').read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
CDN = f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{SHA}/'
e = lambda s: H.escape(s, quote=True)
man = {c['mat']: c for c in json.load(open(R + 'assets/cards/deco-indigo/manifest.json'))['cards']}
_allspec = {x['name']: x for x in json.load(open(R + 'scripts/albumcard/specs/deco-indigo_nov07.json'))['mats']}
_mo = json.load(open(R + 'assets/cards/deco-indigo/manifest.json'))['cards']  # Nov 26: page = manifest cards, manifest order
spec = [dict(_allspec[c['mat']], holiday=c['holiday']) for c in _mo]
rec = json.load(open(R + 'config/album-records/deco-indigo.json'))
NEWURL = {}
for v in rec.values() if isinstance(rec, dict) else []:
    pass
def walk(o):
    if isinstance(o, dict):
        if o.get('mat') and o.get('url'): NEWURL.setdefault(o['mat'], o['url'])
        for x in o.values(): walk(x)
    elif isinstance(o, list):
        for x in o: walk(x)
walk(rec)
NEWURL.update({'Eaton Indigo': 'https://www.ozarkmahjongg.com/product-page/eaton-indigo-mat', 'Dark Blue Art Deco, Gold Geometric Fans': 'https://go.shopmy.us/p-102728926', 'Vegan Leather – Hunter Green': 'https://www.bambirdboutique.com/discount/MAHJMATCH?redirect=%2Fproducts%2Forigami-leather-mat%3Fvariant%3D67732658880821%26sca_ref%3D10069575.cf1ZUJEgbaOpCDgy', 'Pink & Blue Grandmillennial': 'https://www.etsy.com/listing/4527255793',
               'Chinoiserie Pastel Floral': 'https://www.etsy.com/listing/4497703295',
               'The Kerry (Glamourous)': 'https://www.etsy.com/listing/4610692079'})
FIXKEY = {'Deco Dragon (Indigo)': 'www.bambirdboutique.com/deco-neoprene-mahjong-mat-copy-2?v=67663098282293', 'Deco Dragon (Lagoon)': 'www.bambirdboutique.com/deco-neoprene-mahjong-mat-copy-2?v=67663098315061', 'Deco Dragon (Mulberry)': 'www.bambirdboutique.com/deco-neoprene-mahjong-mat-copy-2?v=67663098347829', 'Sunday Sherbert Double-Sided Mahjong Mat – Leatherette 31.5"': 'mahjongregister.com/snowflake-reindeer-lodge-double-sided-leatherette-mahjong-mat-31-5-x-31-5-copy'}
PARTNERS = set(json.load(open(R + 'builder/fym_flags/nonpartner_allow.json'))['partners'])
RN = {v['n']: v for v in D['racks'].values()}
TILE_URL = D['tiles']['www.bambirdboutique.com/deco-tile-set?v=53195200004405']['u']
SET = 'Deco Indigo'
def plain(u):
    p = U.urlparse(u); q = U.parse_qs(p.query)
    return f'{p.scheme}://{p.netloc}' + q['redirect'][0] if '/discount/' in p.path and 'redirect' in q else u
def brandpg(m):
    p = U.urlparse((m or {}).get('dc') or '').path
    return p if p.endswith('-discount-code') else None
MISSR = []
OTHERURL = {}
for _k in ('deco-lagoon', 'deco-mulberry'):
    for _x in json.load(open(R + f'scripts/albumcard/specs/{_k}_nov07.json'))['mats']:
        if _x.get('url'): OTHERURL.setdefault(_x['name'], _x['url'])

RALIAS = {'Bam Bird Boutique Indigo': 'Bam Bird Boutique Indigo Wood', 'Bam Bird Boutique Olive': 'Bam Bird Boutique Olive Green Wood', 'Peace Love Mahjong Acrylic Burl': 'Peace Love Mahjong Acrylic Burlwood'}
def rack(n):
    v = RN.get(n) or RN.get(RALIAS.get(n, ''))
    if not v: MISSR.append(n); return e(n)
    return f'<a href="{e(v["u"])}" target="_blank" rel="sponsored noopener">{e(n)}</a>'
def figure(n, s, hol):
    c = man[s['name']]
    m = D['mats'].get(c.get('fym') or s.get('fym') or '') or D['mats'].get(FIXKEY.get(s['name']) or '') or next((v for v in D['mats'].values() if v.get('n') == s['name'] and v.get('bn') == s['brand']), None)
    brand, mat, retired = s['brand'], s['name'], bool(s.get('retired') or c.get('retired_mat'))
    u = (m.get('u') if m else None) or NEWURL.get(mat) or s.get('url') or OTHERURL.get(mat)
    
    if not u and brand == 'Oh My Mahjong' and (m or s.get('retired')): retired = True; u = 'x'
    if not u: print(f'SET ASIDE (no link): {mat}'); return ''
    partner = brand in PARTNERS or (m and m.get('pa')) or brand == 'Bam Bird Boutique'
    pg = brandpg(m) if (m and partner) else None
    by = f'<a href="{pg}">{e(brand)}</a>' if pg else e(brand)
    ret = '<span class="mm3-ret">Retired</span>' if retired else ''
    label = mat if mat.lower().endswith(' mat') else mat + ' Mat'
    if brand == 'Mahjong Register': u = plain(u)
    if retired and brand == 'Oh My Mahjong':
        btn = f'<a class="mm3-btn" href="{e(D["mats"]["www.ohmymahjong.com/serendipity-mat-in-tube"]["u"].split("?")[0])}?redirect=%2Fcollections%2Fmats" target="_blank" rel="sponsored noopener">Shop Current OMM Mats</a>'
    else:
        btn = f'<a class="mm3-btn" href="{e(u)}" target="_blank" rel="sponsored noopener">Shop the {e(label)}</a>'
    if not partner: code = f'<span class="mm3-code" style="color:#8a8a8a">No code for {e(brand)}</span>'
    elif brand == 'Mahjong Register': code = '<span class="mm3-code">10% off at Mahjong Register with MAHJMATCH (excludes racks and other brands\' products)</span>'
    else: code = '<span class="mm3-code">code MAHJMATCH</span>'
    take = ('<div class="mm3-take"><p>Pair mat: Bam Bird Boutique made the Deco Dragon mats to go with the Deco tiles.</p></div>'
            if mat == 'Deco Dragon (Mulberry)' else '')
    cap = 'Match the tiles: ' + ' · '.join(rack(x) for x in c['racks'])
    if c.get('mat_racks'): cap += '<br>Match the mat: ' + ' · '.join(rack(x) for x in c['mat_racks'])
    alt = f'Bam Bird Boutique Deco Indigo mahjong tiles with {brand} {mat} {"holiday " if hol else ""}mahjong mat'
    cls = 'mm3-c mm3-hc' if hol else 'mm3-c'
    return (f'<figure class="{cls}"><div class="mm3-im"><img src="{CDN}assets/cards/deco-indigo/{c["file"]}" data-lb="" alt="{e(alt)}" loading="lazy" width="750" height="938">'
            f'<a class="mm3-pin" href="#" target="_blank" rel="noopener" aria-label="Save to Pinterest">Save</a></div><figcaption>'
            f'<span class="mm3-n">{n:02d}</span><h3>{SET} + {e(mat)}</h3><span class="mm3-by">Mat by {by}{ret}</span>{take}'
            f'<div class="mm3-l">{btn}{code}</div><div class="mm3-rk" style="margin-top:8px;font-size:.82em;line-height:1.55">{cap}</div></figcaption></figure>')
main = [s for s in spec if not s.get('holiday')]; hol = [s for s in spec if s.get('holiday')]
omm = [s for s in main if s['brand'] == 'Bam Bird Boutique']; cross = [s for s in main if s['brand'] != 'Bam Bird Boutique']
assert len(omm) + len(cross) + len(hol) == len(spec) == len(man)

ofigs = ''.join(figure(n, s, False) for n, s in enumerate(omm, 1))
cfigs = ''.join(figure(n, s, False) for n, s in enumerate(cross, 1))
hfigs = ''.join(figure(n, s, True) for n, s in enumerate(hol, 1))
nb = len({s['brand'] for s in spec}); top3 = main[:3]
top = (f"My top mat picks for Bam Bird Boutique's Deco Indigo tiles are {top3[0]['name']} by {top3[0]['brand']}, "
       f"{top3[1]['name']} by {top3[1]['brand']}, and {top3[2]['name']} by {top3[2]['brand']}.")
tpl = open(R + 'site/livepatch/juniper-album-nov07/juniper-codeblock.html').read()
css = tpl[tpl.index('</style>') + 8:tpl.index('<div class="mm3" id="juniper-album">')]
lb = tpl[tpl.index('<div class="mm3-lb"'):]
HOLCSS = open(R + 'site/livepatch/missed-album-picks-nov07/holcss.html').read().strip()
CC = CDN + 'assets/colorcards/deco-indigo/00-deco-indigo-mahjong-tiles-'
BG = ('<style id="mmdibg">.mm3-launch{display:inline-block;background:#263a63;color:#fff;font-size:12px;font-weight:700;letter-spacing:.12em;'
      'text-transform:uppercase;padding:4px 12px;border-radius:12px;margin:0 0 10px}</style>')
body = (
 f'<div class="mm3" id="deco-indigo-album"><header class="mm3-hero mm3-hero-2"><div class="mm3-hero-img"><img src="{CDN}assets/covers/albums/00-deco-indigo-mahjong-tiles-cover.jpg" data-lb="" alt="Bam Bird Boutique Deco Indigo mahjong tiles" fetchpriority="high"></div>'
 '<div class="mm3-hero-t"><p class="mm3-kicker">Bam Bird Boutique</p><span class="mm3-launch">Preorder opens Thu 11/26</span><h1>Deco Indigo Mahjong Tile Matches</h1><div class="mm3-intro">'
 "<p>Bam Bird Boutique's Deco tiles in Indigo: deep navy-blue backs with a gold-foil palm under an ivory face, and faces in mulberry, teal, rose and gold. "
 'My top Bam Bird Boutique matches come first, then matches from more brands and a holiday section. '
 'Tap any photo to see it bigger, and use code MAHJMATCH to save at our partner brands.</p></div>'
 f'<p class="mm3-cta"><a class="mm3-btn mm3-btn-l" href="{e(TILE_URL)}" target="_blank" rel="sponsored noopener">See Deco Indigo at Bam Bird Boutique</a>'
 '<span>Save with <a href="/bam-bird-boutique-discount-code">Bam Bird Boutique discount code</a> <strong>MAHJMATCH</strong></span></p></div></header>'
 '<section class="mm3-faq" style="max-width:860px;margin:28px auto 8px;padding:0 20px;text-align:center"><h2>What mats match Deco Indigo mahjong tiles?</h2>'
 f'<p>{e(top)} Below are {len(spec)} Deco Indigo mat matches from {nb} brands, and counting: {len(omm)} from Bam Bird Boutique, {len(cross)} from other brands and {len(hol)} for the holidays, each with rack picks and a link to shop.</p></section>'
 '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "What mats match Deco Indigo mahjong tiles?",
   "acceptedAnswer": {"@type": "Answer", "text": top + " Save at partner brands with code MAHJMATCH."}}]}) + '</script>'
 '<section class="mm3-guides"><h2>Colors &amp; racks</h2><div class="mm3-gg">'
 f'<figure class="mm3-g"><picture><source media="(max-width: 640px)" srcset="{CC}color-guide-mobile.jpg"><img src="{CC}tile-edit-moodboard.jpg" data-lb="" '
 'alt="Bam Bird Boutique Deco Indigo mahjong tiles color card: navy-blue backs with a gold-foil palm and ivory faces, faces in mulberry, teal, rose and gold, with rack and mat matches" loading="lazy"></picture>'
 '<figcaption><strong>The Tile Edit</strong><p>Deep indigo backs with a gold-foil palm, ivory faces, and mulberry, teal, rose and gold on the faces. '
 "Bam Bird's own Indigo rack matches the backs, and their Mulberry Wood rack picks up the mulberry crak frames.</p></figcaption></figure>"
 '<style>.mm3-gg>.mm3-g:has(img[src*="tile-edit-moodboard"]){grid-column:1/-1}.mm3-gg>.mm3-g:has(img[src*="tile-edit-moodboard"]) figcaption{max-width:860px;margin:0 auto;padding:20px 26px 12px;font-size:16px}</style>'
 f'<figure class="mm3-g mm3-wheel"><img src="{CDN}assets/colorwheels/deco-indigo-color-wheel.jpg" data-lb="" alt="Deco Indigo mahjong tiles on the color wheel: indigo, gold, ivory, mulberry and teal" loading="lazy">'
 '<figcaption><strong>The colors on the wheel</strong><p>Deco Indigo is a deep jewel-tone set. Mats with berry, teal, green or gold give the navy backs something to stand against; '
 'a plain navy or royal blue mat makes them disappear.</p></figcaption></figure>'
 '<style>.mm3-gg>.mm3-g.mm3-wheel{grid-column:1/-1;max-width:760px;width:100%;margin:6px auto 0}</style>'
 '</div></section>\n'
 f'<section id="top-bam-bird-matches"><h2>Top Bam Bird Boutique matches</h2><p class="mm3-sub">My favorite Bam Bird Boutique mats for Deco Indigo. More matches from other brands are below.</p><div class="mm3-grid">{ofigs}</div></section>'
 f'<section id="cross-brand-matches"><h2>Deco Indigo across more brands</h2><p class="mm3-sub">More mat brands that match Deco Indigo, my top picks first. Tap any photo to see it bigger.</p><div class="mm3-grid">{cfigs}</div></section>'
 f'{HOLCSS}<section class="mm3-hol" id="holiday-matches"><h2>Holiday matches for Deco Indigo</h2><p class="mm3-sub">Christmas and Hanukkah mats for Deco Indigo, with rack picks. '
 'See more holiday matches on the <a href="/holiday-mahjong-matches">Holiday Matches</a> page.</p>'
 f'<div class="mm3-grid">{hfigs}</div></section>'
 '<p class="mm3-foot">Deco Indigo opens for preorder Thursday 11/26 at Bam Bird Boutique. Save with code <strong>MAHJMATCH</strong>. Try it in <a href="/find-your-match">Find Your Mat-ch</a>, browse more <a href="/mahjong-tile-matches">tile match albums</a> or see our <a href="/mahjong-discount-codes">mahjong discount codes</a>.</p></div>')
out = BG + css + body + lb
bad = [m.start() for m in re.finditer(r'(?i)juniper', out)]
assert not bad, out[bad[0] - 80:bad[0] + 80]
from html.parser import HTMLParser as _HP
class _P(_HP):
    V={'img','br','hr','meta','link','input','source','wbr'}
    def __init__(s): super().__init__(); s.n=0
    def handle_starttag(s,t,a): s.n += t=='div'
    def handle_endtag(s,t): s.n -= t=='div'
_p=_P(); _p.feed(out); assert _p.n == 0, ('unbalanced divs', _p.n)  # Nov 23: a missing </div> swallowed the page's button block and hid the whole album
open(HERE + 'deco-indigo-codeblock.html', 'w').write(out)
urls = sorted(set(re.findall(r'https://cdn\.jsdelivr\.net/gh/[^"\s)]+', out)))
open(HERE + 'urls.txt', 'w').write('\n'.join(urls) + '\n')
print(len(re.findall(r'<figure class="mm3-c', out)), 'cards:', len(omm), 'Bam Bird +', len(cross), 'cross-brand +', len(hol), 'holiday;', nb, 'brands;', len(urls), 'cdn urls;', len(out), 'bytes')
print('racks with no link:', sorted(set(MISSR)))
