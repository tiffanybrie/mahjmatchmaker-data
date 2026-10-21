"""Kerry (Betty June & Jeannette) match cards into 11 live album pages (Tiffany Oct 21 3:39pm).
Builds one <figure class="mm3-c"> per set (kerry-<set>.html) + kerry_fix.js (insert after her top 3, renumber, bump counts).
Usage: python3 build.py <card commit sha> <dir of curled live pages>"""
import json, re, sys, html, os
R = '/home/claude/mahjmatchmaker-data/'
SHA, LIVE = sys.argv[1], sys.argv[2]
RM = {k: v[0] for k, v in json.load(open('rackmap.json')).items()}
RM['Mahj Mood Scalloped Clear Acrylic'] = 'https://mahjmood.com/products/copy-scalloped-clear-acrylic-rack-and-pusher-set-of-4?ref=Mahjmatchmaker'
SPEC = json.load(open(R + 'scripts/albumcard/specs/kerry.json'))
MATR = json.load(open(R + 'config/mat-racks-picks.json'))['kerry']['racks']
SHOP = 'https://go.shopmy.us/p-96114928'
out = {}
for c in SPEC['cards']:
    s = c['set']; h = open(f'{LIVE}/{s}.html').read()
    g = h.find('<div class="mm3-grid">'); f0 = re.search(r'<figure class="mm3-c"[\s\S]*?</figure>', h[g:]).group(0)
    name = re.search(r'<h3>(.*?) \+ ', f0).group(1)
    tb = re.search(r'alt="(.*?) ' + re.escape(name) + ' mahjong tiles with', f0)
    tb = tb.group(1) if tb else 'Oh My Mahjong'
    racks, seen = [], set()
    for r in c['racks'] + MATR:
        if r not in seen: seen.add(r); racks.append(f'<a href="{RM[r]}" target="_blank" rel="sponsored noopener">{html.escape(r)}</a>')
    code = ''  # no code on the Kerry; the code line sits in the note (it works on the OMM tiles, not the mat)
    note = ("The Kerry is a watercolor chinoiserie mat in pinks, greens and soft blues. We do not have a code for Betty June &amp; Jeannette; code MAHJMATCH works on " + name + " tiles."
            if s != 'coquette' else "The Kerry is a watercolor chinoiserie mat in pinks, greens and soft blues. Note that we do not have a code for this brand.")
    fig = (f'<figure class="mm3-c"><div class="mm3-im"><img src="https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{SHA}/assets/cards/kerry/{c["file"]}" data-lb="" '
           f'alt="{tb} {name} mahjong tiles with Betty June &amp; Jeannette The Kerry mahjong mat" loading="lazy" width="750" height="938">'
           f'<a class="mm3-pin" href="#" target="_blank" rel="noopener" aria-label="Save to Pinterest">Save</a></div><figcaption><span class="mm3-n">NN</span>'
           f'<h3>{name} + Kerry</h3><span class="mm3-by">Mat by Betty June &amp; Jeannette</span><div class="mm3-take"><p>{note}</p></div>'
           f'<div class="mm3-l"><a class="mm3-btn" href="{SHOP}" target="_blank" rel="sponsored noopener">Shop the Kerry Mat</a>{code}</div>'
           f'<div class="mm3-rk" style="margin-top:8px;font-size:.82em;line-height:1.55">Racks shown: {" · ".join(racks)}</div></figcaption></figure>')
    open(f'kerry-{s}.html', 'w').write(fig); out[s] = {'name': name, 'tile_brand': tb, 'file': f'kerry-{s}.html'}
json.dump(out, open('manifest.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
