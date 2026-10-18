"""Build final vault album code blocks (Oct 18) from the 11:14 vault blocks + v3 cards.
Usage: build_vault.py <commit>   (commit must contain assets/cards/from-the-vault/<set>-v3/)"""
import re, sys, json, html
SHA = sys.argv[1]
S = '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/sunday_live/'
R = '/home/claude/mahjmatchmaker-data/'
NAMES = {'bam-bird-boutique-navy-vegan-leather': ('Navy Vegan Leather', 'Bam Bird Boutique')}
for s in ['lilac-soiree', 'preppy-soiree', 'shangri-la', 'spring-love']:
    src = open(S + f'{s}_codeblock.html').read()
    order = json.load(open(R + f'assets/cards/from-the-vault/{s}-v3/order.json'))
    figs = list(re.finditer(r'<figure class="mm3-c[^"]*".*?</figure>', src, re.S))
    def slug(f):
        m = re.search(r'mahjong-tiles-(?:oh-my-mahjong-)?([a-z0-9-]+)-mat\.jpg', f)
        return m.group(1)
    byslug = {slug(m.group(0)): m.group(0) for m in figs}
    want = [re.search(r'mahjong-tiles-(?:oh-my-mahjong-)?([a-z0-9-]+)-mat\.jpg', f).group(1) for f in order]
    miss = [w for w in want if w not in byslug]; assert not miss, (s, miss, list(byslug))
    newfigs = []
    for i, (w, f) in enumerate(zip(want, order), 1):
        x = byslug[w]
        x = re.sub(r'src="https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]+/assets/cards/[^"]*?/' + re.escape(f) + '"',
                   f'src="https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{SHA}/assets/cards/from-the-vault/{s}-v3/{f}"', x)
        assert f'{s}-v3/{f}' in x, (s, f)
        x = re.sub(r'<span class="mm3-n">\d+</span>', f'<span class="mm3-n">{i}</span>', x)
        newfigs.append(x)
    # drop cancelled figures, fill remaining slots in document order
    keep = [m for m in figs if slug(m.group(0)) in want]
    out = []; last = 0; k = 0
    for m in figs:
        out.append(src[last:m.start()])
        if slug(m.group(0)) in want:
            out.append(newfigs[k]); k += 1
        last = m.end()
    out.append(src[last:]); blk = ''.join(out)
    # cover/hero images -> v3 folder
    blk = re.sub(r'(https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@)[0-9a-f]+(/assets/cards/(?:codefooter-v1/cards/)?from-the-vault/' + s + r'/)(00-[^"]+)',
                 lambda m: f'{m.group(1)}{SHA}/assets/cards/from-the-vault/{s}-v3/{m.group(3)}', blk)
    # FAQ top picks = first three in her order
    def nm(w): return NAMES.get(w, (w.replace('-', ' ').title().replace('Peri Twinkle', 'Peri-twinkle').replace('Soho', 'SoHo'), 'Oh My Mahjong'))
    t = [f'{nm(w)[0]} by {nm(w)[1]}' for w in want[:3]]
    blk = re.sub(r'(My top mat picks for [^"]+? are )[^"]+?(\.")', lambda m: m.group(1) + f'{t[0]}, {t[1]} and {t[2]}' + m.group(2), blk)
    old = [u for u in re.findall(r'from-the-vault/' + s + r'/[^"]+', blk)]
    open(R + f'site/livepatch/albums/{s}.html', 'w').write(blk)
    print(s, len(newfigs), 'leftover old paths:', len(old))
