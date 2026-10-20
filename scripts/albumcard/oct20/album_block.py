"""Album code block (same markup as site/livepatch/papaya/papaya-spritz-codeblock.html) from a manifest of rendered cards.
Usage (module): build(template_html, cards, set_name, tile_full, sha, folder) -> html
cards: [{mat, brand, file, racks, mat_racks, retired?, url?}] in her order. Card images are pinned to jsDelivr @sha."""
import re, json, html as H
import common as C
CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{sha}/assets/cards/{folder}/{file}'
def figures(cards, set_name, tile_full, sha, folder):
    return ''.join(C.figure(i, CDN.format(sha=sha, folder=folder, file=c['file']), tile_full, set_name, c['mat'], c['brand'],
                            c['racks'], c['mat_racks'], url=c.get('url'), retired=c.get('retired', False)) for i, c in enumerate(cards, 1))
def build(tpl, cards, set_name, tile_full, sha, folder):
    figs = figures(cards, set_name, tile_full, sha, folder)
    m = re.search(r'(<div class="mm3-grid">)(.*?)(</div></section>)', tpl, re.S)
    out = tpl[:m.start(2)] + figs + tpl[m.end(2):]
    t = [f"{c['mat']} by {c['brand']}" for c in cards[:3]]
    top = f'My top mat picks for {set_name} are {t[0]}, {t[1]} and {t[2]}.'
    nb = len({c['brand'] for c in cards})
    out = re.sub(r'My top mat picks for [^<]*?\. Below are \d+ [^<]*? mat matches from \d+ brands, and counting,',
                 H.escape(top, quote=False) + f' Below are {len(cards)} {set_name} mat matches from {nb} brands, and counting,', out)
    out = re.sub(r'("text": ")My top mat picks for [^"]*?(")', lambda x: x.group(1) + top.replace('"', '\\"') + x.group(2), out)
    return out
