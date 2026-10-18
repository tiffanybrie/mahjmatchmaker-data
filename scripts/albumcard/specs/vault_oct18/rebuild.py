"""Oct 18 final vault albums (Tiffany's Ready to Ship answers, Oct 18 12:21-12:31):
- order = her saved drag order (c5-v-<set>.order), cover excluded
- Lilac Soiree: cancel Larkspur. Preppy Soiree: cancel Larkspur + Cognac. Shangri La: Yes as is.
- Spring Love: Goldie = clean bright photo assets/mats/clean/goldie-omm.png.
- All: re-render with current gen2 (OMM flag in the approved spot beside the navy logo box),
  footer = MAHJMATCH code (gen2 default), fonts from assets/fonts.
Specs come from the Oct 15 v2 build (scratchpad cards_v5/vault_work/<set>/spec.json, copied to specs/vault_oct18/src/)."""
import json, os, sys, io, base64, subprocess
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'; D = R + 'scripts/albumcard/specs/vault_oct18/'
ORDER = {  # her saved order (mat slugs), Oct 18
 'lilac-soiree': ['chantilly','jade','astor','birdie-pink','amethyst','lorelei','peri-twinkle','enchanted','sweet-marie'],
 'preppy-soiree': ['chantilly','jade','hawthorne','astor','elysium','luna','isla','amethyst','radiance','vivara','peri-twinkle','bam-bird-boutique-navy-vegan-leather','sedona','miracle'],
 'shangri-la': ['jade','camellia','esme','birdie-green','birdie-pink','veranda','spring-fling','elysium','luna','mirage','soho','cognac','merriment','yuletide','winterberry'],
 'spring-love': ['zen-glow','vivienne','goldie','camellia','larkspur','mirage','delilah','serengeti','spring-fling','amethyst','lorelei','jade','birdie-green','veranda','clara','sugarplum','yuletide'],
}
def key(f):
    f = f.replace('-mat.jpg', '')
    for p in ('-oh-my-mahjong-', '-bam-bird-boutique-'):
        if p in f: return ('bam-bird-boutique-' if 'bam-bird' in p else '') + f.split(p)[-1]
    return f
def gold():
    im = Image.open(R + 'assets/mats/clean/goldie-omm.png').convert('RGBA')
    bb = im.getbbox(); im = im.crop(bb); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3])
    W, H = bg.size; s = min(W, H); bg = bg.crop(((W - s)//2, (H - s)//2, (W - s)//2 + s, (H - s)//2 + s))
    bg.thumbnail((1400, 1400)); b = io.BytesIO(); bg.save(b, 'JPEG', quality=92)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
for s, order in ORDER.items():
    spec = json.load(open(D + f'src/{s}/spec.json'))
    by = {key(c['file']): c for c in spec['cards']}
    missing = [k for k in order if k not in by]; assert not missing, (s, missing, list(by))
    cards = []
    for k in order:
        c = dict(by[k]); c.pop('code', None)
        if k == 'goldie': c['mat'] = gold()
        cards.append(c)
    spec['cards'] = cards; spec.pop('code', None); spec['_note'] = f'From the Vault: {s} final (Oct 18)'
    os.makedirs(D + 'out', exist_ok=True); json.dump(spec, open(D + f'out/{s}.json', 'w'))
    out = R + f'assets/cards/from-the-vault/{s}-v3'
    subprocess.run([sys.executable, R + 'scripts/albumcard/gen2.py', D + f'out/{s}.json', out], check=True)
    json.dump([c['file'] for c in cards], open(out + '/order.json', 'w'), indent=1)
    print(s, len(cards))
