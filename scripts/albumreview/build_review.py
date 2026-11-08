"""THE album review page (Album Playbook, Nov 8: "The review page"). One generator for every album.

Usage: python3 scripts/albumreview/build_review.py <set> [outdir]
  outdir default: <scratchpad or /tmp>/albumreview/<set>/ . Writes:
    index.html            the page (publish this; capabilities {db: {rules: [{path: "", read: "view", write: "admin"}]}})
    files.json            {published path: source path} for the Artifact tool's `files` (cards, faces, covers, catalog)
    c/ lo/ f/ t/ cat/     images + the catalog search data (cat/catalog.json + cat/s<N>.jpg sprites)
Refuses to write anything when scripts/checks/album_gate.py <set> fails.

Inputs (all named by config/album-records/<set>.json): the album spec (deco_build-style JSON: groups + mats), the card
manifest (assets/cards/<set>/manifest.json, cards from gen2 = code band enforced), config/colorcards.json,
config/tnt-recs.json (TNT + other_groups), the left-out list, the faces (record faces: groups + 5 picks), the cover
options, and config/fym-mats-snapshot.json + FYM photos (scripts/albumreview/fym_images.py) for "Missed one?".

Her taps save to the artifact db, doc review/<set> (one shared doc per album):
  {set, round, v: {cardId: 'keep'|'remove'}, notes: {cardId: text}, order: {main: [...], hol: [...]}, ordering_off,
   faces: [keys], cover: index, putin: [leftoutId], adds: [{k, n, b}], anything, done, updated}
Claude reads it with ArtifactData (get review/<set>) and applies it with scripts/albumreview/read_review.py.
Page rules: X and heart only (never crush/nope/pass); mat + tiles together (match-card style); nothing pre-set she must clear."""
import json, os, re, sys, html, io, shutil
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'scripts/checks'); sys.path.insert(0, R + 'scripts/albumreview')
import album_gate
SET = sys.argv[1]
SCR = os.environ.get('CLAUDE_SCRATCH') or '/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(SCR if os.path.isdir(SCR) else '/tmp', 'albumreview', SET)

bad, proof = album_gate.check(SET)
if bad:
    sys.exit('REFUSED (album_gate): the review page is built only when steps 1-8 are on record:\n  ' + '\n  '.join(bad))

J = lambda p: json.load(open(R + p))
rec = J(f'config/album-records/{SET}.json')
spec = J(rec['spec']); man = J(rec['cards_dir'] + '/manifest.json')
lo_all = J(rec['leftout']['file'])[rec['leftout']['key']]
cc = J('config/colorcards.json')['sets'][SET]
snap = J('config/fym-mats-snapshot.json')
os.makedirs(OUT, exist_ok=True)
for d in ('c', 'lo', 'f', 't', 'cat', 'nf'): os.makedirs(os.path.join(OUT, d), exist_ok=True)
FILES = {}


def put(pub, im=None, src=None, maxs=None, q=84):
    """Write an image into OUT/pub (resized jpg/png) and list it in files.json."""
    dst = os.path.join(OUT, pub)
    if im is None and maxs is None:
        shutil.copyfile(R + src, dst)
    else:
        im = im or Image.open(R + src)
        if maxs: im = im.copy(); im.thumbnail((maxs, maxs))
        if pub.endswith('.png'): im.save(dst, optimize=True)
        else: im.convert('RGB').save(dst, 'JPEG', quality=q, optimize=True, progressive=True)
    FILES[pub] = dst
    return pub


def cid(fn): return re.sub(r'-mat\.jpg$', '', fn.replace(f'{SET}-mahjong-tiles-', ''))


def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and').replace("'", '')).strip('-')


# ---- cards
specmat = {m['name']: m for m in spec['mats']}
cards = []
for c in man['cards']:
    i = cid(c['file'])
    put(f'c/{i}.jpg', src=f"{rec['cards_dir']}/{c['file']}", maxs=1080, q=82)
    m = specmat.get(c['mat'], {})
    tags = []
    if c.get('caption_note') == 'TNT rec': tags.append('TNT rec')
    elif c.get('caption_note') and c['caption_note'] not in ('Retired', 'Holiday match'): tags.append(c['caption_note'])
    if c.get('retired_mat'): tags.append('Retired')
    if not c.get('partner', True): tags.append('No code at this brand (caption only)')
    if c.get('lowres'): tags.append('Small brand photo')
    title = f"TNT rec · {c['mat']} · {c['brand']}" if c.get('caption_note') == 'TNT rec' else c['mat']
    cards.append({'id': i, 'mat': c['mat'], 'brand': c['brand'], 'title': title, 'g': man['groups'].get(c['group'], c['group']),
                  'hol': bool(c.get('holiday')), 'why': c.get('why', ''), 'tags': tags, 'fym': c.get('fym'), 'her_note': m.get('her_note')})

# ---- left out (mat full + the cards' tile inset, match-card style)
TP = rec['tile_photo']
put('t/inset.jpg', src=TP['inset'], maxs=420)
leftout = []
for n, m in enumerate(lo_all):
    i = f"lo-{slug(m['brand'])}-{slug(m['name'])}"
    put(f'lo/{i}.jpg', src=m['img'], maxs=900, q=82)
    leftout.append({'id': i, 'name': m['name'], 'brand': m['brand'], 'why': m['why'], 'retired': m.get('retired', False), 'hol': bool(m.get('holiday')), 'more': m.get('more_from')})
# ---- new finds (Playbook step 3b discovery): mats not in our catalog, Bring it in / Skip
disc = rec.get('discovery') or {}
finds = []
for f in disc.get('new_finds', []):
    put(f"nf/{f['id']}.jpg", src=f['img'], maxs=900, q=84)
    finds.append({k: f.get(k, '') for k in ('id', 'name', 'seller', 'url', 'source', 'why', 'note')})

# ---- tiles, covers, colour card, wheel, faces
put('t/tile.jpg', src=TP['file'], maxs=1400)
put('t/cc.jpg', src=rec['colorcard_img'], maxs=1400)
put('t/wheel.jpg', src=rec['wheel_img'], maxs=1200)
covers = []
for n, o in enumerate(rec['covers']['options']):
    put(f't/cover-{n}.jpg', src=o['img'], maxs=1080)
    covers.append({'n': n, 'label': o['label'], 'note': o.get('note', '')})
fz = rec['faces']; picks = [p['key'] if isinstance(p, dict) else p for p in fz['picks']]
whys = {p['key']: p.get('why', '') for p in fz['picks'] if isinstance(p, dict)}
fgroups = []
for g in fz['groups']:
    for it in g['items']: put(f"f/{it['key']}.png", src=fz['dir'] + it['key'] + '.png', maxs=240)
    fgroups.append({'title': g['title'], 'items': [{'k': it['key'], 'l': it['label'], 'why': whys.get(it['key'], '')} for it in g['items']]})

# ---- catalog for "Missed one?": every visible FYM mat, 96px thumbs packed in sprites of 400
from fym_images import image_bytes
vis = [(k, m) for k, m in snap['mats'].items() if not m.get('hid')]
vis.sort(key=lambda x: (x[1]['bn'].lower(), x[1]['n'].lower()))
CACHE = os.path.join(SCR if os.path.isdir(SCR) else '/tmp', 'albumreview', '_fymthumbs')
os.makedirs(CACHE, exist_ok=True)
need = [m['f'] for k, m in vis if not os.path.exists(os.path.join(CACHE, m['f'].replace('/', '_') + '.jpg'))]
if need:
    for f, b in image_bytes(need).items():
        try:
            im = Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((96, 96))
            sq = Image.new('RGB', (96, 96), (246, 238, 230)); sq.paste(im, ((96 - im.width) // 2, (96 - im.height) // 2))
            sq.save(os.path.join(CACHE, f.replace('/', '_') + '.jpg'), quality=80)
        except Exception: pass
in_album = {c['mat'] + '|' + c['brand'] for c in cards}
cat, per, T = [], 400, 96
sheets = [Image.new('RGB', (20 * T, 20 * T), (246, 238, 230)) for _ in range((len(vis) + per - 1) // per)]
for n, (k, m) in enumerate(vis):
    p = os.path.join(CACHE, m['f'].replace('/', '_') + '.jpg')
    s, j = divmod(n, per)
    if os.path.exists(p): sheets[s].paste(Image.open(p), ((j % 20) * T, (j // 20) * T))
    cat.append([k, m['n'], m['bn'], s, j, 1 if m.get('hol') else 0, 1 if (m['n'] + '|' + m['bn']) in in_album else 0])
for s, im in enumerate(sheets):
    im.save(os.path.join(OUT, f'cat/s{s}.jpg'), quality=72, optimize=True, progressive=True); FILES[f'cat/s{s}.jpg'] = os.path.join(OUT, f'cat/s{s}.jpg')
json.dump(cat, open(os.path.join(OUT, 'cat/catalog.json'), 'w'), separators=(',', ':'), ensure_ascii=False)
FILES['cat/catalog.json'] = os.path.join(OUT, 'cat/catalog.json')

# ---- proof for "What Claude did" (steps 1-8), all read from data via album_gate
P = proof; t = P['research']['tnt'] or {}; og = P['research']['other'] or {}
tnt_recs = len(t.get('recs', [])); og_recs = len(og.get('recs', []))
groups_txt = 'Tiles & Tablescapes' + ''.join(f", {g['name']} ({g['members']})" for g in og.get('groups', []))
terms = ', '.join(f'“{x}”' for x in og.get('terms', [])) or '—'
pool = P['pool']
ck = P.get('catalog') or {}
import datetime as _dt
CKT = _dt.datetime.fromisoformat(ck['at']).strftime('%b %-d, %-I:%M %p').replace('AM', 'am').replace('PM', 'pm') if ck.get('at') else ''
nhol = sum(1 for c in cards if c['hol'])
steps = [
 {'n': 1, 'name': 'Tiles ready in Find Your Mat-ch', 'ok': bool(P['fym'].get('slug') and P['fym'].get('back')),
  'txt': (f"Your tile photo yes: {TP['approved_at'][:16].replace('T', ' ')}. " if TP.get('approved_at') else '') + f"Tile photo, colours and back colour (walls in Table view, {P['fym'].get('back')}) are in the app (photo below). The tile shot on the cards is under The tiles.", 'img': 't/tile.jpg'},
 {'n': 2, 'name': 'Colour card', 'ok': bool(P['colorcard'].get('img')), 'txt': 'Back colour first, then layers, then face colours by how many tiles carry them.', 'img': 't/cc.jpg'},
 {'n': 3, 'name': 'Facebook research', 'ok': bool(t.get('scanned') and og.get('scanned')),
  'txt': f"Searched {groups_txt}. Terms: {terms}. Tiles & Tablescapes recs: {tnt_recs}; other groups: {og_recs}. " + (og.get('note') or '')},
 {'n': '3b', 'name': 'Mat discovery', 'ok': bool(disc.get('at')),
  'txt': f"{len(disc.get('searches', []))} searches (" + ', '.join(sorted({x['where'] for x in disc.get('searches', [])})) + '): ' + '; '.join(f"“{x['terms']}”" for x in disc.get('searches', [])) + f". New finds: {len(disc.get('new_finds', []))} (below, Bring it in or Skip). Missed catalog mats added: " + (', '.join(disc.get('misses_added', [])) or 'none') + '. ' + (('Complementary side: ' + '; '.join(f"“{x['terms']}”" for x in disc.get('searches', []) if x.get('complementary')) + '. ' + disc.get('complementary', '') + ' ') if disc.get('complementary') else '') + disc.get('recheck_nonpartner', '')},
 {'n': 4, 'name': 'Candidates pulled', 'ok': bool(pool.get('size') and ck.get('at')),
  'txt': (f"Catalog checked {CKT}: {len(ck.get('added', []))} new mats added ({ck.get('shopmy_new', 0)} from ShopMy, {ck.get('partner_new', 0)} from partner stores). " if ck.get('at') else 'Catalog not checked. ')
         + f"Pool of {pool.get('size')} mats ({pool.get('year_round', '?')} year-round, {pool.get('holiday', '?')} holiday in Find Your Mat-ch, plus the new ones). Sources: " + '; '.join(pool.get('sources', [])) + '.'},
 {'n': 5, 'name': 'By-sight check', 'ok': P['leftout'] > 0, 'txt': f"{P['leftout']} mats cut by eye. Each one is in Left out below with the reason. " + (rec.get('bysight') or {}).get('catalog_new', '')},
 {'n': 6, 'name': 'Holiday section', 'ok': bool(P['holiday']['n'] or P['holiday'].get('note')),
  'txt': f"{nhol} holiday cards. " + (P['holiday'].get('note') or '')},
 {'n': 7, 'name': 'Ordered', 'ok': True,
  'txt': 'Standouts first: the 5-6 matches that look best together (the colour card top 3 come from them). Colour theory carries the weight; your past pairings and Tiles & Tablescapes recs add a little (' + str(P['cards'].get('tnt', 0)) + ' TNT recs, labelled, no automatic front spot). ' + (rec.get('rank') or {}).get('note', '')},
 {'n': 8, 'name': 'Cards built', 'ok': P['cards'].get('band') == 'PASS',
  'txt': f"{P['cards'].get('n')} match cards. Code band check: {P['cards'].get('band')} (every card with a partner piece says MAHJMATCH)."},
]
rounds = rec.get('rounds', [])
DATA = {'set': SET, 'name': rec['name'], 'brand': rec['brand'], 'round': len(rounds) + 1,
        'last': rounds[-1] if rounds else None, 'steps': steps, 'covers': covers, 'coverDefault': rec['covers'].get('default', 0),
        'finds': finds, 'faces': fgroups, 'picks': picks, 'legacyFaces': rec.get('legacy_faces_key'), 'cards': cards, 'leftout': leftout,
        'groupsOrder': list(dict.fromkeys(c['g'] for c in cards if not c['hol']))}

e = html.escape
TPL = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review_template.html')).read()
page = (TPL.replace('__TITLE__', e(f"{rec['name']} Album Review"))
           .replace('__SETNAME__', e(rec['name'])).replace('__BRAND__', e(rec['brand']))
           .replace('__COL__', cc.get('col', '#7a2c55'))
           .replace('"__DATA__"', json.dumps(DATA, ensure_ascii=False).replace('</', '<\\/')))
open(os.path.join(OUT, 'index.html'), 'w').write(page)
json.dump(FILES, open(os.path.join(OUT, 'files.json'), 'w'), indent=0)
print(f'ALBUM REVIEW PAGE {SET}: {OUT}/index.html  ({len(cards)} cards, {len(leftout)} left out, {len(cat)} catalog mats, {len(FILES)} files)')
