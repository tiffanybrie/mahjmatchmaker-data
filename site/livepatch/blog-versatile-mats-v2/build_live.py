"""Live code block for /blog/most-versatile-mahjong-mats (Tiffany approved v3 + tip edit, Oct 25 8:19pm).
Step 1: python3 build_live.py images   -> saves the product photos to assets/blog/most-versatile-mahjong-mats/ (white bg)
Step 2: commit + push, then python3 build_live.py block <commit>  -> live-block.html (images pinned on jsDelivr at <commit>)
Reuses the live post's own <style> (.mmart) so the look matches the rest of the blog."""
import io, json, os, re, sys, unicodedata, urllib.request
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(D + '/../../..')
IMGDIR = REPO + '/assets/blog/most-versatile-mahjong-mats'
src = open(D + '/build.py').read()
exec(src[:src.index('\ndef card(')])  # P, PHOTO, RETIRED, COGNAC_CARD, MATS, SECT, sets()

FYM = open('/home/claude/fymlive/index.html').read()
DD, _ = json.JSONDecoder().raw_decode(FYM[FYM.index('const D=') + 8:])
ALB = {st['name']: st.get('album') for st in DD['sets']}


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def fname(name, brand):
    return f'{slug(name)}-{slug(brand)}-mahjong-mat.jpg'


if sys.argv[1] == 'images':
    os.makedirs(IMGDIR, exist_ok=True)
    for sec in MATS.values():
        for name, brand, *_ in sec:
            if name == 'Cognac':
                continue
            u = P[name]['img'][PHOTO[name]].split('?')[0] + '?width=1200'
            b = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read()
            im = Image.open(io.BytesIO(b)).convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
            im = Image.alpha_composite(bg, im).convert('RGB'); im.thumbnail((1000, 1000))
            im.save(f'{IMGDIR}/{fname(name, brand)}', 'JPEG', quality=84); print(fname(name, brand))
    sys.exit()

commit = sys.argv[2]
CDN = f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{commit}/assets/blog/most-versatile-mahjong-mats/'
live = open('/tmp/claude-0/-home-claude/f4da3022-6ec8-595a-90aa-668aea191899/scratchpad/vmats/live.html').read()
style = re.search(r'<style>\.mmart\{.*?</style>', live, re.S).group(0)
BRANDPAGE = {'Oh My Mahjong': '/oh-my-mahjong-discount-code', 'Charleston Mahjong Club': '/charleston-mahjong-club-discount-code',
             'Bam Bird Boutique': '/bam-bird-boutique-discount-code', 'Mahj & Vine': '/mahj-and-vine-discount-code',
             'Tigre de Tartan': '/tigre-de-tartan-discount-code', 'Sunday Mahjong': '/sunday-mahjong-discount-code',
             'Mahjong Row & Co.': '/mahjong-row-and-co-discount-code'}


def setlinks(name, n=8):
    s = P[name]['sets'][:n]
    a = [f'<a href="{ALB[x].replace("https://www.mahjmatchmaker.com", "")}">{x}</a>' if ALB.get(x) else x for x in s]
    return a[0] if len(a) == 1 else ', '.join(a[:-1]) + ' and ' + a[-1]


def mat(name, brand, title, text):
    m = DD['mats'].get(P[name]['key'], {})
    shop = m.get('u') if name != 'Cognac' else None
    nm = title.split(' by ')[0]
    head = (f'<a href="{shop}" target="_blank" rel="sponsored noopener">{nm}</a>' if shop else nm) + f' by <a href="{BRANDPAGE[brand]}">{brand}</a>'
    if name == 'Cognac':
        fig = f'<figure class="mmart-fig"><img src="{COGNAC_CARD}" alt="Heritage 2.0 tiles on the Oh My Mahjong Cognac mat" loading="lazy"><figcaption>Heritage 2.0 tiles on the Cognac mat</figcaption></figure>'
    else:
        fig = f'<figure class="mmart-fig"><img src="{CDN}{fname(name, brand)}" alt="{title} mahjong mat" loading="lazy"></figure>'
    return f'<h3>{head}</h3>\n{fig}\n<p>{text}</p>\n<p><strong>See it with</strong> {setlinks(name)}.</p>\n'


out = [style, '<article class="mmjg mmart" id="most-versatile-mahjong-mats">',
       '<p class="mmart-dek">The mats I reach for again and again, because they work with so many tile sets.</p>',
       "<p>If you're only buying one or two mats, marry the versatile one, then date the rest. You want a mat that plays nicely with the tiles you have now <em>and</em> the tiles you'll fall for next year. These are the ones that keep showing up in my match albums, from lots of different brands.</p>"]
for k in ('leather', 'color', 'earthy', 'dark'):
    h, intro = SECT[k]
    out.append(f'<h2>{h}</h2>\n<p>{intro}</p>')
    out += [mat(*m) for m in MATS[k]]
out.append("<h2>Retired favorites worth hunting for</h2>\n<p>Spring Fling, Citrus Songbird and Enchanted by Oh My Mahjong were some of the most versatile mats I've ever matched. They're retired, so if you see one in a mahjong buy/sell group, grab it.</p>")
out.append('<div class="mmart-pair">' + ''.join(f'<figure class="mmart-fig" style="margin:0"><span class="mmart-tag">Retired</span><img src="{u}" alt="Amara tiles on the retired Oh My Mahjong {n} mat" loading="lazy"><figcaption>{n}</figcaption></figure>' for n, u in RETIRED) + '</div>')
out.append("""<h2>How to pick a mat that works with everything</h2>
<ul>
<li><strong>Start with leather or a leather look.</strong> Solid, warm neutrals go with almost every tile set.</li>
<li><strong>Look for three or more colors.</strong> Different tile backs can each pull a different one.</li>
<li><strong>Don't fear green.</strong> Your bams are green, so earthy greens and natural textures like rattan and basketweave are always in play.</li>
<li><strong>Test it in <a href="/find-your-match">Find <em>Your</em> Mat-ch™</a>!</strong> Start with the mat you're eyeing and swipe through the tile sets you own. If it works with all of them, you've found your versatile mat.</li>
</ul>
<div class="mmart-box"><p><strong>Ready to pick your mat?</strong></p><p>Use code <strong>MAHJMATCH</strong> to save at our partner brands.</p><a class="mmart-btn" href="/mahjong-discount-codes">Meet our partner brands</a></div>
</article>""")
open(D + '/live-block.html', 'w').write('\n'.join(out))
print('live-block.html', len('\n'.join(out)))
