"""Mat Gallery v2 (/mahjong-mats), Oct 20.
Changes from v1 (build.py): a mat can sit in several color sections (primary + Tiffany's "also" colors; Multicolor = any mat
tagged multi), retired mats get their own section at the bottom (with a "Hide retired" toggle, default on, that keeps them
out of the color sections), duplicates are collapsed to one card, raw store titles are cleaned, and launch-blocking images
(placeholders, wrong images, no mat in the photo) are hidden.

Inputs: matgallery.html (889 rows, v1 JSON), manifest.json, held-low-98.json, config/mat-color-overrides.json (+ guesses via
scripts/colors/matcolors.py), config/tiffany-color-notes/*.json, and the FYM mat visual audit CSV (argv[1]).
Usage: python3 build_v2.py <audit report.csv> <pairs.json from phash> > matgallery-v2.html
Side outputs: dedupe_oct20.csv, hidden_oct20.csv, v2_counts.json (same folder), and overrides updated in place."""
import json, sys, os, re, csv, html, difflib, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
P = lambda *a: os.path.join(ROOT, *a)
AUDIT, PAIRS = sys.argv[1], sys.argv[2]
COMMIT = '3e8af50f24b40ffdcc7f8c76540feb0b36907f14'  # same jsDelivr image base as the live block
TODAY = '2026-10-20'

t = open(os.path.join(HERE, 'matgallery.html')).read()
F = json.loads(re.search(r'<script type="application/json">(.*?)</script>', t, re.S).group(1).replace('<\\/', '</'))
man = json.load(open(os.path.join(HERE, 'manifest.json')))
held = set(json.load(open(os.path.join(HERE, 'held-low-98.json'))))
log = lambda *a: print(*a, file=sys.stderr)

# ---------- 1. Tiffany's color calls -> config/mat-color-overrides.json ----------
OV_PATH = P('config/mat-color-overrides.json')
OV = json.load(open(OV_PATH))
G = json.load(open(P('config/mat-color-guesses.json')))['mats']
notes = []
for fn in sorted(glob.glob(P('config/tiffany-color-notes/2026-10-20-pink-section*.json'))):
    for c in json.load(open(fn))['corrections']:
        notes.append(dict(c, _src=os.path.basename(fn)))
# Coordinator relay, Oct 20 evening: Britt Mills Novella Leatherette
notes.append({'brand': 'Britt Mills', 'name': 'Novella Leatherette', 'primary': 'orange', 'also': ['red'],
              'note': 'peachy-pink center, rust border; not pink', '_src': 'tiffany-chat-oct20-evening'})


def norm(s):
    s = s.lower().replace('&', ' and ').replace('é', 'e').replace('á', 'a')
    s = re.sub(r"[’']", '', s)
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return ' '.join(w for w in s.split() if w not in ('mahjong', 'mahj', 'mat', 'the', 'and', 'ships', 'rolled', 'neoprene'))


def bnorm(s):
    return re.sub(r'[^a-z]', '', s.lower().replace('&', 'and').replace('mahjongg', 'mahjong').replace('mahjongg', 'mahjong').replace('mah jongg', 'mahjong'))


unmatched = []
applied = []
for c in notes:
    cn = norm(c['name'])
    best = []
    for r in F:
        if c['brand'] != '*' and bnorm(r[2]) != bnorm(c['brand']):
            continue
        rn = norm(r[1])
        sc = 1.0 if rn == cn else (0.95 if cn and (cn in rn or rn in cn) else difflib.SequenceMatcher(None, cn, rn).ratio())
        best.append((sc, r))
    best.sort(key=lambda x: -x[0])
    if not best or best[0][0] < 0.75:
        unmatched.append(c); continue
    top = best[0][0]
    hits = [r for sc, r in best if sc >= top - 1e-9]
    if len(hits) > 1 and top < 1.0:  # several equally-close names: only accept if they are the same mat listed twice
        pass
    for r in hits:
        k = man[r[0]]
        rec = dict(OV['mats'].get(k) or {kk: vv for kk, vv in (G.get(k) or {}).items() if kk not in ('prev', 'conf')})
        rec.update(primary=c['primary'], holiday=False, skip=False, image=r[0], by='tiffany-chat-' + TODAY)
        rec.setdefault('secondary', []); rec.setdefault('tone', 'blend'); rec.setdefault('src', 'claude-look')
        if c.get('also'):
            rec['also'] = c['also']
        if c.get('note'):
            rec['note'] = c['note']
        OV['mats'][k] = rec
        applied.append((c['brand'], c['name'], r[1], c['primary'], c.get('also', [])))
OV['updated'] = TODAY
json.dump(OV, open(OV_PATH, 'w'), indent=1, ensure_ascii=False)
sys.path.insert(0, P('scripts/colors'))
import matcolors as MC  # loads the overrides we just wrote

# ---------- audit CSV ----------
AR = list(csv.DictReader(open(AUDIT)))
inv = {v: k for k, v in man.items()}
by_type = {}
for a in AR:
    if a['mat_id'] in inv:
        by_type.setdefault(a['problem_type'], {})[inv[a['mat_id']]] = a
rename = {}
for img, a in by_type.get('raw store title', {}).items():
    m = re.match(r'rename to "(.*)"', a['suggested_fix'])
    if m:
        rename[img] = m.group(1)

# ---------- 2. names + brands ----------
BRANDFIX = {'Mahj and Moon': 'Mahj & Moon', 'Ozark Mah Jongg': 'Ozark Mahjongg'}


def clean(n):
    n = re.sub(r'\[[^\]]*\]', '', n)
    n = re.sub(r'\([^)]*(33|in\b|waterproof|retired)[^)]*\)', '', n, flags=re.I)
    n = re.sub(r'\(\s*retired\s*\)', '', n, flags=re.I)
    n = re.sub(r'\b(pre[- ]?order|preorder)\b[^|]*', '', n, flags=re.I)
    n = re.sub(r'\bships\s+rolled\b', '', n, flags=re.I)
    n = re.sub(r'\d+(\.\d+)?\s*("|in|inch(es)?)?\s*[x×]\s*\d+(\.\d+)?\s*("|in|inch(es)?|cm)?', '', n, flags=re.I)
    n = re.sub(r'\b\d+\s*(in|cm)\b', '', n, flags=re.I)
    n = re.sub(r'\b(mahjong|mahj)\s+(playing\s+|table\s+)?mats?\b', '', n, flags=re.I)
    n = re.sub(r'\s*[|]\s*', ' | ', n)
    n = re.sub(r'(\s*[-–|:/]\s*)+$', '', n.strip())
    n = re.sub(r'^(\s*[-–|:/]\s*)+', '', n)
    n = re.sub(r'\s*-\s*(-\s*)+', ' - ', n)
    n = re.sub(r'\s{2,}', ' ', n).strip(' -–|:/')
    if n.isupper() and len(n) > 4:
        n = re.sub(r"\b([A-Z])([A-Z']*)\b", lambda m: m.group(1) + m.group(2).lower(), n)
    return n


rows = []
for r in F:
    if r[0] in held:
        continue
    img, name, brand, url, ret, _sec, code = r
    raw = name
    ret = 1 if (ret or re.search(r'\(\s*retired\s*\)', name, re.I) or img in by_type.get('"(retired)" in name but not flagged retired', {})) else 0
    nm = clean(rename.get(img, name)) or clean(name) or name
    brand = BRANDFIX.get(brand, brand)
    rows.append(dict(img=img, key=man[img], name=nm, raw=raw, brand=brand, url='' if ret else url, ret=ret, code=code, old=_sec))

# ---------- 3. hide ----------
hidden = {}  # img -> reason


def hide(img, why):
    if img not in hidden:
        hidden[img] = why


R = {x['img']: x for x in rows}
for img in by_type.get('placeholder image', {}):
    if img in R: hide(img, 'placeholder image ("Photo coming soon")')
for img, a in by_type.get('wrong image (shows another mat)', {}).items():
    if img in R: hide(img, 'wrong image: ' + a['detail'])
for img, a in by_type.get('lifestyle/table scene', {}).items():
    if img in R and 'no mat visible' in a['detail']: hide(img, 'image shows no mat: ' + a['detail'])

# ---------- 4. dedupe ----------
groups = []  # (keep, [drop], reason)


def score_keep(x):  # cleanest name and a working URL win
    s = 0
    if x['url']: s += 100
    if x['key'].startswith('alb'): s -= 20
    if re.search(r'ships rolled|\d+\s*x\s*\d+|pre-?order|imperfect|copy', x['raw'] + ' ' + x['key'], re.I): s -= 30
    if re.search(r'mahjong mat', x['raw'], re.I): s -= 5
    if re.search(r'sca_ref|ref=|\?.*aff', x['url'] or ''): s += 3
    s -= len(x['raw']) / 100
    return s


def add_group(imgs, reason, keep=None):
    imgs = [i for i in dict.fromkeys(imgs) if i in R]
    live = [i for i in imgs if i not in hidden]
    if len(imgs) < 2:
        return
    for g in groups:  # merge overlapping groups
        if set(g['all']) & set(imgs):
            g['all'] = list(dict.fromkeys(g['all'] + imgs)); g['reason'] += '; ' + reason
            if keep: g['keep'] = keep
            return
    groups.append({'all': imgs, 'reason': reason, 'keep': keep})


pairs = json.load(open(PAIRS))
for d, cd, a, b in pairs:
    if d <= 6 and cd <= 5 and a in R and b in R and R[a]['brand'] == R[b]['brand']:
        add_group([a, b], f'same image (phash {d}, color diff {cd})')
# same-brand names that differ only by size / Ships Rolled / Mahjong Mat suffixes
nk = {}
for x in rows:
    k = (bnorm(x['brand']), norm(clean(x['raw'])))
    nk.setdefault(k, []).append(x['img'])
for k, imgs in nk.items():
    if len(imgs) > 1 and k[1]:
        add_group(imgs, 'same name after removing size/Ships Rolled/Mahjong Mat')
# audit-listed duplicates (same mat listed twice / collab under both brands)
for t_ in ('duplicate mat (same/near-identical name in brand)', 'duplicate mat (same image hash)'):
    for img, a in by_type.get(t_, {}).items():
        m = re.search(r'#(\d+)', a['detail'])
        if m:
            other = [inv[b['mat_id']] for b in AR if b['seq'] == m.group(1) and b['mat_id'] in inv]
            if other: add_group([img, other[0]], 'audit: ' + a['detail'][:80])
add_group(['four-winds-social--fws-x-mahj-mood-collab-rally-in-pink', 'mahj-mood--rally-in-pink'], 'collab listed under both brands', keep='mahj-mood--rally-in-pink')
add_group(['four-winds-social--fws-x-mahj-mood-eloise', 'mahj-mood--the-eloise-collection-mat-collab-with-four-winds-social'], 'collab listed under both brands', keep='mahj-mood--the-eloise-collection-mat-collab-with-four-winds-social')

dd_rows = []
for g in groups:
    cands = [i for i in g['all'] if i not in hidden]  # a wrong-image listing never wins
    if not cands:
        continue
    keep = g['keep'] if g['keep'] in cands else max(cands, key=lambda i: score_keep(R[i]))
    # wrong-image Peace Love / Let's Mahj On pairs: the hidden one is already out, nothing else to drop
    drops = [i for i in g['all'] if i != keep]
    for i in drops:
        if i not in hidden:
            hide(i, f'duplicate of {keep} ({g["reason"][:90]})')
    dd_rows.append([len(dd_rows) + 1, R[keep]['brand'], keep, R[keep]['name'], R[keep]['url'] or '(retired)', ' | '.join(drops),
                    ' | '.join(R[i]['raw'] for i in drops), ' | '.join('hidden: wrong image' if hidden[i].startswith('wrong') else 'hidden: duplicate' for i in drops), g['reason']])

# ---------- 5. sections ----------
COL = [('pink', 'Pink'), ('red', 'Red'), ('orange', 'Orange & Peach'), ('yellow', 'Yellow & Mustard'), ('green', 'Green'), ('teal', 'Teal & Aqua'),
       ('blue', 'Blue'), ('purple', 'Purple & Lilac'), ('brown', 'Brown & Tan'), ('neutral', 'Neutral & Ivory'), ('bw', 'Black & White'),
       ('dark', 'Dark & Moody'), ('holiday', 'Holiday'), ('multi', 'Multicolor')]
SEC = {'gold': 'yellow', 'peach': 'orange', 'coral': 'orange', 'mustard': 'yellow'}
VALID = {c for c, _ in COL}


def sections(x):
    r = MC.get(x['key'])
    if r is None:
        return [x['old']]
    if r.get('holiday'):
        out = ['holiday']
    else:
        out = [SEC.get(r['primary'], r['primary'])]
    for a in r.get('also', []) or []:
        a = SEC.get(a, a)
        if a in VALID and a not in out:
            out.append(a)
    return [c for c in out if c in VALID] or [x['old']]


vis = [x for x in rows if x['img'] not in hidden]
for x in vis:
    x['secs'] = sections(x)
order = {c: i for i, (c, _) in enumerate(COL)}
vis.sort(key=lambda x: (order.get(x['secs'][0], 99), x['brand'].lower(), x['name'].lower()))

active = [x for x in vis if not x['ret']]
retired = [x for x in vis if x['ret']]
cnt = {c: sum(1 for x in active if c in x['secs']) for c, _ in COL}
cnt_with_ret = {c: sum(1 for x in vis if c in x['secs']) for c, _ in COL}
cnt['retired'] = len(retired)

# ---------- side outputs ----------
with open(os.path.join(HERE, 'dedupe_oct20.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['group', 'brand', 'kept_img', 'kept_name', 'kept_url', 'dropped_imgs', 'dropped_raw_names', 'what_happened', 'why'])
    w.writerows(dd_rows)
with open(os.path.join(HERE, 'hidden_oct20.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['img', 'catalog_key', 'brand', 'name_in_catalog', 'reason'])
    for img, why in sorted(hidden.items(), key=lambda kv: (kv[1].split(':')[0].split(' (')[0], kv[0])):
        w.writerow([img, R[img]['key'], R[img]['brand'], R[img]['raw'], why])
json.dump({'section_counts_active': cnt, 'section_counts_if_retired_shown': cnt_with_ret, 'unique_active_mats': len(active),
           'retired': len(retired), 'hidden': len(hidden), 'dedupe_groups': len(dd_rows), 'held_low_out': len(held),
           'applied_color_calls': applied, 'unmatched_color_calls': unmatched,
           'renamed': {x['img']: [x['raw'], x['name']] for x in vis if x['raw'] != x['name']}},
          open(os.path.join(HERE, 'v2_counts.json'), 'w'), indent=1, ensure_ascii=False)

# ---------- HTML ----------
CSS = open(os.path.join(HERE, 'style.css')).read() + '.mmg-chip.mmg-tog{border-style:dashed}\n.mmg-chip.mmg-tog[aria-pressed="true"]{border-style:solid}\n'
data = json.dumps([[x['img'], x['name'], x['brand'], x['url'], x['ret'], x['secs'], x['code']] for x in vis],
                  separators=(',', ':'), ensure_ascii=False).replace('</', '<\\/')
chips = ('<button type="button" class="mmg-chip" data-f="all" aria-pressed="true">All mats</button>'
         + ''.join(f'<button type="button" class="mmg-chip" data-f="{c}" aria-pressed="false">{html.escape(l)}</button>' for c, l in COL if cnt[c])
         + (f'<button type="button" class="mmg-chip" data-f="retired" aria-pressed="false">Retired</button>' if retired else '')
         + '<button type="button" class="mmg-chip mmg-tog" data-t="ret" aria-pressed="true">Hide retired</button>')
brands = sorted({x['brand'] for x in vis}, key=str.lower)
opts = '<option value="">All brands</option>' + ''.join(f'<option>{html.escape(b)}</option>' for b in brands)
secs = ''.join(f'<section class="mmg-sec" data-c="{c}"><h2 class="mmg-h">{html.escape(l)} mahjong mats</h2><ul class="mmg-grid"></ul><p class="mmg-empty">No mats here from that brand yet.</p></section>'
               for c, l in COL if cnt_with_ret[c])
secs += '<section class="mmg-sec" data-c="retired"><h2 class="mmg-h">Retired mats</h2><p class="mmg-intro">No longer sold, kept here so you can see what goes with the tiles you already own.</p><ul class="mmg-grid"></ul><p class="mmg-empty">No retired mats from that brand.</p></section>' if retired else ''
JS = r"""(function(){var r=document.currentScript.parentNode,R=JSON.parse(r.querySelector('script[type="application/json"]').textContent),B='https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@__C__/assets/mats/gallery/',f='all',br='',hr=true;
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function card(x,i){var shop=x[3]?'<a class="mmg-shop" href="'+esc(x[3])+'" target="_blank" rel="sponsored noopener">Shop the mat</a>':'<span class="mmg-ret">Retired</span>';var img='<img src="'+B+x[0]+'.webp" alt="'+esc(x[2]+' '+x[1])+' mahjong mat" loading="lazy" decoding="async" width="640" height="640">';return '<li class="mmg-card" data-b="'+esc(x[2])+'" data-i="'+i+'"'+(x[4]?' data-r="1"':'')+'>'+(x[3]?'<a class="mmg-img" href="'+esc(x[3])+'" target="_blank" rel="sponsored noopener">'+img+'</a>':'<span class="mmg-img">'+img+'</span>')+'<div class="mmg-body"><span class="mmg-brand">'+esc(x[2])+'</span><span class="mmg-name">'+esc(x[1])+'</span>'+(x[6]?'<a class="mmg-code" href="'+esc(x[6])+'">'+esc(x[2])+' guide</a>':'')+shop+'</div></li>'}
r.querySelectorAll('.mmg-sec').forEach(function(s){var c=s.dataset.c,h='';R.forEach(function(x,i){if(c==='retired'?x[4]:x[5].indexOf(c)>-1)h+=card(x,i)});s.querySelector('.mmg-grid').innerHTML=h});
var chips=r.querySelectorAll('.mmg-chip[data-f]'),tog=r.querySelector('.mmg-tog'),sel=r.querySelector('.mmg-brand-sel'),tot=r.querySelector('.mmg-total');
function go(){var seen={},all=0;chips.forEach(function(x){x.setAttribute('aria-pressed',x.dataset.f===f?'true':'false')});tog.setAttribute('aria-pressed',hr?'true':'false');r.querySelectorAll('.mmg-sec').forEach(function(s){var c=s.dataset.c,on=f==='all'||c===f,n=0;s.hidden=!on;if(!on)return;s.querySelectorAll('.mmg-card').forEach(function(d){var ok=(!br||d.dataset.b===br)&&!(hr&&c!=='retired'&&d.dataset.r);d.hidden=!ok;if(ok){n++;if(!seen[d.dataset.i]){seen[d.dataset.i]=1;all++}}});s.querySelector('.mmg-empty').style.display=n?'none':'block';if(!n&&f==='all')s.hidden=true});tot.textContent=all+' mats'}
chips.forEach(function(x){x.addEventListener('click',function(){f=x.dataset.f;go()})});tog.addEventListener('click',function(){hr=!hr;go()});sel.addEventListener('change',function(){br=sel.value;go()});go()})();""".replace('__C__', COMMIT)
print(f"""<style>{CSS}</style>
<div class="mmg"><span class="mmg-eyebrow">The Mat Library</span>
<h1 class="mmg-title">Mahjong Mats by Color</h1>
<p class="mmg-intro">Every mat in my matching library, all in one place. Browse by color or pick a brand, then tap any mat to shop it. Want to see which tiles go with a mat? <a href="/mahjong-tile-matches">See my tile matches</a>, and watch for Find Your Match, coming 10.27.</p>
<div class="mmg-chips" role="group" aria-label="Filter mats by color">{chips}</div>
<div class="mmg-tools"><label for="mmg-brand">Brand</label><select id="mmg-brand" class="mmg-brand-sel">{opts}</select><span class="mmg-total" aria-live="polite"></span></div>
{secs}
<script type="application/json">{data}</script>
<script>{JS}</script></div>""")
log('active', len(active), 'retired', len(retired), 'hidden', len(hidden), 'groups', len(dd_rows), 'unmatched', len(unmatched))
log(json.dumps(cnt))
