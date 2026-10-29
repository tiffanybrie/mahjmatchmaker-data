import sys, re, base64
SRC, OUT = sys.argv[1], sys.argv[2]
h = open(SRC).read()
def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c == n, (c, a[:90])
    h = h.replace(a, b)
# 1. version
rep('<title>Find Your Mat-ch (Version 1.6)</title>', '<title>Find Your Mat-ch (Version 1.7)</title>')
rep('color:var(--mute)">Version 1.6</small>', 'color:var(--mute)">Version 1.7</small>')
# 2. Shop by brand = a feature (Tiffany Oct 29 1:57pm: the code callout was weak light-gray text)
rep('.tbrw{display:flex;align-items:center;gap:10px;margin:10px 2px 8px}',
    '.bbox{margin:12px 0 10px;padding:10px 12px;background:#fff5f8;border:2px solid #c8325f;border-radius:16px;box-shadow:0 3px 12px rgba(200,50,95,.12)}.tbrw{display:flex;align-items:center;gap:10px;margin:0 0 8px}')
rep('.tbrw label{font:700 12px var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--ink,#2a2036);white-space:nowrap}',
    '.tbrw label{font:800 13px var(--body);letter-spacing:.1em;text-transform:uppercase;color:#c8325f;white-space:nowrap}')
rep('.tbrw select{flex:1;min-width:0;font:600 15px var(--body);color:var(--navy);background:#fff;border:2px solid #ead7e0;border-radius:999px;padding:9px 14px;appearance:auto}',
    '.tbrw select{flex:1;min-width:0;font:700 15px var(--body);color:var(--navy);background:#fff;border:2px solid #c8325f;border-radius:999px;padding:9px 14px;appearance:auto;box-shadow:0 2px 8px rgba(200,50,95,.15)}')
rep('.bnote{margin:-2px 2px 8px;font:600 13px/1.35 var(--body);border-radius:12px;padding:7px 11px}',
    '.bnote{margin:0;font:700 14px/1.35 var(--body);padding:0}.bnote>span{display:block;border-radius:12px;padding:8px 12px}')
rep('.bnote.ok{background:#fde8ef;color:#a3285a}.bnote.no{background:#f1eef3;color:#5e5368}.bnote.gen{background:transparent;color:var(--mute);padding:0 2px;font-size:12px}',
    '.bnote.ok>span{background:#fde8ef;color:#a3285a}.bnote.no>span{background:#f1eef3;color:#5e5368;font-weight:600}.bnote.gen>span{background:#fde8ef;color:#c8325f}.bnote b{color:#a3285a;letter-spacing:.04em;font-weight:800}')
rep('<p class="bnote gen">Partner brands come first. Save 10% or more at any of them with code <b>MAHJMATCH</b>.</p>',
    '<p class="bnote gen"><span>✦ Partner brands come first. Save 10% or more at any of them with code <b>MAHJMATCH</b></span></p>')
rep('`<p class="bnote ok">Save 10% or more at ${esc(b)} with code <b>MAHJMATCH</b></p>`',
    '`<p class="bnote ok"><span>✦ Save 10% or more at ${esc(b)} with code <b>MAHJMATCH</b></span></p>`')
rep('`<p class="bnote no">No discount available for ${esc(b)}</p>`',
    '`<p class="bnote no"><span>No discount available for ${esc(b)}</span></p>`')
rep('return `<div class="tbrw"><label for="${id}">Shop by brand</label>', 'return `<div class="bbox"><div class="tbrw"><label for="${id}">Shop by brand</label>')
rep('</select></div>${bnote(cur)}`;}', '</select></div>${bnote(cur)}</div>`;}')
# 3. card title = tile BACK colour (Tiffany Oct 29 1:31pm); ivory-back sets use their colour-card colour
TC = {'sunday-mahjong-sunday-blues': ('#d0b07e', '#283445'), 'sunday-mahjong-nature-walk': ('#56292c', '#5a1c24'),
      'sunday-mahjong-plum-panda': ('#4a1e30', '#4e2938'), 'sunday-mahjong-hummingbird': ('#5c6d40', '#a0493f'),
      'sunday-mahjong-sunday': ('#d2b586', '#b58438'), 'anders-ruff-brownstone-bloom': ('#c4ab8f', '#7b2d3b')}
for slug, (a, b) in TC.items():
    m = re.search(r'\{"slug":"%s","name":"[^"]*","maker":"[^"]*","tile":"[^"]*","tc":"%s"' % (re.escape(slug), a), h)
    assert m, slug
    s = m.group(0); h = h.replace(s, s[:-8] + b + '"', 1)
# 4. Hummingbird tile photo = the canonical album photo (fills the frame; rule 3)
FULL = sys.argv[4] if len(sys.argv) > 4 else 't103/sunday-mahjong-hummingbird.jpg'
_f = re.findall(r'"full":"[^"]*t95/sunday-mahjong-hummingbird-clean\.jpg"', h); assert len(_f) == 1, _f
h = h.replace(_f[0], '"full":"' + FULL + '"')
rep('"src":"assets/tiles/album/hummingbird.png","fo":"t16/sunday-mahjong-hummingbird.jpg"', '"src":"assets/tiles/album/hummingbird.png"')  # no reframe any more: the photo IS the album photo
m = re.search(r'"p953c390fb35e":"data:image/jpeg;base64,[^"]+"', h); assert m
h = h.replace(m.group(0), '"p953c390fb35e":"data:image/jpeg;base64,' + base64.b64encode(open(sys.argv[3], 'rb').read()).decode() + '"', 1)
open(OUT, 'w').write(h)
print('ok', len(h))
